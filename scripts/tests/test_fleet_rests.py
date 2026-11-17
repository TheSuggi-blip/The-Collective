"""A losing route rests, never for good (decisions D227, orders D13): the dispatcher's rests on disposable trees; no
engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
H = 3600


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = "home:core:base"
ROUTES = {
    "rays": {"id": "rays", "kind": "hunt", "title": "t", "place": "far:nebula", "sell_at": BASE, "min_bid": 50, "species": ["veil_ray"], "max_ships": 1,
             "min_creatures": 2},
    "curd": {"id": "curd", "kind": "hunt", "title": "t", "place": "far:pool", "sell_at": BASE, "min_bid": 50, "species": ["curd_eel"], "max_ships": 1,
             "min_creatures": 3, "requires": {"bid": {"item": "curd", "base": "base", "min_price": 100, "min_qty": 5}}},
    "ice": {"id": "ice", "kind": "mine", "title": "t", "belt": "far:belt", "station": BASE, "max_ships": 2, "sell": [{"item": "ice", "min_price": 20}],
            "requires": {"bid": {"item": "ice", "base": "base", "min_price": 20, "min_qty": 10}}},
    "ore": {"id": "ore", "kind": "mine", "title": "t", "belt": "far:belt", "station": BASE, "max_ships": 2, "sell": [{"item": "iron_ore", "min_price": 5}],
            "min_left": {"iron_ore": 1000}},
    "carry": {"id": "carry", "kind": "circuit", "title": "t", "max_ships": 1, "stops": [{"at": BASE, "sell": [{"item": "gas", "min_price": 30}]}]},
    "trade": {"id": "trade", "kind": "circuit", "title": "t", "max_ships": 1, "stops": [{"at": "far:dock:depot", "buy": [{"item": "gas", "qty": 10}]},
                                                                                       {"at": BASE, "sell": [{"item": "gas", "min_price": 30}]}]},
    "gather": {"id": "gather", "kind": "mine", "title": "t", "belt": "far:belt", "station": BASE, "max_ships": 4},
    "missions": {"id": "missions", "kind": "circuit", "title": "t", "once": True, "stops": [{"at": BASE}]},
    "mine": {"id": "mine", "kind": "mine", "title": "t", "belt": "far:rift", "station": BASE, "max_ships": 2},
}
PILOT = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True, "goods": 0}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-rests-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.root / "fleet", self.data / "fleet" / "orders", self.data / "routes",
                       self.data / "wildlife", self.data / "scouting", self.data / "market"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nhome\tHome\t0\t0\tvoidborn\nfar\tFar\t1\t0\tvoidborn\n", encoding="ascii")
        for rid, route in ROUTES.items():
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route), encoding="ascii")
        (self.root / "routes" / "plans" / "drone.json").write_text(json.dumps({"role": "drone", "owner": "Apophis", "routes": ["rays", "mine"]}), encoding="ascii")
        self.dispatch = load("dispatch")
        self.now = time.time()
        self.routes = self.dispatch.load_routes(self.root)

    def stamp(self, at):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(at))

    def ran(self, rid, at, delta, minutes=10, **extra):
        """A run of the route that started at `at` (seconds since the epoch) and changed its pilot's wallet by `delta`."""
        return dict({"route": rid, "kind": ROUTES[rid]["kind"], "pilot": "drone-1", "started": self.stamp(at), "minutes": minutes, "credits_before": 20000,
                     "credits_after": 20000 + delta, "one_time": 0, "kills": 2, "notes": []}, **extra)

    def book(self, rows, now, before=None):
        """rest_book on its own: the rests at `now` from the record before and the verdicts the rows give."""
        return self.dispatch.rest_book(self.routes, rows, now, str(self.data), before or {}, self.dispatch.losing(self.routes, rows, now),
                                       self.dispatch.lately_losing(self.routes, rows, now))

    def rest(self, level, start, end, **extra):
        return dict({"from": self.stamp(start), "until": self.stamp(end), "why": "w", "level": level, "net48": -1}, **extra)

    def put_rests(self, book):
        tmp = self.data / "routes" / "rests.json.tmp"                 # moved into place, as the dispatcher writes it
        tmp.write_text(json.dumps(book), encoding="ascii")
        os.replace(tmp, self.data / "routes" / "rests.json")

    def state(self, **extra):
        return dict({"now": self.now, "data": str(self.data), "rows": [], "orders": {}, "rest": {}, "booked": {}, "loss": {}, "late": {}}, **extra)

    def market(self, item, price, qty, age):
        (self.data / "market" / "base.json").write_text(json.dumps({"base": "base", "read_at": self.stamp(self.now - age),
                                                                    "items": [{"item_id": item, "best_buy": price, "best_buy_qty": qty}]}))


