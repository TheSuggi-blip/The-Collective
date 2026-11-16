#!/usr/bin/env python3
"""routes.py -- check the route files, write their index, and attach what the runs measured.

WHAT: game/routes/<id>.json are the fleet's tasks (game/routes/BLUEPRINT.md); game/routes/plans/<role>.json
      lists them per role, one file per role, kept by the role's Admiral. This script
        check     validates every route file and the plans (the gate);
        index     writes three files in game/routes/: master-index.md (the groups of routes and the
                  plans at a glance; every name is a link into the two below), index.md (every
                  route with its measured figures, grouped by what it is for, with its zone) and
                  plan.md (every role's plan in its order, and what is planned);
        measure   reads the runs (data/routes/runs.jsonl) and prints, per route, runs,
                  minutes and credits per ship-hour; with --write it stores the figures
                  in the route file's `measured` block when they moved by a fifth or more.
RULES:
  - A route's id is its file name; its systems are on the chart (game/map/galaxy.tsv).
  - A plan names only routes that exist and carries its role's Admiral as
    `owner`. The last route of every list is always open: the `park` route
    (dock and wait: a docked ship costs nothing) or a mine, not `off`, not
    `once`, without `max_ships`, `min_credits`, `requires` and
    `skip_if_booked`. A list that can run out leaves a ship adrift.
  - The three index files are written by this script, never by hand; `check` fails on a stale one.
  - A route's group comes from its own file: once per pilot, paying (measured above zero), a
    test (not measured yet), a fitting, reading and waiting (census, park), measured at a loss,
    off. Its zone comes from the chart: home space when every system it touches is our
    empire's, beyond the border otherwise.
  - A measured block changes only on a real move, so a pass rarely makes a commit.
  - A hunt is not credited with what it got for goods it carried in from an
    earlier run: those were earned on another route.
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

KINDS = {"circuit": ("stops",), "hunt": ("place", "sell_at"), "census": ("systems",), "mine": ("belt", "station")}
FRONT = "---\nname: %s\nid: %s\ntier: intel\nauthor: Unity\n---\n\n"
INDEXES = (("index.md", "routes-index"), ("plan.md", "routes-plan"), ("master-index.md", "routes-master-index"))
STAGES = (("once", "Once per Pilot", "Missions and rewards the game pays once per pilot: a new pilot's first work, and seed money."),
          ("paying", "Paying Routes", "Work that repeats and whose runs measured above zero."),
          ("test", "Tests", "Work that repeats and has no measured figure yet: one ship until its first RESULT line is read."),
          ("fit", "Fitting", "A module bought and fitted: the tool a kind of work needs."),
          ("service", "Reading and Waiting", "The census and the park route: they earn nothing; they keep the picture fresh and a ship without work docked."),
          ("losing", "Measured at a Loss", "Work that repeats and whose runs measured zero or below."),
          ("off", "Off", "Written down, not flown."))


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


def systems_of(route):
    places = []
    if route.get("kind") == "circuit":
        places += [str(s.get("at", "")) for s in route.get("stops") or [] if isinstance(s, dict)]
        places += [str(step.get("at", "")) for s in route.get("stops") or [] if isinstance(s, dict)
                   for key in ("mine", "hunt") for step in s.get(key) or [] if isinstance(step, dict)]
    places += [str(route.get(k, "")) for k in ("place", "sell_at", "belt", "station")]
    return [p.split(":")[0] for p in places if p] + list(route.get("systems") or [])


def check(root):
    routes, errors = routes_of(root)
    known = chart(root)
    for rid, route in routes.items():
        where = "game/routes/%s.json: " % rid
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
        if kind == "circuit":
            for n, stop in enumerate(route.get("stops") or [], 1):
                if not isinstance(stop, dict) or len(str(stop.get("at", "")).split(":")) != 3:
                    errors.append(where + "stop %d: `at` must be system:poi:base" % n)
                    continue
                for key in ("mine", "hunt"):
                    for step in stop.get(key) or []:
                        if not isinstance(step, dict) or len(str(step.get("at", "")).split(":")) != 2:
                            errors.append(where + "stop %d: the `at` of a `%s` step must be system:poi" % (n, key))
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
        for rid in ids:
            if rid not in routes:
                errors.append(where + "names `%s`, which is no route file" % rid)
        last = routes.get(ids[-1]) if ids else None
        closed = [key for key in ("once", "max_ships", "min_credits", "requires", "skip_if_booked") if (last or {}).get(key)] + (["status off"] if (last or {}).get("status") == "off" else [])
        if last is not None and (closed or not (last.get("park") or last.get("kind") == "mine")):
            errors.append(where + "must end with a route that is always open (the `park` route, or a mine, without %s); `%s` is not, and a list that runs out leaves a ship adrift"
                          % (", ".join(closed) or "limits", ids[-1]))
        if not ids:
            errors.append(where + "`routes` is empty: end it with the `park` route")
    if routes:
        files = index_files(root, keep_id=True)
        for name, _front in INDEXES:
            if files[name] != current_index(root, name):
                errors.append("game/routes/%s is missing or stale: run `python3 -B game/fleet/routes.py index` (index.md, plan.md and master-index.md are written together)" % name)
    return errors, len(routes)


def current_index(root, name="index.md"):
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


def stage(route):
    """The group a route stands in, from its own file (STAGES)."""
    measured = route.get("measured") or {}
    if route.get("status") == "off":
        return "off"
    if route.get("park") or route.get("kind") == "census":
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
            route.get("status", "")]
    return ", ".join(g for g in gate if g) or "every pilot"


def figure(route):
    measured = route.get("measured") or {}
    return ("one-time" if route.get("once") else format(measured["cph_per_ship"], ",")) if measured else "TBD"


def anchor(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def stamps(root, keep_id):
    """{file name: id}: the id a file carries; a file without one gets a new id, a second apart each and never on a full
    minute, or None under keep_id."""
    out, moment = {}, time.time() - len(INDEXES) - 1
    for name, _front in INDEXES:
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
    """{file name: text} of index.md, plan.md and master-index.md. Under keep_id a file that has no id yet reads `missing`."""
    routes, _errors = routes_of(root)
    systems, home = atlas(root)
    ids = stamps(root, keep_id)
    facts = {}
    for rid, route in routes.items():
        where, far = zone(route, systems, home)
        facts[rid] = {"stage": stage(route), "zone": where, "far": far}
    titles = {key: title for key, title, _text in STAGES}
    place = lambda rid: facts[rid]["zone"] + (", %d jumps" % facts[rid]["far"] if facts[rid]["far"] and facts[rid]["zone"] == "beyond the border" else "")
    order = lambda rid: (facts[rid]["zone"] != "home space", routes[rid].get("kind", ""), rid)
    groups = [(key, title, text, sorted((r for r in routes if facts[r]["stage"] == key), key=order)) for key, title, text in STAGES]
    groups = [g for g in groups if g[3]]

    index = ["# index.md -- Routes We Fly", "",
             "Written by `python3 -B game/fleet/routes.py index`, never by hand. A route is a",
             "task one pilot carries out by itself; its file is `game/routes/<id>.json`",
             "(`BLUEPRINT.md`). The figures are what our own runs measured. The groups and the",
             "plans at a glance: [master-index.md](master-index.md); every plan in its order:",
             "[plan.md](plan.md). Inside a group: home space first, then by kind and name."]
    for _key, title, text, rids in groups:
        index += ["", "## " + title, "", text, "",
                  "| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for rid in rids:
            route, m = routes[rid], routes[rid].get("measured") or {}
            index.append("| [%s](%s.json) | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                rid, rid, cell(route.get("kind", "")), place(rid), cell(route.get("title", "")), cell(open_to(route)), m.get("runs", "TBD"), m.get("minutes", "TBD"),
                format(m["credits_per_run"], ",") if m else "TBD", figure(route), m.get("date", "--")))

    roles, owners, _plan_errors = division.load_plan(root)
    planned = {}
    for role in roles:
        try:
            items = read_json(Path(root) / "routes" / "plans" / (role + ".json")).get("planned") or []
        except (OSError, ValueError):
            items = []
        planned[role] = [i for i in items if isinstance(i, dict) and i.get("what")]
    plan = ["# plan.md -- The Plans", "",
            "Written by `python3 -B game/fleet/routes.py index`, never by hand, from",
            "`plans/<role>.json`: per role (the word before the dash of a pilot's name) the routes",
            "the dispatcher tries in this order for a free pilot. The role's Admiral keeps the",
            "file; `planned` in it is what the Admiral means to do next. The roles at a glance:",
            "[master-index.md](master-index.md); every route's figures: [index.md](index.md)."]
    for role in sorted(roles):
        plan += ["", "## " + role, "", "Kept by %s. Routes: %d." % (owners.get(role) or "--", len(roles[role])), "",
                 "| # | Route | Group | Zone | Open to | Credits per ship-hour |", "|---|---|---|---|---|---|"]
        for n, rid in enumerate(roles[role], 1):
            if rid in routes:
                plan.append("| %d | [%s](%s.json) | %s | %s | %s | %s |" % (n, rid, rid, titles[facts[rid]["stage"]], place(rid), cell(open_to(routes[rid])), figure(routes[rid])))
            else:
                plan.append("| %d | %s | no route file | -- | -- | -- |" % (n, cell(rid)))
        if planned[role]:
            plan += ["", "Planned:", "", "| What | When |", "|---|---|"] + ["| %s | %s |" % (cell(i.get("what", "")), cell(i.get("when", "--"))) for i in planned[role]]

    def best(key, rids):
        seen = [(routes[r]["measured"], r) for r in rids if routes[r].get("measured")]
        if not seen:
            return "not measured yet"
        field, unit = ("credits_per_run", "cr a run") if key == "once" else ("cph_per_ship", "cr per ship-hour")
        m, rid = max(seen, key=lambda pair: pair[0].get(field) or 0)
        return "%s: %s %s" % (rid, format(m.get(field) or 0, ","), unit)

    master = ["# master-index.md -- Routes and Plans", "",
              "Written by `python3 -B game/fleet/routes.py index`, never by hand. Start here: every",
              "name below is a link into one of the sub-indexes of this folder.", "",
              "| File | Holds |", "|---|---|",
              "| [index.md](index.md) | Every route with its measured figures, group by group |",
              "| [plan.md](plan.md) | Every role's plan in its order, and what its Admiral means to do next |",
              "| [BLUEPRINT.md](BLUEPRINT.md) | How a route is written, and what is automatic |",
              "", "## Routes by Group", "",
              "| Group | What it holds | Routes | Home space | Beyond the border | Best measured |", "|---|---|---|---|---|---|"]
    for key, title, text, rids in groups:
        master.append("| [%s](index.md#%s) | %s | %d | %d | %d | %s |" % (
            title, anchor(title), cell(text), len(rids), sum(1 for r in rids if facts[r]["zone"] == "home space"),
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
        master += ["", "## Plans by Role", "", "| Role | Kept by | Routes | The first three, in order | Planned |", "|---|---|---|---|---|"]
        for role in sorted(roles):
            master.append("| [%s](plan.md#%s) | %s | %d | %s | %d |" % (cell(role), anchor(role), cell(owners.get(role) or "--"), len(roles[role]),
                                                                    cell(" > ".join(roles[role][:3])), len(planned[role])))
    books = sorted((Path(root) / "routes" / "guidebook").glob("*.md")) if (Path(root) / "routes" / "guidebook").is_dir() else []
    if books:
        master += ["", "## The Guidebooks", "", "What each division learned about its routes, its levelling and its ships; kept by its Admiral, read by every member.", "",
                   "| Guidebook | Title |", "|---|---|"]
        for path in books:
            title = next((l[2:].strip() for l in path.read_text(encoding="ascii", errors="replace").splitlines() if l.startswith("# ")), path.stem)
            master.append("| [guidebook/%s](guidebook/%s) | %s |" % (path.name, path.name, cell(title)))
    texts = {"index.md": index, "plan.md": plan, "master-index.md": master}
    return {name: (FRONT % (front, ids[name]) + "\n".join(texts[name]) + "\n") if ids[name] else "missing" for name, front in INDEXES}


def write_index(root):
    """Write the index files that changed; [(file name, `written` or `current`)]."""
    done = []
    for name, text in index_files(root).items():
        if text == current_index(root, name):
            done.append((name, "current"))
        else:
            (Path(root) / "routes" / name).write_text(text, encoding="ascii")
            done.append((name, "written"))
    return done


def earned(row):
    """A run's credits without the sale of goods it carried in: a hunt that sells another place's goods did not earn them."""
    if row.get("kind") != "hunt":
        return row.get("delta", 0)
    gained, carried = row.get("goods") or {}, 0.0
    for item, sale in (row.get("sold") or {}).items():
        units, credits = sale[0], sale[2]
        extra = units - gained.get(item, 0)
        if units > 0 and extra > 0:
            carried += credits * extra / units
    return row.get("delta", 0) - carried


def readable(row):
    """False for a run that read no wallet at its start or at its end: it says nothing about credits. A pilot's wallet is
    never 0 (it keeps a floor): a 0 at either end is the engine not answering."""
    before, after = row.get("credits_before"), row.get("credits_after")
    numbers = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (before, after))
    return numbers and before > 0 and after > 0 and "wallet not read" not in (row.get("notes") or [])


def measure(root, data, write, only=None):
    """Print what the runs measured per route; with `write`, store it in the route files, of the routes in `only` when given."""
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
    changed = []
    for rid in sorted({r.get("route") for r in rows if r.get("route")}):
        every = [r for r in rows if r.get("route") == rid and r.get("minutes")]
        mine = [r for r in every if readable(r)]
        if not mine:
            if every:
                print("%-28s runs %-4d none read a wallet: no figure" % (rid, len(every)))
                if write and (only is None or rid in only) and (routes.get(rid) or {}).get("measured"):
                    del routes[rid]["measured"]
                    (Path(root) / "routes" / (rid + ".json")).write_text(json.dumps(routes[rid], indent=1) + "\n", encoding="ascii")
                    changed.append(rid)
            continue
        minutes = sum(r["minutes"] for r in mine)
        figure = {"date": time.strftime("%Y-%m-%d", time.gmtime()), "runs": len(mine), "minutes": round(statistics.median(r["minutes"] for r in mine)),
                  "credits_per_run": int(round(sum(earned(r) for r in mine) / len(mine), -1)),
                  "cph_per_ship": int(round(60 * sum(earned(r) for r in mine) / minutes, -1)) if minutes else 0}
        print("%-28s runs %-4d minutes %-4d credits per run %-8s per ship-hour %-8s %s" % (
            rid, figure["runs"], figure["minutes"], format(figure["credits_per_run"], ","), format(figure["cph_per_ship"], ","),
            ("" if rid in routes else "(no route file)") + (" (%d more runs read no wallet)" % (len(every) - len(mine)) if len(every) > len(mine) else "")))
        old = (routes.get(rid) or {}).get("measured") or {}
        moved = not old or abs(figure["cph_per_ship"] - old.get("cph_per_ship", 0)) >= 0.2 * max(abs(old.get("cph_per_ship", 0)), 100) \
            or figure["runs"] >= 2 * max(old.get("runs", 0), 1)
        if write and (only is None or rid in only) and rid in routes and moved:
            routes[rid]["measured"] = figure
            (Path(root) / "routes" / (rid + ".json")).write_text(json.dumps(routes[rid], indent=1) + "\n", encoding="ascii")
            changed.append(rid)
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
        if any(state == "written" for _name, state in done):
            print("commit the three together: git add -- game/routes/index.md game/routes/plan.md game/routes/master-index.md")
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
