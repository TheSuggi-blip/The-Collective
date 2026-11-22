#!/usr/bin/env python3
"""stats.py -- the fleet's statistics, computed by the store into tables of its own: the fleet as one purse, what each division gives the whole, class capacity, where the ship-hours go, the reserve's days of supply, refill and regrowth, XP per ship-hour, the next upgrade of each ship, gather against buy, and control-chart alerts.

WHAT: the store (store.py) calls compute(conn, data, root, now) in every pass; compute decides by itself what is due
      and writes these tables into live.db (the read copy carries them to every reader):
        stats_money_hour    per whole UTC hour and division (and Fleet): the steady money of that hour by station/fleet.py's
                            own window(), the wallets at its end, the treasury when read near its end, the idle share of
                            the collector's minute samples; kept by retention.py (hourly, a backfill of history.json's hours).
                            Only the Fleet rows are summed over hours: a division's hour need not add up (see DESCRIPTIONS)
        stats_supply_hour   per hour and supply chain: its stock against its keep (view supply_status); kept by retention.py
        stats_time          every TIME_EVERY seconds: ships per role and state (own, other, once, shared, hand, docked,
                            space, offline) from the table ships; kept KEEP days
        stats_pilot_hour    per pilot, key and hour in which it moved: a skill (level, total XP) from ship_skills, or a
                            counter of the ship file (ships_lost, ships_destroyed, pirates_destroyed, damage_taken); kept
                            KEEP days. stats_pilot_last: each pilot's and key's newest reading, what the next is measured against
        stats_route_author  the first author of every route file (git log --diff-filter=A), read once per new file
        stats_refill        per bid, field and herd: what came back per hour, the median over its recovery events with n
        stats_figures       every figure of every view: view, subject, figure, hours, value (NULL: not measured), n, text
      The views (hive.py stats <view>; the tool fleet):
        kpi           the fleet as one purse over 1, 6, 24, 72 hours: throughput (income), operating expense (costs), steady
                      net, paid once, net of everything, net per ship-hour, the trend against the window before, the
                      change of wallets plus treasury, the reserve and the surplus at the best bid (surplus.py)
        contribution  per division: its own net, the income its route files enabled for every division, its service
        classes       per role: the places of its own class work open now against its ships; the spill
        time          per role and fleet: the share of ship-hours in own work, another class's, once, shared, by hand,
                      docked or in space without work, offline; the runs' hours by class beside it
        supply        per reserve good: held, needed, min and max (game/reserve.tsv when it carries them), net change
                      an hour over 24 h, days of supply, hours to target, the routes that feed it, ships on them
        gather        per reserve good: what a unit gathered cost against the best ask and the best bid
        xp            XP per ship-hour per role and skill and per route (24 h); per ship the hours to its next tier
        upgrades      per ship: hull, tier, Piloting, the Piloting and the hulls of the next tier, empty module slots
        alerts        the newest hour outside median +- MAD_K x MAD_SCALE x MAD of its own 7-day hourly history; first,
                      every base of ours that reads wrecked and every facility of ours not active (basewatch.py)
        refill        per bid, field and herd: units back an hour, median over events with n (hive.py refill reads it)
        status        when each part ran, its rows, its seconds, its last fault
RULES:
  - Money is the fleet's one rule: the windows of 1, 6 and 24 hours are the collector's own (fleet.json totals.rates,
    station/fleet.py rates(): what hive.py fleet prints); a longer window and every trend add whole hours, each the
    window() of station/fleet.py over that hour. A run's credits are routes.earned's (the store's runs, route_hour).
    The reserve and the surplus are surplus.py's; what a route carries is fill.carries; whose work a route is,
    workclass.py; a role, an owner, division.py. A cost is a positive number; net = income - costs.
  - Every figure carries its window (hours) and its n. What no record holds is NULL, printed `not measured`, with the
    record that would be needed in its text. A rate from fewer than MIN_N events or hours says so.
  - What is due: the samples once an hour (time samples every TIME_EVERY seconds), the figures every FIGURES_EVERY
    seconds, the route authors when a route file is new; every part in its own try and transaction: a part that fails
    is named in stats.status and never holds up another part nor the store's pass.
  - It reads the store's tables, the data folder and the repository (git log, read only); it writes only its own tables.
    It moves no ship, changes no plan and calls no game: nothing here acts by itself.
WHY:  Suggi, 2026-11-18: everything in the database, computed by itself; the fleet as a whole earns, and the divisions
      help each other. Every Admiral read the fleet with its own arithmetic and no figure said how many ships a class's
      own work employs, where the hours go, or how soon a good runs out (knowledge/planning-and-command.md).

USAGE:
  hive.py stats <view> [--hours N] [--member <Member>]     views: kpi, contribution, classes, time, supply, gather, xp,
                                                           upgrades, alerts, refill, status
  stats.py <view> [--hours N] [--member <Member>] [--data <dir>]    the same
  --hours N      kept for the tool's argument: the store computes kpi over 1, 6, 24 and 72 hours and contribution, time
                 and xp over 24; another N is said `not measured` and those are shown
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import hashlib
import importlib.util
import json
import os
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names
import division                                   # noqa: E402  roles, owners, members
import workclass                                  # noqa: E402  whose work a route is
import retention                                  # noqa: E402  r22: how long stats_money_hour, stats_supply_hour, stats_route_author stay

# store.py imports this file: store, hive, fill, dispatch, surplus and routes are imported inside the functions.

HOUR, DAY = 3600, 86400
TIME_EVERY = 600               # seconds between two samples of where the ships are (stats_time)
FIGURES_EVERY = 600            # seconds between two computations of the figures (the heavy part: about 2 s)
KEEP = {"stats_time": 30, "stats_pilot_hour": 8}     # days a sample table keeps; stats_money_hour, stats_supply_hour: retention.py RETAIN
WINDOWS = (1, 6, 24, 72)       # hours of the kpi
MIN_N = 24                     # hours of history an alert needs; a rate from fewer events says so
SPLIT_SPAN = 2.0               # hours: a skill reading spanning more is not split over routes (it would give each its mean)
MIN_SAMPLES = HOUR // TIME_EVERY   # samples of stats_time a ship-hour estimate needs (one hour of them)
MAD_K = 3                      # alerts: the band is median +- MAD_K x MAD_SCALE x MAD
MAD_SCALE = 1.4826             # the Hampel identifier: 1.4826 x MAD estimates the standard deviation of normal data
                               # (1.0 gives the raw median +- 3 x MAD = 2.02 sigma, which flags about 4.3 % of normal hours)
FRESH = 3 * HOUR               # Intel's service: a place read within this counts as fresh
COUNTERS = ("ships_lost", "ships_destroyed", "pirates_destroyed", "damage_taken")   # the ship file's counters sampled
READ = "read_hours"            # the key of a pilot's reading itself: its gain is the hours since the pilot's reading before
NOT_XP = COUNTERS + (READ,)
STATES = ("own", "other", "once", "shared", "hand", "docked", "space", "offline")
STATE_TEXT = {"own": "own-class work", "other": "another class's work", "once": "missions paid once", "shared": "shared work (sell, craft, fit its own stores)",
              "hand": "by hand or an engine goal, no route", "docked": "docked without work", "space": "in space without work", "offline": "offline"}
VIEWS_SHOWN = ("kpi", "contribution", "classes", "time", "supply", "gather", "xp", "upgrades", "alerts", "refill", "status")

SCHEMA = """
CREATE TABLE IF NOT EXISTS stats_money_hour (hour INTEGER NOT NULL, division TEXT NOT NULL, minutes REAL, income REAL, costs REAL, net REAL,
  rewards REAL, bought REAL, once REAL, total REAL, wallets REAL, fuel REAL, repair REAL, ships INTEGER, wallets_end REAL, treasury REAL,
  idle REAL, samples INTEGER, t INTEGER NOT NULL, PRIMARY KEY (hour, division));
CREATE TABLE IF NOT EXISTS stats_supply_hour (hour INTEGER NOT NULL, chain TEXT NOT NULL, item TEXT, place TEXT, stock INTEGER, keep INTEGER,
  status TEXT, t INTEGER NOT NULL, PRIMARY KEY (hour, chain));
CREATE TABLE IF NOT EXISTS stats_time (t INTEGER NOT NULL, role TEXT NOT NULL, state TEXT NOT NULL, ships INTEGER NOT NULL,
  PRIMARY KEY (t, role, state));
CREATE TABLE IF NOT EXISTS stats_pilot_hour (hour INTEGER NOT NULL, pilot TEXT NOT NULL, role TEXT, key TEXT NOT NULL, level INTEGER,
  value REAL, gain REAL, t INTEGER NOT NULL, PRIMARY KEY (hour, pilot, key));
CREATE INDEX IF NOT EXISTS stats_pilot_hour_key ON stats_pilot_hour (key, hour);
CREATE TABLE IF NOT EXISTS stats_pilot_last (pilot TEXT NOT NULL, key TEXT NOT NULL, level INTEGER, value REAL, t INTEGER NOT NULL,
  PRIMARY KEY (pilot, key));
