"""Pilots born in another empire (the Plan-500 wave of 2026-11-22, queue.log ENT-234): the dispatcher never sends
them on a Voidborn empire mission, nor on a route whose first place lies more than FOREIGN_REACH jumps from where
they stand, unless the route says `far_ok`. A Voidborn pilot is judged as before. No engine, no network."""

from pathlib import Path
import sys
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
import dispatch          # noqa: E402

LANES = {"home": ["h1"], "h1": ["home", "h2"], "h2": ["h1", "h3"], "h3": ["h2", "h4"], "h4": ["h3", "h5"],
         "h5": ["h4", "h6"], "h6": ["h5", "h7"], "h7": ["h6", "sol"], "sol": ["h7", "sirius"], "sirius": ["sol"]}
NEAR = {"id": "hunt-sirius", "kind": "hunt", "place": "sirius:belt"}
FAR = {"id": "train-jumps-trader", "kind": "circuit", "stops": [{"at": "home:core:central_nexus"}]}


def pilot(empire, system):
    return {"name": "x-1", "role": "trader", "credits": 50000, "docked": True, "modules": [], "skills": {}, "goods": 0,
            "empire": empire, "system": system}


class NewbornReachTests(unittest.TestCase):
    def setUp(self):
        self.saved = dispatch.LANES_CACHE.get("lanes")
        dispatch.LANES_CACHE["lanes"] = LANES
        self.addCleanup(dispatch.LANES_CACHE.__setitem__, "lanes", self.saved)

    def test_a_voidborn_mission_is_closed_to_a_pilot_of_another_empire(self):
        why = dispatch.newborn_reason(pilot("solarian", "sol"), "voidborn-signal-protocol", FAR)
        self.assertIn("Voidborn", why)
        self.assertIsNone(dispatch.newborn_reason(pilot("voidborn", "home"), "voidborn-signal-protocol", FAR))

    def test_a_far_route_is_closed_and_a_near_one_open(self):
        why = dispatch.newborn_reason(pilot("solarian", "sol"), FAR["id"], FAR)
        self.assertIn("jumps", why)
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", "sol"), NEAR["id"], NEAR))
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", "sol"), FAR["id"], dict(FAR, far_ok=True)))

    def test_a_voidborn_pilot_far_from_home_is_judged_as_before(self):
        self.assertIsNone(dispatch.newborn_reason(pilot("voidborn", "sol"), FAR["id"], FAR))
        self.assertIsNone(dispatch.newborn_reason(pilot(None, "sol"), FAR["id"], FAR))

    def test_an_unknown_place_closes_nothing(self):
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", None), FAR["id"], FAR))
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", "sol"), "x", {"id": "x", "kind": "circuit", "stops": [{"at": "nowhere:p:b"}]}))

    def test_why_not_uses_it(self):
        reason, _ = dispatch.why_not(pilot("nebula", "sol"), "voidborn-selling", dict(FAR, id="voidborn-selling"), {"rows": [], "now": 0})
        self.assertIn("Voidborn", str(reason))

    def test_pilot_of_carries_empire_and_system(self):
        row = dispatch.pilot_of({"name": "x-1", "empire": "nebula", "system": "haven", "credits": 1}, {}, "/nonexistent", set())
        self.assertEqual((row["empire"], row["system"]), ("nebula", "haven"))


if __name__ == "__main__":
    unittest.main()
