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
    "lanes": ["active_freight", "hub_upkeep", "internal_supply", "public_freight", "arbitrage", "liquidate_surplus"],
    "hub_upkeep_reorder_pct": 0.60,
    "hub_upkeep_targets": {
        "outpost": {"fuel_cell": 200, "steel_plate": 180, "circuit_board": 45, "hull_patch": 25},
        "station": {"fuel_cell": 1000, "steel_plate": 400, "circuit_board": 100, "flex_polymer": 150, "copper_wiring": 150, "hull_patch": 40, "repair_kit": 50},
    },
    "hub_bunker_fuel_targets": {"outpost": 50000, "station": 50000},
    "hub_bunker_reorder_pct": 0.96,
    "hub_upkeep_max_unit_price": {
        "fuel_cell": 115, "steel_plate": 120, "circuit_board": 900,
        "hull_patch": 350, "repair_kit": 400, "flex_polymer": 250, "copper_wiring": 250,
    },
    "arb_bid_depth_cap": 1.0,
    "min_arb_bid_qty": 1,
    "liquidate_min_revenue_cr": 300,
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


CORE_HAUL_LANES = ("active_freight", "internal_supply", "public_freight", "arbitrage", "liquidate_surplus")


def load_policy(policy_path=None):
    merged = json.loads(json.dumps(DEFAULT_POLICY))
    path = Path(policy_path) if policy_path else (ROOT / "haul-policy.json")
    if not path.is_absolute():
        path = REPO / path
    raw = read_json(path, {})
    if isinstance(raw, dict):
        merged.update(raw)
    is_main_policy = (policy_path is None) or (path.name == "haul-policy.json")
    if is_main_policy:
        merged["enabled"] = True
        lanes_cur = [str(x) for x in (merged.get("lanes") or []) if str(x)]
        for req_l in CORE_HAUL_LANES:
            if req_l not in lanes_cur:
                lanes_cur.append(req_l)
        merged["lanes"] = lanes_cur
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
    import worldcache as _wc
    return _wc.cached(("haul_base_map", str(data), _wc.db_sig(data)), 25.0, lambda: _load_base_map_uncached(data))


