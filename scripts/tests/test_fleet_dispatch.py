"""The dispatcher's choice of a route and the route gate, on disposable trees; no engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest


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

    def state(self, rows=(), orders=None, rest=None, booked=None):
        return {"now": self.now, "data": str(self.data), "rows": list(rows), "orders": orders or {}, "rest": rest or {}, "booked": booked or {}}

    def pick(self, name, credits=20000, modules=(), docked=False, **state):
        route, argument = self.dispatch.pick({"name": name, "credits": credits, "modules": list(modules), "docked": docked}, PLAN,
                                             self.dispatch.load_routes(self.root), self.state(**state))
        return (route["id"] if route else None), argument


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


class RouteGateTests(Tree):
    def setUp(self):
        super().setUp()                                                                           # the gate's tree has a plan without the unknown route
        self.put_plan({role: [r for r in ids if r in ROUTES] + ["open"] for role, ids in PLAN["roles"].items()})

    def test_the_gate_passes_a_clean_tree_with_current_indexes(self):
        self.assertEqual([e.split(" is ")[0] for e in self.routes.check(str(self.root))[0][-3:]],
                         ["game/routes/index.md", "game/routes/plan.md", "game/routes/master-index.md"])    # the three are written together
        self.assertEqual(self.routes.write_index(str(self.root)), [("index.md", "written"), ("plan.md", "written"), ("master-index.md", "written")])
        self.assertEqual(self.routes.check(str(self.root)), ([], 6))
        first = {name: (self.root / "routes" / name).read_text(encoding="ascii") for name in ("index.md", "plan.md", "master-index.md")}
        self.assertEqual(self.routes.index_files(str(self.root)), first)                          # same input, same bytes, same ids
        self.assertEqual(len({text.split("\nid: ")[1].split("\n")[0] for text in first.values()}), 3)
        for rid in ROUTES:                                                                        # every route once, in one group
            self.assertEqual(first["index.md"].count("| [%s](%s.json) |" % (rid, rid)), 1, rid)
        self.assertIn("| [drone](plan.md#drone) | Apophis | 5 | missions > whale > rays | 0 |", first["master-index.md"])
        self.assertIn("](index.md#tests) |", first["master-index.md"])                            # a group's name leads into the sub-index
        self.assertIn("## Tests\n", first["index.md"])
        self.assertIn("## drone\n\nKept by Apophis. Routes: 5.", first["plan.md"])
        self.assertIn("| 1 | [missions](missions.json) |", first["plan.md"])
        self.assertIn("| home space |", first["index.md"])                                        # the chart's empire column gives the zone

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

    def test_measure_writes_only_the_routes_it_is_given(self):
        rows = [{"route": rid, "pilot": "p", "minutes": 30, "delta": 600, "credits_before": 5000, "credits_after": 5600, "started": "2026-11-15T10:00:00Z"} for rid in ("mine", "rays")]
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.routes.measure(str(self.root), str(self.data), True, {"mine"})
        self.assertIn("measured", json.loads((self.root / "routes" / "mine.json").read_text()))
        self.assertNotIn("measured", json.loads((self.root / "routes" / "rays.json").read_text()))  # another division's file is left alone

    def test_measure_writes_a_figure_once_and_again_only_on_a_real_move(self):
        rows = [{"route": "mine", "pilot": "miner-1", "minutes": 30, "delta": -40, "credits_before": 9000, "credits_after": 8960},
                {"route": "mine", "pilot": "miner-2", "minutes": 60, "delta": -50, "credits_before": 9000, "credits_after": 8950}]
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.routes.measure(str(self.root), str(self.data), True)
        figure = json.loads((self.root / "routes" / "mine.json").read_text())["measured"]
        self.assertEqual((figure["runs"], figure["minutes"], figure["credits_per_run"], figure["cph_per_ship"]), (2, 45, -40, -60))
        stamp = (self.root / "routes" / "mine.json").stat().st_mtime_ns
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            handle.write(json.dumps({"route": "mine", "pilot": "miner-3", "minutes": 45, "delta": -45, "credits_before": 9000, "credits_after": 8955}) + "\n")
        self.routes.measure(str(self.root), str(self.data), True)
        self.assertEqual((self.root / "routes" / "mine.json").stat().st_mtime_ns, stamp)          # 3 runs, the same rate: untouched

    def test_a_hunt_is_not_credited_with_goods_it_carried_in(self):
        rows = [{"route": "rays", "kind": "hunt", "pilot": "drone-1", "minutes": 30, "delta": 1140, "goods": {"carapace": 3}, "sold": {"curd": [4, 330, 1320]},
                 "credits_before": 20000, "credits_after": 21140},
                {"route": "rays", "kind": "hunt", "pilot": "drone-2", "minutes": 30, "delta": 3000, "goods": {"curd": 9}, "sold": {"curd": [10, 330, 3300]},
                 "credits_before": 20000, "credits_after": 23000}]
        self.assertEqual([round(self.routes.earned(r)) for r in rows], [-180, 2670])            # all four carried in; one of ten
        self.assertEqual(self.routes.earned({"route": "missions", "kind": "circuit", "delta": 500, "sold": {"curd": [4, 330, 1320]}}), 500)
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.routes.measure(str(self.root), str(self.data), True)
        figure = json.loads((self.root / "routes" / "rays.json").read_text())["measured"]
        self.assertEqual((figure["runs"], figure["credits_per_run"], figure["cph_per_ship"]), (2, 1240, 2490))

    def test_a_run_that_read_no_wallet_gives_no_figure_and_takes_a_false_one_out(self):
        blind = [{"route": "mine", "kind": "mine", "pilot": "miner-1", "minutes": 45, "delta": 0, "credits_before": 0, "credits_after": 0},
                 {"route": "mine", "kind": "census", "pilot": "scout-1", "minutes": 7, "delta": 0},
                 {"route": "mine", "kind": "mine", "pilot": "miner-2", "minutes": 45, "delta": 0, "credits_before": None, "credits_after": 9000, "notes": ["wallet not read"]}]
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
            handle.write(json.dumps({"route": "mine", "kind": "mine", "pilot": "miner-3", "minutes": 60, "delta": -190, "credits_before": 9000, "credits_after": 8810}) + "\n")
        self.routes.measure(str(self.root), str(self.data), True)
        figure = json.loads(path.read_text())["measured"]
        self.assertEqual((figure["runs"], figure["credits_per_run"], figure["cph_per_ship"]), (1, -190, -190))   # the one run that read

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
