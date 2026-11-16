#!/usr/bin/env python3
"""catalog-refresh.py -- keep the game's catalog in the data folder current: notice a new version, download it, check it, say what changed.

WHAT: the game publishes its catalog (items, recipes, facilities, hulls,
      skills) at https://game.spacemolt.com/api/catalog.json. Our readers
      (scripts/catalog-index.py, game/fleet/craftbook.py, store.py,
      surplus.py, routemaker.py, empire.py) take the newest
      <data>/catalog/<version>.json. This script keeps that file current:
        check     our version, the live version, and whether they differ
        refresh   when the live catalog is new: download it to a temporary
                  name in <data>/catalog/, check it, rename it to
                  <version>.json in one step, move older copies to old/,
                  print what changed and (--notice) write a log entry for
                  the queue log; when nothing is new: one line, nothing
                  written
        diff      what changed between two versions on disk
RULES:
  - The live version is learned cheaply: the game's public status
    (https://game.spacemolt.com/api/stats, about 200 bytes, names the
    running version). Only when it differs from ours is the catalog asked
    for, and then with the ETag of our copy (If-None-Match): an unchanged
    catalog answers 304 with no body, and since 0.715.5 such a
    revalidation does not count against the limit of one download a
    minute (game/rules/11-public-data.md). The ETag and what was done are
    kept in <data>/catalog/refresh.json.
  - A download replaces nothing until it passed the check: it parses, its
    version is digits and dots, and each group the readers use (items,
    recipes, facilities, ships, skills) is a list whose rows carry the
    fields they read, with at least 80% of the rows of the copy in force.
    A file that fails is moved aside as <version>.json.rejected, the reason
    is printed, the exit is 1, and the old copy stays in force. A catalog
    older than ours is refused the same way: every reader takes the
    highest version.
  - The two newest version files stay in <data>/catalog/; older ones are
    moved to <data>/catalog/old/. Nothing is ever deleted. A new copy of
    the version we hold (same name, other content) pushes the old bytes to
    old/<version>-<time>.json first.
  - The change summary lists per group the rows added, removed and changed
    (the first --top ids of each) and, for a changed row, every changed
    field a reader uses, old -> new; fields of text only (description,
    lore) are counted, not listed.
  - The notice (--notice <file>, outside the repository) is a queue entry
    in the protocol's form for `scripts/comms.py append queue`; it names no
    pilot of ours.
  - --dry-run downloads and checks but writes nothing: no file, no state,
    no notice.
  - Exit 0 when the work ran (a new catalog or none), 1 on an error: no
    answer from the game, a rejected download, a version not on disk.
WHY:  Suggi: "Always refresh the catalog data and all data when updates
      come out, so our data is accurate." The fleet's copy stood at 0.717.0
      while the game ran 0.719.3: every recipe, cost and hull figure the
      divisions planned with could be stale, and nobody was told. This
      script runs in the hourly job without AI; the catalog files, the craft
      book and the database follow the newest file by themselves.

USAGE:
  catalog-refresh.py check                    our version, the live one, same or not (exit 0)
  catalog-refresh.py refresh [--notice FILE]  fetch, check and install a new catalog; print what changed
  catalog-refresh.py refresh --dry-run        the same, writing nothing
  catalog-refresh.py diff <old> <new>         what changed between two versions on disk
  --data <dir>     the unit's data folder (default /srv/collective/data)
  --root <dir>     repository root (default: the parent of this file's folder)
  --url <url>      the catalog (default https://game.spacemolt.com/api/catalog.json)
  --stats-url <url>  the game's status, which names its version (default https://game.spacemolt.com/api/stats)
  --top <n>        ids and changed rows listed per group (default 15; 0 = all)

Stdlib only. ASCII only.
"""

import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
import zlib
from pathlib import Path

