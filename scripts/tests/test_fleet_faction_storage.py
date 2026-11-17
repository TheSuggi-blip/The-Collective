"""What each faction storage holds and where our bases stand (DECISIONS Q67 (2) and (3)): game/fleet/empire.py collect
views the faction's storage at each place it stores through the gate's read (a fake here), keeps a place's last reading
when its view fails, reads the fuel of a bunker from the faction's info, takes a base's id and place from our census;
store.py loads the rows into the table faction_storage and the view inventory_faction counts them with their worth;
hive.py empire (empire.py show) prints them. No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

REPO = Path(__file__).resolve().parents[2]
OUTPOST = "0123456789abcdef0123456789abcdef"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


empire = load("empire_storage_under_test", REPO / "game" / "fleet" / "empire.py")
store = load("store_storage_under_test", REPO / "game" / "fleet" / "store.py")
state_tests = load("store_state_fixture_for_storage", REPO / "scripts" / "tests" / "test_fleet_store_state.py")

INFO = {"id": "f1", "name": "The Test", "tag": "TEST", "leader_username": "Lead Ship", "member_count": 2, "owned_bases": 1, "at_war": False,
        "created_at": "2026-11-15T18:09:32Z", "members": [{"username": "Lead Ship", "role": "Leader"}]}
OWNED = {"facilities": [
    {"facility_id": "b1", "type_id": "faction_fuel_bunker", "name": "Faction Fuel Bunker", "base_id": OUTPOST, "system_id": "wild", "status": "active", "rent_per_cycle": 0},
    {"facility_id": "l1", "type_id": "faction_lockbox", "name": "Faction Lockbox", "base_id": OUTPOST, "system_id": "wild", "status": "active", "rent_per_cycle": 0},
    {"facility_id": "l2", "type_id": "faction_lockbox", "name": "Faction Lockbox", "base_id": "hub_station", "system_id": "home", "status": "active", "rent_per_cycle": 69},
    {"facility_id": "w3", "type_id": "faction_warehouse", "name": "Faction Warehouse", "base_id": "lab_station", "system_id": "lab", "status": "active", "rent_per_cycle": 261},
    {"facility_id": "h1", "type_id": "hiring_board", "name": "Hiring Board", "base_id": "board_station", "system_id": "home", "status": "active", "rent_per_cycle": 26}],
    "faction_rent": {"facilities": 5, "total_rent_per_cycle": 356, "est_rent_per_day": 30758}}
CATALOG = {"version": "9.9.9", "facilities": [
    {"id": "faction_lockbox", "name": "Faction Lockbox", "category": "faction", "level": 1, "build_cost": 200000, "faction_cap": 100000, "faction_service_type": "faction_storage"},
    {"id": "faction_warehouse", "name": "Faction Warehouse", "category": "faction", "level": 2, "build_cost": 750000, "faction_cap": 200000,
     "faction_service_type": "faction_storage", "upgrades_from": "faction_lockbox"}]}
EMPTY = {"credits": 5000, "items": [], "recent_activity": [], "hint": "No items in faction storage at any station."}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-faction-storage-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in ("fleet", "station", "catalog", "scouting"):
            (self.data / folder).mkdir(parents=True)
        (self.root / "game" / "map").mkdir(parents=True)
        put = lambda rel, value: (self.data / rel).write_text(json.dumps(value), encoding="utf-8")
        put("fleet/flagships.json", {"Lead Ship": {"of": "Unity", "role": "command"}})
        put("fleet/fleet.json", {"ships": [{"name": "Lead Ship"}]})
        put("station/stations.json", [{"name": "Test Rock", "type": "outpost", "system": "wild", "tag": "TEST", "condition": "thriving", "services": []},
                                      {"name": "Hub Station", "type": "station", "system": "home", "tag": "", "services": ["storage"]}])
        put("station/map.json", {"systems": [{"id": "wild", "name": "Wild", "empire": "", "jumps": 4}, {"id": "home", "name": "Home", "empire": "voidborn", "jumps": 0}]})
        put("catalog/9.9.9.json", CATALOG)
        put("scouting/wild.json", {"read_at": "2026-11-17T18:06:22Z", "system": {"id": "wild", "pois": [
            {"id": "wild_belt", "name": "Wild Belt", "type": "asteroid_belt", "has_base": False},
            {"id": "rock_place", "name": "Test Rock", "type": "station", "has_base": True, "base_id": OUTPOST, "base_name": "Test Rock", "base_type": "outpost"}]}, "pois": {}})
        put("scouting/home.json", {"read_at": "2026-11-17T18:00:00Z", "system": {"id": "home", "pois": [
            {"id": "hub_station", "name": "Hub Station", "type": "station", "has_base": True, "base_id": "hub_station", "base_name": "Hub Station"}]}, "pois": {}})
        (self.root / "game" / "map" / "sites.tsv").write_text("system\tpoi\tstatus\tproposed_by\tnote\n")
        self.calls = []

    def see(self, storage, info=INFO):
        """The gate's read faked: the faction, its facilities, the cards, and one storage view per place (`storage`: base ->
        an answer, or None for a failed view)."""
        def fake(pilot, group, action, params=None):
            self.calls.append((pilot, group, action, dict(params or {})))
            if (group, action) == ("spacemolt_storage", "view"):
                found = storage.get((params or {}).get("station_id"))
                return (found, "") if found is not None else (None, "Timeout: the gate did not answer")
            found = {("spacemolt_faction", "info"): info, ("spacemolt_facility", "faction_owned"): OWNED,
                     ("spacemolt_facility", "types"): {"rent_per_cycle": 1}}.get((group, action))
            return (found, "") if found is not None else (None, "no answer")
        return fake

    def collect(self, storage, info=INFO):
        return empire.collect(str(self.data), str(self.root), see=self.see(storage, info), pause=0, now=1794945600)


class CollectTests(Tree):
    def test_each_place_where_the_faction_stores_is_viewed_once_and_its_goods_are_rows(self):
        held = dict(EMPTY, items=[{"item_id": "steel_plate", "name": "Steel Plate", "quantity": 120}, {"item_id": "iron_ore", "quantity": 7},
                                  {"item_id": "copper_ore", "quantity": 3, "base_id": "hub_station"}])        # an item filed under another base is that base's
        state, notes = self.collect({OUTPOST: held, "hub_station": EMPTY, "lab_station": EMPTY})
        views = [c[3] for c in self.calls if c[1:3] == ("spacemolt_storage", "view")]
        self.assertEqual(views, [{"target": "faction", "station_id": OUTPOST}, {"target": "faction", "station_id": "hub_station"},
                                 {"target": "faction", "station_id": "lab_station"}])     # the outpost, then each base of the storage line; no hiring board
        self.assertEqual({c[0] for c in self.calls}, {"Lead Ship"})
        self.assertEqual([(r["base"], r["base_name"], r["item"], r["units"]) for r in state["faction_storage"]],
                         [(OUTPOST, "Test Rock", "iron_ore", 7), (OUTPOST, "Test Rock", "steel_plate", 120)])
        self.assertEqual(state["faction_storage_error"], "")
        self.assertEqual(state["faction_storage_places"], [{"base": OUTPOST, "base_name": "Test Rock"}, {"base": "hub_station", "base_name": "Hub Station"},
                                                           {"base": "lab_station", "base_name": "lab_station"}])
        self.assertEqual(notes, ["the fuel of the bunker(s) at %s not read: no field of the faction's info holds it" % OUTPOST])

    def test_the_outpost_takes_its_base_id_and_place_from_our_census_and_is_no_office(self):
        state, _notes = self.collect({OUTPOST: EMPTY, "hub_station": EMPTY, "lab_station": EMPTY})
        self.assertEqual([(b["base"], b["name"], b["system"], b["poi"], b["kind"]) for b in state["bases"]], [(OUTPOST, "Test Rock", "wild", "rock_place", "outpost")])
        self.assertEqual([(t["system"], t["claim"]) for t in state["territory"]], [("wild", "outpost"), ("home", "office"), ("lab", "office")])
        (self.data / "scouting" / "wild.json").unlink()                 # no census: the one base id our facilities name there, no place
        state, _notes = self.collect({OUTPOST: EMPTY, "hub_station": EMPTY, "lab_station": EMPTY})
        self.assertEqual([(b["base"], b["poi"]) for b in state["bases"]], [(OUTPOST, "")])

    def test_a_view_that_fails_keeps_the_last_reading_of_its_place_and_says_why(self):
        first, _notes = self.collect({OUTPOST: dict(EMPTY, items=[{"item_id": "steel_plate", "quantity": 120}]),
                                      "hub_station": dict(EMPTY, items=[{"item_id": "water_ice", "quantity": 9}]), "lab_station": EMPTY})
        empire.save(str(self.data), first)
        state, notes = self.collect({OUTPOST: EMPTY, "lab_station": EMPTY})      # the hub's view fails, the outpost was emptied
        self.assertEqual([(r["base"], r["item"], r["units"], r["read_at"]) for r in state["faction_storage"]],
                         [("hub_station", "water_ice", 9, first["written_at"])])        # the old row, with the time it was read
        self.assertEqual(state["faction_storage_error"], "Hub Station: Timeout: the gate did not answer")
        self.assertIn("faction storage not read at Hub Station: Timeout: the gate did not answer: the last reading of each stays", notes)
        self.assertEqual(self.collect({OUTPOST: {"credits": 1, "items": None}, "hub_station": {"error_free": True}, "lab_station": EMPTY})[0]["faction_storage_error"],
                         "Hub Station: no list `items` in the answer")                  # `items: null` is an empty place; no list and no hint is no storage view

    def test_the_fuel_of_a_bunker_is_read_from_the_faction_info(self):
        empty = {OUTPOST: EMPTY, "hub_station": EMPTY, "lab_station": EMPTY}
        fuel = lambda state: [(r["base"], r["base_name"], r["units"]) for r in state["faction_storage"] if r["item"] == "fuel"]
        state, notes = self.collect(empty, dict(INFO, fuel_bunkers=[{"base_id": OUTPOST, "fuel_reserve": 1200, "fuel_capacity": 50000}]))
        self.assertEqual((fuel(state), notes), ([(OUTPOST, "Test Rock", 1200)], []))
        self.assertEqual(fuel(self.collect(empty, dict(INFO, fuel_bunkers=[{"fuel_reserve": 300}]))[0]), [(OUTPOST, "Test Rock", 300)])   # one bunker: its base
        state, _notes = self.collect(empty, dict(INFO, total_fuel_reserve=0, total_fuel_capacity=50000))
        self.assertEqual(fuel(state), [(OUTPOST, "Test Rock", 0)])                         # an empty bunker is a row of 0, not a fact left out
        empire.save(str(self.data), state)
        self.assertEqual(fuel(self.collect(empty, None)[0]), [(OUTPOST, "Test Rock", 0)])   # no info: the last reading stays

    def test_show_prints_each_place_with_its_goods_or_empty(self):
        state, _notes = self.collect({OUTPOST: dict(EMPTY, items=[{"item_id": "steel_plate", "quantity": 1200}]), "hub_station": EMPTY, "lab_station": EMPTY},
                                     dict(INFO, total_fuel_reserve=40))
        empire.save(str(self.data), state)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(empire.show(str(self.data)), 0)
        text = out.getvalue()
        self.assertIn("  Test Rock (outpost) in wild, thriving | place rock_place, base id %s\n" % OUTPOST, text)
        self.assertIn("FACTION STORAGE | 3 place(s) | read 2026-11-17T20:00:00Z\n", text)
        self.assertIn("  Test Rock (%s): 1,200 steel_plate, 40 fuel\n" % OUTPOST, text)
        self.assertIn("  Hub Station (hub_station): empty\n", text)
        self.assertIn("  lab_station: empty\n", text)
        done = subprocess.run([sys.executable, "-I", "-B", str(REPO / "game" / "fleet" / "hive.py"), "empire", "--data", str(self.data)],
                              capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("  Test Rock (%s): 1,200 steel_plate, 40 fuel\n" % OUTPOST, done.stdout)    # hive.py empire is empire.py show
        empire.save(str(self.data), {k: v for k, v in state.items() if not k.startswith("faction_storage")})
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            empire.show(str(self.data))
        self.assertIn("FACTION STORAGE | not read yet", out.getvalue())

    def test_a_storage_view_is_the_only_new_call_and_only_a_view(self):
        self.assertIn(("spacemolt_storage", "view"), empire.VIEWS)
        for action in ("deposit", "withdraw"):
            self.assertEqual(empire.look("Lead Ship", "spacemolt_storage", action, {"target": "faction"})[0], None)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-faction-storage-store-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "game"
        self.now = time.time()
        state_tests.fixture(self.data, self.root, self.now)
        path = self.data / "empire" / "empire.json"
        held = json.loads(path.read_text())
        held["faction_storage"] = [{"base": "base_o", "base_name": "Our Outpost", "item": "steel_plate", "units": 30, "read_at": "2026-11-16T11:50:00Z"},
                                   {"base": "base_o", "base_name": "Our Outpost", "item": "fuel", "units": 500, "read_at": "2026-11-16T11:50:00Z"},
                                   {"base": "base_a", "base_name": "A Station", "item": "iron_ore", "units": 4}]
        path.write_text(json.dumps(held))

    def read(self, sql):
        conn = store.connect(str(self.data))
        try:
            return conn.execute(sql).fetchall()
        finally:
            conn.close()

    def test_the_store_loads_the_rows_and_the_view_counts_them_with_their_worth(self):
        out = store.one_pass(str(self.data), now=self.now, root=str(self.root))
        self.assertEqual(out["snapshot"]["problems"], [])
        self.assertEqual(self.read("SELECT base, base_name, item, units, t FROM faction_storage ORDER BY base, item"),
                         [("base_a", "A Station", "iron_ore", 4, store.epoch(state_tests.STAMP)),       # no time of its own: the reading's
                          ("base_o", "Our Outpost", "fuel", 500, store.epoch("2026-11-16T11:50:00Z")),
                          ("base_o", "Our Outpost", "steel_plate", 30, store.epoch("2026-11-16T11:50:00Z"))])
        self.assertEqual(self.read("SELECT place, base_name, item, name, units, base_value, worth FROM inventory_faction ORDER BY place, item"),
                         [("faction:base_a", "A Station", "iron_ore", "Iron Ore", 4, 5, 20), ("faction:base_o", "Our Outpost", "fuel", None, 500, None, None),
                          ("faction:base_o", "Our Outpost", "steel_plate", "Steel Plate", 30, 60, 1800)])
        craftbook = load("craftbook_beside_faction_storage", REPO / "game" / "fleet" / "craftbook.py")
        owned = craftbook.inventory(str(self.data))                 # the storage book's views stay craftbook.py's sums
        self.assertEqual({r["id"]: r["units"] for g in owned["groups"] for r in g["rows"]}, dict(self.read("SELECT item, units FROM inventory")))
        self.assertEqual(self.read("SELECT COUNT(*) FROM inventory_by_station WHERE place LIKE 'faction:%'"), [(0,)])
        path = self.data / "empire" / "empire.json"
        held = json.loads(path.read_text())
        held["faction_storage"] = []
        path.write_text(json.dumps(held))
        later = path.stat().st_mtime + 7
        os.utime(path, (later, later))
        store.one_pass(str(self.data), now=self.now + 30, root=str(self.root))
        self.assertEqual(self.read("SELECT COUNT(*) FROM faction_storage"), [(0,)])          # an emptied storage leaves no row
        self.assertEqual(self.read("SELECT COUNT(*) FROM bases"), [(1,)])


if __name__ == "__main__":
    unittest.main()
