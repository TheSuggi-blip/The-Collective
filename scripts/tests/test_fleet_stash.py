"""game/fleet/stash.py: which goods of a hold are stored. No engine, no network."""

import importlib.util
from pathlib import Path
import sys
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


class StashTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(FLEET))
        self.addCleanup(sys.path.remove, str(FLEET))
        spec = importlib.util.spec_from_file_location("stash_under_test", FLEET / "stash.py")
        self.stash = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.stash)

    def test_ammunition_stays_and_the_rest_is_stored_largest_first(self):
        cargo = [{"item_id": "carbon_ore", "quantity": 8}, {"item_id": "pulse_cell", "quantity": 40}, {"item_id": "lead_ore", "quantity": 1},
                 {"item_id": "carbon_ore", "quantity": 4}, {"item_id": "empty", "quantity": 0}, "noise"]
        self.assertEqual(self.stash.leftovers(cargo, {"pulse_cell"}), [("carbon_ore", 12), ("lead_ore", 1)])
        self.assertEqual(self.stash.leftovers(None, set()), [])


if __name__ == "__main__":
    unittest.main()
