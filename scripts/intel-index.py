#!/usr/bin/env python3
"""intel-index.py -- build planets/index.md and players/index.md.

WHAT: one table of contents per folder, built from the frontmatter of
      its data files (<a|n|h>-<key>.md). Systems are grouped by zone:
      the empire whose space they lie in, home space first, lawless
      space last, sorted by jumps from home. Pilots are grouped by
      standing: hostile, neutral, ally.
WHY:  a reader finds a system or a pilot without opening every file.
      The index holds nothing that is not in the files.

USAGE:
  intel-index.py                 write both index files (when they changed)
  intel-index.py --check         write nothing; exit 1 when one is stale
  intel-index.py --root <dir>    another tree (used by tests)

Run it in the commit that adds or changes a data file;
scripts/validate-intel.py fails on a stale or missing index.

Stdlib only. ASCII only.
"""

import argparse
import os
import re
import sys
import time

FILE_RE = re.compile(r"^([anh])-([a-z0-9_.\-]+)\.md$")
HOME_EMPIRE = "voidborn"
STANDING_ORDER = ("hostile", "neutral", "ally")
TITLES = {"planets": "Systems We Know", "players": "Pilots We Know"}
WHAT = {"planets": "system", "players": "pilot"}


def read_file(path):
    """Return (frontmatter fields, first heading) of a data file."""
    fields, title, inside = {}, "", False
    with open(path, encoding="ascii", errors="replace") as handle:
        lines = handle.read().split("\n")
    for number, line in enumerate(lines):
        if number == 0 and line.strip() == "---":
            inside = True
            continue
        if inside:
            if line.strip() == "---":
                inside = False
            elif ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            break
    return fields, title


def chart_jumps(root):
    """System id -> jumps from home, from map/galaxy.tsv (column 7)."""
    jumps = {}
    path = os.path.join(root, "map", "galaxy.tsv")
    if not os.path.isfile(path):
        return jumps
    with open(path, encoding="ascii", errors="replace") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 7 and parts[0] and parts[0] != "id" and not line.startswith("#"):
                jumps[parts[0]] = parts[6]
    return jumps


def cell(value):
    return str(value if value not in (None, "") else "--").replace("|", "/")


def rows_of(root, folder):
    directory = os.path.join(root, folder)
    out = []
    for name in sorted(os.listdir(directory)) if os.path.isdir(directory) else []:
        if not FILE_RE.match(name):
            continue
        fields, title = read_file(os.path.join(directory, name))
        out.append((name, fields, title))
    return out


def number(text):
    return int(text) if str(text).isdigit() else 10 ** 6


def body(root, folder):
    """The index text below its frontmatter."""
    rows = rows_of(root, folder)
    what = WHAT[folder]
    lines = ["# index.md -- %s" % TITLES[folder], "",
             "Built by `scripts/intel-index.py` from the %s files of this folder;" % what,
             "never edited by hand. Files listed: %d. The format of a %s file:" % (len(rows), what),
             "`BLUEPRINT.md`."]
    if folder == "planets":
        jumps = chart_jumps(root)
        zones = {}
        for name, fields, title in rows:
            empire = (fields.get("empire") or "none").lower()
            zones.setdefault("lawless" if empire in ("none", "lawless", "-", "") else empire, []).append((name, fields, title))
        order = sorted(zones, key=lambda z: (z != HOME_EMPIRE, z == "lawless", z))
        for zone in order:
            lines += ["", "## %s space" % zone.capitalize(), "",
                      "| System | Standing | Threat | Police level | Jumps from home | Updated | File |",
                      "|---|---|---|---|---|---|---|"]
            for name, fields, title in sorted(zones[zone], key=lambda r: (number(jumps.get(r[1].get("system_id"), "")), r[0])):
                lines.append("| %s | %s | %s | %s | %s | %s | [%s](%s) |" % (
                    cell(title or fields.get("system_id")), cell(fields.get("standing")), cell(fields.get("threat")),
                    cell(fields.get("police_level")), cell(jumps.get(fields.get("system_id"))), cell(fields.get("updated")),
                    name, name))
    else:
        by = {}
        for name, fields, title in rows:
            by.setdefault(fields.get("standing"), []).append((name, fields, title))
        for standing in STANDING_ORDER:
            lines += ["", "## %s" % standing.capitalize(), ""]
            group = by.get(standing) or []
            if not group:
                lines.append("None filed.")
                continue
            lines += ["| Pilot | Threat | Empire | Faction | Standing since | Updated | File |", "|---|---|---|---|---|---|---|"]
            for name, fields, title in sorted(group, key=lambda r: r[0]):
                lines.append("| %s | %s | %s | %s | %s | %s | [%s](%s) |" % (
                    cell(fields.get("username") or title), cell(fields.get("threat")), cell(fields.get("empire")),
                    cell(fields.get("faction")), cell(fields.get("standing_since")), cell(fields.get("updated")), name, name))
    return "\n".join(lines) + "\n"


def split(text):
    """(frontmatter block with its --- lines, body) of an existing index."""
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        end = text.index("\n---\n", 4) + 5
        return text[:end], text[end:].lstrip("\n")
    return "", text


def state(root, folder):
    """current, stale, missing, or empty (no data files and no index)."""
    path = os.path.join(root, folder, "index.md")
    if not os.path.isfile(path):
        return "missing" if rows_of(root, folder) else "empty"
    with open(path, encoding="ascii", errors="replace") as handle:
        _front, old = split(handle.read())
    return "current" if old == body(root, folder) else "stale"


def new_id(root):
    """A timestamp id no file of the two folders carries yet, and never one ending on :00."""
    used = set()
    for folder in TITLES:
        directory = os.path.join(root, folder)
        for name in os.listdir(directory) if os.path.isdir(directory) else []:
            if name.endswith(".md"):
                used.add(read_file(os.path.join(directory, name))[0].get("id"))
    stamp = time.time()
    while True:
        text = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(stamp))
        if text not in used and time.gmtime(stamp).tm_sec != 0:
            return text
        stamp += 1


def write(root, folder):
    """Write the index when it is missing or stale. Returns True when written."""
    path = os.path.join(root, folder, "index.md")
    front = ""
    if not os.path.isfile(path) and not rows_of(root, folder):
        return False                                   # nothing to list and nothing to correct
    if os.path.isfile(path):
        with open(path, encoding="ascii", errors="replace") as handle:
            front, old = split(handle.read())
        if old == body(root, folder):
            return False
    if not front:
        front = "---\nname: %s-index\nid: %s\ntier: intel\nauthor: Unity\n---\n" % (folder, new_id(root))
    with open(path + ".tmp", "w", encoding="ascii") as handle:
        handle.write(front + "\n" + body(root, folder))
    os.replace(path + ".tmp", path)
    return True


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Build planets/index.md and players/index.md.")
    parser.add_argument("--root", default=os.path.join(here, ".."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    bad = 0
    for folder in ("planets", "players"):
        if not os.path.isdir(os.path.join(root, folder)):
            continue
        if args.check:
            result = state(root, folder)
            print("%s/index.md: %s" % (folder, result))
            bad += result in ("stale", "missing")
        else:
            print("%s/index.md: %s" % (folder, "written" if write(root, folder) else "current"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
