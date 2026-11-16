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
                "pilot, started, before, done, onetime, notes, reached = 'trader-1', time.time() - 120, 5000, [], [0], ['a note'], 1",
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


if __name__ == "__main__":
    unittest.main()
