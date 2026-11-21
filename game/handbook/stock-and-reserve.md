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

## needs

the needs register (game/needs.tsv, written by needs.py only): per need its id, project, owner division, kind (facility, hull, item), ref (the catalog's id), units, priority (1 high to 3), place, due date, status (open, done, dropped), note, added and changed with who did it, the file's line, and error (why a broken row does not count; NULL for a good one). The open needs are the reserve's targets

- Kind: snapshot
- Columns: id, project, division, kind, ref, units, priority, place, due, status, note, added, added_by, changed, changed_by, line, error, src; one row per line
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `needs`, game/needs.tsv
- The open needs by division and priority: `SELECT division, priority, id, kind, ref, units, project FROM needs WHERE status = 'open' ORDER BY division, priority, id`
- Rows of the register that do not count, and why: `SELECT line, id, error FROM needs WHERE error IS NOT NULL ORDER BY line`
- Open needs per project: `SELECT project, COUNT(*), GROUP_CONCAT(id) FROM needs WHERE status = 'open' GROUP BY project ORDER BY 2 DESC`

## need_status

per open need, computed by the store on its pass (needs.py compute: when game/needs.tsv changed, else every 300 s): its rank (the order stock is given to the needs: priority, due, added), covered (percent of its raw units stock covers), colour (red under 50, yellow 50 to 99, green nothing short, broken), stale, raw units, raw units short, what is short, to gather, to buy, to craft, what it takes from stock, the fee, the facilities of its kind our empire holds: needs.py list

- Kind: statistics
- Columns: id, rank, project, division, priority, kind, ref, units, place, due, stale, covered, colour, raw_units, raw_short, short_items, gather, buy, craft, stock, fee, stands, problem, storage_book, catalog, t; one row per id
- Kept: not over time: needs.compute deletes rows, what stands is the newest
- Refreshed: the store's pass (every 60 s), by needs.compute
- The open needs, highest first, with their colour: `SELECT rank, colour, covered, id, division, ref, short_items FROM need_status ORDER BY rank`
- The red needs of each division: `SELECT division, COUNT(*), GROUP_CONCAT(id) FROM need_status WHERE colour = 'red' GROUP BY division`
- What the open needs still ask to gather: `SELECT id, gather FROM need_status WHERE gather IS NOT NULL ORDER BY rank`
