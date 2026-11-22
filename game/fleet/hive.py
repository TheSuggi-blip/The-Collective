#!/usr/bin/env python3
"""hive.py -- the fleet's figures from its own readings: money, routes and their history, levels, what the work carries, what a base takes, a system.

WHAT: reads the unit's data folder (fleet/, routes/runs.jsonl, market/, scouting/, wildlife/, stock/, catalog/, intel/) and
      the route files, and prints one answer:
        fleet                 credits, the faction's treasury and the fleet's money (wallets + treasury), steady money per
                              hour (rewards paid once left out) over 1, 6 and 24 hours, per division
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
        standing              the standing fleet of a member: its plan route by route with the credits per ship-hour of each
                              and the ships each carries (what its bid, field or herd regains; fill.py `carries`),
                              and every ship on one line: what it flies now, what it earned per hour in the last hours,
                              and what closes the best route to it when it waits
        tasks                 one unit for all work: credits per ship-hour by kind of work (mining, hunting, trade, ...)
                              and by division with the idle ships counted, beside the best route as the scale
        forecast              the hours ahead, per division: every route with the ships on it now, what a ship-hour on
                              it measured and what that makes per hour and per turn, per ship of the division and
                              for the fleet; what is paid once stands apart
        refill                what comes back by itself between our readings, per hour: the units a bid regains, what a
                              field grows back, the animals of a herd
        docs                  the fleet's written knowledge by section, from the store (docs.py mirrors the repository
                              every minute and keeps every version): the rulebook rule by rule, the orders in force block
                              by block, strategy, empire, guidebooks, templates, the game's rules, the metrics, and the
                              members' writing (plans, reports, every log entry, their own files); the files, a file's
                              sections by title, one section whole (--section; its versions, each against the one before:
                              --history), the sections that hold a word (--grep)
        changes               the sections whose text changed since a time (default: the member's last turn, its newest
                              entry in communications/reports.log) and those that left their file; the briefing lists
                              them too (CHANGED SINCE YOUR LAST TURN)
        division <name|all>   what each Admiral is doing, from the store alone (docs_division.py): its mission, its block
                              of the orders in force, its plan, its guidebook's sections, its last session entry, the
                              requests open to and from it, its claims in force; one short block a division
        guide <division|all>  a division's guidebook from the store (guidebook.py; its chapters game/routes/guidebook/
                              <division>/, command the Fleet Admiral's): its class card whole, the index of its chapters
                              (entries with status, updated, size, over cap) and the class's computed figures (stats.py);
                              --chapter one chapter whole, --grep the entries that hold a word, --retired the entries
                              retired or gone from their chapter, kept in the store
        briefing              a session's start in one answer: the orders in force, the requests addressed to the member
                              (and how many of them are stale: untouched for more than 3 days, comms.py), the fleet's
                              money, its own standing fleet (plan, what each route carries, every ship), its plan file
                              in short (plan.py) and the fill gate; above it all one line while a base of ours
                              reads wrecked or a facility of ours damaged or offline (basewatch.py)
        store                 the history store (store.py): what it holds, and every route's credits per ship-hour over
                              the whole hours of a window, also beyond what the records still hold
        store price <item>    one item's lowest and highest best bid and best ask per station over a window
        empire                what we hold: the faction with its members and limit, our bases, our offices at other
                              stations and their rent, the sites proposed for a base, the next steps of the member
                              limit (empire.py show; the file: governance/empire.md)
        surplus, reserve      what we hold beyond what our bases and upgrades take, where it lies and its best bid
                              (surplus: what the fleet may sell); what the reserve's targets (the open needs of game/needs.tsv) take against
                              what we hold, and what is short (reserve). Both are surplus.py's answers
        inventory             what the fleet owns in goods: every item in station storage and in the holds added up, by
                              kind of item (raw, refined, parts, modules ...); `inventory stations` lists it per station
                              (the craft book's own count: craftbook.py inventory)
        supply                the supply chains (game/supply/chains.tsv): the goods the fleet must never run out of, each
                              against what stands at its place now, with the ships on its routes: show, check (the
                              gate) or duty (the plan change for a short chain, a dry run here); supply.py's answers
        needs                 the needs register (game/needs.tsv, needs.py): the open needs, highest priority first, with
                              their covered percent, colour and what is short (list), one need or project (show), per
                              item (items), the gate (check); it only reads: a need is written by needs.py or the tool needs
        rival                 benchmark vs #1 [HEXC], unclaimed resource-monopoly outpost sites, docked crafting spreads & hull targets
        contracts             bottleneck procurement candidates, rival board contracts & communications/contracts.log
        flow                  what each division put into the reserve per hour: of every item the reserve asks for
                              (surplus.py reserve), the units it holds (storage and holds) and their change per hour over
                              the last 4, 12 and 24 hours, from the store's hourly samples (store.py, stock_hour); the
                              yield of a division that stores what the bases take instead of selling it
        sql "<statement>"     one SELECT or WITH statement on the store's read copy (store.py query: read only, one statement,
                              a time stop), its rows as an aligned table with the column names, values as they are
        schema [<table>]      every table and view of the store with what a row is and its columns; with a table's name its
                              columns and three example questions as SQL
        handbook [<topic>]    the store's handbook, written from the code (scripts/handbook.py; docs_handbook.py reads
                              it): how the data flows, where to ask what, every table and view with its columns,
                              how long its rows are kept, how often refreshed, its examples; a topic: a table's name,
                              a subject or a word; without one the contents and how the data flows
        stats <view>          the fleet's statistics the store computes by itself (stats.py; definitions: game/metrics.md):
                              kpi, contribution, classes, time, supply, gather, xp, upgrades, alerts, refill, status
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
  hive.py gauges ship <pilot>... | side <pilot>... | species [--role <role>]
  hive.py levels [<Member>|all]
  hive.py capacity
  hive.py base outpost|station
  hive.py system <system id>
  hive.py learnings [--hours N]
  hive.py standing [<Member>|<role>|all] [--hours N]
  hive.py tasks [--hours N]
  hive.py forecast [<Member>|all] [--hours N]
  hive.py refill
  hive.py docs [<path|kind|owner>] [--section <id> [--history]] [--grep <word>]
  hive.py changes [--since <ISO time>|<N>h] [--member <name>]
  hive.py division [<Member>|<division>|all]
  hive.py guide [<division>|<Member>|all] [--chapter <name>] [--grep <word>] [--retired]
  hive.py briefing [<Member>|all] [--hours N]
  hive.py store [--hours N]
  hive.py store price <item id> [--hours N]
  hive.py inventory [stations] [--item <item id>] [--top N]
  hive.py empire
  hive.py surplus [--top N] [--kind <kind>] [--item <item id>] [--all]
  hive.py reserve
  hive.py supply [show|check|duty]
  hive.py needs [list [<division>] [--project <text>] [--all] | show <id>|<project> | items | check]
  hive.py flow [<Member>|all] [--hours N]
  hive.py sql "<SELECT or WITH statement>" [--limit N]
  hive.py schema [<table or view>]
  hive.py handbook [<table or view>|<subject>|<word>]
  hive.py watchdog [--hours N] [--json]
  hive.py stats <view> [--hours N] [--member <Member>]
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
import board                                      # noqa: E402  the divisions' names
import craftbook                                  # noqa: E402  the catalog: what a thing takes
import dispatch                                   # noqa: E402  routes, orders, runs
import division                                   # noqa: E402  who commands which ship
import empire as holdings                         # noqa: E402  the faction, our bases and offices
import routes as routefiles                       # noqa: E402  a route's group and zone, what a run earned
import store as history                           # noqa: E402  the history store's read copy
import surplus as spare                           # noqa: E402  the reserve and what we hold beyond it

HOLD = 65                      # a starter's hold, units
TURN = 4                       # hours: what a bid or a field must carry
PAYS = 1000                    # credits a hold must bring at the best bid before a good counts as paying work
PROFILES = "/opt/data/profiles"                  # each member's workspace: <PROFILES>/<name>/workspace-<name>
FEES = {"outpost": ("outpost_kit", 100000), "station": ("station_core", 5000000)}      # the founding fee: the game's faction guide, read 2026-11-15
TIERS = ((10, 2), (20, 3), (30, 4), (50, 5))                                           # Piloting level -> hull tier (game/catalog/master-index.md)
SQL_ROWS = 200                 # rows `sql` prints unless --limit says more
SQL_CELL = 120                 # characters of one cell `sql` prints; a longer text is cut and the cut is said


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
    print(treasury_line(data, totals.get("credits"), now))
    away = [a for a in fleet.get("away") or [] if isinstance(a, dict)]
    if away:                                                          # station/fleet.py rejoin: signed in again within minutes
        print("  AWAY | %d pilot(s) the engine holds signed out, not in the count above; the collector signs them in again by itself: %s"
              % (len(away), ", ".join("%d of %s" % (n, d) for d, n in sorted(Counter(str(a.get("division")) for a in away).items()))))
    print("  steady money per hour, the rewards the game pays once per pilot left out; costs are money out (net = income - costs):")
    for key in ("1h", "6h", "24h"):
        w = windows.get(key) or {}
        if w:
            print("    last %-3s (%s min measured): net %s | income %s | costs %s (metered: fuel %s + repairs %s = %s%s) | paid once, not counted: %s"
                  % (key, num(w.get("minutes")), num(w.get("cph")), num(w.get("income_per_hour")), num(w.get("costs_per_hour")), num(w.get("fuel_cr_per_hour")),
                     num(w.get("repair_cr_per_hour")), num(w.get("metered_per_hour")),
                     "; the game's counter of credits spent %s" % num(w["spent_per_hour"]) if "spent_per_hour" in w else "", num(w.get("one_time_per_hour"))))
            seed, left = w.get("seed") or {}, []
            if w.get("transfers_moved_per_hour"):                     # station/fleet.py: gifts between our ships are neither income nor costs
                left.append("gifts between our ships, %s an hour (%s of them name one side only and move no division)"
                            % (num(w.get("transfers_moved_per_hour")), num(w.get("transfers_unpaired_per_hour"))))
            if w.get("treasury_moved_per_hour"):                      # station/fleet.py: a deposit moves money between two purses of ours
                left.append("deposits into the faction's treasury, %s an hour (a move between two purses of ours, no cost)" % num(w.get("treasury_moved_per_hour")))
            if w.get("gifts_unseen"):                                 # station/fleet.py matching: each side counts when its wallet was read
                left.append("held out: %s cr of gifts not yet seen by their receivers" % num(w.get("gifts_unseen")))
            if w.get("gifts_early"):
                left.append("held out: %s cr of gifts their receivers showed in this window, given before it" % num(w.get("gifts_early")))
            if seed.get("pilots"):
                left.append("the first wallets of %s new pilots, %s cr" % (seed.get("pilots"), num(seed.get("credits"))))
            gone = w.get("presence") or {}
            if gone.get("left") or gone.get("back"):                  # station/fleet.py: a ship off the engine's list is no loss
                left.append("%s ships the engine stopped listing and %s it lists again, with their wallets (%s cr)"
                            % (gone.get("left") or 0, gone.get("back") or 0, num(gone.get("credits"))))
            if left:
                print("      left out: " + "; ".join(left))
    once = read(Path(data) / "fleet" / "onetime.json", [])
    for label, seconds in (("1h", 3600), ("24h", 86400)):
        near = [r for r in once if isinstance(r, list) and len(r) == 4 and isinstance(r[0], (int, float)) and isinstance(r[3], (int, float)) and r[0] >= now - seconds
                and r[2] != "Wallet top-up"]                    # wallet.py TITLE: half of a gift between our ships, no reward and no buy
        kept = [-r[3] for r in near if str(r[2]).startswith(routefiles.TREASURY)]       # a deposit into the treasury: no buy either
        near = [r for r in near if not str(r[2]).startswith(routefiles.TREASURY)]
        rows, tax = [r[3] for r in near if r[2] != "Weekly tax"], [-r[3] for r in near if r[2] == "Weekly tax"]
        print("    money booked once, last %-3s: rewards %s in %d bookings | bought once (tools, goods for a mission) %s in %d buys%s%s"
              % (label, num(sum(v for v in rows if v > 0)), sum(1 for v in rows if v > 0), num(-sum(v for v in rows if v < 0)), sum(1 for v in rows if v < 0),
                 " | weekly tax %s from %d pilots (once a week; kept out of the steady money)" % (num(sum(tax)), len(tax)) if tax else "",
                 " | into the faction's treasury %s in %d deposits (a move between two purses of ours)" % (num(sum(kept)), len(kept)) if kept else ""))
    hour = (windows.get("1h") or {}).get("divisions") or {}
    print("  %-10s %5s %8s %8s %12s %10s %10s %10s %10s %10s" % ("division", "ships", "at work", "docked", "credits", "net/h", "income/h", "costs/h", "metered/h", "gifts/h"))
    for name, row in sorted((totals.get("divisions") or {}).items()):
        w = hour.get(name) or {}
        print("  %-10s %5s %8s %8s %12s %10s %10s %10s %10s %10s" % (name, row.get("ships"), row.get("working"), row.get("parked"), num(row.get("credits")),
                                                                   num(w.get("cph")), num(w.get("income_per_hour")), num(w.get("costs_per_hour")),
                                                                   num(w.get("metered_per_hour")), num(w.get("transfers_per_hour"))))
    print("  the last hour; metered/h: fuel and repairs the collector saw bought; gifts/h: what our own gifts put into the division (+) or took out (-),"
          " left out of its income and costs")
    print("  why ships are docked and what would give them work: fill.py (tool fill_status)")
    return 0


def treasury_line(data, wallets, now):
    """The faction's treasury beside the wallets (empire.py collect: data/empire/empire.json faction.treasury and its time),
    and the fleet's money: wallets + treasury (Suggi, 2026-11-17: the treasury is the fleet's main purse)."""
    state = read(Path(data) / "empire" / "empire.json", {})
    faction = state.get("faction") if isinstance(state, dict) and isinstance(state.get("faction"), dict) else {}
    money = faction.get("treasury")
    if not isinstance(money, (int, float)) or isinstance(money, bool):
        return "  TREASURY | not measured (no reading in %s: `empire.py collect` writes it) | fleet money = wallets %s + treasury not measured" % (
            Path(data) / "empire" / "empire.json", num(wallets))
    total = num(wallets + money) if isinstance(wallets, (int, float)) else "not measured"
    return "  TREASURY | the faction's treasury %s cr (read %s by empire.py collect) | fleet money = wallets %s + treasury %s = %s cr" % (
        num(money), ago(state.get("written_at"), now), num(wallets), num(money), total)


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
    """The newest catalog/<version>.json: the highest version in the file name, craftbook.load's rule; a file not named
    by digits and dots (ammo.json, refresh.json) is no catalog. By version, not by file time (2026-11-16): a copy
    written later is not a newer catalog."""
    import re                                      # only this function of hive.py matches a name
    files = [p for p in (Path(data) / "catalog").glob("*.json") if re.fullmatch(r"\d+(\.\d+)*", p.stem)]
    return max(files, key=lambda p: tuple(int(n) for n in p.stem.split("."))) if files else Path(data) / "catalog" / "none.json"


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
    craftbook.choose(cat, str(Path(root).parent))                    # the recipes the fleet chose: game/reserve-recipes.tsv of this repository
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
    craftbook.print_taken(cat, {item: step[2] for item, step in steps.items()}, "  ")
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
    held = read(Path(data) / "empire" / "empire.json", {})                  # what the faction owns, as empire.py collect read it from the game
    held = held if isinstance(held, dict) else {}
    built = ["%s %s" % (b.get("kind") or "base", b.get("name") or "?") for b in held.get("bases") or [] if isinstance(b, dict) and b.get("system") == sid]
    built += ["%s tier %s at %s (%s)" % (f.get("name") or f.get("type") or "office", f.get("level") or 1, f.get("base") or "?", f.get("status") or "?")
              for f in held.get("facilities") or [] if isinstance(f, dict) and f.get("system") == sid]
    plans = ["%s%s" % (x.get("status") or "candidate", (", proposed by " + x["proposed_by"]) if x.get("proposed_by") else "")
             for x in held.get("sites") or [] if isinstance(x, dict) and x.get("system") == sid]
    print("  ours here: %s%s" % (", ".join(built) or "nothing built", (" | a site of ours: " + "; ".join(plans)) if plans else ""))
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


def moves(seen):
    """(added, taken, hours) of a series [(time, value)]: the sum of the rises and of the falls between two readings, and its span."""
    seen = sorted(seen)
    pairs = list(zip(seen, seen[1:]))
    return (sum(max(0, b[1] - a[1]) for a, b in pairs), sum(max(0, a[1] - b[1]) for a, b in pairs),
            (seen[-1][0] - seen[0][0]) / 3600 if len(seen) > 1 else 0.0)


def bid_moves(seen):
    """(added, taken) units at the best bid over a series [(time, units, bid)]: the least that is sure. A rise at the same
    price is a refill. A higher price with less than half the units is a new small bid on top: its units were added;
    when the price falls again that small bid was used up. Every other change of price is left out: a deep bid whose
    price creeps is the same demand, and a lower price is the next step of the ladder coming into view."""
    added = taken = 0
    for (_t0, u0, b0), (_t1, u1, b1) in zip(seen, seen[1:]):
        if b1 == b0:
            added, taken = added + max(0, u1 - u0), taken + max(0, u0 - u1)
        elif b1 > b0 and u1 * 2 < u0:
            added += u1
        elif b1 < b0 and u0 * 2 < u1:
            taken += u0
    return added, taken


def json_lines(path):
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict):
                    yield row
    except OSError:
        return


def series(data):
    """The readings over time: ({(base, item): [(time, bid units, bid)]}, {(system, place, resource): [(time, units)]},
    {(system, place, species): [(time, animals)]}) from market/history.jsonl and wildlife/history.jsonl. A herd that a
    reading of its place no longer lists stands at 0 in that reading."""
    bids, deposits, herds = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in json_lines(Path(data) / "market" / "history.jsonl"):
        if row.get("base") and row.get("item") and isinstance(row.get("bid_qty"), (int, float)):
            bids[(row["base"], row["item"])].append((epoch(row.get("t")), row["bid_qty"], row.get("bid") or 0))
    known = defaultdict(set)
    for row in json_lines(Path(data) / "wildlife" / "history.jsonl"):
        at, system = epoch(row.get("at")), row.get("system")
        found = {poi: entry for poi, entry in (row.get("herds") or {}).items() if isinstance(entry, dict)}
        for poi, entry in (row.get("deposits") or {}).items():
            for res, units in (entry or {}).items() if isinstance(entry, dict) else []:
                if isinstance(units, (int, float)):
                    deposits[(system, poi, res)].append((at, units))
        for poi in set(row.get("deposits") or {}) | set(row.get("pilots") or {}) | set(found):
            here = {s: c for s, c in (found.get(poi) or {}).items() if isinstance(c, (int, float))}
            known[(system, poi)] |= set(here)
            for species in known[(system, poi)]:
                herds[(system, poi, species)].append((at, here.get(species, 0)))
    return bids, deposits, herds


def rates(data):
    """What comes back per hour, as the least our readings prove: ({(base, item): (units a bid regained at its best
    price, units taken, hours watched)}, {(system, place, resource): (units a field grew back, taken, hours)},
    {(system, place, species): (animals that came back, killed or left, hours)}). Only what was read twice or more,
    half an hour apart or more. The same arithmetic as the tables of `refill`: bid_moves and moves."""
    bids, deposits, herds = series(data)
    read_at = {base: epoch((entry or {}).get("read_at")) for base, entry in (read(Path(data) / "market" / "history.state.json", {}) or {}).items()
               if isinstance(entry, dict)}
    out = ({}, {}, {})
    for (base, item), seen in bids.items():
        seen.sort()
        added, taken = bid_moves(seen)
        hours = (max(read_at.get(base, 0), seen[-1][0]) - seen[0][0]) / 3600     # the span runs to the last reading of the book
        if hours >= 0.5:
            out[0][(base, item)] = (added / hours, taken / hours, hours)
    for index, table in ((1, deposits), (2, herds)):
        for key, seen in table.items():
            added, taken, hours = moves(seen)
            if hours >= 0.5:
                out[index][key] = (added / hours, taken / hours, hours)
    return out


def show_refill(root, data, now):
    bids, deposits, herds = series(data)
    read_at = {base: epoch((entry or {}).get("read_at")) for base, entry in (read(Path(data) / "market" / "history.state.json", {}) or {}).items()
               if isinstance(entry, dict)}
    _market, where = books(data)
    print("REFILL | what comes back by itself, per hour, from our own readings | a rise between two readings is the least that came back: "
          "what was sold, mined or killed in between hides the rest | a place read twice or more, half an hour apart or more")
    table = []
    for (base, item), seen in bids.items():
        seen.sort()
        added, taken = bid_moves(seen)
        hours = (max(read_at.get(base, 0), seen[-1][0]) - seen[0][0]) / 3600     # a move is written when a value changed: the span runs to the last reading of the book
        bid = next((b for _t, _u, b in reversed(seen) if b), 0)
        if hours >= 0.5 and added > 0 and bid > 0:
            table.append((-(added / hours * bid), label(base, where), item, bid, seen[-1][1], max(u for _t, u, _b in seen), len(seen), hours, added / hours, taken / hours))
    print("BIDS that regained units at their best price: %d of %d watched | sorted by the credits an hour the regained units are worth at the bid | "
          "the steps below the best price are not in the record yet" % (len(table), len(bids)))
    print("  %-30s %-26s %7s %9s %9s %6s %6s %12s %12s %11s" % ("station", "item", "bid", "units now", "most seen", "moves", "hours", "regained/h", "worth cr/h", "taken/h"))
    for worth_h, base, item, bid, units, most, n, hours, added, taken in sorted(table)[:25]:
        print("  %-30s %-26s %7s %9s %9s %6d %6.1f %12s %12s %11s" % (base[:30], item[:26], num(bid), num(units), num(most), n, hours, num(added), num(-worth_h), num(taken)))
    if not table:
        print("  not measured: no bid was seen to rise between two readings")
    table = []
    for (system, poi, res), seen in deposits.items():
        added, taken, hours = moves(seen)
        if hours >= 0.5:
            table.append((-added / hours, system, poi, res, sorted(seen)[-1][1], len(seen), hours, added / hours, taken / hours))
    print("FIELDS read twice or more: %d | sorted by what grew back" % len(table))
    print("  %-14s %-30s %-16s %10s %8s %6s %12s %11s" % ("system", "place", "resource", "units now", "readings", "hours", "grew back/h", "taken/h"))
    for _key, system, poi, res, units, n, hours, added, taken in sorted(table)[:20]:
        print("  %-14s %-30s %-16s %10s %8d %6.1f %12s %11s" % (str(system)[:14], poi[:30], res[:16], num(units), n, hours, num(added), num(taken)))
    if not table:
        print("  not measured: no field was read twice half an hour apart")
    table = []
    for (system, poi, species), seen in herds.items():
        added, taken, hours = moves(seen)
        if hours >= 0.5:
            counts = [c for _t, c in seen]
            table.append((-added / hours, system, poi, species, sorted(seen)[-1][1], min(counts), max(counts), len(seen), hours, added / hours, taken / hours))
    print("HERDS read twice or more: %d | sorted by the animals that came back" % len(table))
    print("  %-14s %-30s %-16s %4s %7s %5s %8s %6s %12s %14s" % ("system", "place", "species", "now", "fewest", "most", "readings", "hours", "came back/h", "killed, left/h"))
    for _key, system, poi, species, last, low, high, n, hours, added, taken in sorted(table)[:25]:
        print("  %-14s %-30s %-16s %4d %7d %5d %8d %6.1f %12.1f %14.1f" % (str(system)[:14], poi[:30], species[:16], last, low, high, n, hours, added, taken))
    if not table:
        print("  not measured: no herd was read twice half an hour apart")
    return 0


def pilot_stats(rows, since):
    """{pilot or route: [runs, steady credits, minutes that read a wallet, paid once, minutes flown]} of the runs started since a time."""
    by_pilot, by_route = defaultdict(lambda: [0, 0.0, 0.0, 0, 0.0]), defaultdict(lambda: [0, 0.0, 0.0, 0, 0.0])
    for row in rows:
        if epoch(row.get("started")) >= since:
            for entry in (by_pilot[row.get("pilot")], by_route[row.get("route")]):
                entry[0] += 1
                entry[3] += row.get("one_time") or 0
                entry[4] += row.get("minutes") or 0
                if routefiles.readable(row):
                    entry[1] += routefiles.earned(row) - (row.get("one_time") or 0)
                    entry[2] += row.get("minutes") or 0
    return by_pilot, by_route


def per_hour(credits, minutes):
    return num(credits / minutes * 60) if minutes else "--"


def work_of(route):
    """The kind of work a route is, for one table of all work."""
    if not route:
        return "route file gone"
    if routefiles.stage(route) == "fit":
        return "fitting (tools, bought once)"
    if route.get("once"):
        return "missions that pay once"
    if routefiles.standing(route):
        return "standing work (trains, gathers)"
    return {"mine": "mining", "hunt": "hunting", "census": "census (reads, no pay)", "circuit": "trade and delivery"}.get(route.get("kind"), str(route.get("kind") or "?"))


def scale(routes, by_route):
    """[(credits per ship-hour, route id, runs)], best first: the routes that repeat and are judged on their pay (no
    mission paid once, no fitting, no census, no park), with two runs or more. A fitting sells the hold it came with:
    fit-ice-harvester read 88,356 credits per ship-hour as the fleet's best route on 2026-11-16."""
    return sorted(((credits / minutes * 60, rid, runs) for rid, (runs, credits, minutes, _o, _f) in by_route.items()
                   if runs >= 2 and minutes and rid in routes and not routes[rid].get("once") and dispatch.judged(routes[rid])
                   and not (routes[rid].get("requires") or {}).get("stored")), reverse=True)        # a route that sells a stored load is paid for work done earlier


