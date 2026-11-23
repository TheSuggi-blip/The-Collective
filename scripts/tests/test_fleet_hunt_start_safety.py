"""A hunt never starts a fight run for a ship still in a battle or under 60% hull (two ships lost, 2026-11-23).

Two newborn hunters fell from 50 and 34 percent hull to 3 and 10 percent over five
and three hunt runs of about two minutes each (runs.jsonl, 06:52 to 07:10 UTC): each
run set the combat mode `external`, which ended the engine's flight from the fight
the run before had left, then failed to fly to its place and ended. hunt.py now
flees a battle it finds at the start before it sets `external`, and a ship under
60 percent hull goes straight to its station for repair instead of to the place.
"""

from pathlib import Path
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


class HuntStartSafetyTests(unittest.TestCase):
    def setUp(self):
        self.text = (FLEET / "hunt.py").read_text(encoding="ascii")

    def test_a_battle_at_the_start_is_fled_before_the_mode_external(self):
        flee = self.text.find("in a battle at the start: fleeing before anything else")
        external = self.text.find("if not combat_mode('external'):")
        self.assertGreater(flee, 0)
        self.assertGreater(external, flee)

    def test_a_ship_still_fighting_after_its_flight_does_not_hunt(self):
        self.assertIn("sys.exit('still in a battle after 5 minutes of flight: no hunt (combat mode left at flee)')", self.text)

    def test_a_ship_under_60_percent_goes_to_repair_not_to_the_place(self):
        self.assertIn("REPAIR_FIRST = START_HULL[0] < START_HULL[1] * 0.6", self.text)
        self.assertIn("if not SHORT and not REPAIR_FIRST and goal('navigate-to-system'", self.text)


if __name__ == "__main__":
    unittest.main()
