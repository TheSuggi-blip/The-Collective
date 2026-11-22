#!/usr/bin/env python3
"""reserves.py -- the gate `requires.reserve` of a route: open only while the last reading of a faction reserve (the fuel in a bunker, or an item of the faction's storage at a base) stands under a floor.

WHAT: the dispatcher's one rule (dispatch.why_not) asks closed() of every route; a route whose file carries
      `requires.reserve: {"base": "<base id>", "item": "fuel", "below": N, "max_age_minutes": M}` is open only while
      the newest reading of that reserve reads under N units. The readings, the newest wins:
        empire     data/empire/empire.json `faction_storage` (base, item, units, read_at): what empire.py collect
                   read through the leader's flagship, views only, every 15 minutes (the routes-index pass); the fuel
                   of a bunker is the row of item `fuel` (the faction's info: `fuel_bunkers`, `total_fuel_reserve`)
        bunker     for item `fuel`, the run rows of the route itself whose stop at that base holds the step `bunker`:
                   route_run.py reads `faction_fuel_reserve` there and notes `bunker +N fuel from M cells, reserve R`
                   (data/routes/runs.jsonl); its time is the run's end (routes.ended), so the reading after a supply
                   run counts at once and no second ship is sent on the reading from before it
        show       prints every route that carries the field: its reading, where from, its age, and open or closed
RULES:
  - A reading older than `max_age_minutes` (default MAX_AGE) closes the route: `reserve: not read for <age>`; no
    reading at all closes it: `reserve: not read`. A gate never opens on a reading nobody refreshed: the empire
    reading goes on every 15 minutes whether the route flies or not, so a closed route opens again by itself.
  - Off until the Fleet Admiral switches it on (the switch file data/fleet/reserve-gate-on, absent = off): while
    off, a route that carries the field stays closed, `reserve: the gate is off`, so no route that leans on the gate
    for its stop flies unbounded. `show` says what the gate would do in either state.
  - The field is checked by `routes.py check` (faults()): base a base id, item an item id (default `fuel`), below a
    whole number above 0, max_age_minutes a whole number above 0, nothing else.
  - It reads only: it moves no ship, writes no file.
WHY:  Apollo, requests.log ENT-266: the bunker route of our outpost at GSC-0044 was a budget (`once`, `max_pilots` 3)
      that its Admiral raised by hand each turn; without a stop, one ship puts about 2,600 fuel an hour into a bunker
      whose draw was 18 units in 2.5 hours. With the gate it is a standing route that keeps the bunker over a floor.

USAGE:
  reserves.py show [--root <dir>] [--data <dir>]
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the data folder

SWITCH = "reserve-gate-on"     # data/fleet/<this>: the gate judges by the readings; absent: every route with the field stays closed
MAX_AGE = 60                   # minutes a reading counts by default: the empire reading comes every 15 minutes
KEYS = ("base", "item", "below", "max_age_minutes")
BUNKER = re.compile(r"^bunker \+\d+ fuel from \d+ cells, reserve (\d+)$")     # route_run.py's note of its bunker step
BASE = re.compile(r"[a-z0-9_]{1,80}")               # a base id: a station's word id or an outpost's 32 hex digits
ITEM = re.compile(r"[a-z0-9_]{1,80}")
EMPIRE = {"path": None, "stamp": None, "rows": {}, "whole": {}}   # empire.json's faction storage, read again only when the file changed
RUNS = {"key": None, "found": {}}                    # the bunker readings of one list of run rows (one pass of the dispatcher)


def need_of(route):
    """The route's `requires.reserve` with its defaults, or None when it carries none."""
    need = ((route or {}).get("requires") or {}).get("reserve") if isinstance((route or {}).get("requires"), dict) else None
    if not isinstance(need, dict):
        return None
    return {"base": str(need.get("base") or ""), "item": str(need.get("item") or "fuel"), "below": need.get("below"),
            "max_age_minutes": need.get("max_age_minutes") if need.get("max_age_minutes") is not None else MAX_AGE}


