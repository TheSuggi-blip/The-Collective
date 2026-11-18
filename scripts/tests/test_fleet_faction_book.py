"""The faction's storage in the storage book (requests ENT-267, Apollo): the service ledger puts the faction's own reading
(data/empire/empire.json, faction_storage: empire.py collect, views only) into data/stock/storage.json as the entry and
member `Faction` (game/fleet/factionbook.py), so that the book's totals, the table holdings, craftbook's inventory and
surplus.py reserve count what lies in the Lockboxes and at the outpost. The ledger's pass runs here with a fleet of no
ship: no call reaches the gate. No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
OUTPOST = "443f0c5b2a1fbbcea95d13b76a797fe9"
EMPIRE = {"written_at": "2026-11-18T01:04:40Z", "faction_storage_error": "",
          "faction_storage": [{"base": OUTPOST, "base_name": "CLTV Outpost GSC-0044", "item": "copper_ore", "units": 40, "read_at": "2026-11-18T01:04:38Z"},
                              {"base": OUTPOST, "base_name": "CLTV Outpost GSC-0044", "item": "iron_ore", "units": 155, "read_at": "2026-11-18T01:04:38Z"},
                              {"base": OUTPOST, "base_name": "CLTV Outpost GSC-0044", "item": "fuel", "units": 3615, "read_at": "2026-11-18T01:04:40Z"},
                              {"base": "node_beta_industrial_station", "base_name": "Node Beta Industrial Station", "item": "flex_polymer", "units": 285,
                               "read_at": "2026-11-18T00:49:10Z"}]}
CATALOG = {"version": "9.9.9", "items": [{"id": "flex_polymer", "name": "Flex Polymer", "category": "refined", "size": 1, "base_value": 30},
                                         {"id": "iron_ore", "name": "Iron Ore", "category": "ore", "size": 1, "base_value": 5},
                                         {"id": "copper_ore", "name": "Copper Ore", "category": "ore", "size": 1, "base_value": 6}],
           "recipes": [], "facilities": [{"id": "recruitment_center", "name": "Recruitment Center", "level": 3, "build_cost": 1,
                                          "build_materials": [{"item_id": "flex_polymer", "quantity": 300}]}], "ships": []}
MINER = {"read_at": "2026-11-18T00:30:00Z", "stations": {"node_beta_industrial_station": {"flex_polymer": 15, "iron_ore": 900}}}


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_book_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FactionBookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-faction-book-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in ("empire", "stock", "fleet", "catalog", "market"):
            (self.data / folder).mkdir(parents=True)
        (self.root / "game").mkdir(parents=True)
        (self.data / "empire" / "empire.json").write_text(json.dumps(EMPIRE))
        (self.data / "catalog" / "9.9.9.json").write_text(json.dumps(CATALOG))
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": "miner-1", "status": "connected"}]}))
        (self.data / "stock" / "storage.json").write_text(json.dumps({"pilots": {"miner-1": MINER}}))
        (self.root / "game" / "reserve.tsv").write_text("kind\tid\tunits\tnote\nfacility\trecruitment_center\t1\tthe upgrade at Node Beta\n")

    def ledger_pass(self):
        """One pass of the service `ledger` (--once) over a fleet that names no ship it may read: no call to the gate."""
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": []}))
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "FLEET_MEMBER": "ledger", "FLEET_TAXES": os.devnull, "HOME": self.temp.name}
        done = subprocess.run([sys.executable, "-I", "-B", str(FLEET / "ledger.py"), "--once", "--data", str(self.data)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, timeout=60)
        self.assertEqual(done.returncode, 0, done.stdout)
        return json.loads((self.data / "stock" / "storage.json").read_text())

    def test_the_ledger_s_pass_puts_the_faction_s_storage_into_the_book_as_member_faction(self):
        book = self.ledger_pass()
        self.assertEqual(book["pilots"]["Faction"]["stations"], {OUTPOST: {"copper_ore": 40, "iron_ore": 155},           # no bunker fuel: a tank, no item
                                                                 "node_beta_industrial_station": {"flex_polymer": 285}})
        self.assertEqual((book["pilots"]["Faction"]["member"], book["pilots"]["Faction"]["read_at"]), ("Faction", "2026-11-18T00:49:10Z"))   # its oldest place
        self.assertEqual(book["totals"]["by_station"]["node_beta_industrial_station"], {"flex_polymer": 300, "iron_ore": 900})
        self.assertEqual(book["totals"]["by_member"]["Faction"], {OUTPOST: {"copper_ore": 40, "iron_ore": 155}, "node_beta_industrial_station": {"flex_polymer": 285}})
        self.assertIn("miner-1", book["pilots"])                                       # a fleet file that names nobody takes nobody out

    def test_stock_surplus_reserve_and_the_table_holdings_count_it(self):
        self.ledger_pass()
        surplus = load("surplus")
        rows = {r["id"]: r for r in surplus.surplus(str(self.data), str(self.root))["rows"]}
        self.assertEqual((rows["flex_polymer"]["held"], rows["flex_polymer"]["short"]), (300, 0))       # it read 15 of 300, and the 285 were bought twice
        inventory = load("craftbook").inventory(str(self.data))
        self.assertEqual(next(r for g in inventory["groups"] for r in g["rows"] if r["id"] == "iron_ore")["units"], 1055)
        store = load("store")
        rows = store.read_storage(self.data / "stock" / "storage.json", {"data": str(self.data)})["holdings"]
        faction = sorted((r["pilot"], r["member"], r["place"], r["item"], r["units"]) for r in rows if r["pilot"] == "Faction")
        self.assertEqual(faction, [("Faction", "Faction", OUTPOST, "copper_ore", 40), ("Faction", "Faction", OUTPOST, "iron_ore", 155),
                                   ("Faction", "Faction", "node_beta_industrial_station", "flex_polymer", 285)])
        self.assertEqual({r["member"] for r in rows if r["pilot"] == "miner-1"}, {"Zero"})

    def test_the_entry_follows_the_reading_and_leaves_the_book_alone_without_one(self):
        ledger = load("ledger")
        book = {"pilots": {"miner-1": MINER}}
        self.assertTrue(ledger.factionbook.put(book, str(self.data)))
        self.assertFalse(ledger.factionbook.put(book, str(self.data)))                   # the same reading: nothing to write again
        ledger.leave(book, str(self.data))                                                # the fleet file names miner-1 only
        self.assertEqual(sorted(book["pilots"]), ["Faction", "miner-1"])                  # the faction's entry is no pilot
        failed = dict(EMPIRE, faction_storage_error="Node Beta Industrial Station: no answer")
        (self.data / "empire" / "empire.json").write_text(json.dumps(failed))
        self.assertTrue(ledger.factionbook.put(book, str(self.data)))
        self.assertEqual(book["pilots"]["Faction"]["error"], "Node Beta Industrial Station: no answer")
        (self.data / "empire" / "empire.json").unlink()
        self.assertFalse(ledger.factionbook.put(book, str(self.data)))                   # no reading: the last entry stays as it was
        self.assertIn("Faction", book["pilots"])


if __name__ == "__main__":
    unittest.main()
