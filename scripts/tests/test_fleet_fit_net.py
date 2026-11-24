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

    def test_live_module_dicts_and_cpu_power_caps(self):
        """The ship files keep modules as dicts ({"type": ...}); a buy must fit the hull's CPU and power."""
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            (data / "store").mkdir(parents=True, exist_ok=True)
            (data / "fleet").mkdir(parents=True, exist_ok=True)
            (data / "catalog").mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE lanes (a TEXT, b TEXT);
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, base TEXT);
                CREATE TABLE hulls (id TEXT, name TEXT, tier INTEGER, weapon_slots INTEGER, defense_slots INTEGER, utility_slots INTEGER, cpu INTEGER, power INTEGER);
                CREATE TABLE books (base TEXT, item TEXT, ask REAL, ask_qty INTEGER);
                INSERT INTO lanes VALUES ('s1', 's2');
                INSERT INTO systems VALUES ('s1', 'voidborn', 0), ('s2', 'voidborn', 0);
                INSERT INTO places VALUES ('s1', 'p1', 'b1'), ('s2', 'p2', 'b2');
                INSERT INTO hulls VALUES ('cobble', 'Cobble', 0, 1, 1, 2, 12, 24);
                INSERT INTO books VALUES ('b2', 'shield_booster_iv', 7800, 5), ('b2', 'survey_scanner_ii', 14000, 5);
            """)
            con.commit()
            con.close()
            (data / "catalog" / "0.734.2.json").write_text(json.dumps({"version": "0.734.2", "items": [
                {"id": "shield_booster_iv", "slot": "defense", "cpu_usage": 8, "power_usage": 15},
                {"id": "survey_scanner_ii", "slot": "utility", "cpu_usage": 5, "power_usage": 7},
                {"id": "mining_laser_i", "slot": "utility", "cpu_usage": 2, "power_usage": 5},
                {"id": "pulse_laser_i", "slot": "weapon", "cpu_usage": 2, "power_usage": 5}]}), encoding="ascii")
            pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii"))
            world = fit_net.load_fit_world(str(data), pol)
            ship = {"name": "scout-9", "division": "Intel", "system": "s1", "class": "Cobble", "credits": 60000,
                    "modules": [{"kind": "mining", "name": "Mining Laser I", "slot": "utility", "type": "mining_laser_i"},
                                {"kind": "weapon", "name": "Pulse Laser I", "slot": "weapon", "type": "pulse_laser_i"}]}
            plan = fit_net.plan_ship_fit(ship, world, pol)
            self.assertIsNotNone(plan)
            # 1. the off-role module of a live ship file is named by its type id, so it is stripped
            self.assertIn("mining_laser_i", plan["unfit"])
            # 2. what stays fitted plus what is bought stays within the hull's 12 CPU / 24 power:
            #    Shield Booster IV (8) and Survey Scanner II (5) together need 13 CPU, so only one is bought
            bought = [m for m, _p in plan["buy_fit"]]
            self.assertIn("shield_booster_iv", bought)
            self.assertNotIn("survey_scanner_ii", bought)
            off = set(pol["off_role_modules"]["Intel"])
            kept = [m["type"] for m in ship["modules"] if m["type"] not in off]
            cost = {"shield_booster_iv": (8, 15), "survey_scanner_ii": (5, 7), "mining_laser_i": (2, 5), "pulse_laser_i": (2, 5)}
            self.assertLessEqual(sum(cost[m][0] for m in kept + bought), 12)
            self.assertLessEqual(sum(cost[m][1] for m in kept + bought), 24)

    def test_royal_guard_command_and_military_support_specialties(self):
        pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii"))
        # 1. Sentinels 60/40 split: royal_guard_escort + royal_guard_utility
        specs = {fit_net.resolve_specialty(f"sentinel-{n}", "Military", [], pol) for n in range(1, 36)}
        self.assertEqual(specs, {"royal_guard_escort", "royal_guard_utility"})
        # 2. Frontline drones stay 100% pure firepower (brawler / ewar / flak_tank)
        d_specs = {fit_net.resolve_specialty(f"drone-{n}", "Military", [], pol) for n in range(1, 96)}
        self.assertEqual(d_specs, {"brawler", "ewar", "flak_tank"})
        # 3. Command Flagships: Prime Directive -> command_ewar_tac, 4 regional flagships -> command_stealth_ewar, core 6 hulls -> 4 support roles
        self.assertEqual(fit_net.resolve_specialty("Prime Directive", "Command", [], pol), "command_ewar_tac")
        self.assertEqual(fit_net.resolve_specialty("Crimson Aegis", "Command", [], pol), "command_stealth_ewar")
        self.assertEqual(fit_net.resolve_specialty("Solar Mandate", "Command", [], pol), "command_stealth_ewar")
        self.assertEqual(fit_net.resolve_specialty("Zero Point", "Command", [], pol, ship_class="triage"), "command_medical")
        self.assertEqual(fit_net.resolve_specialty("Golden Chariot", "Command", [], pol, ship_class="anvil"), "command_logi_rep")
        self.assertEqual(fit_net.resolve_specialty("Hades", "Command", [], pol, ship_class="gestalt"), "command_carrier_screen")
        # 4. Verify slot classification of all support/tactical/medical/jammer/flak modules
        self.assertEqual(fit_net._module_slot_type("fleet_hospital"), "utility")
        self.assertEqual(fit_net._module_slot_type("ecm_jammer"), "utility")
        self.assertEqual(fit_net._module_slot_type("remote_armor_repairer_ii"), "utility")
        self.assertEqual(fit_net._module_slot_type("target_painter_ii"), "utility")
        self.assertEqual(fit_net._module_slot_type("combat_drone_bay"), "utility")
        self.assertEqual(fit_net._module_slot_type("sensor_dampener"), "utility")
        self.assertEqual(fit_net._module_slot_type("cloaking_device_i"), "utility")
        self.assertEqual(fit_net._module_slot_type("em_disruptor_i"), "weapon")
        self.assertEqual(fit_net._module_slot_type("emp_missile_launcher"), "weapon")
        self.assertEqual(fit_net._module_slot_type("flak_cannon_ii"), "weapon")
        self.assertEqual(fit_net._module_slot_type("shield_recharger_ii"), "defense")
        self.assertEqual(fit_net._module_slot_type("regenerative_armor_ii"), "defense")

    def test_auto_enqueue_schema_duplicates_bursar_reserve_and_royal_guard(self):
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
                INSERT INTO hulls VALUES
                    ('t0_hull', 'Starter', 0),
                    ('broadaxe', 'Broadaxe', 2),
                    ('dualism', 'Dualism', 2),
                    ('prayer', 'Prayer', 1);
                INSERT INTO ships VALUES
                    ('drone-1', 'Military', 'crimson', 't0_hull'),
                    ('sentinel-1', 'Military', 'voidborn', 't0_hull'),
                    ('trader-1', 'Trade', 'voidborn', 't0_hull'),
                    ('trader-2', 'Trade', 'voidborn', 't0_hull'),
                    ('trader-3', 'Trade', 'voidborn', 't0_hull');
                INSERT INTO ship_skills VALUES
                    ('drone-1', 'piloting', 12),
                    ('sentinel-1', 'piloting', 11),
                    ('trader-1', 'piloting', 5),
                    ('trader-2', 'piloting', 5),
                    ('trader-3', 'piloting', 5);
                INSERT INTO ship_listings VALUES
                    ('broadaxe', 'crimson_hub', 95000, 1795500000),
                    ('dualism', 'crimson_hub', 66920, 1795500000),
                    ('prayer', 'crimson_hub', 30000, 1795500000);
            """)
            con.commit()
            con.close()
            # trader-1 is a Bursar desk (excluded), trader-3 is already state="building" (must NOT duplicate!)
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({"crimson_hub": {"pilot": "trader-1"}}), encoding="ascii")
            (data / "fleet" / "upgrade_queue.json").write_text(json.dumps([
                {"id": "u-1", "pilot": "trader-3", "division": "Trade", "hull": "apophenia",
                 "station": "s1:p1:crimson_hub", "max_price": 200000, "state": "building", "created_at": 1795400000}
            ]), encoding="ascii")
            pol = json.loads((ROOT / "game" / "upgrade-policy.json").read_text(encoding="ascii"))
            # Lower Trade min_t0_bursar_reserve to 1 for this 3-trader unit fixture so trader-2 is eligible, then test reserve=2 blocks it
            pol["divisions"]["Trade"]["min_t0_bursar_reserve"] = 1
            (repo / "game" / "upgrade-policy.json").write_text(json.dumps(pol), encoding="ascii")

            res = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500100)
            pilots_added = {a["pilot"]: a["hull"] for a in res["added"]}
            self.assertEqual(pilots_added.get("drone-1"), "broadaxe")
            self.assertEqual(pilots_added.get("sentinel-1"), "dualism")
            self.assertEqual(pilots_added.get("trader-2"), "prayer")
            self.assertNotIn("trader-1", pilots_added)
            self.assertNotIn("trader-3", pilots_added)

            # Verify exact serve_upgrades() schema on disk: state="queued", 3-part station, no "status" key
            q_disk = json.loads((data / "fleet" / "upgrade_queue.json").read_text(encoding="ascii"))
            auto_rows = [r for r in q_disk if r.get("source") == "auto_policy"]
            self.assertEqual(len(auto_rows), 3)
            for r in auto_rows:
                self.assertEqual(r.get("state"), "queued")
                self.assertNotIn("status", r)
                self.assertEqual(r.get("station"), "s1:p1:crimson_hub")
                self.assertIn("batch_id", r)

            # Verify max_auto_tier=3 refuses T4 hulls even when affordable & listed
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.execute("INSERT INTO hulls VALUES ('panacea', 'Panacea', 4)")
            con.execute("INSERT INTO ships VALUES ('Zero Point', 'Command', 'voidborn', 't0_hull')")
            con.execute("INSERT INTO ship_skills VALUES ('Zero Point', 'piloting', 35)")
            con.execute("INSERT INTO ship_listings VALUES ('panacea', 'crimson_hub', 400000, 1795500000)")
            con.commit()
            con.close()
            pol_t4 = json.loads((repo / "game" / "upgrade-policy.json").read_text(encoding="ascii"))
            pol_t4["divisions"]["Command"] = {
                "enabled": True, "max_active": 2,
                "cohorts": [{"empire": "any", "specialty": "t4_test", "share": 1.0,
                             "ladder": [{"hull": "panacea", "tier": 4, "min_piloting": 30, "max_price": 500000}]}]
            }
            (repo / "game" / "upgrade-policy.json").write_text(json.dumps(pol_t4), encoding="ascii")
            res_t4 = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500120)
            self.assertNotIn("Zero Point", {a["pilot"] for a in res_t4["added"]})

            # Verify min_t0_bursar_reserve blocks Trade T0 upgrades when reserve reached
            (data / "fleet" / "upgrade_queue.json").write_text("[]", encoding="ascii")
            pol["divisions"]["Trade"]["min_t0_bursar_reserve"] = 3
            (repo / "game" / "upgrade-policy.json").write_text(json.dumps(pol), encoding="ascii")
            res_res = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500150)
            self.assertNotIn("trader-2", {a["pilot"] for a in res_res["added"]})

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
