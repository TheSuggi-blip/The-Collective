"""game/fleet/guard.py against a made-up gate, and the guard kind in the dispatcher and the route gate. No engine, no
network, no waiting: every folder is a temporary one and the runner's clock moves only when it sleeps."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
FIRING = {"attack", "fire", "engage", "hunt", "advance", "target", "shoot", "use_weapon"}     # battle commands a guard never sends


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Clock:
    """The runner's clock and sleep: a sleep moves the clock, nothing waits."""

    def __init__(self):
        self.now = time.time()

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class Gate:
    """Answers the runner's calls the way census.py and hunt.py read the engine, and keeps every call it was sent.
    `on_look(n)` runs before the n-th answer of get_nearby; `reach` False refuses the goal go-to-poi."""

    def __init__(self, on_look=None, reach=True, credits=9000, nearby=None):
        self.calls, self.looks, self.fighting = [], 0, False
        self.on_look, self.reach, self.credits = on_look, reach, credits
        self.nearby = nearby if nearby is not None else [{"username": "miner-1", "faction_tag": "COL"}, {"username": "Raider", "faction_tag": "PIR"}]

    def __call__(self, method, path, body=None, timeout=120):
        self.calls.append((method, path, body))
        if path.endswith("/goal"):
            if body["type"] == "go-to-poi" and not self.reach:
                return 400, {"error": "no way to the poi"}
            return 200, {"success": True, "message": "done"}
        if path.endswith("/combat-mode"):
            return 200, {"mode": body["mode"]}
        if path.endswith("/raw"):
            action = body["action"]
            if body["toolGroup"] == "spacemolt_battle" and action == "status":
                return 200, {"structuredContent": {"is_participant": self.fighting}}
            if body["toolGroup"] == "spacemolt_battle" and action == "stance":
                self.fighting = False                        # the stance flee takes the ship out
                return 200, {"structuredContent": {"stance": body["params"].get("stance")}}
            if action == "get_nearby":
                self.looks += 1
                if self.on_look:
                    self.on_look(self.looks)
                return 200, {"structuredContent": {"poi_id": "belt", "nearby": self.nearby, "pirate_count": 0}}
            return 200, {"structuredContent": {}}
        if method == "GET":
            return 200, {"state": {"credits": self.credits}}
        return 404, {}

    def raws(self):
        return [(body["toolGroup"], body["action"], body.get("params") or {}) for _m, path, body in self.calls if path.endswith("/raw")]

    def goals(self):
        return [(body["type"], body["options"]) for _m, path, body in self.calls if path.endswith("/goal")]


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-guard-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("fleet/orders", "fleet/ships", "routes"):
            (self.data / folder).mkdir(parents=True)
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": "sentinel-1"}, {"name": "miner-1"}]}))
        self.ship(100, 100)
        self.guarded(True)
        self.guard = load("guard")
        self.clock = Clock()

    def ship(self, hull, top):
        (self.data / "fleet" / "ships" / "sentinel-1.json").write_text(json.dumps({"name": "sentinel-1", "hull": hull, "max_hull": top}))

    def guarded(self, flying):
        """The order file of the pilot on the guarded route: there while it works, gone when its run ended."""
        path = self.data / "fleet" / "orders" / "miner-1.json"
        if flying:
            path.write_text(json.dumps({"pilot": "miner-1", "what": "mine belt-x", "since": "2026-11-16T10:00:00Z"}))
        elif path.exists():
            path.unlink()

    def run_guard(self, gate, minutes=60, extra=()):
        opts = self.guard.parse(["sentinel-1", "far", "belt", "--guards", "belt-x", "--station", "home:core:base", "--minutes", str(minutes),
                                 "--route", "guard-x"] + list(extra))
        with contextlib.redirect_stdout(io.StringIO()) as said:
            row = self.guard.run(opts, gate, str(self.data), sleep=self.clock.sleep, clock=self.clock)
        self.said = said.getvalue()
        return row

    def rows(self):
        return [json.loads(line) for line in (self.data / "routes" / "runs.jsonl").read_text().splitlines()]

    def assert_docked(self, gate):
        self.assertEqual(gate.goals()[-1], ("prepare-at-station", {"systemId": "home", "poiId": "core", "baseId": "base", "refuel": True}))

    def test_it_leaves_two_looks_after_the_guarded_order_is_gone_and_docks(self):
        orders = []

        def look(n):
            orders.append(json.loads((self.data / "fleet" / "orders" / "sentinel-1.json").read_text())["what"])
            if n == 3:
                self.guarded(False)                          # the guarded ship's run ended before the third look
        gate = Gate(on_look=look)
        row = self.run_guard(gate)
        self.assertEqual(gate.looks, 4)                      # looks 3 and 4 saw nobody on the guarded route
        self.assertEqual(set(orders), {"guard guard-x"})
        self.assertFalse((self.data / "fleet" / "orders" / "sentinel-1.json").exists())    # the order file goes when the run ends
        self.assert_docked(gate)
        self.assertEqual(self.rows(), [row])
        self.assertEqual((row["route"], row["kind"], row["pilot"], row["guards"], row["place"], row["left"], row["looks"], row["docked"]),
                         ("guard-x", "guard", "sentinel-1", "belt-x", "far:belt", "guarded ship gone", 4, True))
        self.assertEqual(row["notes"], ["guarded 3 min, 4 looks, 1 strangers, left: guarded ship gone"])
        self.assertEqual(row["strangers"], {"Raider": "PIR"})
        self.assertEqual((row["credits_before"], row["credits_after"], row["delta"], row["one_time"]), (9000, 9000, 0, 0))
        self.assertIn("ours miner-1 | strangers Raider [PIR] | pirates 0 | hull 100% | on belt-x: miner-1", self.said)
        self.assertIn("RESULT sentinel-1: guard guard-x at far:belt for belt-x:", self.said)
        self.assertEqual([b["mode"] for m, p, b in gate.calls if p.endswith("/combat-mode")], ["flee"])     # the engine's own answer to a fight

    def test_one_look_without_the_guarded_order_is_not_enough(self):
        # a pilot between two runs of the guarded route carries no order file for up to one dispatcher pass
        def look(n):
            self.guarded(n != 2)
        gate = Gate(on_look=look)
        row = self.run_guard(gate, minutes=4)
        self.assertEqual((row["left"], row["looks"]), ("4 minutes passed", 5))

    def test_it_leaves_when_its_hull_is_under_60_percent(self):
        def look(n):
            if n == 2:
                self.ship(59, 100)
        gate = Gate(on_look=look)
        row = self.run_guard(gate)
        self.assertEqual((row["left"], row["looks"], row["lowest_hull_pct"]), ("hull 59%", 2, 59))
        self.assert_docked(gate)
        self.ship(60, 100)                                   # 60 percent is not under 60: it stays
        self.assertEqual(self.run_guard(Gate(), minutes=1)["left"], "1 minutes passed")

    def test_in_a_fight_it_flees_and_leaves_and_never_fires(self):
        gate = Gate()

        def look(n):
            if n == 2:
                gate.fighting = True                         # a ship attacked it after its second look
        gate.on_look = look
        row = self.run_guard(gate)
        self.assertEqual((row["left"], row["looks"]), ("in a fight", 2))
        battle = [(action, params) for group, action, params in gate.raws() if group == "spacemolt_battle"]
        self.assertIn(("stance", {"stance": "flee"}), battle)
        self.assertEqual({action for action, _p in battle}, {"status", "stance"})
        self.assertEqual({params.get("stance") for action, params in battle if action == "stance"}, {"flee"})
        self.assertFalse({action for _g, action, _p in gate.raws()} & FIRING)
        self.assertEqual([b["mode"] for m, p, b in gate.calls if p.endswith("/combat-mode")], ["flee"])
        self.assertEqual({kind for kind, _o in gate.goals()}, {"navigate-to-system", "go-to-poi", "prepare-at-station"})
        self.assert_docked(gate)
        self.assertLess(gate.calls.index(next(c for c in gate.calls if c[2] and c[2].get("action") == "stance")),
                        gate.calls.index(next(c for c in gate.calls if c[2] and c[2].get("type") == "prepare-at-station")))   # out before it flies on

    def test_it_leaves_after_its_minutes(self):
        gate = Gate()
        row = self.run_guard(gate, minutes=3)
        self.assertEqual((row["left"], row["looks"], row["stay_minutes"]), ("3 minutes passed", 4, 3.0))
        self.assertEqual(row["notes"], ["guarded 3 min, 4 looks, 1 strangers, left: 3 minutes passed"])
        self.assert_docked(gate)

    def test_the_stop_file_ends_the_watch(self):
        def look(n):
            if n == 2:
                (self.data / "fleet" / "STOP").write_text("")
        row = self.run_guard(Gate(on_look=look))
        self.assertEqual((row["left"], row["looks"], row["docked"]), ("STOP file", 2, True))

    def test_a_place_not_reached_still_writes_its_row_and_docks(self):
        gate = Gate(reach=False)
        row = self.run_guard(gate)
        self.assertEqual(gate.looks, 0)
        self.assertEqual([kind for kind, _o in gate.goals()], ["navigate-to-system"] + ["go-to-poi"] * 3 + ["prepare-at-station"])
        self.assertEqual(self.rows(), [row])
        self.assertEqual((row["notes"], row["looks"], row["stay_minutes"], row["docked"]), (["place not reached"], 0, 0.0, True))

    def test_a_crash_still_writes_its_row_and_frees_the_pilot(self):
        def look(n):
            if n == 2:
                raise RuntimeError("the gate answered nonsense")
        gate = Gate(on_look=look, credits=None)
        with self.assertRaises(RuntimeError):
            self.run_guard(gate)
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["notes"][0], "guarded 1 min, 1 looks, 1 strangers, left: crashed")        # the second look never came back
        self.assertTrue(rows[0]["notes"][1].startswith("crashed: RuntimeError: the gate answered nonsense (line "), rows[0]["notes"])
        self.assertEqual(rows[0]["notes"][2:], ["wallet not read"])
        self.assertFalse((self.data / "fleet" / "orders" / "sentinel-1.json").exists())

    def test_the_command_line_needs_the_guarded_route_and_the_station(self):
        parse = self.guard.parse
        self.assertEqual(parse(["s-1", "far", "belt", "--guards", "belt-x", "--station", "home:core:base"]),
                         {"pilot": "s-1", "system": "far", "poi": "belt", "guards": "belt-x", "station": ["home", "core", "base"], "minutes": 60.0,
                          "route": "guard-belt-x", "follow": None})
        self.assertEqual(parse(["s-1", "far", "belt", "--guards", "kit-x", "--station", "home:core:base", "--follow", "hauler-1"])["follow"], "hauler-1")
        for args in (["s-1", "far", "belt", "--station", "home:core:base"], ["s-1", "far", "belt", "--guards", "belt-x"],
                     ["s-1", "far", "belt", "--guards", "belt-x", "--station", "home:core"], ["s-1", "far"]):
            with self.assertRaises(SystemExit):
                parse(args)

    def test_it_writes_no_sighting(self):
        source = (FLEET / "guard.py").read_text(encoding="ascii")
        self.assertNotIn("sightings", source.split('"""', 2)[2])           # its code names no sightings file: `sight` is their one writer
        self.run_guard(Gate(), minutes=1)
        self.assertFalse((self.data / "intel").exists())


