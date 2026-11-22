"""game/fleet/fill.py why_lines: `fill.py status --why <pilot>` prints, for one pilot, every route of its whole list in
order with the reason dispatch.why_not closes it now, or `open`, and which one it flies (Zero's report and Mercury's,
2026-11-22: each wrote the same scratch loop to learn why working ships took a training loop). Pure: survey's answer
is a small dict, dispatch's rule is replaced by a fake. No engine, no network.
"""

import importlib.util
import os
from pathlib import Path
import sys
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)
FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_why_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WhyTests(unittest.TestCase):
    def setUp(self):
        self.fill = load("fill")
        for attr in ("why_not", "pilot_of", "role_of"):
            self.addCleanup(setattr, self.fill.dispatch, attr, getattr(self.fill.dispatch, attr))
        closed = {"gather-a": "the field is at its floor", "train-loop": None, "park": None}
        self.fill.dispatch.why_not = lambda pilot, rid, route, state: (closed.get(rid), None)
        self.fill.dispatch.pilot_of = lambda ship, named, data, ammo: {"name": ship["name"]}
        self.fill.dispatch.role_of = lambda name, named: "miner"
        routes = {rid: {"id": rid} for rid in closed}
        self.seen = {"data": "/nowhere", "named": {}, "routes": routes, "roles": {"miner": ["gather-a", "train-loop", "park"]}, "own": {},
                     "state": {"orders": {"miner-1": "mine train-loop"}}, "by_route": {}, "played": {},
                     "fleet": {"ships": [{"name": "miner-1", "status": "connected"}]}}

    def test_every_route_of_the_list_with_its_reason_and_the_one_flown(self):
        lines = self.fill.why_lines(self.seen, "miner-1")
        self.assertEqual(lines[0], "WHY miner-1 | role miner | flies train-loop | 3 routes in its list, in order")
        self.assertEqual(lines[1:], ["   1 gather-a                                 closed: the field is at its floor",
                                     "   2 train-loop                               open  <- flies it now",
                                     "   3 park                                     open"])

    def test_an_unknown_pilot_is_said_plainly(self):
        self.assertEqual(self.fill.why_lines(self.seen, "miner-99"), ["WHY miner-99: no ship of that name in fleet.json"])


if __name__ == "__main__":
    unittest.main()
