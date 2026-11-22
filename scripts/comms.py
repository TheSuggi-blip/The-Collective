#!/usr/bin/env python3
"""comms.py -- read the fleet's logs: the orders in force, the requests and their state, the last session entries.

WHAT: communications/ holds the append-only logs of The Collective
      (communications/protocol.md). This script answers, without AI, what a
      member asks of them at session start:
        orders     the newest entry of orders.log: the orders in force, complete
        requests   the requests of requests.log by state: OPEN (no answer yet),
                   ACCEPTED (the last answer says yes) and, with --all, CLOSED
                   (the last answer says done or no); a request not closed whose
                   newest entry (the request, or its last answer) is older than
                   STALE_DAYS (3) is marked STALE and counted
        digest     the last session entries of each member from reports.log and
                   the requests not closed: the record a summary of the
                   divisions is written from
        check      the gate of the three logs' rules
        admirals   the Admirals' own log (admirals.log): the claims in force
                   and its last entries
      and it is the one way an entry is written to any log:
        append     appends one prepared entry under a lock: it sets the entry's
                   number and time, puts exactly one blank line before it, runs
                   the gate and commits the log by path under the writer's name
RULES (append):
  - the entry file starts `## [ENT-NEXT] | NOW | <Name> | <category>`, with
    ` | ref: ...` and ` | see: ...` after it where they apply; the body follows;
  - <Name> is the writer given with --as; orders.log takes entries of Unity only;
  - the category belongs to the log: order (orders), session (reports), request
    or answer (requests), general (queue), error (errors), note or claim
    (admirals); a claim carries a `Claims:` line and is refused when another member's claim in force names one of
    its routes (standing work excepted);
  - the entry file lies outside the repository: an untracked file in the
    working copy holds every member's push;
  - an entry that breaks the gate is taken out again and nothing is committed.
RULES (check):
  - a header has the protocol's form, and the ENT numbers of a log rise by one;
  - orders.log: written by Unity only, category `order`, with a `Changed:` line
    and an `In force` line;
  - orders.log, its newest entry only (an older entry is history): the whole
    entry at most ENTRY_CHARS characters, Suggi's standing orders and goals
    included; the `Changed:` line at most CHANGED_WORDS words; PLAN, from the line
    after its heading to the first member block, at most PLAN_WORDS; each member's
    block (`UNITY, ...` to the next block heading), its heading line not counted,
    at most BLOCK_WORDS. A word is a run of characters between spaces; Suggi's
    standing orders and goals are no part of a word count (Suggi, 2026-11-18:
    lean orders);
  - reports.log: category `session`, with the lines Session, Did, Worked,
    Failed, Requests, Suggestions and Report;
  - requests.log: a `request` has a `To:` and a `Need:` line; an `answer` names
    a request of this log in `see:` and its `Answer:` line starts with yes, no
    or done.
RULES (requests):
  - STALE is a mark, never a state: no machine closes a request. Only an
    answer (yes, no or done) moves it; a stale one is answered or closed by its
    members (Suggi, 2026-11-22: nothing piles up forever).
WHY:  an order that has to be searched for is guessed, and a request without a
      state is lost. The newest order and the open requests are one command
      away for every member, and the board of requests is computed from the
      log instead of kept by hand. Six members write the same logs in one
      working copy: a number read and an entry appended by hand collide, so
      the append is one locked step.

USAGE:
  comms.py orders
  comms.py requests [--to NAME] [--from NAME] [--all]
  comms.py digest [--last N] [--member NAME]
  comms.py check
  comms.py admirals [--last N] [--member NAME]
  comms.py append <orders|reports|requests|queue|errors|admirals> <entry file> --as <Name>
  --root <dir>   repository root (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import argparse
import calendar
import fcntl
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HEADER = re.compile(r"^## \[ENT-(\d{3,})\] \| (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC \| ([A-Za-z][A-Za-z0-9_-]*) \| ([a-z]+)((?: \| (?:ref|see): [^|]+)*)$")
SESSION_LINES = ("Session", "Did", "Worked", "Failed", "Requests", "Suggestions", "Report")
ANSWER_WORDS = ("yes", "no", "done")
LOGS = {"orders": ("order",), "reports": ("session",), "requests": ("request", "answer"), "queue": ("general",), "errors": ("error",),
        "admirals": ("note", "claim"), "contracts": ("contract", "bursar", "filled", "expired")}
GATED = ("orders", "reports", "requests")
ENTRY_CHARS = 8000            # the newest orders entry, whole, Suggi's S and G lines included (Suggi, 2026-11-18)
PLAN_WORDS = 150              # ... PLAN, its heading line not counted
BLOCK_WORDS = 80              # ... each member's block, its heading line not counted
CHANGED_WORDS = 60            # ... the `Changed:` line
STALE_DAYS = 3                # r22: a request not closed whose newest entry is older than this is marked STALE (never closed)
MEMBER_BLOCK = re.compile(r"^([A-Z]{3,}), ")      # a member's block heading: `UNITY, Fleet Admiral (...)`, as members() reads it
DRAFT = re.compile(r"^## \[ENT-NEXT\] \| NOW \| ([A-Za-z][A-Za-z0-9_-]*) \| ([a-z]+)((?: \| (?:ref|see): [^|]+)*)$")


def parse(text):
    """(entries, errors) of one log's text. An entry: num, when, by, category, ref, see, head, body."""
    entries, errors = [], []
    for line in text.splitlines():
        if line.startswith("## [ENT-"):
            match = HEADER.match(line.rstrip())
            if match is None:
                errors.append("header not in the protocol's form: " + line[:70])
                entries.append(None)                       # its body lines belong to no entry
                continue
            extra = dict(part.split(": ", 1) for part in match.group(5).split(" | ") if ": " in part)
            entries.append({"num": int(match.group(1)), "when": match.group(2), "by": match.group(3), "category": match.group(4),
                            "ref": extra.get("ref", "").strip(), "see": extra.get("see", "").strip(), "head": line.rstrip(), "body": []})
        elif entries and entries[-1] is not None:
            entries[-1]["body"].append(line.rstrip())
    entries = [e for e in entries if e is not None]
    for entry in entries:
        while entry["body"] and not entry["body"][-1]:
            entry["body"].pop()
    return entries, errors


