#!/usr/bin/env python3
"""Fleet collector of The Collective -- our own ships' live state, as files.

WHAT: asks the fleet engine (through its gate) for the state of every pilot it
flies and writes it into the unit's data folder, outside the repository:

    <FLEET_DATA>/fleet.json            one row per ship, totals, totals per division
    <FLEET_DATA>/ships/<name>.json     one file per ship: position, hull, cargo,
                                       modules, skills, missions, what it is doing
    <FLEET_DATA>/history.json          one sample a minute, 48 hours: credits, ships,
                                       credits earned, one-time rewards, ore, missions,
                                       per division; ships working, parked and adrift,
                                       and the meters
    <FLEET_DATA>/meters.json           the meters: fuel bought, hull repaired and the
                                       credits that left with them, counted from pass to
                                       pass, in all and per division
    <FLEET_DATA>/orders/<name>.json    (read) what a fleet script is doing with a pilot
                                       ({"what", "since"}), written and kept fresh by that
                                       script; a file not touched for 20 minutes is ignored
    <FLEET_DATA>/onetime.json          (read) one-time money, written by the birth script
                                       and the runners: a reward the game pays once per
                                       pilot (above zero) and what was bought for it
                                       (below zero); kept apart so the metrics count
                                       steady money only

Metrics in fleet.json (`totals.rates`): steady money, per hour, over the last
hour at the top level and over 1, 6 and 24 hours under `windows`:
    income_per_hour  what the game's counter of credits earned rose by, less the
                     one-time rewards: sales and repeatable rewards
    costs_per_hour   everything spent (earned minus the change of the wallets),
                     less what was bought for one-time rewards: fuel, repairs,
                     goods, modules
    cph              income minus costs: what the fleet makes by itself
    cph_per_ship     cph / ships
    fuel_cr_per_hour, repair_cr_per_hour, fuel_units_per_hour, hull_points_per_hour
                     from the meters; absent until both ends of the window carry them
    the same per division; `ships_changed` marks a window in which the fleet grew
    (a new pilot's first credits then count as income)
    earned_per_hour (= income_per_hour), net_per_hour (all wallets, one-time
    money included), ore_per_hour, missions_per_hour: kept for older readers
Ships in the totals: `working` (a loop, a goal or a script's order), `parked`
(docked without work: it costs nothing), `adrift` (in space without work);
`idle` = parked + adrift.

Every file is written whole and then renamed, so a reader never sees half a
file. A ship's file is rewritten only when its content changed. Nothing here
goes to the game: the engine answers from its own mirror of the game's state.
It sends no command.

Who reads it: the command station (station/server.py), the six agents with
their file tools, and scripts.

It runs as the service `fleet` of the unit (/srv/collective/services/fleet/run).
Settings come from the environment: FLEET_GATE (address of the gate, required),
FLEET_DATA (default /srv/collective/data/fleet), FLEET_EVERY (seconds, default 10).

Stdlib only. ASCII only. Run: python3 -I -B fleet.py [--once]
"""

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

GATE = os.environ.get("FLEET_GATE", "").rstrip("/")
DATA = Path(os.environ.get("FLEET_DATA", "/srv/collective/data/fleet"))
EVERY = max(5, int(os.environ.get("FLEET_EVERY", "10")))
HISTORY_EVERY = 60           # seconds between two history samples
HISTORY_CAP = 2880           # 48 hours of samples
WINDOW = 3600                # the metrics' first window
WINDOWS = (("1h", 3600), ("6h", 6 * 3600), ("24h", 24 * 3600))
MIN_SPAN = 300               # no rate from less than five minutes of samples
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # the gate is inside the unit

