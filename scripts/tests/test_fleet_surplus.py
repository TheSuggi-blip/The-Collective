"""game/fleet/surplus.py on a small catalog, storage book and order books in a temporary folder: the reserve met level by level, the surplus, where it lies and its bids. No engine, no network, no live data."""

import calendar
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "game" / "fleet" / "surplus.py"
CATALOG = {
    "version": "9.9.9",
    "items": [{"id": "iron_ore", "name": "Iron Ore", "category": "ore", "size": 1, "base_value": 5},
              {"id": "steel_plate", "name": "Steel Plate", "category": "refined", "size": 1, "base_value": 18},
              {"id": "frame", "name": "Frame", "category": "component", "size": 2, "base_value": 90},
              {"id": "polymer", "name": "Polymer", "category": "refined", "size": 1, "base_value": 27},
              {"id": "caustic_sac", "name": "Caustic Sac", "category": "misc", "size": 1, "base_value": 140},
              {"id": "gem", "name": "Gem", "category": "misc", "size": 1, "base_value": 50},
              {"id": "fuel_cell", "name": "Fuel Cell", "category": "consumable", "size": 1, "base_value": 43},
              {"id": "laser", "name": "Laser", "type": "weapon", "slot": "weapon", "size": 5, "base_value": 300}],
    "recipes": [{"id": "smelt", "inputs": [{"item_id": "iron_ore", "quantity": 10}], "outputs": [{"item_id": "steel_plate", "quantity": 1}], "hand_craftable": True,
                 "produced_by_facility_ids": []},
                {"id": "break_frame", "inputs": [{"item_id": "frame", "quantity": 1}], "outputs": [{"item_id": "steel_plate", "quantity": 2}], "hand_craftable": True,
                 "produced_by_facility_ids": []},
                {"id": "assemble_frame", "inputs": [{"item_id": "steel_plate", "quantity": 4}], "outputs": [{"item_id": "frame", "quantity": 1}], "hand_craftable": False,
                 "produced_by_facility_ids": ["frame_plant"]},
                {"id": "cook_polymer", "inputs": [{"item_id": "caustic_sac", "quantity": 3}], "outputs": [{"item_id": "polymer", "quantity": 2}], "hand_craftable": True,
                 "produced_by_facility_ids": []}],
    "facilities": [{"id": "lockbox", "name": "Lockbox", "level": 1, "build_cost": 1000, "build_materials": [{"item_id": "steel_plate", "quantity": 10}]},
                   {"id": "frame_rack", "name": "Frame Rack", "level": 1, "build_cost": 500, "build_materials": [{"item_id": "frame", "quantity": 2}]},
                   {"id": "vat", "name": "Vat", "level": 1, "build_cost": 10, "build_materials": [{"item_id": "polymer", "quantity": 4}]}],
    "ships": [{"id": "skiff", "name": "Skiff", "build_materials": [{"item_id": "frame", "quantity": 1}]}]}
BOOK = {"updated_at": "2026-11-16T18:30:00Z", "pilots": {"miner-1": {"read_at": "2026-11-16T18:20:00Z", "stations": {"home_base": {"iron_ore": 30}}}},
        "totals": {"by_station": {"home_base": {"iron_ore": 30, "steel_plate": 3, "gem": 5}, "far_base": {"iron_ore": 50, "steel_plate": 1, "laser": 2}},
                   "holds_by_member": {"Zero": {"iron_ore": 20}}}}
