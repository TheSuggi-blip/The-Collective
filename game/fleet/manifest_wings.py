#!/usr/bin/env python3
"""manifest_wings.py -- shared cached resolver for game/fleet-500-manifest.tsv wings & Task Forces.

WHAT: reads game/fleet-500-manifest.tsv once (mtime-cached) and exposes wing_of(pilot),
      matches_wing(pilot, wing_prefix, wing_contains, exclude_wing_prefix), and
      task_forces() for dispatch.py, mine_net.py, hunt_net.py, and haul.py.

Usage:
  python3 -I -B game/fleet/manifest_wings.py

Stdlib only. ASCII only.
"""

import csv
from pathlib import Path

_DEFAULT_REPO = Path(__file__).resolve().parents[2]
_CACHE = {"path": "", "mtime": 0.0, "by_pilot": {}, "rows": []}


def _load(repo_root=None):
    rp = Path(repo_root) if repo_root else _DEFAULT_REPO
    mp = rp / "game" / "fleet-500-manifest.tsv"
    if not mp.is_file():
        return {}, []
    try:
        mt = mp.stat().st_mtime
    except OSError:
        return {}, []
    if _CACHE["path"] == str(mp) and _CACHE["mtime"] == mt and _CACHE["by_pilot"]:
        return _CACHE["by_pilot"], _CACHE["rows"]
    by_p = {}
    rows = []
    try:
        lines = [
            ln for ln in mp.read_text(encoding="utf-8", errors="replace").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")
        ]
        for row in csv.DictReader(lines, delimiter="\t"):
            p = str(row.get("pilot") or "").strip()
            if not p:
                continue
            rec = {
                "pilot": p,
                "division": str(row.get("division") or "").strip(),
                "wing": str(row.get("wing") or "").strip(),
                "prefix": str(row.get("prefix") or "").strip(),
                "empire": str(row.get("empire") or "").strip().lower(),
                "target_t1": str(row.get("target_t1") or "").strip().lower(),
                "target_t2": str(row.get("target_t2") or "").strip().lower(),
            }
            by_p[p] = rec
            rows.append(rec)
    except OSError:
        return {}, []
    _CACHE.update({"path": str(mp), "mtime": mt, "by_pilot": by_p, "rows": rows})
    return by_p, rows


def info_of(pilot, repo_root=None):
    by_p, _ = _load(repo_root)
    return by_p.get(str(pilot or "").strip()) or {}


def wing_of(pilot, repo_root=None):
    return str(info_of(pilot, repo_root).get("wing") or "")


def matches_wing(pilot, wing_prefix=None, wing_contains=None, exclude_wing_prefix=None, repo_root=None):
    """Return (ok: bool, reason: str) for route/cohort wing filters."""
    w = wing_of(pilot, repo_root)
    if wing_prefix:
        pfxs = [str(x) for x in (wing_prefix if isinstance(wing_prefix, (list, tuple)) else [wing_prefix]) if x]
        if pfxs and not any(w.startswith(p) for p in pfxs):
            return False, "wing %r not in %s" % (w or "none", ",".join(pfxs))
    if wing_contains:
        subs = [str(x).lower() for x in (wing_contains if isinstance(wing_contains, (list, tuple)) else [wing_contains]) if x]
        wl = w.lower()
        if subs and not any(s in wl for s in subs):
            return False, "wing %r lacks %s" % (w or "none", ",".join(subs))
    if exclude_wing_prefix:
        epfxs = [str(x) for x in (exclude_wing_prefix if isinstance(exclude_wing_prefix, (list, tuple)) else [exclude_wing_prefix]) if x]
        if epfxs and any(w.startswith(p) for p in epfxs):
            return False, "wing %r excluded by %s" % (w, ",".join(epfxs))
    return True, ""


def task_forces(repo_root=None):
    """Return manifest-defined 1A Command Task Forces (tf-prime [10], tf-alpha [8], tf-beta [8])."""
    _, rows = _load(repo_root)
    specs = (
        ("tf-prime", "1A-Prime.", "gsc_0044"),
        ("tf-alpha", "1A-Alpha.", "atria"),
        ("tf-beta",  "1A-Beta.",  "felis"),
    )
    out = {}
    for sq_id, pfx, outpost in specs:
        members = [r for r in rows if r["wing"].startswith(pfx)]
        if not members:
            continue
        cmds = [r["pilot"] for r in members if "-- Command" in r["wing"]]
        others = [r["pilot"] for r in members if "-- Command" not in r["wing"]]
        leader = cmds[0] if cmds else members[0]["pilot"]
        ordered = cmds + others
        out[sq_id] = {
            "squad_id": sq_id,
            "outpost_system": outpost,
            "leader": leader,
            "command_ships": cmds,
            "size": len(ordered),
            "members": ordered,
        }
    return out


if __name__ == "__main__":
    for k, v in task_forces().items():
        print(k, v["size"], v["outpost_system"], v["leader"])
