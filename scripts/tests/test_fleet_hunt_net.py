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


if __name__ == "__main__":
    unittest.main()