def show_tasks(root, data, now, hours):
    routes, rows = dispatch.load_routes(root), dispatch.run_rows(data)
    by_pilot, by_route = pilot_stats(rows, now - hours * 3600)
    kinds = defaultdict(lambda: [0, 0, 0.0, 0.0, 0, 0.0])            # routes, runs, credits, read minutes, paid once, minutes flown
    for rid, (runs, credits, minutes, once, flown) in by_route.items():
        entry = kinds[work_of(routes.get(rid))]
        entry[0] += 1
        for index, value in ((1, runs), (2, credits), (3, minutes), (4, once), (5, flown)):
            entry[index] += value
    print("TASKS | the last %g hours of runs | one unit for all work: credits per ship-hour | steady money: a reward the game pays once stands in its own column" % hours)
    print("  %-30s %6s %5s %12s %11s %13s %10s %19s" % ("kind of work", "routes", "runs", "ship-h flown", "credits", "per ship-hour", "paid once", "per ship-h with it"))
    for name, (count, runs, credits, minutes, once, flown) in sorted(kinds.items(), key=lambda kv: -(kv[1][2] / kv[1][3] if kv[1][3] else -10 ** 9)):
        print("  %-30s %6d %5d %12.1f %11s %13s %10s %19s" % (name, count, runs, flown / 60, num(credits), per_hour(credits, minutes), num(once) if once else "--",
                                                          per_hour(credits + once, minutes)))
    print("  a mission that pays once buys its goods from the steady money and is paid in the last column: judge it there; it cannot be flown twice")
    crew, _fleet = pilots(data)
    ships = Counter(division.owner(ship.get("name") or "", data) for ship, _detail in crew)
    owners = defaultdict(lambda: [0, 0.0, 0.0, 0, 0.0])
    for pilot, values in by_pilot.items():
        entry = owners[division.owner(pilot or "", data)]
        for index, value in enumerate(values):
            entry[index] += value
    print("  by division, from the runs of these %g hours (the wallets' own figure per division is `hive.py fleet`): income per hour is the runs' steady credits over the hours" % hours)
    print("  %-10s %5s %12s %6s %12s %13s %17s" % ("division", "ships", "ship-h flown", "busy", "income/h", "paid once/h", "per ship-h flown"))
    total = [0, 0.0, 0.0, 0, 0.0]
    for member in division.MEMBERS:
        runs, credits, minutes, once, flown = owners.get(member, [0, 0.0, 0.0, 0, 0.0])
        clock = ships.get(member, 0) * hours
        total = [a + b for a, b in zip(total, (runs, credits, minutes, once, flown))]
        print("  %-10s %5d %12.1f %5.0f%% %12s %13s %17s" % (member, ships.get(member, 0), flown / 60, 100 * flown / 60 / clock if clock else 0, num(credits / hours),
                                                            num(once / hours) if once else "--", per_hour(credits, minutes)))
    clock = sum(ships.values()) * hours
    print("  %-10s %5d %12.1f %5.0f%% %12s %13s %17s" % ("FLEET", sum(ships.values()), total[4] / 60, 100 * total[4] / 60 / clock if clock else 0, num(total[1] / hours),
                                                        num(total[3] / hours) if total[3] else "--", per_hour(total[1], total[2])))
    best = scale(routes, by_route)
    if best:
        print("  THE SCALE | best repeating route with two runs or more: %s at %s credits per ship-hour | a ship without work earns 0 | every figure above reads against these two"
              % (best[0][1], num(best[0][0])))
    return 0


