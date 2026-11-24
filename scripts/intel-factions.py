#!/usr/bin/env python3
"""intel-factions.py -- file the player factions that matter to us, and the zones they hold.

WHAT: from the command station's copy of the game's public data it writes
        game/factions/<letter>-<tag>.md   one file per player faction that holds a
                                     base (station or outpost) anywhere, or
                                     had two or more pilots in our space in
                                     the last 24 hours;
        game/factions/index.md            the zones held by other players (every
                                     system with a player base, nearest
                                     first), the factions by standing, every
                                     tag seen in our space, and the pirate
                                     strongholds.
      The data: stations.json (every base and its owner), pilots.json (each
      pilot's last system on the public event stream, with empire and tag),
      map.json (empire and lanes of every system), feed.json (the daily
      feed: a faction's name, leader, member count, allies, enemies, wars;
      a pilot's kill count), and the pilots our own ships met (met.json,
      written by game/fleet/sight.py: the ship a pilot flew).
RULES:
  - A faction file has a written part and a kept part. From the title to
    `## Standing History` it is written anew at every run. The frontmatter
    fields id, standing, standing_since and threat, and everything from
    `## Standing History` on, are kept as they are: they are set by hand
    (who may set a standing: game/players/BLUEPRINT.md s.3).
  - A file is rewritten only when its written part changed, so a faction
    that did not move makes no commit; `updated` changes with it.
  - The letter of an existing file is kept: a change of standing is a
    rename by hand (git mv), never a second file.
  - Our own faction and our own pilots are never filed.
  - A new file is filed neutral with threat unknown. At most --max new
    files per run (default 40), factions with a base first.
  - ASCII only: a character outside ASCII is written \\u{hex}.
WHY:  an Admiral sees whose space a system is and whose ships are in ours
      before a ship of ours meets them.

USAGE:
  intel-factions.py                    write what changed; print what was written
  intel-factions.py --station <dir>    the station's data (default: the unit's data folder)
  intel-factions.py --met <file>       pilots our ships met (default: the unit's data folder)
  intel-factions.py --fleet <file>     our own pilots (default: the unit's fleet.json)
  intel-factions.py --root <dir>       another repository tree (used by tests)

Stdlib only. ASCII only.
"""

import argparse
import json
import os
import re
import sys
import time

HOME_EMPIRE = "voidborn"
HOME_SYSTEM = "nexus_prime"
OWN_TAG = "CLTV"
STATION = "/srv/collective/data/station"
MET = "/srv/collective/data/intel/met.json"
FLEET = "/srv/collective/data/fleet/fleet.json"
WINDOW = 24 * 3600
FILE_RE = re.compile(r"^([anh])-([a-z0-9_]+)\.md$")
STANDINGS = {"a": "ally", "n": "neutral", "h": "hostile"}
KEPT_FROM = "## Standing History"
LISTED = 30                                  # pilots named per faction file; the rest is a count


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return default


def ascii_text(value):
    """One line of ASCII: a character outside ASCII becomes \\u{hex}, a pipe a slash."""
    text = " ".join(str(value if value is not None else "").split()).replace("|", "/")
    return "".join(c if 31 < ord(c) < 127 else "\\u{%x}" % ord(c) for c in text)


def key_of(tag):
    """The file key of a tag: lower case; a character outside a-z and 0-9 is written x plus its hex code."""
    return "".join(c if c in "abcdefghijklmnopqrstuvwxyz0123456789" else "x%x" % ord(c) for c in str(tag).lower())


def jumps_from(systems, start):
    """{system id: jumps from start} over the lanes of the chart."""
    lanes = {s.get("id"): [x for x in s.get("lanes") or [] if isinstance(x, str)] for s in systems if isinstance(s, dict)}
    out, edge = {start: 0}, [start]
    while edge:
        nxt = []
        for here in edge:
            for there in lanes.get(here, []):
                if there not in out:
                    out[there] = out[here] + 1
                    nxt.append(there)
        edge = nxt
    return out


