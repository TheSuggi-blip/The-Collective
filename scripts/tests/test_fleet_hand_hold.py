"""A runner never writes its order over a fresh hand hold (requests ENT-289), on disposable trees; no engine, no network.

2026-11-21: a drone was taken by hand (gate.take) at 20:06:15 UTC, while a pass of the dispatcher that had read the order
files at its start was still running; at 20:06:21 UTC the pass wrote the drone's order over the hold and started a hunt,
whose runner removed the order file at its end. The next hunt left the dock between the hand's uninstall_mod and
install_mod, and the drone flew without a weapon.
"""

import ast
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test_hold", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Flying:
    """A runner process that has not ended, as the dispatcher's reaping sees it."""

    def poll(self):
        return None


class PassTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-hand-hold-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.root / "fleet", self.data / "fleet" / "orders", self.data / "routes"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nhome\tHome\t0\t0\tvoidborn\nfar\tFar\t1\t0\tvoidborn\n", encoding="ascii")
        route = {"id": "mine", "kind": "mine", "title": "t", "belt": "far:belt", "station": "home:core:base", "max_ships": 2}
        (self.root / "routes" / "mine.json").write_text(json.dumps(route), encoding="ascii")
        (self.root / "routes" / "plans" / "miner.json").write_text(json.dumps({"role": "miner", "owner": "Zero", "routes": ["mine"]}), encoding="ascii")
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [
            {"name": n, "status": "connected", "credits": 9000, "activity": {"kind": "idle"}} for n in ("miner-1", "miner-2")]}))
        self.dispatch = load("dispatch")
        self.spawned = []
        self.dispatch.spawn = lambda argv, log, env: self.spawned.append((argv, str(log), env)) or Flying()
        self.order = lambda pilot: json.loads((self.data / "fleet" / "orders" / (pilot + ".json")).read_text())["what"]

    def hold(self, pilot, mark="hand Zero"):
        path = self.data / "fleet" / "orders" / (pilot + ".json")
        path.write_text(json.dumps({"pilot": pilot, "what": mark, "since": "2026-11-21T20:06:15Z"}))
        return path

    def real_pass(self):
        return self.dispatch.one_pass(str(self.root), str(self.data), False, [])

    def test_a_pilot_taken_by_hand_during_the_pass_keeps_its_hold_and_is_not_started(self):
        real = self.dispatch.pick

        def taken_meanwhile(pilot, plan, routes, state):                     # gate.take while the pass runs, after its read
            if pilot["name"] == "miner-1":
                self.hold("miner-1")
            return real(pilot, plan, routes, state)

        self.dispatch.pick = taken_meanwhile
        lines = self.real_pass()
        self.assertEqual(self.order("miner-1"), "hand Zero", lines)          # the fault: `mine mine` written over the hold
        self.assertEqual([argv[4] for argv, _log, _env in self.spawned], ["miner-2"])
        self.assertEqual(lines[0], "miner-1: `mine mine` not started: the pilot was taken during this pass (`hand Zero`); it stays so, and gets work when that order ends")
        self.assertEqual(lines[1], "miner-2 -> mine mine")

    def test_the_dispatcher_sends_a_held_pilot_again_only_when_its_hold_ends(self):
        path = self.hold("miner-1")
        self.assertEqual(self.real_pass(), ["miner-2 -> mine mine"])         # a fresh hold: the pilot is not free
        (self.data / "fleet" / "orders" / "miner-2.json").unlink()
        os.utime(path, (time.time() - 21 * 60, time.time() - 21 * 60))      # 20 minutes after its last command the hold ends
        self.assertEqual(self.real_pass(), ["miner-1 -> mine mine", "miner-2 -> mine mine"])
        self.assertEqual(self.order("miner-1"), "mine mine")


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-hand-hold-runner-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet" / "orders").mkdir(parents=True)
        self.division = load("division")

    def put(self, mark, age=0):
        path = self.data / "fleet" / "orders" / "drone-1.json"
        path.write_text(json.dumps({"pilot": "drone-1", "what": mark}))
        os.utime(path, (time.time() - age, time.time() - age))

    def may(self, env):
        return self.division.may("drone-1", str(self.data), env=env)

    def test_a_runner_the_dispatcher_started_refuses_over_a_fresh_hand_hold(self):
        runner = {"FLEET_MEMBER": "dispatch", "FLEET_HOLD": "hunt hunt-home"}
        self.put("hand Apophis")
        ok, why = self.may(runner)
        self.assertFalse(ok, why)                                            # the fault: a service passed over any order file
        self.assertIn("drone-1 is held by hand (`hand Apophis`): the run `hunt hunt-home` does not start", why)
        self.put("hand Apophis", age=21 * 60)
        self.assertTrue(self.may(runner)[0])                                 # a dead hold holds nothing
        self.put("hunt hunt-home")
        self.assertTrue(self.may(runner)[0])                                 # the dispatcher's own order: the run is its own
        self.put("hand Apophis")
        self.assertTrue(self.may({"FLEET_MEMBER": "wallet"})[0])             # a service that is no runner: as before
        self.assertTrue(self.may({"HERMES_SESSION_PROFILE": "apophis"})[0])  # the hand's own member: its own hold
        self.assertFalse(self.may({"HERMES_SESSION_PROFILE": "zero", "FLEET_HOLD": "mine mine"})[0])   # another member: as before
        old = dict(os.environ)
        for key in ("HERMES_SESSION_PROFILE", "HERMES_HOME", "HERMES_SCRATCH_DIR", "TMPDIR"):   # the runner's own shell names no member
            os.environ.pop(key, None)
        os.environ.update(runner)
        try:
            with self.assertRaises(SystemExit) as stop:
                self.division.require("drone-1", str(self.data))
        finally:
            os.environ.clear()
            os.environ.update(old)
        self.assertIn("REFUSED: drone-1 is held by hand", str(stop.exception))

    def test_every_runner_asks_division_before_it_writes_its_order(self):
        for script, write in (("route_run.py", "order('circuit ' + ROUTE['id'])"), ("hunt.py", "order('hunt ' + route_id)"), ("census.py", "ORDER.write_text("),
                              ("mine.py", "with open(order_file, \"w\""), ("guard.py", "    run(opts, call, DATA)")):
            source = (FLEET / script).read_text(encoding="ascii")
            ast.parse(source)
            self.assertIn(write, source, script)
            self.assertLess(source.index("division.require("), source.index(write), script)


if __name__ == "__main__":
    unittest.main()
