#!/usr/bin/env python3
"""heldgate.py -- the gate `requires.held_below` of a route: open only while a division holds fewer units of a good than a number.

WHAT: the dispatcher's one rule (dispatch.why_not, and with it fill.py's reasons) asks closed() of every route; a route
      whose file carries `requires.held_below: {"item": "water_ice", "units": 5000, "division": "Mining"}` is open only
      while the units of that item held by the division's pilots stand under `units`: their personal storage at every
      station and their holds, as the storage book holds them (data/stock/storage.json, ledger.py, read about every 40
      minutes: totals.by_member and totals.holds_by_member, per member of the division).
      `division`: a division (Mining) or its Admiral (Zero); left out: the division whose class of work the route is
      (workclass.roles_for: a mine route is the miners', Mining's). `item` an item id, `units` a whole number above 0.
        show     every route that carries the field: what the division holds, the book's state, open or closed
RULES:
  - A book that is not whole (its entry `whole`, ledger.py: fewer than WHOLE_SHARE of the pilots read) reads less than
    the division holds, so it decides nothing: it closes nothing (a pilot that flew the route in the last RECENT hours,
    by the run rows, keeps it) and opens nothing new (every other pilot: `held_below: the storage book is not whole`).
    A book older than MAX_AGE hours counts as not whole. A book that does not say how whole it is is judged as it stands.
  - Off until the Fleet Admiral switches it on (ON below): while off, a route that carries the field stays closed
    (`held_below: the gate is off`), so no route that leans on the gate flies unbounded. `show` says what it would do.
  - The field is checked by `routes.py check` (faults()): item, units and division as above, nothing else.
  - It reads only: it moves no ship, writes no file.
WHY:  Zero, errors.log ENT-111: at the resume of 2026-11-21 six miners took Central Nexus ice routes on a bid of 371
      units while Mining stored 18,541 water ice; "stored ice is sold before new ice is mined" stood only in a turn skill.

USAGE:
  heldgate.py show [--root <dir>] [--data <dir>]
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
import division                                   # noqa: E402  the data folder, which member keeps which role

ON = False                     # the gate judges by the book; off: every route with the field stays closed (house rule: off until switched on)
RECENT = 2 * 60 * 60           # a book that is not whole keeps the route open to a pilot that flew it this recently
MAX_AGE = 3                    # hours: a book older than this counts as not whole (the ledger reads every pilot about every 40 minutes)
KEYS = ("item", "units", "division")
ITEM = re.compile(r"[a-z0-9_]{1,80}")
DIVISIONS = {"command": "Unity", "mining": "Zero", "trade": "Mercury", "logistics": "Apollo", "military": "Apophis", "intel": "Oracle"}   # plan.DIVISIONS
BOOK = {"path": None, "stamp": None, "book": {}}   # the storage book, read again only when the file changed


def need_of(route):
    """The route's `requires.held_below`, or None when it carries none."""
    need = ((route or {}).get("requires") or {}).get("held_below") if isinstance((route or {}).get("requires"), dict) else None
    return need if isinstance(need, dict) else None


def member_of(name):
    """The member a `division` value names (Mining or Zero), or ''."""
    word = str(name or "").strip()
    if word.capitalize() in division.MEMBERS:
        return word.capitalize()
    return DIVISIONS.get(word.lower(), "")


def keeper(route, rid=None):
    """The member whose division's stores the gate counts: the field's `division`, else the division of the route's own
    class of work (its first role, workclass.roles_for)."""
    need = need_of(route) or {}
    if need.get("division"):
        return member_of(need["division"])
    import workclass
    roles = workclass.roles_for(route, rid)
    return division.ROLES.get(roles[0], "") if roles else ""


def faults(need):
    """What is wrong with a route's `requires.held_below` (routes.py check): [] when nothing."""
    if not isinstance(need, dict):
        return ["`requires.held_below` must be {\"item\": \"<item id>\", \"units\": N, \"division\": \"<division>\"}"]
    out = []
    if not (isinstance(need.get("item"), str) and ITEM.fullmatch(need["item"])):
        out.append("`requires.held_below` needs `item`, an item id")
    units = need.get("units")
    if not isinstance(units, int) or isinstance(units, bool) or units < 1:
        out.append("`requires.held_below` of %s needs `units`, a whole number of 1 or more" % need.get("item"))
    if "division" in need and not member_of(need.get("division")):
        out.append("`requires.held_below` of %s: `division` must be a division (%s) or its Admiral" % (need.get("item"), ", ".join(sorted(d.capitalize() for d in DIVISIONS))))
    unknown = sorted(set(need) - set(KEYS))
    if unknown:
        out.append("`requires.held_below` of %s names fields no reader knows: %s" % (need.get("item"), ", ".join(unknown)))
    return out


