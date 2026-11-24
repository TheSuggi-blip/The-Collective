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

    def test_a_spent_fund_draws_no_top_up_and_a_poor_funded_pilot_gets_only_the_normal_one(self):
        """A fund given for a hull and spent on it stays `held` for its hours; the top-up must not refill the pilot
        to the fund's size from donors and the treasury (a pilot so refilled commissioned a second hull)."""
        w, now = self.wallet, time.time()
        held = {"drone-4": 400000}
        rows = [("drone-4", 110000, "Apophis"), ("drone-9", 900000, "Apophis")]          # the hull bought: 110,000 left
        self.assertEqual(w.plan_gifts(w.topup_view(rows, held, {}), {}), [])               # neither receiver nor donor
        rows = [("drone-4", 5000, "Apophis"), ("drone-9", 900000, "Apophis")]
        self.assertEqual(w.plan_gifts(w.topup_view(rows, held, {}), {}), [("drone-9", "drone-4", w.TARGET - 5000)])
        rows = [("drone-4", 410000, "Apophis"), ("drone-9", 2000, "Apophis")]             # unspent: its fund is no gift
        self.assertEqual(w.plan_gifts(w.topup_view(rows, held, {}), {}), [])
        rows = [("drone-4", 2000, "Apophis"), ("drone-9", 900000, "Apophis")]             # no fund: as before
        self.assertEqual(w.topup_view(rows, {}, {}), rows)

    def test_officer_self_withdrawal_marks_fund_given_without_self_gift(self):
        """When a promoted Officer withdraws its own queued fund (e.g. trader-6), serve_funds must mark the row given
        immediately without calling give(actor, actor, ...) which SpaceMolt rejects with invalid_target."""
        w, now = self.wallet, time.time()
        self.put(docked=False)
        (self.data / "empire").mkdir(parents=True, exist_ok=True)
        (self.data / "empire" / "empire.json").write_text(json.dumps({
            "members": [{"pilot": "trader-6", "role": "officer"}],
            "facilities": [{"type": "faction_storage", "base_id": "base_alpha", "active": True}],
        }))
        fleet = json.loads((self.data / "fleet" / "fleet.json").read_text())
        fleet["ships"].append({"name": "trader-6", "credits": 40000, "docked": "base_alpha", "poi": "base_alpha"})
        fleet["ships"].append({"name": "trader-3", "credits": 20000, "docked": "base_alpha", "poi": "base_alpha"})
        (self.data / "fleet" / "fleet.json").write_text(json.dumps(fleet))
        w.write_funds(str(self.data), [
            {"pilot": "drone-0", "credits": 1000, "why": "prior", "hours": 6, "at": int(now) - 3600,
             "state": "given", "probed": {"ok": True}},
        ])
        w.add_fund(str(self.data), "trader-6", 180000, "upgrade apophenia", 48, now)
        w.add_fund(str(self.data), "trader-3", 170000, "upgrade apophenia", 48, now)
        self.assertEqual(w.serve_funds(str(self.data), "Prime Directive", now, False), 0)
        give_calls = [c for c in self.calls if c[0] == "give"]
        self.assertEqual(give_calls, [("give", "trader-6", "trader-3", 170000)])
        rows = {r["pilot"]: r for r in w.funds(str(self.data))}
        self.assertEqual(rows["trader-6"]["state"], "given")
        self.assertEqual(rows["trader-3"]["state"], "given")
        self.assertEqual(w.withdrawn(str(self.data)), 0)
        self.assertEqual(w.funded(str(self.data), now).get("trader-6"), 180000)

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
        self.assertEqual(sorted((r["pilot"], r["credits"]) for r in rows), [("drone-60", 10900), ("drone-61", 10750), ("drone-62", 4000)])   # rule F7's line
        self.assertEqual(self.calls, [])
        self.topup()                                                                              # never a second row a pilot
        self.assertEqual(len([r for r in w.funds(str(self.data)) if r.get("kind") == "topup"]), 3)
        self.put(docked=True)
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        withdrawals = [c for c in self.calls if c[0] == "withdraw"]
        self.assertEqual(withdrawals[-1], ("withdraw", "Prime Directive", 25650))                # one withdrawal for all three
        self.assertEqual(sorted(c[2:] for c in self.calls if c[0] == "give"), [("drone-60", 10900), ("drone-61", 10750), ("drone-62", 4000)])
        self.assertEqual({r["state"] for r in w.funds(str(self.data)) if r.get("kind") == "topup"}, {"given"})
        self.assertEqual(w.funded(str(self.data), time.time()), {})                               # a top-up is no fund the sweep keeps
        self.assertEqual(w.withdrawn(str(self.data)), 0)

    def test_the_day_cap_and_the_switch_hold(self):
        w = self.wallet
        w.TREASURY_TOPUP = False
        self.topup()
        self.assertEqual([r for r in w.funds(str(self.data)) if r.get("kind") == "topup"], [])  # switched off: nothing
        w.TREASURY_TOPUP, w.TREASURY_DAY = True, 11000
        self.topup()
        self.assertEqual([r["pilot"] for r in w.funds(str(self.data)) if r.get("kind") == "topup"], ["drone-60"])   # 10,900 fits, 10,750 more does not

    def test_a_withdrawal_waits_for_a_docked_leader_and_keeps_the_floor(self):
        w, now = self.wallet, time.time()
        w.TREASURY_TOPUP = True
        self.topup()
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual(self.calls, [])                                                          # not docked
        self.put(docked=True)
        self.treasury[0] = w.FUND_FLOOR + 11000
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual([c for c in self.calls if c[0] == "withdraw"][-1], ("withdraw", "Prime Directive", 10900))     # what the floor allows

    def withdrawn_rows(self, *pilots):
        rows = [{"pilot": p, "credits": c, "why": "t", "at": int(time.time()) - 600, "hours": 0, "state": "withdrawn",
                 "withdrawn_at": int(time.time()) - 300, "kind": "topup"} for p, c in pilots]
        self.wallet.write_funds(str(self.data), rows)

    def test_credits_withdrawn_for_named_pilots_are_no_donors_to_give(self):
        # 2026-11-23 06:32-09:40 UTC: the leader held 182,310 cr withdrawn for 44 named pilots; the top-up pass took it
        # for the richest donor of the command group and gave it away to others, the named pilots' gifts then failed
        # (`insufficient_funds`, the leader 861 cr) and the leader stood under rule F7's floor.
        w = self.wallet
        w.TREASURY_TOPUP = True
        w.refresh = lambda pilot: None
        ships = [{"name": "Prime Directive", "credits": 30500 + 21650, "docked": False}, {"name": "drone-4", "credits": 20000},
                 {"name": "drone-60", "credits": 100}, {"name": "drone-61", "credits": 250}, {"name": "drone-70", "credits": 100}]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))
        self.withdrawn_rows(("drone-60", 10900), ("drone-61", 10750))
        self.topup()
        self.assertEqual([c for c in self.calls if c[0] == "give"], [])                          # the leader keeps what it owes
        rows = [r for r in w.funds(str(self.data)) if r.get("kind") == "topup"]
        self.assertEqual(sorted((r["pilot"], r["state"]) for r in rows),
                         [("drone-60", "withdrawn"), ("drone-61", "withdrawn"), ("drone-70", "open")])   # each pilot once

    def test_a_withdrawn_top_up_whose_pilot_was_topped_since_ends_and_goes_back_with_the_deposit(self):
        w, now = self.wallet, time.time()
        self.put(docked=False, drone=20000)
        self.withdrawn_rows(("drone-4", 10900), ("drone-60", 10900))
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual([c[2:] for c in self.calls if c[0] == "give"], [("drone-60", 10900)])   # drone-4 holds 20,000 now
        states = {r["pilot"]: r["state"] for r in w.funds(str(self.data))}
        self.assertEqual(states, {"drone-4": "ended", "drone-60": "given"})
        self.assertEqual(w.withdrawn(str(self.data)), 0)                                          # the leader deposits it again

    def test_a_gift_the_leader_cannot_pay_ends_its_row_and_the_pilot_is_asked_again(self):
        w, now = self.wallet, time.time()
        self.put(docked=False)
        self.withdrawn_rows(("drone-60", 10900))
        w.give = lambda donor, pilot, credits: (False, '{"error":"API call failed: insufficient_funds: You only have 861 credits."}')
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)       # no HALT every pass
        row = w.funds(str(self.data))[0]
        self.assertEqual(row["state"], "ended")
        self.assertIn("insufficient_funds", row["note"])
        w.TREASURY_TOPUP = True
        self.assertEqual(w.treasury_topups(str(self.data), [("drone-60", 100)], now, False), {"drone-60"})   # a new row
        self.assertEqual([r["state"] for r in w.funds(str(self.data)) if r["pilot"] == "drone-60"], ["ended", "open"])

    def test_the_leaders_own_top_up_is_given_by_the_withdrawal(self):
        w, now = self.wallet, time.time()
        self.put(docked=True)
        self.withdrawn_rows(("Prime Directive", 9000))
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual([c for c in self.calls if c[0] == "give"], [])                          # no gift to itself
        self.assertEqual(w.funds(str(self.data))[0]["state"], "given")
        ships = [{"name": "Prime Directive", "credits": 1384, "docked": False}]                  # an old row, its money gone
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))
        self.withdrawn_rows(("Prime Directive", 9000))
        self.assertEqual(w.serve_topups(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual(w.funds(str(self.data))[0]["state"], "ended")                           # a new row asks again


class AdmiralSelfFundingTests(FundTests):
    """Autonomous division treasury access (Suggi, 2026-11-24; rule F12): Admirals fund own division uncapped
    per pilot/day keeping 500k floor; serve_funds batches up to FUND_BATCH and uses docked Officers."""

    def put_empire(self, treasury=1800000, officer=None):
        (self.data / "empire").mkdir(exist_ok=True)
        members = [{"pilot": "Prime Directive", "role": "Leader"}]
        if officer:
            members.append({"pilot": officer, "role": "Officer"})
        (self.data / "empire" / "empire.json").write_text(
            json.dumps({
                "faction": {"leader": "Prime Directive", "treasury": treasury},
                "members": members,
                "facilities": [{"type": "faction_lockbox", "base": "node_beta_industrial_station", "status": "active"}],
            }),
            encoding="ascii",
        )

    def put_fleet(self, extra=None):
        ships = [
            {"name": "Prime Directive", "credits": 50000, "docked": ""},
            {"name": "Zero Point", "credits": 50000, "docked": "node_beta_industrial_station"},
            {"name": "miner-1", "credits": 25000},
            {"name": "miner-2", "credits": 25000},
            {"name": "miner-3", "credits": 25000},
            {"name": "trader-1", "credits": 25000},
        ]
        if extra:
            ships.extend(extra)
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}), encoding="ascii")

    def test_admiral_funds_own_division_uncapped_and_rejects_foreign_or_below_floor(self):
        w, now = self.wallet, time.time()
        self.put_empire(treasury=2200000)
        self.put_fleet()
        self.assertIsNone(w.ADMIRAL_MAX_SINGLE)
        self.assertIsNone(w.ADMIRAL_DAY_CAP)
        self.assertEqual(w.add_fund(str(self.data), "miner-1", 600000, "Tier 2 Miner", 6, now, who="Zero"), 0)
        self.assertEqual(w.add_fund(str(self.data), "miner-2", 600000, "Tier 2 Miner", 6, now, who="Zero"), 0)
        self.assertEqual(w.add_fund(str(self.data), "trader-1", 100000, "wrong div", 6, now, who="Zero"), 1)
        self.assertEqual(w.add_fund(str(self.data), "miner-3", 450000, "large uncapped", 6, now, who="Zero"), 0)
        # 2,200,000 - 1,650,000 open = 550,000 left; asking 100,000 breaks 500,000 FUND_FLOOR
        self.assertEqual(w.add_fund(str(self.data), "trader-1", 100000, "floor test", 6, now, who="Mercury"), 1)
        # fund --show must format cleanly when caps are None
        self.assertEqual(w.main(["fund", "--show", "--data", str(self.data)]), 0)

    def test_serve_funds_batches_open_rows_and_uses_docked_officer_when_leader_undocked(self):
        w, now = self.wallet, time.time()
        self.put_empire(treasury=1800000, officer="Zero Point")
        self.put_fleet()
        self.treasury[0] = 1800000
        self.assertEqual(w.add_fund(str(self.data), "miner-1", 200000, "batch 1", 6, now, who="Zero"), 0)
        self.assertEqual(w.add_fund(str(self.data), "miner-2", 250000, "batch 2", 6, now, who="Zero"), 0)
        self.assertEqual(w.serve_funds(str(self.data), "Prime Directive", now, False), 0)
        self.assertEqual(self.calls, [
            ("withdraw", "Zero Point", 1),
            ("withdraw", "Zero Point", 450000),
            ("give", "Zero Point", "miner-1", 200000),
            ("give", "Zero Point", "miner-2", 250000),
        ])
        self.assertEqual([r["state"] for r in w.funds(str(self.data))], ["given", "given"])




