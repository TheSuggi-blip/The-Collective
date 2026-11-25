#!/usr/bin/env python3
"""Unit tests for Financial Statements v7.2 (OpEx subsections, dynamic Hulls/Modules Balance Sheet, Buffett ROIC)."""
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import accounting


class FinancialStatementsV2Tests(unittest.TestCase):
    def test_balance_sheet_exposes_dynamic_hulls_modules_and_hard_assets(self):
        con = sqlite3.connect(":memory:")
        con.executescript("""
            CREATE TABLE ships (pilot TEXT, class TEXT, credits REAL);
            CREATE TABLE hulls (id TEXT, name TEXT, tier INTEGER);
            CREATE TABLE hull_materials (hull TEXT, item TEXT, units INTEGER);
            CREATE TABLE ship_modules (pilot TEXT, name TEXT);
            CREATE TABLE items (id TEXT, name TEXT, base_value REAL);
            CREATE TABLE faction (treasury REAL);
            CREATE TABLE faction_facilities (type TEXT, status TEXT);
            CREATE TABLE facilities (id TEXT, build_cost REAL);
        """)
        con.execute("INSERT INTO faction VALUES (5000000)")
        con.executemany("INSERT INTO items VALUES (?, ?, ?)", [
            ("steel_plate", "Steel Plate", 100.0),
            ("mining_laser_ii", "Mining Laser II", 25000.0),
            ("shield_booster_ii", "Shield Booster II", 40000.0),
        ])
        con.execute("INSERT INTO hulls VALUES ('prospect', 'Prospect', 2)")
        con.execute("INSERT INTO hull_materials VALUES ('prospect', 'steel_plate', 1000)")  # 100k per hull
        con.executemany("INSERT INTO ships VALUES (?, ?, ?)", [
            ("miner-1", "prospect", 10000),
            ("miner-2", "prospect", 15000),
        ])
        con.executemany("INSERT INTO ship_modules VALUES (?, ?)", [
            ("miner-1", "Mining Laser II"),
            ("miner-2", "Shield Booster II"),
        ])
        con.execute("INSERT INTO facilities VALUES ('faction_lockbox', 200000)")
        con.execute("INSERT INTO faction_facilities VALUES ('faction_lockbox', 'active')")

        bs = accounting.compute_balance_sheet(con, data_dir=Path(tempfile.mkdtemp()))
        self.assertEqual(bs["fleet_hulls"], 200000)
        self.assertEqual(bs["fleet_modules"], 65000)
        self.assertEqual(bs["fleet_book"], 265000)
        self.assertEqual(bs["facility_invested"], 200000)
        self.assertEqual(bs["hard_assets"], 465000)
        self.assertEqual(bs["operating_invested_capital"], 465000 + bs["vault_live_market"])
        self.assertEqual(bs["net_worth"], bs["liquid_cash"] + bs["vault_live_market"] + bs["hard_assets"])

        # Upgrade miner-1 by fitting another module -> balance sheet updates dynamically!
        con.execute("INSERT INTO ship_modules VALUES ('miner-1', 'Shield Booster II')")
        bs2 = accounting.compute_balance_sheet(con, data_dir=Path(tempfile.mkdtemp()))
        self.assertEqual(bs2["fleet_modules"], 105000)
        self.assertEqual(bs2["hard_assets"], 505000)

    def test_opex_breakdown_reconciles_to_matched_direct_costs_zero_plugs(self):
        con = sqlite3.connect(":memory:")
        con.executescript("""
            CREATE TABLE stats_money_hour (
                hour INTEGER, division TEXT, minutes REAL, income REAL, costs REAL,
                net REAL, rewards REAL, bought REAL, once REAL, total REAL,
                wallets REAL, fuel REAL, repair REAL, ships INTEGER,
                wallets_end REAL, treasury REAL, idle REAL, samples INTEGER, t REAL
            );
            CREATE TABLE runs (pilot TEXT, route TEXT, kind TEXT, started TEXT, t REAL, minutes REAL, credits REAL, one_time REAL, readable INTEGER, row TEXT);
        """)
        import time
        now_t = time.time()
        hr = int(now_t // 3600) * 3600
        con.execute(
            "INSERT INTO stats_money_hour VALUES (?, 'ALL', 60, 200000, 120000, 80000, 10000, 0, 10000, 90000, 0, 65000, 3000, 500, 1000000, 5000000, 0, 10, ?)",
            (hr, now_t),
        )
        con.execute(
            "INSERT INTO stats_money_hour VALUES (?, 'Mining', 60, 0, 65000, -65000, 0, 0, 0, -65000, 0, 65000, 0, 130, 100000, 0, 0, 10, ?)",
            (hr, now_t),
        )
        con.execute(
            "INSERT INTO stats_money_hour VALUES (?, 'Trade', 60, 200000, 55000, 145000, 10000, 0, 10000, 155000, 0, 0, 3000, 85, 900000, 0, 0, 10, ?)",
            (hr, now_t),
        )
        con.execute(
            "INSERT INTO runs VALUES ('hauler-1', 'craft-steel-plate', 'craft', '2026-11-25T17:00:00Z', ?, 60, -20000, 0, 1, '{}')",
            (now_t - 600,),
        )
        with tempfile.TemporaryDirectory() as td:
            pnl = accounting.compute_pnl(con, repo_root=ROOT, data_dir=Path(td), fleet_json={}, hours=1, now=now_t)
        ob = pnl["opex_breakdown"]
        self.assertEqual(ob["fuel_h"], 65000)
        self.assertEqual(ob["repair_h"], 3000)
        self.assertEqual(ob["craft_inputs_h"], 20000)
        self.assertEqual(ob["other_cogs_h"], 32000)
        self.assertEqual(
            ob["fuel_h"] + ob["repair_h"] + ob["craft_inputs_h"] + ob["other_cogs_h"],
            ob["gross_direct_h"],
        )
        self.assertEqual(
            ob["gross_direct_h"] - ob["reclassified_once_h"],
            ob["matched_direct_h"],
        )


if __name__ == "__main__":
    unittest.main()

