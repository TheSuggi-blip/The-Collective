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

## Class Card

The mining class in short (rule F14). Levels: 60 miners, table
`ship_skills` and the tool fleet (view=levels), 2026-11-17 23:25 UTC.

### Ships

- Tier 0, 59 miners: the Threshold, hold 65, 2 utility slots,
  cpu 16, power 30. Ice miner: Mining Laser I and Ice Harvester I;
  laser miner: Mining Laser I; both a Pulse Laser I in the weapon slot
  and the default stance flee.
- Tier 1, no Piloting asked: the Liminal (Voidborn Miner), hold 75
  with ore at half volume (about 150 ore a load), speed 2, 3 utility
  slots, no weapon slot. Commissioned with credits only: 58,589 cr at
  Node Beta (168 ticks), 83,307 at Central Nexus (84 ticks), with a
  Mining Laser I and two Shield Booster I (`commission_quote`,
  2026-11-17 11:06 UTC). One miner flies it since 2026-11-17 23:17 UTC
  (hull 65, shield 170, cargo 75, speed 2, a Mining Laser I and two
  Shield Booster I); its old Threshold stays at Node Beta with its
  modules. The test of section 7. For ice: the Rime.
- Tier 2, Piloting 10: the Resonance Miner (hold 180, 4 utility slots);
  for ice the Hoarfrost.
- Style: a gather shuttle of one jump to a station of ours, every field
  with a floor; ice and gas sold only as far as a bid regains; every
  new field, hull or fit first on one ship.

### Skills

In the order they are levelled. Level: lowest / median / highest of
the 60.

| Skill | Why it matters | What trains it, on which routes | Level now | Next goal |
|---|---|---|---|---|
| Mining | +1% yield a level; the pull picks the rarer deposit more often (10% at 0, 50% at 20): silicon, nickel, platinum | 1 XP a unit mined on every gather and mine route; mining missions 15 to 45 | 6 / 8 / 10 | 10 on every miner |
| Deep Core Mining | +5% a level from deep core deposits, which a survey reveals | mining with a laser (power 3 or more); Deep Core Prospecting 25 XP (14 miners so far) | 7 / 9 / 9 | 10; a deep core deposit read |
| Piloting | opens tier 2 at 10 | flying, jumps, missions | 7 / 8 / 9, about 25 hours to 10 | 10 |
| Voidborn Mastery | our empire's skill, only from Voidborn missions (rule F35) | the voidborn routes of the list First; Crystal Resonance Harvest 35, Material Synthesis: Basic 25 | 0 / 0 / 1 (9 miners at 1) | 2: the links after The Collective Provides |
| Navigation | -1% fuel, jump fuel and jump time a level | every jump of the shuttles; `train-navigation-trader` | 4 / 5 / 6 | 6 |
| Refining, Crafting | steel and piping from our own iron and copper | `craft-steel-experiment`, the other steel and piping crafts | 0 / 2 / 4; 0 / 2 / 5 | 5: the steel of our own iron |
| Trading | market fees | the drains and carries of stored goods | 0 / 2 / 4 | -- |
| Exploration, Scanning | a first visit; a survey shows deep core deposits | far tests; none of ours scans | 2; 0 | -- |

## Standing Plan

What the miners fly between two turns (2026-11-17 23:26 UTC, orders.log
ENT-050). The reserve's iron is met: 356,467 iron ore held against the
323,780 it takes, and that iron is the steel plate still to make, 32,378
plates of 10 iron each (surplus.py reserve, 23:04 UTC). So the division
makes before it gathers, and gathers only what the reserve lacks. A free
miner takes the first open route of the list First (the once routes:
the Voidborn chain, the two new Voidborn mining links, The Forge Tax,
Deep Core at Deep Range, the First Hunts), its own routes (soma sales and
carries where it stores soma, `@ice-sell`, the outpost route for the
seated miners, then `@reserve-prism` or `@reserve-hamal`), then the list
Then as the supply pass keeps it.

