import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import mine
import mine_net


class MineNetTests(unittest.TestCase):
    def _world(self):
        return {
            "adj": {"sys_a": {"sys_b", "sys_c"}, "sys_b": {"sys_a"}, "sys_c": {"sys_a"}},
            "systems": {
                "sys_a": {"empire": "voidborn", "stronghold": False},
                "sys_b": {"empire": "voidborn", "stronghold": False},
                "sys_c": {"empire": "", "stronghold": False},
            },
            "stations_by_sys": {
                "sys_a": [("sys_a", "st_a", "base_a")],
                "sys_b": [("sys_b", "st_b", "base_b")],
            },
            "fields": [
                {"system": "sys_a", "poi": "belt_iron", "resource": "iron_ore", "remaining": 90000, "max_remaining": 100000, "richness": 50, "t": 1},
                {"system": "sys_b", "poi": "belt_carbon", "resource": "carbon_ore", "remaining": 8000, "max_remaining": 20000, "richness": 40, "t": 1},
                {"system": "sys_a", "poi": "belt_ice", "resource": "nitrogen_ice", "remaining": 20000, "max_remaining": 50000, "richness": 40, "t": 1},
                {"system": "sys_b", "poi": "belt_dry", "resource": "silicon_ore", "remaining": 1000, "max_remaining": 10000, "richness": 30, "t": 1},
                {"system": "sys_c", "poi": "belt_lawless", "resource": "silicon_ore", "remaining": 9000, "max_remaining": 10000, "richness": 60, "t": 1},
            ],
            "pirates": set(),
            "item_vals": {"iron_ore": 4.0, "carbon_ore": 12.0, "nitrogen_ice": 6.0, "silicon_ore": 20.0},
            "shortages": {"carbon_ore": 5000, "silicon_ore": 2000},
            "full_items": {"iron_ore"},
        }

    def test_live_floor_breach_detection(self):
        res = [
            {"resource_id": "carbon_ore", "remaining": 2900, "max_remaining": 20000},
            {"resource_id": "iron_ore", "remaining": 9000, "max_remaining": 20000},
        ]
        hit = mine.check_floor_breached(res, min_left_pct=15.0, floor_resource="carbon_ore")
        self.assertIsNotNone(hit)
        self.assertEqual(hit[0], "carbon_ore")
        self.assertIsNone(mine.check_floor_breached(res, min_left_pct=15.0, floor_resource="iron_ore"))

    def test_tool_matching_deficit_priority_and_policed_gate(self):
        pol = dict(mine_net.DEFAULT_POLICY, policed_only=True, allow_lawless_for_deficit=False)
        w = self._world()
        ore_pilot = {"name": "miner-1", "system": "sys_a", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
        cands = mine_net.score_belt_candidates(ore_pilot, w, pol, {}, {})
        self.assertEqual(cands[0]["resource"], "carbon_ore")
        self.assertEqual(cands[0]["tier"], "deficit")
        self.assertNotIn("sys_b:belt_dry", [c["belt_key"] for c in cands])
        self.assertNotIn("sys_c:belt_lawless", [c["belt_key"] for c in cands])
        ice_pilot = {"name": "miner-2", "system": "sys_a", "tier": 0, "modules": [{"type": "ice_harvester_i"}]}
        ic = mine_net.score_belt_candidates(ice_pilot, w, pol, {}, {})
        self.assertEqual([c["resource"] for c in ic], ["nitrogen_ice"])
        t1_pilot = {"name": "miner-3", "system": "sys_a", "tier": 1, "modules": [{"type": "mining_laser_iii"}]}
        t1c = mine_net.score_belt_candidates(t1_pilot, w, pol, {}, {})
        self.assertIn("sys_c:belt_lawless", [c["belt_key"] for c in t1c])

    def test_atomic_claims_adaptive_cap_and_floor_cooldown(self):
        pol = dict(mine_net.DEFAULT_POLICY, max_per_belt=3, units_per_ship_run=250)
        self.assertEqual(mine_net.adaptive_belt_cap(1800, 10000, pol), 1)
        self.assertEqual(mine_net.adaptive_belt_cap(5000, 10000, pol), 3)
        with tempfile.TemporaryDirectory() as tmp:
            now_t = time.time()
            self.assertTrue(mine_net.claim_belt_atomic(tmp, "miner-1", "sys_b:belt_carbon", 1, pol, now_t=now_t))
            self.assertFalse(mine_net.claim_belt_atomic(tmp, "miner-2", "sys_b:belt_carbon", 1, pol, now_t=now_t))
            mine_net.release_belt_claim(tmp, "miner-1", cooldown_belt="sys_b:belt_carbon", cooldown_minutes=90, policy=pol, now_t=now_t)
            self.assertFalse(mine_net.claim_belt_atomic(tmp, "miner-2", "sys_b:belt_carbon", 1, pol, now_t=now_t + 60))
            self.assertTrue(mine_net.claim_belt_atomic(tmp, "miner-2", "sys_b:belt_carbon", 1, pol, now_t=now_t + 91 * 60))

    def test_global_optimal_assignment(self):
        pol = dict(mine_net.DEFAULT_POLICY, policed_only=True, allow_lawless_for_deficit=False)
        w = self._world()
        p1 = {"name": "miner-1", "system": "sys_a", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
        p2 = {"name": "miner-2", "system": "sys_b", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
        assigned = mine_net.assign_optimal_mines([p1, p2], w, pol, {}, {})
        self.assertEqual(assigned["miner-2"]["belt_key"], "sys_b:belt_carbon")


if __name__ == "__main__":
    unittest.main()
