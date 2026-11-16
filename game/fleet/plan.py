#!/usr/bin/env python3
"""plan.py -- each division's plan file: every ship with the routes it flies, in their order; the dispatcher sends the ships by it.

WHAT: a division's plan is one file its Admiral keeps: data/plans/plan-<division>.md in the unit's data folder (it
      names our ships, so it is not in the public repository). It holds three lists:
        First, for Every Ship   routes every ship tries first, in this order (the missions that pay once, the fittings)
        Ships                   one row per ship: its hull and its levels (written by this script) and, in the last
                                cell, its own routes in their order
        Then, for Every Ship    routes every ship tries after its own (shared paying routes, standing work, the
                                census), ending with the `park` route
        Planned                 what the Admiral means to do next (`- what | when`): shown to every member in
                                game/routes/plan-<role>.md, so it names no ship
      A ship's own routes may name a TEMPLATE as `@<name>`, in any mix with route ids (`@ice-loop, gather-x`): a
      named list of routes of the division, kept in the repository (game/routes/templates/<division>.json, no ship
      named), so a ship is switched to another kind of work with one word and a change of the template moves every
      ship that names it. `@<name>` stands for the template's routes in their order; a route that then stands twice
      is flown at its first place.
      A free ship takes the first route of First + its own + Then that is open to it (the dispatcher's one rule,
      dispatch.why_not) within the minute. `apply` checks the file and writes what the fleet's tools read:
        data/plans/assign.json            {pilot: its routes in order, every template expanded}: the dispatcher and
                                          fill.py fly by it
        game/routes/plans/<role>.json     the role's routes in one order with the ships planned on each, and the ships
                                          on each template (counts, no names); plan-<role>.md and master-index.md are
                                          written from it, one commit
RULES:
  - A member changes the file of its own division; the Fleet Admiral any. A shell that is no member changes nothing.
  - A file that fails the check changes nothing: the plan applied last stays in force, and the ships fly on.
  - The level columns and the form of the file are the script's: `apply` writes the file again in its one form. Free
    text of the Admiral stands under `## Notes` and is kept as it is.
  - A ship of the division without a row gets one by itself, with the own routes most ships of its role have.
  - Before a division has a file, its plan is read from the role's plan in force: First is its opening run of
    missions that pay once and fittings, Then is the rest. The first `apply` writes the file; no ship changes its work.
  - Every applied version is kept in data/plans/history/ (the newest 40 of a division).
  - One writer at a time (the lock data/plans/plans.lock, held from the reading to the commit).
  - A plan that passes its check is written and flown at once. The repository's copy of it (the role plans and
    plan-<role>.md: counts, no names) is one commit in a folder every member works in: while another member holds
    an uncommitted route file there, the copy waits and the next `apply` writes it (the five-minute job runs one).
    Only a change that brings a new route file or a template with it needs that commit, and is refused without it.
  - A template is changed by the member that keeps the division, or the Fleet Admiral, like the plan. Its change is
    one commit (the templates file, the role plans, the pages) and applies the division's plan again in the same
    call. An `@<name>` the division does not hold, a template without a route or with a route that has no file, and
    an `@` in First or Then fail the check; a template no ship uses is a note. A template a ship names is not removed.
WHY:  one plan per role sent every ship of a division down the same list: forty miners on one buyer. Suggi,
      2026-11-16: each Admiral has one file with all its ships and the routes of each, changes only that file each
      turn, and the ships are sent by it. Templates (Suggi, 2026-11-16): ships are switched between kinds of work by
      a preconfigured list, not route by route.

From another script:
  plan.apply(root, data, [division], who, changes={division: change(plan)}, extra={path: text}, message=..., commit=...)
  plan.put_first(plan, ids) / put_own(plan, ships, id) / put_then(plan, id, routes) / take_out(plan, id)
  plan.division_of(word)            the division of a division's name, a member's name or a role
  dispatch.own_lists(data)          {pilot: its routes in order}, as applied

USAGE:
  plan.py [show] [<division>|<Member>|all] [--brief]    the file, what the check says and whether it is applied
  plan.py check [<division>|<Member>|all]               PASS or HALT per division (exit 1 on a HALT)
  plan.py apply [<division>|<Member>|all] [--quiet]     after a change by hand: check, write, commit
  plan.py set <ships> <routes> [--division <name>]      the own routes of ships: names with commas, a range
                                                        (miner-1..10), a role or `all`; routes with commas in their
                                                        order (`@<name>` for a template, in any mix), or `none`
  plan.py first <routes> [--division <name>]            the list First, whole
  plan.py then <routes> [--division <name>]             the list Then, whole
  plan.py templates [<division>|<Member>|all]           each template: name, title, trains, its routes in order, and
                                                        how many ships of the division use it
  plan.py template <name> <routes|none> [--title "..."] [--trains a,b] [--note "..."] [--division <name>]
                                                        make or replace a template (routes with commas, in their
                                                        order; an option not given keeps its value); `none` removes
                                                        it, refused while a ship names it
  plan.py use <ships> <name[,name...]> [--division <name>]
                                                        `set` with `@` before each name: the ships fly the templates
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)
  --data <dir>   the unit's data folder (default: the fleet's)

Stdlib only. ASCII only.
"""

