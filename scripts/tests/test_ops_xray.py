#!/usr/bin/env python3
"""Unit tests for ops_xray.py, collective_mcp xray/liquidate tools, and new store.py operational tables/views."""
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FLEET = REPO / "game" / "fleet"
if str(FLEET) not in sys.path:
    sys.path.insert(0, str(FLEET))

import collective_mcp
import ops_xray
import store


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")


class OpsXrayUnitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="test-ops-xray-")
        self.root = Path(self.tmp.name)
        self.data = self.root / "data"
        self.data.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_compute_anomalies_detects_all_classes(self):
        now_t = 1795900000
        _write_json(self.data / "fleet" / "passenger_boards.json", {"updated_at": now_t - 30, "boards": {"b1": {"waiting": []}}})
        _write_json(self.data / "empire" / "empire.json", {"credits": 85000})
        _write_json(self.data / "fleet" / "fleet.json", {"ships": [{"name": "p%d" % i, "credits": 2000} for i in range(60)]})
        _write_json(
            self.data / "fleet" / "bursar_buys.json",
            {"updated_at": now_t, "entries": {"MCV One": {"hub_a": {"at": now_t - 60, "items": {"item_%d" % i: 5 for i in range(55)}}}}},
        )
        _write_json(self.data / "fleet" / "bursar_claims.json", {"nova_terra_central": {"pilot": "MCV One", "claimed_at": now_t}})
        _write_json(self.root / "services" / "status.json", {"services": {"bursar": {"state": "stopped"}, "haul": {"state": "running"}}})
        log_dir = self.data / "routes" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        for i in range(5):
            lp = log_dir / ("run_%d.log" % i)
            lp.write_text("ERR cargo_full and access_denied\n", encoding="utf-8")
            os.utime(lp, (now_t - 30, now_t - 30))

        anoms = ops_xray.compute_anomalies(self.data, now_t=now_t)
        codes = {a[0]: a[1] for a in anoms}
        self.assertEqual(codes.get("passenger_boards_thin"), "CRITICAL")
        self.assertEqual(codes.get("treasury_below_topup_floor"), "CRITICAL")
        self.assertEqual(codes.get("bursar_excess_buy_orders"), "WARN")
        self.assertEqual(codes.get("unstaffed_tier1_hub"), "WARN")
        self.assertEqual(codes.get("service_down"), "CRITICAL")
        self.assertEqual(codes.get("recent_cargo_full"), "WARN")
        self.assertEqual(codes.get("recent_access_denied"), "WARN")

    def test_plan_zero_hop_liquidation_size_aware_and_deducts_cltv_orders(self):
        now_t = 1795900000
        _write_json(
            self.data / "stock" / "storage.json",
            {"faction": {"base_a": {"lead_ore": 400, "fuel": 500, "methane_ice": 300}}},
        )
        _write_json(
            self.data / "catalog" / "0.2.0.json",
            {"items": [
                {"id": "lead_ore", "name": "Lead Ore", "size": 2, "base_value": 100},
                {"id": "methane_ice", "name": "Methane Ice", "size": 1, "base_value": 36},
                {"id": "fuel", "name": "Fuel", "size": 1, "base_value": 10},
            ]},
        )
        _write_json(
            self.data / "market" / "base_a.json",
            {"base": "base_a", "system": "sys_a", "read_at": now_t - 60, "items": [
                {"item_id": "lead_ore", "item_name": "Lead Ore", "best_buy": 120.0, "best_buy_qty": 350, "best_sell": 140.0, "best_sell_qty": 10},
                {"item_id": "methane_ice", "item_name": "Methane Ice", "best_buy": 36.0, "best_buy_qty": 300, "best_sell": 45.0, "best_sell_qty": 10},
                {"item_id": "fuel", "item_name": "Fuel", "best_buy": 15.0, "best_buy_qty": 500, "best_sell": 20.0, "best_sell_qty": 10},
            ]},
        )
        _write_json(
            self.data / "fleet" / "bursar_buys.json",
            {"updated_at": now_t, "entries": {"MCV One": {"base_a": {"at": now_t - 30, "items": {"lead_ore": 50}}}}},
        )
        _write_json(
            self.data / "empire" / "empire.json",
            {"members": [{"name": "MCV Off", "role": "Officer"}]},
        )
        dbp = self.data / "store" / "read.db"
        dbp.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(str(dbp))
        con.execute("CREATE TABLE ships (pilot TEXT, role TEXT, base TEXT, cargo_used INTEGER, cargo_capacity INTEGER, credits INTEGER, docked INTEGER)")
        con.execute("INSERT INTO ships VALUES ('MCV Off', 'trader', 'base_a', 20, 220, 15000, 1)")
        con.execute("CREATE TABLE books (base TEXT, system TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER, t INTEGER)")
        con.execute("INSERT INTO books VALUES ('base_a', 'sys_a', 'lead_ore', 120.0, 350, 140.0, 10, ?)", (now_t - 60,))
        con.execute("INSERT INTO books VALUES ('base_a', 'sys_a', 'methane_ice', 36.0, 300, 45.0, 10, ?)", (now_t - 60,))
        con.execute("INSERT INTO books VALUES ('base_a', 'sys_a', 'fuel', 15.0, 500, 20.0, 10, ?)", (now_t - 60,))
        con.execute("CREATE TABLE items (id TEXT, size INTEGER)")
        con.execute("INSERT INTO items VALUES ('lead_ore', 2)")
        con.execute("INSERT INTO items VALUES ('methane_ice', 1)")
        con.execute("INSERT INTO items VALUES ('fuel', 1)")
        con.commit()
        con.close()

        jobs = ops_xray.plan_zero_hop_liquidation(self.data, min_cash=5000, max_jobs=5, now_t=now_t)
        self.assertEqual(len(jobs), 2)
        lead = [j for j in jobs if j["item"] == "lead_ore"][0]
        self.assertEqual(lead["item_size"], 2)
        self.assertEqual(lead["free_hold"], 200)
        self.assertEqual(lead["chunk_units"], 100)
        self.assertEqual(lead["qty"], 300)
        self.assertEqual(lead["est_cash"], 36000)
        self.assertNotIn("fuel", [j["item"] for j in jobs])

        dry = ops_xray.run_liquidate(self.data, min_cash=5000, max_jobs=5, execute=False)
        self.assertIn("LIQUIDATE (DRY-RUN)", dry)
        self.assertIn("lead_ore (size=2, chunk=100)", dry)

    def test_mcp_xray_and_liquidate_plans_and_hints(self):
        self.assertTrue(collective_mcp.schema("xray")["annotations"]["readOnlyHint"])
        self.assertFalse(collective_mcp.schema("xray")["annotations"]["destructiveHint"])
        self.assertFalse(collective_mcp.schema("liquidate")["annotations"]["readOnlyHint"])
        self.assertTrue(collective_mcp.schema("liquidate")["annotations"]["destructiveHint"])
        self.assertEqual(collective_mcp.TOOLS["xray"]["plan"]({"hours": 6, "top": 5}),
                         [("game/fleet/ops_xray.py", ["xray", "--hours", "6", "--top", "5"])])
        self.assertEqual(collective_mcp.TOOLS["liquidate"]["plan"]({"base": "b1", "execute": True}),
                         [("game/fleet/ops_xray.py", ["liquidate", "--base", "b1", "--execute"])])
        self.assertEqual(collective_mcp.TOOLS["liquidate"]["plan"]({}),
                         [("game/fleet/ops_xray.py", ["liquidate"])])

    def test_store_loads_operational_tables_and_vault_cashable_view(self):
        now_t = 1795900000
        _write_json(self.data / "fleet" / "bursar_buys.json",
                    {"updated_at": now_t, "entries": {"MCV One": {"base_a": {"at": now_t - 60, "items": {"lead_ore": 40}}}}})
        _write_json(self.data / "fleet" / "bursar_claims.json",
                    {"base_a": {"pilot": "MCV One", "base": "base_a", "claimed_at": now_t, "unwind": True}})
        _write_json(self.data / "fleet" / "haul_claims.json",
                    {"supply:faction:base_a:lead_ore#1": {"pilot": "LSV Two", "at": now_t}})
        _write_json(self.data / "fleet" / "passenger_rep_claims.json",
                    {"base_b": {"pilot": "LSV Pax", "at": now_t, "exp": now_t + 600}})
        _write_json(self.data / "fleet" / "passenger_boards.json",
                    {"updated_at": now_t, "boards": {
                        "base_a": {"system": "sys_a", "t": now_t, "fare_surge": 1.8, "demand_level": "surging",
                                   "transit_lounge": {"occupancy": 4, "capacity": 60}, "waiting": [{"id": "c1"}, {"id": "c2"}]}
                    }})
        _write_json(self.data / "fleet" / "fleet.json", {"updated_at": now_t, "ships": [{"name": "p1", "credits": 5000}]})
        _write_json(self.data / "catalog" / "0.2.0.json", {
            "items": [
                {"id": "lead_ore", "name": "Lead Ore", "category": "raw", "size": 2, "base_value": 100},
                {"id": "reserved_item", "name": "Reserved", "category": "raw", "size": 1, "base_value": 50},
            ],
            "recipes": [], "facilities": [], "ships": [], "skills": [],
        })
        _write_json(self.data / "empire" / "empire.json", {
            "written_at": now_t,
            "faction": {"id": "f1", "name": "CLTV", "tag": "CLTV", "treasury": 500000},
            "faction_storage": [
                {"base": "base_a", "base_name": "Base A", "item": "lead_ore", "units": 200},
                {"base": "base_a", "base_name": "Base A", "item": "reserved_item", "units": 200},
            ],
        })
        _write_json(self.data / "market" / "base_a.json", {
            "base": "base_a", "system": "sys_a", "read_at": now_t,
            "items": [
                {"item_id": "lead_ore", "item_name": "Lead Ore", "category": "raw", "best_buy": 120, "best_buy_qty": 150, "best_sell": 140, "best_sell_qty": 10},
                {"item_id": "reserved_item", "item_name": "Reserved", "category": "raw", "best_buy": 50, "best_buy_qty": 100, "best_sell": 60, "best_sell_qty": 10},
            ],
        })
        _write_json(self.data / "fleet" / "price_oracle.json", {
            "updated_at": now_t,
            "items": {
                "lead_ore": {"fair_price": 120, "twap": 120, "vwm": 120, "stations": 2, "total_qty": 300, "total_cash": 36000, "spoof_risk": "LOW"},
                "reserved_item": {"fair_price": 50, "twap": 50, "vwm": 50, "stations": 2, "total_qty": 100, "total_cash": 5000, "spoof_risk": "LOW"},
            },
        })
        needs_p = self.root / "needs.tsv"
        needs_p.parent.mkdir(parents=True, exist_ok=True)
        needs_p.write_text(
            "id\tproject\tdivision\tkind\tref\tunits\tpriority\tplace\tdue\tstatus\tnote\tadded\tadded_by\tchanged\tchanged_by\n"
            "n1\tP\tmining\titem\treserved_item\t100\t1\t\t\topen\t\t2026-11-28T00:00Z\tUnity\t2026-11-28T00:00Z\tUnity\n",
            encoding="utf-8",
        )

        store.one_pass(str(self.data), now=now_t, root=str(self.root))
        conn = store.connect(str(self.data))
        self.addCleanup(conn.close)

        oo = conn.execute("SELECT pilot, base, item, qty FROM cltv_open_orders").fetchall()
        self.assertEqual(oo, [("MCV One", "base_a", "lead_ore", 40)])

        lc = {r[0]: (r[1], r[2], r[3], r[4]) for r in conn.execute("SELECT kind, claim_key, pilot, base, item FROM live_claims").fetchall()}
        self.assertEqual(set(lc.keys()), {"bursar", "haul", "passenger_rep"})
        self.assertEqual(lc["bursar"], ("base_a", "MCV One", "base_a", "unwind"))
        self.assertEqual(lc["haul"][1:4], ("LSV Two", "base_a", "lead_ore"))

        pb = conn.execute("SELECT base, waiting, lounge_occ, lounge_cap, fare_surge, demand_level FROM passenger_boards").fetchall()
        self.assertEqual(pb, [("base_a", 2, 4, 60, 1.8, "surging")])

        fa = {r[0]: r[1] for r in conn.execute("SELECT code, severity FROM fleet_anomalies").fetchall()}
        self.assertEqual(fa.get("passenger_boards_thin"), "CRITICAL")

        vc = conn.execute("SELECT vault_base, sell_base, same_base, item, item_size, ext_bid_qty, sellable_qty, est_cash, cr_per_m3 FROM vault_cashable").fetchall()
        self.assertEqual(len(vc), 1)
        self.assertEqual(vc[0], ("base_a", "base_a", 1, "lead_ore", 2, 110, 110, 13200.0, 60.0))


if __name__ == "__main__":
    unittest.main()
