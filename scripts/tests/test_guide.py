"""scripts/guide.py and game/fleet/guidebook.py: the guidebooks as capped chapters of entries. The gate passes a clean
division and refuses each fault alone (form, caps, chapter names, a doubled title, an old file beside its chapters);
the split of an old guidebook loses no line (the entries read back equal the old text minus its headings), maps each
section to its chapter, dates each entry by git blame, refuses a split that would change a line and takes a source
file (command: DESIGN.md); the store mirrors every entry as its own section of kind guide owned by the division, with
every version kept; tidy takes a retired entry out only once the store holds it, and the store keeps it; the readers
(hive.py guide, the briefing, hive.py division, the tool docs) read it from the store; a pass over the real chapters
is timed. No engine, no network.
"""

import contextlib
import importlib.util
import io
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

REPO = Path(__file__).resolve().parents[2]
FLEET = REPO / "game" / "fleet"
SCRIPT = REPO / "scripts" / "guide.py"
HIVE = FLEET / "hive.py"
NOW = 4070908800                                   # 2099-01-01 00:00 UTC
OLD = """---
name: guidebook-military
id: 20990101T000003Z
tier: intel
author: Unity
---

# military.md -- Guidebook of the Military Division

Kept by Apophis; read by every member.

- A figure carries its date.

## Class Card

The class in short.

### Ships

- Tier 0: the Threshold.

### Skills

| Skill | Why |
|---|---|
| Weapons | damage |

## Standing Plan

What the drones fly.

## 1. Route Guides

How a route is built.

### Hunts of grazers (`hunt.py`)

Hunt the grazers.

```
## not a heading: inside a fence
### nor this
```

### Guard (`guard.py`)

Guard the miners.

## 4. Levelling Guide

Weapons first.

## 5. Ships and Fits

A fit.

## 6. Pirates

Flee from a pack.

#### A sub-heading of an entry

It stays in its entry.

## 7. Open Tests

None open.

## 8. Ships

A second section of that title.
"""


def load(name, path):
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text, mtime=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii")
    if mtime is not None:
        os.utime(path, (mtime, mtime))


def bump(path, text):
    path.write_text(text, encoding="ascii")
    later = path.stat().st_mtime + 7
    os.utime(path, (later, later))


def entry(title, body, status="proven", updated="2026-11-01", evidence="hive.py route x", extra=""):
    return "### %s\nStatus: %s. Updated: %s.%s Evidence: %s.\n\n%s\n" % (title, status, updated, extra, evidence, body)


def chapter(name, chapter_name, *entries):
    return "# %s guidebook -- %s (%s.md)\n\n%s" % (name.capitalize(), chapter_name, chapter_name, "\n".join(entries))


def tool():
    """scripts/guide.py, or the test fails: without it no guidebook is capped."""
    found = load("guide_under_test", SCRIPT)
    if found is None:
        raise AssertionError("scripts/guide.py is missing: the guidebooks are not chapters with caps")
    return found