def faults(need):
    """What is wrong with a route's `requires.reserve` (routes.py check): [] when nothing."""
    if not isinstance(need, dict):
        return ["`requires.reserve` must be {\"base\": \"<base id>\", \"item\": \"fuel\", \"below\": N}"]
    out = ["`requires.reserve` knows no `%s` (%s)" % (key, ", ".join(KEYS)) for key in sorted(need) if key not in KEYS]
    if not (isinstance(need.get("base"), str) and BASE.fullmatch(need["base"])):
        out.append("`requires.reserve.base` must be a base id (a station's id, or an outpost's 32 hex digits)")
    if "item" in need and not (isinstance(need["item"], str) and ITEM.fullmatch(need["item"])):
        out.append("`requires.reserve.item` must be an item id (`fuel` for a bunker)")
    for key in ("below", "max_age_minutes"):
        value = need.get(key)
        if (key == "below" or value is not None) and not (isinstance(value, int) and not isinstance(value, bool) and value > 0):
            out.append("`requires.reserve.%s` must be a whole number above 0" % key)
    return out


def stamp_of(text):
    """Seconds since the epoch of a UTC time written YYYY-MM-DDTHH:MM:SS..., or None (as dispatch.read_time reads it)."""
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return None


def empire_rows(data):
    """{(base, item): (units, epoch read, base name)} of the faction's storage in data/empire/empire.json."""
    path = Path(data) / "empire" / "empire.json"
    try:
        found = path.stat()
    except OSError:
        return {}
    stamp = (found.st_ino, found.st_mtime_ns, found.st_size)   # empire.py writes by os.replace: a new reading is a new inode
    if EMPIRE["path"] != str(path) or EMPIRE["stamp"] != stamp:
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            state = {}
        rows = {}
        for r in state.get("faction_storage") or [] if isinstance(state, dict) else []:
            if not (isinstance(r, dict) and isinstance(r.get("units"), (int, float)) and not isinstance(r.get("units"), bool)):
                continue
            at = stamp_of(r.get("read_at") or state.get("written_at"))
            if at is not None:
                rows[(str(r.get("base")), str(r.get("item")))] = (int(r["units"]), at, str(r.get("base_name") or r.get("base")))
        EMPIRE.update(path=str(path), stamp=stamp, rows=rows, whole=whole_bases(state))
    return EMPIRE["rows"]


def whole_bases(state):
    """{base: epoch} of the places whose faction storage the reading viewed whole (empire.py read_storage): each place
    of `faction_storage_places` that `faction_storage_error` does not name ("<name>: <why>"), at the reading's
    `written_at`. A place whose view failed keeps its old rows and is no whole reading."""
    at = stamp_of(state.get("written_at")) if isinstance(state, dict) else None
    if at is None:
        return {}
    error, out = str(state.get("faction_storage_error") or ""), {}
    for place in state.get("faction_storage_places") or []:
        if isinstance(place, dict) and place.get("base"):
            names = (str(place.get("base_name") or place["base"]), str(place["base"]))
            if not any(name + ":" in error for name in names):
                out[str(place["base"])] = at
    return out


def empire_whole(data):
    """{base: epoch} of the places the newest empire.json viewed whole, {} when it cannot be read."""
    path = Path(data) / "empire" / "empire.json"
    empire_rows(data)
    try:
        found = path.stat()
    except OSError:
        return {}
    same = EMPIRE["path"] == str(path) and EMPIRE["stamp"] == (found.st_ino, found.st_mtime_ns, found.st_size)
    return EMPIRE.get("whole") or {} if same else {}


def bunkers_at(route):
    """The base ids where the route's stops hold the step `bunker`."""
    return {str(stop.get("at")).split(":")[-1] for stop in route.get("stops") or [] if isinstance(stop, dict) and stop.get("bunker") and stop.get("at")}


