#!/usr/bin/env python3
"""routemaker.py -- find every way to earn that the fleet's own data shows, cost it, and write the route file for it.

WHAT: the service `routemaker` runs it. Every ten minutes it reads what the
      ships and services collected -- every field and what is left in it
      (data/scouting/), every station's order book with the depth at the
      best price (data/market/), every mission board (data/missions/), every
      herd (data/wildlife/), what we own (data/stock/), the runs so far
      (data/routes/runs.jsonl), the chart (game/map/galaxy.tsv) and the
      game's catalog of items and recipes (data/catalog/, fetched once a day
      from the game's public address) -- and writes
      data/routes/opportunities.json: one candidate per way to earn, with
      its estimate in credits per ship-hour after fuel, what the estimate
      rests on, what is uncertain about it, and the route file that flies
      it. For the candidates that would pay most if their book were deep, it
      reads the book price level by price level through a pilot docked
      there (data/market/ladders.json): a station's bid is often a ladder
      of single units. Five kinds:
        mine     a field, sold whole at the station that pays most for its mix
        trade    an item on offer at one station and bid for at another
        craft    a hand recipe whose inputs are on offer or in our storage
        hunt     a herd of a species whose loot a run of ours already sold
        mission  a mission on a board: its reward, what it asks for, how
                 many of our pilots have not booked it yet
      `show` prints the list for a member; `route <id>` prints a candidate's
      route file, ready to be saved under game/routes/ as a test.
RULES:
  - It reads only: files, and `view_market` through a docked pilot (at
    most 16 reads a pass). It moves no ship, buys nothing, changes no
    plan and writes no file of the repository.
  - An estimate is not a measurement. Every candidate is `untested` until a
    ship has flown its route and `routes.py measure` holds its figure; a
    candidate whose route exists shows that route's measured figure beside
    the estimate.
  - Units are sold down a book's price levels only as far as 80% of its
    best bid, and bought up to 120% of its best offer. Where no level is
    known, the depth at the best price counts; where a saved book has no
    depth at all, one unit counts. A gap that one load closes is costed
    as one load, not as an hour of loads. A book read more than six hours
    ago is `stale`.
  - A route it writes is a test: `max_ships` 1. The Admiral who flies it
    lifts the limit after the first RESULT line (game/routes/BLUEPRINT.md).
WHY:  five Admirals should not each search 30 systems, six books and six
      boards by hand at every turn, and a new field or a new bid that a
      scout brings home should show up as a route within minutes.

USAGE:
  routemaker.py                     run forever (the service `routemaker`)
  routemaker.py --once              one pass, then stop
  routemaker.py show [<Member>|all] [--kind mine|trade|craft|hunt|mission] [--top N]
                                    the candidates for a member's ships (default: the member this shell belongs to), best first
  routemaker.py route <id>          the route file of one candidate, with what its estimate rests on
  --data <dir>                      the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import os
import statistics
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict, deque
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent     # the game/ folder
EVERY = 600                  # seconds between two passes
CATALOG_URL = "https://game.spacemolt.com/api/catalog.json"
CATALOG_EVERY = 24 * 3600    # the catalog is fetched once a day at most
STALE = 6 * 3600             # a book or a field read longer ago is marked stale
LADDER_FRESH = 45 * 60       # a ladder read longer ago is read again when a candidate needs it
LADDER_READS = 16            # ladders read through docked pilots in one pass, at most
GATE = "http://172.30.0.32:7580"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
HARVESTER = {"ice_field": "ice_harvester_i", "gas_cloud": "gas_harvester_i"}
ROLE = {"mine": "miner", "trade": "trader", "craft": "hauler", "hunt": "drone", "mission": ""}
MEMBER_KINDS = {"Zero": ("mine", "mission"), "Mercury": ("trade", "mission"), "Apollo": ("craft", "mission"),
                "Apophis": ("hunt", "mission"), "Oracle": ("mission",), "Unity": ("mine", "trade", "craft", "hunt", "mission")}
# What a starter hull does, where no record measures it. Each is printed with every list.
ASSUME = {
    "cargo": 65,             # units in a starter's hold; replaced by the fleet's median when the live file is there
    "fuel_price": 13.0,      # credits per unit of fuel; replaced by the collector's meter when it has clean readings
    "fuel_per_jump": 1,      # units: the game's find_route for a starter hull, read 2026-11-15
    "fuel_per_leg": 2,       # units for one flight inside a system (station to field); fitted from the mine runs
    "jump_minutes": 2.0,     # minutes per jump; fitted from the census runs
    "leg_minutes": 1.5,      # minutes for one flight inside a system
    "dock_minutes": 1.5,     # minutes for a stop at a station
    "mine_rate": 0.05,       # units a minute per point of a field's richness; replaced by the mine runs' own figure
    "tax": 0.01,             # share of a purchase that goes to tax
}


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def age_of(stamp, now):
    try:
        return now - calendar.timegm(time.strptime(str(stamp)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return None


def num(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else 0


def sid(value, fallback=""):
    """A system's id from a field that holds the id or the system's whole record."""
    if isinstance(value, dict):
        value = value.get("id") or value.get("system_id")
    return str(value or fallback)


# ---------------------------------------------------------------- what is read

def load_chart(root):
    """{system: [neighbours]} from the chart."""
    lanes = {}
    try:
        lines = (Path(root) / "map" / "galaxy.tsv").read_text(encoding="utf-8").splitlines()
    except OSError:
        return lanes
    rows = [l.split("\t") for l in lines if l and not l.startswith("#")]
    if not rows:
        return lanes
    head = {name: n for n, name in enumerate(rows[0])}
    for row in rows[1:]:
        if len(row) > head.get("lanes", 99):
            lanes[row[head["id"]]] = [x for x in row[head["lanes"]].split(",") if x and x != "-"]
    return lanes


class Chart:
    def __init__(self, lanes):
        self.lanes, self.cache = lanes, {}

    def jumps(self, a, b):
        """Jumps between two systems along the lanes; None when no way is charted."""
        if a == b:
            return 0
        if a not in self.cache:
            dist, queue = {a: 0}, deque([a])
            while queue:
                here = queue.popleft()
                for there in self.lanes.get(here, ()):
                    if there not in dist:
                        dist[there] = dist[here] + 1
                        queue.append(there)
            self.cache[a] = dist
        return self.cache[a].get(b)


def load_world(data, root, now):
    """Everything the candidates are made from, as plain dicts."""
    data = Path(data)
    world = {"now": now, "fields": [], "stations": {}, "books": {}, "boards": {}, "herds": [], "chart": Chart(load_chart(root)),
             "ladders": read_json(data / "market" / "ladders.json", {}), "wanted": {}}
    for path in sorted((data / "scouting").glob("*.json")) if (data / "scouting").is_dir() else []:
        scout = read_json(path, {})
        system = sid(scout.get("system"), path.stem)
        for poi_id, entry in (scout.get("pois") or {}).items():
            poi = entry.get("poi") if isinstance(entry.get("poi"), dict) else {}
            if poi.get("type") == "station" and poi.get("base_id"):
                world["stations"][poi["base_id"]] = {"system": system, "poi": poi_id, "name": poi.get("name") or poi_id,
                                                     "at": "%s:%s:%s" % (system, poi_id, poi["base_id"])}
            resources = [{"id": r.get("resource_id"), "richness": num(r.get("richness")), "remaining": num(r.get("remaining"))}
                         for r in entry.get("resources") or poi.get("resources") or [] if isinstance(r, dict) and r.get("resource_id")]
            if resources:
                world["fields"].append({"system": system, "poi": poi_id, "name": poi.get("name") or poi_id, "type": poi.get("type") or "",
                                        "read_at": scout.get("read_at"), "resources": resources})
    for path in sorted((data / "market").glob("*.json")) if (data / "market").is_dir() else []:
        book = read_json(path, {})
        if path.name.startswith("history.") or not book.get("base"):
            continue
        items = {}
        for item in book.get("items") or []:
            if isinstance(item, dict) and item.get("item_id"):
                items[item["item_id"]] = {"bid": num(item.get("best_buy")), "bid_qty": num(item.get("best_buy_qty", item.get("buy_quantity"))),
                                          "bid_depth_known": "best_buy_qty" in item, "ask": num(item.get("best_sell")),
                                          "ask_qty": num(item.get("best_sell_qty", item.get("sell_quantity"))), "name": item.get("item_name") or item["item_id"]}
        world["books"][book["base"]] = {"system": sid(book.get("system")), "read_at": book.get("read_at"), "items": items}
    for path in sorted((data / "missions").glob("*.json")) if (data / "missions").is_dir() else []:
        board = read_json(path, {})
        if board.get("base"):
            world["boards"][board["base"]] = {"system": sid(board.get("system")), "read_at": board.get("read_at"),
                                              "missions": [m for m in board.get("missions") or [] if isinstance(m, dict)]}
    for path in sorted((data / "wildlife").glob("*.json")) if (data / "wildlife").is_dir() else []:
        wild = read_json(path, {})
        for poi_id, entry in (wild.get("pois") or {}).items():
            creatures = [c for c in entry.get("creatures") or [] if isinstance(c, dict) and c.get("species")]
            if creatures:
                world["herds"].append({"system": sid(wild.get("system"), path.stem), "poi": poi_id, "read_at": entry.get("read_at") or wild.get("read_at"),
                                       "species": Counter(c["species"] for c in creatures),
                                       "hull": {c["species"]: num(c.get("max_hull")) for c in creatures},
                                       "pirates": len(entry.get("pirates") or [])})
    catalog = read_json(newest_catalog(data), {})
    items = catalog.get("items") or []
    recipes = catalog.get("recipes") or []
    world["items"] = {i["id"]: i for i in (items.values() if isinstance(items, dict) else items) if isinstance(i, dict) and i.get("id")}
    world["recipes"] = [r for r in (recipes.values() if isinstance(recipes, dict) else recipes) if isinstance(r, dict) and r.get("hand_craftable")]
    world["catalog_version"] = catalog.get("version") or ""
    world["stock"] = (read_json(data / "stock" / "storage.json", {}).get("totals") or {}).get("by_station") or {}
    world["runs"] = []
    try:
        with open(data / "routes" / "runs.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    world["runs"].append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        pass
    world["routes"] = {}
    for path in sorted((Path(root) / "routes").glob("*.json")):
        route = read_json(path, None)
        if isinstance(route, dict) and route.get("id"):
            world["routes"][route["id"]] = route
    world["plans"] = division.load_plan(root)[0]
    fleet = read_json(data / "fleet" / "fleet.json", {})
    ships = [s for s in fleet.get("ships") or [] if isinstance(s, dict)]
    world["pilots"] = len(ships)
    world["docked"] = {}
    for ship in ships:
        if ship.get("docked") and ship.get("status") == "connected" and ship.get("name"):
            world["docked"].setdefault(ship["docked"], ship["name"])
    booked = defaultdict(set)
    for row in read_json(data / "fleet" / "onetime.json", []):
        if isinstance(row, list) and len(row) >= 4 and num(row[3]) > 0:
            booked[str(row[2]).lower()].add(str(row[1]))
    world["booked"] = booked
    world["assume"] = assumptions(world, ships, read_json(data / "fleet" / "meters.json", {}))
    return world


def newest_catalog(data):
    """The newest catalog in data/catalog/. Only a file named by a version (its name starts with a digit) is a catalog:
    this script writes ammo.json into the same folder, and taken for the catalog it failed every pass."""
    folder = Path(data) / "catalog"
    files = sorted((p for p in folder.glob("*.json") if p.stem[:1].isdigit()), key=lambda p: p.stat().st_mtime) if folder.is_dir() else []
    return files[-1] if files else folder / "none.json"


def assumptions(world, ships, meters):
    """The figures every estimate uses, each with where it comes from."""
    out = {key: {"value": value, "from": "assumed"} for key, value in ASSUME.items()}
    holds = [num(s.get("cargo_capacity")) for s in ships if num(s.get("cargo_capacity")) > 0]
    if holds:
        out["cargo"] = {"value": int(statistics.median(holds)), "from": "median hold of %d ships" % len(holds)}
    clean = meters.get("clean") if isinstance(meters, dict) else None
    if isinstance(clean, list) and len(clean) == 4 and num(clean[0]) >= 20:
        out["fuel_price"] = {"value": round(clean[1] / clean[0], 2), "from": "the collector's meter, %d units bought" % clean[0]}
    rates = []
    by_route = defaultdict(lambda: [0.0, 0.0])
    for row in world["runs"]:
        if row.get("kind") == "mine" and num(row.get("minutes")) >= 10 and row.get("ore") is not None:
            by_route[row.get("route")][0] += num(row["ore"])
            by_route[row.get("route")][1] += num(row["minutes"])
    fields = {(f["system"], f["poi"]): f for f in world["fields"]}
    for rid, (ore, minutes) in by_route.items():
        belt = str((world["routes"].get(rid) or {}).get("belt") or "")
        field = fields.get(tuple(belt.split(":"))) if belt.count(":") == 1 else None
        rich = sum(r["richness"] for r in field["resources"] if r["remaining"] > 0) if field else 0
        if rich and ore and minutes >= 60:
            rates.append(ore / minutes / rich)
    if rates:
        out["mine_rate"] = {"value": round(statistics.median(rates), 4), "from": "the mine runs of %d routes, the haul of one jump included" % len(rates)}
    return out


def refresh_catalog(data, now, fetch=None):
    """Fetch the game's catalog once a day into data/catalog/<version>.json; returns what it did, in a word."""
    folder = Path(data) / "catalog"
    newest = newest_catalog(data)
    if newest.exists() and now - newest.stat().st_mtime < CATALOG_EVERY:
        return "fresh"
    try:
        if fetch is None:
            with urllib.request.urlopen(urllib.request.Request(CATALOG_URL, headers={"User-Agent": "the-collective-routemaker"}), timeout=60) as answer:
                raw = answer.read(60_000_000)
        else:
            raw = fetch()
        catalog = json.loads(raw.decode("utf-8"))
        version = "".join(c for c in str(catalog.get("version") or "unknown") if c.isalnum() or c in ".-")[:20] or "unknown"
        folder.mkdir(parents=True, exist_ok=True)
        tmp = folder / (".%s.%d.tmp" % (version, os.getpid()))
        tmp.write_bytes(raw)
        os.replace(tmp, folder / (version + ".json"))
        return "fetched " + version
    except Exception as error:                                # no catalog is no reason to stop: the last one is used
        return "not fetched: %s" % type(error).__name__