def rate_of(route, rid, by_route, cands):
    """(credits per ship-hour, what the figure rests on) of a route that repeats: the runs of the window when two or
    more of them read a wallet, else what all its runs measured (the route file), else the route maker's estimate;
    (None, `not measured`) when nothing speaks of it. The `park` route earns 0."""
    if route.get("park"):
        return 0.0, "waits docked"
    runs, credits, minutes, _once, _flown = by_route.get(rid, [0, 0.0, 0.0, 0, 0.0])
    if runs >= 2 and minutes:
        return credits / minutes * 60, "%d runs of the window" % runs
    if worth(route) is not None:
        return float(worth(route)), "all its runs"
    if cands.get(rid) is not None:
        return float(cands[rid]), "the route maker's estimate"
    return None, "not measured"


def forecast(routes, on, by_route, cands, hours):
    """[(route id, ships on it, credits per ship-hour or None, what that rests on, steady credits an hour, paid once)],
    the most first: what the routes bring while the ships of `on` ({route id: ships}) stay on them. A route that pays
    once per pilot adds no steady money: its reward (what its runs measured, per ship) stands in the last field."""
    found = []
    for rid, ships in on.items():
        route = routes.get(rid) or {}
        if route.get("once"):
            paid = worth(route)
            found.append((rid, ships, None, "pays once per pilot" if paid is not None else "pays once, not measured", 0.0, int((paid or 0) * ships)))
            continue
        rate, rests = rate_of(route, rid, by_route, cands) if route else (None, "route file gone")
        found.append((rid, ships, rate, rests, (rate or 0.0) * ships, 0))
    return sorted(found, key=lambda row: (-(row[4] + row[5]), row[0]))


