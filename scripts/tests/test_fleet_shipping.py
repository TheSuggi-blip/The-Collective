import unittest
from unittest import mock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "game" / "fleet"))
import shipping


class TestFleetShipping(unittest.TestCase):
    def test_format_list_prioritizes_neutral_partner(self):
        body = {
            "structuredContent": {
                "shipments": [
                    {"id": "sh-npc-1", "origin": "Sol", "destination": "Node Beta", "reward": 2000, "collateral": 500, "volume": 40, "shipper_tag": "NPC"},
                    {"id": "sh-irlc-1", "origin": "Ironlight", "destination": "Atria", "reward": 1200, "collateral": 200, "volume": 20, "shipper_tag": "IRLC"},
                ]
            }
        }
        out = shipping.format_list(body, {"IRLC": "Ironlight Combine"}, limit=10)
        lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
        self.assertIn("[PARTNER:IRLC]", lines[1])
        self.assertIn("sh-irlc-1", lines[1])
        self.assertIn("sh-npc-1", lines[2])

    def test_call_shipping_uses_raw_endpoint_and_toolgroup(self):
        with mock.patch.object(shipping.gate, "call", return_value=(200, '{"result":"ok"}')) as m:
            code, body = shipping.call_shipping("hauler-13", "list_all", {})
            self.assertEqual(code, 200)
            self.assertEqual(body["result"], "ok")
            method, path, payload = m.call_args[0][0], m.call_args[0][1], m.call_args[0][2]
            self.assertEqual(method, "post")
            self.assertEqual(path, "/accounts/hauler-13/raw")
            self.assertEqual(payload["toolGroup"], "spacemolt_shipping")
            self.assertEqual(payload["action"], "list_all")


if __name__ == "__main__":
    unittest.main()
