"""The tug (requests ENT-369, ENT-376; errors.log ENT-142): game/fleet/tug.py picks a ship stranded in space with a
tank that cannot reach the nearest station with fuel, never one that is docked, moving, flown by a runner or in a
fight; a pass settles what an earlier pass towed. No engine, no network."""

import os
from pathlib import Path
import sys
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
import tug               # noqa: E402

LANES = {"a": ["b"], "b": ["a", "c"], "c": ["b", "d"], "d": ["c"], "e": []}
STATIONS = {"a": ("a_poi", "a_base")}


def ship(**kw):
    out = {"system": "d", "docked": "", "in_transit": False, "jumping": False, "fuel": 4, "max_fuel": 95,
           "status": "connected"}
    out.update(kw)
    return out


class PickTests(unittest.TestCase):
    def test_a_dry_tank_three_jumps_from_fuel_is_towed(self):
        why = tug.stranded(ship(), "", LANES, STATIONS)
        self.assertTrue(why)
        self.assertIn("3 jumps", why)

    def test_a_docked_ship_is_never_towed(self):
        self.assertIsNone(tug.stranded(ship(docked="d_base"), "", LANES, STATIONS))

    def test_a_ship_on_its_way_is_left_alone(self):
        self.assertIsNone(tug.stranded(ship(in_transit=True), "", LANES, STATIONS))
        self.assertIsNone(tug.stranded(ship(jumping=True), "", LANES, STATIONS))

    def test_a_ship_a_runner_flies_is_left_to_the_runner(self):
        self.assertIsNone(tug.stranded(ship(), "hunt hunt-x", LANES, STATIONS))

    def test_a_ship_held_by_hand_of_another_is_left_alone(self):
        self.assertIsNone(tug.stranded(ship(), "hand Apophis", LANES, STATIONS, mark="hand Unity"))

    def test_a_tank_that_reaches_the_station_is_not_towed(self):
        self.assertIsNone(tug.stranded(ship(fuel=20), "", LANES, STATIONS))
        self.assertIsNone(tug.stranded(ship(system="a", fuel=3), "", LANES, STATIONS))

    def test_a_full_enough_tank_is_never_towed(self):
        self.assertIsNone(tug.stranded(ship(fuel=40), "", LANES, STATIONS, below=25))

    def test_no_station_in_reach_is_towed(self):
        why = tug.stranded(ship(system="e", fuel=10), "", LANES, STATIONS)
        self.assertIn("no station with fuel", why)

    def test_an_unread_tank_or_a_ship_in_a_fight_is_not_judged(self):
        self.assertIsNone(tug.stranded(ship(fuel=None), "", LANES, STATIONS))
        self.assertIsNone(tug.stranded(ship(activity={"kind": "battle"}), "", LANES, STATIONS))
        self.assertIsNone(tug.stranded(ship(status="disconnected"), "", LANES, STATIONS))


class SettleTests(unittest.TestCase):
    def test_a_towed_ship_now_docked_is_refuelled(self):
        self.assertEqual(tug.settle({"at": 100}, ship(docked="x_base"), 200, 15), "refuel")

    def test_a_towed_ship_still_in_space_waits_then_is_given_up(self):
        self.assertEqual(tug.settle({"at": 100}, ship(), 100 + 5 * 60, 15), "wait")
        self.assertEqual(tug.settle({"at": 100}, ship(), 100 + 16 * 60, 15), "give up")


    def test_safe_stations_excludes_pirate_strongholds(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "map").mkdir(parents=True)
            (root / "map/galaxy.tsv").write_text(
                "id\tflags\npublic_sys\tsafe\npirate_sys\tstronghold\n",
                encoding="utf-8",
            )
            (root / "scouting").mkdir(parents=True)
            (root / "scouting/public_sys.json").write_text(
                '{"pois":{"p1":{"base":{"id":"pub_base"},"services":["refuel"]}}}',
                encoding="utf-8",
            )
            (root / "scouting/pirate_sys.json").write_text(
                '{"pois":{"p2":{"base":{"id":"pir_base"},"services":["refuel"]}}}',
                encoding="utf-8",
            )
            got = tug.safe_stations(root, root)
            self.assertIn("public_sys", got)
            self.assertNotIn("pirate_sys", got)


if __name__ == "__main__":
    unittest.main()
