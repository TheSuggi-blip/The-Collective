#!/usr/bin/env python3
"""store.py -- keeps the fleet's history and its current state in one SQLite file: the runs, the price moves and the census readings with their sums by hour and by day, the members' own observations, and beside them what the fleet's own files say now.

WHAT: the service `store` runs it. Every minute it reads the new whole lines of the records of the
      unit's data folder and writes them into <data>/store/live.db:
        routes/runs.jsonl       -> runs      one row a run           sums: route_hour  (runs, minutes, credits)
        market/history.jsonl    -> moves     one row a price move    sums: market_hour (lowest and highest bid, ask)
        wildlife/history.jsonl  -> readings  one row a field or herd sums: reading_day (first and last count)
        observations/<division>.jsonl -> observations  one row an observation a member wrote with observe.py (six
                                records, one per division: command, mining, trade, logistics, military, intel); no sums
      In the same pass it loads the snapshot tables: what a file says NOW (state, not history), from
        fleet/fleet.json, fleet/ships/*.json, fleet/orders/*.json  -> ships, ship_skills, ship_modules, ship_cargo
        stock/storage.json                                          -> holdings (views inventory, inventory_by_station)
        market/<base>.json, market/ladders.json                     -> books, ladders
        catalog/<newest version>.json                               -> items, recipes, recipe_inputs, recipe_outputs,
                                                                       recipe_facilities, facilities, facility_materials,
                                                                       hulls, hull_materials, skills
        scouting/<system>.json, wildlife/<system>.json              -> places, fields, herds
        missions/<base>.json, intel/met.json                        -> missions, met
        station/map.json (else game/map/galaxy.tsv)                 -> systems, lanes (view fleet_positions)
        station/stations.json, station/feed.json (its factions)     -> stations, factions
        empire/empire.json                                          -> faction, faction_members, bases, faction_facilities,
                                                                       territory, sites (view our_stations)
        game/routes/*.json, game/routes/plans/<role>.json (the
        repository's game/ folder, --root)                          -> routes, plan_routes
      After a pass that wrote, and at least every five minutes, it publishes a copy, <data>/store/read.db,
      which every other program reads; the first pass of a UTC day also writes
      <data>/store/backup/collective-<date>.db (the five newest stay). `hive.py sql` and `hive.py schema`
      ask the copy through query() and schema().
RULES:
  - This service is the only writer of live.db; no other program opens that file. Two containers share
    the data folder, and file locks, appends and live SQLite files do not work between them (services
    README, "Data"). Readers open the copy through connect(): read-only and immutable.
  - One writer at a time: <data>/store/writer.lease, created with O_EXCL and renewed every pass. `once`
    is refused while a serve holds a lease renewed in the last five minutes.
  - A pass reads each record from where the last pass stopped (table cursor) and writes its rows, its
    sums and its new place in one transaction. A last line without its newline waits for the next pass.
  - A record shorter than its place, or whose first line changed, was cut by the keeper
    (scripts/data-keeper.py): it is read again from its start. Every row has a key and goes in with
    INSERT OR IGNORE, so a line read twice is one row: a run by (pilot, route, started), a price move by
    (base, item, t), a reading by (system, poi, what, t), an observation by (division, kind, subject, t, digest: the first
    16 hex of the sha256 of its line, so two observations of one subject in one second are two rows and the same line
    read again is one). An observation counts only in its own division's record and by that division's member
    (observe.py's rule, checked again here: the files can be written from any shell); a record not there is skipped.
  - Sums are recomputed from the raw rows, only for the hours (days) that got new rows. Raw rows older
    than --keep-days are deleted by whole hours (readings by whole days); their sums stay, and a line of
    such an hour that turns up again is not taken in: those sums are final. Observations have no sums: they are kept
    KEEP_TABLES days (30), or --keep-days when that is longer, cut and sealed by whole days.
  - A run counts for credits and read minutes only when it read a wallet (credits_before and
    credits_after above 0, no note `wallet not read`); its credits are its steady credits: what the run
    earned by the fleet's one rule (routes.py, earned: a hunt's sale of goods it carried in is left out)
    minus one_time. Credits per ship-hour = 60 * credits / read minutes. hive.py counts the same way.
  - A herd its place's census no longer lists stands at 0 in that census (once). A bid or ask of 0 is no
    price: it is left out of the lowest and highest of its hour, and stands as NULL in the table books.
  - A bad line is skipped and counted; a failed pass is printed and tried again at the next tick.
  - Snapshot tables: the table `source` remembers every file they were read from (size, mtime, when
    loaded, rows, note). A file is read again only when its size or mtime changed; its rows (column
    `src`: the file a row came from) are deleted and written anew inside the pass's one snapshot
    transaction. A bad or missing file is skipped: its rows stay as last read, `source.note` says why, the
    pass's line names it once, and the other files go on. A file of a folder that is gone takes its rows
    with it; a missing file of a fixed name keeps them. A fault of the snapshot never stops the history.
  - One function per quantity: who commands a pilot and its role are division.py's (owner, role_of), the
    order a ship flies is division.order_of (an order not touched for division.ORDER_FRESH is none: a
    pilot whose order aged is read again without a file change), a route's group is routes.py's stage. The
    views inventory and inventory_by_station add up the storage book as craftbook.py inventory does (its
    totals per station and the holds per member; worth = units x base value); a test holds the two equal.
  - The snapshot tables are derived: when their definition in this file changes, they are dropped and
    loaded anew from the files at the next pass.
  - query() reads the read copy only: exactly one statement that begins with SELECT or WITH, under
    `PRAGMA query_only` and an authorizer that allows reading and nothing else; a statement that runs
    longer than its seconds is stopped; at most `limit` rows come back, and a cut is said.
WHY:  the keeper cuts the records to their newest lines, so what a route earned last week was lost, and
      every reader parsed megabytes of JSON again for each answer. Here the history stays as sums, and the
      fleet's state is one SQL question away for every Admiral, without a parser of its own.

From another program (the module's functions):
  conn = store.connect(data)            the read copy, or None while there is none
  store.route_rates(conn, since_epoch)  {route: (runs, read minutes, credits, one_time, credits per ship-hour or None)}
  store.query(data, sql, limit, seconds)  {columns, rows, cut, error}: one read-only statement on the read copy
  store.schema(conn)                    {table or view: {kind, description, columns, examples}}

USAGE:
  store.py serve [--every 60]     run forever (the service `store`)
  store.py once                   one pass, then stop
  store.py recount                ask the writer to count every raw run kept again by the fleet's one rule
                                  (routes.earned) and to sum its hours again: after a record that rule reads
                                  was mended (the tax record, the wallet guard's gifts)
  store.py status                 from the read copy: rows and newest row of each table, age of the copy, the
                                  snapshot tables with the age of their newest source, the files not read
  --data <dir>                    the unit's data folder (default /srv/collective/data)
  --root <dir>                    the repository's game/ folder (default: the parent of this file's folder)
  --keep-days N                   days of raw rows kept (default 7; observations at least 30: KEEP_TABLES)

Stdlib only. ASCII only.
"""

import argparse
import calendar
import hashlib
import json
import os
import re
import signal
import sqlite3
import sys
import time
import urllib.parse
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names (fleet_positions)
import division                                   # noqa: E402  who commands a pilot, its role, the order it flies
import routes as routefiles                       # noqa: E402  what a run earned, a route's group: one rule for the store and for hive.py

EVERY = 60                     # seconds between two passes
KEEP_DAYS = 7                  # days of raw rows kept; the sums stay for good
PUBLISH = 300                  # seconds: the read copy is renewed at least this often
BACKUPS = 5                    # daily backups kept
LEASE_FRESH = 300              # seconds: a writer lease renewed this recently belongs to a living writer
HEAD = 65536                   # bytes of a record's first line that mark it (a cut changes its first line)
HOUR, DAY = 3600, 86400
ROOT = Path(__file__).resolve().parent.parent      # the repository's game/ folder, as routes.py and hive.py take it (--root)

SCHEMA = """
CREATE TABLE IF NOT EXISTS cursor (record TEXT PRIMARY KEY, offset INTEGER NOT NULL, head TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value);
CREATE TABLE IF NOT EXISTS runs (pilot TEXT NOT NULL, route TEXT NOT NULL, kind TEXT, started TEXT NOT NULL,
  t INTEGER NOT NULL, minutes REAL, credits REAL, one_time REAL, readable INTEGER, row TEXT,
  PRIMARY KEY (pilot, route, started));
CREATE INDEX IF NOT EXISTS runs_route ON runs (route, t);
CREATE INDEX IF NOT EXISTS runs_t ON runs (t);
CREATE TABLE IF NOT EXISTS moves (base TEXT NOT NULL, item TEXT NOT NULL, t INTEGER NOT NULL,
  bid REAL, bid_qty REAL, ask REAL, ask_qty REAL, PRIMARY KEY (base, item, t));
CREATE INDEX IF NOT EXISTS moves_t ON moves (t);
CREATE TABLE IF NOT EXISTS readings (system TEXT NOT NULL, poi TEXT NOT NULL, what TEXT NOT NULL, kind TEXT,
  amount REAL, t INTEGER NOT NULL, PRIMARY KEY (system, poi, what, t));
CREATE INDEX IF NOT EXISTS readings_place ON readings (system, poi, kind, t);
CREATE INDEX IF NOT EXISTS readings_t ON readings (t);
CREATE TABLE IF NOT EXISTS route_hour (route TEXT NOT NULL, hour INTEGER NOT NULL, runs INTEGER, minutes REAL,
  read_minutes REAL, credits REAL, one_time REAL, PRIMARY KEY (route, hour));
CREATE TABLE IF NOT EXISTS market_hour (base TEXT NOT NULL, item TEXT NOT NULL, hour INTEGER NOT NULL,
  bid_lo REAL, bid_hi REAL, ask_lo REAL, ask_hi REAL, moves INTEGER, PRIMARY KEY (base, item, hour));
CREATE TABLE IF NOT EXISTS reading_day (system TEXT NOT NULL, poi TEXT NOT NULL, what TEXT NOT NULL, kind TEXT,
  day INTEGER NOT NULL, first REAL, last REAL, t_first INTEGER, t_last INTEGER, PRIMARY KEY (system, poi, what, day));
CREATE TABLE IF NOT EXISTS observations (division TEXT NOT NULL, member TEXT NOT NULL, kind TEXT NOT NULL, subject TEXT NOT NULL,
  t INTEGER NOT NULL, at TEXT NOT NULL, fields TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', digest TEXT NOT NULL,
  PRIMARY KEY (division, kind, subject, t, digest));
CREATE INDEX IF NOT EXISTS observations_kind ON observations (kind, t);
CREATE INDEX IF NOT EXISTS observations_subject ON observations (subject);
"""
NEWEST = (("runs", "t"), ("moves", "t"), ("readings", "t"), ("route_hour", "hour"), ("market_hour", "hour"), ("reading_day", "day"),
          ("observations", "t"))


