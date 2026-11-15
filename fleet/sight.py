#!/usr/bin/env python3
"""sight.py -- what our ships see where they are: the pilots they meet, and a first read of a system nobody read.

WHAT: every 30 s it reads the fleet's live file (data/fleet/fleet.json). For
      each place (system and POI) one of our ships is at, and that was not
      looked at in the last ten minutes, it asks the game through that ship
      and writes:
        data/intel/met.json           every foreign pilot our ships met: faction
                                      tag, ship class, where, first and last
                                      time, how often, whether it was in a fight
        data/intel/sightings.jsonl    one line per look: time, place, pilots,
                                      pirates, creatures
        data/scouting/<system>.json   a first read of a system that has no
                                      scouting file (the format of
                                      fleet/census.py), so the hourly tracker
                                      files the system in planets/
      The hourly tracker (scripts/intel-track.py) turns these into the files
      and indexes of the repository; the command station reads those.
RULES:
  - It sends only calls that read (get_nearby, get_system, get_poi). It never
    moves a ship, never fights and never writes to a player.
  - One look per place per ten minutes, at most 12 looks a pass, never through
    a ship that is jumping, in transit or not connected.
  - Our own pilots (every name of fleet.json) are never recorded.
  - A system that has a scouting file is left to the census: this script never
    overwrites one.
  - The file data/fleet/STOP halts every look.
WHY:  a ship that enters a place is the fleet's eye there. What it sees is
      kept without anyone asking for it.

USAGE:
  sight.py              run forever (the service `sight`)
  sight.py --once       one pass
  --data <dir>          the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GATE = "http://172.30.0.32:7580"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
EVERY = 30                   # seconds between two passes
PLACE_REST = 600             # seconds before a place is looked at again
PER_PASS = 12                # looks in one pass at most
LOG_LIMIT = 5_000_000        # bytes of sightings.jsonl before it is moved aside


def stamp(now):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name("%s.%d.tmp" % (path.name, os.getpid()))
    tmp.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, path)


def ask_gate(pilot, action):
    """The structured answer of one reading call through the engine's gate, or {} when it gave none."""
    body = json.dumps({"toolGroup": "spacemolt", "action": action, "params": {}}).encode()
    request = urllib.request.Request("%s/accounts/%s/raw" % (GATE, urllib.parse.quote(pilot, safe="")), data=body, method="POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with OPENER.open(request, timeout=60) as response:
            answer = json.loads(response.read().decode("utf-8", "replace") or "{}")
    except (urllib.error.URLError, OSError, ValueError):
        return {}
    content = answer.get("structuredContent") if isinstance(answer, dict) else None
    return content if isinstance(content, dict) else {}


def looks(rows, seen, now):
    """[(system, poi, pilot)] to look at in this pass: one of our ships per place that rested long enough, the longest-rested first."""
    places = {}
    for row in rows:
        if not isinstance(row, dict) or row.get("status") != "connected" or row.get("jumping") or row.get("in_transit"):
            continue
        system, poi = row.get("system"), row.get("poi")
        if system and poi and (system, poi) not in places:
            places[(system, poi)] = row.get("name")
    due = [(seen.get("%s:%s" % place, 0), place, pilot) for place, pilot in places.items() if now - seen.get("%s:%s" % place, 0) >= PLACE_REST]
    return [(place[0], place[1], pilot) for _last, place, pilot in sorted(due)[:PER_PASS]]


def record(met, own, system, poi, near, now):
    """Fold one get_nearby answer into `met`; returns the line for sightings.jsonl."""
    pilots = []
    for row in near.get("nearby") or []:
        name = row.get("username") if isinstance(row, dict) else None
        if not name or name in own:
            continue
        pilots.append(name)
        entry = met.setdefault(name, {"first": stamp(now), "times": 0})
        entry.update({"faction_tag": row.get("faction_tag") or "", "ship_class": row.get("ship_class") or "", "system": system, "poi": poi,
                      "last": stamp(now), "times": entry.get("times", 0) + 1})
        if row.get("in_combat"):
            entry["in_combat_at"] = stamp(now)
    count = lambda key: len([x for x in near.get(key) or [] if isinstance(x, dict)])
    return {"at": stamp(now), "system": system, "poi": poi, "pilots": sorted(pilots), "pirates": count("pirates"), "creatures": count("creatures")}


def one_pass(data, ask, seen, now):
    """One pass over the fleet; returns the lines it would log. `seen` ({place: time of the last look}) is updated."""
    data = Path(data)
    if (data / "fleet" / "STOP").exists():
        return []
    rows = read_json(data / "fleet" / "fleet.json", {}).get("ships") or []
    own = {row.get("name") for row in rows if isinstance(row, dict)}
    todo = looks(rows, seen, now)
    if not todo:
        return []
    met = read_json(data / "intel" / "met.json", {})
    met = met if isinstance(met, dict) else {}
    lines, said = [], []
    for system, poi, pilot in todo:
        seen["%s:%s" % (system, poi)] = now
        near = ask(pilot, "get_nearby")
        if not near or near.get("poi_id") not in (None, poi):         # no answer, or the ship has moved on: no sighting
            continue
        line = record(met, own, system, poi, near, now)
        lines.append(line)
        if line["pilots"] or line["pirates"]:
            said.append("%s:%s %d pilot(s), %d pirate(s)" % (system, poi, len(line["pilots"]), line["pirates"]))
        scouting = data / "scouting" / (system + ".json")
        if not scouting.exists():
            read = ask(pilot, "get_system").get("system")
            if isinstance(read, dict) and read.get("id") == system:
                write_json(scouting, {"system": read, "read_at": stamp(now), "source": "fleet/sight.py, an own ship passing", "pois": {poi: ask(pilot, "get_poi")}})
                said.append("%s: first read of the system saved" % system)
    if lines:
        write_json(data / "intel" / "met.json", met)
        log = data / "intel" / "sightings.jsonl"
        if log.exists() and log.stat().st_size > LOG_LIMIT:
            os.replace(log, log.with_name("sightings.1.jsonl"))
        with open(log, "a", encoding="utf-8") as handle:
            handle.write("".join(json.dumps(line, separators=(",", ":")) + "\n" for line in lines))
    return said


def main():
    parser = argparse.ArgumentParser(description="What our ships see where they are.")
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    seen = {}
    while True:
        try:
            for text in one_pass(args.data, ask_gate, seen, time.time()):
                print(stamp(time.time()), text, flush=True)
        except Exception as error:                      # a bad file or answer never ends the service
            print(stamp(time.time()), "pass failed: %s: %s" % (type(error).__name__, error), flush=True)
        if args.once:
            return 0
        time.sleep(EVERY)


if __name__ == "__main__":
    sys.exit(main())
