#!/usr/bin/env python3
"""herds.py -- every place a species was ever counted by our census, with its count now, the age of the read, the law there and the pirate record, for the hunters.

WHAT: reads the store's read copy (store.connect): reading_day (every herd a census counted, by day), herds (the newest
      count of each place), places (when each system was last read), systems (jumps from home, empire, strongholds),
      observations kind pirate (the pirates our ships met) and public_battles (pirate and npc battles on record), and
      prints one table per species: place, animals now, the most ever counted there in one census, minutes since the
      system was read, jumps, empire or lawless, pirates met there in the window, and whether a hunt may take one
      now (more animals than the herd keeps, rule F38).
RULES:
  - Read only. A place counted once and empty now stays on the list with 0: herds come back.
  - `huntable` means count now above the kept herd (default 2, rule F38: two grazers left unhurt); a ranch of another
    faction is never prey (hunt.py, foreign_ranched).
WHY:  orders ENT-083 (P3, block ORACLE): the Atria kit's last parts are creature parts; Intel reads the herds of five
      species with each system's pirate record for Military. On 2026-11-23 the figures were joined by hand.

USAGE:
  hive.py herds <species>[,<species>...] [--hours 72] [--keep 2]
  herds.py <species>[,<species>...] [--hours 72] [--keep 2] [--data <data folder>]
  e.g. hive.py herds mirror_skate,cauldronback,inkwyrm,magnet_barnacle,silica_borer

Stdlib only. ASCII only."""
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def table(conn, species, now, hours=72.0, keep=2):
    """{species: [row, ...]} with row = dict(system, poi, now, most, age_min, jumps, law, pirates, battles, huntable),
    nearest first, then the larger herd."""
    marks = ",".join("?" * len(species))
    seen = conn.execute("SELECT what, system, poi, MAX(last), MAX(first) FROM reading_day WHERE what IN (%s) "
                        "GROUP BY what, system, poi" % marks, list(species)).fetchall()
    count = {(c, s, p): n for c, s, p, n in conn.execute(
        "SELECT creature, system, poi, count FROM herds WHERE creature IN (%s)" % marks, list(species))}
    read = {s: t for s, t in conn.execute("SELECT system, MAX(t) FROM places GROUP BY system")}
    chart = {s: (e, j, sh) for s, e, j, sh in conn.execute("SELECT id, empire, jumps, stronghold FROM systems")}
    since = now - hours * 3600
    pirates = Counter(s for (s,) in conn.execute(
        "SELECT subject FROM observations WHERE kind = 'pirate' AND t >= ?", (since,)))
    battles = Counter(s for (s,) in conn.execute(
        "SELECT system FROM public_battles WHERE category IN ('pirate', 'npc')"))
    out = defaultdict(list)
    for what, system, poi, last, first in seen:
        empire, jumps, stronghold = chart.get(system, (None, None, None))
        n = count.get((what, system, poi), 0)
        most = max(int(last or 0), int(first or 0), n)
        age = int((now - read[system]) / 60) if read.get(system) else None
        out[what].append({"system": system, "poi": poi, "now": n, "most": most, "age_min": age, "jumps": jumps,
                          "law": (empire or "lawless") + (" stronghold" if stronghold else ""),
                          "pirates": pirates.get(system, 0), "battles": battles.get(system, 0), "huntable": n > keep})
    for what in out:
        out[what].sort(key=lambda r: (r["jumps"] if r["jumps"] is not None else 999, -r["now"], r["system"], r["poi"]))
    return out


def show(conn, species, now, hours=72.0, keep=2):
    found = table(conn, species, now, hours, keep)
    print("HERDS | %s | every place our census ever counted them | huntable: more than %d now (rule F38) | pirates: met by "
          "our ships in %g h (observations kind pirate); battles: pirate and npc battles on record (public_battles)"
          % (", ".join(species), keep, hours))
    for what in species:
        rows = found.get(what, [])
        print("%s | %d places, %d animals now, %d places huntable" % (
            what, len(rows), sum(r["now"] for r in rows), sum(1 for r in rows if r["huntable"])))
        if not rows:
            print("  not seen by any census")
            continue
        print("  %-16s %-34s %4s %5s %8s %5s %-20s %7s %7s %s" % (
            "system", "poi", "now", "most", "read", "jumps", "law", "pirates", "battles", "huntable"))
        for r in rows:
            print("  %-16s %-34s %4d %5d %8s %5s %-20s %7d %7d %s" % (
                r["system"], r["poi"], r["now"], r["most"], "%dm" % r["age_min"] if r["age_min"] is not None else "--",
                r["jumps"] if r["jumps"] is not None else "--", r["law"], r["pirates"], r["battles"],
                "yes" if r["huntable"] else "no"))
    return 0


def main(args):
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in ("--data", "--hours", "--keep"))]
    if not words:
        sys.exit(__doc__)
    import division
    import store
    conn = store.connect(value("--data", division.DATA))
    if conn is None:
        print("HERDS | no read copy of the store yet")
        return 1
    species = [s.strip() for s in ",".join(words).split(",") if s.strip()]
    return show(conn, species, time.time(), float(value("--hours", "72")), int(value("--keep", "2")))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
