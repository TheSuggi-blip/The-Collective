#!/usr/bin/env python3
"""hive.py -- the fleet's figures from its own readings: money, routes and their history, levels, what the work carries, what a base takes, a system.

WHAT: reads the unit's data folder (fleet/, routes/runs.jsonl, market/, scouting/, wildlife/, stock/, catalog/, intel/) and
      the route files, and prints one answer:
        fleet                 credits, steady money per hour (rewards paid once left out) over 1, 6 and 24 hours, per division
        routes                every route: its group, zone, ships on it, what its runs measured, and its runs in the last hours
        route <id>            one route: its file, its last runs, and its credits per ship-hour hour by hour
        history               the fleet's credits hour by hour, with and without the rewards paid once, per division
        ship <pilot>          one ship: place, hull, fuel, hold, modules, wallet, order, skills
        levels                per division: the pilots' levels, the XP an hour since birth, the hours to the next hull tier
        capacity              what mining, hunting and the missions that pay once carry: bids, what is left in the fields,
                              what regrows, herds, tools; and how many ships that employs against the ships we have
        base outpost|station  what founding one takes, down to the ore: credits, parts, the facility that makes the part,
                              what we hold, what is missing and where our readings show it
        system <id>           one system: chart, places, what is left in its fields, its herds, its market, who was met, our ships
        learnings             per member: its newest report, and the knowledge files and learning questions it wrote or
                              changed in the last hours (from the git history of its workspace)
RULES:
  - It reads only: it moves no ship and writes no file.
  - Every figure names what it rests on; what no reading holds is printed as `not measured`, never filled in.
  - A route's group and zone are the route index's own (routes.py); a waiting ship is the dispatcher's own rule (fill.py).
WHY:  the same questions were answered turn after turn by hand, each Admiral with its own arithmetic. One script, the
      same for all, and the collective MCP server (collective_mcp.py) hands its answers to every member as tools.

USAGE:
  hive.py fleet
  hive.py routes [--group once|paying|test|fit|service|losing|off] [--kind <kind>] [--zone home|beyond] [--hours N]
  hive.py route <route id>
  hive.py history [--hours N]
  hive.py ship <pilot>
  hive.py levels [<Member>|all]
  hive.py capacity
  hive.py base outpost|station
  hive.py system <system id>
  hive.py learnings [--hours N]
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import os
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import craftbook                                  # noqa: E402  the catalog: what a thing takes
import dispatch                                   # noqa: E402  routes, orders, runs
import division                                   # noqa: E402  who commands which ship
import routes as routefiles                       # noqa: E402  a route's group and zone, what a run earned

HOLD = 65                      # a starter's hold, units
TURN = 4                       # hours: what a bid or a field must carry
PAYS = 1000                    # credits a hold must bring at the best bid before a good counts as paying work
PROFILES = "/opt/data/profiles"                  # each member's workspace: <PROFILES>/<name>/workspace-<name>
FEES = {"outpost": ("outpost_kit", 100000), "station": ("station_core", 5000000)}      # the founding fee: the game's faction guide, read 2026-11-15
TIERS = ((10, 2), (20, 3), (30, 4), (50, 5))                                           # Piloting level -> hull tier (game/catalog/master-index.md)


def worth(route):
    """What the runs measured: credits per ship-hour, for a route that pays once credits per run; None when not measured."""
    measured = route.get("measured") or {}
    if not measured:
        return None
    return measured.get("credits_per_run") if route.get("once") else measured.get("cph_per_ship")


def num(n):
    return format(int(round(n)), ",") if isinstance(n, (int, float)) else "--"


def epoch(stamp):
    try:
        return calendar.timegm(time.strptime(str(stamp)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0


def ago(stamp, now):
    t = epoch(stamp)
    return "%d min ago" % ((now - t) // 60) if t else "never"


def read(path, default):
    return dispatch.read_json(path, default)


def books(data):
    """{base: {item: row}} of the saved order books, and {base: (system, when read)}."""
    out, where = {}, {}
    for path in sorted((Path(data) / "market").glob("*.json")):
        book = read(path, {})
        if isinstance(book, dict) and isinstance(book.get("items"), list):
            base = book.get("base") or path.stem
            out[base] = {row.get("item_id"): row for row in book["items"] if isinstance(row, dict)}
            where[base] = (book.get("system") or "?", book.get("read_at") or "")
    return out, where


def label(base, where):
    """A base's id, or for a player's station (an id of 32 hex digits) `station in <system>`."""
    hexid = len(str(base)) == 32 and all(c in "0123456789abcdef" for c in str(base))
    return "station in %s" % (where.get(base) or ("?", ""))[0] if hexid else str(base)


def demand(market, item, floor):
    """(best bid, units bid for at `floor` credits or more over all stations, stations that bid so, the base of the best bid)."""
    best, units, count = (0, ""), 0, 0
    for base, rows in market.items():
        row = rows.get(item) or {}
        bid = row.get("best_buy") or 0
        if bid >= floor and bid > 0:
            units += int(row.get("best_buy_qty") if isinstance(row.get("best_buy_qty"), (int, float)) else 1)
            count += 1
            best = max(best, (bid, base))
    return best[0], units, count, best[1]


def best_bid(market, item):
    """(bid, units at that bid, base) of the best saved bid for an item; (0, 0, '') when nobody bids."""
    best = (0, 0, "")
    for base, rows in market.items():
        row = rows.get(item) or {}
        if (row.get("best_buy") or 0) > best[0]:
            best = (row["best_buy"], int(row.get("best_buy_qty") if isinstance(row.get("best_buy_qty"), (int, float)) else 1), base)
    return best


def cheapest(market, item, limit=3):
    rows = [((r.get(item) or {}).get("best_sell") or 0, int((r.get(item) or {}).get("best_sell_qty") or (r.get(item) or {}).get("sell_quantity") or 0), base)
            for base, r in market.items()]
    return sorted(r for r in rows if r[0] > 0)[:limit]


def fields(data):
    """[(system, place, resource, remaining, max, richness, when read)] from the census files."""
    out = []
    for path in sorted((Path(data) / "scouting").glob("*.json")):
        scan = read(path, {})
        for poi, entry in (scan.get("pois") or {}).items() if isinstance(scan, dict) and isinstance(scan.get("pois"), dict) else []:
            for res in entry.get("resources") or [] if isinstance(entry, dict) else []:
                if isinstance(res, dict) and res.get("resource_id"):
                    out.append((path.stem, poi, res["resource_id"], res.get("remaining"), res.get("max_remaining"), res.get("richness"), scan.get("read_at") or ""))
    return out


def regrowth(data):
    """({(system, place, resource): units an hour}, {(system, place, species): (fewest, most, last)}) between the first and
    the last census of a place, from wildlife/history.jsonl. A field's figure is net: what grew back less what was mined."""
    deposits, herds = defaultdict(list), defaultdict(list)
    try:
        with open(Path(data) / "wildlife" / "history.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                at = epoch(row.get("at"))
                for poi, found in (row.get("deposits") or {}).items():
                    for res, units in (found or {}).items():
                        if isinstance(units, (int, float)):
                            deposits[(row.get("system"), poi, res)].append((at, units))
                for poi, found in (row.get("herds") or {}).items():
                    for species, count in (found or {}).items():
                        herds[(row.get("system"), poi, species)].append((at, count))
    except OSError:
        pass
    rates = {}
    for key, seen in deposits.items():
        seen.sort()
        hours = (seen[-1][0] - seen[0][0]) / 3600
        if len(seen) >= 2 and hours >= 0.5:
            rates[key] = (seen[-1][1] - seen[0][1]) / hours
    counts = {key: (min(c for _t, c in seen), max(c for _t, c in seen), sorted(seen)[-1][1]) for key, seen in herds.items()}
    return rates, counts


def pilots(data):
    """[(fleet row, live file)] of every ship."""
    fleet = read(Path(data) / "fleet" / "fleet.json", {})
    return [(ship, read(Path(data) / "fleet" / "ships" / dispatch.ship_file(ship.get("name") or ""), {})) for ship in fleet.get("ships") or []], fleet


def modules_of(detail):
    return [m.get("type") or m.get("type_id") for m in detail.get("modules") or [] if isinstance(m, dict)]


def show_fleet(root, data, now):
    fleet = read(Path(data) / "fleet" / "fleet.json", {})
    totals = fleet.get("totals") or {}
    windows = (totals.get("rates") or {}).get("windows") or {}
    print("FLEET | %s ships: %s at work, %s docked without work, %s adrift | credits %s (%s a ship) | read %s"
          % (totals.get("ships"), totals.get("working"), totals.get("parked"), totals.get("adrift"), num(totals.get("credits")), num(totals.get("credits_per_ship")),
             ago(fleet.get("updated_at"), now)))
    print("  steady money per hour, the rewards the game pays once per pilot left out:")
    for key in ("1h", "6h", "24h"):
        w = windows.get(key) or {}
        if w:
            print("    last %-3s (%s min measured): net %s | income %s | costs %s (fuel %s, repairs %s) | paid once, not counted: %s"
                  % (key, num(w.get("minutes")), num(w.get("cph")), num(w.get("income_per_hour")), num(w.get("costs_per_hour")), num(w.get("fuel_cr_per_hour")),
                     num(w.get("repair_cr_per_hour")), num(w.get("one_time_per_hour"))))
    once = read(Path(data) / "fleet" / "onetime.json", [])
    for label, seconds in (("1h", 3600), ("24h", 86400)):
        rows = [r[3] for r in once if isinstance(r, list) and len(r) == 4 and isinstance(r[0], (int, float)) and isinstance(r[3], (int, float)) and r[0] >= now - seconds]
        print("    money booked once, last %-3s: rewards %s in %d bookings | bought once (tools, goods for a mission) %s in %d buys"
              % (label, num(sum(v for v in rows if v > 0)), sum(1 for v in rows if v > 0), num(-sum(v for v in rows if v < 0)), sum(1 for v in rows if v < 0)))
    hour = (windows.get("1h") or {}).get("divisions") or {}
    print("  %-10s %5s %8s %8s %12s %10s %10s %10s" % ("division", "ships", "at work", "docked", "credits", "net/h", "income/h", "costs/h"))
    for name, row in sorted((totals.get("divisions") or {}).items()):
        w = hour.get(name) or {}
        print("  %-10s %5s %8s %8s %12s %10s %10s %10s" % (name, row.get("ships"), row.get("working"), row.get("parked"), num(row.get("credits")),
                                                         num(w.get("cph")), num(w.get("income_per_hour")), num(w.get("costs_per_hour"))))
    print("  why ships are docked and what would give them work: fill.py (tool fill_status)")
    return 0


def window_stats(rows, since):
    """{route: [runs, credits earned, minutes, paid once]} of the runs started since a time that read a wallet."""
    out = defaultdict(lambda: [0, 0.0, 0.0, 0])
    for row in rows:
        if epoch(row.get("started")) >= since:
            entry = out[row.get("route")]
            entry[0] += 1
            entry[3] += row.get("one_time") or 0
            if routefiles.readable(row):
                entry[1] += routefiles.earned(row) - (row.get("one_time") or 0)
                entry[2] += row.get("minutes") or 0
    return out


def show_routes(root, data, now, value, args):
    routes, rows = dispatch.load_routes(root), dispatch.run_rows(data)
    systems, home = routefiles.atlas(root)
    orders = dispatch.fresh_orders(data, now)
    hours = float(value("--hours", "4"))
    seen = window_stats(rows, now - hours * 3600)
    titles = {key: title for key, title, _text in routefiles.STAGES}
    table = []
    for rid, route in routes.items():
        group, (zone, far) = routefiles.stage(route), routefiles.zone(route, systems, home)
        if value("--group", group) != group or value("--kind", route["kind"]) != route["kind"]:
            continue
        if value("--zone", "") and (value("--zone", "") == "home") != (zone == "home space"):
            continue
        flying = sum(1 for what in orders.values() if what == route["kind"] + " " + rid) if route["kind"] != "census" else sum(
            1 for what in orders.values() if what.startswith("census ") and what.split(" ", 1)[1] in set(route.get("systems") or []))
        runs, credits, minutes, once = seen.get(rid, [0, 0.0, 0.0, 0])
        table.append((-(credits / minutes * 60 if minutes else -10 ** 9), rid, titles[group], route["kind"], zone + (" %dj" % far if far and zone != "home space" else ""),
                      flying, route.get("max_ships"), routefiles.figure(route), runs, credits, credits / minutes * 60 if minutes else None, once))
    print("ROUTES | %d listed | the last %g hours of runs beside what `routes.py measure` stored | credits are steady money: a reward paid once stands in its own column"
          % (len(table), hours))
    print("  %-38s %-18s %-7s %-20s %-9s %10s | %4s %9s %11s %9s" % ("route", "group", "kind", "zone", "ships/cap", "measured/h", "runs", "credits", "per ship-h", "paid once"))
    for _key, rid, group, kind, zone, flying, cap, figure, runs, credits, rate, once in sorted(table):
        print("  %-38s %-18s %-7s %-20s %-9s %10s | %4d %9s %11s %9s" % (rid[:38], group, kind, zone[:20], "%d/%s" % (flying, cap if cap else "-"), figure, runs,
                                                                         num(credits) if runs else "--", num(rate) if rate is not None else "--", num(once) if once else "--"))
    return 0


def show_route(root, data, now, rid):
    routes = dispatch.load_routes(root)
    route = routes.get(rid)
    if not route:
        near = sorted(r for r in routes if rid in r)[:12]
        print("no route file game/routes/%s.json%s" % (rid, ": did you mean " + ", ".join(near) if near else ""))
        return 1
    systems, home = routefiles.atlas(root)
    zone, far = routefiles.zone(route, systems, home)
    titles = {key: title for key, title, _text in routefiles.STAGES}
    orders = dispatch.fresh_orders(data, now)
    on_it = sorted(p for p, what in orders.items() if what == route["kind"] + " " + rid)
    print("ROUTE %s | %s | %s | %s%s | open to: %s" % (rid, route.get("title"), titles[routefiles.stage(route)], zone, " (%d jumps from home)" % far if far else "", routefiles.open_to(route)))
    print("  measured by `routes.py measure`: %s" % (json.dumps(route.get("measured")) if route.get("measured") else "not measured yet"))
    print("  flying it now: %s" % (", ".join(on_it) or "nobody"))
    print("  note: %s" % str(route.get("note") or "")[:600])
    rows = [r for r in dispatch.run_rows(data) if r.get("route") == rid]
    print("  runs on record: %d; the last %d:" % (len(rows), min(12, len(rows))))
    for row in rows[-12:]:
        credits = routefiles.earned(row) if routefiles.readable(row) else None
        print("    %s  %-14s %5s min  credits %8s  paid once %7s  %s" % (str(row.get("started"))[5:16], row.get("pilot"), row.get("minutes"), num(credits), num(row.get("one_time")) if row.get("one_time") else "--",
                                                                    "; ".join(str(n) for n in (row.get("notes") or [])[:3])[:120]))
    buckets = defaultdict(lambda: [0, 0.0, 0.0])
    for row in rows:
        t = epoch(row.get("started"))
        if t >= now - 24 * 3600 and routefiles.readable(row):
            b = buckets[t // 3600]
            b[0] += 1
            b[1] += routefiles.earned(row) - (row.get("one_time") or 0)
            b[2] += row.get("minutes") or 0
    if buckets:
        print("  hour by hour, the last 24 hours (UTC hour: runs, steady credits, per ship-hour):")
        print("    " + " | ".join("%s: %d, %s, %s" % (time.strftime("%H:00", time.gmtime(hour * 3600)), b[0], num(b[1]), num(b[1] / b[2] * 60) if b[2] else "--")
                                  for hour, b in sorted(buckets.items())))
    return 0


def show_history(data, now, hours):
    history = read(Path(data) / "fleet" / "history.json", [])
    marks, last = [], None
    for row in history if isinstance(history, list) else []:
        if isinstance(row, list) and len(row) >= 8 and row[0] >= now - (hours + 1) * 3600 and (last is None or row[0] - last >= 3600):
            marks.append(row)
            last = row[0]
    if history and marks and history[-1][0] != marks[-1][0]:
        marks.append(history[-1])
    names = sorted({name for row in marks for name in row[7]})
    print("HISTORY | the fleet's credits hour by hour | `steady` is the change without the rewards the game pays once per pilot")
    print("  %-11s %12s %9s %9s %7s | steady change per division: %s" % ("UTC", "credits", "change", "steady", "at work", ", ".join(names)))
    for before, row in zip(marks, marks[1:]):
        extra = row[8] if len(row) > 8 and isinstance(row[8], dict) else {}
        steady = (row[1] - before[1]) - (row[4] - before[4])
        per = []
        for name in names:
            a, b = before[7].get(name), row[7].get(name)
            per.append(num((b[1] - a[1]) - (b[3] - a[3])) if a and b else "--")
        print("  %-11s %12s %9s %9s %7s | %s" % (time.strftime("%m-%d %H:%M", time.gmtime(row[0])), num(row[1]), num(row[1] - before[1]), num(steady),
                                              (extra.get("w") or ["--"])[0], ", ".join(per)))
    if len(marks) < 2:
        print("  fewer than two hourly samples on record")
    return 0


def show_ship(data, now, name):
    detail = read(Path(data) / "fleet" / "ships" / dispatch.ship_file(name), None)
    if not isinstance(detail, dict):
        print("no ship `%s` in the fleet's files" % name)
        return 1
    order = division.order_of(name, data, now)
    print("SHIP %s | %s, commanded by %s | %s | read %s" % (name, detail.get("class") or (detail.get("ship") or {}).get("class") or "?", division.owner(name, data),
                                                         detail.get("status"), ago(detail.get("written_at") or detail.get("state_at"), now)))
    print("  at %s / %s%s | hull %s of %s | fuel %s of %s | hold %s of %s | credits %s" % (
        detail.get("system_name") or detail.get("system"), detail.get("poi_name") or detail.get("poi"), ", docked" if detail.get("docked") else ", in space",
        detail.get("hull"), detail.get("max_hull"), detail.get("fuel"), detail.get("max_fuel"), detail.get("cargo_used"), detail.get("cargo_capacity"), num(detail.get("credits"))))
    print("  order: %s | engine: %s" % (order or "none (free for the dispatcher)", json.dumps(detail.get("activity"))[:160]))
    print("  modules: %s" % (", ".join(str(m) for m in modules_of(detail)) or "none"))
    cargo = detail.get("cargo") if isinstance(detail.get("cargo"), list) else []
    print("  hold: %s" % (", ".join("%s %s" % (c.get("quantity"), c.get("item")) for c in cargo if isinstance(c, dict)) or "empty"))
    skills = detail.get("skills") if isinstance(detail.get("skills"), dict) else {}
    print("  skills: %s" % (", ".join("%s %s" % (k, v.get("level")) for k, v in sorted(skills.items(), key=lambda kv: -(kv[1].get("level") or 0))[:8]) or "none read"))
    missions = detail.get("mission_list") if isinstance(detail.get("mission_list"), list) else []
    print("  missions held: %s" % ("; ".join(str(m.get("title") or m.get("id")) for m in missions if isinstance(m, dict))[:400] or "none"))
    return 0


def show_levels(data, now, who):
    cat = read(craftbook_file(data), {})
    tables = {s.get("id"): s.get("xp_per_level") or [] for s in cat.get("skills") or []} if isinstance(cat, dict) else {}
    groups = defaultdict(list)
    for ship, detail in pilots(data)[0]:
        owner = division.owner(ship.get("name") or "", data)
        if who in ("all", owner):
            groups[ship.get("division") or owner].append(detail)

    def total(skill, entry):
        table = tables.get(skill) or []
        return sum(table[:int(entry.get("level") or 0)]) + (entry.get("xp") or 0)

    print("LEVELS | from every pilot's live file | XP an hour is the pilot's whole XP in a skill over its hours played since birth: an average, not a route's rate")
    print("  Piloting opens the hull tiers: %s" % ", ".join("level %d -> tier %d" % t for t in TIERS))
    for name, crew in sorted(groups.items()):
        skills = defaultdict(list)
        hours = []
        for detail in crew:
            played = ((detail.get("stats") or {}).get("time_played") or 0) / 3600
            hours.append(played)
            for skill, entry in (detail.get("skills") or {}).items() if isinstance(detail.get("skills"), dict) else []:
                if isinstance(entry, dict):
                    skills[skill].append((entry.get("level") or 0, total(skill, entry) / played if played > 0.2 else None, total(skill, entry)))
        if not skills:
            print("  %-10s %d ships: no skills read" % (name, len(crew)))
            continue
        pilot = skills.get("piloting") or [(0, None, 0)]
        levels = sorted(level for level, _r, _t in pilot)
        rates = [r for _l, r, _t in pilot if r]
        rate = statistics.median(rates) if rates else None
        have = statistics.median(t for _l, _r, t in pilot)
        target = next(((level, tier) for level, tier in TIERS if level > levels[len(levels) // 2]), None)
        need = sum((tables.get("piloting") or [])[:target[0]]) - have if target and tables.get("piloting") else None
        eta = "%s hours to Piloting %d (tier %d hulls) at that rate" % (num(need / rate), target[0], target[1]) if need and rate else "hours to the next tier: not measured"
        print("  %-10s %2d ships, %s hours played (median) | Piloting %d / %d / %d (lowest, median, highest), %s XP an hour | %s"
              % (name, len(crew), num(statistics.median(hours)) if hours else "--", levels[0], levels[len(levels) // 2], levels[-1], num(rate) if rate else "--", eta))
        top = sorted(((statistics.median(level for level, _r, _t in rows), skill, statistics.median([r for _l, r, _t in rows if r] or [0])) for skill, rows in skills.items()
                      if skill != "piloting"), reverse=True)[:5]
        print("             other skills, median level (XP an hour): %s" % ", ".join("%s %d (%s)" % (skill, level, num(r)) for level, skill, r in top))
    return 0


def craftbook_file(data):
    files = [p for p in (Path(data) / "catalog").glob("*.json") if p.stem[:1].isdigit()]
    return max(files, key=lambda p: p.stat().st_mtime) if files else Path(data) / "catalog" / "none.json"


def show_capacity(root, data, now):
    market, where = books(data)
    cat = read(craftbook_file(data), {})
    items = {i.get("id"): i for i in cat.get("items") or []} if isinstance(cat, dict) else {}
    crew, fleet = pilots(data)
    owned = Counter(m for _ship, detail in crew for m in set(modules_of(detail)))
    rates, herd_counts = regrowth(data)
    per_ship = HOLD * TURN                                           # about one hold an hour: a run and its way home
    print("CAPACITY | what the fleet's readings say the work carries | %s ships | one ship is taken to bring one hold (%d units) an hour" % (len(crew), HOLD))
    print("MINING | per good the stations of our books bid for: the bids, what is left in the fields we have read, the tool it takes")
    print("  %-16s %-44s %8s %7s %8s | %11s %6s %12s | %-16s %4s" % ("good", "bids (best cr; units at stations)", "ships/4h", "by bid", "by field", "left, units", "fields", "change/h", "tool", "ours"))
    goods = defaultdict(lambda: [0, 0, 0.0, 0])                      # item -> [left, fields with any, net change an hour, fields with a rate]
    for system, poi, res, left, _most, _rich, _when in fields(data):
        entry = goods[res]
        entry[0] += left or 0
        entry[1] += 1 if (left or 0) > 0 else 0
        if (system, poi, res) in rates:
            entry[2] += rates[(system, poi, res)]
            entry[3] += 1
    mining_places, table = 0, []
    for res, (left, count, change, rated) in goods.items():
        bid, depth, stations, base = demand(market, res, PAYS / HOLD)
        if not stations:
            continue
        tool = {"ice": "ice_harvester_i", "gas": "gas_harvester_i", "mining": "mining_laser_i"}.get(str((items.get(res) or {}).get("extracted_by") or "mining"),
                                                                                                    str((items.get(res) or {}).get("extracted_by")))
        by_bid, by_field = depth // per_ship, left // per_ship
        ships = int(min(by_bid, by_field, owned.get(tool, 0)))
        table.append((bid * min(depth, left), res, bid, depth, "%d: best %s" % (stations, label(base, where)), by_bid, by_field, left, count, change if rated else None,
                      tool, owned.get(tool, 0), ships))
    for _worth, res, bid, depth, base, by_bid, by_field, left, count, change, tool, ours, ships in sorted(table, reverse=True)[:14]:
        print("  %-16s %-44s %8d %7d %8d | %11s %6d %12s | %-16s %4d" % (res[:16], ("%s cr; %s at %s" % (bid, num(depth), base))[:44], ships, by_bid, by_field, num(left), count,
                                                                         ("%+d" % change) if change is not None else "not measured", tool, ours))
    best_by_tool = defaultdict(int)
    for _worth, _res, _bid, _depth, _base, by_bid, by_field, _left, _count, _change, tool, ours, ships in table:
        best_by_tool[tool] = max(best_by_tool[tool], ships)
    mining_places = sum(best_by_tool.values())                       # per tool its best good: a ship carries one hold at a time
    print("  listed: goods whose hold of %d units brings %s cr or more at the best bid. `ships/4h` is the smallest of: what the best bid takes in %d hours," % (HOLD, num(PAYS), TURN))
    print("  what the fields hold for %d hours, the ships that carry the tool. A bid is used up as we sell into it; how fast it refills is not measured." % TURN)
    print("  `change/h` is net, between the first and the last census of a field: what grew back less what anyone mined. A bid's refill is not measured.")
    for tool in ("ice_harvester_i", "gas_harvester_i"):
        offers = cheapest(market, tool, 6)
        recipes = [r.get("id") for r in (cat.get("recipes") or [] if isinstance(cat, dict) else []) if any(o.get("item_id") == tool for o in r.get("outputs") or [])]
        print("  %s: %d ships carry one | on offer: %s | %s" % (tool, owned.get(tool, 0), "; ".join("%d at %s cr (%s)" % (units, price, label(base, where)) for price, units, base in offers)
                                                             or "none in our books", "made by the recipe " + ", ".join(recipes) if recipes else "no recipe makes it"))
    book = read(Path(data) / "routes" / "opportunities.json", {})
    cands = book.get("candidates") or [] if isinstance(book, dict) else []
    routes = dispatch.load_routes(root)
    hunts = [r for r in routes.values() if r["kind"] == "hunt" and r.get("status") != "off"]
    paying = [r for r in hunts if (worth(r) or 0) > 0]
    tests = [r for r in hunts if worth(r) is None]
    known = [c for c in cands if c.get("kind") == "hunt" and isinstance(c.get("route"), dict)]
    untried = [c for c in cands if c.get("kind") == "hunt" and not isinstance(c.get("route"), dict)]
    print("HUNTING | one hunter stands at one herd (the ranching rule)")
    print("  herds with a route: %d measured above zero (median %s cr per hunter-hour), %d not measured yet, %d measured at a loss"
          % (len(paying), num(statistics.median(worth(r) for r in paying)) if paying else "--", len(tests), len(hunts) - len(paying) - len(tests)))
    print("  herds in the route maker's list: %d with known loot (estimates, %s cr per hunter-hour at the median), %d whose loot nobody has sold (one test hunt each)"
          % (len(known), num(statistics.median(c.get("per_ship_hour") or 0 for c in known)) if known else "--", len(untried)))
    shrunk = sum(1 for (_s, _p, _sp), (low, high, last) in herd_counts.items() if last < high)
    print("  herds read more than once: %d; smaller at the last census than at their largest: %d. How fast a herd grows back: not measured." % (len(herd_counts), shrunk))
    hunting_places = len(paying) + len(tests)
    once = [(c.get("pilots_open") or 0, c.get("per_run") or 0, c.get("id")) for c in cands
            if c.get("kind") == "mission" and (c.get("pilots_open") or 0) > 0 and not c.get("needs") and (c.get("per_run") or 0) > 0]      # a mission that costs more than it pays is no credit to collect
    print("ONCE | missions the game pays once per pilot, flyable now: %d, %s cr still to collect (pilots that have not flown it x reward)"
          % (len(once), num(sum(n * reward for n, reward, _i in once))))
    for n, reward, cid in sorted(once, key=lambda r: -r[0] * r[1])[:5]:
        print("    %-52s %3d pilots x %s cr" % (str(cid)[:52], n, num(reward)))
    print("SHIPS | %d in the fleet | places of repeating work that pays or is under test today: about %d (mining %d by its tightest limit, hunting %d)"
          % (len(crew), mining_places + hunting_places, mining_places, hunting_places))
    gap = len(crew) - mining_places - hunting_places
    print("  %s" % ("%d ships have no repeating paying place today: more ships would wait too. What lifts the limit is named above, per good." % gap if gap > 0
                    else "%d more ships would find a place today" % -gap))
    print("  the route maker's list is %s old; fields and herds are as old as their census (tool system)" % ("%d minutes" % ((now - epoch(book.get("written_at"))) // 60) if isinstance(book, dict) and book.get("written_at") else "not dated"))
    return 0


def show_base(root, data, now, kind):
    if kind not in FEES:
        print("name one: outpost or station")
        return 1
    part, fee = FEES[kind]
    cat = craftbook.load(data)
    if cat is None:
        print("no catalog in the data folder")
        return 1
    have, _places, when = craftbook.stock(data)
    market, where = books(data)
    makers = cat["makers"].get(part) or []
    plants = [cat["facilities"][f] for r in makers for f in r.get("produced_by_facility_ids") or [] if f in cat["facilities"]]
    chain = []
    step = plants[0] if plants else None
    while step and len(chain) < 8:
        chain.append(step)
        step = cat["facilities"].get(step.get("upgrades_from") or "")
    chain.reverse()
    print("BASE | founding %s %s in a lawless system (no empire, no police), at a place without a station, by a faction member with the right to manage bases"
          % ("an" if kind == "outpost" else "a", kind))
    print("  the founding fee: %s cr | the part: 1 %s, in the hold of the ship that founds it" % (num(fee), part))
    print("  the part is made by the recipe %s, in: %s" % (", ".join(r["id"] for r in makers) or "no recipe in the catalog", ", ".join(p["id"] for p in plants) or "no facility in the catalog"))
    wanted = Counter({part: 1})
    credits = fee
    if chain:
        print("  the facility that makes it, built step by step (each an upgrade of the one before):")
        for plant in chain:
            credits += plant.get("build_cost") or 0
            for m in plant.get("build_materials") or []:
                wanted[m.get("item_id")] += m.get("quantity") or 0
            print("    %-34s level %s  %12s cr  %s" % (plant["id"], plant.get("level"), num(plant.get("build_cost")), craftbook.parts(plant.get("build_materials"))[:150]))
    print("  credits in all, fee and facility: %s | where a production facility of ours may stand: not read yet (a station's facility commands)" % num(credits))
    offers = cheapest(market, part)
    print("  a finished %s on offer: %s" % (part, "; ".join("%d at %s cr (%s)" % (u, num(p), label(b, where)) for p, u, b in offers) or "none in our books"))
    if offers:
        print("  THE SHORT WAY: buy the part and pay the fee: %s cr in all, no facility. Seen in one order book, read %s: an offer, not a purchase made."
              % (num(offers[0][0] + fee), ago(where.get(offers[0][2], ("", ""))[1], now)))
    steps, raw = {}, {}
    for item, units in wanted.items():
        craftbook.expand(cat, item, units, steps, raw)
    print("  made on the way, for the part and the facility together (one recipe per item; the catalog tool `catalog_needs` shows the others):")
    for item, (units, runs, recipe, depth) in sorted(steps.items(), key=lambda kv: (kv[1][3], kv[0])):
        print("    %s%s %s <- %s x %s, %s" % ("  " * depth, num(units), item, recipe["id"], num(runs), craftbook.where(cat, recipe)[:110]))
    seen = defaultdict(list)
    for system, poi, res, left, _most, _rich, _when in fields(data):
        if (left or 0) > 0:
            seen[res].append((left, "%s:%s" % (system, poi)))
    print("  mined, hunted or bought, against the storage book of %s:" % when)
    print("    %-24s %10s %10s %10s  where our readings show it" % ("item", "units", "we hold", "missing"))
    missing_any = 0
    for item, units in sorted(raw.items(), key=lambda kv: -kv[1]):
        short = max(0, units - have.get(item, 0))
        missing_any += 1 if short else 0
        places = sorted(seen.get(item) or [], reverse=True)[:2]
        offers = cheapest(market, item, 2)
        source = "; ".join(["field %s (%s left)" % (place, num(left)) for left, place in places] + ["%d on offer at %s cr (%s)" % (u, p, label(b, where)) for p, u, b in offers])
        print("    %-24s %10s %10s %10s  %s" % (item, num(units), num(have.get(item, 0)), num(short), (source or "no field and no offer in our readings") if short else "held"))
    print("  %d of %d inputs are short. A step that runs only in a facility needs that facility first: the list above names it." % (missing_any, len(raw)))
    return 0


def show_system(root, data, now, sid):
    systems, home = routefiles.atlas(root)
    if sid not in systems:
        near = sorted(s for s in systems if sid in s)[:12]
        print("no system `%s` on the chart%s" % (sid, ": did you mean " + ", ".join(near) if near else ""))
        return 1
    empire, jumps = systems[sid]
    print("SYSTEM %s | %s | %s jumps from home" % (sid, "our empire" if empire == home else ("lawless" if empire in ("-", "") else "empire " + empire), jumps if jumps is not None else "?"))
    scan = read(Path(data) / "scouting" / (sid + ".json"), None)
    wild = read(Path(data) / "wildlife" / (sid + ".json"), {})
    if not isinstance(scan, dict):
        print("  never read by a census of ours")
    else:
        info = scan.get("system") if isinstance(scan.get("system"), dict) else {}
        print("  census read %s | police level %s | %s" % (ago(scan.get("read_at"), now), info.get("police_level", "?"), str(info.get("description") or "")[:200]))
        for poi, entry in (scan.get("pois") or {}).items():
            inner = entry.get("poi") if isinstance(entry.get("poi"), dict) else {}
            left = ", ".join("%s %s of %s" % (r.get("resource_id"), num(r.get("remaining")), num(r.get("max_remaining"))) for r in entry.get("resources") or [] if isinstance(r, dict))
            herd = Counter(c.get("species") for c in ((wild.get("pois") or {}).get(poi) or {}).get("creatures") or [] if isinstance(c, dict))
            print("    %-34s %-14s %s%s" % (poi[:34], inner.get("type") or "?", left or "no deposit read", (" | creatures: " + ", ".join("%d %s" % (n, s) for s, n in herd.most_common(6))) if herd else ""))
    market, where = books(data)
    for base, (system, when) in sorted(where.items()):
        if system == sid:
            rows = market[base]
            print("  market %s, read %s: %d goods, %d with a bid, %d on offer" % (base, ago(when, now), len(rows), sum(1 for r in rows.values() if (r.get("best_buy") or 0) > 0),
                                                                          sum(1 for r in rows.values() if (r.get("best_sell") or 0) > 0)))
    met = read(Path(data) / "intel" / "met.json", {})
    met = met.get("pilots") if isinstance(met, dict) and isinstance(met.get("pilots"), dict) else met
    tags = Counter((e.get("faction_tag") or "no faction") for e in met.values() if isinstance(e, dict) and e.get("system") == sid) if isinstance(met, dict) else Counter()
    print("  pilots of others our ships met here: %s" % (", ".join("%d %s" % (n, tag) for tag, n in tags.most_common(8)) or "none on record"))
    crew, _fleet = pilots(data)
    ours = Counter(ship.get("division") for ship, _detail in crew if ship.get("system") == sid)
    print("  our ships here now: %s" % (", ".join("%d %s" % (n, name) for name, n in ours.most_common()) or "none"))
    flown = sorted(rid for rid, route in dispatch.load_routes(root).items() if sid in routefiles.systems_of(route))
    print("  routes that touch it: %s" % (", ".join(flown) or "none"))
    return 0


def git_lines(folder, *args):
    try:
        done = subprocess.run(["git", "-C", str(folder)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=20)
        return done.stdout.splitlines() if done.returncode == 0 else []
    except (OSError, subprocess.SubprocessError):
        return []


def show_learnings(root, data, now, hours, profiles=PROFILES):
    repo = Path(root).parent
    print("LEARNINGS | per member: its newest report, and what it wrote into its own knowledge in the last %g hours (the git history of its workspace)" % hours)
    for name in division.MEMBERS:
        low = name.lower()
        work = Path(profiles) / low / ("workspace-" + low)
        newest = None
        for path in sorted((repo / "reports").glob("*_%s_*.md" % low)):
            stamp = git_lines(repo, "log", "-1", "--format=%ct", "--", str(path.relative_to(repo)))
            at = int(stamp[0]) if stamp and stamp[0].isdigit() else 0
            newest = max(newest or (0, path), (at, path))
        print("%s" % name)
        if newest:
            title = next((line[2:].strip() for line in newest[1].read_text(encoding="ascii", errors="replace").splitlines() if line.startswith("# ")), newest[1].stem)
            print("  newest report (%s): reports/%s" % (time.strftime("%m-%d %H:%M UTC", time.gmtime(newest[0])) if newest[0] else "not committed", newest[1].name))
            print("    %s" % title[:200])
        else:
            print("  no report yet")
        if not work.is_dir():
            print("  workspace not found: %s" % work)
            continue
        changed = {}
        for line in git_lines(work, "log", "--since=%d seconds ago" % int(hours * 3600), "--name-status", "--format=", "--", "knowledge", "LEARNINGS.md"):
            cells = line.split("\t")
            if len(cells) >= 2:
                changed.setdefault(cells[-1], set()).add("new" if cells[0].startswith("A") else "changed")
        files = sorted((work / "knowledge").glob("*.md")) if (work / "knowledge").is_dir() else []
        files = [f for f in files if f.name != "knowledge-guide.md"]
        print("  knowledge files: %d%s" % (len(files), "" if files else " (none written yet)"))
        for path in files:
            rel = "knowledge/" + path.name
            mark = "NEW" if "new" in changed.get(rel, ()) else ("CHANGED" if rel in changed else "")
            text = path.read_text(encoding="ascii", errors="replace").splitlines()
            title = next((line[2:].strip() for line in text if line.startswith("# ")), path.stem)
            print("    %-8s %-36s %4d lines  %s" % (mark, path.name[:36], len(text), title[:110]))
        book = work / "LEARNINGS.md"
        if book.is_file():
            text = book.read_text(encoding="ascii", errors="replace").splitlines()
            last = git_lines(work, "log", "-1", "--format=%cd %s", "--date=format:%m-%d %H:%M", "--", "LEARNINGS.md")
            print("    %-8s LEARNINGS.md: %d lines, %d headings; last commit: %s" % ("CHANGED" if "LEARNINGS.md" in changed else "", len(text),
                                                                                 sum(1 for line in text if line.startswith("#")), (last[0] if last else "none")[:120]))
    return 0


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data", "--group", "--kind", "--zone", "--hours"))]
    if not words or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    now, verb, rest = time.time(), words[0], words[1:]
    if verb == "fleet":
        return show_fleet(root, data, now)
    if verb == "routes":
        return show_routes(root, data, now, value, args)
    if verb == "route" and rest:
        return show_route(root, data, now, rest[0])
    if verb == "history":
        return show_history(data, now, float(value("--hours", "12")))
    if verb == "ship" and rest:
        return show_ship(data, now, " ".join(rest))
    if verb == "levels":
        _kind, me = division.member()
        return show_levels(data, now, rest[0] if rest else (me if me in division.MEMBERS and me != "Unity" else "all"))
    if verb == "capacity":
        return show_capacity(root, data, now)
    if verb == "base" and rest:
        return show_base(root, data, now, rest[0])
    if verb == "system" and rest:
        return show_system(root, data, now, rest[0])
    if verb == "learnings":
        return show_learnings(root, data, now, float(value("--hours", "8")))
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
