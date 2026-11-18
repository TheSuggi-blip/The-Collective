#!/usr/bin/env python3
"""pull.py -- each class flies its own work, and goods are gathered only while the reserve needs them: the class guard and the pull rule of the dispatcher, with their dry run.

WHAT: two closing reasons of the dispatcher's one rule (dispatch.why_not calls closes()), each behind its own switch
      file, and the dry run Unity reads before she switches them on:
        class guard  a route that is not the pilot's own class of work (workclass.own: its kind, its stops, its id
                     and its file's `open_to`) is refused: `class: <class> is <roles>' work`
        pull rule    a route that brings goods of the reserve and earns nothing (it sells nothing and takes no
                     mission) is closed while every good it brings stands full: `full: <item> <held> of max <max>`
      A good of the reserve is an item the reserve's walk asks for (surplus.py: demand above 0) or that a `max` or
      `min` line of game/reserve.tsv names. Its levels: max = the file's `max` line, else what the reserve asks of it
      (its demand); min = the file's `min` line, else 90 percent of max rounded up. What it holds is surplus.py's `held` (station
      storage and the holds: craftbook.inventory), one number per good. What a route brings: a mine route the
      resources its field (`belt`) holds by its last census (dispatch.field_left; without a census the goods of its
      `min_left`), a circuit those of its mine steps and the outputs of the recipes of its craft stops (the catalog's,
      else the step's `makes`). A route that hunts, buys without crafting, carries or reads brings nothing here.
        check    the dry run on the live files, per division: the plan rows the class guard would refuse (route,
                 class, the ships whose own list holds it), the routes the pull rule would close now with each good
                 and its level, and per role how many ships start and how many wait when the dispatcher's next pass
                 is played with both rules off and with both on
        levels   per good of the reserve: held, need, min, max, full or open, since when and until when
RULES:
  - The class guard acts only while data/fleet/class-guard-on exists, the pull rule only while data/fleet/pull-on
    exists (absent = off: the dispatcher's rule is what it was). Rule F23: gathering is the miners' work; a mission
    that pays once, selling or crafting a ship's own stores, fitting and training stay open to every role
    (workclass.SHARED).
  - Hysteresis: a good becomes full when it holds its max or more and stays full until it holds less than its min;
    between the two it keeps what it was. A full mark carries its own end: FULL_HOURS after the last reading at max
    or above it lapses, whatever lies between min and max. A storage book older than BOOK_HOURS measures nothing: no
    good is full then.
  - The record data/routes/pull.json (the levels, the marks, what each field and recipe yields) is written by the
    dispatcher's real pass alone, read again at most every EVERY seconds, and carries its own end (`until`,
    RECORD_HOURS after its writing): a record past its end closes nothing. A dry pass and `check` write nothing.
  - A route that also brings a good outside the reserve, earns (sells, takes a mission), pays once, or whose goods
    are not known is never closed by the pull rule: that is its Admiral's call.
  - It reads only (the record aside): it moves no ship and changes no plan.
WHY:  2026-11-17: the reserve's iron was met, yet traders, haulers, drones and scouts gathered iron for one to two hours
      more, until a fleet-wide order docked them: the filler lent the miners' routes to every waiting ship, and no route
      stopped by itself when its good was full (a target, no stop level: push, not pull). Suggi, 2026-11-18: "Ore is
      miners job"; "We have division of labor, not all on same job, they have different ship utilities."

USAGE:
  pull.py check [<division>|<Member>|all] [--now <UTC time>]   the dry run: what the two rules would refuse and close, who would wait
  pull.py levels [--now <UTC time>]                             the goods of the reserve with their levels and marks
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import math
import os
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import workclass                                  # noqa: E402  whose work a route is: the one answer

# dispatch.py imports this file: dispatch, surplus, craftbook, fill and plan are imported inside the functions that need them.

GUARD_SWITCH = "fleet/class-guard-on"   # under the data folder: the class guard acts while it exists (r21, off until Unity read the dry run)
PULL_SWITCH = "fleet/pull-on"           # under the data folder: the pull rule acts while it exists (r21, off until Unity read the dry run)
RECORD = "routes/pull.json"             # under the data folder: the levels and the marks, written by the dispatcher's real pass
EVERY = 300                   # seconds: the dispatcher reads the levels again at most this often (surplus.py takes about a second)
RECORD_HOURS = 1              # a record not written again within this closes nothing (the dispatcher stopped)
FULL_HOURS = 6                # a full mark lapses this long after its last reading at max or above
BOOK_HOURS = 3                # a storage book older than this measures nothing
MIN_SHARE = 0.9               # min = 90 percent of max, rounded up, where game/reserve.tsv names no min (max 1: min 1)
FORCE = {}                    # check() sets {"class_guard": bool, "pull": record or None} for its own played pass; empty elsewhere
SWITCHES = {}                 # (data, file) -> (now, exists): one look per clock reading of the caller
CACHE = {"path": None, "stamp": None, "record": None}      # the record as read, read again when the file changed
PLURAL = {"command": "command ships"}
num = "{:,}".format


def stamp(epoch):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))


def epoch(text):
    """Seconds of a UTC time written YYYY-MM-DDTHH:MM:SS...; None when it does not read."""
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return None


# ---- the switches

def switch(data, name, now=None):
    """True while the switch file `name` exists under the data folder; one look per (data, now), so that a pass of the
    dispatcher or of fill.py that asks thousands of times reads the disk once. No data folder: off."""
    if not data:
        return False
    key = (str(data), name)
    seen = SWITCHES.get(key)
    if now is not None and seen is not None and seen[0] == now:
        return seen[1]
    found = (Path(data) / name).exists()
    if len(SWITCHES) > 64:
        SWITCHES.clear()
    SWITCHES[key] = (now, found)
    return found


def guard_on(state):
    """The class guard's state for this call: check()'s own setting, the pass's (state["class_guard"]), else its file."""
    if "class_guard" in FORCE:
        return bool(FORCE["class_guard"])
    if "class_guard" in state:
        return bool(state["class_guard"])
    return switch(state.get("data"), GUARD_SWITCH, state.get("now"))


