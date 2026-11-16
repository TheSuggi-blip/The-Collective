---
name: guidebook-mining
id: 20261115T205803Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# mining.md -- Guidebook of the Mining Division

Kept by Zero; read by every member. What the Mining division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Zero writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`. Every earning is in credits per ship-hour
  (orders F19).
- The plan in force is the division's plan file (data/plans/plan-mining.md
  in the unit, the tool plan); `game/routes/plan-miner.md` shows it with
  counts and no names. Every route with its figure: `game/routes/master-index.md`
  and its sub-indexes. The fleet as it flies: `python3 -I -B game/fleet/hive.py
  standing`; the next four hours: the tool hive, verb forecast.

## Standing Plan

What the miners fly between two turns (2026-11-16 23:30 UTC, orders.log
ENT-019). A free miner takes the first open route of the list First (the
missions that pay once), its own routes, the list Then (census, park).
Every miner's own routes are templates (section 2): one ship-list in two
halves, `@ice-sell` and then `@reserve-prism` or `@reserve-hamal`, so the
division is spread over two iron fields. Seven miners carry a one-ship
test beyond the border in front of them. Credits per ship-hour are
steady money from `route_earnings` (the tool sql) at 23:02 UTC, over the
window named; `carries` is the tool fill's reading at 23:19 to 23:28 UTC.

| # | Route | Ships | Carries | Per ship-hour, measured | What it is for |
|---|---|---|---|---|---|
| F | The once line of the Central Nexus board, the Precedence, Concurrent, Substrate and mining missions, the First Hunts | their limits | -- | judged with the reward | Every pilot flies them first; 98,576 cr paid once to miners in the 4 hours to 23:00 UTC (`hive.py standing`) |
| 1 | `carry-null-matter-synchrony-nexus` | 1, a test | bid 221 cr x 10, 106 in all levels | not measured | Stored null matter (350 at Synchrony) into the one bid for it |
| 2 | `drain-methane-experiment` | 1 | bid 36 cr x 284 at The Experiment | 17,639 (13 runs, 12 h) | Stored methane sold where it lies |
| 3 | `drain-ice-nexus`, `drain-ice-node-alpha`, three `carry-ice-*-nexus` | 2, 2; 3, 2, 3 | a water-ice bid of 30 or 65 units | no run in 11 h | 18,546 water ice stored by miners; the bids read 34 cr x 5 and 27 cr x 2 |
| 4 | four water-ice mine routes to Central Nexus | 1, 2, 1, 1 | open on an order of 300 units at its best price | no run in 12 h | New ice only on a deep order |
| 5 | `gather-acubens-belt-carbon` | 1 | about 1 (grows back 56 to 98 an hour) | new | Carbon for the circuit boards |
| 6 | `gather-ironhollow-fading-signal` | 5 | about 7 (grows back 518 an hour) | -220 (1 run) | Iron beyond the border into The Experiment |
| 7 | `gather-schedar-belt` | 1, a test | 142,846 above its floor | new | Iron beyond the border, one jump from Node Beta |
| 8 | `gather-gsc-0027-prism-scatter`, `gather-hamal-crystal-bloom` | shared, 66 and 76 | 32,841 and 57,205 above floor | -139 and -168 (124 runs each, 4 h) | Iron into Node Beta; full at their limits most of the turn |
| 9 | `mine-acubens` | shared, 18 | closed: 331 iron under its 10,000 floor | -173 (3 runs, 4 h) | Opens again when the field grows back |
| T | `mine-gliese-876-belt`, `mine-stillwork-belt`, `mine-dewfall-fray`, `mine-gaugewatch-belt`, `mine-gossamer-null`, `mine-gsc-0033-void-whisper`, `mine-thinspace-rubble` | 1 each | -- | Gliese 876 Belt 2,880 (2 runs, 12 h); the others new | Tests beyond the border: null matter sold at Central Nexus, iron stored there |
| Then | `census-frontier`, `park` | 12 for the fleet | -- | -470 (72 runs, 4 h) | Reading, when nothing else is open |

Why this plan. The buyers bound Mining, not the ships or the fields.
Water ice: miners store 18,546 units (the storage book, 23:02 UTC) and
the bids hold 2 to 6 units at their best price; no new ice is mined for
sale. Silicon ore: the one field we read that holds it (Nexus Prime,
Material Harvesters) reads 0 to 2 units all day; no route can gather it.
Carbon ore: one field in our space holds any (Acubens Belt, 259 units).
Iron ore: the reserve takes 503,400 and the fleet holds 202,343 (the tool
stock, view=reserve, 23:02 UTC); gathered at about 1.0 cr (Prism
Scatter) to 1.8 cr (Hamal) of fuel per unit of iron against an ask of
4 cr at Central Nexus (28,337 units at its best price, 23:02 UTC). The
two shared iron fields stood full at 66 and 76 ships of every division,
so new iron places were opened beyond the border.

What would change it: a water-ice order of 300 units or more at Central
Nexus (the gated routes open by themselves); the first RESULT line of
each test (Schedar Belt lifted toward what it carries; a test that meets
a hostile ship leaves the plan, rule F13); a silicon field found by
Intel; carbon bought cheaper than gathered (4 cr asks against about
1.2 cr gathered). Each turn starts with `stalled.py` of the
mining-chains skill.

## 1. Route Guides

How each kind of route of this division is flown: the fit and the
skills it needs, its place, its steps, what opens and closes it. A
credits figure in this section is a dated reading and no verdict: what
a route earns now is in the fleet's database with its age (rule F22;
the tool `routes`, the view `route_earnings`).

### Drains and carries of stored goods (kind `circuit`)

- Fit: none; any miner flies them. Trains Piloting and Trading.
- A drain sells at the station where the goods lie: stop 1 stores the
  hold, withdraws the item and sells it into the bid at `min_price` or
  more (the withdraw takes only what the bid takes); stop 2 stores what
  is left. A carry withdraws a load (65 units, `qty`), flies it to the
  bid's station, sells, stores the rest there.
- Opens only for a pilot that stores the item itself (`requires.stored`,
  per pilot) while a book read within the hour shows the bid
  (`requires.bid`). Comes first in every list: what is stored is sold
  before more is mined.
- Readings: `drain-methane-experiment` 17,639 per ship-hour over 13 runs
  (12 h to 23:02 UTC), about 2,280 cr a run of 7 minutes; the water-ice
  drains and carries flew no run in 11 hours (no bid of 30 units).

### Ice mine routes (kind `mine`, with `sell`)

- Fit: Ice Harvester I (a mining laser alone takes no ice). Trains
  Mining and Piloting.
- `mine.py` mines for `minutes`, flies to the station, sells the hold
  then the pilot's storage there into every bid level at the floor or
  more, stores the rest.
- Opens only on `requires.bid`: the Central Nexus routes on an order of
  300 water ice at its best price. Count the jumps from field to buyer
  first: one-jump routes measured 7,280 to 8,950 per ship-hour on
  2026-11-16 morning, four- and five-jump routes 1,210 to 2,990.
- Methane comes with the water, not alone: Ruchbah Ice Belt gave 10 to
  17 methane in loads of 311 to 344 units (four runs, 10:11 to 11:39
  UTC, 2026-11-16), about 3 to 5 percent.

### Standing work for the reserve (kind `mine`, no `sell`)

- Fit: Mining Laser I. Trains Mining (one XP a unit mined).
- Mines for 45 minutes, stores everything at its station, sells
  nothing; closes below its `min_left` floor and opens when the field
  has grown back. It is never judged on its pay (rule F8).
- Readings, the 4 hours to 23:30 UTC (data/routes/runs.jsonl, steady
  money from route_earnings): Prism Scatter 207 ore a ship-hour, 65%
  iron by what the field gave up, about 135 iron, -139 cr a ship-hour;
  Hamal Crystal Bloom 180 ore, 51% iron, about 92 iron, -168 cr; Acubens
  Shadow Pocket 281 ore while it was open. Ironhollow's first run: 233
  ore in 45 minutes, -165 cr (2026-11-16 19:16 UTC).
- What the fields grew back (hive.py refill, 23:03 UTC): Ironhollow
  Fading Signal 522 iron an hour, Pherkad 267, LHS 1140 Prospectors'
  Leavings 258, Antares Afternoon Drift 254; Acubens Belt 56 carbon
  (readings, 12 h); Prism Scatter and Hamal near 0 while ships work
  them. A field we read was seen back at 100,000 between two reads
  (Prism Scatter, 2026-11-16): how a field refills in one step is not
  known.

### Tests beyond the border (kind `mine`, one good sold)

- Written by the route maker, added one ship at a time by the tool
  fill. Each sells null matter at Central Nexus (221 cr x 10, 106 units
  in all levels, 23:03 UTC) and stores the iron and copper there.
- `requires.empty_hold`; one ship until the first RESULT line (rules F8,
  F13). Read the pilots met at the place before lifting (the table
  `met`): combat drones of the faction tagged BUSY were seen in combat at
  Ironhollow Fading Signal (19:52 UTC) and Gliese 876 Belt (23:04 UTC).
- Seven tests share one bid of 106 units: their null matter is a bonus;
  the iron they store is what they are for.

### Fits by hand

- `refit.py` of the mining-chains skill swaps a module at a station.
  When the engine's goal answers 409 ("another request ... is already
  being processed") for minutes, the raw market `buy` takes the best ask
  at once: read the ask first (2026-11-16 23:16 UTC, one Mining Laser I
  at 1,600 cr plus 1% at Central Nexus).

## 2. Route Templates

A kind of work is a named list of routes: a template, kept in
`game/routes/templates/mining.json` and listed in
`game/routes/templates-mining.md`. A ship's row in the plan file names a
template as `@<name>`, alone or beside routes of its own.

| Template | For | Trains | Fit |
|---|---|---|---|
| `ice-sell` | Stored null matter, methane and ice sold where a bid stands, then the water-ice mine routes on a deep order | Mining, Piloting, Trading | none for the drains; Ice Harvester I for the mine routes |
| `reserve-prism` | Carbon first, then iron: Ironhollow, Schedar Belt, Prism Scatter, Hamal, Acubens | Mining | Mining Laser I |
| `reserve-hamal` | The same with Hamal before Prism Scatter | Mining | Mining Laser I |

| Task | How |
|---|---|
| See the templates and how many ships use each | the tool `plan` with `action=templates` (`plan.py templates`) |
| Make or change one | `plan.py template <name> <routes with commas> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py set <ships> @ice-sell,@reserve-prism` |

A ship born tomorrow gets `@ice-sell,@reserve-prism` (or `-hamal`) and
is at work within the minute. A one-ship test goes in front of a ship's
templates as a route of its own.

This guidebook keeps no list of routes that did not pay (Suggi,
2026-11-16; rule F22). What a route earns now, with its age, is asked
each turn: the tool `routes`, or `SELECT * FROM route_earnings` through
the tool `sql`.

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first.

| Route | Pays | Measured | Date | Note |
|---|---|---|---|---|
| `voidborn-concurrent` (Concurrent Approval) | 3,000 cr | 39 miner runs, +115,037 cr, of it 117,000 once | 2026-11-15 | Its two neural soma come with the accept |
| `voidborn-mining-missions` (Iron Supply Run, Copper Requisition) | 1,500 + 1,800 cr | 3 runs by 22:24 UTC, +6,430 cr | 2026-11-15 | Booked for every miner now |
| `voidborn-precedence` | 4,000 cr | 146 runs of the fleet, 580,000 cr once | 2026-11-16 | Booked for every miner now |
| `voidborn-first-hunt-*` (three herds) | 930 to 970 cr | one ship each at a time | 2026-11-16 | The home herds read 0 to 3 grazers (queue.log ENT-063): slow |
| `voidborn-signal-fragments` | 7,000 cr | 40 miner runs, +275,879 cr | 2026-11-16 08:00 to 12:20 UTC | Pilots with navigation 3 |
| `voidborn-conductive-lattice` | about 10,900 cr | 32 miner runs, +273,451 cr | 2026-11-16 08:00 to 12:20 UTC | The Node Beta chain |
| `voidborn-network-expansion` | 1,500 cr | 12 miner runs, +17,374 cr | 2026-11-16 08:00 to 12:20 UTC | After First Steps |

## 4. Levelling Guide

Which skills a ship of this division levels and on which work (rule
F23): the work of its own role first, gathering ore only when none is
open. A miner's role is mining, so gathering for the reserve trains its
own skill. Levels below: `hive.py levels` (the tool fleet, view levels),
2026-11-16 23:15 UTC, 60 miners, 28 hours played (median): Piloting 3 /
6 / 7 (lowest, median, highest), 155 XP an hour; median Mining 5 (116 XP
an hour), Deep Core Mining 5 (126), Navigation 4 (51), Trading 2 (16),
Exploration 2 (12); 63 hours to Piloting 10 at that rate. At 18:40 UTC,
40 miners: Piloting 5 / 5 / 7, Mining 5, 77 hours to Piloting 10.

| Kind of ship | Fit | Work and template | Skills it raises | Next step |
|---|---|---|---|---|
| Ice miner | Mining Laser I, Ice Harvester I, Pulse Laser I | `@ice-sell` first, then `@reserve-*` | Mining by every unit mined (ice like ore); Piloting by the jumps; Trading on the drains | Ice Harvester II (made by hand, section 5) once a water bid carries ships again |
| Laser miner (born 2026-11-16 evening) | Mining Laser I, Pulse Laser I | `@reserve-*` and the drains of `@ice-sell` | Mining, Deep Core Mining; Piloting on the far tests | An Ice Harvester I (687 to 709 cr at Ironlight Crossroads, 1,413 cr at home) only when an ice bid carries more ships than carry one |
| Test miner beyond the border | Mining Laser I, empty hold | one test route, then its templates | Piloting and Navigation (4 to 7 jumps a way), Mining | Lift the test when its RESULT line holds |

- Mining XP is one point per unit mined. Level 5 needs 900 XP, level 6
  1,285 (the pilots' files).
- Mining level shifts which deposit a pull picks, not how much it
  yields: the rarer deposit is picked 10% of the time at level 0, 50% at
  20 (the official miner guide, read 2026-11-15). At Mining 4 a nebula
  gave 14.5% energy crystal where its richness alone gives 8.3%.
- Piloting 10, 20, 30 and 50 open hull tiers 2 to 5. A route with more
  jumps trains more Piloting per hour: the tests beyond the border (4 to
  7 jumps) and the carries do; the gather routes one jump from Node Beta
  do least.

## 5. Ships and Fits

- The hull: Threshold (tier 0): 2 utility slots, 16 cpu, 30 power, hold
  65. The ice miner flies the Mining Laser I and an Ice Harvester I in
  the two utility slots and the Pulse Laser I in its weapon slot: cpu 8
  of 16, power 17 of 30 (`install_mod`, 2026-11-15).
- Ice Harvester I: 1,413 cr at our stations plus 1% tax; a fit by route
  costs 1,449 to 1,460 cr with the fuel (four fit routes, started
  2026-11-16 03:15 UTC, 3.6 to 4.2 minutes each). At Ironlight Crossroads (LHS 1140,
  beyond the border) the fit costs 687 or 709 cr with fuel and tax,
  8.7 to 12.4 minutes from Node Beta (9 runs to 04:22 UTC,
  `data/routes/runs.jsonl`): about 760 cr less a ship than at home. 18 asks at 638 cr stood
  at 04:24 UTC; 20 asks at 518 cr at 07:42 UTC. 39 of the 40 miners
  carry one (2026-11-16 08:01 UTC, `hive.py standing`).
- A hold is counted in space, not in units: each row of the pilot's
  `state/cargo` carries a `size` (tungsten and lead ore 2, ice and the
  other ores 1). The game refused a withdraw of 23 units into a hold
  with 9 free (2026-11-16 12:15 UTC).
- Goods move between two of our own pilots docked at one station:
  `deposit` (spacemolt_storage) with `source` storage and `target` the
  other pilot's name gives them from the one storage into the other
  (2026-11-16 08:11 UTC, silicon ore and energy crystal to Logistics,
  read back from both storages).
- Size a route that buys a module by the asks at its one station, one
  ship at a time where they are few (errors.log ENT-026). One route per
  station, each with its own `max_pilots`.
- Nitrogen Vent (cpu 4, power 9): with the harvester in place of the
  laser it lifted the water share of a load from 59% to 83% (one run
  each). The one vent ship took a Mining Laser I in its place on
  2026-11-16 23:16 UTC (1,600 cr plus 1% at Central Nexus): with no water
  bid it had no work; the vent lies in its storage at Central Nexus.
- Mining Laser I asks, 2026-11-16 23:12 UTC: 1,433 cr at Node Alpha and
  Sirius, 1,442 at a player's station in LHS 1140, 1,600 at Central Nexus
  and The Experiment, 1,791 to 1,942 at the others.
- A gas miner (Gas Harvester I beside the laser) has no slot left for an
  ice harvester; `requires.without_module` takes one module only, so the
  gas route stands before the ice fits in the plan.
- The next step of the fit: Ice Harvester II, made by hand from 1 Ice
  Harvester I, 2 ceramite plating, 3 liquid nitrogen and 1 power cell
  (catalog `build_ice_harvester_ii`; cpu 6, power 12, base value 1,800),
  on offer at 2,130 cr at Ironlight Crossroads (queue.log ENT-046). Its
  gain in units a minute is not in the catalog and not measured: one
  miner tests it once the waiting miners carry the Mark I.
- The next hull: tier 2 opens at Piloting 10, about 119 hours away for
  the median miner. Until then the money goes into harvesters (orders
  F17, strategy principle 1).
- Extraction filters take one ore out of a pull's draw (Magnetic Ore
  Separator, Flotation Cell, Electromagnetic Refinery, Isotope
  Separator); not bought: no rare ore of our fields has a buyer with
  depth.

## 6. Tests Flown

### Energy crystal at the nebula of `hunt-gsc-veil-ray`, 2026-11-15

One miner (Mining 4), 21:22 to 22:22 UTC, by hand: 166 units in three
loads (24 energy crystal, 94 iron ore, 48 copper ore), one palladium
ore bought at 436 cr, one focused crystal crafted in a station
workshop (24 ticks, no credit cost) and sold at The Experiment for
1,466 cr (a station bid of one unit), four raw crystals sold at 40 cr.
Result: +1,022 cr in 59.9 minutes after fuel and the palladium, about
1,020 credits per ship-hour; the bid was 40 cr after the sale.

### Ice at Wolf 1061 (frontier), 2026-11-15

One miner (Mining 4), by hand, 22:25 to 23:01 UTC, with one Ice
Harvester I bought at Synchrony: 126 units in two loads (water ice 77,
nitrogen 40, methane 5, deuterium 4); sold at Synchrony, water ice at
34 to 36 cr, methane at 47. Result: +2,688 cr in 30.1 minutes after
fuel, about 5,360 credits per ship-hour, one run. It opened the ice
routes of section 1.

### Fit routes per station, 2026-11-16

Four fit routes, one per station with asks, each `max_pilots` the asks
there and one ship at a time: the first runs at Node Beta, Node Gamma,
Synchrony and The Experiment fitted at 1,449 to 1,460 cr with fuel in
3.6 to 4.2 minutes each (`data/routes/runs.jsonl`, started 03:15 UTC); no buy above
the limit and no run without an ask, against six of ten runs that
found no ask when one route served ten fields (2026-11-15).

### Loops without a runner, 2026-11-16

Not a test: after the engine's restart of 02:00 UTC five miners flew
mining loops with no runner for about 65 minutes; the loops stored
their ice and sold none. Stopped by hand at 03:07 UTC; three sold what
the loops had stored, 1,111 water ice and 23 methane, +42,928 cr in
their wallets (errors.log ENT-032). A ship shown "busy by hand (loop)"
with no hand hold in `data/fleet/orders/` is such a loop.

### Stored methane drained, 2026-11-16

`drain-methane-experiment`, one ship at a time from 18:56 UTC: 13 runs
to 23:02 UTC, 17,639 credits per ship-hour (route_earnings), about 2,280
cr a run of 5 to 12 minutes; the withdraw step took only what the bid
took. 1,127 stored methane at 18:00 UTC; 479 stored and a bid of 284 left
at The Experiment at 23:02 UTC.

### Iron at Ironhollow Fading Signal, 2026-11-16

One miner, 19:16 UTC: 233 ore in 45 minutes into storage at The
Experiment (one jump), -165 cr (data/routes/runs.jsonl); no stranger in
its notes. The field grew back about 520 iron an hour between reads with
no ship of ours on it. Lifted to 5 ships at 23:25 UTC.

## 7. Open Tests

- The one-ship tests beyond the border (Standing Plan, row T): the first
  RESULT line of each, then lift toward what its field carries or take
  it out when a hostile ship meets it (rule F13).
- `gather-schedar-belt`: iron share of a load and the minutes a run takes
  one jump from Node Beta.
- `carry-null-matter-synchrony-nexus`: whether a carry of 65 sells into a
  bid of 10 units at its best price and 106 in all.
- `gather-acubens-belt-carbon`: carbon a run against the field's regrowth
  of 56 to 98 an hour.
- A Flotation Cell (filter_copper_ore) in place of the ice harvester on
  one iron miner: the iron share of its loads against 51 to 65%. The
  harvester of one miner lies in its storage at Node Beta since
  2026-11-16 19:01 UTC; no cell bought yet. Store the hold first.
- Deuterium ice: a bid of 175 cr x 6 at Node Beta; 3,273 stored in the
  fleet, 2 cr bids elsewhere (the tool stock, surplus, 23:04 UTC).
- Methane ice: 36 cr bids of 1,000 at six stations (23:02 UTC). The
  fields hold little of it (Ruchbah 3,483, Wolf 1061 564, Achernar 302)
  and it comes as 3 to 5% of an ice load.
