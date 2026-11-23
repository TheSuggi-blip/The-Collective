#!/usr/bin/env python3
"""guidebook.py -- the divisions' guidebooks as capped chapters of small entries: their form and caps, one store section an entry, and the reader.

WHAT: each division keeps its guidebook as a folder game/routes/guidebook/<division>/ of chapter files (rule F14), and
      the Fleet Admiral hers as game/routes/guidebook/command/ (owner Command: how she leads, the design in force):
        card.md          the Class Card: how the class builds its ships and levels; read whole at every turn
        ships.md         hulls, fits, modules, the upgrade ladder
        levelling.md     which work trains which skill, in what order
        routes.md        the kinds of work of the class and how its routes are built and judged
        tests.md         open tests and their results
        lessons.md       findings, pitfalls, tactics
        topic-<name>.md  at most TOPICS of the division's own (logistics topic-bases.md, military topic-pirates.md,
                         command topic-design.md)
      A chapter is its title line `# ...` and a list of entries, each:
        ### <title>
        Status: proven|test|retired. Updated: YYYY-MM-DD. [Id: <slug>.] Evidence: <route ids, the hive.py call of each
        figure, reports>.
        <what to do and why>
      This module is the reading side; docs.py (the store's mirror), hive.py, docs_division.py and the MCP server
      import it:
        parse(text)              one chapter -> its title, its head and its entries (title, status, updated, id,
                                 evidence, text: the status line and the body, line)
        sections(text, chapter)  the store's sections of one chapter (docs.py, kind `guide`, owner the division): one
                                 an entry, its id the entry's `Id:` or the slug of its title, its title
                                 `[<chapter> <status> <updated>] <title>`, its text the entry's text; the head below the
                                 title line, when there is one, as `_head`. Every version stays in doc_versions
        hive.py guide            a division: its card whole, the index of every chapter (entries: status, updated,
                                 characters, id) and the class's computed figures from stats.py's tables (XP per
                                 ship-hour of its roles' skills, the top routes of its own class by XP per ship-hour,
                                 its ships' next tiers and empty slots); all: one block a division. --chapter: one
                                 chapter whole; --grep: the entries that hold a word; --retired: the entries retired
                                 or gone from their chapter, kept in the store
        briefing(...)            the briefing's part: the member's own card whole and every chapter or entry of its
                                 division over its cap (Unity: her card, and every division's over-cap list)
        division_part(...)       the GUIDEBOOK line of `hive.py division` (docs_division.py)
        mcp_view(tools, arg)     the tool docs gains view=guide with the arguments chapter and retired (no new tool)
      The writing side is scripts/guide.py: check (the gate), sizes, split (an old guidebook into chapters), tidy.
RULES:
  - The caps and the chapter names stand here only (CARD_MAX, CHAPTER_MAX, ENTRY_MAX, HEAD_MAX, CHAPTERS_MAX,
    TOPICS, CHAPTERS). A chapter's characters are the sum of its entries' texts (status line and body; the headings
    not counted), the same number as the store's column chars of its sections. Over a cap nothing is cut by a script:
    the gate HALTs and the briefing names what its Admiral refines (merge entries, retire what is outdated).
  - An entry's key in the store is its chapter's path and its id. A renamed title is a new entry, unless its status
    line keeps the old id (`Id: <old slug>.`): then its versions go on under the old key. An entry moved to another
    chapter is a new key; the old one keeps its versions.
  - Numbers come from the store: an entry names the call that shows a figure (`hive.py stats xp --member Zero`,
    `hive.py route <id>`); the reader prints the class's computed figures beside the card, never into a chapter.
    What no table holds is printed `not measured`.
  - It reads only: the chapter files are written by their Admiral and by scripts/guide.py.
WHY:  Suggi, 2026-11-18: "The guidebooks are bloating, but they are good. We need a system where the data collected in
      the guidebooks gets to the database so it is saved there and can evolve and grow and change over time and adapt.
      But it all has to be capped." Five files of 32,000 to 83,000 characters, each a mix of card, plan, route
      guides, tests and long histories, were read whole at every turn and their numbers went stale.

USAGE:
  hive.py guide [<division>|<member>|all] [--chapter <name>] [--grep <word>] [--retired]
  guidebook.py parse <chapter file>     the sections of one chapter as the store loads them: id, characters, title
  --data <dir>   the unit's data folder (default /srv/collective/data)
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names
import division                                   # noqa: E402  the members, their roles

FOLDER = "game/routes/guidebook"                  # the guidebooks, one folder a division, in the repository
DIVISIONS = tuple(name.lower() for name in board.NAMES.values())    # mining, trade, logistics, military, intel, command (Unity's)
CHAPTERS = ("card", "ships", "levelling", "routes", "tests", "lessons")      # the fixed chapters, in their reading order
TOPIC = re.compile(r"^topic-[a-z0-9]+(?:-[a-z0-9]+)*$")                       # a division's own chapter: topic-<name>.md
TOPICS = 2                     # topic chapters a division keeps at most
CHAPTERS_MAX = 8               # chapter files a division keeps at most (the six fixed and TOPICS)
CARD_MAX = 4500                # characters of card.md's entries: read whole at every turn
CHAPTER_MAX = 12000             # characters of the entries of every other chapter
ENTRY_MAX = 2250               # characters of one entry (its status line and its body); aim at about 1,800
HEAD_MAX = 450                 # characters a chapter may hold between its title line and its first entry
HIGH_WATERMARK = 0.90          # soft curation trigger (90% of cap): merge or mark outdated entries retired before overflow
STATUSES = ("proven", "test", "retired")
NAMES = {"card": "the Class Card", "ships": "Ships and Fits", "levelling": "Levelling", "routes": "Routes",
         "tests": "Tests", "lessons": "Lessons"}                                # a chapter's title, after its division's name
HEAD = "_head"                 # the store's section id of a chapter's head (a title's slug never starts with `_`)
TEXT_CHARS = 25000             # characters of entry text the reader prints at most (an MCP answer is cut at 30,000)
FIGURE_ROWS = 5                # rows of each computed figure beside the card
STATUS_LINE = re.compile(r"^Status: ([a-z]+)\. Updated: (\d{4}-\d{2}-\d{2})\.(?: Id: ([a-z0-9]+(?:-[a-z0-9]+)*)\.)? Evidence: (\S.*)$")
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE = re.compile(r"^[ \t]*(```|~~~)")
STORE_TITLE = re.compile(r"^\[([a-z0-9-]+) (\S+) (\S+)\] (.*)$", re.S)


# ---- one chapter: its form

def cap_of(chapter):
    """The characters a chapter's entries may hold."""
    return CARD_MAX if chapter == "card" else CHAPTER_MAX


