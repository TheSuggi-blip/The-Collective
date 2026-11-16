#!/usr/bin/env python3
"""catalog-index.py -- build game/catalog/: every recipe, facility, hull, module and item of the game, as a master index with sub-indexes.

WHAT: the game publishes its catalog (the route maker fetches it once a day
      into the unit's data folder, catalog/<version>.json). This script turns
      it into files every member can read, search and click through:
        master-index.md          start here: every group with its count, every name a link
        recipes/<category>.md    the recipes of one category: what each makes, from what, where
        ships/<empire>.md        the hulls of one empire, tier by tier
        modules.md               every module, slot by slot
        facilities.md            what founding a base takes, and every facility that is no
                                 production line: the faction's, defense, personal, service
        skills.md                every skill and what a level gives
        tables/*.tsv             the full tables (recipes, facilities, ships, modules, items)
                                 for a search by text and for scripts
RULES:
  - Built from the catalog, never written by hand. A new release of the game
    is a new catalog: the hourly job rebuilds the folder.
  - The catalog is the game's public data; nothing of ours is in these files.
  - A file is rewritten only when its text changed; the master index keeps
    its id. A file the catalog no longer gives (a category that is gone) is
    removed.
  - --check fails a stale or missing folder when a catalog is on disk, and
    passes with a note where none is (a machine without the data folder).
  - --commit commits the folder by path as Unity when it was written. It
    writes nothing while game/catalog/ holds a change that is not committed.
WHY:  what a division can make, fit, fly and build was looked up call by
      call, by each Admiral for itself. One set of tables, kept by a script,
      is the same for all and is current with the game; a master index with
      sub-indexes keeps every file short enough to read (Suggi, 2026-11-16).

USAGE:
  catalog-index.py              write game/catalog/ when it changed
  catalog-index.py --check      the gate: exit 1 when the folder is stale or missing
  catalog-index.py --commit     write, and commit the folder by path as Unity (the hourly job)
  --root <dir>                  repository root (default: the parent of this file's folder)
  --catalog <file>              the catalog to read (default: the newest in /srv/collective/data/catalog/)

Stdlib only. ASCII only.
"""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

FOLDER = "game/catalog"
DATA = "/srv/collective/data/catalog"
HOME_EMPIRE = "voidborn"
ID = re.compile(r"^id: (\S+)$", re.M)
FOUNDING = (("outpost_kit", "An outpost"), ("station_core", "A station"))
BUILT = "Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version %s; never edited by hand."


def newest(folder=DATA):
    """The catalog file of the highest version in the data folder, or None."""
    files = [p for p in Path(folder).glob("*.json") if re.fullmatch(r"\d+(\.\d+)*", p.stem)] if Path(folder).is_dir() else []
    return max(files, key=lambda p: tuple(int(n) for n in p.stem.split("."))) if files else None


def plain(value):
    """One cell: ASCII, one line, no tab."""
    return " ".join(str("" if value is None else value).split()).encode("ascii", "replace").decode("ascii")


def cell(text):
    return plain(text).replace("|", "/")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-") or "none"


def parts(rows):
    """`item x qty; item x qty` of a list of {item_id, quantity}."""
    return "; ".join("%s x %s" % (r.get("item_id"), r.get("quantity")) for r in rows or [] if isinstance(r, dict))


def flags(row, names):
    return ", ".join(n if row[n] is True else "%s=%s" % (n, plain(row[n])) for n in names if row.get(n))


def money(value):
    return "{:,}".format(int(value)) if isinstance(value, (int, float)) else "--"


def gives(facility):
    return facility.get("faction_service_type") or facility.get("service_type") or facility.get("personal_service_type")


def table(head, rows):
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]


def tsv(title, version, columns, rows):
    head = ["# %s" % title, "# Source: the game's public catalog, version %s | Rows: %d" % (version, len(rows)),
            "# Written by scripts/catalog-index.py. Do not edit by hand.", "\t".join(columns)]
    return "\n".join(head + ["\t".join(plain(c) for c in row) for row in rows]) + "\n"


