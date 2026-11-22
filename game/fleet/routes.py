#!/usr/bin/env python3
"""routes.py -- check the route files, write their index, and attach what the runs measured.

WHAT: game/routes/<id>.json are the fleet's tasks (game/routes/BLUEPRINT.md); game/routes/plans/<role>.json
      lists them per role, one file per role, kept by the role's Admiral; game/routes/templates/<division>.json
      holds a division's templates (named lists of routes a ship's plan row names as `@<name>`, plan.py). This script
        check     validates every route file, the plans and the templates files (the gate);
        index     writes into game/routes/: master-index.md (the groups of routes and the plans at
                  a glance; every name is a link into a sub-index), one index per group of routes
                  (index-<group>.md: every route of the group with its measured figures and its
                  zone), one plan per role (plan-<role>.md: the role's routes in their order,
                  the ships planned on each, the templates its ships fly and what is planned; no
                  figure, since what a route earns changes by the hour) and one page per division
                  that has templates (templates-<division>.md); it removes a file it wrote once and
                  writes no longer;
        measure   reads the runs (data/routes/runs.jsonl) and prints, per route, runs,
                  minutes and credits per ship-hour over the readable runs that ended in the last
                  MEASURE_HOURS (12; a mission that pays once: all its runs); with --write it stores
                  the figures in the route file's `measured` block when they moved by a fifth or
                  more, and takes the block out of a repeating route without a readable run in the
                  window: it is a test again;
        idle      prints, and changes nothing: every route file with status off and the sentence of its note
                  that says why, then every route file that no plan and no template names
                  (data/plans/plan-*.md, game/routes/plans/*.json, game/routes/templates/*.json), with
                  its kind and when its last run in data/routes/runs.jsonl ended.
RULES:
  - A route's id is its file name; its systems are on the chart (game/map/galaxy.tsv).
  - A plan names only routes that exist and carries its role's Admiral as
    `owner`. The last route of every list is always open: the `park` route
    (dock and wait: a docked ship costs nothing) or a mine, not `off`, not
    `once`, without `max_ships`, `min_credits`, `requires` and
    `skip_if_booked`. A list that can run out leaves a ship adrift.
  - The index files are written by this script, never by hand; `check` fails on a stale one. No file
    holds every route or every plan: a group or a role that grows fills its own file (Suggi, 2026-11-16).
  - A route's group comes from its own file: once per pilot, paying (measured above zero), a
    test (not measured yet), a fitting, reading and waiting (census, park), measured at a loss,
    off. Its zone comes from the chart: home space when every system it touches is our
    empire's, beyond the border otherwise.
  - A measured block changes only on a real move, so a pass rarely makes a commit. A figure forgets: it rests
    on the runs of the last MEASURE_HOURS only, and a repeating route without a readable run in that window has
    no figure at all, good or bad (Suggi, 2026-11-16: the game changes by the hour; no route is marked bad for
    good). A block written before the window (without `hours`) is written again once.
  - A templates file names no pilot, holds templates of 2 to 40 lower-case letters, digits and dashes, each
    with one route or more that has a route file, and carries its division's Admiral as `owner`.
  - A hunt is not credited with what it got for goods it carried in from an
    earlier run: those were earned on another route.
  - A run is not credited or charged with what another hand of ours moved through its pilot's wallet
    while it flew: the wallet guard's top-ups between our own ships (wallet.py), like the weekly tax, a
    deposit into the faction's treasury (onetime.json, title TREASURY: money the Collective keeps), and a
    gift booked in the PRE seconds before the run's span that its first wallet did not yet hold.
  - A run that read no wallet (no credits before and after, both 0, or the note
    `wallet not read`) counts for nothing: a route whose runs are all such has
    no figure, and a figure built on them is taken out of its file.
WHY:  what a route pays is written next to the route, and a wrong file is caught
      before a pilot flies it.

USAGE:
  routes.py check | index | measure | idle         [--root <dir>] [--data <dir>]
  routes.py measure --write <route id>... | --role <role> | --all
                    writes the measured block of the routes named, of a role's plan, or of every route (the hourly
                    job); without one of the three it writes nothing and says so

Stdlib only. ASCII only.
"""

import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import division                                   # noqa: E402  the plan files and who keeps them
import workclass                                  # noqa: E402  r22: whose work a route is, the sale rule's switch
import taxes                                      # noqa: E402  the weekly tax a run in flight carried

KINDS = {"circuit": ("stops",), "hunt": ("place", "sell_at"), "census": ("systems",), "mine": ("belt", "station"), "guard": ("guards", "station")}
PLACES = {"mine": "belt", "hunt": "place"}       # the kinds that work at one place, and the field that names it: what a guard keeps
FRONT = "---\nname: %s\nid: %s\ntier: intel\nauthor: Unity\n---\n\n"
MASTER = "master-index.md"
WRITTEN = "`python3 -B game/fleet/routes.py index`, never by hand"       # every file `index` writes says so
MEASURE_HOURS = 12             # a figure rests on the readable runs that ended in this window: the game changes by the hour
TEMPLATE = re.compile(r"[a-z][a-z0-9-]{1,39}")        # a template's name (fullmatch): 2 to 40 lower-case letters, digits and dashes, a letter first
STAGES = (("once", "Once per Pilot", "Missions and rewards the game pays once per pilot: a new pilot's first work, and seed money."),
          ("paying", "Paying Routes", "Work that repeats and whose runs of the last %d hours measured above zero." % MEASURE_HOURS),
          ("test", "Tests", "Work that repeats and has no measured figure: new, or no readable run in the last %d hours. One ship until its first "
           "RESULT line is read." % MEASURE_HOURS),
          ("fit", "Fitting", "A module bought and fitted: the tool a kind of work needs."),
          ("service", "Standing Work, Reading and Waiting", "Standing work (it trains a skill or gathers into storage and is not judged on its pay), the census and the park "
           "route: they keep every ship busy and the picture fresh."),
          ("losing", "Measured at a Loss", "Work that repeats and whose runs of the last %d hours measured zero or below." % MEASURE_HOURS),
          ("off", "Off", "Written down, not flown."))
SLUGS = {"once": "once-per-pilot", "paying": "paying-routes", "test": "tests", "fit": "fitting", "service": "standing-work",
         "losing": "measured-at-a-loss", "off": "off"}               # a group's sub-index: index-<slug>.md


def read_json(path):
    return json.loads(Path(path).read_text(encoding="ascii"))


def chart(root):
    out = set()
    path = Path(root) / "map" / "galaxy.tsv"
    if path.is_file():
        for line in path.read_text(encoding="ascii", errors="replace").splitlines():
            if line and not line.startswith("#"):
                out.add(line.split("\t")[0])
    return out


def routes_of(root):
    out, errors = {}, []
    for path in sorted((Path(root) / "routes").glob("*.json")):
        if path.name == "plan.json":
            continue
        try:
            out[path.stem] = read_json(path)
        except (OSError, ValueError) as error:
            errors.append("game/routes/%s: not readable as ASCII JSON: %s" % (path.name, error))
    return out, errors


def plan_module():
    """game/fleet/plan.py, which knows the divisions, their Admirals (DIVISIONS) and their roles (roles_of): imported
    when first asked, not at the top, since plan.py imports this file."""
    import plan
    return plan


def templates_path(root, name):
    """A division's templates file: game/routes/templates/<division>.json."""
    return Path(root) / "routes" / "templates" / (name + ".json")


def template_divisions(root):
    """The divisions that have a templates file, by name; a file whose name is no division is the gate's to name."""
    folder = Path(root) / "routes" / "templates"
    known = plan_module().DIVISIONS
    return sorted(path.stem for path in folder.glob("*.json") if path.stem in known) if folder.is_dir() else []


def templates_of(root, name, text=None):
    """({template: {title, routes, trains, note}} in the file's order, its `owner`, [errors]) of a division's templates
    file, or of `text` when given (a change not written yet); ({}, "", []) when the division has none. The one reader:
    plan.py expands a ship's `@<name>` by it, and this file's gate and pages read it."""
    where = "game/routes/templates/%s.json: " % name
    if text is None:
        path = templates_path(root, name)
        if not path.is_file():
            return {}, "", []
        try:
            text = path.read_text(encoding="ascii")
        except (OSError, UnicodeDecodeError) as error:
            return {}, "", [where + "not readable as ASCII: %s" % error]
    try:
        spec = json.loads(text)
    except ValueError as error:
        return {}, "", [where + "not readable as JSON: %s" % error]
    if not isinstance(spec, dict) or spec.get("division") != name or not isinstance(spec.get("templates"), dict):
        return {}, "", [where + "needs `division` equal to the file name and an object `templates`"]
    out, errors = {}, []
    words = lambda value: isinstance(value, str) and all(ord(c) < 128 for c in value)
    for key, entry in spec["templates"].items():
        if not TEMPLATE.fullmatch(key) or division.pilots_named(key):
            errors.append(where + "`%s` is no template name: 2 to 40 lower-case letters, digits and dashes, a letter first, never a pilot's name" % key)
            continue
        entry = entry if isinstance(entry, dict) else {}
        ids, trains = entry.get("routes"), entry.get("trains", [])
        if not isinstance(ids, list) or not all(isinstance(rid, str) for rid in ids):
            errors.append(where + "the template `%s` needs `routes`, a list of route ids in the order a ship tries them" % key)
            continue
        if not all(words(entry.get(field, "")) for field in ("title", "note")) or not isinstance(trains, list) or not all(words(t) for t in trains):
            errors.append(where + "the template `%s`: `title` and `note` are ASCII texts and `trains` a list of skills" % key)
            continue
        out[key] = {"title": entry.get("title", ""), "routes": list(ids), "trains": list(trains), "note": entry.get("note", "")}
    return out, str(spec.get("owner") or ""), errors


