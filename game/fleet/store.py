#!/usr/bin/env python3
"""store.py -- keeps the fleet's history in one SQLite file: the runs, the price moves and the census readings, with their sums by hour and by day.

WHAT: the service `store` runs it. Every minute it reads the new whole lines of three records of the
      unit's data folder and writes them into <data>/store/live.db:
        routes/runs.jsonl       -> runs      one row a run           sums: route_hour  (runs, minutes, credits)
        market/history.jsonl    -> moves     one row a price move    sums: market_hour (lowest and highest bid, ask)
        wildlife/history.jsonl  -> readings  one row a field or herd sums: reading_day (first and last count)
      After a pass that wrote, and at least every five minutes, it publishes a copy, <data>/store/read.db,
      which every other program reads; the first pass of a UTC day also writes
      <data>/store/backup/collective-<date>.db (the five newest stay).
RULES:
  - This service is the only writer of live.db; no other program opens that file. Two containers share
    the data folder, and file locks, appends and live SQLite files do not work between them (services
    README, "Data"). Readers open the copy through connect(): read-only and immutable.
  - One writer at a time: <data>/store/writer.lease, created with O_EXCL and renewed every pass. `once`
    is refused while a serve holds a lease renewed in the last five minutes.
  - A pass reads each record from where the last pass stopped (table cursor) and writes its rows, its
    sums and its new place in one transaction. A last line without its newline waits for the next pass.
  - A record shorter than its place, or whose first line changed, was cut by the keeper
    (scripts/data-keeper.py): it is read again from its start. Every row has a key and goes in with
    INSERT OR IGNORE, so a line read twice is one row: a run by (pilot, route, started), a price move by
    (base, item, t), a reading by (system, poi, what, t).
  - Sums are recomputed from the raw rows, only for the hours (days) that got new rows. Raw rows older
    than --keep-days are deleted by whole hours (readings by whole days); their sums stay, and a line of
    such an hour that turns up again is not taken in: those sums are final.
  - A run counts for credits and read minutes only when it read a wallet (credits_before and
    credits_after above 0, no note `wallet not read`); its credits are its steady credits, delta minus
    one_time. Credits per ship-hour = 60 * credits / read minutes.
  - A herd its place's census no longer lists stands at 0 in that census (once). A bid or ask of 0 is no
    price: it is left out of the lowest and highest of its hour.
  - A bad line is skipped and counted; a failed pass is printed and tried again at the next tick.
WHY:  the keeper cuts the records to their newest lines, so what a route earned last week was lost, and
      every reader parsed megabytes of JSON again for each answer. Here the history stays as sums.

From another program (the module's functions):
  conn = store.connect(data)            the read copy, or None while there is none
  store.route_rates(conn, since_epoch)  {route: (runs, read minutes, credits, one_time, credits per ship-hour or None)}

USAGE:
  store.py serve [--every 60]     run forever (the service `store`)
  store.py once                   one pass, then stop
  store.py status                 from the read copy: rows and newest row of each table, age of the copy
  --data <dir>                    the unit's data folder (default /srv/collective/data)
  --keep-days N                   days of raw rows kept (default 7)

Stdlib only. ASCII only.
"""

import argparse
import calendar
import hashlib
import json
import os
import signal
import sqlite3
import sys
import time
import urllib.parse
from pathlib import Path

EVERY = 60                     # seconds between two passes
KEEP_DAYS = 7                  # days of raw rows kept; the sums stay for good
PUBLISH = 300                  # seconds: the read copy is renewed at least this often
BACKUPS = 5                    # daily backups kept
LEASE_FRESH = 300              # seconds: a writer lease renewed this recently belongs to a living writer
HEAD = 65536                   # bytes of a record's first line that mark it (a cut changes its first line)
HOUR, DAY = 3600, 86400

