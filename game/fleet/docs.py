#!/usr/bin/env python3
"""docs.py -- the fleet's written knowledge by section in the store: the rulebook rule by rule, the orders in force block by block, the strategy, the empire, the guidebooks with their class cards and levelling guides, the route templates, the game's rules, the metrics, and everything the members write as they work (the division plans, the reports, every log entry, the members' own files), each section with every version it had.

WHAT: the service `store` (store.py) calls it at every pass; the files stay the source, the tables only mirror them:
        files(data, root)  the source files: of the repository governance/rulebook.md, governance/strategy.md,
                           governance/empire.md, game/routes/guidebook/<division>/<chapter>.md (game/routes/guidebook/
                           <division>.md before its split), game/routes/templates/<division>.json,
                           game/rules/*.md, game/metrics.md, communications/orders.log, reports/*.md, and the logs
                           requests, queue, admirals, errors and reports (communications/<log>.log and its archive
                           communications/archive/<log>-<date>.log); of the data folder (source name and path
                           `data/...`) the plans data/plans/plan-<division>.md and the members' own files
                           data/docs/members/<member>/... (docs_export.py copies them there from the members' folders)
        read(path, ctx)    one file -> the rows of the snapshot table docs (path, kind, owner, section, n: its place in
                           the file, title, text, sha, chars, t: the file's mtime), read again only when the file changed
        keep(conn, now)    after the snapshot, the history table doc_versions: a new row for every section whose sha
                           is new, last_seen moved on for every version that stands
      parse(path) splits one file into (section id, title, text):
        Markdown     by heading; the id is the heading path slugged (`part-b-how-we-play/12-standing-rules`); the file's
                     title heading with the text above it is `top`. Each row `| F<n> <title> | <text> |` of the rulebook
                     is its own section `F<n>`, and each table row of game/rules/*.md its own section named by its first
                     cell (`credits`); such rows are not in the text of their heading's section
        a chapter    game/routes/guidebook/<division>/<chapter>.md (kind guide, guidebook.py): one section an entry, its
                     id the entry's Id or its title's slug, its title `[<chapter> <status> <updated>] <title>`
        templates    one section per template: its name, its title, its JSON
        orders.log   the newest entry only, by block: `head` (its header and Changed line), each S<n>, G<n>, D<n> and
                     P<n> line, each block's own lines (`standing-orders`, `direction`, `plan`, `turn`, `every-admiral`)
                     and each member's block (`unity`, `zero`, `mercury`, `apollo`, `apophis`, `oracle`)
        a log        every entry one section `ENT-<n>` (communications/protocol.md): its title the head line, its text
                     the body, its n the ENT number. An archived entry stands under its log's own path
                     (communications/requests.log): CI's archiving moves it, it changes nothing
        COLLECTIVE.md  of a member, while it stands: the part below the MISSION mark is the section `mission`; the part
                     above it, the same in every member's copy, is loaded from Unity's copy only (the master), so it
                     stands once. Since 2026-11-18 it is split: each member's MISSION.md (its role card) and the roster
                     ROSTER.md, the same in every workspace, copied once to data/docs/members/fleet/ (owner Fleet)
        plans, reports, the metrics and the members' other files: by heading, as Markdown
      The owner of a section: the division of the member or division the file's name or folder names
      (guidebook/military.md, plan-military.md, a report <date>_apophis_<slug>.md, members/apophis/: Military); of a
      log entry its author's division (a name that is no member's stands as written); Fleet for governance, the game's
      rules and the metrics, Unity for the orders. Readers: hive.py docs and changes, the briefing's section CHANGED
      SINCE YOUR LAST TURN, hive.py division (docs_division.py), the MCP tool docs; all read the store's read copy.
RULES:
  - Nobody writes the tables by hand: members edit the files, git keeps their history, the gates check them, and the
    store mirrors them every minute. A file is parsed only when its size or mtime changed (the store's table source).
  - A section's sha is the sha1 of its title and its text. doc_versions gets a row only when a section's sha is not
    the sha of its newest version (a text set back to an older one is a new row: the order of changes is kept).
    last_seen is the last pass in which a version stood: exact for a version that stands no more (set when it stops);
    for one that stands, the newest pass that changed a section, at most KEEP_EVERY (15 minutes) old, so a quiet pass
    writes no row. A section that left (its file changed or went) keeps every row; its last_seen stops. Rows of
    doc_versions are never deleted.
  - The first pass that finds doc_versions empty is the baseline (meta `docs.baseline`): what it loads counts as no
    change, or every member would read the whole fleet's knowledge as new once. So is, for each kind, the pass that
    first loads a kind with no version on record (meta `docs.baseline.<kind>`): a kind added later (the logs, the
    reports) does not read as thousands of new sections once.
  - A log is append-only: a new entry is a new section, the entries before it keep their sha and add no version. A
    changed log is parsed whole; its parse and its rows cost milliseconds (the timing in the test).
  - The briefing lists the rules and the orders one line a section and the members' writing one line a file (a claim
    one line), titles and sizes only, BRIEF_ROWS lines at most; nothing of the member's own writing.
  - A member's last turn is the time of its newest entry in communications/reports.log (its archive too); with no
    member named, Unity's.
WHY:  every member read the whole rulebook (35,000 characters), its guidebook and the orders at every turn to find what
      changed. Suggi, 2026-11-17: keep them in the database, kept there by scripts, with history, so that nobody needs
      to read whole files. Suggi, 2026-11-18: everything in the database, so the other agents know what the other
      Admirals are doing; they edit their files, a script fetches them and stores them, never by hand.

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

LOGS = ("requests", "queue", "admirals", "errors", "reports")     # the logs kept entry by entry (orders.log: its newest entry, by block)
KINDS = (                      # kind, its files (a glob: a repository path, or `data/...` in the unit's data folder), its owner
    ("rulebook", "governance/rulebook.md", "Fleet"),          # ('': the division its file's name or folder names; '*': each entry's author's)
    ("orders", "communications/orders.log", "Unity"),
    ("strategy", "governance/strategy.md", "Fleet"),
    ("empire", "governance/empire.md", "Fleet"),
    ("guide", "game/routes/guidebook/*/*.md", ""),           # a guidebook's chapters, one section an entry (guidebook.py); before the row below
    ("guidebook", "game/routes/guidebook/*.md", ""),
    ("template", "game/routes/templates/*.json", ""),
    ("rules", "game/rules/*.md", "Fleet"),
    ("metrics", "game/metrics.md", "Fleet"),
    ("needs", "game/needs.md", "Fleet"),                     # what a need is and how one is added (needs.py: the register itself)
    ("handbook", "game/handbook.md", "Fleet"), ("handbook", "game/handbook/*.md", "Fleet"),    # the store's handbook (scripts/handbook.py)
    ("plan", "data/plans/plan-*.md", ""),
    ("report", "reports/*.md", ""),
) + tuple(("log", pattern % name, "*") for name in LOGS for pattern in ("communications/archive/%s-*.log", "communications/%s.log")) + (
    ("member", "data/docs/members/**/*.md", ""),               # docs_export.py's copies of each member's own files
)
ORDER = list(dict.fromkeys(kind for kind, _pattern, _owner in KINDS))
DATA_PREFIX = "data/"          # a KINDS path in the unit's data folder, not the repository
LEDGER = ("plan", "report", "log", "member")     # what the members write as they work: the briefing lists it one line a file
BASELINE = "docs.baseline."    # meta key of a kind's first loading (counts as no change), + the kind
MISSION_MARK = "<!-- MISSION"  # COLLECTIVE.md: above it the part every member's copy shares, below it the member's own mission
REPORT_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}_([a-z]+)_")
LOG_ENTRY = re.compile(r"^## \[ENT-(\d+)\]")
LOG_ARCHIVE = re.compile(r"^communications/archive/([a-z]+)-\d{4}-\d{2}-\d{2}\.log$")
SLUG = 60                      # characters of one part of a section id
LIST_ROWS = 150                # sections `docs` lists by title; more, and it lists the files only
TEXT_CHARS = 25000             # characters of text `docs` prints at most (an answer of the MCP tools is cut at 30,000)
BRIEF_ROWS = 30                # lines of the briefing's section, at most
KEEP_EVERY = 900               # seconds: last_seen of the versions that stand is moved on at a pass that changed a section, else this often
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
    """(kind, owner) of a repository path (`data/...`: of the data folder); ('', '') for a file that is no source. A log
    has no one owner: ('log', ''), each entry's is its author's (entry_owner)."""
    rel = str(rel).replace(os.sep, "/")
    for kind, pattern, owner in KINDS:
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(rel, "*/" + pattern):
            if owner == "*":
                return kind, ""
            return kind, owner or owner_of(kind, rel)
    return "", ""


def division_name(word):
    """The division's name of a member's or a division's name (any case): `zero` and `mining` -> Mining; another word
    as it stands, titled."""
    member = member_of(word)
    return board.NAMES.get(member, member) if member else str(word or "").strip().title()


def owner_of(kind, rel):
    """The owner of a file whose KINDS row names none: the division its name or folder names (guidebook/mining.md,
    plan-mining.md, a report `<date>_zero_<slug>.md`, members/zero/...)."""
    parts = str(rel).split("/")
    stem = Path(rel).stem.lower()
    if kind == "report":
        found = REPORT_NAME.match(parts[-1])
        stem = found.group(1) if found else stem
    elif kind == "member" and "members" in parts[:-2]:
        stem = parts[parts.index("members") + 1]
    elif kind == "plan" and stem.startswith("plan-"):
        stem = stem[len("plan-"):]
    elif kind == "guide":                          # game/routes/guidebook/<division>/<chapter>.md: its folder names the division
        stem = parts[-2]
    return division_name(stem)


def entry_owner(head):
    """The owner of a log entry by its head line: its author's division (a name that is no member's stands as written)."""
    found = ENTRY.match(head or "")
    return division_name(found.group(3)) if found else ""


def doc_path(rel, kind):
    """The path a source's sections stand under in the table docs: an archived log's entries under their log's own
    path (CI moves the oldest entries to communications/archive/<log>-<date>.log: they stay the same sections)."""
    found = LOG_ARCHIVE.match(rel) if kind == "log" else None
    return "communications/%s.log" % found.group(1) if found else rel


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


def parse_log(text):
    """[(ENT-NNN, its head line, its body)] of a log: one section an entry (communications/protocol.md), in the log's
    order. The file's comment blocks (`<!-- ... -->` from a line's start: the head of a log or an archive, CI's
    `Appended ...` lines between archived entries) belong to no entry, so an entry has one text in its log and in its
    archive; what stands before the first entry is no section."""
    entries, comment, out, seen = [], False, [], {}
    for line in text.splitlines():
        if comment or line.startswith("<!--"):
            comment = "-->" not in line
            continue
        found = LOG_ENTRY.match(line)
        if found:
            entries.append(["ENT-" + found.group(1), line.rstrip(), []])
        elif entries:
            entries[-1][2].append(line.rstrip())
    for sid, head, body in entries:
        seen[sid] = seen.get(sid, 0) + 1
        out.append((sid if seen[sid] == 1 else "%s-%d" % (sid, seen[sid]), head, "\n".join(body).strip("\n")))
    return out


def parse_collective(text, whole):
    """A member's COLLECTIVE.md: the part below the MISSION mark is one section `mission` (titled by its first
    heading); the part above it, which every member's copy shares, only when `whole` (Unity's copy, the master), so
    that it stands once in the store."""
    lines = text.splitlines()
    at = next((n for n, line in enumerate(lines) if line.lstrip().startswith(MISSION_MARK)), None)
    if at is None:
        return parse_markdown(text)
    below = "\n".join(lines[at + 1:]).strip("\n")
    title = next((HEADING.match(line).group(2).strip() for line in lines[at + 1:] if HEADING.match(line)), "the member's own mission")
    return (parse_markdown("\n".join(lines[:at])) if whole else []) + ([("mission", title, below)] if below.strip() else [])


def parse(path, kind=None):
    """[(section id, title, text)] of one source file, by its kind (from its path when not given)."""
    kind = kind or kind_of(Path(path).resolve().as_posix())[0]
    with open(path, "rb") as handle:
        text = handle.read().decode("utf-8", errors="replace")
    if kind == "template":
        return parse_templates(text)
    if kind == "orders":
        return parse_orders(text)
    if kind == "log":
        return parse_log(text)
    if kind == "member" and Path(path).name == "COLLECTIVE.md":
        return parse_collective(text, Path(path).parent.name.lower() == "unity")
    if kind == "guide":                            # a guidebook's chapter: one section an entry (guidebook.py)
        return __import__("guidebook").sections(text, Path(path).stem)
    return parse_markdown(text, "F" if kind == "rulebook" else "table" if kind == "rules" else "")


def sha(title, text):
    return hashlib.sha1(("%s\n%s" % (title, text)).encode("utf-8")).hexdigest()


# ---- the store's side: the files, one file's rows, the history

def sources(repo, data=None):
    """[(source name, path, kind, owner)] of every source file that exists, in the order of KINDS: the source name is the
    repository path, `data/<path>` for a file of the data folder (none without `data`). Dot files are no source; a
    member's file lies in a member's folder (data/docs/members/<member>/...)."""
    out = []
    for kind, pattern, _owner in KINDS:
        if pattern.startswith(DATA_PREFIX) and data is None:
            continue
        base, inner, prefix = (Path(data), pattern[len(DATA_PREFIX):], DATA_PREFIX) if pattern.startswith(DATA_PREFIX) else (Path(repo), pattern, "")
        for path in sorted(base.glob(inner)):
            rel = prefix + path.relative_to(base).as_posix()
            if path.is_file() and not path.name.startswith(".") and (kind != "member" or len(path.relative_to(base).parts) > 3):
                out.append((rel, path, kind, kind_of(rel)[1]))
    return out


def files(data, root):
    """The store's loader: [(source name, path, reader, required, note)]; the source name is the repository path, or
    data/<path> for a plan or a member's file in the data folder."""
    repo = Path(root).resolve().parent
    return [(rel, path, read, False, "") for rel, path, _kind, _owner in sources(repo, data)]


