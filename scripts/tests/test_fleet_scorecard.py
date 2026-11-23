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

            # Intel: docked waiting scout counts as docked watch (F8) -> 100% effective employment, 50% freshness ALARM
            intel = sc["divisions"]["Intel"]
            self.assertEqual(intel["employment"]["pct"], 100.0)
            i_codes = {t["code"] for t in intel["triggers"]}
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


if __name__ == "__main__":
    unittest.main()
