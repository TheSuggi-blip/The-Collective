#!/usr/bin/env python3
"""Fleet collector of The Collective -- our own ships' live state, as files.

WHAT: asks the fleet engine (through its gate) for the state of every pilot it
flies and writes it into the unit's data folder, outside the repository:

    <FLEET_DATA>/fleet.json            one row per ship, totals, totals per division
    <FLEET_DATA>/ships/<name>.json     one file per ship: position, hull, cargo,
                                       modules, skills, missions, what it is doing
    <FLEET_DATA>/history.json          credits and ship count over time (capped)

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
HISTORY_EVERY = 300          # seconds between two history samples
HISTORY_CAP = 576            # 48 hours of samples
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
        "state_at": text(st.get("updatedAt"), 30),
    }


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
        history.append([int(now), total["credits"], total["ships"]])
        write(DATA / "history.json", history[-HISTORY_CAP:])
    hour_ago = [h for h in history if now - h[0] <= 3900]
    if len(hour_ago) >= 2 and hour_ago[-1][0] > hour_ago[0][0]:
        total["credits_per_hour"] = round((hour_ago[-1][1] - hour_ago[0][1]) * 3600 / (hour_ago[-1][0] - hour_ago[0][0]))
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
