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

    def test_a_free_pilot_whose_run_ended_after_its_reading_is_read_first(self):
        now = 1_800_000_000
        text = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
        names = ["hauler-%d" % n for n in range(1, 9)]
        (self.data / "routes" / "logs").mkdir()

        def ended(pilot, ago):
            path = self.data / "routes" / "logs" / (pilot + ".log")
            path.write_text("RESULT\n")
            os.utime(path, (now - ago, now - ago))

        book = {"pilots": {name: {"read_at": text(now - 1500), "stations": {}} for name in names}}
        ended("hauler-6", 300)                                       # free, its run ended after the reading: it waits on the book
        ended("hauler-7", 600)                                       # the same, and it waits longer: first
        ended("hauler-8", 300)                                       # its run ended, but a new run flies it
        order = self.data / "fleet" / "orders" / "hauler-8.json"
        order.write_text(json.dumps({"pilot": "hauler-8", "what": "circuit craft-steel"}))
        os.utime(order, (now - 10, now - 10))
        ended("hauler-5", 2000)                                      # read after its last run: nothing changed since
        ended("hauler-4", 10)                                        # between two runs: the dispatcher sends it on
        self.assertEqual(ledger.due(names, book, str(self.data), now), ["hauler-7", "hauler-6"])
        batch, step = ledger.batch_of(names, 0, book, str(self.data), now)
        self.assertEqual((batch, step), (["hauler-7", "hauler-6", "hauler-1", "hauler-2", "hauler-3", "hauler-4"], 4))   # the rotation keeps its four
        book["pilots"]["hauler-7"]["read_at"] = text(now)            # read: it waits no longer
        self.assertEqual(ledger.due(names, book, str(self.data), now), ["hauler-6"])
        book["pilots"]["hauler-6"]["error_at"] = text(now - 30)      # its reading just failed: not every pass
        self.assertEqual(ledger.due(names, book, str(self.data), now), [])
        self.assertEqual(ledger.due(names, book, str(self.data), now + 200), ["hauler-6", "hauler-4"])   # tried again after two minutes; and nobody sent hauler-4 on
        os.utime(order, (now - 3000, now - 3000))                    # an order file nobody touched for 50 minutes is dead
        self.assertEqual(ledger.due(names, book, str(self.data), now + 200), ["hauler-6", "hauler-8", "hauler-4"])
        batch, step = ledger.batch_of(names, 4, book, str(self.data), now + 200)
        self.assertEqual((batch, step), (["hauler-4", "hauler-5", "hauler-6", "hauler-7", "hauler-8"], 4))   # a pilot the rotation reads anyway is read once
        many = ["hauler-%d" % n for n in range(1, 21)]
        for name in many[8:]:
            ended(name, 100)
        big = {"pilots": {name: {"read_at": text(now - 1500)} for name in many}}
        batch, step = ledger.batch_of(many, 0, big, str(self.data), now)
        self.assertEqual((len(batch), step, batch[3:]), (7, 4, many[:4]))                        # three at most in front of the four

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

    def test_a_pilot_that_is_not_connected_for_a_moment_keeps_its_stores_in_the_book(self):
        # 2026-11-16: the book fell from 336,568 to 131,954 units in 18 minutes; a pilot left it whenever one pass did not read it `connected`
        book = {"pilots": {"miner-1": {"stations": {"home": {"iron_ore": 5}}}, "miner-2": {"stations": {"home": {"iron_ore": 7}}}, "miner-9": {"stations": {}}}}
        fleet = self.data / "fleet" / "fleet.json"
        fleet.parent.mkdir(parents=True, exist_ok=True)
        ships = [{"name": "miner-1", "status": "connected"}, {"name": "miner-2", "status": "reconnecting"}]
        fleet.write_text(json.dumps({"engine": {"ok": False}, "ships": ships}))
        self.assertEqual((ledger.leave(book, str(self.data)), sorted(book["pilots"])), ([], ["miner-1", "miner-2", "miner-9"]))      # the engine does not answer: nobody leaves
        fleet.write_text(json.dumps({"engine": {"ok": True}, "ships": []}))
        self.assertEqual(ledger.leave(book, str(self.data)), [])                                  # a file that names nobody is no roster
        fleet.write_text(json.dumps({"engine": {"ok": True}, "ships": ships}))
        now = time.time()
        self.assertEqual(ledger.leave(book, str(self.data), now), [])                            # left out once: its count starts (r22, requests ENT-284)
        self.assertEqual((ledger.leave(book, str(self.data), now + ledger.LEAVE_LONG), sorted(book["pilots"])), (["miner-9"], ["miner-1", "miner-2"]))   # only the pilot the fleet has no longer
        self.assertEqual(ledger.pilots_of(str(self.data)), ["miner-1"])                           # and only a connected pilot is read

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


    def test_ship_listings_pass_paginates_and_throttles(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "fleet").mkdir(parents=True)
            (data / "fleet" / "fleet.json").write_text(json.dumps({
                "ships": [{"name": "Scout-1", "status": "connected", "docked": "central_nexus", "in_combat": False}]
            }), encoding="ascii")
            pages = {
                1: {"total": 2, "total_pages": 2, "listings": [
                    {"listing_id": "l1", "ship_id": "s1", "class_id": "Prayer", "ship_name": "P1", "category": "Commercial",
                     "tier": 2, "base_id": "haven_base", "base_name": "Haven", "price": 3288, "seller": "Bob", "listed_at": "2026-11-24T00:00:00Z"}
                ]},
                2: {"total": 2, "total_pages": 2, "listings": [
                    {"listing_id": "l1", "ship_id": "s1", "class_id": "Prayer", "ship_name": "P1", "category": "Commercial",
                     "tier": 2, "base_id": "haven_base", "base_name": "Haven", "price": 3288, "seller": "Bob", "listed_at": "2026-11-24T00:00:00Z"},
                    {"listing_id": "l2", "ship_id": "s2", "class_id": "broadaxe", "ship_name": "B1", "category": "Combat",
                     "tier": 2, "base_id": "krynn_base", "base_name": "Krynn", "price": 37000, "seller": "Red", "listed_at": "2026-11-24T01:00:00Z"},
                ]},
            }
            calls = []
            def fake_fetch(pilot, page):
                calls.append((pilot, page))
                return pages[page], ""
            n1 = ledger.ship_listings_pass(data, now=10000, fetch=fake_fetch, pause=0)
            self.assertEqual(n1, 2)
            self.assertEqual(calls, [("Scout-1", 1), ("Scout-1", 2)])
            out = json.loads((data / "market" / "ship_listings.json").read_text(encoding="ascii"))
            self.assertEqual([r["class_id"] for r in out["listings"]], ["broadaxe", "prayer"])
            # market_pass must skip ship_listings.json cleanly
            self.assertEqual(ledger.market_pass(data, {}), 0)
            # throttled within SHIP_LISTINGS_EVERY unless force=True
            n2 = ledger.ship_listings_pass(data, now=time.time(), fetch=fake_fetch, pause=0)
            self.assertEqual(n2, 0)

if __name__ == "__main__":
    unittest.main()
