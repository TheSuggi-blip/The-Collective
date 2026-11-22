"""Fuel before a hunt (requests ENT-369, Apophis; errors.log ENT-142): game/fleet/fuelplan.py's rules, the notes hunt.py
writes when its sell_at sells no fuel or its tank is short before it sets out, and the dispatcher's rest of that
(route, pilot) at once. No engine, no network."""

import ast
import calendar
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
import dispatch          # noqa: E402
import fuelplan          # noqa: E402

LANES = {"a": ["b"], "b": ["a", "c"], "c": ["b", "d"], "d": ["c"]}


class FuelPlanTests(unittest.TestCase):
    def test_the_way_counts_both_legs_and_a_short_tank_is_short(self):
        self.assertEqual(fuelplan.way(LANES, "a", "c"), 2)
        self.assertEqual(fuelplan.way(LANES, "a", "d", "b"), 5)
        self.assertIsNone(fuelplan.way(LANES, "a", "zz"))
        self.assertTrue(fuelplan.fuel_short(4, 5))          # the hunter at GSC-0005 held 4
        self.assertFalse(fuelplan.fuel_short(95, 5))
        self.assertFalse(fuelplan.fuel_short(None, 5))      # an unread tank is not judged

    def test_a_station_that_answered_with_no_fuel_is_passed_over(self):
        stations = {"b": ("pb", "base_b"), "d": ("pd", "base_d")}
        self.assertEqual(fuelplan.nearest_fuel(LANES, "a", stations)[3], "base_b")
        self.assertEqual(fuelplan.nearest_fuel(LANES, "a", stations, skip={"base_b"})[3], "base_d")
        self.assertIsNone(fuelplan.nearest_fuel(LANES, "a", stations, skip={"base_b", "base_d"}))

    def test_a_tank_under_half_after_a_refuel_means_the_station_sold_none(self):
        self.assertTrue(fuelplan.refuelled_short(9, 100))
        self.assertFalse(fuelplan.refuelled_short(95, 100))
        self.assertFalse(fuelplan.refuelled_short(None, 100))

    def test_fuel_stations_reads_the_refuel_service(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "scouting").mkdir()
            (Path(folder) / "scouting" / "levy.json").write_text(json.dumps({"pois": {"p1": {
                "poi": {"id": "p1"}, "base": {"id": "levy_base", "services": ["refuel", "market"]}}}}))
            (Path(folder) / "scouting" / "dry.json").write_text(json.dumps({"pois": {"p2": {
                "poi": {"id": "p2"}, "base": {"id": "dry_base", "services": ["market"]}}}}))
            self.assertEqual(fuelplan.fuel_stations(folder), {"levy": ("p1", "levy_base")})


def row(notes, minutes=12.0, ago=60, route="hunt-far", pilot="d-1"):
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - ago - minutes * 60))
    return {"route": route, "pilot": pilot, "kind": "hunt", "started": started, "minutes": minutes, "delta": 0, "notes": notes}


class DispatchRestTests(unittest.TestCase):
    def test_a_hunt_whose_sell_at_sold_no_fuel_rests_for_its_pilot_at_once(self):
        rows = [row([dispatch.NO_FUEL_AT_SELL + " the_levy: tank 9/100"])]
        why = dispatch.stalled_reason("hunt-far", {"kind": "hunt"}, "d-1", rows, time.time())
        self.assertIsNotNone(why)
        self.assertIn("fuel", why)
        self.assertIsNone(dispatch.stalled_reason("hunt-far", {"kind": "hunt"}, "d-2", rows, time.time()))   # another pilot: open

    def test_a_hunt_not_flown_for_fuel_rests_at_once_and_a_plain_run_does_not(self):
        rows = [row(["fuel 4 short for gsc_0005 and on to fuel" + dispatch.FUEL_NOT_FLOWN], minutes=0.5)]
        self.assertIsNotNone(dispatch.stalled_reason("hunt-far", {"kind": "hunt"}, "d-1", rows, time.time()))
        self.assertIsNone(dispatch.stalled_reason("hunt-far", {"kind": "hunt"}, "d-1", [row(["ranch floor kept"])], time.time()))

    def test_the_rest_ends_after_its_time(self):
        rows = [row([dispatch.NO_FUEL_AT_SELL + " the_levy: tank 9/100"], ago=dispatch.STALL_REST + 60)]
        self.assertIsNone(dispatch.stalled_reason("hunt-far", {"kind": "hunt"}, "d-1", rows, time.time()))


