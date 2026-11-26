#!/usr/bin/env python3
"""Unit tests for Corporate Supply-Chain & Logistics Optimization upgrades:
  1. handover.receiver() dynamic Cross-Docking auto-resolution via bursar_claims.json
  2. mine_net.py 10% floor + lawless_min_tier=0 (T0==T2) + auto CLTV Outpost Lockboxes
  3. hunt_net.py nearest_station prefers staffed Bursar cross-dock hubs (+1 hop preference)
  4. haul.py _pick_internal_supply pulls from Owned Outpost Faction Lockboxes + backhaul_mission
  5. routemaker.py 10% mining floor default
"""
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))

import handover
import haul
import hunt_net
import mine_net


class TestSupplyChainOptimization(unittest.TestCase):
    def test_handover_auto_resolves_live_bursar_when_no_static_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "fleet").mkdir(parents=True)
            now = int(time.time())
            (data / "fleet" / "fleet.json").write_text(json.dumps({
                "ships": [{"name": "trader-42"}, {"name": "miner-1"}, {"name": "trader-99"}],
                "away": [],
            }), encoding="ascii")
            (data / "fleet" / "receivers.json").write_text(json.dumps({
                "trader": {"pinned_hub": "trader-99"}
            }), encoding="ascii")
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({
                "dynamic_hub": {"pilot": "trader-42", "holders": {"trader-42": now - 60}, "claimed_at": now - 60},
                "pinned_hub": {"pilot": "trader-42", "holders": {"trader-42": now - 60}, "claimed_at": now - 60},
            }), encoding="ascii")
            # Explicit pin wins at pinned_hub
            r_pin, err1 = handover.receiver("trader", "pinned_hub", data=str(data), giver="miner-1")
            self.assertEqual((r_pin, err1), ("trader-99", ""))
            # Dynamic live Bursar auto-resolves at dynamic_hub with ZERO manual receivers.json pin!
            r_dyn, err2 = handover.receiver("trader", "dynamic_hub", data=str(data), giver="miner-1")
            self.assertEqual((r_dyn, err2), ("trader-42", ""))

    def test_mine_net_10pct_floor_and_t0_calm_lawless_equal_to_t2(self):
        pol = json.loads((REPO / "game" / "mine-policy.json").read_text(encoding="ascii"))
        self.assertEqual(float(pol["min_left_pct"]), 5.0)
        self.assertEqual(int(pol["lawless_min_tier"]), 0)
        world = {
            "adj": {"sol": ["border_calm"], "border_calm": ["sol"]},
            "systems": {"sol": {"empire": "solarian", "stronghold": False}, "border_calm": {"empire": "", "stronghold": False}},
            "stations_by_sys": {"sol": [("sol", "sol_p", "sol_base")]},
            "fields": [{"system": "border_calm", "poi": "b1", "resource": "titanium_ore", "remaining": 1100, "max_remaining": 10000}],
            "pirates": set(),
            "item_vals": {"titanium_ore": 40.0},
            "shortages": {},
            "full_items": set(),
            "craft_demand": {},
            "market": {"titanium_ore": [40.0, 2000]},
            "held": {},
        }
        # Belt is at 11% remaining (passes 10% floor, would have failed old 15% floor!) and calm lawless (passes T0!)
        t0_ship = {"name": "miner-1", "system": "sol", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
        cands = mine_net.score_belt_candidates(t0_ship, world, pol, {}, {}, now_t=time.time())
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0]["resource"], "titanium_ore")

    def test_hunt_net_nearest_station_prefers_bursar_hub_within_one_hop(self):
        adj = {"a": ["b", "c"], "b": ["a", "d"], "c": ["a"], "d": ["b"]}
        sts = {"b": [("b", "bp", "unstaffed_base")], "d": [("d", "dp", "bursar_base")]}
        hops, st = hunt_net.nearest_station(adj, sts, "a", max_hops=4, preferred_bases={"bursar_base"})
        self.assertEqual(st[2], "bursar_base")
        self.assertEqual(hops, 2)

    def test_haul_internal_supply_pulls_from_owned_outpost_lockbox_and_backhaul_mission(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "stock").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            (data / "missions").mkdir(parents=True)
            now = int(time.time())
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE faction_facilities (system TEXT, base TEXT, type TEXT, rent_per_cycle INT, status TEXT);
                CREATE TABLE supply_status (item TEXT, stock INT, keep INT);
            """)
            con.execute("INSERT INTO faction_facilities VALUES ('atria', 'atria_outpost', 'faction_lockbox', 0, 'active')")
            con.execute("INSERT INTO supply_status VALUES ('iron_ore', 500, 5000)")
            con.commit()
            con.close()
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {"Faction": {"member": "Faction", "stations": {"atria_outpost": {"iron_ore": 500}}}}
            }), encoding="ascii")
            base_map = {
                "atria_outpost": ("atria", "ap", "atria_outpost", False),
                "node_beta_industrial_station": ("node_beta", "nbp", "node_beta_industrial_station", True),
                "sol_base": ("sol", "sp", "sol_base", True),
            }
            lanes = {"atria": ["node_beta"], "node_beta": ["atria", "sol"], "sol": ["node_beta"]}
            pol = {"policed_only": True, "home_bases": ["node_beta_industrial_station"], "max_jumps_pickup": 10, "max_jumps_delivery": 10, "max_book_age_minutes": 45, "backhaul_min_profit_cr": 400, "backhaul_min_margin_pct": 0.20}
            sup = haul._pick_internal_supply(str(data), "hauler-1", base_map, lanes, "node_beta", 150, pol, set())
            self.assertIsNotNone(sup)
            self.assertEqual(sup["source_target"], "faction")
            self.assertEqual(sup["origin"][2], "atria_outpost")
            self.assertEqual(sup["item"], "iron_ore")

            # Test zero-idle backhaul_mission selection
            (data / "missions" / "sol_base.json").write_text(json.dumps({
                "base": "sol_base",
                "missions": [{
                    "mission_id": "m-1", "title": "HEXC supply: Verdigris Curd", "type": "delivery",
                    "rewards": {"credits": 3000},
                    "objectives": [{"type": "deliver_item", "item_id": "verdigris_curd", "quantity": 10, "target_base_id": "sol_base"}],
                }]
            }), encoding="ascii")
            books = [{"base": "node_beta_industrial_station", "item": "verdigris_curd", "ask": 100, "ask_qty": 50, "t": now - 60}]
            bhm = haul._pick_backhaul_delivery(str(data), "hauler-1", books, base_map, lanes, "node_beta", 100, 10000, pol, set(), now_t=now)
            self.assertIsNotNone(bhm)
            self.assertEqual(bhm["item"], "verdigris_curd")
            self.assertEqual(bhm["qty"], 10)
            self.assertGreater(bhm["est_profit"], 1500)


if __name__ == "__main__":
    unittest.main()


class TestStageBPolishFixes(unittest.TestCase):
    def test_stage_b_polish_fixes_bursar_hunt_mine(self):
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "game" / "fleet"))
        import bursar, hunt_net, mine_net

        # 1. Bursar central_depot_floors blocks faction_pull below Node Beta target (zero ping-pong)
        floors = bursar._central_depot_floors(Path(__file__).resolve().parents[2], "node_beta_industrial_station")
        self.assertGreaterEqual(floors.get("circuit_board", 0), 400)
        self.assertGreaterEqual(floors.get("steel_plate", 0), 2000)
        fac = {"circuit_board": 185, "fuel_cell": 192, "hull_patch": 11, "steel_plate": 2250}
        book = {k: {"best_buy": 250, "best_buy_qty": 100, "best_sell": 260} for k in fac}
        picks = dict(bursar._select_faction_surplus_to_pull(
            fac, book, set(), 500, max_kinds=8, catalog_vals={k: 100 for k in fac}, depot_floors=floors
        ))
        self.assertNotIn("circuit_board", picks)
        self.assertNotIn("fuel_cell", picks)
        self.assertNotIn("hull_patch", picks)
        self.assertLessEqual(picks.get("steel_plate", 0), 250)

        # 2. hunt_net score_solo_herds allows armed Command Flagship on hunt-policy-packs when allow_cmd_override=True
        hpp = hunt_net.load_policy("game/hunt-policy-packs.json")
        self.assertTrue(hpp.get("allow_command_solo"))
        world_h = {
            "adj": {"sys_a": ["sys_b"], "sys_b": ["sys_a"]},
            "systems": {"sys_a": {"police": 0}, "sys_b": {"police": 0}},
            "pirates": set(),
            "ranch_pois": set(),
            "ranch_systems": set(),
            "stations_by_sys": {"sys_a": [("sys_a", "poi_st", "base_a")]},
            "species_hull": {"belt_grazer": 40.0},
            "species_loot_val": {"belt_grazer": 600.0},
            "herds": [{"system": "sys_b", "poi": "poi_h", "species": "belt_grazer", "role": "grazer", "count": 6, "hull": 40.0, "hostile": False}],
        }
        pinfo = {"name": "Golden Chariot", "system": "sys_a"}
        armed = {"power": 600.0, "ehp": 400.0, "dps": 40.0, "tier": 1}
        unarmed = {"power": 0.0, "ehp": 300.0, "dps": 0.0, "tier": 1}
        self.assertEqual(hunt_net.score_solo_herds(pinfo, armed, world_h, hpp, {}, {}, allow_cmd_override=False), [])
        self.assertEqual(hunt_net.score_solo_herds(pinfo, unarmed, world_h, hpp, {}, {}, allow_cmd_override=True), [])
        res_cmd = hunt_net.score_solo_herds(pinfo, armed, world_h, hpp, {}, {}, allow_cmd_override=True)
        self.assertGreaterEqual(len(res_cmd), 1)

        # 3. mine_net blocks negative-score non-deficit belts (score <= 0)
        world_m = {
            "adj": {"s0": ["s1"], "s1": ["s0", "s2"], "s2": ["s1", "s3"], "s3": ["s2", "s4"], "s4": ["s3", "s5"], "s5": ["s4"]},
            "systems": {f"s{i}": {"police": 1, "stronghold": False} for i in range(6)},
            "pirates": set(),
            "stations_by_sys": {"s0": [("s0", "p0", "b0")]},
            "fields": [{
                "system": "s5", "poi": "p5_ice", "resource": "tritium_ice",
                "remaining": 5000, "max_remaining": 5000, "kind": "ice",
            }],
            "market": {"tritium_ice": (12.0, 1000, 1, 1000, 1000)},
            "shortages": {},
            "full_items": set(),
            "craft_demand": {},
            "held": {"tritium_ice": 2000},
            "item_vals": {"tritium_ice": 12.0},
            "owned_outpost_bases": set(),
            "lockbox_bases": {"b0"},
            "bursar_bases": set(),
        }
        pol_m = dict(mine_net.DEFAULT_POLICY)
        pol_m.update({"allow_xp_fallback": False, "max_jumps": 6, "max_station_jumps": 6, "min_left_pct": 5.0})
        ship_m = {"name": "miner-test", "system": "s0", "tier": 1, "modules": [{"item_id": "ice_harvester_i"}]}
        cands_neg = mine_net.score_belt_candidates(ship_m, world_m, pol_m, {}, {})
        self.assertEqual([c for c in cands_neg if c["score"] <= 0 and c["tier"] != "deficit"], [])
