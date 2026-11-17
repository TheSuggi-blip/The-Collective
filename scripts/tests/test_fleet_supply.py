"""game/fleet/supply.py and its hooks: the chains file parses and a broken row is reported without stopping the store; the view
supply_status says short, low and ok with the stock at its place, the change over 24 hours, the ships on the sources; check is the
gate; duty lists a source route the keeper's plan lacks, refuses --write while DUTY_ENABLED is False, and when on puts the route into
the list Then with its end and takes it out again; hive.py supply and the MCP tool supply only read. A disposable data folder and
repository; plan.apply is a fake; no engine, no network."""

import importlib.util
import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"
sys.path.insert(0, str(FLEET))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


store = load("store_supply_under_test", FLEET / "store.py")
import supply                                     # noqa: E402  the module store.py reads the chains with
import plan as planfile                           # noqa: E402  plan.apply is replaced by a fake in the tests that write
import division                                   # noqa: E402  who runs the script

STAMP = "2026-11-16T12:00:00Z"
BOOK = {"updated_at": STAMP,
        "pilots": {"miner-1": {"read_at": STAMP, "stations": {"base_a": {"iron_ore": 10, "water_ice": 3}, "base_b": {"iron_ore": 2}}},
                   "trader-2": {"read_at": STAMP, "stations": {"base_b": {"iron_ore": 7, "steel_plate": 4}}}},
        "totals": {"holds_by_member": {"Zero": {"iron_ore": 5}, "Mercury": {"steel_plate": 1}}}}
CHAINS = ("# the chains of the test\n"
          "chain\titem\tplace\tkeep\tneed_per_hour\tsources\tkeeper\tnote\n"
          "iron\tiron_ore\tfleet\t30\t6\tmine-a, mine-b,gone-route\tMining\tshort: 24 held\n"
          "ice\twater_ice\tbase_a\t2\t0\t\tLogistics\tlow: 3 at base_a\n"
          "ice-sys\twater_ice\tsys_a\t1\t0\t\tlogistics\tok: 3 in sys_a, its station base_a by the census\n"
          "plate\tsteel_plate\tfleet\t2\t\tmine-a\tTrade\tok: 5\n"
          "bunker\tfuel\tbase_o\t5000\t0\t\tLogistics\tshort, and no reading of the place\n"
          "bad chain\tiron_ore\tfleet\tlots\t0\t\tNobody\tbroken\n")


def write(path, value, mtime=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="ascii")
    if mtime is not None:
        os.utime(path, (mtime, mtime))


def bump(path, value):
    write(path, value)
    later = path.stat().st_mtime + 7
    os.utime(path, (later, later))


