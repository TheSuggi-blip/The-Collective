"""The ledger: everything the members write, in the store by itself (docs.py's kinds plan, report, log, member, metrics;
docs_export.py; docs_division.py; hive.py division; the MCP tool docs, view=division). The export copies its allowlist
and nothing else (a .env, memory/, scripts/, a link, a file that holds a key never leave), only what changed, and
removes what left; the store keeps the plans, the reports by heading, every log entry as one section (an archived
entry is the same section, no new version), the members' files with their division as owner and the roster once; a
kind's first loading is no change; a quiet pass writes no row; the briefing lists the other divisions' writing one line a
file; `hive.py division` answers from the store with an empty ships table, under 4,000 characters. No engine, no network.
"""

import contextlib
import importlib.util
import io
import json
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

REPO = Path(__file__).resolve().parents[2]
FLEET = REPO / "game" / "fleet"
HIVE = FLEET / "hive.py"
T0 = 4070908800                                    # 2099-01-01 00:00 UTC


def load(name):
    path = FLEET / (name + ".py")
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(name + "_ledger_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text, mtime=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii")
    if mtime is not None:
        os.utime(path, (mtime, mtime))


def bump(path, text):
    """A new text and an mtime the last pass did not see."""
    old = Path(path).stat().st_mtime if Path(path).exists() else T0
    Path(path).write_text(text, encoding="ascii")
    os.utime(path, (old + 7, old + 7))


def entry(num, when, who, category, body, extra=""):
    return "## [ENT-%03d] | %s UTC | %s | %s%s\n%s\n" % (num, when, who, category, extra, body)


HEAD = "<!-- requests.log -- What one member asks of another.\n    See communications/protocol.md.\n-->\n\n"
ARCHIVE_HEAD = "<!-- requests.log archive -- ENT-001 to ENT-001\n     Moved from active log on 2099-01-01 09:00 UTC\n-->\n\n"
REQ1 = entry(1, "2099-01-01 08:00", "Apophis", "request", "To: Zero.\nNeed: a guard at the belt.\nBy: next turn.\nWhy: two kills.", " | ref: game/routes/x.json")
REQ2 = entry(2, "2099-01-01 09:00", "Zero", "request", "To: Mercury.\nNeed: a buyer for iron.\nBy: tonight.\nWhy: 40,000 held.", " | ref: game/routes/y.json")
REQ3 = entry(3, "2099-01-01 09:30", "Mercury", "answer", "Answer: yes. Two traders by tonight.", " | see: ENT-002")
REQ4 = entry(4, "2099-01-01 10:00", "Oracle", "request", "To: Apollo.\nNeed: a haul.\nBy: now.\nWhy: none.", " | ref: game/routes/z.json")
REQ5 = entry(5, "2099-01-01 10:30", "Apollo", "answer", "Answer: done. Hauled.", " | see: ENT-004")
ADMIRALS = (entry(1, "2099-01-01 07:00", "Zero", "claim", "Claims: mine-alpha-belt for 4 ships.\nWhy: its bid regains 300 an hour.") + "\n"
            + entry(2, "2099-01-01 07:30", "Apophis", "note", "The belt is quiet."))
REPORTS_LOG = (entry(1, "2099-01-01 06:00", "Zero", "session", "Session: the first.\nDid: mined.\nWorked: none.\nFailed: none.\nRequests: none.\n"
                     "Suggestions: none.\nReport: first.", " | ref: reports/2099-01-01_zero_first.md") + "\n"
               + entry(2, "2099-01-01 12:00", "Zero", "session", "Session: iron for the reserve.\nDid: 12,000 iron stored.\nWorked: Prism Scatter.\n"
                       "Failed: the gold test (errors.log ENT-009).\nRequests: requests.log ENT-002.\nSuggestions: none.\nReport: iron.",
                       " | ref: reports/2099-01-01_zero_iron.md"))
