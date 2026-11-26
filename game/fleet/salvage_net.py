#!/usr/bin/env python3
"""salvage_net.py -- Policy-driven autonomous Combat Salvage AutoNet for 6C Salvage Tenders.

WHAT:
  Dynamic combat-wreck recovery engine for 6C Combat Salvage Tenders (Outer Rim pilots
  fitted with `salvage_module`, `outer_rim_salvage_array`, or `salvage_drone`, plus
  optional `basic_tow_rig` / `advanced_tow_rig`). Discovers fresh wreck hot-zones from
  active fleet combat claims (`data/fleet/hunt_claims.json`) and recent `public_battles`
  in `read.db`, coordinates claims atomically in `data/fleet/salvage_claims.json`, loots
  and field-scraps wrecks via `spacemolt_salvage` (`wrecks`, `loot`, `scrap_wreck`),
  deposits recovered cargo into Faction Lockboxes (`target="faction"`), logs
  intersegment transfers in `data/stock/handover.jsonl`, and writes `runs.jsonl`.

RULES:
  - DISABLED BY DEFAULT (`game/salvage-policy.json` `"enabled": false`). When disabled,
    `has_salvage_work()` returns False immediately and CLI execution exits 0 cleanly
    without touching the game gate or moving any ship.
  - Policed systems only when `policed_only` is true unless the pilot carries a cloak
    and `allow_lawless_with_cloak` is explicitly enabled.
  - Enforces atomic per-system claim caps (`max_ships_per_system`) and minimum fuel
    reserve (`min_fuel_reserve_pct`) before undocking.
  - Pure stdlib, 7-bit ASCII only.

Usage:
  python3 -I -B game/fleet/salvage_net.py <pilot> [--minutes 35] [--policy game/salvage-policy.json] [--route salvage-network] [--dry-run]
"""

