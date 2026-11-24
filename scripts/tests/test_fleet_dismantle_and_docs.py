"""Tests for safe empire.py dismantle, conditional watchdog NPC_RENT_MIGRATION alert, and game_docs live discovery."""

import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import empire     # noqa: E402
import game_docs  # noqa: E402
import watchdog   # noqa: E402


class DismantleGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="dismantle-test-")
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name)
        (self.data / "empire").mkdir()
        (self.data / "fleet").mkdir()
        self.write_state()

    def write_state(self, member_count=235, containers=2, extra_fac=True):
        facs = [
            {"facility_id": "f-rec-npc", "type": "recruitment_center", "name": "Recruitment Center", "base": "npc_base", "system": "node_beta", "status": "active", "rent_per_cycle": 351},
            {"facility_id": "f-lock-npc", "type": "faction_lockbox", "name": "Faction Lockbox", "base": "npc_base", "system": "node_beta", "status": "active", "rent_per_cycle": 69},
            {"facility_id": "f-rec-own", "type": "recruitment_center", "name": "Recruitment Center", "base": "own_keep", "system": "gsc_0044", "status": "active", "rent_per_cycle": 0},
        ]
        if not extra_fac:
            facs = [f for f in facs if f["facility_id"] != "f-rec-own"]
        (self.data / "empire" / "empire.json").write_text(json.dumps({
            "faction": {"id": "fac-1", "member_count": member_count, "members_limit": 250, "owned_bases": 1},
            "members": [
                {"pilot": "Prime Directive", "role": "leader"},
                {"pilot": "hauler-3", "role": "builder"},
                {"pilot": "miner-1", "role": "member"},
            ],
            "facilities": facs,
            "faction_storage": ([{"base": "npc_base", "item": "cargo_container", "quantity": containers}] if containers else []),
        }), encoding="ascii")
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({
            "ships": [
                {"name": "Prime Directive", "credits": 50000, "docked": "npc_base"},
                {"name": "hauler-3", "credits": 50000, "docked": "npc_base"},
                {"name": "miner-1", "credits": 50000, "docked": "npc_base"},
            ]
        }), encoding="ascii")

    def test_blocks_when_cap_drops_below_seated_members(self):
        self.write_state(member_count=235, containers=2, extra_fac=True)
        # Removing f-rec-npc drops cap 250 -> 200 < 235 seated -> MUST REFUSE!
        self.assertEqual(empire.dismantle_facility(str(self.data), "hauler-3", "f-rec-npc", dry=True, caller="Apollo"), 1)

    def test_blocks_storage_while_other_facilities_exist_and_blocks_missing_containers(self):
        self.write_state(member_count=150, containers=2, extra_fac=True)
        # Cannot dismantle lockbox while recruitment_center still stands at npc_base
        self.assertEqual(empire.dismantle_facility(str(self.data), "hauler-3", "f-lock-npc", dry=True, caller="Apollo"), 1)
        # Missing cargo_container blocks dismantle
        self.write_state(member_count=150, containers=0, extra_fac=True)
        self.assertEqual(empire.dismantle_facility(str(self.data), "hauler-3", "f-rec-npc", dry=True, caller="Apollo"), 1)
        # Member without manage_facilities refused
        self.write_state(member_count=150, containers=2, extra_fac=True)
        self.assertEqual(empire.dismantle_facility(str(self.data), "miner-1", "f-rec-npc", dry=True, caller="Unity"), 1)
        # Foreign Admiral refused on real run
        self.assertEqual(empire.dismantle_facility(str(self.data), "hauler-3", "f-rec-npc", dry=False, caller="Zero"), 1)

    def test_executes_safely_when_all_guards_pass(self):
        self.write_state(member_count=150, containers=2, extra_fac=True)
        self.assertEqual(empire.dismantle_facility(str(self.data), "hauler-3", "f-rec-npc", dry=True, caller="Apollo"), 0)
        calls = []

        def fake_call(pilot, body):
            calls.append((pilot, body))
            return 200, json.dumps({"status": "dismantling", "packages": 2})

        self.assertEqual(empire.dismantle_facility(str(self.data), "hauler-3", "f-rec-npc", dry=False, caller="Apollo", call_fn=fake_call), 0)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1]["action"], "faction_dismantle")
        self.assertEqual(calls[0][1]["params"]["facility_id"], "f-rec-npc")


