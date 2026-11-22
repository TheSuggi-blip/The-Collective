"""dispatch.pairs: the runs of each (route, pilot) indexed once per pass list, the same rows in the same order as the
filter over every run row it replaced (a pass took about 52 s against 43 after the stall rest came in); a list that
grew, or another list, is indexed again."""

import importlib.util
import os
from pathlib import Path
import sys
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)
FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))


def load():
    spec = importlib.util.spec_from_file_location("dispatch_pairs_test", FLEET / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PairsTests(unittest.TestCase):
    def setUp(self):
        self.dispatch = load()

    def test_the_index_gives_the_rows_the_old_filter_gave(self):
        rows = [{"route": r, "pilot": p, "n": i} for i, (r, p) in enumerate([("a", "x"), ("b", "x"), ("a", "y"), ("a", "x")])]
        old = [r for r in rows if r.get("route") == "a" and r.get("pilot") == "x"]
        self.assertEqual(self.dispatch.pairs(rows).get(("a", "x")), old)
        self.assertEqual([r["n"] for r in old], [0, 3])
        self.assertIsNone(self.dispatch.pairs(rows).get(("c", "x")))

    def test_a_list_that_grew_or_another_list_is_indexed_again(self):
        rows = [{"route": "a", "pilot": "x"}]
        self.assertEqual(len(self.dispatch.pairs(rows)[("a", "x")]), 1)
        rows.append({"route": "a", "pilot": "x"})
        self.assertEqual(len(self.dispatch.pairs(rows)[("a", "x")]), 2)
        other = [{"route": "b", "pilot": "x"}]
        self.assertNotIn(("a", "x"), self.dispatch.pairs(other))

    def test_the_stall_rest_reads_the_index(self):
        now = 1_800_000_000
        stamp = lambda ago: __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime(now - ago))
        rows = [{"route": "r", "pilot": "x", "started": stamp(300 - i), "minutes": 0.2, "delta": 0} for i in range(3)]
        rows.append({"route": "r", "pilot": "y", "started": stamp(100), "minutes": 20, "delta": 500})
        self.assertIn("short zero-credit runs", self.dispatch.stalled_reason("r", {"kind": "circuit"}, "x", rows, now))
        self.assertIsNone(self.dispatch.stalled_reason("r", {"kind": "circuit"}, "y", rows, now))


if __name__ == "__main__":
    unittest.main()
