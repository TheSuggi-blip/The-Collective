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
                  window: it is a test again.
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
    while it flew: the wallet guard's top-ups between our own ships (wallet.py), like the weekly tax.
  - A run that read no wallet (no credits before and after, both 0, or the note
    `wallet not read`) counts for nothing: a route whose runs are all such has
    no figure, and a figure built on them is taken out of its file.
WHY:  what a route pays is written next to the route, and a wrong file is caught
      before a pilot flies it.

USAGE:
  routes.py check | index | measure                [--root <dir>] [--data <dir>]
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
        if kind == "guard" and route.get("guards"):    # a guard keeps the place of a route of ours: one that exists and works at one place
            guarded = routes.get(str(route["guards"]))
            if not isinstance(guarded, dict):
                errors.append(where + "`guards` names `%s`, which is no route file" % route["guards"])
            elif guarded_place(route, guarded) is None:
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
        levels = lambda value: isinstance(value, dict) and all(isinstance(v, int) and not isinstance(v, bool) for v in value.values())
        need = route.get("requires") if isinstance(route.get("requires"), dict) else {}
        if "skills_below" in need and not levels(need["skills_below"]):
            errors.append(where + "`requires.skills_below` must be {skill: level}")
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
                or route.get("kind") == "guard")


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
    if any(isinstance(s, dict) and s.get("fit") for s in route.get("stops") or []):
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
            "needs %s" % need["module"] if need.get("module") else "", "without %s" % need["without_module"] if need.get("without_module") else "",
            "empty hold" if need.get("empty_hold") else "", "from %s cr" % format(route["min_credits"], ",") if route.get("min_credits") else "",
            "after the reward %s" % (need["booked"] if isinstance(need["booked"], str) else ", ".join(need["booked"])) if need.get("booked") else "",
            "from %s" % ", ".join("%s %s" % (k, v) for k, v in sorted(need["skills"].items())) if isinstance(need.get("skills"), dict) and need["skills"] else "",
            "with %s" % ", ".join("%s %s stored at %s" % (w.get("min", 1), w.get("item"), w.get("at")) for w in ([need["stored"]] if isinstance(need["stored"], dict) else need["stored"]) if isinstance(w, dict)) if need.get("stored") else "",
            "while %s" % ", ".join("%s bids %s cr for %s" % (b.get("base"), b.get("min_price", 1), b.get("item")) for b in ([need["bid"]] if isinstance(need["bid"], dict) else need["bid"]) if isinstance(b, dict)) if need.get("bid") else "",
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
    books = sorted((Path(root) / "routes" / "guidebook").glob("*.md")) if (Path(root) / "routes" / "guidebook").is_dir() else []
    if books:
        master += ["", "## The Guidebooks", "", "What each division learned about its routes, its levelling and its ships; kept by its Admiral, read by every member.", "",
                   "| Guidebook | Title |", "|---|---|"]
        for path in books:
            title = next((l[2:].strip() for l in path.read_text(encoding="ascii", errors="replace").splitlines() if l.startswith("# ")), path.stem)
            master.append("| [guidebook/%s](guidebook/%s) | %s |" % (path.name, path.name, cell(title)))
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


def gifts(data=None):
    """[(epoch, giver, taker, credits)] of the wallet guard's top-ups (wallet.py: data/fleet/gifts.jsonl). The file lies
    beside the tax record, so what points that record elsewhere (FLEET_TAXES, a test) points this one there too."""
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
                        rows.append((row["at"], str(row.get("from") or ""), str(row.get("to") or ""), row["credits"]))
        except OSError:
            return []
        GIFTS.update(path=str(path), stamp=stamp, rows=rows)
    return GIFTS["rows"]


def moved(row, data=None):
    """Credits another hand of ours took out of (+) or put into (-) the row's pilot while its run flew (taxes.span): the
    wallet guard's top-ups between our own ships. Nobody earned or lost them, so no route is credited or charged with
    them: 2026-11-16, the guard's gifts to a hundred new ships read as a loss of 298,508 cr an hour for the fleet."""
    pilot, found = row.get("pilot"), taxes.span(row)
    if not pilot or not found:
        return 0
    return sum(credits * ((giver == pilot) - (taker == pilot)) for at, giver, taker, credits in gifts(data) if found[0] <= at <= found[1])


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


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Check the route files, write their index, attach what the runs measured.")
    parser.add_argument("command", choices=("check", "index", "measure"))
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
        print("Errors: %d | Warnings: 0" % len(errors))
        return 1 if errors else 0
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
