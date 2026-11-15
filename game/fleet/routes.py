#!/usr/bin/env python3
"""routes.py -- check the route files, write their index, and attach what the runs measured.

WHAT: game/routes/<id>.json are the fleet's tasks (game/routes/BLUEPRINT.md); game/routes/plan.json
      lists them per role. This script
        check     validates every route file and the plan (the gate);
        index     writes game/routes/index.md: every route with its measured figures and the plan;
        measure   reads the runs (data/routes/runs.jsonl) and prints, per route, runs,
                  minutes and credits per ship-hour; with --write it stores the figures
                  in the route file's `measured` block when they moved by a fifth or more.
RULES:
  - A route's id is its file name; its systems are on the chart (game/map/galaxy.tsv).
  - The plan names only routes that exist, and the last route of every
    role's list is always open: not `off`, not `once`, without `max_ships`,
    `min_credits` and `requires`. A list that can fill up leaves a ship idle.
  - index.md is written by this script, never by hand; `check` fails on a stale one.
  - A measured block changes only on a real move, so a pass rarely makes a commit.
  - A hunt is not credited with what it got for goods it carried in from an
    earlier run: those were earned on another route.
  - A run that read no wallet (no credits before and after, both 0, or the note
    `wallet not read`) counts for nothing: a route whose runs are all such has
    no figure, and a figure built on them is taken out of its file.
WHY:  what a route pays is written next to the route, and a wrong file is caught
      before a pilot flies it.

USAGE:
  routes.py check | index | measure [--write]      [--root <dir>] [--data <dir>]

Stdlib only. ASCII only.
"""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

KINDS = {"circuit": ("stops",), "hunt": ("place", "sell_at"), "census": ("systems",), "mine": ("belt", "station")}
FRONT = "---\nname: routes-index\nid: %s\ntier: intel\nauthor: Unity\n---\n"


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
        for key, parts in (("place", 2), ("belt", 2), ("sell_at", 3), ("station", 3)):
            if route.get(key) and len(str(route[key]).split(":")) != parts:
                errors.append(where + "`%s` must have %d parts joined by a colon" % (key, parts))
        for system in systems_of(route):
            if known and system not in known:
                errors.append(where + "system `%s` is not on the chart" % system)
    plan_path = Path(root) / "routes" / "plan.json"
    if plan_path.is_file():
        try:
            for role, ids in (read_json(plan_path).get("roles") or {}).items():
                for rid in ids:
                    if rid not in routes:
                        errors.append("game/routes/plan.json: role `%s` names `%s`, which is no route file" % (role, rid))
                last = routes.get(ids[-1]) if ids else None
                closed = [key for key in ("once", "max_ships", "min_credits", "requires") if (last or {}).get(key)] + (["status off"] if (last or {}).get("status") == "off" else [])
                if last is not None and (closed or last.get("kind") not in ("mine",)):
                    errors.append("game/routes/plan.json: role `%s` must end with a route that is always open (a mine without %s); `%s` is not, and a full list leaves a ship idle"
                                  % (role, ", ".join(closed) or "limits", ids[-1]))
        except (OSError, ValueError) as error:
            errors.append("game/routes/plan.json: not readable as ASCII JSON: %s" % error)
    if routes and index_text(root, keep_id=True) != current_index(root):
        errors.append("game/routes/index.md is missing or stale: run `python3 -B game/fleet/routes.py index`")
    return errors, len(routes)


def current_index(root):
    path = Path(root) / "routes" / "index.md"
    return path.read_text(encoding="ascii") if path.is_file() else ""


def cell(value):
    return str(value).replace("|", "/").replace("\n", " ")


def index_text(root, keep_id=False):
    routes, _errors = routes_of(root)
    old = current_index(root)
    stamp = old.split("\nid: ", 1)[1].split("\n", 1)[0] if "\nid: " in old else ""
    if not stamp:
        if keep_id:
            return "missing"
        moment = time.time()
        while time.gmtime(moment).tm_sec == 0:
            moment += 1
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(moment))
    lines = [FRONT % stamp, "# index.md -- Routes We Fly", "",
             "Written by `python3 -B game/fleet/routes.py index`, never by hand. A route is a",
             "task one pilot carries out by itself; its file is `game/routes/<id>.json`",
             "(`BLUEPRINT.md`). The figures are what our own runs measured.", "",
             "| Route | Kind | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |",
             "|---|---|---|---|---|---|---|---|---|"]
    for rid, route in sorted(routes.items(), key=lambda kv: (kv[1].get("kind", ""), kv[0])):
        m = route.get("measured") or {}
        gate = [("once per pilot" if route.get("once") else ""), ("up to %s ships" % route["max_ships"] if route.get("max_ships") else ""),
                ("needs %s" % route["requires"]["module"] if (route.get("requires") or {}).get("module") else ""), route.get("status", "")]
        per_hour = ("one-time" if route.get("once") else format(m["cph_per_ship"], ",")) if m else "TBD"
        lines.append("| [%s](%s.json) | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            rid, rid, cell(route.get("kind", "")), cell(route.get("title", "")), cell(", ".join(g for g in gate if g) or "every pilot"),
            m.get("runs", "TBD"), m.get("minutes", "TBD"), format(m["credits_per_run"], ",") if m else "TBD", per_hour, m.get("date", "--")))
    plan_path = Path(root) / "routes" / "plan.json"
    if plan_path.is_file():
        lines += ["", "## The Plan", "", "`plan.json`: per role, the routes the dispatcher tries in this order for a free pilot.", "",
                  "| Role | Routes, first that is open |", "|---|---|"]
        try:
            for role, ids in sorted((read_json(plan_path).get("roles") or {}).items()):
                lines.append("| %s | %s |" % (cell(role), cell(" > ".join(ids))))
        except (OSError, ValueError):
            lines.append("| -- | plan.json is not readable |")
    return "\n".join(lines) + "\n"


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
    """False for a run that read no wallet: it says nothing about credits. A pilot's wallet is never 0 (it keeps a floor)."""
    before, after = row.get("credits_before"), row.get("credits_after")
    numbers = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (before, after))
    return numbers and bool(before or after) and "wallet not read" not in (row.get("notes") or [])


def measure(root, data, write):
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
                if write and (routes.get(rid) or {}).get("measured"):
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
        if write and rid in routes and moved:
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
    args = parser.parse_args()
    if args.command == "check":
        errors, count = check(args.root)
        for line in errors:
            print("ERROR " + line)
        print("Checked %d route files." % count)
        print("Errors: %d | Warnings: 0" % len(errors))
        return 1 if errors else 0
    if args.command == "index":
        text = index_text(args.root)
        if text == current_index(args.root):
            print("game/routes/index.md: current")
        else:
            (Path(args.root) / "routes" / "index.md").write_text(text, encoding="ascii")
            print("game/routes/index.md: written")
        return 0
    return measure(args.root, args.data, args.write)


if __name__ == "__main__":
    sys.exit(main())
