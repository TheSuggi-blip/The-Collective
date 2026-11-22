"""game/fleet/handover.py and its three runners (r22, Suggi 2026-11-21: "Only Zero mines, only Mercury trades"): goods
change hands by a gift into another pilot of ours' storage. The receiver, what a gift gives, the gate's check, the
ledger's hook, and the hand-over of mine.py and hunt.py run whole on a fake gate. No engine, no network."""

import ast
import io
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
import handover                                   # noqa: E402  the module under test
import workclass                                  # noqa: E402  its switch

FLEET_FILE = {"ships": [{"name": "miner-1"}, {"name": "drone-1"}, {"name": "trader-9"}, {"name": "hauler-3"}], "away": [{"name": "trader-4"}]}
FLAGS = {"Mercurys Ledger": {"admiral": "Unity", "division": "Command", "role": "command"}}


class Data(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-handover-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "data"
        (self.data / "fleet").mkdir(parents=True)
        (self.data / "fleet" / "fleet.json").write_text(json.dumps(FLEET_FILE))
        (self.data / "fleet" / "flagships.json").write_text(json.dumps(FLAGS))
        (self.data / "fleet" / "receivers.json").write_text(json.dumps({"trader": {"central_nexus": "trader-9", "*": "trader-4"}, "hauler": {"node_beta": "drone-1"}}))
        self.switch(True)
        self.addCleanup(workclass.SEEN.clear)

    def switch(self, on):
        path = self.data / "fleet" / "strict-classes-on"
        path.write_text("") if on else (path.exists() and path.unlink())
        workclass.SEEN.clear()


class ReceiverTests(Data):
    def test_a_role_goes_to_the_pilot_named_for_the_station_else_the_star(self):
        self.assertEqual(handover.receiver("trader", "central_nexus", str(self.data), "miner-1"), ("trader-9", ""))
        self.assertEqual(handover.receiver("trader", "node_beta", str(self.data), "miner-1"), ("trader-4", ""))      # `*`; away pilots are ours
        self.assertEqual(handover.receiver("Mercurys Ledger", "x", str(self.data)), ("Mercurys Ledger", ""))
        self.assertIn("no scout named to receive at x", handover.receiver("scout", "x", str(self.data))[1])

    def test_never_a_stranger_and_never_the_giver(self):
        self.assertIn("is not a pilot of ours", handover.receiver("Strange Pilot", "x", str(self.data))[1])
        self.assertIn("is the giver itself", handover.receiver("trader", "central_nexus", str(self.data), "trader-9")[1])
        (self.data / "fleet" / "fleet.json").write_text("not json")
        self.assertIsNone(handover.receiver("trader", "central_nexus", str(self.data))[0])                       # no fleet read: no gift

    def test_the_plan_of_a_gift_keeps_ammunition_and_the_keep(self):
        plan = handover.planned({"items": "all", "source": "both", "keep": {"water_ice": 10}}, {"water_ice": 50, "iron_ore": 3},
                                {"water_ice": 5, "kinetic_rounds": 40}, {"kinetic_rounds"})
        self.assertEqual(plan, {"iron_ore": {"cargo": 0, "storage": 3}, "water_ice": {"cargo": 5, "storage": 40}})
        self.assertEqual(handover.planned({"items": ["kinetic_rounds"], "source": "cargo"}, {}, {"kinetic_rounds": 40}, {"kinetic_rounds"}),
                         {"kinetic_rounds": {"cargo": 40, "storage": 0}})                                      # named: given
        self.assertEqual(handover.planned({"to": "trader"}, {"water_ice": 7}, {"water_ice": 9}, set()), {"water_ice": {"cargo": 0, "storage": 7}})

    def test_the_gate_names_a_stranger_a_wrong_source_and_a_wrong_keep(self):
        self.assertEqual(handover.faults({"to": "trader"}), [])
        self.assertEqual(handover.faults("Mercurys Ledger", FLAGS), [])
        self.assertEqual(handover.faults({"to": "trader-9"}), [])            # a numbered pilot: the gate's own rule names it
        self.assertIn("a gift to a stranger is a loss", handover.faults({"to": "Strange Pilot"}, FLAGS)[0])
        self.assertEqual(len(handover.faults({"to": "trader", "source": "faction", "keep": {"x": -1}, "items": []})), 3)


class ReceiversCommandTests(Data):
    def run_cli(self, *args, member="mercury"):
        env = dict(os.environ, HERMES_SESSION_PROFILE=member)
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "handover.py")] + list(args) + ["--data", str(self.data)],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60, env=env)

    def test_a_keeper_names_a_receiver_of_its_role_and_only_a_pilot_of_ours(self):
        self.assertIn("named trader at synchrony_hub: trader-4", self.run_cli("receivers", "set", "trader", "synchrony_hub", "trader-4").stdout)
        self.assertEqual(handover.receivers(str(self.data))["trader"]["synchrony_hub"], "trader-4")
        self.assertIn("REFUSED: `Strange` is not a pilot of ours", self.run_cli("receivers", "set", "trader", "x", "Strange").stdout)
        self.assertIn("REFUSED: `miner-1` is a miner, not a trader", self.run_cli("receivers", "set", "trader", "x", "miner-1").stdout)
        self.assertIn("REFUSED: the receivers of the haulers are named by Apollo", self.run_cli("receivers", "set", "hauler", "x", "hauler-3").stdout)
        self.assertIn("dropped trader at synchrony_hub", self.run_cli("receivers", "drop", "trader", "synchrony_hub").stdout)

    def test_the_dry_run_says_to_whom_and_calls_nothing(self):
        root = Path(self.temp.name) / "game"
        (root / "routes").mkdir(parents=True)
        (root / "routes" / "gift-ice.json").write_text(json.dumps({"id": "gift-ice", "kind": "mine", "belt": "a:b", "station": "s:p:central_nexus", "gift": "trader"}))
        (self.data / "stock").mkdir()
        (self.data / "stock" / "storage.json").write_text(json.dumps({"pilots": {"miner-1": {"read_at": "2026-11-21T22:00:00Z", "stations": {"central_nexus": {"water_ice": 300}}}}}))
        done = self.run_cli("dry-run", "gift-ice", "miner-1", "--root", str(root))
        self.assertIn("at central_nexus", done.stdout)
        self.assertIn("to trader-9", done.stdout)
        self.assertIn("would go water_ice 300", done.stdout)