def gather(station, met_path, fleet_path, now):
    """Everything the folder is written from, as plain dicts."""
    chart = [s for s in (read_json(os.path.join(station, "map.json"), {}).get("systems") or []) if isinstance(s, dict) and s.get("id")]
    space = {s["id"]: (s.get("empire") or "lawless") for s in chart}
    names = {s["id"]: s.get("name") or s["id"] for s in chart}
    jumps = jumps_from(chart, HOME_SYSTEM)
    own = {s.get("name") for s in read_json(fleet_path, {}).get("ships") or [] if isinstance(s, dict)}
    feed = read_json(os.path.join(station, "feed.json"), {})
    known = feed.get("factions") if isinstance(feed.get("factions"), dict) else {}
    kills = {p.get("name"): (p.get("stats") or {}).get("ships_destroyed") or 0
             for p in (feed.get("players") or {}).values() if isinstance(p, dict)} if isinstance(feed.get("players"), dict) else {}
    met = read_json(met_path, {})
    met = met if isinstance(met, dict) else {}
    bases, pirates = {}, []
    for row in read_json(os.path.join(station, "stations.json"), []):
        if not isinstance(row, dict) or not row.get("system"):
            continue
        entry = {"name": row.get("name") or "", "kind": row.get("type") or "", "system": row["system"], "condition": row.get("condition") or "",
                 "wrecked": bool(row.get("wrecked")), "mobile": bool(row.get("mobile")), "faction": row.get("faction") or ""}
        if row.get("tag"):
            bases.setdefault(row["tag"], []).append(entry)
        elif row.get("empire") == "pirates":
            pirates.append(entry)
    seen, carried = {}, {}
    for pilot, row in (read_json(os.path.join(station, "pilots.json"), {}) or {}).items():
        if not (isinstance(row, list) and len(row) >= 4 and row[3]) or pilot in own:
            continue
        carried[row[3]] = carried.get(row[3], 0) + 1
        if space.get(row[0]) == HOME_EMPIRE and isinstance(row[1], (int, float)) and now - row[1] <= WINDOW:
            seen.setdefault(row[3], []).append((pilot, row[0]))
    return {"space": space, "names": names, "jumps": jumps, "known": known, "kills": kills, "met": met, "bases": bases,
            "pirates": pirates, "seen": seen, "carried": carried}


def system_cell(data, system):
    return "%s (`%s`)" % (ascii_text(data["names"].get(system, system)), system)


def jumps_cell(data, system):
    return str(data["jumps"][system]) if system in data["jumps"] else "no lane found"


