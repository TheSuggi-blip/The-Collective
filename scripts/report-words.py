#!/usr/bin/env python3
"""report-words.py -- the word gate for reports/: every section holds at least its minimum of words.

WHAT: governance/template-reports.md sets a minimum number of words for
      each section of a report (its table "Minimum Length"). An agent
      cannot count 250 words by eye; this script counts them.
RULES:
  - The minimums are read from the template's table, never from this
    file: a number changed there is the number checked here. A cell
    with a number is a minimum, `none` means no minimum, `--` means the
    section is not part of that kind of report.
  - The kind of a report: one with a `## Strategy` section is a fleet
    report, any other a division report (the rule of
    check-report-format.sh).
  - A word is a run of characters between spaces that holds a letter or
    a digit. Everything between a section's `##` heading and the next
    one counts, lists, tables and sub-headings included; code-fence
    lines and table rule lines do not.
  - A section the kind needs and the report lacks is an error here too.
  - `--template-check` checks the template itself: the table is
    readable, and the two checklist lines that name the minimums say
    the same numbers as the table.
WHY:  a minimum that has to be counted by the writer is guessed. The
      gate says how many words each section holds and how many it needs.

USAGE:
  report-words.py reports/<file>.md [more files]
  report-words.py --template-check
  --root <dir>   repository root (default: the parent of this file's folder)

PASS: one line per section, then `REPORT WORDS: PASS`, exit 0.
HALT: the same lines, then `REPORT WORDS: HALT`, exit 1.
It counts words. Whether the words carry facts is the writer's gate.

Stdlib only. ASCII only.
"""

import argparse
import re
import sys
from pathlib import Path

TEMPLATE = "governance/template-reports.md"
KINDS = ("division", "fleet")
HAS_WORD = re.compile(r"[A-Za-z0-9]")
RULE_ROW = re.compile(r"^\s*\|?[\s|:-]+\|?\s*$")


def minimums(root):
    """({kind: {section: minimum words}}, errors) from the template's Minimum Length table."""
    out, errors = {kind: {} for kind in KINDS}, []
    try:
        lines = (Path(root) / TEMPLATE).read_text(encoding="ascii").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        return out, ["%s: not readable: %s" % (TEMPLATE, error)]
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "### Minimum Length")
    except StopIteration:
        return out, ["%s: no `### Minimum Length` heading" % TEMPLATE]
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if line.startswith("|"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    if len(rows) < 3 or [c.lower() for c in rows[0]] != ["section", "division report", "fleet report"]:
        return out, ["%s: the Minimum Length table must start with `| Section | Division report | Fleet report |`" % TEMPLATE]
    for cells in rows[2:]:
        if len(cells) != 3:
            errors.append("%s: Minimum Length row with %d cells: %s" % (TEMPLATE, len(cells), " | ".join(cells)))
            continue
        for kind, cell in zip(KINDS, cells[1:]):
            if cell == "--":
                continue
            if cell == "none":
                out[kind][cells[0]] = 0
            elif cell.isdigit() and int(cell) > 0:
                out[kind][cells[0]] = int(cell)
            else:
                errors.append("%s: Minimum Length of %s (%s report) is `%s`: a number, `none` or `--`" % (TEMPLATE, cells[0], kind, cell))
    for kind in KINDS:
        if not any(out[kind].values()):
            errors.append("%s: the Minimum Length table sets no minimum for a %s report" % (TEMPLATE, kind))
    return out, errors


def template_check(root):
    """Errors of the template: the table, and the checklist lines that repeat its numbers."""
    wanted, errors = minimums(root)
    if errors:
        return errors
    text = (Path(root) / TEMPLATE).read_text(encoding="ascii")
    for kind in KINDS:
        match = re.search(r"^- \[ \] %s report, minimum words: (.+?)\s+\(PASS / HALT\)\s*$" % kind.capitalize(), text, re.M)
        if match is None:
            errors.append("%s: no checklist line `- [ ] %s report, minimum words: ...`" % (TEMPLATE, kind.capitalize()))
            continue
        said = {}
        for part in match.group(1).split(","):
            name, _space, number = part.strip().rpartition(" ")
            if number.isdigit():
                said[name] = int(number)
        table = {name: number for name, number in wanted[kind].items() if number}
        if said != table:
            errors.append("%s: the checklist line of the %s report says %s, the table says %s" % (TEMPLATE, kind, said, table))
    return errors


def sections(text):
    """{heading: words} for every `## ` section of a report's body, and the kind of the report."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":                    # skip the frontmatter
        try:
            lines = lines[lines.index("---", 1) + 1:]
        except ValueError:
            pass
    counts, current, fenced = {}, None, False
    for line in lines:
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced and line.startswith("## "):
            current = line[3:].strip()
            counts[current] = 0
            continue
        if current is None or RULE_ROW.match(line):
            continue
        counts[current] += sum(1 for token in line.split() if HAS_WORD.search(token))
    return counts, ("fleet" if "Strategy" in counts else "division")


def check(path, wanted):
    """(lines to print, number of sections under their minimum or missing) for one report."""
    try:
        text = Path(path).read_text(encoding="ascii", errors="replace")
    except OSError as error:
        return ["%s: not readable: %s" % (path, error)], 1
    counts, kind = sections(text)
    lines, short = ["%s (%s report)" % (path, kind)], 0
    for name, minimum in wanted[kind].items():
        if name not in counts:
            lines.append("  %-15s missing" % name)
            short += 1
        elif counts[name] < minimum:
            lines.append("  %-15s %4d words, minimum %d: SHORT by %d" % (name, counts[name], minimum, minimum - counts[name]))
            short += 1
        else:
            lines.append("  %-15s %4d words, minimum %s: OK" % (name, counts[name], minimum or "none"))
    return lines, short


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="The word gate for reports: every section holds at least its minimum of words.")
    parser.add_argument("files", nargs="*")
    parser.add_argument("--root", default=str(here.parent))
    parser.add_argument("--template-check", action="store_true")
    args = parser.parse_args()
    if args.template_check:
        errors = template_check(args.root)
        for line in errors:
            print("ERROR " + line)
        print("Errors: %d | Warnings: 0" % len(errors))
        return 1 if errors else 0
    if not args.files:
        parser.error("name a report, or use --template-check")
    wanted, errors = minimums(args.root)
    if errors:
        for line in errors:
            print("ERROR " + line)
        print("REPORT WORDS: HALT -- the template's minimums are not readable")
        return 1
    short = 0
    for path in args.files:
        lines, count = check(path, wanted)
        print("\n".join(lines))
        short += count
    if short:
        print("REPORT WORDS: HALT -- %d section(s) missing or under their minimum; write what was done, measured, checked or weighed" % short)
        return 1
    print("REPORT WORDS: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
