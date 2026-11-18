#!/usr/bin/env python3
"""guide.py -- the guidebooks' chapters: the gate of their form and caps, their sizes, the split of an old guidebook into chapters, and the tidy step that takes retired entries out.

WHAT: each division keeps its guidebook as a folder game/routes/guidebook/<division>/ of chapter files, each a list
      of entries `### <title>` with a status line (game/fleet/guidebook.py: the form, the caps, the reader). This
      script is the writing side:
        check [<division>|all]   the gate: exit 1 on HALT (RULES below); one line a fault, then the count line
        sizes [<division>|all]   every chapter: its entries, its characters against its cap, its entries over theirs
        split <division>|all     an old guidebook game/routes/guidebook/<division>.md (or the file --source names, for
                                 one division: Unity's DESIGN.md for command) into its chapters, without a word of its
                                 content changed: its head (the text above its first `##` section) becomes the entry
                                 `How this guidebook is kept` (`About <source>`) of lessons.md; each `##` section becomes one or more
                                 entries (its text above its first `###`, then each `###`) in the chapter its title maps
                                 to (MAP, then OWN for the division's own, else lessons). A title loses its section
                                 number, which the status line keeps: `Status: proven. Updated: <the date of the last
                                 commit that touched the entry's lines (git blame)>. Evidence: migrated from
                                 guidebook/<division>.md (<source>) section <its number, else its title>.` The split is checked
                                 before a file is written (every line of the old text minus its headings stands, in
                                 its order, in the entries' bodies; else HALT and nothing written); then it writes the
                                 six chapters and its topics and removes the old file (the store keeps its versions;
                                 a --source file outside the guidebooks is left where it stands)
        tidy <division>|all      takes every entry whose status is retired out of its chapter, once the store's read
                                 copy holds that entry's text (doc_versions: the same path, id and sha); an entry the
                                 store has not read yet waits for the next pass and stays. It writes the chapter files
                                 only; their Admiral commits them
RULES (check):
  - game/routes/guidebook/ holds one folder a division (mining, trade, logistics, military, intel, command: the Fleet
    Admiral's) and nothing else
    but names that begin with an upper-case letter; an old <division>.md beside its folder is doubled, one without
    its folder is not split yet.
  - A division's folder holds the six chapters card, ships, levelling, routes, tests and lessons (.md), at most
    TOPICS chapters topic-<name>.md, at most CHAPTERS_MAX files, nothing else.
  - A chapter: its first line `# <title>`, at most HEAD_MAX characters before its first entry, no other `#` or `##`
    heading outside a fence; each entry `### <title>` with the status line right below it:
    `Status: proven|test|retired. Updated: YYYY-MM-DD. [Id: <slug>.] Evidence: <what it rests on>`, a real date and
    not a future one; ASCII only.
  - Caps (guidebook.py): an entry at most ENTRY_MAX characters (its status line and body), card.md at most CARD_MAX,
    every other chapter at most CHAPTER_MAX (the sum of its entries). Over a cap is never cut by a script: the gate
    HALTs and names the chapter its Admiral refines (merge entries, retire what is outdated, then tidy).
  - No two entries of a division share an id (the slug of the title, or its `Id:`), whatever their chapters.
WHY:  Suggi, 2026-11-18: "The guidebooks are bloating, but they are good ... But it all has to be capped." The store
      keeps every version of every entry (docs.py, kind guide), so a chapter can stay small: what is retired leaves
      the file and stays searchable (hive.py guide --retired), and no machine ever cuts knowledge.

USAGE:
  guide.py check [<division>|all]                  the gate: exit 1 on HALT
  guide.py sizes [<division>|all]                  the chapters' sizes against their caps
  guide.py split <division>|all [--source <file>] [--updated YYYY-MM-DD] [--git <repository>] [--dry-run]
                                                   the dates from `git blame` of <repository> (default --root) for the
                                                   file at its path there, else its path below --root, else its name; with
                                                   --updated one date for every entry (a file git does not hold)
  guide.py tidy <division>|all [--data <dir>] [--dry-run]
  --root <dir>   the repository (default: the parent of this file's folder)
  --data <dir>   the unit's data folder, for tidy's read of the store (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import argparse
import calendar
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "game" / "fleet"))
import docs                                       # noqa: E402  slug, sha, the store's read copy
import guidebook as book                          # noqa: E402  the form, the caps, the parser (one place)

DATA = "/srv/collective/data"
MAP = (("class card", "card"), ("ships and fits", "ships"), ("levelling guide", "levelling"), ("route guides", "routes"),
       ("route templates", "routes"), ("missions that pay once", "routes"), ("standing plan", "routes"), ("open tests", "tests"),
       ("tests flown", "tests"))         # a `##` section's title (its number off, lower case, its beginning) -> its chapter
OWN = {"logistics": (("the fleet's storage home", "topic-bases"), ("base building", "topic-bases"), ("the stations' list", "topic-station"),
                     ("the faction's plates and boards", "topic-station")),
       "military": (("pirates", "topic-pirates"),),
       "command": (("game facts that shape the fleet", "lessons"), ("what others' fleets taught", "lessons"), ("the design in force", "topic-design"),
                   ("what limits scale", "topic-systems"), ("the engine and the door", "topic-systems"), ("the work cycle", "topic-systems"))}
                                                        # a division's own map, before MAP (command: Unity's DESIGN.md, 2026-11-18); the rest goes to REST
REST = "lessons"
HEAD_TITLE = "How this guidebook is kept"               # the entry of an old guidebook's head (the text above its first section)
NUMBER = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(\S.*)$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class SplitError(Exception):
    """A split that would lose or change a line, or an old file the split cannot read: nothing is written."""


def folder(root):
    return Path(root) / book.FOLDER


def chapter_files(root, name):
    base = folder(root) / name
    return sorted(base.glob("*.md"), key=lambda p: book.chapter_rank(p.stem)) if base.is_dir() else []


def divisions(which):
    if which in (None, "", "all"):
        return list(book.DIVISIONS)
    name = book.which(which)
    if name in (None, "all"):
        sys.exit("guide.py: no division `%s`: %s or all" % (which, ", ".join(book.DIVISIONS)))
    return [name]


# ---- the gate

def check_chapter(path, chapter, today):
    """(errors, entries) of one chapter file: [str], [(id, title, line)]."""
    rel = "%s/%s/%s" % (book.FOLDER, path.parent.name, path.name)
    raw = path.read_bytes()
    errors, found = [], []
    bad = [n for n, line in enumerate(raw.split(b"\n"), 1) if any(b > 127 for b in line)]
    if bad:
        errors.append("%s: not ASCII at line %s" % (rel, ", ".join(str(n) for n in bad[:5])))
    text = raw.decode("ascii", errors="replace")
    parsed = book.parse(text)
    first = next((line for line in text.splitlines() if line.strip()), "")
    if not first.startswith("# ") or not parsed["title"]:
        errors.append("%s: its first line is no title `# <title>`" % rel)
    for n, line in parsed["stray"]:
        errors.append("%s:%d: a heading `%s` in a chapter: an entry is `### <title>`, only the first line is `# `" % (rel, n, line[:60]))
    head = "\n".join(parsed["head"])
    if len(head) > book.HEAD_MAX:
        errors.append("%s: %s characters between its title and its first entry, over %s: move them into an entry" % (rel, docs.num(len(head)), docs.num(book.HEAD_MAX)))
    size = 0
    for entry in parsed["entries"]:
        where = "%s:%d `%s`" % (rel, entry["line"], entry["title"][:60])
        size += len(entry["text"])
        if entry["evidence"] is None:
            errors.append("%s: the line below the title is no status line `Status: proven|test|retired. Updated: YYYY-MM-DD. [Id: <slug>.] Evidence: ...` "
                          "(it reads `%s`)" % (where, entry["status_line"][:70]))
        else:
            if entry["status"] not in book.STATUSES:
                errors.append("%s: status `%s` is none of %s" % (where, entry["status"], ", ".join(book.STATUSES)))
            try:
                stamp = calendar.timegm(time.strptime(entry["updated"], "%Y-%m-%d"))
                if stamp > today + 86400:
                    errors.append("%s: Updated %s lies in the future" % (where, entry["updated"]))
            except ValueError:
                errors.append("%s: Updated %s is no date" % (where, entry["updated"]))
        if len(entry["text"]) > book.ENTRY_MAX:
            errors.append("%s: %s characters, over the entry's cap of %s: refine it (say what to do and why; name the call of each figure)"
                          % (where, docs.num(len(entry["text"])), docs.num(book.ENTRY_MAX)))
        found.append((book.entry_id(entry), entry["title"], "%s:%d" % (rel, entry["line"])))
    if size > book.cap_of(chapter):
        errors.append("%s: %s characters in %d entries, over its cap of %s: refine it (merge entries, retire what is outdated, then tidy)"
                      % (rel, docs.num(size), len(parsed["entries"]), docs.num(book.cap_of(chapter))))
    return errors, found


def check(root, which, now=None):
    """([errors], [warnings], chapters read, entries read) of the guidebooks of one division or all."""
    base, names = folder(root), divisions(which)
    errors, warnings, chapters, entries = [], [], 0, 0
    today = int(now if now is not None else time.time())
    if base.is_dir() and which in (None, "", "all"):
        for path in sorted(base.iterdir()):
            if path.name.startswith(".") or path.name[:1].isupper():
                continue
            if path.is_dir() and path.name not in book.DIVISIONS:
                errors.append("%s/%s/: no division's folder (%s)" % (book.FOLDER, path.name, ", ".join(book.DIVISIONS)))
            elif path.is_file() and not (path.suffix == ".md" and path.stem in book.DIVISIONS):
                errors.append("%s/%s: no guidebook file: a division's knowledge lies in its folder's chapters" % (book.FOLDER, path.name))
    for name in names:
        old, own = base / (name + ".md"), base / name
        if old.is_file():
            errors.append("%s/%s.md: %s" % (book.FOLDER, name, "stands beside its chapters, so its text stands twice: remove it" if own.is_dir() else
                                                "not split into chapters yet: python3 -B scripts/guide.py split %s" % name))
        if not own.is_dir():
            if not old.is_file():
                errors.append("%s/%s/: missing: every division keeps its guidebook (rule F14)" % (book.FOLDER, name))
            continue
        files = [p for p in sorted(own.iterdir()) if not p.name.startswith(".")]
        topics = []
        for path in files:
            if path.is_dir() or path.suffix != ".md" or not book.chapter_ok(path.stem):
                errors.append("%s/%s/%s: no chapter (%s.md or topic-<name>.md)" % (book.FOLDER, name, path.name, ".md, ".join(book.CHAPTERS)))
            elif path.stem not in book.CHAPTERS:
                topics.append(path.stem)
        for chapter in book.CHAPTERS:
            if not (own / (chapter + ".md")).is_file():
                errors.append("%s/%s/%s.md: missing: a division keeps the six chapters %s" % (book.FOLDER, name, chapter, ", ".join(book.CHAPTERS)))
        if len(topics) > book.TOPICS:
            errors.append("%s/%s/: %d topic chapters (%s), at most %d" % (book.FOLDER, name, len(topics), ", ".join(topics), book.TOPICS))
        if len(files) > book.CHAPTERS_MAX:
            errors.append("%s/%s/: %d files, at most %d chapters" % (book.FOLDER, name, len(files), book.CHAPTERS_MAX))
        seen = {}
        for path in chapter_files(root, name):
            if not book.chapter_ok(path.stem):
                continue
            found_errors, found = check_chapter(path, path.stem, today)
            errors += found_errors
            chapters += 1
            entries += len(found)
            for sid, title, where in found:
                if sid in seen:
                    errors.append("%s: the entry `%s` has the id `%s` of %s: one title (or Id:) once in a division" % (where, title[:60], sid, seen[sid]))
                else:
                    seen[sid] = where
    return errors, warnings, chapters, entries


def run_check(root, which):
    errors, warnings, chapters, entries = check(root, which)
    for line in errors:
        print("HALT " + line)
    for line in warnings:
        print("WARN " + line)
    print("GUIDE CHECK | %s | %d chapters, %d entries | %s" % (which or "all", chapters, entries, "HALT" if errors else "PASS"))
    print("Errors: %d | Warnings: %d" % (len(errors), len(warnings)))
    return 1 if errors else 0


def sizes(root, which):
    """[(division, chapter, entries, chars, cap, entries over ENTRY_MAX, largest entry)] from the files."""
    out = []
    for name in divisions(which):
        for path in chapter_files(root, name):
            parsed = book.parse(path.read_text(encoding="ascii", errors="replace"))
            texts = [len(e["text"]) for e in parsed["entries"]]
            out.append((name, path.stem, len(texts), sum(texts), book.cap_of(path.stem), sum(1 for t in texts if t > book.ENTRY_MAX), max(texts, default=0)))
    return out


def run_sizes(root, which):
    rows = sizes(root, which)
    print("GUIDE SIZES | %s | characters of a chapter: its entries' texts (status line and body) | caps: card %s, a chapter %s, an entry %s"
          % (which or "all", docs.num(book.CARD_MAX), docs.num(book.CHAPTER_MAX), docs.num(book.ENTRY_MAX)))
    print("  %-10s %-15s %7s %8s %7s %6s %13s %8s" % ("division", "chapter", "entries", "chars", "cap", "over", "entries over", "largest"))
    for name, chapter, count, chars, cap, over, largest in rows:
        print("  %-10s %-15s %7d %8s %7s %6s %13d %8s" % (name, chapter, count, docs.num(chars), docs.num(cap), "OVER" if chars > cap else "", over, docs.num(largest)))
    print("  %d chapters, %d over their cap; %d entries, %d over theirs" % (len(rows), sum(1 for r in rows if r[3] > r[4]), sum(r[2] for r in rows), sum(r[5] for r in rows)))
    return 0


# ---- the split of an old guidebook

def blame_dates(git, rel, text):
    """{line number: YYYY-MM-DD of the last commit that touched it} from `git blame` of HEAD; SplitError when git
    fails or HEAD's file differs from the one split."""
    try:
        done = subprocess.run(["git", "-C", str(git), "blame", "--line-porcelain", "HEAD", "--", rel], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as error:
        raise SplitError("git blame of %s in %s: %s" % (rel, git, error))
    if done.returncode != 0:
        raise SplitError("git blame of %s in %s: %s (no repository? give --git <repository> or --updated YYYY-MM-DD)" % (rel, git, done.stderr.strip()[:200]))
    dates, lines, t = {}, [], None
    for line in done.stdout.splitlines():
        if line.startswith("committer-time "):
            t = int(line.split()[1])
        elif line.startswith("\t"):
            lines.append(line[1:])
            dates[len(lines)] = time.strftime("%Y-%m-%d", time.gmtime(t))
    if lines != text.splitlines():
        raise SplitError("%s differs from its text at HEAD of %s: commit it first, or give --updated YYYY-MM-DD" % (rel, git))
    return dates


def chapter_for(name, title):
    low = title.lower()
    for key, chapter in OWN.get(name, ()) + MAP:
        if low.startswith(key):
            return chapter
    return REST


def numbered(title):
    """(its number or '', the title without it): `15.3 The first outpost` -> ('15.3', 'The first outpost')."""
    found = NUMBER.match(title)
    return (found.group(1), found.group(2).strip()) if found else ("", title.strip())


def segments(text, name, head_title=HEAD_TITLE):
    """The old guidebook's parts in their order: [{title, label, chapter, lines: [(line number, line)], at: [the
    heading's line number]}]; and the list of every line that is no heading (the frontmatter left out), the text a
    split must keep."""
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        close = next((n for n in range(1, len(lines)) if lines[n].strip() == "---"), None)
        if close is None:
            raise SplitError("its frontmatter is not closed")
        start = close + 1
    head = {"title": head_title, "label": "", "chapter": REST, "lines": [], "at": []}
    out, keep, section, titled, fence = [head], [], None, False, False
    for i in range(start, len(lines)):
        line, n = lines[i], i + 1
        heading = None
        if book.FENCE.match(line):
            fence = not fence
        elif not fence:
            heading = book.HEADING.match(line)
        level = len(heading.group(1)) if heading else 0
        if level == 1 and not titled and section is None:
            titled = True
            continue
        if level == 1:
            raise SplitError("line %d: a second title `%s`: split it by hand" % (n, line[:60]))
        if level == 2:
            number, title = numbered(heading.group(2).strip())
            section = {"title": title, "label": number or title, "chapter": chapter_for(name, title), "lines": [], "at": [n]}
            out.append(section)
            continue
        if level == 3:
            number, title = numbered(heading.group(2).strip())
            parent = section or head
            out.append({"title": title, "label": number or parent["label"], "chapter": parent["chapter"], "lines": [], "at": [n]})
            continue
        out[-1]["lines"].append((n, line))
        keep.append(line)
    return out, keep


def plan_split(text, name, dates, today, source=None):
    """The entries of a split in the old file's order: [{chapter, title, status_line, body, label}]; `source` the name
    the Evidence line gives the old file (default guidebook/<name>.md)."""
    import docs as writings
    source = source or "guidebook/%s.md" % name
    parts, keep = segments(text, name, HEAD_TITLE if source.startswith("guidebook/") else "About " + source)
    entries, seen = [], set()
    for part in parts:
        body = [line for _n, line in part["lines"]]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        if not body:
            continue
        title = part["title"]
        if writings.slug(title) in seen:
            title = "%s (section %s)" % (title, part["label"] or "head")
        n = 2
        while writings.slug(title) in seen:
            title, n = "%s %d" % (part["title"], n), n + 1
        seen.add(writings.slug(title))
        numbers = part["at"] + [n for n, _line in part["lines"]]
        updated = max((dates.get(n) for n in numbers if dates.get(n)), default=None) if isinstance(dates, dict) else dates
        where = " section %s" % part["label"] if part["label"] else ", the text above its first section"
        entries.append({"chapter": part["chapter"], "title": title, "label": part["label"], "body": "\n".join(body),
                        "status_line": "Status: proven. Updated: %s. Evidence: migrated from %s%s." % (updated or today, source, where)})
    return entries, keep


def render(name, entries):
    """{chapter: its text}: the six chapters (an empty one holds its title line) and every topic an entry names."""
    names = list(book.CHAPTERS) + sorted({e["chapter"] for e in entries if e["chapter"] not in book.CHAPTERS})
    out = {}
    for chapter in names:
        parts = [book.title_line(name, chapter)]
        parts += ["### %s\n%s\n\n%s" % (e["title"], e["status_line"], e["body"]) for e in entries if e["chapter"] == chapter]
        out[chapter] = "\n\n".join(parts) + "\n"
    return out


def lost(keep, entries, texts):
    """What a split would lose or change: [str]; [] when every line of the old text minus its headings stands, in its
    order, in the bodies of the chapters' entries read back by guidebook.py's parser, and nothing else stands there."""
    read = {}
    for chapter, text in texts.items():
        for entry in book.parse(text)["entries"]:
            read[entry["title"]] = (chapter, entry)
    problems, got = [], []
    for e in entries:
        found = read.pop(e["title"], None)
        if found is None:
            problems.append("the entry `%s` is not read back from its chapter" % e["title"])
            continue
        chapter, entry = found
        if chapter != e["chapter"] or entry["body"] != e["body"] or entry["evidence"] is None:
            problems.append("the entry `%s` reads back changed (%s)" % (e["title"], chapter))
        got += entry["body"].splitlines()
    problems += ["an entry `%s` stands that the old file does not hold" % title for title in read]
    want = [line for line in keep if line.strip()]
    have = [line for line in got if line.strip()]
    if want != have:
        at = next((n for n, (a, b) in enumerate(zip(want, have)) if a != b), min(len(want), len(have)))
        problems.append("the old text minus its headings and the entries differ at its %d. line that is not blank: `%s` against `%s` (%d lines against %d)"
                        % (at + 1, (want[at] if at < len(want) else "")[:60], (have[at] if at < len(have) else "")[:60], len(want), len(have)))
    return problems


def split(root, name, git=None, updated=None, dry=False, now=None, source=None):
    """Split game/routes/guidebook/<name>.md, or the file `source` names, into game/routes/guidebook/<name>/:
    ({chapter: (entries, characters)} written or that would be, lines of text kept)."""
    base = folder(root)
    old, own = (Path(source) if source else base / (name + ".md")), base / name
    if not old.is_file():
        raise SplitError("%s: no such file%s" % (source or "%s/%s.md" % (book.FOLDER, name), " (already split)" if own.is_dir() and not source else ""))
    if own.is_dir() and any(own.iterdir()):
        raise SplitError("%s/%s/ holds chapters already: the split writes into an empty folder only" % (book.FOLDER, name))
    text = old.read_bytes().decode("ascii")
    today = time.strftime("%Y-%m-%d", time.gmtime(now if now is not None else time.time()))
    if updated:
        if not DATE.match(updated):
            raise SplitError("--updated %s is no date YYYY-MM-DD" % updated)
        dates = updated
    else:
        repo, rel = Path(git or root).resolve(), old.name   # a copy outside both: its name in the repository git reads
        for base_dir in (repo, Path(root).resolve()):       # its path in --git, else its path in --root (a tree of that repository)
            try:
                rel = old.resolve().relative_to(base_dir).as_posix()
                break
            except ValueError:
                continue
        dates = blame_dates(repo, rel, text)
    entries, keep = plan_split(text, name, dates, today, old.name if source else None)
    texts = render(name, entries)
    problems = lost(keep, entries, texts)
    if problems:
        raise SplitError("; ".join(problems[:5]))
    out = {}
    for chapter, chapter_text in texts.items():
        parsed = book.parse(chapter_text)
        out[chapter] = (len(parsed["entries"]), sum(len(e["text"]) for e in parsed["entries"]))
    if not dry:
        own.mkdir(parents=True, exist_ok=True)
        for chapter, chapter_text in texts.items():
            (own / (chapter + ".md")).write_text(chapter_text, encoding="ascii")
        if not source or old.resolve().parent == base.resolve():
            old.unlink()
    return out, len(keep)


def run_split(root, which, git, updated, dry, source=None):
    code, names = 0, divisions(which)
    if source and len(names) != 1:
        print("HALT split: --source names the file of one division, not all; nothing written")
        return 1
    for name in names:
        if which in (None, "", "all") and not (folder(root) / (name + ".md")).is_file():
            print("SPLIT %s | no %s/%s.md: %s" % (name, book.FOLDER, name, "split already" if (folder(root) / name).is_dir() else
                                                 "nothing to split (command: split command --source <file>)"))
            continue
        try:
            done, lines = split(root, name, git, updated, dry, source=source)
        except SplitError as error:
            print("HALT split %s: %s; nothing written" % (name, error))
            code = 1
            continue
        print("SPLIT %s | %s -> %s/%s/: %d chapters, %d entries; %d lines of text kept, checked line by line%s"
              % (name, source or "game/routes/guidebook/%s.md" % name, book.FOLDER, name, len(done), sum(n for n, _c in done.values()), lines,
                 " (dry run: nothing written)" if dry else ", the old file left where it stands" if source else ", the old file removed"))
        for chapter, (count, chars) in done.items():
            cap = book.cap_of(chapter)
            print("  %-15s %3d entries %8s of %6s characters%s" % (chapter, count, docs.num(chars), docs.num(cap), "  OVER: its Admiral refines it" if chars > cap else ""))
    return code


# ---- tidy: retired entries out of their chapter, once the store holds them

def tidy(root, data, name, dry=False):
    """{'removed': [(chapter, id, title)], 'waiting': [...], 'why': text or None}; the chapter files rewritten unless
    dry."""
    conn, why = docs.open_copy(data)
    out = {"removed": [], "waiting": [], "why": why}
    try:
        for path in chapter_files(root, name):
            text = path.read_text(encoding="ascii")
            rows = [s for s in book.sections(text, path.stem) if s[0] != book.HEAD]
            parsed = book.parse(text)["entries"]
            rel = "%s/%s/%s" % (book.FOLDER, name, path.name)
            drop = []
            for (sid, title, body), entry in zip(rows, parsed):
                if entry["status"] != "retired":
                    continue
                kept = conn is not None and conn.execute("SELECT 1 FROM doc_versions WHERE path = ? AND section = ? AND sha = ?",
                                                         (rel, sid, docs.sha(title, body))).fetchone()
                (out["removed"] if kept else out["waiting"]).append((path.stem, sid, entry["title"]))
                if kept:
                    drop.append(entry)
            if drop and not dry:
                lines = text.splitlines()
                starts = [e["line"] for e in parsed]
                cut = set()
                for entry in drop:
                    later = [s for s in starts if s > entry["line"]]
                    cut.update(range(entry["line"], (later[0] if later else len(lines) + 1)))
                left = [line for n, line in enumerate(lines, 1) if n not in cut]
                while left and not left[-1].strip():
                    left.pop()
                path.write_text("\n".join(left) + "\n", encoding="ascii")
    finally:
        if conn is not None:
            conn.close()
    return out


def run_tidy(root, data, which, dry):
    for name in divisions(which):
        done = tidy(root, data, name, dry)
        print("TIDY %s | %d retired entries: %d %s (each stands in the store: doc_versions, hive.py guide %s --retired), %d wait for the store's next pass%s"
              % (name, len(done["removed"]) + len(done["waiting"]), len(done["removed"]), "would leave its chapter" if dry else "left its chapter", name,
                 len(done["waiting"]), " (%s)" % done["why"] if done["why"] else ""))
        for chapter, sid, title in done["removed"]:
            print("  %s %s.md %s: %s" % ("would remove" if dry else "removed", chapter, sid, title[:70]))
        for chapter, sid, title in done["waiting"]:
            print("  waits  %s.md %s: the store's read copy holds no version with this text yet; tidy again after its next pass" % (chapter, sid))
    if not dry:
        print("  commit the chapters by path under your name; the store keeps every version")
    return 0


def main(argv):
    parser = argparse.ArgumentParser(prog="guide.py", description=__doc__.split("\n")[0], add_help=True)
    parser.add_argument("verb", choices=("check", "sizes", "split", "tidy"))
    parser.add_argument("division", nargs="?", default="all")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--data", default=DATA)
    parser.add_argument("--git", default=None)
    parser.add_argument("--updated", default=None)
    parser.add_argument("--source", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.verb == "check":
        return run_check(args.root, args.division)
    if args.verb == "sizes":
        return run_sizes(args.root, args.division)
    if args.verb == "split":
        return run_split(args.root, args.division, args.git, args.updated, args.dry_run, args.source)
    return run_tidy(args.root, args.data, args.division, args.dry_run)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
