#!/usr/bin/env python3
"""fill.py -- keep every ship of a division at work: say why ships wait, and fill the plan with the work that stands open.

WHAT: the dispatcher gives a free pilot the first route of its role's plan that is open to it. A ship waits (docked,
      costing nothing) when every route of its plan is closed to it. This script reads the files the dispatcher
      reads and uses the dispatcher's own rule (dispatch.why_not), so the two cannot disagree. It
        status   per role: how many ships work, start and wait; for every route of the plan why it is closed to
                 the waiting pilots; then the work outside the plan: route files measured above zero with a free
                 place, the route maker's candidates with a ready route file, and what closes the rest
        check    the gate: no ship is idle (Suggi, 2026-11-16). PASS: no ship of the role waits. HALT (exit 1): ships
                 wait; the line says whether paying work or a test stands open (fill adds it) or whether the plan
                 lacks standing work for them (a route that trains or gathers: routes.py `standing`)
        fill     puts that work into the plan, in front of the census and the park route: the paying routes, then
                 up to --tests tests of one ship each. With --write it writes the route files and the plan,
                 rebuilds the three index files, runs the route gate and commits by path as the member
        add, drop, lift   one change to a plan, or to a route's `max_ships`, gated and committed the same way
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
  - `fill --once` adds only missions that pay once and buy nothing: the five-minute job runs it for every role, so a
    new once route reaches every plan without waiting for a turn (requests ENT-144).
  - A list of the route maker older than an hour is no ground for PASS while ships wait: the gate says so.
WHY:  a plan of one-ship tests and routes that pay once left 102 of 146 ships docked while the route files that
      paid stood in other plans, and finding out why took a turn. One command shows it and one command fills it.

USAGE:
  fill.py [status] [<Member>|<role>|all]
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
import routes as routefiles                       # noqa: E402  the route gate and the three index files

STALE = 60 * 60                # a list of the route maker older than this is no ground for PASS
HOURS = 4                      # a turn: what a bid must carry
INDEXES = ("routes/index.md", "routes/plan.md", "routes/master-index.md")


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


def proven(route):
    """True for a route measured above zero on two runs or more: one good run is a test result, not yet a route that pays."""
    return (worth(route) or 0) > 0 and ((route.get("measured") or {}).get("runs") or 0) >= 2


def buys(route):
    """True for a route with a stop that buys goods: such a route is never added as a test by itself."""
    return any(isinstance(stop, dict) and stop.get("buy") for stop in route.get("stops") or [])


def survey(root, data, now=None):
    """Everything the answers rest on, read once: plans, route files, the candidates, and the dispatcher's next pass
    played through for every free pilot of the fleet, in its order: who starts on its own plan, who waits and why."""
    now = time.time() if now is None else now
    roles, owners, _errors = division.load_plan(root)
    routes = dispatch.load_routes(root)
    rows = dispatch.run_rows(data)
    state = {"now": now, "data": data, "rows": rows, "orders": dispatch.fresh_orders(data, now), "rest": dispatch.resting(routes, rows, now),
             "booked": dispatch.booked(data), "loss": dispatch.losing(routes, rows, now),
             "late": dispatch.lately_losing(routes, rows, now)}
    by_route = {}
    for row in rows:
        by_route.setdefault(row.get("route"), []).append(row)
    named = dispatch.flagships(data)
    ammo = set(dispatch.read_json(Path(data) / "catalog" / "ammo.json", []) or [])
    fleet = dispatch.read_json(Path(data) / "fleet" / "fleet.json", {})
    blank = lambda: {"ships": 0, "work": [], "hand": [], "away": [], "starting": [], "waiting": [], "reasons": {}}
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
        elif (ship.get("activity") or {}).get("kind") != "idle":
            crew["hand"].append(name)                  # the engine runs a loop or a goal for it: given by hand
        else:
            pilot, why = dispatch.pilot_of(ship, named, data, ammo), []
            for rid in roles.get(role) or []:
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
    return {"now": now, "data": data, "root": root, "roles": roles, "owners": owners, "routes": routes, "state": state, "crews": crews, "by_route": by_route, "named": named,
            "played": played, "taken": {}, "candidates": book.get("candidates") or [], "list_age": age_of(book.get("written_at") or "", now),
            "fleet_at": fleet.get("updated_at") or "?" if isinstance(fleet, dict) else "?"}


HOLD = 65                      # a starter's hold, units


def regains(seen):
    """What comes back per hour by our own readings (hive.py `rates`), read once per survey."""
    if "rates" not in seen:
        import hive                                # here, not at the top: hive.py reads fill.py for the standing fleet
        seen["rates"] = hive.rates(seen["data"])
    return seen["rates"]


def carries(seen, route):
    """How many ships a route carries, from our own readings: {"ships": what it carries hour after hour (None: not
    measured), "extra": ships more for one turn while today's standing order or field holds, "text": what both rest
    on}; None for a route nothing of this limits (a circuit, a census) or that no reading speaks of. A mine route that
    sells is carried by what its bid regains per hour at its best price, shared by the routes that sell the same good
    at the same station; one that sells nothing by what its field grows back; a hunt by one hunter (the herd's regain
    is named). The standing depth of a bid is one order: it can leave within the hour (errors ENT-046, ENT-054)."""
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
        if rate is None and not stands:
            return None
        text = ("the %s bid at %s regains %s units an hour at its best price" % (item, base, format(int(rate[0]), ",")) if rate is not None
                else "what the %s bid at %s regains is not measured" % (item, base))
        text += "; %s units stand at %s cr now, one order that can leave within the hour" % (format(depth, ","), row["best_buy"]) if stands else "; no bid at its price now"
        text += "; %d routes share the bid" % same if same > 1 else ""
        return {"ships": None if rate is None else int(rate[0] / per_ship / same), "extra": int(depth // (per_ship * HOURS) // same), "text": text}
    place = str(route.get("belt", ""))
    system, poi = (place.split(":") + [""])[:2]
    back = [rate[0] for key, rate in fields.items() if key[0] == system and key[1] == poi]
    left = dispatch.field_left(seen["data"], place, seen["now"], fresh=float("inf")) or {}
    if not back and not left:
        return None
    text = "its field grew back %s units an hour" % format(int(sum(back)), ",") if back else "what its field grows back is not measured"
    text += "; %s units lie in it" % format(sum(left.values()), ",") if left else ""
    return {"ships": int(sum(back) / per_ship) if back else None, "extra": int(sum(left.values()) // (per_ship * HOURS)), "text": text}


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
    """What one role's ships do now and what would give its waiting ships work.
    {ships, work, hand, away, starting [(pilot, route)], waiting [pilot], idle [pilot left without any offer],
     plan [(route id, flying, cap, Counter of reasons, hint)], paying [(route id, worth, pilots)],
     tests [(route id, estimate, route to write or None, pilot)], closed {reason: [(worth, route id)]}}"""
    crew = seen["crews"].get(role) or {"ships": 0, "work": [], "hand": [], "away": [], "starting": [], "waiting": [], "reasons": {}}
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
    left = list(waiting)
    paying, closed = [], {}

    def offer(rid, route, value, limit=None):
        """The waiting pilots the route is open to, taken off the list; the commonest reason when there are none."""
        took, why = [], Counter()
        for pilot in list(left):
            if limit is not None and len(took) >= limit:
                break
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
               if rid not in plan and route.get("status") != "off" and not route.get("park") and route.get("kind") != "census" and proven(route)]
    by_hand = []
    for value, rid, route in sorted(outside, key=lambda r: (-r[0], r[1])):
        if buys(route):                                           # it buys goods: in a plan by its Admiral's word only, never by this script
            by_hand.append((value, rid))
            continue
        if route.get("once") and refused_to(seen, rid, role):
            closed.setdefault("the board refused it to this role", []).append((value, rid))
            continue
        took = offer(rid, route, value) if left else []
        if took:
            paying.append((rid, value, took))
    found, seen_ids = [], set(plan) | {rid for rid, _v, _t in paying} | {rid for _v, rid in by_hand}
    for cand in sorted(seen["candidates"], key=lambda c: -(c.get("per_ship_hour") or 0)):
        draft = cand.get("route")
        if not isinstance(draft, dict) or cand.get("needs") or (cand.get("per_ship_hour") or 0) < floor or str(cand.get("status", "")).startswith("off"):
            continue
        rid = cand.get("route_id") or draft.get("id")
        if not rid or rid in seen_ids or (rid in routes and (proven(routes[rid]) or (worth(routes[rid]) is not None and worth(routes[rid]) <= 0))):
            continue                                              # proven ones are judged above, by their figure; one measured at a loss is no test
        seen_ids.add(rid)
        route = routes.get(rid) or dict(draft, id=rid)
        if route.get("once") and refused_to(seen, rid, role):
            continue
        if buys(route):                                           # a gap is flown once by hand, with one load (errors.log ENT-027)
            by_hand.append((cand["per_ship_hour"], rid))
            continue
        took = offer(rid, route, cand["per_ship_hour"], limit=1) if left and len(found) < tests else []
        if took:
            found.append((rid, cand["per_ship_hour"], None if rid in routes else route, took[0]))
    seen["taken"] = {name: what for name, what in state["orders"].items() if name not in seen["played"]}
    return {"role": role, "owner": seen["owners"].get(role) or division.ROLES.get(role, "?"), "ships": crew["ships"], "work": crew["work"], "hand": crew["hand"],
            "away": crew["away"], "starting": starting, "waiting": [p["name"] for p in waiting], "idle": [p["name"] for p in left], "plan": rows,
            "paying": paying, "tests": found, "closed": closed, "by_hand": sorted(by_hand, reverse=True)}


def verdict(seen, got):
    """(True for PASS, the line). No ship is idle (Suggi, 2026-11-16): PASS only when no ship of the role waits."""
    waiting, places, tests = len(got["waiting"]), sum(len(p) for _r, _v, p in got["paying"]), len(got["tests"])
    if not waiting:
        return True, "PASS: no ship of %s waits" % got["role"]
    if places or tests:
        return False, ("HALT: %d ships of %s wait while %d places of paying work and %d tests stand open: python3 -I -B game/fleet/fill.py fill %s --write"
                       % (waiting, got["role"], places, tests, got["role"]))
    if seen["list_age"] > STALE:
        return False, ("HALT: %d ships of %s wait and the route maker's list is %s old, so no test can be named: its service fails; write to the Fleet Admiral in requests.log"
                       % (waiting, got["role"], "%d minutes" % (seen["list_age"] // 60) if seen["list_age"] != float("inf") else "missing or not dated"))
    return False, ("HALT: %d ships of %s wait and nothing that pays is open to them: the plan lacks standing work for them (a route that trains or gathers, each "
                   "sized by what its place carries: the skill fleet-play, `Plan a Division`); what closes each route is listed by `fill.py status %s`"
                   % (waiting, got["role"], got["role"]))


def show(seen, got):
    def short(names):
        return ", ".join(names[:3]) + (" ..." if len(names) > 3 else "")
    print("FILL | %s (%s) | %d ships: %d at work, %d starting, %d waiting, %d by hand, %d away | fleet file %s"
          % (got["role"], got["owner"], got["ships"], len(got["work"]), len(got["starting"]), len(got["waiting"]), len(got["hand"]), len(got["away"]), seen["fleet_at"]))
    if got["waiting"]:
        print("  the plan, in its order                    flying/cap  closed to the %d waiting pilots because" % len(got["waiting"]))
        for n, (rid, flying, cap, why, hint) in enumerate(got["plan"], 1):
            print("  %2d %-38s %3d/%-5s  %s%s" % (n, rid[:38], flying, cap if cap else "-", ", ".join("%s %d" % kv for kv in why.most_common(4)) or "--", (" | " + hint) if hint else ""))
        if got["paying"] or got["tests"]:
            print("  open outside the plan (fill adds it):")
            for rid, value, pilots in got["paying"]:
                print("     PAYING %-38s %s measured, %d of the waiting pilots (%s)" % (rid[:38], format(int(value), ","), len(pilots), short(pilots)))
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
    if seen["list_age"] > STALE / 2:
        print("  NOTE: the route maker's list is %s old" % ("%d minutes" % (seen["list_age"] // 60) if seen["list_age"] != float("inf") else "missing or not dated"))
    ok, line = verdict(seen, got)
    print("  " + line)
    return ok


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def commit(root, data, who, files, message):
    """Write {path relative to the game folder: text} with the three index files, run the route gate, commit by path as
    `who`. (True, the commit's line) or (False, why); on a failure every file is put back."""
    if (Path(data) / "fleet" / "STOP").exists():
        return False, "REFUSED: fleet/STOP exists: nothing is changed while the fleet is halted"
    (Path(data) / "routes").mkdir(parents=True, exist_ok=True)
    with open(Path(data) / "routes" / "fill.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)                           # one writer of the plans at a time, from the check to the commit
        dirty = git(root, "status", "--porcelain", "--", "routes")[1].strip()
        if dirty:
            return False, "REFUSED: game/routes holds a change that is not committed; commit it or take it back first:\n" + dirty
        paths = sorted(set(files) | set(INDEXES))
        new = [rel for rel in paths if not (Path(root) / rel).exists()]
        for rel, text in files.items():
            (Path(root) / rel).write_text(text, encoding="ascii")
        routefiles.write_index(root)
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


def plan_text(root, role, change, note):
    """The plan file of a role after `change(list of route ids)`, with one dated line added to its note."""
    path = Path(root) / "routes" / "plans" / (role + ".json")
    plan = json.loads(path.read_text(encoding="ascii"))
    plan["routes"] = change(list(plan["routes"]))
    plan["note"] = (str(plan.get("note") or "") + " " + note).strip()
    return json.dumps(plan, indent=1) + "\n"


def after_the_once(seen, ids, new):
    """The list with `new` put behind its last route that pays once (at the head when it holds none): the once line stays together."""
    at = max((n + 1 for n, rid in enumerate(ids) if (seen["routes"].get(rid) or {}).get("once")), default=0)
    return ids[:at] + [rid for rid in new if rid not in ids] + ids[at:]


def before_the_wait(seen, ids, new):
    """The list with `new` put in front of the first census or park route (the routes that only read and wait)."""
    at = next((n for n, rid in enumerate(ids) if (seen["routes"].get(rid) or {}).get("park") or (seen["routes"].get(rid) or {}).get("kind") == "census"), len(ids))
    return ids[:at] + [rid for rid in new if rid not in ids] + ids[at:]


def may_change(who, role):
    return who == "Unity" or division.ROLES.get(role) == who


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data", "--tests", "--floor", "--role"))]
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
        files, lines, added = {}, [], []
        for role in chosen:
            if not may_change(who, role):
                sys.exit("REFUSED: the %s plan is kept by %s (orders F1): ask in requests.log" % (role, division.ROLES.get(role)))
            got = read_role(seen, role, floor, tests)
            once = "--once" in args                                 # only missions that pay once (they buy nothing: read_role keeps buying routes out)
            paying = [rid for rid, _v, _p in got["paying"] if not once or seen["routes"][rid].get("once")]
            found = [] if once else got["tests"]
            new = paying + [rid for rid, _v, _d, _p in found]
            print("%s: %d waiting; %d %s and %d tests to add%s" % (role, len(got["waiting"]), len(paying), "routes that pay once" if once else "paying routes", len(found),
                                                                   ": " + ", ".join(new) if new else ""))
            if not new:
                continue
            for rid, estimate, draft, _pilot in found:
                if draft is not None:
                    draft = dict(draft, max_ships=1)
                    draft["note"] = (str(draft.get("note") or "") + " Added as a test by fill.py on %s (%s): one ship until its first RESULT line is read." % (stamp, who)).strip()
                    files["routes/%s.json" % rid] = json.dumps(draft, indent=1) + "\n"
                    seen["routes"][rid] = draft
            note = "%s (fill.py, %s): added %s, open to ships that waited." % (stamp, who, ", ".join(new))
            files["routes/plans/%s.json" % role] = plan_text(root, role, lambda ids, new=new: (after_the_once if once else before_the_wait)(seen, ids, new), note)
            added += new
            lines.append("%s +%d" % (role, len(new)))
        if not files:
            print("nothing to add")
            return 0
        if "--write" not in args:
            print("not written: add --write")
            return 0
        ok, line = commit(root, data, who, files, "plans: fill.py adds open work for waiting ships (%s): %s" % ("; ".join(lines), ", ".join(sorted(set(added)))[:400]))
        print(line)
        if ok:
            print("the dispatcher gives the routes to the waiting ships within the minute; read `fill.py` again in two minutes")
        return 0 if ok else 1

    if verb in ("add", "drop") and rest:
        rid = rest[0]
        mine = [r for r in seen["roles"] if division.ROLES.get(r) == who]
        role = value("--role", mine[0] if len(mine) == 1 else "")
        if role not in seen["roles"]:
            sys.exit("name the plan: --role <%s>" % "|".join(sorted(seen["roles"])))
        if not may_change(who, role):
            sys.exit("REFUSED: the %s plan is kept by %s (orders F1): ask in requests.log" % (role, division.ROLES.get(role)))
        if verb == "add":
            if rid not in seen["routes"]:
                sys.exit("no route file game/routes/%s.json: `routemaker.py route <candidate id>` prints one" % rid)
            if rid in seen["roles"][role]:
                sys.exit("%s stands in the %s plan already" % (rid, role))
            change = (lambda ids: [rid] + ids) if "--first" in args else (lambda ids: before_the_wait(seen, ids, [rid]))
        else:
            if rid not in seen["roles"][role]:
                sys.exit("%s is not in the %s plan" % (rid, role))
            change = lambda ids: [r for r in ids if r != rid]
        word = "added" if verb == "add" else "taken out"
        ok, line = commit(root, data, who, {"routes/plans/%s.json" % role: plan_text(root, role, change, "%s (fill.py, %s): %s %s." % (stamp, who, rid, word))},
                          "%s plan: %s %s (fill.py)" % (role, rid, word))
        print(line)
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
        route = json.loads((Path(root) / "routes" / (rid + ".json")).read_text(encoding="ascii"))
        was = route.get("max_ships")
        route["max_ships"] = ships
        route["note"] = (str(route.get("note") or "") + " %s (fill.py, %s): max_ships %s -> %d." % (stamp, who, was if was else "none", ships)).strip()
        ok, line = commit(root, data, who, {"routes/%s.json" % rid: json.dumps(route, indent=1) + "\n"}, "%s: max_ships %s -> %d (fill.py, %s)" % (rid, was if was else "none", ships, who))
        print(line)
        return 0 if ok else 1
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
