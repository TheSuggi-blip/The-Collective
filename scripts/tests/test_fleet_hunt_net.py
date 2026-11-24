import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import hunt_net


class HuntNetTests(unittest.TestCase):
    def _weps(self):
        return {
            "pulse_laser_i": {"dps": 10.0, "reach": 3, "damage": 10.0},
            "pulse_laser_iii": {"dps": 24.0, "reach": 4, "damage": 24.0},
            "heavy_plasma_iv": {"dps": 60.0, "reach": 4, "damage": 60.0},
        }

    def _world(self):
        return {
            "adj": {"sys_a": {"sys_b", "sys_p"}, "sys_b": {"sys_a"}, "sys_p": {"sys_a"}},
            "systems": {
                "sys_a": {"empire": "voidborn", "stronghold": False},
                "sys_b": {"empire": "", "stronghold": False},
                "sys_p": {"empire": "", "stronghold": False},
            },
            "stations_by_sys": {"sys_a": [("sys_a", "st_a", "base_a")]},
            "herds": [
                {"system": "sys_a", "poi": "poi_soft", "species": "belt_grazer", "name": "Belt-Grazer", "role": "grazer", "count": 6, "t": 1},
                {"system": "sys_a", "poi": "poi_whale", "species": "pilot_whale", "name": "Pilot Whale", "role": "grazer", "count": 5, "t": 1},
                {"system": "sys_b", "poi": "poi_cauldron", "species": "cauldronback", "name": "Cauldronback", "role": "grazer", "count": 4, "t": 1},
                {"system": "sys_a", "poi": "poi_low", "species": "belt_grazer", "name": "Belt-Grazer", "role": "grazer", "count": 2, "t": 1},
            ],
            "pirates": {"sys_p"},
            "pirate_details": {"sys_p:poi_pir": [{"name": "Flinch", "tier": "scout", "hull": 95, "max_hull": 95, "shield": 35, "max_shield": 35}]},
            "ranch_pois": set(),
            "ranch_systems": set(),
            "species_hull": dict(hunt_net.DEFAULT_SPECIES_HULL),
            "needs_items": {"alloy_scale"},
            "species_loot_val": {"belt_grazer": 2500.0, "pilot_whale": 18000.0, "cauldronback": 22000.0},
        }

    def test_percentage_power_auto_scales_from_t0_to_t4(self):
        weps = self._weps()
        t0 = hunt_net.compute_ship_power({"max_hull": 75, "max_shield": 80, "armor": 3, "tier": 0, "modules": [{"type": "pulse_laser_i"}]}, weps)
        t2 = hunt_net.compute_ship_power({"max_hull": 150, "max_shield": 150, "armor": 6, "tier": 2, "modules": [{"type": "pulse_laser_iii"}, {"type": "pulse_laser_iii"}, {"type": "pulse_laser_iii"}]}, weps)
        t4 = hunt_net.compute_ship_power({"max_hull": 450, "max_shield": 450, "armor": 15, "tier": 4, "modules": [{"type": "heavy_plasma_iv"} for _ in range(4)]}, weps)
        self.assertLess(t0["power"], t2["power"])
        self.assertLess(t2["power"], t4["power"])

        soft = hunt_net.compute_target_threat(60, role="grazer")
        whale = hunt_net.compute_target_threat(220, role="grazer")
        elite_pirate = hunt_net.compute_target_threat(240, 120, role="pirate")

        # T0 passes soft grazer, fails pilot whale solo
        self.assertTrue(hunt_net.passes_combat_gate(t0, soft, 1.35)[0])
        self.assertFalse(hunt_net.passes_combat_gate(t0, whale, 1.35)[0])
        # T2 passes pilot whale solo; T4 auto-graduates to elite pirate solo!
        self.assertTrue(hunt_net.passes_combat_gate(t2, whale, 1.35)[0])
        self.assertTrue(hunt_net.passes_combat_gate(t4, elite_pirate, 1.35)[0])

    def test_dynamic_pack_sizing_3_5_8_10(self):
        weps = self._weps()
        pl3 = hunt_net.compute_ship_power({"max_hull": 90, "max_shield": 90, "armor": 4, "tier": 0, "modules": [{"type": "pulse_laser_iii"}, {"type": "shield_booster_ii"}]}, weps)
        t2 = hunt_net.compute_ship_power({"max_hull": 150, "max_shield": 150, "armor": 6, "tier": 2, "modules": [{"type": "pulse_laser_iii"}, {"type": "pulse_laser_iii"}, {"type": "pulse_laser_iii"}]}, weps)
        whale = hunt_net.compute_target_threat(220, role="grazer")
        raider_pir = hunt_net.compute_target_threat(170, 60, role="pirate")
        heavy_pir = hunt_net.compute_target_threat(280, 120, role="pirate")
        boss_pir = hunt_net.compute_target_threat(420, 200, role="pirate")
        self.assertEqual(hunt_net.choose_pack_size(pl3, whale, 1.80, sizes=(3, 5, 8, 10)), 3)
        self.assertIn(hunt_net.choose_pack_size(pl3, raider_pir, 2.20, sizes=(3, 5, 8, 10)), (5, 8))
        self.assertIn(hunt_net.choose_pack_size(pl3, heavy_pir, 2.20, sizes=(3, 5, 8, 10)), (8, 10))
        # Boss pirate exceeds safe 10x T0 ratio, but 5-8x T2 Recursions clear it cleanly!
        self.assertIsNone(hunt_net.choose_pack_size(pl3, boss_pir, 2.20, sizes=(3, 5, 8, 10)))
        self.assertIn(hunt_net.choose_pack_size(t2, boss_pir, 2.20, sizes=(3, 5, 8, 10)), (5, 8))

    def test_pack_forming_joining_launch_and_quota(self):
        weps = self._weps()
        pl3_doc = {"name": "drone-1", "system": "sys_a", "max_hull": 90, "max_shield": 90, "armor": 4, "tier": 0,
                   "modules": [{"type": "pulse_laser_iii"}, {"type": "shield_booster_ii"}]}
        spow = hunt_net.compute_ship_power(pl3_doc, weps)
        w = self._world()
        pol = json.loads(json.dumps(hunt_net.DEFAULT_POLICY))
        targets = hunt_net.score_pack_targets(pl3_doc, spow, w, pol, {}, {})
        self.assertTrue(any(t["mode"] == "pirate" for t in targets))
        self.assertTrue(any(t["species"] == "pilot_whale" for t in targets))
        with tempfile.TemporaryDirectory() as tmp:
            now_t = time.time()
            p1 = hunt_net.pack_try_join_or_create(tmp, "drone-1", "sys_a", spow, targets, w, pol, 40, now_t=now_t)
            self.assertEqual(p1["state"], "forming")
            self.assertEqual(p1["leader"], "drone-1")
            need_sz = p1["desired_size"]
            last = p1
            for i in range(2, need_sz + 1):
                last = hunt_net.pack_try_join_or_create(tmp, "drone-%d" % i, "sys_a", spow, targets, w, pol, 40, now_t=now_t)
            self.assertEqual(last["state"], "launched")
            self.assertEqual(len(last["members"]), need_sz)

    def test_solo_f38_floor_ranch_exclusion_and_cooldown(self):
        weps = self._weps()
        t0_doc = {"name": "drone-9", "system": "sys_a", "max_hull": 75, "max_shield": 80, "armor": 3, "tier": 0, "modules": [{"type": "pulse_laser_i"}]}
        spow = hunt_net.compute_ship_power(t0_doc, weps)
        w = self._world()
        pol = json.loads(json.dumps(hunt_net.DEFAULT_POLICY))
        cands = hunt_net.score_solo_herds(t0_doc, spow, w, pol, {}, {})
        keys = [c["key"] for c in cands]
        # poi_soft open; poi_low (count=2 <= keep_herd) excluded; poi_whale too strong for T0 solo
        self.assertIn("sys_a:poi_soft", keys)
        self.assertNotIn("sys_a:poi_low", keys)
        self.assertNotIn("sys_a:poi_whale", keys)
        # Partner ranch hard-excluded
        w["ranch_pois"].add("sys_a:poi_soft")
        self.assertNotIn("sys_a:poi_soft", [c["key"] for c in hunt_net.score_solo_herds(t0_doc, spow, w, pol, {}, {})])

    def test_escort_demand_only_activates_when_civilians_at_risk(self):
        w = self._world()
        pol = json.loads(json.dumps(hunt_net.DEFAULT_POLICY))
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "fleet" / "ships").mkdir(parents=True)
            (Path(tmp) / "fleet" / "orders").mkdir(parents=True)
            # Safe policed miner -> 0 escort demand (100% Military free to farm!)
            (Path(tmp) / "fleet" / "ships" / "miner-1.json").write_text(json.dumps({"name": "miner-1", "system": "sys_a", "poi": "b1", "docked": ""}))
            (Path(tmp) / "fleet" / "orders" / "miner-1.json").write_text(json.dumps({"pilot": "miner-1", "what": "mine-network mine-network"}))
            self.assertEqual(hunt_net.detect_escort_demands(tmp, w, pol, {}), [])
            # Lawless miner -> escort demand activates automatically!
            (Path(tmp) / "fleet" / "ships" / "miner-2.json").write_text(json.dumps({"name": "miner-2", "system": "sys_b", "poi": "b2", "docked": ""}))
            (Path(tmp) / "fleet" / "orders" / "miner-2.json").write_text(json.dumps({"pilot": "miner-2", "what": "mine_net mine-network"}))
            dems = hunt_net.detect_escort_demands(tmp, w, pol, {})
            self.assertEqual(len(dems), 1)
            self.assertEqual(dems[0]["follow"], "miner-2")



