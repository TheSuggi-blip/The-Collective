#!/usr/bin/env python3
"""Unit tests for GAAP/IFRS accounting, IAS 2 NRV valuation, matching principle, transfer pricing, watchdog & api_income."""

import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))
sys.path.insert(0, str(REPO / "station"))

import accounting
import server
import watchdog


def _build_fixture(tmp_dir, now=None):
    now = int(time.time()) if now is None else now
    root = Path(tmp_dir) / "repo"
    data = Path(tmp_dir) / "data"
    (root / "game" / "routes").mkdir(parents=True)
    (data / "store").mkdir(parents=True)
    (data / "fleet").mkdir(parents=True)
    (data / "stock").mkdir(parents=True)

    for i in range(410):
        rid = "aaa-route-%04d" % i
        (root / "game" / "routes" / (rid + ".json")).write_text(
            json.dumps({"id": rid, "title": "Filler %d" % i, "once": False}),
            encoding="ascii",
        )
    (root / "game" / "routes" / "mission-zeta-seed.json").write_text(
        json.dumps({"id": "mission-zeta-seed", "title": "One-time Seed Mission", "once": True}),
        encoding="ascii",
    )
    (root / "game" / "routes" / "fit-laser-iii.json").write_text(
        json.dumps({"id": "fit-laser-iii", "title": "Fit Mining Laser III", "once": True}),
        encoding="ascii",
    )
    (root / "game" / "routes" / "sell-copper.json").write_text(
        json.dumps({"id": "sell-copper", "title": "Sell Copper Ore", "once": False}),
        encoding="ascii",
    )
    (root / "game" / "routes" / "bad-bleed.json").write_text(
        json.dumps({"id": "bad-bleed", "title": "Broken Trade Route", "once": False}),
        encoding="ascii",
    )

    fj = {
        "ships": [],
        "totals": {
            "rates": {
                "windows": {
                    "24h": {
                        "minutes": 1440,
                        "income_per_hour": 80000,
                        "costs_per_hour": 150000,
                        "cph": -70000,
                        "rewards_per_hour": 300000,
                        "bought_once_per_hour": 50000,
                        "one_time_per_hour": 250000,
                        "total_per_hour": 180000,
                        "treasury_own_per_hour": -10000,
                        "purse_per_hour": 170000,
                        "divisions": {
                            "Mining": {"cph": -30000},
                            "Trade": {"cph": 20000},
                            "Military": {"cph": -40000},
                            "Logistics": {"cph": -10000},
                            "Intel": {"cph": -10000},
                            "Command": {"cph": 0},
                        },
                    }
                }
            }
        },
    }
    (data / "fleet" / "fleet.json").write_text(json.dumps(fj), encoding="ascii")

    db = data / "store" / "read.db"
    conn = sqlite3.connect(str(db))
    conn.executescript("""
        CREATE TABLE items (id TEXT PRIMARY KEY, name TEXT, base_value REAL);
        CREATE TABLE books (item TEXT, station TEXT, bid REAL, bid_qty REAL);
        CREATE TABLE holdings (item TEXT, place TEXT, units REAL);
        CREATE TABLE ships (pilot TEXT PRIMARY KEY, division TEXT, role TEXT, status TEXT, flies TEXT, activity TEXT, credits REAL, t INT, class TEXT, system TEXT, docked TEXT);
        CREATE TABLE runs (pilot TEXT, route TEXT, kind TEXT, started TEXT, t REAL, minutes REAL, credits REAL, one_time REAL, readable INT, row TEXT);
        CREATE TABLE stock_hour (hour INT, division TEXT, item TEXT, units REAL, t INT);
        CREATE TABLE faction (treasury REAL, member_count INT, members_limit INT, owned_bases INT);
        CREATE TABLE faction_facilities (id TEXT);
        CREATE TABLE places (system TEXT, t INT);
        CREATE TABLE stats_figures (view TEXT, subject TEXT, hours REAL, figure TEXT, value REAL, text TEXT);
    """)
    conn.executemany("INSERT INTO items VALUES (?,?,?)", [
        ("silicon_ore", "Silicon Ore", 10),
        ("quantum_fragments", "Quantum Fragments", 600),
        ("circuit_board", "Circuit Board", 200),
        ("copper_ore", "Copper Ore", 8),
    ])
    conn.executemany("INSERT INTO books VALUES (?,?,?,?)", [
        ("silicon_ore", "st1", 800, 5),
        ("silicon_ore", "st2", 12, 100),
        ("quantum_fragments", "st1", 3, 100),
        ("circuit_board", "st1", 250, 10),
        ("copper_ore", "st1", 4, 500),
    ])
    conn.executemany("INSERT INTO holdings VALUES (?,?,?)", [
        ("silicon_ore", "b1", 1000),
        ("quantum_fragments", "b1", 100),
        ("circuit_board", "b1", 100),
    ])
    conn.executemany("INSERT INTO ships VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
        ("miner-1", "Mining", "miner", "connected", "mine field-a", "mining", 20000, now - 10, "Liminal", "sys1", ""),
        ("trader-1", "Trade", "trader", "connected", "circuit sell-copper", "docked", 50000, now - 10, "Barter", "sys1", "st1"),
        ("drone-1", "Military", "drone", "connected", "hunt field-b", "fighting", 20000, now - 10, "Recursion", "sys1", ""),
    ])
    conn.execute("INSERT INTO faction VALUES (100000, 50, 100, 1)")
    conn.execute("INSERT INTO places VALUES ('sys1', ?)", (now - 100,))
    conn.execute("INSERT INTO stats_figures VALUES ('kpi', 'Fleet', 24, 'net', -70000, '')")

    run_rows = []
    for i in range(24):
        run_rows.append(("miner-1", "mission-zeta-seed", "circuit", "2026-11-23T00:00:00Z", now - 3600 * (i + 0.5), 30.0, -10000.0, 200000.0, 1, "{}"))
    run_rows.append(("drone-1", "fit-laser-iii", "circuit", "2026-11-23T01:00:00Z", now - 3600, 10.0, 24000.0, -120000.0, 1, "{}"))
    for i in range(10):
        run_rows.append(("trader-1", "sell-copper", "circuit", "2026-11-23T02:00:00Z", now - 3600 * (i + 0.2), 20.0, 48000.0, 0.0, 1, "{}"))
    for i in range(5):
        run_rows.append(("trader-1", "bad-bleed", "circuit", "2026-11-23T03:00:00Z", now - 1800 * (i + 1), 15.0, -6000.0, 0.0, 1, "{}"))
    conn.executemany("INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?,?)", run_rows)

    h1 = now - (now % 3600)
    h0 = h1 - 86400
    conn.executemany("INSERT INTO stock_hour VALUES (?,?,?,?,?)", [
        (h0, "Trade", "circuit_board", 0, h0),
        (h1, "Trade", "circuit_board", 600, h1),
        (h0, "Trade", "copper_ore", 0, h0),
        (h1, "Trade", "copper_ore", 12000, h1),
        (h0, "Mining", "copper_ore", 1000, h0),
        (h1, "Mining", "copper_ore", 1000, h1),
    ])
    conn.commit()
    conn.close()

    ho = {"at": h0 + 7200, "from": "miner-1", "to": "trader-1", "items": {"copper_ore": 12000}}
    (data / "stock" / "handover.jsonl").write_text(json.dumps(ho) + "\n", encoding="ascii")
    return root, data, now


