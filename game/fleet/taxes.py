#!/usr/bin/env python3
"""taxes.py -- keeps each pilot's weekly tax apart, so that no run and no hour reads it as a loss.

WHAT: the game takes a tax from every pilot's wallet once a week, in one moment. A run in flight at that moment showed it as a
      loss, and the loss stop closed paying routes on it (2026-11-16: 38 runs, -149,123 cr). This script asks the game for each
      pilot's latest tax statement (`get_tax_estimate`, a reading command) and keeps what was paid in two places:
        data/fleet/taxes.json    {pilot: [[the assessment's time, credits paid], ...]}: the record. routes.py `earned` and the
                                 dispatcher's loss stop give a run back the tax taken while it flew (in_run), so fill.py,
                                 hive.py, the store and a route's measured figure all read the run without it.
        data/fleet/onetime.json  one row [time, pilot, "Weekly tax", -paid]: the collector keeps every row of that file out
                                 of the steady money per hour.
RULES:
  - It only reads in the game: no ship moves, nothing is paid.
  - One entry per pilot and assessment: a second pass books nothing twice.
  - A pass first asks one pilot; only when its last assessment is newer than the newest one on record are all pilots asked.
  - A pilot whose statement cannot be read is named and left for the next pass.
  - The record's place can be named in the environment (FLEET_TAXES): the unit tests point it away from the fleet's own.
WHY:  a figure that carries a tax is no figure of the route (requests.log ENT-147, errors.log ENT-056).

From another script:
  taxes.in_run(row)                 credits of weekly tax taken from the row's pilot while its run was in flight (0 for most)
  taxes.paid(pilot, start, end)     the same for any span of epoch seconds

USAGE:
  taxes.py                 one pass (the five-minute job runs it)
  taxes.py --all           ask every pilot, whatever the record says
  taxes.py --dry-run       print what would be booked, write nothing
  taxes.py show            the record: per assessment the pilots and the credits
  --data <dir>             the unit's data folder (default: the fleet's)

Stdlib only. ASCII only.
"""

import calendar
import fcntl
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the data folder
import gate                                       # noqa: E402  the engine's door

TITLE = "Weekly tax"
SLACK = 120                    # seconds after a run's end in which its last wallet reading may still fall
STATEMENT = re.compile(r"Latest completed statement: assessed (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})[^;]*; owed [\d,]+cr; paid ([\d,]+)cr")
CACHE = {"path": None, "stamp": None, "by_pilot": {}}


def record_file(data=None):
    """The record's path: under the data folder named, else where FLEET_TAXES points, else in the fleet's data folder."""
    if data:
        return os.path.join(data, "fleet", "taxes.json")
    return os.environ.get("FLEET_TAXES") or os.path.join(division.DATA, "fleet", "taxes.json")


def statement(text):
    """(epoch of the assessment, credits paid) from the answer to get_tax_estimate; None when it names no completed statement."""
    found = STATEMENT.search(text or "")
    if not found:
        return None
    return calendar.timegm(time.strptime(found.group(1), "%Y-%m-%dT%H:%M:%S")), int(found.group(2).replace(",", ""))


def load(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, ValueError):
        return default
    return value if isinstance(value, type(default)) else default


def by_pilot(data=None):
    """{pilot: [(epoch, credits paid), ...]} of the record, read again only when the file changed."""
    path = record_file(data)
    try:
        stamp = os.stat(path).st_mtime_ns
    except OSError:
        return {}
    if CACHE["path"] != path or CACHE["stamp"] != stamp:
        found = {}
        for pilot, entries in load(path, {}).items():
            found[pilot] = [(int(e[0]), e[1]) for e in entries if isinstance(e, list) and len(e) == 2 and all(isinstance(v, (int, float)) for v in e)]
        CACHE.update(path=path, stamp=stamp, by_pilot=found)
    return CACHE["by_pilot"]


def paid(pilot, start, end, data=None):
    """Credits of weekly tax taken from the pilot between two epoch seconds (both counted)."""
    return sum(amount for at, amount in by_pilot(data).get(pilot, ()) if start <= at <= end)


