#!/usr/bin/env python3
"""
WHAT: Ridgecrest-anchored Hub-and-Spoke Passenger Liner AutoNet (`6B. Passenger & Resort Liners`).
HOW : Runs one bounded session (`--minutes 40`) for a berth-equipped 6B liner (`Futures`, `Loose Change`,
      `Consortium`, `Concordia`, `Premiere`, etc., or any ship with a fitted passenger cabin).
      Uses free zero-tick remote `list_station_passengers` polling (90s shared cache across all 28 liners)
      to maximize VIP/First-Class fares (`6x`), speed bonuses (`+50%`), Ridgecrest inbound resort tourism
      spend (`100%` venue revenue into Treasury), and Ridgecrest Transit Lounge layovers (`+25%` free
      tourism revenue with zero upkeep footfall).

Usage:
    python3 -I -B game/fleet/passenger_net.py --pilot "<name>" [--minutes 40] [--dry]
"""
import fcntl
import json
import sqlite3
import sys
import time
import concurrent.futures
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import fuelplan

PASSENGER_HULL_BERTHS = {
    "technically_legal": {"economy": 1, "business": 0, "first": 0},
    "cogito":            {"economy": 1, "business": 0, "first": 0},
    "fugue":             {"economy": 0, "business": 1, "first": 0},
    "futures":           {"economy": 0, "business": 1, "first": 0},
    "loose_change":      {"economy": 4, "business": 0, "first": 0},
    "nebula_tender":     {"economy": 2, "business": 1, "first": 0},
    "pennon":            {"economy": 0, "business": 2, "first": 2},
    "omnibus":           {"economy": 14, "business": 0, "first": 0},
    "consortium":        {"economy": 8, "business": 4, "first": 0},
    "reticence":         {"economy": 0, "business": 4, "first": 0},
    "muster":            {"economy": 18, "business": 2, "first": 0},
    "promenade":         {"economy": 12, "business": 6, "first": 1},
    "midlife_crisis":    {"economy": 16, "business": 2, "first": 0},
    "cloister":          {"economy": 10, "business": 6, "first": 1},
    "treasury":          {"economy": 0, "business": 0, "first": 3},
    "concordia":         {"economy": 0, "business": 8, "first": 2},
    "premiere":          {"economy": 16, "business": 8, "first": 4},
    "liquidity_event":   {"economy": 0, "business": 0, "first": 8},
    "midas":             {"economy": 0, "business": 0, "first": 6},
    "comet":             {"economy": 0, "business": 0, "first": 48},
}

CABIN_MODULE_BERTHS = {
    "economy_passenger_cabin":     ("economy", 12),
    "business_passenger_cabin":    ("business", 6),
    "first_class_passenger_suite": ("first", 3),
}

DEFAULT_POLICY = {
    "enabled": True,
    "home_base": "a2cee88abdcb31db229c04315f0ef6e1",
    "home_system": "ridgecrest",
    "board_cache_ttl_s": 90,
    "max_hops": 16,
    "min_fare_per_jump": 220,
    "ridgecrest_dest_bonus": 2.0,
    "ridgecrest_origin_bonus": 1.6,
    "first_class_bonus": 1.35,
    "business_class_bonus": 1.15,
    "corridor_detour_max_hops": 3,
    "max_multi_stops": 2,
    "enable_lounge_layovers": True,
    "lounge_detour_max_hops": 4,
    "lounge_min_free_slots": 2,
    "policed_only": False,
    "avoid_pirate_hours": 4.0,
    "avoid_pirate_strongholds": True,
    "min_fuel_pct_before_jump": 25.0,
    "max_reposition_hops": 14,
    "rest_seconds_when_empty": 20,
    "use_jumpgates": True,
    "max_gate_toll_cr": 500,
    "gate_cr_per_jump": 140.0,
}


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {} if default is None else default


def read_policy(policy_path=None):
    p = Path(policy_path) if policy_path else (ROOT / "passenger-policy.json")
    raw = read_json(p, {})
    pol = dict(DEFAULT_POLICY)
    if isinstance(raw, dict):
        pol.update(raw)
    return pol


def is_enabled(policy):
    return bool((policy or {}).get("enabled", False))


