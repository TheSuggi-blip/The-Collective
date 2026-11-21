"""The route field `requires.ask` (requests ENT-297): the dispatcher opens a route that buys only while a fresh book shows
the ask, fill.py gives the same reason, routes.py check reads the field. On disposable trees; no engine, no network.

2026-11-21: trade-silver-bar-alpha-to-arneb paid +4,099 cr on its first run, then Node Alpha's ask of 50 bars was gone;
a failed buy does not end a run, and the pilot would have flown 16 jumps empty, so the route had to go off by hand.
"""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test_ask", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ASK = {"item": "silver_bar", "base": "node_alpha_processing_station", "max_price": 415, "min_qty": 50}
ROUTE = {"id": "trade", "kind": "circuit", "title": "t", "requires": {"ask": ASK},
         "stops": [{"at": "home:core:node_alpha_processing_station", "buy": [{"item": "silver_bar", "qty": 50, "max_price": 420}]}]}


class AskTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-requires-ask-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.data / "fleet" / "orders", self.data / "routes", self.data / "market"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nhome\tHome\t0\t0\tvoidborn\n", encoding="ascii")
        (self.root / "routes" / "trade.json").write_text(json.dumps(ROUTE), encoding="ascii")
        park = {"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [{"at": "home:core:base"}]}
        (self.root / "routes" / "park.json").write_text(json.dumps(park), encoding="ascii")
        (self.root / "routes" / "plans" / "trader.json").write_text(json.dumps({"role": "trader", "owner": "Mercury", "routes": ["trade", "park"]}), encoding="ascii")
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": "trader-1", "status": "connected", "credits": 90000, "activity": {"kind": "idle"}}]}))
        self.dispatch = load("dispatch")
        self.now = time.time()

    def book(self, ask, depth, age_minutes=5):
        read = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - age_minutes * 60))
        rows = [{"item_id": "silver_bar", "best_buy": 0, "best_buy_qty": 0, "best_sell": ask, "best_sell_qty": depth, "sell_quantity": depth + 200}]
        (self.data / "market" / "node_alpha_processing_station.json").write_text(json.dumps({"base": "node_alpha_processing_station", "read_at": read, "items": rows}))

    def why(self, route=ROUTE):
        state = {"now": self.now, "data": str(self.data), "rows": [], "orders": {}, "rest": {}, "booked": {}, "loss": {}, "late": {}, "pirates": {}}
        pilot = {"name": "trader-1", "role": "trader", "credits": 90000, "docked": True, "modules": [], "skills": {}, "goods": 0}
        return self.dispatch.why_not(pilot, route["id"], route, state)[0]

    def test_a_route_opens_only_while_a_fresh_book_shows_the_ask_at_or_under_its_price_and_depth(self):
        self.book(414, 50)
        self.assertIsNone(self.why())
        self.book(414, 49)
        self.assertEqual(self.why(), "no ask for silver_bar at node_alpha_processing_station: best 414 cr x 49")   # the fault: open, 16 jumps empty
        self.book(416, 500)
        self.assertEqual(self.why(), "no ask for silver_bar at node_alpha_processing_station: best 416 cr x 500")
        self.book(0, 0)
        self.assertEqual(self.why(), "no ask for silver_bar at node_alpha_processing_station: best 0 cr x 0")      # the ask is gone
        self.book(414, 50, age_minutes=61)
        self.assertEqual(self.why(), "no ask for silver_bar at node_alpha_processing_station: its book not read in 60 minutes")
        self.assertIsNone(self.why(dict(ROUTE, requires={"ask": dict(ASK, max_age_minutes=90)})))                     # its own age
        (self.data / "market" / "node_alpha_processing_station.json").unlink()
        self.assertEqual(self.why(), "no ask for silver_bar at node_alpha_processing_station: its book not read in 60 minutes")
        self.book(300, 10)
        self.assertIsNone(self.why(dict(ROUTE, requires={"ask": [dict(ASK, min_qty=None)]})))                         # a list; min_qty 1

    def test_the_dispatcher_and_fill_give_the_same_reason(self):
        self.book(414, 49)
        lines = self.dispatch.one_pass(str(self.root), str(self.data), True, [])
        self.assertEqual(lines, ["trader-1 -> circuit park"])               # the buy route closed, the pilot goes on down its list
        (self.root / "routes" / "plans" / "trader.json").write_text(json.dumps({"role": "trader", "owner": "Mercury", "routes": ["trade"]}), encoding="ascii")
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), [])
        fill = load("fill")
        seen = fill.survey(str(self.root), str(self.data), self.now)        # the pilot waits: fill names why, in the dispatcher's words
        self.assertEqual([p["name"] for p in seen["crews"]["trader"]["waiting"]], ["trader-1"])
        self.assertEqual(dict(seen["crews"]["trader"]["reasons"].get("trade") or {}), {"no ask for silver_bar at node_alpha_processing_station: best 414 cr x 49": 1})
        self.book(414, 50)
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["trader-1 -> circuit trade"])   # the ask is back: open

    def test_the_gate_reads_the_field(self):
        routes = load("routes")
        self.assertTrue(hasattr(routes, "ask_faults"))
        self.assertEqual(routes.ask_faults(ASK), [])
        self.assertEqual(routes.ask_faults([ASK, dict(ASK, item="gold_bar", max_age_minutes=30)]), [])
        self.assertIn("must be {item, base, max_price", routes.ask_faults("silver_bar")[0])
        self.assertIn("needs `base`", routes.ask_faults({"item": "x", "max_price": 1})[0])
        self.assertIn("needs `max_price`", routes.ask_faults(dict(ASK, max_price=0))[0])
        self.assertIn("`min_qty` must be a whole number", routes.ask_faults(dict(ASK, min_qty=2.5))[0])
        self.assertIn("names fields no reader knows: min_price", routes.ask_faults(dict(ASK, min_price=1))[0])
        errors = [e for e in routes.check(str(self.root))[0] if "index" not in e]
        self.assertEqual(errors, [])
        (self.root / "routes" / "trade.json").write_text(json.dumps(dict(ROUTE, requires={"ask": dict(ASK, max_price=-1)})), encoding="ascii")
        errors = [e for e in routes.check(str(self.root))[0] if "index" not in e]
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("game/routes/trade.json: `requires.ask` of silver_bar needs `max_price`", errors[0])
        self.assertIn("while node_alpha_processing_station asks 415 cr or less for silver_bar", routes.open_to(ROUTE))


if __name__ == "__main__":
    unittest.main()
