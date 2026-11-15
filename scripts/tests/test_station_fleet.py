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

    def test_the_command_group_is_the_flagships_and_their_guard(self):
        self.fleet.FLAGSHIPS.update({"Prime Directive": {"admiral": "Unity", "division": "Command", "role": "command", "of": "Unity"},
                                     "Zero Point": {"admiral": "Unity", "division": "Command", "role": "command", "of": "Zero"},
                                     "Hades": {"admiral": "Unity", "division": "Command", "role": "command", "of": "Apophis"}})
        self.addCleanup(self.fleet.FLAGSHIPS.clear)
        self.assertEqual(self.fleet.division_of("Prime Directive"), ("Command", "Unity", 0))
        self.assertEqual(self.fleet.division_of("Zero Point"), ("Command", "Unity", 0))
        self.assertEqual(self.fleet.division_of("sentinel-3"), ("Command", "Unity", 3))
        self.assertEqual(self.fleet.division_of("One of Seven"), ("Unassigned", "", 0))
        names = ("sentinel-2", "Zero Point", "miner-1", "Hades", "sentinel-1", "Prime Directive")
        rows = sorted((self.fleet.ship_row(account(n)) for n in names), key=self.fleet.row_order)
        self.assertEqual([(r["name"], r["flagship_of"]) for r in rows],
                         [("Prime Directive", "Unity"), ("Hades", "Apophis"), ("Zero Point", "Zero"), ("sentinel-1", ""), ("sentinel-2", ""), ("miner-1", "")])
        self.assertEqual([r["flagship"] for r in rows], [True, True, True, False, False, False])
        totals = self.fleet.totals(rows)["divisions"]
        self.assertEqual((totals["Command"]["ships"], totals["Command"]["admiral"], totals["Mining"]["ships"]), (5, "Unity", 1))

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

    def test_a_ship_under_a_fresh_order_is_at_work_and_a_stale_order_is_ignored(self):
        import os
        with tempfile.TemporaryDirectory(prefix="fleet-test-") as tmp:
            self.fleet.DATA = Path(tmp)
            (Path(tmp) / "orders").mkdir()
            for name in ("miner-1", "miner-2"):
                (Path(tmp) / "orders" / (name + ".json")).write_text(json.dumps({"pilot": name, "what": "route voidborn-missions-1", "since": "2026-01-01T00:00:00Z"}))
            (Path(tmp) / "orders" / "broken.json").write_text("{not json")
            now = (Path(tmp) / "orders" / "miner-1.json").stat().st_mtime
            os.utime(Path(tmp) / "orders" / "miner-2.json", (now - 3600, now - 3600))
            rows = [self.fleet.ship_row(account(n)) for n in ("miner-1", "miner-2", "miner-3")] + [self.fleet.ship_row(account("miner-4", goal="dock-at"))]
            (Path(tmp) / "orders" / "miner-4.json").write_text(json.dumps({"pilot": "miner-4", "what": "hunt", "since": ""}))
            self.fleet.apply_orders(rows, now)
        self.assertEqual([r["activity"]["kind"] for r in rows], ["order", "idle", "idle", "goal"])
        self.assertEqual([r["order"] for r in rows], ["route voidborn-missions-1", "", "", "hunt"])
        self.assertEqual(self.fleet.totals(rows)["idle"], 2)

    def test_files_are_written_whole(self):
        with tempfile.TemporaryDirectory(prefix="fleet-test-") as tmp:
            path = Path(tmp) / "fleet.json"
            self.fleet.write(path, {"ships": []})
            self.assertEqual(self.fleet.read(path, None), {"ships": []})
            self.assertEqual([p.name for p in Path(tmp).iterdir()], ["fleet.json"])
            self.assertEqual(self.fleet.read(Path(tmp) / "missing.json", "default"), "default")

    def test_rates_count_recurring_income_only(self):
        # one hour: wallets +25,000, earned +24,000 of which 20,000 one-time; 4 ships
        a = [0, 1000, 4, 5000, 0, 100, 2, {"Mining": [4, 1000, 5000, 0, 100, 2]}]
        b = [3600, 26000, 4, 29000, 20000, 400, 6, {"Mining": [4, 26000, 29000, 20000, 400, 6]}]
        r = self.fleet.rates([a, b], 3600)
        self.assertEqual((r["cph"], r["cph_per_ship"], r["net_per_hour"], r["earned_per_hour"]), (5000, 1250, 25000, 4000))
        self.assertEqual((r["ore_per_hour"], r["missions_per_hour"], r["window_minutes"]), (300, 4.0, 60))
        self.assertEqual(r["divisions"]["Mining"]["cph"], 5000)
        self.assertEqual(r["divisions"]["Mining"]["earned_per_hour"], 4000)

    def test_cph_goes_below_zero_when_ships_only_spend(self):
        # one hour of fuel for ore nobody buys: wallets -400, nothing earned
        a = [0, 10000, 2, 500, 0, 0, 0, {"Mining": [2, 10000, 500, 0, 0, 0]}]
        b = [3600, 9600, 2, 500, 0, 90, 0, {"Mining": [2, 9600, 500, 0, 90, 0]}]
        r = self.fleet.rates([a, b], 3600)
        self.assertEqual((r["cph"], r["cph_per_ship"], r["earned_per_hour"]), (-400, -200, 0))

    def test_top_skill_is_the_highest_level_then_the_most_xp(self):
        acc = account("miner-1")
        acc["state"]["skills"] = {"mining": {"level": 3, "xp": 10}, "piloting": {"level": 3, "xp": 90}, "trading": {"level": 0, "xp": 30}}
        self.assertEqual(self.fleet.ship_row(acc)["top_skill"], ["piloting", 3])
        acc["state"]["skills"] = {}
        self.assertEqual(self.fleet.ship_row(acc)["top_skill"], ["", 0])

    def test_rates_need_five_minutes_and_skip_old_rows(self):
        old_style = [0, 1000, 4]                      # rows from before the metrics
        a = [100, 1000, 4, 5000, 0, 0, 0, {}]
        b = [300, 2000, 4, 6000, 0, 0, 0, {}]
        self.assertIsNone(self.fleet.rates([old_style, a, b], 300))
        self.assertIsNone(self.fleet.rates([], 300))

    def test_rates_ignore_samples_older_than_the_window(self):
        ancient = [0, 0, 1, 0, 0, 0, 0, {}]
        a = [10000, 1000, 2, 1000, 0, 0, 0, {}]
        b = [13600, 3000, 2, 3000, 0, 0, 0, {}]
        r = self.fleet.rates([ancient, a, b], 13600)
        self.assertEqual((r["cph"], r["cph_per_ship"]), (2000, 1000))

    def test_sample_splits_one_time_rewards_by_division(self):
        with tempfile.TemporaryDirectory(prefix="fleet-test-") as tmp:
            setattr(self.fleet, "DATA", Path(tmp))
            self.fleet.write(Path(tmp) / "onetime.json", [[10, "miner-6", "x", 1000], [20, "trader-1", "x", 20000], [99, "miner-6", "y", 5]])
            rows = [self.fleet.ship_row(account("miner-6", credits=500)), self.fleet.ship_row(account("trader-1", credits=700))]
            h = self.fleet.sample(50, rows)
            self.assertEqual(h[:5], [50, 1200, 2, 0, 21000])
            self.assertEqual(h[7]["Mining"][3], 1000)
            self.assertEqual(h[7]["Trade"][3], 20000)
            self.assertEqual(h[7]["Mining"][4], 7)


if __name__ == "__main__":
    unittest.main()