def pull_record(state):
    """The pull rule's record for this call, or None (off, no record, or a record past its end): check()'s own, the
    pass's (state["pull"]), else the file while its switch file exists."""
    if "pull" in FORCE:
        return FORCE["pull"]
    if "pull" in state:
        return state["pull"]
    if not switch(state.get("data"), PULL_SWITCH, state.get("now")):
        return None
    record = read_record(state.get("data"))
    return record if in_force(record, state.get("now")) else None


# ---- the class guard

def role_words(roles):
    """`miners`, `traders and haulers`, `drones, sentinels, scouts and command ships`."""
    names = [PLURAL.get(role, role + "s") for role in roles] or ["nobody"]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def class_reason(role, route, rid):
    """Why a route is not a ship of `role`'s own work (rule F23), or None: `class: gather is miners' work`."""
    if workclass.own(role, route, rid):
        return None
    return "class: %s is %s' work" % (workclass.work_class(route, rid), role_words(workclass.roles_for(route, rid)))


# ---- the pull rule

def earns(route):
    """True for a route that sells (a mine route's `sell`, a stop's `sell`) or takes a mission (a stop's `accept`)."""
    if route.get("sell"):
        return True
    return any(isinstance(stop, dict) and (stop.get("sell") or stop.get("accept")) for stop in route.get("stops") or [])


def places_of(route):
    """[(place, its min_left floor)] of the fields a route mines: a mine route's belt, a circuit's mine steps."""
    if route.get("kind") == "mine":
        return [(str(route.get("belt") or ""), route.get("min_left") if isinstance(route.get("min_left"), dict) else {})]
    out = []
    for stop in route.get("stops") or []:
        for step in (stop.get("mine") or []) if isinstance(stop, dict) and isinstance(stop.get("mine"), list) else []:
            if isinstance(step, dict):
                out.append((str(step.get("at") or step.get("belt") or ""), step.get("min_left") if isinstance(step.get("min_left"), dict) else {}))
    return out


def crafts_of(route):
    """[(recipe, makes)] of the craft jobs of a circuit's stops."""
    out = []
    for stop in route.get("stops") or []:
        jobs = stop.get("craft") if isinstance(stop, dict) else None
        for job in jobs if isinstance(jobs, list) else [jobs] if isinstance(jobs, dict) else []:
            if isinstance(job, dict):
                out.append((str(job.get("recipe") or ""), str(job.get("makes") or "")))
    return out


