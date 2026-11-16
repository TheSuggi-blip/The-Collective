#!/usr/bin/env python3
"""fleetfile.py -- write the section `## Routes Now` into a member's own FLEET.md: its plans route by route, and every ship of its division on one line with what it flies now.

WHAT: a member's FLEET.md (in its private workspace) says how its division is meant to work; this script
      adds what it does now, read from the fleet's live files, between two marks:
        Plan <role>    every route of the role's plan in its order: kind, group, ships on it now against
                       its limit, the ships it carries (what its bid, field or herd regains; fill.py
                       `carries`), what its runs measured (game/routes/plans/<role>.json, the route files)
        Ships <role>   every ship of the role, by its number: what it does now and since when, its last
                       run, its Piloting, Mining and Navigation levels and its modules; then one count line
      Unity's block holds the roles command and sentinel; every other member's block its one role.
RULES:
  - A member writes its own file only; the Fleet Admiral may name any member or `all`. A shell that is
    no member writes nothing. Printing (--print) is free for everyone and writes nothing.
  - Only the text between the two marks (both lines included) is the script's. A file without the marks
    gets the block appended after one blank line; a file with only one of them is refused (HALT) and not
    touched. Everything outside the marks stays byte for byte.
  - The file is written through a temporary file and a rename, and only when the block changed in more
    than the line that carries the time: a run that finds nothing new prints `unchanged`.
  - --commit commits FLEET.md by path in the workspace's own git repository as the member that runs the
    script, only when the file had no uncommitted change before the write.
  - One run writes at a time (the lock data/fleet/fleetfile.lock, held from the reading to the commit):
    the hourly job and a member's preflight never write or commit the same file together.
  - The figures are the fleet's own: ships on a route counted as the dispatcher counts them (fill.py), a
    route's group and figure from routes.py, a run's credits by routes.earned; what no file holds is `--`.
  - No ship's position beyond the system of a ship that waits: the file is private, the habit is not.
WHY:  an Admiral read its plan in one file and its ships in another, turn after turn. One generated
      section in its own FLEET.md puts both beside the design, and no hand keeps it.

USAGE:
  fleetfile.py [<Member>|all] [--print] [--commit]
  --root <dir>      the repository's game/ folder (default: the parent of this file's folder)
  --data <dir>      the unit's data folder (default /srv/collective/data)
  --profiles <dir>  where the members' workspaces lie (default /opt/data/profiles): <profiles>/<name>/workspace-<name>/FLEET.md

Stdlib only. ASCII only.
"""

import fcntl
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dispatch                                   # noqa: E402  orders, routes, runs, flagships
import division                                   # noqa: E402  who asks, which roles are whose
import fill                                       # noqa: E402  ships on a route, counted as the dispatcher counts them
import hive                                       # noqa: E402  the ships' files, modules, numbers and times
import routes as routefiles                       # noqa: E402  a route's group and figure, what a run earned

BEGIN = "<!-- ROUTES-NOW:BEGIN written by game/fleet/fleetfile.py; do not edit between the two marks -->"
END = "<!-- ROUTES-NOW:END -->"
BEGIN_MARK, END_MARK = "<!-- ROUTES-NOW:BEGIN", "<!-- ROUTES-NOW:END"
STAMP = "Written by `game/fleet/fleetfile.py` at "
TIME = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")
SKILLS = ("piloting", "mining", "navigation")
PLAN_HEAD = ("#", "Route", "Kind", "Group", "Ships now / limit", "Carries", "Measured")
SHIP_HEAD = ("Ship", "Does now", "Since (UTC)", "Last run", "Piloting", "Mining", "Navigation", "Modules")
OPTIONS = ("--root", "--data", "--profiles")
FLAGS = ("--print", "--commit")


class Halt(Exception):
    """A file this script must not write: nothing is written, the run ends with exit 1."""


def cell(value):
    """One table cell: one line of printable ASCII without a `|` (routes.cell), `--` when empty."""
    text = routefiles.cell(value).replace("\r", " ")
    return "".join(c if 32 <= ord(c) < 127 else "?" for c in text).strip() or "--"