| # | Route | Ships (max) | Field or bid now | Measured | What it is for |
|---|---|---|---|---|---|
| F | `voidborn-crystal-resonance`, `voidborn-material-synthesis` | 1; 1 | Prism Scatter 86 energy crystal, Spacetime Seep 15,844 iron (22:44 UTC) | tests from 23:19 UTC | Voidborn Mastery for the 68 pilots holding The Collective Provides (rule F35) |
| F | `mission-the-forge-tax-crucible`, `mission-deep-core-prospecting-first-step` | 3; 2 | Hearsay Cobalt 3,222 (17:00 UTC); Deep Range 531 platinum (16:48 UTC) | two hand-ins each, +4,340 to +4,631 cr a run in 67 to 79 minutes | 5,000 cr once a pilot and 20 units of a reserve ore kept |
| 1 | soma sales and carries; `@ice-sell` drains and carries | 1 each | soma bids at four stations; no water-ice bid | 4,580 to 10,150 per ship-hour (route_earnings, 4 h) | Stored goods sold where a bid stands |
| 2 | `mine-dheneb-cryobelt` | 2 | Hex Star methane 36 cr x 643 (22:47 UTC) | 906 per ship-hour, 9 runs (4 h) | Ice only where a bid stands |
| 3 | `gather-gsc-0044-belt-faction` | 1, lift_to 10 | GSC-0044 Belt 100,000 iron, 100,000 copper | test from 23:19 UTC | The outpost's faction storage, seated miners only (orders ENT-050, ZERO (1)) |
| 4 | `craft-steel-experiment`, `craft-steel-node-beta` | 10; 11 (shared) | 137,676 and 39,514 iron in miners' storage (23:03 UTC) | Experiment: first run 2.9 minutes, 0 cr, 50 plates | Steel plate for the reserve from our own iron |
| 5 | `gather-goldcrest-gold` | 3 | 9,159 gold (21:06 UTC), about 830 back an hour | 325 gold in 90 minutes, -767 cr (one run) | Gold, short 14,068 |
| 6 | `gather-subra-floodlight-flats-silicon` | 2, floor 500 | 3,739 silicon, about 90 back an hour | 422 to 464 ore a run of 90 to 94 minutes, a third silicon, -35 to -43 cr | Silicon, short 51,567 |
| 7 | `gather-jadecove-nickel` | 1 | Long Errand Band 1,745 nickel (18:15 UTC) | test from 23:22 UTC | Nickel, short 15,486 |
| 8 | `gather-acubens-belt-carbon` | 2 | 170 carbon, about 56 back an hour | -234 cr a run | Carbon, short 88,913 (bought at 4 cr is cheaper: Trade's) |
| Then | as the supply pass keeps it: iron sources while the chain iron-ore reads short, the steel crafts, census, park | shared | -- | -- | Standing work for the rest |

Why this plan. Mining stored +9,845 units of the reserve's items an hour
over the 4 hours to 23:24 UTC (hive.py flow Zero): iron +5,972, copper
+3,225, gold +246, carbon +229, platinum +38, silicon +34, nickel +14.
Iron and copper were no longer needed: that fuel fed nothing. Steel
plate from stored iron is reserve work at about 0 cr, and the short ores
lie in few fields, most of them far from our stations: gold (The Gold
Crest), silicon (Floodlight Flats), nickel (Jadecove), carbon (Acubens).
A unit gathered there costs 1 to 5 cr of fuel against asks of 312 to 632
cr for silicon; carbon is asked at 4 cr, so buying it is cheaper.

What would change it: the RESULT lines of the five tests; the supply
chain iron-ore renewed (requests.log, turn of 23:00 UTC), which takes the
iron sources out of the list Then; more miners seated in the faction;
a deep water-ice order at Central Nexus; the stored iron all smelted.
Each turn starts with `stalled.py` of the mining-chains skill,
`fill.py status miner`, `hive.py flow Zero` and `surplus.py reserve`.

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
- Readings of 2026-11-17 03:00 to 07:00 UTC (miner runs, medians; 15
  runs of the window carry gifts of 10,000 cr or more to the Fleet
  Admiral's flagship, data/fleet/gifts.jsonl, so their sums mislead):
  Schedar Belt 84 runs, 260 ore in 46.5 minutes, -204 cr a run; Ironhollow
  Fading Signal 46 runs, 256 ore in 47.9 minutes, -165 cr; Pherkad 77
  runs, 159 ore in 48.2 minutes, -182 cr; Echo Ejecta 4 runs, 172 ore in
  55 minutes; Garnet Belt 3 runs, 176 ore in 87 minutes (two jumps). The
  end step of commit 0eca38b held: at 07:03 UTC no miner waited with ore
  aboard (`fill.py status miner`).
- A floor does not make a field grow back faster: the game refills a
  depleted deposit gradually in proportion to its capacity
  (game/rules/13-not-stated.md, from the official mining page), and
  Hamal grew back about 360 iron an hour at 31,000 while closed (table
  readings, 03:52 to 06:18 UTC). Floors are 20,000 iron since 2026-11-17
  07:12 UTC; a floor keeps a stock for later and stops the open-close
  flapping of a field near it, nothing more.
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
| `reserve-prism` | Make, then gather what the reserve lacks: a loaded hold stored, steel plate from the pilot's own iron at The Experiment and Node Beta, then gold, silicon, nickel and carbon (since 2026-11-17 23:20 UTC; the iron fields left it when the reserve's iron was met) | Mining, Crafting, Refining | Mining Laser I |
| `reserve-hamal` | The same with the short-ore fields in the other order (carbon, nickel, silicon, gold), so the division is spread | Mining, Crafting, Refining | Mining Laser I |

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

The mining missions of the boards (rule F34; data/missions, read
2026-11-17 11:05 UTC); each counts only units the pilot mines itself:

| Mission | Asks | Pays | Where the ore lies | State |
|---|---|---|---|---|
| Deep Core Prospecting (nine boards) | 20 platinum ore | 5,000 cr, 10 exotic matter, deep core mining 25 XP | Markab Belt 503 of 8,000 at 07:57 UTC, 0 at 17:04 UTC; Deep Range Mineral Fields 531 (2 jumps from First Step Memorial's board); 82 Eridani Belt 563; Stillwater 199 | `mission-deep-core-prospecting-nova-terra`: 11 pilots handed in from 11:20 to 18:40 UTC (+5,000 cr each, runs of 41 to 66 minutes), 5 runs found too little; it rests. The pilot keeps its 20 platinum in storage after the hand-in. `mission-deep-core-prospecting-first-step`: two hand-ins (+4,631 and +4,604 cr a run, 76 and 79 minutes), 2 ships and 12 pilots from 23:16 UTC |
| Titanium Extraction Contract (ten boards) | 20 titanium ore | 3,500 cr, mining 25 XP | 70 at GSC-0028, 50 at Jasmine, 12 or less elsewhere (7 to 11 jumps) | not flown: no field holds a load |
| The Forge Tax (The Crucible Garrison) | 20 cobalt ore | 5,000 cr, mining 20 XP | Hearsay Cobalt in Sargas 3,222 (18 jumps from the board); Tabit 270 (29 jumps) | `mission-the-forge-tax-crucible`: two hand-ins (+4,364 and +4,340 cr a run, 67 and 68 minutes), 3 ships and 20 pilots from 23:16 UTC |
| Crystal Resonance Harvest (Central Nexus, after The Collective Provides) | 20 energy crystal | 4,000 cr, Voidborn Mastery 35, mining 45 XP | Prism Scatter 86 (2 jumps), Thornhaven 69, Cedarhold 66, Okab 58 | `voidborn-crystal-resonance`: one-ship test from 23:19 UTC |
| Material Synthesis: Basic (Central Nexus, after The Collective Provides) | 10 iron ore mined and 1 steel plate smelted | 1,500 cr, Voidborn Mastery 25, crafting 25 XP | Spacetime Seep 15,844 iron (2 jumps) | `voidborn-material-synthesis`: one-ship test from 23:19 UTC |
| Amplification Materials (Central Nexus, after The Collective Provides) | 15 silver ore | 4,000 cr, Voidborn Mastery 25 XP | Errai Belt 284 (14 jumps, read 12:13 UTC); Elnath and Avior 0 | not flown: no silver field near |
| The Collective Provides (Central Nexus, the Voidborn chain) | 20 nickel ore | 2,500 cr, Voidborn Mastery 25 XP | Gliese 876 Belt 635 of 12,000, about 28 back an hour (7 jumps, 3 from the pirate stronghold Gliese 581); Algorab 1,342 (12 jumps); Jadecove 609, Azha 570, Rotanev 424; GSC-0049 reef 39, about 10 back an hour | Trade's route, off; the readings in admirals.log ENT-029 |

## 4. Levelling Guide

Which skills a ship of this division levels and on which work (rules
F23, F30): the work of its own class first. A miner's class is mining,
so gathering for the reserve trains its own skills and stores what the
reserve lacks at once. Sources: the catalog 0.723.2 (table `skills`,
column `training`), the official skills page
(https://www.spacemolt.com/docs/skills.md), the pilots' files (table
`ship_skills`) and `hive.py levels Zero`, read 2026-11-17 07:13 UTC: 60
miners, 36 hours played (median).

| Skill | How the game trains it | Our routes that train it | Level of 60 miners (lowest / median / highest), XP an hour | What it gives |
|---|---|---|---|---|
| Mining | Mine at asteroid belts, ice fields or gas clouds | every gather and mine route; one XP a unit mined | 4 / 6 / 8, 154 | +1% yield a level on every resource; the pull's choice leans to rarer ores |
| Deep Core Mining | Mine with equipment of power 3 or more, or reveal deep core deposits with survey_system | every gather route (Mining Laser I has power 5) | 4 / 7 / 8, 180 | +5% a level from hidden deep core deposits only; nothing on ordinary deposits |
| Piloting | Fly: travel, jump, mine, fight; a bonus for missions | all; the more jumps, the more | 5 / 7 / 8, 171 | in-system speed; tier 2 hulls at 10, about 48 hours away at that rate |
| Navigation | Travel between systems and places | the gather shuttles (a jump each load), carries, `train-navigation-trader` | 3 / 4 / 5, 49 | -1% fuel, jump fuel and jump time a level |
| Trading | Sell and buy | the drains and carries | 0 / 2 / 3, 10 | market fees |
| Exploration | Visit a system for the first time | the far tests | 2 / 2 / 2, 10 | survey power |
| Refining | Refine ores, process gases or refine ice at a station | none of ours | 0 | workshop speed beside Crafting |
| Scanning, Drone Control | Survey or query places; deploy drones | none of ours | 0 | survey reveals deposits; drone mining yield |

- What the ships farm: iron and copper ore, about half and half, into
  storage at Node Beta and The Experiment, with a little carbon, gold
  and platinum (hive.py flow Zero, the 4 hours to 07:15 UTC: iron +7,062
  an hour, copper +7,022, carbon +112, gold +35, platinum +15).
- Mining XP is one point per unit mined; level 5 needs 900 XP, level 6
  1,285 (the pilots' files). Deep Core Mining rises as fast because the
  laser counts as advanced equipment; it pays only on deep core
  deposits, which a survey reveals and no route of ours mines yet.
- Mining level shifts which deposit a pull picks, not how much it
  yields: the rarer deposit is picked 10% of the time at level 0, 50% at
  20 (the official miner guide, read 2026-11-15).
- Piloting 10, 20, 30 and 50 open hull tiers 2 to 5; a tier 1 hull asks
  no Piloting (table `hulls`, piloting_required empty for tier 1).
- Ships on work of the class: 57 of 60 miners mined or gathered at the
  start of this turn (07:05 UTC, fleet file: 34 Schedar, 20 Ironhollow,
  one each at Echo Ejecta, Garnet and the Acubens carbon); the other
  three flew missions that pay once and an ice test. After the turn the
  same 57 plus the one returned from the null-matter tests.

| Kind of ship | Fit | Work and template | Skills it raises | Next step |
|---|---|---|---|---|
| Ice miner | Mining Laser I, Ice Harvester I, Pulse Laser I | `@ice-sell` first, then `@reserve-*` | Mining, Deep Core Mining by the laser, Piloting, Navigation; Trading on the drains | A Liminal (section 5) or Ice Harvester II when a water bid carries ships again |
| Laser miner | Mining Laser I, Pulse Laser I | `@reserve-*` and the drains of `@ice-sell` | Mining, Deep Core Mining, Piloting, Navigation | A Liminal (section 5) |
| Test miner beyond the border | Mining Laser I, empty hold | one test route, then its templates | Piloting, Navigation, Exploration, Mining | Lift the test when its RESULT line holds |

## 5. Ships and Fits

- The next hull of the class is a tier 1 Miner, open now without
  Piloting: the Voidborn Liminal (table `hulls`, catalog 0.723.2): hold
  75 with ore stored at half volume, so about 150 units of ore a load
  against the Threshold's 65; speed 2 against 1; 3 utility slots, cpu 18,
  power 34; shield 120, hull 65; no weapon slot. A gather run is a shuttle
  of loads, so the load size sets what a ship brings an hour (section 1).
  Its materials (the tool catalog, ask=build): 5 shield matrix, 3 ore
  hopper, 1 processing core, 12 silicate composite, 10 copper wiring, 5
  void nanite suspension (made in a facility), 2 shield emitter. The
  game's `commission_quote` (2026-11-17 11:06 UTC): 58,589 cr with
  credits only at Node Beta (168 ticks), 83,307 at Central Nexus (84
  ticks), with a Mining Laser I and two Shield Booster I; with our own
  materials 8,659 and 12,053 cr. One was ordered at Node Beta at 11:11
  UTC for 58,881 cr (`commission.py` of the mining-chains skill). The tier 2
  step at Piloting 10 is the Resonance Miner (hold 180, 4 utility slots,
  cpu 28, power 48); for ice the Rime (tier 1) and the Hoarfrost (tier 2).
- Half of every iron load is copper the fleet holds in surplus (hive.py
  flow, above): a copper filter (Flotation Cell, section 5 below) on the
  third slot of a Liminal would turn that half into iron.

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
- Tier 2 opens at Piloting 10, about 42 hours away for the median miner
  (the tool fleet, view=levels, 2026-11-17 11:10 UTC). The step before
  it is the tier 1 Liminal above, which asks no Piloting.
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

- The Liminal: one hull ordered at Node Beta (58,881 cr, 2026-11-17
  11:11 UTC); its yard bought its last parts at its own bids once a miner
  sold them there (19:33 UTC, -12,325 cr); built by 20:01 UTC; its pilot
  switched in at 23:17 UTC (commission.py --switch-only). Its first runs
  fly `gather-goldcrest-gold` against the Threshold's 325 gold in 90
  minutes on the same field; a second hull only on that figure.
- `craft-steel-experiment` (from 23:19 UTC, 10 ships): plates a run and
  minutes; how often the ledger lets one pilot run again.
- `voidborn-material-synthesis`, `voidborn-crystal-resonance` (one ship
  each): whether the craft step counts for the objective; crystals a
  load at Prism Scatter.
- `gather-gsc-0044-belt-faction` (one ship, seated miners only): whether
  mine.py's `deposit: faction` stores the loads into the outpost's
  faction storage; then lift_to 10, and Botein and Acrux the same way.
- `gather-jadecove-nickel` (one ship): nickel a run, stored at The
  Crescent Moon beside the silicon of Floodlight Flats.
- Silicon beyond Floodlight Flats: Zubenelhakrabi Crystal Sand 771 (its
  nearest station is a pirate station, Dross Citadel in Algol: not flown);
  Emberglow 4,935 and GSC-0007 Dark Beacon Cluster 18,639 lie 19 and 27
  jumps out (table fields, 2026-11-17 15:03 UTC). A test stores, never
  sells (rule F24).
- The default stance `flee`: 34 of 60 miners set by 15:17 UTC (the
  script's state file); the other 26 from 19:22 UTC by the same script,
  22 minutes, inside the turn.
- A Flotation Cell (filter_copper_ore) on one iron miner: the iron share
  of its loads against about 50%. Not bought yet; a Liminal has the third
  slot for it.
