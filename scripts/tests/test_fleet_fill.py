"""game/fleet/fill.py on a disposable repository and data folder: why ships wait, the gate, and the plan it fills. No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
HOME = {"at": "home:core:base"}
GATHER = "class: gather is miners' work"          # rule F23's reason for a gather route offered to another role (game/fleet/pull.py)
MEASURED = lambda cph: {"date": "2026-11-15", "runs": 3, "minutes": 30, "credits_per_run": cph // 2, "cph_per_ship": cph}
ROUTES = {
    "park": {"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [HOME]},
    "once": {"id": "once", "kind": "circuit", "title": "t", "once": True, "stops": [HOME]},
    "rays": {"id": "rays", "kind": "hunt", "title": "t", "place": "home:nebula", "sell_at": "home:core:base", "max_ships": 1, "measured": MEASURED(3000)},
    "ice": {"id": "ice", "kind": "mine", "title": "t", "belt": "far:belt", "station": "home:core:base", "max_ships": 2, "requires": {"module": "ice_harvester"},
            "sell": [{"item": "water_ice", "min_price": 20}], "measured": MEASURED(5000)},
    "herd2": {"id": "herd2", "kind": "hunt", "title": "t", "place": "far:cloud", "sell_at": "home:core:base", "max_ships": 1, "measured": MEASURED(2000)},
    "bad": {"id": "bad", "kind": "hunt", "title": "t", "place": "far:rift", "sell_at": "home:core:base", "measured": MEASURED(-300)},
    "freight": {"id": "freight", "kind": "circuit", "title": "t", "max_ships": 1, "stops": [HOME], "measured": MEASURED(1500)},     # paying work that is no hunt: open to every role
}
PLANS = {"drone": ("Apophis", ["once", "rays", "park"]), "hauler": ("Apollo", ["once", "park"]), "miner": ("Zero", ["ice", "park"])}
SHIPS = {"drone-1": [], "drone-2": [], "hauler-1": [], "hauler-2": [], "hauler-3": [], "miner-1": ["ice_harvester"], "miner-2": []}
CANDIDATES = [
    {"id": "trade-x", "kind": "trade", "per_ship_hour": 900, "status": "new", "route_id": "",
     "route": {"id": "trade-x", "kind": "circuit", "title": "t", "note": "An estimate.", "max_ships": 1, "stops": [HOME]}},
    {"id": "mine-gas", "kind": "mine", "per_ship_hour": 800, "status": "new", "route_id": "",
     "route": {"id": "mine-gas", "kind": "mine", "title": "t", "belt": "far:gas", "station": "home:core:base", "max_ships": 1, "requires": {"module": "gas_harvester"}}},
    {"id": "craft-y", "kind": "craft", "per_ship_hour": 7000, "status": "new", "route_id": "", "needs": "a craft step in the circuit runner"},
    {"id": "trade-buys", "kind": "trade", "per_ship_hour": 5000, "status": "new", "route_id": "",
     "route": {"id": "trade-buys", "kind": "circuit", "title": "t", "max_ships": 1, "stops": [{"at": "home:core:base", "buy": [{"item": "x", "qty": 5, "max_price": 100}]}]}},
    {"id": "trade-low", "kind": "trade", "per_ship_hour": 100, "status": "new", "route_id": "",
     "route": {"id": "trade-low", "kind": "circuit", "title": "t", "max_ships": 1, "stops": [HOME]}},
]


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-fill-test-")
        self.addCleanup(self.temp.cleanup)
        self.top, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        self.root = self.top / "game"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.data / "fleet" / "orders", self.data / "fleet" / "ships", self.data / "routes", self.data / "market"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nid\tname\tx\ty\tempire\tflags\tjumps_from_home\tlanes\nhome\tHome\t0\t0\tvoidborn\t-\t0\tfar\n"
                                                      "far\tFar\t1\t0\tvoidborn\t-\t1\thome\n", encoding="ascii")
        for rid, route in ROUTES.items():
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        for role, (owner, ids) in PLANS.items():
            (self.root / "routes" / "plans" / (role + ".json")).write_text(json.dumps({"role": role, "owner": owner, "note": "n", "routes": ids}, indent=1) + "\n", encoding="ascii")
        self.fill = load("fill")
        self.fill.routefiles.write_index(str(self.root))
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "start")
        self.now = time.time()
        ships = [{"name": name, "status": "connected", "activity": {"kind": "idle"}, "docked": True, "credits": 20000, "cargo_used": 0} for name in SHIPS]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"updated_at": "now", "ships": ships}))
        for name, modules in SHIPS.items():
            (self.data / "fleet" / "ships" / (name + ".json")).write_text(json.dumps({"modules": [{"type": m} for m in modules], "cargo": []}))
        with open(self.data / "routes" / "runs.jsonl", "w") as handle:
            for name in SHIPS:
                handle.write(json.dumps({"route": "once", "pilot": name, "stops": 1, "of": 1}) + "\n")
        self.put_list(CANDIDATES)
        (self.data / "market" / "base.json").write_text(json.dumps({"base": "base", "items": [
            {"item_id": "water_ice", "best_buy": 28, "best_buy_qty": 5200}, {"item_id": "ice_harvester", "best_sell": 1413, "best_sell_qty": 2}]}))

    def put_list(self, candidates, age=60):
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - age))
        (self.data / "routes" / "opportunities.json").write_text(json.dumps({"written_at": stamp, "candidates": candidates}))

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.top)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout

    def read(self, role, **more):
        seen = self.fill.survey(str(self.root), str(self.data))
        return seen, self.fill.read_role(seen, role, **more)

    def flown(self, rid, pilot="hauler-9"):
        """One run row of a route: it has flown (fill.spare lifts only a route with a run, requests ENT-216)."""
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            handle.write(json.dumps({"route": rid, "pilot": pilot, "stops": 1, "of": 1, "started": "2026-11-17T10:00:00Z", "minutes": 30,
                                     "credits_before": 20000, "credits_after": 19800, "delta": -200}) + "\n")

    def run_fill(self, member, *args):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HERMES_SESSION_PROFILE": member, "HOME": self.temp.name, "FLEET_TAXES": os.devnull,
               "FLEET_COMMIT_WAIT": "0"}                   # a route file in work is looked at again without the seconds between
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "fill.py")] + list(args) + ["--root", str(self.root), "--data", str(self.data)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)


class ReadTests(Tree):
    def test_a_pilot_with_an_open_route_starts_and_the_rest_wait_with_the_reason(self):
        seen, got = self.read("drone")
        self.assertEqual((got["starting"], got["waiting"]), ([("drone-1", "rays")], ["drone-2"]))
        self.assertEqual({rid: dict(why) for rid, _f, _c, why, _h in got["plan"]},
                         {"once": {"done once": 1}, "rays": {"max_ships 1 reached": 1}, "park": {"the pilot is docked": 1}})          # of the one that waits
        self.assertEqual(got["paying"], [("herd2", 2000, ["drone-2"])])                           # measured above zero, a free place, in no plan of theirs
        self.assertEqual(self.fill.verdict(seen, got)[0], False)
        self.assertIn("HALT: 1 ships of drone wait while 1 places of paying work and 0 tests stand open", self.fill.verdict(seen, got)[1])

    def test_a_sale_circuit_is_never_added_to_another_class_s_plan(self):
        # orders ENT-061 P5, Apollo (reports.log ENT-101): the hourly pass added sell circuits to miner, hauler and sentinel plans
        sale = dict(ROUTES["freight"], id="sell-x", stops=[dict(HOME, sell=[{"item": "water_ice", "min_price": 1}])])
        (self.root / "routes" / "sell-x.json").write_text(json.dumps(sale, indent=1) + "\n", encoding="ascii")
        _seen, got = self.read("hauler")
        self.assertNotIn("sell-x", [rid for rid, _value, _pilots in got["paying"]])
        self.assertEqual(got["closed"].get(self.fill.SALE_TRADES), [(1500, "sell-x")])

    def test_work_outside_the_plan_is_offered_once_and_what_closes_the_rest_is_named(self):
        _seen, got = self.read("hauler")
        self.assertEqual(got["waiting"], ["hauler-1", "hauler-2", "hauler-3"])
        self.assertEqual(got["paying"], [("freight", 1500, ["hauler-1"])])                        # one place: one pilot
        self.assertEqual([(rid, value, pilot) for rid, value, _draft, pilot in got["tests"]], [("trade-x", 900, "hauler-2")])
        self.assertEqual(got["idle"], ["hauler-3"])
        self.assertEqual(got["closed"], {GATHER: [(5000, "ice"), (800, "mine-gas")], self.fill.NO_HUNT: [(3000, "rays"), (2000, "herd2")]})    # rule F16: haulers earn;
        # rule F23: gathering is the miners' (2026-11-17: the filler lent iron routes to every waiting ship); never `bad`, `craft-y`, `trade-low`
        self.assertEqual(got["by_hand"], [(5000, "trade-buys")])                                 # it buys goods: never added by itself, however high its estimate
        _seen, got = self.read("hauler", tests=0)
        self.assertEqual((got["tests"], got["idle"]), ([], ["hauler-2", "hauler-3"]))

    def test_only_work_the_waiting_ships_may_take_is_counted(self):
        bought = dict(ROUTES["herd2"], id="gap", kind="circuit", stops=[{"at": "home:core:base", "buy": [{"item": "x", "qty": 5, "max_price": 100}]}])
        bought.pop("place"); bought.pop("sell_at")
        (self.root / "routes" / "gap.json").write_text(json.dumps(bought, indent=1) + "\n", encoding="ascii")
        mission = dict(ROUTES["once"], id="board", measured=MEASURED(6000))
        (self.root / "routes" / "board.json").write_text(json.dumps(mission, indent=1) + "\n", encoding="ascii")
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            for pilot in ("hauler-7", "hauler-8"):
                handle.write(json.dumps({"route": "board", "pilot": pilot, "stops": 1, "of": 1, "notes": ["board_mission not offered"]}) + "\n")
            handle.write(json.dumps({"route": "board", "pilot": "drone-7", "stops": 1, "of": 1, "notes": []}) + "\n")
        seen, got = self.read("hauler")
        self.assertNotIn("gap", [rid for rid, _v, _p in got["paying"]])                          # it buys goods: its Admiral's word puts it in a plan
        self.assertIn((2000, "gap"), got["by_hand"])
        self.assertNotIn("board", [rid for rid, _v, _p in got["paying"]])                        # refused to every hauler that flew it
        self.assertIn("board", [rid for _v, rid in got["closed"]["the board refused it to this role"]])
        _seen, drones = self.read("drone")
        self.assertNotIn("board", (drones["closed"].get("the board refused it to this role") or []))

    def test_one_good_run_is_no_paying_route_and_a_losing_route_is_offered_to_nobody(self):
        once = dict(ROUTES["freight"], measured=dict(MEASURED(1500), runs=1))
        (self.root / "routes" / "freight.json").write_text(json.dumps(once, indent=1) + "\n", encoding="ascii")
        _seen, got = self.read("hauler")
        self.assertEqual(got["paying"], [])                                                       # measured on one run: not yet a route that pays
        (self.root / "routes" / "freight.json").write_text(json.dumps(ROUTES["freight"], indent=1) + "\n", encoding="ascii")
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - ago))
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            for ago, delta in ((900, 105), (300, -4635)):
                handle.write(json.dumps({"route": "freight", "pilot": "drone-9", "minutes": 10, "started": stamp(ago), "credits_before": 9000, "credits_after": 9000 + delta}) + "\n")
        _seen, got = self.read("hauler")
        self.assertEqual(got["paying"], [])
        self.assertIn("at a loss: 2 runs, -4,530 cr in 6 hours", got["closed"])

    def test_a_module_decides_and_a_bid_says_how_many_ships_a_mine_carries(self):
        seen, got = self.read("miner")
        self.assertEqual((got["starting"], got["waiting"]), ([("miner-1", "ice")], ["miner-2"]))
        self.assertEqual(dict(got["plan"][0][3]), {"needs ice_harvester": 1})
        deep = self.fill.carries(seen, ROUTES["ice"])
        self.assertEqual((deep["ships"], deep["extra"], self.fill.carried(deep)), (None, 20, "? +20"))    # 5,200 units stand: 260 a ship in four hours
        self.assertIn("what the water_ice bid at base regains is not measured; 5,200 units stand at 28 cr now", deep["text"])
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - ago))
        (self.data / "market" / "history.jsonl").write_text("".join(
            json.dumps({"t": stamp(ago), "base": "base", "item": "water_ice", "bid": 28, "bid_qty": units, "ask": 0, "ask_qty": 0}) + "\n"
            for ago, units in ((7200, 5000), (3600, 4800), (0, 5200))))
        seen, _got = self.read("miner")
        deep = self.fill.carries(seen, ROUTES["ice"])                                             # errors ENT-046, ENT-054: sized on the depth, not on the regain
        self.assertEqual((deep["ships"], deep["extra"], self.fill.carried(deep)), (3, 20, "3 +20"))        # 400 units came back in two hours; a ship brings 65 an hour
        self.assertIn("regains 200 units an hour at its best price", deep["text"])
        self.assertIsNone(self.fill.carries(seen, ROUTES["once"]))
        # a gathering field: read full twice (no regain to see: not measured, never 0), and its own floor counted off
        (self.data / "wildlife").mkdir(exist_ok=True)
        (self.data / "scouting").mkdir(exist_ok=True)
        (self.data / "wildlife" / "history.jsonl").write_text("".join(
            json.dumps({"at": stamp(ago), "system": "far", "deposits": {"rocks": {"iron_ore": 100000}}}) + "\n" for ago in (7200, 0)))
        (self.data / "scouting" / "far.json").write_text(json.dumps({"system": "far", "read_at": stamp(0), "pois": {"rocks": {"resources": [{"resource_id": "iron_ore", "remaining": 100000}]}}}))
        gather = {"id": "gather", "kind": "mine", "belt": "far:rocks", "station": "home:core:base", "min_left": {"iron_ore": 40000}}
        seen, _got = self.read("miner")
        deep = self.fill.carries(seen, gather)
        self.assertEqual((deep["ships"], deep["extra"], self.fill.carried(deep)), (None, 230, "? +230"))    # 60,000 above the floor, 260 a ship in four hours
        self.assertIn("what its field grows back is not measured; 100,000 units lie in it, 60,000 above its floor", deep["text"])
        self.assertEqual(self.fill.carried(None), "--")
        self.assertEqual(self.fill.asks(seen, "ice_harvester"), [(2, 1413, "base")])
        # requests ENT-333: a gather on a mixed field counts only the goods its floor names (silicon none: it carries no ship)
        (self.data / "scouting" / "mixed.json").write_text(json.dumps({"system": "mixed", "read_at": stamp(0), "pois": {"flats": {"resources": [
            {"resource_id": "iron_ore", "remaining": 78875}, {"resource_id": "copper_ore", "remaining": 96000}, {"resource_id": "silicon_ore", "remaining": 0}]}}}))
        silicon = {"id": "silicon", "kind": "mine", "belt": "mixed:flats", "station": "home:core:base", "min_left": {"silicon_ore": 500}}
        deep = self.fill.carries(seen, silicon)
        self.assertEqual((deep["ships"], deep["extra"], self.fill.carried(deep)), (0, 0, "0"))
        self.assertIn("none of its goods (silicon_ore)", deep["text"])
        iron = dict(silicon, min_left={"iron_ore": 40000})
        deep = self.fill.carries(seen, iron)
        self.assertIn("78,875 units lie in it, 38,875 above its floor", deep["text"])

    def test_the_gate_passes_only_on_a_fresh_list(self):
        for name in ("herd2", "freight"):                                                         # no paying work outside the plan
            (self.root / "routes" / (name + ".json")).unlink()
        self.put_list([])
        seen, got = self.read("hauler")
        ok, line = self.fill.verdict(seen, got)                                                   # Suggi, 2026-11-16: no ship idle: a waiting ship is a HALT
        self.assertEqual((ok, line.startswith("HALT: 3 ships of hauler wait and nothing that pays is open to them: the plan lacks standing work")), (False, True))
        self.put_list([], age=2 * 3600)
        seen, got = self.read("hauler")
        self.assertEqual(self.fill.verdict(seen, got)[0], False)
        self.assertIn("the route maker's list is 120 minutes old", self.fill.verdict(seen, got)[1])
        (self.data / "fleet" / "orders" / "hauler-1.json").write_text(json.dumps({"what": "circuit once"}))
        (self.data / "fleet" / "orders" / "hauler-2.json").write_text(json.dumps({"what": "hand Apollo"}))
        seen, got = self.read("hauler")
        self.assertEqual((got["work"], got["hand"], got["waiting"]), (["hauler-1"], ["hauler-2"], ["hauler-3"]))


class WriteTests(Tree):
    def test_fill_writes_the_plan_the_route_file_and_the_indexes_in_one_commit(self):
        done = self.run_fill("apollo", "check")
        self.assertEqual((done.returncode, done.stdout.count("HALT")), (1, 1))
        done = self.run_fill("apollo", "fill")
        self.assertIn("hauler: 3 waiting, 0 on standing work; 1 paying routes and 1 tests to add: freight, trade-x", done.stdout)
        self.assertIn("not written: add --write", done.stdout)
        self.assertEqual(self.git("status", "--porcelain"), "")
        done = self.run_fill("apollo", "fill", "--write")
        self.assertIn("committed", done.stdout, done.stdout)
        plan = json.loads((self.root / "routes" / "plans" / "hauler.json").read_text())
        self.assertEqual(plan["routes"], ["once", "trade-x", "freight", "park"])                  # the role's routes in one order, from the division's plan file
        self.assertEqual((plan["ships"], plan["of"]), ({"once": 3, "trade-x": 1, "freight": 1, "park": 3}, 3))
        lists = json.loads((self.data / "plans" / "assign.json").read_text())["pilots"]          # each a ship's own route: the paying one to the ship it was open to
        self.assertEqual(sorted(lists.values()), [["once", "freight", "park"], ["once", "park"], ["once", "trade-x", "park"]])
        test = json.loads((self.root / "routes" / "trade-x.json").read_text())
        self.assertEqual((test["max_ships"], "Added as a test by fill.py" in test["note"]), (3, True))           # rule F37: three results at once
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.git("log", "-1", "--format=%an"), "Apollo\n")
        self.assertEqual(sorted(self.git("show", "--name-only", "--format=", "HEAD").split()),
                         ["game/routes/index-tests.md", "game/routes/master-index.md", "game/routes/plan-hauler.md", "game/routes/plans/hauler.json", "game/routes/trade-x.json"])
        done = self.run_fill("apollo", "check")                                                   # the dispatcher would start two; the third has nothing open
        self.assertEqual((done.returncode, done.stdout.startswith("HALT: 1 ships of hauler wait and nothing that pays is open to them")), (1, True))

    def commit_route(self, route):
        (self.root / "routes" / (route["id"] + ".json")).write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        self.fill.routefiles.write_index(str(self.root))
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "a route")

    def test_a_guidebook_in_work_holds_no_plan_change_and_a_route_file_in_work_is_waited_for(self):
        self.commit_route({"id": "gather", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "max_ships": 5})
        (self.root / "routes" / "guidebook").mkdir()
        (self.root / "routes" / "guidebook" / "military.md").write_text("an Admiral writes its guidebook for most of a turn\n")
        self.assertIn("committed", self.run_fill("apollo", "add", "gather").stdout)                # requests ENT-171: no script reads a guidebook
        self.assertEqual(self.git("status", "--porcelain").split(), ["??", "game/routes/guidebook/"])      # still there, still the Admiral's to commit
        looks, real = [], self.fill.in_work
        self.fill.in_work = lambda root: looks.append(1) or ([" M game/routes/ice.json"] if len(looks) < 3 else real(root))
        self.addCleanup(setattr, self.fill, "in_work", real)
        text = json.dumps({"role": "hauler", "owner": "Apollo", "routes": ["once", "gather", "park"]}, indent=1) + "\n"
        done, line = self.fill.commit(str(self.root), str(self.data), "Apollo", {"routes/plans/hauler.json": text}, "a plan", tries=4, wait=0)
        self.assertEqual((done, len(looks)), (True, 3), line)                                      # the other member committed between two looks
        done, line = self.fill.commit(str(self.root), str(self.data), "Apollo", {"routes/plans/hauler.json": text.replace("once", "gather2")}, "a plan", tries=1, wait=0)
        self.assertEqual((done, line.split("\n")[0]), (True, line.split("\n")[0]) if done else (False, "HALT: nothing changed; the route gate says:"))

    def test_standing_work_gives_every_waiting_ship_a_place_and_the_gate_passes(self):
        self.commit_route({"id": "gather", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "max_ships": 5})
        self.assertEqual(self.run_fill("apollo", "check").returncode, 1)
        self.assertIn("committed", self.run_fill("apollo", "add", "gather").stdout)
        done = self.run_fill("apollo", "check")
        self.assertEqual((done.returncode, done.stdout), (0, "PASS: no ship of hauler waits\n"))

    def test_a_ship_on_standing_work_is_offered_paying_work_and_the_gate_says_so(self):
        self.commit_route({"id": "gather", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "standing": True, "max_ships": 5})
        self.assertIn("committed", self.run_fill("apollo", "add", "gather").stdout)
        orders = self.data / "fleet" / "orders"
        for name in ("hauler-1", "hauler-2", "hauler-3"):                                          # all three gather now
            (orders / (name + ".json")).write_text(json.dumps({"pilot": name, "what": "mine gather", "since": "2026-11-16T10:00:00Z"}))
        done = self.run_fill("apollo", "check")
        self.assertEqual(done.returncode, 0)
        self.assertIn("PASS: no ship of hauler waits | 1 places of paying work and 1 tests stand open to its ships on standing work", done.stdout)
        self.assertIn("committed", self.run_fill("apollo", "fill", "--write").stdout)
        lists = json.loads((self.data / "plans" / "assign.json").read_text())["pilots"]
        self.assertEqual(sorted(ids.index("gather") > ids.index(rid) for ids in lists.values() for rid in ("freight", "trade-x") if rid in ids), [True, True])   # before its standing work
        self.assertEqual(self.run_fill("apollo", "check").stdout, "PASS: no ship of hauler waits\n")

    def test_the_gate_names_the_ships_that_stand_on_park(self):
        # Apollo's report of 2026-11-17: the gate read PASS while a hauler parked; park is the route no ship should reach (rule F8)
        self.commit_route({"id": "gather", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "standing": True, "max_ships": 5})
        self.assertIn("committed", self.run_fill("apollo", "add", "gather").stdout)
        orders = self.data / "fleet" / "orders"
        for name, what in (("hauler-1", "circuit park"), ("hauler-2", "mine gather"), ("hauler-3", "mine gather")):
            (orders / (name + ".json")).write_text(json.dumps({"pilot": name, "what": what, "since": "2026-11-16T10:00:00Z"}))
        seen, got = self.read("hauler")
        self.assertEqual(got["park"], ["hauler-1"])
        passed, line = self.fill.verdict(seen, got)
        self.assertTrue(passed)                                                                      # at work by its order: no HALT
        self.assertIn("1 on park, the route no ship should reach", line)
        self.assertIn("hauler-1", line)

    def test_standing_work_that_is_full_while_ships_wait_is_lifted_as_far_as_its_field_carries(self):
        # 2026-11-16: the gate said HALT three times until a shared gather route was lifted by hand; its field held tens of thousands above its floor
        self.commit_route({"id": "gather", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "standing": True, "max_ships": 1,
                           "min_left": {"iron_ore": 99400}, "open_to": ["hauler"]})                 # its Admiral's word: haulers gather here (rule F23)
        self.assertIn("committed", self.run_fill("apollo", "add", "gather").stdout)
        (self.data / "scouting").mkdir(exist_ok=True)
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (self.data / "scouting" / "far.json").write_text(json.dumps({"system": "far", "read_at": stamp, "pois": {"rocks": {"resources": [{"resource_id": "iron_ore", "remaining": 100000}]}}}))
        seen, got = self.read("hauler")
        self.assertEqual((len(got["starting"]), len(got["waiting"])), (1, 2))                     # one hauler gathers, two wait at its limit
        self.assertEqual(self.fill.spare(seen, got), [])                                          # requests ENT-216: never flown, a test keeps one ship
        self.assertIn("gather", seen.get("unflown") or {})
        for _ in range(2):
            self.flown("gather")
        seen, got = self.read("hauler")
        self.assertEqual(self.fill.spare(seen, got), [])                                          # rule F37: two results decide nothing
        self.flown("gather")
        seen, got = self.read("hauler")
        self.assertEqual(self.fill.spare(seen, got), [("gather", 1)])                             # 600 units above the floor carry two ships a turn: one place more
        self.assertEqual(self.fill.spare(seen, got, served=set(got["waiting"])), [])              # ships that get other work need no place
        chart = self.root / "map" / "galaxy.tsv"                                                  # 2026-11-17: a lawless test route was raised from 1 ship to 4 by this script
        policed = chart.read_text(encoding="ascii")
        chart.write_text(policed.replace("far\tFar\t1\t0\tvoidborn", "far\tFar\t1\t0\t"), encoding="ascii")
        self.assertEqual(self.fill.spare(seen, got), [])                                          # beyond the border the limit is its Admiral's (rule F13)
        chart.write_text(policed, encoding="ascii")
        done = self.run_fill("unity", "fill", "all", "--once")
        self.assertIn("gather: standing work, full while 1 ship waits and its field carries more: max_ships 1 -> 2 (not written: add --write)", done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "gather.json").read_text())["max_ships"], 1)
        done = self.run_fill("unity", "fill", "all", "--once", "--write")
        self.assertIn("max_ships 1 -> 2", done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "gather.json").read_text())["max_ships"], 2)
        self.assertNotIn("max_ships", self.run_fill("unity", "fill", "all", "--once", "--write").stdout)      # the field carries no third ship
        self.assertEqual(self.git("status", "--porcelain"), "")
        sells = dict(json.loads((self.root / "routes" / "gather.json").read_text()), sell=[{"item": "iron_ore", "min_price": 1}], max_ships=1)
        seen["routes"]["gather"] = sells                                                          # a route that sells is its Admiral's to lift
        self.assertEqual(self.fill.spare(seen, got), [])

    def test_fill_names_the_ship_each_test_went_to(self):
        done = self.run_fill("apollo", "fill")                                                    # Zero, 2026-11-16: a test on a ship's own routes went unseen
        self.assertRegex(done.stdout, r"  test trade-x -> hauler-\d \(in front of its own routes")

    def test_the_once_pass_adds_only_missions_that_pay_once_behind_the_once_line(self):
        # requests ENT-144: a new once route reached a plan only at its Admiral's next turn, hours later
        self.commit_route(dict(ROUTES["once"], id="board", measured=MEASURED(6000)))
        done = self.run_fill("unity", "fill", "all", "--once", "--write")
        self.assertIn("committed", done.stdout, done.stdout)
        plans = {role: json.loads((self.root / "routes" / "plans" / (role + ".json")).read_text())["routes"] for role in PLANS}
        self.assertEqual(plans, {"drone": ["once", "board", "rays", "park"], "hauler": ["once", "board", "park"], "miner": ["board", "ice", "park"]})   # herd2 and freight repeat, trade-x is a test: all stay out
        self.assertEqual((self.git("log", "-1", "--format=%an"), self.git("status", "--porcelain")), ("Unity\n", ""))
        self.assertIn("nothing to add", self.run_fill("unity", "fill", "all", "--once", "--write").stdout)

    def test_the_once_pass_never_adds_a_route_that_unfits_a_module(self):
        # requests ENT-466 (Zero), errors.log ENT-166 (Apophis): the pass put a strip route into another division's First
        self.commit_route(dict(ROUTES["once"], id="strip-x", measured=MEASURED(6000),
                               stops=[{"at": "home:core:base", "unfit": ["pulse_laser_i"], "store": "all"}]))
        done = self.run_fill("unity", "fill", "all", "--once", "--write")
        plans = {role: json.loads((self.root / "routes" / "plans" / (role + ".json")).read_text())["routes"] for role in PLANS}
        self.assertTrue(all("strip-x" not in ids for ids in plans.values()), (plans, done.stdout))
        _seen, got = self.read("hauler")
        self.assertIn("strip-x", [rid for _v, rid in got["by_hand"]])                            # listed for its Admiral's word, never added

    def test_a_member_changes_its_own_plans_only_and_never_a_tree_in_work(self):
        done = self.run_fill("zero", "fill", "hauler", "--write")
        self.assertEqual((done.returncode, "REFUSED: the hauler plan is kept by Apollo" in done.stdout), (1, True))
        (self.root / "routes" / "rays.json").write_text(json.dumps(dict(ROUTES["rays"], title="x"), indent=1) + "\n")
        done = self.run_fill("apollo", "fill", "--write")
        self.assertIn("REFUSED: game/routes holds a change that is not committed", done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "plans" / "hauler.json").read_text())["routes"], ["once", "park"])
        self.git("checkout", "--", ".")
        (self.data / "fleet" / "STOP").write_text("")
        self.assertIn("REFUSED: fleet/STOP exists", self.run_fill("apollo", "fill", "--write").stdout)

    def test_add_drop_and_lift_are_one_command_each_and_the_gate_undoes_a_wrong_one(self):
        self.assertIn("committed", self.run_fill("apophis", "add", "herd2", "--role", "drone").stdout)
        self.assertEqual(json.loads((self.root / "routes" / "plans" / "drone.json").read_text())["routes"], ["once", "herd2", "rays", "park"])     # Military holds two roles (drone, and the sentinels lent, D226): into each drone's own routes
        self.assertIn("committed", self.run_fill("apophis", "lift", "herd2", "3").stdout)
        self.assertEqual(json.loads((self.root / "routes" / "herd2.json").read_text())["max_ships"], 3)
        self.assertIn("REFUSED: ice stands in no plan of yours", self.run_fill("apophis", "lift", "ice", "9").stdout)
        done = self.run_fill("zero", "lift", "ice", "30")                                         # Suggi, 2026-11-16: read what a route carries before lifting it
        self.assertEqual((done.returncode, "REFUSED: ice carries about 20 ships, not 30" in done.stdout), (1, True), done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "ice.json").read_text())["max_ships"], 2)
        self.assertIn("committed", self.run_fill("zero", "lift", "ice", "20").stdout)
        kit = self.root / "routes" / "templates" / "military.json"                               # a template of the division that holds the route
        kit.parent.mkdir()
        kit.write_text(json.dumps({"division": "military", "owner": "Apophis", "templates": {"hunts": {"routes": ["herd2", "rays"]}}}, indent=1) + "\n", encoding="ascii")
        subprocess.run([sys.executable, "-I", "-B", str(FLEET / "routes.py"), "index", "--root", str(self.root)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.git("add", "-A")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "a template")
        done = self.run_fill("apophis", "drop", "herd2", "--role", "drone")
        self.assertIn("committed", done.stdout)
        self.assertIn("note: herd2 still stands in the template @hunts of the military division", done.stdout)       # plan.take_out cannot reach a template
        done = self.run_fill("apophis", "drop", "park", "--role", "drone")                                           # a plan must end with a route that is always open
        self.assertEqual((done.returncode, "HALT military: nothing changed; the plan applied last stays in force" in done.stdout), (1, True), done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "plans" / "drone.json").read_text())["routes"], ["once", "rays", "park"])
        self.assertEqual(self.git("status", "--porcelain"), "")


class IndexDebounceTests(Tree):
    """Zero's and Mercury's reports of 2026-11-24: fill.py lift refused every lift and plan.py apply left the
    repository's copy behind, because commit() deferred the index for FLEET_INDEX_DEBOUNCE seconds after any index
    write and the route gate then found that index stale. A commit that changes what the index shows writes it."""

    def test_a_lift_within_the_debounce_window_writes_the_index_and_commits(self):
        os.environ["FLEET_INDEX_DEBOUNCE"] = "900"
        self.addCleanup(os.environ.pop, "FLEET_INDEX_DEBOUNCE", None)
        route = json.loads((self.root / "routes" / "ice.json").read_text())
        route["max_ships"] = 7
        ok, said = self.fill.commit(str(self.root), str(self.data), "Zero", {"routes/ice.json": json.dumps(route, indent=1) + "\n"}, "ice to 7")
        self.assertTrue(ok, said)
        self.assertEqual(json.loads((self.root / "routes" / "ice.json").read_text())["max_ships"], 7)
        self.assertEqual(self.fill.routefiles.check(str(self.root))[0], [])
        self.assertEqual(self.git("status", "--porcelain"), "")


class ReserveTests(Tree):
    """requests ENT-213 (Zero) and Military's report of 2026-11-17: fill.py wrote tests that sold silicon, iron and nickel the
    reserve is short of, and its hourly job put an armor-plate sale into a drone's routes (rule F24)."""

    def test_a_route_or_a_test_that_sells_a_short_item_is_not_added_and_says_why(self):
        sells_ice = dict(CANDIDATES[1], id="mine-ice-sell", route=dict(CANDIDATES[1]["route"], id="mine-ice-sell", requires={}, open_to=["hauler"],
                                                                          sell=[{"item": "water_ice", "min_price": 20}]))
        self.put_list([sells_ice] + CANDIDATES)
        seen = self.fill.survey(str(self.root), str(self.data))
        seen["kept"] = {"water_ice": 500}                                                        # what surplus.py would read: the reserve lacks it
        got = self.fill.read_role(seen, "hauler")
        self.assertNotIn("mine-ice-sell", [rid for rid, _v, _d, _p in got["tests"]])
        self.assertIn("mine-ice-sell", [rid for _v, rid in got["closed"].get(self.fill.RESERVE_SHORT, [])])
        seen = self.fill.survey(str(self.root), str(self.data))
        seen["kept"] = {}
        got = self.fill.read_role(seen, "hauler")
        self.assertIn("mine-ice-sell", [rid for rid, _v, _d, _p in got["tests"]])                # nothing short: it is a test as before
        self.assertEqual(self.fill.sold({"kind": "circuit", "stops": [{"at": "a", "sell": [{"item": "armor_plate"}]}, {"at": "b", "sell": "all"}]}), ["armor_plate"])
        seen = self.fill.survey(str(self.root), str(self.data))
        seen["routes"]["freight"] = dict(seen["routes"]["freight"], stops=[{"at": "home:core:base", "sell": [{"item": "armor_plate", "min_price": 300}]}])
        seen["kept"] = {"armor_plate": 5931}
        got = self.fill.read_role(seen, "hauler")
        self.assertNotIn("freight", [rid for rid, _v, _p in got["paying"]])                      # a proven sale of a short item is not lent either
        self.assertIn("freight", [rid for _v, rid in got["closed"].get(self.fill.SALE_TRADES, [])])          # a sale circuit closes to a hauler first by P5; the reserve rule stands for the mine route above


