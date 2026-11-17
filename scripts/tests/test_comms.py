"""comms.py on disposable trees: the newest orders, the state of each request, the digest, each rule of the gate."""

import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "comms.py"
spec = importlib.util.spec_from_file_location("comms_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
comms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comms)

COMMENT = "<!-- a log of the test tree.\n    See communications/protocol.md for the full spec.\n-->\n\n"
ORDERS = COMMENT + """## [ENT-001] | 2026-01-01 08:00 UTC | Unity | order | ref: game/routes/plan.json
Changed: first entry.
In force from 2026-01-01 08:00 UTC until a newer entry.
FLEET
F1. Old order.

## [ENT-002] | 2026-01-01 12:00 UTC | Unity | order | ref: game/routes/plan.json | see: ENT-001
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
REQUESTS = COMMENT + """## [ENT-001] | 2026-01-01 09:00 UTC | Zero | request | ref: game/routes/mine-a.json
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
Need: keep clear of the nebula of game/routes/hunt-b.json this turn.
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
        self.root = Path(self.temp.name) / "repo"                                           # drafts lie beside it, never in it
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


class AppendTests(Tree):
    def draft(self, text):
        path = Path(self.temp.name) / "draft.txt"
        path.write_text(text, encoding="ascii")
        return str(path)

    def log(self, name):
        return (self.root / "communications" / (name + ".log")).read_text(encoding="ascii")

    def test_the_script_sets_number_and_time_and_one_blank_line(self):
        self.write("requests", COMMENT)
        draft = self.draft("## [ENT-NEXT] | NOW | Zero | request | ref: game/routes/mine-a.json\nTo: Apophis.\nNeed: one guard.\n\n\n")
        code, text = self.run_command(comms.append, "requests", draft, "Zero")
        self.assertEqual((code, text.strip()), (0, "appended ENT-001 to communications/requests.log (not committed)"))
        code, _text = self.run_command(comms.append, "requests", self.draft("## [ENT-NEXT] | NOW | Apophis | answer | see: ENT-001\nAnswer: yes. From the next turn.\n"), "Apophis")
        self.assertEqual(code, 0)
        body = self.log("requests")[len(COMMENT):]
        self.assertRegex(body, r"\A## \[ENT-001\] \| \d{4}-\d\d-\d\d \d\d:\d\d UTC \| Zero \| request \| ref: game/routes/mine-a.json\nTo: Apophis.\nNeed: one guard.\n\n"
                               r"## \[ENT-002\] \| \d{4}-\d\d-\d\d \d\d:\d\d UTC \| Apophis \| answer \| see: ENT-001\nAnswer: yes. From the next turn.\n\Z")
        self.assertEqual(comms.check(str(self.root)), [])

    def test_a_refused_entry_leaves_the_log_byte_for_byte(self):
        before = {name: self.log(name) for name in ("orders", "reports", "requests")}
        order = "## [ENT-NEXT] | NOW | %s | order\nChanged: x.\nIn force from now until a newer entry.\nFLEET\nF1. y.\n"
        cases = [("orders", order % "Zero", "Zero", "orders.log is written by the Fleet Admiral only"),
                 ("orders", order % "Unity", "Zero", "the entry names Unity as its writer, the append is made as Zero"),
                 ("reports", "## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nNeed: x.\n", "Zero", "category `request` does not belong in reports.log (it takes: session)"),
                 ("requests", "## [ENT-008] | 2026-01-01 16:00 UTC | Zero | request\nTo: Unity.\nNeed: x.\n", "Zero", "the first line must be `## [ENT-NEXT] | NOW |"),
                 ("requests", "## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nNeed: x.\n\n## [ENT-NEXT] | NOW | Zero | request\nTo: all.\nNeed: y.\n", "Zero", "one entry per call"),
                 ("requests", "## [ENT-NEXT] | NOW | Zero | request\n\n", "Zero", "the entry has no body"),
                 ("requests", "## [ENT-NEXT] | NOW | Zero | request\nNeed: x.\n", "Zero", "requests.log the entry: a request needs a `To:` line"),
                 ("requests", "## [ENT-NEXT] | NOW | Zero | answer | see: ENT-099\nAnswer: yes.\n", "Zero", "an answer names a request of this log"),
                 ("reports", "## [ENT-NEXT] | NOW | Zero | session\nSession: x.\nDid: y.\nReport: z.\n", "Zero", "reports.log the entry: no `Worked:` line")]
        for log, text, writer, message in cases:
            code, printed = self.run_command(comms.append, log, self.draft(text), writer)
            self.assertEqual(code, 1, message)
            self.assertIn("NOT APPENDED: ", printed)
            self.assertIn(message, printed)
            self.assertEqual({name: self.log(name) for name in before}, before, message)

    def test_an_entry_that_names_a_pilot_of_ours_is_refused(self):
        # requests ENT-052: the logs are public; a rule in a skill was broken three times, the command refuses
        before = self.log("requests")
        named = "## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nNeed: a look at data/routes/logs/scout-10.log and at miner-3.\n"
        code, printed = self.run_command(comms.append, "requests", self.draft(named), "Zero")
        self.assertEqual(code, 1)
        self.assertIn("NOT APPENDED: the entry names a pilot of ours (scout-10, miner-3)", printed)
        self.assertEqual(self.log("requests"), before)
        free = "## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nNeed: the log of one scout; the miner- ships, sentinel-<n>, 30 drones and Prime Directive wait.\n"
        code, _printed = self.run_command(comms.append, "requests", self.draft(free), "Zero")
        self.assertEqual(code, 0)                                                              # a role word, a placeholder and a flagship are no pilot's name

    def test_an_entry_file_inside_the_repository_is_refused(self):
        inside = self.root / "draft.txt"
        inside.write_text("## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nNeed: x.\n", encoding="ascii")
        before = self.log("requests")
        code, printed = self.run_command(comms.append, "requests", str(inside), "Zero")
        self.assertEqual(code, 1)
        self.assertIn("keep the entry file outside the repository", printed)
        self.assertEqual(self.log("requests"), before)

    def test_an_old_fault_in_a_log_does_not_block_a_good_entry(self):
        self.write("requests", REQUESTS.replace("To: Unity.\n", ""))                          # ENT-003 was written without its To: line
        code, _text = self.run_command(comms.append, "requests", self.draft("## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nNeed: x.\n"), "Zero")
        self.assertEqual(code, 0)
        self.assertIn("## [ENT-008] | ", self.log("requests"))

    def test_a_claim_over_a_route_another_member_claims_in_force_is_refused(self):
        # requests ENT-180 (Apollo): two divisions claimed two gas routes nine minutes apart (errors.log ENT-069)
        self.write("admirals", COMMENT)
        routes = self.root / "game" / "routes"
        routes.mkdir(parents=True)
        (routes / "mine-a.json").write_text('{"id": "mine-a", "kind": "mine", "sell": "x:y:z", "max_ships": 2}', encoding="ascii")
        (routes / "gather-x.json").write_text('{"id": "gather-x", "kind": "mine", "standing": true, "max_ships": 60}', encoding="ascii")
        first = "## [ENT-NEXT] | NOW | Zero | claim\nClaims: mine-a (2 ships) and up to 20 places on gather-x.\n"
        self.assertEqual(self.run_command(comms.append, "admirals", self.draft(first), "Zero")[0], 0)
        over = "## [ENT-NEXT] | NOW | Apollo | claim\nClaims: mine-a (1 ship), the silicon-ore ask at the capital.\n"
        code, text = self.run_command(comms.append, "admirals", self.draft(over), "Apollo")
        self.assertEqual(code, 1)
        self.assertIn("NOT APPENDED: mine-a is claimed by Zero in admirals.log ENT-001", text)
        self.assertNotIn("silicon-ore", text)                                                   # no route file: words, not compared
        shared = "## [ENT-NEXT] | NOW | Apollo | claim\nClaims: up to 10 places on gather-x.\n"
        self.assertEqual(self.run_command(comms.append, "admirals", self.draft(shared), "Apollo")[0], 0)   # standing work is shared
        again = "## [ENT-NEXT] | NOW | Zero | claim\nClaims: mine-a (2 ships).\n"
        self.assertEqual(self.run_command(comms.append, "admirals", self.draft(again), "Zero")[0], 0)      # its own claim renewed
        self.run_command(comms.append, "admirals", self.draft("## [ENT-NEXT] | NOW | Zero | note\nReleases: ENT-001, ENT-003.\n"), "Zero")
        self.assertEqual(self.run_command(comms.append, "admirals", self.draft(over), "Apollo")[0], 0)     # released: free to claim

    def test_the_admirals_log_takes_notes_and_claims_and_shows_the_claims_in_force(self):
        self.write("admirals", COMMENT)                                                         # Suggi, 2026-11-16: the Admirals coordinate among themselves
        claim = "## [ENT-NEXT] | NOW | Zero | claim | ref: game/routes/mine-a.json\nClaims: mine-a, for 12 ships.\nWhy: the ice bid at the capital.\n"
        code, text = self.run_command(comms.append, "admirals", self.draft(claim), "Zero")
        self.assertEqual((code, text.strip()), (0, "appended ENT-001 to communications/admirals.log (not committed)"))
        code, text = self.run_command(comms.append, "admirals", self.draft("## [ENT-NEXT] | NOW | Apophis | claim\nThe herd at the nebula.\n"), "Apophis")
        self.assertEqual((code, "a claim needs a `Claims:` line" in text), (1, True))
        code, text = self.run_command(comms.append, "admirals", self.draft("## [ENT-NEXT] | NOW | Apophis | general\nA notice.\n"), "Apophis")
        self.assertEqual((code, "does not belong in admirals.log" in text), (1, True))
        self.run_command(comms.append, "admirals", self.draft("## [ENT-NEXT] | NOW | Apophis | note\nTwo guards go to the field of mine-a at the next turn.\n"), "Apophis")
        code, text = self.run_command(comms.show_admirals, 12, None)
        self.assertEqual((code, "CLAIMS IN FORCE: 1" in text, "ENT-001" in text, "mine-a, for 12 ships." in text, "Two guards go" in text), (0, True, True, True, True))
        self.assertNotIn("Two guards go", self.run_command(comms.show_admirals, 12, "Zero")[1])
        self.run_command(comms.append, "admirals", self.draft("## [ENT-NEXT] | NOW | Apophis | note\nReleases: ENT-001.\n"), "Apophis")
        self.assertIn("CLAIMS IN FORCE: 1", self.run_command(comms.show_admirals, 12, None)[1])     # only its writer ends a claim
        self.run_command(comms.append, "admirals", self.draft("## [ENT-NEXT] | NOW | Zero | note\nReleases: ENT-001.\nThe bid is gone.\n"), "Zero")
        self.assertIn("CLAIMS IN FORCE: 0", self.run_command(comms.show_admirals, 12, None)[1])
        old = COMMENT + "## [ENT-001] | 2026-01-01 08:00 UTC | Zero | claim\nClaims: mine-a, for 12 ships.\n"
        self.write("admirals", old)
        self.assertIn("CLAIMS IN FORCE: 0", self.run_command(comms.show_admirals, 12, None)[1])     # a claim lapses by itself

    def test_the_counter_goes_on_after_an_archive_run_and_queue_takes_general(self):
        (self.root / "communications" / "archive" / "queue-2026-01-01.log").write_text(
            COMMENT + "## [ENT-041] | 2026-01-01 08:00 UTC | Unity | general\nOld.\n", encoding="ascii")
        self.write("queue", COMMENT)
        code, text = self.run_command(comms.append, "queue", self.draft("## [ENT-NEXT] | NOW | Zero | general | ref: game/routes/index.md\nA notice.\n"), "Zero")
        self.assertEqual((code, text.strip()), (0, "appended ENT-042 to communications/queue.log (not committed)"))

    @unittest.skipUnless(shutil.which("git"), "git is not installed")
    def test_the_entry_is_committed_by_path_under_the_writers_name(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root)] + list(args), capture_output=True, text=True, check=True).stdout.strip()
        git("init", "-q")
        git("-c", "user.name=Seed", "-c", "user.email=seed@example.invalid", "add", "communications")
        git("-c", "user.name=Seed", "-c", "user.email=seed@example.invalid", "commit", "-q", "-m", "seed")
        (self.root / "communications" / "errors.log").write_text(COMMENT + "another member's work in progress\n", encoding="ascii")
        git("add", "communications/errors.log")                                              # staged by someone else: not ours to commit
        draft = self.draft("## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nNeed: x.\n")
        code, text = self.run_command(comms.append, "requests", draft, "Zero")
        self.assertEqual(code, 0, text)
        self.assertRegex(text.strip(), r"^appended ENT-008 to communications/requests.log, committed [0-9a-f]{7,} as Zero$")
        self.assertEqual(git("log", "-1", "--format=%an <%ae> | %s"), "Zero <zero@suggi-workspace.dev> | requests.log: ENT-008 (request, Zero)")
        self.assertEqual(git("show", "--name-only", "--format=", "HEAD"), "communications/requests.log")
        self.assertEqual(git("status", "--short"), "A  communications/errors.log")            # still staged, still theirs


if __name__ == "__main__":
    unittest.main()
