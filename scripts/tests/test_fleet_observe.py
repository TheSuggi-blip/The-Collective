"""observe.py on a disposable data folder: a good add writes one line and returns the row; each rule failing alone writes nothing; a member writes only its own division's record (Unity: command); two processes adding at the same moment leave whole lines; show and kinds print what was added; the store takes the lines into its table."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "game" / "fleet" / "observe.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


observe = load("observe_under_test", SCRIPT)
NOBODY = {"HERMES_SESSION_PROFILE": "", "HERMES_HOME": "", "HERMES_SCRATCH_DIR": "", "TMPDIR": "", "FLEET_MEMBER": ""}


def shell(profile, **more):
    """The environment of a member's shell (or of nobody's: profile ''), every other way of naming one cleared."""
    return dict(NOBODY, HERMES_SESSION_PROFILE=profile, **more)


class ObserveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-observe-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.as_member("oracle")

    def as_member(self, profile, **more):
        patcher = mock.patch.dict(os.environ, shell(profile, **more))
        patcher.start()
        self.addCleanup(patcher.stop)

    def record(self, name):
        return self.data / "observations" / ("%s.jsonl" % name)

    def lines(self, name):
        path = self.record(name)
        return path.read_text(encoding="ascii").splitlines() if path.exists() else []

    def cli(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as said:
            code = observe.main(list(argv) + ["--data", str(self.data)])
        return code, said.getvalue()

    def recent(self, hours=1):
        return observe.stamp(time.time() - hours * 3600)

    def test_a_good_add_writes_one_line_and_returns_the_row(self):
        at = self.recent()
        row = observe.add("scan", "sys_far", {"belts": 2, "ice": True, "owner": "ROGU", "jumps": 7.5}, note="two belts, no station",
                          at=at, data=str(self.data))
        self.assertEqual(row, {"t": at, "member": "Oracle", "division": "intel", "kind": "scan", "subject": "sys_far",
                               "fields": {"belts": 2, "ice": True, "owner": "ROGU", "jumps": 7.5}, "note": "two belts, no station"})
        self.assertEqual([json.loads(line) for line in self.lines("intel")], [row])
        self.assertEqual(list(json.loads(self.lines("intel")[0])), ["t", "member", "division", "kind", "subject", "fields", "note"])
        self.assertEqual(sorted(p.name for p in (self.data / "observations").iterdir()), ["intel.jsonl"])
        self.assertTrue(self.record("intel").read_bytes().endswith(b"}\n"))
        now = observe.add("travel", "sys_a>sys_b", {}, data=str(self.data))                     # no --at: now
        self.assertLess(abs(observe.when(now["t"], time.time())[0] - time.time()), 5)
        self.assertEqual(len(self.lines("intel")), 2)

    def test_the_command_line_reads_numbers_truth_and_text(self):
        code, said = self.cli("add", "price", "far_base", "item=iron_ore", "bid=14", "ask=-3.5", "big=1e3", "listed=true", "id=007",
                              "label=a b", "--note", "seen docked", "--at", self.recent(2)[:16].replace("T", " "))
        self.assertEqual(code, 0, said)
        self.assertIn("observe: added to", said)
        row = json.loads(self.lines("intel")[0])
        self.assertEqual(row["fields"], {"item": "iron_ore", "bid": 14, "ask": -3.5, "big": 1000.0, "listed": True, "id": "007", "label": "a b"})
        self.assertEqual((type(row["fields"]["bid"]), type(row["fields"]["big"])), (int, float))
        self.assertEqual((row["note"], row["t"][-4:]), ("seen docked", ":00Z"))

    def test_each_rule_failing_alone_writes_nothing(self):
        good = {"kind": "scan", "subject": "sys_far", "fields": {"belts": 2}, "note": "", "at": None}
        long_fields = {"k%02d" % n: "x" * 160 for n in range(24)}                               # every field within its rules, the line too long
        broken = [
            ("kind with a capital", {"kind": "Scan"}, "kind `Scan`"),
            ("kind of one letter", {"kind": "s"}, "kind `s`"),
            ("kind of 33 characters", {"kind": "s" * 33}, "kind `"),
            ("kind with a dash", {"kind": "scan-far"}, "kind `scan-far`"),
            ("no subject", {"subject": ""}, "no subject"),
            ("a blank subject", {"subject": "   "}, "no subject"),
            ("a subject of 121", {"subject": "s" * 121}, "121 characters long; at most 120"),
            ("a subject with a tab", {"subject": "sys\tfar"}, "subject holds a character"),
            ("a subject not ASCII", {"subject": "sys" + chr(0xe9)}, "subject holds a character"),
            ("25 fields", {"fields": {"k%d" % n: n for n in range(25)}}, "25 fields; at most 24"),
            ("a key with a capital", {"fields": {"Belts": 2}}, "key `Belts`"),
            ("a key that starts with a digit", {"fields": {"2belts": 2}}, "key `2belts`"),
            ("a key of 33", {"fields": {"k" * 33: 2}}, "key `"),
            ("a text value of 201", {"fields": {"owner": "x" * 201}}, "201 characters long; a text value is at most 200"),
            ("an empty value", {"fields": {"owner": ""}}, "field `owner` has no value"),
            ("a value with a line break", {"fields": {"owner": "a\nb"}}, "field `owner` holds a character"),
            ("a value that is a list", {"fields": {"owner": [1, 2]}}, "field `owner` is a list"),
            ("a value that is None", {"fields": {"owner": None}}, "field `owner` is a NoneType"),
            ("a value that is NaN", {"fields": {"owner": float("nan")}}, "is no number JSON can carry"),
            ("a note of 401", {"note": "n" * 401}, "401 characters long; at most 400"),
            ("a note not ASCII", {"note": "caf" + chr(0xe9)}, "note holds a character"),
            ("a time ahead", {"at": observe.stamp(time.time() + 3600)}, "lies ahead of this clock"),
            ("a time too old", {"at": observe.stamp(time.time() - 31 * 86400)}, "older than 30 days"),
            ("a time unreadable", {"at": "yesterday"}, "is no UTC time"),
            ("a line of more than 4000 bytes", {"fields": long_fields}, "at most 4000"),
        ]
        self.assertLess(len(json.dumps({"t": "2026-11-16T22:10:05Z", "fields": dict(list(long_fields.items())[:20])})), 4000)   # the line, not a field
        for what, change, words in broken:
            case = dict(good, **change)
            with self.assertRaises(ValueError, msg=what) as caught:
                observe.add(case["kind"], case["subject"], case["fields"], note=case["note"], at=case["at"], data=str(self.data))
            self.assertIn(words, str(caught.exception), what)
            self.assertTrue(str(caught.exception).startswith("refused: "), what)
            self.assertNotIn("\n", str(caught.exception), what)
            self.assertFalse(self.record("intel").exists(), what)
        observe.add(**dict(good, data=str(self.data)))                                           # the good one itself passes
        self.assertEqual(len(self.lines("intel")), 1)

    def test_the_command_line_refuses_with_one_plain_line(self):
        for argv, words in ((["add", "scan", "sys_far", "belts=2", "belts=3"], "field `belts` is given twice"),
                            (["add", "scan", "sys_far", "belts"], "`belts` is no key=value"),
                            (["add", "scan"], "add takes <kind> <subject>"),
                            (["add", "scan", "sys_far", "--note"], "--note takes a value"),
                            (["add", "scan", "sys_far", "--force"], "no option --force"),
                            (["add", "Scan", "sys_far"], "kind `Scan`"),
                            (["show", "--last", "many"], "--last takes a number"),
                            (["show", "--division", "navy"], "names no division")):
            code, said = self.cli(*argv)
            self.assertEqual(code, 1, argv)
            self.assertEqual(said.count("\n"), 1, said)
            self.assertIn(words, said, argv)
        self.assertFalse(self.record("intel").exists())

    def test_a_member_writes_only_its_own_division_and_unity_command(self):
        code, said = self.cli("add", "price", "far_base", "bid=3", "--division", "trade")
        self.assertEqual(code, 1)
        self.assertIn("Oracle writes the intel record only", said)
        self.assertFalse(self.record("trade").exists())
        self.assertEqual(self.cli("add", "price", "far_base", "bid=3", "--division", "intel")[0], 0)  # its own: fine
        with self.assertRaises(ValueError) as caught:
            observe.add("price", "far_base", {"bid": 3}, data=str(self.data), member="Zero")         # a script cannot write in another's name
        self.assertIn("this shell is Oracle: it writes as Oracle only, not as Zero", str(caught.exception))
        self.assertEqual(observe.add("scan", "x", {}, data=str(self.data), member="oracle")["member"], "Oracle")
        self.as_member("unity")
        self.assertEqual(observe.add("note", "fleet", {"ships": 246}, data=str(self.data))["division"], "command")
        code, said = self.cli("add", "note", "fleet", "--division", "intel")
        self.assertEqual(code, 1)
        self.assertIn("Unity writes the command record only", said)
        self.as_member("zero")
        self.assertEqual(observe.add("yield", "belt_a", {"ore": 40}, data=str(self.data))["division"], "mining")
        self.assertEqual(sorted(p.name for p in (self.data / "observations").iterdir()), ["command.jsonl", "intel.jsonl", "mining.jsonl"])
        self.assertEqual([len(self.lines(name)) for name in ("intel", "command", "mining")], [2, 1, 1])
        for profile, more, words in (("", {}, "no member of The Collective"), ("", {"FLEET_MEMBER": "dispatch"}, "the service dispatch writes no observation")):
            self.as_member(profile, **more)
            with self.assertRaises(ValueError) as caught:
                observe.add("scan", "x", {}, data=str(self.data))
            self.assertIn(words, str(caught.exception))
        self.assertEqual([len(self.lines(name)) for name in ("intel", "command", "mining")], [2, 1, 1])

    def test_a_line_left_without_its_newline_does_not_swallow_the_next(self):
        self.record("intel").parent.mkdir()
        self.record("intel").write_bytes(b'{"t": "2026-11-16T1')
        observe.add("scan", "sys_far", {"belts": 2}, data=str(self.data))
        lines = self.lines("intel")
        self.assertEqual((len(lines), json.loads(lines[1])["subject"]), (2, "sys_far"))
        self.assertEqual((len(observe.rows(str(self.data), "intel")), observe.read_record(self.record("intel"))[1]), (1, 1))

    def test_two_processes_adding_at_the_same_moment_leave_whole_lines(self):
        start = time.time() + 1.0                                                                  # both wait for one moment, then write
        code = ("import sys, time; sys.path.insert(0, %r); import observe; time.sleep(max(0, %r - time.time())); "
                "[observe.add('load', 'writer-%%s' %% sys.argv[1], {'n': n, 'pad': 'x' * 200}, note='y' * 400, data=%r) for n in range(50)]"
                % (str(SCRIPT.parent), start, str(self.data)))
        runs = [subprocess.Popen([sys.executable, "-I", "-B", "-c", code, name], env=shell(profile), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True) for name, profile in (("a", "oracle"), ("b", "oracle"))]
        for proc in runs:
            _out, err = proc.communicate(timeout=120)
            self.assertEqual(proc.returncode, 0, err)
        raw = self.record("intel").read_bytes()
        self.assertTrue(raw.endswith(b"\n"))
        rows = [json.loads(line) for line in raw.decode("ascii").splitlines()]
        self.assertEqual(len(rows), 100)
        self.assertEqual(sorted((r["subject"], r["fields"]["n"]) for r in rows), sorted((s, n) for s in ("writer-a", "writer-b") for n in range(50)))

    def test_show_and_kinds_print_what_was_added(self):
        observe.add("scan", "sys_far", {"belts": 2, "ice": True}, note="two belts", at=self.recent(3), data=str(self.data))
        observe.add("scan", "sys_near", {"belts": 1, "stations": 1}, at=self.recent(2), data=str(self.data))
        observe.add("travel", "sys_a>sys_b", {"minutes": 4.5, "label": "a b"}, at=self.recent(1), data=str(self.data))
        self.as_member("mercury")
        observe.add("price", "far_base", {"item": "iron_ore", "bid": 14}, data=str(self.data))
        code, said = self.cli("show")                                                            # its own division by default
        self.assertEqual(code, 0)
        self.assertIn("OBSERVE show | trade | 1 of 1 rows", said)
        self.assertRegex(said, r"trade\s+Mercury\s+price\s+far_base  item=iron_ore bid=14")
        code, said = self.cli("show", "scan", "--division", "Oracle")
        lines = said.splitlines()
        self.assertIn("OBSERVE show | intel | kind scan | 2 of 2 rows", lines[0])
        self.assertRegex(lines[1], r"intel\s+Oracle\s+scan\s+sys_far  belts=2 ice=true  -- two belts$")   # oldest first
        self.assertRegex(lines[2], r"sys_near  belts=1 stations=1$")
        code, said = self.cli("show", "--division", "all", "--last", "2", "--subject", "SYS_")
        self.assertIn("| 2 of 3 rows", said)
        self.assertIn('label="a b"', said)
        self.assertNotIn("sys_far", said)
        code, said = self.cli("kinds", "--division", "all")
        self.assertEqual(code, 0)
        self.assertIn("OBSERVE kinds | all | 3 kinds, 4 rows", said)
        self.assertRegex(said, r"intel\s+scan\s+2\s+\S+Z\s+belts, ice, stations")
        self.assertRegex(said, r"trade\s+price\s+1\s+\S+Z\s+bid, item")
        self.assertIn("no observation on record", self.cli("kinds", "--division", "military")[1])

    def test_the_store_takes_the_lines_and_keeps_them_as_long_as_observe_allows(self):
        store = load("store_beside_observe", ROOT / "game" / "fleet" / "store.py")
        self.assertEqual(store.KEEP_TABLES["observations"], observe.OLDEST_DAYS)                 # one figure: the oldest --at the store still takes
        self.assertEqual(set(store.OBSERVED), set(observe.DIVISIONS.values()))
        observe.add("scan", "sys_far", {"belts": 2, "ice": True}, data=str(self.data))
        self.as_member("apollo")
        observe.add("price", "far_base", {"item": "steel_plate", "ask": 70}, data=str(self.data))
        store.one_pass(str(self.data), root=str(self.data / "no-repository"))
        found = store.query(str(self.data), "SELECT division, member, kind, json_extract(fields, '$.belts'), json_extract(fields, '$.ask') "
                                            "FROM observations ORDER BY division")
        self.assertEqual((found["error"], found["rows"]), (None, [("intel", "Oracle", "scan", 2, None), ("logistics", "Apollo", "price", None, 70)]))

    def test_from_the_command_line_as_a_member_shell_runs_it(self):
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "add", "scan", "sys_far", "belts=2", "--data", str(self.data)],
                              env=shell("oracle"), capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(len(self.lines("intel")), 1)
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "add", "scan", "sys_far", "--data", str(self.data)],
                              env=shell(""), capture_output=True, text=True, timeout=60)
        self.assertEqual((done.returncode, done.stderr), (1, ""))
        self.assertIn("observe: refused: this shell is no member", done.stdout)


if __name__ == "__main__":
    unittest.main()
