#!/usr/bin/env python3
"""ledger.py -- keep the fleet's books: what we own and where it lies, and how every order book moved.

WHAT: the service `ledger` runs it. Every 30 s it does two things.
        storage   reads the personal storage of the next four pilots at every
                  station where they store goods (storage `view`, a call that
                  only reads and answers from anywhere) and writes
                  data/stock/storage.json: per pilot and station, and the
                  totals per station and per division, with what the ships
                  carry in their holds. Every pilot is read about once in 50
                  minutes by that rotation. On top of it, each pass reads up
                  to three pilots that wait on the book: a pilot without an
                  order for 45 s whose last run ended after its reading (the
                  dispatcher closes a route with `requires.stored` to it
                  until the storage is read again), the longest wait first.
                  The faction's storage stands in the book as the entry and
                  member `Faction`, from the faction's own reading
                  (factionbook.py: empire.json, every 15 minutes; no call).
        market    looks at the order books our ships saved (data/market/) and,
                  for every book that was read again, appends one line per
                  item whose best bid or best ask changed to
                  data/market/history.jsonl.
      `show` prints the books for a member or the fleet.
RULES:
  - It reads only. It moves no ship, buys and sells nothing.
  - A pilot it could not read keeps its last reading and its error; a total
    never counts a pilot twice. A pilot not read since it was signed in again
    (an engine start, a resume) keeps its last whole reading, with the time it
    was read, until its turn reads it again.
  - A pilot leaves the book only when it left the fleet: the fleet file, read
    while the engine answers, has not named it (nor its list `away`) for
    LEAVE_AFTER seconds on end while it named at least LEAVE_SHARE of the
    book's pilots, or for LEAVE_LONG seconds whatever it named; a flagship
    never. A file written while the engine signs its pilots in names a part
    of the fleet: nobody leaves on it (2026-11-21 19:20 UTC: a file of 5 ships
    took 241 pilots out of the book and the iron chain read 33,107 of 250,690).
  - The book says how whole it is (`whole`): the pilots of the fleet, how many
    it holds a reading of, how many were read since their last sign in or the
    engine's start (fleet.json, presence.jsonl), how many it keeps from before,
    the ones it lacks and the oldest reading. It is whole when it holds a
    reading of WHOLE_SHARE of the fleet's pilots; decides() gives a reader
    that answer and its words (supply.py duty adds no source on a book that is
    not whole).
  - The files are the unit's data, never the repository's.
  - No ship waits on the book (rule F32): a free pilot is read within about a
    minute or two of the end of its run; a reading that failed is tried again
    after two minutes, not every pass.
WHY:  9,000 units of ore lay in storage unseen, a second purchase was made
      for a mission that hands its goods out, and a price that held for one
      read was taken for a trade. Nobody can plan from goods and prices no
      file holds.

USAGE:
  ledger.py                   run forever (the service `ledger`)
  ledger.py --once            one pass over every pilot and every book, then stop (about ten minutes)
  ledger.py show [<Member>|all] [--item <item id>]
                              the stock of a member's ships (default: the member this shell belongs to)
  ledger.py prices <item id> [--base <base id>] [--last N]
                              the last N moves (default 20) of an item's best bid and ask
  --data <dir>                the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402
import factionbook                                # noqa: E402  the faction's storage as the book's entry `Faction` (requests ENT-267)

GATE = "http://172.30.0.32:7580"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
EVERY = 30                   # seconds between two passes
PER_PASS = 4                 # pilots read per pass by the rotation: 246 ships in about 50 minutes
DUE_PER_PASS = 3             # and on top of them the pilots that wait on the book (due), at most this many a pass
RETRY = 120                  # seconds until a waiting pilot whose reading failed is tried again
WAIT = 45                    # a pilot waits on the book when the dispatcher (a pass every 30 s) did not send it on within this
HOME = "central_nexus"       # any station answers with the list of the pilot's storage locations
LEAVE_AFTER = 3600           # seconds on end a pilot stands outside a fleet file that names the fleet before it leaves the book
LEAVE_SHARE = 0.9            # a fleet file names the fleet when it names this share of the book's pilots (fewer: a fleet signing in)
LEAVE_LONG = 86400           # seconds on end outside every fleet file after which a pilot leaves whatever the file named
WHOLE_SHARE = 0.95           # the book is whole when it holds a reading of this share of the fleet's pilots
PRESENCE_TAIL = 1_000_000    # bytes read from the end of fleet/presence.jsonl for the pilots' last sign in


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name("%s.%d.tmp" % (path.name, os.getpid()))
    tmp.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, path)


def now_text():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def view(pilot, station):
    """The pilot's storage at a station: ({item: quantity}, [other base ids], error)."""
    body = {"toolGroup": "spacemolt_storage", "action": "view", "params": {"station_id": station}}
    request = urllib.request.Request(GATE + "/accounts/%s/raw" % urllib.parse.quote(pilot, safe=""), data=json.dumps(body).encode(),
                                     method="POST", headers={"Content-Type": "application/json"})
    try:
        with OPENER.open(request, timeout=60) as answer:
            found = json.loads(answer.read().decode("utf-8", "replace") or "{}")
    except (urllib.error.URLError, OSError, ValueError) as error:
        return None, [], "%s: %s" % (type(error).__name__, str(error)[:120])
    content = found.get("structuredContent") if isinstance(found, dict) else None
    if not isinstance(content, dict) or "items" not in content:
        return None, [], str((content or {}).get("error") or found.get("error") or found)[:200]
    items = {str(i.get("item_id")): int(i.get("quantity") or 0) for i in content.get("items") or [] if isinstance(i, dict) and i.get("item_id")}
    return items, [str(l.get("base_id")) for l in content.get("locations") or [] if isinstance(l, dict) and l.get("base_id")], ""


