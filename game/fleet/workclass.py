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
      Strict classes, behind the switch file data/fleet/strict-classes-on (absent = off: the classes above, as
      before; Suggi, 2026-11-21: "Only Zero mines, only Mercury trades", each division its own activities):
        trade    a circuit that buys and neither crafts nor supplies a base                trader
        sell     a circuit that sells and neither buys nor crafts                          trader
        craft    a circuit that crafts, with or without a buy (Logistics crafts what we    hauler, trader
                 build with, Trade what sells; off, a buy wins over a craft)
        once, deliver, fit, other                                                          every role
                 deliver: a circuit whose stops only `gift` (handover.py), with `store` and `withdraw`; no buy, sell
                 or craft (off: such a circuit is `other`)
      and the sale rule (sale_refused, called by dispatch.why_not): a route that sells (a mine route's `sell` without
      `gift`, a hunt route without `gift_to`, which sells its loot at `sell_at`, a circuit stop's `sell`) is refused to a pilot
      that is not a trader: `sells: Trade's work (F23); give the goods to a trader with `gift``. A mission that pays
      once keeps its sale. The goods reach a trader by gift (handover.py).
      A route file may add roles by `open_to` (a list of roles): its Admiral's word that another class may fly it,
      with the reason in its note. `open_to` lifts no sale rule.
RULES:
  - Gathering is the miners' work (Suggi, 2026-11-18: "Ore is miners job, its not something everyone does"). Every
    division flies the work of its own class; work every role shares is a mission, selling or crafting its own stores,
    fitting and training (rule F23); with the switch on, selling and buying are Trade's, crafting Logistics' and Trade's.
  - The class is read from the route file alone (its kind, its stops, its id), never from who flies it.
  - The switch is read from the data folder of the caller's pass (follow(): the dispatcher's and fill.py's state
    name it; else FLEET_DATA_ROOT or /srv/collective/data), at most once a second. STRICT, set by a caller (a test,
    a dry run), overrides the file. CLASS_ROLES and SHARED answer for the state the switch is in.
WHY:  until 2026-11-18 the filler lent the miners' gather routes to every waiting ship, so traders, haulers, drones and
      scouts all gathered iron, overshot the reserve and burnt fuel. One function now says whose work a route is.