def load_fuel_first(world):
    """hunt.py's fuel_first, taken out of its syntax tree, on a stub world: {'here', 'fuel', 'size', 'gives': {base: fuel}}."""
    tree = ast.parse((FLEET / "hunt.py").read_text(encoding="utf-8"))
    found = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "fuel_first"]
    calls = []

    def goal(kind, options):
        calls.append(("goal", options.get("baseId")))
        world["here"] = {"base_b": "b", "base_d": "d"}.get(options.get("baseId"), world["here"])
        world["fuel"] = max(world["fuel"], world["gives"].get(options.get("baseId"), 0))
        return True

    space = {"fuelplan": fuelplan, "dispatch": dispatch, "system_id": "d", "sell_at": ["a", "pa", "base_a"],
             "tank": lambda: (world["fuel"], world["size"]), "ship_system": lambda: world["here"], "say": lambda text: None,
             "goal": goal, "raw": lambda *a, **k: calls.append(("raw",) + a) or {}}
    exec(compile(ast.Module(body=found, type_ignores=[]), "hunt.py", "exec"), space)
    return space["fuel_first"], calls


class FuelFirstTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        game, data = Path(self.folder.name) / "game", Path(self.folder.name) / "data"
        (game / "map").mkdir(parents=True)
        (game / "map" / "galaxy.tsv").write_text("id\tlanes\tjumps_from_home\tflags\na\tb\t0\t\nb\ta,c\t1\t\nc\tb,d\t2\t\nd\tc\t3\t\n")
        (data / "scouting").mkdir(parents=True)
        for system, base in (("b", "base_b"), ("d", "base_d")):
            (data / "scouting" / (system + ".json")).write_text(json.dumps({"pois": {"p": {"poi": {"id": "p" + system}, "base": {"id": base, "services": ["refuel"]}}}}))
        self.game, self.data = str(game), str(data)

    def test_a_tank_that_holds_the_way_sets_out_at_once(self):
        first, calls = load_fuel_first({"here": "a", "fuel": 60, "size": 95, "gives": {}})
        self.assertIsNone(first(self.game, self.data))
        self.assertEqual(calls, [])

    def test_a_short_tank_takes_fuel_at_the_nearest_station_first(self):
        first, calls = load_fuel_first({"here": "a", "fuel": 9, "size": 95, "gives": {"base_b": 95}})
        self.assertIsNone(first(self.game, self.data))
        self.assertEqual(calls[0], ("goal", "base_b"))

    def test_a_station_with_no_fuel_is_passed_over_and_then_the_hunt_is_not_flown(self):
        first, calls = load_fuel_first({"here": "a", "fuel": 9, "size": 95, "gives": {}})   # no station gives fuel (The Levy, 2026-11-22)
        note = first(self.game, self.data)
        self.assertTrue(note.endswith(dispatch.FUEL_NOT_FLOWN), note)
        self.assertEqual([c[1] for c in calls if c[0] == "goal"], ["base_b", "base_d"])

    def test_a_tank_about_full_flies_as_before(self):
        first, calls = load_fuel_first({"here": "a", "fuel": 90, "size": 95, "gives": {}})
        self.assertIsNone(first(self.game, self.data))


class HuntWritesTheNotesTests(unittest.TestCase):
    def test_hunt_py_uses_the_dispatcher_s_own_words(self):
        text = (FLEET / "hunt.py").read_text(encoding="utf-8")
        ast.parse(text)
        self.assertIn("dispatch.NO_FUEL_AT_SELL", text)
        self.assertIn("dispatch.FUEL_NOT_FLOWN", text)
        self.assertIn("fuelplan.fuel_short", text)


if __name__ == "__main__":
    unittest.main()
