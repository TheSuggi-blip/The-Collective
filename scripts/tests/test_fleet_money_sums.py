"""The divisions add up to the fleet (station/fleet.py window): figure by figure and to the credit, in every window,
whoever loads the collector (game/fleet/stats.py loads it by path for stats_money_hour). No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import random
import sys
import tempfile
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"
sys.path.insert(0, str(FLEET))
LEADER = "Prime Directive"
FLAGSHIPS = {LEADER: {"admiral": "Unity", "division": "Command", "role": "command", "of": "Unity"},
             "Hades": {"admiral": "Unity", "division": "Command", "role": "command", "of": "Apophis"}}
TREASURY = "Faction treasury: credits deposited (the Collective keeps them)"
# every figure a reader may sum over the divisions; cph, one_time and total follow from the first four
ADDED = ("income_per_hour", "costs_per_hour", "cph", "rewards_per_hour", "bought_once_per_hour", "one_time_per_hour", "total_per_hour",
         "wallets_per_hour", "transfers_per_hour", "treasury_moved_per_hour", "fuel_cr_per_hour", "repair_cr_per_hour", "metered_per_hour",
         "spent_per_hour", "unexplained_per_hour")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample(t, divisions):
    """A history row as sample() writes it, from {division: [ships, credits, earned, spent, fuel cr, repair cr]}."""
    return [t, sum(v[1] for v in divisions.values()), sum(v[0] for v in divisions.values()), sum(v[2] for v in divisions.values()), 0, 0, 0,
            {d: [v[0], v[1], v[2], 0, 0, 0] for d, v in divisions.items()},
            {"s": sum(v[3] for v in divisions.values()), "ds": {d: v[3] for d, v in divisions.items()},
             "m": [0, sum(v[4] for v in divisions.values()), 0, sum(v[5] for v in divisions.values()), 0],
             "d": {d: [0, v[4], 0, v[5]] for d, v in divisions.items()}}]


def gaps(w):
    """{figure: the fleet's figure less the sum of its divisions'} of one window, the figures that differ."""
    out = {}
    for key in ADDED:
        if key in w:
            gap = w[key] - sum(row.get(key, 0) for row in w["divisions"].values())
            if gap:
                out[key] = gap
    return out


class TheHourThatBrokeTests(unittest.TestCase):
    """2026-11-17 20:00 UTC, stats_money_hour: the fleet -48,148 cr an hour, its divisions -14,053. stats.py loads
    station/fleet.py by path and never read the flagship entries: the leader's gift sides (+65,230 cr) and deposits
    (30,898 cr) counted for no division, and window() showed only the divisions of its end sample."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-sums-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        (self.data / "fleet" / "flagships.json").write_text(json.dumps(FLAGSHIPS))
        self.fleet = load(ROOT / "station" / "fleet.py", "collector_sums_test")
        self.fleet.DATA = self.data / "fleet"

    def hour(self):
        """The hour's shape in small: miner-1 and trader-1 give the leader 30,000 and 35,230, the leader deposits 30,898;
        Mining sells for 4,000 and Command for 1,000 meanwhile."""
        a = sample(0, {"Mining": [1, 50000, 10000, 0, 0, 0], "Trade": [1, 60000, 5000, 0, 0, 0], "Command": [2, 20000, 3000, 0, 0, 0]})
        b = sample(3600, {"Mining": [1, 50000 - 30000 + 4000, 14000, 0, 0, 0], "Trade": [1, 60000 - 35230, 5000, 0, 0, 0],
                          "Command": [2, 20000 + 65230 - 30898 + 1000, 4000, 0, 0, 0]})
        gifts = [(600, "miner-1", LEADER, 30000), (1200, "trader-1", LEADER, 35230)]
        one = [[900, "miner-1", "Wallet top-up", -30000], [900, LEADER, "Wallet top-up", 30000], [1500, LEADER, TREASURY, -30898]]
        return [a, b], one, gifts

    def test_the_divisions_add_up_when_the_reader_did_not_load_the_flagships(self):
        history, one, gifts = self.hour()
        self.fleet.FLAGSHIPS.clear()                                    # as stats.py loaded it: the leader in no division
        w = self.fleet.window(history, 3600, 3600, one, gifts)
        self.assertEqual((w["income_per_hour"], w["costs_per_hour"], w["cph"]), (5000, 0, 5000))      # the fleet: the move is no money
        self.assertEqual(gaps(w), {})                                   # orig: cph 34,332 below the divisions' sum
        self.assertEqual(w["divisions"]["Unassigned"]["wallets_per_hour"], -65230 + 30898)          # what no division held, on a line
        self.assertEqual(w["divisions"]["Command"]["costs_per_hour"], -34332)                        # ... and Command wrong without the entries

    def test_with_the_flagships_loaded_command_holds_the_leader_s_moves(self):
        history, one, gifts = self.hour()
        self.fleet.FLAGSHIPS.update(FLAGSHIPS)
        w = self.fleet.window(history, 3600, 3600, one, gifts)
        self.assertEqual(gaps(w), {})
        self.assertNotIn("Unassigned", w["divisions"])
        self.assertEqual({d: (r["income_per_hour"], r["costs_per_hour"]) for d, r in w["divisions"].items()},
                         {"Mining": (4000, 0), "Trade": (0, 0), "Command": (1000, 0)})

    def test_stats_reads_the_flagship_entries_of_its_data_folder(self):
        import stats
        rule = stats.load_by_path("collector_sums_stats", ROOT / "station" / "fleet.py")
        self.assertEqual(rule.division_of(LEADER)[0], "Unassigned")      # loaded by path: no entries yet
        stats.money_records(str(self.data), rule, 3600)
        self.assertEqual(rule.division_of(LEADER)[0], "Command")

    def test_a_regroup_whose_two_readings_differ_falls_out_of_no_division(self):
        # regroup.jsonl 2026-11-17 19:29:29 UTC (from the samples of 19:28:24 and 19:29:29): Command lost 899,768 cr,
        # Military gained 900,679: the hour from 19:00 read its divisions 919 cr an hour below the fleet.
        self.fleet.ROLES["sentinel"] = ("Military", "Apophis")
        out = {"ships": 20, "credits": 899768, "earned": 1418327, "spent": 320657}
        came = {"ships": 20, "credits": 900679, "earned": 1419764, "spent": 321183}
        a = sample(0, {"Command": [26, 1150003, 1926684, 645047, 0, 0], "Military": [50, 2261480, 3410846, 948120, 0, 0]})
        b = sample(3600, {"Command": [6, 1150003 - 899768 + 2000, 1926684 - 1418327 + 3000, 645047 - 320657 + 1000, 0, 0],
                          "Military": [70, 2261480 + 900679 + 5000, 3410846 + 1419764 + 9000, 948120 + 321183 + 4000, 0, 0]})
        line = (1800, "Command", "Military", (), "sentinel", out, came)
        w = self.fleet.window([a, b], 3600, 3600, [], regroups=[line])
        self.assertEqual(gaps(w), {})                                   # orig: income 1,437, costs 526, net 911 below the fleet
        self.assertEqual((w["divisions"]["Command"]["income_per_hour"], w["divisions"]["Command"]["costs_per_hour"]), (3000, 1000))
        self.assertEqual((w["divisions"]["Military"]["income_per_hour"], w["divisions"]["Military"]["costs_per_hour"]), (9000 + 1437, 4000 + 526))
        self.assertEqual(w["divisions"]["Military"]["regroup"], {"ships": 20, "credits": 899768, "earned": 1418327})


