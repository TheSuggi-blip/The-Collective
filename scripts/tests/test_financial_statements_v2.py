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


    def test_in_transit_treasury_sweeps_prevent_liquid_cash_dip(self):
        import json
        con = sqlite3.connect(":memory:")
        con.executescript("CREATE TABLE ships (pilot TEXT, class TEXT, credits REAL); CREATE TABLE faction (treasury REAL);")
        con.execute("INSERT INTO ships VALUES ('trader-1', 'prospect', 100000)")
        con.execute("INSERT INTO faction VALUES (5000000)")
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            (tdp / "empire").mkdir()
            (tdp / "fleet").mkdir()
            (tdp / "empire" / "empire.json").write_text(json.dumps({
                "written_at": "2026-11-26T13:05:45Z",
                "faction": {"treasury": 5000000},
            }), encoding="ascii")
            # Sweep booked at 13:16:29Z (after 13:05:45Z treasury read!)
            import calendar, time as _t
            ts_after = calendar.timegm(_t.strptime("2026-11-26T13:16:29", "%Y-%m-%dT%H:%M:%S"))
            (tdp / "fleet" / "onetime.json").write_text(json.dumps([
                [ts_after - 1000, "trader-1", "Faction treasury: credits deposited (old)", -50000],
                [ts_after, "Prime Directive", "Faction treasury: credits deposited (the Collective keeps them)", -185840],
                [ts_after + 5, "Unity", "Treasury fund: credits withdrawn for top-up", 10000],
            ]), encoding="ascii")
            bs = accounting.compute_balance_sheet(con, data_dir=tdp)
            self.assertEqual(bs["treasury_in_transit"], 175840)
            self.assertEqual(bs["treasury"], 5175840)
            self.assertEqual(bs["liquid_cash"], 5275840)

    def test_revenue_breakdown_mission_buy_capex_exclusion_and_fuel_cap(self):
        import json, time as _t
        now_t = _t.time()
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            (tdp / "fleet").mkdir()
            (tdp / "fleet" / "onetime.json").write_text(json.dumps([
                [now_t - 600, "trader-20", "mission-diplomatic-pouch-sol: gold_ore bought", -1540],
                [now_t - 300, "drone-1", "Broadaxe hull bought from listing", -10000],
            ]), encoding="ascii")
            fj = {
                "ships": [],
                "totals": {
                    "rates": {
                        "windows": {
                            "1h": {
                                "minutes": 60,
                                "income_per_hour": 500000,
                                "costs_per_hour": 200000,
                                "cph": 300000,
                                "rewards_per_hour": 50000,
                                "bought_once_per_hour": 11540,
                                "treasury_own_per_hour": -5000,
                                "purse_per_hour": 333460,
                                "repair_cr_per_hour": 1000,
                                "unexplained_per_hour": 4000,
                                "fuel_cr_per_hour": 290000,  # inflated by free bunker refuels!
                                "divisions": {
                                    "Trade": {"income_per_hour": 300000, "cph": 280000, "one_time_per_hour": 0, "fuel_cr_per_hour": 20000},
                                    "Logistics": {"income_per_hour": 195000, "cph": 100000, "one_time_per_hour": 0, "fuel_cr_per_hour": 150000},
                                    "Military": {"income_per_hour": 5000, "cph": -80000, "one_time_per_hour": 0, "fuel_cr_per_hour": 120000},
                                },
                            }
                        }
                    }
                },
            }
            pnl = accounting.compute_pnl(None, repo_root=ROOT, data_dir=tdp, fleet_json=fj, hours=1, now=now_t)
            # 1. Mission ore buy (-1540) moved OUT of CapEx (-10000 only) and INTO Seed Net!
            self.assertEqual(pnl["capex_gross_h"], -10000)
            self.assertEqual(pnl["capex_net_h"], -10000)
            self.assertEqual(pnl["mission_buy_once_h"], -1540)
            self.assertEqual(pnl["seed_net_h"], 50000 - 1540)
            # 2. Inflated fuel_cr_per_hour (290k) capped at gross_direct - repair (204k - 1k = 203k),
            #    so passive_inflows_h stays true unexplained_per_hour (4000) instead of phantom 91k!
            self.assertEqual(pnl["passive_inflows_h"], 4000)
            self.assertEqual(pnl["opex_breakdown"]["fuel_h"], 203000)
            # 3. Revenue breakdown separates Trade, Logistics Freight, Other, and Passive Escrow cleanly
            rb = pnl["revenue_breakdown"]
            self.assertEqual(rb["trade_sales_h"], 300000)
            self.assertEqual(rb["freight_sales_h"], 195000)
            self.assertEqual(rb["other_sales_h"], 5000)
            self.assertEqual(rb["passive_escrow_h"], 4000)
            self.assertEqual(rb["trade_sales_h"] + rb["freight_sales_h"] + rb["other_sales_h"] + rb["passive_escrow_h"], 504000)




class BuyEscrowBalanceSheetTests(unittest.TestCase):
    def test_buy_escrow_booked_as_current_asset_on_balance_sheet(self):
        import json, time
        with tempfile.TemporaryDirectory() as td:
            fdir = Path(td) / "fleet"
            fdir.mkdir(parents=True)
            (fdir / "bursar_buys.json").write_text(json.dumps({
                "updated_at": int(time.time()),
                "entries": {
                    "trader-1": {
                        "central_nexus": {
                            "at": int(time.time()),
                            "items": {"fuel_cell": 200},
                            "orders": {"o1": {"item": "fuel_cell", "rem": 200, "price": 50}},
                        }
                    }
                },
            }), encoding="utf-8")
            cash_cr, ords, units, _ts = accounting._load_buy_escrow(td)
            self.assertEqual((cash_cr, ords, units), (10000, 1, 200))
            bs = accounting.compute_balance_sheet(conn=None, fleet_json={"ships": [{"name": "trader-1", "credits": 50000}]}, data_dir=td)
            self.assertEqual(bs["liquid_cash"], 50000)
            self.assertEqual(bs["buy_escrow_cash"], 10000)
            self.assertEqual(bs["total_cash_and_escrow"], 60000)
            self.assertEqual(bs["net_worth"], 60000)


if __name__ == "__main__":
    unittest.main()