class LedgerHookTests(Data):
    def test_both_sides_of_a_gift_since_their_reading_are_read_first_in_one_pass(self):
        now = time.time()
        (self.data / "stock").mkdir()
        rows = [{"at": int(now - 300), "from": "miner-1", "to": "trader-9", "base": "central_nexus", "items": {"water_ice": 64}},
                {"at": int(now - 9 * 3600), "from": "drone-1", "to": "trader-4", "base": "x", "items": {"meat": 3}}]
        (self.data / "stock" / "handover.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        stamp = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
        book = {"pilots": {"miner-1": {"read_at": stamp(now - 600)}, "trader-9": {"read_at": stamp(now - 60)}, "drone-1": {"read_at": stamp(now - 99999)}}}
        names = ["miner-1", "trader-9", "drone-1", "trader-4", "hauler-3"]
        self.assertEqual(handover.sides_first(names, book, str(self.data), now, ["hauler-3"], []), ["miner-1", "hauler-3"])   # trader-9 read since; the old gift asks nothing
        book["pilots"]["trader-9"]["read_at"] = stamp(now - 900)
        self.assertEqual(handover.sides_first(names, book, str(self.data), now, ["hauler-3"], []), ["miner-1", "trader-9", "hauler-3"])
        self.assertEqual(handover.sides_first(names, book, str(self.data), now, [], ["miner-1"]), ["trader-9"])              # the rotation reads it anyway
        book["pilots"]["trader-9"]["error_at"] = stamp(now - 30)
        self.assertEqual(handover.sides_first(names, book, str(self.data), now, [], []), ["miner-1"])                        # a failed reading waits RETRY

    def test_the_ledger_puts_them_first(self):
        source = (FLEET / "ledger.py").read_text(encoding="ascii")
        batch = next(node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == "batch_of")
        self.assertIn("handover.sides_first(names, book, data, now, first, turns)", ast.unparse(batch))


# mine.py run whole: its main() with a fake opener for the gate (the only way out), a made-up data folder, no waiting
FAKE_MINE = r'''
import io, json, pathlib, sys, time, types
CONFIG = json.loads(pathlib.Path(sys.argv[1]).read_text())
WORLD, LOG = CONFIG["world"], []
time.sleep = lambda seconds: None
sys.modules["division"] = types.SimpleNamespace(require=lambda pilot: None)
sys.path.insert(0, CONFIG["fleet"])
import mine


def answer(method, path, body):
    if method == "GET" and path.endswith("/state/cargo"):
        return [{"item_id": k, "quantity": v} for k, v in sorted(WORLD["cargo"].items()) if v]
    if method == "GET" and path.endswith("/loop"):
        return {"running": True}
    if method == "GET":
        return {"state": {"credits": WORLD["credits"]}, "hasExecutingGoal": False}
    if path.endswith("/loop"):
        return {}
    if path.endswith("/goal"):
        LOG.append(["goal", body["type"]])
        return {"success": True}
    action, params = body["action"], body["params"]
    LOG.append([action, params])
    if action == "view":
        return {"structuredContent": {"items": [{"item_id": k, "quantity": v} for k, v in sorted(WORLD["storage"].items()) if v]}}
    if action == "view_market":
        return {"structuredContent": {"items": [{"item_id": params.get("item_id"), "buy_orders": [{"price_each": 30, "quantity": 999}]}]}}
    if action == "sell":
        units = min(params["quantity"], WORLD["cargo"].get(params["item_id"], 0) or WORLD["storage"].get(params["item_id"], 0))
        WORLD["credits"] += units * 30
        place = "cargo" if WORLD["cargo"].get(params["item_id"]) else "storage"
        WORLD[place][params["item_id"]] -= units
        return {}
    if action == "deposit" and params.get("target") == "self":
        WORLD["storage"][params["item_id"]] = WORLD["storage"].get(params["item_id"], 0) + WORLD["cargo"].pop(params["item_id"], 0)
        return {}
    if action == "deposit":
        given = WORLD.setdefault("given", {}).setdefault(params["target"], {})
        for row in params.get("items") or [{"item_id": params["item_id"], "quantity": params["quantity"]}]:
            place = "storage" if params.get("source") == "storage" else "cargo"
            units = min(row["quantity"], WORLD[place].get(row["item_id"], 0))
            WORLD[place][row["item_id"]] -= units
            given[row["item_id"]] = given.get(row["item_id"], 0) + units
        return {}
    return {}


class Answer(io.BytesIO):
    status = 200
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False


def opener_open(request, timeout=None):
    body = json.loads(request.data.decode()) if request.data else None
    return Answer(json.dumps(answer(request.get_method(), request.full_url, body)).encode())


mine.OPENER = types.SimpleNamespace(open=opener_open)
sys.argv = ["mine.py"] + CONFIG["argv"]
try:
    mine.main()
finally:
    pathlib.Path(CONFIG["log"]).write_text(json.dumps({"log": LOG, "world": WORLD}))
'''


def fly_mine(argv, world, data, switch):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(data) / "fleet" / "strict-classes-on"
        path.write_text("") if switch else (path.exists() and path.unlink())
        config = {"world": world, "argv": argv, "fleet": str(FLEET), "log": str(Path(folder) / "log.json")}
        (Path(folder) / "config.json").write_text(json.dumps(config))
        done = subprocess.run([sys.executable, "-I", "-B", "-c", FAKE_MINE, str(Path(folder) / "config.json")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, timeout=120, env=dict(os.environ, FLEET_DATA_ROOT=str(data)))
        out = json.loads((Path(folder) / "log.json").read_text())
    rows = [json.loads(line) for line in (Path(data) / "routes" / "runs.jsonl").read_text().splitlines()]
    return out["log"], out["world"], rows[-1], done.stdout


class MineHandOverTests(Data):
    """A mine route's `gift`: the run ends at the station with the hand-over instead of the sale."""
    ARGV = ["miner-1", "far:belt", "home:core:central_nexus", "--minutes", "0", "--route", "gift-ice", "--sell-items", "water_ice:20"]
    WORLD = {"credits": 9000, "cargo": {"water_ice": 40}, "storage": {"water_ice": 200}}

    def test_with_the_switch_on_the_load_goes_to_the_trader_and_nothing_is_sold(self):
        log, world, row, out = fly_mine(self.ARGV + ["--gift", json.dumps({"to": "trader"})], dict(self.WORLD), self.data, True)
        self.assertNotIn("sell", [step[0] for step in log], out)
        self.assertEqual(world["given"], {"trader-9": {"water_ice": 240}}, out)
        self.assertEqual((row["given"], row["given_to"], row["sold"], row["delta"]), ({"water_ice": 240}, "trader-9", {}, 0))
        self.assertIn("RESULT gift miner-1 -> trader-9 at central_nexus: water_ice 240", out)
        record = [json.loads(line) for line in (self.data / "stock" / "handover.jsonl").read_text().splitlines()]
        self.assertEqual([(r["from"], r["to"], r["items"]) for r in record], [("miner-1", "trader-9", {"water_ice": 240})])

    def test_with_the_switch_off_the_route_sells_as_before(self):
        log, world, row, out = fly_mine(self.ARGV + ["--gift", json.dumps({"to": "trader"})], dict(self.WORLD), self.data, False)
        self.assertIn("sell", [step[0] for step in log], out)
        self.assertNotIn("given", world)
        self.assertNotIn("given", row)

    def test_a_gift_to_a_stranger_keeps_the_load_in_the_miners_storage(self):
        log, world, row, out = fly_mine(self.ARGV + ["--gift", "Strange Pilot"], dict(self.WORLD), self.data, True)
        self.assertNotIn("given", world)
        self.assertEqual(world["storage"]["water_ice"], 240, out)            # stored at the dock, given to nobody, not sold
        self.assertTrue(any("is not a pilot of ours" in note for note in row["notes"]), row["notes"])


# hunt.py run whole: its module level as it stands, `call` answered by a fake gate, its file paths in a made-up folder
FAKE_HUNT = r'''
import ast, json, pathlib, sys, time, types
CONFIG = json.loads(pathlib.Path(sys.argv[1]).read_text())
WORLD, LOG = CONFIG["world"], []
time.sleep = lambda seconds: None
sys.modules["division"] = types.SimpleNamespace(require=lambda pilot: None)
sys.argv = ["hunt.py"] + CONFIG["argv"]
TMP = CONFIG["tmp"]


def call(method, path, body=None, timeout=900):
    if method == "GET" and path.endswith("/state/cargo"):
        return 200, [{"item_id": k, "quantity": v} for k, v in sorted(WORLD["cargo"].items()) if v]
    if method == "GET":
        return 200, {"state": {"credits": WORLD["credits"]}}
    if method == "PATCH" or path.endswith("/combat-heartbeat"):
        return 200, {}
    if path.endswith("/goal"):
        LOG.append(["goal", body["type"]])
        return 200, {"success": True}
    action, params = body["action"], body["params"]
    LOG.append([action, params])
    if action == "get_nearby":
        return 200, {"structuredContent": {"creatures": None, "creature_count": 0}}
    if action == "view_market":
        return 200, {"structuredContent": {"items": [{"item_id": "veil_curd", "best_buy": 300, "best_buy_qty": 50, "buy_quantity": 50}]}}
    if action == "view":
        return 200, {"structuredContent": {"items": [{"item_id": k, "quantity": v} for k, v in sorted(WORLD["storage"].items()) if v]}}
    if action == "sell":
        units = min(params["quantity"], WORLD["cargo"].get(params["item_id"], 0))
        WORLD["cargo"][params["item_id"]] -= units
        WORLD["credits"] += units * 300
        return 200, {}
    if action == "deposit" and params.get("target") == "self":
        WORLD["storage"][params["item_id"]] = WORLD["storage"].get(params["item_id"], 0) + WORLD["cargo"].pop(params["item_id"], 0)
        return 200, {}
    if action == "deposit":
        given = WORLD.setdefault("given", {}).setdefault(params["target"], {})
        for row in params.get("items") or [{"item_id": params["item_id"], "quantity": params["quantity"]}]:
            units = min(row["quantity"], WORLD["cargo"].get(row["item_id"], 0))
            WORLD["cargo"][row["item_id"]] -= units
            given[row["item_id"]] = given.get(row["item_id"], 0) + units
        return 200, {}
    if action == "status":
        return 200, {"structuredContent": {"is_participant": False}}
    return 200, {"structuredContent": {}}


PATHS = {"SHIPS": TMP + "/ships/", "MARKET": TMP + "/market/", "ORDER": TMP + "/order.json", "RUNS": TMP + "/runs.jsonl"}
tree = ast.parse(pathlib.Path(CONFIG["runner"]).read_text(encoding="ascii"))
keep = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("call", "save_herd", "kept_goods", "own_names"):
        continue                                          # the fake gate answers; no herd, no reserve, no fleet file of the unit is read
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in PATHS:
        node = ast.copy_location(ast.parse("%s = %r" % (node.targets[0].id, PATHS[node.targets[0].id])).body[0], node)
    keep.append(node)
tree.body = keep
space = {"__name__": "__main__", "__file__": CONFIG["runner"], "call": call, "save_herd": lambda near: None, "kept_goods": lambda data, root: {},
         "own_names": lambda: set()}
try:
    exec(compile(ast.fix_missing_locations(tree), CONFIG["runner"], "exec"), space)
except SystemExit:
    pass
finally:
    pathlib.Path(CONFIG["log"]).write_text(json.dumps({"log": LOG, "world": WORLD}))
'''


def fly_hunt(argv, world, data, switch):
    with tempfile.TemporaryDirectory() as folder:
        (Path(folder) / "market").mkdir()
        path = Path(data) / "fleet" / "strict-classes-on"
        path.write_text("") if switch else (path.exists() and path.unlink())
        config = {"world": world, "argv": argv, "runner": str(FLEET / "hunt.py"), "tmp": folder, "log": str(Path(folder) / "log.json")}
        (Path(folder) / "config.json").write_text(json.dumps(config))
        done = subprocess.run([sys.executable, "-I", "-B", "-c", FAKE_HUNT, str(Path(folder) / "config.json")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, timeout=120, env=dict(os.environ, FLEET_DATA_ROOT=str(data)), cwd=str(FLEET))
        out = json.loads((Path(folder) / "log.json").read_text())
        rows = [json.loads(line) for line in (Path(folder) / "runs.jsonl").read_text().splitlines()] if (Path(folder) / "runs.jsonl").exists() else [{}]
    return out["log"], out["world"], rows[-1], done.stdout


class HuntHandOverTests(Data):
    """A hunt route's `gift_to`: at `sell_at` nothing is sold, the loot goes to the trader's storage there."""
    ARGV = ["drone-1", "far", "cloud", "--kills", "1", "--minutes", "1", "--sell-at", "home:core:central_nexus", "--route", "hunt-x", "--min-bid", "50"]
    WORLD = {"credits": 9000, "cargo": {"veil_curd": 4, "carapace": 2}, "storage": {}}

    def test_with_the_switch_on_the_loot_goes_to_the_trader_and_nothing_is_sold(self):
        log, world, row, out = fly_hunt(self.ARGV + ["--gift-to", "trader"], json.loads(json.dumps(self.WORLD)), self.data, True)
        self.assertNotIn("sell", [step[0] for step in log], out)
        self.assertEqual(world["given"], {"trader-9": {"carapace": 2, "veil_curd": 4}}, out)
        self.assertIn("RESULT gift drone-1 -> trader-9 at central_nexus: carapace 2, veil_curd 4", out)
        self.assertEqual(row.get("sold"), {}, out)

    def test_with_the_switch_off_the_hunt_sells_as_before(self):
        log, world, row, out = fly_hunt(self.ARGV + ["--gift-to", "trader"], json.loads(json.dumps(self.WORLD)), self.data, False)
        self.assertIn("sell", [step[0] for step in log], out)
        self.assertNotIn("given", world)

    def test_what_a_gift_leaves_aboard_is_stored_never_sold(self):
        log, world, row, out = fly_hunt(self.ARGV + ["--gift-to", "Strange Pilot"], json.loads(json.dumps(self.WORLD)), self.data, True)
        self.assertNotIn("sell", [step[0] for step in log], out)
        self.assertEqual(world["storage"], {"veil_curd": 4, "carapace": 2}, out)
        self.assertTrue(any("is not a pilot of ours" in note for note in row.get("notes") or []), row)


if __name__ == "__main__":
    unittest.main()


class UndockedGiverTests(Data):
    """Apophis, requests ENT-352 (2): 15 of 783 give runs since 09:35 UTC on 2026-11-22 gave nothing, every deposit
    answered `not_docked`; the goods stayed with the giver and the same ship was sent again. A refused gift docks
    once and tries again; the note says so."""

    def test_a_gift_refused_for_an_undocked_giver_docks_once_and_gives(self):
        state = {"docked": False, "hold": {"creature_carapace": 12, "lead_ore": 3}, "given": {}}
        calls = []

        def raw(action, params=None, group="spacemolt"):
            calls.append(action)
            if action == "dock":
                state["docked"] = True
                return {"structuredContent": {"ok": True}}
            if action == "view":
                return {"structuredContent": {"items": []}}
            if action == "deposit":
                if not state["docked"]:
                    return {"error": "API call failed: not_docked: You must be docked at a station to perform this act"}
                for row in params.get("items") or [{"item_id": params["item_id"], "quantity": params["quantity"]}]:
                    state["hold"][row["item_id"]] -= row["quantity"]
                return {"structuredContent": {"ok": True}}
            return {}

        out = handover.give(raw, lambda: dict(state["hold"]), lambda text: None, lambda s: None, "drone-8", "central_nexus",
                            {"to": "trader", "items": "all", "source": "cargo"}, str(self.data), "give-drone-stores-central-nexus")
        self.assertEqual(out["given"], {"creature_carapace": 12, "lead_ore": 3})
        self.assertEqual(calls.count("dock"), 1)
        self.assertIn("docked again", out["note"] or "")
        self.assertIn("docked again", out["line"])
