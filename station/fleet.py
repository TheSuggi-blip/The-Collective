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
                                       steady money only. Its `Wallet top-up` rows are
                                       left out: they are the halves of a gift
    <FLEET_DATA>/gifts.jsonl           (read) the wallet guard's gifts between our own
                                       pilots (game/fleet/wallet.py): {"at", "from", "to",
                                       "credits"}; moved credits nobody earned or spent
    <FLEET_DATA>/presence.jsonl        one line per pilot the engine stopped listing ("sign": -1, with the credits
                                       and counters of its last reading) or lists again (+1, with what it holds
                                       now): {"at", "pilot", "sign", "credits", "earned", "spent"}
    <FLEET_DATA>/fleet.json `away`      the pilots of the fleet the engine holds signed out (`disconnected` in its
                                       GET /accounts): [{"name", "division"}]; each is signed in again by this
                                       collector (rejoin), so the list is empty but for some minutes
    <FLEET_DATA>/rejoin-off            (optional, by hand) empty: no pilot is signed in again; with names, one a
                                       line: those pilots are left signed out and are not named as away. The
                                       file STOP beside it also stops every sign-in
    <FLEET_DATA>/seed.json             {pilot: [first seen epoch, credits, earned, spent]}
                                       as the collector first saw each pilot; at the first
                                       start every pilot present is put at epoch 0

Metrics in fleet.json (`totals.rates`): steady money, per hour, over the last
hour at the top level and over 1, 6 and 24 hours under `windows`:
    income_per_hour  what the game's counter of credits earned rose by, less the
                     one-time rewards: sales and repeatable rewards
    costs_per_hour   everything spent (earned minus the change of the wallets),
                     less what was bought for one-time rewards: fuel, repairs,
                     goods, modules; a positive number lowers the net
    cph              income minus costs (of the rounded figures): what the fleet
                     makes by itself
    cph_per_ship     cph / ships
    fuel_cr_per_hour, repair_cr_per_hour, fuel_units_per_hour, hull_points_per_hour,
    metered_per_hour (fuel and repair credits together)
                     from the meters; absent until both ends of the window carry them
    spent_per_hour   the game's own counter of credits spent (fuel, repairs, goods,
                     modules; no tax, no gift), beside costs as a check; absent until
                     both ends of the window carry it
    transfers_per_hour  per division: credits our own gifts put into its wallets less
                     what they took out (gifts.jsonl); taken out of its change of
                     wallets. For the fleet the gifts cancel and nothing is taken out:
                     there it is the sum of the divisions' (0 while ONE_SIDED is off),
                     transfers_moved_per_hour all the credits the gifts moved and
                     transfers_unpaired_per_hour those of gifts whose record names one
                     side only (left out of every division while ONE_SIDED is off)
    presence         {left, back, credits, earned}: the pilots the engine stopped listing
                     and those it lists again in the window (presence.jsonl), and what that
                     took out of (-) or put into (+) the sums; left out of the figures, so a
                     ship that drops out of the engine's list is no loss
    seed             {pilots, credits, earned}: the pilots first seen in the window and
                     what they held then (seed.json); taken out of the change of the
                     wallets and of credits earned, so a new ship adds no income
    the same per division; `ships_changed` marks a window in which the fleet grew
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
    python3 -I -B fleet.py --backfill-seeds [--dry-run]   once, by the Fleet Admiral, after the
    install: the pilots of the last birth (birth.json, birth.log) go into seed.json at their
    registration time, so the windows that hold that birth leave their starting wallets out
