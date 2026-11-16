#!/usr/bin/env python3
"""observe.py -- a member writes down what it saw in the game (a scan far away, a price at a station we read no book of, a fight with a species) as one checked line of its division's own record; the store makes the lines one SQL table, `observations`.

WHAT: `add` appends ONE JSON line to <data>/observations/<division>.jsonl, the record of the caller's division:
        {"t": "2026-11-16T22:10:05Z", "member": "Oracle", "division": "intel", "kind": "scan", "subject": "sys_far",
         "fields": {"belts": 2, "ice": true, "owner": "ROGU"}, "note": "two belts, no station"}
      t is when it was seen (--at, default now). The service `store` (store.py) reads the new whole lines of the six
      records into the table `observations` at its next pass and publishes them with its next copy:
      `hive.py sql "SELECT ... FROM observations"`, a field by json_extract(fields, '$.<key>'). `show` and `kinds` read
      the records themselves: what was written, also before the store took it.
RULES:
  - Only a member writes (Unity or an Admiral, by division.member: HERMES_SESSION_PROFILE or HERMES_HOME), and only its
    own division's record: Unity command, Zero mining, Mercury trade, Apollo logistics, Apophis military, Oracle intel.
    A service or any other shell writes nothing: the records are written in the agents' container only, where the
    lock below holds (services README, "Data": a lock is not seen between the two containers).
  - kind: a lower-case letter, then 1 to 31 lower-case letters, digits or _. subject: 1 to 120 printable ASCII
    characters, not blank. At most 24 fields; a key: a lower-case letter, then up to 31 lower-case letters, digits or
    _, each key once; a value: a number (JSON's form: 12, -3.5, 1e3; `007` stays a text), true or false, else a text
    of 1 to 200 printable ASCII characters. note: at most 400 printable ASCII characters. The whole line: at most 4000
    bytes. --at: not more than 10 minutes ahead of this clock, and not older than 30 days (the store keeps
    observations 30 days: an older one would never reach the table). A broken rule writes nothing: one plain line,
    exit 1 (ValueError with that line from add()).
  - One writer at a time per record: an exclusive flock on the record itself, opened for appending, and the whole line
    in one write ending in its newline. A record whose last line was left without its newline gets one first, so a
    broken line never swallows the next. This script never changes or takes out a line.
  - An observation never goes into the repository: the records live in the data folder only (they may name our ships
    and where they are). Write what no file of the fleet holds already: not order books, census counts or runs.
  - Look before you name (`kinds`): one name per kind of thing, the same keys for the same measure.
WHY:  store.py is the Fleet Admiral's alone, so an Admiral that measured something new (a scan, a travel time, what a
      mission paid, a price seen far away) had no table for it. Suggi, 2026-11-16: the Admirals do the easier data
      work themselves, where it cannot break the systems. A checked line in a record of its own is that: the store
      only reads it.

From another script:
  observe.add(kind, subject, fields, note="", at=None, data=None, member=None)
                                  the row written ({t, member, division, kind, subject, fields, note}); ValueError
                                  with the same plain line on a broken rule. member, when given, must be the shell's
                                  own: a script cannot write in another member's name
  observe.rows(data=None, which=None)
                                  the readable rows of one division's record (None: of all six), oldest first

USAGE:
  observe.py add <kind> <subject> [key=value ...] [--note "text"] [--at <UTC time>]   one observation (default: now)
  observe.py show [<kind>] [--subject <text>] [--division <name>|all] [--last N]       the newest rows as plain lines
                                                                                       (default: own division, 20 rows)
  observe.py kinds [--division <name>|all]                                             every kind on record: its rows,
                                                                                       newest time and field names
  --data <dir>   the unit's data folder (default /srv/collective/data)
  --at           2026-11-16T22:10:05Z, 2026-11-16 22:10 (UTC)
  --subject      the rows whose subject holds the text (any case)

Stdlib only. ASCII only.
"""

import calendar
import fcntl
import json
import math
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names (NAMES), as the store names its records
import division                                   # noqa: E402  who is asking (member), the data folder

FOLDER = "observations"        # <data>/observations/<division>.jsonl, one record per division
KIND = re.compile(r"[a-z][a-z0-9_]{1,31}")
KEY = re.compile(r"[a-z][a-z0-9_]{0,31}")
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?")     # JSON's number: `007` is no number
WHEN = re.compile(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})(:\d{2})?Z?")
SUBJECT_MAX, FIELDS_MAX, VALUE_MAX, NOTE_MAX, LINE_MAX = 120, 24, 200, 400, 4000
AHEAD = 600                    # seconds an observation may lie ahead of this clock (clocks differ a little, not more)
OLDEST_DAYS = 30               # store.py keeps observations this long (KEEP_TABLES): an older one would never reach the table
DIVISIONS = {member: board.NAMES[member].lower() for member in division.MEMBERS}    # Unity command, Zero mining, ...


