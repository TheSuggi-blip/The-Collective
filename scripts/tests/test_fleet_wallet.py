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


class GiveReadsTests(__import__("unittest").TestCase):
    """Q67 (5), requests ENT-220: after a gift the receiver's wallet is read at once, so the next run starts from a wallet that holds it."""

    def test_an_answered_gift_reads_the_receiver_and_a_refused_one_does_not(self):
        import importlib.util
        from pathlib import Path as P
        spec = importlib.util.spec_from_file_location("wallet_give_under_test", P(__file__).resolve().parents[2] / "game" / "fleet" / "wallet.py")
        wallet = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(P(__file__).resolve().parents[2] / "game" / "fleet"))
        spec.loader.exec_module(wallet)
        import gate
        calls, answers = [], [(200, '{"result": "ok"}')]
        saved = gate.call
        gate.call = lambda method, path, body=None, timeout=None: (calls.append((path, (body or {}).get("action"))), answers[0])[1]
        try:
            self.assertTrue(wallet.give("miner-1", "hauler-3", 500)[0])
            self.assertEqual([a for _p, a in calls], ["deposit", "get_status"])
            self.assertIn("hauler-3", calls[1][0])
            calls.clear()
            answers[0] = (500, '{"error": "no"}')
            self.assertFalse(wallet.give("miner-1", "hauler-3", 500)[0])
            self.assertEqual([a for _p, a in calls], ["deposit"])
        finally:
            gate.call = saved


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

    def test_a_gate_that_does_not_answer_ends_no_pass_and_loses_no_record(self):
        # 2026-11-16: a deposit timed out, the pass ended in a fault, and the gifts it had given before were booked nowhere
        calls = []

        def give(donor, pilot, credits):
            calls.append(pilot)
            if len(calls) == 2:
                raise TimeoutError("timed out")
            return True, "ok"
        self.wallet.give, self.wallet.WAIT = give, 0
        os.environ["HERMES_SESSION_PROFILE"] = "unity"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)
        self.assertEqual(self.wallet.main(["topup", "--data", str(self.data)]), 1)             # one gift failed: the pass says so and goes on
        self.assertEqual(calls, ["miner-1", "trader-1", "miner-2"])
        gifts = [json.loads(line) for line in (self.data / "fleet" / "gifts.jsonl").read_text().splitlines()]
        self.assertEqual([(g["from"], g["to"], g["credits"]) for g in gifts if g["credits"]], [("miner-3", "miner-1", 17500), ("miner-3", "miner-2", 11000)])
        self.assertEqual([(g["to"], g["credits"], g["unsure"]) for g in gifts if "unsure" in g], [("trader-1", 0, 15000)])
        rows = json.loads((self.data / "fleet" / "onetime.json").read_text())
        self.assertEqual([r[3] for r in rows if r[2] == "Wallet top-up"], [-17500, 17500, -11000, 11000])
        calls.clear()
        self.wallet.main(["topup", "--data", str(self.data)])                                  # all three on cooldown: none is given twice
        self.assertEqual(calls, [])
        self.put({"miner-1": 2500, "miner-3": 80000, "trader-1": 5000, "Prime Directive": 90000})
        (self.data / "fleet" / "gifts.jsonl").write_text("")

        def late(donor, pilot, credits):                                                       # the gate does not answer, the game took the gift
            self.put({"miner-1": 2500 + credits if pilot == "miner-1" else 2500, "miner-3": 80000, "trader-1": 5000 + credits if pilot == "trader-1" else 5000, "Prime Directive": 90000})
            raise TimeoutError("timed out")
        self.wallet.give = late
        self.wallet.main(["topup", "--data", str(self.data)])
        gifts = [json.loads(line) for line in (self.data / "fleet" / "gifts.jsonl").read_text().splitlines()]
        self.assertEqual([(g["to"], g["credits"]) for g in gifts], [("miner-1", 17500), ("trader-1", 15000)])     # the wallet showed each: booked
        self.put({"miner-1": 2500, "miner-3": 80000})
        (self.data / "fleet" / "gifts.jsonl").write_text("")
        self.wallet.give, self.wallet.BUDGET = give, -1                                         # the pass's seconds are used up: the gift waits for the next pass
        calls.clear()
        self.wallet.main(["topup", "--data", str(self.data)])
        self.assertEqual(calls, [])

    def test_several_ships_give_when_no_one_can_give_the_whole_need_and_the_receiver_is_read_again(self):
        # requests ENT-176 (Mercury): a trader at 298 cr, and no trader could give 19,702 cr and keep 30,000
        self.put({"trader-1": 298, "trader-2": 45000, "trader-3": 40000, "trader-4": 30500, "Prime Directive": 31000})
        rows = self.wallet.wallets(str(self.data))
        gifts = self.wallet.plan_gifts(rows, {})
        self.assertEqual(gifts, [("trader-2", "trader-1", 15000), ("trader-3", "trader-1", 4702)])   # richest first, each above KEEP only
        self.put({"trader-1": 298, "trader-2": 36000, "trader-3": 32000, "Prime Directive": 33500})
        gifts = self.wallet.plan_gifts(self.wallet.wallets(str(self.data)), {})
        self.assertEqual(gifts, [("trader-2", "trader-1", 6000), ("trader-3", "trader-1", 2000), ("Prime Directive", "trader-1", 3500)])
        self.put({"trader-1": 298, "trader-2": 30400, "Prime Directive": 30900})
        self.assertEqual(self.wallet.plan_gifts(self.wallet.wallets(str(self.data)), {}), [])        # under 1,000 to spare: no call
        self.put({"trader-1": 298, "trader-2": 45000, "trader-3": 40000})
        sent, read = [], []
        self.wallet.give = lambda donor, pilot, credits: (sent.append((donor, pilot, credits)) or True, "ok")
        self.wallet.refresh = lambda pilot: read.append(pilot)
        os.environ["HERMES_SESSION_PROFILE"] = "unity"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)
        self.assertEqual(self.wallet.main(["topup", "--data", str(self.data)]), 0)
        self.assertEqual(sent, [("trader-2", "trader-1", 15000), ("trader-3", "trader-1", 4702)])
        self.assertEqual(read, ["trader-1"])                                                      # once, after its last gift
        rows = json.loads((self.data / "fleet" / "onetime.json").read_text())
        self.assertEqual(sum(r[3] for r in rows if r[2] == "Wallet top-up"), 0)

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
        self.assertEqual(dispatch.FLOOR, 0)
        self.assertIsNone(dispatch.why_not(pilot, "ice", pays, state)[0])
        self.assertIsNone(dispatch.why_not(pilot, "gather", gather, state)[0])
        self.assertIsNone(dispatch.why_not(pilot, "test", test, state)[0])
        needs_cash = dict(test, min_credits=5000)
        self.assertEqual(dispatch.why_not(pilot, "test", needs_cash, state)[0], "wallet below 5000 cr")
        self.assertIsNone(dispatch.why_not(dict(pilot, credits=5000), "test", needs_cash, state)[0])


