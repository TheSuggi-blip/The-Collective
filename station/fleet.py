#!/usr/bin/env python3
"""Fleet collector of The Collective -- our own ships' live state, as files.

WHAT: asks the fleet engine (through its gate) for the state of every pilot it
flies and writes it into the unit's data folder, outside the repository:

    <FLEET_DATA>/fleet.json            one row per ship, totals, totals per division
    <FLEET_DATA>/ships/<name>.json     one file per ship: position, hull, cargo,
                                       modules, skills, missions, what it is doing
    <FLEET_DATA>/history.json          one sample a minute, 48 hours: credits, ships,
                                       credits earned, one-time rewards, ore, missions,
                                       per division
    <FLEET_DATA>/orders/<name>.json    (read) what a fleet script is doing with a pilot
                                       ({"what", "since"}), written and kept fresh by that
                                       script; a file not touched for 20 minutes is ignored
    <FLEET_DATA>/onetime.json          (read) one-time rewards, written by the birth
                                       script; kept apart so CPH counts recurring income

Metrics in fleet.json, over the last 60 minutes:
    cph              change of all wallets per hour with one-time rewards taken
                     out: what the fleet earns minus what it spends
    cph_per_ship     cph / ships
    earned_per_hour  credits earned per hour, one-time rewards excluded,
                     spending not subtracted
    net_per_hour     change of all wallets per hour (one-time rewards included)
    credits_per_ship, ore_per_hour, missions_per_hour; the same per division

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
WINDOW = 3600                # the metrics' window
MIN_SPAN = 300               # no rate from less than five minutes of samples
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # the gate is inside the unit

# Pilot name -> division and its Admiral (COLLECTIVE.md; names: <role>-<n>).
ROLES = {
    "miner": ("Mining", "Zero"), "trader": ("Trade", "Mercury"), "hauler": ("Logistics", "Apollo"),
    "drone": ("Military", "Apophis"), "scout": ("Intel", "Oracle"),
}
ROLE_NAME = re.compile(r"([a-z]+)-(\d{1,4})")
STATS = ("credits_earned", "credits_spent", "ore_mined", "trades_completed", "missions_completed", "jumps_completed",
         "systems_explored", "ships_lost", "ships_destroyed", "pirates_destroyed", "damage_taken", "time_played")


def text(v, n=120):
    return str(v)[:n] if isinstance(v, (str, int, float)) and not isinstance(v, bool) else ""


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0


def division_of(name):
    """(division, admiral, number) from a pilot's name; pilots outside the naming rule are unassigned."""
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
        "name": name, "division": division, "admiral": admiral, "number": number,
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


def totals(rows):
    out = {"ships": len(rows), "connected": 0, "credits": 0, "cargo_used": 0, "cargo_capacity": 0, "idle": 0, "divisions": {}}
    for r in rows:
        d = out["divisions"].setdefault(r["division"], {"admiral": r["admiral"], "ships": 0, "credits": 0, "cargo_used": 0,
                                                        "cargo_capacity": 0, "idle": 0})
        for bucket in (out, d):
            bucket["credits"] += r["credits"]
            bucket["cargo_used"] += r["cargo_used"]
            bucket["cargo_capacity"] += r["cargo_capacity"]
            bucket["idle"] += 1 if r["activity"]["kind"] == "idle" else 0
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


def sample(now, rows):
    """One history row: [t, credits, ships, earned, onetime, ore, missions, {division: [...]}]."""
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
    return [int(now), sum(r["credits"] for r in rows), len(rows), sum(r["earned"] for r in rows), sum(one.values()),
            sum(r["ore_mined"] for r in rows), sum(r["missions_done"] for r in rows), divisions]


def rates(history, now):
    """Metrics over the last WINDOW seconds, for the fleet and per division."""
    full = [h for h in history if isinstance(h, list) and len(h) == 8 and now - h[0] <= WINDOW + 90]
    if len(full) < 2 or full[-1][0] - full[0][0] < MIN_SPAN:
        return None
    a, b = full[0], full[-1]
    hours = (b[0] - a[0]) / 3600

    def per_hour(x, y):
        return round((y - x) / hours)

    out = {"window_minutes": round((b[0] - a[0]) / 60), "net_per_hour": per_hour(a[1], b[1]),
           "cph": per_hour(a[1] - a[4], b[1] - b[4]), "earned_per_hour": per_hour(a[3] - a[4], b[3] - b[4]),
           "ore_per_hour": per_hour(a[5], b[5]),
           "missions_per_hour": round((b[6] - a[6]) / hours, 1), "divisions": {}}
    out["cph_per_ship"] = round(out["cph"] / b[2]) if b[2] else 0
    for division, d in b[7].items():
        e = a[7].get(division, [0, 0, 0, 0, 0, 0])
        cph = per_hour(e[1] - e[3], d[1] - d[3])
        out["divisions"][division] = {"cph": cph, "cph_per_ship": round(cph / d[0]) if d[0] else 0,
                                      "earned_per_hour": per_hour(e[2] - e[3], d[2] - d[3]),
                                      "net_per_hour": per_hour(e[1], d[1]), "ore_per_hour": per_hour(e[4], d[4])}
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


def collect_once(last):
    """One pass: ask the engine, write the files. `last` holds what was written before."""
    now = time.time()
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
    rows = sorted((ship_row(a) for a in accounts), key=lambda r: (r["division"], r["number"], r["name"]))
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
    total = totals(rows)
    history = read(DATA / "history.json", [])
    if not history or now - history[-1][0] >= HISTORY_EVERY:
        history.append(sample(now, rows))
        write(DATA / "history.json", history[-HISTORY_CAP:])
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