TABLES = {"recipes.tsv": ["id", "name", "category", "makes", "from", "time", "by_hand", "facilities", "notes"],
          "facilities.tsv": ["id", "name", "category", "level", "upgrades_from", "recipe", "build_cost", "build_time", "labor_cost", "materials", "power_draw",
                             "life_support_draw", "gives", "needs_service", "empire", "notes"],
          "ships.tsv": ["id", "name", "empire", "class", "category", "tier", "piloting_required", "shipyard_tier", "hull", "shield", "armor", "speed", "fuel", "cargo",
                        "cpu", "power", "weapon_slots", "defense_slots", "utility_slots", "crew", "build_time", "build_materials", "default_modules", "notes"],
          "modules.tsv": ["id", "name", "type", "slot", "cpu", "power", "size", "base_value", "damage", "reach", "cooldown", "effect", "special"],
          "items.tsv": ["id", "name", "category", "rarity", "size", "base_value", "made_by", "used_in_recipes", "used_in_builds", "extracted_by"]}


def tables(cat):
    """{tables/<name>.tsv: text} of the five full tables."""
    version = cat.get("version") or "?"
    recipes, items = cat.get("recipes") or [], cat.get("items") or []
    makes, uses, builds = {}, {}, {}
    for r in recipes:
        for o in r.get("outputs") or []:
            makes.setdefault(o.get("item_id"), []).append(r["id"])
        for i in r.get("inputs") or []:
            uses[i.get("item_id")] = uses.get(i.get("item_id"), 0) + 1
    for row in (cat.get("facilities") or []) + (cat.get("ships") or []):
        for m in row.get("build_materials") or []:
            builds[m.get("item_id")] = builds.get(m.get("item_id"), 0) + 1
    rows = {
        "recipes.tsv": ("Every recipe of the game: what it makes, from what, and where.",
                        [[r["id"], r.get("name"), r.get("category"), parts(r.get("outputs")), parts(r.get("inputs")), r.get("crafting_time"),
                          "yes" if r.get("hand_craftable") else "no", ", ".join(r.get("produced_by_facility_ids") or []),
                          flags(r, ("requires_unlock", "fuel_output", "package_operation", "no_recycle"))] for r in sorted(recipes, key=lambda r: r["id"])]),
        "facilities.tsv": ("Every facility of the game: what it makes or gives, and what building it takes.",
                           [[f["id"], f.get("name"), f.get("category"), f.get("level"), f.get("upgrades_from"), f.get("recipe_id"), f.get("build_cost"),
                             f.get("build_time"), f.get("labor_cost"), parts(f.get("build_materials")), f.get("power_draw"), f.get("life_support_draw"),
                             gives(f), f.get("requires_service_type"), f.get("empire"),
                             flags(f, ("unique", "player_station_buildable", "station_or_faction_only", "pirate_base_only", "faction_cap", "power_supply",
                                       "life_support_supply"))] for f in sorted(cat.get("facilities") or [], key=lambda f: f["id"])]),
        "ships.tsv": ("Every hull of the game: who builds it, what it needs, what it carries.",
                      [[s["id"], s.get("name"), s.get("faction"), s.get("class"), s.get("category"), s.get("tier"), s.get("piloting_required"), s.get("shipyard_tier"),
                        s.get("base_hull"), s.get("base_shield"), s.get("base_armor"), s.get("base_speed"), s.get("base_fuel"), s.get("cargo_capacity"),
                        s.get("cpu_capacity"), s.get("power_capacity"), s.get("weapon_slots"), s.get("defense_slots"), s.get("utility_slots"), s.get("crew_capacity"),
                        s.get("build_time"), parts(s.get("build_materials")), ", ".join(s.get("default_modules") or []),
                        flags(s, ("starter_ship", "npc_role", "prestige_lock", "required_reputation", "required_achievement", "required_faction_achievement",
                                  "mobile_base"))] for s in sorted(cat.get("ships") or [], key=lambda s: (str(s.get("faction")), s.get("tier") or 0, s["id"]))]),
        "modules.tsv": ("Every module of the game: its slot, what it draws, what it does.",
                        [[m["id"], m.get("name"), m.get("type"), m.get("slot"), m.get("cpu_usage"), m.get("power_usage"), m.get("size"), m.get("base_value"),
                          m.get("damage"), m.get("reach"), m.get("cooldown"), json.dumps(m.get("effect"), sort_keys=True) if m.get("effect") else "", m.get("special")]
                         for m in sorted((i for i in items if i.get("type")), key=lambda m: (str(m.get("slot")), str(m.get("type")), m["id"]))]),
        "items.tsv": ("Every item of the game: its kind, its size, its base value, how often it is made and used.",
                      [[i["id"], i.get("name"), i.get("category") or ("module" if i.get("type") else ""), i.get("rarity"), i.get("size"), i.get("base_value"),
                        ", ".join(makes.get(i["id"], [])[:6]), uses.get(i["id"], 0), builds.get(i["id"], 0), i.get("extracted_by")]
                       for i in sorted(items, key=lambda i: i["id"])])}
    return {"tables/" + name: tsv(title, version, TABLES[name], body) for name, (title, body) in rows.items()}, {name: len(body) for name, (_t, body) in rows.items()}


