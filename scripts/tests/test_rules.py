"""rules.py on disposable trees: the rule rows and the retired list, each rule of the gate, list, refs, and the real
rulebook passing its own gate."""

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "rules.py"
spec = importlib.util.spec_from_file_location("rules_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules)

NONE = "F" + "99"              # a number no rulebook holds, built here so that this file cites no such rule itself

RULEBOOK = """---
name: rulebook
---

# rulebook.md -- a test

Rules F1 to F7 below.

## 8. Rules of Engagement

Fired upon: F2.

## 12. Standing Rules

| Rule | Says |
|---|---|
| F1 Chain of command | Each Admiral commands its own ships; a pipe \\| stays in its cell |
| F2 Stance (Suggi) | No ship fires first (2026-11-15) |
| F3 Anywhere (Suggi, 2026-11-16) | Every ship may work anywhere (2026-11-16, 2026-11-17) |
| F7 Wallets (Suggi) | Every pilot keeps 3,000 cr |

## 13. Retired Rules

- F5 Fleet size: retired 2026-11-18; now section 8.3
- F6 Never used: retired 2026-11-16; now nothing
"""
ORDERS = """## [ENT-001] | 2026-01-01 08:00 UTC | Unity | order
Changed: first.
In force from now.
P1. An old order cites %s: history.

## [ENT-002] | 2026-01-01 12:00 UTC | Unity | order | see: ENT-001
Changed: second.
In force from now.
P1. Work inside rule F3 and rules F1, F7.
""" % NONE


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rules-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.home = Path(self.temp.name) / "home"
        self.put("governance/rulebook.md", RULEBOOK)
        self.put("communications/orders.log", ORDERS)
        self.put("communications/protocol.md", "The standing rules (F1 to F7) are section 12.\n")
        self.put("game/routes/a.json", '{"note": "hold empty on the way out (orders F3); see F6"}\n')
        self.put("scripts/x.py", "import atexit  # noqa: F401  not a rule\nLIMIT = 3  # rule F7\n")
        self.put("reports/old.md", "An old report cites %s: history.\n" % NONE)
        self.put("communications/archive/orders-2026-01-01.log", "## [ENT-000] | 2026-01-01 07:00 UTC | Unity | order\n%s\n" % NONE)

    def put(self, rel, text, root=None):
        path = (root or self.root) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="ascii")
        return path

    def errors(self):
        return rules.check(str(self.root))[0]

    def run_command(self, function, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = function(str(self.root), *args)
        return code, out.getvalue()


class ReadTests(Tree):
    def test_the_rows_of_section_12_and_the_lines_of_section_13(self):
        found, retired, problems, text = rules.read_rulebook(str(self.root))
        self.assertEqual([(r["num"], r["title"]) for r in found],
                         [(1, "Chain of command"), (2, "Stance (Suggi)"), (3, "Anywhere (Suggi, 2026-11-16)"), (7, "Wallets (Suggi)")])
        self.assertEqual(found[0]["text"], "Each Admiral commands its own ships; a pipe \\| stays in its cell")
        self.assertEqual([(r["num"], r["title"], r["date"], r["now"]) for r in retired],
                         [(5, "Fleet size", "2026-11-18", "section 8.3"), (6, "Never used", "2026-11-16", "nothing")])
        self.assertEqual((problems, len(text)), ([], len(RULEBOOK)))

    def test_a_citation_is_a_word_and_a_linter_code_is_none(self):
        self.assertEqual(rules.cited("rule F8, rules F8, F23 (F27); orders F13."), [8, 8, 23, 27, 13])
        self.assertEqual(rules.cited("import atexit  # noqa: F401, E402 and UF6 and F8x and xF8"), [])


class GateTests(Tree):
    def test_the_clean_tree_passes_and_a_retired_number_cited_is_a_warning(self):
        errors, warnings = rules.check(str(self.root))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, ["F6 is retired (now nothing): cited 1 times in 1 checked files; `rules.py refs F6` lists them"])

    def test_an_unknown_number_in_each_checked_place_halts(self):
        for rel in ("governance/strategy.md", "game/fleet/x.py", "scripts/tests/test_y.py", "communications/protocol.md"):
            before = (self.root / rel).read_text(encoding="ascii") if (self.root / rel).is_file() else None
            self.put(rel, "line one\nas rule %s says\n" % NONE)
            self.assertEqual(self.errors(), ["%s is cited but is no rule and no retired number: %s:2" % (NONE, rel)], rel)
            if before is None:
                (self.root / rel).unlink()
            else:
                self.put(rel, before)
        self.assertEqual(self.errors(), [])
        self.put("communications/orders.log", ORDERS + "T1. Mind %s.\n" % NONE)
        self.assertEqual(self.errors(), ["%s is cited but is no rule and no retired number: communications/orders.log:%d" % (NONE, ORDERS.count("\n") + 1)])

    def test_history_is_never_checked(self):
        self.put("communications/queue.log", "## [ENT-001] | 2026-01-01 08:00 UTC | Zero | general\nper %s\n" % NONE)
        self.put("reports/2026-01-01_x.md", "%s\n" % NONE)
        self.assertEqual(self.errors(), [])                                  # old orders entry, archive, logs, reports

    def test_two_rules_with_one_title_halt(self):
        self.put("governance/rulebook.md", RULEBOOK.replace("| F7 Wallets (Suggi) |", "| F7 stance (Fleet Admiral) |"))
        self.assertEqual(self.errors(), ["rules F2, F7 share the title `stance`"])

    def test_a_retired_number_that_is_also_a_rule_halts_and_a_number_stands_once(self):
        self.put("governance/rulebook.md", RULEBOOK + "- F3 Anywhere: retired 2026-11-18; now F1\n")
        self.assertIn("F3 is a rule of section 12 and a retired number of section 13 (line %d): a number stands once" % (len(RULEBOOK.splitlines()) + 1), self.errors())
        self.put("governance/rulebook.md", RULEBOOK + "- F6 Never used: retired 2026-11-16; now nothing\n")
        self.assertEqual(self.errors(), ["F6 stands 2 times in section 13: a number is never used twice"])
        self.put("governance/rulebook.md", RULEBOOK.replace("| F7 Wallets (Suggi) |", "| F7 Wallets (Suggi) |\n| F7 Purse |"))
        self.assertEqual(self.errors(), ["F7 stands 2 times in section 12: a number is never used twice"])

    def test_a_retired_line_out_of_form_halts(self):
        self.put("governance/rulebook.md", RULEBOOK + "- F7 Wallets, retired some day\n")
        self.assertEqual(self.errors(), ["governance/rulebook.md:%d: a retired line reads `F<n> <title>: retired <YYYY-MM-DD>; "
                                         "now <where>` (found `- F7 Wallets, retired some day`)" % (len(RULEBOOK.splitlines()) + 1)])

    def test_the_rulebook_over_its_ceiling_halts(self):
        self.addCleanup(setattr, rules, "RULEBOOK_MAX", rules.RULEBOOK_MAX)
        rules.RULEBOOK_MAX = len(RULEBOOK)
        self.assertEqual(self.errors(), [])
        rules.RULEBOOK_MAX = len(RULEBOOK) - 1
        self.assertEqual(self.errors(), ["governance/rulebook.md is %s characters, more than RULEBOOK_MAX %s: merge or move text "
                                         "before adding" % (format(len(RULEBOOK), ","), format(len(RULEBOOK) - 1, ","))])

    def test_the_command_exits_1_on_halt(self):
        self.put("game/b.md", "%s\n" % NONE)
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "check", "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("HALT: 4 rules, 2 retired numbers", done.stdout)
        self.assertTrue(done.stdout.rstrip().endswith("Errors: 1 | Warnings: 1"))