def chapter_ok(name):
    """True for a chapter's name (the file's stem): one of CHAPTERS or topic-<name>."""
    return name in CHAPTERS or bool(TOPIC.match(name))


def chapter_rank(name):
    return (CHAPTERS.index(name), "") if name in CHAPTERS else (len(CHAPTERS), name)


def title_line(division_name, chapter):
    """The title line split.py writes at a chapter's top."""
    words = NAMES.get(chapter) or "Topic: " + chapter[len("topic-"):].replace("-", " ")
    return "# %s guidebook -- %s (%s.md)" % (division_name.capitalize(), words, chapter)


def parse(text):
    """One chapter's text -> {'title': its `# ` line's words, 'head': [lines between the title and the first entry],
    'entries': [entry], 'stray': [(line number, line)]: a heading of level 1 or 2 below the title (the gate refuses
    it; its line stays in the text where it stands)}. An entry: {'title', 'line' (its heading's), 'status', 'updated',
    'id', 'evidence' (None when its first line is no status line of the form), 'status_line', 'text' (the status line
    and the body, blank lines at both ends taken off), 'body'}. A fenced block is never split."""
    out, current, fence = {"title": "", "head": [], "entries": [], "stray": []}, None, False
    for n, line in enumerate(text.splitlines(), 1):
        heading = None
        if FENCE.match(line):
            fence = not fence
        elif not fence:
            heading = HEADING.match(line)
        if heading and len(heading.group(1)) == 3:
            current = {"title": heading.group(2).strip(), "line": n, "lines": []}
            out["entries"].append(current)
            continue
        if heading and len(heading.group(1)) == 1 and current is None and not out["title"] and not any(x.strip() for x in out["head"]):
            out["title"] = heading.group(2).strip()
            continue
        if heading and len(heading.group(1)) <= 2:
            out["stray"].append((n, line))
        (current["lines"] if current is not None else out["head"]).append(line)
    for entry in out["entries"]:
        lines = entry.pop("lines")
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        first = lines[0] if lines else ""
        found = STATUS_LINE.match(first)
        entry.update(status_line=first, status=found.group(1) if found else None, updated=found.group(2) if found else None,
                     id=found.group(3) if found else None, evidence=found.group(4) if found else None, text="\n".join(lines))
        body = lines[1:] if found else lines
        while body and not body[0].strip():
            body = body[1:]
        entry["body"] = "\n".join(body)
    while out["head"] and not out["head"][0].strip():
        out["head"].pop(0)
    while out["head"] and not out["head"][-1].strip():
        out["head"].pop()
    return out


