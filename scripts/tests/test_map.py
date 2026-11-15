"""Chart regressions use a disposable chart, never game/map/galaxy.tsv and never the network."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "map.py"

# home - alpha - beta - far, and an island with no lane to the rest.
PAYLOAD = {
    "systems": [
        {"id": "far", "name": "Far", "x": 30.04, "y": -1.26, "connections": ["beta"],
         "is_stronghold": True},
        {"id": "nexus_prime", "name": "Nexus Prime", "x": -4000, "y": 2000, "empire": "voidborn",
         "is_home": True, "connections": ["alpha"], "online": 7},
        {"id": "beta", "name": "Beta Two", "x": 20, "y": 0, "connections": ["far", "alpha"]},
        {"id": "alpha", "name": "Alpha", "x": 10, "y": 0, "empire": "voidborn",
         "connections": ["nexus_prime", "beta"]},
        {"id": "island", "name": "Island", "x": 99, "y": 99, "connections": []},
    ]
}


class MapTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("map_under_test", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.map = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.map)
        self.temp = tempfile.TemporaryDirectory(prefix="map-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = self.temp.name

    def chart(self):
        self.map.write_chart(self.root, self.map.rows_from_api(PAYLOAD), "2026-11-14T00:00:01Z")
        return self.map.read_chart(self.root)

    def test_rows_are_sorted_and_carry_flags_jumps_and_lanes(self):
        rows = self.map.rows_from_api(PAYLOAD)
        self.assertEqual([row[0] for row in rows], ["alpha", "beta", "far", "island", "nexus_prime"])
        by_id = {row[0]: row for row in rows}
        self.assertEqual(by_id["nexus_prime"], ["nexus_prime", "Nexus Prime", "-4000.0", "2000.0",
                                                "voidborn", "home", "0", "alpha"])
        self.assertEqual(by_id["far"], ["far", "Far", "30.0", "-1.3", "-", "stronghold", "3", "beta"])
        self.assertEqual(by_id["beta"][7], "alpha,far")
        self.assertEqual(by_id["island"][6], "-")

    def test_chart_survives_a_round_trip(self):
        systems = self.chart()
        self.assertEqual(len(systems), 5)
        self.assertEqual(systems["far"].jumps, 3)
        self.assertEqual(systems["far"].flags, ["stronghold"])
        self.assertEqual(systems["alpha"].lanes, ["beta", "nexus_prime"])
        self.assertIsNone(systems["island"].jumps)
        self.assertEqual(systems["island"].lanes, [])
        self.assertEqual(self.map.chart_rows_on_disk(self.root), self.map.rows_from_api(PAYLOAD))

    def test_route_is_the_shortest_and_none_without_lanes(self):
        systems = self.chart()
        self.assertEqual(self.map.route(systems, "nexus_prime", "far"),
                         ["nexus_prime", "alpha", "beta", "far"])
        self.assertEqual(self.map.route(systems, "far", "far"), ["far"])
        self.assertIsNone(self.map.route(systems, "nexus_prime", "island"))

    def test_find_by_id_or_name(self):
        systems = self.chart()
        self.assertEqual(self.map.find(systems, "beta").id, "beta")
        self.assertEqual(self.map.find(systems, "beta two").id, "beta")
        self.assertEqual(self.map.find(systems, "Nexus Prime").id, "nexus_prime")
        with self.assertRaises(SystemExit):
            self.map.find(systems, "nowhere")

    def test_non_ascii_chart_cell_is_refused(self):
        payload = {"systems": [{"id": "x", "name": "Caf" + chr(0xE9), "x": 0, "y": 0, "connections": []}]}
        with self.assertRaises(ValueError):
            self.map.rows_from_api(payload)

    def test_intel_file_lookup(self):
        self.chart()
        self.assertEqual(self.map.intel_file(self.root, "far"), "none yet")
        planets = Path(self.root) / "game" / "planets"
        planets.mkdir()
        (planets / "h-far.md").write_text("fixture\n", encoding="ascii")
        self.assertEqual(self.map.intel_file(self.root, "far"), "game/planets/h-far.md")


if __name__ == "__main__":
    unittest.main()
