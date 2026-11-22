"""Requests ENT-343, ENT-344 and ENT-345 (2026-11-22): a module list in `requires.module`, the fit gate warning,
several receivers at one station, the shipping reads, and the ammunition of a fitted weapon kept aboard a hunt.
On disposable trees; no engine, no network."""

import ast
import calendar
import glob
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
sys.path.insert(0, str(FLEET))
import handover                                   # noqa: E402  the module under test
import workclass                                  # noqa: E402  its switch


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_r25_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hunt_function(name):
    """hunt.py flies a hunt when loaded: take one top-level function out of its syntax tree."""
    path = FLEET / "hunt.py"
    found = [n for n in ast.parse(path.read_text(encoding="utf-8")).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if not found:
        raise AssertionError("hunt.py has no top-level function %s" % name)
    space = {"calendar": calendar, "glob": glob, "json": json, "os": os, "time": time}
    exec(compile(ast.Module(body=found, type_ignores=[]), str(path), "exec"), space)
    return space[name]


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-r25-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in (self.root / "routes" / "plans", self.root / "map", self.data / "fleet" / "orders", self.data / "routes"):
            folder.mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text("# chart\nhome\tHome\t0\t0\tvoidborn\n", encoding="ascii")
        self.routes_files = {
            "gather": {"id": "gather", "kind": "mine", "title": "t", "belt": "home:belt", "station": "home:core:base",
                       "requires": {"module": ["mining_laser_i", "mining_laser_iii"]}},
            "gather-old": {"id": "gather-old", "kind": "mine", "title": "t", "belt": "home:belt2", "station": "home:core:base",
                           "requires": {"module": "mining_laser_i"}},
            "fit-laser": {"id": "fit-laser", "kind": "circuit", "title": "t", "stops": [
                {"at": "home:core:base", "fit": [{"module": "mining_laser_iii", "max_price": 9000, "replace": "mining_laser_i"}]}]},
        }
        for rid, route in self.routes_files.items():
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps(route), encoding="ascii")
        (self.root / "routes" / "plans" / "miner.json").write_text(json.dumps({"role": "miner", "owner": "Zero", "routes": ["fit-laser", "gather", "gather-old"]}), encoding="ascii")
        self.dispatch, self.routes = load("dispatch"), load("routes")

    def why(self, rid, modules):
        pilot = {"name": "miner-1", "credits": 20000, "modules": list(modules), "docked": True}
        state = {"now": time.time(), "data": str(self.data), "rows": [], "orders": {}, "rest": {}, "booked": {}}
        return self.dispatch.why_not(pilot, rid, self.dispatch.load_routes(self.root)[rid], state)[0]


class ModuleListTests(Tree):
    """requests ENT-343 (1), errors.log ENT-128: an exact module id shut 17 Laser III miners out of every gather."""

    def test_a_list_opens_to_any_one_of_its_modules(self):
        self.assertIsNone(self.why("gather", ["mining_laser_iii"]))
        self.assertIsNone(self.why("gather", ["mining_laser_i", "pulse_laser_i"]))
        self.assertEqual(self.why("gather", ["pulse_laser_i"]), "needs one of mining_laser_i, mining_laser_iii")
        self.assertEqual(self.why("gather-old", ["mining_laser_iii"]), "needs mining_laser_i")     # a word stays one exact module

    def test_the_route_gate_takes_a_list_and_refuses_an_empty_one(self):
        errors, _count = self.routes.check(str(self.root))
        self.assertFalse([e for e in errors if "requires.module" in e], errors)
        (self.root / "routes" / "gather.json").write_text(json.dumps(dict(self.routes_files["gather"], requires={"module": []})), encoding="ascii")
        errors, _count = self.routes.check(str(self.root))
        self.assertTrue(any("game/routes/gather.json" in e and "requires.module" in e for e in errors), errors)

    def test_the_index_names_the_list(self):
        self.assertIn("needs mining_laser_i or mining_laser_iii", self.routes.open_to(self.routes_files["gather"]))


class FitGateTests(Tree):
    """requests ENT-343 (2): a fit route that replaces module M beside a route of the same plan that asks M."""

    def test_the_refit_is_named_where_a_route_of_its_plan_asks_the_old_module(self):
        found = self.routes.fit_gate_warnings(str(self.root), self.routes.routes_of(str(self.root))[0])
        self.assertEqual(found, [("fit-laser", "miner", "gather-old", "mining_laser_i")])    # the list route takes the new laser

    def test_another_refit_of_the_same_module_is_no_warning(self):
        other = {"id": "fit-other", "kind": "circuit", "title": "t", "requires": {"module": "mining_laser_i"}, "stops": [
            {"at": "home:core:base", "fit": [{"module": "mining_laser_ii", "max_price": 5000, "replace": "mining_laser_i"}]}]}
        (self.root / "routes" / "fit-other.json").write_text(json.dumps(other), encoding="ascii")
        (self.root / "routes" / "plans" / "miner.json").write_text(json.dumps({"role": "miner", "owner": "Zero", "routes": ["fit-laser", "fit-other"]}), encoding="ascii")
        self.assertEqual(self.routes.fit_gate_warnings(str(self.root), self.routes.routes_of(str(self.root))[0]), [])

    def test_no_warning_when_no_route_asks_the_old_module(self):
        (self.root / "routes" / "plans" / "miner.json").write_text(json.dumps({"role": "miner", "owner": "Zero", "routes": ["fit-laser", "gather"]}), encoding="ascii")
        self.assertEqual(self.routes.fit_gate_warnings(str(self.root), self.routes.routes_of(str(self.root))[0]), [])