class FallbackTests(Tree):
    """2026-11-17 03:09 UTC: 68 ships waited eight minutes for a hand: the three large home fields stood at their floors and two
    plans lacked the shared standing routes that had room."""

    def gather(self, **more):
        route = dict({"id": "gather", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "standing": True, "max_ships": 1,
                      "min_left": {"iron_ore": 99400}}, **more)
        (self.root / "routes" / "gather.json").write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        self.fill.routefiles.write_index(str(self.root))
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "a route")
        (self.data / "scouting").mkdir(exist_ok=True)
        self.field(100000)

    def field(self, remaining):
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (self.data / "scouting" / "far.json").write_text(json.dumps({"system": "far", "read_at": stamp, "pois": {"rocks": {"resources": [
            {"resource_id": "iron_ore", "remaining": remaining}]}}}))

    def test_a_role_whose_ships_wait_is_lent_standing_work_of_another_plan(self):
        self.gather(open_to=["hauler"])                                                          # rule F23: lent to haulers only by its file's word
        self.assertIn("committed", self.run_fill("zero", "add", "gather").stdout)                 # Mining's plan holds it; Logistics' does not
        seen, got = self.read("hauler", tests=0)
        self.assertEqual(len(got["idle"]), 2)                                                     # three wait, one is offered the paying route
        self.assertEqual(self.fill.borrow(seen, got, "hauler", 2), ["gather"])
        self.assertEqual(self.fill.borrow(seen, got, "hauler", 0), [])                            # nobody is left waiting: nothing is lent
        self.assertEqual(self.fill.borrow(seen, got, "miner", 2), [])                             # never a route of the role's own plan
        seen["routes"]["gather"] = dict(seen["routes"]["gather"], sell=[{"item": "iron_ore", "min_price": 1}])
        self.assertEqual(self.fill.borrow(seen, got, "hauler", 2), [])                            # a route that sells is its Admiral's to give
        seen, got = self.read("hauler", tests=0)
        chart = self.root / "map" / "galaxy.tsv"
        policed = chart.read_text(encoding="ascii")
        chart.write_text(policed.replace("far\tFar\t1\t0\tvoidborn", "far\tFar\t1\t0\t"), encoding="ascii")
        self.assertEqual(self.fill.borrow(seen, got, "hauler", 2), [])                            # beyond the border a plan is its Admiral's alone
        chart.write_text(policed, encoding="ascii")
        self.field(99400)                                                                         # the field at its floor carries nobody more
        seen, got = self.read("hauler", tests=0)
        self.assertEqual(self.fill.borrow(seen, got, "hauler", 2), [])

    def test_the_fallback_writes_the_plan_only_with_its_switch(self):
        self.gather(open_to=["hauler"])
        self.assertIn("committed", self.run_fill("zero", "add", "gather").stdout)
        done = self.run_fill("unity", "fill", "all", "--once", "--write")
        self.assertNotIn("lent", done.stdout)                                                     # the switch file is not there
        self.assertEqual(json.loads((self.root / "routes" / "plans" / "hauler.json").read_text())["routes"], ["once", "park"])
        (self.data / "fleet" / "fallback-on").write_text("")
        done = self.run_fill("unity", "fill", "all", "--once")
        self.assertIn("lent to the hauler plan's list Then", done.stdout, done.stdout)
        self.assertEqual(self.git("status", "--porcelain"), "")                                   # without --write nothing is written
        done = self.run_fill("unity", "fill", "all", "--once", "--write")
        self.assertIn("committed", done.stdout, done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "plans" / "hauler.json").read_text())["routes"], ["once", "gather", "park"])
        self.assertEqual((self.git("log", "-1", "--format=%an"), self.git("status", "--porcelain")), ("Unity\n", ""))
        self.assertNotIn("lent", self.run_fill("unity", "fill", "all", "--once", "--write").stdout)   # it is in the plan now: lent once

    def test_a_route_beyond_the_border_is_lifted_only_as_far_as_its_lift_to_says(self):
        self.gather(lift_to=2, open_to=["hauler"])
        self.assertIn("committed", self.run_fill("apollo", "add", "gather").stdout)
        seen, got = self.read("hauler")
        self.assertEqual(self.fill.spare(seen, got), [])                                          # requests ENT-216: lift_to waits for the first RESULT line
        for _ in range(3):                                                                        # rule F37: three results
            self.flown("gather")
        seen, got = self.read("hauler")
        chart = self.root / "map" / "galaxy.tsv"
        chart.write_text(chart.read_text(encoding="ascii").replace("far\tFar\t1\t0\tvoidborn", "far\tFar\t1\t0\t"), encoding="ascii")
        self.assertEqual(self.fill.spare(seen, got), [("gather", 1)])                             # its Admiral wrote 2: one place more, beyond the border too
        seen["routes"]["gather"] = dict(seen["routes"]["gather"], lift_to=1)
        self.assertEqual(self.fill.spare(seen, got), [])                                          # never past the Admiral's number
        seen["routes"]["gather"] = {k: v for k, v in seen["routes"]["gather"].items() if k != "lift_to"}
        self.assertEqual(self.fill.spare(seen, got), [])                                          # without it the limit stays its Admiral's (rule F13)

    def test_a_test_goes_to_a_ship_of_the_callers_own_roles_only(self):
        done = self.run_fill("unity", "fill", "all")                                              # the Fleet Admiral's job: no test on an Admiral's ship
        self.assertIn("hauler: 3 waiting, 0 on standing work; 1 paying routes and 0 tests to add: freight", done.stdout, done.stdout)
        self.assertIn("1 paying routes and 1 tests to add: freight, trade-x", self.run_fill("apollo", "fill").stdout)


