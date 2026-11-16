#!/usr/bin/env python3
"""dispatch.py -- keep every pilot at work: give each free pilot the next task of its role.

WHAT: every 30 s it reads the fleet's live files, the plans (game/routes/plans/<role>.json) and
      the route files (game/routes/<id>.json), and starts one runner per free pilot:
        circuit  -> game/fleet/route_run.py   stops with missions, buying and selling
        hunt     -> game/fleet/hunt.py        grazers at one place, loot, sell
        census   -> game/fleet/census.py      read one system whole (the stalest first)
        mine     -> game/fleet/mine.py        the engine's mining loop for a set time
      A pilot's role is the word before the dash of its name; its role's plan
      file lists route ids in the order they are tried, and the role's
      Admiral keeps that file (division.py). A flagship's name has
      no role word: its role is in data/fleet/flagships.json
      ({pilot: {admiral, division, role}}).
RULES:
  - A pilot is free when it is connected, the engine runs no loop and no goal
    for it, and it carries no fresh order file (data/fleet/orders/<pilot>.json:
    written by every runner, so two programs never drive one pilot).
  - The file data/fleet/STOP halts every start.
  - A pilot with no open route is left where it is. Every plan ends with the
    `park` route (dock at home and wait): it is given to a pilot in space and
    never to a docked one, so a fleet without paying work costs nothing.
  - A real pass is the service's or the Fleet Admiral's; --dry-run is free.
  - A route is skipped for a pilot when: it is a `park` route and the pilot is
    docked; the pilot has a reward booked (data/fleet/onetime.json) that the
    route lists under `skip_if_booked`; it is `once` and the pilot has done it
    (or tried it twice; a run that found nothing to buy is no try, the route rests `retry_minutes`, default 60); `max_ships` pilots fly it already; the pilot lacks a
    module the route `requires` or has fewer credits than `min_credits`; a hunt's
    place rests after a run without a kill (`rest_minutes`, default 30) or its
    last census (younger than 90 minutes) shows fewer than `min_creatures`; a
    census has no system older than `every_minutes` (default 60).
  - It sends no command to the game itself: the runners do.
  - No route flies at a loss unattended: a route whose runs of the last six hours (two or more) lost money in sum is
    closed until the window moves on (`losing`); the census, park and fitting routes are not judged.
  - Why ships wait, and what would give them work: game/fleet/fill.py, which uses this script's own rule.
WHY:  no ship waits for a hand to give it work, and a new ship climbs the same
      ladder as the ones before it: what we learned is in the route files.

USAGE:
  dispatch.py              run forever (the service `dispatch`)
  dispatch.py --once       one pass
  dispatch.py --dry-run    one pass that starts nothing and prints what it would start
  --root <dir>   repository root (default: the parent of this file's folder)
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import argparse
import calendar
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  who commands which ship, and the plan files

EVERY = 30                   # seconds between two passes
ORDER_FRESH = 20 * 60        # an order file not touched for this long is dead
CENSUS_FRESH = 90 * 60       # a census older than this says nothing about a herd
KINDS = {"circuit": "route_run.py", "hunt": "hunt.py", "census": "census.py", "mine": "mine.py"}


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def flagships(data):
    """{pilot: {admiral, division, role}} from data/fleet/flagships.json: the ships whose names carry no role word."""
    found = read_json(Path(data) / "fleet" / "flagships.json", {})
    return {name: entry for name, entry in found.items() if isinstance(entry, dict)} if isinstance(found, dict) else {}


def role_of(name, ships):
    """A pilot's role: the one its flagship entry names, else the word before the dash of its name."""
    entry = ships.get(name)
    return str(entry.get("role") or "") if entry else name.split("-")[0]


def ship_file(name):
    """The name of a pilot's live file, by the fleet collector's rule (station/fleet.py, file_name)."""
    return (re.sub(r"[^A-Za-z0-9_.-]", "_", name)[:60] or "pilot") + ".json"