def fixture(data, root, now, chains=CHAINS):
    ship = lambda name, division_, docked: {"name": name, "division": division_, "system": "sys_a", "poi": "sys_a_belt", "docked": docked,
                                            "status": "connected", "class": "Threshold", "state_at": STAMP}
    write(data / "fleet" / "fleet.json", {"updated_at": STAMP, "ships": [ship("miner-1", "Mining", "base_a"), ship("trader-2", "Trade", "")]})
    write(data / "fleet" / "orders" / "miner-1.json", {"pilot": "miner-1", "what": "mine mine-a"}, mtime=now - 60)
    write(data / "stock" / "storage.json", BOOK)
    write(data / "catalog" / "0.2.0.json", {"version": "0.2.0", "items": [{"id": item} for item in ("iron_ore", "water_ice", "steel_plate", "fuel")]})
    write(data / "scouting" / "sys_a.json", {"read_at": STAMP, "system": {"id": "sys_a", "pois": [
        {"id": "base_a", "name": "A Station", "type": "station", "has_base": True, "base_id": "base_a"}]}, "pois": {}})
    write(data / "empire" / "empire.json", {"written_at": STAMP, "bases": [{"base": "base_o", "name": "Our Outpost", "system": "sys_b", "kind": "outpost"}]})
    write(root / "routes" / "mine-a.json", {"id": "mine-a", "kind": "mine", "title": "A", "belt": "sys_a:sys_a_belt", "standing": True, "min_left": {"iron_ore": 10}})
    write(root / "routes" / "mine-b.json", {"id": "mine-b", "kind": "mine", "title": "B", "belt": "sys_a:sys_a_belt", "standing": True, "min_left": {"iron_ore": 10}})
    write(root / "routes" / "census-x.json", {"id": "census-x", "kind": "census", "title": "Census", "systems": ["sys_a"]})
    write(root / "routes" / "park.json", {"id": "park", "kind": "circuit", "title": "Dock and wait", "park": True, "stops": []})
    write(root / "routes" / "plans" / "miner.json", {"role": "miner", "owner": "Zero", "routes": ["mine-a", "census-x", "park"], "ships": {"mine-a": 2}})
    if chains is not None:
        write(root / "supply" / "chains.tsv", chains)


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-supply-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "game"
        self.now = time.time()
        fixture(self.data, self.root, self.now)

    def one(self, now=None):
        return store.one_pass(str(self.data), now=self.now if now is None else now, root=str(self.root))

    def rows(self):
        return {r["chain"]: r for r in supply.read(str(self.data))["rows"]}

    def run_main(self, *words):
        out = io.StringIO()
        with redirect_stdout(out):
            code = supply.main(list(words) + ["--root", str(self.root), "--data", str(self.data)])
        return code, out.getvalue()


class FileTests(Base):
    def test_the_file_parses_and_a_broken_row_is_reported_and_the_store_goes_on(self):
        out = self.one()
        self.assertEqual(out["snapshot"]["loaded"]["supply"], 1)
        self.assertNotIn("game/supply/chains.tsv", [name for name, _note in out["snapshot"]["problems"]])
        self.assertEqual(out["snapshot"]["loaded"]["holdings"], 1)                       # the other loaders went on
        conn = store.connect(str(self.data))
        self.addCleanup(conn.close)
        found = conn.execute("SELECT chain, item, place, keep, need_per_hour, sources, keeper, line, error FROM supply_chains ORDER BY line").fetchall()
        self.assertEqual([row[:8] for row in found[:5]], [
            ("iron", "iron_ore", "fleet", 30, 6.0, "mine-a,mine-b,gone-route", "Mining", 3), ("ice", "water_ice", "base_a", 2, 0.0, "", "Logistics", 4),
            ("ice-sys", "water_ice", "sys_a", 1, 0.0, "", "Logistics", 5), ("plate", "steel_plate", "fleet", 2, 0.0, "mine-a", "Trade", 6),
            ("bunker", "fuel", "base_o", 5000, 0.0, "", "Logistics", 7)])
        self.assertEqual([row[8] for row in found[:5]], [None] * 5)
        broken = found[5]
        self.assertEqual((broken[0], broken[3], broken[7]), ("bad chain", None, 8))
        for words in ("chain `bad chain`", "keep must be a whole number", "keeper `Nobody`"):
            self.assertIn(words, broken[8])

    def test_each_rule_of_a_row_and_a_file_without_its_header(self):
        rows, problem = supply.parse("chain\titem\tplace\tkeep\tneed_per_hour\tsources\tkeeper\tnote\n"
                                     "a\tiron_ore\tfleet\t1\t-2\tok-route,Bad Route\tMining\n"
                                     "a\tIron Ore\t\t1\t0\t\tMining\tnote\n"
                                     "b\tiron_ore\tfleet\t1\n"
                                     "c\tiron_ore\tfleet\t1\t0\t\tMining\tnote\textra\n")
        self.assertEqual(problem, "")
        errors = [r["error"] or "" for r in rows]
        self.assertIn("need_per_hour must be a number, 0 or more", errors[0])
        self.assertIn("source `Bad Route` is no route id", errors[0])
        self.assertIn("chain a stands on line 2 too", errors[1])
        self.assertIn("item `Iron Ore` is no item id", errors[1])
        self.assertIn("no place", errors[1])
        self.assertIn("needs chain, item, place", errors[2])
        self.assertIn("9 cells, the header has 8", errors[3])
        self.assertEqual(supply.parse("# only words\nnot\ta\theader\n"), ([], "line 2: the header `chain<TAB>item<TAB>place<TAB>keep<TAB>need_per_hour<TAB>sources<TAB>keeper<TAB>note` "
                                                                          "must come before the first chain"))
        self.assertEqual(supply.parse("# nothing\n")[1], "no header `chain<TAB>item<TAB>place<TAB>keep<TAB>need_per_hour<TAB>sources<TAB>keeper<TAB>note`")

    def test_a_file_that_cannot_be_read_is_named_its_rows_stay_and_a_file_that_went_takes_them(self):
        self.one()
        path = self.root / "supply" / "chains.tsv"
        bump(path, "iron\tiron_ore\tfleet\t30\n")                                         # no header: the whole file is not read
        out = self.one(now=self.now + 30)
        self.assertIn(("game/supply/chains.tsv", "bad: ValueError: line 1: the header `chain<TAB>item<TAB>place<TAB>keep<TAB>need_per_hour<TAB>sources<TAB>keeper"
                                                 "<TAB>note` must come before the first chain"), out["snapshot"]["problems"])
        self.assertEqual(len(self.rows()), 6)                                             # as last read
        path.write_bytes(CHAINS.replace("short: 24 held", "short: \xe9").encode("latin-1"))     # not ASCII
        os.utime(path, (self.now + 99, self.now + 99))
        copy = self.data / "store" / "read.db"
        os.utime(copy, (time.time() - store.PUBLISH - 5,) * 2)                           # a pass that only names a file publishes when the copy is due
        out = self.one(now=self.now + 60)
        self.assertTrue(any(name == "game/supply/chains.tsv" and "UnicodeDecodeError" in note for name, note in out["snapshot"]["problems"]))
        res = supply.read(str(self.data))
        self.assertIn("NOT READ NOW", supply.first_line("T", res))
        path.unlink()
        out = self.one(now=self.now + 90)
        self.assertEqual((out["snapshot"]["gone"], self.rows()), (1, {}))