def source_name(path, ctx):
    """A file's source name: its repository path, else data/<its path in the data folder>."""
    path = Path(path).resolve()
    for base, prefix in ((Path(ctx["root"]).resolve().parent, ""), (Path(ctx.get("data") or "/nonexistent").resolve(), DATA_PREFIX)):
        try:
            return prefix + path.relative_to(base).as_posix()
        except ValueError:
            continue
    return path.as_posix()


def read(path, ctx):
    """One source file -> {docs: [rows]} (store.py's reader form). A log's entry stands at n = its ENT number (an
    archive and its log share one path) and is owned by its author's division."""
    rel = source_name(path, ctx)
    kind, owner = kind_of(rel)
    where = doc_path(rel, kind)
    mtime = int(os.stat(path).st_mtime)
    rows = []
    for n, (sid, title, text) in enumerate(parse(path, kind), 1):
        if kind == "log":
            n, owner = (int(sid[4:].split("-")[0]) if sid.startswith("ENT-") else 0), entry_owner(title)
        rows.append({"path": where, "kind": kind, "owner": owner, "section": sid, "n": n, "title": title, "text": text,
                     "sha": sha(title, text), "chars": len(text), "t": mtime})
    return {"docs": rows}


def meta_of(conn, key):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def mark_baselines(conn, now, kinds, newest):
    """meta docs.baseline.<kind>: the pass that first loads a kind with no version on record is that kind's baseline, and
    what it loads counts as no change (a kind added to a store that has run for days: thousands of log entries and
    reports would read as new once). A kind whose versions came before these marks takes 0: docs.baseline counts."""
    todo = [kind for kind in sorted(k for k in kinds if k) if meta_of(conn, BASELINE + kind) is None]
    if todo:
        recorded = {kind_of(path)[0] for path in {path for path, _section in newest}}
        conn.executemany("INSERT OR REPLACE INTO meta VALUES (?, ?)", [(BASELINE + kind, 0 if kind in recorded else int(now)) for kind in todo])


