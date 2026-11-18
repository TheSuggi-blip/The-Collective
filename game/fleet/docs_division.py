#!/usr/bin/env python3
"""docs_division.py -- what each Admiral is doing, in one short block per division, from the store alone: its mission, its block of the orders in force, its plan, its guidebook's sections, its last session entry, the requests open to and from it, and its claims in force.

WHAT: `hive.py division <name|all>` and the MCP tool docs (view=division) print it. It reads the store's read copy
      only (the tables docs and doc_versions, which docs.py fills from the files at every pass), one block a division
      under LIMIT characters:
        MISSION      the member's own mission: its MISSION.md whole (copied into the data folder by docs_export.py),
                     cut only when the block would pass LIMIT; while a member has none yet, the part below the MISSION
                     mark of its old COLLECTIVE.md (the section `mission`)
        ORDERS       its block of the newest entry of communications/orders.log: its order and its Measure
        PLAN         its plan file data/plans/plan-<division>.md: the lists First and Then, and the own routes of its
                     ships with how many ships have each (plan.py's parser; a template `@<name>` is expanded by the
                     division's templates as the store holds them, and counted by itself too)
        GUIDEBOOK    game/routes/guidebook/<division>/: each chapter with its entries and characters, OVER its cap,
                     and when it last changed (guidebook.py); a guidebook not split yet (<division>.md): each top
                     section with its characters (its parts added) and when its text last changed
        LAST REPORT  its newest session entry in communications/reports.log (the archive too): Session, Did, Worked,
                     Failed, each line cut
        REQUESTS     the requests not closed that are addressed to it or that it wrote (comms.py's states)
        CLAIMS       its claims in admirals.log in force (comms.py: younger than CLAIM_HOURS, not released)
RULES:
  - The store only: no file of the repository or the data folder is read, no ship's state. A part the store does not
    hold says so (`not in the store: ...`), never filled in.
  - One parser per thing: comms.py's for the entries (request states, claims in force), plan.py's for the plan file,
    docs.py's for names and owners. No ship of ours is named: a plan is shown as route ids with counts.
  - Each line is cut to its share; the block says where each part stands whole (hive.py docs ... --section ...).
WHY:  Suggi, 2026-11-18: everything in the database, so that the other agents know what the other Admirals are doing
      and everyone can know everything. One answer per division instead of six files and four logs read by hand.

USAGE:
  docs_division.py [<Member>|<division>|all] [--data <dir>] [--root <dir>]
  --data <dir>   the unit's data folder (default: the fleet's)
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import importlib.util
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names
import division                                   # noqa: E402  the members, the data folder
import docs as writings                           # noqa: E402  the store's read copy, names, owners, stamps

LIMIT = 4000                   # characters of one division's block, at most (its lines and their line ends)
MISSION_LEAST = 300            # characters of the mission kept when the other parts leave less room
CUT = {"order": 320, "measure": 190, "first": 120, "then": 120, "own": 200, "templates": 100, "guide": 330,
       "session": 100, "did": 150, "worked": 80, "failed": 80, "request": 92, "claim": 120}
REQUEST_ROWS = 2               # requests listed each way (to it, from it), the newest; the rest counted
CLAIM_ROWS = 2


def clip(text, size):
    """One line of at most `size` characters: its whitespace folded, a cut said with `...`."""
    line = " ".join(str(text or "").split())
    return line if len(line) <= size else line[:max(size - 3, 0)].rstrip() + "..."


def short(t):
    return time.strftime("%m-%d %H:%M", time.gmtime(t)) if t else "--"


def load_comms():
    """scripts/comms.py beside this script's repository (its parser of the logs' entries), loaded by its path."""
    path = Path(__file__).resolve().parents[2] / "scripts" / "comms.py"
    spec = importlib.util.spec_from_file_location("comms_of_division", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def entries(conn, comms, log):
    """The entries of one log as comms.parse gives them, rebuilt from the store's sections (head line, body)."""
    rows = conn.execute("SELECT title, text FROM docs WHERE path = ? AND kind = 'log' ORDER BY n", ("communications/%s.log" % log,)).fetchall()
    found, _errors = comms.parse("\n\n".join("%s\n%s" % (title, text or "") for title, text in rows))
    return found


