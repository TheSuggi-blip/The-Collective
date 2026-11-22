"""game/fleet/routes.py buy_limit_warnings: a circuit whose `requires.ask` opens on an ask its own buy step refuses
(the buy's max_price under the ask gate x route_run.TAX, the 1% the runner adds) is named by `routes.py check`
(requests ENT-357, Mercury; errors.log ENT-138: train-trading-weapon-housing-node-alpha, gate 231 and buy 231 on an ask
of 230, bought nothing twice). Pure function over route dicts. No engine, no network.
"""

import importlib.util
import os
from pathlib import Path
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_buy_limit_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def route(gate, limit, item="weapon_housing", listed=False):
    ask = {"item": item, "base": "node_alpha_processing_station", "max_price": gate, "min_qty": 10}
    return {"id": "train-x", "kind": "circuit", "title": "t", "requires": {"ask": [ask] if listed else ask},
            "stops": [{"at": "node_alpha:node_alpha_processing_station:node_alpha_processing_station",
                       "buy": [{"item": "weapon_housing", "qty": 1, "max_price": limit}], "stop_on_failed_buy": True}]}


class BuyLimitTests(unittest.TestCase):
    def setUp(self):
        self.routes = load("routes")

    def test_a_buy_limit_under_the_gate_with_tax_is_named(self):
        found = self.routes.buy_limit_warnings({"train-x": route(231, 231)})
        self.assertEqual(found, [("train-x", 1, "weapon_housing", 231, 231)])

    def test_the_fixed_route_and_a_list_gate_are_judged_alike(self):
        self.assertEqual(self.routes.buy_limit_warnings({"train-x": route(230, 233)}), [])       # 230 x 1.01 = 232.3
        self.assertEqual(self.routes.buy_limit_warnings({"train-x": route(231, 231, listed=True)}), [("train-x", 1, "weapon_housing", 231, 231)])

    def test_a_gate_on_another_item_or_no_gate_names_nothing(self):
        self.assertEqual(self.routes.buy_limit_warnings({"train-x": route(231, 231, item="iron_ore")}), [])
        plain = route(231, 231)
        plain.pop("requires")
        self.assertEqual(self.routes.buy_limit_warnings({"train-x": plain}), [])


if __name__ == "__main__":
    unittest.main()
