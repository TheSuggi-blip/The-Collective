#!/usr/bin/env python3
"""Unit tests for progression.py, governance blueprint docs indexing, collective_mcp view=progression, and /api/progression."""

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))
sys.path.insert(0, str(REPO / "station"))

import collective_mcp                             # noqa: E402
import docs                                       # noqa: E402
import progression                                # noqa: E402
import server                                     # noqa: E402
import store                                      # noqa: E402


class ProgressionAndBlueprintTests(unittest.TestCase):
    def test_docs_kinds_indexes_all_governance_blueprints_and_protocol(self):
        patterns = [(k, p) for k, p, _o in docs.KINDS]
        self.assertIn(("blueprint", "governance/knowledge-and-memory-loop.md"), patterns)
        self.assertIn(("blueprint", "governance/progression-roadmap.md"), patterns)
        self.assertIn(("blueprint", "communications/protocol.md"), patterns)
        with tempfile.TemporaryDirectory(prefix="bp-docs-") as tmp:
            repo = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (repo / "governance").mkdir(parents=True)
            (repo / "communications").mkdir(parents=True)
            (repo / "governance" / "knowledge-and-memory-loop.md").write_text("# Blueprint\n\n## 1. Anchor\n\nClean.\n", encoding="ascii")
            (repo / "governance" / "progression-roadmap.md").write_text("# Roadmap\n\n## 1. Horizons\n\nForward.\n", encoding="ascii")
            (repo / "communications" / "protocol.md").write_text("# Protocol\n\n## Format\n\nAppend-only.\n", encoding="ascii")
            store.one_pass(str(data), now=1795380000.0, root=str(repo / "game"))
            conn = sqlite3.connect(str(data / "store" / "read.db"))
            try:
                paths = sorted(r[0] for r in conn.execute("SELECT DISTINCT path FROM docs WHERE kind = 'blueprint'"))
                self.assertEqual(paths, [
                    "communications/protocol.md",
                    "governance/knowledge-and-memory-loop.md",
                    "governance/progression-roadmap.md",
                ])
            finally:
                conn.close()

    def test_progression_compute_and_write_roadmap_markers(self):
        with tempfile.TemporaryDirectory(prefix="prog-test-") as tmp:
            repo = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (repo / "governance").mkdir(parents=True)
            (data / "catalog").mkdir(parents=True)
            roadmap = repo / "governance" / "progression-roadmap.md"
            roadmap.write_text("# Roadmap\n\n" + progression.BEGIN_MARK + "\n" + progression.END_MARK + "\n", encoding="ascii")
            store.one_pass(str(data), now=1795380000.0, root=str(repo / "game"))
            st = progression.write_roadmap(str(repo), data=str(data), commit=False, now=1795380000.0)
            self.assertEqual(st, "written")
            txt = roadmap.read_text(encoding="ascii")
            self.assertIn("### Strategic Rung Progress Across Horizons", txt)
            self.assertIn("2026-11-14", txt)

    def test_mcp_and_station_api_progression(self):
        plan = collective_mcp.TOOLS["fleet"]["plan"]({"view": "progression"})
        self.assertEqual(plan, [("game/fleet/hive.py", ["progression"])])
        with tempfile.TemporaryDirectory(prefix="prog-srv-") as tmp:
            unit = Path(tmp) / "data"
            st_sub = unit / "station"
            st_sub.mkdir(parents=True)
            store.one_pass(str(unit), now=1795380000.0, root=str(REPO / "game"))
            old_data, old_cache = server.DATA, dict(server.PROGRESSION_CACHE)
            try:
                server.DATA = st_sub
                server.PROGRESSION_CACHE["at"] = 0.0
                server.PROGRESSION_CACHE["data"] = None
                res = server.api_progression()
                self.assertEqual(len(res["rungs"]), 12)
                self.assertGreaterEqual(len(res["milestones"]), 7)
            finally:
                server.DATA = old_data
                server.PROGRESSION_CACHE.update(old_cache)


if __name__ == "__main__":
    unittest.main()