def template_faults(templates, routes):
    """What is wrong with a division's templates beside the route files, one line each: a template without a route, a
    route with no file, an `@` among its routes (a template holds route ids, never another template). The one rule:
    plan.py's check halts a plan on it and this file's gate fails on it."""
    out = []
    for key, entry in templates.items():
        if not entry["routes"]:
            out.append("the template `%s` holds no route" % key)
        for rid in entry["routes"]:
            if rid.startswith("@"):
                out.append("the template `%s` names `%s`: a template holds route ids, never another template" % (key, rid))
            elif rid not in routes:
                out.append("the template `%s` names `%s`, which is no route file" % (key, rid))
    return out


def systems_of(route):
    places = []
    if route.get("kind") == "circuit":
        places += [str(s.get("at", "")) for s in route.get("stops") or [] if isinstance(s, dict)]
        places += [str(step.get("at", "")) for s in route.get("stops") or [] if isinstance(s, dict)
                   for key in ("mine", "hunt") for step in s.get(key) or [] if isinstance(step, dict)]
    places += [str(route.get(k, "")) for k in ("place", "sell_at", "belt", "station")]
    return [p.split(":")[0] for p in places if p] + list(route.get("systems") or [])


def closes(route):
    """What keeps a route from being always open, as the last route of a plan must be: the fields that limit it, or
    `limits` for a route that is neither the `park` route nor a mine; [] for one that is always open."""
    closed = [key for key in ("once", "max_ships", "min_credits", "requires", "skip_if_booked") if route.get(key)] + (["status off"] if route.get("status") == "off" else [])
    return closed or ([] if route.get("park") or route.get("kind") == "mine" else ["limits"])


def check(root):
    routes, errors = routes_of(root)
    known = chart(root)
    for rid, route in routes.items():
        where = "game/routes/%s.json: " % rid
        named = division.pilots_named(json.dumps(route))
        if named:                                  # the repository is public: which pilot flies what stays in the data folder (requests ENT-052)
            errors.append(where + "names a pilot of ours (%s): write the role and a count; which ship stays in the data folder" % ", ".join(named[:5]))
        if not isinstance(route, dict) or route.get("id") != rid:
            errors.append(where + "`id` must equal the file name")
            continue
        kind = route.get("kind")
        if kind not in KINDS:
            errors.append(where + "`kind` must be one of %s" % ", ".join(sorted(KINDS)))
            continue
        for field in ("title",) + KINDS[kind]:
            if not route.get(field):
                errors.append(where + "`%s` is missing" % field)
        if kind == "guard" and route.get("guards"):    # a guard keeps the place of a route of ours, or follows a circuit's pilot (ENT-217)
            guarded = routes.get(str(route["guards"]))
            if not isinstance(guarded, dict):
                errors.append(where + "`guards` names `%s`, which is no route file" % route["guards"])
            elif guarded.get("kind") != "circuit" and guarded_place(route, guarded) is None:
                errors.append(where + "`guards` names `%s`, a %s: a guard keeps the place of a mine or a hunt, and it has none" % (route["guards"], guarded.get("kind") or "route without a kind"))
        if kind == "circuit":
            for n, stop in enumerate(route.get("stops") or [], 1):
                if not isinstance(stop, dict) or len(str(stop.get("at", "")).split(":")) != 3:
                    errors.append(where + "stop %d: `at` must be system:poi:base" % n)
                    continue
                for key in ("mine", "hunt"):
                    for step in stop.get(key) or []:
                        if not isinstance(step, dict) or len(str(step.get("at", "")).split(":")) != 2:
                            errors.append(where + "stop %d: the `at` of a `%s` step must be system:poi" % (n, key))
                for job in stop.get("craft") or []:                  # route_run.py's craft step (requests ENT-013)
                    if not isinstance(job, dict) or not isinstance(job.get("recipe"), str) or not job["recipe"]:
                        errors.append(where + "stop %d: a `craft` entry needs `recipe`, a recipe id" % n)
                        continue
                    runs = job.get("runs")
                    if not isinstance(runs, int) or isinstance(runs, bool) or runs < 1:
                        errors.append(where + "stop %d: the `craft` of %s needs `runs`, a whole number of 1 or more" % (n, job["recipe"]))
                    if not (isinstance(job.get("makes"), str) and job["makes"]):
                        errors.append(where + "stop %d: the `craft` of %s needs `makes`: the runner counts what was made by that item in storage" % (n, job["recipe"]))
                if "unfit" in stop:
                    if not (isinstance(stop["unfit"], list) and stop["unfit"] and all(isinstance(m, str) and m for m in stop["unfit"])):
                        errors.append(where + "stop %d: `unfit` must be a non-empty list of module ids" % n)
                for want in stop["fit"] if isinstance(stop.get("fit"), list) else []:     # a `replace` or `count` of the fit step (requests ENT-290)
                    errors += [where + "stop %d: " % n + line for line in fit_faults(want)]
        levels = lambda value: isinstance(value, dict) and all(isinstance(v, int) and not isinstance(v, bool) for v in value.values())
        pos_counts = lambda value: isinstance(value, dict) and bool(value) and all(isinstance(k, str) and k and isinstance(v, int) and not isinstance(v, bool) and v >= 1 for k, v in value.items())
        need = route.get("requires") if isinstance(route.get("requires"), dict) else {}
        if need.get("hold") and need.get("empty_hold"):
            errors.append(where + "`requires.hold` and `requires.empty_hold` together close the route to every pilot")
        if "skills_below" in need and not levels(need["skills_below"]):
            errors.append(where + "`requires.skills_below` must be {skill: level}")
        if "modules_below" in need and not pos_counts(need["modules_below"]):
            errors.append(where + "`requires.modules_below` must be {module_id: count >= 1}")
        if "any_module" in need and not (isinstance(need["any_module"], list) and need["any_module"] and all(isinstance(m, str) and m for m in need["any_module"])):
            errors.append(where + "`requires.any_module` must be a non-empty list of module ids")
        if "module" in need and not ((isinstance(need["module"], str) and need["module"]) or pos_counts(need["module"])
                                     or (isinstance(need["module"], list) and need["module"] and all(isinstance(m, str) and m for m in need["module"]))):
            errors.append(where + "`requires.module` must be a module id, a non-empty list of module ids (any one of them) or {module_id: count >= 1}")
        if "without_module" in need and not ((isinstance(need["without_module"], str) and need["without_module"]) or (isinstance(need["without_module"], list) and need["without_module"] and all(isinstance(m, str) and m for m in need["without_module"]))):
            errors.append(where + "`requires.without_module` must be a module id or a non-empty list of module ids")
        if "reserve" in need:                          # requests ENT-266: the gate on a faction reserve (reserves.py)
            errors += [where + line for line in reserve_faults(need["reserve"])]
        if "ask" in need:                              # requests ENT-297: the buy end of a route (dispatch.ask_missing)
            errors += [where + line for line in ask_faults(need["ask"])]
        if "held_below" in need:                       # Q75 (1), errors.log ENT-111: what the division holds (heldgate.py)
            errors += [where + line for line in __import__("heldgate").faults(need["held_below"])]
        if "strict" in need and not isinstance(need["strict"], bool):     # requests ENT-332: dispatch.why_not reads true or false only
            errors.append(where + "`requires.strict` must be true (open only while strict classes are on) or false (only while off)")
        floors = [("`min_left`", route.get("min_left"))] + [("stop %d: the `min_left` of a `mine` step" % n, step.get("min_left"))
                                                             for n, stop in enumerate(route.get("stops") or [], 1) if isinstance(stop, dict)
                                                             for step in stop.get("mine") or [] if isinstance(step, dict)]
        for label, floor in floors:
            if floor is not None and not levels(floor):
                errors.append(where + label + " must be {resource: units}")
        for key, parts in (("place", 2), ("belt", 2), ("sell_at", 3), ("station", 3)):
            if route.get(key) and len(str(route[key]).split(":")) != parts:
                errors.append(where + "`%s` must have %d parts joined by a colon" % (key, parts))
        for system in systems_of(route):
            if known and system not in known:
                errors.append(where + "system `%s` is not on the chart" % system)
    errors += gift_faults(routes)                 # r22: a gift goes to a role or a flagship of ours, never to a stranger
    roles, _owners, plan_errors = division.load_plan(root)
    errors += plan_errors
    if (Path(root) / "routes" / "plan.json").exists():
        errors.append("game/routes/plan.json: the one plan file is gone; each role has game/routes/plans/<role>.json")
    for role, ids in roles.items():
        where = "game/routes/plans/%s.json: " % role
        named = division.pilots_named(current_plan(root, role))
        if named:
            errors.append(where + "names a pilot of ours (%s): `Planned` is read by every member and the public; write the role and a count" % ", ".join(named[:5]))
        for rid in ids:
            if rid not in routes:
                errors.append(where + "names `%s`, which is no route file" % rid)
        last = routes.get(ids[-1]) if ids else None
        if last is not None and closes(last):
            errors.append(where + "must end with a route that is always open (the `park` route, or a mine, without %s); `%s` is not, and a list that runs out leaves a ship adrift"
                          % (", ".join(closes(last)), ids[-1]))
        if not ids:
            errors.append(where + "`routes` is empty: end it with the `park` route")
    folder = Path(root) / "routes" / "templates"
    keepers = plan_module().DIVISIONS if folder.is_dir() else {}
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:     # a division's templates (plan.py `template`)
        where = "game/routes/templates/%s: " % path.name
        if path.stem not in keepers:
            errors.append(where + "`%s` is no division of the fleet (%s)" % (path.stem, ", ".join(sorted(keepers))))
            continue
        try:
            named = division.pilots_named(path.read_text(encoding="ascii"))
        except (OSError, UnicodeDecodeError):
            named = []                                 # templates_of names the fault
        if named:                                      # the repository is public: a template is read by everyone (requests ENT-052)
            errors.append(where + "names a pilot of ours (%s): a template is read by every member and the public; write the role and a count" % ", ".join(named[:5]))
        templates, owner, faults = templates_of(root, path.stem)
        errors += faults
        if not faults and owner != keepers[path.stem]:
            errors.append(where + "`owner` must be %s, who keeps the %s division" % (keepers[path.stem], path.stem))
        errors += [where + line for line in template_faults(templates, routes)]
    if routes:
        files = index_files(root, keep_id=True)
        for name in files:
            if files[name] != current_index(root, name):
                errors.append("game/routes/%s is missing or stale: run `python3 -B game/fleet/routes.py index` (master-index.md, every index-<group>.md, "
                              "every plan-<role>.md and every templates-<division>.md are written together)" % name)
        for name in stale(root):
            errors.append("game/routes/%s is written no longer (master-index.md and its sub-indexes took its place): run "
                          "`python3 -B game/fleet/routes.py index`, which removes it" % name)
    return errors, len(routes)


