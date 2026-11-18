#!/usr/bin/env python3
"""docs_handbook.py -- the reader of the store's handbook (game/handbook.md and game/handbook/<subject>.md, written from the code by scripts/handbook.py): its contents and how the data flows, or the sections of one topic: a table or view, a subject, or a word.

WHAT: `hive.py handbook [<topic>]` and the MCP tool docs (view=handbook, topic) print it. It reads the handbook's
      sections from the store's read copy (the table docs, kind `handbook`, which docs.py fills from the files at
      every pass); while the store holds none yet (its first pass after the files came), the files themselves,
      parsed the same way (docs.parse), and the answer says so:
        no topic        the head of game/handbook.md, its contents and how the data flows
        a topic         the sections it names, each whole: a table's or a view's section (route_earnings), a
                        subject's file with its lines of Where to ask what (money, Map and intel), a section's id or
                        title (where-to-ask-what, the-figures); else every section whose title or text holds all its
                        words
RULES:
  - It reads only. An answer prints at most docs.TEXT_CHARS characters of text; the sections beyond are listed by id.
  - One parser: docs.py's (docs.parse, docs.slug), so the store's rows and the files give the same sections.
WHY:  Suggi, 2026-11-18: a handbook of how the database works, kept current by itself. A member reads the part it
      needs, never the whole handbook.

USAGE:
  docs_handbook.py [<topic>] [--data <dir>] [--root <dir>]
  --data <dir>   the unit's data folder (default: the fleet's)
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import os
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the data folder's default
import docs as writings                           # noqa: E402  the parser, the read copy, the text budget

KIND = "handbook"              # its kind in the table docs (docs.KINDS)
MASTER = "game/handbook.md"
FOLDER = "game/handbook"
FIRST = ("top", "contents", "how-the-data-flows")      # what an answer without a topic shows, of game/handbook.md


def from_store(data):
    """[(path, section, title, text)] of the handbook in the store's read copy, in file order; [] when it holds none."""
    conn, _why = writings.open_copy(data)
    if conn is None:
        return []
    try:
        return conn.execute("SELECT path, section, title, text FROM docs WHERE kind = ? ORDER BY path, n", (KIND,)).fetchall()
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def from_files(root):
    """The same rows parsed from the files themselves (docs.parse), for the time before the store holds them."""
    repo = Path(root).resolve().parent
    paths = [repo / MASTER] + sorted((repo / FOLDER).glob("*.md"))
    rows = []
    for path in paths:
        if path.is_file():
            rel = path.relative_to(repo).as_posix()
            rows += [(rel, sid, title, text) for sid, title, text in writings.parse(str(path), KIND)]
    return rows


def pick(rows, topic):
    """(the rows a topic names, how they matched): none, the head, the contents and how the data flows; else the
    sections whose id is the topic's slug, ends with it or lies under it, and the subject file it names; else a title;
    else words."""
    if not topic.strip():
        return [r for r in rows if r[0] == MASTER and r[1] in FIRST], "the head, the contents and how the data flows"
    want, low = writings.slug(topic), " ".join(topic.lower().split())
    named = [r for r in rows if r[1] == want or r[1].endswith("/" + want) or r[1].startswith(want + "/")]
    named += [r for r in rows if r[0] != MASTER and Path(r[0]).stem == want and r not in named]
    if named:
        return named, "by name"
    titled = [r for r in rows if " ".join((r[2] or "").lower().split()) == low]
    if titled:
        return titled, "by title"
    words = low.split()
    return [r for r in rows if all(w in ("%s\n%s" % (r[2] or "", r[3] or "")).lower() for w in words)], "the sections that hold `%s`" % topic


def show(root, data, now, topic):
    """hive.py handbook [<topic>]: the sections a topic names, whole, up to docs.TEXT_CHARS characters."""
    rows = from_store(data)
    source = writings.copy_line(data, now)
    if not rows:
        rows = from_files(root)
        source = "read from the files: the store holds no handbook yet (it mirrors them at its next pass)"
    if not rows:
        print("HANDBOOK | no handbook: neither the store nor %s holds one; write it with `python3 -I -B scripts/handbook.py`" % MASTER)
        return 1
    picked, how = pick(rows, topic or "")
    if not picked:
        print("HANDBOOK | nothing matches `%s`: name a table or view (`hive.py schema` lists them), a subject (the contents: "
              "`hive.py handbook`) or a word | %s" % (topic, source))
        return 1
    print("HANDBOOK%s | %d section%s, %s | the store's handbook, written from the code by scripts/handbook.py (table docs, kind handbook) | %s"
          % (" " + topic if topic else "", len(picked), "" if len(picked) == 1 else "s", how, source))
    budget, rest = writings.TEXT_CHARS, []
    for path, section, title, text in picked:
        if len(text or "") + 100 > budget:
            rest.append((path, section, title))
            continue
        budget -= len(text or "") + 100
        print("=== %s %s" % (path, section))
        print(text or "")
    if rest:
        print("... %d more sections, over %s characters (one: hive.py handbook <id>):" % (len(rest), writings.num(writings.TEXT_CHARS)))
        for path, section, title in rest:
            print("  %-36s %-40s %s" % (path, section, (title or "")[:60]))
    print("  the contents: hive.py handbook; one table or view: hive.py handbook <name>; a subject: hive.py handbook money; "
          "a word: hive.py handbook <word>; its versions: hive.py docs %s --section <id> --history" % (picked[0][0]))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    here = Path(__file__).resolve().parent
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data"))]
    return show(value("--root", str(here.parent)), value("--data", division.DATA), time.time(), " ".join(words))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
