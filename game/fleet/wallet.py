#!/usr/bin/env python3
"""wallet.py -- no ship of ours goes broke: a ship whose wallet runs low is given credits by a rich ship of its division.

WHAT: every pilot pays its own fuel, repairs, fittings and tax from its own wallet. This script reads every wallet
      (data/fleet/fleet.json) and, for each pilot under LOW, has the richest ship of the same division give it
      credits up to TARGET (a credit gift: the game's storage `deposit` of item `credits` to the pilot's name; it
      works from anywhere, also while both ships fly). A division without a donor is helped by the command group.
      Every gift is booked twice in data/fleet/onetime.json (`Wallet top-up`, minus for the giver, plus for the
      receiver), so it moves no division's steady money, and kept in data/fleet/gifts.jsonl.
      The dispatcher does its part (dispatch.py, FLOOR): a pilot under 5,000 cr is sent only on work that pays.
RULES:
  - A donor keeps KEEP credits at least; one gift per pilot per COOLDOWN (the wallets are read every ten seconds,
    the game's answer can lag): a pilot is never given twice for one low reading.
  - Every gift is booked the moment the game took it, with its own time: a fault later in the pass never loses the
    record, and a run's figure leaves the gift out by that time (routes.moved). A gate that does not answer is no
    fault of the pass: the wallet is read again after WAIT seconds; a gift that shows is booked, one that does not
    is kept in gifts.jsonl with 0 credits (`unsure`), so its pilot is on cooldown and never given twice.
  - Gifts are not income for the game's tax. They go between our own pilots only, never to another player.
  - `check` prints one HALT line for every pilot under the floor of rule F7 (3,000 cr) and exits 1 then.
  - A real `topup` is the Fleet Admiral's or the five-minute job's; `--dry-run` is free.
WHY:  Suggi, 2026-11-16: "No ships can go broke, this is important." Standing work costs fuel and earns nothing, and
      the weekly tax takes a share of every wallet in one moment.

USAGE:
  wallet.py [check]            every wallet against the floors; HALT for a pilot under 3,000 cr
  wallet.py topup [--dry-run]  give each pilot under LOW credits up to TARGET from a rich ship of its division
  --data <dir>                 the unit's data folder (default: the fleet's)

Stdlib only. ASCII only.
"""

import fcntl
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dispatch                                   # noqa: E402  flagships, roles
import division                                   # noqa: E402  who asks, which roles are whose

FLOOR = 3000                   # rule F7: every pilot keeps this
LOW = 10000                    # a wallet under this is topped up
TARGET = 20000                 # ... to this
KEEP = 30000                   # a donor never goes under this
COOLDOWN = 30 * 60             # one gift per pilot in this many seconds
WAIT = 15                      # seconds until the fleet file shows a gift the gate did not answer for
BUDGET = 150                   # seconds a pass may give for: what is left waits for the next pass (the job runs every five minutes)
TITLE = "Wallet top-up"


def wallets(data):
    """[(pilot, credits, division)] of every ship whose wallet was read."""
    named = dispatch.flagships(data)
    fleet = dispatch.read_json(Path(data) / "fleet" / "fleet.json", {})
    out = []
    for ship in fleet.get("ships") or [] if isinstance(fleet, dict) else []:
        name, credits = ship.get("name"), ship.get("credits")
        if name and isinstance(credits, (int, float)) and not isinstance(credits, bool):
            owner = division.ROLES.get(dispatch.role_of(name, named), "")
            out.append((name, int(credits), owner))
    return out