CREATE TABLE IF NOT EXISTS stats_route_author (route TEXT PRIMARY KEY, author TEXT, member TEXT, division TEXT, added INTEGER, t INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS stats_refill (kind TEXT NOT NULL, place TEXT NOT NULL, what TEXT NOT NULL, now REAL, events INTEGER, median REAL,
  q1 REAL, q3 REAL, ours INTEGER, ours_median REAL, per_hour REAL, taken_per_hour REAL, hours REAL, readings INTEGER, t INTEGER NOT NULL,
  PRIMARY KEY (kind, place, what));
CREATE TABLE IF NOT EXISTS stats_figures (view TEXT NOT NULL, subject TEXT NOT NULL, figure TEXT NOT NULL, hours REAL NOT NULL, value REAL,
  n INTEGER, text TEXT, t INTEGER NOT NULL, PRIMARY KEY (view, subject, figure, hours));
"""
TABLES = ("stats_money_hour", "stats_supply_hour", "stats_time", "stats_pilot_hour", "stats_pilot_last", "stats_route_author", "stats_refill",
          "stats_figures")

DESCRIPTIONS = {
    "stats_money_hour": "history (stats.py): per whole UTC hour and division (Fleet: the whole) the steady money of that hour by station/fleet.py's "
                        "window(): income, costs, net (= income - costs), paid once (rewards - bought), total, per hour over `minutes`; wallets at the "
                        "hour's end, the treasury when read near it, the idle share of the collector's minute samples (Fleet); kept " + retention.short("stats_money_hour") + ". The Fleet "
                        "rows add up to the collector's window over a longer span; a division's rows of one hour need not add up to the Fleet's (a "
                        "move between our purses whose two sides fall into different hours): sum the Fleet rows only",
    "stats_supply_hour": "history (stats.py): per hour and supply chain its stock against its keep and its status (view supply_status); kept %s"
                         % retention.short("stats_supply_hour"),
    "stats_time": "history (stats.py): every 10 minutes the ships per role and state: own, other (another class's work), once, shared, hand, "
                  "docked, space (without work), offline; a sample is the state at that moment (work sampling); kept 30 days",
    "stats_pilot_hour": "history (stats.py): per pilot, key and UTC hour in which it moved: a skill's level and total XP (value) and the gain since "
                        "the pilot's reading before, or a counter of its ship file (ships_lost, ships_destroyed, pirates_destroyed, damage_taken); kept 8 days",
    "stats_pilot_last": "state (stats.py): each pilot's and key's newest reading, against which the next hour's gain is measured",
    "stats_route_author": "state (stats.py): the first author of every route file (git log --diff-filter=A) with its member and division: whose "
                          "work a route's income is (view contribution)",
    "stats_refill": "now (stats.py): per bid (base, item), field and herd (system:poi, what) what came back an hour: the median over its recovery "
                    "events (a take, then a rise before the next take) with q1, q3 and n, the same for the takes of our own sales (ours), and "
                    "hive.py's least-that-is-sure sum over the hours watched (per_hour); hive.py refill prints it",
    "stats_figures": "now (stats.py): every figure of every stats view (kpi, contribution, classes, time, supply, gather, xp, upgrades, alerts): "
                     "view, subject, figure, hours (its window, 0 for none), value (NULL: not measured), n (the records behind it), text (what it "
                     "rests on), t (computed); hive.py stats <view> prints them",
}
EXAMPLES = {
    "stats_money_hour": (("The fleet's steady net hour by hour", "SELECT datetime(hour, 'unixepoch') AS hour, ROUND(net) AS net, ROUND(income) AS income, "
                          "ROUND(costs) AS costs, ROUND(once) AS paid_once FROM stats_money_hour WHERE division = 'Fleet' ORDER BY hour DESC LIMIT 24"),
                         ("The fleet's steady credits over the last 72 whole hours", "SELECT ROUND(SUM(net * minutes / 60.0)) AS net_credits, "
                          "COUNT(*) AS hours FROM stats_money_hour WHERE division = 'Fleet' AND hour >= strftime('%s', 'now') - 72 * 3600"),
                         ("The idle share of the fleet hour by hour", "SELECT datetime(hour, 'unixepoch'), ROUND(100 * idle, 1) AS idle_pct, samples "
                          "FROM stats_money_hour WHERE division = 'Fleet' ORDER BY hour DESC LIMIT 24")),
    "stats_supply_hour": (("The share of hours each chain stood at its keep", "SELECT chain, item, ROUND(100.0 * SUM(stock >= keep) / COUNT(*)) AS pct_ok, "
                           "COUNT(*) AS hours FROM stats_supply_hour GROUP BY chain"),
                          ("One chain hour by hour", "SELECT datetime(hour, 'unixepoch'), stock, keep, status FROM stats_supply_hour ORDER BY chain, hour DESC LIMIT 24"),
                          ("Hours a chain stood short", "SELECT chain, COUNT(*) FROM stats_supply_hour WHERE status = 'short' GROUP BY chain")),
    "stats_time": (("Where the fleet's ship-hours went in the last 24 hours", "SELECT state, SUM(ships) AS seen, ROUND(100.0 * SUM(ships) / "
                    "(SELECT SUM(ships) FROM stats_time WHERE t >= strftime('%s', 'now') - 86400), 1) AS pct FROM stats_time "
                    "WHERE t >= strftime('%s', 'now') - 86400 GROUP BY state ORDER BY 2 DESC"),
                   ("The traders' states in the newest sample", "SELECT state, ships FROM stats_time WHERE role = 'trader' AND t = (SELECT MAX(t) FROM stats_time)"),
                   ("Ships without work per sample", "SELECT datetime(t, 'unixepoch'), SUM(ships) FROM stats_time WHERE state IN ('docked', 'space') "
                    "GROUP BY t ORDER BY t DESC LIMIT 24")),
    "stats_pilot_hour": (("XP gained per skill in the last 24 hours", "SELECT key, SUM(gain) FROM stats_pilot_hour WHERE gain > 0 AND key NOT IN "
                          "('ships_lost', 'ships_destroyed', 'pirates_destroyed', 'damage_taken') AND hour >= strftime('%s', 'now') - 86400 GROUP BY key ORDER BY 2 DESC"),
                         ("Ships lost per role in the last 24 hours", "SELECT role, SUM(gain) FROM stats_pilot_hour WHERE key = 'ships_lost' AND gain > 0 "
                          "AND hour >= strftime('%s', 'now') - 86400 GROUP BY role"),
                         ("Piloting XP of one pilot hour by hour", "SELECT datetime(hour, 'unixepoch'), level, value, gain FROM stats_pilot_hour "
                          "WHERE key = 'piloting' ORDER BY pilot, hour DESC LIMIT 24")),
    "stats_pilot_last": (("The highest Piloting levels", "SELECT pilot, level, value FROM stats_pilot_last WHERE key = 'piloting' ORDER BY level DESC, value DESC LIMIT 10"),
                         ("Pilots per Piloting level", "SELECT level, COUNT(*) FROM stats_pilot_last WHERE key = 'piloting' GROUP BY level ORDER BY level"),
                         ("When each pilot was last read", "SELECT pilot, datetime(MAX(t), 'unixepoch') FROM stats_pilot_last GROUP BY pilot ORDER BY 2 LIMIT 20")),
    "stats_route_author": (("Route files per division", "SELECT division, COUNT(*) FROM stats_route_author GROUP BY division ORDER BY 2 DESC"),
                           ("Who wrote the routes that earned most in 24 hours", "SELECT a.route, a.division, ROUND(SUM(h.credits)) FROM route_hour h JOIN "
                            "stats_route_author a ON a.route = h.route WHERE h.hour >= strftime('%s', 'now') - 86400 GROUP BY a.route ORDER BY 3 DESC LIMIT 10"),
                           ("Route files written by no member", "SELECT route, author FROM stats_route_author WHERE member IS NULL")),
    "stats_refill": (("Bids that come back fastest after a take", "SELECT place AS base, what AS item, median, events, ours, hours FROM stats_refill "
                      "WHERE kind = 'bid' AND events > 0 ORDER BY median DESC LIMIT 20"),
                     ("Fields that grow back", "SELECT place, what, median, events, per_hour FROM stats_refill WHERE kind = 'field' AND events > 0 ORDER BY median DESC LIMIT 20"),
                     ("Herds and how fast they regrow", "SELECT place, what, now, median, events FROM stats_refill WHERE kind = 'herd' ORDER BY median DESC LIMIT 20")),
    "stats_figures": (("The fleet's kpi over 24 hours", "SELECT figure, value, n, text FROM stats_figures WHERE view = 'kpi' AND hours = 24"),
                      ("What each division enabled for the others", "SELECT subject, value, n FROM stats_figures WHERE view = 'contribution' "
                       "AND figure = 'enabled_others' ORDER BY value DESC"),
                      ("Every alert that is raised", "SELECT subject, value, text FROM stats_figures WHERE view = 'alerts' AND figure = 'alert' AND n > 0 "
                       "AND text LIKE 'OUT%'")),
}

num = lambda value: format(int(round(value)), ",") if isinstance(value, (int, float)) and not isinstance(value, bool) else "--"


def stamp(t):
    return time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(t)) if t else "never"


def epoch(text):
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return None


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.loads(handle.read())
    except (OSError, ValueError):
        return default


def median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def quartiles(values):
    """(q1, median, q3) of a list; None for an empty one; with one value all three are it."""
    values = sorted(v for v in values if v is not None)
    if not values:
        return None
    if len(values) == 1:
        return values[0], values[0], values[0]
    q = statistics.quantiles(values, n=4, method="inclusive")
    return q[0], q[1], q[2]


def mad(values):
    """The median absolute deviation from the median (NIST handbook 1.3.5.6), unscaled."""
    m = median(values)
    return None if m is None else statistics.median(abs(v - m) for v in values)


def division_of(member):
    return board.NAMES.get(member, member)


ROLE_MEMO = {}                 # (pilot, data) -> role: emptied at every compute (a flagship may change role)
CACHE = {}                     # the collector's money rule, the catalog's XP tables, the reserve of this computation


def role_of(pilot, data):
    """division.role_of, read once per pilot and pass (it reads the flagships' file at every call)."""
    key = (pilot, str(data))
    if key not in ROLE_MEMO:
        ROLE_MEMO[key] = division.role_of(pilot, data) or ""
    return ROLE_MEMO[key]


def owner_division(pilot, data):
    return division_of(division.ROLES.get(role_of(pilot, data), "Unity"))


def meta_get(conn, key, default=None):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else default


def meta_put(conn, key, value):
    conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", (key, value))


def has_table(conn, name):
    return conn.execute("SELECT 1 FROM sqlite_master WHERE name = ?", (name,)).fetchone() is not None


def write_figures(conn, view, rows, now):
    """Replace one view's rows of stats_figures: rows are (subject, figure, hours, value, n, text)."""
    conn.execute("DELETE FROM stats_figures WHERE view = ?", (view,))
    conn.executemany("INSERT OR REPLACE INTO stats_figures VALUES (?,?,?,?,?,?,?,?)",
                     [(view, str(s), f, float(h), v if v is None else float(v), n, t, int(now)) for s, f, h, v, n, t in rows])
    return len(rows)


def load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---- the money: station/fleet.py's own window over each whole hour

def collector(root):
    """station/fleet.py of this repository (the collector's money rule), loaded by path once per process."""
    if "collector" not in CACHE:
        CACHE["collector"] = load_by_path("station_fleet_rule", Path(root).resolve().parent / "station" / "fleet.py")
    return CACHE["collector"]


def money_records(data, rule, now):
    """What window() reads beside history.json, from the collector's own files under data/fleet."""
    folder = Path(data) / "fleet"
    rule.load_flagships(folder)          # station/fleet.py division_of: the flagships stand in Command, not in Unassigned
    one = read_json(folder / "onetime.json", [])
    gifts = rule.read_gifts(folder / "gifts.jsonl")
    seeds = read_json(folder / "seed.json", {})
    presence = rule.read_presence(folder / "presence.jsonl")
    moves = rule.read_moves(folder / "moves.jsonl")
    regroups = rule.read_regroup(folder / "regroup.jsonl")
    found = rule.sides_of(gifts, one)
    sides = (found, rule.read_times(found, moves[0], moves[1], now))
    return one if isinstance(one, list) else [], gifts, seeds if isinstance(seeds, dict) else {}, presence, sides, regroups


def hour_slice(history, hour):
    """The samples of one whole hour, chained to the next: from the last sample at or before its start to the last at or
    before its end; None when they do not span 50 minutes (a gap, or the record begins inside the hour)."""
    start = [h for h in history if h[0] <= hour]
    if not start:
        return None
    a = start[-1]
    inside = [h for h in history if a[0] <= h[0] <= hour + HOUR]
    if len(inside) < 2 or inside[-1][0] - a[0] < 3000 or hour - a[0] > 300:
        return None
    return inside


def money_rows(rule, piece, records, hour, now, treasury):
    """The rows of stats_money_hour of one hour: the Fleet's and each division's, from window() over the slice."""
    one, gifts, seeds, presence, sides, regroups = records
    b = piece[-1]
    w = rule.window(piece, b[0], b[0] - piece[0][0], one, gifts, seeds, presence, sides, regroups)
    if w is None:
        return []
    shares = [x[8]["w"] for x in piece[1:] if len(x) > 8 and isinstance(x[8], dict) and isinstance(x[8].get("w"), list) and sum(x[8]["w"]) > 0]
    idle = sum((s[1] + s[2]) / float(sum(s)) for s in shares) / len(shares) if shares else None

    def row(name, f, ships, wallets_end, treasury_now, idle_now, samples):
        return (hour, name, f.get("minutes", w["minutes"]), f.get("income_per_hour"), f.get("costs_per_hour"), f.get("cph"), f.get("rewards_per_hour"),
                f.get("bought_once_per_hour"), f.get("one_time_per_hour"), f.get("total_per_hour"), f.get("wallets_per_hour"), f.get("fuel_cr_per_hour"),
                f.get("repair_cr_per_hour"), ships, wallets_end, treasury_now, idle_now, samples, int(now))
    out = [row("Fleet", w, b[2], b[1], treasury, idle, len(shares))]
    for name, f in sorted((w.get("divisions") or {}).items()):
        out.append(row(name, dict(f, minutes=w["minutes"]), (b[7].get(name) or [0, 0])[0], (b[7].get(name) or [0, 0])[1], None, None, None))
    return out


def sample_money(conn, data, root, now):
    """Every whole hour history.json spans and stats_money_hour lacks (a backfill on the first run): its rows."""
    history = read_json(Path(data) / "fleet" / "history.json", [])
    history = [h for h in history if isinstance(h, list) and len(h) >= 8 and isinstance(h[0], (int, float))] if isinstance(history, list) else []
    if len(history) < 2:
        return 0
    done = {h for (h,) in conn.execute("SELECT DISTINCT hour FROM stats_money_hour")}
    last = int(history[-1][0]) // HOUR * HOUR
    todo = [h for h in range(int(history[0][0]) // HOUR * HOUR, last, HOUR) if h not in done and h + HOUR <= history[-1][0]]
    if not todo:
        return 0
    rule = collector(root)
    records = money_records(data, rule, now)
    state = read_json(Path(data) / "empire" / "empire.json", {})
    faction = state.get("faction") if isinstance(state, dict) and isinstance(state.get("faction"), dict) else {}
    read_at, treasury = epoch(state.get("written_at")) if isinstance(state, dict) else None, faction.get("treasury")
    rows = []
    for hour in todo:
        piece = hour_slice(history, hour)
        if piece is None:
            continue
        near = treasury if isinstance(treasury, (int, float)) and read_at and abs(read_at - (hour + HOUR)) <= 1800 else None
        rows += money_rows(rule, piece, records, hour, now, near)
    conn.executemany("INSERT OR REPLACE INTO stats_money_hour VALUES (%s)" % ",".join("?" * 19), rows)
    return len(rows)


def tiled(conn, name, start, end):
    """{figure: credits per hour} of the whole hours [start, end) of stats_money_hour, weighted by their minutes, with
    `hours` (on record) and `n` (rows); None when no hour is on record."""
    rows = conn.execute("SELECT minutes, income, costs, net, once, total, fuel, repair, ships FROM stats_money_hour WHERE division = ? AND hour >= ? "
                        "AND hour < ?", (name, start, end)).fetchall()
    rows = [r for r in rows if r[0]]
    if not rows:
        return None
    minutes = sum(r[0] for r in rows)
    out = {"hours": minutes / 60.0, "n": len(rows)}
    for index, key in enumerate(("income", "costs", "net", "once", "total", "fuel", "repair"), 1):
        out[key] = sum((r[index] or 0) * r[0] for r in rows) / minutes
    ships = [r[8] for r in rows if r[8]]
    out["per_ship"] = out["net"] / (sum(ships) / len(ships)) if ships else None
    return out


# ---- the samples: where the ships are, the pilots' skills and counters, the supply chains

def ship_state(role, status, flies, activity, docked, routes):
    """One ship's state now: own, other, once, shared (its route's class against its role, workclass.py), hand, docked,
    space or offline."""
    if status and status != "connected":
        return "offline"
    if flies and not flies.startswith("hand "):
        kind, _, rest = flies.partition(" ")
        if kind == "census":
            return "own" if workclass.own(role, {"kind": "census"}, "census") else "other"
        route = routes.get(rest)
        if route is None:
            return "other"
        if route.get("park"):
            return "docked"
        cls = workclass.work_class(route, rest)
        if cls == "once":
            return "once"
        if cls in workclass.SHARED:
            return "shared"
        return "own" if workclass.own(role, route, rest) else "other"
    if flies or (activity and activity != "idle"):
        return "hand"
    return "docked" if docked else "space"


def sample_time(conn, root, now):
    """One sample of stats_time from the table ships: ships per role and state. 0 rows while no ship is listed."""
    routes = route_files(root)
    count = Counter()
    for _pilot, role, status, flies, activity, docked in conn.execute("SELECT pilot, role, status, flies, activity, docked FROM ships"):
        count[(role or "?", ship_state(role or "", status, flies, activity, docked, routes))] += 1
    conn.executemany("INSERT OR REPLACE INTO stats_time VALUES (?,?,?,?)", [(int(now), role, state, n) for (role, state), n in sorted(count.items())])
    return len(count)


def xp_tables(data):
    """{skill: [XP of each level]} from the newest catalog (hive.py's craftbook_file rule), cached by the file's time."""
    import hive
    path = hive.craftbook_file(data)
    try:
        mark = (str(path), os.stat(path).st_mtime)
    except OSError:
        return {}
    if CACHE.get("xp_mark") != mark:
        cat = read_json(path, {})
        CACHE["xp_tables"] = {s.get("id"): s.get("xp_per_level") or [] for s in cat.get("skills") or [] if isinstance(s, dict)} if isinstance(cat, dict) else {}
        CACHE["xp_mark"] = mark
    return CACHE["xp_tables"]


def total_xp(tables, skill, level, xp):
    """A skill's whole XP: the XP of every level below its own plus the XP into its level (hive.py show_levels' rule)."""
    return sum((tables.get(skill) or [])[:int(level or 0)]) + (xp or 0)


def sample_pilots(conn, data, now):
    """The hour's sample of every pilot's skills (ship_skills) and counters (fleet/ships/<pilot>.json): a row of
    stats_pilot_hour for each key that moved since the pilot's reading before (gain), or that is read for the first
    time (gain NULL); the key read_hours (value: the reading's time in hours) always moves: its gain is the hours the
    pilot's other gains of that row's hour span, the denominator of every XP rate. stats_pilot_last keeps the newest
    reading."""
    import dispatch
    tables, hour = xp_tables(data), int(now) // HOUR * HOUR
    roles = dict(conn.execute("SELECT pilot, role FROM ships"))
    found = {(pilot, READ): (None, now / 3600.0) for pilot in roles}      # every pilot read: the hours between two readings
    for pilot, skill, level, xp in conn.execute("SELECT pilot, skill, level, xp FROM ship_skills"):
        found[(pilot, skill)] = (level, total_xp(tables, skill, level, xp))
    for pilot in roles:
        detail = read_json(Path(data) / "fleet" / "ships" / dispatch.ship_file(pilot), {})
        counts = detail.get("stats") if isinstance(detail, dict) and isinstance(detail.get("stats"), dict) else {}
        for key in COUNTERS:
            if isinstance(counts.get(key), (int, float)):
                found[(pilot, key)] = (None, counts[key])
    last = {(p, k): (lv, v) for p, k, lv, v in conn.execute("SELECT pilot, key, level, value FROM stats_pilot_last")}
    rows = []
    for (pilot, key), (level, value) in found.items():
        before = last.get((pilot, key))
        if before is None and key != READ and (pilot, READ) in last:
            before = (0, 0)                        # a skill or counter a pilot read before did not list yet: it rose from 0
        if before is None or before[1] != value or before[0] != level:
            rows.append((hour, pilot, roles.get(pilot) or role_of(pilot, data), key, level, value, None if before is None else value - before[1], int(now)))
    conn.executemany("INSERT OR REPLACE INTO stats_pilot_hour VALUES (?,?,?,?,?,?,?,?)", rows)
    conn.executemany("INSERT OR REPLACE INTO stats_pilot_last VALUES (?,?,?,?,?)", [(p, k, lv, v, int(now)) for (p, k), (lv, v) in found.items()])
    return len(rows)


def sample_supply(conn, now):
    """The hour's sample of every supply chain (view supply_status): stock, keep, status."""
    if not has_table(conn, "supply_status"):
        return 0
    hour = int(now) // HOUR * HOUR
    rows = [(hour, chain, item, place, stock, keep, status, int(now)) for chain, item, place, stock, keep, status in
            conn.execute("SELECT chain, item, place, stock, keep, status FROM supply_status WHERE chain IS NOT NULL")]
    conn.executemany("INSERT OR REPLACE INTO stats_supply_hour VALUES (?,?,?,?,?,?,?,?)", rows)
    return len(rows)


def git_authors(root):
    """{route id: (author, epoch)} of the commit that first added game/routes/<id>.json, by one `git log` of the clone."""
    import hive
    repo = Path(root).resolve().parent
    out = {}
    author, when = None, None
    for line in hive.git_lines(repo, "log", "--diff-filter=A", "--reverse", "--name-only", "--format=@%an|%ct", "--", "game/routes"):
        if line.startswith("@") and "|" in line:
            author, when = line[1:].rsplit("|", 1)
        elif line.startswith("game/routes/") and line.endswith(".json") and line.count("/") == 2 and author:
            out.setdefault(Path(line).stem, (author, int(when) if when.isdigit() else None))
    return out


def sample_authors(conn, root, now):
    """stats_route_author for the route files it does not know yet (one git log when there is one); a file the log does
    not name (not committed yet, or no git where the store runs) is kept with no author and asked again after an hour."""
    known = {r for (r,) in conn.execute("SELECT route FROM stats_route_author WHERE author IS NOT NULL OR t >= ?", (int(now - HOUR),))}
    new = [r for (r,) in conn.execute("SELECT id FROM routes") if r not in known]     # a file git does not know yet: asked again an hour later
    if not new:
        return 0
    found = git_authors(root)
    names = {m.lower(): m for m in division.MEMBERS}
    rows = []
    for rid in new:
        author, added = found.get(rid, (None, None))
        member = names.get(str(author or "").lower())
        rows.append((rid, author, member, division_of(member) if member else "none", added, int(now)))
    conn.executemany("INSERT OR REPLACE INTO stats_route_author VALUES (?,?,?,?,?,?)", rows)
    return len(rows)


# ---- refill and regrowth

def recoveries(seen, step):
    """[(rate per hour, the take's time)] of a series [(t, ...)]: an event begins at a take (step() says (added, taken)
    of two readings) and its rate is the units that came back before the next take over the hours from the take to the
    last rise seen. A take with no rise after it is no event (no reading says when the book was read)."""
    out, start, added, last = [], None, 0, None
    for a, b in zip(seen, seen[1:]):
        up, down = step(a, b)
        if down > 0:
            if start is not None and added > 0 and last > start:
                out.append((added * 3600.0 / (last - start), start))
            start, added, last = b[0], 0, None
        elif up > 0 and start is not None:
            added, last = added + up, b[0]
    if start is not None and added > 0 and last > start:
        out.append((added * 3600.0 / (last - start), start))
    return out


def our_sales(conn, routes, since):
    """{(base, item): [(start, end)]} of our runs that sold an item at a station, from the store's raw runs: a mine
    route's station or sell_at, a circuit stop's `at` with a sell list."""
    out = defaultdict(list)
    for route, t, minutes, line in conn.execute("SELECT route, t, minutes, row FROM runs WHERE t >= ? AND row LIKE '%\"sold\"%'", (since,)):
        try:
            row = json.loads(line)
        except (TypeError, ValueError):
            continue
        sold = row.get("sold") if isinstance(row.get("sold"), dict) else {}
        spec = routes.get(route) or {}
        bases = [str(spec.get(k) or "").split(":")[-1] for k in ("station", "sell_at") if spec.get(k)]
        bases += [str(s.get("at") or "").split(":")[-1] for s in spec.get("stops") or [] if isinstance(s, dict) and s.get("sell")]
        for item in sold:
            for base in set(b for b in bases if b):
                out[(base, item)].append((t, t + (minutes or 0) * 60))
    return out


def compute_refill(conn, root, now):
    """stats_refill from the store's raw rows (moves, readings: their last KEEP_DAYS) by hive.py's own arithmetic
    (bid_moves: a best bid is one step of a ladder; moves: rises and falls of a count)."""
    import hive
    routes = route_files(root)
    rows = []
    bids = defaultdict(list)
    for base, item, t, units, bid in conn.execute("SELECT base, item, t, bid_qty, bid FROM moves WHERE bid_qty IS NOT NULL ORDER BY base, item, t"):
        bids[(base, item)].append((t, units, bid or 0))
    since = min((s[0][0] for s in bids.values()), default=int(now))
    sales = our_sales(conn, routes, since - DAY)
    step_bid = lambda a, b: hive.bid_moves([a, b])
    for (base, item), seen in bids.items():
        if len(seen) < 2:
            continue
        added, taken = hive.bid_moves(seen)
        hours = (seen[-1][0] - seen[0][0]) / 3600.0
        events = recoveries(seen, step_bid)
        prior = {b[0]: a[0] for a, b in zip(seen, seen[1:])}
        ours = [r for r, at in events if any(prior.get(at, at) <= end and start <= at for start, end in sales.get((base, item), ()))]
        q = quartiles([r for r, _at in events])
        rows.append(("bid", base, item, seen[-1][1], len(events), q[1] if q else None, q[0] if q else None, q[2] if q else None, len(ours),
                     median(ours), added / hours if hours >= 0.5 else None, taken / hours if hours >= 0.5 else None, hours, len(seen), int(now)))
    counts = defaultdict(list)
    for system, poi, what, kind, amount, t in conn.execute("SELECT system, poi, what, kind, amount, t FROM readings ORDER BY system, poi, what, t"):
        counts[(kind, "%s:%s" % (system, poi), what)].append((t, amount))
    step_count = lambda a, b: (max(0, b[1] - a[1]), max(0, a[1] - b[1]))
    for (kind, place, what), seen in counts.items():
        if len(seen) < 2:
            continue
        added, taken, hours = hive.moves(seen)
        rises = [(b[1] - a[1]) * 3600.0 / (b[0] - a[0]) for a, b in zip(seen, seen[1:]) if b[1] > a[1] and b[0] > a[0]]
        q = quartiles(rises)
        rows.append((kind or "?", place, what, seen[-1][1], len(rises), q[1] if q else None, q[0] if q else None, q[2] if q else None, None, None,
                     added / hours if hours >= 0.5 else None, taken / hours if hours >= 0.5 else None, hours, len(seen), int(now)))
    conn.execute("DELETE FROM stats_refill")
    conn.executemany("INSERT OR REPLACE INTO stats_refill VALUES (%s)" % ",".join("?" * 15), rows)
    return len(rows)


# ---- the figures

def fleet_windows(data):
    """(fleet.json, its totals.rates.windows): the collector's own money (station/fleet.py rates), as hive.py fleet reads it."""
    fleet = read_json(Path(data) / "fleet" / "fleet.json", {})
    totals = fleet.get("totals") if isinstance(fleet, dict) and isinstance(fleet.get("totals"), dict) else {}
    return fleet if isinstance(fleet, dict) else {}, ((totals.get("rates") or {}).get("windows") or {}) if isinstance(totals.get("rates"), dict) else {}


KPI_KEYS = (("income", "income_per_hour"), ("costs", "costs_per_hour"), ("net", "cph"), ("once", "one_time_per_hour"), ("total", "total_per_hour"),
            ("purse", "purse_per_hour"), ("per_ship", "cph_per_ship"), ("fuel", "fuel_cr_per_hour"), ("repair", "repair_cr_per_hour"))


def figures_kpi(conn, data, root, now):
    fleet, windows = fleet_windows(data)
    source = "fleet.json of %s (station/fleet.py rates, as hive.py fleet)" % (fleet.get("updated_at") or "?")
    newest = conn.execute("SELECT MAX(hour) FROM stats_money_hour WHERE division = 'Fleet'").fetchone()[0]
    end = (newest + HOUR) if newest is not None else int(now) // HOUR * HOUR
    rows = []
    for hours in WINDOWS:
        w = windows.get("%dh" % hours) if hours in (1, 6, 24) else None
        if w:
            for key, field in KPI_KEYS:
                rows.append(("Fleet", key, hours, w.get(field), w.get("minutes"), source + ", minutes measured in n"))
        else:
            got = tiled(conn, "Fleet", end - hours * HOUR, end)
            for key, _field in KPI_KEYS:
                rows.append(("Fleet", key, hours, got.get(key) if got else None, got["n"] if got else 0,
                             ("the %d whole hours to %s of stats_money_hour (station/fleet.py window over each hour); n = hours on record" % (hours, stamp(end)))
                             if got else "not measured: no whole hour in stats_money_hour (station/fleet.py history.json, 48 hours) for this window"))
        before = tiled(conn, "Fleet", end - 2 * hours * HOUR, end - hours * HOUR)
        this = tiled(conn, "Fleet", end - hours * HOUR, end)
        rows.append(("Fleet", "net_tiled", hours, this["net"] if this else None, this["n"] if this else 0, "whole hours to %s" % stamp(end)))
        rows.append(("Fleet", "net_before", hours, before["net"] if before else None, before["n"] if before else 0,
                     "the %d whole hours before; n = hours on record" % hours))
        then = conn.execute("SELECT wallets_end, treasury FROM stats_money_hour WHERE division = 'Fleet' AND hour = ?", (end - hours * HOUR - HOUR,)).fetchone()
        last = conn.execute("SELECT wallets_end, treasury FROM stats_money_hour WHERE division = 'Fleet' AND hour = ?", (end - HOUR,)).fetchone()
        purse = (last[0] + last[1]) - (then[0] + then[1]) if then and last and None not in (then[0], then[1], last[0], last[1]) else None
        rows.append(("Fleet", "purse_change", hours, purse, 2 if purse is not None else 0,
                     "wallets + treasury at the end of the hour to %s against %d hours before" % (stamp(end), hours) if purse is not None else
                     "not measured: the treasury is read at both ends only once stats_money_hour holds a treasury reading %d hours apart "
                     "(empire.json, one reading at a time)" % hours))
    totals = fleet.get("totals") if isinstance(fleet.get("totals"), dict) else {}
    state = read_json(Path(data) / "empire" / "empire.json", {})
    faction = state.get("faction") if isinstance(state, dict) and isinstance(state.get("faction"), dict) else {}
    treasury = faction.get("treasury") if isinstance(faction.get("treasury"), (int, float)) else None
    rows += [("Fleet", "wallets", 0, totals.get("credits"), totals.get("ships"), source),
             ("Fleet", "treasury", 0, treasury, 1 if treasury is not None else 0, "empire.json of %s" % (state.get("written_at") if isinstance(state, dict) else "?")),
             ("Fleet", "purse", 0, (totals.get("credits") or 0) + treasury if treasury is not None and totals.get("credits") is not None else None, 1,
              "wallets + treasury (hive.py fleet, TREASURY line)")]
    one = read_json(Path(data) / "fleet" / "onetime.json", [])
    tax = [-r[3] for r in one if isinstance(r, list) and len(r) == 4 and r[2] == "Weekly tax" and isinstance(r[0], (int, float))
           and isinstance(r[3], (int, float)) and r[0] >= now - 24 * HOUR] if isinstance(one, list) else []
    rows.append(("Fleet", "tax", 24, sum(tax), len(tax), "weekly tax booked in onetime.json in 24 h (inside `paid once`, as hive.py fleet books it)"))
    rent = conn.execute("SELECT SUM(rent_per_cycle), COUNT(*) FROM faction_facilities").fetchone() if has_table(conn, "faction_facilities") else (None, 0)
    rows.append(("Fleet", "rent", 0, rent[0], rent[1], "rent per cycle of our faction's facilities (empire.json); its cycle's length is not measured"))
    try:
        res = reserve(data, root, now)
        worth = lambda units, r: min(units, r["bid_units"] or 0) * (r["bid"] or 0)
        kept = sum(worth(r["reserved"], r) for r in res["rows"])
        rows += [("Fleet", "surplus_worth", 0, res["totals"]["worth_at_bid"], res["totals"]["with_surplus"],
                  "surplus.py: the surplus at the best bid within its depth (storage book of %s)" % res["written"]),
                 ("Fleet", "reserve_worth", 0, kept, sum(1 for r in res["rows"] if r["reserved"]),
                  "the reserved units at the best bid within its depth, surplus.py's rows and rule"),
                 ("Fleet", "surplus_units", 0, res["totals"]["surplus"], res["totals"]["items"], "surplus.py totals"),
                 ("Fleet", "reserve_units", 0, res["totals"]["reserved"], res["totals"]["items"], "surplus.py totals")]
    except Exception as error:                     # noqa: BLE001  no reserve read: the other figures stand
        rows.append(("Fleet", "surplus_worth", 0, None, 0, "not measured: surplus.py failed: %s: %s" % (type(error).__name__, error)))
    return rows


def route_files(root):
    """dispatch.load_routes, once per computation (six parts read it)."""
    if "routes" not in CACHE:
        import dispatch
        CACHE["routes"] = dispatch.load_routes(root)
    return CACHE["routes"]


def reserve(data, root, now):
    """surplus.py's answer, once per computation (three views read it)."""
    if "reserve" not in CACHE:
        import surplus
        CACHE["reserve"] = surplus.surplus(data, str(Path(root).resolve().parent), now=now)
    return CACHE["reserve"]


def run_rows(conn, since):
    """The store's raw runs since a time: [(pilot, route, t, minutes, credits, readable, row dict)]."""
    out = []
    for pilot, route, t, minutes, credits, readable, line in conn.execute(
            "SELECT pilot, route, t, minutes, credits, readable, row FROM runs WHERE t >= ?", (since,)):
        try:
            row = json.loads(line)
        except (TypeError, ValueError):
            row = {}
        out.append((pilot, route, t, minutes or 0, credits or 0, readable, row if isinstance(row, dict) else {}))
    return out


def ship_hours(conn, since, until, roles=None):
    """({role: ship-hours}, samples) of a window by work sampling: the mean ships per sample of stats_time in the window
    times its hours. {} while fewer than MIN_SAMPLES samples fall into it (one hour of samples)."""
    out = Counter()
    found = conn.execute("SELECT COUNT(DISTINCT t) FROM stats_time WHERE t >= ? AND t <= ?", (since, until)).fetchone()[0]
    if found < MIN_SAMPLES:
        return out, found
    for role, ships in conn.execute("SELECT role, SUM(ships) FROM stats_time WHERE t >= ? AND t <= ? GROUP BY role", (since, until)):
        if roles is None or role in roles:
            out[role] += ships / float(found) * (until - since) / 3600.0
    return out, found


def run_class(route, rid, role):
    """own, other, once or shared: a run's route against the pilot's role (workclass.py)."""
    if not route:
        return "other"
    cls = workclass.work_class(route, rid)
    if cls == "once":
        return "once"
    if cls in workclass.SHARED:
        return "shared"
    return "own" if workclass.own(role, route, rid) else "other"


def figures_contribution(conn, data, root, now, hours):
    import store
    routes = route_files(root)
    fleet, windows = fleet_windows(data)
    since = int(now - hours * HOUR)
    rows = []
    names = [division_of(m) for m in division.MEMBERS]
    for name in names:
        for w in (1, 6, 24):
            f = ((windows.get("%dh" % w) or {}).get("divisions") or {}).get(name)
            rows.append((name, "own_net", w, f.get("cph") if f else None, (windows.get("%dh" % w) or {}).get("minutes"),
                         "fleet.json (station/fleet.py rates), steady net per hour" if f else "not measured: no window in fleet.json"))
        rows.append((name, "own_net", 72, None, 0, "not measured: the collector's window() over one hour does not add up per division (a move "
                     "between our purses whose sides fall into different hours), so whole hours cannot be summed per division; 72 h needs one "
                     "window over 72 h of samples (history.json holds about 48)"))
    authors = {r: (d, m) for r, d, m in conn.execute("SELECT route, division, member FROM stats_route_author")}
    rates = store.route_rates(conn, since)
    enabled, routes_of = Counter(), Counter()
    for rid, (_runs, _minutes, credits, _once, _rate) in rates.items():
        owner = (authors.get(rid) or ("not read", None))[0]
        enabled[owner] += credits or 0
        routes_of[owner] += 1
    others = Counter()
    runs = run_rows(conn, since)
    for pilot, rid, _t, _minutes, credits, readable, _row in runs:
        owner = (authors.get(rid) or ("not read", None))[0]
        if readable and owner_division(pilot, data) != owner:
            others[owner] += credits
    for name in names + ["none", "not read"]:
        if name in ("none", "not read") and not routes_of.get(name):
            continue
        rows.append((name, "enabled", hours, enabled.get(name, 0), routes_of.get(name, 0),
                     "steady credits (route_hour, routes.earned) of every ship on the routes whose file this division's Admiral wrote first"))
        rows.append((name, "enabled_others", hours, others.get(name, 0), routes_of.get(name, 0),
                     "of that, by ships of the other divisions (raw runs that read a wallet)"))
    rows += service_intel(conn, routes, now, since, hours)
    rows += service_logistics(conn, data, root, now, since, hours)
    rows += service_military(conn, data, runs, since, hours)
    rows += service_trade_mining(conn, data, routes, runs, now, since, hours)
    rows += service_handover(data, now, since, hours)     # orders ENT-064: what hunts and gathers hand over, at its worth
    return rows


def place_reads(conn):
    """({(system, poi): newest reading}, {base: newest book}) from readings and fields, and books."""
    places = {}
    for system, poi, t in conn.execute("SELECT system, poi, MAX(t) FROM readings GROUP BY system, poi"):
        places[(system, poi)] = t
    for system, poi, t in conn.execute("SELECT system, poi, MAX(t) FROM fields GROUP BY system, poi"):
        places[(system, poi)] = max(places.get((system, poi)) or 0, t or 0)
    return places, dict(conn.execute("SELECT base, MAX(t) FROM books GROUP BY base"))


def service_intel(conn, routes, now, since, hours):
    """Intel: the age of the newest reading of each place the routes flown in the window use."""
    places, books = place_reads(conn)
    ages = []
    flown = [r for (r,) in conn.execute("SELECT DISTINCT route FROM route_hour WHERE hour >= ? AND runs > 0", (int(since) // HOUR * HOUR,))]
    for rid in flown:
        route = routes.get(rid) or {}
        for key in ("belt", "place"):
            spot = str(route.get(key) or "").split(":")
            if len(spot) >= 2:
                t = places.get((spot[0], spot[1]))
                ages.append((now - t) / 3600.0 if t else None)
        stations = [route.get("station"), route.get("sell_at")] + [s.get("at") for s in route.get("stops") or [] if isinstance(s, dict)]
        for at in {str(s).split(":")[-1] for s in stations if s}:
            t = books.get(at)
            ages.append((now - t) / 3600.0 if t else None)
    known = [a for a in ages if a is not None]
    text = "places (fields, herds, stations) of the %d routes flown in %g h; ages in hours at compute time; %d of %d places never read" % (
        len(flown), hours, len(ages) - len(known), len(ages))
    return [("Intel", "place_age_median", hours, median(known), len(known), text),
            ("Intel", "place_age_max", hours, max(known) if known else None, len(known), text),
            ("Intel", "place_fresh_share", hours, sum(1 for a in known if a <= FRESH / 3600.0) / float(len(ages)) if ages else None, len(ages),
             "share of those places read within %d hours (a place never read counts as not fresh)" % (FRESH // 3600))]


def service_logistics(conn, data, root, now, since, hours):
    rows = []
    found = conn.execute("SELECT chain, SUM(stock >= keep), COUNT(*) FROM stats_supply_hour WHERE hour >= ? AND keep IS NOT NULL GROUP BY chain",
                         (int(since) // HOUR * HOUR,)).fetchall()
    ok, seen = sum(r[1] for r in found), sum(r[2] for r in found)
    rows.append(("Logistics", "chains_at_keep", hours, ok / float(seen) if seen else None, seen,
                 "share of chain-hours at or above keep (stats_supply_hour, %d chains)" % len(found) if seen else
                 "not measured: no hourly sample of supply_status yet (stats_supply_hour)"))
    try:
        import store
        items = sorted(r["id"] for r in reserve(data, root, now)["rows"] if r["demand"])
        flow = store.reserve_flow(conn, items, (int(hours),))
        rate = (flow["sums"].get("Logistics") or {}).get("rate", {}).get(int(hours))
        base = flow["base"].get(int(hours))
        rows.append(("Logistics", "reserve_units_change", hours, rate * base[1] if rate is not None and base else None, len(items),
                     "net change of the reserve's items Logistics holds (storage and holds, store.reserve_flow) over %.1f h of samples; "
                     "deliveries into faction storage: not measured (no run records units stored)" % (base[1] if base else 0)))
    except Exception as error:                     # noqa: BLE001
        rows.append(("Logistics", "reserve_units_change", hours, None, 0, "not measured: %s: %s" % (type(error).__name__, error)))
    return rows


def service_military(conn, data, runs, since, hours):
    mine = [r for r in runs if owner_division(r[0], data) == "Military"]
    hunts = [r for r in mine if r[6].get("kind") == "hunt"]
    kills = sum(r[6].get("kills") or 0 for r in hunts if isinstance(r[6].get("kills"), (int, float)))
    lost = conn.execute("SELECT SUM(gain), COUNT(DISTINCT pilot) FROM stats_pilot_hour WHERE key = 'ships_lost' AND gain IS NOT NULL AND hour >= ? "
                        "AND role IN ('drone', 'sentinel')", (int(since) // HOUR * HOUR,)).fetchone()
    sampled = conn.execute("SELECT COUNT(*) FROM stats_pilot_hour WHERE hour >= ? AND role IN ('drone', 'sentinel')", (int(since) // HOUR * HOUR,)).fetchone()[0]
    combat = [k for (k,) in conn.execute("SELECT id FROM skills WHERE category = 'Combat'")] if has_table(conn, "skills") else []
    marks = ",".join("?" * len(combat)) or "''"
    gained = conn.execute("SELECT SUM(gain) FROM stats_pilot_hour WHERE gain > 0 AND hour >= ? AND role IN ('drone', 'sentinel') AND key IN (%s)" % marks,
                          [int(since) // HOUR * HOUR] + combat).fetchone()[0]
    total, samples = conn.execute("SELECT SUM(gain), COUNT(*) FROM stats_pilot_hour WHERE key = ? AND gain > 0 AND hour >= ? AND role IN ('drone', 'sentinel')",
                                  (READ, int(since) // HOUR * HOUR)).fetchone()
    return [("Military", "kills", hours, kills, len(hunts), "kills of the hunt runs of Military's ships (runs)"),
            ("Military", "hunts", hours, len(hunts), len(hunts), "hunt runs flown by Military's ships"),
            ("Military", "ships_lost", hours, lost[0] if sampled else None, lost[1] or 0,
             "the ship files' counter ships_lost, its gain in stats_pilot_hour" if sampled else
             "not measured: no hourly sample of the ship files' counters yet (stats_pilot_hour)"),
            ("Military", "combat_xp_per_ship_hour", hours, (gained or 0) / total if total and sampled else None, samples,
             "XP gained in the Combat skills (table skills) over the hours Military's pilots were read (stats_pilot_hour, read_hours)" if total and sampled else
             "not measured: needs two hourly readings of the pilots' skills (stats_pilot_hour)")]


def service_handover(data, now, since, hours):
    """[(division, figure, hours, value, n, text)]: the goods each division handed over by gift (data/stock/handover.jsonl,
    handover.py: one line per gift of goods) in the window, by the giver's division, at what they would sell for now:
    per item, the units of all givers together within the depth of the best bid of any saved order book (craftbook.bids
    rule), shared among the divisions by their units; beyond the depth and without a bid they count 0, and how many such
    units there are is named. Orders ENT-064, block UNITY: under strict classes a hunt or a gather earns nothing in its
    wallet, so P1 reads what it enabled here; never more than the books would pay today."""
    path = Path(data) / "stock" / "handover.jsonl"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        return [("Command", "handed_over_worth", hours, None, 0, "not measured: %s cannot be read (%s)" % (path.name, type(error).__name__))]
    best = {}
    for book_path in sorted((Path(data) / "market").glob("*.json")):
        book = read_json(book_path, {})
        for row in book.get("items") or [] if isinstance(book, dict) else []:
            bid = row.get("best_buy") if isinstance(row.get("best_buy"), (int, float)) else 0
            depth = row.get("best_buy_qty") if isinstance(row.get("best_buy_qty"), (int, float)) else 1     # no depth saved: one unit (F12)
            if bid > best.get(row.get("item_id"), (0, 0))[0]:
                best[row.get("item_id")] = (bid, depth)
    given, gifts = defaultdict(Counter), Counter()          # item -> {division: units}
    for line in lines:
        try:
            gift = json.loads(line)
        except ValueError:
            continue
        if not isinstance(gift, dict) or not isinstance(gift.get("at"), (int, float)) or not since <= gift["at"] <= now:
            continue
        name = owner_division(str(gift.get("from") or ""), data)
        gifts[name] += 1
        for item, count in (gift.get("items") or {}).items() if isinstance(gift.get("items"), dict) else []:
            if isinstance(count, (int, float)) and not isinstance(count, bool) and count > 0:
                given[item][name] += count
    worth, units, beyond = Counter(), Counter(), Counter()
    for item, by in given.items():
        total = float(sum(by.values()))
        bid, depth = best.get(item, (0, 0))
        sold = min(total, max(depth, 0)) if bid > 0 else 0
        for name, count in by.items():
            units[name] += count
            worth[name] += bid * sold * count / total
            beyond[name] += count - sold * count / total
    rows = []
    for name in sorted(gifts):
        rows.append((name, "handed_over_worth", hours, worth[name], gifts[name],
                     "credits the goods given by gift (handover.jsonl, %d gifts) would sell for now: each item within the depth of its best bid in any "
                     "saved book, shared by units; %s units beyond the depth or without a bid, at 0" % (gifts[name], num(beyond[name]))))
        rows.append((name, "handed_over_units", hours, units[name], gifts[name], "units of goods given by gift to the receivers of Trade and Logistics"))
    return rows


def service_trade_mining(conn, data, routes, runs, now, since, hours):
    rows = []
    sells = [r for r in runs if owner_division(r[0], data) == "Trade" and run_class(routes.get(r[1]), r[1], role_of(r[0], data)) == "shared"
             and workclass.work_class(routes.get(r[1]) or {}, r[1]) == "sell"]
    read = [r for r in sells if r[5]]
    minutes = sum(r[3] for r in read)
    rows.append(("Trade", "sell_credits", hours, sum(r[4] for r in read), len(read),
                 "steady credits of Trade's runs on sell-class routes (selling stored goods); whether each unit sold was surplus at that moment "
                 "is not recorded"))
    rows.append(("Trade", "sell_cph", hours, 60.0 * sum(r[4] for r in read) / minutes if minutes else None, len(read), "credits per ship-hour of those runs"))
    mines = [r for r in runs if owner_division(r[0], data) == "Mining" and r[6].get("kind") == "mine" and isinstance(r[6].get("ore"), (int, float))]
    ore, minutes = sum(r[6]["ore"] for r in mines), sum(r[3] for r in mines)
    shiphours, samples = ship_hours(conn, since, int(now), ("miner",))
    rows.append(("Mining", "ore_per_run_hour", hours, 60.0 * ore / minutes if minutes else None, len(mines), "units of ore the mine runs of Mining brought, per hour of those runs"))
    rows.append(("Mining", "ore_per_ship_hour", hours, ore / shiphours["miner"] if shiphours.get("miner") else None, len(mines),
                 "the same per ship-hour of the miners (%d samples of stats_time: mean ships x hours)" % samples if shiphours.get("miner") else
                 "not measured: %d samples of stats_time in the window (needs %d)" % (samples, MIN_SAMPLES)))
    days = [v for (v,) in conn.execute("SELECT value FROM stats_figures WHERE view = 'supply' AND figure = 'days' AND value IS NOT NULL")]
    rows.append(("Mining", "reserve_days_median", 0, median(days), len(days), "median days of supply of the reserve's goods that run down (view supply)"))
    return rows


def figures_classes(conn, data, root, now):
    import dispatch
    import fill
    routes = route_files(root)
    last = []
    for (line,) in conn.execute("SELECT r.row FROM runs r JOIN (SELECT route, MAX(t) AS t FROM runs WHERE kind = 'hunt' GROUP BY route) m "
                                "ON m.route = r.route AND m.t = r.t"):
        try:
            last.append(json.loads(line))
        except (TypeError, ValueError):
            continue
    rest = dispatch.resting(routes, last, now)
    seen = {"data": data, "routes": routes, "now": now}
    ships = Counter(role for (role,) in conn.execute("SELECT role FROM ships"))
    rows = []
    for role in sorted(division.ROLES):
        places, count, capped, unknown = 0, 0, 0, 0
        for rid, route in routes.items():
            cls = workclass.work_class(route, rid)
            if cls in workclass.SHARED or not workclass.own(role, route, rid) or route.get("status") == "off" or route.get("park") or rest.get(rid, 0) > now:
                continue
            cap = int(route.get("max_ships") or 1)
            deep = fill.carries(seen, route)
            if deep is not None and (deep.get("ships") is not None or deep.get("extra")):
                carry = (deep.get("ships") or 0) + (deep.get("extra") or 0)
                if carry < cap:
                    cap, capped = carry, capped + 1
            elif deep is not None:
                unknown += 1
            places += cap
            count += 1
        n = ships.get(role, 0)
        text = "routes of its own class (workclass.py) switched on, not resting; max_ships, never above fill.carries (%d capped, %d whose carry is not measured)" % (capped, unknown)
        rows += [(role, "ships", 0, n, n, "ships of the role now (table ships)"), (role, "places", 0, places, count, text),
                 (role, "spill", 0, max(0, n - places), n, "ships with no place of their own class")]
    return rows


def figures_time(conn, data, root, now, hours):
    since = int(now - hours * HOUR)
    rows = []
    found = conn.execute("SELECT role, state, SUM(ships), COUNT(DISTINCT t) FROM stats_time WHERE t >= ? GROUP BY role, state", (since,)).fetchall()
    samples = conn.execute("SELECT COUNT(DISTINCT t) FROM stats_time WHERE t >= ?", (since,)).fetchone()[0]
    by = defaultdict(Counter)
    for role, state, ships, _n in found:
        by[role][state] += ships
        by["Fleet"][state] += ships
    for role, counts in by.items():
        total = sum(counts.values())
        for state in STATES:
            rows.append((role, state, hours, counts.get(state, 0) / float(total) if total else None, total,
                         "share of %d ship observations in %d samples (stats_time, one every %d min)" % (total, samples, TIME_EVERY // 60)))
        rows.append((role, "ship_hours", hours, total / float(samples) * hours if samples >= MIN_SAMPLES else None, samples,
                     "mean ships per sample x %g h (work sampling)" % hours if samples >= MIN_SAMPLES else
                     "not measured: %d samples (needs %d)" % (samples, MIN_SAMPLES)))
    routes = route_files(root)
    spent = defaultdict(Counter)
    for pilot, rid, _t, minutes, _c, _r, _row in run_rows(conn, since):
        role = role_of(pilot, data)
        cls = run_class(routes.get(rid), rid, role)
        spent[role][cls] += minutes / 60.0
        spent["Fleet"][cls] += minutes / 60.0
    for role, counts in spent.items():
        for cls in ("own", "other", "once", "shared"):
            rows.append((role, "run_" + cls, hours, counts.get(cls, 0), None, "hours of runs started in the window by route class (runs, workclass.py)"))
    history = read_json(Path(data) / "fleet" / "history.json", [])
    w = [h[8]["w"] for h in history if isinstance(h, list) and len(h) > 8 and isinstance(h[8], dict) and isinstance(h[8].get("w"), list)
         and h[0] >= since and sum(h[8]["w"]) > 0] if isinstance(history, list) else []
    total = float(sum(sum(x) for x in w))
    for index, name in enumerate(("working", "parked", "adrift")):
        rows.append(("Fleet", "collector_" + name, hours, sum(x[index] for x in w) / total if total else None, len(w),
                     "the collector's minute samples (history.json extra w): ship-minutes %s" % name))
    return rows


def reserve_levels(root):
    """{item: (min, max)} from game/reserve.tsv when its header carries the columns `min` and `max`; {} otherwise."""
    path = Path(root).resolve().parent / "game" / "reserve.tsv"
    try:
        lines = path.read_text(encoding="ascii").splitlines()
    except (OSError, UnicodeDecodeError):
        return {}
    header, out = None, {}
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = [c.strip() for c in line.split("\t")]
        if header is None:
            header = cells
            if "min" not in header and "max" not in header:
                return {}
            continue
        row = dict(zip(header, cells))
        value = lambda key: float(row[key]) if row.get(key, "").replace(".", "", 1).isdigit() else None
        if row.get("id"):
            out[row["id"]] = (value("min"), value("max"))
    return out


def feeders(conn, routes, item):
    """The route ids that bring an item: a mine route whose field yields it (table fields), a stop that crafts or buys
    it, a supply chain that names it."""
    fields = {"%s:%s" % (s, p) for s, p in conn.execute("SELECT system, poi FROM fields WHERE resource = ?", (item,))}
    out = set()
    for rid, route in routes.items():
        if route.get("status") == "off":
            continue
        if route.get("kind") == "mine" and str(route.get("belt") or "") in fields:
            out.add(rid)
        for stop in route.get("stops") or []:
            if not isinstance(stop, dict):
                continue
            if any(isinstance(j, dict) and j.get("makes") == item for j in stop.get("craft") or []) or \
               any(isinstance(b, dict) and b.get("item") == item for b in stop.get("buy") or []) or \
               any(isinstance(m, dict) and "%s" % m.get("at") in fields for m in stop.get("mine") or []):
                out.add(rid)
    if has_table(conn, "supply_chains"):
        for (sources,) in conn.execute("SELECT sources FROM supply_chains WHERE item = ?", (item,)):
            out |= {s for s in str(sources or "").split(",") if s in routes}
    return sorted(out)


def figures_supply(conn, data, root, now):
    import store
    routes = route_files(root)
    res = reserve(data, root, now)
    wanted = [r for r in res["rows"] if r["demand"]]
    flow = store.reserve_flow(conn, [r["id"] for r in wanted], (24,))
    rate = defaultdict(float)
    known = set()
    for row in flow["rows"]:
        if row["rate"].get(24) is not None:
            rate[row["item"]] += row["rate"][24]
            known.add(row["item"])
    span = flow["base"].get(24, (None, 0, True))
    levels = reserve_levels(root)
    flies = Counter(f for (f,) in conn.execute("SELECT flies FROM ships WHERE flies IS NOT NULL"))
    rows, gather = [], []
    for r in wanted:
        item = r["id"]
        low, high = levels.get(item, (None, None))
        target = high if high is not None else r["demand"]
        change = rate.get(item) if item in known else None
        rows += [(item, "held", 0, r["held"], 1, "surplus.py (storage book of %s)" % res["written"]),
                 (item, "needed", 0, r["demand"], 1, "surplus.py demand: what the reserve's targets ask of it"),
                 (item, "short", 0, r["short"], 1, "surplus.py short"),
                 (item, "min", 0, low, 1 if low is not None else 0, "game/reserve.tsv min" if low is not None else "not set (game/reserve.tsv carries no min)"),
                 (item, "max", 0, high, 1 if high is not None else 0, "game/reserve.tsv max" if high is not None else "not set (game/reserve.tsv carries no max)"),
                 (item, "rate", 24, change, int(span[1] or 0),
                  "net change per hour, every division's storage and holds (store.reserve_flow over %.1f h of stock_hour)" % span[1]
                  if change is not None else "not measured: no hourly sample of stock_hour spans the item")]
        days = r["held"] / (-change * 24) if change is not None and change < 0 else None
        to_target = (target - r["held"]) / change if change and change > 0 and r["held"] < target else None
        rows.append((item, "days", 24, days, 1 if days is not None else 0, "held / what it loses a day (only for a good that runs down)"))
        rows.append((item, "to_target", 24, to_target, 1 if to_target is not None else 0,
                     "hours to %s at the net change of 24 h (only for a good that grows and is below it)" % ("max" if high is not None else "the demand")))
        feed = feeders(conn, routes, item)
        on = sum(flies.get("%s %s" % ((routes.get(f) or {}).get("kind"), f), 0) for f in feed)
        rows.append((item, "routes", 0, len(feed), len(feed), ",".join(feed[:12]) + (" ..." if len(feed) > 12 else "")))
        rows.append((item, "ships", 0, on, len(feed), "our ships flying those routes now (ships.flies)"))
        gather += gather_rows(conn, routes, item, r)
    return rows, gather


def gather_rows(conn, routes, item, r):
    """Gather against buy for one reserve good: the cost per unit of the mine runs at fields that yield it (runs that sold
    nothing: their credits are their costs; every unit of ore of the run counts), the best ask (the store's books: the
    saved order books, as fill.asks reads them), the best bid (surplus.py, craftbook.bids)."""
    fields = {"%s:%s" % (s, p) for s, p in conn.execute("SELECT system, poi FROM fields WHERE resource = ?", (item,))}
    ids = [rid for rid, route in routes.items() if route.get("kind") == "mine" and str(route.get("belt") or "") in fields]
    cost, units, n = 0.0, 0, 0
    if ids:
        marks = ",".join("?" * len(ids))
        for credits, line in conn.execute("SELECT credits, row FROM runs WHERE readable = 1 AND route IN (%s)" % marks, ids):
            try:
                row = json.loads(line)
            except (TypeError, ValueError):
                continue
            if isinstance(row.get("ore"), (int, float)) and row["ore"] > 0 and not row.get("sold"):
                cost, units, n = cost - (credits or 0), units + row["ore"], n + 1
    asks = conn.execute("SELECT ask_qty, ask, base FROM books WHERE item = ? AND ask IS NOT NULL ORDER BY ask LIMIT 1", (item,)).fetchall()
    return [(item, "gather_cost", 0, cost / units if units else None, n,
             "the costs (minus the credits) of %d mine runs that sold nothing at fields that yield it, over %s units of ore they brought "
             "(a field of several ores: every unit counts)" % (n, num(units)) if units else "not measured: no run that gathered it without a sale"),
            (item, "ask", 0, asks[0][1] if asks else None, asks[0][0] if asks else 0, "best ask at %s (units at it in n)" % asks[0][2] if asks else "no ask in our books"),
            (item, "bid", 0, r["bid"], r["bid_units"], "best bid at %s (units at it in n), surplus.py" % (r["bid_at_name"] or r["bid_at"]) if r["bid"] else "no bid in our books")]


def figures_xp(conn, data, root, now, hours):
    """XP per hour a pilot was read (stats_pilot_hour): per role and skill, per route (each reading's gain split over the
    routes flown between it and the reading before, by minutes), and per ship the hours to its next Piloting tier."""
    import hive
    since = int(now - hours * HOUR) // HOUR * HOUR
    rows = []
    skip = ",".join("'%s'" % k for k in NOT_XP)
    read = {(p, h): (gain, t) for p, h, gain, t in conn.execute("SELECT pilot, hour, gain, t FROM stats_pilot_hour WHERE key = ? AND gain > 0 AND hour > ?",
                                                                (READ, since))}
    role_hours, role_pilots = Counter(), defaultdict(set)
    for (pilot, _hour), (gain, _t) in read.items():
        role_hours[role_of(pilot, data)] += gain
        role_pilots[role_of(pilot, data)].add(pilot)
    for role, key, gain, pilots in conn.execute("SELECT role, key, SUM(gain), COUNT(DISTINCT pilot) FROM stats_pilot_hour WHERE gain > 0 AND hour > ? "
                                                "AND key NOT IN (%s) GROUP BY role, key" % skip, (since,)).fetchall():
        h = role_hours.get(role)
        rows.append(("%s|%s" % (role, key), "xp_per_ship_hour", hours, gain / h if h else None, pilots,
                     "XP gained over the %.0f hours its %d pilots were read (stats_pilot_hour); n = pilots that gained" % (h, len(role_pilots[role])) if h else
                     "not measured: no two readings of the role's pilots in the window"))
    gained = defaultdict(float)
    for hour, pilot, gain in conn.execute("SELECT hour, pilot, SUM(gain) FROM stats_pilot_hour WHERE gain > 0 AND hour > ? AND key NOT IN (%s) "
                                          "GROUP BY hour, pilot" % skip, (since,)):
        gained[(pilot, hour)] += gain
    longest = max((g for g, _t in read.values()), default=1.0)
    flown = defaultdict(list)
    for pilot, rid, t, minutes, _c, _r, _row in run_rows(conn, int(since - longest * HOUR)):
        flown[pilot].append((t, t + minutes * 60, rid))
    per_route, route_hours, pilot_hours = Counter(), Counter(), Counter()
    blurred = 0
    for (pilot, hour), (span, t) in read.items():
        if span > SPLIT_SPAN:
            blurred += 1
            continue
        gain, begin = gained.get((pilot, hour), 0.0), t - span * HOUR
        overlap = Counter()
        for start, end, rid in flown.get(pilot, ()):
            o = min(end, t) - max(start, begin)
            if o > 0:
                overlap[rid] += o
        total = sum(overlap.values())
        for rid, o in overlap.items():
            per_route[rid] += gain * o / max(total, span * HOUR)
            route_hours[rid] += o / 3600.0
            pilot_hours[rid] += 1
        if total < span * HOUR:
            per_route["(no route)"] += gain * (span * HOUR - total) / (span * HOUR)
            route_hours["(no route)"] += (span * HOUR - total) / 3600.0
            pilot_hours["(no route)"] += 1
    for rid in route_hours:
        rows.append((rid, "route_xp_per_ship_hour", hours, per_route[rid] / route_hours[rid] if route_hours[rid] else None, pilot_hours[rid],
                     "each reading's XP gain split over the routes flown since the reading before, by minutes; n = pilot readings"))
    if blurred:
        rows.append(("(readings over %g h)" % SPLIT_SPAN, "route_xp_per_ship_hour", hours, None, blurred,
                     "not split over routes: %d readings spanned more than %g hours (each route would get the pilot's mean)" % (blurred, SPLIT_SPAN)))
    tables = xp_tables(data)
    pace = dict(conn.execute("SELECT pilot, SUM(gain) FROM stats_pilot_hour WHERE key = 'piloting' AND gain > 0 AND hour > ? GROUP BY pilot", (since,)))
    watched = Counter()
    for (pilot, _hour), (gain, _t) in read.items():
        watched[pilot] += gain
    for pilot, level, value in conn.execute("SELECT pilot, level, value FROM stats_pilot_last WHERE key = 'piloting'"):
        target = next((lv for lv, _tier in hive.TIERS if lv > (level or 0)), None)
        need = total_xp(tables, "piloting", target, 0) - value if target and tables.get("piloting") else None
        rate = (pace.get(pilot) or 0) / watched[pilot] if watched.get(pilot) else None
        rows.append((pilot, "hours_to_tier", hours, need / rate if need is not None and rate else None, int(watched.get(pilot, 0)),
                     "XP to Piloting %s (hive.TIERS) at its own Piloting XP an hour over %.0f h read" % (target, watched.get(pilot, 0)) if rate else
                     "not measured: no Piloting XP gained between two readings in the window" if target else "the highest tier's Piloting reached"))
    return rows


def figures_upgrades(conn, data, now):
    hulls = {}
    for hid, name, cls, tier, need, weapon, defense, utility, faction in conn.execute(
            "SELECT id, name, class, tier, piloting_required, weapon_slots, defense_slots, utility_slots, faction FROM hulls"):
        hulls[name] = hulls[hid] = (hid, name, cls, tier, need, weapon, defense, utility, faction)
    fitted = defaultdict(Counter)
    for pilot, slot in conn.execute("SELECT pilot, slot FROM ship_modules"):
        fitted[pilot][slot] += 1
    pilot_level = dict(conn.execute("SELECT pilot, level FROM ship_skills WHERE skill = 'piloting'"))
    unique = list({v[0]: v for v in hulls.values()}.values())
    rows = []
    for pilot, hull in conn.execute("SELECT pilot, class FROM ships ORDER BY pilot"):
        h = hulls.get(hull)
        level = pilot_level.get(pilot)
        if h is None:
            rows.append((pilot, "tier", 0, None, 0, "hull %s: not in the catalog's hulls" % hull))
            continue
        hid, name, cls, tier, _need, weapon, defense, utility, faction = h
        nxt = [x for x in unique if x[2] == cls and x[3] == (tier or 0) + 1 and x[8] in (faction, None, "")]
        named = [x[4] for x in nxt if x[4] is not None]
        need = min(named) if named else (0 if nxt else None)
        names = ", ".join(sorted(x[1] for x in nxt)[:6]) or "none in the catalog"
        rows += [(pilot, "tier", 0, tier, 1, "hull %s (%s, class %s); tier %s hulls of its class: %s" % (name, hid, cls, (tier or 0) + 1, names)),
                 (pilot, "piloting", 0, level, 1, "ship_skills"),
                 (pilot, "piloting_next", 0, need, len(nxt), "the Piloting the next tier's hulls of its class need (hulls.piloting_required)" if named else
                  "the catalog names no Piloting for the next tier's hulls of its class (0)" if nxt else "no hull of the next tier in its class"),
                 (pilot, "empty_weapon", 0, max(0, (weapon or 0) - fitted[pilot]["weapon"]), weapon or 0, "weapon slots of the hull less modules fitted"),
                 (pilot, "empty_defense", 0, max(0, (defense or 0) - fitted[pilot]["defense"]), defense or 0, "defense slots of the hull less modules fitted"),
                 (pilot, "empty_utility", 0, max(0, (utility or 0) - fitted[pilot]["utility"]), utility or 0, "utility slots of the hull less modules fitted")]
    return rows


def band(values, newest):
    """(median, MAD, low, high, out) of a history against its newest value: out is 'HIGH', 'LOW' or ''."""
    m, d = median(values), mad(values)
    low, high = m - MAD_K * MAD_SCALE * d, m + MAD_K * MAD_SCALE * d
    return m, d, low, high, ("HIGH" if newest > high else "LOW" if newest < low else "") if d > 0 else ""


def alert_row(subject, series, newest_hour, shown=num):
    """One alert: the newest hour against the 7 days before it (n >= MIN_N hours); shown formats a value."""
    newest = series.get(newest_hour)
    history = [v for h, v in series.items() if newest_hour - 7 * DAY <= h < newest_hour and v is not None]
    if newest is None or len(history) < MIN_N:
        return (subject, "alert", 0, newest, len(history), "not judged: %d hours of history before %s (needs %d)%s" % (
            len(history), stamp(newest_hour), MIN_N, "" if newest is not None else "; the newest hour has no value"))
    m, d, low, high, out = band(history, newest)
    text = "%s: hour %s %s against median %s, MAD %s, band %s to %s (median +- %g x %g x MAD) over %d hours" % (
        ("OUT " + out) if out else ("ok" if d > 0 else "not judged: MAD 0, no spread"), stamp(newest_hour), shown(newest), shown(m), shown(d), shown(low), shown(high),
        MAD_K, MAD_SCALE, len(history))
    return (subject, "alert", 0, newest, len(history), text)


def figures_alerts(conn, now):
    rows = []
    raw_money = conn.execute(
        "SELECT hour, net, idle, ships, minutes FROM stats_money_hour WHERE division = 'Fleet' AND hour >= ?",
        (int(now) - 9 * DAY,)).fetchall()
    # Exclude paused zero-ship hours from the 7-day baseline so an idle pause cannot collapse MAD to 0.
    money = {h: (net, idle) for h, net, idle, ships, minutes in raw_money
             if (ships is None or ships > 0) and (minutes is None or minutes > 0)}
    if money:
        newest = max(money)
        rows.append(alert_row("Fleet steady net per hour", {h: v[0] for h, v in money.items()}, newest))
        rows.append(alert_row("Fleet idle share", {h: v[1] for h, v in money.items()}, newest, lambda v: "%.1f%%" % (100 * v)))
    else:
        rows.append(("Fleet steady net per hour", "alert", 0, None, 0, "not judged: stats_money_hour holds no hour yet"))
    series = defaultdict(dict)
    for route, hour, credits, minutes in conn.execute("SELECT route, hour, credits, read_minutes FROM route_hour WHERE hour >= ? AND read_minutes > 0",
                                                      (int(now) - 9 * DAY,)):
        series[route][hour] = 60.0 * credits / minutes
    for route, found in sorted(series.items()):
        if len(found) > MIN_N:
            rows.append(alert_row("route " + route, found, max(found)))
    return rows


# ---- the pass

PARTS = ("money", "time", "pilots", "supply", "authors", "refill", "figures", "prune")


def due(conn, part, now, every):
    """True when the part last ran `every` seconds ago or more (hourly parts: in an earlier UTC hour)."""
    last = meta_get(conn, "stats.%s.at" % part)
    if last is None:
        return True
    if every == HOUR:
        return int(last) // HOUR < int(now) // HOUR
    return now - float(last) >= every


def run_part(conn, part, work, now, out):
    """One part in its own transaction; a fault is kept in meta (stats.<part>.error) and never stops the others."""
    begun = time.time()
    conn.execute("BEGIN IMMEDIATE")
    try:
        rows = work()
        meta_put(conn, "stats.%s.at" % part, int(now))
        meta_put(conn, "stats.%s.rows" % part, int(rows or 0))
        meta_put(conn, "stats.%s.seconds" % part, round(time.time() - begun, 3))
        meta_put(conn, "stats.%s.error" % part, "")
        conn.execute("COMMIT")
        out["rows"] += int(rows or 0)
        out["parts"][part] = round(time.time() - begun, 3)
    except Exception as error:                     # noqa: BLE001  a failing figure never holds up the pass
        conn.execute("ROLLBACK")
        said = "%s: %s" % (type(error).__name__, str(error).splitlines()[0][:200] if str(error) else "")
        out["errors"].append("%s: %s" % (part, said))
        conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", ("stats.%s.error" % part, "%s at %s" % (said, stamp(now))))
        conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", ("stats.%s.at" % part, int(now)))      # tried again when due next


def prune(conn, now):
    gone = conn.execute("DELETE FROM stats_time WHERE t < ?", (int(now - KEEP["stats_time"] * DAY),)).rowcount
    return gone + conn.execute("DELETE FROM stats_pilot_hour WHERE hour < ?", (int(now - KEEP["stats_pilot_hour"] * DAY),)).rowcount


def setup(conn):
    """The tables (store.py runs SCHEMA too); the snapshot-like stats tables are made again when their text changes."""
    version = hashlib.sha256(SCHEMA.encode("ascii")).hexdigest()[:16]
    if meta_get(conn, "stats.schema") != version:
        for table in ("stats_figures", "stats_refill", "stats_pilot_last"):
            conn.execute("DROP TABLE IF EXISTS %s" % table)
        conn.executescript(SCHEMA)
        meta_put(conn, "stats.schema", version)


def compute(conn, data, root, now):
    """The store's hook: every part that is due, each in its own transaction. {rows, parts {part: seconds}, errors}."""
    out = {"rows": 0, "parts": {}, "errors": []}
    setup(conn)
    data, root = str(data), str(root)
    hours = 24
    work = (("money", HOUR, lambda: sample_money(conn, data, root, now)),
            ("time", TIME_EVERY, lambda: sample_time(conn, root, now)),
            ("pilots", HOUR, lambda: sample_pilots(conn, data, now)),
            ("supply", HOUR, lambda: sample_supply(conn, now)),
            ("authors", FIGURES_EVERY, lambda: sample_authors(conn, root, now)),
            ("refill", HOUR, lambda: compute_refill(conn, root, now)),
            ("figures", FIGURES_EVERY, lambda: compute_figures(conn, data, root, now, hours)),
            ("prune", HOUR, lambda: prune(conn, now)))
    ROLE_MEMO.clear()
    CACHE.pop("reserve", None)
    CACHE.pop("routes", None)
    for part, every, job in work:
        if due(conn, part, now, every):
            run_part(conn, part, job, now, out)
    return out


def compute_figures(conn, data, root, now, hours):
    """Every view's rows of stats_figures; a view that fails keeps its last rows and is named in its own row."""
    count = 0
    jobs = (("kpi", lambda: figures_kpi(conn, data, root, now)), ("classes", lambda: figures_classes(conn, data, root, now)),
            ("time", lambda: figures_time(conn, data, root, now, hours)), ("supply", None),
            ("contribution", lambda: figures_contribution(conn, data, root, now, hours)), ("xp", lambda: figures_xp(conn, data, root, now, hours)),
            ("upgrades", lambda: figures_upgrades(conn, data, now)), ("alerts", lambda: figures_alerts(conn, now)))
    for view, job in jobs:
        conn.execute("SAVEPOINT view")
        try:
            if view == "supply":
                supply, gather = figures_supply(conn, data, root, now)
                count += write_figures(conn, "supply", supply, now) + write_figures(conn, "gather", gather, now)
            else:
                count += write_figures(conn, view, job(), now)
            conn.execute("RELEASE view")
        except Exception as error:                 # noqa: BLE001  one view that fails keeps its last rows
            conn.execute("ROLLBACK TO view")
            conn.execute("RELEASE view")
            conn.execute("INSERT OR REPLACE INTO stats_figures VALUES (?, '(view)', 'error', 0, NULL, 0, ?, ?)",
                         (view, "%s: %s" % (type(error).__name__, str(error).splitlines()[0][:200] if str(error) else ""), int(now)))
    return count


# ---- the reader: hive.py stats <view>

def figures(conn, view):
    """{subject: {(figure, hours): (value, n, text)}} of one view, and the time it was computed."""
    out, at = defaultdict(dict), None
    for subject, figure, hours, value, n, text, t in conn.execute(
            "SELECT subject, figure, hours, value, n, text, t FROM stats_figures WHERE view = ?", (view,)):
        out[subject][(figure, hours)] = (value, n, text)
        at = max(at or 0, t)
    if at is None:                                 # a view with no row: the time of the computation that found none
        at = int(meta_get(conn, "stats.figures.at", 0)) or None
    return out, at


def cell(entry, scale=1.0, unit=""):
    if not entry or entry[0] is None:
        return "not measured"
    return "%s%s" % (num(entry[0] * scale), unit)


def pct(entry):
    return "not measured" if not entry or entry[0] is None else "%.0f%%" % (100 * entry[0])


def head(view, title, at, data, now, extra=""):
    path = Path(data) / "store" / "read.db"
    written = path.stat().st_mtime if path.is_file() else None
    print("STATS %s | %s | computed %s (%s old) | the store's read copy written %s%s" % (
        view.upper(), title, stamp(at), "%d min" % ((now - at) // 60) if at else "--", stamp(written), " | " + extra if extra else ""))


def roles_of(member):
    return [r for r, m in division.ROLES.items() if member in (None, m)]


def show_kpi(conn, data, now, args):
    rows, at = figures(conn, "kpi")
    head("kpi", "the fleet as one purse: steady money per hour (credits an hour; a cost is positive; net = income - costs)", at, data, now)
    fleet = rows.get("Fleet") or {}
    if not fleet:
        print("  not measured: stats.py has not computed the kpi yet (the store computes it every %d minutes)" % (FIGURES_EVERY // 60))
        return 0
    print("  %-34s %14s %14s %14s %14s" % ("per hour, last", "1 h", "6 h", "24 h", "72 h"))
    for key, title in (("income", "throughput (income)"), ("costs", "operating expense (costs)"), ("fuel", "  of it fuel (metered)"),
                       ("repair", "  of it repairs (metered)"), ("net", "steady net"), ("once", "paid once (rewards - bought)"),
                       ("total", "net of everything (wallets)"), ("purse", "net of the purse (+ treasury)"),
                       ("per_ship", "net per ship-hour"), ("net_tiled", "steady net, whole hours"),
                       ("net_before", "  the window before (trend)")):
        print("  %-34s %14s %14s %14s %14s" % (title, *(cell(fleet.get((key, float(h)))) for h in WINDOWS)))
    print("  %-34s %14s %14s %14s %14s" % ("n (minutes or hours behind)", *(num((fleet.get(("net", float(h))) or (0, 0))[1]) for h in WINDOWS)))
    print("  %-34s %14s %14s %14s %14s" % ("wallets + treasury, change", *(cell(fleet.get(("purse_change", float(h)))) for h in WINDOWS)))
    for h in WINDOWS:
        this, before = fleet.get(("net_tiled", float(h))), fleet.get(("net_before", float(h)))
        if this and before and this[0] is not None and before[0] is not None:
            print("  trend %2d h: steady net %s an hour against %s in the %d hours before (%+.0f%%), n %d and %d hours" % (
                h, num(this[0]), num(before[0]), h, 100.0 * (this[0] - before[0]) / abs(before[0]) if before[0] else 0, this[1], before[1]))
    print("  1, 6, 24 h: %s" % (fleet.get(("net", 24.0)) or (0, 0, "?"))[2])
    print("  72 h and the trends: %s" % (fleet.get(("net", 72.0)) or (0, 0, "?"))[2])
    for key, title in (("wallets", "wallets now"), ("treasury", "treasury"), ("purse", "the fleet's money"), ("reserve_worth", "the reserve at the best bid"),
                       ("surplus_worth", "the surplus at the best bid"), ("tax", "weekly tax, 24 h"), ("rent", "rent per cycle")):
        entry = fleet.get((key, 0.0)) or fleet.get((key, 24.0))
        print("  %-30s %14s  n %-6s %s" % (title, cell(entry), num(entry[1]) if entry else "--", entry[2] if entry else "not measured"))
    print("  purse change: %s" % (fleet.get(("purse_change", 24.0)) or (0, 0, "?"))[2])
    return 0


def show_contribution(conn, data, now, args):
    rows, at = figures(conn, "contribution")
    hours = float(args.get("hours", 24))
    head("contribution", "what each division gives the whole fleet: its own net, the income its route files enabled, its service", at, data, now)
    names = [division_of(m) for m in division.MEMBERS if args.get("member") in (None, m)]
    print("  %-10s %12s %12s %12s %12s | %14s %18s %6s" % ("division", "own net 1h", "6h", "24h", "72h", "enabled 24h", "of it for others", "routes"))
    for name in names + [n for n in ("none", "not read") if n in rows and not args.get("member")]:
        r = rows.get(name) or {}
        print("  %-10s %12s %12s %12s %12s | %14s %18s %6s" % (name, *(cell(r.get(("own_net", float(h)))) for h in WINDOWS),
                                                         cell(r.get(("enabled", 24.0))), cell(r.get(("enabled_others", 24.0))),
                                                         num((r.get(("enabled", 24.0)) or (0, 0))[1])))
    print("  own net: credits an hour (fleet.json, stats_money_hour); enabled: steady credits in the window of every ship on the routes the division wrote "
          "first (git log), whoever flew them")
    for name in names:
        r = rows.get(name) or {}
        service = [(f, h, v) for (f, h), v in sorted(r.items()) if f not in ("own_net", "enabled", "enabled_others")]
        for figure, h, (value, n, text) in service:
            shown = "not measured" if value is None else ("%.0f%%" % (100 * value) if "share" in figure or "at_keep" in figure else
                                                          "%.1f" % value if abs(value) < 100 else num(value))
            print("  %-10s %-26s %14s  n %-5s %s" % (name, figure, shown, num(n), text))
    return 0


def show_classes(conn, data, now, args):
    rows, at = figures(conn, "classes")
    head("classes", "class capacity: places of each role's own class work open now against its ships", at, data, now)
    print("  %-9s %6s %8s %7s %7s  %s" % ("role", "ships", "places", "routes", "spill", "what the places rest on"))
    for role in roles_of(args.get("member")):
        r = rows.get(role) or {}
        places = r.get(("places", 0.0)) or (None, 0, "not measured")
        print("  %-9s %6s %8s %7s %7s  %s" % (role, cell(r.get(("ships", 0.0))), cell(places), num(places[1]), cell(r.get(("spill", 0.0))), places[2]))
    return 0


def show_time(conn, data, now, args):
    rows, at = figures(conn, "time")
    hours = 24
    head("time", "where the ship-hours went, last %d h: work sampling of the table ships every %d min" % (hours, TIME_EVERY // 60), at, data, now)
    print("  %-9s %9s " % ("role", "ship-h") + " ".join("%8s" % s for s in STATES) + " | runs h: own other once shared")
    for role in roles_of(args.get("member")) + ([] if args.get("member") else ["Fleet"]):
        r = rows.get(role) or {}
        print("  %-9s %9s " % (role, cell(r.get(("ship_hours", float(hours))))) + " ".join("%8s" % pct(r.get((s, float(hours)))) for s in STATES)
              + " | " + " ".join(cell(r.get(("run_" + c, float(hours)))) for c in ("own", "other", "once", "shared")))
    fleet = rows.get("Fleet") or {}
    print("  the collector's minute samples (history.json): working %s, parked %s, adrift %s, n %s" % (
        pct(fleet.get(("collector_working", 24.0))), pct(fleet.get(("collector_parked", 24.0))), pct(fleet.get(("collector_adrift", 24.0))),
        num((fleet.get(("collector_working", 24.0)) or (0, 0))[1])))
    print("  states: " + "; ".join("%s = %s" % (s, STATE_TEXT[s]) for s in STATES))
    entry = fleet.get(("own", 24.0))
    print("  n: %s" % (entry[2] if entry else "not measured: no sample yet (stats_time)"))
    return 0


def show_supply(conn, data, now, args):
    rows, at = figures(conn, "supply")
    head("supply", "the reserve's goods: held against needed, min and max, the net change an hour (24 h), days of supply", at, data, now)
    print("  %-26s %10s %10s %10s %8s %8s %10s %8s %9s %6s %5s" % ("item", "held", "needed", "short", "min", "max", "per h 24h", "days", "to target", "routes", "ships"))
    order = sorted(rows.items(), key=lambda kv: (-((kv[1].get(("short", 0.0)) or (0,))[0] or 0), kv[0]))
    for item, r in order:
        if item == "(view)":
            continue
        v = lambda key, h=0.0: r.get((key, h))
        print("  %-26s %10s %10s %10s %8s %8s %10s %8s %9s %6s %5s" % (
            item[:26], cell(v("held")), cell(v("needed")), cell(v("short")), "not set" if not v("min") or v("min")[0] is None else cell(v("min")),
            "not set" if not v("max") or v("max")[0] is None else cell(v("max")), cell(v("rate", 24.0)),
            "--" if not v("days", 24.0) or v("days", 24.0)[0] is None else "%.1f" % v("days", 24.0)[0],
            "--" if not v("to_target", 24.0) or v("to_target", 24.0)[0] is None else "%.0f h" % v("to_target", 24.0)[0], cell(v("routes")), cell(v("ships"))))
    print("  days: only for a good that runs down; to target: only for one that grows below its max (or demand); -- = not that case or not measured")
    if "(view)" in rows:
        print("  ERROR of the last computation: %s" % (rows["(view)"].get(("error", 0.0)) or (0, 0, "?"))[2])
    return show_gather(conn, data, now, args, heading=False)


def show_gather(conn, data, now, args, heading=True):
    rows, at = figures(conn, "gather")
    if heading:
        head("gather", "gather against buy per reserve good", at, data, now)
    print("GATHER OR BUY | credits a unit: what a gathered unit cost, the best ask to buy it, the best bid to sell it")
    print("  %-26s %12s %6s %10s %10s  %s" % ("item", "gather cost", "runs", "best ask", "best bid", "where"))
    for item, r in sorted(rows.items()):
        g, a, b = r.get(("gather_cost", 0.0)), r.get(("ask", 0.0)), r.get(("bid", 0.0))
        shown = lambda e: "not measured" if not e or e[0] is None else "%.1f" % e[0]
        print("  %-26s %12s %6s %10s %10s  ask: %s; bid: %s" % (item[:26], shown(g), num(g[1]) if g else "0", shown(a), shown(b),
                                                              a[2] if a else "--", b[2] if b else "--"))
    return 0


def show_xp(conn, data, now, args):
    rows, at = figures(conn, "xp")
    head("xp", "XP per ship-hour, last 24 h, from the hourly skill samples (stats_pilot_hour)", at, data, now)
    roles = roles_of(args.get("member"))
    found = sorted(((s.split("|")[0], s.split("|")[1], r[("xp_per_ship_hour", 24.0)]) for s, r in rows.items() if "|" in s and ("xp_per_ship_hour", 24.0) in r),
                   key=lambda x: (x[0], -(x[2][0] or 0)))
    print("PER ROLE AND SKILL (XP per ship-hour, n = pilots that gained):")
    shown = 0
    for role, skill, (value, n, _text) in found:
        if role in roles:
            print("  %-9s %-22s %10s  n %d" % (role, skill, "%.1f" % value if value is not None else "not measured", n or 0))
            shown += 1
    if not shown:
        print("  not measured: no skill moved between two hourly samples in the window (stats_pilot_hour needs two samples)")
    routes = sorted(((s, r[("route_xp_per_ship_hour", 24.0)]) for s, r in rows.items() if ("route_xp_per_ship_hour", 24.0) in r), key=lambda x: -(x[1][0] or 0))
    print("PER ROUTE (all skills, XP per ship-hour on the route, n = pilot-hours):")
    for rid, (value, n, _text) in routes[:int(args.get("top", 25))]:
        print("  %-44s %10s  n %d" % (rid[:44], "%.1f" % value if value is not None else "not measured", n or 0))
    if not routes:
        print("  not measured: no XP gain on record in the window")
    pilots = sorted(((s, r[("hours_to_tier", 24.0)]) for s, r in rows.items() if ("hours_to_tier", 24.0) in r), key=lambda x: (x[1][0] is None, x[1][0] or 0, x[0]))
    pilots = [p for p in pilots if args.get("member") is None or division.ROLES.get(role_of(p[0], data)) == args.get("member")]
    print("PER SHIP: hours to the next Piloting tier at its own pace (%d ships, %d with a pace):" % (len(pilots), sum(1 for p in pilots if p[1][0] is not None)))
    for pilot, (value, n, text) in pilots[:int(args.get("top", 25))]:
        print("  %-18s %10s  %s" % (pilot[:18], "%.0f h" % value if value is not None else "not measured", text))
    return 0


def show_upgrades(conn, data, now, args):
    rows, at = figures(conn, "upgrades")
    head("upgrades", "per ship: its hull and tier, Piloting against the next tier, empty module slots", at, data, now)
    if not rows:
        print("  not measured: no ship in the table ships")
        return 0
    print("  %-18s %4s %8s %8s %6s %6s %6s  %s" % ("ship", "tier", "piloting", "needs", "weapon", "defense", "utility", "hull and the next tier's hulls of its class"))
    for pilot, r in sorted(rows.items()):
        if args.get("member") and division.ROLES.get(role_of(pilot, data)) != args.get("member"):
            continue
        needs = r.get(("piloting_next", 0.0))
        print("  %-18s %4s %8s %8s %6s %6s %6s  %s" % (pilot[:18], cell(r.get(("tier", 0.0))), cell(r.get(("piloting", 0.0))),
                                                    "none" if needs and needs[0] == 0 else cell(needs),
                                                    cell(r.get(("empty_weapon", 0.0))), cell(r.get(("empty_defense", 0.0))), cell(r.get(("empty_utility", 0.0))),
                                                    (r.get(("tier", 0.0)) or (0, 0, ""))[2][:110]))
    print("  needs: the Piloting the next tier's hulls of its class ask (none: the catalog names none); weapon/defense/utility: empty slots of the hull "
          "(hulls) against the modules fitted (ship_modules)")
    return 0


def show_alerts(conn, data, now, args):
    rows, at = figures(conn, "alerts")
    head("alerts", "control chart: the newest hour against median +- %g x %g x MAD of its own 7-day hourly history (n >= %d)" % (MAD_K, MAD_SCALE, MIN_N), at, data, now)
    out = [(s, r[("alert", 0.0)]) for s, r in rows.items() if ("alert", 0.0) in r]
    raised = [x for x in out if str(x[1][2]).startswith("OUT")]
    print("  %d series watched, %d out of their band" % (len(out), len(raised)))
    for subject, (value, n, text) in sorted(out, key=lambda x: (not str(x[1][2]).startswith("OUT"), not x[0].startswith("Fleet"), x[0])):
        if str(text).startswith("OUT") or subject.startswith("Fleet"):
            print("  %-44s %s" % (subject[:44], text))
    return 0


def show_refill(conn, data, now, args):
    """The three tables of `hive.py refill`, from stats_refill."""
    at = conn.execute("SELECT MAX(t) FROM stats_refill").fetchone()[0]
    head("refill", "what comes back by itself, per hour, from the store's raw readings (7 days)", at, data, now,
         "a rise between two readings is the least that came back; median over recovery events (a take, then rises before the next take)")
    import hive
    _books, where = hive.books(data)
    top = int(args.get("top", 25))
    print("BIDS that came back after a take, per station and item | per h = units an hour, the median over events (q1-q3), n events; ours = events "
          "after a sale of ours | sum/h = hive.py's least-that-is-sure sum over the hours watched; a best bid is one step of a ladder (hive.bid_moves)")
    print("  %-30s %-24s %9s %9s %13s %4s %10s %4s %9s %9s %6s" % ("station", "item", "units now", "per h", "q1-q3", "n", "ours per h", "n", "sum/h", "taken/h", "hours"))
    found = conn.execute("SELECT place, what, now, median, q1, q3, events, ours_median, ours, per_hour, taken_per_hour, hours FROM stats_refill "
                         "WHERE kind = 'bid' AND events > 0 ORDER BY median DESC LIMIT ?", (top,)).fetchall()
    for base, item, units, med, q1, q3, n, ours, n_ours, sums, taken, hours in found:
        print("  %-30s %-24s %9s %9s %13s %4d %10s %4d %9s %9s %6.1f" % (hive.label(base, where)[:30], item[:24], num(units), num(med), "%s-%s" % (num(q1), num(q3)),
                                                                     n, num(ours) if ours is not None else "--", n_ours, num(sums), num(taken), hours))
    if not found:
        print("  not measured: no bid came back after a take in the store's raw moves")
    for kind, title in (("field", "FIELDS that grew back"), ("herd", "HERDS that regrew")):
        found = conn.execute("SELECT place, what, now, median, q1, q3, events, per_hour, taken_per_hour, hours, readings FROM stats_refill "
                             "WHERE kind = ? AND events > 0 ORDER BY median DESC LIMIT ?", (kind, top)).fetchall()
        print("%s | per h = the median over the readings that rose (units or animals an hour between two readings), n rises; sum/h = hive.py's rises over the "
              "hours watched" % title)
        print("  %-44s %-18s %9s %9s %13s %4s %9s %9s %6s %8s" % ("place", "what", "now", "per h", "q1-q3", "n", "sum/h", "taken/h", "hours", "readings"))
        for place, what, units, med, q1, q3, n, sums, taken, hours, readings in found:
            print("  %-44s %-18s %9s %9s %13s %4d %9s %9s %6.1f %8d" % (place[:44], what[:18], num(units), "%.1f" % med, "%.1f-%.1f" % (q1, q3), n,
                                                                    "%.1f" % sums if sums is not None else "--", "%.1f" % taken if taken is not None else "--", hours, readings))
        if not found:
            print("  not measured: no %s rose between two readings in the store's raw readings" % kind)
    return 0


def show_status(conn, data, now, args):
    head("status", "the parts of stats.py: when each last ran, its rows and seconds, its last fault", None, data, now)
    for part in PARTS:
        at = meta_get(conn, "stats.%s.at" % part)
        print("  %-8s last %s, %s rows, %s s%s" % (part, stamp(int(at)) if at else "never", meta_get(conn, "stats.%s.rows" % part, "--"),
                                                  meta_get(conn, "stats.%s.seconds" % part, "--"),
                                                  " | FAULT %s" % meta_get(conn, "stats.%s.error" % part) if meta_get(conn, "stats.%s.error" % part) else ""))
    for table in TABLES:
        if has_table(conn, table):
            print("  %-20s %8d rows" % (table, conn.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0]))
    return 0


def ready(data):
    """True when the store's read copy holds stats_refill with rows (hive.py refill reads it; before, its own records)."""
    import store
    conn = store.connect(data)
    if conn is None:
        return False
    try:
        return has_table(conn, "stats_refill") and conn.execute("SELECT COUNT(*) FROM stats_refill").fetchone()[0] > 0
    finally:
        conn.close()


SHOW = {"kpi": show_kpi, "contribution": show_contribution, "classes": show_classes, "time": show_time, "supply": show_supply, "gather": show_gather,
        "xp": show_xp, "upgrades": show_upgrades, "alerts": show_alerts, "refill": show_refill, "status": show_status}


def main(argv):
    args, words, it = {}, [], iter(argv)
    for word in it:
        if word in ("--hours", "--member", "--data", "--root", "--top"):
            args[word[2:]] = next(it, "")
        elif not word.startswith("--"):
            words.append(word)
    view = words[0] if words else ""
    if view not in SHOW:
        print("STATS | name a view: %s | hive.py stats <view> [--hours N] [--member <Member>]" % ", ".join(VIEWS_SHOWN))
        return 2
    if str(args.get("member", "")).lower() in ("", "all"):
        args.pop("member", None)
    if args.get("member"):
        named = next((m for m in division.MEMBERS if args["member"].lower() in (m.lower(), division_of(m).lower())), None)
        if named is None:
            print("STATS | no member `%s`: %s" % (args["member"], ", ".join(division.MEMBERS)))
            return 1
        args["member"] = named
    data = args.get("data") or division.DATA
    if view == "alerts":                                   # Q75 (3), errors.log ENT-112: our bases first, read from the files
        __import__("basewatch").show(data, time.time())
    computed = {"kpi": (1, 6, 24, 72)}.get(view, (24,))
    if args.get("hours") and view not in ("upgrades", "classes", "refill", "status", "alerts", "supply", "gather") and \
            float(args["hours"]) not in computed:
        print("STATS %s | --hours %s: not measured: the store computes this view over %s hours; shown: those" % (
            view.upper(), args["hours"], ", ".join(str(h) for h in computed)))
    import store
    conn = store.connect(data)
    if conn is None:
        print("STATS %s | not measured: no read copy at %s (the service `store` publishes it)" % (view.upper(), Path(data) / "store" / "read.db"))
        return 1
    try:
        if not has_table(conn, "stats_figures"):
            print("STATS %s | not measured: the store's read copy holds no table of stats.py yet (the store computes them in its pass)" % view.upper())
            return 1
        return SHOW[view](conn, data, time.time(), args)
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
