#!/usr/bin/env python3
"""intel-planets.py -- file the systems our ships have read.

WHAT: for every system a scout of ours read (one JSON file per system in
      the unit's data folder, written by the fleet's scripts), writes the
      system file game/planets/<a|n>-<system_id>.md in the form of
      game/planets/BLUEPRINT.md, when no file for that system exists yet.
      A system in our home empire is filed as ally, any other as neutral.
      An existing file is never touched: its history is append-only and
      its notes are written by hand.
WHY:  what a ship saw reaches the repository without an agent retyping it.
      A ship of ours is written `own ship`, never by name.

USAGE:
  intel-planets.py                      file what is new; print what was written
  intel-planets.py --data <dir>         the scouting reads (default: the unit's data folder)
  intel-planets.py --root <dir>         another repository tree (used by tests)
Afterwards: python3 scripts/intel-index.py && python3 scripts/validate-intel.py

Stdlib only. ASCII only.
"""

import argparse
import importlib.util
import json
import os
import re
import sys
import time

HOME_EMPIRE = "voidborn"
DATA = "/srv/collective/data/scouting"
RESOURCE_TYPES = ("asteroid_belt", "ice_field", "gas_cloud")
SYSTEM_ID_RE = re.compile(r"^[a-z0-9_]+$")