def read_log(root, name, archive=False):
    """(entries, errors) of communications/<name>.log; with archive, the archived entries come first."""
    folder = Path(root) / "communications"
    paths = sorted((folder / "archive").glob(name + "-*.log")) if archive and (folder / "archive").is_dir() else []
    entries, errors = [], []
    for path in paths + [folder / (name + ".log")]:
        try:
            found, bad = parse(path.read_text(encoding="ascii", errors="replace"))
        except OSError:
            errors.append("%s: not readable" % path.name)
            continue
        entries += found
        errors += bad
    return entries, errors


def field(entry, label):
    """The text after `<label>:` in an entry's body, or ''."""
    if entry is None:
        return ""
    for line in entry["body"]:
        if line.startswith(label + ":"):
            return line[len(label) + 1:].strip()
    return ""


def first_word(text):
    match = re.match(r"[a-z]+", text.strip().lower())
    return match.group(0) if match else ""


def request_states(entries):
    """[(state, request, last answer or None)] in the order the requests were written."""
    requests = {e["num"]: e for e in entries if e["category"] == "request"}
    last = {}
    for entry in entries:
        named = re.search(r"ENT-(\d+)", entry["see"])
        if entry["category"] == "answer" and named and int(named.group(1)) in requests:
            last[int(named.group(1))] = entry
    out = []
    for num in sorted(requests):
        answer = last.get(num)
        state = "OPEN" if answer is None else ("ACCEPTED" if first_word(field(answer, "Answer")) == "yes" else "CLOSED")
        out.append((state, requests[num], answer))
    return out


def addressed(request, name):
    """True when the request's To: line names the member, or all."""
    names = [n for n in re.split(r"[^a-z]+", field(request, "To").lower()) if n]
    return name.lower() in names or "all" in names


def stale_days(state, request, answer, now):
    """The days since the newest entry of a request not closed (the request, or its last answer) when they are more than
    STALE_DAYS; None for a closed or a fresh one."""
    if state == "CLOSED":
        return None
    try:
        age = (now - calendar.timegm(time.strptime((answer or request)["when"], "%Y-%m-%d %H:%M"))) / 86400.0
    except (ValueError, KeyError, TypeError):
        return None
    return age if age > STALE_DAYS else None