# Pilot name -> division and its Admiral (COLLECTIVE.md; names: <role>-<n>).
# A flagship's name carries no role word: <FLEET_DATA>/flagships.json names its
# division, that division's Admiral and whose ship it is
# ({pilot: {admiral, division, role, of}}), read at every pass. The six flagships
# and the guard (`sentinel-<n>`) are the command group: the Command division.
FLAGSHIPS = {}
ROLES = {
    "miner": ("Mining", "Zero"), "trader": ("Trade", "Mercury"), "hauler": ("Logistics", "Apollo"),
    "drone": ("Military", "Apophis"), "scout": ("Intel", "Oracle"), "sentinel": ("Command", "Unity"),
}
ROLE_NAME = re.compile(r"([a-z]+)-(\d{1,4})")
STATS = ("credits_earned", "credits_spent", "ore_mined", "trades_completed", "missions_completed", "jumps_completed",
         "systems_explored", "ships_lost", "ships_destroyed", "pirates_destroyed", "damage_taken", "time_played")


def text(v, n=120):
    return str(v)[:n] if isinstance(v, (str, int, float)) and not isinstance(v, bool) else ""


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0


def division_of(name):
    """(division, admiral, number) from a pilot's name; a flagship from its entry (number 0: first of its division);
    pilots outside both are unassigned."""
    entry = FLAGSHIPS.get(name or "")
    if entry:
        return (text(entry.get("division"), 20) or "Unassigned", text(entry.get("admiral"), 20), 0)
    m = ROLE_NAME.fullmatch(name or "")
    if m and m.group(1) in ROLES:
        return ROLES[m.group(1)] + (int(m.group(2)),)
    return ("Unassigned", "", 0)


def file_name(name):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)[:60] or "pilot"


def activity(account):
    """What the engine is doing with this pilot right now, in one short record."""
    loop = account.get("loop") or {}
    if loop.get("running"):
        return {"kind": "loop", "type": text(loop.get("type"), 40), "since": text(loop.get("startedAt"), 30)}
    goal = account.get("executingGoal") or {}
    if account.get("hasExecutingGoal") and goal:
        return {"kind": "goal", "type": text(goal.get("goalType"), 40), "since": text(goal.get("startedAt"), 30)}
    job = account.get("runningJob") or {}
    if account.get("hasRunningJob") and job:
        return {"kind": "job", "type": text(job.get("goalType") or job.get("type"), 40), "since": text(job.get("startedAt"), 30)}
    return {"kind": "idle", "type": "", "since": ""}


ORDER_FRESH = 20 * 60        # seconds an order file counts without being touched


def orders(now):
    """{pilot name: (what, since)} from the order files the fleet's scripts keep fresh."""
    out = {}
    folder = DATA / "orders"
    for path in folder.glob("*.json") if folder.is_dir() else []:
        try:
            if now - path.stat().st_mtime > ORDER_FRESH:
                continue
            d = json.loads(path.read_text(encoding="utf-8"))
            out[text(d.get("pilot"), 40)] = (text(d.get("what"), 60), text(d.get("since"), 30))
        except (OSError, ValueError, AttributeError):
            continue
    return out


def apply_orders(rows, now):
    """A ship under a script's order carries it; between two goals it is at work, not idle."""
    given = orders(now)
    for row in rows:
        what, since = given.get(row["name"], ("", ""))
        row["order"] = what
        if what and row["activity"]["kind"] == "idle":
            row["activity"] = {"kind": "order", "type": what, "since": since}
    return rows


def ship_row(account):
    """The short row of fleet.json for one account of the engine's dashboard data."""
    st = account.get("state") or {}
    player, ship, loc = st.get("player") or {}, st.get("ship") or {}, st.get("location") or {}
    name = text(account.get("username"), 40)
    division, admiral, number = division_of(name)
    loop = account.get("loop") or {}
    return {
        "name": name, "division": division, "admiral": admiral, "number": number, "flagship": name in FLAGSHIPS,
        "flagship_of": text((FLAGSHIPS.get(name) or {}).get("of"), 20),
        "empire": text(player.get("empire"), 20), "status": text(account.get("status"), 20),
        "credits": num(player.get("credits")),
        "class": text(ship.get("class_name") or ship.get("class_id"), 40),
        "hull": num(ship.get("hull")), "max_hull": num(ship.get("max_hull")),
        "shield": num(ship.get("shield")), "max_shield": num(ship.get("max_shield")),
        "fuel": num(ship.get("fuel")), "max_fuel": num(ship.get("max_fuel")),
        "cargo_used": num(ship.get("cargo_used")), "cargo_capacity": num(ship.get("cargo_capacity")),
        "system": text(loc.get("system_id"), 80), "system_name": text(loc.get("system_name"), 80),
        "poi": text(loc.get("poi_id"), 80), "poi_name": text(loc.get("poi_name"), 80),
        "docked": text(loc.get("docked_at"), 80), "in_transit": bool(loc.get("in_transit")),
        "dest_poi": text(loc.get("transit_dest_poi_name"), 80), "arrival_tick": num(loc.get("transit_arrival_tick")),
        "activity": activity(account),
        "loop_failures": num(loop.get("consecutiveFailures")), "loop_last_failure": text(loop.get("lastFailure"), 200),
        "missions": len((st.get("missions") or {}).get("active") or []),
        "earned": num((player.get("stats") or {}).get("credits_earned")),
        "ore_mined": num((player.get("stats") or {}).get("ore_mined")),
        "missions_done": num((player.get("stats") or {}).get("missions_completed")),
        "top_skill": top_skill(st.get("skills")),
        "state_at": text(st.get("updatedAt"), 30),
    }