class TestFleetAccounting(unittest.TestCase):
    def test_ias2_vault_valuation_rejects_thin_bid_and_overpriced_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            _root, data, _now = _build_fixture(tmp)
            conn = sqlite3.connect(str(data / "store" / "read.db"))
            try:
                vv = accounting.vault_valuation(conn)
            finally:
                conn.close()
            self.assertEqual(vv["catalog"], 90000)
            self.assertEqual(vv["unbounded_bid"], 825300)
            self.assertEqual(vv["nrv"], 30300)
            self.assertEqual(vv["liquid"], 8000)
            self.assertTrue(len(vv["top_gaps"]) >= 2)

    def test_matching_principle_reconciliation_and_transfer_pricing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data, now = _build_fixture(tmp)
            conn = sqlite3.connect(str(data / "store" / "read.db"))
            try:
                pnl = accounting.compute_pnl(conn, repo_root=str(root), data_dir=str(data), hours=24, now=now)
            finally:
                conn.close()
            self.assertEqual(pnl["once_mission_direct_h"], -10000)
            self.assertEqual(pnl["capex_fit_direct_h"], 1000)
            self.assertEqual(pnl["once_direct_h"], -9000)
            self.assertEqual(pnl["recurring_cash_h"], -61000)
            self.assertEqual(pnl["seed_net_h"], 290000)
            self.assertEqual(pnl["capex_net_h"], -49000)
            self.assertEqual(
                pnl["recurring_cash_h"] + pnl["seed_net_h"] + pnl["capex_net_h"] + pnl["treasury_own_h"],
                pnl["purse_h"],
            )
            self.assertTrue(pnl["has_inventory_accrual"])
            self.assertEqual(pnl["inventory_accrual_h"], 7000)
            self.assertEqual(pnl["accrual_operating_h"], -54000)
            divs = pnl["by_division"]
            self.assertEqual(divs["Mining"]["tx_out_h"], 2000)
            self.assertEqual(divs["Trade"]["tx_in_h"], 2000)
            self.assertEqual(sum(d["tx_out_h"] for d in divs.values()), sum(d["tx_in_h"] for d in divs.values()))
            self.assertEqual(sum(d["accrual_op_h"] for d in divs.values()), pnl["accrual_operating_h"])

    def test_watchdog_does_not_false_alarm_profitable_once_mission(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data, now = _build_fixture(tmp)
            res = watchdog.inspect(str(root), str(data), hours=24.0, now=now, save=False)
            bleeds = [f["summary"] for f in res["findings"] if f["code"] in ("ROUTE_BLEED", "ROUTE_LOSS")]
            joined = " ".join(bleeds)
            self.assertNotIn("mission-zeta-seed", joined)
            self.assertIn("bad-bleed", joined)

    def test_api_income_uses_read_db_and_loads_over_400_routes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data, _now = _build_fixture(tmp)
            st_dir = data / "station"
            st_dir.mkdir(parents=True)
            old_repo, old_data, old_fleet = server.REPO, server.DATA, server.FLEET
            try:
                server.REPO = root
                server.DATA = st_dir
                server.FLEET = data / "fleet"
                inc = server.api_income(24)
            finally:
                server.REPO, server.DATA, server.FLEET = old_repo, old_data, old_fleet
            self.assertEqual(inc["source"], "read.db")
            by_r = {r["route"]: r for r in inc["routes"]}
            self.assertIn("mission-zeta-seed", by_r)
            self.assertTrue(by_r["mission-zeta-seed"]["once"])
            self.assertEqual(by_r["mission-zeta-seed"]["credits"], -240000)
            self.assertEqual(by_r["mission-zeta-seed"]["one_time"], 4800000)
            self.assertEqual(by_r["mission-zeta-seed"]["matched_net"], 4560000)


    def test_ship_pnl_24h_matches_accounting_principles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data, now = _build_fixture(tmp)
            conn = sqlite3.connect(str(data / "store" / "read.db"))
            try:
                m_pnl = accounting.ship_pnl_24h(conn, "miner-1", repo_root=str(root), data_dir=str(data), now=now)
                t_pnl = accounting.ship_pnl_24h(conn, "trader-1", repo_root=str(root), data_dir=str(data), now=now)
                d_pnl = accounting.ship_pnl_24h(conn, "drone-1", repo_root=str(root), data_dir=str(data), now=now)
            finally:
                conn.close()
            self.assertEqual(m_pnl["recurring_cash"], 0)
            self.assertEqual(m_pnl["once_direct"], -240000)
            self.assertEqual(m_pnl["seed_matched"], 4560000)
            self.assertEqual(m_pnl["handovers_out_nrv"], 48000)
            self.assertEqual(m_pnl["accrual_value_add"], 48000)
            self.assertEqual(m_pnl["total_wallet"], m_pnl["credits"] + m_pnl["one_time"])
            self.assertEqual(t_pnl["recurring_cash"], 450000)
            self.assertEqual(t_pnl["handovers_in_nrv"], 48000)
            self.assertEqual(t_pnl["accrual_value_add"], 402000)
            self.assertEqual(d_pnl["recurring_cash"], 0)
            self.assertEqual(d_pnl["capex_matched"], -96000)
            self.assertEqual(d_pnl["total_wallet"], -96000)


    def test_scorecard_uses_matched_drags_and_detects_diplo_reply(self):
        import scorecard
        with tempfile.TemporaryDirectory() as tmp:
            root, data, now = _build_fixture(tmp)
            (data / "comms").mkdir(parents=True, exist_ok=True)
            (data / "comms" / "diplomacy.json").write_text(json.dumps({
                "factions": {
                    "IRLC": {"tag": "IRLC", "leader": "ILC Comptroller", "status": "neutrality_agreed", "last_sent_at": "2026-11-23T05:03:11Z"},
                    "HEXC": {"tag": "HEXC", "leader": "HexCogitoAI", "status": "neutrality_agreed", "last_sent_at": "2026-11-23T05:03:11Z"},
                }
            }), encoding="ascii")
            (data / "comms" / "messages.jsonl").write_text(
                json.dumps({"t": "2026-11-23T03:35:10Z", "channel": "private", "sender": "HexCogitoAI", "tag": "HEXC", "own": False, "text": "ok"}) + "\n"
                + json.dumps({"t": "2026-11-23T14:24:13Z", "channel": "private", "sender": "ILC Comptroller", "tag": "IRLC", "own": False, "text": "trade on exchange"}) + "\n",
                encoding="ascii",
            )
            neutral_n, pend_n, pend_tags = scorecard._load_diplomacy_pending(str(data))
            self.assertEqual(neutral_n, 2)
            self.assertEqual(pend_n, 1)
            self.assertEqual(pend_tags, ["IRLC"])

            sc = scorecard.compute_scorecard(str(root), str(data), now=now)
            drags_txt = " | ".join(sc["enterprise"]["drags"])
            self.assertIn("recurring cash", drags_txt)
            self.assertNotIn("steady net", drags_txt)


if __name__ == "__main__":
    unittest.main()
