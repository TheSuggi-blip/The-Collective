"""game/fleet/upgrades.py batch hull-upgrade queue: ownership, piloting gate, sweep protection, and state machine."""

import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import upgrades  # noqa: E402


class FakeGate:
    def __init__(self, quote_price=350000, delivered=False):
        self.quote_price = quote_price
        self.delivered = delivered
        self.calls = []
        self.booked = []

    def q(self, name):
        return name

    def call(self, method, path, body=None, timeout=90):
        self.calls.append((method, path, body))
        if path.endswith("/goal"):
            return 200, json.dumps({"success": True, "message": "docked"})
        act = (body or {}).get("action")
        if act == "commission_quote":
            return 200, json.dumps({"text": "Option 1 -- Credits only: %s cr" % format(self.quote_price, ",")})
        if act == "commission_ship":
            return 200, json.dumps({"status": "sourcing"})
        if act == "list_ships":
            ships = []
            if self.delivered:
                ships.append({"ship_id": "ship-rec-1", "class_id": "recursion", "is_active": False, "location_base_id": "node_beta_base"})
            return 200, json.dumps({"ships": ships})
        if act == "switch_ship":
            return 200, json.dumps({"switched": True})
        return 200, json.dumps({})

    def book_onetime(self, pilot, title, amount, data=None):
        self.booked.append((pilot, title, amount))


class FakeWallet:
    def __init__(self):
        self.funds = []

    def add_fund(self, data, pilot, credits, why, now=None, who="Unity"):
        self.funds.append((pilot, credits, why, who))
        return 0


class FakeDivision:
    def order_of(self, pilot, data):
        p = Path(data) / "fleet" / "orders" / (pilot + ".json")
        if not p.is_file():
            return ""
        return json.loads(p.read_text()).get("what") or ""


class UpgradeQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="upg-q-test-")
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name)
        (self.data / "fleet" / "orders").mkdir(parents=True)
        (self.data / "store").mkdir(parents=True)
        self._write_db()
        self._write_fleet({"drone-1": ("Military", 50000), "drone-2": ("Military", 400000), "miner-1": ("Mining", 400000)})

    def _write_db(self):
        con = sqlite3.connect(str(self.data / "store" / "read.db"))
        con.executescript("""
            CREATE TABLE hulls (id TEXT, name TEXT, tier INT, piloting_required INT, faction TEXT, category TEXT, cargo INT, speed INT, weapon_slots INT, defense_slots INT, utility_slots INT);
            CREATE TABLE ships (pilot TEXT, division TEXT, role TEXT, empire TEXT, class TEXT, credits INT);
            CREATE TABLE ship_skills (pilot TEXT, skill TEXT, level INT);
            INSERT INTO hulls VALUES ('recursion', 'Recursion', 2, 10, 'voidborn', 'Combat', 50, 3, 4, 3, 2);
            INSERT INTO hulls VALUES ('threshold', 'Threshold', 0, 0, 'voidborn', 'Starter', 65, 2, 1, 1, 1);
            INSERT INTO ships VALUES ('drone-1', 'Military', 'drone', 'voidborn', 'threshold', 50000);
            INSERT INTO ships VALUES ('drone-2', 'Military', 'drone', 'voidborn', 'threshold', 400000);
            INSERT INTO ships VALUES ('miner-1', 'Mining', 'miner', 'voidborn', 'threshold', 400000);
            INSERT INTO ship_skills VALUES ('drone-1', 'piloting', 11);
            INSERT INTO ship_skills VALUES ('drone-2', 'piloting', 12);
            INSERT INTO ship_skills VALUES ('miner-1', 'piloting', 12);
        """)
        con.commit()
        con.close()

    def _write_fleet(self, mapping):
        ships = [{"name": n, "division": d, "credits": c, "status": "connected", "docked": "node_beta_base", "in_combat": False}
                 for n, (d, c) in mapping.items()]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}), encoding="ascii")

    def test_division_boundary_and_full_lifecycle(self):
        rc_bad, _ = upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000, pilots="miner-1", now=1000)
        self.assertEqual(rc_bad, 1)

        rc, lines = upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000, count=2, role="drone", now=1000)
        self.assertEqual(rc, 0, lines)
        self.assertEqual(upgrades.protected_pilots(self.data), {"drone-1", "drone-2"})

        gate, wal, div = FakeGate(quote_price=350000, delivered=False), FakeWallet(), FakeDivision()
        upgrades.serve_upgrades(self.data, now=1010, gate_mod=gate, wallet_mod=wal, division_mod=div)
        rows = {r["pilot"]: r for r in upgrades.load_queue(self.data)}
        self.assertEqual(rows["drone-2"]["state"], "building")
        self.assertEqual(rows["drone-2"]["paid"], 350000)
        self.assertEqual(rows["drone-1"]["state"], "funding")
        self.assertEqual(len(wal.funds), 1)
        self.assertEqual(wal.funds[0][0], "drone-1")
        self.assertEqual(gate.booked, [("drone-2", "Recursion hull commissioned", -350000)])

        gate.delivered = True
        upgrades.serve_upgrades(self.data, now=2000, gate_mod=gate, wallet_mod=wal, division_mod=div)
        rows2 = {r["pilot"]: r for r in upgrades.load_queue(self.data)}
        self.assertEqual(rows2["drone-2"]["state"], "done")

        rc_c1, _ = upgrades.queue_cancel(self.data, "Apophis", "drone-1", now=2010)
        self.assertEqual(rc_c1, 0)
        rc_c2, _ = upgrades.queue_cancel(self.data, "Apophis", "drone-2", now=2010)
        self.assertEqual(rc_c2, 1)
        self.assertEqual(upgrades.protected_pilots(self.data), set())

    def test_stop_file_halts_serve(self):
        upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000, pilots="drone-2", now=1000)
        (self.data / "fleet" / "STOP").write_text("", encoding="ascii")
        gate, wal, div = FakeGate(), FakeWallet(), FakeDivision()
        upgrades.serve_upgrades(self.data, now=1010, gate_mod=gate, wallet_mod=wal, division_mod=div)
        self.assertEqual(gate.calls, [])


if __name__ == "__main__":
    unittest.main()
