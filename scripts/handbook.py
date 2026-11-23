#!/usr/bin/env python3
"""handbook.py -- writes the store's handbook, game/handbook.md and one file per subject in game/handbook/: how the fleet's data flows, where to ask what, and every table and view of the SQL store with its description, columns, how long its rows are kept, how often it is refreshed and its tested example queries; the kinds of the written knowledge and the statistics; all from the code itself.

WHAT: the members ask the store through hive.py's verbs and the MCP tool `collective`; what each table holds, where
      it comes from and how to ask it stood scattered over docstrings, skills and BOX.md. This script writes it:
        game/handbook.md     (frontmatter like game/metrics.md) the head, the contents, and:
          How the data flows   FLOW below: the one part kept by hand (at most FLOW_CAP characters), what no
                               script can say: the game, the engine's gate, the services, the data folder, the
                               store, the readers; what is private and what is public
          Where to ask what    every view, action or ask of the MCP tools (collective_mcp.TOOLS: its text, cut to
                               ASK_CHARS, and the script line its plan builds) and every hive.py verb no tool
                               reaches (hive.py's usage, read as text), one line each, filed by subject
        game/handbook/<subject>.md   one file per subject (SUBJECTS: ships and pilots, routes and runs, money,
                               markets, map and intel, our faction, stock and reserve, the catalog, supply,
                               statistics, written knowledge, the store itself), a section per table or view:
                               its kind (snapshot, history, statistics, view, bookkeeping), store.DESCRIPTIONS,
                               its columns and key from PRAGMA table_info of a fresh empty schema made in memory by
                               the store's own setup (store.SCHEMA, store.setup_snapshot), never the live
                               database; how long its rows are kept (store.KEEP_DAYS, KEEP_TABLES, stats.KEEP,
                               retention.py's RETAIN and BOUNDED, a DELETE in the code); how often it is refreshed (store.RECORDS, LOADERS, the
                               functions that write it, stats.compute's parts); store.EXAMPLES, which
                               test_fleet_store_state.py runs. statistics.md adds The figures (stats.VIEWS_SHOWN,
                               each with its section of game/metrics.md), written-knowledge.md The kinds (docs.KINDS
                               with their files, owner and readers)
      docs.py mirrors every file into the store as kind `handbook` (owner Fleet, one section per heading); hive.py
      handbook [<topic>] and the MCP tool docs (view=handbook) read it in parts (docs_handbook.py).
RULES:
  - Written from the code, never by hand: the same code gives the same bytes on every machine. Nothing is read from
    the data folder or a database, and no time stands in it; the id of game/handbook.md is kept once given.
  - A table or view without a description (store.DESCRIPTIONS) fails the generator: nothing is written and the table
    is named. A table no subject names stands in game/handbook/other.md, a call no subject names under Other: each
    is printed as a WARNING (it does not fail) until SUBJECTS, ASKS or VERBS name it.
  - Every file at most CAP characters: a subject's tables carry all their examples while its file stays under the
    cap, else the first two, else the first; above the cap with one, or a game/handbook.md above it, fails.
  - game/handbook/ is this script's alone: a file there it no longer writes is removed, and the gate fails on it.
  - --check exits 1 when a file differs from what the generator writes now, is missing or is left over.
  - --commit writes, then commits game/handbook.md and game/handbook/ by path as Unity (three tries; a commit that
    fails takes the files back). It writes nothing while game/fleet/, game/metrics.md or this script hold a change
    that is not committed: that is a member's work in progress, and the handbook must describe committed code.
WHY:  Suggi, 2026-11-18: "We need a handbook or guide for how the database/sql works. This handbook must also always
      be auto updated to be kept up to date." A handbook written from the code cannot say more or less than the code.

USAGE:
  handbook.py              write game/handbook.md and game/handbook/ where their text changed
  handbook.py --check      the gate: exit 1 when a file is stale, missing or left over, or the generator fails
  handbook.py --commit     write, and commit them by path as Unity (the hourly job intel-track)
  --root <dir>             the repository (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import argparse
import ast
import importlib
import inspect
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = "game/handbook.md"
FOLDER = "game/handbook"
SOURCES = ("game/fleet", "game/metrics.md", "scripts/handbook.py")     # what the handbook is written from (--commit waits on them)
CAP = 40000                    # characters of one file, at most
FLOW_CAP = 2500                # characters of the part kept by hand, at most
ASK_CHARS = 105                # characters of one line's text in Where to ask what
EXAMPLES_MAX = 3               # examples per table while its file stays under CAP
MARK = "Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand."
ID = re.compile(r"^id: (\S+)$", re.M)

FLOW = """\
The game -> the fleet engine and its gate -> the services -> the data folder (files) -> the store (live.db) ->
its read copy (read.db) -> hive.py and the MCP tool `collective` -> the members.

- The game: only the fleet engine holds the game key. Every program of ours reaches the game through the
  engine's gate; no member and no service holds the key.
- The services run on the unit's shelf, one program each, started again when they end:
  - `fleet`: our ships' live state as files (station/fleet.py): data/fleet/. Sends no command.
  - `sight`: who is where our ships are, a first read of a system nobody read: intel/met.json, scouting/.
  - `ledger`: every pilot's station storage (stock/storage.json) and every move of a best bid or ask
    (market/history.jsonl).
  - `dispatch`: gives each free pilot the next route of its plan; the runners it starts fly the route and
    append routes/runs.jsonl.
  - `routemaker`: costs every way to earn our readings show: routes/opportunities.json.
  - `runhost`: flies the dispatcher's runs, each as a thread.
  - `station`: Suggi's command station (map, fleet, intel, chat): data/station/.
  - `inbox`: what other pilots write to our ships (comms/messages.jsonl); a message to us is filed in
    communications/contacts/.
  - `keeper`: cuts the append-only records to their newest lines (the old lines to data/archive/).
  - `store`: the one writer of the database, below.
