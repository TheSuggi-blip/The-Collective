#!/usr/bin/env python3
"""docs.py -- the fleet's written knowledge by section in the store: the rulebook rule by rule, the orders in force block by block, the strategy, the empire, the guidebooks with their class cards and levelling guides, the route templates and the game's rules, each section with every version it had.

WHAT: the service `store` (store.py) calls it at every pass; the files stay the source, the tables only mirror them:
        files(data, root)  the source files of the repository: governance/rulebook.md, governance/strategy.md,
                           governance/empire.md, game/routes/guidebook/<division>.md, game/routes/templates/<division>.json,
                           game/rules/*.md, communications/orders.log
        read(path, ctx)    one file -> the rows of the snapshot table docs (path, kind, owner, section, n: its place in
                           the file, title, text, sha, chars, t: the file's mtime), read again only when the file changed
        keep(conn, now)    after the snapshot, the history table doc_versions: a new row for every section whose sha
                           is new, last_seen moved on for every version that stands
      parse(path) splits one file into (section id, title, text):
        Markdown     by heading; the id is the heading path slugged (`part-b-how-we-play/12-standing-rules`); the file's
                     title heading with the text above it is `top`. Each row `| F<n> <title> | <text> |` of the rulebook
                     is its own section `F<n>`, and each table row of game/rules/*.md its own section named by its first
                     cell (`credits`); such rows are not in the text of their heading's section
        templates    one section per template: its name, its title, its JSON
        orders.log   the newest entry only, by block: `head` (its header and Changed line), each S<n>, G<n>, D<n> and
                     P<n> line, each block's own lines (`standing-orders`, `direction`, `plan`, `turn`, `every-admiral`)
                     and each member's block (`unity`, `zero`, `mercury`, `apollo`, `apophis`, `oracle`)
      The owner of a section: the division of the file's name (guidebook/military.md: Military), Fleet for governance
      and the game's rules, Unity for the orders. Readers: hive.py docs and changes, the briefing's section CHANGED
      SINCE YOUR LAST TURN, the MCP tool docs; all read the store's read copy.
RULES:
  - Nobody writes the tables by hand: members edit the files, git keeps their history, the gates check them, and the
    store mirrors them every minute. A file is parsed only when its size or mtime changed (the store's table source).
  - A section's sha is the sha1 of its title and its text. doc_versions gets a row only when a section's sha is not
    the sha of its newest version (a text set back to an older one is a new row: the order of changes is kept).
    last_seen is the last pass in which a version stood. A section that left (its file changed or went) keeps every
    row; its last_seen stops. Rows of doc_versions are never deleted.
  - The first pass that finds doc_versions empty is the baseline (meta `docs.baseline`): what it loads counts as no
    change, or every member would read the whole fleet's knowledge as new once.
  - A member's last turn is the time of its newest entry in communications/reports.log (its archive too); with no
    member named, Unity's.
WHY:  every member read the whole rulebook (35,000 characters), its guidebook and the orders at every turn to find what
      changed. Suggi, 2026-11-17: keep them in the database, kept there by scripts, with history, so that nobody needs
      to read whole files.

USAGE:
  docs.py parse <file>      the sections of one file as the store loads them: id, characters, title

Stdlib only. ASCII only.
"""

import calendar
import difflib
import fnmatch
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names: a file's owner
import division                                   # noqa: E402  the members, who runs this

KINDS = (                      # kind, its files (repository paths, a glob), its owner ('': the division of the file's name)
    ("rulebook", "governance/rulebook.md", "Fleet"),
    ("orders", "communications/orders.log", "Unity"),
    ("strategy", "governance/strategy.md", "Fleet"),
    ("empire", "governance/empire.md", "Fleet"),
    ("guidebook", "game/routes/guidebook/*.md", ""),
    ("template", "game/routes/templates/*.json", ""),
    ("rules", "game/rules/*.md", "Fleet"),
)
ORDER = [kind for kind, _pattern, _owner in KINDS]
SLUG = 60                      # characters of one part of a section id
LIST_ROWS = 150                # sections `docs` lists by title; more, and it lists the files only
TEXT_CHARS = 25000             # characters of text `docs` prints at most (an answer of the MCP tools is cut at 30,000)
BRIEF_ROWS = 30                # lines of the briefing's section, at most
REPORTS = "communications/reports.log"

HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE = re.compile(r"^[ \t]*(```|~~~)")
RULE_ROW = re.compile(r"^\|\s*(F\d+)\b")
SEPARATOR = re.compile(r"^\s*\|?(?:\s*:?-{2,}:?\s*\|)+\s*:?-*:?\s*$")
ENTRY = re.compile(r"^## \[ENT-(\d+)\] \| (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC \| ([A-Za-z][A-Za-z0-9_-]*) \| ([a-z]+)")
BLOCK = re.compile(r"^([A-Z]{2,}(?: [A-Z]{2,})*)(?=,|\s*\(|\s*$)")
ITEM = re.compile(r"^([A-Z])(\d+)\.\s")


# ---- one file -> sections

def slug(text):
    """A section id's part: lower case, a dash between words, at most SLUG characters."""
    found = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return found[:SLUG].strip("-") or "section"


def cells(line):
    """The cells of a Markdown table row, split at each `|` that is not escaped."""
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") and not body.endswith("\\|") else body
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", body)]


def kind_of(rel):
    """(kind, owner) of a repository path; ('', '') for a file that is no source."""
    rel = str(rel).replace(os.sep, "/")
    for kind, pattern, owner in KINDS:
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(rel, "*/" + pattern):
            if not owner:
                stem = Path(rel).stem.lower()
                owner = next((name for name in board.NAMES.values() if name.lower() == stem), stem.title())
            return kind, owner
    return "", ""


def parse_markdown(text, rows=""):
    """[(id, title, text)] of a Markdown file by heading; rows='F': each rule row `| F<n> ... |` is its own section,
    rows='table': each table row that is no header is its own section named by its first cell."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":                       # the frontmatter is no section
        for n in range(1, len(lines)):
            if lines[n].strip() == "---":
                lines = lines[n + 1:]
                break
    out, stack, fence, titled = [], [], False, False
    current = {"id": "top", "title": "", "lines": [], "row": False}
    out.append(current)
    for n, line in enumerate(lines):
        if FENCE.match(line):
            fence = not fence
            current["lines"].append(line)
            continue
        heading = None if fence else HEADING.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            if level == 1 and not titled and not stack and len(out) == 1:      # the file's title: it heads `top`
                titled = True
                current["title"] = title
                current["lines"].append(line)
                continue
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, slug(title)))
            current = {"id": "/".join(part for _level, part in stack), "title": title, "lines": [line], "row": False}
            out.append(current)
            continue
        if not fence and rows and line.lstrip().startswith("|"):
            if rows == "F":
                rule = RULE_ROW.match(line.strip())
                if rule:
                    parts = cells(line)
                    out.append({"id": rule.group(1), "title": parts[0], "lines": [" | ".join(parts[1:])], "row": True})
                    continue
            elif rows == "table" and not SEPARATOR.match(line):
                header = n + 1 < len(lines) and SEPARATOR.match(lines[n + 1])
                parts = cells(line)
                if not header and parts and parts[0]:
                    base = "" if current["id"] == "top" else current["id"] + "/"
                    out.append({"id": base + slug(parts[0]), "title": parts[0], "lines": [" | ".join(parts[1:])], "row": True})
                    continue
        current["lines"].append(line)
    found, seen = [], {}
    for section in out:
        body = "\n".join(section["lines"]).strip("\n")
        if not body.strip() and not section["row"]:
            continue
        sid = section["id"]
        seen[sid] = seen.get(sid, 0) + 1
        if seen[sid] > 1:
            sid = "%s-%d" % (sid, seen[sid])
        found.append((sid, section["title"] or "(the head of the file)", body))
    return found


def parse_templates(text):
    """[(name, title, JSON)] of a templates file: {templates: {name: {...}}} (or a list of objects with a name)."""
    found = json.loads(text)
    templates = found.get("templates") if isinstance(found, dict) else None
    if isinstance(templates, dict):
        pairs = list(templates.items())
    elif isinstance(templates, list):
        pairs = [(t.get("name") or t.get("id"), t) for t in templates if isinstance(t, dict)]
    else:
        raise ValueError("no object `templates`")
    out, seen = [], set()
    for name, body in pairs:
        sid = str(name) if re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", str(name or "")) else slug(name)
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        title = body.get("title") if isinstance(body, dict) and isinstance(body.get("title"), str) else str(name)
        out.append((sid, title, json.dumps(body, indent=1, ensure_ascii=True)))
    return out


def item_title(line):
    """`D3. Every division researches its own class` of a numbered line: its number and its words up to the first stop."""
    found = ITEM.match(line)
    rest = line[found.end():].strip()
    head = "%s%s. %s" % (found.group(1), found.group(2), re.split(r"[:.;](?:\s|$)", rest, maxsplit=1)[0].strip())
    return head if len(head) <= 80 else head[:77] + "..."


def parse_orders(text):
    """[(id, title, text)] of the newest entry of orders.log: `head`, each S/G/D/P line, each block's own lines, each
    member's block."""
    lines = text.splitlines()
    starts = [n for n, line in enumerate(lines) if line.startswith("## [ENT-")]
    if not starts:
        return []
    entry = lines[starts[-1]:]
    header = ENTRY.match(entry[0])
    when = "ENT-%s of %s UTC" % (header.group(1), header.group(2)) if header else entry[0][3:40]
    head = {"id": "head", "title": "%s: the entry's head and its Changed line" % when, "lines": [entry[0]]}
    out, block, current = [head], head, head
    for line in entry[1:]:
        named = BLOCK.match(line)
        item = ITEM.match(line)
        if named:
            block = current = {"id": slug(named.group(1)), "title": line.strip()[:100], "lines": [line]}
            out.append(current)
        elif item:
            current = {"id": item.group(1) + item.group(2), "title": item_title(line), "lines": [line]}
            out.append(current)
        elif current is not block and line[:1] in (" ", "\t", ""):
            current["lines"].append(line)                          # a numbered line's own continuation (`  Goal: ...`)
        else:
            current = block
            block["lines"].append(line)
    found, seen = [], {}
    for section in out:
        body = "\n".join(section["lines"]).strip("\n")
        sid = section["id"]
        seen[sid] = seen.get(sid, 0) + 1
        if seen[sid] > 1:
            sid = "%s-%d" % (sid, seen[sid])
        found.append((sid, section["title"], body))
    return found


