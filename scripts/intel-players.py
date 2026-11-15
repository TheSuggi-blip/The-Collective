#!/usr/bin/env python3
"""intel-players.py -- file the armed pilots seen in our space.

WHAT: reads what the command station collects from the game's public
      data (the live event stream and the daily feed) and writes a pilot
      file players/n-<key>.md, in the form of players/BLUEPRINT.md, for
      every pilot that
        1. made its last jump of the past 24 hours into a system of our
           home empire, and
        2. has destroyed at least --kills player ships (default 1).
      Such a pilot is filed neutral with threat medium: the blueprint's
      "armed; has destroyed player ships".
RULES:
  - A standing other than neutral is never set here: hostile and ally are
    set by an agent or by Suggi (players/BLUEPRINT.md s.3).
  - A pilot of ours is never filed. A pilot that has a file is never
    touched: its history is append-only and written by hand.
  - At most --max new files per run (default 10), highest kill count first.
WHY:  an Admiral sees who in our space can kill before a ship meets them.

USAGE:
  intel-players.py                   file what is new; print what was written
  intel-players.py --station <dir>   the station's data (default: the unit's data folder)
  intel-players.py --fleet <file>    our own pilots (default: the unit's fleet.json)
  intel-players.py --root <dir>      another repository tree (used by tests)
Afterwards: python3 scripts/intel-index.py && python3 scripts/validate-intel.py

Stdlib only. ASCII only.
"""

import argparse
import importlib.util
import json
import os
import sys
import time

HOME_EMPIRE = "voidborn"
STATION = "/srv/collective/data/station"
FLEET = "/srv/collective/data/fleet/fleet.json"
WINDOW = 24 * 3600


def sibling(name):
    """Another script of this folder, loaded by path (a hyphenated name cannot be imported)."""
    sys.dont_write_bytecode = True                    # no __pycache__ in the shared clone
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    spec = importlib.util.spec_from_file_location(name[:-3].replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return default


def escaped(text):
    """ASCII text; a character outside ASCII becomes \\u{hex} (BLUEPRINT s.4)."""
    out = []
    for ch in str(text):
        if ch in "|\r\n":
            out.append(" ")
        elif 32 <= ord(ch) < 127:
            out.append(ch)
        else:
            out.append("\\u{%x}" % ord(ch))
    return "".join(out)


def home_systems(root):
    out = set()
    path = os.path.join(root, "map", "galaxy.tsv")
    if os.path.isfile(path):
        with open(path, encoding="ascii", errors="replace") as handle:
            for line in handle:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 5 and not line.startswith("#") and parts[4] == HOME_EMPIRE:
                    out.add(parts[0])
    return out


def candidates(root, station, fleet_file, min_kills, now):
    """[(kills, username, system, seen_at, record)] for pilots the rule selects."""
    home = home_systems(root)
    pilots = read_json(os.path.join(station, "pilots.json"), {})
    feed = read_json(os.path.join(station, "feed.json"), {})
    players = feed.get("players") if isinstance(feed, dict) else {}
    ours = {str(s.get("name")).lower() for s in (read_json(fleet_file, {}).get("ships") or []) if isinstance(s, dict)}
    out = []
    for name, seen in (pilots.items() if isinstance(pilots, dict) else []):
        if not isinstance(seen, list) or len(seen) < 2 or seen[0] not in home or name.lower() in ours:
            continue
        if not isinstance(seen[1], (int, float)) or now - seen[1] > WINDOW:
            continue
        record = (players or {}).get(name.lower())
        stats = (record or {}).get("stats") or {}
        kills = stats.get("ships_destroyed") or 0
        if isinstance(kills, int) and kills >= min_kills:
            out.append((kills, name, seen[0], seen[1], record))
    return sorted(out, key=lambda r: (-r[0], r[1])), str((feed or {}).get("built_at") or "unknown")


def pilot_file(key, name, system, seen_at, record, built, stamp):
    stats = record.get("stats") or {}
    day = time.strftime("%Y-%m-%d", time.gmtime(seen_at))
    when = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(seen_at))
    empire = escaped(record.get("empire") or "unknown")
    faction = escaped(record.get("faction") or "none")
    shown = escaped(name)
    source = "Daily feed, players, built %s" % escaped(built)
    kills, lost, pirates = stats.get("ships_destroyed", 0), stats.get("ships_lost", 0), stats.get("pirates_destroyed", 0)
    lines = ["---", "name: " + key, "id: " + stamp, "tier: intel", "author: Unity", "kind: player", "username: " + shown,
             "standing: neutral", "standing_since: " + day, "threat: medium", "empire: " + empire, "faction: " + faction,
             "updated: " + day, "---", "", "# " + shown, "",
             "A pilot with %s player ship%s destroyed on its record, seen in our space." % (format(kills, ","), "" if kills == 1 else "s"),
             "Neutral: it has not met us. On contact a Collective pilot docks or", "leaves, and reports the sighting.", "",
             "## Identity", "", "| Field | Value | When | Source |", "|---|---|---|---|",
             "| Empire | %s | %s | %s |" % (empire, day, source),
             "| Faction, role | %s | %s | %s |" % (faction, day, source),
             "| Usual area | Last jump into %s | %s | Public event stream |" % (escaped(system), when),
             "", "## Strength", "", "| Field | Value | When | Source |", "|---|---|---|---|",
             "| Player ships destroyed | %s | %s | %s |" % (format(kills, ","), day, source),
             "| Pirates destroyed | %s | %s | %s |" % (format(pirates, ","), day, source),
             "| Ships lost | %s | %s | %s |" % (format(lost, ","), day, source),
             "", "## Standing History", "", "Append-only, newest last.", "", "| Date | Standing | By | Reason |", "|---|---|---|---|",
             "| %s | neutral | Unity | No contact with The Collective; filed by `scripts/intel-players.py` for its kill record |" % day,
             "", "## Encounters", "", "Append-only, newest last. None with The Collective yet.", "",
             "| When | Where | What happened | Our pilot | Source |", "|---|---|---|---|---|",
             "| %s | %s | Jumped into the system | none | Public event stream |" % (when, escaped(system)),
             "", "## Notes", "",
             "- Filed by a script from public data: its ship, its fit and what it does here are not known.",
             "- The kill count is a lifetime number; it does not say whom it attacks."]
    return "\n".join(lines) + "\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="File the armed pilots seen in our space.")
    parser.add_argument("--root", default=os.path.join(here, ".."))
    parser.add_argument("--station", default=STATION)
    parser.add_argument("--fleet", default=FLEET)
    parser.add_argument("--kills", type=int, default=1)
    parser.add_argument("--max", type=int, default=10)
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    intel, index = sibling("validate-intel.py"), sibling("intel-index.py")   # the naming rule; the id allocator
    rows, built = candidates(root, args.station, args.fleet, max(1, args.kills), time.time())
    written = 0
    for kills, name, system, seen_at, record in rows:
        if written >= args.max:
            print("more pilots match than --max allows; the rest is left for the next run")
            break
        path, note = intel.suggest_name(root, "player", escaped(name), "neutral")
        if note.startswith("exists already"):
            continue
        key = os.path.basename(path)[2:-3]
        text = pilot_file(key, name, system, seen_at, record, built, index.new_id(root))             # an id no intel file carries
        with open(os.path.join(root, path), "w", encoding="ascii") as handle:
            handle.write(text)
        print("written " + path)
        written += 1
    print("%d new pilot file(s); %d pilot(s) match the rule" % (written, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