def table_row(cells):
    return "| " + " | ".join(cell(c) for c in cells) + " |"


def table(head, rows):
    return [table_row(head), "|" + "---|" * len(head)] + [table_row(r) for r in rows]


def hhmm(stamp):
    t = hive.epoch(stamp) if stamp else 0
    return time.strftime("%H:%M", time.gmtime(t)) if t else "--"


def newest_runs(rows):
    """{pilot: its newest run row}: the latest start, the later line of runs.jsonl on a tie."""
    out = {}
    for n, row in enumerate(rows):
        pilot = row.get("pilot") if isinstance(row, dict) else None
        if pilot:
            key = (hive.epoch(row.get("started")), n)
            if pilot not in out or key >= out[pilot][0]:
                out[pilot] = (key, row)
    return {pilot: row for pilot, (_key, row) in out.items()}


def last_run(row):
    """`<route>: <+/-credits> cr in <minutes> min, started <MM-DD HH:MM>`, or `--`."""
    if not row:
        return "--"
    if routefiles.readable(row):
        credits = routefiles.earned(row)
        money = "%s%s cr" % ("-" if credits < 0 else "+", hive.num(abs(credits)))
    else:
        money = "wallet not read"
    t = hive.epoch(row.get("started"))
    return "%s: %s in %s min, started %s" % (row.get("route") or "?", money, hive.num(row.get("minutes")),
                                             time.strftime("%m-%d %H:%M", time.gmtime(t)) if t else "--")


def level(detail, skill):
    """A skill's level from the ship's live file ({skill: {level: N}} or {skill: N}); 0 for a skill the file does not
    list, `--` when no skills were read."""
    skills = detail.get("skills") if isinstance(detail, dict) else None
    if not isinstance(skills, dict) or not skills:
        return "--"
    entry = skills.get(skill, 0)
    value = entry.get("level") if isinstance(entry, dict) else entry
    return str(int(value)) if isinstance(value, (int, float)) and not isinstance(value, bool) else "--"


def modules(detail):
    if not isinstance(detail, dict) or not detail:
        return "--"
    return ", ".join(sorted({str(m) for m in hive.modules_of(detail) if m})) or "none"


def doing(ship, what, since, routes):
    """(Does now, Since, count key) of one ship: the cases hive.py standing tells apart."""
    if ship.get("status") != "connected":
        return "not connected", "--", "not connected"
    if what and what.startswith("hand "):
        return "by hand: " + what[5:], hhmm(since), "by hand"
    if what:
        rid = what.split(" ", 1)[1] if " " in what else what
        route = routes.get(rid) or {}
        return "flies " + what, hhmm(since), "waiting" if route.get("park") else "on a route"
    activity = ship.get("activity") if isinstance(ship.get("activity"), dict) else {}
    if activity.get("kind") != "idle":
        return "busy by hand (%s)" % activity.get("kind"), hhmm(activity.get("since")), "by hand"
    return "waits %s at %s" % ("docked" if ship.get("docked") else "in space", ship.get("system") or "?"), "--", "waiting"


def read_state(root, data, now):
    """Everything a block rests on, read once for every member."""
    plans, _owners, _errors = division.load_plan(root)
    orders = dispatch.fresh_orders(data, now)
    since = {}
    for pilot in orders:
        found = dispatch.read_json(Path(data) / "fleet" / "orders" / (pilot + ".json"), {})
        since[pilot] = found.get("since") if isinstance(found, dict) else None
    crew, _fleet = hive.pilots(data)
    return {"now": now, "data": data, "plans": plans, "routes": dispatch.load_routes(root), "orders": orders, "since": since,
            "named": dispatch.flagships(data), "crew": crew, "runs": newest_runs(dispatch.run_rows(data)),
            "titles": {key: title for key, title, _text in routefiles.STAGES}}


def roles_of(member):
    return sorted(role for role, who in division.ROLES.items() if who == member)