def parse(path, kind=None):
    """[(section id, title, text)] of one source file, by its kind (from its path when not given)."""
    kind = kind or kind_of(Path(path).resolve().as_posix())[0]
    with open(path, "rb") as handle:
        text = handle.read().decode("utf-8", errors="replace")
    if kind == "template":
        return parse_templates(text)
    if kind == "orders":
        return parse_orders(text)
    return parse_markdown(text, "F" if kind == "rulebook" else "table" if kind == "rules" else "")


def sha(title, text):
    return hashlib.sha1(("%s\n%s" % (title, text)).encode("utf-8")).hexdigest()


# ---- the store's side: the files, one file's rows, the history

def sources(repo):
    """[(repository path, path, kind, owner)] of every source file that exists, in the order of KINDS."""
    out = []
    for kind, pattern, _owner in KINDS:
        for path in sorted(Path(repo).glob(pattern)):
            if path.is_file():
                rel = path.relative_to(repo).as_posix()
                out.append((rel, path, kind, kind_of(rel)[1]))
    return out


def files(data, root):
    """The store's loader: [(source name, path, reader, required, note)]; the source name is the repository path."""
    repo = Path(root).resolve().parent
    return [(rel, path, read, False, "") for rel, path, _kind, _owner in sources(repo)]


def read(path, ctx):
    """One source file -> {docs: [rows]} (store.py's reader form)."""
    repo = Path(ctx["root"]).resolve().parent
    try:
        rel = Path(path).resolve().relative_to(repo).as_posix()
    except ValueError:
        rel = Path(path).as_posix()
    kind, owner = kind_of(rel)
    mtime = int(os.stat(path).st_mtime)
    return {"docs": [{"path": rel, "kind": kind, "owner": owner, "section": sid, "n": n, "title": title, "text": text,
                      "sha": sha(title, text), "chars": len(text), "t": mtime}
                     for n, (sid, title, text) in enumerate(parse(path, kind), 1)]}