class Base(unittest.TestCase):
    def setUp(self):
        self.guide = tool()
        self.book = self.guide.book
        self.temp = tempfile.TemporaryDirectory(prefix="guide-test-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.shelf = self.repo / "game" / "routes" / "guidebook"

    def division(self, name="mining", **chapters):
        """A division's six chapters, each with one small entry unless given."""
        for c in self.book.CHAPTERS:
            text = chapters.get(c, chapter(name, c, entry("%s entry" % c.capitalize(), "Do this, because that.")))
            write(self.shelf / name / (c + ".md"), text)
        for c, text in chapters.items():
            if c not in self.book.CHAPTERS:
                write(self.shelf / name / (c + ".md"), text)

    def errors(self, which="mining"):
        return self.guide.check(self.repo, which, now=NOW)[0]


class FormTests(Base):
    def test_a_clean_division_passes_and_the_caps_stand_in_guidebook_py_only(self):
        self.division()
        self.assertEqual(self.errors(), [])
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "check", "mining", "--root", str(self.repo)], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn("Errors: 0 | Warnings: 0", done.stdout)
        source = SCRIPT.read_text(encoding="ascii")
        for name in ("CARD_MAX =", "CHAPTER_MAX =", "ENTRY_MAX =", "CHAPTERS_MAX =", "TOPICS ="):
            self.assertNotIn(name, source, "a cap stands twice: %s" % name)
        self.assertEqual((self.book.CARD_MAX, self.book.CHAPTER_MAX, self.book.ENTRY_MAX, self.book.CHAPTERS_MAX), (4500, 12000, 2250, 8))
        self.assertIn("command", self.book.DIVISIONS)

    def test_each_fault_alone_halts(self):
        cases = {
            "no status line": {"ships": chapter("mining", "ships", "### A\nThe body only.\n")},
            "is none of": {"ships": chapter("mining", "ships", entry("A", "x", status="maybe"))},
            "is no date": {"ships": chapter("mining", "ships", entry("A", "x", updated="2099-13-40"))},
            "lies in the future": {"ships": chapter("mining", "ships", entry("A", "x", updated="2099-02-01"))},
            "over the entry's cap": {"ships": chapter("mining", "ships", entry("A", "y" * 2300))},
            "card.md: 4,": {"card": chapter("mining", "card", entry("A", "c" * 2100), entry("B", "c" * 2100), entry("C", "c" * 500))},
            "over its cap of 12,000": {"lessons": chapter("mining", "lessons", *[entry("L%d" % n, "l" * 2100) for n in range(6)])},
            "the id `ships-entry`": {"lessons": chapter("mining", "lessons", entry("Ships entry", "a second of that title"))},
            "the id `same`": {"lessons": chapter("mining", "lessons", entry("One", "a", extra=" Id: same."), entry("Two", "b", extra=" Id: same."))},
            "a heading `## Part`": {"tests": chapter("mining", "tests", entry("A", "x")) + "\n## Part\n"},
            "no chapter": {"notes": "# notes\n"},
            "3 topic chapters": {"topic-a": chapter("mining", "topic-a"), "topic-b": chapter("mining", "topic-b"), "topic-c": chapter("mining", "topic-c")},
            "not ASCII": {"routes": chapter("mining", "routes", entry("A", "caf" + chr(0xe9)))},
            "between its title and its first entry": {"routes": chapter("mining", "routes", "h" * 500 + "\n\n" + entry("A", "x"))},
            "no title": {"routes": entry("A", "x")},
        }
        for word, chapters in cases.items():
            with self.subTest(word):
                shutil.rmtree(self.shelf, ignore_errors=True)
                if word == "not ASCII":
                    self.division()
                    (self.shelf / "mining" / "routes.md").write_bytes(chapters["routes"].encode("latin-1"))
                else:
                    self.division(**chapters)
                found = self.errors()
                self.assertTrue(any(word in line for line in found), "%s not in %s" % (word, found))
        shutil.rmtree(self.shelf, ignore_errors=True)
        self.division()
        (self.shelf / "mining" / "tests.md").unlink()
        self.assertTrue(any("tests.md: missing" in line for line in self.errors()))
        self.division()
        write(self.shelf / "mining.md", "# old\n")
        self.assertTrue(any("stands beside its chapters" in line for line in self.errors()))
        shutil.rmtree(self.shelf / "mining")
        self.assertTrue(any("not split into chapters yet" in line for line in self.errors()))
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "check", "mining", "--root", str(self.repo)], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 1)
        self.assertIn("HALT game/routes/guidebook/mining.md: not split", done.stdout)

    def test_an_entry_parses_into_its_parts_and_a_fence_is_never_split(self):
        text = chapter("mining", "lessons", entry("Fences", "```\n### not an entry\n```\nafter", extra=" Id: kept-id."))
        found = self.book.parse(text)
        self.assertEqual(found["title"], "Mining guidebook -- lessons (lessons.md)")
        self.assertEqual(len(found["entries"]), 1)
        e = found["entries"][0]
        self.assertEqual((e["status"], e["updated"], e["id"], e["evidence"]), ("proven", "2026-11-01", "kept-id", "hive.py route x."))
        self.assertEqual(e["body"], "```\n### not an entry\n```\nafter")
        self.assertEqual(self.book.sections(text, "lessons"), [("kept-id", "[lessons proven 2026-11-01] Fences", e["text"])])


