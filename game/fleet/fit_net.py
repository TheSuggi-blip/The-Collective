#!/usr/bin/env python3
"""Dynamic Multi-Specialty Module Auto-Fitter (`fit-network`, game/fit-policy.json).

WHAT:
  One autonomous fitting runner for all divisions, governed by `game/fit-policy.json`.
  Deterministically resolves each pilot's division + specialty (ore/ice/gas for Mining,
  brawler/ewar/escort for Military, freight/passenger for Logistics, bursar/mobile for Trade,
  recon for Intel), preserving existing specialized tools (`ice_harvester`, `gas_harvester`,
  `passenger_cabin`) and Bursar desk status. Computes exact off-role modules to `unfit` and
  missing/upgradable slot fills available at safe policed stations <= `max_price` within
  `max_jumps`. `dispatch.py` queries `needs_fit()` so already-fitted ships skip `fit-network`
  in 0ms with zero wasted travel.

USAGE:
  python3 -I -B game/fleet/fit_net.py <pilot> [--policy game/fit-policy.json] [--route fit-network]

Stdlib only. ASCII only.
"""
import collections
import fcntl
import json
import os
import re
import signal
import sqlite3
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DATA = Path(os.environ.get("COLLECTIVE_DATA", "/srv/collective/data"))
TICK = 10.5

sys.path.insert(0, str(ROOT / "fleet"))
import gate


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {} if default is None else default


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp.%d" % os.getpid())
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=True), encoding="ascii")
    os.replace(tmp, p)


def ship_file_name(pilot):
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", str(pilot)).strip("_") + ".json"


def _mod_id(m):
    """A fitted module's type id, lower case: the ship files keep modules as dicts ({"type": ...})."""
    if isinstance(m, dict):
        m = m.get("type_id") or m.get("type") or m.get("item_id") or m.get("id") or ""
    return str(m or "").lower()


def _catalog_costs(data_dir):
    """item id -> (cpu, power) from the newest catalog of the data folder (catalog/<version>.json); {} if none."""
    files = [p for p in (Path(data_dir) / "catalog").glob("*.json") if re.fullmatch(r"\d+(\.\d+)*", p.stem)]
    if not files:
        return {}
    raw = read_json(max(files, key=lambda p: tuple(int(n) for n in p.stem.split("."))), {})
    costs = {}
    for it in raw.get("items") or []:
        if isinstance(it, dict) and it.get("id") and (it.get("cpu_usage") is not None or it.get("power_usage") is not None):
            costs[str(it["id"]).lower()] = (int(it.get("cpu_usage") or 0), int(it.get("power_usage") or 0))
    return costs


def _pilot_bucket(pilot):
    m = re.search(r"(\d+)$", str(pilot))
    if m:
        return (int(m.group(1)) * 37) % 100
    h = 0
    for ch in str(pilot):
        h = (h * 31 + ord(ch)) % 100
    return h


def resolve_specialty(pilot, division, fitted_modules, policy, is_bursar=False, ship_class=""):
    """Deterministically resolve ship specialty via pilot pins, hull class, fitted tools, & division mix."""
    if division == "Trade" and is_bursar:
        return "bursar"
    dspec = ((policy.get("specialties") or {}).get(division)) or {}
    pinned = (dspec.get("pin_pilots") or {}).get(str(pilot))
    if pinned:
        return str(pinned)
    is_sent = str(pilot).startswith("sentinel-")
    # For non-sentinel ships, match hull class to specialized role (e.g. Triage -> command_medical)
    cls_l = str(ship_class or "").lower().replace(" ", "_")
    if cls_l and not is_sent:
        for spec_name, hull_list in (dspec.get("detect_by_hull") or {}).items():
            if cls_l in {str(x).lower() for x in (hull_list or [])}:
                return str(spec_name)
    fset = {str(m).lower() for m in (fitted_modules or [])}
    if not is_sent:
        for spec_name, mod_list in (dspec.get("detect_by_module") or {}).items():
            if fset & {str(x).lower() for x in (mod_list or [])}:
                return str(spec_name)
    if is_sent and dspec.get("sentinel_mix"):
        mix = dspec.get("sentinel_mix") or []
    else:
        mix = dspec.get("mix") or []
    if not mix:
        return "default"
    b = _pilot_bucket(pilot)
    cum = 0
    for spec_name, pct in mix:
        cum += int(pct)
        if b < cum:
            return str(spec_name)
    return str(mix[-1][0])