def ship_berths(hull_class, modules=None):
    """Compute total {economy, business, first} passenger berths from hull + installed cabins."""
    cid = str(hull_class or "").strip().lower().replace(" ", "_").replace("-", "_")
    base = dict(PASSENGER_HULL_BERTHS.get(cid) or {"economy": 0, "business": 0, "first": 0})
    for m in (modules or []):
        if isinstance(m, dict):
            mid = str(m.get("type_id") or m.get("id") or m.get("module") or "").strip().lower()
        else:
            mid = str(m or "").strip().lower()
        if mid in CABIN_MODULE_BERTHS:
            cls, cap = CABIN_MODULE_BERTHS[mid]
            base[cls] = base.get(cls, 0) + cap
    return base


def total_berths(berths):
    return int((berths or {}).get("economy", 0)) + int((berths or {}).get("business", 0)) + int((berths or {}).get("first", 0))


def simulate_seat_allocation(passengers, berths):
    """Greedy SpaceMolt seat allocation (first -> business -> economy, matching game downgrade rules).
    Returns (seated_list, total_fare, remaining_berths)."""
    rem = {
        "first": int((berths or {}).get("first", 0)),
        "business": int((berths or {}).get("business", 0)),
        "economy": int((berths or {}).get("economy", 0)),
    }
    order = {"first": 0, "business": 1, "economy": 2}
    ranked = sorted(
        [p for p in (passengers or []) if isinstance(p, dict)],
        key=lambda x: (order.get(str(x.get("class") or "economy").lower(), 2), -int(x.get("estimated_fare") or x.get("base_fare") or 0)),
    )
    seated = []
    tot_fare = 0
    for p in ranked:
        cls = str(p.get("class") or "economy").lower()
        if cls == "first":
            if rem["first"] > 0:
                rem["first"] -= 1
            else:
                continue
        elif cls == "business":
            if rem["business"] > 0:
                rem["business"] -= 1
            elif rem["first"] > 0:
                rem["first"] -= 1
            else:
                continue
        else:
            if rem["economy"] > 0:
                rem["economy"] -= 1
            elif rem["business"] > 0:
                rem["business"] -= 1
            elif rem["first"] > 0:
                rem["first"] -= 1
            else:
                continue
        seated.append(p)
        tot_fare += int(p.get("estimated_fare") or p.get("base_fare") or 0)
    return seated, tot_fare, rem


def has_passenger_work(pilot_name, pilot_info=None, data_dir=None, repo_root=None, policy_path=None):
    """True iff policy is enabled and pilot's active ship has >= 1 passenger berth (hull or fitted cabin)."""
    pol = read_policy(policy_path)
    if not is_enabled(pol):
        return False
    pinfo = pilot_info if isinstance(pilot_info, dict) else {}
    hcls = pinfo.get("class") or pinfo.get("class_id") or pinfo.get("ship_class") or ""
    mods = pinfo.get("modules") or []
    if data_dir and (not hcls or not mods):
        db_p = Path(data_dir) / "store" / "read.db"
        if db_p.is_file():
            try:
                con = sqlite3.connect("file:%s?mode=ro&immutable=1" % db_p, uri=True, timeout=3)
                try:
                    if not hcls:
                        r = con.execute("SELECT class FROM ships WHERE pilot=?", (pilot_name,)).fetchone()
                        if r and r[0]:
                            hcls = str(r[0])
                    if not mods:
                        mods = [r[0] for r in con.execute("SELECT module FROM ship_modules WHERE pilot=?", (pilot_name,)).fetchall() if r and r[0]]
                finally:
                    con.close()
            except sqlite3.Error:
                pass
    b = ship_berths(hcls, mods)
    return total_berths(b) > 0


