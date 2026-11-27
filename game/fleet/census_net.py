#!/usr/bin/env python3
"""census_net.py -- Dynamic whole-map Intelligence AutoNet for 7A Covert Recon & 7B Deep-Core Surveyors.

WHAT:
  Replaces hardcoded static census routes with a live, self-adapting whole-map staleness
  scheduler covering 100% of non-stronghold systems in `read.db:systems` (currently 512/521;
  automatically discovers any new systems added by SpaceMolt patches with zero manual edits).

  Features:
    - Equal whole-map freshness across all 4 galactic quadrants (EN, ES, WN, WS) and all 5 empires.
    - Never-scanned rim systems get immediate top priority until 100% of the map is covered.
    - Wing specialization (manifest wings):
        * 7A. Covert Recon: prioritizes never-scanned frontier/rim systems, rival hub systems
          (arneb, dheneb, lhs_1140, plus any system hosting a player station in read.db:stations),
          and balancing the stalest quadrant.
        * 7B. Deep-Core Surveyors: prioritizes resource-belt & wildlife-herd systems so Miners
          and Military always have <4h fresh scarce-ore (<3%) and Tier-S herd intelligence.
    - Atomic claim deconfliction in `data/fleet/census_claims.json` (1 scout per system).
    - Fuel-safe reachability pre-check via `fuelplan.can_reach_with_refuels` + multi-leg chaining
      via proven `census.py <pilot> <system> --stay --route <route_id>`.
    - Pure stdlib, 7-bit ASCII only.

Usage:
  python3 -I -B game/fleet/census_net.py <pilot> [--minutes 35] [--policy game/census-policy.json] [--route census-network] [--dry-run]
"""

import argparse
import fcntl
import json
import os
import sqlite3
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

FLEET = Path(__file__).resolve().parent
REPO = FLEET.parent.parent
DATA_DEFAULT = Path(os.environ.get("COLLECTIVE_DATA") or "/srv/collective/data")
POLICY_DEFAULT = REPO / "game" / "census-policy.json"

sys.path.insert(0, str(FLEET))
import fuelplan as _fp
import worldcache as _wc

_SURVEY_FLAG_CACHE = {}


def _has_survey_scanner(ship_doc):
    mods = (ship_doc or {}).get("modules") or []
    for m in mods:
        tid = str((m.get("type") or m.get("type_id") or m.get("name") or "") if isinstance(m, dict) else m).lower().replace(" ", "_")
        if "survey_scanner" in tid:
            return True
    return False


DEFAULT_POLICY = {
    "enabled": True,
    "allow_strongholds": False,
    "target_fresh_hours": 4.0,
    "min_rescan_minutes": 45.0,
    "claim_ttl_s": 1800,
    "chain_legs": 3,
    "chain_jumps": 4,
    "quadrant_balance_bonus": 2500.0,
    "never_scanned_bonus": 100000.0,
    "rival_hub_systems": [
        "arneb", "dheneb", "lhs_1140", "zosma", "cloverfield", "beid", "antares", "segin",
    ],
    "exclude_systems": [],
    "rest_seconds_when_empty": 45,
}


def read_json(path, fallback):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return fallback


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")
    os.replace(tmp, p)


def load_policy(policy_path=None):
    p = Path(policy_path) if policy_path else POLICY_DEFAULT
    if not p.is_absolute():
        p = REPO / p
    raw = read_json(p, {})
    pol = dict(DEFAULT_POLICY)
    if isinstance(raw, dict):
        pol.update(raw)
    return pol


def _quadrant(x, y):
    return ("W" if float(x or 0.0) < 0.0 else "E") + ("S" if float(y or 0.0) < 0.0 else "N")


def _pilot_wing(pilot, repo_root=REPO):
    try:
        import upgrades as _upg
        wmap = _upg._load_manifest_wings(str(repo_root))
        return str(wmap.get(pilot) or "")
    except Exception:
        return ""


