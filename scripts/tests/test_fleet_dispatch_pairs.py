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


    def test_runs_that_read_or_reached_nothing_rest_whatever_their_minutes(self):
        # requests ENT-334, errors.log ENT-121: 63 refused census runs of 1.5 minutes each, places 0, delta 0, no note
        now = 1_800_000_000
        stamp = lambda ago: __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime(now - ago))
        refused = [{"route": "census-worked-far", "kind": "census", "pilot": "x", "started": stamp(600 - 150 * i), "minutes": 1.5,
                    "places": 0, "creatures": 0, "delta": 0, "notes": []} for i in range(3)]
        census = {"kind": "census"}
        self.assertIn("read or reached nothing", self.dispatch.stalled_reason("census-worked-far", census, "x", refused, now))
        read = refused[:2] + [dict(refused[2], places=3, delta=-95)]
        self.assertIsNone(self.dispatch.stalled_reason("census-worked-far", census, "x", read, now))
        noted = [{"route": "c", "kind": "circuit", "pilot": "x", "started": stamp(900 - 200 * i), "minutes": 4, "delta": -40,
                  "notes": ["alderamin not reached"]} for i in range(3)]
        self.assertIn("read or reached nothing", self.dispatch.stalled_reason("c", {"kind": "circuit"}, "x", noted, now))
        self.assertIsNone(self.dispatch.stalled_reason("c", {"kind": "circuit"}, "x", noted[:2], now))
        self.assertIsNone(self.dispatch.stalled_reason("c", {"kind": "guard"}, "x", noted, now))
        long_ago = [dict(r, started=stamp(4 * 3600)) for r in refused]
        self.assertIsNone(self.dispatch.stalled_reason("census-worked-far", census, "x", long_ago, now))

    def test_requires_strict_follows_the_switch_file(self):
        # requests ENT-332: a hand-over route opens by itself the minute strict classes go on
        import tempfile
        keep = self.dispatch.workclass.DATA
        self.addCleanup(setattr, self.dispatch.workclass, "DATA", keep)
        with tempfile.TemporaryDirectory() as data:
            (Path(data) / "fleet").mkdir()
            state = {"data": data, "rows": [], "orders": {}, "now": 1_800_000_000}
            pilot = {"name": "miner-1", "role": "miner", "docked": True}
            on = {"kind": "circuit", "requires": {"strict": True}, "stops": []}
            off = {"kind": "circuit", "requires": {"strict": False}, "stops": []}
            self.dispatch.workclass.SEEN.clear()
            self.assertEqual(self.dispatch.why_not(pilot, "give", on, state)[0], "open only while strict classes are on")
            self.assertNotEqual(self.dispatch.why_not(pilot, "keep", off, state)[0], "open only while strict classes are off")
            (Path(data) / "fleet" / "strict-classes-on").write_text("")
            self.dispatch.workclass.SEEN.clear()
            self.assertNotEqual(self.dispatch.why_not(pilot, "give", on, state)[0], "open only while strict classes are on")
            self.assertEqual(self.dispatch.why_not(pilot, "keep", off, state)[0], "open only while strict classes are off")
            self.dispatch.workclass.SEEN.clear()

if __name__ == "__main__":
    unittest.main()
