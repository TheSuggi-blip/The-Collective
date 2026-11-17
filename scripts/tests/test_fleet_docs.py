"""game/fleet/docs.py and its place in store.py, hive.py and the MCP server: the fleet's written knowledge by section in the store, every version kept. A rulebook gives one section per rule row with stable ids; the game's rules row by row, the templates and the newest orders entry by block; a changed row adds one version and an unchanged pass none; a text set back is a new version; `changes --since` lists only what changed; a section that leaves keeps its history; a fault of the history is named and the pass goes on; the briefing lists the changes and only counts the member's own; a full pass over copies of the real repository files and a pass with no change, timed. No engine, no network."""

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

RULEBOOK = """---
name: rulebook
id: 20990101T000001Z
tier: guide
author: Unity
---

# rulebook.md -- The Rulebook

Read at every session start.

# Part A -- The Game

## 1. The Game

- A game of ships.

```
# not a heading: inside a fence
```

# Part B -- How We Play

## 12. Standing Rules

How the fleet carries out the standing orders.

| Rule | Says |
|---|---|
| F1 Chain of command | Each Admiral commands its own ships |
| F2 Stance (Suggi) | No ship fires first |
| F7 Wallet floor (Suggi) | Every pilot keeps 3,000 cr; a pipe \\| stays in its cell |
"""

RULES = """---
name: rules-07-economy
id: 20990101T000002Z
tier: rules
author: Unity
---

# Rules 07 -- Economy

Digest of the official pages.
| Topic | Rule |
|---|---|
| Credits | Only currency |
| Mining | `mine` (1 tick) |
"""

GUIDE = """# mining.md -- Guidebook of the Mining Division

## Class Card

### Ships

A hull with room.

### Skills

| Skill | Level |
|---|---|
| mining | 10 |

## 4. Levelling Guide

Mine.
"""

ORDERS = """## [ENT-001] | 2099-01-01 10:00 UTC | Unity | order
Changed: the first.
DIRECTION (his words)
D1. Old direction.

## [ENT-002] | 2099-01-02 10:00 UTC | Unity | order | see: ENT-001
Changed: the second.
In force from this entry until a newer one.
STANDING ORDERS (Suggi)
S1. Explore freely.
DIRECTION (his words)
D1. Income first: be positive.
D2. You are the players.
PLAN (the reading)
P1. No ship is idle (rule F8).
  Goal: the fill gate says PASS.
TURN (the tasks of now)
None beyond the blocks below.
ZERO, Mining (the miner- ships)
Order: mine.
Measure: units.
"""

TEMPLATES = {"division": "mining", "owner": "Zero", "templates": {"ice-sell": {"title": "Ice sold", "routes": ["a", "b"]},
                                                                   "reserve": {"title": "For the reserve", "routes": ["c"]}}}


def load(name, required=True):
    path = FLEET / (name + ".py")
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(name + "_docs_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text, mtime=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii")
    if mtime is not None:
        os.utime(path, (mtime, mtime))


def bump(path, text=None):
    """Change a file: a new text when given, and an mtime the last pass did not see."""
    if text is not None:
        path.write_text(text, encoding="ascii")
    later = path.stat().st_mtime + 7
    os.utime(path, (later, later))