class HelperTests(Tree):
    def test_list_names_each_rule_its_size_citations_dates_and_the_retired(self):
        code, text = self.run_command(rules.show_list)
        self.assertEqual(code, 0)
        rows = {line.split()[0]: line for line in text.splitlines() if line[:1] == "F"}
        self.assertRegex(rows["F3"], r"^F3 +\d+ +2  2026-11-16, 2026-11-17 +Anywhere \(Suggi, 2026-11-16\)$")   # orders, a.json
        self.assertRegex(rows["F7"], r"^F7 +\d+ +3  - +Wallets \(Suggi\)$")                                     # protocol, orders, x.py
        self.assertIn("Fleet size: retired 2026-11-18; now section 8.3", rows["F5"])
        self.assertIn("RETIRED 2 |", text)

    def test_refs_finds_the_repository_and_this_machine_and_skips_what_it_cannot_read(self):
        self.put(".agents/skills/spacemolt/fleet-play/SKILL.md", "Rule F3: anywhere.\n", self.home)
        self.put("profiles/zero/skills/mine/SKILL.md", "x\nper F3\n", self.home)
        self.put("profiles/zero/SOUL.md", "F3 too\n", self.home)
        self.put("profiles/zero/workspace-zero/ROSTER.md", "nothing\n", self.home)
        self.put("profiles/zero/workspace-zero/AGENTS.md", "see F3\n", self.home)
        self.put("profiles/zero/notes.md", "F3 here is not read\n", self.home)
        closed = self.put("profiles/zero/workspace-zero/MISSION.md", "F3 closed\n", self.home)
        os.chmod(closed, 0)
        self.addCleanup(os.chmod, closed, 0o644)
        code, text = self.run_command(rules.show_refs, str(self.home), 3)
        self.assertEqual(code, 0)
        self.assertIn("F3 Anywhere (Suggi, 2026-11-16) | a rule of section 12, line %d" % (RULEBOOK.splitlines().index(next(l for l in RULEBOOK.splitlines() if l.startswith("| F3 "))) + 1), text)
        self.assertIn("IN THE FILES `check` READS: 3", text)
        self.assertIn("  communications/orders.log:9: P1. Work inside rule F3 and rules F1, F7.", text)
        self.assertIn("  game/routes/a.json:1:", text)
        self.assertNotIn("notes.md", text)
        lines = [line for line in text.splitlines() if line.startswith("  " + str(self.home))]
        self.assertEqual(len([line for line in lines if "MISSION.md" not in line]), 4, text)
        self.assertEqual(any("MISSION.md" in line for line in lines), os.access(closed, os.R_OK))   # a closed file is skipped
        code, text = self.run_command(rules.show_refs, None, 6)
        self.assertIn("F6 Never used | retired 2026-11-16; now nothing", text)
        self.assertNotIn("ON THIS MACHINE", text)


class RealRepositoryTests(unittest.TestCase):
    def test_the_rulebook_of_this_tree_passes_its_gate(self):
        root = SCRIPT.parents[1]
        errors, _warnings = rules.check(str(root))
        self.assertEqual(errors, [])
        found, retired, _problems, text = rules.read_rulebook(str(root))
        self.assertLessEqual(len(text), rules.RULEBOOK_MAX)
        self.assertEqual(sorted(r["num"] for r in found + retired), list(range(1, len(found) + len(retired) + 1)))   # no gap


if __name__ == "__main__":
    unittest.main()
