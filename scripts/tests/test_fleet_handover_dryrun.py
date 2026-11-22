"""r23, requests ENT-318: a hunt's hand-over dry run says it gives the hold at the run's end, not the storage; no engine,
no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
LEADER = "Prime Directive"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_r23_small_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HuntGiftDryRunTests(unittest.TestCase):
    def test_a_hunt_gift_dry_run_says_it_gives_the_hold_not_the_storage(self):
        temp = tempfile.TemporaryDirectory(prefix="fleet-r23-handover-test-")
        self.addCleanup(temp.cleanup)
        root, data = Path(temp.name) / "game", Path(temp.name) / "data"
        (root / "routes").mkdir(parents=True)
        (data / "stock").mkdir(parents=True)
        (data / "fleet").mkdir(parents=True)
        route = {"id": "hunt-x", "kind": "hunt", "title": "t", "place": "far:belt", "sell_at": "home:core:base", "species": ["carapace"], "gift_to": "trader"}
        (root / "routes" / "hunt-x.json").write_text(json.dumps(route))
        (data / "stock" / "storage.json").write_text(json.dumps({"pilots": {"drone-1": {"read_at": "2026-11-22T00:00:00Z", "stations": {"base": {"iron_ore": 900, "steel_plate": 40}}}}}))
        handover = load("handover")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            handover.dry_run(str(root), str(data), "hunt-x", "drone-1")
        self.assertIn("source cargo", out.getvalue())
        self.assertNotIn("iron_ore", out.getvalue())


if __name__ == "__main__":
    unittest.main()
