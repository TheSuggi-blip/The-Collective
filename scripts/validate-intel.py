#!/usr/bin/env python3
"""validate-intel.py -- gate for the intel files in planets/ and players/.

WHAT: checks every data file in planets/ and players/ against the rules
of that folder's BLUEPRINT.md, and tells a writer which file name a
pilot or a star system gets.

RULES CHECKED:
  1. The file name is <letter>-<key>.md: a (ally), n (neutral) or
     h (hostile).
  2. The frontmatter carries the required fields.
  3. The letter matches the `standing` field.
  4. The key matches the pilot's username (players/) or the system id
     (planets/). A second pilot whose name gives the same key gets
     the suffix -2, -3, ...
  5. One file per pilot and per system: nobody is filed twice, not
     even under another letter.
  6. Ally and hostile standing name who set it and why.
  7. `threat` is unknown, low, medium or high; dates are YYYY-MM-DD.
  8. A system id that is not in map/galaxy.tsv is a warning (a typo,
     or a system that is not on the public chart).

Files whose name starts with an upper-case letter (BLUEPRINT.md) and
dot files are not data files and are skipped.

USAGE:
  validate-intel.py                     check both folders; exit 1 on errors
  validate-intel.py --name player "<username>" [ally|neutral|hostile]
  validate-intel.py --name planet <system_id> [ally|neutral|hostile]
  validate-intel.py --root <dir>        check another tree (used by tests)

Stdlib only. ASCII only.
"""

import argparse
import os
import re
import sys

STANDINGS = {"a": "ally", "n": "neutral", "h": "hostile"}
LETTERS = {word: letter for letter, word in STANDINGS.items()}
THREATS = ("unknown", "low", "medium", "high")
FOLDERS = {"players": "player", "planets": "system"}
ID_FIELD = {"player": "username", "system": "system_id"}
REQUIRED = ["name", "id", "tier", "author", "kind", "standing",
            "standing_since", "threat", "updated"]
DATE_FIELDS = ["standing_since", "updated"]
FILE_RE = re.compile(r"^([anh])-([a-z0-9_.\-]+)\.md$")
SYSTEM_ID_RE = re.compile(r"^[a-z0-9_]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SUFFIX_RE = re.compile(r"^-[0-9]+$")
ESCAPE_RE = re.compile(r"\\u\{([0-9A-Fa-f]{1,6})\}")
KEEP = set("abcdefghijklmnopqrstuvwxyz0123456789_.-")


def decode_escapes(text):
    """Turn the ASCII form \\u{1F980} back into the character it stands for."""
    return ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), text)


def player_key(username):
    """File key of a pilot: lower case, space -> _, other ASCII
    punctuation dropped, any non-ASCII character written as u<hex>."""
    out = []
    for ch in decode_escapes(username).strip().lower():
        if ch in KEEP:
            out.append(ch)
        elif ch == " ":
            out.append("_")
        elif ord(ch) < 128:
            continue
        else:
            out.append("u%x" % ord(ch))
    return "".join(out) or "unnamed"


def ident_of(kind, entity):
    """What makes two entries the same pilot or the same system."""
    return decode_escapes(entity).strip().lower() if kind == "player" else entity.strip()


def base_key(kind, entity):
    return player_key(entity) if kind == "player" else entity.strip()


def key_fits(kind, key, entity):
    base = base_key(kind, entity)
    if key == base:
        return True
    return kind == "player" and key.startswith(base) and bool(SUFFIX_RE.match(key[len(base):]))


def read_frontmatter(path):
    """Return (fields, error). Frontmatter is the key: value block
    between the first two --- lines."""
    try:
        with open(path, encoding="ascii") as handle:
            lines = handle.read().split("\n")
    except UnicodeDecodeError:
        return None, "contains non-ASCII characters"
    if not lines or lines[0].strip() != "---":
        return None, "no frontmatter (the first line must be ---)"
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields, None
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return None, "the frontmatter is not closed with ---"


def chart_ids(root):
    """System ids in map/galaxy.tsv, or None when there is no chart."""
    path = os.path.join(root, "map", "galaxy.tsv")
    if not os.path.isfile(path):
        return None
    ids = set()
    with open(path, encoding="ascii", errors="replace") as handle:
        for line in handle:
            first = line.split("\t", 1)[0].strip()
            if first and first != "id" and not line.startswith("#"):
                ids.add(first)
    return ids


def data_files(root, folder):
    """Yield (file name, letter, key) for each data file, or
    (file name, None, problem) for a name that breaks the rule."""
    directory = os.path.join(root, folder)
    if not os.path.isdir(directory):
        return
    for name in sorted(os.listdir(directory)):
        if os.path.isdir(os.path.join(directory, name)):
            yield name, None, "folders are not allowed here"
            continue
        if name.startswith(".") or name[:1].isupper():
            continue
        match = FILE_RE.match(name)
        if match:
            yield name, match.group(1), match.group(2)
        else:
            yield name, None, "the name must be <a|n|h>-<key>.md in lower case"


