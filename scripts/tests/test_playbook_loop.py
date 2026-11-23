#!/usr/bin/env python3
"""Unit tests for the Anchor-and-Delta Division Playbook, High-Watermark Curation & Empirical Drift Loop."""

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))
sys.path.insert(0, str(REPO / "station"))

import guidebook as book                          # noqa: E402
import playbook_anchor                            # noqa: E402
import store                                      # noqa: E402


class PlaybookLoopTests(unittest.TestCase):
    def test_high_watermark_and_drift_scanner_detect_near_cap_stale_test_and_archived_route(self):
        with tempfile.TemporaryDirectory(prefix="pb-loop-") as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (root / "game" / "routes").mkdir(parents=True)
            (data / "catalog").mkdir(parents=True)
            (data / "routes" / "archive").mkdir(parents=True)
            (data / "catalog" / "0.732.3.json").write_text("{}", encoding="ascii")
            for i in range(6):
                (root / "game" / "routes" / ("mine-live-%d.json" % i)).write_text('{"kind":"mine","status":"open"}', encoding="ascii")
            (root / "game" / "routes" / "mine-disabled-one.json").write_text('{"kind":"mine","status":"off"}', encoding="ascii")
            (data / "routes" / "archive" / "mine-gone-old.json").write_text('{"kind":"mine"}', encoding="ascii")

            gdir = root / "game" / "routes" / "guidebook" / "mining"
            gdir.mkdir(parents=True)
            (gdir / "card.md").write_text(
                "# Mining guidebook -- the Class Card (card.md)\n\n"
                "### Ships\n"
                "Status: proven. Updated: 2026-11-20. Evidence: table hulls (catalog 0.723.2); route mine-gone-old.\n\n"
                + ("A" * 4050) + "\n",
                encoding="ascii",
            )
            (gdir / "tests.md").write_text(
                "# Mining guidebook -- Tests (tests.md)\n\n"
                "### Old belt trial\n"
                "Status: test. Updated: 2026-11-10. Evidence: route mine-disabled-one.\n\n"
                "Testing belt yield.\n",
                encoding="ascii",
            )
            for ch in ("ships", "levelling", "routes", "lessons"):
                (gdir / (ch + ".md")).write_text(
                    "# Mining guidebook -- %s (%s.md)\n\n### Rule\nStatus: proven. Updated: 2026-11-22. Evidence: live.\n\nBody.\n" % (ch, ch),
                    encoding="ascii",
                )

            now_ts = 1795377600.0  # 2026-11-22T20:00:00Z
            cur = playbook_anchor.scan_division_curation(str(root), "mining", data=str(data), now=now_ts)
            self.assertEqual(cur["near_count"], 1)
            kinds = {w["kind"] for w in cur["drift_warnings"]}
            self.assertIn("stale_catalog_ref", kinds)
            self.assertIn("archived_route", kinds)
            self.assertIn("stale_test", kinds)
            self.assertIn("disabled_route", kinds)

    def test_division_playbooks_sql_view_and_anchor_computation(self):
        with tempfile.TemporaryDirectory(prefix="pb-sql-") as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (root / "game" / "routes" / "guidebook" / "mining").mkdir(parents=True)
            for ch in book.CHAPTERS:
                (root / "game" / "routes" / "guidebook" / "mining" / (ch + ".md")).write_text(
                    "# Mining -- %s\n\n### Entry\nStatus: proven. Updated: 2026-11-22. Evidence: live.\n\nKeep lean.\n" % ch,
                    encoding="ascii",
                )
            store.one_pass(str(data), now=1795377600.0, root=str(root / "game"))
            conn = sqlite3.connect(str(data / "store" / "read.db"))
            try:
                rows = conn.execute("SELECT division, guide_chapters, guide_entries FROM division_playbooks ORDER BY division").fetchall()
                by_div = {r[0]: (r[1], r[2]) for r in rows}
                self.assertEqual(len(by_div), 6)
                self.assertEqual(by_div["mining"], (6, 6))
                anc = playbook_anchor.compute_division_anchor(conn, str(root), data=str(data), division_name="mining", now=1795377600.0)
                self.assertEqual(anc["division"], "mining")
                self.assertEqual(anc["member"], "Zero")
                self.assertEqual(len(anc["curation"]["chapters"]), 6)
            finally:
                conn.close()

    def test_precommit_has_guidebook_needs_and_comms_gates(self):
        pc = (REPO / ".githooks" / "pre-commit").read_text(encoding="ascii")
        self.assertIn("scripts/guide.py check", pc)
        self.assertIn("game/fleet/needs.py check", pc)
        self.assertIn("scripts/comms.py check", pc)



    def test_station_api_playbooks_uses_unit_data_parent_not_station_subdir(self):
        import server
        with tempfile.TemporaryDirectory(prefix="pb-srv-") as tmp:
            unit = Path(tmp) / "data"
            station_sub = unit / "station"
            station_sub.mkdir(parents=True)
            (unit / "catalog").mkdir(parents=True)
            (unit / "catalog" / "0.732.3.json").write_text("{}", encoding="ascii")
            store.one_pass(str(unit), now=1795377600.0, root=str(REPO / "game"))
            conn = sqlite3.connect(str(unit / "store" / "read.db"))
            try:
                conn.execute("INSERT INTO ships (pilot, member, division, role, number, class, docked, flies, t, src) VALUES ('m-1', 'Zero', 'Mining', 'miner', 1, 'Threshold', 0, 'mine-x', 1, 't')")
                conn.commit()
            finally:
                conn.close()
            old_data, old_cache = server.DATA, dict(server.PLAYBOOKS_CACHE)
            try:
                server.DATA = station_sub
                server.PLAYBOOKS_CACHE["at"] = 0.0
                server.PLAYBOOKS_CACHE["data"] = None
                res = server.api_playbooks()
                mining = next(d for d in res["divisions"] if d["division"] == "mining")
                self.assertEqual(mining["fleet"]["ships_total"], 1)
                self.assertEqual(mining["catalog_version"], "0.732.3")
            finally:
                server.DATA = old_data
                server.PLAYBOOKS_CACHE.update(old_cache)


    def test_multi_empire_anchor_surfaces_all_active_division_empires_and_hulls(self):
        with tempfile.TemporaryDirectory(prefix="pb-multi-") as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (root / "game" / "routes" / "guidebook" / "mining").mkdir(parents=True)
            for ch in book.CHAPTERS:
                (root / "game" / "routes" / "guidebook" / "mining" / (ch + ".md")).write_text(
                    "# Mining -- %s\n\n### Entry\nStatus: proven. Updated: 2026-11-23. Evidence: live.\n\nBody.\n" % ch,
                    encoding="ascii",
                )
            store.one_pass(str(data), now=1795377600.0, root=str(root / "game"))
            conn = sqlite3.connect(str(data / "store" / "read.db"))
            try:
                conn.executemany(
                    "INSERT INTO ships (pilot, member, division, role, number, class, empire, docked, flies, t, src) VALUES (?, 'Zero', 'Mining', 'miner', ?, ?, ?, 0, 'mine-x', 1, 't')",
                    [
                        ("miner-1", 1, "Threshold", "voidborn"),
                        ("miner-61", 61, "Theoria", "solarian"),
                        ("miner-96", 96, "Prospect", "nebula"),
                    ],
                )
                conn.executemany(
                    "INSERT INTO hulls (id, name, category, class, tier, faction, cargo, fuel, weapon_slots, defense_slots, utility_slots, cpu, power, piloting_required, src) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 't')",
                    [
                        ("threshold", "Threshold", "Civilian", "Starter", 0, "voidborn", 65, 95, 1, 2, 2, 16, 30, 0),
                        ("theoria", "Theoria", "Civilian", "Starter", 0, "solarian", 70, 100, 1, 1, 3, 16, 28, 0),
                        ("prospect", "Prospect", "Civilian", "Starter", 0, "nebula", 100, 130, 1, 1, 2, 13, 26, 0),
                        ("liminal", "Liminal", "Industrial", "Miner", 1, "voidborn", 75, 100, 0, 2, 3, 18, 34, 0),
                        ("archimedes", "Archimedes", "Industrial", "Miner", 1, "solarian", 80, 100, 1, 1, 4, 18, 34, 0),
                        ("bonanza", "Bonanza", "Industrial", "Miner", 1, "nebula", 180, 130, 0, 1, 3, 12, 24, 0),
                    ],
                )
                conn.commit()
                anc = playbook_anchor.compute_division_anchor(conn, str(root), data=str(data), division_name="mining", now=1795377600.0)
                emps = {e["empire"] for e in anc["fleet"]["empires"]}
                self.assertEqual(emps, {"voidborn", "solarian", "nebula"})
                unlock_names = {u["name"] for u in anc["fleet"]["next_unlocks"]}
                self.assertTrue({"Liminal", "Archimedes", "Bonanza"}.issubset(unlock_names))
                lines_txt = "\n".join(playbook_anchor.anchor_lines(anc))
                self.assertIn("solarian", lines_txt)
                self.assertIn("Bonanza", lines_txt)
                self.assertIn("Archimedes", lines_txt)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
