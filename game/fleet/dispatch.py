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
  - No global wallet floor grounds newborns (FLOOR = 0, Suggi 2026-11-23); routes needing purchase cash set their own
    min_credits, while wallet.py still tops up low wallets from division donors.
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
    `requires.bid` (item, base, min_price, min_qty); the station's book, read
    within `max_age_minutes` (default 60), shows no ask the route names in
    `requires.ask` (item, base, max_price, min_qty), or was not read in that
    time (requests ENT-297); the pilot's own storage at a
    station holds less than `requires.stored` asks (at, item, min), or was not
    read again since the pilot's last run of the route; a once run whose every stop
    was skipped (`every stop skipped`) is no try and the route rests; a
    census has no system older than `every_minutes` (default 60); a guard sees no pilot of
    ours on the route it guards (`nobody flies <id>`); a guard route without `max_ships`
    takes one ship.
  - `requires.held_below` (item, units, division; game/fleet/heldgate.py, off until switched on there): a route is
    open only while the division's pilots hold fewer units of the item, storage and holds (data/stock/storage.json);
    a book that is not whole closes nothing and opens nothing new (Zero, errors.log ENT-111).
  - `requires.strict` (true or false): a route is open only while data/fleet/strict-classes-on stands (true) or only
    while it is absent (false), so a hand-over route starts by itself the minute strict classes go on (requests ENT-332).
  - A (route, pilot) pair rests 30 minutes after three runs in a row that read or reached nothing, whatever their
    minutes: a census row with no place read and no credit moved, or a note `not reached` / `not flown` (ENT-334).
  - An engine loop that runs for a pilot with no fresh order file for five
    minutes belongs to no runner (an engine restart, a dead runner): the
    dispatcher stops that loop through the gate and names it in its log.
  - It sends no command to the game itself: the runners do.
  - Right before it writes a pilot's order it reads the pilot's order file again: a pilot taken during the pass (a
    hand hold of gate.py) keeps that order, is not started and is named in the pass's lines; it is given work when
    that order ends. A runner it started refuses to start over a fresh hand hold (division.may). Requests ENT-289.
  - A runner is started as a process of its own, or handed to the run host (game/fleet/runhost.py: one
    program that flies runs as threads, under 1 MB a waiting run where a process holds 13 MB) when
    data/fleet/hosting.json names the route's kind: {"kinds": ["mine", ...], "max_runs": N}. Without that
    file, with a host that is away, draining or at `max_runs`, the run is a process as before. A job the
    host did not take within a minute is taken back and started as a process.
  - No route flies at a loss unattended: a route whose runs of the last six hours (two or more) lost money in sum is
    closed until the window moves on (`losing`), and so is a repeating route whose last three runs inside those six
    hours each lost money (`lately_losing`); the census, park and fitting routes are not judged.
  - Behind ENABLED_RESTS (decisions D227, orders D13): a repeating route those two would close rests instead, by its
    record in data/routes/rests.json (`rest_book`): 6 hours, 24 when it loses again after its last rest, then 72 at
    most; 6 hours while its runs of the last 48 hours paid in sum, and 6 again when its last rest ended over 72
    hours ago. A run that pays after a rest sets its level back to 0. A rest ends early when a reading newer than its
    start shows back what the route names (`wakes`: its bid, its field above `min_left`, its herd at `min_creatures`).
    Every rest carries its end; a route that pays once and standing work never rest. --dry-run prints the rests a
    real pass would write.
  - Behind the switch file data/fleet/class-guard-on (absent = off; rule F23): a route that is not the pilot's own
    class of work (workclass.own; the role as role_of reads it) is refused, `class: <class> is <roles>' work`. A
    mission that pays once, selling or crafting its own stores, fitting and training stay open to every role.
  - Behind the switch file data/fleet/strict-classes-on (absent = off; rule F23, workclass.py): selling is Trade's
    alone. A route that sells (a mine route's `sell`, a hunt route without `gift_to`, a circuit stop's `sell`) is
    refused to a pilot that is not a trader, `sells: Trade's work (F23); give the goods to a trader with `gift``; a
    mission that pays once keeps its sale. The switch also gives the class guard the strict classes.
  - Behind the switch file data/fleet/pull-on (absent = off): a route that only brings goods of the reserve and earns
    nothing is closed while every one of them holds its max (game/reserve.tsv, else what the reserve asks), and opens
    again when one falls below its min (else 90 percent of max), `full: <item> <held> of max <max>`; the levels and
    marks are kept in data/routes/pull.json by the real pass, each with its own end (game/fleet/pull.py).
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
import fcntl
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
import pull                                       # noqa: E402  the class guard and the pull rule, each behind its switch file (r21)
import workclass                                  # noqa: E402  r22: the sale rule, behind data/fleet/strict-classes-on
import reserves                                   # noqa: E402  requires.reserve: a faction reserve under a floor (requests ENT-266)
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


_JSON_CACHE = {}


def _read_cached_json(path, default):
    p = Path(path)
    try:
        st = p.stat()
    except OSError:
        return default
    key = str(p)
    stamp = (st.st_mtime_ns, st.st_size)
    hit = _JSON_CACHE.get(key)
    if hit and hit[0] == stamp:
        return hit[1]
    val = read_json(p, default)
    if len(_JSON_CACHE) > 256:
        _JSON_CACHE.clear()
    _JSON_CACHE[key] = (stamp, val)
    return val


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


SHORT = ": objectives not done"   # route_run.py: a mine step ended with the mission's objective still open


def short(row):
    """A run whose mine step left the mission's objective open: the field ran short under it (Markab Belt, Rotanev
    Daylight Seam, 2026-11-17). Its pilot did not get what it came for: no try, and the route rests for it."""
    return any(str(note).startswith("mine ") and str(note).endswith(SHORT) for note in row.get("notes") or [])


def unfinished(row):
    """A run that went all the way round and did not get what it came to buy or fit: no finished run of a `once` route."""
    return row.get("stops") == row.get("of") and any(str(note).endswith(NO_BUY) for note in row.get("notes") or [])


NOT_OFFERED = " not offered"
REFUSALS = 3                   # runs a board may refuse on a route with `requires.booked` or `requires.skills` before the route counts as done for the pilot
CUT = "wallet not read"        # route_run.py: the run ended before it read the wallet at its end


def cut(row):
    """A run the engine cut before its end: a stop not reached and the wallet unread (an outage of the engine's
    sign-ins, 2026-11-22 23:15 UTC: requests ENT-379). No try of a `once` route; a run of them rests the route
    (failed_run) so a lasting outage is never hammered."""
    notes = [str(n) for n in row.get("notes") or []]
    return (row.get("stops") or 0) < (row.get("of") or 0) and CUT in notes and any(n.endswith("not reached") for n in notes)


def refused(row):
    """A run whose mission was not offered on the board (either full loop or early-aborted empty tour at stop 1)."""
    notes = [str(note) for note in row.get("notes") or []]
    has_unoffered = any(note.endswith(NOT_OFFERED) for note in notes)
    return has_unoffered and (row.get("stops") == row.get("of") or EARLY_UNOFFERED in notes)


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


_BY_PILOT = {"rows": None, "count": -1, "by": {}, "by_route": {}}