class Flying:
    def poll(self):
        return None


class FaultTests(Tree):
    def test_a_route_that_loses_again_after_its_rest_rests_longer_and_the_window_does_not_reopen_it(self):
        # 2026-11-17: 24 judged routes lost again on every opening of the six-hour window (-141,260 cr in 48 hours)
        self.dispatch.ENABLED_RESTS = True
        self.dispatch.spawn = lambda argv, log, env: Flying()
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": "drone-1", "status": "connected", "credits": 20000,
                                                                                "activity": {"kind": "idle"}}]}))
        t0 = self.now
        runs = self.data / "routes" / "runs.jsonl"

        def add(*rows):
            with runs.open("a") as handle:
                handle.write("".join(json.dumps(r) + "\n" for r in rows))
        add(self.ran("rays", t0 - 2 * H, -500), self.ran("rays", t0 - 1 * H, -500))

        def at(moment):
            with mock.patch("time.time", return_value=moment):
                return self.dispatch.one_pass(str(self.root), str(self.data), False, [])

        self.assertIn("drone-1 -> mine mine", at(t0))                                       # it lost over two runs: closed
        self.assertIn("drone-1 -> hunt rays", at(t0 + 6 * H + 60))                         # opened again after six hours
        add(self.ran("rays", t0 + 6 * H + 120, -400), self.ran("rays", t0 + 6 * H + 1200, -400))
        self.assertIn("drone-1 -> mine mine", at(t0 + 7 * H))                              # it lost again on its next opening
        late = at(t0 + 13 * H + 60)                                                         # the six-hour window holds none of those runs now
        self.assertNotIn("drone-1 -> hunt rays", late)
        self.assertIn("drone-1 -> mine mine", late)
        rest = json.loads((self.data / "routes" / "rests.json").read_text())["rays"]
        self.assertEqual((rest["level"], rest["until"]), (2, self.stamp(t0 + 7 * H + 24 * H)))
        self.assertIn("drone-1 -> hunt rays", at(t0 + 31 * H + 60))                        # a rest ends by itself: no hand is needed