def brings(route, record):
    """The goods a route brings, sorted; None when they are not known or the route brings something this rule cannot
    judge (a hunt's loot). A mine route: what its field holds by the record (`yields`, from the last census), else the
    goods of its floor (`min_left`); a circuit: the same of its mine steps and the outputs of its craft stops' recipes."""
    if route.get("kind") not in ("mine", "circuit"):
        return None
    if any(isinstance(stop, dict) and stop.get("hunt") for stop in route.get("stops") or []):
        return None
    goods = set()
    for place, floor in places_of(route):
        found = (record.get("yields") or {}).get(place)
        if not found and not floor:
            return None                                  # a field of unknown yield: nothing is judged
        goods.update(found or floor)
    for recipe, makes in crafts_of(route):
        found = (record.get("makes") or {}).get(recipe) or ([makes] if makes else [])
        if not found:
            return None
        goods.update(found)
    return sorted(goods) or None


def full_now(entry, now):
    """True while a good's mark says full and its own end has not come."""
    if not isinstance(entry, dict) or not entry.get("full"):
        return False
    until = epoch(entry.get("until"))
    return until is not None and (now is None or now < until)


def full_reason(route, rid, record, now=None):
    """Why the pull rule closes a route, or None: it earns nothing, pays not once, and every good it brings is a good of
    the reserve that stands full. `full: iron_ore 251,133 of max 185,470` (several goods: one part each, with `; `)."""
    if not record or earns(route) or workclass.work_class(route, rid) == "once":
        return None
    goods = brings(route, record)
    if not goods:
        return None
    items, parts = record.get("items") or {}, []
    for item in goods:
        entry = items.get(item)
        if not full_now(entry, now):
            return None                                  # a good outside the reserve, or one that is not full: open
        parts.append("%s %s of max %s" % (item, num(entry["held"]), num(entry["max"])))
    return "full: " + "; ".join(parts)


def closes(pilot, rid, route, state):
    """The dispatcher's hook (dispatch.why_not): the class guard's reason, then the pull rule's, each only while its
    switch is on; None when neither closes the route (both off: always None)."""
    if guard_on(state):
        role = pilot.get("role") or str(pilot.get("name") or "").split("-")[0]
        why = class_reason(role, route, rid)
        if why:
            return why
    record = pull_record(state)
    return full_reason(route, rid, record, state.get("now")) if record else None


# ---- the levels and the record

def levels(res):
    """{item: {held, need, max, min, set}} of every good of the reserve (surplus.surplus's answer `res`): an item its
    walk asks for, or one a `max`/`min` line names. A good whose max comes out at 0 or less has no level."""
    named = res.get("levels") or {}
    rows = {r["id"]: r for r in res.get("rows") or []}
    out = {}
    for item in sorted({i for i, r in rows.items() if (r.get("demand") or 0) > 0} | set(named)):
        row, line = rows.get(item) or {}, named.get(item) or {}
        need = int(row.get("demand") or 0)
        top = line.get("max") if line.get("max") is not None else need
        if top <= 0:
            continue
        low = line.get("min") if line.get("min") is not None else math.ceil(top * MIN_SHARE)
        out[item] = {"held": int(row.get("held") or 0), "need": need, "max": int(top), "min": int(min(low, top)),
                     "set": "file" if line else "need"}
    return out


def mark(level, before, now, fresh):
    """One good's level with its mark, from the mark before: full at max or above (its end renewed), open below min,
    between the two what it was while its end has not come. A storage book that is not fresh marks nothing full."""
    entry = dict(level)
    was = full_now(before, now)
    if not fresh:
        entry.update(full=False, why="the storage book is not fresh: not measured")
    elif level["held"] >= level["max"]:
        entry.update(full=True, since=before.get("since") if was else stamp(now), until=stamp(now + FULL_HOURS * 3600))
    elif level["held"] < level["min"] or not was:
        entry.update(full=False)
    else:
        entry.update(full=True, since=before.get("since"), until=before.get("until"))
    return entry


def yields_of(data, routes, now):
    """({place: [resources its last census reads above 0]} of every field a route mines, {recipe: [outputs]} of every
    recipe a route crafts by the catalog)."""
    import craftbook                              # the catalog
    import dispatch                               # the one reader of a field (field_left)
    found, makes = {}, {}
    for route in routes.values():
        for place, _floor in places_of(route):
            if place and place not in found and len(place.split(":")) == 2:
                left = dispatch.field_left(data, place, now, fresh=float("inf")) or {}
                found[place] = sorted(item for item, units in left.items() if units > 0)
    cat = craftbook.load(data) or {}
    recipes = cat.get("recipes") or {}
    for route in routes.values():
        for recipe, _makes in crafts_of(route):
            outputs = [o.get("item_id") for o in (recipes.get(recipe) or {}).get("outputs") or [] if isinstance(o, dict) and o.get("item_id")]
            if recipe and outputs:
                makes[recipe] = sorted(set(outputs))
    return {place: goods for place, goods in found.items() if goods}, makes


