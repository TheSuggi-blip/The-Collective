"""game/fleet/stop_pilot.py and route_run.py per-pilot stop tests. No engine, no network."""

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("FLEET_TAXES", os.devnull)

REPO = Path(__file__).resolve().parents[2]


def load_mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class StopPilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="fleet-stop-test-")
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name)
        (self.data / "fleet" / "host" / "running").mkdir(parents=True)
        (self.data / "fleet" / "orders").mkdir(parents=True)
        (self.data / "fleet" / "flagships.json").write_text("{}", encoding="ascii")
        self.sp = load_mod("stop_pilot_under_test", "game/fleet/stop_pilot.py")

    def add_hosted(self, pilot, what):
        jname = self.sp.runhost.job_file(pilot)
        (self.data / "fleet" / "host" / "running" / jname).write_text(
            json.dumps({"pilot": pilot, "what": what, "script": "route_run.py", "since": "2026-11-23T09:00:00Z"}),
            encoding="ascii",
        )

    def add_standalone(self, pilot, what):
        (self.data / "fleet" / "orders" / (pilot + ".json")).write_text(
            json.dumps({"pilot": pilot, "what": what, "since": "2026-11-23T09:00:00Z"}),
            encoding="ascii",
        )

    def test_stops_only_named_hosted_pilot_and_enforces_division_ownership(self):
        self.add_hosted("miner-14", "circuit bad-nebula-loop")
        self.add_hosted("miner-15", "circuit good-ore-loop")
        self.add_hosted("trader-3", "circuit bad-nebula-loop")
        os.environ["HERMES_SESSION_PROFILE"] = "zero"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)

        rc = self.sp.main(["miner-14", "--data", str(self.data)])
        self.assertEqual(rc, 0)
        self.assertTrue((self.data / "fleet" / "host" / "stop" / "miner-14").exists())
        self.assertFalse((self.data / "fleet" / "host" / "stop" / "miner-15").exists())
        self.assertFalse((self.data / "fleet" / "STOP").exists())

        rc_bad = self.sp.main(["trader-3", "--data", str(self.data)])
        self.assertEqual(rc_bad, 1)
        self.assertFalse((self.data / "fleet" / "host" / "stop" / "trader-3").exists())

        rc_trav = self.sp.main(["../STOP", "--data", str(self.data)])
        self.assertEqual(rc_trav, 1)
        self.assertFalse((self.data / "fleet" / "STOP").exists())

    def test_route_batch_stops_only_own_division_ships_on_that_route(self):
        self.add_hosted("miner-1", "circuit wrong-cross")
        self.add_hosted("miner-2", "circuit wrong-cross")
        self.add_hosted("miner-3", "mine good-belt")
        self.add_hosted("trader-1", "circuit wrong-cross")
        os.environ["HERMES_SESSION_PROFILE"] = "zero"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)

        rc = self.sp.main(["--route", "wrong-cross", "--data", str(self.data)])
        self.assertEqual(rc, 0)
        self.assertTrue((self.data / "fleet" / "host" / "stop" / "miner-1").exists())
        self.assertTrue((self.data / "fleet" / "host" / "stop" / "miner-2").exists())
        self.assertFalse((self.data / "fleet" / "host" / "stop" / "miner-3").exists())
        self.assertFalse((self.data / "fleet" / "host" / "stop" / "trader-1").exists())

    def test_standalone_run_writes_per_pilot_stop_and_idle_writes_nothing(self):
        self.add_standalone("hauler-9", "circuit carry-iron")
        os.environ["HERMES_SESSION_PROFILE"] = "apollo"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)

        self.assertEqual(self.sp.main(["hauler-9", "--data", str(self.data)]), 0)
        self.assertTrue((self.data / "fleet" / "stop" / "hauler-9").exists())
        self.assertEqual(self.sp.main(["hauler-99", "--data", str(self.data)]), 0)
        self.assertFalse((self.data / "fleet" / "stop" / "hauler-99").exists())
        self.assertFalse((self.data / "fleet" / "host" / "stop" / "hauler-99").exists())

    def test_route_run_checks_sleep_zero_and_records_systemexit_stop_reason(self):
        src = (REPO / "game" / "fleet" / "route_run.py").read_text(encoding="ascii")
        self.assertIn("def stop_reason():", src)
        self.assertIn("time.sleep(0)", src)
        self.assertIn("except SystemExit as leave:", src)
        self.assertIn("stopped by per-pilot stop file", src)


if __name__ == "__main__":
    unittest.main()