class ViewTests(Base):
    def test_the_view_says_short_low_and_ok_at_each_place(self):
        self.one()
        rows = self.rows()
        got = {name: (r["status"], r["stock"], r["keep"]) for name, r in rows.items()}
        self.assertEqual(got, {"iron": ("short", 24, 30), "ice": ("low", 3, 2), "ice-sys": ("ok", 3, 1), "plate": ("ok", 5, 2), "bunker": ("short", 0, 5000),
                               "bad chain": ("broken", 24, None)})
        iron = rows["iron"]
        self.assertEqual((iron["hours_left"], iron["sources_listed"], iron["sources_known"], iron["ships"], iron["sources_planned"]), (4.0, 3, 2, 1, 1))
        self.assertEqual((rows["ice"]["place_rows"], rows["bunker"]["place_rows"]), (2, 0))      # base_a holds two items; the bunker no reading
        self.assertEqual((iron["change_24h"], rows["ice"]["change_24h"]), (None, None))         # one sample is no change
        self.assertEqual([r["chain"] for r in supply.read(str(self.data))["rows"]][:3], ["bad chain", "bunker", "iron"])   # broken, then the shortest

    def test_the_change_over_24_hours_is_read_from_the_hourly_samples_for_the_fleet_only(self):
        noon = store.epoch("2026-11-16T12:10:00Z")
        self.one(now=noon)
        book = json.loads(json.dumps(BOOK))
        book["pilots"]["miner-1"]["stations"]["base_a"]["iron_ore"] = 110
        bump(self.data / "stock" / "storage.json", book)
        self.one(now=noon + 25 * 3600)
        rows = self.rows()
        self.assertEqual((rows["iron"]["change_24h"], rows["iron"]["change_hours"], rows["iron"]["stock"], rows["iron"]["status"]), (100, 25, 124, "ok"))
        self.assertEqual((rows["ice"]["change_24h"], rows["ice"]["change_hours"]), (None, None))

    def test_show_and_check(self):
        self.one()
        code, text = self.run_main("show")
        self.assertEqual(code, 0)
        self.assertRegex(text, r"(?m)^  short\s+bunker\s+fuel\s+base_o\s+0 \(not read\)\s+5,000")
        self.assertIn("SUM | 6 chains: 2 short, 1 low, 2 ok, 1 broken", text)
        code, text = self.run_main("check")
        self.assertEqual(code, 1)
        self.assertIn("SHORT iron: iron_ore at fleet: 24 of 30 | 3 sources (1 in a plan), 1 ships on them now | keeper Mining", text)
        self.assertIn("SHORT bunker: fuel at base_o: 0 of 5,000 (no reading of the place", text)
        self.assertIn("BROKEN line 8 (bad chain)", text)
        self.assertIn("ERROR iron: source gone-route has no route file", text)
        self.assertIn("HALT: 2 chains short, 1 rows broken, 1 errors (of 6 chains)", text)
        bump(self.root / "supply" / "chains.tsv", "chain\titem\tplace\tkeep\tneed_per_hour\tsources\tkeeper\tnote\nplate\tsteel_plate\tfleet\t2\t0\tmine-a\tTrade\t\n")
        self.one(now=self.now + 30)
        code, text = self.run_main("check")
        self.assertEqual((code, text.splitlines()[-1]), (0, "PASS: 1 chains, every one at its keep or above"))

    def test_no_read_copy_and_no_view_are_said_plainly(self):
        code, text = self.run_main("check")
        self.assertEqual(code, 1)
        self.assertIn("no read copy of the store yet", text)