def make_record(root, data, now, before=None, res=None, routes=None):
    """(the record at `now`, [the marks that changed, one line each]) from surplus.py's answer (read here when `res` is
    None), the route files and the record before. root is the game/ folder."""
    import dispatch
    import surplus
    res = surplus.surplus(data, str(Path(root).parent)) if res is None else res
    routes = dispatch.load_routes(root) if routes is None else routes
    book = epoch(res.get("written"))
    fresh = book is not None and now - book <= BOOK_HOURS * 3600
    old = (before or {}).get("items") or {}
    items, told = {}, []
    for item, level in levels(res).items():
        entry = mark(level, old.get(item) or {}, now, fresh)
        items[item] = entry
        if entry["full"] and not full_now(old.get(item), now):
            told.append("%s full: %s of max %s; routes that only bring it close until it holds less than %s" % (item, num(entry["held"]), num(entry["max"]), num(entry["min"])))
        elif full_now(old.get(item), now) and not entry["full"]:
            told.append("%s open again: %s, below its min %s%s" % (item, num(entry["held"]), num(entry["min"]),
                                                                    "" if fresh else " (the storage book is not fresh)"))
    found, makes = yields_of(data, routes, now)
    record = {"what": "the reserve's pull levels (pull.py): per good held, need, min, max and its mark; what each field and recipe yields",
              "written_at": stamp(now), "until": stamp(now + RECORD_HOURS * 3600), "book": res.get("written") or None,
              "book_fresh": fresh, "catalog": res.get("catalog"), "items": items, "yields": found, "makes": makes}
    return record, told


def record_path(data):
    return Path(data) / RECORD


def read_record(data):
    """The record as the file holds it, read again only when the file changed; None without one."""
    if not data:
        return None
    path = record_path(data)
    try:
        found = path.stat()
    except OSError:
        return None
    key = (found.st_ino, found.st_mtime_ns, found.st_size)
    if CACHE["path"] != str(path) or CACHE["stamp"] != key:
        try:
            record = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            record = None
        CACHE.update(path=str(path), stamp=key, record=record if isinstance(record, dict) else None)
    return CACHE["record"]


def in_force(record, now):
    """True for a record whose own end has not come."""
    until = epoch((record or {}).get("until"))
    return until is not None and (now is None or now < until)


def write_record(data, record):
    path = record_path(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(".%s.%d.tmp" % (path.name, os.getpid()))
    tmp.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="ascii")
    os.replace(tmp, path)


def keep(root, data, now, dry_run, state):
    """The dispatcher's hook (one_pass): the two switches read once for the pass into `state` (class_guard, pull), and
    with the pull rule on the record of levels, made again when it is EVERY seconds old (a real pass writes it; a dry
    pass says what it would write). [lines] of what changed. A fault here never stops the pass: the pull rule then
    closes nothing this pass."""
    state["class_guard"] = switch(data, GUARD_SWITCH, now)
    state["pull"] = None
    if not switch(data, PULL_SWITCH, now):
        return []
    lines = []
    try:
        before = read_record(data)
        written = epoch((before or {}).get("written_at"))
        record = before
        if before is None or written is None or now - written >= EVERY or now < written:
            record, told = make_record(root, data, now, before)
            if not dry_run:
                write_record(data, record)
            lines += [("dry run, not written: " if dry_run else "") + "pull: " + line for line in told]
        state["pull"] = record if in_force(record, now) else None
    except Exception as error:                               # noqa: BLE001  a bad file must not stop the dispatcher
        lines.append("pull levels not read this pass: %s: %s" % (type(error).__name__, error))
    return lines


# ---- the dry run

def dry_fleet(fill, root, data, now, guard, record):
    """fill.survey played with both rules set by hand (FORCE): {role: (ships, starting, waiting)} and the survey. FORCE is
    set on the module the dispatcher calls (run as a script, this file is __main__ and dispatch.py holds its own copy)."""
    force = fill.dispatch.pull.FORCE
    force.clear()
    force.update(class_guard=guard, pull=record)
    try:
        seen = fill.survey(root, data, now)
    finally:
        force.clear()
    return {role: (crew["ships"], len(crew["starting"]), len(crew["waiting"])) for role, crew in seen["crews"].items()}, seen


