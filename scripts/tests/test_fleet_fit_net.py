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
            # the defence buy follows the live policy: Mining took its defence loadouts out (0916d551, Zero)
            ice_def = (((pol.get("specialties") or {}).get("Mining") or {}).get("loadouts") or {}).get("ice", {}).get("defense") or []
            if "shield_booster_iv" in ice_def:
                self.assertIn("shield_booster_iv", bought_ids)
            else:
                self.assertNotIn("shield_booster_iv", bought_ids)

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
        self.assertEqual(fit_net.resolve_specialty("Prime Directive", "Military", [], pol), "command_ewar_tac")
        self.assertEqual(fit_net.resolve_specialty("Crimson Aegis", "Military", [], pol), "command_stealth_ewar")
        self.assertEqual(fit_net.resolve_specialty("Solar Mandate", "Military", [], pol), "command_stealth_ewar")
        self.assertEqual(fit_net.resolve_specialty("Zero Point", "Military", [], pol, ship_class="triage"), "command_medical")
        self.assertEqual(fit_net.resolve_specialty("Golden Chariot", "Military", [], pol, ship_class="anvil"), "command_logi_rep")
        self.assertEqual(fit_net.resolve_specialty("Hades", "Military", [], pol, ship_class="gestalt"), "command_carrier_screen")
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
                    ('floor_price', 'Floor Price', 1);
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
                    ('floor_price', 'crimson_hub', 15000, 1795500000);
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
            self.assertEqual(pilots_added.get("trader-2"), "floor_price")
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


    def test_pilot_of_compat_and_cooldown(self):
        import tempfile, time
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            pol = {"enabled": True, "policed_only": True, "max_jumps": 4, "min_wallet_keep_cr": 10000,
                   "strip_off_role": True, "off_role_modules": {"Logistics": ["pulse_laser_i"]},
                   "max_price": {"cargo_expander_ii": 2500},
                   "specialties": {"Logistics": {"mix": [["freight", 100]], "loadouts": {"freight": {"utility": ["cargo_expander_ii"]}}}}}
            pol_p = data / "fit-policy.json"
            pol_p.write_text(json.dumps(pol), encoding="ascii")
            world = {"adj": {"s1": set()}, "stations": {"b1": ("s1", "p1", "b1", True)},
                     "hulls": {"threshold": {"tier": 1, "weapon": 1, "defense": 2, "utility": 2, "cpu": 100, "power": 100}},
                     "asks": {"cargo_expander_ii": [(1500, "b1", 5)]}, "item_slots": {"cargo_expander_ii": "utility"},
                     "bursar_pilots": set(), "mod_cost": {}}
            # Simulate dispatch.pilot_of() minimal dict (role + hull, missing division/class)
            pilot_doc = {"name": "hauler-19", "role": "hauler", "hull": "Threshold", "system": "s1", "credits": 25000, "modules": []}
            plan = fit_net.needs_fit("hauler-19", pilot_doc, data_dir=data, policy_path=pol_p, world_cache=world)
            self.assertIsNotNone(plan)
            self.assertEqual(plan["buy_fit"][0][0], "cargo_expander_ii")
            # Cooldown suppresses immediate retry loops
            fit_net._stamp_fit_cooldown("hauler-19", 600, data_dir=data)
            self.assertIsNone(fit_net.needs_fit("hauler-19", pilot_doc, data_dir=data, policy_path=pol_p, world_cache=world))



    def test_minmax_cohort_partition_t1_to_t3_climb_and_hull_locked_fits(self):
        """Pilots stay locked in their exact specialty split across T1->T2->T3 and never cross-overwrite."""
        pol = json.loads((ROOT / "game" / "upgrade-policy.json").read_text(encoding="ascii"))
        fpol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii"))

        # 1. Exact 65/20/15 Mining partition with empire affinity (Nebula -> Gas, Solarian -> Ore, Voidborn -> Ice)
        mining_ships = (
            [{"pilot": f"miner-n-{i}", "division": "Mining", "empire": "nebula", "class": "prospect", "hull_id": "prospect", "tier": 0, "piloting": 12} for i in range(35)]
            + [{"pilot": f"miner-s-{i}", "division": "Mining", "empire": "solarian", "class": "theoria", "hull_id": "theoria", "tier": 0, "piloting": 12} for i in range(35)]
            + [{"pilot": f"miner-v-{i}", "division": "Mining", "empire": "voidborn", "class": "threshold", "hull_id": "threshold", "tier": 0, "piloting": 12} for i in range(60)]
        )
        amap = upgrades.assign_cohort_pilots(mining_ships, pol["divisions"]["Mining"]["cohorts"])
        by_spec = {pol["divisions"]["Mining"]["cohorts"][i]["specialty"]: amap[i] for i in amap}
        self.assertEqual((len(by_spec["ore_miner"]), len(by_spec["ice_harvester"]), len(by_spec["gas_harvester"])), (85, 26, 19))
        self.assertTrue(all(s["empire"] == "nebula" for s in by_spec["gas_harvester"]))
        self.assertEqual(sum(1 for s in by_spec["ore_miner"] if s["empire"] == "solarian"), 35)

        # 2. T1 -> T2 progression MUST continue even after 100% of a specialty reaches T1 (fixes deficit<=0 stall bug)
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            repo = Path(tmp) / "repo"
            (data / "store").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
            (repo / "game").mkdir(parents=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE faction (treasury INTEGER);
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, base TEXT);
                CREATE TABLE hulls (id TEXT, name TEXT, tier INTEGER);
                CREATE TABLE ships (pilot TEXT, division TEXT, empire TEXT, class TEXT);
                CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INTEGER);
                CREATE TABLE ship_listings (class_id TEXT, base TEXT, price INTEGER, t INTEGER);
                INSERT INTO faction VALUES (12000000);
                INSERT INTO systems VALUES ('s1', 'voidborn', 0);
                INSERT INTO places VALUES ('s1', 'p1', 'hub1');
                INSERT INTO hulls VALUES
                    ('rime', 'Rime', 1),
                    ('cold_storage', 'Cold Storage', 2),
                    ('bonanza', 'Bonanza', 1),
                    ('motherlode', 'Motherlode', 2);
                INSERT INTO ships VALUES
                    ('miner-1', 'Mining', 'voidborn', 'rime'),
                    ('miner-2', 'Mining', 'solarian', 'bonanza');
                INSERT INTO ship_skills VALUES ('miner-1', 'piloting', 15), ('miner-2', 'piloting', 15);
                INSERT INTO ship_listings VALUES
                    ('cold_storage', 'hub1', 150000, 1795500000),
                    ('motherlode', 'hub1', 140000, 1795500000);
            """)
            con.commit()
            con.close()
            (repo / "game" / "upgrade-policy.json").write_text(json.dumps(pol), encoding="ascii")
            res = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500100)
            added_map = {a["pilot"]: a["hull"] for a in res["added"]}
            # miner-1 (already T1 Ice Rime) MUST upgrade to T2 Ice Cold Storage, NEVER Ore Motherlode!
            self.assertEqual(added_map.get("miner-1"), "cold_storage")
            # miner-2 (already T1 Ore Bonanza) MUST upgrade to T2 Ore Motherlode, NEVER Ice Cold Storage!
            self.assertEqual(added_map.get("miner-2"), "motherlode")

        # 3. fit_net detect_by_hull + sentinel_detect_by_hull + off_role_by_specialty
        self.assertEqual(fit_net.resolve_specialty("miner-99", "Mining", [], fpol, ship_class="rime"), "ice")
        self.assertEqual(fit_net.resolve_specialty("miner-99", "Mining", [], fpol, ship_class="accretion"), "gas")
        self.assertEqual(fit_net.resolve_specialty("sentinel-1", "Military", [], fpol, ship_class="triage"), "royal_guard_utility")
        self.assertEqual(fit_net.resolve_specialty("sentinel-1", "Military", [], fpol, ship_class="bad_idea"), "royal_guard_escort")
        self.assertEqual(fit_net.resolve_specialty("scout-1", "Intel", [], fpol, ship_class="absence"), "covert_recon")
        self.assertEqual(fit_net.resolve_specialty("scout-1", "Intel", [], fpol, ship_class="peer_review"), "sensor_survey")
        self.assertEqual(fit_net._module_slot_type("neural_disruptor"), "weapon")
        self.assertEqual(fit_net._module_slot_type("deep_core_survey_scanner"), "utility")
        self.assertEqual(fit_net._module_slot_type("hull_reinforcement_iii"), "defense")



    def test_fit_net_never_strips_last_harvester_and_self_heals_zero_harvester_miner(self):
        """Regression: never strip mining_laser_i without replacement harvester in stock, and self-heal miner-108."""
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            (data / "store").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
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
                INSERT INTO hulls VALUES ('prospect', 'Prospect', 0, 1, 1, 2), ('rime', 'Rime', 1, 0, 2, 3);
                INSERT INTO books VALUES ('b1', 'cargo_expander_ii', 1500, 5), ('b2', 'ice_harvester_ii', 2500, 5);
            """)
            con.commit()
            con.close()
            pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii"))
            world = fit_net.load_fit_world(str(data), pol)
            # 1. Rime (ice specialty) with only mining_laser_i at b1 (no ice harvester at b1, only at b2):
            # MUST go to b2 to swap mining_laser_i -> ice_harvester_ii, NEVER strip mining_laser_i at b1!
            ship_swap = {"name": "miner-108", "division": "Mining", "system": "s1", "class": "rime", "credits": 30000, "modules": ["mining_laser_i"]}
            p1 = fit_net.plan_ship_fit(ship_swap, world, pol)
            self.assertIsNotNone(p1)
            if p1["base"] == "b1":
                self.assertNotIn("mining_laser_i", p1["unfit"])
            else:
                self.assertIn("ice_harvester_ii", [m for m, _ in p1["buy_fit"]])
            # 2. Miner stranded with 0 harvesters & 2 cargo expanders (miner-108) self-heals at b2!
            ship_zero = {"name": "miner-108", "division": "Mining", "system": "s1", "class": "rime", "credits": 30000, "modules": ["cargo_expander_i", "cargo_expander_ii"]}
            world["hulls"]["rime"]["utility"] = 2
            p2 = fit_net.plan_ship_fit(ship_zero, world, pol)
            self.assertIsNotNone(p2)
            self.assertEqual(p2["base"], "b2")
            self.assertIn("cargo_expander_i", p2["unfit"])
            self.assertIn("ice_harvester_ii", [m for m, _ in p2["buy_fit"]])


if __name__ == "__main__":
    unittest.main()
