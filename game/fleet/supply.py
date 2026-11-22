#!/usr/bin/env python3
"""supply.py -- the supply chains: the goods the fleet must never run out of, each at its place against what stands there now, with the ships on duty for it.

WHAT: game/supply/chains.tsv (kept by the Fleet Admiral with Logistics) names each chain: an item, the place it must
      stand at (a base of ours, a system, or `fleet` for anywhere), the units that must stand there at least (keep),
      the units used an hour, the routes that gather, craft or carry it (its sources) and the division that keeps it
      on duty (its keeper). The store (store.py) reads the file into the table supply_chains whenever it changed; its
      view supply_status sets each chain beside the storage book (table holdings), the store's hourly samples
      (stock_hour), the order each ship flies (ships.flies) and the plans (plan_routes). This script answers from it:
        show     every chain: status, stock, keep, need an hour, the change over 24 hours, its sources with the ships
                 on them now and how many of them stand in a plan; broken rows and short chains first
        check    the gate: one line per short chain, per broken row and per item, place or source the readings do not
                 know; HALT (exit 1) when there is one, else PASS
        duty     for each short chain with sources: the source routes the plan of its keeper division does not hold
                 yet, and the change that puts them in as standing work (the division's list Then, in front of its
                 census and park routes: plan.put_then and plan.apply, the way `fill.py add` puts a route in); the
                 routes duty put in earlier whose end came; for a short chain without a source, the route files that
                 bring its item. --write makes the change, behind DUTY_ENABLED
      For store.py: chain_files() and read_chains() read the file; STATUS_VIEW is the view; DESCRIPTIONS and EXAMPLES
      describe both for `hive.py schema`.
RULES:
  - The file is tab-separated, `#` starts a comment, and the header `chain<TAB>item<TAB>place<TAB>keep<TAB>
    need_per_hour<TAB>sources<TAB>keeper<TAB>note` comes before the first chain. A file without it, or not ASCII, is
    not read: the store names it and its rows stay as last read. A row that breaks a rule is kept with its line and
    the reason in `error`, counts as `broken`, and never stops the store nor the other rows. No file: no chains.
  - A row: chain (lower-case letters, digits and dashes, once in the file), item (an item id), place (`fleet`, a
    base id or base name of ours, or a system id), keep (a whole number, 0 or more), need_per_hour (a number, 0 or
    more; empty is 0: not known), sources (route ids with commas, or empty), keeper (Mining, Trade, Logistics,
    Military, Intel or Command), note.
  - Stock is what the storage book holds of the item at the place: at `fleet` every station storage and every hold
    added; at a base id the storage there; at a base name or a system id every base the census (places) or our
    empire (bases) puts there. Stock sums personal storage, ship holds, and faction storage (including outpost fuel
    bunkers from faction_storage, deduplicated against holdings Faction rows). A place the book holds nothing at (place_rows 0) has no reading, and its 0 is said to
    be not measured.
  - Status: short below keep, low below twice keep, ok from twice keep; broken for a row with an error. The change
    over 24 hours is that of the store's hourly samples (newest sample against the newest one at least 24 hours
    older, else the oldest), for `fleet` only: the samples are per division, not per place.
  - Ships on a chain: our ships whose order (ships.flies) is one of its sources now; sources_planned: how many of its
    sources stand in at least one role plan (plan_routes).
  - duty: a source is held when it stands in a role plan of the keeper's division (plan_routes, the repository's copy;
    the live plan is read again inside the change, and a route it holds anywhere is left alone). A source without a
    route file or switched off is named and never added. One plan.apply per division (it commits through fill.commit),
    by the Fleet Admiral or by the keeper for its own division (orders F1); never while fleet/STOP exists.
  - Every route duty puts in carries its own end: data/supply/duty.json keeps it with its chain and an end DUTY_HOURS
    later. A later `duty --write` takes it out of the list Then when its chain is ok, gone, kept by another division or
    no longer names it, or when its end came and the chain is not short; a chain still short at the end renews it.
    Duty takes out only what it put in, and only from the list Then.
  - Rule F23, each class flies its own work (workclass.own): duty puts a source into a division's plan only when it is
    the own work of every role of that division (a gather route into Mining's alone, unless its file's `open_to`
    names the other roles); another is named and never added, and a route duty put in earlier that is not of the
    division's class is taken out at the next `duty --write`. A mission that pays once stays every role's.
  - A storage book that is not whole (ledger.decides: a reading of fewer than ledger.WHOLE_SHARE of the fleet's
    pilots) reads less than the fleet holds: duty puts no source in and renews no end on it, and every answer's first
    line says how whole the book is (requests ENT-284, r22).
  - DUTY_ENABLED = False: `duty --write` is refused (exit 1); `duty` and `duty --dry-run` only say what would change.
  - It reads the store's read copy and the route files; it moves no ship. Only `duty --write` writes: the plan of a
    division (data/plans, game/routes/plans) and data/supply/duty.json.
WHY:  Suggi, 2026-11-17: the goods the fleet must never run out of (iron, fuel, later food and power for our bases) get
      supply chains in the SQL database, visible to every member through the MCP tool, so that ships are always on duty
      for them, kept up to date by scripts and not by hand.

USAGE:
  supply.py [show]              every chain: status, stock, keep, need/h, 24 h change, sources, ships on them
  supply.py check               the gate: one line per short chain, broken row or unknown id; exit 1 on any
  supply.py duty [--dry-run]    what duty would change: sources to put into the keepers' plans, ends due
  supply.py duty --write        make that change (refused while DUTY_ENABLED is False)
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import math
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names
import division                                   # noqa: E402  who runs this, which roles are whose, the data folder
import workclass                                  # noqa: E402  whose work a route is (rule F23)

# store.py imports this file for its reader: store, plan and dispatch are imported inside the functions that need them.

FILE = "supply/chains.tsv"                        # under the repository's game/ folder
NAME = "game/" + FILE                             # its name in the store's table source
HEADER = ["chain", "item", "place", "keep", "need_per_hour", "sources", "keeper", "note"]
KEEPERS = tuple(board.NAMES[member] for member in division.MEMBERS)      # Command, Mining, Logistics, Trade, Military, Intel
CHAIN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ITEM = re.compile(r"^[a-z0-9_]+$")
ROUTE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
DUTY_ENABLED = True            # on since 2026-11-17 20:30 UTC, after its dry run on live data (round r20)
DUTY_HOURS = 24                # a route duty put in stands this long, renewed while its chain is still short
RECORD = "supply/duty.json"    # under the data folder: the routes duty put in, with their ends
STOP = "fleet/STOP"            # under the data folder: nothing is written while the fleet is halted
ORDER = {"broken": 0, "short": 1, "low": 2, "ok": 3}
RULE = ("short = stock below keep, low = below twice keep; `fleet` = every station storage and every hold; the 24 h change is the "
        "store's hourly samples, for `fleet` only (/Nh: the samples span N hours); ships = our ships flying a source now; in plans = sources "
        "that stand in a role plan")
num = "{:,}".format


# ---- the file: store.py's reader

def row_of(number, cells, seen):
    """One row of the file as the table supply_chains holds it; `error` names every rule it breaks (None: a good row)."""
    errors = []
    if len(cells) < len(HEADER) - 1:
        errors.append("needs chain, item, place, keep, need_per_hour, sources and keeper separated by tabs (%d cells)" % len(cells))
    if len(cells) > len(HEADER):
        errors.append("%d cells, the header has %d: a tab inside the note?" % (len(cells), len(HEADER)))
    chain, item, place, keep, need, sources, keeper, note = (cells + [""] * len(HEADER))[:len(HEADER)]
    if not CHAIN.match(chain):
        errors.append("chain `%s`: lower-case letters, digits and dashes" % chain)
    elif chain in seen:
        errors.append("chain %s stands on line %d too" % (chain, seen[chain]))
    seen.setdefault(chain, number)
    if not ITEM.match(item):
        errors.append("item `%s` is no item id" % item)
    if not place:
        errors.append("no place: `fleet`, a base of ours or a system id")
    units = int(keep) if keep.isdigit() else None
    if units is None:
        errors.append("keep must be a whole number, 0 or more, not `%s`" % keep)
    try:
        rate = float(need) if need else 0.0
    except ValueError:
        rate = None
    if rate is None or not math.isfinite(rate) or rate < 0:
        errors.append("need_per_hour must be a number, 0 or more, not `%s`" % need)
        rate = None
    ids = [rid.strip() for rid in sources.split(",") if rid.strip()]
    errors += ["source `%s` is no route id" % rid for rid in ids if not ROUTE.match(rid)]
    named = next((k for k in KEEPERS if k.lower() == keeper.lower()), None)
    if named is None:
        errors.append("keeper `%s`: one of %s" % (keeper, ", ".join(KEEPERS)))
    return {"chain": chain or None, "item": item or None, "place": place or None, "keep": units, "need_per_hour": rate, "sources": ",".join(ids),
            "keeper": named or keeper or None, "note": note, "line": number, "error": "; ".join(errors) or None}


def parse(text):
    """(rows, problem) of the file's text: problem is '' or why the whole file cannot be read (no header)."""
    rows, header, seen = [], False, {}
    for number, raw in enumerate(text.split("\n"), 1):
        line = raw.rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = [cell.strip() for cell in line.split("\t")]
        if not header:
            if cells[:len(HEADER)] != HEADER:
                return [], "line %d: the header `%s` must come before the first chain" % (number, "<TAB>".join(HEADER))
            header = True
            continue
        rows.append(row_of(number, cells, seen))
    if not header:
        return [], "no header `%s`" % "<TAB>".join(HEADER)
    return rows, ""