class ParseTests(unittest.TestCase):
    def setUp(self):
        self.docs = load("docs")
        if self.docs is None:
            self.fail("game/fleet/docs.py is missing: the fleet's written knowledge is not parsed by section")
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-docs-parse-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)

    def sections(self, rel, text):
        write(self.repo / rel, text)
        return self.docs.parse(self.repo / rel)

    def test_a_rulebook_yields_one_section_per_rule_row_with_stable_ids(self):
        found = self.sections("governance/rulebook.md", RULEBOOK)
        ids = [sid for sid, _title, _text in found]
        self.assertEqual(ids, ["top", "part-a-the-game", "part-a-the-game/1-the-game", "part-b-how-we-play", "part-b-how-we-play/12-standing-rules",
                               "F1", "F2", "F7"])
        by = {sid: (title, text) for sid, title, text in found}
        self.assertEqual(by["F2"], ("F2 Stance (Suggi)", "No ship fires first"))
        self.assertEqual(by["F7"][1], "Every pilot keeps 3,000 cr; a pipe \\| stays in its cell")
        self.assertNotIn("F1 Chain", by["part-b-how-we-play/12-standing-rules"][1])            # a rule row is no part of its heading's text
        self.assertIn("| Rule | Says |", by["part-b-how-we-play/12-standing-rules"][1])
        self.assertIn("# not a heading", by["part-a-the-game/1-the-game"][1])                  # a fence keeps its lines
        self.assertNotIn("id: 2099", by["top"][1])                                              # the frontmatter is no section
        changed = self.sections("governance/rulebook.md", RULEBOOK.replace("No ship fires first", "No ship of ours fires first"))
        self.assertEqual([sid for sid, _t, _x in changed], ids)                                  # the ids stand when a text changes
        shas = lambda rows: {sid: self.docs.sha(title, text) for sid, title, text in rows}
        moved = {sid for sid, digest in shas(changed).items() if shas(found)[sid] != digest}
        self.assertEqual(moved, {"F2"})

    def test_the_rules_row_by_row_a_guidebook_by_heading_the_templates_and_the_newest_orders_entry_by_block(self):
        rules = self.sections("game/rules/07-economy.md", RULES)
        self.assertEqual([(sid, title) for sid, title, _x in rules], [("top", "Rules 07 -- Economy"), ("credits", "Credits"), ("mining", "Mining")])
        guide = self.sections("game/routes/guidebook/mining.md", GUIDE)
        self.assertEqual([sid for sid, _t, _x in guide], ["top", "class-card", "class-card/ships", "class-card/skills", "4-levelling-guide"])
        self.assertIn("| mining | 10 |", dict((s, x) for s, _t, x in guide)["class-card/skills"])   # a guidebook's tables stay in their section
        self.assertEqual(self.docs.kind_of("game/routes/guidebook/military.md"), ("guidebook", "Military"))
        self.assertEqual(self.docs.kind_of("game/routes/templates/command.json"), ("template", "Command"))
        self.assertEqual(self.docs.kind_of("communications/orders.log"), ("orders", "Unity"))
        self.assertEqual(self.docs.kind_of("game/rules/01-game.md"), ("rules", "Fleet"))
        templates = self.sections("game/routes/templates/mining.json", json.dumps(TEMPLATES))
        self.assertEqual([(sid, title) for sid, title, _x in templates], [("ice-sell", "Ice sold"), ("reserve", "For the reserve")])
        self.assertEqual(json.loads(templates[0][2]), TEMPLATES["templates"]["ice-sell"])
        orders = self.sections("communications/orders.log", ORDERS)
        by = {sid: (title, text) for sid, title, text in orders}
        self.assertEqual(list(by), ["head", "standing-orders", "S1", "direction", "D1", "D2", "plan", "P1", "turn", "zero"])
        self.assertEqual(by["D1"], ("D1. Income first", "D1. Income first: be positive."))         # the newest entry only
        self.assertEqual(by["P1"][1], "P1. No ship is idle (rule F8).\n  Goal: the fill gate says PASS.")
        self.assertIn("ENT-002", by["head"][0])
        self.assertIn("Changed: the second.", by["head"][1])
        self.assertEqual(by["zero"][1], "ZERO, Mining (the miner- ships)\nOrder: mine.\nMeasure: units.")
        self.assertEqual(by["turn"][1], "TURN (the tasks of now)\nNone beyond the blocks below.")


