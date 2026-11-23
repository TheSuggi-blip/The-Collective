#!/usr/bin/env python3
"""stop_pilot.py -- stop one or more in-flight ships of your division cleanly without touching global fleet/STOP.

WHAT: signals individual running ship(s) (or every running ship of your division on a named route) to end their
      current run cleanly at the next checkpoint, write their RESULT row, release their order file, and take the
      updated plan on the next dispatcher tick (within 30 seconds).
        - Hosted runs (in runhost: data/fleet/host/running/<job>.json): writes data/fleet/host/stop/<pilot>.
          runhost wakes that thread within 1 second, raises SystemExit("stopped by the host's stop file"),
          and unlinks the stop file.
        - Standalone runs (fresh order file outside runhost): writes data/fleet/stop/<pilot>. route_run.py
          reads and auto-unlinks it before the next stop or inside watch/mine/hunt loops.
RULES:
  - Strict division ownership (orders F1, division.py): an Admiral may stop only pilots of its own division;
    Unity (Fleet Admiral) and unattended service/admin shells may stop any pilot.
  - Never creates or touches global data/fleet/STOP; other divisions and other pilots keep flying undisturbed.
  - Rejects invalid pilot names (path separators, `..`, empty).
  - Pilots with no active run are reported as IDLE without creating stale stop files.
  - `--list` is read-only and prints currently running ships in your division (or all for Unity).
WHY:  Zero (reports ENT-148, 2026-11-23): twelve Nebula ships on a superseded circuit needed a per-pilot stop
      without halting the entire 500-ship fleet with data/fleet/STOP.

USAGE:
  stop_pilot.py --list [--data <dir>]                         list active runs in your division (or all for Unity)
  stop_pilot.py <pilot> [<pilot2> ...] [--dry-run]            stop named pilot(s) (also accepts comma-separated names)
  stop_pilot.py --route <route_id> [--dry-run]                stop all active runs of your division on <route_id>
  --data <dir>                                                the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402
import runhost                                    # noqa: E402


def valid_pilot(name):
    """True when `name` is a safe pilot identifier (no path separators or traversal)."""
    if not isinstance(name, str):
        return False
    s = name.strip()
    if not s or s in (".", "..") or "/" in s or "\\" in s or "\x00" in s:
        return False
    return True


def safe_file_name(pilot):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", pilot)[:60] or "pilot"


def read_json(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def active_runs(data, now=None):
    """{pilot: {'mode': 'runhost'|'standalone', 'what': str, 'script': str, 'since': str}} for all active runs."""
    now = time.time() if now is None else now
    root = Path(data) / "fleet"
    out = {}
    running_dir = root / "host" / "running"
    if running_dir.is_dir():
        for p in sorted(running_dir.glob("*.json")):
            job = read_json(p)
            pilot = str(job.get("pilot") or "").strip()
            if pilot and valid_pilot(pilot):
                out[pilot] = {
                    "mode": "runhost",
                    "what": str(job.get("what") or ""),
                    "script": str(job.get("script") or ""),
                    "since": str(job.get("since") or ""),
                }
    orders_dir = root / "orders"
    if orders_dir.is_dir():
        for p in sorted(orders_dir.glob("*.json")):
            try:
                if now - p.stat().st_mtime > division.ORDER_FRESH:
                    continue
            except OSError:
                continue
            order = read_json(p)
            pilot = str(order.get("pilot") or p.stem).strip()
            what = str(order.get("what") or "")
            if not pilot or not valid_pilot(pilot) or pilot in out:
                continue
            if what.startswith("hand "):
                continue
            out[pilot] = {
                "mode": "standalone",
                "what": what,
                "script": "",
                "since": str(order.get("since") or ""),
            }
    return out


def matches_route(what, route_id):
    """True when a run's `what` string (e.g. 'circuit foo', 'mine foo', 'hunt foo') matches `route_id`."""
    if not what or not route_id:
        return False
    w = what.strip()
    if w == route_id:
        return True
    parts = w.split()
    return len(parts) >= 2 and parts[-1] == route_id