def stamp(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def epoch(text):
    """Seconds of a UTC stamp 'YYYY-MM-DDTHH:MM:SSZ'; ValueError for anything else."""
    if not isinstance(text, str) or len(text) < 19:
        raise ValueError("no time stamp")
    return calendar.timegm(time.strptime(text[:19], "%Y-%m-%dT%H:%M:%S"))


def number(value):
    """An int or float as it is; None for anything else (a bool is no number)."""
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def text_of(row, key):
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError("no %s" % key)
    return value


def readable(row):
    """True when the run read a wallet at both ends (game/fleet/routes.py, readable)."""
    before, after = number(row.get("credits_before")), number(row.get("credits_after"))
    notes = row.get("notes") if isinstance(row.get("notes"), list) else []
    return before is not None and after is not None and before > 0 and after > 0 and "wallet not read" not in notes


def earned(row):
    """What the run earned, by the rule every figure of the fleet uses (routes.py, earned); its plain delta when the
    row's goods cannot be read."""
    try:
        return number(routefiles.earned(row)) or 0
    except (TypeError, ValueError, KeyError, IndexError, AttributeError):
        return number(row.get("delta")) or 0


# ---- one line of each record -> raw rows; each returns (rows added, the sums it touched), None for a sealed hour

def take_run(conn, row, sealed, line):
    pilot, route, started = text_of(row, "pilot"), text_of(row, "route"), text_of(row, "started")
    t = epoch(started)
    if t < sealed:
        return None
    one_time = number(row.get("one_time")) or 0
    credits = earned(row) - one_time
    kind = row.get("kind") if isinstance(row.get("kind"), str) else None
    added = conn.execute("INSERT OR IGNORE INTO runs VALUES (?,?,?,?,?,?,?,?,?,?)", (
        pilot, route, kind, started, t, number(row.get("minutes")) or 0, credits, one_time,
        1 if readable(row) else 0, line)).rowcount
    return added, {(route, t - t % HOUR)} if added else set()


def take_move(conn, row, sealed, line):
    base, item = text_of(row, "base"), text_of(row, "item")
    t = epoch(row.get("t"))
    if t < sealed:
        return None
    added = conn.execute("INSERT OR IGNORE INTO moves VALUES (?,?,?,?,?,?,?)", (
        base, item, t, number(row.get("bid")), number(row.get("bid_qty")), number(row.get("ask")),
        number(row.get("ask_qty")))).rowcount
    return added, {(base, item, t - t % HOUR)} if added else set()


GONE = ("SELECT what FROM readings WHERE system = ? AND poi = ? AND kind = 'herd' AND amount > 0 AND t = "
        "(SELECT MAX(t) FROM readings WHERE system = ? AND poi = ? AND kind = 'herd' AND t < ?)")


def take_census(conn, row, sealed, line):
    system = text_of(row, "system")
    t = epoch(row.get("at"))
    deposits, herds = row.get("deposits"), row.get("herds")
    if not isinstance(deposits, dict) and not isinstance(herds, dict):
        raise ValueError("no deposits and no herds")
    if t < sealed:
        return None
    rows = []
    for kind, group in (("field", deposits), ("herd", herds)):
        for poi, counts in (group.items() if isinstance(group, dict) else ()):
            if not isinstance(counts, dict):
                continue
            poi = str(poi)
            for what, amount in counts.items():
                if number(amount) is not None:
                    rows.append((system, poi, str(what), kind, number(amount), t))
            if kind == "herd":                     # a herd the last census of this place counted and this one does not list
                for (what,) in conn.execute(GONE, (system, poi, system, poi, t)).fetchall():
                    if what not in counts:
                        rows.append((system, poi, what, "herd", 0, t))
    added, keys = 0, set()
    for one in rows:
        if conn.execute("INSERT OR IGNORE INTO readings VALUES (?,?,?,?,?,?)", one).rowcount:
            added += 1
            keys.add((one[0], one[1], one[2], t - t % DAY))
    return added, keys


EARNED_RULE = "3"                 # the rule of what a run earned (routes.earned); a new mark has the raw runs kept counted again


def recount(conn):
    """Count every raw run kept again by the fleet's one rule (earned) and sum its hours again: after the rule changed
    (EARNED_RULE), or when asked (`store.py recount`) after a record the rule reads was mended (the tax record, the
    wallet guard's gifts). The runs whose credits moved."""
    keys, moved = set(), 0
    conn.execute("BEGIN IMMEDIATE")
    try:
        for pilot, route, started, t, one_time, credits, line in conn.execute("SELECT pilot, route, started, t, one_time, credits, row FROM runs").fetchall():
            try:
                parsed = json.loads(line)
            except (TypeError, ValueError):
                continue
            if not isinstance(parsed, dict):
                continue
            new = earned(parsed) - (one_time or 0)
            if new != credits:
                conn.execute("UPDATE runs SET credits = ? WHERE pilot = ? AND route = ? AND started = ?", (new, pilot, route, started))
                keys.add((route, t - t % HOUR))
                moved += 1
        sum_routes(conn, keys)
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('earned.rule', ?)", (EARNED_RULE,))
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return moved


# ---- sums, recomputed from the raw rows of one hour (day)

def sum_routes(conn, keys):
    for route, hour in keys:
        conn.execute(
            "INSERT OR REPLACE INTO route_hour SELECT route, ?, COUNT(*), SUM(minutes), "
            "SUM(CASE WHEN readable = 1 THEN minutes ELSE 0 END), SUM(CASE WHEN readable = 1 THEN credits ELSE 0 END), "
            "SUM(CASE WHEN readable = 1 THEN one_time ELSE 0 END) FROM runs WHERE route = ? AND t >= ? AND t < ? GROUP BY route",
            (hour, route, hour, hour + HOUR))


def sum_market(conn, keys):
    for base, item, hour in keys:
        conn.execute(
            "INSERT OR REPLACE INTO market_hour SELECT base, item, ?, MIN(CASE WHEN bid > 0 THEN bid END), "
            "MAX(CASE WHEN bid > 0 THEN bid END), MIN(CASE WHEN ask > 0 THEN ask END), MAX(CASE WHEN ask > 0 THEN ask END), "
            "COUNT(*) FROM moves WHERE base = ? AND item = ? AND t >= ? AND t < ? GROUP BY base, item",
            (hour, base, item, hour, hour + HOUR))


def sum_readings(conn, keys):
    for system, poi, what, day in keys:
        rows = conn.execute("SELECT kind, amount, t FROM readings WHERE system = ? AND poi = ? AND what = ? AND t >= ? AND t < ? "
                            "ORDER BY t", (system, poi, what, day, day + DAY)).fetchall()
        if rows:
            conn.execute("INSERT OR REPLACE INTO reading_day VALUES (?,?,?,?,?,?,?,?,?)",
                         (system, poi, what, rows[-1][0], day, rows[0][1], rows[-1][1], rows[0][2], rows[-1][2]))


def sum_none(conn, keys):
    """Observations have no sums: each row stays as it was written, for KEEP_TABLES days."""


OBSERVED = tuple(board.NAMES[member].lower() for member in division.MEMBERS)   # observe.py's six records, one per division
KEEP_TABLES = {"observations": 30}         # days a table's raw rows stay at least, beyond --keep-days: no sums keep what a member saw


def take_observation(name):
    """The reader of observations/<name>.jsonl (observe.py): one row an observation, keyed by (division, kind, subject, t,
    digest of its line). A line of another division, of another member than the division's own, or whose fields are not
    key: number, true/false or text, is bad."""
    owner = next(member for member in division.MEMBERS if board.NAMES[member].lower() == name)

    def take(conn, row, sealed, line):
        member, kind, subject = text_of(row, "member"), text_of(row, "kind"), text_of(row, "subject")
        if row.get("division") != name or member != owner:      # the file is writable from any shell: the rule is read again here
            raise ValueError("an observation of %s by %s in the record of %s" % (row.get("division"), member, name))
        fields, note = row.get("fields", {}), row.get("note", "")
        if not isinstance(fields, dict) or not isinstance(note, str) or not all(isinstance(v, (int, float, str)) for v in fields.values()):
            raise ValueError("fields or note not as observe.py writes them")
        t = epoch(row.get("t"))
        if t < sealed:
            return None
        digest = hashlib.sha256(line.encode("utf-8")).hexdigest()[:16]
        added = conn.execute("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?,?,?,?,?)", (
            name, member, kind, subject, t, stamp(t), json.dumps(fields, sort_keys=True, allow_nan=False), note, digest)).rowcount
        return added, set()
    return take


RECORDS = (                    # record, its raw table, a line -> rows, the sums, the seal's step
    ("routes/runs.jsonl", "runs", take_run, sum_routes, HOUR),
    ("market/history.jsonl", "moves", take_move, sum_market, HOUR),
    ("wildlife/history.jsonl", "readings", take_census, sum_readings, DAY),
) + tuple(("observations/%s.jsonl" % name, "observations", take_observation(name), sum_none, DAY) for name in OBSERVED)


# ---- the snapshot tables: what the fleet's files say now (state, not history)

# A snapshot table: its name, its columns, its key. Each also carries `src` (the file its row came from), by which a
# file's rows are replaced; `source` keeps the files themselves.
SNAPSHOT = (
    ("ships", "pilot TEXT, member TEXT, division TEXT, role TEXT, number INTEGER, class TEXT, empire TEXT, status TEXT, activity TEXT, "
              "system TEXT, poi TEXT, docked INTEGER, base TEXT, in_transit INTEGER, hull INTEGER, max_hull INTEGER, shield INTEGER, "
              "max_shield INTEGER, fuel INTEGER, max_fuel INTEGER, cargo_used INTEGER, cargo_capacity INTEGER, credits INTEGER, flies TEXT, "
              "t INTEGER", "pilot"),
    ("ship_skills", "pilot TEXT, skill TEXT, level INTEGER, xp INTEGER", "pilot, skill"),
    ("ship_modules", "pilot TEXT, module TEXT, name TEXT, slot TEXT, kind TEXT", ""),
    ("ship_cargo", "pilot TEXT, item TEXT, units INTEGER", ""),
    ("holdings", "pilot TEXT, member TEXT, place TEXT, item TEXT, units INTEGER, t INTEGER", ""),
    ("books", "base TEXT, system TEXT, item TEXT, name TEXT, category TEXT, bid INTEGER, bid_qty INTEGER, ask INTEGER, ask_qty INTEGER, "
              "bid_depth INTEGER, ask_depth INTEGER, t INTEGER", "base, item"),
    ("ladders", "base TEXT, item TEXT, side TEXT, step INTEGER, price INTEGER, qty INTEGER, t INTEGER", "base, item, side, step"),
    ("items", "id TEXT, name TEXT, category TEXT, size INTEGER, base_value INTEGER, rarity TEXT, tradeable INTEGER, stackable INTEGER, "
              "type TEXT, slot TEXT, extracted_by TEXT, description TEXT", "id"),
    ("recipes", "id TEXT, name TEXT, category TEXT, hand INTEGER, facility_only INTEGER, time REAL, fuel_output INTEGER, "
                "requires_unlock INTEGER, description TEXT", "id"),
    ("recipe_inputs", "recipe TEXT, item TEXT, units INTEGER", ""),
    ("recipe_outputs", "recipe TEXT, item TEXT, units INTEGER", ""),
    ("recipe_facilities", "recipe TEXT, facility TEXT", ""),
    ("facilities", "id TEXT, name TEXT, category TEXT, level INTEGER, build_cost INTEGER, build_time INTEGER, labor_cost INTEGER, upgrades_from TEXT, "
                   "recipe TEXT, service_type TEXT, requires_service_type TEXT, faction_service_type TEXT, personal_service_type TEXT, "
                   "faction_cap INTEGER, power_draw INTEGER, power_supply INTEGER, empire TEXT, player_buildable INTEGER, description TEXT", "id"),
    ("facility_materials", "facility TEXT, item TEXT, units INTEGER", ""),
    ("hulls", "id TEXT, name TEXT, class TEXT, tier INTEGER, category TEXT, faction TEXT, shipyard_tier INTEGER, piloting_required INTEGER, "
              "cargo INTEGER, hull INTEGER, shield INTEGER, armor INTEGER, speed INTEGER, fuel INTEGER, cpu INTEGER, power INTEGER, weapon_slots INTEGER, "
              "defense_slots INTEGER, utility_slots INTEGER, build_time INTEGER, description TEXT", "id"),
    ("hull_materials", "hull TEXT, item TEXT, units INTEGER", ""),
    ("skills", "id TEXT, name TEXT, category TEXT, max_level INTEGER, training TEXT, empire TEXT, description TEXT", "id"),
    ("places", "system TEXT, poi TEXT, kind TEXT, name TEXT, class TEXT, base TEXT, x REAL, y REAL, t INTEGER", "system, poi"),
    ("fields", "system TEXT, poi TEXT, resource TEXT, remaining INTEGER, max_remaining INTEGER, richness INTEGER, t INTEGER", ""),
    ("herds", "system TEXT, poi TEXT, creature TEXT, name TEXT, role TEXT, count INTEGER, t INTEGER", ""),
    ("systems", "id TEXT, name TEXT, x REAL, y REAL, empire TEXT, home INTEGER, stronghold INTEGER, jumps INTEGER", "id"),
    ("lanes", "a TEXT, b TEXT", ""),
    ("stations", "name TEXT, kind TEXT, system TEXT, tag TEXT, faction TEXT, empire TEXT, condition TEXT, services TEXT, wrecked INTEGER, "
                 "mobile INTEGER", ""),
    ("factions", "tag TEXT, name TEXT, members INTEGER, leader TEXT, allies TEXT, enemies TEXT, wars TEXT", "tag"),
    ("faction", "id TEXT, name TEXT, tag TEXT, leader TEXT, member_count INTEGER, members_limit INTEGER, treasury INTEGER, owned_bases INTEGER, "
                "at_war INTEGER, created INTEGER, t INTEGER", ""),
    ("faction_members", "pilot TEXT, role TEXT, t INTEGER", ""),
    ("bases", "base TEXT, name TEXT, system TEXT, poi TEXT, kind TEXT, t INTEGER", ""),
    ("faction_facilities", "id TEXT, type TEXT, name TEXT, level INTEGER, base TEXT, system TEXT, status TEXT, rent_per_cycle INTEGER, t INTEGER", ""),
    ("territory", "system TEXT, claim TEXT, note TEXT, t INTEGER", ""),
    ("sites", "system TEXT, poi TEXT, status TEXT, note TEXT, t INTEGER", ""),
    ("missions", "base TEXT, system TEXT, id TEXT, template TEXT, title TEXT, kind TEXT, difficulty INTEGER, reward INTEGER, reward_items TEXT, "
                 "reward_xp INTEGER, expires_ticks INTEGER, giver TEXT, objectives TEXT, t INTEGER", ""),
    ("met", "name TEXT, faction TEXT, class TEXT, system TEXT, poi TEXT, first INTEGER, t INTEGER, times INTEGER, in_combat INTEGER", "name"),
    ("routes", "id TEXT, kind TEXT, grp TEXT, title TEXT, place TEXT, station TEXT, status TEXT, max_ships INTEGER, once INTEGER, cph INTEGER, "
               "credits_per_run INTEGER, runs INTEGER, minutes REAL, measured TEXT", "id"),
    ("plan_routes", "role TEXT, n INTEGER, route TEXT, ships INTEGER", "role, n"),
)
COLUMNS = {name: [part.split()[0] for part in columns.split(", ")] for name, columns, _key in SNAPSHOT}
LOOKUPS = (("ships", "system"), ("holdings", "item"), ("books", "item"), ("ladders", "item"), ("recipe_inputs", "item"),
           ("recipe_outputs", "item"), ("facility_materials", "item"), ("fields", "resource"), ("herds", "creature"), ("lanes", "a"),
           ("stations", "system"), ("missions", "base"))


def views():
    """The views over the snapshot tables. fleet_positions counts per division by its Admiral (division.owner) and names the
    column after the division (board.NAMES), in the order of division.MEMBERS."""
    per = ", ".join("SUM(s.member = '%s') AS %s" % (member, board.NAMES.get(member, member).lower()) for member in division.MEMBERS)
    return (
        "CREATE VIEW IF NOT EXISTS inventory AS SELECT h.item AS item, i.name AS name, i.category AS category, SUM(h.units) AS units, "
        "SUM(CASE WHEN h.place <> 'hold' THEN h.units ELSE 0 END) AS in_storage, SUM(CASE WHEN h.place = 'hold' THEN h.units ELSE 0 END) AS in_holds, "
        "i.base_value AS base_value, SUM(h.units) * i.base_value AS worth FROM holdings h LEFT JOIN items i ON i.id = h.item GROUP BY h.item;\n"
        "CREATE VIEW IF NOT EXISTS inventory_by_station AS SELECT h.place AS place, h.item AS item, i.name AS name, i.category AS category, "
        "SUM(h.units) AS units FROM holdings h LEFT JOIN items i ON i.id = h.item GROUP BY h.place, h.item;\n"
        "CREATE VIEW IF NOT EXISTS fleet_positions AS SELECT s.system AS system, y.name AS name, y.empire AS empire, y.jumps AS jumps, "
        "COUNT(*) AS ships, SUM(COALESCE(s.docked, 0) = 1) AS docked, SUM(COALESCE(s.docked, 0) = 0) AS flying, %s "
        "FROM ships s LEFT JOIN systems y ON y.id = s.system GROUP BY s.system;\n"
        "CREATE VIEW IF NOT EXISTS our_stations AS SELECT st.name AS name, st.kind AS kind, st.system AS system, st.tag AS tag, "
        "st.faction AS faction, st.condition AS condition, st.services AS services, st.wrecked AS wrecked, st.mobile AS mobile, b.base AS base, "
        "b.poi AS poi, b.kind AS base_kind FROM stations st JOIN faction f ON st.tag = f.tag "
        "LEFT JOIN bases b ON b.system = st.system AND b.name = st.name;\n" % per) + EARNINGS


def window(hours, column):
    """The SQL of one column of route_earnings summed over the hours of the last `hours` hours (0: every hour kept)."""
    return "SUM(r.%s)" % column if not hours else "SUM(CASE WHEN r.hour >= strftime('%%s', 'now') - %d THEN r.%s END)" % (hours * HOUR, column)


# What a route earns NOW is a question of the window: a bid that left three hours ago still stands in a day's sum. One row
# per route that ever flew: its steady credits per ship-hour over the last 4, 12 and 24 hours and over all hours kept, the
# runs behind each, and the hours since it last flew (a figure nobody refreshed is old, not bad).
EARNINGS = ("CREATE VIEW IF NOT EXISTS route_earnings AS SELECT r.route AS route, x.kind AS kind, x.grp AS grp, "
            "datetime(MAX(r.hour), 'unixepoch') AS last_hour, CAST((strftime('%s', 'now') - MAX(r.hour)) / 3600 AS INTEGER) AS hours_since, "
            + ", ".join("COALESCE(%s, 0) AS runs_%s, ROUND(60.0 * %s / NULLIF(%s, 0)) AS cph_%s" % (window(h, "runs"), name, window(h, "credits"), window(h, "read_minutes"), name)
                        for h, name in ((4, "4h"), (12, "12h"), (24, "24h"), (0, "all")))
            + ", ROUND(SUM(r.one_time)) AS paid_once FROM route_hour r LEFT JOIN routes x ON x.id = r.route GROUP BY r.route;\n")
VIEWS = ("inventory", "inventory_by_station", "fleet_positions", "our_stations", "route_earnings")


def snapshot_schema():
    """The SQL that makes the table `source`, the snapshot tables, their indexes and the views."""
    out = ["CREATE TABLE IF NOT EXISTS source (name TEXT PRIMARY KEY, loader TEXT NOT NULL, size INTEGER, mtime REAL, t INTEGER, "
           "rows INTEGER NOT NULL DEFAULT 0, note TEXT NOT NULL DEFAULT '');"]
    for name, columns, key in SNAPSHOT:
        out.append("CREATE TABLE IF NOT EXISTS %s (%s, src TEXT NOT NULL%s);" % (name, columns, ", PRIMARY KEY (%s)" % key if key else ""))
        out.append("CREATE INDEX IF NOT EXISTS %s_src ON %s (src);" % (name, name))
    out += ["CREATE INDEX IF NOT EXISTS %s_%s ON %s (%s);" % (table, column, table, column) for table, column in LOOKUPS]
    return "\n".join(out) + "\n" + views()


def setup_snapshot(conn):
    """Make the snapshot tables; drop and make them again when their definition changed (they are derived from the files)."""
    text = snapshot_schema()
    version = hashlib.sha256(text.encode("ascii")).hexdigest()[:16]
    if meta(conn, "snapshot.schema", "") == version:
        return
    try:
        old = json.loads(meta(conn, "snapshot.tables", "{}"))
    except ValueError:
        old = {}
    old = old if isinstance(old, dict) else {}
    for view in set(old.get("views") or []) | set(VIEWS):
        conn.execute("DROP VIEW IF EXISTS %s" % view)
    for table in set(old.get("tables") or []) | {name for name, _c, _k in SNAPSHOT} | {"source"}:
        conn.execute("DROP TABLE IF EXISTS %s" % table)
    conn.executescript(text)
    made = {"tables": ["source"] + [name for name, _c, _k in SNAPSHOT], "views": list(VIEWS)}
    conn.execute("INSERT OR REPLACE INTO meta VALUES ('snapshot.tables', ?)", (json.dumps(made),))
    conn.execute("INSERT OR REPLACE INTO meta VALUES ('snapshot.schema', ?)", (version,))


# ---- reading one file: each reader returns {table: [rows as dicts]}; ValueError and its kin mark the file bad

def load_json(path):
    with open(path, "rb") as handle:
        return json.loads(handle.read().decode("utf-8"))


def when(value, default=None):
    """Integer epoch of a UTC stamp ('2026-11-16T18:00:00Z', '2026-11-16 18:00:00') or of a number; default otherwise."""
    if number(value) is not None:
        return int(value)
    try:
        return epoch(str(value).replace(" ", "T"))
    except ValueError:
        return default


def flag(value):
    """1 or 0 for a truth value, None when the file says nothing."""
    return None if value is None else (1 if value else 0)


def words(values):
    """A list as comma text without the empty entries; None for no list."""
    return ",".join(str(v) for v in values if v not in (None, "")) if isinstance(values, list) else None


def text(value):
    return value if isinstance(value, str) and value != "" else None


def mtime_of(path):
    return int(os.stat(path).st_mtime)


def need(found, kind, what):
    if not isinstance(found, kind):
        raise ValueError(what)
    return found


def read_fleet(path, ctx):
    """fleet/fleet.json -> ships: one row per ship the collector lists; its member and role by division.py, the order it
    flies by division.order_of (fleet/orders/<pilot>.json while a runner touches it)."""
    fleet = need(load_json(path), dict, "not a fleet file: no object")
    data, now, read = ctx["data"], ctx["now"], when(fleet.get("updated_at"), mtime_of(path))
    rows = []
    for ship in need(fleet.get("ships"), list, "no list `ships`"):
        if not isinstance(ship, dict) or not text(ship.get("name")):
            continue
        name, docked = ship["name"], ship.get("docked")
        act = ship.get("activity") if isinstance(ship.get("activity"), dict) else {}
        rows.append({"pilot": name, "member": division.owner(name, data), "division": text(ship.get("division")), "role": division.role_of(name, data) or None,
                     "number": number(ship.get("number")), "class": text(ship.get("class")), "empire": text(ship.get("empire")), "status": text(ship.get("status")),
                     "activity": " ".join(str(v) for v in (act.get("kind"), act.get("type")) if v) or None, "system": text(ship.get("system")),
                     "poi": text(ship.get("poi")), "docked": 1 if docked else 0, "base": text(docked), "in_transit": flag(ship.get("in_transit")),
                     "hull": number(ship.get("hull")), "max_hull": number(ship.get("max_hull")), "shield": number(ship.get("shield")),
                     "max_shield": number(ship.get("max_shield")), "fuel": number(ship.get("fuel")), "max_fuel": number(ship.get("max_fuel")),
                     "cargo_used": number(ship.get("cargo_used")), "cargo_capacity": number(ship.get("cargo_capacity")), "credits": number(ship.get("credits")),
                     "flies": division.order_of(name, data, now) or None, "t": when(ship.get("state_at"), read)})
    return {"ships": rows}


def read_ship(path, ctx):
    """fleet/ships/<pilot>.json -> ship_skills, ship_modules, ship_cargo of one pilot."""
    ship = need(load_json(path), dict, "not a ship file: no object")
    pilot = need(text(ship.get("name")), str, "no `name`")
    skills = ship.get("skills") if isinstance(ship.get("skills"), dict) else {}
    out = {"ship_skills": [{"pilot": pilot, "skill": skill, "level": number(entry.get("level")), "xp": number(entry.get("xp"))}
                           for skill, entry in skills.items() if isinstance(entry, dict)],
           "ship_modules": [{"pilot": pilot, "module": text(m.get("type") or m.get("type_id")), "name": text(m.get("name")), "slot": text(m.get("slot")),
                             "kind": text(m.get("kind"))} for m in ship.get("modules") or [] if isinstance(m, dict)],
           "ship_cargo": []}
    for row in ship.get("cargo") or []:
        item = (row.get("item") or row.get("item_id")) if isinstance(row, dict) else None      # the ship files write `item`, the engine `item_id` (ledger.py)
        if item:
            out["ship_cargo"].append({"pilot": pilot, "item": str(item), "units": number(row.get("quantity"))})
    return out


def read_storage(path, ctx):
    """stock/storage.json (the ledger's storage book) -> holdings: per pilot, station and item; and the holds as the book sums
    them, per member (place `hold`, no pilot: the book does not say which ship carries what)."""
    book = need(load_json(path), dict, "not a storage book: no object")
    data, read = ctx["data"], when(book.get("updated_at"), mtime_of(path))
    rows = []
    for pilot, entry in need(book.get("pilots"), dict, "no `pilots`").items():
        if not isinstance(entry, dict):
            continue
        member, at = division.owner(pilot, data), when(entry.get("read_at"), read)
        for base, goods in (entry.get("stations") or {}).items() if isinstance(entry.get("stations"), dict) else []:
            for item, units in (goods or {}).items() if isinstance(goods, dict) else []:
                rows.append({"pilot": pilot, "member": member, "place": base, "item": item, "units": number(units), "t": at})
    holds = (book.get("totals") or {}).get("holds_by_member") if isinstance(book.get("totals"), dict) else None
    for member, goods in (holds or {}).items() if isinstance(holds, dict) else []:
        for item, units in (goods or {}).items() if isinstance(goods, dict) else []:
            rows.append({"pilot": None, "member": member, "place": "hold", "item": item, "units": number(units), "t": read})
    return {"holdings": rows}


def price(value):
    """A price of 0 is no price (the history's rule): None."""
    value = number(value)
    return value if value else None


def read_book(path, ctx):
    """market/<base>.json -> books: the station's best bid and ask per item when our ship read it."""
    book = need(load_json(path), dict, "not an order book: no object")
    items = need(book.get("items"), list, "not an order book: no list `items`")
    base, read = text(book.get("base")) or Path(path).stem, when(book.get("read_at"), mtime_of(path))
    return {"books": [{"base": base, "system": text(book.get("system")), "item": row["item_id"], "name": text(row.get("item_name")),
                       "category": text(row.get("category")), "bid": price(row.get("best_buy")), "bid_qty": number(row.get("best_buy_qty")),
                       "ask": price(row.get("best_sell")), "ask_qty": number(row.get("best_sell_qty")), "bid_depth": number(row.get("buy_quantity")),
                       "ask_depth": number(row.get("sell_quantity")), "t": read}
                      for row in items if isinstance(row, dict) and text(row.get("item_id"))]}


def read_ladders(path, ctx):
    """market/ladders.json -> ladders: {base: {item: {bids: [[price, units]...], asks: [...], t}}}, step 1 the best."""
    found = need(load_json(path), dict, "no object")
    rows, read = [], mtime_of(path)
    for base, items in found.items():
        for item, entry in (items or {}).items() if isinstance(items, dict) else []:
            if not isinstance(entry, dict):
                continue
            for side, key in (("bid", "bids"), ("ask", "asks")):
                for step, pair in enumerate(entry.get(key) or [], 1):
                    if isinstance(pair, list) and len(pair) >= 2:
                        rows.append({"base": base, "item": item, "side": side, "step": step, "price": number(pair[0]), "qty": number(pair[1]),
                                     "t": when(entry.get("t"), read)})
    return {"ladders": rows}


def pairs(recipe_or_build, key, owner, units="units"):
    return [{owner[0]: owner[1], "item": text(m.get("item_id")), units: number(m.get("quantity"))}
            for m in recipe_or_build.get(key) or [] if isinstance(m, dict) and text(m.get("item_id"))]


def read_catalog(path, ctx):
    """catalog/<version>.json (the game's catalog) -> items, recipes and their inputs, outputs and facilities, facilities and
    their materials, hulls (the catalog's `ships`) and their materials, skills. An item without a category keeps NULL."""
    cat = need(load_json(path), dict, "not a catalog: no object")
    need(cat.get("items"), list, "not a catalog: no list `items`")
    rows = {name: [] for name in ("items", "recipes", "recipe_inputs", "recipe_outputs", "recipe_facilities", "facilities",
                                  "facility_materials", "hulls", "hull_materials", "skills")}
    listed = lambda key: [r for r in cat.get(key) or [] if isinstance(r, dict) and text(r.get("id"))]
    for i in listed("items"):
        rows["items"].append({"id": i["id"], "name": text(i.get("name")), "category": text(i.get("category")), "size": number(i.get("size")),
                              "base_value": number(i.get("base_value")), "rarity": text(i.get("rarity")), "tradeable": flag(i.get("tradeable")),
                              "stackable": flag(i.get("stackable")), "type": text(i.get("type")), "slot": text(i.get("slot")),
                              "extracted_by": text(i.get("extracted_by")), "description": text(i.get("description"))})
    for r in listed("recipes"):
        rows["recipes"].append({"id": r["id"], "name": text(r.get("name")), "category": text(r.get("category")), "hand": flag(r.get("hand_craftable")),
                                "facility_only": flag(r.get("facility_only")), "time": number(r.get("crafting_time")), "fuel_output": number(r.get("fuel_output")),
                                "requires_unlock": flag(r.get("requires_unlock")), "description": text(r.get("description"))})
        rows["recipe_inputs"] += pairs(r, "inputs", ("recipe", r["id"]))
        rows["recipe_outputs"] += pairs(r, "outputs", ("recipe", r["id"]))
        rows["recipe_facilities"] += [{"recipe": r["id"], "facility": str(f)} for f in r.get("produced_by_facility_ids") or [] if f]
    for f in listed("facilities"):
        rows["facilities"].append({"id": f["id"], "name": text(f.get("name")), "category": text(f.get("category")), "level": number(f.get("level")),
                                   "build_cost": number(f.get("build_cost")), "build_time": number(f.get("build_time")), "labor_cost": number(f.get("labor_cost")),
                                   "upgrades_from": text(f.get("upgrades_from")), "recipe": text(f.get("recipe_id")), "service_type": text(f.get("service_type")),
                                   "requires_service_type": text(f.get("requires_service_type")), "faction_service_type": text(f.get("faction_service_type")),
                                   "personal_service_type": text(f.get("personal_service_type")), "faction_cap": number(f.get("faction_cap")),
                                   "power_draw": number(f.get("power_draw")), "power_supply": number(f.get("power_supply")), "empire": text(f.get("empire")),
                                   "player_buildable": flag(f.get("player_station_buildable")), "description": text(f.get("description"))})
        rows["facility_materials"] += pairs(f, "build_materials", ("facility", f["id"]))
    for s in listed("ships"):
        rows["hulls"].append({"id": s["id"], "name": text(s.get("name")), "class": text(s.get("class")), "tier": number(s.get("tier")),
                              "category": text(s.get("category")), "faction": text(s.get("faction")), "shipyard_tier": number(s.get("shipyard_tier")),
                              "piloting_required": number(s.get("piloting_required")), "cargo": number(s.get("cargo_capacity")), "hull": number(s.get("base_hull")),
                              "shield": number(s.get("base_shield")), "armor": number(s.get("base_armor")), "speed": number(s.get("base_speed")),
                              "fuel": number(s.get("base_fuel")), "cpu": number(s.get("cpu_capacity")), "power": number(s.get("power_capacity")),
                              "weapon_slots": number(s.get("weapon_slots")), "defense_slots": number(s.get("defense_slots")),
                              "utility_slots": number(s.get("utility_slots")), "build_time": number(s.get("build_time")), "description": text(s.get("description"))})
        rows["hull_materials"] += pairs(s, "build_materials", ("hull", s["id"]))
    for k in listed("skills"):
        rows["skills"].append({"id": k["id"], "name": text(k.get("name")), "category": text(k.get("category")), "max_level": number(k.get("max_level")),
                               "training": text(k.get("training_source")), "empire": text(k.get("empire_restriction")), "description": text(k.get("description"))})
    return rows


def read_scouting(path, ctx):
    """scouting/<system>.json (a census) -> places (every place of the system's chart, the visited ones too) and fields
    (what is left of each resource)."""
    scan = need(load_json(path), dict, "not a census: no object")
    info = scan.get("system") if isinstance(scan.get("system"), dict) else {}
    system, read = text(info.get("id")) or Path(path).stem, when(scan.get("read_at"), mtime_of(path))
    places, fields = {}, []
    for p in info.get("pois") or [] if isinstance(info.get("pois"), list) else []:
        if isinstance(p, dict) and text(p.get("id")):
            spot = p.get("position") if isinstance(p.get("position"), dict) else {}
            places[p["id"]] = {"system": system, "poi": p["id"], "kind": text(p.get("type")), "name": text(p.get("name")), "class": text(p.get("class")),
                               "base": text(p.get("base_id")) if p.get("has_base") or p.get("base_id") else None, "x": number(spot.get("x")),
                               "y": number(spot.get("y")), "t": read}
    for poi, entry in need(scan.get("pois") or {}, dict, "`pois` is no object").items():
        if not isinstance(entry, dict):
            continue
        inner = entry.get("poi") if isinstance(entry.get("poi"), dict) else {}
        base = entry.get("base") if isinstance(entry.get("base"), dict) else {}
        spot = inner.get("position") if isinstance(inner.get("position"), dict) else {}
        row = places.setdefault(poi, {"system": system, "poi": poi, "kind": text(inner.get("type")), "name": text(inner.get("name")),
                                      "class": text(inner.get("class")), "base": None, "x": number(spot.get("x")), "y": number(spot.get("y")), "t": read})
        row["base"] = row["base"] or text(base.get("id")) or text(inner.get("base_id"))
        for res in entry.get("resources") or [] if isinstance(entry.get("resources"), list) else []:
            if isinstance(res, dict) and text(res.get("resource_id")):
                fields.append({"system": system, "poi": poi, "resource": res["resource_id"], "remaining": number(res.get("remaining")),
                               "max_remaining": number(res.get("max_remaining")), "richness": number(res.get("richness")), "t": read})
    return {"places": list(places.values()), "fields": fields}


def read_wildlife(path, ctx):
    """wildlife/<system>.json -> herds: the creatures counted at each place, by species."""
    wild = need(load_json(path), dict, "not a wildlife census: no object")
    system, read = text(wild.get("system")) or Path(path).stem, when(wild.get("read_at"), mtime_of(path))
    rows = {}
    for poi, entry in need(wild.get("pois") or {}, dict, "`pois` is no object").items():
        for c in entry.get("creatures") or [] if isinstance(entry, dict) else []:
            if isinstance(c, dict) and text(c.get("species")):
                row = rows.setdefault((poi, c["species"]), {"system": system, "poi": poi, "creature": c["species"], "name": text(c.get("name")),
                                                            "role": text(c.get("role")), "count": 0, "t": when(entry.get("read_at"), read)})
                row["count"] += 1
    return {"herds": list(rows.values())}


def read_missions(path, ctx):
    """missions/<base>.json -> missions on offer at a station when our ship read its board."""
    board_ = need(load_json(path), dict, "not a mission board: no object")
    base, read = text(board_.get("base")) or Path(path).stem, when(board_.get("read_at"), mtime_of(path))
    rows = []
    for m in need(board_.get("missions"), list, "no list `missions`"):
        if not isinstance(m, dict):
            continue
        reward = m.get("rewards") if isinstance(m.get("rewards"), dict) else {}
        goods = reward.get("items") if isinstance(reward.get("items"), dict) else {}
        goals = [str(o.get("description") or o.get("type")) for o in m.get("objectives") or [] if isinstance(o, dict)]
        giver = m.get("giver") if isinstance(m.get("giver"), dict) else {}
        rows.append({"base": base, "system": text(board_.get("system")), "id": text(m.get("mission_id")) or text(m.get("id")), "template": text(m.get("template_id")),
                     "title": text(m.get("title")), "kind": text(m.get("type")), "difficulty": number(m.get("difficulty")), "reward": number(reward.get("credits")),
                     "reward_items": ",".join("%s %s" % (units, item) for item, units in sorted(goods.items())) or None,
                     "reward_xp": number(reward.get("piloting_xp")), "expires_ticks": number(m.get("expires_in_ticks")), "giver": text(giver.get("name")),
                     "objectives": "; ".join(goals) or None, "t": read})
    return {"missions": rows}


def read_met(path, ctx):
    """intel/met.json -> met: the pilots of other players our ships met, with where and when last seen."""
    found = need(load_json(path), dict, "no object")
    found = found["pilots"] if isinstance(found.get("pilots"), dict) else found
    return {"met": [{"name": name, "faction": text(e.get("faction_tag")), "class": text(e.get("ship_class")), "system": text(e.get("system")),
                     "poi": text(e.get("poi")), "first": when(e.get("first")), "t": when(e.get("last")), "times": number(e.get("times")),
                     "in_combat": when(e.get("in_combat_at"))} for name, e in found.items() if isinstance(e, dict)]}


def read_route(path, ctx):
    """game/routes/<id>.json -> routes: one route file with its group (routes.py stage) and what its runs measured."""
    route = need(routefiles.read_json(path), dict, "not a route file: no object")
    measured = route.get("measured") if isinstance(route.get("measured"), dict) else {}
    return {"routes": [{"id": Path(path).stem, "kind": text(route.get("kind")), "grp": routefiles.stage(route), "title": text(route.get("title")),
                        "place": text(route.get("belt") or route.get("place")), "station": text(route.get("station") or route.get("sell_at")),
                        "status": text(route.get("status")), "max_ships": number(route.get("max_ships")), "once": flag(route.get("once")),
                        "cph": number(measured.get("cph_per_ship")), "credits_per_run": number(measured.get("credits_per_run")),
                        "runs": number(measured.get("runs")), "minutes": number(measured.get("minutes")), "measured": text(measured.get("date"))}]}


def read_plan(path, ctx):
    """game/routes/plans/<role>.json -> plan_routes: the role's routes in their order and the ships the plan puts on each."""
    plan = need(routefiles.read_json(path), dict, "not a plan file: no object")
    ships = plan.get("ships") if isinstance(plan.get("ships"), dict) else {}
    role = text(plan.get("role")) or Path(path).stem
    return {"plan_routes": [{"role": role, "n": n, "route": str(rid), "ships": number(ships.get(rid))}
                            for n, rid in enumerate(need(plan.get("routes"), list, "no list `routes`"), 1)]}


def lawless(empire):
    """An empire's id; None for lawless space ('' in the station's map, '-' on the chart)."""
    return None if empire in (None, "", "-") else str(empire)


def read_map(path, ctx):
    """station/map.json -> systems and lanes: {systems: [{id, name, x, y, empire, home, stronghold, lanes, jumps}]}."""
    found = need(load_json(path), dict, "not a map: no object")
    systems, lanes = [], []
    for s in need(found.get("systems"), list, "no list `systems`"):
        if isinstance(s, dict) and text(s.get("id")):
            systems.append({"id": s["id"], "name": text(s.get("name")), "x": number(s.get("x")), "y": number(s.get("y")), "empire": lawless(s.get("empire")),
                            "home": flag(s.get("home")), "stronghold": flag(s.get("stronghold")), "jumps": number(s.get("jumps"))})
            lanes += [{"a": s["id"], "b": str(b)} for b in s.get("lanes") or [] if b]
    return {"systems": systems, "lanes": lanes}


def read_chart(path, ctx):
    """game/map/galaxy.tsv (the repository's chart, scripts/map.py) -> systems and lanes, when station/map.json is missing."""
    systems, lanes, cols = [], [], {}
    with open(path, encoding="ascii", errors="replace") as handle:
        for line in handle:
            cells = line.rstrip("\n").split("\t")
            if not cells[0] or cells[0].startswith("#"):
                continue
            if cells[0] == "id":
                cols = {name: n for n, name in enumerate(cells)}
                continue
            if not cols:
                raise ValueError("no header line `id ...`")
            cell = lambda name: cells[cols[name]] if name in cols and cols[name] < len(cells) else ""
            flags = set(cell("flags").split(","))
            jumps = cell("jumps_from_home")
            systems.append({"id": cells[0], "name": cell("name") or None, "x": float(cell("x")) if cell("x") else None,
                            "y": float(cell("y")) if cell("y") else None, "empire": lawless(cell("empire")), "home": 1 if "home" in flags else 0,
                            "stronghold": 1 if "stronghold" in flags else 0, "jumps": int(jumps) if jumps.isdigit() else None})
            lanes += [{"a": cells[0], "b": b} for b in cell("lanes").split(",") if b and b != "-"]
    return {"systems": systems, "lanes": lanes}


def read_stations(path, ctx):
    """station/stations.json -> stations: every station and outpost of the galaxy, its owner's faction tag in `tag`."""
    found = load_json(path)
    found = found.get("stations") if isinstance(found, dict) else found
    return {"stations": [{"name": text(s.get("name")), "kind": text(s.get("type")), "system": text(s.get("system")), "tag": text(s.get("tag")),
                          "faction": text(s.get("faction")), "empire": lawless(s.get("empire")), "condition": text(s.get("condition")),
                          "services": words(s.get("services")), "wrecked": flag(s.get("wrecked")), "mobile": flag(s.get("mobile"))}
                         for s in need(found, list, "no list of stations") if isinstance(s, dict)]}


def read_factions(path, ctx):
    """station/feed.json -> factions (its `players` are not loaded)."""
    found = need(load_json(path), dict, "no object")
    return {"factions": [{"tag": tag, "name": text(f.get("name")), "members": number(f.get("members")), "leader": text(f.get("leader")),
                          "allies": words(f.get("allies")), "enemies": words(f.get("enemies")), "wars": words(f.get("wars"))}
                         for tag, f in need(found.get("factions"), dict, "no object `factions`").items() if isinstance(f, dict)]}


def read_empire(path, ctx):
    """empire/empire.json (our faction, its members, bases, facilities, territory and sites) -> faction, faction_members, bases,
    faction_facilities, territory, sites. Keys it does not know are left out; a list that is missing is an empty table."""
    found = need(load_json(path), dict, "no object")
    read = when(found.get("written_at"), mtime_of(path))
    listed = lambda key: [r for r in found.get(key) or [] if isinstance(r, dict)] if isinstance(found.get(key), list) else []
    own = found.get("faction") if isinstance(found.get("faction"), dict) else {}
    out = {"faction": [{"id": text(own.get("id")), "name": text(own.get("name")), "tag": text(own.get("tag")), "leader": text(own.get("leader")),
                        "member_count": number(own.get("member_count")), "members_limit": number(own.get("members_limit")), "treasury": number(own.get("treasury")),
                        "owned_bases": number(own.get("owned_bases")), "at_war": flag(own.get("at_war")), "created": when(own.get("created_at")), "t": read}] if own else []}
    out["faction_members"] = [{"pilot": text(m.get("pilot")), "role": text(m.get("role")), "t": read} for m in listed("members")]
    out["bases"] = [{"base": text(b.get("base")), "name": text(b.get("name")), "system": text(b.get("system")), "poi": text(b.get("poi")),
                     "kind": text(b.get("kind")), "t": read} for b in listed("bases")]
    out["faction_facilities"] = [{"id": text(f.get("facility_id")), "type": text(f.get("type")), "name": text(f.get("name")), "level": number(f.get("level")),
                                  "base": text(f.get("base")), "system": text(f.get("system")), "status": text(f.get("status")),
                                  "rent_per_cycle": number(f.get("rent_per_cycle")), "t": read} for f in listed("facilities")]
    out["territory"] = [{"system": text(r.get("system")), "claim": text(r.get("claim")), "note": text(r.get("note")), "t": read} for r in listed("territory")]
    out["sites"] = [{"system": text(r.get("system")), "poi": text(r.get("poi")), "status": text(r.get("status")), "note": text(r.get("note")), "t": read}
                    for r in listed("sites")]
    return out


# ---- which files feed which tables

def data_files(folder, reader, skip=()):
    """A folder's *.json of the data folder: [(source name, path, reader, required, note when missing)], none required."""
    def files(data, root):
        base = Path(data) / folder
        return [("%s/%s" % (folder, p.name), p, reader, False, "") for p in sorted(base.glob("*.json")) if p.name not in skip] if base.is_dir() else []
    return files


def data_file(name, reader, missing="missing"):
    """One file of a fixed name in the data folder: required (a missing one is named and its rows stay)."""
    return lambda data, root: [(name, Path(data) / name, reader, True, missing)]


def repo_files(folder, reader, skip=()):
    def files(data, root):
        base = Path(root) / folder
        return [("game/%s/%s" % (folder, p.name), p, reader, False, "") for p in sorted(base.glob("*.json")) if p.name not in skip] if base.is_dir() else []
    return files


def catalog_files(data, root):
    """The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog."""
    found = [p for p in (Path(data) / "catalog").glob("*.json") if re.fullmatch(r"\d+(\.\d+)*", p.stem)] if (Path(data) / "catalog").is_dir() else []
    if not found:
        return [("catalog/<version>.json", Path(data) / "catalog" / "none.json", read_catalog, True, "missing: no catalog/<version>.json")]
    newest = max(found, key=lambda p: tuple(int(n) for n in p.stem.split(".")))
    return [("catalog/%s" % newest.name, newest, read_catalog, True, "missing")]


def map_files(data, root):
    """station/map.json; while it is missing, the repository's chart game/map/galaxy.tsv stands in."""
    main = Path(data) / "station" / "map.json"
    if main.is_file():
        return [("station/map.json", main, read_map, True, "missing")]
    return [("station/map.json", main, read_map, True, "missing: the chart game/map/galaxy.tsv stands in"),
            ("game/map/galaxy.tsv", Path(root) / "map" / "galaxy.tsv", read_chart, True, "missing")]


LOADERS = (    # loader, the tables it fills, its files, whole (one file holds all rows: a new reading replaces them all)
    ("ships", ("ship_skills", "ship_modules", "ship_cargo"), data_files("fleet/ships", read_ship), False),
    ("holdings", ("holdings",), data_file("stock/storage.json", read_storage), True),
    ("books", ("books",), data_files("market", read_book, skip=("ladders.json", "history.state.json")), False),
    ("ladders", ("ladders",), data_file("market/ladders.json", read_ladders), True),
    ("catalog", ("items", "recipes", "recipe_inputs", "recipe_outputs", "recipe_facilities", "facilities", "facility_materials", "hulls",
                 "hull_materials", "skills"), catalog_files, True),
    ("scouting", ("places", "fields"), data_files("scouting", read_scouting), False),
    ("wildlife", ("herds",), data_files("wildlife", read_wildlife), False),
    ("missions", ("missions",), data_files("missions", read_missions), False),
    ("met", ("met",), data_file("intel/met.json", read_met), True),
    ("map", ("systems", "lanes"), map_files, True),
    ("stations", ("stations",), data_file("station/stations.json", read_stations), True),
    ("factions", ("factions",), data_file("station/feed.json", read_factions), True),
    ("empire", ("faction", "faction_members", "bases", "faction_facilities", "territory", "sites"),
     data_file("empire/empire.json", read_empire, "missing: our empire's collector has not written it yet"), True),
    ("routes", ("routes",), repo_files("routes", read_route, skip=("plan.json",)), False),
    ("plans", ("plan_routes",), repo_files("routes/plans", read_plan), False),
)
FED = dict([(table, ("fleet", "orders")) for table in ("ships",)] + [(table, (loader,)) for loader, tables, _f, _w in LOADERS for table in tables])
BAD = (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError, RecursionError)


# ---- the snapshot pass

def cell(value):
    """A value SQLite takes: a truth value as 1 or 0, a list or an object as its JSON text."""
    if isinstance(value, bool):
        return int(value)
    if value is None or isinstance(value, (int, float, str)):
        return value
    return json.dumps(value, sort_keys=True)


def stat_of(path):
    try:
        found = os.stat(path)
    except OSError:
        return None
    return (found.st_size, found.st_mtime) if os.path.isfile(path) else None


def fill(conn, tables, rows, src, whole):
    """Replace a file's rows: delete what came from it (every row of the tables, for a loader whose one file holds them all),
    then write the new rows. The number of rows written."""
    for table in tables:
        if whole:
            conn.execute("DELETE FROM %s" % table)
        else:
            conn.execute("DELETE FROM %s WHERE src = ?" % table, (src,))
    count = 0
    for table in tables:
        columns = COLUMNS[table]
        found = [tuple(cell(r.get(c)) for c in columns) + (src,) for r in rows.get(table) or []]
        conn.executemany("INSERT OR REPLACE INTO %s (%s, src) VALUES (%s)" % (table, ", ".join(columns), ", ".join("?" * (len(columns) + 1))), found)
        count += len(found)
    return count


class Pass:
    """One snapshot pass: the files known from the last pass, and what this pass did (loaded, problems named, files gone)."""

    def __init__(self, conn, data, root, now):
        self.conn, self.data, self.root, self.now = conn, data, root, now
        self.known = {row[0]: row for row in conn.execute("SELECT name, loader, size, mtime, t, rows, note FROM source")}
        self.out = {"loaded": Counter(), "rows": 0, "problems": [], "gone": 0, "flies": 0}

    def changed(self, name, found):
        old = self.known.get(name)
        return old is None or found is None or (old[2], old[3]) != found

    def keep(self, name, loader, found, t, rows, note):
        self.conn.execute("INSERT OR REPLACE INTO source VALUES (?,?,?,?,?,?,?)",
                          (name, loader, found[0] if found else None, found[1] if found else None, t, rows, note))

    def problem(self, name, loader, found, note):
        """A bad or missing file: its rows stay as last read; named in the pass's line when its note is new."""
        old = self.known.get(name)
        self.keep(name, loader, found, old[4] if old else None, old[5] if old else 0, note)
        if not old or old[6] != note:
            self.out["problems"].append((name, note))

    def load(self, loader, tables, name, path, reader, whole):
        """Read one file and replace its rows; True when it was loaded."""
        found = stat_of(path)
        try:
            rows = reader(path, {"data": self.data, "root": self.root, "now": self.now})
        except BAD as error:
            self.problem(name, loader, found, "bad: %s: %s" % (type(error).__name__, str(error).splitlines()[0][:160] if str(error) else ""))
            return False
        count = fill(self.conn, tables, rows, name, whole)
        self.keep(name, loader, found, int(self.now), count, "")
        self.out["loaded"][loader] += 1
        self.out["rows"] += count
        return True

    def forget(self, name, tables):
        for table in tables:
            self.conn.execute("DELETE FROM %s WHERE src = ?" % table, (name,))
        self.conn.execute("DELETE FROM source WHERE name = ?", (name,))
        self.out["gone"] += 1

    def run(self, loader, tables, files, whole):
        listed, loaded = files(self.data, self.root), False
        for name, path, reader, required, missing in listed:
            found = stat_of(path)
            if found is None:
                if required:
                    self.problem(name, loader, None, missing)
                continue
            if self.changed(name, found) or (self.known.get(name) or ("",) * 7)[6]:     # a bad file is tried again at every pass (named once)
                loaded = self.load(loader, tables, name, path, reader, whole) or loaded
        names = {entry[0] for entry in listed}
        for name, row in list(self.known.items()):
            if row[1] == loader and name not in names:
                if not whole:                      # a file of a folder that is gone takes its rows with it
                    self.forget(name, tables)
                elif loaded:                       # a whole loader's rows were all replaced: the old file is no source any more
                    self.conn.execute("DELETE FROM source WHERE name = ?", (name,))

    def fleet(self):
        """ships from fleet/fleet.json (read again when it or fleet/flagships.json changed), and the order each flies: a
        pilot is read again by division.order_of when its order file changed or went, or when its order aged past
        division.ORDER_FRESH (the file need not change for that)."""
        main, flags = Path(self.data) / "fleet" / "fleet.json", Path(self.data) / "fleet" / "flagships.json"
        rebuilt = False
        found, flagged = stat_of(main), stat_of(flags)
        flags_changed = self.changed("fleet/flagships.json", flagged) if flagged else "fleet/flagships.json" in self.known
        if found is None:
            self.problem("fleet/fleet.json", "fleet", None, "missing")
        elif self.changed("fleet/fleet.json", found) or flags_changed or (self.known.get("fleet/fleet.json") or ("",) * 7)[6]:
            rebuilt = self.load("fleet", ("ships",), "fleet/fleet.json", main, read_fleet, True)
        if flagged and flags_changed:
            self.keep("fleet/flagships.json", "flagships", flagged, int(self.now), 0, "")
        elif not flagged and "fleet/flagships.json" in self.known:
            self.conn.execute("DELETE FROM source WHERE name = ?", ("fleet/flagships.json",))
        folder = Path(self.data) / "fleet" / "orders"
        orders = {p.stem: ("fleet/orders/%s" % p.name, stat_of(p)) for p in folder.glob("*.json")} if folder.is_dir() else {}
        dirty = set()
        for pilot, (name, seen) in orders.items():
            if seen and self.changed(name, seen):
                dirty.add(pilot)
                self.keep(name, "orders", seen, int(self.now), 1, "")
                self.out["loaded"]["orders"] += 1
        for name, row in list(self.known.items()):
            if row[1] == "orders" and Path(name).stem not in orders:
                dirty.add(Path(name).stem)
                self.conn.execute("DELETE FROM source WHERE name = ?", (name,))
        for (pilot,) in self.conn.execute("SELECT pilot FROM ships WHERE flies IS NOT NULL").fetchall():
            seen = (orders.get(pilot) or ("", None))[1]
            if seen is None or self.now - seen[1] > division.ORDER_FRESH:
                dirty.add(pilot)
        if not rebuilt:
            for pilot in sorted(dirty):
                flies = division.order_of(pilot, self.data, self.now) or None
                self.out["flies"] += self.conn.execute("UPDATE ships SET flies = ? WHERE pilot = ? AND flies IS NOT ?", (flies, pilot, flies)).rowcount


def take_snapshot(conn, data, root, now):
    """Load every snapshot table whose files changed, in one transaction: {loaded: {loader: files}, rows, problems, gone, flies
    (ships whose order changed without fleet.json being read again)}."""
    work = Pass(conn, data, root, now)
    conn.execute("BEGIN IMMEDIATE")
    try:
        work.fleet()
        for loader, tables, files, whole in LOADERS:
            work.run(loader, tables, files, whole)
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return work.out


def snapshot_said(snap):
    """The snapshot's part of the pass's line, or '' when it did nothing worth a line."""
    if snap.get("error"):
        return "snapshot failed: %s" % snap["error"]
    parts = []
    if snap["loaded"]:
        parts.append("snapshot: %d files read (%s), %d rows" % (sum(snap["loaded"].values()), ", ".join(
            "%s %d" % (k, v) for k, v in sorted(snap["loaded"].items())), snap["rows"]))
    if snap["gone"]:
        parts.append("%d files gone" % snap["gone"])
    if snap.get("flies"):
        parts.append("%d ships' orders changed or aged" % snap["flies"])
    if snap["problems"]:
        parts.append("not read: " + "; ".join("%s (%s)" % (name, note) for name, note in snap["problems"]))
    return " | ".join(parts)


# ---- the database

def folder_of(data):
    return Path(data) / "store"


def open_live(data):
    """The writer's connection to live.db (WAL), with the tables made."""
    folder = folder_of(data)
    folder.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(folder / "live.db"), isolation_level=None, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(SCHEMA)
    setup_snapshot(conn)
    return conn


def meta(conn, key, default=0):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else default


def mark(first):
    """What marks a record: the digest of its first line, when that line is whole."""
    return hashlib.sha256(first).hexdigest()[:32] if first.endswith(b"\n") else ""


def new_lines(path, offset, head):
    """(whole new lines as bytes, the offset after them, the record's mark, cut?) of one record."""
    with open(path, "rb") as handle:
        size = os.fstat(handle.fileno()).st_size
        now = mark(handle.readline(HEAD))
        cut = size < offset or bool(head and now and head != now)
        start = 0 if cut else offset
        handle.seek(start)
        chunk = handle.read()
    whole = chunk[:chunk.rfind(b"\n") + 1]
    return whole, start + len(whole), now, cut


def take_record(conn, data, name, table, take, add_up, step):
    """Read one record's new lines and write rows, sums and cursor in one transaction: {added, bad, old, cut}."""
    out = {"added": 0, "bad": 0, "old": 0, "cut": False, "moved": False}
    path = Path(data) / name
    if not path.is_file():
        return out
    row = conn.execute("SELECT offset, head FROM cursor WHERE record = ?", (name,)).fetchone()
    offset, head = row if row else (0, "")
    whole, end, now, cut = new_lines(path, offset, head)
    out["cut"] = cut
    if end == offset and now == head and not cut:
        return out
    sealed = meta(conn, "sealed." + table)
    touched = set()
    conn.execute("BEGIN IMMEDIATE")
    try:
        for raw in whole.split(b"\n"):
            if not raw.strip():
                continue
            try:
                line = raw.decode("utf-8").strip()
                parsed = json.loads(line)
                if not isinstance(parsed, dict):
                    raise ValueError("not an object")
                got = take(conn, parsed, sealed, line)
            except (ValueError, TypeError, KeyError, AttributeError, OverflowError):
                out["bad"] += 1
                continue
            if got is None:
                out["old"] += 1
                continue
            out["added"] += got[0]
            touched |= got[1]
        add_up(conn, touched)
        conn.execute("INSERT OR REPLACE INTO cursor VALUES (?,?,?)", (name, end, now))
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    out["moved"] = True
    return out


def prune(conn, now, keep_days):
    """Delete raw rows older than keep_days (a table of KEEP_TABLES: its own days when longer) by whole hours (readings and
    observations: days) and seal those hours: rows deleted."""
    gone = 0
    conn.execute("BEGIN IMMEDIATE")
    try:
        for table, step in dict((table, step) for _name, table, _take, _sum, step in RECORDS).items():     # six records feed one table
            cut = int(now - max(keep_days, KEEP_TABLES.get(table, 0)) * DAY) // step * step
            if cut > meta(conn, "sealed." + table):
                gone += conn.execute("DELETE FROM %s WHERE t < ?" % table, (cut,)).rowcount
                conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", ("sealed." + table, cut))
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return gone


def copy_to(conn, target):
    """VACUUM INTO a temporary name beside target, then rename it into place."""
    target = Path(target)
    tmp = target.with_name(".%s.%d.tmp" % (target.name, os.getpid()))
    if tmp.exists():
        tmp.unlink()
    try:
        conn.execute("VACUUM INTO ?", (str(tmp),))
        handle = os.open(str(tmp), os.O_RDONLY)
        try:
            os.fsync(handle)
        finally:
            os.close(handle)
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()


def backup(conn, data, now, keep=BACKUPS):
    """The day's backup when it is not there yet; the `keep` newest stay. Its name, or None."""
    folder = folder_of(data) / "backup"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / ("collective-%s.db" % time.strftime("%Y-%m-%d", time.gmtime(now)))
    made = None
    if not target.exists():
        copy_to(conn, target)
        made = target.name
    for old in sorted(folder.glob("collective-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].db"))[:-keep]:
        old.unlink()
    return made


def one_pass(data, now=None, keep_days=KEEP_DAYS, root=None):
    """Read every record, load the snapshot tables whose files changed, prune, publish the copy when due, write the day's
    backup: what was done."""
    begun = time.time()
    now = begun if now is None else now
    out = {"records": {}, "snapshot": {"loaded": Counter(), "rows": 0, "problems": [], "gone": 0, "flies": 0}, "pruned": 0, "published": False, "backup": None,
           "recounted": 0}
    conn = open_live(data)
    try:
        for name, table, take, add_up, step in RECORDS:
            try:
                out["records"][name] = take_record(conn, data, name, table, take, add_up, step)
            except (OSError, sqlite3.Error) as error:  # one record that fails never holds up the others
                out["records"][name] = {"added": 0, "bad": 0, "old": 0, "cut": False, "moved": False,
                                        "error": "%s: %s" % (type(error).__name__, error)}
        asked = folder_of(data) / "recount"                # `store.py recount` asks; a new rule asks by itself
        if asked.exists() or meta(conn, "earned.rule", "") != EARNED_RULE:
            try:
                out["recounted"] = recount(conn)
                if asked.exists():
                    asked.unlink()
            except (OSError, sqlite3.Error) as error:      # the old sums stand; the next pass tries again
                out["records"]["recount"] = {"added": 0, "bad": 0, "old": 0, "cut": False, "moved": False, "error": "%s: %s" % (type(error).__name__, error)}
        try:
            out["snapshot"] = take_snapshot(conn, data, root or ROOT, now)
        except Exception as error:                     # a fault of the snapshot never holds up the history
            out["snapshot"] = {"loaded": Counter(), "rows": 0, "problems": [], "gone": 0, "flies": 0, "error": "%s: %s" % (type(error).__name__, error)}
        out["pruned"] = prune(conn, now, keep_days)
        snap = out["snapshot"]
        wrote = out["pruned"] or out["recounted"] or any(r["added"] or r["moved"] for r in out["records"].values()) or snap["loaded"] or snap["gone"] or snap["flies"]
        read = folder_of(data) / "read.db"
        if wrote or not read.exists() or time.time() - read.stat().st_mtime >= PUBLISH:
            copy_to(conn, read)
            out["published"] = True
        out["backup"] = backup(conn, data, now)
    finally:
        conn.close()
    out["seconds"] = time.time() - begun
    return out


def said(out):
    """The pass's one line, or None when it wrote nothing."""
    records = out["records"]
    snap = snapshot_said(out.get("snapshot") or {"loaded": {}, "rows": 0, "problems": [], "gone": 0, "flies": 0})
    if not (out["pruned"] or out["backup"] or out.get("recounted") or snap or any(r["added"] or r["bad"] or r["cut"] or r.get("error") for r in records.values())):
        return None
    parts = []
    for name, r in records.items():
        if name.startswith("observations/") and not (r["added"] or r["bad"] or r["old"] or r["cut"] or r.get("error")):
            continue                               # six records that mostly stand still: named only in a pass that read one
        part = "%s +%d" % (name, r["added"])
        extra = [w for w, on in (("cut: read from 0", r["cut"]), ("%d bad" % r["bad"], r["bad"]),
                                 ("%d sealed" % r["old"], r["old"]), ("failed: %s" % r.get("error"), r.get("error"))) if on]
        parts.append(part + (" (%s)" % ", ".join(extra) if extra else ""))
    if snap:
        parts.append(snap)
    if out.get("recounted"):
        parts.append("%d runs counted again" % out["recounted"])
    if out["pruned"]:
        parts.append("%d old rows deleted" % out["pruned"])
    if out["backup"]:
        parts.append("backup %s" % out["backup"])
    return "%s | %s | %.2f s" % (" | ".join(parts), "copy published" if out["published"] else "copy not due", out["seconds"])


# ---- one writer

def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def lease(data, me=None):
    """Take or renew the writer's lease: None when it is ours, else who holds it."""
    folder = folder_of(data)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "writer.lease"
    me = me or "%s %d" % (os.uname().nodename, os.getpid())
    for _ in range(3):
        try:
            handle = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            try:
                holder, age = path.read_text(encoding="ascii").strip(), time.time() - path.stat().st_mtime
            except (OSError, UnicodeDecodeError):
                continue
            if holder == me:
                os.utime(str(path))
                return None
            host, _, pid = holder.partition(" ")
            dead = host == me.partition(" ")[0] and pid.isdigit() and not alive(int(pid))
            if age < LEASE_FRESH and not dead:
                return "%s, renewed %d s ago" % (holder, age)
            try:
                path.unlink()
            except FileNotFoundError:
                pass
            continue
        try:
            os.write(handle, me.encode("ascii"))
        finally:
            os.close(handle)
        return None
    return "the lease could not be taken"


def release(data, me=None):
    path = folder_of(data) / "writer.lease"
    me = me or "%s %d" % (os.uname().nodename, os.getpid())
    try:
        if path.read_text(encoding="ascii").strip() == me:
            path.unlink()
    except (OSError, UnicodeDecodeError):
        pass


# ---- for readers

def connect(data):
    """A read-only connection to the published copy, or None while no copy exists."""
    path = folder_of(data) / "read.db"
    if not path.is_file():
        return None
    return sqlite3.connect("file:%s?mode=ro&immutable=1" % urllib.parse.quote(str(path.resolve())), uri=True)


def route_rates(conn, since_epoch):
    """{route: (runs, read minutes, credits, one_time, credits per ship-hour or None)} over the hours from the
    hour that holds since_epoch on (whole hours: the sums are kept by hour)."""
    out = {}
    for route, runs, read_minutes, credits, one_time in conn.execute(
            "SELECT route, SUM(runs), SUM(read_minutes), SUM(credits), SUM(one_time) FROM route_hour WHERE hour >= ? "
            "GROUP BY route ORDER BY route", (int(since_epoch) // HOUR * HOUR,)):
        rate = round(60.0 * credits / read_minutes, 1) if read_minutes else None
        out[route] = (runs, read_minutes, credits, one_time, rate)
    return out


DESCRIPTIONS = {               # one line per table and view: what a row is and where it comes from (schema(), hive.py schema)
    "cursor": "history bookkeeping: where each record (routes/runs.jsonl, market/history.jsonl, wildlife/history.jsonl, observations/<division>.jsonl) "
              "was read to, by byte",
    "meta": "the store's settings: the sealed hour (day) of each raw table, the snapshot schema's version and its tables",
    "runs": "history: one row per run of a route (pilot, route, start, minutes, steady credits, paid once, read a wallet), the raw rows of --keep-days days",
    "moves": "history: one row per change of an item's best bid or ask at a station (market/history.jsonl), the raw rows of --keep-days days",
    "readings": "history: one row per census count of a field (units left) or a herd (animals) at a place, the raw rows of --keep-days days",
    "route_hour": "history: per route and UTC hour the runs, minutes, read minutes, steady credits and paid once; kept for good",
    "market_hour": "history: per station, item and UTC hour the lowest and highest best bid and best ask; kept for good",
    "reading_day": "history: per place, field or herd and UTC day the first and the last count; kept for good",
    "observations": "history: one row per observation a member wrote with observe.py (observations/<division>.jsonl): division, member, kind, "
                    "subject, when it was seen (t, at), note; `fields` is JSON text, one field read by json_extract(fields, '$.<key>'); kept 30 days at least",
    "source": "snapshot bookkeeping: every file the snapshot tables were read from: size, mtime, when loaded (t), rows, and why not (note)",
    "ships": "now: one row per ship of ours (fleet/fleet.json): member and division, place, docked at which base, hull, fuel, hold, wallet, the order it flies",
    "ship_skills": "now: every skill of every ship with its level and XP (fleet/ships/<pilot>.json)",
    "ship_modules": "now: every module fitted to every ship (fleet/ships/<pilot>.json)",
    "ship_cargo": "now: what each ship carries in its hold, from its own live file (fleet/ships/<pilot>.json)",
    "holdings": "now: what we hold per pilot, station and item (stock/storage.json); place `hold`: the holds per member as the book sums them, no pilot",
    "books": "now: each station's order book as our ship read it: best bid and ask with their units per item (market/<base>.json); no price is NULL",
    "ladders": "now: the price ladder of an item at a station, every bid and ask step with its units, step 1 the best (market/ladders.json)",
    "items": "catalog: every item of the game: name, category (NULL where the catalog gives none), size, base value, rarity, module type and slot",
    "recipes": "catalog: every recipe: category, made by hand or only in a facility, crafting time; inputs, outputs and facilities in their own tables",
    "recipe_inputs": "catalog: what a recipe takes, item and units per run",
    "recipe_outputs": "catalog: what a recipe makes, item and units per run",
    "recipe_facilities": "catalog: the facilities a recipe runs in",
    "facilities": "catalog: every facility type: level, build cost, time and labor, the facility it upgrades, its services, faction cap (member cap for recruitment)",
    "facility_materials": "catalog: what a facility takes to build, item and units",
    "hulls": "catalog: every hull (the catalog's `ships`): class, tier, cargo, hull, shield, slots, the piloting it needs; no price is in the catalog",
    "hull_materials": "catalog: what a hull takes to build, item and units",
    "skills": "catalog: every skill: category, highest level, how it is trained, the empire that may learn it",
    "places": "now: every place (POI) of a system our census read: its kind, name, class and the base on it (scouting/<system>.json)",
    "fields": "now: what is left in each resource field of a place, by the newest census (scouting/<system>.json)",
    "herds": "now: the creatures at a place by species, counted by the newest census (wildlife/<system>.json)",
    "systems": "the map: every star system, its empire (NULL lawless), capital (home), stronghold and jumps from our home (station/map.json, else game/map/galaxy.tsv)",
    "lanes": "the map: the jump lanes, one row per direction as the map lists them",
    "stations": "every station and outpost of the galaxy: kind, system, its owner's faction tag and name, condition, services (station/stations.json)",
    "factions": "every faction of the game: tag, name, members, leader, allies, enemies, wars as comma text (station/feed.json)",
    "faction": "our faction, one row: tag, leader, members and their limit, treasury, bases owned, at war (empire/empire.json)",
    "faction_members": "our faction's members and their roles (empire/empire.json)",
    "bases": "our faction's bases: base id, name, system, place, kind (empire/empire.json)",
    "faction_facilities": "our faction's facilities: type, level, base, status, rent per cycle (empire/empire.json)",
    "territory": "the systems our faction claims (empire/empire.json)",
    "sites": "places our faction watches or plans for (empire/empire.json)",
    "missions": "now: the missions on offer at each station our ships read: kind, reward in credits, items, XP, objectives (missions/<base>.json)",
    "met": "the pilots of OTHER players our ships met: faction, ship class, where last seen, first and last seen (t), times met (intel/met.json)",
    "routes": "the repository's route files (game/routes/<id>.json): kind, group (routes.py stage), cap, what the runs measured (cph per ship-hour)",
    "plan_routes": "each role's plan in its order: the routes its ships try and the ships the plan puts on each (game/routes/plans/<role>.json)",
    "inventory": "view: what the fleet holds per item, in storage and in the holds, with its base value and worth (units x base value): craftbook.py inventory's sums",
    "inventory_by_station": "view: what the fleet holds per place (a station's base id, or `hold`) and item",
    "fleet_positions": "view: our ships per system: the system's name, empire and jumps from home, ships, docked, flying (in space), ships per division",
    "our_stations": "view: the stations and outposts whose owner's tag is our faction's, joined to our bases",
    "route_earnings": "view: what each route earned per ship-hour (steady credits) over the last 4, 12 and 24 hours and over all hours kept, the runs behind each "
                      "figure, and the hours since it last flew: ask here what a route earns now; an empty cph_4h means it did not fly, not that it does not pay",
}

EXAMPLES = {                   # three questions per table and view, as SQL (hive.py schema <table>); the tests run each one
    "cursor": (("Where is each record read to?", "SELECT record, offset FROM cursor ORDER BY record"),
               ("How far is the run record read?", "SELECT offset FROM cursor WHERE record = 'routes/runs.jsonl'"),
               ("How many records are read?", "SELECT COUNT(*) FROM cursor")),
    "meta": (("Which hours and days are sealed?", "SELECT key, datetime(value, 'unixepoch') FROM meta WHERE key LIKE 'sealed.%'"),
             ("Which snapshot schema is in use?", "SELECT value FROM meta WHERE key = 'snapshot.schema'"),
             ("Every setting", "SELECT key, value FROM meta ORDER BY key")),
    "runs": (("The last ten runs", "SELECT pilot, route, started, minutes, credits FROM runs ORDER BY t DESC LIMIT 10"),
             ("Steady credits per ship-hour per route over the raw runs that read a wallet",
              "SELECT route, COUNT(*) AS runs, ROUND(60.0 * SUM(credits) / SUM(minutes)) AS per_ship_hour FROM runs WHERE readable = 1 AND minutes > 0 "
              "GROUP BY route ORDER BY per_ship_hour DESC"),
             ("Routes whose runs read no wallet", "SELECT route, COUNT(*) FROM runs WHERE readable = 0 GROUP BY route ORDER BY 2 DESC")),
    "moves": (("The last price moves of iron_ore", "SELECT base, datetime(t, 'unixepoch') AS at, bid, bid_qty, ask, ask_qty FROM moves WHERE item = 'iron_ore' "
               "ORDER BY t DESC LIMIT 10"),
              ("Which items moved most often", "SELECT item, COUNT(*) FROM moves GROUP BY item ORDER BY 2 DESC LIMIT 10"),
              ("Moves per station", "SELECT base, COUNT(*) FROM moves GROUP BY base ORDER BY 2 DESC")),
    "readings": (("The newest field counts in node_beta", "SELECT poi, what, amount, datetime(t, 'unixepoch') FROM readings WHERE system = 'node_beta' "
                  "AND kind = 'field' ORDER BY t DESC LIMIT 20"),
                 ("Herds counted at 0", "SELECT system, poi, what, datetime(t, 'unixepoch') FROM readings WHERE kind = 'herd' AND amount = 0 ORDER BY t DESC LIMIT 20"),
                 ("Readings per system", "SELECT system, COUNT(*) FROM readings GROUP BY system ORDER BY 2 DESC")),
    "route_hour": (("Credits per ship-hour per route over the last 24 hours",
                    "SELECT route, SUM(runs) AS runs, ROUND(60.0 * SUM(credits) / SUM(read_minutes)) AS per_ship_hour FROM route_hour "
                    "WHERE hour >= strftime('%s', 'now') - 86400 GROUP BY route HAVING SUM(read_minutes) > 0 ORDER BY per_ship_hour DESC"),
                   ("The fleet's steady credits hour by hour", "SELECT datetime(hour, 'unixepoch') AS hour, SUM(runs), SUM(credits) FROM route_hour "
                    "GROUP BY 1 ORDER BY 1 DESC LIMIT 24"),
                   ("Routes that paid once", "SELECT route, SUM(one_time) FROM route_hour GROUP BY route HAVING SUM(one_time) > 0 ORDER BY 2 DESC")),
    "market_hour": (("The highest bid for iron_ore per station in the last day", "SELECT base, MAX(bid_hi) FROM market_hour WHERE item = 'iron_ore' "
                     "AND hour >= strftime('%s', 'now') - 86400 GROUP BY base ORDER BY 2 DESC"),
                    ("The cheapest ask ever seen for steel_plate", "SELECT base, MIN(ask_lo), datetime(MAX(hour), 'unixepoch') FROM market_hour "
                     "WHERE item = 'steel_plate' GROUP BY base ORDER BY 2"),
                    ("Hours of prices per item", "SELECT item, COUNT(*) FROM market_hour GROUP BY item ORDER BY 2 DESC LIMIT 20")),
    "reading_day": (("How the fields changed per day", "SELECT system, poi, what, date(day, 'unixepoch') AS day, first, last, last - first AS change "
                     "FROM reading_day WHERE kind = 'field' ORDER BY day DESC, change LIMIT 20"),
                    ("Herds that shrank in a day", "SELECT system, poi, what, date(day, 'unixepoch'), first, last FROM reading_day WHERE kind = 'herd' "
                     "AND last < first ORDER BY day DESC"),
                    ("Days on record per system", "SELECT system, COUNT(DISTINCT day) FROM reading_day GROUP BY system ORDER BY 2 DESC")),
    "observations": (("The newest observations of every division", "SELECT at, division, member, kind, subject, fields, note FROM observations "
                      "ORDER BY t DESC LIMIT 20"),
                     ("Every kind on record: its rows, its newest time, which division", "SELECT kind, division, COUNT(*) AS n, "
                      "datetime(MAX(t), 'unixepoch') AS newest FROM observations GROUP BY kind, division ORDER BY n DESC"),
                     ("Prices seen at stations we read no book of (kind price): fields read by json_extract",
                      "SELECT at, subject AS station, json_extract(fields, '$.item') AS item, json_extract(fields, '$.bid') AS bid, "
                      "json_extract(fields, '$.ask') AS ask FROM observations WHERE kind = 'price' ORDER BY t DESC LIMIT 20")),
    "source": (("Which files could not be read, and why", "SELECT name, note FROM source WHERE note <> ''"),
               ("How fresh is each loader's newest file", "SELECT loader, COUNT(*) AS files, datetime(MAX(mtime), 'unixepoch') AS newest_file, "
                "datetime(MAX(t), 'unixepoch') AS loaded FROM source GROUP BY loader"),
               ("The largest files", "SELECT name, size, rows FROM source ORDER BY size DESC LIMIT 10")),
    "ships": (("Where are our ships, by system", "SELECT system, COUNT(*) AS ships FROM ships GROUP BY system ORDER BY ships DESC"),
              ("Ships low on fuel", "SELECT pilot, system, fuel, max_fuel FROM ships WHERE fuel < max_fuel / 4 ORDER BY fuel"),
              ("What each division flies now", "SELECT division, flies, COUNT(*) FROM ships GROUP BY division, flies ORDER BY division, 3 DESC")),
    "ship_skills": (("The highest Piloting levels", "SELECT pilot, level FROM ship_skills WHERE skill = 'piloting' ORDER BY level DESC LIMIT 10"),
                    ("Average and highest level per skill", "SELECT skill, ROUND(AVG(level), 1), MAX(level) FROM ship_skills GROUP BY skill ORDER BY 2 DESC"),
                    ("The skills of the mining division", "SELECT k.skill, ROUND(AVG(k.level), 1) FROM ship_skills k JOIN ships s ON s.pilot = k.pilot "
                     "WHERE s.division = 'Mining' GROUP BY k.skill ORDER BY 2 DESC")),
    "ship_modules": (("How many ships carry each module", "SELECT module, COUNT(DISTINCT pilot) FROM ship_modules GROUP BY module ORDER BY 2 DESC"),
                     ("Ships with an ice harvester", "SELECT pilot FROM ship_modules WHERE module = 'ice_harvester_i'"),
                     ("Ships without a mining laser", "SELECT pilot FROM ships WHERE pilot NOT IN (SELECT pilot FROM ship_modules WHERE module = 'mining_laser_i')")),
    "ship_cargo": (("What our holds carry, by item", "SELECT item, SUM(units) FROM ship_cargo GROUP BY item ORDER BY 2 DESC"),
                   ("Which ships carry iron_ore", "SELECT pilot, units FROM ship_cargo WHERE item = 'iron_ore' ORDER BY units DESC"),
                   ("Ships with a full hold", "SELECT pilot, cargo_used, cargo_capacity FROM ships WHERE cargo_used >= cargo_capacity")),
    "holdings": (("Who holds iron_ore, and where", "SELECT pilot, place, units FROM holdings WHERE item = 'iron_ore' ORDER BY units DESC LIMIT 20"),
                 ("Storage per member", "SELECT member, SUM(units) FROM holdings WHERE place <> 'hold' GROUP BY member"),
                 ("The stations where we store goods", "SELECT place, COUNT(DISTINCT item), SUM(units) FROM holdings WHERE place <> 'hold' GROUP BY place")),
    "books": (("Which stations bid for iron_ore, and how much", "SELECT base, system, bid, bid_qty, datetime(t, 'unixepoch') AS read FROM books "
               "WHERE item = 'iron_ore' AND bid IS NOT NULL ORDER BY bid DESC"),
              ("The cheapest offers of steel_plate", "SELECT base, ask, ask_qty FROM books WHERE item = 'steel_plate' AND ask IS NOT NULL ORDER BY ask"),
              ("Bought at one station's ask, bid higher at another", "SELECT a.item, a.base AS buy_at, a.ask, b.base AS sell_at, b.bid, b.bid - a.ask AS margin "
               "FROM books a JOIN books b ON b.item = a.item AND b.base <> a.base WHERE a.ask IS NOT NULL AND b.bid > a.ask ORDER BY margin DESC LIMIT 20")),
    "ladders": (("The whole bid ladder of iron_ore", "SELECT base, step, price, qty FROM ladders WHERE item = 'iron_ore' AND side = 'bid' ORDER BY base, step"),
                ("Units bid at 100 cr or more, per item", "SELECT item, SUM(qty) FROM ladders WHERE side = 'bid' AND price >= 100 GROUP BY item ORDER BY 2 DESC"),
                ("Items with a ladder per station", "SELECT base, COUNT(DISTINCT item) FROM ladders GROUP BY base")),
    "items": (("The items of highest base value", "SELECT id, name, base_value FROM items ORDER BY base_value DESC LIMIT 10"),
              ("How many items have no category", "SELECT COUNT(*) FROM items WHERE category IS NULL"),
              ("Find an item by its name", "SELECT id, name, category FROM items WHERE name LIKE '%steel%'")),
    "recipes": (("Recipes made by hand", "SELECT id, name, time FROM recipes WHERE hand = 1 ORDER BY name LIMIT 20"),
                ("Recipes per category", "SELECT category, COUNT(*) FROM recipes GROUP BY category ORDER BY 2 DESC"),
                ("What makes steel_plate", "SELECT r.id, r.name, o.units, r.hand FROM recipe_outputs o JOIN recipes r ON r.id = o.recipe WHERE o.item = 'steel_plate'")),
    "recipe_inputs": (("Which recipes use steel_plate", "SELECT r.id, r.name, i.units FROM recipe_inputs i JOIN recipes r ON r.id = i.recipe "
                       "WHERE i.item = 'steel_plate' ORDER BY r.name"),
                      ("What the recipe of steel_plate takes", "SELECT item, units FROM recipe_inputs WHERE recipe IN "
                       "(SELECT recipe FROM recipe_outputs WHERE item = 'steel_plate')"),
                      ("The inputs most recipes use", "SELECT item, COUNT(*) FROM recipe_inputs GROUP BY item ORDER BY 2 DESC LIMIT 10")),
    "recipe_outputs": (("What makes steel_plate", "SELECT recipe, units FROM recipe_outputs WHERE item = 'steel_plate'"),
                       ("Recipes with more than one output", "SELECT recipe, COUNT(*) FROM recipe_outputs GROUP BY recipe HAVING COUNT(*) > 1"),
                       ("Goods we hold that no recipe makes", "SELECT DISTINCT item FROM holdings WHERE item NOT IN (SELECT item FROM recipe_outputs)")),
    "recipe_facilities": (("Where steel_plate is made", "SELECT f.recipe, f.facility FROM recipe_facilities f JOIN recipe_outputs o ON o.recipe = f.recipe "
                           "WHERE o.item = 'steel_plate'"),
                          ("Recipes per facility", "SELECT facility, COUNT(*) FROM recipe_facilities GROUP BY facility ORDER BY 2 DESC LIMIT 10"),
                          ("Recipes that run only in a facility", "SELECT id FROM recipes WHERE facility_only = 1 AND id IN (SELECT recipe FROM recipe_facilities) "
                           "LIMIT 20")),
    "facilities": (("Which facility types raise the faction's member limit, and what they cost",
                    "SELECT id, level, faction_cap AS member_cap, build_cost, build_time, labor_cost, upgrades_from FROM facilities "
                    "WHERE faction_service_type = 'faction_recruitment' ORDER BY level"),
                   ("Faction facilities by cost", "SELECT id, faction_service_type, level, build_cost FROM facilities WHERE category = 'faction' ORDER BY build_cost"),
                   ("The upgrade chain above hiring_board", "WITH RECURSIVE up(id, level) AS (SELECT id, level FROM facilities WHERE id = 'hiring_board' "
                    "UNION ALL SELECT f.id, f.level FROM facilities f JOIN up ON f.upgrades_from = up.id) SELECT id, level FROM up")),
    "facility_materials": (("What recruitment_desk takes to build", "SELECT item, units FROM facility_materials WHERE facility = 'recruitment_desk'"),
                           ("Facilities that need steel_plate", "SELECT facility, units FROM facility_materials WHERE item = 'steel_plate' ORDER BY units DESC LIMIT 20"),
                           ("The recruitment chain's materials against what we hold",
                            "SELECT m.item, SUM(m.units) AS needed, (SELECT SUM(units) FROM holdings h WHERE h.item = m.item) AS held FROM facility_materials m "
                            "JOIN facilities f ON f.id = m.facility WHERE f.faction_service_type = 'faction_recruitment' GROUP BY m.item")),
    "hulls": (("The hulls with the most cargo", "SELECT id, name, class, tier, cargo FROM hulls ORDER BY cargo DESC LIMIT 10"),
              ("Tier 2 hulls of the voidborn", "SELECT id, name, class, cargo, piloting_required FROM hulls WHERE tier = 2 AND faction = 'voidborn'"),
              ("Hulls per class", "SELECT class, COUNT(*) FROM hulls GROUP BY class ORDER BY 2 DESC")),
    "hull_materials": (("What the hull of most cargo takes to build", "SELECT item, units FROM hull_materials WHERE hull = "
                        "(SELECT id FROM hulls ORDER BY cargo DESC LIMIT 1)"),
                       ("Hulls that need processing_core", "SELECT hull, units FROM hull_materials WHERE item = 'processing_core' ORDER BY units DESC LIMIT 10"),
                       ("Materials over all tier 1 hulls", "SELECT m.item, SUM(m.units) FROM hull_materials m JOIN hulls h ON h.id = m.hull WHERE h.tier = 1 "
                        "GROUP BY m.item ORDER BY 2 DESC LIMIT 10")),
    "skills": (("Every skill", "SELECT id, name, category, max_level FROM skills ORDER BY category, id"),
               ("How mining is trained", "SELECT id, training FROM skills WHERE id = 'mining'"),
               ("Skills only one empire may learn", "SELECT id, empire FROM skills WHERE empire IS NOT NULL")),
    "places": (("The stations among the places we read", "SELECT system, poi, name, base FROM places WHERE base IS NOT NULL"),
               ("Places per kind", "SELECT kind, COUNT(*) FROM places GROUP BY kind ORDER BY 2 DESC"),
               ("The places of node_beta", "SELECT poi, kind, name FROM places WHERE system = 'node_beta'")),
    "fields": (("Where iron_ore is left", "SELECT system, poi, remaining, max_remaining, datetime(t, 'unixepoch') FROM fields WHERE resource = 'iron_ore' "
                "AND remaining > 0 ORDER BY remaining DESC"),
               ("What is left in all fields, per resource", "SELECT resource, SUM(remaining), COUNT(*) FROM fields GROUP BY resource ORDER BY 2 DESC"),
               ("Fields within 3 jumps of home", "SELECT f.system, f.poi, f.resource, f.remaining, y.jumps FROM fields f JOIN systems y ON y.id = f.system "
                "WHERE y.jumps <= 3 AND f.remaining > 0 ORDER BY y.jumps, f.remaining DESC")),
    "herds": (("The largest herds", "SELECT system, poi, creature, count FROM herds ORDER BY count DESC LIMIT 10"),
              ("Where cauldronbacks live", "SELECT system, poi, count FROM herds WHERE creature = 'cauldronback'"),
              ("Animals per system", "SELECT system, SUM(count) FROM herds GROUP BY system ORDER BY 2 DESC")),
    "systems": (("Systems within 3 jumps of home", "SELECT id, name, empire, jumps FROM systems WHERE jumps <= 3 ORDER BY jumps, id"),
                ("The empires' capitals and strongholds", "SELECT id, name, empire, home, stronghold FROM systems WHERE home = 1 OR stronghold = 1"),
                ("The nearest lawless systems", "SELECT id, jumps FROM systems WHERE empire IS NULL ORDER BY jumps LIMIT 10")),
    "lanes": (("The neighbours of nexus_prime", "SELECT b FROM lanes WHERE a = 'nexus_prime'"),
              ("Systems with the most lanes", "SELECT a, COUNT(*) FROM lanes GROUP BY a ORDER BY 2 DESC LIMIT 10"),
              ("Lanes that cross a border", "SELECT l.a, x.empire, l.b, y.empire FROM lanes l JOIN systems x ON x.id = l.a JOIN systems y ON y.id = l.b "
               "WHERE COALESCE(x.empire, '') <> COALESCE(y.empire, '') LIMIT 20")),
    "stations": (("Which stations and outposts lie within 3 jumps of our home, and who owns them",
                  "SELECT s.name, s.kind, s.system, y.jumps, s.tag, s.faction FROM stations s JOIN systems y ON y.id = s.system WHERE y.jumps <= 3 "
                  "ORDER BY y.jumps, s.system, s.name"),
                 ("Stations per faction", "SELECT tag, faction, COUNT(*) FROM stations GROUP BY tag, faction ORDER BY 3 DESC"),
                 ("Wrecked or mobile stations", "SELECT name, system, kind, wrecked, mobile FROM stations WHERE wrecked = 1 OR mobile = 1")),
    "factions": (("The largest factions", "SELECT tag, name, members, leader FROM factions ORDER BY members DESC LIMIT 10"),
                 ("Factions at war", "SELECT tag, name, wars FROM factions WHERE wars <> ''"),
                 ("The owners of stations within 5 jumps", "SELECT DISTINCT f.tag, f.name, f.members FROM stations s JOIN systems y ON y.id = s.system "
                  "JOIN factions f ON f.tag = s.tag WHERE y.jumps <= 5")),
    "faction": (("Our faction", "SELECT tag, name, leader, member_count, members_limit, treasury, owned_bases, at_war FROM faction"),
                ("Room for members", "SELECT member_count, members_limit, members_limit - member_count AS free FROM faction"),
                ("Our faction beside the others by size", "SELECT f.tag, f.members, (SELECT COUNT(*) FROM factions g WHERE g.members > f.members) + 1 AS rank "
                 "FROM factions f JOIN faction o ON o.tag = f.tag")),
    "faction_members": (("Members per role", "SELECT role, COUNT(*) FROM faction_members GROUP BY role"),
                        ("Our ships that are no members", "SELECT pilot FROM ships WHERE pilot NOT IN (SELECT pilot FROM faction_members)"),
                        ("Members per division", "SELECT s.division, COUNT(*) FROM faction_members m JOIN ships s ON s.pilot = m.pilot GROUP BY s.division")),
    "bases": (("Our bases", "SELECT base, name, system, poi, kind FROM bases"),
              ("Our bases and their jumps from home", "SELECT b.name, b.system, y.jumps FROM bases b LEFT JOIN systems y ON y.id = b.system ORDER BY y.jumps"),
              ("Our ships docked at our bases", "SELECT b.name, COUNT(s.pilot) FROM bases b LEFT JOIN ships s ON s.base = b.base GROUP BY b.base")),
    "faction_facilities": (("Our facilities and their rent", "SELECT name, type, level, base, status, rent_per_cycle FROM faction_facilities ORDER BY base"),
                           ("Rent per cycle in all", "SELECT SUM(rent_per_cycle) FROM faction_facilities"),
                           ("Facilities not active", "SELECT name, base, status FROM faction_facilities WHERE status <> 'active'")),
    "territory": (("Our territory", "SELECT system, claim, note FROM territory"),
                  ("Our ships in our territory", "SELECT t.system, COUNT(s.pilot) FROM territory t LEFT JOIN ships s ON s.system = t.system GROUP BY t.system"),
                  ("Our territory and its jumps from home", "SELECT t.system, y.jumps FROM territory t LEFT JOIN systems y ON y.id = t.system ORDER BY y.jumps")),
    "sites": (("The sites we watch", "SELECT system, poi, status, note FROM sites"),
              ("Sites per status", "SELECT status, COUNT(*) FROM sites GROUP BY status"),
              ("Stations in the systems of our sites", "SELECT si.system, si.poi, st.name, st.tag FROM sites si JOIN stations st ON st.system = si.system")),
    "missions": (("The missions of highest reward", "SELECT base, title, kind, reward FROM missions ORDER BY reward DESC LIMIT 10"),
                 ("Missions per station", "SELECT base, COUNT(*), SUM(reward) FROM missions GROUP BY base"),
                 ("Missions that hand out items", "SELECT base, title, reward_items FROM missions WHERE reward_items IS NOT NULL")),
    "met": (("Pilots of others seen in the last hour", "SELECT name, faction, class, system, datetime(t, 'unixepoch') FROM met "
             "WHERE t >= strftime('%s', 'now') - 3600 ORDER BY t DESC"),
            ("The factions we meet most", "SELECT faction, COUNT(*), SUM(times) FROM met GROUP BY faction ORDER BY 3 DESC LIMIT 10"),
            ("Pilots seen in combat", "SELECT name, faction, system, datetime(in_combat, 'unixepoch') FROM met WHERE in_combat IS NOT NULL ORDER BY in_combat DESC")),
    "routes": (("Paying routes by credits per ship-hour", "SELECT id, kind, cph, runs, measured FROM routes WHERE grp = 'paying' ORDER BY cph DESC"),
               ("Routes per group", "SELECT grp, COUNT(*) FROM routes GROUP BY grp"),
               ("The routes our ships fly now", "SELECT r.id, r.grp, COUNT(s.pilot) FROM routes r JOIN ships s ON s.flies = r.kind || ' ' || r.id "
                "GROUP BY r.id ORDER BY 3 DESC")),
    "plan_routes": (("The miner plan in its order", "SELECT n, route, ships FROM plan_routes WHERE role = 'miner' ORDER BY n"),
                    ("Every plan with each route's group and figure", "SELECT p.role, p.n, p.route, r.grp, r.cph FROM plan_routes p "
                     "LEFT JOIN routes r ON r.id = p.route ORDER BY p.role, p.n"),
                    ("Routes in more than one plan", "SELECT route, COUNT(DISTINCT role) FROM plan_routes GROUP BY route HAVING COUNT(DISTINCT role) > 1")),
    "inventory": (("What do we hold most of, by worth", "SELECT item, name, units, base_value, worth FROM inventory ORDER BY worth DESC LIMIT 10"),
                  ("Goods we hold that no station bids for", "SELECT item, units FROM inventory WHERE item NOT IN (SELECT item FROM books WHERE bid IS NOT NULL) "
                   "ORDER BY units DESC"),
                  ("The worth of what we hold, per category", "SELECT category, SUM(worth) FROM inventory GROUP BY category ORDER BY 2 DESC")),
    "inventory_by_station": (("What lies at node_beta_industrial_station", "SELECT item, name, units FROM inventory_by_station "
                              "WHERE place = 'node_beta_industrial_station' ORDER BY units DESC"),
                             ("Where iron_ore lies", "SELECT place, units FROM inventory_by_station WHERE item = 'iron_ore'"),
                             ("The worth of the goods per place", "SELECT v.place, SUM(v.units * i.base_value) FROM inventory_by_station v "
                              "LEFT JOIN items i ON i.id = v.item GROUP BY v.place ORDER BY 2 DESC")),
    "fleet_positions": (("Where are our ships, by system and division", "SELECT * FROM fleet_positions ORDER BY ships DESC"),
                        ("Our ships away from home", "SELECT system, name, empire, jumps, ships FROM fleet_positions WHERE jumps > 0 ORDER BY jumps DESC"),
                        ("Systems where ships lie docked", "SELECT system, docked, flying FROM fleet_positions WHERE docked > 0")),
    "route_earnings": (("What every route earned per ship-hour in the last 4 hours, best first",
                        "SELECT route, kind, runs_4h, cph_4h, cph_24h FROM route_earnings WHERE runs_4h > 0 ORDER BY cph_4h DESC"),
                       ("Routes that have not flown for 12 hours or more: their figure is old, a test tells what they pay now",
                        "SELECT route, kind, hours_since, runs_all, cph_all FROM route_earnings WHERE hours_since >= 12 ORDER BY hours_since"),
                       ("Routes that pay less now than over the day (a bid or a field that is running out)",
                        "SELECT route, cph_4h, cph_24h, runs_4h FROM route_earnings WHERE runs_4h >= 2 AND cph_4h < cph_24h ORDER BY cph_4h - cph_24h")),
    "our_stations": (("Our stations and outposts", "SELECT name, kind, system, condition, base FROM our_stations"),
                     ("Our stations and their jumps from home", "SELECT o.name, o.system, y.jumps FROM our_stations o LEFT JOIN systems y ON y.id = o.system"),
                     ("Our stations that no base row of empire.json names", "SELECT name, system FROM our_stations WHERE base IS NULL")),
}


def schema(conn):
    """{table or view: {kind, description (None when it has none), columns [(name, type)], examples}} of a database, in the
    order of DESCRIPTIONS, then any other."""
    found = {name: kind for name, kind in conn.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%'")}
    order = [name for name in DESCRIPTIONS if name in found] + sorted(name for name in found if name not in DESCRIPTIONS)
    return {name: {"kind": found[name], "description": DESCRIPTIONS.get(name), "examples": EXAMPLES.get(name, ()),
                   "columns": [(row[1], row[2]) for row in conn.execute("SELECT * FROM pragma_table_info(?)", (name,))]} for name in order}


# ---- the read side: one statement, reading only

ALLOWED = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}
PRAGMAS = {"table_info", "table_xinfo", "index_list", "index_info", "index_xinfo", "foreign_key_list"}       # read as table functions only
LIMIT_MAX = 100000             # rows: the most one answer may carry


def reads_only(action, arg1, arg2, _db, _trigger):
    """The authorizer of query(): reading, functions (not load_extension), recursive WITH and the pragma functions that only
    read; everything else (a write, ATTACH, a pragma that sets, a transaction) is refused."""
    if action == sqlite3.SQLITE_FUNCTION:
        return sqlite3.SQLITE_DENY if str(arg2).lower() == "load_extension" else sqlite3.SQLITE_OK
    if action in ALLOWED:
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_PRAGMA and str(arg1).lower() in PRAGMAS:
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def statement(sql):
    """The statement without leading comments and blanks, and its first word in capitals."""
    body = str(sql or "")
    while True:
        body = body.lstrip()
        if body.startswith("--"):
            body = body.partition("\n")[2]
        elif body.startswith("/*") and "*/" in body:
            body = body.split("*/", 1)[1]
        else:
            break
    word = ""
    for char in body:
        if not (char.isalpha() or char == "_"):
            break
        word += char
    return body, word.upper()


def query(data, sql, limit=200, seconds=5):
    """One read-only statement on the read copy: {columns, rows (at most `limit`), cut (more rows matched), error (one plain
    line or None)}. Only a statement that begins with SELECT or WITH; a second statement, a write, ATTACH and a pragma that
    sets are refused by SQLite itself (query_only, the authorizer, one statement per call), not by the words alone; a
    statement still running after `seconds` is stopped."""
    out = {"columns": [], "rows": [], "cut": False, "error": None}
    body, word = statement(sql)
    if not body.strip().rstrip(";").strip():
        out["error"] = "no statement: give one SELECT or WITH statement"
        return out
    if word not in ("SELECT", "WITH"):
        out["error"] = "refused: only one statement that begins with SELECT or WITH is taken, not %s" % (word or body.split()[0][:20])
        return out
    try:
        limit = max(1, min(int(limit), LIMIT_MAX))
        seconds = float(seconds)
    except (TypeError, ValueError):
        out["error"] = "the limit and the seconds must be numbers"
        return out
    conn = connect(data)
    if conn is None:
        out["error"] = "no read copy yet: %s (the service `store` publishes it)" % (folder_of(data) / "read.db")
        return out
    deadline = time.monotonic() + seconds
    try:
        conn.execute("PRAGMA query_only = 1")
        conn.set_authorizer(reads_only)
        conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 1000)
        cursor = conn.execute(body)
        out["columns"] = [column[0] for column in cursor.description or ()]
        rows = cursor.fetchmany(limit + 1)
        out["cut"] = len(rows) > limit
        out["rows"] = [tuple(row) for row in rows[:limit]]
    except (sqlite3.Error, sqlite3.Warning, OverflowError, MemoryError) as error:
        said = str(error).splitlines()[0] if str(error) else type(error).__name__
        if "one statement at a time" in said:
            said = "refused: only one statement is taken (%s)" % said
        elif "interrupted" in said:
            said = "stopped: the statement ran longer than %g s" % seconds
        elif "not authorized" in said or "prohibited" in said:
            said = "refused: the statement would do more than read (%s)" % said
        out["error"] = "%s: %s" % (type(error).__name__, said) if not said.startswith(("stopped", "refused")) else said
        out["columns"], out["rows"] = [], []
    finally:
        conn.close()
    return out


def status(data, now=None):
    """The lines of `status`, from the read copy."""
    now = time.time() if now is None else now
    conn = connect(data)
    if conn is None:
        return ["no read copy yet: %s" % (folder_of(data) / "read.db")]
    folder = folder_of(data)
    try:
        lines = ["read copy %s: %.2f MB, written %s, %d s old" % (
            folder / "read.db", (folder / "read.db").stat().st_size / 1e6, stamp((folder / "read.db").stat().st_mtime),
            now - (folder / "read.db").stat().st_mtime)]
        for table, column in NEWEST:
            count, newest = conn.execute("SELECT COUNT(*), MAX(%s) FROM %s" % (column, table)).fetchone()
            lines.append("  %-12s %9d rows   newest %s" % (table, count, stamp(newest) if newest is not None else "--"))
        for record, offset in conn.execute("SELECT record, offset FROM cursor ORDER BY record"):
            lines.append("  cursor %-24s at byte %d" % (record, offset))
        sealed = conn.execute("SELECT key, value FROM meta WHERE key LIKE 'sealed.%' ORDER BY key").fetchall()
        lines.append("  raw rows kept from: %s" % (", ".join("%s %s" % (k[7:], stamp(v)) for k, v in sealed) or "all"))
        lines += snapshot_status(conn, now)
    finally:
        conn.close()
    return lines


def snapshot_status(conn, now):
    """The status lines of the snapshot tables: rows, and the age of the newest file each is read from; then every file that
    could not be read, with its note."""
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'source'").fetchone():
        return ["  snapshot tables: none yet (the store of this copy is older)"]
    newest = {loader: (files, mtime) for loader, files, mtime in conn.execute("SELECT loader, COUNT(*), MAX(mtime) FROM source GROUP BY loader")}
    lines = ["  snapshot tables (what the files say now): rows, and the newest file each is read from"]
    for name, _columns, _key in SNAPSHOT:
        count = conn.execute("SELECT COUNT(*) FROM %s" % name).fetchone()[0]
        seen = [newest[loader] for loader in FED.get(name, ()) if loader in newest]
        files, mtime = sum(f for f, _m in seen), max((m for _f, m in seen if m is not None), default=None)
        lines.append("  %-18s %9d rows   %s" % (name, count, "newest source %s, %s old, %d files" % (stamp(mtime), ago(now - mtime), files)
                                                            if mtime is not None else "no source read"))
    for name, note in conn.execute("SELECT name, note FROM source WHERE note <> '' ORDER BY name"):
        lines.append("  not read: %s: %s" % (name, note))
    return lines


def ago(seconds):
    seconds = max(0, int(seconds))
    return "%d s" % seconds if seconds < 120 else "%d min" % (seconds // 60) if seconds < 7200 else "%.1f h" % (seconds / 3600.0)


def main(argv):
    parser = argparse.ArgumentParser(description="The fleet's history store.")
    parser.add_argument("verb", choices=("serve", "once", "status", "recount"))
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--root", default=str(ROOT), help="the repository's game/ folder")
    parser.add_argument("--every", type=int, default=EVERY)
    parser.add_argument("--keep-days", type=float, default=KEEP_DAYS)
    args = parser.parse_args(argv)
    if args.verb == "status":
        print("\n".join(status(args.data)))
        return 0
    if args.verb == "recount":                                  # the writer does it: this only asks (one writer of live.db)
        folder_of(args.data).mkdir(parents=True, exist_ok=True)
        (folder_of(args.data) / "recount").write_text(stamp(time.time()) + "\n", encoding="ascii")
        print("store: asked; the writer's next pass counts every raw run kept again and sums its hours again")
        return 0
    if args.verb == "once":
        holder = lease(args.data)
        if holder:
            print("store: not run, the writer's lease is held by %s" % holder)
            return 1
        try:
            print(said(one_pass(args.data, keep_days=args.keep_days, root=args.root)) or "store: nothing new")
        finally:
            release(args.data)
        return 0
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))      # a stop runs the `finally` below: the lease goes
    print("%s store: a pass every %d s into %s, raw rows kept %g days, copy for readers %s" % (
        stamp(time.time()), args.every, folder_of(args.data) / "live.db", args.keep_days, folder_of(args.data) / "read.db"), flush=True)
    waiting = None
    try:
        while True:
            try:
                holder = lease(args.data)
                if holder:
                    if holder.split(",")[0] != waiting:
                        print("%s waiting: the writer's lease is held by %s" % (stamp(time.time()), holder), flush=True)
                    waiting = holder.split(",")[0]
                else:
                    waiting = None
                    line = said(one_pass(args.data, keep_days=args.keep_days, root=args.root))
                    if line:
                        print(stamp(time.time()), line, flush=True)
            except Exception as error:                 # one failed pass never ends the service
                print("%s pass failed: %s: %s" % (stamp(time.time()), type(error).__name__, error), flush=True)
            time.sleep(args.every)
    finally:
        release(args.data)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
