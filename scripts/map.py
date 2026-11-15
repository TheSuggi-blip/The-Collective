#!/usr/bin/env python3
"""map.py -- the galaxy chart of The Collective.

WHAT: keeps game/map/galaxy.tsv, the chart of every star system (id, name,
coordinates, empire, jump lanes), and answers two questions from it:
where a system is, and how many jumps lie between two systems.

The chart comes from the game's public map (no login). It holds what
every pilot knows from the first day: names, positions and lanes. What
is inside a system is learned by going there and is kept in game/planets/.

USAGE:
  map.py refresh              fetch the public chart, rewrite game/map/galaxy.tsv
  map.py where <system>       one system: position, empire, lanes, jumps from home
  map.py route <from> <to>    the shortest route between two systems, in jumps

A system is named by its id (nexus_prime) or its name ("Nexus Prime").
`route` counts lanes only; the game's own find_route may choose
differently (fuel, wormholes).

Stdlib only. ASCII only.
"""

import argparse
import collections
import json
import os
import sys
import time
import urllib.request

SOURCE = "https://game.spacemolt.com/api/map"
HOME = "nexus_prime"
USER_AGENT = "The-Collective map.py (github.com/TheSuggi-blip/The-Collective)"
COLUMNS = ["id", "name", "x", "y", "empire", "flags", "jumps_from_home", "lanes"]
System = collections.namedtuple("System", "id name x y empire flags jumps lanes")


def chart_path(root):
    return os.path.join(root, "game", "map", "galaxy.tsv")


def jumps_from(systems, start):
    """Breadth-first count of jumps from `start` to every system."""
    lanes = {s["id"]: s["connections"] for s in systems}
    dist = {start: 0} if start in lanes else {}
    queue = collections.deque(dist)
    while queue:
        here = queue.popleft()
        for there in lanes.get(here, ()):
            if there in lanes and there not in dist:
                dist[there] = dist[here] + 1
                queue.append(there)
    return dist


def rows_from_api(payload):
    """Turn the public map's JSON into chart rows, sorted by id."""
    systems = payload["systems"]
    dist = jumps_from(systems, HOME)
    rows = []
    for s in sorted(systems, key=lambda s: s["id"]):
        flags = [f for f, on in (("home", s.get("is_home")), ("stronghold", s.get("is_stronghold"))) if on]
        rows.append([
            s["id"],
            s["name"],
            "%.1f" % s["x"],
            "%.1f" % s["y"],
            s.get("empire") or "-",
            ",".join(flags) or "-",
            str(dist[s["id"]]) if s["id"] in dist else "-",
            ",".join(sorted(s["connections"])),
        ])
    for row in rows:
        for cell in row:
            if "\t" in cell or "\n" in cell or not cell.isascii():
                raise ValueError("chart cell is not plain one-line ASCII: %r" % cell)
    return rows


def read_chart(root):
    """Return {id: System} from game/map/galaxy.tsv."""
    path = chart_path(root)
    if not os.path.isfile(path):
        sys.exit("No chart at %s. Run: map.py refresh" % path)
    systems = {}
    with open(path, encoding="ascii") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            cells = line.split("\t")
            if cells[0] == "id":
                continue
            if len(cells) != len(COLUMNS):
                sys.exit("Broken chart row (expected %d columns): %s" % (len(COLUMNS), line))
            systems[cells[0]] = System(
                cells[0], cells[1], float(cells[2]), float(cells[3]), cells[4],
                [] if cells[5] == "-" else cells[5].split(","),
                None if cells[6] == "-" else int(cells[6]),
                cells[7].split(",") if cells[7] else [],
            )
    return systems


def chart_rows_on_disk(root):
    path = chart_path(root)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="ascii") as handle:
        return [line.rstrip("\n").split("\t") for line in handle
                if line.strip() and not line.startswith("#") and not line.startswith("id\t")]


