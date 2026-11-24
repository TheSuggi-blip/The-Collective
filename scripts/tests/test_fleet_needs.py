"""game/fleet/needs.py: the needs register (game/needs.tsv) written by script alone, each division its own, under its caps;
the open needs as the reserve's targets (surplus.py, pull.py) with the demand unchanged by the migration; stock given to the
needs in priority order with a covered percent and a colour; the store's tables needs and need_status; the MCP tool needs.
A disposable repository (git) and data folder; no engine, no network, no live data."""

import calendar
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

REPO = Path(__file__).resolve().parents[2]
FLEET = REPO / "game" / "fleet"
SCRIPT = FLEET / "needs.py"
sys.path.insert(0, str(FLEET))
import surplus                                    # noqa: E402  the reserve's walk: it takes the open needs as its targets
import pull                                       # noqa: E402  the dispatcher's pull rule: the same demand

NOW = calendar.timegm(time.strptime("2026-11-21T20:00:00Z", "%Y-%m-%dT%H:%M:%SZ"))
CATALOG = {
    "version": "9.9.9",
    "items": [{"id": "iron_ore", "name": "Iron Ore", "category": "ore", "size": 1, "base_value": 5},
              {"id": "steel_plate", "name": "Steel Plate", "category": "refined", "size": 1, "base_value": 18},
              {"id": "gem", "name": "Gem", "category": "misc", "size": 1, "base_value": 50},
              {"id": "fuel_cell", "name": "Fuel Cell", "category": "consumable", "size": 1, "base_value": 43},
              {"id": "laser", "name": "Laser", "type": "weapon", "slot": "weapon", "size": 5, "base_value": 300}],
    "recipes": [{"id": "smelt", "inputs": [{"item_id": "iron_ore", "quantity": 10}], "outputs": [{"item_id": "steel_plate", "quantity": 1}],
                 "hand_craftable": True, "produced_by_facility_ids": []}],
    "facilities": [{"id": "lockbox", "name": "Lockbox", "level": 1, "build_cost": 1000, "build_materials": [{"item_id": "steel_plate", "quantity": 10}]},
                   {"id": "vault", "name": "Vault", "level": 2, "build_cost": 500, "build_materials": [{"item_id": "steel_plate", "quantity": 4},
                                                                                                    {"item_id": "gem", "quantity": 2}]}],
    "ships": [{"id": "skiff", "name": "Skiff", "build_materials": [{"item_id": "steel_plate", "quantity": 3}]}]}
TOTALS = {"by_station": {"home_base": {"iron_ore": 30, "steel_plate": 3, "gem": 5}, "far_base": {"iron_ore": 50, "steel_plate": 1, "laser": 2}},
          "holds_by_member": {"Zero": {"iron_ore": 20}}}
HEADER = "\t".join(["id", "project", "division", "kind", "ref", "units", "priority", "place", "due", "status", "note", "added", "added_by", "changed",
                    "changed_by"])
RESERVE_HEAD = "kind\tid\tunits\tnote\n"


