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
    "max_book_age_minutes": 180,
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


def neutral_partner_tags(data):
    """{tag_upper: faction_name} of active Neutral Pact diplomatic partners."""
    dip = read_json(Path(data) / "comms" / "diplomacy.json", {})
    out = {}
    if isinstance(dip, dict):
        for tag, rec in (dip.get("factions") or {}).items():
            if isinstance(rec, dict) and str(rec.get("status") or "").lower() in ("neutral", "allied", "pact"):
                out[str(tag).upper()] = str(rec.get("name") or tag)
    return out


def extract_shipments(resp):
    if not isinstance(resp, dict):
        return []
    sc = resp.get("structuredContent") if isinstance(resp.get("structuredContent"), dict) else resp
    for k in ("shipments", "contracts", "active", "entries", "items"):
        v = sc.get(k)
        if isinstance(v, list):
            return [x for x in v if isinstance(x, dict)]
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


def pick_freight_contract(entries, cur_sys, base_map, lanes, policy, avail_cash, has_hazmat, neutral_tags, claimed_keys):
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
        if policed and (not oloc[3] or not dloc[3]):
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


def pick_arbitrage_job(books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed_keys, now_t=None):
    """Pure selector: returns best safe fresh cross-station arbitrage job dict or None."""
    now_t = time.time() if now_t is None else now_t
    policed = bool(policy.get("policed_only", True))
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 25)
    min_cpj = float(policy.get("min_cr_per_jump") or 80)
    min_tot = float(policy.get("min_total_profit") or 600)
    max_age_s = float(policy.get("max_book_age_minutes") or 180) * 60.0
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
                jkey = "arb:%s:%s:%s" % (iid, ab, bb)
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
        if "contract_candidates" in tbls:
            for (short_s,) in con.execute("SELECT short_items FROM contract_candidates WHERE short_items IS NOT NULL").fetchall():
                for part in str(short_s).split(","):
                    m = re.match(r"\s*([a-z0-9_]+)\s+([\d,]+)", part.strip())
                    if m:
                        open_needs.add(m.group(1))
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
    stop_file = DATA / "fleet" / "host" / "stop" / ship_file_name(pilot)
    started = time.time()
    notes = []

    def say(msg):
        print("%s | %s | %s" % (utc_now(), pilot, msg), flush=True)

    def raw(action, params=None, group="spacemolt"):
        _, d = gate.call("POST", "/accounts/%s/raw" % p_enc, {"toolGroup": group, "action": action, "params": params or {}}, timeout=120)
        return d if isinstance(d, dict) else {}

    def body(d):
        sc = d.get("structuredContent") if isinstance(d, dict) else None
        return sc if isinstance(sc, dict) else {}

    def get_state():
        _, d = gate.call("GET", "/accounts/%s" % p_enc, timeout=60)
        return (d.get("state") or {}) if isinstance(d, dict) else {}

    def get_credits():
        return int(get_state().get("credits") or 0)

    def get_cargo():
        _, rows = gate.call("GET", "/accounts/%s/state/cargo" % p_enc, timeout=60)
        return {r.get("item_id"): int(r.get("quantity") or 0) for r in rows if isinstance(r, dict)} if isinstance(rows, list) else {}

    def go_dock(loc):
        sys_id, poi_id, base_id = loc[0], loc[1], loc[2]
        st, ans = gate.call("POST", "/accounts/%s/goal" % p_enc,
                            {"goal": "prepare-at-station", "options": {"systemId": sys_id, "poiId": poi_id, "baseId": base_id, "refuel": True}},
                            timeout=900)
        ok = (st == 200 and isinstance(ans, dict) and ans.get("ok"))
        msg = "" if ok else str((ans or {}).get("error") or (ans or {}).get("output") or st)[:100]
        return ok, msg

    def save_market(base_id, sys_id):
        items = [i for i in (body(raw("view_market", {}, group="spacemolt_market")).get("items") or []) if isinstance(i, dict)]
        if items:
            rows = [{k: i.get(k) for k in ("item_id", "item_name", "category", "best_buy", "best_buy_qty", "buy_quantity", "best_sell", "best_sell_qty", "sell_quantity")} for i in items]
            write_json(DATA / "market" / ("%s.json" % base_id), {"base": base_id, "system": sys_id, "read_at": utc_now(), "source": "view_market, hauler docked", "items": rows})
        return {str(i.get("item_id")): i for i in items if i.get("item_id")}

    def stop_requested():
        if (DATA / "fleet" / "STOP").exists():
            return "fleet STOP"
        if stop_file.exists():
            try:
                stop_file.unlink()
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
            "one_time": 0, "notes": notes[:12],
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
            if isinstance(cur, dict) and cur.get("pid") == os.getpid():
                order_path.unlink()
        except OSError:
            pass

    atexit.register(cleanup)

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
    avail_cash = max(0, before - int(policy.get("fuel_reserve_cr") or 6000))
    lane_order = list(policy.get("lanes") or DEFAULT_POLICY["lanes"])
    completed = 0

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
            pick = pick_freight_contract(entries, cur_sys, base_map, lanes, policy, avail_cash, has_hazmat, ntags, claimed)
            if pick and claim_job(DATA, pilot, pick["job_key"]):
                cid, oloc, dloc = pick["cid"], pick["origin"], pick["dest"]
                say("freight %s: %s -> %s (%d cr, %dj+%dj%s)" % (
                    cid[:8], oloc[2], dloc[2], pick["reward"], pick["pickup_hops"], pick["delivery_hops"],
                    " partner=" + pick["partner"] if pick["partner"] else ""))
                ok_o, msg_o = go_dock(oloc)
                if not ok_o:
                    notes.append("freight orig err: %s" % msg_o[:40])
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

        elif lane == "arbitrage":
            books_rows = _load_books(DATA)
            claimed = active_claimed_keys(DATA)
            job = pick_arbitrage_job(books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed)
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
                gate.call("POST", "/accounts/%s/goal" % p_enc,
                          {"goal": "buy-items", "options": {"items": [{"itemId": iid, "maxPrice": int(round(live_ask * 1.02)), "maxQuantity": buy_q}]}},
                          timeout=300)
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
                if live_bid >= live_ask * 1.05:
                    d = raw("sell", {"item_id": iid, "quantity": got}, group="spacemolt_market")
                    time.sleep(TICK)
                    say("arb sold %d %s at %s @ ~%d cr%s" % (got, iid, sloc[2], int(live_bid), " ERR" if "error" in d else ""))
                    notes.append("arb %d %s %s->%s" % (got, iid, bloc[2], sloc[2]))
                else:
                    # Bid slipped: deposit safely for local Bursar rather than panic-selling at a loss
                    raw("deposit", {"item_id": iid, "quantity": got, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                    time.sleep(TICK)
                    say("arb %s bid slipped (%s < cost %s): stored %d at %s for Bursar" % (iid, live_bid, live_ask, got, sloc[2]))
                    notes.append("arb stored %d %s at %s" % (got, iid, sloc[2]))
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
        say("no eligible haul/freight/arb/supply job matched policy right now; resting 120s")
        notes.append("no eligible job")
        end_nap = time.time() + 120.0
        while time.time() < end_nap and not stop_requested():
            time.sleep(min(20.0, max(1.0, end_nap - time.time())))
            try:
                os.utime(order_path)
            except OSError:
                pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