- The data folder /srv/collective/data/ is PRIVATE, never committed: where our ships are and what they carry
  stays there. The repository (the clone /srv/collective/the-collective, mirrored to GitHub) is PUBLIC: rules,
  orders, routes, the roles' plans, guidebooks, reports, logs, the catalog as files, this handbook.
- The store (game/fleet/store.py, service `store`) reads every minute the new lines of the records and every
  file that changed, of the data folder and the repository, into data/store/live.db, which no other program
  opens; it computes the statistics when due (stats.py) and publishes data/store/read.db, the copy every reader
  opens read-only.
- The readers: game/fleet/hive.py (one verb per question; `hive.py sql` asks any SELECT) and the MCP tool
  `collective` (game/fleet/collective_mcp.py), which runs those scripts for each member. Nobody writes a table
  by hand: members edit files, the gates check them, the store loads them. A new kind of input starts as a file
  a script writes, or a member's line by observe.py.
"""

SUBJECTS = (    # (title, the tables and views it holds, in their order); the calls of each subject: ASKS and VERBS
    ("Ships and pilots", ("ships", "ship_skills", "ship_modules", "ship_cargo", "fleet_positions", "hull_readiness", "stats_pilot_hour", "stats_pilot_last")),
    ("Routes and runs", ("routes", "plan_routes", "runs", "route_hour", "route_earnings", "fuel_sinks", "stats_route_author", "missions")),
    ("Money", ("stats_money_hour",)),
    ("Markets", ("books", "ladders", "moves", "market_hour", "contract_candidates")),
    ("Map and intel", ("systems", "lanes", "places", "fields", "herds", "readings", "reading_day", "stations", "outpost_candidates", "factions", "public_battles", "leaderboards", "rival_snapshots", "met", "player_comms", "observations")),
    ("Our faction", ("faction", "faction_members", "bases", "our_stations", "faction_facilities", "faction_storage", "inventory_faction",
                     "territory", "sites")),
    ("Stock and reserve", ("holdings", "inventory", "inventory_by_station", "stock_hour", "needs", "need_status")),
    ("The catalog", ("items", "recipes", "recipe_inputs", "recipe_outputs", "recipe_facilities", "facilities", "facility_materials", "hulls",
                     "hull_materials", "skills", "game_releases")),
    ("Supply", ("supply_chains", "supply_status", "stats_supply_hour")),
    ("Statistics", ("stats_time", "stats_refill", "stats_figures")),
    ("Written knowledge", ("docs", "doc_versions", "division_playbooks")),
    ("Plans and the door", ("birth_plans",)),
    ("The store itself", ("source", "cursor", "meta")),
)
OTHER = "Other"                # the subject of a table or a call no entry above names
BOOKKEEPING = ("source", "cursor", "meta")      # the store's own marks: the files read, where a record was read to, its settings
ASKS = {        # MCP tool -> {view, action or ask (or '' for every other value): subject}
    "fleet": {"money": "Money", "history": "Money", "forecast": "Money", "levels": "Ships and pilots", "board": "Ships and pilots",
              "capacity": "Routes and runs", "standing": "Routes and runs", "tasks": "Routes and runs", "refill": "Statistics",
              "kpi": "Statistics", "contribution": "Statistics", "classes": "Statistics", "time": "Statistics", "supply": "Statistics",
              "xp": "Statistics", "upgrades": "Statistics", "alerts": "Statistics", "watchdog": "Statistics", "rival": "Map and intel", "rivals": "Map and intel", "contracts": "Markets", "shipping": "Markets", "progression": "Our faction", "scorecard": "Statistics", "upgrade_plan": "Ships and pilots"},
    "ship": {"": "Ships and pilots"}, "routes": {"": "Routes and runs"}, "route": {"": "Routes and runs"}, "candidates": {"": "Routes and runs"},
    "market": {"": "Markets"}, "stock": {"": "Stock and reserve"}, "catalog": {"": "The catalog"}, "base_plan": {"": "Our faction"},
    "system": {"": "Map and intel"}, "comms": {"contacts": "Map and intel", "safe_comms": "Map and intel", "": "Written knowledge"}, "search": {"": "Written knowledge"},
    "docs": {"": "Written knowledge"}, "supply": {"": "Supply"}, "sql": {"": "The store itself"},
    "fill": {"": "Plans and the door"}, "plan": {"": "Plans and the door"}, "command": {"": "Plans and the door"},
    "goal": {"": "Plans and the door"}, "hold": {"": "Plans and the door"}, "stop": {"": "Plans and the door"}, "fund": {"": "Money"},
}
ASKS["needs"] = {"": "Stock and reserve"}          # the needs register (needs.py): its table, need_status and the tool
VERBS = {       # hive.py verbs that no tool reaches as hive.py <verb> (the tool `hive` passes them): subject; None: a tool gives
    "gauges": "Ships and pilots", "store": "Routes and runs", "store price": "Markets", "empire": "Our faction",   # the same answer
    "flow": "Stock and reserve", "briefing": "Plans and the door", "handbook": "Written knowledge",               # through its own script
    "surplus": None, "inventory": None, "supply": None,
}
VERBS["needs"] = None                              # the tool needs gives the same answers (needs.py)
VERBS["watchdog"] = None                           # the tool fleet view=watchdog gives the same answer (watchdog.py)
READERS = {     # docs.py kind -> the readers beside `docs doc=<kind>` (hive.py docs <kind>) that answer it
    "orders": "comms view=orders", "log": "comms view=requests, view=digest", "plan": "plan action=show; docs view=division",
    "metrics": "fleet view=<figure>", "handbook": "docs view=handbook (hive.py handbook)", "member": "docs view=division",
    "guidebook": "docs view=division",
}
WRITE = r"(?:INSERT(?:\s+OR\s+\w+)?\s+INTO|REPLACE\s+INTO|UPDATE)\s+%s\b"
DELETE = r"DELETE\s+FROM\s+%s\b"
HOURLY = "once an hour (the store's first pass of a UTC hour)"


class Refused(Exception):
    """The generator cannot write the handbook: the reason names the table or the part."""


# ---- the code it reads

def modules(root):
    """The fleet's modules the handbook is written from, imported from <root>/game/fleet."""
    folder = str(Path(root).resolve() / "game" / "fleet")
    if folder not in sys.path:
        sys.path.insert(0, folder)
    return {name: importlib.import_module(name) for name in ("store", "stats", "docs", "supply", "collective_mcp", "needs")}


