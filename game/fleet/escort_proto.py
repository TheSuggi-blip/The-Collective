#!/usr/bin/env python3
"""escort_proto.py -- unified proactive Convoy & Field Escort Pack protocol (haul.py + mine_net.py <-> hunt_net.py).

WHAT:
  Shared flock-locked coordination layer over `data/fleet/escort_requests.json`:
    - `haul.py` checks EVERY hop of a job's BFS path. Strongholds are hard-blocked.
      Lawless/pirate corridors (including neutral/friend player contracts -- zero blind trust)
      require fresh census, high economic/strategic floor, and a 3/5/7/10-ship Military Convoy
      Escort Pack before leaving dock.
    - `mine_net.py` requests a 3/5/7/10-ship Field Escort Pack when a Priority-1 deficit belt
      (non-stronghold) is dodged strictly due to recent pirate sightings; once secured, the
      belt unlocks for Mining until drained or cleared.
    - `hunt_net.py` Lane 1 pulls the nearest 3/5/7/10 combat-ready Military ships (preferring
      Command Flagships and Royal Guard Sentinels) to rally and guard/follow the convoy or field,
      releasing instantly back to hunting when the request clears (0 ships held when space is clear).

Usage:
  Imported as a shared library by haul.py, mine_net.py, and hunt_net.py (no standalone CLI).

Stdlib only. Pure 7-bit ASCII.
"""

import collections
import fcntl
import json
import os
import sqlite3
import time
from pathlib import Path

DEFAULT_TTL_S = 1800
MAX_FIELD_REQUESTS = 2
MAX_CONVOY_REQUESTS = 4


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return default


def _write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp.%d" % os.getpid())
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="ascii")
    os.replace(tmp, p)


def bfs_path(adj, src, dst, max_hops=45):
    """Return full shortest system path [src, ..., dst] or None if unreachable within max_hops."""
    if not src or not dst:
        return None
    if src == dst:
        return [src]
    parent = {src: None}
    depth = {src: 0}
    q = collections.deque([src])
    while q:
        cur = q.popleft()
        d = depth[cur]
        if d >= max_hops:
            continue
        for nxt in adj.get(cur) or ():
            if nxt in parent:
                continue
            parent[nxt] = cur
            depth[nxt] = d + 1
            if nxt == dst:
                path = [dst]
                node = cur
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return path
            q.append(nxt)
    return None


def load_pirate_threat(data_dir, hours=6.0, now_t=None):
    """Return {system_id: {'count': int, 'raiders': int, 'elites': int, 'last_t': float}} from read.db observations."""
    now_t = time.time() if now_t is None else float(now_t)
    cutoff = now_t - float(hours or 6.0) * 3600.0
    db = Path(data_dir) / "store" / "read.db"
    out = {}
    if not db.is_file():
        return out
    con = None
    try:
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
        if "observations" in tbls:
            for subj, note, t in con.execute(
                "SELECT subject, COALESCE(note, ''), COALESCE(t, 0) FROM observations WHERE kind = 'pirate' AND t >= ?",
                (cutoff,),
            ):
                if not subj:
                    continue
                sys_id = str(subj).split(":", 1)[0].strip()
                if not sys_id:
                    continue
                rec = out.setdefault(sys_id, {"count": 0, "raiders": 0, "elites": 0, "last_t": 0.0})
                rec["count"] += 1
                low = str(note or "").lower()
                if "elite" in low or "boss" in low or "dread" in low or "warlord" in low:
                    rec["elites"] += 1
                elif "raider" in low or "cruiser" in low or "frigate" in low:
                    rec["raiders"] += 1
                if float(t or 0) > rec["last_t"]:
                    rec["last_t"] = float(t or 0)
    except sqlite3.Error:
        pass
    finally:
        if con is not None:
            con.close()
    return out


def load_recent_raids(data_dir, hours=24.0, now_t=None):
    """Return set of system_ids with recent raid observations."""
    now_t = time.time() if now_t is None else float(now_t)
    cutoff = now_t - float(hours or 24.0) * 3600.0
    db = Path(data_dir) / "store" / "read.db"
    raids = set()
    if not db.is_file():
        return raids
    con = None
    try:
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
        if "observations" in tbls:
            for (subj,) in con.execute(
                "SELECT DISTINCT subject FROM observations WHERE kind = 'raid' AND t >= ?", (cutoff,)
            ):
                if subj:
                    raids.add(str(subj).split(":", 1)[0].strip())
    except sqlite3.Error:
        pass
    finally:
        if con is not None:
            con.close()
    return raids


