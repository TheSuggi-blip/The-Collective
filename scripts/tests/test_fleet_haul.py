#!/usr/bin/env python3
import importlib.util
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


haul = _load("haul_test_mod", ROOT / "game" / "fleet" / "haul.py")


class HaulEngineTests(unittest.TestCase):
    def setUp(self):
        self.base_map = {
            "base_a": ("sys_a", "p_a", "base_a", "voidborn"),
            "base_b": ("sys_b", "p_b", "base_b", "voidborn"),
            "base_w": ("sys_w", "p_w", "base_w", ""),
        }
        self.lanes = {"sys_a": ["sys_b", "sys_w"], "sys_b": ["sys_a"], "sys_w": ["sys_a"]}

    def test_freight_picker_enforces_policed_collateral_hazmat_and_partner_priority(self):
        entries = [
            {"id": "lawless_high", "origin_base_id": "base_a", "destination_base_id": "base_w", "base_reward": 9000, "collateral": 0, "package_id": "p1"},
            {"id": "hazmat_job", "origin_base_id": "base_a", "destination_base_id": "base_b", "base_reward": 5000, "collateral": 0, "requires_hazmat": True, "package_id": "p2"},
            {"id": "pub_job", "origin_base_id": "base_a", "destination_base_id": "base_b", "base_reward": 2000, "collateral": 1000, "package_id": "p3"},
            {"id": "hexc_job", "origin_base_id": "base_a", "destination_base_id": "base_b", "base_reward": 1800, "collateral": 1000, "shipper_tag": "HEXC", "package_id": "p4"},
        ]
        # Neutral partner HEXC (1800 * 1.25 = 2250) beats generic pub_job (2000); lawless & hazmat rejected
        pick = haul.pick_freight_contract(entries, "sys_a", self.base_map, self.lanes, haul.DEFAULT_POLICY, 20000, False, {"HEXC": "Hex"}, set())
        self.assertIsNotNone(pick)
        self.assertEqual(pick["cid"], "hexc_job")
        self.assertEqual(pick["partner"], "HEXC")
        # Claiming hexc_job makes next hauler pick pub_job
        pick2 = haul.pick_freight_contract(entries, "sys_a", self.base_map, self.lanes, haul.DEFAULT_POLICY, 20000, False, {"HEXC": "Hex"}, {"freight:hexc_job"})
        self.assertEqual(pick2["cid"], "pub_job")

    def test_arbitrage_picker_and_atomic_claims(self):
        now_t = time.time()
        books = [
            {"base": "base_a", "item": "durasteel_plate", "ask": 100, "ask_qty": 50, "bid": 80, "bid_qty": 10, "t": now_t - 60},
            {"base": "base_b", "item": "durasteel_plate", "ask": 180, "ask_qty": 10, "bid": 150, "bid_qty": 40, "t": now_t - 60},
            {"base": "base_w", "item": "durasteel_plate", "ask": 500, "ask_qty": 10, "bid": 400, "bid_qty": 40, "t": now_t - 60},
        ]
        job = haul.pick_arbitrage_job(books, self.base_map, self.lanes, "sys_a", 30, 10000, haul.DEFAULT_POLICY, set(), now_t=now_t)
        self.assertIsNotNone(job)
        self.assertEqual(job["item"], "durasteel_plate")
        self.assertEqual(job["buy_loc"][2], "base_a")
        self.assertEqual(job["sell_loc"][2], "base_b")
        self.assertEqual(job["qty"], 30)
        # Atomic claim prevents duplicate assignment
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(haul.claim_job(tmp, "hauler-1", job["job_key"], now_t=now_t))
            self.assertFalse(haul.claim_job(tmp, "hauler-2", job["job_key"], now_t=now_t))
            haul.release_job(tmp, "hauler-1")
            self.assertTrue(haul.claim_job(tmp, "hauler-2", job["job_key"], now_t=now_t))


    def test_sell_bid_claim_fresh_books_and_freight_hold_cap(self):
        now_t = time.time()
        entries = [{"id": "c1", "origin_base_id": "base_a", "destination_base_id": "base_b", "base_reward": 2000, "collateral": 1000, "volume": 100}]
        self.assertIsNone(haul.pick_freight_contract(entries, "sys_a", self.base_map, self.lanes, haul.DEFAULT_POLICY, 20000, False, {}, set(), hold_cap=65))
        self.assertIsNotNone(haul.pick_freight_contract(entries, "sys_a", self.base_map, self.lanes, haul.DEFAULT_POLICY, 20000, False, {}, set(), hold_cap=120))
        stale = [
            {"base": "base_a", "item": "control_node", "ask": 100, "ask_qty": 30, "bid": 80, "bid_qty": 10, "t": now_t - 3600},
            {"base": "base_b", "item": "control_node", "ask": 200, "ask_qty": 10, "bid": 160, "bid_qty": 30, "t": now_t - 60},
        ]
        self.assertIsNone(haul.pick_arbitrage_job(stale, self.base_map, self.lanes, "sys_a", 30, 10000, haul.DEFAULT_POLICY, set(), now_t=now_t))
        fresh = [
            {"base": "base_a", "item": "control_node", "ask": 100, "ask_qty": 30, "bid": 80, "bid_qty": 10, "t": now_t - 60},
            {"base": "base_b", "item": "control_node", "ask": 200, "ask_qty": 10, "bid": 160, "bid_qty": 30, "t": now_t - 60},
        ]
        j = haul.pick_arbitrage_job(fresh, self.base_map, self.lanes, "sys_a", 30, 10000, haul.DEFAULT_POLICY, set(), now_t=now_t)
        self.assertEqual(j["job_key"], "arb-bid:base_b:control_node")
        self.assertIsNone(haul.pick_arbitrage_job(fresh, self.base_map, self.lanes, "sys_a", 30, 10000, haul.DEFAULT_POLICY, {"arb-bid:base_b:control_node"}, now_t=now_t))

    def test_global_optimal_assignment_gives_spread_to_closest_biggest_hauler(self):
        now_t = time.time()
        books = [
            {"base": "base_a", "item": "lead_shielding", "ask": 100, "ask_qty": 100, "bid": 80, "bid_qty": 10, "t": now_t - 60},
            {"base": "base_b", "item": "lead_shielding", "ask": 300, "ask_qty": 10, "bid": 250, "bid_qty": 100, "t": now_t - 60},
        ]
        peers = [
            {"pilot": "hauler-far", "system": "sys_b", "hold_cap": 65, "avail_cash": 20000, "has_hazmat": False},
            {"pilot": "hauler-near", "system": "sys_a", "hold_cap": 480, "avail_cash": 30000, "has_hazmat": False},
        ]
        assigned = haul.assign_optimal_arbitrage(books, self.base_map, self.lanes, peers, haul.DEFAULT_POLICY, set(), now_t=now_t)
        self.assertIn("hauler-near", assigned)
        self.assertNotIn("hauler-far", assigned)
        self.assertEqual(assigned["hauler-near"]["job_key"], "arb-bid:base_b:lead_shielding")
        self.assertGreater(assigned["hauler-near"]["qty"], 65)


    def test_internal_supply_reads_live_need_status_and_supply_status(self):
        """_pick_internal_supply reads short items from live need_status and supply_status tables."""
        import sqlite3, tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            (data / "store").mkdir(parents=True, exist_ok=True)
            (data / "stock").mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE need_status (id TEXT, short_items TEXT);
                CREATE TABLE supply_status (item TEXT, stock INTEGER, keep INTEGER);
                INSERT INTO need_status VALUES ('atria', 'foil_scale 500, alloy_scale 200');
                INSERT INTO supply_status VALUES ('iron_ore', 45000, 60000), ('copper_ore', 80000, 50000);
            """)
            con.commit()
            con.close()
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {
                    "hauler-1": {
                        "outer_base": {"iron_ore": 120, "copper_ore": 500, "foil_scale": 50},
                    }
                }
            }), encoding="ascii")
            base_map = {
                "outer_base": ("sys_out", "poi_out", "outer_base", True, "voidborn"),
                "node_beta_industrial_station": ("node_beta", "poi_nb", "node_beta_industrial_station", True, "voidborn"),
            }
            lanes = {"sys_out": {"node_beta"}, "node_beta": {"sys_out"}}
            pol = {"policed_only": True, "home_bases": ["node_beta_industrial_station"], "max_jumps_pickup": 10, "max_jumps_delivery": 10}
            job = haul._pick_internal_supply(str(data), "hauler-1", base_map, lanes, "sys_out", 100, pol, set())
            self.assertIsNotNone(job)
            self.assertIn(job["item"], ("iron_ore", "foil_scale"))
            self.assertEqual(job["dest"][2], "node_beta_industrial_station")

if __name__ == "__main__":
    unittest.main()
