import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "game" / "fleet"))
import scorecard


def _make_fixture(tmp):
    root = Path(tmp) / "repo"
    data = Path(tmp) / "data"
    (root / "communications").mkdir(parents=True)
    (data / "store").mkdir(parents=True)
    (data / "fleet").mkdir(parents=True)
    (data / "comms").mkdir(parents=True)

    (root / "communications" / "requests.log").write_text(
        "## [ENT-001] | 2026-11-23 01:00 UTC | Mercury | request | ref: x\nTo: Unity.\nNeed: test.\n",
        encoding="ascii",
    )
    (data / "comms" / "diplomacy.json").write_text(
        json.dumps({"factions": {"HEXC": {"status": "neutrality_agreed", "last_inbound_at": "2026-11-23T04:00:00Z", "last_outbound_at": "2026-11-23T05:00:00Z"}}}),
        encoding="ascii",
    )
    (data / "fleet" / "fleet.json").write_text(
        json.dumps({
            "updated_at": "2026-11-23T05:30:00Z",
            "ships": [
                {"name": "Prime Directive", "division": "Command", "status": "working", "credits": 50000, "docked": False},
                {"name": "miner-1", "division": "Mining", "status": "working", "credits": 20000, "docked": False},
                {"name": "miner-2", "division": "Mining", "status": "waiting", "credits": 20000, "docked": True},
                {"name": "trader-1", "division": "Trade", "status": "working", "credits": 40000, "docked": False},
                {"name": "hauler-1", "division": "Logistics", "status": "waiting", "credits": 15000, "docked": True},
                {"name": "drone-1", "division": "Military", "status": "working", "credits": 25000, "docked": False},
                {"name": "scout-1", "division": "Intel", "status": "waiting", "credits": 10000, "docked": True},
            ],
        }),
        encoding="ascii",
    )
    (data / "fleet" / "watchdog.state.json").write_text(
        json.dumps({
            "last": {"epoch": 1795410000, "total_money": 13500000, "p10_pilots": 80, "t2_hulls": 0, "idle_ships": 100},
            "history": [{"epoch": 1795388400, "total_money": 10500000, "p10_pilots": 60, "t2_hulls": 0, "idle_ships": 120}],
        }),
        encoding="ascii",
    )

    conn = sqlite3.connect(str(data / "store" / "read.db"))
    conn.executescript("""
        CREATE TABLE faction (member_count INT, members_limit INT, treasury INT);
        INSERT INTO faction VALUES (2, 7, 1900000);
        CREATE TABLE hulls (id TEXT, name TEXT, tier INT, weapon_slots INT, defense_slots INT, utility_slots INT);
        INSERT INTO hulls VALUES ('starter', 'Threshold', 0, 1, 1, 2);
        INSERT INTO hulls VALUES ('t2_miner', 'Resonance Miner', 2, 2, 2, 3);
        CREATE TABLE ships (pilot TEXT, division TEXT, class TEXT, empire TEXT, credits INT);
        INSERT INTO ships VALUES
            ('Prime Directive', 'Command', 'starter', 'voidborn', 50000),
            ('miner-1', 'Mining', 'starter', 'voidborn', 20000),
            ('miner-2', 'Mining', 'starter', 'solarian', 20000),
            ('trader-1', 'Trade', 'starter', 'nebula', 40000),
            ('hauler-1', 'Logistics', 'starter', 'outerrim', 15000),
            ('drone-1', 'Military', 'starter', 'crimson', 25000),
            ('scout-1', 'Intel', 'starter', 'voidborn', 10000);
        CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INT);
        INSERT INTO ship_skills VALUES
            ('Prime Directive', 'piloting', 10),
            ('miner-1', 'piloting', 11),
            ('miner-2', 'piloting', 5),
            ('trader-1', 'piloting', 9),
            ('hauler-1', 'piloting', 8),
            ('drone-1', 'piloting', 10),
            ('scout-1', 'piloting', 10);
        CREATE TABLE ship_modules (pilot TEXT, module TEXT);
        INSERT INTO ship_modules VALUES
            ('miner-1', 'mining_laser_ii'),
            ('miner-1', 'pulse_laser_i'),
            ('trader-1', 'mining_laser_i'),
            ('drone-1', 'pulse_laser_ii');
        CREATE TABLE stats_money_hour (hour INT, division TEXT, income REAL, costs REAL, net REAL, total REAL);
        INSERT INTO stats_money_hour VALUES
            (1795400000, 'Fleet', 80000, 140000, -60000, 120000),
            (1795300000, 'Fleet', 90000, 75000, 15000, 100000),
            (1795400000, 'Trade', 45000, 20000, 25000, 30000),
            (1795300000, 'Trade', 20000, 22000, -2000, 10000),
            (1795400000, 'Mining', 10000, 25000, -15000, -15000);
        CREATE TABLE stats_figures (view TEXT, subject TEXT, figure TEXT, hours REAL, value REAL);
        INSERT INTO stats_figures VALUES
            ('kpi', 'Fleet', 'net', 24, -60000),
            ('kpi', 'Fleet', 'net', 6, -95000),
            ('kpi', 'Fleet', 'net', 1, -80000),
            ('kpi', 'Fleet', 'total', 24, 140000),
            ('kpi', 'Fleet', 'wallets', 24, 11000000),
            ('kpi', 'Fleet', 'treasury', 24, 1900000),
            ('kpi', 'Fleet', 'surplus_worth', 24, 380000),
            ('contribution', 'Mining', 'ore_per_ship_hour', 24, 18.5),
            ('contribution', 'Mining', 'handed_over_worth', 24, 120000),
            ('contribution', 'Trade', 'sell_cph', 24, 12000),
            ('contribution', 'Military', 'combat_xp_per_ship_hour', 24, 22.0),
            ('contribution', 'Military', 'kills', 24, 55),
            ('contribution', 'Military', 'ships_lost', 24, 0);
        CREATE TABLE fuel_sinks (category TEXT, ship_hours_24h REAL, net_credits_24h REAL);
        INSERT INTO fuel_sinks VALUES ('productive', 3000, 200000), ('jump_loops', 1500, -700000), ('census', 500, -400000);
        CREATE TABLE supply_status (chain TEXT, item TEXT, status TEXT, stock REAL, keep REAL);
        INSERT INTO supply_status VALUES ('fuel-a', 'fuel_cell', 'OK', 5000, 5000), ('core-a', 'station_core', 'SHORT', 0, 1);
        CREATE TABLE need_status (id TEXT, priority INT, division TEXT, covered REAL, short_items TEXT, fee INT);
        INSERT INTO need_status VALUES ('atria-outpost-kit', 1, 'logistics', 92.3, 'foil_scale 630', 0);
        CREATE TABLE division_playbooks (division TEXT, max_chapter_pct REAL, open_needs INT, ready_needs INT);
        INSERT INTO division_playbooks VALUES ('mining', 98.5, 1, 0), ('trade', 80.0, 0, 0);
        CREATE TABLE places (system TEXT, t INT);
        INSERT INTO places VALUES ('s1', 1795409000), ('s2', 1795300000);
    """)
    conn.commit()
    conn.close()
    return root, data