# ---------------------------------------------------------------- the candidates

def value(world, key):
    return world["assume"][key]["value"]


def trip(world, jumps, legs=2, docks=1):
    """(minutes, fuel credits) of a round trip of `jumps` jumps each way, with flights inside a system and stops."""
    minutes = 2 * jumps * value(world, "jump_minutes") + legs * value(world, "leg_minutes") + docks * value(world, "dock_minutes")
    fuel = (2 * jumps * value(world, "fuel_per_jump") + legs * value(world, "fuel_per_leg")) * value(world, "fuel_price")
    return minutes, fuel


def warn_age(world, stamp, what, warnings):
    age = age_of(stamp, world["now"])
    if age is None or age > STALE:
        warnings.append("%s is stale (read %s)" % (what, stamp or "never"))


def lawless(world, system):
    return system not in world.get("policed", ())


def ladder(world, base, item, side):
    """The price levels [[price, units], ...] of one side of an item's book, best first; None when no fresh read holds them."""
    entry = ((world["ladders"].get(base) or {}).get(item) or {})
    if not entry or world["now"] - num(entry.get("t")) > LADDER_FRESH:
        return None
    return entry.get(side) or []


def want_ladder(world, base, item, worth):
    """Note that a candidate would like this book read level by level; `worth` ranks the wishes."""
    key = (base, item)
    world["wanted"][key] = max(world["wanted"].get(key, 0), worth)