def baselines(conn):
    """{kind: its baseline}, from the meta marks."""
    return {key[len(BASELINE):]: int(value or 0) for key, value in conn.execute("SELECT key, value FROM meta WHERE key LIKE ?", (BASELINE + "%",))}


def keep(conn, now, problems=None):
    """The history of every section (doc_versions), after the snapshot loaded the table docs: a new row for each section
    whose sha is not its newest version's; a version that stopped standing in this pass (its section got a new text or
    left) takes last_seen = the pass before (meta docs.pass), the last one in which it stood; the versions that stand
    take last_seen = now at a pass that changed a section, else every KEEP_EVERY seconds (meta docs.refreshed), not at
    every pass: rewriting thousands of rows a minute said nothing new. One transaction; a fault is returned, never
    raised (the next pass compares again), and named in `problems` (the snapshot's, which the pass's line prints):
    {added, standing, left, error}."""
    now, out = int(now), {"added": 0, "standing": 0, "left": 0, "error": None}
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'docs'").fetchone():
            return out
        conn.execute("BEGIN IMMEDIATE")
        try:
            newest = {(path, section): (version, digest) for path, section, version, digest in
                      conn.execute("SELECT path, section, MAX(version), sha FROM doc_versions GROUP BY path, section")}
            standing, fresh, kinds, present = [], [], set(), set()
            for path, section, digest, kind in conn.execute("SELECT path, section, sha, kind FROM docs"):
                present.add((path, section))
                old = newest.get((path, section))
                if old and old[1] == digest:
                    standing.append(old[0])
                else:
                    fresh.append((path, section))
                    kinds.add(kind)
            if fresh and not newest and meta_of(conn, "docs.baseline") is None:
                conn.execute("INSERT OR REPLACE INTO meta VALUES ('docs.baseline', ?)", (now,))
            mark_baselines(conn, now, kinds, newest)
            before, refreshed = int(meta_of(conn, "docs.pass") or 0), int(meta_of(conn, "docs.refreshed") or 0)
            ended = [newest[key][0] for key in fresh if key in newest] + [version for key, (version, _digest) in newest.items() if key not in present]
            left = []
            for start in range(0, len(ended), 500):                # a version that stood until the last pass: its last_seen >= the last refresh
                chunk = ended[start:start + 500]
                left += [v for (v,) in conn.execute("SELECT version FROM doc_versions WHERE version IN (%s) AND last_seen >= ?" % ",".join("?" * len(chunk)),
                                                    chunk + [refreshed])]
            if before:                                             # before the first pass of this rule every standing version was moved on at each pass
                conn.executemany("UPDATE doc_versions SET last_seen = ? WHERE version = ?", [(before, v) for v in left])
            for path, section in fresh:
                conn.execute("INSERT INTO doc_versions (path, section, sha, title, text, first_seen, last_seen) "
                             "SELECT path, section, sha, title, text, ?, ? FROM docs WHERE path = ? AND section = ?", (now, now, path, section))
            if fresh or left or now - refreshed >= KEEP_EVERY:
                conn.executemany("UPDATE doc_versions SET last_seen = ? WHERE version = ? AND last_seen < ?", [(now, v, now) for v in standing])
                conn.execute("INSERT OR REPLACE INTO meta VALUES ('docs.refreshed', ?)", (now,))
            conn.execute("INSERT OR REPLACE INTO meta VALUES ('docs.pass', ?)", (now,))
            conn.execute("COMMIT")
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        out.update(added=len(fresh), standing=len(standing), left=len(left))
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


