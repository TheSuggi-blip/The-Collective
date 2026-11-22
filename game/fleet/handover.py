#!/usr/bin/env python3
"""handover.py -- goods given into the storage of another pilot of ours: a circuit stop's `gift`, a mine route's `gift`, a hunt route's `gift_to`.

WHAT: the one hand-over the three runners share (route_run.py, mine.py, hunt.py). Docked at a station with storage,
      the giver's goods go into the receiver's own storage there: `spacemolt_storage` `deposit` with `target` the
      receiver's name and `source` `storage` or `cargo` (the game's direct transfer, a gift: the receiver need be
      neither docked nor online; miner-22 to trader-10 at central_nexus, 2026-11-21 22:12 UTC). A gift:
        to       a role word (trader, hauler, ...): the pilot its Admiral named for this station in
                 data/fleet/receivers.json ({role: {base id or "*": pilot}}; the repository is public and a route
                 file names no numbered pilot of ours, requests ENT-052), or a pilot of ours by name (a flagship,
                 or any ship of fleet.json in a route file outside the repository)
        items    a list of item ids, or "all" (the default): every good but ammunition (data/catalog/ammo.json)
        source   storage (the default), cargo, or both (the hold first)
        keep     {item: units} the giver keeps here
      Many items go in one call (the v2 `items` list) where the game takes it, else one call per item; what went is
      read back from the giver's storage view and hold, never taken from the answer. Every gift that moved goods is
      one line of data/stock/handover.jsonl (at, from, to, base, items, route): the service ledger reads both sides
      again, first, at its next pass (sides_first), so that the storage book neither loses a unit nor counts one twice.
        receivers                                    the receivers named, per role and station
        receivers set <role> <base|*> <pilot>        name one: a pilot of ours of that role, or a flagship
        receivers add <role> <base|*> <pilot>        one more at that station: the givers are spread over them
        receivers drop <role> <base|*>               take one out
        dry-run <route id> [<giver>]                 per gift of the route: where, to whom (or why to nobody), and
                                                     with a giver what the storage book holds there and would go
RULES:
  - Behind the switch file data/fleet/strict-classes-on (workclass.strict_on; absent = off): off, a gift gives
    nothing and calls nothing; the run is what it was before.
  - A gift goes only to a pilot of ours (fleet.json, its `away`, flagships.json) and never to the giver itself: any
    other name is refused before a call (a gift to a stranger is a loss). A refused gift leaves the goods with the
    giver, and says so. Nothing is sold here.
  - A gift is no one's earning: no wallet moves, so no run is credited or charged with it; what the receiver sells
    is Trade's income (rule F23).
  - The runner hands in its own `raw`, `cargo`, `say` and `sleep`: a run in the run host stops at its own sleep,
    and this module prints nothing (the runner prints the line give() returns).
  - `receivers set` and `drop` are the keeper's: the Admiral of that role (Mercury the traders, Apollo the haulers)
    or the Fleet Admiral.
WHY:  Suggi, 2026-11-21: "Only Zero mines, only Mercury trades": selling is Trade's alone, and the goods of the other
      divisions reach a trader (or a hauler, for what we build with) by gift into its storage, where its sell and
      craft routes find them: storage is per pilot, and faction storage needs `manage_treasury` to take out.

USAGE:
  handover.py receivers [set <role> <base|*> <pilot> | drop <role> <base|*>]
  handover.py dry-run <route id> [<giver>]
  --data <dir>   the unit's data folder (default FLEET_DATA_ROOT or /srv/collective/data)
  --root <dir>   the repository's game/ folder (default: the parent of this file's folder)

Stdlib only. ASCII only.
"""

import calendar
import fcntl
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import workclass                                  # noqa: E402  the switch data/fleet/strict-classes-on
import zlib                                       # noqa: E402  requests ENT-344 (2): which receiver of several

DATA = os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data"
RECEIVERS = os.path.join("fleet", "receivers.json")
RECORD = os.path.join("stock", "handover.jsonl")
ROLES = workclass.ALL
SOURCES = ("storage", "cargo", "both")
TICK = 11                    # seconds a game tick takes, with a margin (route_run.py TICK)
TAIL = 256 * 1024            # bytes of the record the ledger reads from its end
SIDES_HOURS = 6              # a gift older than this asks the ledger for nothing
SIDES_PER_PASS = 4           # pilots the ledger reads first for gifts, at most, a pass
RETRY = 120                  # seconds: a side whose reading failed is asked for again after this (ledger.py RETRY)


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def ours(data=None):
    """The names of our pilots: the ships and the `away` list of data/fleet/fleet.json, and the flagships. An
    unreadable fleet file names none: then no gift goes."""
    data = data or DATA
    fleet = read_json(Path(data) / "fleet" / "fleet.json", {})
    rows = ((fleet.get("ships") or []) + (fleet.get("away") or [])) if isinstance(fleet, dict) else []
    names = {str(s.get("name")) for s in rows if isinstance(s, dict) and s.get("name")}
    flags = read_json(Path(data) / "fleet" / "flagships.json", {})
    return names | (set(flags) if isinstance(flags, dict) else set())