def needed_escorts_for_threat(pirate_count=0, raiders=0, elites=0, lawless=False):
    """Scale convoy/field escort pack size cleanly across [3, 5, 7, 10] based on observed threat."""
    if elites >= 1 or pirate_count >= 8 or raiders >= 6:
        return 10
    if pirate_count >= 5 or raiders >= 4:
        return 7
    if pirate_count >= 2 or raiders >= 2:
        return 5
    if pirate_count >= 1 or lawless:
        return 3
    return 0


def assess_path_threat(path, systems_meta, strongholds, pirate_threat, raid_systems=None):
    """Inspect every hop of `path`. Returns dict: stronghold_hit, lawless_hops, pirate_hops, raid_hit, needed."""
    raids = raid_systems or set()
    sh = strongholds or set()
    lawless_hops = []
    pirate_hops = []
    max_p, max_r, max_e = 0, 0, 0
    sh_hit = False
    raid_hit = False
    for sys_id in path or ():
        smeta = (systems_meta or {}).get(sys_id) or {}
        if sys_id in sh or smeta.get("stronghold"):
            sh_hit = True
        if sys_id in raids:
            raid_hit = True
        if not smeta.get("empire"):
            lawless_hops.append(sys_id)
        pt = (pirate_threat or {}).get(sys_id)
        if pt and int(pt.get("count") or 0) > 0:
            pirate_hops.append(sys_id)
            max_p = max(max_p, int(pt.get("count") or 0))
            max_r = max(max_r, int(pt.get("raiders") or 0))
            max_e = max(max_e, int(pt.get("elites") or 0))
    needed = 0 if sh_hit else needed_escorts_for_threat(max_p, max_r, max_e, lawless=bool(lawless_hops))
    return {
        "stronghold_hit": sh_hit,
        "raid_hit": raid_hit,
        "lawless_hops": lawless_hops,
        "pirate_hops": pirate_hops,
        "needed": needed,
    }


def _clean_requests_unlocked(doc, now_t):
    raw_reqs = doc.get("requests") if isinstance(doc, dict) and isinstance(doc.get("requests"), dict) else {}
    out = {}
    for k, rec in raw_reqs.items():
        if not isinstance(rec, dict) or not rec.get("active", True):
            continue
        exp = float(rec.get("expires_at") or 0)
        if exp > 0 and exp <= now_t:
            continue
        esc = rec.get("escorts") if isinstance(rec.get("escorts"), dict) else {}
        live_esc = {p: v for p, v in esc.items() if isinstance(v, dict) and (now_t - float(v.get("at") or 0)) < 3600}
        rec = dict(rec)
        rec["escorts"] = live_esc
        out[str(k)] = rec
    return out


def _with_lock(data_dir, fn):
    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_p = fdir / "escort_requests.lock"
    req_p = fdir / "escort_requests.json"
    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            return fn(req_p)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def request_escort(data_dir, key, mode, requester, guards, system, poi, needed=3,
                   dest_system="", threat_systems=None, resource="", reason="",
                   priority=90, ttl_s=DEFAULT_TTL_S, now_t=None):
    """Create or refresh an escort request atomically. Returns the stored request dict or None if capped."""
    now_t = time.time() if now_t is None else float(now_t)
    needed = max(1, min(10, int(needed or 3)))

    def _op(req_p):
        reqs = _clean_requests_unlocked(_read_json(req_p, {}), now_t)
        if key not in reqs:
            same_mode = sum(1 for r in reqs.values() if r.get("mode") == mode)
            cap = MAX_FIELD_REQUESTS if mode == "field" else MAX_CONVOY_REQUESTS
            if same_mode >= cap:
                _write_json(req_p, {"updated_at": int(now_t), "requests": reqs})
                return None
            rec = {
                "key": str(key), "mode": str(mode), "requester": str(requester),
                "guards": str(guards), "system": str(system), "poi": str(poi),
                "dest_system": str(dest_system or ""), "threat_systems": list(threat_systems or []),
                "resource": str(resource or ""), "reason": str(reason or ""),
                "needed": needed, "priority": int(priority), "escorts": {},
                "created_at": int(now_t), "expires_at": int(now_t + float(ttl_s or DEFAULT_TTL_S)),
                "active": True,
            }
        else:
            rec = dict(reqs[key])
            rec["needed"] = max(int(rec.get("needed") or 3), needed)
            rec["expires_at"] = max(int(rec.get("expires_at") or 0), int(now_t + float(ttl_s or DEFAULT_TTL_S)))
            rec["active"] = True
        reqs[str(key)] = rec
        _write_json(req_p, {"updated_at": int(now_t), "requests": reqs})
        return rec

    return _with_lock(data_dir, _op)


