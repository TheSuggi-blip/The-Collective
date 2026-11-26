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



_FIT_MANIFEST_CACHE = {"mtime": -1.0, "by_pilot": {}}


def _manifest_wing_of(pilot):
    p = REPO / "game" / "fleet-500-manifest.tsv"
    if not p.is_file():
        return ""
    try:
        mt = p.stat().st_mtime
    except OSError:
        return ""
    if mt != _FIT_MANIFEST_CACHE["mtime"]:
        by_p = {}
        try:
            with p.open("r", encoding="utf-8", errors="replace") as fh:
                lines = [ln for ln in fh if ln.strip() and not ln.startswith("#")]
            import csv as _csv
            for r in _csv.DictReader(lines, delimiter="\t"):
                pil = str(r.get("pilot") or "").strip()
                if pil:
                    by_p[pil] = str(r.get("wing") or "").strip()
        except OSError:
            pass
        _FIT_MANIFEST_CACHE["mtime"] = mt
        _FIT_MANIFEST_CACHE["by_pilot"] = by_p
    return _FIT_MANIFEST_CACHE["by_pilot"].get(str(pilot), "")


def resolve_specialty(pilot, division, fitted_modules, policy, is_bursar=False, ship_class=""):
    """Deterministically resolve ship specialty via pilot pins, hull class, fitted tools, & division mix."""
    if division == "Trade" and is_bursar:
        return "bursar"
    dspec = ((policy.get("specialties") or {}).get(division)) or {}
    pinned = (dspec.get("pin_pilots") or {}).get(str(pilot))
    if pinned:
        return str(pinned)
    is_sent = str(pilot).startswith(("sentinel-", "GSV "))
    fg_set = set(str(x) for x in (dspec.get("flagship_pilots") or []))
    is_fg = str(pilot) in fg_set
    cls_l = str(ship_class or "").lower().replace(" ", "_")
    if is_fg and cls_l:
        for spec_name, hull_list in (dspec.get("flagship_detect_by_hull") or {}).items():
            if cls_l in {str(x).lower() for x in (hull_list or [])}:
                return str(spec_name)
    wmap = dspec.get("wing_prefix_specialty") or {}
    if wmap and not is_fg:
        wing = _manifest_wing_of(pilot)
        if wing:
            for wp, sp_name in wmap.items():
                if wing.startswith(str(wp)):
                    return str(sp_name)
    if is_sent and cls_l:
        for spec_name, hull_list in (dspec.get("sentinel_detect_by_hull") or {}).items():
            if cls_l in {str(x).lower() for x in (hull_list or [])}:
                return str(spec_name)
    if cls_l and not is_sent and not is_fg:
        for spec_name, hull_list in (dspec.get("detect_by_hull") or {}).items():
            if cls_l in {str(x).lower() for x in (hull_list or [])}:
                return str(spec_name)
    fset = {str(m).lower() for m in (fitted_modules or [])}
    if not is_sent and not is_fg:
        for spec_name, mod_list in (dspec.get("detect_by_module") or {}).items():
            if fset & {str(x).lower() for x in (mod_list or [])}:
                return str(spec_name)
    if is_fg and dspec.get("flagship_mix"):
        mix = dspec.get("flagship_mix") or []
    elif is_sent and dspec.get("sentinel_mix"):
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
    import worldcache as _wc
    mp = (policy or {}).get("max_price") or {}
    mp_sig = tuple(sorted((str(k), int(v)) for k, v in mp.items() if isinstance(v, (int, float))))
    bc_sig = _wc.file_sig(Path(data_dir) / "fleet" / "bursar_claims.json")
    ck = ("fit_world", str(data_dir), _wc.db_sig(data_dir), bc_sig, mp_sig)
    return _wc.cached(ck, 25.0, lambda: _load_fit_world_uncached(data_dir, policy))


