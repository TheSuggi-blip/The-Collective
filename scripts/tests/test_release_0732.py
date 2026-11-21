"""The game's releases 0.729.0 and 0.732.0 in the fleet's readers: a catalog without `hand_craftable` (recipes made by hand are
those with facility_only false outside Ship Passive), renamed recipe categories, and what a buyer pays on top at a pirate
stronghold, at a player's station and at our own. Small catalogs and data folders of its own; no engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record (routemaker.py loads hive.py)

REPO = Path(__file__).resolve().parents[2]
FLEET = REPO / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_0732_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


craftbook, maker, store = load("craftbook"), load("routemaker"), load("store")

# a catalog of the 0.729.0 shape: new category names, no hand_craftable, facility_only only where it is true
CATALOG = {"version": "9.9.9",
           "items": [{"id": "iron_ore", "name": "Iron Ore", "category": "ore", "size": 1, "base_value": 5},
                     {"id": "steel_plate", "name": "Steel Plate", "category": "refined", "size": 1, "base_value": 18},
                     {"id": "frame", "name": "Frame", "category": "component", "size": 2, "base_value": 90}],
           "recipes": [{"id": "smelt", "name": "Smelt", "category": "Smelting", "inputs": [{"item_id": "iron_ore", "quantity": 10}],
                        "outputs": [{"item_id": "steel_plate", "quantity": 1}], "crafting_time": 1, "produced_by_facility_ids": ["smelter"]},
                       {"id": "assemble_frame", "name": "Assemble Frame", "category": "Machining", "inputs": [{"item_id": "steel_plate", "quantity": 4}],
                        "outputs": [{"item_id": "frame", "quantity": 1}], "crafting_time": 2, "facility_only": True, "produced_by_facility_ids": ["frame_plant"]},
                       {"id": "hull_passive", "name": "Hull Passive", "category": "Ship Passive", "inputs": [{"item_id": "frame", "quantity": 1}],
                        "outputs": [{"item_id": "frame", "quantity": 1}], "crafting_time": 1, "produced_by_facility_ids": []}],
           "facilities": [], "ships": [], "skills": []}


class Folder(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="release-0732-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "repo"
        for folder in ("catalog", "stock", "market", "fleet", "scouting", "missions", "wildlife", "routes", "empire"):
            (self.data / folder).mkdir(parents=True)
        (self.root / "game" / "map").mkdir(parents=True)
        (self.root / "game" / "routes" / "plans").mkdir(parents=True)
        self.source = self.data / "catalog" / "9.9.9.json"
        self.source.write_text(json.dumps(CATALOG), encoding="utf-8")

    def put(self, name, value):
        (self.data / name).write_text(json.dumps(value), encoding="utf-8")

    def craftbook(self, *words):
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "craftbook.py")] + list(words) + ["--data", str(self.data), "--root", str(self.root)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


class HandTests(Folder):
    def test_the_rule_of_0729_names_what_is_made_by_hand_and_an_old_catalog_keeps_its_field(self):
        self.assertEqual([craftbook.by_hand(r) for r in CATALOG["recipes"]], [True, False, False])         # facility_only, Ship Passive
        self.assertEqual([craftbook.by_hand({"hand_craftable": h, "facility_only": None, "category": "Refining"}) for h in (True, False)], [True, False])

    def test_the_craft_book_lists_hand_recipes_of_a_catalog_without_the_field(self):
        out = self.craftbook("recipes", "--hand")
        self.assertIn("1 recipes (catalog 9.9.9):", out.stdout)
        self.assertIn("smelt: 1 steel_plate <- 10 iron_ore | by hand", out.stdout)
        self.put("stock/storage.json", {"updated_at": "2026-11-21T20:00:00Z", "pilots": {"hauler-1": {"read_at": "2026-11-21T20:00:00Z",
                                                                                                     "stations": {"base_a": {"iron_ore": 30}}}}})
        self.assertIn("smelt", self.craftbook("can", "all").stdout)                                    # three runs of stored ore, by hand

    def test_an_old_category_name_answers_with_the_categories_the_catalog_holds(self):
        out = self.craftbook("recipes", "--category", "Refining")
        self.assertEqual(out.returncode, 1)
        self.assertIn("no recipe in the category `Refining`", out.stdout)
        self.assertIn("Its 3 categories: Machining 1, Ship Passive 1, Smelting 1", out.stdout)
        self.assertIn("1 recipes (catalog 9.9.9):", self.craftbook("recipes", "--category", "smelting").stdout)

    def test_the_store_and_the_catalog_files_mark_the_hand_recipes(self):
        rows = {r["id"]: r["hand"] for r in store.read_catalog(self.source, {})["recipes"]}
        self.assertEqual(rows, {"smelt": 1, "assemble_frame": 0, "hull_passive": 0})
        (self.root / "game").mkdir(exist_ok=True)
        done = subprocess.run([sys.executable, "-I", "-B", str(REPO / "scripts" / "catalog-index.py"), "--root", str(self.root), "--catalog", str(self.source)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.assertEqual(done.returncode, 0, done.stdout)
        tsv = (self.root / "game" / "catalog" / "tables" / "recipes.tsv").read_text(encoding="ascii")
        self.assertIn("smelt\tSmelt\tSmelting\tsteel_plate x 1\tiron_ore x 10\t1\tyes", tsv)
        self.assertIn("| `smelt` | steel_plate x 1 | iron_ore x 10 | by hand, or in: smelter | 1 |",
                      (self.root / "game" / "catalog" / "recipes" / "smelting.md").read_text(encoding="ascii"))


CHART = ("id\tname\tx\ty\tempire\tflags\tjumps_from_home\tlanes\nhome\tHome\t0\t0\tvoidborn\thome\t0\tmid,pir\nmid\tMid\t1\t0\tvoidborn\t-\t1\thome\n"
         "pir\tPir\t0\t1\t-\tstronghold\t1\thome\n")
NOW = 1_800_000_000
STAMP = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW - 600))
OURS, THEIRS = "a" * 32, "b" * 32                # player stations: an id of 32 hex digits
FACTION = "f" * 32


def station(system, poi, base, owner=None, fee=None):
    entry = {"kind": "normal", "poi": {"id": poi, "system_id": system, "type": "station", "name": poi.title(), "base_id": base}}
    if owner:
        entry["base"] = {"id": base, "faction_id": owner, "market_fee_bps": fee}
    return {poi: entry}


def row(item, bid=0, bid_qty=0, ask=0, ask_qty=0):
    return {"item_id": item, "item_name": item.title(), "best_buy": bid, "best_buy_qty": bid_qty, "best_sell": ask, "best_sell_qty": ask_qty}


class FeeTests(Folder):
    def setUp(self):
        super().setUp()
        (self.root / "game" / "map" / "galaxy.tsv").write_text(CHART, encoding="ascii")
        self.put("scouting/home.json", {"system": "home", "read_at": STAMP, "pois": station("home", "core", "home_base")})
        self.put("scouting/mid.json", {"system": "mid", "read_at": STAMP, "pois": dict(station("mid", "ours", OURS, FACTION, 100),
                                                                                    **station("mid", "theirs", THEIRS, "c" * 32, 300))})
        self.put("scouting/pir.json", {"system": "pir", "read_at": STAMP, "pois": station("pir", "keep", "keep_base")})
        self.put("empire/empire.json", {"faction": {"id": FACTION, "tag": "CLTV"}})
        self.put("fleet/fleet.json", {"ships": [{"name": "trader-1", "cargo_capacity": 20, "docked": None, "status": "connected"}]})
        self.put("catalog/9.9.9.json", dict(CATALOG, items=CATALOG["items"] + [{"id": "gel", "size": 1}]))

    def book(self, base, system, rows):
        self.put("market/%s.json" % base, {"base": base, "system": system, "read_at": STAMP, "items": rows})

    def world(self):
        world = maker.load_world(str(self.data), self.root / "game", NOW)
        world["policed"] = maker.policed_systems(self.root / "game")
        return world

    def test_a_buyer_pays_five_percent_at_a_stronghold_the_owner_s_fee_at_a_player_s_station_and_none_at_ours(self):
        for base, system in (("home_base", "home"), ("keep_base", "pir"), (OURS, "mid"), (THEIRS, "mid")):
            self.book(base, system, [row("gel", ask=100, ask_qty=20)])
        self.book("sink_base", "home", [row("gel", bid=200, bid_qty=1000)])
        world = self.world()
        found = {c["basis"]["buy_at"]: c for c in maker.trade_candidates(world) if c["kind"] == "trade"}
        for base, share in (("home_base", 0.01), ("keep_base", 0.05), (OURS, 0.0), (THEIRS, 0.03)):
            basis = found[base]["basis"]
            jumps = world["chart"].jumps(world["books"][base]["system"], "home")
            fuel = maker.trip(world, jumps, legs=0, docks=2)[1]
            self.assertEqual(found[base]["per_run"], int(round(basis["got"] - basis["paid"] * (1 + share) - fuel)), base)
        self.assertEqual([maker.buy_share(world, b) for b in ("home_base", "keep_base", OURS, THEIRS, "c" * 32)],
                         [0.01, 0.05, 0.0, 0.03, 0.01])                     # sales tax, stronghold, ours, its 300 bps, no reading: the default

    def test_a_catalog_without_the_field_still_gives_craft_candidates(self):
        self.book("home_base", "home", [row("iron_ore", ask=1, ask_qty=500), row("steel_plate", bid=60, bid_qty=8)])
        world = self.world()
        self.assertEqual([r["id"] for r in world["recipes"]], ["smelt"])
        crafts = [c for c in maker.craft_candidates(world) if c["basis"]["recipe"] == "smelt"]
        self.assertEqual(len(crafts), 1)
        self.assertEqual(crafts[0]["basis"]["inputs"], ["80 iron_ore for 80 cr (depth at the best price)"])


if __name__ == "__main__":
    unittest.main()