def loose_status(entry):
    """The status word of an entry whose status line does not have the form: what follows `Status:`, else None."""
    found = re.match(r"^Status:\s*([A-Za-z]+)", entry.get("status_line") or "")
    return found.group(1).lower() if found else None


def entry_id(entry):
    """An entry's id: its `Id:` when its status line names one, else the slug of its title (docs.py's slug)."""
    import docs                                   # docs.py imports this module inside its parse: imported here, not above
    return entry.get("id") or docs.slug(entry["title"])


def store_title(chapter, entry):
    """The title an entry stands under in the store: `[<chapter> <status> <updated>] <title>` (`?` for a part its
    status line lacks)."""
    status = entry.get("status") or loose_status(entry) or "?"
    return "[%s %s %s] %s" % (chapter, status, entry.get("updated") or "?", entry["title"])


def read_title(title):
    """(chapter, status, updated, title) of a store title; ('', '', '', title) for any other."""
    found = STORE_TITLE.match(title or "")
    return found.groups() if found else ("", "", "", title or "")


def sections(text, chapter):
    """[(section id, title, text)] of one chapter as the store loads it (docs.py, kind `guide`): the head below the
    title line when there is one (`_head`), then one section an entry; a second entry with one id is `<id>-2` (the
    gate refuses it)."""
    found = parse(text)
    out, seen = [], {}
    head = "\n".join(found["head"])
    if head.strip():
        out.append((HEAD, "[%s head] %s" % (chapter, found["title"] or "(no title line)"), head))
    for entry in found["entries"]:
        sid = entry_id(entry)
        seen[sid] = seen.get(sid, 0) + 1
        out.append((sid if seen[sid] == 1 else "%s-%d" % (sid, seen[sid]), store_title(chapter, entry), entry["text"]))
    return out


def place(path):
    """(division, chapter) of a chapter's repository path game/routes/guidebook/<division>/<chapter>.md; ('', '') else."""
    parts = str(path).replace(os.sep, "/").split("/")
    if len(parts) >= 2 and "/".join(parts[:-2]).endswith(FOLDER) and parts[-1].endswith(".md"):
        return parts[-2], parts[-1][:-3]
    return "", ""


# ---- the readers (the store's read copy only)

def num(n):
    return format(int(n), ",") if isinstance(n, (int, float)) else "--"


def which(word):
    """A division's folder name for a member's or a division's name (any case); 'all' for all; None for anything else."""
    low = str(word or "").strip().lower()
    if low in ("", "all"):
        return "all"
    if low in DIVISIONS:
        return low
    member = next((m for m in division.MEMBERS if m.lower() == low), None)
    name = board.NAMES.get(member, "").lower() if member else ""
    return name if name in DIVISIONS else None


def member_of(name):
    """The member whose division a folder name is."""
    return next((m for m, n in board.NAMES.items() if n.lower() == name), "")


def store_rows(conn):
    """{division: {chapter: [row]}} of every chapter section that stands in the table docs; a row: {path, section,
    n, title (the entry's own), status, updated, chars, t}. The chapters in reading order."""
    out = {}
    for path, section, n, title, chars, t in conn.execute("SELECT path, section, n, title, chars, t FROM docs WHERE kind = 'guide' ORDER BY path, n"):
        name, chapter = place(path)
        if not name:
            continue
        _chapter, status, updated, plain = read_title(title)
        out.setdefault(name, {}).setdefault(chapter, []).append({"path": path, "section": section, "n": n, "title": plain, "status": status,
                                                                  "updated": updated, "chars": chars or 0, "t": t})
    return {name: dict(sorted(chapters.items(), key=lambda kv: chapter_rank(kv[0]))) for name, chapters in out.items()}


def entries_of(rows):
    """The rows of a chapter that are entries (its head left out)."""
    return [r for r in rows if r["section"] != HEAD]


def chapter_chars(rows):
    return sum(r["chars"] for r in entries_of(rows))


