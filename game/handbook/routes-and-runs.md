# Routes and runs -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## routes

the repository's route files (game/routes/<id>.json): kind, group (routes.py stage), cap, what the runs measured (cph per ship-hour)

- Kind: snapshot
- Columns: id, kind, grp, title, place, station, status, max_ships, once, cph, credits_per_run, runs, minutes, measured, src; one row per id
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `routes`, game/routes/*.json
- Paying routes by credits per ship-hour: `SELECT id, kind, cph, runs, measured FROM routes WHERE grp = 'paying' ORDER BY cph DESC`
- Routes per group: `SELECT grp, COUNT(*) FROM routes GROUP BY grp`
- The routes our ships fly now: `SELECT r.id, r.grp, COUNT(s.pilot) FROM routes r JOIN ships s ON s.flies = r.kind || ' ' || r.id GROUP BY r.id ORDER BY 3 DESC`

## plan_routes

each role's plan in its order: the routes its ships try and the ships the plan puts on each (game/routes/plans/<role>.json)

- Kind: snapshot
- Columns: role, n, route, ships, src; one row per role, n
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `plans`, game/routes/plans/*.json
- The miner plan in its order: `SELECT n, route, ships FROM plan_routes WHERE role = 'miner' ORDER BY n`
- Every plan with each route's group and figure: `SELECT p.role, p.n, p.route, r.grp, r.cph FROM plan_routes p LEFT JOIN routes r ON r.id = p.route ORDER BY p.role, p.n`
- Routes in more than one plan: `SELECT route, COUNT(DISTINCT role) FROM plan_routes GROUP BY route HAVING COUNT(DISTINCT role) > 1`

## runs

history: one row per run of a route (pilot, route, start, minutes, steady credits, paid once, read a wallet), the raw rows of --keep-days days

- Kind: history
- Columns: pilot, route, kind, started, t, minutes, credits, one_time, readable, row; one row per pilot, route, started
- Kept: 7 days (store.py KEEP_DAYS, --keep-days), then deleted by whole hours
- Refreshed: the store's pass (every 60 s): the new whole lines of data/routes/runs.jsonl
- The last ten runs: `SELECT pilot, route, started, minutes, credits FROM runs ORDER BY t DESC LIMIT 10`
- Steady credits per ship-hour per route over the raw runs that read a wallet: `SELECT route, COUNT(*) AS runs, ROUND(60.0 * SUM(credits) / SUM(minutes)) AS per_ship_hour FROM runs WHERE readable = 1 AND minutes > 0 GROUP BY route ORDER BY per_ship_hour DESC`
- Routes whose runs read no wallet: `SELECT route, COUNT(*) FROM runs WHERE readable = 0 GROUP BY route ORDER BY 2 DESC`

## route_hour

history: per route and UTC hour the runs, minutes, read minutes, steady credits and paid once; kept 90 days (retention.py)

- Kind: history
- Columns: route, hour, runs, minutes, read_minutes, credits, one_time; one row per route, hour
- Kept: 90 days by `hour`, then deleted (retention.py RETAIN; hourly, at most 5000 rows a table and pass)
- Refreshed: the store's pass (every 60 s): summed again for the hours that got new rows of runs
- Credits per ship-hour per route over the last 24 hours: `SELECT route, SUM(runs) AS runs, ROUND(60.0 * SUM(credits) / SUM(read_minutes)) AS per_ship_hour FROM route_hour WHERE hour >= strftime('%s', 'now') - 86400 GROUP BY route HAVING SUM(read_minutes) > 0 ORDER BY per_ship_hour DESC`
- The fleet's steady credits hour by hour: `SELECT datetime(hour, 'unixepoch') AS hour, SUM(runs), SUM(credits) FROM route_hour GROUP BY 1 ORDER BY 1 DESC LIMIT 24`
- Routes that paid once: `SELECT route, SUM(one_time) FROM route_hour GROUP BY route HAVING SUM(one_time) > 0 ORDER BY 2 DESC`

## route_earnings

view: what each route earned per ship-hour (steady credits) over the last 4, 12 and 24 hours and over all hours kept, the runs behind each figure, and the hours since it last flew: ask here what a route earns now; an empty cph_4h means it did not fly, not that it does not pay

- Kind: view over route_hour, routes
- Columns: route, kind, grp, last_hour, hours_since, runs_4h, cph_4h, runs_12h, cph_12h, runs_24h, cph_24h, runs_all, cph_all, paid_once
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- What every route earned per ship-hour in the last 4 hours, best first: `SELECT route, kind, runs_4h, cph_4h, cph_24h FROM route_earnings WHERE runs_4h > 0 ORDER BY cph_4h DESC`
- Routes that have not flown for 12 hours or more: their figure is old, a test tells what they pay now: `SELECT route, kind, hours_since, runs_all, cph_all FROM route_earnings WHERE hours_since >= 12 ORDER BY hours_since`
- Routes that pay less now than over the day (a bid or a field that is running out): `SELECT route, cph_4h, cph_24h, runs_4h FROM route_earnings WHERE runs_4h >= 2 AND cph_4h < cph_24h ORDER BY cph_4h - cph_24h`

## fuel_sinks

view: trailing 24-hour runs, ship-hours and net credits grouped into productive work vs jump_loops, census and handovers

- Kind: view over runs
- Columns: category, runs_24h, ship_hours_24h, net_credits_24h
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- 24h ship-hours and net credits across productive work vs jump loops, census and handovers: `SELECT * FROM fuel_sinks ORDER BY ship_hours_24h DESC`
- Share of fleet ship-hours spent on empty jump loops: `SELECT category, ship_hours_24h, net_credits_24h FROM fuel_sinks WHERE category = 'jump_loops'`
- Productive vs non-productive 24h credit balance: `SELECT CASE WHEN category = 'productive' THEN 'productive' ELSE 'overhead' END AS grp, SUM(ship_hours_24h), SUM(net_credits_24h) FROM fuel_sinks GROUP BY 1`

## stats_route_author

state (stats.py): the first author of every route file (git log --diff-filter=A) with its member and division: whose work a route's income is (view contribution)

- Kind: statistics
- Columns: route, author, member, division, added, t; one row per route
- Kept: a route whose file is gone and that no route_hour row of the last 90 days names goes (retention.py RETAIN; hourly, at most 5000 rows a table and pass)
- Refreshed: stats.py part `authors`, every 600 s (FIGURES_EVERY)
- Route files per division: `SELECT division, COUNT(*) FROM stats_route_author GROUP BY division ORDER BY 2 DESC`
- Who wrote the routes that earned most in 24 hours: `SELECT a.route, a.division, ROUND(SUM(h.credits)) FROM route_hour h JOIN stats_route_author a ON a.route = h.route WHERE h.hour >= strftime('%s', 'now') - 86400 GROUP BY a.route ORDER BY 3 DESC LIMIT 10`
- Route files written by no member: `SELECT route, author FROM stats_route_author WHERE member IS NULL`

## missions

now: the missions on offer at each station our ships read: kind, reward in credits, items, XP, objectives (missions/<base>.json)

- Kind: snapshot
- Columns: base, system, id, template, title, kind, difficulty, reward, reward_items, reward_xp, expires_ticks, giver, objectives, t, src
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `missions`, data/missions/*.json
- The missions of highest reward: `SELECT base, title, kind, reward FROM missions ORDER BY reward DESC LIMIT 10`
- Missions per station: `SELECT base, COUNT(*), SUM(reward) FROM missions GROUP BY base`
- Missions that hand out items: `SELECT base, title, reward_items FROM missions WHERE reward_items IS NOT NULL`
