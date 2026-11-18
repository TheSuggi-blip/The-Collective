"""game/fleet/routes.py moved and earned at a run's seam: a gift of the wallet sweep names the giver's wallet after it
(data/fleet/sweep.jsonl), and the run that ended on that figure gave it (requests ENT-264, Apophis). The records are
the live ones of 2026-11-17 (drone-17's hunt that sold 10,717 cr and was swept to 50,000 at its end), on a disposable
data folder. No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
GIFT = {"at": 1794955309, "from": "drone-17", "to": "Prime Directive", "credits": 13220}       # 2026-11-17 22:41:49 UTC
ANSWER = ('{"result":{"player":{"id":"b1e9e35ce4cf1765da1a62771c16cf31","username":"drone-17","empire":"voidborn","credits":50000,'
          '"status_message":"","clan_tag":"","primary_color":"#FFFFFF","secondary_color":"#0')         # the sweep row's text, cut at 200 as wallet.note cuts it
SWEPT = {"at": 1794955309, "credits": 13220, "from": "drone-17", "kind": "gift", "state": "booked", "text": ANSWER, "to": "Prime Directive"}
HUNT = {"route": "hunt-sandrift-ice-fields-hollow-pilgrim", "kind": "hunt", "pilot": "drone-17", "started": "2026-11-17T21:46:43Z", "minutes": 55.4,
        "credits_before": 52793, "credits_after": 50000, "delta": -2793, "one_time": 0, "kills": 4,
        "goods": {"crystal_melt": 3, "creature_carapace": 7, "raw_xeno_meat": 4}, "sold": {"crystal_melt": [7, 1531, 10717]}, "notes": []}
NEXT = {"route": "gather-schedar-belt", "kind": "mine", "pilot": "drone-17", "started": "2026-11-17T22:42:31Z", "minutes": 49.7,
        "credits_before": 50000, "credits_after": 49714, "delta": -286, "one_time": 0, "ore": 26, "sold": {}, "notes": []}


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_seam_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SweepSeamTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-sweep-seam-test-")
        self.addCleanup(self.temp.cleanup)
        self.fleet = Path(self.temp.name) / "data" / "fleet"
        (Path(self.temp.name) / "data" / "routes").mkdir(parents=True)
        self.fleet.mkdir(parents=True)
        os.environ["FLEET_TAXES"] = str(self.fleet / "taxes.json")                 # routes reads the files beside the tax record
        self.addCleanup(os.environ.__setitem__, "FLEET_TAXES", os.devnull)
        self.routes = load("routes")

    def books(self, gifts, swept):
        (self.fleet / "gifts.jsonl").write_text("".join(json.dumps(g) + "\n" for g in gifts))
        (self.fleet / "sweep.jsonl").write_text("".join(json.dumps(s, sort_keys=True) + "\n" for s in swept))

    def test_the_sweep_gift_at_the_seam_is_the_run_s_that_ended_on_the_sweep_s_keep(self):
        self.books([GIFT], [SWEPT])
        self.assertEqual((self.routes.moved(HUNT), round(self.routes.earned(HUNT))), (13220, 4303))    # it read 0 and -8,917
        self.assertEqual((self.routes.moved(NEXT), self.routes.earned(NEXT)), (0, -286))               # the run that began on 50,000 did not give it

    def test_a_gift_is_nobody_s_earning_on_either_side(self):
        self.books([GIFT], [SWEPT])
        leader = {"route": "park", "kind": "circuit", "pilot": "Prime Directive", "started": "2026-11-17T22:20:00Z", "minutes": 45,
                  "credits_before": 50000, "credits_after": 63220, "delta": 13220, "one_time": 0, "notes": []}
        self.assertEqual((self.routes.moved(leader), self.routes.earned(leader)), (-13220, 0))         # the receiver's run earned nothing by it
        plain = dict(HUNT, kind="circuit", sold={})                                                      # the giver's run: what the wallet moved, the gift taken out
        self.assertEqual(self.routes.earned(plain), -2793 + 13220)

    def test_two_sweeps_in_one_run_are_both_its_own(self):
        # Hades, 2026-11-17 23:16:25 UTC, 101.5 minutes: swept 34,628 cr seven minutes in, sold platinum for 18,550 cr, swept 17,686 cr three
        # seconds after its end; it read 0 cr earned
        name = "Hades"
        run = {"route": "mine-gsc-0049-platinum-group-reef", "kind": "mine", "pilot": name, "started": "2026-11-17T23:16:25Z", "minutes": 101.5,
               "credits_before": 84628, "credits_after": 50000, "delta": -34628, "one_time": 0, "ore": 207, "sold": {"platinum_ore": [53, 18550]}, "notes": []}
        gifts = [{"at": 1794957833, "from": name, "to": "Prime Directive", "credits": 34628}, {"at": 1794963478, "from": name, "to": "Prime Directive", "credits": 17686}]
        text = ANSWER.replace("drone-17", name)
        self.books(gifts, [dict(SWEPT, at=g["at"], credits=g["credits"], **{"from": name, "text": text}) for g in gifts])
        self.assertEqual(self.routes.earned(run), 17686)

    def test_without_the_sweep_s_row_or_with_another_wallet_the_seam_rule_stays_as_it_was(self):
        self.books([GIFT], [])
        self.assertEqual(self.routes.moved(HUNT), 0)                                                     # no row: the old test of the seam
        self.books([GIFT], [dict(SWEPT, text=ANSWER.replace('"credits":50000', '"credits":51000'))])
        self.assertEqual(self.routes.moved(HUNT), 0)                                                     # the run ended on another figure
        self.books([GIFT], [dict(SWEPT, text=ANSWER.replace('"username":"drone-17"', '"username":"drone-18"'))])
        self.assertEqual(self.routes.moved(HUNT), 0)                                                     # the answer names another pilot's wallet
        self.books([GIFT], [dict(SWEPT, state="unsure")])
        self.assertEqual(self.routes.moved(HUNT), 0)                                                     # a gift the sweep did not book
        both = dict(NEXT, credits_after=50000, delta=0)                                                  # began and ended on 50,000: the old rule decides
        self.books([GIFT], [SWEPT])
        self.assertEqual(self.routes.moved(both), 0)


if __name__ == "__main__":
    unittest.main()
