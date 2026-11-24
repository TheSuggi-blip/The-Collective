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
        needs       the needs register (needs.py): every division's needs read, a member's own division's written
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
    if value is None or value is False or value == "":       # by identity: 0 == False, and a 0 is a value (requests ENT-212)
        return []
    return [option or "--" + name.replace("_", "-"), str(value)]


def need(args, *names):
    missing = [n for n in names if args.get(n) in (None, "", [])]
    if missing:
        raise ValueError("this needs: " + ", ".join(missing))


STATS_VIEWS = ('kpi', 'contribution', 'classes', 'time', 'supply', 'xp', 'upgrades', 'alerts')       # hive.py stats <view>: definitions in game/metrics.md


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
    if view == "rival":
        return [("game/fleet/hive.py", ["rival"])]
    if view == "contracts":
        return [("game/fleet/hive.py", ["contracts"])]
    if view == "progression":
        return [("game/fleet/hive.py", ["progression"])]
    if view == "scorecard":
        return [("game/fleet/scorecard.py", ["--who", a.get("member") or "all"])]
    if view == "rivals":
        return [("game/fleet/rivals.py", [a.get("member") or "all"])]
    if view == "shipping":
        return [("game/fleet/shipping.py", ["list"])]
    if view == "upgrade_plan":
        return [("game/fleet/upgrades.py", [a.get("member") or "all"])]
    if view == "forecast":
        return [("game/fleet/hive.py", ["forecast"] + ([a["member"]] if a.get("member") else []) + flag(a, "hours"))]
    if view == "watchdog":
        return [("game/fleet/watchdog.py", ["show"] + flag(a, "hours"))]
    if view in STATS_VIEWS:                         # the fleet's statistics, computed by the store (stats.py)
        return [("game/fleet/hive.py", ["stats", view] + flag(a, "member") + flag(a, "hours"))]
    raise ValueError("view is one of: money, history, levels, capacity, board, standing, tasks, refill, forecast, watchdog, " + ", ".join(STATS_VIEWS))


def plan_file(a):
    action = a.get("action") or "show"
    where = flag(a, "division")
    if action in ("show", "check", "apply"):
        return [("game/fleet/plan.py", [action] + ([a["division"]] if a.get("division") else []) + (["--brief"] if a.get("brief") and action == "show" else []))]
    if action == "set":
        need(a, "ships", "routes")
        return [("game/fleet/plan.py", ["set", a["ships"], a["routes"]] + where)]
    if action in ("first", "then"):
        need(a, "routes")
        return [("game/fleet/plan.py", [action, a["routes"]] + where)]
    if action == "templates":
        return [("game/fleet/plan.py", ["templates"] + ([a["division"]] if a.get("division") else []))]
    if action == "template":
        need(a, "name", "routes")
        return [("game/fleet/plan.py", ["template", a["name"], a["routes"]] + flag(a, "title") + flag(a, "trains") + flag(a, "note") + where)]
    if action == "use":
        need(a, "ships", "name")
        return [("game/fleet/plan.py", ["use", a["ships"], a["name"]] + where)]
    if action in ("planned", "note"):                 # requests ENT-263: Planned and Notes by script, never by hand
        text = a.get("what") if action == "planned" else a.get("note")
        if not text and not a.get("clear"):
            raise ValueError("action=%s needs %s (or clear=true)" % (action, "what" if action == "planned" else "note"))
        return [("game/fleet/plan.py", [action] + ([str(text)] if text else []) + (["--clear"] if a.get("clear") else [])
                 + (flag(a, "when") if action == "planned" else []) + where)]
    raise ValueError("action is one of: show, check, apply, set, first, then, templates, template, use, planned, note")


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
    if ask == "releases":
        return [("game/fleet/craftbook.py", ["releases"] + flag(a, "top"))]
    raise ValueError("ask is one of: item, needs, build, can, recipes, releases")