def show_forecast(root, data, now, who, hours):
    routes, rows = dispatch.load_routes(root), dispatch.run_rows(data)
    orders = dispatch.fresh_orders(data, now)
    _by_pilot, by_route = pilot_stats(rows, now - hours * 3600)
    book = read(Path(data) / "routes" / "opportunities.json", {})
    cands = {c["route"]["id"]: c["per_ship_hour"] for c in (book.get("candidates") if isinstance(book, dict) else None) or []
             if isinstance(c, dict) and isinstance(c.get("route"), dict) and c["route"].get("id") and isinstance(c.get("per_ship_hour"), (int, float))}
    titles = {key: title for key, title, _text in routefiles.STAGES}
    crew, fleet = pilots(data)
    members = [m for m in division.MEMBERS if who in ("all", m)]
    if not members:
        print("no member `%s`: %s or all" % (who, ", ".join(division.MEMBERS)))
        return 1
    census = {system: rid for rid, route in routes.items() if route.get("kind") == "census" for system in route.get("systems") or []}
    print("FORECAST | the next %g hours, if every ship stays on the route it flies now and each route pays what it measured | steady money; what is paid once "
          "stands apart | fleet data read %s" % (hours, ago(fleet.get("updated_at"), now)))
    print("  a figure rests on the runs of the last %g hours (two or more), else on all runs of the route, else on the route maker's estimate; `not measured` counts as 0" % hours)
    print("  no promise: a route closes when its bid, its field or its herd is used up (the tool fill says what each carries), and the dispatcher then sends the ship "
          "to the next route of its list")
    total = [0, 0.0, 0]
    for member in members:
        mine = [ship for ship, _detail in crew if division.owner(ship.get("name") or "", data) == member]
        on, state = Counter(), Counter()
        for ship in mine:
            what = orders.get(ship.get("name") or "")
            if ship.get("status") != "connected":
                state["not connected"] += 1
            elif what and what.startswith("hand "):
                state["by hand"] += 1
            elif what:
                kind, _, rest = what.partition(" ")
                on[census.get(rest, rest) if kind == "census" else rest] += 1
                state["on a route"] += 1
            elif (ship.get("activity") or {}).get("kind") != "idle":
                state["by hand"] += 1
            else:
                state["waiting"] += 1
        planned = Counter()                                    # ships that have the route in their plan (the role plans' counts)
        for role, keeper in division.ROLES.items():
            spec = read(Path(root) / "routes" / "plans" / (role + ".json"), {}) if keeper == member else {}
            for rid, count in (spec.get("ships") if isinstance(spec, dict) and isinstance(spec.get("ships"), dict) else {}).items():
                planned[rid] += count if isinstance(count, int) else 0
        found = forecast(routes, on, by_route, cands, hours)
        steady, once = sum(row[4] for row in found), sum(row[5] for row in found)
        total = [total[0] + len(mine), total[1] + steady, total[2] + once]
        print("%s | %d ships: %s" % (member.upper(), len(mine), ", ".join("%d %s" % (n, key) for key, n in state.most_common()) or "none"))
        print("  %-40s %-8s %-16s %5s %7s %13s %-26s %10s %11s %10s" % ("route", "kind", "group", "ships", "in plan", "per ship-hour", "rests on", "per hour",
                                                                        "in %g h" % hours, "paid once"))
        for rid, ships, rate, rests, hour, paid in found:
            route = routes.get(rid) or {}
            print("  %-40s %-8s %-16s %5d %7s %13s %-26s %10s %11s %10s" % (
                rid[:40], str(route.get("kind") or "?")[:8], titles.get(routefiles.stage(route), "?")[:16] if route else "--", ships, planned.get(rid) or "--",
                num(rate) if rate is not None else "--", rests[:26], num(hour) if rate is not None else "--", num(hour * hours) if rate is not None else "--",
                num(paid) if paid else "--"))
        print("  SUM %s | steady money: %s credits an hour, %s per ship of the division, %s in %g hours | paid once on the way: %s"
              % (member, num(steady), num(steady / len(mine)) if mine else "--", num(steady * hours), hours, num(once) if once else "--"))
    if len(members) > 1:
        print("FLEET | %d ships | steady money: %s credits an hour, %s per ship, %s in %g hours | paid once on the way: %s"
              % (total[0], num(total[1]), num(total[1] / total[0]) if total[0] else "--", num(total[1] * hours), hours, num(total[2]) if total[2] else "--"))
    return 0