class HuntNetWorldFromStoreTests(unittest.TestCase):
    """load_combat_world reads the store's real schema: stations has no id/poi columns."""

    def _store(self, root):
        import sqlite3
        (root / "store").mkdir(parents=True)
        conn = sqlite3.connect(str(root / "store" / "read.db"))
        c = conn.cursor()
        c.execute("CREATE TABLE lanes (a TEXT, b TEXT, src TEXT NOT NULL)")
        c.executemany("INSERT INTO lanes VALUES (?, ?, 'x')", [("sys_a", "sys_b"), ("sys_a", "sys_p"), ("sys_a", "sys_h")])
        c.execute("CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER)")
        c.executemany("INSERT INTO systems VALUES (?, ?, ?)", [("sys_a", "voidborn", 0), ("sys_b", "", 0), ("sys_p", "", 0), ("sys_h", "", 0)])
        c.execute("CREATE TABLE stations (name TEXT, kind TEXT, system TEXT, tag TEXT, faction TEXT, empire TEXT, "
                  "condition TEXT, services TEXT, wrecked INTEGER, mobile INTEGER, src TEXT NOT NULL)")
        c.execute("INSERT INTO stations VALUES ('Hex Rock', 'station', 'sys_h', 'HEXC', 'Hex', NULL, NULL, NULL, 0, 0, 'x')")
        c.execute("CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, class TEXT, base TEXT, x REAL, y REAL, t INTEGER, src TEXT NOT NULL)")
        c.executemany("INSERT INTO places VALUES (?, ?, ?, ?, NULL, ?, 0, 0, 1, 'x')", [
            ("sys_a", "st_a", "station", "Alpha Station", "base_a"),
            ("sys_h", "st_h", "station", "Hex Rock", "base_h"),
            ("sys_a", "poi_soft", "asteroid_belt", "Belt", None),
        ])
        c.execute("CREATE TABLE herds (system TEXT, poi TEXT, creature TEXT, name TEXT, role TEXT, count INTEGER, t INTEGER, src TEXT NOT NULL)")
        c.executemany("INSERT INTO herds VALUES (?, ?, ?, ?, 'grazer', ?, 1, 'x')", [
            ("sys_a", "poi_soft", "belt_grazer", "Belt-Grazer", 6),
            ("sys_b", "poi_tag", "belt_grazer", "[HEXC] Belt-Grazer", 5),
        ])
        c.execute("CREATE TABLE observations (division TEXT NOT NULL, member TEXT NOT NULL, kind TEXT NOT NULL, subject TEXT NOT NULL, "
                  "t INTEGER NOT NULL, at TEXT NOT NULL, fields TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', digest TEXT NOT NULL)")
        c.execute("INSERT INTO observations VALUES ('intel', 'Oracle', 'pirate', 'sys_p', ?, 'now', '{}', '', 'd1')", (int(time.time()),))
        c.execute("CREATE TABLE bases (base TEXT, name TEXT, system TEXT, poi TEXT, kind TEXT, t INTEGER, src TEXT NOT NULL)")
        c.execute("INSERT INTO places VALUES ('sys_b', 'out_b', 'station', 'CLTV Outpost B', NULL, 'base_out', 0, 0, 1, 'x')")
        c.execute("INSERT INTO bases VALUES ('base_out', 'CLTV Outpost B', 'sys_b', 'out_b', 'outpost', 1, 'x')")
        conn.commit()
        conn.close()

    def test_world_loads_herds_docks_pirates_and_partner_systems(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._store(root)
            world = hunt_net.load_combat_world(root, root, dict(hunt_net.DEFAULT_POLICY))
            self.assertEqual([h["poi"] for h in world["herds"]], ["poi_soft"])
            self.assertIn("sys_b:poi_tag", world["ranch_pois"])
            self.assertEqual(world["stations_by_sys"].get("sys_a"), [("sys_a", "st_a", "base_a")])
            self.assertNotIn("sys_h", world["stations_by_sys"])
            self.assertNotIn("sys_b", world["stations_by_sys"])      # an outpost of ours: no storage, its fuel is a supply chain
            self.assertIn("sys_p", world["pirates"])
            self.assertIn("sys_h", world["ranch_systems"])

    def test_a_solo_hunt_is_found_on_the_store_world(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._store(root)
            world = hunt_net.load_combat_world(root, root, dict(hunt_net.DEFAULT_POLICY))
            ship = {"name": "drone-1", "system": "sys_a", "max_hull": 100, "max_shield": 80, "modules": [{"type": "pulse_laser_iii"}]}
            weps = {"pulse_laser_iii": {"dps": 24.0, "reach": 4, "damage": 24.0}}
            spow = hunt_net.compute_ship_power(ship, weps, {})
            cands = hunt_net.score_solo_herds(ship, spow, world, dict(hunt_net.DEFAULT_POLICY), {}, {})
            self.assertEqual([c["key"] for c in cands], ["sys_a:poi_soft"])
            self.assertEqual(cands[0]["sell_at"], "sys_a:st_a:base_a")


class HuntNetRuleF9Tests(unittest.TestCase):
    """Rule F9: a side hunts freely only within both gauges of gauges.py (firepower x 7 >= hull, half its
    toughness >= weight); hunt_net's own power ratio never opens a hunt the gauges refuse."""

    ITEMS = {
        "pulse_laser_i": {"id": "pulse_laser_i", "damage": 10, "cooldown": 1},
        "pulse_laser_iii": {"id": "pulse_laser_iii", "damage": 28, "cooldown": 1},
        "autocannon_ii": {"id": "autocannon_ii", "damage": 18, "cooldown": 1, "ammo_type": "autocannon"},
        "autocannon_rounds": {"id": "autocannon_rounds", "category": "ammo"},
    }

    def _world(self):
        return {
            "adj": {"sys_a": set()}, "systems": {"sys_a": {"empire": "voidborn", "stronghold": False}},
            "stations_by_sys": {"sys_a": [("sys_a", "st_a", "base_a")]},
            "herds": [{"system": "sys_a", "poi": "poi_whale", "species": "pilot_whale", "name": "Pilot Whale",
                       "role": "grazer", "count": 6, "t": 1}],
            "pirates": set(), "pirate_details": {}, "ranch_pois": set(), "ranch_systems": set(),
            "species_hull": {"pilot_whale": 220}, "needs_items": set(), "species_loot_val": {"pilot_whale": 18000.0},
        }

    def _ship(self, mods, cargo=None):
        return {"name": "drone-1", "system": "sys_a", "max_hull": 75, "max_shield": 155,
                "modules": [{"kind": "weapon", "slot": "weapon", "type": m} for m in mods], "cargo": cargo or []}

    def test_a_laser_iii_ship_never_solos_a_whale_but_three_make_a_pack(self):
        ship = self._ship(["pulse_laser_iii"])
        weps = {"pulse_laser_iii": {"dps": 28.0, "reach": 4, "damage": 28.0}}
        spow = hunt_net.compute_ship_power(dict(ship, max_shield=400), weps, {})
        f9 = hunt_net.f9_gauge(ship, self.ITEMS)
        pol = dict(hunt_net.DEFAULT_POLICY)
        self.assertEqual(hunt_net.score_solo_herds(ship, spow, self._world(), pol, {}, {}, f9=f9), [])
        packs = hunt_net.score_pack_targets(ship, spow, self._world(), pol, {}, {}, f9=f9)
        self.assertEqual([(p["key"], p["desired_size"]) for p in packs], [("pack:sys_a:poi_whale", 3)])

    def test_three_starters_make_no_whale_pack_where_the_gauges_refuse(self):
        ship = self._ship(["pulse_laser_i"])
        ship["max_hull"], ship["max_shield"] = 60, 40
        f9 = hunt_net.f9_gauge(ship, self.ITEMS)
        self.assertFalse(hunt_net.f9_passes(f9, 220, "grazer", n=3))

    def test_a_gun_without_rounds_adds_no_firepower(self):
        dry = hunt_net.f9_gauge(self._ship(["autocannon_ii"]), self.ITEMS)
        wet = hunt_net.f9_gauge(self._ship(["autocannon_ii"], [{"item": "autocannon_rounds", "quantity": 5}]), self.ITEMS)
        self.assertEqual(dry[0], 0)
        self.assertEqual(wet[0], 18)


    def test_war_wing_dormant_in_peacetime_and_active_on_war_posture(self):
        """War Wing stays 100% dormant in peacetime (F2 RoE) and activates base defense strictly on war posture."""
        import tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            (data / "empire").mkdir(parents=True, exist_ok=True)
            (data / "fleet").mkdir(parents=True, exist_ok=True)
            (data / "empire" / "empire.json").write_text(json.dumps({"faction": {"at_war": False, "wars": []}}), encoding="ascii")
            pol = dict(hunt_net.DEFAULT_POLICY, war_wing={"enabled": True, "defenders_per_base": 10, "min_power": 300.0, "max_jumps": 15})
            # 1. Peacetime -> dormant!
            w_on, w_tags = hunt_net.detect_war_posture(str(data), pol)
            self.assertFalse(w_on)
            self.assertEqual(w_tags, set())

            # 2. Active war -> base defense activates for owned stations/outposts!
            (data / "empire" / "empire.json").write_text(json.dumps({"faction": {"at_war": True, "wars": [{"tag": "HOST"}]}}), encoding="ascii")
            w_on2, w_tags2 = hunt_net.detect_war_posture(str(data), pol)
            self.assertTrue(w_on2)
            self.assertIn("HOST", w_tags2)
            world = {
                "adj": {"s1": {"s2"}, "s2": {"s1"}},
                "owned_bases": [{"base": "st_vb", "system": "s2", "poi": "p2", "kind": "station"}],
            }
            job = hunt_net.pick_war_assignment("drone-1", {"system": "s1"}, {"power": 600.0}, world, pol, {}, w_tags2)
            self.assertIsNotNone(job)
            self.assertEqual(job["mode"], "war_defense")
            self.assertEqual(job["system"], "s2")

if __name__ == "__main__":
    unittest.main()