def owner_line(rows):
    """The owner of a file's rows, or `each` when they have several (a log: each entry its author's)."""
    owners = {r[2] for r in rows}
    return rows[0][2] if len(owners) == 1 else "each"


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
        print("DOCS%s | the fleet's written knowledge by section, mirrored from the repository and the data folder by the store (table docs; every "
              "version: doc_versions) | %d files, %d sections, matched as %s | %s" % (" " + what if what else "", len(by_file), len(picked), how, copy_line(data, now)))
        if not what or (len(picked) > LIST_ROWS and len(by_file) > 1):
            print("  %-44s %-9s %-9s %8s %9s  %s" % ("file", "kind", "owner", "sections", "chars", "file changed"))
            folded = {}
            for path, its in by_file.items():
                if not what and its[0][1] in ("report", "member"):          # many files: one line a kind, its files by `hive.py docs <kind>`
                    folded.setdefault(its[0][1], []).append(its)
                    continue
                print("  %-44s %-9s %-9s %8d %9s  %s" % (path, its[0][1], owner_line(its), len(its), num(sum(r[6] or 0 for r in its)), stamp(max(r[8] or 0 for r in its))))
            for kind, groups in folded.items():
                print("  %-44s %-9s %-9s %8d %9s  %s" % ("%d files (hive.py docs %s)" % (len(groups), kind), kind, "each", sum(len(g) for g in groups),
                                                        num(sum(r[6] or 0 for g in groups for r in g)), stamp(max(r[8] or 0 for g in groups for r in g))))
            print("  a file's sections by title: hive.py docs <file|kind|owner>; one section: --section <id>; a word: --grep <word>; "
                  "what changed: hive.py changes; what a division does: hive.py division <name>")
            return 0
        for path, its in by_file.items():
            shown = its[-LIST_ROWS:]                                      # a log: its newest entries
            print("%s | %s, %s | %d sections%s, %s chars | file changed %s" % (path, its[0][1], owner_line(its), len(its), "" if len(shown) == len(its) else
                                                                                ", the last %d listed" % len(shown), num(sum(r[6] or 0 for r in its)), stamp(max(r[8] or 0 for r in its))))
            print("  %7s  %-50s  %s" % ("chars", "section", "title"))
            for r in shown:
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
    out, marks = [], baselines(conn)
    for path, section, title, chars, first, last, stands, n, kind, owner, count in rows:
        if not stands:
            kind, owner = kind_of(path)
            owner = owner or entry_owner(title)
        elif first <= marks.get(kind, 0):                          # loaded by its kind's first pass: no change
            continue
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