def starts_on(seen, role, routes, record, now):
    """(ships of the role that start on another class's work, on a route the pull rule closes, on park: dock and wait)
    in a played pass."""
    other = full = park = 0
    for _name, rid in (seen["crews"].get(role) or {}).get("starting") or []:
        route = routes.get(rid) or {}
        other += 0 if workclass.own(role, route, rid) else 1
        full += 1 if full_reason(route, rid, record, now) else 0
        park += 1 if route.get("park") else 0
    return other, full, park


def check(root, data, word, now):
    import fill                                   # the survey: the dispatcher's next pass played for every free pilot
    import plan as planfile
    import surplus
    division_of = planfile.division_of
    res = surplus.surplus(data, str(Path(root).parent))
    routes = fill.dispatch.load_routes(root)
    record, _told = make_record(root, data, now, read_record(data), res=res, routes=routes)
    roles, _owners, _errors = fill.division.load_plan(root)
    lists = fill.dispatch.own_lists(data)
    named = fill.dispatch.flagships(data)
    fleet = fill.dispatch.read_json(Path(data) / "fleet" / "fleet.json", {})
    ships = [s for s in (fleet.get("ships") or [] if isinstance(fleet, dict) else []) if isinstance(s, dict) and s.get("name")]
    chosen = sorted(planfile.DIVISIONS) if word in ("", "all") else [division_of(word)] if division_of(word) else None
    if not chosen:
        print("PULL | `%s` is no division, member or role" % word)
        return 1
    off, seen_off = dry_fleet(fill, root, data, now, False, None)
    on, seen_on = dry_fleet(fill, root, data, now, True, record)
    full = sorted(item for item, entry in record["items"].items() if entry["full"])
    print("PULL | the dry run of the class guard (%s) and the pull rule (%s), both off now unless their files exist | clock %s | storage book of %s (%s) | "
          "catalog %s | fleet file of %s, %d ships | %d goods of the reserve, %d full"
          % (GUARD_SWITCH, PULL_SWITCH, stamp(now), res.get("written") or "--", "fresh" if record["book_fresh"] else "NOT fresh: no good is full",
             res.get("catalog"), (fleet.get("updated_at") if isinstance(fleet, dict) else None) or "--", len(ships), len(record["items"]), len(full)))
    print("  switch files now: class-guard-on %s, pull-on %s" % ("present" if switch(data, GUARD_SWITCH) else "absent",
                                                                  "present" if switch(data, PULL_SWITCH) else "absent"))
    if not ships:
        print("  the fleet file lists no ship: who would wait is not measured (the rules act per pilot; with no ship they close nothing)")
    for item in full:
        entry = record["items"][item]
        print("  FULL %-22s held %12s  max %12s  min %12s  (%s)" % (item, num(entry["held"]), num(entry["max"]), num(entry["min"]),
                                                                    "need" if entry["set"] == "need" else "game/reserve.tsv"))
    total = Counter()
    for name in chosen:
        mine = planfile.roles_of(name)
        print("%s (%s) | roles %s" % (name, planfile.DIVISIONS[name], ", ".join(mine)))
        for role in mine:
            ids = roles.get(role) or []
            crew = [s["name"] for s in ships if fill.dispatch.role_of(s["name"], named) == role]
            refused = [(rid, workclass.work_class(routes[rid], rid)) for rid in ids if rid in routes and not workclass.own(role, routes[rid], rid)]
            print("  %s: %d routes in its plan, %d the class guard would refuse%s" % (role, len(ids), len(refused), ":" if refused else ""))
            for rid, cls in refused:
                holders = sum(1 for ship in crew if rid in (lists.get(ship) or ids))
                print("     REFUSED %-42s %-7s %s; in the list of %d of its %d ships" % (rid[:42], cls, class_reason(role, routes[rid], rid), holders, len(crew)))
            closed = [(rid, full_reason(routes[rid], rid, record, now)) for rid in ids if rid in routes and routes[rid].get("status") != "off"]
            closed = [(rid, why) for rid, why in closed if why]
            print("  %s: %d routes of its plan the pull rule would close now%s" % (role, len(closed), ":" if closed else ""))
            for rid, why in closed:
                print("     CLOSED  %-42s %s" % (rid[:42], why))
            n, start_off, wait_off = off.get(role, (len(crew), 0, 0))
            _n, start_on, wait_on = on.get(role, (len(crew), 0, 0))
            bare = sum(1 for ship in crew if not any(rid in routes and workclass.own(role, routes[rid], rid) and routes[rid].get("status") != "off"
                                                     and not routes[rid].get("park") for rid in (lists.get(ship) or ids)))
            other, filling, park_off = starts_on(seen_off, role, routes, record, now)
            _other, _filling, park_on = starts_on(seen_on, role, routes, record, now)
            print("  %s: %d ships | both rules off: %d start (%d of them on another class's work, %d on a route the pull rule closes, %d on park), %d wait "
                  "| both on: %d start (%d on park), %d wait | no work open, park or wait: %d off, %d on (%+d) | ships whose list holds no route of "
                  "their class but park: %d" % (role, n, start_off, other, filling, park_off, wait_off, start_on, park_on, wait_on, park_off + wait_off,
                                                park_on + wait_on, park_on + wait_on - park_off - wait_off, bare))
            waits = Counter(reason for _rid, counts in (seen_on["crews"].get(role) or {}).get("reasons", {}).items() for reason in counts
                            if reason.startswith(("class: ", "full: ")))
            if waits:
                print("     what the two rules close to its waiting ships, route by route: %s" % ", ".join("%s %d" % kv for kv in waits.most_common(4)))
            total.update(ships=n, off=wait_off + park_off, on=wait_on + park_on, refused=len(refused), closed=len(closed), other=other, filling=filling)
    print("SUM | %d ships | both rules off: %d with no work open (park or wait), %d start on another class's work, %d on a route the pull rule closes "
          "| both on: %d with no work open | plan rows refused by the class guard %d | plan rows closed by the pull rule %d"
          % (total["ships"], total["off"], total["other"], total["filling"], total["on"], total["refused"], total["closed"]))
    chains(data, record)
    print("Rule F23: each class flies its own work; gathering is the miners'. The pull rule: a route that only brings goods of the reserve and earns "
          "nothing closes when every one of them holds its max, and opens again when one falls below its min.")
    return 0