def fresh_schema(store):
    """A fresh empty schema in memory, made by the store's own setup functions (as open_live makes live.db)."""
    conn = sqlite3.connect(":memory:")
    conn.executescript(store.SCHEMA)
    store.setup_snapshot(conn)
    return conn


def functions(mods):
    """[(module.name, source)] of every function and method the store's modules define: who writes a table."""
    out = []
    for key in ("store", "stats", "docs", "supply") + (("needs",) if "needs" in mods else ()):     # needs.py writes need_status
        module = mods[key]
        for name, thing in sorted(vars(module).items()):
            found = [(name, thing)] if inspect.isfunction(thing) and thing.__module__ == module.__name__ else []
            if inspect.isclass(thing) and thing.__module__ == module.__name__:
                found = [("%s.%s" % (name, n), f) for n, f in sorted(vars(thing).items()) if inspect.isfunction(f)]
            for label, func in found:
                try:
                    out.append(("%s.%s" % (key, label), inspect.getsource(func)))
                except (OSError, TypeError):
                    continue
    return out


def first_sentence(text, stop=":"):
    """The first sentence of a docstring, up to `stop` or its first full stop, on one line."""
    words = " ".join(str(text or "").split())
    for mark in (stop, ". "):
        if mark in words:
            words = words.split(mark)[0]
    return words.rstrip(".")


def doc_entries(doc, start, end):
    """[(name, text)] of a docstring's block of entries after the line holding `start`, up to the line that begins with
    `end`: an entry is a line indented by 6 to 8 that names it, then two spaces or more and its text; deeper lines go on."""
    out, inside = [], False
    for line in str(doc).splitlines():
        if start in line:
            inside = True
            continue
        if inside and end and line.strip().startswith(end):
            break
        if not inside:
            continue
        found = re.match(r"^ {6,8}(\S.*?)\s{2,}(\S.*)$", line)
        if found and len(line) - len(line.lstrip()) <= 8:
            out.append([found.group(1).strip(), found.group(2).strip()])
        elif out and line.startswith(" " * 12) and line.strip():
            out[-1][1] += " " + line.strip()
    return [(name, text) for name, text in out]


def cut(text, size):
    """One line of at most `size` characters, cut at a word with `...`."""
    text = " ".join(str(text).split())
    if len(text) <= size:
        return text
    return text[:size - 3].rsplit(" ", 1)[0].rstrip(",;:(") + "..."


def cell(text):
    return str(text).replace("|", "/")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


# ---- where to ask what

SELECTORS = ("view", "action", "ask")
SEGMENT = re.compile(r"\b(view|action|ask)=([a-z_]+)((?:(?:,| or| and) [a-z_]+)*)(?: \(default\))?:\s")


def sentence(text):
    """The first sentence of a text (up to a full stop before a capital letter)."""
    return re.split(r"(?<=\.)\s+(?=[A-Z])", str(text).strip(), maxsplit=1)[0]


def segments(text):
    """({value: its text}, the text before them) of a tool's text, split at `view=<value>:` (and `view=a or b:`): the
    first sentence after each."""
    found = list(SEGMENT.finditer(text))
    out = {}
    for n, match in enumerate(found):
        end = found[n + 1].start() if n + 1 < len(found) else len(text)
        values = [match.group(2)] + [w for w in re.findall(r"[a-z_]+", match.group(3)) if w not in ("or", "and")]
        for value in values:
            out.setdefault(value, sentence(text[match.end():end]))
    return out, (text[:found[0].start()] if found else text).strip()


def naming(text, words):
    """The first sentence of a text that holds one of `words` (any case), or ''."""
    for part in re.split(r"(?<=\.)\s+(?=[A-Z])", str(text)):
        if any(word.lower() in part.lower() for word in words):
            return part.strip()
    return ""