def book(data):
    """The storage book (data/stock/storage.json), read again only when the file changed; {} when there is none."""
    path = Path(data) / "stock" / "storage.json"
    try:
        found = path.stat()
    except OSError:
        return {}
    stamp = (found.st_ino, found.st_mtime_ns, found.st_size)
    if BOOK["path"] != str(path) or BOOK["stamp"] != stamp:
        try:
            with open(path, encoding="utf-8") as handle:
                read = json.load(handle)
        except (OSError, ValueError):
            read = {}
        BOOK.update(path=str(path), stamp=stamp, book=read if isinstance(read, dict) else {})
    return BOOK["book"]


def epoch(text):
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except (TypeError, ValueError):
        return None


def held(found, member, item):
    """Units of `item` the member's division holds in the book: storage at every station plus the holds."""
    totals = found.get("totals") or {} if isinstance(found, dict) else {}
    stored = sum(int((goods or {}).get(item, 0) or 0) for goods in ((totals.get("by_member") or {}).get(member) or {}).values() if isinstance(goods, dict))
    return stored + int(((totals.get("holds_by_member") or {}).get(member) or {}).get(item, 0) or 0)


def whole(found, now):
    """(True when the book decides, why not): its entry `whole` (ledger.py) and its age."""
    entry = found.get("whole") if isinstance(found.get("whole"), dict) else None
    if entry is not None and "whole" in entry and not entry["whole"]:
        return False, "%d of %d pilots held" % (entry.get("held") or 0, entry.get("pilots") or 0)
    written = epoch(found.get("updated_at"))
    if written is None or now - written > MAX_AGE * 3600:
        return False, "written %s" % ("at an unknown time" if written is None else "%.1f hours ago" % ((now - written) / 3600))
    return True, ""


def closed(pilot, rid, route, state):
    """The dispatcher's hook (dispatch.why_not): why `requires.held_below` closes the route to the pilot now, or None."""
    need = need_of(route)
    if need is None:
        return None
    if not (state.get("held_gate_on") if "held_gate_on" in state else ON):
        return "held_below: the gate is off (heldgate.ON)"
    member, item, units = keeper(route, rid), str(need.get("item") or ""), need.get("units")
    if not member or not isinstance(units, int):
        return "held_below: the field does not read (routes.py check)"
    found = book(state.get("data") or division.DATA)
    if not found:
        return "held_below: no storage book (data/stock/storage.json)"
    have = held(found, member, item)
    decides, why = whole(found, state.get("now") or time.time())
    if not decides:
        mine = [epoch(r.get("started")) or 0 for r in state.get("rows") or [] if r.get("route") == rid and r.get("pilot") == (pilot or {}).get("name")]
        if mine and (state.get("now") or time.time()) - max(mine) < RECENT:
            return None                                    # it closes nothing: the pilot flew the route within RECENT
        return "held_below: the storage book is not whole (%s): %s reads %s %s, nothing opens on it" % (why, member, format(have, ","), item)
    if have >= units:
        return "held_below: %s holds %s %s, at or above %s" % (member, format(have, ","), item, format(units, ","))
    return None


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    if not args or args[0] != "show" or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    root, data = value("--root", str(Path(__file__).resolve().parent.parent)), value("--data", division.DATA)
    now = time.time()
    found = book(data)
    decides, why = whole(found, now) if found else (False, "no book")
    print("HELD_BELOW | the gate is %s | the storage book %s%s" % ("on" if ON else "off (heldgate.ON = False: every route with the field stays closed)",
                                                                  "decides" if decides else "decides nothing: ", why))
    for path in sorted((Path(root) / "routes").glob("*.json")):
        try:
            route = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            continue
        need = need_of(route)
        if need is None:
            continue
        member = keeper(route, path.stem)
        would = closed({"name": ""}, path.stem, route, {"data": data, "now": now, "rows": [], "held_gate_on": True})
        print("  %-44s %s of %s: %s held, under %s -> %s" % (path.stem[:44], need.get("item"), member or "?", format(held(found, member, str(need.get("item"))), ","),
                                                         need.get("units"), would or "open"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