def reserve_faults(need):
    """reserves.faults, imported here: reserves.py imports this file to read a run's end."""
    import reserves
    return reserves.faults(need)


ASK_FIELDS = ("item", "base", "max_price", "min_qty", "max_age_minutes")


def ask_faults(need):
    """What is wrong with a route's `requires.ask` (dispatch.ask_missing reads it): one {item, base, max_price,
    min_qty, max_age_minutes} or a list of them; `item` and `base` ids, `max_price` a number above 0, `min_qty` and
    `max_age_minutes` whole numbers of 1 or more when given (requests ENT-297)."""
    wants = [need] if isinstance(need, dict) else need if isinstance(need, list) and need else None
    if wants is None:
        return ["`requires.ask` must be {item, base, max_price, min_qty, max_age_minutes} or a list of them"]
    out = []
    for want in wants:
        if not isinstance(want, dict):
            out.append("`requires.ask` holds an entry that is no {item, base, max_price}")
            continue
        for key in ("item", "base"):
            if not (isinstance(want.get(key), str) and want[key]):
                out.append("`requires.ask` needs `%s`, an id" % key)
        price = want.get("max_price")
        if not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
            out.append("`requires.ask` of %s needs `max_price`, the most a unit may be asked, above 0" % want.get("item"))
        for key in ("min_qty", "max_age_minutes"):
            value = want.get(key)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 1):
                out.append("`requires.ask` of %s: `%s` must be a whole number of 1 or more" % (want.get("item"), key))
        unknown = sorted(set(want) - set(ASK_FIELDS))
        if unknown:
            out.append("`requires.ask` of %s names fields no reader knows: %s" % (want.get("item"), ", ".join(unknown)))
    return out


def fit_faults(want):
    """What is wrong with a `fit` entry of a circuit stop (`replace` or `count`, route_run.py's fit step,
    requests ENT-290): `module`, a module id; `max_price`, a number above 0; optional `count` >= 1; optional `replace`."""
    if not isinstance(want, dict) or ("replace" not in want and "count" not in want):
        return []
    if not (isinstance(want.get("module"), str) and want["module"]):
        return ["a `fit` entry needs `module`, a module id"]
    out = []
    price = want.get("max_price")
    if not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
        out.append("the `fit` of %s needs `max_price`, the most it may cost with tax, above 0" % want["module"])
    if "count" in want and (not isinstance(want["count"], int) or isinstance(want["count"], bool) or want["count"] < 1):
        out.append("the `fit` of %s: `count` must be a whole number of 1 or more" % want["module"])
    if "replace" in want and not (isinstance(want["replace"], str) and want["replace"] and want["replace"] != want["module"]):
        out.append("the `fit` of %s: `replace` names the module it takes the place of, an id other than `module`" % want["module"])
    return out


GIFT_DATA = None              # the data folder whose flagships a gift may name (None: division.DATA); a test sets its own


def gift_faults(routes):
    """What is wrong with the gifts of the route files (handover.py, r22), one line each: a circuit stop's `gift`, a
    mine route's `gift` (never with `deposit` faction: the faction's storage gives only with manage_treasury), a hunt
    route's `gift_to` (a receiver's word). The receiver is a role word or a flagship of ours: any other name is a
    stranger, and a gift to a stranger is a loss; a numbered pilot of ours is named by the gate's own rule."""
    import handover                                   # here, not at the top: handover.py imports workclass only
    flags = set(division.flagships(GIFT_DATA or division.DATA))
    out = []
    for rid, route in sorted(routes.items()):
        if not isinstance(route, dict):
            continue
        where = "game/routes/%s.json: " % rid
        for n, stop in enumerate(route.get("stops") or [], 1):
            if isinstance(stop, dict) and "gift" in stop:
                for value in stop["gift"] if isinstance(stop["gift"], list) else [stop["gift"]]:
                    out += [where + "stop %d: " % n + line for line in handover.faults(value, flags)]
        if route.get("kind") == "mine" and "gift" in route:
            out += [where + line for line in handover.faults(route["gift"], flags)]
            if route.get("deposit") == "faction":
                out.append(where + "`gift` with `deposit` faction: the faction's storage gives nothing without manage_treasury; gift from personal storage")
        if "gift_to" in route:
            if route.get("kind") != "hunt" or not isinstance(route["gift_to"], str):
                out.append(where + "`gift_to` is a hunt route's receiver: a role word or a flagship of ours")
            else:
                out += [where + line for line in handover.faults(route["gift_to"], flags)]
    return out


def gives(route):
    """True for a route whose goods go to a pilot of ours while data/fleet/strict-classes-on stands: a hunt route
    with `gift_to`, a circuit whose stops only give (workclass `deliver`). Standing work: no wallet moves by a gift,
    so its runs earn nothing of their own and the loss stop would close them; what they give is sold by Trade."""
    if not workclass.strict_on():
        return False
    return bool(route.get("kind") == "hunt" and route.get("gift_to")) or (route.get("kind") == "circuit" and workclass.work_class(route, None, True) == "deliver")


def module_needs(route):
    """{module id: True} of the modules a route's `requires.module` can be met by, or None when it asks none:
    a word is that module, a list any one of them, a dict every module it names."""
    need = (route.get("requires") or {}).get("module") if isinstance(route.get("requires"), dict) else None
    if isinstance(need, str) and need:
        return {need: True}
    if isinstance(need, list) and need:
        return {m: True for m in need if isinstance(m, str)}
    if isinstance(need, dict) and need:
        return {m: True for m in need}
    return None


def replaces(route):
    """True for a circuit with a `fit` entry that names a module it `replace`s (a refit route)."""
    return route.get("kind") == "circuit" and any(isinstance(w, dict) and w.get("replace") for s in route.get("stops") or [] if isinstance(s, dict)
                                                  for w in (s.get("fit") if isinstance(s.get("fit"), list) else []))


def fit_gate_warnings(root, routes):
    """[(fit route, role, route, module)]: a fit route of a role's plan takes the place of module M (`replace`) while
    another route of the same plan asks `requires.module` M and cannot be met by the module fitted instead: the refit
    ship is refused that route (errors.log ENT-128, requests ENT-343: 17 Laser III miners shut out for three hours)."""
    out = []
    for path in sorted((Path(root) / "routes" / "plans").glob("*.json")):
        try:
            ids = [r for r in (read_json(path).get("routes") or []) if isinstance(r, str)]
        except (OSError, ValueError, AttributeError):
            continue
        for fid in ids:
            fit = routes.get(fid) or {}
            for stop in fit.get("stops") or [] if fit.get("kind") == "circuit" else []:
                for want in stop.get("fit") or [] if isinstance(stop, dict) and isinstance(stop.get("fit"), list) else []:
                    old, new = (want.get("replace"), want.get("module")) if isinstance(want, dict) else (None, None)
                    if not (isinstance(old, str) and old):
                        continue
                    for rid in ids:                  # another fit route asks the old module by design: it is the refit's alternative
                        needs = module_needs(routes.get(rid) or {}) if rid != fid and not replaces(routes.get(rid) or {}) else None
                        if needs and old in needs and new not in needs:
                            out.append((fid, path.stem, rid, old))
    return sorted(set(out))


