#!/usr/bin/env python3
"""Unit tests for game/fleet/shipping.py (spacemolt_shipping freight board reader)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import shipping  # noqa: E402


class ShippingHelperTests(unittest.TestCase):
    def test_pick_docked_pilot_prefers_docked_hauler_then_prime_directive(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "fleet").mkdir(parents=True)
            fleet = {
                "ships": [
                    {"name": "Prime Directive", "status": "connected", "docked": True},
                    {"name": "hauler-7", "status": "connected", "docked": False},
                    {"name": "hauler-12", "status": "connected", "docked": True},
                    {"name": "trader-3", "status": "connected", "docked": True},
                ]
            }
            (data / "fleet" / "fleet.json").write_text(json.dumps(fleet), encoding="ascii")
            self.assertEqual(shipping.pick_docked_pilot(str(data)), "hauler-12")
            self.assertEqual(shipping.pick_docked_pilot(str(data), "Prime Directive"), "Prime Directive")

    def test_format_shipment_rows_prioritizes_neutral_partners_then_reward(self):
        items = [
            {"id": "c-1", "base_reward": 50000, "shipper_name": "RandomGuy", "shipper_faction_tag": "RAND", "origin_base_name": "Sol", "destination_base_name": "Alpha", "distance": 4, "eligible": True},
            {"id": "c-2", "base_reward": 20000, "shipper_name": "ILC Comptroller", "shipper_faction_tag": "IRLC", "origin_base_name": "Ironlight", "destination_base_name": "Node Beta", "distance": 6, "eligible": True},
            {"id": "c-3", "base_reward": 80000, "shipper_name": "Other", "shipper_faction_tag": "XYZ", "origin_base_name": "Krynn", "destination_base_name": "Haven", "distance": 9, "eligible": False},
        ]
        rows = shipping.format_shipment_rows(items, {"HEXC", "IRLC"}, limit=10)
        self.assertEqual([r["id"] for r in rows], ["c-2", "c-3", "c-1"])
        self.assertTrue(rows[0]["partner"])
        self.assertFalse(rows[1]["partner"])


if __name__ == "__main__":
    unittest.main()