def need_line(rid, kind, ref, units, priority=2, division="command", status="open", due="", added="2026-11-21T10:00Z", changed=None, project="a project"):
    """One row of game/needs.tsv as text (the test writes it by hand, as an old copy of the repository would hold it)."""
    return "\t".join([rid, project, division, kind, ref, str(units), str(priority), "", due, status, "", added, "Unity", changed or added, "Unity"])


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_needs_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-needs-test-")
        self.addCleanup(self.temp.cleanup)
        self.repo, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        (self.repo / "game").mkdir(parents=True)
        for folder in ("catalog", "stock", "market", "empire"):
            (self.data / folder).mkdir(parents=True)
        (self.data / "catalog" / "9.9.9.json").write_text(json.dumps(CATALOG), encoding="utf-8")
        self.book(TOTALS)
        (self.repo / "game" / "reserve.tsv").write_text(RESERVE_HEAD + "keep\tfuel_cell\tall\tfuel\n", encoding="ascii")
        try:
            import needs
        except ImportError:                       # a tree without the register: the reserve's own test still runs and shows the demand lost
            needs = None
        self.needs = needs
        if needs is not None:
            self.addCleanup(setattr, needs, "PRUNE_CLOSED", needs.PRUNE_CLOSED)

    def book(self, totals):
        (self.data / "stock" / "storage.json").write_text(json.dumps({"updated_at": "2026-11-21T19:50:00Z", "pilots": {}, "totals": totals}), encoding="utf-8")

    def register(self, *lines):
        (self.repo / "game" / "needs.tsv").write_text("# a register\n" + HEADER + "\n" + "".join(line + "\n" for line in lines), encoding="ascii")

    def git_repo(self):
        for words in (["init", "-q"], ["add", "-A"], ["-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev", "commit", "-q", "-m", "base",
                                                         "--allow-empty"]):
            subprocess.run(["git", "-C", str(self.repo)] + words, check=True, capture_output=True, env=self.env("unity"))

    def env(self, member):
        return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": self.temp.name, "HERMES_SESSION_PROFILE": member, "GIT_CONFIG_NOSYSTEM": "1"}

    def run_needs(self, member, *args):
        return subprocess.run([sys.executable, "-I", "-B", str(SCRIPT)] + list(args) + ["--root", str(self.repo), "--data", str(self.data)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=self.env(member), timeout=120)

    def rows(self):
        rows, problem, _present = self.needs.read(self.repo)
        self.assertEqual(problem, "")
        return {r["id"]: r for r in rows}

    def entries(self, rows=None):
        return {e["id"]: e for e in self.needs.status(str(self.data), str(self.repo), now=NOW, rows=rows)["needs"]}


class WriteTests(Base):
    def test_a_need_is_added_by_its_own_division_and_refused_for_another(self):
        self.git_repo()
        done = self.run_needs("zero", "add", "item", "steel_plate", "10", "--project", "miner hulls tier 2", "--priority", "1")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("committed", done.stdout)
        row = self.rows()["steel-plate"]
        self.assertEqual((row["division"], row["kind"], row["ref"], row["units"], row["priority"], row["status"], row["added_by"]),
                         ("mining", "item", "steel_plate", 10, 1, "open", "Zero"))
        author = subprocess.run(["git", "-C", str(self.repo), "log", "-1", "--format=%an|%s", "--", "game/needs.tsv"], capture_output=True, text=True).stdout.strip()
        self.assertEqual(author, "Zero|needs.tsv: add steel-plate (mining, Zero)")
        refused = self.run_needs("zero", "add", "item", "gem", "2", "--project", "x", "--division", "trade")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("REFUSED: the needs of trade are Mercury's to write", refused.stdout)
        self.assertEqual(self.run_needs("mercury", "done", "steel-plate").returncode, 1)        # Trade closes no need of Mining
        self.assertEqual(self.rows()["steel-plate"]["status"], "open")
        self.assertEqual(self.run_needs("unity", "done", "steel-plate", "--note", "built").returncode, 0)      # the Fleet Admiral any
        self.assertEqual((self.rows()["steel-plate"]["status"], self.rows()["steel-plate"]["changed_by"]), ("done", "Unity"))
        self.assertIn("REFUSED: this shell is no member", self.run_needs("nobody", "add", "item", "gem", "1", "--project", "x").stdout)
        self.assertEqual(subprocess.run(["git", "-C", str(self.repo), "status", "--porcelain"], capture_output=True, text=True).stdout, "")
        check = self.run_needs("zero", "check")
        self.assertEqual(check.returncode, 0, check.stdout)

    def test_a_hand_edit_is_refused_and_named_by_the_gate(self):
        self.git_repo()
        self.assertEqual(self.run_needs("zero", "add", "item", "gem", "2", "--project", "gems").returncode, 0)
        path = self.repo / "game" / "needs.tsv"
        path.write_text(path.read_text() + need_line("by-hand", "item", "gem", 1) + "\n")
        refused = self.run_needs("zero", "add", "item", "iron_ore", "5", "--project", "ore")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("holds a change that is not committed", refused.stdout)
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=Zero", "-c", "user.email=z@x", "commit", "-q", "-am", "by hand"], check=True, capture_output=True)
        check = self.run_needs("zero", "check")
        self.assertEqual(check.returncode, 1)
        self.assertIn("is not in the form needs.py writes", check.stdout)
        self.assertEqual(self.run_needs("unity", "tidy").returncode, 0)                           # tidy writes it again in its one form
        self.assertEqual(self.run_needs("zero", "check").returncode, 0)

    def test_the_cap_of_open_needs_a_division(self):
        self.register(*[need_line("gem-%d" % n, "item", "gem", 1, division="mining") for n in range(self.needs.MAX_OPEN)])
        self.needs.write(self.repo, self.data, "Unity", self.needs.tidier, "tidy", now=NOW)            # the canonical form, no git here
        code, lines = self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "gem", "1", {"project": "one more"}), "add", now=NOW)
        self.assertEqual(code, 1)
        self.assertIn("holds 20 open needs, at most 20 (MAX_OPEN)", lines[0])
        code, _lines = self.needs.write(self.repo, self.data, "Zero", self.needs.changer("Zero", "gem-3", {}, "dropped"), "drop", now=NOW)
        self.assertEqual(code, 0)
        code, _lines = self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "gem", "1", {"project": "one more"}), "add", now=NOW)
        self.assertEqual(code, 0)
        self.register(*[need_line("gem-%d" % n, "item", "gem", 1, division="mining") for n in range(self.needs.MAX_OPEN + 1)])
        errors, _warnings = self.needs.validate(self.needs.read(self.repo)[0], None)
        self.assertEqual(errors, ["game/needs.tsv: 21 open needs of mining, at most 20 (MAX_OPEN): close or drop some"])

    def test_the_fields_are_held_to_their_rules(self):
        self.register()
        cases = (({"project": "p", "note": "x" * 201}, "note: 201 characters, at most 200"), ({"project": ""}, "project: 1 to 80 characters"),
                 ({"project": "p", "priority": "4"}, "priority must be 1, 2 or 3"), ({"project": "p", "due": "21.11.2026"}, "due `21.11.2026`"),
                 ({"project": "p", "place": "Node Beta"}, "place `Node Beta`"))
        for opts, said in cases:
            code, lines = self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "gem", "1", opts), "add", now=NOW)
            self.assertEqual(code, 1, opts)
            self.assertIn(said, lines[0])
        code, lines = self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "ghost_ore", "1", {"project": "p"}), "add", now=NOW)
        self.assertEqual((code, "no item `ghost_ore` in the catalog 9.9.9" in lines[0]), (1, True))
        code, lines = self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "gem", "0", {"project": "p"}), "add", now=NOW)
        self.assertIn("units must be a whole number above 0", lines[0])
        self.assertEqual(self.rows(), {})                                                         # nothing written by a refusal

    def test_a_dry_run_writes_nothing(self):
        self.register()
        before = (self.repo / "game" / "needs.tsv").read_text()
        code, lines = self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "gem", "1", {"project": "p"}), "add", dry=True, now=NOW)
        self.assertEqual(code, 0)
        self.assertTrue(lines[0].startswith("WOULD WRITE game/needs.tsv | add gem (mining)"))
        self.assertEqual((self.repo / "game" / "needs.tsv").read_text(), before)

    def test_closed_rows_leave_after_closed_days_while_the_switch_is_on(self):
        old = "2026-11-01T10:00Z"                                                                 # 20 days before NOW
        self.register(need_line("old-done", "item", "gem", 1, division="mining", status="done", changed=old),
                      need_line("new-done", "item", "gem", 1, division="mining", status="dropped", changed="2026-11-20T10:00Z"))
        self.needs.PRUNE_CLOSED = True
        code, lines = self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "gem", "1", {"project": "p"}), "add", now=NOW)
        self.assertEqual(code, 0)
        self.assertIn("out, closed 14 days or more: old-done", lines[0])
        self.assertEqual(sorted(self.rows()), ["gem", "new-done"])

    def test_closed_rows_stay_while_the_switch_is_off_and_tidy_takes_them_out(self):
        old = "2026-11-01T10:00Z"
        self.register(need_line("old-done", "item", "gem", 1, division="mining", status="done", changed=old))
        self.needs.PRUNE_CLOSED = False
        self.assertEqual(self.needs.write(self.repo, self.data, "Zero", self.needs.adder("Zero", "item", "gem", "1", {"project": "p"}), "add", now=NOW)[0], 0)
        self.assertEqual(sorted(self.rows()), ["gem", "old-done"])
        code, lines = self.needs.write(self.repo, self.data, "Unity", self.needs.tidier, "tidy", dry=True, now=NOW)
        self.assertIn("out, closed 14 days or more: old-done", lines[0])
        self.assertEqual(sorted(self.rows()), ["gem", "old-done"])                                # a dry run
        self.assertEqual(self.needs.write(self.repo, self.data, "Unity", self.needs.tidier, "tidy", now=NOW)[0], 0)
        self.assertEqual(sorted(self.rows()), ["gem"])