BUY_TAX = 1.01                 # route_run.TAX: the runner refuses an ask whose price with this tax tops a buy's max_price


def buy_limit_warnings(routes):
    """[(route id, stop number, item, the ask gate's max_price, the buy's max_price)] of the circuits whose
    `requires.ask` opens on an ask their own buy step refuses: the buy's max_price under the gate x BUY_TAX, so every
    run ends at its failed buy (requests ENT-357; errors.log ENT-138: gate 231, buy 231, ask 230, nothing bought)."""
    out = []
    for rid, route in sorted(routes.items()):
        if not isinstance(route, dict) or route.get("kind") != "circuit":
            continue
        need = route.get("requires") if isinstance(route.get("requires"), dict) else {}
        asks = need.get("ask")
        gates = {}
        for ask in ([asks] if isinstance(asks, dict) else asks if isinstance(asks, list) else []):
            if isinstance(ask, dict) and isinstance(ask.get("max_price"), (int, float)) and not isinstance(ask.get("max_price"), bool):
                gates[ask.get("item")] = max(gates.get(ask.get("item"), 0), ask["max_price"])
        for n, stop in enumerate(route.get("stops") or [], 1):
            for want in stop.get("buy") or [] if isinstance(stop, dict) and isinstance(stop.get("buy"), list) else []:
                limit = want.get("max_price") if isinstance(want, dict) else None
                gate = gates.get(want.get("item")) if isinstance(want, dict) else None
                if gate and isinstance(limit, (int, float)) and not isinstance(limit, bool) and limit < gate * BUY_TAX:
                    out.append((rid, n, want["item"], gate, limit))
    return out


def sale_warnings(routes):
    """[(route id, its strict class, the roles it is closed to)] of the routes that sell outside Trade's class: with
    data/fleet/strict-classes-on the dispatcher refuses them to every pilot that is not a trader (workclass.sales)."""
    rows, _by_class, _by_admiral = workclass.sales(routes, {})
    return [(rid, cls, closed) for rid, cls, closed, _admirals in rows]


def current_plan(root, role):
    """The text of a role's plan file, or '' when it cannot be read."""
    try:
        return (Path(root) / "routes" / "plans" / (role + ".json")).read_text(encoding="ascii")
    except (OSError, UnicodeDecodeError):
        return ""


def current_index(root, name=MASTER):
    path = Path(root) / "routes" / name
    return path.read_text(encoding="ascii") if path.is_file() else ""


def cell(value):
    return str(value).replace("|", "/").replace("\n", " ")


def atlas(root):
    """({system id: (empire, jumps from home or None)}, our empire) from the chart."""
    out, cols = {}, {}
    path = Path(root) / "map" / "galaxy.tsv"
    if path.is_file():
        for line in path.read_text(encoding="ascii", errors="replace").splitlines():
            if not line or line.startswith("#"):
                continue
            cells = line.split("\t")
            if cells[0] == "id":
                cols = {name: n for n, name in enumerate(cells)}
                continue
            at = cols.get("empire", 4)
            jumps = cells[cols["jumps_from_home"]] if "jumps_from_home" in cols and len(cells) > cols["jumps_from_home"] else ""
            out[cells[0]] = (cells[at] if len(cells) > at else "", int(jumps) if jumps.isdigit() else None)
    home = next((e for e, j in out.values() if j == 0), None) or next((e for e, _j in out.values()), "")
    return out, home


def zone(route, systems, home):
    """(`home space` or `beyond the border`, the jumps from home of its farthest system); `--` where the chart knows none of its systems."""
    seen = [systems[s] for s in systems_of(route) if s in systems]
    if not seen:
        return "--", None
    jumps = [j for _e, j in seen if j is not None]
    return ("home space" if all(e == home for e, _j in seen) else "beyond the border"), (max(jumps) if jumps else None)


def standing(route):
    """True for standing work: a route that keeps a ship busy between paying work and is not judged on its pay. It
    trains a skill or gathers into storage: `"standing": true` in its file, a route open only under a skill level
    (`requires.skills_below`), or a mine route that sells nothing (its load goes into the pilot's storage). Suggi,
    2026-11-16: no ship is idle; a ship without paying work levels and gathers. A guard is standing work too: it
    earns nothing and keeps another route's ship company (requests ENT-070)."""
    need = route.get("requires") or {}
    return bool(route.get("standing") or need.get("skills_below") or (route.get("kind") == "mine" and not route.get("sell"))
                or route.get("kind") == "guard" or gives(route))


def guarded_place(guard, guarded):
    """The system:poi a guard keeps: its own `place`, else the place of the route it guards (a mine's `belt`, a hunt's
    `place`); None when the guarded route is no mine and no hunt (a circuit, a census, a guard) or names no place."""
    if not isinstance(guarded, dict) or guarded.get("kind") not in PLACES:
        return None
    return str(guard.get("place") or guarded.get(PLACES[guarded["kind"]]) or "") or None


def stage(route):
    """The group a route stands in, from its own file (STAGES)."""
    measured = route.get("measured") or {}
    if route.get("status") == "off":
        return "off"
    if route.get("park") or route.get("kind") == "census" or standing(route):
        return "service"
    if any(isinstance(s, dict) and (s.get("fit") or s.get("unfit")) for s in route.get("stops") or []):
        return "fit"
    if route.get("once"):
        return "once"
    if not measured:
        return "test"
    return "paying" if (measured.get("cph_per_ship") or 0) > 0 else "losing"


def open_to(route):
    need = route.get("requires") or {}
    gate = ["the park route" if route.get("park") else "", "once per pilot" if route.get("once") else "",
            "up to %s ships" % route["max_ships"] if route.get("max_ships") else "", "%s pilots in all" % route["max_pilots"] if route.get("max_pilots") else "",
            "needs %s" % (" or ".join(need["module"]) if isinstance(need["module"], list) else need["module"]) if need.get("module") else "", "without %s" % need["without_module"] if need.get("without_module") else "",
            "empty hold" if need.get("empty_hold") else "", "goods aboard" if need.get("hold") else "", "from %s cr" % format(route["min_credits"], ",") if route.get("min_credits") else "",
            "after the reward %s" % (need["booked"] if isinstance(need["booked"], str) else ", ".join(need["booked"])) if need.get("booked") else "",
            "from %s" % ", ".join("%s %s" % (k, v) for k, v in sorted(need["skills"].items())) if isinstance(need.get("skills"), dict) and need["skills"] else "",
            "with %s" % ", ".join("%s %s stored at %s" % (w.get("min", 1), " or ".join(map(str, w["items"])) if isinstance(w.get("items"), list) else w.get("item"), w.get("at")) for w in ([need["stored"]] if isinstance(need["stored"], dict) else need["stored"]) if isinstance(w, dict)) if need.get("stored") else "",
            "while %s" % ", ".join("%s bids %s cr for %s" % (b.get("base"), b.get("min_price", 1), b.get("item")) for b in ([need["bid"]] if isinstance(need["bid"], dict) else need["bid"]) if isinstance(b, dict)) if need.get("bid") else "",
            "while %s" % ", ".join("%s asks %s cr or less for %s" % (a.get("base"), a.get("max_price"), a.get("item")) for a in ([need["ask"]] if isinstance(need["ask"], dict) else need["ask"]) if isinstance(a, dict)) if isinstance(need.get("ask"), (dict, list)) and need["ask"] else "",
            "under %s" % ", ".join("%s %s" % (k, v) for k, v in sorted(need["skills_below"].items())) if isinstance(need.get("skills_below"), dict) and need["skills_below"] else "",
            "standing work" if standing(route) and not route.get("park") else "",
            route.get("status", "")]
    return ", ".join(g for g in gate if g) or "every pilot"


def figure(route):
    measured = route.get("measured") or {}
    return ("one-time" if route.get("once") else format(measured["cph_per_ship"], ",")) if measured else "TBD"


def anchor(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def group_file(key):
    """The sub-index of one group of routes."""
    return "index-%s.md" % SLUGS[key]


def plan_file(role):
    """The sub-plan of one role."""
    return "plan-%s.md" % role


def templates_file(name):
    """The page of one division's templates."""
    return "templates-%s.md" % name


def index_names(root):
    """The files `index` writes into game/routes/, in their order: master-index.md, one index per group of routes (every
    group, also an empty one: the set does not change with the routes), one plan per role and one page per division
    that has a templates file."""
    roles, _owners, _errors = division.load_plan(root)
    return ([MASTER] + [group_file(key) for key, _title, _text in STAGES] + [plan_file(role) for role in sorted(roles)]
            + [templates_file(name) for name in template_divisions(root)])


def stale(root):
    """Files of game/routes/ this script wrote once and writes no longer (index.md and plan.md until 2026-11-16, the plan
    of a role that is gone, the templates page of a division whose templates file is gone): `index` removes them,
    `check` fails on them. A file by another hand is never named."""
    made, out = set(index_names(root)), []
    for path in sorted((Path(root) / "routes").glob("*.md")):
        if path.name in made or not (path.name in ("index.md", "plan.md") or path.name.startswith(("index-", "plan-", "templates-"))):
            continue
        try:
            if WRITTEN in path.read_text(encoding="ascii", errors="replace"):
                out.append(path.name)
        except OSError:
            pass
    return out


def stamps(root, names, keep_id):
    """{file name: id}: the id a file carries; a file without one gets a new id, a second apart each and never on a full
    minute, or None under keep_id."""
    out, moment = {}, time.time() - len(names) - 1
    for name in names:
        old = current_index(root, name)
        stamp = old.split("\nid: ", 1)[1].split("\n", 1)[0] if "\nid: " in old else ""
        if not stamp and not keep_id:
            moment += 1
            while time.gmtime(moment).tm_sec == 0:
                moment += 1
            stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(moment))
        out[name] = stamp or None
    return out


