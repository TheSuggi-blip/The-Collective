#!/usr/bin/env python3
import importlib.util
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bursar = _load("bursar_test_mod", ROOT / "game" / "fleet" / "bursar.py")


class BursarEngineTests(unittest.TestCase):
    def _make_world(self, tmp):
        root = Path(tmp)
        data = root / "data"
        (data / "store").mkdir(parents=True, exist_ok=True)
        (data / "fleet" / "orders").mkdir(parents=True, exist_ok=True)
        (root / "game" / "routes").mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(str(data / "store" / "read.db"))
        con.executescript("""
            CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, base TEXT, t INT);
            CREATE TABLE systems (id TEXT, name TEXT, empire TEXT);
            CREATE TABLE books (base TEXT, system TEXT, item TEXT, bid REAL, bid_qty REAL, ask REAL, ask_qty REAL, t INT);
            INSERT INTO systems VALUES ('sys_a', 'Alpha', 'voidborn');
            INSERT INTO systems VALUES ('sys_b', 'Beta', 'voidborn');
            INSERT INTO systems VALUES ('sys_c', 'Wild', '');
            INSERT INTO places VALUES ('sys_a', 'p_a', 'station', 'Base A', 'base_a', 100);
            INSERT INTO places VALUES ('sys_b', 'p_b', 'station', 'Base B', 'base_b', 100);
            INSERT INTO places VALUES ('sys_c', 'p_c', 'station', 'Wild Base', 'base_c', 100);
            INSERT INTO books VALUES ('base_a', 'sys_a', 'iron_ore', 10, 5000, 15, 5000, 100);
            INSERT INTO books VALUES ('base_b', 'sys_b', 'gold_ore', 50, 2000, 70, 2000, 100);
            INSERT INTO books VALUES ('base_c', 'sys_c', 'gold_ore', 90, 9000, 100, 9000, 100);
        """)
        con.close()
        return root, data

    def test_atomic_station_claim_enforces_one_per_station_and_policed_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = self._make_world(tmp)
            now_t = time.time()
            pol = dict(bursar.DEFAULT_POLICY, max_per_station=1, policed_only=True)
            c1 = bursar.claim_station(data, root, "trader-1", {"empire": "voidborn", "base": "base_a"}, pol, now_t=now_t)
            self.assertIsNotNone(c1)
            self.assertEqual(c1["base"], "base_a")
            c2 = bursar.claim_station(data, root, "trader-2", {"empire": "voidborn"}, pol, now_t=now_t)
            self.assertIsNotNone(c2)
            self.assertEqual(c2["base"], "base_b")
            c3 = bursar.claim_station(data, root, "trader-3", {"empire": "voidborn"}, pol, now_t=now_t)
            self.assertIsNone(c3)
            bursar.release_claim(data, "trader-1")
            c4 = bursar.claim_station(data, root, "trader-3", {"empire": "voidborn"}, pol, now_t=now_t)
            self.assertEqual(c4["base"], "base_a")

    def test_plan_bursar_actions_respects_reserves_hits_strong_bids_and_places_buy_walls(self):
        book = {
            "foil_scale": {"best_buy": 40, "best_buy_qty": 20, "best_sell": 80, "best_sell_qty": 100},
            "junk_rock": {"best_buy": 90, "best_buy_qty": 10, "best_sell": 110, "best_sell_qty": 50},
            "surplus_widget": {"best_buy": 20, "best_buy_qty": 5, "best_sell": 120, "best_sell_qty": 50},
        }
        stored = {"foil_scale": 50, "junk_rock": 8, "surplus_widget": 12}
        open_needs = {"foil_scale": 100}
        reserved = {"foil_scale"}
        catalog_vals = {"foil_scale": 50, "junk_rock": 100, "surplus_widget": 100}
        acts = bursar.plan_bursar_actions(book, stored, [], open_needs, reserved, catalog_vals, 80000, bursar.DEFAULT_POLICY)
        self.assertFalse(any(a[0].startswith("sell_") and a[1] == "foil_scale" for a in acts))
        buys = [a for a in acts if a[0] == "buy_create" and a[1] == "foil_scale"]
        self.assertEqual(len(buys), 1)
        self.assertEqual(buys[0][3], 41)
        self.assertIn(("sell_bid", "junk_rock", 8, 90), acts)
        self.assertIn(("sell_create", "surplus_widget", 12, 119), acts)


    def test_bursar_never_outbids_or_undercuts_its_own_standing_orders(self):
        book = {
            "foil_scale": {"best_buy": 41, "best_buy_qty": 200, "best_sell": 80, "best_sell_qty": 100},
            "surplus_widget": {"best_buy": 20, "best_buy_qty": 5, "best_sell": 119, "best_sell_qty": 12},
        }
        own_orders = [
            {"order_id": "b1", "item_id": "foil_scale", "side": "buy", "remaining": 200, "price_each": 41},
            {"order_id": "s1", "item_id": "surplus_widget", "side": "sell", "remaining": 12, "price_each": 119},
        ]
        acts = bursar.plan_bursar_actions(
            book, {"surplus_widget": 12}, own_orders, {"foil_scale": 200}, {"foil_scale"},
            {"foil_scale": 50, "surplus_widget": 100}, 80000, bursar.DEFAULT_POLICY,
        )
        # Already best bid (41) and best ask (119) -> zero modify/create calls!
        self.assertEqual(acts, [])


if __name__ == "__main__":
    unittest.main()
