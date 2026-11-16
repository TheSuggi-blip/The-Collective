"""game/fleet/collective_mcp.py: the protocol over stdin and stdout, the tool list, and the script line each tool builds. No engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


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
        self.assertEqual((env["HF_HUB_OFFLINE"], env["TRANSFORMERS_OFFLINE"], env["HERMES_SESSION_PROFILE"]), ("1", "1", "zero"))

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
        self.assertEqual(self.plan("routes", group="paying", zone="beyond"), [("game/fleet/hive.py", ["routes", "--group", "paying", "--zone", "beyond"])])
        self.assertEqual(self.plan("fill"), [("game/fleet/fill.py", ["status"])])
        self.assertEqual(self.plan("fill", action="fill", who="miner", write=True, tests=4), [("game/fleet/fill.py", ["fill", "miner", "--write", "--tests", "4"])])
        self.assertEqual(self.plan("fill", action="lift", route="mine-x", ships=6), [("game/fleet/fill.py", ["lift", "mine-x", "6"])])
        self.assertEqual(self.plan("fill", action="add", route="mine-x", first=True), [("game/fleet/fill.py", ["add", "mine-x", "--first"])])
        self.assertEqual(self.plan("catalog", ask="needs", name="outpost_kit", quantity=2), [("game/fleet/craftbook.py", ["needs", "outpost_kit", "2"])])
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
        self.assertEqual(sorted(name for name, h in hints.items() if not h["readOnlyHint"]), ["command", "fill", "goal", "hold"])
        self.assertEqual(sorted(name for name, h in hints.items() if h["destructiveHint"]), ["command", "goal", "hold"])

    def test_the_door_is_marked_and_every_script_exists(self):
        self.assertEqual(sorted(name for name, tool in self.server.TOOLS.items() if tool.get("door")), ["command", "goal", "hold"])
        samples = {"ship": {"pilot": "p"}, "route": {"id": "r"}, "market": {"item": "i"}, "base_plan": {"kind": "outpost"}, "system": {"id": "s"}, "search": {"question": "q"},
                   "command": {"pilots": ["p"], "action": "a"}, "goal": {"pilot": "p", "type": "t"}, "hold": {"pilot": "p"}, "hive": {"verb": "fleet"}, "catalog": {"name": "x"}}
        for name, tool in self.server.TOOLS.items():
            for script, _argv in tool["plan"](samples.get(name, {})):
                self.assertTrue((REPO / script).is_file(), "%s: %s" % (name, script))


if __name__ == "__main__":
    unittest.main()