def sibling(name):
    """Another script of this folder, loaded by path (a hyphenated name cannot be imported)."""
    sys.dont_write_bytecode = True                    # no __pycache__ in the shared clone
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    spec = importlib.util.spec_from_file_location(name[:-3].replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ascii_cell(value):
    text = str(value if value is not None else "").replace("|", "/").replace("\n", " ")
    return text.encode("ascii", "replace").decode("ascii")


def chart(root):
    out = {}
    path = os.path.join(root, "game", "map", "galaxy.tsv")
    if not os.path.isfile(path):
        return out
    with open(path, encoding="ascii", errors="replace") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 8 and parts[0] and parts[0] != "id" and not line.startswith("#"):
                out[parts[0]] = {"x": parts[2], "y": parts[3], "empire": parts[4], "jumps": parts[6], "lanes": parts[7].split(",")}
    return out


def filed(root):
    """System ids that already have a file, under any letter."""
    out = set()
    directory = os.path.join(root, "game", "planets")
    for name in os.listdir(directory) if os.path.isdir(directory) else []:
        match = re.match(r"^[anh]-([a-z0-9_]+)\.md$", name)
        if match:
            out.add(match.group(1))
    return out


def resources_of(read):
    poi = read.get("poi") if isinstance(read.get("poi"), dict) else {}
    rows = poi.get("resources") or read.get("resources") or []
    return [r for r in rows if isinstance(r, dict)]


def system_file(system_id, read, spot, stamp):
    system = read.get("system") or {}
    pois = [p for p in system.get("pois") or [] if isinstance(p, dict)]
    reads = read.get("pois") or {}
    when = (read.get("read_at") or "")[:16].replace("T", " ") + " UTC"
    day = (read.get("read_at") or "")[:10]
    empire = (system.get("empire") or spot.get("empire") or "none").lower()
    ours = empire == HOME_EMPIRE
    standing = "ally" if ours else "neutral"
    reason = "Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)"
    name = ascii_cell(system.get("name") or system_id)
    police = system.get("police_level")
    stations = [p for p in pois if p.get("type") == "station"]
    deposits = [p for p in pois if p.get("type") in RESOURCE_TYPES]
    lines = ["---", "name: " + system_id, "id: " + stamp, "tier: intel", "author: Unity", "kind: system", "system_id: " + system_id,
             "standing: " + standing, "standing_since: " + day]
    if ours:
        lines += ["standing_by: Unity", "standing_reason: " + reason]
    lines += ["threat: " + ("low" if ours else "unknown"), "empire: " + empire, "police_level: %s" % police, "updated: " + day, "---", "",
              "# " + name, "",
              "%s system %s jumps from home, police level %s. %s." % (
                  empire.capitalize() if empire != "none" else "Lawless", spot.get("jumps", "an unknown number of"), police,
                  ("Station: " + ", ".join(ascii_cell(p.get("name")) for p in stations)) if stations else "No station on the chart"),
              "", "## Chart", "", "From `game/map/galaxy.tsv` (`python3 scripts/map.py where %s`)." % system_id, "",
              "| Field | Value |", "|---|---|",
              "| Position | x %s, y %s (Galactic Units) |" % (spot.get("x", "?"), spot.get("y", "?")),
              "| Empire | %s |" % (spot.get("empire") if spot.get("empire") not in (None, "-") else "lawless"),
              "| Jumps from home | %s |" % spot.get("jumps", "?"), "| Lanes | %s |" % ", ".join(spot.get("lanes") or []), "",
              "## Points of Interest", "",
              "| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |", "|---|---|---|---|---|---|---|---|"]
    visits = []
    for p in pois:
        kind = ascii_cell(p.get("type")) + (" (%s)" % ascii_cell(p.get("class")) if p.get("class") else "")
        base, res, source = "--", "--", "`get_system`, own ship"
        if p.get("type") in RESOURCE_TYPES:
            res = "not read"
            if p.get("id") in reads:
                rows = resources_of(reads[p["id"]])
                res = "; ".join("%s: richness %s, %s of %s left" % (
                    ascii_cell(r.get("resource_id")), r.get("richness"), r.get("remaining"),
                    r.get("max_remaining") if r.get("max_remaining") is not None else "unknown") for r in rows) or "nothing listed"
                source = "`get_poi`, own ship"
                left = sum(r.get("remaining") or 0 for r in rows)
                visits.append("Read %s: %s" % (ascii_cell(p.get("name")), "nothing left" if left == 0 else "%s units left in all" % format(left, ",")))
        if p.get("type") == "station" and p.get("base_id"):
            base = "`%s`" % ascii_cell(p.get("base_id"))
        hazard = p.get("hazard")
        hazard = "%s, severity %s" % (ascii_cell(hazard.get("type")), hazard.get("severity")) if isinstance(hazard, dict) else "none"
        lines.append("| `%s` | %s | %s | %s | %s | %s | %s | %s |" % (
            ascii_cell(p.get("id")), ascii_cell(p.get("name")), kind, base, res, hazard, when, source))
    lines += ["", "## Stations", "", "| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |", "|---|---|---|---|---|---|---|---|"]
    for p in stations:
        lines.append("| %s (`%s`) | unknown | not tried | not read | unknown | unknown | %s | `get_system`, own ship |" % (
            ascii_cell(p.get("name")), ascii_cell(p.get("base_id") or p.get("id")), when))
    if not stations:
        lines[-2:] = ["None on the chart."]
    lines += ["", "## Threats", "", "| When | What | Source |", "|---|---|---|",
              "| %s | None seen on one pass. Police level %s%s | `get_system`, own ship |" % (
                  day, police, (": " + ascii_cell(system.get("security_status"))) if system.get("security_status") else ""),
              "", "## Standing History", "", "Append-only, newest last.", "", "| Date | Standing | By | Reason |", "|---|---|---|---|",
              "| %s | %s | %s | %s |" % (day, standing, "Unity", reason if ours else "Not judged; filed from a scouting read"),
              "", "## Visits", "", "Append-only, newest last.", "", "| When | By | What was done or seen | Source |", "|---|---|---|---|"]
    for what in visits or ["Passed through and listed the points of interest"]:
        lines.append("| %s | own ship | %s | `get_poi`, own ship |" % (when, what))
    notes = ["- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships."]
    unread = [p.get("id") for p in deposits if p.get("id") not in reads]
    if unread:
        notes.append("- Not read yet: " + ", ".join("`%s`" % ascii_cell(u) for u in unread) + ".")
    if not deposits:
        notes.append("- No belt, ice field or gas cloud on the chart.")
    lines += ["", "## Notes", ""] + notes
    return "\n".join(lines) + "\n", ("a" if ours else "n")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="File the systems our ships have read.")
    parser.add_argument("--root", default=os.path.join(here, ".."))
    parser.add_argument("--data", default=DATA)
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    spots, have, index = chart(root), filed(root), sibling("intel-index.py")
    written = 0
    for name in sorted(os.listdir(args.data)) if os.path.isdir(args.data) else []:
        system_id = name[:-5]
        if not name.endswith(".json") or not SYSTEM_ID_RE.match(system_id) or system_id in have:
            continue
        try:
            with open(os.path.join(args.data, name), encoding="utf-8") as handle:
                read = json.load(handle)
        except (OSError, ValueError):
            print("skipped %s: not readable JSON" % name)
            continue
        if not isinstance(read, dict) or not isinstance(read.get("system"), dict) or not read.get("read_at"):
            print("skipped %s: no system read in it" % name)
            continue
        text, letter = system_file(system_id, read, spots.get(system_id, {}), index.new_id(root))   # an id no intel file carries
        path = os.path.join(root, "game", "planets", "%s-%s.md" % (letter, system_id))
        with open(path, "w", encoding="ascii") as handle:
            handle.write(text)
        print("written game/planets/%s-%s.md" % (letter, system_id))
        written += 1
    print("%d new system file(s)" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