class SeveralReceiversTests(unittest.TestCase):
    """requests ENT-344 (2): several hauler receivers at one station, so the miners' gifts feed more crafters."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-r25-handover-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet").mkdir()
        ships = [{"name": "hauler-%d" % n} for n in range(1, 6)] + [{"name": "miner-%d" % n} for n in range(1, 41)]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))
        (self.data / "fleet" / "flagships.json").write_text("{}")
        (self.data / "fleet" / "receivers.json").write_text(json.dumps({"hauler": {"node_beta": ["hauler-1", "hauler-2", "hauler-3"], "*": "hauler-5"}}))
        (self.data / "fleet" / "strict-classes-on").write_text("")
        workclass.SEEN.clear()
        self.addCleanup(workclass.SEEN.clear)

    def test_the_givers_are_spread_over_the_receivers_and_each_keeps_its_own(self):
        got = {handover.receiver("hauler", "node_beta", str(self.data), "miner-%d" % n)[0] for n in range(1, 41)}
        self.assertEqual(got, {"hauler-1", "hauler-2", "hauler-3"})
        first = handover.receiver("hauler", "node_beta", str(self.data), "miner-7")
        self.assertEqual(handover.receiver("hauler", "node_beta", str(self.data), "miner-7"), first)
        self.assertEqual(handover.receiver("hauler", "far", str(self.data), "miner-7"), ("hauler-5", ""))

    def test_a_receiver_of_the_list_never_gives_to_itself_and_a_stranger_is_left_out(self):
        (self.data / "fleet" / "receivers.json").write_text(json.dumps({"hauler": {"node_beta": ["hauler-1", "Stranger"]}}))
        self.assertEqual(handover.receiver("hauler", "node_beta", str(self.data), "miner-3"), ("hauler-1", ""))
        self.assertIsNone(handover.receiver("hauler", "node_beta", str(self.data), "hauler-1")[0])

    def test_add_puts_one_more_receiver_at_the_station(self):
        os.environ["HERMES_SESSION_PROFILE"] = "apollo"
        try:
            self.assertEqual(handover.main(["receivers", "add", "hauler", "node_beta", "hauler-4", "--data", str(self.data)]), 0)
            self.assertEqual(handover.receivers(str(self.data))["hauler"]["node_beta"], ["hauler-1", "hauler-2", "hauler-3", "hauler-4"])
            self.assertEqual(handover.main(["receivers", "add", "hauler", "far", "hauler-4", "--data", str(self.data)]), 0)
            self.assertEqual(handover.receivers(str(self.data))["hauler"]["far"], ["hauler-4"])
        finally:
            os.environ.pop("HERMES_SESSION_PROFILE", None)


class ShippingReadsTests(unittest.TestCase):
    """requests ENT-344 (3): the freight board read by a hauler on a run (OpenAPI /shipping: these four only view)."""

    def test_the_shipping_reads_are_reads_and_its_commands_are_not(self):
        gate = load("gate")
        self.assertEqual([gate.is_read(a) for a in ("list_all", "profile", "track", "active", "list", "quote", "accept", "post", "deliver", "pay_debt")],
                         [True, True, True, True, True, True, False, False, False, False])


class FittedAmmoTests(unittest.TestCase):
    """requests ENT-345 (2): a Plasma Cannon II ship stored its 3 plasma packs while its magazine was empty."""

    ITEMS = [{"id": "plasma_cannon_ii", "type": "weapon", "ammo_type": "plasma"},
             {"id": "dispersal_plasma_cell_pack", "category": "ammo", "effect": {"type": "ammo", "subtype": "plasma"}},
             {"id": "iron_slug_case", "category": "ammo", "effect": {"type": "ammo", "subtype": "kinetic"}},
             {"id": "ember_gland", "category": "loot"}]

    def test_an_empty_magazine_keeps_the_packs_its_weapon_fires(self):
        fitted_ammo = handover.fitted_ammo
        modules = [{"type_id": "plasma_cannon_ii", "magazine_size": 80, "current_ammo": 0}, {"type_id": "pulse_laser_i"}]
        self.assertEqual(fitted_ammo(modules, self.ITEMS), {"dispersal_plasma_cell_pack"})
        self.assertEqual(fitted_ammo([{"type_id": "x", "loaded_ammo_id": "iron_slug_case"}], self.ITEMS), {"iron_slug_case"})
        self.assertEqual(fitted_ammo([{"type_id": "plasma_cannon_ii"}], []), set())                 # no catalog: the loaded id only

    def test_the_newest_catalog_copy_is_read(self):
        catalog_items = handover.catalog_items
        with tempfile.TemporaryDirectory() as folder:
            for name, items in (("0.723.2.json", [{"id": "old"}]), ("0.732.0.json", [{"id": "new"}]), ("ammo.json", ["x"])):
                Path(folder, name).write_text(json.dumps({"items": items} if name[0].isdigit() else items))
            self.assertEqual(catalog_items(folder), [{"id": "new"}])
            self.assertEqual(catalog_items(os.path.join(folder, "none")), [])


if __name__ == "__main__":
    unittest.main()
