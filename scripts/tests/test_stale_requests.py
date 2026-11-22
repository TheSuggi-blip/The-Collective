"""comms.py marks a request not closed and untouched for more than three days STALE, counts it, and closes nothing;
hive.py briefing names how many stale requests are addressed to the reader."""

import calendar
import contextlib
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


comms = load("comms_for_stale", ROOT / "scripts" / "comms.py")
NOW = calendar.timegm(time.strptime("2026-01-05 10:00", "%Y-%m-%d %H:%M"))
REQUESTS = """<!-- a log of the test tree. -->

## [ENT-001] | 2026-01-01 09:00 UTC | Zero | request
To: Apophis.
Need: one guard at the field of the route.

## [ENT-002] | 2026-01-01 09:30 UTC | Mercury | request
To: Unity.
Need: leave to sell stored ore under 2 cr.

## [ENT-003] | 2026-01-04 09:00 UTC | Unity | answer | see: ENT-002
Answer: yes. From the next turn on.

## [ENT-004] | 2026-01-01 10:00 UTC | Apophis | request
To: all.
Need: keep clear of the nebula this turn.

## [ENT-005] | 2026-01-01 11:00 UTC | Apophis | answer | see: ENT-004
Answer: done. The pirate left.

## [ENT-006] | 2026-01-03 15:00 UTC | Oracle | request
To: Zero, Apollo.
Need: nothing mined at the place of scouting/x.json until it is read.
"""


class StaleRequests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="stale-requests-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        (self.root / "communications" / "archive").mkdir(parents=True)
        self.log = self.root / "communications" / "requests.log"
        self.log.write_text(REQUESTS, encoding="ascii")

    def test_a_request_untouched_for_more_than_three_days_is_marked_counted_and_left_open(self):
        digest = hashlib.sha256(self.log.read_bytes()).hexdigest()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            comms.show_requests(str(self.root), None, None, False, NOW)
        text = out.getvalue()
        self.assertIn("  STALE (4 d) ENT-001 | 2026-01-01 09:00 | Zero -> Apophis", text)       # open, four days without an answer
        self.assertIn("\n  ENT-002 | 2026-01-01 09:30 | Mercury -> Unity", text)               # accepted a day ago: fresh
        self.assertIn("\n  ENT-006 | 2026-01-03 15:00 | Oracle -> Zero, Apollo", text)          # open two days: fresh
        self.assertIn("Stale: 1 not closed and untouched for more than 3 days (ENT-001)", text)
        self.assertTrue(text.rstrip().endswith("Open: 2 | Accepted: 1 | Closed: 1"))
        entries, _errors = comms.read_log(str(self.root), "requests")
        self.assertEqual({r["num"]: s for s, r, _a in comms.request_states(entries)}, {1: "OPEN", 2: "ACCEPTED", 4: "CLOSED", 6: "OPEN"})
        self.assertEqual(hashlib.sha256(self.log.read_bytes()).hexdigest(), digest)                # no machine closes one
        later = io.StringIO()
        with contextlib.redirect_stdout(later):
            comms.show_requests(str(self.root), None, None, False, NOW + 3 * 86400)
        self.assertIn("Stale: 3 not closed and untouched for more than 3 days (ENT-001, ENT-002, ENT-006)", later.getvalue())

    def test_the_line_of_the_briefing_counts_what_is_addressed_to_the_reader(self):
        self.assertEqual(comms.stale_line(str(self.root), "Apophis", NOW),
                         "STALE REQUESTS ADDRESSED TO Apophis: 1 not closed and untouched for more than 3 days: ENT-001 | "
                         "answer each (yes, no or done); no machine closes one")
        self.assertEqual(comms.stale_line(str(self.root), "Zero", NOW), "STALE REQUESTS ADDRESSED TO Zero: 0 not closed and untouched for more than 3 days")
        self.assertTrue(comms.stale_line(str(self.root), "all", NOW).startswith("STALE REQUESTS: 1 not closed"))

    def test_the_briefing_names_the_count(self):
        data = Path(self.temp.name) / "data"
        for folder in ("market", "scouting", "wildlife", "fleet/ships", "routes", "catalog", "stock", "intel"):
            (data / folder).mkdir(parents=True)
        hive = load("hive_for_stale", FLEET / "hive.py")
        now = time.time()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            hive.show_briefing(str(FLEET.parent), str(data), now, "Zero", 4)
        expected = comms.stale_line(str(ROOT), "Zero", now)                                         # the repository's own log, as the briefing read it
        self.assertIn("\n" + expected + "\n", out.getvalue())


if __name__ == "__main__":
    unittest.main()