def load_routes(root):
    """{route id: route} from game/routes/<id>.json; plan.json is not a route."""
    out = {}
    for path in sorted((Path(root) / "routes").glob("*.json")):
        if path.name == "plan.json":
            continue
        route = read_json(path, None)
        if isinstance(route, dict) and route.get("id") == path.stem and route.get("kind") in KINDS:
            out[route["id"]] = route
    return out


def fresh_orders(data, now):
    """{pilot: what} for the order files a runner still touches."""
    out = {}
    folder = Path(data) / "fleet" / "orders"
    for path in folder.glob("*.json") if folder.is_dir() else []:
        try:
            if now - path.stat().st_mtime <= ORDER_FRESH:
                out[path.stem] = str(read_json(path, {}).get("what") or "")
        except OSError:
            continue
    return out


def run_rows(data):
    rows = []
    try:
        with open(Path(data) / "routes" / "runs.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        pass
    return rows


def booked(data):
    """{pilot: titles of the one-time rewards booked for it} from data/fleet/onetime.json."""
    out = {}
    for row in read_json(Path(data) / "fleet" / "onetime.json", []):
        if isinstance(row, list) and len(row) >= 3:
            out.setdefault(str(row[1]), set()).add(str(row[2]))
    return out


NO_BUY = (": not bought", ": not fitted", ": wallet floor")


def unfinished(row):
    """A run that went all the way round and did not get what it came to buy or fit: no finished run of a `once` route."""
    return row.get("stops") == row.get("of") and any(str(note).endswith(NO_BUY) for note in row.get("notes") or [])


NOT_OFFERED = " not offered"
REFUSALS = 3                   # runs a board may refuse on a route with `requires.booked` before the route counts as done for the pilot


def refused(row):
    """A run that went all the way round while the board did not offer its mission."""
    return row.get("stops") == row.get("of") and any(str(note).endswith(NOT_OFFERED) for note in row.get("notes") or [])


def owed(route):
    """The rewards a pilot must hold before the route is open to it (`requires.booked`: one title or a list)."""
    need = (route.get("requires") or {}).get("booked")
    return [need] if isinstance(need, str) else [str(t) for t in need or []]


def done_once(route, rows):
    """A `once` route counts as done after a whole run that got what it came for, or after two tries. A run that found
    nothing to buy is neither: the route opens again for that pilot after a rest (waits_once). On a route that names a
    reward the pilot must hold first (`requires.booked`), a run the board refused is no try either, up to REFUSALS times:
    the pilot flew it before it held that reward. Without `requires.booked` a refusal stays a finished run: a mission
    done once is never offered again."""
    rows = [r for r in rows if not unfinished(r)]
    if owed(route) and sum(1 for r in rows if refused(r)) <= REFUSALS:
        rows = [r for r in rows if not refused(r)]
    if not rows:
        return False
    whole = [r for r in rows if r.get("stops") == r.get("of")]          # it went all the way round
    return bool(whole) or len(rows) >= 2


def waits_once(route, rows, now):
    """True while a `once` route rests for a pilot: its last run found nothing to buy less than retry_minutes (default 60) ago."""
    if not rows or not (unfinished(rows[-1]) or (owed(route) and refused(rows[-1]))):
        return False
    try:
        ended = calendar.timegm(time.strptime(rows[-1]["started"], "%Y-%m-%dT%H:%M:%SZ")) + rows[-1].get("minutes", 0) * 60
    except (KeyError, ValueError):
        return False
    return now < ended + route.get("retry_minutes", 60) * 60


def herd(data, route, now):
    """Creatures of the route's species at its place per the last census; None when no fresh census exists."""
    system, poi = route["place"].split(":")
    path = Path(data) / "wildlife" / (system + ".json")
    try:
        if now - path.stat().st_mtime > CENSUS_FRESH:
            return None
    except OSError:
        return None
    place = (read_json(path, {}).get("pois") or {}).get(poi) or {}
    try:                                              # the place's own reading time: a hunter that left writes only its place
        if now - calendar.timegm(time.strptime(str(place.get("read_at"))[:19], "%Y-%m-%dT%H:%M:%S")) > CENSUS_FRESH:
            return None
    except ValueError:
        pass
    species = set(route.get("species") or [])
    return sum(1 for c in place.get("creatures") or [] if not species or c.get("species") in species)


def stalest_system(data, route, orders, now):
    """The system of a census route read longest ago and not being read now; None when all are fresh."""
    busy = {what.split(" ", 1)[1] for what in orders.values() if what.startswith("census ")}
    best = None
    for system in route.get("systems") or []:
        if system in busy:
            continue
        try:
            age = now - (Path(data) / "scouting" / (system + ".json")).stat().st_mtime
        except OSError:
            age = float("inf")
        if age >= route.get("every_minutes", 60) * 60 and (best is None or age > best[0]):
            best = (age, system)
    return best[1] if best else None


def why_not(pilot, rid, route, state):
    """(why the route is closed to the pilot now, or None when it is open; for an open census the system to read).
    The one rule: pick() and fill.py both use it."""
    if not route:
        return "no route file", None
    if route.get("status") == "off":
        return "off", None
    if route.get("park") and pilot.get("docked"):
        return "the pilot is docked", None
    lost = (state.get("loss") or {}).get(rid)
    if lost:
        return "at a loss: %d runs, %s cr in %d hours" % (lost[0], format(lost[1], ","), LOSS_HOURS), None
    if set(route.get("skip_if_booked") or []) & (state.get("booked") or {}).get(pilot["name"], set()):
        return "its reward is booked", None
    lacks = [title for title in owed(route) if title not in (state.get("booked") or {}).get(pilot["name"], set())]
    if lacks:
        return "needs the reward `%s` first" % lacks[0], None
    if route.get("once"):
        mine = [r for r in state["rows"] if r.get("route") == rid and r.get("pilot") == pilot["name"]]
        if done_once(route, mine):
            return "done once", None
        if waits_once(route, mine, state["now"]):
            return ("rests after a run the board refused" if refused(mine[-1]) else "rests after a buy that found no offer"), None
    mark = route["kind"] + " " + rid
    if route.get("max_pilots"):                   # at most this many different pilots ever: those that flew it and those on it now
        flew = {r.get("pilot") for r in state["rows"] if r.get("route") == rid} | {p for p, what in state["orders"].items() if what == mark}
        if pilot["name"] not in flew and len(flew) >= route["max_pilots"]:
            return "max_pilots %s reached" % route["max_pilots"], None
    if route["kind"] == "census":                 # a census order names its system: it counts for the route that lists that system
        systems = set(route.get("systems") or [])
        flying = sum(1 for what in state["orders"].values() if what.startswith("census ") and what.split(" ", 1)[1] in systems)
    else:
        flying = sum(1 for what in state["orders"].values() if what == mark)
    if flying >= route.get("max_ships", 10 ** 6):
        return "max_ships %s reached" % route["max_ships"], None
    if pilot.get("credits", 0) < route.get("min_credits", 0):
        return "wallet below %s cr" % route["min_credits"], None
    need = (route.get("requires") or {}).get("module")
    if need and need not in pilot.get("modules", []):
        return "needs " + need, None
    if (route.get("requires") or {}).get("empty_hold") and pilot.get("goods", 0) > 5:      # nothing to lose aboard (orders F13); five units count as nothing
        return "hold not empty", None
    if (route.get("requires") or {}).get("without_module") in pilot.get("modules", []):     # the route fits this module: not for a pilot that has it
        return "has the module already", None
    if state["now"] < state["rest"].get(rid, 0):
        return "the place rests", None
    if route["kind"] == "hunt":
        count = herd(state["data"], route, state["now"])
        if count is not None and count < route.get("min_creatures", 1):
            return "herd below %s" % route.get("min_creatures", 1), None
    if route["kind"] == "census":
        system = stalest_system(state["data"], route, state["orders"], state["now"])
        if system is None:
            return "every system read", None
        return None, system
    return None, None


def pick(pilot, plan, routes, state):
    """(route, argument) for the first route of the pilot's role that is open to it, or (None, None)."""
    role = pilot.get("role") or pilot["name"].split("-")[0]
    for rid in (plan.get("roles") or {}).get(role) or []:
        reason, argument = why_not(pilot, rid, routes.get(rid), state)
        if reason is None:
            return routes[rid], argument
    return None, None


def pilot_of(ship, named, data, ammo):
    """What the rule needs to know of one pilot, from its row in fleet.json and its live file: role, wallet, docked, modules, goods aboard."""
    name = ship.get("name") or ""
    detail = read_json(Path(data) / "fleet" / "ships" / ship_file(name), {})
    return {"name": name, "role": role_of(name, named), "credits": ship.get("credits", 0), "docked": bool(ship.get("docked")),
            "modules": [m.get("type") or m.get("type_id") for m in detail.get("modules") or [] if isinstance(m, dict)],
            "goods": sum(int(c.get("quantity") or 0) for c in detail.get("cargo") or [] if isinstance(c, dict) and c.get("item") not in ammo)
            if isinstance(detail.get("cargo"), list) else int(ship.get("cargo_used") or 0)}


def command(route, pilot, argument, root):
    """The runner's command line for one task."""
    here = str(Path(root) / "fleet")
    base = [sys.executable, "-I", "-B", os.path.join(here, KINDS[route["kind"]]), pilot]
    if route["kind"] == "circuit":
        return base + [str(Path(root) / "routes" / (route["id"] + ".json"))]
    if route["kind"] == "census":
        return base + [argument, "--stay", "--route", route["id"]]
    if route["kind"] == "mine":
        sell = ",".join("%s:%d" % (s["item"], s["min_price"]) for s in route.get("sell") or [])
        return base + [route["belt"], route["station"], "--minutes", str(route.get("minutes", 45)), "--route", route["id"]] + (["--sell-items", sell] if sell else [])
    system, poi = route["place"].split(":")
    out = base + [system, poi, "--kills", str(route.get("kills", 8)), "--minutes", str(route.get("minutes", 40)),
                  "--min-bid", str(route.get("min_bid", 100)), "--sell-at", route["sell_at"], "--route", route["id"]]
    out += ["--max-prey-hull", str(route["max_prey_hull"])] if route.get("max_prey_hull") else []
    out += ["--alone"] if route.get("alone") else []
    return out + (["--species", ",".join(route["species"])] if route.get("species") else [])


LOSS_HOURS = 6               # the window a route's runs are judged over


def judged(route):
    """True for a route whose runs must pay: not the census, not park, not a fitting (a tool is bought once)."""
    if route.get("park") or route.get("kind") == "census":
        return False
    return not any(isinstance(stop, dict) and stop.get("fit") for stop in route.get("stops") or [])


def losing(routes, rows, now):
    """{route id: (runs, credits)} of the routes that lost money over their runs of the last LOSS_HOURS: two runs or
    more that read a wallet, negative in sum. A repeating route is summed without the money booked once (a reward, a
    tool); a route that pays once is summed with it, since its reward is its pay. Such a route is closed to every
    pilot until the window moves on: no route flies at a loss unattended (orders F8)."""
    sums = {}
    for row in rows:
        before, after = row.get("credits_before"), row.get("credits_after")
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (before, after)) or not (before > 0 and after > 0):
            continue                                              # the run read no wallet at one end: it says nothing about credits
        try:
            started = calendar.timegm(time.strptime(row.get("started") or "", "%Y-%m-%dT%H:%M:%SZ"))
        except ValueError:
            continue
        route = routes.get(row.get("route"))
        if route is None or started < now - LOSS_HOURS * 3600 or not judged(route):
            continue
        entry = sums.setdefault(route["id"], [0, 0])
        entry[0] += 1
        entry[1] += (after - before) - (0 if route.get("once") else (row.get("one_time") or 0))
    return {rid: (runs, int(total)) for rid, (runs, total) in sums.items() if runs >= 2 and total < 0}