"""

import calendar
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
TRANSFER = "Wallet top-up"   # wallet.py's title for the two halves of a gift between our own pilots in onetime.json
# What the game puts into a new pilot's wallet; its counters of credits earned and spent start at 0. Measured
# 2026-11-16 on every ship file: credits = 100 + earned - spent - weekly tax - gifts given + gifts received held to
# the credit for 121 pilots, old and new alike (the others gave or got gifts gifts.jsonl does not hold).
START_CREDITS = 100
# A gift whose record in gifts.jsonl names one side only (`reconstructed` from a run) moves no division while this is
# off. Measured 2026-11-16 on every ship file: the game's counters put each division's net gifts at 0 except Command
# -76,040 and Trade +76,040, while the 55 one-sided rows counted alone put Intel at +98,257 and Logistics at -81,212:
# their missing halves lay in the same division. True: the known side moves its division.
ONE_SIDED = False
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
        "spent": num((player.get("stats") or {}).get("credits_spent")),
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

    extra: {"w": [working, parked, adrift], "dw": {division: working}, "s": the game's counter of credits spent,
    "ds": {division: credits spent}} and, with the meters, "m": [fuel units, fuel credits, hull points, repair credits,
    fuel burned] and "d": the first four per division.
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
    extra = {"w": [states.count("working"), states.count("parked"), states.count("adrift")], "dw": {},
             "s": sum(r.get("spent", 0) for r in rows), "ds": {}}
    for r, state in zip(rows, states):
        extra["dw"][r["division"]] = extra["dw"].get(r["division"], 0) + (1 if state == "working" else 0)
        extra["ds"][r["division"]] = extra["ds"].get(r["division"], 0) + r.get("spent", 0)
    if meters is not None:
        extra["m"] = [meters["fuel_units"], meters["fuel_cr"], meters["hull_points"], meters["repair_cr"], meters["burned"]]
        extra["d"] = {division: list(values) for division, values in meters["div"].items()}
    return [int(now), sum(r["credits"] for r in rows), len(rows), sum(r["earned"] for r in rows), sum(one.values()),
            sum(r["ore_mined"] for r in rows), sum(r["missions_done"] for r in rows), divisions, extra]


def one_time_until(one, t):
    """One-time money booked up to t, as {division: [rewards, bought]}; the whole fleet under ''.

    A `Wallet top-up` row is no one-time money but one half of a gift between two of our pilots, read from gifts.jsonl
    instead (transfers). Counted here its plus half was a reward and its minus half a purchase: 2026-11-16 the fleet's
    income and costs both fell by every gift (over six hours by 63,149 and 40,591 cr an hour), the costs below zero.
    """
    out = {"": [0, 0]}
    for row in one:
        if isinstance(row, list) and len(row) == 4 and isinstance(row[0], (int, float)) and row[0] <= t and row[2] != TRANSFER:
            value = num(row[3])
            for key in ("", division_of(row[1] if isinstance(row[1], str) else "")[0]):
                out.setdefault(key, [0, 0])[0 if value > 0 else 1] += abs(value)
    return out


def read_gifts(path):
    """[(epoch, giver, taker, credits)] of the wallet guard's gifts between our own pilots (wallet.py: gifts.jsonl).

    A line that is no JSON object, a time or an amount that is no number and a gift of 0 credits (`unsure`: the gate did
    not answer and the wallet did not show it) are left out. A side the record does not know (a `reconstructed` row
    names only one) is an empty name: that side is counted nowhere.
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.readlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and num(row.get("at")) and num(row.get("credits")):
            out.append((row["at"], text(row.get("from"), 40), text(row.get("to"), 40), row["credits"]))
    return out


def transfers(gifts, t0, t1):
    """The gifts of (t0, t1] as ({division: credits received less credits given}, credits moved, credits of gifts whose
    record names one side only).

    Nobody earned or spent a gift: the receiving division's wallets rose by it without a sale, the giving division's fell
    without a purchase. Within one division, and for the fleet, the two halves cancel. A gift with one side unknown moves
    no division while ONE_SIDED is off.
    """
    net, moved, unpaired = {}, 0, 0
    for at, giver, taker, credits in gifts:
        if t0 < at <= t1:
            moved += credits
            if not (giver and taker):
                unpaired += credits
                if not ONE_SIDED:
                    continue
            for name, sign in ((giver, -1), (taker, 1)):
                if name:
                    division = division_of(name)[0]
                    net[division] = net.get(division, 0) + sign * credits
    return net, moved, unpaired


def seeded(seeds, t0, t1):
    """The pilots first seen in (t0, t1] (seed.json), as {division: [pilots, credits, earned, spent]}, all under ''.

    A pilot first seen inside a window brings its first wallet into the window's change of the wallets, and its counters
    as the game had them: none of it was earned or spent while we watched. 2026-11-16 a hundred new pilots joined the
    fleet within half an hour, each with START_CREDITS.
    """
    out = {"": [0, 0, 0, 0]}
    for name, entry in seeds.items() if isinstance(seeds, dict) else []:
        if isinstance(entry, list) and len(entry) >= 3 and t0 < num(entry[0]) <= t1:
            values = (1, num(entry[1]), num(entry[2]), num(entry[3]) if len(entry) > 3 else 0)
            for key in ("", division_of(name)[0]):
                bucket = out.setdefault(key, [0, 0, 0, 0])
                for index, value in enumerate(values):
                    bucket[index] += value
    return out