def meta_of(conn, key):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def keep(conn, now, problems=None):
    """The history of every section (doc_versions), after the snapshot loaded the table docs: a new row for each section
    whose sha is not its newest version's, last_seen = now for each version that stands. One transaction; a fault is
    returned, never raised (the next pass compares again), and named in `problems` (the snapshot's, which the pass's
    line prints): {added, standing, error}."""
    now, out = int(now), {"added": 0, "standing": 0, "error": None}
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'docs'").fetchone():
            return out
        conn.execute("BEGIN IMMEDIATE")
        try:
            newest = {(path, section): (version, digest) for path, section, version, digest in
                      conn.execute("SELECT path, section, MAX(version), sha FROM doc_versions GROUP BY path, section")}
            standing, fresh = [], []
            for path, section, digest in conn.execute("SELECT path, section, sha FROM docs"):
                old = newest.get((path, section))
                if old and old[1] == digest:
                    standing.append(old[0])
                else:
                    fresh.append((path, section))
            if fresh and not newest and meta_of(conn, "docs.baseline") is None:
                conn.execute("INSERT OR REPLACE INTO meta VALUES ('docs.baseline', ?)", (now,))
            for path, section in fresh:
                conn.execute("INSERT INTO doc_versions (path, section, sha, title, text, first_seen, last_seen) "
                             "SELECT path, section, sha, title, text, ?, ? FROM docs WHERE path = ? AND section = ?", (now, now, path, section))
            conn.executemany("UPDATE doc_versions SET last_seen = ? WHERE version = ? AND last_seen < ?", [(now, v, now) for v in standing])
            conn.execute("COMMIT")
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        out.update(added=len(fresh), standing=len(standing))
    except Exception as error:                                   # a fault here never holds up the store's pass
        out["error"] = "%s: %s" % (type(error).__name__, error)
        if problems is not None:
            problems.append(("doc_versions", "not kept: " + out["error"]))
    return out


# ---- the readers' side (hive.py docs, changes, the briefing)

def stamp(t):
    return time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(t)) if t else "--"


def copy_line(data, now):
    path = Path(data) / "store" / "read.db"
    written = path.stat().st_mtime if path.is_file() else None
    return "the store's read copy %s, written %s" % (path, "%s (%d s old)" % (stamp(written), now - written) if written else "never")


def open_copy(data):
    """(connection, None) to the store's read copy, or (None, why not)."""
    import store as history                                      # the store imports this module: imported here, not above
    conn = history.connect(data)
    if conn is None:
        return None, "no read copy at %s: the service `store` has not published one yet" % (Path(data) / "store" / "read.db")
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'doc_versions'").fetchone():
        conn.close()
        return None, "the store's read copy holds no table docs yet: the service `store` loads it at its first pass with docs.py"
    return conn, None


def parse_since(text, now):
    """Seconds of `2026-11-17T12:00Z`, `2026-11-17 12:00`, `2026-11-17`, or `6h` (hours before now); ValueError."""
    text = str(text).strip()
    hours = re.fullmatch(r"(\d+(?:\.\d+)?)\s*h", text)
    if hours:
        return int(now - float(hours.group(1)) * 3600)
    body = text.replace("T", " ").replace(" UTC", "").rstrip("Z").strip()
    for form in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d %H", "%Y-%m-%d"):
        try:
            return calendar.timegm(time.strptime(body, form))
        except ValueError:
            continue
    raise ValueError("not a time: `%s` (2026-11-17T12:00Z, 2026-11-17 12:00, 2026-11-17 or 6h)" % text)


def member_of(name):
    """A member's name for a member's or a division's name (any case); None for anything else."""
    low = str(name or "").lower()
    return next((m for m in division.MEMBERS if low in (m.lower(), board.NAMES.get(m, m).lower())), None)