def top_skill(skills):
    """[name, level] of the pilot's highest skill (XP breaks a tie), or ["", 0]."""
    best = ("", 0, 0)
    for name, v in (skills or {}).items() if isinstance(skills, dict) else []:
        if isinstance(v, dict) and (num(v.get("level")), num(v.get("xp"))) > (best[1], best[2]):
            best = (text(name, 40), num(v.get("level")), num(v.get("xp")))
    return [best[0], best[1]]


def ship_detail(account, row):
    """The full file of one ship: the row plus cargo, modules, skills, missions, counters."""
    st = account.get("state") or {}
    player, ship, loc = st.get("player") or {}, st.get("ship") or {}, st.get("location") or {}
    stats = player.get("stats") or {}
    out = dict(row)
    out["home_base"] = text(player.get("home_base"), 80)
    out["security"] = text(loc.get("security_status"), 80)
    out["lanes"] = [text(c, 80) for c in (loc.get("connections") or [])][:40]
    out["ship"] = {k: num(ship.get(k)) for k in ("armor", "speed", "shield_recharge", "cpu_used", "cpu_capacity", "power_used",
                                                 "power_capacity", "weapon_slots", "defense_slots", "utility_slots")}
    out["cargo"] = [{"item": text(c.get("item_id"), 60), "name": text(c.get("item_name"), 60), "quantity": num(c.get("quantity"))}
                    for c in (st.get("cargo") or []) if isinstance(c, dict)][:200]
    out["modules"] = [{"type": text(m.get("type_id"), 60), "name": text(m.get("name"), 60), "kind": text(m.get("type"), 30),
                       "slot": text(m.get("slot"), 20)} for m in (st.get("modules") or []) if isinstance(m, dict)][:60]
    out["skills"] = {text(k, 40): {"level": num(v.get("level")), "xp": num(v.get("xp")), "next": num(v.get("next_level_xp"))}
                     for k, v in (st.get("skills") or {}).items() if isinstance(v, dict) and (num(v.get("xp")) or num(v.get("level")))}
    missions = []
    for m in ((st.get("missions") or {}).get("active") or [])[:10]:
        missions.append({
            "title": text(m.get("title"), 80), "type": text(m.get("type"), 30), "percent": num(m.get("percent_complete")),
            "credits": num((m.get("rewards") or {}).get("credits")), "expires_in_ticks": num(m.get("expires_in_ticks")),
            "objectives": [{"text": text(o.get("description"), 120), "current": num(o.get("current")), "required": num(o.get("required")),
                            "done": bool(o.get("completed")), "system": text(o.get("system_id"), 80)}
                           for o in (m.get("objectives") or []) if isinstance(o, dict)][:12]})
    out["mission_list"] = missions
    goal = account.get("executingGoal") or {}
    out["goal"] = {"type": text(goal.get("goalType"), 40), "options": goal.get("goalOptions") if isinstance(goal.get("goalOptions"), dict) else {}}
    loop = account.get("loop") or {}
    out["loop"] = {"type": text(loop.get("type"), 40), "running": bool(loop.get("running")), "options": loop.get("options") if isinstance(loop.get("options"), dict) else {},
                   "last_step": text(loop.get("lastStep"), 200), "last_step_at": text(loop.get("lastStepAt"), 30)}
    out["stats"] = {k: num(stats.get(k)) for k in STATS}
    return out


