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
MEASURED = lambda cph: {"date": "2026-11-15", "runs": 3, "minutes": 30, "credits_per_run": cph // 2, "cph_per_ship": cph}
ROUTES = {
    "park": {"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [HOME]},
    "once": {"id": "once", "kind": "circuit", "title": "t", "once": True, "stops": [HOME]},
    "rays": {"id": "rays", "kind": "hunt", "title": "t", "place": "home:nebula", "sell_at": "home:core:base", "max_ships": 1, "measured": MEASURED(3000)},
    "ice": {"id": "ice", "kind": "mine", "title": "t", "belt": "far:belt", "station": "home:core:base", "max_ships": 2, "requires": {"module": "ice_harvester"},
            "sell": [{"item": "water_ice", "min_price": 20}], "measured": MEASURED(5000)},
    "herd2": {"id": "herd2", "kind": "hunt", "title": "t", "place": "far:cloud", "sell_at": "home:core:base", "max_ships": 1, "measured": MEASURED(2000)},
    "bad": {"id": "bad", "kind": "hunt", "title": "t", "place": "far:rift", "sell_at": "home:core:base", "measured": MEASURED(-300)},
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

    def run_fill(self, member, *args):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HERMES_SESSION_PROFILE": member, "HOME": self.temp.name, "FLEET_TAXES": os.devnull}
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

    def test_work_outside_the_plan_is_offered_once_and_what_closes_the_rest_is_named(self):
        _seen, got = self.read("hauler")
        self.assertEqual(got["waiting"], ["hauler-1", "hauler-2", "hauler-3"])
        self.assertEqual(got["paying"], [("herd2", 2000, ["hauler-1"])])                          # one place: one pilot
        self.assertEqual([(rid, value, pilot) for rid, value, _draft, pilot in got["tests"]], [("trade-x", 900, "hauler-2")])
        self.assertEqual(got["idle"], ["hauler-3"])
        self.assertEqual(got["closed"], {"needs ice_harvester": [(5000, "ice")], "max_ships 1 reached": [(3000, "rays")],    # a drone starts on `rays` at the next pass
                                         "needs gas_harvester": [(800, "mine-gas")]})             # never `bad`, `craft-y`, `trade-low`
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
        once = dict(ROUTES["herd2"], measured=dict(MEASURED(2000), runs=1))
        (self.root / "routes" / "herd2.json").write_text(json.dumps(once, indent=1) + "\n", encoding="ascii")
        _seen, got = self.read("hauler")
        self.assertEqual(got["paying"], [])                                                       # measured on one run: not yet a route that pays
        (self.root / "routes" / "herd2.json").write_text(json.dumps(ROUTES["herd2"], indent=1) + "\n", encoding="ascii")
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - ago))
        with open(self.data / "routes" / "runs.jsonl", "a") as handle:
            for ago, delta in ((900, 105), (300, -4635)):
                handle.write(json.dumps({"route": "herd2", "pilot": "drone-9", "minutes": 10, "started": stamp(ago), "credits_before": 9000, "credits_after": 9000 + delta}) + "\n")
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

    def test_the_gate_passes_only_on_a_fresh_list(self):
        for path in (self.root / "routes").glob("herd2.json"):
            path.unlink()
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
        self.assertIn("hauler: 3 waiting, 0 on standing work; 1 paying routes and 1 tests to add: herd2, trade-x", done.stdout)
        self.assertIn("not written: add --write", done.stdout)
        self.assertEqual(self.git("status", "--porcelain"), "")
        done = self.run_fill("apollo", "fill", "--write")
        self.assertIn("committed", done.stdout, done.stdout)
        plan = json.loads((self.root / "routes" / "plans" / "hauler.json").read_text())
        self.assertEqual(plan["routes"], ["once", "trade-x", "herd2", "park"])                    # the role's routes in one order, from the division's plan file
        self.assertEqual((plan["ships"], plan["of"]), ({"once": 3, "trade-x": 1, "herd2": 1, "park": 3}, 3))
        lists = json.loads((self.data / "plans" / "assign.json").read_text())["pilots"]          # each a ship's own route: the paying one to the ship it was open to
        self.assertEqual(sorted(lists.values()), [["once", "herd2", "park"], ["once", "park"], ["once", "trade-x", "park"]])
        test = json.loads((self.root / "routes" / "trade-x.json").read_text())
        self.assertEqual((test["max_ships"], "Added as a test by fill.py" in test["note"]), (1, True))
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.git("log", "-1", "--format=%an"), "Apollo\n")
        self.assertEqual(sorted(self.git("show", "--name-only", "--format=", "HEAD").split()),
                         ["game/routes/index.md", "game/routes/master-index.md", "game/routes/plan.md", "game/routes/plans/hauler.json", "game/routes/trade-x.json"])
        done = self.run_fill("apollo", "check")                                                   # the dispatcher would start two; the third has nothing open
        self.assertEqual((done.returncode, done.stdout.startswith("HALT: 1 ships of hauler wait and nothing that pays is open to them")), (1, True))

    def commit_route(self, route):
        (self.root / "routes" / (route["id"] + ".json")).write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        self.fill.routefiles.write_index(str(self.root))
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "a route")

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
        self.assertEqual(sorted(ids.index("gather") > ids.index(rid) for ids in lists.values() for rid in ("herd2", "trade-x") if rid in ids), [True, True])   # before its standing work
        self.assertEqual(self.run_fill("apollo", "check").stdout, "PASS: no ship of hauler waits\n")

    def test_the_once_pass_adds_only_missions_that_pay_once_behind_the_once_line(self):
        # requests ENT-144: a new once route reached a plan only at its Admiral's next turn, hours later
        self.commit_route(dict(ROUTES["once"], id="board", measured=MEASURED(6000)))
        done = self.run_fill("unity", "fill", "all", "--once", "--write")
        self.assertIn("committed", done.stdout, done.stdout)
        plans = {role: json.loads((self.root / "routes" / "plans" / (role + ".json")).read_text())["routes"] for role in PLANS}
        self.assertEqual(plans, {"drone": ["once", "board", "rays", "park"], "hauler": ["once", "board", "park"], "miner": ["board", "ice", "park"]})   # herd2 repeats, trade-x is a test: both stay out
        self.assertEqual((self.git("log", "-1", "--format=%an"), self.git("status", "--porcelain")), ("Unity\n", ""))
        self.assertIn("nothing to add", self.run_fill("unity", "fill", "all", "--once", "--write").stdout)

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
        self.assertIn("committed", self.run_fill("apophis", "add", "herd2").stdout)
        self.assertEqual(json.loads((self.root / "routes" / "plans" / "drone.json").read_text())["routes"], ["once", "rays", "herd2", "park"])     # into the list Then
        self.assertIn("committed", self.run_fill("apophis", "lift", "herd2", "3").stdout)
        self.assertEqual(json.loads((self.root / "routes" / "herd2.json").read_text())["max_ships"], 3)
        self.assertIn("REFUSED: ice stands in no plan of yours", self.run_fill("apophis", "lift", "ice", "9").stdout)
        done = self.run_fill("zero", "lift", "ice", "30")                                         # Suggi, 2026-11-16: read what a route carries before lifting it
        self.assertEqual((done.returncode, "REFUSED: ice carries about 20 ships, not 30" in done.stdout), (1, True), done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "ice.json").read_text())["max_ships"], 2)
        self.assertIn("committed", self.run_fill("zero", "lift", "ice", "20").stdout)
        self.assertIn("committed", self.run_fill("apophis", "drop", "herd2").stdout)
        done = self.run_fill("apophis", "drop", "park")                                           # a plan must end with a route that is always open
        self.assertEqual((done.returncode, "HALT military: nothing changed; the plan applied last stays in force" in done.stdout), (1, True), done.stdout)
        self.assertEqual(json.loads((self.root / "routes" / "plans" / "drone.json").read_text())["routes"], ["once", "rays", "park"])
        self.assertEqual(self.git("status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
