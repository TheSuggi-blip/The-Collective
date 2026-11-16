"""game/fleet/wallet.py and the dispatcher's wallet floor on a disposable data folder: no ship of ours goes broke. No engine."""

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


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_beside_wallet", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WalletTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-wallet-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        self.put({"miner-1": 2500, "miner-2": 9000, "miner-3": 80000, "miner-4": 35000, "trader-1": 5000, "trader-2": 31000, "Prime Directive": 90000})
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({"Prime Directive": {"admiral": "Unity", "division": "Command", "role": "command"}}))
        (self.data / "fleet" / "onetime.json").write_text(json.dumps([[1, "miner-3", "First Hunt", 1000]]))
        self.wallet = load("wallet")

    def put(self, credits):
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": n, "credits": c} for n, c in credits.items()]}))

    def test_each_low_wallet_is_topped_up_by_the_richest_of_its_division_and_never_twice(self):
        rows = self.wallet.wallets(str(self.data))
        gifts = self.wallet.plan_gifts(rows, {})
        self.assertEqual(gifts, [("miner-3", "miner-1", 17500), ("Prime Directive", "trader-1", 15000), ("miner-3", "miner-2", 11000)])  # lowest first; trader-2 would go under 30,000
        sent = []
        self.wallet.give = lambda donor, pilot, credits: (sent.append((donor, pilot, credits)) or True, "ok")
        os.environ["HERMES_SESSION_PROFILE"] = "unity"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)
        self.assertEqual(self.wallet.main(["topup", "--data", str(self.data)]), 0)
        self.assertEqual(sent, gifts)
        rows = json.loads((self.data / "fleet" / "onetime.json").read_text())
        tops = [r[1:] for r in rows if r[2] == "Wallet top-up"]
        self.assertEqual(tops[:2], [["miner-3", "Wallet top-up", -17500], ["miner-1", "Wallet top-up", 17500]])
        self.assertEqual(sum(r[3] for r in rows if r[2] == "Wallet top-up"), 0)               # the fleet's money does not move
        sent.clear()
        self.wallet.main(["topup", "--data", str(self.data)])                                  # the wallets still read low: no second gift
        self.assertEqual(sent, [])

    def test_the_check_names_a_pilot_under_the_floor_and_a_member_tops_up_nothing(self):
        self.assertEqual(self.wallet.main(["check", "--data", str(self.data)]), 1)
        os.environ["HERMES_SESSION_PROFILE"] = "zero"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)
        with self.assertRaises(SystemExit) as stop:
            self.wallet.main(["topup", "--data", str(self.data)])
        self.assertIn("REFUSED", str(stop.exception))

    def test_the_dispatcher_sends_a_pilot_under_5000_only_on_work_that_pays(self):
        dispatch = load("dispatch")
        state = {"now": time.time(), "data": str(self.data), "rows": [], "orders": {}, "rest": {}, "booked": {}, "loss": {}, "late": {}}
        pilot = {"name": "miner-1", "role": "miner", "credits": 2500, "docked": True, "modules": [], "skills": {}, "goods": 0}
        pays = {"id": "ice", "kind": "mine", "belt": "a:b", "station": "a:b:c", "sell": [{"item": "ice", "min_price": 1}],
                "measured": {"date": "d", "runs": 3, "minutes": 30, "credits_per_run": 500, "cph_per_ship": 1000}}
        gather = {"id": "gather", "kind": "mine", "belt": "a:b", "station": "a:b:c", "standing": True}
        test = {"id": "test", "kind": "circuit", "stops": [{"at": "a:b:c"}]}
        self.assertIsNone(dispatch.why_not(pilot, "ice", pays, state)[0])
        self.assertEqual(dispatch.why_not(pilot, "gather", gather, state)[0], "wallet below 5,000 cr: only work that pays")
        self.assertEqual(dispatch.why_not(pilot, "test", test, state)[0], "wallet below 5,000 cr: only work that pays")
        self.assertIsNone(dispatch.why_not(dict(pilot, credits=5000), "gather", gather, state)[0])


if __name__ == "__main__":
    unittest.main()