URL = "https://game.spacemolt.com/api/catalog.json"
STATS_URL = "https://game.spacemolt.com/api/stats"
DATA = "/srv/collective/data"
AGENT = "the-collective-catalog-refresh"
TIMEOUT = 120
MAX_BYTES = 64_000_000
STATE = "refresh.json"
KEEP = 2                                   # version files kept in the folder; older ones go to old/
FLOOR = 0.8                                # a download keeps at least this share of each group's rows
VERSION = re.compile(r"\d+(\.\d+)*")
GROUPS = (("items", "items"), ("recipes", "recipes"), ("facilities", "facilities"), ("ships", "hulls"), ("skills", "skills"),
          ("achievements", "achievements"), ("faction_achievements", "faction achievements"))
CHECKED = {"items": {"id": str, "size": None, "base_value": None},                       # the fields each reader takes (catalog-index.py,
           "recipes": {"id": str, "inputs": list, "outputs": list, "produced_by_facility_ids": list},   # craftbook.py, store.py):
           "facilities": {"id": str, "category": None, "level": None, "build_cost": None},              # name: the type it must have,
           "ships": {"id": str, "tier": None, "class": None, "build_materials": list},                  # None: present
           "skills": {"id": str, "max_level": None}}
TEXT = {"description", "lore", "satisfied_description", "degraded_description", "flavor_tags", "name", "title"}
QUANTITIES = {"inputs", "outputs", "build_materials", "maintenance_inputs"}
WEIGHTY = {"inputs", "outputs", "build_materials", "build_cost", "labor_cost", "crafting_time", "produced_by_facility_ids", "hand_craftable",
           "facility_only", "base_value", "size", "tier", "piloting_required", "shipyard_tier", "cargo_capacity", "max_level", "level", "recipe_id",
           "upgrades_from", "required_skills", "required_xenobiology"}     # a change here comes first in the lists
SINGULAR = {"items": "item", "recipes": "recipe", "facilities": "facility", "ships": "hull", "skills": "skill", "achievements": "achievement",
            "faction_achievements": "faction achievement"}
LINE = 300                                 # a summary line is cut here unless --top 0
NOTICE_LINES = 25
NOTICE_WIDTH = 220
LAST_LINE = "The catalog files, the craft book and the database follow within the hour."
NOTICE_HEAD = "## [ENT-NEXT] | NOW | Unity | general | ref: game/catalog/master-index.md"


class Refused(Exception):
    """A download that may not join the folder; the text says why."""


# ---------------------------------------------------------------- the network (a test replaces fetch)

def fetch(url, headers):
    """(status, {header: value} in lower case, body bytes) of one GET. 304 and other HTTP errors come back as a status,
    never raised; a body sent gzip-compressed is unpacked."""
    request = urllib.request.Request(url, headers=dict({"User-Agent": AGENT, "Accept-Encoding": "gzip"}, **headers))
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as answer:
            status, head, body = answer.status, {k.lower(): v for k, v in answer.headers.items()}, answer.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as error:
        error.close()
        return error.code, {k.lower(): v for k, v in (error.headers or {}).items()}, b""
    if len(body) > MAX_BYTES:
        raise ValueError("the answer is larger than %d bytes" % MAX_BYTES)
    if head.get("content-encoding", "").lower() == "gzip":
        unpack = zlib.decompressobj(16 + zlib.MAX_WBITS)
        body = unpack.decompress(body, MAX_BYTES + 1)
        if len(body) > MAX_BYTES or unpack.unconsumed_tail:
            raise ValueError("the unpacked answer is larger than %d bytes" % MAX_BYTES)
    return status, head, body


def live_version(stats_url):
    """(the version the game runs, None) or (None, the reason it is not known)."""
    try:
        status, _head, body = fetch(stats_url, {})
        if status != 200:
            return None, "the status page answered %s" % status
        version = json.loads(body.decode("utf-8")).get("version")
    except (OSError, ValueError, AttributeError) as error:
        return None, "the status page is not readable: %s: %s" % (type(error).__name__, error)
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        return None, "the status page names no version"
    return version, None


# ---------------------------------------------------------------- the folder

def key(version):
    return tuple(int(n) for n in version.split("."))


