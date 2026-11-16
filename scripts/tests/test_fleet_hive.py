"""game/fleet/hive.py on a disposable data folder: what the stations bid in all, a field's change between two readings, a route's runs in a window. No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-hive-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("market", "scouting", "wildlife", "fleet/ships", "routes", "catalog", "stock", "intel"):
            (self.data / folder).mkdir(parents=True)
        self.hive = load("hive")
        book = lambda base, system, bid, units: (self.data / "market" / (base + ".json")).write_text(json.dumps(
            {"base": base, "system": system, "read_at": "2026-11-16T00:00:00Z", "items": [{"item_id": "water_ice", "best_buy": bid, "best_buy_qty": units, "best_sell": 0}]}))
        book("hub", "home", 38, 6000)
        book("a" * 32, "far", 20, 4000)
        book("low", "home", 5, 90000)

    def test_demand_adds_the_stations_that_pay_and_names_a_players_station_by_its_system(self):
        market, where = self.hive.books(str(self.data))
        self.assertEqual(self.hive.demand(market, "water_ice", 16), (38, 10000, 2, "hub"))        # the bid of 5 cr does not count
        self.assertEqual(self.hive.demand(market, "iron_ore", 1), (0, 0, 0, ""))
        self.assertEqual((self.hive.label("hub", where), self.hive.label("a" * 32, where)), ("hub", "station in far"))

    def test_a_field_s_change_is_measured_between_its_first_and_last_census(self):
        hour = lambda h: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(1_800_000_000 + h * 3600))
        rows = [{"at": hour(0), "system": "far", "deposits": {"belt": {"water_ice": 1000}}, "herds": {"belt": {"veil_ray": 6}}},
                {"at": hour(2), "system": "far", "deposits": {"belt": {"water_ice": 1500}}, "herds": {"belt": {"veil_ray": 2}}},
                {"at": hour(2), "system": "home", "deposits": {"rock": {"iron_ore": 7}}}]
        (self.data / "wildlife" / "history.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        rates, herds = self.hive.regrowth(str(self.data))
        self.assertEqual(rates, {("far", "belt", "water_ice"): 250.0})                             # one reading is no rate
        self.assertEqual(herds[("far", "belt", "veil_ray")], (2, 6, 2))

    def test_a_window_counts_steady_credits_and_keeps_what_is_paid_once_apart(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        rows = [{"route": "r", "started": stamp(600), "minutes": 30, "delta": 1000, "credits_before": 5000, "credits_after": 6000},
                {"route": "r", "started": stamp(900), "minutes": 30, "delta": 4000, "one_time": 3000, "credits_before": 5000, "credits_after": 9000},
                {"route": "r", "started": stamp(90000), "minutes": 30, "delta": 99, "credits_before": 1, "credits_after": 100}]
        self.assertEqual(self.hive.window_stats(rows, now - 3600)["r"], [2, 2000.0, 60.0, 3000])

    def test_what_comes_back_is_the_sum_of_the_rises_between_readings(self):
        self.assertEqual(self.hive.moves([(0, 100), (3600, 40), (7200, 90), (10800, 90)]), (50, 60, 3.0))
        self.assertEqual(self.hive.moves([(0, 5)]), (0, 0, 0.0))
        # 72 units at 38 are sold out and the step of 7,470 at 34 comes into view: no refill; then 72 at 38 stand again: 72 came back
        self.assertEqual(self.hive.bid_moves([(0, 72, 38), (60, 7470, 34), (120, 7400, 34), (180, 72, 38), (240, 90, 38)]), (72 + 18, 72 + 70))
        self.assertEqual(self.hive.bid_moves([(0, 67284, 18), (60, 67515, 19), (120, 56480, 21)]), (0, 0))      # a deep bid whose price creeps is the same demand
        hour = lambda h: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(1_800_000_000 + h * 3600))
        with open(self.data / "wildlife" / "history.jsonl", "w") as handle:
            for h, herd in ((0, {"belt": {"veil_ray": 6}}), (1, {}), (2, {"belt": {"veil_ray": 4}})):
                handle.write(json.dumps({"at": hour(h), "system": "far", "deposits": {"belt": {"water_ice": 1000 - 100 * h}}, "herds": herd, "pilots": {"belt": 0}}) + "\n")
        with open(self.data / "market" / "history.jsonl", "w") as handle:
            for h, units in ((0, 500), (1, 100), (2, 400)):
                handle.write(json.dumps({"t": hour(h), "base": "hub", "item": "water_ice", "bid": 38, "bid_qty": units, "ask": 0, "ask_qty": 0}) + "\n")
        bids, deposits, herds = self.hive.series(str(self.data))
        self.assertEqual([units for _t, units, _bid in bids[("hub", "water_ice")]], [500, 100, 400])
        self.assertEqual([c for _t, c in herds[("far", "belt", "veil_ray")]], [6, 0, 4])          # the herd was gone at the second reading of its place
        self.assertEqual(self.hive.moves(herds[("far", "belt", "veil_ray")])[:2], (4, 6))
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.hive.show_refill(str(FLEET.parent), str(self.data), time.time()), 0)
        self.assertIn("water_ice", printed.getvalue())
        self.assertIn("veil_ray", printed.getvalue())

    def test_work_is_counted_per_pilot_and_per_route_in_one_unit(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        rows = [{"route": "r", "pilot": "miner-1", "started": stamp(600), "minutes": 30, "delta": 1000, "credits_before": 1000, "credits_after": 2000},
                {"route": "r", "pilot": "miner-2", "started": stamp(900), "minutes": 30, "delta": 4000, "credits_before": 1000, "credits_after": 5000, "one_time": 3000},
                {"route": "r", "pilot": "miner-1", "started": stamp(9000), "minutes": 30, "delta": 8000, "credits_before": 1000, "credits_after": 9000}]
        by_pilot, by_route = self.hive.pilot_stats(rows, now - 3600)
        self.assertEqual(by_pilot["miner-1"], [1, 1000.0, 30.0, 0, 30.0])
        self.assertEqual(by_route["r"], [2, 2000.0, 60.0, 3000, 60.0])
        self.assertEqual(self.hive.per_hour(2000, 60), "2,000")
        self.assertEqual(self.hive.per_hour(2000, 0), "--")

    def test_the_scale_is_a_route_that_repeats_never_a_fitting_or_a_mission(self):
        hive = self.hive if hasattr(self, "hive") else load("hive")
        routes = {"mine": {"id": "mine", "kind": "mine", "sell": [{"item": "ice", "min_price": 1}]}, "gather": {"id": "gather", "kind": "mine"}, "fit": {"id": "fit", "kind": "circuit", "stops": [{"at": "a:b:c", "fit": "ice_harvester_i"}]},
                  "once": {"id": "once", "kind": "circuit", "once": True, "stops": [{"at": "a:b:c"}]}}
        by_route = {"mine": [3, 9000.0, 90.0, 0, 90.0], "fit": [2, 50000.0, 30.0, 0, 30.0], "once": [4, 40000.0, 60.0, 0, 60.0], "gone": [5, 99000.0, 10.0, 0, 10.0],
                    "gather": [6, 70000.0, 30.0, 0, 30.0]}                                        # standing work is no route judged on its pay
        self.assertEqual([rid for _f, rid, _r in hive.scale(routes, by_route)], ["mine"])
        self.assertEqual([hive.work_of(routes[rid]) for rid in ("mine", "gather")], ["mining", "standing work (trains, gathers)"])
        routes["drain"] = {"id": "drain", "kind": "circuit", "requires": {"stored": {"at": "c", "item": "ice", "min": 60}}, "stops": [{"at": "a:b:c"}]}
        by_route["drain"] = [3, 90000.0, 20.0, 0, 20.0]                                               # it sells a load mined earlier: no scale for work
        self.assertEqual([rid for _f, rid, _r in hive.scale(routes, by_route)], ["mine"])

    def test_the_history_store_answers_from_its_read_copy(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, []), 1)              # no copy yet: said, not failed
        self.assertIn("no read copy", said.getvalue())
        runs = [{"route": "ice", "pilot": "miner-1", "started": stamp(7200), "minutes": 30, "delta": 4000, "credits_before": 1000, "credits_after": 5000, "one_time": 1000},
                {"route": "ice", "pilot": "miner-2", "started": stamp(7000), "minutes": 30, "delta": 1000, "credits_before": 1000, "credits_after": 2000},
                {"route": "ice", "pilot": "miner-3", "started": stamp(6900), "minutes": 30, "delta": 0, "credits_before": 0, "credits_after": 0, "notes": ["wallet not read"]}]
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in runs))
        (self.data / "market" / "history.jsonl").write_text("".join(json.dumps(m) + "\n" for m in (
            {"t": stamp(7200), "base": "hub", "item": "water_ice", "bid": 30, "bid_qty": 9, "ask": 0, "ask_qty": 0},
            {"t": stamp(7100), "base": "hub", "item": "water_ice", "bid": 38, "bid_qty": 9, "ask": 44, "ask_qty": 2})))
        self.hive.history.one_pass(str(self.data), now=now)
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, []), 0)
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, ["price", "water_ice"]), 0)
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, ["price", "no_such_item"]), 0)
        text = said.getvalue()
        ice = next(line.split() for line in text.splitlines() if line.strip().startswith("ice "))
        self.assertEqual(ice, ["ice", "3", "1.0", "4,000", "4,000", "1,000"])                 # by hand: (4000 - 1000) + 1000 over the 60 minutes that read a wallet
        hub = next(line.split() for line in text.splitlines() if line.strip().startswith("hub "))
        self.assertEqual(hub[:7], ["hub", "1" if stamp(7200)[:13] == stamp(7100)[:13] else "2", "30", "38", "44", "44", "2"])
        self.assertIn("no price move of `no_such_item`", text)

    def test_what_a_bid_regains_is_one_figure_for_the_tables_and_for_the_plans(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        (self.data / "market" / "history.jsonl").write_text("".join(
            json.dumps({"t": stamp(ago), "base": "hub", "item": "water_ice", "bid": 38, "bid_qty": units, "ask": 0, "ask_qty": 0}) + "\n"
            for ago, units in ((7200, 1000), (3600, 600), (0, 900))))
        bids, fields, herds = self.hive.rates(str(self.data))
        added, taken, hours = bids[("hub", "water_ice")]
        self.assertEqual((round(added), round(taken), round(hours, 1)), (150, 200, 2.0))          # 300 came back and 400 were taken in two hours
        self.assertEqual((fields, herds), ({}, {}))

    def test_the_briefing_is_one_answer_and_says_what_it_could_not_read(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.hive.show_briefing(str(FLEET.parent), str(self.data), time.time(), "Zero", 4)
        text = out.getvalue()
        for part in ("=== THE ORDERS IN FORCE", "=== REQUESTS NOT CLOSED, ADDRESSED TO Zero", "=== THE FLEET'S MONEY", "=== MY STANDING FLEET", "STANDING FLEET | Zero, role miner",
                     "=== THE FILL GATE (no ship is idle)", "PASS: no ship of miner waits"):
            self.assertIn(part, text)

    def test_a_question_without_readings_says_so_instead_of_failing(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(self.hive.show_ship(str(self.data), time.time(), "nobody-1"), 1)
            self.assertEqual(self.hive.show_base(str(FLEET.parent), str(self.data), time.time(), "outpost"), 1)
            self.assertEqual(self.hive.show_history(str(self.data), time.time(), 12), 0)
        self.assertIn("no ship `nobody-1`", out.getvalue())
        self.assertIn("no catalog in the data folder", out.getvalue())
        self.assertIn("fewer than two hourly samples", out.getvalue())


if __name__ == "__main__":
    unittest.main()