def plan_line(tool, args):
    """(the arguments, the script line) of one tool call: a value the plan asks for (`this needs: x`) stands as <x>;
    None when the plan builds no line."""
    args = dict(args)
    for name in tool.get("required", []):
        args.setdefault(name, ["<%s>" % name] if tool["args"].get(name, {}).get("type") == "array" else "<%s>" % name)
    lines = None
    for _try in range(4):
        try:
            lines = tool["plan"](args)
            break
        except ValueError as error:
            names = [n.strip() for n in str(error).split("this needs:")[-1].split(",") if n.strip() in tool["args"]]
            if not names:
                return None
            for name in names:
                args[name] = "<%s>" % name
    if not lines:
        return None
    script, argv = lines[0]
    return args, " ".join([Path(script).name] + [a if " " not in a else '"%s"' % a for a in argv])


def mcp_call(name, args):
    shown = " ".join("%s=%s" % (k, v if not isinstance(v, list) else "[%s]" % ", ".join(v)) for k, v in args.items())
    return ("%s %s" % (name, shown)).strip()


def hive_verbs(root):
    """[(the verb as hive.py's usage names it, what it answers)] from hive.py's docstring, read as text, never run: the
    WHAT block, then each verb of the USAGE block the WHAT block lacks, with the first line of game/fleet/<verb>.py."""
    folder = Path(root).resolve() / "game" / "fleet"
    doc = ast.get_docstring(ast.parse((folder / "hive.py").read_text(encoding="ascii"))) or ""
    out = doc_entries(doc, "and prints one answer:", "RULES:")
    named = {name.strip().split(" ")[0] for label, _text in out for name in label.split(",")}
    for line in doc.splitlines():
        found = re.match(r"^\s+hive\.py ([a-z_]+)\b", line)
        if found and found.group(1) not in named:
            named.add(found.group(1))
            module = folder / ("%s.py" % found.group(1))
            text = ""
            if module.is_file():
                head = (ast.get_docstring(ast.parse(module.read_text(encoding="ascii"))) or "").split("\n")[0]
                text = head.split(" -- ", 1)[-1]
            out.append((found.group(1), text or "see its usage: hive.py --help"))
    return out


def calls(tool):
    """[(value, arguments)] of the calls one line each stands for: every value of the tool's view, action or ask; for a
    tool without one, the call with its required arguments and each optional text argument that changes the script or
    its first word (sql query=..., candidates id=...)."""
    selector = next((s for s in SELECTORS if s in tool["args"] and tool["args"][s].get("enum")), None)
    if selector:
        return [(value, {selector: value}) for value in tool["args"][selector]["enum"]]
    out, base = [("", {})], plan_line(tool, {})
    for name, spec in tool["args"].items():
        if name in tool.get("required", []) or spec.get("type") != "string" or spec.get("enum"):
            continue
        made = plan_line(tool, {name: "<%s>" % name})
        if made and base and made[1].split()[:2] != base[1].split()[:2]:
            out.append((name, {name: "<%s>" % name}))
    return out


def ask_rows(mods, root):
    """{subject: [(text, MCP call, shell line)]}: every view, action or ask of every tool, then the hive.py verbs that no
    tool reaches as hive.py <verb>. A line's text: the tool's own for that value, else hive.py's for the verb it runs,
    else the tool's sentence that names the value, else the tool's text."""
    tools = mods["collective_mcp"].TOOLS
    verbs = {name.strip().split(" ")[0]: text for label, text in hive_verbs(root) for name in label.split(",")}
    rows, reached = {}, set()
    for name, tool in tools.items():
        if name == "hive":
            continue
        parts, head = segments(tool["text"])
        for value, given in calls(tool):
            made = plan_line(tool, given)
            if made is None:
                continue
            args, shell = made
            verb = shell.split()[1] if shell.startswith("hive.py ") and len(shell.split()) > 1 else ""
            reached |= {verb, " ".join(shell.split()[1:3])}
            text = parts.get(value) or (verbs.get(verb) if verb and verb != name else "") or naming(tool["text"], ["=%s " % value, "with %s:" % value]) \
                or verbs.get(verb) or head
            subject = ASKS.get(name, {}).get(value) or ASKS.get(name, {}).get("") or OTHER
            rows.setdefault(subject, []).append((cut(text, ASK_CHARS), mcp_call(name, args), shell))
    for label, text in hive_verbs(root):
        words = [w.strip(",") for w in label.split()]
        verb = " ".join(words[:2]) if " ".join(words[:2]) in VERBS else words[0]
        if verb in reached or (verb in VERBS and VERBS[verb] is None):
            continue
        extra = [w for w in words[1:] if w != "reserve"] if verb != words[0] else []
        call = "hive verb=%s%s" % (words[0], " args=[%s]" % ", ".join(extra) if extra else "")
        if "," in label:
            call = "hive verb=%s" % " or ".join(w.strip() for w in label.split(","))
        rows.setdefault(VERBS.get(verb, OTHER), []).append((cut(text, ASK_CHARS), call, "hive.py " + label.replace(", ", " or ")))
    return rows


# ---- the tables

