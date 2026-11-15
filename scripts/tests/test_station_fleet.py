"""The fleet collector turns the engine's account records into rows; fixtures only, no engine."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / "station" / "fleet.py"


def account(name, system="nexus_prime", credits=100, loop=None, goal=None, docked="central_nexus", status="connected"):
    return {
        "username": name, "status": status, "loop": loop,
        "hasExecutingGoal": bool(goal), "executingGoal": {"goalType": goal, "startedAt": "2026-01-01T00:00:00Z"} if goal else None,
        "hasRunningJob": False, "runningJob": None,
        "state": {
            "player": {"empire": "voidborn", "credits": credits, "home_base": "central_nexus", "stats": {"ore_mined": 7}},
            "ship": {"class_name": "Threshold", "hull": 75, "max_hull": 75, "shield": 80, "max_shield": 80, "fuel": 90, "max_fuel": 95,
                     "cargo_used": 10, "cargo_capacity": 66},
            "location": {"system_id": system, "system_name": "Nexus Prime" if system else "", "poi_id": "the_core", "poi_name": "The Core",
                         "docked_at": docked, "in_transit": False},
            "cargo": [{"item_id": "copper_ore", "item_name": "Copper Ore", "quantity": 10}],
            "modules": [{"type_id": "mining_laser_i", "name": "Mining Laser I", "type": "mining", "slot": "utility"}],
            "skills": {"mining": {"level": 1, "xp": 70, "next_level_xp": 165}, "cooking": {"level": 0, "xp": 0, "next_level_xp": 60}},
            "missions": {"active": [{"title": "Iron Supply Run", "type": "mining", "percent_complete": 50, "rewards": {"credits": 1500},
                                     "objectives": [{"description": "Mine 30 units of Iron Ore", "current": 15, "required": 30, "completed": False}]}]},
            "updatedAt": "2026-01-01 00:00:00",
        },
    }


class FleetCollectorTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("fleet_under_test", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.fleet = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.fleet)

    def test_division_comes_from_the_role_word(self):
        self.assertEqual(self.fleet.division_of("miner-12"), ("Mining", "Zero", 12))
        self.assertEqual(self.fleet.division_of("trader-1"), ("Trade", "Mercury", 1))
        self.assertEqual(self.fleet.division_of("hauler-3"), ("Logistics", "Apollo", 3))
        self.assertEqual(self.fleet.division_of("drone-9"), ("Military", "Apophis", 9))
        self.assertEqual(self.fleet.division_of("scout-2"), ("Intel", "Oracle", 2))

    def test_a_name_outside_the_rule_is_unassigned(self):
        for name in ("One of Seven", "miner", "miner-x", "pirate-1", "", None):
            self.assertEqual(self.fleet.division_of(name), ("Unassigned", "", 0))

    def test_file_name_has_no_path_characters(self):
        self.assertEqual(self.fleet.file_name("One of Seven"), "One_of_Seven")
        self.assertEqual(self.fleet.file_name("../../etc/passwd"), ".._.._etc_passwd")
        self.assertNotIn("/", self.fleet.file_name("a/b\\c"))

    def test_row_carries_position_gauges_and_activity(self):
        row = self.fleet.ship_row(account("miner-1", credits=2046, loop={"type": "mining", "running": True, "startedAt": "t"}))
        self.assertEqual((row["name"], row["division"], row["admiral"], row["number"]), ("miner-1", "Mining", "Zero", 1))
        self.assertEqual((row["system"], row["docked"], row["credits"]), ("nexus_prime", "central_nexus", 2046))
        self.assertEqual((row["cargo_used"], row["cargo_capacity"], row["fuel"], row["max_fuel"]), (10, 66, 90, 95))
        self.assertEqual(row["activity"]["kind"], "loop")
        self.assertEqual(row["missions"], 1)

    def test_activity_order_is_loop_then_goal_then_idle(self):
        self.assertEqual(self.fleet.activity(account("miner-1", goal="dock-at"))["type"], "dock-at")
        self.assertEqual(self.fleet.activity(account("miner-1"))["kind"], "idle")
        stopped = account("miner-1", loop={"type": "mining", "running": False})
        self.assertEqual(self.fleet.activity(stopped)["kind"], "idle")

    def test_detail_keeps_only_skills_in_use_and_never_a_password(self):
        acc = account("miner-1")
        acc["password"] = "must-not-be-copied"
        detail = self.fleet.ship_detail(acc, self.fleet.ship_row(acc))
        self.assertEqual(list(detail["skills"]), ["mining"])
        self.assertEqual(detail["cargo"], [{"item": "copper_ore", "name": "Copper Ore", "quantity": 10}])
        self.assertEqual(detail["mission_list"][0]["objectives"][0]["current"], 15)
        self.assertNotIn("must-not-be-copied", json.dumps(detail))

    def test_totals_add_up_per_division(self):
        rows = [self.fleet.ship_row(account(n, credits=c)) for n, c in (("miner-1", 100), ("miner-2", 250), ("trader-1", 1000), ("One of Seven", 500))]
        total = self.fleet.totals(rows)
        self.assertEqual((total["ships"], total["credits"], total["connected"]), (4, 1850, 4))
        self.assertEqual(total["divisions"]["Mining"]["credits"], 350)
        self.assertEqual(total["divisions"]["Mining"]["ships"], 2)
        self.assertEqual(total["divisions"]["Unassigned"]["ships"], 1)
        self.assertEqual(total["idle"], 4)

    def test_files_are_written_whole(self):
        with tempfile.TemporaryDirectory(prefix="fleet-test-") as tmp:
            path = Path(tmp) / "fleet.json"
            self.fleet.write(path, {"ships": []})
            self.assertEqual(self.fleet.read(path, None), {"ships": []})
            self.assertEqual([p.name for p in Path(tmp).iterdir()], ["fleet.json"])
            self.assertEqual(self.fleet.read(Path(tmp) / "missing.json", "default"), "default")


if __name__ == "__main__":
    unittest.main()
