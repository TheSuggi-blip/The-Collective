"""gate.release ends a hand hold and clears the member's own want token (requests ENT-526, ENT-527; errors ENT-199).

Since 9396c21c release() called division.file_name, which division.py does not define: every release of a hand
hold removed the hold, then raised AttributeError and left the want file. On a disposable data tree; no engine.
"""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name, FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-gate-release-test-")
        self.data = Path(self.temp.name)
        (self.data / "fleet" / "orders").mkdir(parents=True)
        (self.data / "fleet" / "want").mkdir(parents=True)
        self.saved = {k: os.environ.get(k) for k in ("HERMES_SESSION_PROFILE", "HERMES_HOME", "HERMES_SCRATCH_DIR", "TMPDIR", "FLEET_MEMBER")}
        for key in self.saved:
            os.environ.pop(key, None)
        os.environ["HERMES_SESSION_PROFILE"] = "zero"
        sys.path.insert(0, str(FLEET))
        self.division = load("division")
        self.division.DATA = str(self.data)
        self.gate = load("gate")
        self.gate.division = self.division

    def tearDown(self):
        sys.path.remove(str(FLEET))
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self.temp.cleanup()

    def hold(self, pilot, by):
        path = self.data / "fleet" / "orders" / (pilot + ".json")
        path.write_text(json.dumps({"pilot": pilot, "what": "hand " + by}))
        return path

    def want(self, pilot, by):
        path = self.data / "fleet" / "want" / (pilot + ".json")
        path.write_text(json.dumps({"pilot": pilot, "by": by, "why": "commission a hull"}))
        return path

    def test_release_ends_the_hold_and_clears_the_member_s_own_want(self):
        hold, want = self.hold("miner-1", "Zero"), self.want("miner-1", "Zero")
        self.assertEqual(self.gate.release("miner-1"), "released: miner-1")
        self.assertFalse(hold.exists())
        self.assertFalse(want.exists())

    def test_release_leaves_another_member_s_want(self):
        hold, want = self.hold("miner-2", "Zero"), self.want("miner-2", "Unity")
        self.assertEqual(self.gate.release("miner-2"), "released: miner-2")
        self.assertFalse(hold.exists())
        self.assertTrue(want.exists())

    def test_release_without_a_want_file_still_releases(self):
        hold = self.hold("miner-3", "Zero")
        self.assertEqual(self.gate.release("miner-3"), "released: miner-3")
        self.assertFalse(hold.exists())

    def test_release_of_another_member_s_hold_changes_nothing(self):
        hold = self.hold("miner-4", "Apophis")
        self.assertIn("carries no hand hold of yours", self.gate.release("miner-4"))
        self.assertTrue(hold.exists())


if __name__ == "__main__":
    unittest.main()