def show_standing(root, data, now, who, hours):
    import fill                                    # the dispatcher's next pass played through for every free pilot
    seen = fill.survey(root, data, now)
    routes, state = seen["routes"], seen["state"]
    by_pilot, by_route = pilot_stats(state["rows"], now - hours * 3600)
    titles = {key: title for key, title, _text in routefiles.STAGES}
    named = dispatch.flagships(data)
    crew_all, fleet = pilots(data)
    roles = [role for role in seen["roles"] if who in ("all", role, division.ROLES.get(role))]
    if not roles:
        print("no plan of `%s`: a member's name, a role (%s) or all" % (who, ", ".join(sorted(division.ROLES))))
        return 1
    import plan as planfile                        # each ship's own routes, from its division's plan file
    files = {}
    for role in roles:
        its = planfile.division_of(role)
        if its and its not in files:
            files[its] = planfile.load(root, data, its, routes)[0]["ships"]
        own_of = files.get(its) or {}
        crew, plan = seen["crews"].get(role) or {}, seen["roles"].get(role) or []
        mine = [(ship, detail) for ship, detail in crew_all if dispatch.role_of(ship.get("name") or "", named) == role]
        print("STANDING FLEET | %s, role %s: %d ships | fleet data read %s | figures: the last %g hours of runs, steady money (paid once apart) | credits per ship-hour throughout"
              % (division.ROLES.get(role, "?"), role, len(mine), ago(fleet.get("updated_at"), now), hours))
        print("PLAN %s: %d routes, the role's in one order (game/routes/plans/%s.json); each ship flies the list First, its own routes and the list Then of its division's "
              "plan file (`plan.py show`, the tool plan) and takes the first one open to it" % (role, len(plan), role))
        print("  carries: the ships a route keeps busy hour after hour by what its bid, its field or its herd regains (`?` not measured), and `+N` more for one turn "
              "while today's standing order or field holds; never more ships than that on it (fill.py lift refuses)")
        print("  %2s %-40s %-8s %-16s %10s %9s %9s | %4s %9s %13s %9s" % ("#", "route", "kind", "group", "measured/h", "ships/cap", "carries", "runs", "credits", "per ship-hour", "paid once"))
        for n, rid in enumerate(plan, 1):
            route = routes.get(rid)
            if not route:
                print("  %2d %-40s no route file" % (n, rid[:40]))
                continue
            runs, credits, minutes, once, _flown = by_route.get(rid, [0, 0.0, 0.0, 0, 0.0])
            print("  %2d %-40s %-8s %-16s %10s %9s %9s | %4d %9s %13s %9s" % (n, rid[:40], route["kind"], titles[routefiles.stage(route)][:16], routefiles.figure(route),
                                                                          "%d/%s" % (fill.flying_now(route, rid, state["orders"]), route.get("max_ships") or "-"),
                                                                          fill.carried(fill.carries(seen, route)), runs,
                                                                          num(credits) if runs else "--", per_hour(credits, minutes), num(once) if once else "--"))
        waiting = {p["name"]: p for p in crew.get("waiting") or []}
        starting = dict(crew.get("starting") or [])
        ranked = sorted(((worth(routes[rid]) or 0, rid) for rid in plan if rid in routes and not routes[rid].get("once") and (worth(routes[rid]) or 0) > 0), reverse=True)
        print("SHIPS: what each flies now, what it earned, and what closes the best route of the plan to a ship that waits")
        counts, sums = Counter(), [0.0, 0.0, 0.0, 0.0]
        for ship, detail in sorted(mine, key=lambda sd: (sd[0].get("number") or 0, sd[0].get("name") or "")):
            name = ship.get("name") or ""
            what = state["orders"].get(name)
            if ship.get("status") != "connected":
                doing, key = "not connected", "away"
            elif what and what.startswith("hand "):
                doing, key = "by hand: " + what[5:], "by hand"
            elif what:
                rid = what.split(" ", 1)[1] if " " in what else what
                route = routes.get(rid)
                doing = "flies " + what
                key = "reading" if what.startswith("census ") else "waiting" if route and route.get("park") else "on a route that pays once" if route and route.get("once") else \
                    "on standing work" if route and routefiles.standing(route) else "on a route that pays" if route and fill.proven(route) else "on a test or a fitting"
                if route and route.get("park"):
                    doing = "waits docked (the plan's last route)"
            elif (ship.get("activity") or {}).get("kind") != "idle":
                doing, key = "busy by hand (%s)" % (ship.get("activity") or {}).get("kind"), "by hand"
            elif name in starting:
                doing, key = "starts %s at the next pass" % starting[name], "starting"
            else:
                key, doing = "waiting", "waits at %s" % (ship.get("system") or "?")
                if name in waiting and ranked:
                    rid = ranked[0][1]
                    reason, _argument = dispatch.why_not(waiting[name], rid, routes.get(rid), dict(state, orders=seen["played"], rows=seen["by_route"].get(rid, [])))
                    doing += " | best route %s (%s/h): %s" % (rid, num(ranked[0][0]), reason or "open at the next pass")
                elif name in waiting:
                    doing += " | the plan holds no route that repeats and pays"
            counts[key] += 1
            doing += " | own routes: " + (" > ".join(own_of.get(name) or []) or "none")
            runs, credits, minutes, once, flown = by_pilot.get(name, [0, 0.0, 0.0, 0, 0.0])
            sums = [a + b for a, b in zip(sums, (credits, minutes, flown, once))]
            tools = ", ".join(sorted({str(m) for m in modules_of(detail) if m}))
            print("  %-16s %-34s | %2d runs %5.0f min %9s cr %7s/h flown %7s/h clock%s | %s"
                  % (name[:16], (tools or "no module read")[:34], runs, flown, num(credits) if runs else "--", per_hour(credits, minutes), num(credits / hours) if runs else "0",
                     " +%s once" % num(once) if once else "", doing[:260]))
        clock = len(mine) * hours
        print("SUM %s | %s | the runs of %g hours: income %s credits an hour (steady money), paid once %s; busy %d%% of %d ship-hours; %s per ship-hour flown"
              % (role, ", ".join("%d %s" % (n, key) for key, n in counts.most_common()) or "no ship", hours, num(sums[0] / hours), num(sums[3]),
                 100 * sums[2] / 60 / clock if clock else 0, clock, per_hour(sums[0], sums[1])))
        print("  to change it: your plan file gives each ship its own routes (the tool plan: show, set, first, then, apply; `plan.py`); the tool fill says why a route is closed and "
              "adds the work that stands open")
    return 0