def read_presence(path):
    """[(epoch, pilot, sign, credits, earned, spent)] of presence.jsonl; a line that does not read is left out."""
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.readlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and num(row.get("at")) and row.get("sign") in (-1, 1) and isinstance(row.get("pilot"), str):
            out.append((row["at"], row["pilot"], row["sign"], num(row.get("credits")), num(row.get("earned")), num(row.get("spent"))))
    return out


def present(events, t0, t1):
    """The pilots the engine stopped listing and those it lists again in (t0, t1], as {division: [left, back, credits,
    earned, spent]} with the sums signed (what left is below zero), all under ''.

    A pilot the engine no longer lists takes its wallet and its counters out of the fleet's sums, and brings them back
    when it is listed again: nothing of it was spent or earned. 2026-11-16, 22:17 UTC: the engine listed 245 of 246
    pilots, and the fleet's income read -71,022 cr an hour while fuel alone cost 46,420.
    """
    out = {"": [0, 0, 0, 0, 0]}
    for at, name, sign, credits, earned, spent in events:
        if t0 < at <= t1:
            for key in ("", division_of(name)[0]):
                bucket = out.setdefault(key, [0, 0, 0, 0, 0])
                bucket[0 if sign < 0 else 1] += 1
                for index, value in enumerate((credits, earned, spent)):
                    bucket[2 + index] += sign * value
    return out


def note_presence(old, rows, seeds, now, path=None):
    """Write down each pilot the last picture held and this pass does not (-1, with what it held then) and each pilot
    this pass holds again (+1, with what it holds now); the events written.

    `old` are the ship rows of the fleet file before this pass, `seeds` the seed record as read. A pilot the seed record
    does not know is no return but a first sight: note_seeds takes it. Called only for a pass that is written (held()
    keeps a short count back for ten minutes first), so a pilot is written down as gone when the engine left it out for
    that long.
    """
    was = {r["name"]: r for r in of_fleet([s for s in old if isinstance(s, dict)]) if isinstance(r.get("name"), str)}
    if not was:
        return []
    names = {r["name"] for r in rows}
    events = [{"at": int(now), "pilot": name, "sign": -1, "credits": num(r.get("credits")), "earned": num(r.get("earned")), "spent": num(r.get("spent"))}
              for name, r in sorted(was.items()) if name not in names]
    events += [{"at": int(now), "pilot": r["name"], "sign": 1, "credits": r["credits"], "earned": r["earned"], "spent": r.get("spent", 0)}
               for r in rows if r["name"] not in was and isinstance(seeds, dict) and r["name"] in seeds]
    if events:
        with open(path or DATA / "presence.jsonl", "a", encoding="utf-8") as handle:
            handle.write("".join(json.dumps(event, sort_keys=True) + "\n" for event in events))
    return events


def note_seeds(seeds, rows, now):
    """(record, changed): every pilot not yet in the seed record put in as [now, credits, earned, spent].

    With no record at all (the first start, or a file that does not read) every pilot present goes in at epoch 0,
    older than any window: what the fleet held before the collector kept seeds is no birth.
    """
    first = not isinstance(seeds, dict)
    if first and not rows:
        return seeds, False
    seeds = {} if first else seeds
    changed = False
    for r in rows:
        if r["name"] not in seeds:
            seeds[r["name"]] = [0 if first else int(now), r["credits"], r["earned"], r.get("spent", 0)]
            changed = True
    return seeds, changed


def figures(hours, ships, credits, earned, one):
    """Steady money per hour from three changes over a window: the wallets, the game's counter of credits
    earned, and the one-time money ([rewards, bought]). Net is income less costs as rounded, so the three
    figures a reader sees always agree (net = income - costs)."""
    income = round((earned - one[0]) / hours)
    costs = round((earned - credits - one[1]) / hours)
    return {"income_per_hour": income, "costs_per_hour": costs, "cph": income - costs,
            "cph_per_ship": round((income - costs) / ships) if ships else 0, "one_time_per_hour": round((one[0] - one[1]) / hours)}