def versions(folder):
    """{version: path} of the catalog files directly in the folder (the readers' rule: the name is digits and dots)."""
    found = [p for p in Path(folder).glob("*.json") if VERSION.fullmatch(p.stem)] if Path(folder).is_dir() else []
    return {p.stem: p for p in found}


def newest(folder):
    held = versions(folder)
    return max(held, key=key) if held else None


def find(folder, version):
    """The file of a version: in the folder, or moved to old/."""
    for path in (Path(folder) / ("%s.json" % version), Path(folder) / "old" / ("%s.json" % version)):
        if path.is_file():
            return path
    return None


def read_state(folder):
    try:
        state = json.loads((Path(folder) / STATE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return state if isinstance(state, dict) else {}


def write_atomic(path, data):
    path = Path(path)
    tmp = path.with_name(".%s.%d.tmp" % (path.name, os.getpid()))
    tmp.write_bytes(data)
    os.replace(tmp, path)


def write_state(folder, state):
    write_atomic(Path(folder) / STATE, (json.dumps(state, indent=1, sort_keys=True) + "\n").encode("ascii"))


def free_name(path):
    """The path, or the path with -2, -3 ... before its suffixes when it is taken: nothing is ever written over."""
    path, n = Path(path), 2
    base, rest = path.name.split(".json", 1) if ".json" in path.name else (path.name, "")
    candidate = path
    while candidate.exists():
        candidate = path.with_name("%s-%d.json%s" % (base, n, rest))
        n += 1
    return candidate


def stamp(moment=None):
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() if moment is None else moment))


def retire(folder, dry=False):
    """Move every version file but the KEEP newest to old/; returns the names moved."""
    held = versions(folder)
    older = sorted(held, key=key, reverse=True)[KEEP:]
    moved = []
    for version in sorted(older, key=key):
        target = free_name(Path(folder) / "old" / held[version].name)
        if not dry:
            target.parent.mkdir(exist_ok=True)
            os.replace(held[version], target)
        moved.append("%s -> old/%s" % (held[version].name, target.name))
    return moved


# ---------------------------------------------------------------- the check of a download

def rows_of(cat, group):
    rows = cat.get(group)
    return [r for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str) and r["id"]] if isinstance(rows, list) else []


def usable(cat, group):
    """The rows of a group that carry every field a reader takes, with the right type."""
    out = []
    for row in rows_of(cat, group):
        if all(name in row and (kind is None or isinstance(row[name], kind)) for name, kind in CHECKED[group].items()):
            out.append(row)
    return out


def validate(raw, previous):
    """The catalog parsed from raw bytes, or Refused with the reason. previous: the catalog in force, or None."""
    try:
        cat = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise Refused("not JSON: %s" % str(error)[:120])
    if not isinstance(cat, dict):
        raise Refused("not a catalog: the top level is no object")
    version = cat.get("version")
    if not isinstance(version, str) or len(version) > 32 or not VERSION.fullmatch(version):
        raise Refused("no version of digits and dots: %r" % (str(version)[:40],))
    for group in CHECKED:
        if not isinstance(cat.get(group), list):
            raise Refused("version %s: no list `%s`" % (version, group))
        good, before = len(usable(cat, group)), len(usable(previous, group)) if isinstance(previous, dict) else 0
        if good == 0:
            raise Refused("version %s: `%s` holds no row with the fields %s" % (version, group, ", ".join(CHECKED[group])))
        if before and good < FLOOR * before:
            raise Refused("version %s: `%s` holds %d usable rows, the copy in force %d (the floor is %d%%)" % (version, group, good, before, FLOOR * 100))
    return cat


# ---------------------------------------------------------------- what changed

def show(value):
    if value is None:
        return "none"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return " ".join(str(value).split())


def quantities(rows):
    out = {}
    for r in rows or []:
        if isinstance(r, dict) and r.get("item_id") is not None:
            out[str(r["item_id"])] = out.get(str(r["item_id"]), 0) + (r.get("quantity") if isinstance(r.get("quantity"), (int, float)) else 0)
    return out