def read_pilot(pilot, look=view, pause=1.0):
    """{read_at, stations: {base: {item: qty}}} or {read_at, error} for one pilot."""
    items, bases, error = look(pilot, HOME)
    if items is None:
        return {"read_at": now_text(), "error": error}
    stations = {HOME: items} if items else {}
    for base in bases:
        if base == HOME:
            continue
        time.sleep(pause)
        more, _bases, error = look(pilot, base)
        if more is None:
            return {"read_at": now_text(), "error": "%s: %s" % (base, error)}
        if more:
            stations[base] = more
    return {"read_at": now_text(), "stations": stations}


def totals(pilots, data):
    """Totals per station and per member's division, and the holds per member, from the pilots' last good readings."""
    by_station, by_member = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for pilot, entry in pilots.items():
        for base, items in (entry.get("stations") or {}).items():
            for item, quantity in items.items():
                by_station[base][item] += quantity
                by_member[entry.get("member") or division.owner(pilot, data)][base][item] += quantity      # `Faction`: the faction's storage
    holds = defaultdict(lambda: defaultdict(int))
    folder = Path(data) / "fleet" / "ships"
    for path in folder.glob("*.json") if folder.is_dir() else []:
        ship = read_json(path, {})
        for row in ship.get("cargo") or []:
            item = (row.get("item") or row.get("item_id")) if isinstance(row, dict) else None      # the ship files write `item`; the engine's own answer `item_id`
            if item and ship.get("name"):
                holds[division.owner(ship["name"], data)][str(item)] += int(row.get("quantity") or 0)
    plain = lambda d: json.loads(json.dumps(d))
    return {"by_station": plain(by_station), "by_member": plain(by_member), "holds_by_member": plain(holds)}


def save_storage(book, data):
    book["updated_at"] = now_text()
    book["totals"] = totals(book["pilots"], data)
    book["whole"] = wholeness(book, data, book.get("whole"))
    write_json(Path(data) / "stock" / "storage.json", book)


def signed_in(data, names, start=0):
    """{pilot: seconds since the epoch of its last sign in}: the engine's start (`start`) or, later, the line of
    fleet/presence.jsonl that the collector wrote when the engine listed the pilot again (`sign` 1); 0 when neither."""
    out = {name: start for name in names}
    try:
        with open(Path(data) / "fleet" / "presence.jsonl", "rb") as handle:
            handle.seek(0, os.SEEK_END)
            handle.seek(max(0, handle.tell() - PRESENCE_TAIL))
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return out
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue                                         # the first line of the tail may be cut
        if isinstance(row, dict) and row.get("sign") == 1 and row.get("pilot") in out and isinstance(row.get("at"), (int, float)):
            out[row["pilot"]] = max(out[row["pilot"]], int(row["at"]))
    return out


