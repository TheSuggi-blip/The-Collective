"""game/fleet/route_run.py and hunt.py run their stops at module level: what must hold there. Read from the source, no engine."""

import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def rebound(path):
    """The functions of a script whose name is given another value at module level (inside no function)."""
    tree = ast.parse(path.read_text(encoding="ascii"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    stored = set()

    def walk(node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            return                                                       # another scope
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            return                                                       # a comprehension keeps its names to itself
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            stored.add(node.id)
        for child in ast.iter_child_nodes(node):
            walk(child)

    for node in tree.body:
        walk(node)
    return sorted(functions & stored)


class ModuleLevelTests(unittest.TestCase):
    def test_no_step_gives_a_functions_name_another_value(self):
        # 2026-11-16: the accept step bound `offer`, the function the buy and fit steps call; every run with a buy after an accept crashed
        for script in ("route_run.py", "hunt.py"):
            self.assertEqual(rebound(FLEET / script), [], script)

    def test_a_run_that_crashes_still_writes_its_row(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        tree = ast.parse(source)
        self.assertIn("sys.excepthook = crashed", source)
        self.assertIn("atexit.register(finish)", source)
        last = tree.body[-1]
        self.assertTrue(isinstance(last, ast.Expr) and isinstance(last.value, ast.Call) and getattr(last.value.func, "id", "") == "finish")
        finish = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "finish")
        self.assertIn("notes.extend(CRASH)", ast.unparse(finish))
        self.assertIn("runs.jsonl", ast.unparse(finish))

    def test_the_row_of_a_crashed_run_carries_the_error(self):
        # the two functions as they stand in the script, run in a made-up run that ends in an exception
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        tree = ast.parse(source)
        parts = [ast.get_source_segment(source, node) for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ("crashed", "finish")]
        with tempfile.TemporaryDirectory() as folder:
            driver = "\n\n".join([
                "import atexit, fcntl, json, pathlib, sys, time, traceback",
                "DATA = pathlib.Path(%r)" % folder,
                "ROUTE = {'id': 'made-up', 'kind': 'circuit', 'stops': [1, 2]}",
                "pilot, started, before, done, onetime, notes, reached, skipped = 'trader-1', time.time() - 120, 5000, [], [0], ['a note'], 1, 0",
                "CRASH, FINISHED = [], []",
                "credits = lambda: 4900"] + parts + [
                "sys.excepthook = crashed", "atexit.register(finish)", "offer = None", "offer('book')"])
            done = subprocess.run([sys.executable, "-I", "-B", "-c", driver], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
            self.assertIn("TypeError", done.stderr)                      # Python still prints the fault
            rows = [json.loads(line) for line in (Path(folder) / "routes" / "runs.jsonl").read_text().splitlines()]
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0]["route"], rows[0]["stops"], rows[0]["of"], rows[0]["delta"]), ("made-up", 1, 2, -100))
        self.assertEqual(rows[0]["notes"][0], "a note")
        self.assertTrue(rows[0]["notes"][1].startswith("crashed: TypeError: 'NoneType' object is not callable"), rows[0]["notes"])


class EmptyRunTests(unittest.TestCase):
    def test_a_run_whose_every_stop_was_skipped_says_so_in_its_row(self):
        # requests ENT-129: a once route for pilots that hold its mission gave every other pilot a run of 0 minutes booked as done
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        tree = ast.parse(source)
        parts = [ast.get_source_segment(source, node) for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ("crashed", "finish")]
        for skipped, stops, expect in ((2, 2, True), (1, 2, False)):
            with tempfile.TemporaryDirectory() as folder:
                driver = "\n\n".join([
                    "import atexit, fcntl, json, pathlib, sys, time, traceback",
                    "DATA = pathlib.Path(%r)" % folder,
                    "ROUTE = {'id': 'made-up', 'kind': 'circuit', 'stops': %r}" % list(range(stops)),
                    "pilot, started, before, done, onetime, notes, reached, skipped = 'trader-1', time.time(), 5000, [], [0], [], %d, %d" % (stops, skipped),
                    "CRASH, FINISHED = [], []",
                    "credits = lambda: 5000"] + parts + ["finish()"])
                subprocess.run([sys.executable, "-I", "-B", "-c", driver], check=True, timeout=60)
                row = json.loads((Path(folder) / "routes" / "runs.jsonl").read_text().splitlines()[0])
            self.assertEqual("every stop skipped" in row["notes"], expect, row)
        loop = next(node for node in tree.body if isinstance(node, ast.For) and "only_if_active" in ast.unparse(node))
        self.assertIn("skipped += 1", ast.unparse(loop))


class HuntStepTests(unittest.TestCase):
    def test_the_hunt_step_hands_its_hold_to_hunt_py(self):
        # 2026-11-16: a circuit started by an Admiral's hand wrote its order file `circuit <id>`; its hunt step started hunt.py
        # without FLEET_HOLD, so division.may refused hunt.py (`busy: circuit ...`) and the run ended "objectives not done"
        # after the accept. Under the dispatcher FLEET_HOLD was set and the step ran.
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        tree = ast.parse(source)
        hunts = [node for node in ast.walk(tree) if isinstance(node, ast.For) and "'hunt'" in ast.unparse(node.iter)]
        self.assertEqual(len(hunts), 1)
        calls = [node for node in ast.walk(hunts[0]) if isinstance(node, ast.Call) and ast.unparse(node.func) == "subprocess.run"]
        self.assertEqual(len(calls), 1)
        env = [kw for kw in calls[0].keywords if kw.arg == "env"]
        self.assertEqual(len(env), 1, "the hunt step passes no env: hunt.py cannot tell the run's own order from another program's")
        self.assertIn("FLEET_HOLD", ast.unparse(env[0].value))
        self.assertIn("'circuit ' + ROUTE['id']", ast.unparse(env[0].value))
        self.assertIn("order('circuit ' + ROUTE['id'])", source)             # the hold it hands down is the order it wrote


def functions(*names):
    """The named functions of route_run.py, run on stubs: the runner's steps run at module level, so it is not imported."""
    source = (FLEET / "route_run.py").read_text(encoding="ascii")
    tree = ast.parse(source)
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    space = {"re": __import__("re"), "json": __import__("json")}
    exec(compile(ast.Module(body=found, type_ignores=[]), "route_run.py", "exec"), space)
    return space


class BattleAndHuntWordTests(unittest.TestCase):
    def test_a_goal_refused_in_battle_sets_the_stance_flee_and_tries_again(self):
        space = functions("goal", "free_from_battle")
        calls, answers = [], [(200, {"success": False, "message": "Cannot travel: in_battle"}), (200, {"success": True, "message": "ok"})]
        space.update(P="drone-1", say=lambda text: None, time=type("T", (), {"sleep": staticmethod(lambda s: None)}),
                     call=lambda method, path, body=None, timeout=900: answers.pop(0),
                     raw=lambda action, params=None, group="spacemolt": calls.append((action, params, group)) or {"structuredContent": {"is_participant": False}},
                     body=lambda d: d.get("structuredContent") or {})
        self.assertEqual(space["goal"]("go-to-poi", {}), (True, "ok"))
        self.assertEqual(calls[0], ("stance", {"stance": "flee"}, "spacemolt_battle"))
        self.assertEqual(calls[1][0], "status")

    def test_the_hunt_step_s_last_word_goes_into_the_run_row_without_the_pilot(self):
        said = functions("step_said")["step_said"]
        self.assertEqual(said("go-to-poi ok\nSTEP drone-1: kills 0 in 15 min at belt | goods {} | lowest hull 100% | left: a ship that is not ours was at the place"),
                         "kills 0 in 15 min at belt | goods {} | lowest hull 100% | left: a ship that is not ours was at the place")
        self.assertEqual(said("REFUSED: drone-1 is busy\n"), "REFUSED: drone-1 is busy")
        self.assertEqual(said(""), "no output")
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertIn("objectives not done; the step said: {said}; the ship stood at {where_now()}", source)


class StoreStepTests(unittest.TestCase):
    def test_store_all_names_everything_aboard(self):
        # 2026-11-16: the once routes of First Hunt and First Steps left their loot and their ore aboard (carapace, meat,
        # carbon, lead ...); a few units closed every route with `requires.empty_hold` to the pilot. `store: "all"` at a
        # stop moves every good aboard into the pilot's storage there.
        pick = functions("store_list")["store_list"]
        hold = {"creature_carapace": 7, "raw_xeno_meat": 3, "lead_ore": 0}
        self.assertEqual(pick("all", hold), ["creature_carapace", "raw_xeno_meat"])
        self.assertEqual(pick(["raw_xeno_meat", "carbon_ore"], hold), ["raw_xeno_meat"])
        self.assertEqual(pick(None, hold), [])
        self.assertEqual(pick("all", {}), [])

    def test_store_all_keeps_the_ammunition_of_a_fitted_weapon_aboard(self):
        # Apophis, requests ENT-352: a give route's `store: "all"` put a Plasma Cannon II ship's 2 plasma packs into
        # its storage at The Experiment; hunt.py keeps them aboard since c3a8f585. The circuit stop keeps them too.
        sys.path.insert(0, str(FLEET))                                                  # route_run.py puts its folder there itself
        self.addCleanup(sys.path.remove, str(FLEET))
        space = functions("store_list", "aboard_ammo")
        pick = space["store_list"]
        hold = {"dispersal_plasma_cell_pack": 2, "creature_carapace": 7, "iron_slug_case": 4}
        with tempfile.TemporaryDirectory() as folder:
            data = Path(folder)
            (data / "catalog").mkdir()
            (data / "catalog" / "ammo.json").write_text(json.dumps(["dispersal_plasma_cell_pack", "iron_slug_case"]))
            (data / "catalog" / "0.732.0.json").write_text(json.dumps({"items": [
                {"id": "plasma_cannon_ii", "type": "weapon", "ammo_type": "plasma"},
                {"id": "dispersal_plasma_cell_pack", "category": "ammo", "effect": {"type": "ammo", "subtype": "plasma"}},
                {"id": "iron_slug_case", "category": "ammo", "effect": {"type": "ammo", "subtype": "kinetic"}}]}))
            calls = []
            space.update(DATA=data, body=lambda d: d, raw=lambda action, params=None, group="spacemolt": calls.append(action) or
                         {"modules": [{"type_id": "plasma_cannon_ii", "magazine_size": 80, "current_ammo": 0}]})
            keep = space["aboard_ammo"](hold)
            self.assertEqual(keep, {"dispersal_plasma_cell_pack"})                       # the slugs fit no weapon aboard
            self.assertEqual(pick("all", hold, keep), ["creature_carapace", "iron_slug_case"])
            self.assertEqual(pick(["dispersal_plasma_cell_pack"], hold, keep), ["dispersal_plasma_cell_pack"])  # named: stored
            self.assertEqual(space["aboard_ammo"]({"creature_carapace": 7}), set())
            self.assertEqual(calls, ["get_ship"])                                          # no ammunition aboard: no call

    def test_the_store_step_uses_store_list(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertIn("for item in store_list(stop.get('store'), hold, keep):", source)


class StoreFactionStepTests(unittest.TestCase):
    # 2026-11-17: our outpost at GSC-0044 takes goods into its faction storage only (it serves members, no personal
    # trade), and its fuel bunker is supplied the same way; the miners around it and the haulers that supply it need a
    # stop that moves the hold into the faction store there (admirals.log ENT-049, orders.log ENT-042 block APOLLO (2)).
    def test_store_faction_moves_the_hold_into_faction_storage(self):
        route = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [{"at": "wild:outpost:base", "store_faction": "all"}]}
        log, world, row, out = fly(route, {"cargo": {"fuel_cell": 20, "iron_ore": 5}})
        deposits = [params for action, params in log if action == "deposit"]
        self.assertEqual(deposits, [
            {"item_id": "fuel_cell", "quantity": 20, "target": "faction", "source": "cargo"},
            {"item_id": "iron_ore", "quantity": 5, "target": "faction", "source": "cargo"}], out)

    def test_store_faction_names_only_what_is_aboard_and_store_stays_personal(self):
        route = {"id": "made-up", "kind": "circuit", "title": "t",
                 "stops": [{"at": "wild:outpost:base", "store": ["iron_ore"], "store_faction": ["fuel_cell", "carbon_ore"]}]}
        log, world, row, out = fly(route, {"cargo": {"fuel_cell": 3, "iron_ore": 4}})
        deposits = [(params["item_id"], params["target"]) for action, params in log if action == "deposit"]
        self.assertEqual(deposits, [("iron_ore", "self"), ("fuel_cell", "faction")], out)


class BunkerStepTests(unittest.TestCase):
    # 2026-11-17: our outpost's fuel bunker takes fuel only from a ship's tank (`deposit` item_id fuel, target faction);
    # fuel cells stored there stay items. One hauler filled it by script: 64 cells burnt into its tank four at a time and
    # the tank above 15 deposited, 1,292 fuel into the reserve (guidebook logistics.md section 15.3). The orders want it
    # kept by a route (requests.log ENT-251, ENT-252) and the burn of carried cells as a step of its own (ENT-255).
    BUNKER = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [{"at": "wild:outpost:base", "bunker": {"keep": 25}}]}

    def test_the_bunker_step_burns_every_cell_and_leaves_the_keep_in_the_tank(self):
        log, world, row, out = fly(self.BUNKER, {"cargo": {"fuel_cell": 65}, "fuel": 87})
        self.assertEqual(world["cargo"].get("fuel_cell"), 0, out)
        self.assertEqual(world["fuel"], 25, out)
        self.assertEqual(world["reserve"], 65 * 20 + 95 - 25, out)       # docked with refuel the tank stood full: 70 above the keep
        self.assertIn("bunker +1370 fuel from 65 cells, reserve 1370", "; ".join(row["notes"]), out)

    def test_the_bunker_step_burns_whole_cells_in_one_call_and_never_into_less_room_than_a_cell(self):
        log, world, row, out = fly(self.BUNKER, {"cargo": {"fuel_cell": 10}})
        burns = [params for action, params in log if action == "refuel"]
        self.assertTrue(burns, out)
        self.assertTrue(all(p["item_id"] == "fuel_cell" and p["quantity"] >= 1 for p in burns), burns)
        self.assertEqual(sum(p["quantity"] for p in burns), 10, burns)
        self.assertLessEqual(len(burns), 4, burns)                       # 70 of room after the first deposit takes 3 cells at once
        fuel_deposits = [params for action, params in log if action == "deposit" and params["item_id"] == "fuel"]
        self.assertTrue(all(p["target"] == "faction" for p in fuel_deposits), fuel_deposits)

    def test_a_refused_deposit_ends_the_step_and_says_so(self):
        log, world, row, out = fly(self.BUNKER, {"cargo": {"fuel_cell": 5}, "bunker_refuses": True})
        fuel_deposits = [params for action, params in log if action == "deposit" and params["item_id"] == "fuel"]
        self.assertEqual(len(fuel_deposits), 1, out)
        self.assertIn("bunker: deposit refused", "; ".join(row["notes"]), out)

    def test_a_stop_without_cells_and_a_tank_at_the_keep_does_nothing(self):
        route = {"id": "made-up", "kind": "circuit", "title": "t",
                 "stops": [{"at": "wild:outpost:base", "refuel": False, "bunker": {"keep": 25}}]}
        log, world, row, out = fly(route, {"fuel": 20})
        self.assertFalse([a for a, p in log if a in ("refuel", "deposit")], out)
        self.assertEqual(world["fuel"], 20, out)