class HeldBackTests(Tree):
    """requests ENT-233 (Trade): energy crystal and verdigris curd are held back whole for other recipes, yet the filler
    offered a test that sold crystals and a route crafted them into focused crystals for sale; requests ENT-236
    (Military): the filler put tests in front of five guard drones and a mine test on a drone, and two hunts Intel
    claims into the drone plan."""

    def test_a_good_held_back_and_a_craft_that_sells_it_are_not_added(self):
        crafted = {"id": "craft-focus", "kind": "circuit", "title": "t", "max_ships": 1, "measured": MEASURED(6400), "stops": [
            {"at": "home:core:base", "buy": [{"item": "palladium_ore", "qty": 1, "max_price": 450}],
             "craft": [{"recipe": "focus_energy_crystal", "runs": 1, "makes": "focused_crystal", "inputs": ["palladium_ore"]}]},
            {"at": "home:core:base", "sell": [{"item": "focused_crystal", "min_price": 700}]}]}
        (self.root / "routes" / "craft-focus.json").write_text(json.dumps(crafted, indent=1) + "\n", encoding="ascii")
        seen = self.fill.survey(str(self.root), str(self.data))
        seen["catalog"] = {"recipes": {"focus_energy_crystal": {"inputs": [{"item_id": "energy_crystal", "quantity": 4}, {"item_id": "palladium_ore", "quantity": 1}]}}}
        self.assertEqual(self.fill.crafted_for_sale(seen, crafted), ["energy_crystal"])               # what it buys itself is left out
        seen["kept"] = {"energy_crystal": 2763}                                                     # held back for circuit boards: no surplus unit
        self.assertEqual(self.fill.sells_short(seen, crafted), ["energy_crystal"])
        got = self.fill.read_role(seen, "hauler")
        self.assertNotIn("craft-focus", [rid for rid, _v, _p in got["paying"]])                  # a route that buys goes by hand only, as before
        stored = dict(crafted, stops=[{"at": "home:core:base", "craft": crafted["stops"][0]["craft"]}, crafted["stops"][1]])
        self.assertEqual(self.fill.sells_short(seen, stored), ["energy_crystal"])                # all four from storage: the same

    def test_the_reserve_reads_held_back_goods_as_kept(self):
        seen = {"data": str(self.data), "root": str(self.root)}
        import types
        fake = types.ModuleType("surplus")
        fake.surplus = lambda data, root: {"rows": [{"id": "energy_crystal", "short": 0, "reserved": 2763, "surplus": 0},
                                                    {"id": "iron_ore", "short": 60111, "reserved": 319659, "surplus": 0},
                                                    {"id": "crystal_melt", "short": 0, "reserved": 0, "surplus": 64},
                                                    {"id": "water_ice", "short": 0, "reserved": 0, "surplus": 0}]}
        sys.modules["surplus"] = fake
        self.addCleanup(sys.modules.pop, "surplus", None)
        self.assertEqual(self.fill.kept_items(seen), {"energy_crystal": 2763, "iron_ore": 60111})   # a good nobody keeps is free to sell

    def test_a_guard_ship_gets_no_test_and_a_drone_no_mine_test(self):
        guard = {"id": "post", "kind": "guard", "title": "t", "guards": "rays", "station": "home:core:base"}
        (self.root / "routes" / "post.json").write_text(json.dumps(guard, indent=1) + "\n", encoding="ascii")
        (self.data / "plans").mkdir(exist_ok=True)
        (self.data / "plans" / "assign.json").write_text(json.dumps({"pilots": {"drone-1": ["once", "post", "rays", "park"], "drone-2": ["once", "rays", "park"]}}))
        seen = self.fill.survey(str(self.root), str(self.data))
        seen["kept"] = {}
        self.assertTrue(self.fill.guard_ship(seen, "drone-1"))
        self.assertFalse(self.fill.guard_ship(seen, "drone-2"))
        got = self.fill.read_role(seen, "drone")
        given = [p for _rid, _v, pilots in got["paying"] for p in pilots] + [p for _rid, _v, _d, p in got["tests"]]
        self.assertNotIn("drone-1", given)                                                         # its post stays kept
        self.assertIn("mine-gas", [rid for _v, rid in got["closed"].get(GATHER, [])])
        self.assertNotIn("mine-gas", [rid for rid, _v, _d, _p in got["tests"]])
        _seen, hauler = self.read("hauler")
        self.assertIn("mine-gas", [rid for _v, rid in hauler["closed"].get(GATHER, [])])           # rule F23 (r21): a gas field is the miners' too

    def test_a_route_another_division_claimed_is_not_added(self):
        far = dict(ROUTES["freight"], id="far-freight")                                          # a route id holds a dash (comms.claimed_routes)
        (self.root / "routes" / "far-freight.json").write_text(json.dumps(far, indent=1) + "\n", encoding="ascii")
        stamp = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
        (self.top / "communications").mkdir()
        (self.top / "communications" / "admirals.log").write_text(
            "## [ENT-001] | %s UTC | Zero | claim | ref: game/routes/far-freight.json\nClaims: far-freight (1).\nWhy: a test.\n" % stamp, encoding="ascii")
        seen = self.fill.survey(str(self.root), str(self.data))
        seen["kept"] = {}
        self.assertEqual((self.fill.claims(seen), seen.get("claims_error")), ({"far-freight": "Zero"}, None))
        got = self.fill.read_role(seen, "hauler")
        self.assertIn("far-freight", [rid for _v, rid in got["closed"].get(self.fill.CLAIMED, [])])
        self.assertNotIn("far-freight", [rid for rid, _v, _p in got["paying"]])
        _seen, miner = self.read("miner")
        self.assertNotIn("far-freight", [rid for _v, rid in miner["closed"].get(self.fill.CLAIMED, [])])  # the claimer's own

    def test_a_claimed_hunt_that_gives_its_loot_stays_claimed_under_strict_classes(self):
        # errors.log ENT-131: with data/fleet/strict-classes-on a hunt with `gift_to` is standing work (routes.gives),
        # and claims() left standing work out of every claim, so the filler put two hunts Military claimed (admirals.log
        # ENT-088) into the command plan at 09:57 and again at 12:39 UTC. A claim names a herd: it holds for a hunt.
        hunt = {"id": "hunt-far-rays", "kind": "hunt", "title": "t", "max_ships": 1, "place": "home:core", "gift_to": "trader"}
        (self.root / "routes" / "hunt-far-rays.json").write_text(json.dumps(hunt, indent=1) + "\n", encoding="ascii")
        stamp = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
        (self.top / "communications").mkdir()
        (self.top / "communications" / "admirals.log").write_text(
            "## [ENT-001] | %s UTC | Apophis | claim | ref: game/routes/hunt-far-rays.json\nClaims: hunt-far-rays (1).\nWhy: a test.\n" % stamp, encoding="ascii")
        workclass = sys.modules["workclass"]
        old = workclass.STRICT
        workclass.STRICT = True
        self.addCleanup(setattr, workclass, "STRICT", old)
        seen = self.fill.survey(str(self.root), str(self.data))
        self.assertTrue(self.fill.routefiles.standing(hunt))                                   # strict classes: standing work
        self.assertEqual((self.fill.claims(seen), seen.get("claims_error")), ({"hunt-far-rays": "Apophis"}, None))


