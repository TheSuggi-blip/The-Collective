"""game/fleet/stats.py service_handover: what each division handed over to Trade and Logistics (data/stock/handover.jsonl,
one line per gift of goods) at what it would sell for now: per item, the units of all givers within the depth of the
best bid of any saved book, shared by units; beyond the depth or without a bid at 0, and named (orders ENT-064, block UNITY: the goods each division hands
over at their worth, so P1 reads what hunts and gathers enable). A disposable data folder; no engine, no network.
"""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)
FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_handover_worth_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NOW = 1795370000


class HandoverWorthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-handover-worth-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "stock").mkdir()
        (self.data / "market").mkdir()
        rows = [{"at": NOW - 600, "base": "base_a", "from": "miner-1", "to": "hauler-1", "items": {"carbon_ore": 100}, "route": "g"},
                {"at": NOW - 300, "base": "base_b", "from": "drone-2", "to": "trader-3", "items": {"curd": 4, "odd_thing": 2}, "route": "h"},
                {"at": NOW - 90000, "base": "base_a", "from": "miner-1", "to": "hauler-1", "items": {"carbon_ore": 999}, "route": "old"}]
        (self.data / "stock" / "handover.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        book = lambda base, items: {"base": base, "items": [{"item_id": i, "best_buy": b, "best_buy_qty": 50} for i, b in items]}
        (self.data / "market" / "base_a.json").write_text(json.dumps(book("base_a", [("carbon_ore", 3)])))
        (self.data / "market" / "base_c.json").write_text(json.dumps(book("base_c", [("carbon_ore", 9), ("curd", 330)])))
        self.stats = load("stats")
        self.stats.owner_division = lambda pilot, data: {"miner": "Mining", "drone": "Military"}[pilot.split("-")[0]]

    def test_worth_within_the_best_bid_s_depth_and_the_rest_is_named(self):
        rows = {(r[0], r[1]): r for r in self.stats.service_handover(self.data, NOW, NOW - 24 * 3600, 24)}
        self.assertEqual(rows[("Mining", "handed_over_worth")][3], 50 * 9)       # 100 carbon: base_c's bid of 9 holds 50
        self.assertIn("50 units beyond the depth or without a bid", rows[("Mining", "handed_over_worth")][5])
        self.assertEqual(rows[("Military", "handed_over_worth")][3], 4 * 330)     # curd within its depth; odd_thing has no bid
        self.assertEqual(rows[("Military", "handed_over_units")][3], 6)
        self.assertIn("2 units beyond the depth or without a bid", rows[("Military", "handed_over_worth")][5])

    def test_two_divisions_share_one_bid_s_depth_by_their_units(self):
        with open(self.data / "stock" / "handover.jsonl", "a") as handle:
            handle.write(json.dumps({"at": NOW - 100, "base": "base_a", "from": "drone-5", "to": "trader-3", "items": {"carbon_ore": 100}}) + "\n")
        rows = {(r[0], r[1]): r for r in self.stats.service_handover(self.data, NOW, NOW - 24 * 3600, 24)}
        self.assertEqual(rows[("Mining", "handed_over_worth")][3], 25 * 9)        # 200 carbon, depth 50: each gave half
        self.assertEqual(rows[("Military", "handed_over_worth")][3], 25 * 9 + 4 * 330)
        self.assertEqual(rows[("Mining", "handed_over_units")][4], 1)             # one gift in the window; the old one is out

    def test_no_file_is_said_plainly(self):
        (self.data / "stock" / "handover.jsonl").unlink()
        rows = self.stats.service_handover(self.data, NOW, NOW - 24 * 3600, 24)
        self.assertEqual([(r[0], r[1], r[3]) for r in rows], [("Command", "handed_over_worth", None)])
        self.assertIn("not measured", rows[0][5])


if __name__ == "__main__":
    unittest.main()