def over_caps(chapters):
    """[(chapter, what, chars, cap)] of one division: each chapter over its cap, a division over CHAPTERS_MAX
    chapters or TOPICS topics, each entry over ENTRY_MAX, each head over HEAD_MAX."""
    out = []
    if len(chapters) > CHAPTERS_MAX:
        out.append(("", "%d chapters" % len(chapters), len(chapters), CHAPTERS_MAX))
    topics = [c for c in chapters if c not in CHAPTERS]
    if len(topics) > TOPICS:
        out.append(("", "%d topic chapters (%s)" % (len(topics), ", ".join(topics)), len(topics), TOPICS))
    for chapter, rows in chapters.items():
        size = chapter_chars(rows)
        if size > cap_of(chapter):
            out.append((chapter, "the chapter", size, cap_of(chapter)))
        for r in rows:
            if r["section"] == HEAD and r["chars"] > HEAD_MAX:
                out.append((chapter, "its head", r["chars"], HEAD_MAX))
            elif r["section"] != HEAD and r["chars"] > ENTRY_MAX:
                out.append((chapter, "entry `%s`" % r["section"], r["chars"], ENTRY_MAX))
    return out


def over_lines(name, chapters, most=12):
    """The lines that tell a division's Admiral what to refine."""
    found = over_caps(chapters)
    if not found:
        return []
    whole = [x for x in found if x[1] == "the chapter" or not x[0]]
    parts = [x for x in found if x not in whole]
    out = ["  OVER ITS CAP, %s: refine at this turn (merge entries, retire what is outdated, then `python3 -B scripts/guide.py tidy %s`); "
           "a script never cuts it" % (name.capitalize(), name)]
    for chapter, what, size, cap in whole:
        out.append("    %s%s %s of %s" % ((chapter + ".md: ") if chapter else "", what, num(size), num(cap)))
    by_chapter = Counter(chapter for chapter, _what, _size, _cap in parts)
    if parts:
        out.append("    over their own cap: %s" % ", ".join("%s.md %d" % (c, n) for c, n in by_chapter.items()))
        for chapter, what, size, cap in sorted(parts, key=lambda x: -x[2])[:max(0, most - len(out))]:
            out.append("      %s.md %s %s of %s" % (chapter, what, num(size), num(cap)))
    return out


def near_caps(chapters):
    """[(chapter, size, cap, pct)] for chapters at >= HIGH_WATERMARK (90%) up to 100% of their cap."""
    out = []
    for chapter, rows in chapters.items():
        cap = cap_of(chapter)
        size = chapter_chars(rows)
        if int(cap * HIGH_WATERMARK) <= size <= cap:
            out.append((chapter, size, cap, round(100.0 * size / cap, 1)))
    return out


def near_lines(name, chapters):
    """Soft high-watermark curation notice before a chapter hits its hard gate."""
    found = near_caps(chapters)
    if not found:
        return []
    return [
        "  NEAR ITS CAP (>= 90%%), %s: curate proactively (merge overlapping rules or mark superseded entries `Status: retired` for hourly tidy): %s"
        % (name.capitalize(), ", ".join("%s.md %s/%s (%.0f%%)" % (c, num(s), num(cap), pct) for c, s, cap, pct in found))
    ]


def text_of(conn, path, section):
    row = conn.execute("SELECT text FROM docs WHERE path = ? AND section = ?", (path, section)).fetchone()
    return (row[0] if row else "") or ""


def print_entry(conn, row):
    print("### %s" % row["title"])
    print(text_of(conn, row["path"], row["section"]))