class HuntRuleTests(Tree):
    # Zero, report of 2026-11-16: the gate offered Intel's herd to a miner. Rule F16: Intel and Military hunt, Mining,
    # Trade and Logistics earn; rule F9: one hunter per herd.
    def put_route(self, route):
        (self.root / "routes" / (route["id"] + ".json")).write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")

    def add_role(self, role, owner, ship):
        (self.root / "routes" / "plans" / (role + ".json")).write_text(json.dumps({"role": role, "owner": owner, "note": "n", "routes": ["park"]}, indent=1) + "\n", encoding="ascii")
        fleet = json.loads((self.data / "fleet" / "fleet.json").read_text())
        fleet["ships"].append({"name": ship, "status": "connected", "activity": {"kind": "idle"}, "docked": True, "credits": 20000, "cargo_used": 0})
        (self.data / "fleet" / "fleet.json").write_text(json.dumps(fleet))
        (self.data / "fleet" / "ships" / (ship + ".json")).write_text(json.dumps({"modules": [], "cargo": []}))

    def test_a_hunt_outside_the_plan_is_offered_only_to_a_role_that_hunts(self):
        self.assertTrue(set(self.fill.HUNTERS) <= set(self.fill.division.ROLES))                 # every name in the list is a role of the fleet
        self.add_role("scout", "Oracle", "scout-1")
        self.add_role("trader", "Mercury", "trader-1")
        self.put_route({"id": "cull", "kind": "circuit", "title": "t", "max_ships": 1, "measured": MEASURED(2600),     # a circuit whose stop hunts is a hunt too
                        "stops": [{"at": "home:core:base", "hunt": [{"at": "home:nebula", "species": ["glow_ray"], "kills": 3}]}]})
        self.put_list(CANDIDATES + [{"id": "hunt-z", "kind": "hunt", "per_ship_hour": 950, "status": "new", "route_id": "",
                                     "route": {"id": "hunt-z", "kind": "hunt", "title": "t", "place": "far:cloud", "sell_at": "home:core:base", "max_ships": 1}}])
        got = {role: self.read(role)[1] for role in ("drone", "scout", "miner", "trader", "hauler")}
        hunts = lambda role: sorted([rid for rid, _v, _p in got[role]["paying"] if rid in ("cull", "herd2")] + [rid for rid, _v, _d, _p in got[role]["tests"] if rid == "hunt-z"])
        self.assertEqual({role: hunts(role) for role in got}, {"drone": ["cull"], "scout": ["cull"], "miner": [], "trader": [], "hauler": []})
        self.assertEqual(got["scout"]["paying"], [("cull", 2600, ["scout-1"])])                 # its one waiting ship takes the best hunt
        for role in ("miner", "trader", "hauler"):
            self.assertEqual(got[role]["closed"][self.fill.NO_HUNT], [(3000, "rays"), (2600, "cull"), (2000, "herd2"), (950, "hunt-z")], role)
            self.assertIn(("freight", 1500), [(rid, value) for rid, value, _p in got[role]["paying"]])      # paying work that is no hunt stays open
        for role in ("drone", "scout"):
            self.assertNotIn(self.fill.NO_HUNT, got[role]["closed"])
        done = self.run_fill("apollo", "status", "hauler")
        self.assertIn("a hunt: this role does not hunt (rule F16) 4 routes, up to 3,000: rays, cull, herd2 ...", done.stdout)

    def test_a_first_hunt_that_pays_once_stays_open_to_every_role(self):
        self.put_route({"id": "first-hunt", "kind": "circuit", "title": "t", "once": True, "measured": dict(MEASURED(400), credits_per_run=2500),
                        "stops": [{"at": "home:core:base", "accept": ["First Hunt"], "hunt": [{"at": "home:nebula", "species": ["glow_ray"], "kills": 1, "for": ["First Hunt"]}]},
                                  HOME]})
        _seen, got = self.read("miner")
        self.assertEqual(got["paying"], [("first-hunt", 2500, ["miner-2"])])
        self.assertEqual(got["closed"][self.fill.NO_HUNT], [(3000, "rays"), (2000, "herd2")])

    def test_a_hunt_an_admiral_put_into_its_own_plan_stays(self):
        (self.root / "routes" / "plans" / "miner.json").write_text(json.dumps({"role": "miner", "owner": "Zero", "note": "n", "routes": ["ice", "herd2", "park"]}, indent=1) + "\n",
                                                                   encoding="ascii")
        _seen, got = self.read("miner")
        self.assertEqual(got["starting"], [("miner-1", "ice"), ("miner-2", "herd2")])               # the dispatcher sends it
        self.assertEqual([rid for rid, _f, _c, _w, _h in got["plan"]], ["ice", "herd2", "park"])
        self.assertEqual(got["closed"].get(self.fill.NO_HUNT), [(3000, "rays")])                # the hunt outside the plan stays closed