def role_of(name, data=None):
    """A pilot's role: its flagship entry's, else the word before the dash of its name (dispatch.role_of)."""
    flags = read_json(Path(data or DATA) / "fleet" / "flagships.json", {})
    entry = flags.get(name) if isinstance(flags, dict) else None
    return str(entry.get("role") or "") if isinstance(entry, dict) else str(name).split("-")[0]


def receivers(data=None):
    """{role: {base id or "*": pilot or [pilots]}} of data/fleet/receivers.json (a list: several receivers there)."""
    found = read_json(Path(data or DATA) / RECEIVERS, {})
    return {role: dict(table) for role, table in found.items() if role in ROLES and isinstance(table, dict)} if isinstance(found, dict) else {}


def spec_of(value):
    """A gift as a dict ({to, items, source, keep}) from a route's value: a word is the receiver alone."""
    if isinstance(value, str):
        return {"to": value}
    return dict(value) if isinstance(value, dict) else {}


def faults(value, flagships=()):
    """What is wrong with one gift of a route file, one line each (routes.py check). `to` is a role word or a
    flagship; a numbered pilot of ours is the gate's own fault (a route file names none); any other name is a
    stranger."""
    spec, out = spec_of(value), []
    if not spec:
        return ["a gift is a receiver's word or {\"to\", \"items\", \"source\", \"keep\"}"]
    to = spec.get("to")
    if not isinstance(to, str) or not to.strip():
        out.append("a gift needs `to`: a role (%s) or a flagship of ours" % ", ".join(ROLES))
    elif to not in ROLES and to not in set(flagships) and not numbered(to):
        out.append("a gift to `%s`: neither a role (%s) nor a flagship of ours: a gift to a stranger is a loss" % (to, ", ".join(ROLES)))
    items = spec.get("items", "all")
    if items != "all" and not (isinstance(items, list) and items and all(isinstance(i, str) and i for i in items)):
        out.append("a gift's `items` is \"all\" or a list of item ids")
    if spec.get("source", "storage") not in SOURCES:
        out.append("a gift's `source` is one of %s" % ", ".join(SOURCES))
    keep = spec.get("keep", {})
    if not (isinstance(keep, dict) and all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in keep.values())):
        out.append("a gift's `keep` is {item: units}")
    return out


def numbered(name):
    """True for a name of the form of our numbered pilots (role-number): the gate names those itself."""
    head, _, tail = str(name).partition("-")
    return head in ROLES and tail.isdigit()


def receiver(to, base, data=None, giver=None):
    """(the receiver's name, '') or (None, why not): a role word through data/fleet/receivers.json (this station,
    else `*`), a name as it stands; only a pilot of ours, never the giver."""
    data = data or DATA
    to = str(to or "").strip()
    if not to:
        return None, "no receiver named (`to`)"
    if to in ROLES:
        table = receivers(data).get(to) or {}
        name = table.get(base) or table.get("*")
        if isinstance(name, list):                       # requests ENT-344 (2): several receivers, each giver always to the same one
            names = [n for n in name if isinstance(n, str) and n and n != giver and n in ours(data)]
            name = names[zlib.crc32(str(giver or "").encode("utf-8")) % len(names)] if names else None
        if not name:
            return None, "no %s named to receive at %s (handover.py receivers set %s %s <pilot>)" % (to, base, to, base)
    else:
        name = to
    if name not in ours(data):
        return None, "`%s` is not a pilot of ours (fleet.json, flagships): a gift to a stranger is a loss" % name
    if name == giver:
        return None, "`%s` is the giver itself" % name
    return name, ""


def on(data=None):
    """True while the switch data/fleet/strict-classes-on stands (workclass.strict_on)."""
    return workclass.strict_on(data or DATA)


def ammo(data=None):
    found = read_json(Path(data or DATA) / "catalog" / "ammo.json", [])
    return set(found) if isinstance(found, list) else set()


