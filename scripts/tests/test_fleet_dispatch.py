"""The dispatcher's choice of a route and the route gate, on disposable trees; no engine, no network."""

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
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROUTES = {
    "missions": {"id": "missions", "kind": "circuit", "title": "t", "once": True, "min_credits": 8000, "stops": [{"at": "home:core:base"}]},
    "whale": {"id": "whale", "kind": "hunt", "title": "t", "place": "home:cloud", "sell_at": "home:core:base", "species": ["pilot_whale"],
              "requires": {"module": "railgun"}, "max_ships": 1},
    "rays": {"id": "rays", "kind": "hunt", "title": "t", "place": "far:nebula", "sell_at": "home:core:base", "species": ["veil_ray"], "max_ships": 1, "min_creatures": 2},
    "census": {"id": "census", "kind": "census", "title": "t", "systems": ["home", "far"], "every_minutes": 60, "max_ships": 1},
    "mine": {"id": "mine", "kind": "mine", "title": "t", "belt": "far:belt", "station": "home:core:base", "max_ships": 2},
    "open": {"id": "open", "kind": "mine", "title": "t", "belt": "far:rift", "station": "home:core:base"},
}
PLAN = {"roles": {"drone": ["missions", "whale", "rays", "mine"], "scout": ["missions", "census", "mine"], "miner": ["off-route", "mine"]}}
OWNERS = {"drone": "Apophis", "scout": "Oracle", "miner": "Zero", "hauler": "Apollo", "trader": "Mercury"}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-dispatch-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in (self.root / "routes", self.root / "map", self.root / "fleet", self.data / "fleet" / "orders", self.data / "routes",
                       self.data / "wildlife", self.data / "scouting"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nhome\tHome\t0\t0\tvoidborn\nfar\tFar\t1\t0\tvoidborn\n", encoding="ascii")
        for rid, route in ROUTES.items():
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route), encoding="ascii")
        self.put_plan(PLAN["roles"])
        self.dispatch, self.routes = load("dispatch"), load("routes")
        self.now = time.time()

    def put_plan(self, roles, owner=None):
        folder = self.root / "routes" / "plans"
        folder.mkdir(exist_ok=True)
        for path in folder.glob("*.json"):
            path.unlink()
        for role, ids in roles.items():
            (folder / (role + ".json")).write_text(json.dumps({"role": role, "owner": owner or OWNERS[role], "routes": ids}), encoding="ascii")

    def started(self, hours_ago):
        """A run's `started`, the way the runners write it, this many hours before the test's clock."""
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - hours_ago * 3600))

    def state(self, rows=(), orders=None, rest=None, booked=None):
        return {"now": self.now, "data": str(self.data), "rows": list(rows), "orders": orders or {}, "rest": rest or {}, "booked": booked or {}}

    def pick(self, name, credits=20000, modules=(), docked=False, **state):
        route, argument = self.dispatch.pick({"name": name, "credits": credits, "modules": list(modules), "docked": docked}, PLAN,
                                             self.dispatch.load_routes(self.root), self.state(**state))
        return (route["id"] if route else None), argument


class PirateTests(Tree):
    """Orders D9 (Suggi, 2026-11-17: every ship avoids pirates) and Military's report of 2026-11-17: a hunt flew four runs
    into a place with pirates between two turns, kept whole only by the runner's leave rule."""

    def stamp(self, hours_ago):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - hours_ago * 3600))

    def sightings(self, *rows):
        (self.data / "intel").mkdir(exist_ok=True)
        with open(self.data / "intel" / "sightings.jsonl", "w") as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")

    def test_a_hunt_a_mine_and_a_guard_where_a_pirate_was_seen_within_six_hours_are_closed(self):
        self.sightings({"at": self.stamp(2), "system": "far", "poi": "nebula", "pilots": [], "pirates": 1, "creatures": 3},
                       {"at": self.stamp(1), "system": "home", "poi": "core", "pilots": [], "pirates": 0, "creatures": 0})
        seen = self.dispatch.pirates(str(self.data), self.now)
        self.assertEqual(set(seen), {"far"})
        routes = self.dispatch.load_routes(self.root)
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        state = dict(self.state(), pirates=seen)
        self.assertIn("pirates seen in far", self.dispatch.why_not(pilot, "rays", routes["rays"], state)[0])
        self.assertIn("pirates seen in far", self.dispatch.why_not(pilot, "mine", routes["mine"], state)[0])
        guard = {"id": "watch", "kind": "guard", "title": "t", "guards": "mine", "station": "home:core:base"}
        self.assertIn("pirates seen in far", self.dispatch.why_not(pilot, "watch", guard, dict(state, root=str(self.root), orders={"miner-1": "mine mine"}))[0])
        self.assertIsNone(self.dispatch.why_not(pilot, "missions", routes["missions"], state)[0])      # a circuit at home is not touched
        self.sightings({"at": self.stamp(7), "system": "far", "poi": "nebula", "pilots": [], "pirates": 2, "creatures": 3})
        self.assertEqual(self.dispatch.pirates(str(self.data), self.now), {})                         # older than six hours: open again
        (self.data / "observations").mkdir()
        (self.data / "observations" / "intel.jsonl").write_text(json.dumps({"t": self.stamp(3), "kind": "pirate", "subject": "far", "fields": {}}) + "\n"
                                                                 + json.dumps({"t": self.stamp(1), "kind": "pirate", "subject": "home", "fields": {"last": self.stamp(30)}}) + "\n"
                                                                 + "not json\n")
        self.assertEqual(set(self.dispatch.pirates(str(self.data), self.now)), {"far"})              # a member's line counts; a summary by its last fight


