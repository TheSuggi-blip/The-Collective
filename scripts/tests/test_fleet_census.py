"""game/fleet/census.py: the pirates a read keeps, and the next system of a chained census. No engine, no network.

census.py flies a read when it is loaded, so the test takes the functions it needs
out of the file's syntax tree and runs them alone (the way of test_fleet_hunt.py).
"""

import ast
import json
import os
from pathlib import Path
import tempfile
import time
import unittest


CENSUS = Path(__file__).resolve().parents[2] / "game" / "fleet" / "census.py"


def load(*names):
    tree = ast.parse(CENSUS.read_text(encoding="utf-8"))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    missing = set(names) - {node.name for node in found}
    if missing:
        raise AssertionError("census.py has no top-level function %s" % ", ".join(sorted(missing)))
    space = {"json": json, "os": os, "time": time, "Path": Path}
    exec(compile(ast.Module(body=found, type_ignores=[]), str(CENSUS), "exec"), space)
    return [space[n] for n in names]


LANES = {                      # a small chart: home - a - b - c - d, and b - e
    "home": ["a"], "a": ["home", "b"], "b": ["a", "c", "e"], "c": ["b", "d"], "d": ["c"], "e": ["b"],
}


class PirateTests(unittest.TestCase):
    def setUp(self):
        (self.pirate_details,) = load("pirate_details")

    def test_each_pirate_keeps_its_name_faction_tier_hull_and_shield(self):
        near = {"pirate_count": 2, "pirates": [
            {"name": "Flinch", "faction": "pirate_korr", "faction_name": "Grand Marshal Korr", "tier": "scout",
             "hull": 85, "max_hull": 85, "shield": 30, "max_shield": 30, "status": "patrolling", "is_boss": False,
             "pirate_id": "abc", "primary_color": "#66717E"},
            {"name": "Breach Scout", "faction": "pirate_korr", "tier": "scout", "hull": 60, "max_hull": 70},
        ]}
        got = self.pirate_details(near)
        self.assertEqual([p["name"] for p in got], ["Flinch", "Breach Scout"])
        self.assertEqual(got[0]["hull"], 85)
        self.assertEqual(got[0]["max_shield"], 30)
        self.assertEqual(got[0]["faction"], "pirate_korr")
        self.assertNotIn("primary_color", got[0])           # what Military reads, not the paint

    def test_no_list_or_a_broken_one_keeps_nothing(self):
        self.assertEqual(self.pirate_details({"pirate_count": 1}), [])
        self.assertEqual(self.pirate_details({"pirates": "x"}), [])
        self.assertEqual(self.pirate_details({"pirates": [None, 3]}), [])


class ScannerTests(unittest.TestCase):
    """A ship that carries a survey scanner surveys each system it reads (scanning XP, hidden places)."""

    def setUp(self):
        (self.scanner_fitted,) = load("scanner_fitted")

    def test_a_survey_scanner_among_the_modules_is_found(self):
        ship = {"modules": [{"kind": "mining", "name": "Mining Laser I", "slot": "utility", "type": "mining_laser_i"},
                            {"kind": "utility", "name": "Survey Scanner I", "slot": "utility", "type": "survey_scanner_i"}]}
        self.assertTrue(self.scanner_fitted(ship))
        self.assertTrue(self.scanner_fitted({"modules": [{"name": "Survey Scanner II"}]}))

    def test_no_scanner_or_a_broken_file_is_no_scanner(self):
        self.assertFalse(self.scanner_fitted({"modules": [{"type": "mining_laser_i"}, {"type": "pulse_laser_i"}]}))
        self.assertFalse(self.scanner_fitted({"modules": [{"type": "ship_scanner_i", "name": "Ship Scanner I"}]}))
        self.assertFalse(self.scanner_fitted({}))
        self.assertFalse(self.scanner_fitted({"modules": "x"}))
        self.assertFalse(self.scanner_fitted(None))


class ChainTests(unittest.TestCase):
    def setUp(self):
        self.jumps, self.next_system = load("jumps", "next_system")
        self.data = Path(tempfile.mkdtemp())
        (self.data / "scouting").mkdir()
        self.now = time.time()

    def read(self, system, minutes_ago):
        path = self.data / "scouting" / (system + ".json")
        path.write_text("{}", encoding="utf-8")
        os.utime(path, (self.now - minutes_ago * 60, self.now - minutes_ago * 60))

    def test_jumps_counts_lanes_up_to_the_reach(self):
        self.assertEqual(self.jumps(LANES, "b", 2), {"b": 0, "a": 1, "c": 1, "e": 1, "home": 2, "d": 2})
        self.assertEqual(self.jumps(LANES, "b", 1), {"b": 0, "a": 1, "c": 1, "e": 1})

    def test_the_nearest_system_due_is_next_and_a_never_read_one_before_a_stale_one_at_the_same_reach(self):
        route = {"systems": ["d", "c", "e"], "every_minutes": 480}
        self.read("c", 600)                                   # stale, one lane away
        # e is never read and one lane away too: never read first
        self.assertEqual(self.next_system(route, "b", LANES, str(self.data), set(), {"b"}, self.now, 2), "e")
        self.read("e", 10)                                    # now fresh
        self.assertEqual(self.next_system(route, "b", LANES, str(self.data), set(), {"b"}, self.now, 2), "c")

    def test_a_system_another_ship_reads_one_read_on_this_run_or_one_out_of_reach_is_not_next(self):
        route = {"systems": ["c", "d", "e"], "every_minutes": 480}
        self.assertEqual(self.next_system(route, "b", LANES, str(self.data), {"c", "e"}, {"b"}, self.now, 2), "d")
        self.assertIsNone(self.next_system(route, "b", LANES, str(self.data), {"c", "e"}, {"b"}, self.now, 1))
        self.assertIsNone(self.next_system(route, "b", LANES, str(self.data), set(), {"b", "c", "d", "e"}, self.now, 2))

    def test_a_fresh_list_and_a_system_off_the_route_give_nothing(self):
        route = {"systems": ["c"], "every_minutes": 480}
        self.read("c", 30)
        self.assertIsNone(self.next_system(route, "b", LANES, str(self.data), set(), {"b"}, self.now, 2))
        self.assertIsNone(self.next_system({"systems": ["e"], "every_minutes": 60}, "zz", LANES, str(self.data), set(), set(), self.now, 2))


if __name__ == "__main__":
    unittest.main()
