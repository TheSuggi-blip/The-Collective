#!/usr/bin/env python3
"""Tests for dynamic docked manufacturing craft_net.py (P5 Trade commercial vs Logistics industrial)
and craft-demand expansion."""
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import craft_net


class TestCraftNet(unittest.TestCase):
    def test_strict_p5_commercial_vs_industrial_and_demand_expansion(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            repo = Path(tmp) / "repo"
            (data / "store").mkdir(parents=True, exist_ok=True)
            (repo / "game").mkdir(parents=True, exist_ok=True)

            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE recipes (id TEXT, name TEXT, facility_only INTEGER);
                CREATE TABLE recipe_inputs (recipe TEXT, item TEXT, units INTEGER);
                CREATE TABLE recipe_outputs (recipe TEXT, item TEXT, units INTEGER);
                CREATE TABLE items (id TEXT, base_value REAL);
                CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER);
                CREATE TABLE need_status (id TEXT, craft TEXT);
                CREATE TABLE supply_status (item TEXT, stock INTEGER, keep INTEGER);
                INSERT INTO recipes VALUES ('smelt_steel', 'Smelt Steel', 0), ('make_armor_ii', 'Make Armor II', 0), ('fac_only', 'Station Core', 1);
                INSERT INTO recipe_inputs VALUES ('smelt_steel', 'iron_ore', 4), ('make_armor_ii', 'steel_plate', 2), ('fac_only', 'steel_plate', 100);
                INSERT INTO recipe_outputs VALUES ('smelt_steel', 'steel_plate', 1), ('make_armor_ii', 'armor_plate_ii', 1), ('fac_only', 'station_core', 1);
                INSERT INTO items VALUES ('iron_ore', 5), ('steel_plate', 40), ('armor_plate_ii', 1200);
                INSERT INTO books VALUES ('hub1', 'steel_plate', 30, 50, 50, 200), ('hub1', 'armor_plate_ii', 1400, 20, 1800, 5), ('hub1', 'iron_ore', 4, 100, 6, 500);
                INSERT INTO need_status VALUES ('atria', 'steel_plate 100');
                INSERT INTO supply_status VALUES ('iron_ore', 10000, 60000);
            """)
            con.commit()
            con.close()

            pol = json.loads((ROOT / "game" / "craft-policy.json").read_text(encoding="ascii"))
            dem = json.loads((ROOT / "game" / "craft-demand.json").read_text(encoding="ascii"))
            (repo / "game" / "craft-demand.json").write_text(json.dumps(dem), encoding="ascii")

            world = craft_net.load_craft_world(str(data), str(repo), pol)
            raw_dem = craft_net.expand_demand_raw_inputs(world)
            self.assertIn("iron_ore", raw_dem)
            self.assertIn("steel_plate", raw_dem)

            # 1. Trade picks high-margin commercial armor_plate_ii (bid 1400 vs input cost 100)
            t_job = craft_net.pick_craft_job("Trade", "hub1", {"steel_plate": 10}, 50000, world, pol)
            self.assertIsNotNone(t_job)
            self.assertEqual(t_job["mode"], "commercial")
            self.assertEqual(t_job["makes"], "armor_plate_ii")
            self.assertGreater(t_job["est_profit"], 5000)

            # 2. Logistics picks industrial steel_plate (never sells, strict P5)
            l_job = craft_net.pick_craft_job("Logistics", "hub1", {"iron_ore": 40}, 50000, world, pol)
            self.assertIsNotNone(l_job)
            self.assertEqual(l_job["mode"], "industrial")
            self.assertEqual(l_job["makes"], "steel_plate")
            self.assertEqual(l_job["sell_price"], 0)


if __name__ == "__main__":
    unittest.main()
