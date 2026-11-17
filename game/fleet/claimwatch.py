#!/usr/bin/env python3
"""claimwatch.py -- find a pilot the engine holds claimed and free it by an engine restart, without a hand.

WHAT: after a stall the engine can keep a claim on one account: every goal of that pilot answers 409 "Another request
      for this account is already being processed" and every loop start "This account is claimed by a fleet operation
      in progress", while its reads work. Nothing but an engine restart ends it (seen 2026-11-16 and 2026-11-17). A
      pass reads the tail of every pilot's run log, keeps who showed one of the two answers in the last ten minutes
      (data/fleet/claimwatch.json), and calls a pilot claimed when three passes, ten minutes or more from the first to
      the last, each found a newer such answer and the newest is no older than six minutes. With --act and the switch file it then restarts the engine through
      the gate (POST /__gate/engine/restart) and writes what it did to data/fleet/claims.jsonl.
RULES:
  - It restarts only with the switch file data/fleet/claimwatch-on; never while fleet/STOP exists, while a tenth of
    the fleet is not connected (a wave: the game restarts), or while a ship of ours stands under 70 percent hull (it
    may be in a fight); and only when the gate says a restart is free (restart_in_s 0).
  - One restart in two hours. A claim that shows again within two hours of the watch's own restart is not restarted
    away: the pass says so once an hour, for a hand.
  - The Fleet Admiral's and the services' only: a restart signs every pilot off and on again (about four minutes) and
    cuts every run in flight.
  - One answer alone is no claim: a goal that met another request once goes through at its next try.
  - A pass prints a line only when it restarts, when the gate refuses, or when a claim came back: the job that runs
    it delivers what it prints.
WHY:  on 2026-11-17 a guard post beyond the border stood empty for half an hour until its Admiral asked and a hand
      restarted the engine (requests ENT-202). Nobody waits on a service (Suggi).

USAGE:
  claimwatch.py [check]     what the logs show now and what a pass would do; nothing is changed
  claimwatch.py --act       one pass: keep the sightings; restart the engine when a pilot is claimed and every rule holds
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only."""
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  who asks

DATA = os.environ.get("FLEET_DATA_ROOT", "/srv/collective/data")
SIGNS = ("Another request for this account is already being processed", "This account is claimed by a fleet operation in progress")
FRESH = 10 * 60                # an answer older than this is no sighting
GAP = 40 * 60                  # two sightings further apart than this are not one claim: the dispatcher holds a pilot back 30 minutes after
                               # three failed starts, and a mine run tries ten minutes, then logs one line
PASSES = 3                     # passes that each found a newer answer
SPAN = 10 * 60                 # ... from the first to the last, in seconds
YOUNG = 6 * 60                 # ... and the newest answer no older than this: a claim that ended is not restarted away
QUIET = 2 * 60 * 60            # one restart of the watch in this many seconds
HULL = 0.7                     # no restart while a ship stands under this share of its hull
TAIL = 8000                    # bytes read from the end of a log
CLOCK = re.compile(r"^(\d\d):(\d\d):(\d\d) ")