def written_part(tag, data):
    """The part of a faction file that is written anew at every run."""
    info = data["known"].get(tag) if isinstance(data["known"].get(tag), dict) else {}
    bases = sorted(data["bases"].get(tag, []), key=lambda b: (data["jumps"].get(b["system"], 10 ** 6), b["system"], b["name"]))
    name = info.get("name") or (bases[0]["faction"] if bases else "") or tag
    seen = sorted(data["seen"].get(tag, []), key=lambda p: p[0].lower())
    systems = sorted({b["system"] for b in bases})
    lines = ["# %s [%s]" % (ascii_text(name), ascii_text(tag)), ""]
    if bases:
        nearest = bases[0]
        lines.append("A player faction with %d base(s) in %d system(s); the nearest to Nexus Prime is %s jump(s) away, in %s."
                     % (len(bases), len(systems), jumps_cell(data, nearest["system"]), system_cell(data, nearest["system"])))
    else:
        lines.append("A player faction without a base on the public record.")
    lines.append("Pilots of it in our space in the last 24 hours: %d." % len(seen))
    lines += ["", "## Identity", "", "| Field | Value | Source |", "|---|---|---|"]
    for label, value in (("Leader", info.get("leader")), ("Members", info.get("members")),
                         ("Allies", ", ".join(sorted(info.get("allies") or []))), ("Enemies", ", ".join(sorted(info.get("enemies") or []))),
                         ("At war with", ", ".join(sorted(info.get("wars") or [])))):
        lines.append("| %s | %s | Daily feed, factions |" % (label, ascii_text(value) if value not in (None, "", 0) else ("none" if label != "Leader" and info else "not on record")))
    lines.append("| Pilots carrying the tag on the public event stream | %d | Public event stream |" % data["carried"].get(tag, 0))
    lines += ["", "## Bases", ""]
    if bases:
        lines += ["| Base | Kind | System | Space | Jumps from Nexus Prime | Condition |", "|---|---|---|---|---|---|"]
        for b in bases:
            state = ", ".join(x for x in (b["condition"], "wrecked" if b["wrecked"] else "", "mobile" if b["mobile"] else "") if x) or "--"
            lines.append("| %s | %s | %s | %s | %s | %s |" % (ascii_text(b["name"]) or "--", ascii_text(b["kind"]) or "--", system_cell(data, b["system"]),
                                                             ascii_text(data["space"].get(b["system"], "not on the chart")), jumps_cell(data, b["system"]), ascii_text(state)))
    else:
        lines.append("None on the public record.")
    lines += ["", "## Pilots in Our Space", "",
              "Pilots carrying this tag whose last known system is one of ours (public event stream, last 24 hours).", ""]
    if seen:
        lines += ["| Pilot | System | Player ships destroyed | Ship when one of ours met it |", "|---|---|---|---|"]
        for pilot, system in seen[:LISTED]:
            ship = (data["met"].get(pilot) or {}).get("ship_class") if isinstance(data["met"].get(pilot), dict) else None
            lines.append("| %s | %s | %s | %s |" % (ascii_text(pilot), system_cell(data, system), data["kills"].get(pilot, "not on record"), ascii_text(ship) if ship else "not met"))
        if len(seen) > LISTED:
            lines.append("")
            lines.append("And %d more." % (len(seen) - LISTED))
    else:
        lines.append("None in the last 24 hours.")
    return "\n".join(lines) + "\n", name


def split_file(text):
    """(frontmatter fields, written part, kept part) of an existing faction file."""
    fields, body = {}, text
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        end = text.index("\n---\n", 4)
        for line in text[4:end].splitlines():
            key, sep, value = line.partition(":")
            if sep:
                fields[key.strip()] = value.strip()
        body = text[end + 5:].lstrip("\n")
    cut = body.find("\n" + KEPT_FROM)
    if cut < 0:
        return fields, body.rstrip("\n") + "\n", ""
    return fields, body[:cut].rstrip("\n") + "\n", body[cut + 1:]


def existing(root):
    """{key: file name} of the faction files in the folder."""
    folder = os.path.join(root, "game", "factions")
    return {FILE_RE.match(n).group(2): n for n in sorted(os.listdir(folder)) if FILE_RE.match(n)} if os.path.isdir(folder) else {}


def used_ids(root):
    out = set()
    for folder in ("factions", "planets", "players"):
        directory = os.path.join(root, "game", folder)
        for name in os.listdir(directory) if os.path.isdir(directory) else []:
            if name.endswith(".md"):
                try:
                    with open(os.path.join(directory, name), encoding="ascii", errors="replace") as handle:
                        out.add(split_file(handle.read())[0].get("id"))
                except OSError:
                    pass
    return out


def next_id(used, stamp):
    """A timestamp id nobody carries yet, never one ending on :00; the id is added to `used`."""
    while True:
        text = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(stamp))
        if text not in used and time.gmtime(stamp).tm_sec != 0:
            used.add(text)
            return text
        stamp -= 1                                   # backwards: an id is never in the future


def front(fields):
    order = ("name", "id", "tier", "author", "kind", "tag", "faction", "standing", "standing_since", "threat", "updated")
    return "---\n" + "".join("%s: %s\n" % (k, fields[k]) for k in order) + "---\n"