def stale_line(root, who, now=None):
    """The briefing's line: how many requests not closed and addressed to `who` (all: every one) are stale, and which."""
    now = time.time() if now is None else now
    entries, _errors = read_log(root, "requests", archive=True)
    found = [r for r in request_states(entries) if stale_days(r[0], r[1], r[2], now) is not None and (who in (None, "all") or addressed(r[1], who))]
    return ("STALE REQUESTS%s: %d not closed and untouched for more than %d days%s%s"
            % ("" if who in (None, "all") else " ADDRESSED TO " + who, len(found), STALE_DAYS, ": " if found else "",
               ", ".join("ENT-%03d" % r[1]["num"] for r in found)) + (" | answer each (yes, no or done); no machine closes one" if found else ""))


def request_line(state, request, answer, now=None):
    days = stale_days(state, request, answer, now) if now is not None else None
    line = ("  STALE (%.0f d) " % days if days is not None else "  ") + "ENT-%03d | %s | %s -> %s | by %s | %s" % (request["num"], request["when"], request["by"], field(request, "To").rstrip(".") or "?",
                                                      field(request, "By").rstrip(".") or "not said", field(request, "Need")[:160])
    if answer is not None:
        line += "\n          answered ENT-%03d by %s, %s: %s" % (answer["num"], answer["by"], answer["when"], field(answer, "Answer")[:140])
    return line


def show_orders(root):
    entries, _errors = read_log(root, "orders")
    if not entries:
        print("orders.log holds no entry: no orders in force")
        return 1
    newest = entries[-1]
    print("\n".join([newest["head"]] + newest["body"]))
    return 0


def show_requests(root, to, sender, everything, now=None):
    now = time.time() if now is None else now
    entries, _errors = read_log(root, "requests", archive=True)
    rows = [r for r in request_states(entries) if (to is None or addressed(r[1], to)) and (sender is None or r[1]["by"].lower() == sender.lower())]
    for state in ("OPEN", "ACCEPTED") + (("CLOSED",) if everything else ()):
        mine = [r for r in rows if r[0] == state]
        print("%s (%d)" % (state, len(mine)))
        for row in mine:
            print(request_line(*row, now=now))
    stale = [r for r in rows if stale_days(r[0], r[1], r[2], now) is not None]
    if stale:
        print("Stale: %d not closed and untouched for more than %d days (%s): answer each (yes, no or done); no machine closes one"
              % (len(stale), STALE_DAYS, ", ".join("ENT-%03d" % r[1]["num"] for r in stale)))
    print("Open: %d | Accepted: %d | Closed: %d" % tuple(sum(1 for r in rows if r[0] == s) for s in ("OPEN", "ACCEPTED", "CLOSED")))
    return 0


def members(root, sessions):
    """Unity, then every member that reported or that the newest orders name in a block of their own."""
    names = {e["by"] for e in sessions}
    orders, _errors = read_log(root, "orders")
    if orders:
        names |= {m.group(1).capitalize() for m in (re.match(r"^([A-Z]{3,}), ", line) for line in orders[-1]["body"]) if m}
    names.discard("Unity")
    return ["Unity"] + sorted(names)


def show_digest(root, last, member, now=None):
    now = time.time() if now is None else now
    sessions, _errors = read_log(root, "reports")
    requests, _errors = read_log(root, "requests", archive=True)
    pending = [r for r in request_states(requests) if r[0] != "CLOSED"]
    for name in members(root, sessions):
        if member and name.lower() != member.lower():
            continue
        mine = [e for e in sessions if e["by"] == name]
        if not mine:
            print("== %s: no session entry" % name)
        else:
            print("== %s: %d session entries, newest ENT-%03d of %s" % (name, len(mine), mine[-1]["num"], mine[-1]["when"]))
            for entry in mine[-last:]:
                print("\n".join([entry["head"]] + entry["body"]))
                print()
        for row in pending:
            if row[1]["by"] == name or addressed(row[1], name):
                print("  request %s:" % row[0].lower())
                print("  " + request_line(*row, now=now).replace("\n", "\n  "))
        print()
    return 0


def line_of(entry, label):
    """The text after `<label>:` in an entry's body, or ''."""
    return next((line[len(label) + 1:].strip() for line in entry["body"] if line.startswith(label + ":")), "")


def claims_in_force(entries, now=None):
    """The claims of admirals.log still in force: every claim not ended by a `Releases: ENT-NNN` line of its own
    writer. A claim stands until it is released (Suggi, 2026-11-21); `now` is kept for the callers and unused."""
    released = {(entry["by"], int(number)) for entry in entries for number in re.findall(r"ENT-(\d+)", line_of(entry, "Releases"))}
    return [e for e in entries if e["category"] == "claim" and (e["by"], e["num"]) not in released]