def _load_fit_world_uncached(data_dir, policy):
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
        import worldcache as _wc
        con = _wc.ro_db(db, timeout=3.0)
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
    if any(k in m for k in ("remote_armor_repair", "repair_arm", "hospital", "sickbay", "ecm_jammer", "jammer", "dampener", "target_painter", "drone_bay", "refueling_pump", "maintenance_bay", "crew_armory", "fuel_optimizer", "cloak", "fuel_tank", "afterburner", "warp_disruptor", "scanner", "harvester", "mining_laser", "deep_core_extractor", "tracking_computer", "cargo_expander", "cabin")):
        return "utility"
    if any(k in m for k in ("pulse_laser", "beam_laser", "focused_beam", "ion_blaster", "autocannon", "railgun", "missile", "torpedo", "turret", "cannon", "flak", "em_disruptor", "emp_", "neural_disruptor", "blood_reaver", "phase_disruptor", "system_disabler")):
        return "weapon"
    if any(k in m for k in ("shield", "armor", "regenerative_armor", "nanite_hull", "hull_plate", "hull_reinforcement", "point_defense")):
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
    if not division:
        _rm = {"miner": "Mining", "trader": "Trade", "hauler": "Logistics", "drone": "Military", "sentinel": "Military", "scout": "Intel", "command": "Command"}
        division = _rm.get(str(ship_doc.get("role") or "").lower(), "")
    if not pilot or not division:
        return None
    en_divs = policy.get("enabled_divisions")
    if isinstance(en_divs, list) and division not in en_divs:
        return None
    _dspec_en = (policy.get("specialties") or {}).get(division)
    if isinstance(_dspec_en, dict) and _dspec_en.get("enabled") is False:
        return None
    cur_sys = str(ship_doc.get("system") or "")
    credits = int(ship_doc.get("credits") or 0)
    min_keep = int(policy.get("min_wallet_keep_cr") or 10000)
    budget = max(0, credits - min_keep)
    fitted = [i for i in (_mod_id(m) for m in (ship_doc.get("modules") or []) if m) if i]
    cls_key = str(ship_doc.get("class") or ship_doc.get("ship_class") or ship_doc.get("hull") or "").lower()
    hspec = (world.get("hulls") or {}).get(cls_key) or {"tier": 0, "weapon": 1, "defense": 1, "utility": 1}

    is_bursar = pilot in (world.get("bursar_pilots") or set())
    specialty = resolve_specialty(pilot, division, fitted, policy, is_bursar=is_bursar, ship_class=cls_key)

    def _is_primary_harvester(mid_s):
        return any(k in mid_s for k in ("mining_laser", "modulated_mining_laser", "deep_core_extractor", "hyper_mining_laser", "damped_mining_head", "ice_harvester", "gas_harvester", "rad_harvester"))

    # 1. Off-role modules to strip: division-level always safe; specialty-level (`spec_off`) only when
    # a matching primary tool is already kept OR bought at the station (prevents stranding a miner with 0 tools!).
    div_off = {str(x).lower() for x in ((policy.get("off_role_modules") or {}).get(division) or [])}
    spec_off = {str(x).lower() for x in ((((policy.get("specialties") or {}).get(division) or {}).get("off_role_by_specialty") or {}).get(specialty) or [])}
    strip_on = bool(policy.get("strip_off_role", True))
    base_unfit = sorted({m for m in fitted if m in div_off}) if strip_on else []
    spec_unfit_cands = sorted({m for m in fitted if m in spec_off and m not in div_off}) if strip_on else []

    kept_base = [m for m in fitted if m not in div_off]
    kept_without_spec = [m for m in kept_base if m not in spec_off]
    # Self-heal guard: a Mining ship with 0 harvesters and full cargo expanders can swap 1 expander for a harvester
    has_any_harv_base = any(_is_primary_harvester(m) for m in kept_base)
    has_match_harv = any(_is_primary_harvester(m) for m in kept_without_spec)
    heal_expander = None
    if division == "Mining" and not has_any_harv_base:
        budget = max(budget, max(0, credits - 4000))
        exp_fitted = [m for m in kept_base if "cargo_expander" in m]
        if exp_fitted:
            heal_expander = sorted(exp_fitted)[0]

    used_base = {"weapon": 0, "defense": 0, "utility": 0}
    for m in kept_base:
        st = _module_slot_type(m, world.get("item_slots"))
        used_base[st] = used_base.get(st, 0) + 1

    loadout = (((policy.get("specialties") or {}).get(division) or {}).get("loadouts") or {}).get(specialty) or {}
    min_t = int(loadout.get("min_tier") or 0)
    if int(hspec.get("tier") or 0) < min_t:
        return None
    has_any_open = any(max(0, int(hspec.get(st, 0)) - used_base.get(st, 0)) > 0 and (loadout.get(st) or []) for st in ("weapon", "defense", "utility"))
    if not base_unfit and not spec_unfit_cands and not heal_expander and not has_any_open:
        return None

    # CPU and power are hard caps of the hull (rules 06-pilots-and-ships.md): what stays fitted plus what is
    # bought must fit, or install_mod refuses after the buy. Judged only where the hull's caps are known.
    mod_cost = world.get("mod_cost") or {}
    cap_cpu, cap_pow = int(hspec.get("cpu") or 0), int(hspec.get("power") or 0)
    judge_caps = cap_cpu > 0 and cap_pow > 0

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

        # Decide per-station whether specialty swap (`spec_unfit_cands`) or expander self-heal is safe here
        util_cands = [str(x).lower() for x in (loadout.get("utility") or [])]
        harv_avail_here = any(
            _is_primary_harvester(mid) and any(bid == b_id and pr <= budget for pr, bid, _q in (asks.get(mid) or []))
            for mid in util_cands
        )
        station_unfit = list(base_unfit)
        if spec_unfit_cands and (has_match_harv or harv_avail_here):
            station_unfit.extend(spec_unfit_cands)
        elif heal_expander and harv_avail_here and max(0, int(hspec.get("utility", 0)) - used_base.get("utility", 0)) <= 0:
            station_unfit.append(heal_expander)
        station_unfit = sorted(set(station_unfit))
        unfit_set = set(station_unfit)
        kept_here = [m for m in fitted if m not in unfit_set]
        used_here = {"weapon": 0, "defense": 0, "utility": 0}
        for m in kept_here:
            st = _module_slot_type(m, world.get("item_slots"))
            used_here[st] = used_here.get(st, 0) + 1
        use_cpu = sum(mod_cost.get(m, (0, 0))[0] for m in kept_here)
        use_pow = sum(mod_cost.get(m, (0, 0))[1] for m in kept_here)
        have_harv_now = any(_is_primary_harvester(m) for m in kept_here)

        buy_list = []
        spend = 0
        for st in ("weapon", "defense", "utility"):
            free_n = max(0, int(hspec.get(st, 0)) - used_here.get(st, 0))
            cands = [str(x).lower() for x in (loadout.get(st) or [])]
            if free_n <= 0 or not cands:
                continue
            filled_here = 0
            for mid in cands:
                if filled_here >= free_n:
                    break
                # Reserve at least 1 utility slot on Mining hulls for a primary harvester!
                if division == "Mining" and st == "utility" and not have_harv_now and not _is_primary_harvester(mid) and (free_n - filled_here) <= 1:
                    continue
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
                    if _is_primary_harvester(mid):
                        have_harv_now = True
        if not station_unfit and not buy_list:
            continue
        # Score: more upgrades + unfits, fewer jumps, lower cost
        score = len(buy_list) * 100 + len(station_unfit) * 80 - hops * 25 - (spend / 5000.0)
        cand = {
            "station": "%s:%s:%s" % (sys_id, poi_id, base_id),
            "base": base_id,
            "system": sys_id,
            "poi": poi_id,
            "hops": hops,
            "unfit": station_unfit,
            "buy_fit": buy_list,
            "est_cost": spend,
            "specialty": specialty,
            "score": round(score, 2),
        }
        if best is None or cand["score"] > best["score"]:
            best = cand
    return best


