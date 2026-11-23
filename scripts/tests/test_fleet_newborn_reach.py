"""Pilots born in another empire (rule F35; standing-corridor integration Suggi 2026-11-23):
1. Native empire missions (`<empire>-*`) remain strictly locked to pilots born in that empire (F35).
2. Far `once` missions (> FOREIGN_REACH jumps) require `far_ok` so pilots stay local for home missions first.
3. Standing non-`once` class work flows automatically by plan priority so newborns never idle when home work ends.
No engine, no network."""

from pathlib import Path
import sys
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
import dispatch          # noqa: E402

LANES = {"home": ["h1"], "h1": ["home", "h2"], "h2": ["h1", "h3"], "h3": ["h2", "h4"], "h4": ["h3", "h5"],
         "h5": ["h4", "h6"], "h6": ["h5", "h7"], "h7": ["h6", "sol"], "sol": ["h7", "sirius"], "sirius": ["sol"]}
NEAR = {"id": "hunt-sirius", "kind": "hunt", "place": "sirius:belt"}
FAR_STANDING = {"id": "train-jumps-trader", "kind": "circuit", "stops": [{"at": "home:core:central_nexus"}]}
FAR_ONCE = {"id": "mission-far-errand", "kind": "circuit", "once": True, "stops": [{"at": "home:core:central_nexus"}]}


def pilot(empire, system):
    return {"name": "x-1", "role": "trader", "credits": 50000, "docked": True, "modules": [], "skills": {}, "goods": 0,
            "empire": empire, "system": system}


class NewbornReachTests(unittest.TestCase):
    def setUp(self):
        self.saved = dispatch.LANES_CACHE.get("lanes")
        dispatch.LANES_CACHE["lanes"] = LANES
        self.addCleanup(dispatch.LANES_CACHE.__setitem__, "lanes", self.saved)

    def test_a_voidborn_mission_is_closed_to_a_pilot_of_another_empire(self):
        why = dispatch.newborn_reason(pilot("solarian", "sol"), "voidborn-signal-protocol", FAR_ONCE)
        self.assertIn("Voidborn", why)
        self.assertIsNone(dispatch.newborn_reason(pilot("voidborn", "home"), "voidborn-signal-protocol", FAR_ONCE))

    def test_a_far_once_mission_is_closed_and_near_or_far_ok_open(self):
        why = dispatch.newborn_reason(pilot("solarian", "sol"), FAR_ONCE["id"], FAR_ONCE)
        self.assertIn("jumps", why)
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", "sol"), NEAR["id"], NEAR))
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", "sol"), FAR_ONCE["id"], dict(FAR_ONCE, far_ok=True)))

    def test_standing_corridor_work_opens_automatically_for_newborns(self):
        self.assertIsNone(dispatch.newborn_reason(pilot("nebula", "sol"), FAR_STANDING["id"], FAR_STANDING))
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", "sol"), FAR_STANDING["id"], FAR_STANDING))

    def test_a_once_mission_in_the_pilot_s_own_empire_is_open_however_far_it_stands(self):
        # 2026-11-23 14:00 UTC: 36 haulers born nebula and outerrim docked at Alpha Centauri (solarian) after its once
        # missions, every mission of their own empire 11 to 20 jumps away closed by the reach fence: they could not go home
        saved = dispatch.LANES_CACHE.get("empires")
        dispatch.LANES_CACHE["empires"] = {"home": "nebula", "sol": "solarian", "sirius": "solarian"}
        self.addCleanup(dispatch.LANES_CACHE.__setitem__, "empires", saved)
        self.assertIsNone(dispatch.newborn_reason(pilot("nebula", "sol"), FAR_ONCE["id"], FAR_ONCE))         # home work, 8 jumps
        self.assertIn("jumps", dispatch.newborn_reason(pilot("solarian", "sol"), FAR_ONCE["id"], FAR_ONCE))  # another empire's: fenced
        self.assertIn("jumps", dispatch.newborn_reason(pilot("outerrim", "sol"), FAR_ONCE["id"], FAR_ONCE))

    def test_a_voidborn_pilot_far_from_home_is_judged_as_before(self):
        self.assertIsNone(dispatch.newborn_reason(pilot("voidborn", "sol"), FAR_ONCE["id"], FAR_ONCE))
        self.assertIsNone(dispatch.newborn_reason(pilot(None, "sol"), FAR_ONCE["id"], FAR_ONCE))

    def test_an_unknown_place_closes_nothing(self):
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", None), FAR_ONCE["id"], FAR_ONCE))
        self.assertIsNone(dispatch.newborn_reason(pilot("solarian", "sol"), "x", {"id": "x", "kind": "circuit", "once": True, "stops": [{"at": "nowhere:p:b"}]}))

    def test_why_not_uses_it(self):
        reason, _ = dispatch.why_not(pilot("nebula", "sol"), "voidborn-selling", dict(FAR_ONCE, id="voidborn-selling"), {"rows": [], "now": 0})
        self.assertIn("Voidborn", str(reason))

    def test_pilot_of_carries_empire_and_system(self):
        row = dispatch.pilot_of({"name": "x-1", "empire": "nebula", "system": "haven", "credits": 1}, {}, "/nonexistent", set())
        self.assertEqual((row["empire"], row["system"]), ("nebula", "haven"))


if __name__ == "__main__":
    unittest.main()