class LadderTests(Tree):
    def test_a_route_rests_6_then_24_then_72_hours_and_never_longer(self):
        now, rows, book, seen = self.now, [], {}, []
        for _step in range(4):                                                          # two runs lost, each time after the last rest
            rows += [self.ran("rays", now - 50 * 60, -300), self.ran("rays", now - 30 * 60, -300)]
            book, told = self.book(rows, now, book)
            seen.append((book["rays"]["level"], book["rays"]["until"]))
            self.assertTrue(told and told[0].startswith("rays rests until"))
            self.assertEqual(self.book(rows, now + 60, book)[1], [])                    # a standing rest is not given again
            now = self.dispatch.read_time(book["rays"]["until"]) + H
        self.assertEqual(seen, [(1, self.stamp(self.now + 6 * H)), (2, self.stamp(self.now + 7 * H + 24 * H)),
                                (3, self.stamp(self.now + 32 * H + 72 * H)), (3, self.stamp(self.now + 105 * H + 72 * H))])
        self.assertIn("lost again after its last rest: at a loss: 2 runs, -600 cr in 6 hours", book["rays"]["why"])

    def test_a_route_whose_runs_of_48_hours_paid_in_sum_rests_6_hours(self):
        now = self.now
        rows = [self.ran("rays", now - 40 * H, 9000), self.ran("rays", now - 50 * 60, -300), self.ran("rays", now - 30 * 60, -300)]
        book, _told = self.book(rows, now, {"rays": self.rest(2, now - 30 * H, now - 6 * H)})
        self.assertEqual((book["rays"]["level"], book["rays"]["until"], book["rays"]["net48"]), (1, self.stamp(now + 6 * H), 8400))
        self.assertIn("+8,400 cr over 48 hours keeps it at 6 h", book["rays"]["why"])

    def test_a_rest_that_ended_over_72_hours_ago_is_forgotten(self):
        now = self.now
        rows = [self.ran("rays", now - 50 * 60, -300), self.ran("rays", now - 30 * 60, -300)]
        self.assertEqual(self.book(rows, now, {"rays": self.rest(3, now - 145 * H, now - 73 * H)})[0]["rays"]["level"], 1)
        self.assertEqual(self.book(rows, now, {"rays": self.rest(3, now - 143 * H, now - 71 * H)})[0]["rays"]["level"], 3)
        self.assertEqual(self.book([], now, {"rays": self.rest(1, now - 80 * H, now - 74 * H)})[0], {})      # it decides nothing more

    def test_a_run_that_pays_after_a_rest_sets_its_level_to_0(self):
        now = self.now
        paid = [self.ran("rays", now - 50 * 60, 300)]
        book, told = self.book(paid, now, {"rays": self.rest(2, now - 25 * H, now - 1 * H)})
        self.assertEqual((book["rays"]["level"], book["rays"]["reset"]), (0, self.stamp(now - 50 * 60)))
        self.assertIn("paid after its rest", told[0])
        lost = paid + [self.ran("rays", now - 30 * 60, -400), self.ran("rays", now - 20 * 60, -400)]
        self.assertEqual(self.book(lost, now + 60, book)[0]["rays"]["level"], 1)       # it lost again: of level 1, not 3

    def test_a_verdict_on_runs_its_rest_answered_gives_no_new_rest(self):
        now = self.now
        rows = [self.ran("rays", now - 3 * H, -500), self.ran("rays", now - 2 * H, -500)]   # the runs that sent it to rest
        woke = self.rest(1, now - 90 * 60, now - 30 * 60, woke="x")                           # it woke early; the window still holds them
        book, told = self.book(rows, now, {"rays": woke})
        self.assertEqual((book, told), ({"rays": woke}, []))
        book, _told = self.book(rows + [self.ran("rays", now - 20 * 60, -100)], now, {"rays": woke})     # a new run lost: it rests again
        self.assertEqual(book["rays"]["level"], 2)

    def test_a_route_that_pays_once_and_standing_work_never_rest(self):
        now = self.now
        rows = [self.ran(rid, now - m * 60, -300) for rid in ("missions", "gather") for m in (50, 40, 30)]
        self.assertEqual(self.book(rows, now)[0], {})
        self.dispatch.ENABLED_RESTS = True
        state = self.state(loss=self.dispatch.losing(self.routes, rows, now))
        self.assertEqual(self.dispatch.why_not(PILOT, "missions", self.routes["missions"], state)[0], "at a loss: 3 runs, -900 cr in 6 hours")   # the six-hour stop, as before
        self.assertIsNone(self.dispatch.why_not(PILOT, "gather", self.routes["gather"], state)[0])


class WakeTests(Tree):
    def wake(self, rid):
        book, _told = self.book([], self.now, {rid: self.rest(2, self.now - 1 * H, self.now + 23 * H)})
        return book[rid].get("woke"), book[rid]["until"]

    def test_a_bid_read_back_since_the_rest_began_ends_it(self):
        self.market("ice", 25, 50, age=600)
        self.assertEqual(self.wake("ice"), ("base bids 25 cr x 50 for ice", self.stamp(self.now)))
        self.market("ice", 25, 50, age=2 * H)                                            # read before the rest began: says nothing
        self.assertEqual(self.wake("ice"), (None, self.stamp(self.now + 23 * H)))
        self.market("ice", 15, 50, age=600)                                              # below what the route needs
        self.assertIsNone(self.wake("ice")[0])
        self.market("gas", 40, 9, age=600)
        self.assertEqual(self.wake("carry")[0], "base bids 40 cr x 9 for gas")          # a circuit's sale
        self.assertIsNone(self.wake("trade")[0])                                         # it buys too: its ask has no reader here
        self.routes["siphon"] = dict(ROUTES["ice"], id="siphon", requires={}, sell=[{"item": "gas", "min_price": 1}])
        self.assertIsNone(self.wake("siphon")[0])                                        # a floor of 1 cr names no need: nothing to read

    def test_a_route_that_woke_counts_its_runs_from_the_wake(self):
        self.market("ice", 25, 50, age=600)
        during = [self.ran("ice", self.now - 3 * H, -500), self.ran("ice", self.now - 2 * H, -500)]   # flown by hand while it rested
        before = {"ice": self.rest(1, self.now - 4 * H, self.now + 2 * H)}
        book, told = self.book(during, self.now, before)
        self.assertEqual((book["ice"]["until"], len(told)), (self.stamp(self.now), 1))      # it woke, and no rest is given in the same pass
        self.assertEqual(self.book(during, self.now + 60, book)[1], [])                   # nor at the next one: the wake is newer
        later = during + [self.ran("ice", self.now + 120, -300)]
        self.assertEqual(self.book(later, self.now + 1800, book)[0]["ice"]["level"], 2)    # a run after the wake lost: it rests again

    def test_a_field_above_its_floor_and_a_herd_seen_end_a_rest(self):
        self.market("iron_ore", 8, 100, age=600)
        field = lambda left, age: (self.data / "scouting" / "far.json").write_text(json.dumps({
            "read_at": self.stamp(self.now - age), "pois": {"belt": {"resources": [{"resource_id": "iron_ore", "remaining": left}]}}}))
        field(5000, 300)
        self.assertEqual(self.wake("ore")[0], "base bids 8 cr x 100 for iron_ore; the field at far:belt above its floor")
        field(500, 300)
        self.assertIsNone(self.wake("ore")[0])
        herd = lambda count: (self.data / "wildlife" / "far.json").write_text(json.dumps({"pois": {
            "pool": {"read_at": self.stamp(self.now - 300), "creatures": [{"species": "curd_eel"}] * count},
            "nebula": {"read_at": self.stamp(self.now - 300), "creatures": [{"species": "veil_ray"}] * 9}}}))
        self.market("curd", 120, 10, age=600)
        herd(4)
        self.assertEqual(self.wake("curd")[0], "base bids 120 cr x 10 for curd; 4 creatures at far:pool")
        herd(2)
        self.assertIsNone(self.wake("curd")[0])
        self.assertIsNone(self.wake("rays")[0])                                          # a hunt that names no drop: its sale has no reading


