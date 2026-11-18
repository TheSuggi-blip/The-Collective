#!/usr/bin/env python3
"""empire.py -- keep the picture of our empire: the faction and its limit, the bases and offices we own, the systems they stand in, the sites we may build on, and what the faction can build next.

WHAT: four verbs.
        collect   looks through the engine's gate with the leader's flagship, views only: the faction's `info` (every
                  page of its member list, by `offset` and `limit`) and tax estimate, every facility and ship garage
                  the faction owns with its rent, and, once per release of the game's catalog, the game's own card
                  of each faction facility type (what the catalog lacks: its rent per cycle), and what the
                  faction's storage holds at each place it stores (one storage
                  `view` per place: each base of ours and each base with an office of the storage line). It joins
                  the public list of stations and outposts (the command station's data: every base with its
                  owner's tag), the chart, the sites file and our censuses (scouting/<system>.json: the base id
                  and the place of each base), and writes <data>/empire/empire.json: faction, members, bases (base
                  id and place), facilities, territory, sites, ladder, faction_storage (base, base_name, item,
                  units, read_at; the fuel of a bunker as item `fuel`) and faction_storage_error.
        write     writes governance/empire.md from that file: the faction in figures, the bases and the territory,
                  the offices and their rent, the sites, and the ladder of what the faction can build
        show      prints the same in plain lines (hive.py empire), with what each faction storage holds
        site      sets one line of game/map/sites.tsv and commits it by path as the member: a member proposes a
                  `candidate` (its own line it may write again), the Fleet Admiral sets `chosen` or `dropped` (rule
                  F33); `built` is read from the game, never set. The next collect puts it into the tables.
        check     governance/empire.md is what `write` would write
RULES:
  - Views only: it founds, builds, pays and changes nothing. A call that is no view is refused here, before the gate.
  - The repository file names no pilot of ours and holds no balance: the members by name and the treasury are in
    the data file only (the repository is public; rulebook section 10).
  - Territory is what the game's own lists show: a system with a station or an outpost that carries our tag, or with
    an office of ours at somebody else's station. Nothing is claimed by hand.
  - A site is a line of game/map/sites.tsv, set by `site` (Q67, Suggi: never by hand); the script adds what
    the chart and the public list of stations say about its system, and reads the site as `built` once a base of ours
    stands in that system. Suggi gives the direction of the expansion; the Fleet Admiral chooses the system.
  - A fact no reading holds is written `not read`, never filled in. The file is rewritten only when a fact changed.
  - Faction storage: a place whose view fails keeps the rows of its last reading and its error is written in
    `faction_storage_error`; a view without items is an empty place (no row). The fuel of a bunker is read from the
    faction's info (`fuel_bunkers`, else `total_fuel_reserve` while one base holds the bunkers); no field: no row.
  - Members: every page of the list, PAGE a page, until the game says it is whole (`members_truncated`) or the pages
    hold `member_count`; a page that fails keeps the last whole list and says so in a note, never half a list.
WHY:  what we own and where stood in no file: the faction's limit was read by hand, the rent of an office was "not
      read yet" in an order, and a plan for a base had no list of what stands already (Suggi, 2026-11-16: "we need
      to have scripts also where our bases and territories are, so we know our empire"). What each faction storage
      holds and where inside its system our outpost stands were read by hand (DECISIONS Q67 (2) and (3)).

USAGE:
  empire.py collect [--ladder]     one reading, written to <data>/empire/empire.json (--ladder: read the cards again)
  empire.py write [--commit]       governance/empire.md from the data file; --commit commits it by path as Unity
  empire.py show
  empire.py site <system> candidate|chosen|dropped [--poi <poi id>] [--note "<why>"]
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
         ("spacemolt_facility", "faction_owned"), ("spacemolt_facility", "types"),
         ("spacemolt_storage", "view")}            # the only calls this script sends: each reads (a storage view passes while the ship flies)
BASE_ID = re.compile(r"[0-9a-f]{32}")             # the game's id of a base of a player faction (an outpost); an empire's station has a word id
SYSTEM_ID = re.compile(r"[a-z0-9_]{1,60}")        # a system id that names a census file (scouting/<system>.json)
STORES = ("lockbox", "storage")                   # a facility type that stores goods; the storage line's other tiers come from the ladder
FILE = "governance/empire.md"
SITES = "game/map/sites.tsv"
ID = "20261116T192710Z"                           # the file's id: it stays when the file is rewritten
CYCLES_A_DAY = 86.4                               # rent is due every 100 ticks of about 10 s (game/rules/07-economy.md)
BASE_CAP = 20                                   # members a faction holds without a recruitment office: the game's refusal of a
                                                # join (faction_full, "maximum of 20 members", 2026-11-17 10:20 UTC)
STATIONS, OUTPOSTS = 5, 8                         # bases a faction may hold (game/rules/09-factions.md)
PAGE = 100                                        # members per page of `info`: its help says paginated, default limit 50, max 100
PAGES = 30                                        # pages one collect asks at most (3,000 members): a game that ignores `offset` ends the loop
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


def census_bases(data, systems):
    """{base id: {poi, name, system}} of every base our censuses list in `systems`: scouting/<system>.json is a ship's
    `get_system` of that system, each place with `base_id` and `base_name` where a base stands (an outpost is a place
    of its own). Read from disk: no call to the game."""
    out = {}
    for system in sorted(s for s in systems if isinstance(s, str) and SYSTEM_ID.fullmatch(s)):
        scan = read_json(Path(data) / "scouting" / (system + ".json"), {})
        info = scan.get("system") if isinstance(scan, dict) and isinstance(scan.get("system"), dict) else {}
        for p in info.get("pois") if isinstance(info.get("pois"), list) else []:
            if isinstance(p, dict) and p.get("base_id") and p.get("id"):
                out[str(p["base_id"])] = {"poi": str(p["id"]), "name": ascii_text(p.get("base_name") or p.get("name"), 60), "system": system}
    return out


def place_bases(bases, facilities, known):
    """Our bases with the game's base id and their place: the census's base of the same name in the system, else the one
    32-hex base id our facilities in that system name. A base neither gives keeps its name as id and no place."""
    out = []
    for b in bases:
        hit = next((bid for bid, p in sorted(known.items()) if p["system"] == b["system"] and p["name"] == b["name"]), "")
        if not hit:
            ids = {f.get("base") for f in facilities if f.get("system") == b["system"] and BASE_ID.fullmatch(str(f.get("base") or ""))}
            hit = ids.pop() if len(ids) == 1 else ""
        out.append(dict(b, base=hit or b["base"], poi=(known.get(hit) or {}).get("poi", "") if hit else b.get("poi", "")))
    return out


def storage_places(bases, facilities, rungs):
    """[(base id, name)] of every place where the faction stores: each base of ours whose id was read, then each base
    with an office of the storage line (`lockbox` or `storage` in its type, or a type of the ladder's line
    faction_storage). A facility names its base by id; its name is the base's own where we know it."""
    line = {r.get("type") for r in rungs or [] if isinstance(r, dict) and r.get("line") == "faction_storage"}
    out = {}
    for b in bases or []:
        if isinstance(b, dict) and b.get("base") and b.get("base") != b.get("name"):        # the name stands in while no id was read
            out.setdefault(str(b["base"]), str(b.get("name") or b["base"]))
    for f in facilities or []:
        kind = str((f or {}).get("type") or "")
        if isinstance(f, dict) and f.get("base") and (kind in line or any(word in kind for word in STORES)):
            out.setdefault(str(f["base"]), str(f["base"]))
    return list(out.items())


