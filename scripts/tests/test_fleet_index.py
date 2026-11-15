"""fleet-index.py on disposable trees: what is read from a docstring, how a script is run, the rule's errors, the index and its commit."""

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "fleet-index.py"
spec = importlib.util.spec_from_file_location("fleet_index_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index)

DISPATCH = '''#!/usr/bin/env python3
"""dispatch.py -- keep every pilot at work: one task per free pilot.

WHAT: starts one runner per free pilot:
        circuit  -> game/fleet/route_run.py   stops with missions
        hunt     -> game/fleet/hunt.py        grazers at one place
RULES:
  - It sends no command itself.

USAGE:
  dispatch.py              run forever (the service `dispatch`)
  dispatch.py --once       one pass

Stdlib only.
"""
import sys
sys.exit("a script of the fixture must never be run")
'''
ROUTE_RUN = '''"""Fly one pilot along a route file: dock at each stop and
do what the stop says. A second sentence.

Usage: python3 -I route_run.py <pilot> <route id> [--from N]
                               [--verbose]

At every stop it docks.
"""
'''
GATE = '''"""Small client for the engine's gate | no proxy.

Usage:
  gate.py get <path>
  gate.py raw <pilot> <action>
Prints the JSON answer.
"""
'''


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-index-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.fleet = self.root / "game" / "fleet"
        self.fleet.mkdir(parents=True)
        for name, text in (("dispatch.py", DISPATCH), ("route_run.py", ROUTE_RUN), ("gate.py", GATE)):
            self.put(name, text)
        (self.fleet / "notes.txt").write_text("not a script\n", encoding="ascii")

    def put(self, name, text):
        (self.fleet / name).write_text(text, encoding="ascii")

    def text(self):
        return (self.fleet / "index.md").read_text(encoding="ascii")


class ReadTests(Tree):
    def test_the_first_paragraph_and_the_usage_block_are_read_in_both_forms(self):
        scripts, errors = index.read_folder(str(self.root))
        self.assertEqual(errors, [])
        by = {s["name"]: s for s in scripts}
        self.assertEqual(sorted(by), ["dispatch.py", "gate.py", "route_run.py"])
        self.assertEqual(by["dispatch.py"]["summary"], "Keep every pilot at work: one task per free pilot.")       # the `name -- ` is cut, the first letter raised
        self.assertEqual(by["dispatch.py"]["usage"], ["dispatch.py              run forever (the service `dispatch`)", "dispatch.py --once       one pass"])
        self.assertEqual(by["route_run.py"]["summary"], "Fly one pilot along a route file: dock at each stop and do what the stop says. A second sentence.")
        self.assertEqual(by["route_run.py"]["usage"], ["route_run.py <pilot> <route id> [--from N]", "    [--verbose]"])   # `python3 -I ` is cut; the next line stays a continuation
        self.assertEqual(by["gate.py"]["usage"], ["gate.py get <path>", "gate.py raw <pilot> <action>"])                    # the line that is not indented ends the block

    def test_how_a_script_is_run_is_derived(self):
        scripts, _errors = index.read_folder(str(self.root))
        self.assertEqual({s["name"]: s["how"] for s in scripts}, {"dispatch.py": "Service", "route_run.py": "Runner (`circuit` routes)", "gate.py": "By hand"})
        self.assertIn("the dispatcher starts it for a route of the kind `circuit`", {s["name"]: s["run"] for s in scripts}["route_run.py"])

    def test_a_script_that_breaks_the_rule_is_an_error_and_nothing_is_written(self):
        self.put("bare.py", "import sys\n")
        self.put("short.py", '"""Helper.\n\nUsage: short.py\n"""\n')
        self.put("mute.py", '"""Counts the ore every pilot mined in the last hour.\n\nNo word on how to call it.\n"""\n')
        self.put("broken.py", '"""Never closed\n')
        _scripts, errors = index.read_folder(str(self.root))
        self.assertEqual(errors, ["game/fleet/bare.py: no docstring",
                                  "game/fleet/broken.py: not readable as ASCII Python (SyntaxError)",
                                  "game/fleet/mute.py: the docstring has no `Usage:` block",
                                  "game/fleet/short.py: the docstring's first paragraph does not say what the script does"])
        done = subprocess.run(["python3", "-B", str(SCRIPT), "--root", str(self.root)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("ERROR: game/fleet/bare.py: no docstring", done.stdout)
        self.assertFalse((self.fleet / "index.md").exists())


class IndexTests(Tree):
    def build(self, now=1_800_000_001):
        scripts, errors = index.read_folder(str(self.root))
        self.assertEqual(errors, [])
        return scripts, index.write(str(self.root), scripts, now)

    def test_the_index_lists_every_script_and_its_calls(self):
        scripts, written = self.build()
        self.assertTrue(written)
        text = self.text()
        self.assertTrue(text.startswith("---\nname: fleet-index\nid: "))
        self.assertIn("never edited by hand. Scripts listed: 3.", text)
        rows = [line for line in text.splitlines() if line.startswith("| `")]
        self.assertEqual(rows, ["| `dispatch.py` | Keep every pilot at work: one task per free pilot. | Service |",
                                "| `gate.py` | Small client for the engine's gate / no proxy. | By hand |",
                                "| `route_run.py` | Fly one pilot along a route file: dock at each stop and do what the stop says. | Runner (`circuit` routes) |"])
        self.assertIn("### `route_run.py`\n\nFly one pilot along a route file: dock at each stop and do what the stop says. A second\nsentence.\n\n"
                      "A runner: the dispatcher starts it for a route of the kind `circuit`; by hand only for a test with one free pilot.\n\n"
                      "```\nroute_run.py <pilot> <route id> [--from N]\n    [--verbose]\n```\n", text)
        self.assertEqual(index.state(str(self.root), scripts), "current")

    def test_missing_current_stale_and_the_id_is_kept(self):
        scripts, _errors = index.read_folder(str(self.root))
        self.assertEqual(index.state(str(self.root), scripts), "missing")
        self.assertEqual(self.build()[1], True)
        first = self.text()
        self.assertEqual(self.build(now=1_800_000_500)[1], False)                               # unchanged: not rewritten
        self.assertEqual(self.text(), first)
        self.put("tool.py", '"""Counts the ore every pilot mined in the last hour.\n\nUsage: tool.py [--hours N]\n"""\n')
        scripts, _errors = index.read_folder(str(self.root))
        self.assertEqual(index.state(str(self.root), scripts), "stale")
        self.assertEqual(self.build(now=1_800_000_900)[1], True)
        second = self.text()
        self.assertEqual(second.split("\n")[2], first.split("\n")[2])                           # the id line
        self.assertIn("| `tool.py` | Counts the ore every pilot mined in the last hour. | By hand |", second)
        (self.fleet / "index.md").write_text(second.replace("| By hand |", "| By foot |", 1), encoding="ascii")
        self.assertEqual(index.state(str(self.root), scripts), "stale")                         # an edit by hand is caught

    def test_an_id_never_ends_on_a_full_minute(self):
        self.assertEqual(index.new_id(1_800_000_000 - 1_800_000_000 % 60), index.new_id(1_800_000_000 - 1_800_000_000 % 60 - 1))
        self.assertFalse(index.new_id(1_800_000_000 - 1_800_000_000 % 60).endswith("00Z"))


class CommandTests(Tree):
    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "baseline")

    def git(self, *args):
        return subprocess.run(["git"] + list(args), cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout

    def run_script(self, *args):
        return subprocess.run(["python3", "-B", str(SCRIPT), "--root", str(self.root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def test_the_gate_fails_a_missing_and_a_stale_index_and_passes_a_current_one(self):
        done = self.run_script("--check")
        self.assertEqual((done.returncode, done.stdout.splitlines()[0]), (1, "game/fleet/index.md: missing"))
        self.assertEqual(self.run_script().stdout, "game/fleet/index.md: written\n")
        done = self.run_script("--check")
        self.assertEqual((done.returncode, done.stdout), (0, "game/fleet/index.md: current\nErrors: 0 | Warnings: 0\n"))
        self.put("gate.py", GATE.replace("gate.py raw <pilot> <action>", "gate.py raw <pilot> <action> [group]"))
        done = self.run_script("--check")
        self.assertEqual(done.returncode, 1)
        self.assertIn("game/fleet/index.md is stale: run `python3 -B scripts/fleet-index.py`", done.stdout)

    def test_commit_commits_the_index_alone_and_waits_for_a_members_work_in_progress(self):
        (self.root / "notes.txt").write_text("another member's file outside the folder\n", encoding="ascii")
        done = self.run_script("--commit")
        self.assertEqual((done.returncode, done.stdout), (0, "game/fleet/index.md: written\ngame/fleet/index.md: committed\n"))
        self.assertEqual(self.git("show", "--name-only", "--format=", "HEAD").split(), ["game/fleet/index.md"])
        self.assertEqual(self.git("log", "-1", "--format=%an <%ae>").strip(), "Unity <unity@suggi-workspace.dev>")
        self.assertEqual(self.git("status", "--porcelain").strip(), "?? notes.txt")
        self.assertEqual(self.run_script("--commit").stdout, "game/fleet/index.md: current\n")
        self.put("new_tool.py", '"""Half written by another member\n')
        done = self.run_script("--commit")
        self.assertEqual((done.returncode, done.stdout),
                         (0, "game/fleet/index.md: not built; game/fleet holds changes that are not committed: game/fleet/new_tool.py\n"))
        self.assertEqual(self.git("log", "--format=%s").count("rebuilt"), 1)


class RealTests(unittest.TestCase):
    def test_the_repository_index_is_current_and_every_script_keeps_the_rule(self):
        scripts, errors = index.read_folder(str(ROOT))
        self.assertEqual(errors, [])
        self.assertGreaterEqual(len(scripts), 9)
        self.assertEqual(index.state(str(ROOT), scripts), "current", "run `python3 -B scripts/fleet-index.py`")


if __name__ == "__main__":
    unittest.main()
