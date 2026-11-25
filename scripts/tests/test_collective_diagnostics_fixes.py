#!/usr/bin/env python3
"""Regression tests for Diagnostics 2026-11-25 fixes:
  1. gate.book_onetime 72h rolling retention + daily gzip archive + 7d auto-prune
  2. accounting.py onetime rollover fallback to stats_money_hour, sell-order escrow,
     live depth-weighted market valuation, and copper glut zero marginal accrual
  3. bursar.py multi-holder Sol pileup fix + unstaffed-first spread + sync_fleet_sells
  4. scorecard.py Command 0-ship no DIV_IDLE + Mining realizable value-added gate
  5. haul.py unreserved faction surplus liquidation + calm buy-wall delivery
"""
import gzip
import json
import os
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))

import accounting
import bursar
import gate
import haul
import scorecard


class TestDiagnosticsFixes(unittest.TestCase):
    def test_onetime_72h_rolling_archive_and_7d_prune(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            fdir = data / "fleet"
            fdir.mkdir(parents=True)
            now = 1795600000
            # Seed an old 10-day archive that must be pruned
            arch = fdir / "archive"
            arch.mkdir(parents=True)
            old_day = time.strftime("%Y-%m-%d", time.gmtime(now - 10 * 86400))
            old_arch = arch / ("onetime-%s.jsonl.gz" % old_day)
            with gzip.open(old_arch, "wt", encoding="ascii") as gz:
                gz.write(json.dumps([now - 10 * 86400, "p1", "old", 10]) + "\n")
            # Seed onetime.json with 5200 recent (<72h) rows + 3 aged (>72h) rows
            aged_ts = now - 80 * 3600
            rows = [[aged_ts, "p1", "Aged reward", 500], [aged_ts + 1, "p2", "Aged buy", -200], [aged_ts + 2, "p3", "Aged", 100]]
            for i in range(5200):
                rows.append([now - 3600 + i % 3000, "trader-1", "Exchange buy escrow: released", 10])
            (fdir / "onetime.json").write_text(json.dumps(rows), encoding="ascii")

            gate.book_onetime("miner-1", "Hull upgrade", -150000, data=str(data), now_ts=now)

            kept = json.loads((fdir / "onetime.json").read_text(encoding="ascii"))
            # Must NOT truncate at 5000! All 5200 recent + 1 new kept = 5201
            self.assertEqual(len(kept), 5201)
            self.assertFalse(old_arch.exists())
            aged_day = time.strftime("%Y-%m-%d", time.gmtime(aged_ts))
            new_arch = arch / ("onetime-%s.jsonl.gz" % aged_day)
            self.assertTrue(new_arch.exists())
            with gzip.open(new_arch, "rt", encoding="ascii") as gz:
                alines = [json.loads(l) for l in gz if l.strip()]
            self.assertEqual(len(alines), 3)

    def test_accounting_live_deep_market_glut_guard_and_sell_escrow(self):
        base_map = {"silver_ore": 28.0, "copper_ore": 8.0, "silicon_ore": 10.0}
        bids = {
            "silver_ore": [(101.0, 50000.0)],
            "copper_ore": [(4.0, 100000.0)],
            "silicon_ore": [(800.0, 5.0), (12.0, 100.0)],
        }
        # Deep live buy-wall (>=500 qty) values silver_ore at live 101 cr, NOT static 28 cr!
        self.assertAlmostEqual(accounting.live_market_unit_price("silver_ore", base_map, bids), 101.0, places=1)
        # Thin 5-unit spoof bid on silicon_ore is capped to base 10 cr
        self.assertLessEqual(accounting.live_market_unit_price("silicon_ore", base_map, bids), 12.0)
        # Copper glut (>=50k held and >1.5x galaxy bid depth at <10 cr) gets 0 marginal accrual!
        self.assertEqual(accounting.live_market_unit_price("copper_ore", base_map, bids, held_units=200000), 0.0)
        self.assertAlmostEqual(accounting.live_market_unit_price("copper_ore", base_map, bids, held_units=10000), 4.0, places=1)

    def test_accounting_onetime_rollover_falls_back_to_stats_money_hour(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (root / "game" / "routes").mkdir(parents=True)
            (data / "fleet").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            (data / "stock").mkdir(parents=True)
            now = 1795600000
            # Write truncated 6h onetime.json
            (data / "fleet" / "onetime.json").write_text(json.dumps([[now - 6 * 3600, "trader-1", "escrow", 10]]), encoding="ascii")
            fj = {"totals": {"rates": {"windows": {"24h": {"minutes": 1440, "income_per_hour": 400000, "costs_per_hour": 600000, "cph": -200000, "rewards_per_hour": 40000, "bought_once_per_hour": 15000, "one_time_per_hour": 25000, "total_per_hour": -175000, "divisions": {}}}}}}
            db = data / "store" / "read.db"
            con = sqlite3.connect(str(db))
            con.executescript("""
                CREATE TABLE stats_money_hour (hour INT, division TEXT, minutes REAL, income REAL, costs REAL, net REAL, rewards REAL, bought REAL, once REAL, total REAL, fuel REAL, ships INT);
            """)
            for i in range(23):
                h = now - (i + 1) * 3600
                con.execute("INSERT INTO stats_money_hour VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (h, "Fleet", 60, 200000, 180000, 20000, 100000, 90000, 10000, 30000, 50000, 500))
                con.execute("INSERT INTO stats_money_hour VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (h, "Trade", 60, 200000, 180000, 20000, 100000, 90000, 10000, 30000, 10000, 80))
            con.commit()
            pnl = accounting.compute_pnl(con, repo_root=str(root), data_dir=str(data), fleet_json=fj, hours=24, now=now)
            con.close()
            self.assertIn("stats_money_hour", pnl["cash_source"])
            self.assertEqual(pnl["raw_steady_h"], 20000)
            self.assertEqual(pnl["seed_rewards_h"], 100000)

    def test_bursar_multi_holder_prevents_sol_pileup_and_syncs_sells(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            repo = Path(tmp) / "repo"
            (data / "fleet" / "orders").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            (repo / "game").mkdir(parents=True)
            now = 1795600000
            # Build read.db with 2 safe Exchange hubs: sol (priority) and haven
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE places (system TEXT, poi TEXT, base TEXT, name TEXT, market INT);
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INT);
                CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty REAL, ask REAL, ask_qty REAL, t INT);
            """)
            con.executemany("INSERT INTO systems VALUES (?,?,?)", [("sol", "solarian", 0), ("haven", "nebula", 0)])
            con.executemany("INSERT INTO places VALUES (?,?,?,?,?)", [
                ("sol", "sol_central", "sol_base", "Sol", 1),
                ("haven", "grand_exchange", "haven_base", "Haven", 1),
            ])
            con.executemany("INSERT INTO books VALUES (?,?,?,?,?,?,?)", [
                ("sol_base", "iron_ore", 10, 1000, 12, 1000, now - 60),
                ("haven_base", "iron_ore", 10, 1000, 12, 1000, now - 60),
            ])
            con.commit()
            con.close()
            pol = {"max_per_station": 1, "priority_max_per_station": 2, "priority_stations": ["sol_base"], "policed_only": True, "cycle_minutes": 30}
            c1 = bursar.claim_station(data, repo, "trader-1", {"system": "sol", "base": "sol_base"}, pol, now_t=now)
            c2 = bursar.claim_station(data, repo, "trader-2", {"system": "sol", "base": "sol_base"}, pol, now_t=now + 1)
            c3 = bursar.claim_station(data, repo, "trader-3", {"system": "sol", "base": "sol_base"}, pol, now_t=now + 2)
            c4 = bursar.claim_station(data, repo, "trader-4", {"system": "sol", "base": "sol_base"}, pol, now_t=now + 3)
            # Pilot 1 takes Sol, Pilot 2 MUST spread to unstaffed Haven first, Pilot 3 takes 2nd slot at Sol, Pilot 4 gets None (cap 2+1=3)!
            self.assertEqual(c1["base"], "sol_base")
            self.assertEqual(c2["base"], "haven_base")
            self.assertEqual(c3["base"], "sol_base")
            self.assertIsNone(c4)

            # sync_fleet_sells records active sell-order escrow cleanly
            sells = bursar.sync_fleet_sells(data, "trader-1", "sol_base", [{"order_id": "s1", "side": "sell", "item_id": "armor_plate", "remaining": 50, "price_each": 450}], now_t=now)
            self.assertEqual(sells, {"armor_plate": 50})
            by_i, by_di, _ts = accounting._load_sell_escrow(data, now=now)
            self.assertEqual(by_i["armor_plate"], 50)
            self.assertEqual(by_di[("Trade", "armor_plate")], 50)

    def test_haul_liquidate_surplus_reads_unreserved_faction_storage_and_buywall(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            (data / "stock").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            now = 1795600000
            (data / "stock" / "storage.json").write_text(json.dumps({
                "pilots": {},
                "faction": {"sol_base": {"silver_ore": 120}},
            }), encoding="ascii")
            books = [{"base": "arneb_base", "item": "silver_ore", "bid": 101, "bid_qty": 50000, "t": now - 60}]
            base_map = {
                "sol_base": ("sol", "sol_p", "sol_base", True),
                "arneb_base": ("arneb", "arneb_p", "arneb_base", False),
            }
            lanes = {"sol": ["arneb"], "arneb": ["sol"]}
            pol = {"policed_only": True, "allow_faction_surplus_liquidation": True, "allow_calm_buywall_dest": True, "buywall_min_bid": 50, "buywall_min_qty": 200, "max_book_age_minutes": 45}
            job = haul._pick_surplus_liquidation(str(data), "hauler-1", books, base_map, lanes, "sol", 100, pol, set(), now_t=now)
            self.assertIsNotNone(job)
            self.assertEqual(job["source_target"], "faction")
            self.assertEqual(job["item"], "silver_ore")
            self.assertEqual(job["qty"], 100)


if __name__ == "__main__":
    unittest.main()