def work_state(row):
    """working (a loop, a goal, a script's order), parked (docked without work) or adrift (in space without work)."""
    if row["activity"]["kind"] != "idle":
        return "working"
    return "parked" if row["docked"] else "adrift"


def totals(rows):
    out = {"ships": len(rows), "connected": 0, "credits": 0, "cargo_used": 0, "cargo_capacity": 0, "idle": 0,
           "working": 0, "parked": 0, "adrift": 0, "divisions": {}}
    for r in rows:
        d = out["divisions"].setdefault(r["division"], {"admiral": r["admiral"], "ships": 0, "credits": 0, "cargo_used": 0,
                                                        "cargo_capacity": 0, "idle": 0, "working": 0, "parked": 0, "adrift": 0})
        state = work_state(r)
        for bucket in (out, d):
            bucket["credits"] += r["credits"]
            bucket["cargo_used"] += r["cargo_used"]
            bucket["cargo_capacity"] += r["cargo_capacity"]
            bucket["idle"] += 1 if state != "working" else 0
            bucket[state] += 1
        d["ships"] += 1
        out["connected"] += 1 if r["status"] == "connected" else 0
    return out


def onetime_by_division(now):
    """One-time rewards received up to `now`, summed per division and in all."""
    out = {}
    for row in read(DATA / "onetime.json", []):
        if isinstance(row, list) and len(row) == 4 and isinstance(row[0], (int, float)) and row[0] <= now:
            division = division_of(row[1] if isinstance(row[1], str) else "")[0]
            out[division] = out.get(division, 0) + num(row[3])
    return out


METERS = {"fuel_units": 0, "fuel_cr": 0, "hull_points": 0, "repair_cr": 0, "burned": 0, "clean": [0, 0, 0, 0], "div": {}}
PREV = {}                    # pilot name -> (fuel, hull, credits, cargo used) at the pass before


def meter(row, prev, meters):
    """Count what one ship burned and bought between two passes.

    Fuel that rose while docked was bought; hull that rose while docked was repaired. When the hold did
    not change and the wallet did not rise in the same pass, the credits that left are the price: a clean
    reading. A refuel that shares its pass with a sale or a purchase is priced at the average of the clean
    readings so far (at nothing while there is none). `clean` holds fuel units, their credits, hull points,
    their credits of the clean readings.
    """
    fuel, hull = row["fuel"] - prev[0], row["hull"] - prev[1]
    paid, same_hold = prev[2] - row["credits"], row["cargo_used"] == prev[3]
    if fuel < 0:
        meters["burned"] += -fuel
    if not row["docked"] or (fuel <= 0 and hull <= 0):
        return
    fuel, hull = max(fuel, 0), max(hull, 0)
    clean = meters["clean"]
    price_fuel = clean[1] / clean[0] if clean[0] else None
    price_hull = clean[3] / clean[2] if clean[2] else None
    if paid >= 0 and same_hold and not (fuel and hull):
        fuel_cr, hull_cr = (paid, 0) if fuel else (0, paid)
        if fuel:
            clean[0] += fuel
            clean[1] += paid
        else:
            clean[2] += hull
            clean[3] += paid
    elif paid >= 0 and same_hold:                 # both in one pass: the fuel at its average price, the rest is the repair
        fuel_cr = min(paid, round(fuel * price_fuel)) if price_fuel is not None else round(paid * fuel / (fuel + hull))
        hull_cr = paid - fuel_cr
    else:                                         # a sale or a purchase in the same pass hides the price
        fuel_cr = round(fuel * price_fuel) if price_fuel is not None else 0
        hull_cr = round(hull * price_hull) if price_hull is not None else 0
    division = meters["div"].setdefault(row["division"], [0, 0, 0, 0])
    for index, value in enumerate((fuel, fuel_cr, hull, hull_cr)):
        division[index] += value
    meters["fuel_units"] += fuel
    meters["fuel_cr"] += fuel_cr
    meters["hull_points"] += hull
    meters["repair_cr"] += hull_cr