def check(root):
    errors, warnings, counts = [], [], {}
    known = chart_ids(root)
    for folder, kind in FOLDERS.items():
        seen_key, seen_entity = {}, {}
        counts[folder] = 0
        id_field = ID_FIELD[kind]
        for name, letter, key in data_files(root, folder):
            rel = "%s/%s" % (folder, name)
            if letter is None:
                errors.append("%s: %s" % (rel, key))
                continue
            counts[folder] += 1
            if key in seen_key:
                errors.append("%s: the key `%s` is already used by %s" % (rel, key, seen_key[key]))
            seen_key.setdefault(key, rel)
            fields, problem = read_frontmatter(os.path.join(root, folder, name))
            if fields is None:
                errors.append("%s: %s" % (rel, problem))
                continue
            for field in REQUIRED + [id_field]:
                if not fields.get(field):
                    errors.append("%s: the frontmatter field `%s` is missing" % (rel, field))
            if fields.get("kind") and fields["kind"] != kind:
                errors.append("%s: `kind` must be %s" % (rel, kind))
            for field in DATE_FIELDS:
                if fields.get(field) and not DATE_RE.match(fields[field]):
                    errors.append("%s: `%s` must be a date, YYYY-MM-DD" % (rel, field))
            if fields.get("threat") and fields["threat"] not in THREATS:
                errors.append("%s: `threat` must be one of %s" % (rel, ", ".join(THREATS)))
            standing = fields.get("standing", "")
            if standing and standing not in LETTERS:
                errors.append("%s: `standing` must be ally, neutral or hostile" % rel)
            elif standing and LETTERS[standing] != letter:
                errors.append(
                    "%s: the name says `%s-` but the standing is %s (rename it to %s-%s.md)"
                    % (rel, letter, standing, LETTERS[standing], key)
                )
            if standing in ("ally", "hostile"):
                for field in ("standing_by", "standing_reason"):
                    if not fields.get(field):
                        errors.append("%s: %s standing needs `%s`" % (rel, standing, field))
            entity = fields.get(id_field, "")
            if not entity:
                continue
            if kind == "system" and not SYSTEM_ID_RE.match(entity):
                errors.append("%s: `system_id` must be the game's id (a-z, 0-9, _)" % rel)
            if not key_fits(kind, key, entity):
                errors.append(
                    "%s: the key `%s` does not fit %s `%s` (expected `%s`)"
                    % (rel, key, id_field, entity, base_key(kind, entity))
                )
            if kind == "system" and known is not None and entity not in known:
                warnings.append("%s: `%s` is not in map/galaxy.tsv" % (rel, entity))
            ident = ident_of(kind, entity)
            if ident in seen_entity:
                errors.append(
                    "%s: %s `%s` is already filed in %s"
                    % (rel, id_field, entity, seen_entity[ident])
                )
            seen_entity.setdefault(ident, rel)
    return errors, warnings, counts


def suggest_name(root, what, entity, standing):
    """Return (path, note): the file a pilot or system belongs in."""
    kind = "player" if what == "player" else "system"
    folder = "players" if kind == "player" else "planets"
    id_field = ID_FIELD[kind]
    ident = ident_of(kind, entity)
    keys, existing = set(), None
    for name, letter, key in data_files(root, folder):
        if letter is None:
            continue
        keys.add(key)
        fields, _ = read_frontmatter(os.path.join(root, folder, name))
        if fields and fields.get(id_field) and ident_of(kind, fields[id_field]) == ident:
            existing = (name, key)
    if existing:
        target = "%s-%s.md" % (LETTERS[standing], existing[1])
        if target == existing[0]:
            return "%s/%s" % (folder, target), "exists already; edit it, do not create a second file"
        return ("%s/%s" % (folder, target),
                "filed as %s/%s; rename it with: git mv %s/%s %s/%s"
                % (folder, existing[0], folder, existing[0], folder, target))
    key = base_key(kind, entity)
    note = "new file"
    if key in keys:
        number = 2
        while "%s-%d" % (key, number) in keys:
            number += 1
        note = "new file; the key `%s` belongs to another pilot, so this one gets a suffix" % key
        key = "%s-%d" % (key, number)
    return "%s/%s-%s.md" % (folder, LETTERS[standing], key), note


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Gate for planets/ and players/.")
    parser.add_argument("--root", default=os.path.join(here, ".."))
    parser.add_argument("--name", nargs="+", metavar="ARG",
                        help='player "<username>" [standing] | planet <system_id> [standing]')
    args = parser.parse_args()
    root = os.path.abspath(args.root)

    if args.name:
        if len(args.name) not in (2, 3) or args.name[0] not in ("player", "planet"):
            parser.error('--name takes: player "<username>" [standing] | planet <system_id> [standing]')
        standing = args.name[2] if len(args.name) == 3 else "neutral"
        if standing not in LETTERS:
            parser.error("the standing must be ally, neutral or hostile")
        entity = args.name[1]
        if args.name[0] == "planet":
            entity = entity.strip()
            if not SYSTEM_ID_RE.match(entity):
                parser.error("the system id must be the game's id (a-z, 0-9, _); look it up in map/galaxy.tsv")
            known = chart_ids(root)
            if known is not None and entity not in known:
                print("# WARNING: `%s` is not in map/galaxy.tsv" % entity, file=sys.stderr)
        path, note = suggest_name(root, args.name[0], entity, standing)
        print(path)
        print("# " + note)
        return 0

    errors, warnings, counts = check(root)
    for line in warnings:
        print("WARNING: " + line)
    for line in errors:
        print("ERROR: " + line)
    if warnings or errors:
        print("")
    print("Checked %d player files and %d system files."
          % (counts.get("players", 0), counts.get("planets", 0)))
    print("Errors: %d | Warnings: %d" % (len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
