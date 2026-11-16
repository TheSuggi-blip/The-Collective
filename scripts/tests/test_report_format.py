"""The report format gate, run on disposable reports in a temporary folder."""

from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts" / "check-report-format.sh"
FRONT = """---
name: a-disposable-report
id: 20261116T000000Z
tier: report
trigger: session-end
author: Zero
tags: [test]
links: []
---
# A Disposable Report

"""
SECTIONS = ("Situation", "Activities", "Problems", "Plans", "Suggestions", "Feedback", "Learnings", "Cross-links")


class ReportFormatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="report-format-test-")
        self.addCleanup(self.temp.cleanup)
        self.report = Path(self.temp.name) / "2026-11-16_zero_a-disposable-report.md"

    def check(self, activities):
        body = "".join("## %s\n\n%s\n\n" % (name, activities if name == "Activities" else "Nothing to say.") for name in SECTIONS)
        self.report.write_text(FRONT + body, encoding="ascii")
        done = subprocess.run(["bash", str(GATE), str(self.report)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return done.returncode, done.stdout

    def test_a_report_in_the_template_passes(self):
        code, out = self.check("Twelve ships of Mining flew the ice route; one miner waited for a harvester.")
        self.assertEqual(code, 0, out)
        self.assertIn("REPORT FORMAT: PASS", out)

    def test_a_report_that_names_a_pilot_of_ours_halts(self):
        for name in ("miner-12", "trader-3", "hauler-20", "drone-1", "scout-7", "sentinel-10"):
            code, out = self.check("The ice route was flown by %s at noon." % name)
            self.assertEqual(code, 1, name)
            self.assertIn("PILOT NAMED", out)
            self.assertIn("%d:%s" % (self.line_of(name), name), out)
            self.assertIn("REPORT FORMAT: HALT", out)

    def line_of(self, name):
        for number, line in enumerate(self.report.read_text(encoding="ascii").splitlines(), 1):
            if name in line:
                return number
        return 0

    def test_role_words_alone_and_other_numbers_pass(self):
        code, out = self.check("A miner and two drones; route mine-ice-3 paid 4-5 loads; scout ships flew 12 runs; sub-miner-4x is no pilot.")
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
