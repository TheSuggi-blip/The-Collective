#!/usr/bin/env python3
"""rules.py -- the rulebook's standing rules: list them, find where each is cited, and gate their numbers.

WHAT: governance/rulebook.md section 12 holds the fleet's standing rules, one table row each
      (`| F<n> <title> | <text> |`); section 13 holds the retired numbers, one line each
      (`F<n> <title>: retired <YYYY-MM-DD>; now <where its meaning lives>`). This script reads both and answers:
        list        every rule: its number, the characters of its row, how many files of the repository cite it,
                    the dates its text names, its title; then every retired number with the files that cite it
        refs F<n>   every line that cites the number: in the repository (path:line), the files `check` reads apart
                    from the history it never reads; and on this machine, read only, the shared skills, every
                    member's skills (SKILL.md), SOUL.md and workspace AGENTS.md, ROSTER.md, MISSION.md, COLLECTIVE.md
        check       the gate (below); exit 1 on HALT
      A citation is `F<n>` as a word: `F8`, `rule F8`, `rules F8, F23`, `orders F3`, `(F27)`. A linter's code after
      `noqa:` (`# noqa: F401`) is no citation.
RULES (check):
  - Every F<n> cited in governance/, game/, scripts/, communications/protocol.md and the newest entry of
    communications/orders.log is a rule of section 12 or a retired number of section 13. Older entries of the logs,
    the reports and the archive are history: never checked.
  - No two rules share a title (compared without the parenthesis that follows it, in any case).
  - A number stands once: one rule or one retired line, never both, never twice. A number is never reused.
  - Every line of section 13 that starts with F<n> has the retired line's form.
  - The rulebook stays under RULEBOOK_MAX characters.
  - A retired number cited in the checked files is a warning, never an error: the old number still resolves through
    section 13, and the Fleet Admiral decides whether the line is rewritten.
WHY:  Suggi, 2026-11-18: "If we ever change and evolve our playstyle the rules and decisions need to be updated and
      changed" and "make it lean and make sure no info is doubled". A rule merged or retired stays findable under
      its old number, nothing cites a rule that does not exist, and the rulebook does not grow back (37,545
      characters before the lean draft of 2026-11-18).

USAGE:
  rules.py list           every rule and every retired number, with its citations
  rules.py refs F<n>      where the number is cited, here and in the members' skills and profiles
  rules.py check          the gate: exit 1 on HALT
  --root <dir>   repository root (default: the parent of this file's folder)
  --home <dir>   where the shared skills and the members' profiles are (default /opt/data); read by refs only

Stdlib only. ASCII only.
"""

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "game" / "fleet"))
import docs                                       # noqa: E402  the rulebook's one row parser: cells, RULE_ROW

RULEBOOK = "governance/rulebook.md"
RULEBOOK_MAX = 18169           # the lean rulebook of 2026-11-18 (15,799 characters) plus 15 percent
CHECKED = ("governance", "game", "scripts", "communications/protocol.md")    # and the newest entry of orders.log
ORDERS = "communications/orders.log"
HOME = "/opt/data"
OUTSIDE = (".agents/skills/**/*", "profiles/*/skills/**/SKILL.md", "profiles/*/SOUL.md",
           "profiles/*/workspace-*/AGENTS.md", "profiles/*/workspace-*/ROSTER.md",
           "profiles/*/workspace-*/MISSION.md", "profiles/*/workspace-*/COLLECTIVE.md")
SKIP = {".git", "__pycache__"}
CITE = re.compile(r"(?<![A-Za-z0-9_])F(\d+)(?![A-Za-z0-9_])")
NOQA = re.compile(r"noqa\s*:\s*[A-Z]+\d+(?:\s*,\s*[A-Z]+\d+)*")
SECTION = re.compile(r"^## (\d+)\.")
RETIRED = re.compile(r"^(?:[-*]\s+)?F(\d+) (.+?): retired (\d{4}-\d{2}-\d{2}); now (.+)$")
RETIRED_START = re.compile(r"^(?:[-*]\s+)?F\d+\b")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
SHOWN = 5                      # places named per number in an error line; refs names them all


def section_lines(text, number):
    """[(line number, line)] of the rulebook's section `## <number>.` up to the next `## ` heading."""
    out, inside = [], False
    for n, line in enumerate(text.splitlines(), 1):
        head = SECTION.match(line)
        if head or line.startswith("## "):
            inside = bool(head) and head.group(1) == str(number)
            continue
        if inside:
            out.append((n, line))
    return out


def base_title(title):
    """A rule's title without the parenthesis that follows it, lower case: `Stance (Suggi)` -> `stance`."""
    return title.split(" (", 1)[0].strip().lower()


