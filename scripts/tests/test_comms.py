"""comms.py on disposable trees: the newest orders, the state of each request, the digest, each rule of the gate."""

import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "comms.py"
spec = importlib.util.spec_from_file_location("comms_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
comms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comms)

COMMENT = "<!-- a log of the test tree.\n    See communications/protocol.md for the full spec.\n-->\n\n"
ORDERS = COMMENT + """## [ENT-001] | 2026-01-01 08:00 UTC | Unity | order | ref: routes/plan.json
Changed: first entry.
In force from 2026-01-01 08:00 UTC until a newer entry.
FLEET
F1. Old order.

## [ENT-002] | 2026-01-01 12:00 UTC | Unity | order | ref: routes/plan.json | see: ENT-001
Changed: F1 reworded.
In force from 2026-01-01 12:00 UTC until a newer entry.
FLEET
F1. New order.
ZERO, Mining (the miner- ships)
Order: mine.
APOLLO, Logistics (the hauler- ships)
Order: haul.
"""
SESSION = """## [ENT-%03d] | 2026-01-01 %s UTC | %s | session | ref: reports/2026-01-01_x_y.md | see: orders.log ENT-002
Session: %s.
Did: mined 400 ore.
Worked: the new field, 120 ore per hour.
Failed: none.
Requests: none.
Suggestions: none.
Report: y.
"""
REPORTS = COMMENT + "\n".join([SESSION % (1, "09:00", "Zero", "first"), SESSION % (2, "09:05", "Unity", "fleet"),
                               SESSION % (3, "13:00", "Zero", "second"), SESSION % (4, "17:00", "Zero", "third")])
