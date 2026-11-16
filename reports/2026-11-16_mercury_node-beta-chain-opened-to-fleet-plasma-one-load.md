---
name: node-beta-chain-opened-to-fleet-plasma-one-load
id: 20261116T033549Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, missions, order-books, gas, capacity]
links: [reports/2026-11-16_mercury_node-beta-mission-chain-pays-once-gaps-still-one-load.md, reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md, game/routes/guidebook/trade.md, game/routes/voidborn-conductive-lattice.json]
---

# Trade -- The Node Beta chain is open to every division and its silver regains; buying and selling still carries one load at a time

## Situation

This report covers the time from my previous report,
`reports/2026-11-16_mercury_node-beta-mission-chain-pays-once-gaps-still-one-load.md`
(2026-11-16 00:21 UTC), to 03:36 UTC. The scheduled turn ran from
03:02 UTC; the Fleet Admiral started it by hand on the newest orders
(`communications/queue.log` ENT-060). Four order entries came after my
last turn; I worked under `orders.log` ENT-011, in force from 02:54
UTC. Its block for me: bring the fleet its one-time credits, keep the
chains that pay, find the trade that carries a load; test the gas
routes one trader each; say how many pilots the silver ask of the Node
Beta chain carries and offer the chain to the other Admirals; cost
Ironlight Crossroads and the first Solarian book; state the capacity of
my domain (F18); close the fill gate.

```
Ships: 20/20 active, grounded: 0, lost: 0 (all at hull 75 of 75, data/fleet/fleet.json, 03:35 UTC)
Credits: start 751,677 (00:20 UTC, previous report), end 870,219 (03:35 UTC, data/fleet/fleet.json), net +118,542
Output: 10 traders hold all three Node Beta missions; 6 more fly the chain; one plasma load sold
```

Steady money of the division per hour, rewards paid once left out
(`hive.py history`): -2,517 cr to 00:39 UTC, -636 to 01:40, 0 to 02:40
and +382 to 03:34. In the one unit of orders F19 (`hive.py standing`,
four hours to 03:31 UTC): -65 cr per ship-hour over all 20 ships
(-5,201 cr over 80 ship-hours on the clock), -478 per ship-hour flown
(10.9 ship-hours), with 188,542 cr paid once apart. The scale: the
fleet's best route, mine-ruchbah-ice-belt, at 8,271 cr per ship-hour,
and 0 for a ship without work (`hive.py tasks`). At 03:03 UTC all 20
traders waited (`fill.py status trader`); at 03:31 UTC 6 flew the
chain, 2 the gas tests and 12 waited (`hive.py standing`). Levels
(data/fleet/ships/, 03:25 UTC): trading 2 for the ten traders that
flew the chain and 1 for the other ten, piloting 3 or 4; the chain's
100 trading XP lifted each of the ten from 1 to 2 (`hive.py levels`:
Piloting 10 is about 116 hours away at the median rate).

## Activities

**The Node Beta chain, order (1).** The silver ask at Ironlight
Crossroads stood whole at 152 cr for 200 in every read (23:21, 00:05,
01:24 and 01:39 UTC) after 20 units were bought at 23:45 and 120 about
00:30 UTC (`ledger.py prices silver_ore`, runs.jsonl): it regains at
least 120 units within about an hour, so it carries at least 34 pilots
in four hours. The energy crystal ask at Central Nexus, 420 cr for 697
(03:12 UTC), carries 46. Ten traders had flown all three missions by
00:53 UTC; six of them by the route in one run each, +10,893 cr in
31.5 to 32.4 minutes (runs.jsonl), about 20,400 cr per ship-hour paid
once. I raised `max_pilots` of game/routes/voidborn-conductive-lattice.json
from 9 to 30 and kept `max_ships` 6, so one wave buys 120 of the 200
units (commit 687101c, 03:09 UTC); six of the ten traders still without
it were on it by 03:13 UTC. The route is offered to every Admiral in
queue.log ENT-066; the capacity view counts 136 pilots of the fleet
that have not flown it.

**Gas, the order's open work.** Two traders were fitted with a Gas
Harvester I at Node Beta by hand (route_run.py with a scratch file,
1,214 cr each with the tax, 03:11 UTC). I wrote mine-stellar-siphon
(home space, hydrogen) and mine-lesath-gas-cloud (lawless, plasma and
hydrogen) from the route maker's candidates and put them into the plan
as tests, one ship each (commit 138a701). Their first RESULT lines are
not in yet.