class ClassRuleTests(Tree):
    """Rule F23, round r21 (Suggi, 2026-11-18: "Ore is miners job, its not something everyone does"): on 2026-11-17 the
    fallback lent the miners' iron routes to traders, haulers, drones and scouts, who gathered iron for one to two hours
    after the reserve's iron was met. The filler offers, lends and lifts a route only for a role of its class."""

    def gather(self, **more):
        route = dict({"id": "gather", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "standing": True, "max_ships": 1,
                      "min_left": {"iron_ore": 99400}}, **more)
        (self.root / "routes" / "gather.json").write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        self.fill.routefiles.write_index(str(self.root))
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "a route")
        (self.data / "scouting").mkdir(exist_ok=True)
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (self.data / "scouting" / "far.json").write_text(json.dumps({"system": "far", "read_at": stamp, "pois": {"rocks": {"resources": [
            {"resource_id": "iron_ore", "remaining": 100000}]}}}))

    def test_the_fallback_never_lends_a_gather_route_to_a_role_that_does_not_gather(self):
        self.gather()
        self.assertIn("committed", self.run_fill("zero", "add", "gather").stdout)                # Mining's standing work, with room
        seen, got = self.read("hauler", tests=0)
        self.assertEqual(len(got["idle"]), 2)
        self.assertEqual(self.fill.borrow(seen, got, "hauler", 2), [])                            # 2026-11-17: lent to every waiting role
        self.assertIn(GATHER, got["closed"])

    def test_a_gather_route_in_another_plan_is_lent_to_waiting_miners(self):
        self.gather()
        done = self.run_fill("apollo", "add", "gather")                                          # the Admiral's own word: added, with a note
        self.assertIn("committed", done.stdout)
        self.assertIn("note: gather is not hauler work (class: gather is miners' work): the dispatcher refuses it to the hauler ships while "
                      "data/fleet/class-guard-on exists", done.stdout)
        (self.root / "routes" / "freight.json").unlink()                                         # no paying work outside the plan
        seen, got = self.read("miner", tests=0)
        self.assertEqual(got["idle"], ["miner-2"])                                                # it lacks the ice harvester
        self.assertEqual(self.fill.borrow(seen, got, "miner", 1), ["gather"])

    def test_standing_work_of_another_class_is_not_lifted_for_the_waiting_ships(self):
        self.gather()
        self.assertIn("committed", self.run_fill("apollo", "add", "gather").stdout)
        for _ in range(3):                                                                        # rule F37: three results
            self.flown("gather")
        seen, got = self.read("hauler")
        self.assertEqual((len(got["starting"]), len(got["waiting"])), (1, 2))                     # the class guard is off: one hauler gathers
        self.assertEqual(self.fill.spare(seen, got), [])                                          # until 2026-11-18 lifted for the waiting haulers
        seen["routes"]["gather"] = dict(seen["routes"]["gather"], open_to=["hauler"])
        self.assertEqual(self.fill.spare(seen, got), [("gather", 1)])                             # its file's `open_to`: the Admiral's word



