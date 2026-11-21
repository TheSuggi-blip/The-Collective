#!/usr/bin/env python3
"""surplus.py -- say per item what the fleet holds beyond what its build targets reserve: the surplus a trader may sell, where it lies and its best bid.

WHAT: reads the reserve targets (game/reserve.tsv in the repository: what the fleet means to build or keep), the
      game's catalog, what the fleet owns (stock/storage.json: station storage and the holds, as
      craftbook.inventory adds it up) and the saved order books (market/). It answers:
        show      the items with surplus, best worth at a bid first: units held, reserved, surplus, the best bid
                  with its station and depth, and under each where the surplus lies with the bid at that very
                  station (a sale there needs no flight)
        reserve   per target what it takes; per item held against demand, what stock covers, what is still to
                  make and what is SHORT; a SUM line
        check     the gate of game/reserve.tsv and game/reserve-recipes.tsv: exit 1 on a line it does not understand
                  or that names what the catalog does not hold, or on a chosen recipe that does not make its item
      surplus(data, root) gives the same answer to other scripts as one dict.
RULES:
  - The targets file is tab-separated, `#` starts a comment, the header is `kind<TAB>id<TAB>units<TAB>note`.
    kind `facility` (a facility id of the catalog, units = how many), `hull` (a ship class id), `item` (an item
    id, units = how many to have on hand), `keep` (an item id; units a number, or `all` = never surplus),
    `keepkind` (a kind of item as craftbook.kind_of names it, units `all`: every item of it is kept whole), and the
    pull levels of a good: `max` (an item id, units = the most the fleet gathers of it, above 0) and `min` (an item
    id, units = the level below which it is gathered again, 0 or more). Without them a good the reserve asks for has
    max = what the reserve asks of it and min = 90 percent of max (pull.py, the dispatcher's pull rule); they reserve
    nothing and move no figure of this script. A second `max` or `min` line of an item replaces the first. An
    unknown kind or id is an error in `check` and is skipped elsewhere with a NOTE line: never guessed. A
    facility's earlier steps (`upgrades_from`) are targets of their own lines, never added by the script.
  - DEMAND at the top is the build materials of every facility and hull target times its units, plus the item
    targets. It is met level by level: first from what the fleet holds of the item itself (RESERVED, capped by
    what is held); what is still missing is made by the recipe craftbook's `needs` follows (craftbook.recipe_for:
    the one game/reserve-recipes.tsv names for the item, kept by Logistics; else nearest to what is mined, by
    hand before a facility, then the fewest inputs; `reserve` names the recipe taken of every item that has
    more than one, and a row of that file the catalog cannot follow is skipped with a NOTE), whose inputs become demand
    one level down, to what is mined (craftbook.mined) or what no recipe makes (hunted, dropped or bought). An
    item is netted once, after every item that can ask for it (craftbook.rank, highest first), so its whole
    demand meets its stock at once. A recipe run only in a facility is still followed; its row says `facility`.
  - SHORT is the demand that neither stock nor a recipe chain from stock covers; at the raw level, what must
    still be mined, hunted or bought. An input that several items use is shared among them in proportion to
    what each asks of it.
  - The walk follows one recipe per item. What ANOTHER recipe could make of our stock is no surplus either: an
    input of any other recipe of an item the reserve is short of is HELD BACK, as many units as that recipe would
    take to cover the shortage, capped by what is held (one step only: the inputs of that recipe, not their own
    inputs). Its row says what it could make. Read every recipe of a short item before a chain is planned
    (`craftbook.py item <id>`).
  - `keep` and `keepkind` add to the reserved units, capped by what is held. SURPLUS = held - reserved, never
    below 0. No reserve file: no targets, nothing kept, everything held is surplus, and the first line says so.
  - The reserve of an item is taken first from the place that holds the most of it (building happens where the
    goods are gathered); the rest is surplus where it lies.
  - A price is only a bid read from a saved order book (craftbook.bids: the best bid anywhere, its units at that
    price, its station); a base value is no price. An item with no bid anywhere says `no bid`. worth at bid =
    the surplus units the bid's depth covers times the bid: an estimate until sold (orders F12).
  - The first line of every answer names what it rests on: the reserve file, the storage book's time, the
    catalog's version, the order books read and the age of the oldest.
  - It reads only: it sells nothing, moves no ship and writes no file. It names stations and items, never a pilot.
WHY:  one division sold iron ore while another bought it for steel plates: nobody could say which stored goods
      were free to sell. One list of what the fleet means to build, and one answer from it for every member.

USAGE:
  surplus.py show [--top N] [--kind <kind>] [--item <item id>] [--all]
  surplus.py reserve
  surplus.py check
  --root <dir>      the repository (default: two folders above this file)
  --data <dir>      the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import math
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import craftbook                                  # noqa: E402  the catalog, the inventory, the bids and the recipe rule
import division                                   # noqa: E402  the data folder's default

FILE = "game/reserve.tsv"
HEADER = ["kind", "id", "units", "note"]
LEVELS = ("max", "min")       # the pull levels of a good (pull.py): no target, nothing reserved
TARGETS = ("facility", "hull", "item", "keep", "keepkind") + LEVELS
ITEM_KINDS = tuple(key for key, _title in craftbook.KINDS if key != "unknown")      # the kinds a `keepkind` line may name
OPTIONS = ("--root", "--data", "--top", "--kind", "--item")
RULE = ("Split over places: the reserve of an item is taken first from the place that holds the most of it (building happens where the goods are "
        "gathered); the rest is surplus where it lies.")
EMPTY = {"version": "none", "items": {}, "recipes": {}, "facilities": {}, "ships": {}, "makers": {}, "users": {}, "built": {}}
num = "{:,}".format


def read_targets(path, cat):
    """(targets, errors, warnings, present) of the targets file. A target is {line, kind, id, units (int or `all`), note};
    an error names its line and the line is skipped. With cat None only the form is checked, not the ids."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return [], [], [], False
    except (OSError, UnicodeDecodeError) as error:
        return [], ["%s: not readable (%s)" % (FILE, type(error).__name__)], [], True
    targets, errors, warnings, header, seen = [], [], [], False, {}
    version = (cat or {}).get("version")
    for number, raw in enumerate(text.split("\n"), 1):
        line = raw.rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = [c.strip() for c in line.split("\t")]
        if cells[:4] == HEADER:
            header = True
            continue
        if not header:
            errors.append("line %d: the header `kind<TAB>id<TAB>units<TAB>note` must come before the first target" % number)
            header = True                                       # said once; the line itself is still read
        if len(cells) < 3 or not cells[0] or not cells[1]:
            errors.append("line %d: needs kind, id and units separated by tabs: `%s`" % (number, line[:80]))
            continue
        kind, key, units, note = cells[0], cells[1], cells[2], cells[3] if len(cells) > 3 else ""
        if kind not in TARGETS:
            errors.append("line %d: no kind of target `%s` (%s)" % (number, kind, ", ".join(TARGETS)))
            continue
        if kind == "keepkind":
            if key not in ITEM_KINDS:
                errors.append("line %d: no kind of item `%s` (%s)" % (number, key, ", ".join(ITEM_KINDS)))
                continue
            if units not in ("all", ""):
                errors.append("line %d: a keepkind keeps every item of the kind whole: units `all`, not `%s`" % (number, units))
                continue
            units = "all"
        else:
            table = {"facility": "facilities", "hull": "ships"}.get(kind, "items")
            if cat is not None and key not in cat[table]:
                errors.append("line %d: no %s `%s` in the catalog %s" % (number, {"facilities": "facility", "ships": "hull", "items": "item"}[table], key, version))
                continue
            if kind == "keep" and units == "all":
                pass
            elif units.isdigit() and (int(units) > 0 or kind == "min"):
                units = int(units)
            else:
                errors.append("line %d: units must be a whole number %s%s, not `%s`" % (number, "0 or more" if kind == "min" else "above 0",
                                                                                     " or `all`" if kind == "keep" else "", units))
                continue
        if (kind, key) in seen:
            warnings.append("line %d: %s %s stands on line %d too: %s" % (number, kind, key, seen[(kind, key)], "this one counts" if kind in LEVELS else "both count"))
        seen.setdefault((kind, key), number)
        targets.append({"line": number, "kind": kind, "id": key, "units": units, "note": note})
    return targets, errors, warnings, True


