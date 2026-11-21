"""The circuit runner's `fit` step swaps a module (`replace`, requests ENT-290), flown whole on the fleet's fake gate
(scripts/tests/test_fleet_route_run.py, FAKE_RUN) with the fitting calls added; and routes.py check reads the field.
No engine, no network.

2026-11-21: the Threshold has one weapon slot and every drone fills it with a Pulse Laser I (10 damage). The fit step
only installed, so a swap took two calls by hand per ship, and one done by hand lost its dock between them.
"""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TESTS = Path(__file__).resolve().parent
FLEET = TESTS.parents[1] / "game" / "fleet"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(TESTS / "test_fleet_route_run.py", "test_fleet_route_run_for_swap")
DOCK_OLD = '''        if body["type"] == "prepare-at-station":
'''
DOCK_NEW = '''        if body["type"] == "prepare-at-station":
            WORLD["docked"] = True
'''
SELL_OLD = '''    if action == "sell":
'''
FITTING = '''    if action == "get_ship":
        return 200, {"structuredContent": {"modules": [{"type_id": t, "module_id": "mod-%d" % n, "slot": "x"} for n, t in enumerate(WORLD["fitted"])]}}
    if action == "uninstall_mod":
        number = int(str(params.get("module_id")).rsplit("-", 1)[-1])
        gone = WORLD["fitted"].pop(number)
        WORLD["cargo"][gone] = WORLD["cargo"].get(gone, 0) + 1
        if WORLD.get("lose_dock"):                              # the dock is lost between the two calls
            WORLD["docked"] = False
        return 200, {"result": "uninstalled " + gone}
    if action == "install_mod":
        wanted = params.get("module_id")
        if WORLD.get("refusals", 0) > 0 or not WORLD.get("docked", True):
            WORLD["refusals"] = WORLD.get("refusals", 0) - 1
            return 200, {"error": {"code": "not_docked", "message": "you must be docked to install modules"}}
        if not WORLD["cargo"].get(wanted) or len(WORLD["fitted"]) >= WORLD.get("slots", 9):
            return 200, {"error": {"code": "no_slot", "message": "no free slot or module not in cargo"}}
        WORLD["cargo"][wanted] -= 1
        WORLD["fitted"].append(wanted)
        return 200, {"result": "installed " + wanted}
'''
SWITCH = '''    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "FIT_REPLACE" and "fit_replace" in CONFIG:
        node = ast.copy_location(ast.parse("FIT_REPLACE = %r" % CONFIG["fit_replace"]).body[0], node)
    keep.append(node)
'''


def fake():
    """FAKE_RUN of the runner's tests with a ship's slots: get_ship, uninstall_mod, install_mod, the dock."""
    text = BASE.FAKE_RUN
    for old in (DOCK_OLD, SELL_OLD, "    keep.append(node)\n"):
        assert text.count(old) == 1, old
    return text.replace(DOCK_OLD, DOCK_NEW).replace(SELL_OLD, FITTING + SELL_OLD).replace("    keep.append(node)\n", SWITCH)


