#!/usr/bin/env python3
"""haul.py -- dynamic autonomous hauler runner for Logistics division.

WHAT: policy-driven runner (`game/haul-policy.json`, owned & tunable by Apollo/Mercury/Unity).
      Whenever a hauler runs `haul.py`, it dynamically picks and flies the best unclaimed,
      policed-safe, positive-EV job across 4 lanes:
        1. active_freight  -- resumes and delivers any in-progress spacemolt_shipping contract.
        2. public_freight  -- queries spacemolt_shipping list_all (and cached board), scores
                              safe charted policed contracts by cr/jump (+25% for Neutral partners),
                              jumps to origin, accepts & picks up crate, delivers to destination.
        3. arbitrage       -- scans fresh read.db books for safe policed buy_base -> sell_base
                              spreads, claims atomically, flies to buy_base, RE-VERIFIES live
                              view_market before buying, flies to sell_base, sells into bid
                              (or stores safely for local Bursar if bid slipped below cost).
        4. internal_supply -- moves pilot's own remotely stored needs.tsv bottleneck items home
                              to home_bases (faction storage if seated + lockbox active, else self).

USAGE:
  haul.py <pilot> [--minutes 45] [--route haul-network] [--policy game/haul-policy.json]

Stdlib only. ASCII only.
"""
import atexit
import fcntl
import json
import os
import re
import sqlite3
import sys
import threading
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division
import fuelplan
import gate

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DATA = Path(os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data")
TICK = 11
PROTECTED_ITEMS = frozenset(("fuel_cell", "antimatter_containment_cell", "repair_kit", "hull_patch"))

DEFAULT_POLICY = {
    "policed_only": True,
    "max_jumps_pickup": 12,
    "max_jumps_delivery": 25,
    "min_cr_per_jump": 80,
    "min_total_profit": 600,
    "max_collateral": 15000,
    "fuel_reserve_cr": 6000,
    "max_book_age_minutes": 30,
    "max_buy_spend_cr": 35000,
    "min_margin_pct": 0.20,
    "partners_first": True,
    "lanes": ["active_freight", "public_freight", "arbitrage", "internal_supply"],
    "home_bases": ["node_beta_industrial_station", "central_nexus", "the_experiment_research_station"],
}


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name("%s.%d.%d.tmp" % (path.name, os.getpid(), threading.get_ident()))
    tmp.write_text(json.dumps(value, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def _call_json(method, path, payload=None, timeout=120):
    st, txt = gate.call(method, path, payload, timeout=timeout)
    if isinstance(txt, (dict, list)):
        return st, txt
    try:
        return st, json.loads(txt or "{}")
    except (TypeError, ValueError):
        return st, {"error": str(txt)[:200]}


def load_policy(policy_path=None):
    merged = json.loads(json.dumps(DEFAULT_POLICY))
    path = Path(policy_path) if policy_path else (ROOT / "haul-policy.json")
    if not path.is_absolute():
        path = REPO / path
    raw = read_json(path, {})
    if isinstance(raw, dict):
        merged.update(raw)
    return merged


def ship_file_name(pilot):
    return (re.sub(r"[^A-Za-z0-9_.-]", "_", str(pilot))[:60] or "pilot") + ".json"


def _bfs_hops(lanes, src, dst):
    if not src or not dst:
        return None
    if src == dst:
        return 0
    seen = {src: 0}
    q = [src]
    while q:
        cur = q.pop(0)
        d = seen[cur]
        if d >= 50:
            continue
        for nxt in lanes.get(cur) or []:
            if nxt == dst:
                return d + 1
            if nxt not in seen:
                seen[nxt] = d + 1
                q.append(nxt)
    return None


def load_base_map(data):
    """{base_id: (system, poi, base_id, empire)} from read.db places+systems."""
    out = {}
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return out
    con = None
    try:
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if {"places", "systems"} <= tbls:
            for sys_id, poi_id, base_id, emp in con.execute("""
                SELECT p.system, p.poi, p.base, COALESCE(s.empire, '')
                FROM places p LEFT JOIN systems s ON s.id = p.system
                WHERE COALESCE(p.base, '') != ''
            """).fetchall():
                out[str(base_id)] = (str(sys_id), str(poi_id), str(base_id), str(emp or "").strip().lower())
    except sqlite3.Error:
        pass
    finally:
        if con is not None:
            con.close()
    return out


def load_stronghold_bases(data):
    out = set()
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return out
    con = None
    try:
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if {"places", "stations"} <= tbls:
            for base_id, sys_id in con.execute(
                "SELECT p.base, p.system FROM places p JOIN stations s ON LOWER(s.system)=LOWER(p.system) "
                "WHERE COALESCE(p.base,'')!='' AND (LOWER(COALESCE(s.kind,'')) LIKE '%stronghold%' OR LOWER(COALESCE(s.name,'')) LIKE '%stronghold%')"
            ).fetchall():
                out.add(str(base_id))
                out.add(str(sys_id))
    except sqlite3.Error:
        pass
    finally:
        if con is not None:
            con.close()
    return out


def pilot_has_protected_fund(data, pilot):
    try:
        import upgrades as _upg
        if pilot in _upg.protected_pilots(data):
            return True
    except Exception:
        pass
    funds = read_json(Path(data) / "fleet" / "funds.json", [])
    now_t = time.time()
    for r in funds if isinstance(funds, list) else []:
        if isinstance(r, dict) and str(r.get("pilot") or "") == str(pilot):
            st = str(r.get("state") or "")
            if st == "open" or (st == "given" and float(r.get("until") or 0) > now_t):
                return True
    return False


def docked_bursar_at(data, base_id, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    claims = read_json(Path(data) / "fleet" / "bursar_claims.json", {})
    rec = claims.get(str(base_id)) if isinstance(claims, dict) else None
    if isinstance(rec, dict) and rec.get("pilot") and (now_t - float(rec.get("at") or 0)) < 2400:
        return str(rec["pilot"])
    return ""


def neutral_partner_tags(data):
    """{tag_upper: faction_name} of active Neutral Pact diplomatic partners."""
    dip = read_json(Path(data) / "comms" / "diplomacy.json", {})
    out = {}
    if isinstance(dip, dict):
        for tag, rec in (dip.get("factions") or {}).items():
            if isinstance(rec, dict) and str(rec.get("status") or "").lower() in ("neutral", "allied", "pact"):
                out[str(tag).upper()] = str(rec.get("name") or tag)
    return out


def _unwrap_contract(entry):
    """Unwrap nested spacemolt_shipping list_all entry `{contract: {...}, eligible: ...}` safely."""
    if not isinstance(entry, dict):
        return None
    inner = entry.get("contract")
    if isinstance(inner, dict):
        flat = dict(inner)
        for wk in ("eligible", "deadline_ticks", "recovery_ticks", "target_ticks"):
            if wk in entry and wk not in flat:
                flat[wk] = entry[wk]
        return flat
    return entry


def extract_shipments(resp):
    if not isinstance(resp, dict):
        return []
    sc = resp.get("structuredContent") if isinstance(resp.get("structuredContent"), dict) else resp
    for k in ("shipments", "contracts", "active", "entries", "items"):
        v = sc.get(k)
        if isinstance(v, list):
            out = []
            for x in v:
                u = _unwrap_contract(x)
                if isinstance(u, dict):
                    out.append(u)
            return out
    return []


def claim_job(data, pilot, job_key, ttl_s=2400, now_t=None):
    """Atomically claim `job_key` in data/fleet/haul_claims.json. Returns True if claimed."""
    now_t = time.time() if now_t is None else now_t
    fdir = Path(data) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_path = fdir / "haul_claims.lock"
    claims_path = fdir / "haul_claims.json"
    with open(lock_path, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims = read_json(claims_path, {})
            if not isinstance(claims, dict):
                claims = {}
            cleaned = {k: v for k, v in claims.items()
                       if isinstance(v, dict) and (now_t - float(v.get("at") or 0)) < ttl_s and v.get("pilot") != pilot}
            if job_key in cleaned:
                write_json(claims_path, cleaned)
                return False
            cleaned[job_key] = {"pilot": pilot, "at": int(now_t)}
            write_json(claims_path, cleaned)
            return True
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def active_claimed_keys(data, ttl_s=2400, now_t=None):
    now_t = time.time() if now_t is None else now_t
    claims = read_json(Path(data) / "fleet" / "haul_claims.json", {})
    if not isinstance(claims, dict):
        return set()
    return {str(k) for k, v in claims.items() if isinstance(v, dict) and (now_t - float(v.get("at") or 0)) < ttl_s}


def release_job(data, pilot):
    fdir = Path(data) / "fleet"
    lock_path = fdir / "haul_claims.lock"
    claims_path = fdir / "haul_claims.json"
    if not claims_path.is_file():
        return
    with open(lock_path, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims = read_json(claims_path, {})
            if isinstance(claims, dict):
                changed = False
                for k in [k for k, v in claims.items() if isinstance(v, dict) and v.get("pilot") == pilot]:
                    claims.pop(k, None)
                    changed = True
                if changed:
                    write_json(claims_path, claims)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def load_available_haulers(data, pilot, cur_sys, hold_cap, avail_cash, has_hazmat, policy, claimed_pilots):
    """Return currently available Logistics haulers (including `pilot`) for global optimal job matching."""
    fuel_res = int(policy.get("fuel_reserve_cr") or 6000)
    me = {"pilot": str(pilot), "system": str(cur_sys or ""), "hold_cap": int(hold_cap),
          "avail_cash": int(avail_cash), "has_hazmat": bool(has_hazmat)}
    out = {str(pilot): me}
    fl = read_json(Path(data) / "fleet" / "fleet.json", {})
    ships = fl.get("ships") if isinstance(fl, dict) else []
    if not isinstance(ships, list):
        return [me]
    for s in ships:
        if not isinstance(s, dict):
            continue
        nm = str(s.get("name") or "")
        if not nm or nm == str(pilot) or nm in claimed_pilots:
            continue
        if str(s.get("division") or "") != "Logistics" or s.get("status") != "connected" or s.get("in_combat"):
            continue
        ord_s = str(s.get("order") or "").strip()
        if ord_s and not ord_s.startswith("haul "):
            continue
        if pilot_has_protected_fund(data, nm):
            continue
        p_cap = max(10, int(s.get("cargo_capacity") or 65) - int(s.get("cargo_used") or 0))
        p_cash = max(0, int(s.get("credits") or 0) - fuel_res)
        p_sys = str(s.get("system") or "")
        if not p_sys:
            continue
        out[nm] = {"pilot": nm, "system": p_sys, "hold_cap": p_cap, "avail_cash": p_cash, "has_hazmat": False}
    return list(out.values())


def active_claimed_pilots(data, ttl_s=2400, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    claims = read_json(Path(data) / "fleet" / "haul_claims.json", {})
    if not isinstance(claims, dict):
        return set()
    return {str(v.get("pilot")) for v in claims.values()
            if isinstance(v, dict) and v.get("pilot") and (now_t - float(v.get("at") or 0)) < ttl_s}


def assign_optimal_arbitrage(books_rows, base_map, lanes, peers, policy, claimed_keys, now_t=None, exclude_bases=None):
    """Global greedy 1-to-1 optimal matcher across available haulers and fresh arbitrage spreads."""
    now_t = time.time() if now_t is None else float(now_t)
    if not peers:
        return {}
    policed = bool(policy.get("policed_only", True))
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 25)
    min_cpj = float(policy.get("min_cr_per_jump") or 80)
    min_tot = float(policy.get("min_total_profit") or 600)
    max_age_s = float(policy.get("max_book_age_minutes") or 30) * 60.0
    max_spend_cfg = float(policy.get("max_buy_spend_cr") or 35000)
    min_margin = float(policy.get("min_margin_pct") or 0.20)

    by_item = {}
    for r in books_rows or []:
        b_id = str(r.get("base") or "")
        loc = base_map.get(b_id)
        if not loc or (policed and not loc[3]):
            continue
        if exclude_bases and (b_id in exclude_bases or loc[0] in exclude_bases):
            continue
        t = float(r.get("t") or 0)
        if t > 0 and (now_t - t) > max_age_s:
            continue
        iid = str(r.get("item") or "")
        if not iid or iid in PROTECTED_ITEMS:
            continue
        by_item.setdefault(iid, []).append((b_id, loc, float(r.get("ask") or 0), int(r.get("ask_qty") or 0),
                                            float(r.get("bid") or 0), int(r.get("bid_qty") or 0)))

    edges, hop_cache = [], {}
    def _hops(a, b):
        k = (a, b)
        if k not in hop_cache:
            hop_cache[k] = _bfs_hops(lanes, a, b) if (a and b and lanes) else (0 if a == b else 1)
        return hop_cache[k]

    for iid, entries in by_item.items():
        asks = [e for e in entries if e[2] > 0 and e[3] > 0]
        bids = [e for e in entries if e[4] > 0 and e[5] > 0]
        if not asks or not bids:
            continue
        for ab, aloc, ask_p, ask_q, _, _ in asks:
            unit_cost = ask_p * 1.05
            for bb, bloc, _, _, bid_p, bid_q in bids:
                if ab == bb or bid_p < ask_p * (1.0 + min_margin) or bid_p <= unit_cost:
                    continue
                jkey = "arb-bid:%s:%s" % (bb, iid)
                if jkey in claimed_keys:
                    continue
                d_hops = _hops(aloc[0], bloc[0])
                if d_hops is None or d_hops > max_del:
                    continue
                edges.append((jkey, iid, aloc, bloc, ask_p, ask_q, bid_p, bid_q, unit_cost, d_hops))

    if not edges:
        return {}

    scored = []
    for peer in peers:
        p_nm = str(peer["pilot"])
        p_sys = str(peer.get("system") or "")
        p_cap = int(peer.get("hold_cap") or 0)
        p_spend = min(max_spend_cfg, max(0.0, float(peer.get("avail_cash") or 0)))
        if p_cap < 1 or p_spend < 100:
            continue
        for jkey, iid, aloc, bloc, ask_p, ask_q, bid_p, bid_q, unit_cost, d_hops in edges:
            p_hops = _hops(p_sys, aloc[0]) if p_sys else 0
            if p_hops is None or p_hops > max_pick:
                continue
            qty = min(p_cap, int(ask_q), int(bid_q), int(p_spend // unit_cost))
            if qty < 1:
                continue
            tot_hops = max(1, p_hops + d_hops)
            est_profit = qty * (bid_p - unit_cost) - tot_hops * 45.0
            if est_profit < min_tot or (est_profit / tot_hops) < min_cpj:
                continue
            score = (est_profit / tot_hops) * (1.15 if p_hops <= 1 else (1.05 if p_hops <= 3 else 1.0))
            scored.append((score, est_profit, -p_hops, p_nm, jkey, {
                "job_key": jkey, "item": iid, "buy_loc": aloc, "sell_loc": bloc,
                "est_ask": int(round(ask_p)), "est_bid": int(round(bid_p)), "qty": int(qty),
                "est_profit": int(round(est_profit)), "pickup_hops": p_hops, "delivery_hops": d_hops,
            }))

    scored.sort(key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)
    assigned, used_jobs = {}, set()
    for _sc, _pr, _nh, p_nm, jkey, job in scored:
        if p_nm in assigned or jkey in used_jobs:
            continue
        assigned[p_nm] = job
        used_jobs.add(jkey)
        if len(assigned) >= len(peers):
            break
    return assigned


def assign_optimal_freight(entries, base_map, lanes, peers, policy, neutral_tags, claimed_keys,
                           exclude_bases=None, systems_meta=None, pirate_threat=None, raid_systems=None):
    """Global greedy 1-to-1 optimal matcher across available >=100c haulers and public freight contracts.

    Security invariants (Suggi, 2026-11-24):
      - Pirate strongholds are HARD-BLOCKED on endpoints AND every intermediate hop.
      - Zero blind trust for neutral/friend/player contracts into lawless space (could be decoys/traps).
      - Any route crossing lawless or pirate-sighted space requires `allow_escorted_lawless`,
        reward >= `escort_min_reward_cr`, no recent raid, and a 3/5/7/10-ship Military Convoy Escort Pack.
    """
    if not peers or not entries:
        return {}
    import escort_proto as _ep
    policed = bool(policy.get("policed_only", True))
    allow_esc = bool(policy.get("allow_escorted_lawless", False))
    esc_min_rew = float(policy.get("escort_min_reward_cr") or 15000)
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 25)
    min_cpj = float(policy.get("min_cr_per_jump") or 80)
    min_tot = float(policy.get("min_total_profit") or 600)
    max_col = float(policy.get("max_collateral") or 15000)
    partners_first = bool(policy.get("partners_first", True))
    sh_set = set(exclude_bases or ())
    sys_meta = systems_meta if isinstance(systems_meta, dict) else {loc[0]: {"empire": loc[3]} for loc in (base_map or {}).values() if isinstance(loc, (list, tuple)) and len(loc) >= 4}
    p_threat = pirate_threat or {}
    raids = raid_systems or set()

    scored = []
    for raw_c in entries:
        c = _unwrap_contract(raw_c)
        if not isinstance(c, dict):
            continue
        if c.get("eligible") is False:
            continue
        cid = str(c.get("id") or c.get("shipment_id") or "")
        if not cid or ("freight:" + cid) in claimed_keys:
            continue
        orig = str(c.get("origin_base_id") or c.get("origin_base") or "")
        dest = str(c.get("destination_base_id") or c.get("destination_base") or "")
        oloc, dloc = base_map.get(orig), base_map.get(dest)
        if not oloc or not dloc:
            continue
        if orig in sh_set or dest in sh_set or oloc[0] in sh_set or dloc[0] in sh_set:
            continue
        col = float(c.get("collateral") or c.get("failure_debt") or 0)
        rew = float(c.get("base_reward") or c.get("reward_escrow") or c.get("reward") or 0)
        if col > max_col or rew < min_tot:
            continue
        d_path = _ep.bfs_path(lanes, oloc[0], dloc[0], max_hops=max_del) if lanes else [oloc[0], dloc[0]]
        if d_path is None:
            continue
        d_hops = max(0, len(d_path) - 1) if lanes else int(c.get("jumps") or 1)
        if d_hops > max_del:
            continue
        d_risk = _ep.assess_path_threat(d_path, sys_meta, sh_set, p_threat, raids)
        if d_risk["stronghold_hit"] or d_risk["raid_hit"]:
            continue
        req_vol = int(c.get("volume") or c.get("cargo_size") or 100)
        shipper = c.get("shipper") if isinstance(c.get("shipper"), dict) else {}
        recip = c.get("recipient") if isinstance(c.get("recipient"), dict) else {}
        blob = " ".join(str(x or "") for x in (
            c.get("shipper_tag"), c.get("recipient_tag"), c.get("shipper_name"),
            shipper.get("name"), recip.get("name"),
        )).upper()
        partner = next((tag for tag in (neutral_tags or {}) if tag and tag in blob), "")
        for peer in peers:
            p_nm = str(peer["pilot"])
            if int(peer.get("hold_cap") or 0) < req_vol or float(peer.get("avail_cash") or 0) < col:
                continue
            if c.get("requires_hazmat") and not peer.get("has_hazmat"):
                continue
            p_sys = str(peer.get("system") or "")
            p_path = _ep.bfs_path(lanes, p_sys, oloc[0], max_hops=max_pick) if (p_sys and lanes) else [oloc[0]]
            if p_path is None:
                continue
            p_hops = max(0, len(p_path) - 1) if (p_sys and lanes) else 0
            if p_hops > max_pick:
                continue
            full_path = p_path + d_path[1:]
            risk = _ep.assess_path_threat(full_path, sys_meta, sh_set, p_threat, raids)
            if risk["stronghold_hit"] or risk["raid_hit"]:
                continue
            is_contested = bool(risk["lawless_hops"] or risk["pirate_hops"] or not oloc[3] or not dloc[3])
            needs_escort = False
            escort_needed = 0
            if is_contested:
                if not allow_esc or rew < esc_min_rew:
                    continue
                needs_escort = True
                escort_needed = max(3, int(risk["needed"] or 3))
            elif policed and (not oloc[3] or not dloc[3]):
                continue
            tot_hops = max(1, p_hops + d_hops)
            cpj = rew / tot_hops
            if cpj < min_cpj:
                continue
            score = cpj * (1.25 if (partners_first and partner) else 1.0) * (1.15 if p_hops <= 1 else 1.0)
            scored.append((score, rew, -p_hops, p_nm, "freight:" + cid, {
                "job_key": "freight:" + cid, "cid": cid, "pkg_id": str(c.get("package_id") or ""),
                "origin": oloc, "dest": dloc, "reward": int(round(rew)),
                "pickup_hops": p_hops, "delivery_hops": d_hops, "partner": partner,
                "needs_escort": needs_escort, "escort_needed": escort_needed,
                "threat_systems": sorted(set(risk["lawless_hops"] + risk["pirate_hops"])),
            }))

    scored.sort(key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)
    assigned, used_jobs = {}, set()
    for _sc, _rw, _nh, p_nm, jkey, job in scored:
        if p_nm in assigned or jkey in used_jobs:
            continue
        assigned[p_nm] = job
        used_jobs.add(jkey)
        if len(assigned) >= len(peers):
            break
    return assigned


def pick_freight_contract(entries, cur_sys, base_map, lanes, policy, avail_cash, has_hazmat, neutral_tags, claimed_keys, hold_cap=None, exclude_bases=None):
    """Pure selector: returns best safe eligible freight contract dict or None."""
    policed = bool(policy.get("policed_only", True))
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 25)
    min_cpj = float(policy.get("min_cr_per_jump") or 80)
    min_tot = float(policy.get("min_total_profit") or 600)
    max_col = float(policy.get("max_collateral") or 15000)
    partners_first = bool(policy.get("partners_first", True))

    best = None
    for c in entries or []:
        if not isinstance(c, dict):
            continue
        cid = str(c.get("id") or c.get("shipment_id") or "")
        if not cid or ("freight:" + cid) in claimed_keys:
            continue
        orig = str(c.get("origin_base_id") or c.get("origin_base") or "")
        dest = str(c.get("destination_base_id") or c.get("destination_base") or "")
        oloc = base_map.get(orig)
        dloc = base_map.get(dest)
        if not oloc or not dloc:
            continue
        if exclude_bases and (orig in exclude_bases or dest in exclude_bases or oloc[0] in exclude_bases or dloc[0] in exclude_bases):
            continue
        if policed and (not oloc[3] or not dloc[3]):
            continue
        if hold_cap is not None and int(hold_cap) < int(c.get('volume') or c.get('cargo_size') or 100):
            continue
        if c.get("requires_hazmat") and not has_hazmat:
            continue
        col = float(c.get("collateral") or 0)
        if col > max_col or col > avail_cash:
            continue
        rew = float(c.get("base_reward") or c.get("reward_escrow") or c.get("reward") or 0)
        if rew < min_tot:
            continue
        p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
        d_hops = _bfs_hops(lanes, oloc[0], dloc[0]) if lanes else int(c.get("jumps") or 1)
        if p_hops is None or d_hops is None:
            continue
        if p_hops > max_pick or d_hops > max_del:
            continue
        tot_hops = max(1, p_hops + d_hops)
        cpj = rew / tot_hops
        if cpj < min_cpj:
            continue
        blob = (str(c.get("shipper_tag") or "") + " " + str(c.get("recipient_tag") or "") + " " + str(c.get("shipper_name") or "")).upper()
        partner = ""
        for tag in neutral_tags or {}:
            if tag and tag in blob:
                partner = tag
                break
        score = cpj * (1.25 if (partners_first and partner) else 1.0)
        if best is None or score > best[0]:
            best = (score, {
                "job_key": "freight:" + cid,
                "cid": cid,
                "pkg_id": str(c.get("package_id") or ""),
                "origin": oloc,
                "dest": dloc,
                "reward": int(round(rew)),
                "pickup_hops": p_hops,
                "delivery_hops": d_hops,
                "partner": partner,
            })
    return best[1] if best else None


def pick_arbitrage_job(books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed_keys, now_t=None, exclude_bases=None):
    """Pure selector: returns best safe fresh cross-station arbitrage job dict or None."""
    now_t = time.time() if now_t is None else now_t
    policed = bool(policy.get("policed_only", True))
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 25)
    min_cpj = float(policy.get("min_cr_per_jump") or 80)
    min_tot = float(policy.get("min_total_profit") or 600)
    max_age_s = float(policy.get("max_book_age_minutes") or 30) * 60.0
    max_spend = min(float(policy.get("max_buy_spend_cr") or 35000), max(0.0, float(avail_cash)))
    min_margin = float(policy.get("min_margin_pct") or 0.20)
    if hold_cap < 1 or max_spend < 100:
        return None

    by_item = {}
    for r in books_rows or []:
        b_id = str(r.get("base") or "")
        loc = base_map.get(b_id)
        if not loc or (policed and not loc[3]):
            continue
        if exclude_bases and (b_id in exclude_bases or loc[0] in exclude_bases):
            continue
        t = float(r.get("t") or 0)
        if t > 0 and (now_t - t) > max_age_s:
            continue
        iid = str(r.get("item") or "")
        if not iid or iid in PROTECTED_ITEMS:
            continue
        by_item.setdefault(iid, []).append((b_id, loc, float(r.get("ask") or 0), int(r.get("ask_qty") or 0),
                                            float(r.get("bid") or 0), int(r.get("bid_qty") or 0)))

    best = None
    for iid, entries in by_item.items():
        asks = [e for e in entries if e[2] > 0 and e[3] > 0]
        bids = [e for e in entries if e[4] > 0 and e[5] > 0]
        if not asks or not bids:
            continue
        for ab, aloc, ask_p, ask_q, _, _ in asks:
            for bb, bloc, _, _, bid_p, bid_q in bids:
                if ab == bb or bid_p < ask_p * (1.0 + min_margin):
                    continue
                jkey = "arb-bid:%s:%s" % (bb, iid)
                if jkey in claimed_keys:
                    continue
                p_hops = _bfs_hops(lanes, cur_sys, aloc[0]) if cur_sys and lanes else 0
                d_hops = _bfs_hops(lanes, aloc[0], bloc[0]) if lanes else 1
                if p_hops is None or d_hops is None or p_hops > max_pick or d_hops > max_del:
                    continue
                unit_cost = ask_p * 1.05
                if bid_p <= unit_cost:
                    continue
                qty = min(int(hold_cap), int(ask_q), int(bid_q), int(max_spend // unit_cost))
                if qty < 1:
                    continue
                tot_hops = max(1, p_hops + d_hops)
                est_profit = qty * (bid_p - unit_cost) - tot_hops * 45.0
                if est_profit < min_tot or (est_profit / tot_hops) < min_cpj:
                    continue
                score = est_profit / tot_hops
                if best is None or score > best[0]:
                    best = (score, {
                        "job_key": jkey,
                        "item": iid,
                        "buy_loc": aloc,
                        "sell_loc": bloc,
                        "est_ask": int(round(ask_p)),
                        "est_bid": int(round(bid_p)),
                        "qty": int(qty),
                        "est_profit": int(round(est_profit)),
                        "pickup_hops": p_hops,
                        "delivery_hops": d_hops,
                    })
    return best[1] if best else None


def _option(args, flag, default=""):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def _heartbeat(order_path, every=60):
    stop_ev = threading.Event()
    try:
        orig_ino = os.stat(order_path).st_ino
    except OSError:
        orig_ino = None

    def beat():
        while not stop_ev.wait(every):
            try:
                st = os.stat(order_path)
                if orig_ino is not None and st.st_ino != orig_ino:
                    return
                os.utime(order_path)
            except OSError:
                return

    t = threading.Thread(target=beat, name="haul-hb", daemon=True)
    t.stop = stop_ev.set
    t.start()
    return t


def _load_books(data):
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return []
    con = None
    try:
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        con.row_factory = sqlite3.Row
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "books" not in tbls:
            return []
        return [dict(r) for r in con.execute("SELECT base, item, ask, ask_qty, bid, bid_qty, t FROM books WHERE (ask > 0 AND ask_qty > 0) OR (bid > 0 AND bid_qty > 0)").fetchall()]
    except sqlite3.Error:
        return []
    finally:
        if con is not None:
            con.close()


def _pick_internal_supply(data, pilot, base_map, lanes, cur_sys, hold_cap, policy, claimed_keys):
    """Find needed items held in THIS pilot's own storage at a remote station that should move to a home_base."""
    home_bases = [b for b in (policy.get("home_bases") or []) if b in base_map]
    if not home_bases or hold_cap < 1:
        return None
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return None
    open_needs = set()
    con = None
    try:
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
        for tbl_nm in ("need_status", "contract_candidates"):
            if tbl_nm in tbls:
                for (short_s,) in con.execute("SELECT short_items FROM %s WHERE short_items IS NOT NULL" % tbl_nm).fetchall():
                    for part in str(short_s).split(","):
                        m = re.match(r"\s*([a-z0-9_]+)\s+([\d,]+)", part.strip())
                        if m:
                            open_needs.add(m.group(1))
        if "supply_status" in tbls:
            for iid, stk, keep in con.execute("SELECT item, stock, keep FROM supply_status").fetchall():
                if iid and int(keep or 0) > 0 and int(stk or 0) < int(keep or 0):
                    open_needs.add(str(iid))
    except sqlite3.Error:
        return None
    finally:
        if con is not None:
            con.close()
    if not open_needs:
        return None
    stor = read_json(Path(data) / "stock" / "storage.json", {})
    p_stor = (stor.get("pilots") or {}).get(pilot) if isinstance(stor, dict) else None
    if not isinstance(p_stor, dict):
        return None
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 25)
    best = None
    for b_id, items in p_stor.items():
        if b_id in home_bases or b_id not in base_map or not isinstance(items, dict):
            continue
        oloc = base_map[b_id]
        if policy.get("policed_only", True) and not oloc[3]:
            continue
        for iid, qty in items.items():
            q = int(qty or 0)
            if q < 10 or iid not in open_needs:
                continue
            jkey = "supply:%s:%s:%s" % (pilot, b_id, iid)
            if jkey in claimed_keys:
                continue
            p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
            if p_hops is None or p_hops > max_pick:
                continue
            # Pick nearest home_base
            dloc, d_hops = None, None
            for hb in home_bases:
                hl = base_map[hb]
                h = _bfs_hops(lanes, oloc[0], hl[0]) if lanes else 1
                if h is not None and h <= max_del and (d_hops is None or h < d_hops):
                    dloc, d_hops = hl, h
            if dloc is None:
                continue
            take_q = min(q, int(hold_cap))
            score = take_q / max(1.0, float(p_hops + d_hops))
            if best is None or score > best[0]:
                best = (score, {"job_key": jkey, "item": iid, "qty": take_q, "origin": oloc, "dest": dloc})
    return best[1] if best else None


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        sys.exit("USAGE: haul.py <pilot> [--minutes 45] [--route haul-network] [--policy game/haul-policy.json]")
    pilot = args[0]
    division.require(pilot)
    minutes = float(_option(args, "--minutes", "45"))
    route_id = _option(args, "--route", "haul-network")
    policy_path = _option(args, "--policy", "") or None
    policy = load_policy(policy_path)

    p_enc = urllib.parse.quote(pilot, safe="")
    order_path = DATA / "fleet" / "orders" / ship_file_name(pilot)
    stop_files = (DATA / "fleet" / "host" / "stop" / pilot, DATA / "fleet" / "host" / "stop" / ship_file_name(pilot))
    started = time.time()
    notes = []
    inv_cost = [0]

    def say(msg):
        print("%s | %s | %s" % (utc_now(), pilot, msg), flush=True)

    def raw(action, params=None, group="spacemolt"):
        _, d = _call_json("POST", "/accounts/%s/raw" % p_enc, {"toolGroup": group, "action": action, "params": params or {}}, timeout=120)
        return d if isinstance(d, dict) else {}

    def body(d):
        sc = d.get("structuredContent") if isinstance(d, dict) else None
        return sc if isinstance(sc, dict) else {}

    def get_state():
        _, d = _call_json("GET", "/accounts/%s" % p_enc, timeout=60)
        return (d.get("state") or {}) if isinstance(d, dict) else {}

    def get_credits():
        return int(get_state().get("credits") or 0)

    def get_cargo():
        _, rows = _call_json("GET", "/accounts/%s/state/cargo" % p_enc, timeout=60)
        return {r.get("item_id"): int(r.get("quantity") or 0) for r in rows if isinstance(r, dict)} if isinstance(rows, list) else {}

    def run_goal(gtype, options, tries=3, timeout=900):
        waited = 0
        ans = {}
        while tries > 0:
            st, ans = _call_json("POST", "/accounts/%s/goal" % p_enc, {"type": gtype, "options": options}, timeout=timeout)
            if st == 200 and isinstance(ans, dict) and ans.get("success"):
                return True, str(ans.get("message") or "")
            err = str((ans.get("error") or ans.get("message") or st) if isinstance(ans, dict) else ans)
            if "already executing" in err and waited < 30:
                waited += 1
                time.sleep(10)
                continue
            tries -= 1
            time.sleep(10)
        msg = str((ans.get("message") or ans.get("error") or "") if isinstance(ans, dict) else ans)[:100]
        return False, msg

    def go_dock(loc):
        sys_id, poi_id, base_id = loc[0], loc[1], loc[2]
        return run_goal("prepare-at-station", {"systemId": sys_id, "poiId": poi_id, "baseId": base_id, "refuel": True})

    def save_market(base_id, sys_id):
        items = [i for i in (body(raw("view_market", {}, group="spacemolt_market")).get("items") or []) if isinstance(i, dict)]
        if items:
            rows = [{k: i.get(k) for k in ("item_id", "item_name", "category", "best_buy", "best_buy_qty", "buy_quantity", "best_sell", "best_sell_qty", "sell_quantity")} for i in items]
            write_json(DATA / "market" / ("%s.json" % base_id), {"base": base_id, "system": sys_id, "read_at": utc_now(), "source": "view_market, hauler docked", "items": rows})
        return {str(i.get("item_id")): i for i in items if i.get("item_id")}

    def stop_requested():
        if (DATA / "fleet" / "STOP").exists():
            return "fleet STOP"
        for sf in stop_files:
            if sf.exists():
                try:
                    sf.unlink()
                except OSError:
                    pass
                return "per-pilot stop file"
        return ""

    write_json(order_path, {"pilot": pilot, "what": "haul " + route_id, "since": utc_now(), "pid": os.getpid()})
    hb = _heartbeat(order_path)
    before = get_credits()
    finished = []

    def cleanup():
        if finished:
            return
        finished.append(True)
        try:
            hb.stop()
        except Exception:
            pass
        release_job(DATA, pilot)
        after = get_credits()
        mins = round((time.time() - started) / 60.0, 1)
        row = {
            "route": route_id, "kind": "haul", "pilot": pilot,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "minutes": mins, "credits_before": before, "credits_after": after,
            "delta": after - before if before and after else 0,
            "one_time": 0, "inventory_cost": inv_cost[0], "notes": notes[:12],
        }
        runs = DATA / "routes" / "runs.jsonl"
        runs.parent.mkdir(parents=True, exist_ok=True)
        with open(runs, "a", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")
        print("RESULT %s: haul %s | %.1f min | credits %d -> %d (%+d cr) | %s"
              % (pilot, route_id, mins, before, after, after - before, "; ".join(notes[:4]) or "ok"), flush=True)
        try:
            cur = read_json(order_path, {})
            if isinstance(cur, dict) and cur.get("pid") == os.getpid() and cur.get("what") == "haul " + route_id:
                order_path.unlink()
        except OSError:
            pass

    try:
        base_map = load_base_map(DATA)
        try:
            lanes = fuelplan.chart(REPO / "game")[0]
        except Exception:
            lanes = {}
        ship_doc = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
        cur_sys = str(ship_doc.get("system") or "")
        hold_cap = max(10, int(ship_doc.get("cargo_capacity") or 100) - int(ship_doc.get("cargo_used") or 0))
        mods = [str(m).lower() for m in (ship_doc.get("modules") or [])]
        has_hazmat = any("hazmat" in m for m in mods)
        avail_cash = 0 if pilot_has_protected_fund(DATA, pilot) else max(0, before - int(policy.get("fuel_reserve_cr") or 6000))
        strongholds = load_stronghold_bases(DATA) if policy.get("exclude_strongholds", True) else set()
        lane_order = list(policy.get("lanes") or DEFAULT_POLICY["lanes"])
        completed = 0

        # Flush any leftover non-protected cargo from prior runs if docked so hold capacity stays clean
        _cur_cargo = {k: v for k, v in get_cargo().items() if v > 0 and k not in PROTECTED_ITEMS and not str(k).startswith("package:")}
        _cur_base = str(ship_doc.get("base") or ship_doc.get("docked") or "")
        if _cur_cargo and _cur_base and _cur_base in base_map:
            _mb = save_market(_cur_base, base_map[_cur_base][0])
            for _iid, _qty in list(_cur_cargo.items()):
                _row = _mb.get(_iid) or {}
                _bq = int(_row.get("best_buy_qty") or _row.get("buy_quantity") or 0)
                _bp = float(_row.get("best_buy") or 0)
                if _bp >= 10 and _bq > 0:
                    _sq = min(_qty, _bq)
                    raw("sell", {"item_id": _iid, "quantity": _sq}, group="spacemolt")
                    time.sleep(TICK)
                    say("flushed %d leftover %s @ ~%d cr at %s" % (_sq, _iid, int(_bp), _cur_base))
                _left = get_cargo().get(_iid, 0)
                if _left > 0:
                    raw("deposit", {"item_id": _iid, "quantity": _left, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                    time.sleep(TICK)

        for lane in lane_order:
            if completed > 0 or stop_requested() or (time.time() - started) > minutes * 60.0:
                break
            if lane == "active_freight":
                act = extract_shipments(raw("active", {}, group="spacemolt_shipping"))
                for c in act:
                    cid = str(c.get("id") or c.get("shipment_id") or "")
                    pkg = str(c.get("package_id") or "")
                    ob = str(c.get("origin_base_id") or "")
                    db = str(c.get("destination_base_id") or "")
                    if not cid or db not in base_map:
                        continue
                    pkg_item = pkg if pkg.startswith("package:") else ("package:" + pkg)
                    if not get_cargo().get(pkg_item):
                        if ob not in base_map:
                            continue
                        ok_o, msg_o = go_dock(base_map[ob])
                        if not ok_o:
                            notes.append("active orig unreachable: %s" % msg_o[:40])
                            continue
                        raw("withdraw", {"item_id": pkg_item, "quantity": 1}, group="spacemolt_storage")
                        time.sleep(TICK)
                    ok_d, msg_d = go_dock(base_map[db])
                    if ok_d:
                        del_r = raw("deliver", {"shipment_id": cid}, group="spacemolt_shipping")
                        time.sleep(TICK)
                        say("delivered active freight %s -> %s%s" % (cid[:8], db, " ERR" if "error" in del_r else ""))
                        notes.append("active freight %s -> %s" % (cid[:8], db))
                        completed += 1
                        break

            elif lane == "public_freight":
                entries = extract_shipments(raw("list_all", {"limit": 50}, group="spacemolt_shipping"))
                if entries:
                    write_json(DATA / "fleet" / "freight_board.json", {"at": int(time.time()), "entries": entries})
                else:
                    cached = read_json(DATA / "fleet" / "freight_board.json", {})
                    if isinstance(cached, dict) and (time.time() - float(cached.get("at") or 0)) < 600:
                        entries = cached.get("entries") or []
                ntags = neutral_partner_tags(DATA)
                claimed = active_claimed_keys(DATA)
                peers = load_available_haulers(DATA, pilot, cur_sys, hold_cap, avail_cash, has_hazmat, policy, active_claimed_pilots(DATA))
                import escort_proto as _ep
                _p_thr = _ep.load_pirate_threat(DATA, hours=6.0)
                _r_sys = _ep.load_recent_raids(DATA, hours=24.0)
                _s_meta = {}
                try:
                    _db = Path(DATA) / "store" / "read.db"
                    if _db.is_file():
                        _c = sqlite3.connect("file:%s?mode=ro" % _db, uri=True, timeout=3.0)
                        try:
                            for _sid, _emp, _sh in _c.execute("SELECT id, COALESCE(empire,''), COALESCE(stronghold,0) FROM systems"):
                                _s_meta[str(_sid)] = {"empire": str(_emp or ""), "stronghold": bool(_sh)}
                        finally:
                            _c.close()
                except Exception:
                    pass
                pick = assign_optimal_freight(
                    entries, base_map, lanes, peers, policy, ntags, claimed,
                    exclude_bases=strongholds, systems_meta=_s_meta, pirate_threat=_p_thr, raid_systems=_r_sys,
                ).get(pilot)
                if pick and claim_job(DATA, pilot, pick["job_key"]):
                    cid, oloc, dloc = pick["cid"], pick["origin"], pick["dest"]
                    say("freight %s: %s -> %s (%d cr, %dj+%dj%s%s)" % (
                        cid[:8], oloc[2], dloc[2], pick["reward"], pick["pickup_hops"], pick["delivery_hops"],
                        " partner=" + pick["partner"] if pick["partner"] else "",
                        " escort=%d" % pick["escort_needed"] if pick.get("needs_escort") else ""))
                    esc_key = ""
                    try:
                        if pick.get("needs_escort"):
                            esc_key = "convoy:%s:%s" % (pilot, pick["job_key"])
                            need_n = max(3, int(pick.get("escort_needed") or 3))
                            _ep.request_escort(
                                DATA, esc_key, "convoy", pilot, route_id,
                                oloc[0], oloc[1], needed=need_n, dest_system=dloc[0],
                                threat_systems=pick.get("threat_systems") or [],
                                reason="contested_freight", priority=95,
                            )
                        ok_o, msg_o = go_dock(oloc)
                        if not ok_o:
                            notes.append("freight orig err: %s" % msg_o[:40])
                            release_job(DATA, pilot)
                            continue
                        if esc_key:
                            rally_end = time.time() + float(policy.get("escort_rally_timeout_s") or 240)
                            ready_ok = False
                            while time.time() < rally_end and not stop_requested():
                                _rec = _ep.get_escort_request(DATA, esc_key)
                                if _rec and _ep.escort_ready_count(_rec) >= int(_rec.get("needed") or 3):
                                    ready_ok = True
                                    break
                                time.sleep(10)
                            if not ready_ok:
                                say("convoy escort rally timeout (%s); aborting contested freight" % cid[:8])
                                notes.append("convoy escort timeout")
                                release_job(DATA, pilot)
                                continue
                        save_market(oloc[2], oloc[0])
                        acc = raw("accept", {"shipment_id": cid, "carrier": "player"}, group="spacemolt_shipping")
                        time.sleep(TICK)
                        if "error" in acc or (isinstance(body(acc), dict) and body(acc).get("error")):
                            say("freight accept %s refused" % cid[:8])
                            notes.append("freight accept refused")
                            release_job(DATA, pilot)
                            continue
                        pkg_item = pick["pkg_id"] if pick["pkg_id"].startswith("package:") else ("package:" + pick["pkg_id"])
                        raw("withdraw", {"item_id": pkg_item, "quantity": 1}, group="spacemolt_storage")
                        time.sleep(TICK)
                        if not get_cargo().get(pkg_item):
                            raw("return", {"shipment_id": cid}, group="spacemolt_shipping")
                            time.sleep(TICK)
                            notes.append("freight withdraw failed, returned")
                            release_job(DATA, pilot)
                            continue
                        ok_d, msg_d = go_dock(dloc)
                        if ok_d:
                            save_market(dloc[2], dloc[0])
                            del_r = raw("deliver", {"shipment_id": cid}, group="spacemolt_shipping")
                            time.sleep(TICK)
                            say("freight delivered %s -> %s (+%d cr%s)" % (cid[:8], dloc[2], pick["reward"], " ERR" if "error" in del_r else ""))
                            notes.append("freight %s +%d cr" % (cid[:8], pick["reward"]))
                            completed += 1
                    finally:
                        if esc_key:
                            _ep.clear_escort_request(DATA, esc_key)

            elif lane == "arbitrage":
                books_rows = _load_books(DATA)
                claimed = active_claimed_keys(DATA)
                peers = load_available_haulers(DATA, pilot, cur_sys, hold_cap, avail_cash, has_hazmat, policy, active_claimed_pilots(DATA))
                job = assign_optimal_arbitrage(books_rows, base_map, lanes, peers, policy, claimed, exclude_bases=strongholds).get(pilot)
                if job and claim_job(DATA, pilot, job["job_key"]):
                    iid, bloc, sloc = job["item"], job["buy_loc"], job["sell_loc"]
                    say("arb %s: %d units %s (%d cr) -> %s (%d cr) | est +%d cr" % (
                        iid, job["qty"], bloc[2], job["est_ask"], sloc[2], job["est_bid"], job["est_profit"]))
                    ok_b, msg_b = go_dock(bloc)
                    if not ok_b:
                        notes.append("arb buy dock err: %s" % msg_b[:40])
                        release_job(DATA, pilot)
                        continue
                    live_b = save_market(bloc[2], bloc[0])
                    row_b = live_b.get(iid) or {}
                    live_ask = float(row_b.get("best_sell") or 0)
                    live_ask_q = int(row_b.get("best_sell_qty") or row_b.get("sell_quantity") or 0)
                    min_m = float(policy.get("min_margin_pct") or 0.20)
                    if live_ask <= 0 or live_ask_q <= 0 or job["est_bid"] < live_ask * (1.0 + min_m):
                        say("arb %s aborted at %s: live ask %s no longer clears margin vs bid %d" % (iid, bloc[2], live_ask, job["est_bid"]))
                        notes.append("arb live ask shifted")
                        release_job(DATA, pilot)
                        continue
                    buy_q = min(job["qty"], live_ask_q, max(0, int((get_credits() - int(policy.get("fuel_reserve_cr") or 6000)) // (live_ask * 1.05))))
                    if buy_q < 1:
                        release_job(DATA, pilot)
                        continue
                    had = get_cargo().get(iid, 0)
                    run_goal("buy-items", {"items": [{"itemId": iid, "maxPrice": int(round(live_ask * 1.02)), "maxQuantity": buy_q}]}, tries=1, timeout=300)
                    got = get_cargo().get(iid, 0) - had
                    if got <= 0:
                        say("arb %s buy got 0 units at %s" % (iid, bloc[2]))
                        notes.append("arb buy got 0")
                        release_job(DATA, pilot)
                        continue
                    ok_s, msg_s = go_dock(sloc)
                    if not ok_s:
                        notes.append("arb sell dock err: %s" % msg_s[:40])
                        release_job(DATA, pilot)
                        continue
                    live_s = save_market(sloc[2], sloc[0])
                    row_s = live_s.get(iid) or {}
                    live_bid = float(row_s.get("best_buy") or 0)
                    live_bid_q = int(row_s.get("best_buy_qty") or row_s.get("buy_quantity") or 0)
                    sell_q = min(got, live_bid_q) if live_bid_q > 0 else 0
                    if live_bid >= live_ask * 1.05 and sell_q > 0:
                        d = raw("sell", {"item_id": iid, "quantity": sell_q}, group="spacemolt")
                        time.sleep(TICK)
                        say("arb sold %d %s at %s @ ~%d cr%s" % (sell_q, iid, sloc[2], int(live_bid), " ERR" if "error" in d else ""))
                        notes.append("arb sold %d %s %s->%s" % (sell_q, iid, bloc[2], sloc[2]))
                        rem_q = get_cargo().get(iid, 0)
                        if rem_q > 0:
                            inv_cost[0] += int(round(rem_q * live_ask))
                            bp = docked_bursar_at(DATA, sloc[2])
                            if bp and bp != pilot and "error" not in raw("send_gift", {"recipient": bp, "item_id": iid, "quantity": rem_q}, group="spacemolt_social"):
                                time.sleep(TICK)
                            else:
                                raw("deposit", {"item_id": iid, "quantity": rem_q, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                                time.sleep(TICK)
                    else:
                        inv_cost[0] += int(round(got * live_ask))
                        bp = docked_bursar_at(DATA, sloc[2])
                        if bp and bp != pilot and "error" not in raw("send_gift", {"recipient": bp, "item_id": iid, "quantity": got}, group="spacemolt_social"):
                            time.sleep(TICK)
                            say("arb %s bid slipped: gifted %d to Bursar %s at %s (cost %d cr)" % (iid, got, bp, sloc[2], int(round(got * live_ask))))
                            notes.append("arb->bursar %d %s (cost %d)" % (got, iid, int(round(got * live_ask))))
                        else:
                            raw("deposit", {"item_id": iid, "quantity": got, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                            time.sleep(TICK)
                            say("arb %s bid slipped: stored %d at %s (cost %d cr)" % (iid, got, sloc[2], int(round(got * live_ask))))
                            notes.append("arb stored %d %s (cost %d)" % (got, iid, int(round(got * live_ask))))
                    completed += 1

            elif lane == "internal_supply":
                claimed = active_claimed_keys(DATA)
                sup = _pick_internal_supply(DATA, pilot, base_map, lanes, cur_sys, hold_cap, policy, claimed)
                if sup and claim_job(DATA, pilot, sup["job_key"]):
                    iid, oloc, dloc, qty = sup["item"], sup["origin"], sup["dest"], sup["qty"]
                    say("supply %d %s: %s -> %s" % (qty, iid, oloc[2], dloc[2]))
                    ok_o, _ = go_dock(oloc)
                    if not ok_o:
                        release_job(DATA, pilot)
                        continue
                    raw("withdraw", {"item_id": iid, "quantity": qty, "target": "self"}, group="spacemolt_storage")
                    time.sleep(TICK)
                    have = get_cargo().get(iid, 0)
                    if have <= 0:
                        release_job(DATA, pilot)
                        continue
                    ok_d, _ = go_dock(dloc)
                    if ok_d:
                        r_dep = raw("deposit", {"item_id": iid, "quantity": have, "target": "faction", "source": "cargo"}, group="spacemolt_storage")
                        time.sleep(TICK)
                        if "error" in r_dep:
                            raw("deposit", {"item_id": iid, "quantity": have, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                            time.sleep(TICK)
                        notes.append("supply %d %s -> %s" % (have, iid, dloc[2]))
                        completed += 1

        if completed == 0:
            watch_s = float(policy.get("rest_seconds_when_empty") or (float(policy.get("idle_watch_minutes") or 15) * 60.0))
            poll_s = min(180.0, max(30.0, float(policy.get("idle_poll_interval_s") or 180.0)))
            say("no eligible haul/freight/arb/supply job matched policy right now; docked watch %ds (poll %ds)" % (int(watch_s), int(poll_s)))
            notes.append("docked watch %dm" % max(1, int(round(watch_s / 60.0))))
            end_nap = time.time() + watch_s
            next_poll = time.time() + poll_s
            while time.time() < end_nap and not stop_requested():
                time.sleep(min(20.0, max(1.0, end_nap - time.time())))
                try:
                    os.utime(order_path)
                except OSError:
                    pass
                if time.time() >= next_poll and time.time() + 30.0 < end_nap:
                    next_poll = time.time() + poll_s
                    # Re-check internal_supply & public_freight cheaply without exiting the docked watch
                    if "internal_supply" in lane_order:
                        claimed = active_claimed_keys(DATA)
                        sup = _pick_internal_supply(DATA, pilot, base_map, lanes, cur_sys, hold_cap, policy, claimed)
                        if sup and claim_job(DATA, pilot, sup["job_key"]):
                            iid, oloc, dloc, qty = sup["item"], sup["origin"], sup["dest"], sup["qty"]
                            say("watch->supply %d %s: %s -> %s" % (qty, iid, oloc[2], dloc[2]))
                            ok_o, _ = go_dock(oloc)
                            if ok_o:
                                raw("withdraw", {"item_id": iid, "quantity": qty, "target": "self"}, group="spacemolt_storage")
                                time.sleep(TICK)
                                have = get_cargo().get(iid, 0)
                                if have > 0:
                                    ok_d, _ = go_dock(dloc)
                                    if ok_d:
                                        r_dep = raw("deposit", {"item_id": iid, "quantity": have, "target": "faction", "source": "cargo"}, group="spacemolt_storage")
                                        time.sleep(TICK)
                                        if "error" in r_dep:
                                            raw("deposit", {"item_id": iid, "quantity": have, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                                            time.sleep(TICK)
                                        notes.append("supply %d %s -> %s" % (have, iid, dloc[2]))
                                        completed += 1
                                        break
                            release_job(DATA, pilot)
        return 0
    finally:
        cleanup()


if __name__ == "__main__":
    sys.exit(main())
