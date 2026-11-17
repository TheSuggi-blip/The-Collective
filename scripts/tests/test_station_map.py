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

    def test_what_the_faction_owns_reaches_the_map_with_a_mark_per_kind(self):
        (self.base / "data/empire").mkdir()
        (self.base / "data/empire/empire.json").write_text(json.dumps({
            "written_at": "2026-11-17T10:00:00Z", "faction": {"treasury": 104771},
            "bases": [{"name": "Test Rock", "kind": "outpost", "system": "wild"}, "not a row"],
            "facilities": [{"type": "faction_lockbox", "name": "Faction Lockbox", "level": 1, "base": "hub_station", "system": "home", "status": "active"},
                           {"type": "hiring_board", "name": "Hiring Board", "level": 1, "base": "hub_station", "system": "home", "status": "under_construction"},
                           {"type": "faction_desk", "name": "Faction Desk", "level": 2, "base": "hub_station", "system": "home"},
                           {"type": "faction_fuel_bunker", "name": "Faction Fuel Bunker", "level": 1, "base": "0123456789abcdef0123456789abcdef", "system": "wild"},
                           {"type": "faction_lockbox", "name": "Faction Lockbox", "level": 1, "base": "fedcba9876543210fedcba9876543210", "system": "far"},
                           {"type": "faction_lockbox", "name": "No system"}]}), encoding="ascii")
        got = self.station.load_holdings()
        self.assertEqual(got["read_at"], "2026-11-17T10:00:00Z")
        self.assertEqual([(b["system"], b["kind"], b["name"], b["level"], b["status"], b["at"]) for b in got["buildings"]],
                         [("wild", "outpost", "Test Rock", 0, "active", ""), ("home", "storage", "Faction Lockbox", 1, "active", "Hub Station"),
                          ("home", "recruit", "Hiring Board", 1, "under_construction", "Hub Station"), ("home", "office", "Faction Desk", 2, "active", "Hub Station"),
                          ("wild", "fuel", "Faction Fuel Bunker", 1, "active", "Test Rock"),       # inside our own base: named by the base, not by its id
                          ("far", "storage", "Faction Lockbox", 1, "active", "our base here")])      # a base the public list does not carry yet
        self.assertEqual([b["part"] for b in got["buildings"]], [False, False, False, False, True, True])
        self.assertEqual(got["treasury"], 104771)
        self.assertEqual([b["base"] for b in got["buildings"]][1:5], ["hub_station", "hub_station", "hub_station", "0123456789abcdef0123456789abcdef"])   # the id the inventory names a place by
        self.station.HOLDINGS["at"] = 0.0
        (self.base / "data/empire/empire.json").unlink()
        self.assertEqual(self.station.load_holdings(), {"read_at": "", "treasury": 0, "buildings": []})            # no file: nothing owned, no fault

    def test_a_site_reads_built_once_a_base_of_ours_stands_in_its_system(self):
        sites = [{"system": "wild", "status": "chosen", "by": "Zero"}, {"system": "home", "status": "candidate", "by": "Suggi"},
                 {"system": "gone", "status": "dropped", "by": "Oracle"}]
        holdings = {"buildings": [{"system": "wild", "kind": "outpost"}, {"system": "home", "kind": "storage"}, {"system": "gone", "kind": "station"}]}
        self.assertEqual([s["status"] for s in self.station.sites_with_bases(sites, holdings)], ["built", "candidate", "dropped"])
        self.assertEqual(sites[0]["status"], "chosen")                                              # the list read from the file is not changed
        self.assertEqual(self.station.sites_with_bases(sites, {}), sites)

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


class StationWaveTests(unittest.TestCase):
    def test_a_wave_reaches_the_page_as_numbers_and_three_short_words(self):
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("station_server_wave", Path(__file__).resolve().parents[2] / "station" / "server.py")
        server = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server)
        row = server.wave_row({"since": 100, "end": 0, "off": 30, "peak": 31, "ships": 246, "cause": "update", "from": "0.1.0", "to": "<b>0.1.1</b> and a long tail"})
        self.assertEqual(row, {"since": 100, "end": 0, "off": 30, "peak": 31, "ships": 246, "minutes": 0, "cause": "update", "from": "0.1.0",
                               "to": "<b>0.1.1</b> and a l"})                                    # cut to twenty characters; the page writes it as text
        self.assertEqual(server.wave_row({"since": 5, "cause": "<script>"})["cause"], "unknown")
        self.assertEqual((server.wave_row(None), server.wave_row({"cause": "engine"})), (None, None))


if __name__ == "__main__":
    unittest.main()