class FollowTests(RunnerTests):
    """--follow <pilot>: the guard keeps beside one pilot of ours on a circuit (requests ENT-217, ENT-226): it reads that
    pilot's system and place from its live file once a minute, jumps and moves after it, looks, never fires, and ends
    when that pilot's order for the guarded route is gone."""

    def at(self, system, poi, docked=""):
        (self.data / "fleet" / "ships" / "hauler-1.json").write_text(json.dumps({"name": "hauler-1", "system": system, "poi": poi, "docked": docked}))

    def carrying(self, flying, what="circuit kit-x"):
        path = self.data / "fleet" / "orders" / "hauler-1.json"
        if flying:
            path.write_text(json.dumps({"pilot": "hauler-1", "what": what, "since": "2026-11-17T16:00:00Z"}))
        elif path.exists():
            path.unlink()

    def follow(self, gate, minutes=120):
        opts = self.guard.parse(["sentinel-1", "far", "belt", "--guards", "kit-x", "--station", "home:core:base", "--minutes", str(minutes),
                                 "--route", "guard-kit-x", "--follow", "hauler-1"])
        with contextlib.redirect_stdout(io.StringIO()) as said:
            row = self.guard.run(opts, gate, str(self.data), sleep=self.clock.sleep, clock=self.clock)
        self.said = said.getvalue()
        return row

    def test_it_jumps_after_the_followed_pilot_and_ends_when_its_order_is_gone(self):
        self.at("lhs", "crossroads", docked="crossroads_base")
        self.carrying(True)

        def look(n):
            if n == 2:
                self.at("antares", "antares_gate")           # the hauler jumped on after the second look
            if n == 4:
                self.carrying(False)                         # its run ended before the fourth look
        gate = Gate(on_look=look)
        row = self.follow(gate)
        moves = [(kind, options) for kind, options in gate.goals()]
        self.assertEqual(moves, [("navigate-to-system", {"targetSystemId": "lhs"}), ("go-to-poi", {"targetPoiId": "crossroads"}),
                                 ("navigate-to-system", {"targetSystemId": "antares"}), ("go-to-poi", {"targetPoiId": "antares_gate"}),
                                 ("prepare-at-station", {"systemId": "home", "poiId": "core", "baseId": "base", "refuel": True})])
        self.assertEqual((row["left"], row["looks"], row["follow"], row["jumps"], row["docked"]), ("guarded ship gone", 5, "hauler-1", 2, True))
        self.assertEqual(row["notes"][0], "followed hauler-1 4 min, 5 looks, 2 jumps, 1 strangers, left: guarded ship gone")
        self.assertFalse({action for _g, action, _p in gate.raws()} & FIRING)
        self.assertEqual([b["mode"] for m, p, b in gate.calls if p.endswith("/combat-mode")], ["flee"])
        self.assertIn("following hauler-1 on kit-x", self.said)

    def test_a_circuit_order_of_another_route_is_not_the_guarded_one(self):
        self.at("lhs", "crossroads")
        self.carrying(True, what="circuit some-other-route")
        gate = Gate()
        row = self.follow(gate)
        self.assertEqual((row["left"], row["looks"]), ("guarded ship gone", 2))
        self.assertEqual([kind for kind, _o in gate.goals()], ["navigate-to-system", "go-to-poi", "prepare-at-station"])

    def test_it_stays_put_while_the_followed_pilot_stays_and_leaves_under_60_percent(self):
        self.at("lhs", "crossroads")
        self.carrying(True)

        def look(n):
            if n == 3:
                self.ship(59, 100)
        gate = Gate(on_look=look)
        row = self.follow(gate)
        self.assertEqual((row["left"], row["looks"], row["jumps"]), ("hull 59%", 3, 1))
        self.assertEqual([kind for kind, _o in gate.goals()], ["navigate-to-system", "go-to-poi", "prepare-at-station"])

    def test_a_followed_pilot_it_cannot_reach_ends_the_run_and_it_docks(self):
        self.at("lhs", "crossroads")
        self.carrying(True)
        gate = Gate(reach=False)
        row = self.follow(gate)
        self.assertEqual((row["left"], row["looks"], row["docked"]), ("could not follow hauler-1", 0, True))

    def test_the_static_guard_is_unchanged_by_the_follow_tests(self):
        self.assertIsNone(self.guard.parse(["s-1", "far", "belt", "--guards", "belt-x", "--station", "home:core:base"])["follow"])


