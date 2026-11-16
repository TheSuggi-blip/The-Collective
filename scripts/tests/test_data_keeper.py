"""The keeper cuts disposable records in a temporary folder, never the unit's data."""

import gzip
import importlib.util
import os
from pathlib import Path
import stat
import tempfile
import threading
import time
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "data-keeper.py"


class DataKeeperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="data-keeper-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        spec = importlib.util.spec_from_file_location("keeper_under_test", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.keeper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.keeper)
        (self.data / "market").mkdir()
        self.name = "market/history.jsonl"
        self.path = self.data / self.name

    @staticmethod
    def line(number):
        return ('{"n": %06d, "pad": "%s"}\n' % (number, "x" * 80)).encode("ascii")

    def fill(self, first, count):
        with open(self.path, "ab") as handle:
            for number in range(first, first + count):
                handle.write(self.line(number))

    def trim(self, limit=50_000, stay=20_000, keep=5):
        return self.keeper.trim(self.data, self.name, limit, stay, keep=keep, settle=0.1)

    def archived(self):
        return b"".join(gzip.open(path, "rb").read() for path in self.keeper.archives(self.data, self.name))

    def test_a_record_below_its_limit_is_left_alone(self):
        self.fill(0, 100)
        before = self.path.read_bytes()
        self.assertIsNone(self.trim())
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.keeper.archives(self.data, self.name), [])
        self.assertIsNone(self.keeper.trim(self.data, "no/such.jsonl", 1, 1))

    def test_the_newest_lines_stay_and_the_older_ones_are_archived(self):
        self.fill(0, 1000)
        before = self.path.read_bytes()
        os.chmod(self.path, 0o640)
        said = self.trim()
        self.assertIn("market/history.jsonl:", said)
        live = self.path.read_bytes()
        self.assertLessEqual(len(live), 20_000)
        self.assertGreater(len(live), 20_000 - 200)
        self.assertEqual(self.archived() + live, before)
        self.assertTrue(live.startswith(b'{"n": '))
        self.assertTrue(live.endswith(self.line(999)))
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o640)
        self.assertEqual([p.name for p in self.data.joinpath("market").iterdir()], ["history.jsonl"])
        self.assertIsNone(self.trim(), "a second look finds nothing to cut")

    def test_the_newest_archives_are_kept_and_older_ones_deleted(self):
        number = 0
        names = []
        for _ in range(4):
            self.fill(number, 600)
            number += 600
            self.assertIsNotNone(self.trim(keep=2))
            names.append(self.keeper.archives(self.data, self.name)[-1].name)
            time.sleep(1.05)                       # the archive's name carries the second
        kept = [p.name for p in self.keeper.archives(self.data, self.name)]
        self.assertEqual(kept, names[-2:])
        self.assertEqual(self.keeper.KEEP, 5)

    def test_the_same_lines_are_archived_once(self):
        head = b"".join(self.line(n) for n in range(50))
        first = self.keeper.store(self.data, self.name, head)
        self.assertIsNotNone(first)
        self.assertIsNone(self.keeper.store(self.data, self.name, head))
        self.assertEqual(len(self.keeper.archives(self.data, self.name)), 1)
        self.assertEqual(gzip.open(first, "rb").read(), head)

    def test_an_unfinished_last_line_stays_last(self):
        self.fill(0, 1000)
        with open(self.path, "ab") as handle:
            handle.write(b'{"n": 1000, "pad": "half')
        before = self.path.read_bytes()
        self.assertIsNotNone(self.trim())
        live = self.path.read_bytes()
        self.assertTrue(live.endswith(b'{"n": 1000, "pad": "half'))
        self.assertEqual(self.archived() + live, before)

    def test_lines_appended_while_it_cuts_are_neither_lost_nor_doubled(self):
        self.fill(0, 600)
        written = [600]
        stop = threading.Event()

        def writer():
            while not stop.is_set():
                with open(self.path, "ab") as handle:        # open, one line, close: as the fleet's writers do
                    handle.write(self.line(written[0]))
                written[0] += 1

        threads = [threading.Thread(target=writer)]
        threads[0].start()
        try:
            deadline = time.time() + 1.5
            cuts = 0
            while time.time() < deadline:
                if self.trim(limit=40_000, stay=15_000, keep=10_000):
                    cuts += 1
        finally:
            stop.set()
            threads[0].join()
        self.trim(limit=40_000, stay=15_000, keep=10_000)
        everything = self.archived() + self.path.read_bytes()
        numbers = [int(line[6:12]) for line in everything.splitlines()]
        self.assertGreater(cuts, 2)
        self.assertEqual(sorted(numbers), list(range(written[0])), "every line once")
        self.assertTrue(all(len(line) == len(self.line(0)) - 1 for line in everything.splitlines()), "every line whole")

    def test_one_pass_reads_the_table_and_holds_one_lock(self):
        self.keeper.RECORDS.clear()
        self.keeper.SETTLE = 0.1
        self.keeper.RECORDS[self.name] = (0.05, 0.02)
        self.fill(0, 1000)
        lines = self.keeper.one_pass(self.data)
        self.assertEqual(len(lines), 1)
        self.assertEqual(self.keeper.one_pass(self.data), [])
        self.assertTrue(any("market/history.jsonl" in line and "archives 1" in line for line in self.keeper.listing(self.data)))


if __name__ == "__main__":
    unittest.main()
