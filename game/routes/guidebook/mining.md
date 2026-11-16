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

What the miners fly between two turns (2026-11-16 18:40 UTC, orders.log
ENT-017). A free miner takes the first open route of the list First, its
own routes, the list Then. Every miner has routes of its own. Credits per
ship-hour flown are the miner runs of 12:40 to 18:40 UTC
(`data/routes/runs.jsonl`); `carries` is the column of `hive.py standing`.

| # | Route | Ships | Carries | Expected per ship-hour | What it is for |
|---|---|---|---|---|---|
| F | The once line of the Central Nexus board, the First Hunts of Nexus Prime, GSC-0027 and Acubens | their limits | -- | judged with the reward | Every pilot flies them first; 69,584 cr paid once to miners in 12:40 to 18:40 UTC. The six fit routes leave First (plan file, 19:06 UTC): every miner carries a harvester or holds one in storage, and a refitted miner must not be sent to buy one |
| F | `voidborn-resonance-finish` (Mercury's) | 2 | -- | 8,560 cr a run once (one run, Trade) | 8 miners hold Conductive Lattice without Final Calibration; the energy crystal ask reads 420 cr x 461 (18:30 UTC) |
| 1 | `drain-methane-experiment` | 1, a test | bid 36 x 1,000 | not measured: 1,127 stored methane ice x 36 cr | Stored methane sold where it lies |
| 2 | `drain-ice-nexus`, `drain-ice-node-alpha` | 2 each | the bid, 25 cr x 30 | 0 and -39 cr on two runs (12:14 UTC) | Stored water ice sold where it lies, when the bid stands |
| 3 | `carry-ice-node-alpha-nexus`, `-synchrony-nexus`, `-experiment-nexus` | 3, 2, 3 | the bid, 25 cr x 65 | -50 to -96 cr on five runs before the size fix | Stored water ice carried into the Central Nexus bid |
| 4 | `mine-cryogenic-reserve`, `mine-achernar-frost-ring-nexus`, `mine-ruchbah-ice-belt-nexus`, `mine-wolf-1061-frozen-drift-nexus` | 1, 2, 1, 1 | 2, 2, 2, 3 | no run since 12:40 UTC | Open only while Central Nexus bids 300 or more water ice at its best price: a deep order |
| 5 | `mine-nova-terra-ice-shelf`, `mine-gliese-876-belt` | 1 each, tests | -- | not measured | Tests the hourly job put in; one ship each |
| 6 | `gather-gsc-0027-prism-scatter` | first route of 23 ships; 56 for the fleet | 0 +363 | -147 (18 runs) | Iron into storage at Node Beta: about 151 iron and 81 copper a ship-hour |
| 7 | `mine-acubens` | first route of 4 ships; 18 for the fleet | 0 +233 | -167 (48 runs) | Iron into storage at Node Beta: about 218 iron and 80 copper a ship-hour; closes at its floor of 10,000 iron |
| 8 | `gather-hamal-crystal-bloom` | first route of 11 ships; 56 for the fleet | 0 +378 | -175 (64 runs) | Iron into storage at Node Beta: about 97 iron and 94 copper a ship-hour |
| 9 | `gather-ironhollow-fading-signal` | 1, a test | regrowth about 520 iron an hour | not measured | Iron beyond the border into storage at The Experiment; the best iron share we read |
| 10 | `mine-wolf-1061-vent` | the one vent ship | 0 | 6,578 (3 runs, 2026-11-16 morning) | Water ice at Synchrony, while its bid stands |
| T | `census-frontier`, then `park` | 12 for the fleet | -- | -626 | Reading, when a miner has nothing else; a ship should never reach `park` |

Each ship's own list holds rows 1 to 5 first and then the three iron
fields in one of three orders (Prism Scatter, Acubens or Hamal first),
so the division is spread over three fields and each list falls through
to the next field when one is full or at its floor.

Why this plan: buyers, not tools or fields, bound Mining. Our stored
water ice, 19,220 units (the tool stock, 18:25 UTC), is about 17 hours
of what every water-ice bid of ours regains together, about 1,130 units
an hour (Central Nexus 842, Node Alpha 243, Node Gamma 28, Synchrony 11,
The Experiment 5; `hive.py refill`, 18:25 UTC). No water ice is mined
for sale while that stock stands; the routes that sell it are gated by
the bid. Every other miner gathers iron for the stations' list (orders
ENT-017): 491,400 units, of which the fleet holds 104,683 (the tool
base_plan, 18:25 UTC). The order of the iron fields is their iron share:
what each field gave up between the census reads of 14:05 and 18:26 UTC.

What would change it: a water-ice bid of 300 or more at its best price
(the gated routes open by themselves); the drain and the Ironhollow
test's first RESULT lines (lift each to what its bid or its regrowth
carries); a copper filter that lifts the iron share (one ship, by hand);
a field at its floor. Each turn starts with `stalled.py` of the
mining-chains skill.

## 1. Route Guides