import fcntl
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dispatch                                   # noqa: E402  routes, flagships, a ship's file
import division                                   # noqa: E402  who asks, which roles are whose
import routes as routefiles                       # noqa: E402  what a route is

DIVISIONS = {"command": "Unity", "mining": "Zero", "trade": "Mercury", "logistics": "Apollo", "military": "Apophis", "intel": "Oracle"}
SKILLS = ("piloting", "mining", "navigation", "trading", "gunnery", "exploration")
HEAD = ("Ship", "Hull") + tuple(skill.capitalize() for skill in SKILLS) + ("Own routes, in this order",)
SECTIONS = (("first", "First, for Every Ship"), ("ships", "Ships"), ("then", "Then, for Every Ship"), ("planned", "Planned"), ("notes", "Notes"))
NONE = ("", "-", "--", "none")
KEEP = 40                      # applied versions of one division kept in history/
TEMPLATES = "routes/templates/"  # a division's templates file, under the game folder: <division>.json


def roles_of(name):
    return sorted(role for role, owner in division.ROLES.items() if owner == DIVISIONS[name])


def division_of(word):
    """The division a word names: a division, a member or a role; None for anything else."""
    word = str(word or "").strip()
    if word.lower() in DIVISIONS:
        return word.lower()
    owner = word.capitalize() if word.capitalize() in division.MEMBERS else division.ROLES.get(word.lower())
    return next((name for name, who in DIVISIONS.items() if who == owner), None)


def folder(data):
    return Path(data) / "plans"


def path_of(data, name):
    return folder(data) / ("plan-%s.md" % name)


def crew_of(data, name):
    """[(ship, role, its row of fleet.json)] of a division, by role, number and name."""
    named = dispatch.flagships(data)
    fleet = dispatch.read_json(Path(data) / "fleet" / "fleet.json", {})
    roles = roles_of(name)
    found = [(str(ship.get("name")), dispatch.role_of(str(ship.get("name")), named), ship)
             for ship in (fleet.get("ships") or [] if isinstance(fleet, dict) else []) if isinstance(ship, dict) and ship.get("name")]
    return sorted((row for row in found if row[1] in roles), key=lambda r: (roles.index(r[1]), r[2].get("number") or 0, r[0]))


def unique(ids):
    seen = set()
    return [rid for rid in ids if not (rid in seen or seen.add(rid))]


def tokens(text):
    """The route ids of a cell or a list line: `>` or a comma between them; `--` and `none` are no route. A template
    stays as written (`@<name>`): `expand` reads it."""
    out = []
    for word in re.split(r"[>,]", str(text)):
        word = word.strip().strip("`").strip()
        if word.lower() not in NONE:
            out.append(word)
    return unique(out)


def parse(text):
    """{first, ships {ship: own routes}, then, planned [{what, when}], notes, errors} of a plan file's text."""
    plan = {"first": [], "ships": {}, "then": [], "planned": [], "notes": "", "errors": []}
    part, lines = None, text.split("\n")
    for n, line in enumerate(lines, 1):
        if line.startswith("## "):
            title = line[3:].strip().lower()
            part = next((key for key, name in SECTIONS if title.startswith(name.split(",")[0].lower())), "?")
            if part == "?":
                plan["errors"].append("line %d: `%s` is no section of a plan file (First, Ships, Then, Planned, Notes): free text goes under `## Notes`" % (n, line.strip()))
            if part == "notes":
                plan["notes"] = "\n".join(lines[n:]).strip("\n")
                break
        elif part in ("first", "then"):
            item = re.match(r"^\s*(?:\d+[.)]|[-*])\s+(.*)$", line)
            if item:
                plan[part] = unique(plan[part] + tokens(item.group(1)))
        elif part == "planned":
            item = re.match(r"^\s*[-*]\s+(.*\S)\s*$", line)
            if item:
                what, _bar, when = item.group(1).rpartition(" | ")
                plan["planned"].append({"what": what.strip(), "when": when.strip()} if what.strip() else {"what": when.strip(), "when": "--"})
        elif part == "ships" and line.lstrip().startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            ship = cells[0].strip("`").strip() if cells else ""
            if not ship or ship == HEAD[0] or set(ship) <= set("-: "):
                continue
            if ship in plan["ships"]:
                plan["errors"].append("line %d: the ship %s stands in two rows" % (n, ship))
            plan["ships"][ship] = tokens(cells[-1]) if len(cells) > 1 else []
    return plan