def chains(data, record):
    """The supply chains (supply.py, the store's read copy) whose item has a pull level: a keep above the level's min keeps
    duty putting sources into a plan that the pull rule closes."""
    try:
        import supply
        rows = supply.read(data)["rows"]
    except Exception as error:                               # noqa: BLE001  no read copy: said, nothing else
        print("  supply chains not read: %s: %s" % (type(error).__name__, error))
        return
    for row in rows:
        entry = (record.get("items") or {}).get(row.get("item"))
        if entry and row.get("keep") is not None and row["keep"] > entry["min"]:
            print("  NOTE chain %s (%s, keeper %s): keep %s stands above the pull min %s (max %s): supply.py duty puts its sources into the plan while the "
                  "pull rule closes them; one number per good: set the chain's keep at or below the min, or a `max %s` line in game/reserve.tsv"
                  % (row["chain"], row["item"], row["keeper"], num(row["keep"]), num(entry["min"]), num(entry["max"]), row["item"]))


def show_levels(root, data, now):
    record = read_record(data)
    kept = "the record %s, written %s%s" % (RECORD, record.get("written_at"), "" if in_force(record, now) else " (past its end: it closes nothing)") if record else "no record yet"
    record, _told = make_record(root, data, now, record)
    print("LEVELS | the goods of the reserve and their pull levels, read now (%s) | storage book of %s (%s) | %s"
          % (stamp(now), record.get("book") or "--", "fresh" if record["book_fresh"] else "NOT fresh", kept))
    print("  %-28s %12s %12s %12s %12s  %-5s %s" % ("item", "held", "need", "min", "max", "mark", "since / until"))
    for item, entry in sorted(record["items"].items(), key=lambda kv: (not kv[1]["full"], kv[0])):
        print("  %-28s %12s %12s %12s %12s  %-5s %s" % (item[:28], num(entry["held"]), num(entry["need"]), num(entry["min"]), num(entry["max"]),
                                                        "FULL" if entry["full"] else "open", "%s / %s" % (entry.get("since"), entry.get("until")) if entry["full"] else ""))
    print("max = game/reserve.tsv's `max` line, else what the reserve asks (need); min = its `min` line, else 90 percent of max; held = station storage and holds")
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    import division
    root, data = value("--root", str(here.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data", "--now"))]
    if not words or words[0] not in ("check", "levels") or any(a in ("-h", "--help") for a in args):
        print(__doc__.split("USAGE:")[1].split("Stdlib")[0].rstrip())
        return 2
    now = epoch(value("--now", "")) if "--now" in args else time.time()
    if now is None:
        print("--now takes a UTC time YYYY-MM-DDTHH:MM:SSZ")
        return 2
    if words[0] == "levels":
        return show_levels(root, data, now)
    return check(root, data, words[1] if len(words) > 1 else "all", now)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