class BurnCellsStepTests(unittest.TestCase):
    # The same saving on the road (requests.log ENT-255 (3)): a ship that carries cells (100 cr for 20 fuel, about 5 cr a
    # unit) fills its tank from them instead of a station's fuel (12 to 15 cr a unit all-in): `refuel: false` docks
    # without the station's fuel, `burn_cells` burns as many whole cells as the tank has room for.
    def test_a_stop_with_refuel_false_docks_without_the_station_s_fuel(self):
        route = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [{"at": "home:core:base", "refuel": False}]}
        log, world, row, out = fly(route, {"fuel": 40})
        self.assertEqual(world["refuel_asked"], [False], out)
        self.assertEqual(world["fuel"], 40, out)

    def test_every_other_stop_still_refuels_at_the_station(self):
        route = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [{"at": "home:core:base"}]}
        log, world, row, out = fly(route, {"fuel": 40})
        self.assertEqual(world["refuel_asked"], [True], out)

    def test_burn_cells_fills_the_tank_from_the_cells_aboard_by_whole_cells(self):
        route = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [{"at": "home:core:base", "refuel": False, "burn_cells": True}]}
        log, world, row, out = fly(route, {"fuel": 40, "cargo": {"fuel_cell": 5}})
        self.assertEqual([p["quantity"] for a, p in log if a == "refuel"], [2], out)   # 55 of room: two whole cells
        self.assertEqual((world["fuel"], world["cargo"]["fuel_cell"]), (80, 3), out)