def seed(root, name, routes, crew):
    """The plan a division flies before it has a file, from its roles' plans in force: First is the opening run of
    missions that pay once and fittings that every role shares, Then the closing run every role shares, and a ship's
    own routes what its role's plan holds between the two (nothing, for a division of one role)."""
    plans, _owners, _errors = division.load_plan(root)
    lists = {role: plans[role] for role in roles_of(name) if plans.get(role)}
    opening = lambda rid: rid in routes and (routes[rid].get("once") or routefiles.stage(routes[rid]) == "fit")
    first = []
    for column in zip(*lists.values()):
        if len(set(column)) != 1 or not opening(column[0]):
            break
        first.append(column[0])
    rest = {role: ids[len(first):] for role, ids in lists.items()}
    then = []
    for column in zip(*[reversed(ids) for ids in rest.values()]):
        if len(set(column)) != 1:
            break
        then.insert(0, column[0])
    own = {role: ids[:len(ids) - len(then)] for role, ids in rest.items()}
    planned = []
    for role in lists:
        try:
            items = json.loads((Path(root) / "routes" / "plans" / (role + ".json")).read_text(encoding="ascii")).get("planned") or []
        except (OSError, ValueError):
            items = []
        planned += [{"what": str(i.get("what")), "when": str(i.get("when") or "--")} for i in items if isinstance(i, dict) and i.get("what") and i not in planned]
    return {"first": first, "ships": {ship: list(own.get(role) or []) for ship, role, _row in crew}, "then": then, "planned": planned, "notes": "", "errors": []}


def load(root, data, name, routes=None, crew=None, kit=None):
    """(the plan, True when its file exists). The plan carries the division's templates under `templates`: from its
    file in the repository (routes.templates_of), or `kit` (templates, owner, errors) for a change not written yet."""
    templates, _owner, faults = routefiles.templates_of(root, name) if kit is None else kit
    path = path_of(data, name)
    if path.is_file():
        plan, exists = parse(path.read_bytes().decode("ascii", "replace").replace("\ufffd", "?")), True
    else:
        routes = dispatch.load_routes(root) if routes is None else routes
        plan, exists = seed(root, name, routes, crew_of(data, name) if crew is None else crew), False
    plan["templates"] = templates
    plan["errors"] += list(faults)
    return plan, exists


def expand(plan, ship):
    """A ship's own routes as it flies them: each `@<name>` of its cell stands for that template's routes in their
    order, and a route that then stands twice is flown at its first place."""
    out, kit = [], plan.get("templates") or {}
    for word in plan["ships"].get(ship) or []:
        out += list((kit.get(word[1:]) or {}).get("routes") or []) if word.startswith("@") else [word]
    return unique(out)


def users(plan, key):
    """The ships whose cell names the template `key`, in the file's order."""
    return [ship for ship, ids in plan["ships"].items() if "@" + key in ids]


def effective(plan, ship):
    """The routes one ship tries, in order: First, its own (its templates expanded), Then."""
    return unique(plan["first"] + expand(plan, ship) + plan["then"])


def merge(lists):
    """One order that holds every list's routes: a route new to it is put behind the route it follows in its own list."""
    out = []
    for ids in lists:
        at = -1
        for rid in ids:
            if rid in out:
                at = out.index(rid)
            else:
                at += 1
                out.insert(at, rid)
    return out


def check(plan, routes, crew, name):
    """(errors, warnings) of a plan: an error means nothing is applied."""
    errors, warnings = list(plan["errors"]), []
    known = {ship for ship, _role, _row in crew}
    kit, home = plan.get("templates") or {}, "game/routes/templates/%s.json" % name
    errors += ["%s: %s" % (home, line) for line in routefiles.template_faults(kit, routes)]
    for where, ids in (("the list First", plan["first"]), ("the list Then", plan["then"])):
        errors += ["%s: `%s` is a template: the lists First and Then take route ids only; a template goes into a ship's own routes" % (where, rid)
                   for rid in ids if rid.startswith("@")]
    for ship, ids in plan["ships"].items():
        errors += ["the row of %s: `%s` is no template of the %s division (%s holds %s)" % (ship, word, name, home, ", ".join("@" + k for k in kit) or "none")
                   for word in ids if word.startswith("@") and word[1:] not in kit]
    parts = ([("the list First", plan["first"]), ("the list Then", plan["then"])] + [("the row of %s" % ship, ids) for ship, ids in plan["ships"].items()]
             + [("the template @%s" % key, entry["routes"]) for key, entry in kit.items()])
    for where, ids in parts:
        for rid in ids:
            if rid.startswith("@") or (where.startswith("the template") and rid not in routes):
                continue                                  # a template, or a template's fault named above
            if rid not in routes:
                errors.append("%s: no route file game/routes/%s.json" % (where, rid))
            elif routes[rid].get("status") == "off":
                warnings.append("%s: %s is switched off (status off): no ship is sent on it" % (where, rid))
    idle = [key for key in kit if not users(plan, key)]
    if idle:
        warnings.append("%d templates no ship uses: %s" % (len(idle), ", ".join("@" + key for key in idle)))
    for ship in plan["ships"]:
        if ship not in known:
            errors.append("the row of %s: no ship of the %s division has this name (%s)" % (ship, name, ", ".join(roles_of(name))))
    last = routes.get(plan["then"][-1]) if plan["then"] else None
    if not plan["then"]:
        errors.append("the list Then is empty: it ends with the `park` route, or a ship whose routes are all closed is left adrift")
    elif last is not None and routefiles.closes(last):
        errors.append("the list Then must end with a route that is always open (the `park` route): `%s` is not (%s)" % (plan["then"][-1], ", ".join(routefiles.closes(last))))
    missing = [ship for ship, _role, _row in crew if ship not in plan["ships"]]
    if missing:
        warnings.append("%d ships have no row yet (%s%s): apply gives each the own routes most ships of its role have"
                        % (len(missing), ", ".join(missing[:4]), " ..." if len(missing) > 4 else ""))
    lead = Counter(ids[0] for ids in (expand(plan, ship) for ship in plan["ships"]) if ids)
    for rid, ships in sorted(lead.items()):
        limit = (routes.get(rid) or {}).get("max_ships")
        if limit and ships > limit:
            warnings.append("%d ships have %s as their first own route and it takes %d: the others take their next route" % (ships, rid, limit))
    return errors, warnings