def read(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return default


def sightings(data, now):
    """{pilot: (when its newest claim answer was logged, the line)} from the run logs: only an answer logged within the
    last FRESH seconds counts (a run's lines start with the UTC time of day)."""
    found, folder = {}, Path(data) / "routes" / "logs"
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        return found
    of_day = now % 86400
    for name in names:
        path = folder / name
        try:
            if not name.endswith(".log") or now - path.stat().st_mtime > FRESH:
                continue
            with open(path, "rb") as handle:
                handle.seek(max(0, path.stat().st_size - TAIL))
                lines = handle.read().decode("utf-8", "replace").splitlines()
        except OSError:
            continue
        for line in reversed(lines):
            clock = CLOCK.match(line)
            if clock and any(sign in line for sign in SIGNS):
                age = (of_day - (int(clock.group(1)) * 3600 + int(clock.group(2)) * 60 + int(clock.group(3)))) % 86400
                if age <= FRESH:
                    found[name[:-4]] = (now - age, " ".join(line.split())[:200])
                break
    return found


def step(state, hits, now):
    """(the state with this pass's sightings, the pilots claimed now). A sighting counts as a new pass only when its
    answer is newer than the one counted before; a pilot without a sighting keeps its count for GAP seconds (its next
    run starts the log anew), then starts again."""
    before = state.get("seen") if isinstance(state.get("seen"), dict) else {}
    seen = {pilot: was for pilot, was in before.items() if pilot not in hits and isinstance(was, dict) and now - was.get("last", 0) <= GAP}
    for pilot, (at, _line) in hits.items():
        was = before.get(pilot)
        if isinstance(was, dict) and now - was.get("last", 0) <= GAP:
            newer = at > was.get("at", 0) + 1
            seen[pilot] = {"first": was.get("first", now), "last": now if newer else was.get("last", now), "at": max(at, was.get("at", 0)),
                           "passes": int(was.get("passes", 0)) + (1 if newer else 0)}
        else:
            seen[pilot] = {"first": now, "last": now, "at": at, "passes": 1}
    claimed = sorted(pilot for pilot, s in seen.items() if s["passes"] >= PASSES and s["last"] - s["first"] >= SPAN and now - s["at"] <= YOUNG)
    return dict(state, seen=seen), claimed


def hold_back(data, health):
    """Why the engine is not restarted now, or ''."""
    if (Path(data) / "fleet" / "STOP").exists():
        return "fleet/STOP exists"
    fleet = read(Path(data) / "fleet" / "fleet.json", {})
    ships = [s for s in (fleet.get("ships") if isinstance(fleet, dict) else None) or [] if isinstance(s, dict)]
    if not ships:
        return "the fleet file holds no ship"
    away = sum(1 for s in ships if s.get("status") != "connected")
    if away * 10 >= len(ships):
        return "%d of %d ships are not connected: a wave" % (away, len(ships))
    low = sum(1 for s in ships if isinstance(s.get("max_hull"), (int, float)) and s["max_hull"] > 0 and (s.get("hull") or 0) < HULL * s["max_hull"])
    if low:
        return "%d ship(s) under %d percent hull" % (low, round(HULL * 100))
    if not isinstance(health, dict) or health.get("engine") != "running":
        return "the gate does not say that the engine runs"
    if health.get("restart_in_s"):
        return "the gate frees a restart in %s s" % health.get("restart_in_s")
    return ""


def answer_of(text):
    try:
        value = json.loads(text) if isinstance(text, str) else text
    except ValueError:
        return {}
    return value if isinstance(value, dict) else {}


def roles_of(pilots):
    """The pilots as counts per role word, for a line others read: no pilot is named."""
    counts = {}
    for pilot in pilots:
        word = pilot.rsplit("-", 1)[0] if re.search(r"-\d+$", pilot) else "flagship"
        counts[word] = counts.get(word, 0) + 1
    return ", ".join("%d %s" % (n, word) for word, n in sorted(counts.items())) or "none"


def main(argv=None, call=None, now=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    data = args[args.index("--data") + 1] if "--data" in args and args.index("--data") + 1 < len(args) else DATA
    act, now = "--act" in args, time.time() if now is None else now
    kind, who = division.member()
    if act and not (kind == "service" or who == "Unity"):
        sys.exit("REFUSED: the engine restart is the Fleet Admiral's: the watch runs in her five-minute job")
    if call is None:
        import gate
        call = gate.call
    folder = Path(data) / "fleet"
    state = read(folder / "claimwatch.json", {})
    state = state if isinstance(state, dict) else {}
    hits = sightings(data, now)
    new, claimed = step(state, hits, now)
    switch = (folder / "claimwatch-on").exists()
    since = now - float(state.get("restarted") or 0)
    if not act:
        print("CLAIMWATCH | %d pilot(s) logged a claim answer in the last %d minutes (%s) | claimed by the rule: %d | switch %s | the watch's last restart: %s"
              % (len(hits), FRESH // 60, roles_of(hits), len(claimed), "on" if switch else "off",
                 "%d min ago" % (since // 60) if state.get("restarted") else "none"))
        for pilot in sorted(new["seen"]):
            s = new["seen"][pilot]
            print("  %s: %d pass(es) with a newer answer, first %d min ago | %s" % (roles_of([pilot]), s["passes"], (now - s["first"]) // 60,
                                                                                   hits[pilot][1][9:160] if pilot in hits else "no answer in its log now"))
        if claimed:
            print("  a pass with --act would: %s" % ("say that the claim came back (a restart %d min ago)" % (since // 60) if since < QUIET
                                                      else "restart the engine, unless: " + (hold_back(data, answer_of(call("get", "/__gate/healthz")[1])) or "nothing holds it back")
                                                      if switch else "do nothing: the switch file is not there"))
        return 0
    line = ""
    if claimed:
        minutes = int(max(now - new["seen"][pilot]["first"] for pilot in claimed) // 60)
        if since < QUIET:
            if now - float(state.get("told") or 0) >= 3600:
                line = ("claimwatch: %s still answer as claimed, %d minutes after the watch restarted the engine: a hand is needed (the Fleet Admiral)"
                        % (roles_of(claimed), since // 60))
                new["told"] = now
        elif switch:
            why = hold_back(data, answer_of(call("get", "/__gate/healthz")[1]))
            if not why:
                status, text = call("post", "/__gate/engine/restart",
                                    {"reason": "claimwatch: %d account(s) answer 409 to every goal for %d minutes; reads work" % (len(claimed), minutes)})
                if status == 202:
                    new.update(restarted=now, seen={})
                    with open(folder / "claims.jsonl", "a", encoding="utf-8") as handle:
                        handle.write(json.dumps({"at": int(now), "pilots": claimed, "minutes": minutes, "did": "engine restart", "answer": status}) + "\n")
                    line = ("claimwatch: the engine was restarted at %s UTC to free %s held claimed for %d minutes; every pilot signs in again within about four minutes"
                            % (time.strftime("%H:%M", time.gmtime(now)), roles_of(claimed), minutes))
                elif now - float(state.get("told") or 0) >= 3600:
                    line = "claimwatch: %s claimed for %d minutes and the gate refused the restart (%s %s)" % (roles_of(claimed), minutes, status, str(text)[:120])
                    new["told"] = now
    tmp = "%s.%d.tmp" % (folder / "claimwatch.json", os.getpid())
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(new, handle)
    os.replace(tmp, folder / "claimwatch.json")
    if line:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