def load_graph(data_dir):
    """Load galaxy lane graph, base->system map, stronghold set, and Ridgecrest refueling_dock status."""
    adj = {}
    base_to_sys = {}
    sys_to_base = {}
    base_to_poi = {}
    name_to_sys = {}
    strongholds = set()
    refuel_ready = set()
    gates = fuelplan.load_gates(data_dir)
    db_p = Path(data_dir) / "store" / "read.db"
    if not db_p.is_file():
        return {"adj": adj, "base_to_sys": base_to_sys, "sys_to_base": sys_to_base, "name_to_sys": name_to_sys, "strongholds": strongholds, "refuel_ready": refuel_ready, "gates": gates}
    con = sqlite3.connect("file:%s?mode=ro&immutable=1" % db_p, uri=True, timeout=5)
    try:
        for a, b in con.execute("SELECT a, b FROM lanes").fetchall():
            if a and b:
                adj.setdefault(str(a), []).append(str(b))
                adj.setdefault(str(b), []).append(str(a))
        for sid, sname, sh in con.execute("SELECT id, name, stronghold FROM systems").fetchall():
            if sid:
                ss = str(sid)
                if sname:
                    name_to_sys[str(sname).strip().lower()] = ss
                name_to_sys[ss.lower()] = ss
                if sh:
                    strongholds.add(ss)
        for tbl in ("bases", "places"):
            try:
                for b_id, s_id in con.execute("SELECT base, system FROM %s WHERE base IS NOT NULL AND system IS NOT NULL" % tbl).fetchall():
                    bs, ss = str(b_id), str(s_id)
                    if bs and ss:
                        base_to_sys[bs] = ss
                        sys_to_base.setdefault(ss, bs)
            except sqlite3.Error:
                pass
        try:
            for b_id, p_id in con.execute("SELECT base, poi FROM places WHERE base IS NOT NULL AND poi IS NOT NULL").fetchall():
                if b_id and p_id:
                    base_to_poi[str(b_id)] = str(p_id)
        except sqlite3.Error:
            pass
        try:
            for (b_id,) in con.execute("SELECT DISTINCT base FROM faction_facilities WHERE type='refueling_dock' AND COALESCE(status,'active')='active'").fetchall():
                if b_id:
                    refuel_ready.add(str(b_id))
        except sqlite3.Error:
            pass
    finally:
        con.close()
    return {
        "adj": adj,
        "base_to_sys": base_to_sys,
        "sys_to_base": sys_to_base,
        "base_to_poi": base_to_poi,
        "name_to_sys": name_to_sys,
        "strongholds": strongholds,
        "refuel_ready": refuel_ready,
        "gates": gates,
    }


def _resolve_dest_sys(pax, graph):
    dbase = str((pax or {}).get("destination") or "").strip()
    b2s = (graph or {}).get("base_to_sys") or {}
    adj = (graph or {}).get("adj") or {}
    n2s = (graph or {}).get("name_to_sys") or {}
    if dbase and dbase in b2s:
        return str(b2s[dbase])
    raw_s = str((pax or {}).get("destination_system") or "").strip()
    if raw_s in adj:
        return raw_s
    if raw_s:
        mapped = n2s.get(raw_s.lower()) or n2s.get(raw_s.lower().replace(" ", "_"))
        if mapped:
            return mapped
        slug = raw_s.lower().replace(" ", "_").replace("-", "_")
        if slug in adj:
            return slug
    return ""


def bfs_path(adj, src, dst, avoid=None, max_hops=24):
    """Shortest path [src, ..., dst] avoiding blocked systems, or None."""
    if not src or not dst:
        return None
    if src == dst:
        return [src]
    av = avoid or set()
    q = deque([(src, [src])])
    seen = {src}
    while q:
        u, path = q.popleft()
        if len(path) - 1 >= max_hops:
            continue
        for v in adj.get(u) or ():
            if v in seen:
                continue
            if v != dst and v in av:
                continue
            npath = path + [v]
            if v == dst:
                return npath
            seen.add(v)
            q.append((v, npath))
    return None


def bfs_dists(adj, src, avoid=None, max_hops=24):
    if not src:
        return {}
    av = avoid or set()
    d = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        if d[u] >= max_hops:
            continue
        for v in adj.get(u) or ():
            if v in d or v in av:
                continue
            d[v] = d[u] + 1
            q.append(v)
    return d


