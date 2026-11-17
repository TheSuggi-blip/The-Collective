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

What the miners fly between two turns (2026-11-17 03:22 UTC, orders.log
ENT-025). A free miner takes the first open route of the list First (the
missions that pay once), its own routes, the list Then (two shared gather
fields, census, park). Every miner's own routes are templates (section
2): `@ice-sell` and then `@reserve-prism` or `@reserve-hamal`, so the
division is spread over the iron fields. One miner carries a one-ship ice
test in front of them. Credits per ship-hour are steady money from
`route_earnings` (the tool sql) at 03:02 UTC; `carries` is the tool
fill's reading at 03:15 UTC.

| # | Route | Ships | Carries | Per ship-hour, measured | What it is for |
|---|---|---|---|---|---|
| F | The once line of the Central Nexus board, the mining missions, the First Hunts | their limits | -- | judged with the reward | Every pilot flies them first |
| 1 | `carry-null-matter-synchrony-nexus`, `drain-methane-experiment` | 1, 1 | one bid each, regains 0 and 33 an hour | 39,606 (2 runs, 12 h); 17,789 (17 runs, 12 h) | Stored null matter and methane sold where a bid stands |
| 2 | `drain-ice-nexus` (a test: gate 5 units), the other ice drains and carries | 1; 2, 3, 2, 3 | Central Nexus water ice shows 1 to 5 units at its best price at every read since 2026-11-16 13:36 UTC | no run in 15 h | 29,503 water ice stored by the fleet; the test reads whether a bid of 5 refills often enough to pay |
| 3 | four water-ice mine routes to Central Nexus, `mine-groombridge-34-ice-fields` | 1, 2, 1, 1; 1 | open on an order of 300 units at its best price | 434 (1 run, Groombridge) | New ice only on a deep order |
| 4 | `store-hold-central-nexus` | up to 40 | -- | standing | A ship a run left loaded stores its hold; head of both reserve templates |
| 5 | `gather-acubens-belt-carbon` | 1 | under its floor of 60 carbon at 03:02 UTC | -233 (3 runs, 12 h) | Carbon, the only field in our space that holds any |
| 6 | `gather-schedar-belt` | 15 | 141,522 units above floor, 41,620 of them iron | -219 (3 runs, 12 h), 195 to 221 ore a run | Iron one jump from Node Beta |
| 7 | `gather-ironhollow-fading-signal` | 10 | about 7 an hour (grows back 478 iron), 29,718 iron above floor | -216 (28 runs, 12 h), 191 to 242 ore a run | Iron one jump from The Experiment, guarded by Military |
| 8 | `gather-ironhollow-echo-ejecta`, `gather-garnet-belt` | 1, 1, tests | 165,333 and about 170,000 above floor | new | Iron beyond the border: one and two jumps from The Experiment |
| 9 | `gather-gsc-0027-prism-scatter`, `gather-hamal-crystal-bloom`, `mine-acubens` | shared | all three under their floors at 03:02 UTC | -138, -196, -183 (12 h) | Iron at home; open again when the fields grow back |
| Then | `mine-pherkad-rift`, `gather-gsc-0027-spacetime-seep`, `census-frontier`, `park` | shared | Pherkad carries about 9 an hour | -178, -177 (12 h) | Standing work for the rest; copper at Pherkad is not short |

Why this plan. Iron is the reserve's largest short ore (265,455 held of
626,100, the tool stock, view=reserve, 03:03 UTC). It is asked at 4 cr in
depth (25,949 at Central Nexus, millions at a player's station in LHS
1140, 03:18 UTC) and gathered for about 1.0 to 1.5 cr of fuel a unit of
iron one jump from a station. A gather run fills a hold of 65 and flies
it to the station: the jumps between field and station set the yield.
Of more than sixty untouched iron fields beyond the border, only Schedar
Belt and Ironhollow lie one jump from a station of ours (lanes table and
stations table, 03:16 UTC); Garnet Belt and Ironhollow Echo Ejecta are
the next tests. Carbon and silicon have no field to gather: carbon is
asked at 4 cr in depth at four stations, silicon at 312 to 561 cr in a
few hundred units. Water ice: the bids show a few units at a time, so
stored ice is drained by test, not mined.

What would change it: a water-ice order of 300 units or more at Central
Nexus (the gated mine routes open by themselves); the first RESULT line
of the drain test and the two iron tests; a hostile ship at Schedar or
Ironhollow (rule F13: the route leaves the plan until Military has
looked); the home fields growing back over their floors; a silicon or
carbon field found by Intel. Each turn starts with `stalled.py` of the
mining-chains skill and `fill.py status miner`.

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
- A standing run ends docked with its hold stored (mine.py
  `store_last_load`, commit 0eca38b, 2026-11-17 03:13 UTC). Before it, a
  run without `sell` stopped the engine's loop at its time and left the
  partial load aboard: 34 miners waited at 03:02 UTC with 10 to 42 units
  aboard, closed out of every route that wants an empty hold.
- Readings of the night of 2026-11-16 to 17 (data/routes/runs.jsonl):
  Schedar Belt 195 to 221 ore a run of 45 minutes, -156 to -168 cr;
  Ironhollow Fading Signal 191 to 242 ore, -132 to -165 cr; fields four
  to seven jumps from their station (Gliese 876, Stillwork, Gaugewatch,
  Gossamer Null, GSC-0033, Thinspace, Dewfall Fray) 104 to 224 ore in 65
  to 101 minutes, -338 to -1,020 cr a run.
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
| `reserve-prism` | A loaded hold stored first, then carbon, then iron: Schedar Belt, Ironhollow Fading Signal, Ironhollow Echo Ejecta, Garnet Belt, Prism Scatter, Hamal, Acubens | Mining | Mining Laser I |
| `reserve-hamal` | The same with Ironhollow before Schedar and Hamal before Prism Scatter | Mining | Mining Laser I |

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

- `drain-ice-nexus` with a gate of 5 units (2026-11-17 03:13 UTC): credits a
  run and runs an hour against the Central Nexus water-ice bid that shows
  1 to 5 units at its best price at every read.
- `gather-ironhollow-echo-ejecta` and `gather-garnet-belt`: ore a run and
  the iron share, then lift toward what each field carries; the table
  `met` read for combat ships first (rule F13).
- `mine-groombridge-34-ice-fields`: one run, +740 cr (6 deuterium ice sold
  for 1,392 cr, 5 water ice for 128), 102 minutes; a second run before a lift.
- The first runs of mine.py on its new end step (after about 03:58 UTC):
  the note "stored at <station>" in the pilots' logs and no ship left with
  more than five units aboard after a gather run.
- A Gas Harvester I on one laser miner (the 20 born with one free utility
  slot): the route maker estimates 1,000 to 2,850 cr a ship-hour on
  hydrogen bids of 40 to 104 units an hour; not flown by Mining yet.
- A Flotation Cell (filter_copper_ore) on one iron miner: the iron share of
  its loads against 56 to 65%. Not bought yet.
- Deuterium ice: a bid of 175 cr x 6 at Node Beta; 3,273 stored in the
  fleet (2026-11-16 23:04 UTC).