def _row_indexes(rows):
    if _BY_PILOT["rows"] is not rows or _BY_PILOT["count"] != len(rows):
        by_p, by_r = {}, {}
        for row in rows:
            p = row.get("pilot")
            r = row.get("route")
            if p:
                by_p.setdefault(p, []).append(row)
            if r and p:
                by_r.setdefault(r, set()).add(p)
        _BY_PILOT.update(rows=rows, count=len(rows), by=by_p, by_route=by_r)
    return _BY_PILOT["by"], _BY_PILOT["by_route"]


def stuck(name, rows, now=None):
    """True when the pilot's last STUCK runs all ended `stop 1 not reached` and the last of them ended less than STUCK_REST
    seconds before `now`: a ship held in a fight or a lost goal would otherwise be handed one route after another, each
    failing at once (requests ENT-090: 42 park runs in an hour). After the rest it is given one route again, so the hold
    ends by itself when its cause is gone: until 2026-11-17 it ended only with a run that reached a stop, which a held
    pilot never got, and two ships the engine had held claimed stood for two hours and waited for a hand. Without `now`,
    or with a last run whose time does not read, the rest is not counted."""
    mine = (_row_indexes(rows)[0].get(name) or ())[-STUCK:]
    if len(mine) != STUCK or not all("stop 1 not reached" in (r.get("notes") or []) for r in mine):
        return False
    if now is None:
        return True
    ended = run_end(mine[-1])
    if ended is None:
        return True
    return now - ended < STUCK_REST


STALL_RUNS = 3                 # short zero-credit runs in a row on one route: rest that (route, pilot) pair (requests ENT-317)
STALL_MINUTES = 1.0            # runs shorter than this with 0 cr count as stalled loops
STALL_REST = 30 * 60           # seconds of cooldown after a stalled loop or non-ask stop_on_failed_buy
FAILED_BUY_CAUSES = (": wallet floor", ": refused", ": not bought")
NO_FUEL_AT_SELL = "no fuel at sell_at"   # hunt.py: the tank stood under half after the sell_at's refuel (requests ENT-369)
FUEL_NOT_FLOWN = ": not flown (fuel)"    # hunt.py: the tank was short of the way there and on to sell_at, and no fuel stop filled it


def run_end(row):
    """Epoch second a run ended, or None when started is unreadable."""
    try:
        return taxes.parse_utc(row["started"]) + float(row.get("minutes") or 0) * 60
    except (KeyError, TypeError, ValueError):
        return None


def circuit_systems(route):
    """Unique star system ids a circuit route names, in stop order: each stop's own system and those of its mine and
    hunt steps (errors.log ENT-117, requests ENT-312)."""
    out, seen = [], set()
    for stop in route.get("stops") or []:
        if not isinstance(stop, dict):
            continue
        own = str(stop.get("at") or "").split(":")[0]        # requests ENT-312: the stop's own system too
        if own and own not in seen:
            seen.add(own)
            out.append(own)
        for key in ("mine", "hunt"):
            for step in stop.get(key) or []:
                if isinstance(step, dict) and step.get("at"):
                    sys_id = str(step["at"]).split(":")[0]
                    if sys_id and sys_id not in seen:
                        seen.add(sys_id)
                        out.append(sys_id)
    return out


_PAIRS = {"rows": None, "count": -1, "by": {}}


def pairs(rows):
    """{(route, pilot): [run rows in order]} of one pass's run list, built once per list (the cache holds the list
    itself, so a new list is never taken for an old one; a list that grew is indexed again)."""
    if _PAIRS["rows"] is not rows or _PAIRS["count"] != len(rows):
        by = {}
        for row in rows:
            by.setdefault((row.get("route"), row.get("pilot")), []).append(row)
        _PAIRS.update(rows=rows, count=len(rows), by=by)
    return _PAIRS["by"]


def stalled_reason(rid, route, pilot_name, rows, now):
    """Why (rid, pilot_name) rests after repeated zero-minute loops, runs that read or reached nothing (ENT-334) or non-ask
    stop_on_failed_buy (requests ENT-317), or None."""
    if route.get("park") or route.get("kind") == "guard":
        return None
    mine = pairs(rows).get((rid, pilot_name)) or []
    if not mine:
        return None
    last = mine[-1]
    ended = run_end(last)
    if ended is None or now - ended >= STALL_REST:
        return None
    notes = [str(n) for n in (last.get("notes") or [])]
    if any("run ended (stop_on_failed_buy)" in n for n in notes) and any(c in n for n in notes for c in FAILED_BUY_CAUSES):
        return "rests after failed buy (wallet floor or refused)"
    if any(NO_FUEL_AT_SELL in n or FUEL_NOT_FLOWN in n for n in notes):     # requests ENT-369: never set out again on a dry tank
        return "rests after a run whose tank was not filled (its sell_at sold no fuel, or too short to set out)"
    tail = mine[-STALL_RUNS:]
    if len(tail) < STALL_RUNS:
        return None
    if route.get("kind") != "census" and all(
        float(r.get("minutes") or 0) < STALL_MINUTES
        and (r.get("delta") or 0) <= 0
        and not r.get("sold")
        and not any("gift to " in str(n) for n in (r.get("notes") or []))
        for r in tail
    ):
        return "rests after %d short zero-credit runs" % STALL_RUNS
    if all(failed_run(r) for r in tail):            # requests ENT-334, errors.log ENT-121: whatever their minutes
        return "rests after %d runs in a row that read or reached nothing" % STALL_RUNS
    return None


def failed_run(row):
    """True for a run that read or earned nothing: a census row with no place read and no credit moved, or a row whose
    note says `not reached` or `not flown` (census.py, requests ENT-334)."""
    notes = " ".join(str(n) for n in (row.get("notes") or []))
    if "not reached" in notes or "not flown" in notes:
        return True
    return row.get("kind") == "census" and not row.get("places") and not row.get("delta") and not row.get("sold")


def done_once(route, rows):
    """A `once` route counts as done after a whole run that got what it came for, or after two tries. A run that found
    nothing to buy is neither: the route opens again for that pilot after a rest (waits_once). On a route that names a
    reward the pilot must hold first (`requires.booked`), a run the board refused is no try either, up to REFUSALS times:
    the pilot flew it before it held that reward; the same on a route with `requires.skills` (a board that offers it
    only from a skill level). Without either a refusal stays a finished run: a mission done once is never offered
    again. A run the engine cut (cut: wallet unread, a stop not reached) is no try."""
    rows = [r for r in rows if not unfinished(r) and not empty(r) and not short(r) and not cut(r)]
    gated = owed(route) or bool((route.get("requires") or {}).get("skills"))     # requests ENT-379: refused below a skill gate
    if gated and sum(1 for r in rows if refused(r)) <= REFUSALS:
        rows = [r for r in rows if not refused(r)]
    if not rows:
        return False
    whole = [r for r in rows if r.get("stops") == r.get("of") or (refused(r) and not gated)]  # full run or ungated unoffered abort
    return bool(whole) or len(rows) >= 2


def waits_once(route, rows, now):
    """True while a `once` route rests for a pilot: its last run found nothing to buy less than retry_minutes (default 60) ago."""
    if not rows or not (unfinished(rows[-1]) or empty(rows[-1]) or short(rows[-1]) or cut(rows[-1]) or (owed(route) and refused(rows[-1]))):
        return False
    try:
        ended = calendar.timegm(time.strptime(rows[-1]["started"], "%Y-%m-%dT%H:%M:%SZ")) + rows[-1].get("minutes", 0) * 60
    except (KeyError, ValueError):
        return False
    return now < ended + route.get("retry_minutes", 60) * 60


