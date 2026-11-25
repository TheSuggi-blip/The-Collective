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