def sell_into(world, base, item, units):
    """(units sold, credits, how the depth is known) for selling into a station's bids, never below 80% of the best bid."""
    row = (world["books"].get(base) or {"items": {}})["items"].get(item)
    if not row or row["bid"] <= 0 or units <= 0:
        return 0, 0.0, "no bid"
    levels = ladder(world, base, item, "bids")
    if levels is not None:
        sold, income = 0.0, 0.0
        for price, qty in levels:
            if price < 0.8 * levels[0][0] or sold >= units:
                break
            take = min(qty, units - sold)
            sold, income = sold + take, income + take * price
        return sold, income, "price levels read"
    want_ladder(world, base, item, min(units, max(row["bid_qty"], 1) * 50) * row["bid"])
    if row["bid_depth_known"]:
        sold = min(units, row["bid_qty"])
        return sold, sold * row["bid"], "depth at the best price"
    return min(units, 1), min(units, 1) * row["bid"], "one unit: the saved book has no depth"


def buy_from(world, base, item, units):
    """(units bought, credits before tax, how the depth is known) for buying a station's offers, never above 120% of the best offer."""
    row = (world["books"].get(base) or {"items": {}})["items"].get(item)
    if not row or row["ask"] <= 0 or units <= 0:
        return 0, 0.0, "no offer"
    levels = ladder(world, base, item, "asks")
    if levels is not None:
        got, cost = 0.0, 0.0
        for price, qty in levels:
            if price > 1.2 * levels[0][0] or got >= units:
                break
            take = min(qty, units - got)
            got, cost = got + take, cost + take * price
        return got, cost, "price levels read"
    want_ladder(world, base, item, min(units, max(row["ask_qty"], 1)) * row["ask"])
    got = min(units, row["ask_qty"])
    return got, got * row["ask"], "depth at the best price"


def read_ladder(pilot, item):
    """One item's book, level by level, through a pilot docked at the station: ({"bids": [...], "asks": [...]} or None)."""
    body = {"toolGroup": "spacemolt_market", "action": "view_market", "params": {"item_id": item}}
    request = urllib.request.Request(GATE + "/accounts/%s/raw" % urllib.parse.quote(pilot, safe=""), data=json.dumps(body).encode(),
                                     method="POST", headers={"Content-Type": "application/json"})
    try:
        with OPENER.open(request, timeout=60) as answer:
            found = json.loads(answer.read().decode("utf-8", "replace") or "{}")
    except (OSError, ValueError):
        return None
    content = found.get("structuredContent") if isinstance(found, dict) else None
    rows = (content or {}).get("items") if isinstance(content, dict) else None
    if not rows or not isinstance(rows[0], dict):
        return None
    levels = lambda side: [[num(o.get("price_each") or o.get("price")), num(o.get("quantity"))] for o in rows[0].get(side) or []
                           if isinstance(o, dict) and num(o.get("price_each") or o.get("price")) > 0 and num(o.get("quantity")) > 0]
    return {"bids": sorted(levels("buy_orders"), reverse=True)[:40], "asks": sorted(levels("sell_orders"))[:40]}


def fetch_ladders(world, data, look=read_ladder, pause=1.1):
    """Read the most wanted books level by level, at most LADDER_READS, and save them; the number read."""
    wishes = sorted(world["wanted"].items(), key=lambda kv: -kv[1])
    done = 0
    for (base, item), _worth in wishes:
        pilot = world["docked"].get(base)
        if done >= LADDER_READS or not pilot:
            continue
        found = look(pilot, item)
        if found is not None:
            world["ladders"].setdefault(base, {})[item] = dict(found, t=int(world["now"]))
            done += 1
        time.sleep(pause)
    if done:
        for base in list(world["ladders"]):                    # drop what nobody asked for in a day
            world["ladders"][base] = {i: e for i, e in world["ladders"][base].items() if world["now"] - num(e.get("t")) < 24 * 3600}
        path = Path(data) / "market" / "ladders.json"
        tmp = path.with_name("%s.%d.tmp" % (path.name, os.getpid()))
        tmp.write_text(json.dumps(world["ladders"], separators=(",", ":")), encoding="utf-8")
        os.replace(tmp, path)
    return done