def reordered(name, old, new):
    """True when two lists hold the same things in another order: what a reader takes from them (a quantity per item, a
    set of ids) did not change."""
    if not (isinstance(old, list) and isinstance(new, list)) or old == new:
        return False
    if name in QUANTITIES:
        return quantities(old) == quantities(new) and len(old) == len(new)
    return sorted(map(show, old)) == sorted(map(show, new))


def change(name, old, new):
    """One field's change in words: `inputs: iron_ore 5 -> 6, +copper_ore x2, -silicon_ore x1`."""
    if name in QUANTITIES and all(isinstance(v, list) or v is None for v in (old, new)):
        a, b = quantities(old), quantities(new)
        parts = ["%s %s -> %s" % (i, show(a[i]), show(b[i])) for i in sorted(a) if i in b and a[i] != b[i]]
        parts += ["+%s x%s" % (i, show(b[i])) for i in sorted(b) if i not in a]
        parts += ["-%s x%s" % (i, show(a[i])) for i in sorted(a) if i not in b]
        return "%s: %s" % (name, ", ".join(parts) or "order or form only")
    if isinstance(old, dict) and isinstance(new, dict):
        names = sorted(set(old) | set(new))
        parts = ["%s %s -> %s" % (k, show(old.get(k)), show(new.get(k))) for k in names if old.get(k) != new.get(k)]
        return "%s: %s" % (name, ", ".join(parts))
    if isinstance(old, list) and isinstance(new, list) and all(not isinstance(v, (dict, list)) for v in old + new):
        if len(old) <= 12 and len(new) <= 12 and len(set(map(show, old))) == len(old) and len(set(map(show, new))) == len(new):
            a, b = set(map(show, old)), set(map(show, new))
            parts = ["+" + v for v in sorted(b - a)] + ["-" + v for v in sorted(a - b)]
            return "%s: %s" % (name, ", ".join(parts) or "order only")
        at = next((i for i, (x, y) in enumerate(zip(old, new)) if x != y), min(len(old), len(new)))
        return "%s: %d -> %d entries, first difference at %d: %s -> %s" % (name, len(old), len(new), at + 1, show(old[at]) if at < len(old) else "--",
                                                                               show(new[at]) if at < len(new) else "--")
    return "%s: %s -> %s" % (name, show(old), show(new))


def compare(old, new):
    """{group: {before, after, added, removed, figures: [(id, [change])], text: [id], order: [id]}} and the changes outside
    the groups. A row is changed in figures when a field a reader uses moved, in text only when only its words moved, in
    order only when only the order of a list moved (the same materials, the same quantities)."""
    out = {}
    for group, _label in GROUPS:
        if not isinstance(old.get(group), list) and not isinstance(new.get(group), list):
            continue
        a, b = {r["id"]: r for r in rows_of(old, group)}, {r["id"]: r for r in rows_of(new, group)}
        figures, text, order = [], [], []
        for rid in sorted(set(a) & set(b)):
            if a[rid] == b[rid]:
                continue
            names = sorted(n for n in set(a[rid]) | set(b[rid]) if a[rid].get(n) != b[rid].get(n))
            real = [n for n in names if n not in TEXT and not reordered(n, a[rid].get(n), b[rid].get(n))]
            if real:
                figures.append((-len([n for n in real if n in WEIGHTY]), rid, [change(n, a[rid].get(n), b[rid].get(n)) for n in real]))
            elif any(n in TEXT for n in names):
                text.append(rid)
            else:
                order.append(rid)
        figures = [(rid, moved) for _w, rid, moved in sorted(figures)]
        out[group] = {"before": len(a), "after": len(b), "added": sorted(set(b) - set(a)), "removed": sorted(set(a) - set(b)), "figures": figures, "text": text, "order": order,
                      "told": {rid: about(group, b[rid]) for rid in set(b) - set(a)} | {rid: about(group, a[rid]) for rid in set(a) - set(b)}}
    listed = {g for g, _l in GROUPS} | {"version"}
    other = [change(k, old.get(k), new.get(k)) for k in sorted(set(old) | set(new)) if k not in listed and old.get(k) != new.get(k)]
    return out, other


