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

if __name__ == "__main__":
    unittest.main()
