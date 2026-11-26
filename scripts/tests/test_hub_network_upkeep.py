#!/usr/bin/env python3
"""Unit tests for multi-hub AutoNet, RouteMaker Owned Outposts/Lockboxes, and Hauler Hub Upkeep."""
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import haul
import hunt_net
import mine_net
import routemaker


def _make_db(db_path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.executescript("""
        CREATE TABLE lanes (a TEXT, b TEXT);
        CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
        CREATE TABLE places (system TEXT, poi TEXT, base TEXT, name TEXT, kind TEXT);
        CREATE TABLE stations (name TEXT, system TEXT, kind TEXT, services TEXT, tag TEXT);
        CREATE TABLE bases (base TEXT, name TEXT, system TEXT, poi TEXT, kind TEXT);
        CREATE TABLE faction_facilities (system TEXT, base TEXT, type TEXT, status TEXT, rent_per_cycle INTEGER);
        CREATE TABLE fields (system TEXT, poi TEXT, resource TEXT, remaining INTEGER, max_remaining INTEGER, richness REAL, t REAL);
        CREATE TABLE items (id TEXT, base_value REAL);
        CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER, t REAL);
        CREATE TABLE herds (system TEXT, poi TEXT, creature TEXT, name TEXT, role TEXT, count INTEGER, t REAL);
        CREATE TABLE observations (kind TEXT, subject TEXT, t REAL);
        CREATE TABLE need_status (priority INTEGER, gather TEXT, short_items TEXT);
        CREATE TABLE supply_status (item TEXT, stock INTEGER, keep INTEGER);
    """)
    con.executemany("INSERT INTO lanes VALUES (?, ?)", [
        ("node_beta", "nexus_prime"),
        ("nexus_prime", "felis"),
        ("node_beta", "sol"),
        ("node_beta", "krynn"),
        ("felis", "oakridge"),
    ])
    con.executemany("INSERT INTO systems VALUES (?, ?, ?)", [
        ("node_beta", "voidborn", 0),
        ("nexus_prime", "voidborn", 0),
        ("sol", "solarian", 0),
        ("krynn", "crimson", 0),
        ("felis", "", 0),
        ("oakridge", "", 0),
    ])
    con.executemany("INSERT INTO places VALUES (?, ?, ?, ?, ?)", [
        ("node_beta", "nb_poi", "node_beta_industrial_station", "Node Beta", "station"),
        ("sol", "sol_central", "confederacy_central_command", "Sol Central", "station"),
        ("krynn", "war_citadel", "crimson_war_citadel", "Crimson War Citadel", "station"),
    ])
    con.executemany("INSERT INTO stations VALUES (?, ?, ?, ?, ?)", [
        ("Node Beta", "node_beta", "station", "storage,market,refuel", ""),
        ("Sol Central", "sol", "station", "storage,market,refuel", ""),
        ("Crimson War Citadel", "krynn", "station", "storage,market,refuel", ""),
    ])
    con.executemany("INSERT INTO bases VALUES (?, ?, ?, ?, ?)", [
        ("felis_outpost_id", "CLTV Outpost Felis", "felis", "felis_op_poi", "outpost"),
        ("oakridge_st_id", "CLTV Station Oakridge", "oakridge", "oak_poi", "station"),
    ])
    con.executemany("INSERT INTO faction_facilities VALUES (?, ?, ?, ?, ?)", [
        ("node_beta", "node_beta_industrial_station", "faction_lockbox", "active", 69),
        ("sol", "confederacy_central_command", "faction_lockbox", "active", 69),
        ("krynn", "crimson_war_citadel", "faction_lockbox", "active", 69),
        ("felis", "felis_outpost_id", "faction_lockbox", "active", 0),
        ("felis", "felis_outpost_id", "faction_fuel_bunker", "active", 0),
        ("oakridge", "oakridge_st_id", "faction_lockbox", "active", 0),
    ])
    con.commit()
    con.close()


class MultiHubUpkeepTests(unittest.TestCase):
    def test_routemaker_generates_owned_outpost_route_with_faction_deposit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "game"
            data = Path(td) / "data"
            (root / "map").mkdir(parents=True)
            (root / "map" / "galaxy.tsv").write_text(
                "id\tlanes\nnode_beta\tfelis\nfelis\tnode_beta\n", encoding="utf-8"
            )
            (data / "scouting").mkdir(parents=True)
            (data / "market").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
            (data / "fleet" / "strict-classes-on").write_text("1", encoding="utf-8")
            (data / "empire").mkdir(parents=True)
            (data / "empire" / "empire.json").write_text(json.dumps({
                "faction": {"id": "cltv"},
                "bases": [{"base": "felis_op", "name": "CLTV Outpost Felis", "system": "felis", "poi": "felis_op_poi", "kind": "outpost"}],
                "facilities": [{"base": "felis_op", "type": "faction_lockbox", "status": "active", "rent_per_cycle": 0}],
            }), encoding="utf-8")
            (data / "scouting" / "felis.json").write_text(json.dumps({
                "system": "felis", "read_at": "2026-11-25T16:00:00Z",
                "pois": {
                    "felis_belt_b": {
                        "poi": {"name": "Felis Belt B", "type": "asteroid_belt"},
                        "resources": [{"resource_id": "iron_ore", "richness": 100, "remaining": 90000, "max_remaining": 100000}],
                    }
                }
            }), encoding="utf-8")
            (data / "scouting" / "node_beta.json").write_text(json.dumps({
                "system": "node_beta", "read_at": "2026-11-25T16:00:00Z",
                "pois": {
                    "nb_poi": {"poi": {"name": "Node Beta", "type": "station", "base_id": "nb_base"}}
                }
            }), encoding="utf-8")
            (data / "market" / "nb_base.json").write_text(json.dumps({
                "base": "nb_base", "system": "node_beta", "read_at": "2026-11-25T16:00:00Z",
                "items": [{"item_id": "iron_ore", "best_buy": 40, "best_buy_qty": 5000, "best_sell": 50, "best_sell_qty": 100}],
            }), encoding="utf-8")
            world = routemaker.load_world(data, root, now=time.time())
            self.assertIn("felis_op", world["owned_hubs"])
            self.assertIn("felis_op", world["lockboxes"])
            cands = routemaker.mine_candidates(world)
            self.assertEqual(len(cands), 1)
            c = cands[0]
            self.assertEqual(c["route"]["station"], "felis:felis_op_poi:felis_op")
            self.assertEqual(c["route"]["deposit"], "faction")
            self.assertEqual(c["basis"]["hub_kind"], "owned_outpost")

    def test_mine_net_autodiscovers_outpost_from_bases_and_applies_hub_gravity(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            repo = Path(td) / "repo"
            (repo / "game").mkdir(parents=True)
            _make_db(data / "store" / "read.db")
            con = sqlite3.connect(data / "store" / "read.db")
            con.execute("INSERT INTO fields VALUES ('felis', 'felis_belt_b', 'iron_ore', 95000, 100000, 100.0, ?)", (time.time(),))
            con.execute("INSERT INTO items VALUES ('iron_ore', 15.0)")
            con.commit()
            con.close()
            pol = dict(mine_net.DEFAULT_POLICY)
            pol.update({"auto_use_owned_outposts": True, "hub_gravity_bonus": True, "policed_only": False, "market_tier": False, "priority_resources": ["iron_ore"]})
            world = mine_net.load_graph_and_world(data, repo, pol)
            self.assertIn("felis_outpost_id", world["owned_outpost_bases"])
            self.assertIn("felis", world["stations_by_sys"])
            ship = {"name": "miner-1", "system": "felis", "tier": 2, "modules": ["mining_laser_ii"]}
            cands_on = mine_net.score_belt_candidates(ship, world, pol, {}, {})
            pol_off = dict(pol, hub_gravity_bonus=False)
            cands_off = mine_net.score_belt_candidates(ship, world, pol_off, {}, {})
            self.assertEqual(len(cands_on), 1)
            self.assertEqual(cands_on[0]["station"], "felis:felis_op_poi:felis_outpost_id")
            self.assertGreater(cands_on[0]["score"], cands_off[0]["score"])

    def test_hunt_net_prefers_empire_lockbox_hubs(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            repo = Path(td) / "repo"
            (repo / "game").mkdir(parents=True)
            _make_db(data / "store" / "read.db")
            world = hunt_net._load_combat_world_uncached(data, repo, hunt_net.DEFAULT_POLICY, time.time())
            self.assertIn("crimson_war_citadel", world["lockbox_bases"])
            self.assertIn("confederacy_central_command", world["lockbox_bases"])
            self.assertIn("felis_outpost_id", world["lockbox_bases"])

    def test_haul_hub_upkeep_transfer_buy_and_no_pingpong(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            _make_db(data / "store" / "read.db")
            (data / "stock").mkdir(parents=True)
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {
                    "Faction": {
                        "stations": {
                            "node_beta_industrial_station": {"steel_plate": 1500, "circuit_board": 400},
                            "felis_outpost_id": {"iron_ore": 500, "steel_plate": 100},
                            "oakridge_st_id": {"steel_plate": 300, "fuel_cell": 900, "circuit_board": 100, "flex_polymer": 150, "copper_wiring": 150, "hull_patch": 40, "repair_kit": 50},
                        }
                    }
                }
            }), encoding="utf-8")
            (data / "empire").mkdir(parents=True, exist_ok=True)
            (data / "empire" / "empire.json").write_text(json.dumps({"members": [{"pilot": "hauler-1", "role": "Officer"}, {"pilot": "hauler-2", "role": "Officer"}, {"pilot": "hauler-3", "role": "Officer"}]}), encoding="utf-8")
            base_map = haul._load_base_map_uncached(data)
            self.assertIn("felis_outpost_id", base_map)
            self.assertIn("oakridge_st_id", base_map)
            lanes = {"node_beta": ["nexus_prime", "sol"], "nexus_prime": ["node_beta", "felis"], "felis": ["nexus_prime", "oakridge"], "oakridge": ["felis"], "sol": ["node_beta"]}
            pol = dict(haul.DEFAULT_POLICY)
            now_t = time.time()
            books = [{"base": "confederacy_central_command", "item": "fuel_cell", "ask": 35, "ask_qty": 500, "bid": 20, "bid_qty": 100, "t": now_t}]
            job1 = haul._pick_hub_upkeep(data, "hauler-1", books, base_map, lanes, "node_beta", 300, 15000, pol, set(), now_t=now_t)
            self.assertIsNotNone(job1)
            self.assertEqual(job1["item"], "fuel_cell")
            self.assertEqual(job1["mode"], "buy")
            self.assertEqual(job1["dest"][2], "felis_outpost_id")
            self.assertEqual(job1["qty"], 200)
            job2 = haul._pick_hub_upkeep(data, "hauler-2", books, base_map, lanes, "node_beta", 300, 15000, pol, {job1["job_key"]}, now_t=now_t)
            self.assertIsNotNone(job2)
            self.assertEqual(job2["mode"], "transfer")
            self.assertEqual(job2["origin"][2], "node_beta_industrial_station")
            con = sqlite3.connect(data / "store" / "read.db")
            con.execute("INSERT INTO need_status (priority, gather, short_items) VALUES (1, '', 'steel_plate 500, iron_ore 500')")
            con.commit()
            con.close()
            sup = haul._pick_internal_supply(data, "hauler-3", base_map, lanes, "felis", 300, pol, set())
            self.assertIsNotNone(sup)
            self.assertEqual(sup["item"], "iron_ore")
            self.assertEqual(sup["origin"][2], "felis_outpost_id")


    def test_hub_upkeep_min_lot_and_bunker_fill(self):
        """Tiny 5-12 cell warehouse scraps must NOT trigger a 10-jump micro-transfer;
        outposts with low fuel bunkers must trigger bunker_fill bulk buys up to 115 cr,
        and hubs with empty/unscouted POI must be skipped safely."""
        import json, sqlite3, tempfile, time
        with tempfile.TemporaryDirectory() as td:
            tmp_path = Path(td)
            db_p = tmp_path / "store" / "read.db"
            db_p.parent.mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(db_p)
            con.execute("CREATE TABLE bases (base TEXT, system TEXT, poi TEXT, kind TEXT)")
            con.execute("CREATE TABLE places (base TEXT, poi TEXT)")
            con.execute("INSERT INTO bases VALUES ('outpost_ok', 'felis', 'poi_felis_ok', 'outpost')")
            con.execute("INSERT INTO bases VALUES ('outpost_nopoi', 'unscouted', '', 'outpost')")
            con.commit(); con.close()

            (tmp_path / "stock").mkdir(parents=True, exist_ok=True)
            (tmp_path / "stock" / "storage.json").write_text(json.dumps({
                "faction": [{"base": "node_beta_industrial_station", "items": [{"item_id": "fuel_cell", "quantity": 12}]}],
                "pilots": {},
            }), encoding="utf-8")
            (tmp_path / "empire").mkdir(parents=True, exist_ok=True)
            (tmp_path / "empire" / "empire.json").write_text(json.dumps({
                "facilities": [{"type": "faction_fuel_bunker", "status": "active", "base": "outpost_ok"}],
                "faction_storage": [{"base": "outpost_ok", "item": "fuel", "units": 200}],
            }), encoding="utf-8")

            base_map = {
                "node_beta_industrial_station": ("node_beta", "node_beta_industrial_station", "node_beta_industrial_station", "voidborn"),
                "node_alpha_processing_station": ("node_alpha", "node_alpha_processing_station", "node_alpha_processing_station", "voidborn"),
                "outpost_ok": ("felis", "poi_felis_ok", "outpost_ok", ""),
            }
            lanes = {"node_beta": ["node_alpha", "felis"], "node_alpha": ["node_beta"], "felis": ["node_beta"]}
            books = [{"base": "node_alpha_processing_station", "item": "fuel_cell", "ask": 100, "ask_qty": 500, "t": time.time()}]
            pol = haul.load_policy()
            job = haul._pick_hub_upkeep(tmp_path, "hauler-1", books, base_map, lanes, "node_beta", 120, 15000, pol, set())
            self.assertIsNotNone(job)
            self.assertEqual(job["dest"][2], "outpost_ok")
            self.assertTrue(job["bunker_fill"])
            self.assertEqual(job["mode"], "buy")
            self.assertGreaterEqual(job["qty"], 100)


    def test_pull_to_cash_role_guard_consolidate_and_bursar_pull(self):
        """Verify Member haulers cannot pick faction-storage withdraws, Officer haulers consolidate
        outpost surplus to docked Bursars, and Bursars select marketable faction surplus cleanly."""
        import json, tempfile, time
        import bursar
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "empire").mkdir(parents=True, exist_ok=True)
            (d / "fleet").mkdir(parents=True, exist_ok=True)
            (d / "stock").mkdir(parents=True, exist_ok=True)
            (d / "empire" / "empire.json").write_text(json.dumps({
                "members": [
                    {"pilot": "hauler-1", "role": "Officer"},
                    {"pilot": "hauler-99", "role": "Member"},
                    {"pilot": "trader-3", "role": "Officer"},
                ],
                "facilities": [
                    {"type": "faction_lockbox", "status": "active", "base": "node_beta_industrial_station"},
                    {"type": "faction_lockbox", "status": "active", "base": "outpost_atria"},
                ],
                "faction_storage": [
                    {"base": "outpost_atria", "item": "null_matter", "units": 200},
                ],
            }), encoding="utf-8")
            (d / "fleet" / "bursar_claims.json").write_text(json.dumps({
                "node_beta_industrial_station": {"pilot": "trader-3", "claimed_at": time.time()},
            }), encoding="utf-8")
            (d / "stock" / "storage.json").write_text(json.dumps({"pilots": {}}), encoding="utf-8")

            self.assertTrue(haul._pilot_can_withdraw_faction(d, "hauler-1"))
            self.assertFalse(haul._pilot_can_withdraw_faction(d, "hauler-99"))

            base_map = {
                "outpost_atria": ("atria", "poi_atria", "outpost_atria", ""),
                "node_beta_industrial_station": ("node_beta", "node_beta_industrial_station", "node_beta_industrial_station", "voidborn"),
            }
            lanes = {"atria": ["node_beta"], "node_beta": ["atria"]}
            books = [{"base": "node_beta_industrial_station", "item": "null_matter", "bid": 590, "bid_qty": 100, "ask": 650, "t": time.time()}]
            pol = haul.load_policy()

            j_mem = haul._pick_consolidate_to_trader(d, "hauler-99", books, base_map, lanes, "atria", 100, pol, set())
            self.assertIsNone(j_mem)

            j_off = haul._pick_consolidate_to_trader(d, "hauler-1", books, base_map, lanes, "atria", 100, pol, set())
            self.assertIsNotNone(j_off)
            self.assertEqual(j_off["item"], "null_matter")
            self.assertEqual(j_off["dest"][2], "node_beta_industrial_station")
            self.assertEqual(j_off["bursar_pilot"], "trader-3")

            picks = bursar._select_faction_surplus_to_pull(
                {"fuel_cell": 100, "null_matter": 50, "junk_unlisted": 80},
                {"null_matter": {"best_buy": 590, "best_sell": 650}},
                {"fuel_cell"},
                free_hold=80,
            )
            self.assertEqual(picks, [("null_matter", 50)])


    def test_bursar_hits_live_bid_ignoring_inflated_catalog_base(self):
        """Bursar must sell into real live cash bids (e.g. phase_crystal @ 110 cr) instead of letting
        stale inflated catalog base_v (300 cr) block instant cash conversion."""
        import bursar
        book = {"phase_crystal": {"best_buy": 110, "best_buy_qty": 200, "best_sell": 145}}
        pol = {"min_cash_keep": 20000, "sell": {"enabled": True, "max_orders_per_station": 16, "undercut_cr": 1, "min_price_ratio": 0.65, "instant_hit_bid_ratio": 0.72, "respect_reserve": True}, "buy": {"enabled": False}}
        acts = bursar.plan_bursar_actions(book, {"phase_crystal": 40}, [], {}, set(), {"phase_crystal": 300}, 50000, pol)
        self.assertEqual(acts, [("sell_bid", "phase_crystal", 40, 110)])



    def test_zero_catalog_adaptive_bursar_and_lockbox_miner_guard(self):
        import time as _t
        import bursar
        # 1. Zero catalog fallback: if local bid=0, ask=0, and live galactic bid=0, bursar skips (never uses catalog!)
        acts_empty = bursar.plan_bursar_actions(
            book={"mystery_junk": {"best_buy": 0, "best_buy_qty": 0, "best_sell": 0}},
            stored_items={"mystery_junk": 50},
            own_orders=[],
            open_needs={},
            reserved=set(),
            live_market_vals={},
            credits=100000,
            policy={"sell": {"enabled": True, "min_price_ratio": 0.65, "instant_hit_bid_ratio": 0.70}, "buy": {"enabled": False}},
        )
        self.assertEqual(acts_empty, [])

        # 2. Adaptive stale-order price decay: our top ask sitting 40m unsold steps down by 6%!
        now_t = _t.time()
        acts_decay = bursar.plan_bursar_actions(
            book={"silver_ore": {"best_buy": 60, "best_buy_qty": 500, "best_sell": 200}},
            stored_items={"silver_ore": 100},
            own_orders=[{"order_id": "ord-stale", "item_id": "silver_ore", "side": "sell", "remaining": 100, "price_each": 200}],
            open_needs={},
            reserved=set(),
            live_market_vals={"silver_ore": 100.0},
            credits=100000,
            policy={"sell": {"enabled": True, "min_price_ratio": 0.65, "instant_hit_bid_ratio": 0.70, "stale_step_minutes": 25, "stale_step_pct": 0.06}, "buy": {"enabled": False}},
            order_first_seen={"ord-stale": int(now_t - 40 * 60)},
            now_t=now_t,
        )
        self.assertIn(("sell_modify", "silver_ore", "ord-stale", 188), acts_decay)

        # 3. mine-policy.json strictly locks deposit_stations to 10 Lockbox/Outpost hubs & zero non-Lockbox NPC bases
        mp = json.loads((Path(__file__).resolve().parents[2] / "game" / "mine-policy.json").read_text(encoding="utf-8"))
        self.assertEqual(mp.get("deposit_mode"), "faction")
        self.assertEqual(len(mp.get("deposit_stations") or []), 10)
        for bad_base in ("nova_terra_central", "alpha_centauri_colonial_station", "synchrony_hub", "grand_exchange_station"):
            self.assertFalse(any(bad_base in s for s in mp["deposit_stations"]), f"Non-lockbox base {bad_base} leaked in deposit_stations")

        # 4. haul-policy.json prioritizes liquidate_surplus before arbitrage & tightens arb
        hp = json.loads((Path(__file__).resolve().parents[2] / "game" / "haul-policy.json").read_text(encoding="utf-8"))
        self.assertLess(hp["lanes"].index("liquidate_surplus"), hp["lanes"].index("arbitrage"))
        self.assertGreaterEqual(int(hp.get("liquidate_max_slots") or 0), 20)
        self.assertGreaterEqual(float(hp.get("min_margin_pct") or 0), 0.25)



    def test_command_leader_pack_doctrine_and_antiflood_10j(self):
        import hunt_net
        # 1. Command-Ship-Only Pack Leadership Doctrine: non-Command ship CANNOT start a pack!
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            (td / "fleet").mkdir(parents=True, exist_ok=True)
            (td / "fleet" / "flagships.json").write_text(json.dumps({"Prime Directive": {"flagship": True}}), encoding="utf-8")
            w = {"adj": {"sys_a": ["sys_b"], "sys_b": ["sys_a"]}}
            pol = {"packs": {"enabled": True, "require_command_leader": True, "target_share": 0.30, "sizes": [3], "min_member_power": 500.0, "command_flagship_min_power": 150.0, "rally_max_jumps": 10, "rally_timeout_s": 300, "max_forming_packs": 4}}
            targets = [{"key": "pack:sys_a:poi_1", "place_key": "sys_a:poi_1", "mode": "wildlife", "system": "sys_a", "poi": "poi_1", "species": "cloudwhale", "prey_hull": 3433, "desired_size": 3, "dock": "sys_a:st:b1"}]
            spow_d = {"power": 900.0, "tier": 1}
            spow_c = {"power": 300.0, "tier": 1}
            # Regular drone tries to form pack alone -> MUST be rejected (None)!
            self.assertIsNone(hunt_net.pack_try_join_or_create(td, "drone-1", "sys_a", spow_d, targets, w, pol, 40, now_t=1000.0))
            # Command Flagship creates pack -> succeeds as leader!
            pk_cmd = hunt_net.pack_try_join_or_create(td, "Prime Directive", "sys_a", spow_c, targets, w, pol, 40, now_t=1001.0)
            self.assertIsNotNone(pk_cmd)
            self.assertEqual(pk_cmd["leader"], "Prime Directive")
            # Now regular drones join the Command-led pack and launch it!
            pk_j1 = hunt_net.pack_try_join_or_create(td, "drone-1", "sys_a", spow_d, targets, w, pol, 40, now_t=1002.0)
            self.assertEqual(pk_j1["leader"], "Prime Directive")
            pk_j2 = hunt_net.pack_try_join_or_create(td, "drone-2", "sys_b", spow_d, targets, w, pol, 40, now_t=1003.0)
            self.assertEqual(pk_j2["state"], "launched")
            self.assertEqual(pk_j2["leader"], "Prime Directive")


        # 2. Verify live policy invariants (10J radius, Command leadership, lawless-only, zero hardcoded bans, 8M floor / unlimited 24h upgrades)
        root = Path(__file__).resolve().parents[2]
        hp = json.loads((root / "game" / "hunt-policy.json").read_text(encoding="utf-8"))
        self.assertTrue(hp["packs"]["require_command_leader"])
        self.assertTrue(hp["packs"]["pirates_enabled"])
        self.assertTrue(hp["lawless_only"])
        self.assertEqual(hp["packs"]["max_jumps"], 10)
        self.assertFalse(hp["fallback"]["enabled"])
        self.assertEqual(hp["exclude_species"], [])
        mp = json.loads((root / "game" / "mine-policy.json").read_text(encoding="utf-8"))
        self.assertEqual(mp["max_station_jumps"], 10)
        self.assertGreaterEqual(mp["min_market_buyer_qty"], 20)
        self.assertFalse(mp["allow_xp_fallback"])
        self.assertEqual(mp["exclude_resources"], [])
        self.assertGreaterEqual(mp["market_min_bid"], 12)
        up = json.loads((root / "game" / "upgrade-policy.json").read_text(encoding="utf-8"))
        self.assertEqual(up["treasury_floor_cr"], 8000000)
        self.assertEqual(up["max_spend_24h_cr"], 0)

    def test_suggi_lawless_all10_cmd_unlimited_upgrades_and_fuel_loop(self):
        """Verify 10/10 Command ships (incl. unarmed w=0), Lawless-Only Military, and zero-fuel glut sell_bid."""
        import bursar
        root = Path(__file__).resolve().parents[2]
        ppol = hunt_net.load_policy(root / "game" / "hunt-policy-packs.json")
        hpol = hunt_net.load_policy()
        self.assertTrue(hpol.get("lawless_only"))
        self.assertTrue(ppol.get("lawless_only"))
        self.assertEqual(hpol.get("exclude_species"), [])
        self.assertEqual(ppol.get("exclude_species"), [])
        self.assertGreaterEqual(ppol["packs"]["max_forming_packs"], 10)

        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "fleet").mkdir(parents=True)
            (tmp / "fleet" / "flagships.json").write_text(json.dumps({
                "Zero Point": {"flagship": True}, "Crimson Aegis": {"flagship": True}, "Prime Directive": {"flagship": True}
            }), encoding="utf-8")
            w_mix = {
                "data_dir": tmp, "adj": {"sol": ["alpha"], "alpha": ["sol"]},
                "systems": {"sol": {"empire": "solarian", "stronghold": False}, "alpha": {"empire": "", "stronghold": False}},
                "stations_by_sys": {"sol": [("sol", "st_sol", "central_nexus")]},
                "bursar_bases": {"central_nexus"}, "lockbox_bases": {"central_nexus"},
                "ranch_pois": set(), "ranch_systems": set(), "pirates": set(), "pirate_details": {},
                "species_hull": {"cloudwhale": 3433, "frost_moth": 260},
                "species_loot_val": {"cloudwhale": 5000.0, "frost_moth": 4500.0},
                "herds": [
                    {"system": "sol", "poi": "sol_belt", "species": "frost_moth", "role": "grazer", "count": 5},
                    {"system": "alpha", "poi": "alpha_belt", "species": "cloudwhale", "role": "grazer", "count": 5},
                    {"system": "alpha", "poi": "alpha_belt2", "species": "frost_moth", "role": "grazer", "count": 5},
                ],
            }
            solo_c = hunt_net.score_solo_herds(
                {"name": "drone-1", "system": "sol"}, {"power": 1500.0, "dps": 40.0, "ehp": 400.0, "tier": 2},
                w_mix, hpol, {}, {},
            )
            self.assertTrue(len(solo_c) >= 1 and all(c["system"] == "alpha" for c in solo_c))

            zp_cands = hunt_net.score_pack_targets(
                {"name": "Zero Point", "system": "sol"}, {"power": 0.0, "dps": 0.0, "ehp": 469.0, "tier": 2},
                w_mix, ppol, {}, {},
            )
            self.assertTrue(len(zp_cands) >= 1 and all(c["system"] == "alpha" for c in zp_cands))
            pk = hunt_net.pack_try_join_or_create(
                tmp, "Zero Point", "sol", {"power": 0.0, "dps": 0.0, "ehp": 469.0, "tier": 2}, zp_cands, w_mix, ppol, active_military_n=60
            )
            self.assertIsNotNone(pk)
            self.assertEqual(pk["leader"], "Zero Point")

        bpol = json.loads((root / "game" / "bursar-policy.json").read_text(encoding="utf-8"))
        acts = bursar.plan_bursar_actions(
            book={"nitrogen_ice": {"best_buy": 2, "best_buy_qty": 1000, "best_sell": 0}},
            stored_items={"nitrogen_ice": 800},
            own_orders=[], open_needs={}, reserved=set(), live_market_vals={"nitrogen_ice": 2},
            credits=50000, policy=bpol,
        )
        self.assertTrue(any(a[0] == "sell_bid" and a[1] == "nitrogen_ice" and a[2] == 800 for a in acts))



    def test_mine_net_real_bid_qty_competitive_floor_and_relocation(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            repo = Path(td) / "repo"
            (repo / "game").mkdir(parents=True)
            _make_db(data / "store" / "read.db")
            con = sqlite3.connect(data / "store" / "read.db")
            now_t = time.time()
            con.execute("INSERT INTO systems VALUES ('far_pocket', 'crimson', 0)")
            con.execute("INSERT INTO lanes VALUES ('far_pocket', 'oakridge')")
            con.execute("INSERT INTO fields VALUES ('felis', 'felis_silver', 'silver_ore', 1350, 25000, 100.0, ?)", (now_t,))
            con.execute("INSERT INTO fields VALUES ('felis', 'felis_phase', 'phase_crystal', 20000, 25000, 100.0, ?)", (now_t,))
            con.execute("ALTER TABLE books ADD COLUMN bid_depth INTEGER DEFAULT 0")
            con.execute("INSERT INTO books (base, item, bid, bid_qty, bid_depth, ask, ask_qty, t) VALUES ('oakridge_st_id', 'silver_ore', 101.0, 50000, 50000, 120.0, 100, ?)", (now_t,))
            con.execute("INSERT INTO books (base, item, bid, bid_qty, bid_depth, ask, ask_qty, t) VALUES ('oakridge_st_id', 'phase_crystal', 110.0, 10, 50000, 130.0, 100, ?)", (now_t,))
            con.commit()
            con.close()
            pol = dict(mine_net.DEFAULT_POLICY)
            pol.update({
                "min_left_pct": 5.0, "scarce_min_left_pct": 3.0, "scarce_min_bid": 100.0,
                "min_market_buyer_qty": 20, "policed_only": False, "market_tier": True,
                "allow_xp_fallback": False, "priority_resources": [], "max_jumps": 1,
            })
            world = mine_net.load_graph_and_world(data, repo, pol)
            self.assertEqual(world["market"]["phase_crystal"][1], 0)
            self.assertGreater(world["market"]["silver_ore"][1], 40000)
            ship_f = {"name": "miner-f", "system": "felis", "tier": 1, "modules": ["mining_laser_ii"]}
            cands = mine_net.score_belt_candidates(ship_f, world, pol, {}, {})
            self.assertEqual(len(cands), 1)
            self.assertEqual(cands[0]["resource"], "silver_ore")
            self.assertEqual(cands[0]["min_left_pct"], 3.0)
            ship_far = {"name": "miner-far", "system": "far_pocket", "tier": 1, "modules": ["mining_laser_ii"]}
            self.assertEqual(mine_net.score_belt_candidates(ship_far, world, pol, {}, {}), [])
            reloc = mine_net.pick_relocation_hub(ship_far, world, pol, {}, {})
            self.assertIsNotNone(reloc)
            self.assertIn(reloc["system"], ("felis", "oakridge"))

    def test_hunt_net_keep_herd_1_verified_drops_and_adaptive_relocation(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            repo = Path(td) / "repo"
            (repo / "game").mkdir(parents=True)
            _make_db(data / "store" / "read.db")
            con = sqlite3.connect(data / "store" / "read.db")
            now_t = time.time()
            con.execute("INSERT INTO systems VALUES ('crimson_pocket', 'crimson', 0)")
            con.execute("INSERT INTO lanes VALUES ('crimson_pocket', 'oakridge')")
            con.execute("INSERT INTO places VALUES ('felis', 'felis_op_poi', 'felis_outpost_id', 'CLTV Outpost Felis', 'station')")
            con.execute("INSERT INTO herds VALUES ('felis', 'felis_reef', 'rivetshell', 'Rivetshell', 'grazer', 2, ?)", (now_t,))
            con.execute("INSERT INTO books VALUES ('oakridge_st_id', 'rivetshell_meat', 300.0, 8000, 350.0, 100, ?)", (now_t,))
            con.commit()
            con.close()
            pol = dict(hunt_net.DEFAULT_POLICY)
            pol["keep_herd"] = 1
            pol["min_creatures"] = 2
            pol["lawless_only"] = True
            pol["solo"] = dict(pol["solo"], max_jumps=1, min_loot_val=200.0)
            pol["packs"] = dict(pol["packs"], max_jumps=1)
            world = hunt_net._load_combat_world_uncached(data, repo, pol, now_t)
            self.assertGreaterEqual(world["species_loot_val"].get("rivetshell", 0.0), 200.0)
            ship_far = {"name": "drone-c1", "system": "crimson_pocket", "hull": 250, "shield": 120, "modules": ["pulse_laser_iii"]}
            spow = {"power": 950.0, "dps": 25.0, "ehp": 370.0, "tier": 1}
            self.assertEqual(hunt_net.score_solo_herds(ship_far, spow, world, pol, {}, {}), [])
            reloc = hunt_net.pick_relocation_hub(ship_far, spow, world, pol, {}, {})
            self.assertIsNotNone(reloc)
            self.assertEqual(reloc["system"], "felis")



    def test_stage1_haul_consolidate_local_bid_and_bursar_atomic_reserve(self):
        import bursar
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            (data / "stock").mkdir(parents=True)
            (data / "empire").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
            now_t = time.time()
            (data / "empire" / "empire.json").write_text(json.dumps({"members": [{"name": "hauler-1", "role": "officer"}]}), encoding="ascii")
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({
                "dead_hub": {"pilot": "trader-1", "claimed_at": now_t},
                "buyer_hub": {"pilot": "trader-2", "claimed_at": now_t},
            }), encoding="ascii")
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {}, "faction": {"outpost_1": {"plasma_gas": 400}},
            }), encoding="ascii")
            base_map = {
                "outpost_1": ("s_out", "p_out", "outpost_1", False),
                "dead_hub": ("s_dead", "p_dead", "dead_hub", True),
                "buyer_hub": ("s_buy", "p_buy", "buyer_hub", True),
            }
            lanes = {"s_out": ["s_dead", "s_buy"], "s_dead": ["s_out"], "s_buy": ["s_out"]}
            # plasma_gas only has a buyer at buyer_hub (NOT dead_hub!) -> MUST never consolidate to dead_hub!
            books = [{"base": "buyer_hub", "item": "plasma_gas", "bid": 25.0, "bid_qty": 500, "t": now_t}]
            pol = {"max_jumps_pickup": 10, "max_jumps_delivery": 10, "consolidate_min_units": 10, "consolidate_min_value_cr": 500}
            job = haul._pick_consolidate_to_trader(str(data), "hauler-1", books, base_map, lanes, "s_out", 200, pol, set(), now_t=now_t)
            self.assertIsNotNone(job)
            self.assertEqual(job["dest"][2], "buyer_hub")
            # Atomic reserve_fleet_buy stops 60-trader oversubscription!
            g1 = bursar.reserve_fleet_buy(str(data), "trader-1", "dead_hub", "silica_lens", 36, 54, now_t=now_t)
            g2 = bursar.reserve_fleet_buy(str(data), "trader-2", "buyer_hub", "silica_lens", 36, 54, now_t=now_t)
            g3 = bursar.reserve_fleet_buy(str(data), "trader-3", "other_hub", "silica_lens", 36, 54, now_t=now_t)
            self.assertEqual(g1, 36)
            self.assertEqual(g2, 18)
            self.assertEqual(g3, 0)



    def test_craft_net_reads_shared_faction_lockbox_and_tight_idle_timers(self):
        import craft_net
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            repo = Path(td) / "repo"
            (data / "store").mkdir(parents=True)
            (data / "stock").mkdir(parents=True)
            (data / "empire").mkdir(parents=True)
            (repo / "game").mkdir(parents=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE recipes (id TEXT, name TEXT, facility_only INTEGER);
                CREATE TABLE recipe_inputs (recipe TEXT, item TEXT, units INTEGER);
                CREATE TABLE recipe_outputs (recipe TEXT, item TEXT, units INTEGER);
                CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER);
                INSERT INTO recipes VALUES ('refine_methane', 'Refine Methane', 0);
                INSERT INTO recipe_inputs VALUES ('refine_methane', 'methane_ice', 5);
                INSERT INTO recipe_outputs VALUES ('refine_methane', 'liquid_methane', 3);
                INSERT INTO books VALUES ('lockbox_hub', 'methane_ice', 20, 500, 30, 500),
                                         ('lockbox_hub', 'liquid_methane', 100, 500, 120, 500);
            """)
            con.commit()
            con.close()
            (data / "empire" / "empire.json").write_text(json.dumps({
                "members": [{"name": "trader-9", "role": "officer"}],
                "facilities": [{"type": "faction_lockbox", "base": "lockbox_hub", "status": "active"}],
            }), encoding="ascii")
            # Self storage is EMPTY, but shared Faction Lockbox holds 50 methane_ice!
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {"trader-9": {"stations": {"lockbox_hub": {}}}},
                "faction": {"lockbox_hub": {"methane_ice": 50}},
            }), encoding="ascii")
            _rp = Path(__file__).resolve().parents[2]
            pol = json.loads((_rp / "game" / "craft-policy.json").read_text(encoding="ascii"))
            (repo / "game" / "craft-policy.json").write_text(json.dumps(pol), encoding="ascii")
            (repo / "game" / "craft-demand.json").write_text(json.dumps({"enabled": True}), encoding="ascii")
            ship = {"name": "trader-9", "division": "Trade", "base": "lockbox_hub", "credits": 50000}
            self.assertTrue(craft_net.has_craft_job("trader-9", ship, data_dir=data, repo_root=repo))
            # Verify all idle/stale timers <= 2m in live policies
            self.assertLessEqual(int(json.loads((_rp / "game" / "bursar-policy.json").read_text())["sell"]["stale_step_minutes"]), 2)
            self.assertLessEqual(int(json.loads((_rp / "game" / "craft-policy.json").read_text())["idle_watch_minutes"]), 2)
            self.assertLessEqual(int(json.loads((_rp / "game" / "haul-policy.json").read_text())["rest_seconds_when_empty"]), 120)
            self.assertLessEqual(int(json.loads((_rp / "game" / "hunt-policy.json").read_text())["rest_seconds_when_empty"]), 120)


if __name__ == "__main__":
    unittest.main()
