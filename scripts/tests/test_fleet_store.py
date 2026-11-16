"""store.py on a disposable data folder: rows and sums of a pass, a record cut by the keeper, a half-written line, the read copy, the backups, old rows, bad lines, a herd gone, the writer's lease."""

import calendar
import contextlib
import importlib.util
import io
import json
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
SCRIPT = ROOT / "game" / "fleet" / "store.py"
KEEPER = ROOT / "scripts" / "data-keeper.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


store = load("store_under_test", SCRIPT)
keeper = load("keeper_beside_store", KEEPER)


def at(text):
    return calendar.timegm(time.strptime(text, "%Y-%m-%dT%H:%M:%SZ"))


NOW = at("2026-11-16T12:00:00Z")
H9, H10, H11 = at("2026-11-16T09:00:00Z"), at("2026-11-16T10:00:00Z"), at("2026-11-16T11:00:00Z")
RUNS, MARKET, WILD = "routes/runs.jsonl", "market/history.jsonl", "wildlife/history.jsonl"


def run(pilot, route, started, minutes, before, after, delta, one_time=0, notes=()):
    return json.dumps({"route": route, "kind": "circuit", "pilot": pilot, "started": started, "minutes": minutes,
                       "credits_before": before, "credits_after": after, "delta": delta, "one_time": one_time,
                       "notes": list(notes)})


def move(t, base, item, bid, ask):
    return json.dumps({"t": t, "base": base, "item": item, "bid": bid, "bid_qty": 10 if bid else 0,
                       "ask": ask, "ask_qty": 5 if ask else 0})