def ledger_lines(conn, rows):
    """The changed rows of the members' writing (LEDGER kinds) in short, titles and sizes, never whole texts: one line a
    claim of admirals.log (its `Claims:` line cut), then one line a file: a plan, a report, a member's file (its
    sections changed, its size; a report's title when it is new), a log (its new entries counted by author)."""
    sizes = {path: (count, chars or 0) for path, count, chars in
             conn.execute("SELECT path, COUNT(*), SUM(chars) FROM docs WHERE kind IN (%s) GROUP BY path" % ", ".join("?" * len(LEDGER)), LEDGER)}
    claims, files = [], {}
    for row in rows:
        status, path, section, title, _chars, when, kind, owner = row
        files.setdefault(path, []).append(row)
        head = ENTRY.match(title or "")
        if kind == "log" and status != "gone" and head and head.group(4) == "claim":
            text = (conn.execute("SELECT text FROM docs WHERE path = ? AND section = ?", (path, section)).fetchone() or ("",))[0] or ""
            said = next((line[len("Claims:"):].strip() for line in text.splitlines() if line.startswith("Claims:")), "")
            claims.append("  claim %s %s UTC by %s (%s): %s" % (section, head.group(2)[5:], head.group(3), owner,
                                                               said[:100] + ("..." if len(said) > 100 else "") if said else "(no Claims: line)"))
    lines = list(claims)
    for kind in ("plan", "report", "member", "log"):
        for path, its in files.items():
            if its[0][6] != kind:
                continue
            count, chars = sizes.get(path, (0, 0))
            if kind == "log":
                new = [r for r in its if r[0] != "gone"]
                ids = sorted(int(r[2][4:].split("-")[0]) for r in new if r[2].startswith("ENT-"))
                authors = {}
                for r in new:
                    found = ENTRY.match(r[3] or "")
                    authors[found.group(3) if found else "?"] = authors.get(found.group(3) if found else "?", 0) + 1
                lines.append("  %-40s %d new %s%s, by %s%s" % (path, len(new), "entry" if len(new) == 1 else "entries", " (ENT-%03d to ENT-%03d)" % (ids[0], ids[-1]) if ids else "",
                                                                    ", ".join("%s %d" % pair for pair in sorted(authors.items(), key=lambda p: (-p[1], p[0]))) or "--",
                                                                    "; %d left the log" % (len(its) - len(new)) if len(its) > len(new) else ""))
                continue
            if all(r[0] == "new" for r in its) and len(its) == count:
                top = (conn.execute("SELECT title FROM docs WHERE path = ? ORDER BY n LIMIT 1", (path,)).fetchone() or ("",))[0] or ""
                what = "new, %d sections: %s" % (count, top[:70])
            else:
                ids = [r[2] for r in its]
                what = "%d of %d sections %s (%s%s)" % (len(its), count, "gone" if all(r[0] == "gone" for r in its) else "changed",
                                                       ", ".join(ids[:4])[:80], ", ..." if len(ids) > 4 else "")
            lines.append("  %-40s %-9s %s; %s chars" % (path, its[0][7], what, num(chars)))
    return lines


