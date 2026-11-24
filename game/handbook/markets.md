# Markets -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## books

now: each station's order book as our ship read it: best bid and ask with their units per item (market/<base>.json); no price is NULL

- Kind: snapshot
- Columns: base, system, item, name, category, bid, bid_qty, ask, ask_qty, bid_depth, ask_depth, t, src; one row per base, item
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `books`, data/market/*.json
- Which stations bid for iron_ore, and how much: `SELECT base, system, bid, bid_qty, datetime(t, 'unixepoch') AS read FROM books WHERE item = 'iron_ore' AND bid IS NOT NULL ORDER BY bid DESC`
- The cheapest offers of steel_plate: `SELECT base, ask, ask_qty FROM books WHERE item = 'steel_plate' AND ask IS NOT NULL ORDER BY ask`
- Bought at one station's ask, bid higher at another: `SELECT a.item, a.base AS buy_at, a.ask, b.base AS sell_at, b.bid, b.bid - a.ask AS margin FROM books a JOIN books b ON b.item = a.item AND b.base <> a.base WHERE a.ask IS NOT NULL AND b.bid > a.ask ORDER BY margin DESC LIMIT 20`

## ladders

now: the price ladder of an item at a station, every bid and ask step with its units, step 1 the best (market/ladders.json)

- Kind: snapshot
- Columns: base, item, side, step, price, qty, t, src; one row per base, item, side, step
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `ladders`, data/market/ladders.json
- The whole bid ladder of iron_ore: `SELECT base, step, price, qty FROM ladders WHERE item = 'iron_ore' AND side = 'bid' ORDER BY base, step`
- Units bid at 100 cr or more, per item: `SELECT item, SUM(qty) FROM ladders WHERE side = 'bid' AND price >= 100 GROUP BY item ORDER BY 2 DESC`
- Items with a ladder per station: `SELECT base, COUNT(DISTINCT item) FROM ladders GROUP BY base`

## ship_listings

now: galaxy-wide player and shipyard ship listings across all stations, refreshed every 15 min by ledger.py (market/ship_listings.json)

- Kind: snapshot
- Columns: listing_id, ship_id, class_id, ship_name, category, tier, base, base_name, price, seller, listed_at, t, src; one row per listing_id
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `ship_listings`, data/market/ship_listings.json
- Cheapest listed hull per class across the galaxy: `SELECT class_id, MIN(price) AS min_price, base, COUNT(*) AS avail FROM ship_listings WHERE price > 0 GROUP BY class_id ORDER BY min_price LIMIT 25`
- Listed ships under 150,000 cr with cargo >= 250: `SELECT sl.class_id, h.cargo, h.piloting_required, sl.price, sl.base FROM ship_listings sl JOIN hulls h ON h.id = sl.class_id WHERE sl.price > 0 AND sl.price <= 150000 AND h.cargo >= 250 ORDER BY sl.price LIMIT 20`
- Cheapest listed combat hulls by tier: `SELECT sl.class_id, sl.tier, MIN(sl.price) AS min_price, sl.base FROM ship_listings sl WHERE sl.category = 'Combat' AND sl.price > 0 GROUP BY sl.class_id ORDER BY sl.tier, min_price`

## moves

history: one row per change of an item's best bid or ask at a station (market/history.jsonl), the raw rows of --keep-days days

- Kind: history
- Columns: base, item, t, bid, bid_qty, ask, ask_qty; one row per base, item, t
- Kept: 7 days (store.py KEEP_DAYS, --keep-days), then deleted by whole hours
- Refreshed: the store's pass (every 60 s): the new whole lines of data/market/history.jsonl
- The last price moves of iron_ore: `SELECT base, datetime(t, 'unixepoch') AS at, bid, bid_qty, ask, ask_qty FROM moves WHERE item = 'iron_ore' ORDER BY t DESC LIMIT 10`
- Which items moved most often: `SELECT item, COUNT(*) FROM moves GROUP BY item ORDER BY 2 DESC LIMIT 10`
- Moves per station: `SELECT base, COUNT(*) FROM moves GROUP BY base ORDER BY 2 DESC`

## market_hour

history: per station, item and UTC hour the lowest and highest best bid and best ask; kept 90 days (retention.py)

- Kind: history
- Columns: base, item, hour, bid_lo, bid_hi, ask_lo, ask_hi, moves; one row per base, item, hour
- Kept: 90 days by `hour`, then deleted (retention.py RETAIN; hourly, at most 5000 rows a table and pass)
- Refreshed: the store's pass (every 60 s): summed again for the hours that got new rows of moves
- The highest bid for iron_ore per station in the last day: `SELECT base, MAX(bid_hi) FROM market_hour WHERE item = 'iron_ore' AND hour >= strftime('%s', 'now') - 86400 GROUP BY base ORDER BY 2 DESC`
- The cheapest ask ever seen for steel_plate: `SELECT base, MIN(ask_lo), datetime(MAX(hour), 'unixepoch') FROM market_hour WHERE item = 'steel_plate' GROUP BY base ORDER BY 2`
- Hours of prices per item: `SELECT item, COUNT(*) FROM market_hour GROUP BY item ORDER BY 2 DESC LIMIT 20`

## contract_candidates

view: open priority needs with missing items where Station Bursars or Notice Board contracts can source bottlenecks

- Kind: view over need_status
- Columns: need_id, priority, division, target_ref, covered_pct, short_items, fee
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- Open bottleneck needs for Station Bursar buy-bids and Notice Board contracts: `SELECT * FROM contract_candidates ORDER BY priority`
- Priority 1 bottlenecks needing procurement: `SELECT need_id, division, covered_pct, short_items FROM contract_candidates WHERE priority = 1`
- Needs by division with missing items: `SELECT division, COUNT(*) AS open_needs, GROUP_CONCAT(need_id) FROM contract_candidates GROUP BY division`
