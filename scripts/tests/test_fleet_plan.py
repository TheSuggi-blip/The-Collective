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
         "command": ("Unity", ["board", "guard", "gather", "park"]), "sentinel": ("Apophis", ["board", "ice-a", "gather", "park"])}
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
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": self.temp.name, "FLEET_TAXES": os.devnull, "FLEET_COMMIT_WAIT": "0"}
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

    def kit(self, name="mining"):
        path = self.root / "routes" / "templates" / (name + ".json")
        return json.loads(path.read_text())["templates"] if path.is_file() else None

    def still(self):
        """What a refused change must leave as it was: the dispatcher's lists, the plan file, the commit, the folder."""
        return (self.assign(), self.file("mining").read_text(), self.git("rev-parse", "HEAD"), self.git("status", "--porcelain"), self.kit())


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
        # the sentinels are lent to Military (DECISIONS D226): its division holds the roles drone and sentinel
        self.assertEqual(self.run_plan("unity", "apply", "command").returncode, 0)
        self.assertEqual(self.run_plan("unity", "apply", "military").returncode, 0)
        lists = self.assign()["pilots"]
        self.assertEqual((lists["Prime Directive"], lists["sentinel-1"]), (PLANS["command"][1], PLANS["sentinel"][1]))
        self.assertIn("| sentinel-2 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | -- |", self.file("military").read_text())   # its role's list became First and Then
        self.assertNotIn("sentinel-2", self.file("command").read_text())

    def test_a_plan_is_flown_at_once_and_its_copy_in_the_repository_follows_when_the_folder_is_free(self):
        self.run_plan("zero", "apply")
        (self.root / "routes" / "ice-b.json").write_text(json.dumps(dict(ROUTES["ice-b"], title="another member's change, not committed"), indent=1) + "\n", encoding="ascii")
        done = self.run_plan("zero", "set", "miner-1..3", "ice-b,gather")
        self.assertEqual(done.returncode, 0, done.stdout)                                        # the turn of 2026-11-16 18:23 UTC: this was REFUSED, and a run ended on it
        self.assertIn("mining: applied", done.stdout)
        self.assertIn("note: the ships fly by the plan as applied; its copy in the repository", done.stdout)
        self.assertNotIn("REFUSED", done.stdout)
        self.assertEqual(self.assign()["pilots"]["miner-2"][:4], ["board", "fit", "ice-b", "gather"])      # the dispatcher flies the new plan
        self.assertEqual(self.role("miner")["routes"], PLANS["miner"][1])                         # the repository's copy: as it was committed
        self.assertEqual(self.git("status", "--porcelain").split(), ["M", "game/routes/ice-b.json"])      # nothing of ours left behind, nothing of theirs touched
        self.assertEqual(self.run_plan("zero", "check").stdout.split(":")[0], "PASS mining")
        self.git("checkout", "--", ".")                                                          # the other member commits its file or takes it back
        done = self.run_plan("unity", "apply", "all", "--quiet")                                  # the five-minute job
        self.assertIn("committed", done.stdout, done.stdout)
        self.assertEqual((self.role("miner")["routes"][:4], self.git("status", "--porcelain")), (["board", "fit", "ice-b", "gather"], ""))
        self.assertEqual(self.assign()["pilots"]["miner-2"][:4], ["board", "fit", "ice-b", "gather"])

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


class AwayTests(Tree):
    """2026-11-22 23:33 UTC: the engine signed 17 scouts out (fleet.json `away`); every plan change of their division
    then failed on their rows ("no ship of the intel division has this name") and would have dropped them on write."""

    def test_a_ship_the_engine_holds_away_keeps_its_row_and_the_plan_still_changes(self):
        self.run_plan("zero", "apply")
        self.run_plan("zero", "set", "miner-6", "ice-a")
        fleet = json.loads((self.data / "fleet" / "fleet.json").read_text())
        fleet["ships"] = [ship for ship in fleet["ships"] if ship["name"] != "miner-6"]
        fleet["away"] = [{"division": "Mining", "name": "miner-6"}, {"division": "Military", "name": "sentinel-9"}]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps(fleet))
        out = self.run_plan("zero", "set", "miner-1", "gather")
        self.assertEqual(out.returncode, 0, out.stdout)
        text = self.file("mining").read_text()
        self.assertIn("| miner-6 |", text)
        self.assertEqual(self.assign()["pilots"]["miner-6"][2], "ice-a")
        self.assertNotIn("sentinel-9", text)


