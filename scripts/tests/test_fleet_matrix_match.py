"""Unit tests for matrix_match.py, owned_fuel_depots in fuelplan.py, and zero-idle auto-relax."""
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))

import census_net
import fuelplan
import matrix_match


class TestHungarianMatcher(unittest.TestCase):
    def test_beats_greedy_on_crossed_pair(self):
        # Pilot A: R1=1J (1000), R2=2J (2000)
        # Pilot B: R1=0J (0),    R2=10J (10000)
        # Greedy A->R1, B->R2 = 11000. Optimal B->R1, A->R2 = 2000.
        cost = [
            [1000.0, 2000.0],
            [0.0, 10000.0],
        ]
        pairs = matrix_match.min_cost_assignment(cost)
        self.assertEqual(pairs, [(0, 1), (1, 0)])

    def test_rectangular_more_rows_than_cols(self):
        cost = [
            [5000.0, 8000.0],
            [1000.0, 9000.0],
            [9000.0, 500.0],
        ]
        pairs = matrix_match.min_cost_assignment(cost)
        self.assertEqual(pairs, [(1, 0), (2, 1)])

    def test_forbidden_edges_omitted(self):
        F = float(matrix_match.FORBIDDEN)
        cost = [
            [F, 100.0],
            [F, F],
        ]
        pairs = matrix_match.min_cost_assignment(cost)
        self.assertEqual(pairs, [(0, 1)])


class TestMissionBoardGate(unittest.TestCase):
    def test_blocks_unoffered_and_allows_offered_or_stale(self):
        now = time.time()
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            mdir = d / "missions"
            mdir.mkdir(parents=True)
            (mdir / "frontier_station.json").write_text(json.dumps({
                "base": "frontier_station",
                "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 600)),
                "missions": [
                    {"mission_id": "who_buys_old_charts", "template_id": "who_buys_old_charts", "title": "Who Buys Old Charts"},
                ],
            }), encoding="utf-8")

            r_offered = {
                "id": "mission-charts",
                "kind": "circuit",
                "stops": [{"at": "altais:mobile_capital:frontier_station", "accept": ["who_buys_old_charts"]}],
            }
            r_missing = {
                "id": "mission-proposal",
                "kind": "circuit",
                "stops": [{"at": "altais:mobile_capital:frontier_station", "accept": ["the_proposal"]}],
            }
            r_no_board = {
                "id": "mission-other",
                "kind": "circuit",
                "stops": [{"at": "sol:earth:unknown_base", "accept": ["the_proposal"]}],
            }
            self.assertIsNone(matrix_match.mission_offered_on_board(d, r_offered, now))
            why = matrix_match.mission_offered_on_board(d, r_missing, now)
            self.assertIsNotNone(why)
            self.assertIn("not offered", why)
            # Fail-open when board missing
            self.assertIsNone(matrix_match.mission_offered_on_board(d, r_no_board, now))
            # Fail-open when board stale (> 6h)
            self.assertIsNone(matrix_match.mission_offered_on_board(d, r_missing, now + 25000.0))


class TestBatchAssignment(unittest.TestCase):
    def test_closer_pilot_wins_scarce_route_over_alphabetical_first(self):
        routes = {
            "mission-a": {"id": "mission-a", "kind": "circuit", "max_ships": 1, "stops": [{"at": "sys_a:p:b"}]},
            "mission-b": {"id": "mission-b", "kind": "circuit", "max_ships": 1, "stops": [{"at": "sys_b:p:b"}]},
            "mine-net": {"id": "mine-net", "kind": "mine_net", "max_ships": 100},
        }
        plan = {"roles": {"miner": ["mission-a", "mission-b", "mine-net"]}, "pilots": {}}
        state = {"orders": {}, "_order_counts": {}}
        p_alpha = {"name": "EUV Alpha", "role": "miner", "system": "sys_b", "docked": False}
        p_zeta = {"name": "EUV Zeta", "role": "miner", "system": "sys_a", "docked": True}
        free = [({"name": "EUV Alpha"}, p_alpha), ({"name": "EUV Zeta"}, p_zeta)]

        hops_table = {
            ("sys_b", "mission-a"): 10,
            ("sys_b", "mission-b"): 1,
            ("sys_a", "mission-a"): 0,
            ("sys_a", "mission-b"): 10,
        }
        def why_not(_p, _rid, _rt, _st):
            return None, None
        def hops_fn(p, rt):
            return hops_table.get((p["system"], rt["id"]), 5)
        def pick_fn(_p, _pl, _rts, _st):
            return routes["mine-net"], None

        pre, ordered = matrix_match.assign_batch_pilots(free, plan, routes, state, why_not, hops_fn, pick_fn)
        self.assertEqual(pre["EUV Zeta"][0]["id"], "mission-a")
        self.assertEqual(pre["EUV Alpha"][0]["id"], "mission-b")
        self.assertEqual(len(ordered), 2)


class TestOwnedFuelDepots(unittest.TestCase):
    def test_owned_fuel_depots_and_preference(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "empire").mkdir(parents=True)
            (d / "scouting").mkdir(parents=True)
            (d / "empire" / "empire.json").write_text(json.dumps({
                "bases": [
                    {"base": "b_atria", "system": "atria", "poi": "poi_atria", "kind": "outpost"},
                    {"base": "b_dry", "system": "dry_sys", "poi": "poi_dry", "kind": "outpost"},
                    {"base": "b_resort", "system": "ridgecrest", "poi": "poi_rc", "kind": "station"},
                ],
                "facilities": [
                    {"base": "b_atria", "type": "faction_fuel_bunker", "status": "active"},
                    {"base": "b_dry", "type": "faction_fuel_bunker", "status": "active"},
                    {"base": "b_resort", "type": "grazer_grill", "status": "active"},
                ],
                "faction_storage": [
                    {"base": "b_atria", "item": "fuel", "units": 45000},
                    {"base": "b_dry", "item": "fuel", "units": 50},
                ],
            }), encoding="utf-8")
            (d / "scouting" / "npc1.json").write_text(json.dumps({
                "pois": {"p_npc1": {"poi": {"id": "p_npc1"}, "base": {"id": "npc_base_1"}, "services": ["refuel"]}}
            }), encoding="utf-8")

            owned = fuelplan.owned_fuel_depots(d, min_fuel=200)
            self.assertEqual(owned, {"atria": ("poi_atria", "b_atria")})

            all_st = fuelplan.fuel_stations(d)
            self.assertIn("atria", all_st)
            self.assertIn("npc1", all_st)
            self.assertNotIn("dry_sys", all_st)
            self.assertNotIn("ridgecrest", all_st)

            lanes = {
                "here": ["npc1", "mid"],
                "npc1": ["here"],
                "mid": ["here", "atria"],
                "atria": ["mid"],
            }
            # Owned depot at 2J wins over NPC at 1J when preferred (+1 hop free-fuel preference)
            res = fuelplan.nearest_fuel(lanes, "here", all_st, prefer_bases={"b_atria"})
            self.assertEqual(res[1], "atria")
            # At 0J local NPC station, never jump away just to use an owned depot 1J away
            lanes2 = {"npc1": ["atria"], "atria": ["npc1"]}
            res0 = fuelplan.nearest_fuel(lanes2, "npc1", all_st, prefer_bases={"b_atria"})
            self.assertEqual(res0[1], "npc1")


if __name__ == "__main__":
    unittest.main()
