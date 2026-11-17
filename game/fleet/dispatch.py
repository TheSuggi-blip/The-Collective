#!/usr/bin/env python3
"""dispatch.py -- keep every pilot at work: give each free pilot the next task of its role.

WHAT: every 30 s it reads the fleet's live files, the plans (game/routes/plans/<role>.json) and
      the route files (game/routes/<id>.json), and starts one runner per free pilot:
        circuit  -> game/fleet/route_run.py   stops with missions, buying and selling
        hunt     -> game/fleet/hunt.py        grazers at one place, loot, sell
        census   -> game/fleet/census.py      read one system whole (the stalest first)
        mine     -> game/fleet/mine.py        the engine's mining loop for a set time
        guard    -> game/fleet/guard.py       one ship at the place where another route's ship of ours works
      A pilot's role is the word before the dash of its name. A pilot flies its
      own list of routes in its order: data/plans/assign.json, written by
      plan.py from its division's plan file, which its Admiral keeps. A pilot
      that file does not name flies its role's list
      (game/routes/plans/<role>.json). A flagship's name has
      no role word: its role is in data/fleet/flagships.json
      ({pilot: {admiral, division, role}}).
RULES:
  - A pilot is free when it is connected, the engine runs no loop and no goal
    for it, and it carries no fresh order file (data/fleet/orders/<pilot>.json:
    written by every runner, so two programs never drive one pilot).
  - The file data/fleet/STOP halts every start.
  - A pilot under 5,000 cr is sent only on work that pays (a mission that pays once, a route measured paying, park);
    wallet.py tops its wallet up from a rich ship of its division.
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
    last census (younger than 90 minutes) shows fewer than `min_creatures`, and a
    circuit's hunt step that names `min_creatures` is judged the same way; the
    station's book, read within the hour, shows no bid the route names in
    `requires.bid` (item, base, min_price, min_qty); the pilot's own storage at a
    station holds less than `requires.stored` asks (at, item, min), or was not
    read again since the pilot's last run of the route; a once run whose every stop
    was skipped (`every stop skipped`) is no try and the route rests; a
    census has no system older than `every_minutes` (default 60); a guard sees no pilot of
    ours on the route it guards (`nobody flies <id>`); a guard route without `max_ships`
    takes one ship.
  - An engine loop that runs for a pilot with no fresh order file for five
    minutes belongs to no runner (an engine restart, a dead runner): the
    dispatcher stops that loop through the gate and names it in its log.
  - It sends no command to the game itself: the runners do.
  - A runner is started as a process of its own, or handed to the run host (game/fleet/runhost.py: one
    program that flies runs as threads, under 1 MB a waiting run where a process holds 13 MB) when
    data/fleet/hosting.json names the route's kind: {"kinds": ["mine", ...], "max_runs": N}. Without that
    file, with a host that is away, draining or at `max_runs`, the run is a process as before. A job the
    host did not take within a minute is taken back and started as a process.
  - No route flies at a loss unattended: a route whose runs of the last six hours (two or more) lost money in sum is
    closed until the window moves on (`losing`), and so is a repeating route whose last three runs inside those six
    hours each lost money (`lately_losing`); the census, park and fitting routes are not judged.
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
import gate                                       # noqa: E402  the one call the dispatcher sends itself: stop a loop no runner owns
import runhost                                    # noqa: E402  the program that flies hosted runs as threads
import routes as routefiles                       # noqa: E402  what standing work is
import taxes                                      # noqa: E402  the weekly tax a run in flight carried is no loss of its route

EVERY = 30                   # seconds between two passes
ORDER_FRESH = 20 * 60        # an order file not touched for this long is dead
CENSUS_FRESH = 90 * 60       # a census older than this says nothing about a herd
KINDS = {"circuit": "route_run.py", "hunt": "hunt.py", "census": "census.py", "mine": "mine.py", "guard": "guard.py"}


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
EMPTY_RUN = "every stop skipped"   # route_run.py: the pilot held none of the missions its stops wait for, and did nothing


def empty(row):
    """A run whose every stop was skipped by `only_if_active`: the pilot did nothing (requests ENT-129)."""
    return EMPTY_RUN in (row.get("notes") or [])


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


def skills_lacking(route, pilot):
    """[(skill, level)] the route asks for (`requires.skills`: {skill: level}) that the pilot does not hold yet: a board
    that offers a mission only from a skill level (Signal Fragments: navigation 3) refuses every other pilot."""
    need = (route.get("requires") or {}).get("skills") or {}
    held = pilot.get("skills") or {}
    return [(str(skill), int(level)) for skill, level in sorted(need.items()) if int(held.get(skill, 0) or 0) < int(level)]


STUCK = 3                      # runs in a row that ended before their first stop: the pilot rests before it gets a route again
STUCK_REST = 30 * 60           # seconds of that rest, counted from the end of the last of those runs


def stuck(name, rows, now=None):
    """True when the pilot's last STUCK runs all ended `stop 1 not reached` and the last of them ended less than STUCK_REST
    seconds before `now`: a ship held in a fight or a lost goal would otherwise be handed one route after another, each
    failing at once (requests ENT-090: 42 park runs in an hour). After the rest it is given one route again, so the hold
    ends by itself when its cause is gone: until 2026-11-17 it ended only with a run that reached a stop, which a held
    pilot never got, and two ships the engine had held claimed stood for two hours and waited for a hand. Without `now`,
    or with a last run whose time does not read, the rest is not counted."""
    mine = [r for r in rows if r.get("pilot") == name][-STUCK:]
    if len(mine) != STUCK or not all("stop 1 not reached" in (r.get("notes") or []) for r in mine):
        return False
    if now is None:
        return True
    try:
        ended = calendar.timegm(time.strptime(mine[-1]["started"], "%Y-%m-%dT%H:%M:%SZ")) + float(mine[-1].get("minutes") or 0) * 60
    except (KeyError, TypeError, ValueError):
        return True
    return now - ended < STUCK_REST


def done_once(route, rows):
    """A `once` route counts as done after a whole run that got what it came for, or after two tries. A run that found
    nothing to buy is neither: the route opens again for that pilot after a rest (waits_once). On a route that names a
    reward the pilot must hold first (`requires.booked`), a run the board refused is no try either, up to REFUSALS times:
    the pilot flew it before it held that reward. Without `requires.booked` a refusal stays a finished run: a mission
    done once is never offered again."""
    rows = [r for r in rows if not unfinished(r) and not empty(r)]
    if owed(route) and sum(1 for r in rows if refused(r)) <= REFUSALS:
        rows = [r for r in rows if not refused(r)]
    if not rows:
        return False
    whole = [r for r in rows if r.get("stops") == r.get("of")]          # it went all the way round
    return bool(whole) or len(rows) >= 2


def waits_once(route, rows, now):
    """True while a `once` route rests for a pilot: its last run found nothing to buy less than retry_minutes (default 60) ago."""
    if not rows or not (unfinished(rows[-1]) or empty(rows[-1]) or (owed(route) and refused(rows[-1]))):
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


def hunt_floor(data, route, now):
    """Why a circuit is closed by the herd floor of one of its hunt steps (`min_creatures` in a stop's `hunt`), or None:
    the place's fresh census counts fewer of the step's species. Apophis, his report of 2026-11-16 05:27 UTC and
    requests ENT-126: Cracking the Shell flew five runs to an ice field that held no pressblister."""
    for stop in route.get("stops") or []:
        for step in (stop.get("hunt") or []) if isinstance(stop, dict) else []:
            if isinstance(step, dict) and step.get("min_creatures") and step.get("at"):
                count = herd(data, {"place": step["at"], "species": step.get("species")}, now)
                if count is not None and count < int(step["min_creatures"]):
                    return "herd below %s at %s" % (step["min_creatures"], step["at"])
    return None


def field_left(data, place, now, fresh=CENSUS_FRESH):
    """{resource: units left} at a place (system:poi) by the system's last census; None when none younger than `fresh`
    seconds holds the place."""
    system, poi = (str(place).split(":") + [""])[:2]
    book = read_json(Path(data) / "scouting" / (system + ".json"), {})
    entry = (book.get("pois") or {}).get(poi) if isinstance(book, dict) and isinstance(book.get("pois"), dict) else None
    read = read_time(book.get("read_at")) if isinstance(book, dict) else None
    if read is None or now - read > fresh or not isinstance(entry, dict):
        return None
    rows = entry.get("resources") or (entry.get("poi") or {}).get("resources") or []
    return {str(r.get("resource_id")): int(r.get("remaining") or 0) for r in rows if isinstance(r, dict) and r.get("resource_id")}


def field_floor(data, route, now):
    """Why a route is closed by a field floor (`min_left`: {resource: units}; on a mine route for its `belt`, on a `mine`
    step of a circuit for the step's place), or None: the place's fresh census reads less of the resource. The route
    opens again by itself when a census reads the field grown back. Mercury, requests ENT-148: a mission mined a reef
    that read 0 and pilots kept flying to it; and standing work leaves its field enough to regrow."""
    steps = [route] if route.get("kind") == "mine" else [step for stop in route.get("stops") or [] if isinstance(stop, dict) for step in stop.get("mine") or []]
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get("min_left"), dict):
            continue
        place = step.get("belt") or step.get("at") or ""
        left = field_left(data, place, now) if len(str(place).split(":")) == 2 else None
        if left is None:
            continue
        for item, units in sorted(step["min_left"].items()):
            if left.get(item, 0) < int(units):
                return "field below %s %s at %s" % (format(int(units), ","), item, place)
    return None


def skills_reached(route, pilot):
    """The text of `requires.skills_below` ({skill: level}) when the pilot holds every skill named at its level or above,
    or None: a route that trains a skill up to a board's gate is flown only by a pilot still short of it (Apophis and
    Apollo, requests ENT-150, ENT-151: Signal Fragments is offered from navigation 3)."""
    below = (route.get("requires") or {}).get("skills_below") or {}
    held = pilot.get("skills") or {}
    if below and all(int(held.get(skill, 0) or 0) >= int(level) for skill, level in below.items()):
        return ", ".join("%s %d" % (skill, int(level)) for skill, level in sorted(below.items()))
    return None


BID_FRESH = 60 * 60          # a book older than this says nothing about a bid
FLOOR = 5000                 # a pilot under this many credits is sent only on work that pays (Suggi: no ship goes broke)


def read_time(text):
    """Seconds since the epoch of a UTC time written YYYY-MM-DDTHH:MM:SS..., or None."""
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return None


def bids(route):
    """The bids a route sells into (`requires.bid`: one {item, base, min_price, min_qty} or a list of them)."""
    need = (route.get("requires") or {}).get("bid")
    return [need] if isinstance(need, dict) else [b for b in need or [] if isinstance(b, dict)]


def bid_missing(data, route, now):
    """Why a route is closed by `requires.bid`, or None: the station's book, read by a docked ship of ours within
    BID_FRESH, shows the item's best bid under `min_price` (default 1) or fewer than `min_qty` units (default 1) at it.
    A book older than that says nothing and closes nothing. Requests ENT-065 and ENT-125, errors ENT-046: the curd bid
    left seven stations and the veil-ray hunts flew on at a loss for two hours; the ice bids near the fields emptied
    and 36 mine runs stored their ice."""
    for want in bids(route):
        book = read_json(Path(data) / "market" / (str(want.get("base")) + ".json"), {})
        read = read_time(book.get("read_at")) if isinstance(book, dict) else None
        if read is None or now - read > BID_FRESH:
            continue
        row = next((i for i in book.get("items") or [] if isinstance(i, dict) and i.get("item_id") == want.get("item")), {})
        price, depth = int(row.get("best_buy") or 0), int(row.get("best_buy_qty") or 0)
        if price < int(want.get("min_price") or 1) or depth < int(want.get("min_qty") or 1):
            return "no bid for %s at %s: best %d cr x %d" % (want.get("item"), want.get("base"), price, depth)
    return None


def stored_missing(data, route, pilot, rows):
    """Why a route is closed by `requires.stored`, or None: the pilot's own storage at the station named (`at`, a base
    id) holds fewer than `min` units of `item` by data/stock/storage.json (the service ledger reads each pilot about
    every 40 minutes), or that storage was not read again since the pilot's last run of this route began: a carry
    run takes the load out, and the old reading must not send the pilot a second time. Storage is personal: only the
    pilot that stored a load can withdraw it (Zero, requests ENT-117: about 11,100 water ice in miners' storage at
    stations whose bids are gone)."""
    need = (route.get("requires") or {}).get("stored")
    wants = [need] if isinstance(need, dict) else [w for w in need or [] if isinstance(w, dict)]
    if not wants:
        return None
    book = read_json(Path(data) / "stock" / "storage.json", {})
    mine = ((book.get("pilots") or {}) if isinstance(book, dict) else {}).get(pilot["name"]) or {}
    read = read_time(mine.get("read_at"))
    last = max((read_time(r.get("started")) or 0 for r in rows if r.get("route") == route.get("id") and r.get("pilot") == pilot["name"]), default=0)
    for want in wants:
        held = int(((mine.get("stations") or {}).get(str(want.get("at"))) or {}).get(str(want.get("item")), 0) or 0)
        if held < int(want.get("min") or 1):
            return "stores %d %s at %s, %s wanted" % (held, want.get("item"), want.get("at"), want.get("min") or 1)
    if read is None or (last and read <= last):
        return "storage not read since its last run"
    return None


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
    late = (state.get("late") or {}).get(rid)
    if late:
        return "its last %d runs each lost money: %s cr" % (late[0], format(late[1], ",")), None
    if set(route.get("skip_if_booked") or []) & (state.get("booked") or {}).get(pilot["name"], set()):
        return "its reward is booked", None
    lacks = [title for title in owed(route) if title not in (state.get("booked") or {}).get(pilot["name"], set())]
    if lacks:
        return "needs the reward `%s` first" % lacks[0], None
    low = skills_lacking(route, pilot)
    if low:
        return "needs %s %d" % low[0], None
    reached = skills_reached(route, pilot)
    if reached:
        return "holds %s already" % reached, None
    if route.get("once"):
        mine = [r for r in state["rows"] if r.get("route") == rid and r.get("pilot") == pilot["name"]]
        if done_once(route, mine):
            return "done once", None
        if waits_once(route, mine, state["now"]):
            return ("rests after a run the board refused" if refused(mine[-1]) else
                    "rests after a run with every stop skipped" if empty(mine[-1]) else "rests after a buy that found no offer"), None
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
    limit = route.get("max_ships", 1 if route["kind"] == "guard" else 10 ** 6)     # one guard to a place unless its file says more
    if flying >= limit:
        return "max_ships %s reached" % limit, None
    place = None
    if route["kind"] == "guard":                  # it keeps a place only while a pilot of ours flies the route it guards (requests ENT-070)
        folder = Path(state.get("root") or Path(__file__).resolve().parent.parent) / "routes"      # fill.py's state names no root: the default one
        guarded = read_json(folder / (str(route.get("guards")) + ".json"), None)
        place = routefiles.guarded_place(route, guarded)
        if place is None:
            return "guards `%s`: no mine or hunt route file" % route.get("guards"), None
        if guarded["kind"] + " " + str(route["guards"]) not in state["orders"].values():
            return "nobody flies %s" % route["guards"], None
    if pilot.get("credits", 0) < route.get("min_credits", 0):
        return "wallet below %s cr" % route["min_credits"], None
    if pilot.get("credits", 0) < FLOOR and not (route.get("park") or routefiles.stage(route) in ("once", "paying")):
        return "wallet below %s cr: only work that pays" % format(FLOOR, ","), None     # no ship goes broke (wallet.py tops it up)
    need = (route.get("requires") or {}).get("module")
    if need and need not in pilot.get("modules", []):
        return "needs " + need, None
    if (route.get("requires") or {}).get("empty_hold") and pilot.get("goods", 0) > 5:      # nothing to lose aboard (orders F13); five units count as nothing
        return "hold not empty", None
    if (route.get("requires") or {}).get("hold") and pilot.get("goods", 0) <= 5:            # a route that stores what is aboard: not for a pilot that carries nothing
        return "nothing aboard", None
    if (route.get("requires") or {}).get("without_module") in pilot.get("modules", []):     # the route fits this module: not for a pilot that has it
        return "has the module already", None
    if state["now"] < state["rest"].get(rid, 0):
        return "the place rests", None
    lacking = bid_missing(state["data"], route, state["now"]) or stored_missing(state["data"], route, pilot, state["rows"])
    if lacking:
        return lacking, None
    if route["kind"] in ("circuit", "mine"):
        floor = (hunt_floor(state["data"], route, state["now"]) if route["kind"] == "circuit" else None) or field_floor(state["data"], route, state["now"])
        if floor:
            return floor, None
    if route["kind"] == "hunt":
        count = herd(state["data"], route, state["now"])
        if count is not None and count < route.get("min_creatures", 1):
            return "herd below %s" % route.get("min_creatures", 1), None
    if route["kind"] == "census":
        system = stalest_system(state["data"], route, state["orders"], state["now"])
        if system is None:
            return "every system read", None
        return None, system
    if route["kind"] == "guard":                  # the place it keeps, for its command line
        return None, place
    return None, None


def own_lists(data):
    """{pilot: its routes in order} as plan.py applied them (data/plans/assign.json); {} when there is none."""
    found = read_json(Path(data) / "plans" / "assign.json", {})
    pilots = found.get("pilots") if isinstance(found, dict) else None
    return {str(name): [str(rid) for rid in ids] for name, ids in pilots.items() if isinstance(ids, list)} if isinstance(pilots, dict) else {}


def pick(pilot, plan, routes, state):
    """(route, argument) for the first route open to the pilot, or (None, None): of its own list (`pilots` of the
    plan, from its division's plan file), or of its role's list when it has none."""
    role = pilot.get("role") or pilot["name"].split("-")[0]
    for rid in (plan.get("pilots") or {}).get(pilot["name"]) or (plan.get("roles") or {}).get(role) or []:
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
            "skills": {str(k): int((v or {}).get("level") or 0) if isinstance(v, dict) else int(v or 0)
                       for k, v in (detail.get("skills") or {}).items() if isinstance(v, (dict, int))} if isinstance(detail.get("skills"), dict) else {},
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
    if route["kind"] == "guard":                  # the place why_not found: the guard's own, else the guarded route's
        system, poi = (str(argument or route.get("place") or "") + ":").split(":")[:2]
        return base + [system, poi, "--guards", route["guards"], "--station", route["station"], "--minutes", str(route.get("minutes", 60)), "--route", route["id"]]
    system, poi = route["place"].split(":")
    out = base + [system, poi, "--kills", str(route.get("kills", 8)), "--minutes", str(route.get("minutes", 40)),
                  "--min-bid", str(route.get("min_bid", 100)), "--sell-at", route["sell_at"], "--route", route["id"]]
    out += ["--max-prey-hull", str(route["max_prey_hull"])] if route.get("max_prey_hull") else []
    out += ["--alone"] if route.get("alone") else []
    return out + (["--species", ",".join(route["species"])] if route.get("species") else [])


LOSS_HOURS = 6               # the window a route's runs are judged over


def judged(route):
    """True for a route whose runs must pay: not the census, not park, not a fitting (a tool is bought once), not
    standing work (it trains or gathers: its fuel is its price, routes.py `standing`)."""
    if route.get("park") or route.get("kind") == "census" or routefiles.standing(route):
        return False
    return not any(isinstance(stop, dict) and stop.get("fit") for stop in route.get("stops") or [])


RUNNER_FAULT = ("not docked for the sale", "crashed: ", "loop not started")      # notes of a run the runner failed: it says nothing about the route


def faulted(row):
    """A run that ended on the runner's own fault: its goods were not sold, or it crashed."""
    return any(str(note).startswith(RUNNER_FAULT) for note in row.get("notes") or [])


def losing(routes, rows, now):
    """{route id: (runs, credits)} of the routes that lost money over their runs of the last LOSS_HOURS: two runs or
    more that read a wallet, negative in sum. A repeating route is summed without the money booked once (a reward, a
    tool); a route that pays once is summed with it, since its reward is its pay. Such a route is closed to every
    pilot until the window moves on: no route flies at a loss unattended (orders F8). A run the runner failed (its
    load not sold because the ship did not dock, a crash) is not counted: it would close a route for the runner's fault."""
    sums = {}
    for row in rows:
        if faulted(row):
            continue
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
        entry[1] += (after - before) + taxes.in_run(row) + routefiles.moved(row) - (0 if route.get("once") else (row.get("one_time") or 0))
    return {rid: (runs, int(total)) for rid, (runs, total) in sums.items() if runs >= 2 and total < 0}


RECENT = 3                   # a repeating route whose last RECENT runs each lost money is closed, whatever its six-hour sum


def lately_losing(routes, rows, now):
    """{route id: (runs, credits)} of the repeating routes whose last RECENT runs that read a wallet, all inside the last
    LOSS_HOURS, each lost money (the money booked once left out). The six-hour sum of `losing` still held the good runs
    from before a bid left: the veil-ray hunts flew 23 runs at a loss after the curd bid left every station, and 36 mine
    runs stored their ice after the near bids emptied (errors ENT-046; the reports of Zero, Apophis and Mercury of
    2026-11-16). Once routes are judged by `losing` alone: their reward is their pay. Closed until the oldest of the
    three leaves the window, or a newer run pays."""
    last = {}
    for row in rows:
        if faulted(row):
            continue
        before, after = row.get("credits_before"), row.get("credits_after")
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (before, after)) or not (before > 0 and after > 0):
            continue
        route = routes.get(row.get("route"))
        if route is None or route.get("once") or not judged(route):
            continue
        try:
            started = calendar.timegm(time.strptime(row.get("started") or "", "%Y-%m-%dT%H:%M:%SZ"))
        except ValueError:
            continue
        last.setdefault(route["id"], []).append((started, (after - before) + taxes.in_run(row) + routefiles.moved(row) - (row.get("one_time") or 0)))
    out = {}
    for rid, runs in last.items():
        recent = sorted(runs)[-RECENT:]
        if len(recent) == RECENT and recent[0][0] >= now - LOSS_HOURS * 3600 and all(delta < 0 for _t, delta in recent):
            out[rid] = (RECENT, int(sum(delta for _t, delta in recent)))
    return out


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