def block(seen, member):
    """(the block's text without a final newline, ships counted, roles) of one member."""
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(seen["now"]))
    lines = [BEGIN, "## Routes Now", "",
             STAMP + stamp + " from the fleet's live files; changed only by the script (preflight and session-end run it).", ""]
    routes, orders, total = seen["routes"], seen["orders"], 0
    for role in roles_of(member):
        lines += ["### Plan %s" % role, ""]
        plan = seen["plans"].get(role)
        if plan is None:
            lines += ["No plan file game/routes/plans/%s.json." % role, ""]
        elif not plan:
            lines += ["The plan lists no route.", ""]
        else:
            rows = []
            for n, rid in enumerate(plan, 1):
                route = routes.get(rid)
                if not route:
                    rows.append((n, rid, "no route file", "--", "--", "--", "--"))
                    continue
                rows.append((n, rid, route.get("kind"), seen["titles"][routefiles.stage(route)],
                             "%d / %s" % (fill.flying_now(route, rid, orders), route.get("max_ships") or "-"),
                             fill.carried(fill.carries(seen, route)), routefiles.figure(route)))
            lines += table(PLAN_HEAD, rows) + [""]
        mine = sorted(((ship, detail) for ship, detail in seen["crew"] if dispatch.role_of(ship.get("name") or "", seen["named"]) == role),
                      key=lambda sd: (sd[0].get("number") or 0, sd[0].get("name") or ""))
        lines += ["### Ships %s" % role, ""]
        counts = {"on a route": 0, "waiting": 0, "by hand": 0, "not connected": 0}
        rows = []
        for ship, detail in mine:
            name = ship.get("name") or ""
            does, since, key = doing(ship, orders.get(name), seen["since"].get(name), routes)
            counts[key] += 1
            rows.append([name, does, since, last_run(seen["runs"].get(name))] + [level(detail, s) for s in SKILLS] + [modules(detail)])
        lines += (table(SHIP_HEAD, rows) if rows else ["No ship of this role in the fleet's file."]) + [""]
        lines += ["%d ships: %d on a route, %d waiting, %d by hand, %d not connected"
                  % (len(mine), counts["on a route"], counts["waiting"], counts["by hand"], counts["not connected"]), ""]
        total += len(mine)
    lines.append(END)
    return "\n".join(lines), total, roles_of(member)


def without_time(text):
    """The block's lines with the time of its stamp line taken out: what decides `unchanged`."""
    return [TIME.sub("<time>", line) if line.startswith(STAMP) else line for line in text.splitlines()]


def place(text, new):
    """(the file's new text, its old block or None). Raises Halt when the file holds one mark without the other."""
    lines = text.splitlines(keepends=True)
    begins = [n for n, line in enumerate(lines) if line.strip().startswith(BEGIN_MARK)]
    ends = [n for n, line in enumerate(lines) if line.strip().startswith(END_MARK)]
    if not begins and not ends:
        gap = "" if not text or text.endswith("\n\n") else "\n" if text.endswith("\n") else "\n\n"
        return text + gap + new + "\n", None
    if len(begins) != 1 or len(ends) != 1:
        raise Halt("it holds %d BEGIN and %d END marks (one of each, or none, is needed)" % (len(begins), len(ends)))
    b, e = begins[0], ends[0]
    if e < b:
        raise Halt("its END mark stands before its BEGIN mark")
    tail = lines[e][len(lines[e].rstrip("\r\n")):]
    return "".join(lines[:b]) + new + tail + "".join(lines[e + 1:]), "".join(lines[b:e + 1])


