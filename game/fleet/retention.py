#!/usr/bin/env python3
"""retention.py -- how long the store keeps the tables it kept for good: the hourly sums 90 days, the daily sums 400, the written knowledge's versions the newest 20 of each section and every one of the last 30 days; one table of rules, applied in the store's prune step behind a switch that is off, with a dry run.

WHAT: store.py's prune (every pass of the service `store`) calls apply(conn, now, keep_days) after the raw rows. With
      RETAIN_ENABLED on, once an hour (and at the very next pass while a table had more than one batch to go) it
      deletes, table by table of RETAIN, the rows older than the table's days:
        route_hour, market_hour, stats_money_hour, stats_supply_hour   90 days, by `hour`
        reading_day                                                    400 days, by `day`
        doc_versions        30 days by last_seen (the last pass in which a version stood), and only a version that
                            has at least RETAIN_VERSIONS (20) newer versions of its own section: the newest 20 of each
                            section stay whatever their age, so every section, standing or gone from its file, keeps
                            its newest text, and every text that stood in the last 30 days stays (git keeps them all)
        stats_route_author  90 days by `t`, and only a route whose file is gone (the table routes) and that no
                            route_hour row of the last 90 days names; never while the table routes is empty
      BOUNDED names the tables kept for good whose rows the code or the fleet's size bounds: they need no rule.
      READER names, per table, the reader that reads it furthest back: every rule's days lie beyond it.
RULES:
  - Delete only what a coarser tier holds, or what no reader reads: an hour of a sum older than its days has no raw
    row any more (store.py KEEP_DAYS, the sealed hours), and a rule's days are never fewer than --keep-days + 1, so no
    sum goes while its raw rows stand (the store would sum them again).
  - Bounded transactions: one per table and pass, at most RETAIN_BATCH rows each; a table that had more goes on at
    the next pass (meta retain.more), else the rules run again RETAIN_EVERY seconds later (meta retain.at). The pages
    freed stay in live.db, where SQLite reuses them (no VACUUM of the writer's file); read.db is written by VACUUM
    INTO and holds no free page.
  - Off (RETAIN_ENABLED False, the default), apply deletes nothing, reads nothing and writes nothing. The dry run
    reads only: the read copy, opened read-only and immutable, or the file --db names.
WHY:  Suggi, 2026-11-22: nothing of the fleet may pile up forever; check the SQL database for endless growth and put
      the prevention in, without breaking the systems. Nine tables were kept for good; doc_versions grew 5.8 MB of text
      in four days (about 350 MB a year at that rate) and market_hour about 7,000 rows a day.

USAGE:
  retention.py --dry-run [--data <dir>] [--db <file>] [--now <epoch>] [--keep-days N]
      per table: its rows, the rows of the last 24 hours, its rule, the reader that reads it furthest back, the rows
      that would go now and in a year at today's rate, and its size; then the tables that need no rule
  --data <dir>    the unit's data folder (default /srv/collective/data): its store's read copy
  --db <file>     another copy of the store instead (a copy of read.db, for a dry run away from the live files); it is
                  opened immutable, so it must be a whole copy (VACUUM INTO, as read.db is), not a file with a WAL beside it
  --now <epoch>   the time the rules are judged at (default: now)
  --keep-days N   the store's --keep-days (default store.py KEEP_DAYS, 7)

Stdlib only. ASCII only.
"""

import argparse
import math
import sqlite3
import sys
import time
import urllib.parse
from pathlib import Path

HOUR, DAY = 3600, 86400
RETAIN_ENABLED = False         # r22: off. On, the store's prune deletes by RETAIN; off, nothing of these tables is deleted
RETAIN = {                     # table -> days its rows stay (doc_versions and stats_route_author: see WHERE)
    "route_hour": 90, "market_hour": 90, "stats_money_hour": 90, "stats_supply_hour": 90,
    "reading_day": 400,
    "doc_versions": 30,
    "stats_route_author": 90,
}
COLUMN = {"route_hour": "hour", "market_hour": "hour", "stats_money_hour": "hour", "stats_supply_hour": "hour", "reading_day": "day",
          "doc_versions": "last_seen", "stats_route_author": "t"}
