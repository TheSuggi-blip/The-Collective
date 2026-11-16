"""game/fleet/ledger.py and board.py on disposable data folders: the storage book, the moves of an order book, a division's board. No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ledger, board = load("ledger"), load("board")


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-ledger-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("fleet/ships", "fleet/orders", "market", "routes"):
            (self.data / folder).mkdir(parents=True)


class StorageTests(Tree):
    def test_a_pilot_is_read_at_every_station_it_stores_at(self):
        answers = {("miner-1", "central_nexus"): ({"iron_ore": 5}, ["central_nexus", "node_beta"], ""), ("miner-1", "node_beta"): ({"copper_ore": 7}, [], "")}
        entry = ledger.read_pilot("miner-1", look=lambda p, s: answers[(p, s)], pause=0)
        self.assertEqual(entry["stations"], {"central_nexus": {"iron_ore": 5}, "node_beta": {"copper_ore": 7}})
        empty = ledger.read_pilot("miner-2", look=lambda p, s: ({}, [], ""), pause=0)
        self.assertEqual(empty["stations"], {})
        failed = ledger.read_pilot("miner-3", look=lambda p, s: (None, [], "not connected"), pause=0)
        self.assertEqual((failed.get("error"), "stations" in failed), ("not connected", False))
        half = ledger.read_pilot("miner-1", look=lambda p, s: answers[(p, s)] if s == "central_nexus" else (None, [], "timeout"), pause=0)
        self.assertEqual(half["error"], "node_beta: timeout")                                     # a half reading is no reading

    def test_totals_count_each_pilot_once_per_station_and_member(self):
        (self.data / "fleet" / "ships" / "miner-1.json").write_text(json.dumps({"name": "miner-1", "cargo": [{"item_id": "iron_ore", "quantity": 3}]}))
        (self.data / "fleet" / "ships" / "drone-1.json").write_text(json.dumps({"name": "drone-1", "cargo": [{"item": "verdigris_curd", "name": "Verdigris Curd", "quantity": 2}, "broken"]}))
        pilots = {"miner-1": {"stations": {"node_beta": {"iron_ore": 10}}}, "miner-2": {"stations": {"node_beta": {"iron_ore": 5, "copper_ore": 1}}},
                  "drone-1": {"stations": {"central_nexus": {"iron_ore": 2}}}, "drone-2": {"error": "not connected"}}
        found = ledger.totals(pilots, str(self.data))
        self.assertEqual(found["by_station"], {"node_beta": {"iron_ore": 15, "copper_ore": 1}, "central_nexus": {"iron_ore": 2}})
        self.assertEqual(found["by_member"]["Zero"], {"node_beta": {"iron_ore": 15, "copper_ore": 1}})
        self.assertEqual(found["by_member"]["Apophis"], {"central_nexus": {"iron_ore": 2}})
        self.assertEqual(found["holds_by_member"], {"Zero": {"iron_ore": 3}, "Apophis": {"verdigris_curd": 2}})


class MarketTests(Tree):
    def book(self, read_at, items):
        (self.data / "market" / "node_beta.json").write_text(json.dumps({"base": "node_beta", "read_at": read_at, "items": items}))

    def lines(self):
        path = self.data / "market" / "history.jsonl"
        return [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []

    def test_only_a_changed_best_bid_or_ask_is_a_move(self):
        seen = {}
        self.book("2026-01-01T10:00:00Z", [{"item_id": "curd", "best_buy": 330, "best_buy_qty": 240, "best_sell": 0}, {"item_id": "dust", "best_buy": 0, "best_sell": 0},
                                           {"item_id": "ore", "best_buy": 2, "buy_quantity": 9, "best_sell": 5, "sell_quantity": 4}])
        self.assertEqual(ledger.market_pass(str(self.data), seen), 2)                             # the first read is the baseline; an item without a price is none
        self.assertEqual(ledger.market_pass(str(self.data), seen), 0)                             # the same file again: nothing
        self.assertEqual(self.lines()[1], {"t": "2026-01-01T10:00:00Z", "base": "node_beta", "item": "ore", "bid": 2, "bid_qty": 9, "ask": 5, "ask_qty": 4})
        time.sleep(0.01)
        self.book("2026-01-01T10:30:00Z", [{"item_id": "curd", "best_buy": 330, "best_buy_qty": 100, "best_sell": 0}, {"item_id": "ore", "best_buy": 3, "buy_quantity": 9, "best_sell": 5}])
        os.utime(self.data / "market" / "node_beta.json", None)
        self.assertEqual(ledger.market_pass(str(self.data), seen), 1)                             # a smaller bid at the same price is no move; ore's bid rose
        self.assertEqual((self.lines()[-1]["item"], self.lines()[-1]["bid"]), ("ore", 3))
        time.sleep(0.01)
        self.book("2026-01-01T11:00:00Z", [{"item_id": "ore", "best_buy": 3, "best_sell": 5}])
        self.assertEqual(ledger.market_pass(str(self.data), seen), 1)                             # the curd left the book
        self.assertEqual((self.lines()[-1]["item"], self.lines()[-1]["bid"], self.lines()[-1]["ask"]), ("curd", 0, 0))
        self.assertEqual(ledger.market_pass(str(self.data), {}), 0)                               # a restart writes no line twice


class BoardTests(Tree):
    def test_a_ship_is_named_by_what_it_does_and_a_figure_leaves_one_time_money_out(self):
        self.assertEqual(board.state_of({"status": "connected", "docked": True, "activity": {"kind": "idle"}}, ""), "docked, free")
        self.assertEqual(board.state_of({"status": "connected", "docked": False, "activity": {"kind": "idle"}}, ""), "in space, free")
        self.assertEqual(board.state_of({"status": "connected", "activity": {"kind": "goal"}}, "hunt rays"), "hunt rays")
        self.assertEqual(board.state_of({"status": "disconnected"}, "hunt rays"), "not connected")
        rows = [{"minutes": 30, "delta": 5000, "one_time": 4000, "credits_before": 9000}, {"minutes": 30, "delta": -100, "credits_before": 9000},
                {"minutes": 45, "delta": 0, "credits_before": 0}]
        self.assertEqual(board.figure(rows), (2, 1.0, 900, 900))
        self.assertEqual(board.figure([rows[2]]), (0, 0.0, 0, None))

    def test_the_board_of_a_member_lists_its_ships_only(self):
        ships = [{"name": "miner-1", "status": "connected", "docked": True, "system": "home", "credits": 9000, "fuel": 50, "max_fuel": 100, "activity": {"kind": "idle"}},
                 {"name": "miner-2", "status": "connected", "docked": False, "system": "far", "credits": 7000, "fuel": 90, "max_fuel": 100, "activity": {"kind": "goal"}},
                 {"name": "drone-1", "status": "connected", "docked": True, "system": "home", "credits": 1, "activity": {"kind": "idle"}}]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ships": ships}))
        (self.data / "fleet" / "orders" / "miner-2.json").write_text(json.dumps({"pilot": "miner-2", "what": "circuit some-route"}))
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 600))
        (self.data / "routes" / "runs.jsonl").write_text(json.dumps({"route": "some-route", "pilot": "miner-1", "started": started, "minutes": 60, "delta": 250, "credits_before": 9000}) + "\n"
                                                         + json.dumps({"route": "other", "pilot": "drone-1", "started": started, "minutes": 60, "delta": 99, "credits_before": 9000}) + "\n")
        text = "\n".join(board.block("Zero", str(self.data), 4, time.time()))
        self.assertIn("ships 2 | credits 16,000 | lowest wallet 7,000 | lowest fuel 50%", text)
        self.assertIn("circuit some-route", text)
        self.assertIn("docked, free", text)
        self.assertIn("some-route                   runs 1   ship-hours   1.0  credits     +250  per ship-hour +250", text)
        self.assertNotIn("drone-1", text)
        self.assertNotIn("other", text)
        self.assertIn("PLAN miner (game/routes/plans/miner.json)", text)                           # the repository's own plan of the role


if __name__ == "__main__":
    unittest.main()