def claimed_routes(root, text):
    """The route ids a `Claims:` line names: its hyphenated words that are route files of game/routes/. A place written
    in words (an ask, a bid, a field by its name) is no route id and is not compared."""
    folder = Path(root) / "game" / "routes"
    return sorted({word for word in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+", text) if (folder / (word + ".json")).is_file()})


def standing_route(root, route_id):
    """True when the route is standing work by the fleet's one rule (game/fleet/routes.py, standing): its places are
    shared by every division (rule F8), so two claims on it may stand side by side."""
    try:
        route = json.loads((Path(root) / "game" / "routes" / (route_id + ".json")).read_text(encoding="ascii"))
    except (OSError, ValueError, UnicodeDecodeError):
        return False
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "game" / "fleet"))
    try:
        import routes
        return bool(routes.standing(route))
    finally:
        sys.path.pop(0)


def claim_overlaps(root, name, claims_line):
    """[(route id, entry)] for each route of a new claim that another member's claim in force names (requests ENT-180).
    The writer's own claims and standing work are left out."""
    wanted = claimed_routes(root, claims_line)
    if not wanted:
        return []
    entries, _errors = read_log(root, "admirals")
    out = []
    for entry in claims_in_force(entries):
        if entry["by"] == name:
            continue
        theirs = set(claimed_routes(root, line_of(entry, "Claims")))
        out += [(route, entry) for route in wanted if route in theirs and not standing_route(root, route)]
    return out


def show_admirals(root, last, member):
    """The Admirals' own log: the claims in force, then the last entries. A claim stands until a later entry of its
    writer ends it with a `Releases: ENT-NNN` line (Suggi, 2026-11-21)."""
    if not (Path(root) / "communications" / "admirals.log").is_file():
        print("no communications/admirals.log")
        return 0
    entries, _errors = read_log(root, "admirals")
    claims = claims_in_force(entries)
    print("CLAIMS IN FORCE: %d (a claim stands until its writer ends it with a `Releases: ENT-NNN` line; another "
          "division leaves a claimed route to its claimer, or asks)" % len(claims))
    for entry in claims:
        print("  ENT-%03d | %s UTC | %s | %s" % (entry["num"], entry["when"], entry["by"], line_of(entry, "Claims")))
    shown = [e for e in entries if not member or e["by"].lower() == member.lower()][-last:]
    print("LAST %d ENTRIES%s" % (len(shown), (" of " + member) if member else ""))
    for entry in shown:
        print("\n".join([entry["head"]] + entry["body"]))
        print()
    return 0


def block_pattern():
    """The pattern of a block heading line of the orders (`PLAN (...)`, `EVERY ADMIRAL`, `ZERO, Mining ...`): the
    store's one reading of the orders' blocks (game/fleet/docs.py, BLOCK)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "game" / "fleet"))
    try:
        import docs
        return docs.BLOCK
    finally:
        sys.path.pop(0)


def orders_words(entry):
    """[(part, words, limit, name of the limit)] of one orders entry: the `Changed:` line, PLAN (from the line after
    its heading to the first member block, every line between counted), each member's block (its heading line not
    counted, to the next block heading). Suggi's standing orders and goals, and any part outside these, are not counted."""
    parts, counts, current, pattern = [], {}, None, block_pattern()
    changed = next((line for line in entry["body"] if line.startswith("Changed:")), None)
    if changed is not None:
        parts.append(("the `Changed:` line", len(changed.split()), CHANGED_WORDS, "CHANGED_WORDS"))
    for line in entry["body"]:
        found = pattern.match(line)
        head = found.group(1) if found else None
        member = MEMBER_BLOCK.match(line)
        if member:
            current = "block " + member.group(1)
            counts.setdefault(current, 0)
            continue
        if head == "PLAN":
            current = "PLAN"
            counts.setdefault(current, 0)
            continue
        if head is not None and current != "PLAN":
            current = None                                 # a block heading that is no member's ends a member's block
        if current is not None:
            counts[current] += len(line.split())
    for part, words in counts.items():
        parts.append((part, words) + ((PLAN_WORDS, "PLAN_WORDS") if part == "PLAN" else (BLOCK_WORDS, "BLOCK_WORDS")))
    return parts