def _load_census_world(data_dir, policy, now_t=None):
    """Load galaxy graph, system metadata, refuel stations, last-scanned times, fields/herds/rival hubs."""
    now_t = time.time() if now_t is None else float(now_t)
    db_p = Path(data_dir) / "store" / "read.db"
    ck = ("census_world", str(data_dir), _wc.db_sig(data_dir), bool(policy.get("allow_strongholds", False)))

    def _build():
        systems = {}
        adj = {}
        refuel_sys = set()
        field_t = {}
        herd_sys = set()
        rival_station_sys = set()
        battle_sys = set()
        if db_p.is_file():
            con = _wc.ro_db(db_p, timeout=3.0)
            try:
                tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
                if "systems" in tbls:
                    for sid, emp, sh, x, y in con.execute(
                        "SELECT id, COALESCE(empire,''), COALESCE(stronghold,0), COALESCE(x,0), COALESCE(y,0) FROM systems"
                    ).fetchall():
                        s = str(sid or "")
                        if s:
                            systems[s] = {
                                "id": s,
                                "empire": str(emp or ""),
                                "stronghold": int(sh or 0),
                                "quad": _quadrant(x, y),
                            }
                if "lanes" in tbls:
                    for a, b in con.execute("SELECT a, b FROM lanes").fetchall():
                        sa, sb = str(a or ""), str(b or "")
                        if sa and sb:
                            adj.setdefault(sa, set()).add(sb)
                            adj.setdefault(sb, set()).add(sa)
                if "places" in tbls:
                    for s, b in con.execute("SELECT system, base FROM places WHERE base IS NOT NULL AND base != ''").fetchall():
                        if s and b and "_" in str(b):
                            refuel_sys.add(str(s))
                if "bases" in tbls:
                    for (s,) in con.execute("SELECT DISTINCT system FROM bases WHERE system IS NOT NULL AND system != ''").fetchall():
                        if s:
                            refuel_sys.add(str(s))
                if "stations" in tbls:
                    for s, svcs in con.execute("SELECT system, COALESCE(services,'') FROM stations WHERE system IS NOT NULL").fetchall():
                        if s and "refuel" in str(svcs).lower():
                            refuel_sys.add(str(s))
                if "fields" in tbls:
                    for s, mt in con.execute("SELECT system, MAX(COALESCE(t, 0)) FROM fields GROUP BY system").fetchall():
                        if s:
                            field_t[str(s)] = float(mt or 0.0)
                if "herds" in tbls:
                    for (s,) in con.execute("SELECT DISTINCT system FROM herds WHERE system IS NOT NULL").fetchall():
                        if s:
                            herd_sys.add(str(s))
                if "stations" in tbls:
                    for s, tag in con.execute("SELECT system, COALESCE(tag,'') FROM stations WHERE system IS NOT NULL").fetchall():
                        if s and tag and str(tag).upper() != "CLTV":
                            rival_station_sys.add(str(s))
                if "public_battles" in tbls:
                    b_cut = now_t - 14400.0
                    for (s,) in con.execute("SELECT DISTINCT system FROM public_battles WHERE system IS NOT NULL AND t >= ?", (b_cut,)).fetchall():
                        if s:
                            battle_sys.add(str(s))
            finally:
                con.close()
        return {
            "systems": systems,
            "adj": {k: sorted(v) for k, v in adj.items()},
            "refuel_sys": refuel_sys,
            "field_t": field_t,
            "herd_sys": herd_sys,
            "rival_station_sys": rival_station_sys,
            "battle_sys": battle_sys,
        }

    base = _wc.cached(ck, 25.0, _build)
    # Overlay fresh scouting/<sys>.json mtimes & survey_system completion outside cache!
    scout_dir = Path(data_dir) / "scouting"
    last_t = dict(base["field_t"])
    survey_t = {}
    if scout_dir.is_dir():
        try:
            for ent in os.scandir(scout_dir):
                if ent.name.endswith(".json"):
                    sid = ent.name[:-5]
                    st = ent.stat()
                    mt = float(st.st_mtime)
                    if mt > last_t.get(sid, 0.0):
                        last_t[sid] = mt
                    ck_s = (ent.path, mt, st.st_size)
                    has_sv = _SURVEY_FLAG_CACHE.get(ck_s)
                    if has_sv is None:
                        try:
                            txt = Path(ent.path).read_text(encoding="utf-8", errors="ignore")
                            has_sv = ('"survey":' in txt or '"survey" :' in txt)
                        except OSError:
                            has_sv = False
                        if len(_SURVEY_FLAG_CACHE) > 2000:
                            _SURVEY_FLAG_CACHE.clear()
                        _SURVEY_FLAG_CACHE[ck_s] = has_sv
                    if has_sv:
                        survey_t[sid] = mt
        except OSError:
            pass
    out = dict(base)
    out["last_t"] = last_t
    out["survey_t"] = survey_t
    return out


def _bfs_hops(adj, start, avoid=None):
    if not start or start not in adj:
        return {}
    avoid = avoid or set()
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        d = dist[u]
        for v in adj.get(u, ()):
            if v not in dist and v not in avoid:
                dist[v] = d + 1
                q.append(v)
    return dist


