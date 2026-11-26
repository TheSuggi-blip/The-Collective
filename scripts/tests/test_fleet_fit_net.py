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

            pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii")); pol["enabled"] = True; pol.pop("enabled_divisions", None)
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
            pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii")); pol["enabled"] = True; pol.pop("enabled_divisions", None)
            # The caps are judged against a loadout of this test's own: the live Intel loadouts buy nothing
            # since 2026-11-25 (orders ENT-093 P1: no module without a measured payback within a week).
            cap_loadout = {"defense": ["shield_booster_iv"], "utility": ["survey_scanner_ii"]}
            pol["specialties"]["Intel"]["loadouts"] = {"covert_recon": dict(cap_loadout), "sensor_survey": dict(cap_loadout)}
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

    def test_live_intel_policy_auto_fits_scout_without_afterburners(self):
        # Suggi mandate (2026-11-25): all non-bursar fleet divisions always auto-upgrade modules (scanners, cloaks, shields, fuel_optimizer),
        # while fuel-guzzling afterburners remain off-role for Intel scouts.
        pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii")); pol["enabled"] = True; pol.pop("enabled_divisions", None)
        sold = ("shield_booster_iv", "shield_booster_ii", "cloaking_device_i", "survey_scanner_ii", "fuel_optimizer", "afterburner_ii")
        world = {"hulls": {"threshold": {"tier": 0, "weapon": 1, "defense": 2, "utility": 2}},
                 "adj": {"s1": []}, "stations": {"b1": ("s1", "p1", "b1", True)},
                 "asks": {m: [(1000, "b1", 50)] for m in sold}}
        ship = {"name": "scout-9", "division": "Intel", "system": "s1", "class": "Threshold", "credits": 90000,
                "modules": [{"type": "afterburner_ii", "slot": "utility"}]}
        plan = fit_net.plan_ship_fit(ship, world, pol)
        self.assertIsNotNone(plan)
        self.assertIn("afterburner_ii", plan["unfit"])
        bought = [m for m, _p in plan["buy_fit"]]
        self.assertTrue(any(m in bought for m in ("shield_booster_iv", "shield_booster_ii")))
        self.assertFalse(any("afterburner" in m for m in bought))

    def test_live_logistics_and_military_policies_auto_fit_all_slots(self):
        # Suggi mandate (2026-11-25): Logistics haulers and Military drones/sentinels auto-fit full utility, weapon & defense ladders.
        pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii")); pol["enabled"] = True; pol.pop("enabled_divisions", None)
        sold = ("shield_booster_iv", "shield_booster_ii", "cargo_expander_iii", "cargo_expander_ii", "fuel_optimizer",
                "economy_passenger_cabin", "pulse_laser_iii", "tracking_computer_iii", "expanded_fuel_tank")
        slots = {"tier": 2, "weapon": 2, "defense": 2, "utility": 2}
        world = {"hulls": {"prayer": dict(slots), "brawler_hull": dict(slots)},
                 "adj": {"s1": []}, "stations": {"b1": ("s1", "p1", "b1", True)},
                 "asks": {m: [(1000, "b1", 50)] for m in sold}}
        hauler = {"name": "hauler-9", "division": "Logistics", "system": "s1", "class": "Prayer", "credits": 90000, "modules": []}
        hp = fit_net.plan_ship_fit(hauler, world, pol)
        self.assertIsNotNone(hp)
        hb = [m for m, _p in hp["buy_fit"]]
        self.assertIn("cargo_expander_iii", hb)
        self.assertIn("shield_booster_iv", hb)
        drone = {"name": "drone-9", "division": "Military", "system": "s1", "class": "brawler_hull", "credits": 90000, "modules": []}
        dp = fit_net.plan_ship_fit(drone, world, pol)
        self.assertIsNotNone(dp)
        db = [m for m, _p in dp["buy_fit"]]
        self.assertIn("pulse_laser_iii", db)
        self.assertIn("shield_booster_iv", db)

    def test_royal_guard_command_and_military_support_specialties(self):
        pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii")); pol["enabled"] = True; pol.pop("enabled_divisions", None)
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
                    ('dividend', 'Dividend', 1);
                INSERT INTO ships VALUES
                    ('ROU Kestrel', 'Military', 'crimson', 't0_hull'),
                    ('GSV Hector', 'Military', 'voidborn', 't0_hull'),
                    ('MCV Kashgar', 'Trade', 'nebula', 't0_hull'),
                    ('MCV Lubeck', 'Trade', 'nebula', 't0_hull'),
                    ('MCV Malacca', 'Trade', 'nebula', 't0_hull');
                INSERT INTO ship_skills VALUES
                    ('ROU Kestrel', 'piloting', 12),
                    ('GSV Hector', 'piloting', 11),
                    ('MCV Kashgar', 'piloting', 5),
                    ('MCV Lubeck', 'piloting', 5),
                    ('MCV Malacca', 'piloting', 5);
                INSERT INTO ship_listings VALUES
                    ('broadaxe', 'crimson_hub', 95000, 1795500000),
                    ('dualism', 'crimson_hub', 66920, 1795500000),
                    ('dividend', 'crimson_hub', 15000, 1795500000);
            """)
            con.commit()
            con.close()
            import shutil as _sh
            _sh.copyfile(ROOT / "game" / "fleet-500-manifest.tsv", repo / "game" / "fleet-500-manifest.tsv")
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({"crimson_hub": {"pilot": "MCV Kashgar"}}), encoding="ascii")
            (data / "fleet" / "upgrade_queue.json").write_text(json.dumps([
                {"id": "u-1", "pilot": "MCV Malacca", "division": "Trade", "hull": "apophenia",
                 "station": "s1:p1:crimson_hub", "max_price": 200000, "state": "building", "created_at": 1795400000}
            ]), encoding="ascii")
            pol = json.loads((ROOT / "game" / "upgrade-policy.json").read_text(encoding="ascii"))
            pol["enabled"] = True; pol["max_auto_tier"] = 3; pol["listed_only"] = True
            for dcfg in (pol.get("divisions") or {}).values():
                dcfg["enabled"] = True
                for coh in (dcfg.get("cohorts") or []):
                    coh["enabled"] = True
                    coh["allow_bursar_desks"] = False
            pol["divisions"]["Trade"]["min_t0_bursar_reserve"] = 1
            (repo / "game" / "upgrade-policy.json").write_text(json.dumps(pol), encoding="ascii")

            res = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500100)
            pilots_added = {a["pilot"]: a["hull"] for a in res["added"]}
            self.assertEqual(pilots_added.get("ROU Kestrel"), "broadaxe")
            self.assertEqual(pilots_added.get("GSV Hector"), "dualism")
            self.assertEqual(pilots_added.get("MCV Lubeck"), "dividend")
            self.assertNotIn("MCV Kashgar", pilots_added)
            self.assertNotIn("MCV Malacca", pilots_added)

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
        pol = json.loads((ROOT / "game" / "upgrade-policy.json").read_text(encoding="ascii")); pol["enabled"] = True; [c.update({"enabled": True}) for c in (pol.get("divisions") or {}).values()]
        fpol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii")); fpol["enabled"] = True; fpol.pop("enabled_divisions", None); pol.pop("enabled_divisions", None)

        # 1. Exact 5-wing 130-ship Mining manifest partition (38 Ore Prec / 22 Ore Bulk / 18 Deep-Core / 28 Gas / 24 Ice)
        wmap = upgrades._load_manifest_wings(ROOT)
        mining_ships = [
            {"pilot": p, "division": "Mining", "empire": "nebula" if w.startswith("3D.") else "solarian",
             "class": "theoria", "hull_id": "theoria", "tier": 0, "piloting": 12}
            for p, w in wmap.items() if w.startswith("3")
        ]
        amap = upgrades.assign_cohort_pilots(mining_ships, pol["divisions"]["Mining"]["cohorts"], wing_map=wmap)
        by_spec = {pol["divisions"]["Mining"]["cohorts"][i]["specialty"]: amap[i] for i in amap}
        self.assertEqual(
            (len(by_spec["ore_precision"]), len(by_spec["ore_bulk"]), len(by_spec["deep_core_rad"]), len(by_spec["gas"]), len(by_spec["ice"])),
            (38, 22, 18, 28, 24),
        )
        self.assertTrue(all(s["empire"] == "nebula" for s in by_spec["gas"]))

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
                    ('glacius', 'Glacius', 1),
                    ('hoarfrost', 'Hoarfrost', 2),
                    ('archimedes', 'Archimedes', 1),
                    ('resonance_miner', 'Resonance Miner', 2);
                INSERT INTO ships VALUES
                    ('EUV Glaciation', 'Mining', 'solarian', 'glacius'),
                    ('EUV Obsidian', 'Mining', 'solarian', 'archimedes');
                INSERT INTO ship_skills VALUES ('EUV Glaciation', 'piloting', 15), ('EUV Obsidian', 'piloting', 15);
                INSERT INTO ship_listings VALUES
                    ('hoarfrost', 'hub1', 150000, 1795500000),
                    ('resonance_miner', 'hub1', 140000, 1795500000);
            """)
            con.commit()
            con.close()
            import shutil as _sh
            _sh.copyfile(ROOT / "game" / "fleet-500-manifest.tsv", repo / "game" / "fleet-500-manifest.tsv")
            pol["max_auto_tier"] = 3
            pol["listed_only"] = True
            (repo / "game" / "upgrade-policy.json").write_text(json.dumps(pol), encoding="ascii")
            res = upgrades.auto_enqueue_upgrades(str(data), str(repo), now=1795500100)
            added_map = {a["pilot"]: a["hull"] for a in res["added"]}
            self.assertEqual(added_map.get("EUV Glaciation"), "hoarfrost")
            self.assertEqual(added_map.get("EUV Obsidian"), "resonance_miner")

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
            pol = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii")); pol["enabled"] = True; pol.pop("enabled_divisions", None)
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


    def test_live_smart_income_engine_t1_policy(self):
        """Suggi directive (2026-11-26): Smart Income Engine First T1 upgrades enabled, Defense/Intel/Liners held."""
        live_up = json.loads((ROOT / "game" / "upgrade-policy.json").read_text(encoding="ascii"))
        divs = live_up.get("divisions") or {}
        self.assertTrue(live_up.get("enabled"))
        self.assertEqual(live_up.get("max_auto_tier"), 1)
        self.assertGreaterEqual(int(live_up.get("treasury_floor_cr") or 0), 8000000)
        for dname in ("Mining", "Military", "Logistics", "Trade"):
            self.assertTrue(divs[dname]["enabled"], f"{dname} must be enabled for Smart Income Engine T1")
        self.assertFalse(divs["Intel"]["enabled"], "Intel hulls must stay paused for T2")
        # Defense cohorts (1A/1B/1C) & Passenger Liners (6B) must stay disabled
        for coh in divs["Military"]["cohorts"]:
            if str(coh.get("wing_prefix") or "").startswith("1"):
                self.assertFalse(coh.get("enabled", True))
        for coh in divs["Logistics"]["cohorts"]:
            if str(coh.get("wing_prefix") or "").startswith("6B."):
                self.assertFalse(coh.get("enabled", True))
        # Zero prestige-locked hulls anywhere in policy
        all_hulls = {r["hull"] for d in divs.values() for c in (d.get("cohorts") or []) for r in (c.get("ladder") or [])}
        self.assertFalse(all_hulls & {"ledger", "workhorse"})

        live_fp = json.loads((ROOT / "game" / "fit-policy.json").read_text(encoding="ascii"))
        self.assertTrue(live_fp.get("enabled"))
        self.assertEqual(set(live_fp.get("enabled_divisions") or []), {"Mining", "Military", "Logistics", "Trade", "Intel"})
        world = {
            "adj": {"s1": []},
            "stations": {"b1": ("s1", "p1", "b1", True)},
            "hulls": {
                "theoria": {"tier": 0, "weapon": 1, "defense": 1, "utility": 1, "cpu": 16, "power": 28},
                "archimedes": {"tier": 1, "weapon": 1, "defense": 1, "utility": 4, "cpu": 18, "power": 34},
            },
            "asks": {m: [(2000, "b1", 50)] for m in ("fuel_optimizer", "mining_laser_ii", "modulated_mining_laser", "shield_booster_i", "cargo_expander_ii")},
            "mod_cost": {"fuel_optimizer": (3, 2), "mining_laser_ii": (4, 7), "modulated_mining_laser": (7, 12), "shield_booster_i": (2, 4), "cargo_expander_ii": (2, 2)},
        }
        # T0 EUV Miner waits for T1 hull (no wasted starter fit!); T1 Archimedes fits immediately!
        t0_miner = {"name": "EUV Obsidian", "division": "Mining", "system": "s1", "class": "Theoria", "credits": 40000, "modules": []}
        self.assertIsNone(fit_net.plan_ship_fit(t0_miner, world, live_fp))
        t1_miner = {"name": "EUV Obsidian", "division": "Mining", "system": "s1", "class": "Archimedes", "credits": 40000, "modules": []}
        p_t1 = fit_net.plan_ship_fit(t1_miner, world, live_fp)
        self.assertIsNotNone(p_t1)
        self.assertEqual(p_t1["specialty"], "ore_precision")
        # T0 VSV Intel fits ONLY fuel_optimizer!
        t0_intel = {"name": "VSV Vespera", "division": "Intel", "system": "s1", "class": "Theoria", "credits": 40000, "modules": []}
        p_int = fit_net.plan_ship_fit(t0_intel, world, live_fp)
        self.assertIsNotNone(p_int)
        self.assertEqual([m for m, _ in p_int["buy_fit"]], ["fuel_optimizer"])


if __name__ == "__main__":
    unittest.main()
