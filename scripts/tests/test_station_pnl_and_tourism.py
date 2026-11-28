import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import store
import collective_mcp
import station_pnl


class TestTourismSnapshotsAndStationPnl(unittest.TestCase):
    def test_read_leaderboards_persists_hourly_tourism_snapshots(self):
        with tempfile.TemporaryDirectory() as td:
            st_dir = Path(td) / "station"
            st_dir.mkdir(parents=True)
            lb_p = st_dir / "leaderboard.json"
            payload1 = {
                "generated_at": "2026-11-28T01:10:00Z",
                "stations": {
                    "tourism_revenue": [
                        {"rank": 1, "name": "The Obsidian Well", "system_name": "Arneb", "value": 250000000},
                        {"rank": 2, "name": "Hex Star", "system_name": "Dheneb", "value": 220000000},
                    ],
                    "tourism_appeal": [
                        {"rank": 1, "name": "Hex Star", "system_name": "Dheneb", "value": 54},
                    ],
                },
            }
            lb_p.write_text(json.dumps(payload1), encoding="ascii")
            out1 = store.read_leaderboards(lb_p, {})
            self.assertEqual(len(out1["tourism_snapshots"]), 3)
            self.assertTrue((st_dir / "tourism_history.jsonl").exists())

            payload2 = json.loads(json.dumps(payload1))
            payload2["generated_at"] = "2026-11-28T02:10:00Z"
            payload2["stations"]["tourism_revenue"][0]["value"] = 250350000
            lb_p.write_text(json.dumps(payload2), encoding="ascii")
            out2 = store.read_leaderboards(lb_p, {})
            self.assertEqual(len(out2["tourism_snapshots"]), 6)

    def test_collective_mcp_registers_station_pnl_and_station_build(self):
        self.assertIn("station_pnl", collective_mcp.TOOLS)
        self.assertIn("station_build", collective_mcp.TOOLS)
        self.assertNotIn("station_pnl", collective_mcp.WRITES)
        self.assertIn("station_build", collective_mcp.WRITES)
        sch_r = collective_mcp.schema("station_pnl")
        sch_w = collective_mcp.schema("station_build")
        self.assertTrue(sch_r["annotations"]["readOnlyHint"])
        self.assertFalse(sch_w["annotations"]["readOnlyHint"])
        self.assertTrue(sch_w["annotations"]["destructiveHint"])

    def test_station_pnl_format_runs_on_minimal_db(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "store").mkdir()
            db = sqlite3.connect(str(d / "store" / "read.db"))
            db.executescript("""
                CREATE TABLE books (item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER);
                CREATE TABLE fair_prices (item TEXT, fair_price REAL);
                CREATE TABLE faction_facilities (type TEXT, name TEXT, base TEXT, status TEXT, rent_per_cycle INTEGER);
                CREATE TABLE bases (base TEXT, name TEXT, system TEXT, kind TEXT);
                CREATE TABLE faction_storage (base TEXT, item TEXT, units INTEGER);
                CREATE TABLE leaderboards (grp TEXT, board TEXT, rank INTEGER, name TEXT, tag TEXT, value INTEGER);
                CREATE TABLE faction (treasury INTEGER, member_count INTEGER, members_limit INTEGER);
                CREATE TABLE facilities (id TEXT, name TEXT, build_cost INTEGER, upgrades_from TEXT, faction_cap INTEGER);
                CREATE TABLE facility_materials (facility TEXT, item TEXT, units INTEGER);
                CREATE TABLE tourism_snapshots (bucket_h INTEGER, station TEXT, system TEXT, board TEXT, rank INTEGER, value INTEGER, t INTEGER);
                INSERT INTO faction VALUES (8500000, 300, 325);
                INSERT INTO bases VALUES ('b1', 'Collective Resort Ridgecrest', 'ridgecrest', 'station');
                INSERT INTO tourism_snapshots VALUES (100, 'The Obsidian Well', 'Arneb', 'tourism_revenue', 1, 250000000, 360000);
                INSERT INTO tourism_snapshots VALUES (102, 'The Obsidian Well', 'Arneb', 'tourism_revenue', 1, 250700000, 367200);
            """)
            db.commit()
            db.close()
            res = station_pnl.compute_station_pnl(data_dir=str(d))
            self.assertEqual(res["treasury_cr"], 8500000)
            self.assertEqual(res["rivals"][0]["cr_h"], 350000)
            txt = station_pnl.format_report(res, "all")
            self.assertIn("The Obsidian Well", txt)
            self.assertIn("+350,000 cr/h", txt)


if __name__ == "__main__":
    unittest.main()
