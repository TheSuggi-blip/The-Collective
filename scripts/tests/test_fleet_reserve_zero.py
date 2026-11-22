"""r23, requests ENT-315 (Apollo): `requires.reserve` reads an item the faction's storage at a base no longer lists as
0 units when empire.py viewed that base whole in the reading; a base whose view failed, or a reading too old, still
closes the route. No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
OUTPOST = "443f0c5b2a1fbbcea95d13b76a797fe9"
PLATE = {"id": "supply-plate", "kind": "circuit", "title": "steel plate for the outpost", "max_ships": 1, "standing": True,
         "requires": {"reserve": {"base": OUTPOST, "item": "steel_plate", "below": 180}},
         "stops": [{"at": "gsc_0044:da9de8c360c46ffee15dee4e7d1b8476:" + OUTPOST, "store": ["steel_plate"]}]}


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_reserve_zero_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReserveZeroTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-reserve-zero-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "data"
        (self.data / "empire").mkdir(parents=True)
        (self.data / "fleet").mkdir(parents=True)
        (self.data / "fleet" / "reserve-gate-on").write_text("")
        self.now = 1795310000
        self.reserves = load("reserves")

    def empire(self, ago, rows, error=""):
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))
        state = {"written_at": stamp, "faction_storage_error": error,
                 "faction_storage_places": [{"base": OUTPOST, "base_name": "CLTV Outpost GSC-0044"}],
                 "faction_storage": [dict(r, base=OUTPOST, base_name="CLTV Outpost GSC-0044", read_at=stamp) for r in rows]}
        path = self.data / "empire" / "empire.json"
        tmp = path.with_name("empire.json.tmp")
        tmp.write_text(json.dumps(state))
        os.replace(tmp, path)

    def why(self):
        return self.reserves.closed(PLATE, {"data": str(self.data), "now": self.now, "rows": []})

    def test_an_item_a_base_viewed_whole_no_longer_lists_reads_zero_and_opens_the_route(self):
        self.empire(600, [{"item": "circuit_board", "units": 45}])          # the plate is gone from the store
        self.assertIsNone(self.why())
        found = self.reserves.reading(str(self.data), PLATE, [])
        self.assertEqual(found["units"], 0)
        self.empire(600, [{"item": "steel_plate", "units": 180}])          # a row of it stands: the floor decides
        self.assertIn("180", self.why() or "")

    def test_a_base_whose_view_failed_or_a_reading_too_old_still_closes_it(self):
        self.empire(600, [{"item": "circuit_board", "units": 45}], error="CLTV Outpost GSC-0044: timed out")
        self.assertEqual(self.why(), "reserve: not read")
        self.empire(5 * 3600, [{"item": "circuit_board", "units": 45}])
        self.assertIn("not read for", self.why())


if __name__ == "__main__":
    unittest.main()