def _bfs(adj, start, max_hops):
    if not start or start not in adj:
        return {start: 0} if start else {}
    dist = {start: 0}
    q = collections.deque([start])
    while q:
        u = q.popleft()
        d = dist[u]
        if d >= max_hops:
            continue
        for v in adj.get(u, ()):
            if v not in dist:
                dist[v] = d + 1
                q.append(v)
    return dist


def load_fit_world(data_dir, policy):
    """Load lanes, safe policed stations, hulls slot counts, and live module asks from read.db."""
    db = Path(data_dir) / "store" / "read.db"
    adj = {}
    stations = {}       # base_id -> (system, poi, base_id, policed)
    hulls = {}          # id_or_name_lower -> {weapon, defense, utility, tier}
    asks = {}           # item_id -> [(ask_price, base_id, qty)]
    item_slots = {}     # item_id_lower -> weapon | defense | utility
    bursar_pilots = set()
    bc = Path(data_dir) / "fleet" / "bursar_claims.json"
    if bc.is_file():
        d = read_json(bc, {})
        for _b, rec in (d.items() if isinstance(d, dict) else []):
            if isinstance(rec, dict) and rec.get("pilot"):
                bursar_pilots.add(str(rec["pilot"]))
    if db.is_file():
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        try:
            tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            if "lanes" in tbls:
                for a, b in con.execute("SELECT a, b FROM lanes"):
                    adj.setdefault(str(a), set()).add(str(b))
                    adj.setdefault(str(b), set()).add(str(a))
            if "places" in tbls and "systems" in tbls:
                for sys_id, poi_id, base_id, emp, sh in con.execute("""
                    SELECT p.system, p.poi, p.base, COALESCE(s.empire, ''), COALESCE(s.stronghold, 0)
                    FROM places p LEFT JOIN systems s ON s.id = p.system
                    WHERE p.base IS NOT NULL AND p.base != ''
                """):
                    stations[str(base_id)] = (str(sys_id), str(poi_id), str(base_id), bool(emp) and not bool(sh))
            if "hulls" in tbls:
                hcols = {r[1] for r in con.execute("PRAGMA table_info(hulls)").fetchall()}
                cp = ", COALESCE(cpu,0), COALESCE(power,0)" if {"cpu", "power"} <= hcols else ", 0, 0"
                for hid, hnm, tr, ws, ds, us, hcpu, hpow in con.execute(
                    "SELECT id, name, COALESCE(tier,0), COALESCE(weapon_slots,0), COALESCE(defense_slots,0), COALESCE(utility_slots,0)%s FROM hulls" % cp
                ):
                    rec = {"tier": int(tr), "weapon": int(ws), "defense": int(ds), "utility": int(us), "cpu": int(hcpu or 0), "power": int(hpow or 0)}
                    if hid:
                        hulls[str(hid).lower()] = rec
                    if hnm:
                        hulls[str(hnm).lower()] = rec
            max_prices = policy.get("max_price") or {}
            wanted = set(str(k) for k in max_prices.keys())
            if "books" in tbls and wanted:
                ph = ",".join("?" * len(wanted))
                for base_id, iid, ask, aqty in con.execute(
                    "SELECT base, item, ask, COALESCE(ask_qty, 1) FROM books WHERE ask > 0 AND item IN (%s)" % ph,
                    tuple(wanted),
                ):
                    mp = float(max_prices.get(str(iid)) or 0)
                    if mp > 0 and float(ask) <= mp and int(aqty or 0) >= 1:
                        asks.setdefault(str(iid), []).append((int(round(float(ask))), str(base_id), int(aqty or 1)))
                for iid in asks:
                    asks[iid].sort()
            if "items" in tbls:
                for iid, sl in con.execute("SELECT id, LOWER(COALESCE(slot, '')) FROM items WHERE slot IS NOT NULL AND slot != ''"):
                    if sl in ("weapon", "defense", "utility"):
                        item_slots[str(iid).lower()] = str(sl)
        finally:
            con.close()
    return {"adj": adj, "stations": stations, "hulls": hulls, "asks": asks, "item_slots": item_slots, "bursar_pilots": bursar_pilots,
            "mod_cost": _catalog_costs(data_dir)}


