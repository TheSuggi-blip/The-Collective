import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import passenger_net as pn


class PassengerNetTests(unittest.TestCase):
    def test_berth_math_for_futures_with_vip_and_business_cabins(self):
        b = pn.ship_berths("futures", ["first_class_passenger_suite", "business_passenger_cabin"])
        self.assertEqual(b, {"economy": 0, "business": 7, "first": 3})
        self.assertEqual(pn.total_berths(b), 10)
        self.assertEqual(pn.total_berths(pn.ship_berths("cobble", [])), 0)

    def test_seat_allocation_prioritizes_first_class_and_downgrades_overflow(self):
        berths = {"first": 1, "business": 1, "economy": 0}
        pax = [
            {"name": "Eco1", "class": "economy", "estimated_fare": 1000},
            {"name": "First1", "class": "first", "estimated_fare": 11000},
            {"name": "Eco2", "class": "economy", "estimated_fare": 900},
        ]
        seated, fare, rem = pn.simulate_seat_allocation(pax, berths)
        self.assertEqual([p["name"] for p in seated], ["First1", "Eco1"])
        self.assertEqual(fare, 12000)
        self.assertEqual(rem, {"first": 0, "business": 0, "economy": 0})

    def test_ridgecrest_inbound_and_vip_bonus_rank_first(self):
        graph = {
            "adj": {"sol": ["s1", "s2"], "s1": ["sol", "ridgecrest"], "ridgecrest": ["s1"], "s2": ["sol", "other"], "other": ["s2"]},
            "base_to_sys": {"rc_base": "ridgecrest", "other_base": "other"},
            "sys_to_base": {"ridgecrest": "rc_base", "other": "other_base"},
            "strongholds": set(),
            "refuel_ready": {"rc_base"},
        }
        pol = dict(pn.DEFAULT_POLICY, home_base="rc_base", home_system="ridgecrest")
        board = {
            "waiting": [
                {"name": "P1", "class": "first", "destination": "rc_base", "destination_system": "ridgecrest", "estimated_fare": 9000},
                {"name": "P2", "class": "first", "destination": "other_base", "destination_system": "other", "estimated_fare": 9000},
            ]
        }
        berths = pn.ship_berths("futures", ["first_class_passenger_suite", "business_passenger_cabin"])
        cands = pn.score_station_board("sol_base", "sol", board, berths, graph, pol)
        self.assertEqual(len(cands), 2)
        self.assertEqual(cands[0]["dest_base"], "rc_base")
        self.assertGreater(cands[0]["score"], cands[1]["score"])

    def test_reposition_prefers_ridgecrest_high_value_board(self):
        graph = {
            "adj": {"sol": ["s1", "s2"], "s1": ["sol", "ridgecrest"], "ridgecrest": ["s1"], "s2": ["sol", "haven"], "haven": ["s2"]},
            "base_to_sys": {"rc_base": "ridgecrest", "hav_base": "haven", "sol_base": "sol"},
            "sys_to_base": {},
            "strongholds": set(),
            "refuel_ready": {"rc_base"},
        }
        pol = dict(pn.DEFAULT_POLICY, home_base="rc_base", home_system="ridgecrest")
        boards = {
            "rc_base": {"system": "ridgecrest", "waiting": [{"class": "first", "destination": "sol_base", "destination_system": "sol", "estimated_fare": 11000}]},
            "hav_base": {"system": "haven", "waiting": [{"class": "economy", "destination": "sol_base", "destination_system": "sol", "estimated_fare": 1800}]},
        }
        berths = pn.ship_berths("futures", ["first_class_passenger_suite"])
        rep = pn.choose_reposition_hub("sol", boards, berths, graph, pol)
        self.assertIsNotNone(rep)
        self.assertEqual(rep["base"], "rc_base")

    def test_has_passenger_work_blocks_unfitted_cobble_and_allows_futures(self):
        pol_p = ROOT / "game" / "passenger-policy.json"
        self.assertFalse(pn.has_passenger_work("LSV Albatross", {"class": "Cobble", "modules": []}, policy_path=pol_p))
        self.assertTrue(pn.has_passenger_work("LSV Albatross", {"class": "Futures", "modules": []}, policy_path=pol_p))



    def test_display_name_dest_system_and_gate_toll_deduction(self):
        graph = {
            "adj": {
                "ridgecrest": ["cervantes"],
                "cervantes": ["ridgecrest", "miaplacidus", "n1"],
                "miaplacidus": ["cervantes"],
                "n1": ["cervantes", "n2"], "n2": ["n1", "n3"], "n3": ["n2", "n4"],
                "n4": ["n3", "n5"], "n5": ["n4", "kochab"],
                "kochab": ["n5", "starfall"], "starfall": ["kochab"],
            },
            "base_to_sys": {
                "rc_base": "ridgecrest",
                "starfall_salvage_station": "starfall",
            },
            "sys_to_base": {"ridgecrest": "rc_base", "starfall": "starfall_salvage_station"},
            "name_to_sys": {"starfall": "starfall", "ridgecrest": "ridgecrest"},
            "strongholds": set(),
            "refuel_ready": {"rc_base"},
            "gates": {("miaplacidus", "kochab"): 200, ("kochab", "miaplacidus"): 200},
        }
        # Live API returns display name ("Starfall") in destination_system!
        board = {
            "waiting": [
                {"destination": "starfall_salvage_station", "destination_system": "Starfall", "class": "business", "estimated_fare": 3200},
            ]
        }
        berths = pn.ship_berths("futures", ["first_class_passenger_suite"])
        pol = dict(pn.DEFAULT_POLICY, home_base="rc_base", use_jumpgates=True, max_gate_toll_cr=500, gate_cr_per_jump=140.0)
        cands = pn.score_station_board("rc_base", "ridgecrest", board, berths, graph, pol, pilot_credits=5000)
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0]["hops"], 4)
        self.assertEqual(cands[0]["toll_cr"], 200)
        self.assertEqual(cands[0]["fare"], 3000)  # 3200 gross - 200 gate toll!

    def test_passenger_net_isolated_mode_imports_cleanly(self):
        """Regression gate (R5/R6): standalone python3 -I -B must not fail on sibling imports."""
        import subprocess
        script = Path(__file__).resolve().parents[2] / "game" / "fleet" / "passenger_net.py"
        self.assertTrue(script.exists(), f"Missing {script}")
        res = subprocess.run(
            [sys.executable, "-I", "-B", str(script), "--help"],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(res.returncode, 0, f"Isolated -I launch failed: rc={res.returncode} stderr={res.stderr}")
        self.assertNotIn("ModuleNotFoundError", res.stderr)



    def test_raw_error_envelope_and_fly_resync_recovers_from_hop_desync(self):
        import json
        class _FakeGate:
            def __init__(self):
                self.calls = []
                self.cur = "gold_run"
                self.first_jump_failed = False

            def q(self, x):
                return x

            def call(self, method, path, payload=None, timeout=30):
                act = (payload or {}).get("action")
                prm = (payload or {}).get("params") or {}
                self.calls.append((act, prm))
                if act == "jump":
                    tgt = prm.get("id")
                    if not self.first_jump_failed and tgt == "market_prime":
                        self.first_jump_failed = True
                        return 200, json.dumps({"error": "Gold Run is not connected to keel"})
                    self.cur = tgt
                    return 200, json.dumps({"structuredContent": {"details": {"system_id": tgt}, "location": {"system_id": tgt}}})
                if act == "get_status":
                    return 200, json.dumps({"structuredContent": {"location": {"system_id": self.cur, "base_id": ""}}})
                if act in ("travel", "dock", "undock", "refuel"):
                    return 200, json.dumps({"structuredContent": {"ok": True}})
                return 200, json.dumps({"structuredContent": {}})

        fg = _FakeGate()
        ok_err, _, _ = pn._raw(fg, "LSV Test", "jump", {"id": "market_prime"})
        self.assertFalse(ok_err)
        fg.first_jump_failed = False
        orig_sleep = pn.time.sleep
        pn.time.sleep = lambda _s: None
        try:
            graph = {
                "adj": {"gold_run": ["market_prime"], "market_prime": ["gold_run", "haven"], "haven": ["market_prime"]},
                "strongholds": set(),
                "refuel_ready": set(),
                "gates": {},
                "base_to_poi": {"grand_exchange_station": "grand_exchange"},
            }
            ok, final_sys, final_base, why = pn._fly_and_dock(
                fg, "LSV Test", "gold_run", "", "haven", "grand_exchange_station", graph, {}, "/tmp/no-data"
            )
        finally:
            pn.time.sleep = orig_sleep
        self.assertTrue(ok, why)
        self.assertEqual(final_sys, "haven")
        self.assertEqual(final_base, "grand_exchange_station")
        self.assertIn(("travel", {"id": "grand_exchange"}), fg.calls)




class TestPassengerPolicyResolution(unittest.TestCase):
    def test_read_policy_relative_path_from_other_cwd(self):
        import os
        old_cwd = os.getcwd()
        try:
            os.chdir("/tmp")
            pol = pn.read_policy("game/passenger-policy.json")
            self.assertGreaterEqual(len(pol.get("scan_stations") or []), 20)
        finally:
            os.chdir(old_cwd)

    def test_choose_reposition_hub_excludes_claimed(self):
        graph = {
            "adj": {"ridgecrest": ["node_beta", "sol"], "node_beta": ["ridgecrest"], "sol": ["ridgecrest"]},
            "base_to_sys": {"rc": "ridgecrest", "nb": "node_beta", "sol_b": "sol"},
            "name_to_sys": {},
            "gates": {},
        }
        boards = {
            "nb": {"system": "node_beta", "waiting": [{"class": "business", "destination": "rc", "destination_system": "ridgecrest", "estimated_fare": 2000}]},
            "sol_b": {"system": "sol", "waiting": [{"class": "business", "destination": "rc", "destination_system": "ridgecrest", "estimated_fare": 1500}]},
        }
        pol = {"home_base": "rc", "home_system": "ridgecrest", "max_hops": 10, "min_fare_per_jump": 100}
        berths = {"economy": 0, "business": 1, "first": 0}
        r1 = pn.choose_reposition_hub("ridgecrest", boards, berths, graph, pol)
        self.assertEqual(r1["base"], "nb")
        r2 = pn.choose_reposition_hub("ridgecrest", boards, berths, graph, pol, claimed_hubs={"nb"})
        self.assertEqual(r2["base"], "sol_b")



if __name__ == "__main__":
    unittest.main()