ORDERS = """## [ENT-001] | 2099-01-01 05:00 UTC | Unity | order
Changed: the first.
In force from this entry until a newer one.
EVERY ADMIRAL
Order: report.
ZERO, Mining (the miner- ships)
Order: sell ice only as far as each bid regains; gather what the reserve is short of.
Measure: units stored for the reserve per hour.
"""
GUIDE = "# mining.md -- Guidebook of the Mining Division\n\n## Class Card\n\n### Ships\n\nA hull with room.\n\n## 4. Levelling Guide\n\nMine.\n"
TEMPLATES = {"division": "mining", "owner": "Zero", "templates": {"ice-sell": {"title": "Ice sold", "routes": ["sell-ice-a", "sell-ice-b"]}}}
PLAN = """# plan-mining.md -- The Plan of the Mining Division

Kept by Zero; role miner.

## First, for Every Ship

1. voidborn-first

## Ships

| Ship | Hull | Piloting | Mining | Navigation | Trading | Gunnery | Exploration | Own routes, in this order |
|---|---|---|---|---|---|---|---|---|
| miner-1 | Threshold | 9 | 11 | 5 | 4 | 1 | 2 | mine-alpha-belt > @ice-sell |
| miner-2 | Threshold | 9 | 9 | 6 | 3 | 1 | 3 | mine-alpha-belt > craft-steel |
| miner-3 | Threshold | 9 | 9 | 6 | 3 | 1 | 3 | @ice-sell |

## Then, for Every Ship

1. census-frontier
2. park

## Planned

- steel plate from our iron | turn of 03:00 UTC

## Notes

The iron fields hold.
"""
REPORT = "# Mining -- Iron for the Reserve\n\n## Situation\n\nSECRET-SENTINEL-BODY iron held.\n\n## Plans\n\nSteel.\n"
COLLECTIVE = "---\nname: collective\n---\n\n# COLLECTIVE.md -- Members\n\n## How We Work\n\nShared text.\n\n%s\n\n## %s Mission\n\nI am the Admiral of %s.\n"
MARK = "<!-- MISSION: down to this line the file is the same in every member's workspace -->"
MISSION = "# MISSION.md -- Zero, Mining\n\nI am the Admiral of Mining.\n\n- **Every turn.** Read the fields, set the plan.\n- **Never.** More miners on a bid than it regains.\n"


