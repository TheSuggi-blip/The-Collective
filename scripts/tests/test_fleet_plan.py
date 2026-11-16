"""game/fleet/plan.py on a disposable repository and data folder: a division's plan file, its check, what it writes and
how the dispatcher flies by it. No engine, no network."""

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
MEASURED = {"date": "2026-11-15", "runs": 3, "minutes": 30, "credits_per_run": 1500, "cph_per_ship": 3000}
ROUTES = {
    "park": {"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [HOME]},
    "board": {"id": "board", "kind": "circuit", "title": "t", "once": True, "stops": [HOME]},
    "fit": {"id": "fit", "kind": "circuit", "title": "t", "stops": [dict(HOME, fit={"module": "ice_harvester"})]},
    "ice-a": {"id": "ice-a", "kind": "mine", "title": "t", "belt": "far:a", "station": "home:core:base", "max_ships": 3, "sell": [{"item": "ice", "min_price": 1}], "measured": MEASURED},
    "ice-b": {"id": "ice-b", "kind": "mine", "title": "t", "belt": "far:b", "station": "home:core:base", "max_ships": 3, "sell": [{"item": "ice", "min_price": 1}], "measured": MEASURED},
    "gather": {"id": "gather", "kind": "mine", "title": "t", "belt": "far:c", "station": "home:core:base", "standing": True, "max_ships": 40},
    "census": {"id": "census", "kind": "census", "title": "t", "systems": ["far"]},
    "guard": {"id": "guard", "kind": "circuit", "title": "t", "max_ships": 2, "measured": MEASURED, "stops": [HOME]},
}
PLANS = {"miner": ("Zero", ["board", "fit", "ice-a", "ice-b", "gather", "census", "park"]),
         "command": ("Unity", ["board", "guard", "gather", "park"]), "sentinel": ("Unity", ["board", "ice-a", "gather", "park"])}
SHIPS = ["miner-%d" % n for n in range(1, 7)] + ["sentinel-1", "sentinel-2", "Prime Directive"]


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_beside_plan", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-plan-test-")
        self.addCleanup(self.temp.cleanup)
        self.top, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        self.root = self.top / "game"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.data / "fleet" / "orders", self.data / "fleet" / "ships", self.data / "routes"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nid\tname\tx\ty\tempire\tflags\tjumps_from_home\tlanes\nhome\tHome\t0\t0\tvoidborn\t-\t0\tfar\n"
                                                      "far\tFar\t1\t0\tvoidborn\t-\t1\thome\n", encoding="ascii")
        for rid, route in ROUTES.items():
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route, indent=1) + "\n", encoding="ascii")
        for role, (owner, ids) in PLANS.items():
            (self.root / "routes" / "plans" / (role + ".json")).write_text(json.dumps({"role": role, "owner": owner, "note": "n", "routes": ids,
                                                                                       "planned": [{"what": "a test at far", "when": "next turn"}] if role == "miner" else []},
                                                                                      indent=1) + "\n", encoding="ascii")
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({"Prime Directive": {"admiral": "Unity", "division": "Command", "role": "command"}}))
        ships = [{"name": name, "number": n, "class": "Threshold", "status": "connected", "activity": {"kind": "idle"}, "docked": True, "credits": 20000, "cargo_used": 0}
                 for n, name in enumerate(SHIPS, 1)]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"updated_at": "now", "ships": ships}))
        for name in SHIPS:
            (self.data / "fleet" / "ships" / (name.replace(" ", "_") + ".json")).write_text(json.dumps({"modules": [], "cargo": [], "skills": {"piloting": {"level": 4}, "mining": 2}}))
        (self.data / "routes" / "runs.jsonl").write_text("")
        self.plan = load("plan")
        self.plan.dispatch.load_routes  # the module is loaded
        load("routes").write_index(str(self.root))
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "start")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.top)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout

    def run_plan(self, member, *args):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": self.temp.name, "FLEET_TAXES": os.devnull}
        if member:
            env["HERMES_SESSION_PROFILE"] = member
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "plan.py")] + list(args) + ["--root", str(self.root), "--data", str(self.data)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)

    def file(self, name):
        return self.data / "plans" / ("plan-%s.md" % name)

    def assign(self):
        return json.loads((self.data / "plans" / "assign.json").read_text())

    def role(self, role):
        return json.loads((self.root / "routes" / "plans" / (role + ".json")).read_text())