def herd(data, route, now, fresh=CENSUS_FRESH):
    """Creatures of the route's species at its place per the last census; None when none younger than `fresh` seconds
    exists."""
    system, poi = route["place"].split(":")
    path = Path(data) / "wildlife" / (system + ".json")
    try:
        if now - path.stat().st_mtime > fresh:
            return None
    except OSError:
        return None
    place = (read_json(path, {}).get("pois") or {}).get(poi) or {}
    try:                                              # the place's own reading time: a hunter that left writes only its place
        if now - calendar.timegm(time.strptime(str(place.get("read_at"))[:19], "%Y-%m-%dT%H:%M:%S")) > fresh:
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
FLOOR = 0                    # removed 5,000 cr wall (Suggi 2026-11-23): newborns fly natural routes; routes set min_credits when needed


def read_time(text):
    """Seconds since the epoch of a UTC time written YYYY-MM-DDTHH:MM:SS..., or None."""
    try:
        return taxes.parse_utc(text)
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
        found = bid_read(data, want, now)
        if found is None:
            continue
        price, depth = found
        if price < int(want.get("min_price") or 1) or depth < int(want.get("min_qty") or 1):
            return "no bid for %s at %s: best %d cr x %d" % (want.get("item"), want.get("base"), price, depth)
    return None


def bid_read(data, want, now, fresh=BID_FRESH):
    """(best bid, units at it) for `want`'s item ({item, base}) in the station's book read within `fresh` seconds,
    or None when no such book exists: the one reader of a bid, for bid_missing and a rest's early end (wakes)."""
    book = read_json(Path(data) / "market" / (str(want.get("base")) + ".json"), {})
    read = read_time(book.get("read_at")) if isinstance(book, dict) else None
    if read is None or now - read > fresh:
        return None
    row = next((i for i in book.get("items") or [] if isinstance(i, dict) and i.get("item_id") == want.get("item")), {})
    return int(row.get("best_buy") or 0), int(row.get("best_buy_qty") or 0)


ASK_FRESH = 60               # minutes: a book older than this shows no ask (`requires.ask`, its `max_age_minutes`; requests ENT-297)


def asks(route):
    """The asks a route buys from (`requires.ask`: one {item, base, max_price, min_qty, max_age_minutes} or a list of them)."""
    need = (route.get("requires") or {}).get("ask")
    return [need] if isinstance(need, dict) else [a for a in need or [] if isinstance(a, dict)] if isinstance(need, list) else []