class PickTests(Tree):
    def test_a_once_route_comes_first_and_is_not_flown_again(self):
        self.assertEqual(self.pick("drone-1")[0], "missions")
        whole = {"route": "missions", "pilot": "drone-1", "stops": 1, "of": 1, "notes": ["a mission was not offered"]}
        self.assertEqual(self.pick("drone-1", rows=[whole])[0], "rays")
        self.assertEqual(self.pick("drone-2", rows=[whole])[0], "missions")                       # another pilot's run does not count
        broken = {"route": "missions", "pilot": "drone-1", "stops": 0, "of": 1}
        self.assertEqual(self.pick("drone-1", rows=[broken])[0], "missions")                      # one failed try: once more
        self.assertEqual(self.pick("drone-1", rows=[broken, broken])[0], "rays")                  # two: no third

    def test_a_route_can_name_a_reward_the_pilot_must_hold_first(self):
        routes = self.dispatch.load_routes(self.root)
        shell = dict(routes["missions"], requires={"booked": "First Hunt"}, retry_minutes=60)
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        why = lambda rows=(), booked=None: self.dispatch.why_not(pilot, "missions", shell, self.state(rows=rows, booked=booked or {}))[0]
        self.assertEqual(why(), "needs the reward `First Hunt` first")
        held = {"drone-1": {"First Hunt"}}
        self.assertIsNone(why(booked=held))
        started = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))
        turned = {"route": "missions", "pilot": "drone-1", "stops": 1, "of": 1, "minutes": 5, "started": started(3 * 3600), "notes": ["cracking_the_shell not offered"]}
        self.assertIsNone(why(rows=[turned, dict(turned)], booked=held))                           # flown before it held the reward: no try
        self.assertEqual(why(rows=[dict(turned, started=started(600))], booked=held), "rests after a run the board refused")
        self.assertEqual(why(rows=[turned] * 4, booked=held), "done once")                        # the board keeps refusing: enough
        self.assertEqual(self.dispatch.why_not(pilot, "missions", routes["missions"], self.state(rows=[turned]))[0], "done once")   # no reward named: a refusal ends it

    def test_a_route_can_name_the_skill_levels_a_pilot_must_hold(self):
        routes = self.dispatch.load_routes(self.root)
        shell = dict(routes["missions"], requires={"skills": {"navigation": 3}})
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True, "skills": {"navigation": 2, "piloting": 5}}
        self.assertEqual(self.dispatch.why_not(pilot, "missions", shell, self.state())[0], "needs navigation 3")
        self.assertIsNone(self.dispatch.why_not(dict(pilot, skills={"navigation": 3}), "missions", shell, self.state())[0])
        self.assertEqual(self.dispatch.why_not(dict(pilot, skills={}), "missions", shell, self.state())[0], "needs navigation 3")
        self.assertIn("from navigation 3", self.routes.open_to(shell))
        ships = self.data / "fleet" / "ships"
        ships.mkdir(parents=True, exist_ok=True)
        (ships / "drone-1.json").write_text(json.dumps({"skills": {"navigation": {"level": 3, "xp": 1}, "piloting": {"level": 5}}}), encoding="ascii")
        self.assertEqual(self.dispatch.pilot_of({"name": "drone-1"}, {}, str(self.data), set())["skills"], {"navigation": 3, "piloting": 5})

    def test_standing_work_trains_or_gathers_and_is_never_closed_for_its_fuel(self):
        # Suggi, 2026-11-16: no ship idle. Requests ENT-150, ENT-151: a loop that trains navigation loses its fuel by design
        routes = self.dispatch.load_routes(self.root)
        loop = dict(routes["missions"], id="loop", once=False, min_credits=0, requires={"skills_below": {"navigation": 3}})
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True, "skills": {"navigation": 2}}
        self.assertIsNone(self.dispatch.why_not(pilot, "loop", loop, self.state())[0])
        self.assertEqual(self.dispatch.why_not(dict(pilot, skills={"navigation": 3}), "loop", loop, self.state())[0], "holds navigation 3 already")
        self.assertIn("under navigation 3", self.routes.open_to(loop))
        gather = routes["open"]                                                                   # a mine route that sells nothing
        sold = dict(gather, sell=[{"item": "ore", "min_price": 1}])
        self.assertEqual([self.routes.standing(r) for r in (loop, gather, sold, dict(routes["rays"], standing=True), routes["rays"])], [True, True, False, True, False])
        self.assertEqual((self.routes.stage(gather), self.routes.stage(sold)), ("service", "test"))
        self.assertEqual([self.dispatch.judged(r) for r in (gather, loop, sold, routes["rays"])], [False, False, True, True])
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))
        lost = [{"route": rid, "pilot": "drone-%d" % n, "started": stamp(600 * n), "minutes": 5, "credits_before": 9000, "credits_after": 8900}
                for rid in ("open", "rays") for n in (1, 2, 3)]
        self.assertEqual(sorted(self.dispatch.losing(routes, lost, self.now)), ["rays"])            # the hunt is closed for its losses, the gathering is not
        self.assertEqual(sorted(self.dispatch.lately_losing(routes, lost, self.now)), ["rays"])

    def test_a_field_floor_closes_a_route_until_the_census_reads_the_field_grown_back(self):
        # requests ENT-148: a mission mined a reef that read 0 and pilots kept flying to it; standing work leaves its field enough to regrow
        routes = self.dispatch.load_routes(self.root)
        pilot = {"name": "miner-1", "credits": 20000, "modules": [], "docked": True}
        gather = dict(routes["open"], min_left={"iron_ore": 5000})
        circuit = dict(routes["missions"], once=False, min_credits=0,
                       stops=[{"at": "home:core:base", "mine": [{"at": "far:rift", "minutes": 10, "min_left": {"nickel_ore": 20}}]}])

        def read(iron, nickel, ago=60):
            (self.data / "scouting" / "far.json").write_text(json.dumps({
                "system": "far", "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago)),
                "pois": {"rift": {"kind": "normal", "resources": [{"resource_id": "iron_ore", "remaining": iron}, {"resource_id": "nickel_ore", "remaining": nickel}]}}}))

        self.assertIsNone(self.dispatch.why_not(pilot, "open", gather, self.state())[0])           # no census: nothing is known, nothing is closed
        read(4999, 0)
        self.assertEqual(self.dispatch.why_not(pilot, "open", gather, self.state())[0], "field below 5,000 iron_ore at far:rift")
        self.assertEqual(self.dispatch.why_not(pilot, "missions", circuit, self.state())[0], "field below 20 nickel_ore at far:rift")
        self.assertEqual(self.dispatch.field_left(str(self.data), "far:rift", self.now), {"iron_ore": 4999, "nickel_ore": 0})
        read(5000, 20)                                                                             # grown back: open again by itself
        self.assertIsNone(self.dispatch.why_not(pilot, "open", gather, self.state())[0])
        self.assertIsNone(self.dispatch.why_not(pilot, "missions", circuit, self.state())[0])
        read(10, 0, ago=2 * 3600)                                                                  # an old census says nothing
        self.assertIsNone(self.dispatch.why_not(pilot, "open", gather, self.state())[0])
        for wrong in (dict(routes["open"], min_left=5000), dict(routes["open"], requires={"skills_below": ["navigation"]})):
            (self.root / "routes" / "open.json").write_text(json.dumps(wrong), encoding="ascii")
            errors, _count = self.routes.check(str(self.root))
            self.assertTrue(any("game/routes/open.json" in e and ("min_left" in e or "skills_below" in e) for e in errors), errors)

    def test_a_route_that_names_a_bid_is_closed_while_a_fresh_book_shows_none(self):
        # requests ENT-065, ENT-125: the curd bid left every station and the hunts flew on; the near ice bids emptied
        routes = self.dispatch.load_routes(self.root)
        rays = dict(routes["rays"], requires={"bid": {"item": "verdigris_curd", "base": "base", "min_price": 100}})
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        why = lambda route=rays: self.dispatch.why_not(pilot, "rays", route, self.state())[0]
        market = self.data / "market"
        market.mkdir(exist_ok=True)
        book = lambda price, qty, ago=60: (market / "base.json").write_text(json.dumps({"base": "base", "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago)),
                                                                              "items": [{"item_id": "verdigris_curd", "best_buy": price, "best_buy_qty": qty}]}))
        self.assertIsNone(why())                                                                   # no book: nothing known, nothing closed
        book(0, 0)
        self.assertEqual(why(), "no bid for verdigris_curd at base: best 0 cr x 0")
        book(330, 50)
        self.assertIsNone(why())
        book(90, 50)
        self.assertEqual(why(), "no bid for verdigris_curd at base: best 90 cr x 50")
        book(0, 0, ago=2 * 3600)
        self.assertIsNone(why())                                                                   # a book two hours old says nothing
        book(330, 3)
        deep = dict(rays, requires={"bid": [{"item": "verdigris_curd", "base": "base", "min_price": 100, "min_qty": 10}]})
        self.assertEqual(why(deep), "no bid for verdigris_curd at base: best 330 cr x 3")       # a list, and a depth asked
        mine = dict(routes["mine"], requires={"bid": {"item": "water_ice", "base": "base", "min_price": 20}})
        self.assertEqual(self.dispatch.why_not(pilot, "mine", mine, self.state())[0], "no bid for water_ice at base: best 0 cr x 0")

    def test_a_carry_route_goes_only_to_a_pilot_whose_storage_holds_a_load(self):
        # Zero, requests ENT-117: storage is personal; only the pilot that stored the ice can carry it
        routes = self.dispatch.load_routes(self.root)
        carry = dict(routes["missions"], id="missions", once=False, requires={"stored": {"at": "base", "item": "water_ice", "min": 60}})
        pilot = {"name": "miner-1", "credits": 20000, "modules": [], "docked": True}
        stock = self.data / "stock"
        stock.mkdir(exist_ok=True)
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))
        put = lambda qty, ago=60: (stock / "storage.json").write_text(json.dumps({"pilots": {"miner-1": {"read_at": stamp(ago), "stations": {"base": {"water_ice": qty}}}}}))
        why = lambda rows=(), who=pilot: self.dispatch.why_not(who, "missions", carry, self.state(rows=rows))[0]
        self.assertEqual(why(), "stores 0 water_ice at base, 60 wanted")                             # no storage file
        put(59)
        self.assertEqual(why(), "stores 59 water_ice at base, 60 wanted")
        put(65)
        self.assertIsNone(why())
        self.assertEqual(why(who=dict(pilot, name="miner-2")), "stores 0 water_ice at base, 60 wanted")    # another pilot's load is not its own
        ran = {"route": "missions", "pilot": "miner-1", "stops": 1, "of": 1, "started": stamp(30)}
        self.assertEqual(why(rows=[ran]), "storage not read since its last run")                  # the reading is older than the run
        self.assertIsNone(why(rows=[dict(ran, started=stamp(120))]))

    def test_a_circuit_hunt_step_with_a_herd_floor_waits_for_its_herd(self):
        # Apophis, report of 2026-11-16 05:27 UTC; requests ENT-126
        shell = {"id": "shell", "kind": "circuit", "title": "t", "once": True, "stops": [
            {"at": "home:core:base", "hunt": [{"at": "far:nebula", "species": ["veil_ray"], "kills": 3, "min_creatures": 3}]}, {"at": "home:core:base"}]}
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        why = lambda: self.dispatch.why_not(pilot, "shell", shell, self.state())[0]
        self.assertIsNone(why())                                                                   # no census: nothing known
        census = self.data / "wildlife" / "far.json"
        census.write_text(json.dumps({"pois": {"nebula": {"creatures": [{"species": "veil_ray"}, {"species": "veil_ray"}, {"species": "belt_grazer"}]}}}))
        self.assertEqual(why(), "herd below 3 at far:nebula")
        census.write_text(json.dumps({"pois": {"nebula": {"creatures": [{"species": "veil_ray"}] * 3}}}))
        self.assertIsNone(why())

    def test_a_once_run_whose_every_stop_was_skipped_is_no_try_and_the_route_rests(self):
        # requests ENT-129: four traders flew runs of 0 minutes that counted as done
        started = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))
        nothing = {"route": "missions", "pilot": "drone-1", "stops": 1, "of": 1, "minutes": 0.0, "started": started(600), "notes": ["every stop skipped"]}
        routes = self.dispatch.load_routes(self.root)
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        why = lambda rows: self.dispatch.why_not(pilot, "missions", routes["missions"], self.state(rows=rows))[0]
        self.assertEqual(why([nothing]), "rests after a run with every stop skipped")
        self.assertEqual(why([dict(nothing, started=started(2 * 3600))] * 3), None)              # three empty runs are still no try
        self.assertEqual(why([dict(nothing, notes=[], started=started(2 * 3600))]), "done once")

    def test_an_engine_loop_no_runner_owns_is_named_after_five_minutes(self):
        # Zero, requests ENT-083
        fleet = {"ships": [{"name": "miner-1", "status": "connected", "activity": {"kind": "loop"}},
                           {"name": "miner-2", "status": "connected", "activity": {"kind": "loop"}},
                           {"name": "miner-3", "status": "connected", "activity": {"kind": "idle"}}]}
        seen = {}
        self.assertEqual(self.dispatch.orphans(fleet, {"miner-2": "mine mine"}, self.now, seen), [])
        self.assertEqual(self.dispatch.orphans(fleet, {"miner-2": "mine mine"}, self.now + 299, seen), [])
        self.assertEqual(self.dispatch.orphans(fleet, {"miner-2": "mine mine"}, self.now + 300, seen), ["miner-1"])
        fleet["ships"][0]["activity"] = {"kind": "idle"}
        self.assertEqual(self.dispatch.orphans(fleet, {}, self.now + 400, seen), [])              # the loop ended: forgotten
        self.assertNotIn("miner-1", seen)
        self.assertEqual(self.dispatch.orphans(fleet, {}, self.now + 400, seen), [])              # miner-2 lost its order: a new sighting
        self.assertEqual(self.dispatch.orphans(fleet, {}, self.now + 700, seen), ["miner-2"])

    def test_a_pilot_whose_last_three_runs_ended_before_stop_one_is_held_back(self):
        failed = {"route": "park", "pilot": "drone-1", "stops": 0, "of": 1, "notes": ["stop 1 not reached"]}
        self.assertFalse(self.dispatch.stuck("drone-1", [failed, failed]))
        self.assertTrue(self.dispatch.stuck("drone-1", [failed, failed, failed]))
        self.assertFalse(self.dispatch.stuck("drone-1", [failed, failed, failed, dict(failed, stops=1, notes=[])]))
        self.assertFalse(self.dispatch.stuck("drone-2", [failed] * 3))
        timed = dict(failed, started="2026-11-17T00:00:00Z", minutes=1.0)                         # 2026-11-17: the hold ends by itself, no ship waits for a hand
        at = 1794873660                                                                           # 00:01:00 UTC that day: the run's end
        self.assertTrue(self.dispatch.stuck("drone-1", [failed, failed, timed], at + 29 * 60))
        self.assertFalse(self.dispatch.stuck("drone-1", [failed, failed, timed], at + 31 * 60))   # half an hour later it is given one route again
        self.assertTrue(self.dispatch.stuck("drone-1", [failed, failed, failed], at + 31 * 60))   # a last run without a time: held

    def test_credits_module_and_ship_limits_close_a_route(self):
        done = [{"route": "missions", "pilot": "drone-1", "stops": 1, "of": 1}]
        self.assertEqual(self.pick("drone-1", credits=5000)[0], "rays")                           # too poor for the missions
        self.assertEqual(self.pick("drone-1", modules=["railgun"], rows=done)[0], "whale")
        self.assertEqual(self.pick("drone-1", modules=["railgun"], rows=done, orders={"drone-9": "hunt whale"})[0], "rays")
        self.assertEqual(self.pick("drone-1", rows=done, orders={"drone-9": "hunt rays"})[0], "mine")
        self.assertEqual(self.pick("drone-1", rows=done, orders={"drone-9": "hunt rays", "a-1": "mine mine", "a-2": "mine mine"})[0], None)

    def test_a_hunt_rests_after_a_run_without_a_kill_and_needs_a_herd(self):
        done = [{"route": "missions", "pilot": "drone-1", "stops": 1, "of": 1}]
        self.assertEqual(self.pick("drone-1", rows=done, rest={"rays": self.now + 60})[0], "mine")
        (self.data / "wildlife" / "far.json").write_text(json.dumps({"pois": {"nebula": {"creatures": [{"species": "veil_ray"}, {"species": "belt_grazer"}]}}}))
        self.assertEqual(self.pick("drone-1", rows=done)[0], "mine")                              # one ray counted, two wanted
        os.utime(self.data / "wildlife" / "far.json", (self.now - 3 * 3600, self.now - 3 * 3600))
        self.assertEqual(self.pick("drone-1", rows=done)[0], "rays")                              # an old census says nothing
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - 600))
        rest = self.dispatch.resting(self.dispatch.load_routes(self.root), [{"route": "rays", "kills": 0, "started": started, "minutes": 5}], self.now)
        self.assertAlmostEqual(rest["rays"], self.now - 600 + 300 + 1800, delta=2)
        self.assertEqual(self.dispatch.resting(self.dispatch.load_routes(self.root), [{"route": "rays", "kills": 3, "started": started, "minutes": 5}], self.now), {})

    def test_a_once_run_that_found_nothing_to_buy_is_no_run_and_the_route_rests(self):
        started = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))
        empty = {"route": "missions", "pilot": "drone-1", "stops": 1, "of": 1, "minutes": 1, "started": started(600), "notes": ["ice_harvester_i: not bought"]}
        self.assertEqual(self.pick("drone-1", rows=[empty])[0], "rays")                           # ten minutes ago: the route rests
        routes = self.dispatch.load_routes(self.root)
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        self.assertEqual(self.dispatch.why_not(pilot, "missions", routes["missions"], self.state(rows=[empty]))[0], "rests after a buy that found no offer")
        old = dict(empty, started=started(2 * 3600))
        self.assertEqual(self.pick("drone-1", rows=[old])[0], "missions")                         # after the rest: once more
        self.assertEqual(self.pick("drone-1", rows=[old, dict(old), dict(old)])[0], "missions")   # three empty runs are still no finished run
        bought = dict(old, notes=[])
        self.assertEqual(self.pick("drone-1", rows=[old, bought])[0], "rays")                     # the run that bought is the finished one

    def test_a_route_that_lost_money_over_two_runs_is_closed_until_the_window_moves_on(self):
        routes = self.dispatch.load_routes(self.root)
        run = lambda rid, ago, delta, once=0: {"route": rid, "pilot": "p", "minutes": 10, "credits_before": 9000, "credits_after": 9000 + delta, "one_time": once,
                                               "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))}
        losing = lambda *rows: self.dispatch.losing(routes, list(rows), self.now)
        self.assertEqual(losing(run("rays", 600, 105), run("rays", 300, -4635)), {"rays": (2, -4530)})
        self.assertEqual(losing(run("rays", 600, -4635)), {})                                      # one run is no verdict
        unread = dict(run("rays", 200, 0), credits_after=0)                                       # the engine did not answer at the run's end: no reading
        self.assertEqual(losing(run("rays", 600, 105), unread), {})
        self.assertEqual(losing(run("rays", 600, 900), run("rays", 300, -90)), {})                 # it paid in sum
        unsold = lambda ago: dict(run("rays", ago, -120), notes=["not docked for the sale: 500 already executing"])
        self.assertEqual(losing(unsold(900), unsold(600), unsold(300)), {})                        # the runner failed, not the route
        self.assertEqual(losing(unsold(900), run("rays", 600, -200), run("rays", 300, -300)), {"rays": (2, -500)})
        self.assertEqual(losing(dict(run("rays", 600, -50), notes=["crashed: TypeError: x (line 9)"]), run("rays", 300, -300)), {})
        self.assertEqual(losing(run("rays", 8 * 3600, -500), run("rays", 7 * 3600, -500)), {})     # the window has moved on
        self.assertEqual(losing(run("rays", 600, 2000, 3000), run("rays", 300, -100)), {"rays": (2, -1100)})   # a reward paid once is no pay of a repeating route
        self.assertEqual(losing(run("missions", 600, 2000, 3000), run("missions", 300, -100)), {})             # a route that pays once is judged with its reward
        self.assertEqual(losing(run("missions", 600, -300), run("missions", 300, -300)), {"missions": (2, -600)})
        self.assertEqual(losing(run("census", 600, -300), run("census", 300, -300), run("ghost", 600, -9), run("ghost", 300, -9)), {})   # a patrol is not judged; a route without a file is none
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        state = dict(self.state(), loss=losing(run("rays", 600, 105), run("rays", 300, -4635)))
        self.assertEqual(self.dispatch.why_not(pilot, "rays", routes["rays"], state)[0], "at a loss: 2 runs, -4,530 cr in 6 hours")
        route, _argument = self.dispatch.pick(pilot, PLAN, routes, dict(self.state(), loss={"missions": (2, -600)}))
        self.assertEqual(route["id"], "rays")                                                    # the first route of the plan is closed: the next open one is taken

    def test_a_repeating_route_whose_last_three_runs_each_lost_is_closed(self):
        # the six-hour sum held the good runs from before a bid left (errors ENT-046; requests ENT-125)
        routes = self.dispatch.load_routes(self.root)
        run = lambda rid, ago, delta, once=0: {"route": rid, "pilot": "p", "minutes": 10, "credits_before": 9000, "credits_after": 9000 + delta, "one_time": once,
                                               "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - ago))}
        late = lambda *rows: self.dispatch.lately_losing(routes, list(rows), self.now)
        good = [run("rays", 5 * 3600 - 60 * i, 3000) for i in range(5)]
        bad = [run("rays", 3000, -90), run("rays", 2000, -80), run("rays", 1000, -70)]
        self.assertEqual(self.dispatch.losing(routes, good + bad, self.now), {})                   # the six-hour sum still pays
        self.assertEqual(late(*(good + bad)), {"rays": (3, -240)})
        self.assertEqual(late(*(good + bad[:2])), {})                                             # two losing runs are no verdict
        self.assertEqual(late(*(good + bad + [run("rays", 500, 40)])), {})                       # a newer run paid
        self.assertEqual(late(*[dict(r, started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - 7 * 3600 + i))) for i, r in enumerate(bad)]), {})
        self.assertEqual(late(run("missions", 300, -50), run("missions", 200, -50), run("missions", 100, -50)), {})   # a once route: its reward is its pay
        self.assertEqual(late(run("census", 300, -50), run("census", 200, -50), run("census", 100, -50)), {})        # a patrol is not judged
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        state = dict(self.state(), late=late(*(good + bad)))
        self.assertEqual(self.dispatch.why_not(pilot, "rays", routes["rays"], state)[0], "its last 3 runs each lost money: -240 cr")

    def test_the_rule_says_why_a_route_is_closed(self):
        routes, pilot = self.dispatch.load_routes(self.root), {"name": "drone-1", "credits": 5000, "modules": [], "docked": True}
        why = lambda rid, **state: self.dispatch.why_not(pilot, rid, routes.get(rid), self.state(**state))[0]
        self.assertEqual(why("missions"), "wallet below 8000 cr")
        self.assertEqual(why("whale"), "needs railgun")
        self.assertEqual(why("rays", orders={"drone-9": "hunt rays"}), "max_ships 1 reached")
        self.assertEqual(why("rays", rest={"rays": self.now + 60}), "the place rests")
        self.assertEqual(why("ghost"), "no route file")
        self.assertEqual(why("open"), None)                                                       # open: no reason
        self.assertEqual(self.dispatch.why_not(dict(pilot, name="scout-1"), "census", routes["census"], self.state()), (None, "home"))

    def test_a_census_takes_the_stalest_system_nobody_reads(self):
        done = [{"route": "missions", "pilot": "scout-1", "stops": 1, "of": 1}]
        (self.data / "scouting" / "home.json").write_text("{}")
        os.utime(self.data / "scouting" / "home.json", (self.now - 7200, self.now - 7200))
        self.assertEqual(self.pick("scout-1", rows=done), ("census", "far"))                      # never read beats two hours old
        (self.data / "scouting" / "far.json").write_text("{}")
        self.assertEqual(self.pick("scout-1", rows=done), ("census", "home"))
        self.assertEqual(self.pick("scout-1", rows=done, orders={"scout-2": "census home"})[0], "mine")   # max_ships 1
        os.utime(self.data / "scouting" / "home.json", (self.now - 60, self.now - 60))
        self.assertEqual(self.pick("scout-1", rows=done)[0], "mine")                              # everything fresh

    def test_a_park_route_is_for_a_pilot_in_space_and_a_booked_reward_skips_its_route(self):
        routes = dict(self.dispatch.load_routes(self.root))
        routes["park"] = {"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [{"at": "home:core:base"}]}
        routes["gift"] = {"id": "gift", "kind": "circuit", "title": "t", "once": True, "skip_if_booked": ["Iron Supply Run"], "stops": [{"at": "home:core:base"}]}
        plan = {"roles": {"hauler": ["gift", "park"]}}
        pick = lambda docked, booked=None: (self.dispatch.pick({"name": "hauler-1", "credits": 9000, "modules": [], "docked": docked}, plan, routes,
                                                                self.state(booked=booked))[0] or {}).get("id")
        self.assertEqual(pick(False), "gift")
        self.assertEqual(pick(False, {"hauler-1": {"Iron Supply Run"}}), "park")                  # the reward is booked: not flown again
        self.assertEqual(pick(False, {"hauler-2": {"Iron Supply Run"}}), "gift")                  # another pilot's booking does not count
        self.assertEqual(pick(True, {"hauler-1": {"Iron Supply Run"}}), None)                     # docked: it waits, nothing is started
        (self.data / "fleet" / "onetime.json").write_text(json.dumps([[1, "hauler-1", "Iron Supply Run", 1500], [2, "hauler-1", "Copper Requisition", 1800], "broken"]))
        self.assertEqual(self.dispatch.booked(str(self.data)), {"hauler-1": {"Iron Supply Run", "Copper Requisition"}})

    def test_a_census_order_counts_for_the_route_that_lists_its_system(self):
        routes = dict(self.dispatch.load_routes(self.root))
        routes["frontier"] = {"id": "frontier", "kind": "census", "title": "t", "systems": ["wild", "waste"], "every_minutes": 60, "max_ships": 1}
        plan = {"roles": {"scout": ["census", "frontier", "mine"]}}
        pick = lambda orders: (self.dispatch.pick({"name": "scout-1", "credits": 9000, "modules": [], "docked": True}, plan, routes,
                                                   self.state(orders=orders))[0] or {}).get("id")
        self.assertEqual(pick({}), "census")
        self.assertEqual(pick({"flag-1": "census wild"}), "census")              # a ship on the other census route takes no place here
        self.assertEqual(pick({"scout-2": "census far"}), "frontier")             # this route is full: the next one
        self.assertEqual(pick({"scout-2": "census far", "flag-1": "census waste"}), "mine")

    def test_a_route_beyond_the_police_wants_an_empty_hold_and_a_hunter_that_leaves(self):
        routes = {"far": {"id": "far", "kind": "hunt", "title": "t", "place": "far:belt", "sell_at": "home:core:base", "alone": True,
                          "requires": {"empty_hold": True}}, "mine": dict(ROUTES["mine"])}
        plan = {"roles": {"drone": ["far", "mine"]}}
        pick = lambda goods: (self.dispatch.pick({"name": "drone-1", "credits": 9000, "modules": [], "docked": True, "goods": goods}, plan, routes,
                                                 self.state())[0] or {}).get("id")
        self.assertEqual((pick(0), pick(21)), ("far", "mine"))                                    # goods aboard: not sent out
        routes["stash"] = {"id": "stash", "kind": "circuit", "title": "t", "stops": [{"at": "home:core:base", "store": "all"}], "requires": {"hold": True}}
        plan = {"roles": {"drone": ["stash", "far", "mine"]}}                                     # Zero, 2026-11-16: store what is aboard, then the route beyond the border
        self.assertEqual((pick(0), pick(5), pick(21)), ("far", "far", "stash"))
        self.assertEqual(self.dispatch.why_not({"name": "drone-1", "credits": 9000, "modules": [], "docked": True, "goods": 0}, "stash", routes["stash"], self.state())[0], "nothing aboard")
        self.assertIn("--alone", self.dispatch.command(routes["far"], "drone-1", None, str(self.root)))
        self.assertNotIn("--alone", self.dispatch.command(ROUTES["rays"], "drone-1", None, str(self.root)))

    def test_a_mine_route_names_what_it_sells_and_a_fitting_route_is_for_a_pilot_without_the_module(self):
        mine = dict(ROUTES["mine"], sell=[{"item": "ice", "min_price": 20}, {"item": "gas", "min_price": 5}], requires={"without_module": "drill"})
        self.assertEqual(self.dispatch.command(mine, "miner-1", None, str(self.root))[-2:], ["--sell-items", "ice:20,gas:5"])
        self.assertNotIn("--sell-items", self.dispatch.command(ROUTES["mine"], "miner-1", None, str(self.root)))
        lacks = lambda modules: (self.dispatch.pick({"name": "drone-1", "credits": 9000, "modules": modules, "docked": True, "goods": 0},
                                                    {"roles": {"drone": ["mine"]}}, {"mine": mine}, self.state())[0] or {}).get("id")
        self.assertEqual((lacks([]), lacks(["drill"])), ("mine", None))
        few = dict(ROUTES["mine"], max_pilots=2)
        seat = lambda name, rows=(), orders=None: (self.dispatch.pick({"name": name, "credits": 9000, "modules": [], "docked": True, "goods": 0},
                                                                    {"roles": {"drone": ["mine"]}}, {"mine": few}, self.state(rows=rows, orders=orders))[0] or {}).get("id")
        flown = [{"route": "mine", "pilot": "drone-1"}]
        self.assertEqual((seat("drone-3", flown), seat("drone-3", flown, {"drone-2": "mine mine"}), seat("drone-1", flown, {"drone-2": "mine mine"})),
                         ("mine", None, "mine"))                                                     # two pilots have it: a third gets none, the two keep it

    def test_a_route_the_plan_names_but_no_file_holds_is_passed_over(self):
        self.assertEqual(self.pick("miner-1")[0], "mine")
        self.assertEqual(self.pick("hauler-1")[0], None)                                          # a role without a list

    def test_the_command_names_the_runner_and_the_route(self):
        routes = self.dispatch.load_routes(self.root)
        self.assertEqual(self.dispatch.command(routes["missions"], "drone-1", None, str(self.root))[3:],
                         [str(self.root / "fleet" / "route_run.py"), "drone-1", str(self.root / "routes" / "missions.json")])
        hunt = self.dispatch.command(routes["rays"], "drone-1", None, str(self.root))
        self.assertEqual(hunt[4:7], ["drone-1", "far", "nebula"])
        self.assertEqual(hunt[hunt.index("--route") + 1], "rays")
        self.assertEqual(hunt[hunt.index("--species") + 1], "veil_ray")
        self.assertEqual(self.dispatch.command(routes["census"], "scout-1", "far", str(self.root))[4:], ["scout-1", "far", "--stay", "--route", "census"])
        self.assertEqual(self.dispatch.command(routes["mine"], "miner-1", None, str(self.root))[4:7], ["miner-1", "far:belt", "home:core:base"])


class PassTests(Tree):
    def fleet(self, ships):
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))

    def test_a_dry_pass_names_one_task_per_free_pilot_and_starts_nothing(self):
        self.fleet([{"name": "miner-1", "status": "connected", "credits": 9000, "activity": {"kind": "idle"}},
                    {"name": "miner-2", "status": "connected", "credits": 9000, "activity": {"kind": "goal"}},
                    {"name": "miner-3", "status": "disconnected", "credits": 9000, "activity": {"kind": "idle"}},
                    {"name": "miner-4", "status": "connected", "credits": 9000, "activity": {"kind": "idle"}}])
        (self.data / "fleet" / "orders" / "miner-4.json").write_text(json.dumps({"pilot": "miner-4", "what": "mine mine"}))
        children = []
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, children), ["miner-1 -> mine mine"])
        self.assertEqual(children, [])
        self.assertEqual(sorted(p.name for p in (self.data / "fleet" / "orders").iterdir()), ["miner-4.json"])

    def test_a_flagship_takes_the_role_its_entry_names(self):
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({"Zero Point": {"admiral": "Zero", "division": "Mining", "role": "miner"}, "broken": "x"}))
        named = self.dispatch.flagships(str(self.data))
        self.assertEqual(sorted(named), ["Zero Point"])
        self.assertEqual([self.dispatch.role_of(n, named) for n in ("Zero Point", "miner-3", "No Role Ship")], ["miner", "miner", "No Role Ship"])
        self.assertEqual(self.dispatch.ship_file("Zero Point"), "Zero_Point.json")              # the collector's rule: no space in a file name
        self.assertEqual(self.dispatch.ship_file("miner-3"), "miner-3.json")
        self.fleet([{"name": "Zero Point", "status": "connected", "credits": 9000, "activity": {"kind": "idle"}},
                    {"name": "No Role Ship", "status": "connected", "credits": 9000, "activity": {"kind": "idle"}}])
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["Zero Point -> mine mine"])   # a ship without a role gets nothing
        self.assertEqual(self.dispatch.flagships(str(self.root)), {})                             # no file: no flagship

    def test_the_stop_file_halts_every_start_and_a_dead_order_frees_its_pilot(self):
        self.fleet([{"name": "miner-4", "status": "connected", "credits": 9000, "activity": {"kind": "idle"}}])
        order = self.data / "fleet" / "orders" / "miner-4.json"
        order.write_text(json.dumps({"pilot": "miner-4", "what": "mine mine"}))
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), [])
        os.utime(order, (self.now - 3600, self.now - 3600))
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["miner-4 -> mine mine"])
        (self.data / "fleet" / "STOP").write_text("")
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["STOP file present: nothing started"])