def complete(plan, crew):
    """Give every ship of the division a row: one without gets the own routes most ships of its role have."""
    for ship, role, _row in crew:
        if ship not in plan["ships"]:
            same = Counter(tuple(plan["ships"][other]) for other, its, _r in crew if its == role and other in plan["ships"])
            plan["ships"][ship] = list(same.most_common(1)[0][0]) if same else []
    return plan


def level(detail, skill):
    skills = detail.get("skills") if isinstance(detail, dict) else None
    if not isinstance(skills, dict) or not skills:
        return "--"
    entry = skills.get(skill, 0)
    value = entry.get("level") if isinstance(entry, dict) else entry
    return str(int(value)) if isinstance(value, (int, float)) and not isinstance(value, bool) else "--"


def cell(value):
    return str(value).replace("|", "/").replace("\n", " ").strip() or "--"


def render(data, name, plan, crew):
    """The file's text in its one form."""
    roles = roles_of(name)
    lines = ["# plan-%s.md -- The Plan of the %s Division" % (name, name.capitalize()), "",
             "Kept by %s; %s %s. A free ship takes the first route that is open to it of: the" % (DIVISIONS[name], "roles" if len(roles) > 1 else "role", " and ".join(roles)),
             "list First, its own routes, the list Then. The dispatcher sends it within the",
             "minute. To change the plan, change the two lists and the last cell of a ship's row",
             "(route ids in their order, `>` between them, `--` for none; in the cell also",
             "`@<name>` for a template of the division, `plan.py templates`), then run",
             "`python3 -I -B game/fleet/plan.py apply` (the tool plan, action=apply). The other",
             "columns and the form of this file are the script's; a file that fails the check",
             "changes nothing. Free text goes under `## Notes`.", "",
             "## First, for Every Ship", ""]
    lines += ["%d. %s" % (n, rid) for n, rid in enumerate(plan["first"], 1)] or ["None."]
    lines += ["", "## Ships", "", "| " + " | ".join(HEAD) + " |", "|" + "---|" * len(HEAD)]
    for ship, _role, row in crew:
        detail = dispatch.read_json(Path(data) / "fleet" / "ships" / dispatch.ship_file(ship), {})
        lines.append("| " + " | ".join([cell(ship), cell(row.get("class") or "--")] + [level(detail, skill) for skill in SKILLS]
                                       + [cell(" > ".join(plan["ships"].get(ship) or []))]) + " |")
    lines += ["", "## Then, for Every Ship", ""]
    lines += ["%d. %s" % (n, rid) for n, rid in enumerate(plan["then"], 1)] or ["None."]
    lines += ["", "## Planned", "", "What you mean to do next, one line each as `- what | when`. Every member reads it in",
              "`game/routes/plan-<role>.md`: it names no ship of ours.", ""]
    lines += ["- %s | %s" % (cell(item["what"]), cell(item["when"])) for item in plan["planned"]] or ["None."]
    lines += ["", "## Notes", "", plan["notes"].strip("\n") or "None."]
    return "\n".join(lines) + "\n"


def digest(plan, crew):
    """A mark of what the dispatcher flies by: the two lists and every ship's own routes."""
    body = [plan["first"], plan["then"], sorted((ship, plan["ships"].get(ship) or []) for ship, _role, _row in crew)]
    used = sorted({word[1:] for ship, _role, _row in crew for word in plan["ships"].get(ship) or [] if word.startswith("@")})
    if used:                                   # a template's routes are flown: its change is a change of the plan (a plan without one keeps its old mark)
        body.append([(key, ((plan.get("templates") or {}).get(key) or {}).get("routes")) for key in used])
    return hashlib.sha1(json.dumps(body).encode("ascii", "replace")).hexdigest()[:16]


