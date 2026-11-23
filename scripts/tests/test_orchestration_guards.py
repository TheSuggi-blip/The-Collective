import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import comms
import upgrades
import wallet


class TestOrchestrationGuards(unittest.TestCase):
    def test_anti_escalation_blocks_missing_scope_and_division_routing(self):
        # Missing Scope -> blocked
        bad_no_scope = "## [ENT-NEXT] | NOW | Mercury | request\nTo: Unity.\nNeed: what should newborns do?\n"
        err = comms.check_request_autonomy("Mercury", bad_no_scope)
        self.assertIsNotNone(err)
        self.assertIn("Scope:", err)

        # Docked-idle request even with cross-division scope -> blocked
        bad_dock = "## [ENT-NEXT] | NOW | Apollo | request\nTo: Unity.\nScope: cross-division\nNeed: count a docked hauler as operating.\n"
        err2 = comms.check_request_autonomy("Apollo", bad_dock)
        self.assertIsNotNone(err2)
        self.assertIn("docked-idle", err2)

        # Newborn far_ok routing request -> blocked
        bad_nb = "## [ENT-NEXT] | NOW | Mercury | request\nTo: Unity.\nScope: cross-division\nNeed: standing work at home for newborns or far_ok.\n"
        err3 = comms.check_request_autonomy("Mercury", bad_nb)
        self.assertIsNotNone(err3)
        self.assertIn("newborn", err3)

        # Legitimate capital request -> PASS
        good_cap = "## [ENT-NEXT] | NOW | Zero | request\nTo: Unity.\nScope: capital\nNeed: approve 180,000 cr treasury buy for carbon shortfall.\n"
        self.assertIsNone(comms.check_request_autonomy("Zero", good_cap))

        # Legitimate F10 flagship loan -> PASS
        good_loan = "## [ENT-NEXT] | NOW | Apophis | request\nTo: Unity.\nScope: flagship-loan\nNeed: lend Crimson Aegis under F10 for Krynn pair hunts.\n"
        self.assertIsNone(comms.check_request_autonomy("Apophis", good_loan))

        # Peer request (Admiral -> Admiral) -> untouched
        peer = "## [ENT-NEXT] | NOW | Zero | request\nTo: Apollo.\nNeed: bring 500 fuel to outpost.\n"
        self.assertIsNone(comms.check_request_autonomy("Zero", peer))

    def test_upgrades_planner_lists_p0_and_empire_t2_hulls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            data = Path(tmp) / "data"
            (root / "game" / "routes" / "guidebook" / "logistics").mkdir(parents=True)
            (root / "game" / "routes" / "guidebook" / "logistics" / "card.md").write_text("# Card\nvoidborn\n", encoding="ascii")
            (data / "store").mkdir(parents=True)
            conn = sqlite3.connect(str(data / "store" / "read.db"))
            conn.executescript("""
                CREATE TABLE hulls (id TEXT, name TEXT, faction TEXT, tier INT, category TEXT, piloting_required INT, cargo INT, speed INT, weapon_slots INT, defense_slots INT, utility_slots INT);
                INSERT INTO hulls VALUES
                    ('threshold', 'Threshold', 'voidborn', 0, 'Starter', 0, 65, 1, 1, 1, 2),
                    ('ledger', 'Ledger', NULL, 1, 'Commercial', 0, 480, 4, 0, 1, 2),
                    ('workhorse', 'Workhorse', NULL, 2, 'Industrial', 0, 300, 3, 1, 1, 4),
                    ('apophenia', 'Apophenia', 'voidborn', 2, 'Commercial', 10, 240, 2, 1, 2, 2);
                CREATE TABLE ships (pilot TEXT, division TEXT, class TEXT, empire TEXT, credits INT);
                INSERT INTO ships VALUES ('hauler-1', 'Logistics', 'threshold', 'voidborn', 40000), ('hauler-2', 'Logistics', 'threshold', 'nebula', 25000);
                CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INT);
                INSERT INTO ship_skills VALUES ('hauler-1', 'piloting', 10), ('hauler-2', 'piloting', 3);
                CREATE TABLE ship_modules (pilot TEXT, module TEXT);
                INSERT INTO ship_modules VALUES ('hauler-1', 'mining_laser_i');
                CREATE TABLE books (item TEXT, ask REAL, ask_qty INT, base TEXT);
                INSERT INTO books VALUES ('ledger', 35000, 3, 'grand_exchange');
            """)
            conn.commit()
            conn.close()
            out = upgrades.render_upgrades(root, data, who="Apollo")
            self.assertIn("Ledger", out)
            self.assertIn("Workhorse", out)
            self.assertIn("Apophenia", out)
            self.assertIn("35,000 cr", out)
            self.assertIn("missing empires: nebula", out)

    def test_auto_queue_seats_fills_open_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "empire").mkdir()
            (data / "fleet").mkdir()
            (data / "empire" / "empire.json").write_text(json.dumps({
                "faction": {"member_count": 1, "members_limit": 3, "leader": "Prime Directive"},
                "members": [{"pilot": "Prime Directive"}],
            }), encoding="ascii")
            (data / "fleet" / "fleet.json").write_text(json.dumps({
                "ships": [
                    {"name": "Prime Directive", "division": "Command", "number": 0, "credits": 50000},
                    {"name": "hauler-1", "division": "Logistics", "number": 1, "credits": 30000},
                    {"name": "miner-1", "division": "Mining", "number": 1, "credits": 30000},
                    {"name": "scout-1", "division": "Intel", "number": 1, "credits": 20000},
                ]
            }), encoding="ascii")
            added = wallet.auto_queue_seats(str(data), now=1795410000, dry=False)
            self.assertEqual(added, 2)
            rows = wallet.seat_rows(str(data))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["state"], "open")


if __name__ == "__main__":
    unittest.main()