def window(history, now, seconds, one, gifts=(), seeds=None, presence=()):
    """The steady money of one window, for the fleet and per division; None from less than five minutes of samples.

    A division's change of wallets leaves out the gifts it got and gave (transfers); the fleet's does not need to, the
    gifts cancel. The pilots first seen in the window take their first wallet and counters out of both (seeded), and so
    do the pilots the engine stopped listing or lists again (present).
    """
    full = [h for h in history if isinstance(h, list) and len(h) >= 8 and now - h[0] <= seconds + 90]
    if len(full) < 2 or full[-1][0] - full[0][0] < MIN_SPAN:
        return None
    a, b = full[0], full[-1]
    hours = (b[0] - a[0]) / 3600
    before, after = one_time_until(one, a[0]), one_time_until(one, b[0])
    (given, moved, unpaired), new = transfers(gifts, a[0], b[0]), seeded(seeds, a[0], b[0])
    moves = present(presence, a[0], b[0])

    def booked(key):
        return [after.get(key, [0, 0])[i] - before.get(key, [0, 0])[i] for i in (0, 1)]

    def seed(born):
        return {"pilots": born[0], "credits": born[1], "earned": born[2]}

    def joined(key):
        """[credits, earned, spent] that the pilots first seen and those that left or came back brought into the sums."""
        s, p = new.get(key, [0, 0, 0, 0]), moves.get(key, [0, 0, 0, 0, 0])
        return [s[1] + p[2], s[2] + p[3], s[3] + p[4]]

    def absent(key):
        p = moves.get(key, [0, 0, 0, 0, 0])
        return {"left": p[0], "back": p[1], "credits": p[2], "earned": p[3]}

    born, off = new[""], joined("")
    out = figures(hours, b[2], b[1] - a[1] - off[0], b[3] - a[3] - off[1], booked(""))
    out.update({"minutes": round((b[0] - a[0]) / 60), "ships_changed": a[2] != b[2], "divisions": {}, "seed": seed(born), "presence": absent(""),
                "transfers_per_hour": round(sum(given.values()) / hours), "transfers_moved_per_hour": round(moved / hours),
                "transfers_unpaired_per_hour": round(unpaired / hours)})
    xa, xb = (a[8] if len(a) > 8 else {}), (b[8] if len(b) > 8 else {})
    metered = "m" in xa and "m" in xb
    if metered:
        for index, key in enumerate(("fuel_units_per_hour", "fuel_cr_per_hour", "hull_points_per_hour", "repair_cr_per_hour", "fuel_burned_per_hour")):
            out[key] = round((xb["m"][index] - xa["m"][index]) / hours)
        out["metered_per_hour"] = out["fuel_cr_per_hour"] + out["repair_cr_per_hour"]
    spent = all(isinstance(x.get("s"), (int, float)) and isinstance(x.get("ds"), dict) for x in (xa, xb))
    if spent:
        out["spent_per_hour"] = round((xb["s"] - xa["s"] - off[2]) / hours)
    for division, d in b[7].items():
        e = a[7].get(division, [0, 0, 0, 0, 0, 0])
        born, got, off = new.get(division, [0, 0, 0, 0]), given.get(division, 0), joined(division)
        row = figures(hours, d[0], d[1] - e[1] - got - off[0], d[2] - e[2] - off[1], booked(division))
        row.update({"transfers_per_hour": round(got / hours), "seed": seed(born), "presence": absent(division)})
        if metered:
            da, db = (xa.get("d") or {}).get(division) or [0, 0, 0, 0], (xb.get("d") or {}).get(division) or [0, 0, 0, 0]
            row.update({"fuel_cr_per_hour": round((db[1] - da[1]) / hours), "repair_cr_per_hour": round((db[3] - da[3]) / hours)})
            row["metered_per_hour"] = row["fuel_cr_per_hour"] + row["repair_cr_per_hour"]
        if spent:
            row["spent_per_hour"] = round((num(xb["ds"].get(division)) - num(xa["ds"].get(division)) - off[2]) / hours)
        out["divisions"][division] = row
    return out


def rates(history, now, one=None, gifts=None, seeds=None, presence=None):
    """Steady money per hour: the last hour at the top level, and one, six and 24 hours under `windows`.

    `one` is the one-time money ([t, pilot, title, credits] rows), `gifts` the gifts between our pilots (read_gifts) and
    `seeds` the seed record; by default the files the birth script, the runners, the wallet guard and the collector keep.
    """
    one = read(DATA / "onetime.json", []) if one is None else one
    gifts = read_gifts(DATA / "gifts.jsonl") if gifts is None else gifts
    seeds = read(DATA / "seed.json", {}) if seeds is None else seeds
    presence = read_presence(DATA / "presence.jsonl") if presence is None else presence
    first = window(history, now, WINDOW, one, gifts, seeds, presence)
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
    out["windows"] = {name: (first if seconds == WINDOW else window(history, now, seconds, one, gifts, seeds, presence)) for name, seconds in WINDOWS}
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