class FreePartTests(Tree):
    """Requests ENT-263 (Oracle): Planned and Notes are written by the script like every other part, never by hand; a
    `## ` heading twice at a line start fails the check (three plan files carried every heading twice on 2026-11-17)."""

    def setUp(self):
        super().setUp()
        self.run_plan("zero", "apply")

    def test_planned_and_notes_are_written_by_script_with_the_same_commit_and_permission_rules(self):
        done = self.run_plan("zero", "planned", "a test of ice-b at far", "--when", "next turn")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("- a test at far | next turn\n- a test of ice-b at far | next turn\n", self.file("mining").read_text())
        self.assertEqual(self.role("miner")["planned"][-1], {"what": "a test of ice-b at far", "when": "next turn"})     # every member reads it
        self.assertEqual((self.git("log", "-1", "--format=%an %s"), self.git("status", "--porcelain")),
                         ("Zero mining plan: Planned + one line (plan.py, Zero)\n", ""))
        done = self.run_plan("zero", "planned", "--clear", "gather", "far", "first", "--when", "today")      # replace the list by one line
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(self.role("miner")["planned"], [{"what": "gather far first", "when": "today"}])
        self.run_plan("zero", "planned", "--clear")
        self.assertEqual(self.role("miner")["planned"], [])
        self.assertIn("## Planned\n\nWhat you mean", self.file("mining").read_text())
        self.assertIn("plan.py planned`). Every\nmember reads it in `game/routes/plan-<role>.md`: it names no ship of ours.\n\nNone.\n", self.file("mining").read_text())
        before = self.git("rev-parse", "HEAD")
        self.assertEqual(self.run_plan("zero", "note", "ice", "at", "far:b", "is", "for", "the", "best").returncode, 0)
        self.run_plan("zero", "note", "the second line")
        notes = self.file("mining").read_text().split("## Notes\n\n")[1]
        lines = notes.strip().split("\n")
        self.assertEqual(len(lines), 2, notes)
        self.assertRegex(lines[0], r"^- \d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC: ice at far:b is for the best$")
        self.assertTrue(lines[1].endswith(" UTC: the second line"))
        self.assertEqual(self.git("rev-parse", "HEAD"), before)                                  # Notes stay in the data folder: nothing to commit
        self.run_plan("zero", "note", "--clear")
        self.assertTrue(self.file("mining").read_text().endswith("## Notes\n\nNone.\n"))
        self.assertEqual(self.run_plan("zero", "check").stdout.split(":")[0], "PASS mining")

    def test_a_free_part_is_refused_to_another_member_to_a_pilots_name_and_to_more_than_one_line_of_ascii(self):
        before = self.still()
        for member, args, says in (("oracle", ("planned", "x", "--division", "mining"), "REFUSED: the plan of the mining division is kept by Zero"),
                                   ("oracle", ("note", "x", "--division", "mining"), "REFUSED: the plan of the mining division is kept by Zero"),
                                   (None, ("note", "x"), "REFUSED: this shell is no member"),
                                   ("zero", ("planned", "miner-3 first"), "it names no pilot of ours (miner-3)"),
                                   ("zero", ("note", "ice " + chr(0xe9)), "one line of ASCII"),
                                   ("zero", ("planned", "y" * 501), "500 characters at most")):
            done = self.run_plan(member, *args)
            self.assertIn(says, done.stdout, args)
            self.assertNotEqual(done.returncode, 0)
        self.assertEqual(self.still(), before)

    def test_a_heading_twice_at_a_line_start_halts_the_check_and_note_clear_mends_it(self):
        text = self.file("mining").read_text()
        doubled = text.replace("## Notes\n\nNone.", "## Notes\n\n" + text)       # the hand edit of 2026-11-17: the whole file again under Notes
        self.file("mining").write_text(doubled)
        done = self.run_plan("zero", "check")
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("HALT mining: the file fails the check", done.stdout)
        self.assertIn("the heading `## First, for Every Ship` stands twice at a line start (first at line 12)", done.stdout)
        before = (self.assign(), self.git("rev-parse", "HEAD"))
        done = self.run_plan("zero", "apply")
        self.assertEqual((done.returncode, self.file("mining").read_text(), (self.assign(), self.git("rev-parse", "HEAD"))), (1, doubled, before))
        done = self.run_plan("zero", "note", "an extra line")                                   # still a copy under Notes: refused
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("stands twice at a line start", done.stdout)
        self.assertEqual(self.file("mining").read_text(), doubled)
        done = self.run_plan("zero", "note", "--clear")
        self.assertEqual(done.returncode, 0, done.stdout)
        mended = self.file("mining").read_text()
        self.assertEqual([line for line in mended.split("\n") if line.startswith("## ")],
                         ["## First, for Every Ship", "## Ships", "## Then, for Every Ship", "## Planned", "## Notes"])
        self.assertEqual(self.run_plan("zero", "check").stdout.split(":")[0], "PASS mining")
        self.assertEqual(self.plan.twice("## Notes\n`## Notes` in a line\n## notes \n"), [
            "line 3: the heading `## notes` stands twice at a line start (first at line 1): a copy of the file stands in it; "
            "`plan.py note --clear` empties Notes, where such a copy lies"])                    # a heading at a line start only, case and spaces aside


