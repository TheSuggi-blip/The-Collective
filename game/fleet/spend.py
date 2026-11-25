#!/usr/bin/env python3
"""spend.py -- what the fleet bought once, by division and by kind (modules, hulls, craft inputs, mission goods), from the record of money paid once.

WHAT: reads data/fleet/onetime.json (every reward and buy paid once, [t, pilot, title, credits]) and data/fleet/fleet.json
      (each pilot's division) and prints, for a window of hours, the credits each division spent by kind and the
      rewards it was paid, with the fleet's total. The kind is read from the booking's title, the way its writer
      books it: `fit_net <module>` and `...: <module> bought (tool)` are modules, `<Hull> hull bought from listing` and
      `<Hull> hull commissioned` hulls, `(craft inputs)` and `craft_net listed stock` craft inputs, a route's
      `mission-...: <item> bought` mission goods. Moves between purses of ours are left out and counted apart: gifts
      (`Wallet top-up`), treasury funds and deposits, and the market's buy escrow (locked, released, repriced, filled:
      credits held in a standing buy order, Trade's). The record keeps its newest rows only (gate.py book_onetime), so
      the window is cut to what it holds and the answer says how many hours that is.
RULES:
  - Reads only. A row whose pilot the fleet file does not name counts under `none`.
  - A figure the record cannot hold is never filled in: a window longer than the record says `covers N h`.
WHY:  orders ENT-092 (block UNITY) and requests of Oracle, Zero and Apophis: fit-network bought modules for 3.4 million cr
      in six hours and three Admirals summed onetime.json by hand to find whose and what; the briefing showed escrow
      locks as purchases and their release as rewards.

USAGE:
  spend.py [--hours H] [--data <dir>]     the table for the last H hours (default 6)
  spend.py brief [--data <dir>]           the briefing's lines: 1 h and 6 h, the fleet and each division's largest kind

Stdlib only. ASCII only.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

DATA = "/srv/collective/data"
KINDS = ("modules", "hulls", "craft inputs", "mission goods", "other buys")
DEPOSIT = "Faction treasury: credits deposited"     # wallet.py DEPOSIT_TITLE begins so: a move into the treasury
MOVES = ("Wallet top-up", "Treasury fund: credits withdrawn", DEPOSIT)
ESCROW = "Exchange buy escrow"
TAX = "Weekly tax"


def read(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return default


def kind_of(title, credits):
    """The kind of one booking: a kind of KINDS for a buy, `reward`, `move`, `escrow` or `tax`."""
    title = str(title or "")
    if title == TAX:
        return "tax"
    if any(title.startswith(m) for m in MOVES):
        return "move"
    if title.startswith(ESCROW):
        return "escrow"
    if credits >= 0:
        return "reward"
    if title.startswith("fit_net ") or title.endswith("bought (tool)"):
        return "modules"
    if re.search(r" hull (bought from listing|commissioned)$", title):
        return "hulls"
    if title.endswith("(craft inputs)") or title.startswith("craft_net "):
        return "craft inputs"
    if title.startswith("mission-") and " bought" in title:
        return "mission goods"
    return "other buys"


def divisions(data):
    """{pilot: division} from the fleet file."""
    fleet = read(Path(data) / "fleet" / "fleet.json", {})
    ships = fleet.get("ships") if isinstance(fleet, dict) else None
    return {s.get("name"): (s.get("division") or "none") for s in ships or [] if isinstance(s, dict) and s.get("name")}


def gather(data, hours, now=None):
    """{"since", "covers", "rows", "div": {division: {kind: credits spent (positive)}}, "rewards": {division: cr},
    "moves": cr moved, "escrow": net cr held in buy orders}."""
    now = time.time() if now is None else now
    rows = [r for r in read(Path(data) / "fleet" / "onetime.json", []) if isinstance(r, list) and len(r) == 4
            and isinstance(r[0], (int, float)) and isinstance(r[3], (int, float))]
    oldest = min((r[0] for r in rows), default=now)
    since = max(now - hours * 3600, oldest)
    owner = divisions(data)
    out = {"since": since, "covers": (now - since) / 3600, "asked": hours, "rows": 0, "div": {}, "rewards": {}, "moves": 0, "escrow": 0, "tax": 0,
           "deposits": 0, "deposit_n": 0}
    for t, pilot, title, credits in rows:
        if t < since:                                  # a row stamped after `now` (a clock ahead) still counts, as the briefing always did
            continue
        out["rows"] += 1
        kind, division = kind_of(title, credits), owner.get(pilot, "none")
        if kind == "move":
            out["moves"] += abs(credits)
            if str(title).startswith(DEPOSIT):
                out["deposits"] -= credits
                out["deposit_n"] += 1
        elif kind == "escrow":
            out["escrow"] -= credits
        elif kind == "tax":
            out["tax"] -= credits
        elif kind == "reward":
            out["rewards"][division] = out["rewards"].get(division, 0) + credits
        else:
            spent = out["div"].setdefault(division, {})
            spent[kind] = spent.get(kind, 0) + (-credits)
    return out


def num(value):
    return format(int(round(value)), ",")


def table(found):
    lines = ["SPEND | what the fleet bought once, by division and kind, and the rewards paid once | the last %.1f h%s | %d bookings | "
             "data/fleet/onetime.json" % (found["covers"], " (asked %g h; the record holds no older row)" % found["asked"]
                                         if found["covers"] + 0.05 < found["asked"] else "", found["rows"])]
    head = "  %-10s" % "division" + "".join("%14s" % k for k in KINDS) + "%14s%14s" % ("bought", "rewards")
    lines.append(head)
    names = sorted(set(found["div"]) | set(found["rewards"]))
    total = {k: 0 for k in KINDS}
    for name in names:
        spent = found["div"].get(name, {})
        for k in KINDS:
            total[k] += spent.get(k, 0)
        lines.append("  %-10s" % name + "".join("%14s" % num(spent.get(k, 0)) for k in KINDS)
                     + "%14s%14s" % (num(sum(spent.values())), num(found["rewards"].get(name, 0))))
    lines.append("  %-10s" % "fleet" + "".join("%14s" % num(total[k]) for k in KINDS)
                 + "%14s%14s" % (num(sum(total.values())), num(sum(found["rewards"].values()))))
    lines.append("  left out: moves between purses of ours %s cr (gifts, treasury funds and deposits); market buy escrow, net held in "
                 "standing buy orders %s cr%s" % (num(found["moves"]), num(found["escrow"]), "; weekly tax %s cr" % num(found["tax"]) if found["tax"] else ""))
    return lines


def brief(data, now=None):
    """The briefing's lines: for 1 h and 6 h the fleet's buys by kind and the division that spent most on each kind."""
    out = []
    for hours in (1, 6):
        found = gather(data, hours, now)
        total = {k: sum(d.get(k, 0) for d in found["div"].values()) for k in KINDS}
        parts = []
        for k in KINDS:
            if total[k] <= 0:
                continue
            top = max(found["div"].items(), key=lambda kv: kv[1].get(k, 0))
            parts.append("%s %s (most %s %s)" % (k, num(total[k]), top[0], num(top[1].get(k, 0))))
        out.append("    bought once, last %.1f h%s: %s | rewards %s | escrow held in buy orders %s (Trade's, left out)%s"
                   % (found["covers"], "" if found["covers"] + 0.05 >= hours else " (the record holds no older row)",
                      "; ".join(parts) or "nothing", num(sum(found["rewards"].values())), num(found["escrow"]),
                      " | into the faction's treasury %s in %d deposits (a move between two purses of ours)" % (num(found["deposits"]), found["deposit_n"])
                      if found["deposit_n"] else ""))
    out.append("    by division and kind: hive.py spend [--hours H]")
    return out


def main(argv):
    args = list(argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    data = value("--data", DATA)
    if "-h" in args or "--help" in args:
        print(__doc__)
        return 0
    if args and args[0] == "brief":
        print("\n".join(brief(data)))
        return 0
    print("\n".join(table(gather(data, float(value("--hours", "6"))))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