ROLE_KINDS = ("guide", "guidebook", "template")     # the rules of a division's role, which the briefing counts for its own member


def briefing(root, data, now, who):
    """The briefing's section: what changed since the member's last turn, at most BRIEF_ROWS lines: the rules and the
    orders one line a section, the other divisions' plans, reports, claims, logs and members' files one line a file
    (ledger_lines); the member's own division's guidebook and templates (the rules of its role) are counted, not
    listed, and its own writing is left out."""
    member = who if who in division.MEMBERS else "Unity"
    own = {board.NAMES.get(member, member)}                       # its division: its guidebook and its templates
    print("=== CHANGED SINCE YOUR LAST TURN (the rulebook rule by rule, the orders block by block, strategy, empire, guidebooks, templates, "
          "game rules, metrics: one line a section; the other divisions' plans, reports, claims, logs and members' files: one line a file; "
          "`hive.py changes` lists every section)")
    try:
        t, basis = resolve_since(Path(root).resolve().parent, now, None, member)
        conn, why = open_copy(data)
        if conn is None:
            print("  not read: " + why)
            return
        try:
            rows, _baseline = changed(conn, t)
            mine = [r for r in rows_of(conn) if r[2] in own and r[1] in ROLE_KINDS]
            others = [r for r in rows if r[7] not in own]
            ledger = ledger_lines(conn, [r for r in others if r[6] in LEDGER])
        finally:
            conn.close()
    except (OSError, sqlite3.Error, ValueError) as error:
        print("  not read: %s: %s" % (type(error).__name__, error))
        return
    rules = [r for r in others if r[6] not in LEDGER]
    ours = [r for r in rows if r[7] in own and r[6] in ROLE_KINDS]
    print("  since %s (%s): %d sections changed, %d of them of other owners: %d of the rules and orders, one line each; the members' writing in %d lines"
          % (stamp(t), basis, len(rows), len(others), len(rules), len(ledger)))
    room = BRIEF_ROWS - 6
    take_rules = min(len(rules), max(room - len(ledger), room // 2))
    take_ledger = min(len(ledger), room - take_rules)
    more = "hive.py changes" + ("" if member == "Unity" else " --member " + member)
    for row in rules[:take_rules]:
        print(change_line(row))
    if len(rules) > take_rules:
        print("  ... %d more sections of the rules and orders: %s" % (len(rules) - take_rules, more))
    for line in ledger[:take_ledger]:
        print(line)
    if len(ledger) > take_ledger:
        print("  ... %d more lines of the members' writing: %s" % (len(ledger) - take_ledger, more))
    if others:
        print("  one section whole: hive.py docs <file> --section <id> (the tool docs, view=section); what changed in it: add --history; "
              "what a division does: hive.py division <name> (view=division)")
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
