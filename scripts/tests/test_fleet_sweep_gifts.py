"""game/fleet/wallet.py: a gift is written down `sent` before its call and settled at the next pass from the receiver's
wallet, like a deposit (errors.log ENT-116, DECISIONS Q75 (7)). On a disposable data folder, no engine, no network: the
gate's two calls (give, refresh) are fakes and a cut of the job's `timeout 200` is an exception the fake raises."""

import contextlib
import importlib.util
import io
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
LEADER = "Prime Directive"


class Cut(BaseException):
    """The job's timeout ends the pass here (no `except Exception` catches it)."""


def load():
    spec = importlib.util.spec_from_file_location("wallet_sent_gift_test", FLEET / "wallet.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SentGiftTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-sent-gift-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        (self.data / "empire").mkdir()
        (self.data / "empire" / "empire.json").write_text(json.dumps({"faction": {"leader": LEADER, "treasury": 100000}, "members": []}))
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({LEADER: {"admiral": "Unity", "division": "Command", "role": "command"}}))
        self.wallets = {LEADER: 26000, "miner-1": 90000, "miner-2": 20000}
        self.stamp = None                                        # the wallets' reading time in the fleet file (`state_at`); None: not said
        self.write()
        self.wallet = load()
        self.wallet.SWEEP_ENABLED, self.wallet.PER_PASS, self.wallet.SHOW_WAIT, self.wallet.WAIT = True, 1, 0, 0
        self.wallet.refresh = lambda pilot: None
        self.wallet.treasury_read = lambda pilot: None
        self.calls = []
        os.environ["HERMES_SESSION_PROFILE"] = "unity"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)

    def write(self):
        ships = [dict({"name": n, "credits": c, "status": "connected"}, **({"state_at": self.stamp} if self.stamp else {})) for n, c in self.wallets.items()]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))

    def landing(self, cut=True):
        """A give() that the game takes: the giver's wallet falls, the receiver's rises; with `cut`, the pass ends right after."""
        def give(donor, pilot, credits):
            self.calls.append((donor, pilot, credits))
            self.wallets[donor] -= credits
            self.wallets[pilot] += credits
            self.write()
            if cut:
                raise Cut()
            return True, "ok"
        return give

    def go(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.wallet.main(list(args) + ["--data", str(self.data)])
        return code, out.getvalue()

    def rows(self, name):
        path = self.data / "fleet" / name
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def once(self):
        path = self.data / "fleet" / "onetime.json"
        return json.loads(path.read_text()) if path.exists() else []

    def test_a_sweep_gift_cut_after_it_landed_is_booked_at_the_next_pass_with_its_own_time_and_never_twice(self):
        # ENT-116: the job's `timeout 200` cut a pass after its call had landed and before it was booked
        self.wallet.give = self.landing()
        with self.assertRaises(Cut):
            self.go("sweep")
        self.assertEqual(self.calls, [("miner-1", LEADER, 40000)])
        sent = [r for r in self.rows("sweep.jsonl") if r["kind"] == "gift"]
        self.assertEqual([(r["from"], r["to"], r["credits"], r["state"], r["wallets"]) for r in sent],
                         [("miner-1", LEADER, 40000, "sent", {"miner-1": 90000, LEADER: 26000})])      # on disk before the call
        self.assertEqual((self.once(), self.rows("gifts.jsonl")), ([], []))
        at = sent[0]["at"]
        self.calls.clear()
        self.wallet.give = self.landing(cut=False)
        code, text = self.go("sweep")
        self.assertEqual((code, self.calls), (0, []))                  # miner-1 holds 50,000 now: nothing to give, nothing given twice
        self.assertIn("booked at the next pass: the gift miner-1 -> Prime Directive 40,000 cr sent at", text)
        self.assertEqual([r for r in self.once() if r[2] == "Wallet top-up"], [[at, "miner-1", "Wallet top-up", -40000], [at, LEADER, "Wallet top-up", 40000]])
        self.assertEqual([(g["at"], g["from"], g["to"], g["credits"]) for g in self.rows("gifts.jsonl")], [(at, "miner-1", LEADER, 40000)])
        self.go("sweep")
        self.assertEqual(len([r for r in self.once() if r[2] == "Wallet top-up"]), 2)
        self.assertEqual([r["state"] for r in self.rows("sweep.jsonl") if r["kind"] == "gift"], ["sent", "booked"])

    def test_a_cut_gift_the_wallets_do_not_show_is_kept_unsure_and_its_giver_waits(self):
        def lost(donor, pilot, credits):
            self.calls.append((donor, pilot, credits))
            raise Cut()                                          # cut before the game took it: no wallet moves
        self.wallet.give = lost
        with self.assertRaises(Cut):
            self.go("sweep")
        self.calls.clear()
        self.wallet.give = self.landing(cut=False)
        code, text = self.go("sweep")
        self.assertEqual(code, 1)
        self.assertIn("HALT: the gift miner-1 -> Prime Directive 40,000 cr sent at", text)
        self.assertEqual(self.calls, [])                                 # on cooldown from the time it was sent: not asked again now
        self.assertEqual(self.once(), [])
        self.assertEqual([(g["from"], g["credits"], g["unsure"]) for g in self.rows("gifts.jsonl")], [("miner-1", 0, 40000)])

    def test_a_gift_whose_receiver_was_not_read_since_stays_open_then_unsure_and_a_dry_run_writes_nothing(self):
        self.wallet.give = self.landing()
        with self.assertRaises(Cut):
            self.go("sweep")
        self.stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() - 600))      # a reading from before the call
        self.write()
        code, text = self.go("sweep", "--dry-run")
        self.assertIn("open: the gift miner-1 -> Prime Directive 40,000 cr", text)
        self.assertEqual([r["state"] for r in self.rows("sweep.jsonl")], ["sent"])            # the dry run wrote nothing
        code, text = self.go("sweep")
        self.assertIn("open: the gift miner-1 -> Prime Directive 40,000 cr", text)
        self.assertEqual((self.once(), [r["state"] for r in self.rows("sweep.jsonl")]), ([], ["sent"]))
        self.wallet.SENT_KEEP = 0                                        # its end: an open gift never waits for a hand
        code, text = self.go("sweep")
        self.assertEqual(code, 1)
        self.assertEqual([r["state"] for r in self.rows("sweep.jsonl") if r["kind"] == "gift"], ["sent", "unsure"])

    def test_a_top_up_cut_after_it_landed_is_booked_once_and_not_given_twice(self):
        self.wallets = {"miner-1": 2500, "miner-3": 80000}
        self.write()
        self.wallet.give = self.landing()
        with self.assertRaises(Cut):
            self.go("topup")
        sent = [r for r in self.rows("sweep.jsonl") if r["kind"] == "topup"]
        self.assertEqual([(r["from"], r["to"], r["credits"], r["state"], r["wallets"]) for r in sent],
                         [("miner-3", "miner-1", 17500, "sent", {"miner-3": 80000, "miner-1": 2500})])
        self.calls.clear()
        landed = dict(self.wallets)
        self.wallets, self.stamp = {"miner-1": 2500, "miner-3": 80000}, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() - 600))
        self.write()                                                     # the fleet file still holds the readings from before the call
        code, text = self.go("topup")
        self.assertEqual(self.calls, [])                                 # the old code gave miner-1 a second time here
        self.assertIn("open: the top-up miner-3 -> miner-1 17,500 cr", text)
        self.wallets, self.stamp = landed, None
        self.write()                                                     # read again: the gift shows on both wallets
        code, text = self.go("topup")
        self.assertEqual(self.calls, [])
        self.assertIn("booked at the next pass: the top-up miner-3 -> miner-1 17,500 cr", text)
        self.assertEqual([r[1:] for r in self.once() if r[2] == "Wallet top-up"], [["miner-3", "Wallet top-up", -17500], ["miner-1", "Wallet top-up", 17500]])
        self.go("topup")
        self.assertEqual(len([r for r in self.once() if r[2] == "Wallet top-up"]), 2)

    def test_an_answered_gift_ends_its_sent_row_in_the_same_pass(self):
        self.wallet.give = self.landing(cut=False)
        code, _text = self.go("sweep")
        self.assertEqual(code, 0)
        self.assertEqual([r["state"] for r in self.rows("sweep.jsonl") if r["kind"] == "gift"], ["sent", "booked"])
        self.assertEqual(self.wallet.open_gifts(self.wallet.swept(str(self.data)), "gift"), [])
        self.assertEqual(len([r for r in self.once() if r[2] == "Wallet top-up"]), 2)


if __name__ == "__main__":
    unittest.main()
