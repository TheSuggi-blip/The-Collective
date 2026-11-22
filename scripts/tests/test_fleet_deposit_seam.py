"""game/fleet/routes.py moved and earned: the leader's deposit into the faction's treasury that falls near a run's start
is weighed after the moves that fall well inside the run, so a deposit and a gift of the same run net out (requests
ENT-359, Apophis). The records are the live ones of 2026-11-22: Prime Directive's hunt of 13:13:07 UTC deposited
23,198 cr eleven seconds in and took a gift of 12,008 cr six minutes in; it read -23,558 cr where it spent about 360 cr
of fuel. On a disposable data folder. No engine, no network.
"""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
LEADER = "Prime Directive"
HUNT = {"route": "hunt-harborlight-ice-shelf-hollow-pilgrim", "kind": "hunt", "pilot": LEADER, "started": "2026-11-22T13:13:07Z",
        "minutes": 23.7, "credits_before": 73198, "credits_after": 61648, "delta": -11550, "one_time": 0, "kills": 0,
        "goods": {}, "sold": {}, "notes": []}
GIFTS = [{"at": 1795352731, "from": "trader-19", "to": LEADER, "credits": 13586},      # 13:05:31, landed before the run
         {"at": 1795352810, "from": "trader-31", "to": LEADER, "credits": 10163},      # 13:06:50, landed before the run
         {"at": 1795353553, "from": "trader-4", "to": LEADER, "credits": 12008}]       # 13:19:13, well inside the run
DEPOSIT = [1795353198, LEADER, "Faction treasury: credits deposited (the Collective keeps them)", -23198]   # 13:13:18


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_deposit_seam_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DepositSeamTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-deposit-seam-test-")
        self.addCleanup(self.temp.cleanup)
        self.fleet = Path(self.temp.name) / "data" / "fleet"
        (Path(self.temp.name) / "data" / "routes").mkdir(parents=True)
        self.fleet.mkdir(parents=True)
        os.environ["FLEET_TAXES"] = str(self.fleet / "taxes.json")                 # routes reads the files beside the tax record
        self.addCleanup(os.environ.__setitem__, "FLEET_TAXES", os.devnull)
        self.routes = load("routes")

    def books(self, gifts, deposits):
        (self.fleet / "gifts.jsonl").write_text("".join(json.dumps(g) + "\n" for g in gifts))
        (self.fleet / "onetime.json").write_text(json.dumps(deposits))
        (Path(self.temp.name) / "data" / "routes" / "runs.jsonl").write_text(json.dumps(HUNT) + "\n")

    def test_a_deposit_at_the_start_nets_out_against_a_gift_inside_the_run(self):
        self.books(GIFTS, [DEPOSIT])
        self.assertEqual(self.routes.moved(HUNT), 23198 - 12008)                    # it read -12,008
        self.assertEqual(round(self.routes.earned(HUNT)), -360)                     # it read -23,558

    def test_a_seam_deposit_alone_is_weighed_as_before(self):
        self.books([], [DEPOSIT])
        self.assertEqual(self.routes.moved(dict(HUNT, credits_after=50000, delta=-23198)), 23198)   # it brings the change to nothing
        self.assertEqual(self.routes.moved(HUNT), 0)                                # it does not: left out, as before

    def test_a_gift_well_inside_still_counts_without_a_deposit(self):
        self.books(GIFTS, [])
        self.assertEqual(self.routes.moved(dict(HUNT, credits_after=85206, delta=12008)), -12008)


if __name__ == "__main__":
    unittest.main()