How each kind of route of this division is flown: the fit and the
skills it needs, its place, its steps, what opens and closes it. A
credits figure in this section is a dated reading and no verdict: what
a route earns now is in the fleet's database with its age (rule F22;
the tool `routes`, the view `route_earnings`).

Runs of 2026-11-16 12:40 to 18:40 UTC (`data/routes/runs.jsonl`): no
water-ice mine route ran. Every one was closed by its bid gate
(`requires.bid`, 300 units at the best price) while Central Nexus read
0 to 2 units at its best price; the stored ice routes were closed by
theirs (30 and 65 units). 213 miner runs, 126 ship-hours flown: -19,355
cr steady (-154 per ship-hour flown) and 69,584 cr paid once, the once
line of the board and the First Hunts. The four hours before were the
last in which ice paid:


Runs of 2026-11-16 08:00 to 12:20 UTC (`data/routes/runs.jsonl`), after
fuel, per ship-hour flown:

| Route | Credits per ship-hour | Runs | Note |
|---|---|---|---|
| `mine-wolf-1061-vent` | 6,578 | 3 | Sold at Synchrony while its bid stood |
| `mine-ruchbah-ice-belt-nexus` | 3,549 | 3 | Central Nexus, four jumps: the one-ship test of 08:12 UTC holds |
| `mine-alnair-ice-fields-nexus` | 3,182 | 14 | Central Nexus, five jumps |
| `mine-achernar-frost-ring-nexus` | 3,047 | 45 | Central Nexus, four jumps; 8 runs at -138 to -318 cr ended 11:00 to 11:10 UTC while the bid read 0 |
| `mine-wolf-1061-frozen-drift-nexus` | 2,043 | 12 | Central Nexus, four jumps |

Mining over all 40 ships in the four hours to 12:15 UTC: 1,446 credits
per ship-hour, 2,246 per ship-hour flown, 453,122 cr paid once beside
it (`hive.py tasks`); steady net of the division in the hour to 12:15
UTC +39,778 cr (`hive.py fleet`).

The figures below were measured by `routes.py measure` at 08:20 UTC:

Measured by `routes.py measure`, 2026-11-16 08:20 UTC, after fuel, over
every run of a route. The figures of the routes that sold at The
Experiment and Node Alpha were earned while their bids stood; since
07:07 and 07:25 UTC those bids read 0 (the list in this file's history).

| Route | Credits per ship-hour | Runs | Minutes a run | Note |
|---|---|---|---|---|
| `mine-ruchbah-ice-belt` | 7,430 | 46 | 43 | The Experiment, one jump; 8,950 over 16 runs at 04:23 UTC; its last ten runs sold no water ice |
| `mine-achernar-frost-ring` | 5,460 | 35 | 48 | The Experiment, one jump; its last nine runs sold no water ice |
| `mine-wolf-1061-vent` | 5,360 | 5 | 56 | Ice Harvester I with a Nitrogen Vent |
| `mine-achernar-frost-ring-nexus` | 2,650 | 5 | 51 | Central Nexus, four jumps; +2,755, +3,012, +2,916 cr on its paying runs |
| `mine-homam-cryobelt` | 2,660 | 4 | 73 | The Experiment; +5,041 and +8,318 cr while the bid stood; out of the plan |
| `mine-gsc-0041-frost-ring` | 2,080 | 5 | 62 | Node Alpha; out of the plan |
| `mine-wolf-1061-frozen-drift` | 2,070 | 10 | 67 | Node Alpha; sells methane while the water bid regains |
| `mine-alnair-ice-fields-nexus` | 1,820 | 3 | 77 | Central Nexus, five jumps; +3,670 cr on its paying run |
| `mine-wolf-1061-frozen-drift-nexus` | 1,640 | 4 | 66 | Central Nexus, four jumps; +3,496 and +4,333 cr on its paying runs |
| `mine-node-beta-frozen-drift` | 1,340 | 12 | 44 | Field 225 water ice (07:53 UTC); out of the plan |
| `mine-keid-ice-shelf` | 1,120 | 8 | 96 | Node Alpha, five jumps; out of the plan |
| `mine-intercrus-ice-fields` | 880 | 8 | 76 | The Experiment; out of the plan |
| `mine-alnair-ice-fields` | 840 | 9 | 67 | Node Alpha |

Mining as a whole in the four hours to 08:18 UTC: 98 mine runs, 93.9
ship-hours flown, 2,302 credits per ship-hour flown (`hive.py tasks`);
the division over all 40 ships, 1,183 credits per ship-hour (scale
7,910). Steady money of the division in the last hour, read at 08:17
UTC: +14,370 cr (`hive.py fleet`), against +70,528 at 04:16 UTC: the
near bids emptied in between.

## 2. Route Templates

A kind of work is a named list of routes: a template. The templates of
this division are kept in `game/routes/templates/mining.json` and listed
in `game/routes/templates-mining.md`, a page a script writes once the
division has its first template. A ship's row in the plan file names a
template as `@<name>`, alone or beside routes of its own, and a ship is
switched to other work with one word.

| Task | How |
|---|---|
| See the templates and how many ships use each | the tool `plan` with `action=templates` (`plan.py templates`) |
| Make or change one | `plan.py template <name> <routes with commas> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py use <ships> <name>` (the tool `plan` with `action=use`) |
| Take one away | `plan.py template <name> none`, once no ship names it |

A template is a guide for one kind of ship: its routes in the order a
ship tries them, the skills it trains (`--trains`) and, in its note,
the fit it needs. Keep one for each kind of work of the division, so
that a ship born tomorrow gets its work with one word.

This guidebook keeps no list of routes that did not pay (Suggi,
2026-11-16; rule F22). The game changes by the hour: a route that lost
yesterday may pay today. What a route earns now, with the age of the
figure, is asked each turn: the tool `routes`, or `SELECT * FROM
route_earnings` through the tool `hive` with `verb=sql`. How a step of
the game works is a mechanic, not a verdict on a route: it belongs in
the sections below. The list this section held until 2026-11-16 is in
the file's history (`git log -- game/routes/guidebook/mining.md`).

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
open. Per kind of ship: the skill, what raises it, what the next level
opens, and the template that trains it (section 2).

- At 18:40 UTC (`hive.py levels`): Piloting 5 / 5 / 7 (lowest, median,
  highest), 136 XP an hour; median Mining 5 (115 XP an hour), Navigation
  4, Deep Core Mining 4; 77 hours to Piloting 10 (tier 2 hulls) at that
  rate, against 86 at 12:15 UTC. The next hull step stays a tier 2 hull at
  Piloting 10; no miner is near it.
- Mining XP is one point per unit mined. Level 5 needs 900 XP, level 6
  1,285 (the pilots' files). Median of the 40 miners on 2026-11-16 at
  08:20 UTC: Mining 4, Piloting 4, Navigation 3, Deep Core Mining 3
  (`hive.py levels`); at 03:19 UTC it was Mining 2, Piloting 3.
- Every ice route trains Mining (ice fields train it like belts) and
  Piloting (the jumps); the miners on ice since 2026-11-15 stand at
  Mining 4 and 5, the waiting ones at 2.
- Piloting 10, 20, 30 and 50 open hull tiers 2 to 5. At the division's
  average rate (118 XP an hour of Piloting) the median miner needs
  about 103 hours to Piloting 10 (the tool fleet, view levels, 08:20
  UTC). A route that sells at Central Nexus flies four to five jumps
  each way: more Piloting per run than a one-jump route.
- Mining skill raises the share of the rarer deposit in a pull (the
  game's `mine` help). At Mining 4 a nebula gave 14.5% energy crystal
  where its richness alone gives 8.3% (section 6).

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
  each); none on offer in our books since 2026-11-15 23:30 UTC.
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

## 7. Open Tests

- `drain-methane-experiment` (Standing Plan, row 1): the first drain
  flown where its bid stands; its RESULT line says whether the withdraw
  step sells from storage as built.
- `gather-ironhollow-fading-signal` (row 9): iron share of a load beyond
  the border, and whether the field's regrowth of about 520 iron an hour
  holds with a ship on it.
- A Flotation Cell (filter_copper_ore) in place of the ice harvester on
  one iron miner, fitted by hand at Node Beta (skill script `refit.py` of
  mining-chains): the iron share of its loads against 51 to 73%. Half
  done on 2026-11-16 19:01 UTC: the harvester came off one miner and,
  its hold being full, the game put it into the pilot's storage at Node
  Beta, not the hold; no cell was bought yet. Store the hold first.
- The drain and carry routes of stored water ice (rows 2 and 3): their
  first RESULT lines on the fixed runner wait for the Central Nexus bid.
  One carry withdrew 65 water ice at The Experiment or Synchrony at
  12:19 UTC.
- The vent: a second vent route only when a Nitrogen Vent is on offer.
- Deuterium ice: station bids of 2 cr at The Experiment now (492 units);
  the routes sell it from 166 cr only and store the rest.
- Methane ice: 36 cr bids of 1,000 at six stations of ours and 500 at
  Ironlight Crossroads; four of ours read 0 at 17:01 to 17:12 UTC, two
  read 7 cr at 17:17 to 17:18 UTC, and all six read 36 cr x 1,000 again
  at 17:15 to 17:34 UTC (the tool market): whether that is a daily
  refresh is not known. The fields hold it beside water
  ice and little of it (Ruchbah Ice Belt 3,521, Wolf 1061 Frozen Drift
  564, Achernar Frost Ring 302; census 17:39 to 18:25 UTC), so it comes
  with the water, not alone.
- Palladium ore: bids of 358 cr at four stations, 43,460 units in all
  (the tool fleet, view capacity, 12:03 UTC); no field we read holds it.
  Uranium and thorium the same, and they need a tool we lack.
