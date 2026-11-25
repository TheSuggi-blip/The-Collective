#!/usr/bin/env python3
"""tug.py -- a ship of ours stranded in space with a tank that cannot reach fuel is towed to a station by the game's tug and refuelled.

WHAT: reads every ship file (data/fleet/ships/) and picks a ship that stands in space -- not docked, not travelling or
      jumping, connected, in no fight, flown by no runner -- whose tank is under --below and cannot reach the nearest
      station with fuel (fuelplan.py: 1.5 a jump, and 2 for the way to the dock), or that has no such station in
      reach. For each one (at most --limit a pass) it takes the pilot by hand and sends `distress_signal` with
      `distress_type` tow: the game's tug docks the ship at the nearest public station in about five minutes for an
      idle-ship recovery fee (500 cr on 2026-11-22). The pass records the call in data/fleet/tug.json. A later pass
      settles each recorded tow: docked, the ship is refuelled (`refuel`) and released; still in space after --wait
      minutes, it is released and named. Every answer is printed, with one RESULT line a ship. A tow that ends at a
      station selling no fuel (`refuel` answers no_fuel_source) is named in a HALT line and kept in
      data/fleet/tug_dry.json: no tow is called again for that ship in that system while its tank stays low (each tow
      there costs the fee and docks it at the same dry station); a hand brings it fuel cells or a pump ship.
RULES:
  - It never takes a ship a runner flies or another hand holds (division.may, gate.take): a runner that stops on a
    dry tank leaves its pilot free, and the tug takes it on the next pass.
  - --dry-run sends no call and writes no file: it names the ships it would tow and the tows it would settle.
  - A ship is released at the end of its tow, whatever happened.
WHY:  on 2026-11-22 two hunters sat dry in space for hours, one 21 jumps out with 4 fuel, after their sell_at sold no
      fuel (errors.log ENT-142); each was towed by hand (requests.log ENT-369, ENT-376: one script, dry run first,
      then the five-minute pass).

USAGE:
  tug.py [--dry-run] [--below 25] [--limit 3] [--wait 15] [--pilot <name>]

Stdlib only. ASCII only."""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  own ships only, the hand mark
import fuelplan                                   # noqa: E402  the chart and the stations with fuel

BELOW = 25                     # a tank under this is looked at
DOCK_WAY = 2                   # fuel kept for the way from the arrival point to the dock
LIMIT = 3                      # tows called in one pass
WAIT = 15                      # minutes a tow may take before it is given up
REPO = Path(__file__).resolve().parents[2] / "game"


def stranded(ship, order, lanes, stations, below=BELOW, mark=""):
    """The reason the ship should be towed, or None. `order` is what its fresh order file says ('' for none);
    `mark` is this shell's hand mark: a ship held by this hand may be towed, one held by any other may not."""
    fuel = ship.get("fuel")
    max_fuel = ship.get("max_fuel")
    has_mods = isinstance(ship.get("modules"), list)
    if has_mods:
        per_jump = fuelplan.ship_jump_cost(ship)
        dock_way = int(round(fuelplan.ship_dock_reserve(ship)))
    else:
        per_jump = max(fuelplan.PER_JUMP, round(float(max_fuel) / 55.0, 1)) if isinstance(max_fuel, (int, float)) and max_fuel > 0 else fuelplan.PER_JUMP
        dock_way = max(DOCK_WAY, int(round(per_jump)))
    eff_below = min(30, max(below, int(round(per_jump * 3 + dock_way))))
    if not isinstance(fuel, (int, float)) or fuel >= eff_below:
        return None
    if ship.get("docked") or ship.get("docked_at") or ship.get("in_transit") or ship.get("jumping"):
        return None
    if ship.get("status", "connected") != "connected":
        return None
    activity = ship.get("activity") if isinstance(ship.get("activity"), dict) else {}
    if "battle" in str(activity.get("kind") or "") or ship.get("in_battle"):
        return None
    if order and order != mark:
        return None
    here = ship.get("system")
    near = fuelplan.nearest_fuel(lanes, here, stations) if here else None
    if near is None:
        return "fuel %s at %s, no station with fuel in reach" % (fuel, here)
    if fuel < per_jump * near[0] + dock_way:
        return "fuel %s at %s, %d jumps from fuel at %s" % (fuel, here, near[0], near[3])
    return None


def settle(row, ship, now, wait=WAIT):
    """What a pass does with a recorded tow: `refuel` once the ship is docked, `wait` while the tug may still come,
    `give up` after `wait` minutes."""
    if ship.get("docked") or ship.get("docked_at"):
        return "refuel"
    return "give up" if now - float(row.get("at") or 0) > wait * 60 else "wait"


def refused_no_fuel(answer):
    """True when a `refuel` answer says the station sells no fuel and the hold carries no cells."""
    return "no_fuel_source" in str(answer or "")


def dry_hold(row, ship):
    """True while a ship recorded dry at a station without fuel stays in that system with its tank below the line
    it was towed under: calling the tug again would only dock it at the same dry station for another fee."""
    if not isinstance(row, dict):
        return False
    fuel = ship.get("fuel")
    return (ship.get("system") == row.get("system") and isinstance(fuel, (int, float))
            and fuel <= float(row.get("fuel") or 0) + 5)


def dry_path(data):
    return Path(data) / "fleet" / "tug_dry.json"


def load_dry(data):
    try:
        rows = json.loads(dry_path(data).read_text(encoding="utf-8"))
        return rows if isinstance(rows, dict) else {}
    except (OSError, ValueError):
        return {}