def view(raw, base):
    """{item: units} of the pilot's own storage here (`view` with station_id), or None when the answer holds no items."""
    d = raw("view", {"station_id": base}, "spacemolt_storage")
    d = d if isinstance(d, dict) else {}
    sc = d.get("structuredContent")
    if not isinstance(sc, dict) and isinstance(d.get("result"), dict):
        sc = d["result"].get("structuredContent") if isinstance(d["result"].get("structuredContent"), dict) else d["result"]
    if not isinstance(sc, dict) or not isinstance(sc.get("items"), list):
        return None
    return {str(i.get("item_id")): int(i.get("quantity") or 0) for i in sc["items"] if isinstance(i, dict) and i.get("item_id")}


def planned(spec, stored, hold, ammo_ids):
    """{item: {"cargo": units, "storage": units}} a gift gives: of the named items (or every good but ammunition),
    what its sources hold less its `keep`, the hold first."""
    source = spec.get("source") or "storage"
    pools = {"cargo": hold if source in ("cargo", "both") else {}, "storage": stored if source in ("storage", "both") else {}}
    items = spec.get("items", "all")
    names = sorted(set(pools["cargo"]) | set(pools["storage"])) if items == "all" else list(items)
    keep = spec.get("keep") if isinstance(spec.get("keep"), dict) else {}
    out = {}
    for item in names:
        if items == "all" and item in ammo_ids:
            continue
        c, s = max(int(pools["cargo"].get(item, 0) or 0), 0), max(int(pools["storage"].get(item, 0) or 0), 0)
        give = max(c + s - int(keep.get(item, 0) or 0), 0)
        from_cargo = min(c, give)
        from_storage = min(s, give - from_cargo)
        if from_cargo or from_storage:
            out[item] = {"cargo": from_cargo, "storage": from_storage}
    return out


def words(goods):
    return ", ".join("%s %d" % (item, units) for item, units in sorted(goods.items()) if units) or "nothing"


def record(data, row):
    """One line of data/stock/handover.jsonl, appended under a lock."""
    path = Path(data) / RECORD
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n")


def give(raw, cargo, say, sleep, giver, base, value, data=None, route=None, clock=time.time):
    """One gift at the station the giver is docked at (base id). raw(action, params, group) is the runner's call to
    the engine, cargo() its read of the hold ({item: units}), say(text) its log line, sleep(seconds) its wait.
    Returns {to, asked, given, left, note, line}: what was asked and given per item, what stayed with the giver,
    the note for the run's row (None when all went) and the RESULT line the runner prints. Off: nothing is called."""
    data = data or DATA
    spec = spec_of(value)
    out = {"to": None, "asked": {}, "given": {}, "left": {}, "note": None, "line": ""}
    if not on(data):
        out["line"] = "RESULT gift %s at %s: not given, strict classes are off (%s absent)" % (giver, base, workclass.SWITCH)
        return out
    to, why = receiver(spec.get("to"), base, data, giver)
    if not to:
        out.update(note="gift at %s: %s" % (base, why), line="RESULT gift %s at %s: refused before any call: %s; the goods stay with the giver" % (giver, base, why))
        return out
    out["to"] = to
    stored, hold = view(raw, base), cargo()
    if stored is None:
        out.update(note="gift to %s at %s: storage not read, nothing given" % (to, base),
                   line="RESULT gift %s -> %s at %s: nothing given, the storage view did not answer" % (giver, to, base))
        return out
    plan = planned(spec, stored, hold, ammo(data))
    out["asked"] = {item: p["cargo"] + p["storage"] for item, p in plan.items()}
    if not plan:
        out["line"] = "RESULT gift %s -> %s at %s: nothing to give (%s)" % (giver, to, base, "items %s" % (spec.get("items", "all")))
        return out
    given, errors = {}, []
    for source in ("cargo", "storage"):
        batch = {item: p[source] for item, p in plan.items() if p[source]}
        if not batch:
            continue
        read = cargo if source == "cargo" else (lambda: view(raw, base) or {})
        before = dict(hold) if source == "cargo" else dict(stored)
        moved = lambda now: {item: max(min(before.get(item, 0) - now.get(item, 0), units), 0) for item, units in batch.items()}
        went, bulk = {}, False
        if len(batch) > 1:                               # the v2 `items` list: many goods in one call
            bulk = True
            d = raw("deposit", {"items": [{"item_id": item, "quantity": units} for item, units in sorted(batch.items())],
                                "source": source, "target": to}, "spacemolt_storage")
            sleep(TICK)
            went = moved(read())
            if not any(went.values()) and "error" not in (d if isinstance(d, dict) else {}):
                sleep(TICK)                              # an answer without error may land a tick late: one more look
                went = moved(read())
            if "error" in (d if isinstance(d, dict) else {}) and not any(went.values()):
                say("gift to %s: the list of %d goods was not taken (%s): one call per good" % (to, len(batch), str(d.get("error"))[:80]))
        for item, units in sorted(batch.items()):
            rest = units - went.get(item, 0)
            if rest <= 0:
                continue
            d = raw("deposit", {"item_id": item, "quantity": rest, "source": source, "target": to}, "spacemolt_storage")
            sleep(TICK)
            if isinstance(d, dict) and "error" in d:
                errors.append("%s: %s" % (item, " ".join(str(d.get("error")).split())[:80]))
        if not bulk or any(units - went.get(item, 0) > 0 for item, units in batch.items()):
            went = moved(read())
        for item, units in went.items():
            if units:
                given[item] = given.get(item, 0) + units
    out["given"] = given
    out["left"] = {item: units - given.get(item, 0) for item, units in out["asked"].items() if units - given.get(item, 0) > 0}
    if given:
        record(data, {"at": int(clock()), "from": giver, "to": to, "base": base, "items": given, "route": route or ""})
    if out["left"]:
        out["note"] = "gift to %s at %s: %s of %s given, kept %s%s" % (to, base, sum(given.values()), sum(out["asked"].values()), words(out["left"]),
                                                                         (" (%s)" % "; ".join(errors[:3])) if errors else "")
    out["line"] = "RESULT gift %s -> %s at %s: %s%s" % (giver, to, base, words(given), (" | refused, kept by the giver: %s" % words(out["left"])) if out["left"] else "")
    return out


