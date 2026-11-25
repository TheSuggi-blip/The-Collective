#!/usr/bin/env python3
"""mine_net.py -- Policy-driven dynamic smart Mining network (`mine-network`).

WHAT:
  One autonomous runner for Mining (Zero/Unity), governed by `game/mine-policy.json`.
  Each miner dynamically discovers unsaturated resource belts (>= min_left_pct, default 15%)
  from `read.db:fields`, matches its exact fitted harvesting tool (`mining_laser_*` -> ore,
  `ice_harvester_*` -> ice, `gas_harvester_*` -> gas), runs global optimal `(pilot, belt)`
  assignment prioritizing (1) open needs (`need_status.gather`, priority <= needs_max_priority) /
  `supply_chains` shortages while hard-skipping full reserves (`routes/pull.json` marks), (2) market
  goods with a bid >= market_min_bid whose bids take more than the fleet holds, valued at that bid,
  and (3) ultra-low-burn XP fallback belts (every other good, within xp_fallback_max_jumps).
  Claims the belt atomically in `data/fleet/mine_claims.json` (<= max_per_belt, auto-scaled
  down on low-headroom belts), delegates execution to `mine.py` with live in-flight floor
  monitoring (`--min-left-pct`), stamps a belt cooldown immediately if the floor is hit,
  and rotates smoothly across the entire 6-hour turn with zero idle ships.

USAGE:
  python3 -I -B game/fleet/mine_net.py <pilot> [--minutes 45] [--policy game/mine-policy.json] [--route mine-network]

Stdlib only. ASCII only.
"""
import fcntl
import json
import os
import re
import signal
import sqlite3
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # game/
REPO = ROOT.parent
DATA = Path(os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data")
DEFAULT_POLICY_PATH = REPO / "game" / "mine-policy.json"

DEFAULT_POLICY = {
    "enabled": True,
    "min_left_pct": 10.0,
    "max_per_belt": 3,
    "units_per_ship_run": 250,
    "cooldown_minutes": 90,
    "claim_ttl_s": 4200,
    "policed_only": True,
    "lawless_min_tier": 1,
    "allow_lawless_for_deficit": True,
    "allow_lawless_systems": [],
    "exclude_systems": [],
    "exclude_pois": [],
    "exclude_resources": [],
    "pirate_avoid_hours": 6.0,
    "max_jumps": 10,
    "max_station_jumps": 4,
    "prioritize_needs": True,
    "skip_full_reserves": True,
    "allow_xp_fallback": True,
    "xp_fallback_max_jumps": 2,
    "deposit_mode": "personal",
    "deposit_stations": [],
    "market_tier": True,
    "market_min_bid": 5.0,
    "needs_max_priority": 2,
    "gift_surplus_to_trader": False,
    "priority_resources": [],
    "rest_seconds_when_empty": 120,
}

ICE_SUFFIXES = ("_ice",)
GAS_SUFFIXES = ("_gas", "_plasma", "_vapor")


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(obj, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def ship_file_name(pilot):
    return (re.sub(r"[^A-Za-z0-9_.-]", "_", str(pilot or ""))[:60] or "pilot") + ".json"


def load_policy(path=None):
    pol = json.loads(json.dumps(DEFAULT_POLICY))
    p = Path(path) if path else DEFAULT_POLICY_PATH
    if not p.is_absolute():
        p = REPO / p
    user = read_json(p, {})
    if isinstance(user, dict):
        for k, v in user.items():
            if not k.startswith("_"):
                pol[k] = v
    return pol


def resource_tool_kind(resource_id):
    rid = str(resource_id or "").strip().lower()
    if rid.endswith(ICE_SUFFIXES):
        return "ice"
    if rid.endswith(GAS_SUFFIXES):
        return "gas"
    return "ore"


def pilot_tools(ship_doc):
    """Return set of tool kinds ('ore', 'ice', 'gas') fitted on the pilot's ship."""
    tools = set()
    mods = ship_doc.get("modules") or []
    for m in mods:
        tid = str((m.get("type") or m.get("type_id") or "") if isinstance(m, dict) else m).lower()
        if "ice_harvester" in tid or "ice_miner" in tid:
            tools.add("ice")
        elif "gas_harvester" in tid or "gas_scoop" in tid or "gas_collector" in tid:
            tools.add("gas")
        elif "mining_laser" in tid or "strip_miner" in tid or "ore_laser" in tid:
            tools.add("ore")
    return tools


def bfs_distances(adj, start_sys, max_hops=18):
    if not start_sys:
        return {}
    dist = {start_sys: 0}
    q = deque([start_sys])
    while q:
        u = q.popleft()
        d = dist[u]
        if d >= max_hops:
            continue
        for v in adj.get(u) or ():
            if v not in dist:
                dist[v] = d + 1
                q.append(v)
    return dist


_CACHE_LOCK = threading.Lock()
_WORLD_CACHE = {}   # (data_dir, repo_root, pol_sig) -> (ts, world)
_STATIC_CACHE = {}  # (repo_root, data_dir) -> (ts, counts)


def _load_pirate_threat_safe(data_dir, hours):
    try:
        import escort_proto as _ep
        return _ep.load_pirate_threat(data_dir, hours=hours)
    except Exception:
        return {}


def _dispatch_pirates(data_dir, now_t):
    """The systems the dispatcher's pirate stop closes now (dispatch.pirates: the sightings record and the members'
    pirate lines, six hours, a heavy pack 24): one reading of danger for the mine routes and mine-network alike
    (requests ENT-534, 2026-11-25: the observations table alone held 4 of the 21 systems the dispatcher closed)."""
    try:
        import dispatch as _dp
        return {str(s) for s in _dp.pirates(Path(data_dir), float(now_t))}
    except Exception as exc:          # a record that cannot be read closes nothing more than the store's own lines
        print("mine_net: the dispatcher's pirate record not read: %s" % exc, file=sys.stderr)
        return set()


def load_graph_and_world(data_dir, repo_root, policy, now_t=None):
    """Load star graph, systems, stations, fields, pirates, reserves, needs, and item values from read.db & TSVs."""
    if now_t is None:
        import worldcache as _wc
        ck = ("mine_world", str(data_dir), str(repo_root), _wc.db_sig(data_dir),
              str(policy.get("pirate_avoid_hours")), bool(policy.get("craft_demand_tier", True)))
        return _wc.cached(ck, 25.0, lambda: _load_graph_and_world_uncached(data_dir, repo_root, policy, time.time()))
    return _load_graph_and_world_uncached(data_dir, repo_root, policy, float(now_t))


def _load_graph_and_world_uncached(data_dir, repo_root, policy, now_t):
    use_cache = False
    db_path = Path(data_dir) / "store" / "read.db"
    adj = {}
    systems = {}
    stations_by_sys = {}
    fields = []
    pirates = set()
    item_vals = {}
    shortages = {}
    full_items = set()
    market_world = None
    held = {}

    if db_path.exists():
        try:
            import worldcache as _wc
            conn = _wc.ro_db(db_path)
        except sqlite3.Error:
            conn = None
        if conn is not None:
            cur = conn.cursor()

            def _read(label, fn):
                # One table's fault (a renamed column) costs that table only, never the fields (2026-11-24: the
                # stations query named columns the store does not have and the fields were never read).
                try:
                    fn()
                except sqlite3.Error as exc:
                    print("mine_net: %s not read: %s" % (label, exc), file=sys.stderr)

            tbls = set()
            _read("tables", lambda: tbls.update(r[0] for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')").fetchall()))

            def _lanes():
                for a, b in cur.execute("SELECT a, b FROM lanes"):
                    adj.setdefault(a, set()).add(b)
                    adj.setdefault(b, set()).add(a)

            def _systems():
                for sid, emp, sh in cur.execute("SELECT id, empire, stronghold FROM systems"):
                    systems[sid] = {"empire": str(emp or "").lower(), "stronghold": bool(sh)}

            def _stations():
                # places: (system, poi, base) of every station; stations: its kind and services by name, where the
                # names match. A station read without storage, or not of kind station, is no place to deposit.
                info = {}
                if "stations" in tbls:
                    for name, kind, services in cur.execute("SELECT name, kind, services FROM stations"):
                        info[str(name or "")] = (str(kind or ""), str(services or ""))
                for sys_id, poi_id, base_id, name in cur.execute(
                        "SELECT system, poi, base, name FROM places WHERE kind = 'station' AND base IS NOT NULL AND base != ''"):
                    kind, services = info.get(str(name or ""), ("station", "storage"))
                    if kind != "station" or "storage" not in services.split(","):
                        continue
                    stations_by_sys.setdefault(sys_id, []).append((sys_id, poi_id, base_id))

            def _fields():
                for sys_id, poi_id, res, rem, mx, rich, ts in cur.execute(
                    "SELECT system, poi, resource, remaining, max_remaining, richness, t FROM fields WHERE remaining > 0"
                ):
                    fields.append({
                        "system": str(sys_id), "poi": str(poi_id), "resource": str(res),
                        "remaining": int(rem or 0), "max_remaining": int(mx or 0),
                        "richness": float(rich or 1.0), "t": float(ts or 0),
                    })

            def _pirates():
                cutoff = now_t - float(policy.get("pirate_avoid_hours") or 6.0) * 3600.0
                for (subj,) in cur.execute("SELECT DISTINCT subject FROM observations WHERE kind = 'pirate' AND t >= ?", (cutoff,)):
                    if subj:
                        pirates.add(str(subj).split(":", 1)[0].strip())     # a subject `system:poi` counts by its system

            def _items():
                # Strict live-market policy (Suggi directive): NEVER seed item_vals from static catalog base_value!
                pass

            def _books():
                cols = {r[1] for r in cur.execute("PRAGMA table_info(books)").fetchall()}
                bcol = "bid" if "bid" in cols else ("best_buy" if "best_buy" in cols else None)
                qcol = "bid_qty" if "bid_qty" in cols else ("best_buy_qty" if "best_buy_qty" in cols else None)
                tcol = "t" if "t" in cols else None
                if bcol:
                    where = "%s > 0" % bcol
                    params = ()
                    if qcol:
                        where += " AND %s > 0" % qcol
                    if tcol:
                        where += " AND %s >= ?" % tcol
                        params = (now_t - 6.0 * 3600.0,)
                    for iid, bid in cur.execute("SELECT item, MAX(%s) FROM books WHERE %s GROUP BY item" % (bcol, where), params):
                        if iid and bid:
                            item_vals[str(iid)] = float(bid)

            def _supply():
                # supply_status carries the stock beside the keep (supply_chains has no stock column).
                for iid, stk, keep in cur.execute("SELECT item, stock, keep FROM supply_status"):
                    iid = str(iid or "")
                    stk, keep = int(stk or 0), int(keep or 0)
                    if iid and keep > 0 and stk < keep:
                        shortages[iid] = max(shortages.get(iid, 0), keep - stk)

            def _market():
                # What a market good sells for: the best bid at market_min_bid or more and the units those bids
                # take, less what the fleet already holds (2026-11-24: copper held 792,590 against 106 units bid).
                min_bid = float(policy.get("market_min_bid") or 5.0)
                for iid, bid, depth in cur.execute(
                        "SELECT item, MAX(bid), SUM(bid_qty) FROM books WHERE bid >= ? GROUP BY item", (min_bid,)):
                    if iid and bid:
                        market[str(iid)] = [float(bid), int(depth or 0)]
                market_read[0] = True

            def _held():
                for iid, units in cur.execute("SELECT item, SUM(units) FROM inventory GROUP BY item"):
                    if iid:
                        held[str(iid)] = int(units or 0)

            def _needs():
                # The open needs' raw shortfalls (need_status.gather: "uranium_ore 2,304, thorium_ore 1,200").
                max_p = int(policy.get("needs_max_priority") or 2)
                for pr, gather in cur.execute("SELECT priority, gather FROM need_status WHERE gather IS NOT NULL"):
                    if int(pr or 9) > max_p:
                        continue
                    for iid, units in re.findall(r"([a-z0-9_]+) ([0-9][0-9,]*)", str(gather or "")):
                        shortages[iid] = max(shortages.get(iid, 0), int(units.replace(",", "")))

            market = {}
            market_read = [False]
            held = {}
            for label, table, fn in (("lanes", "lanes", _lanes), ("systems", "systems", _systems),
                                     ("stations", "places", _stations), ("fields", "fields", _fields),
                                     ("pirates", "observations", _pirates), ("items", "items", _items),
                                     ("books", "books", _books), ("supply", "supply_status", _supply),
                                     ("market", "books", _market), ("held", "inventory", _held),
                                     ("needs", "need_status", _needs)):
                if table in tbls:
                    _read(label, fn)
            conn.close()
            if market_read[0]:
                hv_min = float(policy.get("high_value_market_min_bid") or 0.0)
                hv_cap = int(policy.get("high_value_stock_cap") or 2000)
                for iid, rec in market.items():
                    h_u = held.get(iid, 0)
                    raw_depth = int(rec[1])
                    net_depth = raw_depth - h_u
                    if hv_min > 0 and rec[0] >= hv_min and raw_depth > 0 and h_u < max(hv_cap, raw_depth * 3):
                        rec[1] = max(net_depth, max(hv_cap, raw_depth * 3) - h_u)
                    else:
                        rec[1] = net_depth
                market_world = market

    allow = [str(x) for x in (policy.get("deposit_stations") or []) if str(x).count(":") == 2]
    if allow:
        stations_by_sys = {}
        for spec in allow:
            sys_id, poi_id, base_id = spec.split(":")
            stations_by_sys.setdefault(sys_id, []).append((sys_id, poi_id, base_id))

    # The needs' raw shortfalls come from need_status (_needs above): game/needs.tsv holds refs and units of whole
    # targets (id, project, division, kind, ref, ...), not raw goods short, and its old reading here never matched.

    # Full: every good the reserve's pull marks full (routes/pull.json, rule F36); a market good without a bid that
    # pays and takes more than we hold is no market good either (score_belt_candidates reads world["market"]).
    # A good the pull marks open is gathered up to its max (rule F36: made while short, stopped at max).
    pull = read_json(Path(data_dir) / "routes" / "pull.json", {})
    for iid, rec in ((pull.get("items") or {}) if isinstance(pull, dict) else {}).items():
        if not isinstance(rec, dict):
            continue
        if rec.get("full") and iid not in shortages:
            full_items.add(str(iid))
        elif not rec.get("full"):
            try:
                room = int(rec.get("max") or 0) - int(rec.get("held") or 0)
            except (TypeError, ValueError):
                room = 0
            if room > 0:
                shortages[str(iid)] = max(shortages.get(str(iid), 0), room)

    for extra in policy.get("priority_resources") or []:
        if isinstance(extra, str) and extra.strip():
            shortages.setdefault(extra.strip(), 5000)

    # Load Tier-2 commercial/industrial crafting demand (game/craft-demand.json)
    craft_demand = {}
    if policy.get("craft_demand_tier", True):
        try:
            import craft_net as _cn
            _cw = _cn.load_craft_world(data_dir, repo_root, {"demand_file": str(policy.get("craft_demand_file") or "game/craft-demand.json")})
            craft_demand = _cn.expand_demand_raw_inputs(_cw)
        except Exception:
            craft_demand = {}

    # Auto-discover CLTV Owned Outposts & Faction Lockboxes (0-rent shared storage hubs!)
    lockbox_bases = set()
    owned_outpost_bases = set()
    bursar_bases = set()
    if db_path.exists():
        try:
            import worldcache as _wc_lb
            _lcon = _wc_lb.ro_db(db_path)
            try:
                _ltbls = {r[0] for r in _lcon.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
                if {"faction_facilities", "places"} <= _ltbls:
                    for fsys, fbase, frent in _lcon.execute(
                        "SELECT system, base, COALESCE(rent_per_cycle, 0) FROM faction_facilities WHERE type = 'faction_lockbox' AND COALESCE(status, 'active') = 'active'"
                    ).fetchall():
                        if fbase:
                            lockbox_bases.add(str(fbase))
                            if int(frent or 0) == 0:
                                owned_outpost_bases.add(str(fbase))
                    _owned_rows = []
                    if "bases" in _ltbls:
                        for ob, osys, opoi, okind in _lcon.execute(
                            "SELECT base, system, COALESCE(poi, base), COALESCE(kind, 'outpost') FROM bases WHERE base IS NOT NULL AND system IS NOT NULL"
                        ).fetchall():
                            if ob:
                                _owned_rows.append((str(osys), str(opoi or ob), str(ob), str(okind or "outpost").lower()))
                                if str(okind or "").lower() == "outpost" and str(ob) in lockbox_bases:
                                    owned_outpost_bases.add(str(ob))
                    if policy.get("auto_use_owned_outposts", True):
                        for osys, opoi, ob, _ok in _owned_rows:
                            if ob in lockbox_bases and osys and opoi:
                                tup = (osys, opoi, ob)
                                lst = stations_by_sys.setdefault(tup[0], [])
                                if tup not in lst:
                                    lst.insert(0, tup)
                        for psys, ppoi, pbase in _lcon.execute(
                            "SELECT system, poi, base FROM places WHERE base IS NOT NULL AND base != ''"
                        ).fetchall():
                            if str(pbase) in lockbox_bases and psys and ppoi:
                                tup = (str(psys), str(ppoi), str(pbase))
                                lst = stations_by_sys.setdefault(tup[0], [])
                                if tup not in lst:
                                    # Prioritize 0-rent owned outposts & Lockboxes at front of system's docks
                                    lst.insert(0, tup)
            except sqlite3.Error:
                pass
            finally:
                _lcon.close()
        except Exception:
            pass

    # Allow miners to cross-dock commercial/market ore at live staffed CLTV Bursar hubs
    if policy.get("allow_bursar_dropoffs", False):
        bc = read_json(Path(data_dir) / "fleet" / "bursar_claims.json", {})
        if isinstance(bc, dict):
            for b_id, rec in bc.items():
                if isinstance(rec, dict) and rec.get("system") and rec.get("poi") and rec.get("base"):
                    bsys = str(rec["system"])
                    bemp = str(rec.get("empire") or (systems.get(bsys) or {}).get("empire") or "")
                    if not bemp and not policy.get("allow_lawless_bursar_dropoffs", False):
                        continue
                    bursar_bases.add(str(rec["base"]))
                    tup = (bsys, str(rec["poi"]), str(rec["base"]))
                    lst = stations_by_sys.setdefault(tup[0], [])
                    if tup not in lst:
                        lst.append(tup)

    # Hard Lockbox-Only Guard (Suggi directive): when deposit_mode == "faction", NEVER route miners to a
    # non-Lockbox NPC station (which would error on faction deposit and fall back into private personal storage!).
    if policy.get("deposit_mode") == "faction":
        valid_fac_hubs = set(lockbox_bases) | set(owned_outpost_bases)
        if valid_fac_hubs:
            filt_st = {}
            for _s, _lst in stations_by_sys.items():
                _keep = [t for t in _lst if t[2] in valid_fac_hubs]
                if _keep:
                    filt_st[_s] = _keep
            if filt_st:
                stations_by_sys = filt_st

    pirates |= _dispatch_pirates(data_dir, now_t)
    pirates.discard("")

    _res_world = {
        "adj": adj, "systems": systems, "stations_by_sys": stations_by_sys,
        "fields": fields, "pirates": pirates, "item_vals": item_vals,
        "shortages": shortages, "full_items": full_items, "craft_demand": craft_demand, "market": market_world,
        "held": held, "lockbox_bases": lockbox_bases, "owned_outpost_bases": owned_outpost_bases,
        "bursar_bases": bursar_bases,
        "data_dir": str(data_dir), "allow_escort_request": True,
        "pirate_threat": _load_pirate_threat_safe(data_dir, float(policy.get("pirate_avoid_hours") or 6.0)),
    }
    if use_cache:
        with _CACHE_LOCK:
            _WORLD_CACHE[ck] = (now_t, _res_world)
    return _res_world


def nearest_station(adj, stations_by_sys, belt_sys, max_hops=4):
    """Return (hops, (sys_id, poi_id, base_id)) for closest station to belt_sys, or (None, None)."""
    dists = bfs_distances(adj, belt_sys, max_hops=max_hops)
    best = None
    for sid, hops in sorted(dists.items(), key=lambda kv: (kv[1], kv[0])):
        sts = stations_by_sys.get(sid)
        if sts:
            best = (hops, sts[0])
            break
    return best if best else (None, None)


def _read_claims_unlocked(path, now_t, ttl_s):
    doc = read_json(path, {})
    raw_claims = doc.get("claims") if isinstance(doc, dict) and isinstance(doc.get("claims"), dict) else {}
    raw_cd = doc.get("cooldowns") if isinstance(doc, dict) and isinstance(doc.get("cooldowns"), dict) else {}
    claims = {}
    for p, rec in raw_claims.items():
        if isinstance(rec, dict) and (now_t - float(rec.get("at") or 0)) <= ttl_s and rec.get("belt"):
            claims[str(p)] = rec
    cooldowns = {}
    for belt_key, until_t in raw_cd.items():
        if float(until_t or 0) > now_t:
            cooldowns[str(belt_key)] = float(until_t)
    return claims, cooldowns


def load_claims_state(data_dir, policy, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    ttl_s = float(policy.get("claim_ttl_s") or 4200)
    path = Path(data_dir) / "fleet" / "mine_claims.json"
    return _read_claims_unlocked(path, now_t, ttl_s)


def count_static_mine_orders(repo_root, data_dir, now_t=None, order_fresh_s=1200.0):
    """Count active static `mine <route_id>` ships per belt from data/fleet/orders/*.json."""
    if now_t is None:
        import worldcache as _wc
        return dict(_wc.cached(("mine_static", str(repo_root), str(data_dir)), 15.0,
                               lambda: _count_static_mine_orders_uncached(repo_root, data_dir, time.time(), order_fresh_s)))
    return _count_static_mine_orders_uncached(repo_root, data_dir, float(now_t), order_fresh_s)


def _count_static_mine_orders_uncached(repo_root, data_dir, now_t, order_fresh_s):
    use_cache = False
    odir = Path(data_dir) / "fleet" / "orders"
    rdir = Path(repo_root) / "game" / "routes"
    if not odir.is_dir() or not rdir.is_dir():
        return {}
    route_belt = {}
    counts = {}
    for p in odir.glob("*.json"):
        try:
            if (now_t - p.stat().st_mtime) > order_fresh_s:
                continue
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        what = str(d.get("what") or "").strip()
        parts = what.split(" ", 1)
        if len(parts) != 2 or parts[0] != "mine":
            continue
        rid = parts[1]
        if rid not in route_belt:
            rd = read_json(rdir / ("%s.json" % rid), {})
            route_belt[rid] = str(rd.get("belt") or "") if isinstance(rd, dict) else ""
        bk = route_belt[rid]
        if bk:
            counts[bk] = counts.get(bk, 0) + 1
    if use_cache:
        with _CACHE_LOCK:
            _STATIC_CACHE[sck] = (now_t, dict(counts))
    return counts


def claim_belt_atomic(data_dir, pilot, belt_key, cap, policy, now_t=None, static_counts=None, repo_root=None):
    """Atomically claim belt_key for pilot if (mine_net claims + static mine orders) < cap and not on cooldown."""
    now_t = time.time() if now_t is None else float(now_t)
    ttl_s = float(policy.get("claim_ttl_s") or 4200)
    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_p = fdir / "mine_claims.lock"
    path = fdir / "mine_claims.json"
    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims, cooldowns = _read_claims_unlocked(path, now_t, ttl_s)
            if cooldowns.get(belt_key, 0) > now_t:
                return False
            claims.pop(str(pilot), None)
            st_c = static_counts
            if st_c is None and repo_root is not None:
                st_c = count_static_mine_orders(repo_root, data_dir, now_t=now_t)
            cur_n = sum(1 for rec in claims.values() if rec.get("belt") == belt_key) + int((st_c or {}).get(belt_key, 0))
            if cur_n >= max(1, int(cap)):
                return False
            claims[str(pilot)] = {"belt": belt_key, "at": int(now_t)}
            write_json(path, {"updated_at": int(now_t), "claims": claims, "cooldowns": cooldowns})
            return True
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def release_belt_claim(data_dir, pilot, cooldown_belt=None, cooldown_minutes=90, policy=None, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    ttl_s = float((policy or DEFAULT_POLICY).get("claim_ttl_s") or 4200)
    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_p = fdir / "mine_claims.lock"
    path = fdir / "mine_claims.json"
    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims, cooldowns = _read_claims_unlocked(path, now_t, ttl_s)
            prev = claims.pop(str(pilot), None)
            rel_belt = str((prev or {}).get("belt") or cooldown_belt or "")
            if cooldown_belt and float(cooldown_minutes or 0) > 0:
                cooldowns[str(cooldown_belt)] = now_t + float(cooldown_minutes) * 60.0
            write_json(path, {"updated_at": int(now_t), "claims": claims, "cooldowns": cooldowns})
            rem = sum(1 for rec in claims.values() if isinstance(rec, dict) and str(rec.get("belt") or "") == rel_belt) if rel_belt else 0
            return rem
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def adaptive_belt_cap(remaining, max_remaining, policy):
    """Adaptive crowding cap: <= max_per_belt (default 3), scaled down on low-headroom belts."""
    max_cap = max(1, int(policy.get("max_per_belt") or 3))
    pct = float(policy.get("min_left_pct") or 10.0)
    floor_u = int(round(max_remaining * pct / 100.0)) if max_remaining > 0 else 0
    headroom = max(0, int(remaining) - floor_u)
    per_ship = max(50, int(policy.get("units_per_ship_run") or 250))
    if headroom <= 0:
        return 0
    return min(max_cap, max(1, headroom // per_ship))


def score_belt_candidates(pilot_info, world, policy, claims, cooldowns, now_t=None, static_counts=None):
    """Return sorted list of candidate belt dicts for one pilot (best first)."""
    now_t = time.time() if now_t is None else float(now_t)
    tools = pilot_tools(pilot_info)
    if not tools:
        return []
    p_sys = str(pilot_info.get("system") or "")
    p_tier = int(pilot_info.get("tier") or pilot_info.get("hull_tier") or 0)
    p_name = str(pilot_info.get("name") or "")
    max_jumps = int(policy.get("max_jumps") or 10)
    max_st_jumps = int(policy.get("max_station_jumps") or 4)
    min_pct = float(policy.get("min_left_pct") or 10.0)
    policed_only = bool(policy.get("policed_only", True))
    lawless_min_t = int(policy["lawless_min_tier"]) if policy.get("lawless_min_tier") is not None else 0
    allow_lawless_def = bool(policy.get("allow_lawless_for_deficit", True))
    allow_sys = set(str(x) for x in (policy.get("allow_lawless_systems") or []))
    excl_sys = set(str(x) for x in (policy.get("exclude_systems") or []))
    excl_pois = set(str(x) for x in (policy.get("exclude_pois") or []))
    excl_res = set(str(x) for x in (policy.get("exclude_resources") or []))
    skip_full = bool(policy.get("skip_full_reserves", True))
    allow_xp = bool(policy.get("allow_xp_fallback", True))
    xp_max_j = int(policy.get("xp_fallback_max_jumps") or 2)

    adj = world["adj"]
    systems = world["systems"]
    pirates = world["pirates"]
    shortages = world["shortages"]
    full_items = world["full_items"]
    craft_demand = world.get("craft_demand") or {}
    item_vals = world["item_vals"]
    market = world.get("market")
    stations_by_sys = world["stations_by_sys"]

    dists = bfs_distances(adj, p_sys, max_hops=max_jumps) if p_sys else {}
    claimed_counts = dict(static_counts or {})
    for cp, rec in (claims or {}).items():
        if cp == p_name:
            continue
        bk = rec.get("belt")
        if bk:
            claimed_counts[bk] = claimed_counts.get(bk, 0) + 1

    by_poi = {}
    _deferred_escorts = []
    for f in world["fields"]:
        sys_id = f["system"]
        poi_id = f["poi"]
        belt_key = "%s:%s" % (sys_id, poi_id)
        if sys_id in excl_sys or belt_key in excl_pois or poi_id in excl_pois:
            continue
        _in_pirate_sys = sys_id in pirates
        if cooldowns.get(belt_key, 0) > now_t:
            continue
        smeta = systems.get(sys_id, {})
        if smeta.get("stronghold"):
            continue
        res = f["resource"]
        if res in excl_res:
            continue
        if resource_tool_kind(res) not in tools:
            continue
        rem, mx = f["remaining"], f["max_remaining"]
        if mx > 0 and (rem * 100.0 / mx) < min_pct:
            continue
        cap = adaptive_belt_cap(rem, mx, policy)
        if cap <= 0 or claimed_counts.get(belt_key, 0) >= cap:
            continue
        hops = dists.get(sys_id) if p_sys else 0
        if hops is None or hops > max_jumps:
            continue
        is_policed = bool(smeta.get("empire"))
        is_deficit = bool(policy.get("prioritize_needs", True) and res in shortages)
        is_craft = bool(policy.get("craft_demand_tier", True) and res in craft_demand and not is_deficit)
        is_full = bool(skip_full and res in full_items and not is_deficit and not is_craft)
        mkt = market.get(res) if market is not None else None
        if skip_full and market is not None and not (is_deficit or is_craft or is_full):
            # No bid at market_min_bid or more, or the fleet holds what those bids take: training ore only.
            is_full = not mkt or mkt[1] <= 0
        if _in_pirate_sys:
            _esc_ok = False
            try:
                import escort_proto as _ep
                _esc_dir = world.get("data_dir") or DATA
                if is_deficit and policy.get("request_escort_for_pirate_deficits", True):
                    _pt = (world.get("pirate_threat") or {}).get(sys_id) or {"count": 1, "raiders": 0, "elites": 0}
                    # Never lure unarmed miners into elite warzones (>=1 elite or >=5 raiders)
                    if int(_pt.get("elites") or 0) == 0 and int(_pt.get("raiders") or 0) < 5 and int(_pt.get("count") or 0) <= 4:
                        if _ep.is_field_escorted(_esc_dir, sys_id, poi_id, now_t=now_t):
                            _esc_ok = True
                        elif world.get("allow_escort_request", False):
                            _deferred_escorts.append((hops, sys_id, poi_id, res, is_policed, _pt))
            except Exception:
                _esc_ok = False
            if not _esc_ok:
                continue
        st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=max_st_jumps)
        if not st_tup:
            continue
        hub_rad = int(policy.get("hub_radius_jumps") or 4)
        _st_base_chk = st_tup[2]
        _in_hub_zone = bool(
            st_hops <= hub_rad
            and (_st_base_chk in (world.get("owned_outpost_bases") or set())
                 or _st_base_chk in (world.get("lockbox_bases") or set()))
        )
        bw_min_bid = float(policy.get("buywall_min_bid") or 50.0)
        bw_min_depth = int(policy.get("buywall_min_depth") or 500)
        is_buywall = bool(mkt and mkt[0] >= bw_min_bid and mkt[1] >= bw_min_depth)
        allow_lawless_bw = bool(policy.get("allow_lawless_for_buywall", True))
        if not is_policed:
            lawless_ok = (
                (not policed_only)
                or _in_hub_zone
                or (sys_id in allow_sys)
                or (p_tier >= lawless_min_t)
                or (allow_lawless_def and is_deficit)
                or (allow_lawless_bw and is_buywall and hops <= int(policy.get("buywall_lawless_max_jumps") or 6))
            )
            if not lawless_ok:
                continue
        if is_full and (not allow_xp or (hops > xp_max_j and not _in_hub_zone)):
            continue

        # Strict live-market valuation (ZERO catalog base_value fallback!)
        _live_b = float(mkt[0]) if (mkt and mkt[0] > 0) else float(item_vals.get(res) or 0.0)
        _held_u = int((world.get("held") or {}).get(res, 0))
        _is_glut = (not is_deficit and _held_u >= 20000 and _live_b < 15.0)
        uval = _live_b
        if is_deficit:
            tier = "deficit"
            uval = max(10.0, _live_b)
            tier_mult = 12.0
        elif is_craft and not _is_glut and _live_b >= 15.0:
            tier = "craft_demand"
            tier_mult = 7.0
        elif not is_full and not _is_glut and _live_b > 0:
            tier = "market"
            tier_mult = 9.0 if is_buywall else 3.0
        else:
            if not allow_xp:
                continue
            tier = "xp_fallback"
            uval = max(1.0, _live_b) if _live_b > 0 else 1.0
            _held_u = int((world.get("held") or {}).get(res, 0))
            _bloated = (_held_u >= 25000 and uval < 12.0) or (res in full_items)
            _hard_glut = (_held_u >= int(policy.get("hard_glut_skip_units") or 200000) and uval < 10.0)
            tier_mult = 0.005 if _hard_glut else (0.05 if _bloated else 0.35)
        if tier == "market" and not policy.get("market_tier", True):
            continue

        headroom_bonus = min(2.0, max(0.5, rem / 10000.0))
        fuel_pen = 35.0 * hops + 25.0 * st_hops
        # Zero, 2026-11-25: a longer way always scores lower. Dividing a negative score (fuel above what the good is worth,
        # every experience-only belt) by the way raised it, and a belt 4 jumps from its station outranked one beside a station.
        _num = (tier_mult * uval * 20.0 * headroom_bonus) - fuel_pen
        if policy.get("hub_gravity_bonus", True) and _num > 0:
            _st_base = st_tup[2]
            if _st_base in (world.get("owned_outpost_bases") or set()) or _st_base in (world.get("lockbox_bases") or set()):
                _hub_mult = 1.25 if st_hops == 0 else (1.18 if st_hops <= 2 else (1.10 if st_hops <= hub_rad else 1.0))
                _num *= _hub_mult
        _way = 1.0 + 0.6 * hops + 1.2 * st_hops
        score = _num / _way if _num >= 0 else _num * _way
        cand = {
            "belt_key": belt_key, "system": sys_id, "poi": poi_id,
            "resource": res, "remaining": rem, "max_remaining": mx,
            "cap": cap, "hops": hops, "st_hops": st_hops,
            "station": "%s:%s:%s" % st_tup, "tier": tier, "score": round(score, 2),
        }
        _tr = _TIER_RANK.get(tier, 9)
        prev = by_poi.get(belt_key)
        if prev is None or (_tr, -cand["score"]) < (_TIER_RANK.get(prev["tier"], 9), -prev["score"]):
            by_poi[belt_key] = cand

    ranked = sorted(by_poi.values(), key=lambda c: (_TIER_RANK.get(c["tier"], 9), -c["score"], c["hops"], c["belt_key"]))
    # Request a field escort ONLY when 0 safe pirate-free deficit belts are available for this pilot!
    if _deferred_escorts and not any(c["tier"] == "deficit" for c in ranked):
        try:
            import escort_proto as _ep
            if not hasattr(_ep, "mark_convoy_started"):
                import importlib as _il_m
                _ep = _il_m.reload(_ep)
            _deferred_escorts.sort(key=lambda x: x[0])
            _hops0, _s0, _p0, _r0, _pol0, _pt0 = _deferred_escorts[0]
            _need0 = min(5, max(3, _ep.needed_escorts_for_threat(_pt0.get("count", 1), _pt0.get("raiders", 0), 0, lawless=not _pol0)))
            _ep.request_escort(
                world.get("data_dir") or DATA, "field:%s:%s" % (_s0, _p0), "field", "mine-network",
                "mine-network", _s0, _p0, needed=_need0, threat_systems=[_s0], resource=_r0,
                reason="pirate_sighted_deficit_belt", priority=88, now_t=now_t,
            )
        except Exception:
            pass
    return ranked


_TIER_RANK = {"deficit": 0, "craft_demand": 1, "market": 2, "xp_fallback": 3}


def assign_optimal_mines(pilots_info, world, policy, claims, cooldowns, now_t=None):
    """Global greedy optimal assignment of available miners -> belts (strict tier rank, then score/hops)."""
    now_t = time.time() if now_t is None else float(now_t)
    triples = []
    caps = {}
    used_counts = {}
    for cp, rec in (claims or {}).items():
        bk = rec.get("belt")
        if bk:
            used_counts[bk] = used_counts.get(bk, 0) + 1
    for pinfo in pilots_info:
        pname = str(pinfo.get("name") or "")
        for c in score_belt_candidates(pinfo, world, policy, claims, cooldowns, now_t=now_t)[:25]:
            caps[c["belt_key"]] = c["cap"]
            triples.append((_TIER_RANK.get(c["tier"], 9), -c["score"], c["hops"], pname, c))
    triples.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]["belt_key"]))
    assigned = {}
    for _tr, _nsc, _h, pname, cand in triples:
        if pname in assigned:
            continue
        bk = cand["belt_key"]
        if used_counts.get(bk, 0) >= caps.get(bk, 1):
            continue
        assigned[pname] = cand
        used_counts[bk] = used_counts.get(bk, 0) + 1
    return assigned


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
                if orig_ino is not None and os.stat(order_path).st_ino != orig_ino:
                    return
                os.utime(order_path)
            except OSError:
                return

    t = threading.Thread(target=beat, daemon=True)
    t.start()
    return stop_ev


NO_BELT_NOTE = "no belt matched policy/tools: not reached"


def record_no_belt(data_dir, pilot, route_id, started, now_t=None):
    """One run row for a run that found no belt: the dispatcher rests (route, pilot) after three of them in a row
    (dispatch.stalled_reason, `not reached`), so the ship takes the next route of its list instead of resting here
    unseen (2026-11-24: ships without a belt re-took mine-network every two minutes and wrote no row)."""
    now_t = time.time() if now_t is None else float(now_t)
    row = {"route": route_id, "kind": "mine", "pilot": pilot,
           "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
           "minutes": round(max(0.0, now_t - float(started)) / 60.0, 1), "credits_before": None, "credits_after": None,
           "delta": 0, "one_time": 0, "ore": 0, "sold": {}, "notes": [NO_BELT_NOTE]}
    path = Path(data_dir) / "routes" / "runs.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    return row


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if not args or args[0].startswith("--"):
        sys.exit("usage: mine_net.py <pilot> [--minutes 45] [--policy game/mine-policy.json] [--route mine-network]")
    pilot = args[0]
    minutes = float(_option(args, "--minutes", "45") or 45)
    route_id = _option(args, "--route", "mine-network") or "mine-network"
    policy_arg = _option(args, "--policy", "")

    sys.path.insert(0, str(ROOT / "fleet"))
    import division
    division.require(pilot)

    stop_flag = []

    def _on_sig(signum, _frame):
        stop_flag.append("signal %d" % signum)
        raise SystemExit("signal %d" % signum)

    signal.signal(signal.SIGTERM, _on_sig)
    signal.signal(signal.SIGINT, _on_sig)

    policy = load_policy(policy_arg or None)
    order_path = DATA / "fleet" / "orders" / (pilot + ".json")
    write_json(order_path, {"pilot": pilot, "what": "mine_net " + route_id, "since": utc_now(), "pid": os.getpid()})
    hb = _heartbeat(order_path)
    claimed_belt = None
    floor_hit = False

    try:
        if not policy.get("enabled", True):
            print("RESULT %s: mine_net %s | disabled in policy" % (pilot, route_id), flush=True)
            time.sleep(60)
            return 0
        ship_doc = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
        ship_doc["name"] = pilot
        world = load_graph_and_world(DATA, REPO, policy)
        claims, cooldowns = load_claims_state(DATA, policy)
        static_counts = count_static_mine_orders(REPO, DATA)
        cands = score_belt_candidates(ship_doc, world, policy, claims, cooldowns, static_counts=static_counts)
        chosen = None
        for cand in cands:
            if claim_belt_atomic(DATA, pilot, cand["belt_key"], cand["cap"], policy, static_counts=static_counts, repo_root=REPO):
                chosen = cand
                claimed_belt = cand["belt_key"]
                break
        if not chosen:
            print("%s %s mine_net: no unsaturated belt matched policy/tools; resting %ds" % (utc_now(), pilot, int(policy.get("rest_seconds_when_empty") or 120)), flush=True)
            started = time.time()
            end_nap = started + float(policy.get("rest_seconds_when_empty") or 120)
            while time.time() < end_nap and not (DATA / "fleet" / "STOP").exists() and not stop_flag:
                time.sleep(min(20.0, max(1.0, end_nap - time.time())))
            record_no_belt(DATA, pilot, route_id, started)
            return 0

        print("%s %s mine_net: claimed %s (%s, %s, %dJ->belt, %dJ->%s, score=%.1f)" % (
            utc_now(), pilot, chosen["belt_key"], chosen["resource"], chosen["tier"],
            chosen["hops"], chosen["st_hops"], chosen["station"].split(":")[2], chosen["score"]), flush=True)

        cmd = [
            sys.executable, "-I", "-B", str(ROOT / "fleet" / "mine.py"),
            pilot, chosen["belt_key"], chosen["station"],
            "--minutes", str(int(round(minutes))),
            "--route", route_id,
            "--min-left-pct", str(policy.get("min_left_pct", 10.0)),
            "--floor-resource", chosen["resource"],
            "--no-order",
        ]
        _dest_base = chosen["station"].split(":")[2] if len(chosen["station"].split(":")) >= 3 else ""
        _owned_outposts = world.get("owned_outpost_bases") or set()
        _lockboxes = world.get("lockbox_bases") or set()
        _bursars = world.get("bursar_bases") or set()
        if _dest_base in _owned_outposts or _dest_base in _lockboxes or policy.get("deposit_mode") == "faction":
            cmd += ["--deposit", "faction"]
        elif policy.get("gift_surplus_to_trader") and (chosen["tier"] == "market" or _dest_base in _bursars):
            cmd += ["--gift", json.dumps({"to": "trader", "items": [chosen["resource"]], "source": "both"})]

        import runhost as _rh
        def _on_mine_line(line):
            nonlocal floor_hit
            if "field floor reached:" in line:
                floor_hit = True
        rc_run = _rh.run_in_thread(
            ROOT / "fleet" / "mine.py", cmd[4:], pilot, "mine_net " + route_id,
            env_extra={"FLEET_MEMBER": os.environ.get("FLEET_MEMBER") or "dispatch", "FLEET_HOLD": os.environ.get("FLEET_HOLD") or ("mine_net " + route_id)},
            on_line=_on_mine_line, caller_stdout=sys.stdout, caller_sleep=time.sleep,
        ) or 0
        # Auto-drain trapped legacy personal locker ore at this Lockbox hub into shared Faction Lockbox
        if policy.get("auto_drain_personal_to_lockbox", True) and (_dest_base in _lockboxes or _dest_base in _owned_outposts):
            try:
                import gate as _g_dr, urllib.parse as _up_dr
                def _jraw(_raw_out):
                    if isinstance(_raw_out, dict):
                        return _raw_out
                    if isinstance(_raw_out, str) and _raw_out.strip():
                        try:
                            return json.loads(_raw_out)
                        except ValueError:
                            return {}
                    return {}
                def _jbody(_d):
                    if not isinstance(_d, dict):
                        return {}
                    for _k in ("structuredContent", "result", "data"):
                        if isinstance(_d.get(_k), dict):
                            return _d[_k]
                    _txt_l = _d.get("content")
                    if isinstance(_txt_l, list) and _txt_l and isinstance(_txt_l[0], dict):
                        return _jraw(_txt_l[0].get("text") or "")
                    return _d
                _pe = _up_dr.quote(pilot, safe="")
                _, _gs_r = _g_dr.call("POST", "/accounts/%s/raw" % _pe, {"toolGroup": "spacemolt", "action": "get_status", "params": {}}, timeout=30)
                _gs = _jbody(_jraw(_gs_r))
                _pl = _gs.get("player") if isinstance(_gs.get("player"), dict) else {}
                _sh = _gs.get("ship") if isinstance(_gs.get("ship"), dict) else {}
                _docked_b = str(_pl.get("docked_at_base") or _gs.get("docked_at_base") or _gs.get("base_id") or "")
                _free_c = max(0, int(_sh.get("cargo_capacity") or 0) - int(_sh.get("cargo_used") or 0))
                if _docked_b == _dest_base and _free_c >= 5:
                    _, _vw_r = _g_dr.call("POST", "/accounts/%s/raw" % _pe, {"toolGroup": "spacemolt_storage", "action": "view", "params": {"station_id": _dest_base}}, timeout=30)
                    _sc = _jbody(_jraw(_vw_r))
                    _rows = _sc.get("items") or _sc.get("storage") or []
                    _moved = 0
                    for _it in (_rows if isinstance(_rows, list) else []):
                        if not isinstance(_it, dict) or _moved >= 6:
                            break
                        _iid = str(_it.get("item_id") or "")
                        _iq = int(_it.get("quantity") or 0)
                        if not _iid or _iq <= 0 or _iid in ("fuel_cell", "fuel", "hull_patch", "repair_kit"):
                            continue
                        if _iid.endswith(("_i", "_ii", "_iii", "_iv", "_v")) and any(w in _iid for w in ("laser", "shield", "armor", "scanner", "expander", "booster", "drone", "cannon", "turret", "beam", "railgun", "missile")):
                            continue
                        _tq = min(_iq, _free_c)
                        if _tq < 1:
                            break
                        _, _rw_r = _g_dr.call("POST", "/accounts/%s/raw" % _pe, {"toolGroup": "spacemolt_storage", "action": "withdraw", "params": {"item_id": _iid, "quantity": _tq, "target": "self"}}, timeout=30)
                        _rw = _jraw(_rw_r)
                        if isinstance(_rw, dict) and "error" not in _rw and not _rw.get("isError"):
                            time.sleep(11.0)
                            _, _rd_r = _g_dr.call("POST", "/accounts/%s/raw" % _pe, {"toolGroup": "spacemolt_storage", "action": "deposit", "params": {"item_id": _iid, "quantity": _tq, "target": "faction", "source": "cargo"}}, timeout=30)
                            _rd = _jraw(_rd_r)
                            time.sleep(11.0)
                            if isinstance(_rd, dict) and "error" not in _rd and not _rd.get("isError"):
                                _moved += 1
                                print("%s %s mine_net: drained %d %s personal -> faction lockbox @ %s" % (utc_now(), pilot, _tq, _iid, _dest_base), flush=True)
                            else:
                                _g_dr.call("POST", "/accounts/%s/raw" % _pe, {"toolGroup": "spacemolt_storage", "action": "deposit", "params": {"item_id": _iid, "quantity": _tq, "target": "self", "source": "cargo"}}, timeout=30)
                                break
            except Exception as _de:
                print("%s %s mine_net: drain err: %s" % (utc_now(), pilot, str(_de)[:80]), flush=True)
        return rc_run
    finally:
        hb.set()
        if claimed_belt:
            rem_miners = release_belt_claim(
                DATA, pilot,
                cooldown_belt=(claimed_belt if floor_hit else None),
                cooldown_minutes=float(policy.get("cooldown_minutes") or 90),
                policy=policy,
            )
            if rem_miners == 0:
                try:
                    import escort_proto as _ep
                    _ep.clear_escort_request(DATA, "field:" + str(claimed_belt))
                except Exception:
                    pass
        try:
            cur = read_json(order_path, {})
            if isinstance(cur, dict) and cur.get("pid") == os.getpid() and cur.get("what") == "mine_net " + route_id:
                order_path.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
