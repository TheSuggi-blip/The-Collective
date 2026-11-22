"""game/fleet/supply.py level_faults: a chain at `fleet` whose keep differs from the `min` line game/reserve.tsv names
for its item is an ERROR of `supply.py check`, so the two readers of one good never disagree again (requests ENT-355,
Zero; errors.log ENT-137: the chain iron-ore read short at a keep of 166,923 while the reserve called 152,651 iron full
at a demand of 60,070, and the miners' plan followed one of them). Pure function over rows and a disposable root.
"""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_levels_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RESERVE = ("# test\nkind\tid\tunits\tnote\n"
           "keep\tfuel_cell\tall\tfuel\n"
           "min\tiron_ore\t60000\tgathered again below\n"
           "max\tiron_ore\t80000\tgathered up to\n")


class LevelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-supply-levels-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "reserve.tsv").write_text(RESERVE, encoding="ascii")
        self.supply = load("supply")

    def test_a_keep_that_differs_from_the_reserve_s_min_is_an_error(self):
        rows = [{"chain": "iron-ore", "item": "iron_ore", "place": "fleet", "keep": 166923}]
        self.assertEqual(self.supply.level_faults(rows, self.root),
                         [("ERROR", "iron-ore: keep 166,923 differs from game/reserve.tsv `min iron_ore 60,000`: one figure for one good (set both alike)")])

    def test_an_equal_keep_another_place_or_no_min_line_is_no_fault(self):
        rows = [{"chain": "iron-ore", "item": "iron_ore", "place": "fleet", "keep": 60000},
                {"chain": "bunker", "item": "iron_ore", "place": "base_o", "keep": 5},
                {"chain": "cells", "item": "fuel_cell", "place": "fleet", "keep": 0}]
        self.assertEqual(self.supply.level_faults(rows, self.root), [])
        self.assertEqual(self.supply.level_faults(rows, self.root / "nowhere"), [])


if __name__ == "__main__":
    unittest.main()