class StandingFallbackCliffTests(unittest.TestCase):
    def test_verdict_and_show_warn_when_once_only_ships_lack_standing_fallback(self):
        import io, contextlib, sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "game" / "fleet"))
        import fill as _fill
        seen = {"list_age": 10.0, "fleet_at": "2026-11-24T00:00:00Z", "told": set()}
        got = {"role": "hauler", "owner": "Apollo", "ships": 2, "work": ["hauler-1", "hauler-2"], "hand": [], "away": [],
               "starting": [], "waiting": [], "standing": [], "next": [], "park": [],
               "once_only": [("hauler-1", "nova_terra"), ("hauler-2", "nova_terra")],
               "idle": [], "plan": [], "paying": [], "tests": [], "closed": {}, "by_hand": [], "refused": []}
        ok, line = _fill.verdict(seen, got)
        self.assertTrue(ok)
        self.assertIn("CLIFF WARNING", line)
        self.assertIn("nova_terra 2", line)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _fill.show(seen, got)
        self.assertIn("CLIFF WARNING (2h idle risk): 2 ship(s)", buf.getvalue())
        # Cleared when once_only is empty
        got["once_only"] = []
        ok2, line2 = _fill.verdict(seen, got)
        self.assertTrue(ok2)
        self.assertNotIn("CLIFF WARNING", line2)

if __name__ == "__main__":
    unittest.main()
