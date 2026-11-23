#!/usr/bin/env python3
"""Unit tests for smart mission reach guard (Rules F34, F35) and empty-tour early abort."""

import ast
import sys
import unittest
from pathlib import Path

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))

import dispatch   # noqa: E402


def load_route_run_fn(name):
    src = (FLEET / "route_run.py").read_text(encoding="ascii")
    tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    ns = {}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "route_run.py", "exec"), ns)
    return ns[name]

LANES = {
    "nexus_prime": ["n1"], "n1": ["nexus_prime", "n2"], "n2": ["n1", "n3"],
    "n3": ["n2", "n4"], "n4": ["n3", "n5"], "n5": ["n4", "n6"],
    "n6": ["n5", "n7"], "n7": ["n6", "sol"], "sol": ["n7", "sirius"], "sirius": ["sol"],
    "haven": ["n7"],
}
EMPIRES = {
    "nexus_prime": "voidborn", "n1": "voidborn", "sol": "solarian",
    "sirius": "solarian", "haven": "nebula", "n7": "",
}

SOL_ONCE = {"id": "mission-form-ta-1-confederacy", "kind": "circuit", "once": True,
            "stops": [{"at": "sol:earth_orbit:sol_central", "accept": ["form_ta_1"]}]}
VB_ONCE = {"id": "voidborn-signal-protocol", "kind": "circuit", "once": True,
           "stops": [{"at": "nexus_prime:core:central_nexus", "accept": ["signal_protocol"]}]}
FIT_ONCE = {"id": "fit-mining-laser-iii-lhs-1140", "kind": "circuit", "once": True,
            "stops": [{"at": "sol:station:yard", "fit": [{"module": "mining_laser_iii"}]}]}
STANDING_MINE = {"id": "gather-sol-belt", "kind": "mine", "place": "sol:belt"}


def make_pilot(empire, system):
    return {"name": "miner-1", "role": "miner", "credits": 30000, "docked": True,
            "modules": [], "skills": {}, "goods": 0, "empire": empire, "system": system}