def class_figures(conn, root, data, name):
    """The computed figures of a division's class, from stats.py's tables (stats_figures, views xp and upgrades): XP
    per ship-hour of its roles' skills, the top routes of its own class by XP per ship-hour, its ships' next tier and
    empty slots. Each line names its window, its n and its call; what no row holds is `not measured`."""
    import stats
    member = member_of(name)
    roles = [r for r, m in division.ROLES.items() if m == member]
    call = "hive.py stats xp --member %s; hive.py stats upgrades --member %s" % (member, member)
    if not stats.has_table(conn, "stats_figures"):
        return ["  not measured: the store's read copy holds no table of stats.py yet (%s)" % call]
    out = []
    rows, at = stats.figures(conn, "xp")
    key = ("xp_per_ship_hour", 24.0)
    skills = sorted(((s.split("|", 1)[0], s.split("|", 1)[1], r[key]) for s, r in rows.items() if "|" in s and s.split("|", 1)[0] in roles and key in r),
                    key=lambda x: -(x[2][0] or 0))
    out.append("  XP per ship-hour of its roles' skills (24 h, n = pilots that gained; computed %s): %s" % (
        stats.stamp(at) if at else "--", "; ".join("%s %s %s n %d" % (role, skill, "%.1f" % v if v is not None else "not measured", n or 0)
                                                   for role, skill, (v, n, _t) in skills[:FIGURE_ROWS * 2]) or "not measured"))
    import workclass
    routes = workclass.load(root)
    key = ("route_xp_per_ship_hour", 24.0)
    own = sorted(((rid, r[key]) for rid, r in rows.items() if key in r and rid in routes
                  and workclass.work_class(routes[rid], rid) not in workclass.SHARED and any(workclass.own(role, routes[rid], rid) for role in roles)),
                 key=lambda x: -(x[1][0] or 0))
    out.append("  Top routes of its own class by XP per ship-hour (24 h, all skills, n = pilot readings): %s" % (
        "; ".join("%s %s n %d" % (rid, "%.1f" % v if v is not None else "not measured", n or 0) for rid, (v, n, _t) in own[:FIGURE_ROWS]) or "not measured"))
    rows, at = stats.figures(conn, "upgrades")
    mine = {p: r for p, r in rows.items() if stats.role_of(p, data) in roles}
    if not mine:
        out.append("  Next upgrades: not measured: no ship of %s in the view upgrades (computed %s)" % (", ".join(roles), stats.stamp(at) if at else "--"))
    else:
        value = lambda r, figure: (r.get((figure, 0.0)) or (None,))[0]
        tiers = Counter(value(r, "tier") for r in mine.values())
        ready = sum(1 for r in mine.values() if value(r, "piloting") is not None and value(r, "piloting_next") not in (None, 0)
                    and value(r, "piloting") >= value(r, "piloting_next"))
        unknown = sum(1 for r in mine.values() if value(r, "piloting") is None or value(r, "piloting_next") is None)
        empty = Counter()
        for r in mine.values():
            for slot in ("weapon", "defense", "utility"):
                empty[slot] += value(r, "empty_" + slot) or 0
        out.append("  Next upgrades (%d ships, computed %s): tiers %s; Piloting reaches the next tier's hulls: %d ships (%d not measured); "
                   "empty slots: weapon %d, defense %d, utility %d" % (
                       len(mine), stats.stamp(at) if at else "--", ", ".join("%s: %d" % ("tier %s" % num(t) if t is not None else "not measured", n)
                                                                            for t, n in sorted(tiers.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))),
                       ready, unknown, empty["weapon"], empty["defense"], empty["utility"]))
    out.append("  whole: %s" % call)
    return out


def head_line(data, now):
    import docs
    return docs.copy_line(data, now)


def show_division(conn, root, data, now, name, chapters):
    path = "%s/%s/" % (FOLDER, name)
    total = sum(len(entries_of(rows)) for rows in chapters.values())
    print("GUIDE %s | %s | %d chapters, %d entries, %s characters | caps: card %s, a chapter %s, an entry %s, %d chapters (%d topics) | %s"
          % (name.capitalize(), path, len(chapters), total, num(sum(chapter_chars(rows) for rows in chapters.values())), num(CARD_MAX), num(CHAPTER_MAX),
             num(ENTRY_MAX), CHAPTERS_MAX, TOPICS, head_line(data, now)))
    card = chapters.get("card") or []
    print("=== THE CLASS CARD (%scard.md, %d entries, %s of %s characters; read whole at every turn)" % (path, len(entries_of(card)), num(chapter_chars(card)), num(CARD_MAX)))
    if not card:
        print("  not in the store: no %scard.md" % path)
    for row in entries_of(card):
        print_entry(conn, row)
    print("=== THE CHAPTERS (an entry: status, updated, characters, id; OVER = over its cap)")
    for chapter, rows in chapters.items():
        size = chapter_chars(rows)
        print("%s.md | %d entries, %s of %s characters%s" % (chapter, len(entries_of(rows)), num(size), num(cap_of(chapter)), "  OVER" if size > cap_of(chapter) else ""))
        if chapter == "card":
            continue
        for r in rows:
            if r["section"] == HEAD:
                print("  %-8s %-10s %6s  %-40s %s" % ("head", "", num(r["chars"]), "", "  OVER" if r["chars"] > HEAD_MAX else ""))
                continue
            print("  %-8s %-10s %6s  %-40s %s%s" % (r["status"], r["updated"], num(r["chars"]), r["section"][:40], r["title"][:70], "  OVER" if r["chars"] > ENTRY_MAX else ""))
    for line in over_lines(name, chapters):
        print(line)
    for line in near_lines(name, chapters):
        print(line)
    print("=== THE FIGURES OF THE CLASS (computed by the store, stats.py; an entry names the call, never the number)")
    for line in class_figures(conn, root, data, name):
        print(line)
    try:
        import playbook_anchor
        repo_root = str(Path(root).resolve().parent if Path(root).name == "game" else Path(root))
        anc = playbook_anchor.compute_division_anchor(conn, repo_root, data=data, division_name=name, now=now)
        print("=== LIVE DIVISION ANCHOR (auto-computed from read.db, catalog & logs; never copy volatile counts into chapters)")
        for line in playbook_anchor.anchor_lines(anc):
            print(line)
    except Exception:
        pass
    print("  a chapter whole: hive.py guide %s --chapter <name>; a word: --grep <word>; retired entries: --retired; an entry's versions: "
          "hive.py docs %s<chapter>.md --section <id> --history; the gate: python3 -B scripts/guide.py check %s" % (name, path, name))
    return 0