def read_storage(pilot, see, places, old, pause, now=None):
    """What the faction's storage holds at each place, one `view` each: (rows, errors). A row: {base, base_name, item,
    units, read_at}. A place whose view fails keeps its rows of the last reading (`old`); a view without items is an
    empty place. An item the answer files under another base is left to that base's own view."""
    rows, errors, stamp = [], [], now_text(now)
    kept = [r for r in old or [] if isinstance(r, dict) and r.get("item") != "fuel"]
    for n, (base, name) in enumerate(places):
        if n and pause:
            time.sleep(pause)
        found, why = see(pilot, "spacemolt_storage", "view", {"target": "faction", "station_id": base}) if pilot else (None, "no flagship of the Fleet Admiral")
        items = found.get("items") if isinstance(found, dict) else None
        empty = isinstance(found, dict) and (("items" in found and items is None) or "no items" in str(found.get("hint") or "").lower())
        if not isinstance(items, list) and not empty:            # no answer, or one that is no storage view
            errors.append("%s: %s" % (name, why or "no list `items` in the answer"))
            rows += [r for r in kept if r.get("base") == base]
            continue
        got = {}
        for i in items if isinstance(items, list) else []:
            if not isinstance(i, dict) or not i.get("item_id") or str(i.get("base_id") or i.get("station_id") or base) != base:
                continue
            try:
                units = int(i.get("quantity") or 0)            # the engine's storage rows: item_id, quantity (ledger.py)
            except (TypeError, ValueError):
                units = 0
            if units > 0:
                got[str(i["item_id"])] = got.get(str(i["item_id"]), 0) + units
        rows += [{"base": base, "base_name": name, "item": item, "units": units, "read_at": stamp} for item, units in sorted(got.items())]
    return rows, errors