def show_eyes(data, who):
    """Compact loadout digest from read.db: faction cap & hull readiness, open P1/P2 needs (gather/buy/craft/fee),
    SHORT/LOW supply chains, division upgrade gaps, MAD anomalies, and NPC/PvP raid battles. Silent if no read.db."""
    conn = history.connect(data)
    if conn is None:
        return
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')")}
        lines = []
        if "faction" in tables:
            fac = conn.execute("SELECT member_count, members_limit, treasury, owned_bases FROM faction LIMIT 1").fetchone()
            hulls_txt, vb_txt = "", ""
            if "ships" in tables and "hulls" in tables:
                tiers = conn.execute(
                    "SELECT COALESCE(h.tier, 0), COUNT(*) FROM ships s "
                    "LEFT JOIN hulls h ON h.id = s.class OR h.name = s.class GROUP BY 1 ORDER BY 1 DESC"
                ).fetchall()
                hulls_txt = " | hulls: " + (", ".join("%d T%d" % (n, tr) for tr, n in tiers) or "none")
            if "ship_skills" in tables and "ships" in tables:
                vb = conn.execute("SELECT COUNT(DISTINCT pilot) FROM ship_skills WHERE skill LIKE '%voidborn%' AND level >= 1").fetchone()[0]
                tot_s = conn.execute("SELECT COUNT(*) FROM ships").fetchone()[0]
                vb_txt = " | Voidborn >=1: %d/%d" % (vb, tot_s)
            if fac:
                mc, ml, trs, ob = fac[0] or 0, fac[1] or 0, fac[2] or 0, fac[3] or 0
                tot_fl = conn.execute("SELECT COUNT(*) FROM ships").fetchone()[0] if "ships" in tables else mc
                open_seats = max(0, min(tot_fl, ml) - mc) if ml else 0
                if ml and mc >= ml - 2:
                    cap_flag = " (AT CAP -- P1 recruitment-center; %d/%d fleet ships seated)" % (mc, tot_fl)
                elif open_seats > 0:
                    cap_flag = " (%d OPEN SEATS READY NOW -- Recruitment Center ACTIVE; queue in 1s: wallet.py seat --pick %d)" % (open_seats, open_seats)
                else:
                    cap_flag = ""
                lines.append("  FACTION | seats %d/%d%s | treasury %s cr | bases %d%s%s"
                             % (mc, ml, cap_flag, num(trs), ob, hulls_txt, vb_txt))
                if who in ("all", "Unity") and "ship_modules" in tables and "ships" in tables:
                    off_tot = conn.execute(
                        "SELECT COUNT(DISTINCT s.pilot) FROM ships s JOIN ship_modules m ON m.pilot=s.pilot "
                        "WHERE (s.division='Mining' AND m.module='pulse_laser_i') "
                        "OR (s.division IN ('Trade','Logistics','Intel') AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i','pulse_laser_i')) "
                        "OR (s.division='Military' AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i'))"
                    ).fetchone()[0]
                    lines.append("  FLEET SLOTS | %d/%d division ships still carry off-role starter modules (`unfit` + multi-slot `fit` `count: 2` live)"
                                 % (off_tot, tot_fl))
        if "ships" in tables and who not in ("all", "Unity"):
            div_name = {"Zero": "Mining", "Mercury": "Trade", "Apollo": "Logistics", "Apophis": "Military", "Oracle": "Intel"}.get(who, who)
            drow = conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(CASE WHEN COALESCE(h.tier,0)=0 THEN 1 ELSE 0 END),0), "
                "COALESCE(MAX(sk.level),0), COALESCE(ROUND(AVG(sk.level),1),0) "
                "FROM ships s LEFT JOIN hulls h ON h.id=s.class OR h.name=s.class "
                "LEFT JOIN ship_skills sk ON sk.pilot=s.pilot AND sk.skill='piloting' WHERE s.division=?",
                (div_name,),
            ).fetchone()
            if drow and drow[0]:
                ready10 = conn.execute(
                    "SELECT COUNT(*) FROM ships s JOIN ship_skills sk ON sk.pilot=s.pilot "
                    "WHERE s.division=? AND sk.skill='piloting' AND sk.level >= 10", (div_name,)
                ).fetchone()[0]
                lines.append("  MY UPGRADE READINESS (%s) | %d/%d ships still Tier-0 hull | Piloting avg %s, max %d (%d ships >= Lv10 ready for T2 hulls)"
                             % (div_name, drow[1], drow[0], drow[3], drow[2], ready10))
                if "ship_modules" in tables:
                    off_map = {
                        "Mining": ("pulse_laser_i",),
                        "Trade": ("mining_laser_i", "ice_harvester_i", "gas_harvester_i", "pulse_laser_i"),
                        "Logistics": ("mining_laser_i", "ice_harvester_i", "gas_harvester_i", "pulse_laser_i"),
                        "Military": ("mining_laser_i", "ice_harvester_i", "gas_harvester_i"),
                        "Intel": ("mining_laser_i", "ice_harvester_i", "gas_harvester_i", "pulse_laser_i"),
                    }
                    off_mods = off_map.get(div_name, ())
                    if off_mods:
                        q_marks = ",".join("?" for _ in off_mods)
                        off_ships = conn.execute(
                            "SELECT COUNT(DISTINCT s.pilot) FROM ships s JOIN ship_modules m ON m.pilot=s.pilot "
                            "WHERE s.division=? AND m.module IN (%s)" % q_marks,
                            (div_name,) + off_mods,
                        ).fetchone()[0]
                        u_under2 = conn.execute(
                            "SELECT COUNT(*) FROM ships s WHERE s.division=? AND "
                            "(SELECT COUNT(*) FROM ship_modules m WHERE m.pilot=s.pilot AND m.slot='utility' AND m.module NOT IN (%s)) < 2" % q_marks,
                            (div_name,) + off_mods,
                        ).fetchone()[0]
                        hold65 = conn.execute("SELECT COUNT(*) FROM ships WHERE division=? AND cargo_capacity <= 65", (div_name,)).fetchone()[0]
                        if off_ships or u_under2:
                            hint = {
                                "Mining": "Threshold fits 2x mining_laser_iii (44 pwr=2.0x) + shield_booster_i once pulse_laser_i (-5 pwr) is stripped, or laser_iii + cargo_expander_iii (165 hold)",
                                "Trade": "Threshold 2U slots fit 2x cargo_expander_ii/iii -> 165-265 hold (2.5x-4.1x/trip) once starter mods are stripped",
                                "Logistics": "Threshold 2U slots fit 2x cargo_expander_ii/iii -> 165-265 hold (2.5x-4.1x/trip) once starter/harvester mods are stripped",
                                "Military": "Stripping mining_laser_i/harvesters frees +5 pwr & 2U slots for 2x shield_booster_ii + afterburner/web/expander",
                                "Intel": "Stripping mining_laser_i + pulse_laser_i frees +10 pwr & 2U slots for survey_scanner_ii + afterburner/cloak",
                            }.get(div_name, "")
                            lines.append(
                                "  SLOT & LOADOUT MULTIPLIER (%s) | %d/%d ships carry off-role starter mods | %d/%d have <2 role utility mods (%d at <=65 hold) | use stop `unfit` + `fit` (`count: 2`, `requires.modules_below`/`any_module`): %s"
                                % (div_name, off_ships, drow[0], u_under2, drow[0], hold65, hint)
                            )
        if "need_status" in tables:
            nrows = conn.execute(
                "SELECT priority, id, division, ROUND(covered, 1), gather, buy, craft, fee "
                "FROM need_status WHERE priority <= 2 ORDER BY priority, rank LIMIT 8"
            ).fetchall()
            if nrows:
                lines.append("  OPEN P1/P2 PRIORITIES (align gather/buy/craft/treasury to close these):")
                for pr, nid, div, cov, gat, buy_s, crf, fee in nrows:
                    parts = []
                    if gat:
                        parts.append("gather: " + str(gat)[:55])
                    if buy_s:
                        parts.append("buy: " + str(buy_s)[:55])
                    if crf:
                        parts.append("craft: " + str(crf).split(";")[0][:55])
                    if fee:
                        parts.append("fee: %s cr" % num(fee))
                    lines.append("    [P%d %5.1f%%] %-22s (%s) -> %s" % (pr or 0, cov or 0.0, str(nid)[:22], div, " | ".join(parts) or "READY (100% stocked, nothing short -> execute or close via needs action=done)"))
        if "supply_status" in tables:
            srows = conn.execute(
                "SELECT chain, item, place, stock, keep, status FROM supply_status "
                "WHERE status != 'ok' ORDER BY CASE status WHEN 'short' THEN 0 WHEN 'not read' THEN 1 ELSE 2 END, chain LIMIT 8"
            ).fetchall()
            if srows:
                lines.append("  SUPPLY BOTTLENECKS: " + "; ".join(
                    "%s (%s @ %s: %s/%s %s)" % (c, it, pl, num(st), num(kp), str(stt).upper()) for c, it, pl, st, kp, stt in srows
                ))
        if "stats_figures" in tables:
            mrows = conn.execute(
                "SELECT subject, text FROM stats_figures WHERE view='alerts' AND text LIKE 'OUT %' ORDER BY subject LIMIT 6"
            ).fetchall()
            if mrows:
                lines.append("  MAD ANOMALIES: " + "; ".join("%s (%s)" % (subj, str(txt).split(":", 1)[0]) for subj, txt in mrows))
        if "public_battles" in tables:
            brows = conn.execute(
                "SELECT system_name, system, category, status, destroyed, tags FROM public_battles "
                "WHERE category != 'pirate' OR tags LIKE '%CLTV%' ORDER BY tick DESC LIMIT 5"
            ).fetchall()
            if brows:
                lines.append("  RAID / PVP BATTLES (public_battles): " + "; ".join(
                    "%s [%s/%s, lost %d, tags %s]" % (sn or sy, cat, stt, d or 0, tg or "-") for sn, sy, cat, stt, d, tg in brows
                ))
        if "fuel_sinks" in tables:
            frows = {r[0]: (r[1], r[2], r[3]) for r in conn.execute("SELECT category, runs_24h, ship_hours_24h, net_credits_24h FROM fuel_sinks").fetchall()}
            jl = frows.get("jump_loops")
            pr = frows.get("productive")
            if jl and jl[1] > 50:
                lines.append(
                    "  24H FLIGHT EFFICIENCY | productive: %.0fh (%+d cr) vs empty train-jumps: %.0fh (%+d cr) -> replace empty jump loops with zero-fuel docked crafting, Station Bursar bids (`hive.py contracts`) & cargo-carrying runs!"
                    % (pr[1] if pr else 0.0, int(pr[2]) if pr else 0, jl[1], int(jl[2]))
                )
        if "contract_candidates" in tables and who in ("all", "Unity", "Mercury", "Apollo"):
            cc_n = conn.execute("SELECT COUNT(*) FROM contract_candidates WHERE priority <= 2").fetchone()[0]
            if cc_n:
                lines.append("  BOTTLENECK CONTRACTS (%d open P1/P2 needs) | run `hive.py contracts` (MCP: `fleet view=contracts`) to post zero-fee Station Bursar buy bids & Notice Board contracts (`communications/contracts.log`)." % cc_n)
        try:
            import rival_playbook
            bline = rival_playbook.benchmark_line(data)
            if bline:
                lines.insert(0, bline)
        except Exception:
            pass
        if lines:
            print("=== EYES & EARS: BOTTLENECKS, PRIORITIES, SUPPLY & ALERTS")
            print("\n".join(lines))
    except Exception as error:                                      # noqa: BLE001  never block briefing
        print("  eyes & ears not read: %s: %s" % (type(error).__name__, error))
    finally:
        conn.close()


