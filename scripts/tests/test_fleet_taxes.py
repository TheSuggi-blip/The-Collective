"""taxes.py on a disposable data folder: a statement read, kept once, and given back to the run that carried it."""

import calendar
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
import taxes                                       # noqa: E402  the one module every reader shares


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_beside_taxes", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def at(text):
    return calendar.timegm(time.strptime(text, "%Y-%m-%dT%H:%M:%SZ"))


def stamp(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


ASSESSED = at("2026-11-16T12:27:33Z")
ANSWER = ("=== TAX RETURN ===\nLatest completed statement: assessed 2026-11-16T12:27:33.069205645Z; owed %scr; paid %scr; unpaid at assessment 0cr; refund 0cr.\n"
          "Status: ACTIVE\nNext assessment: in ~6d\n")


class TaxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-taxes-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        self.record = self.data / "fleet" / "taxes.json"
        self.once = self.data / "fleet" / "onetime.json"
        self.once.write_text(json.dumps([[ASSESSED - 5000, "miner-1", "First Hunt", 1000], [ASSESSED + 100, "miner-1", "fit: tool bought", -640]]))
        was = os.environ.get("FLEET_TAXES")
        os.environ["FLEET_TAXES"] = str(self.record)                                      # what routes.py and dispatch.py read in this test
        self.addCleanup(os.environ.__setitem__, "FLEET_TAXES", was or os.devnull)
        self.asked = []

    def asker(self, pilot):
        self.asked.append(pilot)
        return {"miner-1": ANSWER % ("4,818", "4,818"), "miner-2": ANSWER % ("3,198", "3,198"), "miner-3": "no statement yet", "miner-4": ANSWER % ("2,000", "2,000")}.get(pilot, "")

    def test_a_statement_is_read_from_the_games_text(self):
        self.assertEqual(taxes.statement(ANSWER % ("4,818", "4,818")), (ASSESSED, 4818))
        self.assertIsNone(taxes.statement("Status: ACTIVE, no completed statement"))
        self.assertIsNone(taxes.statement(""))

    def test_a_pass_keeps_each_pilot_once_and_asks_one_pilot_when_nothing_is_new(self):
        added, unread, asked = taxes.collect(str(self.data), ["miner-1", "miner-2", "miner-3"], asker=self.asker)
        self.assertEqual((sorted(added), unread, asked), ([("miner-1", ASSESSED, 4818), ("miner-2", ASSESSED, 3198)], ["miner-3"], True))
        self.assertEqual(json.loads(self.record.read_text()), {"miner-1": [[ASSESSED, 4818]], "miner-2": [[ASSESSED, 3198]]})
        rows = json.loads(self.once.read_text())
        self.assertEqual([r for r in rows if r[2] == "Weekly tax"], [[ASSESSED, "miner-1", "Weekly tax", -4818], [ASSESSED, "miner-2", "Weekly tax", -3198]])
        self.assertEqual(len(rows), 4)                                                    # the two rows that stood there are kept
        self.assertEqual([r[0] for r in rows], sorted(r[0] for r in rows))                # and the file stays in the order of time
        self.asked.clear()
        self.assertEqual(taxes.collect(str(self.data), ["miner-1", "miner-2", "miner-3"], asker=self.asker), ([], [], False))
        self.assertEqual(self.asked, ["miner-1"])                                         # no new assessment: one pilot asked, no more
        added, _unread, asked = taxes.collect(str(self.data), ["miner-1", "miner-2"], everyone=True, asker=self.asker)
        self.assertEqual((added, asked, len(json.loads(self.once.read_text()))), ([], True, 4))   # asked again: nothing twice

    def test_a_dry_run_writes_nothing(self):
        before = self.once.read_text()
        added, _unread, _asked = taxes.collect(str(self.data), ["miner-1"], dry_run=True, asker=self.asker)
        self.assertEqual((len(added), self.once.read_text(), self.record.exists()), (1, before, False))

    def test_a_run_in_flight_gets_its_tax_back_and_no_other_run_does(self):
        taxes.collect(str(self.data), ["miner-1", "miner-2"], asker=self.asker)
        routes = load("routes")
        spanning = {"route": "ice", "kind": "mine", "pilot": "miner-1", "started": stamp(ASSESSED - 1200), "minutes": 40, "delta": -4500,
                    "credits_before": 9000, "credits_after": 4500}
        self.assertEqual(taxes.in_run(spanning), 4818)
        self.assertEqual(routes.earned(spanning), 318)                                    # the run made +318 cr; the tax is not its loss
        ended_before = dict(spanning, started=stamp(ASSESSED - 3600), minutes=30)
        started_after = dict(spanning, started=stamp(ASSESSED + 400))
        other_pilot = dict(spanning, pilot="miner-9")
        self.assertEqual([taxes.in_run(r) for r in (ended_before, started_after, other_pilot)], [0, 0, 0])
        self.assertEqual(routes.earned(ended_before), -4500)
        ends_at_the_moment = dict(spanning, started=stamp(ASSESSED - 60 * 40 - 60), minutes=40)       # its last wallet reading fell after the tax
        self.assertEqual(taxes.in_run(ends_at_the_moment), 4818)
        self.assertEqual(taxes.in_run({"pilot": "miner-1", "started": None, "minutes": 5}), 0)

    def test_the_loss_stop_does_not_close_a_route_on_the_tax(self):
        taxes.collect(str(self.data), ["miner-1", "miner-2", "miner-4"], asker=self.asker)
        dispatch = load("dispatch")
        routes = {"ice": {"id": "ice", "kind": "mine", "sell": [{"item": "water_ice", "min_price": 20}]}}     # it sells: it is judged on its pay
        now = ASSESSED + 1800
        taxed = lambda pilot, paid, ago: {"route": "ice", "pilot": pilot, "started": stamp(ASSESSED - ago), "minutes": 30, "credits_before": 9000, "credits_after": 9000 + 300 - paid}
        rows = [taxed("miner-1", 4818, 600), taxed("miner-2", 3198, 700), taxed("miner-4", 2000, 900)]
        self.assertEqual(dispatch.losing(routes, rows, now), {})                          # three runs of +300 cr each
        self.assertEqual(dispatch.lately_losing(routes, rows, now), {})
        os.environ["FLEET_TAXES"] = str(self.data / "fleet" / "none.json")                # without the record the same rows close the route
        self.assertEqual(dispatch.losing(routes, rows, now), {"ice": (3, -9116)})
        self.assertEqual(dispatch.lately_losing(routes, rows, now), {"ice": (3, -9116)})


if __name__ == "__main__":
    unittest.main()