LOOK_EVERY = 60              # seconds between two looks at the engine's own list while a pilot is away
LOOK_QUIET = 600             # ... after a look that found none away
REJOIN_AFTER = 600           # seconds the engine must have run before a pilot is signed in again
REJOIN_EVERY = 900           # seconds between two tries for one pilot
REJOIN_MOST = 5              # pilots signed in again in one look
AWAY = {}                    # "at": the last look, "every": seconds to the next, "list": the pilots away, "first"/"tried": {pilot: when}


def signed_out(listed):
    """The pilots of the fleet the engine lists `disconnected` (GET /accounts), by name. One it shows `reconnecting` is
    being signed in by the engine itself; a pilot of the account that stands in no division was signed out by us."""
    return sorted(a["username"] for a in listed if isinstance(a, dict) and isinstance(a.get("username"), str) and a.get("status") == "disconnected"
                  and division_of(a["username"])[0] != "Unassigned")


def left_out():
    """(True while pilots may be signed in again, the pilots that are left signed out on purpose) from the files STOP and
    rejoin-off of the fleet's data folder."""
    try:
        names = {line.strip() for line in (DATA / "rejoin-off").read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()}
        switched_off = not names
    except OSError:
        names, switched_off = set(), False
    return not (switched_off or (DATA / "STOP").exists()), names


def rejoin(now, uptime, away=AWAY, opener=None, allowed=True, never=()):
    """Look at the engine's own list for pilots it signed out for good, and sign them in again: (the pilots away, the
    pilots asked back in at this look).

    2026-11-16, 22:07:29 UTC: in a stall of the server one mining pilot's reconnect did not authenticate in time (close
    code 4002). The engine's library holds that close final: the pilot was never connected again and nobody was told.
    Its dashboard left the pilot out, this collector wrote no picture for ten minutes (held), the pilot flew nothing for
    70 minutes and the game towed the drifting ship for 500 cr, until Morpheus signed it in by hand (queue.log ENT-123:
    POST /accounts {"username": the pilot}, answer 202, connected 5 s later). His guards are kept: never a pilot the
    engine shows `reconnecting`, never within REJOIN_AFTER seconds of an engine start (a second connection replaces
    the first, and that close is final too), never a pilot that is not of the fleet. And: only a pilot seen signed out
    at two looks, one try per pilot in REJOIN_EVERY seconds, REJOIN_MOST pilots a look. A look that finds none away is
    followed by the next after LOOK_QUIET seconds. `allowed` False: the pilots away are named and nobody is asked;
    a pilot of `never` is left signed out and not named (left_out). Not flown yet: no pilot has been signed out since
    it was written.
    """
    if now - away.get("at", 0) < away.get("every", LOOK_EVERY):
        return away.get("list", []), []
    away["at"], away["every"] = now, LOOK_QUIET
    opener = opener or OPENER
    try:
        with opener.open(GATE + "/accounts", timeout=25) as r:
            listed = json.loads(r.read(60_000_000)).get("accounts") or []
    except Exception:                               # the engine is away: the pass says so
        return away.get("list", []), []
    out = [name for name in signed_out(listed) if name not in never]
    first, tried = away.setdefault("first", {}), away.setdefault("tried", {})
    for name in [n for n in first if n not in out]:
        del first[name]
    away["list"] = out
    if out:
        away["every"] = LOOK_EVERY
    asked = []
    for name in out:
        seen = first.setdefault(name, now)
        if (not allowed or not isinstance(uptime, (int, float)) or uptime < REJOIN_AFTER or now - seen < LOOK_EVERY or now - tried.get(name, 0) < REJOIN_EVERY
                or len(asked) >= REJOIN_MOST):
            continue
        tried[name] = now
        request = urllib.request.Request(GATE + "/accounts", data=json.dumps({"username": name}).encode("utf-8"), method="POST",
                                         headers={"Content-Type": "application/json"})
        try:
            with opener.open(request, timeout=25) as r:
                r.read(1_000_000)
            asked.append(name)
        except Exception:
            continue
    return out, asked


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
    seen = read(DATA / "seed.json", None)
    away = AWAY.get("list", [])
    if away or len(rows) < max(known, len(seen) if isinstance(seen, dict) else 0):     # a pilot we know is not listed: signed out for good?
        uptime = data.get("uptimeMs")
        allowed, never = left_out()
        away, asked = rejoin(now, uptime / 1000 if isinstance(uptime, (int, float)) and not isinstance(uptime, bool) else None, allowed=allowed, never=never)
        if asked:
            print("fleet: %d pilot(s) the engine had signed out: asked back in" % len(asked), flush=True)
    away = [{"name": name, "division": division_of(name)[0]} for name in away]
    if held(len(rows), known, now):               # the engine signs its pilots in again: keep the last picture, write no sample
        before["engine"] = {"ok": False, "error": "%d of %d pilots signed in" % (len(rows), known), "checked_at": stamp}
        before["away"] = away
        write(DATA / "fleet.json", before)
        return False
    note_presence(before.get("ships") or [], rows, read(DATA / "seed.json", None), now)   # who left the engine's list, who is back
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
    seeds, grown = note_seeds(read(DATA / "seed.json", None), rows, now)   # read anew each pass: a backfill may have written it
    if grown:
        write(DATA / "seed.json", seeds)
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
    total["rates"] = rates(history, now, seeds=seeds if isinstance(seeds, dict) else {})
    write(DATA / "fleet.json", {
        "updated_at": stamp, "engine": {"ok": True, "error": "", "checked_at": stamp, "started_at": text(data.get("startedAt"), 30)},
        "totals": total, "ships": rows, "away": away})
    return True


