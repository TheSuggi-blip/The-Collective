"""r23, requests ENT-312 (Zero): the pirate stop reads every system a circuit names, each stop's own and those of its
mine and hunt steps; on disposable trees, no engine."""

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
    spec = importlib.util.spec_from_file_location(name + "_circuit_pirates_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LINER = {"id": "liner", "kind": "circuit", "title": "t",
         "stops": [{"at": "beta:core:beta_base", "buy": [{"item": "chemical_liner", "qty": 76, "max_price": 627}], "stop_on_failed_buy": True},
                   {"at": "home:core:base", "sell": [{"item": "chemical_liner", "min_price": 700}]}]}
FORGE = {"id": "forge", "kind": "circuit", "title": "t", "requires": {"empty_hold": True},
         "stops": [{"at": "crucible:garrison:garrison", "accept": ["the_forge_tax"],
                    "mine": [{"at": "sargas:hearsay_cobalt", "for": ["The Forge Tax"], "minutes": 60}]},
                   {"at": "crucible:garrison:garrison", "store": ["cobalt_ore"]}]}
GHOSTS = {"id": "ghosts", "kind": "circuit", "title": "t",
          "stops": [{"at": "home:core:base", "hunt": [{"at": "far:siphon", "species": ["drift_ray"], "kills": 4}]}]}


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-circuit-pirates-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in (self.root / "routes", self.data / "fleet" / "orders", self.data / "routes"):
            folder.mkdir(parents=True)
        self.now = time.time()
        for route in (LINER, FORGE, GHOSTS):
            path = self.root / "routes" / (route["id"] + ".json")
            path.write_text(json.dumps(route), encoding="ascii")
            os.utime(path, (self.now - 3600, self.now - 3600))       # written an hour before the runs below
        self.dispatch = load("dispatch")
        self.routes = self.dispatch.load_routes(self.root)

    def started(self, minutes_ago):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - minutes_ago * 60))

    def why(self, rid, pilot="trader-18", credits=46130, rows=(), pirates=None):
        state = {"now": self.now, "data": str(self.data), "rows": list(rows), "orders": {}, "rest": {}, "booked": {},
                 "root": str(self.root), "pirates": pirates or {}}
        return self.dispatch.why_not({"name": pilot, "credits": credits, "modules": [], "docked": True, "goods": 0}, rid, self.routes[rid], state)[0]


class PirateCircuitTests(Base):
    def test_a_circuit_is_closed_where_pirates_were_seen_at_a_stop_or_a_step(self):
        self.assertIsNone(self.why("forge"))
        self.assertIn("pirates seen in sargas", self.why("forge", pirates={"sargas": self.now - 3600}))       # its mine step (ENT-117)
        self.assertIn("pirates seen in crucible", self.why("forge", pirates={"crucible": self.now - 600}))    # its stop
        self.assertIn("pirates seen in far", self.why("ghosts", pirates={"far": self.now - 600}))            # its hunt step
        self.assertIsNone(self.why("forge", pirates={"elsewhere": self.now - 600}))
        self.assertEqual(self.dispatch.circuit_systems(FORGE), ["crucible", "sargas"])


if __name__ == "__main__":
    unittest.main()