def read_rulebook(root):
    """(rules, retired, problems, text). A rule: num, title, text, chars, line. A retired line: num, title, date,
    now, line. Problems: lines of section 13 that start with F<n> and break the form."""
    path = Path(root) / RULEBOOK
    text = path.read_text(encoding="ascii", errors="replace")
    rules, retired, problems = [], [], []
    for n, line in section_lines(text, 12):
        match = docs.RULE_ROW.match(line.strip())
        if not match:
            continue
        parts = docs.cells(line)
        head = parts[0]
        rules.append({"num": int(head[1:].split()[0]), "title": head.split(None, 1)[1] if " " in head else "",
                      "text": " | ".join(parts[1:]), "chars": len(line), "line": n})
    for n, line in section_lines(text, 13):
        if not RETIRED_START.match(line.strip()):
            continue
        match = RETIRED.match(line.strip())
        if match is None:
            problems.append((n, line.strip()))
            continue
        retired.append({"num": int(match.group(1)), "title": match.group(2), "date": match.group(3),
                        "now": match.group(4), "line": n})
    return rules, retired, problems, text


def cited(line):
    """The rule numbers a line cites, in order (a linter's `noqa:` codes left out)."""
    return [int(m.group(1)) for m in CITE.finditer(NOQA.sub("", line))]


def newest_entry_start(lines):
    """The index of the newest entry's header in orders.log's lines (the last `## [ENT-` line), or None."""
    heads = [i for i, line in enumerate(lines) if line.startswith("## [ENT-")]
    return heads[-1] if heads else None


def is_checked(rel):
    return any(rel == part or rel.startswith(part + "/") for part in CHECKED)


def repo_files(root):
    """Every text file of the repository, relative path sorted; .git, __pycache__ and binary files left out."""
    root = Path(root)
    out = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP)
        for name in sorted(files):
            path = Path(folder) / name
            try:
                raw = path.read_bytes()
            except OSError:
                continue
            if b"\x00" in raw[:4096]:
                continue
            out.append((path.relative_to(root).as_posix(), raw.decode("ascii", errors="replace")))
    return out


def citations(root):
    """[(number, rel path, line number, line, checked)] for every citation in the repository. checked: the file is
    one `check` reads (for orders.log: the line lies in its newest entry)."""
    out = []
    for rel, text in repo_files(root):
        lines = text.splitlines()
        start = newest_entry_start(lines) if rel == ORDERS else None
        for i, line in enumerate(lines):
            numbers = cited(line)
            if not numbers:
                continue
            checked = is_checked(rel) or (rel == ORDERS and start is not None and i >= start)
            out += [(num, rel, i + 1, line, checked) for num in numbers]
    return out


def outside_files(home):
    """[(path, text)] of the members' skills and profiles on this machine; what cannot be read is skipped."""
    home = Path(home)
    seen, out = set(), []
    for pattern in OUTSIDE:
        try:
            paths = sorted(home.glob(pattern))
        except OSError:
            continue
        for path in paths:
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            try:
                out.append((str(path), path.read_text(encoding="ascii", errors="replace")))
            except OSError:
                continue
    return out


def check(root):
    """(errors, warnings): the gate's lines."""
    errors, warnings = [], []
    path = Path(root) / RULEBOOK
    if not path.is_file():
        return ["%s: missing" % RULEBOOK], []
    rules, retired, problems, text = read_rulebook(root)
    if not rules:
        errors.append("%s: no rule row `| F<n> <title> | <text> |` in section 12" % RULEBOOK)
    if len(text) > RULEBOOK_MAX:
        errors.append("%s is %s characters, more than RULEBOOK_MAX %s: merge or move text before adding"
                      % (RULEBOOK, format(len(text), ","), format(RULEBOOK_MAX, ",")))
    for n, line in problems:
        errors.append("%s:%d: a retired line reads `F<n> <title>: retired <YYYY-MM-DD>; now <where>` (found `%s`)"
                      % (RULEBOOK, n, line[:80]))
    numbers = {r["num"] for r in rules}
    for item in retired:
        if item["num"] in numbers:
            errors.append("F%d is a rule of section 12 and a retired number of section 13 (line %d): a number stands once"
                          % (item["num"], item["line"]))
    for label, items in (("section 12", rules), ("section 13", retired)):
        count = {}
        for item in items:
            count[item["num"]] = count.get(item["num"], 0) + 1
        errors += ["F%d stands %d times in %s: a number is never used twice" % (num, count[num], label)
                   for num in sorted(count) if count[num] > 1]
    titles = {}
    for rule in rules:
        titles.setdefault(base_title(rule["title"]), []).append(rule["num"])
    for title, nums in sorted(titles.items()):
        if len(nums) > 1:
            errors.append("rules %s share the title `%s`" % (", ".join("F%d" % n for n in nums), title))
    known = numbers | {r["num"] for r in retired}
    gone = {r["num"]: r for r in retired}
    unknown, old = {}, {}
    for num, rel, n, _line, checked in citations(root):
        if not checked:
            continue
        if num not in known:
            unknown.setdefault(num, []).append("%s:%d" % (rel, n))
        elif num in gone and rel != RULEBOOK:
            old.setdefault(num, []).append("%s:%d" % (rel, n))
    for num in sorted(unknown):
        places = unknown[num]
        errors.append("F%d is cited but is no rule and no retired number: %s%s" % (num, ", ".join(places[:SHOWN]),
                      " and %d more" % (len(places) - SHOWN) if len(places) > SHOWN else ""))
    for num in sorted(old):
        places = old[num]
        files = len({p.rsplit(":", 1)[0] for p in places})
        warnings.append("F%d is retired (now %s): cited %d times in %d checked files; `rules.py refs F%d` lists them"
                        % (num, gone[num]["now"], len(places), files, num))
    return errors, warnings


