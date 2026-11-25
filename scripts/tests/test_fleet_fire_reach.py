"""game/fleet/handover.py fire_reach: the distance a hunter must close to so that every weapon able to fire reaches
(errors.log ENT-198: an empty Missile Launcher I, reach 6, kept autocannon hulls at 6 where their guns, reach 2, never
fired). No engine, no network."""

import sys
import unittest
from pathlib import Path

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
import handover                                   # noqa: E402  the module under test

ITEMS = [
    {"id": "autocannon_i", "reach": 2, "ammo_type": "autocannon", "damage": 10},
    {"id": "missile_launcher_i", "reach": 6, "ammo_type": "missile", "damage": 20},
    {"id": "pulse_laser_i", "reach": 3, "damage": 10},
    {"id": "shield_booster_ii", "category": "defense"},
    {"id": "standard_rounds_box", "category": "ammo", "effect": {"subtype": "autocannon"}},
    {"id": "light_missiles", "category": "ammo", "effect": {"subtype": "missile"}},
]


def mod(type_id, ammo=None):
    m = {"type_id": type_id, "module_id": type_id + "-1"}
    if ammo is not None:
        m.update({"magazine_size": 10, "current_ammo": ammo})
    return m


class FireReach(unittest.TestCase):
    def test_empty_launcher_does_not_hold_the_guns_at_six(self):
        mods = [mod("autocannon_i", 5), mod("autocannon_i", 5), mod("missile_launcher_i", 0)]
        self.assertEqual(handover.fire_reach(mods, ITEMS, {}), 2)

    def test_launcher_with_missiles_in_the_hold_still_closes_to_the_guns(self):
        mods = [mod("autocannon_i", 5), mod("missile_launcher_i", 0)]
        self.assertEqual(handover.fire_reach(mods, ITEMS, {"light_missiles": 4}), 2)

    def test_guns_without_rounds_leave_the_launcher(self):
        mods = [mod("autocannon_i", 0), mod("missile_launcher_i", 3)]
        self.assertEqual(handover.fire_reach(mods, ITEMS, {}), 6)

    def test_rounds_in_the_hold_count(self):
        mods = [mod("autocannon_i", 0), mod("missile_launcher_i", 0)]
        self.assertEqual(handover.fire_reach(mods, ITEMS, {"standard_rounds_box": 2}), 2)

    def test_laser_needs_no_ammo(self):
        mods = [mod("pulse_laser_i"), mod("shield_booster_ii")]
        self.assertEqual(handover.fire_reach(mods, ITEMS, {}), 3)

    def test_nothing_can_fire(self):
        self.assertIsNone(handover.fire_reach([mod("missile_launcher_i", 0)], ITEMS, {}))
        self.assertIsNone(handover.fire_reach([], ITEMS, {}))

    def test_unknown_catalog_keeps_the_games_own_reach(self):
        self.assertIsNone(handover.fire_reach([mod("autocannon_i", 5)], [], {}))


if __name__ == "__main__":
    unittest.main()
