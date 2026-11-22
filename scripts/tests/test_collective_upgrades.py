"""Unit tests for the 2026-11-22 Collective fleet, store, wallet and station upgrades.
Disposable folders only: no engine, no live data, no network. ASCII only."""

import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"
STATION = ROOT / "station"
sys.path.insert(0, str(FLEET))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DispatchUpgradesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="collective-upg-dispatch-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        (self.data / "routes").mkdir()
        self.dispatch = load("dispatch_upg_test", FLEET / "dispatch.py")

    def _state(self, now, rows=None, pirates=None):
        return {
            "now": now, "data": str(self.data), "rows": rows or [], "orders": {},
            "rest": {}, "booked": {}, "loss": {}, "late": {}, "pirates": pirates or {},
        }

    def test_circuit_pirate_check_blocks_mine_and_hunt_stops_in_warned_system(self):
        now = time.time()
        route = {
            "id": "circuit-raid", "kind": "circuit",
            "stops": [
                {"at": "safe_sys:station", "buy": [{"item": "fuel", "qty": 10}]},
                {"at": "safe_sys:station", "mine": [{"at": "hot_sys:belt_1"}]},
            ],
        }
        pilot = {"name": "miner-1", "role": "miner", "credits": 40000, "docked": True, "modules": [], "skills": {}, "goods": 0}
        self.assertEqual(self.dispatch.circuit_systems(route), ["hot_sys"])
        # Warned system blocks the circuit
        reason, _ = self.dispatch.why_not(pilot, "circuit-raid", route, self._state(now, pirates={"hot_sys": now - 60}))
        self.assertIsNotNone(reason)
        self.assertIn("pirate", reason.lower())
        # Unwarned system allows the circuit
        reason_ok, _ = self.dispatch.why_not(pilot, "circuit-raid", route, self._state(now, pirates={"other_sys": now - 60}))
        self.assertIsNone(reason_ok)

    def test_failed_buy_and_three_zero_cr_stalls_rest_pilot_for_stall_rest(self):
        now = time.time()
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 120))
        pilot = {"name": "trader-1", "role": "trader", "credits": 45000, "docked": True, "modules": [], "skills": {}, "goods": 0}
        route = {"id": "trade-test", "kind": "trade", "buy_at": "a:b", "sell_at": "c:d"}

        # Case 1: non-ask failed buy (wallet floor) triggers STALL_REST
        rows_fb = [{"route": "trade-test", "pilot": "trader-1", "started": started, "minutes": 0.4,
                    "delta": 0, "notes": ["buy foo: wallet floor", "run ended (stop_on_failed_buy)"]}]
        reason_fb, _ = self.dispatch.why_not(pilot, "trade-test", route, self._state(now, rows=rows_fb))
        self.assertIsNotNone(reason_fb)
        self.assertIn("failed buy", reason_fb)

        # Case 2: 3 consecutive short 0-cr runs trigger STALL_REST
        rows_stall = [
            {"route": "trade-test", "pilot": "trader-1", "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 300 + i * 60)),
             "minutes": 0.3, "delta": 0, "notes": []}
            for i in range(3)
        ]
        reason_st, _ = self.dispatch.why_not(pilot, "trade-test", route, self._state(now, rows=rows_stall))
        self.assertIsNotNone(reason_st)
        self.assertIn("short zero-credit runs", reason_st)

        # Case 3: a healthy run after stalls clears the breaker
        rows_ok = rows_stall + [{"route": "trade-test", "pilot": "trader-1", "started": started, "minutes": 12.0, "delta": 800, "notes": []}]
        reason_ok, _ = self.dispatch.why_not(pilot, "trade-test", route, self._state(now, rows=rows_ok))
        self.assertIsNone(reason_ok)