class CoverTests(Base):
    def test_priority_allocation_covers_the_higher_need_first(self):
        # 5 gems held, two needs of 4 each: the one of priority 1 is covered, the other gets the one gem left
        self.register(need_line("low", "item", "gem", 4, priority=2, added="2026-11-20T10:00Z"), need_line("high", "item", "gem", 4, priority=1))
        found = self.entries()
        self.assertEqual((found["high"]["rank"], found["high"]["covered"], found["high"]["colour"]), (1, 100.0, "green"))
        self.assertEqual((found["low"]["rank"], found["low"]["covered"], found["low"]["colour"], found["low"]["short"]), (2, 25.0, "red", {"gem": 3}))
        self.register(need_line("late", "item", "gem", 4, priority=1, due="2026-12-30"), need_line("soon", "item", "gem", 4, priority=1, due="2026-12-01"))
        found = self.entries()
        self.assertEqual((found["soon"]["rank"], found["soon"]["colour"], found["late"]["colour"]), (1, "green", "red"))      # then by due
        self.register(need_line("young", "item", "gem", 4, priority=1, added="2026-11-21T11:00Z"), need_line("old", "item", "gem", 4, priority=1))
        self.assertEqual(self.entries()["old"]["colour"], "green")                                # then by age

    def test_a_needs_colour_from_its_covered_share_of_raw_units(self):
        self.register(need_line("half", "item", "gem", 10))
        self.assertEqual((self.entries()["half"]["covered"], self.entries()["half"]["colour"]), (50.0, "yellow"))
        self.register(need_line("less", "item", "gem", 11))
        self.assertEqual(self.entries()["less"]["colour"], "red")
        self.register(need_line("all", "item", "gem", 5))
        self.assertEqual(self.entries()["all"]["colour"], "green")
        # a facility: 10 plates = 100 ore raw; 4 plates held cover 40, the 100 ore held cover the other 60
        self.register(need_line("box", "facility", "lockbox", 1))
        box = self.entries()["box"]
        self.assertEqual((box["raw_units"], box["raw_short"], box["covered"], box["colour"], box["fee"]), (100, 0, 100.0, "green", 1000))
        self.assertEqual(box["stock"], {"steel_plate": 4, "iron_ore": 60})
        self.assertEqual(box["craft"], [("steel_plate", 6, 6, "smelt", "by hand")])
        self.book({"by_station": {"home_base": {"iron_ore": 20}}, "holds_by_member": {}})
        box = self.entries()["box"]
        self.assertEqual((box["raw_short"], box["covered"], box["colour"], box["gather"]), (80, 20.0, "red", {"iron_ore": 80}))
        self.register(need_line("ghost", "item", "ghost_ore", 1))
        self.assertEqual((self.entries()["ghost"]["colour"], self.entries()["ghost"]["covered"]), ("broken", None))

    def test_a_need_past_due_or_unchanged_a_week_is_stale_and_reserves_all_the_same(self):
        self.register(need_line("late", "item", "gem", 2, due="2026-11-20"), need_line("quiet", "item", "gem", 1, changed="2026-11-10T10:00Z"),
                      need_line("fresh", "item", "gem", 1))
        found = self.entries()
        self.assertEqual((found["late"]["stale"], found["quiet"]["stale"], found["fresh"]["stale"]), ("past due 2026-11-20", "unchanged 11 days", ""))
        rows = {r["id"]: r for r in surplus.surplus(str(self.data), str(self.repo), now=NOW)["rows"]}
        self.assertEqual(rows["gem"]["reserved"], 4)

    def test_a_facility_our_empire_holds_already_is_named(self):
        (self.data / "empire" / "empire.json").write_text(json.dumps({"facilities": [{"type": "lockbox"}, {"type": "lockbox"}]}))
        self.register(need_line("box", "facility", "lockbox", 1))
        self.assertEqual(self.entries()["box"]["stands"], 2)
        self.assertIn("our empire holds 2 lockbox already: done? (needs.py done box)", self.needs.short_text(self.entries()["box"]))


