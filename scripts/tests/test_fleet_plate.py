"""game/fleet/plate.py: how many plates are made and how many are sold into a bid. No engine, no network."""

import importlib.util
from pathlib import Path
import sys
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


class PlateTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(FLEET))
        self.addCleanup(sys.path.remove, str(FLEET))
        spec = importlib.util.spec_from_file_location("plate_under_test", FLEET / "plate.py")
        self.plate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.plate)

    def test_one_plate_for_every_full_six_carapace(self):
        self.assertEqual(self.plate.crafts({"creature_carapace": 13}), 2)
        self.assertEqual(self.plate.crafts({"creature_carapace": 5}), 0)
        self.assertEqual(self.plate.crafts({}), 0)

    def test_never_past_the_depth_nor_under_the_floor(self):
        self.assertEqual(self.plate.to_sell(10, 373, 4, 200), 4)
        self.assertEqual(self.plate.to_sell(2, 373, 4, 200), 2)
        self.assertEqual(self.plate.to_sell(10, 2, 101, 200), 0)
        self.assertEqual(self.plate.to_sell(10, 0, 0, 200), 0)
        self.assertEqual(self.plate.to_sell(0, 400, 6, 200), 0)

    def test_the_best_bid_is_the_highest_price_with_its_own_depth(self):
        answer = {"structuredContent": {"items": [
            {"item_id": "creature_carapace", "buy_orders": [{"price_each": 1, "quantity": 900}]},
            {"item_id": "armor_plate", "buy_orders": [{"price_each": 300, "quantity": 9}, {"price_each": 373, "quantity": 4}]}]}}
        self.assertEqual(self.plate.best_bid(answer), (373, 4))
        self.assertEqual(self.plate.best_bid({"structuredContent": {"items": []}}), (0, 0))
        self.assertEqual(self.plate.best_bid("noise"), (0, 0))


if __name__ == "__main__":
    unittest.main()
