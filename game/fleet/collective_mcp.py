#!/usr/bin/env python3
"""collective_mcp.py -- the collective MCP server: the fleet's knowledge and the door to its ships, as tools for every member.

WHAT: a Model Context Protocol server over stdin and stdout (JSON-RPC, one message a line). Hermes starts it for a
      member (`mcp_servers.collective` in the profile's settings) and the member sees its tools as
      `mcp_collective_<tool>`. A tool is one row of TOOLS below: it runs one of the fleet's own scripts with the
      member's arguments and hands back what the script printed. The scripts stay the one source of every figure:
        knowledge   fleet, ship, routes, route, candidates, market, stock, catalog, base_plan, system, comms, search
        the door    fill (why ships wait; fill, add, drop, lift a plan), command (one game command to one or many
                    ships), goal (an engine goal for one ship), hold (take or release a ship by hand)
        hive        any verb of hive.py by name: a verb added after this server started is reachable at once
RULES:
  - The server holds no figure and no rule of its own. Who may command which ship is division.py's lock inside
    gate.py and fill.py: an Admiral commands its own ships and changes its own plans, the Fleet Admiral any.
  - Every call through the door leaves one line in data/fleet/door.jsonl: who, tool, arguments, how it ended.
  - The member is the profile Hermes runs the server for (HERMES_SESSION_PROFILE, set where the server is
    registered); every script it starts runs as that member.
  - A script runs for 110 s at most; an answer longer than 30,000 characters is cut and says so.
  - A new tool is a new row in TOOLS and needs a new Hermes process to be seen; a new verb of hive.py does not.
WHY:  an Admiral's turn spent its first half hour finding which script answers what, and commanded ships one shell
      line at a time. One tool list, the same for all six, makes the fleet's data and its ships one call away.

USAGE:
  collective_mcp.py                      serve (started by Hermes)
  collective_mcp.py --list               the tools, one line each
  collective_mcp.py --call <tool> ['<json arguments>']
                                         run one tool and print its answer: a test without Hermes
  --root <dir>   the repository (default: the one this file lies in)
  --data <dir>   the unit's data folder, handed to the scripts (default: theirs)

Stdlib only. ASCII only.
"""

import fcntl
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the member this server runs for