def kinds_of(mods, conn):
    """{table or view: kind} for every table and view of the fresh schema."""
    store, stats = mods["store"], mods["stats"]
    found = dict(conn.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%'"))
    snapshot = {name for name, _c, _k in store.SNAPSHOT}
    out = {}
    for name, kind in found.items():
        out[name] = ("view" if kind == "view" else "bookkeeping" if name in BOOKKEEPING else "snapshot" if name in snapshot
                     else "statistics" if name in getattr(stats, "TABLES", ()) + getattr(mods.get("needs"), "TABLES", ()) else "history")
    return out


def loader_files(files):
    """The files of one loader, as the code names them: a folder's *.json, one file, or its function's first sentence."""
    label = getattr(files, "__qualname__", "")
    try:
        names = inspect.getclosurevars(files).nonlocals
    except (TypeError, ValueError):
        names = {}
    if label.startswith("data_files."):
        return "data/%s/*.json" % names.get("folder", "?")
    if label.startswith("data_file."):
        return "data/%s" % names.get("name", "?")
    if label.startswith("repo_files."):
        return "game/%s/*.json" % names.get("folder", "?")
    module = sys.modules.get(getattr(files, "__module__", ""))
    if getattr(module, "KINDS", None) is not None:
        return "the files of every kind of docs.KINDS (The kinds, in %s)" % part_name("Written knowledge")
    if isinstance(getattr(module, "NAME", None), str):
        return module.NAME
    return first_sentence(inspect.getdoc(files)) or getattr(files, "__name__", "?")


def loader_of(store, name):
    """(loader, its files function) of a snapshot table, or None for one the loader list does not hold (ships)."""
    return next(((loader, files) for loader, tables, files, _whole in store.LOADERS if name in tables), None)


def fixed(files):
    """True when a loader reads files of a fixed name (a missing one keeps its rows), False for a folder's files (a file
    that went takes its rows): its files as an empty data folder and an empty repository show them."""
    with tempfile.TemporaryDirectory(prefix="handbook-") as empty:
        try:
            return any(entry[3] for entry in files(empty, empty))
        except (OSError, ValueError, TypeError, IndexError):
            return False


def stats_parts(stats):
    """{function name: (part, seconds between two runs or None, the constant's name)} of stats.compute's parts."""
    try:
        source = inspect.getsource(stats.compute)
    except (OSError, TypeError):
        return {}
    out = {}
    for part, every, func in re.findall(r'\("(\w+)",\s*(\w+),\s*lambda:\s*(\w+)\(', source):
        seconds = getattr(stats, every, None)
        out[func] = (part, seconds if isinstance(seconds, int) else None, every)
    return out


def part_text(part, seconds, constant):
    return "stats.py part `%s`, %s" % (part, HOURLY if seconds == 3600 else "every %d s (%s)" % (seconds, constant) if seconds else "when due (%s)" % constant)


def refresh_text(mods, name, kind, writers, parts, code):
    """How often a table is refreshed, as the code says it."""
    store = mods["store"]
    every = "the store's pass (every %d s)" % store.EVERY
    if kind == "view":
        return "computed when asked, from its tables"
    records = sorted({rec[0] for rec in store.RECORDS if rec[1] == name})
    if records:
        shown = records[0] if len(records) == 1 else "%s (%d records)" % (re.sub(r"/[a-z]+\.jsonl$", "/<division>.jsonl", records[0]), len(records))
        return "%s: the new whole lines of data/%s" % (every, shown)
    sums = [rec for rec in store.RECORDS if re.search(WRITE % name, inspect.getsource(rec[3]))]
    if sums:
        return "%s: summed again for the %s that got new rows of %s" % (every, "days" if sums[0][4] == store.DAY else "hours", sums[0][1])
    if kind == "snapshot":
        found = loader_of(store, name)
        if found:
            return "%s, when a file changed (size or mtime): loader `%s`, %s" % (every, found[0], loader_files(found[1]))
        fed = getattr(store, "FED", {}).get(name) or ()
        doc = first_sentence(inspect.getdoc(store.Pass.fleet)) if hasattr(getattr(store, "Pass", None), "fleet") else ""
        return "%s: %s%s" % (every, doc or "its loader", " (loaders %s)" % ", ".join(fed) if fed else "")
    if kind == "statistics":
        for writer in writers:                                      # a part's own function writes it
            if writer.split(".")[-1] in parts:
                return part_text(*parts[writer.split(".")[-1]])
        for func, part in sorted(parts.items()):                    # or a part's function calls the one that writes it
            if any(re.search(r"\b%s\(" % re.escape(w.split(".")[-1]), code.get("stats." + func, "")) for w in writers):
                return part_text(*part)
    if writers:
        return "%s, by %s" % (every, ", ".join(writers[:4]) + (" and %d more" % (len(writers) - 4) if len(writers) > 4 else ""))
    return "not stated in the code"


def keep_text(mods, name, kind, deleters):
    """How long a table's rows are kept, as the code says it."""
    store, stats = mods["store"], mods["stats"]
    raw = {rec[1]: rec[4] for rec in store.RECORDS}
    if kind == "view":
        return "nothing: a view stores no row"
    if kind == "snapshot":
        found = loader_of(store, name)
        if found is None or fixed(found[1]):
            return "the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)"
        return "while its file stands: a file's rows are replaced when it changes and go when it goes"
    if name in raw or name in store.KEEP_TABLES:
        days = max(store.KEEP_DAYS, store.KEEP_TABLES.get(name, 0))
        why = "KEEP_TABLES" if store.KEEP_TABLES.get(name, 0) > store.KEEP_DAYS else "KEEP_DAYS, --keep-days"
        return "%g days (store.py %s), then deleted by whole %s" % (days, why, "days" if raw.get(name) == store.DAY else "hours")
    if name in getattr(stats, "KEEP", {}):
        return "%g days (stats.py KEEP)" % stats.KEEP[name]
    rules = getattr(store, "retention", None)              # r22: the tables once kept for good (retention.py RETAIN, BOUNDED)
    if rules is not None and (name in rules.RETAIN or name in rules.BOUNDED):
        return rules.kept(name)
    if deleters:
        return "not over time: %s delete%s rows, what stands is the newest" % (", ".join(deleters[:3]), "" if len(deleters) > 1 else "s")
    return "for good: no step of the code deletes its rows"


def view_tables(conn, name, tables):
    sql = (conn.execute("SELECT sql FROM sqlite_master WHERE name = ?", (name,)).fetchone() or ("",))[0] or ""
    return list(dict.fromkeys(t for t in re.findall(r"(?:FROM|JOIN)\s+(\w+)", sql) if t in tables))


def describe(mods):
    """[(name, entry)] of every table and view in the schema's order: kind, description, columns, key, keep, refresh,
    examples. Refused when one has no description."""
    store = mods["store"]
    conn = fresh_schema(store)
    try:
        found = store.schema(conn)
        missing = [name for name, entry in found.items() if not entry["description"]]
        if missing:
            raise Refused("no description in store.DESCRIPTIONS (or the module that makes it) for: %s" % ", ".join(missing))
        kinds, parts = kinds_of(mods, conn), stats_parts(mods["stats"])
        code = dict(functions(mods))
        out = []
        for name, entry in found.items():
            writers = sorted(label for label, src in code.items() if re.search(WRITE % re.escape(name), src))
            deleters = sorted(label for label, src in code.items() if re.search(DELETE % re.escape(name), src))
            info = conn.execute("SELECT name, pk FROM pragma_table_info(?)", (name,)).fetchall()
            out.append((name, {"kind": kinds[name], "description": entry["description"], "columns": [c for c, _t in entry["columns"]],
                               "key": [n for n, pk in sorted(info, key=lambda r: r[1]) if pk], "examples": list(entry["examples"]),
                               "from": view_tables(conn, name, set(found)) if kinds[name] == "view" else [],
                               "keep": keep_text(mods, name, kinds[name], deleters),
                               "refresh": refresh_text(mods, name, kinds[name], writers, parts, code)}))
        return out
    finally:
        conn.close()


def table_block(name, entry, examples):
    kind = entry["kind"] + (" over %s" % ", ".join(entry["from"]) if entry["from"] else "")
    lines = ["## %s" % name, "", entry["description"], "", "- Kind: %s" % kind,
             "- Columns: %s%s" % (", ".join(entry["columns"]), "; one row per %s" % ", ".join(entry["key"]) if entry["key"] else ""),
             "- Kept: %s" % entry["keep"], "- Refreshed: %s" % entry["refresh"]]
    shown = entry["examples"][:examples]
    for question, sql in shown:
        lines.append("- %s: `%s`" % (question, sql))
    if len(shown) < len(entry["examples"]):
        more = len(entry["examples"]) - len(shown)
        lines.append("- %d more example%s: `hive.py schema %s`" % (more, "" if more == 1 else "s", name))
    if not entry["examples"]:
        lines.append("- No example is written for it yet (store.EXAMPLES).")
    return lines


# ---- the written knowledge and the figures

def kinds_block(docs):
    lines = ["## The kinds", "", "What docs.py mirrors into the tables docs and doc_versions (docs.KINDS); the files stay the source.", "",
             "| Kind | Files | Owner | Ask |", "|---|---|---|---|"]
    rows = {}
    for kind, pattern, owner in docs.KINDS:
        rows.setdefault(kind, ([], owner))[0].append(pattern)
    for kind, (patterns, owner) in rows.items():
        who = {"": "the division its file's name or folder names", "*": "each entry's author's division"}.get(owner, owner)
        ask = "docs doc=%s (hive.py docs %s)" % (kind, kind) + ("; " + READERS[kind] if kind in READERS else "")
        lines.append("| %s | %s | %s | %s |" % (kind, ", ".join("`%s`" % p for p in patterns), who, ask))
    return lines


def figures_block(mods, root):
    stats, docs = mods["stats"], mods["docs"]
    try:
        sections = docs.parse_markdown((Path(root).resolve() / "game" / "metrics.md").read_text(encoding="ascii"))
    except (OSError, UnicodeDecodeError):
        sections = []
    fleet = mods["collective_mcp"].TOOLS.get("fleet", {}).get("args", {}).get("view", {}).get("enum", [])
    lines = ["## The figures", "", "The views of stats.py (stats.VIEWS_SHOWN), computed by the store into stats_figures and its other tables; "
             "each defined in game/metrics.md (`hive.py docs metrics --section <id>`).", ""]
    for view in stats.VIEWS_SHOWN:
        found = next(((sid, title) for sid, title, _text in sections if title.split(" ")[0] == view), None)
        where = "`%s` (%s)" % found if found else "no section of game/metrics.md"
        ask = "fleet view=%s, hive.py stats %s" % (view, view) if view in fleet else "hive.py stats %s" % view
        lines.append("- %s: %s; ask: %s" % (view, where, ask))
    return lines


# ---- the files

def subjects_of(described):
    """[(title, [table names])] in SUBJECTS's order, then OTHER for a table no subject names."""
    known = dict(described)
    out = [(title, [t for t in tables if t in known]) for title, tables in SUBJECTS]
    named = {t for _title, tables in SUBJECTS for t in tables}
    rest = [name for name, _entry in described if name not in named]
    return out + ([(OTHER, rest)] if rest else [])


def part_name(title):
    return "%s/%s.md" % (FOLDER, slug(title))


def part(mods, root, title, tables, known):
    """One subject's file: the most examples a table that keep it under CAP; Refused above the cap with one."""
    size = 0
    for examples in range(EXAMPLES_MAX, 0, -1):
        lines = ["# %s -- the store's handbook" % title, "", MARK,
                 "Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.",
                 "One table alone: `hive.py handbook <table>`; its rows: `hive.py sql \"SELECT ...\"` (the tool sql)."]
        for name in tables:
            lines += [""] + table_block(name, known[name], examples)
        if title == "Statistics":
            lines += [""] + figures_block(mods, root)
        if title == "Written knowledge":
            lines += [""] + kinds_block(mods["docs"])
        text = "\n".join(lines) + "\n"
        if len(text) <= CAP:
            return text
        size = len(text)
    raise Refused("%s is %d characters with one example a table, more than CAP %d: split the subject" % (part_name(title), size, CAP))


def master(mods, root, ident, described, subjects):
    counts = {kind: sum(1 for _n, e in described if e["kind"] == kind) for kind in ("snapshot", "history", "statistics", "bookkeeping", "view")}
    rows = ask_rows(mods, root)
    lines = ["---", "name: handbook", "id: %s" % ident, "tier: guide", "author: Unity", "links:"]
    lines += ["  - %s" % p for p in ("game/fleet/store.py", "game/fleet/stats.py", "game/fleet/docs.py", "game/fleet/collective_mcp.py",
                                     "game/fleet/hive.py", "game/metrics.md", "scripts/handbook.py")]
    lines += ["---", "", "# handbook.md -- the store's handbook: how the fleet's data flows, where to ask what, every table", "", MARK,
              "The gate `python3 -I -B scripts/handbook.py --check` fails a file that differs; the hourly job writes them again. Only How",
              "the data flows is kept by hand, in the script. Every table and view stands in the file of its subject (game/handbook/).",
              "Read it in parts: `hive.py handbook [<topic>]` (MCP: the tool docs, view=handbook, topic=...): no topic gives the",
              "contents and how the data flows; a table's name, a subject or a word gives its sections. The store holds every file",
              "as kind `handbook` of the table docs, one row a section, every version in doc_versions.", "",
              "The store: %d tables and %d views (%d snapshot, %d history, %d statistics, %d bookkeeping); the MCP tool `collective`: %d tools."
              % (len(described) - counts["view"], counts["view"], counts["snapshot"], counts["history"], counts["statistics"],
                 counts["bookkeeping"], len(mods["collective_mcp"].TOOLS)),
              "Kinds: snapshot = what a file says now (replaced when the file changes; it also carries `src`, the file its row came",
              "from; dropped and loaded again when its definition changes); history = rows kept over time (raw rows for days, sums",
              "as each table's Kept line says); statistics = computed by stats.py when due; view = a query over tables, computed when",
              "asked; bookkeeping =",
              "the store's own marks. Columns come from a fresh empty schema; every example runs in test_fleet_store_state.py.", "",
              "## Contents", "",
              "- How the data flows (below): the game to the members; what is private, what is public",
              "- Where to ask what (below): a question -> the MCP call and the shell line, by subject"]
    for title, tables in subjects:
        extra = {"Statistics": " and the figures", "Written knowledge": " and the kinds"}.get(title, "")
        if tables:
            lines.append("- %s, `%s`: %s%s" % (title, part_name(title), ", ".join(tables), extra))
    lines += ["", "## How the data flows", ""] + FLOW.rstrip("\n").split("\n")
    lines += ["", "## Where to ask what", "",
              "Ask through the MCP tool `collective` (each member's tools `mcp_collective_<tool>`) or in a shell from the repository:",
              "`python3 -I -B game/fleet/hive.py <verb>` (the other scripts the same way). The tool `hive` passes any verb of hive.py",
              "(`hive verb=<verb> args=[...]`); the tool `sql` asks any SELECT on the tables (`hive.py sql \"<SELECT ...>\"`). One line",
              "per question, from the tools' own texts (collective_mcp.TOOLS) and hive.py's usage; <x> is a value you give."]
    for title in [t for t, _tables in SUBJECTS] + [OTHER]:
        if rows.get(title):
            lines += ["", "### %s" % title, "", "| What it answers | MCP | Shell |", "|---|---|---|"]
            lines += ["| %s | %s | %s |" % (cell(text), cell(call), cell(shell)) for text, call, shell in rows[title]]
    text = "\n".join(lines) + "\n"
    if len(text) > CAP:
        raise Refused("%s is %d characters, more than CAP %d" % (MASTER, len(text), CAP))
    return text


def new_id(now):
    """A timestamp id of this moment, never one ending on :00 (scripts/validate-ids.sh)."""
    while time.gmtime(now).tm_sec == 0:
        now -= 1
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(now))


