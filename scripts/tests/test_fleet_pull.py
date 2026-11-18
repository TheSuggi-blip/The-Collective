"""game/fleet/pull.py: the class guard (rule F23) and the pull rule of the dispatcher, each behind its switch file, the
reserve's pull levels with their hysteresis and their own ends, and the dry run. A disposable repository and data
folder; no engine, no network."""

import calendar
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
sys.path.insert(0, str(FLEET))
import pull                                       # noqa: E402  the module under test (dispatch.py imports it by this name)
import dispatch                                   # noqa: E402  the dispatcher's one rule, with pull's hook

NOW = calendar.timegm(time.strptime("2026-11-18T01:00:00Z", "%Y-%m-%dT%H:%M:%SZ"))
STAMP = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
CATALOG = {
    "version": "9.9.9",
    "items": [{"id": "iron_ore", "name": "Iron Ore", "category": "ore", "size": 1, "base_value": 5},
              {"id": "silver_ore", "name": "Silver Ore", "category": "ore", "size": 1, "base_value": 20},
              {"id": "steel_plate", "name": "Steel Plate", "category": "refined", "size": 1, "base_value": 18}],
    "recipes": [{"id": "smelt", "inputs": [{"item_id": "iron_ore", "quantity": 10}], "outputs": [{"item_id": "steel_plate", "quantity": 1}],
                 "hand_craftable": True, "produced_by_facility_ids": []}],
    "facilities": [], "ships": []}
ROUTES = {
    "gather-iron": {"id": "gather-iron", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "standing": True},
    "gather-mixed": {"id": "gather-mixed", "kind": "mine", "title": "t", "belt": "far:mixed", "station": "home:core:base", "standing": True},
    "sell-iron": {"id": "sell-iron", "kind": "mine", "title": "t", "belt": "far:rocks", "station": "home:core:base", "sell": [{"item": "iron_ore", "min_price": 9}]},
    "craft-steel": {"id": "craft-steel", "kind": "circuit", "title": "t", "stops": [
        {"at": "home:core:base", "store": "all", "craft": [{"recipe": "smelt", "runs": 4, "per_run": 1, "makes": "steel_plate"}]}]},
    "mission-iron": {"id": "mission-iron", "kind": "circuit", "title": "t", "once": True, "stops": [{"at": "home:core:base", "mine": [{"at": "far:rocks"}]}]},
    "hunt-rays": {"id": "hunt-rays", "kind": "hunt", "title": "t", "place": "far:cloud", "sell_at": "home:core:base"},
    "unknown-field": {"id": "unknown-field", "kind": "mine", "title": "t", "belt": "far:dark", "station": "home:core:base"},
}


def record(full=("iron_ore",), now=NOW, **more):
    """A record as the dispatcher writes it: iron (and what `full` names) full; the fields and the recipe by hand."""
    items = {"iron_ore": {"held": 251133, "need": 185470, "max": 185470, "min": 166923, "full": False},
             "steel_plate": {"held": 0, "need": 10, "max": 10, "min": 9, "full": False}}
    for item in full:
        items[item].update(full=True, since=STAMP(now - 600), until=STAMP(now + 3600))
    out = {"written_at": STAMP(now), "until": STAMP(now + 3600), "items": items, "makes": {"smelt": ["steel_plate"]},
           "yields": {"far:rocks": ["iron_ore"], "far:mixed": ["iron_ore", "silver_ore"]}}
    out.update(more)
    return out


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-pull-test-")
        self.addCleanup(self.temp.cleanup)
        self.top, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        self.root = self.top / "game"
        for folder in (self.root / "routes" / "plans", self.data / "fleet" / "ships", self.data / "routes", self.data / "catalog", self.data / "stock",
                       self.data / "scouting", self.data / "plans", self.data / "market"):
            folder.mkdir(parents=True)
        for rid, route in ROUTES.items():
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route), encoding="ascii")
        (self.data / "catalog" / "9.9.9.json").write_text(json.dumps(CATALOG), encoding="ascii")
        self.book(200, STAMP(NOW - 600))
        (self.root / "reserve.tsv").write_text("kind\tid\tunits\tnote\nitem\tsteel_plate\t10\tten plates\n", encoding="ascii")
        (self.data / "scouting" / "far.json").write_text(json.dumps({"system": "far", "read_at": STAMP(NOW - 7200), "pois": {
            "rocks": {"resources": [{"resource_id": "iron_ore", "remaining": 5000}]},
            "mixed": {"resources": [{"resource_id": "iron_ore", "remaining": 900}, {"resource_id": "silver_ore", "remaining": 40}, {"resource_id": "gold_ore", "remaining": 0}]}}}))
        self.addCleanup(pull.FORCE.clear)
        self.addCleanup(pull.SWITCHES.clear)
        pull.SWITCHES.clear()

    def book(self, iron, written):
        (self.data / "stock" / "storage.json").write_text(json.dumps({"updated_at": written, "pilots": {}, "totals": {
            "by_station": {"base": {"iron_ore": iron}}, "holds_by_member": {}}}), encoding="ascii")

    def state(self, now=NOW, **more):
        return dict({"now": now, "data": str(self.data), "rows": [], "orders": {}, "rest": {}, "booked": {}}, **more)

    def switch(self, name, on=True):
        path = self.data / name
        if on:
            path.write_text("")
        elif path.exists():
            path.unlink()