def bunker_reading(route, rows):
    """(units, epoch of the run's end) of the newest bunker note among the route's own runs, or None."""
    rid = route.get("id")
    last = rows[-1] if rows and isinstance(rows[-1], dict) else {}
    key = (id(rows), len(rows), last.get("pilot"), last.get("started"))      # one list of one pass; a list of the same length and its last run
    if RUNS["key"] != key:
        RUNS.update(key=key, found={})
    if rid not in RUNS["found"]:
        import routes as routefiles                    # here, not at the top: routes.py's check imports this file
        best = None
        for row in rows:
            if row.get("route") != rid:
                continue
            for note in row.get("notes") or []:
                said = BUNKER.match(str(note))
                end = routefiles.ended(row) if said else None
                if said and end is not None and (best is None or end > best[1]):
                    best = (int(said.group(1)), int(end))
        RUNS["found"][rid] = best
    return RUNS["found"][rid]


def reading(data, route, rows):
    """The newest reading of the route's reserve: {units, at, source, name}, or None."""
    need = need_of(route)
    found = empire_rows(data).get((need["base"], need["item"]))
    best = {"units": found[0], "at": found[1], "source": "empire.json (empire.py collect)", "name": found[2]} if found else None
    if best is None and need["item"] != "fuel":     # requests ENT-315: a base viewed whole that lists no row of the item holds none
        at = empire_whole(data).get(need["base"])
        if at is not None:
            best = {"units": 0, "at": at, "source": "empire.json (empire.py collect): the base read whole, no row of the item", "name": need["base"]}
    if need["item"] == "fuel" and need["base"] in bunkers_at(route):
        run = bunker_reading(route, rows or [])
        if run and (best is None or run[1] > best["at"]):
            best = {"units": run[0], "at": run[1], "source": "its run's bunker step", "name": best["name"] if best else need["base"]}
    return best


def age_text(seconds):
    minutes = max(0, int(seconds // 60))
    return "%d min" % minutes if minutes < 120 else "%.1f h" % (minutes / 60.0)


def gate_on(data):
    return (Path(data) / "fleet" / SWITCH).exists()


def judge(data, route, rows, now):
    """Why the reserve closes the route by the readings (the gate's switch aside), or None when it is open."""
    need = need_of(route)
    if need is None:
        return None
    if faults(((route.get("requires") or {}).get("reserve"))):
        return "reserve: the field is not valid (routes.py check)"
    found = reading(data, route, rows)
    if found is None:
        return "reserve: not read"
    age = now - found["at"]
    if age > need["max_age_minutes"] * 60:
        return "reserve: not read for %s" % age_text(age)
    if found["units"] >= need["below"]:
        return "reserve: %s %s at %s, not under %s (read %s ago)" % (need["item"], format(found["units"], ","), found["name"], format(need["below"], ","), age_text(age))
    return None


def closed(route, state):
    """The dispatcher's hook (dispatch.why_not): why `requires.reserve` closes the route now, or None."""
    if need_of(route) is None:
        return None
    if not gate_on(state["data"]):
        return "reserve: the gate is off (data/fleet/%s absent)" % SWITCH
    return judge(state["data"], route, state.get("rows") or [], state["now"])


def show(root, data, now=None):
    """Every route that carries `requires.reserve`, with its reading and what the gate says (the dry run)."""
    now = time.time() if now is None else now
    import dispatch                                    # here, not at the top: dispatch.py imports this file
    routes = dispatch.load_routes(root)
    rows = dispatch.run_rows(data)
    named = [(rid, route) for rid, route in sorted(routes.items()) if isinstance(route, dict) and need_of(route) is not None]
    print("RESERVE GATE | %s | %d route(s) carry requires.reserve" % ("on" if gate_on(data) else "off (data/fleet/%s absent): every such route stays closed" % SWITCH, len(named)))
    for rid, route in named:
        need, found = need_of(route), reading(data, route, rows)
        read = ("%s %s, read %s ago from %s" % (need["item"], format(found["units"], ","), age_text(now - found["at"]), found["source"])) if found else "not read"
        why = judge(data, route, rows, now)
        print("  %s | below %s at %s | %s | would be %s" % (rid, format(need["below"], ",") if isinstance(need["below"], int) else need["below"], need["base"], read,
                                                            ("closed: " + why) if why else "open"))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] != "show" or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    return show(value("--root", str(here.parent)), value("--data", division.DATA))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