class TestFleetScorecard(unittest.TestCase):
    def test_triggers_fire_below_80_and_detect_cashflow_direction(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            sc = scorecard.compute_scorecard(root, data, now=1795410000)
            ent = sc["enterprise"]
            self.assertEqual(ent["cashflow_sign"], "NEGATIVE")
            self.assertEqual(ent["cashflow_trend_24h"], "WORSENING")
            self.assertEqual(ent["verdict"], "GROWING_WITH_DRAG")
            self.assertLess(ent["productive_pct"], 80.0)
            self.assertEqual(ent["open_requests"], 1)
            codes = {t["code"] for t in ent["triggers"]}
            self.assertIn("CASHFLOW_NEGATIVE", codes)
            self.assertIn("PRODUCTIVE_EFFICIENCY", codes)
            self.assertIn("OPEN_SEATS", codes)
            self.assertIn("HULL_UPGRADE_LAG", codes)

            # Mining: 1 P10+ pilot on T0 -> 0% eligible hull upgrade ALARM, 1/2 working -> 50% ALARM, playbook 98.5% ALARM
            mining = sc["divisions"]["Mining"]
            m_codes = {t["code"] for t in mining["triggers"]}
            self.assertIn("DIV_HULL_UPGRADE", m_codes)
            self.assertIn("DIV_IDLE", m_codes)
            self.assertIn("PLAYBOOK_CAP", m_codes)

            # Trade: positive & improving cashflow, 0 P10+ pilots -> uses piloting_to_t2 mode
            trade = sc["divisions"]["Trade"]
            self.assertEqual(trade["trend_24h"], "IMPROVING")
            self.assertEqual(trade["hulls"]["mode"], "piloting_to_t2")

            # Intel: unassigned parked scout counts honestly as IDLE (0% working -> DIV_IDLE + INTEL_FRESHNESS)
            intel = sc["divisions"]["Intel"]
            self.assertEqual(intel["employment"]["pct"], 0.0)
            i_codes = {t["code"] for t in intel["triggers"]}
            self.assertIn("DIV_IDLE", i_codes)
            self.assertIn("INTEL_FRESHNESS", i_codes)

    def test_render_briefing_for_admiral_and_unity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            sc = scorecard.compute_scorecard(root, data, now=1795410000)
            out_zero = scorecard.render_briefing(sc, who="Zero")
            self.assertIn("MY DIVISION (Mining / Zero)", out_zero)
            self.assertIn("ACTIVE TRIGGERS", out_zero)
            self.assertIn("GROWING_WITH_DRAG", out_zero)

            out_unity = scorecard.render_briefing(sc, who="Unity")
            self.assertIn("DIVISIONS", out_unity)
            self.assertIn("TOP FLEET TRIGGERS", out_unity)
            self.assertIn("Logistics", out_unity)


    def test_weighted_triage_ranks_p0_before_p3_and_includes_reqs_and_quick_needs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            sc = scorecard.compute_scorecard(root, data, now=1795410000)
            ent = sc["enterprise"]
            self.assertGreaterEqual(ent["weighted_score"], 0.0)
            self.assertLessEqual(ent["weighted_score"], 100.0)
            self.assertTrue(ent["triage"])
            ranks = [(scorecard.TIER_RANK[x["tier"]], -x["score"]) for x in ent["triage"]]
            self.assertEqual(ranks, sorted(ranks))
            ent_codes = {x["code"] for x in ent["triage"]}
            cmd_codes = {x["code"] for x in sc["divisions"]["Command"]["triage"]}
            self.assertIn("REQ_ENT-001", ent_codes)
            self.assertIn("REQ_ENT-001", cmd_codes)
            log_triage = sc["divisions"]["Logistics"]["triage"]
            atria = [x for x in log_triage if x["code"] == "NEED_atria-outpost-kit"]
            self.assertEqual(len(atria), 1)
            self.assertEqual(atria[0]["tier"], "P1")
            self.assertEqual(atria[0]["effort"], 1)
            self.assertGreaterEqual(atria[0]["score"], 85)
            m_triage = sc["divisions"]["Mining"]["triage"]
            m_idx = {x["code"]: i for i, x in enumerate(m_triage)}
            self.assertLess(m_idx["DIV_IDLE"], m_idx["PLAYBOOK_CAP"])


    def test_war_alert_posture_auto_shifts_weights_and_pins_p0_war_top(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            (data / "empire").mkdir(parents=True, exist_ok=True)
            (data / "empire" / "empire.json").write_text(
                json.dumps({"faction": {"at_war": True}, "relations": {"wars": ["ENDL"], "enemies": ["ENDL"]}}),
                encoding="ascii",
            )
            sc = scorecard.compute_scorecard(root, data, now=1795410000)
            ent = sc["enterprise"]
            self.assertEqual(ent["posture"], "WAR_ALERT")
            self.assertTrue(ent["war"]["at_war"])
            self.assertEqual(ent["weights"]["war_readiness"], 40)
            self.assertEqual(ent["triage"][0]["code"], "ACTIVE_WAR")
            self.assertEqual(ent["triage"][0]["tier"], "P0")
            self.assertEqual(ent["triage"][0]["score"], 100)
            self.assertEqual(sc["divisions"]["Military"]["triage"][0]["code"], "ACTIVE_WAR")


    def test_strategy_kpis_auto_integrate_rank_and_drop_on_completion_or_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            rv_mock = {
                "strategy_playbooks": [
                    {
                        "id": "express_passenger", "name": "4. Express Pax", "short_name": "Express Pax",
                        "divisions": ["Logistics"], "status_code": "GAP", "readiness_pct": 25.0,
                        "matched_count": 1, "total_count": 4, "empires": [{"name": "Outer Rim", "ships": 43}],
                        "effort": 1, "posture_weights": {"WAR_ALERT": 40, "CASHFLOW_RECOVERY": 92, "PEACETIME_GROWTH": 84},
                        "how_to_copy": "Commission Runner hulls", "blocker": "Fast hulls",
                        "kpis": [
                            {"name": "Fast hulls", "owner": "Logistics", "current": "0", "target": ">=5", "matched": False, "source": "fleet.json"},
                            {"name": "Supply chain: outpost-fuel", "owner": "Logistics", "current": "100/5000", "target": ">=5000", "matched": False, "source": "read.db:supply"},
                        ],
                    },
                    {
                        "id": "pve_combat", "name": "8. PvE & Escort", "short_name": "PvE & Escort",
                        "divisions": ["Military"], "status_code": "PARTIAL", "readiness_pct": 50.0,
                        "matched_count": 2, "total_count": 4, "empires": [{"name": "Crimson", "ships": 41}],
                        "effort": 2, "posture_weights": {"WAR_ALERT": 100, "CASHFLOW_RECOVERY": 60, "PEACETIME_GROWTH": 80},
                        "how_to_copy": "Field T2 combat hulls", "blocker": "T2 warships",
                        "kpis": [
                            {"name": "T2 warships", "owner": "Military", "current": "0", "target": ">=5", "matched": False, "source": "read.db:ships"},
                        ],
                    },
                ]
            }
            sc1 = scorecard.compute_scorecard(root, data, now=107200, rivals_doc=rv_mock)
            log_codes_1 = [x["code"] for x in sc1["divisions"]["Logistics"]["triage"]]
            self.assertTrue(any(c.startswith("STRAT_express_passenger_") for c in log_codes_1))
            self.assertTrue(any(x["source"] == "SUPPLY" for x in sc1["divisions"]["Logistics"]["triage"]))
            # Under CASHFLOW_RECOVERY, Express Pax (wt 92, eff 1) outranks PvE Combat (wt 60, eff 2)
            self.assertEqual(rv_mock["strategy_playbooks"][0]["id"], "express_passenger")

            # Mark both Logistics KPIs completed & remove pve_combat strategy -> both auto-drop from triage!
            for k in rv_mock["strategy_playbooks"][0]["kpis"]:
                k["matched"] = True
            rv_mock["strategy_playbooks"][0]["readiness_pct"] = 100.0
            rv_mock["strategy_playbooks"][0]["matched_count"] = 2
            rv_mock["strategy_playbooks"] = [rv_mock["strategy_playbooks"][0]]
            sc2 = scorecard.compute_scorecard(root, data, now=107200, rivals_doc=rv_mock)
            self.assertFalse(any(x["source"] in ("STRATEGY", "SUPPLY") for x in sc2["divisions"]["Logistics"]["triage"]))
            self.assertEqual(sc2["divisions"]["Military"]["playbooks"], [])

    def test_supply_low_at_keep_offrole_slot_and_closing_diplo_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            # Add supply_status with LOW (stock >= keep) and verify it counts as OK at keep
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.execute("CREATE TABLE IF NOT EXISTS supply_status (chain TEXT, item TEXT, status TEXT, stock REAL, keep REAL)")
            con.execute("DELETE FROM supply_status")
            con.execute("INSERT INTO supply_status VALUES ('outpost-fuel', 'fuel', 'low', 5480, 5000)")
            con.execute("INSERT INTO supply_status VALUES ('iron-ore', 'iron_ore', 'ok', 100000, 60000)")
            # Add a military ship with 1 role-matched weapon + 1 off-role mining_laser_i
            con.execute("INSERT OR REPLACE INTO hulls (id, name, tier, weapon_slots, defense_slots, utility_slots) VALUES ('shard', 'Shard', 0, 2, 1, 1)")
            con.execute("INSERT OR REPLACE INTO ships (pilot, division, class) VALUES ('drone-99', 'Military', 'Shard')")
            con.execute("DELETE FROM ship_modules WHERE pilot = 'drone-99'")
            con.execute("INSERT INTO ship_modules (pilot, module) VALUES ('drone-99', 'pulse_laser_i')")
            con.execute("INSERT INTO ship_modules (pilot, module) VALUES ('drone-99', 'mining_laser_i')")
            con.commit()
            con.close()

            # Add tracked neutral partner IRLC with a polite closing ack containing sanitized em-dash " ? "
            (data / "comms").mkdir(parents=True, exist_ok=True)
            (data / "comms" / "diplomacy.json").write_text(json.dumps({
                "factions": {
                    "IRLC": {
                        "tag": "IRLC", "leader": "ILC Comptroller", "status": "neutrality_agreed",
                        "last_sent_at": "2026-11-23T20:17:04Z",
                    }
                }
            }))
            (data / "comms" / "messages.jsonl").write_text(json.dumps({
                "t": "2026-11-23T20:26:50Z", "channel": "private", "own": False,
                "sender": "ILC Comptroller", "tag": "IRLC",
                "text": "Likewise, Unity. The Crossroads book is open ? see you on the exchange. ? Comptroller",
            }) + "\n")

            sc = scorecard.compute_scorecard(root, data, now=107200, rivals_doc={"strategy_playbooks": []})
            # 1) LOW supply chain (5480/5000) satisfies keep -> 2/2 OK (100%), no SUPPLY_CHAINS trigger
            self.assertIn("chains 2/2 OK", sc["divisions"]["Logistics"]["role_kpi"]["value"])
            self.assertFalse(any(t["code"] == "SUPPLY_CHAINS" for t in sc["divisions"]["Logistics"]["triggers"]))
            # 2) Closing ack from neutral partner does NOT trigger DIPLO_PENDING
            self.assertEqual(sc["enterprise"].get("diplo_pending", 0), 0)
            # 3) Off-role mining_laser_i on drone-99 is excluded from fitted_slots while still counted in off_role_ships
            mil_mods = sc["divisions"]["Military"]["modules"]
            self.assertGreaterEqual(mil_mods["off_role_ships"], 1)
            # 4) Unified 3-metric strip renders Purse/h, Recur/h, Accrual/h
            txt = scorecard.render_briefing(sc, "Unity")
            self.assertIn("Purse/h", txt)
            self.assertIn("Recur/h", txt)
            self.assertIn("Accrual/h", txt)


    def test_gap_to_goal_deficits_and_field_congestion_saturation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            # Create a mining route + 22 active orders stacked on one belt + a stacked non-depleting bursar desk
            rdir = Path(root) / "game" / "routes"
            rdir.mkdir(parents=True, exist_ok=True)
            (rdir / "mine-crowded.json").write_text(json.dumps({"id": "mine-crowded", "kind": "mine", "belt": "hamal:hamal_crystal_bloom"}), encoding="ascii")
            (rdir / "bursar-desk.json").write_text(json.dumps({"id": "bursar-desk", "kind": "circuit", "stops": [{"at": "krynn:s:b", "sell_order": []}]}), encoding="ascii")
            odir = Path(data) / "fleet" / "orders"
            odir.mkdir(parents=True, exist_ok=True)
            for i in range(1, 23):
                (odir / f"miner-{i}.json").write_text(json.dumps({"pilot": f"miner-{i}", "what": "mine mine-crowded"}), encoding="ascii")
            for i in range(1, 35):
                (odir / f"trader-{i}.json").write_text(json.dumps({"pilot": f"trader-{i}", "what": "circuit bursar-desk"}), encoding="ascii")

            sc = scorecard.compute_scorecard(root, data, now=1795410000)
            ent = sc["enterprise"]
            # Gap-to-goal deficit fields exist
            self.assertIn("idle_ships", ent)
            self.assertIn("hulls_missing_t2", ent)
            self.assertIn("empty_slots", ent)
            self.assertIn("unseated_ships", ent)
            # Mining field saturation triggers ALARM at 22/belt; Trade stacked desk never false-alarms
            msat = sc["divisions"]["Mining"]["saturation"]
            self.assertEqual(msat["max_per_poi"], 22)
            self.assertEqual(msat["status"], "ALARM")
            m_codes = {t["code"] for t in sc["divisions"]["Mining"]["triggers"]}
            self.assertIn("FIELD_CONGESTION", m_codes)
            self.assertIn("FIELD_CONGESTION", {t["code"] for t in ent["triggers"]})
            t_codes = {t["code"] for t in sc["divisions"]["Trade"]["triggers"]}
            self.assertNotIn("FIELD_CONGESTION", t_codes)
            # Briefing renders gap-to-goal burndown headers
            txt_u = scorecard.render_briefing(sc, who="Unity")
            self.assertIn("GAPS->0", txt_u)
            self.assertIn("HullGap", txt_u)
            self.assertIn("EmptySl", txt_u)
            txt_z = scorecard.render_briefing(sc, who="Zero")
            self.assertIn("Gaps->0", txt_z)
            self.assertIn("Field Saturation", txt_z)


    def test_responsibility_centers_trade_hub_saturation_and_optional_playbook_menu(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = _make_fixture(tmp)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                DROP TABLE IF EXISTS places;
                CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, base TEXT, t INT);
                CREATE TABLE IF NOT EXISTS systems (id TEXT, name TEXT, empire TEXT);
                CREATE TABLE IF NOT EXISTS books (base TEXT, system TEXT, item TEXT, bid REAL, bid_qty REAL, ask REAL, ask_qty REAL);
                CREATE TABLE IF NOT EXISTS stations (name TEXT, kind TEXT, system TEXT);
                INSERT INTO systems VALUES ('krynn', 'Krynn', 'crimson'), ('haven', 'Haven', 'nebula'), ('sol', 'Sol', 'solarian');
                INSERT INTO places VALUES ('krynn', 'p1', 'station', 'Krynn', 'crimson_war_citadel', 1795409000),
                                          ('haven', 'p2', 'station', 'Grand Exchange', 'grand_exchange_station', 1795409000),
                                          ('sol', 'p3', 'station', 'Sol', 'confederacy_central_command', 1795409000);
                INSERT INTO books VALUES ('crimson_war_citadel', 'krynn', 'ore', 10, 100, 12, 100),
                                         ('grand_exchange_station', 'haven', 'ore', 100, 5000, 110, 500),
                                         ('confederacy_central_command', 'sol', 'ore', 90, 4000, 100, 400);
                INSERT INTO stations VALUES ('Krynn', 'station', 'krynn'), ('Grand Exchange', 'station', 'haven'), ('Sol', 'station', 'sol');
            """)
            con.commit()
            con.close()

            rdir = Path(root) / "game" / "routes"
            rdir.mkdir(parents=True, exist_ok=True)
            (rdir / "bursar-desk-krynn.json").write_text(json.dumps({
                "id": "bursar-desk-krynn", "kind": "circuit", "max_ships": 20,
                "requires": {"docked_at": "crimson_war_citadel"},
                "stops": [{"at": "krynn:p1:crimson_war_citadel", "sell_order": [{"item": "ore", "qty": 10, "price": 12}], "watch_minutes": 15}],
            }), encoding="ascii")
            odir = Path(data) / "fleet" / "orders"
            odir.mkdir(parents=True, exist_ok=True)
            for i in range(1, 13):
                (odir / f"trader-{i}.json").write_text(json.dumps({"pilot": f"trader-{i}", "what": "circuit bursar-desk-krynn"}), encoding="ascii")

            rv_mock = {
                "strategy_playbooks": [{
                    "id": "pve_combat", "name": "8. PvE & Escort", "short_name": "PvE & Escort",
                    "divisions": ["Military"], "status_code": "GAP", "readiness_pct": 25.0,
                    "matched_count": 1, "total_count": 4, "empires": [{"name": "Crimson", "ships": 41}],
                    "effort": 2, "posture_weights": {"WAR_ALERT": 100, "CASHFLOW_RECOVERY": 70, "PEACETIME_GROWTH": 80},
                    "how_to_copy": "Field T2 combat hulls", "blocker": "T2 warships",
                    "kpis": [{"name": "T2 warships", "owner": "Military", "current": "0", "target": ">=5", "matched": False, "source": "read.db:ships"}],
                }]
            }
            sc = scorecard.compute_scorecard(root, data, now=1795410000, rivals_doc=rv_mock)
            # 1. Responsibility center metadata attached to every division
            self.assertEqual(sc["divisions"]["Mining"]["responsibility_center"]["short"], "Production")
            self.assertEqual(sc["divisions"]["Trade"]["responsibility_center"]["short"], "Profit Ctr")
            self.assertEqual(sc["divisions"]["Intel"]["responsibility_center"]["short"], "Cost Ctr")
            self.assertEqual(sc["divisions"]["Logistics"]["responsibility_center"]["short"], "Service/Infra")
            # 2. Trade Hub Saturation detects 12 Bursars stacked on Krynn with 2/3 policed hubs uncovered
            tsat = sc["divisions"]["Trade"]["saturation"]
            self.assertEqual(tsat["total_policed_hubs"], 3)
            self.assertEqual(tsat["covered_hubs"], 1)
            self.assertEqual(tsat["uncovered_hubs"], 2)
            self.assertEqual(tsat["max_per_poi"], 12)
            self.assertEqual(tsat["status"], "ALARM")
            self.assertIn("HUB_CONGESTION", {t["code"] for t in sc["divisions"]["Trade"]["triggers"]})
            self.assertIn("HUB_CONGESTION", {t["code"] for t in sc["enterprise"]["triggers"]})
            self.assertTrue(any("grand_exchange_station" in x for x in tsat["top_unserved"]))
            # 3. Military is 100% employed (0 idle) -> optional Playbook demotes to P3 MENU (not P1 WARN)
            mil_pb = [x for x in sc["divisions"]["Military"]["triage"] if x["code"].startswith("STRAT_pve_combat_")]
            self.assertEqual(len(mil_pb), 1)
            self.assertEqual(mil_pb[0]["tier"], "P3")
            self.assertEqual(mil_pb[0]["source"], "MENU")
            self.assertTrue(mil_pb[0]["optional"])
            # 4. routes.concentration_warnings catches Bursar max_ships > 3 and mine max_ships > 10
            import routes as _rt
            cw = _rt.concentration_warnings({
                "bursar-desk-krynn": {"kind": "circuit", "max_ships": 20, "requires": {"docked_at": "crimson_war_citadel"}, "stops": [{"at": "k:p:b", "sell_order": []}]},
                "bursar-ok": {"kind": "circuit", "max_ships": 2, "requires": {"docked_at": "sol"}, "stops": [{"at": "s:p:b", "sell_order": []}]},
                "mine-big": {"kind": "mine", "belt": "hamal:b", "max_ships": 40},
                "mine-ok": {"kind": "mine", "belt": "subra:b", "max_ships": 8},
            })
            cids = [rid for rid, _w in cw]
            self.assertEqual(cids, ["bursar-desk-krynn", "mine-big"])


    def test_smart_networks_fire_on_gaps_and_stay_silent_when_healthy(self):
        """Smart AutoNet notices fire on real gaps/disabled policies and stay completely silent when healthy."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (root / "game" / "routes").mkdir(parents=True, exist_ok=True)
            (data / "store").mkdir(parents=True, exist_ok=True)
            (data / "fleet" / "orders").mkdir(parents=True, exist_ok=True)
            (data / "plans").mkdir(parents=True, exist_ok=True)

            # Minimal SQLite store with ships, hulls, books, ship_listings, bases, systems
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE systems (id TEXT, empire TEXT, police_level INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, base TEXT, t INTEGER);
                CREATE TABLE bases (base TEXT, name TEXT, system TEXT, poi TEXT, kind TEXT, t INTEGER, src TEXT);
                CREATE TABLE hulls (id TEXT, name TEXT, tier INTEGER, cargo INTEGER, weapon_slots INTEGER, defense_slots INTEGER, utility_slots INTEGER);
                CREATE TABLE ships (pilot TEXT, division TEXT, empire TEXT, class TEXT, role TEXT, docked INTEGER);
                CREATE TABLE books (base TEXT, system TEXT, item TEXT, bid REAL, bid_qty INTEGER, ask REAL, ask_qty INTEGER, t INTEGER);
                CREATE TABLE ship_listings (id TEXT, base TEXT, hull TEXT, price REAL, t INTEGER);
                INSERT INTO hulls VALUES ('t0_skiff', 'Skiff', 0, 80, 1, 1, 1), ('t2_prayer', 'Prayer', 1, 540, 0, 1, 2);
                INSERT INTO systems VALUES ('s1', 'voidborn', 5), ('s2', 'solarian', 5);
                INSERT INTO bases VALUES ('b_vb', 'VB Station', 's1', 'p1', 'station', 1795409000, 'test');
            """)
            for i in range(1, 21):
                con.execute("INSERT INTO ships VALUES (?, 'Mining', 'voidborn', 't0_skiff', 'miner', 0)", (f"miner-{i}",))
                con.execute("INSERT INTO ships VALUES (?, 'Military', 'voidborn', 't0_skiff', 'drone', 0)", (f"drone-{i}",))
                con.execute("INSERT INTO ships VALUES (?, 'Logistics', 'voidborn', 't0_skiff', 'hauler', 0)", (f"hauler-{i}",))
            for i in range(1, 11):
                con.execute("INSERT INTO ships VALUES (?, 'Trade', 'voidborn', 't0_skiff', 'trader', 1)", (f"trader-{i}",))
            con.execute("INSERT INTO ships VALUES ('trader-11', 'Trade', 'voidborn', 't2_prayer', 'trader', 1)")
            for i in range(1, 61):
                con.execute("INSERT INTO books VALUES (?, 's1', 'ore', 10, 100, 12, 100, 1795409500)", (f"hub_{i}",))
            # Stale ship_listings (4h old)
            con.execute("INSERT INTO ship_listings VALUES ('sl1', 'hub_1', 't2_prayer', 50000, 1795395000)")
            con.commit()
            con.close()

            # Live fleet json (20 miners, 20 military, 20 logistics, 11 trade)
            fleet_ships = []
            for div, prefix, n in (("Mining", "miner", 20), ("Military", "drone", 20), ("Logistics", "hauler", 20), ("Trade", "trader", 11)):
                for i in range(1, n + 1):
                    fleet_ships.append({"pilot": f"{prefix}-{i}", "division": div, "state": "working", "order": "active"})
            (data / "fleet" / "fleet.json").write_text(json.dumps({"at": 1795409900, "ships": fleet_ships}), encoding="ascii")

            # Policies deployed: mine disabled, hunt shadowed on static routes, bursar understaffed (10/60), haul ON
            (root / "game" / "mine-policy.json").write_text(json.dumps({"enabled": False, "min_left_pct": 0.15}), encoding="ascii")
            (root / "game" / "hunt-policy.json").write_text(json.dumps({"enabled": True, "packs": {"enabled": True, "target_share": 0.25}, "escort": {"enabled": True}}), encoding="ascii")
            (root / "game" / "bursar-policy.json").write_text(json.dumps({"enabled": True, "buy": {"enabled": True}}), encoding="ascii")
            (root / "game" / "haul-policy.json").write_text(json.dumps({"enabled": True, "sell_arb": {"enabled": True}, "shipping": {"enabled": True}}), encoding="ascii")
            (root / "game" / "routes" / "bursar-network.json").write_text(json.dumps({"id": "bursar-network", "kind": "bursar", "max_ships": 65}), encoding="ascii")

            # Plans carry all 4 networks
            pilots_plan = {}
            for i in range(1, 21):
                pilots_plan[f"miner-{i}"] = ["mine-network"]
                pilots_plan[f"drone-{i}"] = ["hunt-network"]
                pilots_plan[f"hauler-{i}"] = ["haul-network"]
            for i in range(1, 12):
                pilots_plan[f"trader-{i}"] = ["bursar-network"]
            (data / "plans" / "assign.json").write_text(json.dumps({"pilots": pilots_plan}), encoding="ascii")

            # Orders: Military stuck on static hunt (15), Logistics active on haul (10), Trade only 10/60 hubs
            for i in range(1, 16):
                (data / "fleet" / "orders" / f"drone-{i}.json").write_text(json.dumps({"pilot": f"drone-{i}", "what": "hunt hunt-static"}), encoding="ascii")
            for i in range(1, 11):
                (data / "fleet" / "orders" / f"hauler-{i}.json").write_text(json.dumps({"pilot": f"hauler-{i}", "what": "haul haul-network"}), encoding="ascii")
                (data / "fleet" / "orders" / f"trader-{i}.json").write_text(json.dumps({"pilot": f"trader-{i}", "what": "bursar bursar-network"}), encoding="ascii")
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({f"hub_{i}": {"pilot": f"trader-{i}"} for i in range(1, 11)}), encoding="ascii")

            sc_bad = scorecard.compute_scorecard(str(root), str(data), now=1795410000, rivals_doc={"strategy_playbooks": []})
            # 1. Disabled mine-network triggers ALARM on Mining AND Command/Enterprise
            self.assertEqual(sc_bad["divisions"]["Mining"]["smart_engine"]["status"], "ALARM")
            self.assertIn("SMART_ENGINE_GAP", {t["code"] for t in sc_bad["divisions"]["Mining"]["triggers"]})
            self.assertIn("SMART_ENGINE_GAP", {t["code"] for t in sc_bad["enterprise"]["triggers"]})
            # 2. Shadowed hunt-network, under-covered Bursars (<51/60), stale ship_listings fire exactly 1 notice each
            for dv in ("Military", "Trade", "Intel"):
                se_trigs = [t for t in sc_bad["divisions"][dv]["triggers"] if t["code"] == "SMART_ENGINE_GAP"]
                self.assertEqual(len(se_trigs), 1, f"expected 1 SMART_ENGINE_GAP for {dv}, got {se_trigs}")
            # 3. Healthy Logistics stays COMPLETELY SILENT (0 SMART_ENGINE_GAP) and tracks O4 1/5 stations
            self.assertEqual(sc_bad["divisions"]["Logistics"]["smart_engine"]["status"], "OK")
            self.assertEqual(sc_bad["divisions"]["Logistics"]["smart_engine"]["o4_empires_covered"], 1)
            self.assertNotIn("SMART_ENGINE_GAP", {t["code"] for t in sc_bad["divisions"]["Logistics"]["triggers"]})
            # 4. Trade mobile cargo preservation counts T1+ Prayer kept off desk
            self.assertEqual(sc_bad["divisions"]["Trade"]["smart_engine"]["mobile_cargo_free"], 1)

            # Now fix every gap -> ALL divisions must drop to SILENT (0 SMART_ENGINE_GAP, zero flood!)
            (root / "game" / "mine-policy.json").write_text(json.dumps({"enabled": True, "min_left_pct": 0.15}), encoding="ascii")
            for i in range(1, 11):
                (data / "fleet" / "orders" / f"miner-{i}.json").write_text(json.dumps({"pilot": f"miner-{i}", "what": "mine_net mine-network"}), encoding="ascii")
            for i in range(1, 17):
                (data / "fleet" / "orders" / f"drone-{i}.json").write_text(json.dumps({"pilot": f"drone-{i}", "what": "hunt_net hunt-network"}), encoding="ascii")
            # 5 of 16 Military ships in a coordinated 5-ship pack (31.2% share)
            (data / "fleet" / "hunt_claims.json").write_text(json.dumps({
                "claims": {
                    f"drone-{i}": {"key": "sys1:pirate_den", "mode": "pack" if i <= 5 else "solo"}
                    for i in range(1, 17)
                }
            }), encoding="ascii")
            (data / "fleet" / "hunt_packs.json").write_text(json.dumps({
                "packs": {"p1": {"status": "active", "members": [f"drone-{i}" for i in range(1, 6)]}}
            }), encoding="ascii")
            # 55/60 safe hubs staffed
            (data / "fleet" / "bursar_claims.json").write_text(json.dumps({f"hub_{i}": {"pilot": f"trader-{i}"} for i in range(1, 56)}), encoding="ascii")
            # Fresh ship_listings (5m old)
            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.execute("UPDATE ship_listings SET t = 1795409700")
            con.commit()
            con.close()

            sc_ok = scorecard.compute_scorecard(str(root), str(data), now=1795410000, rivals_doc={"strategy_playbooks": []})
            for dv in ("Command", "Mining", "Military", "Trade", "Logistics", "Intel"):
                self.assertEqual(sc_ok["divisions"][dv]["smart_engine"]["status"], "OK", f"{dv} not OK: {sc_ok['divisions'][dv]['smart_engine']}")
                self.assertNotIn("SMART_ENGINE_GAP", {t["code"] for t in sc_ok["divisions"][dv]["triggers"]}, f"{dv} flooded when healthy")
            self.assertNotIn("SMART_ENGINE_GAP", {t["code"] for t in sc_ok["enterprise"]["triggers"]})
            txt_all = scorecard.render_briefing(sc_ok, who="all")
            self.assertIn("AUTONET", txt_all)
            txt_mil = scorecard.render_briefing(sc_ok, who="Apophis")
            self.assertIn("AutoNet  :", txt_mil)

    def test_military_coordinated_pack_exempt_from_solo_field_congestion(self):
        """An 8-ship coordinated hunt-network pack on 1 POI must NOT falsely trigger solo FIELD_CONGESTION."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (data / "fleet" / "orders").mkdir(parents=True, exist_ok=True)
            for i in range(1, 9):
                (data / "fleet" / "orders" / f"drone-{i}.json").write_text(
                    json.dumps({"pilot": f"drone-{i}", "what": "hunt_net hunt-network"}), encoding="ascii"
                )
            (data / "fleet" / "hunt_claims.json").write_text(json.dumps({
                "claims": {f"drone-{i}": {"key": "sys_pirate:stronghold_1", "mode": "pack"} for i in range(1, 9)}
            }), encoding="ascii")
            sat = scorecard._compute_field_saturation(str(root), str(data), conn=None, ship_divs={f"drone-{i}": "Military" for i in range(1, 9)})
            self.assertEqual(sat["Military"]["active_depleting"], 0)
            self.assertEqual(sat["Military"]["status"], "OK")

if __name__ == "__main__":
    unittest.main()