class StoreTests(unittest.TestCase):
    """The store's pass over a disposable repository: table docs now, doc_versions for good."""

    def setUp(self):
        self.store = load("store")
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-docs-store-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.data, self.repo = base / "data", base / "repo"
        self.root = self.repo / "game"
        self.data.mkdir()
        write(self.repo / "governance" / "rulebook.md", RULEBOOK)
        write(self.repo / "governance" / "strategy.md", "# Strategy\n\n## I. Purpose\n\nWin.\n")
        write(self.repo / "game" / "routes" / "guidebook" / "mining.md", GUIDE)
        write(self.repo / "game" / "routes" / "templates" / "mining.json", json.dumps(TEMPLATES))
        write(self.repo / "game" / "rules" / "07-economy.md", RULES)
        write(self.repo / "communications" / "orders.log", ORDERS)
        write(self.repo / "communications" / "reports.log", "## [ENT-001] | 2099-01-01 09:00 UTC | Zero | session | ref: reports/x.md\nSession: x\n\n"
                                                          "## [ENT-002] | 2099-01-02 12:00 UTC | Zero | session | ref: reports/y.md\nSession: y\n\n"
                                                          "## [ENT-003] | 2099-01-03 13:00 UTC | Mercury | session | ref: reports/z.md\nSession: z\n")
        self.t0 = 4070908800                         # 2099-01-01 00:00 UTC

    def one(self, now):
        return self.store.one_pass(str(self.data), now=now, root=str(self.root))

    def live(self, sql, args=()):
        conn = sqlite3.connect(str(self.data / "store" / "live.db"))
        try:
            return conn.execute(sql, args).fetchall()
        finally:
            conn.close()

    def read(self, sql, args=()):
        conn = self.store.connect(str(self.data))
        try:
            return conn.execute(sql, args).fetchall()
        finally:
            conn.close()

    def docs(self):
        found = load("docs")
        if found is None:
            self.fail("game/fleet/docs.py is missing")
        return found

    def test_the_store_mirrors_every_section_and_keeps_a_version_only_when_a_text_changed(self):
        self.assertIn("docs", [name for name, _columns, _key in self.store.SNAPSHOT], "store.py has no table docs: the written knowledge is not in the store")
        out = self.one(self.t0)
        self.assertEqual(out["snapshot"]["loaded"]["docs"], 6)
        self.assertEqual(out["versions"]["error"], None)
        sections = self.read("SELECT COUNT(*) FROM docs")[0][0]
        self.assertEqual(sections, 8 + 2 + 5 + 2 + 3 + 10)                  # rulebook, strategy, guidebook, templates, rules, orders
        self.assertEqual(self.read("SELECT COUNT(*) FROM doc_versions")[0][0], sections)
        self.assertEqual(self.read("SELECT owner, COUNT(*) FROM docs GROUP BY owner ORDER BY owner"), [("Fleet", 13), ("Mining", 7), ("Unity", 10)])
        self.assertEqual(self.read("SELECT value FROM meta WHERE key = 'docs.baseline'"), [(self.t0,)])
        self.assertEqual(self.read("SELECT section, n, kind FROM docs WHERE path = 'governance/rulebook.md' AND section LIKE 'F%' ORDER BY n"),
                         [("F1", 6, "rulebook"), ("F2", 7, "rulebook"), ("F7", 8, "rulebook")])
        out = self.one(self.t0 + 60)                                         # nothing changed: no file read, no version
        self.assertEqual((out["snapshot"]["loaded"].get("docs", 0), out["versions"]["added"], out["versions"]["standing"]), (0, 0, sections))
        bump(self.repo / "governance" / "rulebook.md")                       # read again, the same text: no version
        out = self.one(self.t0 + 120)
        self.assertEqual((out["snapshot"]["loaded"]["docs"], out["versions"]["added"]), (1, 0))
        bump(self.repo / "governance" / "rulebook.md", RULEBOOK.replace("No ship fires first", "No ship of ours fires first"))
        out = self.one(self.t0 + 180)
        self.assertEqual(out["versions"]["added"], 1)
        self.assertEqual(self.live("SELECT COUNT(*) FROM doc_versions")[0][0], sections + 1)
        self.assertEqual(self.live("SELECT section, first_seen, last_seen FROM doc_versions WHERE path = 'governance/rulebook.md' AND section = 'F2' ORDER BY version"),
                         [("F2", self.t0, self.t0 + 120), ("F2", self.t0 + 180, self.t0 + 180)])
        self.assertEqual(self.live("SELECT last_seen FROM doc_versions WHERE section = 'F1'"), [(self.t0 + 180,)])     # a version that stands moves on
        self.assertEqual(self.read("SELECT text FROM docs WHERE section = 'F2'"), [("No ship of ours fires first",)])

    def test_a_text_set_back_is_a_new_version_and_a_section_that_leaves_keeps_its_history(self):
        path = self.repo / "governance" / "rulebook.md"
        self.one(self.t0)
        bump(path, RULEBOOK.replace("No ship fires first", "Changed"))
        self.one(self.t0 + 60)
        bump(path, RULEBOOK)
        self.one(self.t0 + 120)
        self.assertEqual(self.live("SELECT text, first_seen FROM doc_versions WHERE section = 'F2' ORDER BY version"),
                         [("No ship fires first", self.t0), ("Changed", self.t0 + 60), ("No ship fires first", self.t0 + 120)])
        bump(path, RULEBOOK.replace("| F7 Wallet floor (Suggi) | Every pilot keeps 3,000 cr; a pipe \\| stays in its cell |\n", ""))
        self.one(self.t0 + 180)
        self.assertEqual(self.read("SELECT COUNT(*) FROM docs WHERE section = 'F7'"), [(0,)])
        self.assertEqual(self.live("SELECT first_seen, last_seen FROM doc_versions WHERE section = 'F7'"), [(self.t0, self.t0 + 120)])
        (self.repo / "governance" / "strategy.md").unlink()                  # a whole file goes: its rows leave docs, its versions stay
        self.one(self.t0 + 240)
        self.assertEqual(self.live("SELECT last_seen FROM doc_versions WHERE section = 'F7'"), [(self.t0 + 120,)])   # its last_seen stops
        self.assertEqual(self.read("SELECT COUNT(*) FROM docs WHERE path = 'governance/strategy.md'"), [(0,)])
        self.assertEqual(self.live("SELECT COUNT(*), MAX(last_seen) FROM doc_versions WHERE path = 'governance/strategy.md'"), [(2, self.t0 + 180)])
        docs = self.docs()
        conn = self.store.connect(str(self.data))
        try:
            rows, _baseline = docs.changed(conn, self.t0 + 100)
        finally:
            conn.close()
        self.assertEqual([(r[0], r[1], r[2]) for r in rows], [("changed", "governance/rulebook.md", "F2"), ("gone", "governance/rulebook.md", "F7"),
                                                               ("gone", "governance/strategy.md", "i-purpose"), ("gone", "governance/strategy.md", "top")])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(docs.show_docs(str(self.data), self.t0 + 300, "rulebook", "F7", "", True), 0)
        self.assertIn("HISTORY governance/rulebook.md F7 | 1 versions on record", out.getvalue())
        self.assertIn("gone from its file", out.getvalue())

    def test_changes_since_lists_only_the_changed_section_and_the_briefing_counts_the_members_own(self):
        docs = self.docs()
        self.one(self.t0)
        bump(self.repo / "governance" / "rulebook.md", RULEBOOK.replace("No ship fires first", "No ship of ours fires first"))
        guide = GUIDE.replace("A hull with room.", "A bigger hull.")
        bump(self.repo / "game" / "routes" / "guidebook" / "mining.md", guide)
        later = self.t0 + 2 * 86400 + 6 * 3600                               # 2099-01-03 06:00 UTC: after Zero's last report, before Mercury's
        self.one(later)
        command = [sys.executable, "-I", "-B", str(HIVE), "changes", "--since", "2099-01-02T00:00Z", "--data", str(self.data), "--root", str(self.root)]
        done = subprocess.run(command, capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        lines = [line for line in done.stdout.splitlines() if line.split()[5:6] == ["changed"]]
        self.assertEqual([line.split()[:2] for line in lines], [["governance/rulebook.md", "F2"], ["game/routes/guidebook/mining.md", "class-card/ships"]])
        done = subprocess.run(command[:5] + ["--since", "2099-01-03T13:00Z"] + command[7:], capture_output=True, text=True, timeout=120)
        self.assertIn("no section changed", done.stdout)                     # a time after the change: nothing
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(docs.show_changes(str(self.root), str(self.data), later + 60, "", "Mercury"), 0)   # Mercury's last turn: 01-03 13:00
        self.assertIn("no section changed", out.getvalue())
        self.assertIn("Mercury's last turn: its newest entry in communications/reports.log, ENT-003", out.getvalue())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            docs.briefing(str(self.root), str(self.data), later + 60, "Zero")
        text = out.getvalue()
        self.assertTrue(text.startswith("=== CHANGED SINCE YOUR LAST TURN"), text)
        self.assertIn("ENT-002 of 2099-01-02 12:00 UTC", text)
        self.assertIn("governance/rulebook.md", text)
        self.assertNotIn("class-card/ships", text)                           # the member's own role's rules: counted, not listed
        self.assertIn("YOUR ROLE'S RULES (game/routes/guidebook/mining.md, game/routes/templates/mining.json): 7 sections, 1 changed since then", text)
        self.assertLessEqual(len(text.splitlines()), 1 + docs.BRIEF_ROWS)

    def test_a_fault_of_the_history_is_named_and_the_pass_goes_on(self):
        writings = self.store.writings
        real = writings.meta_of

        def broken(conn, key):
            raise RuntimeError("boom")
        writings.meta_of = broken
        self.addCleanup(setattr, writings, "meta_of", real)
        out = self.one(self.t0)
        self.assertEqual(out["versions"]["error"], "RuntimeError: boom")
        self.assertTrue(out["published"])                                     # the pass went on and published its copy
        self.assertIn("doc_versions (not kept: RuntimeError: boom)", self.store.said(out))   # named in the pass's line
        self.assertEqual(self.read("SELECT COUNT(*) FROM doc_versions"), [(0,)])          # rolled back: nothing half kept
        self.assertEqual(self.read("SELECT COUNT(*) FROM docs"), [(30,)])
        writings.meta_of = real
        out = self.one(self.t0 + 60)                                         # the next pass compares again and keeps them all
        self.assertEqual((out["versions"]["error"], out["versions"]["added"]), (None, 30))

    def test_the_readers_list_print_and_find_a_section(self):
        self.one(self.t0)
        bump(self.repo / "governance" / "rulebook.md", RULEBOOK.replace("No ship fires first", "No ship of ours fires first"))
        self.one(self.t0 + 60)
        run = lambda *words: subprocess.run([sys.executable, "-I", "-B", str(HIVE)] + list(words) + ["--data", str(self.data), "--root", str(self.root)],
                                            capture_output=True, text=True, timeout=120)
        done = run("docs")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertRegex(done.stdout, r"governance/rulebook.md\s+rulebook\s+Fleet\s+8 ")
        done = run("docs", "Zero")                                                 # a member's name: its division's files
        self.assertIn("game/routes/guidebook/mining.md | guidebook, Mining | 5 sections", done.stdout)
        self.assertIn("game/routes/templates/mining.json | template, Mining | 2 sections", done.stdout)
        done = run("docs", "rulebook", "--section", "F2")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertTrue(done.stdout.startswith("DOCS governance/rulebook.md F2 | F2 Stance (Suggi) | 27 chars | rulebook, Fleet | this text since"))
        self.assertIn("2 versions on record", done.stdout)
        self.assertEqual(done.stdout.splitlines()[1], "No ship of ours fires first")
        done = run("docs", "rulebook", "--section", "F2", "--history")
        self.assertIn("-No ship fires first", done.stdout)
        self.assertIn("+No ship of ours fires first", done.stdout)
        done = run("docs", "--section", "top")                                     # an id many files carry: name the file
        self.assertEqual(done.returncode, 1)
        self.assertIn("sections answer to `top`", done.stdout)
        done = run("docs", "--grep", "levelling")
        self.assertIn("=== game/routes/guidebook/mining.md 4-levelling-guide", done.stdout)
        done = run("docs", "nothing-like-this")
        self.assertEqual(done.returncode, 1)


class ToolTests(unittest.TestCase):
    def test_the_tool_docs_builds_the_line_of_hive_py(self):
        spec = importlib.util.spec_from_file_location("collective_mcp_docs_under_test", FLEET / "collective_mcp.py")
        server = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server)
        self.assertIn("docs", sorted(server.TOOLS), "the MCP server has no tool docs")
        plan = server.TOOLS["docs"]["plan"]
        self.assertEqual(plan({}), [("game/fleet/hive.py", ["docs"])])
        self.assertEqual(plan({"view": "list", "doc": "Mining", "grep": "hull"}), [("game/fleet/hive.py", ["docs", "Mining", "--grep", "hull"])])
        self.assertEqual(plan({"view": "section", "doc": "rulebook", "section": "F8"}), [("game/fleet/hive.py", ["docs", "rulebook", "--section", "F8"])])
        self.assertEqual(plan({"view": "history", "section": "D3"}), [("game/fleet/hive.py", ["docs", "--section", "D3", "--history"])])
        self.assertEqual(plan({"view": "changes", "since": "6h", "member": "Zero"}), [("game/fleet/hive.py", ["changes", "--since", "6h", "--member", "Zero"])])
        with self.assertRaises(ValueError):
            plan({"view": "section"})
        self.assertEqual(server.call(str(REPO), "", "zero", "docs", {"view": "history"}), ("docs: this needs: section", True))