def best_bids(world, item):
    """[(bid, depth at that price, base)] for an item, best first."""
    out = [(row["bid"], row["bid_qty"], base) for base, book in world["books"].items() for row in [book["items"].get(item)] if row and row["bid"] > 0]
    return sorted(out, reverse=True)


def existing(world, kind, **match):
    """The id of a route file that already flies this, or ''."""
    for rid, route in world["routes"].items():
        if route.get("kind") == kind and all(route.get(k) == v for k, v in match.items()):
            return rid
    return ""


def status_of(world, rid):
    """('in the plan of <roles>' | 'route file exists' | 'new', the route's measured figure or None)."""
    if not rid:
        return "new", None
    route = world["routes"].get(rid) or {}
    roles = sorted(role for role, ids in world["plans"].items() if rid in ids)
    state = ("off, " if route.get("status") == "off" else "") + ("in the plan of " + ", ".join(roles) if roles else "route file exists, in no plan")
    return state, (route.get("measured") or {}).get("cph_per_ship")


def candidate(world, cid, kind, title, per_hour, per_run, minutes, basis, warnings, route=None, needs="", rid="", extra=None):
    state, measured = status_of(world, rid)
    out = {"id": cid, "kind": kind, "role": ROLE[kind], "title": title, "per_ship_hour": int(round(per_hour)), "per_run": int(round(per_run)),
           "minutes": round(minutes, 1), "basis": basis, "warnings": warnings, "status": state, "route_id": rid, "measured": measured}
    if route:
        out["route"] = route
    if needs:
        out["needs"] = needs
    out.update(extra or {})
    return out


def mine_candidates(world):
    """Each field, sold whole at the station that pays most for what it yields."""
    out, cargo, rate = [], value(world, "cargo"), value(world, "mine_rate")
    for field in world["fields"]:
        live = [r for r in field["resources"] if r["remaining"] >= 100 and r["richness"] > 0]
        rich = sum(r["richness"] for r in live)
        if not rich:
            continue
        best = None
        for base, station in world["stations"].items():
            book = world["books"].get(base)
            jumps = world["chart"].jumps(field["system"], station["system"])
            if not book or jumps is None:
                continue
            income, parts, thin, floors = 0.0, [], [], []
            for res in live:
                units = cargo * res["richness"] / rich
                sold, got, how = sell_into(world, base, res["id"], units)
                if sold <= 0:
                    continue
                income += got
                floors.append({"item": res["id"], "min_price": max(1, int(0.8 * got / sold))})
                parts.append("%s %d of %d units for %d cr (%s)" % (res["id"], sold, units, got, how))
                if sold < units:
                    thin.append("%s: the bids take %d of %d units a load" % (res["id"], sold, units))
            minutes, fuel = trip(world, jumps)
            minutes += cargo / (rate * rich)
            loads = 60 / minutes                              # an hour of mining, sold down the book
            per_hour = -fuel * loads
            for res in live:
                hour = loads * cargo * res["richness"] / rich
                sold, got, _how = sell_into(world, base, res["id"], hour)
                per_hour += got
                if 0 < sold < 0.99 * hour:
                    thin.append("%s: the bids take %d of the %d units an hour brings" % (res["id"], sold, hour))
            if income > 0 and (best is None or per_hour > best[0]):
                best = (per_hour, income - fuel, minutes, base, jumps, parts, thin, floors)
        if best is None:
            continue
        per_hour, per_run, minutes, base, jumps, parts, thin, floors = best
        station = world["stations"][base]
        warnings = list(thin)
        low = [r["id"] for r in live if r["remaining"] < 10 * cargo * r["richness"] / rich]
        if low:
            warnings.append("nearly mined out: %s hold fewer than ten loads" % ", ".join(low))
        warn_age(world, field["read_at"], "the field's reading", warnings)
        warn_age(world, world["books"][base]["read_at"], "the order book of %s" % base, warnings)
        if lawless(world, field["system"]):
            warnings.append("lawless space: no police at %s" % field["system"])
        tool = HARVESTER.get(field["type"])
        if tool:
            price = num((world["items"].get(tool) or {}).get("base_value"))
            warnings.append("needs the module %s%s, not the mining laser; the rate is measured with the laser on ore" % (tool, " (base value %d cr)" % price if price else ""))
        rid = existing(world, "mine", belt="%s:%s" % (field["system"], field["poi"]), station=station["at"])
        cid = "mine-%s" % field["poi"].replace("_", "-")
        route = {"id": cid, "kind": "mine", "title": "%s: %s; sold at %s" % (field["name"], ", ".join(r["id"] for r in live), station["name"]),
                 "note": "Written by routemaker.py from the field's and the book's readings; an estimate of %d cr per ship-hour, not a measurement. A test: one ship."
                         % per_hour, "belt": "%s:%s" % (field["system"], field["poi"]), "station": station["at"], "minutes": int(max(30, min(90, 2 * minutes))), "max_ships": 1,
                 "sell": floors}
        if tool:
            route["requires"] = {"module": tool}
        if lawless(world, field["system"]):
            route.setdefault("requires", {})["empty_hold"] = True
        out.append(candidate(world, cid, "mine", route["title"], per_hour, per_run, minutes,
                             {"field": "%s:%s" % (field["system"], field["poi"]), "richness": {r["id"]: r["richness"] for r in live},
                              "left": {r["id"]: r["remaining"] for r in live}, "sold_at": base, "jumps": jumps, "a_load": parts},
                             warnings, route=route, rid=rid))
    return out