def read_chains(path, ctx):
    """game/supply/chains.tsv -> supply_chains, one row per line of the file (store.py, a snapshot reader). A file that is
    not ASCII or has no header raises ValueError: the store names it and keeps its rows as last read."""
    rows, problem = parse(Path(path).read_bytes().decode("ascii"))
    if problem:
        raise ValueError(problem)
    return {"supply_chains": rows}


def chain_files(data, root):
    """The store's files of the loader `supply`: the chains file when it is there (a file that went takes its rows)."""
    path = Path(root) / FILE
    return [(NAME, path, read_chains, False, "")] if path.is_file() else []


IN_SOURCES = "instr(',' || c.sources || ',', ',' || %s || ',') > 0"        # a route id among a chain's sources (comma text)
STATUS_VIEW = (
    "CREATE VIEW IF NOT EXISTS supply_status AS WITH "
    "spot(line, place) AS (SELECT line, place FROM supply_chains WHERE place IS NOT NULL AND place <> 'fleet' "
    "UNION SELECT c.line, p.base FROM supply_chains c JOIN places p ON p.base IS NOT NULL AND (p.system = c.place OR p.name = c.place) "
    "UNION SELECT c.line, b.base FROM supply_chains c JOIN bases b ON b.base IS NOT NULL AND (b.system = c.place OR b.name = c.place) "
    "UNION SELECT c.line, fs.base FROM supply_chains c JOIN faction_storage fs ON fs.base IS NOT NULL AND fs.base_name = c.place), "
    "all_stock(place, item, units) AS (SELECT place, item, units FROM holdings "
    "UNION ALL SELECT fs.base, fs.item, fs.units FROM faction_storage fs "
    "WHERE NOT EXISTS (SELECT 1 FROM holdings h2 WHERE h2.pilot = 'Faction' AND h2.place = fs.base AND h2.item = fs.item)), "
    "held(line, units, place_rows) AS (SELECT c.line, COALESCE(SUM(CASE WHEN h.item = c.item THEN h.units END), 0), COUNT(h.place) "
    "FROM supply_chains c LEFT JOIN all_stock h ON c.place = 'fleet' OR h.place IN (SELECT s.place FROM spot s WHERE s.line = c.line) GROUP BY c.line), "
    "newest(hour) AS (SELECT MAX(hour) FROM stock_hour), "
    "base(hour) AS (SELECT COALESCE((SELECT MAX(hour) FROM stock_hour WHERE hour <= (SELECT hour FROM newest) - 86400), (SELECT MIN(hour) FROM stock_hour))), "
    "flow(item, now_units, then_units) AS (SELECT c.item, (SELECT COALESCE(SUM(units), 0) FROM stock_hour WHERE item = c.item AND hour = (SELECT hour FROM newest)), "
    "(SELECT COALESCE(SUM(units), 0) FROM stock_hour WHERE item = c.item AND hour = (SELECT hour FROM base)) FROM supply_chains c GROUP BY c.item) "
    "SELECT c.chain AS chain, c.item AS item, c.place AS place, c.keep AS keep, held.units AS stock, "
    "CASE WHEN c.error IS NOT NULL OR c.keep IS NULL THEN 'broken' WHEN held.units < c.keep THEN 'short' WHEN held.units < 2 * c.keep THEN 'low' ELSE 'ok' END AS status, "
    "c.need_per_hour AS need_per_hour, CASE WHEN c.need_per_hour > 0 THEN ROUND(held.units / c.need_per_hour, 1) END AS hours_left, "
    "CASE WHEN c.place = 'fleet' AND (SELECT hour FROM base) < (SELECT hour FROM newest) THEN f.now_units - f.then_units END AS change_24h, "
    "CASE WHEN c.place = 'fleet' AND (SELECT hour FROM base) < (SELECT hour FROM newest) THEN ((SELECT hour FROM newest) - (SELECT hour FROM base)) / 3600 END AS change_hours, "
    "c.sources AS sources, CASE WHEN COALESCE(c.sources, '') = '' THEN 0 ELSE length(c.sources) - length(replace(c.sources, ',', '')) + 1 END AS sources_listed, "
    "(SELECT COUNT(*) FROM routes r WHERE " + IN_SOURCES % "r.id" + ") AS sources_known, "
    "(SELECT COUNT(*) FROM ships s JOIN routes r ON s.flies = r.kind || ' ' || r.id WHERE " + IN_SOURCES % "r.id" + ") AS ships, "
    "(SELECT COUNT(DISTINCT p.route) FROM plan_routes p WHERE " + IN_SOURCES % "p.route" + ") AS sources_planned, "
    "c.keeper AS keeper, held.place_rows AS place_rows, c.note AS note, c.line AS line, c.error AS error "
    "FROM supply_chains c JOIN held ON held.line = c.line LEFT JOIN flow f ON f.item = c.item;\n")
