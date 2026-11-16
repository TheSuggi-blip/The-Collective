#!/usr/bin/env python3
"""fleet-index.py -- build game/fleet/index.md: every script of the fleet folder, what it does and how to call it.

WHAT: game/fleet/ holds the scripts the fleet is played with (the dispatcher,
      the runners, the tools). This script reads the docstring of each one
      and writes game/fleet/index.md: one table of all scripts (what each
      does, how it is run) and, per script, its full first paragraph and its
      command forms. The index is for the agents: an agent reads it before
      it runs or writes a fleet script.
RULES:
  - The index is built from the scripts' own docstrings, never written by
    hand: what a script says about itself is what the index says.
  - Every script of game/fleet/ starts with a docstring whose first
    paragraph says what the script does and that carries a `Usage:` (or
    `USAGE:`) block: the command forms, one per line, the lines after the
    heading indented. A script without them is an error and nothing is
    written: an agent cannot use what it cannot read.
  - The scripts are read, never run.
  - How a script is run is derived: a service when its usage says
    `run forever`; a runner when the dispatcher's docstring names it after
    `->` with the kind of route it flies; by hand otherwise.
  - The file is rewritten only when its text changed; its id is kept.
  - --commit commits the index by path as Unity when it was written. It
    writes nothing while game/fleet/ holds another change that is not
    committed: that is a member's work in progress.
WHY:  scripts for playing accumulate. A list kept by hand goes stale with
      the first new script; this one cannot say more or less than the
      scripts do.

USAGE:
  fleet-index.py              write game/fleet/index.md when it changed
  fleet-index.py --check      the gate: exit 1 when a script breaks the rule, or the index is stale or missing
  fleet-index.py --commit     write, and commit the index by path as Unity (the hourly job)
  --root <dir>                repository root (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import argparse
import ast
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path

FOLDER = "game/fleet"
INDEX = "index.md"
USAGE = re.compile(r"^\s*usage:\s*(.*)$", re.I)
RUNNER = re.compile(r"^\s*([a-z_]+)\s+->\s+(?:game/fleet/)?([A-Za-z0-9_]+\.py)\b")
PYTHON = re.compile(r"^python3?(?: -[A-Za-z]+)* ")
ID = re.compile(r"^id: (\S+)$", re.M)


def docstring(path):
    """(docstring, problem) of one script, read as text and never run."""
    try:
        return ast.get_docstring(ast.parse(path.read_text(encoding="ascii"))) or "", ""
    except (OSError, UnicodeDecodeError, SyntaxError, ValueError) as error:
        return "", "not readable as ASCII Python (%s)" % type(error).__name__


def read_script(path):
    """{name, summary, usage, problem} of one script: its first paragraph and the lines of its Usage block."""
    doc, problem = docstring(path)
    out = {"name": path.name, "summary": "", "usage": [], "problem": problem}
    if problem:
        return out
    if not doc.strip():
        return dict(out, problem="no docstring")
    lines = doc.split("\n")
    first = []
    for line in lines:
        if not line.strip():
            break
        first.append(line.strip())
    summary = " ".join(first)
    if summary.startswith(path.name + " -- "):
        summary = summary[len(path.name) + 4:]
    out["summary"] = summary[:1].upper() + summary[1:]
    for number, line in enumerate(lines):
        match = USAGE.match(line)
        if not match:
            continue
        rest = []
        for more in lines[number + 1:]:
            if not more.strip() or not more[:1].isspace():
                break
            rest.append(more.rstrip())
        rest = textwrap.dedent("\n".join(rest)).split("\n") if rest else []
        head = match.group(1).strip()
        usage = ([head] + ["    " + more.strip() for more in rest]) if head else rest
        out["usage"] = [PYTHON.sub("", more) for more in usage]
        break
    if len(out["summary"]) < 20 or USAGE.match(first[0]):
        out["problem"] = "the docstring's first paragraph does not say what the script does"
    elif not out["usage"]:
        out["problem"] = "the docstring has no `Usage:` block"
    return out


def read_folder(root):
    """(scripts, errors): every .py of game/fleet/ by name, and what breaks the rule."""
    folder = Path(root) / FOLDER
    scripts = [read_script(path) for path in sorted(folder.glob("*.py"))] if folder.is_dir() else []
    flown = {}
    doc, _problem = docstring(folder / "dispatch.py") if (folder / "dispatch.py").is_file() else ("", "")
    for line in doc.split("\n"):
        match = RUNNER.match(line)
        if match:
            flown[match.group(2)] = match.group(1)
    for script in scripts:
        if any("run forever" in line for line in script["usage"]):
            script["how"], script["run"] = "Service", "A service: it runs by itself and is never started a second time"
        elif script["name"] in flown:
            script["how"] = "Runner (`%s` routes)" % flown[script["name"]]
            script["run"] = "A runner: the dispatcher starts it for a route of the kind `%s`; by hand only for a test with one free pilot" % flown[script["name"]]
        else:
            script["how"], script["run"] = "By hand", "Run by hand"
    return scripts, ["%s/%s: %s" % (FOLDER, s["name"], s["problem"]) for s in scripts if s["problem"]]


def cell(text):
    return " ".join(str(text).split()).replace("|", "/")


def sentence(text):
    """The first sentence of a paragraph."""
    cut = re.search(r"\.(?:\s|$)", text)
    return text[:cut.start() + 1] if cut else text


def body(scripts):
    """The index text below its frontmatter."""
    lines = ["# index.md -- The Fleet's Scripts", "",
             "Built by `python3 -B scripts/fleet-index.py` from the docstring of every script in this",
             "folder; never edited by hand. Scripts listed: %d." % len(scripts), "",
             "- Run a script from the repository root: `python3 -I -B game/fleet/<script> <arguments>`,",
             "  the arguments as listed under \"How to Call Each\".",
             "- Copy a call from here or from a script that works, never from memory.",
             "- A runner holds its pilot's order file while it runs, so two programs never drive one",
             "  pilot: start none for a pilot that is at work. The file `fleet/STOP` in the unit's data",
             "  folder halts every start.",
             "- Who may command which ship is in the orders in force (`communications/orders.log`).",
             "- The tasks the runners fly: `game/routes/master-index.md`. How each kind of work is done: the",
             "  shared skill `fleet-play`.",
             "- A new script: its docstring starts with one paragraph that says what the script does",
             "  and carries a `Usage:` block, one command form per line. Then run the builder.",
             "  `python3 -B scripts/fleet-index.py --check` fails a script without them and a stale index.",
             "", "## Scripts", "", "| Script | What it does | How it is run |", "|---|---|---|"]
    for script in scripts:
        lines.append("| `%s` | %s | %s |" % (script["name"], cell(sentence(script["summary"])), script["how"]))
    lines += ["", "## How to Call Each"]
    for script in scripts:
        lines += ["", "### `%s`" % script["name"], ""] + textwrap.wrap(script["summary"], 88) + ["", script["run"] + ".", "", "```"] + script["usage"] + ["```"]
    return "\n".join(lines) + "\n"


def split_index(path):
    """(frontmatter, body) of the index on disk; ('', '') when there is none."""
    try:
        text = path.read_text(encoding="ascii")
    except (OSError, UnicodeDecodeError):
        return "", ""
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        end = text.index("\n---\n", 4) + 5
        return text[:end], text[end:].lstrip("\n")
    return "", text


def state(root, scripts):
    """`current`, `stale` or `missing`."""
    front, old = split_index(Path(root) / FOLDER / INDEX)
    if not front and not old:
        return "missing"
    return "current" if front and old == body(scripts) else "stale"


def new_id(now):
    """A timestamp id of this moment, never one ending on :00."""
    while time.gmtime(now).tm_sec == 0:
        now -= 1
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(now))


def write(root, scripts, now):
    """Write the index when its text changed; True when it was written. The id of an existing index is kept."""
    path = Path(root) / FOLDER / INDEX
    if state(root, scripts) == "current":
        return False
    front, _old = split_index(path)
    found = ID.search(front)
    front = "---\nname: fleet-index\nid: %s\ntier: intel\nauthor: Unity\n---\n" % (found.group(1) if found else new_id(now))
    tmp = path.with_name(INDEX + ".tmp")
    tmp.write_text(front + "\n" + body(scripts), encoding="ascii")
    tmp.replace(path)
    return True


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Build game/fleet/index.md from the docstrings of the fleet's scripts.")
    parser.add_argument("--root", default=str(here.parent))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    root, rel = Path(args.root).resolve(), "%s/%s" % (FOLDER, INDEX)
    if args.commit:
        _code, out = git(root, "status", "--porcelain", "--untracked-files=all", "--", FOLDER)
        other = sorted(line[3:] for line in out.splitlines() if line[3:] != rel)
        if other:
            print("%s: not built; %s holds changes that are not committed: %s" % (rel, FOLDER, ", ".join(other)))
            return 0
    scripts, errors = read_folder(root)
    if args.check:
        result = state(root, scripts)
        print("%s: %s" % (rel, result))
        if result != "current":
            errors.append("%s is %s: run `python3 -B scripts/fleet-index.py`" % (rel, result))
        for line in errors:
            print("ERROR: " + line)
        print("Errors: %d | Warnings: 0" % len(errors))
        return 1 if errors else 0
    for line in errors:
        print("ERROR: " + line)
    if errors:
        print("%s: not written; fix the script(s) above" % rel)
        return 1
    if not scripts:
        print("%s: no script in %s; nothing written" % (rel, FOLDER))
        return 0
    written = write(root, scripts, time.time())
    print("%s: %s" % (rel, "written" if written else "current"))
    if written and args.commit:
        git(root, "add", "--", rel)
        code, out = git(root, "-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev", "commit", "-q", "-m",
                        "%s: rebuilt from the scripts' docstrings" % rel, "--", rel)
        if code:
            print("%s: written but NOT COMMITTED: %s" % (rel, out.strip()[:200]))
            return 1
        print("%s: committed" % rel)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