class TemplateTests(Tree):
    """Templates: a division's named lists of routes (game/routes/templates/<division>.json), named in a ship's own
    routes as `@<name>` (Suggi, 2026-11-16: ships switched between kinds of work, preconfigured)."""

    def setUp(self):
        super().setUp()
        self.run_plan("zero", "apply")

    def test_a_template_expands_in_order_and_without_a_route_twice(self):
        plan = {"first": ["board"], "then": ["x", "park"], "ships": {"s": ["@a", "x", "@b"], "t": ["@b"]},
                "templates": {"a": {"routes": ["r1", "r2"]}, "b": {"routes": ["r2", "r3", "x"]}}}
        self.assertEqual(self.plan.expand(plan, "s"), ["r1", "r2", "x", "r3"])                  # each in its order; a route twice at its first place
        self.assertEqual(self.plan.effective(plan, "s"), ["board", "r1", "r2", "x", "r3", "park"])
        self.assertEqual(self.plan.effective(plan, "t"), ["board", "r2", "r3", "x", "park"])
        done = self.run_plan("zero", "template", "ice-loop", "ice-b,gather,ice-b", "--title", "Ice for the near bids", "--trains", "mining")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(self.kit(), {"ice-loop": {"title": "Ice for the near bids", "routes": ["ice-b", "gather"], "trains": ["mining"]}})
        self.assertIn("1 templates no ship uses: @ice-loop", done.stdout)                         # a note, not a HALT
        done = self.run_plan("zero", "use", "miner-1..2", "ice-loop")
        self.assertEqual(done.returncode, 0, done.stdout)
        lists = self.assign()["pilots"]
        self.assertEqual(lists["miner-1"], ["board", "fit", "ice-b", "gather", "ice-a", "census", "park"])     # First, the template, Then without its twins
        self.assertEqual(lists["miner-3"], PLANS["miner"][1])                                    # a ship that names none flies on as before
        self.assertIn("| miner-1 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | @ice-loop |", self.file("mining").read_text())   # the cell keeps the word as written

    def test_a_cell_mixes_templates_and_route_ids_in_any_order(self):
        self.run_plan("zero", "template", "ice-loop", "ice-b,gather")
        self.run_plan("zero", "template", "far-ice", "ice-a")
        done = self.run_plan("zero", "set", "miner-3,miner-4", "@ice-loop,census,@far-ice")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(self.assign()["pilots"]["miner-3"], ["board", "fit", "ice-b", "gather", "census", "ice-a", "park"])
        self.assertIn("| miner-3 | Threshold | 4 | 2 | 0 | 0 | 0 | 0 | @ice-loop > census > @far-ice |", self.file("mining").read_text())
        self.assertEqual(self.role("miner")["templates"], {"ice-loop": 2, "far-ice": 2})          # counts of the role's ships, never names
        brief = self.run_plan("zero", "show", "--brief").stdout
        self.assertIn(" 2 ships (miner-3, miner-4): @ice-loop > census > @far-ice", brief)       # grouped by the cell as written
        self.assertIn("@ice-loop: ice-b > gather", brief)
        self.assertEqual(self.run_plan("zero", "check").stdout.split(":")[0], "PASS mining")
        listed = self.run_plan(None, "templates", "mining").stdout                                # reading is free
        self.assertIn("TEMPLATES | mining (Zero) | game/routes/templates/mining.json | 2 templates, 2 ships on them", listed)
        self.assertIn("  @ice-loop -- no title | trains -- | 2 ships\n      ice-b > gather", listed)

    def test_a_template_change_is_one_commit_and_moves_every_ship_that_names_it_at_once(self):
        self.run_plan("zero", "template", "ice-loop", "ice-b,gather", "--note", "the near bids")
        self.assertEqual(self.git("log", "-1", "--format=%an %s"), "Zero mining templates: @ice-loop made: ice-b > gather (plan.py, Zero)\n")
        self.assertIn("game/routes/templates/mining.json", self.git("show", "--name-only", "--format=", "HEAD"))
        self.assertIn("game/routes/templates-mining.md", self.git("show", "--name-only", "--format=", "HEAD"))     # its page in the same commit
        self.run_plan("zero", "use", "miner-1..3", "@ice-loop")
        self.assertEqual(self.role("miner")["templates"], {"ice-loop": 3})
        self.assertEqual(self.git("log", "-1", "--format=%an %s"), "Zero mining plan: 3 ships fly @ice-loop (plan.py, Zero)\n")
        done = self.run_plan("zero", "template", "ice-loop", "gather,ice-a", "--title", "Gather first")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("mining: applied", done.stdout)                                            # the same call applies the plan again
        lists = self.assign()["pilots"]
        self.assertEqual([lists["miner-%d" % n][2:4] for n in (1, 2, 3)], [["gather", "ice-a"]] * 3)
        self.assertEqual(lists["miner-4"], PLANS["miner"][1])
        self.assertEqual(self.kit()["ice-loop"], {"title": "Gather first", "routes": ["gather", "ice-a"], "note": "the near bids"})   # the note kept
        self.assertEqual((self.git("status", "--porcelain"), self.run_plan("zero", "check").stdout.split(":")[0]), ("", "PASS mining"))
        page = (self.root / "routes" / "templates-mining.md").read_text()
        self.assertIn("| ice-loop | Gather first | -- | [gather](gather.json) > [ice-a](ice-a.json) | 3 | the near bids |", page)

    def test_a_wrong_template_halts_with_a_plain_line_and_changes_nothing(self):
        self.run_plan("zero", "template", "ice-loop", "ice-b,gather")
        self.run_plan("zero", "use", "miner-1", "ice-loop")
        before = self.still()
        for args, says in ((("use", "miner-2", "nope"), "HALT mining: the row of miner-2: `@nope` is no template of the mining division (game/routes/templates/mining.json holds @ice-loop)"),
                           (("template", "bad", "ice-a,ice-x"), "HALT mining: game/routes/templates/mining.json: the template `bad` names `ice-x`, which is no route file"),
                           (("template", "ice-loop", "ice-x"), "the template `ice-loop` names `ice-x`, which is no route file"),
                           (("template", "loop", "@ice-loop"), "the template `loop` names `@ice-loop`: a template holds route ids, never another template"),
                           (("template", "hollow", ""), "the template `hollow` holds no route"),
                           (("first", "board,@ice-loop"), "HALT mining: the list First: `@ice-loop` is a template: the lists First and Then take route ids only"),
                           (("then", "@ice-loop,park"), "HALT mining: the list Then: `@ice-loop` is a template")):
            done = self.run_plan("zero", *args)
            self.assertEqual((done.returncode, says in done.stdout, "HALT mining: nothing changed" in done.stdout), (1, True, True), done.stdout)
            self.assertEqual(self.still(), before, args)
        for name in ("x", "Ice", "9-ice", "miner-2-loop", "a" * 41):
            self.assertIn("REFUSED: `%s` is no template name" % name, self.run_plan("zero", "template", name, "ice-a").stdout)
        self.assertEqual(self.still(), before)

    def test_a_template_ship_names_is_not_removed_and_one_no_ship_names_is(self):
        self.run_plan("zero", "template", "ice-loop", "ice-b,gather")
        self.run_plan("zero", "use", "miner-1..3", "ice-loop")
        before = self.still()
        done = self.run_plan("zero", "template", "ice-loop", "none")
        self.assertEqual(done.returncode, 1)
        self.assertIn("REFUSED: the template @ice-loop stands in the own routes of 3 ships of the mining division", done.stdout)
        self.assertEqual(self.still(), before)
        self.assertIn("REFUSED: the mining division has no template `ghost`", self.run_plan("zero", "template", "ghost", "none").stdout)
        self.run_plan("zero", "set", "miner-1..3", "none")
        done = self.run_plan("zero", "template", "ice-loop", "none")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual((self.kit(), self.role("miner")["templates"], self.git("status", "--porcelain")), ({}, {}, ""))
        self.assertIn("Kept by Zero. Templates: 0. Ships on them: 0.", (self.root / "routes" / "templates-mining.md").read_text())

    def test_a_member_keeps_its_own_division_s_templates_only(self):
        self.assertIn("REFUSED: the plan of the command division is kept by Unity", self.run_plan("zero", "template", "guarding", "guard", "--division", "command").stdout)
        self.assertIn("REFUSED: this shell is no member", self.run_plan(None, "template", "ice-loop", "ice-a").stdout)
        self.assertIsNone(self.kit("command"))
        done = self.run_plan("unity", "template", "guarding", "guard", "--division", "command")       # the Fleet Admiral may
        self.assertEqual(done.returncode, 0, done.stdout)
        before = self.still()
        done = self.run_plan("zero", "use", "miner-1", "guarding")                                # another division's template is no template of this one
        self.assertIn("`@guarding` is no template of the mining division", done.stdout)
        self.assertEqual(self.still(), before)
        self.assertIn("REFUSED: no ship of the mining division: sentinel-1", self.run_plan("zero", "use", "sentinel-1", "guarding").stdout)

    def test_a_template_change_needs_its_commit_and_is_refused_whole_without_it(self):
        (self.root / "routes" / "ice-b.json").write_text(json.dumps(dict(ROUTES["ice-b"], title="another member's change, not committed"), indent=1) + "\n", encoding="ascii")
        before = self.still()
        done = self.run_plan("zero", "template", "ice-loop", "ice-b,gather")
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("REFUSED: game/routes holds a change that is not committed", done.stdout)
        self.assertEqual(self.still(), before)                                                   # no templates file, no list changed, nothing committed
        self.assertFalse((self.root / "routes" / "templates-mining.md").exists())
        self.assertFalse((self.root / "routes" / "templates").exists())                          # the folder made for the commit is taken away again


if __name__ == "__main__":
    unittest.main()