class SmartMissionReachTests(unittest.TestCase):
    def setUp(self):
        self.saved_lanes = dispatch.LANES_CACHE.get("lanes")
        self.saved_emp = dispatch.LANES_CACHE.get("empires")
        dispatch.LANES_CACHE["lanes"] = LANES
        dispatch.LANES_CACHE["empires"] = EMPIRES
        dispatch.DIST_CACHE.clear()
        self.addCleanup(self.restore)

    def restore(self):
        dispatch.LANES_CACHE["lanes"] = self.saved_lanes
        dispatch.LANES_CACHE["empires"] = self.saved_emp
        dispatch.DIST_CACHE.clear()

    def test_voidborn_at_home_refuses_far_foreign_once_mission(self):
        why = dispatch.mission_reach_reason(make_pilot("voidborn", "nexus_prime"), SOL_ONCE["id"], SOL_ONCE)
        self.assertIsNotNone(why)
        self.assertIn("foreign once-mission", why)
        # Integrated in why_not()
        w2, _ = dispatch.why_not(make_pilot("voidborn", "nexus_prime"), SOL_ONCE["id"], SOL_ONCE, {"rows": [], "now": 0})
        self.assertIn("foreign once-mission", str(w2))

    def test_own_empire_mastery_mission_always_open_even_when_far(self):
        # Voidborn currently in Sol can fly back home for Voidborn Mastery chain!
        self.assertIsNone(dispatch.mission_reach_reason(make_pilot("voidborn", "sol"), VB_ONCE["id"], VB_ONCE))
        # Solarian at Sol flies Solarian chain cleanly!
        self.assertIsNone(dispatch.mission_reach_reason(make_pilot("solarian", "sol"), SOL_ONCE["id"], SOL_ONCE))

    def test_foreign_once_mission_allowed_when_already_local_or_far_ok(self):
        # Voidborn already physically in Sirius (1 jump from Sol) -> local allowed
        self.assertIsNone(dispatch.mission_reach_reason(make_pilot("voidborn", "sirius"), SOL_ONCE["id"], SOL_ONCE))
        # Explicit far_ok opt-in -> allowed even from Nexus Prime
        self.assertIsNone(dispatch.mission_reach_reason(make_pilot("voidborn", "nexus_prime"), SOL_ONCE["id"], dict(SOL_ONCE, far_ok=True)))

    def test_fit_and_standing_routes_never_blocked_by_mission_guard(self):
        self.assertIsNone(dispatch.mission_reach_reason(make_pilot("voidborn", "nexus_prime"), FIT_ONCE["id"], FIT_ONCE))
        self.assertIsNone(dispatch.mission_reach_reason(make_pilot("voidborn", "nexus_prime"), STANDING_MINE["id"], STANDING_MINE))

    def test_early_aborted_unoffered_tour_counts_refused_and_closes_ungated_once(self):
        aborted = {
            "route": "mission-federation-trade-route-prospectus-grand", "pilot": "miner-104",
            "started": "2026-11-23T02:20:00Z", "minutes": 1.0, "stops": 1, "of": 9,
            "notes": ["federation_trade_route_prospectus not offered", dispatch.EARLY_UNOFFERED],
        }
        self.assertTrue(dispatch.refused(aborted))
        # Ungated once mission -> immediately marked done_once so ship never retries empty tour
        self.assertTrue(dispatch.done_once({"once": True}, [aborted]))
        # Gated once mission (requires.booked) -> NOT permanently done; rests cleanly via waits_once
        gated = {"once": True, "requires": {"booked": "Prior Mission"}, "retry_minutes": 60}
        self.assertFalse(dispatch.done_once(gated, [aborted]))
        self.assertTrue(dispatch.waits_once(gated, [aborted], 1795400000))

    def test_pure_visit_tail_detects_empty_tour_vs_work_stops(self):
        pure_visit_tail = load_route_run_fn("pure_visit_tail")
        self.assertTrue(pure_visit_tail([{"at": "a:b:c", "redock": True}, {"at": "d:e:f", "redock": True}]))
        self.assertFalse(pure_visit_tail([{"at": "a:b:c", "sell": ["iron_ore"]}]))
        self.assertFalse(pure_visit_tail([{"at": "a:b:c", "accept": ["other"]}]))
        self.assertFalse(pure_visit_tail([]))


    def test_refused_skill_gated_once_route_obeys_waits_once_cooldown(self):
        aborted = {
            "route": "mission-skill-gated-example", "pilot": "miner-1",
            "started": "2026-11-23T02:20:00Z", "minutes": 1.0, "stops": 1, "of": 3,
            "notes": ["skill_mission not offered", dispatch.EARLY_UNOFFERED],
        }
        skill_route = {"once": True, "requires": {"skills": {"mining": 5}}, "retry_minutes": 60}
        self.assertFalse(dispatch.done_once(skill_route, [aborted]))
        # 2026-11-23T02:21:00Z == 1795395660 -> 10 min later still waiting, 65 min later free
        import calendar, time
        ended = calendar.timegm(time.strptime("2026-11-23T02:20:00Z", "%Y-%m-%dT%H:%M:%SZ")) + 60
        self.assertTrue(dispatch.waits_once(skill_route, [aborted], ended + 10 * 60))
        self.assertFalse(dispatch.waits_once(skill_route, [aborted], ended + 65 * 60))


    def test_symmetric_5_empire_prefix_guard_and_workclass(self):
        import workclass
        for emp in ("voidborn", "solarian", "nebula", "crimson", "outerrim"):
            rid = emp + "-first-steps"
            self.assertEqual(workclass.work_class({"kind": "circuit", "once": True}, rid), "once")
        why = dispatch.newborn_reason(make_pilot("voidborn", "sol"), "solarian-first-steps", SOL_ONCE)
        self.assertIsNotNone(why)
        self.assertIn("Solarian empire mission", why)
        self.assertIsNone(dispatch.newborn_reason(make_pilot("solarian", "sol"), "solarian-first-steps", SOL_ONCE))
        self.assertIsNotNone(dispatch.newborn_reason(make_pilot("solarian", "nexus_prime"), "voidborn-first-steps", VB_ONCE))


    def test_fill_verdict_scout_docked_watch_exception_F8(self):
        import fill
        seen_docked = {"list_age": 10, "crews": {"scout": {"waiting": [{"name": "scout-1", "docked": "central_nexus"}]}}}
        got_docked = {"role": "scout", "waiting": ["scout-1"], "paying": [], "tests": [], "park": []}
        ok, line = fill.verdict(seen_docked, got_docked)
        self.assertTrue(ok)
        self.assertIn("docked-watch exception", line)
        # Adrift scout (not docked) MUST still HALT
        seen_adrift = {"list_age": 10, "crews": {"scout": {"waiting": [{"name": "scout-1", "docked": ""}]}}}
        ok2, _ = fill.verdict(seen_adrift, got_docked)
        self.assertFalse(ok2)
        # Docked miner MUST still HALT (exception is scouts only)
        seen_miner = {"list_age": 10, "crews": {"miner": {"waiting": [{"name": "miner-1", "docked": "central_nexus"}]}}}
        got_miner = {"role": "miner", "waiting": ["miner-1"], "paying": [], "tests": [], "park": []}
        ok3, _ = fill.verdict(seen_miner, got_miner)
        self.assertFalse(ok3)


if __name__ == "__main__":
    unittest.main()