class Flying:
    """A runner process that has not ended, as the dispatcher's reaping sees it."""

    def poll(self):
        return None


class HostingTests(PassTests):
    """Which runs go to the host (game/fleet/runhost.py: threads of one program) and which stay processes."""

    def setUp(self):
        super().setUp()
        self.spawned = []
        self.dispatch.spawn = lambda argv, log, env: self.spawned.append((argv, str(log), env)) or Flying()
        self.home = self.data / "fleet" / "host"
        self.idle = lambda *names: self.fleet([{"name": n, "status": "connected", "credits": 9000, "activity": {"kind": "idle"}} for n in names])

    def hosting(self, **what):
        (self.data / "fleet" / "hosting.json").write_text(json.dumps(what))

    def host(self, accepting=True, runs=0, age=0.0):
        self.home.mkdir(parents=True, exist_ok=True)
        (self.home / "state.json").write_text(json.dumps({"at": time.time() - age, "accepting": accepting, "runs": runs}))

    def inbox(self):
        folder = self.home / "inbox"
        return {p.stem: json.loads(p.read_text()) for p in sorted(folder.glob("*.json"))} if folder.is_dir() else {}

    def real_pass(self):
        children = []
        return self.dispatch.one_pass(str(self.root), str(self.data), False, children), children

    def test_without_a_hosting_file_every_run_is_a_process_as_before(self):
        self.idle("miner-1")
        self.host()                                                          # a host that runs changes nothing by itself
        lines, children = self.real_pass()
        self.assertEqual((lines, len(children), self.inbox()), (["miner-1 -> mine mine"], 1, {}))
        argv, log, env = self.spawned[0]
        self.assertEqual(argv[1:7], ["-I", "-B", str(self.root / "fleet" / "mine.py"), "miner-1", "far:belt", "home:core:base"])
        self.assertEqual((log, env["FLEET_HOLD"], env["FLEET_MEMBER"]), (str(self.data / "routes" / "logs" / "miner-1.log"), "mine mine", "dispatch"))

    def test_a_kind_the_hosting_file_names_goes_to_a_host_that_accepts(self):
        self.idle("miner-1")
        self.hosting(kinds=["mine"])
        self.host()
        lines, children = self.real_pass()
        self.assertEqual((lines, children, self.spawned), (["miner-1 -> mine mine"], [], []))
        job = self.inbox()["miner-1"]
        self.assertEqual((job["pilot"], job["what"], job["script"], job["argv"][:3]), ("miner-1", "mine mine", "mine.py", ["miner-1", "far:belt", "home:core:base"]))
        self.assertEqual(job["env"], {"FLEET_MEMBER": "dispatch", "FLEET_HOLD": "mine mine"})
        self.assertEqual(json.loads((self.data / "fleet" / "orders" / "miner-1.json").read_text())["what"], "mine mine")   # the order is written first

    def test_a_host_that_is_away_or_full_or_a_kind_not_named_leaves_the_run_a_process(self):
        self.idle("miner-1")
        for hosting, host in (({"kinds": ["mine"]}, None), ({"kinds": ["mine"]}, {"accepting": False}), ({"kinds": ["mine"]}, {"age": 120}),
                              ({"kinds": ["circuit"]}, {}), ({"kinds": "mine"}, {}), ({"kinds": ["mine"], "max_runs": 3}, {"runs": 3})):
            self.hosting(**hosting)
            (self.home / "state.json").unlink(missing_ok=True)
            if host is not None:
                self.host(**host)
            (self.data / "fleet" / "orders" / "miner-1.json").unlink(missing_ok=True)
            del self.spawned[:]
            self.real_pass()
            self.assertEqual((len(self.spawned), self.inbox()), (1, {}), (hosting, host))

    def test_the_hosting_file_can_cap_the_runs_the_host_is_given(self):
        self.idle("miner-1", "miner-2")                                      # the route `mine` takes two ships
        self.hosting(kinds=["mine"], max_runs=2)
        self.host(runs=1)
        self.real_pass()
        self.assertEqual((sorted(self.inbox()), [argv[4] for argv, _log, _env in self.spawned]), (["miner-1"], ["miner-2"]))

    def test_a_job_the_host_did_not_take_in_a_minute_is_started_as_a_process_when_its_order_still_names_it(self):
        self.idle()
        runhost = self.dispatch.runhost
        for pilot, order in (("miner-1", "mine mine"), ("miner-2", "hand Zero"), ("miner-3", "mine mine")):
            (self.data / "fleet" / "orders" / (pilot + ".json")).write_text(json.dumps({"pilot": pilot, "what": order}))
            runhost.submit(str(self.data), pilot, "mine mine", "mine.py", [pilot, "far:belt", "home:core:base"], {"FLEET_HOLD": "mine mine"})
        for pilot in ("miner-1", "miner-2"):                                 # miner-3's job is young: the host may still take it
            os.utime(self.home / "inbox" / (pilot + ".json"), (self.now - 90, self.now - 90))
        lines, children = self.real_pass()
        self.assertEqual(sorted(self.inbox()), ["miner-3"])
        self.assertEqual([argv[3:] for argv, _log, _env in self.spawned], [[str(self.root / "fleet" / "mine.py"), "miner-1", "far:belt", "home:core:base"]])
        self.assertEqual((len(children), self.spawned[0][2]["FLEET_HOLD"]), (1, "mine mine"))
        self.assertEqual(len([line for line in lines if "the host did not take it" in line]), 2)

    def test_a_dry_pass_hands_nothing_over_and_takes_nothing_back(self):
        self.idle("miner-1")
        self.hosting(kinds=["mine"])
        self.host()
        self.dispatch.runhost.submit(str(self.data), "miner-9", "mine mine", "mine.py", ["miner-9"], {})
        os.utime(self.home / "inbox" / "miner-9.json", (self.now - 90, self.now - 90))
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["miner-1 -> mine mine"])
        self.assertEqual((sorted(self.inbox()), self.spawned), (["miner-9"], []))