def stock_plan(a):
    view = a.get("view") or "members"
    if view in ("inventory", "stations"):
        return [("game/fleet/craftbook.py", ["inventory"] + (["stations"] if view == "stations" else []) + flag(a, "item") + flag(a, "top"))]
    if view == "surplus":
        return [("game/fleet/surplus.py", ["show"] + flag(a, "item") + flag(a, "kind") + flag(a, "top"))]
    if view == "reserve":
        return [("game/fleet/surplus.py", ["reserve"])]
    return [("game/fleet/ledger.py", ["show"] + ([a["member"]] if a.get("member") else []) + flag(a, "item"))]


def sql_plan(a):
    if a.get("query"):
        return [("game/fleet/hive.py", ["sql", str(a["query"])] + flag(a, "limit"))]
    return [("game/fleet/hive.py", ["schema"] + ([a["table"]] if a.get("table") not in (None, "", "all") else []))]


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
    if view == "turn_pack":
        return [("scripts/comms.py", ["turn-pack"] + flag(a, "member"))]
    if view == "safe_comms":
        return [("game/fleet/comms_guard.py", flag(a, "last"))]
    raise ValueError("view is one of: orders, requests, digest, contacts, learnings, turn_pack, safe_comms")


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


def stop_plan(a):
    if a.get("list"):
        argv = ["--list"]
    elif a.get("route"):
        argv = ["--route", str(a["route"])]
    elif a.get("pilot"):
        argv = [str(a["pilot"])]
    else:
        argv = ["--list"]
    return [("game/fleet/stop_pilot.py", argv + (["--dry-run"] if a.get("dry_run") else []))]


def errand_plan(a):
    act = str(a.get("action") or "show")
    if act == "show":
        return [("game/fleet/wallet.py", ["errand", "--show"])]
    if act == "cancel":
        need(a, "id")
        return [("game/fleet/wallet.py", ["errand", "cancel", str(a["id"])])]
    need(a, "errand_action", "params_json", "why")
    argv = ["errand", "add", str(a["errand_action"]), "--params", str(a["params_json"]), "--why", str(a["why"])]
    if a.get("station"):
        argv += ["--station", str(a["station"])]
    return [("game/fleet/wallet.py", argv)]


def fund_plan(a):
    if a.get("show") or (not a.get("pilot") and a.get("credits") is None and not a.get("why")):
        return [("game/fleet/wallet.py", ["fund", "--show"])]
    need(a, "pilot", "credits", "why")
    argv = ["fund", str(a["pilot"]), str(a["credits"]), "--why", str(a["why"])]
    if a.get("hours") is not None:
        argv += ["--hours", str(a["hours"])]
    return [("game/fleet/wallet.py", argv)]


