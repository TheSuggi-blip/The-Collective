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
        self.assertEqual(self.dispatch.circuit_systems(route), ["safe_sys", "hot_sys"])     # each stop's own system too (requests ENT-312)
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



class DispatchPairsCacheAndBriefingEyesTests(unittest.TestCase):
    def test_pairs_cache_indexes_runs_once_in_o1(self):
        dispatch = load("dispatch_pairs_test", FLEET / "dispatch.py")
        now = time.time()
        rows = [
            {"route": "trade-x", "pilot": "trader-9", "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 180 + i * 30)),
             "minutes": 0.2, "delta": 0, "notes": []}
            for i in range(5)
        ]
        by = dispatch.pairs(rows)
        self.assertIs(dispatch.pairs(rows), by)
        self.assertEqual(len(by[("trade-x", "trader-9")]), 5)
        pilot = {"name": "trader-9", "role": "trader", "credits": 45000, "docked": True, "modules": [], "skills": {}, "goods": 0}
        route = {"id": "trade-x", "kind": "trade", "buy_at": "a:b", "sell_at": "c:d"}
        state = {"now": now, "data": "", "rows": rows, "orders": {}, "rest": {}, "booked": {}, "loss": {}, "late": {}, "pirates": {}}
        reason, _ = dispatch.why_not(pilot, "trade-x", route, state)
        self.assertIsNotNone(reason)
        self.assertIn("short zero-credit runs", reason)

    def test_hive_show_eyes_prints_priorities_supply_bottlenecks_and_raids(self):
        import contextlib, io
        store = load("store_eyes_test", FLEET / "store.py")
        hive = load("hive_eyes_test", FLEET / "hive.py")
        with tempfile.TemporaryDirectory(prefix="hive-eyes-test-") as tmp:
            base = Path(tmp)
            (base / "store").mkdir()
            conn = sqlite3.connect(str(base / "store" / "read.db"))
            conn.executescript(store.SCHEMA)
            store.setup_snapshot(conn)
            conn.execute("INSERT INTO faction (id, name, tag, leader, member_count, members_limit, treasury, owned_bases, at_war, created, t, src) "
                         "VALUES ('f1', 'The Collective', 'CLTV', 'Prime Directive', 99, 100, 800000, 1, 0, 1, 100, 'empire.json')")
            conn.execute("INSERT INTO ships (pilot, division, role, class, t, src) VALUES ('miner-1', 'Mining', 'miner', 'Threshold', 100, 'fleet.json')")
            conn.execute("INSERT INTO ship_skills (pilot, skill, level, xp, src) VALUES ('miner-1', 'piloting', 11, 500, 'ships')")
            conn.execute("INSERT INTO supply_chains (chain, item, place, keep, need_per_hour, sources, keeper, note, line, error, src) "
                         "VALUES ('outpost-fuel', 'fuel', 'CLTV Outpost', 5000, 0.0, '', 'Logistics', '', 1, NULL, 'supply.tsv')")
            conn.execute("INSERT INTO public_battles (system, system_name, category, status, tick, destroyed, lost, pilots, tags, ended_at, t, src) "
                         "VALUES ('algol', 'Algol', 'npc', 'active', 999, 2, 'Outpost', 'Raider', 'NPC', '', 100, 'battles.json')")
            conn.commit()
            conn.close()
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                hive.show_eyes(str(base), "Zero")
            out = buf.getvalue()
            self.assertIn("=== EYES & EARS:", out)
            self.assertIn("seats 99/100 (AT CAP", out)
            self.assertIn("MY UPGRADE READINESS (Mining)", out)
            self.assertIn("1 ships >= Lv10 ready for T2 hulls", out)
            self.assertIn("outpost-fuel", out)
            self.assertIn("RAID / PVP BATTLES", out)
            self.assertIn("Algol [npc/active", out)