def stamp(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def printable(text):
    return all(" " <= char <= "~" for char in text)


def division_of(word):
    """The division a word names: a division's name or a member's; None for anything else."""
    word = str(word or "").strip()
    if word.lower() in DIVISIONS.values():
        return word.lower()
    return DIVISIONS.get(word.capitalize())


def writer(member=None, env=None):
    """The member that writes and its division; ValueError when this shell may write no observation."""
    kind, name = division.member(env)
    if kind is None:
        raise ValueError("refused: this shell is no member of The Collective (HERMES_SESSION_PROFILE and HERMES_HOME name none): "
                         "only a member writes an observation")
    if kind == "service":
        raise ValueError("refused: the service %s writes no observation: a member writes them, in the agents' container where the "
                         "record's lock holds" % name)
    if member is not None and str(member).strip().capitalize() != name:
        raise ValueError("refused: this shell is %s: it writes as %s only, not as %s" % (name, name, member))
    return name, DIVISIONS[name]


def when(at, now):
    """(epoch, stamp) of --at: None for now, an epoch number, or a UTC text; ValueError when unreadable or out of range."""
    if at is None or at == "":
        t = int(now)
    elif isinstance(at, (int, float)) and not isinstance(at, bool):
        if not math.isfinite(at):
            raise ValueError("refused: --at `%s` is no time" % at)
        t = int(at)
    else:
        found = WHEN.fullmatch(str(at).strip())
        if not found:
            raise ValueError("refused: --at `%s` is no UTC time: write 2026-11-16T22:10:05Z or 2026-11-16 22:10" % at)
        try:
            t = calendar.timegm(time.strptime("%sT%s%s" % (found.group(1), found.group(2), found.group(3) or ":00"), "%Y-%m-%dT%H:%M:%S"))
        except ValueError:
            raise ValueError("refused: --at `%s` is no UTC time: write 2026-11-16T22:10:05Z or 2026-11-16 22:10" % at) from None
    if t > now + AHEAD:
        raise ValueError("refused: --at %s lies ahead of this clock (%s): an observation is of what was seen" % (stamp(t), stamp(now)))
    if t < now - OLDEST_DAYS * 86400:
        raise ValueError("refused: --at %s is older than %d days: the store keeps observations %d days, an older one never "
                         "reaches the table" % (stamp(t), OLDEST_DAYS, OLDEST_DAYS))
    return t, stamp(t)


def check_value(key, value):
    """The value as it is written; ValueError for anything but a number, true/false or a short printable text."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("refused: field `%s`: %s is no number JSON can carry" % (key, value))
        return value
    if isinstance(value, str):
        if not value:
            raise ValueError("refused: field `%s` has no value" % key)
        if len(value) > VALUE_MAX:
            raise ValueError("refused: field `%s` is %d characters long; a text value is at most %d" % (key, len(value), VALUE_MAX))
        if not printable(value):
            raise ValueError("refused: field `%s` holds a character that is no printable ASCII (a tab, a line break, an accent)" % key)
        return value
    raise ValueError("refused: field `%s` is a %s: a value is a number, true or false, or a text" % (key, type(value).__name__))


def value_of(text):
    """A value as typed on the command line: true/false, a number in JSON's form, else the text itself."""
    if text in ("true", "false"):
        return text == "true"
    if NUMBER.fullmatch(text):
        return float(text) if any(char in text for char in ".eE") else int(text)
    return text


def make_row(kind, subject, fields, note="", at=None, member=None, env=None, now=None):
    """The row add() writes and its line as bytes; ValueError with one plain line on a broken rule. Nothing is written."""
    now = time.time() if now is None else now
    name, own = writer(member, env)
    kind = str(kind) if isinstance(kind, str) else ""
    if not KIND.fullmatch(kind):
        raise ValueError("refused: kind `%s` must be 2 to 32 characters: a lower-case letter, then lower-case letters, digits or _" % kind)
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("refused: no subject: name what was observed (a system, a station, a species, a route)")
    if len(subject) > SUBJECT_MAX:
        raise ValueError("refused: the subject is %d characters long; at most %d" % (len(subject), SUBJECT_MAX))
    if not printable(subject):
        raise ValueError("refused: the subject holds a character that is no printable ASCII (a tab, a line break, an accent)")
    fields = {} if fields is None else fields
    if not isinstance(fields, dict):
        raise ValueError("refused: the fields are a dict of key: value, not a %s" % type(fields).__name__)
    if len(fields) > FIELDS_MAX:
        raise ValueError("refused: %d fields; at most %d" % (len(fields), FIELDS_MAX))
    checked = {}
    for key, value in fields.items():
        if not isinstance(key, str) or not KEY.fullmatch(key):
            raise ValueError("refused: key `%s` must be 1 to 32 characters: a lower-case letter, then lower-case letters, digits or _" % key)
        checked[key] = check_value(key, value)
    note = "" if note is None else note
    if not isinstance(note, str):
        raise ValueError("refused: the note is a %s, not a text" % type(note).__name__)
    if len(note) > NOTE_MAX:
        raise ValueError("refused: the note is %d characters long; at most %d" % (len(note), NOTE_MAX))
    if not printable(note):
        raise ValueError("refused: the note holds a character that is no printable ASCII (a tab, a line break, an accent)")
    _t, seen = when(at, now)
    row = {"t": seen, "member": name, "division": own, "kind": kind, "subject": subject, "fields": checked, "note": note}
    line = (json.dumps(row) + "\n").encode("ascii")
    if len(line) > LINE_MAX:
        raise ValueError("refused: the line would be %d bytes; at most %d: fewer or shorter fields, a shorter note" % (len(line), LINE_MAX))
    return row, line


def record(data, name):
    return Path(data) / FOLDER / ("%s.jsonl" % name)


def append(path, line):
    """One whole line onto the record under its lock: the lock is taken on the record itself, opened for appending, so
    two members (or two of one member's scripts) never write into each other's line."""
    try:
        path.parent.mkdir(exist_ok=True)
    except FileNotFoundError:
        raise ValueError("refused: no data folder %s" % path.parent.parent) from None
    handle = os.open(str(path), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        fcntl.flock(handle, fcntl.LOCK_EX)
        size = os.fstat(handle).st_size
        if size and last_byte(path, size) != b"\n":
            line = b"\n" + line                    # a line someone left without its newline would swallow this one
        written = os.write(handle, line)
        if written != len(line):
            raise OSError("only %d of %d bytes written to %s" % (written, len(line), path))
    finally:
        os.close(handle)                           # closing lets the lock go


def last_byte(path, size):
    reader = os.open(str(path), os.O_RDONLY)
    try:
        return os.pread(reader, 1, size - 1)
    finally:
        os.close(reader)


def add(kind, subject, fields, note="", at=None, data=None, member=None):
    """Append one observation to the caller's division's record; the row written. ValueError (one plain line) on a broken
    rule, and then nothing is written."""
    row, line = make_row(kind, subject, fields, note, at, member)
    append(record(data or division.DATA, row["division"]), line)
    return row


# ---- reading the records back

def read_record(path):
    """(rows oldest first, lines not readable) of one record: whole lines only, a line being written is left for later."""
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return [], 0
    rows, bad = [], 0
    for number, piece in enumerate(raw[:raw.rfind(b"\n") + 1].split(b"\n")):
        if not piece.strip():
            continue
        try:
            row = json.loads(piece.decode("ascii"))
            t = calendar.timegm(time.strptime(row["t"][:19], "%Y-%m-%dT%H:%M:%S"))
            if not isinstance(row.get("kind"), str) or not isinstance(row.get("subject"), str) or not isinstance(row.get("fields", {}), dict):
                raise ValueError("not an observation")
        except (ValueError, TypeError, KeyError, AttributeError, UnicodeDecodeError):
            bad += 1
            continue
        rows.append((t, number, row))
    return [row for _t, _n, row in sorted(rows, key=lambda r: (r[0], r[1]))], bad


def chosen(word, env=None):
    """The divisions a --division word names: one, or all six; ValueError for a word that names none."""
    if word in (None, ""):
        kind, name = division.member(env)
        return [DIVISIONS[name]] if kind == "member" else sorted(DIVISIONS.values())
    if str(word).lower() == "all":
        return sorted(DIVISIONS.values())
    found = division_of(word)
    if not found:
        raise ValueError("refused: --division `%s` names no division: %s or all" % (word, ", ".join(sorted(DIVISIONS.values()))))
    return [found]


def gather(data, names):
    rows, bad = [], 0
    for name in names:
        found, broken = read_record(record(data, name))
        rows += found
        bad += broken
    return sorted(rows, key=lambda r: r["t"]), bad


def rows(data=None, which=None):
    """The readable rows of one division's record (a division's or a member's name; None: of all six), oldest first."""
    return gather(data or division.DATA, chosen(which or "all"))[0]


def shown(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str) and value and not re.search(r"[\s=\"]", value):
        return value
    return json.dumps(value)


def show(data, kind=None, subject=None, word=None, last=20):
    names = chosen(word)
    found, bad = gather(data, names)
    picked = [r for r in found if (not kind or r.get("kind") == kind) and (not subject or subject.lower() in str(r.get("subject")).lower())]
    tail = picked[-last:] if last > 0 else []
    where = "all" if len(names) > 1 else names[0]
    print("OBSERVE show | %s%s%s | %d of %d rows, oldest first (--last %d)%s | %s" % (
        where, " | kind " + kind if kind else "", " | subject holds `%s`" % subject if subject else "", len(tail), len(picked), last,
        " | %d lines not readable" % bad if bad else "", Path(data) / FOLDER))
    if not tail:
        print("  no observation on record%s; write one: observe.py add <kind> <subject> key=value ... [--note \"...\"]" % (" that matches" if found else ""))
    for r in tail:
        fields = " ".join("%s=%s" % (k, shown(v)) for k, v in (r.get("fields") or {}).items())
        print("  %s  %-9s %-8s %-16s %s%s%s" % (r.get("t"), r.get("division"), r.get("member"), r.get("kind"), r.get("subject"),
                                             "  " + fields if fields else "", "  -- " + r["note"] if r.get("note") else ""))
    return 0


def kinds(data, word=None):
    names = chosen(word)
    found, bad = gather(data, names)
    table = {}
    for r in found:
        entry = table.setdefault((r.get("division"), r.get("kind")), {"rows": 0, "newest": "", "fields": set()})
        entry["rows"] += 1
        entry["newest"] = max(entry["newest"], str(r.get("t")))
        entry["fields"] |= set(r.get("fields") or {})
    where = "all" if len(names) > 1 else names[0]
    print("OBSERVE kinds | %s | %d kinds, %d rows%s | look here before you name a new kind: one name per kind of thing" % (
        where, len(table), len(found), " | %d lines not readable" % bad if bad else ""))
    if not table:
        print("  no observation on record")
        return 0
    print("  %-10s %-24s %5s  %-20s  %s" % ("division", "kind", "rows", "newest", "fields"))
    for (name, kind), entry in sorted(table.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        print("  %-10s %-24s %5d  %-20s  %s" % (name, kind, entry["rows"], entry["newest"], ", ".join(sorted(entry["fields"])) or "--"))
    return 0


# ---- the command line

OPTIONS = ("--note", "--at", "--data", "--division", "--subject", "--last")


def parse(argv):
    """(words, options) of the command line; ValueError for an option without its value or one this script has not."""
    words, options, n = [], {}, 0
    while n < len(argv):
        arg = argv[n]
        if arg in OPTIONS:
            if n + 1 >= len(argv) or argv[n + 1] in OPTIONS:
                raise ValueError("refused: %s takes a value" % arg)
            options[arg[2:]] = argv[n + 1]
            n += 2
            continue
        if arg.startswith("--"):
            raise ValueError("refused: no option %s here: %s" % (arg, ", ".join(OPTIONS)))
        words.append(arg)
        n += 1
    return words, options


def main(argv):
    try:
        words, options = parse(argv)
        data = options.get("data") or division.DATA
        verb = words[0] if words else ""
        if verb == "add":
            if len(words) < 3:
                raise ValueError("refused: add takes <kind> <subject> [key=value ...]")
            fields = {}
            for pair in words[3:]:
                key, equal, text = pair.partition("=")
                if not equal:
                    raise ValueError("refused: `%s` is no key=value" % pair)
                if key in fields:
                    raise ValueError("refused: field `%s` is given twice" % key)
                fields[key] = value_of(text)
            if options.get("division") is not None:
                name, own = writer()
                if division_of(options["division"]) != own:
                    raise ValueError("refused: %s writes the %s record only (observations/%s.jsonl), not `%s`" % (name, own, own, options["division"]))
            row = add(words[1], words[2], fields, note=options.get("note", ""), at=options.get("at"), data=data)
            print("observe: added to %s: %s %s %s at %s" % (record(data, row["division"]), row["member"], row["kind"], row["subject"], row["t"]))
            return 0
        if verb == "show":
            try:
                last = int(options.get("last", "20"))
            except ValueError:
                raise ValueError("refused: --last takes a number, not `%s`" % options["last"]) from None
            return show(data, words[1] if len(words) > 1 else None, options.get("subject"), options.get("division"), last)
        if verb == "kinds":
            return kinds(data, options.get("division"))
    except ValueError as error:
        print("observe: %s" % error)
        return 1
    print(__doc__)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