def stamp(text):
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0


def recent(data, now, hours=SIDES_HOURS):
    """[gift row] of the record's tail within `hours`, oldest first."""
    path = Path(data) / RECORD
    try:
        with open(path, "rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            handle.seek(max(size - TAIL, 0))
            text = handle.read().decode("utf-8", "replace")
    except OSError:
        return []
    rows = []
    for line in text.splitlines()[1 if size > TAIL else 0:]:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and isinstance(row.get("at"), (int, float)) and now - row["at"] <= hours * 3600:
            rows.append(row)
    return rows


def sides_first(names, book, data, now, first, turns, most=SIDES_PER_PASS):
    """The ledger's hook (ledger.batch_of): the givers and receivers of the gifts since their last reading in the
    storage book, read first in this pass (both sides of a gift in one pass: the book never holds a unit on both
    sides or on neither for longer), then `first`; none twice, none the rotation reads anyway (`turns`), at most
    `most` for gifts. Only pilots the pass reads (`names`); a side whose reading failed within RETRY waits."""
    now = time.time() if now is None else now
    pilots, want = (book or {}).get("pilots") or {}, []
    for row in recent(data, now):
        for side in (row.get("from"), row.get("to")):
            entry = pilots.get(side) or {}
            if side in names and side not in turns and side not in want and stamp(entry.get("read_at")) < row["at"] \
                    and now - stamp(entry.get("error_at")) >= RETRY:
                want.append(side)
    want = want[:most]
    return want + [pilot for pilot in first if pilot not in want]


# ---- the command line

def keeper_may(role, data):
    """True when the shell may name a receiver of `role`: the role's Admiral, the Fleet Admiral or a service."""
    try:
        import division
        kind, name = division.member()
    except Exception:                                 # noqa: BLE001  no division module: nobody is known
        return False
    return kind == "service" or name in ("Unity", workclass.KEEPERS.get(role))


def show_receivers(data):
    table = receivers(data)
    print("RECEIVERS | %s | %s" % (Path(data) / RECEIVERS, "the switch strict-classes-on is %s" % ("on" if on(data) else "off")))
    if not table:
        print("  none named: `handover.py receivers set <role> <base|*> <pilot>`")
    known = ours(data)
    for role in ROLES:
        for base, names in sorted((table.get(role) or {}).items()):
            for name in names if isinstance(names, list) else [names]:
                print("  %-8s %-36s %s%s" % (role, base, name, "" if name in known else "   NOT a pilot of ours: a gift there is refused"))
    return 0


def set_receiver(data, role, base, name, drop=False, add=False):
    if role not in ROLES:
        print("REFUSED: `%s` is no role (%s)" % (role, ", ".join(ROLES)))
        return 1
    if not keeper_may(role, data):
        print("REFUSED: the receivers of the %ss are named by %s or the Fleet Admiral" % (role, workclass.KEEPERS.get(role)))
        return 1
    if not drop and name not in ours(data):
        print("REFUSED: `%s` is not a pilot of ours (fleet.json, flagships)" % name)
        return 1
    if not drop and role_of(name, data) != role and name not in read_json(Path(data) / "fleet" / "flagships.json", {}):
        print("REFUSED: `%s` is a %s, not a %s" % (name, role_of(name, data), role))
        return 1
    path = Path(data) / RECEIVERS
    found = read_json(path, {})
    found = found if isinstance(found, dict) else {}
    table = found.setdefault(role, {})
    if drop:
        table.pop(base, None)
    elif add:                                            # one more receiver at this station (requests ENT-344 (2))
        now = table.get(base)
        now = now if isinstance(now, list) else ([now] if now else [])
        table[base] = now + [name] if name not in now else now
    else:
        table[base] = name
    found["what"] = "the receivers of gifts (handover.py): per role and station base (or *) the pilot of ours whose storage takes them"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(".%s.%d.tmp" % (path.name, os.getpid()))
    tmp.write_text(json.dumps(found, indent=1, sort_keys=True) + "\n", encoding="ascii")
    os.replace(tmp, path)
    print("%s: %s %s at %s" % (path, "dropped" if drop else "named", role, base) + ("" if drop else ": " + name))
    return 0


def gifts_of(route):
    """[(base id, gift value)] of a route: a circuit's stops, a mine route's station, a hunt route's sell_at."""
    if route.get("kind") == "circuit":
        out = []
        for stop in route.get("stops") or []:
            if isinstance(stop, dict) and stop.get("gift"):
                for value in stop["gift"] if isinstance(stop["gift"], list) else [stop["gift"]]:
                    out.append((str(stop.get("at", "")).split(":")[-1], value))
        return out
    if route.get("kind") == "mine" and route.get("gift"):
        return [(str(route.get("station", "")).split(":")[-1], route["gift"])]
    if route.get("kind") == "hunt" and route.get("gift_to"):
        return [(str(route.get("sell_at", "")).split(":")[-1], {"to": route["gift_to"], "items": "all", "source": "cargo"})]
    return []


def dry_run(root, data, rid, giver=None):
    route = read_json(Path(root) / "routes" / (rid + ".json"), None)
    if not isinstance(route, dict):
        print("no route file game/routes/%s.json" % rid)
        return 1
    gifts = gifts_of(route)
    print("DRY RUN | %s: %d gift(s); the switch strict-classes-on is %s (off: every gift gives nothing) | no call is made"
          % (rid, len(gifts), "on" if on(data) else "off"))
    book = read_json(Path(data) / "stock" / "storage.json", {})
    entry = ((book.get("pilots") or {}).get(giver) or {}) if giver and isinstance(book, dict) else {}
    for base, value in gifts:
        spec = spec_of(value)
        to, why = receiver(spec.get("to"), base, data, giver)
        print("  at %-34s to %s" % (base, to or ("nobody: " + why)))
        if giver and (spec.get("source") or "storage") == "cargo":     # a hunt's gift_to: what its hold carries at the run's end
            print("     gives what the hold carries at the run's end (source cargo): %s's storage there stays where it is" % giver)
        elif giver:
            stored = (entry.get("stations") or {}).get(base) or {}
            plan = planned(dict(spec, source="storage"), stored, {}, ammo(data))
            print("     %s's storage there by the book (read %s): would go %s" % (giver, entry.get("read_at") or "never",
                                                                              words({i: p["storage"] for i, p in plan.items()})))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    data, root = value("--data", DATA), value("--root", str(Path(__file__).resolve().parent.parent))
    words_ = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--data", "--root"))]
    if words_[:1] == ["receivers"]:
        if len(words_) == 1:
            return show_receivers(data)
        if words_[1] == "set" and len(words_) == 5:
            return set_receiver(data, words_[2], words_[3], words_[4])
        if words_[1] == "add" and len(words_) == 5:
            return set_receiver(data, words_[2], words_[3], words_[4], add=True)
        if words_[1] == "drop" and len(words_) == 4:
            return set_receiver(data, words_[2], words_[3], None, drop=True)
    if words_[:1] == ["dry-run"] and len(words_) in (2, 3):
        return dry_run(root, data, words_[1], words_[2] if len(words_) == 3 else None)
    print(__doc__.split("USAGE:")[1].split("Stdlib")[0].rstrip())
    return 2


if __name__ == "__main__":
    sys.exit(main())
