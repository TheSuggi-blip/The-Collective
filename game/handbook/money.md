# Money -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## stats_money_hour

history (stats.py): per whole UTC hour and division (Fleet: the whole) the steady money of that hour by station/fleet.py's window(): income, costs, net (= income - costs), paid once (rewards - bought), total, per hour over `minutes`; wallets at the hour's end, the treasury when read near it, the idle share of the collector's minute samples (Fleet); kept for good while retention.py is off (on: 90 days). The Fleet rows add up to the collector's window over a longer span; a division's rows of one hour need not add up to the Fleet's (a move between our purses whose two sides fall into different hours): sum the Fleet rows only

- Kind: statistics
- Columns: hour, division, minutes, income, costs, net, rewards, bought, once, total, wallets, fuel, repair, ships, wallets_end, treasury, idle, samples, t; one row per hour, division
- Kept: for good while retention.py RETAIN_ENABLED is off; on: 90 days by `hour`, then deleted (hourly, at most 5000 rows a table and pass)
- Refreshed: stats.py part `money`, once an hour (the store's first pass of a UTC hour)
- The fleet's steady net hour by hour: `SELECT datetime(hour, 'unixepoch') AS hour, ROUND(net) AS net, ROUND(income) AS income, ROUND(costs) AS costs, ROUND(once) AS paid_once FROM stats_money_hour WHERE division = 'Fleet' ORDER BY hour DESC LIMIT 24`
- The fleet's steady credits over the last 72 whole hours: `SELECT ROUND(SUM(net * minutes / 60.0)) AS net_credits, COUNT(*) AS hours FROM stats_money_hour WHERE division = 'Fleet' AND hour >= strftime('%s', 'now') - 72 * 3600`
- The idle share of the fleet hour by hour: `SELECT datetime(hour, 'unixepoch'), ROUND(100 * idle, 1) AS idle_pct, samples FROM stats_money_hour WHERE division = 'Fleet' ORDER BY hour DESC LIMIT 24`
