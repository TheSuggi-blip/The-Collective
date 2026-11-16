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
