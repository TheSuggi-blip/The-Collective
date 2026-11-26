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
            # Marginal depth-reconciled IAS 2 NRV: 10u circuit_board bid depth (3,750 / 24h = 156/h); 12,000u unbid copper_ore glut adds 0!
            self.assertEqual(pnl["inventory_accrual_h"], 156)
            self.assertEqual(pnl["accrual_operating_h"], -60844)
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



    def test_other_cogs_never_negative_when_passive_fills_or_escrow_unwind_dominate(self):
        import tempfile
        # Simulate Trade escrow unwind + passive sell-order fills making fleet.py costs_per_hour negative (-308k)!
        fj = {
            "totals": {
                "rates": {
                    "windows": {
                        "1h": {
                            "minutes": 60,
                            "income_per_hour": 307000,
                            "costs_per_hour": -308000,
                            "cph": 615000,
                            "rewards_per_hour": 270000,
                            "bought_once_per_hour": 60000,
                            "fuel_cr_per_hour": 270000,
                            "repair_cr_per_hour": 500,
                            "spent_per_hour": 512000,
                            "unexplained_per_hour": 760000,
                            "treasury_own_per_hour": -5000,
                            "purse_per_hour": 820000,
                            "divisions": {
                                "Trade": {"cph": 720000, "one_time_per_hour": 0, "fuel_cr_per_hour": 10000, "unexplained_per_hour": 760000, "spent_per_hour": 140000},
                                "Logistics": {"cph": 140000, "one_time_per_hour": 25000, "fuel_cr_per_hour": 70000, "unexplained_per_hour": 0, "spent_per_hour": 115000},
                                "Mining": {"cph": -65000, "one_time_per_hour": 175000, "fuel_cr_per_hour": 65000, "unexplained_per_hour": 0, "spent_per_hour": 90000},
                                "Military": {"cph": -80000, "one_time_per_hour": 10000, "fuel_cr_per_hour": 85000, "unexplained_per_hour": 0, "spent_per_hour": 105000},
                                "Intel": {"cph": -40000, "one_time_per_hour": -5000, "fuel_cr_per_hour": 40000, "unexplained_per_hour": 0, "spent_per_hour": 45000},
                            },
                        }
                    }
                }
            }
        }
        with tempfile.TemporaryDirectory() as td:
            p = accounting.compute_pnl(None, repo_root=td, data_dir=td, fleet_json=fj, hours=1)
            ob = p["opex_breakdown"]
            # Expense MUST NEVER be negative (which rendered as positive expense credit on HUD!)
            self.assertGreaterEqual(ob["other_cogs_h"], 0, ob)
            self.assertEqual(p["passive_inflows_h"], 760000)
            self.assertEqual(ob["gross_direct_h"], ob["fuel_h"] + ob["repair_h"] + ob["craft_inputs_h"] + ob["other_cogs_h"])
            # Exact zero-plug reconciliation: (active_rev + passive_inflows) - matched_direct == recurring_cash_h!
            self.assertEqual((p["raw_income_h"] + p["passive_inflows_h"]) - ob["matched_direct_h"], p["recurring_cash_h"])



    def test_compute_pnl_does_not_double_count_standing_sell_escrow_and_caps_overpriced_ask_with_oracle(self):
        import sqlite3, tempfile, time
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "fleet").mkdir(parents=True)
            # Standing sell-order escrow from days ago (80,000 units!) MUST NOT appear as +1M cr/h new 1h build!
            (data / "fleet" / "bursar_sells.json").write_text(json.dumps({
                "updated_at": 1795659999,
                "entries": {
                    "trader-1": {
                        "central_nexus": {"at": 1795659999, "items": {"null_matter": 5000}}
                    }
                },
            }), encoding="ascii")
            (data / "fleet" / "price_oracle.json").write_text(json.dumps({
                "updated_at": int(time.time()),
                "items": {
                    "null_matter": {"fair_price": 2.0, "twap": 2.0, "vwm": 2.0, "stations": 2, "total_qty": 97667, "t": int(time.time())}
                }
            }), encoding="ascii")
            con = sqlite3.connect(":memory:")
            con.executescript("""
                CREATE TABLE items (id TEXT, base_value REAL);
                CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER);
                CREATE TABLE stock_hour (hour INTEGER, division TEXT, item TEXT, units INTEGER);
                INSERT INTO items VALUES ('null_matter', 200.0);
                INSERT INTO books VALUES ('deep_range', 'null_matter', 2.0, 48924, 428.0, 4759);
                INSERT INTO stock_hour VALUES (1795654800, 'Trade', 'null_matter', 100);
                INSERT INTO stock_hour VALUES (1795658400, 'Trade', 'null_matter', 100);
            """)
            p = accounting.compute_pnl(con, repo_root=td, data_dir=td, fleet_json={"totals": {"rates": {"windows": {"1h": {"minutes": 60}}}}}, hours=1, now=1795659000)
            # Stock did not change (100 -> 100): inventory accrual MUST be 0, NOT +600k from standing sell escrow!
            self.assertEqual(p["inventory_accrual_h"], 0)
            # Oracle-anchored unit valuation of null_matter MUST be <= 2.5 cr (NEVER 125+ cr from overpriced 428 cr ask!)
            fm = accounting._load_oracle_fair_map(data)
            bm, mb, bbi = accounting._load_price_maps(con, data_dir=data)
            am = accounting._load_ask_map(con)
            u_p = accounting.live_market_unit_price("null_matter", bm, bbi, {}, held_units=5000, max_bid_map=mb, ask_map=am, fair_map=fm)
            self.assertLessEqual(u_p, 2.5)
            con.close()


    def test_revenue_breakdown_reconciles_all_operating_wings_and_divisions(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE ships (pilot TEXT, division TEXT)")
        conn.execute("CREATE TABLE runs (pilot TEXT, route TEXT, kind TEXT, minutes REAL, credits REAL, one_time REAL, readable INTEGER, t REAL)")
        now = time.time()
        conn.executemany(
            "INSERT INTO ships VALUES (?, ?)",
            [
                ("MCV Alexandria", "Trade"), ("MCV Bukhara", "Trade"),
                ("LSV Aether Drift", "Logistics"), ("LSV Belvedere", "Logistics"),
                ("ROU Ashen Blade", "Military"), ("EUV Alabaster", "Mining"), ("VSV Azimuth", "Intel"),
            ],
        )
        conn.executemany(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, 1, ?)",
            [
                ("MCV Alexandria", "bursar-network", "bursar", 30, 6000, 0, now - 600),
                ("MCV Bukhara", "haul-network-trade", "haul", 30, 4000, 0, now - 600),
                ("LSV Aether Drift", "haul-network", "haul", 30, 8000, 0, now - 600),
                ("LSV Belvedere", "haul-network", "haul", 30, 2000, 0, now - 600),
                ("ROU Ashen Blade", "hunt-network", "hunt", 30, 5000, 0, now - 600),
            ],
        )
        fj = {
            "totals": {"rates": {"windows": {
                "1h": {
                    "minutes": 60.0,
                    "income_per_hour": 30000.0,
                    "costs_per_hour": 10000.0,
                    "unexplained_per_hour": 5000.0,
                    "cph": 20000.0,
                    "rewards_per_hour": 0.0,
                    "bought_once_per_hour": 0.0,
                    "divisions": {
                        "Trade": {"income_per_hour": 10000.0, "cph": 8000.0},
                        "Logistics": {"income_per_hour": 10000.0, "cph": 7000.0},
                        "Military": {"income_per_hour": 7000.0, "cph": 4000.0},
                        "Mining": {"income_per_hour": 2500.0, "cph": 800.0},
                        "Intel": {"income_per_hour": 500.0, "cph": 200.0},
                    },
                }
            }}}
        }
        repo_r = str(Path(__file__).resolve().parents[2])
        res = accounting.compute_pnl(conn, repo_root=repo_r, data_dir=repo_r, fleet_json=fj, hours=1, now=now, price_maps=({}, {}))
        rb = res["revenue_breakdown"]
        self.assertEqual(rb["bursar_active_h"], 6000)
        self.assertEqual(rb["mobile_trade_h"], 4000)
        self.assertEqual(rb["logistics_core_h"], 8000)
        self.assertEqual(rb["passenger_liners_h"], 2000)
        self.assertEqual(rb["military_h"], 7000)
        self.assertEqual(rb["mining_h"], 2500)
        self.assertEqual(rb["intel_h"], 500)
        self.assertEqual(rb["passive_escrow_h"], 5000)
        seg_sum = (
            rb["bursar_active_h"] + rb["mobile_trade_h"] + rb["logistics_core_h"]
            + rb["passenger_liners_h"] + rb["military_h"] + rb["mining_h"] + rb["intel_h"]
        )
        self.assertEqual(seg_sum, res["raw_income_h"])
        self.assertEqual(seg_sum + rb["passive_escrow_h"], res["raw_income_h"] + res["passive_inflows_h"])


    def test_mining_segments_and_ifrs10_elimination_reconcile(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "stock").mkdir(parents=True)
            now = time.time()
            # Pick real manifest pilots from 3A (Ore Precision), 3D (Gas), 3E (Ice)
            import manifest_wings as mw
            _repo = Path(__file__).resolve().parents[2]
            wings = {r.split('\t')[0]: r.split('\t')[2] for r in (_repo / 'game' / 'fleet-500-manifest.tsv').read_text(encoding='utf-8').splitlines()[1:] if '\t' in r}
            p_3a = next(p for p, w in wings.items() if w.startswith("3A."))
            p_3d = next(p for p, w in wings.items() if w.startswith("3D."))
            p_3e = next(p for p, w in wings.items() if w.startswith("3E."))
            p_mil = next(p for p, w in wings.items() if w.startswith("2A."))
            (data / "stock" / "handover.jsonl").write_text(
                "\n".join([
                    json.dumps({"at": now - 600, "base": "sol_central", "from": p_3a, "to": "Faction", "items": {"gold_ore": 100}, "route": "mine-network"}),
                    json.dumps({"at": now - 500, "base": "neb_hub", "from": p_3d, "to": "Faction", "items": {"helium_gas": 50}, "route": "mine-network"}),
                    json.dumps({"at": now - 400, "base": "sol_central", "from": p_3e, "to": "Faction", "items": {"water_ice": 200}, "route": "mine-network"}),
                    json.dumps({"at": now - 300, "base": "sol_central", "from": p_mil, "to": "LSV Aether Drift", "items": {"quantum_silk": 10}, "route": "hunt-network"}),
                ]) + "\n",
                encoding="ascii",
            )
            conn = sqlite3.connect(":memory:")
            conn.execute("CREATE TABLE ships (pilot TEXT, division TEXT)")
            conn.execute("CREATE TABLE items (id TEXT, base_value REAL)")
            conn.execute("CREATE TABLE books (base TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER)")
            conn.execute("CREATE TABLE runs (pilot TEXT, route TEXT, kind TEXT, minutes REAL, credits REAL, one_time REAL, readable INTEGER, t REAL, row TEXT)")
            conn.executemany("INSERT INTO ships VALUES (?, ?)", [(p_3a, "Mining"), (p_3d, "Mining"), (p_3e, "Mining"), (p_mil, "Military")])
            conn.executemany("INSERT INTO items VALUES (?, ?)", [("gold_ore", 50.0), ("helium_gas", 80.0), ("water_ice", 10.0), ("quantum_silk", 500.0)])
            conn.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)", [
                ("sol_central", "gold_ore", 50.0, 1000, 60.0, 500),
                ("neb_hub", "helium_gas", 80.0, 1000, 90.0, 500),
                ("sol_central", "water_ice", 10.0, 1000, 15.0, 500),
                ("sol_central", "quantum_silk", 500.0, 1000, 600.0, 500),
            ])
            conn.execute(
                "INSERT INTO runs VALUES (?, 'mine-network', 'mine', 30, 0, 0, 1, ?, ?)",
                (p_3a, now - 600, json.dumps({"ore": 100, "resource": "gold_ore"})),
            )
            fj = {"totals": {"rates": {"windows": {"1h": {"minutes": 60.0, "income_per_hour": 12000.0, "costs_per_hour": 4000.0, "cph": 8000.0}}}}}
            res = accounting.compute_pnl(conn, repo_root=str(_repo), data_dir=str(data), fleet_json=fj, hours=1, now=now)
            # _div_of_pilot must map "Faction" cleanly -> Faction
            self.assertEqual(accounting._div_of_pilot("Faction"), "Faction")
            ms = res["mining_segments"]
            self.assertEqual(ms["3A"]["tx_nrv_h"], 5000)
            self.assertEqual(ms["3A"]["units_h"], 100)
            self.assertEqual(ms["3D"]["tx_nrv_h"], 4000)
            self.assertEqual(ms["3E"]["tx_nrv_h"], 2000)
            it = res["intersegment_totals"]
            self.assertEqual(it["mining_tx_h"], 11000)
            self.assertEqual(it["military_tx_h"], 5000)
            self.assertEqual(it["total_tx_h"], 16000)
            self.assertEqual(it["consolidation_elim_h"], -16000)
            self.assertEqual(it["net_consolidated_impact_h"], 0)
            # Section 1 Consolidated External Revenue MUST NOT double-count internal transfers!
            self.assertEqual(res["raw_income_h"], 12000)
            conn.close()

if __name__ == "__main__":
    unittest.main()