ARRIVES = {"doc_versions": "first_seen"}      # the column a row's arrival is read by, where it is not COLUMN (the rate a day)
RETAIN_VERSIONS = 20           # doc_versions: the newest versions of each section that stay whatever their age
RETAIN_BATCH = 5000            # rows at most one transaction deletes from one table
RETAIN_EVERY = HOUR            # seconds between two runs of the rules (sooner while a table had more than a batch)
WHERE = {                      # beyond the age: the rows of x (the table) that may go
    "doc_versions": "(SELECT COUNT(*) FROM doc_versions w WHERE w.path = x.path AND w.section = x.section AND w.version > x.version) >= :versions",
    "stats_route_author": "x.route NOT IN (SELECT id FROM routes WHERE id IS NOT NULL) AND x.route NOT IN "
                          "(SELECT route FROM route_hour WHERE hour >= :cut)",
}
NEEDS = {"stats_route_author": ("routes", "route_hour")}     # tables a rule reads: missing or (routes) empty, nothing goes
READER = {                     # the reader that reads the table furthest back (r22, read from the code)
    "route_hour": "stats.py alerts, 9 days of each route's hours; route_earnings's cph_all and paid_once sum every hour kept; "
                  "hive.py store --hours N (24 by default)",
    "market_hour": "hive.py store price <item> --hours N (24 by default); nothing else reads it",
    "stats_money_hour": "stats.py alerts, 9 days; kpi 72 h and the 72 h before it (6 days)",
    "stats_supply_hour": "stats.py contribution (Logistics' chains at keep), 24 h; the handbook's examples, every hour kept",
    "reading_day": "no code reads it (stats_refill reads the raw readings); the handbook's examples",
    "doc_versions": "docs.py --history, every version kept; changes, the briefing, division, guide --retired and guide.py tidy "
                    "read the newest version of a section, which always stays",
    "stats_route_author": "stats.py contribution, the routes flown in 24 h; sample_authors, the files of the table routes",
}
BOUNDED = {                    # kept for good, and bounded without a rule
    "cursor": "one row per record the store reads (store.RECORDS), its place in the record",
    "stats_pilot_last": "one row per pilot and key: the pilots ever registered times the keys (the skills a pilot trained, "
                        "stats.COUNTERS and read_hours); made again empty when stats.SCHEMA changes",
}


def on(enabled=None):
    return bool(RETAIN_ENABLED if enabled is None else enabled)


def kept(table, enabled=None):
    """How long a table's rows stay, as the code says it now (the handbook's Kept line, the store's descriptions)."""
    if table in BOUNDED:
        return "for good, bounded: %s (retention.py BOUNDED)" % BOUNDED[table]
    if table not in RETAIN:
        return "for good: retention.py names no rule"
    days, column = RETAIN[table], COLUMN[table]
    rule = {"doc_versions": "the newest %d versions of each section stay whatever their age, and every version that stood in the "
                            "last %d days (by last_seen); git keeps every text" % (RETAIN_VERSIONS, days),
            "stats_route_author": "a route whose file is gone and that no route_hour row of the last %d days names goes" % days}.get(
        table, "%d days by `%s`, then deleted" % (days, column))
    how = "hourly, at most %d rows a table and pass" % RETAIN_BATCH
    if on(enabled):
        return "%s (retention.py RETAIN; %s)" % (rule, how)
    return "for good while retention.py RETAIN_ENABLED is off; on: %s (%s)" % (rule, how)


def short(table, enabled=None):
    """The few words a table's description carries about its keeping."""
    if table not in RETAIN:
        return "for good"
    days = RETAIN[table]
    rule = {"doc_versions": "the newest %d versions of each section and those of the last %d days" % (RETAIN_VERSIONS, days),
            "stats_route_author": "while its route file stands or flew in the last %d days" % days}.get(table, "%d days" % days)
    return ("%s (retention.py)" % rule) if on(enabled) else ("for good while retention.py is off (on: %s)" % rule)


def meta(conn, key, default=0):
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else default


def present(conn, table):
    return conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)).fetchone() is not None


def usable(conn, table):
    """True when the table and every table its rule reads stand (the table routes with a row: an empty one is a snapshot
    that failed, and would make every author look gone)."""
    if not present(conn, table):
        return False
    for other in NEEDS.get(table, ()):
        if not present(conn, other):
            return False
        if other == "routes" and conn.execute("SELECT 1 FROM routes LIMIT 1").fetchone() is None:
            return False
    return True