def ask_missing(data, route, now):
    """Why a route is closed by `requires.ask`, or None: it opens only while the station's book, read by a docked ship
    of ours within `max_age_minutes` (default ASK_FRESH), shows the item's best ask at `max_price` or under with
    `min_qty` units (default 1) at it (a book keeps the units of its best ask only: deeper levels count for nothing).
    Unlike a bid, a book older than that closes the route: an ask not read is no ask. Mercury, requests ENT-297: Node
    Alpha's silver ask was gone after one load, a failed buy does not end a run, and the route would fly 16 jumps empty."""
    for want in asks(route):
        fresh = float(want.get("max_age_minutes") or ASK_FRESH) * 60
        book = read_json(Path(data) / "market" / (str(want.get("base")) + ".json"), {})
        read = read_time(book.get("read_at")) if isinstance(book, dict) else None
        if read is None or now - read > fresh:
            return "no ask for %s at %s: its book not read in %d minutes" % (want.get("item"), want.get("base"), fresh // 60)
        row = next((i for i in book.get("items") or [] if isinstance(i, dict) and i.get("item_id") == want.get("item")), {})
        price, depth = int(row.get("best_sell") or 0), int(row.get("best_sell_qty") or 0)
        if price <= 0 or price > float(want.get("max_price") or 0) or depth < int(want.get("min_qty") or 1):
            return "no ask for %s at %s: best %d cr x %d" % (want.get("item"), want.get("base"), price, depth)
    return None


def stored_missing(data, route, pilot, rows):
    """Why a route is closed by `requires.stored`, or None: the pilot's own storage at the station named (`at`, a base
    id) holds fewer than `min` units of `item` by data/stock/storage.json (the service ledger reads each pilot about
    every 40 minutes), or that storage was not read again since the pilot's last run of this route began: a carry
    run takes the load out, and the old reading must not send the pilot a second time. Storage is personal: only the
    pilot that stored a load can withdraw it (Zero, requests ENT-117: about 11,100 water ice in miners' storage at
    stations whose bids are gone). A want with `items` (a list) is met by any one of them at `min` (requests ENT-349);
    a list of wants means all of them."""
    need = (route.get("requires") or {}).get("stored")
    wants = [need] if isinstance(need, dict) else [w for w in need or [] if isinstance(w, dict)]
    if not wants:
        return None
    spath = Path(data) / "stock" / "storage.json"
    book = _read_cached_json(spath, {})
    mine = ((book.get("pilots") or {}) if isinstance(book, dict) else {}).get(pilot["name"]) or {}
    read = read_time(mine.get("read_at"))
    mine_runs = pairs(rows).get((route.get("id"), pilot["name"])) or ()
    last = max((read_time(r.get("started")) or 0 for r in mine_runs), default=0)
    for want in wants:
        there = (mine.get("stations") or {}).get(str(want.get("at"))) or {}
        if isinstance(want.get("items"), list):          # any one of them opens it (Zero, requests ENT-349)
            names = [str(i) for i in want["items"]]
            if not any(int(there.get(name, 0) or 0) >= int(want.get("min") or 1) for name in names):
                return "stores none of %s at %s at %s or more" % (", ".join(names), want.get("at"), want.get("min") or 1)
            continue
        held = int(there.get(str(want.get("item")), 0) or 0)
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


FOREIGN_REACH = 6               # jumps: how far from where it stands a pilot of another empire is sent (queue.log ENT-234)
ONCE_MISSION_REACH = 6          # jumps: max reach for foreign once-missions for ANY pilot unless far_ok (rules F34, F35)
EARLY_UNOFFERED = "mission not offered: skipped empty tour"  # route_run.py: aborted empty tour at Stop 1 when board had no offer
LANES_CACHE = {"lanes": None}


def route_place(route):
    """The system of a route's first place: a hunt's or mine's place, else its first stop; None when it names none."""
    for key in ("place", "belt"):
        if route.get(key):
            return str(route[key]).split(":")[0] or None
    systems = circuit_systems(route) if route.get("stops") else []
    if systems:
        return systems[0]
    if route.get("station"):
        return str(route["station"]).split(":")[0] or None
    return None


def newborn_reason(pilot, rid, route):
    """Why a route is closed to a pilot born in another empire, or None (the Plan-500 wave of 2026-11-22, queue.log
    ENT-234: 250 pilots born at Sol, Haven, Altais and Krynn, 10 to 21 jumps from our home, lawless space between).
    A Voidborn empire mission is never theirs (rule F35: a pilot's empire skill comes from its own empire's missions);
    a route whose first place lies more than FOREIGN_REACH jumps from where the pilot stands waits for its Admiral to
    write work in the pilot's own region, unless the route says `far_ok`. A Voidborn pilot, or one whose empire or
    place is not read, is judged as before."""
    empire = pilot.get("empire")
    if not empire or empire == "voidborn":
        return None
    if str(rid).startswith("voidborn-"):
        return "a Voidborn empire mission: the pilot was born %s (rule F35)" % empire
    if route.get("far_ok") or route.get("kind") == "census" or not pilot.get("system"):
        return None
    if LANES_CACHE["lanes"] is None:
        import fuelplan
        LANES_CACHE["lanes"] = fuelplan.chart(Path(__file__).resolve().parent.parent)[0]
    place = route_place(route)
    if not place:
        return None
    reach = jumps_between(LANES_CACHE["lanes"], pilot["system"], place)
    if reach is not None and reach > FOREIGN_REACH:
        return "%d jumps from the pilot, born %s: work in its own region first (`far_ok` lifts it)" % (reach, empire)
    return None


def system_empires():
    """{system_id: empire} cached from game/map/galaxy.tsv ('' for lawless/unclaimed frontier)."""
    cached = LANES_CACHE.get("empires")
    if cached is not None:
        return cached
    empires = {}
    tsv = Path(__file__).resolve().parent.parent / "map" / "galaxy.tsv"
    try:
        for line in tsv.read_text(encoding="ascii", errors="replace").splitlines():
            if not line or line.startswith("#") or line.startswith("id	"):
                continue
            parts = line.split("	")
            if len(parts) >= 5:
                emp = parts[4].strip().lower()
                empires[parts[0].strip()] = "" if emp in ("", "-") else emp
    except OSError:
        pass
    LANES_CACHE["empires"] = empires
    return empires


def is_once_mission(rid, route):
    """True for one-time board/storyline mission routes (excludes fit-*, stock-*, buy-*, and standing work)."""
    if not route or not route.get("once"):
        return False
    if str(rid).startswith("mission-"):
        return True
    return any(isinstance(stop, dict) and bool(stop.get("accept")) for stop in (route.get("stops") or []))


def mission_reach_reason(pilot, rid, route):
    """Smart mission guard (rules F34, F35): own-empire storyline/Mastery chains stay open to native pilots anywhere;
    foreign/frontier `once` board missions stay local (<= ONCE_MISSION_REACH jumps) unless `far_ok` or explicit
    `requires.empire` opts in. Prevents fitted Voidborn industrial ships from abandoning outposts/corridors for
    low-yield cross-galaxy tourism with zero Mastery XP."""
    if not is_once_mission(rid, route) or route.get("far_ok"):
        return None
    empire = pilot.get("empire")
    cur_sys = pilot.get("system")
    if not empire or not cur_sys:
        return None
    req_emp = (route.get("requires") or {}).get("empire")
    if req_emp:
        allowed = [req_emp] if isinstance(req_emp, str) else [str(e) for e in req_emp]
        if empire in allowed:
            return None
    place = route_place(route)
    if not place:
        return None
    route_emp = system_empires().get(place, "")
    if route_emp and route_emp == empire:
        return None
    if LANES_CACHE["lanes"] is None:
        import fuelplan
        LANES_CACHE["lanes"] = fuelplan.chart(Path(__file__).resolve().parent.parent)[0]
    reach = jumps_between(LANES_CACHE["lanes"], cur_sys, place)
    if reach is not None and reach > ONCE_MISSION_REACH:
        label = route_emp or "frontier"
        return "%d jumps to foreign once-mission (%s at %s): stay on own-empire Mastery and standing work unless `far_ok` (rules F34, F35)" % (reach, label, place)
    return None


DIST_CACHE = {}


def jumps_between(lanes, src, dst):
    """Lanes from src to dst by the chart, None when no way; each source's whole map is walked once (cached)."""
    key = (id(lanes), src)
    if key not in DIST_CACHE:
        dist, todo = {src: 0}, [src]
        while todo:
            here = todo.pop(0)
            for there in lanes.get(here) or []:
                if there not in dist:
                    dist[there] = dist[here] + 1
                    todo.append(there)
        DIST_CACHE[key] = dist
    return DIST_CACHE[key].get(dst)


def why_not(pilot, rid, route, state):
    """(why the route is closed to the pilot now, or None when it is open; for an open census the system to read).
    The one rule: pick() and fill.py both use it."""
    if not route:
        return "no route file", None
    if route.get("status") == "off":
        return "off", None
    born = newborn_reason(pilot, rid, route)                     # queue.log ENT-234: pilots of other empires stay in their region
    if born:
        return born, None
    empires = (route.get("requires") or {}).get("empire")        # requests ENT-387: a route of one empire's pilots
    if empires:
        allowed = [empires] if isinstance(empires, str) else [str(e) for e in empires]
        if pilot.get("empire") not in allowed:
            return "open only to pilots born %s (the pilot: %s)" % (", ".join(allowed), pilot.get("empire") or "not read"), None
    far_mission = mission_reach_reason(pilot, rid, route)         # rules F34, F35: keep foreign once-missions local unless far_ok
    if far_mission:
        return far_mission, None
    strict = (route.get("requires") or {}).get("strict")          # requests ENT-332: open only in one state of data/fleet/strict-classes-on
    if isinstance(strict, bool):
        workclass.follow(state.get("data"))
        if strict != workclass.strict_on():
            return ("open only while strict classes are on" if strict else "open only while strict classes are off"), None
    if route.get("park") and pilot.get("docked"):
        return "the pilot is docked", None
    sells = workclass.sale_refused(pilot, rid, route, state)      # r22: with data/fleet/strict-classes-on selling is Trade's alone (rule F23)
    if sells:
        return sells, None
    held = pull.closes(pilot, rid, route, state)  # r21: the class guard and the pull rule, each only while its switch file exists
    if held:
        return held, None
    answered = False
    if ENABLED_RESTS and not route.get("once") and judged(route):     # D227: a route that does not pay rests by its record
        reason, answered = rest_of(rid, state)
        if reason:
            return reason, None
    lost = (state.get("loss") or {}).get(rid)
    if lost and not answered:
        return "at a loss: %d runs, %s cr in %d hours" % (lost[0], format(lost[1], ","), LOSS_HOURS), None
    late = (state.get("late") or {}).get(rid)
    if late and not answered:
        return "its last %d runs each lost money: %s cr" % (late[0], format(late[1], ",")), None
    if set(route.get("skip_if_booked") or []) & (state.get("booked") or {}).get(pilot["name"], set()):
        return "its reward is booked", None
    if route.get("kind") in ("hunt", "mine"):
        reason = pirate_reason(str(route.get("place") or route.get("belt") or "").split(":")[0], state)
        if reason:
            return reason, None
    elif route.get("kind") == "circuit":
        for sys_id in circuit_systems(route):
            reason = pirate_reason(sys_id, state)
            if reason:
                return reason, None
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
        mine = list(pairs(state["rows"]).get((rid, pilot["name"])) or [])
        if done_once(route, mine):
            return "done once", None
        if waits_once(route, mine, state["now"]):
            return ("rests after a run the board refused" if refused(mine[-1]) else
                    "rests after a run with every stop skipped" if empty(mine[-1]) else
                    "rests after a mine step its field left short" if short(mine[-1]) else "rests after a buy that found no offer"), None
    stall = stalled_reason(rid, route, pilot["name"], state.get("rows") or [], state["now"])
    if stall:
        return stall, None
    mark = route["kind"] + " " + rid
    if route.get("max_pilots"):                   # at most this many different pilots ever: those that flew it and those on it now
        flew = _row_indexes(state["rows"])[1].get(rid, set()) | {p for p, what in state["orders"].items() if what == mark}
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
        if isinstance(guarded, dict) and guarded.get("kind") == "circuit":       # an escort: it follows the pilot of ours on the circuit (ENT-217)
            flyers = sorted(p for p, what in state["orders"].items() if what == "circuit " + str(route["guards"]))
            if not flyers:
                return "nobody flies %s" % route["guards"], None
            ship = read_json(Path(state["data"]) / "fleet" / "ships" / ship_file(flyers[0]), {}) if state.get("data") else {}
            spot = ":".join(str(ship.get(key) or "") for key in ("system", "poi")) if isinstance(ship, dict) and ship.get("system") else ""
            place = {"place": spot or str(route.get("place") or ":".join(str(route.get("station") or "").split(":")[:2])), "follow": flyers[0]}
            reason = pirate_reason(place["place"].split(":")[0], state)
            if reason:
                return reason, None
        else:
            place = routefiles.guarded_place(route, guarded)
            if place is None:
                return "guards `%s`: no mine, hunt or circuit route file" % route.get("guards"), None
            if guarded["kind"] + " " + str(route["guards"]) not in state["orders"].values():
                return "nobody flies %s" % route["guards"], None
            reason = pirate_reason(str(place).split(":")[0], state)
            if reason:
                return reason, None
    if pilot.get("credits", 0) < route.get("min_credits", 0):
        return "wallet below %s cr" % route["min_credits"], None
    if FLOOR > 0 and pilot.get("credits", 0) < FLOOR and not (route.get("park") or routefiles.stage(route) in ("once", "paying")):
        return "wallet below %s cr: only work that pays" % format(FLOOR, ","), None
    p_mods = pilot.get("modules") or []
    req = route.get("requires") or {}
    need = req.get("module")
    if isinstance(need, str) and need and need not in p_mods:
        return "needs " + need, None
    if isinstance(need, list) and need and not any(m_id in p_mods for m_id in need):     # requests ENT-343: a list is any one of them
        return "needs one of " + ", ".join(str(m_id) for m_id in need), None
    if isinstance(need, dict):
        for m_id, min_n in need.items():
            if p_mods.count(m_id) < min_n:
                return "needs %dx %s" % (min_n, m_id), None
    if req.get("empty_hold") and pilot.get("goods", 0) > 5:                                 # nothing to lose aboard (orders F13); five units count as nothing
        return "hold not empty", None
    if req.get("hold") and pilot.get("goods", 0) <= 5:                                      # a route that stores what is aboard: not for a pilot that carries nothing
        return "nothing aboard", None
    without = req.get("without_module")
    if isinstance(without, str) and without in p_mods:                                      # the route fits this module: not for a pilot that has it
        return "has the module already", None
    if isinstance(without, list) and any(m in p_mods for m in without):
        return "has the module already", None
    mods_below = req.get("modules_below")
    if isinstance(mods_below, dict) and mods_below and all(p_mods.count(m_id) >= want_n for m_id, want_n in mods_below.items()):
        return "has target modules already", None
    any_mod = req.get("any_module")
    if isinstance(any_mod, list) and any_mod and not any(m_id in p_mods for m_id in any_mod):
        return "no target module to strip", None
    if state["now"] < state["rest"].get(rid, 0):
        return "the place rests", None
    lacking = bid_missing(state["data"], route, state["now"]) or stored_missing(state["data"], route, pilot, state["rows"])
    lacking = lacking or ask_missing(state["data"], route, state["now"])    # requests ENT-297: the buy end, read like requires.bid
    lacking = lacking or __import__("heldgate").closed(pilot, rid, route, state)     # Q75 (1), ENT-111: open while the division holds less
    if lacking:
        return lacking, None
    floor = reserves.closed(route, state)        # requests ENT-266: open only while the faction reserve reads under `below`
    if floor:
        return floor, None
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
            "empire": ship.get("empire") or detail.get("empire"), "system": ship.get("system") or detail.get("system"),
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
        return (base + [route["belt"], route["station"], "--minutes", str(route.get("minutes", 45)), "--route", route["id"]] + (["--sell-items", sell] if sell else [])
                + (["--deposit", "faction"] if route.get("deposit") == "faction" else [])
                + (["--gift", json.dumps(route["gift"], sort_keys=True)] if route.get("gift") else []))     # r22: the hand-over (handover.py)
    if route["kind"] == "guard":                  # the place why_not found: the guard's own, else the guarded route's; an escort follows a pilot
        follow = argument.get("follow") if isinstance(argument, dict) else None
        spot = argument.get("place") if isinstance(argument, dict) else argument
        system, poi = (str(spot or route.get("place") or "") + ":").split(":")[:2]
        return (base + [system, poi, "--guards", route["guards"], "--station", route["station"], "--minutes", str(route.get("minutes", 60)), "--route", route["id"]]
                + (["--follow", follow] if follow else []))
    system, poi = route["place"].split(":")
    out = base + [system, poi, "--kills", str(route.get("kills", 8)), "--minutes", str(route.get("minutes", 40)),
                  "--min-bid", str(route.get("min_bid", 100)), "--sell-at", route["sell_at"], "--route", route["id"]]
    out += ["--max-prey-hull", str(route["max_prey_hull"])] if route.get("max_prey_hull") else []
    out += ["--alone"] if route.get("alone") else []
    out += ["--gift-to", str(route["gift_to"])] if route.get("gift_to") else []     # r22: the hand-over instead of the sale (handover.py)
    return out + (["--species", ",".join(route["species"])] if route.get("species") else [])


LOSS_HOURS = 6               # the window a route's runs are judged over
PIRATE_HOURS = 6             # orders D9: a hunt, a mine or a guard where a pirate was seen within this many hours is closed
PIRATE_HEAVY = 1000          # a pack whose hull and shield, read in one census, add up to this or more ...
PIRATE_HEAVY_HOURS = 24      # ... closes its system this long (requests ENT-250: six Nyx elites at Violethall)
PIRATE_TAIL = 4 * 1024 * 1024    # bytes of the sightings record read from its end: six hours of service sight's passes


def pirates(data, now):
    """{system: the second a pirate was last seen there}, within PIRATE_HOURS (PIRATE_HEAVY_HOURS for a pack of
    PIRATE_HEAVY or more hull and shield in one census read): from service sight's record of every
    place our ships read (data/intel/sightings.jsonl, `pirates` above 0) and from the members' own lines
    (data/observations/*.jsonl, kind `pirate`; a summary line counts by its `last` fight). A record that cannot be
    read closes nothing (Military's report of 2026-11-17: D9 was kept between turns by the runner's leave rule alone)."""
    since, seen, packs = now - PIRATE_HOURS * 3600, {}, {}

    def note(system, stamp, hours=PIRATE_HOURS):
        try:
            when = calendar.timegm(time.strptime(str(stamp)[:19], "%Y-%m-%dT%H:%M:%S"))
        except ValueError:
            return
        if system and now - hours * 3600 <= when <= now + 60:
            seen[str(system)] = max(seen.get(str(system), 0), when)
    try:
        with open(Path(data) / "intel" / "sightings.jsonl", "rb") as handle:
            size = handle.seek(0, 2)
            handle.seek(max(0, size - PIRATE_TAIL))
            text = handle.read().decode("utf-8", "replace")
    except OSError:
        text = ""
    for line in text.splitlines():
        if '"pirates"' not in line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        count = row.get("pirates") if isinstance(row, dict) else None
        if isinstance(count, (int, float)) and not isinstance(count, bool) and count > 0:
            note(row.get("system"), row.get("at"))
    for path in sorted((Path(data) / "observations").glob("*.jsonl")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            if '"pirate"' not in line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict) and row.get("kind") == "pirate":
                fields = row.get("fields") if isinstance(row.get("fields"), dict) else {}
                note(row.get("subject"), fields.get("last") or row.get("t"))
                weight = sum(v for v in (fields.get("hull"), fields.get("shield")) if isinstance(v, (int, float)) and not isinstance(v, bool))
                key = (str(row.get("subject") or ""), str(row.get("t") or ""))
                packs[key] = packs.get(key, 0) + weight          # one line per pirate of one census read
    for (system, stamp), weight in packs.items():
        if weight >= PIRATE_HEAVY:
            note(system, stamp, PIRATE_HEAVY_HOURS)
    return seen


def pirate_reason(system, state):
    """The reason a place is closed under orders D9, or None."""
    when = (state.get("pirates") or {}).get(str(system or ""))
    if not when:
        return None
    return "pirates seen in %s %.1f hours ago (orders D9: every ship avoids them)" % (system, max(0.0, state.get("now", when) - when) / 3600)


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
            started = taxes.parse_utc(row.get("started") or "")
        except ValueError:
            continue
        route = routes.get(row.get("route"))
        if route is None or started < now - LOSS_HOURS * 3600 or not judged(route):
            continue
        entry = sums.setdefault(route["id"], [0, 0])
        entry[0] += 1
        entry[1] += earned_by(row, route)
    return {rid: (runs, int(total)) for rid, (runs, total) in sums.items() if runs >= 2 and total < 0}


def earned_by(row, route):
    """What one run of a judged route made, as the loss stop counts it: its wallet's change with the weekly tax and what
    another hand of ours moved through the wallet taken out, and for a repeating route without the money booked once.
    The row must read a wallet at both ends (losing, lately_losing and rest_book filter first)."""
    return ((row["credits_after"] - row["credits_before"]) + taxes.in_run(row) + routefiles.moved(row)
            - (0 if route.get("once") else (row.get("one_time") or 0)))


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
            started = taxes.parse_utc(row.get("started") or "")
        except ValueError:
            continue
        last.setdefault(route["id"], []).append((started, earned_by(row, route)))
    out = {}
    for rid, runs in last.items():
        recent = sorted(runs)[-RECENT:]
        if len(recent) == RECENT and recent[0][0] >= now - LOSS_HOURS * 3600 and all(delta < 0 for _t, delta in recent):
            out[rid] = (RECENT, int(sum(delta for _t, delta in recent)))
    return out


def resting(routes, rows, now):
    """{route id: time before which a hunt's place rests}: its last run ended without a kill."""
    hunts = {rid: route for rid, route in routes.items() if route["kind"] == "hunt"}
    if not hunts:
        return {}
    out, seen = {}, set()
    for last in reversed(rows):
        rid = last.get("route")
        if rid not in hunts or rid in seen:
            continue
        seen.add(rid)
        if not last.get("kills"):
            ended = run_end(last)
            if ended is not None:
                out[rid] = ended + hunts[rid].get("rest_minutes", 30) * 60
        if len(seen) == len(hunts):
            break
    return out


# A route that does not pay rests, never for good (decisions D227, orders D13; rules F8, F22). Measured 2026-11-17 on
# 48 hours of runs: of 60 judged routes closed in three or more six-hour windows, 33 paid in sum (+1,356,158 cr: their
# buyers come and go) and 24 lost again on every opening (-141,260 cr). So a rest grows with the record and wakes early.
ENABLED_RESTS = True         # on since 2026-11-17 20:20 UTC, after the dry run on a copy of the live data (round r20)
REST_HOURS = (6, 24, 72)     # the rest of level 1, 2 and 3
RESET_HOURS = 72             # a rest that ended longer ago is forgotten: the route's next rest is of level 1
NET_HOURS = 48               # a route whose runs of this window paid in sum rests REST_HOURS[0] at most
RESTS = {"path": None, "stamp": None, "book": {}}      # rests.json as why_not reads it for fill.py and hive.py: read again when it changed


def rests_path(data):
    """The rests' record: data/routes/rests.json, {route: {from, until, why, level, net48[, woke][, reset]}}."""
    return Path(data) / "routes" / "rests.json"


def read_rests(data):
    """{route: rest} of the record, read again only when the file changed; {} without one."""
    if not data:
        return {}
    path = rests_path(data)
    try:
        found = path.stat()
    except OSError:
        return {}
    stamp = (found.st_ino, found.st_mtime_ns, found.st_size)
    if RESTS["path"] != str(path) or RESTS["stamp"] != stamp:
        book = read_json(path, {})
        RESTS.update(path=str(path), stamp=stamp, book=book if isinstance(book, dict) else {})
    return RESTS["book"]


def utc(epoch, seconds=True):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ" if seconds else "%Y-%m-%dT%H:%MZ", time.gmtime(epoch))


def rest_end(entry):
    """When a rest ends: its `until`, never later than its start and the longest rest (no rest only a hand can end);
    None for a record that is no rest (level 0, a time that does not read)."""
    start, until = read_time(entry.get("from")), read_time(entry.get("until"))
    if not isinstance(entry.get("level"), int) or entry["level"] < 1 or start is None or until is None:
        return None
    return min(until, start + REST_HOURS[-1] * 3600)


def rest_stands(entry, now):
    """True while a rest closes its route: begun and not ended."""
    end = rest_end(entry) if isinstance(entry, dict) else None
    return end is not None and read_time(entry.get("from")) <= now < end


def rested_until(entry):
    """When the route's last rest ended or ends (rest_end; for a record of level 0 its `until`), or None."""
    end = rest_end(entry)
    return end if end is not None else read_time(entry.get("until"))


def counts_from(entry):
    """From when a run is new to a route's record: the moment a rest woke (the reading that woke it is newer than what
    flew during it), else the rest's start (a run in flight when it began was of the verdict that began it)."""
    return read_time(entry.get("until")) if entry.get("woke") else read_time(entry.get("from"))


def rest_of(rid, state):
    """(why the route rests, or None; True when its last rest ended inside the last LOSS_HOURS, so that a verdict of
    losing or lately_losing may rest on runs that rest answered: rest_book alone judges them). The dispatcher passes
    the rests of its pass in state["rests"]; fill.py and hive.py read the record."""
    entry = (state["rests"] if "rests" in state else read_rests(state.get("data"))).get(rid)
    if not isinstance(entry, dict):
        return None, False
    if rest_stands(entry, state["now"]):
        end = rest_end(entry)
        return "resting until %s (%d h, level %d, %s)" % (utc(end, False), round((end - read_time(entry["from"])) / 3600), entry["level"], entry.get("why") or "it lost money"), True
    return None, (rested_until(entry) or 0) > state["now"] - LOSS_HOURS * 3600


def counted(row):
    """True for a run whose credits speak of its route, as the loss stop counts them: not the runner's fault, a wallet
    read at both ends."""
    before, after = row.get("credits_before"), row.get("credits_after")
    return (not faulted(row) and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (before, after))
            and before > 0 and after > 0)