class WithdrawStepTests(unittest.TestCase):
    # 2026-11-16: about 14,000 water ice lay in miners' storage at stations whose bids regain slowly (requests.log
    # ENT-117); storage is personal, so only the pilot that stored a load can sell it. A stop's `withdraw` takes it
    # from the pilot's storage into the hold, before the stop's sale: sold where it lies, or carried to the next stop.
    def test_withdraw_takes_no_more_than_storage_hold_and_qty(self):
        units = functions("withdraw_units")["withdraw_units"]
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, None, {}, 0), 65)
        self.assertEqual(units({"item": "water_ice"}, 40, 65, None, {}, 0), 40)
        self.assertEqual(units({"item": "water_ice", "qty": 30}, 5500, 65, None, {}, 0), 30)
        self.assertEqual(units({"item": "water_ice"}, 5500, 0, None, {}, 0), 0)
        self.assertEqual(units({"item": "water_ice"}, 0, 65, None, {}, 0), 0)

    def test_withdraw_before_a_sale_here_takes_only_what_the_bid_takes(self):
        units = functions("withdraw_units")["withdraw_units"]
        sell = {"item": "water_ice", "min_price": 25}
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, sell, {"best_buy": 32, "best_buy_qty": 20}, 0), 20)
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, sell, {"best_buy": 32, "best_buy_qty": 563}, 0), 65)
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, sell, {"best_buy": 32, "best_buy_qty": 20}, 15), 5)
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, sell, {"best_buy": 20, "best_buy_qty": 900}, 0), 0)
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, sell, {}, 0), 0)

    def test_free_hold_counts_each_item_by_its_size(self):
        # 2026-11-16 12:15 UTC: the first carries withdrew by item units (65 less 42 aboard = 23); the game refused it,
        # "Need 23 but only 9 available": tungsten and lead ore take two units of space each (state/cargo `size`).
        free = functions("free_space")["free_space"]
        rows = [{"item_id": "carbon_ore", "quantity": 15, "size": 1}, {"item_id": "tungsten_ore", "quantity": 5, "size": 2},
                {"item_id": "lead_ore", "quantity": 3, "size": 2}]
        self.assertEqual(free(65, rows), 65 - 15 - 10 - 6)
        self.assertEqual(free(65, []), 65)
        self.assertEqual(free(65, [{"item_id": "water_ice", "quantity": 7}]), 58)
        self.assertEqual(free(65, None), 0)

    def test_withdraw_takes_no_more_units_than_their_size_fits_in_the_free_hold(self):
        # 2026-11-16 13:28 UTC: a withdraw of 33 plasma gas into an empty hold of 65 was refused, "Need 66 but only 65
        # available": plasma gas takes two units of space a piece (the storage view's `size`), and the step had counted
        # the free hold as item units, so the stop sold nothing.
        units = functions("withdraw_units")["withdraw_units"]
        sell = {"item": "plasma_gas", "min_price": 90}
        self.assertEqual(units({"item": "plasma_gas"}, 83, 65, sell, {"best_buy": 96, "best_buy_qty": 33}, 0, 2), 32)
        self.assertEqual(units({"item": "plasma_gas"}, 83, 65, None, {}, 0, 2), 32)
        self.assertEqual(units({"item": "plasma_gas"}, 83, 1, None, {}, 0, 2), 0)
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, None, {}, 0, 1), 65)
        self.assertEqual(units({"item": "water_ice"}, 5500, 65, None, {}, 0), 65)

    def test_the_withdraw_step_passes_the_size_the_storage_view_names(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertIn("SIZES[", source)
        self.assertIn("SIZES.get(want['item'], 1)", source)

    def test_the_withdraw_step_runs_after_the_book_is_read_and_before_the_sale(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        book = source.index("book, board = save_station(base, system)")
        step = source.index("for want in stop.get('withdraw') or []:")
        sale = source.index("for want in stop.get('sell') or []:")
        self.assertTrue(book < step < sale)
        self.assertIn("'withdraw', {'item_id': want['item'], 'quantity': units, 'target': 'self'}, group='spacemolt_storage'", source)


# The whole runner on a made-up route, its module level run as it stands: `call` (the only way to the engine) is taken
# out and a fake gate answers instead, DATA is a temporary folder, the clock is counted, not waited, and no program is
# started. The fake keeps a wallet, a hold, a storage, a book and the workshop's jobs: a job delivers into storage after
# `ticks` reads of the storage, and `queue` says how many runs the workshop takes at each ask.
FAKE_RUN = r'''
import ast, json, pathlib, subprocess, sys, time, types, urllib.request
CONFIG = json.loads(pathlib.Path(sys.argv[1]).read_text())
WORLD, LOG, clock = CONFIG["world"], [], [1800000000.0]
time.time = lambda: clock[0]
time.sleep = lambda seconds: clock.__setitem__(0, clock[0] + seconds)
urllib.request.build_opener = lambda *a, **k: types.SimpleNamespace(open=lambda *a, **k: 1 / 0)   # no network from a test
subprocess.run = lambda *a, **k: types.SimpleNamespace(stdout="no hunt in a test")
sys.modules["division"] = types.SimpleNamespace(require=lambda pilot: None)
sys.argv = ["route_run.py", "trader-1", CONFIG["route"]]


def items(where):
    return [{"item_id": k, "quantity": v, "size": 1} for k, v in sorted(WORLD[where].items()) if v]


def move(source, target, item, units):
    units = min(units, WORLD[source].get(item, 0))
    WORLD[source][item] = WORLD[source].get(item, 0) - units
    WORLD[target][item] = WORLD[target].get(item, 0) + units


def call(method, path, body=None, timeout=900):
    if method == "GET":
        if path.endswith("/state/cargo"):
            return 200, items("cargo")
        if path.endswith("/loop"):
            return 200, {"running": False}
        return 200, {"state": {"credits": WORLD["credits"], "ship": {"fuel": WORLD["fuel"], "max_fuel": WORLD["max_fuel"]}}, "hasExecutingGoal": False}
    if method == "DELETE" or path.endswith("/loop"):
        LOG.append(["loop", method])
        return 200, {}
    if path.endswith("/goal"):
        LOG.append(["goal", body["type"]])
        if body["type"] == "prepare-at-station":
            WORLD.setdefault("refuel_asked", []).append(body["options"].get("refuel"))
            if body["options"].get("refuel"):                    # the station (or our bunker) fills the tank
                WORLD["fuel"] = WORLD["max_fuel"]
        for want in body["options"].get("items") or []:          # buy-items: at the ask, with the tax of 1 percent
            WORLD["cargo"][want["itemId"]] = WORLD["cargo"].get(want["itemId"], 0) + want["maxQuantity"]
            WORLD["credits"] -= int(round(want["maxQuantity"] * want["maxPrice"] * 1.01))
        return 200, {"success": True, "message": "done"}
    action, params = body["action"], body["params"]
    LOG.append([action, params])
    if action == "get_active_missions":
        return 200, {"result": ""}
    if action == "view_orders":                                       # the pilot's own orders at this station
        return 200, {"structuredContent": {"orders": [dict(o) for o in WORLD.get("orders") or []]}}
    if action == "create_sell_order":                                 # escrow from the hold first, then storage
        want, got = params["quantity"], 0
        for where in ("cargo", "storage"):
            take = min(want - got, WORLD[where].get(params["item_id"], 0))
            WORLD[where][params["item_id"]] = WORLD[where].get(params["item_id"], 0) - take
            got += take
        if not got:
            return 200, {"error": {"code": "insufficient_items"}}
        orders = WORLD.setdefault("orders", [])
        same = next((o for o in orders if o["item_id"] == params["item_id"] and o["price_each"] == params["price_each"]), None)
        if same:
            same["remaining"] += got
        else:
            orders.append({"order_id": "o%d" % (len(orders) + 1), "side": "sell", "item_id": params["item_id"], "remaining": got, "price_each": params["price_each"]})
        return 200, {}
    if action == "modify_order":
        for o in WORLD.get("orders") or []:
            if o["order_id"] == params["order_id"]:
                o["price_each"] = params["new_price"]
        return 200, {}
    if action == "view_market":
        return 200, {"structuredContent": {"items": [dict(row, item_id=k) for k, row in sorted(WORLD["book"].items())]}}
    if action == "get_missions":
        return 200, {"structuredContent": {"missions": WORLD.get("missions") or []}}
    if action == "deposit" and params.get("target") not in (None, "self", "faction"):   # a gift into another pilot's storage (r22)
        if WORLD.get("gift_refuses") or ("items" in params and WORLD.get("bulk") is False):
            return 200, {"error": "refused"}
        source = "storage" if params.get("source") == "storage" else "cargo"
        given = WORLD.setdefault("given", {}).setdefault(params["target"], {})
        for row in params.get("items") or [{"item_id": params["item_id"], "quantity": params["quantity"]}]:
            if row["item_id"] in (WORLD.get("gift_refuses_items") or []):
                continue
            units = min(row["quantity"], WORLD[source].get(row["item_id"], 0))
            WORLD[source][row["item_id"]] -= units
            given[row["item_id"]] = given.get(row["item_id"], 0) + units
        return 200, {}
    if action == "deposit" and params["item_id"] == "fuel":          # the tank into the faction's fuel reserve here
        units = 0 if WORLD.get("bunker_refuses") else min(params["quantity"], WORLD["fuel"])
        WORLD["fuel"] -= units
        WORLD["reserve"] = WORLD.get("reserve", 0) + units
        return 200, ({"error": "refused"} if not units else {})
    if action == "refuel":                                             # fuel cells from the hold, whole cells, 20 fuel each
        n = min(params.get("quantity", 1), WORLD["cargo"].get("fuel_cell", 0))
        WORLD["cargo"]["fuel_cell"] = WORLD["cargo"].get("fuel_cell", 0) - n
        WORLD["fuel"] = min(WORLD["max_fuel"], WORLD["fuel"] + 20 * n)   # a cell burnt into less room loses the rest
        return 200, {}
    if action == "view" and params.get("target") == "faction":
        return 200, {"structuredContent": {"faction_fuel_reserve": WORLD.get("reserve", 0), "faction_fuel_capacity": 50000, "items": []}}
    if action == "deposit":
        move("cargo", "storage", params["item_id"], params["quantity"])
    if action == "withdraw":
        move("storage", "cargo", params["item_id"], params["quantity"])
    if action == "view":
        for job in WORLD["jobs"]:
            job["ticks"] -= 1
            if job["ticks"] == 0:
                WORLD["storage"][job["item"]] = WORLD["storage"].get(job["item"], 0) + job["units"]
        return 200, {"structuredContent": {"items": items("storage")}}
    if action == "sell":
        row = WORLD["book"][params["item_id"]]
        units = min(params["quantity"], WORLD["cargo"].get(params["item_id"], 0))
        WORLD["cargo"][params["item_id"]] -= units
        WORLD["credits"] += units * row["best_buy"]
        row["best_buy_qty"] -= units
    if action == "craft":
        if params.get("dry_run"):
            return 200, {"structuredContent": {"kind": "quote", "details": WORLD["quote"]}}
        asked = -(-params["quantity"] // WORLD["per_run"])      # the game: `quantity` counts made units, rounded up to runs
        runs = min(WORLD["queue"].pop(0) if WORLD["queue"] else 0, asked)
        if runs:
            WORLD["jobs"].append({"item": WORLD["makes"], "units": runs * WORLD["per_run"], "ticks": WORLD["ticks"]})
        return 200, {"structuredContent": {"kind": "job", "details": {"job_id": "job-%d" % len(WORLD["jobs"]), "runs": runs,
                                                                      "message": "%d of %d runs queued" % (runs, asked)}}}
    return 200, {}


tree = ast.parse(pathlib.Path(CONFIG["runner"]).read_text(encoding="ascii"))
keep = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "call":
        continue                                                # the fake gate above answers instead
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "DATA":
        node = ast.copy_location(ast.parse("DATA = pathlib.Path(%r)" % CONFIG["data"]).body[0], node)
    keep.append(node)
tree.body = keep
try:
    exec(compile(ast.fix_missing_locations(tree), CONFIG["runner"], "exec"), {"__name__": "__main__", "__file__": CONFIG["runner"], "call": call})
finally:
    pathlib.Path(CONFIG["log"]).write_text(json.dumps({"log": LOG, "world": WORLD}))
'''


def fly(route, world, runner=FLEET / "route_run.py", files=None):
    """(the gate calls in their order, the fake world after, the run's row, the run's output) of one run of `route`;
    `files`: {path under the data folder: JSON value} written before the run (r22: the fleet, receivers, switch)."""
    base = {"credits": 20000, "cargo": {}, "storage": {}, "book": {}, "jobs": [], "queue": [], "quote": {}, "makes": "", "per_run": 1, "ticks": 1,
            "fuel": 95, "max_fuel": 95}
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        (root / "route.json").write_text(json.dumps(route))
        for name, value in (files or {}).items():
            (root / "data" / name).parent.mkdir(parents=True, exist_ok=True)
            (root / "data" / name).write_text(value if isinstance(value, str) else json.dumps(value))
        config = {"world": dict(base, **world), "route": str(root / "route.json"), "data": str(root / "data"), "runner": str(runner), "log": str(root / "log.json")}
        (root / "config.json").write_text(json.dumps(config))
        done = subprocess.run([sys.executable, "-I", "-B", "-c", FAKE_RUN, str(root / "config.json")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, timeout=120)
        out = json.loads((root / "log.json").read_text())
        record = root / "data" / "stock" / "handover.jsonl"          # r22: the gifts the run recorded for the ledger
        out["world"]["handover"] = [json.loads(line) for line in record.read_text().splitlines()] if record.exists() else []
        rows = [json.loads(line) for line in (root / "data" / "routes" / "runs.jsonl").read_text().splitlines()]
    return out["log"], out["world"], rows[-1], done.stdout


def steps(log):
    """The calls that act or read a book, without the reads of hold and wallet: the order a stop's work runs in."""
    out = []
    for action, params in log:
        if action == "craft":
            out.append("craft dry_run" if params.get("dry_run") else "craft %d" % params["quantity"])
        elif action in ("deposit", "withdraw", "sell"):
            out.append("%s %d %s" % (action, params["quantity"], params["item_id"]))
        else:
            out.append("%s %s" % (action, params) if action in ("goal", "loop") else action)
    return out


CRAFT_STOP = {"at": "home:core:base", "sell": [{"item": "control_node", "min_price": 760}], "buy": [{"item": "silver_wiring", "qty": 8, "max_price": 400}],
              "craft": [{"recipe": "assemble_control_node", "runs": 8, "makes": "control_node", "per_run": 2, "inputs": ["silver_wiring"]}]}
CRAFT_ROUTE = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [CRAFT_STOP]}
CRAFT_WORLD = {"storage": {"circuit_board": 16, "copper_wiring": 32, "gold_wiring": 8},
               "book": {"silver_wiring": {"best_sell": 300, "best_sell_qty": 50}, "control_node": {"best_buy": 800, "best_buy_qty": 20}},
               "quote": {"kind": "quote", "have_inputs": True, "credits_total": 0, "effective_time_per_run": 2},
               "queue": [8], "makes": "control_node", "per_run": 2, "ticks": 2}


class CraftStepTests(unittest.TestCase):
    # requests.log ENT-013 (the Trade Admiral): a circuit buys inputs along its stops, crafts at one station's workshop and
    # sells the product there. The calls are craftchain.py's of the skill logistics-stock, which made five harvesters and
    # 75 liquid hydrogen that way (guidebook logistics.md sections 1 and 11, 2026-11-16).
    def test_a_stop_buys_crafts_and_sells_what_it_made(self):
        log, world, row, out = fly(CRAFT_ROUTE, CRAFT_WORLD)
        self.assertEqual(steps(log), [
            "goal prepare-at-station", "get_active_missions", "view_market", "get_missions",          # dock, hand in, the book
            "goal buy-items",                                                                         # the sale finds no node aboard; the buy
            "deposit 8 silver_wiring", "craft dry_run", "view", "craft 16", "view", "view",            # inputs into storage, quote, queue, wait
            "view_market", "get_missions", "view", "withdraw 16 control_node", "sell 16 control_node"], out)   # a fresh book, then the sale once more
        crafts = [params for action, params in log if action == "craft"]
        self.assertEqual(crafts[0], {"recipe_id": "assemble_control_node", "quantity": 16, "deliver_to": "storage", "preset": "workshop", "dry_run": True})
        self.assertEqual(crafts[1], {"recipe_id": "assemble_control_node", "quantity": 16, "deliver_to": "storage", "preset": "workshop"})
        self.assertEqual((row["credits_before"], row["credits_after"], row["delta"]), (20000, 20000 - 2424 + 16 * 800, 16 * 800 - 2424))
        self.assertEqual((row["stops"], row["of"], row["notes"]), (1, 1, []))
        self.assertEqual((world["cargo"].get("control_node"), world["storage"].get("control_node"), world["book"]["control_node"]["best_buy_qty"]), (0, 0, 4))

    def test_the_rest_is_asked_again_when_the_workshop_queues_fewer_runs(self):
        # 2026-11-16: 7 etchings asked, 3 queued, then 2, 1 and 1 (guidebook logistics.md section 11)
        log, _world, row, out = fly(CRAFT_ROUTE, dict(CRAFT_WORLD, queue=[3, 3, 2], ticks=1))
        self.assertEqual([s for s in steps(log) if s.startswith("craft")], ["craft dry_run", "craft 16", "craft 10", "craft 4"], out)
        self.assertIn("sell 16 control_node", steps(log))
        self.assertEqual((row["delta"], row["notes"]), (16 * 800 - 2424, []))

    def test_one_ask_queues_every_run_of_a_recipe_that_makes_several_a_run(self):
        # the game counts a craft's `quantity` in made units, rounded up to runs: 27 liquid hydrogen asked queued 9 runs of 3
        # (queue.log ENT-114, 2026-11-16 19:02 UTC). Asked `runs`, a recipe of 2 a run queued half and was asked again three
        # times; asked runs x per_run, the workshop takes the whole job at once.
        log, _world, row, out = fly(CRAFT_ROUTE, CRAFT_WORLD)
        self.assertEqual([s for s in steps(log) if s.startswith("craft")], ["craft dry_run", "craft 16"], out)
        self.assertEqual((row["delta"], row["notes"]), (16 * 800 - 2424, []))

    def test_a_craft_without_inputs_makes_nothing_and_the_run_goes_on(self):
        route = dict(CRAFT_ROUTE, stops=[CRAFT_STOP, {"at": "home:core:other"}])
        quote = {"kind": "quote", "have_inputs": False, "credits_total": 0, "message": "missing 8 gold_wiring"}
        log, world, row, out = fly(route, dict(CRAFT_WORLD, quote=quote, storage={}))
        self.assertEqual([s for s in steps(log) if s.startswith(("craft", "withdraw", "sell"))], ["craft dry_run"], out)
        self.assertEqual((row["stops"], row["of"], row["notes"]), (2, 2, ["craft assemble_control_node: no inputs"]))
        self.assertEqual(world["storage"].get("silver_wiring"), 8)                                    # the goods stay where they are
        self.assertEqual(steps(log).count("goal prepare-at-station"), 2)

    def test_a_fee_the_wallet_cannot_pay_above_its_floor_makes_nothing(self):
        quote = dict(CRAFT_WORLD["quote"], credits_total=14577)                                       # 17,576 after the buy, less the floor of 3,000
        log, _world, row, out = fly(CRAFT_ROUTE, dict(CRAFT_WORLD, quote=quote))
        self.assertEqual([s for s in steps(log) if s.startswith(("craft", "withdraw", "sell"))], ["craft dry_run"], out)
        self.assertEqual(row["notes"], ["craft assemble_control_node: fee"])
        log, _world, row, out = fly(CRAFT_ROUTE, dict(CRAFT_WORLD, quote=dict(quote, credits_total=14576)))
        self.assertIn("craft 16", steps(log), out)                                                     # down to the floor itself: crafted
        self.assertEqual(row["notes"], [])

    def test_a_craft_in_a_facility_asks_no_workshop_and_keeps_to_its_fee_a_run(self):
        # requests.log ENT-190 (the Fleet Admiral): refine_steel (5 iron ore, 2 steel plate) runs only in a facility; asked
        # without `preset` the game rents a public one and quotes its fee (guidebook logistics.md section 7, 2026-11-15).
        # `max_fee` is the most a run may cost: the catalog's base value of what one run makes.
        stop = dict(CRAFT_STOP, craft=[dict(CRAFT_STOP["craft"][0], venue="facility", max_fee=40)])
        route = dict(CRAFT_ROUTE, stops=[stop])
        log, _world, row, out = fly(route, dict(CRAFT_WORLD, quote=dict(CRAFT_WORLD["quote"], credits_total=8 * 40)))
        crafts = [params for action, params in log if action == "craft"]
        self.assertEqual(crafts[0], {"recipe_id": "assemble_control_node", "quantity": 16, "deliver_to": "storage", "dry_run": True})
        self.assertEqual(crafts[1], {"recipe_id": "assemble_control_node", "quantity": 16, "deliver_to": "storage"})
        self.assertEqual(row["notes"], [], out)
        log, _world, row, out = fly(route, dict(CRAFT_WORLD, quote=dict(CRAFT_WORLD["quote"], credits_total=8 * 40 + 1)))
        self.assertEqual([s for s in steps(log) if s.startswith(("craft", "withdraw", "sell"))], ["craft dry_run"], out)
        self.assertEqual(row["notes"], ["craft assemble_control_node: fee above max_fee"])

    def test_the_wait_ends_at_craftchain_s_limit_and_the_row_says_how_many_were_made(self):
        log, _world, row, out = fly(CRAFT_ROUTE, dict(CRAFT_WORLD, ticks=10 ** 6))
        after = steps(log)[steps(log).index("craft 16") + 1:]
        self.assertEqual(after, ["view"] * 30, out)                  # (2 ticks x 8 runs + 4) x 11 s x 1.5 = 330 s, a read every 11 s
        self.assertEqual(row["notes"], ["craft assemble_control_node: 0 of 16 made"])
        self.assertEqual(out.count("0 of 16 control_node in storage"), 6)        # `say` every fifth read: the order file stays fresh
        log, _world, row, out = fly(CRAFT_ROUTE, dict(CRAFT_WORLD, queue=[3, 0], ticks=1))             # the workshop takes no more runs
        self.assertEqual([s for s in steps(log) if s.startswith(("craft", "withdraw", "sell"))],
                         ["craft dry_run", "craft 16", "craft 10", "withdraw 6 control_node", "sell 6 control_node"], out)
        self.assertEqual((row["notes"], row["delta"]), (["craft assemble_control_node: 6 of 16 made"], 6 * 800 - 2424))

    def test_a_route_without_craft_flies_as_before(self):
        # the store, withdraw, sell and buy of a route written before the craft step: the same calls in the same order
        stop = {"at": "home:core:base", "store": ["iron_ore"], "withdraw": [{"item": "water_ice", "qty": 30}],
                "sell": [{"item": "water_ice", "min_price": 25}, {"item": "copper_ore", "min_price": 10}], "buy": [{"item": "fuel_cell", "qty": 2, "max_price": 50}]}
        world = {"cargo": {"iron_ore": 12, "copper_ore": 5}, "storage": {"water_ice": 500},
                 "book": {"water_ice": {"best_buy": 30, "best_buy_qty": 40}, "copper_ore": {"best_buy": 12, "best_buy_qty": 3}, "fuel_cell": {"best_sell": 40, "best_sell_qty": 9}}}
        log, world, row, out = fly({"id": "old", "kind": "circuit", "title": "t", "stops": [stop]}, world)
        self.assertEqual(steps(log), ["goal prepare-at-station", "get_active_missions", "deposit 12 iron_ore", "view_market", "get_missions", "view",
                                      "withdraw 30 water_ice", "sell 30 water_ice", "sell 3 copper_ore", "goal buy-items"], out)
        self.assertEqual((row["delta"], row["notes"]), (30 * 30 + 3 * 12 - 81, []))
        self.assertEqual((world["cargo"]["copper_ore"], world["storage"]["iron_ore"]), (2, 12))

    def test_a_craft_entry_without_makes_is_not_crafted(self):
        space = functions("workshop")
        said = []
        space.update(say=said.append, raw=lambda *a, **k: self.fail("no call to the engine"), cargo=lambda: self.fail("no read of the hold"))
        self.assertEqual(space["workshop"]({"recipe": "assemble_control_node", "runs": 8}, "base"), (0, "craft assemble_control_node: no makes"))
        self.assertEqual(len(said), 1)

    def test_the_craft_answer_is_read_where_craftchain_reads_it(self):
        fields = functions("craft_fields")["craft_fields"]
        self.assertEqual(fields({"structuredContent": {"kind": "job", "details": {"runs": 3}}}), {"runs": 3})
        self.assertEqual(fields({"structuredContent": {"kind": "quote", "have_inputs": True}}), {"kind": "quote", "have_inputs": True})
        self.assertEqual(fields({"result": {"structuredContent": {"details": {"runs": 2}}}}), {"runs": 2})
        self.assertEqual(fields({"result": "text only", "error": "x"}), {"result": "text only", "error": "x"})

    def test_the_craft_step_runs_after_the_buy_and_before_the_accept(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        buy, craft = source.index("for want in stop.get('buy') or []:"), source.index("for job in stop.get('craft') or []:")
        self.assertTrue(buy < craft < source.index("if stop.get('accept'):"))
        defined = {node.name for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}
        self.assertTrue({"workshop", "craft_fields", "deposit", "sell_into_bid"} <= defined)
        self.assertEqual(rebound(FLEET / "route_run.py"), [])                                         # no step binds a function's name


GIFT_FILES = {"fleet/fleet.json": {"ships": [{"name": "trader-1"}, {"name": "trader-9"}]}, "fleet/receivers.json": {"trader": {"base": "trader-9"}},
              "fleet/strict-classes-on": ""}
GIFT_STOP = {"at": "home:core:base", "store": "all", "gift": {"to": "trader", "items": "all"}}
GIFT_ROUTE = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [GIFT_STOP]}
GIFT_WORLD = {"cargo": {"water_ice": 30, "iron_ore": 5}, "storage": {"water_ice": 100}}


class GiftStepTests(unittest.TestCase):
    # r22 (Suggi, 2026-11-21: "Only Zero mines, only Mercury trades"): selling is Trade's alone; the goods of the other
    # divisions go by gift into a trader's storage, where its sell routes find them. A stop's `gift` (handover.py) gives
    # them there in one call where the v2 `items` list is taken, else one call per good, read back from the storage.
    def gifts(self, log):
        return [params for action, params in log if action == "deposit" and params.get("target") not in ("self", "faction")]

    def test_a_gift_gives_the_stored_goods_to_the_receiver_named_for_the_station_in_one_call(self):
        log, world, row, out = fly(GIFT_ROUTE, GIFT_WORLD, files=GIFT_FILES)
        self.assertEqual(self.gifts(log), [{"items": [{"item_id": "iron_ore", "quantity": 5}, {"item_id": "water_ice", "quantity": 130}],
                                            "source": "storage", "target": "trader-9"}], out)
        self.assertEqual(world["given"], {"trader-9": {"iron_ore": 5, "water_ice": 130}})
        self.assertEqual({k: v for k, v in world["storage"].items() if v}, {})
        self.assertIn("RESULT gift trader-1 -> trader-9 at base: iron_ore 5, water_ice 130", out)
        self.assertEqual(row["notes"], [], out)
        self.assertEqual(row["delta"], 0)                                     # a gift moves no wallet: nobody earned it

    def test_a_refused_gift_leaves_the_goods_with_the_giver_and_says_so(self):
        log, world, row, out = fly(GIFT_ROUTE, dict(GIFT_WORLD, gift_refuses=True), files=GIFT_FILES)
        self.assertEqual(world["storage"], {"water_ice": 130, "iron_ore": 5}, out)
        self.assertEqual(len(self.gifts(log)), 3, out)                        # the list, then one call per good
        self.assertEqual(row["notes"], ["gift to trader-9 at base: 0 of 135 given, kept iron_ore 5, water_ice 130 (iron_ore: refused; water_ice: refused)"])
        self.assertIn("refused, kept by the giver: iron_ore 5, water_ice 130", out)

    def test_a_list_the_game_refuses_goes_one_good_at_a_time_and_a_good_refused_stays(self):
        world = dict(GIFT_WORLD, bulk=False, gift_refuses_items=["iron_ore"])
        log, world, row, out = fly(GIFT_ROUTE, world, files=GIFT_FILES)
        self.assertEqual([("items" in p, p.get("item_id")) for p in self.gifts(log)], [(True, None), (False, "iron_ore"), (False, "water_ice")], out)
        self.assertEqual(world["given"], {"trader-9": {"water_ice": 130}})
        self.assertEqual(world["storage"]["iron_ore"], 5)
        self.assertEqual(row["notes"], ["gift to trader-9 at base: 130 of 135 given, kept iron_ore 5"], out)

    def test_keep_and_named_items_and_the_hold_as_source(self):
        stop = {"at": "home:core:base", "gift": {"to": "trader-9", "items": ["water_ice"], "source": "both", "keep": {"water_ice": 20}}}
        log, world, row, out = fly(dict(GIFT_ROUTE, stops=[stop]), GIFT_WORLD, files=GIFT_FILES)
        self.assertEqual([(p.get("source"), p.get("item_id"), p.get("quantity")) for p in self.gifts(log)], [("cargo", "water_ice", 30), ("storage", "water_ice", 80)], out)
        self.assertEqual((world["cargo"]["iron_ore"], world["storage"]["water_ice"]), (5, 20))

    def test_a_gift_to_a_stranger_or_to_a_role_with_no_receiver_calls_nothing(self):
        for to, why in (("trader-77", "`trader-77` is not a pilot of ours"), ("hauler", "no hauler named to receive at base")):
            stop = dict(GIFT_STOP, gift={"to": to})
            log, world, row, out = fly(dict(GIFT_ROUTE, stops=[stop]), GIFT_WORLD, files=GIFT_FILES)
            self.assertEqual(self.gifts(log), [], out)
            self.assertTrue(row["notes"] and why in row["notes"][0], row["notes"])
            self.assertEqual(world["storage"], {"water_ice": 130, "iron_ore": 5})

    def test_with_the_switch_off_a_gift_stop_gives_nothing_and_the_run_is_as_before(self):
        files = {k: v for k, v in GIFT_FILES.items() if k != "fleet/strict-classes-on"}
        log, world, row, out = fly(GIFT_ROUTE, GIFT_WORLD, files=files)
        plain, _w, _r, _o = fly(dict(GIFT_ROUTE, stops=[{k: v for k, v in GIFT_STOP.items() if k != "gift"}]), GIFT_WORLD, files=files)
        self.assertEqual(self.gifts(log), [], out)
        self.assertEqual(steps(log), steps(plain))
        self.assertIn("not given, strict classes are off", out)

    def test_every_gift_is_recorded_for_the_ledger_after_store_and_before_store_faction(self):
        log, world, row, out = fly(GIFT_ROUTE, GIFT_WORLD, files=GIFT_FILES)
        self.assertEqual([(r["from"], r["to"], r["base"], r["items"], r["route"]) for r in world["handover"]],
                         [("trader-1", "trader-9", "base", {"iron_ore": 5, "water_ice": 130}, "made-up")], out)
        log, world, row, out = fly(GIFT_ROUTE, dict(GIFT_WORLD, gift_refuses=True), files=GIFT_FILES)
        self.assertEqual(world["handover"], [])                               # nothing moved: nothing for the ledger
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertIn("handover.give(raw, cargo, say, time.sleep, pilot, base, want, str(DATA), ROUTE['id'])", source)
        store, gift, faction = (source.index("for item in store_list(stop.get('store'), hold, keep):"), source.index("handover.give("),
                                source.index("if stop.get('store_faction'):"))
        self.assertTrue(store < gift < faction)                               # after `store`, before `store_faction`


class MineStepStopTests(unittest.TestCase):
    def test_the_mine_step_stops_its_loop_on_every_way_out(self):
        # requests ENT-195: a run told to stop by the run host left its mining loop running, and every goal answered 409
        tree = ast.parse((FLEET / "route_run.py").read_text(encoding="ascii"))
        ends = ["\n".join(ast.unparse(line) for line in node.finalbody) for node in ast.walk(tree) if isinstance(node, ast.Try) and node.finalbody]
        self.assertTrue(any("DELETE" in text and "/loop" in text for text in ends), ends)


ORDER_STOP = {"at": "home:core:base", "sell_order": [{"item": "crystal_melt", "qty": 5, "price": 2900, "floor": 2600}]}
ORDER_ROUTE = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [ORDER_STOP]}


class SellOrderStepTests(unittest.TestCase):
    # orders.log ENT-066 to ENT-068 (block MERCURY: build the order steps yourself, one order first), requests.log ENT-373,
    # rule F39: a stop keeps one resting sell order of a good the pilot holds here, at its price, never under its floor.
    def moves(self, want, row, mine, have):
        return functions("sell_order_moves")["sell_order_moves"](want, row, mine, have)

    def test_nothing_listed_lists_what_is_held_up_to_qty(self):
        self.assertEqual(self.moves({"item": "m", "qty": 5, "price": 2900}, {}, [], 3), [("create", 3, 2900)])
        self.assertEqual(self.moves({"item": "m", "qty": 5, "price": 2900}, {}, [], 9), [("create", 5, 2900)])

    def test_a_listed_order_at_the_price_is_topped_up_and_never_past_qty(self):
        mine = [{"order_id": "a", "remaining": 2, "price_each": 2900}]
        self.assertEqual(self.moves({"item": "m", "qty": 5, "price": 2900}, {}, mine, 9), [("create", 3, 2900)])
        mine = [{"order_id": "a", "remaining": 5, "price_each": 2900}]
        self.assertEqual(self.moves({"item": "m", "qty": 5, "price": 2900}, {}, mine, 9), [])

    def test_an_order_at_another_price_is_repriced_first(self):
        mine = [{"order_id": "a", "remaining": 2, "price_each": 3100}]
        self.assertEqual(self.moves({"item": "m", "qty": 2, "price": 2900}, {}, mine, 0), [("modify", "a", 2900)])

    def test_the_price_never_goes_under_the_floor_and_rises_to_a_higher_bid(self):
        self.assertEqual(self.moves({"item": "m", "qty": 1, "price": 2500, "floor": 2600}, {}, [], 1), [("create", 1, 2600)])
        # a bid above the price: the ask would fill at the bid at once; it is listed at the bid instead, never under it (F12)
        self.assertEqual(self.moves({"item": "m", "qty": 1, "price": 2900}, {"best_buy": 3000}, [], 1), [("create", 1, 3000)])

    def test_nothing_held_and_nothing_listed_does_nothing(self):
        self.assertEqual(self.moves({"item": "m", "qty": 5, "price": 2900}, {}, [], 0), [])

    def test_a_stop_lists_the_stored_good_and_the_run_row_says_so(self):
        log, world, row, out = fly(ORDER_ROUTE, {"storage": {"crystal_melt": 8}})
        acts = [(a, p) for a, p in log if a in ("view_orders", "create_sell_order", "modify_order")]
        self.assertEqual(acts[0][0], "view_orders")
        self.assertEqual(acts[1], ("create_sell_order", {"item_id": "crystal_melt", "quantity": 5, "price_each": 2900}))
        self.assertEqual(world["orders"], [{"order_id": "o1", "side": "sell", "item_id": "crystal_melt", "remaining": 5, "price_each": 2900}])
        self.assertEqual(world["storage"]["crystal_melt"], 3)
        self.assertIn("sell order crystal_melt: 5 listed at 2900", row["notes"], out)

    def test_a_second_run_reprices_and_lists_nothing_more(self):
        world = {"storage": {"crystal_melt": 3}, "orders": [{"order_id": "o1", "side": "sell", "item_id": "crystal_melt", "remaining": 5, "price_each": 3200}]}
        log, world, row, out = fly(ORDER_ROUTE, world)
        acts = [(a, p) for a, p in log if a in ("create_sell_order", "modify_order")]
        self.assertEqual(acts, [("modify_order", {"order_id": "o1", "new_price": 2900})], out)
        self.assertEqual(world["storage"]["crystal_melt"], 3)

    def test_the_order_step_runs_after_the_craft_and_before_the_accept(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertLess(source.index("for job in stop.get('craft')"), source.index("for want in stop.get('sell_order')"))
        self.assertLess(source.index("for want in stop.get('sell_order')"), source.index("if stop.get('accept'):"))


if __name__ == "__main__":
    unittest.main()


class AcceptByTitleTests(unittest.TestCase):
    """A station's procurement missions carry no template and a fresh mission_id each (Shipyard Supply at a shipyard):
    an `accept` entry may name the title, and the first posted copy not yet held is taken."""

    BOARD = [{"template_id": None, "mission_id": "procurement_a_fuel_tank", "title": "Shipyard Supply: Fuel Tank"},
             {"template_id": None, "mission_id": "procurement_b_fuel_tank", "title": "Shipyard Supply: Fuel Tank"},
             {"template_id": "market_participation_buying", "mission_id": "m1", "title": "Market Participation: Buying"}]

    def test_a_template_entry_finds_its_mission_as_before(self):
        find = functions("posted_mission")["posted_mission"]
        self.assertEqual(find(self.BOARD, "market_participation_buying")["mission_id"], "m1")
        self.assertEqual(find(self.BOARD, "procurement_b_fuel_tank")["mission_id"], "procurement_b_fuel_tank")
        self.assertIsNone(find(self.BOARD, "nothing_posted"))

    def test_a_title_entry_takes_the_first_copy_on_the_board(self):
        find = functions("posted_mission")["posted_mission"]
        self.assertEqual(find(self.BOARD, None, "Shipyard Supply: Fuel Tank")["mission_id"], "procurement_a_fuel_tank")
        self.assertIsNone(find(self.BOARD, None, "Shipyard Supply: Engine Core"))

    def test_the_accept_step_reads_the_title_of_an_entry(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        step = source[source.index("if stop.get('accept'):"):source.index("for step in stop.get('mine') or []:")]
        self.assertIn("posted_mission(board,", step)
        self.assertIn("entry.get('title')", step)


class EmptyTourAbortTests(unittest.TestCase):
    """2026-11-23: the empty-tour abort of the accept step read a name `index` the stop loop never binds (`for n, stop in
    enumerate(...)`): every run whose accept took nothing crashed with a NameError (125 runs of every division by 04:25 UTC)."""

    def test_the_accept_step_names_only_the_stop_loops_own_counter(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        loop = source.index("for n, stop in enumerate(ROUTE['stops']):")
        step = source[source.index("if stop.get('accept'):", loop):source.index("for step in stop.get('mine') or []:", loop)]
        self.assertNotIn("[index:]", step)
        self.assertNotIn("{index}", step)
        self.assertIn("pure_visit_tail(ROUTE['stops'][n + 1:])", step)   # the stops after this one: this one holds `accept`

    def test_a_tail_of_visits_only_is_pure_and_a_tail_with_work_is_not(self):
        tail = functions("pure_visit_tail")["pure_visit_tail"]
        stops = [{"at": "a:b:c", "accept": ["m"]}, {"at": "d:e:f"}, {"at": "d:e:f", "redock": True}]
        self.assertTrue(tail(stops[1:]))
        self.assertFalse(tail(stops))
        self.assertFalse(tail([]))