class ReserveTests(Base):
    TARGETS = ("facility\tlockbox\t1\tfaction storage\n", "hull\tskiff\t1\ta hull\n", "item\tsteel_plate\t2\tspare plates\n")

    def reserve_sum(self):
        res = surplus.surplus(str(self.data), str(self.repo), now=NOW)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            surplus.show_reserve(res)
        rows = {r["id"]: (r["demand"], r["taken"], r["make"], r["reserved"], r["surplus"], r["short"]) for r in res["rows"]}
        return [line for line in out.getvalue().splitlines() if line.startswith("SUM |")][0], rows, res["totals"]

    def test_the_reserves_demand_is_the_same_after_the_targets_moved_into_the_needs(self):
        (self.repo / "game" / "reserve.tsv").write_text(RESERVE_HEAD + "".join(self.TARGETS) + "keep\tfuel_cell\tall\tfuel\n", encoding="ascii")
        before = self.reserve_sum()
        (self.repo / "game" / "reserve.tsv").write_text(RESERVE_HEAD + "keep\tfuel_cell\tall\tfuel\n", encoding="ascii")
        self.register(need_line("box", "facility", "lockbox", 1), need_line("skiff", "hull", "skiff", 1, division="military"),
                      need_line("plates", "item", "steel_plate", 2, division="logistics"))
        after = self.reserve_sum()
        self.assertEqual(after, before)
        self.assertIn("SUM | 2 items asked for", after[0])
        self.assertNotEqual(before[0], self.reserve_sum_without_needs())

    def reserve_sum_without_needs(self):
        (self.repo / "game" / "needs.tsv").unlink()
        return self.reserve_sum()[0]

    def test_only_open_needs_are_targets_and_a_broken_row_is_skipped_with_a_note(self):
        self.register(need_line("box", "facility", "lockbox", 1), need_line("shut", "item", "gem", 3, status="done"),
                      need_line("ghost", "item", "ghost_ore", 1), need_line("bad", "item", "gem", "x"))
        res = surplus.surplus(str(self.data), str(self.repo), now=NOW)
        self.assertEqual([(t["kind"], t["id"], t.get("need")) for t in res["targets"]], [("keep", "fuel_cell", None), ("facility", "lockbox", "box")])
        self.assertTrue(any("(ghost): no item `ghost_ore` in the catalog 9.9.9: skipped" in w for w in res["warnings"]))
        self.assertTrue(any("(bad): units must be a whole number above 0" in w for w in res["warnings"]))
        first = surplus.first_line("RESERVE", res)
        self.assertIn("reserve file game/reserve.tsv (2 targets) | 1 of them open needs of game/needs.tsv (needs.py)", first)

    def test_the_pull_rule_reads_the_same_demand(self):
        self.register(need_line("plates", "item", "steel_plate", 9, division="logistics"))
        levels = pull.levels(surplus.surplus(str(self.data), str(self.repo), now=NOW))
        self.assertEqual((levels["steel_plate"]["need"], levels["steel_plate"]["max"]), (9, 9))
        self.assertEqual(levels["iron_ore"]["need"], 50)                                          # 5 plates still to make from ore

    def test_the_gate_fails_a_target_left_in_the_reserve_file(self):
        self.register(need_line("box", "facility", "lockbox", 1))
        self.needs.write(self.repo, self.data, "Unity", self.needs.tidier, "tidy", now=NOW)
        self.assertEqual(self.run_needs("unity", "check").returncode, 0)
        (self.repo / "game" / "reserve.tsv").write_text(RESERVE_HEAD + self.TARGETS[0], encoding="ascii")
        done = self.run_needs("unity", "check")
        self.assertEqual(done.returncode, 1)
        self.assertIn("ERROR game/reserve.tsv line 2: a target (facility, hull or item) stands in the reserve file", done.stdout)

    def test_the_repositorys_own_register_and_reserve_pass_the_gate(self):
        rows, problem, present = self.needs.read(REPO)
        self.assertEqual((problem, present), ("", True))
        self.assertTrue(rows)
        errors, _warnings = self.needs.validate(rows, None, REPO)
        self.assertEqual(errors, [])
        self.assertEqual((REPO / "game" / "needs.tsv").read_text(encoding="ascii"), self.needs.render(rows))
        self.assertEqual(self.needs.reserve_targets(REPO), [])


