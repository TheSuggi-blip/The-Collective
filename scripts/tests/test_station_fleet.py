"""The fleet collector turns the engine's account records into rows; fixtures only, no engine."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


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
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-test-")       # never the live data folder: rates() reads
        self.addCleanup(self.temp.cleanup)                                   # onetime.json, gifts.jsonl and seed.json there
        self.fleet.DATA = Path(self.temp.name)

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
        self.assertEqual(self.fleet.division_of("sentinel-3"), ("Military", "Apophis", 3))   # lent to Military (D226)
        self.assertEqual(self.fleet.division_of("One of Seven"), ("Unassigned", "", 0))
        names = ("sentinel-2", "Zero Point", "miner-1", "Hades", "sentinel-1", "Prime Directive")
        rows = sorted((self.fleet.ship_row(account(n)) for n in names), key=self.fleet.row_order)
        self.assertEqual([(r["name"], r["flagship_of"]) for r in rows],
                         [("Prime Directive", "Unity"), ("Hades", "Apophis"), ("Zero Point", "Zero"), ("sentinel-1", ""), ("sentinel-2", ""), ("miner-1", "")])
        self.assertEqual([r["flagship"] for r in rows], [True, True, True, False, False, False])
        totals = self.fleet.totals(rows)["divisions"]
        self.assertEqual((totals["Command"]["ships"], totals["Command"]["admiral"], totals["Mining"]["ships"]), (3, "Unity", 1))
        self.assertEqual((totals["Military"]["ships"], totals["Military"]["admiral"]), (2, "Apophis"))

    def test_a_pilot_in_no_division_is_not_of_the_fleet(self):
        rows = [self.fleet.ship_row(account(n)) for n in ("miner-1", "One of Seven", "trader-2")]
        self.assertEqual([r["name"] for r in self.fleet.of_fleet(rows)], ["miner-1", "trader-2"])

    def test_a_pass_with_fewer_pilots_is_held_back_for_ten_minutes(self):
        low, held = {}, self.fleet.held
        self.assertFalse(held(146, 146, 1000, low))
        self.assertTrue(held(6, 146, 1060, low))               # the engine restarted: 6 of 146 are signed in
        self.assertTrue(held(100, 146, 1120, low))
        self.assertFalse(held(146, 146, 1180, low))            # all are back: the hold ends
        self.assertEqual(low, {})
        self.assertTrue(held(140, 146, 2000, low))
        self.assertTrue(held(140, 146, 2599, low))
        self.assertFalse(held(140, 146, 2600, low))            # it stayed low for ten minutes: that is the fleet now
        self.assertFalse(held(0, 0, 3000, {}))                 # a first pass has nothing before it

    def test_a_pilot_the_engine_signed_out_for_good_is_named_and_signed_in_again(self):
        # 2026-11-16: close code 4002 left one pilot signed out for 70 minutes; POST /accounts {"username"} brought it back (queue.log ENT-123)
        calls = []

        class Answer:
            def __init__(self, text):
                self.text = text

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def read(self, n=-1):
                return self.text

        class Opener:
            def __init__(self, listed):
                self.listed = listed

            def open(self, request, timeout=0):
                if isinstance(request, str):
                    calls.append(("GET", request, None))
                    return Answer(json.dumps({"accounts": self.listed}).encode())
                calls.append((request.get_method(), request.full_url, json.loads(request.data)))
                return Answer(b"{}")

        self.fleet.GATE = "http://gate"
        listed = [{"username": "miner-1", "status": "connected"}, {"username": "miner-2", "status": "disconnected"},
                  {"username": "drone-3", "status": "reconnecting"}, {"username": "One of Seven", "status": "disconnected"}, "x", {"status": "disconnected"}]
        self.assertEqual(self.fleet.signed_out(listed), ["miner-2"])                      # of the fleet and signed out; never one that reconnects
        listed = [a for a in listed if not (isinstance(a, dict) and a.get("status") == "reconnecting")]     # no wave of reconnects: the engine is not at it
        gate, away, posts = Opener(listed), {}, lambda: [c for c in calls if c[0] == "POST"]
        self.assertEqual(self.fleet.rejoin(1000, 5000, away, gate), (["miner-2"], []))       # the first look only names it
        self.assertEqual(self.fleet.rejoin(1030, 5030, away, gate), (["miner-2"], []))       # no second look within a minute
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.fleet.rejoin(1060, 5060, away, gate), (["miner-2"], ["miner-2"]))   # still out a minute later: asked back in
        self.assertEqual(posts(), [("POST", "http://gate/accounts", {"username": "miner-2"})])
        self.assertEqual(self.fleet.rejoin(1120, 5120, away, gate), (["miner-2"], []))       # one try per pilot in a quarter of an hour
        self.assertEqual(self.fleet.rejoin(1960, 5960, away, gate), (["miner-2"], ["miner-2"]))
        self.assertEqual(len(posts()), 2)
        gate.listed = [{"username": "miner-2", "status": "connected"}]
        self.assertEqual(self.fleet.rejoin(2020, 6020, away, gate), ([], []))               # it is back: the list is empty ...
        before = len(calls)
        self.assertEqual(self.fleet.rejoin(2400, 6400, away, gate), ([], []))               # ... and the next look comes after ten minutes
        self.assertEqual(len(calls), before)
        young, away = Opener(listed), {}
        self.fleet.rejoin(1000, 100, away, young)
        self.assertEqual(self.fleet.rejoin(1060, 160, away, young), (["miner-2"], []))       # an engine that started under ten minutes ago: nobody is signed in
        self.assertEqual(self.fleet.rejoin(1120, None, away, young), (["miner-2"], []))      # ... nor when its age is not known
        self.assertEqual(posts()[2:], [])

        class Away:
            def open(self, request, timeout=0):
                raise OSError("no engine")

        self.assertEqual(self.fleet.rejoin(5000, 9000, {}, Away()), ([], []))
        wave = Opener([{"username": "miner-2", "status": "disconnected"}, {"username": "miner-4", "status": "reconnecting"}])
        self.assertEqual(self.fleet.rejoin(7000, 9000, {"at": 0, "first": {"miner-2": 0}}, wave), (["miner-2"], []))   # the engine signs pilots in itself: nobody is asked now
        # the switch: STOP or an empty rejoin-off names the pilot and asks nobody; a name in rejoin-off is left signed out, unnamed
        self.assertEqual(self.fleet.left_out(), (True, set()))
        seen_before = {"at": 0, "first": {"miner-2": 0}}
        self.assertEqual(self.fleet.rejoin(7000, 9000, dict(seen_before), Opener(listed), allowed=False), (["miner-2"], []))
        self.assertEqual(self.fleet.rejoin(7000, 9000, dict(seen_before), Opener(listed), never={"miner-2"}), ([], []))
        self.assertEqual(len(posts()), 2)
        (self.fleet.DATA / "rejoin-off").write_text("")
        self.assertEqual(self.fleet.left_out(), (False, set()))
        (self.fleet.DATA / "rejoin-off").write_text("miner-2\n\n")
        self.assertEqual(self.fleet.left_out(), (True, {"miner-2"}))
        (self.fleet.DATA / "STOP").write_text("")
        self.assertEqual(self.fleet.left_out(), (False, {"miner-2"}))

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
        self.assertEqual((total["working"], total["parked"], total["adrift"]), (0, 4, 0))          # docked without work: parked
        self.assertEqual(total["divisions"]["Mining"]["parked"], 2)
        adrift = self.fleet.ship_row(account("miner-3", docked=""))
        self.assertEqual(self.fleet.work_state(adrift), "adrift")
        self.assertEqual(self.fleet.totals([adrift])["adrift"], 1)

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
        r = self.fleet.rates([a, b], 3600, one=[[1800, "miner-1", "a starter reward", 20000]])
        self.assertEqual((r["cph"], r["cph_per_ship"], r["net_per_hour"], r["earned_per_hour"]), (5000, 1250, 25000, 4000))
        self.assertEqual((r["ore_per_hour"], r["missions_per_hour"], r["window_minutes"]), (300, 4.0, 60))
        self.assertEqual(r["divisions"]["Mining"]["cph"], 5000)
        self.assertEqual(r["divisions"]["Mining"]["earned_per_hour"], 4000)
        self.assertEqual(r["windows"]["1h"]["cph"], 5000)
        self.assertEqual(r["windows"]["24h"]["cph"], 5000)                                          # the same two samples: the same figure

    def test_cph_goes_below_zero_when_ships_only_spend(self):
        # one hour of fuel for ore nobody buys: wallets -400, nothing earned
        a = [0, 10000, 2, 500, 0, 0, 0, {"Mining": [2, 10000, 500, 0, 0, 0]}]
        b = [3600, 9600, 2, 500, 0, 90, 0, {"Mining": [2, 9600, 500, 0, 90, 0]}]
        r = self.fleet.rates([a, b], 3600, one=[])
        self.assertEqual((r["cph"], r["cph_per_ship"], r["earned_per_hour"]), (-400, -200, 0))
        self.assertEqual((r["income_per_hour"], r["costs_per_hour"]), (0, 400))

    def test_goods_bought_for_a_one_time_reward_are_no_running_cost(self):
        # one hour: a 2,500 reward for which 600 of goods were bought, 500 of sales, 100 of fuel: wallets +2,300, earned +3,000
        a = [0, 10000, 2, 0, 0, 0, 0, {"Mining": [2, 10000, 0, 0, 0, 0]}]
        b = [3600, 12300, 2, 3000, 1900, 0, 1, {"Mining": [2, 12300, 3000, 1900, 0, 1]}]
        one = [[90, "miner-1", "the mission: goods bought", -600], [100, "miner-1", "the mission", 2500], [9000, "miner-1", "later", 700]]
        r = self.fleet.rates([a, b], 3600, one=one)
        self.assertEqual((r["income_per_hour"], r["costs_per_hour"], r["cph"], r["one_time_per_hour"]), (500, 100, 400, 1900))
        self.assertEqual(r["divisions"]["Mining"]["costs_per_hour"], 100)
        self.assertFalse(r["ships_changed"])
        self.assertNotIn("fuel_cr_per_hour", r)                                                     # no meters in these samples: not measured

    def test_the_meters_count_fuel_and_repairs_and_what_they_cost(self):
        meters = {"fuel_units": 0, "fuel_cr": 0, "hull_points": 0, "repair_cr": 0, "burned": 0, "clean": [0, 0, 0, 0], "div": {}}
        row = lambda **change: dict({"division": "Mining", "docked": "base", "fuel": 50, "hull": 60, "credits": 1000, "cargo_used": 10}, **change)
        step = lambda new, old: self.fleet.meter(new, (old["fuel"], old["hull"], old["credits"], old["cargo_used"]), meters)
        step(row(fuel=40, docked=""), row())                                                        # a jump: fuel burned, nothing bought
        self.assertEqual((meters["burned"], meters["fuel_units"]), (10, 0))
        step(row(fuel=90, credits=920), row(fuel=40))                                               # a refuel alone: 50 units for 80 cr
        self.assertEqual((meters["fuel_units"], meters["fuel_cr"], meters["clean"][:2]), (50, 80, [50, 80]))
        step(row(hull=75, credits=970), row())                                                      # a repair alone: 15 points for 30 cr
        self.assertEqual((meters["hull_points"], meters["repair_cr"]), (15, 30))
        step(row(fuel=75, credits=1500, cargo_used=0), row())                                       # a refuel in the pass of a sale: the average price
        self.assertEqual((meters["fuel_units"], meters["fuel_cr"]), (75, 120))
        step(row(fuel=60, hull=70, credits=954), row())                                             # both in one pass: fuel at its average, the rest is repair
        self.assertEqual((meters["fuel_units"], meters["fuel_cr"], meters["hull_points"], meters["repair_cr"]), (85, 136, 25, 60))
        step(row(fuel=60, docked=""), row())                                                        # fuel that rose in space is not a purchase
        self.assertEqual(meters["fuel_units"], 85)
        self.assertEqual(meters["div"], {"Mining": [85, 136, 25, 60]})
        rows = [self.fleet.ship_row(account("miner-1", credits=100))]
        with tempfile.TemporaryDirectory(prefix="fleet-test-") as tmp:
            setattr(self.fleet, "DATA", Path(tmp))
            a = self.fleet.sample(0, rows, {"fuel_units": 0, "fuel_cr": 0, "hull_points": 0, "repair_cr": 0, "burned": 0, "clean": [0, 0, 0, 0], "div": {}})
            b = self.fleet.sample(3600, rows, meters)
        self.assertEqual((b[8]["w"], b[8]["m"]), ([0, 1, 0], [85, 136, 25, 60, 10]))
        r = self.fleet.rates([a, b], 3600, one=[])
        self.assertEqual((r["fuel_cr_per_hour"], r["repair_cr_per_hour"], r["fuel_units_per_hour"], r["hull_points_per_hour"]), (136, 60, 85, 25))
        self.assertEqual(r["divisions"]["Mining"]["fuel_cr_per_hour"], 136)

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
        self.assertIsNone(self.fleet.rates([old_style, a, b], 300, one=[]))
        self.assertIsNone(self.fleet.rates([], 300, one=[]))

    def test_rates_ignore_samples_older_than_the_window(self):
        ancient = [0, 0, 1, 0, 0, 0, 0, {}]
        a = [10000, 1000, 2, 1000, 0, 0, 0, {}]
        b = [13600, 3000, 2, 3000, 0, 0, 0, {}]
        r = self.fleet.rates([ancient, a, b], 13600, one=[])
        self.assertEqual((r["cph"], r["cph_per_ship"]), (2000, 1000))
        self.assertEqual(r["windows"]["6h"]["cph"], round(3000 * 3600 / 13600))                     # six hours reach back to the first sample
        self.assertTrue(r["windows"]["6h"]["ships_changed"])

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

    # Steady money with gifts between our ships and with new pilots (2026-11-16: the owner saw division figures below zero
    # while the fleet's net rose, and costs below zero). Each test writes the files rates() reads into a temp DATA.

    def put(self, onetime=None, gifts=None, seeds=None):
        if onetime is not None:
            self.fleet.write(self.fleet.DATA / "onetime.json", onetime)
        if gifts is not None:
            (self.fleet.DATA / "gifts.jsonl").write_text("".join((g if isinstance(g, str) else json.dumps(g)) + "\n" for g in gifts))
        if seeds is not None:
            self.fleet.write(self.fleet.DATA / "seed.json", seeds)

    @staticmethod
    def at(t, divisions, spent=None):
        """A history row from {division: [ships, credits, earned]}; with spent ({division: credits spent}) the counter too."""
        row = [t, sum(v[1] for v in divisions.values()), sum(v[0] for v in divisions.values()), sum(v[2] for v in divisions.values()), 0, 0, 0,
               {d: [v[0], v[1], v[2], 0, 0, 0] for d, v in divisions.items()}]
        if spent is not None:
            row.append({"s": sum(spent.values()), "ds": dict(spent)})
        return row

    @staticmethod
    def money(w):
        return (w["income_per_hour"], w["costs_per_hour"], w["cph"])

    def test_a_gift_inside_a_division_changes_no_figure(self):
        # an hour of Mining: sales 3,000, costs 1,000; then the same hour with a gift of 5,000 from miner-1 to miner-2,
        # booked as wallet.py books it (twice in onetime.json, once in gifts.jsonl). The old code read 3,000 less income
        # and 5,000 less costs for it.
        history = [self.at(0, {"Mining": [2, 10000, 5000]}), self.at(3600, {"Mining": [2, 12000, 8000]})]
        plain = self.fleet.rates(history, 3600)
        self.put(onetime=[[1800, "miner-1", "Wallet top-up", -5000], [1800, "miner-2", "Wallet top-up", 5000]],
                 gifts=[{"at": 1800, "from": "miner-1", "to": "miner-2", "credits": 5000}])
        gift = self.fleet.rates(history, 3600)
        self.assertEqual(self.money(plain), (3000, 1000, 2000))
        for key in ("1h", "6h", "24h"):
            w, p = gift["windows"][key], plain["windows"][key]
            self.assertEqual((self.money(w), w["one_time_per_hour"]), (self.money(p), p["one_time_per_hour"]))
            self.assertEqual(self.money(w["divisions"]["Mining"]), (3000, 1000, 2000))
            self.assertEqual((w["divisions"]["Mining"]["transfers_per_hour"], w["transfers_moved_per_hour"]), (0, 5000))

    def test_a_gift_of_the_command_group_to_another_division_moves_neither_division_nor_the_fleet(self):
        mock.patch.dict(self.fleet.ROLES, {"sentinel": ("Command", "Unity")}).start()   # the arithmetic of a guard in Command
        self.addCleanup(mock.patch.stopall)
        # Command (sentinel-1): earned 500, spent 1,500. Trade (trader-1): earned 1,000, spent 400. Then the same hour
        # with sentinel-1 giving trader-1 18,000 (a division without a donor is helped by the command group). The old
        # code read Trade's 18,000 as a reward: income -17,000, costs -17,600.
        plain = [self.at(0, {"Command": [1, 50000, 1000], "Trade": [1, 2000, 100]}), self.at(3600, {"Command": [1, 49000, 1500], "Trade": [1, 2600, 1100]})]
        given = [plain[0], self.at(3600, {"Command": [1, 31000, 1500], "Trade": [1, 20600, 1100]})]
        before = self.fleet.rates(plain, 3600)
        self.put(onetime=[[1800, "sentinel-1", "Wallet top-up", -18000], [1800, "trader-1", "Wallet top-up", 18000]],
                 gifts=[{"at": 1800, "from": "sentinel-1", "to": "trader-1", "credits": 18000}])
        after = self.fleet.rates(given, 3600)
        self.assertEqual(self.money(after), self.money(before))
        self.assertEqual(self.money(after), (1500, 1900, -400))
        self.assertEqual(self.money(after["divisions"]["Command"]), (500, 1500, -1000))
        self.assertEqual(self.money(after["divisions"]["Trade"]), (1000, 400, 600))
        self.assertEqual((after["divisions"]["Command"]["transfers_per_hour"], after["divisions"]["Trade"]["transfers_per_hour"]), (-18000, 18000))
        self.assertEqual((after["transfers_per_hour"], after["transfers_moved_per_hour"], after["transfers_unpaired_per_hour"]), (0, 18000, 0))
        self.assertEqual(after["divisions"]["Trade"]["net_per_hour"], 18600)                       # the old readers' raw wallet change stays as it was

    def test_a_pilot_born_in_the_window_with_a_seed_adds_no_income_costs_or_net(self):
        # miner-1 alone: earned 800, spent 300. miner-2 is first seen at 1,200 s with what the game gives a new pilot;
        # in the second case with a wallet and earned counter of its own (the collector was away when it was born).
        alone = [self.at(0, {"Mining": [1, 1000, 0]}), self.at(3600, {"Mining": [1, 1500, 800]})]
        self.assertEqual(self.money(self.fleet.rates(alone, 3600)), (800, 300, 500))
        for seed, extra in (([1200, 100, 0, 0], (100, 0)), ([1200, 6000, 5000, 900], (6000, 5000))):
            self.put(seeds={"miner-1": [0, 1000, 0, 0], "miner-2": seed, "miner-3": [9999, 70, 0, 0]})   # miner-3: after the window
            born = [alone[0], self.at(3600, {"Mining": [2, 1500 + extra[0], 800 + extra[1]]})]
            r = self.fleet.rates(born, 3600)
            self.assertEqual((self.money(r), self.money(r["divisions"]["Mining"])), ((800, 300, 500), (800, 300, 500)))
            self.assertEqual(r["seed"], {"pilots": 1, "credits": extra[0], "earned": extra[1]})
            self.assertTrue(r["ships_changed"])

    def test_a_ship_the_engine_stops_listing_is_no_loss_and_one_it_lists_again_no_gain(self):
        # 2026-11-16, 22:17 UTC: the engine listed 245 of 246 pilots; income read -71,022 cr an hour while fuel alone cost 46,420
        two = [self.at(0, {"Mining": [2, 3000, 900]}), self.at(3600, {"Mining": [2, 3500, 1700]})]      # earned 800, spent 300
        self.assertEqual(self.money(self.fleet.rates(two, 3600)), (800, 300, 500))
        gone = [two[0], self.at(3600, {"Mining": [1, 1500, 1200]})]                                    # miner-2 left with 2,000 cr and 500 earned
        self.assertEqual(self.money(self.fleet.rates(gone, 3600)), (300, 1800, -1500))                 # no record: its wallet reads as money spent
        (self.fleet.DATA / "presence.jsonl").write_text(json.dumps({"at": 1200, "pilot": "miner-2", "sign": -1, "credits": 2000, "earned": 500, "spent": 0})
                                                        + "\nnot json\n" + json.dumps({"at": 9999, "pilot": "miner-3", "sign": -1, "credits": 70}) + "\n")
        r = self.fleet.rates(gone, 3600)
        self.assertEqual((self.money(r), self.money(r["divisions"]["Mining"])), ((800, 300, 500), (800, 300, 500)))
        self.assertEqual((r["presence"], r["divisions"]["Mining"]["presence"]["left"]), ({"left": 1, "back": 0, "credits": -2000, "earned": -500}, 1))
        with open(self.fleet.DATA / "presence.jsonl", "a") as handle:                                  # ... and it is listed again with what it made meanwhile
            handle.write(json.dumps({"at": 2400, "pilot": "miner-2", "sign": 1, "credits": 2100, "earned": 600, "spent": 0}) + "\n")
        back = [two[0], self.at(3600, {"Mining": [2, 3600, 1800]})]
        r = self.fleet.rates(back, 3600)
        self.assertEqual((self.money(r), r["presence"]), ((800, 300, 500), {"left": 1, "back": 1, "credits": 100, "earned": 100}))
        # the pass writes the events down: who the last picture held and this one does not, who is back; a first sight is the seed record's
        rows = [self.fleet.ship_row(account(n, credits=c)) for n, c in (("miner-1", 900), ("trader-1", 800))]
        path = self.fleet.DATA / "noted.jsonl"
        self.assertEqual(self.fleet.note_presence([], rows, {}, 50, path), [])                          # no picture before: nothing to compare
        events = self.fleet.note_presence(rows, rows[:1], {"miner-1": [0, 900, 0, 0], "trader-1": [0, 800, 0, 0]}, 1000, path)
        self.assertEqual([(e["pilot"], e["sign"], e["credits"]) for e in events], [("trader-1", -1, 800)])
        events = self.fleet.note_presence(rows[:1], rows + [self.fleet.ship_row(account("scout-30", credits=100))], {"miner-1": [0, 900, 0, 0], "trader-1": [0, 800, 0, 0]}, 2000, path)
        self.assertEqual([(e["pilot"], e["sign"], e["credits"]) for e in events], [("trader-1", 1, 800)])     # scout-30 is new: no event
        self.assertEqual([(at, name, sign) for at, name, sign, _c, _e, _s in self.fleet.read_presence(path)], [(1000, "trader-1", -1), (2000, "trader-1", 1)])

    def test_gift_rows_with_an_empty_side_no_credits_or_bad_json_are_handled(self):
        self.put(gifts=[{"at": 100, "from": "miner-1", "to": "trader-1", "credits": 900},
                        {"at": 110, "from": "hauler-2", "to": "", "credits": 19010, "reconstructed": "from the run x"},
                        {"at": 120, "from": "", "to": "scout-21", "credits": 18964, "reconstructed": "from the run y"},
                        {"at": 130, "from": "scout-5", "to": "scout-25", "credits": 0, "unsure": 18498},
                        "{not json", "[1, 2]", json.dumps({"at": "soon", "from": "a", "to": "b", "credits": 5}),
                        json.dumps({"at": 140, "from": "miner-1", "to": "miner-2", "credits": True}), ""])
        gifts = self.fleet.read_gifts(self.fleet.DATA / "gifts.jsonl")
        self.assertEqual(gifts, [(100, "miner-1", "trader-1", 900), (110, "hauler-2", "", 19010), (120, "", "scout-21", 18964)])
        self.assertEqual(self.fleet.transfers(gifts, 0, 200), ({"Mining": -900, "Trade": 900}, 38874, 37974))
        self.assertEqual(self.fleet.transfers(gifts, 100, 200), ({}, 37974, 37974))              # a window holds what lies after its start
        self.fleet.ONE_SIDED = True                                                                 # the switch: the known side moves its division
        self.assertEqual(self.fleet.transfers(gifts, 0, 200)[0], {"Mining": -900, "Trade": 900, "Logistics": -19010, "Intel": 18964})
        self.assertEqual(self.fleet.read_gifts(self.fleet.DATA / "missing.jsonl"), [])
        history = [self.at(0, {"Mining": [1, 5000, 0], "Trade": [1, 5000, 0]}), self.at(3600, {"Mining": [1, 4100, 0], "Trade": [1, 5900, 0]})]
        self.fleet.ONE_SIDED = False
        r = self.fleet.rates(history, 3600)
        self.assertEqual((self.money(r["divisions"]["Mining"]), self.money(r["divisions"]["Trade"])), ((0, 0, 0), (0, 0, 0)))
        self.assertEqual((r["transfers_moved_per_hour"], r["transfers_unpaired_per_hour"]), (38874, 37974))

    def test_net_is_income_less_costs_and_the_divisions_add_up_to_the_fleet_on_a_random_history(self):
        mock.patch.dict(self.fleet.ROLES, {"sentinel": ("Command", "Unity")}).start()   # six roles, one per division
        self.addCleanup(mock.patch.stopall)
        import random
        rnd = random.Random(20261116)
        names = {"Mining": "miner", "Trade": "trader", "Logistics": "hauler", "Military": "drone", "Intel": "scout", "Command": "sentinel"}
        state = {d: [3, 30000, 10000] for d in names}
        history, one, gifts, seeds = [], [], [], {}
        for step in range(200):
            t = step * 300
            for d, v in state.items():
                v[2] += rnd.randint(0, 4000)
                v[1] += rnd.randint(-3000, 4000)
            if rnd.random() < 0.3:
                a, b = rnd.sample(sorted(names), 2)
                credits = rnd.randint(1, 20000) * rnd.choice((1, 0, 1, 1))
                giver, taker = "%s-%d" % (names[a], rnd.randint(1, 3)), "%s-%d" % (names[b], rnd.randint(1, 3))
                giver, taker = rnd.choice(((giver, taker), (giver, taker), (giver, ""), ("", taker)))
                gifts.append({"at": t - 10, "from": giver, "to": taker, "credits": credits})
                state[a][1] -= credits if giver else 0
                state[b][1] += credits if taker else 0
                if giver and taker and credits:
                    one += [[t - 10, giver, "Wallet top-up", -credits], [t - 10, taker, "Wallet top-up", credits]]
            if rnd.random() < 0.2:
                d = rnd.choice(sorted(names))
                one.append([t - 20, "%s-1" % names[d], rnd.choice(("a reward", "goods bought")), rnd.randint(-3000, 6000)])
            if rnd.random() < 0.05:
                d = rnd.choice(sorted(names))
                state[d][0] += 1
                state[d][1] += 100
                seeds["%s-%d" % (names[d], state[d][0])] = [t - 5, 100, 0, 0]
            history.append(self.at(t, {d: list(v) for d, v in state.items()}))
        self.put(onetime=one, gifts=gifts, seeds=seeds)
        for side in (False, True):
            self.fleet.ONE_SIDED = side
            r = self.fleet.rates(history, history[-1][0])
            for key in ("1h", "6h", "24h"):
                w = r["windows"][key]
                for row in [w] + list(w["divisions"].values()):
                    self.assertEqual(row["cph"], row["income_per_hour"] - row["costs_per_hour"])
                    self.assertEqual(row["total_per_hour"], row["cph"] + row["one_time_per_hour"])
                    self.assertLessEqual(abs(row["total_per_hour"] - row["wallets_per_hour"]), 3)   # the net of everything is the change of the wallets, to the rounding
                if not side:                                                                        # one-sided rows moved nothing: the sums meet
                    for field in ("income_per_hour", "costs_per_hour", "cph"):
                        self.assertLessEqual(abs(sum(row[field] for row in w["divisions"].values()) - w[field]), len(names))
                if side:
                    self.assertLessEqual(abs(w["transfers_per_hour"] - sum(row["transfers_per_hour"] for row in w["divisions"].values())), len(names))
                else:
                    self.assertEqual(w["transfers_per_hour"], 0)

    def test_the_game_s_counter_of_credits_spent_stands_beside_the_costs(self):
        rows = [self.fleet.ship_row(account("miner-1", credits=500)), self.fleet.ship_row(account("trader-1", credits=700))]
        rows[0]["spent"], rows[1]["spent"] = 1200, 300
        h = self.fleet.sample(50, rows)
        self.assertEqual((h[8]["s"], h[8]["ds"]), (1500, {"Mining": 1200, "Trade": 300}))
        acc = account("miner-1")
        acc["state"]["player"]["stats"]["credits_spent"] = 4321
        self.assertEqual(self.fleet.ship_row(acc)["spent"], 4321)
        history = [self.at(0, {"Mining": [1, 5000, 0]}, {"Mining": 1000}), self.at(3600, {"Mining": [2, 5100, 900]}, {"Mining": 1700})]
        self.put(seeds={"miner-1": [0, 5000, 0, 1000], "miner-2": [600, 100, 0, 50]})
        r = self.fleet.rates(history, 3600)
        self.assertEqual((r["spent_per_hour"], r["divisions"]["Mining"]["spent_per_hour"]), (650, 650))
        self.assertNotIn("spent_per_hour", self.fleet.rates([self.at(0, {"Mining": [1, 0, 0]}), self.at(3600, {"Mining": [1, 0, 0]})], 3600))

    # 2026-11-17 (the owner: the wallets grow and every division shows a loss): money paid once is a line inside the net.

    def test_the_net_of_everything_is_steady_money_plus_money_paid_once_and_is_the_change_of_the_wallets(self):
        # one hour: a 2,500 reward for which 600 of goods were bought, 500 of sales, 100 of fuel: wallets +2,300
        a = [0, 10000, 2, 0, 0, 0, 0, {"Mining": [2, 10000, 0, 0, 0, 0]}]
        b = [3600, 12300, 2, 3000, 1900, 0, 1, {"Mining": [2, 12300, 3000, 1900, 0, 1]}]
        one = [[90, "miner-1", "the mission: goods bought", -600], [100, "miner-1", "the mission", 2500]]
        r = self.fleet.rates([a, b], 3600, one=one)
        for row in (r, r["divisions"]["Mining"], r["windows"]["24h"]):
            self.assertEqual((row["cph"], row["rewards_per_hour"], row["bought_once_per_hour"], row["one_time_per_hour"]), (400, 2500, 600, 1900))
            self.assertEqual((row["total_per_hour"], row["wallets_per_hour"], row["total_per_ship"]), (2300, 2300, 1150))
        self.assertEqual(r["wallets"], {"start": 10000, "end": 12300, "left_out": 0})
        self.assertNotIn("unexplained_per_hour", r)                                                 # these samples carry no counter of credits spent

    def test_the_purse_counts_the_treasury_s_own_flows_and_moves_between_purses_cancel(self):
        # one hour: wallets +1,000 after a 3,000 deposit into the treasury (so the ships made 4,000); the treasury read
        # 10,000 then 12,500: 3,000 of it our deposit, -500 its own (rent). The whole purse made 3,500 an hour
        a = [0, 20000, 2, 0, 0, 0, 0, {"Mining": [2, 20000, 0, 0, 0, 0]}, {"t": [10000, 0]}]
        b = [3600, 21000, 2, 4000, 0, 0, 0, {"Mining": [2, 21000, 4000, 0, 0, 0]}, {"t": [12500, 3600]}]
        one = [[1800, "miner-1", self.fleet.TREASURY + " (the sweep)", -3000]]
        r = self.fleet.rates([a, b], 3600, one=one)
        self.assertEqual((r["total_per_hour"], r["treasury_moved_per_hour"]), (4000, 3000))
        self.assertEqual((r["treasury_own_per_hour"], r["purse_per_hour"]), (-500, 3500))
        self.assertEqual(r["treasury"], {"start": 10000, "end": 12500, "read_from": 0, "read_to": 3600, "deposited": 3000, "own": -500})
        self.assertEqual(r["windows"]["24h"]["purse_per_hour"], 3500)

    def test_without_two_treasury_readings_the_purse_is_not_guessed(self):
        a = [0, 20000, 2, 0, 0, 0, 0, {"Mining": [2, 20000, 0, 0, 0, 0]}, {"t": [10000, 0]}]
        b = [3600, 21000, 2, 1000, 0, 0, 0, {"Mining": [2, 21000, 1000, 0, 0, 0]}, {"t": [10000, 0]}]
        r = self.fleet.rates([a, b], 3600, one=[])
        self.assertNotIn("purse_per_hour", r)
        self.assertNotIn("treasury_own_per_hour", r)

    def test_a_sample_carries_the_treasury_s_newest_reading(self):
        empire = Path(self.temp.name).parent / "empire"
        state = {"written_at": "2026-11-21T23:00:00Z", "faction": {"treasury": 656122}}
        with mock.patch.object(self.fleet, "DATA", Path(self.temp.name) / "fleet"):
            path = Path(self.temp.name) / "empire" / "empire.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(state))
            self.assertEqual(self.fleet.read_treasury(), [656122, 1795302000])
            path.write_text("{}")
            self.assertIsNone(self.fleet.read_treasury())
        self.assertEqual(self.fleet.sample(60, [], treasury=[5, 1])[8]["t"], [5, 1])

    def test_what_the_game_s_own_counters_do_not_explain_is_named(self):
        # one hour: 900 earned and 700 spent by the game's counters, the wallets rose by 150: 50 left without a record (a tax)
        history = [self.at(0, {"Mining": [1, 5000, 0]}, {"Mining": 1000}), self.at(3600, {"Mining": [1, 5150, 900]}, {"Mining": 1700})]
        self.put(onetime=[], gifts=[], seeds={"miner-1": [0, 5000, 0, 1000]})
        r = self.fleet.rates(history, 3600)
        self.assertEqual((r["unexplained_per_hour"], r["divisions"]["Mining"]["unexplained_per_hour"]), (-50, -50))
        self.assertEqual((r["total_per_hour"], r["wallets"]), (150, {"start": 5000, "end": 5150, "left_out": 0}))

    def test_a_division_s_crew_figures_are_the_averages_of_its_ships(self):
        a, b = account("miner-1"), account("miner-2")
        a["state"]["skills"] = {"piloting": {"level": 6}, "mining": {"level": 8}, "trading": {"level": 1}}
        b["state"]["skills"] = {"piloting": {"level": 3}, "mining": {"level": 5}}
        b["state"]["modules"] = [{"type": "weapon", "type_id": "pulse_laser_i"}, {"type": "weapon", "type_id": "rail_gun"}, {"type": "weapon", "type_id": "not in the catalog"}]
        rows = [self.fleet.ship_row(a), self.fleet.ship_row(b)]
        self.assertEqual((rows[0]["piloting"], rows[1]["piloting"], rows[0]["skill"]), (6, 3, ["mining", 8]))
        got = self.fleet.crew(rows, {"miner-1": a, "miner-2": b}, power={"pulse_laser_i": 10, "rail_gun": 30})
        self.assertEqual(got["Mining"], {"ships": 2, "piloting": 4.5, "levels": 11.5, "skill": ["mining", 6.5], "hp": 155, "weapons": 3,
                                         "firepower": 20.0})                                   # 10 + 30 + 0 on two ships
        self.assertEqual(got[""], got["Mining"])
        bare = account("trader-1")
        bare["state"]["skills"] = None                                                              # a pilot the engine has no skills of
        self.assertEqual(self.fleet.ship_row(bare)["piloting"], 0)
        self.assertEqual(self.fleet.crew([self.fleet.ship_row(bare)], {"trader-1": bare}, power={})["Trade"]["skill"], ["", 0])

    def test_a_weapon_s_power_is_its_damage_per_tick_from_the_newest_catalog(self):
        folder = Path(self.temp.name) / "catalog"
        folder.mkdir()
        old = {"items": [{"id": "pulse_laser_i", "type": "weapon", "damage": 99, "cooldown": 1}]}
        new = {"items": [{"id": "pulse_laser_i", "type": "weapon", "damage": 10, "cooldown": 1}, {"id": "rail_gun", "type": "weapon", "damage": 60, "cooldown": 3},
                         {"id": "mining_laser_i", "type": "mining", "damage": 5}, {"id": "odd", "type": "weapon"}]}
        (folder / "0.9.12.json").write_text(json.dumps(old))
        (folder / "0.10.2.json").write_text(json.dumps(new))                                    # 0.10 is newer than 0.9
        (folder / "ammo.json").write_text("[]")
        self.fleet.POWER.update(file="", at=0.0, by={})
        self.assertEqual(self.fleet.weapon_power(now=1000.0, folder=folder), {"pulse_laser_i": 10.0, "rail_gun": 20.0})
        self.assertEqual(self.fleet.POWER["file"], "0.10.2.json")

    def test_a_wave_of_ships_off_the_game_is_shown_named_and_written_down_once(self):
        wave, version, t = {}, {"now": "0.1.0"}, 100000.0
        note = lambda off, now, **more: self.fleet.note_wave(off, 200, now, wave=wave, version=version, **more)
        self.assertEqual(note(3, t), (None, None))                                                  # three ships off are no wave
        shown, record = note(30, t + 10)
        self.assertEqual((shown["since"], shown["off"], shown["cause"], shown["end"], record), (int(t + 10), 30, "unknown", 0, None))
        version.update(before="0.1.0", now="0.1.1", changed=t + 60)                                 # the game's version read changes
        shown, record = note(80, t + 70)
        self.assertEqual((shown["peak"], shown["cause"], shown["from"], shown["to"]), (80, "update", "0.1.0", "0.1.1"))
        shown, record = note(2, t + 250)                                                            # back: it ended, and settles ten minutes
        self.assertEqual((shown["end"], shown["off"], record), (int(t + 250), 2, None))
        shown, record = note(0, t + 250 + 601)
        self.assertEqual(shown, None)
        self.assertEqual(record, {"since": int(t + 10), "end": int(t + 250), "peak": 80, "ships": 200, "cause": "update", "from": "0.1.0", "to": "0.1.1", "minutes": 4.0})
        self.assertEqual((wave, note(0, t + 900)), ({}, (None, None)))                              # written once
        shown, _record = note(60, t + 5000, engine_started="1970-01-02T05:09:30.000Z")              # 105,000 s: our engine started half a minute before
        self.assertEqual(shown["cause"], "engine")
        wave.clear()
        shown, _record = note(60, t + 9000, engine_started="1970-01-02T03:46:40.000Z")              # an engine start hours before is not the cause
        self.assertEqual(shown["cause"], "unknown")

    def test_the_game_s_version_read_keeps_the_one_before_and_when_it_changed(self):
        stats, version = Path(self.temp.name) / "stats.json", {}
        stats.write_text(json.dumps({"version": "0.1.0"}))
        self.assertEqual((self.fleet.game_version(50, stats, version), version), ("0.1.0", {"now": "0.1.0"}))     # the first reading is no change
        stats.write_text(json.dumps({"version": "0.1.1"}))
        self.fleet.game_version(80, stats, version)
        self.assertEqual(version, {"now": "0.1.1", "before": "0.1.0", "changed": 80})
        stats.write_text("not json")
        self.assertEqual(self.fleet.game_version(90, stats, version), "0.1.1")                      # a file that cannot be read changes nothing

    def test_the_seed_record_puts_every_pilot_of_the_first_start_at_epoch_0_and_a_new_one_at_its_first_pass(self):
        rows = [self.fleet.ship_row(account(n, credits=c)) for n, c in (("miner-1", 900), ("trader-1", 800))]
        self.assertEqual(self.fleet.note_seeds(None, [], 50), (None, False))                       # no pilot read: no record yet
        seeds, changed = self.fleet.note_seeds(None, rows, 1000)
        self.assertEqual((seeds, changed), ({"miner-1": [0, 900, 0, 0], "trader-1": [0, 800, 0, 0]}, True))
        self.assertEqual(self.fleet.note_seeds(seeds, rows, 2000), (seeds, False))
        seeds, changed = self.fleet.note_seeds(seeds, rows + [self.fleet.ship_row(account("scout-30", credits=100))], 3000)
        self.assertEqual((seeds["scout-30"], seeds["miner-1"], changed), ([3000, 100, 0, 0], [0, 900, 0, 0], True))

    def test_the_backfill_puts_the_last_birth_at_its_registration_times(self):
        data = self.fleet.DATA
        self.fleet.write(data / "birth.json", {"started_at": "2026-11-16T23:58:00Z", "registered": ["miner-41", "miner-42", "trader-21", "scout-29"]})
        (data / "birth.log").write_text("12:45:58 miner-41: registered (0.6 s)\n23:58:01 miner-41: registered (0.7 s)\n"
                                        "23:58:01 miner-41: accept market_participation_buying: True\n23:59:30 miner-42: registered (0.5 s)\n"
                                        "00:00:10 trader-21: registered (0.6 s)\nnot a line\n00:01:00 miner-6: registered (0.6 s)\n")
        self.fleet.write(data / "fleet.json", {"ships": [{"name": "miner-6", "credits": 90000, "earned": 5, "spent": 7}, {"name": "miner-41", "credits": 20000}]})
        self.fleet.write(data / "seed.json", {"miner-42": [1794873000, 120, 0, 0], "miner-41": [0, 20000, 0, 0]})
        day = 1794787200                                                                            # 2026-11-16 00:00 UTC
        lines = self.fleet.backfill_seeds(data, dry_run=True)
        self.assertIn("--dry-run", lines[-1])
        self.assertEqual(self.fleet.read(data / "seed.json", None)["miner-41"], [0, 20000, 0, 0])   # a rehearsal writes nothing
        lines = self.fleet.backfill_seeds(data)
        seeds = self.fleet.read(data / "seed.json", None)
        self.assertEqual(seeds["miner-41"], [day + 86280 + 1, 100, 0, 0])                           # the last registration line wins
        self.assertEqual(seeds["trader-21"], [day + 86400 + 10, 100, 0, 0])                         # after midnight: the next day
        self.assertEqual(seeds["miner-42"], [1794873000, 120, 0, 0])                                # a time of its own is kept
        self.assertEqual(seeds["miner-6"], [0, 90000, 5, 7])                                        # no pilot of this birth: epoch 0
        self.assertNotIn("scout-29", seeds)                                                         # named, never registered
        self.assertIn("2 put at their registration time", lines[1])
        self.assertEqual(self.fleet.backfill_seeds(data)[-1], "seed: nothing to change")
        self.fleet.write(data / "birth.json", {"registered": []})
        self.assertIn("nothing written", self.fleet.backfill_seeds(data)[0])


    def test_meter_ignores_capex_outliers_and_hull_class_switches(self):
        meters = {"fuel_units": 0, "fuel_cr": 0, "hull_points": 0, "repair_cr": 0, "burned": 0, "clean": [50, 80, 15, 30], "div": {}}
        row = lambda **change: dict({"division": "Mining", "docked": "base", "fuel": 50, "hull": 60, "credits": 1000, "cargo_used": 10, "class": "Threshold"}, **change)
        # ENT-186: a 278,000 cr hull commission sharing a refuel pass uses clean fuel avg, never books as fuel or poisons clean
        self.fleet.meter(row(fuel=70, credits=1000 - 278032), (50, 60, 1000, 10, "Threshold"), meters)
        self.assertEqual(meters["clean"], [50, 80, 15, 30])
        self.assertEqual((meters["fuel_units"], meters["fuel_cr"]), (20, 32))
        # ENT-186: switching hull class (Threshold -> Recursion) must not book higher hull/fuel as repair/refuel
        self.fleet.meter(row(fuel=200, hull=600, credits=1000, **{"class": "Recursion"}), (50, 150, 225430, 10, "Threshold"), meters)
        self.assertEqual((meters["fuel_units"], meters["hull_points"], meters["repair_cr"]), (20, 0, 0))



    def test_bursar_buy_escrow_excluded_from_costs_and_recognizes_fills(self):
        """Buy-order escrow locks/releases produce 0 operating cost; fills recognize exact COGS without polluting treasury."""
        t0, t1, t2 = 10000, 13600, 17200
        # Window 1 (t0 -> t1): trader-1 locks 20,000 cr into Exchange buy escrow (wallet drops 100k -> 80k, earned 0)
        h_lock = [
            [t0, 100000, 1, 0, 0, 0, 0, {"Trade": [1, 100000, 0, 0, 0, 0]}],
            [t1, 80000, 1, 0, 0, 0, 0, {"Trade": [1, 80000, 0, 0, 0, 0]}],
        ]
        one_lock = [[t0 + 100, "trader-1", "Exchange buy escrow: locked", -20000]]
        r_lock = self.fleet.window(h_lock, t1, 3600, one=one_lock)
        self.assertEqual(r_lock["costs_per_hour"], 0)
        self.assertEqual(r_lock["bought_once_per_hour"], 0)
        self.assertEqual(r_lock["treasury_moved_per_hour"], 0)
        self.assertEqual(r_lock["divisions"]["Trade"]["costs_per_hour"], 0)

        # Window 2 (t1 -> t2): order fills (wallet stays 80k, escrow_fill books +20,000 -> COGS = +20,000 cr/h)
        h_fill = [
            [t1, 80000, 1, 0, 0, 0, 0, {"Trade": [1, 80000, 0, 0, 0, 0]}],
            [t2, 80000, 1, 0, 0, 0, 0, {"Trade": [1, 80000, 0, 0, 0, 0]}],
        ]
        one_fill = one_lock + [[t1 + 100, "trader-1", "Exchange buy escrow: filled", 20000]]
        r_fill = self.fleet.window(h_fill, t2, 3600, one=one_fill)
        self.assertEqual(r_fill["costs_per_hour"], 20000)
        self.assertEqual(r_fill["divisions"]["Trade"]["costs_per_hour"], 20000)
        self.assertEqual(r_fill["treasury_moved_per_hour"], 0)

if __name__ == "__main__":
    unittest.main()