def score_station_board(origin_base, origin_sys, board, berths, graph, policy, avoid=None, pilot_credits=None):
    """Score all candidate destination groups from a station's waiting + transit_lounge list."""
    adj = graph["adj"]
    gates = (graph.get("gates") or {}) if policy.get("use_jumpgates", True) else {}
    home_base = str(policy.get("home_base") or "")
    max_hops = int(policy.get("max_hops") or 16)
    min_fpj = float(policy.get("min_fare_per_jump") or 220.0)
    rc_bonus = float(policy.get("ridgecrest_dest_bonus") or 2.0)
    first_b = float(policy.get("first_class_bonus") or 1.35)
    bus_b = float(policy.get("business_class_bonus") or 1.15)
    max_toll = int(policy.get("max_gate_toll_cr") or 500)
    cpj = float(policy.get("gate_cr_per_jump") or 140.0)
    wdists = fuelplan.weighted_dists(adj, origin_sys, gates=gates, avoid=avoid, max_hops=max_hops, cr_per_jump=cpj, max_toll=max_toll, pilot_credits=pilot_credits)

    all_pax = list((board or {}).get("waiting") or [])
    lounge = (board or {}).get("transit_lounge")
    if isinstance(lounge, dict):
        all_pax.extend(lounge.get("passengers") or [])

    by_dest = {}
    for p in all_pax:
        if not isinstance(p, dict):
            continue
        dbase = str(p.get("destination") or "").strip()
        if not dbase or dbase == origin_base:
            continue
        dsys = _resolve_dest_sys(p, graph)
        if not dsys:
            continue
        by_dest.setdefault(dbase, {"dest_sys": dsys, "pax": []})["pax"].append(p)

    cands = []
    for dbase, info in by_dest.items():
        dsys = info["dest_sys"]
        wrow = wdists.get(dsys)
        if wrow is None:
            continue
        hops, toll_cr, _cost = wrow
        if hops <= 0 or hops > max_hops:
            continue
        seated, fare, rem_b = simulate_seat_allocation(info["pax"], berths)
        if not seated or fare <= 0:
            continue
        net_fare = max(0, int(fare) - int(toll_cr))
        if net_fare <= 0:
            continue
        fpj = float(net_fare) / float(max(1, hops))
        if fpj < min_fpj and dbase != home_base:
            continue
        classes = {str(x.get("class") or "economy").lower() for x in seated}
        mult = 1.0
        if dbase == home_base:
            mult *= rc_bonus
        if "first" in classes:
            mult *= first_b
        elif "business" in classes:
            mult *= bus_b
        score = fpj * mult
        cands.append({
            "dest_base": dbase,
            "dest_sys": dsys,
            "hops": hops,
            "toll_cr": int(toll_cr),
            "fare": net_fare,
            "gross_fare": int(fare),
            "fpj": round(fpj, 1),
            "count": len(seated),
            "score": round(score, 1),
            "has_first": "first" in classes,
            "rem_berths": rem_b,
        })
    cands.sort(key=lambda x: (-x["score"], x["hops"], -x["fare"]))
    return cands


def choose_reposition_hub(cur_sys, boards_cache, berths, graph, policy, claimed_hubs=None, avoid=None):
    """Pick the best station with waiting passengers to reposition to (strong Ridgecrest home bias)."""
    adj = graph["adj"]
    b2s = graph["base_to_sys"]
    home_base = str(policy.get("home_base") or "")
    home_sys = str(policy.get("home_system") or "ridgecrest")
    max_rep = int(policy.get("max_reposition_hops") or 14)
    rc_orig_b = float(policy.get("ridgecrest_origin_bonus") or 1.6)
    claimed = claimed_hubs or set()
    gates = (graph.get("gates") or {}) if policy.get("use_jumpgates", True) else {}
    max_toll = int(policy.get("max_gate_toll_cr") or 500)
    cpj = float(policy.get("gate_cr_per_jump") or 140.0)
    wdists = fuelplan.weighted_dists(adj, cur_sys, gates=gates, avoid=avoid, max_hops=max_rep, cr_per_jump=cpj, max_toll=max_toll)

    best = None
    for bid, bdata in (boards_cache or {}).items():
        if not isinstance(bdata, dict):
            continue
        sys_id = str(bdata.get("system") or b2s.get(bid) or "")
        if not sys_id or sys_id not in wdists:
            continue
        if bid in claimed and bid != home_base:
            continue
        hops, rep_toll, _rcost = wdists[sys_id]
        if hops > max_rep:
            continue
        cands = score_station_board(bid, sys_id, bdata, berths, graph, policy, avoid=avoid)
        if not cands:
            continue
        top_fare = max(0, sum(c["fare"] for c in cands[:2]) - int(rep_toll))
        if top_fare <= 0:
            continue
        mult = rc_orig_b if bid == home_base else 1.0
        sc = (float(top_fare) * mult) / (float(hops) + 1.5)
        if best is None or sc > best["score"]:
            best = {"base": bid, "system": sys_id, "hops": hops, "toll_cr": int(rep_toll), "score": sc, "est_fare": top_fare}
    dists = {s: row[0] for s, row in wdists.items()}
    if best:
        return best
    if home_base and home_sys in dists and cur_sys != home_sys:
        return {"base": home_base, "system": home_sys, "hops": dists[home_sys], "score": 1.0, "est_fare": 0}
    return None


def _raw(gate_mod, pilot, action, params=None, group="spacemolt", timeout=45):
    st, txt = gate_mod.call(
        "post",
        "/accounts/%s/raw" % gate_mod.q(pilot),
        {"toolGroup": group, "action": action, "params": params or {}},
        timeout=timeout,
    )
    if st == 200 and isinstance(txt, str) and "{" in txt:
        try:
            j = json.loads(txt[txt.find("{"):])
            if isinstance(j, dict) and (j.get("error") or j.get("isError") or j.get("success") is False):
                err_msg = str(j.get("error") or j.get("message") or j.get("result") or txt)
                return False, {}, err_msg
            sc = j.get("structuredContent") if isinstance(j, dict) else {}
            if isinstance(sc, dict) and sc.get("error"):
                return False, sc, str(sc.get("error"))
            return True, sc if isinstance(sc, dict) else {}, str(j.get("result") or "")
        except ValueError:
            return True, {}, txt
    return False, {}, str(txt)