def resting(routes, rows, now):
    """{route id: time before which a hunt's place rests}: its last run ended without a kill."""
    out = {}
    for rid, route in routes.items():
        if route["kind"] != "hunt":
            continue
        last = next((r for r in reversed(rows) if r.get("route") == rid), None)
        if last and not last.get("kills"):
            try:
                ended = calendar.timegm(time.strptime(last["started"], "%Y-%m-%dT%H:%M:%SZ")) + last.get("minutes", 0) * 60
            except (KeyError, ValueError):
                continue
            out[rid] = ended + route.get("rest_minutes", 30) * 60
    return out


def one_pass(root, data, dry_run, children):
    now = time.time()
    if (Path(data) / "fleet" / "STOP").exists():
        return ["STOP file present: nothing started"]
    fleet = read_json(Path(data) / "fleet" / "fleet.json", {})
    plan = {"roles": division.load_plan(root)[0]}
    routes = load_routes(root)
    rows = run_rows(data)
    state = {"now": now, "data": data, "rows": rows, "orders": fresh_orders(data, now), "rest": resting(routes, rows, now), "booked": booked(data),
             "loss": losing(routes, rows, now)}
    named = flagships(data)
    ammo = set(read_json(Path(data) / "catalog" / "ammo.json", []) or [])      # written by routemaker.py from the game's catalog
    lines = []
    for ship in fleet.get("ships") or []:
        name = ship.get("name") or ""
        if ship.get("status") != "connected" or name in state["orders"] or (ship.get("activity") or {}).get("kind") != "idle":
            continue
        pilot = pilot_of(ship, named, data, ammo)
        route, argument = pick(pilot, plan, routes, state)
        if route is None:
            continue
        what = ("census " + argument) if route["kind"] == "census" else route["kind"] + " " + route["id"]
        state["orders"][name] = what
        lines.append("%s -> %s" % (name, what))
        if dry_run:
            continue
        orders = Path(data) / "fleet" / "orders"
        orders.mkdir(parents=True, exist_ok=True)
        (orders / (name + ".json")).write_text(json.dumps({"pilot": name, "what": what, "since": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))}), encoding="utf-8")
        logs = Path(data) / "routes" / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        with open(logs / (name + ".log"), "w", encoding="utf-8") as log:
            mark = dict(os.environ, FLEET_MEMBER=os.environ.get("FLEET_MEMBER") or "dispatch", FLEET_HOLD=what)    # the runner is the dispatcher's: division.py lets it pass
            children.append(subprocess.Popen(command(route, name, argument, root), stdout=log, stderr=subprocess.STDOUT, start_new_session=True, env=mark))
    children[:] = [c for c in children if c.poll() is None]          # reap the runners that ended
    return lines


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Give each free pilot the next task of its role.")
    parser.add_argument("--root", default=str(here.parent))
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    kind, name = division.member()
    if not args.dry_run and not (kind == "service" or name == "Unity"):
        sys.exit("REFUSED: a real pass starts runners for every division: it is the service's or the Fleet Admiral's. Use --dry-run.")
    children = []
    while True:
        try:
            lines = one_pass(args.root, args.data, args.dry_run, children)
        except Exception as error:                               # a bad file must not end the service
            lines = ["pass failed: %s: %s" % (type(error).__name__, error)]
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for line in lines:
            print(stamp, line, flush=True)
        if not args.dry_run:
            state = {"updated_at": stamp, "running": len(children), "started": lines}
            try:
                tmp = Path(args.data) / "fleet" / "dispatch.json.tmp"
                tmp.write_text(json.dumps(state), encoding="utf-8")
                os.replace(tmp, Path(args.data) / "fleet" / "dispatch.json")
            except OSError:
                pass
        if args.once or args.dry_run:
            return 0
        time.sleep(EVERY)


if __name__ == "__main__":
    sys.exit(main())
