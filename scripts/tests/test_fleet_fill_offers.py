"""fill.py offers no stale or forbidden test (Zero, Apophis, 2026-11-21; DECISIONS Q75 (2)): none from a route maker's
list older than a day, none of a route set off or at a place set off for danger, claimed by another division or of
another class; each refusal printed once with its reason. On the disposable tree of test_fleet_fill; no engine."""

import contextlib
import io
import json
from pathlib import Path
import sys
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_fleet_fill import CANDIDATES, HOME, MEASURED, Tree        # noqa: E402  the disposable repository and data folder


class OfferTests(Tree):
    def test_a_list_older_than_a_day_offers_no_test_and_says_so_once(self):
        # Zero, 2026-11-21 19:33 UTC: eight ice tests offered from a list 5,429 minutes old
        self.put_list(CANDIDATES, age=5429 * 60)
        _seen, got = self.read("hauler")
        self.assertEqual(got["tests"], [])
        self.assertIn(("the route maker's list", "90 hours old, over 24 hours: no test of it is offered until the route maker runs again"), got["refused"])
        self.put_list(CANDIDATES, age=23 * 3600)                    # a list of 23 hours still names its tests
        _seen, got = self.read("hauler")
        self.assertEqual([rid for rid, _v, _d, _p in got["tests"]], ["trade-x"])

    def test_a_route_set_off_for_danger_and_its_place_are_offered_to_nobody(self):
        # Apophis, 2026-11-21: the filler offered the Violethall hunt Unity had taken out for a pirate pack
        off = dict(json.loads((self.root / "routes" / "herd2.json").read_text()), status="off",
                   note="2026-11-21 20:35 UTC (Apophis): status off, danger: six pirates at the place.")
        (self.root / "routes" / "herd2.json").write_text(json.dumps(off, indent=1) + "\n", encoding="ascii")
        near = {"id": "hunt-far-cloud-other", "kind": "hunt", "per_ship_hour": 9000, "status": "new", "route_id": "",
                "route": {"id": "hunt-far-cloud-other", "kind": "hunt", "title": "t", "place": "far:cloud2", "sell_at": "home:core:base", "max_ships": 1}}
        old = {"id": "hunt-old", "kind": "hunt", "title": "t", "place": "home:rift", "sell_at": "home:core:base", "max_ships": 1, "status": "off",
               "note": "Set off by its Admiral: the herd is gone."}
        (self.root / "routes" / "hunt-old.json").write_text(json.dumps(old, indent=1) + "\n", encoding="ascii")
        again = {"id": "hunt-old", "kind": "hunt", "per_ship_hour": 8000, "status": "new", "route_id": "hunt-old", "route": dict(old, status="new")}
        self.put_list(CANDIDATES + [near, again])
        _seen, got = self.read("drone")
        offered = [rid for rid, _v, _p in got["paying"]] + [rid for rid, _v, _d, _p in got["tests"]]
        self.assertNotIn("herd2", offered)
        self.assertNotIn("hunt-old", offered)
        self.assertNotIn("hunt-far-cloud-other", offered)              # the old code offered this test at the place set off for danger
        reasons = dict(got["refused"])
        self.assertEqual(reasons["hunt-old"], "set off: Set off by its Admiral: the herd is gone.")
        self.assertEqual(reasons["hunt-far-cloud-other"], "off for danger: herd2, set off for danger, works at far")

    def test_each_refusal_is_printed_once_with_its_reason(self):
        far = dict(json.loads((self.root / "routes" / "freight.json").read_text()), id="far-freight")
        (self.root / "routes" / "far-freight.json").write_text(json.dumps(far, indent=1) + "\n", encoding="ascii")
        (self.top / "communications").mkdir()
        (self.top / "communications" / "admirals.log").write_text(
            "## [ENT-001] | 2026-11-18 00:22 UTC | Zero | claim | ref: game/routes/far-freight.json\nClaims: far-freight (1).\nWhy: a test.\n", encoding="ascii")
        self.put_list(CANDIDATES, age=5429 * 60)
        seen = self.fill.survey(str(self.root), str(self.data))
        seen["kept"] = {}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            for role in ("hauler", "drone"):
                self.fill.show(seen, self.fill.read_role(seen, role))
        text = out.getvalue()
        self.assertEqual(text.count("not offered: far-freight: claimed by another division (admirals.log, rule F25): Zero's"), 1)   # a claim of the 18th stands
        self.assertEqual(text.count("not offered: the route maker's list: 90 hours old"), 1)
        self.assertEqual(text.count("not offered, class: gather is miners' work (rule F23): 1 route: ice"), 1)   # one line per class reason (the list is stale: no test)
        self.assertNotIn("not offered: ice:", text)


if __name__ == "__main__":
    unittest.main()