NOW = calendar.timegm(time.strptime("2026-11-16T18:30:00Z", "%Y-%m-%dT%H:%M:%SZ"))
HEAD = "kind\tid\tunits\tnote\n"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SurplusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="surplus-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        (self.root / "game").mkdir(parents=True)
        for folder in ("catalog", "stock", "market"):
            (self.data / folder).mkdir(parents=True)
        (self.data / "catalog" / "9.9.9.json").write_text(json.dumps(CATALOG), encoding="utf-8")
        self.book(BOOK["totals"])
        (self.data / "market" / "home_base.json").write_text(json.dumps({"base": "home_base", "system": "home_sys", "read_at": "2026-11-16T17:00:00Z", "items": [
            {"item_id": "iron_ore", "best_buy": 5, "best_buy_qty": 10}, {"item_id": "gem", "best_buy": 0, "best_buy_qty": 0}]}))
        (self.data / "market" / "far_base.json").write_text(json.dumps({"base": "far_base", "system": "far_sys", "read_at": "2026-11-16T18:00:00Z", "items": [
            {"item_id": "iron_ore", "best_buy": 7, "best_buy_qty": 15}, {"item_id": "steel_plate", "best_buy": 30, "best_buy_qty": 2}]}))
        (self.data / "market" / "ladders.json").write_text(json.dumps({"home_base": {"iron_ore": [1, 2]}}))     # the folder's other files are no order book
        self.mod = load(SCRIPT, "surplus_under_test")

    def book(self, totals):
        (self.data / "stock" / "storage.json").write_text(json.dumps(dict(BOOK, totals=totals)), encoding="utf-8")

    def targets(self, text):
        (self.root / "game" / "reserve.tsv").write_text(HEAD + text, encoding="utf-8")

    def result(self):
        return self.mod.surplus(str(self.data), str(self.root), now=NOW)

    def rows(self):
        return {r["id"]: r for r in self.result()["rows"]}

    def run_script(self, *args):
        return subprocess.run([sys.executable, "-I", "-B", str(SCRIPT)] + list(args) + ["--root", str(self.root), "--data", str(self.data)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env={"PATH": "/usr/bin:/bin"})

    def test_held_plates_cover_part_of_the_demand_and_ore_covers_the_rest(self):
        self.targets("facility\tlockbox\t1\tfaction storage\n")
        rows = self.rows()
        plate, ore = rows["steel_plate"], rows["iron_ore"]
        self.assertEqual((plate["demand"], plate["taken"], plate["make"], plate["recipe"], plate["how"], plate["short"]), (10, 4, 6, "smelt", "by hand", 0))
        self.assertEqual((plate["held"], plate["reserved"], plate["surplus"]), (4, 4, 0))
        self.assertEqual((ore["demand"], ore["taken"], ore["reserved"], ore["surplus"], ore["short"], ore["how"]), (60, 60, 60, 40, 0, "mined"))
        self.assertEqual(ore["why"], "for lockbox")
        self.assertEqual(rows["gem"]["why"], "")                                                   # nothing asks for it: all of it is free

    def test_short_is_found_at_the_raw_level_and_carried_up(self):
        self.book({"by_station": {"home_base": {"iron_ore": 10, "steel_plate": 3}, "far_base": {"iron_ore": 15, "steel_plate": 1}}, "holds_by_member": {}})
        self.targets("facility\tlockbox\t1\t\n")
        rows = self.rows()
        self.assertEqual((rows["iron_ore"]["demand"], rows["iron_ore"]["reserved"], rows["iron_ore"]["surplus"], rows["iron_ore"]["short"]), (60, 25, 0, 35))
        self.assertEqual(rows["steel_plate"]["short"], 4)                                         # 25 ore make 2 of the 6 plates still missing
        res = self.result()
        self.assertEqual((res["totals"]["short_raw"], res["totals"]["short_raw_items"], res["totals"]["short_items"]), (35, 1, 2))

    def test_demand_from_several_targets_is_netted_once_and_a_facility_recipe_is_still_followed(self):
        self.targets("facility\tlockbox\t1\t\nfacility\tframe_rack\t1\t\nitem\tsteel_plate\t2\tspare plates\n")
        rows = self.rows()
        frame, plate, ore = rows["frame"], rows["steel_plate"], rows["iron_ore"]
        self.assertEqual((frame["demand"], frame["make"], frame["recipe"], frame["how"]), (2, 2, "assemble_frame", "facility"))   # never break_frame: a circle
        self.assertEqual((plate["demand"], plate["taken"], plate["make"]), (20, 4, 16))           # 10 + 8 for the frames + 2 on hand, against the 4 held once
        self.assertEqual((ore["demand"], ore["reserved"], ore["surplus"], ore["short"]), (160, 100, 0, 60))
        self.assertEqual((plate["short"], frame["short"]), (6, 1))                                # 100 ore make 10 plates, shared in proportion: one frame
        self.assertEqual(ore["why"], "for frame_rack, lockbox, steel_plate on hand")
        self.assertEqual(self.result()["totals"]["fees"], 1500)

    def test_what_another_recipe_could_make_of_our_stock_is_held_back_not_surplus(self):
        # the walk makes plates from ore (smelt); break_frame makes 2 plates from 1 frame. The live case: 94,898 copper ore read as
        # surplus while copper piping was short, because the walk made piping from curd and never looked at draw_copper_piping.
        self.book({"by_station": {"home_base": {"iron_ore": 20, "frame": 9, "gem": 5}}, "holds_by_member": {}})
        self.targets("facility\tlockbox\t1\tfaction storage\n")
        rows = self.rows()
        plate, frame = rows["steel_plate"], rows["frame"]
        self.assertEqual((plate["demand"], plate["make"], plate["short"]), (10, 10, 8))                # 20 ore smelt 2 plates: 8 short
        self.assertEqual((frame["held"], frame["back"], frame["reserved"], frame["surplus"]), (9, 4, 4, 5))       # 4 frames would break into the 8
        self.assertEqual(frame["why"], "held back: another recipe could make steel_plate (break_frame)")
        self.assertEqual((rows["gem"]["back"], rows["gem"]["surplus"]), (0, 5))
        self.assertIn("Held back, not surplus", self.run_script("reserve").stdout)
        self.book({"by_station": {"home_base": {"iron_ore": 100, "frame": 9}}, "holds_by_member": {}})   # nothing short: nothing held back
        self.assertEqual((self.rows()["frame"]["back"], self.rows()["frame"]["surplus"]), (0, 9))
        self.assertNotIn("Held back, not surplus", self.run_script("reserve").stdout)

    def test_an_item_no_recipe_makes_is_short_as_bought_or_hunted(self):
        self.targets("facility\tvat\t1\t\nhull\tskiff\t1\t\n")
        rows = self.rows()
        self.assertEqual((rows["polymer"]["make"], rows["caustic_sac"]["demand"], rows["caustic_sac"]["how"], rows["caustic_sac"]["short"], rows["polymer"]["short"]),
                         (4, 6, "no recipe", 6, 4))
        self.assertEqual((rows["frame"]["demand"], rows["frame"]["how"]), (1, "facility"))

    def test_how_a_row_is_had(self):
        self.targets("item\tsteel_plate\t3\t\n")
        rows = self.rows()
        self.assertEqual((rows["steel_plate"]["how"], rows["steel_plate"]["make"], rows["steel_plate"]["reserved"], rows["steel_plate"]["surplus"]), ("stock", 0, 3, 1))
        self.assertEqual((rows["iron_ore"]["how"], rows["iron_ore"]["demand"], rows["gem"]["how"], rows["laser"]["how"]), ("mined", 0, "no recipe", "no recipe"))
        self.assertNotIn("frame", rows)                                                           # neither held nor asked for

    def test_surplus_is_never_negative_and_never_more_than_held(self):
        for text in ("", "facility\tlockbox\t9\t\nkeep\tgem\t99\t\n", "facility\tframe_rack\t3\t\nkeepkind\tmodule\tall\t\n", "item\tiron_ore\t5000\t\n"):
            self.targets(text)
            for r in self.result()["rows"]:
                self.assertTrue(0 <= r["surplus"] <= r["held"] and 0 <= r["reserved"] <= r["held"] and r["surplus"] + r["reserved"] == r["held"], (text, r))
                self.assertEqual(sum(p["units"] for p in r["at"]), r["surplus"])

    def test_keep_with_a_number_keep_all_and_keepkind(self):
        cases = (("keep\tgem\t3\t\n", 3, 2), ("keep\tgem\t10\t\n", 5, 0), ("keep\tgem\tall\t\n", 5, 0), ("keep\tgem\t2\t\nkeep\tgem\t2\t\n", 4, 1))
        for text, reserved, free in cases:
            self.targets(text)
            gem = self.rows()["gem"]
            self.assertEqual((gem["reserved"], gem["surplus"]), (reserved, free), text)
        self.assertEqual(self.result()["warnings"], ["line 3: keep gem stands on line 2 too: both count"])
        self.targets("keepkind\tmodule\tall\tmodules are kept for fitting\nfacility\tlockbox\t1\t\nkeep\tiron_ore\t30\t\n")
        rows = self.rows()
        self.assertEqual((rows["laser"]["reserved"], rows["laser"]["surplus"], rows["laser"]["why"]), (2, 0, "keepkind module"))
        self.assertEqual((rows["iron_ore"]["reserved"], rows["iron_ore"]["surplus"], rows["iron_ore"]["why"]), (90, 10, "for lockbox; keep 30"))   # keep adds to the build's reserve

    def test_an_unknown_id_or_kind_is_an_error_in_check_and_skipped_in_show(self):
        self.targets("facility\tnope\t1\t\nkeep\tghost\t2\t\nkeepkind\tspaceship\tall\t\nfrigate\tlockbox\t1\t\nfacility\tlockbox\tx\t\nkeepkind\tmodule\t3\t\nfacility\tlockbox\t1\t\n")
        res = self.result()
        self.assertEqual(len(res["errors"]), 6)
        self.assertEqual(res["errors"][0], "line 2: no facility `nope` in the catalog 9.9.9")
        self.assertEqual([t["id"] for t in res["targets"]], ["lockbox"])
        self.assertEqual(self.rows()["iron_ore"]["reserved"], 60)                                 # the good line still counts
        done = self.run_script("check")
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("ERROR line 3: no item `ghost` in the catalog 9.9.9", done.stdout)
        self.assertIn("ERROR line 4: no kind of item `spaceship`", done.stdout)
        self.assertIn("ERROR line 5: no kind of target `frigate`", done.stdout)
        self.assertIn("Errors: 6 | Warnings: 0", done.stdout)
        shown = self.run_script("show")
        self.assertEqual(shown.returncode, 0, shown.stdout)
        self.assertIn("(1 targets, 6 lines skipped)", shown.stdout.split("\n")[0])
        self.assertIn("NOTE line 2: no facility `nope` in the catalog 9.9.9: skipped", shown.stdout)
        self.targets("facility\tlockbox\t1\t\n")
        self.assertEqual((self.run_script("check").returncode, self.run_script("check").stdout.split("\n")[1]), (0, "Errors: 0 | Warnings: 0"))
        (self.root / "game" / "reserve.tsv").write_text("facility\tlockbox\t1\t\n", encoding="utf-8")
        self.assertIn("the header", self.result()["errors"][0])

    def test_without_a_reserve_file_everything_held_is_surplus(self):
        res = self.result()
        self.assertFalse(res["present"])
        self.assertTrue(all(r["surplus"] == r["held"] for r in res["rows"]))
        self.assertEqual(res["totals"]["surplus"], 111)
        for verb in ("show", "reserve", "check"):
            done = self.run_script(verb)
            self.assertEqual(done.returncode, 0, done.stdout)
            self.assertIn("NO RESERVE FILE game/reserve.tsv: no targets, nothing kept, everything held is surplus", done.stdout.split("\n")[0])

    def test_the_reserve_is_taken_from_the_place_with_the_most_and_the_rest_is_surplus_where_it_lies(self):
        self.targets("facility\tlockbox\t1\t\n")
        ore = self.rows()["iron_ore"]
        self.assertEqual({p["place"]: p["units"] for p in ore["at"]}, {"home_base": 20, "hold": 20})   # 60 reserved: 50 at far_base, then 10 at home_base
        self.assertEqual(self.mod.split({"a": 5, "hold": 5, "b": 9}, 10), [("hold", 5), ("a", 4)])    # 9 from b, then a tie: a station gives before the holds
        self.assertEqual(self.mod.split({"a": 5}, 0), [("a", 5)])

    def test_bids_best_anywhere_at_the_place_none_and_worth_capped_by_depth(self):
        self.targets("facility\tlockbox\t1\t\n")
        rows = self.rows()
        ore = rows["iron_ore"]
        self.assertEqual((ore["bid"], ore["bid_units"], ore["bid_at"]), (7, 15, "far_base"))
        self.assertEqual(ore["worth_at_bid"], 15 * 7)                                              # 40 surplus, but the bid takes 15
        self.assertEqual({p["place"]: (p["bid"], p["bid_units"]) for p in ore["at"]}, {"home_base": (5, 10), "hold": (None, 0)})
        self.assertEqual((rows["gem"]["bid"], rows["gem"]["worth_at_bid"], rows["gem"]["surplus"]), (None, 0, 5))
        self.assertEqual((rows["steel_plate"]["bid"], rows["steel_plate"]["worth_at_bid"]), (30, 0))   # a bid, but nothing free to sell
        self.assertEqual(self.result()["rows"][0]["id"], "iron_ore")                              # the most worth at a bid first
        books, read, oldest = self.mod.order_books(str(self.data))
        best = self.mod.craftbook.bids(str(self.data))
        for item, (bid, units, base) in best.items():                                              # one definition of a bid: the best per station is craftbook's best
            self.assertEqual(books[base][item], (bid, units))
            self.assertEqual(max(here[item][0] for here in books.values() if item in here), bid)
        self.assertEqual((read, oldest), (2, "2026-11-16T17:00:00Z"))

    def test_the_first_lines_name_what_the_answer_rests_on(self):
        self.targets("facility\tlockbox\t1\t\n")
        rests = "reserve file game/reserve.tsv (1 targets) | storage book of 2026-11-16T18:30:00Z | catalog 9.9.9 | 2 order books, the oldest read 2026-11-16T17:00:00Z ("
        firsts = {}
        for verb in ("show", "reserve", "check"):
            done = self.run_script(verb)
            self.assertEqual(done.returncode, 0, done.stdout)
            firsts[verb] = done.stdout.split("\n")[0]
            self.assertIn(rests, firsts[verb])
        self.assertTrue(firsts["show"].startswith("SURPLUS | "))
        self.assertTrue(firsts["reserve"].startswith("RESERVE | "))
        self.assertTrue(firsts["check"].startswith("CHECK game/reserve.tsv | "))
        self.assertEqual(self.result()["books"]["age"], "90 min old")
        shown = self.run_script("show").stdout
        self.assertIn("Gem (gem)", shown)
        self.assertIn("no bid", shown)
        self.assertIn("7 cr x 15 at Far Base", shown)
        self.assertEqual(shown.rstrip("\n").split("\n")[-1], self.mod.RULE)
        item = self.run_script("show", "--item", "iron_ore").stdout
        self.assertIn("reserved for lockbox", item)
        self.assertRegex(item, r"Home Base +20 surplus here \| bid here: 5 cr x 10")
        self.assertRegex(item, r"In the holds of our ships +20 surplus here \| bid here: -- \(not at a station\)")
        reserve = self.run_script("reserve").stdout
        self.assertIn("facility lockbox x 1: 10 steel_plate | fee 1,000 cr", reserve)
        self.assertRegex(reserve, r"steel_plate +1 smelt, by hand +4 +10 +4 +6 +0")
        self.assertIn("SUM | 2 items asked for | 104 held, 70 demand, 64 from stock, 6 to make | SHORT 0 units of 0 items", reserve)
        self.assertNotIn("miner-1", shown + item + reserve)                                         # a pilot is never named
        self.assertIn("Laser (laser)", self.run_script("show", "--kind", "module").stdout)
        self.assertNotIn("Gem (gem)", self.run_script("show", "--kind", "module").stdout)

    def press(self):
        """A newer catalog with a second recipe of polymer from the ore we hold; the rule keeps cook_polymer (a tie, then the
        id), which takes caustic sacs nobody holds: the live case of copper piping from curd (2026-11-16)."""
        more = dict(CATALOG, version="9.9.10", recipes=CATALOG["recipes"] + [{"id": "press_polymer", "inputs": [{"item_id": "iron_ore", "quantity": 5}],
                                                                              "outputs": [{"item_id": "polymer", "quantity": 1}], "hand_craftable": True,
                                                                              "produced_by_facility_ids": []}])
        (self.data / "catalog" / "9.9.10.json").write_text(json.dumps(more), encoding="utf-8")

    def choices(self, text):
        (self.root / "game" / "reserve-recipes.tsv").write_text("# chosen recipes\nitem\trecipe\tnote\n" + text, encoding="utf-8")

    def test_a_chosen_recipe_changes_what_the_reserve_names(self):
        self.press()
        self.targets("facility\tvat\t1\t\n")
        rows = self.rows()
        self.assertEqual((rows["polymer"]["recipe"], rows["caustic_sac"]["demand"], rows["iron_ore"]["demand"]), ("cook_polymer", 6, 0))
        self.assertIn("polymer: recipe cook_polymer (1 of 2; choose another in game/reserve-recipes.tsv)", self.run_script("reserve").stdout)
        self.choices("polymer\tpress_polymer\tLogistics, 2026-11-16; not flown yet\n")
        rows = self.rows()
        self.assertEqual((rows["polymer"]["recipe"], rows["polymer"]["make"], rows["iron_ore"]["demand"], rows["iron_ore"]["short"]), ("press_polymer", 4, 20, 0))
        self.assertNotIn("caustic_sac", rows)                                                      # neither held nor asked for any more
        reserve = self.run_script("reserve").stdout
        self.assertIn("polymer: recipe press_polymer (1 of 2; chosen in game/reserve-recipes.tsv line 3)", reserve)
        self.assertTrue(reserve.split("\n")[0].endswith(" | recipes chosen in game/reserve-recipes.tsv: 1"))
        self.assertRegex(reserve, r"polymer +1 press_polymer, by hand +0 +4 +0 +4 +0")
        self.assertNotIn("caustic_sac", reserve)

    def test_no_choices_file_is_today_s_answer(self):
        self.press()
        self.targets("facility\tvat\t1\t\nfacility\tlockbox\t1\t\nhull\tskiff\t1\t\n")
        plain = self.result()
        self.assertFalse(plain["choices"]["present"])
        before = self.run_script("reserve").stdout
        self.assertNotIn("recipes chosen", before.split("\n")[0])                                  # the first line as it always was
        self.choices("")                                                                           # the header alone: no choice
        empty = self.result()
        self.assertEqual((empty["rows"], empty["totals"]), (plain["rows"], plain["totals"]))
        after = self.run_script("reserve").stdout.split("\n")
        self.assertEqual(after[1:], before.split("\n")[1:])                                       # every line under the first, byte for byte
        self.assertTrue(after[0].endswith(" | recipes chosen in game/reserve-recipes.tsv: 0"))
        self.assertEqual(after[0].rsplit(" (", 1)[0], before.split("\n")[0].rsplit(" (", 1)[0])   # the first line up to the books' age, which runs on

    def test_a_bad_row_is_skipped_and_fails_the_gate(self):
        self.press()
        self.targets("facility\tvat\t1\t\n")
        plain = self.result()["rows"]
        self.choices("ghost\tpress_polymer\tx\npolymer\tno_recipe\tx\npolymer\tsmelt\tx\n")
        res = self.result()
        self.assertEqual(res["rows"], plain)                                                       # skipped: the rule's recipe stands
        self.assertEqual(len(res["choices"]["errors"]), 3)
        done = self.run_script("check")
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("ERROR game/reserve-recipes.tsv line 3: no item `ghost` in the catalog 9.9.10", done.stdout)
        self.assertIn("ERROR game/reserve-recipes.tsv line 4: no recipe `no_recipe` in the catalog 9.9.10 (the recipes of polymer: cook_polymer, press_polymer)", done.stdout)
        self.assertIn("ERROR game/reserve-recipes.tsv line 5: the recipe `smelt` does not make polymer (it makes steel_plate;", done.stdout)
        self.assertIn("Errors: 3 | Warnings: 0", done.stdout)
        shown = self.run_script("reserve")
        self.assertEqual(shown.returncode, 0, shown.stdout)
        self.assertIn("NOTE game/reserve-recipes.tsv line 4: no recipe `no_recipe`", shown.stdout)
        self.assertIn("recipes chosen in game/reserve-recipes.tsv: 0, 3 rows skipped", shown.stdout.split("\n")[0])
        (self.root / "game" / "reserve.tsv").unlink()                                               # no reserve file: the choices are still the gate's
        self.assertEqual(self.run_script("check").returncode, 1)
        self.choices("polymer\tpress_polymer\tgood\n")
        self.assertEqual(self.run_script("check").returncode, 0)

    # round r21: game/reserve.tsv names per good a `max` and a `min` (the dispatcher's pull rule, game/fleet/pull.py); they reserve nothing
    def test_max_and_min_lines_are_read_and_change_no_figure(self):
        self.targets("facility\tlockbox\t1\t\n")
        before = self.rows()
        self.targets("facility\tlockbox\t1\t\nmax\tiron_ore\t300\tthe most to gather\nmin\tiron_ore\t0\tgathered again only when none is left\n"
                     "max\tsteel_plate\t20\t\nmax\tsteel_plate\t25\tthe later line counts\n")
        res = self.result()
        self.assertEqual(res["errors"], [])
        self.assertEqual(res["levels"], {"iron_ore": {"max": 300, "min": 0}, "steel_plate": {"max": 25}})
        self.assertEqual(res["warnings"], ["line 6: max steel_plate stands on line 5 too: this one counts"])
        self.assertEqual({k: (r["reserved"], r["surplus"], r["demand"], r["short"]) for k, r in self.rows().items()},
                         {k: (r["reserved"], r["surplus"], r["demand"], r["short"]) for k, r in before.items()})
        done = self.run_script("reserve")
        self.assertIn("  max iron_ore 300: the pull level of the dispatcher's pull rule (pull.py) | the most to gather", done.stdout)
        self.assertEqual(self.run_script("check").returncode, 0)

    def test_a_level_line_breaks_its_rules_alone(self):
        self.targets("max\tiron_ore\t0\t\nmin\tiron_ore\tx\t\nmax\tghost\t5\t\nmin\tiron_ore\t3\t\n")
        res = self.result()
        self.assertEqual(res["errors"], ["line 2: units must be a whole number above 0, not `0`", "line 3: units must be a whole number 0 or more, not `x`",
                                         "line 4: no item `ghost` in the catalog 9.9.9"])
        self.assertEqual(res["levels"], {"iron_ore": {"min": 3}})

    def test_the_real_reserve_file_reads_without_an_error(self):
        targets, errors, _warnings, present = self.mod.read_targets(REPO / "game" / "reserve.tsv", None)
        self.assertTrue(present)
        self.assertEqual(errors, [])
        self.assertTrue(targets)


if __name__ == "__main__":
    unittest.main()