def _stop_requested(data_dir, pilot):
    return (Path(data_dir) / "fleet" / "host" / "stop" / pilot).exists() or (Path(data_dir) / "fleet" / "STOP").exists()


def _denied_bases(data_dir, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    doc = read_json(Path(data_dir) / "fleet" / "passenger_denied_bases.json", {})
    if not isinstance(doc, dict):
        return set()
    return {str(k) for k, exp in doc.items() if float(exp or 0) > now_t}


def _record_denied_base(data_dir, base_id, ttl_s=86400):
    if not base_id:
        return
    p = Path(data_dir) / "fleet" / "passenger_denied_bases.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    now_t = time.time()
    doc = read_json(p, {})
    if not isinstance(doc, dict):
        doc = {}
    doc = {str(k): v for k, v in doc.items() if float(v or 0) > now_t}
    doc[str(base_id)] = int(now_t + ttl_s)
    try:
        p.write_text(json.dumps(doc, sort_keys=True) + "\n", encoding="ascii")
    except OSError:
        pass


def _refresh_boards_cache(gate_mod, pilot, data_dir, graph, policy):
    cache_p = Path(data_dir) / "fleet" / "passenger_boards.json"
    ttl = float(policy.get("board_cache_ttl_s") or 90.0)
    now = time.time()
    cached = read_json(cache_p, {})
    if isinstance(cached, dict) and (now - float(cached.get("updated_at") or 0)) < ttl and len(cached.get("boards") or {}) >= 10:
        return cached["boards"]
    cache_p.parent.mkdir(parents=True, exist_ok=True)
    lock_p = cache_p.with_suffix(".lock")
    with open(lock_p, "a+") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        now = time.time()
        cached = read_json(cache_p, {})
        if isinstance(cached, dict) and (now - float(cached.get("updated_at") or 0)) < ttl and len(cached.get("boards") or {}) >= 10:
            return cached["boards"]
        b2s = graph["base_to_sys"]
        scan_list = list(policy.get("scan_stations") or [])
        hb = str(policy.get("home_base") or "")
        if hb and hb not in scan_list:
            scan_list.insert(0, hb)
        boards = {}
        if isinstance(cached, dict) and isinstance(cached.get("boards"), dict):
            for k, v in cached["boards"].items():
                if isinstance(v, dict) and (now - float(v.get("t") or 0)) < 600.0:
                    boards[k] = v
        def _poll_one(bid):
            ok, sc, _ = _raw(gate_mod, pilot, "list_station_passengers", {"id": bid}, timeout=10)
            if ok and isinstance(sc, dict):
                return bid, {
                    "system": b2s.get(bid, ""),
                    "waiting": sc.get("waiting") or [],
                    "transit_lounge": sc.get("transit_lounge"),
                    "fare_surge": sc.get("fare_surge"),
                    "demand_level": sc.get("demand_level"),
                    "t": int(now),
                }
            return bid, None
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
            futs = [ex.submit(_poll_one, bid) for bid in scan_list]
            done, _ = concurrent.futures.wait(futs, timeout=35)
            for f in done:
                try:
                    bid, bobj = f.result()
                    if bobj is not None:
                        boards[bid] = bobj
                except Exception:
                    pass
        try:
            cache_p.write_text(json.dumps({"updated_at": int(now), "boards": boards}) + "\n", encoding="ascii")
        except OSError:
            pass
        return boards


def _fly_and_dock(gate_mod, pilot, cur_sys, docked_base, dest_sys, dest_base, graph, policy, data_dir, pilot_credits=None):
    """Navigate cleanly along toll-aware shortest path (with gate circuit-breaker), refuel safely, and dock."""
    avoid = set(graph["strongholds"]) if policy.get("avoid_pirate_strongholds", True) else set()
    gates = (graph.get("gates") or {}) if policy.get("use_jumpgates", True) else {}
    max_h = int(policy.get("max_hops") or 16) + 4
    max_t = int(policy.get("max_gate_toll_cr") or 500)
    cpj = float(policy.get("gate_cr_per_jump") or 140.0)
    path, _, _ = fuelplan.weighted_shortest_path(graph["adj"], cur_sys, dest_sys, gates=gates, avoid=avoid, max_hops=max_h, cr_per_jump=cpj, max_toll=max_t, pilot_credits=pilot_credits)
    if not path:
        return False, cur_sys, docked_base, "no_route"
    home_base = str(policy.get("home_base") or "")
    if docked_base and (docked_base != home_base or home_base in graph["refuel_ready"]):
        _raw(gate_mod, pilot, "refuel", {}, timeout=25)
    if cur_sys != dest_sys:
        if docked_base:
            ok_u, _, _ = _raw(gate_mod, pilot, "undock", {}, timeout=35)
            if ok_u:
                docked_base = ""
                time.sleep(10.2)
        idx = 1
        resyncs = 0
        while idx < len(path):
            nxt = path[idx]
            if _stop_requested(data_dir, pilot):
                return False, cur_sys, docked_base, "stopped"
            ok_j, sc_j, msg_j = _raw(gate_mod, pilot, "jump", {"id": nxt}, timeout=120)
            if not ok_j:
                low_m = msg_j.lower()
                if (cur_sys, nxt) in gates and ("gate_refused" in low_m or "gate_toll" in low_m or "gate" in low_m):
                    fuelplan.record_gate_block(data_dir, cur_sys, nxt, reason=low_m[:40])
                    gates.pop((cur_sys, nxt), None)
                    gates.pop((nxt, cur_sys), None)
                    alt_path, _, _ = fuelplan.weighted_shortest_path(graph["adj"], cur_sys, dest_sys, gates=gates, avoid=avoid, max_hops=max_h + 6, cr_per_jump=cpj, max_toll=max_t, pilot_credits=pilot_credits)
                    if alt_path and len(alt_path) > 1:
                        path = alt_path
                        idx = 1
                        continue
                if resyncs < 2 and ("not connected" in low_m or "already in" in low_m or "must undock" in low_m or "docked" in low_m):
                    resyncs += 1
                    ok_gs, sc_gs, _ = _raw(gate_mod, pilot, "get_status", {}, timeout=25)
                    if ok_gs and isinstance(sc_gs, dict):
                        loc_gs = sc_gs.get("location") or {}
                        real_sys = str(loc_gs.get("system_id") or "")
                        real_base = str(loc_gs.get("base_id") or loc_gs.get("docked_at_base") or "")
                        if real_sys:
                            cur_sys = real_sys
                        docked_base = real_base
                        if docked_base:
                            ok_u2, _, _ = _raw(gate_mod, pilot, "undock", {}, timeout=35)
                            if ok_u2:
                                docked_base = ""
                                time.sleep(10.2)
                        if cur_sys == dest_sys:
                            break
                        re_path, _, _ = fuelplan.weighted_shortest_path(graph["adj"], cur_sys, dest_sys, gates=gates, avoid=avoid, max_hops=max_h + 6, cr_per_jump=cpj, max_toll=max_t, pilot_credits=pilot_credits)
                        if re_path and len(re_path) > 1:
                            path = re_path
                            idx = 1
                            continue
                return False, cur_sys, docked_base, "jump_fail:" + msg_j[:60]
            arrived = ""
            if isinstance(sc_j, dict):
                det = sc_j.get("details") if isinstance(sc_j.get("details"), dict) else {}
                loc_j = sc_j.get("location") if isinstance(sc_j.get("location"), dict) else {}
                arrived = str(det.get("system_id") or loc_j.get("system_id") or "")
            if arrived and arrived != nxt and resyncs < 2:
                resyncs += 1
                cur_sys = arrived
                if cur_sys == dest_sys:
                    break
                re_path, _, _ = fuelplan.weighted_shortest_path(graph["adj"], cur_sys, dest_sys, gates=gates, avoid=avoid, max_hops=max_h + 6, cr_per_jump=cpj, max_toll=max_t, pilot_credits=pilot_credits)
                if re_path and len(re_path) > 1:
                    path = re_path
                    idx = 1
                    time.sleep(10.2)
                    continue
            cur_sys = arrived or nxt
            idx += 1
            time.sleep(10.2)
    if docked_base != dest_base:
        if docked_base:
            _raw(gate_mod, pilot, "undock", {}, timeout=35)
            docked_base = ""
            time.sleep(10.2)
        travel_target = (graph.get("base_to_poi") or {}).get(dest_base, dest_base)
        ok_t, _, msg_t = _raw(gate_mod, pilot, "travel", {"id": travel_target}, timeout=120)
        if not ok_t:
            return False, cur_sys, docked_base, "travel_fail:" + msg_t[:60]
        time.sleep(10.2)
        ok_d, _, msg_d = _raw(gate_mod, pilot, "dock", {}, timeout=45)
        if not ok_d and "already docked" not in msg_d.lower():
            low_d = msg_d.lower()
            if "access denied" in low_d or "access_denied" in low_d or "forbidden" in low_d:
                _record_denied_base(data_dir, dest_base)
            return False, cur_sys, docked_base, "dock_fail:" + msg_d[:60]
        docked_base = dest_base
        time.sleep(10.2)
    return True, cur_sys, docked_base, "ok"


def _record_run(data_dir, rec):
    p = Path(data_dir) / "routes" / "runs.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    lock_p = p.with_suffix(".lock")
    try:
        with open(lock_p, "a+") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            with open(p, "a", encoding="ascii") as out:
                out.write(json.dumps(rec, ensure_ascii=True) + "\n")
    except OSError:
        pass


def run_pilot(pilot, minutes=40, route_id="passenger-network", policy_path=None, data_dir="/srv/collective/data"):
    import gate
    pol = read_policy(policy_path)
    if not is_enabled(pol):
        print("%s %s passenger_net: disabled in policy" % (utc_now(), pilot), flush=True)
        return 0
    t0 = time.time()
    deadline = t0 + max(5, int(minutes)) * 60
    graph = load_graph(data_dir)
    home_base = str(pol.get("home_base") or "")
    home_sys = str(pol.get("home_system") or "ridgecrest")

    ok_s, sc_s, _ = _raw(gate, pilot, "get_status", {}, timeout=25)
    if not ok_s:
        print("%s %s passenger_net: get_status failed" % (utc_now(), pilot), flush=True)
        return 1
    pl = sc_s.get("player") or {}
    sh = sc_s.get("ship") or {}
    loc = sc_s.get("location") or {}
    cr_before = int(pl.get("credits") or 0)
    cur_sys = str(loc.get("system_id") or "")
    docked_base = str(loc.get("base_id") or loc.get("docked_at_base") or "")
    hcls = str(sh.get("class_id") or sh.get("class_name") or "")
    mods = sh.get("modules") or []
    berths = ship_berths(hcls, mods)
    if total_berths(berths) <= 0:
        print("%s %s passenger_net: 0 berths on %s; exiting" % (utc_now(), pilot, hcls), flush=True)
        return 0

    delivered_trips = 0
    layovers = 0
    notes = []

    if not docked_base:
        local_b = graph["sys_to_base"].get(cur_sys)
        if local_b:
            ok_f, cur_sys, docked_base, why = _fly_and_dock(gate, pilot, cur_sys, "", cur_sys, local_b, graph, pol, data_dir)
            if not ok_f:
                notes.append(why)
        else:
            ok_f, cur_sys, docked_base, why = _fly_and_dock(gate, pilot, cur_sys, "", home_sys, home_base, graph, pol, data_dir)
            if not ok_f:
                notes.append(why)

    while time.time() < deadline and not _stop_requested(data_dir, pilot):
        ok_lp, sc_lp, _ = _raw(gate, pilot, "list_passengers", {}, timeout=20)
        aboard = (sc_lp.get("passengers") or []) if ok_lp and isinstance(sc_lp, dict) else []
        if aboard:
            dists = bfs_dists(graph["adj"], cur_sys, avoid=graph["strongholds"], max_hops=24)
            best_d = None
            for pax in aboard:
                db = str(pax.get("destination") or "")
                ds = _resolve_dest_sys(pax, graph)
                h = dists.get(ds, 999)
                if db and ds and (best_d is None or h < best_d[0]):
                    best_d = (h, db, ds)
            if best_d:
                _, db, ds = best_d
                did_layover = False
                if (
                    pol.get("enable_lounge_layovers", True)
                    and home_base
                    and db != home_base
                    and docked_base != home_base
                    and home_base in graph["refuel_ready"]
                ):
                    d_to_rc = dists.get(home_sys, 999)
                    d_rc_to_dst = bfs_dists(graph["adj"], home_sys, avoid=graph["strongholds"], max_hops=24).get(ds, 999)
                    if d_to_rc + d_rc_to_dst <= best_d[0] + int(pol.get("lounge_detour_max_hops") or 4):
                        ok_rb, sc_rb, _ = _raw(gate, pilot, "list_station_passengers", {"id": home_base}, timeout=15)
                        lg = (sc_rb.get("transit_lounge") or {}) if ok_rb and isinstance(sc_rb, dict) else {}
                        lfree = int(lg.get("capacity") or 0) - int(lg.get("occupancy") or 0)
                        if lfree >= max(len(aboard), int(pol.get("lounge_min_free_slots") or 2)):
                            ok_f, cur_sys, docked_base, why = _fly_and_dock(gate, pilot, cur_sys, docked_base, home_sys, home_base, graph, pol, data_dir)
                            if ok_f:
                                ok_ul, _, _ = _raw(gate, pilot, "unload_passenger", {"id": "all", "target": "lounge"}, timeout=25)
                                if ok_ul:
                                    layovers += len(aboard)
                                    did_layover = True
                                    time.sleep(10.2)
                if not did_layover:
                    ok_f, cur_sys, docked_base, why = _fly_and_dock(gate, pilot, cur_sys, docked_base, ds, db, graph, pol, data_dir)
                    if ok_f:
                        delivered_trips += 1
                    else:
                        notes.append(why)
                        break
                continue

        if not docked_base:
            break
        ok_b, sc_b, _ = _raw(gate, pilot, "list_station_passengers", {}, timeout=20)
        _denied_b = _denied_bases(data_dir)
        cands = [c for c in score_station_board(docked_base, cur_sys, sc_b if ok_b else {}, berths, graph, pol, avoid=graph["strongholds"]) if c.get("dest_base") not in _denied_b]
        if cands:
            primary = cands[0]
            ok_ld, _, _ = _raw(gate, pilot, "load_passenger", {"id": primary["dest_base"]}, timeout=25)
            time.sleep(10.2)
            rem_b = primary.get("rem_berths") or {}
            if ok_ld and total_berths(rem_b) > 0 and len(cands) > 1 and int(pol.get("max_multi_stops") or 2) >= 2:
                d_from_p1 = bfs_dists(graph["adj"], primary["dest_sys"], avoid=graph["strongholds"], max_hops=12)
                detour_cap = int(pol.get("corridor_detour_max_hops") or 3)
                for extra in cands[1:5]:
                    if d_from_p1.get(extra["dest_sys"], 99) + primary["hops"] <= extra["hops"] + detour_cap:
                        _raw(gate, pilot, "load_passenger", {"id": extra["dest_base"]}, timeout=25)
                        time.sleep(10.2)
                        break
            continue

        boards = _refresh_boards_cache(gate, pilot, data_dir, graph, pol)
        rep = choose_reposition_hub(cur_sys, boards, berths, graph, pol, avoid=graph["strongholds"])
        if rep and rep["base"] != docked_base and time.time() + 180 < deadline:
            ok_f, cur_sys, docked_base, why = _fly_and_dock(gate, pilot, cur_sys, docked_base, rep["system"], rep["base"], graph, pol, data_dir)
            if not ok_f:
                notes.append(why)
                break
            continue
        time.sleep(min(float(pol.get("rest_seconds_when_empty") or 20.0), max(1.0, deadline - time.time())))

    ok_e, sc_e, _ = _raw(gate, pilot, "get_status", {}, timeout=25)
    cr_after = int(((sc_e.get("player") or {}) if ok_e else {}).get("credits") or cr_before)
    mins_run = round((time.time() - t0) / 60.0, 1)
    rec = {
        "route": route_id,
        "kind": "passenger_net",
        "pilot": pilot,
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
        "minutes": mins_run,
        "credits_before": cr_before,
        "credits_after": cr_after,
        "delta": cr_after - cr_before,
        "one_time": 0,
        "delivered_trips": delivered_trips,
        "layovers": layovers,
        "notes": notes[:5],
    }
    _record_run(data_dir, rec)
    print("%s %s passenger_net: done %.1fm delta=%+d cr trips=%d layovers=%d" % (
        utc_now(), pilot, mins_run, cr_after - cr_before, delivered_trips, layovers), flush=True)
    return 0


def _opt(args, flag, default):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print("usage: passenger_net.py <pilot> [--minutes 40] [--route passenger-network] [--policy game/passenger-policy.json] [--data /srv/collective/data]")
        return 0
    pilot = args[0]
    minutes = int(float(_opt(args, "--minutes", "40")))
    route_id = _opt(args, "--route", "passenger-network")
    policy_path = _opt(args, "--policy", str(ROOT / "passenger-policy.json"))
    data_dir = _opt(args, "--data", "/srv/collective/data")
    return run_pilot(pilot, minutes=minutes, route_id=route_id, policy_path=policy_path, data_dir=data_dir)


if __name__ == "__main__":
    sys.exit(main())
