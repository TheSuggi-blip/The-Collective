#!/usr/bin/env python3
"""craftbook.py -- answer what can be made, fitted and built: a recipe, everything a thing takes, and what our stored goods can become.

WHAT: reads the game's catalog (the unit's data folder, catalog/<version>.json:
      recipes, items, facilities, hulls), the fleet's storage book
      (stock/storage.json, kept by the service `ledger`) and the saved order
      books (market/). It answers:
        item <text>         the items whose id or name holds the text; for one
                            item: what makes it, what uses it, what is built with it
        needs <item> [n]    everything n units take, step by step down to what is
                            mined or bought, beside what the fleet has in storage
        build <id>          what a facility or a hull costs and takes, with the
                            same list for its materials
        can [<Member>|all]  what the stored goods of a division's pilots can be
                            made into by hand today, at the station where they
                            lie, and what the result sells for at our stations
        recipes [...]       the recipes of a category, or those that make or use an item
RULES:
  - It reads only: it crafts nothing, buys nothing and moves no ship.
  - A list of needs follows one recipe per item: the one nearest to what
    is mined (so never one that takes a finished thing apart), by hand
    before in a facility, then the one with the fewest inputs. `item <id>`
    shows the others. Ore, ice and gas are taken as mined, never as made.
  - What a result sells for is the best bid of a saved order book and the
    units at that price: an estimate until sold (orders F12).
WHY:  what a base, a hull or a module takes was worked out by hand, call by
      call, and what lay in storage was never held against the recipes. The
      same tables as files: game/catalog/ in the repository.

USAGE:
  craftbook.py item <text>
  craftbook.py needs <item id> [quantity]
  craftbook.py build <facility id or hull id>
  craftbook.py can [<Member>|all] [--top N]
  craftbook.py recipes [--category <name>] [--makes <item id>] [--uses <item id>] [--hand]
  --data <dir>      the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import json
import math
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def load(data):
    """The newest catalog of the data folder with its look-up tables, or None."""
    files = [p for p in (Path(data) / "catalog").glob("*.json") if re.fullmatch(r"\d+(\.\d+)*", p.stem)]
    if not files:
        return None
    raw = read_json(max(files, key=lambda p: tuple(int(n) for n in p.stem.split("."))), {})
    cat = {"version": raw.get("version") or "?", "items": {i["id"]: i for i in raw.get("items") or []}, "recipes": {r["id"]: r for r in raw.get("recipes") or []},
           "facilities": {f["id"]: f for f in raw.get("facilities") or []}, "ships": {s["id"]: s for s in raw.get("ships") or []}, "makers": {}, "users": {}, "built": {}}
    for r in cat["recipes"].values():
        for o in r.get("outputs") or []:
            cat["makers"].setdefault(o.get("item_id"), []).append(r)
        for i in r.get("inputs") or []:
            cat["users"].setdefault(i.get("item_id"), []).append(r)
    for kind in ("facilities", "ships"):
        for row in cat[kind].values():
            for m in row.get("build_materials") or []:
                cat["built"].setdefault(m.get("item_id"), []).append(row["id"])
    return cat


def stock(data):
    """({item: units in storage, fleet}, {(pilot, station): {item: units}}, when the book was written)."""
    book = read_json(Path(data) / "stock" / "storage.json", {})
    total, places = {}, {}
    for pilot, entry in (book.get("pilots") or {}).items():
        for station, goods in ((entry or {}).get("stations") or {}).items():
            places[(pilot, station)] = goods
            for item, units in goods.items():
                total[item] = total.get(item, 0) + int(units or 0)
    return total, places, book.get("updated_at") or "not written yet"


def bids(data):
    """{item: (best bid, units at that price, station)} over the saved order books."""
    best = {}
    for path in sorted((Path(data) / "market").glob("*.json")):
        book = read_json(path, {})
        for row in book.get("items") or [] if isinstance(book, dict) else []:
            bid = row.get("best_buy") or 0
            depth = row.get("best_buy_qty") if isinstance(row.get("best_buy_qty"), (int, float)) else 1      # no depth saved: one unit (orders F12)
            if isinstance(bid, (int, float)) and bid > best.get(row.get("item_id"), (0,))[0]:
                best[row.get("item_id")] = (bid, int(depth or 0), book.get("base") or path.stem)
    return best


def mined(cat, item):
    row = cat["items"].get(item) or {}
    return row.get("category") == "ore" or bool(row.get("extracted_by"))


def rank(cat, item, open_items=()):
    """How many recipes lie between an item and what is mined: 0 for what is mined or has no recipe; 99 inside a circle."""
    memo = cat.setdefault("rank", {})
    if item in memo:
        return memo[item]
    makers = cat["makers"].get(item)
    if not makers or mined(cat, item):
        memo[item] = 0
        return 0
    if item in open_items or len(open_items) > 24:
        return 99
    best = min(1 + max([rank(cat, i.get("item_id"), open_items + (item,)) for i in r.get("inputs") or []] or [0]) for r in makers)
    if best < 99 or not open_items:
        memo[item] = best
    return best


def pick(cat, recipes):
    """The recipe a list of needs follows: nearest to what is mined, by hand first, then the fewest inputs."""
    return sorted(recipes, key=lambda r: (max([rank(cat, i.get("item_id")) for i in r.get("inputs") or []] or [0]), not r.get("hand_craftable"),
                                          len(r.get("inputs") or []), r["id"]))[0]


def expand(cat, item, units, steps, raw, trail=()):
    """Add what `units` of an item take to steps {item: [units, runs, recipe, depth]} and raw {item: units}."""
    makers = cat["makers"].get(item)
    if not makers or mined(cat, item) or item in trail or len(trail) > 24:
        raw[item] = raw.get(item, 0) + units
        return
    recipe = pick(cat, makers)
    per = sum(o.get("quantity") or 0 for o in recipe.get("outputs") or [] if o.get("item_id") == item) or 1
    runs = math.ceil(units / per)
    step = steps.setdefault(item, [0, 0, recipe, len(trail)])
    step[0], step[1], step[3] = step[0] + units, step[1] + runs, min(step[3], len(trail))
    for part in recipe.get("inputs") or []:
        expand(cat, part.get("item_id"), (part.get("quantity") or 0) * runs, steps, raw, trail + (item,))


def where(cat, recipe):
    if recipe.get("hand_craftable"):
        return "by hand"
    return "in a facility: " + ", ".join(recipe.get("produced_by_facility_ids") or ["?"])


def parts(rows):
    return ", ".join("%s %s" % (r.get("quantity"), r.get("item_id")) for r in rows or [])


def print_needs(cat, wanted, have, when):
    """The steps and the raw list for {item: units}."""
    steps, raw = {}, {}
    for item, units in wanted.items():
        expand(cat, item, units, steps, raw)
    if steps:
        print("Made on the way (one recipe per item):")
        for item, (units, runs, recipe, depth) in sorted(steps.items(), key=lambda kv: (kv[1][3], kv[0])):
            print("  %s%s %s <- %s x %s, %s%s" % ("  " * depth, "{:,}".format(units), item, recipe["id"], "{:,}".format(runs), where(cat, recipe),
                                                 " | in storage %s" % "{:,}".format(have[item]) if have.get(item) else ""))
    print("Mined or bought (storage book of %s):" % when)
    print("  %-34s %12s %12s %12s %10s" % ("item", "units", "in storage", "missing", "base value"))
    for item, units in sorted(raw.items(), key=lambda kv: -kv[1]):
        value = (cat["items"].get(item) or {}).get("base_value")
        print("  %-34s %12s %12s %12s %10s" % (item, "{:,}".format(units), "{:,}".format(have.get(item, 0)), "{:,}".format(max(0, units - have.get(item, 0))),
                                           value if value is not None else "?"))
    plants = sorted({f for _u, _r, recipe, _d in steps.values() if not recipe.get("hand_craftable") for f in recipe.get("produced_by_facility_ids") or []})
    if plants:
        print("Facilities the steps run in (any one per step): " + ", ".join(plants))


def show_item(cat, text, have):
    low = text.lower()
    hits = [i for i in cat["items"].values() if low == i["id"]] or [i for i in cat["items"].values() if low in i["id"] or low in str(i.get("name", "")).lower()]
    if not hits:
        print("no item holds `%s`" % text)
        return 1
    if len(hits) > 1:
        print("%d items hold `%s`:" % (len(hits), text))
        for i in sorted(hits, key=lambda i: i["id"])[:60]:
            print("  %-36s %-16s base value %s" % (i["id"], i.get("category") or ("module" if i.get("type") else ""), i.get("base_value")))
        return 0
    item = hits[0]
    print("%s (%s) | %s | size %s | base value %s | in storage, fleet: %s" % (item["id"], item.get("name"), item.get("category") or "module: %s, slot %s" % (item.get("type"), item.get("slot")),
                                                                         item.get("size"), item.get("base_value"), "{:,}".format(have.get(item["id"], 0))))
    if item.get("type"):
        print("  cpu %s, power %s | %s" % (item.get("cpu_usage"), item.get("power_usage"), json.dumps({k: item[k] for k in ("damage", "reach", "cooldown", "effect", "special") if item.get(k)})[:300]))
    makers = cat["makers"].get(item["id"]) or []
    print("Made by %d recipe(s)%s" % (len(makers), "" if makers else ": mined, dropped or bought only"))
    for r in sorted(makers, key=lambda r: (not r.get("hand_craftable"), r["id"]))[:12]:
        print("  %s: %s <- %s | %s" % (r["id"], parts(r.get("outputs")), parts(r.get("inputs")), where(cat, r)))
    users = cat["users"].get(item["id"]) or []
    print("Used in %d recipe(s): %s" % (len(users), ", ".join(sorted(r["id"] for r in users)[:14]) + (" ..." if len(users) > 14 else "")))
    built = cat["built"].get(item["id"]) or []
    print("Built with it: %d facilities and hulls: %s" % (len(built), ", ".join(sorted(built)[:10]) + (" ..." if len(built) > 10 else "")))
    return 0


def show_build(cat, key, have, when):
    row, kind = (cat["facilities"].get(key), "facility") if key in cat["facilities"] else (cat["ships"].get(key), "hull")
    if not row:
        near = sorted(k for k in list(cat["facilities"]) + list(cat["ships"]) if key in k)[:20]
        print("no facility or hull `%s`%s" % (key, ": did you mean " + ", ".join(near) if near else ""))
        return 1
    if kind == "facility":
        print("FACILITY %s (%s) | %s, level %s | cost %s cr, labor %s, build time %s%s%s" % (
            row["id"], row.get("name"), row.get("category"), row.get("level"), "{:,}".format(row.get("build_cost") or 0), row.get("labor_cost"), row.get("build_time"),
            " | makes with the recipe %s" % row["recipe_id"] if row.get("recipe_id") else "",
            " | gives %s" % (row.get("faction_service_type") or row.get("service_type") or row.get("personal_service_type")) if (row.get("faction_service_type") or row.get("service_type") or row.get("personal_service_type")) else ""))
        if row.get("requires_service_type"):
            print("  needs first: a facility that gives %s" % row["requires_service_type"])
        chain, step = [], row
        while step.get("upgrades_from") and step["upgrades_from"] in cat["facilities"] and len(chain) < 8:
            step = cat["facilities"][step["upgrades_from"]]
            chain.append("%s (level %s, %s cr)" % (step["id"], step.get("level"), "{:,}".format(step.get("build_cost") or 0)))
        if chain:
            print("  an upgrade of: " + " <- ".join(chain) + "; each step is built before the next")
    else:
        print("HULL %s (%s) | %s, %s, tier %s | Piloting %s | shipyard tier %s | hull %s, shield %s, cargo %s | slots weapon %s, defense %s, utility %s | cpu %s, power %s" % (
            row["id"], row.get("name"), row.get("faction"), row.get("class"), row.get("tier"), row.get("piloting_required") or "none", row.get("shipyard_tier"),
            row.get("base_hull"), row.get("base_shield"), row.get("cargo_capacity"), row.get("weapon_slots"), row.get("defense_slots"), row.get("utility_slots"),
            row.get("cpu_capacity"), row.get("power_capacity")))
    materials = {m.get("item_id"): m.get("quantity") or 0 for m in row.get("build_materials") or []}
    if not materials:
        print("  no build materials in the catalog")
        return 0
    print("Materials: " + parts(row.get("build_materials")))
    print_needs(cat, materials, have, when)
    return 0


def show_can(cat, data, who, top):
    have, places, when = stock(data)
    best = bids(data)
    found = {}
    for (pilot, station), goods in places.items():
        if who != "all" and division.owner(pilot, data) != who:
            continue
        for recipe in cat["recipes"].values():
            inputs = recipe.get("inputs") or []
            if not recipe.get("hand_craftable") or not inputs:
                continue
            runs = min(int(goods.get(i.get("item_id"), 0)) // max(1, i.get("quantity") or 1) for i in inputs)
            if runs > 0:
                row = found.setdefault((recipe["id"], station), [0, 0])
                row[0], row[1] = row[0] + runs, row[1] + 1
    rows = []
    for (rid, station), (runs, pilots) in found.items():
        recipe = cat["recipes"][rid]
        out = (recipe.get("outputs") or [{}])[0]
        units = runs * (out.get("quantity") or 0)
        bid, depth, base = best.get(out.get("item_id"), (0, 0, ""))
        brings = min(units, depth) * bid
        instead = sum(min(runs * (i.get("quantity") or 0), best.get(i.get("item_id"), (0, 0, ""))[1]) * best.get(i.get("item_id"), (0, 0, ""))[0] for i in recipe.get("inputs") or [])
        rows.append((brings - instead, brings, rid, station, runs, pilots, units, out.get("item_id"), bid, depth, base))
    rows.sort(reverse=True)
    print("CAN BE MADE BY HAND from stored goods | %s | storage book of %s | catalog %s | %d recipe-and-station pairs" % (
        "the fleet" if who == "all" else who, when, cat["version"], len(rows)))
    print("  each pilot crafts from its own storage at the station where the goods lie; `sells for` is the best saved bid and its depth: an estimate")
    for gain, brings, rid, station, runs, pilots, units, item, bid, depth, base in rows[:top]:
        sale = "sells for about %s cr (bid %s x %s at %s), %s more than the inputs at their bids" % ("{:,}".format(brings), bid, "{:,}".format(depth), base, "{:,}".format(gain)) if bid else "no bid for it in our books"
        print("  %-34s at %-32s x %-6s by %3d pilot(s) -> %s %s | %s" % (rid, station, "{:,}".format(runs), pilots, "{:,}".format(units), item, sale))
    if len(rows) > top:
        print("  ... %d more: --top N" % (len(rows) - top))
    return 0


def show_recipes(cat, args, value):
    rows = list(cat["recipes"].values())
    if value("--category", ""):
        rows = [r for r in rows if str(r.get("category")).lower() == value("--category", "").lower()]
    if value("--makes", ""):
        rows = [r for r in rows if any(o.get("item_id") == value("--makes", "") for o in r.get("outputs") or [])]
    if value("--uses", ""):
        rows = [r for r in rows if any(i.get("item_id") == value("--uses", "") for i in r.get("inputs") or [])]
    if "--hand" in args:
        rows = [r for r in rows if r.get("hand_craftable")]
    if len(rows) == len(cat["recipes"]):
        counts = {}
        for r in rows:
            counts[r.get("category")] = counts.get(r.get("category"), 0) + 1
        print("%d recipes in %d categories (catalog %s). Name one with --category, or an item with --makes or --uses:" % (len(rows), len(counts), cat["version"]))
        for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print("  %-24s %d" % (name, n))
        return 0
    print("%d recipes (catalog %s):" % (len(rows), cat["version"]))
    for r in sorted(rows, key=lambda r: r["id"])[:200]:
        print("  %s: %s <- %s | %s" % (r["id"], parts(r.get("outputs")), parts(r.get("inputs")), where(cat, r)))
    return 0


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    data = value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--data", "--top", "--category", "--makes", "--uses"))]
    if not words or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    cat = load(data)
    if cat is None:
        sys.exit("no catalog in %s/catalog: the service `routemaker` fetches it once a day" % data)
    verb, rest = words[0], words[1:]
    have, _places, when = stock(data)
    if verb == "item" and rest:
        return show_item(cat, " ".join(rest), have)
    if verb == "needs" and rest:
        if rest[0] not in cat["items"]:
            sys.exit("no item `%s`: find its id with `craftbook.py item <text>`" % rest[0])
        units = int(rest[1]) if len(rest) > 1 and rest[1].isdigit() else 1
        print("NEEDS of %s %s (catalog %s)" % ("{:,}".format(units), rest[0], cat["version"]))
        print_needs(cat, {rest[0]: units}, have, when)
        return 0
    if verb == "build" and rest:
        return show_build(cat, rest[0], have, when)
    if verb == "can":
        _kind, name = division.member()
        who = rest[0] if rest else (name if name in division.MEMBERS and name != "Unity" else "all")
        if who != "all" and who not in division.MEMBERS:
            sys.exit("`%s` is no member: %s, or all" % (who, ", ".join(division.MEMBERS)))
        return show_can(cat, data, who, int(value("--top", "15")))
    if verb == "recipes":
        return show_recipes(cat, args, value)
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