class EveryWindowTests(unittest.TestCase):
    """Random histories with every path that books money: sales, fuel and repairs metered, rewards and goods paid once,
    gifts (whole, one-sided, with a flagship, with a pilot outside every division), deposits into the treasury, pilots
    first seen, pilots the engine stops listing and lists again, ships that change division; every window, both states of
    ONE_SIDED, with and without the flagship entries: the divisions add up to the fleet to the credit."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-sums-random-")
        self.addCleanup(self.temp.cleanup)
        self.fleet = load(ROOT / "station" / "fleet.py", "collector_sums_random")
        self.fleet.DATA = Path(self.temp.name)
        self.fleet.ROLES["sentinel"] = ("Military", "Apophis")

    def world(self, rnd):
        pilots = ["miner-1", "miner-2", "trader-1", "hauler-1", "scout-1", "drone-1", "sentinel-1", LEADER, "Hades", "One of Seven"]
        state = {d: [3, 40000, 10000, 2000, 500, 100] for d in ("Mining", "Trade", "Logistics", "Intel", "Military", "Command")}
        history, one, gifts, seeds, presence, regroups = [], [], [], {}, [], []
        for step in range(150):
            t = 1_800_000_000 + step * 120 + rnd.randint(0, 20)
            for v in state.values():
                v[2] += rnd.randint(0, 3000)
                v[3] += rnd.randint(0, 1500)
                v[1] += rnd.randint(-2500, 3500)
                v[4] += rnd.randint(0, 400)
                v[5] += rnd.randint(0, 90)
            for _ in range(rnd.randint(0, 2)):
                giver, taker = rnd.sample(pilots, 2)
                giver, taker = rnd.choice(((giver, taker), (giver, taker), (giver, ""), ("", taker)))
                gifts.append((t - rnd.randint(0, 400), giver, taker, rnd.randint(1, 40000)))
            if rnd.random() < 0.3:
                one.append([t - 30, rnd.choice(pilots), rnd.choice(("a reward", "goods bought", TREASURY)), rnd.randint(-9000, 9000)])
            if rnd.random() < 0.05:
                seeds["miner-%d" % (10 + step)] = [t - 7, 100, rnd.randint(0, 50), 0]
            if rnd.random() < 0.05:
                presence.append((t - 11, rnd.choice(pilots), rnd.choice((-1, 1)), rnd.randint(0, 9000), rnd.randint(0, 900), rnd.randint(0, 90)))
            if rnd.random() < 0.03:
                frm, to = rnd.sample(sorted(state), 2)
                gone = {"ships": 1, "credits": rnd.randint(0, 9000), "earned": rnd.randint(0, 900), "spent": rnd.randint(0, 90)}
                came = {key: value + rnd.randint(0, 50) for key, value in gone.items()}
                regroups.append((t - 5, frm, to, ("sentinel-1",), "", gone, came))
            history.append(sample(t, {d: list(v) for d, v in state.items()}))
        return history, one, gifts, seeds, presence, regroups

    def test_the_divisions_add_up_to_the_fleet_in_every_window(self):
        rnd = random.Random(20261118)
        checked = 0
        for _world in range(4):
            history, one, gifts, seeds, presence, regroups = self.world(rnd)
            for side in (False, True):
                self.fleet.ONE_SIDED = side
                for flagships in ({}, FLAGSHIPS):
                    self.fleet.FLAGSHIPS.clear()
                    self.fleet.FLAGSHIPS.update(flagships)
                    for _ in range(25):
                        now = rnd.choice(history[5:])[0]
                        seconds = rnd.choice((3600, 6 * 3600, rnd.randint(300, 6 * 3600)))
                        w = self.fleet.window(history, now, seconds, one, gifts, seeds, presence, None, sorted(regroups))
                        if w is None:
                            continue
                        checked += 1
                        self.assertEqual(gaps(w), {}, "window to %s over %s s, ONE_SIDED %s, flagships %s" % (now, seconds, side, bool(flagships)))
                        for row in [w] + list(w["divisions"].values()):
                            self.assertEqual(row["cph"], row["income_per_hour"] - row["costs_per_hour"])
                            self.assertEqual(row["total_per_hour"], row["cph"] + row["one_time_per_hour"])
                    r = self.fleet.rates(history, history[-1][0], one, [(g[0], g[1], g[2], g[3]) for g in gifts], seeds, presence, ([], []), regroups)
                    for key in ("1h", "6h", "24h"):
                        self.assertEqual(gaps(r["windows"][key]), {})
        self.assertGreater(checked, 300)
        self.fleet.ONE_SIDED = False

    def test_a_division_s_figure_stays_within_a_credit_of_its_own_rate(self):
        self.assertEqual(self.fleet.settle(2, {"A": 1, "B": 1, "C": 1}, 2.0, 3), {"A": 1, "B": 1, "C": 0})   # 0.5 each: two of three up
        self.assertEqual(self.fleet.settle(9, {"A": 4, "B": 5}, 1.0, 9), {"A": 4, "B": 5})                    # own rounding when it adds up
        self.assertEqual(self.fleet.settle(-2, {"A": -1, "B": -1, "C": -1}, 2.0, -3), {"A": -1, "B": -1, "C": 0})
        self.assertIsNone(self.fleet.settle(9, {"A": 4, "B": 4}, 1.0, 9))                                    # parts that do not add up: told


if __name__ == "__main__":
    unittest.main()
