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



    def test_uncapped_escrow_uses_full_free_cash_above_min_keep(self):
        book = {"outpost_kit": {"best_buy": 150000, "best_buy_qty": 1, "best_sell": 220000, "best_sell_qty": 1}}
        pol = json.loads(json.dumps(bursar.DEFAULT_POLICY))
        pol["min_cash_keep"] = 20000
        pol["buy"]["max_escrow_per_station"] = 0
        acts = bursar.plan_bursar_actions(book, {}, [], {"outpost_kit": 1}, set(), {"outpost_kit": 180000}, 200000, pol)
        buys = [a for a in acts if a[0] == "buy_create" and a[1] == "outpost_kit"]
        self.assertEqual(len(buys), 1)
        self.assertEqual(buys[0][2], 1)
        self.assertEqual(buys[0][3], 150001)

    def test_buy_lane_off_unwinds_own_buy_orders_and_keeps_sells(self):
        book = {"cobalt_ink": {"best_buy": 143, "best_buy_qty": 200, "best_sell": 170, "best_sell_qty": 50}}
        own_orders = [
            {"order_id": "b1", "item_id": "cobalt_ink", "side": "buy", "remaining": 200, "price_each": 143},
            {"order_id": "b2", "item_id": "silicon_ore", "side": "buy", "remaining": 0, "price_each": 6},
            {"order_id": "s1", "item_id": "surplus_widget", "side": "sell", "remaining": 12, "price_each": 119},
        ]
        pol = json.loads(json.dumps(bursar.DEFAULT_POLICY))
        pol["buy"]["enabled"] = False
        acts = bursar.plan_bursar_actions(book, {}, own_orders, {"cobalt_ink": 276}, {"cobalt_ink"}, {}, 80000, pol)
        self.assertEqual([a for a in acts if a[0].startswith("buy_")], [("buy_cancel", "cobalt_ink", "b1")])
        pol["buy"]["unwind_when_off"] = False
        acts = bursar.plan_bursar_actions(book, {}, own_orders, {"cobalt_ink": 276}, {"cobalt_ink"}, {}, 80000, pol)
        self.assertEqual([a for a in acts if a[0].startswith("buy_")], [])

    def test_order_stations_read_from_the_view_orders_hint(self):
        hint = ("You must be docked or provide a station_id to view your orders.\n\n2 buy orders and 2 sell orders on the "
                "market at crimson_war_citadel, node_beta_industrial_station (32,961 credits and 301 items in escrow)")
        self.assertEqual(bursar.order_stations(hint), (2, ["crimson_war_citadel", "node_beta_industrial_station"]))
        self.assertEqual(bursar.order_stations("0 buy orders and 3 sell orders on the market at base_a (0 credits and 7 items in escrow)"),
                         (0, ["base_a"]))
        self.assertEqual(bursar.order_stations("No personal orders."), (0, []))

    def test_unwind_base_wins_the_claim_without_taking_another_pilots_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = self._make_world(tmp)
            now_t = time.time()
            pol = dict(bursar.DEFAULT_POLICY, max_per_station=1, policed_only=True)
            c1 = bursar.claim_station(data, root, "trader-1", {"empire": "voidborn", "docked": "base_a"}, pol, now_t=now_t)
            self.assertEqual(c1["base"], "base_a")
            c2 = bursar.claim_station(data, root, "trader-2", {"empire": "voidborn", "docked": "base_b"}, pol,
                                      now_t=now_t, unwind_bases={"base_a"})
            self.assertEqual(c2["base"], "base_a")
            self.assertTrue(c2.get("unwind"))
            claims = json.loads((data / "fleet" / "bursar_claims.json").read_text())
            self.assertEqual(claims["base_a"]["pilot"], "trader-1")
            self.assertNotIn("base_b", claims)
            # a lawless unwind base stays out while policed_only holds
            c3 = bursar.claim_station(data, root, "trader-3", {"empire": "voidborn"}, pol, now_t=now_t, unwind_bases={"base_c"})
            self.assertEqual(c3["base"], "base_b")
            self.assertFalse(c3.get("unwind"))


    def test_fleet_wide_buy_cap_prevents_duplication(self):
        book = {"cobalt_ink": {"best_buy": 100, "best_buy_qty": 20, "best_sell": 160, "best_sell_qty": 50}}
        pol = json.loads(json.dumps(bursar.DEFAULT_POLICY))
        pol["buy"]["enabled"] = True
        pol["buy"]["max_escrow_per_station"] = 0
        pol["buy"]["max_units_per_order"] = 200
        with tempfile.TemporaryDirectory() as tmp:
            bursar.sync_fleet_buys(tmp, "trader-1", "base_a", [{"item_id": "cobalt_ink", "side": "buy", "remaining": 200}])
            other2 = bursar.sync_fleet_buys(tmp, "trader-2", "base_b", [])
            self.assertEqual(other2.get("cobalt_ink"), 200)
            acts2 = bursar.plan_bursar_actions(book, {}, [], {"cobalt_ink": 276}, set(), {"cobalt_ink": 100}, 200000, pol, fleet_open_buys=other2)
            self.assertEqual([(a[0], a[1], a[2]) for a in acts2 if a[0] == "buy_create"], [("buy_create", "cobalt_ink", 76)])
            bursar.sync_fleet_buys(tmp, "trader-2", "base_b", [{"item_id": "cobalt_ink", "side": "buy", "remaining": 76}])
            other3 = bursar.sync_fleet_buys(tmp, "trader-3", "base_c", [])
            acts3 = bursar.plan_bursar_actions(book, {}, [], {"cobalt_ink": 276}, set(), {"cobalt_ink": 100}, 200000, pol, fleet_open_buys=other3)
            self.assertEqual([a for a in acts3 if a[0] == "buy_create"], [])
            acts4 = bursar.plan_bursar_actions(book, {}, [{"order_id": "old1", "item_id": "closed_item", "side": "buy", "remaining": 50, "price_each": 50}], {"cobalt_ink": 276}, set(), {}, 200000, pol, fleet_open_buys=other3)
            self.assertIn(("buy_cancel", "closed_item", "old1"), acts4)

if __name__ == "__main__":
    unittest.main()
