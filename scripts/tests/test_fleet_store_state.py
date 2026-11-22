"""store.py's snapshot tables on a disposable data folder and repository: each loader fills its tables, a file is read again only when it changed, a missing or broken file is skipped and named, the storage book adds up, the views, the map's fallback, our empire, the orders that age; the hourly samples of what each division holds (stock_hour) and reserve_flow; query() reads and nothing else, stops in time and cuts at its limit; schema() describes every table; hive.py sql and schema."""

import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "game" / "fleet" / "store.py"
HIVE = ROOT / "game" / "fleet" / "hive.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


store = load("store_state_under_test", SCRIPT)
STAMP = "2026-11-16T12:00:00Z"
BOOK = {"what": "Personal station storage of every pilot of ours, per station; totals per station and per member's division; the holds",
        "updated_at": STAMP,
        "pilots": {"miner-1": {"read_at": "2026-11-16T11:00:00Z", "stations": {"base_a": {"iron_ore": 10, "water_ice": 3}, "base_b": {"iron_ore": 2}}},
                   "trader-2": {"read_at": "2026-11-16T11:30:00Z", "stations": {"base_b": {"iron_ore": 7, "steel_plate": 4}}},
                   "drone-3": {"read_at": "2026-11-16T11:40:00Z", "error": "not read"}},
        "totals": {"by_station": {"base_a": {"iron_ore": 10, "water_ice": 3}, "base_b": {"iron_ore": 9, "steel_plate": 4}},
                   "by_member": {"Zero": {"base_a": {"iron_ore": 10, "water_ice": 3}, "base_b": {"iron_ore": 2}}, "Mercury": {"base_b": {"iron_ore": 7, "steel_plate": 4}}},
                   "holds_by_member": {"Zero": {"iron_ore": 5}, "Mercury": {"steel_plate": 1}}}}
CATALOG = {"version": "0.2.0",
           "items": [{"id": "iron_ore", "name": "Iron Ore", "category": "ore", "size": 1, "base_value": 5, "rarity": "common", "tradeable": True, "stackable": True},
                     {"id": "water_ice", "name": "Water Ice", "category": "ice", "size": 1, "base_value": 12},
                     {"id": "steel_plate", "name": "Steel Plate", "category": "component", "size": 2, "base_value": 60},
                     {"id": "mining_laser_i", "name": "Mining Laser I", "size": 5, "base_value": 400, "type": "mining", "slot": "utility"}],
           "recipes": [{"id": "make_steel", "name": "Make Steel", "category": "Refining", "inputs": [{"item_id": "iron_ore", "quantity": 4}],
                        "outputs": [{"item_id": "steel_plate", "quantity": 1}], "crafting_time": 2.5, "hand_craftable": True, "produced_by_facility_ids": ["smelter"]},
                       {"id": "make_hull", "name": "Make Hull", "category": "Assembly", "inputs": [{"item_id": "steel_plate", "quantity": 10}],
                        "outputs": [], "crafting_time": 9, "hand_craftable": False, "facility_only": True, "produced_by_facility_ids": []}],
           "facilities": [{"id": "hiring_board", "name": "Hiring Board", "category": "faction", "level": 1, "build_cost": 75000, "build_time": 10, "labor_cost": 5,
                           "faction_service_type": "faction_recruitment", "faction_cap": 50, "build_materials": [{"item_id": "steel_plate", "quantity": 20}]},
                          {"id": "recruitment_desk", "name": "Recruitment Desk", "category": "faction", "level": 2, "build_cost": 300000, "upgrades_from": "hiring_board",
                           "faction_service_type": "faction_recruitment", "faction_cap": 100, "build_materials": [{"item_id": "steel_plate", "quantity": 50}]},
                          {"id": "smelter", "name": "Smelter", "category": "production", "level": 1, "build_cost": 1000, "recipe_id": "make_steel"}],
           "ships": [{"id": "hauler_one", "name": "Hauler One", "class": "Freighter", "tier": 1, "faction": "voidborn", "cargo_capacity": 120,
                      "build_materials": [{"item_id": "steel_plate", "quantity": 30}]}],
           "skills": [{"id": "mining", "name": "Mining", "category": "Industry", "max_level": 100, "training_source": "Mine ore."}]}


def write(path, value, mtime=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="ascii")
    if mtime is not None:
        os.utime(path, (mtime, mtime))