def wanted_bids(route):
    """[{item, base, min_price, min_qty}] of the bids a route sells into by its file: `requires.bid`; else every `sell`
    of a mine route at its station, or of a circuit's stops at the stop's station, whose `min_price` is above 1 (a
    floor of 1 sells at any price and names no need: on 2026-11-17 a 2 cr argon bid would have woken a route that lost
    for two days). A hunt names its drop only in `requires.bid`."""
    if bids(route):
        return bids(route)
    sells = [(str(route.get("station", "")), s) for s in route.get("sell") or []] if route.get("kind") == "mine" else [
        (str(stop.get("at", "")), s) for stop in route.get("stops") or [] if isinstance(stop, dict) and isinstance(stop.get("sell"), list) for s in stop["sell"]]
    return [{"item": s["item"], "base": at.split(":")[-1], "min_price": s["min_price"]} for at, s in sells
            if isinstance(s, dict) and s.get("item") and not s.get("all") and isinstance(s.get("min_price"), (int, float)) and s["min_price"] > 1]


def wakes(data, route, start, now):
    """What came back since a rest began, or None: every reading the route rests on, each newer than the rest's start
    and still fresh, shows it back. Its bids (wanted_bids) at their price and depth, its field floors (`min_left` of a
    mine route or of a circuit's mine step, field_left), its herds (`min_creatures` of a hunt or of a circuit's hunt
    step, herd). None when one reading is missing or short, and for a route with nothing such to read: a hunt that
    names no drop in `requires.bid` (its sale has no reading), a circuit that buys (its ask has no reader here)."""
    if route.get("kind") == "hunt" and not bids(route):
        return None
    if any(isinstance(stop, dict) and stop.get("buy") for stop in route.get("stops") or []):
        return None
    since, seen = now - start, []
    for want in wanted_bids(route):
        found = bid_read(data, want, now, fresh=min(BID_FRESH, since))
        if found is None or found[0] < int(want.get("min_price") or 1) or found[1] < int(want.get("min_qty") or 1):
            return None
        seen.append("%s bids %d cr x %d for %s" % (want.get("base"), found[0], found[1], want.get("item")))
    steps = [route] if route.get("kind") == "mine" else [s for stop in route.get("stops") or [] if isinstance(stop, dict) for s in stop.get("mine") or []]
    for step in steps:
        if isinstance(step, dict) and isinstance(step.get("min_left"), dict):
            place = step.get("belt") or step.get("at") or ""
            left = field_left(data, place, now, fresh=min(CENSUS_FRESH, since)) if len(str(place).split(":")) == 2 else None
            if left is None or any(left.get(item, 0) < int(units) for item, units in step["min_left"].items()):
                return None
            seen.append("the field at %s above its floor" % place)
    herds = [(route, route.get("min_creatures", 1))] if route.get("kind") == "hunt" else [
        ({"place": h["at"], "species": h.get("species")}, int(h["min_creatures"])) for stop in route.get("stops") or [] if isinstance(stop, dict)
        for h in stop.get("hunt") or [] if isinstance(h, dict) and h.get("min_creatures") and h.get("at")]
    for spot, need in herds:
        count = herd(data, spot, now, fresh=min(CENSUS_FRESH, since)) if len(str(spot.get("place", "")).split(":")) == 2 else None
        if count is None or count < need:
            return None
        seen.append("%d creatures at %s" % (count, spot["place"]))
    return "; ".join(seen) or None


