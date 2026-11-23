"""game/fleet/stats.py on a disposable store and data folder: the robust band of an alert (median and MAD), a recovery
event of a bid, a ship's state against its route's class, the pilots' hourly samples and the XP per hour read, the money
of a whole hour by the collector's own window(), and a whole computation on a fleet with no ship (the pause) whose
views say `not measured`. No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
ROOT = FLEET.parent
sys.path.insert(0, str(FLEET))


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stats = load("stats")
store = load("store")
H = 3600
T0 = 1_800_000_000 // H * H                       # a whole UTC hour


class StatsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-stats-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("fleet/ships", "catalog", "store", "empire", "market", "stock", "routes"):
            (self.data / folder).mkdir(parents=True)
        self.conn = sqlite3.connect(":memory:", isolation_level=None)
        self.addCleanup(self.conn.close)
        self.conn.executescript(store.SCHEMA + store.snapshot_schema())
        stats.setup(self.conn)
        stats.ROLE_MEMO.clear()
        stats.CACHE.clear()

    def test_the_band_is_median_plus_minus_three_scaled_mads_and_needs_a_day_of_hours(self):
        self.assertEqual(stats.mad([1, 2, 3, 4, 100]), 1)                     # the outlier does not move the spread
        m, d, low, high, out = stats.band([10, 11, 9, 10, 12, 8, 10], 30)
        self.assertEqual((m, d, out), (10, 1, "HIGH"))
        self.assertAlmostEqual(high, 10 + 3 * 1.4826)
        self.assertEqual(stats.band([5, 5, 5], 9)[4], "")                      # no spread: never judged
        hours = {T0 + n * H: 100.0 + (n % 3) for n in range(30)}
        hours[T0 + 30 * H] = 500.0
        row = stats.alert_row("x", hours, T0 + 30 * H)
        self.assertTrue(row[5].startswith("OUT HIGH"), row)
        self.assertEqual(row[4], 30)
        short = stats.alert_row("x", {T0 + n * H: 1.0 for n in range(5)}, T0 + 4 * H)
        self.assertTrue(short[5].startswith("not judged"), short)

    def test_a_recovery_is_what_came_back_after_a_take_before_the_next(self):
        step = lambda a, b: (max(0, b[1] - a[1]), max(0, a[1] - b[1]))
        seen = [(0, 100), (600, 40), (1800, 70), (3000, 100), (3600, 20), (4200, 20)]
        # a take at 600, 60 back by 3000 (40 minutes): 90 an hour; the second take has no rise after it: no event
        self.assertEqual(stats.recoveries(seen, step), [(90.0, 600)])
        self.assertEqual(stats.recoveries([(0, 5), (60, 9)], step), [])        # a rise with no take before it is no event

    def test_a_ships_state_is_its_routes_class_against_its_role(self):
        routes = {"m": {"id": "m", "kind": "mine", "belt": "a:b", "station": "a:b:c"}, "h": {"id": "h", "kind": "hunt", "place": "a:b"},
                  "p": {"id": "p", "kind": "circuit", "park": True}}
        state = lambda role, flies, status="connected", activity="", docked=0: stats.ship_state(role, status, flies, activity, docked, routes)
        self.assertEqual(state("miner", "mine m"), "own")
        self.assertEqual(state("trader", "mine m"), "other")
        self.assertEqual(state("drone", "hunt h"), "own")
        self.assertEqual(state("miner", "circuit p"), "docked")               # a park route is no work
        self.assertEqual(state("miner", "mine gone"), "other")                # a route file not read: not its own class
        self.assertEqual(state("miner", "hand Zero"), "hand")
        self.assertEqual(state("miner", None, activity="goal go-to-poi"), "hand")
        self.assertEqual(state("miner", None, docked=1), "docked")
        self.assertEqual(state("miner", None), "space")
        self.assertEqual(state("miner", "mine m", status="offline"), "offline")

    def test_xp_is_gained_over_the_hours_a_pilot_was_read(self):
        (self.data / "catalog" / "1.json").write_text(json.dumps({"skills": [{"id": "piloting", "xp_per_level": [100] * 60}]}))
        self.conn.execute("INSERT INTO ships (pilot, role, src) VALUES ('miner-1', 'miner', 'x')")
        self.conn.execute("INSERT INTO ship_skills (pilot, skill, level, xp, src) VALUES ('miner-1', 'piloting', 9, 40, 'x')")
        self.assertEqual(stats.sample_pilots(self.conn, str(self.data), T0), 2)          # piloting and read_hours, gain NULL
        self.conn.execute("UPDATE ship_skills SET xp = 70")
        self.assertEqual(stats.sample_pilots(self.conn, str(self.data), T0 + 2 * H), 2)
        gain = self.conn.execute("SELECT gain FROM stats_pilot_hour WHERE key = 'piloting' AND gain IS NOT NULL").fetchone()[0]
        self.assertEqual(gain, 30)
        rows = {(r[0], r[1]): r for r in stats.figures_xp(self.conn, str(self.data), str(ROOT), T0 + 2 * H + 60, 24)}
        self.assertAlmostEqual(rows[("miner|piloting", "xp_per_ship_hour")][3], 15.0)     # 30 XP over the 2 hours between the readings
        to_tier = rows[("miner-1", "hours_to_tier")]
        self.assertAlmostEqual(to_tier[3], (1000 - 970) / 15.0)                             # 30 XP to Piloting 10 at 15 an hour
        self.assertEqual(stats.sample_pilots(self.conn, str(self.data), T0 + 3 * H), 1)     # nothing moved: only the reading itself

    def test_a_whole_hour_is_the_collectors_own_window_over_its_samples(self):
        rule = stats.collector(str(ROOT))
        history = []
        for n in range(14):                                                                 # two whole hours of samples, ten minutes apart
            t = T0 - 60 + n * 600
            credits, earned = 50_000 + 1_000 * n, 2_000 * n
            history.append([t, credits, 2, earned, 0, 0, 0, {"Mining": [2, credits, earned, 0, 0, 0]}, {"w": [2, 0, 0]}])
        (self.data / "fleet" / "history.json").write_text(json.dumps(history))
        self.assertEqual(stats.sample_money(self.conn, str(self.data), str(ROOT), T0 + 3 * H), 4)   # Fleet and Mining, two hours
        piece = stats.hour_slice(history, T0)
        records = stats.money_records(str(self.data), rule, T0 + 3 * H)
        w = rule.window(piece, piece[-1][0], piece[-1][0] - piece[0][0], *records)
        row = self.conn.execute("SELECT income, costs, net, idle, ships FROM stats_money_hour WHERE division = 'Fleet' AND hour = ?", (T0,)).fetchone()
        self.assertEqual(row[:3], (w["income_per_hour"], w["costs_per_hour"], w["cph"]))
        self.assertEqual((row[3], row[4]), (0.0, 2))
        self.assertEqual(stats.sample_money(self.conn, str(self.data), str(ROOT), T0 + 3 * H), 0)    # an hour is written once
        got = stats.tiled(self.conn, "Fleet", T0, T0 + 2 * H)
        self.assertEqual(got["n"], 2)
        self.assertIsNone(stats.hour_slice(history, T0 + 5 * H))                           # no samples: no hour

    def test_an_hour_written_before_its_bookings_settled_is_written_once_more(self):
        # 2026-11-23: the weekly tax of 12:57 UTC was booked at 13:07 UTC, after the 12:00 UTC hour was written (13:00:36);
        # the hour read -932,716 cr steady net for good and fired the alert and the trend
        history = []
        for n in range(14):
            t = T0 - 60 + n * 600
            credits, earned = 50_000 + 1_000 * n, 2_000 * n
            history.append([t, credits, 2, earned, 0, 0, 0, {"Mining": [2, credits, earned, 0, 0, 0]}, {"w": [2, 0, 0]}])
        (self.data / "fleet" / "history.json").write_text(json.dumps(history))
        self.assertEqual(stats.sample_money(self.conn, str(self.data), str(ROOT), T0 + H + 120), 4)
        first = self.conn.execute("SELECT t FROM stats_money_hour WHERE division = 'Fleet' AND hour = ?", (T0,)).fetchone()[0]
        self.assertEqual(stats.sample_money(self.conn, str(self.data), str(ROOT), T0 + H + 600), 0)    # not settled yet: kept
        self.assertEqual(stats.sample_money(self.conn, str(self.data), str(ROOT), T0 + 3 * H), 4)      # settled: written once more
        again = self.conn.execute("SELECT t FROM stats_money_hour WHERE division = 'Fleet' AND hour = ?", (T0,)).fetchone()[0]
        self.assertEqual((first, again), (T0 + H + 120, T0 + 3 * H))
        self.assertEqual(stats.sample_money(self.conn, str(self.data), str(ROOT), T0 + 4 * H), 0)      # and never again

    def test_a_fleet_with_no_ship_is_computed_and_every_view_says_not_measured(self):
        read = self.data / "store" / "read.db"
        conn = sqlite3.connect(str(read), isolation_level=None)
        conn.executescript(store.SCHEMA + store.snapshot_schema())
        out = stats.compute(conn, str(self.data), str(ROOT), time.time())
        self.assertEqual(out["errors"], [])
        self.assertEqual(set(out["parts"]), set(stats.PARTS))
        self.assertEqual(stats.compute(conn, str(self.data), str(ROOT), time.time())["parts"], {})    # nothing due again at once
        conn.close()
        for view in stats.SHOW:
            with contextlib.redirect_stdout(io.StringIO()) as printed:
                self.assertEqual(stats.main([view, "--data", str(self.data)]), 0, view)
            self.assertIn("STATS %s" % view.upper(), printed.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            stats.main(["upgrades", "--data", str(self.data)])
        self.assertIn("not measured: no ship", printed.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(stats.main(["nothing", "--data", str(self.data)]), 2)
            self.assertEqual(stats.main(["kpi", "--member", "Nobody", "--data", str(self.data)]), 1)

    def test_a_part_that_fails_is_named_and_the_others_run(self):
        stats.CACHE["collector"] = None                                                    # money: the rule is missing
        (self.data / "fleet" / "history.json").write_text(json.dumps([[T0, 1, 1, 0, 0, 0, 0, {}], [T0 + 2 * H, 2, 1, 0, 0, 0, 0, {}]]))
        out = stats.compute(self.conn, str(self.data), str(ROOT), T0 + 3 * H)
        self.assertEqual([e.split(":")[0] for e in out["errors"]], ["money"])
        self.assertIn("figures", out["parts"])
        self.assertIn("AttributeError", stats.meta_get(self.conn, "stats.money.error"))

    def test_the_store_carries_the_tables_their_descriptions_and_examples(self):
        for table in stats.TABLES:
            self.assertIn(table, store.DESCRIPTIONS)
            self.assertEqual(len(store.EXAMPLES[table]), 3, table)
            for _question, sql in store.EXAMPLES[table]:
                self.conn.execute(sql).fetchall()                                          # every example runs on an empty store


if __name__ == "__main__":
    unittest.main()