def save_dry(data, rows):
    path = dry_path(data)
    tmp = path.with_suffix(".json.%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(rows, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def safe_stations(data, repo=REPO):
    """Fuel stations excluding pirate strongholds: a ship near only a pirate station still needs the tug."""
    far = fuelplan.strongholds(repo)
    return {s: v for s, v in fuelplan.fuel_stations(data).items() if s not in far}


def ships(data):
    out = {}
    for path in sorted((Path(data) / "fleet" / "ships").glob("*.json")):
        try:
            out[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
    return out


def state_path(data):
    return Path(data) / "fleet" / "tug.json"


def load_state(data):
    try:
        rows = json.loads(state_path(data).read_text(encoding="utf-8"))
        return rows if isinstance(rows, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(data, rows):
    path = state_path(data)
    tmp = path.with_suffix(".json.%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(rows, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def say(text):
    print("%s %s" % (time.strftime("%H:%M:%S", time.gmtime()), text), flush=True)


def raw(pilot, action, params):
    import gate
    status, out = gate.call("post", "/accounts/%s/raw" % gate.q(pilot),
                            {"toolGroup": "spacemolt", "action": action, "params": params}, timeout=120)
    return status, str(out)[:300]


def run_pass(data, now=None, dry=False, below=BELOW, limit=LIMIT, wait=WAIT, only="", mark=None):
    """Programmatic entry point for automated background tug passes (e.g. from wallet.py serve)."""
    now = time.time() if now is None else float(now)
    mark = division.hand_mark() if mark is None else mark
    fleet = ships(data)
    lanes = fuelplan.chart(REPO)[0]
    stations = safe_stations(data, REPO)
    state = load_state(data)
    dry_rows = load_dry(data)
    dry_before = dict(dry_rows)
    done = 0
    for pilot, row in sorted(state.items()):
        if only and pilot != only:
            continue
        what = settle(row, fleet.get(pilot, {}), now, wait)
        if what == "wait":
            say("%s: tug called %.0f min ago, waiting" % (pilot, (now - float(row.get("at") or 0)) / 60))
            if not dry:
                try:
                    import gate
                    os.utime(gate.hold_file(pilot))
                except OSError:
                    pass
            continue
        if dry:
            say("%s: would %s (dry run)" % (pilot, what))
            continue
        import gate
        result = "the tug did not dock it in %d minutes" % wait
        if what == "refuel":
            status, out = raw(pilot, "refuel", {})
            say("%s refuel: %s %s" % (pilot, status, out))
            result = "towed and refuelled"
            if refused_no_fuel(out):
                here = fleet.get(pilot, {})
                dry_rows[pilot] = {"at": now, "system": here.get("system") or row.get("system"),
                              "fuel": here.get("fuel") if isinstance(here.get("fuel"), (int, float)) else row.get("fuel")}
                result = "towed, but the station sells no fuel: refuel refused"
                print("HALT: tug %s: docked in %s at a station that sells no fuel; no tow is called for it there again: "
                      "a hand brings fuel cells (buy, refuel) or a pump ship" % (pilot, dry_rows[pilot]["system"]), flush=True)
        say(gate.release(pilot))
        print("RESULT tug %s: %s; called with fuel %s at %s" % (pilot, result, row.get("fuel"), row.get("system")),
              flush=True)
        state.pop(pilot, None)
        done += 1
    for pilot, ship in sorted(fleet.items()):
        if only and pilot != only:
            continue
        if pilot in state or limit <= 0:
            continue
        if pilot in dry_rows and not dry_hold(dry_rows[pilot], ship):
            dry_rows.pop(pilot, None)                               # fuelled or moved since: the tug may serve it again
        why = stranded(ship, division.order_of(pilot, data, now), lanes, stations, below, mark)
        if not why:
            continue
        if pilot in dry_rows:
            say("%s: no tow: dry at a station without fuel in %s since %s UTC (tug_dry.json)"
                % (pilot, dry_rows[pilot].get("system"),
                   time.strftime("%H:%M", time.gmtime(float(dry_rows[pilot].get("at") or 0)))))
            continue
        if dry:
            say("%s: would call the tug: %s (dry run)" % (pilot, why))
            limit -= 1
            continue
        ok, reason = division.may(pilot, data)
        if not ok:
            say("%s: not taken: %s" % (pilot, reason))
            continue
        import gate
        gate.take(pilot)
        status, out = raw(pilot, "distress_signal", {"distress_type": "tow"})
        say("%s distress_signal tow (%s): %s %s" % (pilot, why, status, out))
        if status == 200 and '"error"' not in out[:200]:
            state[pilot] = {"at": now, "fuel": ship.get("fuel"), "system": ship.get("system")}
        else:
            say(gate.release(pilot))
            print("RESULT tug %s: the tug was refused: %s" % (pilot, out[:160]), flush=True)
        limit -= 1
    if not dry:
        save_state(data, state)
        if dry_rows != dry_before:
            save_dry(data, dry_rows)
    if done or state or only or dry:
        say("tug: %d settled, %d waiting%s" % (done, len(state), " (dry run)" if dry else ""))
    return 0


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    def opt(name, default):
        return type(default)(argv[argv.index(name) + 1]) if name in argv else default
    return run_pass(
        division.DATA, time.time(),
        dry="--dry-run" in argv,
        below=opt("--below", BELOW),
        limit=opt("--limit", LIMIT),
        wait=opt("--wait", WAIT),
        only=opt("--pilot", ""),
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
