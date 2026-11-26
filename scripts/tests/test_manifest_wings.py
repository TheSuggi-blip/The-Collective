"""Unit tests for manifest_wings, wing-gating in dispatch, mine_net 5-wing scoring, and 1A Task Forces."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import manifest_wings as mw
import mine_net as mn
import hunt_net as hn


class ManifestWingSpecializationTests(unittest.TestCase):
    def test_task_forces_exact_manifest_counts(self):
        tfs = mw.task_forces(ROOT)
        self.assertEqual(tfs["tf-prime"]["size"], 10)
        self.assertEqual(tfs["tf-alpha"]["size"], 8)
        self.assertEqual(tfs["tf-beta"]["size"], 8)
        self.assertIn("Prime Directive", tfs["tf-prime"]["command_ships"])

    def test_route_wing_gates_separate_cohorts_cleanly(self):
        def check(pilot, rid):
            r = json.loads((ROOT / "game" / "routes" / f"{rid}.json").read_text(encoding="utf-8"))
            req = r.get("requires") or {}
            return mw.matches_wing(
                pilot,
                wing_prefix=req.get("wing_prefix"),
                wing_contains=req.get("wing_contains"),
                exclude_wing_prefix=req.get("exclude_wing_prefix"),
                repo_root=ROOT,
            )[0]

        self.assertTrue(check("Prime Directive", "hunt-network-packs"))
        self.assertFalse(check("ROU Ashen Blade", "hunt-network-packs"))
        self.assertTrue(check("MCV Bukhara", "haul-network-trade"))
        self.assertFalse(check("MCV Bukhara", "bursar-network"))
        self.assertTrue(check("MCV Alexandria", "bursar-network"))
        self.assertFalse(check("MCV Alexandria", "haul-network-trade"))
        self.assertFalse(check("MCV Alexandria", "craft-network"))
        self.assertTrue(check("IFV Alembic", "bursar-network"))
        self.assertTrue(check("IFV Alembic", "craft-network"))
        self.assertTrue(check("VSV Azimuth", "census-deep-core"))
        self.assertFalse(check("VSV Night Whisper", "census-deep-core"))
        self.assertTrue(check("VSV Night Whisper", "census-far-1"))
        self.assertFalse(check("VSV Azimuth", "census-far-1"))

    def test_mine_net_five_wing_multipliers(self):
        self.assertGreater(mn._wing_mine_multiplier("3A. Ore -- Precision", "phase_crystal", {"ore"}), 2.0)
        self.assertGreater(mn._wing_mine_multiplier("3B. Ore -- Bulk", "iron_ore", {"ore"}), 2.0)
        self.assertGreater(mn._wing_mine_multiplier("3C. Deep-Core & Rad", "uranium_ore", {"ore"}), 3.0)
        self.assertGreater(mn._wing_mine_multiplier("3D. Gas Harvesters", "plasma_gas", {"gas"}), 3.0)
        self.assertEqual(mn._wing_mine_multiplier("3D. Gas Harvesters", "iron_ore", {"ore"}), 1.0)
        self.assertGreater(mn._wing_mine_multiplier("3E. Ice Harvesters", "methane_ice", {"ice"}), 3.0)

    def test_hunt_net_t0_t1_pack_power_and_standing_squads(self):
        hp = hn.load_policy(str(ROOT / "game" / "hunt-policy.json"))
        hpp = hn.load_policy(str(ROOT / "game" / "hunt-policy-packs.json"))
        self.assertLessEqual(hp["packs"]["min_member_power"], 380.0)
        self.assertLessEqual(hpp["packs"]["min_member_power"], 380.0)
        self.assertTrue(hpp["solo"]["enabled"])
        sq = hn.standing_squad_for_pilot("/srv/collective/data", "Prime Directive", hpp)
        self.assertIsNotNone(sq)
        self.assertEqual(sq["squad_id"], "tf-prime")
        self.assertEqual(sq["size"], 10)


if __name__ == "__main__":
    unittest.main()