def about(group, row):
    """An added or removed row in a few words: what it is and its weightiest figure."""
    if group == "items":
        what = [row.get("category") or row.get("type"), "%s cr" % row["base_value"] if isinstance(row.get("base_value"), (int, float)) else None]
    elif group == "recipes":
        what = ["makes " + ", ".join("%s x%s" % (o, show(q)) for o, q in sorted(quantities(row.get("outputs")).items())) if row.get("outputs") else None]
    elif group == "facilities":
        what = [row.get("category"), "level %s" % row["level"] if row.get("level") is not None else None]
    elif group == "ships":
        what = [row.get("class"), "tier %s" % row["tier"] if row.get("tier") is not None else None]
    elif group == "skills":
        what = [row.get("category")]
    else:
        what = []
    words = ", ".join(show(w) for w in what if w)
    return "%s (%s)" % (row["id"], words) if words else row["id"]


def cut(line, top):
    return line if top == 0 or len(line) <= LINE else line[:LINE - 6] + " (cut)"


def ids(label, names, top):
    shown = names if top == 0 else names[:top]
    more = len(names) - len(shown)
    return "  %s: %s%s" % (label, ", ".join(shown), " (and %d more)" % more if more else "")


def when(path):
    return time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(Path(path).stat().st_mtime)) if path and Path(path).exists() else "not on disk yet"


def summary(old, new, old_path=None, new_path=None, top=15):
    """The change summary as plain lines: a heading with both versions and the files' dates, then one block per group."""
    groups, other = compare(old, new)
    lines = ["CATALOG CHANGES %s (file of %s) -> %s (file of %s)" % (old.get("version"), when(old_path), new.get("version"), when(new_path))]
    if not any(g["added"] or g["removed"] or g["figures"] or g["text"] or g["order"] for g in groups.values()) and not other:
        return lines + ["  no row of any group changed; only the version moved"]
    for group, label in GROUPS:
        g = groups.get(group)
        if g is None:
            continue
        changed = len(g["figures"]) + len(g["text"]) + len(g["order"])
        lines.append("%s: %d -> %d | added %d | removed %d | changed %d (%d in figures, %d in text only, %d in list order only)" % (
            label, g["before"], g["after"], len(g["added"]), len(g["removed"]), changed, len(g["figures"]), len(g["text"]), len(g["order"])))
        if g["added"]:
            lines.append(cut(ids("added", [g["told"][rid] for rid in g["added"]], top), top))
        if g["removed"]:
            lines.append(cut(ids("removed", [g["told"][rid] for rid in g["removed"]], top), top))
        if g["figures"]:
            lines.append("  changed in figures (old -> new), the weightiest first:")
            for rid, moved in g["figures"] if top == 0 else g["figures"][:top]:
                lines.append(cut("    %s: %s" % (rid, "; ".join(moved)), top))
            if top and len(g["figures"]) > top:
                lines.append("    (and %d more changed in figures)" % (len(g["figures"]) - top))
        if g["text"]:
            lines.append(cut(ids("text only", g["text"], top), top))
        if g["order"]:
            lines.append(cut(ids("list order only (the same materials and quantities)", g["order"], top), top))
    for line in other if top == 0 else other[:top]:
        lines.append(cut("other: " + line, top))
    return lines


# ---------------------------------------------------------------- the notice

def pilots_named(text, root):
    """The pilots of ours a text names, by the fleet's one rule for it (game/fleet/division.py); a local copy of the rule
    when the repository is not at hand."""
    sys.path.insert(0, str(Path(root) / "game" / "fleet"))
    try:
        import division
        return division.pilots_named(text)
    except ImportError:
        return re.findall(r"\b(?:command|drone|hauler|miner|scout|sentinel|trader)-[0-9]+\b", str(text))
    finally:
        sys.path.pop(0)