class ClassGuardTests(Tree):
    """Rule F23 (Suggi, 2026-11-18: "Ore is miners job"): each class flies its own work."""

    def test_the_reason_names_the_class_and_its_roles(self):
        self.assertEqual(pull.class_reason("trader", ROUTES["gather-iron"], "gather-iron"), "class: gather is miners' work")
        self.assertEqual(pull.class_reason("miner", ROUTES["hunt-rays"], "hunt-rays"), "class: hunt is drones, sentinels, scouts and command ships' work")
        self.assertIsNone(pull.class_reason("miner", ROUTES["gather-iron"], "gather-iron"))
        for role in ("trader", "hauler", "drone", "scout", "command"):                    # a mission paid once and a craft from its own stores: every role's
            self.assertIsNone(pull.class_reason(role, ROUTES["mission-iron"], "mission-iron"), role)
            self.assertIsNone(pull.class_reason(role, ROUTES["craft-steel"], "craft-steel"), role)
        self.assertIsNone(pull.class_reason("hauler", dict(ROUTES["gather-iron"], open_to=["hauler"]), "gather-iron"))   # its Admiral's word

    def test_the_guard_acts_only_while_its_switch_file_exists(self):
        trader = {"name": "trader-1", "role": "trader", "credits": 20000, "modules": [], "docked": True}
        why = lambda now=NOW: dispatch.why_not(trader, "gather-iron", ROUTES["gather-iron"], self.state(now))[0]
        self.assertIsNone(why())                                                          # off: the rule as it was
        self.switch("fleet/class-guard-on")
        self.assertEqual(why(NOW + 1), "class: gather is miners' work")                   # on: refused, with the reason
        miner = dict(trader, name="Zero Point", role="miner")                            # a flagship: the role its entry names, not its name
        self.assertIsNone(dispatch.why_not(miner, "gather-iron", ROUTES["gather-iron"], self.state(NOW + 1))[0])
        self.assertIsNone(dispatch.why_not(trader, "craft-steel", ROUTES["craft-steel"], self.state(NOW + 1))[0])
        self.assertEqual(dispatch.why_not(trader, "gather-iron", ROUTES["gather-iron"], self.state(NOW + 1, class_guard=False))[0], None)   # the pass's own reading wins
        self.switch("fleet/class-guard-on", on=False)
        self.assertIsNone(why(NOW + 2))

    def test_the_guard_reads_its_file_once_per_clock_reading(self):
        self.assertFalse(pull.switch(str(self.data), pull.GUARD_SWITCH, NOW))
        self.switch("fleet/class-guard-on")
        self.assertFalse(pull.switch(str(self.data), pull.GUARD_SWITCH, NOW))            # the same pass: the reading it made
        self.assertTrue(pull.switch(str(self.data), pull.GUARD_SWITCH, NOW + 30))         # the next pass reads again
        self.assertFalse(pull.switch(None, pull.GUARD_SWITCH, NOW))                       # no data folder: off