def trade_candidates(world):
    """An item on offer at one station and bid for at another, capped by both depths, the hold and the tax."""
    out, cargo, tax = [], value(world, "cargo"), value(world, "tax")
    for a, book_a in world["books"].items():
        for item, ask in book_a["items"].items():
            if ask["ask"] <= 0 or ask["ask_qty"] <= 0:
                continue
            for bid_price, bid_qty, b in best_bids(world, item):
                if b == a or bid_price <= ask["ask"] * (1 + tax):
                    continue
                jumps = world["chart"].jumps(book_a["system"], world["books"][b]["system"])
                if jumps is None:
                    continue
                size = max(1, num((world["items"].get(item) or {}).get("size")) or 1)
                hold = cargo // size
                got, cost, how_buy = buy_from(world, a, item, hold)
                sold, income, how_sell = sell_into(world, b, item, got)
                if sold < got:                                # buy only what the bids take
                    got, cost, how_buy = buy_from(world, a, item, sold)
                units = int(min(got, sold))
                if units <= 0:
                    continue
                minutes, fuel = trip(world, jumps, legs=0, docks=2)
                profit = income - cost * (1 + tax) - fuel
                if profit <= 0:
                    continue
                again = buy_from(world, a, item, 2 * hold)[0] >= 2 * units and sell_into(world, b, item, 2 * hold)[0] >= 2 * units
                loads = 60 / minutes if again else 1
                warnings = ["bought: %s; sold: %s" % (how_buy, how_sell)]
                if not again:
                    warnings.append("one load of %d units closes the gap: costed as one load, not as an hour of loads" % units)
                warn_age(world, book_a["read_at"], "the order book of %s" % a, warnings)
                warn_age(world, world["books"][b]["read_at"], "the order book of %s" % b, warnings)
                cid = "trade-%s-%s-%s" % (item.replace("_", "-"), a.split("_")[0], b.split("_")[0])
                sa, sb = world["stations"].get(a), world["stations"].get(b)
                route = None
                if sa and sb:
                    route = {"id": cid, "kind": "circuit", "title": "%s: bought at %s for %d cr, sold at %s for %d cr" % (ask["name"], sa["name"], ask["ask"], sb["name"], bid_price),
                             "note": "Written by routemaker.py from two order books; %d units cost about %d cr. An estimate, not a measurement. A test: one ship; the buy and the "
                                     "sale carry price limits." % (units, cost), "max_ships": 1, "min_credits": int(cost * 1.1) + 3000,
                             "stops": [{"at": sa["at"], "buy": [{"item": item, "qty": units, "max_price": int(cost / units * 1.03) + 1}]},
                                       {"at": sb["at"], "sell": [{"item": item, "min_price": int(income / units * 0.9)}]}]}
                out.append(candidate(world, cid, "trade", "%s: %s -> %s" % (ask["name"], a, b), profit * loads, profit, minutes,
                                     {"item": item, "buy_at": a, "ask": ask["ask"], "sell_at": b, "bid": bid_price, "units": units, "paid": int(cost), "got": int(income),
                                      "jumps": jumps}, warnings, route=route, needs="" if route else "the stations' places are not scouted yet"))
                break                                         # the best bid for this offer is enough
    return out