SCHEMA = """
CREATE TABLE IF NOT EXISTS cursor (record TEXT PRIMARY KEY, offset INTEGER NOT NULL, head TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value);
CREATE TABLE IF NOT EXISTS runs (pilot TEXT NOT NULL, route TEXT NOT NULL, kind TEXT, started TEXT NOT NULL,
  t INTEGER NOT NULL, minutes REAL, credits REAL, one_time REAL, readable INTEGER, row TEXT,
  PRIMARY KEY (pilot, route, started));
CREATE INDEX IF NOT EXISTS runs_route ON runs (route, t);
CREATE INDEX IF NOT EXISTS runs_t ON runs (t);
CREATE TABLE IF NOT EXISTS moves (base TEXT NOT NULL, item TEXT NOT NULL, t INTEGER NOT NULL,
  bid REAL, bid_qty REAL, ask REAL, ask_qty REAL, PRIMARY KEY (base, item, t));
CREATE INDEX IF NOT EXISTS moves_t ON moves (t);
CREATE TABLE IF NOT EXISTS readings (system TEXT NOT NULL, poi TEXT NOT NULL, what TEXT NOT NULL, kind TEXT,
  amount REAL, t INTEGER NOT NULL, PRIMARY KEY (system, poi, what, t));
CREATE INDEX IF NOT EXISTS readings_place ON readings (system, poi, kind, t);
CREATE INDEX IF NOT EXISTS readings_t ON readings (t);
CREATE TABLE IF NOT EXISTS route_hour (route TEXT NOT NULL, hour INTEGER NOT NULL, runs INTEGER, minutes REAL,
  read_minutes REAL, credits REAL, one_time REAL, PRIMARY KEY (route, hour));
CREATE TABLE IF NOT EXISTS market_hour (base TEXT NOT NULL, item TEXT NOT NULL, hour INTEGER NOT NULL,
  bid_lo REAL, bid_hi REAL, ask_lo REAL, ask_hi REAL, moves INTEGER, PRIMARY KEY (base, item, hour));
CREATE TABLE IF NOT EXISTS reading_day (system TEXT NOT NULL, poi TEXT NOT NULL, what TEXT NOT NULL, kind TEXT,
  day INTEGER NOT NULL, first REAL, last REAL, t_first INTEGER, t_last INTEGER, PRIMARY KEY (system, poi, what, day));
"""
NEWEST = (("runs", "t"), ("moves", "t"), ("readings", "t"), ("route_hour", "hour"), ("market_hour", "hour"), ("reading_day", "day"))