class LevelTests(Tree):
    def test_max_is_the_need_and_min_ninety_percent_unless_the_file_says(self):
        res = {"rows": [{"id": "iron_ore", "held": 251133, "demand": 185470}, {"id": "core", "held": 0, "demand": 1}, {"id": "gem", "held": 9, "demand": 0},
                        {"id": "silver_ore", "held": 50, "demand": 0}],
               "levels": {"silver_ore": {"max": 40}, "core": {"min": 5}, "gem": {"min": 3}}}
        got = pull.levels(res)
        self.assertEqual(got["iron_ore"], {"held": 251133, "need": 185470, "max": 185470, "min": 166923, "set": "need"})
        self.assertEqual((got["core"]["max"], got["core"]["min"]), (1, 1))                 # a min above max is max
        self.assertEqual((got["silver_ore"]["max"], got["silver_ore"]["min"], got["silver_ore"]["set"]), (40, 36, "file"))
        self.assertNotIn("gem", got)                                                      # nothing asks for it and no max: no level
        self.assertEqual(pull.levels({"rows": [{"id": "core", "held": 0, "demand": 1}]})["core"]["min"], 1)   # 90 percent of 1, rounded up

    def test_full_at_max_held_between_and_open_below_min_and_a_mark_ends_by_itself(self):
        level = lambda held: {"held": held, "need": 100, "max": 100, "min": 90, "set": "need"}
        first = pull.mark(level(100), {}, NOW, True)
        self.assertEqual((first["full"], first["since"], first["until"]), (True, STAMP(NOW), STAMP(NOW + pull.FULL_HOURS * 3600)))
        between = pull.mark(level(95), first, NOW + 60, True)
        self.assertEqual((between["full"], between["since"], between["until"]), (True, first["since"], first["until"]))   # hysteresis: it stays full
        self.assertFalse(pull.mark(level(89), between, NOW + 120, True)["full"])                                        # below min: open
        self.assertFalse(pull.mark(level(95), {}, NOW, True)["full"])                                                     # between, open before: open
        self.assertFalse(pull.mark(level(95), first, NOW + pull.FULL_HOURS * 3600, True)["full"])                         # its end came: open
        stale = pull.mark(level(500), first, NOW, False)
        self.assertEqual((stale["full"], stale["why"]), (False, "the storage book is not fresh: not measured"))

    def test_the_record_rests_on_surplus_and_the_census(self):
        made, told = pull.make_record(str(self.root), str(self.data), NOW, None)
        self.assertEqual(sorted(made["items"]), ["iron_ore", "steel_plate"])                 # what the reserve's walk asks for
        iron = made["items"]["iron_ore"]
        self.assertEqual((iron["held"], iron["need"], iron["max"], iron["min"], iron["full"]), (200, 100, 100, 90, True))
        self.assertFalse(made["items"]["steel_plate"]["full"])
        self.assertEqual(made["yields"], {"far:mixed": ["iron_ore", "silver_ore"], "far:rocks": ["iron_ore"]})   # a resource read at 0 is not brought
        self.assertEqual(made["makes"], {"smelt": ["steel_plate"]})
        self.assertEqual((made["until"], made["book_fresh"]), (STAMP(NOW + pull.RECORD_HOURS * 3600), True))
        self.assertEqual(told, ["iron_ore full: 200 of max 100; routes that only bring it close until it holds less than 90"])
        (self.root / "reserve.tsv").write_text("kind\tid\tunits\tnote\nitem\tsteel_plate\t10\t\nmax\tiron_ore\t300\tthe Fleet Admiral's level\n", encoding="ascii")
        again, told = pull.make_record(str(self.root), str(self.data), NOW + 60, made)
        self.assertEqual((again["items"]["iron_ore"]["max"], again["items"]["iron_ore"]["min"], again["items"]["iron_ore"]["full"]), (300, 270, False))
        self.assertEqual(told, ["iron_ore open again: 200, below its min 270"])
        self.book(200, STAMP(NOW - (pull.BOOK_HOURS + 1) * 3600))
        stale, _told = pull.make_record(str(self.root), str(self.data), NOW, None)
        self.assertEqual((stale["book_fresh"], [i for i, e in stale["items"].items() if e["full"]]), (False, []))   # an old book closes nothing


