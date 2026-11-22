# Plans and the door -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## birth_plans

Suggi-approved 500-ship (waves 0-3) and 600-ship Praetorian Royal Guard (waves 0-4) multi-empire birthing cohorts, target hulls and readiness gates (game/birth-plans.tsv)

- Kind: snapshot
- Columns: cohort_id, plan_scope, wave, wave_target, division, role, wing, empire, ships, flagship_hulls, gate, note, src; one row per cohort_id
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `birth_plans`, game/birth-plans.tsv
- Approved 500-ship fleet composition by division, role and empire: `SELECT division, role, empire, SUM(ships) AS ships FROM birth_plans WHERE wave <= 3 GROUP BY division, role, empire ORDER BY division, ships DESC`
- Approved 600-ship fleet and 60-ship Royal Guard composition: `SELECT division, role, wing, empire, SUM(ships) AS ships FROM birth_plans GROUP BY division, role, wing, empire ORDER BY division, ships DESC`
- Phased birthing waves from 246 to 600 ships with readiness gates: `SELECT wave, wave_target, SUM(ships) AS wave_ships, gate FROM birth_plans WHERE wave >= 1 GROUP BY wave, wave_target, gate ORDER BY wave`