class WalletFluidityUpgradeTests(FundTests):
    """Parallel direct member deposits, decoupled sweep/serve, P2P mid-flight funding, multi-tier storage bases,
    and self-healing auto-officer staffing (Suggi, 2026-11-24)."""

    def test_seated_members_deposit_directly_in_parallel_and_cooldown_prevents_double_sweep(self):
        w, now = self.wallet, time.time()
        w.SWEEP_ENABLED = True
        w.SHOW_WAIT = 0
        w.SWEEP_WORKERS = 4
        w.DIRECT_DEPOSIT_PER_PASS = 10
        w.PER_PASS = 10
        w.refresh = lambda p: None
        w.treasury_read = lambda p: None
        (self.data / "empire").mkdir(exist_ok=True)
        (self.data / "empire" / "empire.json").write_text(json.dumps({
            "faction": {"id": "fac-1", "leader": "Prime Directive", "treasury": 1000000},
            "members": [
                {"pilot": "Prime Directive", "role": "leader"},
                {"pilot": "miner-1", "role": "member"},
                {"pilot": "miner-2", "role": "member"},
            ],
            "facilities": [],
        }), encoding="ascii")
        bals = {"Prime Directive": 50000, "miner-1": 80000, "miner-2": 70000, "miner-3": 65000}

        def write_fl():
            ships = [{"name": n, "credits": c, "status": "connected", "docked": ""} for n, c in bals.items()]
            (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}), encoding="ascii")

        write_fl()
        lock = __import__("threading").Lock()
        dep_calls, give_calls = [], []

        def fake_dep(pilot, credits):
            with lock:
                dep_calls.append((pilot, credits))
                bals[pilot] -= credits
                rem = bals[pilot]
                write_fl()
            return True, json.dumps({"player": {"username": pilot, "credits": rem}})

        def fake_give(donor, target, credits):
            with lock:
                give_calls.append((donor, target, credits))
                bals[donor] -= credits
                bals[target] += credits
                rem = bals[donor]
                write_fl()
            return True, json.dumps({"player": {"username": donor, "credits": rem}})

        w.deposit = fake_dep
        w.give = fake_give
        rc = w.sweep(str(self.data), now, False, cash_only=True)
        self.assertEqual(rc, 0)
        # miner-1 (50k) & miner-2 (40k) are seated -> direct deposit to faction!
        # miner-3 (35k) is unseated -> gifted to Prime Directive -> Prime Directive deposits 35k!
        self.assertEqual(sorted(dep_calls), [("Prime Directive", 35000), ("miner-1", 50000), ("miner-2", 40000)])
        self.assertEqual(give_calls, [("miner-3", "Prime Directive", 35000)])
        once = json.loads((self.data / "fleet" / "onetime.json").read_text())
        dep_rows = sorted((r[1], r[3]) for r in once if r[2] == w.DEPOSIT_TITLE)
        self.assertEqual(dep_rows, [("Prime Directive", -35000), ("miner-1", -50000), ("miner-2", -40000)])
        # Second pass immediately: miner-1/miner-2 on cooldown via recent_direct_deposits even if wallet refilled
        bals["miner-1"] = 90000
        write_fl()
        dep_calls.clear()
        give_calls.clear()
        rc2 = w.sweep(str(self.data), now + 60, False, cash_only=True)
        self.assertEqual(rc2, 0)
        self.assertEqual(dep_calls, [])

    def test_cut_direct_deposit_is_settled_once_on_next_pass(self):
        w, now = self.wallet, time.time()
        sent_at = int(now) - 120
        (self.data / "fleet" / "sweep.jsonl").write_text(
            json.dumps({"at": sent_at, "kind": "direct_deposit", "from": "miner-1", "to": "faction",
                        "credits": 40000, "state": "sent", "wallets": {"miner-1": 70000}, "text": ""}) + "\n",
            encoding="ascii",
        )
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({
            "ships": [{"name": "Prime Directive", "credits": 50000, "state_at": ts},
                      {"name": "miner-1", "credits": 30000, "state_at": ts}]
        }), encoding="ascii")
        waiting, failed = w.settle_direct_deposits(str(self.data), now, dry=False)
        self.assertEqual((waiting, failed), ({}, 0))
        once = json.loads((self.data / "fleet" / "onetime.json").read_text())
        self.assertEqual([(r[0], r[1], r[3]) for r in once if r[2] == w.DEPOSIT_TITLE], [(sent_at, "miner-1", -40000)])
        # Re-running settles nothing twice
        waiting2, failed2 = w.settle_direct_deposits(str(self.data), now + 30, dry=False)
        self.assertEqual((waiting2, failed2), ({}, 0))
        once2 = json.loads((self.data / "fleet" / "onetime.json").read_text())
        self.assertEqual(len([r for r in once2 if r[2] == w.DEPOSIT_TITLE]), 1)

    def test_p2p_midflight_funding_fills_without_docked_officer_and_handles_partial(self):
        w, now = self.wallet, time.time()
        w.SHOW_WAIT = 0
        w.SWEEP_WORKERS = 4
        w.P2P_FUND_ENABLED = True
        w.refresh = lambda p: None
        (self.data / "empire").mkdir(exist_ok=True)
        (self.data / "empire" / "empire.json").write_text(json.dumps({
            "faction": {"id": "fac-1", "leader": "Prime Directive", "treasury": 2000000},
            "members": [{"pilot": "Prime Directive", "role": "leader"}],
            "facilities": [{"type": "faction_warehouse", "base": "keep_base", "status": "active"}],
        }), encoding="ascii")
        bals = {"Prime Directive": 50000, "drone-4": 20000, "miner-1": 150000, "miner-2": 130000, "miner-3": 100000}

        def write_fl():
            ships = [{"name": n, "credits": c, "status": "connected", "docked": ""} for n, c in bals.items()]
            (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}), encoding="ascii")

        write_fl()
        lock = __import__("threading").Lock()
        sent_slices = []

        def fake_give(donor, target, credits):
            with lock:
                sent_slices.append((donor, target, credits))
                bals[donor] -= credits
                bals[target] += credits
                rem = bals[donor]
                write_fl()
            return True, json.dumps({"player": {"username": donor, "credits": rem}})

        w.give = fake_give
        self.assertEqual(w.add_fund(str(self.data), "drone-4", 200000, "P2P hull buy", 6, now, who="Unity"), 0)
        rc = w.serve_funds(str(self.data), "Prime Directive", now, False)
        self.assertEqual(rc, 0)
        row = w.funds(str(self.data))[0]
        self.assertEqual(row["state"], "given")
        self.assertEqual(row.get("via"), "p2p")
        self.assertEqual(sum(c for _d, _t, c in sent_slices), 200000)
        # Verify partial fill deducts landed slice safely when one donor is in_battle
        bals["miner-3"] = 90000
        bals["miner-4"] = 90000
        bals["drone-5"] = 10000
        write_fl()
        sent_slices.clear()

        def partial_give(donor, target, credits):
            if donor == "miner-4":
                return False, '{"error":"in_battle"}'
            return fake_give(donor, target, credits)

        w.give = partial_give
        self.assertEqual(w.add_fund(str(self.data), "drone-5", 100000, "Partial P2P", 6, now, who="Unity"), 0)
        rc2 = w.serve_funds(str(self.data), "Prime Directive", now, False)
        self.assertEqual(rc2, 0)
        row2 = [r for r in w.funds(str(self.data)) if r["pilot"] == "drone-5"][0]
        self.assertEqual(row2["state"], "open")
        self.assertEqual(row2["credits"], 60000)  # miner-4 (60k) hit in_battle; miner-3 (40k) landed -> 60k left

    def test_auto_queue_officers_and_upgraded_storage_tiers(self):
        w, now = self.wallet, time.time()
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({
            "Prime Directive": {"admiral": "Unity", "division": "Command", "role": "command"},
            "Zero Point": {"admiral": "Unity", "division": "Command", "role": "command"},
            "Mercurys Ledger": {"admiral": "Unity", "division": "Command", "role": "command"},
        }), encoding="ascii")
        (self.data / "empire").mkdir(exist_ok=True)
        (self.data / "empire" / "empire.json").write_text(json.dumps({
            "faction": {"id": "fac-1", "leader": "Prime Directive", "treasury": 2000000},
            "members": [
                {"pilot": "Prime Directive", "role": "leader"},
                {"pilot": "Zero Point", "role": "member"},
                {"pilot": "Mercurys Ledger", "role": "officer"},
                {"pilot": "trader-5", "role": "member"},
                {"pilot": "trader-11", "role": "member"},
                {"pilot": "hauler-31", "role": "member"},
                {"pilot": "miner-19", "role": "member"},
                {"pilot": "hauler-3", "role": "builder"},
            ],
            "facilities": [
                {"type": "faction_warehouse", "base": "base_alpha", "status": "active"},
            ],
        }), encoding="ascii")
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({
            "ships": [
                {"name": "Prime Directive", "credits": 50000, "docked": ""},
                {"name": "Zero Point", "credits": 50000, "docked": ""},
                {"name": "Mercurys Ledger", "credits": 50000, "docked": "base_alpha"},
                {"name": "trader-5", "credits": 50000, "docked": "base_alpha"},
                {"name": "trader-11", "credits": 50000, "docked": "base_alpha"},
                {"name": "hauler-31", "credits": 50000, "docked": "base_alpha"},
                {"name": "miner-19", "credits": 50000, "docked": "base_alpha"},
                {"name": "hauler-3", "credits": 50000, "docked": "base_alpha"},
            ]
        }), encoding="ascii")
        # Upgraded faction_warehouse base must be recognized by ready_withdrawer!
        self.assertEqual(w.ready_withdrawer(str(self.data), "Prime Directive", request_stop=False), "Mercurys Ledger")
        # auto_queue_officers queues Zero Point (flagship), fills up to LOCKBOX_OFFICERS_PER_BASE=4 docked bankers
        # at base_alpha (trader-11, trader-5, hauler-31), and guarantees division coverage (miner-19 for Mining)
        self.assertEqual(w.MAX_AUTO_OFFICERS, 50)
        self.assertEqual(w.LOCKBOX_OFFICERS_PER_BASE, 4)
        self.assertEqual(w.MIN_OFFICERS_PER_DIVISION, 4)
        self.assertEqual(w.auto_queue_officers(str(self.data), now, dry=False), 0)
        queued = [r["params"]["player_id"] for r in w.errands(str(self.data)) if r.get("action") == "promote"]
        self.assertEqual(queued, ["Zero Point", "trader-11", "trader-5", "hauler-31", "miner-19"])
        # Calling again deduplicates cleanly (zero duplicates!)
        self.assertEqual(w.auto_queue_officers(str(self.data), now + 60, dry=False), 0)
        self.assertEqual(len(w.errands(str(self.data))), 5)

    def test_auto_queue_officers_covers_military_and_intel_divisions(self):
        w, now = self.wallet, time.time()
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({
            "Prime Directive": {"admiral": "Unity", "division": "Command", "role": "command"},
        }), encoding="ascii")
        (self.data / "empire").mkdir(exist_ok=True)
        (self.data / "empire" / "empire.json").write_text(json.dumps({
            "faction": {"id": "fac-1", "leader": "Prime Directive", "treasury": 2000000},
            "members": [
                {"pilot": "Prime Directive", "role": "leader"},
                {"pilot": "drone-1", "role": "member"},
                {"pilot": "drone-2", "role": "member"},
                {"pilot": "scout-1", "role": "member"},
            ],
            "facilities": [],
        }), encoding="ascii")
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({
            "ships": [
                {"name": "Prime Directive", "division": "Command", "credits": 50000, "docked": ""},
                {"name": "drone-1", "division": "Military", "credits": 50000, "docked": ""},
                {"name": "drone-2", "division": "Military", "credits": 50000, "docked": "node_beta"},
                {"name": "scout-1", "division": "Intel", "credits": 50000, "docked": "central_nexus"},
            ]
        }), encoding="ascii")
        self.assertEqual(w.auto_queue_officers(str(self.data), now, dry=False), 0)
        queued = [r["params"]["player_id"] for r in w.errands(str(self.data)) if r.get("action") == "promote"]
        # Docked Military drone-2 promoted before undocked drone-1, plus Intel scout-1
        self.assertEqual(queued, ["drone-2", "drone-1", "scout-1"])



    def test_serve_flock_prevents_concurrent_overlap(self):
        w = self.wallet
        fh = w._acquire_serve_lock(str(self.data))
        self.assertIsNotNone(fh)
        try:
            self.assertIsNone(w._acquire_serve_lock(str(self.data)))
            self.assertEqual(w.serve(str(self.data), time.time(), dry=False), 0)
        finally:
            fh.close()
        fh2 = w._acquire_serve_lock(str(self.data))
        self.assertIsNotNone(fh2)
        fh2.close()


if __name__ == "__main__":
    unittest.main()