def role_files(root, name, plan, crew):
    """{path under the game folder: text} of the role plans that change: the role's routes in one order, the ships
    planned on each, and the ships of the role on each template its ships name (counts, never names)."""
    out = {}
    for role in roles_of(name):
        mine = [ship for ship, its, _row in crew if its == role]
        lists = {ship: effective(plan, ship) for ship in mine}
        union = merge(lists.values()) if mine else unique(plan["first"] + plan["then"])
        path = Path(root) / "routes" / "plans" / (role + ".json")
        try:
            was = path.read_text(encoding="ascii")
            new = json.loads(was)
        except (OSError, ValueError):
            was, new = "", {"role": role, "owner": DIVISIONS[name]}
        named = {key: sum(1 for ship in mine if "@" + key in (plan["ships"].get(ship) or [])) for key in plan.get("templates") or {}}
        new.update(routes=union, ships={rid: sum(1 for ids in lists.values() if rid in ids) for rid in union}, of=len(mine), planned=list(plan["planned"]),
                   templates={key: n for key, n in named.items() if n}, derived="Written by game/fleet/plan.py from the division's plan file (data/plans/plan-%s.md), never by hand." % name)
        text = json.dumps(new, indent=1) + "\n"
        if text != was:
            out["routes/plans/%s.json" % role] = text
    return out


def applied(data, name):
    """The division's entry of assign.json ({digest, applied_at, by}), or {}."""
    found = dispatch.read_json(folder(data) / "assign.json", {})
    entry = (found.get("divisions") or {}).get(name) if isinstance(found, dict) and isinstance(found.get("divisions"), dict) else None
    return entry if isinstance(entry, dict) else {}


def prepare(root, data, name, routes, change=None, kit=None):
    """What applying a division's plan would write, after `change(plan)`, with the templates `kit` when given (a
    change of the division's templates, not written yet); reads only."""
    crew = crew_of(data, name)
    plan, exists = load(root, data, name, routes, crew, kit)
    if change is not None:
        change(plan)
    for key in ("first", "then"):
        plan[key] = unique(plan[key])
    plan["ships"] = {ship: unique(ids) for ship, ids in plan["ships"].items()}
    errors, warnings = check(plan, routes, crew, name)
    if not errors:
        complete(plan, crew)
    return {"name": name, "plan": plan, "crew": crew, "exists": exists, "errors": errors, "warnings": warnings,
            "text": "" if errors else render(data, name, plan, crew), "files": {} if errors else role_files(root, name, plan, crew),
            "digest": digest(plan, crew)}


def write(path, text):
    tmp = Path("%s.%d.tmp" % (path, os.getpid()))
    tmp.write_text(text, encoding="ascii")
    os.replace(tmp, path)


def write_private(data, ready, who, now):
    """The plan file, the lists the dispatcher flies by and the kept version; (the word for the line, changed or not)."""
    name, plan, crew = ready["name"], ready["plan"], ready["crew"]
    home = folder(data)
    (home / "history").mkdir(parents=True, exist_ok=True)
    path = path_of(data, name)
    was = path.read_text(encoding="ascii", errors="replace") if path.is_file() else None
    if was != ready["text"]:
        write(path, ready["text"])
    found = dispatch.read_json(home / "assign.json", {})
    found = found if isinstance(found, dict) else {}
    pilots = found.get("pilots") if isinstance(found.get("pilots"), dict) else {}
    lists = {ship: effective(plan, ship) for ship, _role, _row in crew}
    changed = applied(data, name).get("digest") != ready["digest"] or any(pilots.get(ship) != ids for ship, ids in lists.items())
    if changed:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        pilots.update(lists)
        divisions = found.get("divisions") if isinstance(found.get("divisions"), dict) else {}
        divisions[name] = {"digest": ready["digest"], "applied_at": stamp, "by": who}
        write(home / "assign.json", json.dumps({"written_at": stamp, "pilots": pilots, "divisions": divisions}, separators=(",", ":")) + "\n")
        write(home / "history" / ("plan-%s.%s.%s.md" % (name, time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(now)), ready["digest"][:6])), ready["text"])
        for old in sorted((home / "history").glob("plan-%s.*.md" % name))[:-KEEP]:
            old.unlink(missing_ok=True)
    return ("applied" if changed else "written again (levels or form)" if was != ready["text"] else "unchanged"), changed


