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

    def add_fund(self, data, pilot, credits, why, hours=None, now=None, who="Unity"):
        self.funds.append((pilot, credits, why, who))
        return 0


class RealSignatureWallet(FakeWallet):
    """add_fund bound to the real wallet.add_fund's signature first: a call the real one refuses (TypeError) fails here
    too. FakeWallet accepted a call without `hours`, so a missing argument passed every test while wallet.sweep's
    try/except swallowed the TypeError and no queued upgrade was ever funded."""

    def add_fund(self, *args, **kwargs):
        import inspect
        import wallet
        bound = inspect.signature(wallet.add_fund).bind(*args, **kwargs)
        bound.apply_defaults()
        a = bound.arguments
        return FakeWallet.add_fund(self, a["data"], a["pilot"], a["credits"], a["why"], now=a["now"], who=a["who"])


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

    def test_a_short_wallet_is_funded_through_the_real_add_fund_signature(self):
        rc, lines = upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000,
                                       pilots="drone-1", now=1000)
        self.assertEqual(rc, 0, lines)
        gate, wal, div = FakeGate(), RealSignatureWallet(), FakeDivision()
        upgrades.serve_upgrades(self.data, now=1010, gate_mod=gate, wallet_mod=wal, division_mod=div)
        rows = {r["pilot"]: r for r in upgrades.load_queue(self.data)}
        self.assertEqual(rows["drone-1"]["state"], "funding")
        self.assertEqual([f[0] for f in wal.funds], ["drone-1"])
        self.assertEqual(wal.funds[0][1], 370000 + upgrades.UPGRADE_FLOOR - 50000)

    def test_stop_file_halts_serve(self):
        upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000, pilots="drone-2", now=1000)
        (self.data / "fleet" / "STOP").write_text("", encoding="ascii")
        gate, wal, div = FakeGate(), FakeWallet(), FakeDivision()
        upgrades.serve_upgrades(self.data, now=1010, gate_mod=gate, wallet_mod=wal, division_mod=div)
        self.assertEqual(gate.calls, [])



    def test_busy_funded_and_ready_pilots_receive_polite_stop_and_dispatch_hold(self):
        import dispatch
        dispatch.UPGRADE_HOLD_WAIT.clear()
        dispatch.UPGRADE_TOLD.clear()
        rc, lines = upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000,
                                       pilots="drone-2", now=1000)
        self.assertEqual(rc, 0, lines)
        rows = upgrades.load_queue(self.data)
        rows[0]["state"] = "funded"
        upgrades.save_queue(self.data, rows)

        # Dispatch must hold funded pilot idle up to UPGRADE_HOLD_SECS
        held = dispatch.upgrade_hold_needed("drone-2", self.data, 1050)
        self.assertIsNotNone(held)
        self.assertEqual(held["hull"], "recursion")
        self.assertIsNone(dispatch.upgrade_hold_needed("drone-1", self.data, 1050))
        self.assertIsNone(dispatch.upgrade_hold_needed("drone-2", self.data, 1050 + dispatch.UPGRADE_HOLD_SECS + 1))

        # Busy funded pilot receives host/stop/<pilot> instead of silent deferral
        gate, wal, div = FakeGate(quote_price=350000, delivered=False), FakeWallet(), FakeDivision()
        ord_p = self.data / "fleet" / "orders" / "drone-2.json"
        ord_p.write_text(json.dumps({"pilot": "drone-2", "what": "bursar bursar-network"}), encoding="ascii")
        upgrades.serve_upgrades(self.data, now=1060, gate_mod=gate, wallet_mod=wal, division_mod=div)
        stop_h = self.data / "fleet" / "host" / "stop" / "drone-2"
        self.assertTrue(stop_h.is_file())
        rows_after = upgrades.load_queue(self.data)
        self.assertIn("stop sent", rows_after[0]["note"])

        # Once pilot is free, it commissions; when ready while busy, ready_to_switch + stop sent
        stop_h.unlink()
        ord_p.unlink()
        upgrades.serve_upgrades(self.data, now=1070, gate_mod=gate, wallet_mod=wal, division_mod=div)
        self.assertEqual(upgrades.load_queue(self.data)[0]["state"], "building")
        gate.delivered = True
        ord_p.write_text(json.dumps({"pilot": "drone-2", "what": "hunt hunt-alpha"}), encoding="ascii")
        upgrades.serve_upgrades(self.data, now=2000, gate_mod=gate, wallet_mod=wal, division_mod=div)
        self.assertTrue(stop_h.is_file())
        self.assertTrue(upgrades.load_queue(self.data)[0].get("ready_to_switch"))
        self.assertIn("drone-2", upgrades.hold_pilots(self.data))
        dispatch.UPGRADE_HOLD_WAIT.clear()
        self.assertIsNotNone(dispatch.upgrade_hold_needed("drone-2", self.data, 2010))



    def test_stale_upgrade_hold_reclaimed_and_small_fuel_spend_still_funded(self):
        rc, lines = upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000,
                                       pilots="drone-1", now=1000)
        self.assertEqual(rc, 0, lines)
        rows = upgrades.load_queue(self.data)
        rows[0]["state"] = "funding"
        upgrades.save_queue(self.data, rows)
        self._write_fleet({"drone-1": ("Military", 389700), "drone-2": ("Military", 400000), "miner-1": ("Mining", 400000)})
        (self.data / "fleet" / "orders" / "drone-1.json").write_text(
            json.dumps({"pilot": "drone-1", "what": upgrades.UPGRADE_HOLD}), encoding="ascii")
        gate, wal, div = FakeGate(quote_price=350000, delivered=False), FakeWallet(), FakeDivision()
        upgrades.serve_upgrades(self.data, now=1060, gate_mod=gate, wallet_mod=wal, division_mod=div)
        after = upgrades.load_queue(self.data)[0]
        self.assertEqual(after["state"], "building")
        self.assertEqual(after["paid"], 350000)


    def test_timeout_does_not_abort_and_cheaper_listed_hull_is_bought(self):
        class ListedOrTimeoutGate(FakeGate):
            def __init__(self):
                super().__init__(quote_price=350000, delivered=False)
                self.bought = []

            def call(self, method, path, body=None, timeout=90):
                if "/goal" in path and "drone-1" in path:
                    raise TimeoutError("timed out docking drone-1")
                if isinstance(body, dict) and body.get("action") == "browse_ships":
                    return 200, json.dumps({"structuredContent": {"listings": [
                        {"listing_id": "lst-99", "class_id": "recursion", "base_id": "node_beta_base", "price": 224000},
                        {"listing_id": "lst-98", "class_id": "recursion", "base_id": "node_beta_base", "price": 260000},
                    ]}})
                if isinstance(body, dict) and body.get("action") == "buy_listed_ship":
                    self.bought.append((path, body["params"]["listing_id"]))
                    return 200, json.dumps({"structuredContent": {"ok": True}})
                return super().call(method, path, body=body, timeout=timeout)

        # drone-1 not docked (will raise TimeoutError), drone-2 docked (will buy cheaper listed hull)
        ships = [
            {"name": "drone-1", "division": "Military", "credits": 400000, "status": "connected", "docked": "", "system": "other", "in_combat": False},
            {"name": "drone-2", "division": "Military", "credits": 400000, "status": "connected", "docked": "node_beta_base", "system": "node_beta", "in_combat": False},
        ]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}), encoding="ascii")
        rc, lines = upgrades.queue_add(self.data, "Apophis", "recursion", "node_beta:poi:node_beta_base", 370000,
                                       pilots="drone-1,drone-2", now=1000)
        self.assertEqual(rc, 0, lines)
        gate, wal, div = ListedOrTimeoutGate(), FakeWallet(), FakeDivision()
        upgrades.serve_upgrades(self.data, now=1010, gate_mod=gate, wallet_mod=wal, division_mod=div)
        rows = {r["pilot"]: r for r in upgrades.load_queue(self.data)}
        self.assertEqual(rows["drone-2"]["state"], "done")
        self.assertEqual(rows["drone-2"]["paid"], 224000)
        self.assertIn("bought listed recursion", rows["drone-2"]["note"])
        self.assertEqual(len(gate.bought), 1)
        self.assertEqual(gate.bought[0][1], "lst-99")
        self.assertEqual(gate.booked, [("drone-2", "Recursion hull bought from listing", -224000)])
        self.assertEqual(rows["drone-1"]["state"], "funded")
        self.assertIn("TimeoutError", rows["drone-1"]["note"])

    def test_gate_book_onetime_accepts_data_kwarg_for_hull_capex(self):
        import gate as gate_mod
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "fleet").mkdir(parents=True, exist_ok=True)
            gate_mod.book_onetime("miner-47", "Resonance_miner hull commissioned", -277941, data=tmp)
            rows = json.loads((Path(tmp) / "fleet" / "onetime.json").read_text())
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][1:], ["miner-47", "Resonance_miner hull commissioned", -277941])


if __name__ == "__main__":
    unittest.main()