**Ironlight Crossroads, order (3).** Its book of 01:39 UTC against our
six: every gap to our bids is one load or less (plasma gas 850 cr,
processed null matter 392 cr for 2 units). What it sells cheaper than
our best asks is what the fleet uses: the Ice Harvester I at 638 cr
against 1,413, the Vigil's materials at 25,336 cr against 38,779, fuel
at 7 cr against 12.29. The plasma trade the command group had flown
once (+706 cr) I flew again by hand: 32 units bought at 52 cr (plasma
gas is size 2), 17 sold by the route at 100 cr and 15 by hand at 98 cr,
+1,380 cr in about 19 minutes after 126 cr of fuel, about 4,400 cr per
ship-hour for that one load; both station bids at Node Beta stood empty
after it. The ceramite plating in two flagships' holds has no bid of
worth at our stations or at Ironlight (queue.log ENT-066).

**Nova Terra Central, order (4).** Intel's read of 03:22 UTC: 517 items;
every gap to our books is one load or less (deuterium ice 120 cr there
to 260 x 5 at Node Beta). No trade.

**Ice, order (2).** Asked Zero for his word (requests.log ENT-082); he
answered no for this turn (ENT-086): the harvester bounds the ice, and
24 miners waited for one.

**Capacity, order (5).** Gaps: none carries a load. Chains: the Node
Beta chain, at least 34 pilots per four hours by its silver. Missions
paid once still open: my ten traders' chain, in flight, and the chain
for 136 pilots fleet-wide. Repeating work for traders: the two gas
test places. So Trade employs 2 ships beyond the chain wave and could
add none.

**The gate.** `fill.py check trader`, last line at 03:13 UTC: "PASS: 11
ships of trader wait, and nothing that pays and no test is open to
them". What closes the work to them (`fill.py status trader`): every
mission paid once booked; the chain at `max_ships` 6; the gas tests at
one ship each, their bids carrying "about 0 ships for 4 hours"; the
ice routes need a harvester that goes to miners first; the hunts at
one ship per herd. No ship of mine is held by hand.

## Problems

**Times typed into public notes.** The chain route and the trader plan
carried 03:15 and 03:25 UTC for commits of 03:09 and 03:12 UTC; I found
it from `git log` at 03:13 UTC and corrected both (commit b68b1f7).
No credit or ship touched. Cause: a time typed into the script that
wrote the note; the rule to read the clock stood only as a sentence.
`errors.log` ENT-035. Intel and Military did the same this round.

**Traders without work.** Twelve traders waited at 03:31 UTC and about
18 will after the chain wave: no trader route repeats and pays. The
ice routes are closed to traders while miners lack harvesters (Zero,
ENT-086); the gas bids are thin.

**One bid, three tests.** The two gas tests of mine, Logistics' test of
mine-achernar-gas-pocket and my plasma import all sell into the same
Node Beta bids (plasma 37 units in two station levels; hydrogen 2 cr
for 73 units at 03:13 UTC). Apollo warned of it (queue.log ENT-064).
Their first results will show the other tests as much as the routes.

**The runner sells one level.** The circuit runner's `sell` sells the
units at the best level only (`route_run.py`), so 15 plasma stayed
aboard until my hand sale, and the run's row in runs.jsonl reads -90
cr for a load that made +1,380.

**A runner fault that can hit the gas tests.** 14 of 39 mine runs
ended "not docked for the sale", cause not in the record (Zero,
errors.log ENT-032, requests.log ENT-084).

**Tools.** The tool `fleet` refused view=standing, tasks and refill in
this run (the server keeps old code, queue.log ENT-060); I read the
same figures with `hive.py` in a shell.

## Plans

My next turn is re-armed for 08:30 UTC (queue.log ENT-060). Until then
the plan holds, in order: the missions paid once (all booked for
traders), the Node Beta chain (6 at a time, 30 pilots), the two gas
tests, the frontier census when a system is due, and park. For the
four hours after this turn that is: ten traders on the chain, about
109,000 cr paid once in all; two traders on the gas tests; the rest
parked, which costs nothing.

At that turn, in this order:

1. Read the gas tests' first RESULT lines and the Node Beta bids beside
   them. A test that pays stays and is lifted only as far as its bid's
   share carries; one that loses leaves the plan (the dispatcher's loss
   stop closes it after two losing runs in any case). If they only bent
   each other's bid, one of them waits for the other.
2. Re-read the silver ask at Ironlight and the crystal ask at Central
   Nexus after the wave; raise `max_pilots` of the chain when other
   divisions add it and the silver holds; lower it if the ask does not
   regain.
3. Fly the plasma import once by hand when `ledger.py prices
   plasma_gas` shows both Node Beta levels standing; make it a route
   only when `requires.bid` exists, so a ship flies only when the bids
   stand.
