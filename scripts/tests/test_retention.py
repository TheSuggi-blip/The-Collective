"""retention.py through the store's pass on a disposable data folder: off, nothing of the tables once kept for good goes;
on, what is older than its days goes in bounded batches, the young rows, the newest versions of every section and the sums
whose raw rows still stand stay; an empty routes table takes no author; the dry run reads only; and no table of the
store is kept for good without a rule or a word on what bounds it."""

import calendar
import hashlib
import importlib.util
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


store = load("store_for_retention", FLEET / "store.py")
DAY = 86400
NOW = calendar.timegm(time.strptime("2026-11-16T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ"))
HOUR0 = NOW // 3600 * 3600


class Retention(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="retention-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.rules = store.retention                      # the module the store's prune calls: a test sets its switch itself
        for name in ("RETAIN_ENABLED", "RETAIN_BATCH"):
            self.addCleanup(setattr, self.rules, name, getattr(self.rules, name))
        store.one_pass(str(self.data), now=NOW)          # the tables, the snapshot (the routes of the repository)

    def db(self):
        conn = sqlite3.connect(str(self.data / "store" / "live.db"), isolation_level=None)
        self.addCleanup(conn.close)
        return conn

    def plant(self):
        """Rows of every table once kept for good, old and young; the ids of a route of the repository's files."""
        conn = self.db()
        route = conn.execute("SELECT id FROM routes ORDER BY id LIMIT 1").fetchone()[0]
        old, young = HOUR0 - 100 * DAY, HOUR0 - 10 * DAY
        conn.executemany("INSERT INTO route_hour VALUES (?,?,1,10,10,100,0)", [("old-route", old - i * 3600) for i in range(5)] + [("old-route", young)])
        conn.executemany("INSERT INTO market_hour VALUES ('b1','ore',?,1,2,3,4,1)", [(old,), (old - 3600,), (young,)])
        conn.executemany("INSERT INTO reading_day VALUES ('s1','p1','iron','field',?,1,1,0,0)", [(HOUR0 // DAY * DAY - 401 * DAY,), (HOUR0 // DAY * DAY - 399 * DAY,)])
        conn.executemany("INSERT INTO stats_money_hour (hour, division, t) VALUES (?, 'Fleet', 0)", [(old,), (old - 3600,), (young,)])
        conn.executemany("INSERT INTO stats_supply_hour (hour, chain, t) VALUES (?, 'fuel', 0)", [(old,), (young,)])
        for section, seen in (("a", NOW - 40 * DAY), ("b", NOW - 10 * DAY)):
            conn.executemany("INSERT INTO doc_versions (path, section, sha, title, text, first_seen, last_seen) VALUES ('test/x.md', ?, ?, 't', 'x', ?, ?)",
                             [(section, "%s%02d" % (section, i), seen - 3600, seen) for i in range(25)])
        conn.execute("INSERT INTO doc_versions (path, section, sha, title, text, first_seen, last_seen) VALUES ('test/gone.md', 'c', 'c0', 't', 'x', ?, ?)",
                     (NOW - 200 * DAY, NOW - 100 * DAY))
        conn.executemany("INSERT OR REPLACE INTO stats_route_author VALUES (?, 'Unity', 'Unity', 'Command', 0, ?)",
                         [("gone-long-ago", NOW - 100 * DAY), ("old-route", NOW - 100 * DAY), (route, NOW - 100 * DAY)])
        conn.execute("INSERT INTO route_hour VALUES ('old-route', ?, 1, 10, 10, 100, 0)", (HOUR0 - 20 * DAY,))      # it flew 20 days ago
        return route

    def counts(self):
        conn = self.db()
        q = lambda sql: conn.execute(sql).fetchone()[0]
        return {"route_hour": q("SELECT COUNT(*) FROM route_hour WHERE route = 'old-route'"), "market_hour": q("SELECT COUNT(*) FROM market_hour"),
                "reading_day": q("SELECT COUNT(*) FROM reading_day"), "stats_money_hour": q("SELECT COUNT(*) FROM stats_money_hour WHERE t = 0"),
                "stats_supply_hour": q("SELECT COUNT(*) FROM stats_supply_hour WHERE t = 0"),
                "a": q("SELECT COUNT(*) FROM doc_versions WHERE path = 'test/x.md' AND section = 'a'"),
                "b": q("SELECT COUNT(*) FROM doc_versions WHERE path = 'test/x.md' AND section = 'b'"),
                "c": q("SELECT COUNT(*) FROM doc_versions WHERE path = 'test/gone.md'"),
                "authors": q("SELECT COUNT(*) FROM stats_route_author WHERE t = %d" % (NOW - 100 * DAY))}

    def test_off_nothing_of_the_tables_kept_for_good_goes(self):
        self.rules.RETAIN_ENABLED = False
        self.plant()
        before = self.counts()
        out = store.one_pass(str(self.data), now=NOW + 60)
        self.assertEqual(self.counts(), before)
        self.assertEqual(out["pruned"], 0)
        self.assertIsNone(self.db().execute("SELECT value FROM meta WHERE key = 'retain.at'").fetchone())     # off: nothing written either

    def test_on_old_rows_go_in_bounded_batches_and_what_a_reader_needs_stays(self):
        self.rules.RETAIN_ENABLED, self.rules.RETAIN_BATCH = True, 3
        route = self.plant()
        self.assertEqual(self.counts(), {"route_hour": 7, "market_hour": 3, "reading_day": 2, "stats_money_hour": 3, "stats_supply_hour": 2,
                                         "a": 25, "b": 25, "c": 1, "authors": 3})
        first = store.one_pass(str(self.data), now=NOW + 60)
        self.assertEqual(self.counts()["route_hour"], 4)                        # 3 of the 5 old hours: one batch, one transaction
        self.assertEqual(self.counts()["a"], 22)
        self.assertEqual(self.db().execute("SELECT value FROM meta WHERE key = 'retain.more'").fetchone()[0], 1)
        store.one_pass(str(self.data), now=NOW + 120)                           # a table had more than a batch: the very next pass goes on
        self.assertEqual(self.counts(), {"route_hour": 2, "market_hour": 1, "reading_day": 1, "stats_money_hour": 1, "stats_supply_hour": 1,
                                         "a": 20, "b": 25, "c": 1, "authors": 2})
        self.assertGreaterEqual(first["pruned"], 3)
        conn = self.db()
        self.assertEqual([r for (r,) in conn.execute("SELECT route FROM stats_route_author WHERE t = ? ORDER BY route", (NOW - 100 * DAY,))],
                         sorted(["old-route", route]))                         # gone and not flown in 90 days: gone; flown 20 days ago, or its file stands: stays
        self.assertEqual([s for (s,) in conn.execute("SELECT sha FROM doc_versions WHERE section = 'a' ORDER BY version")], ["a%02d" % i for i in range(5, 25)])
        self.assertEqual(conn.execute("SELECT value FROM meta WHERE key = 'retain.more'").fetchone()[0], 0)
        third = store.one_pass(str(self.data), now=NOW + 180)                   # nothing more, and not due again before an hour
        self.assertEqual(third["pruned"], 0)

    def test_a_sum_never_goes_while_its_raw_rows_stand(self):
        self.rules.RETAIN_ENABLED = True
        self.plant()
        store.one_pass(str(self.data), now=NOW + 60, keep_days=120)            # raw rows kept 120 days: the 100-day-old hours stay
        self.assertEqual(self.counts()["route_hour"], 7)
        self.assertEqual(self.counts()["reading_day"], 1)                       # 401 days: older than 121 too

    def test_an_empty_routes_table_takes_no_author(self):
        conn = sqlite3.connect(":memory:", isolation_level=None)
        self.addCleanup(conn.close)
        conn.executescript("CREATE TABLE meta (key TEXT PRIMARY KEY, value); CREATE TABLE routes (id TEXT); "
                           "CREATE TABLE route_hour (route TEXT, hour INTEGER); "
                           "CREATE TABLE stats_route_author (route TEXT PRIMARY KEY, author TEXT, member TEXT, division TEXT, added INTEGER, t INTEGER);"
                           "INSERT INTO stats_route_author VALUES ('r', 'a', 'Unity', 'Command', 0, 0);")
        self.assertEqual(self.rules.apply(conn, NOW, 7, enabled=True), 0)
        conn.execute("INSERT INTO routes VALUES ('other')")
        conn.execute("DELETE FROM meta")
        self.assertEqual(self.rules.apply(conn, NOW, 7, enabled=True), 1)

    def test_the_dry_run_reads_only_and_counts_what_would_go(self):
        self.plant()
        path = self.data / "copy.db"                                            # a copy as read.db is one: VACUUM INTO, no WAL beside it
        self.db().execute("VACUUM INTO ?", (str(path),))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        done = subprocess.run([sys.executable, "-I", "-B", str(FLEET / "retention.py"), "--dry-run", "--db", str(path), "--now", str(NOW)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("the switch retention.RETAIN_ENABLED is OFF", done.stdout)
        line = lambda table: next(l for l in done.stdout.splitlines() if l.startswith("  %s " % table))
        self.assertIn("would go now: 5 |", line("route_hour"))
        self.assertIn("would go now: 5 |", line("doc_versions"))
        self.assertIn("would go now: 1 |", line("stats_route_author"))
        self.assertIn("in a year at today's rate:", line("market_hour"))
        self.assertIn("no rule: one row per pilot and key", line("stats_pilot_last"))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_no_table_is_kept_for_good_without_a_rule_or_a_bound(self):
        handbook = load("handbook_for_retention", ROOT / "scripts" / "handbook.py")
        kept = {name: entry["keep"] for name, entry in handbook.describe(handbook.modules(ROOT))}
        self.assertEqual([name for name, text in kept.items() if text.startswith("for good: no step")], [])
        self.assertTrue(kept["market_hour"].startswith("for good while retention.py RETAIN_ENABLED is off; on: 90 days"))
        self.assertTrue(self.rules.kept("market_hour", True).startswith("90 days by `hour`"))
        self.assertTrue(kept["cursor"].startswith("for good, bounded"))


if __name__ == "__main__":
    unittest.main()