class SplitTests(Base):
    def old(self, text=OLD, name="military"):
        write(self.shelf / (name + ".md"), text)

    def back(self, name):
        """{title: (chapter, entry)} read back from the written chapters."""
        out = {}
        for path in sorted((self.shelf / name).glob("*.md")):
            for e in self.book.parse(path.read_text(encoding="ascii"))["entries"]:
                out[e["title"]] = (path.stem, e)
        return out

    def test_the_split_loses_no_line_and_maps_each_section_to_its_chapter(self):
        self.old()
        done, kept = self.guide.split(self.repo, "military", updated="2098-12-31", now=NOW)
        self.assertFalse((self.shelf / "military.md").exists(), "the old file stays: its text would stand twice")
        self.assertEqual(sorted(done), sorted(list(self.book.CHAPTERS) + ["topic-pirates"]))
        read = self.back("military")
        order = ["How this guidebook is kept", "Class Card", "Ships", "Skills", "Standing Plan", "Route Guides", "Hunts of grazers (`hunt.py`)",
                 "Guard (`guard.py`)", "Levelling Guide", "Ships and Fits", "Pirates", "Open Tests", "Ships (section 8)"]
        self.assertEqual(sorted(read), sorted(order))
        where = {title: c for title, (c, _e) in read.items()}
        self.assertEqual([where[t] for t in order], ["lessons", "card", "card", "card", "routes", "routes", "routes", "routes", "levelling", "ships",
                                                     "topic-pirates", "tests", "lessons"])
        heading = lambda line: line.startswith(("# ", "## ", "### "))
        lines, fence = [], False
        for line in OLD.split("---\n", 2)[2].splitlines():
            if line.startswith("```"):
                fence = not fence
            if fence or line.startswith("```") or not heading(line):
                lines.append(line)
        concatenated = "\n".join(read[t][1]["body"] for t in order)
        self.assertEqual([x for x in concatenated.splitlines() if x.strip()], [x for x in lines if x.strip()])     # no line lost, none added, the order kept
        self.assertIn("## not a heading: inside a fence", read["Hunts of grazers (`hunt.py`)"][1]["body"])
        self.assertIn("#### A sub-heading of an entry", read["Pirates"][1]["body"])
        self.assertEqual(read["Guard (`guard.py`)"][1]["status_line"],
                         "Status: proven. Updated: 2098-12-31. Evidence: migrated from guidebook/military.md section 1.")
        self.assertEqual(read["How this guidebook is kept"][1]["evidence"], "migrated from guidebook/military.md, the text above its first section.")
        self.assertEqual(self.guide.check(self.repo, "military", now=NOW)[0], [])          # the split's own form passes the gate
        with self.assertRaises(self.guide.SplitError):                                     # never twice into a folder with chapters
            self.old()
            self.guide.split(self.repo, "military", updated="2098-12-31", now=NOW)

    def test_a_split_that_would_change_a_line_is_refused_and_writes_nothing(self):
        self.old()
        real = self.guide.render

        def lossy(name, entries):
            texts = real(name, entries)
            texts["ships"] = texts["ships"].replace("A fit.", "A fit, changed.")
            return texts
        self.guide.render = lossy
        self.addCleanup(setattr, self.guide, "render", real)
        with self.assertRaises(self.guide.SplitError) as caught:
            self.guide.split(self.repo, "military", updated="2098-12-31", now=NOW)
        self.assertIn("reads back changed", str(caught.exception))
        self.assertTrue((self.shelf / "military.md").is_file())
        self.assertFalse((self.shelf / "military").exists())

    @unittest.skipUnless(shutil.which("git"), "git is missing")
    def test_each_entry_is_dated_by_the_last_commit_of_its_lines(self):
        self.old()
        env = dict(os.environ, GIT_AUTHOR_NAME="T", GIT_AUTHOR_EMAIL="t@x", GIT_COMMITTER_NAME="T", GIT_COMMITTER_EMAIL="t@x",
                   GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        git = lambda *words, when=None: subprocess.run(["git", "-C", str(self.repo)] + list(words), check=True, capture_output=True, timeout=60,
                                                       env=dict(env, **({"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when} if when else {})))
        git("init", "-q")
        git("add", "-A")
        git("commit", "-q", "-m", "one", when="2098-12-01T10:00:00Z")
        bump(self.shelf / "military.md", OLD.replace("Guard the miners.", "Guard the miners well."))
        git("commit", "-q", "-am", "two", when="2098-12-20T10:00:00Z")
        self.guide.split(self.repo, "military", now=NOW)
        read = self.back("military")
        self.assertEqual(read["Guard (`guard.py`)"][1]["updated"], "2098-12-20")
        self.assertEqual(read["Pirates"][1]["updated"], "2098-12-01")
        bump(self.shelf / "military" / "ships.md", "# x\n")                         # a file that differs from HEAD is never blamed
        (self.shelf / "military.md").write_text(OLD + "\nnot committed\n", encoding="ascii")
        shutil.rmtree(self.shelf / "military")
        with self.assertRaises(self.guide.SplitError) as caught:
            self.guide.split(self.repo, "military", now=NOW)
        self.assertIn("differs from its text at HEAD", str(caught.exception))

    def test_command_splits_a_source_file_and_leaves_it_where_it_stands(self):
        source = Path(self.temp.name) / "DESIGN.md"
        write(source, "# DESIGN.md -- Fleet Design\n\nWhat it holds.\n\n## 1. Game Facts That Shape the Fleet\n\nOne account, one ship.\n\n"
                      "## 3. The Design in Force\n\n### 3.1. Three Layers, Three Speeds\n\nStrategy, command, execution.\n\n## 6. The Work Cycle\n\nA turn every four hours.\n")
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "split", "command", "--source", str(source), "--updated", "2098-12-31",
                               "--root", str(self.repo)], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertTrue(source.is_file())
        read = self.back("command")
        self.assertEqual({t: c for t, (c, _e) in read.items()}, {"About DESIGN.md": "lessons", "Game Facts That Shape the Fleet": "lessons",
                                                                   "Three Layers, Three Speeds": "topic-design", "The Work Cycle": "topic-systems"})
        self.assertEqual(read["Three Layers, Three Speeds"][1]["evidence"], "migrated from DESIGN.md section 3.1.")


class StoreTests(Base):
    """The store's pass over a disposable repository: one section an entry, every version kept; tidy; the readers."""

    def setUp(self):
        super().setUp()
        self.store = load("store_guide_under_test", FLEET / "store.py")
        self.docs = self.store.writings
        self.data = Path(self.temp.name) / "data"
        self.data.mkdir()
        self.root = self.repo / "game"
        self.division("mining", card=chapter("mining", "card", entry("Ships", "Tier 0: the Threshold."), entry("Skills", "Mining first.")),
                      routes=chapter("mining", "routes", entry("Ice", "Sell ice where a bid stands."), entry("Old ice", "A bid gone.")))
        self.division("command", card=chapter("command", "card", entry("Lead by intent", "What and why, never the how.")))
        write(self.repo / "communications" / "reports.log", "## [ENT-001] | 2098-12-01 09:00 UTC | Zero | session | ref: reports/x.md\nSession: x\n")

    def one(self, now):
        return self.store.one_pass(str(self.data), now=now, root=str(self.root))

    def read(self, sql, args=()):
        conn = self.store.connect(str(self.data))
        try:
            return conn.execute(sql, args).fetchall()
        finally:
            conn.close()

    def hive(self, *words, env=None):
        return subprocess.run([sys.executable, "-I", "-B", str(HIVE)] + list(words) + ["--data", str(self.data), "--root", str(self.root)],
                              capture_output=True, text=True, timeout=120, env=dict(os.environ, **(env or {})))

    def test_every_entry_is_its_own_section_of_kind_guide_with_every_version_kept(self):
        self.assertEqual(self.docs.kind_of("game/routes/guidebook/mining/card.md"), ("guide", "Mining"))
        self.assertEqual(self.docs.kind_of("game/routes/guidebook/command/topic-design.md"), ("guide", "Command"))
        self.assertEqual(self.docs.kind_of("game/routes/guidebook/mining.md"), ("guidebook", "Mining"))        # the old files' versions keep their kind
        out = self.one(NOW)
        self.assertEqual(out["versions"]["error"], None)
        rows = self.read("SELECT owner, section, title, chars FROM docs WHERE path = 'game/routes/guidebook/mining/routes.md' ORDER BY n")
        self.assertEqual([r[:3] for r in rows], [("Mining", "ice", "[routes proven 2026-11-01] Ice"), ("Mining", "old-ice", "[routes proven 2026-11-01] Old ice")])
        text = self.read("SELECT text FROM docs WHERE path = 'game/routes/guidebook/mining/routes.md' AND section = 'ice'")[0][0]
        self.assertEqual(rows[0][3], len(text))
        self.assertTrue(text.startswith("Status: proven. Updated: 2026-11-01. Evidence:"))
        self.assertEqual(self.read("SELECT COUNT(*) FROM docs WHERE kind = 'guide'"), [(8 + 6,)])
        self.assertEqual(self.read("SELECT DISTINCT owner FROM docs WHERE kind = 'guide' ORDER BY owner"), [("Command",), ("Mining",)])
        path = self.shelf / "mining" / "routes.md"
        bump(path, path.read_text(encoding="ascii").replace("Sell ice where a bid stands.", "Sell ice where a bid stands and regains."))
        out = self.one(NOW + 60)
        self.assertEqual(out["versions"]["added"], 1)                                          # one entry changed: one version, its chapter's others none
        self.assertEqual(self.read("SELECT COUNT(*) FROM doc_versions WHERE path = 'game/routes/guidebook/mining/routes.md' AND section = 'ice'"), [(2,)])
        bump(path, path.read_text(encoding="ascii").replace("### Ice\nStatus: proven. Updated: 2026-11-01.", "### Ice where a bid stands\nStatus: proven. Updated: 2026-11-01. Id: ice."))
        self.one(NOW + 120)                                                                    # renamed, its Id kept: the same key goes on
        self.assertEqual(self.read("SELECT COUNT(*) FROM doc_versions WHERE path = 'game/routes/guidebook/mining/routes.md' AND section = 'ice'"), [(3,)])

    def test_tidy_takes_a_retired_entry_out_only_once_the_store_holds_it_and_the_store_keeps_it(self):
        self.one(NOW)
        path = self.shelf / "mining" / "routes.md"
        bump(path, path.read_text(encoding="ascii").replace("### Old ice\nStatus: proven.", "### Old ice\nStatus: retired."))
        done = self.guide.tidy(self.repo, self.data, "mining")
        self.assertEqual((len(done["removed"]), len(done["waiting"])), (0, 1))                 # the store has not read the retired text yet
        self.assertIn("### Old ice", path.read_text(encoding="ascii"))
        self.one(NOW + 60)
        dry = self.guide.tidy(self.repo, self.data, "mining", dry=True)
        self.assertEqual(len(dry["removed"]), 1)
        self.assertIn("### Old ice", path.read_text(encoding="ascii"))                         # a dry run writes nothing
        done = self.guide.tidy(self.repo, self.data, "mining")
        self.assertEqual([x[1] for x in done["removed"]], ["old-ice"])
        left = path.read_text(encoding="ascii")
        self.assertNotIn("Old ice", left)
        self.assertTrue(left.endswith("Sell ice where a bid stands.\n"), left)
        self.assertEqual(self.guide.check(self.repo, "mining", now=NOW)[0], [])
        os.utime(path, (path.stat().st_mtime + 7,) * 2)
        self.one(NOW + 120)
        self.assertEqual(self.read("SELECT COUNT(*) FROM docs WHERE section = 'old-ice'"), [(0,)])
        kept = self.read("SELECT title, text FROM doc_versions WHERE path = 'game/routes/guidebook/mining/routes.md' AND section = 'old-ice' ORDER BY version")
        self.assertEqual([k[0] for k in kept], ["[routes proven 2026-11-01] Old ice", "[routes retired 2026-11-01] Old ice"])
        self.assertIn("A bid gone.", kept[-1][1])
        done = self.hive("guide", "mining", "--retired")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertRegex(done.stdout, r"mining\s+routes\s+old-ice\s+2026-11-01\s+retired, tidied")

    def test_the_readers_show_the_card_the_index_the_figures_and_the_caps(self):
        path = self.shelf / "mining" / "lessons.md"
        write(path, chapter("mining", "lessons", entry("Long", "l" * 2400)))
        self.one(NOW)
        done = self.hive("guide", "mining")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        text = done.stdout
        self.assertIn("=== THE CLASS CARD (game/routes/guidebook/mining/card.md, 2 entries", text)
        self.assertIn("### Ships\nStatus: proven. Updated: 2026-11-01. Evidence: hive.py route x.\n\nTier 0: the Threshold.", text)
        self.assertRegex(text, r"routes.md \| 2 entries, \d+ of 12,000 characters")
        self.assertRegex(text, r"proven\s+2026-11-01\s+[\d,]+\s+long\s+Long\s+OVER")
        self.assertIn("lessons.md entry `long`", text)
        self.assertRegex(text, r"XP per ship-hour of its roles' skills \(24 h, n = pilots that gained; computed [^)]*\): not measured")   # no figure yet
        write(self.root / "routes" / "mine-x.json", '{"kind": "mine", "stops": []}\n')
        write(self.root / "routes" / "census-z.json", '{"kind": "census", "stops": []}\n')
        conn = sqlite3.connect(str(self.data / "store" / "read.db"))
        try:
            conn.executemany("INSERT INTO stats_figures (view, subject, figure, hours, value, n, text, t) VALUES (?, ?, ?, ?, ?, ?, 'x', ?)", [
                ("xp", "miner|mining", "xp_per_ship_hour", 24.0, 120.5, 9, NOW), ("xp", "trader|trading", "xp_per_ship_hour", 24.0, 50.0, 3, NOW),
                ("xp", "mine-x", "route_xp_per_ship_hour", 24.0, 88.0, 12, NOW), ("xp", "census-z", "route_xp_per_ship_hour", 24.0, 99.0, 4, NOW),
                ("upgrades", "miner-1", "tier", 0.0, 0, 1, NOW), ("upgrades", "miner-1", "piloting", 0.0, 10, 1, NOW),
                ("upgrades", "miner-1", "piloting_next", 0.0, 10, 1, NOW), ("upgrades", "miner-1", "empty_utility", 0.0, 1, 2, NOW),
                ("upgrades", "trader-1", "tier", 0.0, 1, 1, NOW)])
            conn.commit()
        finally:
            conn.close()
        text = self.hive("guide", "mining").stdout                                             # the figures of the class only: its roles, its own class's routes
        self.assertIn("miner mining 120.5 n 9", text)
        self.assertNotIn("trading", text)
        self.assertIn("mine-x 88.0 n 12", text)
        self.assertNotIn("census-z", text)
        self.assertIn("Next upgrades (1 ships, computed 2099-01-01 00:00 UTC): tiers tier 0: 1; Piloting reaches the next tier's hulls: 1 ships "
                      "(0 not measured); empty slots: weapon 0, defense 0, utility 1", text)
        done = self.hive("guide", "--chapter", "routes", env={"HERMES_SESSION_PROFILE": "zero"})   # the member's own division by default
        self.assertIn("=== game/routes/guidebook/mining/routes.md ice", done.stdout)
        done = self.hive("guide", "all", "--grep", "intent")
        self.assertIn("### Lead by intent", done.stdout)
        self.assertNotIn("### Ice", done.stdout)
        done = self.hive("guide", "all")
        self.assertIn("Command | 6 chapters", done.stdout)
        sys.path.insert(0, str(FLEET))
        self.addCleanup(sys.path.remove, str(FLEET))
        import guidebook as reader
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.briefing(str(self.root), str(self.data), NOW + 60, "Zero")
        self.assertIn("=== MY CLASS CARD (game/routes/guidebook/mining/card.md", out.getvalue())
        self.assertIn("### Skills", out.getvalue())
        self.assertIn("OVER ITS CAP, Mining", out.getvalue())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.briefing(str(self.root), str(self.data), NOW + 60, "Unity")
        self.assertIn("### Lead by intent", out.getvalue())                                   # Unity's own card, and every division's caps
        self.assertIn("OVER ITS CAP, Mining", out.getvalue())
        conn = self.store.connect(str(self.data))
        try:
            lines = reader.division_part(conn, "Mining", cut=400)
        finally:
            conn.close()
        self.assertTrue(lines[0].startswith("GUIDEBOOK (game/routes/guidebook/mining/, 6 chapters, 8 entries"), lines)
        done = self.hive("division", "Zero")
        self.assertIn("GUIDEBOOK (game/routes/guidebook/mining/", done.stdout)


class ToolTests(unittest.TestCase):
    def test_the_tool_docs_has_the_view_guide_and_keeps_its_other_views(self):
        tool()
        server = load("collective_mcp_guide_under_test", FLEET / "collective_mcp.py")
        docs = server.TOOLS["docs"]
        self.assertIn("guide", docs["args"]["view"]["enum"])
        self.assertIn("chapter", docs["args"])
        plan = docs["plan"]
        self.assertEqual(plan({"view": "guide"}), [("game/fleet/hive.py", ["guide"])])
        self.assertEqual(plan({"view": "guide", "division": "Trade", "chapter": "tests", "grep": "fee", "retired": True}),
                         [("game/fleet/hive.py", ["guide", "Trade", "--chapter", "tests", "--grep", "fee", "--retired"])])
        self.assertEqual(plan({}), [("game/fleet/hive.py", ["docs"])])
        self.assertEqual(plan({"view": "division"}), [("game/fleet/hive.py", ["division", "all"])])


class TimingTests(unittest.TestCase):
    """The store's pass over copies of the repository's real chapter files: a full pass and one with no change."""

    def test_a_pass_over_the_real_chapters(self):
        tool()
        store = load("store_guide_timing", FLEET / "store.py")
        chapters = sorted((REPO / "game" / "routes" / "guidebook").glob("*/*.md"))
        self.assertGreater(len(chapters), 30)
        with tempfile.TemporaryDirectory(prefix="guide-timing-") as temp:
            repo, data = Path(temp) / "repo", Path(temp) / "data"
            data.mkdir()
            for path in chapters:
                target = repo / path.relative_to(REPO)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
            begun = time.time()
            first = store.one_pass(str(data), now=begun, root=str(repo / "game"))
            full = time.time() - begun
            begun = time.time()
            second = store.one_pass(str(data), now=begun + 60, root=str(repo / "game"))
            still = time.time() - begun
            conn = sqlite3.connect(str(data / "store" / "live.db"))
            try:
                stored = conn.execute("SELECT COUNT(*), SUM(chars) FROM docs WHERE kind = 'guide'").fetchone()
            finally:
                conn.close()
        print("\n  timing: %d chapter files, %d entries, %d characters; a full pass %.2f s (store.py's own %.2f s), a pass with no change %.2f s (%.2f s)"
              % (len(chapters), stored[0], stored[1], full, first["seconds"], still, second["seconds"]))
        self.assertEqual(first["snapshot"]["loaded"]["docs"], len(chapters))
        self.assertEqual((second["snapshot"]["loaded"].get("docs", 0), second["versions"]["added"]), (0, 0))
        self.assertLess(full, 60)


if __name__ == "__main__":
    unittest.main()
