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

    def test_the_store_step_uses_store_list(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        self.assertIn("for item in store_list(stop.get('store'), hold):", source)


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

    def test_the_withdraw_step_runs_after_the_book_is_read_and_before_the_sale(self):
        source = (FLEET / "route_run.py").read_text(encoding="ascii")
        book = source.index("book, board = save_station(base, system)")
        step = source.index("for want in stop.get('withdraw') or []:")
        sale = source.index("for want in stop.get('sell') or []:")
        self.assertTrue(book < step < sale)
        self.assertIn("'withdraw', {'item_id': want['item'], 'quantity': units, 'target': 'self'}, group='spacemolt_storage'", source)


if __name__ == "__main__":
    unittest.main()