class DutyTests(Base):
    def setUp(self):
        super().setUp()
        self.one()
        self.calls = []
        real = planfile.apply

        def fake(root, data, names, who, changes=None, extra=None, message=None, commit=None, now=None):
            plan = {"first": [], "ships": {"miner-1": ["mine-a"]}, "then": list(self.then), "templates": {}, "planned": [], "notes": "", "errors": []}
            for name in names:
                changes[name](plan)
            self.calls.append({"names": names, "who": who, "then": plan["then"], "message": message})
            return True, ["%s: applied (a fake)" % names[0]]
        self.then = ["census-x", "park"]
        planfile.apply = fake
        self.addCleanup(setattr, planfile, "apply", real)

    def test_duty_lists_the_source_route_the_keepers_plan_does_not_hold(self):
        code, text = self.run_main("duty")
        self.assertEqual(code, 0)
        self.assertIn("iron (Mining: iron_ore at fleet, 24 of 30): the mining plan (roles miner) holds 1 of its 3 sources: mine-a", text)
        self.assertIn("  ADD mine-b -> the list Then of the mining plan", text)
        self.assertIn("no route file, not added: gone-route", text)
        self.assertIn("bunker (Logistics: fuel at base_o, 0 of 5,000): no source route: Logistics writes one; no route file brings fuel", text)
        self.assertIn("SUM | 1 routes to put into 1 plans, 0 to take out, 0 ends to renew | a dry run: nothing written", text)
        self.assertEqual(self.calls, [])
        self.assertEqual(supply.gatherers(str(self.root), "iron_ore"), ["mine-a", "mine-b"])

    def test_write_is_refused_while_duty_is_not_enabled(self):
        self.addCleanup(setattr, supply, "DUTY_ENABLED", supply.DUTY_ENABLED)
        supply.DUTY_ENABLED = False                       # the state this test reads; the module's own default is on
        code, text = self.run_main("duty", "--write")
        self.assertEqual(code, 1)
        self.assertIn("REFUSED: DUTY_ENABLED is False", text)
        self.assertEqual(self.calls, [])
        self.assertFalse((self.data / "supply" / "duty.json").exists())

    def test_when_enabled_the_route_goes_into_the_list_then_with_its_end_and_out_again(self):
        self.addCleanup(setattr, supply, "DUTY_ENABLED", supply.DUTY_ENABLED)
        self.addCleanup(setattr, division, "member", division.member)
        supply.DUTY_ENABLED = True
        division.member = lambda env=None: ("member", "Zero")
        code, text = self.run_main("duty", "--write")
        self.assertEqual(code, 0, text)
        self.assertEqual([(c["names"], c["who"], c["then"]) for c in self.calls], [(["mining"], "Zero", ["mine-b", "census-x", "park"])])
        self.assertIn("+mine-b", self.calls[0]["message"])
        record = supply.load_record(str(self.data))
        self.assertEqual(sorted(record), ["mining/mine-b"])
        entry = record["mining/mine-b"]
        self.assertEqual((entry["chain"], entry["by"]), ("iron", "Zero"))
        self.assertAlmostEqual(supply.epoch(entry["until"]) - supply.epoch(entry["added"]), supply.DUTY_HOURS * 3600)
        res = supply.read(str(self.data))
        later = supply.epoch(entry["until"]) + 60
        self.assertEqual(supply.steps(res, record, later)["renew"], ["mining/mine-b"])            # still short at its end: renewed
        for row in res["rows"]:
            if row["chain"] == "iron":
                row["status"] = "low"
        self.assertEqual(supply.steps(res, record, supply.epoch(entry["added"]) + 60)["divisions"], {})      # low before its end: it stays
        plan_steps = supply.steps(res, record, later)
        self.assertEqual(plan_steps["divisions"]["mining"]["end"][0][:2], ("mining/mine-b", "mine-b"))
        self.then = ["mine-b", "census-x", "park"]
        good, lines = supply.write(str(self.root), str(self.data), plan_steps, record, "Zero", later)
        self.assertTrue(good, lines)
        self.assertEqual(self.calls[-1]["then"], ["census-x", "park"])
        self.assertEqual(supply.load_record(str(self.data)), {})

    def test_a_member_changes_only_its_own_division(self):
        self.addCleanup(setattr, supply, "DUTY_ENABLED", supply.DUTY_ENABLED)
        self.addCleanup(setattr, division, "member", division.member)
        supply.DUTY_ENABLED = True
        division.member = lambda env=None: ("member", "Apollo")
        code, text = self.run_main("duty", "--write")
        self.assertEqual(code, 1)
        self.assertIn("REFUSED mining: the mining plan is kept by Zero", text)
        self.assertEqual(self.calls, [])