def build(root, ident, mods=None):
    """{repository path: text} of every file of the handbook. Refused when FLOW is too long, a table has no description,
    a file is above CAP, or a text is not ASCII."""
    if len(FLOW) > FLOW_CAP:
        raise Refused("How the data flows is %d characters, more than FLOW_CAP %d" % (len(FLOW), FLOW_CAP))
    mods = mods or modules(root)
    described = describe(mods)
    subjects = subjects_of(described)
    known = dict(described)
    files = {MASTER: master(mods, root, ident, described, subjects)}
    for title, tables in subjects:
        if tables:
            files[part_name(title)] = part(mods, root, title, tables, known)
    for path, text in files.items():
        bad = next((n for n, ch in enumerate(text) if ord(ch) > 127), None)
        if bad is not None:
            raise Refused("%s is not ASCII at character %d: %r" % (path, bad, text[max(0, bad - 40):bad + 10]))
    return files


def unfiled(files):
    """What no subject names, one warning each (never a fault: the handbook still says it, under Other): a table or
    view in other.md, a call under Where to ask what, Other."""
    out = ["the table or view `%s` stands under %s: name it in SUBJECTS of scripts/handbook.py" % (name, OTHER)
           for name in re.findall(r"(?m)^## (\S+)$", files.get(part_name(OTHER), ""))]
    rest = files.get(MASTER, "").split("\n### %s\n" % OTHER, 1)
    for row in (rest[1].split("\n## ")[0].splitlines() if len(rest) == 2 else []):
        cells = row.split(" | ")
        if row.startswith("| ") and len(cells) == 3 and not row.startswith("| What it answers"):
            out.append("the call `%s` stands under %s: name it in ASKS or VERBS of scripts/handbook.py" % (cells[1], OTHER))
    return out