def _fit_cooldown_active(pilot, data_dir=DATA):
    cd = read_json(Path(data_dir) / "fleet" / "fit_cooldown.json", {})
    if isinstance(cd, dict):
        until = float(cd.get(str(pilot)) or 0)
        if until > time.time():
            return True
    return False


def _stamp_fit_cooldown(pilot, seconds, data_dir=DATA):
    p = Path(data_dir) / "fleet" / "fit_cooldown.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    lk = Path(data_dir) / "fleet" / "fit_cooldown.lock"
    with open(lk, "a+", encoding="utf-8") as lfh:
        fcntl.flock(lfh, fcntl.LOCK_EX)
        cd = read_json(p, {})
        if not isinstance(cd, dict):
            cd = {}
        now = time.time()
        cd = {k: v for k, v in cd.items() if isinstance(v, (int, float)) and v > now}
        cd[str(pilot)] = round(now + float(seconds), 1)
        write_json(p, cd)


def needs_fit(pilot, ship_doc, data_dir=DATA, repo_root=REPO, policy_path=None, world_cache=None):
    """Fast open-gate predicate for dispatch.py: returns fit plan dict if pilot needs fitting now, else None."""
    pol_p = Path(policy_path) if policy_path else (Path(repo_root) / "game" / "fit-policy.json")
    policy = read_json(pol_p, {})
    if not policy or not policy.get("enabled", True):
        return None
    if _fit_cooldown_active(pilot, data_dir=data_dir):
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

    p_enc = gate.q(pilot)

    def _parse(text):
        try:
            d = json.loads(text) if isinstance(text, str) else text
            return d if isinstance(d, dict) else {}
        except ValueError:
            return {}

    def _body(d):
        if not isinstance(d, dict):
            return {}
        for k in ("structuredContent", "result", "data"):
            if isinstance(d.get(k), dict):
                return d[k]
        return d

    def raw(action, params=None, group="spacemolt"):
        st, txt = gate.call("POST", "/accounts/%s/raw" % p_enc, {"toolGroup": group, "action": action, "params": params or {}}, timeout=120)
        d = _parse(txt)
        if st >= 400 and "error" not in d:
            d["error"] = "http %d" % st
        return d

    def goal(kind, options, timeout=240):
        st, txt = gate.call("POST", "/accounts/%s/goal" % p_enc, {"type": kind, "options": options}, timeout=timeout)
        d = _parse(txt)
        ok = (200 <= st < 300) and bool(d.get("success", True)) and not d.get("error")
        return ok, d

    def get_status_body():
        try:
            return _body(raw("get_status", {}, group="spacemolt"))
        except Exception:
            return {}

    def get_credits():
        try:
            return int((get_status_body().get("player") or {}).get("credits") or 0)
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

        print("%s %s fit_net: flying to %s (%dJ, unfit=%d, buy=%d, spec=%s)" % (
            utc_now(), pilot, plan["base"], plan["hops"], len(plan["unfit"]), len(plan["buy_fit"]), plan["specialty"]), flush=True)
        ok_d, _ans = goal("prepare-at-station", {"systemId": plan["system"], "poiId": plan["poi"], "baseId": plan["base"], "refuel": True}, timeout=240)
        if not ok_d:
            notes.append("dock failed at %s" % plan["base"])
            _stamp_fit_cooldown(pilot, 1200, data_dir=DATA)
            return 0

        for mid in plan["unfit"]:
            st_b = _body(raw("get_ship", {}, group="spacemolt"))
            live_mods = st_b.get("modules") or (st_b.get("ship") or {}).get("modules") or []
            inst_id = mid
            for lm in live_mods:
                if isinstance(lm, dict) and str(lm.get("type_id") or lm.get("type") or "").lower() == str(mid).lower():
                    inst_id = lm.get("module_id") or lm.get("id") or mid
                    break
            r_un = raw("uninstall_mod", {"module_id": inst_id}, group="spacemolt")
            time.sleep(TICK)
            if "error" not in r_un:
                raw("deposit", {"item_id": mid, "quantity": 1, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                time.sleep(TICK)
                notes.append("unfit %s" % mid)

        total_spent = [0]
        for mid, max_pr in plan["buy_fit"]:
            cr_before = get_credits()
            ok_b, _rb = goal("buy-items", {"items": [{"itemId": mid, "maxPrice": int(max_pr * 1.02) + 5, "maxQuantity": 1}]}, timeout=120)
            time.sleep(TICK)
            if not ok_b:
                notes.append("buy err %s" % mid)
                continue
            st_after = get_status_body()
            cargo_rows = (st_after.get("ship") or {}).get("cargo") or st_after.get("cargo") or []
            have_mid = any(
                isinstance(c, dict) and str(c.get("item_id") or c.get("item") or "").lower() == str(mid).lower() and int(c.get("quantity") or 0) >= 1
                for c in cargo_rows
            )
            cr_after = int((st_after.get("player") or {}).get("credits") or 0)
            if not have_mid:
                notes.append("sold out %s" % mid)
                continue
            try:
                spent = max(0, cr_before - cr_after) if cr_before > 0 and cr_after >= 0 else int(max_pr)
                if spent > 0:
                    total_spent[0] += int(spent)
                    import gate as _gate_mod
                    _gate_mod.book_onetime(pilot, "fit_net %s" % mid, -int(spent), data=str(DATA))
            except Exception:
                pass
            r_ins = raw("install_mod", {"module_id": mid}, group="spacemolt")
            time.sleep(TICK)
            if "error" in r_ins:
                raw("deposit", {"item_id": mid, "quantity": 1, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                time.sleep(TICK)
                notes.append("install err %s" % mid)
            else:
                notes.append("fit %s@%d" % (mid, max_pr))
        had_err = any(n.startswith(("buy err", "install err", "dock failed", "sold out")) for n in notes)
        _stamp_fit_cooldown(pilot, 1200 if had_err else 300, data_dir=DATA)
        return 0
    finally:
        hb.set()
        after = get_credits()
        mins = round((time.time() - started) / 60.0, 1)
        ot_val = -int(total_spent[0]) if "total_spent" in locals() and total_spent[0] > 0 else 0
        row = {
            "route": route_id, "kind": "fit_net", "pilot": pilot,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "minutes": mins, "credits_before": before, "credits_after": after,
            "delta": after - before if before and after else 0,
            "one_time": ot_val, "notes": notes[:10],
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