def write_chart(root, rows, fetched):
    os.makedirs(os.path.join(root, "game", "map"), exist_ok=True)
    with open(chart_path(root), "w", encoding="ascii", newline="\n") as handle:
        handle.write("# The galaxy chart: every star system on the game's public map.\n")
        handle.write("# Source: %s | Fetched: %s | Systems: %d | Home: %s\n"
                     % (SOURCE, fetched, len(rows), HOME))
        handle.write("# Written by scripts/map.py refresh. Do not edit by hand.\n")
        handle.write("# x and y are Galactic Units. empire - means lawless space.\n")
        handle.write("\t".join(COLUMNS) + "\n")
        for row in rows:
            handle.write("\t".join(row) + "\n")


def find(systems, word):
    """Find a system by id or by name (case-insensitive)."""
    if word in systems:
        return systems[word]
    wanted = word.strip().lower()
    for system in systems.values():
        if system.name.lower() == wanted or system.id == wanted.replace(" ", "_"):
            return system
    sys.exit("Unknown system: %s (look it up in game/map/galaxy.tsv)" % word)


def route(systems, start, goal):
    """Shortest list of system ids from start to goal, or None."""
    previous = {start: None}
    queue = collections.deque([start])
    while queue:
        here = queue.popleft()
        if here == goal:
            path = []
            while here is not None:
                path.append(here)
                here = previous[here]
            return path[::-1]
        for there in systems[here].lanes:
            if there in systems and there not in previous:
                previous[there] = here
                queue.append(there)
    return None


def label(system):
    parts = [system.empire if system.empire != "-" else "lawless"] + system.flags
    return "%s (%s)" % (system.id, ", ".join(parts))


def intel_file(root, system_id):
    for letter in "anh":
        name = "game/planets/%s-%s.md" % (letter, system_id)
        if os.path.isfile(os.path.join(root, name)):
            return name
    return "none yet"


def cmd_refresh(root):
    request = urllib.request.Request(SOURCE, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    rows = rows_from_api(payload)
    if not rows:
        sys.exit("The public map returned no systems; the chart was left as it is.")
    if rows == chart_rows_on_disk(root):
        print("No change: %d systems, chart left as it is." % len(rows))
        return 0
    write_chart(root, rows, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("Chart written: %d systems -> %s" % (len(rows), chart_path(root)))
    return 0


def cmd_where(root, word):
    systems = read_chart(root)
    s = find(systems, word)
    print("%s -- %s" % (s.id, s.name))
    print("  position:        x %.1f, y %.1f (Galactic Units)" % (s.x, s.y))
    print("  empire:          %s" % (s.empire if s.empire != "-" else "none (lawless space)"))
    if s.flags:
        print("  flags:           %s" % ", ".join(s.flags))
    print("  jumps from home: %s (home is %s)" % ("no route" if s.jumps is None else s.jumps, HOME))
    print("  lanes:           %s" % "; ".join(label(systems[n]) for n in s.lanes if n in systems))
    print("  intel file:      %s" % intel_file(root, s.id))
    return 0


def cmd_route(root, start_word, goal_word):
    systems = read_chart(root)
    start, goal = find(systems, start_word), find(systems, goal_word)
    path = route(systems, start.id, goal.id)
    if path is None:
        print("No route from %s to %s." % (start.id, goal.id))
        return 1
    print("%d jumps: %s -> %s" % (len(path) - 1, start.id, goal.id))
    for step, system_id in enumerate(path):
        print("  %2d  %s" % (step, label(systems[system_id])))
    return 0


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="The galaxy chart of The Collective.")
    parser.add_argument("--root", default=os.path.join(here, ".."))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("refresh", help="fetch the public chart and rewrite game/map/galaxy.tsv")
    where = sub.add_parser("where", help="one system: position, empire, lanes, jumps from home")
    where.add_argument("system")
    way = sub.add_parser("route", help="the shortest route between two systems, in jumps")
    way.add_argument("start")
    way.add_argument("goal")
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    if args.command == "refresh":
        return cmd_refresh(root)
    if args.command == "where":
        return cmd_where(root, args.system)
    return cmd_route(root, args.start, args.goal)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # The reader closed the pipe early (for example `| head`).
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(1)
