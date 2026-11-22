---
name: metrics
id: 20261118T030157Z
tier: guide
author: Unity
links:
  - governance/strategy.md
  - governance/rulebook.md
  - game/fleet/stats.py
---

# metrics.md -- the fleet's figures, defined

The definitions book of `hive.py stats <view>` (MCP: tool `fleet`, the same views). The store computes every figure
by itself (`game/fleet/stats.py`) into tables of the store; nobody writes one by hand. A new figure is defined here
first, then built.

## Rules every figure keeps

- One purse. The fleet as a whole earns (Suggi). A division is read by what it gives the whole fleet, not by its
  own wallet: a scout that earns little but feeds the others is worth its fuel. Local optima do not add up to the
  optimum of the system (Goldratt, OPT rule 10: https://www.jackvinson.com/blog/2010/12/20/the-rules-of-opt-precursor-to-theory-of-constraints).
- One number, one function. Money is the collector's (`station/fleet.py` window, `hive.py fleet`), a run's credits
  are `routes.earned`'s, the reserve is `surplus.py`'s, what a route carries is `fill.carries`, whose work a route is
  is `workclass.py`'s. stats.py imports them; it never computes them again.
- A cost is a positive number; net = income - costs. Every figure carries its window (hours) and its n (minutes,
  hours, runs, samples or pilots behind it). What no record holds is `not measured`, with the record that would be needed.
- Few, noisy samples: the median and the quartiles (q1-q3) instead of the mean, the median absolute deviation (MAD)
  instead of the standard deviation. Both resist outliers: half the data can be wild before they move (NIST
  handbook 1.3.5.6, https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm).
- Trend = this window against the window before, both of whole hours, each with its n.

## kpi -- the fleet as one purse

- Says: what the fleet earned an hour over 1, 6, 24 and 72 hours. Throughput (income: what the game paid us),
  operating expense (costs; of it fuel and repairs metered), steady net, paid once (rewards - bought), net of
  everything, net per ship-hour, the trend, the change of wallets plus treasury, the reserve and the surplus at the
  best bid, tax booked in 24 h, rent per cycle.
- Formula: 1, 6, 24 h are `fleet.json` totals.rates.windows, the collector's own figures (what `hive.py fleet`
  prints). 72 h and every trend: the minute-weighted mean of whole hours of `stats_money_hour`, each hour the
  collector's `window()` over its own samples. Net per ship-hour = net / mean ships. Holdings at bid = units x best
  bid within its depth (surplus.py).