def section(conn, path, sid):
    return conn.execute("SELECT title, text, chars, t FROM docs WHERE path = ? AND section = ?", (path, sid)).fetchone()


def mission_part(conn, member, room):
    """The member's MISSION.md whole, its lines as they stand, when it fits in `room` characters, else folded and cut;
    while it has none, the section `mission` of its old COLLECTIVE.md."""
    folder = "data/docs/members/%s/" % member.lower()
    rows = conn.execute("SELECT title, text, t FROM docs WHERE path = ? ORDER BY n", (folder + "MISSION.md",)).fetchall()
    path, where = folder + "MISSION.md", "hive.py docs %sMISSION.md" % folder
    if not rows:
        row = section(conn, folder + "COLLECTIVE.md", "mission")
        rows = [row[:2] + row[3:]] if row else []
        path, where = folder + "COLLECTIVE.md, below its MISSION mark", "hive.py docs %sCOLLECTIVE.md --section mission" % folder
    if not rows:
        return ["MISSION | not in the store: no %sMISSION.md (docs_export.py copies it into the data folder; the store loads it at its "
                "next pass)" % folder]
    lines = [line.rstrip() for text in (r[1] or "" for r in rows) for line in text.splitlines() if line.strip()]
    head = "MISSION (%s, file of %s)" % (path, short(max(r[2] or 0 for r in rows)))
    body = ["  " + line for line in lines]
    if len(head) + sum(len(line) + 1 for line in body) <= room:
        return [head] + body
    head = "MISSION (%s, file of %s; cut, whole: %s)" % (path, short(max(r[2] or 0 for r in rows)), where)
    return [head, "  " + clip(" ".join(lines), max(room - len(head) - 4, MISSION_LEAST))]     # 4: the indent and two line ends


def orders_part(conn, member):
    path, sid = "communications/orders.log", member.lower()
    row, head = section(conn, path, sid), section(conn, path, "head")
    if row is None:
        return ["ORDERS | not in the store: no block `%s` in the newest entry of %s" % (sid, path)]
    when = head[0].split(": the entry's head")[0] if head else "the newest entry"
    lines = (row[1] or "").splitlines()
    measure = [line for line in lines[1:] if line.startswith("Measure:")]
    others = [line for line in lines[1:] if not line.startswith("Measure:")]
    out = ["ORDERS (orders.log %s, block %s, %s chars; whole: hive.py docs orders.log --section %s)" % (when, sid, writings.num(row[2]), sid),
           "  " + clip(lines[0] if lines else "", 90)]
    if others:
        out.append("  " + clip(" ".join(others), CUT["order"]))
    out += ["  " + clip(line, CUT["measure"]) for line in measure[:1]]
    return out


