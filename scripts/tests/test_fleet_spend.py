"""spend.py: what the fleet bought once, by division and kind; moves and escrow left out; a window cut to the record."""

import importlib.util
import json
from pathlib import Path
import tempfile
import time
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SpendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-spend-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [
            {"name": "miner-1", "division": "Mining"}, {"name": "drone-1", "division": "Military"},
            {"name": "hauler-1", "division": "Logistics"}, {"name": "trader-1", "division": "Trade"}]}), encoding="ascii")
        self.now = time.time()
        self.spend = load("spend")

    def book(self, rows):
        (self.data / "fleet" / "onetime.json").write_text(json.dumps([[self.now - ago, p, t, c] for ago, p, t, c in rows]), encoding="ascii")

    def test_each_title_falls_to_its_kind(self):
        kind = self.spend.kind_of
        self.assertEqual(kind("fit_net shield_booster_iii", -12000), "modules")
        self.assertEqual(kind("fit-t2-lasers-lhs-1140: mining_laser_iii bought (tool)", -5600), "modules")
        self.assertEqual(kind("Paradox hull bought from listing", -40494), "hulls")
        self.assertEqual(kind("Apophenia hull commissioned", -140000), "hulls")
        self.assertEqual(kind("hauler-6: 120 reinforced_frame bought (craft inputs)", -500000), "craft inputs")
        self.assertEqual(kind("craft_net listed stock coolant_fluid", -300), "craft inputs")
        self.assertEqual(kind("mission-market-participation-alpha: oxygen_gas bought", -32), "mission goods")
        self.assertEqual(kind("Wallet top-up", -10000), "move")
        self.assertEqual(kind("Treasury fund: credits withdrawn from the faction treasury for top-ups: 2 pilots", 4940), "move")
        self.assertEqual(kind("Faction treasury: credits deposited (the Collective keeps them)", -26957), "move")
        self.assertEqual(kind("Exchange buy escrow: locked", -2000), "escrow")
        self.assertEqual(kind("Exchange buy escrow: released", 2000), "escrow")
        self.assertEqual(kind("The Colonies", 5000), "reward")
        self.assertEqual(kind("Weekly tax", -900), "tax")

    def test_a_window_sums_by_division_and_leaves_moves_and_escrow_out(self):
        self.book([(600, "miner-1", "fit_net shield_booster_iii", -12000), (900, "drone-1", "fit_net autocannon_ii", -3000),
                   (1200, "hauler-1", "Prayer hull bought from listing", -4714), (1300, "trader-1", "The Colonies", 5000),
                   (1400, "trader-1", "Exchange buy escrow: locked", -2000), (1500, "trader-1", "Exchange buy escrow: released", 1500),
                   (1600, "miner-1", "Wallet top-up", -10000), (1600, "drone-1", "Wallet top-up", 10000),
                   (5 * 3600, "miner-1", "fit_net mining_laser_ii", -4000), (9 * 3600, "miner-1", "fit_net old", -99999)])
        found = self.spend.gather(str(self.data), 1, self.now)
        self.assertEqual(found["div"]["Mining"], {"modules": 12000})
        self.assertEqual(found["div"]["Military"], {"modules": 3000})
        self.assertEqual(found["div"]["Logistics"], {"hulls": 4714})
        self.assertEqual(found["rewards"], {"Trade": 5000})
        self.assertEqual(found["escrow"], 500)                  # 2,000 locked, 1,500 released: 500 still held
        self.assertEqual(found["moves"], 20000)
        six = self.spend.gather(str(self.data), 6, self.now)
        self.assertEqual(six["div"]["Mining"], {"modules": 16000})
        self.assertAlmostEqual(six["covers"], 6, places=2)

    def test_a_deposit_is_no_buy_and_the_brief_names_it(self):
        self.book([(600, "miner-1", "Faction treasury: credits deposited (the Collective keeps them)", -26957)])
        line = self.spend.brief(str(self.data), self.now)[0]
        self.assertIn("nothing | rewards 0", line)
        self.assertIn("into the faction's treasury 26,957 in 1 deposits", line)

    def test_a_window_longer_than_the_record_is_cut_and_says_so(self):
        self.book([(2 * 3600, "miner-1", "fit_net mining_laser_ii", -4000), (600, "ghost-1", "fit_net x", -10)])
        found = self.spend.gather(str(self.data), 24, self.now)
        self.assertLess(found["covers"], 2.01)
        self.assertEqual(found["div"]["none"], {"modules": 10})        # a pilot the fleet file does not name
        text = "\n".join(self.spend.table(found))
        self.assertIn("asked 24 h; the record holds no older row", text)
        lines = self.spend.brief(str(self.data), self.now)
        self.assertTrue(lines[1].startswith("    bought once, last 2.0 h (the record holds no older row): modules 4,010"), lines[1])


if __name__ == "__main__":
    unittest.main()
