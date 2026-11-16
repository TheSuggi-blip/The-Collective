#!/usr/bin/env python3
"""plate.py -- make our pilots' stored creature carapace into armor plate where each is docked, and sell plates into the bid there.

WHAT: for each pilot named: reads its storage at the station it is docked at; crafts carapace_plating (6 creature carapace ->
      1 armor plate, 0 cr, the station workshop) for every full 6, delivered to storage; waits until the plates stand there;
      reads the armor-plate bid of that station and sells min(plates, depth at the best bid) when that bid is at least
      --min-bid (default 200 cr). The bid is read again for every pilot, so pilots in a row never sell past it. The wallet
      is read before and after; the plates left stay in storage for the next bid. One RESULT line per pilot.
RULES:
  - Own ships only, never a pilot a runner flies (division.may); a pilot that is not docked is skipped.
  - Never sells under the best bid's price or past its depth (orders F12: nothing sold under a standing bid).
  - One command per tick; each pilot is given back to the dispatcher in a finally. Pilots one after the other.
WHY:  carapace is bid 1 cr, an armor plate 220 to 490 cr in pools of 1 to 6 that come back within the hour (guidebooks
      logistics.md and military.md, 2026-11-16); orders ENT-013 ask every division to make its own where it lies.
      First written by Apollo in his skill logistics-stock (one pilot, one station); brought here for every division.

USAGE:
  plate.py <pilot> [<pilot> ...] [--min-bid N] [--no-craft] [--no-sell] [--dry-run]

Run from the repository clone with python3 -I -B. Stdlib only. ASCII only."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  own ships only
import gate                                       # noqa: E402  the engine's gate and the hand hold

TICK = 11                      # seconds: one command per tick
RECIPE = "carapace_plating"
INPUT, OUTPUT, PER = "creature_carapace", "armor_plate", 6


def crafts(stored):
    """How many plates a storage's carapace makes: one for every full six."""
    return int((stored or {}).get(INPUT, 0) or 0) // PER


def to_sell(plates, price, depth, min_bid):
    """Plates to sell into a bid: never past its depth, nothing under the floor."""
    if price < min_bid or plates <= 0 or depth <= 0:
        return 0
    return min(plates, depth)


def structured(answer):
    if not isinstance(answer, dict):
        return {}
    for key in ("structuredContent", "result"):
        val = answer.get(key)
        if isinstance(val, dict):
            inner = val.get("structuredContent")
            return inner if isinstance(inner, dict) else val
    return answer


def best_bid(answer):
    """(price, depth) of the highest armor-plate buy order in a view_market answer; (0, 0) without one."""
    for item in structured(answer).get("items") or []:
        if isinstance(item, dict) and item.get("item_id") == OUTPUT:
            orders = [o for o in item.get("buy_orders") or [] if isinstance(o, dict)]
            if orders:
                top = max(orders, key=lambda o: int(o.get("price_each") or 0))
                return int(top.get("price_each") or 0), int(top.get("quantity") or 0)
    return 0, 0


def raw(pilot, group, action, params):
    status, text = gate.call("post", "/accounts/%s/raw" % gate.q(pilot), {"toolGroup": group, "action": action, "params": params})
    try:
        return status, json.loads(text)
    except ValueError:
        return status, {"text": text}


def stored(pilot, base):
    _, ans = raw(pilot, "spacemolt_storage", "view", {"station_id": base})
    items = structured(ans).get("items") or []
    return {i["item_id"]: int(i.get("quantity") or 0) for i in items if isinstance(i, dict) and i.get("item_id")}


def ship(pilot):
    try:
        with open(os.path.join(division.DATA, "fleet", "ships", pilot + ".json"), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def wallet(pilot):
    status, text = gate.call("get", "/accounts/%s" % gate.q(pilot))
    try:
        d = json.loads(text) if status == 200 else {}
    except ValueError:
        d = {}
    for key in ("credits", "wallet"):
        if isinstance(d.get(key), (int, float)):
            return int(d[key])
    st = d.get("state") or d.get("player") or {}
    if isinstance(st, dict) and isinstance(st.get("credits"), (int, float)):
        return int(st["credits"])
    return ship(pilot).get("credits")


def plate(pilot, min_bid, craft, sell, dry):
    ok, why = division.may(pilot)
    if not ok:
        return "%s: skipped: %s" % (pilot, why)
    base = ship(pilot).get("docked") or ""
    if not base:
        return "%s: skipped: not docked" % pilot
    have = stored(pilot, base)
    runs, plates0 = crafts(have), have.get(OUTPUT, 0)
    if dry:
        _, ans = raw(pilot, "spacemolt_market", "view_market", {"item_id": OUTPUT})
        price, depth = best_bid(ans)
        return "%s at %s: %d carapace, %d plates; would make %d, would sell %d at %d cr (bid %d x %d)" % (
            pilot, base, have.get(INPUT, 0), plates0, runs if craft else 0,
            to_sell(plates0 + (runs if craft else 0), price, depth, min_bid) if sell else 0, price, price, depth)
    if not ((craft and runs) or (sell and plates0)):
        return "%s at %s: nothing to make or sell (%d carapace, %d plates)" % (pilot, base, have.get(INPUT, 0), plates0)
    gate.take(pilot, "spacemolt", "craft")
    made = sold = price = 0
    try:
        before = wallet(pilot)
        if craft and runs:
            raw(pilot, "spacemolt", "craft", {"recipe_id": RECIPE, "quantity": runs, "deliver_to": "storage", "preset": "workshop"})
            for _ in range(30):
                time.sleep(TICK)
                if stored(pilot, base).get(OUTPUT, 0) >= plates0 + runs:
                    break
            made = stored(pilot, base).get(OUTPUT, 0) - plates0
        plates = stored(pilot, base).get(OUTPUT, 0)
        _, ans = raw(pilot, "spacemolt_market", "view_market", {"item_id": OUTPUT})
        price, depth = best_bid(ans)
        n = to_sell(plates, price, depth, min_bid) if sell else 0
        if n:
            raw(pilot, "spacemolt", "sell", {"item_id": OUTPUT, "quantity": n})
            time.sleep(TICK)
            sold = plates - stored(pilot, base).get(OUTPUT, 0)
        after = wallet(pilot)
        gain = (after - before) if isinstance(after, int) and isinstance(before, int) else None
        return "RESULT plate %s at %s: made %d, sold %d at %d cr (bid %d x %d), %d plates stay, wallet %s -> %s (%s cr)" % (
            pilot, base, made, sold, price, price, depth, plates - sold, before, after, gain)
    finally:
        gate.release(pilot)


def main():
    argv = sys.argv[1:]
    if not argv or "-h" in argv or "--help" in argv:
        sys.exit(__doc__)
    min_bid = 200
    if "--min-bid" in argv:
        i = argv.index("--min-bid")
        min_bid = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    pilots = [a for a in argv if not a.startswith("--")]
    for pilot in pilots:
        print(plate(pilot, min_bid, "--no-craft" not in argv, "--no-sell" not in argv, "--dry-run" in argv), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