class PullRuleTests(Tree):
    def test_a_route_closes_only_when_every_good_it_brings_is_full(self):
        rec = record()
        self.assertEqual(pull.full_reason(ROUTES["gather-iron"], "gather-iron", rec, NOW), "full: iron_ore 251,133 of max 185,470")
        self.assertIsNone(pull.full_reason(ROUTES["gather-mixed"], "gather-mixed", rec, NOW))      # silver is outside the reserve: its Admiral's call
        self.assertIsNone(pull.full_reason(ROUTES["sell-iron"], "sell-iron", rec, NOW))            # it sells: it earns
        self.assertIsNone(pull.full_reason(ROUTES["mission-iron"], "mission-iron", rec, NOW))      # a mission paid once
        self.assertIsNone(pull.full_reason(ROUTES["hunt-rays"], "hunt-rays", rec, NOW))
        self.assertIsNone(pull.full_reason(ROUTES["unknown-field"], "unknown-field", rec, NOW))    # a field of unknown yield: not judged
        self.assertEqual(pull.full_reason(dict(ROUTES["unknown-field"], min_left={"iron_ore": 10}), "unknown-field", rec, NOW),
                         "full: iron_ore 251,133 of max 185,470")                                   # its floor names what it gathers
        self.assertIsNone(pull.full_reason(ROUTES["craft-steel"], "craft-steel", rec, NOW))        # steel plate is not full
        both = record(full=("iron_ore", "steel_plate"))
        self.assertEqual(pull.full_reason(ROUTES["craft-steel"], "craft-steel", both, NOW), "full: steel_plate 0 of max 10")
        self.assertIsNone(pull.full_reason(ROUTES["gather-iron"], "gather-iron", rec, NOW + 7200))  # the mark's own end came

    def test_the_rule_acts_only_while_its_switch_file_exists_and_its_record_is_in_force(self):
        miner = {"name": "miner-1", "role": "miner", "credits": 20000, "modules": [], "docked": True}
        why = lambda now: dispatch.why_not(miner, "gather-iron", ROUTES["gather-iron"], self.state(now))[0]
        pull.write_record(str(self.data), record())
        self.assertIsNone(why(NOW))                                                       # off: the record is there and closes nothing
        self.switch("fleet/pull-on")
        self.assertEqual(why(NOW + 1), "full: iron_ore 251,133 of max 185,470")
        self.assertIsNone(why(NOW + 2 * 3600))                                            # the record past its end: nothing closed
        (self.data / "routes" / "pull.json").unlink()
        self.assertIsNone(why(NOW + 3))                                                   # no record: nothing closed
        self.assertIsNone(dispatch.why_not(miner, "gather-iron", ROUTES["gather-iron"], self.state(NOW + 4, pull=None))[0])

    def test_the_dispatchers_pass_keeps_the_record_only_with_the_switch_and_a_dry_pass_writes_none(self):
        state = {}
        self.assertEqual(pull.keep(str(self.root), str(self.data), NOW, False, state), [])
        self.assertEqual(state, {"class_guard": False, "pull": None})
        self.assertFalse((self.data / "routes" / "pull.json").exists())
        self.switch("fleet/pull-on")
        self.switch("fleet/class-guard-on")
        state = {}
        lines = pull.keep(str(self.root), str(self.data), NOW + 1, True, state)
        self.assertEqual(lines, ["dry run, not written: pull: iron_ore full: 200 of max 100; routes that only bring it close until it holds less than 90"])
        self.assertTrue(state["class_guard"] and state["pull"]["items"]["iron_ore"]["full"])
        self.assertFalse((self.data / "routes" / "pull.json").exists())
        state = {}
        self.assertEqual(len(pull.keep(str(self.root), str(self.data), NOW + 2, False, state)), 1)
        written = json.loads((self.data / "routes" / "pull.json").read_text())
        self.assertEqual((written["written_at"], written["items"]["iron_ore"]["full"]), (STAMP(NOW + 2), True))
        self.book(50, STAMP(NOW))
        self.assertEqual(pull.keep(str(self.root), str(self.data), NOW + 60, False, {}), [])           # read again only after EVERY seconds
        lines = pull.keep(str(self.root), str(self.data), NOW + 2 + pull.EVERY, False, {})
        self.assertEqual(lines, ["pull: iron_ore open again: 50, below its min 90"])
        (self.data / "routes" / "pull.json").write_text("{not json")
        state = {}
        self.assertEqual(len(pull.keep(str(self.root), str(self.data), NOW + 900, False, state)), 0)   # a bad record is made again
        self.assertIsNotNone(state["pull"])