def fixture(data, root, now):
    """A small data folder and repository game/ folder with every file the snapshot reads."""
    ship = lambda name, system, docked, **more: dict({"name": name, "division": more.pop("division", "Mining"), "system": system, "poi": system + "_belt",
                                                     "docked": docked, "status": "connected", "class": "Threshold", "hull": 70, "max_hull": 75, "fuel": 10,
                                                     "max_fuel": 95, "cargo_used": 5, "cargo_capacity": 65, "credits": 1000, "state_at": "2026-11-16 11:59:00",
                                                     "activity": {"kind": "loop", "type": "mining"}}, **more)
    write(data / "fleet" / "fleet.json", {"updated_at": STAMP, "ships": [ship("miner-1", "sys_a", "base_a"), ship("trader-2", "sys_b", "", division="Trade"),
                                                                       ship("Flag One", "sys_a", "", division="Command")]})
    write(data / "fleet" / "flagships.json", {"Flag One": {"admiral": "Unity", "division": "Command", "role": "command", "of": "Zero"}})
    write(data / "fleet" / "ships" / "miner-1.json", {"name": "miner-1", "skills": {"mining": {"level": 3, "xp": 10}, "piloting": {"level": 5, "xp": 2}},
                                                      "modules": [{"type": "mining_laser_i", "name": "Mining Laser I", "slot": "utility", "kind": "mining"}],
                                                      "cargo": [{"item": "iron_ore", "quantity": 5}]})
    write(data / "fleet" / "ships" / "trader-2.json", {"name": "trader-2", "skills": {"trading": {"level": 2, "xp": 0}}, "modules": [],
                                                       "cargo": [{"item_id": "steel_plate", "quantity": 1}]})
    write(data / "fleet" / "ships" / "Flag_One.json", {"name": "Flag One", "skills": {}, "modules": [], "cargo": []})
    write(data / "fleet" / "orders" / "miner-1.json", {"pilot": "miner-1", "what": "mine mine-a"}, mtime=now - 60)
    write(data / "stock" / "storage.json", BOOK)
    write(data / "market" / "base_a.json", {"base": "base_a", "system": "sys_a", "read_at": STAMP, "items": [
        {"item_id": "iron_ore", "item_name": "Iron Ore", "category": "ore", "best_buy": 12, "best_buy_qty": 50, "buy_quantity": 80, "best_sell": 0, "best_sell_qty": 0},
        {"item_id": "steel_plate", "item_name": "Steel Plate", "best_buy": 0, "best_buy_qty": 0, "best_sell": 90, "best_sell_qty": 4, "sell_quantity": 4}]})
    write(data / "market" / "base_b.json", {"base": "base_b", "system": "sys_b", "read_at": STAMP, "items": [
        {"item_id": "iron_ore", "item_name": "Iron Ore", "best_buy": 15, "best_buy_qty": 20, "best_sell": 0}]})
    write(data / "market" / "ladders.json", {"base_a": {"iron_ore": {"bids": [[12, 50], [10, 100]], "asks": [], "t": 1794855396}}})
    write(data / "market" / "history.state.json", {"base_a": {"read_at": STAMP}})
    write(data / "catalog" / "0.1.0.json", {"version": "0.1.0", "items": [{"id": "old_item"}]})
    write(data / "catalog" / "0.2.0.json", CATALOG)
    write(data / "catalog" / "ammo.json", {"ammo": []})
    write(data / "scouting" / "sys_a.json", {"read_at": STAMP, "system": {"id": "sys_a", "name": "Sys A", "pois": [
        {"id": "sys_a_belt", "name": "A Belt", "type": "asteroid_belt", "class": "metallic", "position": {"x": 1, "y": 2}},
        {"id": "base_a", "name": "A Station", "type": "station", "has_base": True, "base_id": "base_a"}]},
        "pois": {"sys_a_belt": {"kind": "normal", "poi": {"id": "sys_a_belt", "type": "asteroid_belt"},
                                "resources": [{"resource_id": "iron_ore", "remaining": 400, "max_remaining": 5000, "richness": 40},
                                              {"resource_id": "copper_ore", "remaining": 0, "max_remaining": 900, "richness": 9}]}}})
    write(data / "wildlife" / "sys_a.json", {"system": "sys_a", "read_at": STAMP, "pois": {"sys_a_belt": {"read_at": STAMP, "creatures": [
        {"species": "kiln_snail", "name": "Kiln-Snail", "role": "grazer"}, {"species": "kiln_snail", "name": "Kiln-Snail", "role": "grazer"},
        {"species": "veil_ray", "name": "Veil Ray", "role": "predator"}]}}})
    write(data / "missions" / "base_a.json", {"base": "base_a", "system": "sys_a", "read_at": STAMP, "missions": [
        {"mission_id": "m1", "template_id": "t1", "title": "Haul Ore", "type": "delivery", "difficulty": 2, "rewards": {"credits": 1500, "piloting_xp": 20,
         "items": {"steel_plate": 2}}, "objectives": [{"description": "Deliver 10 iron ore"}], "expires_in_ticks": 99, "giver": {"name": "Clerk"}}]})
    write(data / "intel" / "met.json", {"Other Pilot": {"first": "2026-11-15T10:00:00Z", "times": 4, "faction_tag": "ROGU", "ship_class": "cobble",
                                                        "system": "sys_b", "poi": "sys_b_belt", "last": "2026-11-16T11:00:00Z", "in_combat_at": "2026-11-16T10:00:00Z"}})
    write(data / "station" / "map.json", {"systems": [
        {"id": "sys_a", "name": "Sys A", "x": 0, "y": 0, "empire": "voidborn", "home": True, "stronghold": False, "lanes": ["sys_b"], "jumps": 0},
        {"id": "sys_b", "name": "Sys B", "x": 5, "y": 1, "empire": "", "home": False, "stronghold": False, "lanes": ["sys_a", "sys_c"], "jumps": 1},
        {"id": "sys_c", "name": "Sys C", "x": 9, "y": 9, "empire": "crimson", "home": False, "stronghold": True, "lanes": ["sys_b"], "jumps": 4}],
        "empires": {"voidborn": "#9b59b6"}})
    write(data / "station" / "stations.json", [
        {"name": "A Station", "type": "station", "system": "sys_a", "tag": "", "faction": "", "empire": "voidborn", "condition": "thriving",
         "services": ["market", "repair"], "wrecked": False, "mobile": False},
        {"name": "Our Outpost", "type": "outpost", "system": "sys_b", "tag": "COLL", "faction": "The Collective", "empire": "", "condition": "thriving",
         "services": [], "wrecked": False, "mobile": False},
        {"name": "Far Fort", "type": "station", "system": "sys_c", "tag": "ROGU", "faction": "Rogues", "empire": "", "condition": "damaged",
         "services": ["repair"], "wrecked": True, "mobile": False}])
    write(data / "station" / "feed.json", {"built_at": STAMP, "factions": {
        "COLL": {"name": "The Collective", "members": 146, "leader": "Flag One", "allies": [], "enemies": ["ROGU"], "wars": [""]},
        "ROGU": {"name": "Rogues", "members": 12, "leader": "Boss", "allies": [], "enemies": [], "wars": ["COLL", "XYZ"]}},
        "players": {"someone": {"faction": "ROGU"}}})
    write(data / "station" / "battles.json", [
        {"system": "sys_b", "system_name": "Sys B", "category": "pirate", "status": "completed", "tick": 1234,
         "destroyed": 1, "lost": ["Wreck-1"], "pilots": ["Other Pilot"], "tags": ["ROGU"], "ended_at": STAMP}])
    write(data / "station" / "leaderboard.json", {
        "generated_at": STAMP, "groups": {"factions": {"total_wealth": [
            {"rank": 1, "name": "The Collective", "tag": "COLL", "value": 9000000}]}}})
    write(data / "empire" / "empire.json", {"written_at": STAMP, "unknown_key": 1,
                                            "faction": {"id": "f1", "name": "The Collective", "tag": "COLL", "leader": "Flag One", "member_count": 146,
                                                        "members_limit": 150, "treasury": None, "owned_bases": 1, "at_war": False, "created_at": "2026-11-14T00:00:00Z",
                                                        "colour": "violet"},
                                            "members": [{"pilot": "miner-1", "role": "member"}, {"pilot": "Flag One", "role": "leader"}],
                                            "bases": [{"base": "base_o", "name": "Our Outpost", "system": "sys_b", "poi": "sys_b_rock", "kind": "outpost"}],
                                            "facilities": [{"facility_id": "fac1", "type": "hiring_board", "name": "Hiring Board", "level": 1, "base": "base_o",
                                                            "system": "sys_b", "status": "active", "rent_per_cycle": None}],
                                            "territory": [{"system": "sys_b", "claim": "outpost", "note": "ours"}]})
    write(root / "routes" / "mine-a.json", {"id": "mine-a", "kind": "mine", "title": "Mine A", "belt": "sys_a:sys_a_belt", "station": "base_a", "max_ships": 4,
                                            "sell": [{"item": "iron_ore", "min_price": 1}],
                                            "measured": {"date": "2026-11-16", "runs": 3, "minutes": 12, "credits_per_run": 100, "cph_per_ship": 500}})
    write(root / "routes" / "park.json", {"id": "park", "kind": "circuit", "title": "Dock and wait", "park": True, "stops": []})
    write(root / "routes" / "plan.json", {"not": "a route"})
    write(root / "routes" / "plans" / "miner.json", {"role": "miner", "owner": "Zero", "routes": ["mine-a", "park"], "ships": {"mine-a": 2}})
    write(root / "map" / "galaxy.tsv", "# a chart\nid\tname\tx\ty\tempire\tflags\tjumps_from_home\tlanes\n"
                                       "sys_a\tSys A\t0.0\t0.0\tvoidborn\thome\t0\tsys_b\nsys_b\tSys B\t5.0\t1.0\t-\t-\t1\tsys_a\n")


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-store-state-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "game"
        self.now = time.time()
        fixture(self.data, self.root, self.now)

    def one(self, now=None):
        return store.one_pass(str(self.data), now=self.now if now is None else now, root=str(self.root))

    def read(self, sql, args=()):
        conn = store.connect(str(self.data))
        try:
            return conn.execute(sql, args).fetchall()
        finally:
            conn.close()

    def bump(self, path, value=None):
        """Change a file: new content when given, and an mtime the last pass did not see."""
        if value is not None:
            write(path, value)
        later = path.stat().st_mtime + 7
        os.utime(path, (later, later))

    def test_each_loader_fills_its_tables_from_its_files(self):
        out = self.one()
        self.assertEqual(dict(out["snapshot"]["loaded"]), {"fleet": 1, "orders": 1, "ships": 3, "holdings": 1, "books": 2, "ladders": 1, "catalog": 1,
                                                           "scouting": 1, "wildlife": 1, "missions": 1, "met": 1, "map": 1, "stations": 1, "factions": 1, "battles": 1, "leaderboards": 1,
                                                           "empire": 1, "routes": 2, "plans": 1})
        self.assertEqual(out["snapshot"]["problems"], [])
        self.assertEqual(self.read("SELECT pilot, member, division, role, system, docked, base, flies FROM ships ORDER BY pilot"),
                         [("Flag One", "Unity", "Command", "command", "sys_a", 0, None, None),
                          ("miner-1", "Zero", "Mining", "miner", "sys_a", 1, "base_a", "mine mine-a"),
                          ("trader-2", "Mercury", "Trade", "trader", "sys_b", 0, None, None)])
        self.assertEqual(self.read("SELECT t FROM ships WHERE pilot = 'miner-1'"), [(store.epoch("2026-11-16T11:59:00Z"),)])
        self.assertEqual(self.read("SELECT pilot, skill, level, xp FROM ship_skills ORDER BY pilot, skill"),
                         [("miner-1", "mining", 3, 10), ("miner-1", "piloting", 5, 2), ("trader-2", "trading", 2, 0)])
        self.assertEqual(self.read("SELECT pilot, module, slot FROM ship_modules"), [("miner-1", "mining_laser_i", "utility")])
        self.assertEqual(sorted(self.read("SELECT pilot, item, units FROM ship_cargo")), [("miner-1", "iron_ore", 5), ("trader-2", "steel_plate", 1)])
        self.assertEqual(self.read("SELECT base, item, bid, bid_qty, ask, ask_qty, bid_depth FROM books ORDER BY base, item"),
                         [("base_a", "iron_ore", 12, 50, None, 0, 80), ("base_a", "steel_plate", None, 0, 90, 4, None), ("base_b", "iron_ore", 15, 20, None, None, None)])
        self.assertEqual(self.read("SELECT base, item, side, step, price, qty FROM ladders ORDER BY step"),
                         [("base_a", "iron_ore", "bid", 1, 12, 50), ("base_a", "iron_ore", "bid", 2, 10, 100)])
        self.assertEqual(self.read("SELECT src FROM items GROUP BY src"), [("catalog/0.2.0.json",)])        # the newest version, ammo.json is none
        self.assertEqual(self.read("SELECT id, category, base_value FROM items ORDER BY id"),
                         [("iron_ore", "ore", 5), ("mining_laser_i", None, 400), ("steel_plate", "component", 60), ("water_ice", "ice", 12)])
        self.assertEqual(self.read("SELECT id, hand, facility_only, time FROM recipes ORDER BY id"), [("make_hull", 0, 1, 9.0), ("make_steel", 1, None, 2.5)])
        self.assertEqual(self.read("SELECT recipe, item, units FROM recipe_inputs ORDER BY recipe"), [("make_hull", "steel_plate", 10), ("make_steel", "iron_ore", 4)])
        self.assertEqual(self.read("SELECT recipe, item, units FROM recipe_outputs"), [("make_steel", "steel_plate", 1)])
        self.assertEqual(self.read("SELECT recipe, facility FROM recipe_facilities"), [("make_steel", "smelter")])
        self.assertEqual(self.read("SELECT id, level, upgrades_from, faction_cap, recipe FROM facilities ORDER BY id"),
                         [("hiring_board", 1, None, 50, None), ("recruitment_desk", 2, "hiring_board", 100, None), ("smelter", 1, None, None, "make_steel")])
        self.assertEqual(self.read("SELECT facility, item, units FROM facility_materials ORDER BY facility"),
                         [("hiring_board", "steel_plate", 20), ("recruitment_desk", "steel_plate", 50)])
        self.assertEqual(self.read("SELECT id, class, tier, cargo FROM hulls"), [("hauler_one", "Freighter", 1, 120)])
        self.assertEqual(self.read("SELECT hull, item, units FROM hull_materials"), [("hauler_one", "steel_plate", 30)])
        self.assertEqual(self.read("SELECT id, max_level, training FROM skills"), [("mining", 100, "Mine ore.")])
        self.assertEqual(self.read("SELECT system, poi, kind, base, x FROM places ORDER BY poi"),
                         [("sys_a", "base_a", "station", "base_a", None), ("sys_a", "sys_a_belt", "asteroid_belt", None, 1)])
        self.assertEqual(self.read("SELECT resource, remaining, max_remaining, richness FROM fields ORDER BY resource"),
                         [("copper_ore", 0, 900, 9), ("iron_ore", 400, 5000, 40)])
        self.assertEqual(self.read("SELECT creature, role, count FROM herds ORDER BY creature"), [("kiln_snail", "grazer", 2), ("veil_ray", "predator", 1)])
        self.assertEqual(self.read("SELECT base, id, kind, reward, reward_items, reward_xp, giver, objectives FROM missions"),
                         [("base_a", "m1", "delivery", 1500, "2 steel_plate", 20, "Clerk", "Deliver 10 iron ore")])
        self.assertEqual(self.read("SELECT name, faction, system, first, t, times, in_combat FROM met"),
                         [("Other Pilot", "ROGU", "sys_b", store.epoch("2026-11-15T10:00:00Z"), store.epoch("2026-11-16T11:00:00Z"), 4,
                           store.epoch("2026-11-16T10:00:00Z"))])
        self.assertEqual(self.read("SELECT id, kind, grp, place, station, max_ships, cph, runs, measured FROM routes ORDER BY id"),
                         [("mine-a", "mine", "paying", "sys_a:sys_a_belt", "base_a", 4, 500, 3, "2026-11-16"),
                          ("park", "circuit", "service", None, None, None, None, None, None)])
        self.assertEqual(self.read("SELECT role, n, route, ships FROM plan_routes ORDER BY n"), [("miner", 1, "mine-a", 2), ("miner", 2, "park", None)])

    def test_the_map_its_fallback_the_stations_the_factions_and_our_empire(self):
        self.one()
        self.assertEqual(self.read("SELECT id, empire, home, stronghold, jumps FROM systems ORDER BY id"),
                         [("sys_a", "voidborn", 1, 0, 0), ("sys_b", None, 0, 0, 1), ("sys_c", "crimson", 0, 1, 4)])       # lawless is NULL
        self.assertEqual(self.read("SELECT a, b FROM lanes ORDER BY a, b"), [("sys_a", "sys_b"), ("sys_b", "sys_a"), ("sys_b", "sys_c"), ("sys_c", "sys_b")])
        self.assertEqual(self.read("SELECT name, kind, system, tag, services, wrecked FROM stations ORDER BY name"),
                         [("A Station", "station", "sys_a", None, "market,repair", 0), ("Far Fort", "station", "sys_c", "ROGU", "repair", 1),
                          ("Our Outpost", "outpost", "sys_b", "COLL", "", 0)])
        self.assertEqual(self.read("SELECT tag, members, enemies, wars FROM factions ORDER BY tag"), [("COLL", 146, "ROGU", ""), ("ROGU", 12, "", "COLL,XYZ")])
        self.assertNotIn("players", [row[0] for row in self.read("SELECT name FROM sqlite_master")])
        self.assertEqual(self.read("SELECT tag, member_count, members_limit, treasury, at_war, created FROM faction"),
                         [("COLL", 146, 150, None, 0, store.epoch("2026-11-14T00:00:00Z"))])
        self.assertEqual(self.read("SELECT pilot, role FROM faction_members ORDER BY pilot"), [("Flag One", "leader"), ("miner-1", "member")])
        self.assertEqual(self.read("SELECT base, system, kind FROM bases"), [("base_o", "sys_b", "outpost")])
        self.assertEqual(self.read("SELECT id, type, base, rent_per_cycle FROM faction_facilities"), [("fac1", "hiring_board", "base_o", None)])
        self.assertEqual(self.read("SELECT system, claim FROM territory"), [("sys_b", "outpost")])
        self.assertEqual(self.read("SELECT COUNT(*) FROM sites"), [(0,)])                                  # a missing list is an empty table
        self.assertEqual(self.read("SELECT name, system, tag, base, poi FROM our_stations"), [("Our Outpost", "sys_b", "COLL", "base_o", "sys_b_rock")])
        (self.data / "station" / "map.json").unlink()                                                   # the chart of the repository stands in
        out = self.one()
        self.assertEqual(out["snapshot"]["problems"], [("station/map.json", "missing: the chart game/map/galaxy.tsv stands in")])
        self.assertEqual(self.read("SELECT id, empire, home, jumps, src FROM systems ORDER BY id"),
                         [("sys_a", "voidborn", 1, 0, "game/map/galaxy.tsv"), ("sys_b", None, 0, 1, "game/map/galaxy.tsv")])
        self.assertEqual(self.read("SELECT a, b FROM lanes ORDER BY a"), [("sys_a", "sys_b"), ("sys_b", "sys_a")])
        self.assertEqual(self.one()["snapshot"]["problems"], [])                                        # named once, not at every pass
        write(self.data / "station" / "map.json", {"systems": [{"id": "sys_z", "name": "Z", "empire": "", "lanes": [], "jumps": 2}]})
        self.one()
        self.assertEqual(self.read("SELECT id, src FROM systems"), [("sys_z", "station/map.json")])
        self.assertEqual(self.read("SELECT name, note FROM source WHERE loader = 'map'"), [("station/map.json", "")])

    def test_an_unchanged_file_is_not_read_again_and_a_changed_one_is(self):
        reads = []
        self.addCleanup(setattr, store, "load_json", store.load_json)
        real = store.load_json
        store.load_json = lambda path: reads.append(Path(path).relative_to(self.data).as_posix()) or real(path)
        first = self.one()
        self.assertIn("market/base_a.json", reads)
        self.assertEqual((len(reads), len(set(reads))), (19, 19))            # each JSON file a reader parses, once (orders and flagships: division.py)
        self.assertNotIn("catalog/0.1.0.json", reads)
        reads.clear()
        again = self.one()
        self.assertEqual((reads, dict(again["snapshot"]["loaded"]), again["published"]), ([], {}, False))
        self.assertIsNone(store.said(again))
        stamp = self.read("SELECT t FROM source WHERE name = 'market/base_a.json'")
        self.bump(self.data / "market" / "base_a.json", {"base": "base_a", "system": "sys_a", "read_at": STAMP, "items": [
            {"item_id": "iron_ore", "best_buy": 14, "best_buy_qty": 9}]})
        third = self.one(now=self.now + 30)
        self.assertEqual((reads, dict(third["snapshot"]["loaded"])), (["market/base_a.json"], {"books": 1}))
        self.assertTrue(third["published"])
        self.assertEqual(self.read("SELECT base, item, bid FROM books ORDER BY base"), [("base_a", "iron_ore", 14), ("base_b", "iron_ore", 15)])
        self.assertGreater(self.read("SELECT t FROM source WHERE name = 'market/base_a.json'")[0][0], stamp[0][0])
        self.assertIn("snapshot: 1 files read (books 1)", store.said(third))
        reads.clear()
        self.bump(self.data / "catalog" / "0.2.0.json")                       # the same bytes, a new mtime: read again
        self.assertEqual(dict(self.one()["snapshot"]["loaded"]), {"catalog": 1})
        self.assertEqual(reads, ["catalog/0.2.0.json"])

    def test_a_missing_and_a_broken_file_are_skipped_and_named_and_the_others_go_on(self):
        self.one()
        write(self.data / "market" / "base_a.json", '{"base": "base_a", "items": [')                     # half written
        (self.data / "intel" / "met.json").unlink()
        self.bump(self.data / "market" / "base_b.json", {"base": "base_b", "system": "sys_b", "read_at": STAMP, "items": [
            {"item_id": "iron_ore", "best_buy": 16, "best_buy_qty": 3}]})
        self.bump(self.data / "station" / "feed.json", {"factions": "not an object"})
        out = self.one(now=self.now + 30)
        self.assertEqual(sorted(name for name, _note in out["snapshot"]["problems"]), ["intel/met.json", "market/base_a.json", "station/feed.json"])
        line = store.said(out)
        for name in ("market/base_a.json (bad: JSONDecodeError", "intel/met.json (missing)", "station/feed.json (bad: ValueError: no object `factions`)"):
            self.assertIn(name, line)
        notes = dict(self.read("SELECT name, note FROM source WHERE note <> ''"))
        self.assertEqual(set(notes), {"intel/met.json", "market/base_a.json", "station/feed.json"})
        self.assertEqual(self.read("SELECT base, item, bid FROM books ORDER BY base, item"),             # the broken book keeps its rows; the other was read
                         [("base_a", "iron_ore", 12), ("base_a", "steel_plate", None), ("base_b", "iron_ore", 16)])
        self.assertEqual(self.read("SELECT COUNT(*) FROM met"), [(1,)])                                 # a missing file of a fixed name keeps its rows
        self.assertEqual(self.read("SELECT COUNT(*) FROM factions"), [(2,)])
        self.assertEqual(self.read("SELECT COUNT(*) FROM items"), [(4,)])
        later = self.one(now=self.now + 60)
        self.assertEqual(later["snapshot"]["problems"], [])                                             # named once
        (self.data / "market" / "base_b.json").unlink()                                                  # a file of a folder that is gone takes its rows
        gone = self.one(now=self.now + 90)
        self.assertEqual(gone["snapshot"]["gone"], 1)
        self.assertEqual(self.read("SELECT DISTINCT base FROM books"), [("base_a",)])
        self.assertEqual(self.read("SELECT COUNT(*) FROM source WHERE name = 'market/base_b.json'"), [(0,)])

    def test_the_storage_book_adds_up_and_the_views(self):
        self.one()
        totals = {}
        for goods in list(BOOK["totals"]["by_station"].values()) + list(BOOK["totals"]["holds_by_member"].values()):
            for item, units in goods.items():
                totals[item] = totals.get(item, 0) + units
        self.assertEqual(dict(self.read("SELECT item, SUM(units) FROM holdings GROUP BY item")), totals)
        self.assertEqual(self.read("SELECT pilot, member, place, units FROM holdings WHERE item = 'iron_ore' ORDER BY units"),
                         [("miner-1", "Zero", "base_b", 2), (None, "Zero", "hold", 5), ("trader-2", "Mercury", "base_b", 7), ("miner-1", "Zero", "base_a", 10)])
        self.assertEqual(self.read("SELECT t FROM holdings WHERE pilot = 'trader-2'"), [(store.epoch("2026-11-16T11:30:00Z"),)] * 2)
        self.assertEqual(self.read("SELECT item, name, category, units, in_storage, in_holds, base_value, worth FROM inventory ORDER BY item"),
                         [("iron_ore", "Iron Ore", "ore", 24, 19, 5, 5, 120), ("steel_plate", "Steel Plate", "component", 5, 4, 1, 60, 300),
                          ("water_ice", "Water Ice", "ice", 3, 3, 0, 12, 36)])
        craftbook = load("craftbook_beside_store", ROOT / "game" / "fleet" / "craftbook.py")          # the one rule for what the fleet owns
        owned = craftbook.inventory(str(self.data))
        self.assertEqual({r["id"]: (r["units"], r["stored"], r["held"], r["worth"]) for g in owned["groups"] for r in g["rows"]},
                         {row[0]: tuple(row[1:]) for row in self.read("SELECT item, units, in_storage, in_holds, worth FROM inventory")})
        self.assertEqual({(s["base"], r["id"]): r["units"] for s in owned["stations"] for r in s["rows"]},
                         {(p, i): u for p, i, u in self.read("SELECT place, item, units FROM inventory_by_station")})
        self.assertEqual(self.read("SELECT place, item, name, units FROM inventory_by_station ORDER BY place, item"),
                         [("base_a", "iron_ore", "Iron Ore", 10), ("base_a", "water_ice", "Water Ice", 3), ("base_b", "iron_ore", "Iron Ore", 9),
                          ("base_b", "steel_plate", "Steel Plate", 4), ("hold", "iron_ore", "Iron Ore", 5), ("hold", "steel_plate", "Steel Plate", 1)])
        self.assertEqual(self.read("SELECT system, name, empire, jumps, ships, docked, flying, command, mining, logistics, trade, military, intel "
                                   "FROM fleet_positions ORDER BY system"),
                         [("sys_a", "Sys A", "voidborn", 0, 2, 1, 1, 1, 1, 0, 0, 0, 0), ("sys_b", "Sys B", None, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0)])

    def test_the_order_a_ship_flies_follows_its_order_file_and_ages(self):
        self.one()
        orders = self.data / "fleet" / "orders"
        write(orders / "trader-2.json", {"pilot": "trader-2", "what": "circuit park"}, mtime=self.now + store.division.ORDER_FRESH)
        out = self.one(now=self.now + 30)                                     # fleet.json unchanged: only the order is read again
        self.assertEqual((dict(out["snapshot"]["loaded"]), out["snapshot"]["flies"]), ({"orders": 1}, 1))
        self.assertTrue(out["published"])
        self.assertEqual(self.read("SELECT pilot, flies FROM ships WHERE flies IS NOT NULL ORDER BY pilot"), [("miner-1", "mine mine-a"), ("trader-2", "circuit park")])
        aged = self.one(now=self.now + 30 + store.division.ORDER_FRESH)       # no file changed, the order of miner-1 aged past ORDER_FRESH
        self.assertEqual((dict(aged["snapshot"]["loaded"]), aged["snapshot"]["flies"]), ({}, 1))
        self.assertEqual(self.read("SELECT pilot FROM ships WHERE flies IS NOT NULL"), [("trader-2",)])
        (orders / "trader-2.json").unlink()                                   # the runner ended: its order file is gone
        self.one(now=self.now + 40)
        self.assertEqual(self.read("SELECT COUNT(*) FROM ships WHERE flies IS NOT NULL"), [(0,)])

    def test_a_changed_definition_drops_and_loads_the_snapshot_again(self):
        self.one()
        conn = sqlite3.connect(str(self.data / "store" / "live.db"))
        conn.execute("UPDATE meta SET value = 'old' WHERE key = 'snapshot.schema'")
        conn.execute("CREATE TABLE gone_table (x)")
        conn.execute("UPDATE meta SET value = ? WHERE key = 'snapshot.tables'", (json.dumps({"tables": ["gone_table"], "views": []}),))
        conn.commit()
        conn.close()
        out = self.one()
        self.assertEqual(out["snapshot"]["loaded"]["catalog"], 1)
        names = [row[0] for row in self.read("SELECT name FROM sqlite_master WHERE type = 'table'")]
        self.assertNotIn("gone_table", names)
        self.assertIn("runs", names)                                          # the history is never dropped
        self.assertEqual(self.read("SELECT COUNT(*) FROM items"), [(4,)])

    def stock(self):
        return {(d, i): u for d, i, u in self.read("SELECT division, item, units FROM stock_hour WHERE hour = (SELECT MAX(hour) FROM stock_hour)")}

    def test_stock_hour_holds_one_sample_an_hour_per_division_and_item_and_a_later_pass_of_the_hour_replaces_it(self):
        noon = store.epoch("2026-11-16T12:10:00Z")
        out = self.one(now=noon)
        self.assertEqual(out["sampled"], 4)
        self.assertIn("stock_hour: 4 rows of the hour", store.said(out))
        self.assertEqual(self.stock(), {("Mining", "iron_ore"): 17, ("Mining", "water_ice"): 3, ("Trade", "iron_ore"): 7, ("Trade", "steel_plate"): 5})   # storage + holds
        self.assertEqual(self.read("SELECT DISTINCT hour, t FROM stock_hour"), [(store.epoch("2026-11-16T12:00:00Z"), noon)])
        self.assertEqual(self.one(now=noon + 600)["sampled"], 0)                                 # the book did not change: the hour keeps its sample
        book = json.loads(json.dumps(BOOK))
        book["pilots"]["miner-1"]["stations"] = {"base_b": {"iron_ore": 2}}                     # water ice sold, iron ore moved on
        book["pilots"]["drone-3"] = {"read_at": "2026-11-16T12:20:00Z", "stations": {"base_a": {"iron_ore": 500}}}
        self.bump(self.data / "stock" / "storage.json", book)
        out = self.one(now=noon + 1800)                                                          # the same hour, the book read again: replaced
        self.assertEqual(out["sampled"], 4)
        self.assertEqual(self.stock(), {("Mining", "iron_ore"): 7, ("Trade", "iron_ore"): 7, ("Trade", "steel_plate"): 5, ("Military", "iron_ore"): 500})
        self.assertEqual(self.read("SELECT COUNT(*), COUNT(DISTINCT hour), MAX(t) FROM stock_hour"), [(4, 1, noon + 1800)])
        self.assertEqual(self.one(now=noon + 3600)["sampled"], 4)                                # a new hour, the book unchanged: its first pass samples it
        self.assertEqual(self.read("SELECT hour, COUNT(*) FROM stock_hour GROUP BY hour ORDER BY hour"), [(store.epoch("2026-11-16T12:00:00Z"), 4), (store.epoch("2026-11-16T13:00:00Z"), 4)])
        self.one(now=noon + 31 * 86400)                                                         # 30 days on: the old samples go
        self.assertEqual(self.read("SELECT COUNT(DISTINCT hour) FROM stock_hour"), [(1,)])

    def test_reserve_flow_reads_units_per_hour_over_a_window_and_says_when_the_record_is_short(self):
        noon = store.epoch("2026-11-16T12:10:00Z")
        self.one(now=noon)
        book = json.loads(json.dumps(BOOK))
        book["pilots"]["drone-3"] = {"read_at": "2026-11-16T13:00:00Z", "stations": {"base_a": {"iron_ore": 500, "water_ice": 40}}}
        self.bump(self.data / "stock" / "storage.json", book)
        self.one(now=noon + 2 * 3600)                                                            # two hours later, Military stored 500 ore
        conn = store.connect(str(self.data))
        self.addCleanup(conn.close)
        flow = store.reserve_flow(conn, ["iron_ore", "steel_plate"], (1, 4))
        self.assertEqual((flow["hours"], flow["base"][1], flow["base"][4]), (2.0, (store.epoch("2026-11-16T12:00:00Z"), 2.0, False),
                                                                            (store.epoch("2026-11-16T12:00:00Z"), 2.0, True)))   # 4 hours asked, 2 on record
        rows = {(r["division"], r["item"]): (r["units"], r["rate"][1], r["rate"][4]) for r in flow["rows"]}
        self.assertEqual(rows, {("Military", "iron_ore"): (500, 250.0, 250.0), ("Mining", "iron_ore"): (17, 0.0, 0.0), ("Trade", "iron_ore"): (7, 0.0, 0.0),
                                ("Trade", "steel_plate"): (5, 0.0, 0.0)})                         # water ice is no reserve item here
        self.assertEqual(flow["sums"]["Military"], {"items": 1, "units": 500, "rate": {1: 250.0, 4: 250.0}})
        self.assertEqual(flow["sums"]["Trade"]["units"], 12)
        self.assertEqual(len(store.reserve_flow(conn)["rows"]), 6)                               # no list: every item
        single = tempfile.TemporaryDirectory(prefix="fleet-store-flow-")
        self.addCleanup(single.cleanup)
        fixture(Path(single.name) / "data", Path(single.name) / "game", self.now)
        store.one_pass(str(Path(single.name) / "data"), now=noon, root=str(Path(single.name) / "game"))
        one = store.connect(str(Path(single.name) / "data"))
        self.addCleanup(one.close)
        flow = store.reserve_flow(one, None, (4,))
        self.assertEqual((flow["hours"], flow["base"][4][2], {r["rate"][4] for r in flow["rows"]}), (0.0, True, {None}))   # one sample is no rate

    def test_status_lists_the_snapshot_tables_and_the_files_not_read(self):
        (self.data / "empire" / "empire.json").unlink()
        self.one()
        lines = "\n".join(store.status(str(self.data), now=self.now + 60))
        self.assertRegex(lines, r"books\s+3 rows\s+newest source \S+, \d+ s old, 2 files")
        self.assertRegex(lines, r"faction\s+0 rows\s+no source read")
        self.assertIn("not read: empire/empire.json: missing: our empire's collector has not written it yet", lines)


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-store-query-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "game"
        fixture(self.data, self.root, time.time())
        store.one_pass(str(self.data), root=str(self.root))

    def ask(self, sql, **options):
        return store.query(str(self.data), sql, **options)

    def test_a_select_and_a_with_are_answered(self):
        found = self.ask("SELECT pilot, fuel FROM ships ORDER BY pilot")
        self.assertEqual((found["columns"], found["rows"], found["cut"], found["error"]), (["pilot", "fuel"], [("Flag One", 10), ("miner-1", 10), ("trader-2", 10)], False, None))
        found = self.ask("  -- a comment first\n WITH a AS (SELECT id FROM systems) SELECT COUNT(*) AS n FROM a;")
        self.assertEqual((found["columns"], found["rows"]), (["n"], [(3,)]))
        self.assertEqual(self.ask("SELECT name FROM pragma_table_info('ships') LIMIT 1")["rows"], [("pilot",)])

    def test_writing_and_more_than_one_statement_are_refused(self):
        refused = ["INSERT INTO meta VALUES ('x', 1)", "UPDATE ships SET fuel = 0", "DELETE FROM ships", "DROP TABLE ships",
                   "ATTACH DATABASE '%s' AS other" % (Path(self.temp.name) / "other.db"), "PRAGMA query_only = 0", "PRAGMA user_version = 7",
                   "SELECT 1; DELETE FROM ships", "SELECT 1; SELECT 2", "", "   ", "-- only a comment", ";",
                   "WITH a AS (SELECT 1) DELETE FROM ships", "WITH a AS (SELECT 1) UPDATE ships SET fuel = 0",
                   "WITH a AS (SELECT 1) INSERT INTO meta VALUES ('x', 1)", "SELECT load_extension('x')", "VACUUM", "BEGIN", "CREATE TABLE x (y)"]
        for sql in refused:
            found = self.ask(sql)
            self.assertTrue(found["error"], sql)
            self.assertNotIn("\n", found["error"])
            self.assertNotIn("Traceback", found["error"])
            self.assertEqual((found["rows"], found["columns"]), ([], []), sql)
        self.assertEqual(self.ask("SELECT COUNT(*) FROM ships")["rows"], [(3,)])
        self.assertEqual(self.ask("SELECT COUNT(*) FROM meta WHERE key = 'x'")["rows"], [(0,)])
        self.assertFalse((Path(self.temp.name) / "other.db").exists())
        self.assertIn("refused", self.ask("WITH a AS (SELECT 1) DELETE FROM ships")["error"])
        self.assertIn("one statement", self.ask("SELECT 1; SELECT 2")["error"])
        self.assertIn("no statement", self.ask("")["error"])
        self.assertIn("no such table: nowhere", self.ask("SELECT * FROM nowhere")["error"])

    def test_the_authorizer_itself_refuses_attach_and_a_pragma_that_writes(self):
        conn = sqlite3.connect(":memory:")
        self.addCleanup(conn.close)
        conn.execute("CREATE TABLE t (x)")
        conn.set_authorizer(store.reads_only)
        for sql in ("ATTACH DATABASE ':memory:' AS other", "PRAGMA user_version = 7", "PRAGMA journal_mode = DELETE", "INSERT INTO t VALUES (1)",
                    "SELECT load_extension('x')"):
            with self.assertRaises(sqlite3.DatabaseError, msg=sql):
                conn.execute(sql)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM t").fetchone(), (0,))
        self.assertEqual(conn.execute("SELECT name FROM pragma_table_info('t')").fetchall(), [("x",)])

    def test_an_endless_statement_is_stopped_in_time(self):
        begun = time.monotonic()
        found = self.ask("WITH RECURSIVE r(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM r) SELECT COUNT(*) FROM r", seconds=0.3)
        self.assertLess(time.monotonic() - begun, 5)
        self.assertEqual((found["error"], found["rows"]), ("stopped: the statement ran longer than 0.3 s", []))

    def test_the_row_limit_cuts_and_says_so(self):
        found = self.ask("SELECT a, b FROM lanes ORDER BY a, b", limit=2)
        self.assertEqual((len(found["rows"]), found["cut"]), (2, True))
        found = self.ask("SELECT a, b FROM lanes", limit=4)
        self.assertEqual((len(found["rows"]), found["cut"]), (4, False))

    def test_no_read_copy_is_one_plain_line(self):
        found = store.query(str(Path(self.temp.name) / "empty"), "SELECT 1")
        self.assertIn("no read copy yet", found["error"])

    def test_schema_describes_every_table_and_view_the_store_makes_and_every_example_runs(self):
        made = set(re.findall(r"CREATE (?:TABLE|VIEW) IF NOT EXISTS (\w+)", store.SCHEMA + store.snapshot_schema()))
        conn = store.connect(str(self.data))
        self.addCleanup(conn.close)
        found = store.schema(conn)
        self.assertEqual(set(found), made)
        self.assertEqual(set(store.DESCRIPTIONS), made)                       # no description of a table that is not made
        for name, entry in found.items():
            self.assertTrue(entry["description"], "%s has no description" % name)
            self.assertTrue(entry["columns"], name)
            self.assertEqual(len(entry["examples"]), 3, name)
            for question, sql in entry["examples"]:
                answer = self.ask(sql)
                self.assertIsNone(answer["error"], "%s: %s: %s" % (name, question, answer["error"]))
        self.assertEqual(found["fleet_positions"]["kind"], "view")
        self.assertIn(("flies", "TEXT"), found["ships"]["columns"])
        for name, columns in store.COLUMNS.items():                           # every column can be asked for by its bare name
            self.assertIsNone(self.ask("SELECT %s FROM %s" % (", ".join(columns), name))["error"], name)

    def test_hive_sql_and_schema_from_the_command_line(self):
        command = [sys.executable, "-I", "-B", str(HIVE)]
        done = subprocess.run(command + ["sql", "SELECT id, jumps FROM systems ORDER BY jumps", "--limit", "2", "--data", str(self.data)],
                              capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        lines = done.stdout.splitlines()
        self.assertRegex(lines[0], r"^SQL \| 2 rows \(cut at --limit 2: more rows match")
        self.assertRegex(lines[1], r"^  id\s+jumps$")
        self.assertRegex(lines[3], r"^  sys_a\s+0$")
        done = subprocess.run(command + ["sql", "DELETE FROM ships", "--data", str(self.data)], capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 1)
        self.assertIn("refused", done.stdout)
        done = subprocess.run(command + ["schema", "--data", str(self.data)], capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("TABLE ships -- now: one row per ship of ours", done.stdout)
        self.assertIn("VIEW fleet_positions -- view:", done.stdout)
        done = subprocess.run(command + ["schema", "facilities", "--data", str(self.data)], capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("faction_service_type = 'faction_recruitment'", done.stdout)
        self.assertEqual(done.stdout.count("\n  -- "), 3)


if __name__ == "__main__":
    unittest.main()
