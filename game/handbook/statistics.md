# Statistics -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## stats_time

history (stats.py): every 10 minutes the ships per role and state: own, other (another class's work), once, shared, hand, docked, space (without work), offline; a sample is the state at that moment (work sampling); kept 30 days

- Kind: statistics
- Columns: t, role, state, ships; one row per t, role, state
- Kept: 30 days (stats.py KEEP)
- Refreshed: stats.py part `time`, every 600 s (TIME_EVERY)
- Where the fleet's ship-hours went in the last 24 hours: `SELECT state, SUM(ships) AS seen, ROUND(100.0 * SUM(ships) / (SELECT SUM(ships) FROM stats_time WHERE t >= strftime('%s', 'now') - 86400), 1) AS pct FROM stats_time WHERE t >= strftime('%s', 'now') - 86400 GROUP BY state ORDER BY 2 DESC`
- The traders' states in the newest sample: `SELECT state, ships FROM stats_time WHERE role = 'trader' AND t = (SELECT MAX(t) FROM stats_time)`
- Ships without work per sample: `SELECT datetime(t, 'unixepoch'), SUM(ships) FROM stats_time WHERE state IN ('docked', 'space') GROUP BY t ORDER BY t DESC LIMIT 24`

## stats_refill

now (stats.py): per bid (base, item), field and herd (system:poi, what) what came back an hour: the median over its recovery events (a take, then a rise before the next take) with q1, q3 and n, the same for the takes of our own sales (ours), and hive.py's least-that-is-sure sum over the hours watched (per_hour); hive.py refill prints it

- Kind: statistics
- Columns: kind, place, what, now, events, median, q1, q3, ours, ours_median, per_hour, taken_per_hour, hours, readings, t; one row per kind, place, what
- Kept: not over time: stats.compute_refill deletes rows, what stands is the newest
- Refreshed: stats.py part `refill`, once an hour (the store's first pass of a UTC hour)
- Bids that come back fastest after a take: `SELECT place AS base, what AS item, median, events, ours, hours FROM stats_refill WHERE kind = 'bid' AND events > 0 ORDER BY median DESC LIMIT 20`
- Fields that grow back: `SELECT place, what, median, events, per_hour FROM stats_refill WHERE kind = 'field' AND events > 0 ORDER BY median DESC LIMIT 20`
- Herds and how fast they regrow: `SELECT place, what, now, median, events FROM stats_refill WHERE kind = 'herd' ORDER BY median DESC LIMIT 20`

## stats_figures

now (stats.py): every figure of every stats view (kpi, contribution, classes, time, supply, gather, xp, upgrades, alerts): view, subject, figure, hours (its window, 0 for none), value (NULL: not measured), n (the records behind it), text (what it rests on), t (computed); hive.py stats <view> prints them

- Kind: statistics
- Columns: view, subject, figure, hours, value, n, text, t; one row per view, subject, figure, hours
- Kept: not over time: stats.write_figures deletes rows, what stands is the newest
- Refreshed: stats.py part `figures`, every 600 s (FIGURES_EVERY)
- The fleet's kpi over 24 hours: `SELECT figure, value, n, text FROM stats_figures WHERE view = 'kpi' AND hours = 24`
- What each division enabled for the others: `SELECT subject, value, n FROM stats_figures WHERE view = 'contribution' AND figure = 'enabled_others' ORDER BY value DESC`
- Every alert that is raised: `SELECT subject, value, text FROM stats_figures WHERE view = 'alerts' AND figure = 'alert' AND n > 0 AND text LIKE 'OUT%'`

## The figures

The views of stats.py (stats.VIEWS_SHOWN), computed by the store into stats_figures and its other tables; each defined in game/metrics.md (`hive.py docs metrics --section <id>`).

- kpi: `kpi-the-fleet-as-one-purse` (kpi -- the fleet as one purse); ask: fleet view=kpi, hive.py stats kpi
- contribution: `contribution-what-each-division-gives-the-whole` (contribution -- what each division gives the whole); ask: fleet view=contribution, hive.py stats contribution
- classes: `classes-class-capacity` (classes -- class capacity); ask: fleet view=classes, hive.py stats classes
- time: `time-where-the-ship-hours-go` (time -- where the ship-hours go); ask: fleet view=time, hive.py stats time
- supply: `supply-days-of-supply-of-the-reserve` (supply -- days of supply of the reserve); ask: fleet view=supply, hive.py stats supply
- gather: `gather-gather-against-buy` (gather -- gather against buy); ask: hive.py stats gather
- xp: `xp-skill-per-hour` (xp -- skill per hour); ask: fleet view=xp, hive.py stats xp
- upgrades: `upgrades-the-next-hull` (upgrades -- the next hull); ask: fleet view=upgrades, hive.py stats upgrades
- alerts: `alerts-control-chart` (alerts -- control chart); ask: fleet view=alerts, hive.py stats alerts
- refill: `refill-what-comes-back-by-itself` (refill -- what comes back by itself); ask: fleet view=refill, hive.py stats refill
- status: no section of game/metrics.md; ask: hive.py stats status
