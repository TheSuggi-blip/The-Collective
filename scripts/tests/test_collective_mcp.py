"""game/fleet/collective_mcp.py: the protocol over stdin and stdout, the tool list, and the script line each tool builds. No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


REPO = Path(__file__).resolve().parents[2]
SERVER = REPO / "game" / "fleet" / "collective_mcp.py"


def load():
    spec = importlib.util.spec_from_file_location("collective_mcp_under_test", SERVER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def talk(messages, member="zero"):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HERMES_SESSION_PROFILE": member, "HOME": "/nonexistent"}
    done = subprocess.run([sys.executable, "-I", "-B", str(SERVER)], input="".join(json.dumps(m) + "\n" for m in messages), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, env=env, timeout=120)
    return [json.loads(line) for line in done.stdout.splitlines() if line.strip()]


class FlagTests(__import__("unittest").TestCase):
    """requests ENT-212 (Zero, 2026-11-17): the tool fill with tests=0 wrote four tests; flag() dropped the 0."""

    def test_a_zero_is_passed_on_and_only_none_empty_and_false_are_dropped(self):
        import importlib.util
        from pathlib import Path as P
        spec = importlib.util.spec_from_file_location("mcp_flag_under_test", P(__file__).resolve().parents[2] / "game" / "fleet" / "collective_mcp.py")
        mcp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mcp)
        self.assertEqual(mcp.flag({"tests": 0}, "tests"), ["--tests", "0"])
        self.assertEqual(mcp.flag({"floor": 0}, "floor"), ["--floor", "0"])
        self.assertEqual(mcp.flag({"tests": 3}, "tests"), ["--tests", "3"])
        for empty in (None, "", False):
            self.assertEqual(mcp.flag({"tests": empty}, "tests"), [])
        self.assertEqual(mcp.flag({}, "tests"), [])


class ProtocolTests(unittest.TestCase):
    def test_a_session_from_the_handshake_to_a_call(self):
        answers = talk([
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "hive", "arguments": {"verb": "help"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "no-such-tool", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "route", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 6, "method": "no/such/method"},
            {"jsonrpc": "2.0", "id": 7, "method": "ping"},
        ])
        self.assertEqual([a["id"] for a in answers], [1, 2, 3, 4, 5, 6, 7])                       # the notification gets no answer
        first = answers[0]["result"]
        self.assertEqual((first["protocolVersion"], first["serverInfo"]["name"], "tools" in first["capabilities"]), ("2025-06-18", "collective", True))
        self.assertIn("You are Zero.", first["instructions"])
        tools = answers[1]["result"]["tools"]
        self.assertEqual(len(tools), len(load().TOOLS))
        for tool in tools:
            self.assertEqual(tool["inputSchema"]["type"], "object", tool["name"])
            self.assertTrue(set(tool["inputSchema"]["required"]) <= set(tool["inputSchema"]["properties"]), tool["name"])
        self.assertIn("hive.py capacity", answers[2]["result"]["content"][0]["text"])             # the script's own help
        self.assertEqual(answers[3]["result"]["isError"], True)
        self.assertEqual((answers[4]["result"]["isError"], answers[4]["result"]["content"][0]["text"]), (True, "route: this needs: id"))
        self.assertEqual(answers[5]["error"]["code"], -32601)
        self.assertEqual(answers[6]["result"], {})

    def test_a_running_server_answers_through_the_file_on_disk(self):
        server = load()
        text, failed = server.fresh(str(SERVER.parents[2]), "", "zero", "no-such-tool", {})
        self.assertTrue(failed)
        self.assertIn("no tool `no-such-tool`", text)
        text, _failed = server.fresh(str(SERVER.parents[2]), "", "zero", "hive", {"verb": "help"})
        self.assertIn("hive.py standing", text)                                                   # the script's own help, from the file on disk
        env = server.child_env("zero")
        self.assertEqual((env["HF_HUB_OFFLINE"], env["HF_HOME"], env["HERMES_SESSION_PROFILE"]), ("1", "/opt/search/cache", "zero"))
        self.assertTrue(env["BRAIN_EMBED_URL"].endswith("/embed"))

    def test_a_script_that_says_no_has_answered_and_only_a_tool_that_did_not_run_is_a_fault(self):
        server = load()
        ends = {"refuses.py": (1, "REFUSED: not yours"), "halts.py": (1, "FLEET | 3 ships wait | HALT"), "mutters.py": (1, "http 500"), "fine.py": (0, "PASS"),
                "crashes.py": (1, "Traceback (most recent call last):\n  boom"), "hangs.py": (124, "TIMEOUT")}
        real = server.run_one
        server.run_one = lambda root, data, member, script, argv: ends[script]
        self.addCleanup(setattr, server, "run_one", real)
        for script in ends:
            server.TOOLS["t-" + script] = {"text": "t", "args": {}, "plan": lambda a, script=script: [(script, [])]}
            self.addCleanup(server.TOOLS.pop, "t-" + script)
        ask = lambda script: server.call("/nowhere", "", "zero", "t-" + script, {})
        self.assertEqual(ask("refuses.py"), ("REFUSED: not yours", False))                        # an answer: Hermes pauses a server after three faults in a row
        self.assertEqual(ask("halts.py"), ("FLEET | 3 ships wait | HALT", False))
        self.assertEqual(ask("mutters.py"), ("NOT DONE: the script ended with exit 1 and these words:\nhttp 500", False))
        self.assertEqual(ask("fine.py"), ("PASS", False))
        self.assertEqual((ask("crashes.py")[1], ask("hangs.py")[1], server.call("/nowhere", "", "zero", "no-such-tool", {})[1]), (True, True, True))

    def test_a_shell_that_is_no_member_reads_and_is_told_so(self):
        first = talk([{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}], member="")[0]["result"]
        self.assertIn("no member: the door is closed", first["instructions"])


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.server = load()

    def plan(self, tool, **args):
        return self.server.TOOLS[tool]["plan"](args)

    def test_each_tool_builds_the_line_of_one_script(self):
        self.assertEqual(self.plan("fleet"), [("game/fleet/hive.py", ["fleet"])])
        self.assertEqual(self.plan("fleet", view="board", member="Zero", hours=8), [("game/fleet/board.py", ["Zero", "--hours", "8"])])
        self.assertEqual(self.plan("fleet", view="kpi"), [("game/fleet/hive.py", ["stats", "kpi"])])
        self.assertEqual(self.plan("fleet", view="contribution", member="Oracle", hours=6),
                         [("game/fleet/hive.py", ["stats", "contribution", "--member", "Oracle", "--hours", "6"])])
        for view in ("classes", "time", "supply", "xp", "upgrades", "alerts"):
            self.assertEqual(self.plan("fleet", view=view), [("game/fleet/hive.py", ["stats", view])])
        self.assertEqual(self.plan("fleet", view="refill"), [("game/fleet/hive.py", ["refill"])])      # the store's table stats_refill
        self.assertIn("kpi", self.server.TOOLS["fleet"]["args"]["view"]["enum"])
        self.assertEqual(self.plan("routes", group="paying", zone="beyond"), [("game/fleet/hive.py", ["routes", "--group", "paying", "--zone", "beyond"])])
        self.assertEqual(self.plan("fill"), [("game/fleet/fill.py", ["status"])])
        self.assertEqual(self.plan("fill", action="fill", who="miner", write=True, tests=4), [("game/fleet/fill.py", ["fill", "miner", "--write", "--tests", "4"])])
        self.assertEqual(self.plan("fill", action="lift", route="mine-x", ships=6), [("game/fleet/fill.py", ["lift", "mine-x", "6"])])
        self.assertEqual(self.plan("fill", action="add", route="mine-x", first=True), [("game/fleet/fill.py", ["add", "mine-x", "--first"])])
        self.assertEqual(self.plan("catalog", ask="needs", name="outpost_kit", quantity=2), [("game/fleet/craftbook.py", ["needs", "outpost_kit", "2"])])
        self.assertEqual(self.plan("stock", member="Zero", item="iron_ore"), [("game/fleet/ledger.py", ["show", "Zero", "--item", "iron_ore"])])
        self.assertEqual(self.plan("stock", view="inventory", top=5), [("game/fleet/craftbook.py", ["inventory", "--top", "5"])])
        self.assertEqual(self.plan("stock", view="stations", item="iron_ore"), [("game/fleet/craftbook.py", ["inventory", "stations", "--item", "iron_ore"])])
        self.assertEqual(self.plan("stock", view="surplus", kind="raw", top=5), [("game/fleet/surplus.py", ["show", "--kind", "raw", "--top", "5"])])
        self.assertEqual(self.plan("stock", view="surplus", item="iron_ore"), [("game/fleet/surplus.py", ["show", "--item", "iron_ore"])])
        self.assertEqual(self.plan("stock", view="reserve"), [("game/fleet/surplus.py", ["reserve"])])
        self.assertEqual(self.plan("sql", query="SELECT 1", limit=5), [("game/fleet/hive.py", ["sql", "SELECT 1", "--limit", "5"])])
        self.assertEqual(self.plan("sql"), [("game/fleet/hive.py", ["schema"])])
        self.assertEqual(self.plan("sql", table="route_earnings"), [("game/fleet/hive.py", ["schema", "route_earnings"])])
        self.assertEqual(self.plan("sql", table="all"), [("game/fleet/hive.py", ["schema"])])
        self.assertEqual(self.plan("plan"), [("game/fleet/plan.py", ["show"])])
        self.assertEqual(self.plan("plan", action="show", division="all", brief=True), [("game/fleet/plan.py", ["show", "all", "--brief"])])
        self.assertEqual(self.plan("plan", action="set", ships="miner-1..10", routes="ice-a,gather"), [("game/fleet/plan.py", ["set", "miner-1..10", "ice-a,gather"])])
        self.assertEqual(self.plan("plan", action="then", routes="census,park", division="mining"), [("game/fleet/plan.py", ["then", "census,park", "--division", "mining"])])
        self.assertEqual(self.plan("plan", action="templates"), [("game/fleet/plan.py", ["templates"])])
        self.assertEqual(self.plan("plan", action="templates", division="all"), [("game/fleet/plan.py", ["templates", "all"])])
        self.assertEqual(self.plan("plan", action="template", name="ice-loop", routes="ice-a,gather", title="Ice", trains="mining", note="n", division="mining"),
                         [("game/fleet/plan.py", ["template", "ice-loop", "ice-a,gather", "--title", "Ice", "--trains", "mining", "--note", "n", "--division", "mining"])])
        self.assertEqual(self.plan("plan", action="template", name="ice-loop", routes="none"), [("game/fleet/plan.py", ["template", "ice-loop", "none"])])
        self.assertEqual(self.plan("plan", action="use", ships="miner-1..10", name="ice-loop,far-ice"), [("game/fleet/plan.py", ["use", "miner-1..10", "ice-loop,far-ice"])])
        for args in ({"action": "template", "name": "ice-loop"}, {"action": "use", "ships": "miner-1"}):
            with self.assertRaises(ValueError):
                self.plan("plan", **args)
        self.assertEqual(self.plan("candidates", id="mine-x"), [("game/fleet/routemaker.py", ["route", "mine-x"])])
        self.assertEqual(self.plan("comms", view="requests", member="Zero"), [("scripts/comms.py", ["requests", "--to", "Zero"])])
        self.assertEqual(self.plan("hold", pilot="miner-1", release=True), [("game/fleet/gate.py", ["release", "miner-1"])])
        self.assertEqual(self.plan("goal", pilot="miner-1", type="dock-at", options={"base": "b"}), [("game/fleet/gate.py", ["goal", "miner-1", "dock-at", '{"base": "b"}'])])

    def test_one_command_to_many_ships_is_one_line_a_ship(self):
        lines = self.plan("command", pilots=["miner-1", "miner-2"], action="get_status")
        self.assertEqual(lines, [("game/fleet/gate.py", ["raw", "miner-1", "get_status", "{}"]), ("game/fleet/gate.py", ["raw", "miner-2", "get_status", "{}"])])
        with self.assertRaises(ValueError):
            self.plan("command", pilots=["p%d" % n for n in range(41)], action="get_status")
        with self.assertRaises(ValueError):
            self.plan("fill", action="lift", route="mine-x")

    def test_a_call_through_the_door_leaves_one_line_and_a_reading_call_none(self):
        import tempfile
        with tempfile.TemporaryDirectory(prefix="collective-mcp-door-") as temp:
            self.server.run_one = lambda root, data, member, script, argv: (0, "held: miner-1\n")
            self.assertEqual(self.server.call(str(REPO), temp, "Zero", "hold", {"pilot": "miner-1"}), ("held: miner-1", False))
            self.server.call(str(REPO), temp, "Zero", "ship", {"pilot": "miner-1"})
            lines = [json.loads(line) for line in (Path(temp) / "fleet" / "door.jsonl").read_text().splitlines()]
        self.assertEqual([(r["who"], r["tool"], r["args"], r["ok"], r["answer"]) for r in lines], [("Zero", "hold", {"pilot": "miner-1"}, True, "held: miner-1")])

    def test_the_tools_carry_the_protocols_hints(self):
        hints = {name: self.server.schema(name)["annotations"] for name in self.server.TOOLS}
        self.assertEqual(sorted(name for name, h in hints.items() if not h["readOnlyHint"]), ["command", "fill", "fund", "goal", "hold", "needs", "plan", "stop"])
        self.assertEqual(sorted(name for name, h in hints.items() if h["destructiveHint"]), ["command", "fund", "goal", "hold", "stop"])

    def test_the_door_is_marked_and_every_script_exists(self):
        self.assertEqual(sorted(name for name, tool in self.server.TOOLS.items() if tool.get("door")), ["command", "fund", "goal", "hold", "stop"])
        samples = {"ship": {"pilot": "p"}, "route": {"id": "r"}, "market": {"item": "i"}, "base_plan": {"kind": "outpost"}, "system": {"id": "s"}, "search": {"question": "q"},
                   "command": {"pilots": ["p"], "action": "a"}, "goal": {"pilot": "p", "type": "t"}, "hold": {"pilot": "p"}, "stop": {"list": True}, "fund": {"show": True}, "hive": {"verb": "fleet"}, "catalog": {"name": "x"}}
        for name, tool in self.server.TOOLS.items():
            for script, _argv in tool["plan"](samples.get(name, {})):
                self.assertTrue((REPO / script).is_file(), "%s: %s" % (name, script))


if __name__ == "__main__":
    unittest.main()