class PlanTests(Tree):
    def test_the_first_apply_writes_the_file_from_the_plan_in_force_and_no_ship_changes_its_work(self):
        done = self.run_plan("zero", "show", "--brief")
        self.assertIn("no plan file yet: the ships fly the role's plan in force", done.stdout)
        done = self.run_plan("zero", "apply")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("mining: applied | 6 ships, 0 with routes of their own | First 2, Then 5", done.stdout)
        self.assertEqual(self.git("status", "--porcelain"), "")                                 # the role's file only gained what the script writes, committed
        self.assertEqual(self.role("miner")["routes"], PLANS["miner"][1])
        self.assertEqual((self.role("miner")["ships"]["ice-a"], self.role("miner")["of"]), (6, 6))
        self.assertEqual(self.assign()["pilots"]["miner-3"], PLANS["miner"][1])                  # what the dispatcher flew before, route for route
        text = self.file("mining").read_text()
        for part in ("## First, for Every Ship\n\n1. board\n2. fit\n", "| miner-1 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | -- |",
                     "## Then, for Every Ship\n\n1. ice-a\n2. ice-b\n3. gather\n4. census\n5. park\n", "## Planned", "- a test at far | next turn"):
            self.assertIn(part, text)
        self.assertEqual(self.run_plan("zero", "check").stdout.split(":")[0], "PASS mining")
        self.assertIn("mining: unchanged", self.run_plan("zero", "apply").stdout)               # nothing new: nothing applied twice

    def test_a_division_of_two_roles_keeps_what_differs_as_each_ships_own_routes(self):
        self.assertEqual(self.run_plan("unity", "apply", "command").returncode, 0)
        lists = self.assign()["pilots"]
        self.assertEqual((lists["Prime Directive"], lists["sentinel-1"]), (PLANS["command"][1], PLANS["sentinel"][1]))
        self.assertIn("| sentinel-2 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | ice-a |", self.file("command").read_text())

    def test_each_ship_flies_its_own_routes_and_the_dispatcher_follows_the_file(self):
        self.run_plan("zero", "apply")
        done = self.run_plan("zero", "set", "miner-1..3", "ice-b,gather")
        self.assertEqual(done.returncode, 0, done.stdout)
        done = self.run_plan("zero", "set", "miner-4..6", "ice-a")
        self.assertIn("mining: applied", done.stdout)                                            # the role's routes and counts stay: nothing to commit
        self.assertEqual(self.git("log", "-1", "--format=%an"), "Zero\n")
        self.assertEqual(self.assign()["pilots"]["miner-2"], ["board", "fit", "ice-b", "gather", "ice-a", "census", "park"])
        self.assertEqual(self.role("miner")["ships"], {"board": 6, "fit": 6, "ice-b": 6, "gather": 6, "ice-a": 6, "census": 6, "park": 6})
        self.run_plan("zero", "then", "census,park")                                             # the shared routes out of Then: each ship only its own
        lists = self.assign()["pilots"]
        self.assertEqual((lists["miner-1"], lists["miner-5"]), (["board", "fit", "ice-b", "gather", "census", "park"], ["board", "fit", "ice-a", "census", "park"]))
        self.assertEqual(self.role("miner")["ships"]["ice-a"], 3)
        dispatch = load("dispatch")
        plan = {"roles": {"miner": self.role("miner")["routes"]}, "pilots": dispatch.own_lists(str(self.data))}
        state = {"now": time.time(), "data": str(self.data), "rows": [], "orders": {}, "rest": {}, "booked": {"miner-1": {"board"}, "miner-5": {"board"}, "miner-9": {"board"}},
                 "loss": {}, "late": {}}
        routes = dispatch.load_routes(str(self.root))
        pilot = lambda name: {"name": name, "role": "miner", "credits": 20000, "docked": True, "modules": [], "skills": {}, "goods": 0}
        routes["board"]["skip_if_booked"] = ["board"]
        routes["fit"]["status"] = "off"
        self.assertEqual(dispatch.pick(pilot("miner-1"), plan, routes, state)[0]["id"], "ice-b")
        self.assertEqual(dispatch.pick(pilot("miner-5"), plan, routes, state)[0]["id"], "ice-a")
        self.assertEqual(dispatch.pick(pilot("miner-9"), plan, routes, state)[0]["id"], "ice-a")      # a ship the file does not name flies the role's list

    def test_a_plan_that_fails_the_check_changes_nothing_and_the_last_one_stays_in_force(self):
        self.run_plan("zero", "apply")
        before = (self.assign(), self.file("mining").read_text(), self.git("rev-parse", "HEAD"))
        for args, says in ((("set", "miner-1", "ice-x"), "the row of miner-1: no route file game/routes/ice-x.json"),
                           (("then", "gather"), "the list Then must end with a route that is always open (the `park` route): `gather` is not (max_ships)"),
                           (("then", "none"), "the list Then is empty")):
            done = self.run_plan("zero", *args)
            self.assertEqual((done.returncode, says in done.stdout, "HALT mining: nothing changed" in done.stdout), (1, True, True), done.stdout)
        self.assertEqual((self.assign(), self.file("mining").read_text(), self.git("rev-parse", "HEAD")), before)
        text = self.file("mining").read_text().replace("| miner-2 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | -- |", "| miner-2 | x | x | x | x | x | x | x | ice-a > nowhere |")
        self.file("mining").write_text(text + "\n## Odd Section\n")                             # an Admiral's edit by hand that fails twice
        done = self.run_plan("zero", "check")
        self.assertEqual((done.returncode, "HALT mining: the file fails the check" in done.stdout), (1, True))
        self.assertIn("no route file game/routes/nowhere.json", done.stdout)
        done = self.run_plan("zero", "apply")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(self.assign(), before[0])
        self.assertEqual(self.file("mining").read_text(), text + "\n## Odd Section\n")          # left for the Admiral to mend, never overwritten

    def test_an_edit_by_hand_is_applied_with_its_notes_and_the_levels_are_the_scripts(self):
        self.run_plan("zero", "apply")
        text = self.file("mining").read_text().replace("| miner-2 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | -- |", "| miner-2 | x | 9 | 9 | 9 | 9 | 9 | 9 | ice-b > gather |")
        text = text.replace("## Notes\n\nNone.", "## Notes\n\nIce at far:b is for the two best miners.")
        self.file("mining").write_text(text)
        self.assertIn("HALT mining: changed since it was applied", self.run_plan("zero", "check").stdout)
        self.assertIn("mining: applied", self.run_plan("zero", "apply").stdout)
        new = self.file("mining").read_text()
        self.assertIn("| miner-2 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | ice-b > gather |", new)  # the levels read again; the routes kept
        self.assertIn("Ice at far:b is for the two best miners.", new)
        self.assertEqual(self.assign()["pilots"]["miner-2"][:4], ["board", "fit", "ice-b", "gather"])
        self.assertEqual(len(list((self.data / "plans" / "history").glob("plan-mining.*.md"))), 2)

    def test_a_member_changes_its_own_division_only(self):
        self.assertIn("REFUSED: the plan of the command division is kept by Unity", self.run_plan("zero", "apply", "command").stdout)
        self.assertIn("REFUSED: this shell is no member", self.run_plan(None, "apply").stdout)
        self.assertEqual(self.run_plan("unity", "apply", "mining").returncode, 0)                 # the Fleet Admiral may
        self.assertEqual(self.run_plan(None, "show", "mining", "--brief").returncode, 0)          # reading is free
        self.assertIn("REFUSED: no ship of the mining division: sentinel-1", self.run_plan("zero", "set", "sentinel-1", "ice-a").stdout)

    def test_a_new_ship_gets_a_row_with_the_routes_most_of_its_role_have(self):
        self.run_plan("zero", "apply")
        self.run_plan("zero", "set", "miner-1..5", "ice-a")
        fleet = json.loads((self.data / "fleet" / "fleet.json").read_text())
        fleet["ships"].append({"name": "miner-7", "number": 70, "class": "Threshold", "status": "connected", "activity": {"kind": "idle"}, "docked": True, "credits": 1})
        (self.data / "fleet" / "fleet.json").write_text(json.dumps(fleet))
        self.assertIn("1 ships have no row yet (miner-7)", self.run_plan("zero", "show", "--brief").stdout)
        self.run_plan("zero", "apply")
        self.assertEqual(self.assign()["pilots"]["miner-7"][2], "ice-a")


if __name__ == "__main__":
    unittest.main()