def _module_slot_type(mod_id, item_slots=None):
    m = str(mod_id or "").lower()
    if item_slots and m in item_slots:
        return item_slots[m]
    if any(k in m for k in ("remote_armor_repair", "repair_arm", "hospital", "sickbay", "ecm_jammer", "jammer", "dampener", "target_painter", "drone_bay", "refueling_pump", "maintenance_bay", "crew_armory", "fuel_optimizer", "cloak", "fuel_tank", "afterburner", "warp_disruptor", "scanner", "harvester", "mining_laser", "cargo_expander", "cabin")):
        return "utility"
    if any(k in m for k in ("pulse_laser", "beam_laser", "autocannon", "railgun", "missile", "torpedo", "turret", "cannon", "flak", "em_disruptor", "emp_", "blood_reaver", "phase_disruptor", "system_disabler")):
        return "weapon"
    if any(k in m for k in ("shield", "armor", "regenerative_armor", "nanite_hull", "hull_plate", "point_defense")):
        return "defense"
    return "utility"


def plan_ship_fit(ship_doc, world, policy):
    """Compute minimal single-stop fit plan `{station, hops, unfit, buy_fit, est_cost, specialty}` or None.

    Returns None when the ship has no off-role modules to strip AND no affordable upgradeable slot
    within `max_jumps`, so `dispatch.py` skips `fit-network` immediately with zero wasted travel.
    """
    if not policy or not policy.get("enabled", True):
        return None
    pilot = str(ship_doc.get("name") or ship_doc.get("pilot") or "")
    division = str(ship_doc.get("division") or "")
    if not pilot or not division:
        return None
    cur_sys = str(ship_doc.get("system") or "")
    credits = int(ship_doc.get("credits") or 0)
    min_keep = int(policy.get("min_wallet_keep_cr") or 10000)
    budget = max(0, credits - min_keep)
    fitted = [i for i in (_mod_id(m) for m in (ship_doc.get("modules") or []) if m) if i]
    cls_key = str(ship_doc.get("class") or ship_doc.get("ship_class") or "").lower()
    hspec = (world.get("hulls") or {}).get(cls_key) or {"tier": 0, "weapon": 1, "defense": 1, "utility": 1}

    is_bursar = pilot in (world.get("bursar_pilots") or set())
    specialty = resolve_specialty(pilot, division, fitted, policy, is_bursar=is_bursar, ship_class=cls_key)

    # 1. Off-role modules to strip
    off_set = {str(x).lower() for x in ((policy.get("off_role_modules") or {}).get(division) or [])}
    to_unfit = sorted({m for m in fitted if m in off_set}) if policy.get("strip_off_role", True) else []

    # 2. Remaining fitted count per slot type after stripping off-role modules
    kept = [m for m in fitted if m not in off_set]
    used_slots = {"weapon": 0, "defense": 0, "utility": 0}
    for m in kept:
        st = _module_slot_type(m, world.get('item_slots'))
        used_slots[st] = used_slots.get(st, 0) + 1

    loadout = (((policy.get("specialties") or {}).get(division) or {}).get("loadouts") or {}).get(specialty) or {}
    wanted_by_slot = {}
    for st in ("weapon", "defense", "utility"):
        free_n = max(0, int(hspec.get(st, 0)) - used_slots.get(st, 0))
        if free_n <= 0:
            continue
        cands = [str(x).lower() for x in (loadout.get(st) or [])]
        if cands:
            wanted_by_slot[st] = (free_n, cands)

    if not to_unfit and not wanted_by_slot:
        return None

    # CPU and power are hard caps of the hull (rules 06-pilots-and-ships.md): what stays fitted plus what is
    # bought must fit, or install_mod refuses after the buy. Judged only where the hull's caps are known.
    mod_cost = world.get("mod_cost") or {}
    cap_cpu, cap_pow = int(hspec.get("cpu") or 0), int(hspec.get("power") or 0)
    judge_caps = cap_cpu > 0 and cap_pow > 0
    kept_cpu = sum(mod_cost.get(m, (0, 0))[0] for m in kept)
    kept_pow = sum(mod_cost.get(m, (0, 0))[1] for m in kept)

    policed_only = bool(policy.get("policed_only", True))
    max_jumps = int(policy.get("max_jumps") or 6)
    dists = _bfs(world.get("adj") or {}, cur_sys, max_jumps)
    stations = world.get("stations") or {}
    asks = world.get("asks") or {}

    # Score candidate safe stations within max_jumps
    best = None
    for b_id, loc in stations.items():
        sys_id, poi_id, base_id, is_pol = loc
        if policed_only and not is_pol:
            continue
        hops = dists.get(sys_id)
        if hops is None:
            continue
        buy_list = []
        spend = 0
        use_cpu, use_pow = kept_cpu, kept_pow
        # For each open slot type, pick the highest-ranked affordable module listed at THIS station
        for st, (free_n, cands) in wanted_by_slot.items():
            filled_here = 0
            for mid in cands:
                if filled_here >= free_n:
                    break
                at_here = [pr for pr, bid, _q in (asks.get(mid) or []) if bid == b_id]
                if not at_here:
                    continue
                pr = at_here[0]
                mc, mp = mod_cost.get(mid, (0, 0))
                if judge_caps and (use_cpu + mc > cap_cpu or use_pow + mp > cap_pow):
                    continue
                if spend + pr <= budget:
                    buy_list.append((mid, pr))
                    spend += pr
                    use_cpu += mc
                    use_pow += mp
                    filled_here += 1
        if not to_unfit and not buy_list:
            continue
        # Score: more upgrades + unfits, fewer jumps, lower cost
        score = len(buy_list) * 100 + len(to_unfit) * 80 - hops * 25 - (spend / 5000.0)
        cand = {
            "station": "%s:%s:%s" % (sys_id, poi_id, base_id),
            "base": base_id,
            "system": sys_id,
            "poi": poi_id,
            "hops": hops,
            "unfit": to_unfit,
            "buy_fit": buy_list,
            "est_cost": spend,
            "specialty": specialty,
            "score": round(score, 2),
        }
        if best is None or cand["score"] > best["score"]:
            best = cand
    return best