def craft_candidates(world):
    """A hand recipe whose inputs are on offer at a station or lie in our storage there, its output sold into the best bid."""
    out, tax = [], value(world, "tax")
    for recipe in world["recipes"]:
        outputs = [o for o in recipe.get("outputs") or [] if isinstance(o, dict) and o.get("item_id")]
        inputs = [i for i in recipe.get("inputs") or [] if isinstance(i, dict) and i.get("item_id")]
        if len(outputs) != 1 or not inputs:
            continue
        made, per_batch = outputs[0]["item_id"], max(1, num(outputs[0].get("quantity")))
        bids = best_bids(world, made)
        if not bids:
            continue
        bid_price, bid_qty, sell_base = bids[0]
        for base, book in world["books"].items():
            stock = world["stock"].get(base) or {}
            cost, batches, parts, from_stock = 0.0, 50, [], 0
            for need in inputs:                               # how many batches the inputs allow
                item, qty = need["item_id"], max(1, num(need.get("quantity")))
                if num(stock.get(item)) >= qty:
                    batches = min(batches, num(stock.get(item)) // qty)
                else:
                    batches = min(batches, buy_from(world, base, item, 50 * qty)[0] // qty)
            batches = int(min(batches, sell_into(world, sell_base, made, 50 * per_batch)[0] // per_batch))
            if batches < 1:
                continue
            for need in inputs:
                item, qty = need["item_id"], max(1, num(need.get("quantity")))
                if num(stock.get(item)) >= qty * batches:
                    parts.append("%d %s from our storage" % (qty * batches, item))
                    from_stock += 1
                else:
                    got, paid, how = buy_from(world, base, item, qty * batches)
                    cost += paid * (1 + tax)
                    parts.append("%d %s for %d cr (%s)" % (got, item, paid, how))
            sold, income, how_sell = sell_into(world, sell_base, made, per_batch * batches)
            jumps = world["chart"].jumps(book["system"], world["books"][sell_base]["system"])
            if jumps is None:
                continue
            minutes, fuel = trip(world, jumps, legs=0, docks=2 if sell_base != base else 1)
            minutes += 5 + 0.5 * batches                       # the crafting queue: assumed, not measured
            total = income - cost - fuel
            profit = total / batches
            if total <= 0:
                continue
            warnings = ["one run of %d batch(es), costed once: %d %s sold for %d cr (%s)" % (batches, sold, made, income, how_sell),
                        "the runner has no craft step yet: flown by hand (gate.py raw, storage and craft)"]
            if from_stock:
                warnings.append("uses goods of our storage at %s: ask their Admiral" % base)
            warn_age(world, book["read_at"], "the order book of %s" % base, warnings)
            cid = "craft-%s-%s" % (str(recipe.get("id") or made).replace("_", "-")[:40], base.split("_")[0])
            out.append(candidate(world, cid, "craft", "%s at %s, sold at %s" % (recipe.get("name") or made, base, sell_base), total, total, minutes,
                                 {"recipe": recipe.get("id"), "at": base, "inputs": parts, "makes": "%d %s" % (per_batch * batches, made), "sold_at": sell_base,
                                  "batches": batches, "profit_a_batch": int(profit)}, warnings, needs="a craft step in the circuit runner"))
    return out


def loot_per_kill(world):
    """{species: ({item: units a kill}, median minutes a run, runs)} learned from the hunt runs whose route names one species."""
    seen = defaultdict(lambda: {"kills": 0, "goods": Counter(), "minutes": [], "runs": 0})
    for row in world["runs"]:
        route = world["routes"].get(row.get("route")) or {}
        species = route.get("species") or []
        if row.get("kind") == "hunt" and len(species) == 1 and num(row.get("kills")) > 0:
            entry = seen[species[0]]
            entry["kills"] += num(row["kills"])
            entry["runs"] += 1
            entry["minutes"].append(num(row.get("minutes")))
            for item, units in (row.get("goods") or {}).items():
                entry["goods"][item] += num(units)
    return {s: ({item: units / e["kills"] for item, units in e["goods"].items()}, statistics.median(e["minutes"]), e["runs"]) for s, e in seen.items()}


def hunt_candidates(world):
    """A herd of four or more grazers of 100 hull or less, of a species whose loot our own runs have sold."""
    out, learned = [], loot_per_kill(world)
    for herd in world["herds"]:
        for species, count in herd["species"].items():
            if count < 4 or herd["hull"].get(species, 999) > 100:
                continue
            place = "%s:%s" % (herd["system"], herd["poi"])
            rid = existing(world, "hunt", place=place)
            warnings = []
            warn_age(world, herd["read_at"], "the herd's count", warnings)
            if herd["pirates"]:
                warnings.append("%d pirate(s) were seen at this place" % herd["pirates"])
            if lawless(world, herd["system"]):
                warnings.append("lawless space: no police at %s" % herd["system"])
            cid = "hunt-%s-%s" % (herd["poi"].replace("_", "-"), species.replace("_", "-"))
            if species not in learned:
                out.append(candidate(world, cid, "hunt", "%d %s at %s: what a kill yields is not known" % (count, species, place), 0, 0, 0,
                                     {"place": place, "herd": count, "hull": herd["hull"].get(species)}, warnings + ["no run of ours has sold this species' loot"],
                                     needs="one test hunt (orders F9): what it drops and what the drop sells for", rid=rid))
                continue
            drops, run_minutes, runs = learned[species]
            best = None
            for base, station in world["stations"].items():
                jumps = world["chart"].jumps(herd["system"], station["system"])
                book = world["books"].get(base)
                if jumps is None or not book:
                    continue
                kills = 4
                income, parts, floor = 0.0, [], 0
                for item, per_kill in drops.items():
                    sold, got, how = sell_into(world, base, item, kills * per_kill)
                    if sold > 0:
                        income += got
                        parts.append("%s %.1f units for %d cr (%s)" % (item, sold, got, how))
                        floor = max(floor, int(got / sold * 0.8))
                minutes, fuel = trip(world, jumps)
                minutes += max(8.0, run_minutes - 7)           # the fight and the looting: a measured run less its own short trip
                per_hour = 60 * (income - fuel) / minutes
                if income > 0 and (best is None or per_hour > best[0]):
                    best = (per_hour, income - fuel, minutes, base, jumps, parts, floor)
            if best is None:
                continue
            per_hour, per_run, minutes, base, jumps, parts, floor = best
            station = world["stations"][base]
            route = {"id": cid, "kind": "hunt", "title": "%s at %s; loot sold at %s" % (species, herd["poi"], station["name"]),
                     "note": "Written by routemaker.py from the herd's count, the loot of %d runs of ours and the order book; an estimate of %d cr per hunter-hour, not a "
                             "measurement. A test: one ship, the ranching rules kept." % (runs, per_hour),
                     "place": place, "species": [species], "sell_at": station["at"], "min_bid": floor, "kills": 4, "minutes": int(max(40, minutes + 15)),
                     "max_ships": 1, "min_creatures": 4}
            if lawless(world, herd["system"]):               # beyond the police: no fight beside a foreign ship, nothing to lose aboard
                route.update({"alone": True, "requires": {"empty_hold": True}})
            out.append(candidate(world, cid, "hunt", route["title"], per_hour, per_run, minutes,
                                 {"place": place, "herd": count, "hull": herd["hull"].get(species), "loot_a_kill": {k: round(v, 2) for k, v in drops.items()},
                                  "learned_from_runs": runs, "sold_at": base, "jumps": jumps, "four_kills": parts}, warnings, route=route, rid=rid))
    return out


def herds_named_in(world, text):
    """Where our readings saw a species that a catalog text names, as 'N <species> at <system>:<poi>' (the three largest herds)."""
    text = text.lower()
    found = []
    for herd in world["herds"]:
        for species, count in herd["species"].items():
            if species.replace("_", "-") in text or species.replace("_", " ") in text:
                found.append((count, "%d %s at %s:%s" % (count, species, herd["system"], herd["poi"])))
    return [line for _count, line in sorted(found, reverse=True)[:3]]


def herds_for(world, text, kills, system):
    """[(jumps, creatures, species, system, poi)] of the herds a text names that hold prey of 100 hull or less for `kills`
    kills and two to spare, no pirate seen there: policed space first, then the nearest, then the largest."""
    low, found = text.lower(), []
    for herd in world["herds"]:
        for species, count in herd["species"].items():
            jumps = world["chart"].jumps(system, herd["system"])
            if ((species.replace("_", "-") in low or species.replace("_", " ") in low) and count >= kills + 2
                    and herd["hull"].get(species, 999) <= 100 and jumps is not None and not herd["pirates"]):
                found.append((lawless(world, herd["system"]), jumps, -count, species, herd["system"], herd["poi"]))
    return [(jumps, -count, species, where, poi) for _far, jumps, count, species, where, poi in sorted(found)]


def mission_candidates(world):
    """Every mission on a board: what it pays, what it asks for, what that costs, and how many of our pilots have not booked it."""
    out, seen = [], set()
    known_routes = {}
    for rid, route in world["routes"].items():
        for stop in route.get("stops") or []:
            for accept in stop.get("accept") or []:
                known_routes[accept.get("template") if isinstance(accept, dict) else accept] = rid
    for base, board in world["boards"].items():
        giver = world["stations"].get(base)
        for mission in board["missions"]:
            reward = num((mission.get("rewards") or {}).get("credits"))
            key = (mission.get("template_id") or mission.get("title"), base if not mission.get("template_id") else "")
            if reward <= 0 or key in seen:
                continue
            seen.add(key)
            cost, jumps_total, asks, blockers, stops, hunt_minutes = 0.0, 0, [], [], [], 0.0
            here = board["system"]
            for goal in mission.get("objectives") or []:
                kind, item, qty = goal.get("type"), goal.get("item_id"), max(1, num(goal.get("quantity")))
                target = goal.get("system_id")
                if kind in ("deliver_item", "sell_item"):
                    offers = sorted((row["ask"], b) for b, bk in world["books"].items() for row in [bk["items"].get(item)] if row and row["ask"] > 0 and row["ask_qty"] >= qty)
                    held = sorted(((num((world["stock"].get(b) or {}).get(item)), b) for b in world["stock"]), reverse=True)
                    if offers:
                        cost += qty * offers[0][0] * (1 + value(world, "tax"))
                        asks.append("%d %s: on offer at %s for %d cr" % (qty, item, offers[0][1], offers[0][0]))
                        stops.append(("buy", offers[0][1], item, qty, offers[0][0]))
                    elif held and held[0][0] >= qty:
                        asks.append("%d %s: %d lie in our storage at %s" % (qty, item, held[0][0], held[0][1]))
                        blockers.append("a withdraw step: the goods lie in storage")
                    else:
                        full = " ".join(str((world["items"].get(item) or {}).get("description") or "").split())
                        herds = herds_named_in(world, full)
                        asks.append("%d %s: no seller in our books%s%s" % (qty, item, ". The catalog: " + full[:150] if full else "",
                                                                         ". Seen: " + "; ".join(herds) if herds else ""))
                        blockers.append("a source of %s%s" % (item, " (a hunt: the herd is known)" if herds else ""))
                    if goal.get("target_base_id"):
                        stops.append(("deliver", goal["target_base_id"], item, qty, 0))
                elif kind == "mine_resource":
                    fields = [f for f in world["fields"] if any(r["id"] == item and r["remaining"] >= qty for r in f["resources"])]
                    asks.append("mine %d %s: %s" % (qty, item, ("at %s:%s" % (fields[0]["system"], fields[0]["poi"])) if fields else "no field with it in our readings"))
                    if not fields:
                        blockers.append("a field with %s" % item)
                elif kind == "kill_creature":
                    text = str(goal.get("description") or "kill %d" % qty)
                    spots = herds_for(world, text, qty, board["system"])
                    asks.append(text + (". Herds: " + "; ".join("%d %s at %s:%s" % (s[1], s[2], s[3], s[4]) for s in spots[:4]) if spots else ""))
                    if spots:
                        stops.append(("hunt", "%s:%s" % (spots[0][3], spots[0][4]), spots[0][2], qty, 0))
                        jumps_total += 2 * spots[0][0]
                        hunt_minutes += 5.0 * qty + 2 * value(world, "leg_minutes")     # about five minutes a kill: two hand runs of 2026-11-15
                    else:
                        blockers.append("a herd of four or more for: %s" % text[:60])
                elif kind in ("visit_system", "survey_system", "dock_at_base"):
                    asks.append(str(goal.get("description") or kind))
                    if kind == "survey_system":
                        blockers.append("a survey scanner")
                    if kind == "visit_system":
                        blockers.append("a visit step in the circuit runner")
                    if kind == "dock_at_base":
                        if goal.get("target_base_id") in world["stations"]:
                            stops.append(("dock", goal["target_base_id"], "", 0, 0))
                        else:
                            blockers.append("the place of the station %s" % goal.get("target_base_id"))
                else:
                    asks.append(str(goal.get("description") or kind))
                    blockers.append("a runner step for `%s`" % kind)
                if target:
                    hop = world["chart"].jumps(here, target)
                    if hop is None:
                        blockers.append("a charted way to %s" % target)
                    else:
                        jumps_total += hop
                        here = target
            back = world["chart"].jumps(here, board["system"]) or 0
            jumps = jumps_total + back
            minutes = jumps * value(world, "jump_minutes") + (2 + len(stops)) * value(world, "dock_minutes") + 5 + hunt_minutes
            fuel = jumps * value(world, "fuel_per_jump") * value(world, "fuel_price")
            net = reward - cost - fuel
            title = str(mission.get("title") or mission.get("template_id") or "mission")
            names = {title.lower(), str(mission.get("template_id") or "").lower()} - {""}
            done = len(set().union(*(world["booked"].get(n, set()) for n in names))) if names else 0
            fixed = bool(mission.get("template_id"))
            warnings = ["whether it pays again for the same pilot is not known"] if fixed else ["a mission the station made up: it may be gone at the next read"]
            warn_age(world, board["read_at"], "the board of %s" % base, warnings)
            if jumps > 12:
                warnings.append("a long way: %d jumps there and back, beyond the systems the orders name" % jumps)
            rid = known_routes.get(mission.get("template_id")) or ""
            cid = "mission-%s-%s" % (str(mission.get("template_id") or title).lower().replace("_", "-").replace(" ", "-")[:44], base.split("_")[0])
            route = None
            buys = [s for s in stops if s[0] == "buy"]
            drops = [s for s in stops if s[0] in ("deliver", "dock")]
            hunts = [s for s in stops if s[0] == "hunt"]
            flyable = all(g.get("type") in ("deliver_item", "dock_at_base", "kill_creature") for g in mission.get("objectives") or [])
            if fixed and giver and not blockers and flyable and (drops or hunts) and all(world["stations"].get(s[1]) for s in buys + drops):
                plan = []
                for _, where, item, qty, price in buys:
                    plan.append({"at": world["stations"][where]["at"], "skip_if_hold": {item: qty}, "buy": [{"item": item, "qty": qty, "max_price": int(price * 1.15) + 1, "one_time": True}]})
                plan.append({"at": giver["at"], "accept": [{"template": mission["template_id"], "needs": {s[2]: s[3] for s in buys}}] if buys else [mission["template_id"]]})
                if hunts:
                    plan[-1]["hunt"] = [dict({"at": place, "species": [species], "kills": kills, "minutes": 35, "for": [title]},
                                             **({"alone": True} if lawless(world, place.split(":")[0]) else {}))
                                        for _, place, species, kills, _price in hunts]
                for _, where, _item, _qty, _price in drops:
                    plan.append({"at": world["stations"][where]["at"], "redock": True})
                if hunts or plan[-1]["at"] != giver["at"]:
                    plan.append({"at": giver["at"]})
                route = {"id": cid, "kind": "circuit", "title": "%s: %d cr at %s" % (title, reward, giver["name"]),
                         "note": "Written by routemaker.py from the board and the order books: goods for about %d cr, reward %d cr. A test: one ship; whether the mission "
                                 "hands its goods out at the accept is not known until one accept with an empty hold." % (cost, reward),
                         "once": True, "max_ships": 1, "one_time": [title], "skip_if_booked": [title], "stops": plan}
                if cost:
                    route["min_credits"] = int(cost) + 3000
            out.append(candidate(world, cid, "mission", "%s (%s)" % (title, base), 60 * net / max(minutes, 1), net, minutes,
                                 {"board": base, "reward": reward, "asks": asks, "goods_cost": int(cost), "jumps": jumps}, warnings, route=route,
                                 needs="; ".join(sorted(set(blockers))), rid=rid,
                                 extra={"pilots_booked": done, "pilots_open": max(0, world["pilots"] - done) if fixed else None,
                                        "open_credits": int(max(0, world["pilots"] - done) * net) if fixed and net > 0 else None}))
    return out


def build(data, root, now, policed=None, look=None):
    """One pass: the list of candidates and what it rests on. With `look`, the books the best candidates rest on are
    read level by level first (through docked pilots), and the list is made again from them."""
    def candidates(world):
        rows = mine_candidates(world) + trade_candidates(world) + craft_candidates(world) + hunt_candidates(world) + mission_candidates(world)
        rows.sort(key=lambda c: (-c["per_ship_hour"], c["id"]))
        seen, out = set(), []
        for row in rows:                                      # one candidate per id: the best
            if row["id"] not in seen:
                seen.add(row["id"])
                out.append(row)
        return out

    world = load_world(data, root, now)
    world["policed"] = policed if policed is not None else policed_systems(root)
    rows, read = candidates(world), 0
    if look is not None and world["wanted"]:
        read = fetch_ladders(world, data, look)
        world["wanted"] = {}
        rows = candidates(world)
    return {"written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)), "what": "Ways to earn, computed from the fleet's own readings; estimates until flown",
            "ammo": sorted(i for i, item in world["items"].items() if item.get("category") == "ammo"),
            "assumptions": world["assume"], "catalog": world["catalog_version"], "ladders_read": read,
            "read": {"fields": len(world["fields"]), "order_books": len(world["books"]), "boards": len(world["boards"]), "herds": len(world["herds"]),
                     "recipes": len(world["recipes"]), "runs": len(world["runs"])},
            "candidates": rows}


def policed_systems(root):
    """The systems of an empire on the chart: police there."""
    out = set()
    try:
        lines = (Path(root) / "map" / "galaxy.tsv").read_text(encoding="utf-8").splitlines()
    except OSError:
        return out
    rows = [l.split("\t") for l in lines if l and not l.startswith("#")]
    head = {name: n for n, name in enumerate(rows[0])} if rows else {}
    for row in rows[1:]:
        if "empire" in head and len(row) > head["empire"] and row[head["empire"]] not in ("-", ""):
            out.add(row[head["id"]])
    return out


# ---------------------------------------------------------------- the command line

def show(book, who, kind, top):
    kinds = (kind,) if kind else (MEMBER_KINDS.get(who) or MEMBER_KINDS["Unity"])
    read = book.get("read") or {}
    print("WAYS TO EARN | computed %s from %s fields, %s order books, %s boards, %s herds, %s hand recipes | estimates, not measurements" % (
        book.get("written_at"), read.get("fields"), read.get("order_books"), read.get("boards"), read.get("herds"), read.get("recipes")))
    for name in kinds:
        rows = [c for c in book.get("candidates") or [] if c["kind"] == name]
        rows.sort(key=lambda c: -(c.get("open_credits") or 0) if name == "mission" else -c["per_ship_hour"])
        print("%s: %d candidate(s)%s" % (name.upper(), len(rows), ", best %d" % top if len(rows) > top else ""))
        for c in rows[:top]:
            fig = "%+7d cr/ship-hour" % c["per_ship_hour"] if c["per_ship_hour"] else "   not known       "
            if name == "mission":
                fig = "%+6d cr net, open for %s pilot(s)" % (c["per_run"], c.get("pilots_open") if c.get("pilots_open") is not None else "?")
            line = "  %s | %-34s | %s | %s" % (fig, c["status"][:34], c["id"], c["title"][:80])
            print(line)
            if c.get("measured") is not None:
                print("      measured: %+d cr per ship-hour (the route %s)" % (c["measured"], c["route_id"]))
            if c.get("needs"):
                print("      needs: %s" % c["needs"])
            for warning in c["warnings"][:3]:
                print("      ! %s" % warning)
    print("Assumed where nothing measures it: " + "; ".join("%s %s (%s)" % (k, v["value"], v["from"]) for k, v in sorted((book.get("assumptions") or {}).items())))
    print("A candidate's route file: routemaker.py route <id>. Test it with one ship before it enters a plan (game/routes/BLUEPRINT.md, rule 2).")


def main():
    args = sys.argv[1:]
    data = args[args.index("--data") + 1] if "--data" in args else division.DATA
    flag = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    rest = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--data", "--kind", "--top"))]
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    path = Path(data) / "routes" / "opportunities.json"
    if rest and rest[0] in ("show", "route"):
        book = read_json(path, None) or build(data, ROOT, time.time())
        if rest[0] == "show":
            who = (rest[1] if len(rest) > 1 else division.member()[1] or "Unity").capitalize()
            show(book, "Unity" if who == "All" else who, flag("--kind", ""), int(flag("--top", "8")))
            return 0
        found = next((c for c in book.get("candidates") or [] if len(rest) > 1 and c["id"] == rest[1]), None)
        if not found:
            sys.exit("routemaker.py: no candidate `%s`; `routemaker.py show all` lists them" % (rest[1] if len(rest) > 1 else ""))
        print("# %s | estimate %+d cr per ship-hour, %+d cr a run of %.0f minutes | %s" % (found["title"], found["per_ship_hour"], found["per_run"], found["minutes"], found["status"]))
        print("# rests on: " + json.dumps(found["basis"]))
        for warning in found["warnings"]:
            print("# ! " + warning)
        if found.get("needs"):
            print("# needs: " + found["needs"])
        if found.get("route"):
            print(json.dumps(found["route"], indent=1))
        else:
            print("# no route file: the runners cannot fly this yet")
        return 0
    if rest:
        sys.exit(__doc__)
    kind, name = division.member()
    once = "--once" in args
    if not once and kind != "service":
        sys.exit("REFUSED: the loop is the service's; `routemaker.py --once` makes one pass, `routemaker.py show` reads the list")
    while True:
        try:
            now = time.time()
            fetched = refresh_catalog(data, now)
            book = build(data, ROOT, now, look=read_ladder)
            ammo = Path(data) / "catalog" / "ammo.json"       # what counts as ammunition, for the dispatcher's `empty_hold`
            if book["ammo"] and read_json(ammo, None) != book["ammo"]:
                tmp = ammo.with_name("%s.%d.tmp" % (ammo.name, os.getpid()))
                tmp.write_text(json.dumps(book["ammo"]), encoding="utf-8")
                os.replace(tmp, ammo)
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_name("%s.%d.tmp" % (path.name, os.getpid()))
            tmp.write_text(json.dumps(book, separators=(",", ":")), encoding="utf-8")
            os.replace(tmp, path)
            print(book["written_at"], "candidates: %s | books read level by level: %d | catalog %s" % (
                dict(Counter(c["kind"] for c in book["candidates"])), book["ladders_read"], fetched), flush=True)
        except Exception as error:                            # a bad file must not end the service
            print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pass failed: %s: %s" % (type(error).__name__, error), flush=True)
        if once:
            return 0
        time.sleep(EVERY)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