def stamp(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def epoch(text):
    """Seconds of a UTC stamp 'YYYY-MM-DDTHH:MM:SSZ'; ValueError for anything else."""
    if not isinstance(text, str) or len(text) < 19:
        raise ValueError("no time stamp")
    return calendar.timegm(time.strptime(text[:19], "%Y-%m-%dT%H:%M:%S"))


def number(value):
    """An int or float as it is; None for anything else (a bool is no number)."""
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def text_of(row, key):
    value = row.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError("no %s" % key)
    return value


def readable(row):
    """True when the run read a wallet at both ends (game/fleet/routes.py, readable)."""
    before, after = number(row.get("credits_before")), number(row.get("credits_after"))
    notes = row.get("notes") if isinstance(row.get("notes"), list) else []
    return before is not None and after is not None and before > 0 and after > 0 and "wallet not read" not in notes


# ---- one line of each record -> raw rows; each returns (rows added, the sums it touched), None for a sealed hour

def take_run(conn, row, sealed, line):
    pilot, route, started = text_of(row, "pilot"), text_of(row, "route"), text_of(row, "started")
    t = epoch(started)
    if t < sealed:
        return None
    one_time = number(row.get("one_time")) or 0
    credits = (number(row.get("delta")) or 0) - one_time
    kind = row.get("kind") if isinstance(row.get("kind"), str) else None
    added = conn.execute("INSERT OR IGNORE INTO runs VALUES (?,?,?,?,?,?,?,?,?,?)", (
        pilot, route, kind, started, t, number(row.get("minutes")) or 0, credits, one_time,
        1 if readable(row) else 0, line)).rowcount
    return added, {(route, t - t % HOUR)} if added else set()


def take_move(conn, row, sealed, line):
    base, item = text_of(row, "base"), text_of(row, "item")
    t = epoch(row.get("t"))
    if t < sealed:
        return None
    added = conn.execute("INSERT OR IGNORE INTO moves VALUES (?,?,?,?,?,?,?)", (
        base, item, t, number(row.get("bid")), number(row.get("bid_qty")), number(row.get("ask")),
        number(row.get("ask_qty")))).rowcount
    return added, {(base, item, t - t % HOUR)} if added else set()


GONE = ("SELECT what FROM readings WHERE system = ? AND poi = ? AND kind = 'herd' AND amount > 0 AND t = "
        "(SELECT MAX(t) FROM readings WHERE system = ? AND poi = ? AND kind = 'herd' AND t < ?)")


def take_census(conn, row, sealed, line):
    system = text_of(row, "system")
    t = epoch(row.get("at"))
    deposits, herds = row.get("deposits"), row.get("herds")
    if not isinstance(deposits, dict) and not isinstance(herds, dict):
        raise ValueError("no deposits and no herds")
    if t < sealed:
        return None
    rows = []
    for kind, group in (("field", deposits), ("herd", herds)):
        for poi, counts in (group.items() if isinstance(group, dict) else ()):
            if not isinstance(counts, dict):
                continue
            poi = str(poi)
            for what, amount in counts.items():
                if number(amount) is not None:
                    rows.append((system, poi, str(what), kind, number(amount), t))
            if kind == "herd":                     # a herd the last census of this place counted and this one does not list
                for (what,) in conn.execute(GONE, (system, poi, system, poi, t)).fetchall():
                    if what not in counts:
                        rows.append((system, poi, what, "herd", 0, t))
    added, keys = 0, set()
    for one in rows:
        if conn.execute("INSERT OR IGNORE INTO readings VALUES (?,?,?,?,?,?)", one).rowcount:
            added += 1
            keys.add((one[0], one[1], one[2], t - t % DAY))
    return added, keys


# ---- sums, recomputed from the raw rows of one hour (day)

def sum_routes(conn, keys):
    for route, hour in keys:
        conn.execute(
            "INSERT OR REPLACE INTO route_hour SELECT route, ?, COUNT(*), SUM(minutes), "
            "SUM(CASE WHEN readable = 1 THEN minutes ELSE 0 END), SUM(CASE WHEN readable = 1 THEN credits ELSE 0 END), "
            "SUM(CASE WHEN readable = 1 THEN one_time ELSE 0 END) FROM runs WHERE route = ? AND t >= ? AND t < ? GROUP BY route",
            (hour, route, hour, hour + HOUR))


def sum_market(conn, keys):
    for base, item, hour in keys:
        conn.execute(
            "INSERT OR REPLACE INTO market_hour SELECT base, item, ?, MIN(CASE WHEN bid > 0 THEN bid END), "
            "MAX(CASE WHEN bid > 0 THEN bid END), MIN(CASE WHEN ask > 0 THEN ask END), MAX(CASE WHEN ask > 0 THEN ask END), "
            "COUNT(*) FROM moves WHERE base = ? AND item = ? AND t >= ? AND t < ? GROUP BY base, item",
            (hour, base, item, hour, hour + HOUR))


def sum_readings(conn, keys):
    for system, poi, what, day in keys:
        rows = conn.execute("SELECT kind, amount, t FROM readings WHERE system = ? AND poi = ? AND what = ? AND t >= ? AND t < ? "
                            "ORDER BY t", (system, poi, what, day, day + DAY)).fetchall()
        if rows:
            conn.execute("INSERT OR REPLACE INTO reading_day VALUES (?,?,?,?,?,?,?,?,?)",
                         (system, poi, what, rows[-1][0], day, rows[0][1], rows[-1][1], rows[0][2], rows[-1][2]))


RECORDS = (                    # record, its raw table, a line -> rows, the sums, the seal's step
    ("routes/runs.jsonl", "runs", take_run, sum_routes, HOUR),
    ("market/history.jsonl", "moves", take_move, sum_market, HOUR),
    ("wildlife/history.jsonl", "readings", take_census, sum_readings, DAY),
)


# ---- the database

def folder_of(data):
    return Path(data) / "store"


def open_live(data):
    """The writer's connection to live.db (WAL), with the tables made."""
    folder = folder_of(data)
    folder.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(folder / "live.db"), isolation_level=None, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(SCHEMA)
    return conn


def meta(conn, key, default=0):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else default


def mark(first):
    """What marks a record: the digest of its first line, when that line is whole."""
    return hashlib.sha256(first).hexdigest()[:32] if first.endswith(b"\n") else ""


def new_lines(path, offset, head):
    """(whole new lines as bytes, the offset after them, the record's mark, cut?) of one record."""
    with open(path, "rb") as handle:
        size = os.fstat(handle.fileno()).st_size
        now = mark(handle.readline(HEAD))
        cut = size < offset or bool(head and now and head != now)
        start = 0 if cut else offset
        handle.seek(start)
        chunk = handle.read()
    whole = chunk[:chunk.rfind(b"\n") + 1]
    return whole, start + len(whole), now, cut


def take_record(conn, data, name, table, take, add_up, step):
    """Read one record's new lines and write rows, sums and cursor in one transaction: {added, bad, old, cut}."""
    out = {"added": 0, "bad": 0, "old": 0, "cut": False, "moved": False}
    path = Path(data) / name
    if not path.is_file():
        return out
    row = conn.execute("SELECT offset, head FROM cursor WHERE record = ?", (name,)).fetchone()
    offset, head = row if row else (0, "")
    whole, end, now, cut = new_lines(path, offset, head)
    out["cut"] = cut
    if end == offset and now == head and not cut:
        return out
    sealed = meta(conn, "sealed." + table)
    touched = set()
    conn.execute("BEGIN IMMEDIATE")
    try:
        for raw in whole.split(b"\n"):
            if not raw.strip():
                continue
            try:
                line = raw.decode("utf-8").strip()
                parsed = json.loads(line)
                if not isinstance(parsed, dict):
                    raise ValueError("not an object")
                got = take(conn, parsed, sealed, line)
            except (ValueError, TypeError, KeyError, AttributeError, OverflowError):
                out["bad"] += 1
                continue
            if got is None:
                out["old"] += 1
                continue
            out["added"] += got[0]
            touched |= got[1]
        add_up(conn, touched)
        conn.execute("INSERT OR REPLACE INTO cursor VALUES (?,?,?)", (name, end, now))
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    out["moved"] = True
    return out


def prune(conn, now, keep_days):
    """Delete raw rows older than keep_days by whole hours (readings: days) and seal those hours: rows deleted."""
    gone = 0
    conn.execute("BEGIN IMMEDIATE")
    try:
        for _name, table, _take, _sum, step in RECORDS:
            cut = int(now - keep_days * DAY) // step * step
            if cut > meta(conn, "sealed." + table):
                gone += conn.execute("DELETE FROM %s WHERE t < ?" % table, (cut,)).rowcount
                conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", ("sealed." + table, cut))
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return gone


def copy_to(conn, target):
    """VACUUM INTO a temporary name beside target, then rename it into place."""
    target = Path(target)
    tmp = target.with_name(".%s.%d.tmp" % (target.name, os.getpid()))
    if tmp.exists():
        tmp.unlink()
    try:
        conn.execute("VACUUM INTO ?", (str(tmp),))
        handle = os.open(str(tmp), os.O_RDONLY)
        try:
            os.fsync(handle)
        finally:
            os.close(handle)
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()


def backup(conn, data, now, keep=BACKUPS):
    """The day's backup when it is not there yet; the `keep` newest stay. Its name, or None."""
    folder = folder_of(data) / "backup"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / ("collective-%s.db" % time.strftime("%Y-%m-%d", time.gmtime(now)))
    made = None
    if not target.exists():
        copy_to(conn, target)
        made = target.name
    for old in sorted(folder.glob("collective-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].db"))[:-keep]:
        old.unlink()
    return made


def one_pass(data, now=None, keep_days=KEEP_DAYS):
    """Read every record, prune, publish the copy when due, write the day's backup: what was done."""
    begun = time.time()
    now = begun if now is None else now
    out = {"records": {}, "pruned": 0, "published": False, "backup": None}
    conn = open_live(data)
    try:
        for name, table, take, add_up, step in RECORDS:
            try:
                out["records"][name] = take_record(conn, data, name, table, take, add_up, step)
            except (OSError, sqlite3.Error) as error:  # one record that fails never holds up the others
                out["records"][name] = {"added": 0, "bad": 0, "old": 0, "cut": False, "moved": False,
                                        "error": "%s: %s" % (type(error).__name__, error)}
        out["pruned"] = prune(conn, now, keep_days)
        wrote = out["pruned"] or any(r["added"] or r["moved"] for r in out["records"].values())
        read = folder_of(data) / "read.db"
        if wrote or not read.exists() or time.time() - read.stat().st_mtime >= PUBLISH:
            copy_to(conn, read)
            out["published"] = True
        out["backup"] = backup(conn, data, now)
    finally:
        conn.close()
    out["seconds"] = time.time() - begun
    return out


def said(out):
    """The pass's one line, or None when it wrote nothing."""
    records = out["records"]
    if not (out["pruned"] or out["backup"] or any(r["added"] or r["bad"] or r["cut"] or r.get("error") for r in records.values())):
        return None
    parts = []
    for name, r in records.items():
        part = "%s +%d" % (name, r["added"])
        extra = [w for w, on in (("cut: read from 0", r["cut"]), ("%d bad" % r["bad"], r["bad"]),
                                 ("%d sealed" % r["old"], r["old"]), ("failed: %s" % r.get("error"), r.get("error"))) if on]
        parts.append(part + (" (%s)" % ", ".join(extra) if extra else ""))
    if out["pruned"]:
        parts.append("%d old rows deleted" % out["pruned"])
    if out["backup"]:
        parts.append("backup %s" % out["backup"])
    return "%s | %s | %.2f s" % (" | ".join(parts), "copy published" if out["published"] else "copy not due", out["seconds"])


# ---- one writer

def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def lease(data, me=None):
    """Take or renew the writer's lease: None when it is ours, else who holds it."""
    folder = folder_of(data)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "writer.lease"
    me = me or "%s %d" % (os.uname().nodename, os.getpid())
    for _ in range(3):
        try:
            handle = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            try:
                holder, age = path.read_text(encoding="ascii").strip(), time.time() - path.stat().st_mtime
            except (OSError, UnicodeDecodeError):
                continue
            if holder == me:
                os.utime(str(path))
                return None
            host, _, pid = holder.partition(" ")
            dead = host == me.partition(" ")[0] and pid.isdigit() and not alive(int(pid))
            if age < LEASE_FRESH and not dead:
                return "%s, renewed %d s ago" % (holder, age)
            try:
                path.unlink()
            except FileNotFoundError:
                pass
            continue
        try:
            os.write(handle, me.encode("ascii"))
        finally:
            os.close(handle)
        return None
    return "the lease could not be taken"


def release(data, me=None):
    path = folder_of(data) / "writer.lease"
    me = me or "%s %d" % (os.uname().nodename, os.getpid())
    try:
        if path.read_text(encoding="ascii").strip() == me:
            path.unlink()
    except (OSError, UnicodeDecodeError):
        pass


# ---- for readers

def connect(data):
    """A read-only connection to the published copy, or None while no copy exists."""
    path = folder_of(data) / "read.db"
    if not path.is_file():
        return None
    return sqlite3.connect("file:%s?mode=ro&immutable=1" % urllib.parse.quote(str(path.resolve())), uri=True)


def route_rates(conn, since_epoch):
    """{route: (runs, read minutes, credits, one_time, credits per ship-hour or None)} over the hours from the
    hour that holds since_epoch on (whole hours: the sums are kept by hour)."""
    out = {}
    for route, runs, read_minutes, credits, one_time in conn.execute(
            "SELECT route, SUM(runs), SUM(read_minutes), SUM(credits), SUM(one_time) FROM route_hour WHERE hour >= ? "
            "GROUP BY route ORDER BY route", (int(since_epoch) // HOUR * HOUR,)):
        rate = round(60.0 * credits / read_minutes, 1) if read_minutes else None
        out[route] = (runs, read_minutes, credits, one_time, rate)
    return out


def status(data, now=None):
    """The lines of `status`, from the read copy."""
    now = time.time() if now is None else now
    conn = connect(data)
    if conn is None:
        return ["no read copy yet: %s" % (folder_of(data) / "read.db")]
    folder = folder_of(data)
    try:
        lines = ["read copy %s: %.2f MB, written %s, %d s old" % (
            folder / "read.db", (folder / "read.db").stat().st_size / 1e6, stamp((folder / "read.db").stat().st_mtime),
            now - (folder / "read.db").stat().st_mtime)]
        for table, column in NEWEST:
            count, newest = conn.execute("SELECT COUNT(*), MAX(%s) FROM %s" % (column, table)).fetchone()
            lines.append("  %-12s %9d rows   newest %s" % (table, count, stamp(newest) if newest is not None else "--"))
        for record, offset in conn.execute("SELECT record, offset FROM cursor ORDER BY record"):
            lines.append("  cursor %-24s at byte %d" % (record, offset))
        sealed = conn.execute("SELECT key, value FROM meta WHERE key LIKE 'sealed.%' ORDER BY key").fetchall()
        lines.append("  raw rows kept from: %s" % (", ".join("%s %s" % (k[7:], stamp(v)) for k, v in sealed) or "all"))
    finally:
        conn.close()
    return lines


def main(argv):
    parser = argparse.ArgumentParser(description="The fleet's history store.")
    parser.add_argument("verb", choices=("serve", "once", "status"))
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--every", type=int, default=EVERY)
    parser.add_argument("--keep-days", type=float, default=KEEP_DAYS)
    args = parser.parse_args(argv)
    if args.verb == "status":
        print("\n".join(status(args.data)))
        return 0
    if args.verb == "once":
        holder = lease(args.data)
        if holder:
            print("store: not run, the writer's lease is held by %s" % holder)
            return 1
        try:
            print(said(one_pass(args.data, keep_days=args.keep_days)) or "store: nothing new")
        finally:
            release(args.data)
        return 0
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))      # a stop runs the `finally` below: the lease goes
    print("%s store: a pass every %d s into %s, raw rows kept %g days, copy for readers %s" % (
        stamp(time.time()), args.every, folder_of(args.data) / "live.db", args.keep_days, folder_of(args.data) / "read.db"), flush=True)
    waiting = None
    try:
        while True:
            try:
                holder = lease(args.data)
                if holder:
                    if holder.split(",")[0] != waiting:
                        print("%s waiting: the writer's lease is held by %s" % (stamp(time.time()), holder), flush=True)
                    waiting = holder.split(",")[0]
                else:
                    waiting = None
                    line = said(one_pass(args.data, keep_days=args.keep_days))
                    if line:
                        print(stamp(time.time()), line, flush=True)
            except Exception as error:                 # one failed pass never ends the service
                print("%s pass failed: %s: %s" % (stamp(time.time()), type(error).__name__, error), flush=True)
            time.sleep(args.every)
    finally:
        release(args.data)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
