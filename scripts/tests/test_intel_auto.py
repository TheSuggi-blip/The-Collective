"""The automatic intel (index, system tracker, pilot tracker, the pass that commits) on disposable trees."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
CHART = ("# fixture chart\n"
         "nexus_prime\tNexus Prime\t0.0\t0.0\tvoidborn\thome\t0\tnode_alpha\n"
         "node_alpha\tNode Alpha\t10.0\t0.0\tvoidborn\t-\t1\tnexus_prime,far_rock\n"
         "far_rock\tFar Rock\t20.0\t0.0\t-\t-\t2\tnode_alpha\n")


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_") + "_under_test", SCRIPTS / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def system_file(system_id, standing="ally", empire="voidborn", police="80", title="Fixture"):
    fields = ["name: " + system_id, "id: 20261114T000001Z", "tier: intel", "author: Fixture", "kind: system",
              "system_id: " + system_id, "standing: " + standing, "standing_since: 2026-11-14"]
    if standing != "neutral":
        fields += ["standing_by: Fixture", "standing_reason: fixture"]
    fields += ["threat: low", "empire: " + empire, "police_level: " + police, "updated: 2026-11-14"]
    return "---\n" + "\n".join(fields) + "\n---\n\n# " + title + "\n"


def pilot_file(username, standing="neutral"):
    fields = ["name: fixture", "id: 20261114T000002Z", "tier: intel", "author: Fixture", "kind: player", "username: " + username,
              "standing: " + standing, "standing_since: 2026-11-14"]
    if standing != "neutral":
        fields += ["standing_by: Fixture", "standing_reason: fixture"]
    fields += ["threat: medium", "empire: crimson", "faction: none", "updated: 2026-11-14"]
    return "---\n" + "\n".join(fields) + "\n---\n\n# " + username + "\n"


def scouting_read(system_id, empire="voidborn"):
    return {"read_at": "2026-11-15T13:09:41Z",
            "system": {"id": system_id, "name": "Node Alpha", "empire": empire, "police_level": 55,
                       "security_status": "Low Security (slow police response)",
                       "pois": [{"id": "alpha_belt", "name": "Alpha Belt", "type": "asteroid_belt", "class": "mixed"},
                                {"id": "alpha_station", "name": "Alpha Station", "type": "station", "base_id": "alpha_base"},
                                {"id": "alpha_ice", "name": "Alpha Ice", "type": "ice_field"}]},
            "pois": {"alpha_belt": {"poi": {"resources": [{"resource_id": "iron_ore", "richness": 40, "remaining": 78496, "max_remaining": 100000}]}}}}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="intel-auto-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        for folder in ("players", "planets", "map", "scripts"):
            (self.root / folder).mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text(CHART, encoding="ascii")
        self.data = Path(self.temp.name) / "data"
        for folder in ("scouting", "station"):
            (self.data / folder).mkdir(parents=True)
        self.index, self.gate = load("intel-index"), load("validate-intel")

    def put(self, rel, text):
        (self.root / rel).write_text(text, encoding="ascii")

    def run_script(self, name, *args):
        return subprocess.run(["python3", "-B", str(SCRIPTS / (name + ".py")), "--root", str(self.root)] + list(args),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def station_data(self, pilots, players, ours=()):
        (self.data / "station" / "pilots.json").write_text(json.dumps(pilots), encoding="utf-8")
        (self.data / "station" / "feed.json").write_text(json.dumps({"built_at": "2026-11-15T04:13:42Z", "players": players}), encoding="utf-8")
        (self.data / "fleet.json").write_text(json.dumps({"ships": [{"name": n} for n in ours]}), encoding="utf-8")
        return ["--station", str(self.data / "station"), "--fleet", str(self.data / "fleet.json")]


class IndexTests(Tree):
    def test_systems_are_grouped_by_zone_home_first_and_pilots_by_standing(self):
        self.put("planets/n-far_rock.md", system_file("far_rock", "neutral", "none", "0", "Far Rock"))
        self.put("planets/a-node_alpha.md", system_file("node_alpha", title="Node Alpha"))
        self.put("planets/a-nexus_prime.md", system_file("nexus_prime", title="Nexus Prime"))
        self.put("players/n-gemma.md", pilot_file("Gemma"))
        self.put("players/h-silas_vane.md", pilot_file("Silas Vane", "hostile"))
        self.assertTrue(self.index.write(str(self.root), "planets"))
        self.assertTrue(self.index.write(str(self.root), "players"))
        planets = (self.root / "planets" / "index.md").read_text(encoding="ascii")
        self.assertLess(planets.index("## Voidborn space"), planets.index("## Lawless space"))
        self.assertLess(planets.index("a-nexus_prime.md"), planets.index("a-node_alpha.md"))      # by jumps from home
        self.assertIn("| Far Rock | neutral | low | 0 | 2 | 2026-11-14 | [n-far_rock.md](n-far_rock.md) |", planets)
        players = (self.root / "players" / "index.md").read_text(encoding="ascii")
        self.assertLess(players.index("## Hostile"), players.index("## Neutral"))
        self.assertIn("## Ally\n\nNone filed.", players)
        self.assertIn("| Silas Vane | medium | crimson | none | 2026-11-14 | 2026-11-14 | [h-silas_vane.md](h-silas_vane.md) |", players)

    def test_an_unchanged_folder_is_not_rewritten_and_a_new_file_makes_the_index_stale(self):
        self.put("planets/a-nexus_prime.md", system_file("nexus_prime"))
        self.assertEqual(self.index.state(str(self.root), "planets"), "missing")
        self.assertEqual(self.index.state(str(self.root), "players"), "empty")
        self.assertTrue(self.index.write(str(self.root), "planets"))
        first = (self.root / "planets" / "index.md").read_text(encoding="ascii")
        self.assertFalse(self.index.write(str(self.root), "planets"))
        self.assertEqual(self.index.state(str(self.root), "planets"), "current")
        self.put("planets/a-node_alpha.md", system_file("node_alpha"))
        self.assertEqual(self.index.state(str(self.root), "planets"), "stale")
        self.assertTrue(self.index.write(str(self.root), "planets"))
        second = (self.root / "planets" / "index.md").read_text(encoding="ascii")
        self.assertEqual(first.split("\n---\n")[0], second.split("\n---\n")[0])                   # the id is kept

    def test_the_gate_skips_index_md_as_data_and_fails_on_a_stale_or_missing_one(self):
        self.put("planets/a-nexus_prime.md", system_file("nexus_prime"))
        self.assertEqual(self.gate.check(str(self.root))[0], [])
        self.assertEqual(len(self.gate.check_index(str(self.root))), 1)                           # missing
        self.index.write(str(self.root), "planets")
        self.assertEqual(self.gate.check(str(self.root))[0], [])                                  # index.md is not a bad name
        self.assertEqual(self.gate.check_index(str(self.root)), [])
        self.put("planets/a-node_alpha.md", system_file("node_alpha"))
        self.assertIn("planets/index.md is stale", self.gate.check_index(str(self.root))[0])


class PlanetTrackerTests(Tree):
    def test_a_scouting_read_becomes_a_system_file_that_passes_the_gate(self):
        (self.data / "scouting" / "node_alpha.json").write_text(json.dumps(scouting_read("node_alpha")), encoding="utf-8")
        done = self.run_script("intel-planets", "--data", str(self.data / "scouting"))
        self.assertEqual(done.returncode, 0, done.stdout)
        text = (self.root / "planets" / "a-node_alpha.md").read_text(encoding="ascii")
        self.assertEqual(self.gate.check(str(self.root))[0], [])
        self.assertIn("iron_ore: richness 40, 78496 of 100000 left", text)
        self.assertIn("| `alpha_ice` | Alpha Ice | ice_field | -- | not read |", text)
        self.assertIn("own ship", text)
        self.assertIn("| Jumps from home | 1 |", text)

    def test_an_existing_file_is_never_touched_and_foreign_space_is_filed_neutral(self):
        (self.data / "scouting" / "node_alpha.json").write_text(json.dumps(scouting_read("node_alpha")), encoding="utf-8")
        (self.data / "scouting" / "far_rock.json").write_text(json.dumps(scouting_read("far_rock", "none")), encoding="utf-8")
        (self.data / "scouting" / "broken.json").write_text("{not json", encoding="utf-8")
        self.put("planets/n-node_alpha.md", "hand-written\n")
        done = self.run_script("intel-planets", "--data", str(self.data / "scouting"))
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual((self.root / "planets" / "n-node_alpha.md").read_text(encoding="ascii"), "hand-written\n")
        self.assertFalse((self.root / "planets" / "a-node_alpha.md").exists())
        self.assertIn("standing: neutral", (self.root / "planets" / "n-far_rock.md").read_text(encoding="ascii"))
        self.assertIn("1 new system file(s)", done.stdout)


class PilotTrackerTests(Tree):
    def test_only_an_armed_stranger_seen_in_our_space_today_is_filed(self):
        now = time.time()
        weird = "Zo" + chr(0xEB)
        pilots = {"Killer": ["node_alpha", now - 600, "crimson", "RED"], "Trucker": ["node_alpha", now - 600, "nebula", ""],
                  "miner-1": ["nexus_prime", now - 600, "voidborn", ""], "Raider": ["far_rock", now - 600, "crimson", ""],
                  "Ghost": ["nexus_prime", now - 90000, "crimson", ""], weird: ["nexus_prime", now - 60, "outerrim", ""]}
        stats = lambda kills: {"empire": "crimson", "faction": "RED", "stats": {"ships_destroyed": kills, "ships_lost": 1, "pirates_destroyed": 4}}
        players = {"killer": stats(12), "trucker": stats(0), "miner-1": stats(3), "raider": stats(40), "ghost": stats(9), weird.lower(): stats(2)}
        args = self.station_data(pilots, players, ours=["miner-1"])
        done = self.run_script("intel-players", *args)
        self.assertEqual(done.returncode, 0, done.stdout)
        names = sorted(p.name for p in (self.root / "players").iterdir())
        self.assertEqual(names, ["n-killer.md", "n-zoueb.md"])
        text = (self.root / "players" / "n-killer.md").read_text(encoding="ascii")
        self.assertIn("standing: neutral", text)
        self.assertIn("threat: medium", text)
        self.assertIn("| Player ships destroyed | 12 |", text)
        self.assertIn("username: Zo\\u{eb}", (self.root / "players" / "n-zoueb.md").read_text(encoding="ascii"))
        self.assertEqual(self.gate.check(str(self.root))[0], [])
        again = self.run_script("intel-players", *args)
        self.assertIn("0 new pilot file(s)", again.stdout)

    def test_the_cap_limits_a_run_to_the_highest_kill_counts(self):
        now = time.time()
        pilots = {"P%d" % n: ["nexus_prime", now - 60, "crimson", ""] for n in range(5)}
        players = {"p%d" % n: {"empire": "crimson", "faction": "", "stats": {"ships_destroyed": n + 1}} for n in range(5)}
        done = self.run_script("intel-players", "--max", "2", *self.station_data(pilots, players))
        self.assertEqual(sorted(p.name for p in (self.root / "players").iterdir()), ["n-p3.md", "n-p4.md"], done.stdout)


class TrackPassTests(Tree):
    def setUp(self):
        super().setUp()
        for name in ("intel-index.py", "intel-planets.py", "intel-players.py", "intel-track.py", "validate-intel.py", "validate-ids.sh"):
            shutil.copy(SCRIPTS / name, self.root / "scripts" / name)
        self.put("planets/a-nexus_prime.md", system_file("nexus_prime"))
        self.index.write(str(self.root), "planets")
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "baseline")
        (self.data / "scouting" / "node_alpha.json").write_text(json.dumps(scouting_read("node_alpha")), encoding="utf-8")
        self.args = ["--data", str(self.data / "scouting")] + self.station_data({}, {})

    def git(self, *args):
        return subprocess.run(["git"] + list(args), cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout

    def track(self, *args):
        return subprocess.run(["python3", "-B", str(self.root / "scripts" / "intel-track.py"), "--root", str(self.root)] + list(args) + self.args,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def test_a_pass_commits_exactly_its_own_files_and_leaves_the_clone_clean(self):
        (self.root / "notes.txt").write_text("another agent's work in progress\n", encoding="ascii")
        done = self.track("--commit")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(sorted(self.git("show", "--name-only", "--format=", "HEAD").split()), ["planets/a-node_alpha.md", "planets/index.md"])
        self.assertEqual(self.git("log", "-1", "--format=%an <%ae>").strip(), "Unity <unity@suggi-workspace.dev>")
        self.assertEqual(self.git("status", "--porcelain").strip(), "?? notes.txt")
        self.assertIn("Nothing new.", self.track("--commit").stdout)

    def test_without_commit_a_pass_is_a_rehearsal_that_leaves_nothing_behind(self):
        done = self.track()
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("Would change", done.stdout)
        self.assertIn("planets/a-node_alpha.md", done.stdout)
        self.assertEqual(self.git("status", "--porcelain").strip(), "")
        self.assertIn("baseline", self.git("log", "-1", "--format=%s"))

    def test_a_pass_refuses_to_start_on_uncommitted_intel(self):
        self.put("players/n-gemma.md", pilot_file("Gemma"))
        done = self.track("--commit")
        self.assertEqual(done.returncode, 1)
        self.assertIn("HALT", done.stdout)
        self.assertFalse((self.root / "planets" / "a-node_alpha.md").exists())

    def test_a_failed_gate_takes_the_pass_out_again(self):
        self.put("planets/n-far_rock.md", system_file("far_rock", "neutral", "none", "0").replace("threat: low", "threat: deadly"))
        self.git("add", "-A")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "a bad file gets in")
        done = self.track("--commit")
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertFalse((self.root / "planets" / "a-node_alpha.md").exists())
        self.assertEqual(self.git("status", "--porcelain").strip(), "")
        self.assertIn("a bad file gets in", self.git("log", "-1", "--format=%s"))


if __name__ == "__main__":
    unittest.main()