def fly(route, world, **config):
    """(the calls in their order, the world after, the run's row, the one-time rows, the run's output)."""
    base = {"credits": 40000, "cargo": {}, "storage": {}, "book": {}, "jobs": [], "queue": [], "quote": {}, "makes": "", "per_run": 1, "ticks": 1,
            "fuel": 95, "max_fuel": 95, "fitted": ["mining_laser_i", "pulse_laser_i"], "slots": 2, "docked": True}
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        (root / "route.json").write_text(json.dumps(route))
        setup = dict({"world": dict(base, **world), "route": str(root / "route.json"), "data": str(root / "data"), "runner": str(FLEET / "route_run.py"),
                      "log": str(root / "log.json")}, **config)
        (root / "config.json").write_text(json.dumps(setup))
        done = subprocess.run([sys.executable, "-I", "-B", "-c", fake(), str(root / "config.json")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, timeout=120)
        out = json.loads((root / "log.json").read_text())
        rows = [json.loads(line) for line in (root / "data" / "routes" / "runs.jsonl").read_text().splitlines()]
        once = root / "data" / "fleet" / "onetime.json"
        onetime = json.loads(once.read_text()) if once.is_file() else []
    return out["log"], out["world"], rows[-1], onetime, done.stdout


def fitting(log):
    """The calls of the fit step and the dock, in their order."""
    out = []
    for action, params in log:
        if action == "goal" and params in ("prepare-at-station", "buy-items"):
            out.append(params)
        elif action in ("uninstall_mod", "install_mod"):
            out.append("%s %s" % (action, params["module_id"]))
        elif action == "deposit":
            out.append("deposit %d %s" % (params["quantity"], params["item_id"]))
    return out


SWAP = {"module": "pulse_laser_iii", "max_price": 14500, "replace": "pulse_laser_i"}
ROUTE = {"id": "fit-pulse-laser-iii", "kind": "circuit", "title": "t", "stops": [{"at": "home:core:base", "fit": [SWAP]}]}
BOOK = {"pulse_laser_iii": {"best_sell": 14000, "best_sell_qty": 3}}


class SwapTests(unittest.TestCase):
    def test_one_docked_stop_buys_the_new_module_takes_the_old_out_fits_the_new_and_stores_the_old(self):
        log, world, row, onetime, out = fly(ROUTE, {"book": BOOK})
        self.assertEqual(fitting(log), ["prepare-at-station", "buy-items", "uninstall_mod mod-1", "install_mod pulse_laser_iii", "deposit 1 pulse_laser_i"], out)
        self.assertEqual((world["fitted"], world["storage"].get("pulse_laser_i"), world["cargo"].get("pulse_laser_i")),
                         (["mining_laser_i", "pulse_laser_iii"], 1, 0))      # the fault: install_mod into a full slot, nothing swapped
        self.assertEqual((row["notes"], row["one_time"], row["delta"]), ([], -14140, -14140))
        self.assertEqual([r[2:] for r in onetime], [["fit-pulse-laser-iii: pulse_laser_iii bought (tool)", -14140]])   # a tool bought once

    def test_a_buy_that_fails_takes_nothing_out(self):
        log, world, row, onetime, out = fly(ROUTE, {"book": {"pulse_laser_iii": {"best_sell": 15000, "best_sell_qty": 3}}})
        self.assertEqual(fitting(log), ["prepare-at-station"], out)
        self.assertEqual((world["fitted"], row["notes"], onetime), (["mining_laser_i", "pulse_laser_i"], ["pulse_laser_iii: not bought"], []))

    def test_a_dock_lost_between_the_calls_docks_again_and_fits_before_it_leaves(self):
        log, world, row, _onetime, out = fly(ROUTE, {"book": BOOK, "lose_dock": True})
        self.assertEqual(fitting(log), ["prepare-at-station", "buy-items", "uninstall_mod mod-1", "install_mod pulse_laser_iii", "prepare-at-station",
                                        "install_mod pulse_laser_iii", "deposit 1 pulse_laser_i"], out)
        self.assertEqual((world["fitted"], row["notes"]), (["mining_laser_i", "pulse_laser_iii"], []))

    def test_a_module_that_still_does_not_fit_puts_the_old_one_back_else_the_next_stop_fits_it(self):
        log, world, row, _onetime, out = fly(ROUTE, {"book": BOOK, "refusals": 2})
        self.assertEqual(fitting(log)[2:], ["uninstall_mod mod-1", "install_mod pulse_laser_iii", "prepare-at-station", "install_mod pulse_laser_iii",
                                            "install_mod pulse_laser_i"], out)
        self.assertEqual((world["fitted"], row["notes"]), (["mining_laser_i", "pulse_laser_i"], ["pulse_laser_iii: not fitted, pulse_laser_i fitted again"]), out)
        self.assertEqual(world["cargo"].get("pulse_laser_iii"), 1)          # bought and kept aboard: the next run fits it without a buy
        two = dict(ROUTE, stops=[ROUTE["stops"][0], {"at": "home:core:other"}])
        log, world, row, _onetime, out = fly(two, {"book": BOOK, "refusals": 4})
        self.assertEqual(fitting(log)[-3:], ["prepare-at-station", "install_mod pulse_laser_iii", "deposit 1 pulse_laser_i"], out)
        self.assertEqual((world["fitted"], row["notes"]), (["mining_laser_i", "pulse_laser_iii"],
                                                           ["pulse_laser_iii: not fitted, pulse_laser_i out", "pulse_laser_iii: fitted at other"]))

    def test_a_fit_without_replace_flies_as_before_and_the_switch_off_buys_nothing(self):
        plain = dict(ROUTE, stops=[{"at": "home:core:base", "fit": [{"module": "shield_booster_i", "max_price": 3100}]}])
        log, world, row, _onetime, out = fly(plain, {"book": {"shield_booster_i": {"best_sell": 3000, "best_sell_qty": 2}}, "slots": 3})
        self.assertEqual(fitting(log), ["prepare-at-station", "buy-items", "install_mod shield_booster_i"], out)
        self.assertNotIn("get_ship", [action for action, _params in log])   # the old step reads the live file, as before
        self.assertEqual(row["notes"], [])
        log, world, row, onetime, out = fly(ROUTE, {"book": BOOK}, fit_replace=False)
        self.assertEqual((fitting(log), world["fitted"], onetime), (["prepare-at-station"], ["mining_laser_i", "pulse_laser_i"], []), out)
        self.assertEqual(row["notes"], ["pulse_laser_iii: replace off"])


class GateTests(unittest.TestCase):
    def test_the_gate_reads_a_fit_entry_and_its_replace(self):
        routes = load(FLEET / "routes.py", "routes_under_test_swap")
        self.assertTrue(hasattr(routes, "fit_faults"))
        self.assertEqual(routes.fit_faults(SWAP), [])
        self.assertEqual(routes.fit_faults({"module": "ice_harvester_i", "max_price": 1500}), [])
        self.assertEqual(routes.fit_faults({"module": "ice_harvester"}), [])                       # without `replace`: as before r22
        self.assertIn("needs `module`", routes.fit_faults({"max_price": 10, "replace": "pulse_laser_i"})[0])
        self.assertIn("needs `max_price`", routes.fit_faults({"module": "x", "replace": "pulse_laser_i"})[0])
        for wrong in ("pulse_laser_iii", "", 7):
            self.assertIn("`replace` names the module", routes.fit_faults(dict(SWAP, replace=wrong))[0])


if __name__ == "__main__":
    unittest.main()