def notice(old, new, root, moved=()):
    """The queue entry of a new catalog: the heading line, then 5 to 25 plain lines (the versions, the counts, the weightiest
    changes, the command for every change and the last line). A line that reads like the name of a pilot of ours is left out."""
    groups, other = compare(old, new)
    before, after = old.get("version"), new.get("version")
    body = ["The game's catalog moved from %s to %s: the new copy is checked and in force in the data folder (catalog/%s.json)."
            % (before, after, after)]
    if moved:
        body.append("Moved to catalog/old/: %s." % ", ".join(moved))
    still = []
    for group, label in GROUPS:
        g = groups.get(group)
        if g is None:
            continue
        if g["added"] or g["removed"] or g["figures"]:
            body.append("%s %d -> %d: %d added, %d removed, %d changed in figures, %d in text only, %d in list order only." % (
                label.capitalize(), g["before"], g["after"], len(g["added"]), len(g["removed"]), len(g["figures"]), len(g["text"]), len(g["order"])))
        else:
            quiet = ", ".join("%d in %s" % (len(g[k]), w) for k, w in (("text", "text only"), ("order", "list order only")) if g[k])
            still.append("%s %d%s" % (label, g["after"], " (%s)" % quiet if quiet else ""))
    if still:
        body.append("No row added, removed or changed in figures: %s." % ", ".join(still))
    if not any(g["added"] or g["removed"] or g["figures"] for g in groups.values()):
        body.append("Only the version moved: no figure a reader uses changed.")
    if other:
        body.append("Outside the groups: %s." % "; ".join(other[:3]))
    for group, label in GROUPS[:5]:
        g = groups.get(group)
        for word, names in (("New", g["added"] if g else []), ("Gone", g["removed"] if g else [])):
            if names:
                body.append("%s %s: %s%s." % (word, label, ", ".join(g["told"][rid] for rid in names[:6]), " and %d more" % (len(names) - 6) if len(names) > 6 else ""))
    picks = []
    for rank in range(3):                                       # the weightiest change of each group first, then the second ...
        for group, _label in GROUPS[:5]:
            g = groups.get(group)
            if g and len(g["figures"]) > rank:
                rid, fields = g["figures"][rank]
                picks.append("Changed %s %s: %s." % (SINGULAR[group], rid, "; ".join(fields)))
    tail = ["Every change: python3 -B scripts/catalog-refresh.py diff %s %s" % (before, after), LAST_LINE]
    lines, dropped = [], 0
    for line in body + picks:
        line = line if len(line) <= NOTICE_WIDTH else line[:NOTICE_WIDTH - 6] + " (cut)"
        if pilots_named(line, root):
            dropped += 1
        else:
            lines.append(line)
    if dropped:
        lines.append("%d line(s) left out: they read like the name of a pilot of ours." % dropped)
    lines = lines[:NOTICE_LINES - len(tail)] + tail
    return "\n".join([NOTICE_HEAD] + lines) + "\n"


# ---------------------------------------------------------------- the verbs

def load(path):
    try:
        cat = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return cat if isinstance(cat, dict) else None


def do_check(folder, args):
    ours = newest(folder)
    live, why = live_version(args.stats_url)
    state = read_state(folder)
    print("ours: %s | live: %s | %s" % (ours or "none", live or "unknown (%s)" % why,
                                         "differ" if live and live != ours else "same" if live else "not compared"))
    if state.get("rejected"):
        r = state["rejected"]
        print("last rejected download: %s at %s: %s" % (r.get("version"), r.get("at"), r.get("reason")))
    return 0


def do_diff(folder, args):
    paths = [find(folder, v) for v in (args.old, args.new)]
    for version, path in zip((args.old, args.new), paths):
        if path is None:
            print("catalog-refresh: no file of version %s in %s or its old/" % (version, folder))
            return 1
    old, new = load(paths[0]), load(paths[1])
    if old is None or new is None:
        print("catalog-refresh: a catalog file is not readable JSON")
        return 1
    print("\n".join(summary(old, new, paths[0], paths[1], args.top)))
    return 0