class RouteGateTests(Tree):
    def setUp(self):
        super().setUp()                                                                           # the gate's tree has a plan without the unknown route
        self.put_plan({role: [r for r in ids if r in ROUTES] + ["open"] for role, ids in PLAN["roles"].items()})

    def test_the_gate_passes_a_clean_tree_with_current_indexes(self):
        groups = ["index-once-per-pilot.md", "index-paying-routes.md", "index-tests.md", "index-fitting.md", "index-standing-work.md",
                  "index-measured-at-a-loss.md", "index-off.md"]
        names = ["master-index.md"] + groups + ["plan-%s.md" % role for role in sorted(PLAN["roles"])]
        self.assertEqual(self.routes.index_names(str(self.root)), names)                          # one index per group, one plan per role
        self.assertEqual([e.split(" is ")[0] for e in self.routes.check(str(self.root))[0][-len(names):]], ["game/routes/" + n for n in names])
        self.assertEqual(self.routes.write_index(str(self.root)), [(name, "written") for name in names])   # all written together
        self.assertEqual(self.routes.check(str(self.root)), ([], 6))
        first = {name: (self.root / "routes" / name).read_text(encoding="ascii") for name in names}
        self.assertEqual(self.routes.index_files(str(self.root)), first)                          # same input, same bytes, same ids
        self.assertEqual(len({text.split("\nid: ")[1].split("\n")[0] for text in first.values()}), len(names))
        self.assertEqual(self.routes.write_index(str(self.root)), [(name, "current") for name in names])
        for rid in ROUTES:                                                                        # every route once, in one group
            self.assertEqual(sum(first[g].count("| [%s](%s.json) |" % (rid, rid)) for g in groups), 1, rid)
        self.assertIn("| [drone](plan-drone.md) | Apophis | 5 | missions > whale > rays | 0 |", first["master-index.md"])
        self.assertIn("| [Tests](index-tests.md) |", first["master-index.md"])                    # a group's name leads into its sub-index
        self.assertIn("# index-tests.md -- Tests\n", first["index-tests.md"])
        self.assertIn("\nKept by Apophis. Routes: 5. Ships: --.\n", first["plan-drone.md"])
        self.assertIn("| 1 | [missions](missions.json) |", first["plan-drone.md"])
        self.assertIn("| home space |", "".join(first[g] for g in groups))                        # the chart's empire column gives the zone
        self.assertIn("Routes: 0.", "".join(first[g] for g in groups))                            # an empty group keeps its file: the set never changes

    def test_a_file_written_no_longer_fails_the_gate_and_is_removed_by_index(self):
        self.routes.write_index(str(self.root))
        folder = self.root / "routes"
        made = "Written by `python3 -B game/fleet/routes.py index`, never by hand.\n"
        (folder / "index.md").write_text("# index.md\n\n" + made, encoding="ascii")              # the two files the sub-indexes replaced
        (folder / "plan.md").write_text("# plan.md\n\n" + made, encoding="ascii")
        (folder / "plan-ghost.md").write_text("# plan-ghost.md\n\n" + made, encoding="ascii")    # the plan of a role that is gone
        (folder / "plan-notes.md").write_text("# my own notes\n", encoding="ascii")               # another hand's file is never touched
        self.assertEqual(self.routes.stale(str(self.root)), ["index.md", "plan-ghost.md", "plan.md"])
        errors = self.routes.check(str(self.root))[0]
        self.assertEqual([e.split(" is ")[0] for e in errors], ["game/routes/index.md", "game/routes/plan-ghost.md", "game/routes/plan.md"])
        self.assertEqual([pair for pair in self.routes.write_index(str(self.root)) if pair[1] != "current"],
                         [("index.md", "removed"), ("plan-ghost.md", "removed"), ("plan.md", "removed")])
        self.assertEqual(self.routes.check(str(self.root)), ([], 6))
        self.assertTrue((folder / "plan-notes.md").is_file())

    def test_each_rule_fails_alone(self):
        def errors_with(rid, change):
            route = dict(ROUTES[rid]); route.update(change)
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route), encoding="ascii")
            found = [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e]
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(ROUTES[rid]), encoding="ascii")
            return found
        self.assertIn("`id` must equal the file name", errors_with("mine", {"id": "other"})[0])
        self.assertIn("`kind` must be one of", errors_with("mine", {"kind": "trade"})[0])
        self.assertIn("`belt` is missing", errors_with("mine", {"belt": ""})[0])
        self.assertIn("system `nowhere` is not on the chart", errors_with("rays", {"place": "nowhere:nebula"})[0])
        self.assertIn("`sell_at` must have 3 parts", errors_with("rays", {"sell_at": "home:core"})[0])
        self.assertIn("stop 1: `at` must be system:poi:base", errors_with("missions", {"stops": [{"at": "home"}]})[0])
        self.put_plan({"drone": ["ghost", "open"]})
        self.assertIn("game/routes/plans/drone.json: names `ghost`, which is no route file", [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e][0])
        for last, why in (("mine", "without max_ships"), ("rays", "without max_ships"), ("missions", "without once, min_credits")):
            self.put_plan({"drone": ["open", last]})
            found = [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e]
            self.assertEqual(len(found), 1, last)
            self.assertIn("plans/drone.json: must end with a route that is always open (the `park` route, or a mine, %s); `%s` is not" % (why, last), found[0])
        park = {"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [{"at": "home:core:base"}]}
        (self.root / "routes" / "park.json").write_text(json.dumps(park), encoding="ascii")
        self.put_plan({"drone": ["open", "park"]})
        self.assertEqual([e for e in self.routes.check(str(self.root))[0] if "index.md" not in e], [])    # the park route may end a list
        self.put_plan({"drone": ["open", "park"]}, owner="Zero")
        self.assertIn("`owner` must be Apophis, who commands the drone ships", [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e][0])
        self.put_plan({"drone": []})
        self.assertIn("`routes` is empty", [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e][0])
        (self.root / "routes" / "park.json").unlink()
        (self.root / "routes" / "plan.json").write_text("{}", encoding="ascii")
        self.put_plan({"drone": ["open"]})
        self.assertIn("the one plan file is gone", [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e][0])
        (self.root / "routes" / "plan.json").unlink()

    def test_a_craft_entry_names_its_recipe_its_runs_and_what_it_makes_where_the_stop_sells(self):
        # requests ENT-013: route_run.py's craft step queues `runs` of `recipe` and sells again what it made (`makes`)
        def errors_with(stop):
            route = dict(ROUTES["missions"], stops=[dict({"at": "home:core:base"}, **stop)])
            (self.root / "routes" / "missions.json").write_text(json.dumps(route), encoding="ascii")
            found = [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e]
            (self.root / "routes" / "missions.json").write_text(json.dumps(ROUTES["missions"]), encoding="ascii")
            return found
        good = {"recipe": "assemble_control_node", "runs": 8, "makes": "control_node", "per_run": 2, "inputs": ["silver_wiring"]}
        sells = {"sell": [{"item": "control_node", "min_price": 760}]}
        self.assertEqual(errors_with(dict(sells, craft=[good])), [])
        self.assertEqual(errors_with({"craft": [good]}), [])                                                 # a craft at a stop that sells nothing
        self.assertIn("needs `makes`", errors_with({"craft": [{"recipe": "assemble_control_node", "runs": 1}]})[0])     # the runner refuses an entry without it
        for wrong in ({"runs": 8}, {"recipe": "", "runs": 8}, {"recipe": 7, "runs": 8}, "assemble_control_node"):
            found = errors_with({"craft": [wrong]})
            self.assertEqual(len(found), 1, found)
            self.assertIn("game/routes/missions.json: stop 1: a `craft` entry needs `recipe`, a recipe id", found[0])
        for runs in (0, -1, "8", 2.5, True, None):
            found = errors_with({"craft": [dict(good, runs=runs)]})
            self.assertEqual(len(found), 1, (runs, found))
            self.assertIn("stop 1: the `craft` of assemble_control_node needs `runs`, a whole number of 1 or more", found[0])
        for makes in (None, ""):
            found = errors_with(dict(sells, craft=[dict(good, makes=makes)]))
            self.assertEqual(len(found), 1, found)
            self.assertIn("stop 1: the `craft` of assemble_control_node needs `makes`: the runner counts", found[0])

    def test_a_route_file_or_a_role_plan_that_names_a_pilot_of_ours_fails_the_gate(self):
        # requests ENT-052: the repository never says which pilot flies what
        names = lambda: [e for e in self.routes.check(str(self.root))[0] if "names a pilot of ours" in e]
        self.assertEqual(names(), [])
        path = self.root / "routes" / "missions.json"
        path.write_text(json.dumps(dict(ROUTES["missions"], notes="flown by miner-12 at 23:10, then by miner-12 and scout-3")), encoding="ascii")
        self.assertEqual(names(), ["game/routes/missions.json: names a pilot of ours (miner-12, scout-3): write the role and a count; which ship stays in the data folder"])
        path.write_text(json.dumps(ROUTES["missions"]), encoding="ascii")
        plan = self.root / "routes" / "plans" / "drone.json"
        before = plan.read_text(encoding="ascii")
        plan.write_text(json.dumps(dict(json.loads(before), planned=[{"what": "drone-3 tests the herd", "when": "next turn"}])), encoding="ascii")
        self.assertEqual(len(names()), 1)
        self.assertIn("game/routes/plans/drone.json: names a pilot of ours (drone-3)", names()[0])
        plan.write_text(before, encoding="ascii")
        self.assertEqual(names(), [])
        self.assertEqual(self.routes.division.pilots_named("the miner- ships, sentinel-<n>, Prime Directive, hunter-7, 30 drones, scout-"), [])

    def test_measure_writes_only_the_routes_it_is_given(self):
        rows = [{"route": rid, "pilot": "p", "minutes": 30, "delta": 600, "credits_before": 5000, "credits_after": 5600, "started": self.started(2)} for rid in ("mine", "rays")]
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.routes.measure(str(self.root), str(self.data), True, {"mine"})
        self.assertIn("measured", json.loads((self.root / "routes" / "mine.json").read_text()))
        self.assertNotIn("measured", json.loads((self.root / "routes" / "rays.json").read_text()))  # another division's file is left alone

    def test_measure_writes_a_figure_once_and_again_only_on_a_real_move(self):
        rows = [{"route": "mine", "pilot": "miner-1", "minutes": 30, "delta": -40, "credits_before": 9000, "credits_after": 8960, "started": self.started(3)},
                {"route": "mine", "pilot": "miner-2", "minutes": 60, "delta": -50, "credits_before": 9000, "credits_after": 8950, "started": self.started(3)}]
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.routes.measure(str(self.root), str(self.data), True)
        figure = json.loads((self.root / "routes" / "mine.json").read_text())["measured"]
        self.assertEqual((figure["runs"], figure["minutes"], figure["credits_per_run"], figure["cph_per_ship"]), (2, 45, -40, -60))
        stamp = (self.root / "routes" / "mine.json").stat().st_mtime_ns
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            handle.write(json.dumps({"route": "mine", "pilot": "miner-3", "minutes": 45, "delta": -45, "credits_before": 9000, "credits_after": 8955, "started": self.started(2)}) + "\n")
        self.routes.measure(str(self.root), str(self.data), True)
        self.assertEqual((self.root / "routes" / "mine.json").stat().st_mtime_ns, stamp)          # 3 runs, the same rate: untouched

    def test_a_top_up_between_our_own_ships_is_nobodys_earning(self):
        # 2026-11-16: the wallet guard gave the ships born that day about 19,000 cr each out of ships on standing work; their routes read -2,000 cr a ship-hour
        fleet = self.data / "fleet"
        fleet.mkdir(parents=True, exist_ok=True)
        os.environ["FLEET_TAXES"] = str(fleet / "taxes.json")                                  # the gifts lie beside the tax record
        self.addCleanup(os.environ.__setitem__, "FLEET_TAXES", os.devnull)
        now = int(time.time())
        text = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
        (fleet / "gifts.jsonl").write_text(json.dumps({"at": now - 1800, "from": "miner-1", "to": "miner-9", "credits": 19000}) + "\n"
                                           + json.dumps({"at": now - 1700, "from": "miner-1", "to": "miner-8", "credits": 0, "unsure": 19000}) + "\n" + "not json\n")
        giver = {"route": "mine", "kind": "mine", "pilot": "miner-1", "minutes": 45, "delta": -19120, "credits_before": 90000, "credits_after": 70880, "started": text(now - 3000)}
        taker = dict(giver, pilot="miner-9", delta=18880, credits_before=900, credits_after=19780)
        earlier = dict(giver, started=text(now - 4 * 3600), delta=-120)                         # a run that ended before the gift
        other = dict(giver, pilot="miner-2", delta=-120)
        self.assertEqual([self.routes.moved(r) for r in (giver, taker, earlier, other)], [19000, -19000, 0, 0])
        self.assertEqual([self.routes.earned(r) for r in (giver, taker, earlier, other)], [-120, -120, -120, -120])
        self.assertEqual(self.routes.moved({"route": "mine", "pilot": "miner-1"}), 0)           # a row without a start
        # one gift, one run: the spans of two runs in a row overlap, and the run after the giver's read +19,000 cr nobody made
        seam = now - 300                                                                        # the giver's run ends here, the next begins
        (fleet / "gifts.jsonl").write_text(json.dumps({"at": seam - 60, "from": "miner-1", "to": "miner-9", "credits": 19000}) + "\n")
        first = dict(giver, started=text(seam - 2700), delta=-19120)                            # the gift fell in its last minute: its wallet shows it
        second = dict(giver, started=text(seam), minutes=4, delta=-11)                          # begins a minute after the gift: its wallet does not
        self.assertEqual([self.routes.earned(r) for r in (first, second)], [-120, -11])
        late = dict(first, delta=-120)                                                          # the first run's last reading came before the gift ...
        shown = dict(second, delta=-19011)                                                      # ... and the second run's wallet shows it
        self.assertEqual([self.routes.earned(r) for r in (late, shown)], [-120, -11])
        (fleet / "gifts.jsonl").write_text(json.dumps({"at": seam - 1300, "from": "miner-1", "to": "miner-9", "credits": 19000}) + "\n")
        sale = dict(first, delta=11000)                                                         # well inside a run that also sold for 30,000 cr: it counts whatever the wallet reads
        self.assertEqual(self.routes.earned(sale), 30000)
        (fleet / "gifts.jsonl").write_text(json.dumps({"at": seam - 1300, "from": "miner-1", "to": "miner-9", "credits": 19000, "loose": True}) + "\n")
        self.assertEqual([self.routes.earned(r) for r in (first, dict(first, delta=-120))], [-120, -120])     # a row whose time is its pass's: by the wallet alone

    def test_a_treasury_deposit_and_a_gift_that_lands_late_are_nobodys_earning(self):
        # requests ENT-231: a run read -200,720 cr where its wallet moved -720 (200,000 in as gifts, 200,000 out to the treasury)
        # requests ENT-220: ten gifts booked 3 to 9 minutes before a craft run landed in it and read as 117,329 cr earned
        fleet = self.data / "fleet"
        fleet.mkdir(parents=True, exist_ok=True)
        os.environ["FLEET_TAXES"] = str(fleet / "taxes.json")
        self.addCleanup(os.environ.__setitem__, "FLEET_TAXES", os.devnull)
        now = int(time.time())
        text = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
        start = now - 3000
        (fleet / "gifts.jsonl").write_text("".join(json.dumps({"at": start + 600 + n, "from": "miner-%d" % n, "to": "Prime Directive", "credits": 50000}) + "\n" for n in range(4)))
        (fleet / "onetime.json").write_text(json.dumps([[start + 900, "Prime Directive", "Faction treasury: credits deposited (the Collective keeps them)", -200000],
                                                        [start + 900, "Prime Directive", "Some Reward", 4000]]))
        deposit = {"route": "mine", "kind": "mine", "pilot": "Prime Directive", "minutes": 45, "delta": -720, "credits_before": 17838, "credits_after": 17118, "started": text(start)}
        self.assertEqual(self.routes.moved(deposit), 0)                                          # 200,000 in, 200,000 out: the run's own -720 stays
        self.assertEqual(self.routes.earned(deposit), -720)
        self.assertEqual(self.routes.moved(dict(deposit, pilot="miner-1", delta=-50120)), 50000)  # the giver's side as before
        # gifts booked before the span that landed in the run
        (fleet / "onetime.json").write_text("[]")
        (fleet / "gifts.jsonl").write_text("".join(json.dumps({"at": start - 1200 + 60 * n, "from": "miner-%d" % n, "to": "hauler-3", "credits": 40000}) + "\n" for n in range(3)))
        late = {"route": "craft", "kind": "circuit", "pilot": "hauler-3", "minutes": 15, "delta": 79880, "credits_before": 45000, "credits_after": 124880, "started": text(start)}
        (self.data / "routes" / "runs.jsonl").write_text(json.dumps({"route": "gather", "kind": "mine", "pilot": "hauler-3", "minutes": 30, "delta": -100,
                                                                     "credits_before": 5100, "credits_after": 5000, "started": text(start - 3600)}) + "\n")
        self.assertEqual(self.routes.earned(late), -120)                                         # one landed before (5,000 -> 45,000), two in the run
        sale = dict(late, delta=30000, credits_before=125000, credits_after=155000)            # all three landed before the run: its own sale stays
        self.assertEqual(self.routes.earned(sale), 30000)
        (self.data / "routes" / "runs.jsonl").write_text(json.dumps({"route": "gather", "kind": "mine", "pilot": "hauler-3", "minutes": 25, "delta": -100,
                                                                     "credits_before": 5100, "credits_after": 5000, "started": text(start - 1500)}) + "\n")
        self.assertEqual(self.routes.earned(late), 79880)                                       # the previous run spans the gifts: they are its

    def test_a_guard_may_follow_the_pilot_of_a_circuit(self):
        # requests ENT-217 and ENT-226: the escort; guard.py --follow is Military's half, the dispatcher's is this
        routes = self.dispatch.load_routes(self.root)
        kit = {"id": "kit", "kind": "circuit", "title": "t", "stops": [{"at": "home:core:base"}, {"at": "far:belt"}]}
        (self.root / "routes" / "kit.json").write_text(json.dumps(kit), encoding="ascii")
        guard = {"id": "escort", "kind": "guard", "title": "t", "guards": "kit", "station": "home:core:base"}
        (self.root / "routes" / "escort.json").write_text(json.dumps(guard), encoding="ascii")
        pilot = {"name": "drone-1", "credits": 20000, "modules": [], "docked": True}
        state = dict(self.state(orders={}), root=str(self.root))
        self.assertEqual(self.dispatch.why_not(pilot, "escort", guard, state), ("nobody flies kit", None))
        (self.data / "fleet" / "ships").mkdir(parents=True, exist_ok=True)
        (self.data / "fleet" / "ships" / "hauler-3.json").write_text(json.dumps({"name": "hauler-3", "system": "far", "poi": "belt"}))
        state = dict(self.state(orders={"hauler-3": "circuit kit"}), root=str(self.root))
        reason, argument = self.dispatch.why_not(pilot, "escort", guard, state)
        self.assertEqual((reason, argument), (None, {"place": "far:belt", "follow": "hauler-3"}))
        argv = self.dispatch.command(guard, "drone-1", argument, str(self.root))
        self.assertEqual(argv[4:8], ["drone-1", "far", "belt", "--guards"])
        self.assertEqual(argv[argv.index("--follow") + 1], "hauler-3")
        self.assertNotIn("--follow", self.dispatch.command(dict(guard, guards="mine"), "drone-1", "far:belt", str(self.root)))
        self.assertNotIn("escort", " ".join(self.routes.check(str(self.root))[0]))               # the gate takes a guard of a circuit

    def test_a_hunt_is_not_credited_with_goods_it_carried_in(self):
        rows = [{"route": "rays", "kind": "hunt", "pilot": "drone-1", "minutes": 30, "delta": 1140, "goods": {"carapace": 3}, "sold": {"curd": [4, 330, 1320]},
                 "credits_before": 20000, "credits_after": 21140, "started": self.started(2)},
                {"route": "rays", "kind": "hunt", "pilot": "drone-2", "minutes": 30, "delta": 3000, "goods": {"curd": 9}, "sold": {"curd": [10, 330, 3300]},
                 "credits_before": 20000, "credits_after": 23000, "started": self.started(1)}]
        self.assertEqual([round(self.routes.earned(r)) for r in rows], [-180, 2670])            # all four carried in; one of ten
        self.assertEqual(self.routes.earned({"route": "missions", "kind": "circuit", "delta": 500, "sold": {"curd": [4, 330, 1320]}}), 500)
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.routes.measure(str(self.root), str(self.data), True)
        figure = json.loads((self.root / "routes" / "rays.json").read_text())["measured"]
        self.assertEqual((figure["runs"], figure["credits_per_run"], figure["cph_per_ship"]), (2, 1240, 2490))

    def test_a_run_that_read_no_wallet_gives_no_figure_and_takes_a_false_one_out(self):
        blind = [{"route": "mine", "kind": "mine", "pilot": "miner-1", "minutes": 45, "delta": 0, "credits_before": 0, "credits_after": 0, "started": self.started(3)},
                 {"route": "mine", "kind": "census", "pilot": "scout-1", "minutes": 7, "delta": 0, "started": self.started(3)},
                 {"route": "mine", "kind": "mine", "pilot": "miner-2", "minutes": 45, "delta": 0, "credits_before": None, "credits_after": 9000, "notes": ["wallet not read"],
                  "started": self.started(2)}]
        self.assertEqual([self.routes.readable(r) for r in blind], [False, False, False])
        path = self.root / "routes" / "mine.json"
        route = dict(ROUTES["mine"]); route["measured"] = {"date": "2026-01-01", "runs": 3, "minutes": 45, "credits_per_run": 0, "cph_per_ship": 0}
        path.write_text(json.dumps(route), encoding="ascii")
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in blind))
        self.routes.measure(str(self.root), str(self.data), False)
        self.assertIn("measured", json.loads(path.read_text()))                                 # a rehearsal changes nothing
        self.routes.measure(str(self.root), str(self.data), True)
        self.assertNotIn("measured", json.loads(path.read_text()))                              # "0 credits" was never measured
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            handle.write(json.dumps({"route": "mine", "kind": "mine", "pilot": "miner-3", "minutes": 60, "delta": -190, "credits_before": 9000, "credits_after": 8810,
                                     "started": self.started(2)}) + "\n")
        self.routes.measure(str(self.root), str(self.data), True)
        figure = json.loads(path.read_text())["measured"]
        self.assertEqual((figure["runs"], figure["credits_per_run"], figure["cph_per_ship"]), (1, -190, -190))   # the one run that read

    def measured(self, rid):
        return json.loads((self.root / "routes" / (rid + ".json")).read_text()).get("measured")

    def runs(self, *rows):
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))

    def a_run(self, rid, hours_ago, delta, minutes=30, **more):
        return dict({"route": rid, "pilot": "p", "minutes": minutes, "delta": delta, "credits_before": 9000, "credits_after": 9000 + delta,
                     "started": self.started(hours_ago)}, **more)

    def test_a_figure_rests_on_the_runs_that_ended_in_the_last_twelve_hours(self):
        # Suggi, 2026-11-16: the game changes by the hour; a route that lost yesterday can pay today
        self.assertEqual(self.routes.MEASURE_HOURS, 12)
        self.runs(self.a_run("rays", 30, -900), self.a_run("rays", 12.6, -900), self.a_run("rays", 12.2, 600), self.a_run("rays", 3, 600))
        self.routes.measure(str(self.root), str(self.data), True, now=self.now)                  # 12.2 hours ago + 30 minutes ended inside the window
        figure = self.measured("rays")
        self.assertEqual((figure["runs"], figure["credits_per_run"], figure["cph_per_ship"], figure["hours"]), (2, 600, 1200, 12))
        self.assertEqual(figure["last_run"], self.started(3 - 0.5))                              # the end of the newest run counted
        self.assertEqual(self.routes.stage(json.loads((self.root / "routes" / "rays.json").read_text())), "paying")
        self.assertEqual(self.routes.ended({"started": self.started(1), "minutes": 30}), self.dispatch.read_time(self.started(1)) + 1800)    # the dispatcher's reading
        self.assertIsNone(self.routes.ended({"minutes": 30}))

    def test_a_route_without_a_readable_run_in_the_window_loses_its_figure_and_is_a_test_again(self):
        good = {"date": "2026-11-15", "runs": 9, "minutes": 30, "credits_per_run": 2000, "cph_per_ship": 4000, "hours": 12, "last_run": "2026-11-15T10:00:00Z"}
        for rid in ("rays", "whale"):                                                             # one with old runs, one with no run on record at all
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(dict(ROUTES[rid], measured=good)), encoding="ascii")
        self.runs(self.a_run("rays", 13, 3000), self.a_run("rays", 2, 0, credits_before=0, credits_after=0))     # old, and one that read no wallet
        import contextlib, io
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.routes.measure(str(self.root), str(self.data), False, now=self.now)             # a rehearsal changes nothing
        self.assertEqual((self.measured("rays"), self.measured("whale")), (good, good))
        self.assertIn("rays: no readable run in 12 hours: `--write` takes the figure out; a test again", said.getvalue())
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.routes.measure(str(self.root), str(self.data), True, now=self.now)
        self.assertEqual((self.measured("rays"), self.measured("whale")), (None, None))           # a figure, good or bad, is never kept past its window
        for rid in ("rays", "whale"):
            self.assertIn("%s: no readable run in 12 hours: the figure is taken out; a test again\n" % rid, said.getvalue())
            self.assertEqual(self.routes.stage(json.loads((self.root / "routes" / (rid + ".json")).read_text())), "test")
        self.assertIn("measured block written: rays, whale", said.getvalue())

    def test_a_mission_that_pays_once_keeps_all_its_runs(self):
        self.runs(self.a_run("missions", 40, 4000), self.a_run("missions", 20, 2000))
        self.routes.measure(str(self.root), str(self.data), True, now=self.now)
        self.assertEqual(self.measured("missions"), {"date": time.strftime("%Y-%m-%d", time.gmtime(self.now)), "runs": 2, "minutes": 30, "credits_per_run": 3000,
                                                     "cph_per_ship": 6000})                       # today's block: no window
        (self.root / "routes" / "missions.json").write_text(json.dumps(dict(ROUTES["missions"], measured=self.measured("missions"))), encoding="ascii")
        self.runs()
        self.routes.measure(str(self.root), str(self.data), True, now=self.now)
        self.assertEqual(self.measured("missions")["runs"], 2)                                   # no run on record: a once figure is left alone

    def test_a_block_from_before_the_window_is_written_once_and_an_unchanged_figure_never(self):
        old = {"date": "2026-11-15", "runs": 2, "minutes": 30, "credits_per_run": 600, "cph_per_ship": 1200}
        path = self.root / "routes" / "mine.json"
        path.write_text(json.dumps(dict(ROUTES["mine"], measured=old)), encoding="ascii")
        self.runs(self.a_run("mine", 5, 600), self.a_run("mine", 4, 600))
        self.routes.measure(str(self.root), str(self.data), True, now=self.now)                  # the same figure, but no `hours`: written once
        figure = self.measured("mine")
        self.assertEqual((figure["cph_per_ship"], figure["hours"], figure["last_run"]), (1200, 12, self.started(4 - 0.5)))
        stamp = path.stat().st_mtime_ns
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            handle.write(json.dumps(self.a_run("mine", 1, 650)) + "\n")                              # a newer run, the same rate: a new last_run alone is no reason
        self.routes.measure(str(self.root), str(self.data), True, now=self.now)
        self.assertEqual((path.stat().st_mtime_ns, self.measured("mine")), (stamp, figure))

    def test_a_templates_file_is_gated_like_a_route_file(self):
        folder = self.root / "routes" / "templates"
        folder.mkdir()
        good = {"division": "military", "owner": "Apophis", "templates": {"herds": {"title": "The near herds", "routes": ["rays", "whale"], "trains": ["gunnery"]}}}
        faults = lambda: [e for e in self.routes.check(str(self.root))[0] if "templates" in e and "is missing or stale" not in e]
        (folder / "military.json").write_text(json.dumps(good), encoding="ascii")
        self.assertEqual(faults(), [])
        for change, says in (({"note": "flown by drone-4 and drone-12"}, "game/routes/templates/military.json: names a pilot of ours (drone-4, drone-12): a template is read by every member"),
                             ({"routes": ["rays", "ghost"]}, "game/routes/templates/military.json: the template `herds` names `ghost`, which is no route file"),
                             ({"routes": []}, "game/routes/templates/military.json: the template `herds` holds no route"),
                             ({"routes": ["@other"]}, "the template `herds` names `@other`: a template holds route ids, never another template"),
                             ({"title": 7}, "the template `herds`: `title` and `note` are ASCII texts and `trains` a list of skills")):
            spec = json.loads(json.dumps(good))
            spec["templates"]["herds"].update(change)
            (folder / "military.json").write_text(json.dumps(spec), encoding="ascii")
            self.assertEqual(len(faults()), 1, faults())
            self.assertIn(says, faults()[0])
        for spec, says in ((dict(good, owner="Zero"), "`owner` must be Apophis, who keeps the military division"),
                           (dict(good, division="mining"), "needs `division` equal to the file name"),
                           (dict(good, templates={"Herds": {"routes": ["rays"]}}), "`Herds` is no template name"),
                           (dict(good, templates={"drone-2-loop": {"routes": ["rays"]}}), "is no template name")):
            (folder / "military.json").write_text(json.dumps(spec), encoding="ascii")
            self.assertIn(says, " | ".join(faults()))
        (folder / "military.json").write_text(json.dumps(good), encoding="ascii")
        (folder / "pirates.json").write_text(json.dumps(dict(good, division="pirates")), encoding="ascii")
        self.assertEqual(faults(), ["game/routes/templates/pirates.json: `pirates` is no division of the fleet (command, intel, logistics, military, mining, trade)"])

    def test_the_plan_pages_carry_no_figure_and_each_division_s_templates_have_a_page(self):
        names = lambda: [name for name, _state in self.routes.write_index(str(self.root))]
        names()
        page = (self.root / "routes" / "plan-drone.md").read_text()
        self.assertNotIn("Credits per ship-hour", page)                                          # what a route earns changes by the hour: asked of the tools
        self.assertIn("\n| # | Route | Group | Zone | Open to | Ships planned |\n|---|---|---|---|---|---|\n", page)
        self.assertIn("What a route earns now is not written here, because it changes by the\nhour: ask the tool `route` or `routes`, or the database (`hive.py sql`)", page)
        self.assertNotIn("Templates", page)
        self.assertNotIn("Templates by Division", (self.root / "routes" / "master-index.md").read_text())
        (self.root / "routes" / "templates").mkdir()
        spec = {"division": "military", "owner": "Apophis", "templates": {"herds": {"title": "The near herds", "routes": ["rays", "whale"], "trains": ["gunnery"], "note": "n"},
                                                                          "idle": {"routes": ["mine"]}}}
        (self.root / "routes" / "templates" / "military.json").write_text(json.dumps(spec), encoding="ascii")
        plan = self.root / "routes" / "plans" / "drone.json"
        plan.write_text(json.dumps(dict(json.loads(plan.read_text()), templates={"herds": 3})), encoding="ascii")    # as plan.py role_files writes it
        self.assertIn("templates-military.md", names())
        self.assertEqual(self.routes.check(str(self.root)), ([], 6))
        page = (self.root / "routes" / "templates-military.md").read_text()
        self.assertIn("Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/military.json`:", page)
        self.assertIn("\nKept by Apophis. Templates: 2. Ships on them: 3.\n", page)
        self.assertIn("| Template | Title | Trains | Routes, in this order | Ships on it | Note |\n", page)
        self.assertIn("| herds | The near herds | gunnery | [rays](rays.json) > [whale](whale.json) | 3 | n |\n| idle | -- | -- | [mine](mine.json) | 0 | -- |\n", page)
        self.assertIn("\n| Template | Ships of this role on it |\n|---|---|\n| [herds](templates-military.md) | 3 |\n", (self.root / "routes" / "plan-drone.md").read_text())
        master = (self.root / "routes" / "master-index.md").read_text()
        self.assertIn("## Templates by Division\n", master)
        self.assertIn("| Division | Kept by | Templates | Page |\n|---|---|---|---|\n| military | Apophis | herds, idle | [templates-military.md](templates-military.md) |\n", master)
        self.assertEqual(self.routes.write_index(str(self.root))[-1], ("templates-military.md", "current"))
        (self.root / "routes" / "templates" / "military.json").unlink()                         # the division gives up its templates: the page goes too
        self.assertIn("game/routes/templates-military.md is written no longer", " ".join(self.routes.check(str(self.root))[0]))
        self.assertIn(("templates-military.md", "removed"), self.routes.write_index(str(self.root)))
        self.assertFalse((self.root / "routes" / "templates-military.md").exists())
        self.assertNotIn("Templates by Division", (self.root / "routes" / "master-index.md").read_text())

    def test_the_mining_runner_reads_the_wallet_where_the_engine_puts_it(self):
        mine = load("mine")
        answer = {"username": "miner-7", "state": {"credits": 29785, "location": {}, "ship": {}}, "loop": {}}   # the shape the gate answered on 2026-11-15
        self.assertEqual(mine.credits_of(answer), 29785)
        self.assertIsNone(mine.credits_of({"state": {"player": {"credits": 29785}}}))           # the field the first version read: not there
        self.assertIsNone(mine.credits_of({}))
        self.assertEqual(mine.ore_of({"stats": {"ore_mined": 446}}), 446)
        self.assertIsNone(mine.ore_of({"stats": {}}))


if __name__ == "__main__":
    unittest.main()
