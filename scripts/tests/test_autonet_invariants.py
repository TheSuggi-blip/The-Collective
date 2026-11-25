#!/usr/bin/env python3
"""Unit tests for AutoNet structural invariants, anti-stall fixes, hangar reconciliation, and Jump Gate map parsing."""
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "game" / "fleet"))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "station"))

import ast
import bursar
import haul
import mine_net
import scorecard
import upgrades


def _load_hunt_leave_reason():
    src = (REPO / "game" / "fleet" / "hunt.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "leave_reason":
            exec(compile(ast.Module(body=[node], type_ignores=[]), "hunt.py", "exec"), ns)
            return ns["leave_reason"]
    raise AssertionError("leave_reason not found in hunt.py")


class AutoNetValidatorTests(unittest.TestCase):
    def test_live_repo_passes_validate_autonet(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("validate_autonet", REPO / "scripts" / "validate-autonet.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.check_repo(REPO), [])

    def test_validator_blocks_stripped_arbitrage_and_choked_mining(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("validate_autonet", REPO / "scripts" / "validate-autonet.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / "game" / "routes" / "plans").mkdir(parents=True)
            for rel in mod.REQUIRED_POLICIES:
                (t / rel).write_text((REPO / rel).read_text(encoding="utf-8"), encoding="utf-8")
            for rel in mod.REQUIRED_PLAN_ROUTES:
                (t / rel).write_text((REPO / rel).read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual(mod.check_repo(t), [])

            # Strip arbitrage from haul-policy.json -> MUST FAIL
            hp = json.loads((t / "game" / "haul-policy.json").read_text(encoding="utf-8"))
            hp["lanes"] = ["active_freight", "public_freight", "internal_supply"]
            (t / "game" / "haul-policy.json").write_text(json.dumps(hp), encoding="utf-8")
            errs = mod.check_repo(t)
            self.assertTrue(any("arbitrage" in e for e in errs), errs)

            # Choke mine-policy.json -> MUST FAIL
            mp = json.loads((t / "game" / "mine-policy.json").read_text(encoding="utf-8"))
            mp["policed_only"] = True
            mp["allow_lawless_for_deficit"] = False
            mp["lawless_min_tier"] = 9
            (t / "game" / "mine-policy.json").write_text(json.dumps(mp), encoding="utf-8")
            errs2 = mod.check_repo(t)
            self.assertTrue(any("starves miners" in e for e in errs2), errs2)

            # Strip mine-network from miner.json -> MUST FAIL
            pl = json.loads((t / "game" / "routes" / "plans" / "miner.json").read_text(encoding="utf-8"))
            pl["routes"] = [r for r in pl["routes"] if r != "mine-network"]
            (t / "game" / "routes" / "plans" / "miner.json").write_text(json.dumps(pl), encoding="utf-8")
            errs3 = mod.check_repo(t)
            self.assertTrue(any("mine-network" in e for e in errs3), errs3)


class AutoNetEngineFixesTests(unittest.TestCase):
    def test_haul_load_policy_enforces_core_lanes_and_slippage_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "haul-policy.json"
            p.write_text(json.dumps({"enabled": False, "lanes": ["active_freight"]}), encoding="utf-8")
            pol = haul.load_policy(p)
            self.assertTrue(pol["enabled"])
            for ln in ("active_freight", "internal_supply", "public_freight", "arbitrage", "liquidate_surplus"):
                self.assertIn(ln, pol["lanes"])

        now_t = time.time()
        bmap = {
            "base_a": ("sys_a", "poi_a", "base_a", "voidborn"),
            "base_b": ("sys_b", "poi_b", "base_b", "voidborn"),
        }
        lanes = {"sys_a": ["sys_b"], "sys_b": ["sys_a"]}
        books = [
            {"base": "base_a", "item": "circuit_board", "ask": 100, "ask_qty": 100, "bid": 80, "bid_qty": 10, "t": now_t - 60},
            {"base": "base_b", "item": "circuit_board", "ask": 200, "ask_qty": 10, "bid": 160, "bid_qty": 50, "t": now_t - 60},
        ]
        pol_cap = dict(haul.DEFAULT_POLICY, arb_bid_depth_cap=0.5, min_arb_bid_qty=2)
        job = haul.pick_arbitrage_job(books, bmap, lanes, "sys_a", 100, 50000, pol_cap, set(), now_t=now_t)
        self.assertIsNotNone(job)
        self.assertEqual(job["qty"], 25)  # 50 * 0.5 cap

    def test_hunt_leave_reason_honors_pirates_mode_and_partner_tags(self):
        leave_reason = _load_hunt_leave_reason()
        near = {
            "pirate_count": 0,
            "nearby": [
                {"username": "neutral_miner", "faction_tag": "RAND"},
                {"username": "partner_scout", "faction_tag": "HEXC"},
            ],
        }
        # In pirates mode, harmless neutral passersby are ignored
        self.assertIsNone(leave_reason(near, {"drone-1"}, "pirates", {"bad_pk"}))
        # Filed hostile pilot triggers leave in pirates mode
        near_h = {"pirate_count": 0, "nearby": [{"username": "bad_pk", "faction_tag": "EVIL"}]}
        self.assertIsNotNone(leave_reason(near_h, {"drone-1"}, "pirates", {"bad_pk"}))
        # Partner tag ignored even in strangers mode
        near_p = {"pirate_count": 0, "nearby": [{"username": "partner_scout", "faction_tag": "HEXC"}]}
        self.assertIsNone(leave_reason(near_p, {"drone-1"}, "strangers", set(), ignore_tags=("HEXC",)))
        # Pirate always triggers leave
        near_pir = {"pirate_count": 1, "nearby": []}
        self.assertIsNotNone(leave_reason(near_pir, {"drone-1"}, "pirates", set()))

    def test_bursar_market_reality_hits_live_bid_below_inflated_catalog(self):
        book = {"focused_crystal": {"best_buy": 115, "best_buy_qty": 100, "best_sell": 120}}
        stored = {"focused_crystal": 40}
        catalog = {"focused_crystal": 1200}
        pol = dict(bursar.DEFAULT_POLICY, sell={"enabled": True, "min_price_ratio": 0.65, "instant_hit_bid_ratio": 0.80, "respect_reserve": True, "max_orders_per_station": 8}, buy={"enabled": False})
        acts = bursar.plan_bursar_actions(book, stored, [], {}, set(), catalog, 50000, pol)
        self.assertTrue(any(a[0] == "sell_bid" and a[1] == "focused_crystal" for a in acts), acts)

    def test_mine_net_high_value_keeps_crystals_while_blocking_bloated_copper(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            (data / "store").mkdir(parents=True)
            (data / "routes").mkdir(parents=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE lanes (a TEXT, b TEXT);
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, base TEXT);
                CREATE TABLE fields (system TEXT, poi TEXT, resource TEXT, remaining INTEGER, max_remaining INTEGER, richness INTEGER, t INTEGER);
                CREATE TABLE items (id TEXT, base_value REAL);
                CREATE TABLE books (base TEXT, system TEXT, item TEXT, bid REAL, bid_qty INTEGER);
                CREATE TABLE inventory (item TEXT, units INTEGER);
                INSERT INTO lanes VALUES ('s1', 's2');
                INSERT INTO systems VALUES ('s1', 'voidborn', 0), ('s2', 'voidborn', 0);
                INSERT INTO places VALUES ('s1', 'st1', 'station', 'St1', 'b1');
                INSERT INTO fields VALUES ('s1', 'p_cu', 'copper_ore', 90000, 100000, 5, 1),
                                          ('s1', 'p_fc', 'fury_crystal', 900, 1000, 5, 1);
                INSERT INTO items VALUES ('copper_ore', 8), ('fury_crystal', 450);
                INSERT INTO books VALUES ('b1', 's1', 'copper_ore', 4, 100), ('b1', 's1', 'fury_crystal', 440, 50);
                INSERT INTO inventory VALUES ('copper_ore', 800000), ('fury_crystal', 200);
            """)
            con.commit()
            con.close()
            pol = dict(mine_net.DEFAULT_POLICY, market_tier=True, craft_demand_tier=False,
                       market_min_bid=10, high_value_market_min_bid=25, high_value_stock_cap=2000)
            w = mine_net.load_graph_and_world(str(data), str(tmp), pol, now_t=time.time())
            pilot = {"name": "miner-1", "system": "s1", "tier": 0, "modules": ["mining_laser_i"]}
            tiers = {c["resource"]: c["tier"] for c in mine_net.score_belt_candidates(pilot, w, pol, {}, {})}
            self.assertEqual(tiers.get("fury_crystal"), "market")
            self.assertEqual(tiers.get("copper_ore"), "xp_fallback")

    def test_upgrades_reconcile_built_hangars_marks_switched_and_enqueues_orphans(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "store").mkdir(parents=True)
            (data / "comms").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.execute("CREATE TABLE places (system TEXT, poi TEXT, base TEXT, name TEXT)")
            con.execute("INSERT INTO places VALUES ('unknown_edge', 'mobile_capital', 'frontier_station', 'Frontier Station')")
            con.commit()
            con.close()
            (data / "comms" / "messages.jsonl").write_text(
                json.dumps({
                    "sender": "Shipyard Authority",
                    "pilot": "hauler-53",
                    "text": "Your commissioned Prayer is built and docked at Frontier Station. Use switch_ship to fly it.",
                }) + "\n",
                encoding="utf-8",
            )
            pmap = {
                "miner-18": ("Mining", 50000, {"name": "miner-18", "class": "Resonance Miner"}),
                "hauler-53": ("Logistics", 20000, {"name": "hauler-53", "class": "Cobble"}),
            }
            rows = [{"id": "u-8", "pilot": "miner-18", "hull": "resonance_miner", "state": "building", "station": "s:p:b"}]
            changed = upgrades.reconcile_built_hangars(data, pmap, rows, time.time())
            self.assertTrue(changed)
            self.assertEqual(rows[0]["state"], "done")
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1]["pilot"], "hauler-53")
            self.assertEqual(rows[1]["hull"], "prayer")
            self.assertEqual(rows[1]["station"], "unknown_edge:mobile_capital:frontier_station")
            self.assertTrue(rows[1]["ready_to_switch"])

    def test_scorecard_flags_autonet_lane_missing_and_stalled_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (repo / "game").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            (data / "fleet" / "orders").mkdir(parents=True)
            (repo / "game" / "haul-policy.json").write_text(
                json.dumps({"enabled": True, "lanes": ["active_freight", "public_freight", "internal_supply"]}),
                encoding="utf-8",
            )
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.execute("CREATE TABLE runs (pilot TEXT, route TEXT, t REAL, row TEXT)")
            now = time.time()
            for i in range(15):
                con.execute("INSERT INTO runs VALUES (?, 'haul-network', ?, ?)", (f"hauler-{i}", now - 60, json.dumps({"notes": ["docked watch 15m"]})))
            con.commit()
            sn = scorecard._compute_smart_networks(repo, data, conn=con, tables={"runs"}, live_div={"Logistics": {"total": 20, "working": 20}}, now=now)
            con.close()
            self.assertEqual(sn["Logistics"]["status"], "ALARM")
            self.assertEqual(sn["Logistics"]["notice"]["code"], "AUTONET_LANE_MISSING")
            self.assertEqual(sn["Logistics"]["fill_pct_2h"], 0.0)

    def test_station_load_map_preserves_gates_and_frontier_tier(self):
        import server
        fake_map = {
            "systems": [
                {"id": f"sys_{i}", "name": f"Sys {i}", "x": float(i), "y": 0.0, "empire": "voidborn",
                 "connections": [f"sys_{i+1}"] if i < 104 else [], "frontier_tier": 1 if i == 104 else 0}
                for i in range(105)
            ],
            "empires": {"voidborn": "#8888ff"},
            "gates": [{"from_system": "sys_104", "to_system": "sys_0", "online": True}],
        }
        with mock.patch.object(server, "fetch", return_value=json.dumps(fake_map)):
            m = server.load_map()
        self.assertEqual(len(m["gates"]), 1)
        self.assertEqual(m["gates"][0], {"from": "sys_104", "to": "sys_0", "online": True})
        self.assertEqual(m["systems"][104]["frontier_tier"], 1)


if __name__ == "__main__":
    unittest.main()