class RuleTests(Tree):
    def test_the_rule_names_the_rest_and_its_end_for_fill_and_a_rest_never_outlives_its_end(self):
        self.dispatch.ENABLED_RESTS = True
        why = lambda **state: self.dispatch.why_not(PILOT, "rays", self.routes["rays"], self.state(**state))[0]
        self.put_rests({"rays": self.rest(2, self.now - 1 * H, self.now + 23 * H, why="lost again after its last rest")})
        self.assertEqual(why(), "resting until %s (24 h, level 2, lost again after its last rest)" % time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(self.now + 23 * H)))
        self.assertIsNone(why(rests={}))                                                 # the dispatcher's own rests of the pass win
        self.put_rests({"rays": self.rest(1, self.now - 80 * H, self.now + 99 * H)})     # an end written by hand past the longest rest
        self.assertIsNone(why())
        self.put_rests({"rays": self.rest(1, self.now - 7 * H, self.now - 1 * H)})
        self.assertIsNone(why(loss={"rays": (2, -1000)}))                               # the verdict rests on runs its rest answered
        self.put_rests({"rays": self.rest(1, self.now - 14 * H, self.now - 8 * H)})
        self.assertEqual(why(loss={"rays": (2, -1000)}), "at a loss: 2 runs, -1,000 cr in 6 hours")      # a new verdict: rest_book rests it next pass

    def test_switched_off_the_dispatcher_decides_as_before(self):
        # The decisions of HEAD 872bb48 on this fixture, a record of standing rests on disk beside it.
        self.put_rests({rid: self.rest(2, self.now - 1 * H, self.now + 23 * H) for rid in ("rays", "ice", "carry", "mine")})
        self.dispatch.ENABLED_RESTS = False
        states = [self.state(loss={"rays": (2, -1000)}, late={"ice": (3, -300)}), self.state(rest={"rays": self.now + 60}),
                  self.state(loss={"missions": (2, -600)}), self.state()]
        got = [[self.dispatch.why_not(PILOT, rid, self.routes.get(rid), state)[0] for rid in sorted(ROUTES) + ["ghost"]] for state in states]
        head = [[None, None, None, "its last 3 runs each lost money: -300 cr", None, None, None, "at a loss: 2 runs, -1,000 cr in 6 hours", None, "no route file"],
                [None, None, None, None, None, None, None, "the place rests", None, "no route file"],
                [None, None, None, None, None, "at a loss: 2 runs, -600 cr in 6 hours", None, None, None, "no route file"],
                [None, None, None, None, None, None, None, None, None, "no route file"]]       # carry curd gather ice mine missions ore rays trade ghost
        self.assertEqual(got, head)
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": "drone-1", "status": "connected", "credits": 20000,
                                                                                "activity": {"kind": "idle"}}]}))
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["drone-1 -> hunt rays"])
        self.dispatch.spawn = lambda argv, log, env: Flying()
        (self.data / "routes" / "rests.json").unlink()
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in (self.ran("rays", self.now - 2 * H, -500), self.ran("rays", self.now - H, -500))))
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), False, []), ["drone-1 -> mine mine"])
        self.assertFalse((self.data / "routes" / "rests.json").exists())                 # off: no record is written

    def test_a_dry_pass_names_the_rests_and_writes_none_and_a_bad_record_stops_no_pass(self):
        self.dispatch.ENABLED_RESTS = True
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": "drone-1", "status": "connected", "credits": 20000,
                                                                                "activity": {"kind": "idle"}}]}))
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in (self.ran("rays", self.now - 2 * H, -500), self.ran("rays", self.now - H, -500))))
        with mock.patch("time.time", return_value=self.now):
            lines = self.dispatch.one_pass(str(self.root), str(self.data), True, [])
        self.assertEqual(lines, ["dry run, not written: rays rests until %s (6 h, level 1, at a loss: 2 runs, -1,000 cr in 6 hours)"
                                 % time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(self.now + 6 * H)), "drone-1 -> mine mine"])
        self.assertFalse((self.data / "routes" / "rests.json").exists())
        with mock.patch.object(self.dispatch, "rest_book", side_effect=ValueError("bad record")):
            lines = self.dispatch.one_pass(str(self.root), str(self.data), True, [])
        self.assertEqual(lines, ["rests not kept this pass: ValueError: bad record", "drone-1 -> mine mine"])   # the six-hour stop still holds