ROUTES = {
    "belt-x": {"id": "belt-x", "kind": "mine", "title": "t", "belt": "far:belt", "station": "home:core:base"},
    "rays": {"id": "rays", "kind": "hunt", "title": "t", "place": "far:nebula", "sell_at": "home:core:base", "species": ["veil_ray"], "max_ships": 1},
    "census": {"id": "census", "kind": "census", "title": "t", "systems": ["home", "far"], "every_minutes": 60, "max_ships": 1},
    "trade": {"id": "trade", "kind": "circuit", "title": "t", "stops": [{"at": "home:core:base"}], "max_ships": 1},
    "guard-x": {"id": "guard-x", "kind": "guard", "title": "t", "guards": "belt-x", "station": "home:core:base"},
    "open": {"id": "open", "kind": "mine", "title": "t", "belt": "far:rift", "station": "home:core:base"},
}


class KindTests(unittest.TestCase):
    """The dispatcher and the route gate on a disposable tree (the shape of test_fleet_dispatch.py)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-guard-kind-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.root / "fleet", self.data / "fleet" / "orders", self.data / "routes"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nhome\tHome\t0\t0\tvoidborn\nfar\tFar\t1\t0\tvoidborn\n", encoding="ascii")
        for rid, route in ROUTES.items():
            self.put(route)
        (self.root / "routes" / "plans" / "sentinel.json").write_text(json.dumps({"role": "sentinel", "owner": "Unity", "routes": ["guard-x", "open"]}),
                                                                         encoding="ascii")
        self.dispatch, self.routes = load("dispatch"), load("routes")
        self.now = time.time()
        self.pilot = {"name": "sentinel-1", "credits": 20000, "modules": [], "docked": True}

    def put(self, route):
        (self.root / "routes" / (route["id"] + ".json")).write_text(json.dumps(route), encoding="ascii")

    def why(self, route, orders=None):
        state = {"now": self.now, "data": str(self.data), "rows": [], "orders": orders or {}, "rest": {}, "booked": {}, "root": str(self.root)}
        return self.dispatch.why_not(self.pilot, route["id"], route, state)

    def test_a_guard_is_open_only_while_a_pilot_of_ours_flies_the_route_it_guards(self):
        guard = ROUTES["guard-x"]
        self.assertEqual(self.why(guard), ("nobody flies belt-x", None))
        self.assertEqual(self.why(guard, {"miner-9": "hunt belt-x", "miner-8": "guard belt-x"}), ("nobody flies belt-x", None))   # not its mark
        self.assertEqual(self.why(guard, {"miner-9": "mine belt-x"}), (None, "far:belt"))                 # the mine's belt
        self.assertEqual(self.why(dict(guard, place="far:gate"), {"miner-9": "mine belt-x"}), (None, "far:gate"))   # its own place wins
        self.assertEqual(self.why(dict(guard, guards="rays"), {"drone-1": "hunt rays"}), (None, "far:nebula"))      # a hunt's place
        self.assertEqual(self.why(dict(guard, guards="census"), {"scout-1": "census far"})[0], "guards `census`: no mine or hunt route file")
        self.assertEqual(self.why(dict(guard, guards="ghost"), {"miner-9": "mine ghost"})[0], "guards `ghost`: no mine or hunt route file")

    def test_one_guard_flies_it_unless_its_file_says_more(self):
        guard, orders = ROUTES["guard-x"], {"miner-9": "mine belt-x", "sentinel-2": "guard guard-x"}
        self.assertEqual(self.why(guard, orders), ("max_ships 1 reached", None))
        self.assertEqual(self.why(dict(guard, max_ships=2), orders), (None, "far:belt"))
        self.assertEqual(self.why(dict(guard, max_ships=2), dict(orders, **{"sentinel-3": "guard guard-x"}))[0], "max_ships 2 reached")

    def test_the_command_line(self):
        guard = ROUTES["guard-x"]
        self.assertEqual(self.dispatch.command(guard, "sentinel-1", "far:belt", str(self.root)),
                         [sys.executable, "-I", "-B", str(self.root / "fleet" / "guard.py"), "sentinel-1", "far", "belt", "--guards", "belt-x",
                          "--station", "home:core:base", "--minutes", "60", "--route", "guard-x"])
        self.assertEqual(self.dispatch.command(dict(guard, minutes=30), "sentinel-1", "far:gate", str(self.root))[5:7], ["far", "gate"])
        self.assertIn("--minutes", self.dispatch.command(guard, "sentinel-1", None, str(self.root)))      # no place found: a run that says so, no crash here

    def test_a_dry_pass_starts_the_guard_beside_the_guarded_ship(self):
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": [{"name": "sentinel-1", "status": "connected", "credits": 20000,
                                                                               "activity": {"kind": "idle"}}]}))
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["sentinel-1 -> mine open"])      # nobody on belt-x
        (self.data / "fleet" / "orders" / "miner-9.json").write_text(json.dumps({"pilot": "miner-9", "what": "mine belt-x"}))
        self.assertEqual(self.dispatch.one_pass(str(self.root), str(self.data), True, []), ["sentinel-1 -> guard guard-x"])

    def test_a_guard_is_standing_work_and_never_ends_a_plan(self):
        guard = ROUTES["guard-x"]
        self.assertTrue(self.routes.standing(guard))
        self.assertEqual(self.routes.stage(guard), "service")
        self.assertFalse(self.dispatch.judged(guard))
        self.assertEqual(self.routes.closes(guard), ["limits"])
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.now - 600))
        lost = [{"route": "guard-x", "pilot": "s-%d" % n, "started": stamp, "minutes": 30, "credits_before": 9000, "credits_after": 8900} for n in (1, 2, 3)]
        self.assertEqual(self.dispatch.losing(self.dispatch.load_routes(self.root), lost, self.now), {})    # its fuel is its price

    def test_the_gate_refuses_a_guard_without_a_route_or_without_a_place(self):
        def errors_with(change):
            self.put(dict(ROUTES["guard-x"], **change))
            found = [e for e in self.routes.check(str(self.root))[0] if "index.md" not in e]
            self.put(ROUTES["guard-x"])
            return found
        self.assertEqual(errors_with({}), [])
        self.assertEqual(errors_with({"guards": ""}), ["game/routes/guard-x.json: `guards` is missing"])
        self.assertEqual(errors_with({"station": ""}), ["game/routes/guard-x.json: `station` is missing"])
        self.assertEqual(errors_with({"guards": "ghost"}), ["game/routes/guard-x.json: `guards` names `ghost`, which is no route file"])
        for rid, kind in (("census", "census"), ("trade", "circuit"), ("guard-x", "guard")):
            self.assertEqual(errors_with({"guards": rid}),
                             ["game/routes/guard-x.json: `guards` names `%s`, a %s: a guard keeps the place of a mine or a hunt, and it has none" % (rid, kind)])
        self.assertEqual(errors_with({"place": "far"}), ["game/routes/guard-x.json: `place` must have 2 parts joined by a colon"])
        self.assertEqual(errors_with({"place": "nowhere:belt"}), ["game/routes/guard-x.json: system `nowhere` is not on the chart"])
        self.assertEqual(errors_with({"guards": "rays", "place": "far:gate"}), [])

    def test_the_dispatcher_names_its_runner_for_the_fleet_index(self):
        self.assertEqual(self.dispatch.KINDS["guard"], "guard.py")
        self.assertIn("guard    -> game/fleet/guard.py", self.dispatch.__doc__)
        self.assertEqual(self.routes.KINDS["guard"], ("guards", "station"))


if __name__ == "__main__":
    unittest.main()