def git(folder, *args):
    done = subprocess.run(["git", "-C", str(folder)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def own_repository(folder):
    """True when the folder is the top of a git working tree (never a parent's repository)."""
    code, out = git(folder, "rev-parse", "--show-toplevel")
    return code == 0 and os.path.realpath(out.strip()) == os.path.realpath(str(folder))


def replace_file(path, raw, text):
    """Write `text` over the file through a temporary file in its folder and a rename, keeping its mode; raises Halt
    when the file changed since it was read as `raw`."""
    real = Path(os.path.realpath(str(path)))
    mode = stat.S_IMODE(real.stat().st_mode)
    fd, tmp = tempfile.mkstemp(dir=str(real.parent), prefix="." + real.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(text.encode("latin-1"))
        os.chmod(tmp, mode)
        if real.read_bytes() != raw:
            raise Halt("it changed while the block was built")
        os.replace(tmp, str(real))
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_member(path, new, member, commit):
    """The status word of one member's file: written, unchanged, committed <hash>, ...; raises Halt. `member` is who
    runs the script: the commit carries its name."""
    try:
        raw = Path(path).read_bytes()
    except OSError:
        raise Halt("there is no FLEET.md to write")
    text = raw.decode("latin-1")                    # byte for byte: every byte outside the marks comes back unchanged
    result, old = place(text, new)
    if old is not None and without_time(old) == without_time(new):
        return "unchanged"
    workspace = Path(path).parent
    repo = commit and own_repository(workspace)
    clean = repo and git(workspace, "status", "--porcelain", "--", "FLEET.md") == (0, "")
    replace_file(path, raw, result)
    if not commit:
        return "written"
    if not repo:
        return "written; not committed: no git repository"
    if not clean:
        return "written; not committed: FLEET.md carried an uncommitted change before the write"
    git(workspace, "add", "--", "FLEET.md")
    code, out = git(workspace, "-c", "user.name=" + member, "-c", "user.email=%s@suggi-workspace.dev" % member.lower(), "commit", "-q",
                    "-m", "FLEET.md: routes now (fleetfile.py)", "--", "FLEET.md")
    if code:
        return "written; NOT COMMITTED: " + " ".join(out.split())[-200:]
    return "committed " + git(workspace, "log", "-1", "--format=%h")[1].strip()


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data, profiles = value("--root", str(here.parent)), value("--data", division.DATA), value("--profiles", hive.PROFILES)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in OPTIONS)]
    flags = [a for n, a in enumerate(args) if a.startswith("--") and a not in OPTIONS and (n == 0 or args[n - 1] not in OPTIONS)]
    if any(a in ("-h", "--help") for a in args) or len(words) > 1 or any(f not in FLAGS for f in flags):
        print(__doc__)
        return 2
    kind, me = division.member()
    word = words[0].capitalize() if words else ""
    if word and word != "All" and word not in division.MEMBERS:
        print("REFUSED: `%s` is no member: %s, or all" % (words[0], ", ".join(division.MEMBERS)))
        return 2
    printing = "--print" in args
    if not word and kind != "member":
        print("REFUSED: this shell is no member of The Collective: it writes no FLEET.md (name a member with --print to read a block)")
        return 2
    targets = list(division.MEMBERS) if word == "All" else [word or me]
    if not printing:
        if kind != "member":
            print("REFUSED: this shell is no member of The Collective: it writes no FLEET.md (printing with --print is free)")
            return 2
        if me != "Unity" and targets != [me]:
            print("REFUSED: %s writes its own FLEET.md only; the Fleet Admiral may write any (asked: %s)" % (me, words[0]))
            return 2
    lock = None
    if not printing:                                # one writer at a time, from the reading to the commit; the lock goes with the process
        try:
            (Path(data) / "fleet").mkdir(parents=True, exist_ok=True)
            lock = open(Path(data) / "fleet" / "fleetfile.lock", "w")
            fcntl.flock(lock, fcntl.LOCK_EX)
        except OSError:
            lock = None                             # a data folder this shell cannot write: the write below is still one rename
    seen = read_state(root, data, time.time())
    halted = False
    for member in targets:
        new, ships, roles = block(seen, member)
        if printing:
            print(new + ("\n" if len(targets) > 1 else ""))
            continue
        lower = member.lower()
        path = Path(profiles) / lower / ("workspace-" + lower) / "FLEET.md"
        try:
            status = write_member(path, new, me, "--commit" in args)
        except Halt as why:
            print("HALT: %s: %s: %s; nothing written" % (member, path, why))
            halted = True
            continue
        print("%s: %s: %s (%d ships, %s)" % (member, status, path, ships, ", ".join(roles)))
    return 1 if halted else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