def where(recipe):
    plants = recipe.get("produced_by_facility_ids") or []
    if recipe.get("hand_craftable"):
        return "by hand" + (", or in: " + ", ".join(plants[:3]) if plants else "")
    return "in: " + ", ".join(plants[:4]) + (" (and %d more)" % (len(plants) - 4) if len(plants) > 4 else "") if plants else "in a facility"


def pages(cat):
    """({relative path: text} of the Markdown sub-indexes, the lines of the master index below its title)."""
    version = cat.get("version") or "?"
    recipes, facilities, ships, items = cat.get("recipes") or [], cat.get("facilities") or [], cat.get("ships") or [], cat.get("items") or []
    by_id = {f["id"]: f for f in facilities}
    built = BUILT % version
    out = {}

    # ---- recipes, one sub-index per category
    cats = {}
    for r in recipes:
        cats.setdefault(r.get("category") or "(none)", []).append(r)
    recipe_rows = []
    for name in sorted(cats, key=lambda n: (-len(cats[n]), n)):
        rows, hand = sorted(cats[name], key=lambda r: r["id"]), sum(1 for r in cats[name] if r.get("hand_craftable"))
        out["recipes/%s.md" % slug(name)] = "\n".join(
            ["# %s -- Recipes" % name, "", built, "Up: [master-index.md](../master-index.md). Recipes: %d; by hand: %d; in a facility only: %d." % (len(rows), hand, len(rows) - hand), ""]
            + table(["Recipe", "Makes", "From", "Where", "Time"], [["`%s`" % r["id"], parts(r.get("outputs")), parts(r.get("inputs")), where(r), r.get("crafting_time")] for r in rows])) + "\n"
        recipe_rows.append(["[%s](recipes/%s.md)" % (name, slug(name)), len(rows), hand, len(rows) - hand])

    # ---- hulls, one sub-index per empire
    fleets = {}
    for s in ships:
        fleets.setdefault("pirate and other" if s.get("npc_role") or not s.get("faction") else s["faction"], []).append(s)
    needs = {}
    for s in ships:
        if not s.get("npc_role") and s.get("piloting_required"):
            needs.setdefault(s.get("tier"), set()).add(s["piloting_required"])
    ladder = "; ".join("tier %s: Piloting %s" % (tier, " or ".join(str(n) for n in sorted(needs[tier]))) for tier in sorted(needs)) or "no hull names a Piloting level"
    ship_rows = []
    for name in sorted(fleets, key=lambda n: (n != HOME_EMPIRE, n)):
        rows = sorted(fleets[name], key=lambda s: (s.get("tier") or 0, str(s.get("category")), s["id"]))
        lines = ["# %s -- Hulls" % name.capitalize(), "", built,
                 "Up: [master-index.md](../master-index.md). Hulls: %d. The Piloting a tier needs, from the hulls of the catalog: %s." % (len(rows), ladder),
                 "What a hull is built from: `python3 -I -B game/fleet/craftbook.py build <hull id>`, or `tables/ships.tsv`."]
        for tier in sorted({s.get("tier") or 0 for s in rows}):
            lines += ["", "## Tier %s" % tier, ""] + table(
                ["Hull", "Class", "Work", "Piloting", "Yard tier", "Hull / shield / armor", "Speed", "Fuel", "Cargo", "Slots W / D / U", "CPU / power", "Fitted as built"],
                [["`%s`" % s["id"], s.get("class"), s.get("category"), s.get("piloting_required") or "--", s.get("shipyard_tier"),
                  "%s / %s / %s" % (s.get("base_hull"), s.get("base_shield"), s.get("base_armor")), s.get("base_speed"), s.get("base_fuel"), s.get("cargo_capacity"),
                  "%s / %s / %s" % (s.get("weapon_slots"), s.get("defense_slots"), s.get("utility_slots")), "%s / %s" % (s.get("cpu_capacity"), s.get("power_capacity")),
                  ", ".join(s.get("default_modules") or []) or "--"] for s in rows if (s.get("tier") or 0) == tier])
        out["ships/%s.md" % slug(name)] = "\n".join(lines) + "\n"
        ship_rows.append(["[%s](ships/%s.md)" % (name, slug(name)), len(rows), ", ".join("%s: %d" % (t, sum(1 for s in rows if (s.get("tier") or 0) == t)) for t in sorted({s.get("tier") or 0 for s in rows}))])

    # ---- modules, slot by slot
    modules = [i for i in items if i.get("type")]
    lines, module_rows = ["# Modules", "", built, "Up: [master-index.md](master-index.md). Modules: %d. A hull's slots and its cpu and power: the hull's row in `ships/`." % len(modules)], []
    for slot in sorted({str(m.get("slot")) for m in modules}):
        rows = sorted((m for m in modules if str(m.get("slot")) == slot), key=lambda m: (str(m.get("type")), m["id"]))
        lines += ["", "## %s" % slot.capitalize(), ""] + table(
            ["Module", "Kind", "CPU", "Power", "Base value", "What it does"],
            [["`%s`" % m["id"], m.get("type"), m.get("cpu_usage"), m.get("power_usage"), m.get("base_value"),
              ", ".join(x for x in ("damage %s %s" % (m.get("damage"), m.get("damage_type") or "") if m.get("damage") else "", "reach %s" % m["reach"] if m.get("reach") else "",
                                    "cooldown %s" % m["cooldown"] if m.get("cooldown") else "", json.dumps(m["effect"], sort_keys=True) if m.get("effect") else "",
                                    str(m["special"]) if m.get("special") else "") if x) or "--"] for m in rows])
        module_rows.append(["[%s](modules.md#%s)" % (slot, slug(slot)), len(rows), ", ".join(sorted({str(m.get("type")) for m in rows}))[:160]])
    out["modules.md"] = "\n".join(lines) + "\n"

    # ---- facilities that are no production line, and what founding a base takes
    lines = ["# Bases and Facilities", "", built,
             "Up: [master-index.md](master-index.md). What a facility's materials take down to the ore: `python3 -I -B game/fleet/craftbook.py build <facility id>`.",
             "", "## Founding a Base", "", "The part a founding needs, the recipe that makes it and the facility that runs the recipe.", ""]
    rows = []
    for item, what in FOUNDING:
        for r in recipes:
            if any(o.get("item_id") == item for o in r.get("outputs") or []):
                for fid in r.get("produced_by_facility_ids") or [""]:
                    f = by_id.get(fid) or {}
                    rows.append([what, "`%s`" % item, parts(r.get("inputs")), "`%s`" % fid if fid else "--", f.get("level", "--"), money(f.get("build_cost")), parts(f.get("build_materials"))])
    lines += table(["For", "Part", "The part is made from", "In the facility", "Level", "Facility cost (cr)", "Facility materials"], rows or [["--"] * 7])
    facility_rows = [["[Founding a Base](facilities.md#founding-a-base)", len(rows), "the kit of an outpost, the core of a station"]]
    kinds = sorted({str(f.get("category")) for f in facilities if f.get("category") != "production"})
    for kind in kinds:
        chosen = sorted((f for f in facilities if str(f.get("category")) == kind), key=lambda f: (str(gives(f)), f.get("level") or 0, f["id"]))
        lines += ["", "## %s" % kind.capitalize(), ""] + table(
            ["Facility", "Level", "Gives", "Needs first", "Cost (cr)", "Labor", "Materials", "Notes"],
            [["`%s`" % f["id"], f.get("level"), gives(f) or "--", f.get("requires_service_type") or "--", money(f.get("build_cost")), f.get("labor_cost"),
              parts(f.get("build_materials")) or "--", flags(f, ("unique", "player_station_buildable", "station_or_faction_only", "pirate_base_only", "empire")) or "--"] for f in chosen])
        facility_rows.append(["[%s](facilities.md#%s)" % (kind.capitalize(), slug(kind)), len(chosen), ", ".join(sorted({str(gives(f)) for f in chosen if gives(f)}))[:160] or "--"])
    lines_made = [f for f in facilities if f.get("category") == "production"]
    levels = ", ".join("level %s: %d" % (lv, sum(1 for f in lines_made if f.get("level") == lv)) for lv in sorted({f.get("level") for f in lines_made}, key=lambda v: v or 0))
    lines += ["", "## Production", "",
              "%d production lines (%s). Each runs one recipe: the recipe's row in `recipes/` names its" % (len(lines_made), levels or "none"),
              "lines; a line's cost and materials are in `tables/facilities.tsv` and in `craftbook.py build <facility id>`."]
    facility_rows.append(["[Production](facilities.md#production)", len(lines_made), "one recipe each; the full list is `tables/facilities.tsv`"])
    out["facilities.md"] = "\n".join(lines) + "\n"

    # ---- skills
    skills = sorted(cat.get("skills") or [], key=lambda s: str(s.get("id")))
    out["skills.md"] = "\n".join(["# Skills", "", built, "Up: [master-index.md](master-index.md). Skills: %d." % len(skills), ""]
                                 + table(["Skill", "Kind", "Top level", "What a level gives"], [["`%s`" % s.get("id"), s.get("category"), s.get("max_level"), s.get("description")] for s in skills] or [["--"] * 4])) + "\n"

    master = ["# master-index.md -- The Game's Catalog", "",
              built, "Start here: every name below is a link into one of the sub-indexes of this folder.",
              "Recipes: %d. Facilities: %d. Hulls: %d. Modules: %d. Items: %d. Skills: %d." % (len(recipes), len(facilities), len(ships), len(modules), len(items), len(skills)), "",
              "- Ask a question instead of reading a table: `python3 -I -B game/fleet/craftbook.py` from the",
              "  repository root. `item <text>` finds an item, how it is made and what uses it; `needs <item>",
              "  [quantity]` prints everything it takes down to what is mined or bought, beside what the fleet",
              "  has in storage; `build <facility or hull>` does the same for a building or a ship; `can` lists",
              "  what your division's stored goods can be made into by hand today, and what that sells for.",
              "- A figure here is the game's own. What something sells for is not here: the order books are",
              "  in the unit's data folder (`game/fleet/ledger.py prices <item>`).", "",
              "## Recipes by Category", ""]
    master += table(["Category", "Recipes", "By hand", "In a facility only"], recipe_rows or [["--"] * 4])
    master += ["", "## Bases and Facilities", ""] + table(["Group", "Entries", "Holds"], facility_rows)
    master += ["", "## Hulls by Empire", "", "The Piloting a tier needs: %s." % ladder, ""] + table(["Empire", "Hulls", "Hulls per tier"], ship_rows or [["--"] * 3])
    master += ["", "## Modules by Slot", ""] + table(["Slot", "Modules", "Kinds"], module_rows or [["--"] * 3])
    master += ["", "## Skills", "", "[skills.md](skills.md): %d skills, what a level of each gives." % len(skills)]
    return out, master