def index_files(root, keep_id=False):
    """{file name: text} of master-index.md, every index-<group>.md, every plan-<role>.md and every
    templates-<division>.md, in that order. Under keep_id a file that has no id yet reads `missing`."""
    routes, _errors = routes_of(root)
    systems, home = atlas(root)
    roles, owners, _plan_errors = division.load_plan(root)
    names = index_names(root)
    ids = stamps(root, names, keep_id)
    facts = {}
    for rid, route in routes.items():
        where, far = zone(route, systems, home)
        facts[rid] = {"stage": stage(route), "zone": where, "far": far}
    titles = {key: title for key, title, _text in STAGES}
    place = lambda rid: facts[rid]["zone"] + (", %d jumps" % facts[rid]["far"] if facts[rid]["far"] and facts[rid]["zone"] == "beyond the border" else "")
    order = lambda rid: (facts[rid]["zone"] != "home space", routes[rid].get("kind", ""), rid)
    groups = [(key, title, text, sorted((r for r in routes if facts[r]["stage"] == key), key=order)) for key, title, text in STAGES]
    texts = {}

    for key, title, text, rids in groups:                         # one index per group of routes
        lines = ["# %s -- %s" % (group_file(key), title), "",
                 "Written by " + WRITTEN + ". " + text,
                 "A route is a task one pilot carries out by itself; its file is `game/routes/<id>.json`",
                 "(`BLUEPRINT.md`). The figures are what our own runs measured. Home space first, then by",
                 "kind and name. Up: [master-index.md](master-index.md).", "", "Routes: %d." % len(rids)]
        if rids:
            lines += ["", "| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |",
                      "|---|---|---|---|---|---|---|---|---|---|"]
        for rid in rids:
            route, m = routes[rid], routes[rid].get("measured") or {}
            lines.append("| [%s](%s.json) | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                rid, rid, cell(route.get("kind", "")), place(rid), cell(route.get("title", "")), cell(open_to(route)), m.get("runs", "TBD"), m.get("minutes", "TBD"),
                format(m["credits_per_run"], ",") if m else "TBD", figure(route), m.get("date", "--")))
        texts[group_file(key)] = lines

    planned, counts, flown = {}, {}, {}
    kits = {name: templates_of(root, name)[:2] for name in template_divisions(root)}      # {division: (its templates, its owner)}
    for role in roles:
        try:
            spec = read_json(Path(root) / "routes" / "plans" / (role + ".json"))
        except (OSError, ValueError):
            spec = {}
        spec = spec if isinstance(spec, dict) else {}
        planned[role] = [i for i in spec.get("planned") or [] if isinstance(i, dict) and i.get("what")]
        counts[role] = (spec.get("ships") if isinstance(spec.get("ships"), dict) else {}, spec.get("of") if isinstance(spec.get("of"), int) else 0)
        flown[role] = {str(k): n for k, n in spec["templates"].items() if isinstance(n, int)} if isinstance(spec.get("templates"), dict) else {}
    on = lambda role, rid: "--" if rid not in counts[role][0] else ("all %d" if counts[role][0][rid] == counts[role][1] else "%d of " + str(counts[role][1])) % counts[role][0][rid]
    for role in sorted(roles):                                    # one plan per role
        lines = ["# %s -- The Plan of the Role %s" % (plan_file(role), role), "",
                 "Written by " + WRITTEN + ", from `plans/%s.json`:" % role,
                 "the routes the %s ships fly, in one order, and how many of them have each route in" % role,
                 "their plan. The division's Admiral keeps one plan file with every ship and its own",
                 "routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder",
                 "and not here, and `plans/%s.json` is written from it. `Planned` is what the Admiral" % role,
                 "means to do next. What a route earns now is not written here, because it changes by the",
                 "hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each",
                 "figure with its age. Up: [master-index.md](master-index.md).", "",
                 "Kept by %s. Routes: %d. Ships: %s." % (owners.get(role) or "--", len(roles[role]), counts[role][1] or "--"), "",
                 "| # | Route | Group | Zone | Open to | Ships planned |", "|---|---|---|---|---|---|"]
        for n, rid in enumerate(roles[role], 1):
            if rid in routes:
                lines.append("| %d | [%s](%s.json) | [%s](%s) | %s | %s | %s |" % (
                    n, rid, rid, titles[facts[rid]["stage"]], group_file(facts[rid]["stage"]), place(rid), cell(open_to(routes[rid])), on(role, rid)))
            else:
                lines.append("| %d | %s | no route file | -- | -- | -- |" % (n, cell(rid)))
        if flown[role]:                                           # the templates its ships name as `@<name>` (plan.py role_files)
            its = plan_module().division_of(role)
            page = templates_file(its) if its in kits else None
            lines += ["", "Templates its ships fly (a ship's own routes name one as `@<name>`):", "", "| Template | Ships of this role on it |", "|---|---|"]
            lines += ["| %s | %d |" % ("[%s](%s)" % (key, page) if page else cell(key), n) for key, n in flown[role].items()]
        if planned[role]:
            lines += ["", "Planned:", "", "| What | When |", "|---|---|"] + ["| %s | %s |" % (cell(i.get("what", "")), cell(i.get("when", "--"))) for i in planned[role]]
        texts[plan_file(role)] = lines

    for name, (kit, keeper) in kits.items():                      # one page per division that has a templates file
        mine = [role for role in plan_module().roles_of(name) if role in flown]
        ships = {key: sum(flown[role].get(key, 0) for role in mine) for key in kit}
        link = lambda rid: "[%s](%s.json)" % (rid, rid) if rid in routes else "%s (no route file)" % cell(rid)
        lines = ["# %s -- The Templates of the %s Division" % (templates_file(name), name.capitalize()), "",
                 "Written by " + WRITTEN + ", from `templates/%s.json`:" % name,
                 "the named lists of routes of the %s division. A ship's row in the division's plan" % name,
                 "file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship",
                 "tries its routes in this order; a change of a template moves every ship that names it",
                 "within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.",
                 "Up: [master-index.md](master-index.md).", "",
                 "Kept by %s. Templates: %d. Ships on them: %d." % (keeper or "--", len(kit), sum(ships.values()))]
        if kit:
            lines += ["", "| Template | Title | Trains | Routes, in this order | Ships on it | Note |", "|---|---|---|---|---|---|"]
            lines += ["| %s | %s | %s | %s | %d | %s |" % (cell(key), cell(entry["title"]) or "--", cell(", ".join(entry["trains"])) or "--",
                                                          " > ".join(link(rid) for rid in entry["routes"]) or "--", ships[key], cell(entry["note"]) or "--")
                      for key, entry in kit.items()]
        texts[templates_file(name)] = lines

    def best(key, rids):
        seen = [(routes[r]["measured"], r) for r in rids if routes[r].get("measured")]
        if not seen:
            return "not measured yet" if rids else "--"
        field, unit = ("credits_per_run", "cr a run") if key == "once" else ("cph_per_ship", "cr per ship-hour")
        m, rid = max(seen, key=lambda pair: pair[0].get(field) or 0)
        return "%s: %s %s" % (rid, format(m.get(field) or 0, ","), unit)

    master = ["# master-index.md -- Routes and Plans", "",
              "Written by " + WRITTEN + ". Start here: every",
              "name below is a link into a sub-index of this folder. Each group of routes has its own",
              "index (`index-<group>.md`) and each role its own plan (`plan-<role>.md`), so that no",
              "file grows with the whole fleet. How a route is written, and what is automatic:",
              "[BLUEPRINT.md](BLUEPRINT.md).",
              "", "## Routes by Group", "",
              "| Group | What it holds | Routes | Home space | Beyond the border | Best measured |", "|---|---|---|---|---|---|"]
    for key, title, text, rids in groups:
        master.append("| [%s](%s) | %s | %d | %d | %d | %s |" % (
            title, group_file(key), cell(text), len(rids), sum(1 for r in rids if facts[r]["zone"] == "home space"),
            sum(1 for r in rids if facts[r]["zone"] == "beyond the border"), cell(best(key, rids))))
    master.append("| All | | %d | %d | %d | |" % (len(routes), sum(1 for f in facts.values() if f["zone"] == "home space"), sum(1 for f in facts.values() if f["zone"] == "beyond the border")))
    kinds = sorted({str(r.get("kind", "")) for r in routes.values()})
    master += ["", "## Routes by Zone and Kind", "", "| Zone | Routes | %s | Farthest system, jumps from home |" % " | ".join(kinds), "|---|---|%s---|" % ("---|" * len(kinds))]
    for where in ("home space", "beyond the border", "--"):
        rids = [r for r in routes if facts[r]["zone"] == where]
        if rids:
            far = [facts[r]["far"] for r in rids if facts[r]["far"] is not None]
            master.append("| %s | %d | %s | %s |" % ("not on the chart" if where == "--" else where, len(rids),
                                                   " | ".join(str(sum(1 for r in rids if str(routes[r].get("kind", "")) == k)) for k in kinds), max(far) if far else "--"))
    if roles:
        master += ["", "## Plans by Role", "", "| Role | Kept by | Routes | The first three, in order | Planned | Ships |", "|---|---|---|---|---|---|"]
        for role in sorted(roles):
            master.append("| [%s](%s) | %s | %d | %s | %d | %s |" % (cell(role), plan_file(role), cell(owners.get(role) or "--"), len(roles[role]),
                                                                 cell(" > ".join(roles[role][:3])), len(planned[role]), counts[role][1] or "--"))
    if kits:
        master += ["", "## Templates by Division", "", "Named lists of routes a ship's own routes in its division's plan file name as `@<template>`.", "",
                   "| Division | Kept by | Templates | Page |", "|---|---|---|---|"]
        for name, (kit, keeper) in kits.items():
            master.append("| %s | %s | %s | [%s](%s) |" % (name, cell(keeper or "--"), cell(", ".join(kit)) or "none", templates_file(name), templates_file(name)))
    shelf = Path(root) / "routes" / "guidebook"
    books = sorted(shelf.glob("*.md")) + sorted(shelf.glob("*/card.md")) if shelf.is_dir() else []     # a guidebook in chapters: its card
    if books:
        master += ["", "## The Guidebooks", "", "What each division learned about its routes, its levelling and its ships; kept by its Admiral, read by every member.", "",
                   "| Guidebook | Title |", "|---|---|"]
        for path in books:
            title = next((l[2:].strip() for l in path.read_text(encoding="ascii", errors="replace").splitlines() if l.startswith("# ")), path.stem)
            if path.name == "card.md" and path.parent != shelf:      # its chapters, the card first (scripts/guide.py; hive.py guide <division>)
                title = "%s, chapters: %s" % (path.parent.name.capitalize(), ", ".join("[%s](guidebook/%s/%s)" % (p.stem, path.parent.name, p.name) for p in
                                                                         sorted(path.parent.glob("*.md"), key=lambda p: (p.stem != "card", p.stem))))
            rel = path.relative_to(shelf).as_posix()
            master.append("| [guidebook/%s](guidebook/%s) | %s |" % (rel, rel, cell(title)))
    texts[MASTER] = master
    return {name: (FRONT % ("routes-" + name[:-3], ids[name]) + "\n".join(texts[name]) + "\n") if ids[name] else "missing" for name in names}