def join_escort(data_dir, key, pilot, power=0.0, is_flagship=False, now_t=None):
    """Atomically claim a slot in escort request `key` if open. Returns updated request or None."""
    now_t = time.time() if now_t is None else float(now_t)

    def _op(req_p):
        reqs = _clean_requests_unlocked(_read_json(req_p, {}), now_t)
        rec = reqs.get(str(key))
        if not rec:
            return None
        esc = rec.setdefault("escorts", {})
        if str(pilot) not in esc and len(esc) >= int(rec.get("needed") or 3):
            return None
        prev = esc.get(str(pilot)) or {}
        esc[str(pilot)] = {
            "at": int(now_t),
            "arrived": bool(prev.get("arrived", False)),
            "power": round(float(power or 0.0), 1),
            "flagship": bool(is_flagship),
        }
        reqs[str(key)] = rec
        _write_json(req_p, {"updated_at": int(now_t), "requests": reqs})
        return rec

    return _with_lock(data_dir, _op)


def mark_escort_arrived(data_dir, key, pilot, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)

    def _op(req_p):
        reqs = _clean_requests_unlocked(_read_json(req_p, {}), now_t)
        rec = reqs.get(str(key))
        if not rec or str(pilot) not in (rec.get("escorts") or {}):
            return None
        rec["escorts"][str(pilot)]["arrived"] = True
        rec["escorts"][str(pilot)]["at"] = int(now_t)
        reqs[str(key)] = rec
        _write_json(req_p, {"updated_at": int(now_t), "requests": reqs})
        return rec

    return _with_lock(data_dir, _op)


def release_escort_member(data_dir, key, pilot, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)

    def _op(req_p):
        reqs = _clean_requests_unlocked(_read_json(req_p, {}), now_t)
        rec = reqs.get(str(key))
        if rec and str(pilot) in (rec.get("escorts") or {}):
            rec["escorts"].pop(str(pilot), None)
            reqs[str(key)] = rec
            _write_json(req_p, {"updated_at": int(now_t), "requests": reqs})
        return True

    return _with_lock(data_dir, _op)


def clear_escort_request(data_dir, key, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)

    def _op(req_p):
        reqs = _clean_requests_unlocked(_read_json(req_p, {}), now_t)
        if str(key) in reqs:
            reqs.pop(str(key), None)
            _write_json(req_p, {"updated_at": int(now_t), "requests": reqs})
        return True

    return _with_lock(data_dir, _op)


def list_escort_requests(data_dir, now_t=None):
    """Return active escort requests sorted by (priority desc, unfilled first, created_at asc)."""
    now_t = time.time() if now_t is None else float(now_t)
    req_p = Path(data_dir) / "fleet" / "escort_requests.json"
    reqs = _clean_requests_unlocked(_read_json(req_p, {}), now_t)
    out = list(reqs.values())
    out.sort(key=lambda r: (-int(r.get("priority") or 0), len(r.get("escorts") or {}) >= int(r.get("needed") or 3), int(r.get("created_at") or 0)))
    return out


def get_escort_request(data_dir, key, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    req_p = Path(data_dir) / "fleet" / "escort_requests.json"
    reqs = _clean_requests_unlocked(_read_json(req_p, {}), now_t)
    return reqs.get(str(key))


def escort_ready_count(rec):
    if not isinstance(rec, dict):
        return 0
    return sum(1 for v in (rec.get("escorts") or {}).values() if isinstance(v, dict) and v.get("arrived"))


def is_field_escorted(data_dir, sys_id, poi_id, now_t=None):
    """True when a field escort pack for `sys_id:poi_id` has arrived and meets its needed count."""
    key = "field:%s:%s" % (sys_id, poi_id)
    rec = get_escort_request(data_dir, key, now_t=now_t)
    if not rec:
        return False
    return escort_ready_count(rec) >= max(1, int(rec.get("needed") or 3))
