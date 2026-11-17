#!/usr/bin/env python3
"""mine.py -- one pilot mines at one field for a set time, through the engine's mining loop.

WHAT: starts the engine's mining loop (mine until the hold is full, fly to the
      station, put the ore into the pilot's storage there, fly back), lets it
      run for --minutes, stops it, and waits until the pilot is docked or still.
      Mining trains the Mining skill and flying trains Piloting; the ore stays
      in storage for crafting or a later sale. With --sell-items the run ends
      with a sale: the pilot docks at the station, sells the named goods from
      its hold and from its storage there into the bids that stand at the
      named price or more (the book is read before every sale, and no unit
      goes under the price), and puts the rest of its hold into storage.
      Without it, a run that ends with more than five units aboard docks at
      the station and stores them, so the next empty_hold route opens.
RULES:
  - Stops at once when data/fleet/STOP appears.
  - Told to stop (the run host's stop file or its end, a signal), the run ends whole: it stops the engine's
    loop and writes its row with the reason in the notes; it sells and stores nothing, because whoever stopped
    it wants the ship now. 2026-11-17: eight stopped runs left their loops running and wrote no row.
  - The loop is the engine's: this script only starts and stops it and keeps the
    pilot's order file fresh, so the dispatcher gives the pilot nothing else.
WHY:  a ship without paying work still earns skill, and its ore feeds the workshop.

USAGE:
  mine.py <pilot> <system:poi> <system:poi:base> [--minutes M] [--sell-items item:min_price,...] [--route ID] [--deposit faction]

With --deposit faction the engine's loop and the last load go into the faction's storage at the station (an
outpost of ours has no personal storage; the route field `"deposit": "faction"`).

Writes one row to data/routes/runs.jsonl (minutes, credits before and after, ore mined).
The wallet is read from the engine's answer for the account (state.credits), the ore
from the collector's file of the ship (stats.ore_mined). A run that could not read its
wallet carries the note `wallet not read`: it says nothing about credits.
Stdlib only. ASCII only.
"""

import atexit
import fcntl
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GATE = os.environ.get("FLEET_GATE", "http://172.30.0.32:7580")
DATA = os.environ.get("FLEET_DATA_ROOT", "/srv/collective/data")
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def credits_of(account):
    """The wallet in the engine's answer for one account, or None when the answer holds none."""
    value = ((account or {}).get("state") or {}).get("credits")
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def ore_of(ship):
    """Units mined so far in the collector's file of one ship, or None when it holds no count."""
    value = ((ship or {}).get("stats") or {}).get("ore_mined")
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


DOCK_TRIES = 10                # tries of the dock goal before a sale, 30 s apart: about five minutes


def settled(call, quoted, tries=20, pause=15):
    """Waits until the engine shows neither an executing goal nor a running job for the account; False when it never did."""
    for _ in range(tries):
        account = call("GET", "/accounts/" + quoted)[1]
        if not (account.get("hasExecutingGoal") or account.get("hasRunningJob")):
            return True
        time.sleep(pause)
    return False