def _load_base_map_uncached(data):
    out = {}
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return out
    con = None
    try:
        import worldcache as _wc; con = _wc.ro_db(db, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if {"places", "systems"} <= tbls:
            for sys_id, poi_id, base_id, emp in con.execute("""
                SELECT p.system, p.poi, p.base, COALESCE(s.empire, '')
                FROM places p LEFT JOIN systems s ON s.id = p.system
                WHERE COALESCE(p.base, '') != ''
            """).fetchall():
                out[str(base_id)] = (str(sys_id), str(poi_id), str(base_id), str(emp or "").strip().lower())
        if {"bases", "systems"} <= tbls:
            for sys_id, poi_id, base_id, emp in con.execute("""
                SELECT b.system, COALESCE(b.poi, b.base), b.base, COALESCE(s.empire, '')
                FROM bases b LEFT JOIN systems s ON s.id = b.system
                WHERE COALESCE(b.base, '') != '' AND COALESCE(b.system, '') != ''
            """).fetchall():
                out.setdefault(str(base_id), (str(sys_id), str(poi_id), str(base_id), str(emp or "").strip().lower()))
    except sqlite3.Error:
        pass
    finally:
        if con is not None:
            con.close()
    return out


def load_cltv_outposts(data):
    """Auto-discover active CLTV Owned Outpost base_ids (0-rent Faction Lockboxes) from read.db."""
    import worldcache as _wc
    return set(_wc.cached(("haul_cltv_outposts", str(data), _wc.db_sig(data)), 60.0,
                          lambda: _load_cltv_outposts_uncached(data)))


def _load_cltv_outposts_uncached(data):
    out = set()
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return out
    con = None
    try:
        import worldcache as _wc
        con = _wc.ro_db(db, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "faction_facilities" in tbls:
            for (b_id,) in con.execute(
                "SELECT DISTINCT base FROM faction_facilities WHERE type = 'faction_lockbox' AND COALESCE(rent_per_cycle, 0) = 0 AND COALESCE(status, 'active') = 'active'"
            ).fetchall():
                if b_id:
                    out.add(str(b_id))
        if "bases" in tbls:
            for (b_id,) in con.execute("SELECT base FROM bases WHERE kind = 'outpost'").fetchall():
                if b_id:
                    out.add(str(b_id))
    except sqlite3.Error:
        pass
    finally:
        if con is not None:
            con.close()
    return out


def load_cltv_owned_hubs(data):
    """Auto-discover ALL CLTV Owned Outposts & Stations from read.db (bases + 0-rent facilities).
    Returns {base_id: {'base': base_id, 'system': sys_id, 'poi': poi_id, 'kind': 'outpost'|'station'}}."""
    import worldcache as _wc
    return dict(_wc.cached(("haul_cltv_owned_hubs", str(data), _wc.db_sig(data)), 60.0,
                           lambda: _load_cltv_owned_hubs_uncached(data)))


def _load_cltv_owned_hubs_uncached(data):
    out = {}
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return out
    con = None
    try:
        import worldcache as _wc
        con = _wc.ro_db(db, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "bases" in tbls:
            poi_by_base = {}
            if "places" in tbls:
                for p_b, p_p in con.execute("SELECT base, poi FROM places WHERE COALESCE(base,'')!='' AND COALESCE(poi,'')!=''").fetchall():
                    poi_by_base[str(p_b)] = str(p_p)
            for b_id, sys_id, poi_id, knd in con.execute(
                "SELECT base, system, COALESCE(poi, ''), COALESCE(kind, 'outpost') FROM bases WHERE base IS NOT NULL AND system IS NOT NULL"
            ).fetchall():
                poi_id = str(poi_id or "").strip() or poi_by_base.get(str(b_id), "")
                if b_id and sys_id:
                    k = "station" if "station" in str(knd or "").lower() else "outpost"
                    out[str(b_id)] = {"base": str(b_id), "system": str(sys_id), "poi": str(poi_id or b_id), "kind": k}
        if "faction_facilities" in tbls:
            for b_id, sys_id in con.execute(
                "SELECT DISTINCT base, system FROM faction_facilities WHERE type IN ('faction_lockbox', 'faction_fuel_bunker') AND COALESCE(rent_per_cycle, 0) = 0 AND COALESCE(status, 'active') = 'active'"
            ).fetchall():
                if b_id and sys_id and str(b_id) not in out:
                    out[str(b_id)] = {"base": str(b_id), "system": str(sys_id), "poi": str(b_id), "kind": "outpost"}
    except sqlite3.Error:
        pass
    finally:
        if con is not None:
            con.close()
    return out


def _hub_upkeep_keep_floor(policy, hub_kind, item_id):
    """Minimum upkeep reserve kept at an Owned Outpost/Station (prevents pull/push ping-pong!)."""
    tgts = (policy.get("hub_upkeep_targets") or {}).get(hub_kind) or {}
    return max(0, int(tgts.get(item_id) or 0))


def _pick_hub_upkeep(data, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed_keys, now_t=None, exclude_bases=None):
    """Reorder-point (s, S) automated upkeep resupply for ALL CLTV Owned Outposts & Stations.
    Prefers zero-cash internal transfers from empire Faction/pilot warehouses; falls back to cheap
    policed Exchange purchases when internal stock is absent (e.g. fuel_cell, hull_patch)."""
    if hold_cap < 1:
        return None
    now_t = time.time() if now_t is None else float(now_t)
    owned_hubs = load_cltv_owned_hubs(data)
    if not owned_hubs:
        return None
    reorder_pct = float(policy.get("hub_upkeep_reorder_pct") or 0.60)
    targets_cfg = policy.get("hub_upkeep_targets") or DEFAULT_POLICY["hub_upkeep_targets"]
    max_prices = policy.get("hub_upkeep_max_unit_price") or DEFAULT_POLICY["hub_upkeep_max_unit_price"]
    max_pick = int(policy.get("max_jumps_pickup") or 16)
    max_del = int(policy.get("max_jumps_delivery") or 35)
    max_age_s = float(policy.get("max_book_age_minutes") or 45) * 60.0
    max_spend = min(float(policy.get("max_buy_spend_cr") or 15000), max(0.0, float(avail_cash or 0)))
    sh_set = set(exclude_bases or ())

    can_fac = _pilot_can_withdraw_faction(data, pilot)
    stor = read_json(Path(data) / "stock" / "storage.json", {})
    fac_by_base = _load_faction_storage_by_base(data, stor)
    self_by_base = {}
    if isinstance(stor, dict):
        for b_id, items in _storage_stations((stor.get("pilots") or {}).get(pilot)).items():
            if isinstance(items, dict):
                self_by_base[b_id] = items

    asks_by_item = {}
    for row in books_rows or []:
        if not isinstance(row, dict):
            continue
        b_id = str(row.get("base") or "")
        iid = str(row.get("item") or "")
        ask_p = float(row.get("ask") or 0)
        ask_q = int(row.get("ask_qty") or 0)
        if not b_id or not iid or ask_p <= 0 or ask_q <= 0 or b_id in sh_set:
            continue
        ts = float(row.get("t") or 0)
        if ts and (now_t - ts) > max_age_s:
            continue
        oloc = base_map.get(b_id)
        if not oloc or not oloc[3] or oloc[0] in sh_set:
            continue
        asks_by_item.setdefault(iid, []).append((ask_p, ask_q, oloc))

    bunker_tgts = policy.get("hub_bunker_fuel_targets") or DEFAULT_POLICY["hub_bunker_fuel_targets"]
    emp_data = read_json(Path(data) / "empire" / "empire.json", {})
    bunker_fuel_by_base = {}
    has_bunker_bases = set()
    if isinstance(emp_data, dict):
        bunker_cap_by_base = {}
        _FUEL_FAC_CAPS = {
            "faction_fuel_bunker": 50000,
            "faction_large_fuel_bunker": 150000,
            "faction_capital_fuel_bunker": 500000,
            "refueling_dock": 5000,
            "fuel_depot": 5000,
            "fuel_tank_expansion": 50000,
            "fuel_bunker": 50000,
            "large_fuel_bunker": 150000,
            "capital_fuel_bunker": 500000,
        }
        for fac in (emp_data.get("facilities") or []):
            if isinstance(fac, dict) and str(fac.get("status") or "active") == "active":
                _ft = str(fac.get("type") or "").lower()
                if _ft in _FUEL_FAC_CAPS and fac.get("base"):
                    _fb = str(fac["base"])
                    has_bunker_bases.add(_fb)
                    bunker_cap_by_base[_fb] = bunker_cap_by_base.get(_fb, 0) + _FUEL_FAC_CAPS[_ft]
        for row in (emp_data.get("faction_storage") or []):
            if isinstance(row, dict) and str(row.get("item") or row.get("item_id") or "") == "fuel":
                b_k = str(row.get("base") or row.get("base_id") or "")
                if b_k:
                    bunker_fuel_by_base[b_k] = int(row.get("units") or row.get("quantity") or 0)

    best = None
    for hub_id, hinfo in owned_hubs.items():
        if hub_id in sh_set or hinfo["system"] in sh_set:
            continue
        dloc = base_map.get(hub_id) or (hinfo["system"], hinfo["poi"], hub_id, "")
        if not dloc or not str(dloc[1] or "").strip() or str(dloc[1]) == str(hub_id):
            continue
        hub_kind = hinfo.get("kind") or "outpost"
        tgts = targets_cfg.get(hub_kind) or {}
        cur_inv = fac_by_base.get(hub_id) or {}

        _kpi_upk_boost = 0.0
        _kpi_low_bunkers = set()
        try:
            import kpi_engine as _ke_l
            _lsig = _ke_l.read_kpi_signals(data_dir)
            if _lsig.get("boost_upkeep_urgency"):
                _kpi_upk_boost = 150.0
            _kpi_low_bunkers = set(str(x) for x in (_lsig.get("low_bunker_bases") or []))
        except Exception:
            pass
        # Build prioritized demand list: (item_id, deficit_units, urgency, job_key, bunker_fill_bool, eff_max_pick)
        demands = []
        _cap_here = int(bunker_cap_by_base.get(hub_id) or 0)
        btgt = min(int(bunker_tgts.get(hub_kind) or 0), _cap_here) if _cap_here > 0 else int(bunker_tgts.get(hub_kind) or 0)
        b_reorder = float(policy.get("hub_bunker_reorder_pct") or 0.98)
        if btgt > 0 and hub_id in has_bunker_bases:
            have_f = int(bunker_fuel_by_base.get(hub_id, cur_inv.get("fuel") or 0))
            fill_r = float(have_f) / float(btgt)
            if fill_r < b_reorder:
                # Dynamic multi-hauler surge scaling by fill level (Suggi directive):
                # <20% (<10k/50k): 5 haulers (CRITICAL, 16J) | 20-50% (<25k): 3 haulers (LOW, 12J)
                # 50-80% (<40k): 2 haulers (STEADY, 10J)     | 80-96% (<48k): 1 hauler (TOP-OFF, 8J nearby only!)
                if fill_r < 0.20:
                    _max_slots, urg_b, _b_pick = 5, 10.0, max_pick
                elif fill_r < 0.50:
                    _max_slots, urg_b, _b_pick = 3, 6.0, min(max_pick, 12)
                elif fill_r < 0.80:
                    _max_slots, urg_b, _b_pick = 2, 3.0, min(max_pick, 10)
                else:
                    _max_slots, urg_b, _b_pick = 1, 1.5, min(max_pick, 14)
                _free_jk = ""
                for _si in range(_max_slots):
                    _cand_jk = ("upkeep_bunker:%s" % hub_id) if _si == 0 else ("upkeep_bunker:%s:s%d" % (hub_id, _si))
                    if _cand_jk not in claimed_keys:
                        _free_jk = _cand_jk
                        break
                if _free_jk:
                    cells_need = max(1, (btgt - have_f + 19) // 20)
                    demands.append(("fuel_cell", cells_need, urg_b, _free_jk, True, _b_pick))

        for iid, tgt_raw in tgts.items():
            tgt = int(tgt_raw or 0)
            if tgt <= 0:
                continue
            have_here = int(cur_inv.get(iid) or 0)
            if have_here >= int(round(tgt * reorder_pct)):
                continue
            deficit = max(1, tgt - have_here)
            # Outpost wreck-repair readiness guard (UNCHANGED): full self-repair bill is 180 steel_plate + 45 circuit_board.
            _below_repair_bill = (
                hub_kind == "outpost"
                and ((iid == "steel_plate" and have_here < 180) or (iid == "circuit_board" and have_here < 45))
            )
            # Sovereign Station fast-track build/activation surge (sits behind Outpost CRITICAL/LOW <50% fuel 10.0/6.0,
            # strictly ahead of routine surplus hauls & TOP-OFF 1.2, with up to 3 parallel hauler slots per core item!).
            _station_core = (
                hub_kind == "station"
                and iid in ("steel_plate", "circuit_board", "fuel_cell", "flex_polymer")
            )
            _max_upk_slots = 3 if (_station_core and have_here < int(round(tgt * 0.50))) else 1
            jkey = ""
            for _usi in range(_max_upk_slots):
                _cjk = ("upkeep:%s:%s" % (hub_id, iid)) if _usi == 0 else ("upkeep:%s:%s:s%d" % (hub_id, iid, _usi))
                if _cjk not in claimed_keys:
                    jkey = _cjk
                    break
            if not jkey:
                continue
            if _below_repair_bill:
                urgency = 1.15
            elif _station_core:
                _base_u = 5.2 if iid == "fuel_cell" else 4.5
                urgency = _base_u * (1.0 - 0.5 * (float(have_here) / float(tgt)))
            elif hub_kind == "station":
                urgency = 1.6 * (1.0 - (float(have_here) / float(tgt)))
            else:
                urgency = (1.0 - (float(have_here) / float(tgt))) * (3.0 if iid == "fuel_cell" else 1.0)
            demands.append((iid, deficit, urgency, jkey, False, max_pick))

        for iid, deficit, urgency, jkey, bunker_fill, eff_max_pick in demands:
            # Keep steady fuel_cell trickles flowing (10+ cells) to top outpost bunkers continuously
            lot_floor = 10 if iid in ("fuel_cell", "circuit_board") else 20
            min_lot = min(deficit, int(hold_cap), lot_floor)
            # Local bunker conversion: if this outpost ALREADY holds >=15 fuel_cell in faction_storage AND pilot can withdraw,
            # convert directly into its fuel bunker at 0 jumps!
            if bunker_fill and can_fac and iid == "fuel_cell" and int(cur_inv.get("fuel_cell") or 0) >= 15:
                local_q = min(deficit, int(cur_inv.get("fuel_cell") or 0), int(hold_cap))
                p_hops_loc = _bfs_hops(lanes, cur_sys, dloc[0]) if cur_sys and lanes else 0
                if p_hops_loc is not None and p_hops_loc <= eff_max_pick and local_q >= 10:
                    sc_loc = (urgency * 240.0 + local_q * 2.0) / max(1.0, 1.0 + 0.5 * float(p_hops_loc))
                    cand_loc = (sc_loc, {
                        "job_key": jkey, "mode": "internal", "source_target": "faction",
                        "item": iid, "qty": local_q, "origin": dloc, "dest": dloc,
                        "hub_kind": hub_kind, "bunker_fill": True,
                        "pickup_hops": p_hops_loc, "delivery_hops": 0,
                    })
                    if best is None or cand_loc[0] > best[0]:
                        best = cand_loc
                    continue

            chosen = None
            _upk_srcs = (("faction", fac_by_base), ("self", self_by_base)) if can_fac else (("self", self_by_base),)
            for src_t, src_map in _upk_srcs:
                for sb_id, sitems in src_map.items():
                    if sb_id in owned_hubs or sb_id in sh_set or sb_id not in base_map:
                        continue
                    sq = int((sitems or {}).get(iid) or 0)
                    if sq < min_lot:
                        continue
                    oloc = base_map[sb_id]
                    if policy.get("policed_only", True) and not oloc[3]:
                        continue
                    p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
                    d_hops = _bfs_hops(lanes, oloc[0], dloc[0]) if lanes else 1
                    if p_hops is None or d_hops is None or p_hops > eff_max_pick or d_hops > max_del:
                        continue
                    qty = min(deficit, sq, int(hold_cap))
                    if qty < min_lot:
                        continue
                    sc = (urgency * 1000.0 + qty * 2.0) / max(1.0, float(p_hops + d_hops))
                    if chosen is None or sc > chosen[0]:
                        chosen = (sc, {
                            "job_key": jkey, "mode": "transfer", "source_target": src_t,
                            "item": iid, "qty": qty, "origin": oloc, "dest": dloc,
                            "hub_kind": hub_kind, "max_unit_price": 0,
                            "bunker_fill": bunker_fill,
                            "pickup_hops": p_hops, "delivery_hops": d_hops,
                        })

            if chosen is None and max_spend >= 200:
                cap_p = float(max_prices.get(iid) or 0)
                if cap_p > 0:
                    for ask_p, ask_q, oloc in sorted(asks_by_item.get(iid) or [], key=lambda x: x[0]):
                        if ask_p > cap_p:
                            break
                        p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
                        d_hops = _bfs_hops(lanes, oloc[0], dloc[0]) if lanes else 1
                        if p_hops is None or d_hops is None or p_hops > eff_max_pick or d_hops > max_del:
                            continue
                        qty = min(deficit, ask_q, int(hold_cap), int(max_spend // (ask_p * 1.02)))
                        if qty < min_lot:
                            continue
                        sc = (urgency * 850.0 + qty * 1.5) / max(1.0, float(p_hops + d_hops))
                        if chosen is None or sc > chosen[0]:
                            chosen = (sc, {
                                "job_key": jkey, "mode": "buy", "source_target": "market",
                                "item": iid, "qty": qty, "origin": oloc, "dest": dloc,
                                "hub_kind": hub_kind, "max_unit_price": int(round(cap_p)),
                                "est_ask": int(round(ask_p)),
                                "bunker_fill": bunker_fill,
                                "pickup_hops": p_hops, "delivery_hops": d_hops,
                            })
                        break

            if chosen and (best is None or chosen[0] > best[0]):
                best = chosen

    # Central Supply Depot restock (Node Beta Industrial Station: permanent Voidborn depot feeding all Outposts!)
    # Runs at urgency 0.95 (strictly behind Outpost fuel/repair emergencies, ahead of idle/surplus liquidation).
    depot_base = str(policy.get("central_depot_base") or "")
    depot_tgts = policy.get("central_depot_targets") or {}
    if depot_base and depot_tgts and depot_base in base_map and depot_base not in sh_set:
        dloc_dp = base_map[depot_base]
        if dloc_dp[0] not in sh_set:
            dp_inv = fac_by_base.get(depot_base) or {}
            for iid, tgt_raw in depot_tgts.items():
                tgt = int(tgt_raw or 0)
                if tgt <= 0:
                    continue
                have_dp = int(dp_inv.get(iid) or 0)
                if have_dp >= int(round(tgt * reorder_pct)):
                    continue
                jk_dp = "depot:%s:%s" % (depot_base, iid)
                if jk_dp in claimed_keys:
                    continue
                deficit = max(1, tgt - have_dp)
                lot_floor = 10 if iid in ("fuel_cell", "circuit_board", "hull_patch") else 20
                min_lot = min(deficit, int(hold_cap), lot_floor)
                urg_dp = max(0.35, (1.0 - (float(have_dp) / float(tgt))) * 0.95)
                # Priority 1: 0-jump personal->faction flush at Node Beta (unlocks hauler-6's 3,108 circuit_boards & 20,945 steel_plates!)
                self_at_dp = int((self_by_base.get(depot_base) or {}).get(iid) or 0)
                if self_at_dp >= min_lot:
                    p_hops_dp = _bfs_hops(lanes, cur_sys, dloc_dp[0]) if cur_sys and lanes else 0
                    if p_hops_dp is not None and p_hops_dp <= max_pick:
                        fq = min(deficit, self_at_dp, int(hold_cap))
                        sc_f = (urg_dp * 950.0 + fq * 2.0) / max(1.0, 1.0 + 0.5 * float(p_hops_dp))
                        cand_f = (sc_f, {
                            "job_key": jk_dp, "mode": "transfer", "source_target": "self",
                            "item": iid, "qty": fq, "origin": dloc_dp, "dest": dloc_dp,
                            "hub_kind": "depot", "max_unit_price": 0, "bunker_fill": False,
                            "pickup_hops": p_hops_dp, "delivery_hops": 0,
                        })
                        if best is None or cand_f[0] > best[0]:
                            best = cand_f
                        continue
                # Priority 2: transfer from other Empire Lockboxes or personal storage (NEVER steal from owned Outposts or Node Beta itself!)
                chosen_dp = None
                _dp_srcs = (("faction", fac_by_base), ("self", self_by_base)) if can_fac else (("self", self_by_base),)
                for src_t, src_map in _dp_srcs:
                    for sb_id, sitems in src_map.items():
                        if sb_id == depot_base or sb_id in owned_hubs or sb_id in sh_set or sb_id not in base_map:
                            continue
                        sq = int((sitems or {}).get(iid) or 0)
                        if sq < min_lot:
                            continue
                        oloc = base_map[sb_id]
                        if policy.get("policed_only", True) and not oloc[3]:
                            continue
                        p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
                        d_hops = _bfs_hops(lanes, oloc[0], dloc_dp[0]) if lanes else 1
                        if p_hops is None or d_hops is None or p_hops > max_pick or d_hops > max_del:
                            continue
                        qty = min(deficit, sq, int(hold_cap))
                        if qty < min_lot:
                            continue
                        sc = (urg_dp * 900.0 + qty * 1.5) / max(1.0, float(p_hops + d_hops))
                        if chosen_dp is None or sc > chosen_dp[0]:
                            chosen_dp = (sc, {
                                "job_key": jk_dp, "mode": "transfer", "source_target": src_t,
                                "item": iid, "qty": qty, "origin": oloc, "dest": dloc_dp,
                                "hub_kind": "depot", "max_unit_price": 0, "bunker_fill": False,
                                "pickup_hops": p_hops, "delivery_hops": d_hops,
                            })
                # Priority 3: cheap policed NPC market buy fallback (e.g. 100 cr fuel_cells!)
                if chosen_dp is None and max_spend >= 200:
                    cap_p = float(max_prices.get(iid) or 0)
                    if cap_p > 0:
                        for ask_p, ask_q, oloc in sorted(asks_by_item.get(iid) or [], key=lambda x: x[0]):
                            if ask_p > cap_p:
                                break
                            p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
                            d_hops = _bfs_hops(lanes, oloc[0], dloc_dp[0]) if lanes else 1
                            if p_hops is None or d_hops is None or p_hops > max_pick or d_hops > max_del:
                                continue
                            qty = min(deficit, ask_q, int(hold_cap), int(max_spend // (ask_p * 1.02)))
                            if qty < min_lot:
                                continue
                            sc = (urg_dp * 750.0 + qty * 1.2) / max(1.0, float(p_hops + d_hops))
                            if chosen_dp is None or sc > chosen_dp[0]:
                                chosen_dp = (sc, {
                                    "job_key": jk_dp, "mode": "buy", "source_target": "market",
                                    "item": iid, "qty": qty, "origin": oloc, "dest": dloc_dp,
                                    "hub_kind": "depot", "max_unit_price": int(round(cap_p)),
                                    "est_ask": int(round(ask_p)), "bunker_fill": False,
                                    "pickup_hops": p_hops, "delivery_hops": d_hops,
                                })
                            break
                if chosen_dp and (best is None or chosen_dp[0] > best[0]):
                    best = chosen_dp
    return best[1] if best else None


def load_stronghold_bases(data):
    import worldcache as _wc
    return _wc.cached(("haul_strongholds", str(data), _wc.db_sig(data)), 25.0, lambda: _load_stronghold_bases_uncached(data))


def _load_stronghold_bases_uncached(data):
    out = set()
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return out
    con = None
    try:
        import worldcache as _wc; con = _wc.ro_db(db, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if {"places", "stations"} <= tbls:
            for base_id, sys_id in con.execute(
                "SELECT p.base, p.system FROM places p JOIN stations s ON LOWER(s.system)=LOWER(p.system) "
                "WHERE COALESCE(p.base,'')!='' AND (LOWER(COALESCE(s.kind,'')) LIKE '%stronghold%' OR LOWER(COALESCE(s.name,'')) LIKE '%stronghold%')"
            ).fetchall():
                out.add(str(base_id))
                out.add(str(sys_id))
        if "public_battles" in tbls:
            pb_cut = time.time() - 7200.0
            for (pb_sys,) in con.execute("SELECT DISTINCT system FROM public_battles WHERE category = 'pirate' AND t >= ?", (pb_cut,)).fetchall():
                if pb_sys:
                    out.add(str(pb_sys).strip())
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


def assign_optimal_arbitrage(books_rows, base_map, lanes, peers, policy, claimed_keys, now_t=None, exclude_bases=None, fair_prices=None, cltv_buy_keys=None):
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
    bid_cap_ratio = max(0.2, min(1.0, float(policy.get("arb_bid_depth_cap") or 1.0)))
    min_bid_qty = max(1, int(policy.get("min_arb_bid_qty") or 1))

    allow_bw = bool(policy.get("allow_calm_buywall_dest", False))
    bw_min_bid = float(policy.get("buywall_min_bid") or 50.0)
    bw_min_qty = int(policy.get("buywall_min_qty") or 200)
    by_item = {}
    for r in books_rows or []:
        b_id = str(r.get("base") or "")
        loc = base_map.get(b_id)
        if not loc:
            continue
        if exclude_bases and (b_id in exclude_bases or loc[0] in exclude_bases):
            continue
        t = float(r.get("t") or 0)
        if t > 0 and (now_t - t) > max_age_s:
            continue
        iid = str(r.get("item") or "")
        if not iid or iid in PROTECTED_ITEMS:
            continue
        ask_p, ask_q = float(r.get("ask") or 0), int(r.get("ask_qty") or 0)
        bid_p, bid_q = float(r.get("bid") or 0), int(r.get("bid_qty") or 0)
        is_pol = bool(loc[3])
        is_bw_bid = (allow_bw and bid_p >= bw_min_bid and bid_q >= bw_min_qty)
        if policed and not is_pol and not is_bw_bid:
            continue
        # Only buy from policed stations when policed_only is True; calm buy-wall hubs are sell destinations only!
        eff_ask_p = ask_p if (not policed or is_pol) else 0.0
        eff_ask_q = ask_q if (not policed or is_pol) else 0
        eff_bid_p = bid_p if (not policed or is_pol or is_bw_bid) else 0.0
        eff_bid_q = bid_q if (not policed or is_pol or is_bw_bid) else 0
        if eff_ask_q <= 0 and eff_bid_q <= 0:
            continue
        by_item.setdefault(iid, []).append((b_id, loc, eff_ask_p, eff_ask_q, eff_bid_p, eff_bid_q))

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
        _fp_i = (fair_prices or {}).get(iid)
        for ab, aloc, ask_p, ask_q, _, _ in asks:
            unit_cost = ask_p * 1.05
            for bb, bloc, _, _, bid_p, bid_q in bids:
                if ab == bb or bid_q < min_bid_qty or bid_p < ask_p * (1.0 + min_margin) or bid_p <= unit_cost:
                    continue
                if isinstance(cltv_buy_keys, dict):
                    _cq = int(cltv_buy_keys.get((bb, iid), 0))
                    _net_bq = max(0, int(bid_q) - _cq)
                    if _net_bq < min_bid_qty or (_cq > 0 and _net_bq < 200):
                        continue
                    bid_q = _net_bq
                elif cltv_buy_keys and (bb, iid) in cltv_buy_keys:
                    continue
                if _fp_i is not None:
                    import market_guard as _mg_a
                    if _mg_a.is_mirage_arbitrage_trap(iid, ask_p, bid_p, _fp_i):
                        continue
                # Deep buy-walls (>=500 qty) allow parallel origin asks without single-hauler lock
                jkey = ("arb-bw:%s:%s:%s" % (ab, bb, iid)) if (bid_q >= 500 and bid_p >= bw_min_bid) else ("arb-bid:%s:%s" % (bb, iid))
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
            eff_bid_q = max(1, int(bid_q * bid_cap_ratio))
            qty = min(p_cap, int(ask_q), eff_bid_q, int(p_spend // unit_cost))
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


def pick_arbitrage_job(books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed_keys, now_t=None, exclude_bases=None, fair_prices=None, cltv_buy_keys=None):
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
    bid_cap_ratio = max(0.2, min(1.0, float(policy.get("arb_bid_depth_cap") or 1.0)))
    min_bid_qty = max(1, int(policy.get("min_arb_bid_qty") or 1))
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
        _fp_i = (fair_prices or {}).get(iid)
        for ab, aloc, ask_p, ask_q, _, _ in asks:
            for bb, bloc, _, _, bid_p, bid_q in bids:
                if ab == bb or bid_q < min_bid_qty or bid_p < ask_p * (1.0 + min_margin):
                    continue
                if isinstance(cltv_buy_keys, dict):
                    _cq = int(cltv_buy_keys.get((bb, iid), 0))
                    _net_bq = max(0, int(bid_q) - _cq)
                    if _net_bq < min_bid_qty or (_cq > 0 and _net_bq < 200):
                        continue
                    bid_q = _net_bq
                elif cltv_buy_keys and (bb, iid) in cltv_buy_keys:
                    continue
                if _fp_i is not None:
                    import market_guard as _mg_a
                    if _mg_a.is_mirage_arbitrage_trap(iid, ask_p, bid_p, _fp_i):
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
                eff_bid_q = max(1, int(bid_q * bid_cap_ratio))
                qty = min(int(hold_cap), int(ask_q), eff_bid_q, int(max_spend // unit_cost))
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
    import worldcache as _wc
    return _wc.cached(("haul_books", str(data), _wc.db_sig(data)), 25.0, lambda: _load_books_uncached(data))


def _load_books_uncached(data):
    db = Path(data) / "store" / "read.db"
    if not db.is_file():
        return []
    con = None
    try:
        import worldcache as _wc; con = _wc.ro_db(db, timeout=3.0)
        con.row_factory = sqlite3.Row
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "books" not in tbls:
            return []
        bcols = {r[1] for r in con.execute("PRAGMA table_info(books)").fetchall()}
        bd_col = "COALESCE(bid_depth, bid_qty, 0) AS bid_depth" if "bid_depth" in bcols else "COALESCE(bid_qty, 0) AS bid_depth"
        return [dict(r) for r in con.execute("SELECT base, item, ask, ask_qty, bid, bid_qty, %s, t FROM books WHERE (ask > 0 AND ask_qty > 0) OR (bid > 0 AND bid_qty > 0)" % bd_col).fetchall()]
    except sqlite3.Error:
        return []
    finally:
        if con is not None:
            con.close()


def _storage_stations(entry):
    """Unwrap storage.json pilot/Faction record: handles live {"stations": {base: {item: qty}}} AND flat {base: {item: qty}}."""
    if not isinstance(entry, dict):
        return {}
    st = entry.get("stations")
    if isinstance(st, dict):
        return st
    return {k: v for k, v in entry.items() if isinstance(v, dict)}



def _pilot_can_withdraw_faction(data, pilot):
    """True only if pilot holds Leader/Officer (manage_treasury) in empire.json so Member haulers never burn fuel on permission-denied withdraws."""
    emp = read_json(Path(data) / "empire" / "empire.json", {})
    if not isinstance(emp, dict):
        return False
    allowed_roles = {"leader", "officer"}
    for r in (emp.get("roles") or []):
        if isinstance(r, dict) and (r.get("permissions") or {}).get("manage_treasury"):
            for k in ("id", "name"):
                if r.get(k):
                    allowed_roles.add(str(r[k]).strip().lower())
    for m in (emp.get("members") or []):
        if not isinstance(m, dict):
            continue
        nm = str(m.get("pilot") or m.get("name") or m.get("member") or m.get("username") or "").strip()
        if nm == str(pilot):
            rl = str(m.get("role") or m.get("rank") or "").strip().lower()
            return rl in allowed_roles
    return False


def _load_faction_storage_by_base(data, stor=None):
    """Merge live empire.json faction_storage with stock/storage.json Faction rows so Haulers always see 100% of current Lockbox stock."""
    out = {}
    if isinstance(stor, dict):
        for f_raw in (stor.get("faction"), (stor.get("pilots") or {}).get("Faction")):
            for b_id, items in _storage_stations(f_raw).items():
                if isinstance(items, dict):
                    dst = out.setdefault(str(b_id), {})
                    for k, v in items.items():
                        dst[str(k)] = max(int(dst.get(str(k)) or 0), int(v or 0))
    emp = read_json(Path(data) / "empire" / "empire.json", {})
    if isinstance(emp, dict):
        for row in (emp.get("faction_storage") or []):
            if not isinstance(row, dict):
                continue
            b_id = str(row.get("base") or row.get("base_id") or "")
            iid = str(row.get("item") or row.get("item_id") or "")
            qty = int(row.get("units") or row.get("quantity") or 0)
            if b_id and iid and qty > 0 and iid != "fuel":
                dst = out.setdefault(b_id, {})
                dst[iid] = max(int(dst.get(iid) or 0), qty)
    return out


def _load_cltv_open_buy_qty(data, now_t=None, ttl_s=21600):
    try:
        import market_guard as _mg_hq
        return _mg_hq.load_cltv_buy_qty(data, now_t=now_t, ttl_s=ttl_s)
    except Exception:
        return {}


def _load_cltv_open_buy_keys(data, now_t=None, ttl_s=21600):
    """Return set of (base_id, item_id) where our own CLTV Bursars currently hold open buy orders (anti-wash-trade guard!)."""
    now_t = time.time() if now_t is None else float(now_t)
    out = set()
    doc = read_json(Path(data) / "fleet" / "bursar_buys.json", {})
    entries = doc.get("entries") if isinstance(doc, dict) and isinstance(doc.get("entries"), dict) else {}
    for _p, bases in entries.items():
        if not isinstance(bases, dict):
            continue
        for b_id, rec in bases.items():
            if not isinstance(rec, dict) or (now_t - float(rec.get("at") or 0)) > ttl_s:
                continue
            for iid, q in (rec.get("items") or {}).items():
                if iid and int(q or 0) > 0:
                    out.add((str(b_id), str(iid)))
    return out


def _load_reserved_items_exact(data):
    """Return hard-reserved item IDs: PROTECTED_ITEMS + keep=all + open needs where fleet stock <= 1.25x need + 50."""
    reserved = set(PROTECTED_ITEMS) | {"fuel", "station_core"}
    open_needs = {}
    fleet_stock = {}
    db = Path(data) / "store" / "read.db"
    if db.is_file():
        con = None
        try:
            import worldcache as _wc
            con = _wc.ro_db(db, timeout=3.0)
            tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
            if "holdings" in tbls:
                for iid, u in con.execute("SELECT item, SUM(units) FROM holdings GROUP BY item").fetchall():
                    if iid and u:
                        fleet_stock[str(iid)] = fleet_stock.get(str(iid), 0) + int(u)
            if "faction_storage" in tbls:
                for iid, u in con.execute("SELECT item, SUM(units) FROM faction_storage GROUP BY item").fetchall():
                    if iid and u:
                        fleet_stock[str(iid)] = fleet_stock.get(str(iid), 0) + int(u)
            if "contract_candidates" in tbls:
                for (short_s,) in con.execute("SELECT short_items FROM contract_candidates WHERE short_items IS NOT NULL").fetchall():
                    for part in str(short_s).split(","):
                        m = re.match(r"\s*([a-z0-9_]+)\s+([\d,]+)", part.strip())
                        if m:
                            iid, qty = m.group(1), int(m.group(2).replace(",", ""))
                            if qty > 0:
                                open_needs[iid] = open_needs.get(iid, 0) + qty
            if "supply_status" in tbls:
                for iid, stk, keep in con.execute("SELECT item, stock, keep FROM supply_status").fetchall():
                    if iid and int(keep or 0) > 0 and int(stk or 0) < int(keep or 0):
                        open_needs[str(iid)] = max(open_needs.get(str(iid), 0), int(keep) - int(stk or 0))
            for iid, nq in open_needs.items():
                if fleet_stock.get(iid, 0) <= int(nq * 1.25) + 50:
                    reserved.add(iid)
        except sqlite3.Error:
            pass
        finally:
            if con is not None:
                con.close()
    res_tsv = REPO / "game" / "reserve.tsv"
    if res_tsv.is_file():
        try:
            for ln in res_tsv.read_text(encoding="ascii", errors="replace").splitlines():
                ln = ln.strip()
                if not ln or ln.startswith("#") or ln.lower().startswith("kind\t"):
                    continue
                cols = ln.split("\t")
                if len(cols) >= 3:
                    rk, ri, ru = cols[0].strip().lower(), cols[1].strip(), cols[2].strip().lower()
                    if rk == "keep" and ri:
                        if ru == "all":
                            reserved.add(ri)
                        else:
                            try:
                                if fleet_stock.get(ri, 0) <= int(float(ru) * 1.25):
                                    reserved.add(ri)
                            except ValueError:
                                reserved.add(ri)
        except OSError:
            pass
    return reserved

def _pick_consolidate_to_trader(data, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, policy, claimed_keys, now_t=None, exclude_bases=None):
    """Pull non-reserved surplus from lawless Owned Outposts & non-Bursar hubs to the nearest policed Trade Hub with a docked Bursar Trader."""
    if hold_cap < 1:
        return None
    now_t = time.time() if now_t is None else float(now_t)
    can_fac = _pilot_can_withdraw_faction(data, pilot)
    max_pick = int(policy.get("max_jumps_pickup") or 16)
    max_del = int(policy.get("max_jumps_delivery") or 35)
    min_u = int(policy.get("consolidate_min_units") or 10)
    min_val = float(policy.get("consolidate_min_value_cr") or 250)
    sh_set = set(exclude_bases or ())
    reserved = _load_reserved_items_exact(data)

    claims = read_json(Path(data) / "fleet" / "bursar_claims.json", {})
    bursar_hubs = []
    for b_id, rec in (claims.items() if isinstance(claims, dict) else []):
        if not isinstance(rec, dict) or (now_t - float(rec.get("claimed_at") or 0)) > 7200.0:
            continue
        loc = base_map.get(str(b_id))
        if loc and loc[3] and str(b_id) not in sh_set and loc[0] not in sh_set:
            bursar_hubs.append((str(b_id), loc, str(rec.get("pilot") or "")))
    if not bursar_hubs:
        return None

    # Require a LIVE LOCAL REAL EXTERNAL BID at the EXACT destination Bursar hub (exclude our own CLTV buy orders!)
    cltv_buys = _load_cltv_open_buy_keys(data, now_t=now_t)
    local_bids = {}
    for r in books_rows or []:
        b_s = str(r.get("base") or "")
        iid = str(r.get("item") or "")
        if not b_s or not iid or (b_s, iid) in cltv_buys:
            continue
        bp = float(r.get("bid") or 0)
        bq = int(r.get("bid_qty") or 0)
        if bp >= 5.0 and bq >= 5:
            prev = local_bids.get((b_s, iid))
            if prev is None or bp > prev[0]:
                local_bids[(b_s, iid)] = (bp, bq)

    stor = read_json(Path(data) / "stock" / "storage.json", {})
    owned_hubs = load_cltv_owned_hubs(data)
    bursar_base_set = {b for b, _, _ in bursar_hubs}
    sources = []
    if isinstance(stor, dict):
        for b_id, items in _storage_stations((stor.get("pilots") or {}).get(pilot)).items():
            if isinstance(items, dict) and str(b_id) not in bursar_base_set:
                sources.append(("self", str(b_id), items))
    if can_fac:
        for b_id, items in _load_faction_storage_by_base(data, stor).items():
            if b_id in owned_hubs or b_id not in bursar_base_set:
                sources.append(("faction", b_id, items))

    best = None
    for src_t, b_id, items in sources:
        if b_id not in base_map or b_id in sh_set:
            continue
        oloc = base_map[b_id]
        if oloc[0] in sh_set:
            continue
        p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
        if p_hops is None or p_hops > max_pick:
            continue
        reach_dsts = []
        for db, dloc, bp in bursar_hubs:
            if db == b_id:
                continue
            dh = _bfs_hops(lanes, oloc[0], dloc[0]) if lanes else 1
            if dh is not None and dh <= max_del:
                reach_dsts.append((dh, db, dloc, bp))
        if not reach_dsts:
            continue
        for iid, qty in items.items():
            q = int(qty or 0)
            if b_id in owned_hubs:
                q -= _hub_upkeep_keep_floor(policy, owned_hubs[b_id].get("kind") or "outpost", iid)
            if b_id == str(policy.get("central_depot_base") or ""):
                q -= int((policy.get("central_depot_targets") or {}).get(iid) or 0)
            if q < min_u or iid in reserved:
                continue
            is_owned_outpost = (b_id in owned_hubs and str(owned_hubs[b_id].get("kind") or "") == "outpost")
            fair_u = 0.0
            if is_owned_outpost:
                _oracle_items = (read_json(Path(data) / "fleet" / "price_oracle.json", {}) or {}).get("items") or {}
                fair_u = float((_oracle_items.get(iid) or {}).get("fair_price") or 0.0)
            for d_hops, db, dloc, b_pilot in reach_dsts:
                lb = local_bids.get((db, iid))
                if lb:
                    uval, lb_q = lb
                    take_q = min(q, int(hold_cap), int(lb_q))
                    max_slots = min(6, max(1, min(q, int(lb_q)) // max(1, int(hold_cap))))
                    val_weight = 1.0
                elif is_owned_outpost and fair_u >= 8.0 and d_hops <= 12:
                    # Outposts have no Market Terminal: move high-value non-reserved ore/gas to nearest Bursar hub for sell-order listing!
                    uval = fair_u
                    take_q = min(q, int(hold_cap))
                    max_slots = min(4, max(1, q // max(1, int(hold_cap))))
                    val_weight = 0.70
                else:
                    continue
                if take_q < 1:
                    continue
                est_val = take_q * uval * val_weight
                if est_val < min_val:
                    continue
                jkey = None
                for si in range(max_slots):
                    ck = ("cons:%s:%s:%s:%s" % (src_t, b_id, db, iid)) if si == 0 else ("cons:%s:%s:%s:%s#%d" % (src_t, b_id, db, iid, si))
                    if ck not in claimed_keys:
                        jkey = ck
                        break
                if not jkey:
                    continue
                tot_h = max(1, p_hops + d_hops)
                sc = est_val / float(tot_h)
                if best is None or sc > best[0]:
                    best = (sc, {
                        "job_key": jkey, "item": iid, "qty": take_q, "source_target": src_t,
                        "origin": oloc, "dest": dloc, "bursar_pilot": b_pilot,
                        "est_val": int(round(est_val)), "pickup_hops": p_hops, "delivery_hops": d_hops,
                    })
    return best[1] if best else None

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
        import worldcache as _wc; con = _wc.ro_db(db, timeout=3.0)
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
    owned_outposts = load_cltv_outposts(data)
    owned_hubs = load_cltv_owned_hubs(data)
    sources = []
    if isinstance(stor, dict):
        for b_id, items in _storage_stations((stor.get("pilots") or {}).get(pilot)).items():
            if isinstance(items, dict):
                sources.append(("self", b_id, items))
        for f_raw in (stor.get("faction"), (stor.get("pilots") or {}).get("Faction")):
            for b_id, items in _storage_stations(f_raw).items():
                if isinstance(items, dict):
                    sources.append(("faction", b_id, items))
    if not sources:
        return None
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 25)
    best = None
    for src_target, b_id, items in sources:
        if b_id in home_bases or b_id not in base_map:
            continue
        oloc = base_map[b_id]
        # Allow pickups from our own CLTV Owned Outpost Lockboxes (0-rent regional consolidation hubs!)
        if policy.get("policed_only", True) and not oloc[3] and b_id not in owned_outposts:
            continue
        for iid, qty in items.items():
            q = int(qty or 0)
            if b_id in owned_hubs:
                q -= _hub_upkeep_keep_floor(policy, owned_hubs[b_id].get("kind") or "outpost", iid)
            if q < 10 or iid not in open_needs:
                continue
            max_slots = min(4, max(1, q // max(1, int(hold_cap))))
            jkey = None
            for slot_i in range(max_slots):
                cand_k = ("supply:%s:%s:%s" % (src_target, b_id, iid)) if slot_i == 0 else ("supply:%s:%s:%s#%d" % (src_target, b_id, iid, slot_i))
                if cand_k not in claimed_keys:
                    jkey = cand_k
                    break
            if not jkey:
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
                best = (score, {"job_key": jkey, "item": iid, "qty": take_q, "source_target": src_target, "origin": oloc, "dest": dloc})
    return best[1] if best else None



def _pick_surplus_liquidation(data, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, policy, claimed_keys, now_t=None, exclude_bases=None):
    """Carry pilot's own non-reserved stored items to the best reachable policed live bid to convert surplus to cash."""
    if hold_cap < 1:
        return None
    now_t = time.time() if now_t is None else float(now_t)
    policed = bool(policy.get("policed_only", True))
    max_pick = int(policy.get("max_jumps_pickup") or 16)
    max_del = int(policy.get("max_jumps_delivery") or 30)
    max_age_s = float(policy.get("max_book_age_minutes") or 30) * 60.0
    min_rev = float(policy.get("liquidate_min_revenue_cr") or 300)

    reserved = _load_reserved_items_exact(data)

    stor = read_json(Path(data) / "stock" / "storage.json", {})
    sources = []
    if isinstance(stor, dict):
        for b_id, items in _storage_stations((stor.get("pilots") or {}).get(pilot)).items():
            if isinstance(items, dict):
                sources.append(("self", b_id, items))
        if policy.get("allow_faction_surplus_liquidation", True) and _pilot_can_withdraw_faction(data, pilot):
            for b_id, items in _load_faction_storage_by_base(data, stor).items():
                sources.append(("faction", b_id, items))
    if not sources:
        return None

    allow_bw = bool(policy.get("allow_calm_buywall_dest", True))
    bw_min_bid = float(policy.get("buywall_min_bid") or 50.0)
    bw_min_qty = int(policy.get("buywall_min_qty") or 200)
    cltv_buy_qty = _load_cltv_open_buy_qty(data, now_t=now_t)
    # Anti-lowball reference: never liquidate high-value items (>= 20 cr fair) into a < 70% scam bid!
    fair_by_item = {}
    try:
        import market_guard as _mg_l
        _vwm_l = _mg_l.compute_book_vwm_map(books_rows, cltv_buy_qty=cltv_buy_qty, now_t=now_t)
        for _k, _v in _vwm_l.items():
            fair_by_item[_k] = float(_v.get("vwm") or 0.0)
    except Exception:
        pass
    bids_by_item = {}
    for r in books_rows or []:
        b_id = str(r.get("base") or "")
        loc = base_map.get(b_id)
        if not loc:
            continue
        if exclude_bases and (b_id in exclude_bases or loc[0] in exclude_bases):
            continue
        t = float(r.get("t") or 0)
        if t > 0 and (now_t - t) > max_age_s:
            continue
        bp = float(r.get("bid") or 0)
        bq = int(r.get("bid_qty") or 0)
        iid = str(r.get("item") or "")
        # Strictly load REAL EXTERNAL top-of-book bid_qty (subtract CLTV own qty; never blind deep rival buy-walls!)
        _cq_l = int(cltv_buy_qty.get((b_id, iid), 0))
        _net_bq_l = max(0, bq - _cq_l)
        if not (iid and bp >= 1.0 and _net_bq_l >= 1) or (_cq_l > 0 and _net_bq_l < 200):
            continue
        bq = _net_bq_l
        _fv_l = float(fair_by_item.get(iid) or 0.0)
        if _fv_l >= 20.0 and bp < _fv_l * 0.70:
            continue
        if policed and not loc[3]:
            if not (allow_bw and bp >= bw_min_bid and bq >= bw_min_qty):
                continue
        bids_by_item.setdefault(iid, []).append((b_id, loc, bp, bq))

    owned_outposts = load_cltv_outposts(data)
    owned_hubs = load_cltv_owned_hubs(data)
    best = None
    for src_target, b_id, items in sources:
        if b_id not in base_map:
            continue
        oloc = base_map[b_id]
        if policed and not oloc[3] and b_id not in owned_outposts:
            continue
        p_hops = _bfs_hops(lanes, cur_sys, oloc[0]) if cur_sys and lanes else 0
        if p_hops is None or p_hops > max_pick:
            continue
        for iid, qty in items.items():
            q = int(qty or 0)
            if b_id in owned_hubs:
                q -= _hub_upkeep_keep_floor(policy, owned_hubs[b_id].get("kind") or "outpost", iid)
            if b_id == str(policy.get("central_depot_base") or ""):
                q -= int((policy.get("central_depot_targets") or {}).get(iid) or 0)
            if q < 1 or iid in reserved or iid not in bids_by_item:
                continue
            for sb, sloc, bid_p, bid_q in bids_by_item[iid]:
                d_hops = _bfs_hops(lanes, oloc[0], sloc[0]) if lanes else (0 if oloc[0] == sloc[0] else 1)
                if d_hops is None or d_hops > max_del:
                    continue
                take_q = min(q, int(hold_cap), int(bid_q))
                if take_q < 1:
                    continue
                tot_hops = max(1, p_hops + d_hops)
                est_rev = take_q * bid_p - tot_hops * 45.0
                # Allow clearing huge excess gluts (>=500 units) into live 1-4 cr buy-walls whenever net revenue >= 250 cr!
                eff_min_rev = 250.0 if (q >= 500 and bid_p >= 1.0) else min_rev
                if bid_p < 5.0 and q < 500:
                    continue
                if est_rev < eff_min_rev:
                    continue
                max_slots = min(int(policy.get('liquidate_max_slots') or 8), max(1, min(q, int(bid_q)) // max(1, int(hold_cap))))
                jkey = None
                for slot_i in range(max_slots):
                    cand_k = ("liq:%s:%s:%s:%s" % (src_target, b_id, sb, iid)) if slot_i == 0 else ("liq:%s:%s:%s:%s#%d" % (src_target, b_id, sb, iid, slot_i))
                    if cand_k not in claimed_keys:
                        jkey = cand_k
                        break
                if not jkey:
                    continue
                score = est_rev / float(tot_hops)
                if best is None or score > best[0]:
                    best = (score, {
                        "job_key": jkey, "item": iid, "qty": take_q,
                        "source_target": src_target,
                        "origin": oloc, "dest": sloc, "est_bid": int(round(bid_p)),
                        "est_rev": int(round(est_rev)),
                    })
    return best[1] if best else None

def _pick_backhaul_delivery(data, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed_keys, now_t=None, exclude_bases=None):
    """Zero-idle Corporate Backhaul: find profitable single-item `deliver_item` supply contracts from data/missions/*.json.

    Safe by construction: only selects contracts where we can buy the exact item BEFORE accepting the contract,
    target_base is safe (not stronghold/pirate), and net credit reward beats ask cost + jump fuel by >= min_total_profit!
    """
    if hold_cap < 1 or avail_cash < 500:
        return None
    now_t = time.time() if now_t is None else float(now_t)
    mdir = Path(data) / "missions"
    if not mdir.is_dir():
        return None
    policed = bool(policy.get("policed_only", True))
    allow_bw = bool(policy.get("allow_calm_buywall_dest", True))
    max_pick = int(policy.get("max_jumps_pickup") or 12)
    max_del = int(policy.get("max_jumps_delivery") or 20)
    min_prof = float(policy.get("backhaul_min_profit_cr") or policy.get("min_total_profit") or 400)
    min_margin = float(policy.get("backhaul_min_margin_pct") or 0.20)
    max_spend = min(float(policy.get("max_buy_spend_cr") or 15000), float(avail_cash))
    max_age_s = float(policy.get("max_book_age_minutes") or 45) * 60.0

    asks_by_item = {}
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
        ap = float(r.get("ask") or 0)
        aq = int(r.get("ask_qty") or 0)
        iid = str(r.get("item") or "")
        if iid and ap > 0 and aq > 0 and iid not in PROTECTED_ITEMS:
            asks_by_item.setdefault(iid, []).append((b_id, loc, ap, aq))

    if not asks_by_item:
        return None

    best = None
    for mp in mdir.glob("*.json"):
        try:
            if (now_t - mp.stat().st_mtime) > 7200.0:
                continue
            doc = json.loads(mp.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        m_base = str(doc.get("base") or mp.stem)
        if m_base not in base_map:
            continue
        mloc = base_map[m_base]
        if exclude_bases and (m_base in exclude_bases or mloc[0] in exclude_bases):
            continue
        if policed and not mloc[3] and not allow_bw:
            continue
        for m in doc.get("missions") or []:
            if not isinstance(m, dict) or str(m.get("type") or "") != "delivery":
                continue
            obs = [o for o in (m.get("objectives") or []) if isinstance(o, dict)]
            if len(obs) != 1 or str(obs[0].get("type") or "") != "deliver_item":
                continue
            ob = obs[0]
            iid = str(ob.get("item_id") or "")
            qty = int(ob.get("quantity") or 0)
            t_base = str(ob.get("target_base_id") or m_base)
            rew_cr = int(((m.get("rewards") or {}).get("credits")) or 0)
            if not iid or qty < 1 or qty > int(hold_cap) or rew_cr < min_prof or t_base != m_base:
                continue
            if iid not in asks_by_item:
                continue
            title = str(m.get("title") or "")
            mid = str(m.get("mission_id") or m.get("template_id") or title)
            jkey = "bhm:%s:%s" % (m_base, mid)
            if jkey in claimed_keys:
                continue
            for ab, aloc, ask_p, ask_q in asks_by_item[iid]:
                if ask_q < qty:
                    continue
                buy_cost = qty * ask_p * 1.05
                if buy_cost > max_spend or buy_cost <= 0:
                    continue
                p_hops = _bfs_hops(lanes, cur_sys, aloc[0]) if cur_sys and lanes else 0
                d_hops = _bfs_hops(lanes, aloc[0], mloc[0]) if lanes else (0 if aloc[0] == mloc[0] else 1)
                if p_hops is None or d_hops is None or p_hops > max_pick or d_hops > max_del:
                    continue
                tot_hops = max(1, p_hops + d_hops)
                est_prof = rew_cr - buy_cost - tot_hops * 45.0
                if est_prof < min_prof or (est_prof / buy_cost) < min_margin:
                    continue
                score = est_prof / float(tot_hops)
                if best is None or score > best[0]:
                    best = (score, {
                        "job_key": jkey, "mission_id": mid, "title": title,
                        "item": iid, "qty": qty, "reward_cr": rew_cr,
                        "buy_loc": aloc, "dest_loc": mloc,
                        "est_ask": ask_p, "est_profit": int(round(est_prof)),
                    })
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
    order_path = DATA / "fleet" / "orders" / (pilot + ".json")
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

    def go_dock(loc, refuel=True):
        sys_id, poi_id, base_id = loc[0], loc[1], loc[2]
        return run_goal("prepare-at-station", {"systemId": sys_id, "poiId": poi_id, "baseId": base_id, "refuel": bool(refuel)})

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
        strongholds = set(load_stronghold_bases(DATA)) if policy.get("exclude_strongholds", True) else set()
        # Also exclude systems with recent pirate sightings (<6h) from calm buy-wall arbitrage/liquidation
        try:
            _pdb = DATA / "store" / "read.db"
            if _pdb.is_file():
                import worldcache as _wc_p
                _pc = _wc_p.ro_db(_pdb, timeout=3.0)
                try:
                    _cut_p = time.time() - float(policy.get("pirate_avoid_hours") or 6.0) * 3600.0
                    for (_psubj,) in _pc.execute("SELECT DISTINCT subject FROM observations WHERE kind = 'pirate' AND t >= ?", (_cut_p,)):
                        if _psubj:
                            strongholds.add(str(_psubj).split(":", 1)[0].strip())
                    _pb_cut = time.time() - float(policy.get("pirate_battle_avoid_hours") or 2.0) * 3600.0
                    for (_pbs,) in _pc.execute("SELECT DISTINCT system FROM public_battles WHERE category = 'pirate' AND t >= ?", (_pb_cut,)):
                        if _pbs:
                            strongholds.add(str(_pbs).strip())
                except sqlite3.Error:
                    pass
                finally:
                    _pc.close()
        except Exception:
            pass
        lane_order = list(policy.get("lanes") or DEFAULT_POLICY["lanes"])
        _wlanes = policy.get("wing_lanes")
        if isinstance(_wlanes, dict):
            try:
                import manifest_wings as _mw_hl
                _hl_w = _mw_hl.wing_of(pilot)
                for _wpfx, _wl in _wlanes.items():
                    if _hl_w.startswith(str(_wpfx)) and isinstance(_wl, list) and _wl:
                        lane_order = list(_wl)
                        break
            except Exception:
                pass
        completed = 0

        # Flush any leftover non-protected cargo from prior runs if docked so hold capacity stays clean
        _cur_cargo = {k: v for k, v in get_cargo().items() if v > 0 and k not in PROTECTED_ITEMS and not str(k).startswith("package:")}
        _cur_base = str(ship_doc.get("base") or ship_doc.get("docked") or "")
        _emp_lb0 = read_json(Path(DATA) / "empire" / "empire.json", {})
        _active_lbs0 = {
            str(f.get("base")) for f in (_emp_lb0.get("facilities") or [])
            if isinstance(f, dict) and str(f.get("type") or "") == "faction_lockbox" and str(f.get("status") or "active") == "active" and f.get("base")
        }
        if _cur_cargo and _cur_base and _cur_base in base_map:
            _mb = save_market(_cur_base, base_map[_cur_base][0])
            _ora_f = (read_json(Path(DATA) / "fleet" / "price_oracle.json", {}) or {}).get("items") or {}
            import market_guard as _mg_f
            for _iid, _qty in list(_cur_cargo.items()):
                _row = _mb.get(_iid) or {}
                _bq = int(_row.get("best_buy_qty") or _row.get("buy_quantity") or 0)
                _bp = float(_row.get("best_buy") or 0)
                _fv_f = float((_ora_f.get(_iid) or {}).get("twap") or 0.0)
                _sfloor_f = _mg_f.safe_sell_floor(_iid, _bp, float(_row.get("best_sell") or 0), _fv_f)
                if _bp >= max(10, _sfloor_f) and _bq > 0:
                    _sq = min(_qty, _bq)
                    raw("sell", {"item_id": _iid, "quantity": _sq}, group="spacemolt")
                    time.sleep(TICK)
                    say("flushed %d leftover %s @ ~%d cr at %s" % (_sq, _iid, int(_bp), _cur_base))
                _left = get_cargo().get(_iid, 0)
                if _left > 0:
                    _dep_t = "faction" if _cur_base in _active_lbs0 else "self"
                    _rd_f = raw("deposit", {"item_id": _iid, "quantity": _left, "target": _dep_t, "source": "cargo"}, group="spacemolt_storage")
                    time.sleep(TICK)
                    if _dep_t == "faction" and "error" in _rd_f:
                        raw("deposit", {"item_id": _iid, "quantity": _left, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                        time.sleep(TICK)

        # Lockbox Bridge Sweeper: if this In-Faction Officer Hauler is currently docked at an active Lockbox hub
        # and holds non-reserved goods in its personal storage (e.g., gifted by non-faction Hunters!), drain them into
        # Shared Faction Lockbox so ALL 95 Haulers, Officer Crafters, and Officer Bursars immediately share them!
        if _cur_base and _cur_base in _active_lbs0 and _pilot_can_withdraw_faction(DATA, pilot):
            # Auto-register this docked Officer Hauler into receivers.json['hauler'][_cur_base] (up to 4 active
            # local Officers) so lawless Outpost Lockboxes always have live local Officer Hauler receivers!
            try:
                _rec_p = Path(DATA) / "fleet" / "receivers.json"
                _rec_l = Path(DATA) / "fleet" / "receivers.lock"
                with open(_rec_l, "a+", encoding="utf-8") as _rlf:
                    fcntl.flock(_rlf, fcntl.LOCK_EX)
                    try:
                        _rdoc = read_json(_rec_p, {})
                        if not isinstance(_rdoc, dict):
                            _rdoc = {}
                        _hmap = dict(_rdoc.get("hauler") or {}) if isinstance(_rdoc.get("hauler"), dict) else {}
                        _cur_v = _hmap.get(_cur_base)
                        _hlst = list(_cur_v) if isinstance(_cur_v, list) else ([_cur_v] if isinstance(_cur_v, str) and _cur_v else [])
                        if pilot not in _hlst:
                            _hlst.append(pilot)
                            if len(_hlst) > 4:
                                _hlst = _hlst[-4:]
                            _hmap[_cur_base] = _hlst[0] if len(_hlst) == 1 else _hlst
                            _rdoc["hauler"] = _hmap
                            write_json(_rec_p, _rdoc)
                    finally:
                        fcntl.flock(_rlf, fcntl.LOCK_UN)
            except Exception:
                pass
            try:
                _sv_r = body(raw("view", {"station_id": _cur_base, "target": "self"}, group="spacemolt_storage"))
                _sv_rows = _sv_r.get("items") or _sv_r.get("storage") or []
                _free_h0 = max(0, hold_cap - sum(get_cargo().values()))
                _dr_n = 0
                for _it in (_sv_rows if isinstance(_sv_rows, list) else []):
                    if not isinstance(_it, dict) or _dr_n >= 6 or _free_h0 < 5:
                        break
                    _ii, _iq = str(_it.get("item_id") or ""), int(_it.get("quantity") or 0)
                    if not _ii or _iq <= 0 or _ii in PROTECTED_ITEMS or _ii in ("fuel", "station_core"):
                        continue
                    _tq = min(_iq, _free_h0)
                    if _tq < 1:
                        break
                    _rw_h = raw("withdraw", {"item_id": _ii, "quantity": _tq, "target": "self"}, group="spacemolt_storage")
                    time.sleep(TICK)
                    if "error" not in _rw_h:
                        _rd_h = raw("deposit", {"item_id": _ii, "quantity": _tq, "target": "faction", "source": "cargo"}, group="spacemolt_storage")
                        time.sleep(TICK)
                        if "error" not in _rd_h:
                            _dr_n += 1
                            say("lockbox_drain %d %s self -> faction @ %s" % (_tq, _ii, _cur_base))
                        else:
                            raw("deposit", {"item_id": _ii, "quantity": _tq, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                            time.sleep(TICK)
                            break
            except Exception:
                pass

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

            elif lane == "hub_upkeep":
                books_rows = _load_books(DATA)
                claimed = active_claimed_keys(DATA)
                upk = _pick_hub_upkeep(DATA, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed, exclude_bases=strongholds)
                if upk and claim_job(DATA, pilot, upk["job_key"]):
                    iid, oloc, dloc, qty = upk["item"], upk["origin"], upk["dest"], upk["qty"]
                    say("hub_upkeep (%s) %d %s: %s -> %s (%dj+%dj)" % (
                        upk["mode"], qty, iid, oloc[2], dloc[2], upk["pickup_hops"], upk["delivery_hops"]))
                    ok_o, _ = go_dock(oloc, refuel=True)
                    if not ok_o:
                        release_job(DATA, pilot)
                        continue
                    have = 0
                    if upk["mode"] in ("transfer", "internal"):
                        raw("withdraw", {"item_id": iid, "quantity": qty, "target": upk.get("source_target") or "faction"}, group="spacemolt_storage")
                        time.sleep(TICK)
                        have = get_cargo().get(iid, 0)
                    else:
                        mb = save_market(oloc[2], oloc[0])
                        row = mb.get(iid) or {}
                        live_ask = float(row.get("best_sell") or 0)
                        live_aq = int(row.get("best_sell_qty") or row.get("sell_quantity") or 0)
                        if live_ask > 0 and live_ask <= float(upk.get("max_unit_price") or 0) and live_aq > 0:
                            buy_q = min(qty, live_aq, int(max(0, get_credits() - int(policy.get("fuel_reserve_cr") or 6000)) // (live_ask * 1.02)))
                            if buy_q >= 1:
                                raw("buy", {"item_id": iid, "quantity": buy_q, "auto_list": False}, group="spacemolt")
                                time.sleep(TICK)
                                have = get_cargo().get(iid, 0)
                    if have <= 0:
                        release_job(DATA, pilot)
                        continue
                    ok_d, _ = go_dock(dloc, refuel=(upk.get("hub_kind") == "station" and not upk.get("bunker_fill")))
                    if ok_d:
                        if upk.get("bunker_fill") and iid == "fuel_cell":
                            moved_f = burnt_c = 0
                            for _ in range(120):
                                st_now = get_state()
                                sh_now = st_now.get("ship") if isinstance(st_now.get("ship"), dict) else {}
                                cur_f = int(sh_now.get("fuel") if sh_now.get("fuel") is not None else (st_now.get("fuel") or 0))
                                max_f = int(sh_now.get("max_fuel") or st_now.get("max_fuel") or 95)
                                keep_f = min(30, max(10, max_f - 25))
                                cells_left = get_cargo().get("fuel_cell", 0)
                                n_burn = min(cells_left, max(0, max_f - cur_f) // 20)
                                if n_burn > 0:
                                    raw("refuel", {"item_id": "fuel_cell", "quantity": n_burn}, group="spacemolt")
                                    time.sleep(TICK)
                                    after_c = get_cargo().get("fuel_cell", 0)
                                    burnt_c += max(0, cells_left - after_c)
                                    st_now = get_state()
                                    sh_now = st_now.get("ship") if isinstance(st_now.get("ship"), dict) else {}
                                    cur_f = int(sh_now.get("fuel") if sh_now.get("fuel") is not None else (st_now.get("fuel") or 0))
                                if cur_f <= keep_f:
                                    if n_burn > 0:
                                        continue
                                    break
                                dep_f = cur_f - keep_f
                                raw("deposit", {"item_id": "fuel", "quantity": dep_f, "target": "faction"}, group="spacemolt_storage")
                                time.sleep(TICK)
                                st_after = get_state()
                                sh_after = st_after.get("ship") if isinstance(st_after.get("ship"), dict) else {}
                                f_after = int(sh_after.get("fuel") if sh_after.get("fuel") is not None else (st_after.get("fuel") or 0))
                                if f_after >= cur_f:
                                    break
                                moved_f += (cur_f - f_after)
                                if not get_cargo().get("fuel_cell", 0):
                                    break
                            rem_c = get_cargo().get("fuel_cell", 0)
                            if rem_c > 0:
                                raw("deposit", {"item_id": "fuel_cell", "quantity": rem_c, "target": "faction", "source": "cargo"}, group="spacemolt_storage")
                                time.sleep(TICK)
                            say("hub_upkeep BUNKER_FILLED +%d fuel (%d cells burnt, %d stored) -> %s" % (moved_f, burnt_c, rem_c, dloc[2]))
                            notes.append("hub_upkeep bunker +%d fuel -> %s" % (moved_f, dloc[2]))
                            completed += 1
                        else:
                            r_dep = raw("deposit", {"item_id": iid, "quantity": have, "target": "faction", "source": "cargo"}, group="spacemolt_storage")
                            time.sleep(TICK)
                            if "error" in r_dep:
                                _dep_err = str(r_dep.get("error") or "")[:90]
                                say("hub_upkeep DEPOSIT_ERR %d %s -> %s: %s" % (have, iid, dloc[2], _dep_err))
                                notes.append("hub_upkeep dep_err %s: %s" % (iid, _dep_err[:50]))
                                release_job(DATA, pilot)
                            else:
                                say("hub_upkeep DELIVERED %d %s -> %s" % (have, iid, dloc[2]))
                                notes.append("hub_upkeep %d %s -> %s" % (have, iid, dloc[2]))
                                completed += 1
                    else:
                        release_job(DATA, pilot)

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
                if not hasattr(_ep, "mark_convoy_started"):
                    import importlib as _il_h
                    _ep = _il_h.reload(_ep)
                _p_thr = _ep.load_pirate_threat(DATA, hours=6.0)
                _r_sys = _ep.load_recent_raids(DATA, hours=24.0)
                _s_meta = {}
                try:
                    _db = Path(DATA) / "store" / "read.db"
                    if _db.is_file():
                        import worldcache as _wc; _c = _wc.ro_db(_db, timeout=3.0)
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
                    convoy_fleet_created = False
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
                        if esc_key:
                            raw("undock", {}, group="spacemolt")
                            time.sleep(TICK)
                            cf = raw("create", {}, group="spacemolt_fleet")
                            time.sleep(TICK)
                            if "error" not in cf:
                                convoy_fleet_created = True
                                _rec_f = _ep.get_escort_request(DATA, esc_key) or {}
                                _arrived_es = [p_nm for p_nm, info in (_rec_f.get("escorts") or {}).items()
                                               if isinstance(info, dict) and info.get("arrived")]
                                _invited = []
                                for _epilot in _arrived_es:
                                    _pid32 = _ep.resolve_player_id(_epilot)
                                    _ir = raw("invite", {"player_id": _pid32}, group="spacemolt_fleet")
                                    time.sleep(TICK)
                                    if "error" in _ir:
                                        break
                                    _invited.append(_epilot)
                                if _invited:
                                    _ep.set_convoy_fleet(DATA, esc_key, pilot, _invited)
                                    _wait_acc = time.time() + 35.0
                                    while time.time() < _wait_acc and not stop_requested():
                                        _r2 = _ep.get_escort_request(DATA, esc_key) or {}
                                        _in_n = sum(1 for _p in _invited if ((_r2.get("escorts") or {}).get(_p) or {}).get("in_fleet"))
                                        if _in_n >= len(_invited):
                                            break
                                        time.sleep(3)
                                    say("convoy fleet locked with %d/%d escorts" % (len(_invited), len(_arrived_es)))
                            _ep.mark_convoy_started(DATA, esc_key)
                        ok_d, msg_d = go_dock(dloc)
                        if ok_d:
                            save_market(dloc[2], dloc[0])
                            del_r = raw("deliver", {"shipment_id": cid}, group="spacemolt_shipping")
                            time.sleep(TICK)
                            say("freight delivered %s -> %s (+%d cr%s)" % (cid[:8], dloc[2], pick["reward"], " ERR" if "error" in del_r else ""))
                            notes.append("freight %s +%d cr" % (cid[:8], pick["reward"]))
                            completed += 1
                            _dmeta = _s_meta.get(dloc[0]) or {}
                            if esc_key and not (_dmeta.get("empire") and not _dmeta.get("stronghold")):
                                _safe_border = _ep.nearest_policed_system(lanes, _s_meta, dloc[0], max_hops=12)
                                if _safe_border and _safe_border != dloc[0]:
                                    say("exiting lawless dest %s -> policed border %s under escort" % (dloc[0], _safe_border))
                                    raw("undock", {}, group="spacemolt")
                                    time.sleep(TICK)
                                    goal("navigate-to-system", {"targetSystemId": _safe_border}, timeout=240)
                    finally:
                        if convoy_fleet_created:
                            try:
                                raw("disband", {}, group="spacemolt_fleet")
                            except Exception:
                                pass
                        if esc_key:
                            _ep.clear_escort_request(DATA, esc_key)

            elif lane == "arbitrage":
                books_rows = _load_books(DATA)
                claimed = active_claimed_keys(DATA)
                peers = load_available_haulers(DATA, pilot, cur_sys, hold_cap, avail_cash, has_hazmat, policy, active_claimed_pilots(DATA))
                _cltv_buys_a = _load_cltv_open_buy_qty(DATA)
                _fair_p_a = None
                try:
                    import market_guard as _mg_h
                    _vwm_a = _mg_h.compute_book_vwm_map(books_rows, cltv_buy_qty=_cltv_buys_a)
                    _fair_p_a = _mg_h.update_price_oracle(DATA, _vwm_a)
                except Exception:
                    _fair_p_a = None
                job = assign_optimal_arbitrage(books_rows, base_map, lanes, peers, policy, claimed, exclude_bases=strongholds, fair_prices=_fair_p_a, cltv_buy_keys=_cltv_buys_a).get(pilot)
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
                    if live_bid >= live_ask * 0.92 and sell_q > 0:
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
                            list_p = max(int(round(live_ask * 1.05)), int(live_ask) + 2)
                            r_lo = raw("create_sell_order", {"item_id": iid, "quantity": got, "price_each": list_p}, group="spacemolt_market")
                            time.sleep(TICK)
                            if "error" not in r_lo:
                                say("arb %s bid slipped: listed %d at %s @ %d cr" % (iid, got, sloc[2], list_p))
                                notes.append("arb listed %d %s @ %d" % (got, iid, list_p))
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
                    raw("withdraw", {"item_id": iid, "quantity": qty, "target": sup.get("source_target") or "self"}, group="spacemolt_storage")
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

            elif lane == "liquidate_surplus":
                books_rows = _load_books(DATA)
                claimed = active_claimed_keys(DATA)
                liq = _pick_surplus_liquidation(DATA, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, policy, claimed, exclude_bases=strongholds)
                if liq and claim_job(DATA, pilot, liq["job_key"]):
                    iid, oloc, dloc, qty = liq["item"], liq["origin"], liq["dest"], liq["qty"]
                    say("liquidate %d %s: %s -> %s @ ~%d cr" % (qty, iid, oloc[2], dloc[2], liq["est_bid"]))
                    ok_o, _ = go_dock(oloc)
                    if not ok_o:
                        release_job(DATA, pilot)
                        continue
                    _src_t = liq.get("source_target") or "self"
                    raw("withdraw", {"item_id": iid, "quantity": qty, "target": _src_t}, group="spacemolt_storage")
                    time.sleep(TICK)
                    have = get_cargo().get(iid, 0)
                    if have <= 0:
                        release_job(DATA, pilot)
                        continue
                    ok_d, _ = go_dock(dloc)
                    if ok_d:
                        # Floor-protected multi-tier live bid liquidation: NEVER dump into 1-cr penny scrapers!
                        min_ok_bid = max(5.0, float(liq.get("est_bid") or 0) * 0.55)
                        for _tier_try in range(3):
                            cur_have = get_cargo().get(iid, 0)
                            if cur_have <= 0:
                                break
                            live_d = save_market(dloc[2], dloc[0])
                            rd_row = live_d.get(iid) or {}
                            lb_p = float(rd_row.get("best_buy") or 0)
                            lb_q = int(rd_row.get("best_buy_qty") or rd_row.get("buy_quantity") or 0)
                            if lb_p < min_ok_bid or lb_q <= 0:
                                break
                            sell_n = min(cur_have, lb_q)
                            raw("sell", {"item_id": iid, "quantity": sell_n}, group="spacemolt")
                            time.sleep(TICK)
                        rem = get_cargo().get(iid, 0)
                        if rem < have:
                            notes.append("liquidated %d %s @ %s" % (have - rem, iid, dloc[2]))
                        if rem > 0:
                            bp = docked_bursar_at(DATA, dloc[2])
                            if bp and bp != pilot and "error" not in raw("send_gift", {"recipient": bp, "item_id": iid, "quantity": rem}, group="spacemolt_social"):
                                time.sleep(TICK)
                                notes.append("liq->bursar %d %s" % (rem, iid))
                            else:
                                raw("deposit", {"item_id": iid, "quantity": rem, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                                time.sleep(TICK)
                        completed += 1

            elif lane == "consolidate_to_trader":
                books_rows = _load_books(DATA)
                claimed = active_claimed_keys(DATA)
                cons = _pick_consolidate_to_trader(DATA, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, policy, claimed, exclude_bases=strongholds)
                if cons and claim_job(DATA, pilot, cons["job_key"]):
                    iid, oloc, dloc, qty = cons["item"], cons["origin"], cons["dest"], cons["qty"]
                    say("consolidate %d %s: %s -> %s (bursar %s, ~%d cr)" % (qty, iid, oloc[2], dloc[2], cons.get("bursar_pilot") or "?", cons["est_val"]))
                    ok_o, _ = go_dock(oloc)
                    if not ok_o:
                        release_job(DATA, pilot)
                        continue
                    _src_t = cons.get("source_target") or "self"
                    raw("withdraw", {"item_id": iid, "quantity": qty, "target": _src_t}, group="spacemolt_storage")
                    time.sleep(TICK)
                    have = get_cargo().get(iid, 0)
                    if have <= 0:
                        release_job(DATA, pilot)
                        continue
                    ok_d, _ = go_dock(dloc)
                    if ok_d:
                        # Unified Shared Lockbox policy: deposit straight into shared Faction Lockbox FIRST so Bursars,
                        # Crafters, and Haulers all share instant access; fall back to gifting docked Bursar only if no Lockbox!
                        handed = False
                        rd = raw("deposit", {"item_id": iid, "quantity": have, "target": "faction", "source": "cargo"}, group="spacemolt_storage")
                        time.sleep(TICK)
                        if "error" not in rd:
                            handed = True
                            notes.append("cons->lockbox %d %s @ %s" % (have, iid, dloc[2]))
                        if not handed:
                            bp = docked_bursar_at(DATA, dloc[2]) or cons.get("bursar_pilot")
                            if bp and bp != pilot:
                                rg = raw("send_gift", {"recipient": bp, "item_id": iid, "quantity": have}, group="spacemolt_social")
                                time.sleep(TICK)
                                if "error" not in rg:
                                    handed = True
                                    notes.append("cons->bursar %d %s @ %s" % (have, iid, dloc[2]))
                        if not handed:
                            raw("deposit", {"item_id": iid, "quantity": have, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                            time.sleep(TICK)
                            notes.append("cons->self %d %s @ %s" % (have, iid, dloc[2]))
                        completed += 1
                    else:
                        release_job(DATA, pilot)

            elif lane == "backhaul_mission":
                books_rows = _load_books(DATA)
                claimed = active_claimed_keys(DATA)
                bhm = _pick_backhaul_delivery(DATA, pilot, books_rows, base_map, lanes, cur_sys, hold_cap, avail_cash, policy, claimed, exclude_bases=strongholds)
                if bhm and claim_job(DATA, pilot, bhm["job_key"]):
                    iid, qty = bhm["item"], bhm["qty"]
                    bloc, dloc = bhm["buy_loc"], bhm["dest_loc"]
                    say("backhaul_mission %s: buy %d %s @ %s -> deliver %s (rew +%d, est +%d cr)" % (
                        bhm["title"][:35], qty, iid, bloc[2], dloc[2], bhm["reward_cr"], bhm["est_profit"]))
                    ok_b, _ = go_dock(bloc)
                    if not ok_b:
                        release_job(DATA, pilot)
                        continue
                    q_chk = body(raw("estimate_market_order", {"item_id": iid, "quantity": qty, "side": "buy"}, group="spacemolt_market"))
                    est_u = float(q_chk.get("average_price") or q_chk.get("avg_price") or bhm["est_ask"])
                    if est_u * qty * 1.05 > bhm["reward_cr"] - 200:
                        say("backhaul_mission aborted: live ask %.0f exceeds budget" % est_u)
                        release_job(DATA, pilot)
                        continue
                    rb = raw("buy", {"item_id": iid, "quantity": qty, "auto_list": False}, group="spacemolt")
                    time.sleep(TICK)
                    got = get_cargo().get(iid, 0)
                    if "error" in rb or got < qty:
                        release_job(DATA, pilot)
                        continue
                    ok_d, _ = go_dock(dloc)
                    if ok_d:
                        board = body(raw("get_missions")).get("missions") or []
                        match_m = None
                        for bm in board if isinstance(board, list) else []:
                            if isinstance(bm, dict) and (str(bm.get("mission_id") or "") == bhm["mission_id"] or str(bm.get("title") or "") == bhm["title"]):
                                match_m = bm
                                break
                        done_m = False
                        if match_m:
                            post_mid = str(match_m.get("mission_id") or match_m.get("template_id") or "")
                            if post_mid:
                                acc_r = raw("accept_mission", {"mission_id": post_mid})
                                time.sleep(TICK)
                                if "error" not in acc_r:
                                    acc_b = body(acc_r)
                                    comp_mid = str(acc_b.get("mission_id") or post_mid)
                                    comp_r = raw("complete_mission", {"mission_id": comp_mid})
                                    time.sleep(TICK)
                                    if "error" not in comp_r:
                                        done_m = True
                                        notes.append("backhaul_mission %s +%d cr" % (bhm["title"][:30], bhm["reward_cr"]))
                                        say("backhaul_mission COMPLETED %s (+%d cr)" % (bhm["title"][:35], bhm["reward_cr"]))
                                    else:
                                        raw("abandon_mission", {"mission_id": comp_mid})
                                        time.sleep(TICK)
                        if not done_m:
                            raw("sell", {"item_id": iid, "quantity": got}, group="spacemolt")
                            time.sleep(TICK)
                            rem = get_cargo().get(iid, 0)
                            if rem > 0:
                                inv_cost[0] += int(round(rem * est_u))
                                bp = docked_bursar_at(DATA, dloc[2])
                                if bp and bp != pilot and "error" not in raw("send_gift", {"recipient": bp, "item_id": iid, "quantity": rem}, group="spacemolt_social"):
                                    time.sleep(TICK)
                                else:
                                    raw("deposit", {"item_id": iid, "quantity": rem, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                                    time.sleep(TICK)
                            notes.append("backhaul_mission fallback sold/gifted %d %s" % (got, iid))
                        completed += 1

        if completed == 0:
            watch_s = float(policy.get("rest_seconds_when_empty") or (float(policy.get("idle_watch_minutes") or 15) * 60.0))
            poll_s = min(180.0, max(5.0, float(policy.get("idle_poll_interval_s") or 15.0)))
            say("no eligible haul/freight/arb/supply job matched policy right now; docked watch %ds (poll %ds)" % (int(watch_s), int(poll_s)))
            notes.append("docked watch %dm" % max(1, int(round(watch_s / 60.0))))
            end_nap = time.time() + watch_s
            next_poll = time.time() + poll_s
            while time.time() < end_nap and not stop_requested():
                time.sleep(min(5.0, max(1.0, end_nap - time.time())))
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
                                raw("withdraw", {"item_id": iid, "quantity": qty, "target": sup.get("source_target") or "self"}, group="spacemolt_storage")
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
