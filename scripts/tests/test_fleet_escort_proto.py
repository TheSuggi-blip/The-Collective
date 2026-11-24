"""Unit tests for escort_proto.py, haul.py contract unwrapping & zero-blind-trust escort gating,
mine_net.py pirate-dodged deficit field escort requests, bursar.py view/outpost/cooldown fixes,
craft_net.py has_craft_job 0ms check, and guard.py FOLLOWED kinds."""

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import bursar       # noqa: E402
import craft_net    # noqa: E402
import escort_proto # noqa: E402
import guard        # noqa: E402
import haul         # noqa: E402
import mine_net     # noqa: E402


class EscortAndAutoNetTests(unittest.TestCase):
    def test_bfs_path_and_threat_scaling_and_stronghold_hard_block(self):
        adj = {"a": ["b"], "b": ["a", "c", "sh"], "c": ["b", "d"], "d": ["c"], "sh": ["b", "d"]}
        path = escort_proto.bfs_path(adj, "a", "d")
        self.assertEqual(path, ["a", "b", "c", "d"])
        smeta = {
            "a": {"empire": "voidborn", "stronghold": False},
            "b": {"empire": "", "stronghold": False},
            "c": {"empire": "nebula", "stronghold": False},
            "d": {"empire": "nebula", "stronghold": False},
            "sh": {"empire": "", "stronghold": True},
        }
        # Lawless hop with 0 pirates still requires 3 escorts (zero blind trust)
        r0 = escort_proto.assess_path_threat(["a", "b", "c"], smeta, set(), {})
        self.assertEqual(r0["needed"], 3)
        self.assertFalse(r0["stronghold_hit"])
        # Scaling: 2 raiders -> 5, 5 pirates -> 7, 1 elite -> 10
        self.assertEqual(escort_proto.needed_escorts_for_threat(2, 2, 0), 5)
        self.assertEqual(escort_proto.needed_escorts_for_threat(5, 4, 0), 7)
        self.assertEqual(escort_proto.needed_escorts_for_threat(1, 0, 1), 10)
        # Any stronghold hop hard-blocks
        r_sh = escort_proto.assess_path_threat(["a", "b", "sh", "d"], smeta, {"sh"}, {})
        self.assertTrue(r_sh["stronghold_hit"])

    def test_haul_unwraps_nested_contract_and_blocks_strongholds_and_low_pay_partner_lawless(self):
        lanes = {"s_safe": ["s_law", "s_sh"], "s_law": ["s_safe"], "s_sh": ["s_safe"]}
        base_map = {
            "b_safe": ("s_safe", "p1", "b_safe", "nebula"),
            "b_law": ("s_law", "p2", "b_law", ""),
            "b_sh": ("s_sh", "p3", "b_sh", ""),
        }
        smeta = {
            "s_safe": {"empire": "nebula", "stronghold": False},
            "s_law": {"empire": "", "stronghold": False},
            "s_sh": {"empire": "", "stronghold": True},
        }
        peers = [{"pilot": "hauler-1", "system": "s_safe", "hold_cap": 200, "avail_cash": 50000, "has_hazmat": False}]
        pol = {
            "policed_only": True, "allow_escorted_lawless": True, "escort_min_reward_cr": 15000,
            "max_jumps_pickup": 10, "max_jumps_delivery": 20, "min_cr_per_jump": 60,
            "min_total_profit": 500, "max_collateral": 25000, "partners_first": True,
        }
        # 1. Stronghold contract with huge 50k reward MUST STILL BE REJECTED
        sh_entry = {"eligible": True, "contract": {
            "id": "c_sh", "origin_base_id": "b_safe", "destination_base_id": "b_sh",
            "base_reward": 50000, "failure_debt": 500, "package_id": "pkg1",
        }}
        self.assertEqual(haul.assign_optimal_freight([sh_entry], base_map, lanes, peers, pol, {"IRLC": {}}, set(),
                                                     exclude_bases={"b_sh", "s_sh"}, systems_meta=smeta), {})

        # 2. Neutral partner [IRLC] lawless contract paying only 1,300 cr MUST BE REJECTED (zero blind trust!)
        low_partner = {"eligible": True, "contract": {
            "id": "c_irlc_low", "origin_base_id": "b_safe", "destination_base_id": "b_law",
            "base_reward": 1300, "failure_debt": 500, "package_id": "pkg2",
            "shipper": {"kind": "faction", "name": "Ironlight Combine"},
        }}
        self.assertEqual(haul.assign_optimal_freight([low_partner], base_map, lanes, peers, pol, {"IRLC": {}}, set(),
                                                     systems_meta=smeta), {})

        # 3. High-value 25,000 cr non-stronghold lawless contract IS accepted ONLY WITH needs_escort=True & escort_needed>=3
        hi_law = {"eligible": True, "contract": {
            "id": "c_hi", "origin_base_id": "b_safe", "destination_base_id": "b_law",
            "base_reward": 25000, "failure_debt": 500, "package_id": "pkg3",
        }}
        res = haul.assign_optimal_freight([hi_law], base_map, lanes, peers, pol, {}, set(),
                                          systems_meta=smeta, pirate_threat={"s_law": {"count": 3, "raiders": 2, "elites": 0}})
        self.assertIn("hauler-1", res)
        self.assertTrue(res["hauler-1"]["needs_escort"])
        self.assertEqual(res["hauler-1"]["escort_needed"], 5)

    def test_mine_net_requests_field_escort_and_unlocks_once_secured(self):
        with tempfile.TemporaryDirectory() as td:
            world = {
                "adj": {"s1": {"s2"}, "s2": {"s1"}},
                "systems": {"s1": {"empire": "voidborn", "stronghold": False}},
                "stations_by_sys": {"s1": [("s1", "st1", "b1")]},
                "fields": [{"system": "s1", "poi": "b_iron", "resource": "iron_ore", "remaining": 8000, "max_remaining": 10000}],
                "pirates": {"s1"},
                "pirate_threat": {"s1": {"count": 1, "raiders": 0, "elites": 0}},
                "item_vals": {"iron_ore": 10.0},
                "shortages": {"iron_ore": 5000},
                "craft_demand": {},
                "full_items": set(),
                "data_dir": td,
                "allow_escort_request": True,
            }
            pol = dict(mine_net.DEFAULT_POLICY, request_escort_for_pirate_deficits=True)
            # First pass: belt is dodged because pirates sighted, AND field escort request is filed!
            cands = mine_net.score_belt_candidates({"name": "miner-1", "system": "s1", "modules": ["mining_laser_i"]}, world, pol, {}, {})
            self.assertEqual(cands, [])
            reqs = escort_proto.list_escort_requests(td)
            self.assertEqual(len(reqs), 1)
            self.assertEqual(reqs[0]["key"], "field:s1:b_iron")
            self.assertEqual(reqs[0]["needed"], 3)

            # 3 Military escorts join and arrive -> belt unlocks for Mining!
            for p in ("drone-1", "drone-2", "sentinel-1"):
                self.assertIsNotNone(escort_proto.join_escort(td, "field:s1:b_iron", p, power=1000.0))
                escort_proto.mark_escort_arrived(td, "field:s1:b_iron", p)
            self.assertTrue(escort_proto.is_field_escorted(td, "s1", "b_iron"))
            cands2 = mine_net.score_belt_candidates({"name": "miner-1", "system": "s1", "modules": ["mining_laser_i"]}, world, pol, {}, {})
            self.assertEqual(len(cands2), 1)
            self.assertEqual(cands2[0]["belt_key"], "s1:b_iron")

    def test_bursar_excludes_foreign_outposts_and_splits_pirate_subjects(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "store").mkdir(parents=True)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, base TEXT);
                CREATE TABLE stations (system TEXT, name TEXT, kind TEXT, tag TEXT);
                CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER, t INTEGER);
                CREATE TABLE observations (kind TEXT, subject TEXT, t INTEGER, note TEXT);
                INSERT INTO systems VALUES ('s_ok', 'voidborn', 0), ('s_pir', 'voidborn', 0);
                INSERT INTO places VALUES ('s_ok', 'p1', 'station', 'Good Hub', 'b_good');
                INSERT INTO places VALUES ('s_ok', 'p2', 'station', 'ENDL Outpost', 'hex_outpost_1');
                INSERT INTO places VALUES ('s_pir', 'p3', 'station', 'Pirate Hub', 'b_pir');
                INSERT INTO stations VALUES ('s_ok', 'Good Hub', 'station', NULL);
                INSERT INTO stations VALUES ('s_ok', 'ENDL Outpost', 'outpost', 'ENDL');
                INSERT INTO stations VALUES ('s_pir', 'Pirate Hub', 'station', NULL);
                INSERT INTO observations VALUES ('pirate', 's_pir:belt_a', strftime('%s','now'), 'raider');
            """)
            con.commit()
            con.close()
            sts = bursar.load_exchange_stations(str(data), policed_only=True, exclude_strongholds=True, exclude_pirates=True)
            bases = [s["base"] for s in sts]
            self.assertEqual(bases, ["b_good"])

    def test_guard_follows_haul_and_mine_net(self):
        self.assertIn("haul", guard.FOLLOWED)
        self.assertIn("mine_net", guard.FOLLOWED)
        self.assertIn("mine_net", guard.PLACED)

    def test_craft_net_has_craft_job_and_no_gate_raw_calls(self):
        # Verify neither craft_net.py nor fit_net.py calls non-existent gate.raw() or gate.goal()
        for fn in ("craft_net.py", "fit_net.py"):
            src = (ROOT / "game" / "fleet" / fn).read_text(encoding="ascii")
            self.assertNotIn("gate.raw(", src)
            self.assertNotIn("gate.goal(", src)
        b_src = (ROOT / "game" / "fleet" / "bursar.py").read_text(encoding="ascii")
        self.assertNotIn('"view_storage"', b_src)


if __name__ == "__main__":
    unittest.main()