import fcntl
import json
import os
import sqlite3
import sys
import time
import urllib.parse
from collections import deque
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
DATA = Path(os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data")
DEFAULT_POLICY = REPO / "game" / "salvage-policy.json"
CLAIMS_FILE = "salvage_claims.json"

DEFAULT_SALVAGE_TOOLS = ("outer_rim_salvage_array", "salvage_module", "salvage_drone")
DEFAULT_TOW_TOOLS = ("advanced_tow_rig", "basic_tow_rig")


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json_atomic(path, payload):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp.%d" % os.getpid())
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def read_policy(policy_path=None):
    p = Path(policy_path) if policy_path else DEFAULT_POLICY
    if not p.is_absolute():
        p = REPO / p
    raw = read_json(p, {})
    if not isinstance(raw, dict):
        raw = {}
    pol = {
        "enabled": False,
        "wing_prefix": "6C. Combat Salvage",
        "rest_seconds_when_empty": 30,
        "max_ships_per_system": 2,
        "claim_ttl_seconds": 1800,
        "battle_fresh_seconds": 3600,
        "max_jumps": 10,
        "min_fuel_reserve_pct": 25.0,
        "policed_only": True,
        "allow_lawless_with_cloak": False,
        "scrap_mode": "field",
        "tow_enabled": False,
        "deposit_target": "faction",
        "prefer_lockbox_hubs": True,
        "tools": {
            "salvage": list(DEFAULT_SALVAGE_TOOLS),
            "tow": list(DEFAULT_TOW_TOOLS),
        },
    }
    pol.update(raw)
    return pol


def is_enabled(policy):
    return bool(isinstance(policy, dict) and policy.get("enabled", False))


def _module_ids(pilot_state):
    if not isinstance(pilot_state, dict):
        return set()
    mods = set()
    for src in (pilot_state.get("modules"), (pilot_state.get("ship") or {}).get("modules")):
        if not isinstance(src, list):
            continue
        for m in src:
            if isinstance(m, str) and m.strip():
                mods.add(m.strip().lower())
            elif isinstance(m, dict):
                mid = str(m.get("module_id") or m.get("id") or m.get("type_id") or "").strip().lower()
                if mid:
                    mods.add(mid)
    return mods


def pilot_salvage_tools(pilot_state, policy=None):
    """Return {'salvage': [...], 'tow': [...], 'cloak': bool} fitted on pilot_state."""
    pol = policy or read_policy()
    tools = pol.get("tools") or {}
    salv_set = {str(x).lower() for x in (tools.get("salvage") or DEFAULT_SALVAGE_TOOLS)}
    tow_set = {str(x).lower() for x in (tools.get("tow") or DEFAULT_TOW_TOOLS)}
    fitted = _module_ids(pilot_state)
    salv = sorted(m for m in fitted if m in salv_set or "salvage" in m)
    tow = sorted(m for m in fitted if m in tow_set or "tow_rig" in m)
    has_cloak = any("cloak" in m for m in fitted)
    return {"salvage": salv, "tow": tow, "cloak": has_cloak}


def _load_system_meta(data_dir):
    """Return (policed_by_sys, graph_adj) from read.db if present."""
    policed = {}
    adj = {}
    db_path = Path(data_dir) / "store" / "read.db"
    if not db_path.is_file():
        return policed, adj
    conn = None
    try:
        conn = sqlite3.connect("file:%s?mode=ro&immutable=1" % db_path, uri=True, timeout=2.0)
        for row in conn.execute("SELECT id, COALESCE(police_level, 0) FROM systems"):
            sid = str(row[0] or "")
            if sid:
                policed[sid] = int(row[1] or 0) > 0
        for row in conn.execute("SELECT a, b FROM jumps"):
            a, b = str(row[0] or ""), str(row[1] or "")
            if a and b:
                adj.setdefault(a, []).append(b)
                adj.setdefault(b, []).append(a)
    except sqlite3.Error:
        pass
    finally:
        if conn is not None:
            try:
                conn.close()
            except sqlite3.Error:
                pass
    return policed, adj


def bfs_jumps(graph, start_sys, max_hops=12):
    """Return {system_id: hops} within max_hops."""
    if not start_sys:
        return {}
    dist = {start_sys: 0}
    q = deque([(start_sys, 0)])
    while q:
        cur, d = q.popleft()
        if d >= max_hops:
            continue
        for nxt in graph.get(cur) or ():
            if nxt not in dist:
                dist[nxt] = d + 1
                q.append((nxt, d + 1))
    return dist


def discover_salvage_targets(data_dir=None, policy=None, now=None):
    """Aggregate fresh salvage candidate zones from hunt_claims.json and read.db public_battles."""
    d_dir = Path(data_dir or DATA)
    pol = policy or read_policy()
    now_t = float(time.time() if now is None else now)
    fresh_s = float(pol.get("battle_fresh_seconds") or 3600)
    policed_map, _ = _load_system_meta(d_dir)
    by_key = {}

    # 1. Active fleet hunting zones (highest probability of fresh friendly-created wrecks)
    hclaims = read_json(d_dir / "fleet" / "hunt_claims.json", {})
    if isinstance(hclaims, dict):
        for place, entries in hclaims.items():
            if not isinstance(place, str) or ":" not in place:
                continue
            sys_id, poi_id = place.split(":", 1)
            if not sys_id or not poi_id:
                continue
            active_n = 0
            newest = 0.0
            rows = entries.values() if isinstance(entries, dict) else (entries if isinstance(entries, list) else [])
            for rec in rows:
                if isinstance(rec, dict):
                    ts = float(rec.get("at") or rec.get("t") or now_t)
                    if now_t - ts <= fresh_s:
                        active_n += 1
                        newest = max(newest, ts)
                elif isinstance(rec, (int, float)) and now_t - float(rec) <= fresh_s:
                    active_n += 1
                    newest = max(newest, float(rec))
            if active_n <= 0:
                continue
            key = sys_id + ":" + poi_id
            by_key[key] = {
                "system": sys_id,
                "poi": poi_id,
                "source": "hunt_claims",
                "activity": active_n,
                "last_at": newest or now_t,
                "policed": policed_map.get(sys_id, False),
            }

    # 2. Recent public battles in read.db
    db_path = d_dir / "store" / "read.db"
    if db_path.is_file():
        conn = None
        try:
            conn = sqlite3.connect("file:%s?mode=ro&immutable=1" % db_path, uri=True, timeout=2.0)
            has_pb = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='public_battles'").fetchone()
            if has_pb:
                cols = {r[1] for r in conn.execute("PRAGMA table_info(public_battles)")}
                if {"system", "t"} <= cols:
                    cut = now_t - fresh_s
                    poi_col = "poi" if "poi" in cols else "''"
                    for row in conn.execute(
                        "SELECT system, %s, MAX(t), COUNT(*) FROM public_battles WHERE t >= ? GROUP BY system, %s" % (poi_col, poi_col),
                        (cut,),
                    ):
                        sid = str(row[0] or "")
                        pid = str(row[1] or "")
                        ts = float(row[2] or now_t)
                        cnt = int(row[3] or 1)
                        if not sid:
                            continue
                        key = sid + ":" + pid
                        prev = by_key.get(key)
                        if prev:
                            prev["activity"] += cnt
                            prev["last_at"] = max(prev["last_at"], ts)
                        else:
                            by_key[key] = {
                                "system": sid,
                                "poi": pid,
                                "source": "public_battles",
                                "activity": cnt,
                                "last_at": ts,
                                "policed": policed_map.get(sid, False),
                            }
        except sqlite3.Error:
            pass
        finally:
            if conn is not None:
                try:
                    conn.close()
                except sqlite3.Error:
                    pass

    return sorted(by_key.values(), key=lambda x: (-x["activity"], -x["last_at"], x["system"]))


def _prune_claims(claims, ttl, now_t):
    out = {}
    if not isinstance(claims, dict):
        return out
    for sid, cmap in claims.items():
        if not isinstance(cmap, dict):
            continue
        kept = {p: float(ts) for p, ts in cmap.items() if isinstance(ts, (int, float)) and (now_t - float(ts)) <= ttl}
        if kept:
            out[sid] = kept
    return out


def pick_salvage_target(pilot, pilot_state, targets, claims, graph, policy=None, now=None):
    """Choose best valid salvage target respecting policed/cloak, jump limit, fuel, and system cap."""
    pol = policy or read_policy()
    if not is_enabled(pol):
        return None
    tools = pilot_salvage_tools(pilot_state, pol)
    if not tools["salvage"]:
        return None
    now_t = float(time.time() if now is None else now)
    max_jumps = int(pol.get("max_jumps") or 10)
    max_per_sys = max(1, int(pol.get("max_ships_per_system") or 2))
    ttl = float(pol.get("claim_ttl_seconds") or 1800)
    policed_only = bool(pol.get("policed_only", True))
    allow_cloak = bool(pol.get("allow_lawless_with_cloak", False))

    ship = pilot_state.get("ship") or pilot_state
    fuel = float(ship.get("fuel") if ship.get("fuel") is not None else 100.0)
    max_fuel = float(ship.get("max_fuel") or ship.get("fuel_max") or 100.0)
    min_fuel_pct = float(pol.get("min_fuel_reserve_pct") or 25.0)
    if max_fuel > 0 and (100.0 * fuel / max_fuel) < min_fuel_pct:
        return None

    loc = pilot_state.get("location") or {}
    cur_sys = str(pilot_state.get("system") or loc.get("system_id") or loc.get("system") or "")
    dists = bfs_jumps(graph, cur_sys, max_hops=max_jumps) if (cur_sys and graph) else {}
    live_claims = _prune_claims(claims, ttl, now_t)

    best = None
    best_score = -1e18
    for tgt in targets or ():
        sid = str(tgt.get("system") or "")
        if not sid:
            continue
        is_pol = bool(tgt.get("policed", False))
        if policed_only and not is_pol and not (allow_cloak and tools["cloak"]):
            continue
        if cur_sys and graph:
            if sid not in dists:
                continue
            hops = dists[sid]
        else:
            hops = 0 if sid == cur_sys else 1
        if hops > max_jumps:
            continue
        sys_claims = live_claims.get(sid) or {}
        others = sum(1 for p in sys_claims if p != pilot)
        if others >= max_per_sys:
            continue
        age_min = max(0.0, (now_t - float(tgt.get("last_at") or now_t)) / 60.0)
        score = float(tgt.get("activity") or 1) * 100.0 - hops * 20.0 - age_min * 0.5
        if score > best_score:
            best_score = score
            best = dict(tgt, hops=hops, score=round(score, 2))
    return best


def has_salvage_work(pilot_name, pilot_state, data_dir=None, repo_root=None, policy_path=None, now=None):
    """Dispatcher fast gate: False immediately while disabled or no valid salvage target exists."""
    pol = read_policy(policy_path)
    if not is_enabled(pol):
        return False
    d_dir = Path(data_dir or DATA)
    targets = discover_salvage_targets(d_dir, pol, now=now)
    if not targets:
        return False
    _, graph = _load_system_meta(d_dir)
    claims = read_json(d_dir / "fleet" / CLAIMS_FILE, {})
    chosen = pick_salvage_target(pilot_name, pilot_state, targets, claims, graph, pol, now=now)
    return chosen is not None


def claim_system(data_dir, sys_id, pilot, policy, now=None):
    """Atomically claim sys_id in data/fleet/salvage_claims.json; return True on success."""
    now_t = float(time.time() if now is None else now)
    ttl = float(policy.get("claim_ttl_seconds") or 1800)
    cap = max(1, int(policy.get("max_ships_per_system") or 2))
    cpath = Path(data_dir) / "fleet" / CLAIMS_FILE
    cpath.parent.mkdir(parents=True, exist_ok=True)
    lock_path = cpath.with_suffix(".lock")
    with open(lock_path, "a+", encoding="utf-8") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        claims = _prune_claims(read_json(cpath, {}), ttl, now_t)
        sc = claims.setdefault(sys_id, {})
        others = sum(1 for p in sc if p != pilot)
        if others >= cap:
            return False
        sc[pilot] = now_t
        write_json_atomic(cpath, claims)
        return True


def release_claim(data_dir, sys_id, pilot):
    cpath = Path(data_dir) / "fleet" / CLAIMS_FILE
    lock_path = cpath.with_suffix(".lock")
    if not cpath.is_file():
        return
    with open(lock_path, "a+", encoding="utf-8") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        claims = read_json(cpath, {})
        if isinstance(claims, dict) and isinstance(claims.get(sys_id), dict):
            claims[sys_id].pop(pilot, None)
            if not claims[sys_id]:
                claims.pop(sys_id, None)
            write_json_atomic(cpath, claims)


def _opt(args, flag, default=""):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def run_salvage_cycle(pilot, minutes, policy_path, route_id, dry_run=False):
    pol = read_policy(policy_path)
    if not is_enabled(pol):
        print("%s %s salvage_net: disabled in %s (set enabled=true to activate); exiting cleanly" % (utc_now(), pilot, policy_path), flush=True)
        return 0
    import division
    division.require(pilot)
    fleet_doc = read_json(DATA / "fleet" / "fleet.json", {})
    p_state = {}
    for row in (fleet_doc.get("ships") or []):
        if isinstance(row, dict) and row.get("name") == pilot:
            p_state = row
            break
    targets = discover_salvage_targets(DATA, pol)
    _, graph = _load_system_meta(DATA)
    claims = read_json(DATA / "fleet" / CLAIMS_FILE, {})
    chosen = pick_salvage_target(pilot, p_state, targets, claims, graph, pol)
    if not chosen:
        print("%s %s salvage_net: no eligible salvage targets (targets=%d); resting" % (utc_now(), pilot, len(targets)), flush=True)
        return 0
    if dry_run:
        print("DRY-RUN %s salvage_net: would salvage %s:%s (hops=%s, activity=%s, mode=%s)" % (
            pilot, chosen["system"], chosen.get("poi") or "*", chosen.get("hops"), chosen.get("activity"), pol.get("scrap_mode")), flush=True)
        return 0

    if not claim_system(DATA, chosen["system"], pilot, pol):
        print("%s %s salvage_net: claim cap reached for %s" % (utc_now(), pilot, chosen["system"]), flush=True)
        return 0

    import gate
    import handover
    quoted = urllib.parse.quote(pilot, safe="")
    started = time.time()
    recovered = {}
    notes = []
    try:
        acc0 = gate.call("GET", "/accounts/" + quoted)[1]
        cr_before = int(((acc0.get("state") or {}).get("player") or {}).get("credits") or 0)
        # Travel to target system/POI
        gate.call("POST", "/accounts/%s/goal" % quoted, {
            "type": "travel",
            "options": {"system_id": chosen["system"], "poi_id": chosen.get("poi") or ""},
        }, timeout=120)
        deadline = started + max(5.0, float(minutes)) * 60.0
        while time.time() < deadline and not (DATA / "fleet" / "STOP").exists():
            st, ans = gate.call("POST", "/accounts/%s/raw" % quoted, {
                "toolGroup": "spacemolt_salvage",
                "action": "wrecks",
                "params": {},
            }, timeout=30)
            if st not in (200, 201) or not isinstance(ans, dict) or "error" in ans:
                notes.append("wrecks query failed")
                break
            wrecks = (ans.get("result") or ans).get("wrecks") or []
            if not wrecks:
                notes.append("no wrecks at poi")
                break
            for w in wrecks[:5]:
                wid = str(w.get("id") or w.get("wreck_id") or "")
                if not wid:
                    continue
                gate.call("POST", "/accounts/%s/raw" % quoted, {
                    "toolGroup": "spacemolt_salvage",
                    "action": "loot",
                    "params": {"wreck_id": wid},
                }, timeout=30)
                gate.call("POST", "/accounts/%s/raw" % quoted, {
                    "toolGroup": "spacemolt_salvage",
                    "action": "scrap_wreck",
                    "params": {"wreck_id": wid, "mode": str(pol.get("scrap_mode") or "field")},
                }, timeout=30)
                time.sleep(11)
            break

        # Deposit any recovered hold items to Faction Storage at current/nearest docked base
        acc1 = gate.call("GET", "/accounts/" + quoted)[1]
        st1 = acc1.get("state") or {}
        base_id = str(st1.get("docked_at_base") or "")
        cargo_rows = (st1.get("ship") or {}).get("cargo") or []
        dep_target = "faction" if str(pol.get("deposit_target") or "faction") == "faction" else "self"
        if base_id and cargo_rows:
            for item in cargo_rows:
                iid = str(item.get("item_id") or "")
                qty = int(item.get("quantity") or 0)
                if not iid or qty <= 0 or iid.startswith("fuel_"):
                    continue
                st_d, ans_d = gate.call("POST", "/accounts/%s/raw" % quoted, {
                    "toolGroup": "spacemolt_storage",
                    "action": "deposit",
                    "params": {"item_id": iid, "quantity": qty, "target": dep_target, "source": "cargo"},
                }, timeout=30)
                if st_d in (200, 201) and isinstance(ans_d, dict) and "error" not in ans_d:
                    recovered[iid] = recovered.get(iid, 0) + qty
            if recovered and dep_target == "faction":
                handover.record(DATA, {
                    "at": int(time.time()),
                    "base": base_id,
                    "from": pilot,
                    "to": "Faction",
                    "items": recovered,
                    "route": route_id,
                })
        acc2 = gate.call("GET", "/accounts/" + quoted)[1]
        cr_after = int(((acc2.get("state") or {}).get("player") or {}).get("credits") or cr_before)
        row = {
            "route": route_id,
            "kind": "salvage_net",
            "pilot": pilot,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "minutes": round((time.time() - started) / 60.0, 1),
            "credits_before": cr_before,
            "credits_after": cr_after,
            "delta": cr_after - cr_before,
            "one_time": 0,
            "salvaged": recovered,
            "notes": notes,
        }
        runs_p = DATA / "routes" / "runs.jsonl"
        runs_p.parent.mkdir(parents=True, exist_ok=True)
        with open(runs_p, "a", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")
        print("RESULT %s: salvage_net %s | %.1f min | recovered=%d items | credits %d -> %d (%+d) | %s" % (
            pilot, chosen["system"], row["minutes"], sum(recovered.values()), cr_before, cr_after, row["delta"], "; ".join(notes) or "ok"), flush=True)
        return 0
    finally:
        release_claim(DATA, chosen["system"], pilot)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print("usage: salvage_net.py <pilot> [--minutes 35] [--policy game/salvage-policy.json] [--route salvage-network] [--dry-run]")
        return 0
    pilot = args[0]
    minutes = float(_opt(args, "--minutes", "35") or 35)
    policy_path = _opt(args, "--policy", "game/salvage-policy.json")
    route_id = _opt(args, "--route", "salvage-network")
    dry_run = "--dry-run" in args
    return run_salvage_cycle(pilot, minutes, policy_path, route_id, dry_run=dry_run)


if __name__ == "__main__":
    sys.exit(main())