def fuel_rows(info, facilities, names, old, now=None):
    """The fuel in our bunkers as faction storage rows (item `fuel`), from the faction's info: its list `fuel_bunkers`
    (each bunker's `fuel_reserve`), else `total_fuel_reserve` while every bunker stands at one base. (rows, note): no
    info keeps the last rows; a bunker no field reports gives no row and a note."""
    if info is None:
        return [r for r in old or [] if isinstance(r, dict) and r.get("item") == "fuel"], ""
    bunkers = sorted({str(f.get("base")) for f in facilities if "fuel_bunker" in str(f.get("type") or "") and f.get("base")})
    listed = info.get("fuel_bunkers")
    listed = [dict(v, base_id=k) if isinstance(v, dict) else {"base_id": k, "fuel_reserve": v} for k, v in listed.items()] if isinstance(listed, dict) else listed
    got, stamp = {}, now_text(now)
    for b in listed if isinstance(listed, list) else []:
        units = next((b[k] for k in ("fuel_reserve", "fuel", "reserve") if isinstance(b, dict) and isinstance(b.get(k), (int, float))), None)
        base = next((str(b[k]) for k in ("base_id", "station_id", "base", "station") if isinstance(b, dict) and b.get(k)), bunkers[0] if len(bunkers) == 1 else "")
        if base and units is not None:
            got[base] = got.get(base, 0) + int(units)
    if not got and isinstance(info.get("total_fuel_reserve"), (int, float)) and len(bunkers) == 1:
        got[bunkers[0]] = int(info["total_fuel_reserve"])
    note = "the fuel of the bunker(s) at %s not read: no field of the faction's info holds it" % ", ".join(bunkers) if bunkers and not got else ""
    return [{"base": base, "base_name": names.get(base, base), "item": "fuel", "units": units, "read_at": stamp} for base, units in sorted(got.items())], note


def member_pages(pilot, see, first, pause):
    """The faction's whole member list: ([{pilot, role}], a note or ''). `info` answers one page of it (`members_offset`,
    `members_limit` = the page size, `members_truncated`: that page only, its help); the next pages are asked with
    `offset` and `limit` until the game says the list is whole (`members_truncated` false), else until the pages hold
    `member_count`. A page that is not read: (None, why), and the caller keeps the last whole list (requests ENT-262: the
    first page alone read 50 of 94 members, and a seated miner looked unseated)."""
    out, seen, answer = [], set(), first
    offset = first.get("members_offset") if isinstance(first.get("members_offset"), int) else 0
    for _page in range(PAGES):
        listed = [m for m in answer.get("members") or [] if isinstance(m, dict)]
        fresh = [{"pilot": ascii_text(m.get("username"), 40), "role": ascii_text(m.get("role"), 20)} for m in listed if m.get("username")]
        fresh = [m for m in fresh if not (m["pilot"] in seen or seen.add(m["pilot"]))]
        out += fresh
        total = answer.get("member_count") if isinstance(answer.get("member_count"), int) else first.get("member_count")
        cut = answer.get("members_truncated")
        if not (cut if isinstance(cut, bool) else isinstance(total, int) and len(out) < total):
            return out, ""
        if not fresh:
            return out, "the member list holds %d of %s: the game's page at offset %d brought no new member" % (len(out), num(total), offset)
        offset = (answer["members_offset"] if isinstance(answer.get("members_offset"), int) else offset) + len(listed)
        if pause:
            time.sleep(pause)
        answer, why = see(pilot, "spacemolt_faction", "info", {"limit": PAGE, "offset": offset})
        if answer is None:
            return None, "the faction's member list was not read whole (the page at offset %d: %s): the last whole list stays" % (offset, why)
    return out, "the member list holds %d of %s after %d pages: the rest was not read" % (len(out), num(first.get("member_count")), PAGES)


