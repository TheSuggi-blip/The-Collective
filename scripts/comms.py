#!/usr/bin/env python3
"""comms.py -- read the fleet's logs: the orders in force, the requests and their state, the last session entries.

WHAT: communications/ holds the append-only logs of The Collective
      (communications/protocol.md). This script answers, without AI, what a
      member asks of them at session start:
        orders     the newest entry of orders.log: the orders in force, complete
        requests   the requests of requests.log by state: OPEN (no answer yet),
                   ACCEPTED (the last answer says yes) and, with --all, CLOSED
                   (the last answer says done or no)
        digest     the last session entries of each member from reports.log and
                   the requests not closed: the record a summary of the
                   divisions is written from
        check      the gate of the three logs' rules
      and it is the one way an entry is written to any log:
        append     appends one prepared entry under a lock: it sets the entry's
                   number and time, puts exactly one blank line before it, runs
                   the gate and commits the log by path under the writer's name
RULES (append):
  - the entry file starts `## [ENT-NEXT] | NOW | <Name> | <category>`, with
    ` | ref: ...` and ` | see: ...` after it where they apply; the body follows;
  - <Name> is the writer given with --as; orders.log takes entries of Unity only;
  - the category belongs to the log: order (orders), session (reports), request
    or answer (requests), general (queue), error (errors);
  - the entry file lies outside the repository: an untracked file in the
    working copy holds every member's push;
  - an entry that breaks the gate is taken out again and nothing is committed.
RULES (check):
  - a header has the protocol's form, and the ENT numbers of a log rise by one;
  - orders.log: written by Unity only, category `order`, with a `Changed:` line
    and an `In force` line;
  - reports.log: category `session`, with the lines Session, Did, Worked,
    Failed, Requests, Suggestions and Report;
  - requests.log: a `request` has a `To:` and a `Need:` line; an `answer` names
    a request of this log in `see:` and its `Answer:` line starts with yes, no
    or done.
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
  comms.py append <orders|reports|requests|queue|errors> <entry file> --as <Name>
  --root <dir>   repository root (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import argparse
import fcntl
import re
import subprocess
import sys
import time
from pathlib import Path

HEADER = re.compile(r"^## \[ENT-(\d{3,})\] \| (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC \| ([A-Za-z][A-Za-z0-9_-]*) \| ([a-z]+)((?: \| (?:ref|see): [^|]+)*)$")
SESSION_LINES = ("Session", "Did", "Worked", "Failed", "Requests", "Suggestions", "Report")
ANSWER_WORDS = ("yes", "no", "done")
LOGS = {"orders": ("order",), "reports": ("session",), "requests": ("request", "answer"), "queue": ("general",), "errors": ("error",)}
GATED = ("orders", "reports", "requests")
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


def request_line(state, request, answer):
    line = "  ENT-%03d | %s | %s -> %s | by %s | %s" % (request["num"], request["when"], request["by"], field(request, "To").rstrip(".") or "?",
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


def show_requests(root, to, sender, everything):
    entries, _errors = read_log(root, "requests", archive=True)
    rows = [r for r in request_states(entries) if (to is None or addressed(r[1], to)) and (sender is None or r[1]["by"].lower() == sender.lower())]
    for state in ("OPEN", "ACCEPTED") + (("CLOSED",) if everything else ()):
        mine = [r for r in rows if r[0] == state]
        print("%s (%d)" % (state, len(mine)))
        for row in mine:
            print(request_line(*row))
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


def show_digest(root, last, member):
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
                print("  " + request_line(*row).replace("\n", "\n  "))
        print()
    return 0


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


def append(root, log, entry_file, name, commit=True):
    """Append one prepared entry to a log as one locked step. 0 done, 1 refused, 2 appended but not committed."""
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


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Read the fleet's logs: orders in force, requests by state, last session entries.")
    parser.add_argument("command", choices=("orders", "requests", "digest", "check", "append"))
    parser.add_argument("target", nargs="*", help="append: the log's name and the entry file")
    parser.add_argument("--root", default=str(here.parent))
    parser.add_argument("--as", dest="writer")
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--to")
    parser.add_argument("--from", dest="sender")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--last", type=int, default=3)
    parser.add_argument("--member")
    args = parser.parse_args()
    if args.command == "append":
        if len(args.target) != 2 or args.target[0] not in LOGS or not args.writer:
            parser.error("append takes: <%s> <entry file> --as <Name>" % "|".join(LOGS))
        return append(args.root, args.target[0], args.target[1], args.writer, commit=not args.no_commit)
    if args.target:
        parser.error("only append takes a log and an entry file")
    if args.command == "orders":
        return show_orders(args.root)
    if args.command == "requests":
        return show_requests(args.root, args.to, args.sender, args.all)
    if args.command == "digest":
        return show_digest(args.root, max(args.last, 1), args.member)
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