LIMIT = 30000                  # characters of one answer
SECONDS = 110                  # one script
SEARCH = "/opt/search/venv/bin/python"           # the repository search's own Python (query-collective)
SEARCH_ENV = {"BRAIN_EMBED_URL": "http://embed:8099/embed",      # the unit's warm embedder, as a member's shell names it
              "HF_HOME": "/opt/search/cache", "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}   # and the model on disk when the embedder is away
MEMBERS = list(division.MEMBERS) + ["all"]
S, I, B, O, A = "string", "integer", "boolean", "object", "array"


def arg(kind, text, enum=None, items=None):
    out = {"type": kind, "description": text}
    if enum:
        out["enum"] = list(enum)
    if items:
        out["items"] = {"type": items}
    return out


def flag(args, name, option=None):
    """['--name', value] when the argument is given."""
    value = args.get(name)
    return [] if value in (None, "", False) else [option or "--" + name.replace("_", "-"), str(value)]


def need(args, *names):
    missing = [n for n in names if args.get(n) in (None, "", [])]
    if missing:
        raise ValueError("this needs: " + ", ".join(missing))


def fleet_plan(a):
    view = a.get("view") or "money"
    if view == "money":
        return [("game/fleet/hive.py", ["fleet"])]
    if view == "history":
        return [("game/fleet/hive.py", ["history"] + flag(a, "hours"))]
    if view == "levels":
        return [("game/fleet/hive.py", ["levels"] + ([a["member"]] if a.get("member") else []))]
    if view == "capacity":
        return [("game/fleet/hive.py", ["capacity"])]
    if view == "board":
        return [("game/fleet/board.py", ([a["member"]] if a.get("member") else []) + flag(a, "hours"))]
    if view == "standing":
        return [("game/fleet/hive.py", ["standing"] + ([a["member"]] if a.get("member") else []) + flag(a, "hours"))]
    if view == "tasks":
        return [("game/fleet/hive.py", ["tasks"] + flag(a, "hours"))]
    if view == "refill":
        return [("game/fleet/hive.py", ["refill"])]
    raise ValueError("view is one of: money, history, levels, capacity, board, standing, tasks, refill")


def fill_plan(a):
    action = a.get("action") or "status"
    who = [a["who"]] if a.get("who") else []
    if action in ("status", "check"):
        return [("game/fleet/fill.py", [action] + who)]
    if action == "fill":
        return [("game/fleet/fill.py", ["fill"] + who + (["--write"] if a.get("write") else []) + flag(a, "tests") + flag(a, "floor"))]
    if action in ("add", "drop"):
        need(a, "route")
        return [("game/fleet/fill.py", [action, a["route"]] + flag(a, "role") + (["--first"] if a.get("first") and action == "add" else []))]
    if action == "lift":
        need(a, "route", "ships")
        return [("game/fleet/fill.py", ["lift", a["route"], str(a["ships"])])]
    raise ValueError("action is one of: status, check, fill, add, drop, lift")


def catalog_plan(a):
    ask = a.get("ask") or "item"
    if ask in ("item", "needs", "build"):
        need(a, "name")
        return [("game/fleet/craftbook.py", [ask, a["name"]] + ([str(a["quantity"])] if ask == "needs" and a.get("quantity") else []))]
    if ask == "can":
        return [("game/fleet/craftbook.py", ["can"] + ([a["member"]] if a.get("member") else []) + flag(a, "top"))]
    if ask == "recipes":
        return [("game/fleet/craftbook.py", ["recipes"] + flag(a, "category") + flag(a, "makes") + flag(a, "uses") + (["--hand"] if a.get("by_hand") else []))]
    raise ValueError("ask is one of: item, needs, build, can, recipes")


def comms_plan(a):
    view = a.get("view") or "orders"
    if view == "orders":
        return [("scripts/comms.py", ["orders"])]
    if view == "requests":
        return [("scripts/comms.py", ["requests"] + flag(a, "member", "--to"))]
    if view == "digest":
        return [("scripts/comms.py", ["digest"] + flag(a, "last") + flag(a, "member"))]
    if view == "contacts":
        return [("game/fleet/inbox.py", ["show", "--to-us"] + flag(a, "last"))]
    if view == "learnings":
        return [("game/fleet/hive.py", ["learnings"] + flag(a, "hours"))]
    raise ValueError("view is one of: orders, requests, digest, contacts, learnings")


def command_plan(a):
    need(a, "pilots", "action")
    pilots = a["pilots"] if isinstance(a["pilots"], list) else [a["pilots"]]
    if len(pilots) > 40:
        raise ValueError("at most 40 pilots in one call")
    params = json.dumps(a.get("params") or {})
    return [("game/fleet/gate.py", ["raw", str(p), a["action"], params] + ([a["tool_group"]] if a.get("tool_group") else [])) for p in pilots]


def goal_plan(a):
    need(a, "pilot", "type")
    return [("game/fleet/gate.py", ["goal", a["pilot"], a["type"], json.dumps(a.get("options") or {})] + flag(a, "one_time"))]


TOOLS = {
    "fleet": {
        "text": "The fleet in figures. view=money: credits and steady money per hour (income, costs, net; rewards paid once left out) over 1, 6 and 24 hours, per division. "
                "view=history: credits hour by hour per division. view=levels: pilots' levels, XP an hour, hours to the next hull tier. view=capacity: what mining, hunting "
                "and the once-missions carry (bids, what is left in the fields, herds, tools) and how many ships that employs. view=board: a member's ships one line each, "
                "with their orders and last runs. view=standing: the standing fleet of a member: its plan route by route with the credits per ship-hour of each, and "
                "every ship with what it flies, what it earned per hour and what closes the best route to it. view=tasks: credits per ship-hour by kind of work and by "
                "division, idle ships counted. view=refill: what comes back per hour between our readings: bids, fields, herds.",
        "args": {"view": arg(S, "money (default), history, levels, capacity, board, standing, tasks or refill",
                             ("money", "history", "levels", "capacity", "board", "standing", "tasks", "refill")),
                 "member": arg(S, "for levels, board and standing: a member's name, or all", MEMBERS),
                 "hours": arg(I, "for history, board, standing and tasks: the window in hours")},
        "plan": fleet_plan},
    "ship": {
        "text": "One ship of the fleet from its live file: place, docked or not, hull, fuel, hold, modules, wallet, the order it flies, skills, missions held.",
        "args": {"pilot": arg(S, "the pilot's name, e.g. miner-7")}, "required": ["pilot"],
        "plan": lambda a: [("game/fleet/hive.py", ["ship", a["pilot"]])]},
    "routes": {
        "text": "Every route with what it earns: its group (once per pilot, paying, test, fitting, reading and waiting, at a loss, off), zone, ships on it against its "
                "limit, the credits per ship-hour its runs measured, and its runs, steady credits and credits per ship-hour in the last hours. Filter by group, kind or zone.",
        "args": {"group": arg(S, "once, paying, test, fit, service, losing or off", ("once", "paying", "test", "fit", "service", "losing", "off")),
                 "kind": arg(S, "circuit, hunt, mine or census", ("circuit", "hunt", "mine", "census")), "zone": arg(S, "home or beyond (the border)", ("home", "beyond")),
                 "hours": arg(I, "the window of the runs, default 4")},
        "plan": lambda a: [("game/fleet/hive.py", ["routes"] + flag(a, "group") + flag(a, "kind") + flag(a, "zone") + flag(a, "hours"))]},
    "route": {
        "text": "One route in full: its file's facts, who flies it now, its last twelve runs with credits and notes, and its credits per ship-hour hour by hour over 24 hours.",
        "args": {"id": arg(S, "the route id, e.g. mine-ruchbah-ice-belt")}, "required": ["id"],
        "plan": lambda a: [("game/fleet/hive.py", ["route", a["id"]])]},
    "fill": {
        "text": "Keep every ship at work (orders F8). action=status: per role how many ships work, start and wait, why each route of the plan is closed to the waiting "
                "pilots, and what work stands open outside the plan. action=check: the gate, PASS or HALT. action=fill: put the open paying routes and tests into your "
                "plan (write=true commits it; the dispatcher starts the ships within the minute). action=add or drop: one route into or out of a plan. action=lift: "
                "set a route's max_ships. You change the plans of your own roles only.",
        "args": {"action": arg(S, "status (default), check, fill, add, drop or lift", ("status", "check", "fill", "add", "drop", "lift")),
                 "who": arg(S, "for status, check and fill: a member's name, a role (miner, trader, hauler, drone, scout, sentinel, command) or all"),
                 "route": arg(S, "for add, drop and lift: the route id"), "role": arg(S, "for add and drop: the plan's role, when you keep more than one"),
                 "ships": arg(I, "for lift: the new max_ships"), "first": arg(B, "for add: at the head of the plan instead of in front of the census and park routes"),
                 "write": arg(B, "for fill: write and commit; without it the answer only lists what would be added"),
                 "tests": arg(I, "for fill: at most this many tests added per role, default 8"), "floor": arg(I, "for fill: a candidate counts from this estimate, default 500")},
        "plan": fill_plan},
    "candidates": {
        "text": "Ways to earn that the route maker computed from our own readings (fields, order books, mission boards, herds, recipes), best first, with the estimate "
                "per ship-hour, what it rests on, its warnings and what it still needs. With id: the ready route file of one candidate.",
        "args": {"member": arg(S, "whose ships: a member's name or all", MEMBERS), "kind": arg(S, "mine, trade, craft, hunt or mission", ("mine", "trade", "craft", "hunt", "mission")),
                 "top": arg(I, "how many, default 20"), "id": arg(S, "one candidate's id: prints its route file instead of the list")},
        "plan": lambda a: [("game/fleet/routemaker.py", ["route", a["id"]])] if a.get("id") else
                          [("game/fleet/routemaker.py", ["show"] + ([a["member"]] if a.get("member") else []) + flag(a, "kind") + flag(a, "top"))]},
    "market": {
        "text": "The last moves of one item's best bid and best ask at the stations whose order books our ships read: what it sells for, what it costs, how deep, when read.",
        "args": {"item": arg(S, "the item id, e.g. water_ice"), "base": arg(S, "one station's base id"), "last": arg(I, "how many moves, default 20")}, "required": ["item"],
        "plan": lambda a: [("game/fleet/ledger.py", ["prices", a["item"]] + flag(a, "base") + flag(a, "last"))]},
    "stock": {
        "text": "What our ships hold in station storage and in their holds, per member or for the whole fleet, optionally one item.",
        "args": {"member": arg(S, "a member's name or all", MEMBERS), "item": arg(S, "one item id")},
        "plan": lambda a: [("game/fleet/ledger.py", ["show"] + ([a["member"]] if a.get("member") else []) + flag(a, "item"))]},
    "catalog": {
        "text": "The game's catalog asked as a question. ask=item: find an item by text; for one item how it is made, what uses it, what is built with it. ask=needs: "
                "everything a number of units takes down to what is mined or bought, beside what we store. ask=build: what a facility or a hull costs and takes. "
                "ask=can: what a member's stored goods can be made into by hand today and what that sells for. ask=recipes: the recipes of a category, or that make or "
                "use an item. The same tables as files: game/catalog/master-index.md.",
        "args": {"ask": arg(S, "item (default), needs, build, can or recipes", ("item", "needs", "build", "can", "recipes")),
                 "name": arg(S, "for item: text or an item id; for needs: an item id; for build: a facility id or a hull id"), "quantity": arg(I, "for needs: units, default 1"),
                 "member": arg(S, "for can: a member's name or all", MEMBERS), "top": arg(I, "for can: how many rows"), "category": arg(S, "for recipes: a category name"),
                 "makes": arg(S, "for recipes: an item id it makes"), "uses": arg(S, "for recipes: an item id it uses"), "by_hand": arg(B, "for recipes: only those crafted by hand")},
        "plan": catalog_plan},
    "base_plan": {
        "text": "What founding an outpost or a station of our own takes, from the catalog and our readings: the fee, the part, the facility that makes the part, every "
                "input down to the ore, what we hold, what is missing and where it is found or sold, and whether the finished part is on offer.",
        "args": {"kind": arg(S, "outpost or station", ("outpost", "station"))}, "required": ["kind"],
        "plan": lambda a: [("game/fleet/hive.py", ["base", a["kind"]])]},
    "system": {
        "text": "One star system from our readings: whose space, jumps from home, its places, what is left in its fields, its herds, its market, the pilots of others met "
                "there, our ships there, the routes that touch it.",
        "args": {"id": arg(S, "the system id, e.g. node_beta")}, "required": ["id"],
        "plan": lambda a: [("game/fleet/hive.py", ["system", a["id"]])]},
    "comms": {
        "text": "The Collective's logs. view=orders: the orders in force, complete. view=requests: the board of requests not closed. view=digest: the last entries of "
                "every log. view=contacts: messages other players wrote to our ships. view=learnings: each member's newest report and the knowledge files it wrote "
                "or changed.",
        "args": {"view": arg(S, "orders (default), requests, digest, contacts or learnings", ("orders", "requests", "digest", "contacts", "learnings")),
                 "member": arg(S, "for requests: addressed to this member; for digest: entries of this member"), "last": arg(I, "for digest and contacts: how many entries"),
                 "hours": arg(I, "for learnings: the window in hours, default 8")},
        "plan": comms_plan},
    "search": {
        "text": "Search the Collective's repository by meaning (rules, map, planets, players, factions, routes, guidebooks, reports, catalog): the passages that answer a question.",
        "args": {"question": arg(S, "the question, in plain words"), "top": arg(I, "how many passages, default 8")}, "required": ["question"],
        "plan": lambda a: [("collective-index/query.py", [a["question"], "--top-k", str(a.get("top") or 8)])]},
    "command": {
        "text": "Send one game command to one or many of your ships through the engine's gate, at once (up to 40 pilots, six at a time). The first command takes a "
                "ship by hand: the dispatcher leaves it alone until you release it (tool hold) or 20 minutes pass. Refused for a ship of another division and for a "
                "ship a runner is flying. Reading commands (get_status, view_market, get_system ...) are free.",
        "args": {"pilots": arg(A, "the pilots' names", items=S), "action": arg(S, "the game command, e.g. travel, dock, sell, get_status"),
                 "params": arg(O, "the command's parameters"), "tool_group": arg(S, "the engine's tool group when the command is not in the main one: spacemolt_market, "
                                                                                "spacemolt_storage, spacemolt_battle, spacemolt_faction, spacemolt_social")},
        "required": ["pilots", "action"], "plan": command_plan, "door": True},
    "goal": {
        "text": "Give one of your ships an engine goal: a task the engine carries out by itself over many ticks (travel-to, dock-at, sell-items, buy-items, "
                "complete-mission ...). one_time names the mission whose reward is paid once, so it is booked as one-time money.",
        "args": {"pilot": arg(S, "the pilot's name"), "type": arg(S, "the goal type"), "options": arg(O, "the goal's options"),
                 "one_time": arg(S, "the mission's title, for a hand-in that pays once")},
        "required": ["pilot", "type"], "plan": goal_plan, "door": True},
    "hold": {
        "text": "Take one of your ships by hand (the dispatcher gives it no route) or, with release=true, give it back to the dispatcher. Always release a ship you no "
                "longer drive: a held ship earns nothing.",
        "args": {"pilot": arg(S, "the pilot's name"), "release": arg(B, "true: give it back to the dispatcher")}, "required": ["pilot"],
        "plan": lambda a: [("game/fleet/gate.py", ["release" if a.get("release") else "hold", a["pilot"]])], "door": True},
    "hive": {
        "text": "Any verb of game/fleet/hive.py by name, with its arguments as a list: the way to a figure added after this tool list was loaded. verb=help prints "
                "what exists now.",
        "args": {"verb": arg(S, "the verb, or help"), "args": arg(A, "its arguments", items=S)}, "required": ["verb"],
        "plan": lambda a: [("game/fleet/hive.py", (["--help"] if a["verb"] == "help" else [a["verb"]] + [str(x) for x in a.get("args") or []]))]},
}


WRITES = ("fill", "command", "goal", "hold")      # every other tool only reads


def schema(name):
    tool = TOOLS[name]
    hints = {"readOnlyHint": name not in WRITES, "destructiveHint": bool(tool.get("door")), "idempotentHint": name not in ("command", "goal"), "openWorldHint": False}
    return {"name": name, "description": tool["text"], "annotations": hints,
            "inputSchema": {"type": "object", "properties": tool["args"], "required": tool.get("required", [])}}


def audit(data, member, name, args, failed, text):
    """One line per call through the door, in data/fleet/door.jsonl: who, which tool, with what, how it ended. Never fails a call."""
    try:
        path = Path(data or division.DATA) / "fleet" / "door.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        row = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "who": member or "no member", "tool": name, "args": args, "ok": not failed,
               "answer": " ".join(str(text).split())[:300]}
        with open(path, "a", encoding="utf-8") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    except OSError:
        pass


