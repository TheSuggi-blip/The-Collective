#!/usr/bin/env python3
"""Unit tests for disabled-by-default salvage_net.py (6C Combat Salvage Tenders)."""
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import salvage_net  # noqa: E402
import routes  # noqa: E402
import workclass  # noqa: E402


class SalvageNetTests(unittest.TestCase):
    def test_repo_policy_and_route_disabled_by_default(self):
        pol = salvage_net.read_policy(ROOT / "game" / "salvage-policy.json")
        self.assertFalse(salvage_net.is_enabled(pol))
        route = json.loads((ROOT / "game" / "routes" / "salvage-network.json").read_text(encoding="utf-8"))
        self.assertEqual(route["kind"], "salvage_net")
        self.assertEqual(route.get("status"), "off")
        self.assertEqual(workclass.work_class(route), "haul")
        self.assertTrue(routes.standing(route))

    def test_tool_detection_and_disabled_gate(self):
        pilot_state = {
            "system": "sol",
            "ship": {"fuel": 90, "max_fuel": 100, "modules": ["outer_rim_salvage_array", "advanced_tow_rig"]},
        }
        tools = salvage_net.pilot_salvage_tools(pilot_state)
        self.assertIn("outer_rim_salvage_array", tools["salvage"])
        self.assertIn("advanced_tow_rig", tools["tow"])

        pol_off = salvage_net.read_policy(ROOT / "game" / "salvage-policy.json")
        targets = [{"system": "sol", "poi": "belt_1", "activity": 3, "last_at": time.time(), "policed": True}]
        self.assertIsNone(salvage_net.pick_salvage_target("LSV Tender", pilot_state, targets, {}, {"sol": []}, pol_off))

        pol_on = dict(pol_off, enabled=True)
        picked = salvage_net.pick_salvage_target("LSV Tender", pilot_state, targets, {}, {"sol": []}, pol_on)
        self.assertIsNotNone(picked)
        self.assertEqual(picked["system"], "sol")

    def test_policed_filter_and_atomic_claim_cap(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "fleet").mkdir(parents=True)
            now = time.time()
            (data / "fleet" / "hunt_claims.json").write_text(json.dumps({
                "safe_sys:belt_a": {"ROU One": {"at": now - 60}},
            }), encoding="ascii")
            pol = dict(salvage_net.read_policy(ROOT / "game" / "salvage-policy.json"), enabled=True, max_ships_per_system=1)
            self.assertTrue(salvage_net.claim_system(data, "safe_sys", "LSV Alpha", pol, now=now))
            self.assertFalse(salvage_net.claim_system(data, "safe_sys", "LSV Beta", pol, now=now))
            salvage_net.release_claim(data, "safe_sys", "LSV Alpha")
            self.assertTrue(salvage_net.claim_system(data, "safe_sys", "LSV Beta", pol, now=now))

            # Unpoliced target rejected without cloak when policed_only=True
            p_state = {"system": "safe_sys", "ship": {"fuel": 90, "max_fuel": 100, "modules": ["salvage_module"]}}
            lawless = [{"system": "wild_sys", "poi": "p1", "activity": 5, "last_at": now, "policed": False}]
            self.assertIsNone(salvage_net.pick_salvage_target("LSV Beta", p_state, lawless, {}, {"safe_sys": ["wild_sys"], "wild_sys": ["safe_sys"]}, pol, now=now))

    def test_cli_exits_cleanly_when_disabled(self):
        rc = salvage_net.main(["LSV Test", "--policy", str(ROOT / "game" / "salvage-policy.json")])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
