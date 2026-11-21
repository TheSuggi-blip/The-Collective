"""An alert while a base of ours reads wrecked or a facility of ours damaged (errors.log ENT-112, DECISIONS Q75 (3)): the
briefing's first line, the tool fleet's view=alerts (hive.py stats alerts) and the `since` empire.py collect keeps.
On a disposable data folder from the files the fleet reads already; no engine, no game call."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"
sys.path.insert(0, str(FLEET))
OUTPOST = "CLTV Outpost GSC-0044"
BASE_ID = "443f0c5b2a1fbbcea95d13b76a797fe9"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_base_alert_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def said(function, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        function(*args)
    return out.getvalue()


class BaseAlertTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-base-alert-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("empire", "station", "scouting", "fleet"):
            (self.data / folder).mkdir()
        self.state = {"written_at": "2026-11-18T01:04:00Z", "faction": {"tag": "CLTV", "leader": "Prime Directive"},
                      "bases": [{"base": BASE_ID, "name": OUTPOST, "system": "gsc_0044", "kind": "outpost", "condition": "thriving"}],
                      "facilities": [{"facility_id": "f1", "type": "faction_fuel_bunker", "name": "Faction Fuel Bunker", "base": BASE_ID, "system": "gsc_0044", "status": "active"},
                                     {"facility_id": "f2", "type": "faction_lockbox", "name": "Faction Lockbox", "base": "node_beta_industrial_station", "system": "node_beta", "status": "active"}]}
        self.put(wrecked=True)

    def put(self, wrecked):
        (self.data / "empire" / "empire.json").write_text(json.dumps(self.state))
        (self.data / "station" / "stations.json").write_text(json.dumps([
            {"name": OUTPOST, "type": "outpost", "system": "gsc_0044", "tag": "CLTV", "condition": "thriving", "wrecked": wrecked},
            {"name": "Ashborne Reach", "type": "station", "system": "alula", "tag": "ASHC", "condition": "critical", "wrecked": True}]))

    def test_the_briefing_opens_with_the_wrecked_outpost_while_the_collect_still_reads_it_active(self):
        # ENT-112: the public list read the outpost wrecked while empire.json, 91 hours old, printed both facilities active
        hive = load("hive")
        text = said(load("basewatch").briefing, str(self.data))
        self.assertTrue(text.startswith("BASE ALERT | 1 of our bases"), text)
        self.assertIn("CLTV Outpost GSC-0044 reads wrecked (the public list of stations", text)
        self.assertIn("since after 2026-11-18 01:04 UTC (the last collect read it whole)", text)
        self.assertIn("repair bill not read", text)
        self.assertNotIn("Ashborne", text)                                   # another faction's wreck is no alert of ours
        self.assertIn('__import__("basewatch").briefing(data, now)', (FLEET / "hive.py").read_text(encoding="ascii"))
        source = (FLEET / "hive.py").read_text(encoding="ascii")
        body = source[source.index("def show_briefing("):]
        self.assertLess(body.index("basewatch"), body.index("THE ORDERS IN FORCE"))      # at the top, above the orders
        self.assertTrue(hasattr(hive, "show_briefing"))

    def test_a_damaged_facility_is_named_with_the_time_a_collect_first_read_it_and_the_bill_the_census_read(self):
        basewatch = load("basewatch")
        self.state["facilities"][0]["status"] = "damaged"
        self.state["written_at"] = "2026-11-21T19:50:00Z"
        old = {"base_alerts": [{"key": "facility:f1:damaged", "since": "2026-11-21T19:35:00Z"}]}
        self.state["base_alerts"] = basewatch.stamped(self.state, old, [{"name": OUTPOST, "tag": "CLTV", "wrecked": False}], self.state["written_at"])
        self.assertEqual([(a["key"], a["since"]) for a in self.state["base_alerts"]], [("facility:f1:damaged", "2026-11-21T19:35:00Z")])
        (self.data / "scouting" / "gsc_0044.json").write_text(json.dumps({"read_at": "2026-11-21T20:26:00Z", "pois": {"p": {
            "poi": {"name": OUTPOST}, "base": {"id": BASE_ID, "name": OUTPOST, "hull": 8000, "max_hull": 12000},
            "repairs": {"materials": [{"item_id": "steel_plate", "quantity": 120}, {"item_id": "circuit_board", "quantity": 30}]}}}}))
        self.put(wrecked=False)
        text = basewatch.line(str(self.data))
        self.assertIn("Faction Fuel Bunker at CLTV Outpost GSC-0044 reads damaged (faction_owned (empire.py collect), read 2026-11-21 19:50 UTC), "
                      "since 2026-11-21 19:35 UTC", text)
        self.assertIn("repair bill 120 steel_plate, 30 circuit_board (census 2026-11-21 20:26 UTC); hull 8,000 of 12,000", text)
        # the tool fleet, view=alerts: hive.py stats alerts prints it first, even without a store copy
        stats = load("stats")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            stats.main(["alerts", "--data", str(self.data)])
        self.assertTrue(out.getvalue().startswith("BASES | 1 alert"), out.getvalue())
        self.assertIn("ALERT Faction Fuel Bunker at CLTV Outpost GSC-0044 reads damaged", out.getvalue())

    def test_no_alert_no_line_and_an_alert_ends_with_the_reading_that_shows_the_base_whole(self):
        basewatch = load("basewatch")
        self.put(wrecked=False)
        self.assertEqual(said(basewatch.briefing, str(self.data)), "")
        self.assertEqual(basewatch.alerts(str(self.data)), [])
        self.assertEqual(basewatch.stamped(self.state, {"base_alerts": [{"key": "base:%s:wrecked" % OUTPOST, "since": "x"}]},
                                           [{"name": OUTPOST, "tag": "CLTV", "wrecked": False}], "2026-11-21T22:00:00Z"), [])

    def test_the_collect_keeps_base_alerts_with_since_from_pass_to_pass(self):
        # empire.py collect writes `base_alerts` from its own readings: the first reading that showed it keeps its time
        empire = load("empire")
        self.assertIn('state["base_alerts"] = __import__("basewatch").stamped(state, old, public, state["written_at"])',
                      (FLEET / "empire.py").read_text(encoding="ascii"))
        state = dict(self.state, written_at="2026-11-21T20:00:00Z")
        state["facilities"] = [dict(state["facilities"][0], status="offline")]
        first = load("basewatch").stamped(state, {}, [{"name": OUTPOST, "tag": "CLTV", "wrecked": True}], state["written_at"])
        self.assertEqual([(a["key"], a["since"]) for a in first], [("base:%s:wrecked" % OUTPOST, "2026-11-21T20:00:00Z"), ("facility:f1:offline", "2026-11-21T20:00:00Z")])
        later = load("basewatch").stamped(dict(state, written_at="2026-11-21T20:15:00Z"), {"base_alerts": first},
                                          [{"name": OUTPOST, "tag": "CLTV", "wrecked": True}], "2026-11-21T20:15:00Z")
        self.assertEqual([a["since"] for a in later], ["2026-11-21T20:00:00Z", "2026-11-21T20:00:00Z"])
        self.assertTrue(hasattr(empire, "collect"))


if __name__ == "__main__":
    unittest.main()