def rest_book(routes, rows, now, data, book, loss, late):
    """(the rests at `now`, [what changed, one line each]) from the record before (`book`) and this pass's verdicts
    of losing and lately_losing (`loss`, `late`). A repeating judged route with a verdict and no standing rest gets one
    when a run of it new to its record (counts_from) lost money, else the verdict rests on runs its last rest
    answered: of level 1 (REST_HOURS[0]) without a rest in the last RESET_HOURS or while its runs of the last NET_HOURS
    paid in sum, else one level above its last, at most the last. A standing rest ends early when wakes() reads its
    cause gone (`until` becomes that moment, `woke` says what came back). Once a rest has ended, a new run that paid
    sets its level to 0 (`reset`: that run's start). A record whose rest ended over RESET_HOURS ago is dropped: it
    decides nothing."""
    out = {rid: dict(entry) for rid, entry in (book or {}).items()
           if isinstance(entry, dict) and (rested_until(entry) or 0) >= now - RESET_HOURS * 3600}
    runs, told, figures = {}, [], {}
    for row in rows:
        route = routes.get(row.get("route"))
        if route is None or route.get("once") or not judged(route) or not counted(row):
            continue
        started = read_time(row.get("started"))
        if started is not None:
            runs.setdefault(route["id"], []).append((started, row))

    def made(rid, row):                                  # what a run made, worked out once (routes.moved reads the gifts)
        if id(row) not in figures:
            figures[id(row)] = earned_by(row, routes[rid])
        return figures[id(row)]

    for rid, entry in sorted(out.items()):
        route, end = routes.get(rid), rest_end(entry)
        if end is None:
            continue
        if rest_stands(entry, now):
            woke = wakes(data, route, read_time(entry["from"]), now) if route else None
            if woke:
                entry.update(until=utc(now), woke=woke)
                told.append("%s: its rest ends early, %s came back since it began" % (rid, woke))
            continue
        paid = next((t for t, row in sorted(runs.get(rid, []), key=lambda r: r[0]) if t >= counts_from(entry) and made(rid, row) > 0), None)
        if paid is not None and route is not None:
            entry.update(level=0, reset=utc(paid))
            told.append("%s: a run of %s paid after its rest: its next rest is of level 1" % (rid, utc(paid, False)))
    for rid in sorted(set(loss) | set(late)):
        route, entry = routes.get(rid), out.get(rid)
        if route is None or route.get("once") or not judged(route) or (entry and rest_stands(entry, now)):
            continue                                     # a route that pays once stays with the six-hour stop: its reward is its pay
        since = counts_from(entry) if entry else None
        if entry and not any(t >= (since or float("inf")) and made(rid, row) < 0 for t, row in runs.get(rid, [])):
            continue
        net = int(sum(made(rid, row) for t, row in runs.get(rid, []) if t >= now - NET_HOURS * 3600))
        verdict = ("at a loss: %d runs, %s cr in %d hours" % (loss[rid][0], format(loss[rid][1], ","), LOSS_HOURS) if rid in loss
                   else "its last %d runs each lost money: %s cr" % (late[rid][0], format(late[rid][1], ",")))
        level = entry.get("level") if entry and isinstance(entry.get("level"), int) else 0
        if level < 1:
            level, why = 1, verdict
        elif net > 0:
            level, why = 1, "lost again after its last rest; %s cr over %d hours keeps it at %d h: %s" % (format(net, "+,"), NET_HOURS, REST_HOURS[0], verdict)
        else:
            level, why = min(level + 1, len(REST_HOURS)), "lost again after its last rest: " + verdict
        out[rid] = {"from": utc(now), "until": utc(now + REST_HOURS[level - 1] * 3600), "why": why, "level": level, "net48": net}
        told.append("%s rests until %s (%d h, level %d, %s)" % (rid, utc(now + REST_HOURS[level - 1] * 3600, False), REST_HOURS[level - 1], level, why))
    return out, told