def _load_pilot_ship(data_dir, pilot):
    sp = Path(data_dir) / "fleet" / "ships" / ("%s.json" % pilot)
    doc = read_json(sp, None)
    if isinstance(doc, dict) and doc.get("system"):
        return doc
    fl = read_json(Path(data_dir) / "fleet" / "fleet.json", {})
    for s in (fl.get("ships") or []):
        if isinstance(s, dict) and s.get("name") == pilot:
            return s
    return {}


def _busy_order_systems(data_dir):
    busy = set()
    odir = Path(data_dir) / "fleet" / "orders"
    if not odir.is_dir():
        return busy
    try:
        for ent in os.scandir(odir):
            if not ent.name.endswith(".json"):
                continue
            d = read_json(ent.path, {})
            what = str(d.get("what") or "")
            if what.startswith("census "):
                parts = what.split()
                if len(parts) >= 2:
                    busy.add(parts[1])
    except OSError:
        pass
    return busy


def pick_and_claim_target(data_dir, pilot, policy, cur_sys=None, done=None, max_hops=None, now_t=None, dry=False, repo_root=REPO):
    """Atomically choose and claim the highest-value stale/never-scanned system for `pilot`."""
    now_t = time.time() if now_t is None else float(now_t)
    done = set(done or ())
    if not policy.get("enabled", True):
        return None
    world = _load_census_world(data_dir, policy, now_t=now_t)
    systems = world["systems"]
    if not systems:
        return None

    ship_doc = _load_pilot_ship(data_dir, pilot)
    if not cur_sys:
        cur_sys = str(ship_doc.get("system") or "")
    wing = _pilot_wing(pilot, repo_root=repo_root)
    is_recon = wing.startswith("7A.")
    is_surveyor = wing.startswith("7B.")
    has_scanner = _has_survey_scanner(ship_doc)

    allow_sh = bool(policy.get("allow_strongholds", False))
    exclude = set(str(x) for x in (policy.get("exclude_systems") or []))
    strongholds = {sid for sid, meta in systems.items() if meta["stronghold"] and not allow_sh}
    avoid = strongholds | exclude

    adj = world["adj"]
    refuel_sys = world["refuel_sys"] - avoid
    last_t = world["last_t"]
    survey_t = world.get("survey_t") or {}
    rival_hubs = set(str(x) for x in (policy.get("rival_hub_systems") or [])) | world["rival_station_sys"]
    battle_sys = world.get("battle_sys") or set()
    resource_sys = set(world["field_t"].keys()) | world["herd_sys"]

    # Compute 6-hour freshness ratio per quadrant so scouts equalize coverage across EN/ES/WN/WS
    q_tot = {"EN": 0, "ES": 0, "WN": 0, "WS": 0}
    q_fresh = {"EN": 0, "ES": 0, "WN": 0, "WS": 0}
    cut_6h = now_t - 21600.0
    for sid, meta in systems.items():
        if sid in avoid:
            continue
        qd = meta["quad"]
        q_tot[qd] = q_tot.get(qd, 0) + 1
        if last_t.get(sid, 0.0) >= cut_6h:
            q_fresh[qd] = q_fresh.get(qd, 0) + 1
    q_ratio = {qd: (float(q_fresh[qd]) / float(max(1, q_tot[qd]))) for qd in q_tot}
    min_q_ratio = min(q_ratio.values()) if q_ratio else 1.0

    dists = _bfs_hops(adj, cur_sys, avoid=avoid) if cur_sys else {}
    min_rescan_s = float(policy.get("min_rescan_minutes") or 45.0) * 60.0
    target_fresh_h = float(policy.get("target_fresh_hours") or 4.0)
    never_bonus = float(policy.get("never_scanned_bonus") or 100000.0)
    quad_bonus = float(policy.get("quadrant_balance_bonus") or 2500.0)
    ttl_s = float(policy.get("claim_ttl_s") or 1800.0)

    busy_orders = _busy_order_systems(data_dir)
    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    claims_path = fdir / "census_claims.json"
    lock_path = fdir / "census_claims.lock"

    with open(lock_path, "w", encoding="ascii") as lfh:
        fcntl.flock(lfh, fcntl.LOCK_EX)
        try:
            raw = read_json(claims_path, {})
            claims = raw.get("claims") if isinstance(raw, dict) and isinstance(raw.get("claims"), dict) else (raw if isinstance(raw, dict) else {})
            cleaned = {}
            for sid, rec in claims.items():
                if not isinstance(rec, dict):
                    continue
                at_t = float(rec.get("at") or 0.0)
                if (now_t - at_t) < ttl_s and rec.get("pilot") != pilot:
                    cleaned[str(sid)] = rec

            best = None
            for sid, meta in systems.items():
                if sid in avoid or sid in done or sid in cleaned or sid in busy_orders:
                    continue
                hops = dists.get(sid) if cur_sys else 0
                if cur_sys and hops is None:
                    continue
                if max_hops is not None and hops is not None and hops > max_hops:
                    continue
                lt = last_t.get(sid, 0.0)
                age_s = (now_t - lt) if lt > 0.0 else 1e9
                needs_survey = bool(is_surveyor and has_scanner and survey_t.get(sid, 0.0) <= 0.0)
                eff_min_s = float(policy.get("unsurveyed_7b_min_rescan_minutes") or 15.0) * 60.0 if needs_survey else min_rescan_s
                if lt > 0.0 and age_s < eff_min_s:
                    continue

                if lt <= 0.0:
                    base_score = never_bonus
                else:
                    age_h = age_s / 3600.0
                    base_score = (age_h ** 1.35) * 100.0
                    if age_h >= target_fresh_h:
                        base_score += 2000.0

                # Quadrant equalization: reward lagging quadrants (e.g. WN) proportionally
                q_gap = max(0.0, (q_ratio.get(meta["quad"], 1.0) - min_q_ratio))
                if q_gap < 0.05:
                    base_score += quad_bonus * max(0.0, 1.0 - q_ratio.get(meta["quad"], 1.0))

                # Wing specialization:
                #   7A Covert Recon -> rival hubs, active battlefronts, and lawless frontier/rim
                #   7B Deep-Core Surveyors -> unsurveyed systems (hidden Deep-Core uranium/silver POIs!) & resource belts/herds
                if is_recon:
                    if sid in rival_hubs:
                        base_score += 2400.0
                    if sid in battle_sys:
                        base_score += float(policy.get("battlefront_7a_bonus") or 1600.0)
                    if not meta["empire"]:
                        base_score += 1200.0
                elif is_surveyor:
                    if needs_survey:
                        base_score += float(policy.get("unsurveyed_7b_bonus") or 6500.0)
                    if sid in resource_sys or lt <= 0.0:
                        base_score += 1800.0

                eff_hops = max(0, int(hops or 0))
                score = base_score / (1.0 + 0.14 * eff_hops)
                cand = (score, -eff_hops, sid, meta["quad"], lt)
                if best is None or cand > best:
                    best = cand

            if best is None:
                if not dry:
                    write_json(claims_path, {"updated_at": int(now_t), "claims": cleaned})
                return None

            # Verify fuel reachability on chosen candidate (fallback scan if unreachable)
            chosen_sid = best[2]
            if cur_sys and refuel_sys and ship_doc:
                ok_reach = _fp.can_reach_with_refuels(
                    {k: set(v) for k, v in adj.items()}, cur_sys, chosen_sid, {s: True for s in refuel_sys}, ship=ship_doc, avoid=avoid
                )
                if not ok_reach:
                    # Try nearest reachable stale candidate instead
                    fallback = None
                    for sid, meta in systems.items():
                        if sid in avoid or sid in done or sid in cleaned or sid in busy_orders or sid == chosen_sid:
                            continue
                        hops = dists.get(sid)
                        if hops is None or (max_hops is not None and hops > max_hops):
                            continue
                        lt = last_t.get(sid, 0.0)
                        if lt > 0.0 and (now_t - lt) < min_rescan_s:
                            continue
                        if not _fp.can_reach_with_refuels(
                            {k: set(v) for k, v in adj.items()}, cur_sys, sid, {s: True for s in refuel_sys}, ship=ship_doc, avoid=avoid
                        ):
                            continue
                        sc = (never_bonus if lt <= 0.0 else (((now_t - lt) / 3600.0) ** 1.35) * 100.0) / (1.0 + 0.14 * hops)
                        c2 = (sc, -hops, sid, meta["quad"], lt)
                        if fallback is None or c2 > fallback:
                            fallback = c2
                    if fallback is None:
                        return None
                    best = fallback
                    chosen_sid = best[2]

            if not dry:
                cleaned[chosen_sid] = {"pilot": pilot, "at": int(now_t), "wing": wing, "quad": best[3]}
                write_json(claims_path, {"updated_at": int(now_t), "claims": cleaned})
            return {
                "system": chosen_sid,
                "hops": -best[1],
                "quad": best[3],
                "never_scanned": best[4] <= 0.0,
                "age_hours": None if best[4] <= 0.0 else round((now_t - best[4]) / 3600.0, 2),
                "score": round(best[0], 1),
                "wing": wing,
            }
        finally:
            fcntl.flock(lfh, fcntl.LOCK_UN)