USAGE:
  workclass.py show [<route id>] [--strict]   the class and the roles of one route, or the count of routes per class;
                                              --strict: the answer with the switch off and with it on
  workclass.py roles [--strict]               the classes each role flies (--strict: in both states)
  workclass.py plans [--strict]               per role plan (game/routes/plans/<role>.json): the routes that are not of
                                              its class (--strict: in both states)
  workclass.py sales                          the dry run of the sale rule: the routes it would refuse with the switch
                                              on, per class and per Admiral (whose role plans name them for a role that
                                              is not the traders'), each with the roles it would be closed to
  --data <dir>   the unit's data folder whose switch is read (default FLEET_DATA_ROOT or /srv/collective/data)

Stdlib only. ASCII only.
"""

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # the repository's game/
ALL = ("miner", "trader", "hauler", "drone", "sentinel", "scout", "command")
OFF_SHARED = ("once", "sell", "craft", "fit", "other")
OFF_ROLES = {
    "gather": ("miner",),
    "hunt": ("drone", "sentinel", "scout", "command"),
    "guard": ("drone", "sentinel"),
    "census": ("scout",),
    "trade": ("trader", "hauler"),
    "haul": ("hauler",),
}
STRICT_SHARED = ("once", "deliver", "fit", "other")
STRICT_ROLES = dict(OFF_ROLES, trade=("trader",), sell=("trader",), craft=("hauler", "trader"))
KEEPERS = {"miner": "Zero", "trader": "Mercury", "hauler": "Apollo", "drone": "Apophis", "sentinel": "Apophis", "scout": "Oracle",
           "command": "Unity"}               # division.ROLES: who commands each role (this file imports nothing of the fleet)
ONCE_PREFIXES = ("voidborn-", "mission-", "first-")
HAUL_PREFIXES = ("outpost-", "supply-")
DELIVER_KEYS = {"at", "gift", "store", "withdraw", "refuel", "redock", "skip_if_hold", "only_if_active", "burn_cells"}
SWITCH = os.path.join("fleet", "strict-classes-on")  # under the data folder: the strict classes and the sale rule act while it exists
DATA = os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data"
STRICT = None                 # None: the switch file decides; True or False: a caller's own setting (a test, a dry run)
LOOK = 1.0                    # seconds one look at the switch file holds: a pass that asks thousands of times reads the disk once a second
SEEN = {}                     # data folder -> (monotonic clock of the look, the file existed)
SALE = "sells: Trade's work (F23); give the goods to a trader with `gift`"


def follow(data):
    """The data folder whose switch the answers follow from now on: the caller's pass names it (the dispatcher's
    --data, fill.py's survey). None or empty: unchanged."""
    global DATA
    if data:
        DATA = str(data)


def strict_on(data=None):
    """True while the switch file data/fleet/strict-classes-on exists (STRICT instead, when a caller set it)."""
    if STRICT is not None:
        return bool(STRICT)
    folder = str(data or DATA)
    clock = time.monotonic()
    seen = SEEN.get(folder)
    if seen is None or clock - seen[0] >= LOOK or clock < seen[0]:
        if len(SEEN) > 64:
            SEEN.clear()
        seen = SEEN[folder] = (clock, os.path.exists(os.path.join(folder, SWITCH)))
    return seen[1]


def _strict(strict):
    return strict_on() if strict is None else bool(strict)


def class_roles(strict=None):
    """{class: its roles} in the state the switch is in (or the state `strict` names)."""
    return STRICT_ROLES if _strict(strict) else OFF_ROLES


def shared(strict=None):
    """The classes every role flies, in the state the switch is in (or the state `strict` names)."""
    return STRICT_SHARED if _strict(strict) else OFF_SHARED


def __getattr__(name):
    """workclass.CLASS_ROLES and workclass.SHARED, as their readers (stats.py, guidebook.py, the tests) name them:
    the answer of the state the switch is in."""
    if name == "CLASS_ROLES":
        return class_roles()
    if name == "SHARED":
        return shared()
    raise AttributeError("module 'workclass' has no attribute %r" % name)


def _stops(route):
    return [stop for stop in route.get("stops") or [] if isinstance(stop, dict)]


def work_class(route, rid=None, strict=None):
    """The work class of a route (a dict of its file): gather, hunt, guard, census, trade, haul, once, sell, craft,
    fit or other; with the switch on also deliver, and a circuit that buys and crafts is `craft` (off: `trade`)."""
    strict = _strict(strict)
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
    if strict and "craft" in keys:
        return "craft"
    if "buy" in keys:
        return "trade"
    if "craft" in keys:
        return "craft"
    if "sell" in keys or route.get("sell"):
        return "sell"
    if strict and "gift" in keys and keys <= DELIVER_KEYS:
        return "deliver"
    return "other"


def roles_for(route, rid=None, strict=None):
    """The roles whose work the route is: its class's roles plus its file's `open_to`."""
    strict = _strict(strict)
    cls = work_class(route, rid, strict)
    roles = list(ALL if cls in shared(strict) else class_roles(strict).get(cls, ()))
    for role in route.get("open_to") or []:
        if role in ALL and role not in roles:
            roles.append(role)
    return tuple(roles)


def own(role, route, rid=None, strict=None):
    """True when a ship of `role` may fly the route as work of its own class."""
    return role in roles_for(route, rid, strict)


def classes_of(role, strict=None):
    """The classes a role flies: its own, then the shared ones."""
    strict = _strict(strict)
    return tuple(cls for cls, roles in class_roles(strict).items() if role in roles) + shared(strict)


def sells(route):
    """True for a route that sells: a mine route's `sell` without `gift` (with the switch on mine.py hands the goods
    over instead of selling them, as hunt.py does with `gift_to`), a hunt route without `gift_to` (hunt.py sells its
    loot at `sell_at`), a circuit with a stop's `sell`."""
    kind = route.get("kind")
    if kind == "mine":
        return bool(route.get("sell")) and not route.get("gift")
    if kind == "hunt":
        return not route.get("gift_to")
    if kind == "circuit":
        return any(stop.get("sell") for stop in _stops(route))
    return False


def sale_refused(pilot, rid, route, state):
    """The dispatcher's hook (dispatch.why_not, before the class guard): the sale rule's reason, or None. With the
    switch on, a route that sells is refused to a pilot that is not a trader, unless it is a mission that pays once.
    It first points this module's answers at the pass's data folder (state["data"]). Off: always None."""
    if not isinstance(route, dict):
        return None
    follow((state or {}).get("data"))
    if not strict_on():
        return None
    role = pilot.get("role") or str(pilot.get("name") or "").split("-")[0]
    if role == "trader" or not sells(route) or work_class(route, rid) == "once":
        return None
    return SALE


def load(root=ROOT):
    """{route id: route dict} of every route file."""
    found = {}
    for path in sorted((Path(root) / "routes").glob("*.json")):
        try:
            found[path.stem] = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            continue
    return found


def role_plans(root=ROOT):
    """{role: [route ids]} of game/routes/plans/<role>.json."""
    out = {}
    folder = Path(root) / "routes" / "plans"
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        if path.stem not in ALL:
            continue
        try:
            plan = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            continue
        out[path.stem] = [row.get("route") if isinstance(row, dict) else row for row in plan.get("routes") or []]
    return out


def sales(routes, plans):
    """The dry run of the sale rule with the switch on: ([(route id, strict class, the roles it is closed to, the
    Admirals whose role plans name it for such a role)], {class: routes}, {Admiral: routes}). A route that is off
    closes nothing new and is left out; a route in no such plan counts under `in no plan`."""
    rows, by_class, by_admiral = [], {}, {}
    for rid, route in sorted(routes.items()):
        if not isinstance(route, dict) or route.get("status") == "off" or not sells(route) or work_class(route, rid, True) == "once":
            continue
        closed = [role for role in roles_for(route, rid, True) if role != "trader"]
        if not closed:
            continue
        admirals = sorted({KEEPERS[role] for role, ids in plans.items() if rid in ids and role in closed and role in KEEPERS})
        cls = work_class(route, rid, True)
        rows.append((rid, cls, closed, admirals))
        by_class[cls] = by_class.get(cls, 0) + 1
        for admiral in admirals or ["in no plan"]:
            by_admiral[admiral] = by_admiral.get(admiral, 0) + 1
    return rows, by_class, by_admiral


def narrowed(routes, plans):
    """The plan rows the strict classes take from a role (its own work with the switch off, another class's with it
    on: the class guard, data/fleet/class-guard-on, refuses them while both switches stand): [(role, route id,
    strict class)], {class: rows}, {Admiral: rows}."""
    rows, by_class, by_admiral = [], {}, {}
    for role, ids in sorted(plans.items()):
        for rid in ids:
            route = routes.get(rid)
            if not isinstance(route, dict) or route.get("status") == "off" or not own(role, route, rid, False) or own(role, route, rid, True):
                continue
            cls = work_class(route, rid, True)
            rows.append((role, rid, cls))
            by_class[cls] = by_class.get(cls, 0) + 1
            by_admiral[KEEPERS.get(role, "?")] = by_admiral.get(KEEPERS.get(role, "?"), 0) + 1
    return rows, by_class, by_admiral


def main(argv):
    data = argv[argv.index("--data") + 1] if "--data" in argv and argv.index("--data") + 1 < len(argv) else None
    argv = [a for n, a in enumerate(argv) if a != "--data" and (n == 0 or argv[n - 1] != "--data")]
    both = "--strict" in argv
    argv = [a for a in argv if a != "--strict"]
    if not argv or argv[0] not in ("show", "roles", "plans", "sales"):
        print(__doc__.split("USAGE:")[1].split("Stdlib")[0].rstrip())
        return 2
    follow(data)
    now = strict_on()
    states = (False, True) if both else (now,)
    label = lambda state: "strict classes %s" % ("ON" if state else "off")
    if both or now or argv[0] == "sales":
        print("WORKCLASS | the switch %s is %s" % (os.path.join(DATA, SWITCH), "present: strict classes on" if now else "absent: strict classes off"))
    if argv[0] == "roles":
        for state in states:
            if both:
                print("%s:" % label(state))
            for role in ALL:
                print("%-9s %s" % (role, ", ".join(classes_of(role, state))))
        return 0
    routes = load()
    if argv[0] == "show":
        if len(argv) > 1:
            route = routes.get(argv[1])
            if route is None:
                print("no route file %s" % argv[1])
                return 1
            for state in states:
                print("%s: %s, flown by %s%s" % (argv[1], work_class(route, argv[1], state), ", ".join(roles_for(route, argv[1], state)),
                                                 (" (%s)" % label(state)) if both else ""))
            if both and sells(route) and work_class(route, argv[1], True) != "once":
                print("  it sells: with strict classes on the dispatcher refuses it to every pilot that is not a trader (%s)" % SALE)
            return 0
        for state in states:
            count = {}
            for rid, route in routes.items():
                count[work_class(route, rid, state)] = count.get(work_class(route, rid, state), 0) + 1
            print("WORKCLASS | %d route files by class%s" % (len(routes), (", " + label(state)) if both or state else ""))
            for cls in list(class_roles(state)) + list(shared(state)):
                print("  %-7s %4d   %s" % (cls, count.get(cls, 0), ", ".join(class_roles(state).get(cls, ("every role",)))))
        return 0
    plans = role_plans()
    if argv[0] == "sales":
        rows, by_class, by_admiral = sales(routes, plans)
        print("SALES | the dry run of the sale rule: %d route files that sell would be refused to every pilot that is not a trader "
              "with strict classes on (%s)" % (len(rows), SALE))
        print("  per class (strict): %s" % (", ".join("%s %d" % kv for kv in sorted(by_class.items())) or "none"))
        print("  per Admiral (whose role plans name them for a role that is not the traders'): %s"
              % (", ".join("%s %d" % kv for kv in sorted(by_admiral.items())) or "none"))
        taken, taken_class, taken_admiral = narrowed(routes, plans)
        print("  and the strict classes take %d plan rows from a role whose own work they were (the class guard refuses them while "
              "data/fleet/class-guard-on stands): per class %s; per Admiral %s" % (len(taken), ", ".join("%s %d" % kv for kv in sorted(taken_class.items())) or "none",
                                                                                     ", ".join("%s %d" % kv for kv in sorted(taken_admiral.items())) or "none"))
        for rid, cls, closed, admirals in rows:
            print("  %-46s %-6s closed to %s; in the plans of %s" % (rid[:46], cls, ", ".join(closed), ", ".join(admirals) or "nobody"))
        for role, rid, cls in taken:
            print("  CLASS %-9s %-40s now %s: %s' work" % (role, rid[:40], cls, " and ".join(r + "s" for r in class_roles(True).get(cls, ("every role",)))))
        return 0
    for state in states:
        if both:
            print("%s:" % label(state))
        for role, ids in plans.items():
            other = [rid for rid in ids if rid in routes and not own(role, routes[rid], rid, state)]
            print("%-9s %3d routes in its plan, %d of another class%s" % (role, len(ids), len(other), (": " + ", ".join(other)) if other else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