VIEWS = ("supply_status",)
DESCRIPTIONS = {
    "supply_chains": "the supply chains (game/supply/chains.tsv, kept by the Fleet Admiral with Logistics): per chain the item, its place (`fleet`, a base or "
                     "a system), keep (units that must stand there at least), need per hour (0: not known), sources (route ids with commas), the keeper "
                     "division, note, the file's line, and error (why a broken row does not count; NULL for a good one)",
    "supply_status": "view: each supply chain against what stands at its place now (holdings): stock, status (short below keep, low below twice keep, ok; "
                     "broken), hours left at its need, the change over 24 hours (fleet only, stock_hour), its sources listed and known, our ships on them "
                     "now (ships.flies), its sources in a role plan (plan_routes), place_rows (0: no reading of the place, its 0 is not measured): supply.py show",
}
EXAMPLES = {
    "supply_chains": (("Every chain with its keeper", "SELECT chain, item, place, keep, need_per_hour, keeper FROM supply_chains ORDER BY keeper, chain"),
                      ("Rows of the chains file that do not count, and why", "SELECT line, chain, error FROM supply_chains WHERE error IS NOT NULL ORDER BY line"),
                      ("Chains per keeper", "SELECT keeper, COUNT(*) FROM supply_chains GROUP BY keeper ORDER BY 2 DESC")),
    "supply_status": (("The chains that are broken, short or low, the worst first", "SELECT chain, item, place, stock, keep, status, ships, keeper FROM supply_status "
                       "WHERE status <> 'ok' ORDER BY CASE status WHEN 'broken' THEN 0 WHEN 'short' THEN 1 ELSE 2 END, 1.0 * stock / NULLIF(keep, 0)"),
                      ("Short chains with no ship on their sources", "SELECT chain, item, place, sources, keeper FROM supply_status WHERE status = 'short' AND ships = 0"),
                      ("How the chains held anywhere moved over the last day", "SELECT chain, item, stock, change_24h, change_hours FROM supply_status "
                       "WHERE place = 'fleet' ORDER BY chain")),
}