def orders_size(entry):
    """Error lines for the newest orders entry: the whole entry over ENTRY_CHARS, each part over its word limit, each
    named with its count."""
    where = "orders.log ENT-%03d: " % entry["num"]
    chars = len("\n".join([entry["head"]] + entry["body"]))
    errors = [where + "the entry is %s characters, more than ENTRY_CHARS %s" % (format(chars, ","), format(ENTRY_CHARS, ","))
              ] if chars > ENTRY_CHARS else []
    return errors + [where + "%s is %s words, more than %s %s" % (part, format(words, ","), name, format(limit, ","))
                     for part, words, limit, name in orders_words(entry) if words > limit]


def check(root):
    """Error lines for the three logs this script reads."""
    errors = []
    archived, _errors = read_log(root, "requests", archive=True)
    known = {e["num"] for e in archived if e["category"] == "request"}
    for name in ("orders", "reports", "requests"):
        if not (Path(root) / "communications" / (name + ".log")).is_file():
            errors.append("%s.log: missing" % name)
            continue
        entries, bad = read_log(root, name)
        errors += ["%s.log: %s" % (name, line) for line in bad]
        for before, entry in zip([None] + entries, entries):
            where = "%s.log ENT-%03d: " % (name, entry["num"])
            if before is not None and entry["num"] != before["num"] + 1:
                errors.append(where + "follows ENT-%03d: the numbers rise by one" % before["num"])
            if not entry["body"]:
                errors.append(where + "has no body")
            if name == "orders":
                if entry["by"] != "Unity" or entry["category"] != "order":
                    errors.append(where + "the orders are written by Unity only, category `order` (found %s, `%s`)" % (entry["by"], entry["category"]))
                if not field(entry, "Changed"):
                    errors.append(where + "no `Changed:` line")
                if not any(line.startswith("In force") for line in entry["body"]):
                    errors.append(where + "no `In force` line")
            elif name == "reports":
                if entry["category"] != "session":
                    errors.append(where + "category must be `session` (found `%s`)" % entry["category"])
                errors += [where + "no `%s:` line" % label for label in SESSION_LINES if not field(entry, label)]
            elif entry["category"] == "request":
                errors += [where + "a request needs a `%s:` line" % label for label in ("To", "Need") if not field(entry, label)]
            elif entry["category"] == "answer":
                named = re.search(r"ENT-(\d+)", entry["see"])
                if named is None or int(named.group(1)) not in known:
                    errors.append(where + "an answer names a request of this log in `see:` (found `%s`)" % entry["see"])
                if first_word(field(entry, "Answer")) not in ANSWER_WORDS:
                    errors.append(where + "the `Answer:` line starts with yes, no or done")
            else:
                errors.append(where + "category must be `request` or `answer` (found `%s`)" % entry["category"])
        if name == "orders" and entries:
            errors += orders_size(entries[-1])             # the newest entry only: an older one is history
    return errors


def git_commit(root, rel, name, message):
    """Commit one path under the writer's name; the short hash, or None when git refused six times."""
    identity = ["-c", "user.name=" + name, "-c", "user.email=%s@suggi-workspace.dev" % name.lower()]
    for _attempt in range(6):                                  # another member's commit may hold the index for a moment
        done = subprocess.run(["git", "-C", str(root), "add", "--", rel], capture_output=True, text=True)
        if done.returncode == 0:
            done = subprocess.run(["git", "-C", str(root)] + identity + ["commit", "-q", "-m", message, "--", rel], capture_output=True, text=True)
        if done.returncode == 0:
            return subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
        time.sleep(2)
    return None


