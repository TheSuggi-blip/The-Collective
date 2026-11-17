"""game/fleet/mine.py: the sale step docks before it sells. A made-up engine, no network, no waiting."""

import importlib.util
from pathlib import Path
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


class Engine:
    """Answers the calls of the sale step: busy for a while, then a dock goal that is refused `refusals` times."""

    def __init__(self, busy, refusals, error="already executing a goal"):
        self.busy, self.refusals, self.error, self.goals, self.reads = busy, refusals, error, 0, 0

    def __call__(self, method, path, body=None, timeout=120):
        if path.endswith("/goal"):
            self.goals += 1
            return (200, {"success": True}) if self.goals > self.refusals else (500, {"error": self.error})
        if path.endswith("/state/cargo"):
            return 200, []
        if path.endswith("/raw"):
            return 200, {"structuredContent": {"items": []}}
        self.reads += 1
        return 200, {"hasExecutingGoal": False, "hasRunningJob": self.reads <= self.busy, "state": {"player": {"credits": 5000}}}


class SaleStepTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("mine_under_test", FLEET / "mine.py")
        self.mine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mine)
        self.mine.time.sleep = lambda seconds: None
        self.said = []

    def sale(self, engine):
        notes = []
        sold = self.mine.sell_at_station(engine, self.said.append, "miner-1", ["sys", "poi", "base"], [], notes)
        return sold, notes

    def test_a_dock_refused_in_battle_sets_the_stance_flee(self):
        # requests ENT-090: the engine's combat mode flee leaves the battle stance as it was
        engine, posted = Engine(busy=0, refusals=2, error="in_battle: the ship is in a battle"), []
        original = engine.__call__

        def call(method, path, body=None, timeout=120):
            if path.endswith("/raw"):
                posted.append((body or {}).get("action"))
            return original(method, path, body, timeout)
        notes = []
        self.mine.sell_at_station(call, self.said.append, "miner-1", ["sys", "poi", "base"], [], notes)
        self.assertEqual(posted.count("stance"), 2)
        self.assertEqual(engine.goals, 3)
        self.assertEqual(notes, [])

    def test_the_census_runner_answers_in_battle_with_the_stance_flee(self):
        import ast
        source = (FLEET / "census.py").read_text(encoding="ascii")
        tree = ast.parse(source)
        functions = {node.name: ast.unparse(node) for node in tree.body if isinstance(node, ast.FunctionDef)}
        self.assertIn("free_from_battle()", functions["goal"])
        self.assertIn("in_battle", functions["goal"])
        self.assertIn("'stance', {'stance': 'flee'}, 'spacemolt_battle'", functions["free_from_battle"])

    def test_it_waits_for_a_job_in_flight_and_tries_the_dock_until_it_holds(self):
        engine = Engine(busy=3, refusals=4)
        self.assertEqual(self.sale(engine), ({}, []))                       # docked at the fifth try: no note
        self.assertEqual(engine.goals, 5)
        self.assertGreaterEqual(engine.reads, 4)                            # it read the account until the job had ended

    def test_a_dock_that_never_holds_leaves_the_engines_answer_in_the_notes(self):
        engine = Engine(busy=0, refusals=99, error="cannot dock: in_battle")
        sold, notes = self.sale(engine)
        self.assertEqual((sold, notes), ({}, ["not docked for the sale: 500 cannot dock: in_battle"]))
        self.assertEqual(engine.goals, self.mine.DOCK_TRIES)


class LastLoadTests(unittest.TestCase):
    """A run without a sale stores its last load: a partial hold left aboard closes every empty_hold route to the ship
    (2026-11-17 03:02 UTC: 34 miners waited with 10 to 42 units aboard after their 45-minute gather runs)."""

    def setUp(self):
        spec = importlib.util.spec_from_file_location("mine_under_test", FLEET / "mine.py")
        self.mine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mine)
        self.mine.time.sleep = lambda seconds: None
        self.said = []

    def engine(self, cargo):
        posted = []

        def call(method, path, body=None, timeout=120):
            posted.append((path.rsplit("/", 1)[-1], (body or {}).get("action")))
            if path.endswith("/goal"):
                return 200, {"success": True}
            if path.endswith("/state/cargo"):
                return 200, cargo
            if path.endswith("/raw"):
                return 200, {"structuredContent": {"items": []}}
            return 200, {"hasExecutingGoal": False, "hasRunningJob": False, "state": {"player": {"credits": 5000}}}
        return call, posted

    def test_a_partial_load_is_docked_and_stored(self):
        call, posted = self.engine([{"item_id": "iron_ore", "quantity": 42}, {"item_id": "copper_ore", "quantity": 23}])
        notes = []
        self.assertEqual(self.mine.store_last_load(call, self.said.append, "miner-1", ["sys", "poi", "base"], notes), 65)
        self.assertIn(("goal", None), posted)                                # it docked at the route's station
        self.assertEqual([a for _p, a in posted if a == "deposit"], ["deposit", "deposit"])
        self.assertEqual(notes, [])

    def test_five_units_or_less_stay_aboard_and_no_flight_is_made(self):
        call, posted = self.engine([{"item_id": "iron_ore", "quantity": 5}])
        self.assertEqual(self.mine.store_last_load(call, self.said.append, "miner-1", ["sys", "poi", "base"], []), 5)
        self.assertNotIn(("goal", None), posted)

    def test_main_stores_the_last_load_of_a_run_without_a_sale(self):
        import ast
        tree = ast.parse((FLEET / "mine.py").read_text(encoding="ascii"))
        main = next(ast.unparse(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
        self.assertIn("store_last_load(call, say, quoted, station, notes)", main)


if __name__ == "__main__":
    unittest.main()