class IdleTests(unittest.TestCase):
    def test_idle_names_the_routes_that_are_off_and_those_no_plan_or_template_holds(self):
        temp = tempfile.TemporaryDirectory(prefix="fleet-idle-test-")
        self.addCleanup(temp.cleanup)
        root, data = Path(temp.name) / "game", Path(temp.name) / "data"
        for folder in (root / "routes" / "plans", root / "routes" / "templates", data / "plans", data / "routes"):
            folder.mkdir(parents=True)
        files = {"a": {"status": "off", "note": "Built for a test. 2026-11-16 09:15 UTC (Apophis): status off. The bid it sold into left."},
                 "b": {}, "c": {}, "d": {}, "e": {}, "f": {"status": "off", "note": "Off: too far."}}
        for rid, extra in files.items():
            (root / "routes" / (rid + ".json")).write_text(json.dumps(dict({"id": rid, "kind": "mine", "title": "t"}, **extra)), encoding="ascii")
        (root / "routes" / "plans" / "miner.json").write_text(json.dumps({"role": "miner", "owner": "Zero", "routes": ["b"]}), encoding="ascii")
        (root / "routes" / "templates" / "mining.json").write_text(json.dumps({"division": "mining", "owner": "Zero", "templates": {"ice": {"routes": ["c"]}}}))
        (data / "plans" / "plan-mining.md").write_text("# plan\n\n## First, for Every Ship\n\n1. d\n\n## Ships\n\n| Ship | Hull | Own routes, in this order |\n"
                                                       "|---|---|---|\n| miner-1 | x | @ice > b |\n")
        (data / "routes" / "runs.jsonl").write_text(json.dumps({"route": "e", "started": "2026-11-17T10:00:00Z", "minutes": 30}) + "\n")
        before = sorted(str(p) for p in Path(temp.name).rglob("*"))
        lines = load("routes").idle(str(root), str(data))
        self.assertEqual(lines[:3], ["OFF: 2 route files with status off, and the sentence of each note that says why:",
                                     "  a (mine): 2026-11-16 09:15 UTC (Apophis): status off. The bid it sold into left.",
                                     "  f (mine): Off: too far."])
        self.assertTrue(lines[4].startswith("UNPLANNED: 3 route files named in no plan"))
        self.assertEqual([line.split() for line in lines[5:]], [["a", "mine", "off", "no", "run", "in", "runs.jsonl"],
                                                                 ["e", "mine", "last", "run", "ended", "2026-11-17T10:30Z"],
                                                                 ["f", "mine", "off", "no", "run", "in", "runs.jsonl"]])
        self.assertEqual(sorted(str(p) for p in Path(temp.name).rglob("*")), before)           # it reads only


if __name__ == "__main__":
    unittest.main()
