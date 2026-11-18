"""Tests of game/fleet/workclass.py: whose work a route is (Suggi, 2026-11-18: ore is the miners' job)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "game", "fleet"))
import workclass  # noqa: E402


class WorkClassTests(unittest.TestCase):
    def test_gathering_is_the_miners(self):
        route = {"kind": "mine", "belt": "x"}
        self.assertEqual(workclass.work_class(route, "gather-x"), "gather")
        self.assertEqual(workclass.roles_for(route, "gather-x"), ("miner",))
        for role in ("trader", "hauler", "drone", "sentinel", "scout", "command"):
            self.assertFalse(workclass.own(role, route, "gather-x"), role)

    def test_a_circuit_that_mines_is_gathering(self):
        route = {"kind": "circuit", "stops": [{"at": "a", "mine": {"item": "iron_ore"}}, {"at": "b", "store": "all"}]}
        self.assertEqual(workclass.work_class(route, "c"), "gather")

    def test_hunt_guard_census(self):
        self.assertEqual(workclass.roles_for({"kind": "hunt"}, "hunt-x"), ("drone", "sentinel", "scout", "command"))
        self.assertEqual(workclass.roles_for({"kind": "guard"}, "guard-x"), ("drone", "sentinel"))
        self.assertEqual(workclass.roles_for({"kind": "census"}, "census-x"), ("scout",))

    def test_missions_and_own_stores_are_everyones(self):
        everyone = set(workclass.ALL)
        self.assertEqual(set(workclass.roles_for({"kind": "circuit", "stops": [{"accept": 1, "hunt": 1}]}, "voidborn-first-hunt")), everyone)
        far_sale = {"kind": "circuit", "stops": [{"at": "a", "withdraw": [{"item": "x"}]}, {"at": "b", "sell": [{"item": "x"}]}]}
        self.assertEqual(workclass.work_class(far_sale, "sell-x"), "sell")
        self.assertEqual(set(workclass.roles_for(far_sale, "sell-x")), everyone)
        craft = {"kind": "circuit", "stops": [{"at": "a", "craft": [{"recipe": "r"}], "store": "all"}]}
        self.assertEqual(workclass.work_class(craft, "craft-x"), "craft")

    def test_buying_and_bases(self):
        buy = {"kind": "circuit", "stops": [{"at": "a", "buy": [{"item": "x"}]}, {"at": "b", "store": "all"}]}
        self.assertEqual(workclass.roles_for(buy, "buy-x"), ("trader", "hauler"))
        bunker = {"kind": "circuit", "stops": [{"at": "a", "buy": [{"item": "fuel_cell"}]}, {"at": "b", "bunker": {"keep": 30}}]}
        self.assertEqual(workclass.roles_for(bunker, "supply-x"), ("hauler",))

    def test_open_to_is_the_admirals_word(self):
        route = {"kind": "mine", "open_to": ["hauler", "nobody"]}
        self.assertEqual(workclass.roles_for(route, "mine-x"), ("miner", "hauler"))

    def test_every_route_file_has_a_class(self):
        known = set(workclass.CLASS_ROLES) | set(workclass.SHARED)
        for rid, route in workclass.load().items():
            self.assertIn(workclass.work_class(route, rid), known, rid)


if __name__ == "__main__":
    unittest.main()
