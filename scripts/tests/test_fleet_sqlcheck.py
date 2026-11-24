"""sqlcheck.py: a literal query the store's schema refuses is named (errors.log ENT-194: hunt_net and mine_net asked
the table stations for columns it does not have and read an empty world for hours). On a disposable database; the
last test runs the check over the real scripts against the store's read copy when it exists."""

import importlib.util
import io
import os
from contextlib import redirect_stdout
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
LIVE = "/srv/collective/data/store/read.db"


def load():
    spec = importlib.util.spec_from_file_location("sqlcheck_under_test", ROOT / "game" / "fleet" / "sqlcheck.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = '''
import sqlite3
BAD = "SELECT id, system, poi FROM stations WHERE system IS NOT NULL"
GONE = """SELECT item, MAX(best_buy)
          FROM nowhere GROUP BY item"""
GOOD = "SELECT name, system FROM stations WHERE system = ? AND name = ?"
NAMED = "SELECT name FROM stations WHERE system = :system"
FORMATTED = "SELECT %s FROM stations" % "id"
FSTRING = f"SELECT {'id'} FROM stations"
JOINED = "SELECT id FROM stations WHERE name IN (" + "?" + ")"
TEXT = "Select the eligible pilots from read.db, the best first."
'''


class SqlCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-sqlcheck-test-")
        self.root = Path(self.temp.name)
        self.db = self.root / "read.db"
        con = sqlite3.connect(self.db)
        con.execute("CREATE TABLE stations (name TEXT, kind TEXT, system TEXT, tag TEXT)")
        con.commit()
        con.close()
        self.script = self.root / "runner.py"
        self.script.write_text(MODULE)
        self.sqlcheck = load()

    def tearDown(self):
        self.temp.cleanup()

    def test_a_missing_column_and_a_missing_table_are_named_and_the_rest_pass(self):
        con = self.sqlcheck.connect(str(self.db))
        found = self.sqlcheck.faults(con, self.script)
        self.assertEqual([(error.split(":")[0], sql.split()[1]) for _line, error, sql in found],
                         [("no such column", "id,"), ("no such table", "item,")])
        lines = [line for line, _error, _sql in found]
        self.assertEqual(lines, sorted(lines))

    def test_queries_built_at_run_time_and_prose_are_left_out(self):
        texts = [sql for _line, sql in self.sqlcheck.queries(self.script)]
        self.assertEqual(len(texts), 4)                       # BAD, GONE, GOOD, NAMED
        self.assertFalse(any("%s" in t or "{" in t or t.endswith("(") for t in texts))

    def test_the_command_exits_1_on_a_fault_and_0_when_clean_2_without_a_database(self):
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(self.sqlcheck.main(["--db", str(self.db), str(self.script)]), 1)
        self.assertIn("2 refused by the schema", out.getvalue())
        clean = self.root / "clean.py"
        clean.write_text('Q = "SELECT name FROM stations"\n')
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.sqlcheck.main(["--db", str(self.db), str(clean)]), 0)
            self.assertEqual(self.sqlcheck.main(["--db", str(self.root / "none.db"), str(clean)]), 2)

    @unittest.skipUnless(os.path.isfile(LIVE), "no store read copy on this host")
    def test_every_query_of_the_fleet_scripts_fits_the_store_s_schema(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = self.sqlcheck.main(["--db", LIVE])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
