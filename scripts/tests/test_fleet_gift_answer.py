"""A sweep gift whose own answer shows the giver's wallet fallen is booked though the fleet file lags (the unsure gift
of 2026-11-22 00:45 UTC). No engine, no network: the gate's calls are fakes."""

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
    spec = importlib.util.spec_from_file_location(name + "_gift_answer_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnsweredGiftTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-r23-gift-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        (self.data / "empire").mkdir()
        (self.data / "empire" / "empire.json").write_text(json.dumps({"faction": {"leader": LEADER, "treasury": 100000}, "members": []}))
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({LEADER: {"admiral": "Unity", "division": "Command", "role": "command"}}))
        ships = [{"name": LEADER, "credits": 26000, "status": "connected"}, {"name": "drone-11", "credits": 61168, "status": "connected"}]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))      # never updated: the engine's copy lags
        self.wallet = load("wallet")
        self.wallet.SWEEP_ENABLED, self.wallet.PER_PASS, self.wallet.SHOW_WAIT, self.wallet.WAIT = True, 1, 0, 0
        self.wallet.KEEP_WORK, self.wallet.SWEEP_WORK = self.wallet.KEEP_SHIP, self.wallet.SWEEP_AT   # one line for every role here
        self.wallet.refresh = lambda pilot: None
        self.wallet.treasury_read = lambda pilot: None
        os.environ["HERMES_SESSION_PROFILE"] = "unity"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)

    def go(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.wallet.main(["sweep", "--data", str(self.data)])
        return code, out.getvalue()

    def test_a_gift_whose_answer_shows_the_giver_wallet_fallen_is_booked_though_the_fleet_file_lags(self):
        answer = '{"result":{"player":{"id":"b3b3","username":"drone-11","empire":"voidborn","credits":50000,"status_message":""'
        self.wallet.give = lambda donor, pilot, credits: (True, answer[:200])
        code, text = self.go()
        self.assertIn("given: drone-11 -> Prime Directive 11,168 cr", text)
        self.assertEqual(code, 0)
        gifts = [json.loads(line) for line in (self.data / "fleet" / "gifts.jsonl").read_text().splitlines()]
        self.assertEqual([(g["from"], g["credits"]) for g in gifts], [("drone-11", 11168)])

    def test_an_answer_that_does_not_show_it_still_keeps_the_gift_unsure(self):
        self.assertFalse(self.wallet.answer_shows('{"result":{"player":{"username":"drone-11","credits":61168', "drone-11", 61168, 11168))
        self.assertFalse(self.wallet.answer_shows('{"result":{"player":{"username":"drone-12","credits":50000', "drone-11", 61168, 11168))
        self.assertFalse(self.wallet.answer_shows("ok", "drone-11", 61168, 11168))
        self.assertTrue(self.wallet.answer_shows('{"result":{"player":{"username":"drone-11","credits":50000', "drone-11", 61168, 11168))



if __name__ == "__main__":
    unittest.main()
