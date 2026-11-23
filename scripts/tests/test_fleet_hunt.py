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


class AloneTests(unittest.TestCase):
    """--alone: which strangers make a hunt leave a place without a fight (route field `alone`)."""

    def setUp(self):
        self.leave_reason = load("leave_reason")
        self.alone_mode = load("alone_mode")
        self.hostile_names = load("hostile_names")
        self.folder = tempfile.mkdtemp()
        self.own = {"drone-1", "miner-7", "Hades"}

    def near(self, names, pirates=0):
        return {"nearby": [{"username": n} for n in names], "pirate_count": pirates}

    def route(self, alone):
        path = os.path.join(self.folder, "hunt-x.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"id": "hunt-x", "kind": "hunt", "alone": alone}, fh)
        return path

    def test_true_leaves_for_any_ship_not_ours(self):
        # the rule since 2026-11-16: 61 of 161 drone hunts left so (2026-11-17 04:12 to 08:10 UTC)
        mode = self.alone_mode(self.route(True))
        self.assertEqual(mode, "strangers")
        self.assertIsNotNone(self.leave_reason(self.near(["miner-7", "Combat Drone 187"]), self.own, mode, set()))
        self.assertIsNone(self.leave_reason(self.near(["miner-7", "Hades"]), self.own, mode, set()))

    def test_pirates_stays_beside_a_stranger_and_leaves_for_a_pirate(self):
        mode = self.alone_mode(self.route("pirates"))
        self.assertEqual(mode, "pirates")
        self.assertIsNone(self.leave_reason(self.near(["Combat Drone 187", "VMan"]), self.own, mode, set()))
        why = self.leave_reason(self.near(["VMan"], pirates=1), self.own, mode, set())
        self.assertIn("pirate", why[1])

    def test_pirates_leaves_for_a_pilot_of_the_hostile_list(self):
        with open(os.path.join(self.folder, "h-vman.md"), "w", encoding="utf-8") as fh:
            fh.write("---\nname: vman\nkind: player\nusername: VMan\nstanding: hostile\n---\n")
        with open(os.path.join(self.folder, "n-other.md"), "w", encoding="utf-8") as fh:
            fh.write("---\nname: other\nusername: Other\nstanding: neutral\n---\n")
        hostile = self.hostile_names(self.folder)
        self.assertEqual(hostile, {"VMan"})
        why = self.leave_reason(self.near(["Other", "VMan"]), self.own, "pirates", hostile)
        self.assertIn("hostile", why[1])

    def test_a_missing_or_broken_route_file_keeps_the_strict_rule(self):
        self.assertEqual(self.alone_mode(os.path.join(self.folder, "none.json")), "strangers")
        with open(os.path.join(self.folder, "broken.json"), "w", encoding="utf-8") as fh:
            fh.write("[1, 2")
        self.assertEqual(self.alone_mode(os.path.join(self.folder, "broken.json")), "strangers")



class KeptGoodsTests(unittest.TestCase):
    """A hunt never sells what the reserve keeps (rule F24): four hunt runs sold 13 superfluid vials and a scout hunt 6
    caustic sacs that surplus.py held back (2026-11-17, errors.log ENT-095 and Military's entry of that evening)."""

    def setUp(self):
        import sys
        import types
        self.sys = sys
        self.saved = sys.modules.get("surplus")
        fake = types.ModuleType("surplus")
        fake.surplus = lambda data, root: {"rows": [
            {"id": "superfluid_vial", "short": 0, "reserved": 1, "surplus": 0},     # held back for another recipe
            {"id": "caustic_sac", "short": 384, "reserved": 45, "surplus": 0},      # short
            {"id": "crystal_melt", "short": 0, "reserved": 0, "surplus": 34},       # not in the reserve: for sale
            {"id": "creature_carapace", "short": 0, "reserved": 500, "surplus": 20},  # some to spare: for sale
        ]}
        sys.modules["surplus"] = fake
        self.kept_goods = load("kept_goods")
        self.saleable = load("saleable")

    def tearDown(self):
        if self.saved is None:
            self.sys.modules.pop("surplus", None)
        else:
            self.sys.modules["surplus"] = self.saved

    def test_the_reserve_keeps_what_is_short_or_held_back(self):
        kept = self.kept_goods("/nowhere", "/nowhere")
        self.assertEqual(set(kept), {"superfluid_vial", "caustic_sac"})

    def test_a_kept_good_is_never_offered_for_sale_and_ammo_neither(self):
        kept = self.kept_goods("/nowhere", "/nowhere")
        cargo = {"superfluid_vial": 6, "caustic_sac": 2, "crystal_melt": 3, "creature_carapace": 4, "iron_slug_case": 9}
        self.assertEqual(self.saleable(cargo, kept, {"iron_slug_case"}), {"crystal_melt": 3, "creature_carapace": 4})

    def test_no_reserve_read_keeps_nothing_back(self):
        def broken(data, root):
            raise OSError("no storage book")
        self.sys.modules["surplus"].surplus = broken
        self.assertEqual(self.kept_goods("/nowhere", "/nowhere"), {})

class ForeignRanchTests(unittest.TestCase):
    """A creature another faction ranches carries its tag in its name: never prey (2026-11-23,
    a drone hunted '[HEXC] Patina-Grazer' at a partner's base and was destroyed by its owner)."""

    def setUp(self):
        self.foreign_ranched = load("foreign_ranched")

    def test_a_creature_with_another_faction_tag_is_foreign_ranched(self):
        self.assertTrue(self.foreign_ranched({"name": "[HEXC] Patina-Grazer", "species": "patina_grazer"}))
        self.assertTrue(self.foreign_ranched({"name": "[IRLC] Belt-Grazer"}))

    def test_a_wild_creature_and_one_of_ours_are_not(self):
        self.assertFalse(self.foreign_ranched({"name": "Patina-Grazer", "species": "patina_grazer"}))
        self.assertFalse(self.foreign_ranched({"name": "[CLTV] Belt-Grazer"}))
        self.assertFalse(self.foreign_ranched({"species": "belt_grazer"}))
        self.assertFalse(self.foreign_ranched({"name": None}))


if __name__ == "__main__":
    unittest.main()