def cut_of(table, now, keep_days=0):
    """The time before which a row of the table may go: its days, never fewer than keep_days + 1, in whole hours (days)."""
    days = max(RETAIN[table], (keep_days or 0) + 1)
    step = DAY if COLUMN[table] == "day" else HOUR
    return int(now - days * DAY) // step * step


def selection(table, cut):
    """(SQL that selects the rowids of the rows that may go, its arguments)."""
    sql = "SELECT x.rowid FROM %s x WHERE x.%s < :cut" % (table, COLUMN[table])
    if table in WHERE:
        sql += " AND " + WHERE[table]
    return sql, {"cut": cut, "versions": RETAIN_VERSIONS}


def due(conn, now):
    return bool(int(meta(conn, "retain.more", 0) or 0)) or now - float(meta(conn, "retain.at", 0) or 0) >= RETAIN_EVERY


def apply(conn, now, keep_days=0, enabled=None, batch=None):
    """The store's hook (prune): off, 0 and nothing touched. On and due, per table of RETAIN one transaction that
    deletes at most `batch` rows the rule lets go, then the marks retain.at and retain.more: the rows deleted."""
    if not on(enabled) or not due(conn, now):
        return 0
    batch, gone, more = int(batch or RETAIN_BATCH), 0, False
    for table in RETAIN:
        if not usable(conn, table):
            continue
        sql, args = selection(table, cut_of(table, now, keep_days))
        conn.execute("BEGIN IMMEDIATE")
        try:
            n = conn.execute("DELETE FROM %s WHERE rowid IN (%s LIMIT :batch)" % (table, sql), dict(args, batch=batch)).rowcount
            conn.execute("COMMIT")
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        gone += max(n, 0)
        more = more or n >= batch
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('retain.at', ?)", (int(now),))
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('retain.more', ?)", (1 if more else 0,))
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return gone


# ---- the dry run: reads only

def table_bytes(conn, table):
    """Bytes of a table and its indexes (dbstat), or None where the build of SQLite has no dbstat."""
    names = [table] + [n for (n,) in conn.execute("SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = ?", (table,))]
    try:
        return conn.execute("SELECT SUM(pgsize) FROM dbstat WHERE name IN (%s)" % ",".join("?" * len(names)), names).fetchone()[0] or 0
    except sqlite3.Error:
        return None


def baselines(conn):
    """The passes that loaded a kind of docs whole (meta docs.baseline*): their rows are no day's arrivals."""
    try:
        return {int(v or 0) for (v,) in conn.execute("SELECT value FROM meta WHERE key LIKE 'docs.baseline%'")}
    except sqlite3.Error:
        return set()


def plan_versions(conn, now, days):
    """doc_versions in a year at the rate of the last 24 hours: (rows a year from now without the rule, with it). A
    section's churn is its versions of the last day (its first one not counted when the section is new); a new section
    is one version, which stays."""
    marks, since = sorted(baselines(conn)), int(now - DAY)
    sections, created = [], 0
    for first, count, fresh in conn.execute(
            "SELECT MIN(first_seen), COUNT(*), SUM(first_seen >= ? AND first_seen NOT IN (%s)) FROM doc_versions GROUP BY path, section"
            % (",".join("?" * len(marks)) or "NULL"), [since] + marks):
        new = first >= since and first not in marks
        churn = max((fresh or 0) - (1 if new else 0), 0)
        created += 1 if new else 0
        sections.append((count, churn))
    without = sum(c + 365 * r for c, r in sections) + 365 * created        # a new section a day stays one version
    gone = 0
    for count, churn in sections:
        total = count + 365 * churn
        gone += total - min(total, max(RETAIN_VERSIONS, int(math.ceil(churn * days)) + 1))
    return without, without - gone


