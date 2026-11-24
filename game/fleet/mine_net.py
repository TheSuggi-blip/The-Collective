#!/usr/bin/env python3
"""mine_net.py -- Policy-driven dynamic smart Mining network (`mine-network`).

WHAT:
  One autonomous runner for Mining (Zero/Unity), governed by `game/mine-policy.json`.
  Each miner dynamically discovers unsaturated resource belts (>= min_left_pct, default 15%)
  from `read.db:fields`, matches its exact fitted harvesting tool (`mining_laser_*` -> ore,
  `ice_harvester_*` -> ice, `gas_harvester_*` -> gas), runs global optimal `(pilot, belt)`
  assignment prioritizing (1) open `needs.tsv` / `supply_chains` shortages while hard-skipping
  full reserves, (2) high-margin market yields, and (3) ultra-low-burn XP fallback belts.
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
    "min_left_pct": 15.0,
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


def load_graph_and_world(data_dir, repo_root, policy, now_t=None):
    """Load star graph, systems, stations, fields, pirates, reserves, needs, and item values from read.db & TSVs."""
    now_t = time.time() if now_t is None else float(now_t)
    db_path = Path(data_dir) / "store" / "read.db"
    adj = {}
    systems = {}
    stations_by_sys = {}
    fields = []
    pirates = set()
    item_vals = {}
    shortages = {}
    full_items = set()

    if db_path.exists():
        try:
            conn = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
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
                        pirates.add(str(subj))

            def _items():
                cols = {r[1] for r in cur.execute("PRAGMA table_info(items)").fetchall()}
                vcol = "base_value" if "base_value" in cols else ("value" if "value" in cols else None)
                if vcol:
                    for iid, val in cur.execute("SELECT id, %s FROM items" % vcol):
                        if iid and val:
                            item_vals[str(iid)] = float(val)

            def _books():
                cols = {r[1] for r in cur.execute("PRAGMA table_info(books)").fetchall()}
                bcol = "bid" if "bid" in cols else ("best_buy" if "best_buy" in cols else None)
                if bcol:
                    for iid, bid in cur.execute("SELECT item, MAX(%s) FROM books WHERE %s > 0 GROUP BY item" % (bcol, bcol)):
                        if iid and bid:
                            item_vals[str(iid)] = max(item_vals.get(str(iid), 0.0), float(bid))

            def _supply():
                # supply_status carries the stock beside the keep (supply_chains has no stock column).
                for iid, stk, keep in cur.execute("SELECT item, stock, keep FROM supply_status"):
                    iid = str(iid or "")
                    stk, keep = int(stk or 0), int(keep or 0)
                    if iid and keep > 0 and stk < keep:
                        shortages[iid] = max(shortages.get(iid, 0), keep - stk)

            for label, table, fn in (("lanes", "lanes", _lanes), ("systems", "systems", _systems),
                                     ("stations", "places", _stations), ("fields", "fields", _fields),
                                     ("pirates", "observations", _pirates), ("items", "items", _items),
                                     ("books", "books", _books), ("supply", "supply_status", _supply)):
                if table in tbls:
                    _read(label, fn)
            conn.close()

    allow = [str(x) for x in (policy.get("deposit_stations") or []) if str(x).count(":") == 2]
    if allow:
        # The Admiral's list of deposit stations (system:poi:base): only where a give route of ours collects.
        stations_by_sys = {}
        for spec in allow:
            sys_id, poi_id, base_id = spec.split(":")
            stations_by_sys.setdefault(sys_id, []).append((sys_id, poi_id, base_id))

    needs_tsv = Path(repo_root) / "game" / "needs.tsv"
    if needs_tsv.exists():
        try:
            for ln in needs_tsv.read_text(encoding="ascii", errors="replace").splitlines()[1:]:
                cols = ln.split("\t")
                if len(cols) >= 5 and cols[0].strip() and not cols[0].startswith("#"):
                    status = cols[4].strip().lower() if len(cols) > 4 else ""
                    if status in ("done", "closed", "cancelled"):
                        continue
                    item = cols[1].strip()
                    need_q = int(float(cols[2] or 0))
                    have_q = int(float(cols[3] or 0))
                    if item and need_q > have_q:
                        shortages[item] = max(shortages.get(item, 0), need_q - have_q)
        except (OSError, ValueError):
            pass

    for extra in policy.get("priority_resources") or []:
        if isinstance(extra, str) and extra.strip():
            shortages.setdefault(extra.strip(), 5000)

    return {
        "adj": adj, "systems": systems, "stations_by_sys": stations_by_sys,
        "fields": fields, "pirates": pirates, "item_vals": item_vals,
        "shortages": shortages, "full_items": full_items,
    }


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
    now_t = time.time() if now_t is None else float(now_t)
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
            claims.pop(str(pilot), None)
            if cooldown_belt and float(cooldown_minutes or 0) > 0:
                cooldowns[str(cooldown_belt)] = now_t + float(cooldown_minutes) * 60.0
            write_json(path, {"updated_at": int(now_t), "claims": claims, "cooldowns": cooldowns})
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def adaptive_belt_cap(remaining, max_remaining, policy):
    """Adaptive crowding cap: <= max_per_belt (default 3), scaled down on low-headroom belts."""
    max_cap = max(1, int(policy.get("max_per_belt") or 3))
    pct = float(policy.get("min_left_pct") or 15.0)
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
    min_pct = float(policy.get("min_left_pct") or 15.0)
    policed_only = bool(policy.get("policed_only", True))
    lawless_min_t = int(policy.get("lawless_min_tier") or 1)
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
    item_vals = world["item_vals"]
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
    for f in world["fields"]:
        sys_id = f["system"]
        poi_id = f["poi"]
        belt_key = "%s:%s" % (sys_id, poi_id)
        if sys_id in excl_sys or sys_id in pirates or belt_key in excl_pois or poi_id in excl_pois:
            continue
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
        is_full = bool(skip_full and res in full_items and not is_deficit)
        if not is_policed:
            lawless_ok = (not policed_only) or (sys_id in allow_sys) or (p_tier >= lawless_min_t) or (allow_lawless_def and is_deficit)
            if not lawless_ok:
                continue
        if is_full and (not allow_xp or hops > xp_max_j):
            continue
        st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=max_st_jumps)
        if not st_tup:
            continue

        uval = max(4.0, float(item_vals.get(res) or 8.0))
        if is_deficit:
            tier = "deficit"
            tier_mult = 12.0
        elif not is_full:
            tier = "market"
            tier_mult = 2.0
        else:
            tier = "xp_fallback"
            tier_mult = 0.25
        if tier == "market" and not policy.get("market_tier", True):
            continue

        headroom_bonus = min(2.0, max(0.5, rem / 10000.0))
        fuel_pen = 35.0 * hops + 25.0 * st_hops
        score = ((tier_mult * uval * 20.0 * headroom_bonus) - fuel_pen) / (1.0 + 0.6 * hops + 1.2 * st_hops)
        cand = {
            "belt_key": belt_key, "system": sys_id, "poi": poi_id,
            "resource": res, "remaining": rem, "max_remaining": mx,
            "cap": cap, "hops": hops, "st_hops": st_hops,
            "station": "%s:%s:%s" % st_tup, "tier": tier, "score": round(score, 2),
        }
        prev = by_poi.get(belt_key)
        if prev is None or cand["score"] > prev["score"]:
            by_poi[belt_key] = cand

    return sorted(by_poi.values(), key=lambda c: (-c["score"], c["hops"], c["belt_key"]))


def assign_optimal_mines(pilots_info, world, policy, claims, cooldowns, now_t=None):
    """Global greedy optimal assignment of available miners -> belts (closest/highest-priority wins)."""
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
            triples.append((c["score"], -c["hops"], pname, c))
    triples.sort(key=lambda x: (-x[0], -x[1], x[2], x[3]["belt_key"]))
    assigned = {}
    for _sc, _nh, pname, cand in triples:
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
            if claim_belt_atomic(DATA, pilot, cand["belt_key"], cand["cap"], policy, repo_root=REPO):
                chosen = cand
                claimed_belt = cand["belt_key"]
                break
        if not chosen:
            print("%s %s mine_net: no unsaturated belt matched policy/tools; resting %ds" % (utc_now(), pilot, int(policy.get("rest_seconds_when_empty") or 120)), flush=True)
            end_nap = time.time() + float(policy.get("rest_seconds_when_empty") or 120)
            while time.time() < end_nap and not (DATA / "fleet" / "STOP").exists() and not stop_flag:
                time.sleep(min(20.0, max(1.0, end_nap - time.time())))
            return 0

        print("%s %s mine_net: claimed %s (%s, %s, %dJ->belt, %dJ->%s, score=%.1f)" % (
            utc_now(), pilot, chosen["belt_key"], chosen["resource"], chosen["tier"],
            chosen["hops"], chosen["st_hops"], chosen["station"].split(":")[2], chosen["score"]), flush=True)

        cmd = [
            sys.executable, "-I", "-B", str(ROOT / "fleet" / "mine.py"),
            pilot, chosen["belt_key"], chosen["station"],
            "--minutes", str(int(round(minutes))),
            "--route", route_id,
            "--min-left-pct", str(policy.get("min_left_pct", 15.0)),
            "--floor-resource", chosen["resource"],
            "--no-order",
        ]
        if policy.get("deposit_mode") == "faction":
            cmd += ["--deposit", "faction"]
        elif policy.get("gift_surplus_to_trader") and chosen["tier"] == "market":
            cmd += ["--gift", json.dumps({"to": "trader", "items": [chosen["resource"]]})]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout or ():
            sys.stdout.write(line)
            sys.stdout.flush()
            if "field floor reached:" in line:
                floor_hit = True
        proc.wait()
        return proc.returncode or 0
    finally:
        hb.set()
        if claimed_belt:
            release_belt_claim(
                DATA, pilot,
                cooldown_belt=(claimed_belt if floor_hit else None),
                cooldown_minutes=float(policy.get("cooldown_minutes") or 90),
                policy=policy,
            )
        try:
            cur = read_json(order_path, {})
            if isinstance(cur, dict) and cur.get("pid") == os.getpid() and cur.get("what") == "mine_net " + route_id:
                order_path.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
