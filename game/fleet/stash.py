#!/usr/bin/env python3
"""stash.py -- store what a docked pilot carries in its own storage at that station, so that its hold is free for the next route.

WHAT: for each pilot named: reads its hold from the engine and deposits every good that is not ammunition into the pilot's own
      storage at the station it is docked at, one deposit per tick, then gives the pilot back to the dispatcher.
RULES:
  - Own ships only, and never a pilot a runner is flying (the division's lock); a pilot that is not docked is skipped.
  - Ammunition stays aboard (data/catalog/ammo.json). Nothing is sold: what is stored is Logistics' to sell (ledger.py).
WHY:  a route with `requires.empty_hold` (the mine routes, the census, hunts beyond the border) is closed to a ship that carries
      more than five units left over from a mission or a test. On 2026-11-16 four guard ships with a new harvester waited on that.

USAGE:
  stash.py <pilot> [<pilot> ...] [--dry-run]

Stdlib only. ASCII only."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  own ships only
import gate                                       # noqa: E402  the engine's gate and the hand hold

TICK = 11                      # seconds: one command per tick


def leftovers(cargo, ammo):
    """[(item id, units)] of a hold's goods that are not ammunition, largest first."""
    found = {}
    for row in cargo if isinstance(cargo, list) else []:
        item = (row.get("item_id") or row.get("item")) if isinstance(row, dict) else None
        units = row.get("quantity") if isinstance(row, dict) else None
        if item and item not in ammo and isinstance(units, int) and units > 0:
            found[item] = found.get(item, 0) + units
    return sorted(found.items(), key=lambda kv: (-kv[1], kv[0]))


def read(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return default


def stash(pilot, dry, data=division.DATA):
    ok, why = division.may(pilot, data)
    if not ok:
        return "%s: skipped: %s" % (pilot, why)
    fleet = read(os.path.join(data, "fleet", "fleet.json"), {})
    row = next((s for s in fleet.get("ships") or [] if s.get("name") == pilot), None)
    if not row or not row.get("docked"):
        return "%s: skipped: not docked" % pilot
    status, text = gate.call("get", "/accounts/%s/state/cargo" % gate.q(pilot))
    try:
        cargo = json.loads(text) if status == 200 else None
    except ValueError:
        cargo = None
    if cargo is None:
        return "%s: skipped: the hold was not read (http %s)" % (pilot, status)
    goods = leftovers(cargo, set(read(os.path.join(data, "catalog", "ammo.json"), []) or []))
    if not goods or dry:
        return "%s at %s: %s" % (pilot, row["docked"], ("would store " + ", ".join("%d %s" % (n, i) for i, n in goods)) if goods else "nothing to store")
    stored, failed = [], []
    gate.take(pilot, "spacemolt_storage", "deposit")
    try:
        for item, units in goods:
            status, text = gate.call("post", "/accounts/%s/raw" % gate.q(pilot), {"toolGroup": "spacemolt_storage", "action": "deposit",
                                                                              "params": {"item_id": item, "quantity": units, "target": "self", "source": "cargo"}})
            (stored if status == 200 and '"error"' not in text and "isError\":true" not in text else failed).append("%d %s" % (units, item))
            time.sleep(TICK)
    finally:
        gate.release(pilot)
    return "%s at %s: stored %s%s" % (pilot, row["docked"], ", ".join(stored) or "nothing", " | refused: " + ", ".join(failed) if failed else "")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or "-h" in sys.argv or "--help" in sys.argv:
        sys.exit(__doc__)
    for pilot in args:
        print(stash(pilot, "--dry-run" in sys.argv), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