def write_index(root):
    """Write the index files that changed and remove the ones written no longer; [(file name, `written`, `current` or
    `removed`)]."""
    done = []
    for name, text in index_files(root).items():
        if text == current_index(root, name):
            done.append((name, "current"))
        else:
            (Path(root) / "routes" / name).write_text(text, encoding="ascii")
            done.append((name, "written"))
    for name in stale(root):
        (Path(root) / "routes" / name).unlink()
        done.append((name, "removed"))
    return done


GIFTS = {"path": None, "stamp": None, "rows": []}      # the wallet guard's top-ups, read again only when the file changed
DEPOSITS = {"path": None, "stamp": None, "rows": []}   # the treasury deposits of onetime.json, read again only when it changed
RUNS = {"path": None, "stamp": None, "spans": {}}      # each pilot's runs (span, first and last wallet), read only for a gift before a span
EDGE = 120                    # seconds at a run's start and end in which a wallet reading may fall on either side of a gift
PRE = 30 * 60                 # a gift booked this long before a run's span may land in it: the game shows a gift minutes after its answer (ENT-220)
TREASURY = "Faction treasury: credits deposited"     # the title a deposit into the faction's treasury is booked under (onetime.json)
TREASURY_FUND = "Treasury fund: credits withdrawn"   # a withdrawal from the faction treasury into the leader's wallet (wallet.py fund)
SWEEPS = {"path": None, "stamp": None, "rows": []}     # the sweep's booked gifts with the giver's wallet after each, read again only when the file changed
SWEEP_MATCH = 60              # seconds between a gift's booking (gifts.jsonl) and the sweep's row of it (sweep.jsonl): one gift
PLAYER = re.compile(r'"player":\{[^{}]*?"username":"([^"]*)"[^{}]*?"credits":(-?\d+)')     # the giver's wallet in the gift's answer


def gifts(data=None):
    """[(epoch, giver, taker, credits, loose)] of the wallet guard's top-ups (wallet.py: data/fleet/gifts.jsonl); loose:
    the row's time is not the gift's own to the second. The file lies beside the tax record, so what points that
    record elsewhere (FLEET_TAXES, a test) points this one there too."""
    path = Path(taxes.record_file(data)).with_name("gifts.jsonl")
    try:
        found = path.stat()
    except OSError:
        return []
    stamp = (found.st_mtime_ns, found.st_size)
    if GIFTS["path"] != str(path) or GIFTS["stamp"] != stamp:
        rows = []
        try:
            with open(path, encoding="utf-8") as handle:
                for line in handle:
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(row, dict) and all(isinstance(row.get(key), (int, float)) and not isinstance(row.get(key), bool) for key in ("at", "credits")):
                        rows.append((row["at"], str(row.get("from") or ""), str(row.get("to") or ""), row["credits"], bool(row.get("loose"))))
        except OSError:
            return []
        GIFTS.update(path=str(path), stamp=stamp, rows=rows)
    return GIFTS["rows"]


def sweep_walls(data=None):
    """[(epoch, giver, taker, credits, the giver's wallet after the gift)] of the gifts the wallet sweep booked
    (wallet.py sweep: data/fleet/sweep.jsonl, kind gift, state booked): the gift's answer names the giver's credits
    after it, the sweep's keep (50,000). A row whose answer names no wallet of the giver is left out."""
    path = Path(taxes.record_file(data)).with_name("sweep.jsonl")
    try:
        found = path.stat()
    except OSError:
        return []
    stamp = (found.st_mtime_ns, found.st_size)
    if SWEEPS["path"] != str(path) or SWEEPS["stamp"] != stamp:
        rows = []
        try:
            with open(path, encoding="utf-8") as handle:
                for line in handle:
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    if not (isinstance(row, dict) and row.get("kind") == "gift" and row.get("state") == "booked" and isinstance(row.get("at"), (int, float))
                            and isinstance(row.get("credits"), int) and not isinstance(row.get("credits"), bool)):
                        continue
                    said = PLAYER.search(str(row.get("text") or ""))
                    if said and said.group(1) == str(row.get("from") or ""):
                        rows.append((row["at"], said.group(1), str(row.get("to") or ""), row["credits"], int(said.group(2))))
        except OSError:
            return []
        SWEEPS.update(path=str(path), stamp=stamp, rows=rows)
    return SWEEPS["rows"]


def wall_after(walls, at, giver, taker, credits):
    """The giver's wallet after one gift as the sweep's row of it reads, or None for a gift the sweep did not book."""
    hits = [after for when, frm, to, units, after in walls if frm == giver and to == taker and units == credits and abs(when - at) <= SWEEP_MATCH]
    return hits[0] if len(set(hits)) == 1 else None


def deposits(data=None):
    """[(epoch, pilot, '', credits, False)] of the deposits our pilots made into the faction's treasury: the rows of
    onetime.json whose title begins with TREASURY (gate.book_onetime, wallet.py sweep), the giver's side of a move
    whose other side is the Collective's own purse (requests ENT-231). Read beside the gifts, as one more giver."""
    path = Path(taxes.record_file(data)).with_name("onetime.json")
    try:
        found = path.stat()
    except OSError:
        return []
    stamp = (found.st_mtime_ns, found.st_size)
    if DEPOSITS["path"] != str(path) or DEPOSITS["stamp"] != stamp:
        rows = []
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            loaded = []
        for one in loaded if isinstance(loaded, list) else []:
            if isinstance(one, list) and len(one) == 4 and isinstance(one[0], (int, float)) and isinstance(one[3], (int, float)):
                if str(one[2]).startswith(TREASURY) and one[3] < 0:
                    rows.append((one[0], str(one[1]), "", -one[3], False))
                elif str(one[2]).startswith(TREASURY_FUND) and one[3] > 0:
                    rows.append((one[0], "", str(one[1]), one[3], False))
        DEPOSITS.update(path=str(path), stamp=stamp, rows=rows)
    return DEPOSITS["rows"]