def seen_count(part):
    """Extract the 24h in-our-space pilot count from a faction written part."""
    m = re.search(r"Pilots of it in our space in the last 24 hours: (\d+)\.", part or "")
    return int(m.group(1)) if m else 0


def structural_part(part):
    """Strategic core of a faction dossier (title, bases summary, Identity minus public-stream count, and Bases table).
    Excludes only volatile rolling-24h sighting counts and per-pilot sighting rows."""
    text = str(part or "")
    cut = text.find("\n## Pilots in Our Space")
    core = text[:cut] if cut >= 0 else text
    kept = []
    for line in core.splitlines():
        if line.startswith("Pilots of it in our space in the last 24 hours:"):
            continue
        if line.startswith("| Pilots carrying the tag on the public event stream |"):
            continue
        kept.append(line)
    return "\n".join(kept)


def structural_index(body):
    """Strategic core of game/factions/index.md (Zones Held, Hostile/Allied/Watchlist, Pirate Strongholds,
    and faction list/bases/standing, ignoring only volatile 24h sighting counts and Updated dates)."""
    out = []
    in_tags = False
    for line in str(body or "").splitlines():
        if line.startswith("## Tags Seen in Our Space"):
            in_tags = True
            continue
        if in_tags and line.startswith("## "):
            in_tags = False
        if in_tags:
            continue
        if line.startswith("| ") and line.endswith(" |") and line.count("|") >= 9:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) == 8 and cells[0] != "Faction" and cells[0] != "---":
                # Keep Faction, Tag, Threat, Bases, Nearest base, File; mask volatile 24h pilots & Updated date
                cells[5] = "*"
                cells[6] = "*"
                line = "| " + " | ".join(cells) + " |"
        out.append(line)
    return "\n".join(out)


def write_files(root, data, now, limit, min_interval=0):
    """Write the faction files that are new or changed; returns the paths written."""
    day = time.strftime("%Y-%m-%d", time.gmtime(now))
    folder = os.path.join(root, "game", "factions")
    have, used, written, created = existing(root), None, [], 0
    wanted = [t for t in data["bases"] if t != OWN_TAG] + sorted(t for t, pilots in data["seen"].items() if len(pilots) >= 2 and t not in data["bases"] and t != OWN_TAG)
    wanted += [t for t in sorted(set(data["known"]) | set(data["carried"])) if key_of(t) in have and t not in wanted and t != OWN_TAG]
    for tag in wanted:
        key = key_of(tag)
        part, name = written_part(tag, data)
        if key in have:
            path = os.path.join(folder, have[key])
            with open(path, encoding="ascii", errors="replace") as handle:
                fields, old, kept = split_file(handle.read())
            if old == part:
                continue
            if min_interval > 0:
                try:
                    age = now - os.path.getmtime(path)
                except OSError:
                    age = min_interval
                if age < min_interval:
                    old_n, new_n = seen_count(old), seen_count(part)
                    sighting_jump = ((old_n == 0) != (new_n == 0)) or (abs(new_n - old_n) >= 5)
                    if not sighting_jump and structural_part(old) == structural_part(part):
                        continue
            letter = have[key][0]
            if not fields.get("id"):
                used = used_ids(root) if used is None else used
                fields["id"] = next_id(used, now)
        else:
            if created >= limit:
                continue
            created += 1
            used = used_ids(root) if used is None else used
            letter, kept = "n", ("%s\n\nAppend-only, newest last.\n\n| Date | Standing | Why | Source |\n|---|---|---|---|\n"
                                 "| %s | neutral | Filed by the tracker; it has not met us | `scripts/intel-factions.py` |\n\n## Notes\n\nNone.\n" % (KEPT_FROM, day))
            fields = {"id": next_id(used, now), "standing": "neutral", "standing_since": day, "threat": "unknown"}
            path = os.path.join(folder, "n-%s.md" % key)
        fields.update({"name": "faction-" + key, "tier": "intel", "author": "Unity", "kind": "faction", "tag": ascii_text(tag), "faction": ascii_text(name),
                       "standing": fields.get("standing") or STANDINGS[letter], "standing_since": fields.get("standing_since") or day,
                       "threat": fields.get("threat") or "unknown", "updated": day})
        os.makedirs(folder, exist_ok=True)
        with open(path + ".tmp", "w", encoding="ascii") as handle:
            handle.write(front(fields) + "\n" + part + "\n" + kept)
        os.replace(path + ".tmp", path)
        written.append(os.path.relpath(path, root))
    return written