TOOLS = {
    "fleet": {
        "text": "The fleet in figures. view=money: credits, Net Purse/h (steady + paid once), matched Recurring Cash/h, and transfer-priced IAS2 Accrual Value-Add/h over 1, 6 and 24 hours, per division. "
                "view=history: credits hour by hour per division. view=levels: pilots' levels, XP an hour, hours to the next hull tier. view=capacity: what mining, hunting "
                "and the once-missions carry (bids, what is left in the fields, herds, tools) and how many ships that employs. view=board: a member's ships one line each, "
                "with their orders and last runs. view=standing: the standing fleet of a member: its plan route by route with the credits per ship-hour of each, and "
                "every ship with what it flies, what it earned per hour and what closes the best route to it. view=tasks: credits per ship-hour by kind of work and by "
                "division, idle ships counted. view=refill: what comes back per hour between our readings: bids, fields, herds. view=forecast: the hours ahead per "
                "division: every route with the ships on it now, what a ship-hour on it measured, and what that makes per hour and per turn. "
                "The statistics the store computes by itself (definitions: game/metrics.md; every figure with its window and n, `not measured` "
                "where no record holds it): view=kpi: the fleet as one purse over 1, 6, 24 and 72 hours: throughput, operating expense, steady "
                "net, paid once, net of everything, net per ship-hour, the trend, the reserve and the surplus at the best bid. view=contribution: "
                "per division its Net Purse/h (6h/24h), matched Recurring Cash/h, IAS2 Accrual Value-Add/h, raw steady net, enabled income, and service. view=classes: per role the "
                "places of its own class work open now against its ships, and the spill. view=time: where the ship-hours went: own work, "
                "another class's, once, shared, docked or in space without work, offline. view=supply: per reserve good held, needed, min "
                "and max, change an hour, days of supply, the routes and ships that feed it, and gather against buy. view=xp: XP per "
                "ship-hour per role, skill and route, hours to the next tier. view=upgrades: per ship its tier, Piloting, the next tier's "
                "hulls, empty slots. view=alerts: the hours outside their control band. view=rival: live benchmark vs #1 [HEXC], unclaimed resource-monopoly outpost sites, zero-fuel docked crafting spreads & hull targets. view=contracts: bottleneck procurement candidates for Station Bursars, rival board supply contracts & contracts.log. view=progression: live 3-horizon strategic progression rungs, milestones & ledgers. view=scorecard: MAUTxWSJF weighted triage queue (P0>P1>P2>P3) & live WAR/CASHFLOW/GROWTH posture. view=rivals: rival faction sedcards & live Outsupply/Outsource/Undercut board. view=shipping: live spacemolt_shipping freight contracts. view=upgrade_plan: empire-specialized T1/T2 parallel batch upgrade sheet.",
        "args": {"view": arg(S, "money (default), history, levels, capacity, board, standing, tasks, refill, forecast, kpi, contribution, "
                                "classes, time, supply, xp, upgrades or alerts",
                             ("money", "history", "levels", "capacity", "board", "standing", "tasks", "refill", "rival", "rivals", "contracts", "progression", "scorecard", "shipping", "upgrade_plan", "forecast") + STATS_VIEWS),
                 "member": arg(S, "for levels, board, standing, forecast, contribution, classes, time, xp and upgrades: a member's name, or all", MEMBERS),
                 "hours": arg(I, "for history, board, standing, tasks and forecast: the window in hours")},
        "plan": fleet_plan},
    "ship": {
        "text": "One ship of the fleet from its live file: place, docked or not, hull, fuel, hold, modules, wallet, the order it flies, skills, missions held.",
        "args": {"pilot": arg(S, "the pilot's name, e.g. miner-7")}, "required": ["pilot"],
        "plan": lambda a: [("game/fleet/hive.py", ["ship", a["pilot"]])]},
    "routes": {
        "text": "Every route with what it earns: its group (once per pilot, paying, test, fitting, reading and waiting, at a loss, off), zone, ships on it against its "
                "limit, the credits per ship-hour its runs of the last 12 hours measured (older, a route has no figure and is a test again: nothing is bad for good), and "
                "its runs, steady credits and credits per ship-hour in the last hours. Filter by group, kind or zone. The same over 4, 12 and 24 hours with the hours "
                "since a route last flew: the tool sql, view route_earnings.",
        "args": {"group": arg(S, "once, paying, test, fit, service, losing or off", ("once", "paying", "test", "fit", "service", "losing", "off")),
                 "kind": arg(S, "circuit, hunt, mine, census or guard", ("circuit", "hunt", "mine", "census", "guard")), "zone": arg(S, "home or beyond (the border)", ("home", "beyond")),
                 "hours": arg(I, "the window of the runs, default 4")},
        "plan": lambda a: [("game/fleet/hive.py", ["routes"] + flag(a, "group") + flag(a, "kind") + flag(a, "zone") + flag(a, "hours"))]},
    "upgrades": {
        "text": "Empire-specialized hull & module upgrade planner and autonomous batch hull-upgrade queue (F12/F17/F37). action=status: division cohorts, P0/P10 hull tables, and active queue. action=queue: list queued upgrades. action=add: queue batch of pilots for automatic fund->commission->switch (executed every 5m in wallet sweep). action=cancel: cancel pending entries by id, batch_id, or pilot.",
        "args": {
            "action": arg(S, "status (default), queue, add, or cancel", ("status", "queue", "add", "cancel")),
            "who": arg(S, "member or division filter for status/queue", MEMBERS),
            "hull": arg(S, "for add: catalog hull id (e.g. recursion, prayer, runner, resonance_miner)"),
            "station": arg(S, "for add: shipyard station as system:poi:base"),
            "max_price": arg(I, "for add: maximum acceptable quote in credits"),
            "count": arg(I, "for add: number of eligible pilots to queue (default 5)"),
            "role": arg(S, "for add: optional role filter (miner, trader, hauler, drone, sentinel, scout)"),
            "empire": arg(S, "for add: optional empire filter"),
            "min_piloting": arg(I, "for add: minimum piloting level (enforced >= catalog requirement)"),
            "pilots": arg(S, "for add: optional comma-separated explicit pilot names"),
            "provide_materials": arg(B, "for add: pass provide_materials=true to commission_ship"),
            "target": arg(S, "for cancel: entry id, batch_id, or pilot name"),
        },
        "plan": lambda a: (
            [("game/fleet/upgrades.py", ["queue", "show"] + (["--who", a["who"]] if a.get("who") else []))]
            if a.get("action") == "queue" else
            [("game/fleet/upgrades.py", ["queue", "cancel", str(a.get("target") or "")])]
            if a.get("action") == "cancel" else
            [("game/fleet/upgrades.py", ["queue", "add", "--hull", str(a.get("hull") or ""), "--station", str(a.get("station") or ""),
              "--max-price", str(a.get("max_price") or 0)] + flag(a, "count") + flag(a, "role") + flag(a, "empire")
              + (["--min-piloting", str(a["min_piloting"])] if a.get("min_piloting") is not None else [])
              + flag(a, "pilots") + (["--provide-materials"] if a.get("provide_materials") else []))]
            if a.get("action") == "add" else
            [("game/fleet/upgrades.py", ([a["who"]] if a.get("who") else []))]
        ),
    },
    "route": {
        "text": "One route in full: its file's facts, who flies it now, last twelve runs and 24h hourly rates. Set why=true to diagnose why pilots are open or closed to this route (`hive.py why <id>`).",
        "args": {"id": arg(S, "the route id, e.g. mine-ruchbah-ice-belt"),
                 "why": arg(B, "when true: run hive.py why <id> to group open/closed reasons across pilots"),
                 "member": arg(S, "optional member or role filter when why=true", MEMBERS)},
        "required": ["id"],
        "plan": lambda a: [("game/fleet/hive.py", ["why", a["id"]] + ([a["member"]] if a.get("member") else []))] if a.get("why") else [("game/fleet/hive.py", ["route", a["id"]])]},
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
    "plan": {
        "text": "Your division's plan file: every ship of yours with its own routes in their order. A free ship takes the first route open to it of: the list First (for every "
                "ship), its own routes, the list Then (for every ship, ending with park); the dispatcher sends it within the minute. action=show: the file, what the check says and "
                "whether it is applied (brief=true: a few lines). action=set: give ships their own routes (ships: names with commas, a range like miner-1..10, a role or all; "
                "routes: route ids with commas in their order, or none). action=first or then: set that list whole. action=apply: after you changed the file by hand. Every change "
                "is checked first: a plan that fails changes nothing. action=check: PASS or HALT. You change your own division's plan only. A template is a named list of routes "
                "your division keeps in the repository, which a ship's own routes name as @<name> so that one word switches it to that work and a change of the template moves "
                "every ship that names it (action=templates lists them, action=template makes, replaces or with routes=none removes one, action=use puts ships on templates). "
                "action=planned: one line into Planned (what, when; clear=true empties it first); action=note: one line into Notes (note; clear=true empties it first).",
        "args": {"action": arg(S, "show (default), check, apply, set, first, then, templates, template, use, planned or note",
                               ("show", "check", "apply", "set", "first", "then", "templates", "template", "use", "planned", "note")),
                 "division": arg(S, "command, mining, trade, logistics, military or intel; default: your own (for show, check and templates also all)"),
                 "ships": arg(S, "for set and use: ship names with commas, a range (miner-1..10), a role, or all"),
                 "routes": arg(S, "for set, first, then and template: route ids with commas, in their order (for set also @<template>); none for no route, or to remove a template"),
                 "name": arg(S, "for template: the template's name (2 to 40 lower-case letters, digits and dashes); for use: one name or several with commas"),
                 "title": arg(S, "for template: one line on what it is for; left out: kept as it was"),
                 "trains": arg(S, "for template: the skills it trains, with commas; left out: kept as it was"),
                 "note": arg(S, "for template: a note for the reader; left out: kept as it was; for note: the line written into Notes"),
                 "what": arg(S, "for planned: what the division means to do next, one line that names no ship"),
                 "when": arg(S, "for planned: when, e.g. next turn; left out: --"),
                 "clear": arg(B, "for planned and note: empty the part first"),
                 "brief": arg(B, "for show: the plan in a few lines instead of the whole file")},
        "plan": plan_file},
    "candidates": {
        "text": "Ways to earn that the route maker computed every 3 minutes from our own readings (fields, order books, mission boards incl. Trade Runs, herds, recipes), best first, with the estimate "
                "per ship-hour, what it rests on, its warnings and what it still needs. With id: prints the ready route file; with id and write=true: writes game/routes/<id>.json, checks, indexes and commits it in one step.",
        "args": {"member": arg(S, "whose ships: a member's name or all", MEMBERS), "kind": arg(S, "mine, trade, craft, hunt or mission", ("mine", "trade", "craft", "hunt", "mission")),
                 "top": arg(I, "how many, default 20"), "id": arg(S, "one candidate's id: prints or writes its route file"),
                 "write": arg(B, "with id: write game/routes/<id>.json, check, index and commit it immediately")},
        "plan": lambda a: [("game/fleet/routemaker.py", (["write", a["id"], "--commit"] if a.get("write") else ["route", a["id"]]))] if a.get("id") else
                          [("game/fleet/routemaker.py", ["show"] + ([a["member"]] if a.get("member") else []) + flag(a, "kind") + flag(a, "top"))]},
    "market": {
        "text": "The last moves of one item's best bid and best ask at the stations whose order books our ships read: what it sells for, what it costs, how deep, when read.",
        "args": {"item": arg(S, "the item id, e.g. water_ice"), "base": arg(S, "one station's base id"), "last": arg(I, "how many moves, default 20")}, "required": ["item"],
        "plan": lambda a: [("game/fleet/ledger.py", ["prices", a["item"]] + flag(a, "base") + flag(a, "last"))]},
    "stock": {
        "text": "What we own in goods. view=members (default): what a member's ships hold in station storage and in their holds. view=inventory: the whole fleet added up, "
                "by kind of item (raw, refined, parts, modules ...), with units stored and carried and the catalog's base value. view=stations: the same per station. "
                "view=surplus: what we hold beyond the reserve and may sell, best worth at a standing bid first, where it lies and the bid at that very station (rule "
                "F24). view=reserve: what our bases and upgrades take (the open needs of game/needs.tsv, tool needs) against what we hold, what is short, and what is held back for another "
                "recipe. Optionally one item.",
        "args": {"view": arg(S, "members (default), inventory, stations, surplus or reserve", ("members", "inventory", "stations", "surplus", "reserve")),
                 "member": arg(S, "for members: a member's name or all", MEMBERS), "item": arg(S, "one item id (not for reserve)"),
                 "kind": arg(S, "for surplus: one kind of item (raw, refined, component, module, consumable, ammo, drone, other, contraband)"),
                 "top": arg(I, "for inventory and stations: rows per group, default 40; for surplus: items, default 15")},
        "plan": stock_plan},
    "catalog": {
        "text": "The game's catalog asked as a question. ask=item: find an item by text; for one item how it is made, what uses it, what is built with it. ask=needs: "
                "everything a number of units takes down to what is mined or bought, beside what we store. ask=build: what a facility or a hull costs and takes. "
                "ask=can: what a member's stored goods can be made into by hand today and what that sells for. ask=recipes: the recipes of a category, or that make or "
                "use an item. ask=releases: newest SpaceMolt patch notes and active catalog version. The same tables as files: game/catalog/master-index.md.",
        "args": {"ask": arg(S, "item (default), needs, build, can, recipes or releases", ("item", "needs", "build", "can", "recipes", "releases")),
                 "name": arg(S, "for item: text or an item id; for needs: an item id; for build: a facility id or a hull id"), "quantity": arg(I, "for needs: units, default 1"),
                 "member": arg(S, "for can: a member's name or all", MEMBERS), "top": arg(I, "for can: how many rows"), "category": arg(S, "for recipes: a category name as the catalog writes it (renamed in the game's 0.729.0: Smelting, Machining ...; ask=recipes alone lists them)"),
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
                "or changed. view=turn_pack: orders in force, open requests, active claims and recent errors in one call. view=safe_comms: player hails through the CaMeL + dynamic spotlighting injection firewall.",
        "args": {"view": arg(S, "orders (default), requests, digest, contacts, learnings, turn_pack or safe_comms", ("orders", "requests", "digest", "contacts", "learnings", "turn_pack", "safe_comms")),
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
    "stop": {
        "text": "Stop one or more in-flight ships of your division cleanly (or every active run of your division on a named route) without touching global fleet/STOP. "
                "Use list=true to view running ships in your division first.",
        "args": {"pilot": arg(S, "pilot name or comma-separated pilot names to stop"),
                 "route": arg(S, "stop every active run of your division currently flying this route id"),
                 "list": arg(B, "true: list active runs in your division without stopping any"),
                 "dry_run": arg(B, "true: preview which pilots would be stopped without writing stop files")},
        "plan": stop_plan,
        "door": True},
    "errand": {
        "text": "Queue or inspect docked-leader faction errands (Unity-only, Q75 (12)): promote officer, post_mission on Notice Board, cancel_mission, write_room, role or station policy. The dispatcher holds the leader at its next dock and the 5-minute wallet sweep executes the errand automatically. War, ally, and leadership transfer are permanently blocked.",
        "door": True,
        "args": {
            "action": arg(S, "show (default), add, or cancel", ["show", "add", "cancel"]),
            "errand_action": arg(S, "for add: allowlisted leader action", ["promote", "post_mission", "cancel_mission", "write_room", "create_role", "edit_role", "delete_role", "set_station_policy"]),
            "params_json": arg(S, "for add: JSON object of parameters for the action"),
            "why": arg(S, "for add: short reason for the errand"),
            "station": arg(S, "for add: optional base_id where leader must be docked (e.g. node_beta_industrial_station)"),
            "id": arg(S, "for cancel: errand id to cancel"),
        },
        "plan": errand_plan,
    },
    "fund": {
        "text": "Draw credits from the shared faction treasury for one or more pilots of your division (rule F12: up to 400,000 cr/pilot and 750,000 cr/division per 24h, "
                "keeping 500,000 cr treasury floor; uncapped for Unity), served every 5 minutes. Use show=true to view open funds and 24h division budgets.",
        "args": {"pilot": arg(S, "pilot name or comma-separated pilot names in your division"),
                 "credits": arg(I, "credits to fund each pilot"),
                 "why": arg(S, "short reason (e.g. hull upgrade, fittings, working capital)"),
                 "hours": arg(I, "hours sweep leaves funded credits with the pilot (default 6)"),
                 "show": arg(B, "true: show open/recent funds and 24h division autonomous budgets")},
        "plan": fund_plan,
        "door": True},
    "supply": {
        "text": "The supply chains: the goods the fleet must never run out of (iron, fuel for our outpost's bunker, later food and power), each at its "
                "place (game/supply/chains.tsv, kept by the Fleet Admiral with Logistics), against what stands there now. view=show: every chain with "
                "its status (short: below keep, low: below twice keep, ok, broken: a row of the file that does not count), stock, keep, need per hour, "
                "the change over 24 hours, its source routes with our ships on them now and how many stand in a plan. view=check: the gate, one "
                "line per short chain, broken row or unknown id, HALT or PASS. view=duty: for each short chain the source routes its keeper's plan "
                "does not hold yet and the change that would put them in; read only here. The same rows in SQL: the tool sql, view supply_status.",
        "args": {"view": arg(S, "show (default), check or duty", ("show", "check", "duty"))},
        "plan": lambda a: [("game/fleet/supply.py", [a.get("view") or "show"])] if (a.get("view") or "show") in ("show", "check", "duty")
                          else need(a, "view: show, check or duty")},
    "sql": {
        "text": "Ask the fleet's one database in SQL, read-only: one SELECT over what the fleet knows now and what it measured (ships and where they are, holdings, order "
                "books, the game's catalog with recipes and facilities, the map, stations, factions, our empire, routes, plans, every run, prices and field readings "
                "by the hour). What a route earns now: the view route_earnings (credits per ship-hour over the last 4, 12 and 24 hours, the runs behind each, the hours "
                "since it last flew; an empty figure means it did not fly, not that it does not pay). Without a query: the tables and views with what each holds; "
                "with table: its columns and example questions.",
        "args": {"query": arg(S, "one SELECT statement, e.g. SELECT route, runs_4h, cph_4h, cph_24h, hours_since FROM route_earnings ORDER BY cph_4h DESC"),
                 "table": arg(S, "instead of a query: a table's or view's name for its columns and examples; all (default) lists every table and view"),
                 "limit": arg(I, "for a query: rows at most")},
        "plan": sql_plan},
    "docs": {
        "text": "The fleet's written knowledge by section, from the database (the store mirrors the files every minute and keeps every version): "
                "the rulebook rule by rule (F1 to F35), the orders in force block by block (S, G, D and P lines, each member's block), strategy, empire, "
                "each division's guidebook (its class card: ships, and skills in levelling order; levelling guide; ships and fits) and templates, the "
                "game's rules row by row, the metrics; and what the members write as they work: each division's plan (data/plans), every report, "
                "every entry of the logs requests, queue, admirals, errors and reports, each member's own files (soul, mission, learnings, knowledge). "
                "view=list: the files, or one file's sections by title (doc: a file, a kind or an owner; grep: the sections "
                "that hold a word, whole). view=section: one section whole. view=changes: the sections changed since your last turn (or since). "
                "view=history: every version of one section with when it was first seen, each against the one before. view=division: what each "
                "Admiral is doing, one short block a division: its mission, its orders block, its plan, its guidebook's sections, its last report, "
                "the requests open to and from it, its claims in force.",
        "args": {"view": arg(S, "list (default), section, changes, history or division", ("list", "section", "changes", "history", "division")),
                 "doc": arg(S, "for list, section and history: a file (governance/rulebook.md, guidebook/mining.md, orders.log), a kind (rulebook, "
                              "orders, strategy, empire, guidebook, template, rules, metrics, plan, report, log, member) or an owner (Fleet, Unity, Mining, Trade, "
                              "Logistics, Military, Intel, Command)"),
                 "section": arg(S, "for section and history: the section's id, e.g. F8, D3, zero, class-card/skills"),
                 "grep": arg(S, "for list: only the sections that hold this word, printed whole"),
                 "since": arg(S, "for changes: a UTC time (2026-11-17T12:00Z) or hours back (6h); default: your last turn"),
                 "member": arg(S, "for changes: whose last turn; default: yours", division.MEMBERS),
                 "division": arg(S, "for division: a member's or a division's name, or all (default)")},
        "plan": lambda a: [("game/fleet/hive.py", ["changes"] + flag(a, "since") + flag(a, "member"))] if a.get("view") == "changes" else
                          [("game/fleet/hive.py", ["division", str(a.get("division") or "all")])] if a.get("view") == "division" else
                          (need(a, "section") if a.get("view") in ("section", "history") else None) or
                          [("game/fleet/hive.py", ["docs"] + ([str(a["doc"])] if a.get("doc") else []) + flag(a, "section") + flag(a, "grep")
                            + (["--history"] if a.get("view") == "history" else []))]},
    "hive": {
        "text": "Any verb of game/fleet/hive.py by name, with its arguments as a list: the way to a figure added after this tool list was loaded. verb=help prints "
                "what exists now.",
        "args": {"verb": arg(S, "the verb, or help"), "args": arg(A, "its arguments", items=S)}, "required": ["verb"],
        "plan": lambda a: [("game/fleet/hive.py", (["--help"] if a["verb"] == "help" else [a["verb"]] + [str(x) for x in a.get("args") or []]))]},
}

__import__("guidebook").mcp_view(TOOLS, arg)      # the tool docs gains view=guide: a guidebook by chapter and entry (guidebook.py)
__import__("needs").mcp_tool(TOOLS, arg)          # the tool needs: the needs register, every division's read, its own written (needs.py)

# The tool docs, view=handbook: the store's handbook (game/handbook.md, game/handbook/), written from the code by scripts/handbook.py
# and read in parts by hive.py handbook (docs_handbook.py). Kept apart from the row above so that it adds to the row, not edits it.
TOOLS["docs"]["text"] += (" view=handbook: the store's handbook, written from the code: how the data flows, where to ask what, and every "
                          "table and view with its columns, how long its rows are kept, how often it is refreshed and its example queries "
                          "(topic: a table's name, a subject or a word; without it the contents).")
TOOLS["docs"]["args"]["view"]["enum"].append("handbook")
TOOLS["docs"]["args"]["view"]["description"] += ", or handbook"
TOOLS["docs"]["args"]["topic"] = arg(S, "for handbook: a table's or view's name (route_earnings), a subject (money) or a word; left out: the contents")
TOOLS["docs"]["plan"] = (lambda plan: lambda a: [("game/fleet/hive.py", ["handbook"] + ([str(a["topic"])] if a.get("topic") else []))]
                         if a.get("view") == "handbook" else plan(a))(TOOLS["docs"]["plan"])

WRITES = ("fill", "plan", "command", "goal", "hold", "stop", "fund", "errand")      # every other tool only reads
WRITES += ("needs",)                              # needs.py writes the member's own division's needs (action add, set, done, drop)


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
    """(text, True when the tool could not answer) of one tool call. A script that says no (HALT, REFUSED: it ends
    with exit 1) HAS answered: its words are the answer, and the member reads them. A fault is a tool that did not
    run: an unknown tool, a missing argument, a crash, a timeout. Hermes pauses a server after three faults in a row
    and stops a run after eight: a refused plan change counted as a fault ended a turn (2026-11-16)."""
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
        fault = code not in (0, 1) or (code == 1 and "Traceback (most recent call last)" in text)
    else:                                                          # one command to many ships: six at a time, one block each
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda step: run_one(root, data, member, *step), plan))
        failed, fault = all(code != 0 for code, _text in results), False
        text = "\n".join("%s: %s%s" % (step[1][1], "" if code == 0 else "FAILED: ", " ".join(out.split())[:700]) for step, (code, out) in zip(plan, results))
        text = "%d of %d went through\n%s" % (sum(1 for code, _t in results if code == 0), len(results), text)
    text = text.strip() or "(the script printed nothing; exit %s)" % ("0" if not failed else "not 0")
    if failed and not fault and not any(word in text for word in ("HALT", "REFUSED", "FAILED", "went through")):
        text = "NOT DONE: the script ended with exit 1 and these words:\n" + text      # an answer that says no must say so in its first line
    if tool.get("door"):
        audit(data, member, name, args, failed, text)
    if len(text) > LIMIT:
        text = text[:LIMIT] + "\n... CUT at %d of %d characters: narrow the question (a filter, one member, fewer rows)" % (LIMIT, len(text))
    return text, fault


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
