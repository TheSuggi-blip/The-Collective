#!/usr/bin/env python3
"""mine.py -- one pilot mines at one field for a set time, through the engine's mining loop.

WHAT: starts the engine's mining loop (mine until the hold is full, fly to the
      station, put the ore into the pilot's storage there, fly back), lets it
      run for --minutes, stops it, and waits until the pilot is docked or still.
      Mining trains the Mining skill and flying trains Piloting; the ore stays
      in storage for crafting or a later sale (--sell sells it into the bids).
RULES:
  - Stops at once when data/fleet/STOP appears.
  - The loop is the engine's: this script only starts and stops it and keeps the
    pilot's order file fresh, so the dispatcher gives the pilot nothing else.
WHY:  a ship without paying work still earns skill, and its ore feeds the workshop.

USAGE:
  mine.py <pilot> <system:poi> <system:poi:base> [--minutes M] [--sell] [--route ID]

Writes one row to data/routes/runs.jsonl (minutes, credits before and after, ore mined).
Stdlib only. ASCII only.
"""

import atexit
import fcntl
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GATE = os.environ.get("FLEET_GATE", "http://172.30.0.32:7580")
DATA = os.environ.get("FLEET_DATA_ROOT", "/srv/collective/data")
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def option(args, name, default):
    return args[args.index(name) + 1] if name in args else default


def main():
    args = sys.argv[1:]
    pilot, belt, station = args[0], args[1].split(":"), args[2].split(":")
    minutes = float(option(args, "--minutes", "45"))
    route_id = option(args, "--route", "mine-" + belt[1])
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

    def state():
        return call("GET", "/accounts/" + quoted)[1].get("state") or {}

    def numbers():
        player = state().get("player") or {}
        return int(player.get("credits") or 0), int((player.get("stats") or {}).get("ore_mined") or 0)

    os.makedirs(os.path.dirname(order_file), exist_ok=True)
    with open(order_file, "w", encoding="utf-8") as handle:
        json.dump({"pilot": pilot, "what": "mine " + route_id, "since": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, handle)
    atexit.register(lambda: os.path.exists(order_file) and os.remove(order_file))
    started = time.time()
    credits_before, ore_before = numbers()
    loop = {"type": "mining", "options": {"miningSystemId": belt[0], "beltPoiId": belt[1], "sellSystemId": station[0], "sellStationPoiId": station[1],
                                          "sellBaseId": station[2], "skipMarket": "--sell" not in args, "depositTarget": "personal", "retryOnDepleted": True}}
    status, answer = 0, {}
    for _ in range(40):                                  # a goal of an earlier runner may still be running
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
    call("DELETE", "/accounts/%s/loop" % quoted)
    for _ in range(40):                                  # let the step in flight end
        account = call("GET", "/accounts/" + quoted)[1]
        if not account.get("hasExecutingGoal"):
            break
        time.sleep(15)
    credits_after, ore_after = numbers()
    took = (time.time() - started) / 60
    row = {"route": route_id, "kind": "mine", "pilot": pilot, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)), "minutes": round(took, 1),
           "credits_before": credits_before, "credits_after": credits_after, "delta": credits_after - credits_before, "one_time": 0,
           "ore": ore_after - ore_before, "notes": notes}
    os.makedirs(os.path.join(DATA, "routes"), exist_ok=True)
    with open(os.path.join(DATA, "routes", "runs.jsonl"), "a", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    print("RESULT %s: mined %d ore at %s in %.0f min | credits %d -> %d (%+d) | %s" % (
        pilot, ore_after - ore_before, belt[1], took, credits_before, credits_after, credits_after - credits_before, "; ".join(notes) or "no notes"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