def allowed(pilot, data, kind, who):
    """(True, '') when caller may stop `pilot`, else (False, reason)."""
    if not valid_pilot(pilot):
        return False, "invalid pilot name %r" % (pilot,)
    if kind == "member" and who != "Unity":
        owner = division.owner(pilot, data)
        if owner != who:
            return False, "%s belongs to %s, not %s (orders F1)" % (pilot, owner, who)
    return True, ""


def request_stop(pilot, data, runs=None, dry=False):
    """Signal one pilot's active run to stop. Returns (status, message) where status in ('stopped', 'idle')."""
    runs = active_runs(data) if runs is None else runs
    info = runs.get(pilot)
    if not info:
        return "idle", "IDLE %s: no active run to stop" % pilot
    root = Path(data) / "fleet"
    if info["mode"] == "runhost":
        target = root / "host" / "stop" / pilot
        via = "runhost (data/fleet/host/stop/%s)" % pilot
    else:
        target = root / "stop" / safe_file_name(pilot)
        via = "standalone (data/fleet/stop/%s)" % safe_file_name(pilot)
    if dry:
        return "stopped", "WOULD STOP %s (was: %s) via %s" % (pilot, info["what"] or "?", via)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ\n", time.gmtime()), encoding="utf-8")
    return "stopped", "STOPPED %s (was: %s) via %s" % (pilot, info["what"] or "?", via)


def parse_pilots(raw_args):
    out = []
    for a in raw_args:
        for item in a.split(","):
            s = item.strip()
            if s and s not in out:
                out.append(s)
    return out


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    data = division.DATA
    if "--data" in args:
        i = args.index("--data")
        if i + 1 >= len(args):
            sys.exit("USAGE: --data needs a folder")
        data = args[i + 1]
        args = args[:i] + args[i + 2:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    show_list = "--list" in args
    args = [a for a in args if a != "--list"]
    route_id = ""
    if "--route" in args:
        i = args.index("--route")
        if i + 1 >= len(args):
            sys.exit("USAGE: --route needs a route id")
        route_id = args[i + 1].strip()
        args = args[:i] + args[i + 2:]

    kind, who = division.member()
    runs = active_runs(data)

    if show_list:
        mine = [(p, info) for p, info in sorted(runs.items()) if allowed(p, data, kind, who)[0]]
        scope = who if (kind == "member" and who != "Unity") else "all divisions"
        print("ACTIVE RUNS (%s): %d running" % (scope, len(mine)))
        for p, info in mine:
            print("  %-18s | %-10s | %s" % (p, info["mode"], info["what"] or info["script"] or "?"))
        return 0

    if route_id:
        targets = [p for p, info in sorted(runs.items()) if matches_route(info["what"], route_id) and allowed(p, data, kind, who)[0]]
        if not targets:
            scope = who if (kind == "member" and who != "Unity") else "the fleet"
            print("NONE: no active runs in %s on route %s" % (scope, route_id))
            return 0
        count = 0
        for p in targets:
            st, msg = request_stop(p, data, runs=runs, dry=dry)
            print(msg)
            if st == "stopped":
                count += 1
        print("SUMMARY: %s %d pilot(s) on route %s" % ("would stop" if dry else "stop requested for", count, route_id))
        return 0

    targets = parse_pilots(args)
    if not targets:
        print(__doc__.split("USAGE:")[1].split("Stdlib")[0].strip())
        return 2

    refused = []
    for p in targets:
        ok, why = allowed(p, data, kind, who)
        if not ok:
            refused.append("REFUSED: %s" % why)
    if refused:
        for line in refused:
            print(line)
        return 1

    stopped_n, idle_n = 0, 0
    for p in targets:
        st, msg = request_stop(p, data, runs=runs, dry=dry)
        print(msg)
        if st == "stopped":
            stopped_n += 1
        else:
            idle_n += 1
    if len(targets) > 1:
        print("SUMMARY: %s %d pilot(s), %d idle" % ("would stop" if dry else "stop requested for", stopped_n, idle_n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