def index_body(root, data):
    """The index text below its frontmatter: zones, factions by standing, tags in our space, pirate strongholds."""
    files = {}
    for key, name in existing(root).items():
        with open(os.path.join(root, "game", "factions", name), encoding="ascii", errors="replace") as handle:
            files[key] = (name, split_file(handle.read())[0])
    lines = ["# index.md -- Factions We Know and the Zones They Hold", "",
             "Built by `scripts/intel-factions.py` from the game's public data and the faction files of this folder;",
             "never edited by hand. Files listed: %d. The format of a faction file: `BLUEPRINT.md`." % len(files), "",
             "## Zones Held by Other Players", "",
             "Every system with a base of a player faction, the nearest to Nexus Prime first. A base is a station or an outpost.", ""]
    zones = {}
    for tag, bases in data["bases"].items():
        if tag == OWN_TAG:
            continue
        for b in bases:
            zones.setdefault((b["system"], tag), []).append("%s (%s%s)" % (ascii_text(b["name"]) or "unnamed", ascii_text(b["kind"]) or "base", ", wrecked" if b["wrecked"] else ""))
    if zones:
        lines += ["| System | Space | Jumps from Nexus Prime | Faction | Bases | File |", "|---|---|---|---|---|---|"]
        for (system, tag), named in sorted(zones.items(), key=lambda kv: (data["jumps"].get(kv[0][0], 10 ** 6), kv[0][0], kv[0][1])):
            name = (data["known"].get(tag) or {}).get("name") if isinstance(data["known"].get(tag), dict) else None
            file_name = files.get(key_of(tag), ("", {}))[0]
            lines.append("| %s | %s | %s | %s [%s] | %s | %s |" % (system_cell(data, system), ascii_text(data["space"].get(system, "not on the chart")), jumps_cell(data, system),
                                                                 ascii_text(name or data["bases"][tag][0]["faction"] or tag), ascii_text(tag), "; ".join(sorted(named)),
                                                                 "[%s](%s)" % (file_name, file_name) if file_name else "--"))
    else:
        lines.append("None on the public record.")
    for standing in ("hostile", "neutral", "ally"):
        lines += ["", "## %s" % standing.capitalize(), ""]
        rows = sorted((fields.get("tag", ""), name, fields) for name, fields in files.values() if fields.get("standing") == standing)
        if not rows:
            lines.append("None filed.")
            continue
        lines += ["| Faction | Tag | Threat | Bases | Nearest base (jumps) | Pilots in our space (24 h) | Updated | File |", "|---|---|---|---|---|---|---|---|"]
        for tag, name, fields in rows:
            raw_tag = next((t for t in set(data["bases"]) | set(data["seen"]) | set(data["known"]) if ascii_text(t) == tag), tag)
            bases = data["bases"].get(raw_tag, [])
            near = min((data["jumps"].get(b["system"], 10 ** 6) for b in bases), default=None)
            lines.append("| %s | %s | %s | %d | %s | %d | %s | [%s](%s) |" % (fields.get("faction", "--"), tag, fields.get("threat", "--"), len(bases),
                                                                             "--" if near is None else ("no lane found" if near >= 10 ** 6 else near),
                                                                             len(data["seen"].get(raw_tag, [])), fields.get("updated", "--"), name, name))
    lines += ["", "## Tags Seen in Our Space", "",
              "Every faction tag carried by a pilot whose last known system is one of ours (public event stream, last 24 hours).", ""]
    if data["seen"]:
        lines += ["| Tag | Faction | Pilots | File |", "|---|---|---|---|"]
        for tag, pilots in sorted(data["seen"].items(), key=lambda kv: (-len(kv[1]), kv[0])):
            if tag == OWN_TAG:
                continue
            name = (data["known"].get(tag) or {}).get("name") if isinstance(data["known"].get(tag), dict) else None
            file_name = files.get(key_of(tag), ("", {}))[0]
            lines.append("| %s | %s | %d | %s |" % (ascii_text(tag), ascii_text(name) if name else "not on record", len(pilots), "[%s](%s)" % (file_name, file_name) if file_name else "--"))
    else:
        lines.append("None in the last 24 hours.")
    lines += ["", "## Pirate Strongholds", ""]
    if data["pirates"]:
        lines += ["| System | Space | Jumps from Nexus Prime | Base |", "|---|---|---|---|"]
        for b in sorted(data["pirates"], key=lambda b: (data["jumps"].get(b["system"], 10 ** 6), b["system"])):
            lines.append("| %s | %s | %s | %s |" % (system_cell(data, b["system"]), ascii_text(data["space"].get(b["system"], "not on the chart")), jumps_cell(data, b["system"]), ascii_text(b["name"]) or "--"))
    else:
        lines.append("None on the public record.")
    return "\n".join(lines) + "\n"


