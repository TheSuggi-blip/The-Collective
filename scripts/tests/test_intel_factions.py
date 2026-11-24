"""intel-factions.py on disposable trees: which factions get a file, what is written anew, what is kept, the zones index."""

import importlib.util
import json
from pathlib import Path
import tempfile
import time
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "intel-factions.py"
spec = importlib.util.spec_from_file_location("intel_factions_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
factions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(factions)


def base(name, kind, system, tag="", faction="", empire=""):
    return {"name": name, "type": kind, "system": system, "tag": tag, "faction": faction, "empire": empire, "condition": "thriving",
            "services": [], "wrecked": False, "mobile": False}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="intel-factions-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.station = Path(self.temp.name) / "repo", Path(self.temp.name) / "station"
        self.root.mkdir()
        self.station.mkdir()
        self.now = time.time()
        self.write("map.json", {"systems": [
            {"id": "nexus_prime", "name": "Nexus Prime", "empire": "voidborn", "lanes": ["synchrony"]},
            {"id": "synchrony", "name": "Synchrony", "empire": "voidborn", "lanes": ["nexus_prime", "okab"]},
            {"id": "okab", "name": "Okab", "empire": "", "lanes": ["synchrony", "far"]},
            {"id": "far", "name": "Far", "empire": "", "lanes": ["okab"]}]})
        self.bases = [base("Argon Bank", "outpost", "far", "HEXC", "Hex Collective"), base("Okab Hold", "station", "okab", "HEXC", "Hex Collective"),
                      base("Blood Den", "station", "okab", empire="pirates"), base("Central Nexus", "station", "nexus_prime", empire="voidborn"),
                      base("Our Post", "outpost", "far", "CLTV", "The Collective")]
        self.write("stations.json", self.bases)
        self.write("pilots.json", {
            "HexBot1": ["synchrony", self.now - 100, "nebula", "HEXC"], "HexBot2": ["okab", self.now - 100, "nebula", "HEXC"],
            "Zo\u00eb": ["synchrony", self.now - 5, "nebula", "HEXC"],
            "Olaf": ["nexus_prime", self.now - 50, "solarian", "OLSV"], "Olga": ["synchrony", self.now - 60, "solarian", "OLSV"],
            "Lone": ["nexus_prime", self.now - 10, "crimson", "SOLO"], "Old": ["nexus_prime", self.now - 90000, "crimson", "PAST"],
            "Prime Directive": ["nexus_prime", self.now - 5, "voidborn", "CLTV"], "miner-1": ["nexus_prime", self.now - 5, "voidborn", ""]})
        self.write("feed.json", {"factions": {"HEXC": {"name": "Hex Collective", "members": 72, "leader": "HexLord", "allies": [], "enemies": ["OLSV"], "wars": []},
                                              "OLSV": {"name": "Olsen Line", "members": 40, "leader": "Ole", "allies": [], "enemies": [], "wars": []}},
                                 "players": {"hexbot1": {"name": "HexBot1", "stats": {"ships_destroyed": 3}}}})
        self.write("fleet.json", {"ships": [{"name": "miner-1"}, {"name": "Prime Directive"}]})
        self.write("met.json", {"HexBot1": {"ship_class": "liminal"}})

    def write(self, name, value):
        (self.station / name).write_text(json.dumps(value), encoding="utf-8")

    def run_pass(self, limit=40, now=None):
        now = now or self.now
        data = factions.gather(str(self.station), str(self.station / "met.json"), str(self.station / "fleet.json"), now)
        written = factions.write_files(str(self.root), data, now, limit)
        return written, factions.write_index(str(self.root), data, now)

    def text(self, name):
        return (self.root / "game" / "factions" / name).read_text(encoding="ascii")


class FileTests(Tree):
    def test_a_faction_with_a_base_or_two_pilots_in_our_space_gets_a_file(self):
        written, index = self.run_pass()
        self.assertEqual(sorted(written), ["game/factions/n-hexc.md", "game/factions/n-olsv.md"])           # not SOLO (one pilot), PAST (old), CLTV (ours)
        self.assertEqual(index, "game/factions/index.md")
        hexc = self.text("n-hexc.md")
        self.assertIn("kind: faction\ntag: HEXC\nfaction: Hex Collective\nstanding: neutral\n", hexc)
        self.assertIn("# Hex Collective [HEXC]\n\nA player faction with 2 base(s) in 2 system(s); the nearest to Nexus Prime is 2 jump(s) away, in Okab (`okab`).\n"
                      "Pilots of it in our space in the last 24 hours: 2.\n", hexc)
        rows = [line for line in hexc.splitlines() if line.startswith("| ")]
        self.assertIn("| Leader | HexLord | Daily feed, factions |", rows)
        self.assertIn("| Enemies | OLSV | Daily feed, factions |", rows)
        self.assertIn("| Pilots carrying the tag on the public event stream | 3 | Public event stream |", rows)
        self.assertLess(rows.index("| Okab Hold | station | Okab (`okab`) | lawless | 2 | thriving |"), rows.index("| Argon Bank | outpost | Far (`far`) | lawless | 3 | thriving |"))
        self.assertIn("| HexBot1 | Synchrony (`synchrony`) | 3 | liminal |", rows)
        self.assertIn("| Zo\\u{eb} | Synchrony (`synchrony`) | not on record | not met |", rows)       # ASCII only
        self.assertNotIn("HexBot2", hexc)                                                         # it is not in our space
        olsv = self.text("n-olsv.md")
        self.assertIn("A player faction without a base on the public record.", olsv)
        self.assertIn("\n## Bases\n\nNone on the public record.\n", olsv)
        self.assertTrue(olsv.endswith("| neutral | Filed by the tracker; it has not met us | `scripts/intel-factions.py` |\n\n## Notes\n\nNone.\n"))
        ids = {self.text(n).split("\nid: ")[1].split("\n")[0] for n in ("n-hexc.md", "n-olsv.md", "index.md")}
        self.assertEqual(len(ids), 3)
        self.assertTrue(all(not i.endswith("00Z") for i in ids))

    def test_an_unchanged_faction_is_not_rewritten(self):
        self.run_pass()
        before = {p.name: p.stat().st_mtime_ns for p in (self.root / "game" / "factions").iterdir()}
        self.assertEqual(self.run_pass(now=self.now + 30), ([], None))
        self.assertEqual({p.name: p.stat().st_mtime_ns for p in (self.root / "game" / "factions").iterdir()}, before)

    def test_the_standing_and_the_hand_written_part_are_kept_when_the_facts_move(self):
        self.run_pass()
        folder = self.root / "game" / "factions"
        text = self.text("n-hexc.md").replace("standing: neutral", "standing: hostile").replace("threat: unknown", "threat: high")
        text = text.replace("## Notes\n\nNone.\n", "| 2026-11-16 | hostile | It attacked an own ship at Okab | Unity |\n\n## Notes\n\nIts scouts sit at our gate.\n")
        (folder / "h-hexc.md").write_text(text, encoding="ascii")
        (folder / "n-hexc.md").unlink()                                                           # the rename by hand
        first_id = text.split("\nid: ")[1].split("\n")[0]
        self.write("stations.json", self.bases + [base("Gate Watch", "outpost", "synchrony", "HEXC", "Hex Collective")])
        written, index = self.run_pass(now=self.now + 60)
        self.assertEqual((written, index), (["game/factions/h-hexc.md"], "game/factions/index.md"))
        self.assertFalse((folder / "n-hexc.md").exists())                                         # never a second file
        new = self.text("h-hexc.md")
        self.assertIn("id: %s\n" % first_id, new)
        self.assertIn("standing: hostile\n", new)
        self.assertIn("threat: high\n", new)
        self.assertIn("| Gate Watch | outpost | Synchrony (`synchrony`) | voidborn | 1 | thriving |", new)
        self.assertIn("| 2026-11-16 | hostile | It attacked an own ship at Okab | Unity |\n\n## Notes\n\nIts scouts sit at our gate.\n", new)
        index_text = self.text("index.md")
        self.assertIn("## Hostile\n\n| Faction | Tag | Threat | Bases | Nearest base (jumps) | Pilots in our space (24 h) | Updated | File |\n|---|---|---|---|---|---|---|---|\n"
                      "| Hex Collective | HEXC | high | 3 | 1 | 2 |", index_text)

    def test_the_cap_files_the_factions_with_a_base_first(self):
        written, _index = self.run_pass(limit=1)
        self.assertEqual(written, ["game/factions/n-hexc.md"])
        written, _index = self.run_pass(limit=1, now=self.now + 5)
        self.assertEqual(written, ["game/factions/n-olsv.md"])


class IndexTests(Tree):
    def test_the_index_lists_zones_nearest_first_tags_in_our_space_and_pirate_strongholds(self):
        self.run_pass()
        text = self.text("index.md")
        self.assertTrue(text.startswith("---\nname: factions-index\nid: "))
        zones = text.split("## Zones Held by Other Players")[1].split("## Hostile")[0]
        rows = [line for line in zones.splitlines() if line.startswith("| ") and "System |" not in line]
        self.assertEqual(rows, ["| Okab (`okab`) | lawless | 2 | Hex Collective [HEXC] | Okab Hold (station) | [n-hexc.md](n-hexc.md) |",
                                "| Far (`far`) | lawless | 3 | Hex Collective [HEXC] | Argon Bank (outpost) | [n-hexc.md](n-hexc.md) |"])
        self.assertIn("## Hostile\n\nNone filed.\n", text)
        self.assertIn("## Ally\n\nNone filed.\n", text)
        tags = text.split("## Tags Seen in Our Space")[1].split("## Pirate Strongholds")[0]
        self.assertEqual([line for line in tags.splitlines() if line.startswith("| ") and "Tag |" not in line],
                         ["| HEXC | Hex Collective | 2 | [n-hexc.md](n-hexc.md) |", "| OLSV | Olsen Line | 2 | [n-olsv.md](n-olsv.md) |", "| SOLO | not on record | 1 | -- |"])
        self.assertIn("## Pirate Strongholds\n\n| System | Space | Jumps from Nexus Prime | Base |\n|---|---|---|---|\n| Okab (`okab`) | lawless | 2 | Blood Den |\n", text)
        self.assertNotIn("CLTV", text)                                                            # our own faction is never listed
        for path in (self.root / "game" / "factions").iterdir():
            path.read_text(encoding="ascii")                                                      # raises on a byte outside ASCII

    def test_without_a_chart_nothing_is_written(self):
        (self.station / "map.json").unlink()
        data = factions.gather(str(self.station), str(self.station / "met.json"), str(self.station / "fleet.json"), self.now)
        self.assertEqual(data["space"], {})
        self.assertFalse((self.root / "game" / "factions").exists())

    def test_keys_and_ascii(self):
        self.assertEqual([factions.key_of(t) for t in ("HEXC", "A-1!", "3333")], ["hexc", "ax2d1x21", "3333"])
        self.assertEqual(factions.ascii_text("a | b\n \u2620"), "a / b \\u{2620}")
        self.assertEqual(factions.jumps_from([{"id": "a", "lanes": ["b"]}, {"id": "b", "lanes": ["a", "c"]}, {"id": "c", "lanes": ["b"]}, {"id": "d", "lanes": []}], "a"), {"a": 0, "b": 1, "c": 2})



class ChurnThrottleTests(Tree):
    def test_minor_sighting_drift_skipped_within_min_interval_but_strategic_change_rewrites_immediately(self):
        written, index = self.run_pass()
        self.assertEqual(sorted(written), ["game/factions/n-hexc.md", "game/factions/n-olsv.md"])
        self.assertEqual(index, "game/factions/index.md")
        # 1. Minor 1-pilot rolling drift 10 minutes later: skipped when min_interval=21600
        pilots = json.loads((self.station / "pilots.json").read_text(encoding="utf-8"))
        pilots["HexBot3"] = ["synchrony", self.now + 600, "nebula", "HEXC"]
        self.write("pilots.json", pilots)
        data2 = factions.gather(str(self.station), str(self.station / "met.json"), str(self.station / "fleet.json"), self.now + 600)
        w2 = factions.write_files(str(self.root), data2, self.now + 600, 40, min_interval=21600)
        i2 = factions.write_index(str(self.root), data2, self.now + 600, min_interval=21600, files_written=w2)
        self.assertEqual(w2, [])
        self.assertIsNone(i2)
        # 2. Strategic change (new base built by HEXC): rewrites IMMEDIATELY even within min_interval
        self.bases.append(base("New Outpost", "outpost", "okab", "HEXC", "Hex Collective"))
        self.write("stations.json", self.bases)
        data3 = factions.gather(str(self.station), str(self.station / "met.json"), str(self.station / "fleet.json"), self.now + 700)
        w3 = factions.write_files(str(self.root), data3, self.now + 700, 40, min_interval=21600)
        i3 = factions.write_index(str(self.root), data3, self.now + 700, min_interval=21600, files_written=w3)
        self.assertEqual(w3, ["game/factions/n-hexc.md"])
        self.assertEqual(i3, "game/factions/index.md")
        # 3. Once min_interval elapses, minor drift rewrites cleanly
        pilots["Olaf2"] = ["nexus_prime", self.now + 25000, "solarian", "OLSV"]
        self.write("pilots.json", pilots)
        data4 = factions.gather(str(self.station), str(self.station / "met.json"), str(self.station / "fleet.json"), self.now + 25000)
        w4 = factions.write_files(str(self.root), data4, self.now + 25000, 40, min_interval=21600)
        self.assertIn("game/factions/n-olsv.md", w4)

if __name__ == "__main__":
    unittest.main()
