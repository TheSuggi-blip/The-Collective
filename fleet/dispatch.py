#!/usr/bin/env python3
"""dispatch.py -- keep every pilot at work: give each free pilot the next task of its role.

WHAT: every 30 s it reads the fleet's live files, the plan (routes/plan.json) and
      the route files (routes/<id>.json), and starts one runner per free pilot:
        circuit  -> fleet/route_run.py   stops with missions, buying and selling
        hunt     -> fleet/hunt.py        grazers at one place, loot, sell
        census   -> fleet/census.py      read one system whole (the stalest first)
        mine     -> fleet/mine.py        the engine's mining loop for a set time
      A pilot's role is the word before the dash of its name; the plan lists,
      per role, route ids in the order they are tried.
RULES:
  - A pilot is free when it is connected, the engine runs no loop and no goal
    for it, and it carries no fresh order file (data/fleet/orders/<pilot>.json:
    written by every runner, so two programs never drive one pilot).
  - The file data/fleet/STOP halts every start.
  - A route is skipped for a pilot when: it is `once` and the pilot has done it
    (or tried it twice); `max_ships` pilots fly it already; the pilot lacks a
    module the route `requires` or has fewer credits than `min_credits`; a hunt's
    place rests after a run without a kill (`rest_minutes`, default 30) or its
    last census (younger than 90 minutes) shows fewer than `min_creatures`; a
    census has no system older than `every_minutes` (default 60).
  - It sends no command to the game itself: the runners do.
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
import subprocess
import sys
import time
from pathlib import Path

EVERY = 30                   # seconds between two passes
ORDER_FRESH = 20 * 60        # an order file not touched for this long is dead
CENSUS_FRESH = 90 * 60       # a census older than this says nothing about a herd
KINDS = {"circuit": "route_run.py", "hunt": "hunt.py", "census": "census.py", "mine": "mine.py"}


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def load_routes(root):
    """{route id: route} from routes/<id>.json; plan.json is not a route."""
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


def done_once(route, rows):
    """A `once` route counts as done after a whole run, or after two tries."""
    if not rows:
        return False
    whole = [r for r in rows if r.get("stops") == r.get("of")]          # it went all the way round
    return bool(whole) or len(rows) >= 2


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


def pick(pilot, plan, routes, state):
    """(route, argument) for the first route of the pilot's role that is open to it, or (None, None)."""
    role = pilot["name"].split("-")[0]
    for rid in (plan.get("roles") or {}).get(role) or []:
        route = routes.get(rid)
        if not route or route.get("status") == "off":
            continue
        if route.get("once") and done_once(route, [r for r in state["rows"] if r.get("route") == rid and r.get("pilot") == pilot["name"]]):
            continue
        mark = "census " if route["kind"] == "census" else route["kind"] + " " + rid
        flying = sum(1 for what in state["orders"].values() if (what.startswith(mark) if route["kind"] == "census" else what == mark))
        if flying >= route.get("max_ships", 10 ** 6):
            continue
        if pilot.get("credits", 0) < route.get("min_credits", 0):
            continue
        need = (route.get("requires") or {}).get("module")
        if need and need not in pilot.get("modules", []):
            continue
        if state["now"] < state["rest"].get(rid, 0):
            continue
        if route["kind"] == "hunt":
            count = herd(state["data"], route, state["now"])
            if count is not None and count < route.get("min_creatures", 1):
                continue
        if route["kind"] == "census":
            system = stalest_system(state["data"], route, state["orders"], state["now"])
            if system is None:
                continue
            return route, system
        return route, None
    return None, None


def command(route, pilot, argument, root):
    """The runner's command line for one task."""
    here = str(Path(root) / "fleet")
    base = [sys.executable, "-I", "-B", os.path.join(here, KINDS[route["kind"]]), pilot]
    if route["kind"] == "circuit":
        return base + [str(Path(root) / "routes" / (route["id"] + ".json"))]
    if route["kind"] == "census":
        return base + [argument, "--stay", "--route", route["id"]]
    if route["kind"] == "mine":
        return base + [route["belt"], route["station"], "--minutes", str(route.get("minutes", 45)), "--route", route["id"]]
    system, poi = route["place"].split(":")
    out = base + [system, poi, "--kills", str(route.get("kills", 8)), "--minutes", str(route.get("minutes", 40)),
                  "--min-bid", str(route.get("min_bid", 100)), "--sell-at", route["sell_at"], "--route", route["id"]]
    out += ["--max-prey-hull", str(route["max_prey_hull"])] if route.get("max_prey_hull") else []
    return out + (["--species", ",".join(route["species"])] if route.get("species") else [])


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
    plan = read_json(Path(root) / "routes" / "plan.json", {})
    routes = load_routes(root)
    rows = run_rows(data)
    state = {"now": now, "data": data, "rows": rows, "orders": fresh_orders(data, now), "rest": resting(routes, rows, now)}
    lines = []
    for ship in fleet.get("ships") or []:
        name = ship.get("name") or ""
        if ship.get("status") != "connected" or name in state["orders"] or (ship.get("activity") or {}).get("kind") != "idle":
            continue
        detail = read_json(Path(data) / "fleet" / "ships" / (name + ".json"), {})
        pilot = {"name": name, "credits": ship.get("credits", 0), "modules": [m.get("type") or m.get("type_id") for m in detail.get("modules") or [] if isinstance(m, dict)]}
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
            children.append(subprocess.Popen(command(route, name, argument, root), stdout=log, stderr=subprocess.STDOUT, start_new_session=True))
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
