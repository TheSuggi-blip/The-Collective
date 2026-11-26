#!/usr/bin/env python3
"""Unit tests for open-market anti-manipulation engine (game/fleet/market_guard.py)."""
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import bursar
import haul
import market_guard as mg


class MarketGuardTests(unittest.TestCase):
    def test_vwm_ignores_single_station_spoof_spike_and_cltv_own_orders(self):
        now_t = time.time()
        books = [
            {"base": "sol", "item": "silicon_ore", "bid": 7, "bid_qty": 196000, "t": now_t},
            {"base": "ge", "item": "silicon_ore", "bid": 10, "bid_qty": 8500, "t": now_t},
            {"base": "crimson", "item": "silicon_ore", "bid": 11, "bid_qty": 200, "t": now_t},
            {"base": "exp", "item": "silicon_ore", "bid": 421, "bid_qty": 41, "t": now_t},
            {"base": "crucible", "item": "silicon_ore", "bid": 795, "bid_qty": 200, "t": now_t},
        ]
        # Exclude CLTV's own poisoned order at crucible; VWM MUST stay ~7 cr, NOT 421 or 795 cr!
        vwm = mg.compute_book_vwm_map(books, cltv_buy_keys={("crucible", "silicon_ore")}, now_t=now_t)
        self.assertIn("silicon_ore", vwm)
        self.assertLessEqual(vwm["silicon_ore"]["vwm"], 12.0)

    def test_luld_twap_blocks_flash_pump_but_freely_adapts_to_genuine_multi_hour_shift(self):
        with tempfile.TemporaryDirectory() as td:
            t0 = 1795650000.0
            # Seed oracle at 10 cr across 3 stations
            r0 = mg.update_price_oracle(td, {"silicon_ore": {"vwm": 10.0, "stations": 3, "total_qty": 5000}}, now_t=t0)
            self.assertEqual(r0["silicon_ore"]["fair_price"], 10.0)
            # 5 minutes later, flash pump to 800 cr at 1 station -> LULD MUST clamp hard (< 15 cr)!
            r1 = mg.update_price_oracle(td, {"silicon_ore": {"vwm": 800.0, "stations": 1, "total_qty": 20}}, now_t=t0 + 300)
            self.assertLess(r1["silicon_ore"]["fair_price"], 15.0)
            # Over 12 genuine hours at 50 cr across 4 deep stations -> oracle smoothly tracks upward without static cap!
            cur_t = t0 + 3600
            for _ in range(12):
                r_up = mg.update_price_oracle(td, {"silicon_ore": {"vwm": 50.0, "stations": 4, "total_qty": 5000}}, now_t=cur_t, min_write_interval_s=0)
                cur_t += 3600
            self.assertGreater(r_up["silicon_ore"]["fair_price"], 28.0)

    def test_bait_ask_detector_and_same_station_anti_self_outbid(self):
        # Troll parks 1,000 cr ask on 10 cr ore with 0 local bid -> safe_buy_ceiling caps at ~13 cr, NEVER 765 cr!
        c = mg.safe_buy_ceiling("silicon_ore", local_bid=0, local_ask=1000, fair_val=10.0, max_ratio=0.90)
        self.assertLessEqual(c, 15)
        self.assertGreaterEqual(c, 5)
        # Unanchored item (fair_val=0) with 0 local bid and 1,000 cr ask -> REFUSED (0)!
        self.assertEqual(mg.safe_buy_ceiling("mystery_bait", local_bid=0, local_ask=1000, fair_val=0.0), 0)
        # Same-station anti-self-outbid: trader-79 skips silicon_ore when trader-41 already bids it there!
        book = {"silicon_ore": {"best_buy": 10, "best_buy_qty": 200, "best_sell": 15, "best_sell_qty": 100}}
        pol = json.loads(json.dumps(bursar.DEFAULT_POLICY))
        pol["buy"]["enabled"] = True
        acts = bursar.plan_bursar_actions(
            book, {}, [], {"silicon_ore": 500}, set(), {"silicon_ore": 10.0}, 50000, pol,
            same_station_cltv_buys={"silicon_ore"},
        )
        self.assertFalse(any(a[0] == "buy_create" and a[1] == "silicon_ore" for a in acts))

    def test_mirage_arbitrage_scam_blocked_while_legit_arbitrage_passes(self):
        # EVE Margin-Trading Scam: 10 cr item listed at 500 cr ask + fake 800 cr buy wall -> BLOCKED!
        self.assertTrue(mg.is_mirage_arbitrage_trap("junk_ore", buy_ask=500, sell_bid=800, fair_info={"fair_price": 10.0}))
        # Legitimate regional arbitrage: buy at 14 cr (near 15 cr fair value), sell at 32 cr -> ALLOWED!
        self.assertFalse(mg.is_mirage_arbitrage_trap("hydrogen_gas", buy_ask=14, sell_bid=32, fair_info={"fair_price": 15.0}))
        # Integration check with haul.pick_arbitrage_job
        now_t = time.time()
        base_map = {"a": ("sa", "pa", "a", True), "b": ("sb", "pb", "b", True)}
        lanes = {"sa": ["sb"], "sb": ["sa"]}
        books = [
            {"base": "a", "item": "junk_ore", "ask": 500, "ask_qty": 100, "bid": 10, "bid_qty": 100, "t": now_t},
            {"base": "b", "item": "junk_ore", "ask": 900, "ask_qty": 10, "bid": 800, "bid_qty": 100, "t": now_t},
        ]
        pol = {"policed_only": True, "min_margin_pct": 0.20, "min_total_profit": 500, "min_cr_per_jump": 100, "max_buy_spend_cr": 15000}
        job_scam = haul.pick_arbitrage_job(books, base_map, lanes, "sa", 100, 50000, pol, set(), now_t=now_t, fair_prices={"junk_ore": {"fair_price": 10.0}})
        self.assertIsNone(job_scam)



    def test_sell_side_anti_lowball_blocks_fake_decoy_ask_and_penny_dump(self):
        # Reverse scam: quantum_silk fair value = 2,100 cr; scammer parks 100 cr decoy ask (qty 1) + 80 cr bid!
        floor = mg.safe_sell_floor("quantum_silk", local_bid=80, local_ask=100, fair_val=2100.0)
        self.assertGreaterEqual(floor, 1500)
        fair_map = {"quantum_silk": {"fair_price": 2100.0, "stations": 4}}
        # Bursar MUST NOT dump at 80 cr or undercut 100 cr to 99 cr!
        book = {"quantum_silk": {"best_buy": 80, "best_buy_qty": 500, "best_sell": 100, "best_sell_qty": 1}}
        pol = json.loads(json.dumps(bursar.DEFAULT_POLICY))
        pol["sell"]["instant_hit_bid_ratio"] = 0.60
        acts = bursar.plan_bursar_actions(book, {"quantum_silk": 10}, [], {}, set(), {"quantum_silk": 2100.0}, 50000, pol, fair_price_map=fair_map)
        self.assertFalse(any(a[0] == "sell_bid" for a in acts), acts)
        creates = [a for a in acts if a[0] == "sell_create" and a[1] == "quantum_silk"]
        self.assertEqual(len(creates), 1)
        self.assertGreaterEqual(creates[0][3], 1500)
        # Even with 0 ask + 10 cr bid (and even with 600 units!), Bursar NEVER dumps high-value quantum_silk!
        book2 = {"quantum_silk": {"best_buy": 10, "best_buy_qty": 500, "best_sell": 0, "best_sell_qty": 0}}
        acts2 = bursar.plan_bursar_actions(book2, {"quantum_silk": 600}, [], {}, set(), {"quantum_silk": 2100.0}, 50000, pol, fair_price_map=fair_map)
        self.assertFalse(any(a[0] == "sell_bid" for a in acts2), acts2)
        # Disjoint faction_pull invariant: Bursar does NOT pull quantum_silk from Lockbox if local station only has a lowball 80 cr bid / 100 cr ask!
        picks = bursar._select_faction_surplus_to_pull(
            {"quantum_silk": 20},
            book,
            set(),
            free_hold=80,
            catalog_vals={"quantum_silk": 2100.0},
        )
        self.assertEqual(picks, [])

    def test_non_faction_hunter_lockbox_bridge_routes_via_in_faction_hauler(self):
        import hunt_net
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "empire").mkdir(parents=True)
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [{"name": "drone-1", "role": "Officer"}]
            }), encoding="ascii")
            lbs = {"atria_lockbox", "central_nexus"}
            # In-faction hunter -> direct --deposit faction
            self.assertEqual(hunt_net.hunt_dropoff_args("drone-1", "central_nexus", lbs, data), ["--deposit", "faction"])
            # Outside-faction hunter -> bridged via --gift-to hauler (100% in-faction Officers!)
            self.assertEqual(hunt_net.hunt_dropoff_args("drone-99", "central_nexus", lbs, data), ["--gift-to", "hauler"])
            # Outside-faction hunter at non-lockbox station -> default trader
            self.assertEqual(hunt_net.hunt_dropoff_args("drone-99", "other_station", lbs, data), ["--gift-to", "trader"])



    def test_hybrid_lockbox_routes_safe_hub_to_officer_trader_and_outpost_to_hauler(self):
        import hunt_net
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "empire").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [
                    {"pilot": "drone-1", "role": "Officer"},
                    {"pilot": "trader-4", "role": "Officer"},
                    {"pilot": "trader-8", "role": "Officer"},
                ],
                "facilities": [
                    {"type": "faction_lockbox", "status": "active", "base": "central_nexus"},
                    {"type": "faction_lockbox", "status": "active", "base": "gsc_0044_outpost"},
                ],
            }), encoding="ascii")
            (data / "fleet" / "receivers.json").write_text(json.dumps({
                "trader": {
                    "*": "trader-4",
                    "central_nexus": "trader-8",
                    "node_beta": "trader-72",
                }
            }), encoding="ascii")
            lbs = {"central_nexus", "node_beta", "gsc_0044_outpost"}
            # 1. Safe Lockbox with explicit Officer Trader -> --gift-to trader (<= 2m local sale or lockbox_push!)
            self.assertEqual(hunt_net.hunt_dropoff_args("drone-99", "central_nexus", lbs, data), ["--gift-to", "trader"])
            # 2. Lawless Outpost (only wildcard '*' matches, NO explicit trader docked there) -> --gift-to hauler!
            self.assertEqual(hunt_net.hunt_dropoff_args("drone-99", "gsc_0044_outpost", lbs, data), ["--gift-to", "hauler"])
            # 3. Safe Lockbox whose receiver is still an outside-faction trader -> --gift-to hauler until Officer arrives!
            self.assertEqual(hunt_net.hunt_dropoff_args("drone-99", "node_beta", lbs, data), ["--gift-to", "hauler"])
            # 4. In-faction Hunter at ANY Lockbox -> direct --deposit faction!
            self.assertEqual(hunt_net.hunt_dropoff_args("drone-1", "gsc_0044_outpost", lbs, data), ["--deposit", "faction"])

    def test_bursar_sync_receivers_prefers_officer_and_claim_prioritizes_lockbox(self):
        import sqlite3
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            repo = Path(td) / "repo"
            (data / "empire").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            (repo / "game").mkdir(parents=True)
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [
                    {"pilot": "trader-1", "role": "Officer"},
                    {"pilot": "trader-4", "role": "Officer"},
                ],
                "facilities": [
                    {"type": "faction_lockbox", "status": "active", "base": "central_nexus"},
                    {"type": "faction_lockbox", "status": "active", "base": "the_experiment"},
                ],
            }), encoding="ascii")
            # 1. _sync_bursar_receivers must pick ONLY Officer trader-4 at Lockbox the_experiment (ignoring outside trader-48!)
            now = 1795658000.0
            claims = {
                "the_experiment": {
                    "base": "the_experiment",
                    "pilot": "trader-48",
                    "claimed_at": int(now),
                    "holders": {"trader-48": int(now - 60), "trader-4": int(now)},
                }
            }
            bursar._sync_bursar_receivers(data, claims, now_t=now)
            rec = json.loads((data / "fleet" / "receivers.json").read_text())
            self.assertEqual(rec["trader"]["the_experiment"], "trader-4")
            # 2. Officer trader-1 currently sitting at non-lockbox hub MUST claim central_nexus even though outside trader-72 is already there!
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER, police INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, base TEXT);
                CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER, t REAL);
                INSERT INTO systems VALUES ('sys_a', 'solarian', 0, 1), ('sys_b', 'solarian', 0, 1);
                INSERT INTO places VALUES ('sys_a', 'poi_a', 'station', 'Other', 'other_hub'), ('sys_b', 'poi_b', 'station', 'Central', 'central_nexus');
                INSERT INTO books VALUES ('other_hub', 'iron_ore', 5, 100, 7, 100, 1795658000), ('central_nexus', 'iron_ore', 5, 100, 7, 100, 1795658000);
            """)
            con.commit()
            con.close()
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({
                "central_nexus": {
                    "base": "central_nexus", "system": "sys_b", "poi": "poi_b",
                    "pilot": "trader-72", "claimed_at": int(now), "holders": {"trader-72": int(now)},
                }
            }), encoding="ascii")
            pol = json.loads(json.dumps(bursar.DEFAULT_POLICY))
            pol["max_per_station"] = 1
            pol["exclude_pirates"] = False
            picked = bursar.claim_station(data, repo, "trader-1", {"system": "sys_a", "base": "other_hub", "empire": "solarian"}, pol, now_t=now)
            self.assertIsNotNone(picked)
            self.assertEqual(picked["base"], "central_nexus")



    def test_guarded_bid_price_and_routemaker_best_bids_block_spoof_and_self_buys(self):
        import routemaker
        fair_map = {"lumen_honey_cake": {"fair_price": 2.0, "stations": 4, "total_qty": 10000}}
        # Single-station 78,350 cr spoof MUST be capped near oracle fair value (never 78,350!)
        self.assertLessEqual(mg.guarded_bid_price("lumen_honey_cake", 78350.0, fair_map), 5.0)
        world = {
            "books": {
                "cltv_own_base": {"items": {"silicon_ore": {"bid": 795, "bid_qty": 500}}},
                "spoof_base": {"items": {"silicon_ore": {"bid": 670, "bid_qty": 9}}},
                "real_base": {"items": {"silicon_ore": {"bid": 7, "bid_qty": 50000}}},
            },
            "cltv_buys": {("cltv_own_base", "silicon_ore")},
            "fair_map": {"silicon_ore": {"fair_price": 7.0, "stations": 6, "total_qty": 260000}},
        }
        bids = routemaker.best_bids(world, "silicon_ore")
        # CLTV's own buy order excluded, spoof_base capped from 670 -> 10.5!
        self.assertTrue(all(b[2] != "cltv_own_base" for b in bids), bids)
        self.assertLessEqual(max(b[0] for b in bids), 11.0, bids)



    def test_standing_10_packs_at_3_outposts_and_public_battles_pirate_shield(self):
        import hunt_net, sqlite3
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "fleet").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            ships = (
                [{"name": f"sentinel-{i}"} for i in range(1, 20)]
                + [{"name": f"drone-{i}"} for i in range(1, 40)]
            )
            (data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}), encoding="ascii")
            # Verify all 10 Command Flagships map cleanly to 4x3, 3x5, 3x7 = 48 unique ships across gsc_0044/atria/felis!
            all_members = []
            sizes = []
            outposts = set()
            for sq_id, op_sys, leader, ns, nd in hunt_net.STANDING_SQUAD_SPECS:
                sq = hunt_net.standing_squad_for_pilot(data, leader, {"packs": {"standing_outpost_squads": True}})
                self.assertIsNotNone(sq)
                self.assertEqual(sq["squad_id"], sq_id)
                self.assertEqual(sq["outpost_system"], op_sys)
                self.assertEqual(len(sq["members"]), 1 + ns + nd)
                sizes.append(sq["size"])
                outposts.add(op_sys)
                all_members.extend(sq["members"])
            self.assertEqual(sorted(sizes), [3, 3, 3, 3, 5, 5, 5, 7, 7, 7])
            self.assertEqual(len(all_members), 48)
            self.assertEqual(len(set(all_members)), 48)
            self.assertEqual(outposts, {"gsc_0044", "atria", "felis"})

    def test_craft_net_live_buywall_overproduction_cap_halts_when_stock_reaches_half_depth(self):
        import craft_net
        world = {
            "recipes": {
                "make_rations": {"id": "make_rations", "inputs": [("water_ice", 1)], "outputs": [("solarian_gourmet_rations", 1)], "facility_only": False},
            },
            "books": {"st1": {"solarian_gourmet_rations": {"bid": 270.0, "bid_qty": 100}, "water_ice": {"bid": 5.0, "ask": 5.0, "ask_qty": 500}}},
            "global_bid": {"solarian_gourmet_rations": (270.0, 100)},
            "item_vals": {"solarian_gourmet_rations": 270.0, "water_ice": 5.0},
            "stock_by_item": {"solarian_gourmet_rations": 60, "water_ice": 200},
            "reserve_items": set(),
            "need_crafts": set(),
            "demand": {"commercial_targets": {"solarian_gourmet_rations": {"cap": 400, "division": "Trade"}}},
        }
        pol = {"max_runs_per_cycle": 10, "trade": {"enabled": True, "min_margin_pct": 0.2, "min_profit_cr": 50, "min_bid_qty": 3, "allow_buy_inputs_docked": False}}
        # Live external bid_qty=100 -> 50% cap = 50; fleet already holds 60 -> MUST NOT overproduce!
        job = craft_net.pick_craft_job("Trade", "st1", {"water_ice": 200}, 50000, world, pol)
        self.assertIsNone(job)
        # Drop stock to 10 (< 50) -> crafts cleanly!
        world["stock_by_item"]["solarian_gourmet_rations"] = 10
        job2 = craft_net.pick_craft_job("Trade", "st1", {"water_ice": 200}, 50000, world, pol)
        self.assertIsNotNone(job2)
        self.assertEqual(job2["makes"], "solarian_gourmet_rations")

    def test_outpost_bunker_dynamic_multi_hauler_surge_5_3_2_1(self):
        import haul, sqlite3, time
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "store").mkdir(parents=True)
            (data / "stock").mkdir(parents=True)
            (data / "empire").mkdir(parents=True)
            con = sqlite3.connect(data / "store" / "read.db")
            con.execute("CREATE TABLE bases (base TEXT, system TEXT, poi TEXT, kind TEXT)")
            con.execute("CREATE TABLE places (base TEXT, poi TEXT)")
            con.execute("INSERT INTO bases VALUES ('op1', 'atria', 'poi_atria', 'outpost')")
            con.commit(); con.close()
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {"Faction": {"stations": {
                    "nb": {"fuel_cell": 2000},
                    "op1": {"fuel_cell": 400, "steel_plate": 180, "circuit_board": 45, "hull_patch": 25},
                }}}
            }), encoding="ascii")
            base_map = {
                "nb": ("node_beta", "nb", "nb", "voidborn"),
                "op1": ("atria", "poi_atria", "op1", ""),
            }
            lanes = {"node_beta": ["atria"], "atria": ["node_beta"]}
            pol = haul.load_policy()
            # 1) CRITICAL (0 / 50,000 -> <20%): MUST allow 5 concurrent haulers (slots 0..4), block 6th!
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [{"pilot": f"hauler-{i}", "role": "Officer"} for i in range(1, 8)],
                "facilities": [{"type": "faction_fuel_bunker", "status": "active", "base": "op1"}],
                "faction_storage": [{"base": "op1", "item": "fuel", "units": 0}],
            }), encoding="ascii")
            claimed = set()
            for i in range(1, 6):
                j = haul._pick_hub_upkeep(data, f"hauler-{i}", [], base_map, lanes, "node_beta", 200, 20000, pol, claimed)
                self.assertIsNotNone(j, f"slot {i} must be assigned at 0/50k CRITICAL")
                self.assertTrue(j["bunker_fill"])
                claimed.add(j["job_key"])
            self.assertEqual(len(claimed), 5)
            j6 = haul._pick_hub_upkeep(data, "hauler-6", [], base_map, lanes, "node_beta", 200, 20000, pol, claimed)
            self.assertTrue(j6 is None or not j6.get("bunker_fill"))
            # 2) TOP-OFF (44,000 / 50,000 -> 88%): MUST allow exactly 1 hauler, NOT 2!
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [{"pilot": f"hauler-{i}", "role": "Officer"} for i in range(1, 8)],
                "facilities": [{"type": "faction_fuel_bunker", "status": "active", "base": "op1"}],
                "faction_storage": [{"base": "op1", "item": "fuel", "units": 44000}],
            }), encoding="ascii")
            j_top1 = haul._pick_hub_upkeep(data, "hauler-1", [], base_map, lanes, "node_beta", 200, 20000, pol, set())
            self.assertIsNotNone(j_top1)
            self.assertTrue(j_top1["bunker_fill"])
            j_top2 = haul._pick_hub_upkeep(data, "hauler-2", [], base_map, lanes, "node_beta", 200, 20000, pol, {j_top1["job_key"]})
            self.assertTrue(j_top2 is None or not j_top2.get("bunker_fill"))



    def test_outpost_repair_bill_guard_triggers_before_wreck_shortfall(self):
        import haul, sqlite3
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "store").mkdir(parents=True)
            (data / "stock").mkdir(parents=True)
            (data / "empire").mkdir(parents=True)
            con = sqlite3.connect(data / "store" / "read.db")
            con.execute("CREATE TABLE bases (base TEXT, system TEXT, poi TEXT, kind TEXT)")
            con.execute("CREATE TABLE places (base TEXT, poi TEXT)")
            con.execute("INSERT INTO bases VALUES ('op1', 'atria', 'poi_atria', 'outpost')")
            con.commit(); con.close()
            # Bunker FULL (49,000/50,000), fuel_cell stocked (400/400), but steel_plate=175 (<180) & circuit_board=35 (<45)!
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {"Faction": {"stations": {
                    "nb": {"steel_plate": 1000, "circuit_board": 200},
                    "op1": {"fuel_cell": 400, "steel_plate": 175, "circuit_board": 35, "hull_patch": 35},
                }}}
            }), encoding="ascii")
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [{"pilot": "hauler-1", "role": "Officer"}],
                "facilities": [{"type": "faction_fuel_bunker", "status": "active", "base": "op1"}],
                "faction_storage": [{"base": "op1", "item": "fuel", "units": 49000}],
            }), encoding="ascii")
            base_map = {
                "nb": ("node_beta", "nb", "nb", "voidborn"),
                "op1": ("atria", "poi_atria", "op1", ""),
            }
            lanes = {"node_beta": ["atria"], "atria": ["node_beta"]}
            pol = haul.load_policy()
            j = haul._pick_hub_upkeep(data, "hauler-1", [], base_map, lanes, "node_beta", 200, 20000, pol, set())
            self.assertIsNotNone(j)
            self.assertIn(j["item"], ("steel_plate", "circuit_board"))
            self.assertEqual(j["mode"], "transfer")



    def test_node_beta_central_depot_self_flush_and_restock(self):
        import haul, sqlite3
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "store").mkdir(parents=True)
            (data / "stock").mkdir(parents=True)
            (data / "empire").mkdir(parents=True)
            con = sqlite3.connect(data / "store" / "read.db")
            con.execute("CREATE TABLE bases (base TEXT, system TEXT, poi TEXT, kind TEXT)")
            con.execute("CREATE TABLE places (base TEXT, poi TEXT)")
            con.execute("INSERT INTO bases VALUES ('op1', 'atria', 'poi_atria', 'outpost')")
            con.commit(); con.close()
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {
                    "Faction": {"stations": {
                        "node_beta_industrial_station": {"fuel_cell": 2000, "steel_plate": 2000, "circuit_board": 5, "hull_patch": 150},
                        "op1": {"fuel_cell": 400, "steel_plate": 260, "circuit_board": 70, "hull_patch": 35},
                    }},
                    "hauler-6": {"stations": {
                        "node_beta_industrial_station": {"circuit_board": 3108},
                    }},
                }
            }), encoding="ascii")
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [{"pilot": "hauler-6", "role": "Officer"}],
                "facilities": [{"type": "faction_fuel_bunker", "status": "active", "base": "op1"}],
                "faction_storage": [{"base": "op1", "item": "fuel", "units": 49000}],
            }), encoding="ascii")
            base_map = {
                "node_beta_industrial_station": ("node_beta", "node_beta_industrial_station", "node_beta_industrial_station", "voidborn"),
                "op1": ("atria", "poi_atria", "op1", ""),
            }
            lanes = {"node_beta": ["atria"], "atria": ["node_beta"]}
            pol = haul.load_policy()
            j = haul._pick_hub_upkeep(data, "hauler-6", [], base_map, lanes, "node_beta", 200, 20000, pol, set())
            self.assertIsNotNone(j)
            self.assertEqual(j["hub_kind"], "depot")
            self.assertEqual(j["item"], "circuit_board")
            self.assertEqual(j["source_target"], "self")
            self.assertEqual(j["dest"][2], "node_beta_industrial_station")
            self.assertEqual(j["pickup_hops"], 0)
            self.assertEqual(j["delivery_hops"], 0)



    def test_zero_point_healer_patrol_3pack_always_active_on_tier_s_herds(self):
        import hunt_net
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "fleet").mkdir(parents=True)
            ships = (
                [{"name": f"sentinel-{i}"} for i in range(1, 20)]
                + [{"name": f"drone-{i}"} for i in range(1, 40)]
            )
            (data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}), encoding="ascii")
            (data / "fleet" / "flagships.json").write_text(json.dumps({"Zero Point": {"role": "command"}}), encoding="ascii")
            sq = hunt_net.standing_squad_for_pilot(data, "Zero Point", {"packs": {"standing_outpost_squads": True}})
            self.assertIsNotNone(sq)
            self.assertEqual(sq["squad_id"], "gsc-3b")
            self.assertEqual(sq["size"], 3)
            self.assertEqual(sq["outpost_system"], "gsc_0044")
            world = {
                "adj": {"gsc_0044": {"s1"}, "s1": {"gsc_0044"}},
                "systems": {"gsc_0044": {"empire": "", "stronghold": False}, "s1": {"empire": "", "stronghold": False}},
                "stations_by_sys": {"gsc_0044": [("gsc_0044", "op_poi", "op_base")]},
                "herds": [{"system": "s1", "poi": "p1", "species": "quantum_moth", "role": "grazer", "count": 6}],
                "pirates": set(), "ranch_pois": set(), "ranch_systems": set(),
                "species_hull": {"quantum_moth": 45.0},
                "species_loot_val": {"quantum_moth": 2100.0},
                "bursar_bases": set(), "lockbox_bases": {"op_base"}, "data_dir": str(data),
            }
            pol = hunt_net.deep_merge(hunt_net.load_policy(), {"packs": {
                "sizes": [3], "min_target_hull": 35, "min_loot_val": 750.0,
                "min_loot_per_ship": 250.0, "allow_healer_patrol": True,
            }})
            # Unarmed Zero Point Triage (power=0, ehp=255) scores quantum_moth as a 3-pack!
            zp_cands = hunt_net.score_pack_targets(
                {"name": "Zero Point", "system": "gsc_0044"}, {"power": 0.0, "ehp": 255.0}, world, pol, {}, {}
            )
            self.assertTrue(len(zp_cands) >= 1)
            self.assertEqual(zp_cands[0]["species"], "quantum_moth")
            self.assertEqual(zp_cands[0]["desired_size"], 3)


if __name__ == "__main__":
    unittest.main()
