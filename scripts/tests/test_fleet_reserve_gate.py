"""game/fleet/reserves.py and its hook in dispatch.why_not: `requires.reserve` opens a route only while the newest
reading of a faction reserve stands under a floor (requests ENT-266, Apollo: the bunker route of our outpost at
GSC-0044, a budget raised by hand each turn). The readings: empire.json's faction storage (empire.py collect) and the
route's own bunker notes (route_run.py). routes.py check validates the field. No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
OUTPOST = "443f0c5b2a1fbbcea95d13b76a797fe9"
BUNKER = {"id": "supply-bunker", "kind": "circuit", "title": "fuel for the outpost", "max_ships": 1, "standing": True,
          "requires": {"empty_hold": True, "reserve": {"base": OUTPOST, "item": "fuel", "below": 5000}},
          "stops": [{"at": "the_experiment:the_experiment_research_station:the_experiment_research_station", "buy": [{"item": "fuel_cell", "qty": 65, "max_price": 102}]},
                    {"at": "gsc_0044:da9de8c360c46ffee15dee4e7d1b8476:" + OUTPOST, "refuel": False, "bunker": {"keep": 30}}]}
PARK = {"id": "park", "kind": "circuit", "title": "park", "park": True, "stops": [{"at": "home:core:base"}]}


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_reserve_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReserveGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-reserve-gate-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo" / "game", Path(self.temp.name) / "data"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.data / "fleet" / "orders", self.data / "routes", self.data / "empire"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nhome\tHome\t0\t0\tvoidborn\nthe_experiment\tX\t1\t0\t-\ngsc_0044\tG\t2\t0\t-\n", encoding="ascii")
        self.now = 1794970000                                                                  # 2026-11-18 03:06:40 UTC
        self.dispatch = load("dispatch")
        self.reserves = self.dispatch.reserves
        self.pilot = {"name": "hauler-3", "role": "hauler", "credits": 40000, "modules": [], "docked": True, "goods": 0}
        (self.data / "fleet" / "reserve-gate-on").write_text("")
        self.addCleanup(self.reserves.EMPIRE.update, path=None, stamp=None, rows={})

    def text(self, epoch):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))

    def empire(self, units, ago, item="fuel"):
        rows = [{"base": OUTPOST, "base_name": "CLTV Outpost GSC-0044", "item": item, "units": units, "read_at": self.text(self.now - ago)},
                {"base": OUTPOST, "base_name": "CLTV Outpost GSC-0044", "item": "iron_ore", "units": 533, "read_at": self.text(self.now - ago)}]
        path = self.data / "empire" / "empire.json"
        tmp = path.with_name("empire.json.tmp")                                               # a new reading, as a collect writes it:
        tmp.write_text(json.dumps({"written_at": self.text(self.now - ago), "faction_storage": rows}))
        os.replace(tmp, path)                                                                  # a new file, whatever the clock's grain

    def run_row(self, reserve, ended_ago, minutes=20):
        start = self.now - ended_ago - minutes * 60
        return {"route": "supply-bunker", "kind": "circuit", "pilot": "hauler-3", "started": self.text(start), "minutes": minutes,
                "credits_before": 41937, "credits_after": 35320, "delta": -6617, "notes": ["bunker +1361 fuel from 65 cells, reserve %s" % reserve]}

    def why(self, route=BUNKER, rows=()):
        state = {"now": self.now, "data": str(self.data), "rows": list(rows), "orders": {}, "rest": {}, "booked": {}}
        return self.dispatch.why_not(self.pilot, route["id"], route, state)[0]

    def test_the_route_opens_under_the_floor_and_closes_at_it_by_the_newest_reading(self):
        self.empire(3615, 600)
        self.assertIsNone(self.why())                                                          # 3,615 of a floor of 5,000, read 10 minutes ago
        self.empire(5000, 600)
        self.assertEqual(self.why(), "reserve: fuel 5,000 at CLTV Outpost GSC-0044, not under 5,000 (read 10 min ago)")
        self.empire(3615, 1500)                                                                # the collect read 3,615 25 minutes ago ...
        self.assertIsNone(self.why(rows=[self.run_row(4976, 300)]))                           # its last run read 4,976 five minutes ago: still under
        self.assertEqual(self.why(rows=[self.run_row(6337, 300)]),                             # ... and the supply run that ended 5 minutes ago read 6,337
                         "reserve: fuel 6,337 at CLTV Outpost GSC-0044, not under 5,000 (read 5 min ago)")
        self.assertIsNone(self.why(rows=[self.run_row(6337, 3000)]))                           # a run older than the collect's reading: the collect wins
        self.assertIsNone(self.why(rows=[dict(self.run_row(6337, 300), notes=["bunker +721 fuel from 65 cells, reserve None"])]))   # no figure: no reading

    def test_a_reading_older_than_its_limit_or_none_closes_the_route(self):
        self.assertEqual(self.why(), "reserve: not read")
        self.empire(3615, 61 * 60)
        self.assertEqual(self.why(), "reserve: not read for 61 min")                          # nobody refreshed it: never open on an old reading
        aged = dict(BUNKER, requires={"reserve": {"base": OUTPOST, "below": 5000, "max_age_minutes": 180}})     # `item` defaults to fuel
        self.assertIsNone(self.why(route=aged))
        self.empire(3615, 4 * 3600)
        self.assertEqual(self.why(route=aged), "reserve: not read for 4.0 h")

    def test_an_item_of_the_faction_s_storage_is_a_reserve_too(self):
        self.empire(3615, 600)
        ore = dict(BUNKER, id="ore-to-outpost", requires={"reserve": {"base": OUTPOST, "item": "iron_ore", "below": 500}})
        self.assertEqual(self.why(route=ore), "reserve: iron_ore 533 at CLTV Outpost GSC-0044, not under 500 (read 10 min ago)")
        self.assertIsNone(self.why(route=dict(ore, requires={"reserve": {"base": OUTPOST, "item": "iron_ore", "below": 1000}})))

    def test_the_gate_is_off_until_its_switch_file_stands_and_then_no_route_with_the_field_flies(self):
        self.empire(3615, 600)
        (self.data / "fleet" / "reserve-gate-on").unlink()
        self.assertEqual(self.why(), "reserve: the gate is off (data/fleet/reserve-gate-on absent)")
        self.assertIsNone(self.why(route=dict(BUNKER, requires={"empty_hold": True})))           # a route without the field: as before
        (self.data / "fleet" / "reserve-gate-on").write_text("")
        self.assertIsNone(self.why())

    def test_routes_check_validates_the_field(self):
        routes = load("routes")
        for route in (BUNKER, PARK):
            (self.root / "routes" / (route["id"] + ".json")).write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        (self.root / "routes" / "plans" / "hauler.json").write_text(json.dumps({"role": "hauler", "owner": "Apollo", "routes": ["supply-bunker", "park"]}), encoding="ascii")
        routes.write_index(str(self.root))
        found = lambda: [e for e in routes.check(str(self.root))[0] if "requires.reserve" in e]
        self.assertEqual(found(), [])
        bad = dict(BUNKER, requires={"reserve": {"base": "Not An Id", "item": 7, "below": 0, "max_age_minutes": True, "ceiling": 9000}})
        (self.root / "routes" / "supply-bunker.json").write_text(json.dumps(bad, indent=1) + "\n", encoding="ascii")
        self.assertEqual(found(), ["game/routes/supply-bunker.json: `requires.reserve` knows no `ceiling` (base, item, below, max_age_minutes)",
                                   "game/routes/supply-bunker.json: `requires.reserve.base` must be a base id (a station's id, or an outpost's 32 hex digits)",
                                   "game/routes/supply-bunker.json: `requires.reserve.item` must be an item id (`fuel` for a bunker)",
                                   "game/routes/supply-bunker.json: `requires.reserve.below` must be a whole number above 0",
                                   "game/routes/supply-bunker.json: `requires.reserve.max_age_minutes` must be a whole number above 0"])
        self.assertEqual(self.reserves.faults("fuel"), ["`requires.reserve` must be {\"base\": \"<base id>\", \"item\": \"fuel\", \"below\": N}"])

    def test_show_prints_what_the_gate_would_do(self):
        (self.root / "routes" / "supply-bunker.json").write_text(json.dumps(BUNKER, indent=1) + "\n", encoding="ascii")
        self.empire(3615, 600)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.reserves.show(str(self.root), str(self.data), now=self.now)
        self.assertIn("RESERVE GATE | on | 1 route(s) carry requires.reserve", out.getvalue())
        self.assertIn("supply-bunker | below 5,000 at %s | fuel 3,615, read 10 min ago from empire.json (empire.py collect) | would be open" % OUTPOST, out.getvalue())


if __name__ == "__main__":
    unittest.main()