class TimingTests(unittest.TestCase):
    """A full pass over copies of the repository's real source files, then a pass with no change; both timed and printed."""

    def test_a_full_pass_on_the_real_files_and_a_pass_with_no_change(self):
        store, docs = load("store"), load("docs")
        if docs is None:
            self.fail("game/fleet/docs.py is missing")
        with tempfile.TemporaryDirectory(prefix="fleet-docs-timing-") as temp:
            repo, data = Path(temp) / "repo", Path(temp) / "data"
            data.mkdir()
            copied = 0
            for rel, path, _kind, _owner in docs.sources(REPO):
                (repo / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, repo / rel)
                copied += 1
            self.assertGreater(copied, 10)
            begun = time.time()
            first = store.one_pass(str(data), now=begun, root=str(repo / "game"))
            full = time.time() - begun
            sections = first["versions"]["added"]
            begun = time.time()
            second = store.one_pass(str(data), now=begun + 60, root=str(repo / "game"))
            still = time.time() - begun
            conn = sqlite3.connect(str(data / "store" / "live.db"))
            try:
                stored = conn.execute("SELECT COUNT(*), SUM(chars) FROM docs").fetchone()
            finally:
                conn.close()
        print("\n  timing: %d files, %d sections, %d characters; a full pass %.2f s (store.py's own %.2f s), a pass with no change %.2f s (%.2f s)"
              % (copied, stored[0], stored[1], full, first["seconds"], still, second["seconds"]))
        self.assertEqual(first["snapshot"]["loaded"]["docs"], copied)
        self.assertEqual(stored[0], sections)
        self.assertEqual((second["snapshot"]["loaded"].get("docs", 0), second["versions"]["added"], second["versions"]["standing"]), (0, 0, sections))
        self.assertLess(full, 60)
        self.assertLess(still, 30)


if __name__ == "__main__":
    unittest.main()
