"""Regression tests for open-ended DEA/HWM KPIs, Core Margin, co-op PvE +EV, 3A/3C mining shield, and Ridgecrest fuel gate."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

FLEET_DIR = Path(__file__).resolve().parents[2] / "game" / "fleet"
if str(FLEET_DIR) not in sys.path:
    sys.path.insert(0, str(FLEET_DIR))

import kpi_engine
import mine_net
import hunt_net
import haul


class TestDynamicKPIAndGameTheory(unittest.TestCase):
    def test_open_ended_super_efficiency_and_ranks(self):
        # Below warn -> ALARM (<60)
        s_low, br_low = kpi_engine._score_open_ended(10000, 100000, warn_ratio=0.45)
        self.assertLess(s_low, 60.0)
        self.assertEqual(kpi_engine._status_from_score(s_low), "ALARM")
        self.assertFalse(br_low)

        # At 85% of par -> SOLID (80-99)
        s_sol, _ = kpi_engine._score_open_ended(85000, 100000, warn_ratio=0.45)
        self.assertGreaterEqual(s_sol, 80.0)
        self.assertLess(s_sol, 100.0)
        self.assertEqual(kpi_engine._status_from_score(s_sol), "SOLID")

        # At 1.3x par -> OUTPERFORM (100-119)
        s_out, _ = kpi_engine._score_open_ended(130000, 100000, warn_ratio=0.45)
        self.assertGreaterEqual(s_out, 100.0)
        self.assertLess(s_out, 120.0)
        self.assertEqual(kpi_engine._status_from_score(s_out), "OUTPERFORM")

        # At 2.5x par + beating HWM -> APEX (120+) with breakout bonus
        s_apex, br_apex = kpi_engine._score_open_ended(250000, 100000, warn_ratio=0.45, hwm=200000)
        self.assertGreaterEqual(s_apex, 120.0)
        self.assertTrue(br_apex)
        self.assertEqual(kpi_engine._status_from_score(s_apex), "APEX")
        # Higher output strictly yields higher score (no 100% ceiling)
        s_higher, _ = kpi_engine._score_open_ended(400000, 100000, warn_ratio=0.45, hwm=200000)
        self.assertGreater(s_higher, s_apex)

    def test_open_ended_low_freshness_and_hwm_ratchet(self):
        s_fast, br = kpi_engine._score_open_ended_low(6.0, 18.0, 42.0, hwm_low=10.0)
        self.assertGreaterEqual(s_fast, 120.0)
        self.assertTrue(br)
        # EWMA ratchet moves upward smoothly without spiking 100% on a single burst
        r1 = kpi_engine._ratchet_hwm_high(100.0, 200.0)
        self.assertEqual(r1, 130.0)
        self.assertEqual(kpi_engine._ratchet_hwm_high(130.0, 90.0), 130.0)

    def test_core_operating_margin_tiers(self):
        self.assertEqual(kpi_engine._core_margin_tier(74.2), "ELITE")
        self.assertEqual(kpi_engine._core_margin_tier(50.0), "TARGET")
        self.assertEqual(kpi_engine._core_margin_tier(32.5), "BELOW")
        self.assertEqual(kpi_engine._core_margin_tier(-8.0), "NEG")
        self.assertEqual(kpi_engine._core_margin_tier(None), "WARMUP")

    def test_hunt_coop_pve_vs_opposing_pvp(self):
        # Extract pure function from hunt.py without running top-level CLI side effects
        hunt_src = (FLEET_DIR / "hunt.py").read_text(encoding="ascii")
        i0 = hunt_src.index("def opposing_ship_in_battle(")
        i1 = hunt_src.index("\ndef fight():", i0)
        ns = {}
        exec(hunt_src[i0:i1], ns)
        fn = ns["opposing_ship_in_battle"]

        # Same-side co-op non-CLTV player fighting creature -> STAY (+EV, returns False)
        coop_cells = [
            ["Hollow Pilgrim", "creature", "1", "fire", "1", "2", "10%", "0%", "0", "HexCraft1"],
            ["ROU Broadsword", "player", "2", "fire", "1", "2", "100%", "95%", "0", "Hollow Pilgrim"],
            ["HexCraft1", "player", "2", "fire", "1", "2", "100%", "100%", "0", "Hollow Pilgrim"],
        ]
        self.assertFalse(fn(coop_cells, "ROU Broadsword", {"ROU Broadsword"}))

        # Opposing-side non-CLTV PvP attacker -> FLEE (returns True)
        pvp_cells = [
            ["Hollow Pilgrim", "creature", "1", "fire", "1", "2", "10%", "0%", "0", "ROU Broadsword"],
            ["ROU Broadsword", "player", "2", "fire", "1", "2", "100%", "95%", "0", "Hollow Pilgrim"],
            ["Ganker99", "player", "1", "fire", "1", "2", "100%", "100%", "0", "ROU Broadsword"],
        ]
        self.assertTrue(fn(pvp_cells, "ROU Broadsword", {"ROU Broadsword"}))

        # Pirate NPC joining -> FLEE (returns True)
        pirate_cells = [
            ["ROU Broadsword", "player", "2", "fire", "1", "2", "100%", "95%", "0", "Hollow Pilgrim"],
            ["Void Raider", "pirate", "1", "fire", "1", "2", "100%", "100%", "0", "ROU Broadsword"],
        ]
        self.assertTrue(fn(pirate_cells, "ROU Broadsword", {"ROU Broadsword"}))

    def test_nearest_station_excludes_unseated_outpost_and_no_refuel(self):
        adj = {"atria": {"safe_sys"}, "safe_sys": {"atria"}}
        sts = {
            "atria": [("atria", "poi_op", "base_outpost_atria")],
            "safe_sys": [("safe_sys", "poi_npc", "base_npc_safe")],
        }
        # Seated member uses Atria outpost (0 hops)
        h0, st0 = hunt_net.nearest_station(adj, sts, "atria", max_hops=4, exclude_bases=set())
        self.assertEqual((h0, st0[2]), (0, "base_outpost_atria"))
        # Unseated member excludes outpost -> routes to public NPC station (1 hop)
        h1, st1 = hunt_net.nearest_station(adj, sts, "atria", max_hops=4, exclude_bases={"base_outpost_atria"})
        self.assertEqual((h1, st1[2]), (1, "base_npc_safe"))
        # Same guard in mine_net.nearest_station
        mh1, mst1 = mine_net.nearest_station(adj, sts, "atria", max_hops=4, exclude_bases={"base_outpost_atria"})
        self.assertEqual((mh1, mst1[2]), (1, "base_npc_safe"))

    def test_ridgecrest_no_refuel_dock_pauses_luxury_and_surges_fuel(self):
        import sqlite3
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "empire").mkdir(parents=True)
            (d / "stock").mkdir(parents=True)
            (d / "store").mkdir(parents=True)
            con = sqlite3.connect(str(d / "store" / "read.db"))
            con.execute("CREATE TABLE bases (base TEXT, name TEXT, system TEXT, poi TEXT, kind TEXT)")
            con.execute("INSERT INTO bases VALUES ('st_rc', 'Ridgecrest', 'ridgecrest', 'poi_rc', 'station')")
            con.commit()
            con.close()
            # Owned station WITHOUT refueling_dock
            (d / "empire" / "empire.json").write_text(json.dumps({
                "bases": [{"base": "st_rc", "name": "Ridgecrest", "system": "ridgecrest", "poi": "poi_rc", "kind": "station"}],
                "facilities": [{"base": "st_rc", "type": "grand_hotel_resort", "status": "active"}],
                "faction_storage": [{"base": "st_rc", "item": "steel_plate", "units": 900}],
                "members": [{"username": "Hauler1", "role": "officer"}],
            }), encoding="ascii")
            (d / "stock" / "storage.json").write_text(json.dumps({"pilots": {}, "faction": {}}), encoding="ascii")
            policy = {
                "policed_only": True, "max_jumps_pickup": 10, "max_jumps_delivery": 10,
                "max_buy_spend_cr": 25000, "fuel_reserve_cr": 1000, "hub_upkeep_reorder_pct": 0.7,
                "hub_upkeep_targets": {"station": {"fuel_cell": 2400, "rimeblue_board": 12}},
                "hub_upkeep_max_unit_price": {"fuel_cell": 130, "rimeblue_board": 550},
                "hub_bunker_fuel_targets": {"station": 50000},
            }
            base_map = {
                "st_rc": ("ridgecrest", "poi_rc", "st_rc", "neutral"),
                "st_npc": ("sol", "poi_sol", "st_npc", "solarian"),
            }
            lanes = {"ridgecrest": {"sol"}, "sol": {"ridgecrest"}}
            # 1) Without refueling_dock: luxury food is PAUSED (None) while fuel_cell surges immediately!
            lux_books = [{"base": "st_npc", "item": "rimeblue_board", "ask": 200, "ask_qty": 50, "t": 1e12}]
            job_lux = haul._pick_hub_upkeep(str(d), "Hauler1", lux_books, base_map, lanes, "sol", 100, 30000, policy, set(), now_t=1e12)
            self.assertIsNone(job_lux)
            fuel_books = lux_books + [{"base": "st_npc", "item": "fuel_cell", "ask": 95, "ask_qty": 500, "t": 1e12}]
            job_fuel = haul._pick_hub_upkeep(str(d), "Hauler1", fuel_books, base_map, lanes, "sol", 100, 30000, policy, set(), now_t=1e12)
            self.assertIsNotNone(job_fuel)
            self.assertEqual(job_fuel["item"], "fuel_cell")
            # 2) Once refueling_dock is active: luxury hospitality resumes cleanly!
            (d / "empire" / "empire.json").write_text(json.dumps({
                "bases": [{"base": "st_rc", "name": "Ridgecrest", "system": "ridgecrest", "poi": "poi_rc", "kind": "station"}],
                "facilities": [
                    {"base": "st_rc", "type": "grand_hotel_resort", "status": "active"},
                    {"base": "st_rc", "type": "refueling_dock", "status": "active"},
                ],
                "faction_storage": [{"base": "st_rc", "item": "steel_plate", "units": 900}, {"base": "st_rc", "item": "fuel_cell", "units": 2400}, {"base": "st_rc", "item": "fuel", "units": 5000}],
                "members": [{"username": "Hauler1", "role": "officer"}],
            }), encoding="ascii")
            job_lux_after = haul._pick_hub_upkeep(str(d), "Hauler1", lux_books, base_map, lanes, "sol", 100, 30000, policy, set(), now_t=1e12)
            self.assertIsNotNone(job_lux_after)
            self.assertEqual(job_lux_after["item"], "rimeblue_board")


    def test_bursar_tca_blocks_crystal_melt_54cr_dump_against_2009_gal_bid(self):
        import bursar
        book = {"crystal_melt": {"best_buy": 54, "best_buy_qty": 960, "best_sell": 0, "best_sell_qty": 0}}
        stored = {"crystal_melt": 10}
        # Even when lowball junk bids drag oracle fair_price to 54, gal_bid=2009 MUST block market sell_bid dump!
        acts = bursar.plan_bursar_actions(
            book, stored, [], {}, set(), {"crystal_melt": 2009.0}, 40000,
            {"sell": {"enabled": True, "max_orders_per_station": 8, "min_price_ratio": 0.75, "instant_hit_bid_ratio": 0.85}, "buy": {"enabled": False}},
            fair_price_map={"crystal_melt": {"fair_price": 54.0}},
        )
        kinds = [a[0] for a in acts if a[1] == "crystal_melt"]
        self.assertNotIn("sell_bid", kinds)
        self.assertIn("sell_create", kinds)

    def test_haul_thin_book_arb_spend_cap_and_standing_goals_count(self):
        # Verify thin-book (<40 bid_q) arb exposure is capped at arb_thin_max_spend_cr (12,000 cr)
        books = [
            {"base": "b_ask", "item": "lead_shielding", "ask": 2000, "ask_qty": 20, "bid": 0, "bid_qty": 0, "t": 1e12},
            {"base": "b_bid", "item": "lead_shielding", "ask": 0, "ask_qty": 0, "bid": 3000, "bid_qty": 20, "t": 1e12},
        ]
        bmap = {"b_ask": ("s1", "p1", "b_ask", "solarian"), "b_bid": ("s2", "p2", "b_bid", "solarian")}
        lanes = {"s1": {"s2"}, "s2": {"s1"}}
        peers = [{"pilot": "P1", "system": "s1", "hold_cap": 100, "avail_cash": 40000}]
        pol = {
            "policed_only": True, "max_jumps_pickup": 8, "max_jumps_delivery": 8,
            "min_cr_per_jump": 80, "min_total_profit": 400, "max_arb_book_age_minutes": 15,
            "max_buy_spend_cr": 35000, "arb_thin_max_spend_cr": 12000,
            "min_margin_pct": 0.15, "arb_bid_depth_cap": 0.50, "min_arb_bid_qty": 15,
        }
        res = haul.assign_optimal_arbitrage(books, bmap, lanes, peers, pol, set(), now_t=1e12)
        self.assertIn("P1", res)
        # unit_cost = 2100 -> 12,000 // 2100 = 5 units (NOT 10+ units / 32k blowup!)
        self.assertLessEqual(res["P1"]["qty"], 5)

        # Verify all 13 Eternal Standing Goals compute cleanly
        sgs = kpi_engine.compute_standing_goals(None, {"ships": []}, {}, {}, {}, {}, Path("."), Path("/srv/collective/data"))
        self.assertEqual(len(sgs), 13)
        ids = {g["id"] for g in sgs}
        self.assertTrue({"SG-WEALTH", "SG-MILITARY", "SG-TOURISM", "SG-EBIT", "SG-MARGIN", "SG-TCA", "SG-SEATING", "SG-HULLS", "SG-MODULES"} <= ids)



    def test_treasury_capital_sweep_excluded_from_treasury_ops_and_wallet_costs(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("station_fleet_mod", Path("station/fleet.py"))
        sf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sf)
        # Simulate a 1-hour window where Treasury gains +1,758,102 from reserve sweep (Treasury capital)
        # while operating wallets earn +100,000 and spend -40,000 -> treasury_ops_per_hour MUST be ~0, NOT +1.76M!
        t0, t1 = 1000000, 1003600
        one = [[t0 + 600, "__TREASURY__", "Treasury capital: reserve fleet cash sweep (98 pilots)", 1758102]]
        # one_time_until() must NOT treat Treasury capital as wallet reward/purchase
        bk = getattr(sf, "one_time_until")(one, t1)
        self.assertEqual(bk[""], [0, 0])
        # Build minimal 2-sample history for window()
        a = [t0, 1000000, 1, 500000, 0, 0, 0, {"Trade": [1000000, 1, 500000, 0, 0, 0]}, {"t": [2000000, t0], "m": [0, 0, 0, 0, 0], "s": 100000, "ds": {"Trade": 100000}}]
        b = [t1, 1060000, 1, 600000, 0, 0, 0, {"Trade": [1060000, 1, 600000, 0, 0, 0]}, {"t": [3758102, t1], "m": [100, 20000, 0, 0, 100], "s": 140000, "ds": {"Trade": 140000}}]
        res = sf.window([a, b], t1, 3600, one)
        self.assertEqual(res["treasury_capital_per_hour"], 1758102)
        self.assertEqual(res["treasury_capex_per_hour"], 0)
        self.assertEqual(res["treasury_ops_per_hour"], 0)
        self.assertEqual(res["income_per_hour"], 100000)
        self.assertEqual(res["costs_per_hour"], 40000)

    def test_mine_net_excludes_owned_station_without_refueling_dock(self):
        import mine_net
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "empire").mkdir(parents=True)
            (d / "store").mkdir(parents=True)
            (d / "empire" / "empire.json").write_text(json.dumps({
                "bases": [
                    {"base": "st_rc", "name": "Ridgecrest", "system": "ridgecrest", "kind": "station"},
                    {"base": "op_atria", "name": "Atria", "system": "atria", "kind": "outpost"},
                ],
                "facilities": [
                    {"base": "st_rc", "type": "grand_hotel_resort", "status": "active"},
                    {"base": "op_atria", "type": "faction_fuel_bunker", "status": "active"},
                ],
            }), encoding="ascii")
            pol = {"deposit_stations": ["ridgecrest:poi_rc:st_rc", "atria:poi_at:op_atria", "sol:poi_sol:sol_central"]}
            w = mine_net.load_graph_and_world(str(d), ".", pol, now_t=1e12)
            # Ridgecrest (no refuel facility) MUST be excluded; Atria (bunker) & Sol (NPC) kept!
            self.assertNotIn("ridgecrest", w["stations_by_sys"])
            self.assertIn("atria", w["stations_by_sys"])
            self.assertIn("sol", w["stations_by_sys"])
            # Once refueling_dock activates on Ridgecrest, it auto-unlocks!
            (d / "empire" / "empire.json").write_text(json.dumps({
                "bases": [{"base": "st_rc", "name": "Ridgecrest", "system": "ridgecrest", "kind": "station"}],
                "facilities": [{"base": "st_rc", "type": "refueling_dock", "status": "active"}],
            }), encoding="ascii")
            w2 = mine_net.load_graph_and_world(str(d), ".", pol, now_t=1e12)
            self.assertIn("ridgecrest", w2["stations_by_sys"])


if __name__ == "__main__":
    unittest.main()