# ---- the answers, from the store's read copy

def stamp(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t)) if t is not None else "--"


def sources_of(row):
    return [rid for rid in (row.get("sources") or "").split(",") if rid]


def roles_of(name):
    """The roles of a division by its name (Mining, mining ...), as plan.roles_of names them."""
    return sorted(role for role, member in division.ROLES.items() if board.NAMES.get(member, "").lower() == str(name or "").lower())


def read(data):
    """What the answers rest on, from the store's read copy: {rows (supply_status, worst first), error (why there is none),
    file (when the store read the chains file, its note), book (the storage book's time), sample (newest hour of stock_hour),
    items, places, routes {id: (kind, status)}, plans {role: set of routes}}."""
    import store                                  # here, not at the top: store.py imports this file
    out = {"rows": [], "error": None, "file": None, "book": None, "sample": None, "items": set(), "places": set(), "routes": {}, "plans": {}}
    import ledger                                 # r22 (requests ENT-284): how whole the storage book is; duty puts no source in on a book that is not
    out["whole"], out["whole_words"] = ledger.decides(ledger.book_whole(data))
    conn = store.connect(data)
    if conn is None:
        out["error"] = "no read copy of the store yet: %s (the service `store` publishes it)" % (Path(data) / "store" / "read.db")
        return out
    try:
        made = {name for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')")}
        if "supply_status" not in made:
            out["error"] = "the store's copy has no view supply_status yet: the service `store` makes it at its first pass with this code"
            return out
        cursor = conn.execute("SELECT * FROM supply_status")
        names = [column[0] for column in cursor.description]
        out["rows"] = sorted((dict(zip(names, row)) for row in cursor.fetchall()),
                             key=lambda r: (ORDER.get(r["status"], 9), (r["stock"] or 0) / r["keep"] if r["keep"] else 0, r["chain"] or "", r["line"]))
        out["file"] = conn.execute("SELECT t, note FROM source WHERE name = ?", (NAME,)).fetchone()
        book = conn.execute("SELECT mtime FROM source WHERE name = 'stock/storage.json'").fetchone()
        out["book"] = book[0] if book else None
        out["sample"] = conn.execute("SELECT MAX(hour) FROM stock_hour").fetchone()[0]
        out["items"] = {item for (item,) in conn.execute("SELECT id FROM items")}
        for sql in ("SELECT base, name, system FROM places", "SELECT base, name, system FROM bases", "SELECT id, name, NULL FROM systems",
                    "SELECT DISTINCT place, NULL, NULL FROM holdings"):
            for row in conn.execute(sql):
                out["places"].update(value for value in row if value)
        out["routes"] = {rid: (kind, status) for rid, kind, status in conn.execute("SELECT id, kind, status FROM routes")}
        for role, route in conn.execute("SELECT role, route FROM plan_routes"):
            out["plans"].setdefault(role, set()).add(route)
    finally:
        conn.close()
    return out


def first_line(title, res):
    found = res["file"]
    if found is None:
        said = "the store has not read %s (no file, or not read yet)" % NAME
    else:
        said = "%s read by the store %s%s" % (NAME, stamp(found[0]), " (NOT READ NOW: %s; its rows are as last read)" % found[1] if found[1] else "")
    return "%s | %s | storage book of %s%s | newest hourly sample %s" % (title, said, stamp(res["book"]), " (%s)" % res["whole_words"] if res.get("whole_words") else "", stamp(res["sample"]))


def stock_text(row):
    if row["place"] != "fleet" and not row["place_rows"]:
        return "%s (not read)" % num(row["stock"] or 0)
    return num(row["stock"] or 0)


def change_text(row):
    if row["change_24h"] is None:
        return "--"
    return "{:+,}".format(row["change_24h"]) + ("" if row["change_hours"] == 24 else " /%dh" % row["change_hours"])


def show(res):
    print(first_line("SUPPLY | the goods the fleet must never run out of, broken and short first", res))
    if res["error"]:
        print("  " + res["error"])
        return 1
    if not res["rows"]:
        print("  no chains: %s holds none (or is not there)" % NAME)
        return 0
    print("  %-7s %-22s %-18s %-24s %16s %11s %8s %13s  %-30s %-9s" % ("status", "chain", "item", "place", "stock", "keep", "need/h", "24 h", "sources: ships now, in plans", "keeper"))
    for r in res["rows"]:
        need = "%g" % r["need_per_hour"] if r["need_per_hour"] else "--"
        listed = r["sources_listed"] or 0
        sources = "%d: %d ships, %d in plans" % (listed, r["ships"] or 0, r["sources_planned"] or 0) if listed else "none"
        if listed and (r["sources_known"] or 0) < listed:
            sources += " (%d no file)" % (listed - (r["sources_known"] or 0))
        print("  %-7s %-22s %-18s %-24s %16s %11s %8s %13s  %-30s %-9s" % (r["status"], (r["chain"] or "line %d" % r["line"])[:22], (r["item"] or "?")[:18],
                                                                       (r["place"] or "?")[:24], stock_text(r), num(r["keep"]) if r["keep"] is not None else "?",
                                                                       need, change_text(r), sources, r["keeper"] or "?"))
        if r["error"]:
            print("          line %d: %s" % (r["line"], r["error"]))
    count = {status: sum(1 for r in res["rows"] if r["status"] == status) for status in ORDER}
    print("SUM | %d chains: %d short, %d low, %d ok, %d broken | %d ships on the sources of the short chains now" % (
        len(res["rows"]), count["short"], count["low"], count["ok"], count["broken"], sum(r["ships"] or 0 for r in res["rows"] if r["status"] == "short")))
    print(RULE)
    return 0


def faults(res):
    """[(kind, text)] of the gate: SHORT, BROKEN and ERROR lines."""
    out = []
    if res["file"] is not None and res["file"][1]:
        out.append(("ERROR", "%s is not read now: %s (its rows are as last read)" % (NAME, res["file"][1])))
    for r in res["rows"]:
        name = r["chain"] or "line %d" % r["line"]
        if r["status"] == "broken":
            out.append(("BROKEN", "line %d (%s): %s" % (r["line"], name, r["error"] or "no keep")))
            continue
        if r["status"] == "short":
            read_note = " (no reading of the place: the storage book holds nothing there)" if r["place"] != "fleet" and not r["place_rows"] else ""
            ships = "%d sources (%d in a plan), %d ships on them now" % (r["sources_listed"], r["sources_planned"] or 0, r["ships"] or 0) if r["sources_listed"] else \
                "no source route: %s writes one" % r["keeper"]
            out.append(("SHORT", "%s: %s at %s: %s of %s%s | %s | keeper %s" % (name, r["item"], r["place"], num(r["stock"] or 0), num(r["keep"]), read_note, ships, r["keeper"])))
        if res["items"] and r["item"] not in res["items"]:
            out.append(("ERROR", "%s: item %s is not in the catalog (table items)" % (name, r["item"])))
        if r["place"] != "fleet" and res["places"] and r["place"] not in res["places"]:
            out.append(("ERROR", "%s: place `%s` is no base, place or system of our readings" % (name, r["place"])))
        for rid in sources_of(r):
            if rid not in res["routes"]:
                out.append(("ERROR", "%s: source %s has no route file (game/routes/%s.json)" % (name, rid, rid)))
    return out


def level_faults(rows, root):
    """[("ERROR", text)] of the chains at `fleet` whose keep differs from the `min` line of game/reserve.tsv for their
    item: one good, one figure (requests ENT-355: the chain iron-ore short at 166,923 while the reserve called the
    same iron full, and the miners' plan followed one of them). No reserve file or no min line: nothing to compare."""
    mins = {}
    try:
        text = (Path(root) / "reserve.tsv").read_text(encoding="ascii")
    except (OSError, UnicodeDecodeError):
        return []
    for line in text.split("\n"):
        cells = [c.strip() for c in line.split("\t")]
        if len(cells) >= 3 and cells[0] == "min" and cells[2].isdigit():
            mins[cells[1]] = int(cells[2])
    out = []
    for r in rows:
        low = mins.get(r.get("item"))
        if r.get("place") == "fleet" and low is not None and isinstance(r.get("keep"), int) and r["keep"] != low:
            out.append(("ERROR", "%s: keep %s differs from game/reserve.tsv `min %s %s`: one figure for one good (set both alike)"
                        % (r.get("chain"), num(r["keep"]), r.get("item"), num(low))))
    return out


def check(res, root=None):
    print(first_line("CHECK %s" % NAME, res))
    if res["error"]:
        print("  " + res["error"])
        print("HALT: the chains cannot be read")
        return 1
    found = faults(res) + (level_faults(res["rows"], root) if root else [])
    for kind, text in found:
        print("  %s %s" % (kind, text))
    count = {kind: sum(1 for k, _t in found if k == kind) for kind in ("SHORT", "BROKEN", "ERROR")}
    if found:
        print("HALT: %d chains short, %d rows broken, %d errors (of %d chains)" % (count["SHORT"], count["BROKEN"], count["ERROR"], len(res["rows"])))
        return 1
    print("PASS: %d chains, every one at its keep or above" % len(res["rows"]))
    return 0


# ---- duty: the sources of short chains into their keepers' plans, each with its end

def load_record(data):
    try:
        found = json.loads((Path(data) / RECORD).read_text(encoding="ascii"))
    except (OSError, ValueError):
        return {}
    routes = found.get("routes") if isinstance(found, dict) else None
    return {key: entry for key, entry in (routes or {}).items() if isinstance(entry, dict) and entry.get("route") and entry.get("division")}


def save_record(data, record, now):
    path = Path(data) / RECORD
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(".%s.%d.tmp" % (path.name, os.getpid()))
    tmp.write_text(json.dumps({"written_at": stamp(now), "what": "the routes supply.py duty put into the list Then of a division's plan, each with its "
                                                               "chain and its end", "routes": record}, indent=1, sort_keys=True) + "\n", encoding="ascii")
    os.replace(tmp, path)


def epoch(text):
    """Seconds of a UTC stamp; 0 (long past) for anything else, so an entry without a readable end is due."""
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0


def gatherers(root, item, place="fleet"):
    """The route files that bring an item, by their own fields: a mine route whose floor (min_left) names it, a stop that
    crafts it (craft.makes) or buys it; for a place, also a stop there that stores it. Switched-off routes are left out."""
    out = []
    for path in sorted((Path(root) / "routes").glob("*.json")):
        try:
            route = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(route, dict) or route.get("status") == "off":
            continue
        brings = route.get("kind") == "mine" and item in (route.get("min_left") or {})
        for stop in route.get("stops") or []:
            if not isinstance(stop, dict):
                continue
            brings = brings or any(isinstance(c, dict) and c.get("makes") == item for c in stop.get("craft") or [])
            brings = brings or any(isinstance(b, dict) and b.get("item") == item for b in stop.get("buy") or [])
            stored = stop.get("store")
            if place != "fleet" and place in str(stop.get("at") or "").split(":") and isinstance(stored, list) and item in stored:
                brings = True
        if brings:
            out.append(path.stem)
    return out


def not_own(name, route, rid):
    """Why a route is not the own work of every role of division `name` (rule F23, workclass.own), or None."""
    if route is None:
        return None                                   # no route file read: judged by the lines that name it
    roles = roles_of(name)
    other = [role for role in roles if not workclass.own(role, route, rid)]
    if not other and roles:
        return None
    import pull                                   # the words of the dispatcher's class reason
    return "%s work, the %s' (rule F23)" % (workclass.work_class(route, rid), pull.role_words(workclass.roles_for(route, rid)))


def steps(res, record, now, root=None):
    """What duty would change: {lines: [text], divisions: {division: {add: [(route, chain)], end: [(key, route, why)]}}, renew: [key],
    hints}. Only short chains with sources add; every route of the record whose end came or whose chain no longer asks for it ends.
    With `root` (the game/ folder) the route files are read: a source that is not the keeper division's own class is
    never added, and a route of the record that is not ends (rule F23)."""
    by_chain = {r["chain"]: r for r in res["rows"] if r["chain"]}
    plans, lines, divisions, renew = res["plans"], [], {}, []
    files = workclass.load(root) if root else {}
    for r in res["rows"]:
        if r["status"] != "short":
            continue
        name = (r["keeper"] or "").lower()
        roles = roles_of(name)
        head = "%s (%s: %s at %s, %s of %s)" % (r["chain"], r["keeper"], r["item"], r["place"], num(r["stock"] or 0), num(r["keep"]))
        if not res.get("whole", True):            # r22: a book that is not whole reads less than the fleet holds: short is not measured
            lines.append("%s: not judged, the storage book is not whole (the first line): no source goes in until it is" % head)
            continue
        if not sources_of(r):
            found = gatherers(root, r["item"], r["place"]) if root else []
            lines.append("%s: no source route: %s writes one%s" % (head, r["keeper"], "; route files that bring %s: %s" % (r["item"], ", ".join(found)) if found
                                                                   else "; no route file brings %s" % r["item"]))
            continue
        held = set().union(*[plans.get(role, set()) for role in roles]) if roles else set()
        have = [rid for rid in sources_of(r) if rid in held]
        unknown = [rid for rid in sources_of(r) if rid not in res["routes"]]
        off = [rid for rid in sources_of(r) if rid in res["routes"] and res["routes"][rid][1] == "off"]
        missing = [rid for rid in sources_of(r) if rid not in held and rid not in unknown and rid not in off]
        foreign = [(rid, not_own(name, files.get(rid), rid)) for rid in missing]
        foreign = [(rid, why) for rid, why in foreign if why]
        missing = [rid for rid in missing if rid not in dict(foreign)]
        lines.append("%s: the %s plan (roles %s) holds %d of its %d sources%s" % (head, name, ", ".join(roles) or "none", len(have), len(sources_of(r)),
                                                                              ": " + ", ".join(have) if have else ""))
        if unknown:
            lines.append("  no route file, not added: %s" % ", ".join(unknown))
        if off:
            lines.append("  switched off (status off), not added: %s" % ", ".join(off))
        for rid, why in foreign:
            lines.append("  not the %s plan's class of work, not added: %s (%s)" % (name, rid, why))
        if missing:
            lines.append("  ADD %s -> the list Then of the %s plan, in front of its census and park routes (standing work for every ship of the "
                         "division; plan.put_then + plan.apply, as fill.py add), ending %s unless the chain is still short then"
                         % (", ".join(missing), name, stamp(now + DUTY_HOURS * 3600)))
            divisions.setdefault(name, {"add": [], "end": []})["add"] += [(rid, r["chain"]) for rid in missing]
    for key, entry in sorted(record.items()):
        row = by_chain.get(entry.get("chain"))
        due = epoch(entry.get("until")) <= now
        broken = row is not None and row["status"] == "broken"            # a row with a typo ends nothing before its end
        foreign = not_own(entry["division"], files.get(entry["route"]), entry["route"])
        why = ("it is %s, not the %s division's" % (foreign, entry["division"]) if foreign else
               "its chain %s is gone from the file" % entry.get("chain") if row is None else
               "its chain is ok" if row["status"] == "ok" else
               "its chain is kept by %s now" % row["keeper"] if not broken and (row["keeper"] or "").lower() != entry["division"] else
               "its chain no longer names it" if not broken and entry["route"] not in sources_of(row) else
               "its end %s came and its chain is %s" % (entry.get("until"), row["status"]) if due and row["status"] != "short" else "")
        if why:
            lines.append("END %s: out of the list Then of the %s plan: %s" % (entry["route"], entry["division"], why))
            divisions.setdefault(entry["division"], {"add": [], "end": []})["end"].append((key, entry["route"], why))
        elif due and not res.get("whole", True):  # r22: renewed only on a whole book; ended above as before
            lines.append("HOLD %s in the %s plan: its end came while the storage book is not whole: judged when it is" % (entry["route"], entry["division"]))
        elif due:
            lines.append("RENEW %s in the %s plan: its chain %s is still short; new end %s" % (entry["route"], entry["division"], entry["chain"],
                                                                                          stamp(now + DUTY_HOURS * 3600)))
            renew.append(key)
    return {"lines": lines, "divisions": divisions, "renew": renew}


def write(root, data, plan_steps, record, who, now):
    """Make the change of every division through plan.apply and keep what was put in, with its end: (True when every division
    went through, lines)."""
    import dispatch                               # the route files, as plan.put_then reads them
    import plan as planfile                       # each division's plan file: put_then, apply (it commits through fill.commit)
    routes, lines, good = dispatch.load_routes(root), [], True
    for key in plan_steps["renew"]:
        record[key]["until"] = stamp(now + DUTY_HOURS * 3600)
    for name, step in sorted(plan_steps["divisions"].items()):
        if who != "Unity" and planfile.DIVISIONS.get(name) != who:
            lines.append("REFUSED %s: the %s plan is kept by %s (orders F1); nothing changed there" % (name, name, planfile.DIVISIONS.get(name)))
            good = False
            continue
        added, ended = [], []

        def change(plan, step=step, added=added, ended=ended):
            present = set(plan["first"]) | set(plan["then"]) | {rid for ship in plan["ships"] for rid in planfile.expand(plan, ship)}
            for rid, chain in step["add"]:
                if rid not in present and rid not in [r for r, _c in added]:
                    planfile.put_then(plan, rid, routes)
                    added.append((rid, chain))
            for key, rid, _why in step["end"]:
                plan["then"] = [r for r in plan["then"] if r != rid]
                ended.append(key)
        chains = sorted({chain for _rid, chain in step["add"]})
        message = "plans: supply.py duty, %s plan: %s%s" % (name, "+" + ", +".join(rid for rid, _c in step["add"]) if step["add"] else "",
                                                           ("; -" + ", -".join(rid for _k, rid, _w in step["end"])) if step["end"] else "")
        message += " (short: %s)" % ", ".join(chains) if chains else ""
        ok, out = planfile.apply(root, data, [name], who, changes={name: change}, message=message[:400])
        lines += out
        if not ok:
            good = False
            continue
        for rid, chain in added:
            record["%s/%s" % (name, rid)] = {"division": name, "route": rid, "chain": chain, "added": stamp(now), "until": stamp(now + DUTY_HOURS * 3600), "by": who}
        for key in ended:
            record.pop(key, None)
        lines.append("%s: %d routes put in (%s), %d taken out" % (name, len(added), ", ".join(rid for rid, _c in added) or "none new: the live plan holds them", len(ended)))
    save_record(data, record, now)
    return good, lines


def duty(res, root, data, writing, now=None):
    now = time.time() if now is None else now
    print(first_line("DUTY | the sources of short chains in the plans of their keepers", res))
    if res["error"]:
        print("  " + res["error"])
        return 1
    record = load_record(data)
    plan_steps = steps(res, record, now, root)
    for line in plan_steps["lines"] or ["no chain is short and no route of %s/%s is due" % (Path(data).name, RECORD)]:
        print("  " + line)
    adds = sum(len(step["add"]) for step in plan_steps["divisions"].values())
    ends = sum(len(step["end"]) for step in plan_steps["divisions"].values())
    print("SUM | %d routes to put into %d plans, %d to take out, %d ends to renew | %s" % (
        adds, sum(1 for step in plan_steps["divisions"].values() if step["add"]), ends, len(plan_steps["renew"]),
        "written below" if writing and DUTY_ENABLED else "a dry run: nothing written"))
    if not writing:
        return 0
    if not DUTY_ENABLED:
        print("REFUSED: DUTY_ENABLED is False in game/fleet/supply.py: duty changes no plan until Unity has read this dry run on live data and switched it on")
        return 1
    if (Path(data) / STOP).exists():
        print("REFUSED: %s exists: nothing is changed while the fleet is halted" % STOP)
        return 1
    kind, who = division.member()
    if kind != "member":
        print("REFUSED: this shell is no member of The Collective: it changes no plan")
        return 1
    if who == "Unity":
        try:
            import needs as needbook
            _rc, nlines = needbook.reconcile(Path(root).resolve().parent, data, who, False, now=now)
            for nl in nlines:
                print("  NEEDS auto-closed: " + nl)
        except Exception:
            pass
    if not plan_steps["divisions"] and not plan_steps["renew"]:
        print("nothing to write")
        return 0
    try:
        import routes_hygiene
        routes_hygiene.run_hygiene(root, write=True, commit=True, now=now)
    except Exception:
        pass
    good, lines = write(root, data, plan_steps, record, who, now)
    for line in lines:
        print(line)
    return 0 if good else 1


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data"))]
    if any(a in ("-h", "--help") for a in args) or (words and words[0] not in ("show", "check", "duty")):
        print(__doc__)
        return 1
    verb = words[0] if words else "show"
    res = read(data)
    if verb == "check":
        return check(res, root)
    if verb == "duty":
        return duty(res, root, data, "--write" in args and "--dry-run" not in args)
    return show(res)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