def collect(data, root, see=look, force=False, pause=0.5, now=None):
    """One reading of the empire; (the state, the lines to print). The state is what <data>/empire/empire.json holds."""
    old = read_json(Path(data) / "empire" / "empire.json", {})
    notes, pilot = [], leader(data)
    if not pilot:
        notes.append("no flagship of the Fleet Admiral in fleet/flagships.json: the faction was not read")
    info, why = see(pilot, "spacemolt_faction", "info", {"limit": PAGE}) if pilot else (None, "no leader")
    if info is None:
        notes.append("faction info not read (%s): the last reading stays" % why)
    faction = dict(old.get("faction") or {})
    members = old.get("members") or []
    if info is not None:
        money = next((info[k] for k in ("treasury", "treasury_credits", "treasury_balance", "credits") if isinstance(info.get(k), (int, float))), None)
        faction = {"id": str(info.get("id") or ""), "name": ascii_text(info.get("name"), 60), "tag": ascii_text(info.get("tag"), 8), "leader": ascii_text(info.get("leader_username"), 40),
                   "member_count": info.get("member_count"), "members_limit": info.get("members_limit"), "treasury": money, "owned_bases": info.get("owned_bases"),
                   "at_war": bool(info.get("at_war")), "created_at": str(info.get("created_at") or "")}
        listed, short = member_pages(pilot, see, info, pause)          # every page of the member list (requests ENT-262)
        members = listed if listed is not None else members
        if short:
            notes.append(short)
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
    censused = census_bases(data, {b["system"] for b in bases} | {f.get("system") for f in facilities})      # base ids and places, from our censuses
    bases = place_bases(bases, facilities, censused)
    garages, _why = see(pilot, "spacemolt_faction", "garages") if pilot else (None, "")
    tax, _why = see(pilot, "spacemolt_faction", "tax_estimate") if pilot else (None, "")
    territory, seen = [], set()
    for base in bases:
        if base["system"] and (base["system"], base["kind"]) not in seen:
            seen.add((base["system"], base["kind"]))
            territory.append({"system": base["system"], "claim": base["kind"], "note": base["name"]})
    ours = {b["name"] for b in bases} | {b["base"] for b in bases}         # an office inside a base of ours names the base by its id
    for f in facilities:
        if f["system"] and f["base"] not in ours and (f["system"], "office") not in seen:
            seen.add((f["system"], "office"))
            territory.append({"system": f["system"], "claim": "office", "note": "at %s" % f["base"]})
    sites = []
    for row in site_rows(root):
        known = systems.get(row["system"])
        there = ["%s (%s%s)" % (ascii_text(s.get("name"), 60), s.get("type") or "station", ", " + ascii_text(s.get("tag"), 8) if s.get("tag") else "") for s in public if s.get("system") == row["system"]]
        status = "built" if row["status"] != "dropped" and any(b["system"] == row["system"] for b in bases) else row["status"]      # a base of ours stands there: the game says so, no hand
        sites.append(dict(row, status=status, name=known["name"] if known else "", space=("not on the chart" if not known else known["empire"] or "lawless"), jumps=known["jumps"] if known else None, stations=there))
    feed = ((read_json(Path(data) / "station" / "feed.json", {}) or {}).get("factions") or {}).get(tag) or {}
    ships = [s for s in (read_json(Path(data) / "fleet" / "fleet.json", {}) or {}).get("ships") or [] if isinstance(s, dict) and s.get("name")]
    rungs, version = ladder(data, pilot, see, old, force, pause)
    recruit = {r.get("type"): r.get("cap") for r in rungs if isinstance(r, dict) and r.get("line") == "faction_recruitment"}
    faction["members_limit"] = members_cap(facilities, recruit)        # the info's own members_limit is a page size
    names = {bid: p["name"] for bid, p in censused.items()}
    names.update({b["base"]: b["name"] for b in bases})
    places = [(base, names.get(base, name)) for base, name in storage_places(bases, facilities, rungs)]
    stored, errors = read_storage(pilot, see, places, old.get("faction_storage"), pause, now)
    fuel, unread = fuel_rows(info, facilities, names, old.get("faction_storage"), now)
    if errors:
        notes.append("faction storage not read at %s: the last reading of each stays" % "; ".join(errors))
    if unread:
        notes.append(unread)
    order = {base: n for n, (base, _name) in enumerate(places)}
    stored = sorted(stored + fuel, key=lambda r: (order.get(r["base"], len(order)), r["base"], r["item"] == "fuel", r["item"]))
    state = {"written_at": now_text(now), "faction": faction, "members": members, "bases": bases, "facilities": facilities, "territory": territory, "sites": sites,
             "faction_storage": stored, "faction_storage_error": "; ".join(errors), "faction_storage_places": [{"base": b, "base_name": n} for b, n in places],
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


def members_cap(facilities, recruit):
    """The faction's cap on members: BASE_CAP without a recruitment office; with offices, the best station's office in full
    plus a quarter of each other station's (game/rules/09-factions.md). `members_limit` in the game's faction info is the
    page size of its member list, not the cap (the help of spacemolt_faction info; read wrongly as a cap of 50 until a
    join was refused at 20 on 2026-11-17)."""
    best = {}
    for f in facilities or []:
        cap = recruit.get(f.get("type"))
        if isinstance(cap, int) and not isinstance(cap, bool) and str(f.get("status") or "active") == "active":
            best[f.get("base")] = max(best.get(f.get("base"), 0), cap)
    caps = sorted(best.values(), reverse=True)
    return max(BASE_CAP, caps[0] + sum(c // 4 for c in caps[1:])) if caps else BASE_CAP


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


def show_storage(state):
    """The block `FACTION STORAGE`: each place where the faction stores (the places the reading viewed) with its goods
    (or `empty`), the fuel of a bunker among them; a reading from before this block existed says so."""
    rows = [r for r in state.get("faction_storage") or [] if isinstance(r, dict) and r.get("base")]
    places = [(str(p["base"]), str(p.get("base_name") or p["base"])) for p in state.get("faction_storage_places") or [] if isinstance(p, dict) and p.get("base")]
    places = places or storage_places(state.get("bases"), state.get("facilities"), state.get("ladder"))
    names = {b.get("base"): b.get("name") for b in state.get("bases") or [] if isinstance(b, dict)}
    names.update({r["base"]: r.get("base_name") for r in rows if r.get("base_name")})
    for r in rows:
        if r["base"] not in dict(places):
            places.append((r["base"], r["base"]))
    if "faction_storage" not in state:
        print("FACTION STORAGE | not read yet: the next `empire.py collect` reads it")
        return
    error = state.get("faction_storage_error") or ""
    print("FACTION STORAGE | %d place(s) | read %s%s" % (len(places), state.get("written_at"), (" | NOT READ: %s (the last reading stays)" % error) if error else ""))
    for base, name in places:
        goods = sorted((r for r in rows if r["base"] == base), key=lambda r: (r.get("item") == "fuel", -(r.get("units") or 0), str(r.get("item"))))
        label = names.get(base) or name
        print("  %s%s: %s" % (label, " (%s)" % base if label != base else "", ", ".join("%s %s" % (num(r.get("units")), r.get("item")) for r in goods) or "empty"))


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
    for row, b in zip(bases, state.get("bases") or []):
        where = "place %s, base id %s" % (b.get("poi"), b.get("base")) if b.get("poi") else "place not read (no census of ours lists it)"
        print("  %s (%s) in %s, %s | %s" % (row[0], row[1], row[2].strip("`"), row[3], where))
    print("OFFICES | %d" % len(offices))
    for row in offices:
        print("  %s tier %s at %s (%s), %s, rent %s per cycle" % (row[0], row[1], row[2], row[3].strip("`"), row[4], row[5]))
    show_storage(state)
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


STATUSES = ("candidate", "chosen", "dropped")        # `built` is the game's: a base of ours stands in the system


def set_site(root, data, who, system, status, poi="", note=""):
    """Write the line of one system in game/map/sites.tsv and commit it by path as `who`: (True, the line) or (False,
    why). The system must be on the chart; a member proposes a `candidate` and may write its own line again; the Fleet
    Admiral chooses or drops a site (rule F33) and keeps the proposer's name and note. Nothing is written while the file
    holds a change that is not committed."""
    if system not in chart(data, root):
        return False, "REFUSED: `%s` is no system of the chart (game/map/galaxy.tsv)" % system
    if status not in STATUSES:
        return False, "REFUSED: a site's status is one of %s; `built` is read from the game" % ", ".join(STATUSES)
    if status != "candidate" and who != "Unity":
        return False, "REFUSED: the Fleet Admiral chooses or drops a site (rule F33); propose it as a candidate"
    if git(root, "status", "--porcelain", "--", SITES)[1].strip():
        return False, "REFUSED: %s holds a change that is not committed; commit it or take it back first" % SITES
    path = Path(root) / SITES
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        lines = ["system\tpoi\tstatus\tproposed_by\tnote"]
    clean = lambda text: ascii_text(str(text or "").replace("\t", " "), 300)
    out, line = [], None
    for old in lines:
        cells = old.split("\t")
        if old.startswith("#") or cells[0] != system:
            out.append(old)
            continue
        cells += [""] * (5 - len(cells))
        if who != "Unity" and cells[3] and who not in [c.strip() for c in cells[3].split(",")]:
            return False, "REFUSED: %s stands as another member's line (proposed by %s): ask the Fleet Admiral in requests.log" % (system, cells[3])
        line = "\t".join([system, poi or cells[1] or "-", status, cells[3] or who, clean(note) or cells[4]])
        out.append(line)
    if line is None:
        line = "\t".join([system, poi or "-", status, who, clean(note)])
        out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="ascii")
    git(root, "add", "--", SITES)
    code, said = git(root, "-c", "user.name=" + who, "-c", "user.email=%s@suggi-workspace.dev" % who.lower(), "commit", "-q", "-m",
                     "sites: %s %s (empire.py site, %s)" % (system, status, who), "--", SITES)
    if code != 0:
        git(root, "reset", "-q", "--", SITES)
        git(root, "checkout", "--", SITES)
        return False, "HALT: the commit failed; the file was put back: " + said.strip()[-200:]
    return True, line.replace("\t", " | ")


def git(root, *args):
    done = subprocess.run(["git", "-C", str(root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return done.returncode, done.stdout


def main():
    args = sys.argv[1:]
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root, data = value("--root", str(here.parent.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--root", "--data", "--poi", "--note"))]
    if not words or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    verb = words[0]
    if verb == "show":
        return show(data)
    if verb == "site":
        kind, name = division.member()
        if kind != "member" or len(words) < 3:
            sys.exit("REFUSED: run as a member of the Collective: empire.py site <system> candidate|chosen|dropped [--poi <id>] [--note \"<why>\"]")
        ok, line = set_site(root, data, name, words[1], words[2], poi=value("--poi", ""), note=value("--note", ""))
        print(("site set and committed: %s (the tables read it at the next collect, within a quarter of an hour)" % line) if ok else line)
        return 0 if ok else 1
    if verb == "collect":
        kind, name = division.member()
        if not (kind == "service" or name == "Unity"):
            sys.exit("REFUSED: reading the faction through the leader's flagship is the Fleet Admiral's; read the result with `empire.py show`")
        state, notes = collect(data, root, force="--ladder" in args)
        save(data, state)
        f = state["faction"]
        print("empire: read %s | members %s of %s | bases %d | offices %d | faction storage %d rows | sites %d | ladder %d types of catalog %s" % (
            state["written_at"], num(f.get("member_count")), num(f.get("members_limit")), len(state["bases"]), len(state["facilities"]), len(state["faction_storage"]),
            len(state["sites"]), len(state["ladder"]), state["ladder_of"] or "none"))
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