class StatsPausedHoursTests(unittest.TestCase):
    def test_paused_zero_ship_hours_do_not_blind_mad_baseline(self):
        stats = load("stats_upg_test", FLEET / "stats.py")
        store = load("store_upg_test", FLEET / "store.py")
        conn = sqlite3.connect(":memory:")
        self.addCleanup(conn.close)
        conn.executescript(store.SCHEMA)
        store.setup_snapshot(conn)
        now = 1795300000
        # Insert 60 paused zero-ship hours (>50% of window!) + 30 active working hours with variance
        base_hr = (now // 3600) * 3600 - 95 * 3600
        for i in range(60):
            hr = base_hr + i * 3600
            conn.execute(
                "INSERT INTO stats_money_hour (hour, division, ships, minutes, income, costs, net, total, t) "
                "VALUES (?, 'Fleet', 0, 0, 0, 0, 0, 0, ?)", (hr, now))
        for i in range(30):
            hr = base_hr + (60 + i) * 3600
            net = 50000 + (i % 5) * 4000
            conn.execute(
                "INSERT INTO stats_money_hour (hour, division, ships, minutes, income, costs, net, total, t) "
                "VALUES (?, 'Fleet', 200, 60, ?, 10000, ?, ?, ?)", (hr, net + 10000, net, net, now))
        # Latest active hour: huge negative outlier
        hr_last = base_hr + 91 * 3600
        conn.execute(
            "INSERT INTO stats_money_hour (hour, division, ships, minutes, income, costs, net, total, t) "
            "VALUES (?, 'Fleet', 200, 60, 10000, 90000, -80000, -80000, ?)", (hr_last, now))
        conn.commit()
        rows = stats.figures_alerts(conn, now)
        net_row = next((r for r in rows if r[0] == "Fleet steady net per hour"), None)
        self.assertIsNotNone(net_row)
        self.assertTrue(net_row[5].startswith("OUT LOW:"), net_row[5])
        self.assertNotIn("MAD 0", net_row[5])


class SupplyBunkerFuelTests(unittest.TestCase):
    def test_faction_storage_fuel_counted_without_double_counting_holdings(self):
        store = load("store_sup_test", FLEET / "store.py")
        conn = sqlite3.connect(":memory:")
        self.addCleanup(conn.close)
        conn.executescript(store.SCHEMA)
        store.setup_snapshot(conn)
        conn.execute(
            "INSERT INTO supply_chains (chain, item, place, keep, need_per_hour, sources, keeper, note, line, error, src) "
            "VALUES ('outpost-fuel', 'fuel', 'CLTV Outpost GSC-0044', 5000, 0.0, '', 'Logistics', '', 1, NULL, 'supply.tsv')"
        )
        conn.execute(
            "INSERT INTO supply_chains (chain, item, place, keep, need_per_hour, sources, keeper, note, line, error, src) "
            "VALUES ('steel-check', 'steel_plate', 'CLTV Outpost GSC-0044', 100, 0.0, '', 'Logistics', '', 2, NULL, 'supply.tsv')"
        )
        # Fuel bunker lives ONLY in faction_storage (not in holdings)
        conn.execute(
            "INSERT INTO faction_storage (base, base_name, item, units, t, src) "
            "VALUES ('base_hex_1', 'CLTV Outpost GSC-0044', 'fuel', 4547, 100, 'empire.json')"
        )
        # Non-fuel steel_plate lives in BOTH faction_storage AND holdings (pilot='Faction') -> must NOT double-count
        conn.execute(
            "INSERT INTO faction_storage (base, base_name, item, units, t, src) "
            "VALUES ('base_hex_1', 'CLTV Outpost GSC-0044', 'steel_plate', 250, 100, 'empire.json')"
        )
        conn.execute(
            "INSERT INTO holdings (pilot, member, place, item, units, t, src) "
            "VALUES ('Faction', 'Faction', 'base_hex_1', 'steel_plate', 250, 100, 'storage.json')"
        )
        conn.execute("INSERT INTO holdings (pilot, member, place, item, units, t, src) VALUES ('hauler-1', 'Apollo', 'CLTV Outpost GSC-0044', 'steel_plate', 50, 100, 'storage.json')")
        conn.commit()
        rows = {r[0]: (r[1], r[2]) for r in conn.execute("SELECT chain, stock, status FROM supply_status")}
        self.assertEqual(rows["outpost-fuel"], (4547, "short"))
        # 50 from hauler-1 at base_name; Faction row at base_hex_1 is deduped against faction_storage at base_hex_1 (or counted once via holdings/faction_storage)
        self.assertEqual(rows["steel-check"][0], 300)  # 250 Faction (once, not 500) + 50 hauler-1


class WalletRoleCapTests(unittest.TestCase):
    def test_role_aware_sweep_caps_traders_keep_50k_workers_keep_30k(self):
        wallet = load("wallet_upg_test", FLEET / "wallet.py")
        fleet = {
            "Prime Directive": {"credits": 40000, "status": "connected"},
            "trader-1": {"credits": 58000, "status": "connected"},   # under 60k -> NOT swept
            "trader-2": {"credits": 75000, "status": "connected"},   # >= 60k -> sweeps 25k (keeps 50k)
            "miner-1": {"credits": 39999, "status": "connected"},    # under 40k -> NOT swept
            "miner-2": {"credits": 52000, "status": "connected"},    # >= 40k -> sweeps 22k (keeps 30k)
            "drone-1": {"credits": 45000, "status": "connected"},    # >= 40k -> sweeps 15k (keeps 30k)
        }
        named = {"Prime Directive": {"role": "command"}}
        plan = wallet.plan_sweep(fleet, "Prime Directive", set(), named)
        self.assertEqual(plan, [("trader-2", 25000), ("miner-2", 22000), ("drone-1", 15000)])


class StorePublicFeedsAndStationOpsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="collective-upg-ops-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "fleet").mkdir()
        (self.base / "station").mkdir()
        (self.base / "store").mkdir()

    def test_store_reads_battles_and_both_leaderboard_formats(self):
        store = load("store_feed_test", FLEET / "store.py")
        b_path = self.base / "station" / "battles.json"
        b_path.write_text(json.dumps([{"system": "alcyone", "system_name": "Alcyone", "category": "pvp", "status": "active",
                                       "tick": 99, "destroyed": 2, "lost": ["A"], "pilots": ["P1"], "tags": ["HOST"], "ended_at": ""}]))
        got_b = store.read_battles(b_path, {})
        self.assertEqual(len(got_b["public_battles"]), 1)
        self.assertEqual(got_b["public_battles"][0]["category"], "pvp")

        # Raw /api/leaderboard format (no "groups" wrapper)
        l_path = self.base / "station" / "leaderboard.json"
        l_path.write_text(json.dumps({"generated_at": "2026-11-22T01:00:00Z",
                                      "players": {"total_wealth": [{"rank": 1, "username": "Alpha", "empire": "voidborn", "value": 999}]}}))
        got_l = store.read_leaderboards(l_path, {})
        self.assertEqual(len(got_l["leaderboards"]), 1)
        self.assertEqual((got_l["leaderboards"][0]["grp"], got_l["leaderboards"][0]["name"], got_l["leaderboards"][0]["tag"]),
                         ("players", "Alpha", "voidborn"))

    def test_station_api_ops_returns_structured_json(self):
        server = load("station_ops_test", STATION / "server.py")
        server.FLEET = self.base / "fleet"
        server.DATA = self.base / "station"
        server.OPS = {"at": 0.0, "value": None}
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 10))
        (self.base / "fleet" / "fleet.json").write_text(json.dumps({"ships": [
            {"name": "miner-1", "division": "Mining", "credits": 45000, "state_at": now_iso},
            {"name": "trader-1", "division": "Trade", "credits": 55000, "state_at": now_iso},
        ]}))
        res = server.api_ops()
        self.assertEqual(res["freshness"]["ships"], 2)
        self.assertLessEqual(res["freshness"]["max_s"], 15)
        self.assertEqual(res["readiness"]["sweepable"], {"ships": 1, "credits": 15000})
        for key in ("freshness", "readiness", "supply", "needs", "alerts", "services"):
            self.assertIn(key, res)


if __name__ == "__main__":
    unittest.main()
