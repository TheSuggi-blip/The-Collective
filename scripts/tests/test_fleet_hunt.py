"""game/fleet/hunt.py: which goods stay aboard after the sale. No engine, no network.

hunt.py flies a hunt when it is loaded, so the test takes the one function it needs
out of the file's syntax tree and runs it alone.
"""

import ast
import calendar
import glob
import json
import os
from pathlib import Path
import tempfile
import time
import unittest


HUNT = Path(__file__).resolve().parents[2] / "game" / "fleet" / "hunt.py"


def load(name):
    tree = ast.parse(HUNT.read_text(encoding="utf-8"))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if not found:
        raise AssertionError("hunt.py has no top-level function %s" % name)
    space = {"calendar": calendar, "glob": glob, "json": json, "os": os, "time": time}
    exec(compile(ast.Module(body=found, type_ignores=[]), str(HUNT), "exec"), space)
    return space[name]


def book(folder, base, read_at, items):
    with open(os.path.join(folder, base + ".json"), "w", encoding="utf-8") as fh:
        json.dump({"base": base, "read_at": read_at, "items": items}, fh)


class WantedGoodsTests(unittest.TestCase):
    def setUp(self):
        self.wanted_goods = load("wanted_goods")
        self.folder = tempfile.mkdtemp()
        self.now = calendar.timegm(time.strptime("2026-11-16T19:00:00Z", "%Y-%m-%dT%H:%M:%SZ"))

    def test_a_bid_read_within_the_hour_keeps_the_good_aboard(self):
        book(self.folder, "central_nexus", "2026-11-16T18:30:00Z",
             [{"item_id": "verdigris_curd", "best_buy": 330, "buy_quantity": 50}])
        self.assertEqual(self.wanted_goods(self.folder, 100, self.now), {"verdigris_curd"})

    def test_a_book_older_than_an_hour_keeps_nothing_aboard(self):
        # the case of 2026-11-16 19:02 UTC: one curd bid at 368 cr in a book 268 minutes old kept 6 curd aboard
        book(self.folder, "nova_terra_central", "2026-11-16T13:57:16Z",
             [{"item_id": "verdigris_curd", "best_buy": 368, "buy_quantity": 1}])
        self.assertEqual(self.wanted_goods(self.folder, 100, self.now), set())

    def test_a_low_or_empty_bid_and_a_file_without_a_time_keep_nothing(self):
        book(self.folder, "the_experiment_research_station", "2026-11-16T18:59:00Z",
             [{"item_id": "creature_carapace", "best_buy": 2, "buy_quantity": 476},
              {"item_id": "ember_gland", "best_buy": 480, "buy_quantity": 0}])
        with open(os.path.join(self.folder, "ladders.json"), "w", encoding="utf-8") as fh:
            json.dump({"items": [{"item_id": "verdigris_curd", "best_buy": 330, "buy_quantity": 5}]}, fh)
        with open(os.path.join(self.folder, "broken.json"), "w", encoding="utf-8") as fh:
            fh.write("{")
        self.assertEqual(self.wanted_goods(self.folder, 100, self.now), set())


if __name__ == "__main__":
    unittest.main()