def show_all(conn, data, now, found):
    print("GUIDE all | the guidebooks, one block a division (command: the Fleet Admiral's) (a division: hive.py guide <division>) | caps: card %s, a chapter %s, an entry %s | %s"
          % (num(CARD_MAX), num(CHAPTER_MAX), num(ENTRY_MAX), head_line(data, now)))
    for name in DIVISIONS:
        chapters = found.get(name)
        if not chapters:
            print("%s | not in the store: no chapter of %s/%s/" % (name.capitalize(), FOLDER, name))
            continue
        statuses = Counter(r["status"] for rows in chapters.values() for r in entries_of(rows))
        print("%s | %d chapters, %d entries (%s), %s characters | %s" % (
            name.capitalize(), len(chapters), sum(statuses.values()), ", ".join("%s %d" % (s, statuses[s]) for s in sorted(statuses)),
            num(sum(chapter_chars(rows) for rows in chapters.values())),
            ", ".join("%s %s%s" % (c, num(chapter_chars(rows)), " OVER" if chapter_chars(rows) > cap_of(c) else "") for c, rows in chapters.items())))
        for line in over_lines(name, chapters, most=6):
            print(line)
    return 0


def show_entries(conn, data, now, label, rows, word=""):
    """Entries printed whole up to TEXT_CHARS; those over the budget listed by id."""
    budget, rest, shown = TEXT_CHARS, [], 0
    for r in rows:
        text = text_of(conn, r["path"], r["section"])
        if word and word not in (r["title"] + "\n" + text).lower():
            continue
        if len(text) + 200 > budget:
            rest.append(r)
            continue
        budget -= len(text) + 200
        shown += 1
        print("=== %s %s | %s %s | %s chars" % (r["path"], r["section"], r["status"], r["updated"], num(r["chars"])))
        print("### %s" % r["title"])
        print(text)
    if rest:
        print("... %d more entries (one: hive.py docs <path> --section <id>):" % len(rest))
        for r in rest:
            print("  %-48s %-40s %s" % (r["path"], r["section"][:40], r["title"][:60]))
    if not shown and not rest:
        print("  no entry %s" % label)
    return 0


def retired_rows(conn):
    """Every entry whose newest version is retired, or that left its chapter without being retired: [dict], from
    doc_versions (kept for good)."""
    pattern = FOLDER + "/%/%.md"
    rows = conn.execute(
        "SELECT v.path, v.section, v.title, LENGTH(v.text), v.first_seen, v.last_seen, d.section IS NOT NULL FROM doc_versions v "
        "LEFT JOIN docs d ON d.path = v.path AND d.section = v.section WHERE v.path LIKE ? AND v.version IN "
        "(SELECT MAX(version) FROM doc_versions WHERE path LIKE ? GROUP BY path, section) ORDER BY v.path, v.section", (pattern, pattern)).fetchall()
    out = []
    for path, section, title, chars, first, last, stands in rows:
        name, chapter = place(path)
        _c, status, updated, plain = read_title(title)
        if not name or section == HEAD or (stands and status != "retired"):
            continue
        out.append({"path": path, "division": name, "chapter": chapter, "section": section, "title": plain, "status": status, "updated": updated,
                    "chars": chars or 0, "first": first, "last": last, "stands": bool(stands)})
    return out


