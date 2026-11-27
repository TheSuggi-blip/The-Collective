#!/usr/bin/env python3
"""Regression tests for SQL fair_prices/clean_books/wing_kpis, MCP wings/income/market/docs, and wallet settle() CapEx resilience."""

import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import accounting
import collective_mcp
import docs as fleet_docs
import market_guard
import store
import wallet


class TestTrinitySqlMcpEbitUpgrades(unittest.TestCase):
    def test_market_guard_thin_bootstrap_haircut_and_spoof_risk(self):
        with tempfile.TemporaryDirectory() as td:
            now_t = time.time()
            vwm_map = {
                "spoof_item": {"vwm": 400000.0, "stations": 1, "total_qty": 1, "total_cash": 400000.0},
                "mid_thin": {"vwm": 100.0, "stations": 1, "total_qty": 15, "total_cash": 1500.0},
                "deep_multi": {"vwm": 50.0, "stations": 5, "total_qty": 500, "total_cash": 25000.0},
            }
            res = market_guard.update_price_oracle(td, vwm_map, now_t=now_t, min_write_interval_s=0)
            self.assertEqual(res["spoof_item"]["spoof_risk"], "THIN")
            self.assertEqual(res["spoof_item"]["twap"], 200000.0)
            self.assertLessEqual(res["spoof_item"]["fair_price"], 270000.0)
            self.assertEqual(res["mid_thin"]["spoof_risk"], "SINGLE_HUB")
            self.assertEqual(res["mid_thin"]["twap"], 75.0)
            self.assertEqual(res["deep_multi"]["spoof_risk"], "LOW")
            self.assertEqual(res["deep_multi"]["fair_price"], 50.0)

    def test_store_materializes_fair_prices_clean_books_and_wing_kpis(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "fleet").mkdir(parents=True)
            (data / "market").mkdir(parents=True)
            now_t = int(time.time())
            (data / "fleet" / "price_oracle.json").write_text(json.dumps({
                "updated_at": now_t,
                "items": {
                    "iron_ore": {"fair_price": 10.0, "twap": 10.0, "vwm": 10.0, "stations": 6, "total_qty": 5000, "total_cash": 50000.0, "spoof_risk": "LOW", "t": now_t},
                },
            }), encoding="ascii")
            (data / "fleet" / "kpi_snapshot.json").write_text(json.dumps({
                "updated_at": now_t,
                "windows": {
                    "6h": {
                        "wings": [{
                            "id": "3A", "name": "Ore Precision", "division": "Mining", "pillar": "Extraction",
                            "responsibility_center": "Ore", "ships": 38, "working": 37, "idle": 1, "idle_pct": 2.6,
                            "fuel_h": 1200.0, "rof": 5.5, "health_pct": 92.0, "status": "OK", "staged": False,
                            "kpis": [{"k": "Ore / h", "v": "+10k", "score": 95}],
                        }],
                    },
                },
            }), encoding="ascii")
            conn = sqlite3.connect(":memory:")
            conn.executescript(store.snapshot_schema())
            fp_rows = store.read_fair_prices(data / "fleet" / "price_oracle.json", {})["fair_prices"]
            wk_rows = store.read_wing_kpis(data / "fleet" / "kpi_snapshot.json", {})["wing_kpis"]
            self.assertEqual(len(fp_rows), 1)
            self.assertEqual(len(wk_rows), 1)
            conn.execute(
                "INSERT INTO fair_prices (item, fair_price, twap, vwm, stations, total_qty, total_cash, spoof_risk, t, src) VALUES (?,?,?,?,?,?,?,?,?,?)",
                ("iron_ore", 10.0, 10.0, 10.0, 6, 5000, 50000.0, "LOW", now_t, "fleet/price_oracle.json"),
            )
            conn.execute(
                "INSERT INTO books (base, system, item, name, category, bid, bid_qty, ask, ask_qty, bid_depth, ask_depth, t, src) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                ("spoof_base", "sys1", "iron_ore", "Iron Ore", "raw", 5000, 1, 12, 100, 1, 100, now_t, "market/spoof.json"),
            )
            row = conn.execute("SELECT raw_bid, fair_price, is_spoof_bid, guarded_bid, spoof_risk FROM clean_books WHERE item = 'iron_ore'").fetchone()
            self.assertEqual(row, (5000, 10.0, 1, 15.0, "LOW"))
            conn.close()

    def test_wallet_settle_confirms_via_moves_during_concurrent_treasury_capex(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "fleet").mkdir(parents=True)
            sent_at = int(time.time()) - 120
            (data / "fleet" / "moves.jsonl").write_text(
                json.dumps({"at": sent_at + 45, "pilot": "Prime Directive", "moved": -361793}) + "\n",
                encoding="ascii",
            )
            (data / "fleet" / "fleet.json").write_text(json.dumps({"ships": []}), encoding="ascii")
            orig_tr = wallet.treasury_read
            try:
                # Treasury dropped from 4.9M -> 3.3M due to concurrent facility build!
                wallet.treasury_read = lambda _leader: 3369767
                st = wallet.settle(str(data), {
                    "at": sent_at, "from": "Prime Directive", "credits": 361793, "before": 4906668,
                })
                self.assertEqual(st, "booked")
                ot = json.loads((data / "fleet" / "onetime.json").read_text(encoding="ascii"))
                self.assertEqual(len(ot), 1)
                self.assertEqual(ot[0][1], "Prime Directive")
                self.assertEqual(ot[0][3], -361793)
            finally:
                wallet.treasury_read = orig_tr

    def test_mcp_income_wings_and_docs_divisions(self):
        self.assertIn("Trinity", collective_mcp.MEMBERS)
        self.assertIn("income", collective_mcp.TOOLS["fleet"]["args"]["view"]["enum"])
        self.assertIn("wings", collective_mcp.TOOLS["fleet"]["args"]["view"]["enum"])
        self.assertEqual(collective_mcp.fleet_plan({"view": "income", "hours": 6}), [("game/fleet/accounting.py", ["--income", "--hours", "6"])])
        self.assertEqual(collective_mcp.fleet_plan({"view": "wings", "hours": 6}), [("game/fleet/kpi_engine.py", ["--summary", "--hours", "6"])])
        self.assertEqual(fleet_docs.kind_of("governance/fleet-division-handbook.md"), ("blueprint", "Fleet"))
        self.assertEqual(fleet_docs.kind_of("governance/divisions/division-hunters.md"), ("division", "Fleet"))


if __name__ == "__main__":
    unittest.main()
