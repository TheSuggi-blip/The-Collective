#!/usr/bin/env python3
"""fill.py -- keep every ship of a division at work: say why ships wait, and fill the plan with the work that stands open.

WHAT: the dispatcher gives a free pilot the first route of its own list that is open to it (its division's plan
      file, plan.py: the list First, its own routes, the list Then). A ship waits (docked, costing nothing) when
      every route of its list is closed to it. This script reads the files the dispatcher
      reads and uses the dispatcher's own rule (dispatch.why_not), so the two cannot disagree. It
        status   per role: how many ships work, start and wait; for every route of the plan why it is closed to
                 the waiting pilots; then the work outside the plan: route files measured above zero with a free
                 place, the route maker's candidates with a ready route file, and what closes the rest
        check    the gate: no ship is idle (Suggi, 2026-11-16). PASS: no ship of the role waits. HALT (exit 1): ships
                 wait; the line says whether paying work or a test stands open (fill adds it) or whether the plan
                 lacks standing work for them (a route that trains or gathers: routes.py `standing`)
        fill     puts that work into the division's plan file: a mission that pays once into the list First, a
                 paying route into the own routes of the ships it is open to, then up to --tests tests of one ship
                 each. With --write it writes the route files and the plan (plan.py), rebuilds the index
                 files, runs the route gate and commits by path as the member
        add, drop, lift   one change: a route into a plan's list Then (--first: at the head of First), a route out
                 of a plan everywhere, or a route's `max_ships`; gated and committed the same way
RULES:
  - A member changes the plans of its own roles only; the Fleet Admiral any (orders F1).
  - Nothing is written while game/routes/ holds a change that is not committed, or while fleet/STOP exists.
  - It moves no ship: the dispatcher does, within the minute after the commit.
  - A test is the candidate's own route file: one ship, the limits the route maker wrote. A candidate that needs
    what no waiting pilot has (a module, a step no runner flies) is listed with what it needs and never added.
  - A route counts as paying from two measured runs. A candidate whose route buys goods is never added by itself:
    a gap is flown once by hand with one load. The dispatcher closes any route that lost money over two runs.
  - How many ships a route carries is read before it is lifted (Suggi, 2026-11-16: never all ships on one route):
    `carries` counts what its bid, its field or its herd regains per hour, and apart from that what today's standing
    order holds; `hive.py standing` prints both for every route of a plan, and `lift` refuses more ships than the two
    together carry.
  - A ship on standing work counts as free for paying work and for tests: `status` lists what stands open to it
    outside its plan, `fill` puts it in front of its own routes, and the gate's PASS line names it.
  - Standing work of a plan that is full while ships of the role wait is lifted by `fill` itself, by as many places as
    ships wait and never past what its field carries (carries(): what grows back, and what lies above its floor for one
    turn). 2026-11-16: three times in one evening the gate said HALT until a shared gather route was lifted by hand.
    A route that sells is never lifted by the script: what a bid carries is its Admiral's to weigh. Nor is a route
    beyond the border (rule F13: its Admiral weighs what a lost ship costs): on 2026-11-17 the script raised a one-ship
    test at a lawless belt to 4 ships and a lawless gather route from 7 to 20 within ten minutes of its install.
  - `lift_to` in a route file is its Admiral's word for how far the script may lift that route, beyond the border too:
    never past it, and never past what the field carries. A route beyond the border without it is not lifted.
  - The fallback, behind the switch file data/fleet/fallback-on: a role whose ships wait while nothing of its plan is
    open or can be lifted is lent standing work of other plans, into its list Then: a mine route in home space that
    sells nothing, that a waiting ship can fly and whose field carries more ships; two routes a pass at most. Its
    Admiral reorders or drops them. 2026-11-17 03:09 UTC: 68 ships waited eight minutes for a hand, because two plans
    lacked the shared routes that had room. Only a route of the role's own class is lent (rule F23, workclass.own):
    a gather route to miners alone, unless its file's `open_to` names the role.
  - Rule F23, each class flies its own work (workclass.py; Suggi, 2026-11-18: "Ore is miners job"): a route outside
    the role's own class is never offered, added as a paying route or a test, lent, or lifted for the role's waiting
    ships by this script; it is listed under `class: <class> is <roles>' work`. A mission that pays once, selling or
    crafting a ship's own stores and fitting stay every role's. `add` of such a route prints a note and adds it (the
    Admiral's own word): the dispatcher refuses it to the role's ships while data/fleet/class-guard-on exists; the
    route file's `open_to` is the way to open it to another class. 2026-11-17: the fallback lent the miners' iron
    routes to traders, haulers, drones and scouts, who gathered iron for hours after the reserve's iron was met.
  - A test goes to a ship of the caller's own roles only: the Fleet Admiral's hourly job gives tests to the command
    group, and each Admiral chooses the tests of its ships (2026-11-17: tests the job put on miners, haulers and drones
    were taken off by their Admirals turn after turn).
  - `fill --once` adds only missions that pay once and buy nothing: the five-minute job runs it for every role, so a
    new once route reaches every plan without waiting for a turn (requests ENT-144).
  - A list of the route maker older than an hour is no ground for PASS while ships wait: the gate says so. A list
    older than OFFER_STALE (a day) offers no test at all: its figures are from before (Zero, Apophis, 2026-11-21: after
    the pause the filler offered tests from a list 5,429 minutes old; DECISIONS Q75 (2)).
  - Never offered or added (Q75 (2)): a route set `off` (its own file), or a route or a test whose place is the place of
    a route set off for danger (`danger:` in its note: rule F27), one another division claims (admirals.log, claims in
    force until released: comms.claims_in_force), one of another class (workclass.own). Each such refusal is printed
    once in a call, with its reason (`not offered: <route>: <reason>`).
  - A hunt (a hunt route, or a circuit with a stop that hunts) is offered and added outside the plan only to a role that
    hunts (HUNTERS, rule F16: Military and Intel hunt, Mining, Trade and Logistics earn; one hunter per herd, rule F9). A
    mission that pays once per pilot is every pilot's, its first hunt too, and what an Admiral put into its own plan
    stays (Zero, report of 2026-11-16: the gate offered Intel's herd to a miner).
WHY:  a plan of one-ship tests and routes that pay once left 102 of 146 ships docked while the route files that
      paid stood in other plans, and finding out why took a turn. One command shows it and one command fills it.

USAGE:
  fill.py [status] [<Member>|<role>|all]
  fill.py status --why <pilot>   one pilot's whole list in order: why each route is closed now, or open
  fill.py check [<Member>|<role>|all]
  fill.py fill [<role>|all] [--write] [--once] [--tests N] [--floor CR]
  fill.py add <route id> [--role <role>] [--first]
  fill.py drop <route id> [--role <role>]
  fill.py lift <route id> <ships>
  --tests N    at most N tests added per role in one run (default 8)
  --floor CR   a candidate counts from this estimate, in credits per ship-hour (default 500)
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import fcntl
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dispatch                                   # noqa: E402  the rule that closes a route to a pilot
import division                                   # noqa: E402  who commands which ship, and the plan files
import plan as planfile                           # noqa: E402  each division's plan file: every ship with its own routes
import pull                                       # noqa: E402  the class reason of rule F23, in the dispatcher's words
import routes as routefiles                       # noqa: E402  the route gate and the index files
import workclass                                  # noqa: E402  whose work a route is (rule F23)

STALE = 60 * 60                # a list of the route maker older than this is no ground for PASS
OFFER_STALE = 24 * 60 * 60     # Q75 (2): a list older than this offers no test at all
HOURS = 4                      # a turn: what a bid must carry
HUNTERS = ("drone", "scout", "command", "sentinel")     # the roles that hunt, rule F16: Military's drones, Intel's scouts and the command group; miners, traders and haulers earn
NO_HUNT = "a hunt: this role does not hunt (rule F16)"


def age_of(stamp, now):
    try:
        return now - calendar.timegm(time.strptime(str(stamp)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return float("inf")


def worth(route):
    """What the runs measured: credits per ship-hour, for a route that pays once credits per run; None when not measured."""
    measured = route.get("measured") or {}
    if not measured:
        return None
    return measured.get("credits_per_run") if route.get("once") else measured.get("cph_per_ship")


def mark_of(route, argument):
    return ("census " + argument) if route["kind"] == "census" else route["kind"] + " " + route["id"]


def flying_now(route, rid, orders):
    """Pilots on a route now, counted as the dispatcher counts them."""
    if route.get("kind") == "census":
        systems = set(route.get("systems") or [])
        return sum(1 for what in orders.values() if what.startswith("census ") and what.split(" ", 1)[1] in systems)
    return sum(1 for what in orders.values() if what == str(route.get("kind", "")) + " " + rid)


RESULTS = 3                    # rule F37 (Suggi, 2026-11-22): a test decides on three independent results, never on one


def proven(route):
    """True for a route measured above zero on RESULTS runs or more (F37): fewer good runs are test results, not yet a
    route that pays."""
    return (worth(route) or 0) > 0 and ((route.get("measured") or {}).get("runs") or 0) >= RESULTS


def buys(route):
    """True for a route with a stop that buys goods: such a route is never added as a test by itself."""
    return any(isinstance(stop, dict) and stop.get("buy") for stop in route.get("stops") or [])


def hunts(route):
    """True for a route that hunts: kind `hunt`, or a circuit with a stop that hunts (its `hunt` steps, BLUEPRINT.md)."""
    return route.get("kind") == "hunt" or any(isinstance(stop, dict) and stop.get("hunt") for stop in route.get("stops") or [])


def not_for(route, role):
    """Why the rulebook closes a route outside a role's plan to the role, or None: a hunt, to a role that does not hunt
    (rule F16; rule F9 keeps one hunter per herd, and a miner sent there takes the place of a hunter). A mission that pays
    once per pilot is every pilot's: the starter line's first hunts stay open to every role (Zero, report of 2026-11-16:
    the gate offered Intel's herd to a miner)."""
    if hunts(route) and not route.get("once") and role not in HUNTERS:
        return NO_HUNT
    return None


def survey(root, data, now=None):
    """Everything the answers rest on, read once: plans, route files, the candidates, and the dispatcher's next pass
    played through for every free pilot of the fleet, in its order: who starts on its own plan, who waits and why."""
    now = time.time() if now is None else now
    roles, owners, _errors = division.load_plan(root)
    routes = dispatch.load_routes(root)
    own = dispatch.own_lists(data)                      # each pilot's own list, as its division's plan file was applied
    rows = dispatch.run_rows(data)
    state = {"now": now, "data": data, "rows": rows, "orders": dispatch.fresh_orders(data, now), "rest": dispatch.resting(routes, rows, now),
             "booked": dispatch.booked(data), "loss": dispatch.losing(routes, rows, now),
             "late": dispatch.lately_losing(routes, rows, now), "pirates": dispatch.pirates(data, now)}
    by_route = {}
    for row in rows:
        by_route.setdefault(row.get("route"), []).append(row)
    named = dispatch.flagships(data)
    ammo = set(dispatch.read_json(Path(data) / "catalog" / "ammo.json", []) or [])
    fleet = dispatch.read_json(Path(data) / "fleet" / "fleet.json", {})
    blank = lambda: {"ships": 0, "work": [], "hand": [], "away": [], "starting": [], "waiting": [], "standing": [], "next": [], "park": [], "reasons": {}}
    crews = {role: blank() for role in roles}
    played = dict(state["orders"])                     # the orders as they stand after the dispatcher's next pass
    for ship in fleet.get("ships") or [] if isinstance(fleet, dict) else []:
        name = ship.get("name") or ""
        role = dispatch.role_of(name, named)
        crew = crews.setdefault(role, blank())
        crew["ships"] += 1
        what = state["orders"].get(name)
        if ship.get("status") != "connected":
            crew["away"].append(name)
        elif what:
            crew["hand" if what.startswith("hand ") else "work"].append(name)
            flown = routes.get(what.split(" ", 1)[1]) if " " in what and not what.startswith("hand ") else None
            if flown and flown.get("park"):
                crew.setdefault("park", []).append(name)             # at work by its order, yet on the route no ship should reach (rule F8)
            if flown and routefiles.standing(flown) and not flown.get("park"):      # free for paying work and tests when its run ends
                pilot = dict(dispatch.pilot_of(ship, named, data, ammo), docked=True, goods=0)
                for rid in own.get(name) or roles.get(role) or []:
                    if rid == flown.get("id"):
                        crew["standing"].append(pilot)                 # nothing ahead of its standing work is open: free for what pays
                        break
                    reason, argument = dispatch.why_not(pilot, rid, routes.get(rid), dict(state, orders=played, rows=by_route.get(rid, [])))
                    if reason is None:                                 # its own list sends it there when this run ends: the place is its own
                        played[name + " (next)"] = mark_of(routes[rid], argument)
                        crew["next"].append((name, rid))
                        break
        elif (ship.get("activity") or {}).get("kind") != "idle":
            crew["hand"].append(name)                  # the engine runs a loop or a goal for it: given by hand
        else:
            pilot, why = dispatch.pilot_of(ship, named, data, ammo), []
            for rid in own.get(name) or roles.get(role) or []:
                reason, argument = dispatch.why_not(pilot, rid, routes.get(rid), dict(state, orders=played, rows=by_route.get(rid, [])))
                if reason is None:
                    played[name] = mark_of(routes[rid], argument)
                    crew["starting"].append((name, rid))
                    break
                why.append((rid, reason))
            else:
                crew["waiting"].append(pilot)
                for rid, reason in why:
                    crew["reasons"].setdefault(rid, Counter())[reason] += 1
    book = dispatch.read_json(Path(data) / "routes" / "opportunities.json", {})
    book = book if isinstance(book, dict) else {}
    return {"now": now, "data": data, "root": root, "roles": roles, "owners": owners, "own": own, "routes": routes, "state": state, "crews": crews, "by_route": by_route, "named": named,
            "fleet": fleet,
            "played": played, "taken": {}, "candidates": book.get("candidates") or [], "list_age": age_of(book.get("written_at") or "", now),
            "fleet_at": fleet.get("updated_at") or "?" if isinstance(fleet, dict) else "?"}


HOLD = 65                      # a starter's hold, units
RESERVE_SHORT = "sells an item the reserve is short of or holds back (rule F24)"
CLAIMED = "claimed by another division (admirals.log, rule F25)"


def sold(route):
    """The item ids a route sells by name: a mine route's `sell`, each circuit stop's `sell` list (`all` names none)."""
    items = [s.get("item") for s in route.get("sell") or [] if isinstance(s, dict)]
    for stop in route.get("stops") or []:
        if isinstance(stop, dict) and isinstance(stop.get("sell"), list):
            items += [s.get("item") for s in stop["sell"] if isinstance(s, dict)]
    return [item for item in items if item]


def short_items(seen):
    """{item: units short}: what the reserve lacks (surplus.py, game/reserve.tsv), read once per survey; {} when it
    cannot be read, so that a fault there changes nothing else (requests ENT-213)."""
    if "short" not in seen:
        try:
            import surplus
            res = surplus.surplus(seen["data"], str(Path(seen["root"]).parent))
            seen["short"] = {r["id"]: r["short"] for r in res["rows"] if (r.get("short") or 0) > 0}
        except Exception:                                  # noqa: BLE001  no reserve read: no route is closed by it
            seen["short"] = {}
    return seen["short"]


def kept_items(seen):
    """{item: units}: what the reserve keeps and has none of to spare (surplus.py: short, or held with no surplus unit,
    a good held back for another recipe included; requests ENT-233), read once per survey; {} when it cannot be read."""
    if "kept" not in seen:
        try:
            import surplus
            res = surplus.surplus(seen["data"], str(Path(seen["root"]).parent))
            seen["kept"] = {r["id"]: (r.get("short") or 0) or (r.get("reserved") or 0) for r in res["rows"]
                            if (r.get("short") or 0) > 0 or ((r.get("reserved") or 0) > 0 and (r.get("surplus") or 0) <= 0)}
        except Exception:                                  # noqa: BLE001  no reserve read: no route is closed by it
            seen["kept"] = {}
    return seen["kept"]


def crafted_for_sale(seen, route):
    """The inputs a route's craft stops use from storage for an output the same route sells (by the catalog's recipe),
    less what that stop buys itself: a reserve good crafted and sold is a reserve good sold (errors.log ENT-090)."""
    out, sells = [], set(sold(route))
    for stop in route.get("stops") or []:
        if not isinstance(stop, dict):
            continue
        bought = {b.get("item") for b in stop.get("buy") or [] if isinstance(b, dict)}
        for job in stop.get("craft") or []:
            if not isinstance(job, dict) or job.get("makes") not in sells:
                continue
            if "catalog" not in seen:
                try:
                    import craftbook
                    seen["catalog"] = craftbook.load(seen["data"]) or {}
                except Exception:                          # noqa: BLE001  no catalog: the craft's inputs are not known
                    seen["catalog"] = {}
            recipe = (seen["catalog"].get("recipes") or {}).get(job.get("recipe")) or {}
            out += [i.get("item_id") for i in recipe.get("inputs") or [] if isinstance(i, dict) and i.get("item_id") not in bought]
    return [item for item in out if item]


def sells_short(seen, route):
    """The items of the reserve a route would sell, or craft into what it sells: such a route is never added or lent by
    this script (rule F24; requests ENT-213, ENT-233)."""
    kept = kept_items(seen)
    return [item for item in dict.fromkeys(sold(route) + crafted_for_sale(seen, route)) if item in kept]


def claims(seen):
    """{route id: the member whose claim in force names it} of admirals.log (rule F25; requests ENT-236): a route another
    division claimed is not added to a plan by this script. Standing work is shared and never claimed, but for a hunt:
    a claim names a herd, which carries one side, and with strict classes on every hunt that gives its loot is standing
    work (routes.gives; errors.log ENT-131). {} when the log cannot be read."""
    if "claims" not in seen:
        seen["claims"] = {}
        try:
            import importlib.util
            repo = Path(seen["root"]).resolve().parent                # the log of the tree read; the reader of the fleet's own repository
            spec = importlib.util.spec_from_file_location("comms_claims", Path(__file__).resolve().parents[2] / "scripts" / "comms.py")
            comms = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(comms)
            entries, _errors = comms.read_log(repo, "admirals")
            for entry in comms.claims_in_force(entries):
                for rid in comms.claimed_routes(repo, comms.line_of(entry, "Claims")):
                    route = seen["routes"].get(rid) or {}
                    if route.get("kind") == "hunt" or not routefiles.standing(route):
                        seen["claims"].setdefault(rid, entry["by"])
        except Exception as error:                         # noqa: BLE001  no log read: no route is closed by it
            seen["claims"] = {}
            seen["claims_error"] = "%s: %s" % (type(error).__name__, error)
    return seen["claims"]


def work_systems(route):
    """The systems a route works in (its `place`, its `belt`, the `at` of its mine and hunt steps): where its danger is."""
    places = [str(route.get(key) or "") for key in ("place", "belt")]
    places += [str(step.get("at") or "") for stop in route.get("stops") or [] if isinstance(stop, dict)
               for key in ("mine", "hunt") for step in stop.get(key) or [] if isinstance(step, dict)]
    return {p.split(":")[0] for p in places if p}


def danger_places(seen):
    """{system: route id} of the routes set `off` whose note says `danger:` (rule F27: an Admiral sets a route off for
    pirates as `status off, danger: <why>`; a prey too strong for a hull is no danger of the place); read once per
    survey (Q75 (2), Apophis 2026-11-21: the filler offered the Violethall hunt again)."""
    if "danger" not in seen:
        seen["danger"] = {}
        for rid, route in sorted(seen["routes"].items()):
            if route.get("status") == "off" and "danger:" in str(route.get("note") or "").lower():     # `status off, danger: <why>`
                for system in work_systems(route):
                    seen["danger"].setdefault(system, rid)
    return seen["danger"]


def refusal(seen, rid, route):
    """Why the filler never offers this route (Q75 (2)), or None: set off, or its place is a place set off for danger."""
    if route.get("status") == "off":
        return "set off: " + (" ".join(str(route.get("note") or "").split()[-24:]) or "its file says off")[-160:]
    near = sorted(system for system in work_systems(route) if system in danger_places(seen) and danger_places(seen)[system] != rid)
    if near:
        return "off for danger: %s, set off for danger, works at %s" % (danger_places(seen)[near[0]], near[0])
    return None


def guard_ship(seen, name):
    """True for a ship whose own list, past the missions that pay once and the fittings, begins with a guard: it keeps a
    post, and no test or paying route is put in front of it (requests ENT-236: five of seven posts would have stood
    empty for the hours of a far test)."""
    for rid in seen["own"].get(name) or []:
        route = seen["routes"].get(rid) or {}
        if route.get("once") or route.get("status") == "off" or routefiles.stage(route) == "fit":
            continue
        return route.get("kind") == "guard"
    return False


def regains(seen):
    """What comes back per hour by our own readings (hive.py `rates`), read once per survey."""
    if "rates" not in seen:
        import hive                                # here, not at the top: hive.py reads fill.py for the standing fleet
        seen["rates"] = hive.rates(seen["data"])
    return seen["rates"]


SALE_TRADES = "a sale circuit is Trade's work (orders P5): the goods go to a trader by gift"

def carries(seen, route):
    """How many ships a route carries, from our own readings: {"ships": what it carries hour after hour (None: not
    measured), "extra": ships more for one turn while today's standing order or field holds, "text": what both rest
    on}; None for a route nothing of this limits (a circuit, a census) or that no reading speaks of. A mine route that
    sells is carried by what its bid regains per hour at its best price, shared by the routes that sell the same good
    at the same station; one that sells nothing by what its field grows back; a hunt by one hunter (the herd's regain
    is named). The standing depth of a bid is one order: it can leave within the hour (errors ENT-046, ENT-054). A bid
    nobody sold into and a field that read full show no regain: that is `not measured`, never 0."""
    bids, fields, herds = regains(seen)
    kind = route.get("kind")
    if kind == "hunt" and len(str(route.get("place", "")).split(":")) == 2:
        system, poi = route["place"].split(":")
        back = [herds[(system, poi, s)][0] for s in route.get("species") or [] if (system, poi, s) in herds]
        if not back:
            return None
        return {"ships": 1, "extra": 0, "text": "its herd regains %.1f animals an hour and a hunter kills about %.0f: one hunter per place"
                % (sum(back), route.get("kills", 8) * 60 / (route.get("minutes", 40) + 15))}
    if kind != "mine":
        return None
    per_ship = HOLD * 60 / (route.get("minutes", 45) + 15)               # units an hour: a starter's hold, a run and its way home
    sells = route.get("sell") or []
    if sells:
        base, item = str(route.get("station", "")).split(":")[-1], sells[0].get("item")
        book = dispatch.read_json(Path(seen["data"]) / "market" / (base + ".json"), {})
        row = next((i for i in book.get("items") or [] if i.get("item_id") == item), None) if isinstance(book, dict) else None
        same = sum(1 for other in seen["routes"].values() if other.get("kind") == "mine" and other.get("status") != "off" and other.get("station") == route.get("station")
                   and (other.get("sell") or [{}])[0].get("item") == item) or 1       # the routes that sell the same good into the same bid share it
        stands = bool(row) and (row.get("best_buy") or 0) >= sells[0].get("min_price", 0) and isinstance(row.get("best_buy_qty"), (int, float))
        depth, rate = (int(row["best_buy_qty"]) if stands else 0), bids.get((base, item))
        if rate is not None and not rate[0] and not rate[1]:
            rate = None                                # nothing was taken and nothing came back: the readings say nothing
        if rate is None and not stands:
            return None
        text = ("the %s bid at %s regains %s units an hour at its best price" % (item, base, format(int(rate[0]), ",")) if rate is not None
                else "what the %s bid at %s regains is not measured" % (item, base))
        text += "; %s units stand at %s cr now, one order that can leave within the hour" % (format(depth, ","), row["best_buy"]) if stands else "; no bid at its price now"
        text += "; %d routes share the bid" % same if same > 1 else ""
        return {"ships": None if rate is None else int(rate[0] / per_ship / same), "extra": int(depth // (per_ship * HOURS) // same), "text": text}
    place = str(route.get("belt", ""))
    system, poi = (place.split(":") + [""])[:2]
    back = [rate[0] for key, rate in fields.items() if key[0] == system and key[1] == poi and (rate[0] or rate[1])]     # a field that read full shows no regain
    left = dispatch.field_left(seen["data"], place, seen["now"], fresh=float("inf")) or {}
    if not back and not left:
        return None
    floor = route.get("min_left") if isinstance(route.get("min_left"), dict) else {}
    if floor:                                          # requests ENT-333: a gather counts only the goods its floor names, never the other ores of a mixed field
        back = [rate[0] for key, rate in fields.items() if key[0] == system and key[1] == poi and len(key) > 2 and key[2] in floor and (rate[0] or rate[1])]
        left = {item: units for item, units in left.items() if item in floor}
        if not back and not any(left.values()):
            return {"ships": 0, "extra": 0, "text": "none of its goods (%s) lie in its field or grow back there" % ", ".join(sorted(floor))}
    free = sum(max(0, units - int(floor.get(item, 0))) for item, units in left.items())          # what may be taken before the route's own floor closes it
    text = "its field grew back %s units an hour" % format(int(sum(back)), ",") if back else "what its field grows back is not measured"
    text += "; %s units lie in it%s" % (format(sum(left.values()), ","), ", %s above its floor" % format(free, ",") if floor else "") if left else ""
    return {"ships": int(sum(back) / per_ship) if back else None, "extra": int(free // (per_ship * HOURS)), "text": text}


def carried(deep):
    """The cell `3 +20` of what carries() found: ships hour after hour (`?`: not measured), and ships more for one turn."""
    if not deep:
        return "--"
    return "%s%s" % (deep["ships"] if deep["ships"] is not None else "?", " +%d" % deep["extra"] if deep["extra"] else "")


def asks(seen, item):
    """[(units at the best ask, the ask, base)] for an item over the saved order books, cheapest first."""
    out = []
    for path in sorted((Path(seen["data"]) / "market").glob("*.json")):
        book = dispatch.read_json(path, {})
        for row in book.get("items") or [] if isinstance(book, dict) and isinstance(book.get("items"), list) else []:
            if row.get("item_id") == item and (row.get("best_sell") or 0) > 0:
                out.append((int(row.get("best_sell_qty") or row.get("sell_quantity") or 0), row["best_sell"], book.get("base") or path.stem))
    return sorted(out, key=lambda r: r[1])


def refused_to(seen, rid, role):
    """True when a once route was flown by pilots of this role and the board refused it to every one of them
    (`... not offered`): the mission is not for this role, and no waiting ship of it may take it (requests ENT-095)."""
    mine = [r for r in seen["by_route"].get(rid, []) if dispatch.role_of(str(r.get("pilot") or ""), seen.get("named") or {}) == role]
    return bool(mine) and all(dispatch.refused(r) for r in mine)


def read_role(seen, role, floor=500, tests=8):
    """What one role's ships do now and what would give its waiting ships work, and its ships on standing work
    paying work.
    {ships, work, hand, away, starting [(pilot, route)], waiting [pilot], standing [pilot on standing work],
     idle [waiting pilot left without any offer],
     plan [(route id, flying, cap, Counter of reasons, hint)], paying [(route id, worth, pilots)],
     tests [(route id, estimate, route to write or None, pilot)], closed {reason: [(worth, route id)]}}"""
    crew = seen["crews"].get(role) or {"ships": 0, "work": [], "hand": [], "away": [], "starting": [], "waiting": [], "standing": [], "next": [], "reasons": {}}
    routes, plan = seen["routes"], seen["roles"].get(role) or []
    state = dict(seen["state"], orders=dict(seen["played"], **seen["taken"]))     # what free pilots start and take is counted, role after role
    starting, waiting = crew["starting"], crew["waiting"]

    def closed_to(pilot, rid, route):
        """The dispatcher's rule, given only the runs of this route (the rule reads no others)."""
        return dispatch.why_not(pilot, rid, route, dict(state, rows=seen["by_route"].get(rid, [])))

    rows = []
    for rid in plan:
        route, why = routes.get(rid) or {}, crew["reasons"].get(rid) or Counter()
        deep = carries(seen, route) if any(r.startswith("max_ships") for r in why) else None
        hint = "carries %s ships hour after hour, %d more this turn: %s" % ("about %d" % deep["ships"] if deep["ships"] is not None else "an unmeasured number of",
                                                                               deep["extra"], deep["text"]) if deep else ""
        rows.append((rid, flying_now(route, rid, seen["state"]["orders"]), route.get("max_ships"), why, hint))
    left = list(waiting) + list(crew.get("standing") or [])           # a ship on standing work is free for what pays
    paying, closed, refused = [], {}, []                         # refused: [(route id, why)] the filler never offers (Q75 (2))

    def offer(rid, route, value, limit=None):
        """The pilots the route is open to (waiting, or on standing work), taken off the list; the commonest reason
        when there are none. A pilot whose own list holds the route is passed over: the dispatcher gives it to it."""
        took, why = [], Counter()
        for pilot in list(left):
            if limit is not None and len(took) >= limit:
                break
            if rid in (seen["own"].get(pilot["name"]) or plan) or guard_ship(seen, pilot["name"]):
                continue
            reason, argument = closed_to(pilot, rid, route)
            if reason is None:
                state["orders"][pilot["name"]] = mark_of(route, argument)
                took.append(pilot["name"])
                left.remove(pilot)
            else:
                why[reason] += 1
        if not took and why:
            closed.setdefault(why.most_common(1)[0][0], []).append((value, rid))
        return took

    outside = [(worth(route), rid, route) for rid, route in routes.items()
               if route.get("status") != "off" and not route.get("park") and route.get("kind") != "census" and proven(route)]
    by_hand = []
    for value, rid, route in sorted(outside, key=lambda r: (-r[0], r[1])):
        rule = not_for(route, role) if rid not in plan else None         # what its Admiral put into the plan stays
        if rule:
            closed.setdefault(rule, []).append((value, rid))
            continue
        other = pull.class_reason(role, route, rid)                # rule F23: never offered outside the role's own class
        if other:
            if rid not in plan:
                closed.setdefault(other, []).append((value, rid))
                refused.append((rid, other))
            continue
        if rid not in plan and role != "trader" and route.get("kind") == "circuit" and not route.get("once") and workclass.sells(route):
            closed.setdefault(SALE_TRADES, []).append((value, rid))     # orders ENT-061 P5: never added to another class's plan, even with strict classes off
            refused.append((rid, SALE_TRADES))
            continue
        danger = refusal(seen, rid, route) if rid not in plan else None
        if danger:                                                # Q75 (2): a place set off for danger is never offered
            refused.append((rid, danger))
            continue
        if buys(route):                                           # it buys goods: in a plan by its Admiral's word only, never by this script
            if rid not in plan:
                by_hand.append((value, rid))
            continue
        if rid not in plan and sells_short(seen, route):         # a reserve good is kept, never sold by a route this script adds (ENT-213)
            closed.setdefault(RESERVE_SHORT, []).append((value, rid))
            continue
        owner = seen["owners"].get(role) or division.ROLES.get(role)
        if rid not in plan and claims(seen).get(rid, owner) != owner:     # another division's claim stands (rule F25)
            closed.setdefault(CLAIMED, []).append((value, rid))
            refused.append((rid, "%s: %s's" % (CLAIMED, claims(seen)[rid])))
            continue
        if route.get("once") and refused_to(seen, rid, role):
            if rid not in plan:
                closed.setdefault("the board refused it to this role", []).append((value, rid))
            continue
        took = offer(rid, route, value) if left else []
        if took:
            paying.append((rid, value, took))
    found, seen_ids = [], set(plan) | {rid for rid, _v, _t in paying} | {rid for _v, rid in by_hand}
    stale = seen["list_age"] > OFFER_STALE and bool(seen["candidates"])
    if stale:                                                     # Q75 (2): no test from a list older than a day
        refused.append(("the route maker's list", "%s old, over %d hours: no test of it is offered until the route maker runs again"
                        % ("%d hours" % (seen["list_age"] // 3600) if seen["list_age"] != float("inf") else "not dated", OFFER_STALE // 3600)))
    for cand in [] if stale else sorted(seen["candidates"], key=lambda c: -(c.get("per_ship_hour") or 0)):
        draft = cand.get("route")
        if not isinstance(draft, dict) or cand.get("needs") or (cand.get("per_ship_hour") or 0) < floor or str(cand.get("status", "")).startswith("off"):
            continue
        rid = cand.get("route_id") or draft.get("id")
        if not rid or rid in seen_ids or (rid in routes and (proven(routes[rid]) or (worth(routes[rid]) is not None and worth(routes[rid]) <= 0))):
            continue                                              # proven ones are judged above, by their figure; one measured at a loss is no test
        seen_ids.add(rid)
        route = routes.get(rid) or dict(draft, id=rid)
        danger = refusal(seen, rid, route)                        # Q75 (2): set off, or at a place set off for danger
        if danger:
            refused.append((rid, danger))
            continue
        rule = not_for(route, role)                               # never in the plan here: seen_ids holds the plan
        if rule:
            closed.setdefault(rule, []).append((cand["per_ship_hour"], rid))
            continue
        if route.get("once") and refused_to(seen, rid, role):
            continue
        if buys(route):                                           # a gap is flown once by hand, with one load (errors.log ENT-027)
            by_hand.append((cand["per_ship_hour"], rid))
            continue
        if sells_short(seen, route):                              # a test that sells what the reserve lacks is no test of ours (ENT-213)
            closed.setdefault(RESERVE_SHORT, []).append((cand["per_ship_hour"], rid))
            continue
        other = pull.class_reason(role, route, rid)                # rule F23: a test of another class is not this role's (ENT-236: a mine test is the miners')
        if other:
            closed.setdefault(other, []).append((cand["per_ship_hour"], rid))
            refused.append((rid, other))
            continue
        owner = seen["owners"].get(role) or division.ROLES.get(role)
        if claims(seen).get(rid, owner) != owner:
            closed.setdefault(CLAIMED, []).append((cand["per_ship_hour"], rid))
            refused.append((rid, "%s: %s's" % (CLAIMED, claims(seen)[rid])))
            continue
        took = offer(rid, route, cand["per_ship_hour"], limit=1) if left and len(found) < tests else []
        if took:
            found.append((rid, cand["per_ship_hour"], None if rid in routes else route, took[0]))
    seen["taken"] = {name: what for name, what in state["orders"].items() if name not in seen["played"]}
    return {"role": role, "owner": seen["owners"].get(role) or division.ROLES.get(role, "?"), "ships": crew["ships"], "work": crew["work"], "hand": crew["hand"],
            "away": crew["away"], "starting": starting, "waiting": [p["name"] for p in waiting], "standing": [p["name"] for p in crew.get("standing") or []],
            "next": list(crew.get("next") or []), "park": list(crew.get("park") or []),
            "idle": [p["name"] for p in left if p in waiting], "plan": rows,
            "paying": paying, "tests": found, "closed": closed, "by_hand": sorted(by_hand, reverse=True), "refused": refused}


def tell_refused(seen, got):
    """Q75 (2): each route the filler never offers, printed once in a call with its reason (`seen` keeps what was told):
    a line each for a list too old, a route set off or at a place set off for danger and a claim; the routes of another
    class (hundreds: every gather route to every other role) in one line per class reason, the first few named."""
    told = seen.setdefault("told", set())
    grouped = {}
    for rid, why in got.get("refused") or []:
        if (rid, why) in told:
            continue
        told.add((rid, why))
        if why.startswith("class: "):
            grouped.setdefault(why, []).append(rid)
        else:
            print("  not offered: %s: %s" % (rid, why))
    for why, ids in sorted(grouped.items()):
        print("  not offered, %s (rule F23): %d route%s: %s%s" % (why, len(ids), "" if len(ids) == 1 else "s", ", ".join(ids[:6]), " ..." if len(ids) > 6 else ""))


def spare(seen, got, served=(), room=None):
    """[(route id, places)]: standing work of the role's plan that is full while ships of the role wait, with the places
    to add: one per waiting ship its limit closes it to, and no more than its field carries (carries(): the ships it
    keeps busy hour after hour plus those it carries for one turn above its floor). `served` are waiting pilots this
    call gives other work; `room` ({route id: places left to give}) is shared by the roles of one call, so that a route
    several plans hold is lifted once for all of them. Only a mine route that sells nothing: what a bid carries is no
    script's to lift. Only a route in home space: beyond the border the limit is its Admiral's (rule F13). Only a route
    of the role's own class (rule F23, workclass.own): a gather route is lifted for waiting miners alone."""
    room = {} if room is None else room
    systems, home = routefiles.atlas(seen["root"])
    need = len([name for name in got["waiting"] if name not in served])
    found = []
    for rid, _flying, cap, why, _hint in got["plan"]:
        route = seen["routes"].get(rid) or {}
        closed = sum(count for reason, count in why.items() if str(reason).startswith("max_ships"))
        if need <= 0 or not closed or not isinstance(cap, int) or route.get("kind") != "mine" or route.get("sell") or not routefiles.standing(route):
            continue
        if not workclass.own(got["role"], route, rid):              # rule F23: never lifted for ships of another class
            continue
        if max(len(seen["by_route"].get(rid) or []), (route.get("measured") or {}).get("runs") or 0) < RESULTS:
            seen.setdefault("unflown", {})[rid] = "not lifted: a test until %d measured runs (rule F37; requests ENT-216)" % RESULTS
            continue
        limit = route.get("lift_to") if isinstance(route.get("lift_to"), int) and not isinstance(route.get("lift_to"), bool) else None
        if limit is None and routefiles.zone(route, systems, home)[0] != "home space":    # also a route whose systems the chart does not know
            continue                                                 # beyond the border only as far as its Admiral wrote into the file (`lift_to`)
        if rid not in room:
            deep = carries(seen, route)
            room[rid] = max(0, ((deep["ships"] or 0) + deep["extra"] if deep else 0) - cap)
            if limit is not None:
                room[rid] = min(room[rid], max(0, limit - cap))
        places = min(need, closed, room[rid])
        if places > 0:
            found.append((rid, places))
            room[rid] -= places
            need -= places
    return found


def fallback_on(data):
    """The fallback's switch: the file data/fleet/fallback-on."""
    return (Path(data) / "fleet" / "fallback-on").exists()


def borrow(seen, got, role, need, most=2):
    """[route id]: standing work of OTHER plans to lend to a role whose `need` ships wait with nothing of their own plan
    open (the fallback). Only what a hand would have added: a mine route that sells nothing, in home space (beyond the
    border a plan is its Admiral's alone, rule F13), switched on, with a ship limit, whose field carries more ships than
    fly it now (carries()), and that at least one of the waiting ships can fly (the dispatcher's rule says open, or
    full: a full one is lifted by spare() on the next pass). The routes with the most places first, `most` at most.
    Only a route of the waiting role's own class (rule F23, workclass.own): never a gather route to a role that does not
    gather, unless its file's `open_to` names the role."""
    if need <= 0:
        return []
    systems, home = routefiles.atlas(seen["root"])
    plan = set(seen["roles"].get(role) or [])
    others = {rid for other, ids in seen["roles"].items() if other != role for rid in ids} - plan
    idle = set(got["idle"])
    waiting = [pilot for pilot in (seen["crews"].get(role) or {}).get("waiting") or [] if pilot["name"] in idle]
    found = []
    for rid in sorted(others):
        route = seen["routes"].get(rid) or {}
        cap = route.get("max_ships")
        if (route.get("status") == "off" or route.get("park") or route.get("kind") != "mine" or route.get("sell")
                or not isinstance(cap, int) or isinstance(cap, bool)):
            continue
        if not workclass.own(role, route, rid):                     # rule F23: each class flies its own work
            continue
        if routefiles.zone(route, systems, home)[0] != "home space":
            continue
        deep = carries(seen, route)
        places = ((deep["ships"] or 0) + deep["extra"] if deep else 0) - flying_now(route, rid, seen["state"]["orders"])
        if places <= 0:
            continue
        state = dict(seen["state"], orders=dict(seen["played"], **seen["taken"]), rows=seen["by_route"].get(rid, []))
        open_to = 0
        for pilot in waiting:
            reason = dispatch.why_not(pilot, rid, route, state)[0]
            if reason is None or str(reason).startswith("max_ships"):
                open_to += 1
        if open_to:
            found.append((min(places, open_to), rid))
    return [rid for _places, rid in sorted(found, key=lambda entry: (-entry[0], entry[1]))[:most]]


def raise_cap(root, data, who, rid, ships, stamp):
    """Write a route's `max_ships` with a line in its note and commit it: (True, the commit's line) or (False, why)."""
    route = json.loads((Path(root) / "routes" / (rid + ".json")).read_text(encoding="ascii"))
    was = route.get("max_ships")
    route["max_ships"] = ships
    route["note"] = (str(route.get("note") or "") + " %s (fill.py, %s): max_ships %s -> %d." % (stamp, who, was if was else "none", ships)).strip()
    return commit(root, data, who, {"routes/%s.json" % rid: json.dumps(route, indent=1) + "\n"}, "%s: max_ships %s -> %d (fill.py, %s)" % (rid, was if was else "none", ships, who))


def verdict(seen, got):
    """(True for PASS, the line). No ship is idle (Suggi, 2026-11-16): PASS only when no ship of the role waits."""
    waiting, places, tests = len(got["waiting"]), sum(len(p) for _r, _v, p in got["paying"]), len(got["tests"])
    parked = got.get("park") or []
    if not waiting:
        return True, "PASS: no ship of %s waits" % got["role"] + (
            " | %d places of paying work and %d tests stand open to its ships on standing work: python3 -I -B game/fleet/fill.py fill %s --write"
            % (places, tests, got["role"]) if places or tests else "") + (
            " | %d on park, the route no ship should reach (rule F8; Apollo's report of 2026-11-17): %s; `fill.py status %s` says what closes the rest"
            % (len(parked), ", ".join(parked[:4]) + (" ..." if len(parked) > 4 else ""), got["role"]) if parked else "")
    if places or tests:
        return False, ("HALT: %d ships of %s wait while %d places of paying work and %d tests stand open: python3 -I -B game/fleet/fill.py fill %s --write"
                       % (waiting, got["role"], places, tests, got["role"]))
    if seen["list_age"] > STALE:
        return False, ("HALT: %d ships of %s wait and the route maker's list is %s old, so no test can be named: its service fails; write to the Fleet Admiral in requests.log"
                       % (waiting, got["role"], "%d minutes" % (seen["list_age"] // 60) if seen["list_age"] != float("inf") else "missing or not dated"))
    if got["role"] == "scout":
        w_pilots = ((seen.get("crews") or {}).get("scout") or {}).get("waiting") or []
        if w_pilots and len(w_pilots) == waiting and all(bool(p.get("docked")) for p in w_pilots):
            return True, ("PASS: %d docked scout(s) on watch with no due census or open scout work (rule F8 docked-watch exception, ENT-381/398)" % waiting)
    return False, ("HALT: %d ships of %s wait and nothing that pays is open to them: the plan lacks standing work for them (a route that trains or gathers, each "
                   "sized by what its place carries: the skill fleet-play, `Plan a Division`); what closes each route is listed by `fill.py status %s`"
                   % (waiting, got["role"], got["role"]))


def show(seen, got):
    def short(names):
        return ", ".join(names[:3]) + (" ..." if len(names) > 3 else "")
    print("FILL | %s (%s) | %d ships: %d at work, %d starting, %d waiting, %d by hand, %d away | standing work: %d free for what pays, %d take a route of their list "
          "next | fleet file %s" % (got["role"], got["owner"], got["ships"], len(got["work"]), len(got["starting"]), len(got["waiting"]), len(got["hand"]), len(got["away"]),
                                     len(got.get("standing") or []), len(got.get("next") or []), seen["fleet_at"]))
    if got["waiting"] or got["paying"] or got["tests"]:
        if got["waiting"]:
            print("  the role's routes, in one order           flying/cap  closed to the %d waiting pilots because" % len(got["waiting"]))
        for n, (rid, flying, cap, why, hint) in enumerate(got["plan"] if got["waiting"] else [], 1):
            print("  %2d %-38s %3d/%-5s  %s%s" % (n, rid[:38], flying, cap if cap else "-", ", ".join("%s %d" % kv for kv in why.most_common(4)) or "--", (" | " + hint) if hint else ""))
        if got["paying"] or got["tests"]:
            print("  open outside the plan to ships that wait or do standing work (fill adds it):")
            for rid, value, pilots in got["paying"]:
                print("     PAYING %-38s %s measured, open to %d ships (%s)" % (rid[:38], format(int(value), ","), len(pilots), short(pilots)))
            for rid, value, draft, pilot in got["tests"]:
                print("     TEST   %-38s %s estimated per ship-hour, one ship%s" % (rid[:38], format(int(value), ","), "" if draft is None else "; its route file is written"))
        if got.get("by_hand"):
            print("  not added by itself: %d candidates that buy goods, up to %s estimated per ship-hour (%s ...): a gap is flown once by hand with one load"
                  % (len(got["by_hand"]), format(int(got["by_hand"][0][0]), ","), got["by_hand"][0][1][:44]))
        if got["closed"] and got["idle"]:
            print("  closed outside the plan to the %d pilots still without work, by what closes it:" % len(got["idle"]))
            for reason, items in sorted(got["closed"].items(), key=lambda kv: -max(v or 0 for v, _r in kv[1])):
                items.sort(key=lambda r: -(r[0] or 0))
                print("     %-24s %d routes, up to %s: %s" % (reason, len(items), format(int(items[0][0] or 0), ","), short([r for _v, r in items])))
                if reason.startswith("needs "):
                    module = reason[6:]
                    offers = asks(seen, module)
                    fits = sorted(rid for rid, route in seen["routes"].items() if route.get("status") != "off" and any(
                        isinstance(f, dict) and f.get("module") == module for s in route.get("stops") or [] if isinstance(s, dict)
                        for f in (s.get("fit") if isinstance(s.get("fit"), list) else [s.get("fit")])))
                    print("        %s on offer in our books: %s | routes that fit it: %s"
                          % (module, "; ".join("%d at %s cr (%s)" % o for o in offers[:6]) or "none", ", ".join(fits) or "none"))
    tell_refused(seen, got)                                       # Q75 (2): each refusal once, with its reason
    if seen["list_age"] > STALE / 2:
        print("  NOTE: the route maker's list is %s old" % ("%d minutes" % (seen["list_age"] // 60) if seen["list_age"] != float("inf") else "missing or not dated"))
    ok, line = verdict(seen, got)
    print("  " + line)
    return ok


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def in_work(root):
    """The lines of `git status` for what game/routes holds uncommitted, the guidebooks left out: no script reads a
    guidebook, and an Admiral writes its own for most of a turn (requests ENT-171)."""
    lines = git(root, "status", "--porcelain", "--", "routes")[1].splitlines()
    return [line for line in lines if line.strip() and "routes/guidebook/" not in line]


def commit(root, data, who, files, message, tries=None, wait=None):
    """Write {path relative to the game folder: text} with the index files, run the route gate, commit by path as
    `who`. (True, the commit's line) or (False, why); on a failure every file is put back. Another member's route
    file in work is waited for, `tries` times `wait` seconds, before the refusal: the turns overlap in one clone."""
    if (Path(data) / "fleet" / "STOP").exists():
        return False, "REFUSED: fleet/STOP exists: nothing is changed while the fleet is halted"
    tries = COMMIT_TRIES if tries is None else tries
    wait = float(os.environ.get("FLEET_COMMIT_WAIT", COMMIT_WAIT)) if wait is None else wait
    (Path(data) / "routes").mkdir(parents=True, exist_ok=True)
    with open(Path(data) / "routes" / "fill.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)                           # one writer of the plans at a time, from the check to the commit
        dirty = in_work(root)
        for _again in range(max(0, tries - 1)):
            if not dirty:
                break
            time.sleep(wait)
            dirty = in_work(root)
        if dirty:
            return False, "REFUSED: game/routes holds a change that is not committed; commit it or take it back first:\n" + "\n".join(dirty)
        before = {p.name for p in (Path(root) / "routes").glob("*.md")}
        new = [rel for rel in files if not (Path(root) / rel).exists()]
        for rel, text in files.items():
            (Path(root) / rel).write_text(text, encoding="ascii")
        made = ["routes/" + name for name, _state in routefiles.write_index(root)]     # written, current and removed
        new += [rel for rel in made if rel.split("/")[-1] not in before]
        paths = sorted(set(files) | set(made))
        errors, _count = routefiles.check(root)
        if not errors:
            git(root, "add", "--", *paths)
            code, out = git(root, "-c", "user.name=" + who, "-c", "user.email=%s@suggi-workspace.dev" % who.lower(), "commit", "-q", "-m", message, "--", *paths)
            if code == 0:
                return True, "committed %s as %s: %s" % (git(root, "log", "-1", "--format=%h")[1].strip(), who, message[:110])
            errors = ["the commit failed: " + out.strip()[-300:]]
            git(root, "reset", "-q", "--", *paths)
        for rel in new:
            (Path(root) / rel).unlink(missing_ok=True)
        if [p for p in paths if p not in new]:
            git(root, "checkout", "--", *[p for p in paths if p not in new])
        return False, "HALT: nothing changed; the route gate says:\n  " + "\n  ".join(errors[:8])


COMMIT_TRIES, COMMIT_WAIT = 4, 4.0                 # a route file another member has in work: looked at this often, this many seconds apart


def may_change(who, role):
    return who == "Unity" or division.ROLES.get(role) == who


def why_lines(seen, name):
    """The lines of `fill.py status --why <pilot>`: every route of the pilot's whole list in order, with the reason the
    dispatcher's own rule (dispatch.why_not) closes it now or `open`, and the one it flies (the reports of Zero and
    Mercury, 2026-11-22: each wrote the same scratch loop to learn why working ships took a training loop)."""
    fleet = seen.get("fleet") or dispatch.read_json(Path(seen["data"]) / "fleet" / "fleet.json", {})
    ship = next((s for s in (fleet.get("ships") or [] if isinstance(fleet, dict) else []) if s.get("name") == name), None)
    if ship is None:
        return ["WHY %s: no ship of that name in fleet.json" % name]
    role = dispatch.role_of(name, seen["named"])
    pilot = dispatch.pilot_of(ship, seen["named"], seen["data"], set(dispatch.read_json(Path(seen["data"]) / "catalog" / "ammo.json", []) or []))
    order = seen["state"]["orders"].get(name) or ""
    flown = order.split(" ", 1)[1] if " " in order and not order.startswith("hand ") else ""
    ids = seen["own"].get(name) or seen["roles"].get(role) or []
    out = ["WHY %s | role %s | flies %s | %d routes in its list, in order" % (name, role, flown or (order or "nothing"), len(ids))]
    for n, rid in enumerate(ids, 1):
        reason, _argument = dispatch.why_not(pilot, rid, seen["routes"].get(rid), dict(seen["state"], orders=seen["played"] or seen["state"]["orders"], rows=seen["by_route"].get(rid, [])))
        mark = "  <- flies it now" if rid == flown else ""
        out.append("  %2d %-40s %s%s" % (n, rid[:40], "open" if reason is None else "closed: " + str(reason), mark))
    return out


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data", "--tests", "--floor", "--role", "--why"))]
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    verb = words[0] if words and words[0] in ("status", "check", "fill", "add", "drop", "lift") else "status"
    rest = words[1:] if words and words[0] == verb else words
    kind, who = division.member()
    who = who if kind == "member" else ""
    seen = survey(root, data)
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(seen["now"]))
    floor, tests = int(value("--floor", "500")), int(value("--tests", "8"))

    def roles_of(word):
        if word == "all":
            return sorted(seen["roles"])
        if word in seen["roles"]:
            return [word]
        if word in division.MEMBERS:
            return sorted(r for r in seen["roles"] if division.ROLES.get(r) == word)
        sys.exit("`%s` is no member and no role: %s, %s, or all" % (word, ", ".join(division.MEMBERS), ", ".join(sorted(seen["roles"]))))

    if verb == "status" and "--why" in args:          # one pilot's whole list with the reason each route is closed
        for line in why_lines(seen, value("--why", "")):
            print(line)
        return 0
    if verb in ("status", "check"):
        chosen = roles_of(rest[0] if rest else ("all" if who in ("Unity", "") else who))
        results = [(role, read_role(seen, role, floor, tests)) for role in chosen]
        ok = True
        for role, got in results:
            if verb == "status":
                ok = show(seen, got) and ok
            else:
                good, line = verdict(seen, got)
                print(line)
                ok = ok and good
        if len(results) > 1:
            total = lambda key: sum(len(got[key]) for _r, got in results)
            print("FLEET | %d ships: %d at work, %d starting, %d waiting, %d by hand | %s" % (sum(got["ships"] for _r, got in results), total("work"), total("starting"),
                                                                                           total("waiting"), total("hand"), "PASS" if ok else "HALT"))
        return 0 if ok or verb == "status" else 1

    if not who:
        sys.exit("REFUSED: this shell is no member of The Collective: it changes no plan")
    if verb == "fill":
        chosen = roles_of(rest[0]) if rest else sorted(r for r in seen["roles"] if division.ROLES.get(r) == who)
        files, lines, added, changes = {}, [], [], {}
        room, lifts = {}, Counter()                                 # standing work that is full while ships wait: places to add, per route
        for role in chosen:
            if not may_change(who, role):
                sys.exit("REFUSED: the %s plan is kept by %s (orders F1): ask in requests.log" % (role, division.ROLES.get(role)))
            got = read_role(seen, role, floor, tests if division.ROLES.get(role) == who else 0)     # a test goes to the caller's own roles only
            once = "--once" in args                                 # only missions that pay once (they buy nothing: read_role keeps buying routes out)
            paying = [(rid, pilots) for rid, _v, pilots in got["paying"] if not once or seen["routes"][rid].get("once")]
            found = [] if once else got["tests"]
            new = [rid for rid, _p in paying] + [rid for rid, _v, _d, _p in found]
            print("%s: %d waiting, %d on standing work; %d %s and %d tests to add%s" % (role, len(got["waiting"]), len(got["standing"]), len(paying),
                                                                                   "routes that pay once" if once else "paying routes", len(found), ": " + ", ".join(new) if new else ""))
            for rid, pilots in paying:                              # Zero, 2026-11-16: a test put on a ship went unseen and the next `plan.py set` took it off
                if not seen["routes"][rid].get("once"):
                    print("  %s -> %s (in front of its own routes)" % (rid, ", ".join(pilots)))
            for rid, _estimate, _draft, pilot in found:
                print("  test %s -> %s (in front of its own routes; keep it when you set that ship's routes)" % (rid, pilot))
            tell_refused(seen, got)                                 # Q75 (2): what is never offered, each once, with its reason
            served = {name for _rid, pilots in paying for name in pilots} | {pilot for _rid, _estimate, _draft, pilot in found}
            lifted = spare(seen, got, served, room)
            for rid, why in sorted((seen.get("unflown") or {}).items()):
                print("  %s: %s" % (rid, why))
            seen["unflown"] = {}
            for rid, places in lifted:
                lifts[rid] += places
            still = len(got["idle"]) - sum(places for _rid, places in lifted)
            lent = borrow(seen, got, role, still) if fallback_on(data) else []
            if lent:
                print("  standing work of other plans lent to the %s plan's list Then (%d ship%s with nothing open; the fallback): %s"
                      % (role, still, " waits" if still == 1 else "s wait", ", ".join(lent)))
            if not new and not lent:
                continue
            for rid, estimate, draft, _pilot in found:
                if draft is not None:
                    draft = dict(draft, max_ships=RESULTS)
                    draft["note"] = (str(draft.get("note") or "") + " Added as a test by fill.py on %s (%s): up to %d ships, one result each, until %d runs are read (rule F37)."
                                     % (stamp, who, RESULTS, RESULTS)).strip()
                    files["routes/%s.json" % rid] = json.dumps(draft, indent=1) + "\n"
                    seen["routes"][rid] = draft
            edits = changes.setdefault(planfile.division_of(role), [])
            for rid, pilots in paying:                              # a mission that pays once is for every ship; a route that repeats for the ships it is open to
                if seen["routes"][rid].get("once"):
                    edits.append(lambda plan, rid=rid: planfile.put_first(plan, [rid]))
                else:
                    edits.append(lambda plan, rid=rid, pilots=pilots: planfile.put_own(plan, pilots, rid))
            for rid, _estimate, _draft, pilot in found:
                edits.append(lambda plan, rid=rid, pilot=pilot: planfile.put_own(plan, [pilot], rid))
            name = planfile.division_of(role)
            for rid in lent:                                        # as `fill.py add` puts a route: the list Then, or the tail of the role's ships in a division of two roles
                if len(planfile.roles_of(name)) > 1:
                    ships = [ship for ship, its, _row in planfile.crew_of(data, name) if its == role]
                    edits.append(lambda plan, rid=rid, ships=ships: planfile.put_own(plan, ships, rid, tail=True))
                else:
                    edits.append(lambda plan, rid=rid: planfile.put_then(plan, rid, seen["routes"]))
            added += new + lent
            lines.append("%s +%d" % (role, len(new) + len(lent)))
        for rid, places in sorted(lifts.items()):                   # before the plans: a lift is its own commit, as `fill.py lift` makes it
            was = seen["routes"][rid]["max_ships"]
            print("%s: standing work, full while %d ship%s wait%s and its field carries more: max_ships %d -> %d%s"
                  % (rid, places, "" if places == 1 else "s", "s" if places == 1 else "", was, was + places, "" if "--write" in args else " (not written: add --write)"))
            if "--write" in args:
                print(raise_cap(root, data, who, rid, was + places, stamp)[1])
        if not added:
            print("nothing to add")
            return 0
        if "--write" not in args:
            print("not written: add --write")
            return 0
        ok, out = planfile.apply(root, data, sorted(changes), who, changes={name: (lambda plan, edits=edits: [edit(plan) for edit in edits]) for name, edits in changes.items()},
                                 extra=files, message="plans: fill.py adds open work (%s): %s" % ("; ".join(lines), ", ".join(sorted(set(added)))[:400]), commit=commit)
        print("\n".join(out))
        if ok:
            print("the dispatcher gives the routes to the ships within the minute (a ship on standing work when its run ends); read `fill.py` again in two minutes")
        return 0 if ok else 1

    if verb in ("add", "drop") and rest:
        rid = rest[0]
        mine = [r for r in seen["roles"] if division.ROLES.get(r) == who]
        role = value("--role", mine[0] if len(mine) == 1 else "")
        if role not in seen["roles"]:
            sys.exit("name the plan: --role <%s>" % "|".join(sorted(seen["roles"])))
        if not may_change(who, role):
            sys.exit("REFUSED: the %s plan is kept by %s (orders F1): ask in requests.log" % (role, division.ROLES.get(role)))
        name = planfile.division_of(role)
        if verb == "add":
            if rid not in seen["routes"]:
                sys.exit("no route file game/routes/%s.json: `routemaker.py route <candidate id>` prints one" % rid)
            if rid in seen["roles"][role]:
                sys.exit("%s stands in the %s plan already" % (rid, role))
            if "--first" in args:
                change = lambda plan: planfile.put_first(plan, [rid], head=True)
            elif len(planfile.roles_of(name)) > 1:                  # a division of two roles: the route is for the ships of the role named
                ships = [ship for ship, its, _row in planfile.crew_of(data, name) if its == role]
                change = lambda plan: planfile.put_own(plan, ships, rid, tail=True)
            else:
                change = lambda plan: planfile.put_then(plan, rid, seen["routes"])
        else:
            if rid not in seen["roles"][role]:
                sys.exit("%s is not in the %s plan" % (rid, role))
            change = lambda plan: planfile.take_out(plan, rid)
        word = "added" if verb == "add" else "taken out"
        ok, out = planfile.apply(root, data, [name], who, changes={name: change}, message="%s plan: %s %s (fill.py)" % (role, rid, word), commit=commit)
        print("\n".join(out))
        other = pull.class_reason(role, seen["routes"][rid], rid) if verb == "add" else None
        if other:                                              # rule F23: the Admiral's own word, said plainly
            print("note: %s is not %s work (%s): the dispatcher refuses it to the %s ships while data/fleet/class-guard-on exists; the route "
                  "file's `open_to` opens it to another class" % (rid, role, other, role))
        holds = [key for key, entry in routefiles.templates_of(root, name)[0].items() if rid in entry["routes"]] if verb == "drop" else []
        if holds:                                              # take_out reaches the lists and the ships' cells, never a template's own routes
            print("note: %s still stands in the template%s %s of the %s division: a ship that names it flies the route on. `plan.py template <name> <routes>` "
                  "writes the template without it" % (rid, "s" if len(holds) > 1 else "", ", ".join("@" + key for key in holds), name))
        return 0 if ok else 1

    if verb == "lift" and len(rest) == 2 and rest[1].isdigit() and int(rest[1]) >= 1:
        rid, ships = rest[0], int(rest[1])
        if rid not in seen["routes"]:
            sys.exit("no route file game/routes/%s.json" % rid)
        if who != "Unity" and not any(rid in ids and division.ROLES.get(role) == who for role, ids in seen["roles"].items()):
            sys.exit("REFUSED: %s stands in no plan of yours: put it into your plan first (`fill.py add %s`)" % (rid, rid))
        deep = carries(seen, seen["routes"][rid])
        most = max(1, (deep["ships"] or 0) + deep["extra"]) if deep else None
        if most is not None and ships > most:
            sys.exit("REFUSED: %s carries about %d ships, not %d: %s. Never all ships on one buyer or one field: put the others on other routes or on standing work "
                     "(the skill fleet-play, `Plan a Division`)" % (rid, most, ships, deep["text"]))
        ok, line = raise_cap(root, data, who, rid, ships, stamp)
        print(line)
        return 0 if ok else 1
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