def last_turn(repo, member):
    """(seconds, what it rests on) of a member's last turn: its newest session entry in reports.log (the archive too);
    (None, why) when it has none."""
    folder = Path(repo) / "communications"
    paths = sorted((folder / "archive").glob("reports-*.log")) if (folder / "archive").is_dir() else []
    newest = None
    for path in paths + [folder / "reports.log"]:
        try:
            text = path.read_text(encoding="ascii", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            found = ENTRY.match(line)
            if found and found.group(3) == member and found.group(4) == "session":
                t = calendar.timegm(time.strptime(found.group(2), "%Y-%m-%d %H:%M"))
                if newest is None or t >= newest[0]:
                    newest = (t, "ENT-%s of %s UTC" % (found.group(1), found.group(2)))
    if newest is None:
        return None, "no session entry of %s in %s" % (member, REPORTS)
    return newest[0], "%s's last turn: its newest entry in %s, %s" % (member, REPORTS, newest[1])


def rows_of(conn):
    """Every section that stands: [(path, kind, owner, section, n, title, chars, sha, t)] in the order of KINDS, then file
    order."""
    rows = conn.execute("SELECT path, kind, owner, section, n, title, chars, sha, t FROM docs").fetchall()
    rank = lambda kind: ORDER.index(kind) if kind in ORDER else len(ORDER)
    return sorted(rows, key=lambda r: (rank(r[1]), r[0], r[4] or 0))


def pick(rows, what):
    """The rows a filter names: a file (its path or the end of it), a kind, an owner (a member's name too), else a part
    of a path; ([rows], how it matched)."""
    if not what:
        return rows, "every file"
    low = str(what).lower().strip().strip("/")
    member = member_of(low)
    owners = {low} | ({member.lower(), board.NAMES.get(member, member).lower()} if member else set())
    tiers = (("file", lambda r: r[0].lower() == low or r[0].lower().endswith("/" + low)),
             ("kind", lambda r: low in (r[1], r[1] + "s")),
             ("owner", lambda r: r[2].lower() in owners),
             ("part of a path", lambda r: low in r[0].lower()))
    for how, test in tiers:
        found = [r for r in rows if test(r)]
        if found:
            return found, how
    return [], ""


def files_of(rows):
    """{path: [rows]} in the rows' order."""
    out = {}
    for row in rows:
        out.setdefault(row[0], []).append(row)
    return out


def num(n):
    return format(int(n), ",") if isinstance(n, (int, float)) else "--"


def versions_of(conn, path, section):
    return conn.execute("SELECT version, sha, title, text, first_seen, last_seen FROM doc_versions WHERE path = ? AND section = ? "
                        "ORDER BY version", (path, section)).fetchall()


def find_section(conn, rows, section):
    """[(path, section)] that a section id names among the rows' files (standing or gone): the id itself, else any
    case, else a path that ends with it, else one that begins with it."""
    paths = {r[0] for r in rows}
    known = sorted({(r[0], r[3]) for r in rows} | {(p, s) for p, s in conn.execute("SELECT DISTINCT path, section FROM doc_versions") if p in paths})
    low = section.lower()
    for test in (lambda s: s == section, lambda s: s.lower() == low, lambda s: s.lower().endswith("/" + low), lambda s: s.lower().startswith(low)):
        found = [(p, s) for p, s in known if test(s)]
        if found:
            return found
    return []


def show_section(conn, data, now, path, section, history):
    versions = versions_of(conn, path, section)
    row = conn.execute("SELECT kind, owner, title, text, sha, chars FROM docs WHERE path = ? AND section = ?", (path, section)).fetchone()
    if not history:
        if row is None:
            last = versions[-1] if versions else None
            print("DOCS %s %s | gone from its file: last seen %s; its versions: --history" % (path, section, stamp(last[5]) if last else "--"))
            return 0
        kind, owner, title, text, digest, chars = row
        since = next((v[4] for v in reversed(versions) if v[1] == digest), None)
        print("DOCS %s %s | %s | %s chars | %s, %s | this text since %s, %d versions on record (--history) | %s"
              % (path, section, title, num(chars), kind, owner, stamp(since), len(versions), copy_line(data, now)))
        print(text)
        return 0
    standing = row[4] if row else None
    print("HISTORY %s %s | %d versions on record, kept for good from the store's first reading | %s | %s"
          % (path, section, len(versions), "stands now" if row else "gone from its file", copy_line(data, now)))
    for n, (version, digest, title, text, first, last) in enumerate(versions, 1):
        print("  v%d  first seen %s  last seen %s%s  %s chars  sha %s  %s" % (n, stamp(first), stamp(last), " (stands)" if n == len(versions) and digest == standing else "",
                                                                         num(len(text or "")), digest[:10], title[:70]))
    budget = TEXT_CHARS
    for n, (version, digest, title, text, first, last) in enumerate(versions, 1):
        if n == 1:
            lines = ["=== v1, whole (first seen %s):" % stamp(first)] + (text or "").splitlines()
        else:
            before = versions[n - 2]
            diff = list(difflib.unified_diff(("%s\n%s" % (before[2], before[3] or "")).splitlines(), ("%s\n%s" % (title, text or "")).splitlines(),
                                             "v%d" % (n - 1), "v%d" % n, lineterm="", n=1))
            lines = ["=== v%d against v%d (first seen %s):" % (n, n - 1, stamp(first))] + diff[2:]
        size = sum(len(line) + 1 for line in lines)
        if size > budget:
            print("... the texts of v%d to v%d are not printed (%d characters at most): hive.py sql \"SELECT text FROM doc_versions WHERE path = '%s' "
                  "AND section = '%s' ORDER BY version\"" % (n, len(versions), TEXT_CHARS, path, section))
            break
        budget -= size
        print("\n".join(lines))
    return 0


def show_docs(data, now, what, section, grep, history):
    """hive.py docs: the files, a file's sections by title, one section's text (or its versions), the sections that
    hold a word."""
    conn, why = open_copy(data)
    if conn is None:
        print("DOCS | " + why)
        return 1
    try:
        rows = rows_of(conn)
        picked, how = pick(rows, what)
        if not picked:
            kinds = ", ".join(ORDER)
            print("DOCS | nothing matches `%s`: name a file (governance/rulebook.md, guidebook/mining.md), a kind (%s) or an owner "
                  "(Fleet, Unity, %s)" % (what, kinds, ", ".join(board.NAMES[m] for m in division.MEMBERS)))
            return 1
        if section:
            found = find_section(conn, picked, section)
            if len(found) != 1:
                if found:
                    print("DOCS | %d sections answer to `%s` in %s: name the file too, or the whole id" % (len(found), section, what or "every file"))
                else:
                    print("DOCS | no section `%s` in %s; the ids: hive.py docs %s" % (section, what or "any file", what or "<file>"))
                for path, sid in found[:40]:
                    print("  %-44s %s" % (path, sid))
                return 1
            return show_section(conn, data, now, found[0][0], found[0][1], history)
        if grep:
            word = grep.lower()
            hits = [r for r in picked if word in (r[5] or "").lower()
                    or word in (conn.execute("SELECT text FROM docs WHERE path = ? AND section = ?", (r[0], r[3])).fetchone()[0] or "").lower()]
            print("DOCS %s | %d sections hold `%s`, printed whole up to %s characters | %s" % (what or "every file", len(hits), grep, num(TEXT_CHARS), copy_line(data, now)))
            budget, rest = TEXT_CHARS, []
            for r in hits:
                text = conn.execute("SELECT text FROM docs WHERE path = ? AND section = ?", (r[0], r[3])).fetchone()[0] or ""
                if len(text) + 200 > budget:
                    rest.append(r)
                    continue
                budget -= len(text) + 200
                print("=== %s %s | %s | %s chars" % (r[0], r[3], r[5], num(r[6])))
                print(text)
            if rest:
                print("... %d more sections hold it (one: --section <id>):" % len(rest))
                for r in rest:
                    print("  %-44s %-40s %s" % (r[0], r[3], r[5][:60]))
            return 0
        by_file = files_of(picked)
        print("DOCS%s | the fleet's written knowledge by section, mirrored from the repository by the store (table docs; every version: "
              "doc_versions) | %d files, %d sections, matched as %s | %s" % (" " + what if what else "", len(by_file), len(picked), how, copy_line(data, now)))
        if not what or len(picked) > LIST_ROWS:
            print("  %-44s %-9s %-9s %8s %9s  %s" % ("file", "kind", "owner", "sections", "chars", "file changed"))
            for path, its in by_file.items():
                print("  %-44s %-9s %-9s %8d %9s  %s" % (path, its[0][1], its[0][2], len(its), num(sum(r[6] or 0 for r in its)), stamp(its[0][8])))
            print("  a file's sections by title: hive.py docs <file|kind|owner>; one section: --section <id>; a word: --grep <word>; "
                  "what changed: hive.py changes")
            return 0
        for path, its in by_file.items():
            print("%s | %s, %s | %d sections, %s chars | file changed %s" % (path, its[0][1], its[0][2], len(its), num(sum(r[6] or 0 for r in its)), stamp(its[0][8])))
            print("  %7s  %-50s  %s" % ("chars", "section", "title"))
            for r in its:
                print("  %7s  %-50s  %s" % (num(r[6]), r[3], (r[5] or "")[:90]))
        print("  one section whole: hive.py docs %s --section <id>; its versions: add --history; a word: --grep <word>" % (what or "<file>"))
        return 0
    finally:
        conn.close()


def changed(conn, since):
    """The sections whose newest version came after `since` (and after the baseline), and those that left their file
    after it: [(status, path, section, title, chars, when, kind, owner)] in the order of KINDS, then file order."""
    baseline = int(meta_of(conn, "docs.baseline") or 0)
    rows = conn.execute(
        "SELECT v.path, v.section, v.title, LENGTH(v.text), v.first_seen, v.last_seen, d.section IS NOT NULL, d.n, d.kind, d.owner, "
        "(SELECT COUNT(*) FROM doc_versions w WHERE w.path = v.path AND w.section = v.section) FROM doc_versions v "
        "LEFT JOIN docs d ON d.path = v.path AND d.section = v.section WHERE v.version IN (SELECT MAX(version) FROM doc_versions GROUP BY path, section) "
        "AND ((v.first_seen > ? AND v.first_seen > ?) OR (d.section IS NULL AND v.last_seen >= ?))", (since, baseline, since)).fetchall()
    out = []
    for path, section, title, chars, first, last, stands, n, kind, owner, count in rows:
        if not stands:
            kind, owner = kind_of(path)
        status = "gone" if not stands else "new" if count == 1 else "changed"
        out.append((status, path, section, title or "", chars or 0, first if stands else last, kind, owner, n if stands else 10 ** 6))
    rank = lambda kind: ORDER.index(kind) if kind in ORDER else len(ORDER)
    out.sort(key=lambda r: (rank(r[6]), r[1], r[8], r[2]))
    return [r[:8] for r in out], baseline


def resolve_since(repo, now, since, member):
    """(seconds, what it rests on) of --since, else of the member's last turn, else of 24 hours ago."""
    if since:
        t = parse_since(since, now)
        return t, "--since %s" % since
    t, basis = last_turn(repo, member)
    if t is None:
        return int(now - 86400), basis + ": the last 24 hours"
    return t, basis


def change_line(row):
    status, path, section, title, chars, when, _kind, _owner = row
    return "  %-40s %-30s %7s  %s %-7s %s" % (path[:40], section[:30], num(chars), time.strftime("%m-%d %H:%M", time.gmtime(when)), status, title[:70])


def show_changes(root, data, now, since, who):
    """hive.py changes: the sections that changed since a time, the member's last turn by default."""
    member = member_of(who) if who else None
    if who and member is None:
        print("CHANGES | no member `%s`: %s" % (who, ", ".join(division.MEMBERS)))
        return 1
    if member is None:
        kind, name = division.member()
        member = name if kind == "member" and name in division.MEMBERS else "Unity"
    try:
        t, basis = resolve_since(Path(root).resolve().parent, now, since, member)
    except ValueError as error:
        print("CHANGES | %s" % error)
        return 1
    conn, why = open_copy(data)
    if conn is None:
        print("CHANGES | " + why)
        return 1
    try:
        rows, baseline = changed(conn, t)
    finally:
        conn.close()
    print("CHANGES | the fleet's written knowledge: the sections whose text changed after %s (%s), and those that left their file | %d sections | "
          "versions on record since %s, the store's first reading, which counts as no change | %s"
          % (stamp(t), basis, len(rows), stamp(baseline), copy_line(data, now)))
    if not rows:
        print("  no section changed")
        return 0
    print("  %-40s %-30s %7s  %-11s %-7s %s" % ("file", "section", "chars", "when (UTC)", "what", "title"))
    for row in rows:
        print(change_line(row))
    print("  one section whole: hive.py docs <file> --section <id> (the tool docs, view=section); what changed in it: add --history")
    return 0


def briefing(root, data, now, who):
    """The briefing's section: the sections changed since the member's last turn, at most BRIEF_ROWS lines; the
    member's own division's sections (its guidebook and templates: the rules of its role) are counted, not listed."""
    member = who if who in division.MEMBERS else "Unity"
    own = {board.NAMES.get(member, member)}                       # its division: its guidebook and its templates
    print("=== CHANGED SINCE YOUR LAST TURN (the rulebook rule by rule, the orders block by block, strategy, empire, guidebooks, "
          "templates, game rules: one line a section; `hive.py changes` lists them all)")
    try:
        t, basis = resolve_since(Path(root).resolve().parent, now, None, member)
        conn, why = open_copy(data)
        if conn is None:
            print("  not read: " + why)
            return
        try:
            rows, _baseline = changed(conn, t)
            mine = [r for r in rows_of(conn) if r[2] in own]
        finally:
            conn.close()
    except (OSError, sqlite3.Error, ValueError) as error:
        print("  not read: %s: %s" % (type(error).__name__, error))
        return
    others = [r for r in rows if r[7] not in own]
    ours = [r for r in rows if r[7] in own]
    print("  since %s (%s): %d sections changed, %d of them of other owners, listed here" % (stamp(t), basis, len(rows), len(others)))
    room = BRIEF_ROWS - 4
    for row in others[:room if len(others) <= room else room - 1]:
        print(change_line(row))
    if len(others) > room:
        print("  ... %d more: hive.py changes%s" % (len(others) - room + 1, "" if member == "Unity" else " --member " + member))
    if others:
        print("  one section whole: hive.py docs <file> --section <id> (the tool docs, view=section); what changed in it: add --history")
    paths = sorted({r[0] for r in mine})
    print("  YOUR ROLE'S RULES (%s): %d sections, %d changed since then (not listed: %s); not printed whole here: titles `hive.py docs %s`, "
          "one section `hive.py docs %s --section <id>`" % (", ".join(paths) or "no file of %s" % ", ".join(sorted(own)), len(mine), len(ours),
                                                            "hive.py changes" + ("" if member == "Unity" else " --member " + member),
                                                            board.NAMES.get(member, member), board.NAMES.get(member, member)))


VALUED = ("--section", "--grep", "--since", "--member", "--root", "--data", "--hours", "--limit", "--group", "--kind", "--zone", "--item", "--top")


def hive(verb, args, root, data, now):
    """hive.py's verbs docs and changes, with their own options."""
    value = lambda name: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else ""
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in VALUED)]
    rest = words[words.index(verb) + 1:] if verb in words else []
    if verb == "changes":
        return show_changes(root, data, now, value("--since"), value("--member") or (rest[0] if rest else ""))
    if "--history" in args and not value("--section"):
        print("DOCS | --history needs --section <id>: hive.py docs <file> --section <id> --history")
        return 1
    return show_docs(data, now, " ".join(rest), value("--section"), value("--grep"), "--history" in args)


def main(argv):
    if len(argv) >= 2 and argv[0] == "parse":
        path = Path(argv[1])
        kind, owner = kind_of(path.resolve().as_posix())
        found = parse(path, kind)
        print("PARSE %s | %s, %s | %d sections, %s chars" % (path, kind or "no source kind: read as Markdown", owner or "--", len(found),
                                                          num(sum(len(text) for _sid, _title, text in found))))
        for sid, title, text in found:
            print("  %-44s %7s  %s" % (sid, num(len(text)), title[:90]))
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