def release_claim(data_dir, pilot, system_id=None):
    fdir = Path(data_dir) / "fleet"
    claims_path = fdir / "census_claims.json"
    lock_path = fdir / "census_claims.lock"
    if not claims_path.exists():
        return
    with open(lock_path, "w", encoding="ascii") as lfh:
        fcntl.flock(lfh, fcntl.LOCK_EX)
        try:
            raw = read_json(claims_path, {})
            claims = raw.get("claims") if isinstance(raw, dict) and isinstance(raw.get("claims"), dict) else {}
            changed = False
            for sid in list(claims.keys()):
                rec = claims.get(sid)
                if isinstance(rec, dict) and rec.get("pilot") == pilot and (system_id is None or sid == system_id):
                    claims.pop(sid, None)
                    changed = True
            if changed:
                write_json(claims_path, {"updated_at": int(time.time()), "claims": claims})
        finally:
            fcntl.flock(lfh, fcntl.LOCK_UN)


def has_census_work(data_dir, pilot, policy_path=None):
    pol = load_policy(policy_path)
    if not pol.get("enabled", True):
        return False
    return pick_and_claim_target(data_dir, pilot, pol, dry=True) is not None


def run_pilot(pilot, minutes=35, policy_path=None, route_id="census-network", data_dir=None, dry_run=False):
    data = Path(data_dir) if data_dir else DATA_DEFAULT
    pol = load_policy(policy_path)
    if not pol.get("enabled", True):
        print("census_net: disabled in policy", flush=True)
        return 0
    deadline = time.time() + max(5, int(minutes or 35)) * 60.0
    max_legs = max(1, int(pol.get("chain_legs") or 3))
    chain_j = max(1, int(pol.get("chain_jumps") or 4))
    done = set()
    cur_sys = None
    legs = 0
    try:
        while legs < max_legs and (legs == 0 or (deadline - time.time()) > 420.0):
            hop_lim = None if legs == 0 else chain_j
            pick = pick_and_claim_target(data, pilot, pol, cur_sys=cur_sys, done=done, max_hops=hop_lim, dry=dry_run)
            if not pick and legs > 0:
                # Relax hop limit if no immediate neighbor is stale
                pick = pick_and_claim_target(data, pilot, pol, cur_sys=cur_sys, done=done, max_hops=chain_j * 2, dry=dry_run)
            if not pick:
                if legs == 0:
                    print("RESULT %s: census_net: all reachable systems fresh (0 due)" % pilot, flush=True)
                break
            target_sys = pick["system"]
            print(
                "CENSUS_NET leg %d/%d | %s (%s) -> %s [quad=%s, hops=%d, age=%s]"
                % (legs + 1, max_legs, pilot, pick["wing"] or "Intel", target_sys, pick["quad"],
                   pick["hops"], "NEVER" if pick["never_scanned"] else ("%.1fh" % pick["age_hours"])),
                flush=True,
            )
            if dry_run:
                done.add(target_sys)
                cur_sys = target_sys
                legs += 1
                continue
            cmd = [
                sys.executable, "-I", "-B", str(FLEET / "census.py"),
                pilot, target_sys, "--stay", "--route", str(route_id),
            ]
            env = dict(os.environ)
            env["COLLECTIVE_DATA"] = str(data)
            res = subprocess.run(cmd, env=env, check=False)
            release_claim(data, pilot, target_sys)
            done.add(target_sys)
            cur_sys = str(_load_pilot_ship(data, pilot).get("system") or target_sys)
            legs += 1
            if res.returncode != 0:
                break
        return 0
    finally:
        if not dry_run:
            release_claim(data, pilot)


def main():
    ap = argparse.ArgumentParser(description="Dynamic whole-map Intelligence AutoNet (512/512 non-stronghold systems).")
    ap.add_argument("pilot")
    ap.add_argument("--minutes", type=int, default=35)
    ap.add_argument("--policy", default=str(POLICY_DEFAULT))
    ap.add_argument("--route", default="census-network")
    ap.add_argument("--data", default=str(DATA_DEFAULT))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    return run_pilot(a.pilot, minutes=a.minutes, policy_path=a.policy, route_id=a.route, data_dir=a.data, dry_run=a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
