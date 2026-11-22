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


class FuelTests(unittest.TestCase):
    """A census never ends where its tank cannot take it on (2026-11-22: a ship read a system without a station
    21 jumps out with 17 fuel and stood two hours in space, every next census refused for fuel). Which stations
    sell fuel: the census files' own reads (services `refuel`); the nearest by the chart's lanes; short by the
    chain's rule (1.5 a jump and 15 over)."""

    def setUp(self):
        self.jumps, self.fuel_stations, self.nearest_fuel, self.fuel_short = load(
            "jumps", "fuel_stations", "nearest_fuel", "fuel_short")
        self.tmp = tempfile.TemporaryDirectory()
        self.data = Path(self.tmp.name)
        (self.data / "scouting").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def scouting(self, system, pois):
        (self.data / "scouting" / (system + ".json")).write_text(json.dumps({"system": {}, "pois": pois}), encoding="utf-8")

    def station(self, poi, base, services):
        return {"poi": {"id": poi, "type": "station", "base_id": base}, "base": {"id": base, "name": "x"}, "services": services}

    def test_a_station_whose_read_lists_refuel_sells_fuel_and_one_without_does_not(self):
        self.scouting("c", {"c_st": self.station("c_st", "base_c", ["market", "refuel", "storage"]),
                            "c_belt": {"poi": {"id": "c_belt", "type": "asteroid_belt"}, "resources": []}})
        self.scouting("d", {"d_st": self.station("d_st", "base_d", ["storage"])})       # a wrecked station: storage only
        self.scouting("e", {"e_belt": {"poi": {"id": "e_belt", "type": "asteroid_belt"}}})
        (self.data / "scouting" / "broken.json").write_text("{", encoding="utf-8")
        self.assertEqual(self.fuel_stations(str(self.data)), {"c": ("c_st", "base_c")})

    def test_no_scouting_folder_gives_no_station(self):
        self.assertEqual(self.fuel_stations(str(self.data / "none")), {})

    def test_the_nearest_station_with_fuel_by_lanes(self):
        stations = {"a": ("a_st", "base_a"), "d": ("d_st", "base_d")}
        self.assertEqual(self.nearest_fuel(LANES, "e", stations), (2, "a", "a_st", "base_a"))
        self.assertEqual(self.nearest_fuel(LANES, "c", stations), (1, "d", "d_st", "base_d"))
        self.assertEqual(self.nearest_fuel(LANES, "d", stations), (0, "d", "d_st", "base_d"))
        self.assertIsNone(self.nearest_fuel(LANES, "e", {}))
        self.assertIsNone(self.nearest_fuel(LANES, "zz", stations))                   # off the chart

    def test_short_by_the_chains_rule_and_an_unread_tank_is_not_judged(self):
        self.assertTrue(self.fuel_short(17, 21))          # the case of 2026-11-22: 21 jumps home on 17
        self.assertFalse(self.fuel_short(95, 21))
        self.assertTrue(self.fuel_short(40, 17))          # 1.5 x 17 + 15 = 40.5
        self.assertFalse(self.fuel_short(41, 17))
        self.assertFalse(self.fuel_short(None, 21))       # the engine gave no fuel: as before, the engine decides
        self.assertFalse(self.fuel_short(17, None))       # no way known: as before


class RemoteBookTests(unittest.TestCase):
    """Game 0.728.0: view_market takes base_id, so a docked census reads the books of other stations from afar.
    Which books: those of data/market that are station books, not the one it is docked at, older than the age,
    the stalest first, at most `limit`."""

    def setUp(self):
        (self.stale_books,) = load("stale_books")
        self.tmp = tempfile.TemporaryDirectory()
        self.data = Path(self.tmp.name)
        (self.data / "market").mkdir()
        self.now = time.time()

    def tearDown(self):
        self.tmp.cleanup()

    def book(self, base, minutes_ago, system="s", items=True):
        path = self.data / "market" / (base + ".json")
        body = {"base": base, "system": system, "read_at": "x"}
        if items:
            body["items"] = []
        path.write_text(json.dumps(body), encoding="utf-8")
        os.utime(path, (self.now - minutes_ago * 60, self.now - minutes_ago * 60))

    def test_the_stalest_books_first_and_never_the_station_docked_at(self):
        self.book("here", 500)
        self.book("old", 300, "far")
        self.book("older", 900, "farther")
        self.book("fresh", 10)
        got = self.stale_books(str(self.data), "here", self.now, 8, 3600)
        self.assertEqual(got, [("older", "farther"), ("old", "far")])

    def test_the_limit_holds_and_files_that_are_no_station_book_are_left_out(self):
        for i in range(5):
            self.book("b%d" % i, 100 + i)
        self.book("history", 999)                               # the ledger's files are not books
        (self.data / "market" / "ladders.json").write_text("{}", encoding="utf-8")
        (self.data / "market" / "b9.json.123.tmp").write_text("{}", encoding="utf-8")
        self.book("noitems", 999, items=False)
        got = self.stale_books(str(self.data), "here", self.now, 2, 3600)
        self.assertEqual([b for b, _ in got], ["b4", "b3"])

    def test_no_market_folder_gives_nothing(self):
        self.assertEqual(self.stale_books(str(self.data / "none"), "here", self.now, 8, 3600), [])


if __name__ == "__main__":
    unittest.main()