def child_env(member):
    env = dict(os.environ)
    if member:
        env["HERMES_SESSION_PROFILE"] = member.lower()
    env.pop("PYTHONPATH", None)
    for key, value in SEARCH_ENV.items():              # Hermes starts a server with a bare environment: the search needs these to find its model
        env.setdefault(key, value)
    return env


def run_one(root, data, member, script, argv):
    """(exit code, what the script printed)."""
    path = Path(root) / script
    python = SEARCH if script.startswith("collective-index/") and Path(SEARCH).exists() else sys.executable
    line = [python] + ([] if python == SEARCH else ["-I", "-B"]) + [str(path)] + list(argv)
    if data and script.startswith("game/fleet/") and not script.endswith("gate.py"):
        line += ["--data", data]
    try:
        done = subprocess.run(line, cwd=str(root), env=child_env(member), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=SECONDS)
        return done.returncode, done.stdout
    except subprocess.TimeoutExpired as error:
        return 124, "%s\nTIMEOUT: `%s` did not end within %d s" % (error.stdout or "", script, SECONDS)
    except OSError as error:
        return 127, "could not start `%s`: %s" % (script, error)


def call(root, data, member, name, args):
    """(text, True when it failed) of one tool call."""
    tool = TOOLS.get(name)
    if tool is None:
        return "no tool `%s`: %s" % (name, ", ".join(sorted(TOOLS))), True
    try:
        need(args, *tool.get("required", []))
        plan = tool["plan"](args)
    except (ValueError, KeyError, TypeError) as error:
        return "%s: %s" % (name, error), True
    if len(plan) == 1:
        code, text = run_one(root, data, member, *plan[0])
        failed = code != 0
    else:                                                          # one command to many ships: six at a time, one block each
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda step: run_one(root, data, member, *step), plan))
        failed = all(code != 0 for code, _text in results)
        text = "\n".join("%s: %s%s" % (step[1][1], "" if code == 0 else "FAILED: ", " ".join(out.split())[:700]) for step, (code, out) in zip(plan, results))
        text = "%d of %d went through\n%s" % (sum(1 for code, _t in results if code == 0), len(results), text)
    text = text.strip() or "(the script printed nothing; exit %s)" % ("0" if not failed else "not 0")
    if tool.get("door"):
        audit(data, member, name, args, failed, text)
    if len(text) > LIMIT:
        text = text[:LIMIT] + "\n... CUT at %d of %d characters: narrow the question (a filter, one member, fewer rows)" % (LIMIT, len(text))
    return text, failed


