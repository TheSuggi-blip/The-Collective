"""Every literal SQL query of the fleet's scripts, prepared against the store's own schema: a column or a table
the store does not have is named before a runner reads an empty world from it.

Two network runners (hunt_net, mine_net) read 0 herds and 0 belts for hours on 2026-11-24 because one query asked
the table stations for columns it does not have, inside a broad `except sqlite3.Error` (errors.log ENT-194, queue
ENT-307); their unit tests fed hand-made worlds and passed. This check reads each module's string constants (no
import, no run), takes those that start with SELECT or WITH and hold FROM, and asks SQLite to prepare each one
(`EXPLAIN`, parameters bound to NULL) on a read-only connection to the store's read copy. It reports only what the
schema answers: `no such column` and `no such table`. A query built at run time (an f-string, `%` formatting,
`.format`, a string joined to a variable) is not a constant whole and is skipped; a syntax error of a fragment is
not reported. The unit tests run it over game/fleet/ and station/ whenever the read copy exists (the suggestion of
Zero and Apophis, reports.log ENT-192 and ENT-193).

Usage:
  sqlcheck.py                       every .py of game/fleet/ and station/ against data/store/read.db
  sqlcheck.py <file.py>...          those files only
  sqlcheck.py --db <path> [files]   another database (a test's)
Prints one line per fault (file:line, the error, the query) and a count; exit 1 when a fault stands, 2 when the
database cannot be opened.
"""
import ast
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB = "/srv/collective/data/store/read.db"
FOLDERS = ("game/fleet", "station")
SCHEMA_FAULT = ("no such column", "no such table")
QUERY = re.compile(r"(?s)^(SELECT|WITH)\b")          # upper case: the fleet's queries; prose ("Select the ...") is not one
NAMED = re.compile(r"(?<![:\w]):([A-Za-z_]\w*)")


def queries(path):
    """[(line, sql)]: the string constants of a module that read as one whole SELECT or WITH query."""
    try:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return []
    found, fragments = [], set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):              # an f-string: built at run time
            fragments.update(id(part) for part in node.values)
        elif isinstance(node, ast.BinOp):                 # "..." + x, "..." % x: a piece of a query built at run time
            fragments.update((id(node.left), id(node.right)))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ("format", "join"):
            fragments.add(id(node.func.value))            # "...".format(x), "...".join(x)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in fragments:
            sql = node.value.strip()
            if QUERY.match(sql) and " from " in " ".join(sql.lower().split()) and not any(m in sql for m in ("{", "%s", "%(", "%d")):
                found.append((node.lineno, sql))
    return found


def faults(con, path):
    """[(line, error, sql)] of the queries the schema refuses."""
    out = []
    for line, sql in queries(path):
        names = NAMED.findall(sql)
        params = {n: None for n in names} if names else (None,) * sql.count("?")
        try:
            con.execute("EXPLAIN " + sql, params)
        except sqlite3.Error as exc:
            if any(str(exc).startswith(word) for word in SCHEMA_FAULT):
                out.append((line, str(exc), " ".join(sql.split())))
    return out


def files_of(args):
    if args:
        return [Path(a) for a in args]
    return sorted(p for folder in FOLDERS for p in (REPO / folder).glob("*.py"))


def connect(db):
    return sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=5.0)


def main(argv):
    db = DB
    if argv[:1] == ["--db"]:
        if len(argv) < 2:
            print(__doc__)
            return 2
        db, argv = argv[1], argv[2:]
    if not Path(db).is_file():
        print("sqlcheck: no database at %s" % db)
        return 2
    try:
        con = connect(db)
        con.execute("SELECT 1 FROM sqlite_master LIMIT 1")
    except sqlite3.Error as exc:
        print("sqlcheck: %s cannot be read: %s" % (db, exc))
        return 2
    count = bad = 0
    for path in files_of(argv):
        found = faults(con, path)
        count += len(queries(path))
        for line, error, sql in found:
            bad += 1
            try:
                name = path.resolve().relative_to(REPO)
            except ValueError:
                name = path
            print("%s:%d %s :: %s" % (name, line, error, sql[:200]))
    print("sqlcheck: %d queries prepared, %d refused by the schema of %s" % (count, bad, db))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