class Fixture(unittest.TestCase):
    """A disposable repository and data folder with every kind of the ledger."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-ledger-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.data, self.repo = base / "data", base / "repo"
        self.root = self.repo / "game"
        self.data.mkdir()
        comm = self.repo / "communications"
        write(self.repo / "governance" / "rulebook.md", "# Rulebook\n\n## 12. Standing Rules\n\n| Rule | Says |\n|---|---|\n| F1 Chain | Each commands its own |\n", T0)
        write(comm / "orders.log", ORDERS, T0)
        write(comm / "archive" / "requests-2099-01-01.log", ARCHIVE_HEAD + REQ1, T0)
        write(comm / "requests.log", HEAD + REQ2 + "\n" + REQ3, T0)
        write(comm / "admirals.log", ADMIRALS, T0)
        write(comm / "reports.log", REPORTS_LOG, T0)
        write(comm / "queue.log", entry(1, "2099-01-01 04:00", "Morpheus", "general", "Repository live."), T0)
        write(self.repo / "reports" / "2099-01-01_zero_iron.md", REPORT, T0)
        write(self.root / "routes" / "guidebook" / "mining.md", GUIDE, T0)
        write(self.root / "routes" / "templates" / "mining.json", json.dumps(TEMPLATES), T0)
        write(self.root / "metrics.md", "# Metrics\n\n## kpi\n\nThroughput.\n", T0)
        write(self.data / "plans" / "plan-mining.md", PLAN, T0)
        write(self.data / "plans" / "history" / "plan-mining.20990101T000000Z.abc.md", PLAN, T0)
        members = self.data / "docs" / "members"
        write(members / "zero" / "MISSION.md", MISSION, T0)
        write(members / "zero" / "SOUL.md", "# Zero\n\nA miner's soul.\n", T0)
        write(members / "zero" / "knowledge" / "iron.md", "# Iron\n\n## Fields\n\nPrism.\n", T0)
        write(members / "fleet" / "ROSTER.md", "# ROSTER.md\n\n## Members\n\nSix.\n", T0)
        write(members / "unity" / "COLLECTIVE.md", COLLECTIVE % (MARK, "Unity", "Command"), T0)
        write(members / "mercury" / "COLLECTIVE.md", COLLECTIVE % (MARK, "Mercury", "Trade"), T0)
        write(members / ".stray.md", "not a member's", T0)

    def docs(self):
        found = load("docs")
        if found is None:
            self.fail("game/fleet/docs.py is missing")
        return found

    def one(self, now):
        store = load("store")
        return store.one_pass(str(self.data), now=now, root=str(self.root))

    def read(self, sql, args=()):
        conn = sqlite3.connect("file:%s?mode=ro" % (self.data / "store" / "live.db"), uri=True)
        try:
            return conn.execute(sql, args).fetchall()
        finally:
            conn.close()


class StoreTests(Fixture):
    def test_every_kind_of_the_ledger_is_kept_by_section_with_its_owner(self):
        out = self.one(T0)
        self.assertIsNone(out["versions"]["error"])
        kinds = dict(self.read("SELECT kind, COUNT(DISTINCT path) FROM docs GROUP BY kind"))
        for kind in ("plan", "report", "log", "member", "metrics"):
            self.assertIn(kind, kinds, "the store holds no %s: the members' writing is not in the database" % kind)
        self.assertEqual(self.read("SELECT section, owner FROM docs WHERE path = 'data/plans/plan-mining.md' ORDER BY n"),
                         [("top", "Mining"), ("first-for-every-ship", "Mining"), ("ships", "Mining"), ("then-for-every-ship", "Mining"),
                          ("planned", "Mining"), ("notes", "Mining")])
        self.assertEqual(self.read("SELECT COUNT(*) FROM docs WHERE path LIKE '%history%'"), [(0,)])        # the applied versions stay out
        self.assertEqual(self.read("SELECT section, owner FROM docs WHERE kind = 'report' ORDER BY n"), [("top", "Mining"), ("situation", "Mining"), ("plans", "Mining")])
        rows = self.read("SELECT section, n, owner, title, text FROM docs WHERE path = 'communications/requests.log' ORDER BY n")
        self.assertEqual([(r[0], r[1], r[2]) for r in rows], [("ENT-001", 1, "Military"), ("ENT-002", 2, "Mining"), ("ENT-003", 3, "Trade")])
        self.assertTrue(rows[0][3].startswith("## [ENT-001] | 2099-01-01 08:00 UTC | Apophis | request"))  # the archive's entry, under its log's path
        self.assertEqual(rows[1][4], "To: Mercury.\nNeed: a buyer for iron.\nBy: tonight.\nWhy: 40,000 held.")
        self.assertEqual(self.read("SELECT owner FROM docs WHERE path = 'communications/queue.log'"), [("Morpheus",)])   # no member: as written
        self.assertEqual(self.read("SELECT COUNT(*) FROM docs WHERE kind = 'log' AND text LIKE '%<!--%'"), [(0,)])
        members = self.read("SELECT path, section, owner FROM docs WHERE kind = 'member' ORDER BY path, n")
        self.assertIn(("data/docs/members/fleet/ROSTER.md", "members", "Fleet"), members)
        self.assertIn(("data/docs/members/zero/knowledge/iron.md", "fields", "Mining"), members)
        self.assertEqual([r[1] for r in members if r[0] == "data/docs/members/mercury/COLLECTIVE.md"], ["mission"])     # the shared part once
        self.assertEqual([r[1] for r in members if r[0] == "data/docs/members/unity/COLLECTIVE.md"], ["top", "how-we-work", "mission"])
        self.assertEqual(self.read("SELECT owner FROM docs WHERE path = 'data/docs/members/mercury/COLLECTIVE.md'"), [("Trade",)])
        self.assertFalse([r for r in members if ".stray" in r[0]])
        self.assertEqual(self.read("SELECT owner FROM docs WHERE kind = 'metrics' LIMIT 1"), [("Fleet",)])

    def test_an_archived_entry_stays_one_section_and_adds_no_version(self):
        self.one(T0)
        comm = self.repo / "communications"
        bump(comm / "archive" / "requests-2099-01-01.log", ARCHIVE_HEAD + REQ1 + "\n\n<!-- Appended 2099-01-02 03:00 UTC -- ENT-002 to ENT-002 -->\n\n" + REQ2)
        bump(comm / "requests.log", HEAD + REQ3)
        out = self.one(T0 + 60)
        self.assertEqual((out["versions"]["error"], out["versions"]["added"], out["versions"]["left"]), (None, 0, 0))
        self.assertEqual(self.read("SELECT section, src FROM docs WHERE path = 'communications/requests.log' ORDER BY n"),
                         [("ENT-001", "communications/archive/requests-2099-01-01.log"), ("ENT-002", "communications/archive/requests-2099-01-01.log"),
                          ("ENT-003", "communications/requests.log")])
        conn = load("store").connect(str(self.data))
        try:
            rows, _baseline = self.docs().changed(conn, T0 - 1)
        finally:
            conn.close()
        self.assertEqual(rows, [])

    def test_a_kind_first_loaded_is_no_change_and_a_new_entry_is_one_new_section(self):
        for path in [self.repo / "communications" / name for name in ("requests.log", "admirals.log", "reports.log", "queue.log")] + \
                    [self.repo / "communications" / "archive" / "requests-2099-01-01.log", self.repo / "reports" / "2099-01-01_zero_iron.md"]:
            path.rename(path.with_name(path.name + ".later"))
        shutil.move(str(self.data / "plans"), str(self.data / "plans.later"))
        self.one(T0)                                                         # a store that ran before the ledger
        for path in list(self.repo.rglob("*.later")) + [self.data / "plans.later"]:
            path.rename(path.with_name(path.name[:-len(".later")]))
        out = self.one(T0 + 3600)                                            # the kinds come in: loaded, counted as no change
        self.assertGreater(out["versions"]["added"], 10)
        docs = self.docs()
        conn = load("store").connect(str(self.data))
        try:
            rows, _baseline = docs.changed(conn, T0 + 1)
            self.assertEqual([r for r in rows if r[6] in docs.LEDGER], [], "a kind's first loading reads as new sections")
        finally:
            conn.close()
        bump(self.repo / "communications" / "requests.log", HEAD + REQ2 + "\n" + REQ3 + "\n" + REQ4)
        out = self.one(T0 + 3660)
        self.assertEqual((out["snapshot"]["loaded"]["docs"], out["versions"]["added"]), (1, 1))      # append-only: one new section
        conn = load("store").connect(str(self.data))
        try:
            rows, _baseline = docs.changed(conn, T0 + 3601)
        finally:
            conn.close()
        self.assertEqual([(r[0], r[1], r[2], r[7]) for r in rows], [("new", "communications/requests.log", "ENT-004", "Intel")])

    def test_a_quiet_pass_writes_no_row_and_a_version_that_leaves_keeps_its_last_pass(self):
        docs = self.docs()
        self.one(T0)
        self.one(T0 + 60)
        self.one(T0 + 120)
        self.assertEqual(self.read("SELECT COUNT(*) FROM doc_versions WHERE last_seen > ?", (T0,)), [(0,)])     # two quiet passes: no row moved
        bump(self.data / "plans" / "plan-mining.md", PLAN.replace("The iron fields hold.", "The iron fields are done."))
        self.one(T0 + 180)
        self.assertEqual(self.read("SELECT first_seen, last_seen FROM doc_versions WHERE path = 'data/plans/plan-mining.md' AND section = 'notes' ORDER BY version"),
                         [(T0, T0 + 120), (T0 + 180, T0 + 180)])                # the old text stood until the pass before
        self.assertEqual(self.read("SELECT MIN(last_seen) FROM doc_versions WHERE path = 'governance/rulebook.md'"), [(T0 + 180,)])  # a change moves the standing on
        self.one(T0 + 180 + docs.KEEP_EVERY)                                 # quiet, but KEEP_EVERY after the last move
        self.assertEqual(self.read("SELECT MIN(last_seen) FROM doc_versions WHERE path = 'governance/rulebook.md'"), [(T0 + 180 + docs.KEEP_EVERY,)])
        (self.data / "docs" / "members" / "zero" / "knowledge" / "iron.md").unlink()
        self.one(T0 + 240 + docs.KEEP_EVERY)
        self.assertEqual(self.read("SELECT last_seen FROM doc_versions WHERE path = 'data/docs/members/zero/knowledge/iron.md' AND section = 'fields'"),
                         [(T0 + 180 + docs.KEEP_EVERY,)])
        self.one(T0 + 300 + docs.KEEP_EVERY)                                 # a section long gone is never moved again
        self.assertEqual(self.read("SELECT last_seen FROM doc_versions WHERE path = 'data/docs/members/zero/knowledge/iron.md' AND section = 'fields'"),
                         [(T0 + 180 + docs.KEEP_EVERY,)])

    def test_the_briefing_lists_the_other_divisions_writing_one_line_a_file(self):
        docs = self.docs()
        self.one(T0)
        comm = self.repo / "communications"
        bump(comm / "admirals.log", ADMIRALS + "\n" + entry(3, "2099-01-02 08:00", "Apophis", "claim", "Claims: guard-alpha-belt for 2 ships.\nWhy: the miners."))
        bump(comm / "requests.log", HEAD + REQ2 + "\n" + REQ3 + "\n" + REQ4 + "\n" + REQ5)
        write(self.repo / "reports" / "2099-01-02_apophis_guard.md", "# Military -- The Guard\n\n## Situation\n\nSECRET-SENTINEL-BODY guarded.\n", T0 + 50)
        write(self.data / "plans" / "plan-military.md", PLAN.replace("Mining", "Military").replace("mining", "military"), T0 + 50)
        bump(self.data / "plans" / "plan-mining.md", PLAN.replace("The iron fields hold.", "Zero's own change."))
        write(self.data / "docs" / "members" / "zero" / "knowledge" / "gold.md", "# Gold\n\nNone yet.\n", T0 + 50)
        self.one(T0 + 30 * 3600)                                             # after Zero's last turn (2099-01-01 12:00)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            docs.briefing(str(self.root), str(self.data), T0 + 31 * 3600, "Zero")
        text = out.getvalue()
        self.assertIn("claim ENT-003 01-02 08:00 UTC by Apophis (Military)", text)
        self.assertIn("guard-alpha-belt for 2 ships", text)
        self.assertRegex(text, r"reports/2099-01-02_apophis_guard.md\s+Military\s+new, 2 sections: Military -- The Guard")
        self.assertRegex(text, r"data/plans/plan-military.md\s+Military\s+new, 6 sections")
        self.assertRegex(text, r"communications/requests.log\s+2 new entries \(ENT-004 to ENT-005\), by Apollo 1, Oracle 1")
        self.assertNotIn("SECRET-SENTINEL-BODY", text)                        # titles and sizes, never whole texts
        self.assertNotIn("plan-mining.md", text)                              # the member's own writing: not listed
        self.assertNotIn("gold.md", text)
        self.assertLessEqual(len(text.splitlines()), 1 + docs.BRIEF_ROWS)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            docs.briefing(str(self.root), str(self.data), T0 + 31 * 3600, "Apophis")
        self.assertIn("data/plans/plan-mining.md", out.getvalue())             # Zero's plan for another member
        self.assertIn("gold.md", out.getvalue())


class DivisionTests(Fixture):
    def setUp(self):
        super().setUp()
        self.one(T0)

    def test_what_a_division_does_from_the_store_alone_with_no_ship_signed_on(self):
        reader = load("docs_division")
        self.assertIsNotNone(reader, "game/fleet/docs_division.py is missing: no answer to what each Admiral is doing")
        self.assertEqual(self.read("SELECT COUNT(*) FROM ships"), [(0,)])     # the pause: no ship in the store
        shutil.rmtree(str(self.data / "plans"))                              # the store alone: no file is read
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(reader.show(str(self.root), str(self.data), T0 + 13 * 3600, "Zero"), 0)
        text = out.getvalue()
        block = text.split("\n", 1)[1]
        self.assertLess(len(block), reader.LIMIT)
        self.assertIn("DIVISION Mining (Zero)", block)
        self.assertIn("I am the Admiral of Mining.", block)                   # MISSION.md whole
        self.assertIn("- **Never.** More miners on a bid than it regains.", block)
        self.assertIn("Measure: units stored for the reserve per hour.", block)
        self.assertIn("3 ships in its table, 1 routes First, 2 Then, 4 own routes with the templates expanded", block)
        self.assertIn("First: voidborn-first", block)
        self.assertIn("Routes in the ships' cells, ships naming each: mine-alpha-belt 2, craft-steel 1", block)
        self.assertIn("Templates, ships naming each (its routes): @ice-sell 2 (2)", block)
        self.assertNotIn("miner-1", block)                                    # no ship named
        self.assertRegex(block, r"GUIDEBOOK \(game/routes/guidebook/mining.md, 4 sections")
        self.assertIn("class-card", block)
        self.assertIn("LAST REPORT (reports.log ENT-002 of 2099-01-01 12:00 UTC", block)
        self.assertIn("Did: 12,000 iron stored.", block)
        self.assertIn("REQUESTS not closed: 1 to Zero, 1 from it", block)
        self.assertIn("ENT-001 OPEN 01-01 08:00 from Apophis: a guard at the belt.", block)
        self.assertIn("ENT-002 ACCEPTED 01-01 09:00 to Mercury: a buyer for iron.", block)
        self.assertIn("CLAIMS in force (admirals.log, 24 hours from the entry, not released): 1", block)
        self.assertIn("mine-alpha-belt for 4 ships", block)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.show(str(self.root), str(self.data), T0 + 40 * 3600, "mining")   # a division's name; the claim is older than 24 hours
        self.assertIn("CLAIMS in force (admirals.log, 24 hours from the entry, not released): 0", out.getvalue())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.show(str(self.root), str(self.data), T0 + 13 * 3600, "Mercury")
        self.assertIn("I am the Admiral of Trade.", out.getvalue())          # no MISSION.md yet: the old COLLECTIVE.md's mission
        self.assertIn("PLAN | not in the store", out.getvalue())

    def test_hive_division_all_and_the_tool_docs(self):
        run = lambda *words: subprocess.run([sys.executable, "-I", "-B", str(HIVE)] + list(words) + ["--data", str(self.data), "--root", str(self.root)],
                                            capture_output=True, text=True, timeout=120)
        done = run("division", "all")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        for name in ("Command (Unity)", "Mining (Zero)", "Logistics (Apollo)", "Trade (Mercury)", "Military (Apophis)", "Intel (Oracle)"):
            self.assertIn("DIVISION " + name, done.stdout)
        self.assertLess(len(done.stdout), 6 * 4000 + 400)
        done = run("division", "nobody")
        self.assertEqual(done.returncode, 1)
        self.assertIn("no member or division `nobody`", done.stdout)
        spec = importlib.util.spec_from_file_location("collective_mcp_ledger_under_test", FLEET / "collective_mcp.py")
        server = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server)
        plan = server.TOOLS["docs"]["plan"]
        self.assertEqual(plan({"view": "division", "division": "Zero"}), [("game/fleet/hive.py", ["division", "Zero"])])
        self.assertEqual(plan({"view": "division"}), [("game/fleet/hive.py", ["division", "all"])])
        self.assertIn("division", server.TOOLS["docs"]["args"]["view"]["enum"])


class ExportTests(unittest.TestCase):
    """docs_export.py on disposable profiles: the allowlist only, what changed only, what left removed."""

    def setUp(self):
        self.export = load("docs_export")
        self.assertIsNotNone(self.export, "game/fleet/docs_export.py is missing: the members' own files never reach the store")
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-export-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.profiles, self.data = base / "profiles", base / "data"
        self.secret = "TOKEN=" + "never-copied-" + "x" * 12
        for member in ("unity", "zero", "oracle", "mercury", "apollo", "apophis"):
            home = self.profiles / member
            work = home / ("workspace-" + member)
            write(home / "SOUL.md", "# %s\n" % member, T0)
            write(home / ".env", self.secret, T0)
            write(home / "config.yaml", "model: x\n", T0)
            write(work / ".env", self.secret, T0)
            write(work / "MISSION.md", "# %s mission\n" % member, T0)
            write(work / "LEARNINGS.md", "# learnings\n", T0)
            write(work / "AGENTS.md", "# agents\n", T0)
            write(work / "FLEET.md", "# fleet\n", T0)
            write(work / "ROSTER.md", "# roster\n", T0)
            write(work / "memory" / "2099.md", "# memory\n", T0)
            write(work / "scripts" / "x.md", "# script\n", T0)
            write(work / "knowledge" / "iron.md", "# iron\n", T0)
            write(work / "knowledge" / ".hidden.md", "# hidden\n", T0)
            write(work / "knowledge" / "notes.txt", "notes\n", T0)
            write(work / "knowledge" / "deep" / "x.md", "# deep\n", T0)
        write(self.profiles / "unity" / "workspace-unity" / "DESIGN.md", "# design\n", T0)
        write(self.profiles / "zero" / "workspace-zero" / "DESIGN.md", "# not unity's\n", T0)
        write(self.profiles / "zero" / "workspace-zero" / "COLLECTIVE.md", "# old\n", T0)
        os.unlink(self.profiles / "oracle" / "SOUL.md")
        os.symlink(self.profiles / "oracle" / ".env", self.profiles / "oracle" / "SOUL.md")      # a link is never followed
        self.target = self.data / "docs" / "members"

    def copies(self):
        return sorted(p.relative_to(self.target).as_posix() for p in self.target.rglob("*") if p.is_file())

    def test_only_the_allowlist_is_copied_and_never_a_dotenv(self):
        lines, counts = self.export.run(str(self.profiles), str(self.data))
        found = self.copies()
        expected = {"fleet/ROSTER.md", "unity/DESIGN.md", "zero/COLLECTIVE.md"}
        for member in ("unity", "zero", "oracle", "mercury", "apollo", "apophis"):
            expected |= {"%s/%s" % (member, name) for name in ("SOUL.md", "MISSION.md", "LEARNINGS.md", "knowledge/iron.md")}
        expected.discard("oracle/SOUL.md")
        self.assertEqual(found, sorted(expected))
        for path in self.target.rglob("*"):
            if path.is_file():
                self.assertNotIn(self.secret, path.read_text(encoding="ascii"), path)
        self.assertEqual(counts["copied"], len(expected))
        self.assertEqual(os.stat(self.target / "zero" / "SOUL.md").st_mtime, T0)     # the copy keeps its source's time

    def test_copied_only_when_changed_and_what_left_is_removed(self):
        self.export.run(str(self.profiles), str(self.data))
        _lines, counts = self.export.run(str(self.profiles), str(self.data))
        self.assertEqual((counts["copied"], counts["touched"], counts["removed"]), (0, 0, 0))
        mission = self.profiles / "zero" / "workspace-zero" / "MISSION.md"
        os.utime(mission, (T0 + 60, T0 + 60))                                 # the time only: no copy, the time set
        _lines, counts = self.export.run(str(self.profiles), str(self.data))
        self.assertEqual((counts["copied"], counts["touched"]), (0, 1))
        write(mission, "# zero mission, changed\n", T0 + 120)
        (self.profiles / "zero" / "workspace-zero" / "knowledge" / "iron.md").unlink()
        write(self.target / "zero" / "planted.md", "# not from the allowlist\n")
        lines, counts = self.export.run(str(self.profiles), str(self.data))
        self.assertEqual((counts["copied"], counts["removed"]), (1, 2), lines)
        self.assertEqual((self.target / "zero" / "MISSION.md").read_text(), "# zero mission, changed\n")
        self.assertFalse((self.target / "zero" / "knowledge").exists())       # an empty folder goes too
        shutil.move(str(self.profiles / "apollo"), str(self.profiles / "apollo.away"))   # a profile not mounted: its copies stay
        lines, counts = self.export.run(str(self.profiles), str(self.data))
        self.assertEqual((counts["removed"], counts["missing"]), (0, 1))
        self.assertTrue((self.target / "apollo" / "SOUL.md").is_file())
        self.assertTrue(any("apollo" in line and "copies" in line for line in lines))

    def test_a_file_that_holds_a_key_is_held_back_and_a_dry_run_writes_nothing(self):
        lines, counts = self.export.run(str(self.profiles), str(self.data), dry_run=True)
        self.assertFalse(self.target.exists())
        self.assertGreater(counts["copied"], 20)
        self.assertTrue(lines[0].startswith("  would copy "))
        self.export.run(str(self.profiles), str(self.data))
        key = "gh" + "p_" + "A1b2" * 9                                        # built here: no key-like text in the repository
        write(self.profiles / "zero" / "workspace-zero" / "knowledge" / "iron.md", "# iron\n\nthe key %s\n" % key, T0 + 60)
        lines, counts = self.export.run(str(self.profiles), str(self.data))
        self.assertEqual(counts["held"], 1)
        self.assertFalse((self.target / "zero" / "knowledge" / "iron.md").exists())
        self.assertIn("  held back zero/knowledge/iron.md: it holds what looks like a credential", lines)


class TimingTests(unittest.TestCase):
    """The repository's real logs and reports (the members' writing that lives there) in a pass, then a quiet pass, then
    a pass after one new entry in requests.log: each timed and printed."""

    def test_a_pass_on_the_real_logs_and_one_new_entry(self):
        store, docs = load("store"), load("docs")
        with tempfile.TemporaryDirectory(prefix="fleet-ledger-timing-") as temp:
            repo, data = Path(temp) / "repo", Path(temp) / "data"
            data.mkdir()
            for rel, path, _kind, _owner in docs.sources(REPO):
                (repo / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, repo / rel)
            spent = []
            for n in range(3):
                if n == 2:
                    with open(repo / "communications" / "requests.log", "a", encoding="ascii") as handle:
                        handle.write("\n" + entry(9999, "2099-01-01 00:00", "Zero", "request", "To: Mercury.\nNeed: a timing.\nBy: now.\nWhy: the test."))
                begun = time.time()
                out = store.one_pass(str(data), now=begun + 60 * n, root=str(repo / "game"))
                spent.append((time.time() - begun, out))
            conn = sqlite3.connect(str(data / "store" / "live.db"))
            try:
                logs = conn.execute("SELECT COUNT(*) FROM docs WHERE kind = 'log'").fetchone()[0]
                reports = conn.execute("SELECT COUNT(*) FROM docs WHERE kind = 'report'").fetchone()[0]
            finally:
                conn.close()
        print("\n  timing: %d log entries, %d report sections; the first pass %.2f s, a quiet pass %.2f s, a pass after one new entry %.2f s (%d file read, %d version added)"
              % (logs, reports, spent[0][0], spent[1][0], spent[2][0], spent[2][1]["snapshot"]["loaded"].get("docs", 0), spent[2][1]["versions"]["added"]))
        self.assertGreater(logs, 100)
        self.assertEqual((spent[1][1]["snapshot"]["loaded"].get("docs", 0), spent[1][1]["versions"]["added"]), (0, 0))
        self.assertEqual((spent[2][1]["snapshot"]["loaded"]["docs"], spent[2][1]["versions"]["added"]), (1, 1))
        self.assertLess(spent[1][0], 30)
        self.assertLess(spent[2][0], 30)


if __name__ == "__main__":
    unittest.main()