def wholeness(book, data, before=None):
    """How whole the book is (its entry `whole`): the fleet's pilots (the fleet file's ships and `away`, and every pilot the
    book keeps; the faction's entry is no pilot), how many it holds a reading of, how many of those were read since the
    pilot's last sign in or the engine's start (fresh) and how many it keeps from before, the pilots it lacks, the oldest
    reading it carries, and `whole`: a reading of WHOLE_SHARE of the pilots at least. `before`: the entry of the pass
    before, whose engine start stands in while the fleet file does not say it (the collector holds a sign-in back)."""
    pilots = book.get("pilots") or {}
    names = sorted((set(pilots) | (roster(data) or set())) - {factionbook.MEMBER})
    engine = read_json(Path(data) / "fleet" / "fleet.json", {}).get("engine") or {}
    started = str(engine.get("started_at") or (before or {}).get("engine_started") or "")
    since = signed_in(data, names, stamp(started))
    held, fresh, missing, read = 0, 0, [], []
    for name in names:
        entry = pilots.get(name) or {}
        if not isinstance(entry.get("stations"), dict):
            missing.append(name)
            continue
        held += 1
        fresh += 1 if stamp(entry.get("read_at")) >= since.get(name, 0) else 0
        read.append(str(entry.get("read_at") or ""))
    last = max(since.values(), default=0)
    return {"pilots": len(names), "held": held, "fresh": fresh, "kept": held - fresh, "missing": len(missing), "missing_names": missing[:12],
            "oldest": min(read, default=""), "engine_started": started, "signed_in": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(last)) if last else "",
            "whole": bool(names) and held >= WHOLE_SHARE * len(names)}


def words(whole):
    """One line of how whole a book's entry `whole` says it is."""
    if not isinstance(whole, dict) or "whole" not in whole:
        return "how whole it is not said (a book written before the ledger said it)"
    text = "%d of %d pilots held, %d read since their sign in, %d kept from before, the oldest reading %s" % (
        whole.get("held") or 0, whole.get("pilots") or 0, whole.get("fresh") or 0, whole.get("kept") or 0, whole.get("oldest") or "--")
    if whole.get("missing"):
        text += "; no reading of %d: %s%s" % (whole["missing"], ", ".join(whole.get("missing_names") or []), " ..." if whole["missing"] > len(whole.get("missing_names") or []) else "")
    return text + ("" if whole.get("whole") else "; NOT WHOLE (below %d percent of the fleet)" % round(WHOLE_SHARE * 100))


def decides(whole):
    """(True when a reader may decide on the book, its words) for a book's entry `whole`. A book that does not say is
    judged as it stands, as before the ledger said it."""
    return (not isinstance(whole, dict) or "whole" not in whole or bool(whole["whole"])), words(whole)


def book_whole(data):
    """The entry `whole` of the storage book in the data folder; {} when there is no book or it does not say."""
    found = read_json(Path(data) / "stock" / "storage.json", {})
    whole = found.get("whole") if isinstance(found, dict) else None
    return whole if isinstance(whole, dict) else {}


def price_row(item):
    return [item.get("best_buy") or 0, item.get("best_buy_qty", item.get("buy_quantity")) or 0,
            item.get("best_sell") or 0, item.get("best_sell_qty", item.get("sell_quantity")) or 0]


def market_moves(book, last):
    """(lines to append, the new state of this base) for one saved order book against the state before."""
    state, lines = {}, []
    for item in book.get("items") or []:
        if not isinstance(item, dict) or not item.get("item_id"):
            continue
        row = price_row(item)
        if not (row[0] or row[2]):
            continue
        state[item["item_id"]] = row
        before = (last or {}).get(item["item_id"])
        if before is None or before[0] != row[0] or before[2] != row[2]:
            lines.append({"t": book.get("read_at"), "base": book.get("base"), "item": item["item_id"], "bid": row[0], "bid_qty": row[1], "ask": row[2], "ask_qty": row[3]})
    for gone in sorted(set(last or {}) - set(state)):
        lines.append({"t": book.get("read_at"), "base": book.get("base"), "item": gone, "bid": 0, "bid_qty": 0, "ask": 0, "ask_qty": 0})
    return lines, state


def market_pass(data, seen):
    """Append the moves of every order book read again since the last pass; the number of lines written."""
    folder = Path(data) / "market"
    state_path = folder / "history.state.json"
    state, wrote = read_json(state_path, {}), 0
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        if path.name.startswith("history."):
            continue
        try:
            stamp = path.stat().st_mtime_ns
        except OSError:
            continue
        if seen.get(path.name) == stamp:
            continue
        seen[path.name] = stamp
        book = read_json(path, {})
        if not book.get("base") or book.get("read_at") == (state.get(book["base"]) or {}).get("read_at"):
            continue
        lines, items = market_moves(book, (state.get(book["base"]) or {}).get("items"))
        state[book["base"]] = {"read_at": book.get("read_at"), "items": items}
        if lines:
            with open(folder / "history.jsonl", "a", encoding="utf-8") as handle:
                handle.write("".join(json.dumps(line, separators=(",", ":")) + "\n" for line in lines))
            wrote += len(lines)
        write_json(state_path, state)
    return wrote


