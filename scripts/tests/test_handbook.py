"""scripts/handbook.py and game/fleet/docs_handbook.py: the store's handbook is written from the code alone (the same
bytes twice, every table and view of the schema its own section, every file under the cap, a table without a
description refused by name), the committed files are current, the gate fails a stale, missing or left-over file,
the store mirrors it as kind handbook, and hive.py handbook, the MCP tool docs (view=handbook) and the briefing lead
to it. No engine, no network, no live data."""

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "handbook.py"
FLEET = ROOT / "game" / "fleet"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


handbook = load("handbook_under_test", SCRIPT)


def run(*args, root=ROOT):
    return subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--root", str(root)] + list(args), capture_output=True, text=True, timeout=120)


class Generator(unittest.TestCase):
    def setUp(self):
        self.mods = handbook.modules(ROOT)

    def test_the_generator_is_deterministic_and_reads_no_data_and_no_time(self):
        first = handbook.build(ROOT, "20990101T000001Z", self.mods)
        time.sleep(1.1)
        self.assertEqual(handbook.build(ROOT, "20990101T000001Z", self.mods), first)
        self.assertNotIn(time.strftime("%Y-%m-%d %H:%M", time.gmtime()), "\n".join(first.values()))      # no clock in it
        conn = handbook.fresh_schema(self.mods["store"])                     # the columns come from memory, never from a database file
        self.addCleanup(conn.close)
        self.assertEqual([row[2] for row in conn.execute("PRAGMA database_list")], [""])

    def test_every_table_and_view_of_a_fresh_schema_has_one_section_with_its_columns(self):
        files = handbook.build(ROOT, "20990101T000001Z", self.mods)
        conn = handbook.fresh_schema(self.mods["store"])
        self.addCleanup(conn.close)
        made = [name for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%'")]
        self.assertGreater(len(made), 50)
        docs = self.mods["docs"]
        for name in made:
            holding = [path for path, text in files.items() if "\n## %s\n" % name in text]
            self.assertEqual(len(holding), 1, "%s stands in %s" % (name, holding))
            sections = {sid: body for sid, _title, body in docs.parse_markdown(files[holding[0]])}
            self.assertIn(docs.slug(name), sections, name)
            body = sections[docs.slug(name)]
            for column, _type in self.mods["store"].schema(conn)[name]["columns"]:
                self.assertIn(column, body.split("- Columns: ")[1].split("\n")[0], "%s.%s" % (name, column))
            for _question, sql in self.mods["store"].EXAMPLES.get(name, ())[:1]:
                self.assertIn(sql, body, name)
        self.assertEqual(handbook.unfiled(files), [])                       # today every table and every call has its subject

    def test_keep_and_refresh_say_what_the_code_says(self):
        found = dict(handbook.describe(self.mods))
        store, stats = self.mods["store"], self.mods["stats"]
        self.assertIn("%g days" % max(store.KEEP_DAYS, store.KEEP_TABLES["observations"]), found["observations"]["keep"])
        self.assertIn("%g days" % store.KEEP_DAYS, found["runs"]["keep"])
        self.assertIn("for good", found["route_hour"]["keep"])
        self.assertIn("summed again", found["route_hour"]["refresh"])
        self.assertIn("%g days (stats.py KEEP)" % stats.KEEP["stats_time"], found["stats_time"]["keep"])
        self.assertIn("part `time`", found["stats_time"]["refresh"])
        self.assertIn("part `figures`", found["stats_figures"]["refresh"])
        self.assertIn("loader `books`", found["books"]["refresh"])
        self.assertIn("data/market/*.json", found["books"]["refresh"])
        self.assertEqual(found["route_earnings"]["from"], ["route_hour", "routes"])
        self.assertEqual(found["ship_skills"]["key"], ["pilot", "skill"])
        self.assertNotIn("not stated in the code", "".join(e["refresh"] for e in found.values()))

    def test_where_to_ask_has_a_line_for_every_tool_and_files_every_call(self):
        rows = handbook.ask_rows(self.mods, ROOT)
        calls = [call.split(" ")[0] for lines in rows.values() for _text, call, _shell in lines]
        for name in self.mods["collective_mcp"].TOOLS:
            if name != "hive":
                self.assertIn(name, calls, name)
        shells = [shell for lines in rows.values() for _t, _c, shell in lines]
        self.assertIn("hive.py handbook", shells)                       # the MCP tool docs, view=handbook
        self.assertIn("hive.py sql <query>", shells)
        self.assertTrue(all(len(text) <= handbook.ASK_CHARS for lines in rows.values() for text, _c, _s in lines))

    def test_a_table_or_a_call_no_subject_names_stands_under_other_with_a_warning(self):
        self.addCleanup(setattr, handbook, "SUBJECTS", handbook.SUBJECTS)
        self.addCleanup(setattr, handbook, "VERBS", handbook.VERBS)
        handbook.SUBJECTS = tuple((title, tuple(t for t in tables if t != "lanes")) for title, tables in handbook.SUBJECTS)
        handbook.VERBS = {verb: subject for verb, subject in handbook.VERBS.items() if verb != "flow"}
        files = handbook.build(ROOT, "20990101T000001Z", self.mods)
        self.assertIn("\n## lanes\n", files["game/handbook/other.md"])
        self.assertIn("\n### Other\n", files[handbook.MASTER])
        warned = handbook.unfiled(files)
        self.assertEqual(len(warned), 2, warned)
        self.assertIn("`lanes`", warned[0])
        self.assertIn("hive verb=flow", warned[1])

    def test_a_table_without_a_description_fails_the_generator_with_its_name(self):
        store = self.mods["store"]
        kept = store.DESCRIPTIONS.pop("route_earnings")
        self.addCleanup(store.DESCRIPTIONS.__setitem__, "route_earnings", kept)
        with self.assertRaises(handbook.Refused) as caught:
            handbook.build(ROOT, "20990101T000001Z", self.mods)
        self.assertIn("route_earnings", str(caught.exception))

    def test_every_file_stays_under_the_cap_in_ascii_and_a_cap_too_small_fails(self):
        files = handbook.build(ROOT, "20990101T000001Z", self.mods)
        self.assertLessEqual(len(handbook.FLOW), handbook.FLOW_CAP)
        for path, text in files.items():
            self.assertLessEqual(len(text), handbook.CAP, path)
            self.assertTrue(text.isascii(), path)
        self.addCleanup(setattr, handbook, "CAP", handbook.CAP)
        handbook.CAP = 3000
        with self.assertRaises(handbook.Refused) as caught:
            handbook.build(ROOT, "20990101T000001Z", self.mods)
        self.assertIn("more than CAP 3000", str(caught.exception))

    def test_a_long_subject_drops_examples_before_it_fails(self):
        self.addCleanup(setattr, handbook, "CAP", handbook.CAP)
        known = dict(handbook.describe(self.mods))
        tables = dict(handbook.SUBJECTS)["The catalog"]
        full = handbook.part(self.mods, ROOT, "The catalog", tables, known)
        self.assertNotIn("more examples", full)
        handbook.CAP = len(full) - 1                                        # one character too many: two examples a table
        cut = handbook.part(self.mods, ROOT, "The catalog", tables, known)
        self.assertLess(len(cut), len(full))
        self.assertIn("- 1 more example: `hive.py schema items`", cut)
        handbook.CAP = 500                                                  # not even one example a table fits: refused, by name
        with self.assertRaises(handbook.Refused) as caught:
            handbook.part(self.mods, ROOT, "The catalog", tables, known)
        self.assertIn("game/handbook/the-catalog.md", str(caught.exception))


class Committed(unittest.TestCase):
    def test_the_committed_handbook_is_current(self):
        files = handbook.build(ROOT, handbook.current_id(ROOT) or "20990101T000001Z")
        self.assertEqual(handbook.stale(ROOT, files), ([], []), "run `python3 -I -B scripts/handbook.py` and commit game/handbook.md, game/handbook/")
        done = run("--check")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn("current", done.stdout)


class Gate(unittest.TestCase):
    """--check and the write on a copy of what the handbook is written from."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="handbook-test-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        shutil.copytree(FLEET, self.root / "game" / "fleet", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(ROOT / "game" / "metrics.md", self.root / "game" / "metrics.md")
        (self.root / "scripts").mkdir()

    def test_missing_written_current_stale_and_left_over(self):
        done = run("--check", root=self.root)
        self.assertEqual(done.returncode, 1)
        self.assertIn("stale:", done.stdout)
        self.assertIn("game/handbook.md", done.stdout)
        done = run(root=self.root)
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertTrue((self.root / "game" / "handbook.md").is_file())
        ident = handbook.current_id(self.root)
        self.assertRegex(ident or "", r"^\d{8}T\d{6}Z$")
        self.assertFalse(ident.endswith("00Z"))
        self.assertEqual(run("--check", root=self.root).returncode, 0)
        self.assertIn("current", run(root=self.root).stdout)              # nothing to write: the file is not touched
        stray = self.root / "game" / "handbook" / "gone-subject.md"
        stray.write_text("# a subject that is no more\n", encoding="ascii")
        done = run("--check", root=self.root)
        self.assertEqual(done.returncode, 1)
        self.assertIn("gone-subject.md", done.stdout)
        run(root=self.root)
        self.assertFalse(stray.exists())
        store = self.root / "game" / "fleet" / "store.py"                  # a description changes: the gate fails until written again
        store.write_text(store.read_text(encoding="ascii").replace("one row per ship of ours", "one row per ship of the fleet"), encoding="ascii")
        self.assertEqual(run("--check", root=self.root).returncode, 1)
        run(root=self.root)
        self.assertIn("one row per ship of the fleet", (self.root / "game" / "handbook" / "ships-and-pilots.md").read_text(encoding="ascii"))
        self.assertEqual(handbook.current_id(self.root), ident)            # the id is kept
        for cache in self.root.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)

    @unittest.skipUnless(shutil.which("git"), "git is missing")
    def test_commit_by_path_as_unity_and_a_members_work_in_progress_holds_it(self):
        shutil.copy(SCRIPT, self.root / "scripts" / "handbook.py")
        git = lambda *args: subprocess.run(["git", "-C", str(self.root)] + list(args), capture_output=True, text=True, timeout=60)
        git("init", "-q")
        git("add", "-A")
        git("-c", "user.name=Tester", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "the tree")
        (self.root / "governance").mkdir()
        (self.root / "governance" / "other.md").write_text("another member's staged work\n", encoding="ascii")
        git("add", "--", "governance/other.md")
        done = run("--commit", root=self.root)
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("committed", done.stdout)
        self.assertEqual(git("log", "-1", "--format=%an <%ae>").stdout.strip(), "Unity <unity@suggi-workspace.dev>")
        names = git("show", "--name-only", "--format=", "HEAD").stdout.split()
        self.assertTrue(names and all(n == "game/handbook.md" or n.startswith("game/handbook/") for n in names), names)
        self.assertEqual(git("diff", "--cached", "--name-only").stdout.split(), ["governance/other.md"])     # still staged, not committed
        self.assertEqual(git("status", "--porcelain", "--", "game/handbook.md", "game/handbook").stdout, "")
        store = self.root / "game" / "fleet" / "store.py"                  # a member's change in game/fleet/: nothing is built
        store.write_text(store.read_text(encoding="ascii").replace("one row per ship of ours", "one row per ship"), encoding="ascii")
        head = git("rev-parse", "HEAD").stdout
        done = run("--commit", root=self.root)
        self.assertEqual(done.returncode, 0)
        self.assertIn("not built", done.stdout)
        self.assertEqual(git("rev-parse", "HEAD").stdout, head)
        self.assertEqual(git("status", "--porcelain", "--", "game/handbook.md", "game/handbook").stdout, "")
        for cache in self.root.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)


class Reader(unittest.TestCase):
    """docs.py's kind handbook, docs_handbook.py on the store's copy and on the files, hive.py handbook, the tool docs."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="handbook-reader-test-")
        self.addCleanup(temp.cleanup)
        self.data = Path(temp.name)
        sys.path.insert(0, str(FLEET))
        self.addCleanup(sys.path.remove, str(FLEET))
        self.docs = load("docs", FLEET / "docs.py") if "docs" not in sys.modules else sys.modules["docs"]
        self.reader = load("docs_handbook_under_test", FLEET / "docs_handbook.py")

    def ask(self, topic):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.reader.show(str(ROOT / "game"), str(self.data), time.time(), topic)
        return code, out.getvalue()

    def test_docs_mirrors_every_handbook_file_as_kind_handbook_owner_fleet_one_section_a_heading(self):
        self.assertEqual(self.docs.kind_of("game/handbook.md"), ("handbook", "Fleet"))
        self.assertEqual(self.docs.kind_of("game/handbook/money.md"), ("handbook", "Fleet"))
        listed = [rel for rel, _path, kind, _owner in self.docs.sources(ROOT) if kind == "handbook"]
        on_disk = ["game/handbook.md"] + sorted("game/handbook/" + p.name for p in (ROOT / "game" / "handbook").glob("*.md"))
        self.assertEqual(sorted(listed), sorted(on_disk))
        rows = self.docs.read(ROOT / "game" / "handbook" / "routes-and-runs.md", {"root": str(ROOT / "game"), "data": str(self.data)})["docs"]
        self.assertEqual({(r["kind"], r["owner"], r["path"]) for r in rows}, {("handbook", "Fleet", "game/handbook/routes-and-runs.md")})
        text = (ROOT / "game" / "handbook" / "routes-and-runs.md").read_text(encoding="ascii")
        self.assertEqual(len(rows), 1 + text.count("\n## "))               # the head, then one section a heading

    def test_without_a_store_the_files_answer_and_say_so(self):
        code, out = self.ask("")
        self.assertEqual(code, 0)
        self.assertIn("read from the files", out)
        for part in ("=== game/handbook.md top", "=== game/handbook.md contents", "=== game/handbook.md how-the-data-flows", "## How the data flows"):
            self.assertIn(part, out)
        self.assertNotIn("## Where to ask what", out)
        code, out = self.ask("route_earnings")
        self.assertEqual(code, 0)
        self.assertIn("=== game/handbook/routes-and-runs.md route-earnings", out)
        self.assertIn("cph_4h", out)
        code, out = self.ask("money")
        self.assertIn("=== game/handbook.md where-to-ask-what/money", out)
        self.assertIn("=== game/handbook/money.md stats-money-hour", out)
        code, out = self.ask("zzqqx nothing")
        self.assertEqual(code, 1)
        self.assertIn("nothing matches", out)

    def test_from_the_stores_read_copy(self):
        store = sys.modules.get("store") or load("store", FLEET / "store.py")
        folder = self.data / "store"
        folder.mkdir()
        conn = sqlite3.connect(str(folder / "read.db"))
        conn.executescript(store.SCHEMA)
        store.setup_snapshot(conn)
        for rel, path, kind, _owner in self.docs.sources(ROOT):
            if kind == "handbook":
                rows = self.docs.read(path, {"root": str(ROOT / "game"), "data": str(self.data)})["docs"]
                conn.executemany("INSERT INTO docs (path, kind, owner, section, n, title, text, sha, chars, t, src) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                                 [(r["path"], r["kind"], r["owner"], r["section"], r["n"], r["title"], r["text"], r["sha"], r["chars"], r["t"], rel) for r in rows])
        conn.commit()
        conn.close()
        code, out = self.ask("stats_figures")
        self.assertEqual(code, 0)
        self.assertIn("the store's read copy", out)
        self.assertNotIn("read from the files", out)
        self.assertIn("=== game/handbook/statistics.md stats-figures", out)
        code, out = self.ask("where to ask what")
        self.assertIn("=== game/handbook.md where-to-ask-what", out)

    def test_hive_py_handbook_and_the_tool_docs_view_handbook(self):
        done = subprocess.run([sys.executable, "-I", "-B", str(FLEET / "hive.py"), "handbook", "ship_skills", "--data", str(self.data)],
                              capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("=== game/handbook/ships-and-pilots.md ship-skills", done.stdout)
        server = load("collective_mcp_handbook_test", FLEET / "collective_mcp.py")
        plan = server.TOOLS["docs"]["plan"]
        self.assertEqual(plan({"view": "handbook"}), [("game/fleet/hive.py", ["handbook"])])
        self.assertEqual(plan({"view": "handbook", "topic": "route_earnings"}), [("game/fleet/hive.py", ["handbook", "route_earnings"])])
        self.assertEqual(plan({"view": "section", "section": "F8"}), [("game/fleet/hive.py", ["docs", "--section", "F8"])])   # the others as before
        self.assertEqual(plan({}), [("game/fleet/hive.py", ["docs"])])
        self.assertIn("handbook", server.TOOLS["docs"]["args"]["view"]["enum"])
        self.assertIn("view=handbook", server.TOOLS["docs"]["text"])
        self.assertIn("topic", server.TOOLS["docs"]["args"])
        self.assertEqual(len(server.TOOLS), 22)                                                   # no new tool by the handbook (the 22nd: needs, r22)

    def test_the_briefing_points_to_the_handbook(self):
        hive = load("hive_handbook_test", FLEET / "hive.py")
        for folder in ("fleet/ships", "routes", "market"):
            (self.data / folder).mkdir(parents=True, exist_ok=True)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            hive.show_briefing(str(ROOT / "game"), str(self.data), time.time(), "Zero", 4)
        self.assertIn("=== THE HANDBOOK", out.getvalue())
        self.assertIn("hive.py handbook", out.getvalue().split("=== THE HANDBOOK")[1])


if __name__ == "__main__":
    unittest.main()
