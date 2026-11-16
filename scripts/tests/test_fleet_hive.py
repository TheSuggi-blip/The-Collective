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