class DoorTests(Base):
    def test_hive_supply_reads_and_never_hands_on_write(self):
        self.one()
        line = [sys.executable, "-I", "-B", str(FLEET / "hive.py"), "supply"]
        where = ["--data", str(self.data), "--root", str(self.root)]
        done = subprocess.run(line + ["check"] + where, capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertIn("HALT: 2 chains short", done.stdout)
        done = subprocess.run(line + ["duty", "--write"] + where, capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("a dry run: nothing written", done.stdout)
        self.assertNotIn("REFUSED", done.stdout)
        done = subprocess.run(line + where, capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("SUPPLY | the goods the fleet must never run out of", done.stdout)

    def test_the_mcp_tool_supply_runs_the_script_and_only_reads(self):
        server = load("collective_mcp_supply_under_test", FLEET / "collective_mcp.py")
        plan = server.TOOLS["supply"]["plan"]
        self.assertEqual(plan({}), [("game/fleet/supply.py", ["show"])])
        self.assertEqual(plan({"view": "duty"}), [("game/fleet/supply.py", ["duty"])])
        with self.assertRaises(ValueError):
            plan({"view": "duty --write"})
        self.assertTrue(server.schema("supply")["annotations"]["readOnlyHint"])
        self.assertTrue((ROOT / "game" / "supply" / "chains.tsv").is_file())
        rows, problem = supply.parse((ROOT / "game" / "supply" / "chains.tsv").read_text(encoding="ascii"))      # the repository's own file
        self.assertEqual((problem, [r["error"] for r in rows if r["error"]]), ("", []))


if __name__ == "__main__":
    unittest.main()