class WatchdogTests(unittest.TestCase):
    def test_watchdog_detects_fast_zero_loops_ready_needs_and_velocity(self):
        import sqlite3
        import tempfile
        import watchdog

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            (root / "game").mkdir(parents=True)
            (root / "communications").mkdir(parents=True)
            (root / "communications" / "requests.log").write_text(
                "## [ENT-001] | 2026-11-21 18:00 UTC | Zero | request | ref: game/needs.tsv\n@Unity need site approval\n",
                encoding="ascii",
            )
            (root / "communications" / "errors.log").write_text("", encoding="ascii")
            data = Path(tmp) / "data"
            (data / "services").mkdir(parents=True)
            (data / "store").mkdir(parents=True)
            (data / "services" / "status.json").write_text(
                json.dumps({s: {"state": "running"} for s in watchdog.CORE_SERVICES}),
                encoding="ascii",
            )

            now = 1795315200.0  # 2026-11-22 02:40:00 UTC
            db = data / "store" / "read.db"
            con = sqlite3.connect(str(db))
            con.executescript(
                """
                CREATE TABLE ships (pilot TEXT, division TEXT, role TEXT, class TEXT, status TEXT, activity TEXT, flies TEXT, credits INTEGER, t INTEGER);
                CREATE TABLE runs (pilot TEXT, route TEXT, kind TEXT, t INTEGER, minutes REAL, credits REAL);
                CREATE TABLE faction (treasury INTEGER, member_count INTEGER, members_limit INTEGER, owned_bases INTEGER);
                CREATE TABLE faction_facilities (id TEXT);
                CREATE TABLE places (system TEXT, poi TEXT);
                CREATE TABLE stats_figures (view TEXT, subject TEXT, figure TEXT, hours REAL, value REAL, text TEXT);
                CREATE TABLE need_status (id TEXT, rank INTEGER, project TEXT, division TEXT, priority INTEGER, kind TEXT, ref TEXT, covered REAL, fee INTEGER, stands INTEGER, short_items TEXT, gather TEXT, buy TEXT, craft TEXT);
                CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INTEGER);
                CREATE TABLE ship_modules (pilot TEXT, module TEXT);
                CREATE TABLE supply_status (chain TEXT, place TEXT, status TEXT, stock INTEGER, keep INTEGER, hours_left REAL);
                """
            )
            con.execute("INSERT INTO ships VALUES ('trader-1','trade','trader','Threshold','active','docked','bad-loop',55000,?)", (int(now - 10),))
            con.execute("INSERT INTO ships VALUES ('miner-1','mining','miner','Prospect','active','mining','mine-iron',40000,?)", (int(now - 12),))
            for i in range(5):
                con.execute("INSERT INTO runs VALUES ('trader-1','bad-loop','circuit',?,0.4,0.0)", (int(now - 600 + i * 60),))
            con.execute("INSERT INTO faction VALUES (2500000, 99, 100, 2)")
            con.execute("INSERT INTO faction_facilities VALUES ('fac-1')")
            con.execute("INSERT INTO places VALUES ('SYS-1','POI-1')")
            con.execute("INSERT INTO stats_figures VALUES ('kpi','fleet','steady_net_per_hour',24,42000,'')")
            con.execute("INSERT INTO need_status VALUES ('rec-center',1,'Cap','command',1,'facility','recruitment_office',1.0,2000000,0,'','','','')")
            con.execute("INSERT INTO need_status VALUES ('stalled-hull',2,'Hull','mining',1,'hull','prospect',0.50,0,0,'20 silicon','','','')")
            con.execute("INSERT INTO ship_skills VALUES ('trader-1','piloting',22)")
            con.execute("INSERT INTO ship_modules VALUES ('miner-1','mining_laser_iii')")
            con.execute("INSERT INTO supply_status VALUES ('outpost-fuel','GSC-0044','OK',4600,5000,120.0)")
            con.commit()
            con.close()

            r1 = watchdog.inspect(root / "game", data, hours=4.0, now=now - 5 * 3600.0, save=True)
            self.assertIsNone(r1["velocity"])
            r2 = watchdog.inspect(root / "game", data, hours=4.0, now=now, save=True)
            codes = {f["code"] for f in r2["findings"]}
            self.assertIn("FAST_ZERO_WARN", codes)
            self.assertIn("NEED_READY_NOW", codes)
            self.assertIn("FACTION_CAP_NEAR", codes)
            self.assertIn("P1_NEED_STALLED", codes)
            self.assertIn("OVERDUE_REQUESTS", codes)
            self.assertIsNotNone(r2["velocity"])
            self.assertAlmostEqual(r2["velocity"]["dt_hours"], 5.0, places=1)