def show_retired(conn, data, now, name, word):
    found = [r for r in retired_rows(conn) if name == "all" or r["division"] == name]
    if word:
        found = [r for r in found if word in r["title"].lower() or word in (conn.execute(
            "SELECT text FROM doc_versions WHERE path = ? AND section = ? ORDER BY version DESC LIMIT 1", (r["path"], r["section"])).fetchone()[0] or "").lower()]
    print("GUIDE %s --retired | entries retired, or gone from their chapter, kept in the store for good (doc_versions)%s | %d entries | %s"
          % (name if name == "all" else name.capitalize(), ", holding `%s`" % word if word else "", len(found), head_line(data, now)))
    if found:
        print("  %-10s %-12s %-40s %-10s %-22s %s" % ("division", "chapter", "id", "updated", "state", "title"))
    for r in found:
        state = "retired, stands (tidy)" if r["stands"] else "retired, tidied" if r["status"] == "retired" else "gone, not retired"
        print("  %-10s %-12s %-40s %-10s %-22s %s" % (r["division"], r["chapter"], r["section"][:40], r["updated"], state, r["title"][:60]))
    print("  its text and every version: hive.py docs <path> --section <id> --history; the guidebooks before the split of 2026-11-18: "
          "hive.py docs guidebook/<division>.md (their sections stay in doc_versions)")
    if not found:
        print("  no entry %s" % ("holds `%s`" % word if word else "was retired or left its chapter yet"))
    return 0


def value_of(args, name):
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else ""


VALUED = ("--chapter", "--grep", "--data", "--root", "--hours", "--limit", "--group", "--kind", "--zone", "--item", "--top", "--section", "--since", "--member")


def hive(args, root, data, now):
    """hive.py guide: args as hive.py got them (the verb among them)."""
    import docs
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in VALUED)]
    rest = words[words.index("guide") + 1:] if "guide" in words else words
    if rest:
        name = which(rest[0])
    else:
        _kind, me = division.member()
        name = which(me) if me in division.MEMBERS else "all"
    if name is None:
        print("GUIDE | no division `%s`: %s, a member's name, or all" % (rest[0], ", ".join(DIVISIONS)))
        return 1
    chapter, word = value_of(args, "--chapter").lower().replace(".md", ""), value_of(args, "--grep").lower()
    conn, why = docs.open_copy(data)
    if conn is None:
        print("GUIDE | " + why)
        return 1
    try:
        if "--retired" in args:
            return show_retired(conn, data, now, name, word)
        found = store_rows(conn)
        if chapter or word:
            names = DIVISIONS if name == "all" else (name,)
            rows = [r for n in names for c, its in (found.get(n) or {}).items() if not chapter or c == chapter for r in entries_of(its)]
            label = "in %s%s" % ("every guidebook" if name == "all" else name.capitalize(), " --chapter " + chapter if chapter else "")
            if chapter and not rows:
                print("GUIDE %s | no chapter `%s` in the store: %s" % (name, chapter, ", ".join(sorted({c for n in names for c in (found.get(n) or {})},
                                                                                                    key=chapter_rank)) or "none"))
                return 1
            print("GUIDE %s | %d entries %s%s, printed whole up to %s characters | %s" % (
                name if name == "all" else name.capitalize(), len(rows), label, " holding `%s`" % word if word else "", num(TEXT_CHARS), head_line(data, now)))
            return show_entries(conn, data, now, "holds `%s`" % word if word else label, rows, word)
        if name == "all":
            return show_all(conn, data, now, found)
        if not found.get(name):
            print("GUIDE %s | not in the store: no chapter of %s/%s/ (before its split: hive.py docs guidebook/%s.md) | %s"
                  % (name.capitalize(), FOLDER, name, name, head_line(data, now)))
            return 1
        return show_division(conn, root, data, now, name, found[name])
    finally:
        conn.close()


def briefing(root, data, now, who):
    """The briefing's part (hive.py briefing): the member's own Class Card whole and what of its division stands over
    its cap; for Unity (command) and all, every division's over-cap list too."""
    import docs
    name = which(who) or "all"
    print("=== %s" % ("MY CLASS CARD (%s/%s/card.md, from the store; caps: card %s, a chapter %s, an entry %s characters)" % (FOLDER, name, num(CARD_MAX), num(CHAPTER_MAX), num(ENTRY_MAX))
                       if name != "all" else "THE GUIDEBOOKS' CAPS (every chapter or entry over its cap; a division: hive.py guide <division>)"))
    conn, why = docs.open_copy(data)
    if conn is None:
        print("  not read: " + why)
        return
    try:
        found = store_rows(conn)
        if name != "all":
            card = entries_of((found.get(name) or {}).get("card") or [])
            if not card:
                print("  not in the store: no %s/%s/card.md (before its split: hive.py docs guidebook/%s.md)" % (FOLDER, name, name))
            for row in card:
                print_entry(conn, row)
            lines = over_lines(name, found.get(name) or {})
            print("\n".join(lines) if lines else "  every chapter of %s within its cap" % name.capitalize())
            print("  the chapters: hive.py guide %s (the tool docs, view=guide)" % name)
            for nline in near_lines(name, found.get(name) or {}):
                print(nline)
            try:
                import playbook_anchor
                repo_root = str(Path(root).resolve().parent if Path(root).name == "game" else Path(root))
                if len(list((Path(repo_root) / "game" / "routes").glob("*.json"))) >= 5:
                    cur = playbook_anchor.scan_division_curation(repo_root, name, data=data, now=now)
                    if cur["drift_warnings"]:
                        print("  DRIFT CHECK (%d item(s) in %s guidebook -- re-verify or mark Status: retired):" % (len(cur["drift_warnings"]), name))
                        for w in cur["drift_warnings"][:4]:
                            print("    %s.md `%s`: %s" % (w["chapter"], w["entry"][:42], w["detail"]))
            except Exception:
                pass
            if name != "command":
                return
            print("=== THE GUIDEBOOKS' CAPS (every chapter or entry over its cap; a division: hive.py guide <division>)")
        lines = [line for n in DIVISIONS if n != name for line in over_lines(n, found.get(n) or {}, most=6)]
        print("\n".join(lines) if lines else "  every chapter within its cap")
    finally:
        conn.close()


