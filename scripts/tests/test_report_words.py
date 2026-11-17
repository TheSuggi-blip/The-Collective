"""report-words.py: the minimums come from the template's table; each section is counted; the template agrees with itself."""

import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "report-words.py"
spec = importlib.util.spec_from_file_location("report_words_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
words = importlib.util.module_from_spec(spec)
spec.loader.exec_module(words)

TEMPLATE = """# A template of the test tree

- [ ] Division report, minimum words: Situation 5, Problems 3  (PASS / HALT)
- [ ] Fleet report, minimum words: Situation 5, Strategy 4  (PASS / HALT)

### Minimum Length

| Section | Division report | Fleet report |
|---|---|---|
| Situation | 5 | 5 |
| Problems | 3 | -- |
| Strategy | -- | 4 |
| Cross-links | none | none |

## The Next Heading

| Section | Division report | Fleet report |
|---|---|---|
| Situation | 999 | 999 |
"""
FRONT = "---\nname: x\nid: 20260101T000001Z\n---\n\n# Mining -- a title of many words that count for nothing\n\n"
GOOD = "## Situation\n\nOne two three four five.\n\n## Problems\n\nNone were found.\n\n## Cross-links\n\n"


def flat(line):
    return " ".join(line.split())


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="report-words-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "governance").mkdir()
        (self.root / "reports").mkdir()
        self.template(TEMPLATE)

    def template(self, text):
        (self.root / "governance" / "template-reports.md").write_text(text, encoding="ascii")

    def report(self, body):
        path = self.root / "reports" / "2026-01-01_zero_x.md"
        path.write_text(FRONT + body, encoding="ascii")
        return str(path)

    def run_check(self, body):
        wanted, errors = words.minimums(str(self.root))
        self.assertEqual(errors, [])
        return words.check(self.report(body), wanted)

    def run_main(self, *argv):
        out, old = io.StringIO(), sys.argv
        sys.argv = ["report-words.py", "--root", str(self.root)] + list(argv)
        try:
            with contextlib.redirect_stdout(out):
                code = words.main()
        finally:
            sys.argv = old
        return code, out.getvalue()


class CountTests(Tree):
    def test_the_minimums_are_the_table_under_the_heading_and_nothing_else(self):
        wanted, errors = words.minimums(str(self.root))
        self.assertEqual(errors, [])
        self.assertEqual(wanted, {"division": {"Situation": 5, "Problems": 3, "Cross-links": 0}, "fleet": {"Situation": 5, "Strategy": 4, "Cross-links": 0}})

    def test_a_report_with_enough_words_in_every_section_passes(self):
        lines, short = self.run_check(GOOD)
        self.assertEqual(short, 0, lines)
        self.assertTrue(lines[0].endswith("(division report)"))
        self.assertEqual([flat(line) for line in lines[1:]],
                         ["Situation 5 words, minimum 5: OK", "Problems 3 words, minimum 3: OK", "Cross-links 0 words, minimum none: OK"])

    def test_a_short_section_and_a_missing_one_halt(self):
        lines, short = self.run_check("## Situation\n\nOne two three four.\n\n## Cross-links\n")
        self.assertEqual(short, 2)
        self.assertEqual([flat(line) for line in lines[1:3]], ["Situation 4 words, minimum 5: SHORT by 1", "Problems missing"])

    def test_what_counts_as_a_word(self):
        body = ("## Situation\n\n"
                "- Ships: 55 -- idle 0\n"                                 # 4: the dashes hold no letter and no digit
                "| Route | Credits |\n|---|---|\n| hunt | 3,220 |\n"       # 2, the rule row 0, 2
                "### A sub-heading\n"                                     # 2
                "```\nShips: 1/1\n```\n"                                  # 2: the fence lines count for nothing, the line inside does
                "## Problems\n\nNone.\n\n## Cross-links\n")
        counts, kind = words.sections(FRONT + body)
        self.assertEqual((counts, kind), ({"Situation": 12, "Problems": 1, "Cross-links": 0}, "division"))

    def test_a_heading_inside_a_code_fence_opens_no_section(self):
        counts, _kind = words.sections(FRONT + "## Situation\n\n```\n## Strategy\nfour words in here\n```\nafter the fence\n")
        self.assertEqual(counts, {"Situation": 8})

    def test_a_report_with_a_strategy_section_is_a_fleet_report(self):
        lines, short = self.run_check("## Situation\n\nOne two three four five.\n\n## Strategy\n\nOne two three.\n\n## Cross-links\n")
        self.assertTrue(lines[0].endswith("(fleet report)"))
        self.assertEqual(short, 1)
        self.assertEqual(flat(lines[2]), "Strategy 3 words, minimum 4: SHORT by 1")
        self.assertFalse(any("Problems" in line for line in lines))

    def test_the_command_prints_pass_or_halt(self):
        code, text = self.run_main(self.report(GOOD))
        self.assertEqual((code, text.rstrip().split("\n")[-1]), (0, "REPORT WORDS: PASS"))
        code, text = self.run_main(self.report("## Situation\n\nToo short.\n\n## Problems\n\nNone were found.\n\n## Cross-links\n"))
        self.assertEqual(code, 1)
        self.assertTrue(text.rstrip().split("\n")[-1].startswith("REPORT WORDS: HALT -- 1 section(s) missing or under their minimum"))


class TemplateTests(Tree):
    def test_the_fixture_template_agrees_with_itself(self):
        self.assertEqual(words.template_check(str(self.root)), [])
        self.assertEqual(self.run_main("--template-check"), (0, "Errors: 0 | Warnings: 0\n"))

    def test_a_checklist_line_that_disagrees_with_the_table_is_an_error(self):
        self.template(TEMPLATE.replace("Situation 5, Problems 3", "Situation 5, Problems 2"))
        found = words.template_check(str(self.root))
        self.assertEqual(len(found), 1)
        self.assertIn("the checklist line of the division report says {'Situation': 5, 'Problems': 2}, the table says {'Situation': 5, 'Problems': 3}", found[0])

    def test_a_missing_checklist_line_a_bad_cell_and_a_missing_table_are_errors(self):
        self.template(TEMPLATE.replace("- [ ] Fleet report, minimum words: Situation 5, Strategy 4  (PASS / HALT)\n", ""))
        self.assertIn("no checklist line `- [ ] Fleet report, minimum words: ...`", words.template_check(str(self.root))[0])
        self.template(TEMPLATE.replace("| Problems | 3 | -- |", "| Problems | few | -- |"))
        self.assertIn("Minimum Length of Problems (division report) is `few`", words.minimums(str(self.root))[1][0])
        self.template(TEMPLATE.replace("### Minimum Length", "### Lengths"))
        self.assertEqual(words.minimums(str(self.root))[1], ["governance/template-reports.md: no `### Minimum Length` heading"])
        code, text = self.run_main(self.report(GOOD))
        self.assertEqual((code, text.rstrip().split("\n")[-1]), (1, "REPORT WORDS: HALT -- the template's minimums are not readable"))

    def test_the_real_template_is_readable_and_agrees_with_itself(self):
        self.assertEqual(words.template_check(str(ROOT)), [])
        wanted, errors = words.minimums(str(ROOT))
        self.assertEqual(errors, [])
        self.assertEqual(sorted(wanted["division"]), ["Activities", "Cross-links", "Feedback", "Learnings", "Plans", "Problems", "Situation", "Suggestions"])
        self.assertEqual(sorted(wanted["fleet"]), ["Advice and Suggestions", "Cross-links", "Divisions", "Learnings", "Plans", "Situation", "Strategy"])
        self.assertTrue(all(number > 0 for kind in wanted.values() for name, number in kind.items() if name != "Cross-links"))


if __name__ == "__main__":
    unittest.main()
