# Stock and reserve -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## holdings

now: what we hold per pilot, station and item (stock/storage.json); place `hold`: the holds per member as the book sums them, no pilot; pilot and member `Faction`: the faction's storage at a base (the reading of faction_storage, without a bunker's fuel)

- Kind: snapshot
- Columns: pilot, member, place, item, units, t, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `holdings`, data/stock/storage.json
- Who holds iron_ore, and where: `SELECT pilot, place, units FROM holdings WHERE item = 'iron_ore' ORDER BY units DESC LIMIT 20`
- Storage per member: `SELECT member, SUM(units) FROM holdings WHERE place <> 'hold' GROUP BY member`
- The stations where we store goods: `SELECT place, COUNT(DISTINCT item), SUM(units) FROM holdings WHERE place <> 'hold' GROUP BY place`

## inventory

view: what the fleet holds per item, in storage and in the holds, with its base value and worth (units x base value): craftbook.py inventory's sums

- Kind: view over holdings, items
- Columns: item, name, category, units, in_storage, in_holds, base_value, worth
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- What do we hold most of, by worth: `SELECT item, name, units, base_value, worth FROM inventory ORDER BY worth DESC LIMIT 10`
- Goods we hold that no station bids for: `SELECT item, units FROM inventory WHERE item NOT IN (SELECT item FROM books WHERE bid IS NOT NULL) ORDER BY units DESC`
- The worth of what we hold, per category: `SELECT category, SUM(worth) FROM inventory GROUP BY category ORDER BY 2 DESC`

## inventory_by_station

view: what the fleet holds per place (a station's base id, or `hold`) and item

- Kind: view over holdings, items
- Columns: place, item, name, category, units
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- What lies at node_beta_industrial_station: `SELECT item, name, units FROM inventory_by_station WHERE place = 'node_beta_industrial_station' ORDER BY units DESC`
- Where iron_ore lies: `SELECT place, units FROM inventory_by_station WHERE item = 'iron_ore'`
- The worth of the goods per place: `SELECT v.place, SUM(v.units * i.base_value) FROM inventory_by_station v LEFT JOIN items i ON i.id = v.item GROUP BY v.place ORDER BY 2 DESC`

## stock_hour

history: one sample an hour of what each division (Mining, Trade, Logistics, Military, Intel, Command) holds of each item, station storage and holds added (stock/storage.json through holdings), units above 0 only; t = the pass that wrote it; kept 30 days. What flows in per hour: hive.py flow

- Kind: history
- Columns: hour, division, item, units, t; one row per hour, division, item
- Kept: 30 days (store.py KEEP_TABLES), then deleted by whole hours
- Refreshed: the store's pass (every 60 s), by store.sample_stock
- What the Military division holds now, the most first: `SELECT item, units FROM stock_hour WHERE division = 'Military' AND hour = (SELECT MAX(hour) FROM stock_hour) ORDER BY units DESC LIMIT 20`
- Units each division gained per hour over the last 4 hours, per item (an item gone to 0 is missing from the newest sample): `SELECT n.division, n.item, n.units, ROUND((n.units - COALESCE(o.units, 0)) * 3600.0 / (n.t - b.t), 1) AS per_hour FROM stock_hour n JOIN (SELECT MAX(hour) AS hour, MAX(t) AS t FROM stock_hour WHERE hour <= (SELECT MAX(hour) FROM stock_hour) - 4 * 3600) b LEFT JOIN stock_hour o ON o.hour = b.hour AND o.division = n.division AND o.item = n.item WHERE n.hour = (SELECT MAX(hour) FROM stock_hour) AND n.t > b.t ORDER BY per_hour DESC LIMIT 20`
- Copper ore held per division hour by hour: `SELECT datetime(hour, 'unixepoch') AS hour, division, units FROM stock_hour WHERE item = 'copper_ore' ORDER BY hour DESC, division LIMIT 48`