def show_briefing(root, data, now, who, hours):
    """A session's start in one answer (Suggi, 2026-11-16: the orders and the overview loaded at preflight): the orders in
    force, the requests not closed that are addressed to the member, the fleet's money, the member's standing fleet
    and the fill gate of its roles."""
    __import__("basewatch").briefing(data, now)                       # Q75 (3), errors.log ENT-112: a wrecked base, a damaged facility: first
    import fill
    repo = Path(root).resolve().parent
    comms = repo / "scripts" / "comms.py"
    asks = ["requests"] + ([] if who in ("all", "Unity") else ["--to", who])
    for title, words in (("THE ORDERS IN FORCE (the newest entry of communications/orders.log)", ["orders"]),
                         ("REQUESTS NOT CLOSED" + ("" if len(asks) == 1 else ", ADDRESSED TO " + who), asks)):
        print("=== " + title)
        if comms.is_file():
            done = subprocess.run([sys.executable, "-B", str(comms)] + words, cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
            print(done.stdout.rstrip())
        else:
            print("  not read: %s is missing" % comms)
    try:                                                            # r22: the requests addressed to the reader untouched over 3 days, counted
        print(__import__("docs_division").load_comms().stale_line(str(repo), who, now))
    except Exception as error:                                      # noqa: BLE001  a count that fails never holds up the briefing
        print("  stale requests not counted: %s: %s" % (type(error).__name__, error))
    if who not in ("all", "Unity") and comms.is_file():
        done_out = subprocess.run([sys.executable, "-B", str(comms), "requests", "--from", who],
                                  cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60)
        if "OPEN (" in done_out.stdout and not ("OPEN (0)" in done_out.stdout and "ACCEPTED (0)" in done_out.stdout):
            print("=== MY OUTBOUND REQUESTS (open or accepted)")
            print(done_out.stdout.rstrip())
    import docs as writings                                         # Suggi, 2026-11-17: what changed in the written knowledge, not the whole files
    writings.briefing(root, data, now, who)
    __import__("guidebook").briefing(root, data, now, who)           # Suggi, 2026-11-18: the own class card, and what stands over its cap
    __import__("needs").briefing(root, data, now, who)               # Suggi, 2026-11-21: the division's open needs, how many are red
    show_eyes(data, who)
    print("=== THE FLEET'S MONEY")
    show_fleet(root, data, now)
    print("=== MY STANDING FLEET")
    code = show_standing(root, data, now, who, hours)
    print("=== THE FORECAST (the SUM line of what the routes flown now bring; every route: `hive.py forecast`)")
    import contextlib                                               # Oracle, 2026-11-16: the orders ask for this line before and after a plan change
    import io
    lines = io.StringIO()
    with contextlib.redirect_stdout(lines):
        show_forecast(root, data, now, who if who in division.MEMBERS else "all", hours)
    print("\n".join(line for line in lines.getvalue().splitlines() if line.lstrip().startswith("SUM")) or "  not read")
    print("=== MY PLAN FILE (every ship with its own routes; I change it and the dispatcher sends the ships by it)")
    import plan as planfile
    planfile.show(root, data, sorted(planfile.DIVISIONS) if who in ("all", "Unity") and who != planfile.DIVISIONS["command"] else [planfile.division_of(who)] if planfile.division_of(who) else [], True)
    print("=== THE FILL GATE (no ship is idle)")
    seen = fill.survey(root, data, now)
    for role in sorted(r for r in seen["roles"] if who in ("all", r, division.ROLES.get(r))):
        print(fill.verdict(seen, fill.read_role(seen, role))[1])
    print("=== THE HANDBOOK: how the data flows, where to ask what, every table and view with its columns and examples: "
          "hive.py handbook [<table>|<subject>|<word>] (the tool docs, view=handbook)")
    return code


def show_store(data, now, hours, rest):
    """The history store's read copy (store.py, the service `store`): its tables and every route's credits per ship-hour
    over the whole hours of the window; with `price <item>`, the item's price range per station. The store keeps sums by
    hour as retention.py says (90 days once it is on), so a window may reach back past what the records still hold."""
    conn = history.connect(data)
    if conn is None:
        print("STORE | no read copy at %s: the service `store` has not published one yet (services/status.json)" % (Path(data) / "store" / "read.db"))
        return 1
    try:
        since = int(now - hours * 3600) // 3600 * 3600
        when = time.strftime("%Y-%m-%d %H:%M", time.gmtime(since))
        if rest and rest[0] == "price":
            if len(rest) < 2:
                print("STORE price | name the item: hive.py store price <item id> [--hours N]")
                return 1
            _books, where = books(data)
            rows = conn.execute("SELECT base, COUNT(*), MIN(bid_lo), MAX(bid_hi), MIN(ask_lo), MAX(ask_hi), SUM(moves), MAX(hour) FROM market_hour "
                                "WHERE item = ? AND hour >= ? GROUP BY base ORDER BY MAX(bid_hi) DESC, base", (rest[1], since)).fetchall()
            print("STORE price %s | per station, the whole hours since %s UTC | the lowest and highest best bid and best ask a reading saw (the store's hourly sums); "
                  "a price is what stood at the top of the book, not what a load sells for" % (rest[1], when))
            if not rows:
                print("  no price move of `%s` on record in that time" % rest[1])
                return 0
            print("  %-34s %5s %9s %9s %9s %9s %6s  %s" % ("station", "hours", "bid low", "bid high", "ask low", "ask high", "moves", "newest hour (UTC)"))
            for base, count, bid_lo, bid_hi, ask_lo, ask_hi, moved, newest in rows:
                print("  %-34s %5d %9s %9s %9s %9s %6d  %s" % (label(base, where)[:34], count, num(bid_lo), num(bid_hi), num(ask_lo), num(ask_hi), moved,
                                                         time.strftime("%m-%d %H:00", time.gmtime(newest))))
            return 0
        for line in history.status(data, now):
            print(("STORE | " + line) if line.startswith("read copy") else line)
        rates = history.route_rates(conn, since)
        print("ROUTES | the whole hours since %s UTC | steady credits (money paid once left out) of the runs that read a wallet, per ship-hour of those runs" % when)
        if not rates:
            print("  no run on record in that time")
            return 0
        print("  %-48s %5s %8s %11s %11s %10s" % ("route", "runs", "ship-h", "credits", "per ship-h", "paid once"))
        order = sorted(rates.items(), key=lambda kv: (kv[1][4] is None, -(kv[1][4] or 0), kv[0]))
        for route, (runs, minutes, credits, one_time, rate) in order:
            print("  %-48s %5d %8.1f %11s %11s %10s" % (route[:48], runs, (minutes or 0) / 60, num(credits), num(rate) if rate is not None else "not read", num(one_time) if one_time else "--"))
        total_minutes, total = sum(v[1] or 0 for v in rates.values()), sum(v[2] or 0 for v in rates.values())
        print("  %-48s %5d %8.1f %11s %11s" % ("ALL ROUTES", sum(v[0] for v in rates.values()), total_minutes / 60, num(total), per_hour(total, total_minutes)))
        return 0
    finally:
        conn.close()


def copy_line(data, now):
    """What an answer of the store rests on: the read copy, when it was written and how old it is."""
    path = Path(data) / "store" / "read.db"
    written = path.stat().st_mtime if path.is_file() else None
    return "the store's read copy %s, written %s (%s)" % (path, time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(written)) if written else "never",
                                                       "%d s old" % (now - written) if written else "not published yet")


def shown(value, width=SQL_CELL):
    """A value as it is, on one line; NULL for none; a text longer than `width` cut with `...`."""
    text = "NULL" if value is None else str(value).replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return (text[:width - 3] + "...", True) if len(text) > width else (text, False)


def show_sql(data, now, statement, limit):
    """One read-only statement on the store's read copy (store.py query), its rows as an aligned table: numbers to the right,
    values as they are, NULL for none."""
    try:
        limit = int(limit)
    except ValueError:
        print("SQL | --limit takes a number, not `%s`" % limit)
        return 1
    found = history.query(data, statement, limit=limit)
    if found["error"]:
        print("SQL | %s | %s" % (found["error"], copy_line(data, now)))
        print("  the tables and their columns: hive.py schema; one table with three example questions: hive.py schema <table>")
        return 1
    rows, cut = [], 0
    for row in found["rows"]:
        cells = [shown(v) for v in row]
        cut += sum(1 for _text, was in cells if was)
        rows.append([text for text, _was in cells])
    values = lambda n: [row[n] for row in found["rows"] if row[n] is not None]
    right = [bool(values(n)) and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values(n)) for n in range(len(found["columns"]))]
    widths = [max([len(str(c))] + [len(r[n]) for r in rows]) for n, c in enumerate(found["columns"])]
    line = lambda cells: "  " + "  ".join((c.rjust(w) if right[n] else c.ljust(w)) for n, (c, w) in enumerate(zip(cells, widths))).rstrip()
    print("SQL | %d rows%s | %s" % (len(rows), " (cut at --limit %d: more rows match; raise it or narrow the statement)" % limit if found["cut"] else "",
                                    copy_line(data, now)))
    print(line([str(c) for c in found["columns"]]))
    print(line(["-" * w for w in widths]))
    for row in rows:
        print(line(row))
    if cut:
        print("  %d cells longer than %d characters are cut (...): select substr(<column>, %d) for the rest" % (cut, SQL_CELL, SQL_CELL - 2))
    return 0


def show_schema(data, now, name):
    """Every table and view of the store with its description and columns; one table with its columns and example questions."""
    conn = history.connect(data)
    if conn is None:
        print("SCHEMA | no read copy at %s: the service `store` has not published one yet" % (Path(data) / "store" / "read.db"))
        return 1
    try:
        found = history.schema(conn)
    finally:
        conn.close()
    if name and name not in found:
        near = sorted(n for n in found if name.lower() in n)
        print("SCHEMA | no table or view `%s`%s" % (name, ": did you mean " + ", ".join(near) if near else "; hive.py schema lists them all"))
        return 1
    if not name:
        tables = sum(1 for t in found.values() if t["kind"] == "table")
        print("SCHEMA | %d tables, %d views | %s | `hive.py schema <table>`: its columns and three example questions; "
              "`hive.py sql \"<SELECT ...>\"` asks" % (tables, len(found) - tables, copy_line(data, now)))
        for table, entry in found.items():
            print("%s %s -- %s" % (entry["kind"].upper(), table, entry["description"] or "no description"))
            print("  " + ", ".join(column for column, _type in entry["columns"]))
        return 0
    entry = found[name]
    print("SCHEMA %s | %s | %s" % (name, entry["kind"], entry["description"] or "no description"))
    for column, kind in entry["columns"]:
        print("  %-24s %s" % (column, kind or "--"))
    print("EXAMPLES (hive.py sql \"<statement>\"):")
    for question, sql in entry["examples"]:
        print("  -- %s" % question)
        print("  %s" % sql)
    if not entry["examples"]:
        print("  none written for this table")
    return 0