def reject(folder, tmp, raw, why, state, etag, args):
    """Move a refused download aside, keep its ETag and hash so it is not fetched and kept again, and say why. The same
    bytes refused before are said in one line with exit 0: the first refusal was the alarm."""
    version = None
    try:
        version = json.loads(raw.decode("utf-8")).get("version")
    except (UnicodeDecodeError, ValueError, AttributeError):
        pass
    version = version if isinstance(version, str) and VERSION.fullmatch(version) else None
    digest = hashlib.sha256(raw).hexdigest()
    if args.dry_run:
        print("REJECTED (dry run, nothing written): %s" % why)
        return 1
    before = state.get("rejected") or {}
    if before.get("sha256") == digest and (folder / str(before.get("file"))).is_file():
        tmp.unlink()                                             # our own download, the same bytes as the file kept aside
        print("the live catalog is still the one rejected at %s (%s); the copy in force stays %s" % (before.get("at"), before.get("reason"), newest(folder)))
        return 0
    target = free_name(folder / ("%s.json.rejected" % (version or "unknown")))
    os.replace(tmp, target)
    write_state(folder, dict(state, rejected={"version": version, "etag": etag, "sha256": digest, "reason": why, "at": stamp(), "file": target.name}))
    print("REJECTED: %s; moved aside as %s; the copy in force stays %s" % (why, target.name, newest(folder) or "none"))
    return 1


def do_refresh(folder, root, args):
    if not args.dry_run:
        folder.mkdir(parents=True, exist_ok=True)
    if not folder.is_dir():
        print("catalog-refresh: no folder %s" % folder)
        return 1
    if args.dry_run:
        return refresh(folder, root, args)
    lock = os.open(folder, os.O_RDONLY)                          # one refresh at a time (the hourly job, a member by hand):
    try:                                                         # the lock is on the folder itself, so no file is written
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            print("catalog-refresh: another refresh holds the lock; nothing done")
            return 0
        return refresh(folder, root, args)
    finally:
        os.close(lock)


def install_report(folder, root, args, old_cat, old_path, new_cat, new_path, moved):
    print("\n".join(summary(old_cat or {"version": "none"}, new_cat, old_path, new_path, args.top)))
    if moved:
        print("moved to old/: " + ", ".join(moved))
    if args.notice and old_cat is not None and not args.dry_run:
        write_atomic(Path(args.notice), notice(old_cat, new_cat, root, moved).encode("ascii", "replace"))
        print("notice written: %s" % args.notice)


