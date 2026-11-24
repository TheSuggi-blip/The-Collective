"""Docked-leader errand queue (Q75 (12)): wallet.py errand queue + serve_errands + dispatch leader_errand_action."""
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
if str(FLEET) not in sys.path:
    sys.path.insert(0, str(FLEET))

import dispatch
import wallet


class LeaderErrandQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data = Path(self.tmp.name)
        (self.data / "fleet").mkdir(parents=True)
        (self.data / "empire").mkdir(parents=True)
        (self.data / "empire" / "empire.json").write_text(
            json.dumps({"faction": {"leader": "Prime Directive"}}), encoding="utf-8"
        )
        dispatch.ERRAND_DOCK_WAIT.clear()
        dispatch.ERRAND_TOLD.clear()

    def tearDown(self):
        self.tmp.cleanup()

    def _write_fleet(self, docked=""):
        ship = {"name": "Prime Directive", "credits": 500000, "status": "connected", "docked": docked}
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [ship]}), encoding="utf-8")
        return ship

    def test_unity_only_and_security_allowlist_block_war_and_leadership_transfer(self):
        now = 1795480000
        # Non-Unity Admiral refused (F11)
        self.assertEqual(wallet.add_errand(self.data, "promote", {"player_id": "hauler-1", "role_id": "officer"}, "need officer", now=now, who="Apollo"), 1)
        # Leadership transfer refused even for Unity
        self.assertEqual(wallet.add_errand(self.data, "promote", {"player_id": "hauler-1", "role_id": "leader"}, "bad", now=now, who="Unity"), 1)
        # War/ally/kick refused
        for forbidden in ("declare_war", "accept_ally", "kick", "disband"):
            self.assertEqual(wallet.add_errand(self.data, forbidden, {"target_faction_id": "HIVE"}, "bad", now=now, who="Unity"), 1)
        # Valid promote & post_mission accepted for Unity
        self.assertEqual(wallet.add_errand(self.data, "promote", {"player_id": "hauler-1", "role_id": "officer"}, "unlock GSC-0044 iron", now=now, who="Unity"), 0)
        self.assertEqual(wallet.add_errand(
            self.data, "post_mission",
            {"title": "Atria Titanium", "description": "Deliver titanium", "type": "delivery",
             "objectives": [{"type": "deliver_item", "item_id": "refined_titanium", "quantity": 500}],
             "rewards": {"credits": 150000}},
            "finish Atria outpost", station="node_beta_industrial_station", now=now + 1, who="Unity"
        ), 0)
        rows = wallet.errands(self.data)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["action"], "promote")
        self.assertEqual(rows[1]["station"], "node_beta_industrial_station")

    def test_serve_errands_waits_for_dock_matches_station_and_executes_once(self):
        now = 1795480000
        wallet.add_errand(self.data, "promote", {"player_id": "hauler-1", "role_id": "officer"}, "promote officer", now=now, who="Unity")
        wallet.add_errand(
            self.data, "post_mission",
            {"title": "Atria Iron", "description": "Deliver iron", "type": "delivery",
             "objectives": [{"type": "deliver_item", "item_id": "iron_ore", "quantity": 100}],
             "rewards": {"credits": 50000}},
            "post notice", station="node_beta_industrial_station", now=now, who="Unity"
        )
        calls = []

        def fake_raw(pilot, group, action, params):
            calls.append((pilot, group, action, params))
            return True, "ok"

        with mock.patch.object(wallet, "errand_raw", side_effect=fake_raw):
            # 1. Undocked: nothing runs
            self._write_fleet(docked="")
            self.assertEqual(wallet.serve_errands(self.data, "Prime Directive", now + 10, dry=False), 0)
            self.assertEqual(calls, [])
            # 2. Docked at central_nexus: promote runs (any station), post_mission waits for node_beta
            self._write_fleet(docked="central_nexus")
            self.assertEqual(wallet.serve_errands(self.data, "Prime Directive", now + 20, dry=False), 0)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][2], "promote")
            rows = wallet.errands(self.data)
            self.assertEqual(rows[0]["state"], "done")
            self.assertEqual(rows[1]["state"], "open")
            # 3. Docked at node_beta_industrial_station: post_mission runs and promote does not double-fire
            self._write_fleet(docked="node_beta_industrial_station")
            self.assertEqual(wallet.serve_errands(self.data, "Prime Directive", now + 30, dry=False), 0)
            self.assertEqual(len(calls), 2)
            self.assertEqual(calls[1][2], "post_mission")
            rows = wallet.errands(self.data)
            self.assertEqual(rows[1]["state"], "done")
            self.assertEqual(rows[1]["station_used"], "node_beta_industrial_station")

    def test_cancel_and_expiry(self):
        now = 1795480000
        wallet.add_errand(self.data, "promote", {"player_id": "hauler-2", "role_id": "officer"}, "cancel me", now=now, who="Unity")
        eid = wallet.errands(self.data)[0]["id"]
        self.assertEqual(wallet.cancel_errand(self.data, eid, now=now + 5, who="Unity"), 0)
        self.assertEqual(wallet.errands(self.data)[0]["state"], "cancelled")
        # Stale errand expires after ERRAND_WAIT hours
        wallet.add_errand(self.data, "promote", {"player_id": "hauler-3", "role_id": "officer"}, "stale", now=now, who="Unity")
        self._write_fleet(docked="")
        wallet.serve_errands(self.data, "Prime Directive", now + (wallet.ERRAND_WAIT + 1) * 3600, dry=False)
        self.assertEqual(wallet.errands(self.data)[1]["state"], "ended")

    def test_dispatch_leader_errand_action_parks_and_holds_at_required_station(self):
        now = 1795480000
        routes = {
            "park": {"id": "park", "kind": "circuit", "park": True, "stops": [{"at": "nexus_prime:the_core:central_nexus"}]},
            "park-node-beta": {"id": "park-node-beta", "kind": "circuit", "park": True, "stops": [{"at": "node_beta:node_beta_industrial_station:node_beta_industrial_station"}]},
        }
        wallet.add_errand(
            self.data, "post_mission",
            {"title": "T", "description": "D", "type": "delivery", "objectives": [{"type": "deliver_item", "item_id": "iron_ore", "quantity": 10}], "rewards": {"credits": 1000}},
            "notice board", station="node_beta_industrial_station", now=now, who="Unity"
        )
        # Undocked -> routes to park-node-beta
        act, obj = dispatch.leader_errand_action("Prime Directive", {"name": "Prime Directive", "docked": ""}, self.data, now + 5, routes)
        self.assertEqual(act, "park")
        self.assertEqual(obj["id"], "park-node-beta")
        # Docked at wrong station -> routes to park-node-beta
        act2, obj2 = dispatch.leader_errand_action("Prime Directive", {"name": "Prime Directive", "docked": "central_nexus"}, self.data, now + 10, routes)
        self.assertEqual(act2, "park")
        self.assertEqual(obj2["id"], "park-node-beta")
        # Docked at required station -> holds up to ERRAND_HOLD_SECS
        act3, _obj3 = dispatch.leader_errand_action("Prime Directive", {"name": "Prime Directive", "docked": "node_beta_industrial_station"}, self.data, now + 20, routes)
        self.assertEqual(act3, "hold")
        # After ERRAND_HOLD_SECS -> releases so leader never freezes
        act4, _obj4 = dispatch.leader_errand_action("Prime Directive", {"name": "Prime Directive", "docked": "node_beta_industrial_station"}, self.data, now + 20 + dispatch.ERRAND_HOLD_SECS + 1, routes)
        self.assertIsNone(act4)


class SweepStepErrorTests(LeaderErrandQueueTests):
    def test_an_upgrade_step_that_raises_is_printed_and_fails_the_pass(self):
        # errors.log ENT-171: wallet.sweep wrapped serve_upgrades in `except Exception: pass`, so a TypeError on every
        # pass stood unseen for hours; now the step's error is a HALT line and the pass reports a failure
        import io
        import contextlib
        import upgrades
        self._write_fleet(docked="")
        out = io.StringIO()
        with mock.patch.object(upgrades, "serve_upgrades", side_effect=TypeError("missing a required argument: 'hours'")), \
                contextlib.redirect_stdout(out):
            rc = wallet.sweep(str(self.data), 1795480000, True)
        self.assertIn("HALT: the upgrade queue's step failed: TypeError", out.getvalue())
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
