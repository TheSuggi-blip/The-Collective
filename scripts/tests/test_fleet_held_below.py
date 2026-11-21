"""The route field `requires.held_below` (Zero, errors.log ENT-111, DECISIONS Q75 (1)): a mine route opens only while the
division stores less of its good; the dispatcher's rule says so (and with it fill.py), a book that is not whole decides
nothing, routes.py check reads the field. On a disposable data folder; no engine, no network.

2026-11-21: six miners took Central Nexus ice routes on a bid of 371 units while Mining stored 18,541 water ice."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))

ROUTE = {"id": "mine-ice", "kind": "mine", "title": "t", "belt": "achernar:frost_ring", "station": "home:core:central_nexus",
         "sell": [{"item": "water_ice", "min_price": 20}], "requires": {"held_below": {"item": "water_ice", "units": 3000}}}


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_held_below_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HeldBelowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-held-below-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "stock").mkdir()
        (self.data / "fleet").mkdir()
        self.now = time.time()
        self.dispatch = load("dispatch")
        self.gate = sys.modules.get("heldgate") or __import__("heldgate")       # the module dispatch.why_not asks
        self.addCleanup(setattr, self.gate, "ON", self.gate.ON)
        self.gate.ON = True

    def put(self, stored, aboard=0, whole=True, age=0):
        written = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - age))
        (self.data / "stock" / "storage.json").write_text(json.dumps({"updated_at": written, "pilots": {},
            "whole": {"pilots": 100, "held": 100 if whole else 40, "whole": whole},
            "totals": {"by_member": {"Zero": {"central_nexus": {"water_ice": stored - 541}, "synchrony_hub": {"water_ice": 541}}, "Mercury": {"central_nexus": {"water_ice": 99999}}},
                       "holds_by_member": {"Zero": {"water_ice": aboard}}}}))

    def why(self, route=ROUTE, rows=()):
        state = {"now": self.now, "data": str(self.data), "rows": list(rows), "orders": {}, "rest": {}, "booked": {}, "loss": {}, "late": {}, "pirates": {}}
        pilot = {"name": "miner-1", "role": "miner", "credits": 90000, "docked": True, "modules": [], "skills": {}, "goods": 0}
        return self.dispatch.why_not(pilot, route["id"], route, state)[0]

    def test_a_mine_route_stays_shut_while_the_division_stores_its_good_above_the_number(self):
        self.put(18541)
        self.assertEqual(self.why(), "held_below: Zero holds 18,541 water_ice, at or above 3,000")
        self.put(2000, aboard=999)                                             # storage and holds together: 2,999
        self.assertIsNone(self.why())
        self.put(2000, aboard=1000)
        self.assertEqual(self.why(), "held_below: Zero holds 3,000 water_ice, at or above 3,000")
        other = dict(ROUTE, requires={"held_below": {"item": "water_ice", "units": 3000, "division": "Trade"}})
        self.assertEqual(self.why(other), "held_below: Mercury holds 99,999 water_ice, at or above 3,000")   # a division named counts its own

    def test_a_book_that_is_not_whole_closes_nothing_and_opens_nothing_new(self):
        self.put(10, whole=False)
        self.assertTrue(self.why().startswith("held_below: the storage book is not whole (40 of 100 pilots held)"))
        flew = {"route": "mine-ice", "pilot": "miner-1", "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - 1800))}
        self.assertIsNone(self.why(rows=[flew]))                                # it keeps the pilot that flew it within two hours
        self.put(10, age=4 * 3600)                                             # a book four hours old counts as not whole
        self.assertTrue(self.why().startswith("held_below: the storage book is not whole (written 4.0 hours ago)"))

    def test_off_the_field_keeps_its_route_shut_and_the_route_gate_reads_the_field(self):
        self.gate.ON = False                                                    # the state the module ships in
        self.put(10)
        self.assertEqual(self.why(), "held_below: the gate is off (heldgate.ON)")
        self.assertEqual(self.gate.faults({"item": "water_ice", "units": 3000}), [])
        self.assertEqual(self.gate.faults({"item": "water_ice", "units": 0, "division": "Navy", "at": "x"}), [
            "`requires.held_below` of water_ice needs `units`, a whole number of 1 or more",
            "`requires.held_below` of water_ice: `division` must be a division (Command, Intel, Logistics, Military, Mining, Trade) or its Admiral",
            "`requires.held_below` of water_ice names fields no reader knows: at"])
        source = (FLEET / "routes.py").read_text(encoding="ascii")
        self.assertIn('__import__("heldgate").faults(need["held_below"])', source)
        blueprint = (FLEET.parent / "routes" / "BLUEPRINT.md").read_text(encoding="ascii")
        self.assertIn("| `requires.held_below` |", blueprint)


if __name__ == "__main__":
    unittest.main()