def build(root, cat):
    """{relative path: text} of the whole folder; the master index keeps its id."""
    files, counts = tables(cat)
    more, master = pages(cat)
    files.update(more)
    master += ["", "## Full Tables", "", "Tab-separated, one row per thing, a header row under three comment lines: for a search by text and for scripts.", ""]
    master += table(["Table", "Rows", "Columns"], [["`tables/%s`" % name, counts[name], ", ".join(TABLES[name])] for name in sorted(TABLES)])
    path = Path(root) / FOLDER / "master-index.md"
    kept = ID.search(path.read_text(encoding="ascii")) if path.is_file() else None
    stamp = kept.group(1) if kept else None
    if not stamp:
        moment = time.time()
        while time.gmtime(moment).tm_sec == 0:
            moment -= 1
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(moment))
    files["master-index.md"] = "---\nname: catalog-master-index\nid: %s\ntier: intel\nauthor: Unity\n---\n\n%s\n" % (stamp, "\n".join(str(line) for line in master))
    return files


def stale(root, files):
    """(files to write, files to remove): what differs from the folder, and what the folder holds beyond the build."""
    folder = Path(root) / FOLDER
    changed = sorted(name for name, text in files.items() if not (folder / name).is_file() or (folder / name).read_text(encoding="ascii", errors="replace") != text)
    extra = sorted(str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file() and str(p.relative_to(folder)) not in files) if folder.is_dir() else []
    return changed, extra


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def main():
    parser = argparse.ArgumentParser(description="Build game/catalog/ from the game's public catalog.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--catalog")
    args = parser.parse_args()
    source = Path(args.catalog) if args.catalog else newest()
    if source is None or not source.is_file():
        print("%s: no catalog on disk: not checked and not written" % FOLDER)
        return 0
    try:
        cat = json.loads(source.read_text(encoding="utf-8"))
    except ValueError as error:
        print("%s: the catalog %s is not readable: %s" % (FOLDER, source.name, error))
        return 1
    files = build(args.root, cat)
    changed, extra = stale(args.root, files)
    if args.check:
        if changed or extra:
            print("%s: stale or missing: %d file(s) to write (%s), %d to remove; run python3 -B scripts/catalog-index.py" % (FOLDER, len(changed), ", ".join(changed[:4]), len(extra)))
            return 1
        print("%s: current" % FOLDER)
        return 0
    if not changed and not extra:
        print("%s: current" % FOLDER)
        return 0
    if args.commit and git(args.root, "status", "--porcelain", "--", FOLDER)[1].strip():
        print("%s: holds a change that is not committed; nothing written" % FOLDER)
        return 0
    folder = Path(args.root) / FOLDER
    for name in changed:
        (folder / name).parent.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text(files[name], encoding="ascii")
    for name in extra:
        (folder / name).unlink()
    print("%s: written (%d files, %d removed), catalog %s" % (FOLDER, len(changed), len(extra), cat.get("version")))
    if args.commit:
        git(args.root, "add", "-A", "--", FOLDER)
        code, out = git(args.root, "-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev", "commit", "-q", "-m",
                        "catalog: game/catalog/ rebuilt from the game's catalog %s by scripts/catalog-index.py" % cat.get("version"), "--", FOLDER)
        if code != 0:
            git(args.root, "reset", "-q", "--", FOLDER)
            git(args.root, "checkout", "--", FOLDER)
            git(args.root, "clean", "-fdq", "--", FOLDER)
            print("HALT: the commit failed; the folder was put back: " + out.strip()[-200:])
            return 1
        print("%s: committed" % FOLDER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