def run_spans(data=None):
    """{pilot: [(span first, span last, credits before, credits after)]} of every run in data/routes/runs.jsonl, read
    again only when the file changed. Asked only for a gift booked just before a run's span (late_gifts)."""
    folder = Path(taxes.record_file(data)).parent.parent if data is None else Path(data)
    path = folder / "routes" / "runs.jsonl"
    try:
        found = path.stat()
    except OSError:
        return {}
    stamp = (found.st_mtime_ns, found.st_size)
    if RUNS["path"] != str(path) or RUNS["stamp"] != stamp:
        spans = {}
        try:
            with open(path, encoding="utf-8") as handle:
                for line in handle:
                    try:
                        one = json.loads(line)
                    except ValueError:
                        continue
                    when = taxes.span(one) if isinstance(one, dict) else None
                    if when and one.get("pilot"):
                        spans.setdefault(str(one["pilot"]), []).append((when[0], when[1], one.get("credits_before"), one.get("credits_after")))
        except OSError:
            return {}
        RUNS.update(path=str(path), stamp=stamp, spans=spans)
    return RUNS["spans"]


def late_gifts(row, found, data=None):
    """Credits of gifts to the row's pilot booked in the PRE seconds before its span that landed while it flew
    (requests ENT-220: ten gifts for the outpost booked 3 to 9 minutes before a craft run read as 117,329 cr it
    earned). A gift that another run of the pilot spans is that run's. What the pilot's wallet gained between its
    previous run's last reading and this run's first is what landed before: the rest of the gifts, latest first,
    landed in the run, each taken out only while that brings the run's change nearer to nothing."""
    pilot = row.get("pilot")
    early = [(at, credits) for at, giver, taker, credits, _loose in _gifts_for(pilot, data) if taker == pilot and giver != pilot and found[0] - PRE <= at < found[0]]
    if not early:
        return 0
    spans = run_spans(data).get(pilot) or []
    early = [(at, credits) for at, credits in early if not any(s0 <= at <= s1 for s0, s1, _b, _a in spans if s0 != found[0])]
    if not early:
        return 0
    before = row.get("credits_before")
    prior = [s for s in spans if s[1] <= found[0] + taxes.LAG + EDGE and s[0] != found[0]]
    landed = 0
    if prior and isinstance(before, (int, float)) and isinstance(max(prior)[3], (int, float)) and max(prior)[3] > 0:
        landed = max(0, before - max(prior)[3])               # what reached the wallet between the two runs
    tax_paid = row.get("_tax_paid")
    plain = (row.get("delta") or 0) + (tax_paid if tax_paid is not None else taxes.in_run(row, data))
    total = 0
    for at, credits in sorted(early):                          # the earliest landed first
        if landed >= credits * 0.9:
            landed -= credits
            continue
        if abs(plain - total - credits) < abs(plain - total):
            total += credits
    return -total


_PILOT_EVENTS = {"g_id": None, "d_id": None, "g_len": -1, "d_len": -1, "by_pilot": {}, "gifts_by_taker": {}}


def _indexed_events(data=None):
    """Per-pilot sorted (gifts + deposits) and taker-only gifts, rebuilt only when gifts(data) or deposits(data) change."""
    g = gifts(data)
    d = deposits(data)
    if (_PILOT_EVENTS["g_id"] is not g or _PILOT_EVENTS["d_id"] is not d
            or _PILOT_EVENTS["g_len"] != len(g) or _PILOT_EVENTS["d_len"] != len(d)):
        by_p = {}
        by_t = {}
        for ev in g:
            giver, taker = ev[1], ev[2]
            if giver:
                by_p.setdefault(giver, []).append(ev)
            if taker and taker != giver:
                by_p.setdefault(taker, []).append(ev)
            if taker:
                by_t.setdefault(taker, []).append(ev)
        for ev in d:
            giver, taker = ev[1], ev[2]
            if giver:
                by_p.setdefault(giver, []).append(ev)
            if taker and taker != giver:
                by_p.setdefault(taker, []).append(ev)
        for lst in by_p.values():
            lst.sort()
        _PILOT_EVENTS.update(g_id=g, d_id=d, g_len=len(g), d_len=len(d), by_pilot=by_p, gifts_by_taker=by_t)
    return _PILOT_EVENTS["by_pilot"], _PILOT_EVENTS["gifts_by_taker"]


def _gifts_for(pilot, data=None):
    _, by_t = _indexed_events(data)
    return by_t.get(pilot, ())


def moved(row, data=None):
    """Credits another hand of ours took out of (+) or put into (-) the row's pilot while its run flew (taxes.span): the
    wallet guard's top-ups between our own ships, the sweep's gifts (a gift whose giver's wallet after it, sweep_walls,
    is the run's last wallet is that run's, wherever it fell in the span), the deposits into the faction's treasury
    (deposits) and a gift that landed in the run although booked just before it (late_gifts). Nobody earned or lost
    them, so no route is credited or charged with them: 2026-11-16, the guard's gifts to a hundred new ships read as a
    loss of 298,508 cr an hour for the fleet; 2026-11-17, a deposit of 200,000 cr read as -120,673 cr a ship-hour of a
    mine route (ENT-231)."""
    pilot, found = row.get("pilot"), taxes.span(row)
    if not pilot or not found:
        return 0
    by_p, _ = _indexed_events(data)
    evs = by_p.get(pilot)
    tax_paid = taxes.paid(pilot, found[0], found[1], data)
    plain = (row.get("delta") or 0) + tax_paid
    total, seam = 0, []
    if evs:
        start, end = found[0] + taxes.LAG, found[1] - taxes.SLACK
        before, after = row.get("credits_before"), row.get("credits_after")
        walls = None
        for at, giver, taker, credits, loose in evs:
            if at < found[0]:
                continue
            if at > found[1]:
                break
            sign = (giver == pilot) - (taker == pilot)
            if not sign:
                continue
            if sign > 0:
                if walls is None:
                    walls = sweep_walls(data)
                wall = wall_after(walls, at, giver, taker, credits) if walls else None
            else:
                wall = None
            if wall is not None and (wall == after) != (wall == before):
                total += credits * sign if wall == after else 0
                continue
            if not loose and start + EDGE <= at <= end - EDGE:
                total += credits * sign
            else:
                seam.append(credits * sign)
        for moved_credits in seam:
            if abs(plain + total + moved_credits) < abs(plain + total):
                total += moved_credits
    return total + late_gifts(dict(row, delta=plain - tax_paid + total, _tax_paid=tax_paid), found, data)


def earned(row):
    """A run's credits without the sale of goods it carried in (a hunt that sells another place's goods did not earn
    them), without the weekly tax the game took from its pilot while it flew (taxes.py) and without what the wallet
    guard moved through its pilot's wallet (moved): the one rule for what a run earned, read by hive.py, the store, the
    dispatcher's loss stop and the measured figures."""
    delta = (row.get("delta") or 0) + taxes.in_run(row) + moved(row)
    if row.get("kind") != "hunt":
        return delta
    gained, carried = row.get("goods") or {}, 0.0
    for item, sale in (row.get("sold") or {}).items():
        units, credits = sale[0], sale[2]
        extra = units - gained.get(item, 0)
        if units > 0 and extra > 0:
            carried += credits * extra / units
    return delta - carried


def readable(row):
    """False for a run that read no wallet at its start or at its end: it says nothing about credits. A pilot's wallet is
    never 0 (it keeps a floor): a 0 at either end is the engine not answering."""
    before, after = row.get("credits_before"), row.get("credits_after")
    numbers = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (before, after))
    return numbers and before > 0 and after > 0 and "wallet not read" not in (row.get("notes") or [])


def ended(row):
    """When a run ended, in seconds since the epoch, or None: its `started` read as dispatch.losing reads it, by the
    dispatcher's own reader of a UTC time (dispatch.read_time), plus its minutes (as dispatch.resting counts a run's
    end). The one clock of a run's figure: `measure` keeps the runs that ended inside its window."""
    import dispatch                                # here, not at the top: dispatch.py imports this file
    start = dispatch.read_time(row.get("started")) if row.get("started") else None
    return None if start is None else start + (row.get("minutes") or 0) * 60