HELD_BACK = set()             # pilots already named as held back, so that a pass every 30 s names each once
ORPHAN_MINUTES = 5            # an engine loop without a fresh order file this long belongs to no runner
ORPHANS = {}                  # pilot -> when its loop was first seen without an order file


def orphans(fleet, orders, now, seen):
    """[pilot] whose engine loop has run with no fresh order file for ORPHAN_MINUTES: no runner owns it (a loop left by
    an engine restart or a dead runner). `seen` keeps the first sighting and forgets a pilot whose loop ended or got an
    owner. Zero, requests ENT-083: two mining loops of guard ships stored ice for hours after the restart of 02:01 UTC."""
    out, current = [], set()
    for ship in fleet.get("ships") or [] if isinstance(fleet, dict) else []:
        name = ship.get("name") or ""
        if ship.get("status") == "connected" and (ship.get("activity") or {}).get("kind") == "loop" and name not in orders:
            current.add(name)
            if now - seen.setdefault(name, now) >= ORPHAN_MINUTES * 60:
                out.append(name)
    for name in [n for n in seen if n not in current]:
        del seen[name]
    return out


def hosting(data):
    """({the kinds of route whose runs go to the run host}, the most runs it is given) from data/fleet/hosting.json:
    {"kinds": ["mine", ...], "max_runs": N}. No file, or one that is not of this form: (set(), 0), every run a process."""
    found = read_json(Path(data) / "fleet" / "hosting.json", {})
    kinds = found.get("kinds") if isinstance(found, dict) else None
    if not isinstance(kinds, list):
        return set(), 0
    cap = found.get("max_runs")
    return {str(k) for k in kinds if str(k) in KINDS}, cap if isinstance(cap, int) and not isinstance(cap, bool) and cap > 0 else 10 ** 6