def sample(now, rows, meters=None):
    """One history row: [t, credits, ships, earned, onetime, ore, missions, {division: [...]}, extra].

    extra: {"w": [working, parked, adrift], "dw": {division: working}} and, with the meters,
    "m": [fuel units, fuel credits, hull points, repair credits, fuel burned] and "d": the first four per division.
    """
    one = onetime_by_division(now)
    divisions = {}
    for r in rows:
        d = divisions.setdefault(r["division"], [0, 0, 0, 0, 0, 0])   # ships, credits, earned, onetime, ore, missions
        d[0] += 1
        d[1] += r["credits"]
        d[2] += r["earned"]
        d[4] += r["ore_mined"]
        d[5] += r["missions_done"]
    for division, value in one.items():
        divisions.setdefault(division, [0, 0, 0, 0, 0, 0])[3] = value
    states = [work_state(r) for r in rows]
    extra = {"w": [states.count("working"), states.count("parked"), states.count("adrift")], "dw": {}}
    for r, state in zip(rows, states):
        extra["dw"][r["division"]] = extra["dw"].get(r["division"], 0) + (1 if state == "working" else 0)
    if meters is not None:
        extra["m"] = [meters["fuel_units"], meters["fuel_cr"], meters["hull_points"], meters["repair_cr"], meters["burned"]]
        extra["d"] = {division: list(values) for division, values in meters["div"].items()}
    return [int(now), sum(r["credits"] for r in rows), len(rows), sum(r["earned"] for r in rows), sum(one.values()),
            sum(r["ore_mined"] for r in rows), sum(r["missions_done"] for r in rows), divisions, extra]


def one_time_until(one, t):
    """One-time money booked up to t, as {division: [rewards, bought]}; the whole fleet under ''."""
    out = {"": [0, 0]}
    for row in one:
        if isinstance(row, list) and len(row) == 4 and isinstance(row[0], (int, float)) and row[0] <= t:
            value = num(row[3])
            for key in ("", division_of(row[1] if isinstance(row[1], str) else "")[0]):
                out.setdefault(key, [0, 0])[0 if value > 0 else 1] += abs(value)
    return out


def figures(hours, ships, credits, earned, one):
    """Steady money per hour from three changes over a window: the wallets, the game's counter of credits
    earned, and the one-time money ([rewards, bought])."""
    income = earned - one[0]
    costs = earned - credits - one[1]
    net = income - costs
    return {"income_per_hour": round(income / hours), "costs_per_hour": round(costs / hours), "cph": round(net / hours),
            "cph_per_ship": round(net / hours / ships) if ships else 0, "one_time_per_hour": round((one[0] - one[1]) / hours)}


def window(history, now, seconds, one):
    """The steady money of one window, for the fleet and per division; None from less than five minutes of samples."""
    full = [h for h in history if isinstance(h, list) and len(h) >= 8 and now - h[0] <= seconds + 90]
    if len(full) < 2 or full[-1][0] - full[0][0] < MIN_SPAN:
        return None
    a, b = full[0], full[-1]
    hours = (b[0] - a[0]) / 3600
    before, after = one_time_until(one, a[0]), one_time_until(one, b[0])

    def booked(key):
        return [after.get(key, [0, 0])[i] - before.get(key, [0, 0])[i] for i in (0, 1)]

    out = figures(hours, b[2], b[1] - a[1], b[3] - a[3], booked(""))
    out.update({"minutes": round((b[0] - a[0]) / 60), "ships_changed": a[2] != b[2], "divisions": {}})
    xa, xb = (a[8] if len(a) > 8 else {}), (b[8] if len(b) > 8 else {})
    metered = "m" in xa and "m" in xb
    if metered:
        for index, key in enumerate(("fuel_units_per_hour", "fuel_cr_per_hour", "hull_points_per_hour", "repair_cr_per_hour", "fuel_burned_per_hour")):
            out[key] = round((xb["m"][index] - xa["m"][index]) / hours)
    for division, d in b[7].items():
        e = a[7].get(division, [0, 0, 0, 0, 0, 0])
        row = figures(hours, d[0], d[1] - e[1], d[2] - e[2], booked(division))
        if metered:
            da, db = (xa.get("d") or {}).get(division) or [0, 0, 0, 0], (xb.get("d") or {}).get(division) or [0, 0, 0, 0]
            row.update({"fuel_cr_per_hour": round((db[1] - da[1]) / hours), "repair_cr_per_hour": round((db[3] - da[3]) / hours)})
        out["divisions"][division] = row
    return out


