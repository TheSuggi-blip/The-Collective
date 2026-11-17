"""The fleet's money between our own purses: the collector's matching (station/fleet.py: a gift or a deposit counts in
the window that read its wallet change, a deposit is never a purchase), the sweep into the faction's treasury
(game/fleet/wallet.py sweep) and the treasury beside the wallets (game/fleet/hive.py fleet). No engine, no network."""

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

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"
sys.path.insert(0, str(FLEET))
T0 = 1_800_000_000                                 # the tests' clock: a window of whole hours from here
STEP = 600
LEADER = "Prime Directive"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def history(moves=(), steps=8):
    """Samples every STEP seconds from T0. Mining (miner-1): earned +1,000 and wallet +500 a step; Command (the leader):
    earned +600 and wallet +300 a step. `moves`: (division, credits, from the sample at this offset on)."""
    rows = []
    for k in range(steps):
        t = T0 + k * STEP
        div = {"Mining": [1, 100000 + 500 * k, 10000 + 1000 * k], "Command": [1, 40000 + 300 * k, 5000 + 600 * k]}
        spent = {d: v[2] - v[1] for d, v in div.items()}          # the counters: credits = earned - spent, a move apart
        for division, credits, since in moves:
            if t >= T0 + since:
                div[division][1] += credits
        rows.append([t, sum(v[1] for v in div.values()), 2, sum(v[2] for v in div.values()), 0, 0, 0,
                     {d: [v[0], v[1], v[2], 0, 0, 0] for d, v in div.items()}, {"s": sum(spent.values()), "ds": spent}])
    return rows


NOW = T0 + 7 * STEP                                 # the last sample; the hour (T0 + 600, T0 + 4200] is the 1h window


class CollectorMatchingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-money-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.fleet = load(ROOT / "station" / "fleet.py", "collector_money_test")
        self.fleet.DATA = self.data
        self.fleet.FLAGSHIPS = {LEADER: {"admiral": "Unity", "division": "Command", "role": "command", "of": "Unity"}}

    def put(self, gifts=(), onetime=(), moves=None):
        (self.data / "gifts.jsonl").write_text("".join(json.dumps(g) + "\n" for g in gifts))
        (self.data / "onetime.json").write_text(json.dumps(list(onetime)))
        if moves is not None:
            (self.data / "moves.jsonl").write_text("".join(json.dumps(m) + "\n" for m in moves))

    def gift(self, at, giver, taker, credits):
        return ({"at": T0 + at, "from": giver, "to": taker, "credits": credits},
                [[T0 + at, giver, "Wallet top-up", -credits], [T0 + at, taker, "Wallet top-up", credits]])

    @staticmethod
    def nets(r):
        return {key: (w["income_per_hour"], w["costs_per_hour"], w["cph"], {d: (x["income_per_hour"], x["costs_per_hour"], x["cph"]) for d, x in w["divisions"].items()})
                for key, w in r["windows"].items()}

    def plain(self):
        self.put()
        return self.fleet.rates(history(), NOW)

    def test_the_hour_that_began_between_the_givers_and_the_leader_reads_no_gift_as_money_earned(self):
        # 2026-11-17 19:08 UTC: the hour from 18:08:03 held the leader's reading of 189,565 cr of gifts (18:09:07) whose givers
        # were read before it began (18:01 to 18:08): costs -95,755 cr an hour. Here 30,000 cr: miner-1 read at once, the
        # leader 20 minutes later, inside the hour; the hour must read as the hour without the gift.
        plain = self.nets(self.plain())
        row, books = self.gift(300, "miner-1", LEADER, 30000)
        self.put([row], books, [{"at": T0 - 3600, "start": 1}, {"at": T0 + STEP, "pilot": "miner-1", "moved": -30000},
                                {"at": T0 + 3 * STEP, "pilot": LEADER, "moved": 30000}])
        r = self.fleet.rates(history([("Mining", -30000, STEP), ("Command", 30000, 3 * STEP)]), NOW)
        self.assertEqual(self.nets(r), plain)
        self.assertGreater(r["windows"]["1h"]["costs_per_hour"], 0)
        self.assertEqual((r["windows"]["1h"]["gifts_early"], r["windows"]["1h"]["gifts_unseen"]), (30000, 0))

    def test_a_gift_its_receiver_has_not_shown_is_held_out_of_every_window(self):
        # errors.log ENT-094: 189,040 cr of gifts booked before the receiving wallet showed them read about sum/hours too low
        # in every window that held them. A gift booked, the giver read, the receiver's reading older than the gift.
        plain = self.nets(self.plain())
        row, books = self.gift(5 * STEP + 30, "miner-1", LEADER, 24000)
        self.put([row], books, [{"at": T0 - 3600, "start": 1}, {"at": T0 + 6 * STEP, "pilot": "miner-1", "moved": -24000}])
        r = self.fleet.rates(history([("Mining", -24000, 6 * STEP)]), NOW)
        self.assertEqual(self.nets(r), plain)
        for key in ("1h", "6h", "24h"):
            self.assertEqual(r["windows"][key]["gifts_unseen"], 24000)
        # once the leader is read, the gift is whole in the window and moves nothing either
        self.put([row], books, [{"at": T0 - 3600, "start": 1}, {"at": T0 + 6 * STEP, "pilot": "miner-1", "moved": -24000},
                                {"at": T0 + 7 * STEP, "pilot": LEADER, "moved": 24000}])
        r = self.fleet.rates(history([("Mining", -24000, 6 * STEP), ("Command", 24000, 7 * STEP)]), NOW)
        self.assertEqual(self.nets(r), plain)
        self.assertEqual(r["windows"]["1h"]["gifts_unseen"], 0)

    def test_a_deposit_booked_in_the_window_and_read_before_it_costs_nothing(self):
        # Unity, 2026-11-17: a deposit booked inside the window while its wallet drop was read before it began; the old
        # code read the booking as money bought once against no fall of the wallets, the costs below zero.
        plain = self.nets(self.plain())
        self.put([], [[T0 + 1000, LEADER, "Faction treasury: credits deposited (the Collective keeps them)", -50000]],
                 [{"at": T0 - 3600, "start": 1}, {"at": T0 + STEP, "pilot": LEADER, "moved": -50000}])
        r = self.fleet.rates(history([("Command", -50000, STEP)]), NOW)
        self.assertEqual(self.nets(r), plain)
        w = r["windows"]["1h"]
        self.assertGreater(w["costs_per_hour"], 0)
        self.assertEqual((w["bought_once_per_hour"], w["treasury_moved_per_hour"]), (0, 0))   # the hour did not read it

    def test_a_deposit_into_the_treasury_is_a_move_between_two_purses_never_a_purchase(self):
        plain = self.plain()
        self.put([], [[T0 + 2000, LEADER, "Faction treasury: credits deposited (the Collective keeps them)", -36000]],
                 [{"at": T0 - 3600, "start": 1}, {"at": T0 + 4 * STEP, "pilot": LEADER, "moved": -36000}])
        r = self.fleet.rates(history([("Command", -36000, 4 * STEP)]), NOW)
        self.assertEqual(self.nets(r), self.nets(plain))
        w, p = r["windows"]["1h"], plain["windows"]["1h"]
        self.assertEqual((w["bought_once_per_hour"], w["one_time_per_hour"]), (0, 0))
        self.assertEqual((w["treasury_moved_per_hour"], w["divisions"]["Command"]["treasury_moved_per_hour"]), (36000, 36000))
        self.assertEqual((w["total_per_hour"], w["wallets_per_hour"]), (p["total_per_hour"], p["wallets_per_hour"]))
        # with no reading of the moves at all (before the collector kept moves.jsonl) it counts at its booking time
        (self.data / "moves.jsonl").unlink()
        r = self.fleet.rates(history([("Command", -36000, 4 * STEP)]), NOW)
        self.assertEqual(self.nets(r), self.nets(plain))

    def test_the_moves_are_written_when_a_wallet_changes_by_what_the_counters_do_not_explain(self):
        path, last, state = self.data / "m.jsonl", {}, {"started": 0, "pruned": 0}
        row = lambda name, credits, earned, spent, status="connected": {"name": name, "credits": credits, "earned": earned, "spent": spent, "status": status}
        self.assertEqual(self.fleet.note_moves([row("miner-1", 1000, 500, 0), row("miner-2", 50, 0, 0)], T0, path, last, state), [])
        events = self.fleet.note_moves([row("miner-1", 1400, 1000, 100), row("miner-2", 30050, 0, 0)], T0 + 10, path, last, state)
        self.assertEqual(events, [{"at": T0 + 10, "pilot": "miner-2", "moved": 30000}])           # a sale and fuel: no move
        self.fleet.note_moves([row("miner-1", 1400, 1000, 100)], T0 + 20, path, last, state)      # miner-2 not listed: its reading goes
        self.assertEqual(self.fleet.note_moves([row("miner-1", 1400, 1000, 100), row("miner-2", 90, 0, 0)], T0 + 30, path, last, state), [])
        self.assertEqual(self.fleet.note_moves([row("miner-1", 0, 0, 0, "disconnected")], T0 + 40, path, last, state), [])
        moves, starts = self.fleet.read_moves(path)
        self.assertEqual((moves, starts), ([(T0 + 10, "miner-2", 30000)], [T0]))

    def test_each_side_is_read_when_its_wallet_showed_it(self):
        side = lambda at, pilot, credits, kind="gift", move=0: (T0 + at, pilot, credits, kind, move)
        sides = [side(100, LEADER, 1000, move=1), side(110, LEADER, 2000, move=2), side(120, LEADER, 3000, move=3),
                 side(400, "miner-1", -7000, move=4), side(900, LEADER, -9000, "deposit", -1)]
        moves = [(T0 + 300, LEADER, 3000), (T0 + 350, "miner-1", -7000), (T0 + 950, LEADER, -6000)]
        read = self.fleet.read_times(sides, moves, [T0 - 3600], T0 + 1000)
        self.assertEqual(read, [T0 + 300, T0 + 300, T0 + 950, T0 + 350, T0 + 950])   # two in one reading; booked 50 s after its reading
        read = self.fleet.read_times(sides[:1], [], [T0 - 3600], T0 + 1000)
        self.assertEqual(read, [None])                                                   # not read yet: in transit
        self.assertEqual(self.fleet.read_times(sides[:1], [], [T0 - 3600], T0 + 100 + self.fleet.TRANSIT_MAX + 1), [T0 + 100])
        self.assertEqual(self.fleet.read_times(sides[:1], [], [], T0 + 1000), [T0 + 100])              # no readings kept
        self.assertEqual(self.fleet.read_times(sides[:1], [], [T0 - 3600, T0 + 500], T0 + 1000), [T0 + 100])  # a restart since
        self.assertEqual(self.fleet.read_times(sides[:1], [(T0 + 700, LEADER, 55)], [T0 - 3600], T0 + 1000), [T0 + 700])


