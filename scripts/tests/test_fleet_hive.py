"""game/fleet/hive.py on a disposable data folder: what the stations bid in all, a field's change between two readings, a route's runs in a window. No engine, no network."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import time
import unittest


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