def spawn(argv, log_path, env):
    """A runner as a process of its own, its output in the pilot's log."""
    with open(log_path, "w", encoding="utf-8") as log:
        return subprocess.Popen(argv, stdout=log, stderr=subprocess.STDOUT, start_new_session=True, env=env)


def one_pass(root, data, dry_run, children):
    now = time.time()
    if (Path(data) / "fleet" / "STOP").exists():
        return ["STOP file present: nothing started"]
    fleet = read_json(Path(data) / "fleet" / "fleet.json", {})
    plan = {"roles": division.load_plan(root)[0], "pilots": own_lists(data)}
    routes = load_routes(root)
    rows = run_rows(data)
    state = {"now": now, "data": data, "rows": rows, "orders": fresh_orders(data, now), "rest": resting(routes, rows, now), "booked": booked(data),
             "loss": losing(routes, rows, now), "late": lately_losing(routes, rows, now), "root": root}
    named = flagships(data)
    ammo = set(read_json(Path(data) / "catalog" / "ammo.json", []) or [])      # written by routemaker.py from the game's catalog
    lines = []
    logs = Path(data) / "routes" / "logs"
    kinds, cap = hosting(data)
    hosted = runhost.load(data) if kinds and runhost.accepting(data, now) else None      # runs the host has; None: no host takes runs now
    for job in [] if dry_run else runhost.take_back(data, now):
        name, what, script = str(job.get("pilot")), str(job.get("what")), str(job.get("script"))
        if state["orders"].get(name) != what or script not in KINDS.values():
            lines.append("%s: `%s` dropped: the host did not take it within a minute, and the pilot's order no longer names it" % (name, what))
            continue
        logs.mkdir(parents=True, exist_ok=True)
        mark = dict(os.environ, FLEET_MEMBER=os.environ.get("FLEET_MEMBER") or "dispatch", FLEET_HOLD=what)
        children.append(spawn([sys.executable, "-I", "-B", os.path.join(str(Path(root) / "fleet"), script)] + [str(a) for a in job.get("argv") or []],
                              logs / (name + ".log"), mark))
        lines.append("%s: `%s` started as a process: the host did not take it within a minute" % (name, what))
    for name in orphans(fleet, state["orders"], now, ORPHANS):
        if dry_run:
            lines.append("%s runs an engine loop no runner owns: a real pass stops it" % name)
            continue
        status, _answer = gate.call("delete", "/accounts/%s/loop" % gate.q(name), timeout=60)
        ORPHANS.pop(name, None)
        lines.append("%s ran an engine loop no runner owns for %d minutes: loop stopped (HTTP %s)" % (name, ORPHAN_MINUTES, status))
    for ship in fleet.get("ships") or []:
        name = ship.get("name") or ""
        if ship.get("status") != "connected" or name in state["orders"] or (ship.get("activity") or {}).get("kind") != "idle":
            continue
        pilot = pilot_of(ship, named, data, ammo)
        if stuck(name, rows, now):
            if name not in HELD_BACK:
                HELD_BACK.add(name)
                lines.append("%s held back: its last %d runs ended `stop 1 not reached`; it gets a route again %d minutes after the last of them" % (name, STUCK, STUCK_REST // 60))
            continue
        HELD_BACK.discard(name)
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
        logs.mkdir(parents=True, exist_ok=True)
        mark = {"FLEET_MEMBER": os.environ.get("FLEET_MEMBER") or "dispatch", "FLEET_HOLD": what}    # the runner is the dispatcher's: division.py lets it pass
        argv = command(route, name, argument, root)
        if hosted is not None and route["kind"] in kinds and hosted < cap:
            runhost.submit(data, name, what, KINDS[route["kind"]], argv[4:], mark, now)       # the pilot onwards: the host runs the script itself
            hosted += 1
        else:
            children.append(spawn(argv, logs / (name + ".log"), dict(os.environ, **mark)))
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