def apply(root, data, names, who, changes=None, extra=None, message=None, commit=None, now=None):
    """Check and write the plans of the divisions named, each after its change. (True when none halted, the lines).
    `extra` ({path under the game folder: text}, a new route file or a division's templates file) goes into the same
    commit. A division whose plan fails the check changes nothing; with `extra` or a change one failure stops all."""
    now = time.time() if now is None else now
    routes, kits = dispatch.load_routes(root), {}
    for rel, text in (extra or {}).items():                  # a route file that is written with the plan counts as there
        if rel.startswith("routes/") and rel.count("/") == 1 and rel.endswith(".json"):
            try:
                routes[rel[7:-5]] = json.loads(text)
            except ValueError:
                pass
        elif rel.startswith(TEMPLATES) and rel.count("/") == 2 and rel.endswith(".json"):      # and so do templates written with it
            kits[rel[len(TEMPLATES):-5]] = routefiles.templates_of(root, rel[len(TEMPLATES):-5], text)
    folder(data).mkdir(parents=True, exist_ok=True)
    lines, good = [], True
    with open(folder(data) / "plans.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ready = [prepare(root, data, name, routes, (changes or {}).get(name), kits.get(name)) for name in names]
        for one in ready:
            for text in one["errors"][:12]:
                lines.append("HALT %s: %s" % (one["name"], text))
            if one["errors"]:
                good = False
                lines.append("HALT %s: nothing changed; the plan applied last stays in force (%s)" % (one["name"], path_of(data, one["name"])))
        if not good and (extra or changes):
            return False, lines
        files = dict(extra or {})
        for one in ready:
            files.update(one["files"])
        waits = ""
        if files:
            if commit is None:
                import fill                                # here, not at the top: fill.py reads this file
                commit = fill.commit
            patience = {} if extra else {"tries": 1}        # the copy alone is not worth a wait: the next apply writes it
            made = sorted({(Path(root) / rel).parent for rel in files if not (Path(root) / rel).parent.is_dir()}, key=str)  # the first templates file: commit writes into folders that exist
            for place in made:
                place.mkdir(parents=True)
            done, line = commit(root, data, who, files, message or "plans: %s (plan.py, %s)" % (", ".join(o["name"] for o in ready if o["files"]) or "routes", who), **patience)
            for place in reversed(made if not done else []):
                if place.is_dir() and not any(place.iterdir()):
                    place.rmdir()                          # nothing committed: no empty folder left behind
            if done:
                lines.append(line)
            elif extra:                                    # a new route file must be in the repository before a ship is sent on it
                lines.append(line)
                return False, lines
            else:                                          # only the repository's copy of the plan: the ships do not wait for it
                waits = " ".join(line.split("\n")[0].split(": ", 1)[-1].split())
        for one in ready:
            if one["errors"]:
                continue
            word, _changed = write_private(data, one, who, now)
            own = sum(1 for ship, _role, _row in one["crew"] if one["plan"]["ships"].get(ship))
            lines.append("%s: %s | %d ships, %d with routes of their own | First %d, Then %d | %s"
                         % (one["name"], word, len(one["crew"]), own, len(one["plan"]["first"]), len(one["plan"]["then"]), path_of(data, one["name"])))
            lines += ["  note %s: %s" % (one["name"], text) for text in one["warnings"][:8]]
        if waits:
            lines.append("  note: the ships fly by the plan as applied; its copy in the repository (game/routes/plans/, plan-<role>.md) waits, because %s. "
                         "The next apply writes it (the five-minute job runs one): nothing to do." % waits.rstrip("."))
    return good, lines


def put_first(plan, ids, head=False):
    """Routes into the list First: behind its last route, or at its head."""
    new = [rid for rid in ids if rid not in plan["first"]]
    plan["first"] = new + plan["first"] if head else plan["first"] + new


def put_own(plan, ships, rid, tail=False):
    """A route into the own routes of the ships named: in front (it is tried before the others), or behind."""
    for ship in ships:
        own = plan["ships"].setdefault(ship, [])
        if rid not in own:
            own.append(rid) if tail else own.insert(0, rid)


def put_then(plan, rid, routes):
    """A route into the list Then, in front of its first census or park route (the routes that only read and wait)."""
    if rid in plan["then"]:
        return
    waits = lambda r: (routes.get(r) or {}).get("park") or (routes.get(r) or {}).get("kind") == "census"
    at = next((n for n, r in enumerate(plan["then"]) if waits(r)), len(plan["then"]))
    plan["then"].insert(at, rid)


def take_out(plan, rid):
    """A route out of both lists and every ship's own routes."""
    plan["first"] = [r for r in plan["first"] if r != rid]
    plan["then"] = [r for r in plan["then"] if r != rid]
    plan["ships"] = {ship: [r for r in ids if r != rid] for ship, ids in plan["ships"].items()}


def ships_named(words, crew):
    """The ships a word names: names with commas, a range (miner-1..10), a role, or all. (ships, the words not known)."""
    known, by_role, out, unknown = [ship for ship, _role, _row in crew], {}, [], []
    for ship, role, _row in crew:
        by_role.setdefault(role, []).append(ship)
    for word in [w.strip() for w in str(words).split(",") if w.strip()]:
        span = re.match(r"^([a-z]+)-(\d+)\.\.(?:[a-z]+-)?(\d+)$", word)
        if word == "all":
            out += known
        elif word in by_role:
            out += by_role[word]
        elif span:
            found = ["%s-%d" % (span.group(1), n) for n in range(int(span.group(2)), int(span.group(3)) + 1)]
            out += [ship for ship in found if ship in known]
            unknown += [ship for ship in found if ship not in known]
        elif word in known:
            out.append(word)
        else:
            unknown.append(word)
    return unique(out), unknown


def state(root, data, name, routes):
    """(True when the file is applied as it stands, the line that says so or why not, the prepared plan)."""
    ready = prepare(root, data, name, routes)
    entry = applied(data, name)
    if not ready["exists"]:
        return False, "no plan file yet: the ships fly the role's plan in force; `plan.py apply` writes the file from it", ready
    if ready["errors"]:
        return False, "the file fails the check and is not applied; the plan applied %s stays in force" % (entry.get("applied_at") or "before"), ready
    if entry.get("digest") != ready["digest"]:
        return False, "changed since it was applied: run `plan.py apply` (the five-minute job applies it too)", ready
    return True, "applied %s by %s" % (entry.get("applied_at") or "?", entry.get("by") or "?"), ready


def brief(ready):
    """The plan in a few lines: the two lists, and the ships by their own routes."""
    plan, groups = ready["plan"], {}
    for ship, _role, _row in ready["crew"]:
        groups.setdefault(" > ".join(plan["ships"].get(ship) or []) or "no route of its own", []).append(ship)
    lines = ["  First, for every ship (%d): %s" % (len(plan["first"]), " > ".join(plan["first"]) or "none")]
    for own, ships in groups.items():
        lines.append("  %2d ships (%s): %s" % (len(ships), ", ".join(ships[:3]) + (" ..." if len(ships) > 3 else ""), own))
    kit = plan.get("templates") or {}
    for key in [key for key in kit if users(plan, key)]:
        lines.append("     @%s: %s" % (key, " > ".join(kit[key]["routes"])))
    lines.append("  Then, for every ship (%d): %s" % (len(plan["then"]), " > ".join(plan["then"]) or "none"))
    return lines


def show(root, data, names, short):
    routes = dispatch.load_routes(root)
    code = 0
    for name in names:
        _good, word, ready = state(root, data, name, routes)
        own = sum(1 for ship, _role, _row in ready["crew"] if ready["plan"]["ships"].get(ship))
        print("PLAN FILE | %s (%s) | %s | %d ships, %d with routes of their own | %s" % (name, DIVISIONS[name], path_of(data, name), len(ready["crew"]), own, word))
        for text in ready["errors"][:12]:
            print("  HALT: " + text)
        for text in ready["warnings"][:8]:
            print("  note: " + text)
        if ready["errors"]:
            code = 1
        elif short:
            print("\n".join(brief(ready)))
        else:
            print(ready["text"] if not ready["exists"] else path_of(data, name).read_text(encoding="ascii", errors="replace"))
    return code


def template_text(name, kit):
    """The text of a division's templates file, in its one form: the fields a template does not use are left out."""
    body = {}
    for key, entry in kit.items():
        one = {"title": entry["title"]} if entry.get("title") else {}
        one["routes"] = list(entry["routes"])
        if entry.get("trains"):
            one["trains"] = list(entry["trains"])
        if entry.get("note"):
            one["note"] = entry["note"]
        body[key] = one
    return json.dumps({"division": name, "owner": DIVISIONS[name], "templates": body}, indent=1) + "\n"


def list_templates(root, data, names):
    """Print each division's templates: name, title, trains, routes in order, and the ships of its plan that name it."""
    routes = dispatch.load_routes(root)
    for name in names:
        kit, _owner, faults = routefiles.templates_of(root, name)
        plan, _exists = load(root, data, name, routes)
        if not kit and not faults:
            print("TEMPLATES | %s (%s) | none yet: `plan.py template <name> <routes>` makes one, `plan.py use <ships> <name>` puts ships on it" % (name, DIVISIONS[name]))
            continue
        print("TEMPLATES | %s (%s) | game/routes/templates/%s.json | %d templates, %d ships on them" % (
            name, DIVISIONS[name], name, len(kit), sum(1 for ids in plan["ships"].values() if any(word.startswith("@") and word[1:] in kit for word in ids))))
        for text in faults + routefiles.template_faults(kit, routes):
            print("  HALT: " + text)
        for key, entry in kit.items():
            print("  @%s -- %s | trains %s | %d ships" % (key, entry["title"] or "no title", ", ".join(entry["trains"]) or "--", len(users(plan, key))))
            print("      %s" % (" > ".join(entry["routes"]) or "no route"))
            if entry["note"]:
                print("      note: " + entry["note"])
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data", "--division", "--title", "--trains", "--note"))]
    verb = words[0] if words and words[0] in ("show", "check", "apply", "set", "first", "then", "templates", "template", "use") else "show"
    rest = words[1:] if words and words[0] == verb else words
    kind, who = division.member()
    who = who if kind == "member" else ""
    mine = division_of(who) if who else None

    def named(word):
        if word == "all":
            return sorted(DIVISIONS)
        found = division_of(word)
        if not found:
            sys.exit("`%s` is no division, no member and no role: %s, or all" % (word, ", ".join(sorted(DIVISIONS))))
        return [found]

    if verb in ("show", "check", "templates"):
        names = named(rest[0]) if rest else ([mine] if mine and who != "Unity" else sorted(DIVISIONS))
        if verb == "templates":                               # reading is free
            return list_templates(root, data, names)
        if verb == "show":
            return show(root, data, names, "--brief" in args)
        routes, code = dispatch.load_routes(root), 0
        for name in names:
            good, word, ready = state(root, data, name, routes)
            print("%s %s: %s%s" % ("PASS" if good else "HALT", name, word, "".join("\n  " + text for text in ready["errors"][:12])))
            code = code if good else 1
        return code
    if not who:
        sys.exit("REFUSED: this shell is no member of The Collective: it changes no plan")

    def allowed(names):
        for name in names:
            if who != "Unity" and DIVISIONS[name] != who:
                sys.exit("REFUSED: the plan of the %s division is kept by %s (rule F1): ask in requests.log" % (name, DIVISIONS[name]))
        return names

    if verb == "apply":
        names = allowed(named(rest[0]) if rest else ([mine] if who != "Unity" else sorted(DIVISIONS)))
        good, lines = apply(root, data, names, who)
        quiet = "--quiet" in args                             # the five-minute job: only what changed or halted
        lines = [line for line in lines if not quiet or line.startswith(("HALT", "REFUSED", "committed")) or ": applied |" in line]
        if lines:
            print("\n".join(lines))
        return 0 if good else 1
    if not value("--division", mine or ""):
        sys.exit("name the division: --division <%s>" % "|".join(sorted(DIVISIONS)))
    name = allowed(named(value("--division", mine or "")))[0]
    if verb == "template" and len(rest) == 2:
        key = rest[0][1:] if rest[0].startswith("@") else rest[0]
        if not routefiles.TEMPLATE.fullmatch(key) or division.pilots_named(key):
            sys.exit("REFUSED: `%s` is no template name: 2 to 40 lower-case letters, digits and dashes, a letter first, never a pilot's name" % key)
        kit, _owner, faults = routefiles.templates_of(root, name)
        if faults:
            sys.exit("REFUSED: game/routes/templates/%s.json fails its check; mend it by hand first:\n  %s" % (name, "\n  ".join(faults)))
        texts = [value(option, "") for option in ("--title", "--note", "--trains")]
        if any(ord(c) > 127 or c in "\n\r" for text in texts for c in text):
            sys.exit("REFUSED: a template's title, trains and note are one line of ASCII")
        if rest[1].strip().lower() in ("none", "-", "--"):
            if key not in kit:
                sys.exit("REFUSED: the %s division has no template `%s` (%s)" % (name, key, ", ".join("@" + k for k in kit) or "none"))
            ships = users(load(root, data, name)[0], key)
            if ships:
                sys.exit("REFUSED: the template @%s stands in the own routes of %d ships of the %s division (%s%s): give them other routes first "
                         "(`plan.py use` or `plan.py set`), then remove it" % (key, len(ships), name, ", ".join(ships[:4]), " ..." if len(ships) > 4 else ""))
            del kit[key]
            note = "%s templates: @%s removed (plan.py, %s)" % (name, key, who)
        else:
            ids, was = tokens(rest[1]), kit.get(key) or {}
            kit[key] = {"title": value("--title", was.get("title") or ""), "routes": ids, "note": value("--note", was.get("note") or ""),
                        "trains": tokens(value("--trains", ",".join(was.get("trains") or [])))}       # an option not given keeps its value
            note = "%s templates: @%s %s %s (plan.py, %s)" % (name, key, "is now" if was else "made:", " > ".join(ids) or "no route", who)
        good, lines = apply(root, data, [name], who, extra={TEMPLATES + name + ".json": template_text(name, kit)}, message=note)
        print("\n".join(lines))
        return 0 if good else 1
    if verb in ("set", "use") and len(rest) == 2:
        ships, unknown = ships_named(rest[0], crew_of(data, name))
        if unknown or not ships:
            sys.exit("REFUSED: no ship of the %s division: %s" % (name, ", ".join(unknown) or rest[0]))
        ids = tokens(rest[1]) if verb == "set" else ["@" + (word[1:] if word.startswith("@") else word) for word in tokens(rest[1])]
        if verb == "use" and not ids:
            sys.exit("REFUSED: name a template (`plan.py templates` lists them); `plan.py set <ships> none` takes their own routes away")
        change = lambda plan: plan["ships"].update({ship: list(ids) for ship in ships})
        note = "%s plan: %d ships fly %s (plan.py, %s)" % (name, len(ships), " > ".join(ids) or "no route of their own", who)
    elif verb in ("first", "then") and len(rest) == 1:
        ids = tokens(rest[0])
        change = lambda plan: plan.update({verb: list(ids)})
        note = "%s plan: the list %s set (plan.py, %s)" % (name, verb.capitalize(), who)
    else:
        sys.exit(__doc__)
    good, lines = apply(root, data, [name], who, changes={name: change}, message=note)
    print("\n".join(lines))
    return 0 if good else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