class RegroupTests(unittest.TestCase):
    """2026-11-17 19:28:24 -> 19:29:29 UTC: the role sentinel went from Command to Military (ROLES, D226), and every
    division window that held the moment read the 20 ships' wallets and counters as Military's income and Command's loss."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-regroup-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.fleet = load(ROOT / "station" / "fleet.py", "collector_regroup_test")
        self.fleet.DATA = self.data
        self.fleet.ROLES["sentinel"] = ("Military", "Apophis")          # the mapping after the move

    @staticmethod
    def sample(t, command, military):
        div = {"Command": command, "Military": military}
        return [t, sum(v[1] for v in div.values()), sum(v[0] for v in div.values()), sum(v[2] for v in div.values()), 0, 0, 0,
                {d: [v[0], v[1], v[2], 0, 0, 0] for d, v in div.items()}, {"s": sum(v[3] for v in div.values()), "ds": {d: v[3] for d, v in div.items()}}]

    def test_twenty_ships_that_change_division_are_neither_division_s_income_nor_loss(self):
        moved = [20, 899768, 1418327, 320657]                            # ships, credits, earned, spent of the 20 sentinels
        before = self.sample(T0, [26, 1150003, 1926684, 645047], [50, 2261480, 3410846, 948120])
        after = self.sample(T0 + 3600, [6, 1150003 - moved[1], 1926684 - moved[2], 645047 - moved[3]],
                            [70, 2261480 + moved[1], 3410846 + moved[2], 948120 + moved[3]])
        record = {"at": T0 + 1800, "from": "Command", "to": "Military", "role": "sentinel", "pilots": [],
                  "out": dict(zip(("ships", "credits", "earned", "spent"), moved)), "in": dict(zip(("ships", "credits", "earned", "spent"), moved))}
        (self.data / "regroup.jsonl").write_text(json.dumps(record) + "\n")
        r = self.fleet.rates([before, after], T0 + 3600, one=[], gifts=[], seeds={}, presence=[])
        for division in ("Command", "Military"):
            w = r["divisions"][division]
            self.assertEqual((w["income_per_hour"], w["costs_per_hour"], w["cph"]), (0, 0, 0))
            self.assertEqual(w["spent_per_hour"], 0)
        self.assertEqual((r["income_per_hour"], r["costs_per_hour"], r["cph"]), (0, 0, 0))
        self.assertEqual(r["divisions"]["Military"]["regroup"], {"ships": 20, "credits": 899768, "earned": 1418327})

    def test_a_reward_counts_for_the_division_that_held_its_pilot_then(self):
        # sentinel-1 earned a reward of 3,500 in Command before the move: Command's income is its earnings less that reward
        before = self.sample(T0, [2, 100000, 50000, 10000], [1, 1000, 1000, 0])
        after = self.sample(T0 + 3600, [1, 30000, 26000, 10000], [2, 81000, 33500, 0])       # sentinel-1 (70,000 / 30,000 earned) moved
        record = {"at": T0 + 2400, "from": "Command", "to": "Military", "role": "", "pilots": ["sentinel-1"],
                  "out": {"ships": 1, "credits": 80000, "earned": 32500, "spent": 0}, "in": {"ships": 1, "credits": 80000, "earned": 32500, "spent": 0}}
        (self.data / "regroup.jsonl").write_text(json.dumps(record) + "\n")
        r = self.fleet.rates([before, after], T0 + 3600, one=[[T0 + 1200, "sentinel-1", "Workshop Production Run", 3500]], gifts=[], seeds={}, presence=[])
        self.assertEqual((r["divisions"]["Command"]["rewards_per_hour"], r["divisions"]["Military"]["rewards_per_hour"]), (3500, 0))
        self.assertEqual(self.fleet.division_then("sentinel-1", T0 + 1200, self.fleet.read_regroup(self.data / "regroup.jsonl")), "Command")
        self.assertEqual(self.fleet.division_then("sentinel-1", T0 + 3000, self.fleet.read_regroup(self.data / "regroup.jsonl")), "Military")

    def test_the_collector_writes_the_move_it_sees_and_the_one_it_did_not_from_two_samples(self):
        old = [{"name": "sentinel-%d" % n, "division": "Command", "credits": 1000 * n, "earned": 10, "spent": 1, "ore_mined": 0, "missions_done": 0} for n in (1, 2)]
        rows = [dict(r, division="Military", credits=r["credits"] + 5) for r in old] + [{"name": "miner-1", "division": "Mining", "credits": 7}]
        lines = self.fleet.note_regroup(old, rows, T0, self.data / "regroup.jsonl")
        self.assertEqual([(x["from"], x["to"], x["role"], x["pilots"], x["out"]["credits"], x["in"]["credits"]) for x in lines],
                         [("Command", "Military", "sentinel", ["sentinel-1", "sentinel-2"], 3000, 3010)])
        self.assertEqual(self.fleet.note_regroup(rows, rows, T0 + 10, self.data / "regroup.jsonl"), [])
        (self.data / "regroup.jsonl").unlink()
        history = [self.sample(T0, [26, 1150003, 1926684, 645047], [50, 2261480, 3410846, 948120]),
                   self.sample(T0 + 65, [6, 250235, 508357, 324390], [70, 3162159, 4830610, 1269303])]
        (self.data / "history.json").write_text(json.dumps(history))
        out = self.fleet.regroup_from_history(self.data, T0, T0 + 65, "sentinel", "Command", "Military", dry_run=True)
        self.assertFalse((self.data / "regroup.jsonl").exists())
        out = self.fleet.regroup_from_history(self.data, T0, T0 + 65, "sentinel", "Command", "Military")
        found = self.fleet.read_regroup(self.data / "regroup.jsonl")
        self.assertEqual([(r[0], r[1], r[2], r[4], r[5]["ships"], r[5]["credits"], r[5]["spent"], r[6]["credits"], r[6]["earned"]) for r in found],
                         [(T0 + 65, "Command", "Military", "sentinel", 20, 899768, 320657, 900679, 1419764)])
        self.assertIn("holds this move already", self.fleet.regroup_from_history(self.data, T0, T0 + 65, "sentinel", "Command", "Military")[-1])


class SweepTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-sweep-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        (self.data / "empire").mkdir()
        (self.data / "empire" / "empire.json").write_text(json.dumps({"written_at": "2026-11-17T18:46:21Z",
            "faction": {"leader": LEADER, "treasury": 364915}, "members": [{"pilot": LEADER, "role": "Leader"}, {"pilot": "hauler-3", "role": "Builder"}]}))
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({LEADER: {"admiral": "Unity", "division": "Command", "role": "command", "of": "Unity"}}))
        self.wallets = {LEADER: 26000, "miner-1": 90000, "miner-2": 80000, "miner-3": 75000, "miner-4": 70000, "miner-5": 65000,
                        "hauler-3": 300000, "drone-1": 100000, "trader-1": 59999}
        self.fight = {"drone-1"}
        self.write()
        self.wallet = load(FLEET / "wallet.py", "wallet_sweep_test")
        self.wallet.SHOW_WAIT = 0
        self.calls = []
        self.wallet.refresh = lambda pilot: None
        self.wallet.treasury_read = lambda pilot: None             # no read of the treasury: the wallet check (a test sets one)
        os.environ["HERMES_SESSION_PROFILE"] = "unity"
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)

    def write(self):
        ships = [{"name": n, "credits": c, "status": "connected", "loop_failures": 2 if n in self.fight else 0,
                  "loop_last_failure": "Mining run failed: in_battle" if n in self.fight else ""} for n, c in self.wallets.items()]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))

    def give(self, donor, pilot, credits):
        self.calls.append(("give", donor, credits))
        if donor == "miner-3":
            return False, '{"error": "in_battle: you are in combat"}'
        self.wallets[donor] -= credits
        self.wallets[pilot] += credits
        self.write()
        return True, "ok"

    def deposit(self, pilot, credits):
        self.calls.append(("deposit", pilot, credits))
        self.wallets[pilot] -= credits
        self.write()
        return True, "ok"

    def run_sweep(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.wallet.main(["sweep", "--data", str(self.data)] + list(args))
        return code, out.getvalue()

    def test_the_sweep_is_off_until_switched_on_and_its_dry_run_says_what_it_would_do(self):
        self.wallet.give, self.wallet.deposit = self.give, self.deposit
        self.wallet.SWEEP_ENABLED = False                     # the state this test reads; the module's own default is on
        with self.assertRaises(SystemExit) as stop:
            self.run_sweep()
        self.assertIn("REFUSED: the sweep is off", str(stop.exception))
        code, text = self.run_sweep("--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("would give: miner-1 -> Prime Directive 40,000 cr (keeps 50,000)", text)
        self.assertEqual(text.count("would give:"), 4)                                   # PER_PASS
        self.assertIn("left out: hauler-3 (300,000 cr): a builder: holds credits for a buy", text)
        self.assertIn("left out: drone-1 (100,000 cr): its loop fails in a fight", text)
        self.assertIn("the treasury read 364,915 cr at 2026-11-17 18:46:21 UTC", text)
        self.assertEqual(self.calls, [])
        self.assertEqual(sorted(p.name for p in (self.data / "fleet").iterdir()), ["flagships.json", "fleet.json"])   # wrote nothing

    def test_a_pass_gives_a_few_ships_books_each_gift_and_the_leader_deposits_what_it_holds_above_the_line(self):
        self.wallet.SWEEP_ENABLED = True
        self.wallet.give, self.wallet.deposit = self.give, self.deposit
        code, text = self.run_sweep()
        self.assertEqual(code, 0)
        self.assertEqual(self.calls, [("give", "miner-1", 40000), ("give", "miner-2", 30000), ("give", "miner-3", 25000), ("give", "miner-4", 20000),
                                      ("deposit", LEADER, 66000)])
        self.assertIn("in a fight: miner-3 gives nothing now; asked again after 10 minutes", text)
        self.assertIn("deposited: Prime Directive 66,000 cr into the faction's treasury", text)
        once = json.loads((self.data / "fleet" / "onetime.json").read_text())
        self.assertEqual(sum(r[3] for r in once if r[2] == "Wallet top-up"), 0)
        self.assertEqual([r[1:] for r in once if r[2] != "Wallet top-up"],
                         [[LEADER, "Faction treasury: credits deposited (the Collective keeps them)", -66000]])
        routes = load(FLEET / "routes.py", "routes_sweep_test")
        self.assertTrue(self.wallet.DEPOSIT_TITLE.startswith(routes.TREASURY))
        os.environ["FLEET_TAXES"] = str(self.data / "fleet" / "taxes.json")             # routes reads the files beside the tax record
        try:
            self.assertEqual([(r[1], r[3]) for r in routes.deposits()], [(LEADER, 66000)])
        finally:
            os.environ["FLEET_TAXES"] = os.devnull
        gifts = [json.loads(line) for line in (self.data / "fleet" / "gifts.jsonl").read_text().splitlines()]
        self.assertEqual([(g["from"], g["to"], g["credits"]) for g in gifts], [("miner-1", LEADER, 40000), ("miner-2", LEADER, 30000), ("miner-4", LEADER, 20000)])
        self.assertEqual(self.wallets[LEADER], 50000)
        # the next pass: the givers on cooldown, miner-3 refused for its fight a moment ago, miner-5 gives; no deposit under the line
        self.calls.clear()
        code, text = self.run_sweep()
        self.assertEqual(self.calls, [("give", "miner-5", 15000)])
        self.assertIn("left out: miner-3 (75,000 cr): refused for a fight 0 min ago", text)
        self.assertIn("no deposit: the leader holds 65,000 cr, under 70,000", text)

    def test_a_gift_the_wallet_does_not_show_and_a_refused_deposit_are_not_booked(self):
        self.wallet.SWEEP_ENABLED, self.wallet.PER_PASS = True, 1
        self.wallets[LEADER] = 95000
        self.write()
        self.wallet.give = lambda donor, pilot, credits: (self.calls.append(("give", donor, credits)), (True, "ok"))[1]   # the wallet never shows it
        self.wallet.deposit = lambda pilot, credits: (self.calls.append(("deposit", pilot, credits)), (False, '{"error": "Two programs never drive one pilot"}'))[1]
        code, text = self.run_sweep()
        self.assertEqual(code, 1)
        self.assertIn("HALT: the gift miner-1 -> Prime Directive 40,000 cr is not booked", text)
        self.assertIn("HALT: the deposit of 45,000 cr was refused", text)
        self.assertFalse((self.data / "fleet" / "onetime.json").exists())
        gifts = [json.loads(line) for line in (self.data / "fleet" / "gifts.jsonl").read_text().splitlines()]
        self.assertEqual([(g["from"], g["credits"], g["unsure"]) for g in gifts], [("miner-1", 0, 40000)])     # on cooldown, booked nowhere
        self.calls.clear()
        self.run_sweep()                                                                     # refused: tried again at the next pass
        self.assertEqual(self.calls, [("give", "miner-2", 30000), ("deposit", LEADER, 45000)])
        os.environ["HERMES_SESSION_PROFILE"] = "zero"
        with self.assertRaises(SystemExit) as stop:
            self.run_sweep()
        self.assertIn("REFUSED: a real sweep is the Fleet Admiral's", str(stop.exception))

    def test_a_deposit_is_checked_in_the_treasury_while_a_gift_reaches_the_leader_s_wallet_late(self):
        # 2026-11-17 20:26 UTC: the fleet file read the leader at 80,898; a gift of 10,146 reached its wallet after that
        # reading, the deposit of 30,898 landed, the wallet read 60,146: the old check kept a deposit that landed unsure.
        self.wallet.SWEEP_ENABLED, self.wallet.PER_PASS = True, 1
        self.wallets = {LEADER: 80898, "miner-1": 60146}
        self.fight = set()
        self.write()
        late, purse = {}, [364095]

        def give(donor, pilot, credits):
            self.calls.append(("give", donor, credits))
            self.wallets[donor] -= credits
            late[pilot] = late.get(pilot, 0) + credits              # reaches the leader's reading only later
            self.write()
            return True, "ok"

        def deposit(pilot, credits):
            self.calls.append(("deposit", pilot, credits))
            self.wallets[pilot] += late.pop(pilot, 0) - credits
            purse[0] += credits
            self.write()
            return True, "ok"
        self.wallet.give, self.wallet.deposit = give, deposit
        self.wallet.treasury_read = lambda pilot: purse[0]
        code, text = self.run_sweep()
        self.assertEqual(self.calls, [("give", "miner-1", 10146), ("deposit", LEADER, 30898)])
        self.assertEqual((code, self.wallets[LEADER], purse[0]), (0, 60146, 394993))
        self.assertIn("deposited: Prime Directive 30,898 cr into the faction's treasury", text)
        once = json.loads((self.data / "fleet" / "onetime.json").read_text())
        self.assertEqual([r[3] for r in once if r[2] != "Wallet top-up"], [-30898])
        # a treasury that does not rise keeps the deposit unsure, whatever the wallet shows
        self.wallet.treasury_read = lambda pilot: 394993
        self.assertFalse(self.wallet.deposit_landed(str(self.data), LEADER, 90000, 30000, 394993))

    def test_a_deposit_the_leader_s_wallet_does_not_show_stops_the_deposits_for_a_while_and_is_not_booked(self):
        self.wallet.SWEEP_ENABLED, self.wallet.PER_PASS = True, 0
        self.wallets[LEADER] = 95000
        self.write()
        self.wallet.deposit = lambda pilot, credits: (self.calls.append(("deposit", pilot, credits)), (True, "ok"))[1]   # answered, never shown
        code, text = self.run_sweep()
        self.assertEqual((code, self.calls), (1, [("deposit", LEADER, 45000)]))
        self.assertIn("HALT: the deposit of 45,000 cr is not booked", text)
        self.assertFalse((self.data / "fleet" / "onetime.json").exists())
        self.calls.clear()
        code, text = self.run_sweep()
        self.assertEqual(self.calls, [])                                                     # no second deposit on top of an unsure one
        self.assertIn("no deposit: the deposit of 45,000 cr at", text)


class HiveFleetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-money-hive-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        self.hive = load(FLEET / "hive.py", "hive_money_test")
        self.collector = load(ROOT / "station" / "fleet.py", "collector_money_hive_test")
        self.collector.DATA = self.data / "fleet"
        self.collector.FLAGSHIPS = {LEADER: {"admiral": "Unity", "division": "Command", "role": "command", "of": "Unity"}}

    def show(self, rates, credits=10302200):
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"updated_at": "", "totals": {"ships": 2, "working": 2, "parked": 0, "adrift": 0,
            "credits": credits, "credits_per_ship": 1, "divisions": {"Command": {"ships": 1, "credits": 1}, "Mining": {"ships": 1, "credits": 1}}, "rates": rates}}))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.hive.show_fleet(str(FLEET.parent), str(self.data), NOW)
        return out.getvalue()

    @staticmethod
    def nets(text):
        return {line.split()[1]: line.split("net ")[1].split(" |")[0] for line in text.splitlines() if line.strip().startswith("last ")}

    def test_the_fleet_prints_the_three_nets_without_a_gift_in_transit_and_the_sum_held_out(self):
        (self.data / "fleet" / "gifts.jsonl").write_text("")
        (self.data / "fleet" / "onetime.json").write_text("[]")
        plain = self.nets(self.show(self.collector.rates(history(), NOW)))
        (self.data / "fleet" / "gifts.jsonl").write_text(json.dumps({"at": T0 + 5 * STEP + 30, "from": "miner-1", "to": LEADER, "credits": 189040}) + "\n")
        (self.data / "fleet" / "onetime.json").write_text(json.dumps([[T0 + 5 * STEP + 30, "miner-1", "Wallet top-up", -189040],
                                                                       [T0 + 5 * STEP + 30, LEADER, "Wallet top-up", 189040],
                                                                       [T0 + 6000, LEADER, "Faction treasury: credits deposited (the Collective keeps them)", -1000]]))
        (self.data / "fleet" / "moves.jsonl").write_text(json.dumps({"at": T0 - 3600, "start": 1}) + "\n"
                                                         + json.dumps({"at": T0 + 6 * STEP, "pilot": "miner-1", "moved": -189040}) + "\n")
        text = self.show(self.collector.rates(history([("Mining", -189040, 6 * STEP)]), NOW))
        self.assertEqual(self.nets(text), plain)
        self.assertEqual(len(plain), 3)
        self.assertIn("held out: 189,040 cr of gifts not yet seen by their receivers", text)
        self.assertIn("into the faction's treasury 1,000 in 1 deposits", text)
        self.assertIn("bought once (tools, goods for a mission) 0 in 0 buys", text)           # a deposit is no buy

    def test_the_headline_puts_the_treasury_beside_the_wallets(self):
        text = self.show(None)
        self.assertIn("  TREASURY | not measured (no reading in", text)
        (self.data / "empire").mkdir()
        (self.data / "empire" / "empire.json").write_text(json.dumps({"written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW - 600)),
                                                                      "faction": {"treasury": 364915}}))
        text = self.show(None)
        self.assertIn("  TREASURY | the faction's treasury 364,915 cr (read 10 min ago by empire.py collect) | fleet money = wallets 10,302,200 + "
                      "treasury 364,915 = 10,667,115 cr", text)
        self.assertTrue(text.splitlines()[0].startswith("FLEET | 2 ships"))                    # the headline itself as it was


if __name__ == "__main__":
    unittest.main()