def refresh(folder, root, args):
    state = read_state(folder)
    held = versions(folder)
    ours = newest(folder)
    ours_path = held.get(ours)
    ours_cat = load(ours_path) if ours_path else None
    # 1. a copy that came in by another hand (the route maker's daily fetch) is announced once, against the last one
    #    announced; on the first run the second-newest file of the folder stands for it
    lower = sorted((v for v in held if v != ours), key=key)
    announced = state.get("announced") or (lower[-1] if lower else None)
    if ours and announced and key(ours) > key(announced) and find(folder, announced):
        before_cat = load(find(folder, announced))
        print("catalog %s is on disk beside %s and was not announced yet:" % (ours, announced))
        moved = retire(folder, dry=args.dry_run)
        install_report(folder, root, args, before_cat, find(folder, announced), ours_cat, ours_path, moved)
        if not args.dry_run:
            write_state(folder, dict(state, announced=ours))
        return 0
    # 2. the game's version, about 200 bytes: the same as ours, and nothing more is asked
    live, why = live_version(args.stats_url)
    if live is not None and live == ours:
        print("catalog current: %s (the game runs %s)" % (ours, live))
        return 0
    # 3. the catalog itself, with the ETags of our copy and of a refused one: an unchanged catalog answers 304, no body
    tags = [t for t in (state.get("etag") if state.get("etag_version") == ours else None, (state.get("rejected") or {}).get("etag")) if t]
    headers = {"If-None-Match": ", ".join(dict.fromkeys(tags))} if tags else {}
    try:
        status, head, raw = fetch(args.url, headers)
    except (OSError, ValueError) as error:
        print("FAILED: the catalog could not be fetched: %s: %s; the copy in force stays %s" % (type(error).__name__, error, ours or "none"))
        return 1
    etag = head.get("etag")
    if status == 304:
        refused = (state.get("rejected") or {})
        if refused.get("etag") and refused.get("etag") in (etag, headers.get("If-None-Match")):
            print("the live catalog is still the one rejected at %s (%s); the copy in force stays %s" % (refused.get("at"), refused.get("reason"), ours))
        else:
            print("catalog current: %s; the game runs %s with the same catalog (ETag %s)" % (ours, live or "a version not read: %s" % why, etag or "kept"))
        return 0
    if status != 200 or not raw:
        print("FAILED: the catalog answered %s with %d bytes; the copy in force stays %s" % (status, len(raw), ours or "none"))
        return 1
    # 4. the check: nothing joins the folder before it passed
    tmp = folder / (".download-%d.tmp" % os.getpid())
    if not args.dry_run:
        tmp.write_bytes(raw)
    try:
        cat = validate(raw, ours_cat)
        version = cat["version"]
        if ours and key(version) < key(ours):
            raise Refused("version %s is older than our copy %s: every reader takes the highest version" % (version, ours))
    except Refused as error:
        return reject(folder, tmp, raw, str(error), state, etag, args)
    target = folder / ("%s.json" % version)
    fresh = dict(state, etag=etag, etag_version=version, checked_at=stamp())
    fresh.pop("rejected", None)
    if version == ours and cat == ours_cat:
        if not args.dry_run:
            tmp.unlink()
            if etag and (etag != state.get("etag") or state.get("etag_version") != ours):
                write_state(folder, fresh)                       # the ETag of our copy: the next ask is answered 304
        print("catalog current: %s; the game runs %s with the same catalog%s" % (ours, live or "a version not read", " (dry run)" if args.dry_run else ""))
        return 0
    # 5. the rename, in one step, then the old copies to old/
    old_cat, old_path = ours_cat, ours_path
    if version == ours:                                          # the same name, other content: the old bytes go to old/ first
        kept = free_name(folder / "old" / ("%s-%s.json" % (version, stamp())))
        if not args.dry_run:
            kept.parent.mkdir(exist_ok=True)
            shutil.copy2(ours_path, kept)
            old_path = kept
        print("catalog %s was published again with other content; the old copy %s old/%s" % (version, "would be kept as" if args.dry_run else "is kept as", kept.name))
    if args.dry_run:
        print("DRY RUN: would install %s.json (%d bytes) beside %s; nothing written" % (version, len(raw), ours or "nothing"))
        older = sorted(dict(held, **{version: target}), key=key, reverse=True)[KEEP:]
        install_report(folder, root, args, old_cat, old_path, cat, None, ["%s.json -> old/" % v for v in sorted(older, key=key)])
        return 0
    os.replace(tmp, target)
    moved = retire(folder)
    write_state(folder, dict(fresh, announced=version, installed_at=stamp(), installed_from=ours))
    print("installed %s.json (%d bytes); in force now instead of %s" % (version, len(raw), ours or "nothing"))
    install_report(folder, root, args, old_cat, old_path, cat, target, moved)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Keep the game's catalog in the data folder current and say what changed.")
    parser.add_argument("verb", choices=("check", "refresh", "diff"))
    parser.add_argument("old", nargs="?")
    parser.add_argument("new", nargs="?")
    parser.add_argument("--data", default=DATA)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--url", default=URL)
    parser.add_argument("--stats-url", default=STATS_URL)
    parser.add_argument("--notice")
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.top < 0:
        parser.error("--top takes 0 or more")
    folder = Path(args.data) / "catalog"
    if args.verb == "diff":
        if not args.old or not args.new:
            parser.error("diff takes two versions: diff <old> <new>")
        return do_diff(folder, args)
    if args.old or args.new:
        parser.error("%s takes no version" % args.verb)
    if args.notice and Path(args.notice).resolve().is_relative_to(Path(args.root).resolve()):
        print("catalog-refresh: keep the notice file outside the repository (an untracked file there holds every push)")
        return 1
    if args.verb == "check":
        return do_check(folder, args)
    return do_refresh(folder, args.root, args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
