"""game/fleet/gauges.py on a disposable data folder: a ship's and a side's firepower and toughness against the herds (rule F9). No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record (the hive verb loads hive.py)


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gauges = load("gauges")
CATALOG = {"version": "1.0", "items": [{"id": "pulse_laser_i", "type": "weapon", "damage": 10, "cooldown": 1},
                                       {"id": "piercing_railgun_i", "type": "weapon", "damage": 60, "cooldown": 3},
                                       {"id": "mining_laser_i", "type": "mining"}]}
HERDS = [("calm_ray", "grazer", 70), ("slag_tortoise", "grazer", 90), ("mantis", "predator", 60), ("pilot_whale", "grazer", 220),
         ("cloudwhale", "grazer", 486), ("cloudwhale", "grazer", 3304)]


def ship(name, guns=("pulse_laser_i",), levels=(4, 2, 3), hull=75, shield=130):
    """A live ship file: the fixture of rule F9, one Pulse Laser I, Gunnery 4, Weapons 2, Tactics 3, hull 75, shield 130."""
    modules = [{"kind": "mining", "slot": "utility", "type": "mining_laser_i"}] + [{"kind": "weapon", "slot": "weapon", "type": g} for g in guns]
    skills = {k: {"level": v, "xp": 0} for k, v in zip(("gunnery", "weapons", "tactics"), levels)}
    skills["mining"] = {"level": 9, "xp": 0}                                     # no combat skill: raises nothing
    return {"name": name, "modules": modules, "skills": skills, "hull": 60, "max_hull": hull, "shield": 999, "max_shield": shield}


class Folder(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-gauges-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("fleet/ships", "catalog", "wildlife"):
            (self.data / folder).mkdir(parents=True)
        self.put("catalog/1.0.json", CATALOG)
        self.put("wildlife/mid.json", {"system": "mid", "pois": {"mid_cloud": {"creatures": [
            {"species": s, "role": r, "hull": h, "max_hull": h} for s, r, h in HERDS]}}})
        self.fleet([ship("drone-1"), ship("drone-2"), ship("drone-3"), ship("miner-1", guns=(), levels=(0, 0, 0), shield=80)])

    def put(self, name, value):
        (self.data / name).write_text(json.dumps(value), encoding="utf-8")

    def fleet(self, ships):
        self.put("fleet/fleet.json", {"ships": [{"name": s["name"]} for s in ships]})
        for s in ships:
            self.put("fleet/ships/%s.json" % s["name"], s)

    def book(self):
        return gauges.read(str(self.data))


class ShipTests(Folder):
    def test_the_fixture_ship_has_firepower_10_9_and_toughness_205(self):
        firepower, toughness = gauges.ship_gauges("drone-1", data=str(self.data))
        self.assertAlmostEqual(firepower, 10.9)                                   # 10 x (1 + 0.04 + 0.02 + 0.03)
        self.assertEqual(toughness, 205)                                          # max_hull 75 + max_shield 130, not the hull and shield of the moment
        self.assertEqual(gauges.ship_gauges("miner-1", data=str(self.data)), (0, 155))   # unarmed: toughness only
        self.assertIsNone(gauges.ship_gauges("nobody", data=str(self.data)))

    def test_a_weapon_counts_its_damage_per_tick(self):
        self.fleet([ship("drone-9", guns=("piercing_railgun_i", "unknown_gun"), levels=(0, 0, 0))])
        self.assertEqual(gauges.ship_gauges("drone-9", data=str(self.data))[0], 20)      # 60 every 3 ticks; a module the catalog lacks adds nothing


class CreatureTests(Folder):
    def test_a_creature_weighs_its_hull_and_a_predator_twice_its_hull(self):
        book = self.book()
        self.assertEqual(gauges.creature("calm_ray", book=book), (70, 70))
        self.assertEqual(gauges.creature("mantis", book=book), (60, 120))
        self.assertEqual(gauges.creature("cloudwhale", book=book), (3304, 3304))  # the highest hull any reading saw
        self.assertIsNone(gauges.creature("unseen", book=book))

    def test_one_ship_passes_70_fails_90_on_firepower_and_a_60_predator_on_toughness(self):
        book = self.book()
        self.assertEqual(gauges.passes("drone-1", "calm_ray", book=book), (True, True))         # 70 <= 76.3 and 70 <= 102.5
        self.assertEqual(gauges.passes("drone-1", "slag_tortoise", book=book), (False, True))   # 90 > 76.3
        self.assertEqual(gauges.passes("drone-1", "mantis", book=book), (True, False))          # weighs 120 > 102.5
        self.assertEqual(gauges.passes("drone-1", "unseen", book=book), (False, False))

    def test_three_ships_pass_a_220_hull_grazer(self):
        book = self.book()
        firepower, toughness = gauges.side_gauges(["drone-1", "drone-2", "drone-3"], book=book)
        self.assertAlmostEqual(firepower, 32.7)
        self.assertAlmostEqual(firepower * gauges.KILL_FACTOR, 228.9)
        self.assertEqual((toughness, toughness * gauges.STAND_SHARE), (615, 307.5))
        self.assertEqual(gauges.passes(["drone-1", "drone-2", "drone-3"], "pilot_whale", book=book), (True, True))
        self.assertEqual(gauges.passes(["drone-1", "drone-2"], "pilot_whale", book=book), (False, False))  # 152.6 and 205 under 220
        self.assertEqual(gauges.passes((32.7, 615), "pilot_whale", book=book), (True, True))


class GroupTests(Folder):
    def test_the_smallest_group_of_typical_ships_passes_both_gauges(self):
        book = self.book()
        self.assertEqual(gauges.typical("drone", book=book)[:2], (10.9, 205))
        self.assertEqual([gauges.smallest_group("drone", s, book=book) for s in ("calm_ray", "slag_tortoise", "mantis", "pilot_whale", "cloudwhale", "unseen")],
                         [1, 2, 2, 3, None, None])                                # 3304 hull takes 44 ships: beyond GROUP_MAX
        self.assertEqual(gauges.smallest_group("drone", "cloudwhale", max_n=50, book=book), 44)

    def test_a_role_without_ships_on_file_is_the_fleet_and_no_ship_at_all_a_starter(self):
        book = self.book()
        self.assertEqual(gauges.typical("trader", book=book)[2], "no trader ship on file: median of the fleet's 4 ship(s)")
        self.assertEqual(gauges.typical("all", book=book)[:2], (10.9, 205))      # the median of three drones and one miner
        self.fleet([])
        for path in (self.data / "fleet" / "ships").glob("*.json"):
            path.unlink()
        empty = self.book()
        self.assertEqual(gauges.typical("drone", book=empty)[:2], (10.0, 155))
        self.assertEqual(gauges.smallest_group("drone", "calm_ray", book=empty), 1)      # 70 <= 70 and 70 <= 77.5


class CommandTests(Folder):
    def run_main(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = gauges.main(list(args) + ["--data", str(self.data)])
        return code, out.getvalue()

    def test_the_three_answers(self):
        code, text = self.run_main("ship", "drone-1", "nobody")
        self.assertEqual(code, 1)
        self.assertIn("drone-1 (drone) | pulse_laser_i 10 a tick | gunnery 4, weapons 2, tactics 3: +9% | hull 75 + shield 130 | firepower 10.9: kills up to 76.3 hull", text)
        self.assertIn("`nobody`: no ship file of that name", text)
        code, text = self.run_main("side", "drone-1", "drone-2", "drone-3")
        self.assertEqual(code, 0)
        self.assertIn("firepower 32.7: kills up to 228.9 hull | toughness 615: stands up to 307.5 weight", text)
        self.assertIn("passes 4 of the 5 species of our readings: calm_ray, slag_tortoise, mantis, pilot_whale", text)
        code, text = self.run_main("species", "--role", "drone")
        lines = {line.split()[0]: line for line in text.splitlines()[2:]}
        self.assertEqual(code, 0)
        self.assertTrue(lines["calm_ray"].rstrip().endswith("passes                       1"))
        self.assertIn("fails firepower", lines["slag_tortoise"])
        self.assertIn("fails toughness", lines["mantis"])
        self.assertTrue(lines["cloudwhale"].endswith("none of 20 or fewer"))

    def test_the_hive_verb_hands_over_to_gauges(self):
        hive, out = load("hive"), io.StringIO()
        with mock.patch.object(sys, "argv", ["hive.py", "--data", str(self.data), "gauges", "side", "drone-1", "drone-2", "drone-3"]), contextlib.redirect_stdout(out):
            code = hive.main()
        self.assertEqual(code, 0)
        self.assertIn("SIDE of 3 ship(s): drone-1, drone-2, drone-3 | firepower 32.7: kills up to 228.9 hull", out.getvalue())


if __name__ == "__main__":
    unittest.main()
