"""The station's map data beyond the public feeds: the sites named for a base and a foreign group's pilots with the hulls
our own ships saw. Fixtures only, no network."""

import importlib.util
import json
from pathlib import Path
import tempfile
import time
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / "station" / "server.py"


class StationMapTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("station_map_under_test", SCRIPT)
        assert spec is not None and spec.loader is not None
        self.station = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.station)
        self.temp = tempfile.TemporaryDirectory(prefix="station-map-test-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.station.DATA, self.station.REPO, self.station.FLEET = base / "station", base / "repo", base / "data" / "fleet"
        for folder in ("station", "repo/game/map", "data/fleet", "data/intel", "data/catalog"):
            (base / folder).mkdir(parents=True)
        self.base = base

    def test_the_sites_named_for_a_base_come_from_the_repository_file(self):
        (self.base / "repo/game/map/sites.tsv").write_text(
            "# a comment\nsystem\tpoi\tstatus\tproposed_by\tnote\nyildun\t-\tcandidate\tSuggi\ta note\nold_place\t-\tdropped\tOracle\tx\nshort\tline\n", encoding="ascii")
        self.assertEqual(self.station.load_sites(), [{"system": "yildun", "status": "candidate", "by": "Suggi"},
                                                     {"system": "old_place", "status": "dropped", "by": "Oracle"}])
        self.station.SITES["at"] = 0.0
        (self.base / "repo/game/map/sites.tsv").unlink()
        self.assertEqual(self.station.load_sites(), [])                                             # no file: no sites, no fault

    def test_a_foreign_group_is_listed_with_the_hulls_our_ships_saw(self):
        now = time.time()
        (self.base / "data/catalog/0.9.0.json").write_text(json.dumps({"ships": [{"id": "big_hull", "name": "Old Name", "tier": 1}]}), encoding="ascii")
        (self.base / "data/catalog/0.10.0.json").write_text(json.dumps({"ships": [{"id": "big_hull", "name": "Big Hull", "tier": 3}, {"id": "skiff", "name": "Skiff", "tier": 1}]}),
                                                         encoding="ascii")
        (self.base / "data/catalog/ammo.json").write_text("{}", encoding="ascii")                   # not a version: never the catalog
        (self.base / "data/intel/met.json").write_text(json.dumps({"Ann": {"ship_class": "skiff", "times": 2, "last": "2026-11-17T00:00:00Z"},
                                                                 "Bob": {"ship_class": "big_hull", "times": 7}, "Dee": {"ship_class": "unknown_hull", "times": 1}}), encoding="ascii")
        (self.base / "data/fleet/fleet.json").write_text(json.dumps({"ships": [{"name": "miner-1"}]}), encoding="ascii")
        self.station.PILOTS.update({"Ann": ["sol", now - 60, "solarian", "IRLC"], "Bob": ["sol", now - 600, "solarian", "IRLC"],
                                    "Cy": ["sol", now - 30, "solarian", "IRLC"], "Dee": ["sol", now - 90, "", "IRLC"],
                                    "Late": ["sol", now - 4000, "solarian", "IRLC"], "Else": ["sol", now - 10, "solarian", "BUSY"],
                                    "Away": ["alpha", now - 10, "solarian", "IRLC"], "miner-1": ["sol", now - 10, "voidborn", "IRLC"]})
        self.station.VALUE["feed"] = {"factions": {"IRLC": {"name": "Ironclad", "members": 40}},
                                      "players": {"bob": {"name": "Bob", "stats": {"ships_destroyed": 4, "time_played": 7200}}}}
        got = self.station.api_faction("sol|IRLC")
        self.assertEqual([p["name"] for p in got["pilots"]], ["Bob", "Ann", "Dee", "Cy"])               # the highest tier first; one hour; never our own
        self.assertEqual((got["count"], got["known"], got["top_tier"], got["name"], got["members"], got["standing"]), (4, 3, 3, "Ironclad", 40, "unknown"))
        bob, cy, dee = got["pilots"][0], got["pilots"][3], got["pilots"][2]
        self.assertEqual((bob["hull"], bob["tier"], bob["times"], bob["destroyed"], bob["hours"]), ("Big Hull", 3, 7, 4, 2))   # the newest catalog: 0.10 is above 0.9
        self.assertEqual((cy["hull"], cy["tier"], cy["times"]), ("", 0, 0))                           # never met by our ships
        self.assertEqual((dee["hull"], dee["tier"]), ("unknown hull", 0))                             # a hull the catalog does not hold keeps its id
        self.assertEqual(self.station.api_faction("sol|")["count"], 0)                               # no tag: nobody
        self.assertEqual(self.station.api_faction("nowhere|IRLC")["pilots"], [])


if __name__ == "__main__":
    unittest.main()
