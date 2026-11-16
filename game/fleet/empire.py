#!/usr/bin/env python3
"""empire.py -- keep the picture of our empire: the faction and its limit, the bases and offices we own, the systems they stand in, the sites we may build on, and what the faction can build next.

WHAT: four verbs.
        collect   looks through the engine's gate with the leader's flagship, views only: the faction's `info` and
                  tax estimate, every facility and ship garage the faction owns with its rent, and, once per release
                  of the game's catalog, the game's own card of each faction facility type (what the catalog lacks:
                  its rent per cycle). It joins the public list of stations and outposts (the command station's
                  data: every base with its owner's tag), the chart, and the sites file, and writes
                  <data>/empire/empire.json: faction, members, bases, facilities, territory, sites, ladder.
        write     writes governance/empire.md from that file: the faction in figures, the bases and the territory,
                  the offices and their rent, the sites, and the ladder of what the faction can build
        show      prints the same in plain lines (hive.py empire)
        check     governance/empire.md is what `write` would write
RULES:
  - Views only: it founds, builds, pays and changes nothing. A call that is no view is refused here, before the gate.
  - The repository file names no pilot of ours and holds no balance: the members by name and the treasury are in
    the data file only (the repository is public; rulebook section 10).
  - Territory is what the game's own lists show: a system with a station or an outpost that carries our tag, or with
    an office of ours at somebody else's station. Nothing is claimed by hand.
  - A site is a line of game/map/sites.tsv, kept by hand by the Fleet Admiral (Intel proposes); the script adds what
    the chart and the public list of stations say about its system. Where a base is built is Suggi's decision.
  - A fact no reading holds is written `not read`, never filled in. The file is rewritten only when a fact changed.
WHY:  what we own and where stood in no file: the faction's limit was read by hand, the rent of an office was "not
      read yet" in an order, and a plan for a base had no list of what stands already (Suggi, 2026-11-16: "we need
      to have scripts also where our bases and territories are, so we know our empire").

USAGE:
  empire.py collect [--ladder]     one reading, written to <data>/empire/empire.json (--ladder: read the cards again)
  empire.py write [--commit]       governance/empire.md from the data file; --commit commits it by path as Unity
  empire.py show
  empire.py check
  --root <dir>   the repository's root (default: two folders above this file)
  --data <dir>   the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  who may run a collect; the leader's flagship

GATE = "http://172.30.0.32:7580"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
VIEWS = {("spacemolt_faction", "info"), ("spacemolt_faction", "tax_estimate"), ("spacemolt_faction", "garages"),
         ("spacemolt_facility", "faction_owned"), ("spacemolt_facility", "types")}       # the only calls this script sends: each reads
FILE = "governance/empire.md"
SITES = "game/map/sites.tsv"
ID = "20261116T192710Z"                           # the file's id: it stays when the file is rewritten
CYCLES_A_DAY = 86.4                               # rent is due every 100 ticks of about 10 s (game/rules/07-economy.md)
STATIONS, OUTPOSTS = 5, 8                         # bases a faction may hold (game/rules/09-factions.md)
GIVES = {"faction_recruitment": "members", "faction_storage": "units per item type", "faction_storage_extension": "units per item type in a named bucket",
         "faction_market": "open faction orders", "faction_company_store": "members-only listings", "faction_missions": "posted missions",
         "faction_commons": "rooms", "faction_ship_garage": "shared ships", "faction_transit": "connecting passengers"}      # what a line's `faction_cap` counts


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def now_text(now=None):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))


def ascii_text(value, cap=200):
    """A name or a note from the game for an ASCII file: what is no ASCII becomes `?`."""
    return str(value if value is not None else "").encode("ascii", "replace").decode("ascii").replace("|", "/").replace("\n", " ").strip()[:cap]


def look(pilot, group, action, params=None):
    """One view through the gate: (the answer's content, '') or (None, why not)."""
    if (group, action) not in VIEWS:
        return None, "refused: `%s %s` is no view of this script" % (group, action)
    body = {"toolGroup": group, "action": action, "params": params or {}}
    request = urllib.request.Request(GATE + "/accounts/%s/raw" % urllib.parse.quote(pilot, safe=""), data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with OPENER.open(request, timeout=90) as answer:
            found = json.loads(answer.read().decode("utf-8", "replace") or "{}")
    except (urllib.error.URLError, OSError, ValueError) as error:
        return None, "%s: %s" % (type(error).__name__, str(error)[:120])
    content = found.get("structuredContent") if isinstance(found, dict) else None
    if not isinstance(content, dict) or content.get("error"):
        return None, ascii_text((content or {}).get("error") or (found.get("error") if isinstance(found, dict) else found), 200)
    return content, ""


def leader(data):
    """The flagship the Fleet Admiral flies: the faction's leader."""
    return next((name for name, entry in division.flagships(data).items() if isinstance(entry, dict) and entry.get("of") == "Unity"), "")


def chart(data, root):
    """{system id: {name, empire ('' = lawless), jumps from home}} from the station's copy of the public map, else the repository's chart."""
    rows = (read_json(Path(data) / "station" / "map.json", {}) or {}).get("systems") or []
    out = {str(s.get("id")): {"name": ascii_text(s.get("name"), 60), "empire": str(s.get("empire") or ""), "jumps": s.get("jumps")} for s in rows if isinstance(s, dict) and s.get("id")}
    if out:
        return out
    try:
        lines = (Path(root) / "game" / "map" / "galaxy.tsv").read_text(encoding="utf-8").splitlines()
    except OSError:
        return {}
    for line in lines:
        cells = line.split("\t")
        if line.startswith("#") or len(cells) < 7 or cells[0] == "id":
            continue
        out[cells[0]] = {"name": ascii_text(cells[1], 60), "empire": "" if cells[4] == "-" else cells[4], "jumps": int(cells[6]) if cells[6].lstrip("-").isdigit() else None}
    return out


def site_rows(root):
    """The lines of game/map/sites.tsv: system, poi, status, proposed_by, note."""
    try:
        lines = (Path(root) / SITES).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.split("\t")]
        if not line.strip() or line.startswith("#") or cells[0] == "system":
            continue
        cells += [""] * (5 - len(cells))
        rows.append({"system": cells[0], "poi": cells[1] if cells[1] != "-" else "", "status": cells[2] or "candidate", "proposed_by": cells[3], "note": ascii_text(cells[4], 300)})
    return rows


def catalog(data):
    """(version, the faction's facility types) of the newest catalog on disk."""
    files = [p for p in (Path(data) / "catalog").glob("*.json") if re.fullmatch(r"\d+(\.\d+)*", p.stem)]
    if not files:
        return "", []
    raw = read_json(max(files, key=lambda p: tuple(int(n) for n in p.stem.split("."))), {})
    return str(raw.get("version") or ""), [f for f in raw.get("facilities") or [] if isinstance(f, dict) and f.get("category") == "faction" and f.get("id")]


def ladder(data, pilot, see, old, force, pause):
    """What the faction can build, line by line and tier by tier: the catalog's rows with the rent of the game's own
    card. The cards are read once per release of the catalog (or with --ladder); a card not read leaves its rent None."""
    version, types = catalog(data)
    if not types:
        return old.get("ladder") or [], old.get("ladder_of") or ""
    kept = {r.get("type"): r for r in old.get("ladder") or [] if isinstance(r, dict)}
    again = force or old.get("ladder_of") != version or any(kept.get(t["id"], {}).get("rent_per_cycle") is None for t in types)
    rows = []
    for t in types:
        card = {}
        if again and pilot:
            card, _why = see(pilot, "spacemolt_facility", "types", {"facility_type": t["id"]})
            card = card or {}
            time.sleep(pause)
        before = kept.get(t["id"], {})
        rent = card.get("rent_per_cycle") if isinstance(card.get("rent_per_cycle"), (int, float)) else before.get("rent_per_cycle")
        rows.append({"type": t["id"], "name": ascii_text(t.get("name"), 60), "line": str(t.get("faction_service_type") or ""), "level": t.get("level") or 1,
                     "cost": t.get("build_cost") or 0, "rent_per_cycle": rent, "build_time": t.get("build_time"), "cap": t.get("faction_cap"),
                     "materials": [{"item": str(m.get("item_id")), "units": int(m.get("quantity") or 0)} for m in t.get("build_materials") or [] if isinstance(m, dict)],
                     "upgrades_from": str(t.get("upgrades_from") or ""), "requires": str(t.get("requires_service_type") or "")})
    rows.sort(key=lambda r: (r["line"] != "faction_storage", r["line"] != "faction_recruitment", r["line"], r["level"], r["type"]))      # storage first: every other line needs it
    return rows, version


def collect(data, root, see=look, force=False, pause=0.5, now=None):
    """One reading of the empire; (the state, the lines to print). The state is what <data>/empire/empire.json holds."""
    old = read_json(Path(data) / "empire" / "empire.json", {})
    notes, pilot = [], leader(data)
    if not pilot:
        notes.append("no flagship of the Fleet Admiral in fleet/flagships.json: the faction was not read")
    info, why = see(pilot, "spacemolt_faction", "info") if pilot else (None, "no leader")
    if info is None:
        notes.append("faction info not read (%s): the last reading stays" % why)
    faction = dict(old.get("faction") or {})
    members = old.get("members") or []
    if info is not None:
        money = next((info[k] for k in ("treasury", "treasury_credits", "treasury_balance", "credits") if isinstance(info.get(k), (int, float))), None)
        faction = {"id": str(info.get("id") or ""), "name": ascii_text(info.get("name"), 60), "tag": ascii_text(info.get("tag"), 8), "leader": ascii_text(info.get("leader_username"), 40),
                   "member_count": info.get("member_count"), "members_limit": info.get("members_limit"), "treasury": money, "owned_bases": info.get("owned_bases"),
                   "at_war": bool(info.get("at_war")), "created_at": str(info.get("created_at") or "")}
        members = [{"pilot": ascii_text(m.get("username"), 40), "role": ascii_text(m.get("role"), 20)} for m in info.get("members") or [] if isinstance(m, dict) and m.get("username")]
    tag = faction.get("tag") or ""
    systems = chart(data, root)
    public = [s for s in read_json(Path(data) / "station" / "stations.json", []) or [] if isinstance(s, dict)]
    bases = [{"base": ascii_text(s.get("name"), 60), "name": ascii_text(s.get("name"), 60), "system": str(s.get("system") or ""), "poi": "",
              "kind": "outpost" if s.get("type") == "outpost" else "station", "condition": ascii_text(s.get("condition"), 20), "services": [ascii_text(x, 30) for x in s.get("services") or []][:20]}
             for s in public if tag and s.get("tag") == tag]
    if info is not None and isinstance(faction.get("owned_bases"), int) and faction["owned_bases"] != len(bases):
        notes.append("the game counts %d base(s) of ours, the public list of stations shows %d: the list is fetched every 15 minutes" % (faction["owned_bases"], len(bases)))
    owned, why = see(pilot, "spacemolt_facility", "faction_owned") if pilot else (None, "no leader")
    facilities, rent = old.get("facilities") or [], old.get("rent") or {}
    if owned is None:
        notes.append("the faction's facilities not read (%s): the last reading stays" % why)
    else:
        pick = lambda row, *keys: next((row[k] for k in keys if row.get(k) not in (None, "")), "")
        facilities = [{"facility_id": str(pick(f, "facility_id", "id")), "type": str(pick(f, "type_id", "facility_type", "type")), "name": ascii_text(pick(f, "name"), 60),
                       "level": pick(f, "level") or 1, "base": ascii_text(pick(f, "base_id", "station_id", "base_name", "station_name", "base"), 60),
                       "system": str(pick(f, "system_id", "system")), "status": ascii_text(pick(f, "status", "state") or "active", 30),
                       "rent_per_cycle": f.get("rent_per_cycle") if isinstance(f.get("rent_per_cycle"), (int, float)) else None}
                      for f in owned.get("facilities") or [] if isinstance(f, dict)]
        bill = owned.get("faction_rent") or {}
        rent = {"facilities": bill.get("facilities"), "per_cycle": bill.get("total_rent_per_cycle"), "per_day": bill.get("est_rent_per_day"), "arrears": bill.get("arrears")}
    garages, _why = see(pilot, "spacemolt_faction", "garages") if pilot else (None, "")
    tax, _why = see(pilot, "spacemolt_faction", "tax_estimate") if pilot else (None, "")
    territory, seen = [], set()
    for base in bases:
        if base["system"] and (base["system"], base["kind"]) not in seen:
            seen.add((base["system"], base["kind"]))
            territory.append({"system": base["system"], "claim": base["kind"], "note": base["name"]})
    ours = {b["name"] for b in bases}
    for f in facilities:
        if f["system"] and f["base"] not in ours and (f["system"], "office") not in seen:
            seen.add((f["system"], "office"))
            territory.append({"system": f["system"], "claim": "office", "note": "at %s" % f["base"]})
    sites = []
    for row in site_rows(root):
        known = systems.get(row["system"])
        there = ["%s (%s%s)" % (ascii_text(s.get("name"), 60), s.get("type") or "station", ", " + ascii_text(s.get("tag"), 8) if s.get("tag") else "") for s in public if s.get("system") == row["system"]]
        sites.append(dict(row, name=known["name"] if known else "", space=("not on the chart" if not known else known["empire"] or "lawless"), jumps=known["jumps"] if known else None, stations=there))
    feed = ((read_json(Path(data) / "station" / "feed.json", {}) or {}).get("factions") or {}).get(tag) or {}
    ships = [s for s in (read_json(Path(data) / "fleet" / "fleet.json", {}) or {}).get("ships") or [] if isinstance(s, dict) and s.get("name")]
    rungs, version = ladder(data, pilot, see, old, force, pause)
    state = {"written_at": now_text(now), "faction": faction, "members": members, "bases": bases, "facilities": facilities, "territory": territory, "sites": sites,
             "rent": rent, "garages": {"stations": (garages or {}).get("station_count"), "ships": (garages or {}).get("total_ships")} if garages is not None else old.get("garages") or {},
             "tax": {k: (tax or {}).get(k) for k in ("domicile", "net_taxable_profit", "income_tax_total", "tax_prepaid")} if tax is not None else old.get("tax") or {},
             "relations": {"allies": [ascii_text(x, 30) for x in feed.get("allies") or []], "enemies": [ascii_text(x, 30) for x in feed.get("enemies") or []],
                           "wars": [ascii_text(x, 30) for x in feed.get("wars") or []]},
             "fleet": {"ships": len(ships), "in_faction": len({m["pilot"] for m in members} & {s["name"] for s in ships})},
             "ladder": rungs, "ladder_of": version, "notes": notes}
    return state, notes


def save(data, state):
    path = Path(data) / "empire" / "empire.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name("%s.%d.tmp" % (path.name, os.getpid()))
    tmp.write_text(json.dumps(state, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, path)


def num(value, unit=""):
    return "not read" if not isinstance(value, (int, float)) else "{:,}".format(int(round(value))) + unit


def table(head, rows):
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]


def facts(state):
    """The empire in rows, one list for the page and for `show`: (faction rows, base rows, office rows, site rows, ladder rows)."""
    f, fleet, rel = state.get("faction") or {}, state.get("fleet") or {}, state.get("relations") or {}
    bases, rent = state.get("bases") or [], state.get("rent") or {}
    stations = sum(1 for b in bases if b.get("kind") == "station")
    listed = lambda names: ", ".join(names) if names else "none"
    faction = [("Name and tag", "%s [%s]" % (f.get("name") or "not read", f.get("tag") or "?")), ("Founded", (f.get("created_at") or "not read")[:10]),
               ("Leader", "the Fleet Admiral's flagship"),
               ("Members", "%s of a limit of %s" % (num(f.get("member_count")), num(f.get("members_limit")))),
               ("Ships of the fleet in it", "%s of %s" % (num(fleet.get("in_faction")), num(fleet.get("ships")))),
               ("Stations of our own", "%d of %d a faction may hold" % (stations, STATIONS)), ("Outposts", "%d of %d" % (len(bases) - stations, OUTPOSTS)),
               ("Offices at stations", "%d, rent %s cr per cycle (%s cr a day)" % (len(state.get("facilities") or []), num(rent.get("per_cycle")), num(rent.get("per_day")))),
               ("Shared ships in garages", num((state.get("garages") or {}).get("ships"))),
               ("At war", "yes" if f.get("at_war") else "no"), ("Allies", listed(rel.get("allies"))), ("Marked enemies", listed(rel.get("enemies")))]
    base_rows = [[b.get("name"), b.get("kind"), "`%s`" % b.get("system"), b.get("condition") or "--", ", ".join(b.get("services") or []) or "--"] for b in bases]
    office_rows = [[o.get("name") or o.get("type"), o.get("level"), o.get("base") or "--", "`%s`" % o.get("system") if o.get("system") else "--", o.get("status"), num(o.get("rent_per_cycle"))]
                   for o in state.get("facilities") or []]
    site_rows_ = [["`%s`" % s.get("system"), s.get("name") or "--", s.get("space"), num(s.get("jumps")), ", ".join(s.get("stations") or []) or "none",
                   s.get("status"), s.get("proposed_by") or "--", s.get("note") or "--"] for s in state.get("sites") or []]
    rungs = []
    for r in state.get("ladder") or []:
        gives = "%s %s" % (num(r.get("cap")), GIVES.get(r.get("line"), "")) if isinstance(r.get("cap"), (int, float)) else "--"
        rungs.append([r.get("line") or "--", r.get("level"), "%s (`%s`)" % (r.get("name"), r.get("type")), num(r.get("cost")),
                      ", ".join("%s %s" % ("{:,}".format(m["units"]), m["item"]) for m in r.get("materials") or []) or "--",
                      num(r.get("rent_per_cycle")), num(r["rent_per_cycle"] * CYCLES_A_DAY) if isinstance(r.get("rent_per_cycle"), (int, float)) else "not read", gives.strip()])
    return faction, base_rows, office_rows, site_rows_, rungs


def page(state):
    """governance/empire.md as text."""
    faction, bases, offices, sites, rungs = facts(state)
    territory = state.get("territory") or []
    lines = ["---", "name: empire", "id: %s" % ID, "tier: map", "author: Unity", "status: written by game/fleet/empire.py; never edited by hand",
             "links: [governance/map.md, game/rules/09-factions.md, game/map/sites.tsv, game/catalog/facilities.md, governance/strategy.md]", "---", "",
             "# empire.md -- What The Collective Holds", "",
             "Our empire in one file: the faction, its bases, its offices at other", "stations, the systems they stand in, the sites we may build on, and what",
             "the faction can build next. Written by `python3 -I -B game/fleet/empire.py", "write` from what the game itself answers; never edited by hand. The map",
             "around it is `governance/map.md`.", "",
             "Not in this file, and not in the repository: where our ships are, what", "they store, the members by name and the treasury's balance. They are live",
             "data of the unit (the tools `hive` with `verb=empire`, `stock`, `ship`;", "`game/fleet/empire.py show`).", "",
             "Facts as of %s." % (state.get("written_at") or "not read"), "",
             "## 1. The Faction", ""] + table(["Fact", "Now"], faction) + ["",
             "The member limit is set by recruitment offices (section 5): the best", "station's office counts in full, each other station's office adds a quarter",
             "of its own limit.", "", "## 2. Bases and Territory", ""]
    lines += (table(["Base", "Kind", "System", "Condition", "Services"], bases) if bases else ["We hold no station and no outpost yet."]) + [""]
    lines += (["Systems we hold something in:", ""] + table(["System", "What", "Note"], [["`%s`" % t["system"], t["claim"], t["note"]] for t in territory])
              if territory else ["Territory: none. A system counts when a station or an outpost there", "carries our tag, or when an office of ours stands at a station there."])
    lines += ["", "What founding a base takes: `game/rules/09-factions.md` (fees and limits)", "and the tool `base_plan` (every part down to the ore, against what we",
              "hold).", "", "## 3. Offices at Other Stations", ""]
    lines += (table(["Office", "Tier", "Station", "System", "State", "Rent per cycle"], offices) if offices else ["None yet. The first one at a station is the Faction Lockbox: every other", "office there needs it."])
    lines += ["", "## 4. Sites", "", "Places proposed for a base of ours, from `game/map/sites.tsv`; the columns", "Space, Jumps and Stations there are read from the chart and the public",
              "list of stations. Where a base is built is Suggi's decision.", ""]
    lines += table(["System", "Name", "Space", "Jumps from home", "Stations there", "Status", "Proposed by", "Note"], sites) if sites else ["No site is proposed."]
    lines += ["", "## 5. What The Faction Can Build", "",
              "Every faction facility of the game's catalog (%s), line by line and" % (state.get("ladder_of") or "not read"), "tier by tier. A higher tier is an upgrade of the one before it and",
              "replaces its rent. Rent is due every 100 ticks (about 17 minutes) at a", "station that is not ours; at our own station or outpost it is none. The",
              "rent is the game's own card for the type (`facility types`), the day is", "86.4 cycles. Every line but the first needs faction storage at the same",
              "station. What a thing takes down to the ore: the tool `catalog` with", "`ask=build`.", ""]
    lines += table(["Line", "Tier", "Facility", "Credits", "Materials", "Rent per cycle", "Rent per day", "Gives"], rungs) if rungs else ["Not read: no catalog on disk."]
    lines += ["", "## 6. Keeping This File", "",
              "| Task | How |", "|---|---|", "| Read the empire again | `python3 -I -B game/fleet/empire.py collect` (the Fleet Admiral's hourly job; views only) |",
              "| Write this file | `python3 -I -B game/fleet/empire.py write --commit` (rewritten only when a fact changed) |",
              "| Ask it | the tool `hive` with `verb=empire`; in the history store the tables `faction`, `bases`, `faction_facilities`, `territory`, `sites` |",
              "| Propose a site | a line in `game/map/sites.tsv`: system, place, status, who proposes, note |", ""]
    text = "\n".join(lines)
    return text.encode("ascii", "replace").decode("ascii")


def body(text):
    """A page without its line of the reading's time: two pages with the same facts are the same page."""
    return "\n".join(line for line in text.splitlines() if not line.startswith("Facts as of "))


def show(data):
    state = read_json(Path(data) / "empire" / "empire.json", {})
    if not state:
        print("EMPIRE | not read yet: `empire.py collect` writes %s" % (Path(data) / "empire" / "empire.json"))
        return 1
    faction, bases, offices, sites, rungs = facts(state)
    f = state.get("faction") or {}
    print("EMPIRE | what The Collective holds | read from the game %s | the file: %s" % (state.get("written_at"), FILE))
    for key, value in faction:
        print("  %-26s %s" % (key, value))
    print("  %-26s %s" % ("Treasury", num(f.get("treasury"), " cr") if isinstance(f.get("treasury"), (int, float)) else "no balance in the game's answer (it shows none while the treasury is empty)"))
    print("BASES | %d" % len(bases))
    for row in bases:
        print("  %s (%s) in %s, %s" % (row[0], row[1], row[2].strip("`"), row[3]))
    print("OFFICES | %d" % len(offices))
    for row in offices:
        print("  %s tier %s at %s (%s), %s, rent %s per cycle" % (row[0], row[1], row[2], row[3].strip("`"), row[4], row[5]))
    print("SITES | %d proposed (where a base is built is Suggi's decision)" % len(sites))
    for row in sites:
        print("  %s (%s): %s space, %s jumps from home, stations there: %s | %s, by %s | %s" % (row[0].strip("`"), row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    print("NEXT STEPS OF THE MEMBER LIMIT | the recruitment line (the whole ladder: section 5 of %s)" % FILE)
    for row in rungs:
        if row[0] in ("faction_storage", "faction_recruitment"):
            print("  %-20s tier %s %-40s %12s cr | %s | rent %s per cycle, %s a day | %s" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    for note in state.get("notes") or []:
        print("  NOTE %s" % note)
    return 0


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data"))]
    if not words or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    verb = words[0]
    if verb == "show":
        return show(data)
    if verb == "collect":
        kind, name = division.member()
        if not (kind == "service" or name == "Unity"):
            sys.exit("REFUSED: reading the faction through the leader's flagship is the Fleet Admiral's; read the result with `empire.py show`")
        state, notes = collect(data, root, force="--ladder" in args)
        save(data, state)
        f = state["faction"]
        print("empire: read %s | members %s of %s | bases %d | offices %d | sites %d | ladder %d types of catalog %s" % (
            state["written_at"], num(f.get("member_count")), num(f.get("members_limit")), len(state["bases"]), len(state["facilities"]), len(state["sites"]), len(state["ladder"]), state["ladder_of"] or "none"))
        for note in notes:
            print("  NOTE %s" % note)
        return 0
    if verb in ("write", "check"):
        state = read_json(Path(data) / "empire" / "empire.json", {})
        path = Path(root) / FILE
        if not state:
            print("%s: no reading on disk (%s): not checked and not written" % (FILE, Path(data) / "empire" / "empire.json"))
            return 0
        text = page(state).rstrip("\n") + "\n"
        try:
            have = path.read_text(encoding="utf-8")
        except OSError:
            have = ""
        same = body(have) == body(text)
        if verb == "check":
            print("%s: %s" % (FILE, "current" if same else "stale or missing; run python3 -I -B game/fleet/empire.py write"))
            return 0 if same else 1
        if same:
            print("%s: current" % FILE)
            return 0
        if "--commit" in args and git(root, "status", "--porcelain", "--", FILE)[1].strip():
            print("%s: holds a change that is not committed; nothing written" % FILE)
            return 0
        path.write_text(text, encoding="ascii")
        print("%s: written" % FILE)
        if "--commit" in args:
            git(root, "add", "--", FILE)
            code, out = git(root, "-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev", "commit", "-q", "-m",
                            "empire: governance/empire.md rewritten from the reading of %s by game/fleet/empire.py" % state.get("written_at"), "--", FILE)
            if code != 0:
                git(root, "reset", "-q", "--", FILE)
                if have:
                    path.write_text(have, encoding="utf-8")
                else:
                    path.unlink()
                print("HALT: the commit failed; the file was put back: " + out.strip()[-200:])
                return 1
            print("%s: committed" % FILE)
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
