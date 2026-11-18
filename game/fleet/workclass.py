#!/usr/bin/env python3
"""workclass.py -- whose work a route is: the work class of every route and the classes each role flies

WHAT: one answer, used by every script that gives ships work (the dispatcher's rule, fill.py, supply.py, the
      statistics): what class of work a route is, and which roles do that class.
        gather   mining ore, ice or gas (kind mine, or a circuit with a mine stop)        miner
        hunt     hunting wildlife (kind hunt, or a circuit with a hunt stop)               drone, sentinel, scout, command
        guard    guarding and escorting (kind guard)                                      drone, sentinel
        census   reading the world (kind census)                                          scout
        trade    buying for the fleet or for a price gap (a circuit that buys)            trader, hauler
        haul     supplying our bases (a bunker or faction-storage stop, outpost- and       hauler
                 supply- circuits)
        once     a mission the game pays once per pilot (voidborn-, mission-, first-;      every role
                 `once` or `one_time` in the file)
        sell, craft, fit, other                                                          every role
                 a ship sells its own stores, here or at a far buyer (storage is the pilot's own), crafts from its
                 own stores (rule F24), fits a module, trains or docks
      A route file may add roles by `open_to` (a list of roles): its Admiral's word that another class may fly it,
      with the reason in its note.
RULES:
  - Gathering is the miners' work (Suggi, 2026-11-18: "Ore is miners job, its not something everyone does"). Every
    division flies the work of its own class; work every role shares is a mission, selling or crafting its own stores,
    fitting and training (rule F23).
  - The class is read from the route file alone (its kind, its stops, its id), never from who flies it.
WHY:  until 2026-11-18 the filler lent the miners' gather routes to every waiting ship, so traders, haulers, drones and
      scouts all gathered iron, overshot the reserve and burnt fuel. One function now says whose work a route is.

USAGE:
  workclass.py show [<route id>]   the class and the roles of one route, or the count of routes per class
  workclass.py roles               the classes each role flies
  workclass.py plans               per role plan (game/routes/plans/<role>.json): the routes that are not of its class

Stdlib only. ASCII only.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # the repository's game/
ALL = ("miner", "trader", "hauler", "drone", "sentinel", "scout", "command")
SHARED = ("once", "sell", "craft", "fit", "other")
CLASS_ROLES = {
    "gather": ("miner",),
    "hunt": ("drone", "sentinel", "scout", "command"),
    "guard": ("drone", "sentinel"),
    "census": ("scout",),
    "trade": ("trader", "hauler"),
    "haul": ("hauler",),
}
ONCE_PREFIXES = ("voidborn-", "mission-", "first-")
HAUL_PREFIXES = ("outpost-", "supply-")


def _stops(route):
    return [stop for stop in route.get("stops") or [] if isinstance(stop, dict)]


def work_class(route, rid=None):
    """The work class of a route (a dict of its file): gather, hunt, guard, census, trade, haul, once, sell, craft,
    fit or other."""
    rid = str(rid or route.get("id") or "")
    kind = route.get("kind")
    if route.get("once") or route.get("one_time") or rid.startswith(ONCE_PREFIXES):
        return "once"
    if kind == "mine":
        return "gather"
    if kind in ("hunt", "guard", "census"):
        return kind
    stops = _stops(route)
    keys = set()
    for stop in stops:
        keys.update(stop.keys())
    if "mine" in keys:
        return "gather"
    if "hunt" in keys:
        return "hunt"
    if keys & {"bunker", "store_faction"} or rid.startswith(HAUL_PREFIXES):
        return "haul"
    if "fit" in keys:
        return "fit"
    if "buy" in keys:
        return "trade"
    if "craft" in keys:
        return "craft"
    if "sell" in keys or route.get("sell"):
        return "sell"
    return "other"


def roles_for(route, rid=None):
    """The roles whose work the route is: its class's roles plus its file's `open_to`."""
    cls = work_class(route, rid)
    roles = list(ALL if cls in SHARED else CLASS_ROLES.get(cls, ()))
    for role in route.get("open_to") or []:
        if role in ALL and role not in roles:
            roles.append(role)
    return tuple(roles)


def own(role, route, rid=None):
    """True when a ship of `role` may fly the route as work of its own class."""
    return role in roles_for(route, rid)


def classes_of(role):
    """The classes a role flies: its own, then the shared ones."""
    return tuple(cls for cls, roles in CLASS_ROLES.items() if role in roles) + SHARED


def load(root=ROOT):
    """{route id: route dict} of every route file."""
    found = {}
    for path in sorted((Path(root) / "routes").glob("*.json")):
        try:
            found[path.stem] = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            continue
    return found


def main(argv):
    if not argv or argv[0] not in ("show", "roles", "plans"):
        print(__doc__.split("USAGE:")[1].split("Stdlib")[0].rstrip())
        return 2
    if argv[0] == "roles":
        for role in ALL:
            print("%-9s %s" % (role, ", ".join(classes_of(role))))
        return 0
    routes = load()
    if argv[0] == "show":
        if len(argv) > 1:
            route = routes.get(argv[1])
            if route is None:
                print("no route file %s" % argv[1])
                return 1
            print("%s: %s, flown by %s" % (argv[1], work_class(route, argv[1]), ", ".join(roles_for(route, argv[1]))))
            return 0
        count = {}
        for rid, route in routes.items():
            count[work_class(route, rid)] = count.get(work_class(route, rid), 0) + 1
        print("WORKCLASS | %d route files by class" % len(routes))
        for cls in list(CLASS_ROLES) + list(SHARED):
            print("  %-7s %4d   %s" % (cls, count.get(cls, 0), ", ".join(CLASS_ROLES.get(cls, ("every role",)))))
        return 0
    folder = Path(ROOT) / "routes" / "plans"
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        role = path.stem
        if role not in ALL:
            continue
        try:
            plan = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            continue
        ids = [row.get("route") if isinstance(row, dict) else row for row in plan.get("routes") or []]
        other = [rid for rid in ids if rid in routes and not own(role, routes[rid], rid)]
        print("%-9s %3d routes in its plan, %d of another class%s" % (role, len(ids), len(other), (": " + ", ".join(other)) if other else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
