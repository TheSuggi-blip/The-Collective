"""game/fleet/mobile.py: a stop at a moving station follows the station; every other stop is left as written."""

import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
import mobile  # noqa: E402


def world(folder, stations, census):
    (folder / "station").mkdir(parents=True)
    (folder / "scouting").mkdir(parents=True)
    (folder / "station" / "stations.json").write_text(json.dumps(stations), encoding="ascii")
    for system, pois in census.items():
        doc = {"system": {"id": system, "pois": pois}}
        (folder / "scouting" / ("%s.json" % system)).write_text(json.dumps(doc), encoding="ascii")


CAPITAL = {"name": "Frontier Station", "system": "altais", "mobile": True, "wrecked": False}
FIXED = {"name": "Central Nexus", "system": "nexus_prime", "mobile": False, "wrecked": False}
ALTAIS = [{"id": "altais_star"}, {"id": "mobile_capital", "has_base": True, "base_id": "frontier_station"}]


class LocateTests(unittest.TestCase):
    def test_moved_station_is_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [CAPITAL, FIXED], {"altais": ALTAIS})
            system, poi, line = mobile.locate("frontier", "mobile_capital", "frontier_station", tmp)
            self.assertEqual((system, poi), ("altais", "mobile_capital"))
            self.assertIn("altais:mobile_capital", line)

    def test_station_where_the_route_says_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [CAPITAL], {"altais": ALTAIS})
            self.assertEqual(mobile.locate("altais", "mobile_capital", "frontier_station", tmp), ("altais", "mobile_capital", ""))

    def test_fixed_station_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [CAPITAL, FIXED], {"altais": ALTAIS})
            self.assertEqual(mobile.locate("nexus_prime", "the_core", "central_nexus", tmp), ("nexus_prime", "the_core", ""))

    def test_no_census_or_broken_files_leave_the_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [CAPITAL], {})
            self.assertEqual(mobile.locate("frontier", "mobile_capital", "frontier_station", tmp), ("frontier", "mobile_capital", ""))
            (Path(tmp) / "station" / "stations.json").write_text("not json", encoding="ascii")
            self.assertEqual(mobile.locate("frontier", "mobile_capital", "frontier_station", tmp), ("frontier", "mobile_capital", ""))

    def test_station_arrived_before_its_census_is_followed_by_name(self):
        # the station list names the new system; that system's census predates the arrival; an older census named its poi
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [dict(CAPITAL, system="distant_light")], {"altais": ALTAIS, "distant_light": [{"id": "rigel_minor_star"}]})
            system, poi, line = mobile.locate("altais", "mobile_capital", "frontier_station", tmp)
            self.assertEqual((system, poi), ("distant_light", "mobile_capital"))
            self.assertIn("distant_light:mobile_capital", line)

    def test_station_by_name_needs_a_census_that_named_its_poi(self):
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [dict(CAPITAL, system="distant_light")], {"distant_light": [{"id": "rigel_minor_star"}]})
            self.assertEqual(mobile.locate("altais", "mobile_capital", "frontier_station", tmp), ("altais", "mobile_capital", ""))

    def test_base_whose_id_is_no_station_name_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [dict(CAPITAL, system="distant_light")], {"altais": ALTAIS})
            self.assertEqual(mobile.locate("altais", "mobile_capital", "a1b2c3", tmp), ("altais", "mobile_capital", ""))

    def test_wrecked_mobile_station_is_not_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            world(Path(tmp), [dict(CAPITAL, wrecked=True)], {"altais": ALTAIS})
            self.assertEqual(mobile.locate("frontier", "mobile_capital", "frontier_station", tmp), ("frontier", "mobile_capital", ""))


class RunnerTests(unittest.TestCase):
    """The two runners that travel to a named station ask mobile.locate before the travel goal."""

    def test_route_run_locates_each_stop(self):
        text = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertRegex(text, r"system, poi, base = stop\['at'\]\.split\(':'\)\n\s+system, poi, moved = mobile\.locate\(system, poi, base, DATA\)")

    def test_hunt_locates_its_sell_at(self):
        text = (FLEET / "hunt.py").read_text(encoding="ascii")
        self.assertTrue(re.search(r"sell_at\[0\], sell_at\[1\], MOVED = mobile\.locate\(sell_at\[0\], sell_at\[1\], sell_at\[2\]", text))


if __name__ == "__main__":
    unittest.main()