def keep_rests(routes, rows, now, data, loss, late, dry_run):
    """(the rests of this pass or None, [lines]): rest_book on the record, written back when it changed (a real pass
    only; under data/routes/rests.lock, written whole and then moved into place). A dry run writes nothing and says
    so. A fault here never stops the pass: without this pass's rests why_not reads the record as it stands."""
    path, lock, lines = rests_path(data), None, []
    try:
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            lock = open(path.with_name("rests.lock"), "w")
            fcntl.flock(lock, fcntl.LOCK_EX)
        before = read_json(path, {})
        book, told = rest_book(routes, rows, now, data, before if isinstance(before, dict) else {}, loss, late)
        lines += [("dry run, not written: " if dry_run else "") + line for line in told]
        if not dry_run and book != before:
            tmp = path.with_name("rests.json.%d.tmp" % os.getpid())
            tmp.write_text(json.dumps(book, indent=1, sort_keys=True) + "\n", encoding="ascii")
            os.replace(tmp, path)
        return book, lines
    except Exception as error:                               # noqa: BLE001  a bad record must not stop the dispatcher
        return None, lines + ["rests not kept this pass: %s: %s" % (type(error).__name__, error)]
    finally:
        if lock is not None:
            lock.close()


HELD_BACK = set()             # pilots already named as held back, so that a pass every 30 s names each once
ORPHAN_MINUTES = 5            # an engine loop without a fresh order file this long belongs to no runner
ORPHANS = {}                  # pilot -> when its loop was first seen without an order file
FUND_DOCK_WAIT = {}           # (leader, fund_at) -> epoch first held docked for wallet.py sweep
FUND_HOLD_SECS = 12 * 60      # two 5m passes max so the leader never freezes if sweep is off
FUND_TOLD = set()             # keys already logged once while waiting at dock
SEAT_HOLD_WAIT = {}           # pilot -> epoch first held idle for wallet.py sweep seat pass
SEAT_HOLD_SECS = 7 * 60       # one 5m pass + margin for queued seat invite/join
SEAT_BATCH_HOLD = 20          # max idle unseated pilots held per pass