def rates(history, now, one=None):
    """Steady money per hour: the last hour at the top level, and one, six and 24 hours under `windows`.

    `one` is the one-time money ([t, pilot, title, credits] rows); by default the file the birth script
    and the runners keep.
    """
    one = read(DATA / "onetime.json", []) if one is None else one
    first = window(history, now, WINDOW, one)
    if first is None:
        return None
    full = [h for h in history if isinstance(h, list) and len(h) >= 8 and now - h[0] <= WINDOW + 90]
    a, b = full[0], full[-1]
    hours = (b[0] - a[0]) / 3600

    def per_hour(x, y):
        return round((y - x) / hours)

    out = dict(first)
    out.update({"window_minutes": first["minutes"], "earned_per_hour": first["income_per_hour"], "net_per_hour": per_hour(a[1], b[1]),
                "ore_per_hour": per_hour(a[5], b[5]), "missions_per_hour": round((b[6] - a[6]) / hours, 1)})
    out["divisions"] = {}
    for division, row in first["divisions"].items():
        d, e = b[7][division], a[7].get(division, [0, 0, 0, 0, 0, 0])
        out["divisions"][division] = dict(row, earned_per_hour=row["income_per_hour"], net_per_hour=per_hour(e[1], d[1]),
                                          ore_per_hour=per_hour(e[4], d[4]))
    out["windows"] = {name: (first if seconds == WINDOW else window(history, now, seconds, one)) for name, seconds in WINDOWS}
    return out