def measure(root, data, write, only=None, now=None):
    """Print what the runs measured per route; with `write`, store it in the route files, of the routes in `only` when
    given. A repeating route counts the readable runs that ended in the last MEASURE_HOURS, and one without such a run
    loses its figure (it is a test again); a mission that pays once counts all its runs."""
    now = time.time() if now is None else now
    rows = []
    try:
        with open(Path(data) / "routes" / "runs.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        pass
    routes, _errors = routes_of(root)
    since = now - MEASURE_HOURS * 3600
    changed = []

    def put(rid, figure):
        if figure is None:
            del routes[rid]["measured"]
        else:
            routes[rid]["measured"] = figure
        (Path(root) / "routes" / (rid + ".json")).write_text(json.dumps(routes[rid], indent=1) + "\n", encoding="ascii")
        changed.append(rid)

    held = {rid for rid, route in routes.items() if isinstance(route, dict) and route.get("measured") and not route.get("once")}    # a figure with no run left is forgotten too
    for rid in sorted({r.get("route") for r in rows if r.get("route")} | held):
        route = routes.get(rid) if isinstance(routes.get(rid), dict) else {}
        once = bool(route.get("once"))
        every = [r for r in rows if r.get("route") == rid and r.get("minutes")]
        if not once:                                              # the window: what a route earns changes by the hour
            every = [r for r in every if (ended(r) or 0) >= since]
        mine = [r for r in every if readable(r)]
        may = write and (only is None or rid in only) and rid in routes
        if not mine:
            if every:
                print("%-28s runs %-4d none read a wallet: no figure" % (rid, len(every)))
            if once and every and may and route.get("measured"):
                put(rid, None)
            elif not once and route.get("measured"):
                if may:
                    put(rid, None)
                    print("%s: no readable run in %d hours: the figure is taken out; a test again" % (rid, MEASURE_HOURS))
                elif not write:
                    print("%s: no readable run in %d hours: `--write` takes the figure out; a test again" % (rid, MEASURE_HOURS))
            continue
        minutes = sum(r["minutes"] for r in mine)
        figure = {"date": time.strftime("%Y-%m-%d", time.gmtime(now)), "runs": len(mine), "minutes": round(statistics.median(r["minutes"] for r in mine)),
                  "credits_per_run": int(round(sum(earned(r) for r in mine) / len(mine), -1)),
                  "cph_per_ship": int(round(60 * sum(earned(r) for r in mine) / minutes, -1)) if minutes else 0}
        if not once:
            figure.update(hours=MEASURE_HOURS, last_run=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(max(ended(r) for r in mine))))
        print("%-28s runs %-4d minutes %-4d credits per run %-8s per ship-hour %-8s %s" % (
            rid, figure["runs"], figure["minutes"], format(figure["credits_per_run"], ","), format(figure["cph_per_ship"], ","),
            ("" if rid in routes else "(no route file)") + (" (%d more runs read no wallet)" % (len(every) - len(mine)) if len(every) > len(mine) else "")
            + ("" if once else " (the last %d hours, the newest run ended %s)" % (MEASURE_HOURS, figure["last_run"]))))
        old = route.get("measured") or {}
        moved = not old or abs(figure["cph_per_ship"] - old.get("cph_per_ship", 0)) >= 0.2 * max(abs(old.get("cph_per_ship", 0)), 100) \
            or figure["runs"] >= 2 * max(old.get("runs", 0), 1) or (not once and "hours" not in old)      # a block from before the window: once more
        if may and moved:
            put(rid, figure)
    if write:
        print("measured block written: %s" % (", ".join(changed) or "none"))
    return 0


def why_off(note):
    """What a route's note says of why it is off: its last sentence that names `off` (else its last sentence), and when
    that says little more than `off` (`2026-11-16 09:15 UTC (Apophis): status off.`) the sentence after it, or before
    it when it ends the note."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(`])", str(note or "").strip()) if s.strip()]
    if not sentences:
        return "(no note)"
    said = [n for n, s in enumerate(sentences) if re.search(r"\boff\b", s, re.IGNORECASE)]
    at = said[-1] if said else len(sentences) - 1
    core = re.sub(r"^\d{4}-\d\d-\d\d \d\d:\d\d UTC[^:]*:\s*", "", sentences[at])
    if len(core) >= 40 or len(sentences) == 1:
        return sentences[at]
    return " ".join([sentences[at], sentences[at + 1]] if at + 1 < len(sentences) else [sentences[at - 1], sentences[at]])


def named_routes(root, data):
    """{route id} a plan or a template names: each division's plan file (data/plans/plan-*.md: First, the ships' own
    routes, Then, by plan.py's own reader), each role's plan (game/routes/plans/*.json) and each templates file
    (game/routes/templates/*.json, whatever its division)."""
    roles, _owners, _errors = division.load_plan(root)
    named = {rid for ids in roles.values() for rid in ids}
    parse = plan_module().parse
    for path in sorted((Path(data) / "plans").glob("plan-*.md")):
        try:
            plan = parse(path.read_bytes().decode("ascii", "replace"))
        except OSError:
            continue
        named |= {rid for ids in [plan["first"], plan["then"]] + list(plan["ships"].values()) for rid in ids if not rid.startswith("@")}
    folder = Path(root) / "routes" / "templates"
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        try:
            spec = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError, UnicodeDecodeError):
            continue
        kit = spec.get("templates") if isinstance(spec, dict) else None
        for entry in kit.values() if isinstance(kit, dict) else []:
            named |= {str(rid) for rid in (entry.get("routes") if isinstance(entry, dict) else None) or [] if isinstance(rid, str)}
    return named


def idle(root, data):
    """The lines of `idle`: the route files that are off and why, then those no plan and no template names, with their
    kind and the end of their last run. Reads only."""
    routes, errors = routes_of(root)
    routes = {rid: route for rid, route in routes.items() if isinstance(route, dict)}
    off = sorted(rid for rid, route in routes.items() if route.get("status") == "off")
    lines = ["OFF: %d route files with status off, and the sentence of each note that says why:" % len(off)]
    lines += ["  %s (%s): %s" % (rid, routes[rid].get("kind", "?"), why_off(routes[rid].get("note"))) for rid in off]
    last = {}
    try:
        with open(Path(data) / "routes" / "runs.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                when = ended(row) if isinstance(row, dict) and row.get("route") else None
                if when is not None:
                    last[str(row["route"])] = max(when, last.get(str(row["route"]), when))
    except OSError:
        pass
    span = "runs.jsonl holds runs that ended from %s to %s" % tuple(time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(t)) for t in (min(last.values()), max(last.values()))) if last else "runs.jsonl holds no run"
    named = named_routes(root, data)
    loose = sorted(rid for rid in routes if rid not in named)
    lines += ["", "UNPLANNED: %d route files named in no plan (data/plans/plan-*.md, game/routes/plans/*.json) and no template "
                  "(game/routes/templates/*.json); %s:" % (len(loose), span)]
    lines += ["  %-48s %-8s %-4s %s" % (rid, routes[rid].get("kind", "?"), "off" if routes[rid].get("status") == "off" else "",
                                         "last run ended " + time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(last[rid])) if rid in last else "no run in runs.jsonl")
              for rid in loose]
    return lines + ["ERROR " + line for line in errors]


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Check the route files, write their index, attach what the runs measured.")
    parser.add_argument("command", choices=("check", "index", "measure", "idle"))
    parser.add_argument("--root", default=str(here.parent))
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("ids", nargs="*", help="measure --write: the routes whose measured block is written")
    parser.add_argument("--role", help="measure --write: the routes of this role's plan")
    parser.add_argument("--all", action="store_true", help="measure --write: every route (the hourly job)")
    args = parser.parse_args()
    if args.command == "check":
        errors, count = check(args.root)
        for line in errors:
            print("ERROR " + line)
        print("Checked %d route files." % count)
        warned = sale_warnings(routes_of(args.root)[0])      # r22: a sale outside Trade's class; each named only while the switch is on
        workclass.follow(args.data)
        for rid, cls, closed in warned if workclass.strict_on() else []:
            print("WARNING game/routes/%s.json: %s route that sells: the dispatcher refuses it to every %s (%s)" % (rid, cls, ", ".join(closed), workclass.SALE))
        if warned and not workclass.strict_on():
            print("WARNING %d route files sell outside Trade's class: with data/fleet/strict-classes-on the dispatcher refuses them to every pilot "
                  "that is not a trader; the list: `python3 -B game/fleet/workclass.py sales`" % len(warned))
        gated = fit_gate_warnings(args.root, routes_of(args.root)[0])     # requests ENT-343 (2): a refit the plan's gates refuse
        for fid, role, rid, module in gated:
            print("WARNING game/routes/%s.json: replaces %s in the %s plan, while %s asks `requires.module` %s: a refitted ship is refused it "
                  "(a list of modules means any one of them)" % (fid, module, role, rid, module))
        limits = buy_limit_warnings(routes_of(args.root)[0])        # requests ENT-357: a gate on an ask the buy refuses
        for rid, n, item, gate, limit in limits:
            print("WARNING game/routes/%s.json: stop %d buys %s at a max_price of %s, under the `requires.ask` gate of %s x %.2f (the runner's tax): "
                  "the gate opens on an ask the buy refuses; set max_price to %d or more" % (rid, n, item, limit, gate, BUY_TAX, -(-gate * BUY_TAX // 1)))
        print("Errors: %d | Warnings: %d" % (len(errors), (len(warned) if workclass.strict_on() else min(len(warned), 1)) + len(gated) + len(limits)))
        return 1 if errors else 0
    if args.command == "idle":
        for line in idle(args.root, args.data):
            print(line)
        return 0
    if args.command == "index":
        done = write_index(args.root)
        for name, state in done:
            print("game/routes/%s: %s" % (name, state))
        changed = ["game/routes/" + name for name, state in done if state != "current"]
        if changed:
            print("commit them together: git add -- " + " ".join(changed))
        return 0
    only = set(args.ids)
    if args.role:
        roles, _owners, _errors = division.load_plan(args.root)
        if args.role not in roles:
            print("no plan for the role `%s`: %s" % (args.role, ", ".join(sorted(roles))))
            return 1
        only |= set(roles[args.role])
    if args.write and not only and not args.all:
        print("NOTHING WRITTEN: `measure --write` needs the routes it may change: route ids, --role <role> (the routes of that plan), or --all.")
        print("The figures below are a rehearsal. Every route is measured and committed by the hourly job; write by hand only what you need at once.")
        return measure(args.root, args.data, False)
    return measure(args.root, args.data, args.write, None if args.all or not args.write else only)


if __name__ == "__main__":
    sys.exit(main())