- Net of the purse (`purse_per_hour`, the station's headline in the top bar and under Metrics, one window on both):
  net of everything + the treasury's own flows, i.e. its change between its two readings at the window's ends less
  the deposits our ships booked between them (rent, buildings it paid, money paid in or out). The fleet is one entity
  (consolidation): a move between two of its purses is neither income nor cost. Absent until both ends of a window
  carry a treasury reading (empire.json, carried in each sample since 2026-11-22).
- Window and n: n = minutes behind a window (1-24 h) or whole hours on record (72 h, trends).
- Sources: fleet/fleet.json, fleet/history.json, empire.json, stats_money_hour, surplus.py.
- Follows: throughput accounting (throughput, inventory, operating expense; https://en.wikipedia.org/wiki/Throughput_accounting).
- Caveats: history.json holds about 48 hours, so 72 h fills only as stats_money_hour grows (n says how many hours).
  Tiled hours match one window over the same span within about 1% (live copy 2026-11-18: 6 h 9,257 against 9,352;
  24 h 1,946 against 1,947). The treasury is read once at a time: the purse change needs two readings that many hours apart.

## contribution -- what each division gives the whole

- Says: per division (a) its own steady net (the collector's windows), (b) income enabled: the steady credits that
  ships of every division earned on the routes whose file its Admiral wrote, and the part of it others earned,
  (c) its service measure: Intel: age of the newest reading of each place the routes flown in the window use
  (median, max, share read within 3 h). Logistics: share of chain-hours at or above keep (stats_supply_hour), the
  reserve units it holds, net change. Military: kills and hunts flown (runs), ships lost (ship files' counter),
  combat XP per hour read. Trade: credits and credits per ship-hour of its sell runs. Mining: ore per run-hour and
  per ship-hour, the median days of supply of the reserve.
  (d) handed over (every division, since 2026-11-22): the units each gave by gift to the receivers of Trade and
  Logistics (data/stock/handover.jsonl) and what they would sell for now: per item, all givers' units within the
  depth of the best bid of any saved book, shared by units; beyond the depth or without a bid at 0, named.
- Formula: (b) sum of route_hour credits per route, grouped by the route file's first author (`git log
  --diff-filter=A`, cached in stats_route_author; asked again only for a new file).
- Sources: fleet.json, route_hour, runs, stats_route_author, readings, books, stats_supply_hour, stats_pilot_hour,
  data/stock/handover.jsonl, data/market/*.json.
- Follows: throughput of the whole system over local efficiency (theory of constraints, above); data timeliness
  for Intel (https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/information-management/guidance-data-quality.html).
- Caveats: the first author is who wrote the file, not who keeps it. A division's own net over 72 h is not measured:
  the collector's window over one hour does not add up per division (a move between our purses whose two sides fall
  into different hours); only the fleet's hours are summed. Whether a unit sold was surplus at that moment is not recorded. (d) is worth at today's books,
  not money: when Trade sells the goods it becomes Trade's income, so (d) and Trade's income are never added; one
  bid's depth is shared over the whole window.

## classes -- class capacity

- Says: per role, the places of its own class work open now against its ships; the spill = ships with no place of
  their own class (they fly another class's work or wait).
- Formula: places = sum over the routes `workclass.own(role)` and not shared, switched on, not parked, not resting,
  of max_ships, each never above `fill.carries` (ships + extra) when that is measured. spill = max(0, ships - places).
- Sources: game/routes, fill.carries, the table ships. n = routes counted.
- Follows: fleet utilization = active vehicle-time over available vehicle-time; low means idle assets or a fleet
  larger than its work (https://www.gpsinsight.com/blog/how-to-measure-vehicle-utilization-rate/).
- Caveats: a place is an upper bound: a route whose carry is not measured counts its max_ships.

## time -- where the ship-hours go

- Says: per role and fleet the share of ship-hours in own-class work, another class's work, missions paid once,
  shared work (sell, craft, fit its own stores), by hand, docked without work, in space without work, offline.
- Formula: work sampling: every 10 minutes each ship's state from the table ships (its route's class against its
  role); share = observations in a state / all observations. Ship-hours = mean ships per sample x hours. Beside it,
  the hours of runs started in the window by class, and the collector's minute samples (working, parked, adrift).
- Window and n: 24 h; n = ship observations; at least 6 samples (one hour) for ship-hours.
- Sources: stats_time, runs, fleet/history.json.
- Follows: work sampling (activity sampling): many instantaneous observations estimate the share of time per
  activity (APO, https://apo-tokyo.org/wp-content/uploads/2014/07/pmtt_010.pdf); empty running = deadhead share
  (https://strongtoweronline.com/insights/trucking-kpis).
- Caveats: a sample sees the state at that moment; the error of a share p from N observations is about
  2 x sqrt(p (1 - p) / N) at 95%.

## supply -- days of supply of the reserve

- Says: per reserve good held, needed, short, min and max (game/reserve.tsv, else `not set`), net change an hour
  over 24 h, days of supply (a good that runs down), hours to target (one that grows below its max or its demand),
  the routes that feed it and our ships on them now.
- Formula: days = held / (-change x 24); hours to target = (target - held) / change.
- Sources: surplus.py, store.reserve_flow (stock_hour), fields, supply_chains, the table ships.
- Follows: days of supply = inventory on hand / expected daily demand, the forward measure; min-max replenishment
  (https://inact.io/en/blog/inventory-kpis-7-metrics/, https://usersolutions.com/blog/glossary/min-max-inventory).
- Caveats: the change is net (gathered + bought - used - sold), not demand alone.

## gather -- gather against buy

- Says: per reserve good what a gathered unit cost, the best ask to buy it, the best bid to sell it.
- Formula: cost = the costs (minus credits) of the mine runs that sold nothing at fields that yield it / the units
  of ore they brought.
- Sources: runs, fields, books, surplus.py.
- Follows: make or buy: compare the relevant (avoidable) cost of making with the price of buying
  (https://openstax.org/books/principles-managerial-accounting/pages/10-3-evaluate-and-determine-whether-to-make-or-buy-a-component).
- Caveats: a field of several ores spreads its cost over all of them; ship time is not priced.

## refill -- what comes back by itself

- Says: per station and item how fast a bid's units come back after a take (and after a sale of ours), per field
  how fast it grows back, per herd how fast it regrows. `hive.py refill` prints this table.
- Formula: a recovery event begins at a take; its rate = units back before the next take / hours from the take to
  the last rise; the median and q1-q3 over the events, with n. A best bid is one step of a ladder: `hive.bid_moves`
  reads each step. Fields and herds: the median over the readings that rose. sum/h = hive.py's least-that-is-sure
  sum of rises over the hours watched.
- Sources: moves, readings (the store's raw rows, 7 days), runs.
- Caveats: a rise between two readings is the least that came back; a take with no rise after it is no event.

## xp -- skill per hour

- Says: XP per hour per role and skill, per route, and per ship the hours to its next Piloting tier (10, 20, 30,
  50 open tiers 2 to 5) at its own pace.
- Formula: each hour every pilot's skills are read (stats_pilot_hour; a row when a value moved; read_hours = hours
  since its reading before). Rate = XP gained / hours read. Per route: each reading's gain is split over the routes
  flown since the reading before by minutes (readings over 2 h are not split). Hours to tier = XP still needed /
  its Piloting XP an hour.
- Sources: ship_skills, catalog xp_per_level, runs. n = pilots or readings.
- Caveats: skills are read while a pilot is listed; the pause gives none.

## upgrades -- the next hull

- Says: per ship its hull and tier, Piloting, the Piloting the next tier of its class asks (none: the catalog
  names none), those hulls, and empty weapon, defense and utility slots.
- Sources: ships, ship_skills, hulls, ship_modules.
- Follows: replacement planning: age and use start a review; fit and cost decide
  (https://autosist.com/blog/what-is-fleet-replacement-planning).

## alerts -- control chart

- Says: which series' newest hour lies outside its own band: the fleet's steady net an hour, the idle share, each
  route's credits per ship-hour.
- Formula: band = median +- 3 x 1.4826 x MAD of the 7 days before the hour (Hampel identifier: 1.4826 x MAD
  estimates the standard deviation of normal data, so the band is the 3-sigma line); at least 24 hours of history;
  a series with MAD 0 is not judged.
- Follows: Shewhart individuals chart, 3-sigma limits (NIST 6.3.2.2, https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc322.htm);
  robust limits (https://blogs.sas.com/content/iml/2021/06/01/hampel-filter-robust-outliers.html); at least 30
  points for a chart of single observations (ASTM E2587, https://store.astm.org/e2587-25.html).
- Caveats: the raw median +- 3 x MAD (2 sigma) would flag about one normal hour in 23 per series. An alert asks for
  a look, never a change by itself. A slow drift is the EWMA's job (NIST 6.3.2.4,
  https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm): not built yet.

## Adding a figure

Write its section here first (says, formula, window and n, sources, follows, caveats), then build it in
`game/fleet/stats.py` from the function that already computes its parts, with a test, and its view in `hive.py stats`.
