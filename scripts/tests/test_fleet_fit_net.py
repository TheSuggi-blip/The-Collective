#!/usr/bin/env python3
"""Tests for dynamic multi-specialty fit_net.py & policy-driven upgrades.auto_enqueue_upgrades."""
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import fit_net
import upgrades


class TestFitNetAndAutoUpgrade(unittest.TestCase):
    def test_fit_net_preserves_specialty_strips_offrole_and_skips_when_full(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            (data / "store").mkdir(parents=True, exist_ok=True)
            (data / "fleet").mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE lanes (a TEXT, b TEXT);
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, base TEXT);
                CREATE TABLE hulls (id TEXT, name TEXT, tier INTEGER, weapon_slots INTEGER, defense_slots INTEGER, utility_slots INTEGER);
                CREATE TABLE books (base TEXT, item TEXT, ask REAL, ask_qty INTEGER);
                INSERT INTO lanes VALUES ('s1', 's2');
                INSERT INTO systems VALUES ('s1', 'voidborn', 0), ('s2', 'voidborn', 0);
                INSERT INTO places VALUES ('s1', 'p1', 'b1'), ('s2', 'p2', 'b2');
                INSERT INTO hulls VALUES ('t0_miner', 'Skiff', 0, 1, 1, 2), ('t0_trader', 'Trader', 0, 0, 1, 2);
                INSERT INTO books VALUES ('b2', 'ice_harvester_iii', 7000, 5), ('b2', 'shield_booster_iv', 8000, 5), ('b2', 'mining_laser_iii', 7000, 5);
            """)
            con.commit()
            con.close()
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({"b1": {"pilot": "trader-1"}}), encoding="ascii")

            pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii"))
            world = fit_net.load_fit_world(str(data), pol)

            # 1. Ice miner keeps ice specialty (detect_by_module), strips pulse_laser_i, fits ice_harvester_iii + shield_booster_iv
            ship = {"name": "miner-1", "division": "Mining", "system": "s1", "class": "t0_miner", "credits": 40000, "modules": ["ice_harvester_i", "pulse_laser_i"]}
            plan = fit_net.plan_ship_fit(ship, world, pol)
            self.assertIsNotNone(plan)
            self.assertEqual(plan["specialty"], "ice")
            self.assertEqual(plan["unfit"], ["pulse_laser_i"])
            bought_ids = [m for m, _p in plan["buy_fit"]]
            self.assertIn("ice_harvester_iii", bought_ids)
            self.assertIn("shield_booster_iv", bought_ids)

            # 2. Already cleanly fitted ship returns None (0ms dispatch skip!)
            ship_full = {"name": "miner-2", "division": "Mining", "system": "s1", "class": "t0_miner", "credits": 40000, "modules": ["mining_laser_iii", "cargo_expander_iii", "shield_booster_iv"]}
            self.assertIsNone(fit_net.plan_ship_fit(ship_full, world, pol))

            # 3. Bursar desk ship strips off-role laser ONLY, buys 0 modules (no wasted CapEx!)
            bursar_ship = {"name": "trader-1", "division": "Trade", "system": "s1", "class": "t0_trader", "credits": 40000, "modules": ["mining_laser_i"]}
            b_plan = fit_net.plan_ship_fit(bursar_ship, world, pol)
            self.assertIsNotNone(b_plan)
            self.assertEqual(b_plan["specialty"], "bursar")
            self.assertEqual(b_plan["unfit"], ["mining_laser_i"])
            self.assertEqual(b_plan["buy_fit"], [])

    def test_auto_enqueue_respects_treasury_floor_bursar_exclusion_and_mix(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            repo = Path(tmp) / "repo"
            (data / "store").mkdir(parents=True, exist_ok=True)
            (data / "fleet").mkdir(parents=True, exist_ok=True)
            (repo / "game").mkdir(parents=True, exist_ok=True)

            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE faction (treasury INTEGER);
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, base TEXT);
                CREATE TABLE hulls (id TEXT, name TEXT, tier INTEGER);
                CREATE TABLE ships (pilot TEXT, division TEXT, empire TEXT, class TEXT);
                CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INTEGER);
                CREATE TABLE ship_listings (class_id TEXT, base TEXT, price INTEGER, t INTEGER);
                INSERT INTO faction VALUES (10000000);
                INSERT INTO systems VALUES ('s1', 'crimson', 0);
                INSERT INTO places VALUES ('s1', 'p1', 'crimson_hub');
                INSERT INTO hulls VALUES ('t0_hull', 'Starter', 0), ('broadaxe', 'Broadaxe', 2), ('prayer', 'Prayer', 1);
                INSERT INTO ships VALUES ('drone-1', 'Military', 'crimson', 't0_hull'),
                                         ('trader-1', 'Trade', 'voidborn', 't0_hull'),
                                         ('trader-2', 'Trade', 'voidborn', 't0_hull');
                INSERT INTO ship_skills VALUES ('drone-1', 'piloting', 12), ('trader-1', 'piloting', 5), ('trader-2', 'piloting', 5);
                INSERT INTO ship_listings VALUES ('broadaxe', 'crimson_hub', 95000, 1795500000),
                                                 ('prayer', 'crimson_hub', 30000, 1795500000);
            """)
            con.commit()
            con.close()
            # trader-1 is a Bursar desk (must be EXCLUDED); trader-2 is mobile Trade (eligible!)
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({"crimson_hub": {"pilot": "trader-1"}}), encoding="ascii")
            pol = json.loads((ROOT / "game" / "upgrade-policy.json").read_text(encoding="ascii"))
            (repo / "game" / "upgrade-policy.json").write_text(json.dumps(pol), encoding="ascii")

            res = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500100)
            pilots_added = {a["pilot"]: a["hull"] for a in res["added"]}
            self.assertEqual(pilots_added.get("drone-1"), "broadaxe")
            self.assertEqual(pilots_added.get("trader-2"), "prayer")
            self.assertNotIn("trader-1", pilots_added)

            # Drop treasury below floor (8.5M) -> must refuse all auto-enqueues!
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.execute("UPDATE faction SET treasury = 5000000")
            con.commit()
            con.close()
            res2 = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500200)
            self.assertEqual(res2["added"], [])
            self.assertIn("floor", res2.get("skipped", ""))


if __name__ == "__main__":
    unittest.main()