def sell_at_station(call, say, quoted, station, wanted, notes, target="self"):
    """Dock at the route's station; sell each wanted (item, min_price) from the hold, then from the storage there, into the
    bids at min_price or more; store the rest of the hold. Returns {item: [units, credits]}."""
    def raw(action, params, group="spacemolt"):
        return call("POST", "/accounts/%s/raw" % quoted, {"toolGroup": group, "action": action, "params": params})[1]

    def content(answer):
        found = answer.get("structuredContent") if isinstance(answer, dict) else None
        return found if isinstance(found, dict) else {}

    def hold():
        rows = call("GET", "/accounts/%s/state/cargo" % quoted)[1]
        return {r.get("item_id"): r.get("quantity") or 0 for r in (rows if isinstance(rows, list) else []) if isinstance(r, dict)}

    last = ""
    for attempt in range(DOCK_TRIES):
        if attempt in (0, DOCK_TRIES // 2):
            settled(call, quoted)                        # a goal or a job still in flight refuses the dock goal
        status, answer = call("POST", "/accounts/%s/goal" % quoted, {"type": "prepare-at-station", "options": {
            "systemId": station[0], "poiId": station[1], "baseId": station[2], "refuel": True}}, timeout=900)
        if status == 200 and answer.get("success"):
            break
        last = "%s %s" % (status, " ".join(str(answer.get("error") or answer.get("message") or answer).split())[:90])
        say("dock for the sale, try %d of %d: %s" % (attempt + 1, DOCK_TRIES, last))
        if "in_battle" in last.lower().replace(" ", "_"):     # the engine's flee mode leaves the battle stance as it was (requests ENT-090)
            raw("stance", {"stance": "flee"}, "spacemolt_battle")
            say("in a battle: stance flee")
        time.sleep(30)
    else:
        notes.append("not docked for the sale: " + last)   # the engine's last answer: the cause is in the record
        return {}
    wallet = lambda: credits_of(call("GET", "/accounts/" + quoted)[1]) or 0
    sold = {}
    for item, floor in wanted:
        for _ in range(4):                               # the hold first, then the storage; the book is read before every sale
            stored = {str(i.get("item_id")): int(i.get("quantity") or 0)
                      for i in content(raw("view", {"station_id": station[2]}, "spacemolt_storage")).get("items") or [] if isinstance(i, dict)}
            have = hold().get(item, 0) or stored.get(item, 0)
            rows = content(raw("view_market", {"item_id": item}, "spacemolt_market")).get("items") or []
            bids = (rows[0].get("buy_orders") if rows and isinstance(rows[0], dict) else None) or []
            levels = [(o.get("price_each") or o.get("price") or 0, o.get("quantity") or 0) for o in bids if isinstance(o, dict)]
            units = int(min(have, sum(q for p, q in levels if p >= floor)))
            if units <= 0:
                if have:
                    say("%s: %d units, no bid at %d cr or more here (best %s): kept" % (item, have, floor, max([p for p, _q in levels] or [0])))
                break
            before = wallet()
            raw("sell", {"item_id": item, "quantity": units})
            time.sleep(11)
            got = wallet() - before
            say("sold %d %s: %+d cr" % (units, item, got))
            if got <= 0:
                notes.append("%s: a sale brought nothing" % item)
                break
            sold[item] = [sold.get(item, [0, 0])[0] + units, sold.get(item, [0, 0])[1] + got]
    ammo = ammo_ids()
    stashed = {}
    for item, units in hold().items():                   # the rest goes into storage here: the hold is free for the next work
        if units and item not in ammo:
            if "error" not in raw("deposit", {"item_id": item, "quantity": units, "target": target, "source": "cargo"}, "spacemolt_storage"):
                stashed[item] = units
            time.sleep(11)
    if stashed:
        say("stored at %s: %s" % (station[2], stashed))
    return sold


def ammo_ids():
    """The item ids that are ammunition (data/catalog/ammo.json): they stay aboard."""
    try:
        with open(os.path.join(DATA, "catalog", "ammo.json"), encoding="utf-8") as handle:
            return set(json.load(handle))
    except (OSError, ValueError):
        return set()


def store_last_load(call, say, quoted, station, notes, target="self"):
    """A run without a sale ends with its last load in storage: dock at the route's station and store the hold when more
    than five units of goods are aboard (the dispatcher's line for requires.empty_hold), so that the next route that wants
    an empty hold opens to the ship. Returns the units found aboard."""
    rows = call("GET", "/accounts/%s/state/cargo" % quoted)[1]
    ammo = ammo_ids()
    aboard = sum(int(r.get("quantity") or 0) for r in (rows if isinstance(rows, list) else [])
                 if isinstance(r, dict) and r.get("item_id") not in ammo)
    if aboard > 5:
        say("%d units aboard at the end of the run: stored at %s" % (aboard, station[2]))
        sell_at_station(call, say, quoted, station, [], notes, target)
    return aboard


def option(args, name, default):
    return args[args.index(name) + 1] if name in args else default


def main():
    args = sys.argv[1:]
    pilot, belt, station = args[0], args[1].split(":"), args[2].split(":")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import division                               # the division's lock: own ships only, never a pilot another program flies
    division.require(pilot)
    minutes = float(option(args, "--minutes", "45"))
    route_id = option(args, "--route", "mine-" + belt[1])
    deposit = "faction" if option(args, "--deposit", "personal") == "faction" else "personal"
    target = "faction" if deposit == "faction" else "self"     # the storage call's word for the same choice
    quoted = urllib.parse.quote(pilot, safe="")
    order_file = os.path.join(DATA, "fleet", "orders", pilot + ".json")

    def call(method, path, body=None, timeout=120):
        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(GATE + path, data=data, method=method, headers={"Content-Type": "application/json"} if data else {})
        try:
            with OPENER.open(request, timeout=timeout) as answer:
                return answer.status, json.loads(answer.read().decode("utf-8", "replace") or "{}")
        except urllib.error.HTTPError as error:
            try:
                return error.code, json.loads(error.read().decode("utf-8", "replace") or "{}")
            except ValueError:
                return error.code, {}
        except Exception as error:
            return 0, {"error": "%s: %s" % (type(error).__name__, error)}

    def say(text):
        print(time.strftime("%H:%M:%S", time.gmtime()), pilot, text, flush=True)
        try:
            os.utime(order_file)
        except OSError:
            pass

    def numbers():
        """(credits, ore mined so far); None for a value that could not be read."""
        try:
            live = (re.sub(r"[^A-Za-z0-9_.-]", "_", pilot)[:60] or "pilot") + ".json"      # the collector's file-name rule
            with open(os.path.join(DATA, "fleet", "ships", live), encoding="utf-8") as handle:
                ship = json.load(handle)
        except (OSError, ValueError):
            ship = {}
        return credits_of(call("GET", "/accounts/" + quoted)[1]), ore_of(ship)

    os.makedirs(os.path.dirname(order_file), exist_ok=True)
    with open(order_file, "w", encoding="utf-8") as handle:
        json.dump({"pilot": pilot, "what": "mine " + route_id, "since": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, handle)
    atexit.register(lambda: os.path.exists(order_file) and os.remove(order_file))
    started = time.time()
    credits_before, ore_before = numbers()
    loop = {"type": "mining", "options": {"miningSystemId": belt[0], "beltPoiId": belt[1], "sellSystemId": station[0], "sellStationPoiId": station[1],
                                          "sellBaseId": station[2], "skipMarket": "--sell" not in args, "depositTarget": deposit, "retryOnDepleted": True}}
    status, answer, notes, stopped = 0, {}, [], ""
    try:
        for _ in range(40):                              # a goal of an earlier runner may still be running
            status, answer = call("POST", "/accounts/%s/loop" % quoted, loop)
            if status in (200, 201) and "error" not in answer:
                break
            time.sleep(15)
        say("mining loop at %s, ore to %s: %s %s" % (belt[1], station[2], status, str(answer.get("error") or "started")[:100]))
        notes = [] if status in (200, 201) and "error" not in answer else ["loop not started"]
        while not notes and time.time() - started < minutes * 60 and not os.path.exists(os.path.join(DATA, "fleet", "STOP")):
            time.sleep(30)
            try:
                os.utime(order_file)
            except OSError:
                pass
            loop_state = call("GET", "/accounts/%s/loop" % quoted)[1]
            if not loop_state.get("running"):
                notes.append("the loop ended by itself: " + str(loop_state.get("lastFailure") or "")[:80])
    except SystemExit as leave:                          # told to stop (runhost.py's stop file or its end, a signal): the run still ends whole
        stopped = leave.code if isinstance(leave.code, str) and leave.code else "stopped"
        notes.append(stopped)
        say("told to stop (%s): the loop is ended and the row written; nothing is sold or stored" % stopped)
    call("DELETE", "/accounts/%s/loop" % quoted)
    for _ in range(0 if stopped else 40):                # let the step in flight end; a stopped run leaves at once
        account = call("GET", "/accounts/" + quoted)[1]
        if not account.get("hasExecutingGoal"):
            break
        time.sleep(15)
    sold = {}
    wanted = [(pair.split(":")[0], int(pair.split(":")[1])) for pair in option(args, "--sell-items", "").split(",") if pair.count(":") == 1]
    if stopped:
        pass                                             # whoever stopped the run wants the ship now
    elif wanted and "loop not started" not in notes and not os.path.exists(os.path.join(DATA, "fleet", "STOP")):
        sold = sell_at_station(call, say, quoted, station, wanted, notes, target)
    elif "loop not started" not in notes and not os.path.exists(os.path.join(DATA, "fleet", "STOP")):
        store_last_load(call, say, quoted, station, notes, target)  # a partial load left aboard closes every empty_hold route
    credits_after, ore_after = numbers()
    took = (time.time() - started) / 60
    if credits_before is None or credits_after is None:
        notes.append("wallet not read")
    delta = 0 if "wallet not read" in notes else credits_after - credits_before
    ore = None if ore_before is None or ore_after is None else ore_after - ore_before
    row = {"route": route_id, "kind": "mine", "pilot": pilot, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)), "minutes": round(took, 1),
           "credits_before": credits_before, "credits_after": credits_after, "delta": delta, "one_time": 0,
           "ore": ore, "sold": sold, "notes": notes}
    os.makedirs(os.path.join(DATA, "routes"), exist_ok=True)
    with open(os.path.join(DATA, "routes", "runs.jsonl"), "a", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    print("RESULT %s: mined %s ore at %s in %.0f min | sold (units, credits) %s | credits %s -> %s (%+d) | %s" % (
        pilot, "an unread amount of" if ore is None else ore, belt[1], took, sold or "nothing", credits_before, credits_after, delta,
        "; ".join(notes) or "no notes"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