def plan(conn, now, keep_days=0):
    """Per table of RETAIN, read only: {table: {rows, day, now, year_without, year_with, bytes, rule, reader}}."""
    out = {}
    for table in RETAIN:
        if not present(conn, table):
            out[table] = None
            continue
        rows = conn.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0]
        arrive = ARRIVES.get(table, COLUMN[table])
        day = conn.execute("SELECT COUNT(*) FROM %s WHERE %s >= ?" % (table, arrive), (int(now - DAY),)).fetchone()[0]
        if table == "doc_versions":
            marks = baselines(conn)
            if marks:
                day -= conn.execute("SELECT COUNT(*) FROM doc_versions WHERE first_seen >= ? AND first_seen IN (%s)" % ",".join("?" * len(marks)),
                                    [int(now - DAY)] + sorted(marks)).fetchone()[0]
        sql, args = selection(table, cut_of(table, now, keep_days))
        going = conn.execute("SELECT COUNT(*) FROM (%s)" % sql, args).fetchone()[0] if usable(conn, table) else 0
        days = max(RETAIN[table], (keep_days or 0) + 1)
        if table == "doc_versions":
            without, with_rule = plan_versions(conn, now, days)
        elif table == "stats_route_author":
            without, with_rule = None, None            # its rows go only when a route file goes: no rate says when
        else:
            oldest = conn.execute("SELECT MIN(%s) FROM %s" % (COLUMN[table], table)).fetchone()[0]
            span = max((now - oldest) / DAY, 1.0) if oldest is not None else 1.0
            without = rows + 365 * day
            with_rule = min(without, int(round(day * min(days, span + 365))))
        out[table] = {"rows": rows, "day": day, "now": going, "year_without": without, "year_with": with_rule,
                      "bytes": table_bytes(conn, table), "rule": kept(table, True), "reader": READER.get(table, "--")}
    return out


def mb(n):
    return "%.1f MB" % (n / 1e6) if n is not None else "not measured"


def report(conn, now, keep_days, where):
    """The dry run's lines."""
    lines = ["RETAIN | the switch retention.RETAIN_ENABLED is %s: %s | %s, judged at %s UTC | read only"
             % ("ON" if on() else "OFF", "the store's prune deletes by these rules" if on() else "the store deletes none of these rows",
                where, time.strftime("%Y-%m-%d %H:%M", time.gmtime(now)))]
    found = plan(conn, now, keep_days)
    for table, f in found.items():
        if f is None:
            lines.append("  %s: not in this copy" % table)
            continue
        per = (f["bytes"] / float(f["rows"])) if f["bytes"] is not None and f["rows"] else None
        year = ("not projected: its rows go only when a route file goes" if f["year_without"] is None else
                "%s rows held without the rule, %s with it: %s would have gone (%s without, %s with)"
                % (format(f["year_without"], ","), format(f["year_with"], ","), format(f["year_without"] - f["year_with"], ","),
                   mb(per * f["year_without"] if per is not None else None), mb(per * f["year_with"] if per is not None else None)))
        lines.append("  %-19s %9s rows (%s), %s in the last 24 h | would go now: %s | in a year at today's rate: %s"
                     % (table, format(f["rows"], ","), mb(f["bytes"]), format(f["day"], ","), format(f["now"], ","), year))
        lines.append("      rule: %s" % f["rule"])
        lines.append("      reads furthest back: %s" % f["reader"])
    for table, why in BOUNDED.items():
        rows = conn.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0] if present(conn, table) else None
        lines.append("  %-19s %9s rows | no rule: %s" % (table, format(rows, ",") if rows is not None else "--", why))
    return lines


def open_copy(data, db):
    """(connection, what it is) to a store file, read-only and immutable."""
    path = Path(db) if db else Path(data) / "store" / "read.db"
    if not path.is_file():
        return None, "no store file at %s" % path
    return sqlite3.connect("file:%s?mode=ro&immutable=1" % urllib.parse.quote(str(path.resolve())), uri=True), str(path)


def main(argv):
    parser = argparse.ArgumentParser(description="The retention of the store's tables kept for good: the dry run.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--db")
    parser.add_argument("--now", type=float)
    parser.add_argument("--keep-days", type=float, default=7)
    args = parser.parse_args(argv)
    if not args.dry_run:
        print("RETAIN | only --dry-run here: the store's pass applies the rules itself, while RETAIN_ENABLED is on")
        return 2
    conn, where = open_copy(args.data, args.db)
    if conn is None:
        print("RETAIN | " + where)
        return 1
    try:
        print("\n".join(report(conn, args.now or time.time(), args.keep_days, where)))
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