def division_part(conn, name, clip=lambda text, size: text, cut=600):
    """The GUIDEBOOK line of `hive.py division` from the chapters in the store; [] when the store holds none."""
    chapters = store_rows(conn).get(str(name).lower())
    if not chapters:
        return []
    import docs
    since = dict(((p, s), t) for p, s, t in conn.execute("SELECT path, section, MAX(first_seen) FROM doc_versions WHERE path LIKE ? GROUP BY path, section",
                                                          ("%s/%s/%%" % (FOLDER, str(name).lower()),)))
    items = []
    for chapter, rows in chapters.items():
        size = chapter_chars(rows)
        changed = max((since.get((r["path"], r["section"])) or 0 for r in rows), default=0)
        items.append("%s %d/%s%s %s" % (chapter, len(entries_of(rows)), num(size), " OVER" if size > cap_of(chapter) else "",
                                        docs.stamp(changed)[5:16] if changed else "--"))
    total = sum(len(entries_of(rows)) for rows in chapters.values())
    return ["GUIDEBOOK (%s/%s/, %d chapters, %d entries, %s chars; a chapter: entries/chars, OVER its cap, last change; whole: hive.py guide %s)"
            % (FOLDER, str(name).lower(), len(chapters), total, num(sum(chapter_chars(rows) for rows in chapters.values())), str(name).lower()),
            "  " + clip(", ".join(items), cut)]


def mcp_view(tools, arg):
    """The view guide of the MCP tool docs (collective_mcp.py calls it once after its TOOLS): the view, its two
    arguments chapter and retired, its line in the tool's text, and its plan in front of the tool's own."""
    tool = tools["docs"]
    view = tool["args"]["view"]
    if "guide" in view.get("enum", []):
        return
    view.setdefault("enum", []).append("guide")
    view["description"] = view["description"].replace(" or division", ", division or guide")
    tool["args"]["chapter"] = arg("string", "for guide: one chapter printed whole (card, ships, levelling, routes, tests, lessons, topic-<name>)")
    tool["args"]["retired"] = arg("boolean", "for guide: the entries retired or gone from their chapter, kept in the store")
    for name in ("division", "grep"):
        if name in tool["args"]:
            tool["args"][name]["description"] += " (also for guide)"
    tool["text"] += (" view=guide: a division's guidebook (division: yours by default, or all): its class card whole, the index of its chapters "
                     "(entries with status, updated, size; over cap) and the class's computed figures; chapter: one chapter whole; grep: the entries "
                     "that hold a word; retired: the retired entries, kept in the store.")
    own = tool["plan"]

    def plan(a):
        if a.get("view") != "guide":
            return own(a)
        out = ["guide"] + ([str(a["division"])] if a.get("division") else [])
        out += ["--chapter", str(a["chapter"])] if a.get("chapter") else []
        out += ["--grep", str(a["grep"])] if a.get("grep") else []
        return [("game/fleet/hive.py", out + (["--retired"] if a.get("retired") else []))]
    tool["plan"] = plan


def main(argv):
    if len(argv) >= 2 and argv[0] == "parse":
        path = Path(argv[1])
        found = sections(path.read_text(encoding="ascii", errors="replace"), path.stem)
        print("PARSE %s | chapter %s | %d sections, %s chars" % (path, path.stem, len(found), num(sum(len(text) for _sid, _title, text in found))))
        for sid, title, text in found:
            print("  %-44s %7s  %s" % (sid, num(len(text)), title[:90]))
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
