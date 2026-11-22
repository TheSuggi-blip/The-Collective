"""Tests of game/fleet/workclass.py: whose work a route is (Suggi, 2026-11-18: ore is the miners' job)."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "game", "fleet"))
import workclass  # noqa: E402


class WorkClassTests(unittest.TestCase):
    def setUp(self):
        prev = workclass.STRICT
        workclass.STRICT = False
        self.addCleanup(setattr, workclass, "STRICT", prev)

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


class StrictClassTests(unittest.TestCase):
    """r22 (Suggi, 2026-11-21: "Only Zero mines, only Mercury trades"): behind data/fleet/strict-classes-on selling and
    buying are Trade's, crafting Logistics' and Trade's, and the dispatcher refuses a sale on a route of another class."""
    BUY_CRAFT = {"kind": "circuit", "stops": [{"at": "a", "buy": [{"item": "x"}], "craft": [{"recipe": "r"}]}]}
    BUY = {"kind": "circuit", "stops": [{"at": "a", "buy": [{"item": "x"}]}, {"at": "b", "sell": [{"item": "x"}]}]}
    SELL = {"kind": "circuit", "stops": [{"at": "a", "withdraw": [{"item": "x"}]}, {"at": "b", "sell": [{"item": "x"}]}]}
    GIFT = {"kind": "circuit", "stops": [{"at": "a", "withdraw": [{"item": "x"}]}, {"at": "b", "store": "all", "gift": {"to": "trader"}}]}
    MINE_SELL = {"kind": "mine", "belt": "a:b", "station": "a:b:c", "sell": [{"item": "x", "min_price": 9}]}
    HUNT = {"kind": "hunt", "place": "a:b", "sell_at": "a:b:c"}

    def setUp(self):
        self.addCleanup(setattr, workclass, "STRICT", None)
        self.addCleanup(workclass.SEEN.clear)
        self.addCleanup(setattr, workclass, "DATA", workclass.DATA)

    def test_off_the_classes_are_those_of_today(self):
        workclass.STRICT = False
        self.assertEqual(workclass.work_class(self.BUY_CRAFT, "c"), "trade")          # a buy wins over a craft
        self.assertEqual(workclass.roles_for(self.BUY, "b"), ("trader", "hauler"))
        self.assertEqual(set(workclass.roles_for(self.SELL, "s")), set(workclass.ALL))
        self.assertEqual(workclass.work_class(self.GIFT, "g"), "other")
        self.assertEqual(workclass.classes_of("miner"), ("gather", "once", "sell", "craft", "fit", "other"))
        self.assertEqual(workclass.SHARED, ("once", "sell", "craft", "fit", "other"))

    def test_on_selling_and_buying_are_the_traders_and_crafting_the_haulers_and_traders(self):
        workclass.STRICT = True
        self.assertEqual(workclass.work_class(self.BUY_CRAFT, "c"), "craft")
        self.assertEqual(workclass.roles_for(self.BUY_CRAFT, "c"), ("hauler", "trader"))
        self.assertEqual(workclass.roles_for(self.BUY, "b"), ("trader",))
        self.assertEqual(workclass.roles_for(self.SELL, "s"), ("trader",))
        self.assertEqual(workclass.work_class(self.GIFT, "g"), "deliver")
        self.assertEqual(set(workclass.roles_for(self.GIFT, "g")), set(workclass.ALL))
        self.assertEqual(workclass.classes_of("hauler"), ("haul", "craft", "once", "deliver", "fit", "other"))
        self.assertEqual(workclass.CLASS_ROLES["sell"], ("trader",))
        self.assertNotIn("sell", workclass.SHARED)
        bunker = {"kind": "circuit", "stops": [{"at": "a", "buy": [{"item": "fuel_cell"}]}, {"at": "b", "bunker": {"keep": 30}}]}
        self.assertEqual(workclass.roles_for(bunker, "supply-x"), ("hauler",))         # base supply stays Logistics'

    def test_the_switch_file_decides_in_the_data_folder_the_caller_follows(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "fleet").mkdir()
            workclass.follow(folder)
            self.assertFalse(workclass.strict_on())
            (Path(folder) / "fleet" / "strict-classes-on").write_text("")
            workclass.SEEN.clear()                                                     # one look holds a second
            self.assertTrue(workclass.strict_on())
            self.assertEqual(workclass.roles_for(self.SELL, "s"), ("trader",))
            workclass.STRICT = False                                                   # a caller's own setting wins
            self.assertFalse(workclass.strict_on())

    def test_with_the_switch_on_a_sale_is_refused_to_every_pilot_but_a_trader(self):
        workclass.STRICT = True
        miner, drone, trader = {"name": "miner-1"}, {"name": "drone-1", "role": "drone"}, {"name": "Mercurys Ledger", "role": "trader"}
        self.assertEqual(workclass.sale_refused(miner, "m", self.MINE_SELL, {}), workclass.SALE)
        self.assertEqual(workclass.sale_refused(drone, "h", self.HUNT, {}), workclass.SALE)
        self.assertIsNone(workclass.sale_refused(drone, "h", dict(self.HUNT, gift_to="trader"), {}))        # the loot is given
        self.assertIsNone(workclass.sale_refused(miner, "m", dict(self.MINE_SELL, sell=[]), {}))
        self.assertIsNone(workclass.sale_refused(miner, "m", dict(self.MINE_SELL, gift={"to": "trader"}), {}))   # mine.py gives
        self.assertIsNone(workclass.sale_refused(miner, "m", dict(self.MINE_SELL, gift="trader"), {}))           # a bare word too
        self.assertIsNone(workclass.sale_refused(trader, "s", self.SELL, {}))
        self.assertEqual(workclass.sale_refused({"name": "hauler-1"}, "s", self.SELL, {}), workclass.SALE)
        self.assertIsNone(workclass.sale_refused(miner, "voidborn-sell", dict(self.SELL, once=True), {}))    # a mission paid once
        self.assertEqual(workclass.SALE, "sells: Trade's work (F23); give the goods to a trader with `gift`")
        workclass.STRICT = False
        self.assertIsNone(workclass.sale_refused(miner, "m", self.MINE_SELL, {}))

    def test_the_dry_run_counts_the_sales_per_class_and_per_admiral(self):
        routes = {"m": self.MINE_SELL, "h": self.HUNT, "g": dict(self.HUNT, gift_to="trader"), "s": self.SELL, "o": dict(self.HUNT, status="off"),
                  "mg": dict(self.MINE_SELL, gift={"to": "trader", "items": ["x"]})}
        rows, by_class, by_admiral = workclass.sales(routes, {"miner": ["m", "mg"], "drone": ["h"], "trader": ["s"]})
        self.assertEqual([r[0] for r in rows], ["h", "m"])
        self.assertEqual((by_class, by_admiral), ({"gather": 1, "hunt": 1}, {"Zero": 1, "Apophis": 1}))
        taken, by_class, by_admiral = workclass.narrowed({"s": self.SELL}, {"drone": ["s"], "trader": ["s"]})
        self.assertEqual((taken, by_class, by_admiral), ([("drone", "s", "sell")], {"sell": 1}, {"Apophis": 1}))

    def test_roles_and_show_print_both_states_when_asked(self):
        script = Path(__file__).resolve().parents[2] / "game" / "fleet" / "workclass.py"
        with tempfile.TemporaryDirectory() as folder:
            done = subprocess.run([sys.executable, "-I", "-B", str(script), "roles", "--strict", "--data", folder], stdout=subprocess.PIPE, text=True, timeout=60)
        self.assertIn("strict classes off:", done.stdout)
        self.assertIn("strict classes ON:", done.stdout)
        self.assertIn("trader    trade, sell, craft, once, deliver, fit, other", done.stdout)
        self.assertIn("miner     gather, once, sell, craft, fit, other", done.stdout)


if __name__ == "__main__":
    unittest.main()
