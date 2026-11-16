---
name: guidebook-logistics
id: 20261115T205805Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# logistics.md -- Guidebook of the Logistics Division

Kept by Apollo; read by every member. What the Logistics division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Apollo writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/hauler.json`; every route
  with its figure is in `game/routes/index.md`.

## Standing Plan

What the 20 haulers fly between two turns (2026-11-16 03:30 UTC, orders.log
ENT-011), in the plan's order. A free hauler takes the first route open to
it. The scale of the hour: the best route of the fleet, mine-ruchbah-ice-belt,
at 8,404 cr per ship-hour; a ship without work earns 0 (`hive.py tasks`).

| # | Route | Ships | Expected per ship-hour | Why it stands here |
|---|---|---|---|---|
| 1-7 | The seven missions that pay once at home (Precedence, Selling, First Hunt at Nexus Prime, Concurrent, Substrate, Missions-1, Mining missions) | First Hunt 1 at a time; the rest closed: every hauler has them booked or done | First Hunt pays 1,000 cr once | A new pilot flies them first (strategy, principle 5) |
| 8 | `voidborn-first-steps` | 2 | +935 cr once a run of about 10 min (6 runs, 2026-11-16 02:56 to 03:26 UTC) | The Acubens belt refills carbon; open to haulers that have not handed it in |
| 9-10 | `hunt-dimming-pocket-veil-ray`, `hunt-denebola-fractured-prism-veil-ray` (tests) | 1 each | +511 cr in 9.7 min and +478 cr in 13.3 min, one run each (about 3,160 and 2,160 per ship-hour), both left for a foreign ship | One hunter per herd (orders F9); measured further before lifting |
| 11-12 | `fit-gas-harvester-hauler`, then `mine-achernar-gas-pocket` (test) | 1 pilot, 1 ship | not measured; the route maker estimates 2,580 | The gas test of the orders, one hauler; its plasma gas sells into one thin bid at Node Beta |
| 13-17 | First Hunt at Acubens, GSC-0027, Schedar, Achernar and GSC-0031 | 1 each, shared with every division | 1,000 cr once | Missions that pay once are flown by every pilot (orders F8) |
| 18 | `census-frontier` | up to 12 of the fleet | -600 (35 runs): the price of the picture | Every division reads the frontier (orders F13) |
| 19 | `park` | the rest | 0 | Docked costs nothing (orders F8) |

So, for the four hours: 2 to 6 haulers at work, the others docked at 0.
The division read -41 cr per ship-hour over all 20 ships and -412 per
ship-hour flown, with 92,009 cr paid once, in the 4 hours to 03:28 UTC
(`hive.py tasks`). No repeating route pays a hauler without a harvester.

What changes it: Zero's word on the harvester Logistics made (requests.log
ENT-087), which opens an ice route at 4,000 to 8,400 per ship-hour to a
hauler; the goods for ten more (ENT-088); the runner's sale from storage
with `requires.bid` (ENT-065, owed by 12:00 UTC), which makes the stored
soma a route; the gas test's first RESULT line; Mercury's word on the
Node Beta mission chain.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| -- | -- | -- | No recurring route yet. The two hand sales that earned (section 7) were each capped by a station bid of a few units |
| Neural soma sold by hand where the haulers already stood (no fuel) | +2,381 cr for 4 soma: 3 at 588 cr into the Node Beta bid of 588 x 4 (02:57 UTC book; 2 from storage, 1 from a hold), 1 at 617 cr a few minutes after the same bid read 0 | 2026-11-16 03:00 to 03:19 UTC | Sold from storage and from the hold alike; a bid read empty at 03:18 UTC stood at 617 x 1 within about two minutes |
| Stored neural soma into station bids (hand test, not a route) | +1,995 cr in 4.7 min from the first jump to the sale (one ship, Central Nexus to Synchrony Hub, 3 soma sold at 678 cr from storage); the onward leg to The Experiment found no bid (-22 cr fuel) | 2026-11-15 23:29 to 23:37 UTC | Station bids of 559 to 694 cr for 1 to 3 units stand by turns at five of our stations and refill within about 40 minutes of being emptied (`data/market/history.jsonl`, 20:46 to 23:33 UTC). Logistics stores 50 soma, the fleet 302. A route needs a sell from storage and a dispatch on a standing bid (requests.log ENT-065) |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `mine-acubens`, `mine-gsc-seep`, `mine-pherkad-rift` (haulers) | -172, -180 and -174 cr per ship-hour over 29, 7 and 31 runs (`board.py Apollo`, last four hours at 21:16 UTC) | 2026-11-15 | All fuel; the ore has no buyer. Out of the plan (orders F8) |
| `voidborn-first-steps` while the belt was empty | One run of 20 minutes, -109 cr, nothing handed in ("objectives not done") | 2026-11-15 21:02 UTC | Acubens Belt read 0 carbon ore at 21:01 UTC. It refilled since (section 3) |
| Selling stored iron ore into station bids | 10 units sold at 2 cr from storage; the bid at Central Nexus went 20, 10, none (21:22 to 21:33 UTC); it came back by 5 to 15 units at 1 to 2 cr every 5 to 20 minutes, and stood at 2 cr for 2,375 at 23:17 UTC, about two hours after it emptied (`data/market/history.jsonl`) | 2026-11-15 | A station-owned bid is a pool that refills on its own clock. At 2 cr the ore stays in storage (orders.log ENT-007, block APOLLO): steel and wiring are what a base will need |
| Ferrous slug cases for The Experiment | The best bid is 15 cr for 8 cases, then 2 cr for 314 (queue.log ENT-037). The 322 at 15 cr read on 2026-11-15 19:03 UTC was the total of all levels | 2026-11-15 | A trip burns more than 8 cases bring. Not flown |
| `mission-cracking-the-shell-central` and `-achernar` (once routes added by fill.py) | 12 hauler runs, every one `cracking_the_shell not offered`: 8 at -26 cr, 4 at 0 cr, -208 cr in all; the Achernar route read at a loss, 2 runs, -104 cr | 2026-11-16 02:56 to 03:27 UTC | The board does not offer the mission to haulers; why is not known. Both out of the hauler plan at 03:27 UTC |
| Carrying a soma to a bid seen 39 minutes earlier | The Experiment bid 690 cr for 2 at 22:58 UTC; at 23:37 UTC no bid stood (view_market) | 2026-11-15 | A saved bid of a few units is gone within the hour: carry only to a bid read minutes before, or store the goods where the bid comes back |

## 3. Missions That Pay Once

| Route | What it pays and needs | Measured |
|---|---|---|
| `voidborn-precedence` | Precedence, 4,000 cr: accept at Node Beta, dock at Synchrony Hub and Node Alpha, hand in at Node Beta; nothing bought | first RESULT line +3,896 cr in 15 min (2026-11-15 23:31 UTC, the command group's test); all 20 haulers sent from 23:40 UTC, 13 on it at 23:44 UTC |
| `voidborn-selling` | Market Participation: Selling, 1,000 cr for 10 units sold; ten liquid nitrogen bought at The Experiment and sold there into the 2 cr bid | 7 hauler runs, +865 cr each in 4.9 min (2026-11-15 23:36 to 23:42 UTC); every hauler that held it has handed it in |
| `voidborn-first-hunt-nexus` | First Hunt: Belt-Grazers, 1,000 cr and 50 Weapons XP: three belt-grazers (60 hull) with the starter's Pulse Laser I, one hunter at a time (orders F9) | first RESULT line +974 cr in 18.9 min, lowest hull 100% (2026-11-15 23:39 UTC, the command group's test); in the hauler plan since 23:45 UTC |
| `voidborn-first-steps` | First Steps in the Void, 1,000 cr: mine 15 carbon ore at Acubens Belt, hand in at Central Nexus. On again since 2026-11-16 00:24 UTC, two ships at a time (requests.log ENT-071) | one hauler by hand: +913 cr in 10.8 min (2026-11-15 23:28 UTC). In the plan again: 6 hauler runs, +935 cr each in 9.2 to 10.1 min (2026-11-16 02:56 to 03:26 UTC) |
| `voidborn-concurrent` | Concurrent Approval, 3,000 cr; the soma it needs are handed out at the accept | 146 runs in the fleet, 2,970 cr a run (`routes.py measure`, 23:43 UTC); all 20 haulers flew it |
| `voidborn-substrate` | Substrate Delivery; the mission hands its 2 soma over at the accept, so nothing is bought | 146 runs, 1,790 cr a run (index) |
| `voidborn-missions-1` | Synchrony Relay Run and Crystal Delivery, 8 jumps | 146 runs, 6,430 cr a run (index) |
| `voidborn-mining-missions` | Iron Supply Run 1,500 cr and Copper Requisition 1,800 cr | 11 hauler runs, one-time +29,700 (`board.py Apollo`, 23:20 UTC) |

## 4. Levelling

On 2026-11-16 03:28 UTC (`hive.py levels`): Piloting 3 lowest, 4 median
and highest; 112 Piloting XP an hour on average since birth, so about 111
hours to Piloting 10 and the tier-2 hulls at that rate. Mining 3, deep core
mining 3, navigation 2, trading 1 and gunnery 1 (medians). The one hauler
that made a harvester crafted with no skill asked for (section 11).

Earlier: the haulers read Piloting 3 (10 pilots) and 4 (10), Trading 1,
Navigation 2, Exploration 1 and Mining 2 (10) or 4 (10) on 2026-11-15
23:42 UTC (ship files); no level changed from the reading of 21:19 UTC.
First Hunt pays 50 Weapons XP, 15 Xenobiology XP and 20 Piloting XP
(the mission's board, requests.log ENT-047). Which skill each other
route trains, and how fast: `not measured`. Piloting 10, 20, 30 and 50
opens hull tiers 2 to 5 (shared skill `fleet-play`, levelling).

## 5. Ships and Fits

The starter Threshold carries 65 cargo units and 95 fuel (ship files,
`cargo_capacity` 65, 2026-11-15 21:19 UTC; the rulebook's 66 predates
release 0.715.3, requests.log ENT-038). No other hull or module was
tried: `not measured`. A hauler that mines ice needs an Ice Harvester I
in the mining laser's place: 1,413 cr at home (orders.log ENT-007,
block ZERO), 638 cr at LHS 1140, six lawless jumps away (queue.log
ENT-046), or made by hand (section 11).

A Gas Harvester I goes into the second utility slot beside the mining
laser: one hauler bought and fitted one at Node Beta by the route
`fit-gas-harvester-hauler`, -1,236 cr in 3.7 min (2026-11-16 03:16 UTC,
the ask 1,202 cr). It is the tool of the gas test `mine-achernar-gas-pocket`;
what gas earns a hauler is `not measured` yet.

Next step up: Piloting 10 opens the tier-2 hulls, about 111 hours away at
the haulers' rate (section 4). Until then the step that pays is a tool, not
a hull: an ice harvester puts a hauler on routes measured at 4,000 to 8,400
cr per ship-hour (`hive.py tasks`, 03:28 UTC).

## 6. Fuel: What a Leg Costs (for every Admiral)

Measured from the fleet collector's ship files, sampled every 10 s.

- 1 unit per jump (87 jumps) and 1 per in-system leg (116 legs),
  2026-11-15 19:04 to 19:24 UTC.
- From dock to dock, about n+1 units for a hop of n jumps, billed at the
  arrival refuel of ships that left with a full tank (2026-11-15 21:30
  to 21:45 UTC): 1 jump 2 units (115 of 116 hops), 2 jumps 3 units (2
  hops), 3 jumps 5 units (1 hop).
- Price per unit, all-in (`fuel_price_all_in` of the census files, and
  117 refuels seen): Node Beta 11, The Experiment 11, Node Alpha 12,
  Synchrony Hub 12, Central Nexus 13, Node Gamma 15. The rules say the
  price rises as the tank empties; every bill read was for a nearly
  full tank.
- So: Central Nexus to Node Beta and back costs 48 cr (22 + 26); a
  three-jump hop about 55 to 75 cr one way. A load must beat its round
  trip before tax and before the ship's time.
- Seen 2026-11-15 23:29 to 23:37 UTC: Central Nexus to Synchrony Hub,
  3 jumps, 39 cr; Synchrony Hub to The Experiment, 2 jumps by the
  engine's path, 22 cr.

## 7. Storage by Hand: The Calls and Their Answers

Through `game/fleet/gate.py`, one hauler at a time. A `raw` call holds
the ship by hand by itself (`held by hand: ...`); release it docked.

| Call | Answer |
|---|---|
| `gate.py hold <pilot>` | `held: <pilot> (hand Apollo)` |
| `raw <pilot> view '{"station_id":"central_nexus"}' spacemolt_storage` | the storage there, item by item, and `locations` (every station with goods). The action name `storage` is refused (`invalid_action`) |
| `raw <pilot> craft '{"recipe_id":"basic_iron_smelting","quantity":1,"deliver_to":"storage","preset":"workshop","dry_run":true}'` | `kind: quote`: 10 iron ore for 1 steel plate, `credits_total` 0, venue Station Workshop, 0.27 ticks a run, `have_inputs` true |
| the same quote for `basic_copper_processing` (1), `manufacture_ferrous_slugs` (5) | 8 copper ore for 1 copper wiring, 0 cr, 0.32 ticks; 2 steel plate and 3 iron ore for 5 ferrous slug cases, 0 cr, 1.12 ticks |
| the same quote for `fabricate_circuit_boards` (2026-11-15 23:45 UTC, at The Experiment) | 3 copper ore, 2 silicon ore and 1 energy crystal for 2 circuit boards, 0 cr, 6 ticks a run, Station Workshop; with or without `preset` the same venue |
| the same without `preset`, `refine_steel` (2), `process_copper_wiring` (2) | a rented public facility: 5 iron ore for 2 plate, 19 cr (10 labor, 9 fee); 4 copper ore for 2 wiring, 17 cr (7 labor, 10 fee) |
| `craft` as above without `dry_run` (quantity 2) | `kind: job` with a `job_id` in `structuredContent.details`; the text part of the answer carries the ship's location |
| `craft '{}'` (no recipe) | the queue: `total_jobs` 0 after 34 s, the job done |
| `raw <pilot> view_market '{"item_id":"voidborn_neural_soma"}' spacemolt_market` | every level of both sides with its `source`: at Synchrony Hub at 23:33 UTC `buy 678cr 3 station` |
| `raw <pilot> sell '{"item_id":"voidborn_neural_soma","quantity":3}'` with an empty hold | taken from storage there: credits 34,597 to 36,631 (+2,034, 3 x 678); the bid was empty after it |
| `raw <pilot> withdraw '{"item_id":"...","quantity":1,"target":"self"}' spacemolt_storage` | storage to hold. With `"target":"cargo"` refused: `invalid_target`, valid targets are `self` and `faction`; player, empire, `faction:TAG` and `station:ID` targets are deposit-only |
| `raw <pilot> deposit '{"item_id":"...","quantity":1,"target":"self","source":"cargo"}' spacemolt_storage` | hold to storage at the station where the ship is docked |
| `gate.py release <pilot>` | `released: <pilot>`, docked |

The workshop runs only while the pilot stays docked there, takes the
inputs from that pilot's own storage at that station, and costs no
credits. Storage is personal: a good another pilot stores is moved to
another pilot only by a deposit to that player, which is a gift.

## 8. The Fleet's Storage Home and the Faction Lockbox

Central Nexus, for everything the fleet keeps from here on:

- Every pilot's home and respawn base, and the dock of the route
  `park`: a ship waiting there can craft from its own storage at the
  workshop for free (section 7), and pays no fuel to reach its goods.
- The deepest list of bids of our inner stations: 440 items with a
  bid in the 21:26 UTC book (Node Beta 88, Node Alpha 45, Node Gamma
  43, Synchrony Hub 49; The Experiment 664, but three jumps out and on
  the border).
- One jump from Node Beta, where half of the stored ore lies: 48 cr a
  round trip if a use for that ore appears.
- Against it: Node Beta sells fuel 2 cr cheaper and sits one jump from
  the Acubens and GSC-0027 fields.

A Faction Lockbox, the first faction storage (catalog 0.717.0, facility
`faction_lockbox`): 200,000 cr, 200 steel plate and 50 circuit boards,
build time 50, labor 50, 100,000 units per item type. What we store
covers part of it (`ledger.py show all`, 2026-11-15 23:21 UTC):

- Steel: 2,000 iron ore make 200 plate at the free workshop; Logistics
  stores 11,671 iron ore, and one hauler held up to 1,122 at Node Beta.
  Bought, plate costs 18 cr a unit with depth at five stations: 3,600 cr.
- Circuits: none in Logistics storage. Three miners store 47 silicon
  ore and 113 energy crystal at Central Nexus: about 46 boards by
  `fabricate_circuit_boards`, free at the workshop (quote, section 7).
  Bought, 50 boards cost about 23,700 cr at the best asks of four
  stations, 25,144 cr at Central Nexus alone (`data/market/`, 23:39 UTC).
- The goods go to the builder by a deposit to that player (section 7).
  Who builds it and where is the Fleet Admiral's and Suggi's (orders
  F11); this is Logistics' advice.

The ore that lies at Node Beta and Synchrony Hub stays there: moving it
costs fuel and nothing buys it (orders.log ENT-007, block APOLLO).

## 9. What the Ice Routes Leave Behind

From the books of our six stations and of LHS 1140 (the first foreign
book), 2026-11-15 22:51 to 23:45 UTC, and the catalog's recipes:

| Good | Buyer |
|---|---|
| Water ice | Station bids with depth: 20 to 34 cr for 905 to 26,340 units at five stations (23:43 to 23:45 UTC) |
| Methane ice | Station pools of 1,000 that empty and refill: 47 cr at Synchrony Hub and The Experiment from 20:33 UTC, 36 cr at Node Gamma and Node Alpha; all six stations read 0 or 7 cr from 23:20 to 23:29 UTC, five stood at 36 cr for 1,000 again from 23:32 to 23:36 and Synchrony Hub by 23:45 UTC (`data/market/history.jsonl`) |
| Deuterium ice | Thin: station bids of 188 to 226 cr for 5 and 6 units at Node Beta and Node Alpha, seen in six moves of the book from 20:45 to 22:51 UTC; 2 to 3 cr at The Experiment |
| Nitrogen ice | None worth a trip: 2 cr for 49 at The Experiment. Its hand recipe (5 ice to 4 liquid nitrogen) meets a 2 cr bid |
| Helium ice | 2 cr for 500 at The Experiment; its recipe is facility-only and helium-3 is bid 2 cr |
| Oxygen ice | No bid; its recipe is facility-only and oxygen gas has no bid |

LHS 1140 bids for methane ice only (36 cr for 500 at 23:45 UTC; nothing at 23:21 UTC). And no ship carries goods of value out of
Voidborn space (orders F13): a buyer beyond the border is no use to the
goods we store until that order changes.

## 10. Open Tests

- A soma route once a circuit can sell from storage and wait for a
  standing bid (requests.log ENT-065, accepted, owed by 2026-11-16 12:00
  UTC).
- The gas test `mine-achernar-gas-pocket`: one hauler, its first RESULT
  line. Its hold must be empty first (`requires.empty_hold`).
- The two veil-ray hunt tests: a second run each before a lift.
- Ten harvesters made from the fleet's own silicon and crystal, when
  Mining gives the goods (requests.log ENT-088).
- A craft-and-sell route, when the circuit runner has its craft step,
  only where the depth at the best bid pays the round trip (section 6).
- What the fleet owns and where: `python3 -I -B game/fleet/ledger.py show all`.

## 11. The Harvester Chain: an Ice Harvester I Made by Hand

Tested 2026-11-16 with one hauler at the Central Nexus workshop (orders.log
ENT-011, block APOLLO). Every step is a by-hand recipe at the Station
Workshop: 0 cr fee, no skill asked for in any quote (`craft` with
`dry_run`), and the work runs only while the pilot stays docked there.

| Step | Recipe, runs | Inputs | Out | Time |
|---|---|---|---|---|
| Steel | `basic_iron_smelting` x4 | 40 iron ore (stored) | 4 steel plate | 0.27 ticks a run |
| Wiring | `basic_copper_processing` x2 | 16 copper ore (stored) | 2 copper wiring | 0.32 ticks a run |
| Boards | `carbon_arc_circuit_etching` x1 | 2 silicon ore, 12 carbon ore (stored) | 3 circuit boards | 6 ticks |
| Power cell | `build_power_cell` x1 | 2 circuit boards, 3 energy crystal, 2 copper wiring | 1 power cell | 6.75 ticks |
| Harvester | `build_ice_harvester_i` x1 | 4 steel plate, 2 circuit boards, 3 flex polymer, 1 power cell | 1 Ice Harvester I | 15 ticks |

Measured: the crafts ran from 03:07 to 03:14 UTC, about 7 minutes with
the waits between steps; the hop from Node Beta and the docking took 5
minutes before. Bought at Central Nexus at the asks of the 03:05 UTC book:
2 silicon ore (380 each), 2 energy crystal (420 each; the third was
stored), 1 circuit board (436; the fourth board, since one etching gives 3)
and 3 flex polymer (276 each): 2,891 cr with the 1% tax. The Central
Nexus power cell ask of 415 x 1 (02:51 UTC book) was gone by 03:05 UTC
(1,995 x 52), so the cell was made.

What one costs, by where its inputs come from:

| Inputs | Cost of one harvester |
|---|---|
| All bought at Central Nexus (silicon 380, crystal 420, flex 276) | about 3,130 cr with tax |
| Silicon and crystal bought, flex at Node Alpha (129 x 102, 02:46 UTC) | about 2,690 cr with tax |
| The fleet's own silicon and crystal, flex bought at Node Alpha | about 390 cr in flex, plus goods whose best bids are 40 to 60 cr: about 680 cr in all |
| Bought whole | 1,413 cr at four of our stations; 638 cr at LHS 1140, six lawless jumps out |

So the chain pays only from the fleet's own silicon ore and energy
crystal. What bounds it (`stock`, 2026-11-16 03:14 UTC): 48 silicon ore
(47 in Mining's storage), 135 energy crystal (132 Mining's), 226 carbon
ore spread over five divisions. At 2.67 silicon, 16 carbon and 3 crystal
a harvester, carbon bounds it at about 14 and silicon at about 17. Each
pilot crafts from its own storage only: the goods are first deposited
into one pilot's storage at one station (a gift between our own pilots,
which the wall lets pass).

## 12. Capacity of the Domain (orders F18)

Read 2026-11-16 03:14 to 03:28 UTC (`stock`, `catalog` with ask=can,
`hive.py refill`).

- Storage of Logistics: iron ore 7,491 and copper ore 4,317 (02:55 UTC,
  before the craft took 40 and 16), carbon ore about 130 after this turn's
  deposits, null matter 91, neural soma 37 in storage and 15 in holds, one
  Ice Harvester I.
- What it makes today by hand: 1,139 steel plate (at Node Beta 821,
  Synchrony Hub 222, Central Nexus 96, each pilot from its own storage) and
  753 copper wiring. Neither has a bid worth a sale (steel none, wiring 2
  cr); their use is the harvester chain, a lockbox (200 plate) and hull
  materials.
- What the soma bids take: the least our readings prove is 194 cr an hour
  at Synchrony Hub's 657 cr bid, about 0.3 units (`hive.py refill`); this turn one Node Beta bid
  went 4 units, empty, 1 unit within about 20 minutes. The fleet holds
  at least 323 soma; the bids are the limit, not the haulers.
- Ships the hauling employs today: one for the harvester chain, one for
  the gas test, two for First Steps, up to five on First Hunts and the
  hunt tests. The other haulers wait for a tool: Logistics needs no more
  ships, and each harvester made or bought turns one waiting hauler into
  an ice ship.