def pilots_of(data):
    ships = read_json(Path(data) / "fleet" / "fleet.json", {}).get("ships") or []
    return sorted(s["name"] for s in ships if isinstance(s, dict) and s.get("name") and s.get("status") == "connected")


def stamp(text):
    """Seconds since the epoch of a time now_text() wrote, or 0."""
    try:
        return calendar.timegm(time.strptime(str(text)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0


def due(names, book, data, now=None):
    """The pilots that wait on the book, the longest wait first: a pilot without a fresh order file (no run flies it,
    no hand holds it) whose last run ended after its storage was read (the run's log, data/routes/logs/<pilot>.log,
    is written last when the run ends). The dispatcher closes every route with `requires.stored` to such a pilot
    until the storage is read again. A pilot between two runs is not read: the dispatcher sends it on within WAIT
    seconds. A reading that failed is tried again after RETRY seconds."""
    now = time.time() if now is None else now
    waits = []
    for pilot in names:
        try:
            ended = (Path(data) / "routes" / "logs" / (pilot + ".log")).stat().st_mtime
        except OSError:
            continue                                             # never flew a run: the rotation reads it
        entry = (book.get("pilots") or {}).get(pilot) or {}
        if now - ended < WAIT or ended <= stamp(entry.get("read_at")) or now - stamp(entry.get("error_at")) < RETRY:
            continue
        if division.order_of(pilot, data, now):
            continue
        waits.append((ended, pilot))
    return [pilot for _ended, pilot in sorted(waits)]


def batch_of(names, turn, book, data, now=None):
    """(The pilots to read this pass, how many of them the rotation gave): the next PER_PASS of the rotation, and in
    front of them up to DUE_PER_PASS pilots that wait on the book. The rotation never loses its turn."""
    turns = [names[(turn + n) % len(names)] for n in range(min(PER_PASS, len(names)))]
    first = [pilot for pilot in due(names, book, data, now) if pilot not in turns][:DUE_PER_PASS]
    return first + turns, len(turns)


def roster(data):
    """Every pilot the fleet file names, connected or not, with the pilots it holds signed out (`away`); None while the
    engine does not answer or the file names nobody (then nobody leaves the book: a pilot that reconnects for a moment
    still owns what it stored)."""
    fleet = read_json(Path(data) / "fleet" / "fleet.json", {})
    names = {s["name"] for s in (fleet.get("ships") or []) + (fleet.get("away") or []) if isinstance(s, dict) and s.get("name")}
    return names if names and (fleet.get("engine") or {}).get("ok", True) else None


def leave(book, data, now=None):
    """Take the pilots out of the book that left the fleet; the names taken out. The book's `unlisted` keeps, per pilot the
    fleet file leaves out, the first pass that did: one leaves after LEAVE_AFTER seconds on end while the file names
    LEAVE_SHARE of the book's pilots, or after LEAVE_LONG whatever it names. A file that is no roster (the engine away,
    a sign-in held back, nobody named) takes nobody out and ends every count: the fleet file read next starts them anew.
    A flagship and the faction's entry never leave."""
    now = time.time() if now is None else now
    known = roster(data)
    clocks = book.setdefault("unlisted", {})
    if known is None:
        clocks.clear()
        return []
    stays = known | set(division.flagships(data)) | {factionbook.MEMBER}
    pilots = [name for name in book["pilots"] if name != factionbook.MEMBER]
    named = sum(1 for name in pilots if name in known) >= LEAVE_SHARE * len(pilots)
    for name in [n for n in clocks if n in stays or n not in book["pilots"]]:
        del clocks[name]
    gone = []
    for name in sorted(set(pilots) - stays):
        out = now - (stamp(clocks.setdefault(name, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)))) or now)
        if out >= LEAVE_LONG or (named and out >= LEAVE_AFTER):
            gone.append(name)
    for name in gone:
        del book["pilots"][name]
        del clocks[name]
    return gone