class TradeRunAndAgilityTests(unittest.TestCase):
    def test_route_run_active_parses_both_hex_and_named_trade_run_ids(self):
        import ast, re
        src = (Path(__file__).resolve().parents[2] / "game" / "fleet" / "route_run.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        fn_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "active")
        ns = {
            "re": re,
            "verbose": False,
            "say": lambda *a: None,
            "text": lambda d: d["text"],
            "raw": lambda *a, **kw: {
                "text": (
                    "--- Say Hello [0123456789abcdef0123456789abcdef]\nObjectives:\n- Visit Nexus [DONE]\nRewards: 1000\n"
                    "--- Trade Run: Precision Optic to Market Prime [trade_alpha_centauri_market_prime_precision_optic]\n"
                    "Objectives:\n- Sell 1 Precision Optic [DONE]\nRewards: 260 XP\n"
                )
            },
        }
        exec(compile(ast.Module(body=[fn_node], type_ignores=[]), "<route_run.active>", "exec"), ns)
        got = ns["active"]()
        self.assertEqual(len(got), 2)
        self.assertEqual(got[0], ("Say Hello", "0123456789abcdef0123456789abcdef", True))
        self.assertEqual(got[1], ("Trade Run: Precision Optic to Market Prime", "trade_alpha_centauri_market_prime_precision_optic", True))

    def test_routemaker_synthesizes_xp_trade_run_with_named_mission_id(self):
        import routemaker
        world = {
            "now": 1795320000.0,
            "pilots": 40,
            "routes": {},
            "booked": {},
            "items": {"precision_optic": {"name": "Precision Optic", "size": 1}},
            "fields": [],
            "herds": [],
            "stock": {},
            "stations": {
                "alpha_base": {"at": "alpha:p1:alpha_base", "name": "Alpha Base", "system": "alpha"},
                "prime_base": {"at": "prime:p2:prime_base", "name": "Prime Exchange", "system": "prime"},
            },
            "books": {
                "alpha_base": {"items": {"precision_optic": {"ask": 400, "ask_qty": 10, "bid": 0, "bid_qty": 0}}},
                "prime_base": {"items": {"precision_optic": {"ask": 0, "ask_qty": 0, "bid": 650, "bid_qty": 10}}},
            },
            "boards": {
                "alpha_base": {
                    "system": "alpha",
                    "read_at": 1795319900.0,
                    "missions": [{
                        "template_id": None,
                        "mission_id": "trade_alpha_prime_optic",
                        "title": "Trade Run: Precision Optic to Prime",
                        "type": "trading",
                        "rewards": {"credits": 0, "skill_xp": {"trading": 40}, "piloting_xp": 260},
                        "objectives": [{"type": "sell_item", "system_id": "prime", "target_base_id": "prime_base", "item_id": "precision_optic", "quantity": 2}],
                    }],
                }
            },
            "assume": {
                "jump_minutes": {"value": 0.5},
                "dock_minutes": {"value": 0.5},
                "leg_minutes": {"value": 0.5},
                "fuel_per_jump": {"value": 2.0},
                "fuel_price": {"value": 5.0},
                "tax": {"value": 0.01},
            },
            "strongholds": set(),
            "player_fees": {},
            "chart": type("C", (), {"jumps": staticmethod(lambda a, b: 3 if a != b else 0), "systems": {"alpha": {"empire": "voidborn"}, "prime": {"empire": "voidborn"}}})(),
        }
        cands = routemaker.mission_candidates(world)
        self.assertEqual(len(cands), 1)
        c = cands[0]
        self.assertEqual(c["xp"], 300)
        self.assertIsNotNone(c["route"])
        self.assertNotIn("once", c["route"])
        # Stop 0 buys at alpha_base, Stop 1 accepts mission_id, Stop 2 sells at prime_base
        self.assertEqual(c["route"]["stops"][1]["accept"][0]["template"], "trade_alpha_prime_optic")
        self.assertEqual(c["route"]["stops"][2]["sell"][0]["item"], "precision_optic")


if __name__ == "__main__":
    unittest.main()
