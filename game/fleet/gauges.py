#!/usr/bin/env python3
"""gauges.py -- what a ship or a side of ours can hunt: its firepower and its toughness against a creature (rule F9).

WHAT: rule F9 (governance/rulebook.md, section 12) judges a hunt by two gauges of the side that flies it, one ship
      or a group (a game fleet, DECISIONS D228); a creature must pass both:
        firepower   the sum over the side's armed ships of each weapon's damage per tick (the catalog's `damage`
                    over its `cooldown` in ticks), raised 1% per level of the pilot's Gunnery, 1% per level of
                    its Weapons and 1% per level of Tactics. The side kills a creature of up to KILL_FACTOR times
                    its firepower in hull.
        toughness   the sum of the side's ships' hull and shield as the game reports them (max_hull and
                    max_shield of the ship files). The side stands a creature that weighs up to STAND_SHARE of
                    it: a creature weighs its hull, a predator PREDATOR_WEIGHT times its hull.
      It reads the ship files (data/fleet/ships/, the ships fleet.json lists), the newest catalog (data/catalog/)
      and the herd readings (data/wildlife/): a species' hull is the highest max_hull any reading saw. A role's
      typical ship has the median firepower and the median toughness of the role's ships; with no ship of the
      role on file, of the whole fleet; with no ship on file at all, STARTER. The smallest group of a role is
      the fewest typical ships that pass both gauges together. The route maker (routemaker.py) asks it which
      herds one ship may hunt and which wait for a group.
RULES:
  - It reads only: it moves no ship and writes no file.
  - Within both gauges a side hunts a species freely; above either the hunt is a test (rule F9). A species that
    more than GROUP_MAX typical ships would need is out of reach: no group.
  - A creature whose hull no reading holds passes nothing; a weapon the catalog does not know adds nothing.
WHY:  a fixed limit of 100 hull judged a starter and a fitted warship alike, and a group not at all. Suggi,
      2026-11-17: "if we can kill it, it is fine"; "not just hull and shield but also weapons firepower ... both
      are important; ship level also".

USAGE:
  gauges.py ship <pilot>...             each ship: its weapons, skills, firepower and toughness, what it kills and stands
  gauges.py side <pilot>...             the pilots as one side: its gauges and the species of our readings it passes
  gauges.py species [--role <role>]     every species seen: hull, weight, whether one typical ship of the role passes
                                        both gauges, the smallest group that does (default: drone, the hunting role;
                                        `--role all`: the whole fleet's typical ship)
  --data <dir>                          the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import json
import os
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the data folder, a pilot's role

# Rule F9 (governance/rulebook.md, section 12, 2026-11-17). The 7 and the half rest on our runs to that day: a starter
# with one Pulse Laser I (about 11 damage a tick with its skills; hull 75, shield up to 130) killed grazers of up to
# 70 hull in over 1,300 runs, never below 76% hull, and killed nothing of 90 to 120 hull in 9 runs.
KILL_FACTOR = 7              # rule F9: a side kills a creature of up to 7 x its firepower in hull
STAND_SHARE = 0.5            # rule F9: a side stands a creature that weighs up to half its toughness
PREDATOR_WEIGHT = 2          # rule F9: a predator weighs twice its hull (it fights to the death; a starting weight, not measured)
SKILLS = ("gunnery", "weapons", "tactics")       # rule F9: each raises firepower 1% a level
SKILL_STEP = 0.01
GROUP_MAX = 20               # the largest group asked for; a species beyond it is out of reach
HUNTER = "drone"             # the hunting role (routemaker.py ROLE["hunt"]): the default of `species`
# Where no ship file is on record: the fit every ship of ours was born with (the ship files of 2026-11-17: 246
# Threshold hulls of 75 hull and 80 shield, one Pulse Laser I each, 10 damage a tick by catalog 0.723.2), no skill.
STARTER = {"firepower": 10.0, "toughness": 75 + 80}


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def num(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else 0


# ---------------------------------------------------------------- what is read

def newest_catalog(data):
    """The newest catalog in data/catalog/: the highest version in a file name of digits and dots (routemaker.py's
    and craftbook.py's rule)."""
    folder = Path(data) / "catalog"
    files = [p for p in folder.glob("*.json") if re.fullmatch(r"\d+(\.\d+)*", p.stem)] if folder.is_dir() else []
    return max(files, key=lambda p: tuple(int(n) for n in p.stem.split("."))) if files else folder / "none.json"


def load_items(data):
    """{item id: item} of the newest catalog."""
    items = read_json(newest_catalog(data), {}).get("items") or []
    return {i["id"]: i for i in (items.values() if isinstance(items, dict) else items) if isinstance(i, dict) and i.get("id")}


def load_ships(data):
    """{pilot: its live file} of every ship fleet.json lists (of every file when it lists none)."""
    fleet = read_json(Path(data) / "fleet" / "fleet.json", {})
    listed = {s.get("name") for s in (fleet.get("ships") or [] if isinstance(fleet, dict) else []) if isinstance(s, dict) and s.get("name")}
    folder, out = Path(data) / "fleet" / "ships", {}
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        ship = read_json(path, None)
        if isinstance(ship, dict) and ship.get("name") and (not listed or ship["name"] in listed):
            out[ship["name"]] = ship
    return out


def read_creatures(data):
    """Every creature of every herd reading (data/wildlife/<system>.json), as the readers wrote it."""
    folder, out = Path(data) / "wildlife", []
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        wild = read_json(path, {})
        for entry in (wild.get("pois") or {}).values() if isinstance(wild, dict) and isinstance(wild.get("pois"), dict) else []:
            out.extend(c for c in (entry.get("creatures") or [] if isinstance(entry, dict) else []) if isinstance(c, dict) and c.get("species"))
    return out


def species_table(creatures):
    """{species: {hull, role, weight, seen}}: the highest hull any reading saw, the role (predator when any reading
    says so), the weight rule F9 gives it, and how many creatures were read."""
    seen = {}
    for c in creatures:
        if not isinstance(c, dict) or not c.get("species"):
            continue
        row = seen.setdefault(c["species"], {"hull": 0, "roles": Counter(), "seen": 0})
        row["hull"] = max(row["hull"], num(c.get("max_hull")), num(c.get("hull")))
        row["roles"][str(c.get("role") or "")] += 1
        row["seen"] += 1
    out = {}
    for species, row in seen.items():
        role = "predator" if row["roles"]["predator"] else row["roles"].most_common(1)[0][0]
        out[species] = {"hull": row["hull"], "role": role, "weight": row["hull"] * (PREDATOR_WEIGHT if role == "predator" else 1), "seen": row["seen"]}
    return out


def read(data=division.DATA, items=None, creatures=None):
    """The readings every gauge rests on, read once: ships, catalog items, species (`items` and `creatures` when the
    caller has read them already). Pass it as `book` to the other functions."""
    ships = load_ships(data)
    return {"data": str(data), "ships": ships, "roles": {name: division.role_of(name, data) for name in ships},
            "items": load_items(data) if items is None else items,
            "species": species_table(read_creatures(data) if creatures is None else creatures), "typical": {}}


# ---------------------------------------------------------------- the gauges

def weapons_of(ship, items):
    """[(module id, damage a tick)] of a ship's weapons: the catalog's damage over its cooldown; 0 where the catalog
    does not know the module."""
    out = []
    for module in ship.get("modules") or []:
        if isinstance(module, dict) and (module.get("kind") == "weapon" or module.get("slot") == "weapon"):
            name = str(module.get("type") or module.get("id") or "?")
            item = items.get(name) or {}
            damage = num(item.get("damage"))
            out.append((name, damage / max(1, num(item.get("cooldown")) or 1) if damage > 0 else 0.0))
    return out


def skill_levels(ship):
    """{skill: level} of the skills that raise firepower (SKILLS)."""
    skills = ship.get("skills") or {}
    level = lambda entry: num(entry.get("level")) if isinstance(entry, dict) else num(entry)
    return {name: level(skills.get(name)) for name in SKILLS} if isinstance(skills, dict) else {name: 0 for name in SKILLS}


def gauges_of(ship, items):
    """{firepower, toughness, weapons, bonus, hull, shield} of one ship's live file."""
    guns, levels = weapons_of(ship, items), skill_levels(ship)
    bonus = SKILL_STEP * sum(levels.values())
    hull, shield = num(ship.get("max_hull")), num(ship.get("max_shield"))
    return {"firepower": sum(d for _w, d in guns) * (1 + bonus), "toughness": hull + shield, "weapons": guns, "levels": levels,
            "bonus": bonus, "hull": hull, "shield": shield}


def book_of(book, data):
    return book if book is not None else read(data)


def ship_gauges(pilot, data=division.DATA, book=None):
    """(firepower, toughness) of one pilot's ship; None when no live file of it is on record."""
    book = book_of(book, data)
    ship = book["ships"].get(pilot)
    if ship is None:
        return None
    found = gauges_of(ship, book["items"])
    return found["firepower"], found["toughness"]


def side_gauges(pilots, data=division.DATA, book=None):
    """(firepower, toughness) of the pilots as one side: the sums over the ships on record (unknown pilots add nothing)."""
    book = book_of(book, data)
    found = [ship_gauges(p, book=book) for p in pilots]
    return sum(f[0] for f in found if f), sum(f[1] for f in found if f)


def creature(species, data=division.DATA, book=None):
    """(hull, weight) of a species by our readings: the highest max_hull seen, a predator weighing PREDATOR_WEIGHT
    times it; None when no reading saw the species or its hull."""
    row = book_of(book, data)["species"].get(species)
    return (row["hull"], row["weight"]) if row and row["hull"] > 0 else None


def fits(gauge, hull, weight):
    """(ok_firepower, ok_toughness) of a side's (firepower, toughness) against a creature's hull and weight."""
    firepower, toughness = gauge
    return hull <= KILL_FACTOR * firepower, weight <= STAND_SHARE * toughness


def passes(side, species, data=division.DATA, book=None):
    """(ok_firepower, ok_toughness) of a side against a species: `side` is (firepower, toughness), a pilot or a list
    of pilots. A species whose hull no reading holds passes nothing."""
    book = book_of(book, data)
    if isinstance(side, str):
        side = [side]
    gauge = side if isinstance(side, tuple) else side_gauges(side, book=book)
    found = creature(species, book=book)
    return fits(gauge, *found) if found else (False, False)


def typical(role, data=division.DATA, book=None):
    """(firepower, toughness, what it rests on) of one typical ship of a role ('' or 'all': the whole fleet): the
    median of each gauge over the role's ships on file; with none of the role, of the fleet's; with none, STARTER."""
    book = book_of(book, data)
    role = "" if role in ("", "all", None) else role
    if role not in book["typical"]:
        rows = [gauges_of(ship, book["items"]) for name, ship in sorted(book["ships"].items()) if not role or book["roles"].get(name) == role]
        label = "median of %d %s ship(s)" % (len(rows), role or "fleet")
        if not rows and book["ships"]:
            rows = [gauges_of(ship, book["items"]) for _name, ship in sorted(book["ships"].items())]
            label = "no %s ship on file: median of the fleet's %d ship(s)" % (role, len(rows))
        if rows:
            book["typical"][role] = (statistics.median(r["firepower"] for r in rows), statistics.median(r["toughness"] for r in rows), label)
        else:
            book["typical"][role] = (STARTER["firepower"], STARTER["toughness"], "no ship on file: a starter (one Pulse Laser I, hull 75, shield 80, no skill)")
    return book["typical"][role]


def group_needed(gauge, hull, weight, max_n=GROUP_MAX):
    """The fewest ships of one ship's (firepower, toughness) that pass both gauges together (1: one ship alone), or
    None: more than `max_n`, or a gauge of nothing."""
    for n in range(1, max_n + 1):
        if all(fits((n * gauge[0], n * gauge[1]), hull, weight)):
            return n
    return None


def smallest_group(role, species, max_n=GROUP_MAX, data=division.DATA, book=None):
    """The fewest typical ships of a role that pass both gauges for a species (1: one alone), or None: out of reach of
    `max_n` ships, or a species whose hull no reading holds."""
    book = book_of(book, data)
    found = creature(species, book=book)
    if not found:
        return None
    firepower, toughness, _label = typical(role, book=book)
    return group_needed((firepower, toughness), found[0], found[1], max_n)


# ---------------------------------------------------------------- the command line

def limits(gauge):
    return "firepower %.1f: kills up to %.1f hull | toughness %g: stands up to %g weight" % (gauge[0], KILL_FACTOR * gauge[0], gauge[1], STAND_SHARE * gauge[1])


def names_in(words, known):
    """([pilots], [words that name none]): a pilot's name may hold spaces (a flagship), so the longest run of words that
    names a pilot wins."""
    found, unknown, n = [], [], 0
    while n < len(words):
        for end in range(len(words), n, -1):
            name = " ".join(words[n:end])
            if name in known:
                found.append(name)
                n = end
                break
        else:
            unknown.append(words[n])
            n += 1
    return found, unknown


def why_not(ok):
    return "passes" if all(ok) else "fails " + " and ".join(name for name, good in zip(("firepower", "toughness"), ok) if not good)


def show_ships(book, pilots):
    print("GAUGES | rule F9: a side kills a creature of up to %d x its firepower in hull and stands one that weighs up to %g of its toughness "
          "(a predator weighs %d x its hull) | %d ship file(s)" % (KILL_FACTOR, STAND_SHARE, PREDATOR_WEIGHT, len(book["ships"])))
    for pilot in pilots:
        g = gauges_of(book["ships"][pilot], book["items"])
        guns = ", ".join("%s %g a tick" % (w, round(d, 2)) if d else "%s (not in the catalog)" % w for w, d in g["weapons"]) or "no weapon"
        skills = ", ".join("%s %d" % (k, v) for k, v in g["levels"].items())
        print("  %s (%s) | %s | %s: +%d%% | hull %g + shield %g | %s" % (pilot, book["roles"].get(pilot) or "-", guns, skills, round(100 * g["bonus"]),
                                                                  g["hull"], g["shield"], limits((g["firepower"], g["toughness"]))))


def show_side(book, pilots):
    gauge = side_gauges(pilots, book=book)
    print("SIDE of %d ship(s): %s | %s" % (len(pilots), ", ".join(pilots), limits(gauge)))
    rows = sorted(book["species"].items(), key=lambda kv: (kv[1]["weight"], kv[1]["hull"], kv[0]))
    judged = [(s, row, fits(gauge, row["hull"], row["weight"]) if row["hull"] > 0 else (False, False)) for s, row in rows]
    good = [s for s, _row, ok in judged if all(ok)]
    print("  passes %d of the %d species of our readings: %s" % (len(good), len(rows), ", ".join(good) or "none"))
    for label, test in (("fails firepower", lambda ok: not ok[0]), ("fails toughness", lambda ok: not ok[1])):
        bad = ["%s %g" % (s, row["hull"]) for s, row, ok in judged if test(ok)]
        if bad:
            print("  %s (%d): %s" % (label, len(bad), ", ".join(bad)))


def show_species(book, role):
    role = "" if role in ("", "all") else role
    gauge = typical(role, book=book)
    print("SPECIES | rule F9 | one typical %s ship (%s): %s | groups of up to %d" % (role or "fleet", gauge[2], limits(gauge), GROUP_MAX))
    print("  %-22s %-10s %6s %7s  %-28s %s" % ("species", "role", "hull", "weight", "one ship", "smallest group"))
    for species, row in sorted(book["species"].items(), key=lambda kv: (kv[1]["weight"], kv[1]["hull"], kv[0])):
        ok = fits(gauge[:2], row["hull"], row["weight"]) if row["hull"] > 0 else (False, False)
        n = smallest_group(role, species, book=book)
        size = "no hull on record" if row["hull"] <= 0 else ("none of %d or fewer" % GROUP_MAX if n is None else str(n))
        print("  %-22s %-10s %6g %7g  %-28s %s" % (species[:22], row["role"][:10], row["hull"], row["weight"], why_not(ok), size))


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--data", "--role", "--root"))]
    if not words or any(a in ("-h", "--help") for a in args) or words[0] not in ("ship", "side", "species"):
        sys.exit(__doc__)
    book = read(value("--data", division.DATA))
    if words[0] == "species":
        show_species(book, value("--role", HUNTER))
        return 0
    pilots, unknown = names_in(words[1:], book["ships"])
    if pilots and words[0] == "ship":
        show_ships(book, pilots)
    elif pilots:
        show_side(book, pilots)
    for word in unknown:
        print("  `%s`: no ship file of that name (data/fleet/ships/)" % word)
    return 0 if pilots and not unknown else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