FLOW_ROWS = 12                 # items `flow` prints per division


def rate_text(rate):
    return "{:+,.1f}".format(rate) if rate is not None else "--"


def show_flow(root, data, now, who, hours):
    """What each division put into the reserve per hour. A division that stores what the bases take (hunt goods, ore)
    instead of selling it reads as a loss in money; its yield is the units it gathers (Military's wish, 2026-11-16). Runs
    record no goods stored, so the figure is the store's hourly samples of the storage book (store.reserve_flow, table
    stock_hour); which items are the reserve's is surplus.py's answer (every item its walk asks for, as `reserve` lists
    them). Per division the items gained per hour over the window asked, the most first, at most FLOW_ROWS; a SUM line."""
    names = {member: board.NAMES.get(member, member) for member in division.MEMBERS}
    member = None
    if who != "all":
        member = next((m for m in division.MEMBERS if who.lower() in (m.lower(), names[m].lower())), None)
        if member is None:
            print("FLOW | no member `%s`: %s, or all" % (who, ", ".join(division.MEMBERS)))
            return 1
    try:
        hours = int(float(hours))
    except ValueError:
        print("FLOW | --hours takes a number of hours, not `%s`" % hours)
        return 1
    hours = max(1, hours)
    windows = tuple(sorted({4, 12, 24, hours}))
    found = spare.surplus(data, str(Path(root).parent))        # surplus.py takes the repository, this script its game folder
    items = sorted(r["id"] for r in found["rows"] if r["demand"])
    conn = history.connect(data)
    if conn is None:
        print("FLOW | no read copy at %s: the service `store` has not published one yet" % (Path(data) / "store" / "read.db"))
        return 1
    try:
        flow = history.reserve_flow(conn, items, windows)
    finally:
        conn.close()
    hour_text = lambda h: time.strftime("%Y-%m-%d %H:00", time.gmtime(h))
    print("FLOW | what each division put into the reserve per hour: the units it holds (station storage and holds) of the %d items the reserve asks for "
          "(surplus.py reserve), and their change per hour, the most gained over the last %d hours first | storage book of %s | the store's samples "
          "(stock_hour): %s" % (len(items), hours, found["written"] or "-- (none yet)", "%s to %s UTC, %.1f hours on record" % (
              hour_text(flow["oldest"]), hour_text(flow["newest"]), flow["hours"]) if flow["newest"] is not None else "none yet"))
    if flow["newest"] is None:
        print("  no sample yet: the service `store` writes one an hour from the storage book")
        return 0
    short = [w for w in windows if flow["base"][w][2]]
    if short:
        print("  only %.1f hours on record: the figures of the last %s hours read from the oldest sample (%s UTC), over the hours there are%s"
              % (flow["hours"], ", ".join("%d" % w for w in short), hour_text(flow["oldest"]), "; one sample is no rate (--)" if flow["hours"] <= 0 else ""))
    by = defaultdict(list)
    for row in flow["rows"]:
        by[row["division"]].append(row)
    order = [names[m] for m in division.MEMBERS] + sorted(set(by) - set(names.values()))
    head = "  %-32s %12s" % ("item", "held now") + "".join(" %12s" % ("per h, %dh" % w) for w in windows)
    for name in order:
        if member is not None and name != names[member]:
            continue
        of = next((m for m in division.MEMBERS if names[m] == name), "")
        mine = by.get(name) or []
        if not mine:
            if member is not None:                     # asked for by name: said; in `all` a division without any is left out
                print("%s (%s) | none of the reserve's items in the samples" % (name, of))
            continue
        total = flow["sums"][name]
        print("%s (%s) | %d of the reserve's items held now, %s units" % (name, of, total["items"], num(total["units"])))
        print(head)
        ranked = sorted(mine, key=lambda r: (r["rate"][hours] is None, -(r["rate"][hours] or 0), -r["units"], r["item"]))
        for r in ranked[:FLOW_ROWS]:
            print("  %-32s %12s" % (r["item"][:32], num(r["units"])) + "".join(" %12s" % rate_text(r["rate"][w]) for w in windows))
        if len(ranked) > FLOW_ROWS:
            print("  ... %d more items: hive.py sql \"SELECT item, units FROM stock_hour WHERE division = '%s' AND hour = %d\"" % (len(ranked) - FLOW_ROWS, name, flow["newest"]))
        print("  %-32s %12s" % ("SUM %d items" % len(mine), num(total["units"])) + "".join(" %12s" % rate_text(total["rate"][w]) for w in windows))
    return 0


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data", "--group", "--kind", "--zone", "--hours", "--item", "--top", "--limit"))]
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
    if verb == "gauges":                              # rule F9: firepower and toughness against the herds (gauges.py, its own usage)
        import gauges                                 # here: only this verb needs it
        return gauges.main(args[args.index(verb) + 1:] + ["--data", data])
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
    if verb == "standing":
        _kind, me = division.member()
        return show_standing(root, data, now, rest[0] if rest else (me if me in division.MEMBERS else "all"), float(value("--hours", str(TURN))))
    if verb == "tasks":
        return show_tasks(root, data, now, float(value("--hours", str(TURN))))
    if verb == "forecast":
        return show_forecast(root, data, now, rest[0] if rest else "all", float(value("--hours", str(TURN))))
    if verb == "refill":                             # the store's table stats_refill (stats.py); before its first computation, the records
        import stats
        return stats.main(["refill", "--data", data]) if stats.ready(data) else show_refill(root, data, now)
    if verb in ("docs", "changes"):                                 # the fleet's written knowledge by section, from the store (docs.py)
        import docs as writings
        return writings.hive(verb, args, root, data, now)
    if verb == "division":                                          # what each Admiral is doing, from the store (docs_division.py)
        return __import__("docs_division").show(root, data, now, rest[0] if rest else "all")
    if verb == "guide":                                             # a guidebook by chapter and entry, from the store (guidebook.py)
        return __import__("guidebook").hive(args, root, data, now)
    if verb == "briefing":
        _kind, me = division.member()
        return show_briefing(root, data, now, rest[0] if rest else (me if me in division.MEMBERS else "all"), float(value("--hours", str(TURN))))
    if verb == "store":
        return show_store(data, now, float(value("--hours", "24")), rest)
    if verb == "empire":
        return holdings.show(data)
    if verb in ("surplus", "reserve"):
        found = spare.surplus(data, str(Path(root).parent))        # surplus.py takes the repository, this script its game folder
        if verb == "reserve":
            return spare.show_reserve(found)
        return spare.show(found, int(value("--top", "15")), value("--kind", ""), value("--item", ""), "--all" in args)
    if verb == "supply":                           # the supply chains (supply.py); hive.py only reads: --write is never handed on
        import supply as chains
        return chains.main([rest[0] if rest else "show", "--root", root, "--data", data])
    if verb == "needs":                            # the needs register (needs.py); hive.py only reads: a write verb is refused there
        return __import__("needs").hive(args[args.index(verb) + 1:], root, data)
    if verb == "flow":
        return show_flow(root, data, now, rest[0] if rest else "all", value("--hours", str(TURN)))
    if verb == "inventory":
        return craftbook.show_inventory(craftbook.load(data) or {"version": "none", "items": {}}, data, rest[0] if rest else "total", value("--item", ""), int(value("--top", "40")))
    if verb == "contracts":                          # bottleneck procurement contracts, Station Bursar bids & rival board contracts
        import contracts
        return contracts.main(["--data", data, "--root", str(Path(root).parent if Path(root).name == "game" else root)])
    if verb == "progression":                        # live enterprise progression roadmap, rungs & milestones
        import progression
        return progression.main(["show", "--data", data, "--root", str(Path(root).parent if Path(root).name == "game" else root)])
    if verb == "rival":                              # #1 [HEXC] benchmark, resource-monopoly outposts, docked factory spreads & hull targets
        import rival_playbook
        return rival_playbook.main(["--data", data])
    if verb == "watchdog":                           # cross-turn velocity, loops and bottlenecks (watchdog.py)
        import watchdog
        wd_args = ["show", "--hours", value("--hours", str(TURN)), "--root", root, "--data", data]
        if "--json" in args:
            wd_args.append("--json")
        return watchdog.main(wd_args)
    if verb == "stats":                              # the fleet's statistics, computed by the store (stats.py, its own usage)
        import stats
        return stats.main(args[args.index(verb) + 1:] + ["--data", data])
    if verb == "handbook":                         # the store's handbook, written from the code (docs_handbook.py)
        return __import__("docs_handbook").show(root, data, now, " ".join(rest))
    if verb == "sql":
        return show_sql(data, now, " ".join(rest), value("--limit", str(SQL_ROWS)))
    if verb == "schema":
        return show_schema(data, now, rest[0] if rest else "")
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