class FundTests(unittest.TestCase):
    """Orders ENT-063 (Unity's block), requests ENT-345/ENT-348: the treasury pays one pilot for a buy (one Recursion
    for Military). The game withdraws from the treasury only while the leader stands docked (2026-11-22 13:58 UTC:
    `not_docked`); the first fund ever takes 1 cr first (rule F12); the sweep and the top-ups leave the fund alone."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-fund-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({"Prime Directive": {"admiral": "Unity", "division": "Command", "role": "command"}}))
        (self.data / "fleet" / "onetime.json").write_text("[]")
        self.wallet = load("wallet")
        self.treasury = [1663512]
        self.calls, self.booked = [], []
        w = self.wallet
        w.FUND_READ = 0
        w.treasury_read = lambda leader: self.treasury[0]

        def withdraw(leader, credits):
            self.calls.append(("withdraw", leader, credits))
            self.treasury[0] -= credits
            return True, '{"result": "ok"}'
        w.withdraw = withdraw
        w.give = lambda donor, pilot, credits: (self.calls.append(("give", donor, pilot, credits)), (True, "ok"))[1]
        w.gate_book = lambda pilot, title, amount: self.booked.append((pilot, title, amount))
        self.put(docked=False)

    def put(self, docked, drone=20000):
        ships = [{"name": "Prime Directive", "credits": 61648, "docked": docked}, {"name": "drone-4", "credits": drone}]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))

    def test_a_fund_waits_for_a_docked_leader_probes_one_credit_then_withdraws_and_gives(self):
        w, now = self.wallet, time.time()
        self.assertEqual(w.add_fund(str(self.data), "drone-4", 315699, "Recursion for Military", 6, now), 0)
        self.assertEqual(w.add_fund(str(self.data), "drone-4", 1000, "twice", 6, now), 1)            # one open fund a pilot
        self.assertEqual(w.serve_funds(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual(self.calls, [])                                                             # not docked: nothing called
        self.put(docked=True)
        self.assertEqual(w.serve_funds(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual(self.calls, [("withdraw", "Prime Directive", 1), ("withdraw", "Prime Directive", 315699),
                                      ("give", "Prime Directive", "drone-4", 315699)])
        self.assertEqual([a for _p, _t, a in self.booked], [1, 315699])                              # paid once, never steady
        self.assertFalse(any(t.startswith("Faction treasury: credits deposited") for _p, t, _a in self.booked))
        self.assertEqual(w.funds(str(self.data))[0]["state"], "given")
        self.assertEqual(w.funded(str(self.data), time.time()), {"drone-4": 315699})
        self.assertEqual(w.funded(str(self.data), time.time() + 7 * 3600), {})                        # it ends by itself
        gifts = [json.loads(l) for l in (self.data / "fleet" / "gifts.jsonl").read_text().splitlines()]
        self.assertEqual([(g["from"], g["to"], g["credits"]) for g in gifts], [("Prime Directive", "drone-4", 315699)])
        self.calls.clear()
        self.assertEqual(w.add_fund(str(self.data), "drone-4", 1000, "a second buy", 6, now), 0)
        w.serve_funds(str(self.data), "Prime Directive", now, False)
        self.assertEqual(self.calls[0], ("withdraw", "Prime Directive", 1000))                       # no probe after the first fund

    def test_the_treasury_keeps_its_floor_and_a_funded_pilot_gives_nothing(self):
        w, now = self.wallet, time.time()
        self.treasury[0] = w.FUND_FLOOR + 1000
        self.put(docked=True, drone=320000)
        w.add_fund(str(self.data), "drone-4", 315699, "Recursion", 6, now)
        self.assertEqual(w.serve_funds(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual(self.calls, [])                                                             # under the floor: waits
        rows = w.funds(str(self.data))
        rows[0].update(state="given", given_at=int(now))
        w.write_funds(str(self.data), rows)
        named = {}
        skip = {"Prime Directive"} | set(w.funded(str(self.data), now))
        self.assertEqual(w.plan_sweep(w.ships(str(self.data)), "Prime Directive", skip, named), [])  # the sweep leaves it
        rows = [("drone-4", 320000, "Apophis"), ("drone-9", 2000, "Apophis")]
        held = w.funded(str(self.data), now)
        self.assertEqual(w.plan_gifts([(n, c - held.get(n, 0), o) for n, c, o in rows], {}), [])     # no top-up from a fund

    def test_a_withdrawal_whose_gift_failed_stays_with_the_leader_and_is_given_next_pass(self):
        w, now = self.wallet, time.time()
        self.put(docked=True)
        w.add_fund(str(self.data), "drone-4", 315699, "Recursion", 6, now)
        w.give = lambda donor, pilot, credits: (False, "in_battle")
        self.assertEqual(w.serve_funds(str(self.data), "Prime Directive", now, False), 1)
        self.assertEqual(w.funds(str(self.data))[0]["state"], "withdrawn")
        self.assertEqual(w.withdrawn(str(self.data)), 315699)                                         # kept out of the deposit
        w.give = lambda donor, pilot, credits: (self.calls.append(("give", donor, pilot, credits)), (True, "ok"))[1]
        self.put(docked=False)
        self.assertEqual(w.serve_funds(str(self.data), "Prime Directive", now, False), 0)            # a gift needs no dock
        self.assertEqual(self.calls[-1], ("give", "Prime Directive", "drone-4", 315699))
        self.assertEqual([c[0] for c in self.calls].count("withdraw"), 2)                            # the probe and one withdrawal


class TreasuryTopupTests(FundTests):
    """Requests ENT-380, ENT-384, ENT-385, ENT-386, ENT-389 (2026-11-23): newborns born with 100 to 250 cr and no ship of
    their division above the sweep's line to give: the treasury tops them up to TREASURY_LINE, many pilots in one
    withdrawal, within TREASURY_DAY a day, each pilot at most once in TREASURY_EVERY."""

    def put(self, docked, drone=20000):
        ships = [{"name": "Prime Directive", "credits": 30500, "docked": docked}, {"name": "drone-4", "credits": drone},
                 {"name": "drone-60", "credits": 100}, {"name": "drone-61", "credits": 250}, {"name": "drone-62", "credits": 7000}]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))

    def topup(self):
        os.environ["HERMES_SESSION_PROFILE"] = "unity"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)
        return self.wallet.main(["topup", "--data", str(self.data)])

    def test_stranded_pilots_under_the_line_are_funded_from_the_treasury_in_one_withdrawal(self):
        w, now = self.wallet, time.time()
        w.TREASURY_TOPUP = True
        w.refresh = lambda pilot: None
        self.topup()                                                                              # no donor: rows, no call
        rows = [r for r in w.funds(str(self.data)) if r.get("kind") == "topup"]
        self.assertEqual(sorted((r["pilot"], r["credits"]) for r in rows), [("drone-60", 5900), ("drone-61", 5750)])   # 7,000 is above the line
        self.assertEqual(self.calls, [])
        self.topup()                                                                              # never a second row a pilot
        self.assertEqual(len([r for r in w.funds(str(self.data)) if r.get("kind") == "topup"]), 2)
        self.put(docked=True)
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        withdrawals = [c for c in self.calls if c[0] == "withdraw"]
        self.assertEqual(withdrawals[-1], ("withdraw", "Prime Directive", 11650))                # one withdrawal for both
        self.assertEqual(sorted(c[2:] for c in self.calls if c[0] == "give"), [("drone-60", 5900), ("drone-61", 5750)])
        self.assertEqual({r["state"] for r in w.funds(str(self.data)) if r.get("kind") == "topup"}, {"given"})
        self.assertEqual(w.funded(str(self.data), time.time()), {})                               # a top-up is no fund the sweep keeps
        self.assertEqual(w.withdrawn(str(self.data)), 0)

    def test_the_day_cap_and_the_switch_hold(self):
        w = self.wallet
        w.TREASURY_TOPUP = False
        self.topup()
        self.assertEqual([r for r in w.funds(str(self.data)) if r.get("kind") == "topup"], [])  # switched off: nothing
        w.TREASURY_TOPUP, w.TREASURY_DAY = True, 6000
        self.topup()
        self.assertEqual([r["pilot"] for r in w.funds(str(self.data)) if r.get("kind") == "topup"], ["drone-60"])   # 5,900 fits, 5,750 more does not

    def test_a_withdrawal_waits_for_a_docked_leader_and_keeps_the_floor(self):
        w, now = self.wallet, time.time()
        w.TREASURY_TOPUP = True
        self.topup()
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual(self.calls, [])                                                          # not docked
        self.put(docked=True)
        self.treasury[0] = w.FUND_FLOOR + 6000
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual([c for c in self.calls if c[0] == "withdraw"][-1], ("withdraw", "Prime Directive", 5900))     # what the floor allows


if __name__ == "__main__":
    unittest.main()
