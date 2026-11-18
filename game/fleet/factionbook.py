#!/usr/bin/env python3
"""factionbook.py -- the faction's storage in the storage book: the entry `Faction` of data/stock/storage.json, so that the tools stock, surplus.py and the table holdings count what lies in the Lockboxes and at our outposts.

WHAT: the service `ledger` calls put() in every pass: it sets book["pilots"]["Faction"] to what the faction's
      storage holds at each place where it stores, {member: Faction, read_at, stations: {base id: {item: units}},
      source}, from the faction's own reading: data/empire/empire.json `faction_storage`, which empire.py collect
      reads through the leader's flagship (storage `view`, target faction, station_id <base>: a view, it answers from
      anywhere) every 15 minutes, one view per place. The book's totals then hold it per station (by_station) and as
      the member `Faction` (by_member); the store loads it into holdings as pilot and member `Faction`.
        show   prints the entry as the book would hold it now
RULES:
  - One reading, never two: the faction's storage is read by empire.py alone, and the book takes that reading as it
    stands (the brief: no info doubled). No game call here, no trip, no docked pilot.
  - Items only: the fuel of a bunker (item `fuel`, a tank, no item of storage) stays in empire.json and the table
    faction_storage.
  - The entry's read_at is the oldest reading of its places (a place whose view failed keeps its rows and its time);
    an error of the last reading is kept as `error`. No reading of the faction yet: no entry; a reading that holds
    no goods: an entry with no stations.
  - The entry is no pilot: the ledger never reads it through the gate and never takes it out with the pilots the
    fleet file no longer names.
WHY:  Apollo, requests.log ENT-267: the table holdings knew no faction storage while routes put goods there (155 iron
      ore at the outpost, the Recruitment Center's 285 flex polymer into the faction store at Node Beta); the reserve
      read flex 15 of 300 after they landed, and a member who read it might buy them twice.

USAGE:
  factionbook.py show [--data <dir>]
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the data folder

MEMBER = "Faction"            # the entry's name in book["pilots"] and its member in the totals and the table holdings
TANK = "fuel"                 # the bunker's fuel: a tank, not an item of storage


def entry(data):
    """The faction's entry of the storage book from data/empire/empire.json, or None while no reading holds the faction's
    storage."""
    try:
        state = json.loads((Path(data) / "empire" / "empire.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(state, dict) or not isinstance(state.get("faction_storage"), list):
        return None
    stations, times = {}, []
    for row in state["faction_storage"]:
        if not isinstance(row, dict) or not row.get("base") or not row.get("item") or row.get("item") == TANK:
            continue
        units = row.get("units")
        if not isinstance(units, int) or isinstance(units, bool) or units <= 0:
            continue
        goods = stations.setdefault(str(row["base"]), {})
        goods[str(row["item"])] = goods.get(str(row["item"]), 0) + units
        if row.get("read_at"):
            times.append(str(row["read_at"]))
    times += [str(state["written_at"])] if state.get("written_at") else []
    out = {"member": MEMBER, "read_at": min(times) if times else "", "stations": stations, "source": "the faction's storage as empire.py collect read it (data/empire/empire.json, faction_storage)"}
    if state.get("faction_storage_error"):
        out["error"] = str(state["faction_storage_error"])[:300]
    return out


def put(book, data):
    """Set the faction's entry in the book (its `pilots`); True when it changed, so the ledger writes the book again."""
    found = entry(data)
    pilots = book.setdefault("pilots", {})
    if found is None or pilots.get(MEMBER) == found:
        return False
    pilots[MEMBER] = found
    return True


def show(data):
    found = entry(data)
    if found is None:
        print("FACTION BOOK | no reading of the faction's storage yet (empire.py collect writes data/empire/empire.json)")
        return 1
    print("FACTION BOOK | the entry `%s` of the storage book | oldest reading %s | %d place(s) with goods%s" % (
        MEMBER, found["read_at"] or "not read", len(found["stations"]), " | NOT READ: %s" % found["error"] if found.get("error") else ""))
    for base, goods in sorted(found["stations"].items()):
        print("  %s: %s" % (base, ", ".join("%s %s" % (item, format(units, ",")) for item, units in sorted(goods.items(), key=lambda g: (-g[1], g[0])))))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] != "show" or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    return show(args[args.index("--data") + 1] if "--data" in args and args.index("--data") + 1 < len(args) else division.DATA)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