def pilots_named(text):
    """The pilots of ours a text names, by the fleet's one rule for it (game/fleet/division.py)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "game" / "fleet"))
    try:
        import division
        return division.pilots_named(text)
    finally:
        sys.path.pop(0)


def append(root, log, entry_file, name, commit=True):
    """Append one prepared entry to a log as one locked step. 0 done, 1 refused, 2 appended but not committed. An entry
    that names a pilot of ours is refused: the logs are public (requests ENT-052)."""
    root = Path(root)
    path = root / "communications" / (log + ".log")
    try:
        lines = Path(entry_file).read_text(encoding="ascii").strip("\n").split("\n")
    except (OSError, UnicodeDecodeError) as error:
        print("NOT APPENDED: the entry file is not readable as ASCII: %s" % error)
        return 1
    problems = []
    draft = DRAFT.match(lines[0].rstrip())
    if draft is None:
        problems.append("the first line must be `## [ENT-NEXT] | NOW | <Name> | <category>`, then ` | ref: ...` and ` | see: ...` where they apply")
    else:
        if draft.group(1) != name:
            problems.append("the entry names %s as its writer, the append is made as %s" % (draft.group(1), name))
        if draft.group(2) not in LOGS[log]:
            problems.append("category `%s` does not belong in %s.log (it takes: %s)" % (draft.group(2), log, ", ".join(LOGS[log])))
    if log == "orders" and name != "Unity":
        problems.append("orders.log is written by the Fleet Admiral only")
    if any(line.startswith("## [ENT-") for line in lines[1:]):
        problems.append("one entry per call")
    if not any(line.strip() for line in lines[1:]):
        problems.append("the entry has no body")
    if log == "admirals" and draft is not None and draft.group(2) == "claim" and not any(line.startswith("Claims:") for line in lines[1:]):
        problems.append("a claim needs a `Claims:` line: the route ids or the place, and for how many ships")
    named = pilots_named("\n".join(lines))
    if named:
        problems.append("the entry names a pilot of ours (%s): the repository is public; write the division and a count, or `a miner`; "
                        "which ship it was stays in the data folder" % ", ".join(named[:5]))
    if not path.is_file():
        problems.append("communications/%s.log does not exist" % log)
    if Path(entry_file).resolve().is_relative_to(root.resolve()):
        problems.append("keep the entry file outside the repository (your scratch directory): an untracked file there holds every push")
    if problems:
        for line in problems:
            print("NOT APPENDED: " + line)
        return 1
    lock = open(root / ".git" / "comms.lock", "w") if (root / ".git").is_dir() else None
    try:
        if lock is not None:
            fcntl.flock(lock, fcntl.LOCK_EX)                   # one writer at a time, from the number to the commit
        before = path.read_text(encoding="ascii", errors="replace")
        if log == "admirals" and draft.group(2) == "claim":
            claims_line = next((line[len("Claims:"):] for line in lines[1:] if line.startswith("Claims:")), "")
            overlaps = claim_overlaps(root, name, claims_line)
            for route, entry in overlaps:                     # read under the lock: a claim a minute old counts
                print("NOT APPENDED: %s is claimed by %s in admirals.log ENT-%03d (in force until it is released): leave it out "
                      "of your claim, ask %s in requests.log, or claim it once %s releases it" % (route, entry["by"], entry["num"],
                                                                                    entry["by"], entry["by"]))
            if overlaps:
                return 1
        entries, _errors = parse(before)
        if not entries:
            entries, _errors = read_log(root, log, archive=True)   # the counter goes on after an archive run
        number = entries[-1]["num"] + 1 if entries else 1
        head = lines[0].rstrip().replace("[ENT-NEXT] | NOW", "[ENT-%03d] | %s" % (number, time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())), 1)
        text = "\n".join([head] + [line.rstrip() for line in lines[1:]]) + "\n"
        gap = "" if before.endswith("\n\n") or not before else ("\n" if before.endswith("\n") else "\n\n")
        known = set(check(root)) if log in GATED else set()
        size = path.stat().st_size
        with open(path, "a", encoding="ascii", newline="\n") as handle:
            handle.write(gap + text)
        fresh = [line for line in check(root) if line not in known] if log in GATED else []
        if fresh:
            with open(path, "r+b") as handle:
                handle.truncate(size)                          # take the entry out again
            for line in fresh:
                print("NOT APPENDED: " + line.replace("ENT-%03d" % number, "the entry"))
            return 1
        rel = "communications/%s.log" % log
        if not commit or not (root / ".git").is_dir():
            print("appended ENT-%03d to %s (not committed)" % (number, rel))
            return 0
        sha = git_commit(root, rel, name, "%s.log: ENT-%03d (%s, %s)" % (log, number, draft.group(2), name))
        if sha is None:
            print("appended ENT-%03d to %s but NOT COMMITTED: git refused; commit it by path under your name" % (number, rel))
            return 2
        print("appended ENT-%03d to %s, committed %s as %s" % (number, rel, sha, name))
        return 0
    finally:
        if lock is not None:
            lock.close()


def post_one(root, log, writer, category, body, ref="", see="", commit=True):
    """1-step atomic log append: formats the protocol header into a self-cleaning temp file outside the repository,
    validates and commits via append(), and removes the temp file immediately."""
    import os, tempfile
    if not writer:
        prof = os.environ.get("HERMES_SESSION_PROFILE", "").strip()
        writer = prof.capitalize() if prof else ""
    if not writer:
        print("NOT APPENDED: pass --as <Name> or set HERMES_SESSION_PROFILE")
        return 1
    hdr = "## [ENT-NEXT] | NOW | %s | %s" % (writer, category)
    if ref:
        hdr += " | ref: %s" % ref.strip()
    if see:
        hdr += " | see: %s" % see.strip()
    clean_body = "\n".join(ln.rstrip() for ln in str(body or "").replace("\\n", "\n").splitlines()).strip()
    if not clean_body:
        print("NOT APPENDED: body is empty")
        return 1
    fd, tmp_path = tempfile.mkstemp(prefix="comms-post-", suffix=".md", dir="/tmp")
    try:
        with os.fdopen(fd, "w", encoding="ascii") as fh:
            fh.write(hdr + "\n" + clean_body + "\n")
        return append(root, log, tmp_path, writer, commit=commit)
    except UnicodeEncodeError:
        print("NOT APPENDED: entry contains non-ASCII characters")
        return 1
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def show_turn_pack(root, member=None):
    """All log context a member needs at turn start in one call: orders in force, open/accepted requests, active claims & recent errors."""
    import os
    who = member or (os.environ.get("HERMES_SESSION_PROFILE", "").strip().capitalize() or None)
    print("=== 1. ACTIVE ORDERS IN FORCE ===")
    show_orders(root)
    print("\n=== 2. OPEN & ACCEPTED REQUESTS (%s) ===" % (who or "ALL"))
    show_requests(root, who if who and who != "Unity" else None, None, False)
    if who and who != "Unity":
        print("--- Sent by %s ---" % who)
        show_requests(root, None, who, False)
    print("\n=== 3. ACTIVE CLAIMS & RECENT ADMIRALS NOTES ===")
    show_admirals(root, 6, None)
    print("\n=== 4. NEWEST 5 ERRORS.LOG HEADERS ===")
    errs, _ = read_log(root, "errors")
    for e in errs[-5:]:
        print("  ENT-%03d | %s | %s | %s" % (e["num"], e["when"], e["by"], (e["body"][0][:110] if e["body"] else "")))
    return 0


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Read and post to the fleet's logs in one step.")
    parser.add_argument("command", choices=("orders", "requests", "digest", "check", "admirals", "append", "post", "turn-pack"))
    parser.add_argument("target", nargs="*", help="append: the log's name and the entry file")
    parser.add_argument("--root", default=str(here.parent))
    parser.add_argument("--as", dest="writer")
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--to")
    parser.add_argument("--from", dest="sender")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--last", type=int)
    parser.add_argument("--member")
    parser.add_argument("--cat", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--ref", default="")
    parser.add_argument("--see", default="")
    args = parser.parse_args()
    if args.command == "post":
        if len(args.target) != 1 or args.target[0] not in LOGS or not args.cat:
            parser.error("post takes: <%s> --cat <category> --body '<text>' [--ref ...] [--see ...] [--as <Name>]" % "|".join(LOGS))
        return post_one(args.root, args.target[0], args.writer, args.cat, args.body, args.ref, args.see, commit=not args.no_commit)
    if args.command == "turn-pack":
        return show_turn_pack(args.root, args.member)
    if args.command == "append":
        if len(args.target) != 2 or args.target[0] not in LOGS or not args.writer:
            parser.error("append takes: <%s> <entry file> --as <Name>" % "|".join(LOGS))
        return append(args.root, args.target[0], args.target[1], args.writer, commit=not args.no_commit)
    if args.target:
        parser.error("only append and post take positional log arguments")
    if args.command == "orders":
        return show_orders(args.root)
    if args.command == "requests":
        return show_requests(args.root, args.to, args.sender, args.all)
    if args.command == "digest":
        return show_digest(args.root, max(args.last or 3, 1), args.member)
    if args.command == "admirals":
        return show_admirals(args.root, max(args.last or 12, 1), args.member)
    errors = check(args.root)
    for line in errors:
        print("ERROR " + line)
    print("Errors: %d | Warnings: 0" % len(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