class ConditionalRentAlertTests(unittest.TestCase):
    def _make_db(self, root_dir, owned_bases, facilities):
        db = Path(root_dir) / "store" / "read.db"
        db.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(str(db))
        con.executescript("""
            CREATE TABLE faction (id TEXT, name TEXT, tag TEXT, leader TEXT, member_count INT, members_limit INT, treasury INT, owned_bases INT, at_war INT);
            CREATE TABLE faction_facilities (id TEXT, type TEXT, name TEXT, level INT, base TEXT, system TEXT, status TEXT, rent_per_cycle INT);
            CREATE TABLE places (system TEXT, poi TEXT);
            CREATE TABLE ships (pilot TEXT, division TEXT, role TEXT, class TEXT, status TEXT, activity TEXT, flies TEXT, credits INTEGER, t INTEGER);
            CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INT);
            INSERT INTO ships VALUES ('miner-1', 'Mining', 'miner', 'threshold', 'connected', 'mining', 'mine-1', 40000, 1795492990);
        """)
        con.execute("INSERT INTO faction VALUES ('f1','CLTV','CLTV','Prime Directive',100,200,2000000,?,0)", (owned_bases,))
        for f in facilities:
            con.execute("INSERT INTO faction_facilities VALUES (?,?,?,?,?,?,?,?)", f)
        con.commit()
        con.close()

    def test_rent_alert_fires_only_when_npc_offices_pay_rent_and_disappears_at_zero(self):
        with tempfile.TemporaryDirectory(prefix="wd-rent-") as td:
            self._make_db(td, owned_bases=1, facilities=[
                ("1", "recruitment_center", "Recruitment Center", 1, "npc_b", "node_beta", "active", 351),
                ("2", "faction_lockbox", "Faction Lockbox", 1, "npc_b", "node_beta", "active", 69),
            ])
            rep = watchdog.inspect(str(ROOT), td, hours=4.0, now=1795493000, save=False)
            codes = [f["code"] for f in rep.get("findings") or []]
            self.assertIn("NPC_RENT_MIGRATION", codes)

        with tempfile.TemporaryDirectory(prefix="wd-rent-zero-") as td:
            self._make_db(td, owned_bases=2, facilities=[
                ("1", "recruitment_center", "Recruitment Center", 1, "own_keep", "gsc_0044", "active", 0),
                ("2", "faction_lockbox", "Faction Lockbox", 1, "npc_b", "node_beta", "active", 69),
            ])
            rep = watchdog.inspect(str(ROOT), td, hours=4.0, now=1795493000, save=False)
            codes = [f["code"] for f in rep.get("findings") or []]
            self.assertNotIn("NPC_RENT_MIGRATION", codes)


class GameDocsTests(unittest.TestCase):
    def test_overview_search_help_and_guide_with_version_cache(self):
        with tempfile.TemporaryDirectory(prefix="gdocs-test-") as td:
            (Path(td) / "station").mkdir()
            (Path(td) / "station" / "stats.json").write_text(json.dumps({"version": "0.734.2"}), encoding="ascii")
            gate_calls = []

            def fake_gate(pilot, action, params=None):
                gate_calls.append((action, params))
                if action == "get_commands":
                    return {"structuredContent": {"actions": [
                        {"tool": "spacemolt_drone", "action": "deploy", "description": "Deploy a drone"},
                        {"tool": "spacemolt_facility", "action": "faction_dismantle", "description": "Pack 100% materials"},
                    ]}}, ""
                if action == "get_guide" and not (params or {}).get("guide"):
                    return {"result": "Available guides (2):\n  - drones -- Drone Pilot Guide\n      Autonomous drones.\n  - base-builder -- Base Builder Guide\n      Outposts and stations.\n"}, ""
                return {"result": "Full guide text for " + str((params or {}).get("guide"))}, ""

            ov = game_docs.render_overview(td, gate_fn=fake_gate)
            self.assertIn("2 actions across 2 tool groups", ov)
            self.assertIn("spacemolt_drone", ov)
            self.assertIn("drones", ov)
            # Second call uses cache (no extra gate call!)
            n_before = len(gate_calls)
            cm = game_docs.render_commands(td, search="dismantle", gate_fn=fake_gate)
            self.assertEqual(len(gate_calls), n_before)
            self.assertIn("spacemolt_facility.faction_dismantle", cm)
            # Help fetch & cache
            http_calls = []
            hp1 = game_docs.render_help(td, "spacemolt_facility", "faction_dismantle", http_fn=lambda t, tp: (http_calls.append((t, tp)) or "HELP BODY", ""))
            hp2 = game_docs.render_help(td, "spacemolt_facility", "faction_dismantle", http_fn=lambda t, tp: (http_calls.append((t, tp)) or "HELP BODY", ""))
            self.assertEqual(len(http_calls), 1)
            self.assertIn("HELP BODY", hp1)
            self.assertEqual(hp1, hp2)
            # Guide fetch & cache
            gd = game_docs.render_guide(td, "drones", gate_fn=fake_gate)
            self.assertIn("Full guide text for drones", gd)


if __name__ == "__main__":
    unittest.main()