def write(path, value):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def read(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


POSITION = {}                # pilot name -> (system id, system name) last named by the engine


def row_order(row):
    """Roster order: by division; in it the division's own flagship, the other flagships by name, then the ships by number."""
    return (row["division"], row["number"], row.get("flagship_of") != row["admiral"], row["name"])


def load_flagships():
    """Read the flagship entries anew: a ship registered a minute ago stands in its division at the next pass."""
    found = read(DATA / "flagships.json", {})
    FLAGSHIPS.clear()
    if isinstance(found, dict):
        FLAGSHIPS.update({str(name): entry for name, entry in found.items() if isinstance(entry, dict)})


LOW_HOLD = 600               # seconds a pass that lists fewer pilots than the one before is held back
LOW = {}                     # "since": when the first such pass was seen


def of_fleet(rows):
    """The rows of the fleet. A pilot of the account that stands in no division (no role word, no flagship entry) is
    not of the fleet: it gets no row, no file and no place in a figure."""
    return [r for r in rows if r.get("division") != "Unassigned"]


def held(count, known, now, low=LOW):
    """True while a pass that lists fewer pilots than the one before is held back, LOW_HOLD seconds from the first.

    After a restart the engine signs its pilots in again over some minutes; a sample of a part of the fleet would read
    as credits lost and ships gone. A count that stays low for longer is the fleet as it is, and is written."""
    if count >= known:
        low.pop("since", None)
        return False
    low.setdefault("since", now)
    return now - low["since"] < LOW_HOLD


def collect_once(last):
    """One pass: ask the engine, write the files. `last` holds what was written before."""
    now = time.time()
    load_flagships()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    try:
        with OPENER.open(GATE + "/dashboard/data", timeout=25) as r:
            data = json.loads(r.read(60_000_000))
        accounts = [a for a in data.get("accounts", []) if isinstance(a, dict) and a.get("username")]
    except Exception as e:                      # the engine is away: keep the last rows, say so
        fleet = read(DATA / "fleet.json", {"ships": [], "totals": totals([])})
        fleet["engine"] = {"ok": False, "error": (type(e).__name__ + ": " + str(e))[:200], "checked_at": stamp}
        write(DATA / "fleet.json", fleet)
        return False
    rows = of_fleet(sorted((ship_row(a) for a in accounts), key=row_order))
    before = read(DATA / "fleet.json", {})
    known = len(of_fleet([s for s in before.get("ships") or [] if isinstance(s, dict)]))
    if held(len(rows), known, now):               # the engine signs its pilots in again: keep the last picture, write no sample
        before["engine"] = {"ok": False, "error": "%d of %d pilots signed in" % (len(rows), known), "checked_at": stamp}
        write(DATA / "fleet.json", before)
        return False
    apply_orders(rows, now)
    for row in rows:                              # between two systems the engine names none: keep the last one
        row["jumping"] = not row["system"]
        if row["system"]:
            POSITION[row["name"]] = (row["system"], row["system_name"])
        elif row["name"] in POSITION:
            row["system"], row["system_name"] = POSITION[row["name"]]
    by_name = {text(a.get("username"), 40): a for a in accounts}
    keep = set()
    for row in rows:
        fn = file_name(row["name"]) + ".json"
        keep.add(fn)
        detail = ship_detail(by_name[row["name"]], row)
        mark = json.dumps(detail, sort_keys=True)
        if last.get(fn) != mark:
            detail["written_at"] = stamp
            write(DATA / "ships" / fn, detail)
            last[fn] = mark
    for path in (DATA / "ships").glob("*.json"):   # a pilot the engine no longer flies
        if path.name not in keep:
            path.unlink()
            last.pop(path.name, None)
    for row in rows:                              # what each ship burned and bought since the pass before
        if row["status"] == "connected" and row["max_fuel"]:
            before = PREV.get(row["name"])
            if before:
                meter(row, before, METERS)
            PREV[row["name"]] = (row["fuel"], row["hull"], row["credits"], row["cargo_used"])
    total = totals(rows)
    history = read(DATA / "history.json", [])
    if not history or now - history[-1][0] >= HISTORY_EVERY:
        history.append(sample(now, rows, METERS))
        write(DATA / "history.json", history[-HISTORY_CAP:])
        write(DATA / "meters.json", METERS)
    total["credits_per_ship"] = round(total["credits"] / total["ships"]) if total["ships"] else 0
    total["earned"] = sum(r["earned"] for r in rows)
    total["onetime"] = sum(onetime_by_division(now).values())
    for division, d in total["divisions"].items():
        d["credits_per_ship"] = round(d["credits"] / d["ships"]) if d["ships"] else 0
    total["rates"] = rates(history, now)
    write(DATA / "fleet.json", {
        "updated_at": stamp, "engine": {"ok": True, "error": "", "checked_at": stamp, "started_at": text(data.get("startedAt"), 30)},
        "totals": total, "ships": rows})
    return True


def main():
    if not GATE:
        sys.exit("fleet: FLEET_GATE is not set")
    (DATA / "ships").mkdir(parents=True, exist_ok=True)
    last = {}
    saved = read(DATA / "meters.json", {})          # the meters count on over a restart
    if isinstance(saved, dict) and isinstance(saved.get("clean"), list) and len(saved["clean"]) == 4 and isinstance(saved.get("div"), dict):
        METERS.update({key: saved[key] for key in METERS if key in saved})
    for row in read(DATA / "fleet.json", {}).get("ships", []):   # positions survive a restart
        if isinstance(row, dict) and row.get("system"):
            POSITION[text(row.get("name"), 40)] = (text(row["system"], 80), text(row.get("system_name"), 80))
    if "--once" in sys.argv:
        print("fleet: one pass,", "ok" if collect_once(last) else "engine not reached")
        return
    print(f"fleet: collecting every {EVERY} s into {DATA}", flush=True)
    state = None
    while True:
        ok = collect_once(last)
        if ok != state:                           # say it once per change, not every pass
            print("fleet: engine reached" if ok else "fleet: engine not reached", flush=True)
            state = ok
        time.sleep(EVERY)


if __name__ == "__main__":
    main()
