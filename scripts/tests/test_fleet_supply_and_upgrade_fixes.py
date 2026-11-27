"""Regression tests for zero-idle order naming, battle escape, prestige quote fail, station fuel hubs, and 5B crafting."""
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))

import craft_net
import fuelplan
import upgrades


class TestSupplyAndUpgradeFixes(unittest.TestCase):
    def test_bursar_and_haul_use_canonical_pilot_order_filenames(self):
        for rel in ("game/fleet/bursar.py", "game/fleet/haul.py"):
            txt = (REPO / rel).read_text(encoding="utf-8")
            self.assertNotIn('"orders" / ship_file_name(pilot)', txt, f"{rel} still uses ship_file_name for orders!")
            self.assertIn('"orders" / (pilot + ".json")', txt, f"{rel} missing canonical pilot + .json order path!")

    def test_owned_fuel_depots_includes_station_refueling_dock(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "store").mkdir(parents=True)
            con = sqlite3.connect(d / "store" / "read.db")
            con.execute("CREATE TABLE bases (system TEXT, poi TEXT, base TEXT, kind TEXT)")
            con.execute("CREATE TABLE faction_facilities (base TEXT, type TEXT, status TEXT)")
            con.execute("CREATE TABLE faction_storage (base TEXT, item TEXT, units INTEGER)")
            con.execute("INSERT INTO bases VALUES ('ridgecrest', 'poi_rc', 'base_rc', 'station')")
            con.execute("INSERT INTO faction_facilities VALUES ('base_rc', 'refueling_dock', 'active')")
            con.execute("INSERT INTO faction_storage VALUES ('base_rc', 'fuel', 3500)")
            con.commit()
            con.close()
            depots = fuelplan.owned_fuel_depots(d, min_fuel=200)
            self.assertIn("ridgecrest", depots)
            self.assertEqual(depots["ridgecrest"], ("poi_rc", "base_rc"))

    def test_upgrades_escape_battle_sends_flee_and_retreat(self):
        calls = []

        class FakeGate:
            @staticmethod
            def q(s):
                return s

            @staticmethod
            def call(method, path, body=None, timeout=60):
                calls.append((path, body))
                act = (body or {}).get("action")
                if act == "status":
                    return 200, json.dumps({"result": "You are not in an active battle."})
                return 200, json.dumps({"ok": True})

        old_sleep = upgrades.time.sleep
        upgrades.time.sleep = lambda _s: None
        try:
            ok = upgrades._escape_battle(FakeGate, "GSV Asclepius", wait_ticks=1)
        finally:
            upgrades.time.sleep = old_sleep
        self.assertTrue(ok)
        actions = [(b.get("toolGroup"), b.get("action"), b.get("params")) for _p, b in calls]
        self.assertIn(("spacemolt_battle", "stance", {"stance": "flee"}), actions)
        self.assertIn(("spacemolt_battle", "retreat", {}), actions)

    def test_craft_net_5b_workshop_crafts_industrial_supply_first_and_skips_cooled(self):
        world = {
            "recipes": {
                "bad_fuel": {"id": "bad_fuel", "inputs": [("plasma_gas", 4)], "outputs": [("fuel_cell", 1)], "facility_only": False},
                "good_fuel": {"id": "good_fuel", "inputs": [("liquid_hydrogen", 2), ("steel_plate", 1)], "outputs": [("fuel_cell", 1)], "facility_only": False},
            },
            "books_by_base": {"node_beta": {}},
            "global_bid": {},
            "item_vals": {},
            "need_crafts": {"fuel_cell"},
            "need_craft_caps": {"fuel_cell": 2400},
            "stock_by_item": {"fuel_cell": 200},
            "demand": {"industrial_targets": {"fuel_cell": {"cap": 2400}}},
            "reserve_items": {"fuel_cell"},
        }
        pol = {
            "enabled": True,
            "max_runs_per_cycle": 10,
            "logistics": {"enabled": True, "use_needs_tsv": True, "use_industrial_targets": True, "allow_buy_inputs_docked": False},
            "trade": {"enabled": True},
        }
        stored = {"plasma_gas": 40, "liquid_hydrogen": 20, "steel_plate": 10}
        job = craft_net.pick_craft_job(
            "Trade", "node_beta", stored, 50000, world, pol,
            skip_recipes={"bad_fuel"}, wing="5B. Mobile Field Workshops",
        )
        self.assertIsNotNone(job)
        self.assertEqual(job["recipe"], "good_fuel")
        self.assertEqual(job["mode"], "industrial")


if __name__ == "__main__":
    unittest.main()