def current_id(root):
    """The id of game/handbook.md on disk, or None."""
    try:
        text = (Path(root) / MASTER).read_text(encoding="ascii")
    except (OSError, UnicodeDecodeError):
        return None
    found = ID.search(text.split("\n---\n", 1)[0]) if text.startswith("---\n") else None
    return found.group(1) if found else None


def stale(root, files):
    """(paths to write, paths to remove): what differs from the disk, and what game/handbook/ holds beyond the build."""
    root = Path(root)
    changed = []
    for path, text in sorted(files.items()):
        try:
            same = (root / path).read_text(encoding="ascii") == text
        except (OSError, UnicodeDecodeError):
            same = False
        if not same:
            changed.append(path)
    folder = root / FOLDER
    extra = sorted(p.relative_to(root).as_posix() for p in folder.rglob("*") if p.is_file() and p.relative_to(root).as_posix() not in files) \
        if folder.is_dir() else []
    return changed, extra


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def retry(root, *args, tries=3, wait=2.0):
    """A git command tried up to `tries` times (another member's commit can hold the index for a moment)."""
    code, out = 1, ""
    for n in range(tries):
        code, out = git(root, *args)
        if code == 0:
            return code, out
        if n + 1 < tries:
            time.sleep(wait)
    return code, out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write the store's handbook (game/handbook.md, game/handbook/) from the code.")
    parser.add_argument("--root", default=str(HERE.parent))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if args.commit:
        _code, out = git(root, "status", "--porcelain", "--untracked-files=all", "--", *SOURCES)
        other = sorted(line[3:] for line in out.splitlines() if line.strip())
        if other:
            print("%s: not built; its sources hold changes that are not committed: %s" % (MASTER, ", ".join(other)))
            return 0
    begun = time.time()
    try:
        files = build(root, current_id(root) or new_id(time.time()))
    except Refused as error:
        print("%s: not written: %s" % (MASTER, error))
        if args.check:
            print("Errors: 1 | Warnings: 0")
        return 1
    seconds = time.time() - begun
    changed, extra = stale(root, files)
    warnings = unfiled(files)
    for line in warnings:
        print("WARNING: " + line)
    size = "%d files, %s characters, the largest %d, generated in %.2f s" % (len(files), format(sum(len(t) for t in files.values()), ","),
                                                                            max(len(t) for t in files.values()), seconds)
    if args.check:
        if changed or extra:
            print("%s: stale: %d to write (%s), %d to remove (%s) | %s" % (MASTER, len(changed), ", ".join(changed[:4]), len(extra), ", ".join(extra[:4]), size))
            print("ERROR: run `python3 -I -B scripts/handbook.py` and commit game/handbook.md and game/handbook/")
            print("Errors: 1 | Warnings: %d" % len(warnings))
            return 1
        print("%s: current | %s" % (MASTER, size))
        print("Errors: 0 | Warnings: %d" % len(warnings))
        return 0
    if not changed and not extra:
        print("%s: current | %s" % (MASTER, size))
        return 0
    for path in changed:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".tmp")
        tmp.write_text(files[path], encoding="ascii")
        tmp.replace(target)
    for path in extra:
        (root / path).unlink()
    print("%s: written: %d files (%s), %d removed (%s) | %s" % (MASTER, len(changed), ", ".join(changed), len(extra), ", ".join(extra) or "--", size))
    if args.commit:
        paths = [MASTER, FOLDER]
        retry(root, "add", "-A", "--", *paths)
        code, out = retry(root, "-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev", "commit", "-q", "-m",
                          "%s, %s/: rebuilt from the code (scripts/handbook.py)" % (MASTER, FOLDER), "--", *paths)
        if code:
            retry(root, "reset", "-q", "--", *paths)
            for path in paths:                                      # one at a time: a path not in HEAD fails alone
                git(root, "checkout", "--", path)
                git(root, "clean", "-fdq", "--", path)
            print("%s: written but NOT COMMITTED, taken back: %s" % (MASTER, out.strip()[:200]))
            return 1
        print("%s: committed" % MASTER)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
