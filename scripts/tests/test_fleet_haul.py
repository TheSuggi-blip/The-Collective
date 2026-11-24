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


if __name__ == "__main__":
    unittest.main()