def show_list(root):
    rules, retired, problems, text = read_rulebook(root)
    files = {}
    for num, rel, _n, _line, _checked in citations(root):
        if rel != RULEBOOK:
            files.setdefault(num, set()).add(rel)
    print("RULES %d | section 12 of %s, %s characters of RULEBOOK_MAX %s | files: files of the repository other than "
          "the rulebook that cite the number, history included" % (len(rules), RULEBOOK, format(len(text), ","),
                                                                    format(RULEBOOK_MAX, ",")))
    print("%-5s %6s %6s  %-24s %s" % ("rule", "chars", "files", "dates", "title"))
    for rule in rules:
        dates = sorted(set(DATE.findall(rule["title"] + " " + rule["text"])))
        print("%-5s %6d %6d  %-24s %s" % ("F%d" % rule["num"], rule["chars"], len(files.get(rule["num"], ())),
                                         ", ".join(dates) or "-", rule["title"]))
    print("RETIRED %d | section 13: a number is never reused; an old text citing it means the rule named" % len(retired))
    for item in retired:
        print("F%-4d %6s %6d  %s: retired %s; now %s" % (item["num"], "", len(files.get(item["num"], ())), item["title"],
                                                         item["date"], item["now"]))
    for n, line in problems:
        print("NOT READ line %d of section 13: %s" % (n, line[:100]))
    return 0


def show_refs(root, home, number):
    rules, retired, _problems, _text = read_rulebook(root)
    rule = next((r for r in rules if r["num"] == number), None)
    gone = next((r for r in retired if r["num"] == number), None)
    if rule is not None:
        print("F%d %s | a rule of section 12, line %d" % (number, rule["title"], rule["line"]))
    elif gone is not None:
        print("F%d %s | retired %s; now %s (section 13, line %d)" % (number, gone["title"], gone["date"], gone["now"], gone["line"]))
    else:
        print("F%d | no rule and no retired number" % number)
    found = [c for c in citations(root) if c[0] == number]
    for checked, label in ((True, "IN THE FILES `check` READS"), (False, "IN THE REST OF THE REPOSITORY (history and files the gate does not read)")):
        mine = [c for c in found if c[4] == checked]
        print("%s: %d" % (label, len(mine)))
        for _num, rel, n, line, _c in mine:
            print("  %s:%d: %s" % (rel, n, line.strip()[:160]))
    if home is None:
        return 0
    outside = []
    for path, text in outside_files(home):
        for n, line in enumerate(text.splitlines(), 1):
            if number in cited(line):
                outside.append("  %s:%d: %s" % (path, n, line.strip()[:160]))
    print("ON THIS MACHINE (%s: shared skills, members' skills, SOUL.md, workspace AGENTS.md, ROSTER.md, MISSION.md, "
          "COLLECTIVE.md; read only): %d" % (home, len(outside)))
    for line in outside:
        print(line)
    return 0


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="The rulebook's standing rules: list, refs, check.")
    parser.add_argument("command", choices=("list", "refs", "check"))
    parser.add_argument("number", nargs="?", help="refs: the rule, F<n> or <n>")
    parser.add_argument("--root", default=str(here.parent))
    parser.add_argument("--home", default=HOME)
    parser.add_argument("--no-home", action="store_true", help="refs: the repository only")
    args = parser.parse_args()
    if not (Path(args.root) / RULEBOOK).is_file():
        print("HALT: %s not found under %s" % (RULEBOOK, args.root))
        return 1
    if args.command == "refs":
        match = re.fullmatch(r"[Ff]?(\d+)", args.number or "")
        if match is None:
            parser.error("refs takes a rule: F<n>")
        return show_refs(args.root, None if args.no_home else args.home, int(match.group(1)))
    if args.number:
        parser.error("only refs takes a rule")
    if args.command == "list":
        return show_list(args.root)
    errors, warnings = check(args.root)
    for line in errors:
        print("ERROR " + line)
    for line in warnings:
        print("WARN " + line)
    rules, retired, _problems, text = read_rulebook(args.root)
    print("%s: %d rules, %d retired numbers, %s of RULEBOOK_MAX %s characters" % ("HALT" if errors else "PASS", len(rules),
          len(retired), format(len(text), ","), format(RULEBOOK_MAX, ",")))
    print("Errors: %d | Warnings: %d" % (len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