def write_index(root, data, now, min_interval=0, files_written=None):
    """Write game/factions/index.md if it changed; returns its relative path, or None."""
    path = os.path.join(root, "game", "factions", "index.md")
    body = index_body(root, data)
    head = ""
    if os.path.isfile(path):
        with open(path, encoding="ascii", errors="replace") as handle:
            text = handle.read()
        if text.startswith("---\n") and "\n---\n" in text[4:]:
            end = text.index("\n---\n", 4) + 5
            head, old = text[:end], text[end:].lstrip("\n")
            if old == body:
                return None
            if min_interval > 0 and files_written == []:
                try:
                    age = now - os.path.getmtime(path)
                except OSError:
                    age = min_interval
                if age < min_interval and structural_index(old) == structural_index(body):
                    return None
    elif not existing(root):
        return None
    if not head:
        head = "---\nname: factions-index\nid: %s\ntier: intel\nauthor: Unity\n---\n" % next_id(used_ids(root), now)
    with open(path + ".tmp", "w", encoding="ascii") as handle:
        handle.write(head + "\n" + body)
    os.replace(path + ".tmp", path)
    return os.path.relpath(path, root)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="File the player factions that matter to us, and the zones they hold.")
    parser.add_argument("--root", default=os.path.join(here, ".."))
    parser.add_argument("--station", default=STATION)
    parser.add_argument("--met", default=MET)
    parser.add_argument("--fleet", default=FLEET)
    parser.add_argument("--max", type=int, default=40)
    parser.add_argument("--min-interval", type=int, default=0,
                        help="seconds before minor rolling-24h sighting drift rewrites an unchanged faction dossier (0=always)")
    args = parser.parse_args()
    root, now = os.path.abspath(args.root), time.time()
    data = gather(args.station, args.met, args.fleet, now)
    if not data["space"]:
        print("factions: the station's chart is not readable (%s); nothing written" % os.path.join(args.station, "map.json"))
        return 0
    written = write_files(root, data, now, args.max, min_interval=args.min_interval)
    index = write_index(root, data, now, min_interval=args.min_interval, files_written=written)
    for path in written + ([index] if index else []):
        print("written " + path)
    print("factions: %d file(s) written, index %s" % (len(written), "written" if index else "current"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