def show(data, who, item):
    book = read_json(Path(data) / "stock" / "storage.json", {})
    if not book:
        sys.exit("no storage book yet: the service `ledger` writes data/stock/storage.json")
    pilots, total = book.get("pilots") or {}, book.get("totals") or {}
    read = [p for p, e in pilots.items() if "stations" in e]
    print("STOCK | written %s | pilots read %d, with an error %d | oldest reading %s" % (
        book.get("updated_at"), len(read), len(pilots) - len(read), min((pilots[p]["read_at"] for p in read), default="--")))
    print("WHOLE | %s" % words(book.get("whole")))
    members = sorted(total.get("by_member") or {}) if who == "all" else [who]
    for member in members:
        print("%s: storage" % member)
        for base, items in sorted((total.get("by_member") or {}).get(member, {}).items()):
            rows = sorted(((q, i) for i, q in items.items() if not item or i == item), reverse=True)
            if rows:
                print("  %-34s %s" % (base, ", ".join("%s %s" % (i, format(q, ",")) for q, i in rows[:14])))
        hold = sorted(((q, i) for i, q in ((total.get("holds_by_member") or {}).get(member) or {}).items() if not item or i == item), reverse=True)
        print("  %-34s %s" % ("in the holds", ", ".join("%s %s" % (i, format(q, ",")) for q, i in hold[:14]) or "nothing"))
    if who == "all":
        print("FLEET: storage by station")
        for base, items in sorted((total.get("by_station") or {}).items()):
            rows = sorted(((q, i) for i, q in items.items() if not item or i == item), reverse=True)
            if rows:
                print("  %-34s %s" % (base, ", ".join("%s %s" % (i, format(q, ",")) for q, i in rows[:14])))


def prices(data, item, base, last):
    rows = []
    try:
        with open(Path(data) / "market" / "history.jsonl", encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get("item") == item and (not base or row.get("base") == base):
                    rows.append(row)
    except OSError:
        sys.exit("no price history yet: the service `ledger` writes data/market/history.jsonl")
    for row in rows[-last:]:
        print("%s  %-34s bid %6s x %-6s ask %6s x %s" % (row.get("t"), row.get("base"), row.get("bid"), row.get("bid_qty"), row.get("ask"), row.get("ask_qty")))
    print("%d move(s) of %s on record%s" % (len(rows), item, (" at " + base) if base else ""))


def main():
    args = sys.argv[1:]
    data = args[args.index("--data") + 1] if "--data" in args else division.DATA
    if args and args[0] == "show":
        rest = [a for n, a in enumerate(args[1:]) if not a.startswith("--") and args[n] not in ("--data", "--item")]
        who = rest[0] if rest else division.member()[1]
        show(data, "all" if who == "all" else who.capitalize(), args[args.index("--item") + 1] if "--item" in args else "")
        return 0
    if args and args[0] == "prices" and len(args) > 1:
        prices(data, args[1], args[args.index("--base") + 1] if "--base" in args else "", int(args[args.index("--last") + 1]) if "--last" in args else 20)
        return 0
    if [a for a in args if a not in ("--once", "--data", data)]:
        sys.exit(__doc__)
    kind, name = division.member()
    if not (kind == "service" or name == "Unity"):
        sys.exit("REFUSED: the ledger's passes are the service's; read the books with `ledger.py show` and `ledger.py prices`")
    once = "--once" in args
    book = read_json(Path(data) / "stock" / "storage.json", {})
    book = {"what": "Personal station storage of every pilot of ours, per station; totals per station and per member's division; the holds",
            "source": "storage view with station_id, read through each pilot (read only); the entry Faction from empire.json (factionbook.py)",
            "pilots": book.get("pilots") or {}, "unlisted": book.get("unlisted") or {}, "whole": book.get("whole") or {}}      # a restart keeps the counts
    seen, turn = {}, 0
    while True:
        try:
            wrote = market_pass(data, seen)
            names = pilots_of(data)
            leave(book, data)
            faction = factionbook.put(book, data)            # the faction's storage, from its own reading: no call
            batch, step = (names, len(names)) if once or not names else batch_of(names, turn, book, data)
            turn += step
            for pilot in batch:
                if (Path(data) / "fleet" / "STOP").exists():
                    break
                entry = read_pilot(pilot)
                if "error" in entry and "stations" in (book["pilots"].get(pilot) or {}):
                    entry = dict(book["pilots"][pilot], error=entry["error"], error_at=entry["read_at"])
                book["pilots"][pilot] = entry
                time.sleep(1)
            if batch or faction:
                save_storage(book, data)
            if wrote or once:
                print(now_text(), "market moves written: %d | pilots read this pass: %d" % (wrote, len(batch)), flush=True)
        except Exception as error:                               # a bad file or a lost gate must not end the service
            print(now_text(), "pass failed: %s: %s" % (type(error).__name__, error), flush=True)
        if once:
            return 0
        time.sleep(EVERY)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