class ReadersTests(Base):
    def test_the_store_mirrors_the_file_and_computes_need_status_when_due(self):
        import store
        self.register(need_line("box", "facility", "lockbox", 1, priority=1), need_line("gems", "item", "gem", 10, division="trade"),
                      need_line("bad", "item", "gem", "x"))
        store.one_pass(str(self.data), now=NOW, root=str(self.repo / "game"))
        conn = sqlite3.connect(str(self.data / "store" / "live.db"))
        self.addCleanup(conn.close)
        self.assertEqual(conn.execute("SELECT id, status, error IS NULL FROM needs ORDER BY line").fetchall(),
                         [("box", "open", 1), ("gems", "open", 1), ("bad", "open", 0)])
        found = conn.execute("SELECT rank, id, colour, covered FROM need_status ORDER BY rank").fetchall()
        self.assertEqual(found, [(1, "box", "green", 100.0), (2, "bad", "broken", None), (3, "gems", "yellow", 50.0)])      # then by id
        at = conn.execute("SELECT value FROM meta WHERE key = 'needs.at'").fetchone()[0]
        store.one_pass(str(self.data), now=NOW + 60, root=str(self.repo / "game"))            # not due: the file did not change, EVERY not passed
        self.assertEqual(conn.execute("SELECT value FROM meta WHERE key = 'needs.at'").fetchone()[0], at)
        self.register(need_line("box", "facility", "lockbox", 1, priority=1))
        os.utime(self.repo / "game" / "needs.tsv", (NOW + 100, NOW + 100))
        store.one_pass(str(self.data), now=NOW + 120, root=str(self.repo / "game"))           # the file changed: computed again
        self.assertEqual(conn.execute("SELECT id FROM need_status").fetchall(), [("box",)])
        for name in ("needs", "need_status"):
            self.assertEqual(len(store.EXAMPLES[name]), 3)
            self.assertTrue(store.DESCRIPTIONS[name])

    def test_the_mcp_tool_builds_each_action_and_is_a_writing_tool(self):
        server = load("collective_mcp")
        plan = lambda **a: server.TOOLS["needs"]["plan"](a)
        self.assertEqual(plan(), [("game/fleet/needs.py", ["list"])])
        self.assertEqual(plan(action="list", division="mining", project="Atria", all=True), [("game/fleet/needs.py", ["list", "mining", "--project", "Atria", "--all"])])
        self.assertEqual(plan(action="show", id="lockbox"), [("game/fleet/needs.py", ["show", "lockbox"])])
        self.assertEqual(plan(action="show", project="Atria outpost"), [("game/fleet/needs.py", ["show", "Atria outpost"])])
        self.assertEqual(plan(action="items"), [("game/fleet/needs.py", ["items"])])
        self.assertEqual(plan(action="check"), [("game/fleet/needs.py", ["check"])])
        self.assertEqual(plan(action="add", kind="facility", ref="hiring_board", units=1, project="Atria outpost", priority=1, due="2026-12-01", dry_run=True),
                         [("game/fleet/needs.py", ["add", "facility", "hiring_board", "1", "--project", "Atria outpost", "--priority", "1", "--due", "2026-12-01",
                                                   "--dry-run"])])
        self.assertEqual(plan(action="set", id="lockbox", units=0, place="-"), [("game/fleet/needs.py", ["set", "lockbox", "--units", "0", "--place", "-"])])
        self.assertEqual(plan(action="done", id="lockbox", note="built"), [("game/fleet/needs.py", ["done", "lockbox", "--note", "built"])])
        self.assertEqual(plan(action="drop", id="lockbox"), [("game/fleet/needs.py", ["drop", "lockbox"])])
        for args in ({"action": "show"}, {"action": "add", "kind": "item"}, {"action": "done"}, {"action": "fly"}):
            with self.assertRaises(ValueError):
                plan(**args)
        self.assertIn("needs", server.WRITES)
        self.assertFalse(server.schema("needs")["annotations"]["readOnlyHint"])
        self.assertFalse(server.TOOLS["needs"].get("door"))
        self.register(need_line("box", "facility", "lockbox", 1))
        text, failed = server.call(str(REPO), str(self.data), "Zero", "needs", {"action": "list"})
        self.assertFalse(failed, text)
        self.assertTrue(text.startswith("NEEDS | the open needs"), text[:200])

    def test_hive_reads_the_register_and_refuses_a_write(self):
        self.register(need_line("box", "facility", "lockbox", 1))
        self.needs.write(self.repo, self.data, "Unity", self.needs.tidier, "tidy", now=NOW)
        run = lambda *a: subprocess.run([sys.executable, "-I", "-B", str(FLEET / "hive.py"), "needs"] + list(a) + ["--root", str(self.repo / "game"), "--data", str(self.data)],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=self.env("zero"), timeout=120)
        done = run("list")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("box", done.stdout)
        self.assertEqual(run("check").returncode, 0)
        refused = run("add", "item", "gem", "1", "--project", "x")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("REFUSED: hive.py reads only", refused.stdout)

    def test_the_briefing_line_counts_the_divisions_open_and_red_needs(self):
        self.register(need_line("box", "facility", "lockbox", 1, division="mining"), need_line("gems", "item", "gem", 9, division="trade"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.needs.briefing(str(self.repo / "game"), str(self.data), NOW, "Zero")
        self.assertTrue(out.getvalue().startswith("=== NEEDS | mining: 1 open, 0 red, 0 stale | the fleet: 2 open, 0 red, 0 stale | colours not measured yet"))
        import store
        store.one_pass(str(self.data), now=NOW, root=str(self.repo / "game"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.needs.briefing(str(self.repo / "game"), str(self.data), NOW, "Mercury")
        self.assertEqual(out.getvalue(), "=== NEEDS | trade: 1 open, 0 red, 0 stale | the fleet: 2 open, 0 red, 0 stale | the tool needs: action=list, action=add\n")



class AddPrioritySortRoundtripTests(unittest.TestCase):
    def test_add_with_string_priority_roundtrips_cleanly_in_check(self):
        import needs
        with tempfile.TemporaryDirectory(prefix="needs-rt-") as td:
            repo = Path(td) / "repo"
            data = Path(td) / "data"
            (repo / "game").mkdir(parents=True)
            data.mkdir(parents=True)
            # Existing priority-3 row whose id sorts AFTER guild-hall-recruiting
            rc1, _ = needs.write(repo, data, "Apollo", needs.adder("Apollo", "facility", "transit_lounge", "1",
                                 {"id": "transit-lounge", "project": "pax", "priority": "3", "division": "logistics"}), "add", now=1700000000)
            self.assertEqual(rc1, 0)
            rc2, _ = needs.write(repo, data, "Apollo", needs.adder("Apollo", "facility", "guild_hall_recruiting", "1",
                                 {"project": "400 seats", "priority": "3", "place": "central_nexus", "division": "logistics"}), "add", now=1700000060)
            self.assertEqual(rc2, 0)
            rows, prob, pres = needs.read(repo)
            self.assertTrue(pres and not prob)
            text = needs.path_of(repo).read_bytes().decode("ascii")
            self.assertEqual(text, needs.render(rows))

if __name__ == "__main__":
    unittest.main()