def fresh(root, data, member, name, args):
    """(text, True when it failed) of one tool call, answered by a new process of this file as it stands on disk now.

    A server lives for days inside Hermes and keeps the code it started with: answered this way, a change of a tool's code
    needs no reload of the server (a new tool name or argument still does: the list is read once). When the file on disk
    cannot answer (it does not start, or ends at once without a word), the code in memory answers a reading call; a call
    through the door is never sent a second time."""
    line = [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--root", str(root)] + (["--data", data] if data else []) + ["--call", str(name), json.dumps(args)]
    door = bool((TOOLS.get(name) or {}).get("door"))
    try:
        done = subprocess.run(line, env=child_env(member), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=SECONDS + 60)
    except subprocess.TimeoutExpired:
        return "TIMEOUT: `%s` did not answer within %d s; read the ship before sending it again" % (name, SECONDS + 60), True
    except OSError as error:
        return ("%s: the tool's file could not be started: %s" % (name, error), True) if door else call(root, data, member, name, args)
    text = done.stdout.rstrip("\n")
    if done.returncode not in (0, 1) or not text.strip():
        why = " ".join((done.stderr or "").split())[-300:]
        return ("%s: the tool's file on disk gave no answer (%s)" % (name, why or "exit %s" % done.returncode), True) if door else call(root, data, member, name, args)
    return text, done.returncode == 1


def answer(message, root, data, member):
    """The JSON-RPC answer to one message, or None for a notification."""
    method, ident = message.get("method"), message.get("id")
    if ident is None:
        return None
    params = message.get("params") or {}
    if method == "initialize":
        result = {"protocolVersion": params.get("protocolVersion") or "2024-11-05", "capabilities": {"tools": {"listChanged": False}},
                  "serverInfo": {"name": "collective", "version": "1.0.0"},
                  "instructions": "The Collective's own data and the door to its ships. Every answer is printed by a script of game/fleet/ in the repository, from the "
                                  "fleet's own readings: a figure names what it rests on. You are %s." % (member or "no member: the door is closed, reading is open")}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [schema(name) for name in TOOLS]}
    elif method == "tools/call":
        text, failed = fresh(root, data, member, params.get("name"), params.get("arguments") or {})
        result = {"content": [{"type": "text", "text": text}], "isError": bool(failed)}
    elif method in ("resources/list", "prompts/list", "resources/templates/list"):
        result = {method.split("/")[0] if "templates" not in method else "resourceTemplates": []}
    else:
        return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": "method not found: %s" % method}}
    return {"jsonrpc": "2.0", "id": ident, "result": result}


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    root = value("--root", str(Path(__file__).resolve().parents[2]))
    data = value("--data", "")
    kind, name = division.member()
    member = name if kind == "member" else ""
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    if "--list" in args:
        for tool in TOOLS:
            print("%-11s %s%s" % (tool, "[door] " if TOOLS[tool].get("door") else "", TOOLS[tool]["text"][:150]))
        return 0
    if "--call" in args:
        rest = args[args.index("--call") + 1:]
        if not rest:
            sys.exit(__doc__)
        try:
            given = json.loads(rest[1]) if len(rest) > 1 and not rest[1].startswith("--") else {}
        except ValueError as error:
            sys.exit("the arguments are not JSON: %s" % error)
        text, failed = call(root, data, member, rest[0], given)
        print(text)
        return 1 if failed else 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except ValueError:
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "not JSON"}}
        else:
            try:
                out = answer(message, root, data, member) if isinstance(message, dict) else None
            except Exception as error:                             # a fault in one call must not end the server
                out = {"jsonrpc": "2.0", "id": message.get("id"), "error": {"code": -32603, "message": "%s: %s" % (type(error).__name__, error)}}
        if out is not None:
            sys.stdout.write(json.dumps(out) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (BrokenPipeError, KeyboardInterrupt):
        sys.exit(0)