REQUESTS = COMMENT + """## [ENT-001] | 2026-01-01 09:00 UTC | Zero | request | ref: routes/mine-a.json
To: Apophis.
Need: one guard at the field of the route.
By: next turn.
Why: an armed pilot was seen there twice.

## [ENT-002] | 2026-01-01 09:10 UTC | Apophis | answer | see: ENT-001
Answer: yes. One drone from the next turn on.

## [ENT-003] | 2026-01-01 09:20 UTC | Mercury | request
To: Unity.
Need: leave to sell stored ore under 2 cr.
By: 2026-01-02 08:00 UTC.

## [ENT-004] | 2026-01-01 10:00 UTC | Apophis | request
To: all.
Need: keep clear of the nebula of routes/hunt-b.json this turn.
Why: a pirate.

## [ENT-005] | 2026-01-01 13:00 UTC | Unity | answer | see: ENT-003
Answer: no. The ore feeds the workshop.

## [ENT-006] | 2026-01-01 14:00 UTC | Apophis | answer | see: ENT-001
Answer: done. The guard flew four hours; no contact.

## [ENT-007] | 2026-01-01 15:00 UTC | Oracle | request
To: Zero, Apollo.
Need: nothing mined at the place of scouting/x.json until it is read.
"""


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="comms-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "communications" / "archive").mkdir(parents=True)
        self.write("orders", ORDERS)
        self.write("reports", REPORTS)
        self.write("requests", REQUESTS)

    def write(self, name, text):
        (self.root / "communications" / (name + ".log")).write_text(text, encoding="ascii")

    def run_command(self, function, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = function(str(self.root), *args)
        return code, out.getvalue()


class ReadTests(Tree):
    def test_orders_prints_the_newest_entry_whole_and_nothing_older(self):
        code, text = self.run_command(comms.show_orders)
        self.assertEqual(code, 0)
        self.assertTrue(text.startswith("## [ENT-002] | 2026-01-01 12:00 UTC | Unity | order"))
        self.assertIn("F1. New order.", text)
        self.assertIn("Order: haul.", text)
        self.assertNotIn("Old order", text)

    def test_a_log_without_an_entry_has_no_orders_in_force(self):
        self.write("orders", COMMENT)
        code, text = self.run_command(comms.show_orders)
        self.assertEqual((code, text.strip()), (1, "orders.log holds no entry: no orders in force"))

    def test_the_last_answer_sets_the_state_of_a_request(self):
        entries, _errors = comms.read_log(str(self.root), "requests")
        states = {request["num"]: state for state, request, _answer in comms.request_states(entries)}
        self.assertEqual(states, {1: "CLOSED", 3: "CLOSED", 4: "OPEN", 7: "OPEN"})          # yes, then done; no; none; none
        self.write("requests", REQUESTS.split("## [ENT-006]")[0])
        entries, _errors = comms.read_log(str(self.root), "requests")
        self.assertEqual(comms.request_states(entries)[0][0], "ACCEPTED")                   # yes alone

    def test_requests_are_filtered_by_whom_they_name_and_who_wrote_them(self):
        _code, text = self.run_command(comms.show_requests, "Zero", None, False)
        self.assertIn("ENT-004", text)                                                      # to all
        self.assertIn("ENT-007 | 2026-01-01 15:00 | Oracle -> Zero, Apollo | by not said", text)
        self.assertNotIn("ENT-003", text)
        self.assertTrue(text.rstrip().endswith("Open: 2 | Accepted: 0 | Closed: 0"))
        _code, text = self.run_command(comms.show_requests, "Unity", None, True)
        self.assertIn("ENT-003", text)
        self.assertIn("answered ENT-005 by Unity, 2026-01-01 13:00: no. The ore feeds the workshop.", text)
        _code, text = self.run_command(comms.show_requests, None, "apophis", False)
        self.assertTrue(text.rstrip().endswith("Open: 1 | Accepted: 0 | Closed: 0"))

    def test_an_archived_request_keeps_its_state(self):
        head, tail = REQUESTS.split("## [ENT-005]")
        (self.root / "communications" / "archive" / "requests-2026-01-01.log").write_text(head, encoding="ascii")
        self.write("requests", COMMENT + "## [ENT-005]" + tail)
        entries, _errors = comms.read_log(str(self.root), "requests", archive=True)
        self.assertEqual([state for state, _r, _a in comms.request_states(entries)], ["CLOSED", "CLOSED", "OPEN", "OPEN"])
        self.assertEqual(comms.check(str(self.root)), [])                                   # the answers still find their requests

    def test_the_digest_gives_each_member_its_last_entries_and_names_who_did_not_report(self):
        _code, text = self.run_command(comms.show_digest, 2, None)
        blocks = text.split("== ")
        self.assertEqual([b.split(":")[0] for b in blocks[1:]], ["Unity", "Apollo", "Zero"])
        self.assertIn("Apollo: no session entry", text)
        zero = blocks[3]
        self.assertTrue(zero.startswith("Zero: 3 session entries, newest ENT-004 of 2026-01-01 17:00"))
        self.assertIn("Session: second.", zero)
        self.assertIn("Session: third.", zero)
        self.assertNotIn("Session: first.", zero)
        self.assertIn("request open:", zero)                                                # ENT-004 to all, ENT-007 to Zero
        self.assertIn("ENT-007", zero)
        self.assertNotIn("ENT-001", text)                                                   # closed requests are not in the digest
        _code, text = self.run_command(comms.show_digest, 1, "unity")
        self.assertEqual(text.count("== "), 1)


class GateTests(Tree):
    def errors_with(self, name, old, new):
        source = {"orders": ORDERS, "reports": REPORTS, "requests": REQUESTS}[name]
        self.assertEqual(source.count(old), 1, old)
        self.write(name, source.replace(old, new))
        found = comms.check(str(self.root))
        self.write(name, source)
        return found

    def test_the_clean_tree_passes(self):
        self.assertEqual(comms.check(str(self.root)), [])

    def test_each_rule_fails_alone(self):
        self.assertIn("header not in the protocol's form", self.errors_with("orders", "| 2026-01-01 12:00 UTC | Unity", "| 12:00 | Unity")[0])
        self.assertIn("orders.log ENT-002: the orders are written by Unity only",
                      self.errors_with("orders", "12:00 UTC | Unity | order", "12:00 UTC | Zero | order")[0])
        self.assertIn("category `order`", self.errors_with("orders", "12:00 UTC | Unity | order", "12:00 UTC | Unity | general")[0])
        self.assertEqual(self.errors_with("orders", "Changed: F1 reworded.\n", ""), ["orders.log ENT-002: no `Changed:` line"])
        self.assertEqual(self.errors_with("orders", "In force from 2026-01-01 12:00 UTC until a newer entry.\n", ""), ["orders.log ENT-002: no `In force` line"])
        self.assertEqual(self.errors_with("orders", "## [ENT-002]", "## [ENT-003]"), ["orders.log ENT-003: follows ENT-001: the numbers rise by one"])
        self.assertEqual(self.errors_with("reports", "Session: second.\n", ""), ["reports.log ENT-003: no `Session:` line"])
        self.assertEqual(self.errors_with("reports", "09:05 UTC | Unity | session", "09:05 UTC | Unity | general"),
                         ["reports.log ENT-002: category must be `session` (found `general`)"])
        self.assertEqual(self.errors_with("requests", "To: Unity.\n", ""), ["requests.log ENT-003: a request needs a `To:` line"])
        self.assertEqual(self.errors_with("requests", "Need: leave to sell stored ore under 2 cr.\n", ""), ["requests.log ENT-003: a request needs a `Need:` line"])
        self.assertIn("an answer names a request of this log", self.errors_with("requests", "answer | see: ENT-003", "answer | see: ENT-002")[0])
        self.assertEqual(self.errors_with("requests", "Answer: no. The ore", "Answer: maybe. The ore"),
                         ["requests.log ENT-005: the `Answer:` line starts with yes, no or done"])
        self.assertIn("category must be `request` or `answer`", self.errors_with("requests", "15:00 UTC | Oracle | request", "15:00 UTC | Oracle | general")[0])

    def test_a_missing_log_is_an_error(self):
        (self.root / "communications" / "requests.log").unlink()
        self.assertEqual(comms.check(str(self.root)), ["requests.log: missing"])


if __name__ == "__main__":
    unittest.main()