def leader_of_empire(data):
    emp = read_json(Path(data) / "empire" / "empire.json", {}) or {}
    fac = emp.get("faction") if isinstance(emp, dict) else {}
    return str((fac or {}).get("leader") or "Prime Directive")


def leader_fund_action(name, ship, data, now, routes):
    """When an open treasury fund waits in data/fleet/funds.json, route the undocked leader to `park` once
    or hold the docked leader up to FUND_HOLD_SECS so the 5-minute wallet sweep can withdraw docked."""
    leader = leader_of_empire(data)
    if name != leader:
        return None, None
    frows = read_json(Path(data) / "fleet" / "funds.json", [])
    if not isinstance(frows, list):
        return None, None
    open_rows = [r for r in frows if isinstance(r, dict) and r.get("state") == "open" and now - float(r.get("at") or 0) < 24 * 3600]
    active_keys = {(leader, int(r.get("at") or 0)) for r in open_rows}
    for k in list(FUND_DOCK_WAIT):
        if k not in active_keys:
            FUND_DOCK_WAIT.pop(k, None)
            FUND_TOLD.discard(k)
    if not open_rows:
        return None, None
    todo = open_rows[0]
    key = (leader, int(todo.get("at") or 0))
    emp_d = read_json(Path(data) / "empire" / "empire.json", {}) or {}
    facs = (emp_d.get("facilities") or []) if isinstance(emp_d, dict) else []
    lboxes = {str(f.get("base")) for f in facs if isinstance(f, dict) and f.get("type") == "faction_lockbox" and f.get("status") == "active" and f.get("base")}
    dock_station = str(ship.get("docked") or "")
    at_valid_dock = bool(dock_station) and (not lboxes or dock_station in lboxes)
    if at_valid_dock:
        since = FUND_DOCK_WAIT.setdefault(key, now)
        if now - since < FUND_HOLD_SECS:
            return "hold", todo
        return None, None
    park_r = (routes.get("park-lockbox") or routes.get("park")) if isinstance(routes, dict) else None
    if key not in FUND_DOCK_WAIT and park_r is not None:
        return "park", park_r
    return None, None


def seat_hold_needed(name, data, now):
    """True when data/fleet/seats.json holds open seat picks and `name` (the leader or one of the next batch
    of queued pilots) should wait idle up to SEAT_HOLD_SECS for wallet.py sweep to invite and join it."""
    srows = read_json(Path(data) / "fleet" / "seats.json", [])
    if not isinstance(srows, list) or not srows:
        SEAT_HOLD_WAIT.clear()
        return False
    emp = read_json(Path(data) / "empire" / "empire.json", {}) or {}
    fac = (emp.get("faction") or {}) if isinstance(emp, dict) else {}
    mc, ml = int(fac.get("member_count") or 0), int(fac.get("members_limit") or 0)
    if ml and mc >= ml:
        SEAT_HOLD_WAIT.clear()
        return False
    open_pilots = [str(r.get("pilot")) for r in srows if isinstance(r, dict) and r.get("state") == "open"
                   and r.get("pilot") and now - float(r.get("at") or 0) < 6 * 3600]
    if not open_pilots:
        SEAT_HOLD_WAIT.clear()
        return False
    leader = str(fac.get("leader") or "Prime Directive")
    wanted = {leader} | set(open_pilots[:SEAT_BATCH_HOLD])
    for p in list(SEAT_HOLD_WAIT):
        if p not in wanted:
            SEAT_HOLD_WAIT.pop(p, None)
    if name not in wanted:
        return False
    since = SEAT_HOLD_WAIT.setdefault(name, now)
    return (now - since) < SEAT_HOLD_SECS


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
             "loss": losing(routes, rows, now), "late": lately_losing(routes, rows, now), "root": root, "pirates": pirates(data, now)}
    named = flagships(data)
    ammo = set(read_json(Path(data) / "catalog" / "ammo.json", []) or [])      # written by routemaker.py from the game's catalog
    lines = []
    if ENABLED_RESTS:                             # D227: this pass's rests, kept before any pilot is given a route
        book, told = keep_rests(routes, rows, now, data, state["loss"], state["late"], dry_run)
        lines += told
        if book is not None:
            state["rests"] = book
    lines += pull.keep(root, data, now, dry_run, state)      # r21: the two switches of this pass, and with pull-on the reserve's levels
    logs = Path(data) / "routes" / "logs"
    kinds, cap = hosting(data)
    hosted = runhost.load(data) if kinds and runhost.accepting(data, time.time()) else None      # runs the host has; None: no host takes runs now
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
        f_act, f_obj = leader_fund_action(name, ship, data, now, routes)
        if f_act == "hold":
            fkey = (name, int(f_obj.get("at") or 0))
            if fkey not in FUND_TOLD:
                FUND_TOLD.add(fkey)
                lines.append("%s held docked for open treasury fund (%s %s cr)" % (name, f_obj.get("pilot"), format(int(f_obj.get("credits") or 0), ",")))
            continue
        if seat_hold_needed(name, data, now):
            continue
        if f_act == "park" and f_obj is not None:
            route, argument = f_obj, None
        else:
            route, argument = pick(pilot, plan, routes, state)
        if route is None:
            continue
        what = ("census " + argument) if route["kind"] == "census" else route["kind"] + " " + route["id"]
        state["orders"][name] = what
        lines.append("%s -> %s" % (name, what))
        if dry_run:
            continue
        taken = division.order_of(name, data)      # requests ENT-289: read again right before the write; a hold taken during this pass stands
        if taken:
            state["orders"][name] = taken
            lines[-1] = "%s: `%s` not started: the pilot was taken during this pass (`%s`); it stays so, and gets work when that order ends" % (name, what, taken)
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
