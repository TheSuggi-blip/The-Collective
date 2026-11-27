"""Unit tests for kpi_engine.py dynamic upgrade gaps, 17-wing KPIs, and closed-loop signals."""
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))

import kpi_engine


class TestDynamicUpgradeGaps(unittest.TestCase):
    def test_hulls_scale_dynamically_with_piloting_and_exclude_staged_6b(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            db = d / "test.db"
            con = sqlite3.connect(str(db))
            con.execute("CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INT)")
            con.execute("CREATE TABLE hulls (id TEXT, name TEXT, tier INT, weapon_slots INT, defense_slots INT, utility_slots INT)")
            con.execute("CREATE TABLE ships (pilot TEXT, class TEXT)")
            con.execute("CREATE TABLE ship_modules (pilot TEXT, module TEXT, name TEXT, slot TEXT, kind TEXT)")
            con.executemany("INSERT INTO hulls VALUES (?, ?, ?, ?, ?, ?)", [
                ("prospect", "Prospect", 0, 1, 1, 1),
                ("archimedes", "Archimedes", 1, 0, 1, 2),
                ("resonance_miner", "Resonance Miner", 2, 0, 2, 3),
                ("congregation", "Congregation", 1, 0, 1, 1),
            ])
            # Pilot 1: 3A T0 with P5 (max possible T1 -> missing 1)
            # Pilot 2: 3A T1 with P12 (max possible T2 -> missing 1)
            # Pilot 3: 3A T2 with P25 (max possible T3 -> missing 1!)
            # Pilot 4: 4C T1 with P40 (Bursar ladder caps at T1 -> missing 0! Exempt from modules!)
            # Pilot 5: 6B T0 with P5 (staged/disabled in upgrade-policy.json -> counted as staged)
            con.executemany("INSERT INTO ship_skills VALUES (?, 'piloting', ?)", [
                ("EUV One", 5), ("EUV Two", 12), ("EUV Three", 25), ("MCV Desk", 40), ("LSV Pax", 5),
            ])
            con.executemany("INSERT INTO ships VALUES (?, ?)", [
                ("EUV One", "prospect"), ("EUV Two", "archimedes"), ("EUV Three", "resonance_miner"),
                ("MCV Desk", "congregation"), ("LSV Pax", "prospect"),
            ])
            con.execute("INSERT INTO ship_modules VALUES ('EUV Two', 'mining_laser_ii', 'Mining Laser II', 'utility', 'utility')")
            con.commit()

            ships = [
                {"name": "EUV One", "division": "Mining", "wing": "3A. Ore -- Precision", "class": "prospect", "piloting": 5},
                {"name": "EUV Two", "division": "Mining", "wing": "3A. Ore -- Precision", "class": "archimedes", "piloting": 12},
                {"name": "EUV Three", "division": "Mining", "wing": "3A. Ore -- Precision", "class": "resonance_miner", "piloting": 25},
                {"name": "MCV Desk", "division": "Trade", "wing": "4C. Pure Bursar Desks", "class": "congregation", "piloting": 40},
                {"name": "LSV Pax", "division": "Logistics", "wing": "6B. Passenger & Resort Liners", "class": "prospect", "piloting": 5},
            ]
            gaps = kpi_engine.compute_upgrade_gaps(con, ships, REPO, d)
            con.close()

            h = gaps["hulls"]
            self.assertEqual(h["active_ships"], 4)
            self.assertEqual(h["staged_ships"], 1)
            # Possible steps: 1 + 2 + 3 + 1 = 7; filled: 0 + 1 + 2 + 1 = 4; missing = 3 (T1:1, T2:1, T3:1)
            self.assertEqual(h["possible_steps"], 7)
            self.assertEqual(h["filled_steps"], 4)
            self.assertEqual(h["missing_steps"], 3)
            self.assertEqual(h["ships_missing"], 3)
            self.assertEqual(h["missing_by_tier"], {"T1": 1, "T2": 1, "T3": 1})

            m = gaps["modules"]
            self.assertEqual(m["bursar_exempt_ships"], 1)
            self.assertEqual(m["staged_ships"], 1)
            self.assertEqual(m["active_ships"], 3)
            self.assertGreater(m["possible_slots"], 0)
            self.assertEqual(m["filled_slots"], 1)


class TestWingMappingAndSignals(unittest.TestCase):
    def test_all_17_wing_prefixes_map_distinctly(self):
        samples = [
            ("1A-Prime. Task Force Prime (10) -- Command", "Military", "1A-1C"),
            ("1B. Grand Battle Line", "Military", "1A-1C"),
            ("1C. Outpost Sentinels (Medics)", "Military", "1A-1C"),
            ("2A. Heavy Pirate Hunters", "Military", "2A-2B"),
            ("2B. Fast Wildlife & Raiders", "Military", "2A-2B"),
            ("3A. Ore -- Precision", "Mining", "3A"),
            ("3B. Ore -- Bulk", "Mining", "3B"),
            ("3C. Deep-Core & Rad", "Mining", "3C"),
            ("3D. Gas Harvesters", "Mining", "3D"),
            ("3E. Ice Harvesters", "Mining", "3E"),
            ("4A. Express Arbitrage", "Trade", "4A"),
            ("4B. Bulk Trade Haulers", "Trade", "4B"),
            ("4C. Pure Bursar Desks", "Trade", "4C"),
            ("5A. Station Refiners & Bursars", "Trade", "5A"),
            ("5B. Mobile Field Workshops", "Trade", "5B"),
            ("6A. Supply Chain Bulk Haulers", "Logistics", "6A"),
            ("6B. Passenger & Resort Liners", "Logistics", "6B"),
            ("6C. Combat Salvage Tenders", "Logistics", "6C"),
            ("6C. Fleet Fuel Tankers", "Logistics", "6C"),
            ("7A. Covert Recon", "Intel", "7A"),
            ("7B. Deep-Core Surveyors", "Intel", "7B"),
        ]
        for lbl, div, exp in samples:
            self.assertEqual(kpi_engine.wing_id_of(lbl, div), exp)

    def test_signal_publish_and_read(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            kpi_engine._LAST_SIGNAL_WRITE = 0.0
            snap = {
                "upgrades": {"hulls": {"by_wing": {"3A": {"pct_done": 20.0}}}},
                "infra": {"bunker_avg_pct": 80.0, "low_bunker_bases": ["b1"], "supply_sla_pct": 70.0},
                "windows": {"6h": {
                    "fleet": {"core_ebit_h": 12000, "rev_per_fuel": 1.9, "idle_pct": 2.5, "galaxy_median_min": 14.0, "bursar_stations_occupied": 42},
                    "wings": [
                        {"id": "3A", "health_pct": 65.0, "rof": 1.1, "staged": False},
                        {"id": "6B", "health_pct": 40.0, "rof": 0.4, "staged": True},
                    ],
                }},
            }
            kpi_engine.publish_kpi_signals(d, snap, now=time.time())
            sig = kpi_engine.read_kpi_signals(d)
            self.assertEqual(sig["tighten_fuel_wings"], ["3A"])
            self.assertNotIn("6B", sig["tighten_fuel_wings"])
            self.assertTrue(sig["boost_upkeep_urgency"])
            self.assertEqual(sig["low_bunker_bases"], ["b1"])
            self.assertIn("3A", sig["priority_upgrade_wings"])


if __name__ == "__main__":
    unittest.main()