def recent(data, now):
    """{pilot: the time of its last gift received} within COOLDOWN."""
    out = {}
    try:
        with open(Path(data) / "fleet" / "gifts.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict) and now - (row.get("at") or 0) < COOLDOWN:
                    out[row.get("to")] = row.get("at")
    except OSError:
        pass
    return out


def plan_gifts(rows, given):
    """[(donor, pilot, credits)]: for each pilot under LOW, lowest first, the richest ship of its division that keeps
    KEEP after the gift; else the richest of the command group."""
    purse = {name: credits for name, credits, _owner in rows}
    out = []
    for name, credits, owner in sorted(rows, key=lambda r: r[1]):
        if credits >= LOW or name in given:
            continue
        need = TARGET - credits
        for group in (owner, "Unity"):
            donors = sorted(((purse[n], n) for n, _c, o in rows if o == group and n != name and purse[n] - need >= KEEP), reverse=True)
            if donors:
                donor = donors[0][1]
                purse[donor] -= need
                purse[name] += need
                out.append((donor, name, need))
                break
    return out


def give(donor, pilot, credits):
    """(True, text) when the game took the gift."""
    import gate
    status, answer = gate.call("post", "/accounts/%s/raw" % gate.q(donor),
                               {"toolGroup": "spacemolt_storage", "action": "deposit", "params": {"item_id": "credits", "quantity": int(credits), "target": pilot}}, timeout=90)
    ok = status == 200 and '"error"' not in answer[:200]
    return ok, answer[:200]


def landed(data, pilot, was, credits):
    """True when the pilot's wallet shows the gift after all: the gate did not answer in time, the game may have taken it."""
    time.sleep(WAIT)
    have = {name: credits_now for name, credits_now, _owner in wallets(data)}
    return have.get(pilot, was) >= was + credits * 0.9


def unsure(data, donor, pilot, credits, now):
    """A gift the gate did not answer for and the wallet does not show: kept with 0 credits, so the pilot is on cooldown
    (recent) and no figure counts it (routes.moved)."""
    with open(Path(data) / "fleet" / "gifts.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps({"at": int(now), "from": donor, "to": pilot, "credits": 0, "unsure": credits}) + "\n")


def book(data, gifts, now):
    """The gifts into gifts.jsonl and, twice each, into onetime.json (kept out of the steady money)."""
    folder = Path(data) / "fleet"
    with open(folder / "gifts.jsonl", "a", encoding="utf-8") as handle:
        for donor, pilot, credits in gifts:
            handle.write(json.dumps({"at": int(now), "from": donor, "to": pilot, "credits": credits}) + "\n")
    once = folder / "onetime.json"
    with open(str(once) + ".lock", "w") as lock:                    # the lock the runners and gate.py book under
        fcntl.flock(lock, fcntl.LOCK_EX)
        rows = dispatch.read_json(once, [])
        rows = rows if isinstance(rows, list) else []
        for donor, pilot, credits in gifts:
            rows += [[int(now), donor, TITLE, -credits], [int(now), pilot, TITLE, credits]]
        tmp = "%s.%d.tmp" % (once, os.getpid())
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(rows[-8000:], handle, separators=(",", ":"))
        os.replace(tmp, once)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    data = args[args.index("--data") + 1] if "--data" in args else division.DATA
    verb = "topup" if "topup" in args else "check"
    now = time.time()
    rows = wallets(data)
    if not rows:
        print("wallet: no wallet read in %s" % data)
        return 1
    low = sorted(r for r in rows if r[1] < LOW)
    if verb == "check":
        poorest = min(rows, key=lambda r: r[1])
        print("WALLETS | %d pilots | poorest %s %s cr | under %s cr: %d | under the floor %s cr: %d"
              % (len(rows), poorest[0], format(poorest[1], ","), format(LOW, ","), len(low), format(FLOOR, ","), sum(1 for r in rows if r[1] < FLOOR)))
        bad = [r for r in rows if r[1] < FLOOR]
        for name, credits, owner in bad:
            print("HALT: %s holds %s cr, under the floor of %s (division of %s): `wallet.py topup` gives it credits" % (name, format(credits, ","), format(FLOOR, ","), owner))
        return 1 if bad else 0
    kind, who = division.member()
    if "--dry-run" not in args and not (who == "Unity" or kind == "service"):
        sys.exit("REFUSED: a real top-up is the Fleet Admiral's or the five-minute job's; use --dry-run")
    gifts = plan_gifts(rows, recent(data, now))
    done, failed = [], []
    for donor, pilot, credits in gifts:
        if "--dry-run" in args:
            print("would give: %s -> %s %s cr" % (donor, pilot, format(credits, ",")))
            continue
        if time.time() - now > BUDGET:                          # a gate that answers slowly: the rest waits for the next pass
            break
        try:
            ok, text = give(donor, pilot, credits)
        except Exception as error:                              # the gate did not answer (a timeout): the game may still have taken the gift
            was = next((have for name, have, _owner in rows if name == pilot), 0)
            ok, text = landed(data, pilot, was, credits), "the gate did not answer (%s: %s) and the wallet does not show the gift" % (type(error).__name__, error)
            if not ok:
                unsure(data, donor, pilot, credits, time.time())
        if ok:
            book(data, [(donor, pilot, credits)], time.time())  # at once and with its own time: a fault later in the pass never loses the record
            done.append((donor, pilot, credits))
        else:
            failed.append((donor, pilot, text))
    for donor, pilot, credits in done:
        print("given: %s -> %s %s cr" % (donor, pilot, format(credits, ",")))
    for donor, pilot, text in failed:
        print("HALT: the gift %s -> %s failed: %s" % (donor, pilot, text))
    stranded = [name for name, credits, _o in low if name not in {p for _d, p, _c in gifts}]
    for name in stranded:
        if name not in recent(data, now):
            print("HALT: %s is under %s cr and no ship of its division or of the command group can give without going under %s" % (name, format(LOW, ","), format(KEEP, ",")))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
