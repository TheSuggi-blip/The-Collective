"""scripts/catalog-index.py and game/fleet/craftbook.py on a small catalog: the folder that is built, its gate, and what a thing takes. No engine, no network."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
CATALOG = {
    "version": "9.9.9",
    "items": [{"id": "iron_ore", "name": "Iron Ore", "category": "ore", "size": 1, "base_value": 5},
              {"id": "steel_plate", "name": "Steel Plate", "category": "refined", "size": 1, "base_value": 18},
              {"id": "frame", "name": "Frame", "category": "component", "size": 2, "base_value": 90},
              {"id": "outpost_kit", "name": "Outpost Kit", "category": "component", "size": 50, "base_value": 9000},
              {"id": "laser", "name": "Laser", "type": "weapon", "slot": "weapon", "cpu_usage": 2, "power_usage": 5, "size": 5, "base_value": 300, "damage": 9}],
    "recipes": [{"id": "smelt", "name": "Smelt", "category": "Refining", "inputs": [{"item_id": "iron_ore", "quantity": 10}], "outputs": [{"item_id": "steel_plate", "quantity": 1}],
                 "crafting_time": 1, "hand_craftable": True, "produced_by_facility_ids": []},
                {"id": "break_frame", "name": "Break a Frame", "category": "Refining", "inputs": [{"item_id": "frame", "quantity": 1}], "outputs": [{"item_id": "steel_plate", "quantity": 2}],
                 "crafting_time": 1, "hand_craftable": True, "produced_by_facility_ids": []},
                {"id": "assemble_frame", "name": "Assemble Frame", "category": "Components", "inputs": [{"item_id": "steel_plate", "quantity": 4}], "outputs": [{"item_id": "frame", "quantity": 1}],
                 "crafting_time": 2, "hand_craftable": False, "facility_only": True, "produced_by_facility_ids": ["frame_plant"]},
                {"id": "assemble_outpost_kit", "name": "Assemble Outpost Kit", "category": "Shipbuilding", "inputs": [{"item_id": "frame", "quantity": 2}],
                 "outputs": [{"item_id": "outpost_kit", "quantity": 1}], "crafting_time": 9, "hand_craftable": False, "facility_only": True, "produced_by_facility_ids": ["kit_plant"]}],
    "facilities": [{"id": "frame_plant", "name": "Frame Plant", "category": "production", "level": 1, "recipe_id": "assemble_frame", "build_cost": 1000, "build_time": 5, "labor_cost": 2,
                    "build_materials": [{"item_id": "steel_plate", "quantity": 5}]},
                   {"id": "kit_plant", "name": "Kit Plant", "category": "production", "level": 2, "recipe_id": "assemble_outpost_kit", "build_cost": 600000, "build_time": 9, "labor_cost": 3,
                    "build_materials": [{"item_id": "frame", "quantity": 3}]},
                   {"id": "lockbox", "name": "Lockbox", "category": "faction", "level": 1, "build_cost": 200000, "build_time": 5, "labor_cost": 5, "faction_service_type": "faction_storage",
                    "build_materials": [{"item_id": "steel_plate", "quantity": 200}]}],
    "ships": [{"id": "skiff", "name": "Skiff", "faction": "voidborn", "class": "Miner", "category": "Industrial", "tier": 2, "piloting_required": 10, "shipyard_tier": 1, "base_hull": 90,
               "base_shield": 50, "base_armor": 1, "base_speed": 2, "base_fuel": 100, "cargo_capacity": 80, "cpu_capacity": 20, "power_capacity": 30, "weapon_slots": 1,
               "defense_slots": 1, "utility_slots": 2, "build_time": 3, "build_materials": [{"item_id": "frame", "quantity": 2}], "default_modules": ["laser"]}],
    "skills": [{"id": "mining", "category": "Industry", "max_level": 100, "description": "More ore per pull."}]}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="catalog-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        (self.root / "game").mkdir(parents=True)
        for folder in ("catalog", "stock", "market", "fleet"):
            (self.data / folder).mkdir(parents=True)
        self.source = self.data / "catalog" / "9.9.9.json"
        self.source.write_text(json.dumps(CATALOG), encoding="utf-8")

    def run_index(self, *args):
        return subprocess.run([sys.executable, "-B", str(REPO / "scripts" / "catalog-index.py"), "--root", str(self.root), "--catalog", str(self.source)] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def text(self, name):
        return (self.root / "game" / "catalog" / name).read_text(encoding="ascii")


class IndexTests(Tree):
    def test_a_master_index_with_sub_indexes_is_built_and_kept_current(self):
        self.assertEqual(self.run_index("--check").returncode, 1)                                 # nothing there yet
        self.assertIn("game/catalog: written (13 files, 0 removed), catalog 9.9.9", self.run_index().stdout)
        self.assertEqual((self.run_index("--check").returncode, self.run_index().stdout), (0, "game/catalog: current\n"))
        master = self.text("master-index.md")
        self.assertIn("| [Refining](recipes/refining.md) | 2 | 2 | 0 |", master)                   # a group's name leads into its sub-index
        self.assertIn("| [voidborn](ships/voidborn.md) | 1 | 2: 1 |", master)
        self.assertIn("The Piloting a tier needs: tier 2: Piloting 10.", master)
        self.assertIn("| `smelt` | steel_plate x 1 | iron_ore x 10 | by hand | 1 |", self.text("recipes/refining.md"))
        self.assertIn("| `assemble_frame` | frame x 1 | steel_plate x 4 | in: frame_plant | 2 |", self.text("recipes/components.md"))
        self.assertIn("| An outpost | `outpost_kit` | frame x 2 | `kit_plant` | 2 | 600,000 | frame x 3 |", self.text("facilities.md"))
        self.assertIn("| `lockbox` | 1 | faction_storage | -- | 200,000 | 5 | steel_plate x 200 | -- |", self.text("facilities.md"))
        self.assertIn("smelt\tSmelt\tRefining\tsteel_plate x 1\tiron_ore x 10\t1\tyes", self.text("tables/recipes.tsv"))
        first = master.split("\nid: ")[1].split("\n")[0]
        changed = dict(CATALOG, version="9.9.10", recipes=[r for r in CATALOG["recipes"] if r["category"] != "Components"])
        self.source.write_text(json.dumps(changed), encoding="utf-8")
        self.assertEqual(self.run_index("--check").returncode, 1)                                 # a new release: stale
        self.assertIn("1 removed", self.run_index().stdout)                                       # the category that is gone takes its file with it
        self.assertFalse((self.root / "game" / "catalog" / "recipes" / "components.md").exists())
        self.assertEqual(self.text("master-index.md").split("\nid: ")[1].split("\n")[0], first)   # the id is kept

    def test_without_a_catalog_nothing_is_checked_or_written(self):
        self.source.unlink()
        done = subprocess.run([sys.executable, "-B", str(REPO / "scripts" / "catalog-index.py"), "--root", str(self.root), "--catalog", str(self.source), "--check"],
                              stdout=subprocess.PIPE, text=True)
        self.assertEqual((done.returncode, done.stdout), (0, "game/catalog: no catalog on disk: not checked and not written\n"))

    def test_the_real_folder_is_current_with_the_catalog_on_disk(self):
        done = subprocess.run([sys.executable, "-B", str(REPO / "scripts" / "catalog-index.py"), "--check"], stdout=subprocess.PIPE, text=True)
        self.assertEqual(done.returncode, 0, done.stdout)


class CraftbookTests(Tree):
    def setUp(self):
        super().setUp()
        self.book = load(REPO / "game" / "fleet" / "craftbook.py", "craftbook_under_test")
        (self.data / "stock" / "storage.json").write_text(json.dumps({"updated_at": "now", "pilots": {
            "miner-1": {"stations": {"home_base": {"iron_ore": 25}}}, "drone-1": {"stations": {"home_base": {"iron_ore": 9}}}}}))
        (self.data / "market" / "home_base.json").write_text(json.dumps({"base": "home_base", "items": [{"item_id": "steel_plate", "best_buy": 30, "best_buy_qty": 1}]}))
        self.cat = self.book.load(str(self.data))

    def test_what_a_thing_takes_follows_the_recipe_nearest_to_the_ore(self):
        steps, raw = {}, {}
        self.book.expand(self.cat, "outpost_kit", 1, steps, raw)
        self.assertEqual({item: (units, runs, recipe["id"]) for item, (units, runs, recipe, _depth) in steps.items()},
                         {"outpost_kit": (1, 1, "assemble_outpost_kit"), "frame": (2, 2, "assemble_frame"), "steel_plate": (8, 8, "smelt")})   # never `break_frame`: a circle
        self.assertEqual(raw, {"iron_ore": 80})

    def test_the_inventory_adds_storage_and_holds_by_kind_of_item_and_by_station(self):
        book = {"updated_at": "2026-11-16T18:00:00Z", "pilots": {"miner-1": {"read_at": "2026-11-16T17:10:00Z", "stations": {"home_base": {"iron_ore": 25}}},
                                                                 "drone-1": {"read_at": "2026-11-16T17:40:00Z", "stations": {"far_base": {"laser": 2}}},
                                                                 "drone-2": {"read_at": "2026-11-16T17:50:00Z", "error": "timeout"}},
                "totals": {"by_station": {"home_base": {"iron_ore": 34, "steel_plate": 6, "ghost_item": 3}, "far_base": {"laser": 2, "iron_ore": 1}, "a" * 32: {"frame": 1}},
                           "holds_by_member": {"Zero": {"iron_ore": 5, "frame": 0}, "Apophis": {"iron_ore": 10}}}}
        (self.data / "stock" / "storage.json").write_text(json.dumps(book))
        (self.data / "market" / ("a" * 32 + ".json")).write_text(json.dumps({"base": "a" * 32, "system": "far_system", "items": []}))
        inv = self.book.inventory(str(self.data))
        self.assertEqual((inv["written"], inv["pilots"], inv["oldest"], inv["catalog"]), ("2026-11-16T18:00:00Z", 2, "2026-11-16T17:10:00Z", "9.9.9"))
        self.assertEqual(inv["total"], {"items": 5, "units": 62, "worth": 50 * 5 + 6 * 18 + 2 * 300 + 1 * 90})        # an item the catalog lacks is worth 0
        self.assertEqual([(g["key"], g["items"], g["units"], g["worth"]) for g in inv["groups"]],
                         [("raw", 1, 50, 250), ("refined", 1, 6, 108), ("component", 1, 1, 90), ("module", 1, 2, 600), ("unknown", 1, 3, 0)])
        ore = inv["groups"][0]["rows"][0]
        self.assertEqual((ore["units"], ore["stored"], ore["held"], ore["at"]), (50, 35, 15, {"home_base": 34, "far_base": 1, "hold": 15}))
        self.assertEqual([(s["base"], s["name"], s["units"], s["worth"]) for s in inv["stations"]],
                         [("far_base", "Far Base", 3, 605), ("home_base", "Home Base", 43, 278), ("a" * 32, "A player's station in far_system", 1, 90),
                          ("hold", "In the holds of our ships", 15, 75)])                                  # by what lies there; the holds last
        self.assertEqual(sum(r["units"] for s in inv["stations"] for r in s["rows"]), inv["total"]["units"])        # every unit stands in one place
        run = lambda *args: subprocess.run([sys.executable, "-I", "-B", str(REPO / "game" / "fleet" / "craftbook.py"), "inventory"] + list(args) + ["--data", str(self.data)],
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env={"FLEET_MEMBER": "Unity", "PATH": "/usr/bin:/bin"}).stdout
        self.assertIn("TOTAL 5 kinds of item, 62 units, worth 1,048 cr", run())
        self.assertIn("Raw materials (ores, ice, gas) | 1 kinds, 50 units, worth 250", run())
        self.assertIn("Far Base (far_base) | 2 kinds, 3 units, worth 605", run("stations"))
        self.assertIn("Iron Ore (iron_ore): 50 units, 35 in storage, 15 in the holds", run("--item", "iron_ore"))
        self.assertIn("no outpost_kit in storage or in a hold", run("--item", "outpost_kit"))
        (self.data / "stock" / "storage.json").unlink()
        self.assertEqual(self.book.inventory(str(self.data))["total"], {"items": 0, "units": 0, "worth": 0})
        self.assertIn("no storage book yet", run())

    def choices(self, text):
        """The repository's game/reserve-recipes.tsv in the test's own root; None takes it away."""
        path = self.root / "game" / "reserve-recipes.tsv"
        if text is None:
            path.unlink(missing_ok=True)
        else:
            path.write_text("# chosen recipes\nitem\trecipe\tnote\n" + text, encoding="utf-8")

    def salvage(self):
        """The catalog with a third recipe of steel_plate from a creature good no recipe makes: the rule takes it (a tie on
        the level and the inputs, then the id), as it took verdigris_smelting for copper piping (2026-11-16)."""
        more = dict(CATALOG, version="9.9.10", items=CATALOG["items"] + [{"id": "scrap_hide", "name": "Scrap Hide", "category": "misc", "size": 1, "base_value": 7}],
                    recipes=CATALOG["recipes"] + [{"id": "press_hide_plate", "name": "Press Hide Plate", "category": "Refining", "inputs": [{"item_id": "scrap_hide", "quantity": 3}],
                                                   "outputs": [{"item_id": "steel_plate", "quantity": 2}], "crafting_time": 1, "hand_craftable": True, "produced_by_facility_ids": []}])
        (self.data / "catalog" / "9.9.10.json").write_text(json.dumps(more), encoding="utf-8")

    def needs(self, *args):
        return subprocess.run([sys.executable, "-I", "-B", str(REPO / "game" / "fleet" / "craftbook.py")] + list(args) + ["--data", str(self.data), "--root", str(self.root)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env={"FLEET_MEMBER": "Unity", "PATH": "/usr/bin:/bin"})

    def test_a_chosen_recipe_is_what_needs_follows_and_every_answer_names_the_recipe_taken(self):
        self.salvage()
        cat = self.book.choose(self.book.load(str(self.data)), str(self.root))         # no file: the rule's recipe
        steps, raw = {}, {}
        self.book.expand(cat, "steel_plate", 4, steps, raw)
        self.assertEqual(({i: s[2]["id"] for i, s in steps.items()}, raw), ({"steel_plate": "press_hide_plate"}, {"scrap_hide": 6}))
        self.assertEqual(cat["choices"]["present"], False)
        before = self.needs("needs", "steel_plate", "4")
        self.assertIn("steel_plate: recipe press_hide_plate (1 of 3; choose another in game/reserve-recipes.tsv)", before.stdout)
        self.choices("steel_plate\tsmelt\tLogistics, 2026-11-16; flown\n")
        cat = self.book.choose(self.book.load(str(self.data)), str(self.root))
        steps, raw = {}, {}
        self.book.expand(cat, "steel_plate", 4, steps, raw)
        self.assertEqual(({i: s[2]["id"] for i, s in steps.items()}, raw), ({"steel_plate": "smelt"}, {"iron_ore": 40}))
        after = self.needs("needs", "steel_plate", "4")
        self.assertEqual(after.returncode, 0, after.stdout)
        self.assertIn("4 steel_plate <- smelt x 4, by hand", after.stdout)
        self.assertIn("steel_plate: recipe smelt (1 of 3; chosen in game/reserve-recipes.tsv line 3)", after.stdout)
        self.assertNotIn("scrap_hide", after.stdout)
        built = self.needs("build", "frame_plant")                                                  # build breaks down by the same recipe
        self.assertIn("5 steel_plate <- smelt x 5", built.stdout)
        item = self.needs("item", "steel_plate").stdout                                              # every recipe with its id and inputs, the followed one marked
        self.assertIn("  press_hide_plate: 2 steel_plate <- 3 scrap_hide | by hand\n", item)
        self.assertIn("  break_frame: 2 steel_plate <- 1 frame | by hand\n", item)
        self.assertIn("  smelt: 1 steel_plate <- 10 iron_ore | by hand | <- every list of needs follows this one (chosen in game/reserve-recipes.tsv line 3)", item)
        self.assertIn("to follow another: a row `steel_plate<TAB><recipe id><TAB>", item)

    def test_no_file_or_an_empty_one_is_today_s_answer_and_a_bad_row_is_skipped_with_a_note(self):
        self.salvage()
        plain = self.needs("needs", "outpost_kit").stdout
        self.choices("")                                                                             # the header alone: no choice
        self.assertEqual(self.needs("needs", "outpost_kit").stdout, plain)
        self.choices(None)
        lines = plain.split("\n")
        self.assertEqual(lines[:5], ["NEEDS of 1 outpost_kit (catalog 9.9.10)", "Made on the way (one recipe per item):",
                                     "  1 outpost_kit <- assemble_outpost_kit x 1, in a facility: kit_plant", "    2 frame <- assemble_frame x 2, in a facility: frame_plant",
                                     "      8 steel_plate <- press_hide_plate x 4, by hand"])               # the steps as before; the recipe block follows them
        self.assertEqual(lines[5:7], [self.book.TAKEN, "  steel_plate: recipe press_hide_plate (1 of 3; choose another in game/reserve-recipes.tsv)"])
        self.choices("ghost_item\tsmelt\tx\nsteel_plate\tno_such_recipe\tx\nsteel_plate\tassemble_frame\tx\nsteel_plate\tsmelt\tgood\nsteel_plate\tbreak_frame\tagain\n")
        cat = self.book.choose(self.book.load(str(self.data)), str(self.root))
        self.assertEqual({item: row["recipe"] for item, row in cat["choices"]["rows"].items()}, {"steel_plate": "smelt"})   # the good row stands, the bad ones are skipped
        self.assertEqual([e.split(": ", 1)[0] for e in cat["choices"]["errors"]], ["game/reserve-recipes.tsv line 3", "game/reserve-recipes.tsv line 4",
                                                                                 "game/reserve-recipes.tsv line 5", "game/reserve-recipes.tsv line 7"])
        self.assertIn("the recipe `assemble_frame` does not make steel_plate (it makes frame;", cat["choices"]["errors"][2])
        noted = self.needs("needs", "steel_plate").stdout
        self.assertIn("  NOTE game/reserve-recipes.tsv line 3: no item `ghost_item` in the catalog 9.9.10: skipped", noted)
        self.assertIn("1 steel_plate <- smelt x 1", noted)
        self.choices("ghost_item\tsmelt\tx\n")                                                       # only a bad row: the answer is the rule's
        self.assertIn("8 steel_plate <- press_hide_plate x 4", self.needs("needs", "outpost_kit").stdout)
        _rows, errors, _warnings, present = self.book.read_choices(self.root / "game" / "reserve-recipes.tsv", None)   # the form alone, no catalog
        self.assertEqual((errors, present), ([], True))

    def test_the_real_choices_file_reads_without_an_error(self):
        rows, errors, _warnings, present = self.book.read_choices(REPO / "game" / "reserve-recipes.tsv", None)
        self.assertTrue(present)
        self.assertEqual(errors, [])
        self.assertTrue(all(row["note"] for row in rows.values()))                                 # who chose it, when, flown or not

    def test_stored_goods_are_held_against_the_recipes_made_by_hand(self):
        have, places, _when = self.book.stock(str(self.data))
        self.assertEqual((have, len(places)), ({"iron_ore": 34}, 2))
        self.assertEqual(self.book.bids(str(self.data)), {"steel_plate": (30, 1, "home_base")})
        done = subprocess.run([sys.executable, "-I", "-B", str(REPO / "game" / "fleet" / "craftbook.py"), "can", "all", "--data", str(self.data)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env={"FLEET_MEMBER": "Unity", "PATH": "/usr/bin:/bin"})
        self.assertIn("1 recipe-and-station pairs", done.stdout)                                  # the pilot with 9 ore cannot smelt
        self.assertIn("smelt", done.stdout)
        self.assertIn("-> 2 steel_plate | sells for about 30 cr (bid 30 x 1 at home_base)", done.stdout)


if __name__ == "__main__":
    unittest.main()