def plan_part(conn, name):
    """First and Then, the routes the ships' cells name with how many ships name each, and the templates the same way
    (the number of routes each expands to from the division's templates in the store)."""
    import plan as plans                          # plan.py's parser of a plan file: only this part needs it
    path = "data/plans/plan-%s.md" % name.lower()
    rows = conn.execute("SELECT text, t FROM docs WHERE path = ? ORDER BY n", (path,)).fetchall()
    if not rows:
        return ["PLAN | not in the store: no %s (a division without a file flies its role's plan)" % path]
    found = plans.parse("\n\n".join(text or "" for text, _t in rows))
    kit = {}
    for sid, text in conn.execute("SELECT section, text FROM docs WHERE path = ?", ("game/routes/templates/%s.json" % name.lower(),)):
        try:
            body = json.loads(text or "{}")
        except ValueError:
            continue
        kit[sid] = body if isinstance(body, dict) else {}
    found["templates"] = kit
    named, flown = Counter(), set()
    for ship, words in found["ships"].items():
        named.update(words)
        flown.update(plans.expand(found, ship))
    routes = sorted(((w, n) for w, n in named.items() if not w.startswith("@")), key=lambda p: (-p[1], p[0]))
    kits = sorted(((w, n) for w, n in named.items() if w.startswith("@")), key=lambda p: (-p[1], p[0]))
    size = lambda word: len((kit.get(word[1:]) or {}).get("routes") or [])
    return ["PLAN (%s, file of %s; whole: hive.py docs plan-%s.md): %d ships in its table, %d routes First, %d Then, %d own routes with the "
            "templates expanded" % (path, short(max(t or 0 for _text, t in rows)), name.lower(), len(found["ships"]), len(found["first"]),
                                    len(found["then"]), len(flown)),
            "  First: " + clip(", ".join(found["first"]) or "--", CUT["first"]),
            "  Then: " + clip(", ".join(found["then"]) or "--", CUT["then"]),
            "  Routes in the ships' cells, ships naming each: " + clip(", ".join("%s %d" % p for p in routes) or "--", CUT["own"]),
            "  Templates, ships naming each (its routes): " + clip(", ".join("%s %d (%d)" % (w, n, size(w)) for w, n in kits) or "--", CUT["templates"])]


def guide_part(conn, name):
    found = __import__("guidebook").division_part(conn, name, clip, CUT["guide"])      # its chapters (guidebook.py), when the store holds them
    if found:
        return found
    path = "game/routes/guidebook/%s.md" % name.lower()
    rows = conn.execute("SELECT section, chars, sha FROM docs WHERE path = ? ORDER BY n", (path,)).fetchall()
    if not rows:
        return ["GUIDEBOOK | not in the store: no %s" % path]
    since = {}
    for sid, digest, first in conn.execute("SELECT section, sha, first_seen FROM doc_versions WHERE path = ?", (path,)):
        since[(sid, digest)] = max(since.get((sid, digest), 0), first)
    first_reading = max(int(writings.meta_of(conn, "docs.baseline") or 0), writings.baselines(conn).get("guidebook", 0))
    tops = {}
    for sid, chars, digest in rows:
        top = sid.split("/")[0]
        item = tops.setdefault(top, [0, 0, 0])
        item[0] += chars or 0
        item[1] += 0 if top == sid else 1
        item[2] = max(item[2], since.get((sid, digest), 0))
    items = ["%s %s%s %s%s" % (top[:28], writings.num(chars), "(+%d)" % parts if parts else "", short(when), "*" if when and when <= first_reading else "")
             for top, (chars, parts, when) in tops.items()]
    return ["GUIDEBOOK (%s, %d sections, %s chars; top sections: chars, (+parts), last change, * since the first reading %s)"
            % (path, len(rows), writings.num(sum(r[1] or 0 for r in rows)), short(first_reading)),
            "  " + clip(", ".join(items), CUT["guide"])]


def report_part(conn, comms, member):
    mine = [e for e in entries(conn, comms, "reports") if e["by"] == member and e["category"] == "session"]
    if not mine:
        return ["LAST REPORT | not in the store: no session entry of %s in communications/reports.log" % member]
    last = mine[-1]
    out = ["LAST REPORT (reports.log ENT-%03d of %s UTC; %s)" % (last["num"], last["when"], clip(last["ref"] or "no ref", 90))]
    for label in ("Session", "Did", "Worked", "Failed"):
        out.append("  %s: %s" % (label, clip(comms.field(last, label) or "--", CUT[label.lower()])))
    return out