def census(t, system, deposits, herds):
    return json.dumps({"at": t, "system": system, "deposits": deposits, "herds": herds, "pilots": {}})


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-store-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("routes", "market", "wildlife"):
            (self.data / folder).mkdir()

    def append(self, name, lines, end="\n"):
        with open(self.data / name, "a", encoding="ascii") as handle:
            handle.write("".join(line + end for line in lines))

    def one(self, now=NOW, **options):
        return store.one_pass(str(self.data), now=now, **options)

    def live(self, sql, args=()):
        conn = sqlite3.connect(str(self.data / "store" / "live.db"))
        try:
            return conn.execute(sql, args).fetchall()
        finally:
            conn.close()

    def count(self, table):
        return self.live("SELECT COUNT(*) FROM %s" % table)[0][0]

    def offset(self, name):
        return self.live("SELECT offset FROM cursor WHERE record = ?", (name,))[0][0]

    def sums(self):
        return {table: sorted(self.live("SELECT * FROM %s" % table)) for table in ("route_hour", "market_hour", "reading_day")}

    def first_lines(self):
        self.append(RUNS, [
            run("p1", "r1", "2026-11-16T09:05:00Z", 10, 100, 400, 300, one_time=100),
            run("p2", "r1", "2026-11-16T09:20:00Z", 20, 500, 550, 50),
            run("p3", "r1", "2026-11-16T09:40:00Z", 30, 0, 999, 999, notes=["wallet not read"]),
            run("p1", "r2", "2026-11-16T10:10:00Z", 15, 400, 300, -100)])
        self.append(MARKET, [
            move("2026-11-16T09:01:00Z", "b1", "ore", 10, 0),
            move("2026-11-16T09:02:00Z", "b1", "ore", 12, 20),
            move("2026-11-16T09:30:00Z", "b1", "ore", 8, 18),
            move("2026-11-16T10:00:00Z", "b1", "ore", 9, 19)])
        self.append(WILD, [
            census("2026-11-16T09:05:00Z", "s1", {"p1": {"iron": 100, "ice": 50}}, {"p1": {"grazer": 3}}),
            census("2026-11-16T10:05:00Z", "s1", {"p1": {"iron": 80, "ice": 50}}, {"p1": {"grazer": 2}})])

    def test_rows_sums_a_keeper_cut_and_a_half_written_line(self):
        self.first_lines()
        out = self.one()
        self.assertEqual({k: v["added"] for k, v in out["records"].items()}, {RUNS: 4, MARKET: 4, WILD: 6})
        self.assertEqual((self.count("runs"), self.count("moves"), self.count("readings")), (4, 4, 6))
        # by hand: r1 in hour 09: 3 runs, 60 minutes, 30 read (p3 read no wallet), credits (300-100)+50 = 250, one_time 100
        self.assertEqual(self.live("SELECT runs, minutes, read_minutes, credits, one_time FROM route_hour WHERE route = 'r1' AND hour = ?",
                                   (H9,)), [(3, 60.0, 30.0, 250.0, 100.0)])
        self.assertEqual(self.live("SELECT bid_lo, bid_hi, ask_lo, ask_hi, moves FROM market_hour WHERE hour = ?", (H9,)),
                         [(8.0, 12.0, 18.0, 20.0, 3)])                  # the ask of 0 is no price
        self.assertEqual(self.live("SELECT first, last FROM reading_day WHERE what = 'iron'"), [(100.0, 80.0)])

        self.append(RUNS, [run("p2", "r2", "2026-11-16T10:30:00Z", 25, 300, 600, 300)])
        self.append(MARKET, [move("2026-11-16T10:20:00Z", "b1", "ore", 11, 21), move("2026-11-16T10:21:00Z", "b2", "gas", 3, 4)])
        self.one()
        self.assertEqual((self.count("runs"), self.count("moves")), (5, 6))
        before = self.sums()
        offsets = {name: self.offset(name) for name in (RUNS, MARKET)}

        for name in (RUNS, MARKET):                 # the keeper's own cut: the newest part stays, the file is shorter
            size = (self.data / name).stat().st_size
            self.assertIsNotNone(keeper.trim(self.data, name, size - 1, size // 2, settle=0.01))
            self.assertLess((self.data / name).stat().st_size, offsets[name])
        self.append(RUNS, [run("p3", "r2", "2026-11-16T11:10:00Z", 5, 600, 700, 100)])
        self.append(MARKET, [move("2026-11-16T11:05:00Z", "b1", "ore", 13, 22)])
        out = self.one()
        self.assertTrue(out["records"][RUNS]["cut"] and out["records"][MARKET]["cut"])
        self.assertEqual((out["records"][RUNS]["added"], out["records"][MARKET]["added"]), (1, 1))
        self.assertEqual((self.count("runs"), self.count("moves"), self.count("readings")), (6, 7, 6))
        self.assertEqual(self.live("SELECT COUNT(*) FROM (SELECT pilot, route, started FROM runs GROUP BY 1, 2, 3)")[0][0], 6)
        after = self.sums()
        for table, rows in before.items():          # every hour before the cut is unchanged, the new hour is there
            self.assertEqual([r for r in after[table] if r not in rows and H11 not in r], [], table)
            self.assertEqual([r for r in rows if r not in after[table]], [], table)
        self.assertEqual(self.live("SELECT runs, credits FROM route_hour WHERE route = 'r2' AND hour = ?", (H11,)), [(1, 100.0)])

        whole = run("p4", "r2", "2026-11-16T11:30:00Z", 5, 700, 800, 100)
        size = (self.data / RUNS).stat().st_size
        self.append(RUNS, [whole[:40]], end="")     # half written: no newline yet
        out = self.one()
        self.assertEqual((out["records"][RUNS]["added"], out["records"][RUNS]["bad"], self.count("runs")), (0, 0, 6))
        self.assertEqual(self.offset(RUNS), size)
        self.append(RUNS, [whole[40:]])
        out = self.one()
        self.assertEqual((out["records"][RUNS]["added"], self.count("runs")), (1, 7))
        self.assertEqual(self.offset(RUNS), (self.data / RUNS).stat().st_size)

    def test_a_cut_record_that_grew_past_its_old_place_is_read_again(self):
        self.append(MARKET, [move("2026-11-16T09:%02d:00Z" % m, "b1", "ore", 10 + m, 0) for m in range(10)])
        self.one()
        old = self.offset(MARKET)
        size = (self.data / MARKET).stat().st_size
        keeper.trim(self.data, MARKET, size - 1, size // 2, settle=0.01)
        self.append(MARKET, [move("2026-11-16T10:%02d:00Z" % m, "b1", "ore", 30 + m, 0) for m in range(10)])
        self.assertGreater((self.data / MARKET).stat().st_size, old)       # longer than before: only the first line tells
        out = self.one()
        self.assertTrue(out["records"][MARKET]["cut"])
        self.assertEqual((out["records"][MARKET]["added"], self.count("moves")), (10, 20))

    def test_a_record_shorter_than_its_place_is_read_again_by_its_size_alone(self):
        self.addCleanup(setattr, store, "HEAD", store.HEAD)
        store.HEAD = 8                              # no first line is whole within 8 bytes: no mark, the size alone tells
        self.append(MARKET, [move("2026-11-16T09:%02d:00Z" % m, "b1", "ore", 10 + m, 0) for m in range(10)])
        self.one()
        self.assertEqual(self.live("SELECT head FROM cursor WHERE record = ?", (MARKET,)), [("",)])
        size = (self.data / MARKET).stat().st_size
        keeper.trim(self.data, MARKET, size - 1, size // 2, settle=0.01)
        self.append(MARKET, [move("2026-11-16T10:00:00Z", "b1", "ore", 40, 0)])
        out = self.one()
        self.assertTrue(out["records"][MARKET]["cut"])
        self.assertEqual((out["records"][MARKET]["added"], self.count("moves")), (1, 11))

    def test_the_read_copy_is_immutable_and_route_rates_gives_the_hand_figure(self):
        self.assertIsNone(store.connect(str(self.data)))
        self.first_lines()
        self.assertTrue(self.one()["published"])
        self.assertEqual(self.live("PRAGMA journal_mode"), [("wal",)])
        self.assertNotEqual((self.data / "store" / "read.db").read_bytes()[18:20], b"\x02\x02")   # the copy is no WAL file
        conn = store.connect(str(self.data))
        self.addCleanup(conn.close)
        self.assertTrue(conn.execute("PRAGMA database_list").fetchall()[0][2].endswith("read.db"))
        with self.assertRaises(sqlite3.OperationalError):
            conn.execute("INSERT INTO meta VALUES ('x', 1)")
        rates = store.route_rates(conn, H9 + 600)                          # from the hour that holds 09:10 on
        self.assertEqual(rates["r1"], (3, 30.0, 250.0, 100.0, 500.0))      # 60 * 250 / 30
        self.assertEqual(rates["r2"], (1, 15.0, -100.0, 0.0, -400.0))
        self.assertEqual(sorted(store.route_rates(conn, H10)), ["r2"])
        names = sorted(p.name for p in (self.data / "store").iterdir())
        self.assertEqual([n for n in names if n.endswith(".tmp")], [])

    def test_a_run_earns_what_the_fleets_one_rule_says(self):
        # a hunt that sold 5 curd for 500 cr but gained only 2 of them here: 3/5 of the sale is not this run's
        hunt = {"route": "hunt-a", "kind": "hunt", "pilot": "p1", "started": "2026-11-16T09:05:00Z", "minutes": 30, "credits_before": 1000,
                "credits_after": 1600, "delta": 600, "one_time": 50, "goods": {"curd": 2}, "sold": {"curd": [5, 100, 500]}, "notes": []}
        broken = dict(hunt, pilot="p2", sold={"curd": [5]})                                    # goods that cannot be read: the plain delta
        self.append(RUNS, [json.dumps(hunt), json.dumps(broken)])
        self.one()
        routes = load("routes_beside_store", ROOT / "game" / "fleet" / "routes.py")
        self.assertEqual(routes.earned(hunt), 300.0)
        self.assertEqual(self.live("SELECT pilot, credits FROM runs ORDER BY pilot"), [("p1", routes.earned(hunt) - 50), ("p2", 550.0)])
        self.assertEqual(self.live("SELECT runs, read_minutes, credits, one_time FROM route_hour"), [(2, 60.0, 800.0, 100.0)])

    def test_a_mended_record_has_the_raw_runs_counted_again(self):
        self.first_lines()
        self.one()
        self.assertEqual(self.live("SELECT credits FROM runs WHERE pilot = 'p2'"), [(50.0,)])
        self.assertEqual(self.live("SELECT value FROM meta WHERE key = 'earned.rule'"), [(store.EARNED_RULE,)])
        fleet = self.data / "fleet"
        fleet.mkdir(exist_ok=True)
        os.environ["FLEET_TAXES"] = str(fleet / "taxes.json")                                  # the gifts lie beside the tax record
        self.addCleanup(os.environ.__setitem__, "FLEET_TAXES", os.devnull)
        at = calendar.timegm(time.strptime("2026-11-16T09:25:00", "%Y-%m-%dT%H:%M:%S"))
        (fleet / "gifts.jsonl").write_text(json.dumps({"at": at, "from": "p2", "to": "p9", "credits": 30}) + "\n")   # p2 gave 30 cr while its run flew
        self.assertEqual(self.one()["recounted"], 0)                                           # nobody asked: the rows stand
        self.assertEqual(self.live("SELECT credits FROM runs WHERE pilot = 'p2'"), [(50.0,)])
        self.assertEqual(store.main(["recount", "--data", str(self.data)]), 0)
        out = self.one()
        self.assertEqual((out["recounted"], out["published"]), (1, True))
        self.assertIn("1 runs counted again", store.said(out))
        self.assertEqual(self.live("SELECT credits FROM runs WHERE pilot = 'p2'"), [(80.0,)])
        self.assertEqual(self.live("SELECT credits FROM route_hour WHERE route = 'r1'"), [(280.0,)])    # 200 + 80: the hour is summed again
        self.assertFalse((self.data / "store" / "recount").exists())
        self.assertEqual(self.one()["recounted"], 0)

    def test_six_daily_backups_leave_five(self):
        days = [at("2026-11-%02dT00:05:00Z" % d) for d in range(10, 16)]
        for day in days:
            self.assertIsNotNone(self.one(now=day)["backup"])
            self.assertIsNone(self.one(now=day + 3600)["backup"])            # once a day
        kept = sorted(p.name for p in (self.data / "store" / "backup").iterdir())
        self.assertEqual(kept, ["collective-2026-11-%02d.db" % d for d in range(11, 16)])
        conn = sqlite3.connect("file:%s?mode=ro&immutable=1" % (self.data / "store" / "backup" / kept[-1]), uri=True)
        self.addCleanup(conn.close)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM runs").fetchone(), (0,))

    def test_old_raw_rows_go_their_sums_stay_and_a_line_of_a_sealed_hour_is_not_taken(self):
        old = run("p1", "r9", "2026-11-05T09:05:00Z", 10, 100, 200, 100)
        self.append(RUNS, [old, run("p1", "r9", "2026-11-16T09:05:00Z", 10, 200, 260, 60)])
        out = self.one()
        self.assertEqual(out["pruned"], 1)
        self.assertEqual(self.count("runs"), 1)
        self.assertEqual(self.live("SELECT hour, credits FROM route_hour ORDER BY hour"),
                         [(at("2026-11-05T09:00:00Z"), 100.0), (H9, 60.0)])
        self.append(RUNS, [old])
        out = self.one()
        self.assertEqual((out["records"][RUNS]["added"], out["records"][RUNS]["old"], self.count("runs")), (0, 1, 1))
        self.assertEqual(self.live("SELECT COUNT(*) FROM route_hour")[0][0], 2)

    def test_bad_lines_are_skipped_and_counted(self):
        self.append(RUNS, ["{not json", "[1, 2]", json.dumps({"route": "r1", "started": "2026-11-16T09:00:00Z"}),
                           run("p1", "r1", "yesterday", 5, 1, 2, 1),
                           run("p1", "r1", "2026-11-16T09:05:00Z", 10, 100, 400, 300), ""])
        out = self.one()
        self.assertEqual((out["records"][RUNS]["added"], out["records"][RUNS]["bad"]), (1, 4))
        self.assertIn("4 bad", store.said(out))

    def test_a_herd_its_place_no_longer_lists_stands_at_zero_once(self):
        self.append(WILD, [census("2026-11-16T09:00:00Z", "s1", {}, {"p1": {"grazer": 3, "ray": 2}, "p2": {"whale": 1}}),
                           census("2026-11-16T10:00:00Z", "s1", {}, {"p1": {"grazer": 1}}),
                           census("2026-11-16T11:00:00Z", "s1", {}, {"p1": {"grazer": 1}})])
        self.one()
        self.assertEqual(self.live("SELECT what, amount, t FROM readings WHERE what = 'ray' ORDER BY t"),
                         [("ray", 2.0, H9), ("ray", 0.0, H10)])
        self.assertEqual(self.live("SELECT amount FROM readings WHERE what = 'whale'"), [(1.0,)])   # p2 not counted again: unknown
        self.assertEqual(self.live("SELECT first, last FROM reading_day WHERE what = 'ray'"), [(2.0, 0.0)])

    def test_one_writer_holds_the_lease(self):
        data = str(self.data)
        self.assertIsNone(store.lease(data, me="other-box 7"))
        self.assertIsNone(store.lease(data, me="other-box 7"))                       # renewed by its holder
        self.assertIn("other-box 7", store.lease(data, me="this-box 8"))
        with contextlib.redirect_stdout(io.StringIO()) as said:
            self.assertEqual(store.main(["once", "--data", data]), 1)               # `once` refused beside a living serve
        self.assertIn("lease is held by other-box 7", said.getvalue())
        self.assertFalse((self.data / "store" / "live.db").exists())
        stale = time.time() - store.LEASE_FRESH - 5
        os.utime(self.data / "store" / "writer.lease", (stale, stale))
        self.assertIsNone(store.lease(data, me="this-box 8"))                        # a stale lease is taken over
        store.release(data, me="this-box 8")
        self.assertFalse((self.data / "store" / "writer.lease").exists())

    def test_once_and_status_from_the_command_line(self):
        self.first_lines()
        command = [sys.executable, "-I", "-B", str(SCRIPT)]
        done = subprocess.run(command + ["status", "--data", str(self.data)], capture_output=True, text=True, timeout=60)
        self.assertIn("no read copy yet", done.stdout)
        done = subprocess.run(command + ["once", "--data", str(self.data)], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("routes/runs.jsonl +4", done.stdout)
        self.assertFalse((self.data / "store" / "writer.lease").exists())
        done = subprocess.run(command + ["status", "--data", str(self.data)], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertRegex(done.stdout, r"runs\s+4 rows\s+newest 2026-11-16T10:10:00Z")
        self.assertRegex(done.stdout, r"route_hour\s+2 rows")


if __name__ == "__main__":
    unittest.main()