REGISTERED = re.compile(r"(\d\d):(\d\d):(\d\d) (.+?): registered\b.*")


def backfill_seeds(data, dry_run=False):
    """Put the pilots of the last birth into the seed record at their registration time; the lines to print.

    A record begun after a birth holds its pilots at epoch 0, and the windows that hold the birth would count their
    starting wallets as money made. birth.json names the pilots and the birth's start, birth.log the time of day each
    was registered (the last such line of a pilot wins; a time of day before the start is of the next day). A pilot is
    put in with START_CREDITS and its counters at 0, as the game makes it, when the record lacks it or holds it at epoch
    0; one the record holds with a time of its own is left. Every other pilot of fleet.json the record lacks goes in at
    epoch 0. The collector reads the record anew at every pass and only adds to it, so this may run while it runs.
    """
    data = Path(data)
    seeds = read(data / "seed.json", None)
    seeds = dict(seeds) if isinstance(seeds, dict) else {}
    birth = read(data / "birth.json", {})
    birth = birth if isinstance(birth, dict) else {}
    names = {n for n in birth.get("registered") or [] if isinstance(n, str)}
    try:
        start = calendar.timegm(time.strptime(str(birth.get("started_at"))[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return ["seed: birth.json names no start (started_at): nothing written"]
    try:
        lines = (data / "birth.log").read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        lines = []
    born = {}
    for line in lines:
        m = REGISTERED.fullmatch(line.strip())
        if m and m.group(4) in names:
            t = start - start % 86400 + int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            born[m.group(4)] = t + 86400 if t < start - 60 else t
    put, kept, zero = [], [], 0
    for name, t in sorted(born.items()):
        entry = seeds.get(name)
        if isinstance(entry, list) and entry and num(entry[0]):
            kept.append(name)
            continue
        seeds[name] = [t, START_CREDITS, 0, 0]
        put.append(name)
    fleet = read(data / "fleet.json", {})
    for row in (fleet.get("ships") or [] if isinstance(fleet, dict) else []):
        if isinstance(row, dict) and isinstance(row.get("name"), str) and row["name"] not in seeds:
            seeds[row["name"]] = [0, num(row.get("credits")), num(row.get("earned")), num(row.get("spent"))]
            zero += 1
    out = ["seed: the birth of %s: %d pilots named, %d found registered in birth.log" % (birth.get("started_at"), len(names), len(born)),
           "seed: %d put at their registration time (%s .. %s UTC) with %d cr; %d left as the record had them; %d other pilots put at epoch 0"
           % (len(put), time.strftime("%H:%M:%S", time.gmtime(min(born[n] for n in put))) if put else "--",
              time.strftime("%H:%M:%S", time.gmtime(max(born[n] for n in put))) if put else "--", START_CREDITS, len(kept), zero)]
    if dry_run:
        out.append("seed: --dry-run, %s not written" % (data / "seed.json"))
    elif put or zero:
        write(data / "seed.json", seeds)
        out.append("seed: written %s (%d pilots)" % (data / "seed.json", len(seeds)))
    else:
        out.append("seed: nothing to change")
    return out


def main():
    if "--backfill-seeds" in sys.argv:              # needs no gate: it reads and writes the data folder only
        print("\n".join(backfill_seeds(DATA, "--dry-run" in sys.argv)))
        return
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