def requests_part(conn, comms, member):
    states = [r for r in comms.request_states(entries(conn, comms, "requests")) if r[0] != "CLOSED"]
    to = [r for r in states if comms.addressed(r[1], member) and r[1]["by"] != member]
    of = [r for r in states if r[1]["by"] == member]
    out = ["REQUESTS not closed: %d to %s, %d from it, the newest listed (all: comms.py requests --to %s)" % (len(to), member, len(of), member)]
    for rows, word in ((to, "from"), (of, "to")):
        for state, request, _answer in rows[-REQUEST_ROWS:]:
            other = request["by"] if word == "from" else comms.field(request, "To").rstrip(".")
            out.append("  " + clip("ENT-%03d %s %s %s %s: %s" % (request["num"], state, request["when"][5:], word, other, comms.field(request, "Need")), CUT["request"]))
    return out


def claims_part(conn, comms, member, now):
    claims = [e for e in comms.claims_in_force(entries(conn, comms, "admirals"), now) if e["by"] == member]
    out = ["CLAIMS in force (admirals.log, %d hours from the entry, not released): %d" % (comms.CLAIM_HOURS, len(claims))]
    for entry in claims[-CLAIM_ROWS:]:
        out.append("  " + clip("ENT-%03d %s UTC: %s" % (entry["num"], entry["when"][5:], comms.line_of(entry, "Claims")), CUT["claim"]))
    if len(claims) > CLAIM_ROWS:
        out.append("  ... %d older" % (len(claims) - CLAIM_ROWS))
    return out


def block(conn, comms, member, now):
    """One division's block as lines, under LIMIT characters with their line ends: every part but the mission at its
    own cut, the mission in the room left (whole when it fits)."""
    name = board.NAMES.get(member, member)
    rest = []
    for part in (lambda: orders_part(conn, member), lambda: plan_part(conn, name), lambda: guide_part(conn, name),
                 lambda: report_part(conn, comms, member), lambda: requests_part(conn, comms, member), lambda: claims_part(conn, comms, member, now)):
        try:
            rest += part()
        except (ValueError, KeyError, TypeError, AttributeError) as error:   # one part that fails is said; the others stand
            rest.append("  a part not read: %s: %s" % (type(error).__name__, error))
    head = "DIVISION %s (%s)" % (name, member)
    room = LIMIT - 48 - len(head) - 1 - sum(len(line) + 1 for line in rest)      # 48: the room of the cut line, never needed then
    try:
        mission = mission_part(conn, member, room)
    except (ValueError, KeyError, TypeError, AttributeError) as error:
        mission = ["MISSION | not read: %s: %s" % (type(error).__name__, error)]
    out, size = [], 0
    for line in [head] + mission + rest:
        tail = "... cut at %d characters (LIMIT)" % size
        if size + len(line) + 1 + len(tail) + 1 >= LIMIT:
            out.append(tail)
            break
        out.append(line)
        size += len(line) + 1
    return out


def show(root, data, now, who):
    """hive.py division: one division's block, or every division's (all)."""
    names = list(division.MEMBERS) if str(who or "all").lower() == "all" else [writings.member_of(who)]
    if names == [None]:
        print("DIVISION | no member or division `%s`: %s, or all" % (who, ", ".join("%s (%s)" % (m, board.NAMES.get(m, m)) for m in division.MEMBERS)))
        return 1
    conn, why = writings.open_copy(data)
    if conn is None:
        print("DIVISION | " + why)
        return 1
    try:
        comms = load_comms()
        print("DIVISION | what each Admiral is doing, from the store alone (docs, doc_versions) | %s" % writings.copy_line(data, now))
        for member in names:
            print("\n".join(block(conn, comms, member, now)))
    finally:
        conn.close()
    return 0


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--data", "--root"))]
    if any(a in ("-h", "--help") for a in args) or len(words) > 1:
        sys.exit(__doc__)
    here = Path(__file__).resolve().parent
    return show(value("--root", str(here.parent)), value("--data", division.DATA), time.time(), words[0] if words else "all")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
