# Supply -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## supply_chains

the supply chains (game/supply/chains.tsv, kept by the Fleet Admiral with Logistics): per chain the item, its place (`fleet`, a base or a system), keep (units that must stand there at least), need per hour (0: not known), sources (route ids with commas), the keeper division, note, the file's line, and error (why a broken row does not count; NULL for a good one)

- Kind: snapshot
- Columns: chain, item, place, keep, need_per_hour, sources, keeper, note, line, error, src; one row per line
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `supply`, game/supply/chains.tsv
- Every chain with its keeper: `SELECT chain, item, place, keep, need_per_hour, keeper FROM supply_chains ORDER BY keeper, chain`
- Rows of the chains file that do not count, and why: `SELECT line, chain, error FROM supply_chains WHERE error IS NOT NULL ORDER BY line`
- Chains per keeper: `SELECT keeper, COUNT(*) FROM supply_chains GROUP BY keeper ORDER BY 2 DESC`

## supply_status

view: each supply chain against what stands at its place now (holdings): stock, status (short below keep, low below twice keep, ok; broken), hours left at its need, the change over 24 hours (fleet only, stock_hour), its sources listed and known, our ships on them now (ships.flies), its sources in a role plan (plan_routes), place_rows (0: no reading of the place, its 0 is not measured): supply.py show

- Kind: view over supply_chains, places, bases, holdings, stock_hour, routes, ships, plan_routes
- Columns: chain, item, place, keep, stock, status, need_per_hour, hours_left, change_24h, change_hours, sources, sources_listed, sources_known, ships, sources_planned, keeper, place_rows, note, line, error
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- The chains that are broken, short or low, the worst first: `SELECT chain, item, place, stock, keep, status, ships, keeper FROM supply_status WHERE status <> 'ok' ORDER BY CASE status WHEN 'broken' THEN 0 WHEN 'short' THEN 1 ELSE 2 END, 1.0 * stock / NULLIF(keep, 0)`
- Short chains with no ship on their sources: `SELECT chain, item, place, sources, keeper FROM supply_status WHERE status = 'short' AND ships = 0`
- How the chains held anywhere moved over the last day: `SELECT chain, item, stock, change_24h, change_hours FROM supply_status WHERE place = 'fleet' ORDER BY chain`

## stats_supply_hour

history (stats.py): per hour and supply chain its stock against its keep and its status (view supply_status); kept for good

- Kind: statistics
- Columns: hour, chain, item, place, stock, keep, status, t; one row per hour, chain
- Kept: for good: no step of the code deletes its rows
- Refreshed: stats.py part `supply`, once an hour (the store's first pass of a UTC hour)
- The share of hours each chain stood at its keep: `SELECT chain, item, ROUND(100.0 * SUM(stock >= keep) / COUNT(*)) AS pct_ok, COUNT(*) AS hours FROM stats_supply_hour GROUP BY chain`
- One chain hour by hour: `SELECT datetime(hour, 'unixepoch'), stock, keep, status FROM stats_supply_hour ORDER BY chain, hour DESC LIMIT 24`
- Hours a chain stood short: `SELECT chain, COUNT(*) FROM stats_supply_hour WHERE status = 'short' GROUP BY chain`