def in_run(row, data=None):
    """Credits of weekly tax taken from the row's pilot while its run was in flight: from its start to its end and the
    seconds its last wallet reading may take. 0 for a row without a start."""
    try:
        start = calendar.timegm(time.strptime(str(row.get("started"))[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0
    minutes = row.get("minutes") if isinstance(row.get("minutes"), (int, float)) else 0
    return paid(row.get("pilot"), start, start + minutes * 60 + SLACK, data)


def ask(pilot):
    """The text of the pilot's tax statement, or '' when the engine did not answer."""
    try:
        status, answer = gate.call("post", "/accounts/%s/raw" % gate.q(pilot), {"toolGroup": "spacemolt", "action": "get_tax_estimate", "params": {}}, timeout=90)
    except Exception:                               # the engine is away: the next pass asks again
        return ""
    if status != 200:
        return ""
    try:
        body = json.loads(answer, strict=False)
    except ValueError:
        return answer
    return str(body.get("result") or "") if isinstance(body, dict) else ""


def write(path, value):
    tmp = "%s.%d.tmp" % (path, os.getpid())
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(value, handle, separators=(",", ":"))
    os.replace(tmp, path)


def book(data, found, dry_run=False):
    """Put {pilot: (epoch, paid)} into the record and into onetime.json, each entry once: [(pilot, epoch, paid)] added."""
    path = record_file(data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    added = []
    with open(path + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        record = load(path, {})
        for pilot, (at, amount) in sorted(found.items()):
            entries = record.setdefault(pilot, [])
            if amount > 0 and not any(isinstance(e, list) and e and e[0] == at for e in entries):
                entries.append([at, amount])
                added.append((pilot, at, amount))
        if added and not dry_run:
            write(path, record)
    if added and not dry_run:
        once = os.path.join(os.path.dirname(path), "onetime.json")
        with open(once + ".lock", "w") as lock:                      # the lock the runners and gate.py book under
            fcntl.flock(lock, fcntl.LOCK_EX)
            rows = load(once, [])
            have = {(row[1], row[0]) for row in rows if isinstance(row, list) and len(row) == 4 and row[2] == TITLE}
            rows += [[at, pilot, TITLE, -amount] for pilot, at, amount in added if (pilot, at) not in have]
            rows.sort(key=lambda row: row[0] if isinstance(row, list) and row and isinstance(row[0], (int, float)) else 0)
            write(once, rows[-8000:])
    return added


def collect(data, pilots, everyone=False, dry_run=False, asker=ask):
    """One pass: (entries added, pilots whose statement could not be read, whether all were asked)."""
    newest = max((at for entries in by_pilot(data).values() for at, _amount in entries), default=0)
    if not everyone and pilots:
        first = statement(asker(pilots[0]))
        if first is not None and first[0] <= newest:
            return [], [], False
    with ThreadPoolExecutor(max_workers=6) as pool:
        texts = dict(zip(pilots, pool.map(asker, pilots)))
    found, unread = {}, []
    for pilot in pilots:
        got = statement(texts.get(pilot))
        if got is None:
            unread.append(pilot)
        else:
            found[pilot] = got
    return book(data, found, dry_run), unread, True


def show(data):
    by_time = {}
    for pilot, entries in by_pilot(data).items():
        for at, amount in entries:
            entry = by_time.setdefault(at, [0, 0])
            entry[0] += 1
            entry[1] += amount
    print("TAXES | %s | the weekly tax per assessment; kept out of the steady money and of every run's credits" % record_file(data))
    for at, (count, total) in sorted(by_time.items()):
        print("  assessed %s UTC: %d pilots paid %s cr" % (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(at)), count, format(int(total), ",")))
    if not by_time:
        print("  no assessment on record")
    return 0


def main(argv):
    data = argv[argv.index("--data") + 1] if "--data" in argv else division.DATA
    if "show" in argv:
        return show(data)
    try:
        with open(os.path.join(data, "fleet", "fleet.json"), encoding="utf-8") as handle:
            pilots = sorted(ship.get("name") for ship in json.load(handle).get("ships") or [] if isinstance(ship, dict) and ship.get("name"))
    except (OSError, ValueError):
        print("taxes: no fleet file in %s" % data)
        return 1
    added, unread, asked = collect(data, pilots, everyone="--all" in argv, dry_run="--dry-run" in argv)
    if not asked:
        print("taxes: no assessment since the newest one on record; one pilot asked")
        return 0
    when = sorted({at for _pilot, at, _amount in added})
    print("taxes: %d pilots asked | %s %d entries, %s cr in all%s | statements not read: %d%s" % (
        len(pilots), "would book" if "--dry-run" in argv else "booked", len(added), format(sum(a for _p, _t, a in added), ","),
        " (assessed %s UTC)" % ", ".join(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t)) for t in when) if when else "",
        len(unread), " (%s ...)" % ", ".join(unread[:3]) if unread else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