def order_books(data):
    """({base: {item: (bid, units at that price)}}, order books read, the oldest reading): the bid at each station, read
    from the same fields and with the same depth rule as craftbook.bids, which gives the best bid anywhere."""
    by, read = {}, []
    for path in sorted((Path(data) / "market").glob("*.json")):
        book = craftbook.read_json(path, {})
        if not isinstance(book, dict) or not isinstance(book.get("items"), list):
            continue                                            # the market folder's other files (history, ladders) are no order book
        here = by.setdefault(book.get("base") or path.stem, {})
        read.append(book.get("read_at") or "")
        for row in book["items"]:
            if not isinstance(row, dict):
                continue
            bid = row.get("best_buy") or 0
            depth = row.get("best_buy_qty") if isinstance(row.get("best_buy_qty"), (int, float)) else 1      # no depth saved: one unit (orders F12)
            if isinstance(bid, (int, float)) and bid > here.get(row.get("item_id"), (0,))[0]:
                here[row.get("item_id")] = (bid, int(depth or 0))
    stamps = sorted(r for r in read if r)
    return by, len(read), stamps[0] if stamps else ""


def age(stamp, now):
    try:
        minutes = max(0, int((now - calendar.timegm(time.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ"))) // 60))
    except (TypeError, ValueError):
        return "age unknown"
    return "%d min old" % minutes if minutes < 120 else "%.1f h old" % (minutes / 60.0)


def meet(cat, held, top, labels):
    """Meet the demand {item: units} level by level against held {item: units}: {item: step}. A step is {demand, taken
    (from stock), make (units still to make), runs, recipe, inputs {item: units asked}, missing (units no recipe
    makes), short, by (the targets whose demand reaches it)}."""
    steps, pending, done, labels = {}, dict(top), set(), {item: set(names) for item, names in labels.items()}
    order = lambda item: (-craftbook.rank(cat, item), item)
    while pending:
        item = min(pending, key=order)                              # the highest rank first: whatever asks for an item is netted before it
        units = pending.pop(item)
        step = steps.setdefault(item, {"demand": 0, "taken": 0, "make": 0, "runs": 0, "per": 1, "recipe": None, "inputs": {}, "missing": 0, "short": 0,
                                       "by": set()})
        step["by"].update(labels.get(item, ()))
        take = min(max(0, held.get(item, 0) - step["taken"]), units)
        step["demand"], step["taken"], rest = step["demand"] + units, step["taken"] + take, units - take
        if rest <= 0:
            continue
        makers = cat["makers"].get(item)
        if not makers or craftbook.mined(cat, item) or item in done:
            step["missing"] += rest                                 # mined, hunted or bought; or asked again inside a circle of recipes (craftbook's trail rule)
            continue
        done.add(item)
        recipe = craftbook.recipe_for(cat, item)
        per = sum(o.get("quantity") or 0 for o in recipe.get("outputs") or [] if o.get("item_id") == item) or 1
        runs = math.ceil(rest / per)
        step.update(make=rest, runs=runs, per=per, recipe=recipe)
        for part in recipe.get("inputs") or []:
            need = (part.get("quantity") or 0) * runs
            if need <= 0:
                continue
            step["inputs"][part.get("item_id")] = step["inputs"].get(part.get("item_id"), 0) + need
            pending[part.get("item_id")] = pending.get(part.get("item_id"), 0) + need
            labels.setdefault(part.get("item_id"), set()).update(step["by"])
    cover = {}
    for item in sorted(steps, key=lambda i: (craftbook.rank(cat, i), i)):      # from what is mined up: every input is known before what it makes
        step = steps[item]
        made = 0
        if step["runs"]:
            share = min([cover.get(part, Fraction(1)) for part in step["inputs"]] or [Fraction(1)])     # each asker gets its share of an input's cover
            made = min(step["make"], math.floor(step["runs"] * share) * step["per"])
        step["short"] = step["demand"] - step["taken"] - made
        cover[item] = Fraction(step["demand"] - step["short"], step["demand"]) if step["demand"] else Fraction(1)
    return steps


def held_back(cat, steps, held):
    """{item: (units, [what it could make])}: the inputs of every OTHER recipe of an item the reserve is short of, as many
    units as that recipe takes to cover the shortage. What is mined has no recipe to follow and holds nothing back."""
    back = {}
    for item in sorted(steps):
        step = steps[item]
        if step["short"] <= 0 or craftbook.mined(cat, item):
            continue
        used = step["recipe"]["id"] if step["recipe"] else None
        for recipe in cat["makers"].get(item) or []:
            if recipe.get("id") == used:
                continue
            per = sum(o.get("quantity") or 0 for o in recipe.get("outputs") or [] if o.get("item_id") == item) or 1
            runs = math.ceil(step["short"] / per)
            for part in recipe.get("inputs") or []:
                need = (part.get("quantity") or 0) * runs
                if need > 0 and held.get(part.get("item_id"), 0) > 0 and part.get("item_id") != item:
                    units, names = back.get(part.get("item_id"), (0, []))
                    back[part.get("item_id")] = (units + need, names + ["%s (%s)" % (item, recipe.get("id"))])
    return back


def split(at, reserved):
    """[(place, units of surplus there)]: the reserve is taken first from the place with the most units (stations before the
    holds on a tie, then by id); the rest is surplus where it lies."""
    left, out = reserved, []
    for place, units in sorted(at.items(), key=lambda kv: (-kv[1], kv[0] == "hold", kv[0])):
        take = min(units, left)
        left -= take
        if units - take > 0:
            out.append((place, units - take))
    return sorted(out, key=lambda pu: (-pu[1], pu[0]))


def how_made(cat, item, step):
    """How the reserve gets an item: `by hand` or `facility` (the recipe it follows), `mined`, `no recipe` (hunted, dropped or bought),
    `stock` (what is held covers the demand), `circle` (asked again inside a circle of recipes); empty when nothing asks for it."""
    if step and step["recipe"]:
        return "by hand" if craftbook.by_hand(step["recipe"]) else "facility"
    if craftbook.mined(cat, item):
        return "mined"
    if not cat["makers"].get(item):
        return "no recipe"
    return "" if not step else ("circle" if step["missing"] else "stock")


def why_text(labels, keep, kinds, kind, could=()):
    parts = []
    if labels:
        names = sorted(labels)
        parts.append("for " + ", ".join(names[:3]) + (" +%d more" % (len(names) - 3) if len(names) > 3 else ""))
    if kind in kinds:
        parts.append("keepkind " + kind)
    if keep:
        parts.append("keep %s" % (keep if keep == "all" else num(keep)))
    if could:
        parts.append("held back: another recipe could make " + ", ".join(could[:3]) + (" +%d more" % (len(could) - 3) if len(could) > 3 else ""))
    return "; ".join(parts)


def surplus(data, root, cat=None, now=None):
    """The reserve and the surplus of every item held or asked for: {written, catalog, file, present, targets, errors, warnings,
    books: {read, oldest, age}, rows, totals, rule, choices (craftbook.choose: game/reserve-recipes.tsv, its rows and errors),
    taken (craftbook.taken_lines: the recipe the walk took of every item that has more than one), levels ({item: {max, min}}
    of the file's `max` and `min` lines)}. A row is {id, name, kind, held, demand, taken, make, recipe, how, level,
    kept, reserved, surplus, short, why, bid, bid_units, bid_at, bid_at_name, worth_at_bid, at: [{place, name, units, bid,
    bid_units}]}, the most worth at a bid first; bid is None where no order book bids for the item, and worth_at_bid is then 0."""
    cat = craftbook.choose(cat or craftbook.load(data) or dict(EMPTY), root)      # the recipes the fleet chose (game/reserve-recipes.tsv)
    now = time.time() if now is None else now
    targets, errors, warnings, present = read_targets(Path(root) / FILE, cat)
    inv = craftbook.inventory(data, cat)
    have = {r["id"]: r for g in inv["groups"] for r in g["rows"]}
    held = {item: r["units"] for item, r in have.items()}
    top, labels, keep, kinds, levels = {}, {}, {}, set(), {}
    for t in targets:
        t["takes"], t["fee"] = {}, None
        if t["kind"] in LEVELS:                                 # a pull level: no demand, nothing reserved (pull.py reads it)
            levels.setdefault(t["id"], {})[t["kind"]] = t["units"]
            continue
        if t["kind"] in ("facility", "hull"):
            row = cat["facilities" if t["kind"] == "facility" else "ships"][t["id"]]
            for m in row.get("build_materials") or []:
                t["takes"][m.get("item_id")] = t["takes"].get(m.get("item_id"), 0) + (m.get("quantity") or 0) * t["units"]
            t["fee"] = (row.get("build_cost") or 0) * t["units"] if t["kind"] == "facility" else None
        elif t["kind"] == "item":
            t["takes"][t["id"]] = t["units"]
        elif t["kind"] == "keep":
            keep[t["id"]] = "all" if "all" in (t["units"], keep.get(t["id"])) else keep.get(t["id"], 0) + t["units"]
        else:
            kinds.add(t["id"])
        label = t["id"] if t["kind"] != "item" else "%s on hand" % t["id"]
        for item, units in t["takes"].items():
            if units > 0:
                top[item] = top.get(item, 0) + units
                labels.setdefault(item, set()).add(label)
    steps = meet(cat, held, top, labels)
    other = held_back(cat, steps, held)
    best = craftbook.bids(data)
    there, read, oldest = order_books(data)
    rows = []
    for item in sorted(set(held) | set(steps)):
        known = cat["items"].get(item) or {}
        step = steps.get(item)
        kind = have[item]["kind"] if item in have else craftbook.kind_of(known)
        units = held.get(item, 0)
        taken = step["taken"] if step else 0
        kept = "all" if keep.get(item) == "all" or kind in kinds else keep.get(item, 0)
        reserved = units if kept == "all" else min(units, taken + kept)
        back = min(units - reserved, other.get(item, (0, []))[0])      # what another recipe of a short item would take of it
        reserved += back
        free = max(0, units - reserved)
        bid, depth, base = best.get(item, (None, 0, None))
        at = [{"place": place, "name": craftbook.place_name(data, place), "units": n, "bid": there.get(place, {}).get(item, (None, 0))[0],
               "bid_units": there.get(place, {}).get(item, (None, 0))[1]} for place, n in split(have[item]["at"] if item in have else {}, reserved)]
        rows.append({"id": item, "name": known.get("name") or item, "kind": kind, "held": units, "demand": step["demand"] if step else 0, "taken": taken,
                     "make": step["make"] if step else 0, "recipe": step["recipe"]["id"] if step and step["recipe"] else None, "how": how_made(cat, item, step),
                     "level": craftbook.rank(cat, item) if known else 0, "kept": kept, "back": back, "reserved": reserved, "surplus": free,
                     "short": step["short"] if step else 0,
                     "why": why_text(step["by"] if step else (), keep.get(item), kinds, kind, other.get(item, (0, []))[1] if back else ()),
                     "bid": bid, "bid_units": depth if bid else 0, "bid_at": base, "bid_at_name": craftbook.place_name(data, base) if base else None,
                     "worth_at_bid": min(free, depth) * bid if bid else 0, "at": at})
    rows.sort(key=lambda r: (-r["worth_at_bid"], -r["surplus"], r["id"]))
    raw = [r for r in rows if r["short"] > 0 and not r["recipe"]]
    totals = {"items": sum(1 for r in rows if r["held"]), "held": sum(r["held"] for r in rows), "reserved": sum(r["reserved"] for r in rows),
              "surplus": sum(r["surplus"] for r in rows), "with_surplus": sum(1 for r in rows if r["surplus"]),
              "no_bid": sum(1 for r in rows if r["surplus"] and not r["bid"]), "worth_at_bid": sum(r["worth_at_bid"] for r in rows),
              "short_items": sum(1 for r in rows if r["short"] > 0), "short_raw": sum(r["short"] for r in raw), "short_raw_items": len(raw),
              "fees": sum(t["fee"] or 0 for t in targets)}
    return {"written": inv["written"], "catalog": cat["version"], "file": FILE, "present": present, "targets": targets, "errors": errors,
            "warnings": warnings, "books": {"read": read, "oldest": oldest, "age": age(oldest, now) if oldest else ""}, "rows": rows, "totals": totals,
            "rule": RULE, "choices": cat["choices"], "taken": craftbook.taken_lines(cat, {item: s["recipe"] for item, s in steps.items() if s["recipe"]}),
            "levels": levels}


def first_line(title, res):
    """What an answer rests on, in its first line."""
    if res["present"]:
        file = "reserve file %s (%d targets%s)" % (res["file"], len(res["targets"]), ", %d lines skipped" % len(res["errors"]) if res["errors"] else "")
    else:
        file = "NO RESERVE FILE %s: no targets, nothing kept, everything held is surplus" % res["file"]
    books = "%d order books, the oldest read %s (%s)" % (res["books"]["read"], res["books"]["oldest"] or "--", res["books"]["age"] or "age unknown") \
        if res["books"]["read"] else "no order book read: no bid anywhere"
    chosen = res.get("choices") or {}
    recipes = " | recipes chosen in %s: %d%s" % (chosen["file"], len(chosen["rows"]), ", %d rows skipped" % len(chosen["errors"]) if chosen["errors"] else "") \
        if chosen.get("present") else ""                            # no file of chosen recipes: the line as it always was
    return "%s | %s | storage book of %s | catalog %s | %s%s" % (title, file, res["written"] or "-- (none yet)", res["catalog"], books, recipes)


def bid_text(bid, units, at=None, place=None):
    if place == "hold":
        return "-- (not at a station)"
    if not bid:
        return "no bid"
    return "%s cr x %s%s" % (num(bid), num(units), " at " + at if at else "")


def notes(res):
    for error in res["errors"] + (res.get("choices") or {}).get("errors", []):
        print("  NOTE %s: skipped" % error)
    for warning in res["warnings"] + (res.get("choices") or {}).get("warnings", []):
        print("  NOTE %s" % warning)


def show(res, top, kind, item, every):
    print(first_line("SURPLUS | what the fleet holds beyond its reserve, best worth at a bid first", res))
    if not res["written"]:
        print("no storage book yet: the service `ledger` writes stock/storage.json")
        return 1
    notes(res)
    t = res["totals"]
    print("  TOTAL %s items with surplus of %s held | %s units held, %s reserved, %s surplus | %s cr at the best bids within their depth (an estimate "
          "until sold) | %s items with surplus have no bid anywhere" % (num(t["with_surplus"]), num(t["items"]), num(t["held"]), num(t["reserved"]),
                                                                        num(t["surplus"]), num(t["worth_at_bid"]), num(t["no_bid"])))
    rows = res["rows"]
    if item:
        rows = [r for r in rows if r["id"] == item]
        if not rows:
            print("  no %s held and none asked for by a target" % item)
            print(RULE)
            return 0
    else:
        rows = [r for r in rows if (every or r["surplus"] > 0) and (not kind or r["kind"] == kind)]
    print("  %-40s %-10s %11s %11s %11s  %-50s %12s" % ("item", "kind", "held", "reserved", "surplus", "best bid (units at it, station)", "worth at bid"))
    for r in rows[:top] if not item else rows:
        print("  %-40s %-10s %11s %11s %11s  %-50s %12s" % (("%s (%s)" % (r["name"], r["id"]))[:40], r["kind"], num(r["held"]), num(r["reserved"]),
                                                           num(r["surplus"]), bid_text(r["bid"], r["bid_units"], r["bid_at_name"]), num(r["worth_at_bid"])))
        if item and r["why"]:
            print("      reserved %s" % r["why"])
        if item and r["short"]:
            print("      short %s: %s" % (num(r["short"]), "to mine, hunt or buy" if not r["recipe"] else "not covered by stock nor made from it"))
        for place in r["at"]:
            print("      %-44s %11s surplus here | bid here: %s" % (place["name"][:44], num(place["units"]), bid_text(place["bid"], place["bid_units"], place=place["place"])))
    if not item and len(rows) > top:
        print("  ... %d more: --top N" % (len(rows) - top))
    print(RULE)
    return 0


def show_reserve(res):
    print(first_line("RESERVE | what the targets take, level by level, against what the fleet holds", res))
    if not res["written"]:
        print("no storage book yet: the service `ledger` writes stock/storage.json")
        return 1
    notes(res)
    rows = {r["id"]: r for r in res["rows"]}
    print("Targets (%s):" % res["file"])
    if not res["targets"]:
        print("  none")
    for t in res["targets"]:
        if t["kind"] in ("facility", "hull", "item"):
            what = ", ".join("%s %s" % (num(n), i) for i, n in sorted(t["takes"].items())) or "no build materials in the catalog"
            print("  %s %s x %s: %s%s%s" % (t["kind"], t["id"], t["units"], what, " | fee %s cr" % num(t["fee"]) if t["fee"] else "", " | " + t["note"] if t["note"] else ""))
        elif t["kind"] in LEVELS:
            print("  %s %s %s: the pull level of the dispatcher's pull rule (pull.py)%s" % (t["kind"], t["id"], num(t["units"]), " | " + t["note"] if t["note"] else ""))
        elif t["kind"] == "keep":
            r = rows.get(t["id"])
            print("  keep %s %s: %s held, %s reserved%s" % (t["id"], t["units"] if t["units"] == "all" else num(t["units"]), num(r["held"] if r else 0),
                                                          num(r["reserved"] if r else 0), " | " + t["note"] if t["note"] else ""))
        else:
            mine = [r for r in res["rows"] if r["kind"] == t["id"] and r["held"]]
            print("  keepkind %s: %d items, %s units held, all kept%s" % (t["id"], len(mine), num(sum(r["held"] for r in mine)), " | " + t["note"] if t["note"] else ""))
    asked = sorted((r for r in res["rows"] if r["demand"]), key=lambda r: (-r["level"], r["id"]))
    print("Items, from the top level down (level = recipe steps above what is mined or bought; to make = units still made by the recipe):")
    print("  %-30s %5s %-42s %11s %11s %11s %11s %11s" % ("item", "level", "how", "held", "demand", "from stock", "to make", "SHORT"))
    for r in asked:
        how = "%s, %s" % (r["recipe"], r["how"]) if r["recipe"] else r["how"]
        print("  %-30s %5s %-42s %11s %11s %11s %11s %11s" % (r["id"][:30], r["level"], how[:42], num(r["held"]), num(r["demand"]), num(r["taken"]),
                                                              num(r["make"]), num(r["short"])))
    taken = [line for line in res.get("taken") or [] if not line.startswith("NOTE ")]      # the skipped rows stand under the first line already
    if taken:
        print(craftbook.TAKEN)
        for line in taken:
            print("  " + line)
    backs = sorted((r for r in res["rows"] if r.get("back")), key=lambda r: (-r["back"], r["id"]))
    if backs:
        print("Held back, not surplus: an input of another recipe of something that is short (one recipe is followed above; read them all with `craftbook.py item <id>`):")
        for r in backs:
            print("  %-30s %11s of %s held | %s" % (r["id"][:30], num(r["back"]), num(r["held"]), r["why"].split("held back: ")[-1]))
    t = res["totals"]
    print("SUM | %d items asked for | %s held, %s demand, %s from stock, %s to make | SHORT %s units of %d items to mine, hunt or buy (%d items short in all) | fees %s cr"
          % (len(asked), num(sum(r["held"] for r in asked)), num(sum(r["demand"] for r in asked)), num(sum(r["taken"] for r in asked)),
             num(sum(r["make"] for r in asked)), num(t["short_raw"]), t["short_raw_items"], t["short_items"], num(t["fees"])))
    print(RULE)
    return 0


def check(res):
    """The gate of game/reserve.tsv and of game/reserve-recipes.tsv (craftbook.read_choices: a row of an unknown item or recipe,
    or of a recipe that does not make its item, fails here though the answers merely skip it)."""
    print(first_line("CHECK %s" % res["file"], res))
    chosen = res.get("choices") or {"errors": [], "warnings": []}
    errors, warnings = chosen["errors"], chosen["warnings"]
    if not res["present"]:
        print("  no reserve file: nothing to check (no targets is no error)")
    else:
        errors, warnings = res["errors"] + errors, res["warnings"] + warnings
    for error in errors:
        print("  ERROR %s" % error)
    for warning in warnings:
        print("  WARNING %s" % warning)
    print("Errors: %d | Warnings: %d" % (len(errors), len(warnings)))
    return 1 if errors else 0


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in OPTIONS)]
    if not words or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    cat = craftbook.load(data)
    if cat is None:
        sys.exit("no catalog in %s/catalog: the hourly job fetches it (scripts/catalog-refresh.py)" % data)
    verb = words[0]
    if verb not in ("show", "reserve", "check"):
        sys.exit(__doc__)
    top, kind = value("--top", "15"), value("--kind", "")
    if not top.isdigit():
        sys.exit("--top takes a whole number, not `%s`" % top)
    if kind and kind not in ITEM_KINDS + ("unknown",):
        sys.exit("no kind of item `%s`: %s" % (kind, ", ".join(ITEM_KINDS + ("unknown",))))
    res = surplus(data, root, cat)
    if verb == "check":
        return check(res)
    if verb == "reserve":
        return show_reserve(res)
    return show(res, int(top), kind, value("--item", ""), "--all" in args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