class DryRunTests(Tree):
    def run_check(self, *args):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": self.temp.name, "FLEET_TAXES": os.devnull}
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "pull.py")] + list(args) + ["--root", str(self.root), "--data", str(self.data),
                                                                                               "--now", STAMP(NOW)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, timeout=120)

    def plans(self):
        for role, owner, ids in (("miner", "Zero", ["gather-iron", "park"]), ("trader", "Mercury", ["gather-iron", "craft-steel", "park"])):
            (self.root / "routes" / "plans" / (role + ".json")).write_text(json.dumps({"role": role, "owner": owner, "routes": ids}), encoding="ascii")
        (self.root / "routes" / "park.json").write_text(json.dumps({"id": "park", "kind": "circuit", "title": "t", "park": True, "stops": [{"at": "home:core:base"}]}))

    def test_the_dry_run_on_an_empty_fleet_file_says_so_and_closes_nothing_harmful(self):
        self.plans()
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"updated_at": STAMP(NOW), "ships": []}))
        done = self.run_check("check")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("the fleet file lists no ship: who would wait is not measured", done.stdout)
        self.assertIn("REFUSED gather-iron", done.stdout)
        self.assertRegex(done.stdout, r"CLOSED  gather-iron +full: iron_ore 200 of max 100\n")
        self.assertFalse((self.data / "routes" / "pull.json").exists())                   # a dry run writes nothing

    def test_the_dry_run_counts_who_starts_and_who_waits_with_both_rules_off_and_on(self):
        self.plans()
        ships = [{"name": name, "status": "connected", "activity": {"kind": "idle"}, "docked": True, "credits": 20000, "cargo_used": 0}
                 for name in ("miner-1", "trader-1", "trader-2")]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"updated_at": STAMP(NOW), "ships": ships}))
        for ship in ships:
            (self.data / "fleet" / "ships" / (ship["name"] + ".json")).write_text(json.dumps({"modules": [], "cargo": []}))
        done = self.run_check("check")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("trader: 2 ships | both rules off: 2 start (2 of them on another class's work, 2 on a route the pull rule closes, 0 on park), 0 wait | "
                      "both on: 2 start (0 on park), 0 wait | no work open, park or wait: 0 off, 0 on (+0)", done.stdout)   # off: they gather iron; on: they craft steel
        self.assertIn("miner: 1 ships | both rules off: 1 start (0 of them on another class's work, 1 on a route the pull rule closes, 0 on park), 0 wait | "
                      "both on: 0 start (0 on park), 1 wait | no work open, park or wait: 0 off, 1 on (+1)", done.stdout)
        self.assertIn("SUM | 3 ships | both rules off: 0 with no work open (park or wait), 2 start on another class's work, 3 on a route the pull rule closes "
                      "| both on: 1 with no work open", done.stdout)
        self.assertEqual(self.run_check("levels").returncode, 0)


if __name__ == "__main__":
    unittest.main()