def needs_fit(pilot, ship_doc, data_dir=DATA, repo_root=REPO, policy_path=None, world_cache=None):
    """Fast open-gate predicate for dispatch.py: returns fit plan dict if pilot needs fitting now, else None."""
    pol_p = Path(policy_path) if policy_path else (Path(repo_root) / "game" / "fit-policy.json")
    policy = read_json(pol_p, {})
    if not policy or not policy.get("enabled", True):
        return None
    doc = dict(ship_doc or {})
    doc["name"] = pilot
    world = world_cache if world_cache is not None else load_fit_world(data_dir, policy)
    return plan_ship_fit(doc, world, policy)


def _heartbeat(order_path, every=60):
    stop_ev = threading.Event()
    def beat():
        while not stop_ev.wait(every):
            try:
                os.utime(order_path)
            except OSError:
                return
    threading.Thread(target=beat, daemon=True).start()
    return stop_ev


def _option(args, flag, default=""):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if not args or args[0].startswith("--"):
        sys.exit("usage: fit_net.py <pilot> [--policy game/fit-policy.json] [--route fit-network]")
    pilot = args[0]
    route_id = _option(args, "--route", "fit-network") or "fit-network"
    policy_arg = _option(args, "--policy", "")
    pol_p = Path(policy_arg) if policy_arg else (REPO / "game" / "fit-policy.json")
    if not pol_p.is_absolute():
        pol_p = REPO / pol_p
    policy = read_json(pol_p, {})

    import division
    division.require(pilot)

    started = time.time()
    order_path = DATA / "fleet" / "orders" / (pilot + ".json")
    write_json(order_path, {"pilot": pilot, "what": "fit_net " + route_id, "since": utc_now(), "pid": os.getpid()})
    hb = _heartbeat(order_path)
    notes = []
    before = 0

    def raw(action, params=None, group="spacemolt_ship"):
        return gate.raw(pilot, action, params or {}, group=group)

    def get_credits():
        try:
            r = raw("get_status", {}, group="spacemolt")
            return int(((r.get("result") or r).get("player") or {}).get("credits") or 0)
        except Exception:
            return 0

    try:
        before = get_credits()
        ship_doc = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
        ship_doc["name"] = pilot
        if before > 0:
            ship_doc["credits"] = before
        world = load_fit_world(DATA, policy)
        plan = plan_ship_fit(ship_doc, world, policy)
        if not plan:
            notes.append("already fitted")
            return 0

        # Dock at target station
        ans = gate.goal(pilot, "prepare-at-station", {"systemId": plan["system"], "poiId": plan["poi"], "baseId": plan["base"], "refuel": True}, timeout=240)
        if not (isinstance(ans, dict) and ans.get("success", True) and not ans.get("error")):
            notes.append("dock failed at %s" % plan["base"])
            return 0

        # 1. Strip off-role starter modules
        for mid in plan["unfit"]:
            r_un = raw("uninstall_mod", {"module_id": mid}, group="spacemolt_ship")
            time.sleep(TICK)
            if "error" not in r_un:
                raw("deposit", {"item_id": mid, "quantity": 1, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                time.sleep(TICK)
                notes.append("unfit %s" % mid)

        # 2. Buy & fit upgraded modules
        for mid, max_pr in plan["buy_fit"]:
            r_buy = raw("buy", {"item_id": mid, "quantity": 1, "max_price": int(max_pr * 1.02) + 5}, group="spacemolt_market")
            time.sleep(TICK)
            if "error" in r_buy:
                notes.append("buy err %s" % mid)
                continue
            r_ins = raw("install_mod", {"module_id": mid}, group="spacemolt_ship")
            time.sleep(TICK)
            if "error" in r_ins:
                raw("deposit", {"item_id": mid, "quantity": 1, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                time.sleep(TICK)
                notes.append("install err %s" % mid)
            else:
                notes.append("fit %s@%d" % (mid, max_pr))
        return 0
    finally:
        hb.set()
        after = get_credits()
        mins = round((time.time() - started) / 60.0, 1)
        row = {
            "route": route_id, "kind": "fit_net", "pilot": pilot,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "minutes": mins, "credits_before": before, "credits_after": after,
            "delta": after - before if before and after else 0,
            "one_time": 1, "notes": notes[:10],
        }
        runs = DATA / "routes" / "runs.jsonl"
        runs.parent.mkdir(parents=True, exist_ok=True)
        with open(runs, "a", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")
        print("RESULT %s: fit_net %s | %.1f min | credits %d -> %d (%+d cr) | %s"
              % (pilot, route_id, mins, before, after, after - before, "; ".join(notes[:5]) or "ok"), flush=True)
        try:
            cur = read_json(order_path, {})
            if isinstance(cur, dict) and cur.get("pid") == os.getpid() and cur.get("what") == "fit_net " + route_id:
                order_path.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