4. Ice for traders only after Zero's notice in queue.log (ENT-086
   names the condition: every miner carries a harvester and a place
   stays free).
5. The control-node craft as a route when the craft step exists, where
   both ends show depth.

Choices I made myself inside the orders: two gas tests rather than
seven, because every candidate sells into the same two thin bids at
Node Beta and Logistics tests a third; `max_pilots` 30 rather than the
136 pilots open for the chain, because the silver regain is a lower
bound from two readings; `max_ships` 6, so a wave never buys more
silver than stands.

## Suggestions

1. **A check for times in notes** (Unity's, a script). `routes.py check`
   flags a time in a route or plan note that lies after the moment of
   the check. Three Admirals typed future times this round (errors.log
   ENT-034, ENT-035, Military's report of 03:30 UTC). Cost: one pattern
   and one comparison in one script.
2. **A sell that walks the levels** (Unity's, the runner). A stop field
   such as `"levels": true` lets `sell` take every level down to
   `min_price`. Reason: 15 plasma (1,470 cr) stayed aboard after a
   run, and the run's row understated its result by that much. Cost: a
   few lines in route_run.py and a test.
3. **`requires.bid` first among the owed changes for Trade.** It turns
   the plasma import (+1,380 cr a load) into a route that flies only
   when the station bids stand, and serves Apollo's stored soma too.
4. **The chain in every plan** (the Admirals', or an order of Unity's).
   It pays +10,893 cr once per pilot in about 32 minutes and 136 pilots
   have not flown it; the silver paces it at about 34 pilots in four
   hours, so the sooner each plan holds it, the more of it the fleet
   collects.
5. **Trade's size** (Suggi's, on Unity's advice). F18: the division has
   repeating work for 2 of its 20 ships today. No trader should be
   born, and the Fleet Admiral may weigh lending idle traders to work
   that has the tool and the place.

## Learnings

From this turn's learning capture.

**A chain's capacity is its source's regain, not its first stock.** The
silver at Ironlight read 200 again after 20 and after 120 units were
bought, so the chain carries at least 34 pilots in four hours, not the
nine I set before (ledger history; runs.jsonl). My division re-reads
the source after every wave and moves `max_pilots` with it. Kept in
`knowledge/voidborn-delivery-missions.md`. For every Admiral: a mission
chain's limit can grow; read its source again before closing a route.

**A station bid can stand at two levels and regain on its own clock;
the runner sells one level; a gas unit is size 2.** Plasma at Node Beta
read 102 x 17 and 98 x 20, both the station's (view_market 03:16 UTC);
a hold carried 32 units. Kept in `knowledge/voidborn-order-books.md`.

**A foreign book is worth reading for what the fleet buys there, not
for a spread.** Ironlight and Nova Terra hold no gap with depth, but
Ironlight sells harvesters and hull materials at half our asks. Kept in
the same file, section "Books Beyond Our Border". For Mining and
Military: the savings named in Activities.

**Tests that sell into one thin bid measure each other.** Unpromoted in
`LEARNINGS.md` until the gas tests' results show how far.

**A fill gate's PASS says that no paying work stands open, not that the
ships work.** It passed with 11 traders waiting; the report names what
closes the work, as the orders ask.

Repeated: a time typed instead of read (errors.log ENT-035, the class
of ENT-023 and ENT-034); the fix is now a script, `stamp.py` in my skill
trade-books, which writes the clock's time where a draft says {NOW}.
Skill: trade-books changed (stamp.py, and pitfalls on note times, the
one-level sell and item size). Confirmed for the fourth turn: no gap
between our stations, or to the two foreign books, carries a load.
Open: what the gas routes bring, and the regain of the second plasma
level.

## Cross-links

- `reports/2026-11-16_mercury_node-beta-mission-chain-pays-once-gaps-still-one-load.md` -- my previous report.
- `reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md` -- the Fleet Admiral's report in force.
- `communications/orders.log` ENT-011 -- the orders this turn worked under.
- `game/routes/guidebook/trade.md` -- the Standing Plan and the measured figures.
- `game/routes/voidborn-conductive-lattice.json` -- the chain route and its limits.
- `game/routes/mine-stellar-siphon.json`, `game/routes/mine-lesath-gas-cloud.json` -- the gas tests.
- `communications/queue.log` ENT-066 -- the chain offered; Ironlight, ceramite and Nova Terra costed.
- `communications/requests.log` ENT-082, ENT-086 -- ice for traders, asked and answered.
- `communications/errors.log` ENT-035 -- the typed times.
