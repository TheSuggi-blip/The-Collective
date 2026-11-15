#!/usr/bin/env python3
"""board.py -- the board of a division: what each of its ships does now, its plan, what is planned, and what its runs earned.

WHAT: one read of the fleet's live data, printed for a member: its ships by
      what they are doing (a runner's task, a hand hold, docked and free, in
      space and free), the plan of each of its roles with every route's
      measured figure and how many ships fly it now, what its Admiral has
      planned next, and what the runs of its ships earned and cost in the
      last hours. With `all` it prints every division, so that Admirals see
      each other's work and plans before they send ships anywhere.
RULES:
  - It reads only: the fleet's live file, the order files, the runs file
    (the unit's data folder) and the plans and routes (the repository).
  - Nothing here is kept by hand and nothing is written: the board is
    computed at every call, so it cannot be stale.
  - Credits per ship-hour leave one-time rewards out and count only runs
    that read a wallet.
WHY:  five Admirals command ships in the same six systems. Each has to see
      who is where and who plans what, without asking and without a file
      somebody forgot to update.

USAGE:
  board.py                    the board of the member this shell belongs to
  board.py <Member>           the board of that member (Zero, Apollo, Mercury, Apophis, Oracle, Unity)
  board.py all                every division, one block each
  --hours N                   the window of the runs table (default 4)
  --data <dir>                the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent     # the game/ folder
NAMES = {"Zero": "Mining", "Mercury": "Trade", "Apollo": "Logistics", "Apophis": "Military", "Oracle": "Intel", "Unity": "Command"}


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def runs_since(data, since):
    rows = []
    try:
        with open(Path(data) / "routes" / "runs.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                    if calendar.timegm(time.strptime(row["started"], "%Y-%m-%dT%H:%M:%SZ")) >= since:
                        rows.append(row)
                except (ValueError, KeyError):
                    continue
    except OSError:
        pass
    return rows


def state_of(ship, what):
    """One word group for what a ship is doing now."""
    if ship.get("status") != "connected":
        return "not connected"
    if what:
        return what
    if (ship.get("activity") or {}).get("kind") not in (None, "idle"):
        return "busy without an order file (%s)" % (ship.get("activity") or {}).get("kind")
    return "docked, free" if ship.get("docked") else "in space, free"


def figure(rows):
    """(runs with a wallet reading, ship-hours, credits without one-time, per ship-hour or None)."""
    read = [r for r in rows if (r.get("credits_before") or 0) > 0]
    minutes = sum(r.get("minutes") or 0 for r in read)
    credits = sum((r.get("delta") or 0) - (r.get("one_time") or 0) for r in read)
    return len(read), minutes / 60.0, credits, (round(60 * credits / minutes) if minutes else None)


def block(who, data, hours, now):
    """The board of one member as lines."""
    fleet = read_json(Path(data) / "fleet" / "fleet.json", {})
    ships = [s for s in fleet.get("ships") or [] if isinstance(s, dict) and s.get("name") and division.owner(s["name"], data) == who]
    age = ""
    try:
        age = "%d s old" % (now - calendar.timegm(time.strptime(fleet.get("updated_at", ""), "%Y-%m-%dT%H:%M:%SZ")))
    except ValueError:
        age = "age unknown"
    lines = ["BOARD of %s (%s) | %s | fleet data %s" % (who, NAMES.get(who, "?"), time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(now)), age)]
    if not ships:
        return lines + ["  no ship in the fleet's live file", ""]
    doing = defaultdict(list)
    for ship in ships:
        doing[state_of(ship, division.order_of(ship["name"], data, now))].append(ship)
    lines.append("  ships %d | credits %s | lowest wallet %s | lowest fuel %s%%" % (
        len(ships), format(sum(s.get("credits") or 0 for s in ships), ","), format(min(s.get("credits") or 0 for s in ships), ","),
        min((round(100 * s["fuel"] / s["max_fuel"]) for s in ships if s.get("max_fuel")), default="?")))
    lines.append("NOW")
    for what, group in sorted(doing.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        where = Counter(s.get("system") or "?" for s in group).most_common(4)
        names = ", ".join(sorted(s["name"] for s in group)[:6]) + (" ..." if len(group) > 6 else "")
        lines.append("  %-42s %3d  at %s | %s" % (what[:42], len(group), ", ".join("%s %d" % w for w in where), names))
    roles, owners, _errors = division.load_plan(ROOT)
    flying = Counter(division.order_of(s["name"], data, now) for s in ships)
    for role in sorted(r for r in roles if owners.get(r) == who):
        lines.append("PLAN %s (game/routes/plans/%s.json)" % (role, role))
        for n, rid in enumerate(roles[role], 1):
            route = read_json(ROOT / "routes" / (rid + ".json"), None)
            if not isinstance(route, dict):
                lines.append("  %d %-28s NO ROUTE FILE" % (n, rid))
                continue
            m = route.get("measured") or {}
            gate = [g for g in ("once" if route.get("once") else "", "off" if route.get("status") == "off" else "",
                                "max %s" % route["max_ships"] if route.get("max_ships") else "", "park" if route.get("park") else "") if g]
            paid = "one-time" if route.get("once") else ("%s cr per ship-hour over %s runs" % (format(m["cph_per_ship"], ","), m.get("runs")) if m else "not measured")
            lines.append("  %d %-28s %-16s flying %-3d %s" % (n, rid, ", ".join(gate), sum(c for what, c in flying.items() if what.endswith(" " + rid)), paid))
        for item in read_json(ROOT / "routes" / "plans" / (role + ".json"), {}).get("planned") or []:
            if isinstance(item, dict):
                lines.append("  planned: %s%s" % (str(item.get("what") or "")[:150], (" | when: %s" % item["when"]) if item.get("when") else ""))
    own = {s["name"] for s in ships}
    rows = [r for r in runs_since(data, now - hours * 3600) if r.get("pilot") in own]
    lines.append("RUNS of the last %g hours (credits without one-time rewards; only runs that read a wallet)" % hours)
    by = defaultdict(list)
    for row in rows:
        by[row.get("route") or "?"].append(row)
    for rid, group in sorted(by.items()):
        n, ship_hours, credits, rate = figure(group)
        once = sum(r.get("one_time") or 0 for r in group)
        lines.append("  %-28s runs %-3d ship-hours %5.1f  credits %+8d  per ship-hour %s  | one-time %+d" % (
            rid, n, ship_hours, credits, format(rate, "+,") if rate is not None else "no reading", once))
    if not by:
        lines.append("  no run")
    return lines + [""]


def main():
    args = sys.argv[1:]
    data = args[args.index("--data") + 1] if "--data" in args else division.DATA
    hours = float(args[args.index("--hours") + 1]) if "--hours" in args else 4.0
    rest = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--data", "--hours"))]
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    who = rest[0] if rest else division.member()[1]
    now = time.time()
    members = list(NAMES) if who == "all" else [who.capitalize()]
    if members[0] not in NAMES:
        sys.exit("board.py: name a member (%s) or `all`; this shell is no member" % ", ".join(NAMES))
    for name in members:
        print("\n".join(block(name, data, hours, now)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
