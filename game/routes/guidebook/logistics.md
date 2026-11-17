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
- The plan in force is the division's plan file (`plan.py show`, the tool
  plan); `game/routes/plan-hauler.md` is written from it, and every route
  with its figure is in `game/routes/master-index.md` and its sub-indexes.

## Class Card

The hauler's class in short (rule F14): it moves, makes and builds. The detail is in section 4
(levelling), section 5 (ships and fits) and section 15 (base building). Sources: the catalog's tables
`skills`, `hulls` and `facilities` (catalog 0.723.2), the game's help of `spacemolt_facility` and its
list of 318 actions (`get_commands`, read 2026-11-17 07:58 UTC), the table `ship_skills` and the tool
fleet with view=levels (levels below: 2026-11-17 12:01 UTC).

### Ships

- Tier 0, every hauler now: Threshold, cargo 65, fuel 95, hull 75, a mining laser and a pulse
  laser; four carry a Gas Harvester I, one a Cargo Expander I (hold 85).
- Tier 1, no Piloting asked: Ledger (no empire, cargo 480, hull 150, shield 70, speed 4) is the
  hauler's next hull, for it holds and survives, but no listing and no commission quote of it was
  read; Prayer (540, no shield) and Congregation (1,900, speed 1) are Outer Rim hulls listed on the
  exchange (section 5). No slot: they haul and cannot gather. None tested.
- Tier 2, Piloting 10 (about 57 hours away): Apophenia, the Voidborn freighter, cargo 240, hull 140,
  shield 145, fuel 300.
- Fit: hold first (Cargo Expander I, +20 hold, 352 cr); a Gas Harvester I only for the gas haulers.
  Default stance flee (game 0.721.0), set by script from 2026-11-17 07:54 UTC.
- Style: dock to dock, every leg with cargo; craft where the goods lie; build where the Fleet
  Admiral chooses; never fight.

### Skills

| Skill | Why it matters | What trains it, on which routes | Logistics now | Next goal |
|---|---|---|---|---|
| Crafting | Station workshop speed x1 at level 0 to x5 at 100 (the higher of Crafting and Refining); facility jobs ignore it | Crafting at a station: `@craft-reserve` (steel, copper piping), `craft-boards-*`, the Workshop Production Run mission (25 XP) | 2 to 4 on 38 haulers (2.7 on average) | 5 on the builder, 3 on every hauler |
| Refining | The same speed rule; smelting, gas and ice processing | `basic_iron_smelting` on `@craft-reserve` (crafting and refining rose together, 145 runs) | 2 to 4 on 38 (2.7) | as Crafting |
| Corporation Management | A faction facility of tier N asks its builder for level N (tier 1 asks none); needed for a station of our own | Building a faction facility: one Lockbox build took the builder from 0 to 3 (185 of 585 XP, the Fleet Admiral's reading of 2026-11-17 09:58 UTC) | 3 on the builder, 0 on the other three haulers of the faction | 4 on the builder, by the Hiring Board and the offices |
| Navigation | Fuel and jump fuel -1% a level, jump time -1% | Every jump: `@stored-goods` carries, the builder's hauls | 3 to 5 (3.6) | 5 |
| Piloting | Tier 2 hulls at 10, tier 3 at 20 | Flying, jumping, mining; 20 XP with each board mission | 5 / 7 / 8 (lowest, median, highest), 174 XP an hour, 50 hours to 10 | 10 |
| Voidborn Mastery | Our empire's skill: +1% cloak and energy weapon damage a level (rule F35) | Only Voidborn missions: the list First of the plan | 0 to 1 on 39 haulers (0.1) | 1 on every hauler |
| Engineering | Module power and CPU -1% a level, for a fuller fit | Crafting components or modules (the harvester chain) | 0 to 2 on 29 (0.1) | 2 on the builder |
| Trading | Sales of stored goods | Each sale: `@stored-goods` | 1 to 2 (1.8) | 3 |
| Mining, Deep Core Mining | The fallback only (rule F23) | `@gather-reserve`, `@gas-harvest`, the Then list | mining 4 to 7 (5.7), deep core 4 to 9 (7.0) | not a goal |

## Standing Plan

What the 40 haulers fly between two turns (2026-11-17 12:10 UTC, orders.log ENT-036), from the
division's plan file (`plan.py show`; the role plan `game/routes/plan-hauler.md` is written from
it). A free hauler takes the first route open to it of: the list First, its own routes, the list
Then. Figures: the runs of the four hours to 11:45 UTC (the briefing's standing fleet), credits per
ship-hour flown; the division's SUM line read 18,268 cr an hour of steady income over those runs,
680 per ship-hour flown, busy 67% of 160 ship-hours.

| Order | Template or routes | Ships | Carries | Per ship-hour (dated reading) | Why it stands here |
|---|---|---|---|---|---|
| First (every ship) | the 18 once missions (`voidborn-*`, `mission-cracking-the-shell-central`) | as their files say | -- | 2,032 cr paid once to haulers in the four hours | Strategy, principle 5; rule F35 |
| By script, this turn | the builder at Node Beta (`build.py`, section 15.4), two haulers carry crystal and copper to The Experiment | 3 | -- | fuel only | Orders ENT-036, block APOLLO (3): the Hiring Board, the gold boards |
| Own 1 (the builder) | `outpost-kit-ironlight-to-experiment` (off: the kit costs 148,663 cr), then `craft-boards-gold-experiment` | 1 | the 90 gold, 90 copper and 30 crystal in its storage at The Experiment | not measured | The outpost (orders (2)); the Recruitment Desk's last 60 boards (orders (3)) |
| Own 1 (the silicon hauler) | `craft-boards-node-beta`, then `gather-glasslight-shoal-silicon` | 1 | the 340 silicon ore it stores at Node Beta | the gather run -461 (1 run, 255 silicon ore) | Boards for the reserve (24,925 asked): 45 a run from 30 silicon |
| Own 1, a test (rule F34) | `mission-workshop-production-run-node-beta` | 1 | -- | not measured; 3,500 cr and 25 crafting XP a pilot | Crafting missions are Logistics' |
| Own 1 (two haulers) | `mine-achernar-gas-pocket`, `mine-grumium-belt` | 1 each | the bid at the selling end | Achernar -119 (3 runs), Grumium 2,677 (1 run, 20 palladium sold) | The best mine runs of the division |
| Own (every hauler) | `@stored-goods`: Trade's hydrogen and soma sells first, then plate, plasma, liquid hydrogen | 1 a route, only the pilot that stores the good, only while its bid stands | one ship while its bid stands | sell-hydrogen-at-node-beta 19,015 (4 runs), sell-soma-at-node-beta 10,958 (11), carry-hydrogen-synchrony-to-experiment 9,688 (3), sell-soma-at-synchrony 9,320 (8), sell-hydrogen-at-node-gamma 8,042 (5), carry-soma-synchrony-to-alpha 4,225 (12) | The paying work of the division; Trade keeps the floors |
| Own (the four gas haulers) | `@gas-harvest`: Achernar, Lesath, Amberfall | 1 each | the bid at the selling end | Achernar -119, Lesath -7,565 (1 run) | The gas they store feeds the hydrogen sells |
| Own (every hauler) | `@craft-reserve`: steel at Node Beta, Central Nexus, Synchrony Hub, then `craft-piping-plate-node-beta` | 11, 2, 3 (any role); piping 1 until its first RESULT line | the iron, plate and copper each pilot stores | craft-steel-node-beta 7 (178 runs) | Steel and copper piping for the reserve at 0 cr; trains crafting and refining |
| Own (every hauler) | `@gather-reserve`: Hamal Crystal Bloom, GSC-0027 Prism Scatter, Spacetime Seep | the fleet's shared caps | all three at their floors at 12:02 UTC | Hamal -214 (138 runs), Prism Scatter -140 (127) | The fallback: ore into storage. Not judged on pay |
| Then (every ship) | `gather-schedar-belt`, `gather-ironhollow-echo-ejecta`, `census-frontier`, `park` | -- | Mining's caps (45 and 35 of every plan) | Schedar -386 (170 runs), Echo Ejecta -229 (40) | The Fleet Admiral's list for every plan |

So, for the four hours: once money where a pilot still holds a link; hydrogen and soma into each
bid as it stands; the Hiring Board at Node Beta; 60 gold boards at The Experiment; 45 silicon boards
a run at Node Beta; plate and piping from what haulers store; iron gathered at Schedar and Echo
Ejecta by the rest.

What changes it: the Fleet Admiral's word on the kit's price (switch the kit route on, section
15.3); Schedar Belt at its floor (Mining expects it within about two hours): its haulers then take
the piping and steel crafts first; the piping test's first RESULT line (lift it to the haulers that
store plate); the Workshop mission's first RESULT line (lift it to every hauler that stores iron).

## 1. Route Guides

How each kind of route of this division is flown: the fit and the skills it needs, its
place, its steps, what opens and closes it. A credits figure in this section is a dated
reading and no verdict: what a route earns now is in the fleet's database with its age
(rule F22; the tool `routes`, the view `route_earnings`).

### 1.1 Stored goods sold or carried (template `stored-goods`)

- Fit: none. Trains trading (each sale) and navigation (each jump).
- Steps: a circuit; at the stop that sells, `withdraw` takes from the pilot's own
  storage only what the bid takes at its best price, `sell` puts it in; what is left goes
  back with `store`. A carry withdraws at the storing station and sells one hop away.
- Opens: `requires.stored` (only the pilot whose storage holds the good; storage is
  personal) and `requires.bid` (a book of the last hour shows the bid at its floor).
  `max_ships` 1: a pool bid of a few units takes one load.
- Closes: the bid read gone; the good sold out of that pilot's storage.
- Readings, 2026-11-16 19:16 to 2026-11-17 00:19 UTC (runs table): carry of liquid hydrogen
  Node Beta to Central Nexus 3 runs +4,854 cr in 24.6 min; liquid hydrogen sold at Node
  Beta 3 runs +1,876 cr in 7.7 min; plasma at Node Beta 3 runs +1,766 cr in 18.4 min;
  liquid hydrogen at Central Nexus 1 run -78 cr in 8.6 min (the bid had gone). The soma
  routes flew no run in the period.
- Earlier hand sales of the same kind (2026-11-15 and 16): neural soma into pools of 1 to
  4 units at 559 to 694 cr (+1,995 cr for 3 at Synchrony Hub, +2,381 for 4 at Node Beta);
  armor plate from carapace into pools of 3 to 6 at 222 to 396 cr (+4,240 cr for 12
  plates); stored hydrogen gas made into 75 liquid hydrogen and 42 sold at 116 cr
  (+4,798 cr in about 20 minutes). The bids, not the haulers, bound this work.

### 1.2 Crafting what we build with (template `craft-reserve`, and hand chains)

- Fit: none; the pilot stays docked while the workshop runs. Trains crafting and
  refining: one hauler went from crafting 0 to 1 and refining 0 to 1 on 145 runs of
  smelting (section 14).
- Steps: `craft-steel-node-beta` stores the hold, crafts `basic_iron_smelting` (10 iron
  ore, 1 steel plate, 0 cr) from the pilot's own iron, takes the plates aboard and stores
  them again. A stop's craft step asks the game for runs x per_run made units, its
  `quantity`, since commit 258a554 (queue.log ENT-128).
- Opens: `requires.stored` (800 iron ore at Node Beta) once per reading of the storage
  book, about every 40 minutes; 50 runs leave a margin for a book that old.
- Readings: 60 plates in 8.7 min for 24 cr (2026-11-17 00:03 UTC); one run found under
  600 iron because a hand craft had used 200 after the book was read (00:16 UTC, -60 cr).
- Hand chains, by the scripts of the skill logistics-stock: `catch.py` takes a hauler at
  the end of its run and flies it to the workshop; `craftchain.py` runs recipes in a row;
  `stage.py` stores, buys one unit first, fills a storage by loads, flies, gives to
  another pilot and crafts as many runs as the stored inputs allow.
- For a ship of any role (requests.log ENT-190, 2026-11-17 03:58 UTC): `craft-steel-node-beta`
  (50 runs, 550 iron stored there, 11 ships), `craft-steel-central-nexus` and
  `craft-steel-synchrony-hub` (25 runs, 300 iron, 2 and 3 ships). `max_ships` is what the
  stored ore carries for four hours at about 7 minutes a run.
- A craft in a public facility: a `craft` entry with `venue: "facility"` is asked without the
  workshop preset and the game rents a public facility; `max_fee` refuses a quote above runs x
  max_fee (route_run.py, commit 30a7961). `craft-steel-refine-node-beta` (refine_steel, 100 runs,
  max_fee 36): 500 iron ore into 200 plate for 2,900 cr in 1.3 minutes (2026-11-17 04:08 UTC,
  one run). A plate by refine: 2.5 iron and 14.5 cr; by hand: 10 iron and 0 cr. The route is in
  no plan while the Fleet Admiral weighs the fee (requests.log ENT-200).
- Recipes made by hand so far, all at a station workshop for 0 cr and with no skill
  asked: `basic_iron_smelting`, `basic_copper_processing`, `carbon_arc_circuit_etching`,
  `build_power_cell`, `build_ice_harvester_i`, `compress_hydrogen_gas`, `carapace_plating`,
  `draw_copper_piping` (12 copper ore and 2 steel plate, 4 copper piping, 1.6 ticks a run,
  2026-11-17 00:14 UTC). Quoted, not made: `fabricate_circuit_boards`.

### 1.3 Gas (template `gas-harvest`)

- Fit: a Gas Harvester I in the second utility slot (1,202 cr at Node Beta, section 5).
  Trains mining.
- Steps: the engine's mining loop at a gas cloud for the route's minutes; at the end the
  pilot docks at the route's station, sells into the bids at the route's floors and
  stores the rest of its hold there.
- Opens: the module, an empty hold (beyond the border, rule F13), a bid where named.
- Readings, 2026-11-16 19:16 to 2026-11-17 00:19 UTC: Amberfall 1 run -320 cr in 41.6 min,
  Deepwell haze 2 runs -1,428 in 128.3 min; The Experiment haze 2 runs +3,942 in 111.7 min
  (now Trade's claim). What a small bid does not take stays stored where the ship sold.

### 1.4 Gathering for the reserve (template `gather-reserve`)

- Fit: the starter mining laser. Trains mining and deep core mining.
- Steps: the engine's mining loop at the field for 45 minutes; the ore goes into the
  pilot's storage at Node Beta. A run ends where its minutes run out, often at the field;
  the loop finishes its sequence (mine, then dock at Node Beta) after the order ends, for
  minutes: `catch.py` waits for the dock (2026-11-17 00:10 to 00:14 UTC).
- Opens: a field's place under its fleet-wide cap; `min_left` closes a field.
- Readings, 2026-11-16 19:16 to 2026-11-17 00:19 UTC: Hamal Crystal Bloom 58 runs -7,575 cr
  in 2,437 min; Spacetime Seep 29 runs -3,305 in 1,093 min; Prism Scatter 20 runs -2,091 in
  840 min. Standing work: its cost is the fuel, about -150 to -190 cr a ship-hour.

### 1.5 Beyond the border (a test)

- `buy-gold-ironlight-boards`: one ship with an empty hold to Ironlight Crossroads (LHS
  1140, lawless, police 0, six jumps), 3 gold ore at 145 cr or less, booked as money paid
  once (craft inputs, requests.log ENT-172), then `fabricate_gold_circuit_boards` at Node
  Beta from the pilot's own stored copper ore and energy crystal. Written 2026-11-16
  23:58 UTC. First RESULT line: 2026-11-17 00:35 UTC, 3 of 3 stops in 20.6 min, -561 cr (414 of
  it gold booked once), 2 boards made. Out of the plan since 04:05 UTC: the 75 silicon ore Trade
  bought make the next 111 boards for no new spend. Our hunters sold at that station 14 times on 2026-11-16
  without a loss (runs table).

### 1.6 Missions that pay once (the list First)

- The once line is section 3. From 19:16 to 00:19 UTC haulers were paid 240,938 cr once
  (runs table, column one_time): Mining Missions 60,900, Missions 1 59,548, Substrate
  41,522, Conductive Lattice 29,420, Resonance Finish 26,548, Network Expansion 12,000,
  First Steps Board 9,000, First Hunt 2,000.
- A once route measured on another role's pilots may not open to a hauler: read its runs
  by role before it enters the plan (skill logistics-stock).

## 2. Route Templates

A kind of work is a named list of routes: a template. The templates of
this division are kept in `game/routes/templates/logistics.json` and listed
in `game/routes/templates-logistics.md`, a page a script writes once the
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
the file's history (`git log -- game/routes/guidebook/logistics.md`).

The division's templates (2026-11-17 12:05 UTC, `plan.py templates`):

| Template | Routes, in the order a ship tries them | Trains | Ships |
|---|---|---|---|
| `stored-goods` | Trade's three hydrogen and five soma sell and carry routes, then `sell-plate-node-beta`, `sell-plasma-node-beta` and the three liquid hydrogen routes (since 2026-11-17 08:00 UTC) | trading, navigation | 40 |
| `gas-harvest` | `mine-achernar-gas-pocket`, `mine-lesath-gas-cloud`, `mine-amberfall-emission-nebula` (clouds that sell at our own stations, since 2026-11-17 08:00 UTC) | mining | 4 (the Gas Harvester I) |
| `craft-reserve` | `craft-steel-node-beta`, `craft-steel-central-nexus`, `craft-steel-synchrony-hub`, `craft-piping-plate-node-beta` (since 2026-11-17 12:05 UTC) | crafting, refining | 40 |
| `gather-reserve` | `gather-hamal-crystal-bloom`, `gather-gsc-0027-prism-scatter`, `gather-gsc-0027-spacetime-seep` | mining | 40 |

Every hauler's cell reads `@stored-goods, @craft-reserve, @gather-reserve`; the four gas
haulers put `@gas-harvest` after the first; the builder, the silicon hauler, the two mine
haulers and the Workshop mission's test ship each put their own route before all.

## 3. Missions That Pay Once

| Route | What it pays and needs | Measured |
|---|---|---|
| `voidborn-signal-protocol` (Mercury's) | The Signal Protocol, 3,500 cr: docks at Node Beta and Node Gamma, hand-in at Central Nexus; needs The Collective Provides done | 5 hauler runs, +3,407 cr each in 14.3 min (2026-11-16 12:48 UTC) |
| `voidborn-hardware-cargo` (Mercury's) | Hardware Optimization: Cargo, 1,500 cr: a Cargo Expander I (352 cr at Synchrony Hub) held in the hold at the hand-in; the objective is `have_item`, a fitted module does not count | 2 hauler runs +1,070 cr each in 11 min with the module left aboard (utility slots full); 1 run -430 cr with it fitted, handed in later by `handin_module.py` +1,500 cr |
| `voidborn-atmospheric-extraction` (Mercury's) | Atmospheric Extraction: Setup, 2,000 cr: a Gas Harvester I (1,202 cr at Node Beta) held in the hold at the hand-in | 1 hauler run +738 cr in 8.8 min; 3 runs -1,262 cr with the harvester fitted; one of them handed in later, +2,000 cr |
| `voidborn-resonance-finish` (Mercury's) | Resonance Substrate and Final Calibration, about 15,000 cr less 15 energy crystals bought at Central Nexus (limit 430 cr) | no hauler run read yet; one hauler's chain run stopped after Conductive Lattice at +2,264 cr (13:03 UTC, `energy_crystal: not bought`) |
| `voidborn-precedence` | Precedence, 4,000 cr: accept at Node Beta, dock at Synchrony Hub and Node Alpha, hand in at Node Beta; nothing bought | first RESULT line +3,896 cr in 15 min (2026-11-15 23:31 UTC, the command group's test); all 20 haulers sent from 23:40 UTC, 13 on it at 23:44 UTC |
| `voidborn-selling` | Market Participation: Selling, 1,000 cr for 10 units sold; ten liquid nitrogen bought at The Experiment and sold there into the 2 cr bid | 7 hauler runs, +865 cr each in 4.9 min (2026-11-15 23:36 to 23:42 UTC); every hauler that held it has handed it in |
| `voidborn-first-hunt-nexus` | First Hunt: Belt-Grazers, 1,000 cr and 50 Weapons XP: three belt-grazers (60 hull) with the starter's Pulse Laser I, one hunter at a time (orders F9) | first RESULT line +974 cr in 18.9 min, lowest hull 100% (2026-11-15 23:39 UTC, the command group's test); in the hauler plan since 23:45 UTC |
| `voidborn-first-steps` | First Steps in the Void, 1,000 cr: mine 15 carbon ore at Acubens Belt, hand in at Central Nexus. On again since 2026-11-16 00:24 UTC, two ships at a time (requests.log ENT-071) | one hauler by hand: +913 cr in 10.8 min (2026-11-15 23:28 UTC). In the plan again: 6 hauler runs, +935 cr each in 9.2 to 10.1 min (2026-11-16 02:56 to 03:26 UTC) |
| `voidborn-concurrent` | Concurrent Approval, 3,000 cr; the soma it needs are handed out at the accept | 146 runs in the fleet, 2,970 cr a run (`routes.py measure`, 23:43 UTC); all 20 haulers flew it |
| `voidborn-substrate` | Substrate Delivery; the mission hands its 2 soma over at the accept, so nothing is bought | 146 runs, 1,790 cr a run (index) |
| `voidborn-missions-1` | Synchrony Relay Run and Crystal Delivery, 8 jumps | 146 runs, 6,430 cr a run (index) |
| `voidborn-mining-missions` | Iron Supply Run 1,500 cr and Copper Requisition 1,800 cr | 11 hauler runs, one-time +29,700 (`board.py Apollo`, 23:20 UTC) |

## 4. Levelling Guide

Which skills a ship of this division levels and on which work (rule F23): the work of
its own role first, gathering ore only when none is open. Every hauler is a Threshold.

| Kind of ship | Fit | Skills its work trains | Template | Next step |
|---|---|---|---|---|
| Hauler | mining laser, pulse laser | navigation (about 3 XP a jump, 1 a dock), trading (each sale), piloting | `stored-goods`, once missions | navigation 3 opens Signal Fragments (7,000 cr once) |
| Crafter (any hauler docked at a workshop) | none | crafting and refining (0 to 1 each on 145 smelting runs) | `craft-reserve`, hand chains | which crafting level a recipe asks for is not read: no quote asked for one |
| Gas hauler (4) | Gas Harvester I beside the laser | mining | `gas-harvest` | -- |
| Every hauler, fallback | mining laser | mining, deep core mining | `gather-reserve` | -- |

Levels on 2026-11-17 00:09 UTC (table ship_skills, 40 haulers): piloting 3 to 7 (average
4.5), deep core mining 1 to 7, mining 1 to 6, navigation 2 to 4, exploration 2, trading 0
to 2; crafting and refining 0 to 3 on the 9 haulers that carry them. The tool fleet
(view=levels, 00:01 UTC): Piloting median 6, 153 Piloting XP an hour since birth, 75 hours
to Piloting 10 and the tier-2 hulls at that rate (141 hours on 2026-11-16 09:00 UTC, 20
haulers).

Levels on 2026-11-17 04:05 UTC (table ship_skills; the tool fleet, view=levels): Piloting 4 /
6 / 7 (lowest, median, highest), 168 Piloting XP an hour since birth, 63 hours to Piloting 10;
navigation 3 or 4 on every hauler; crafting and refining 1 to 3 on haulers 1 to 20, none on the
20 born on 2026-11-16, which the any-role steel routes now train.

Levels on 2026-11-17 08:00 UTC (table ship_skills, 40 haulers; the tool fleet, view=levels): Piloting 5
/ 7 / 7, 171 Piloting XP an hour since birth, 57 hours to Piloting 10; navigation 3 to 5 (3.6 on
average); crafting and refining 2 to 4 on 36 haulers (2.6), none on 4; engineering 2 on one hauler;
Corporation Management 0 on all.

Navigation is bought with jumps: ten haulers went from navigation 2 to 3 in 3 to 6 loops
of six jumps and three docks between our own stations (49 loops, -5,341 cr, 2026-11-16
13:05 to 14:27 UTC; `train.py` of the skill logistics-stock), 534 cr a pilot against
7,000 cr once. First Hunt pays 50 Weapons XP, 15 Xenobiology XP and 20 Piloting XP.

A hull needs no Piloting level at tier 1: the freighters of section 5 are open to our
pilots today (`browse_ships` with can_fly, 2026-11-17 00:23 UTC). Piloting 10, 20, 30 and
50 open tiers 2 to 5.

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
the ask 1,202 cr). Four haulers carry one (table ship_modules, 2026-11-17 00:09 UTC); their
work is the template `gas-harvest` (section 1.3).

An Ice Harvester I made by hand went into a hauler's second utility slot
beside the mining laser the same way (`withdraw` from storage, then
`install_mod`, docked at Central Nexus, 2026-11-16 09:25 UTC): the Threshold
answer listed 2 utility slots, cpu 8 of 16 and power 17 of 30 in use.

A Cargo Expander I takes a utility slot (cpu 1, power 1, size 10) and lifts
the Threshold's hold from 65 to 85: one hauler bought one at Synchrony Hub for
352 cr in Hardware Optimization: Cargo and flies with it (2026-11-16 13:08 UTC,
get_ship `cargo_capacity` 85). The Threshold has two utility slots: a hauler
that carries a harvester and the mining laser has no room for it.

Next step up: Piloting 10 opens the tier-2 hulls, about 141 hours away at
the haulers' rate (section 4). Until then the step that pays is a tool, not
a hull: an ice harvester puts a hauler on routes measured at 4,000 to 8,400
cr per ship-hour (`hive.py tasks`, 03:28 UTC).

Hulls on the exchange (`browse_ships`, all charted stations, `can_fly` true for a hauler
of ours, 2026-11-17 00:23 UTC; the catalog's figures):

| Hull | Class, tier | Cargo | Speed | Hull, shield | Slots | Cheapest listing |
|---|---|---|---|---|---|---|
| Threshold (ours) | Miner, 0 | 65 | 1 | 75, 80 | 1 weapon, 2 defence, 2 utility | -- |
| Prayer | Freighter, 1 | 540 | 3 | 40, 0 | none | 3,848 cr at Frontier Station (18 jumps); 6,000 at Ironlight Crossroads (6 jumps, 2 listed) |
| Floor Price | Freighter, 1 | 400 | 1 | 55, 15 | 1 utility | 7,479 cr at Trader's Rest (22 jumps) |
| Worship | Freighter, 1 | 1,100 | 2 | 60, 0 | none | 9,741 cr at Deep Range Outpost (19 jumps) |
| Congregation | Bulk Hauler, 1 | 1,900 | 1 | 100, 0 | none | 12,080 cr at First Step Memorial Station (18 jumps) |

A freighter without slots carries no mining laser: it hauls and cannot gather. Buying a
listed ship stores the pilot's present ship at that station (the game's help of
`buy_listed_ship`). No Ledger (480 cargo) was listed; its commission quote asks a docked
ship and was not read. The first hull test is planned (plan file, Planned).

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
| `raw <pilot> deposit '{"item_id":"...","quantity":N,"target":"<another pilot of ours>","source":"cargo"}' spacemolt_storage` | hold to that pilot's storage at this station; the wall let it pass (2026-11-16, before 04:55 UTC). `scripts/gather.py` of the skill logistics-stock does it for many donors, withdraw first where the goods lie in storage |
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
| Nitrogen ice | 2 cr for 49 at The Experiment (the only bid read). Its hand recipe (5 ice to 4 liquid nitrogen) meets a 2 cr bid |
| Helium ice | 2 cr for 500 at The Experiment; its recipe is facility-only and helium-3 is bid 2 cr |
| Oxygen ice | No bid; its recipe is facility-only and oxygen gas has no bid |

LHS 1140 bids for methane ice only (36 cr for 500 at 23:45 UTC; nothing at 23:21 UTC). And no ship carries goods of value out of
Voidborn space (orders F13): a buyer beyond the border is no use to the
goods we store until that order changes.

## 10. Open Tests

- `craft-boards-node-beta`: first RESULT line 2026-11-17 04:47 UTC, 45 boards from 30 silicon in
  20 minutes, -770 cr (the carbon, booked once). `craft-boards-silicon-central-nexus` (08:05 UTC):
  65 boards from the builder's 43 silicon at Central Nexus; first RESULT line next turn.
- The Lockbox at The Experiment (section 15.2) and the default stance flee on every hauler
  (`set_stance.py`, from 07:54 UTC): read next turn.
- The three any-role steel routes (2026-11-17 03:58 UTC): which divisions' ships fly them once
  the Fleet Admiral puts them in every plan's list Then.
- The gas routes of `gas-harvest`, one ship each.
- A Prayer bought and flown by one hauler (section 5). `refine_steel` was flown once
  (section 1.2); its use waits on the Fleet Admiral's word.
- What the fleet owns and where: `python3 -I -B game/fleet/ledger.py show all`; the
  stations' list: section 13.

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
a harvester, carbon bounds it at about 14 and silicon at about 18. Each
pilot crafts from its own storage only: the goods are first deposited
into one pilot's storage at one station (a gift between our own pilots,
which the wall lets pass).

Staged for ten (2026-11-16 04:51 to 05:15 UTC): `scripts/gather.py` of the
skill logistics-stock moved 101 carbon ore, 138 iron ore and 106 copper ore
from six haulers docked at Central Nexus into the crafting hauler's
storage there; one hauler bought 30 flex polymer at Node Alpha at 129 cr
(3,908 cr, 3,958 with fuel); the workshop made 20 steel plate and 18 copper
wiring from them, free. That storage then held 20 steel plate, 18 copper
wiring, 103 carbon ore, 30 flex polymer and the harvester made before.
What ten more take: 40 steel plate, 40 circuit boards (14 etchings: 28
silicon, 168 carbon; or `fabricate_circuit_boards`, 2 silicon, 3 copper
and 1 crystal for 2 boards), 10 power cells (30 crystal, 20 wiring) and 30
flex. With 103 carbon and 30 silicon: 8 etchings and 7 fabrications give
38 boards, so 9 harvesters; 20 more steel plate (200 iron ore) and 2
wiring are still to be gathered.

Five made (2026-11-16 08:52 to 09:24 UTC, one hauler at the Central Nexus
workshop, by `craftchain.py` of the skill logistics-stock): 7 carbon-arc
etchings (14 silicon, 84 carbon) gave 21 boards, then 5 power cells, then 5
harvesters; 0 cr fee, no skill asked, about 32 minutes of crafting with the
waits. The etchings came as jobs of 3, 2, 1 and 1 runs because a craft's
`quantity` counts made units, rounded up to runs: 7 asked of a recipe that makes
3 a run is 3 runs (queue.log ENT-114, 2026-11-16 19:02 UTC); 5 power cells and 5
harvesters, 1 a run, were queued whole (about 32 and 70 ticks). The harvesters took about 18
minutes for five, about 3.6 minutes each against 13.9 ticks quoted (about
2.5 minutes at 11 s a tick). Mining gave 30 silicon ore and
35 energy crystal by deposit (requests.log ENT-124). The first harvester is
fitted to the hauler that made it (09:25 UTC); the five lie in its storage,
unplaced, because the bids bound ice work (section 12). Left there: 16
silicon, 20 crystal, 19 carbon, 15 flex polymer, 8 wiring, 1 board; four
more need 160 iron ore and about 15 copper ore gathered (1 etching and 6
`fabricate_circuit_boards` runs for their 16 boards).

## 12. Capacity of the Domain (orders F18)

Read 2026-11-16 23:49 to 2026-11-17 00:24 UTC (the tools stock with view=reserve, base_plan with
kind=station, fill with action=status, the runs table):

- Storage of Logistics at Node Beta: iron ore from 25 to 1,892 a pilot in 39 storages
  (Node Beta 600 or more in 19), copper ore up to 1,295 a pilot, energy crystal 1 to 15 in
  22 storages; the faction's 293 steel plate and 4 copper piping in one storage; at Central
  Nexus 32 silicon, 20 energy crystal, 15 flex polymer, 5 Ice Harvester I and carbon ore 1 to
  89 in 23 storages.
- What limits it first: the bids for the stored goods; the silicon for the boards (Trade's
  claim on the one deep ask); iron for the station.
- Ships the division's work employs: 33 on the shared gather fields, 1 on the steel craft,
  1 on the gold test, up to 11 on stored goods while their bids stand, up to 3 on gas, the
  once line for the rest. Logistics needs no more ships.

Read 2026-11-16 12:48 to 13:36 UTC (the tools stock, catalog with ask=can,
base_plan with kind=station, fill with action=status):

- Storage of Logistics: iron ore 11,431 and copper ore 6,063 at Central Nexus,
  Node Beta and Synchrony Hub; at Node Beta 213 argon, 204 hydrogen (made into 75
  liquid hydrogen at 13:35 UTC), 175 neon, 105 null matter and 83 plasma gas; 58
  neural soma by ones to fours in 29 storages (Synchrony Hub 30, Node Beta 21,
  Central Nexus 5, The Experiment 2; storage book of 13:44 UTC); 128 platinum, 30
  palladium, 84 nickel, 46 rhodium and 32 osmium ore from the reef of The
  Collective Provides; 6 armor plate (Node Beta 3, The Experiment 3); the chain's
  goods and 5 made Ice Harvester I at Central Nexus.
- What it makes by hand today (ask=can): steel plate and copper wiring from the
  ore (bids of 15 and 2 cr), ionized neon (bid 2 cr), one armor plate, and liquid
  hydrogen (111 cr x 112 at Central Nexus). The liquid hydrogen and the plate stood
  at the highest bids of these (books of 12:48 to 13:36 UTC).
- What limits it first: the bids. Soma pools of 1 to 4 at 376 to 734 cr, plate
  pools of 4 to 6 at 234 to 361 cr, plasma 33 at 96 cr, hydrogen gas 1 unit at
  34 cr at Node Beta at 13:36 UTC; water ice no bid at Central Nexus at 12:48 UTC.
- Ships the hauling employs: the once line for 5 to 10 haulers this turn; one
  ship per stored-goods route while its bid stands; three gas tests. No repeating
  route pays a hauler. Logistics needs no more ships.
- For the station (S6, base_plan 12:55 UTC): the five inputs the fleet holds most
  of by units are iron ore (59,564 of 491,400), copper ore (40,988 of 768),
  carbon ore (1,335 of 97,008), creature carapace (787 of 35,640) and platinum ore
  (523 of 3,720); the five it lacks most are iron ore (431,836 short; fields of
  100,000 at Ruchbah and Nightveil), salvage metal (249,600; no field, no offer),
  carbon ore (95,673; Gliese 876 and Furud belts, 44,531 on offer at 4 cr at Nova
  Terra Central), anchor plate (93,690; none) and alloy scale (56,520; none).
  Proposed to keep rather than sell: platinum ore (short 3,197; bid 63 cr, ask
  150 cr at Central Nexus), iron and copper ore (kept already), energy crystal
  (120 of 80) and nitrogen bladder (13 of 192; bid 1 to 2 cr).

Read 2026-11-16 08:47 to 09:00 UTC (the tools stock, fleet with
view=capacity, catalog with ask=can, base_plan with kind=station):

- Storage of Logistics: iron ore 11,431 and copper ore 6,063 at Node Beta,
  Synchrony Hub and Central Nexus; 204 hydrogen, 213 argon, 175 neon and 83
  plasma gas at Node Beta; 58 neural soma (storage book of 09:16 UTC); the chain's goods at Central
  Nexus; 6 armor plate after this turn's sales.
- What it makes by hand today (ask=can): armor plate from the carapace
  left (about 1 to 3 plates a station), 75 liquid hydrogen (bid 98 x 12),
  copper wiring and steel plate with no bid worth a sale.
- The work a harvester opens: water ice is bid at 29 cr for 5,333 units at
  Central Nexus, about 20 ships for four hours, methane ice about 27, and 48
  ships carry a harvester. The bids, not the tool, bound ice work today, as
  Zero answered (requests.log ENT-115).
- Ships the hauling employs: the once missions for every hauler that turn; no
  repeating route was measured for haulers then. Logistics needs no more ships; each
  repeating place that opens (a bid that regains more than the miners take)
  is one waiting hauler put to work.
- For the station (S6, base_plan 08:59 UTC): the five inputs the fleet holds
  most of against the need are copper ore (40,928 held, 768 needed), iron
  ore (59,458 of 491,400), creature carapace (746 of 35,640), carbon ore
  (814 of 97,008) and energy crystal (135 of 80); the five it lacks most are
  iron ore (431,942 short; fields of 100,000 at Dimming Pocket and Low
  Charge Glint), salvage metal (249,600; no field, no offer), carbon ore
  (96,194; Gliese 876 and Furud belts, 44,531 on offer at 4 cr at Nova Terra
  Central), anchor plate (93,690; none) and alloy scale (56,520; none).

## 13. The Stations' List (orders.log ENT-017 and ENT-020, P4)

One station takes a fee of 5,000,000 cr, one station core and the foundry that
makes it (38,000,000 cr); two stations take the list twice. Read 2026-11-16 18:26
UTC (the tool base_plan with kind=station) against the storage book of 18:37 UTC
(`data/stock/storage.json`, summed per station). Units are for one station.

| Input | Needed | Held | Where it lies (units) | Missing | Known source |
|---|---|---|---|---|---|
| iron ore | 491,400 | 107,707 | Node Beta 75,679, Synchrony Hub 22,254, Central Nexus 9,296 | 383,693 | fields of 100,000 at Nightveil and Marfik; 24,442 asked at 1 cr at Central Nexus |
| salvage metal | 249,600 | 0 | -- | 249,600 | none read |
| carbon ore | 97,008 | 2,133 | Central Nexus 1,864, Node Beta 148 | 94,875 | Gliese 876 belt (2,901 left), Furud belt (612); 44,531 asked at 4 cr at Nova Terra Central |
| anchor plate | 93,690 | 0 | -- | 93,690 | none read |
| alloy scale | 56,520 | 0 | -- | 56,520 | none read |
| silicon ore | 52,808 | 34 | Central Nexus 34 | 52,774 | 424 asked at 420 cr at Central Nexus (book of 19:07 UTC); 1 to 4 units at 312 to 376 cr elsewhere |
| salvage components | 41,600 | 0 | -- | 41,600 | 546 asked at 87 cr at Node Alpha |
| foil scale | 41,220 | 0 | -- | 41,220 | none read |
| creature carapace | 35,640 | 904 | Node Beta 365, Central Nexus 312, The Experiment 157 | 34,736 | Military's hunts |
| verdigris curd | 34,832 | 37 | Node Beta 21 | 34,795 | Military's hunts |
| ferrous nodule | 28,260 | 0 | -- | 28,260 | 636 asked at 60 cr at Synchrony Hub |
| nickel ore | 18,320 | 514 | Node Gamma 290, Central Nexus 224 | 17,806 | 2,669 asked at 100 cr at Central Nexus |
| gold ore | 16,740 | 0 | -- | 16,740 | Gold Crest (764 left), Rastaban belt (589) |
| graphene thread | 13,260 | 0 | -- | 13,260 | none read |
| silica lens | 10,440 | 0 | -- | 10,440 | none read |
| crystallized biogas | 4,420 | 118 | Central Nexus 48 | 4,302 | 7 asked at 165 cr in LHS 1140 |
| irradiated marrow | 4,000 | 0 | -- | 4,000 | none read |
| quantum fragments | 3,720 | 0 | -- | 3,720 | 24 asked at 600 cr at Node Beta |
| platinum ore | 3,720 | 799 | Central Nexus 503, Node Gamma 225 | 2,921 | 29 asked at 250 cr at Central Nexus |
| uranium ore | 2,304 | 0 | -- | 2,304 | Acubens belt (1 left) |
| thorium ore | 1,200 | 0 | -- | 1,200 | none read |
| copper ore | 768 | 75,869 | Node Beta 49,796, Synchrony Hub 19,253 | 0 | held |
| fluorine gas | 384 | 0 | -- | 384 | 192,627 asked at 36 cr in LHS 1140 |
| nitrogen bladder | 192 | 45 | Central Nexus 33 | 147 | 6 asked at 27 cr at Nova Terra Central |
| cobalt ink | 192 | 0 | -- | 192 | none read |
| lithium ore | 120 | 1 | Central Nexus 1 | 119 | Stormwatch belt (25,000), Acrux belt (12,182) |
| cobalt ore | 80 | 0 | -- | 80 | 200 asked at 140 cr in LHS 1140 |
| energy crystal | 80 | 528 | Node Beta 408, Central Nexus 120 | 0 | held |
| hoarfrost heartcore | 40 | 0 | -- | 40 | none read |
| polonium ore | 20 | 0 | -- | 20 | 200 asked at 1,000 cr in LHS 1140 |

So: 28 of 30 inputs are short; 18 have a field or an offer in our readings, 2 more
come from Military's hunts, and 10 have none: salvage metal, anchor plate, alloy
scale, foil scale, graphene thread, silica lens, irradiated marrow, thorium ore,
cobalt ink and hoarfrost heartcore (Intel's search, orders ENT-017).

Steel is the largest made step: 49,140 plate by `basic_iron_smelting` (10 iron ore
a plate) is what makes the iron line 491,400. The catalog names cheaper ways in
iron (`catalog`, item steel_plate): `refine_steel` in a facility, 5 iron ore for 2
plate (2.5 a plate; a public facility quoted 19 cr on 2026-11-15, section 7, and
that quote does not say whether for one run or two), and by hand
`sinter_tungsten_steel` (4 iron, 2 tungsten for 3 plate) or `forge_vanadium_steel`
(4 iron, 2 vanadium for 3). By refine_steel the iron line would be 122,850 units
and 24,570 runs, about 233,000 to 467,000 cr of fees; the fleet holds 107,707 iron
ore today. Which way the stations' steel goes is not decided; the hand recipe asks
no facility and no fee.

Copper piping (26,120 for one station) is reckoned above from verdigris curd
(`verdigris_smelting`, 4 curd for 3 piping), which the fleet barely holds (37 of
34,832). The catalog lists a second hand recipe, `draw_copper_piping`: 12 copper ore
and 2 steel plate make 4 copper piping (`catalog`, recipes that make copper_piping,
2026-11-16 19:20 UTC). By it the piping takes 78,360 copper ore, about what the
fleet stores today (75,869), and 13,060 steel plate more (130,600 iron ore), and
the curd line falls away. Not quoted or made yet: the next step to test.

What one station's steps take, by hand or in a facility, against what we hold (the tool
base_plan with kind=station and the catalog's recipes, 2026-11-17 00:00 to 00:21 UTC):

| Step | Recipe | Today | Why |
|---|---|---|---|
| steel plate | `basic_iron_smelting` by hand | yes | 219,328 iron ore held of 491,400, 21,932 plates by hand; about 25 plates a minute at the workshop (section 14) |
| copper piping | `draw_copper_piping` by hand | yes, tested | 12 copper and 2 plate for 4 piping (2026-11-17 00:14 UTC); copper held 144,122 |
| copper wiring | `basic_copper_processing` by hand | yes | copper held |
| armor plate | `carapace_plating` by hand | in part | 1,164 carapace, 194 plates of 5,940 |
| liquid nitrogen | `nitrogen_bladder_decanting` by hand | in part | 49 bladders, 48 of 192 |
| circuit board | four hand recipes | in part | silicon 32 held (no field read), or gold bought beyond the border (section 1.5) |
| gold wiring, processing core | `draw_gold_wire`, `assemble_gold_processing_core` by hand | not yet | gold ore: none held; fields at Gold Crest and Rastaban, an ask at Ironlight Crossroads |
| power battery | `assemble_power_battery` by hand | not yet | 3 lithium and 2 cobalt ore each: lithium asked at 14 cr and cobalt at 140 cr at Ironlight Crossroads |
| silicate composite | `sinter_silicate_composite` by hand | no | 4 silicon a unit, 36,640 silicon for 9,160 |
| hull plating | `reforge_hull_plating` by hand | no | salvage metal and salvage components come from wrecks (the catalog's text); none held |
| titanium alloy, durasteel plate, aluminum sheet, graphene sheet, control node, power cell | by hand from creature parts | no | anchor plate (magnet-barnacle), alloy scale (cauldronback), foil scale (mirror-skate), graphene thread (inkwyrm), silica lens (silica-borer), irradiated marrow (geiger-hound): the catalog names each creature; none read in our herds |
| docking ring, reinforced bulkhead, reinforced frame, quantum control core, quantum dot matrix, the reactors, the core | a facility only | no | four facility types each; whether a public facility at our stations runs them is not read |

So the station waits first on creature parts and wreck salvage, which no field and no
book of ours holds: the search for those creatures is Intel's and the hunt Military's.
Steel is the step that eats iron: `refine_steel` in a facility takes 5 iron for 2 plates
against 10 for 1 by hand; its fee per run is not read yet (planned).

## 14. The Faction's Plates and Boards (orders.log ENT-017 and ENT-020, P5)

The lockbox and the hiring board take 275 steel plate and 75 circuit boards
(orders ENT-017). Who builds them and where is the Fleet Admiral's; the goods move
to the builder by a deposit to that pilot (section 7).

Steel plate, made 2026-11-16 18:59 to 19:05 UTC at the Node Beta workshop by
`basic_iron_smelting` (10 iron ore, 1 plate, 0.27 ticks a run, 0 cr), from the iron
ore the gather routes put into hauler storage there (catch.py and craftchain.py of
the skill logistics-stock, logs of the turn):

| Batch | Plates | Minutes of crafting | Credits | Skill |
|---|---|---|---|---|
| one hauler, 1,450 iron ore | 145 | 5.7 | 0 | crafting 0 (25 XP) to 1 (75 XP), refining 0 (15 XP) to 1 (65 XP): about 110 XP each for 145 runs |
| one hauler, 1,170 iron ore | 117 | 5.2 | 0 | not read |
| one hauler, 130 iron ore | 13 | 0.7 | 0 | not read |

So 275 plate took 2,750 iron ore, 0 cr and about 6 minutes of workshop time with
three haulers in parallel, about 25 plates a minute a hauler; no skill is asked.
The two smaller batches went by deposit into the first hauler's storage (117 and 13
plates, three loads of 57 at most). All 275 lie in one Logistics storage at Node
Beta (`view` of that storage, 19:08 UTC). What the hand took besides: each hauler
was taken at the end of its gather run, where its minutes ran out (at the field),
and flown to Node Beta, 3.5 to 5 minutes; those hops are the ones its gather run
flies anyway.

For the stations' 49,140 plate the same recipe takes 491,400 iron ore and, at
about 25 plates a minute, about 33 hours of one docked hauler's workshop time;
`refine_steel` in a facility takes a quarter of the ore (section 13).

Circuit boards, 2026-11-17 00:45 UTC: 1 held. Mining gave 16 silicon ore and 17 carbon ore
into the crafting hauler's storage at Central Nexus (requests.log ENT-175), which then held
32 silicon and 36 carbon (the game's storage view, 2026-11-16 23:53 UTC). Four hand recipes
make boards (catalog 0.719.3):

| Recipe | Inputs | Boards | Ticks a run |
|---|---|---|---|
| `carbon_arc_circuit_etching` | 2 silicon ore, 12 carbon ore | 3 | 6 |
| `fabricate_circuit_boards` | 3 copper ore, 2 silicon ore, 1 energy crystal | 2 | 6 |
| `fabricate_gold_circuit_boards` | 3 copper ore, 3 gold ore, 1 energy crystal | 2 | 9 |
| `reclaim_circuit_boards` | 3 rare salvage, 5 salvage components | 1 | 3 |

Made and given, 2026-11-17: 16 etchings, 48 boards, at the Node Beta workshop from 01:44 to
02:01 UTC (stage.py; 192 carbon ore bought there at 4 cr, 787 cr); 200 steel plate and 50
circuit boards given to the Fleet Admiral's flagship at Node Beta from 04:07 to 04:11 UTC by
script (catch.py and stage.py: `withdraw` to the hold, then `deposit` with the flagship as
`target` and `source` cargo; HTTP 200, 0 cr, the giver's hold lighter by each load; requests.log
ENT-197). Next: `craft-boards-node-beta`, 45 boards a run (section 1.2), from the 32 silicon
at Node Beta; 43 more silicon lie at Central Nexus.

Before (kept for the record): the crafting hauler was taken at the end of its run (about 01:23 UTC) by
`catch.py`, carries its silicon, carbon and board to Node Beta, buys carbon there at 4 cr up
to 192 in storage, etches 16 runs (48 boards) and gives every board into the storage that
holds the faction's steel plate (`stage.py` of the skill logistics-stock). Its log is read
next turn. With the board held, 49 of 75.

The other 26: silicon has no field in the 66 systems Intel read (admirals.log ENT-003); the
one deep ask, Central Nexus at 420 cr for 425 units (book of 2026-11-16 23:49 UTC), is
Trade's claim (admirals.log ENT-004), and 18 units are asked of Trade (requests.log
ENT-179). Gold needs no silicon: Ironlight Crossroads asked gold ore at 138 cr, and the
test `buy-gold-ironlight-boards` makes 2 boards from 3 of it (section 1.5). A board costs
about 280 cr of silicon at 420 cr by etching, about 207 cr of gold at 138 cr, and 515 to
743 cr bought whole at the asks of our books (2026-11-16 23:30 to 23:49 UTC).

Boards, 2026-11-17 08:10 UTC (storage book of 07:25 to 07:32 UTC): 51 held by Logistics (45 and 1 at
Node Beta, 5 at Central Nexus); 50 go to the Lockbox at The Experiment (section 15.2), 1 stays. The
Hiring Board and the Recruitment Desk take 125: `craft-boards-silicon-central-nexus` makes 65 from the
builder's 43 silicon ore, which leaves about 59. Ways to them, each per board: Ironlight Crossroads asks
boards at 301 cr for 74 (book of 07:55 UTC), the cheapest ask read; gold ore asked there at 142 cr makes
a board for 213 cr of gold and half an energy crystal (asked at 420 cr at Central Nexus); Mining stores
135 gold ore at The Experiment and the command group and Intel 671 energy crystal at Node Beta, which
make 90 boards for no new credits if the Fleet Admiral allocates them (rule F31; requests.log).

## 15. Base Building: the Builder's Work (orders.log ENT-031)

Logistics is the fleet's base builder from 2026-11-17 (rule F16): the Fleet Admiral chooses each site
and allocates its credits and materials (rule F33); the build, its supply and its upkeep are ours.

### 15.1 What the game says

Read 2026-11-17 07:58 UTC: the help of `spacemolt_facility` and the game's list of actions
(`get_commands`, 318); `game/rules/09-factions.md`; `governance/empire.md`, section 5; the tool
base_plan. A line marked "read" was not flown by us.

- A faction facility: `spacemolt_facility facility` with `action` `faction_build` and
  `facility_type`, docked at the station, permission manage_facilities. Faction storage (the
  Lockbox) comes first at every station. The materials come from the faction's store there (or a
  named Storage Extension bucket); the ship's cargo backfills a shortfall (read). The first Lockbox,
  at Node Beta, was built from the builder's own storage there (the Fleet Admiral, 2026-11-17 05:38
  UTC). A facility of tier N asks its builder for Corporation Management N; tier 1 asks none (read).
- Rent at a station that is not ours: every 100 ticks (about 17 minutes), from the treasury: the
  Lockbox 69 cr a cycle, 5,962 cr a day (`governance/empire.md`, section 5). Paused while it is
  built; unpaid, the facility stops but storage stays reachable. None at our own station or outpost.
- An outpost: `spacemolt_facility deploy_outpost` (in the action list; its parameters are not in
  the help text): an Outpost Kit (30 units of hold) in the cargo of an undocked ship at a place of a
  lawless system without a station, permission manage_bases, a fee of 100,000 cr (the treasury
  first, then the wallet: `base_cost`). Eight per faction, any number per system. It comes with
  faction storage and a fuel bunker, serves members only, pays no rent and draws no maintenance;
  fuel deposited in its bunker refuels our ships free (read). `dismantle_outpost`, docked there,
  packs it back into a kit; the fee is lost and its storage must be empty first.
- A station of our own: `found_station` with a Station Core in the cargo, 5,000,000 cr, five per
  faction, one per system; then faction storage, power, life support and services by
  `faction_build`. Every service and infrastructure facility draws maintenance from faction storage
  each cycle and goes offline when undersupplied (help text). What each draws: not read; the card
  `facility types facility_type=<id>` answers it and is refused to a pilot on a run.
- The kit made by us: `assemble_outpost_kit` in an outpost frame assembler (level 2, 600,000 cr,
  800 steel plate, 300 circuit boards, 120 reinforced frames, 40 control nodes: base_plan, 07:54
  UTC). Bought: 74,010 cr at Ironlight Crossroads in LHS 1140, 2 listed (book of 07:55 UTC). The
  first kit is bought.

### 15.2 The Lockbox at The Experiment (orders P5 and block APOLLO (2))

The builder is a hauler with crafting 4 and engineering 2, which made the boards. It carries the
Lockbox's goods into its own storage at The Experiment Research Station and waits there, docked and
held by my hand, until the Fleet Admiral takes it at 09:30 UTC (`holdfor.py` of the skill
logistics-stock: it keeps the hold fresh, stops the moment another hand or a runner takes the ship,
and lets go at 11:30 UTC). Loads, by `catch.py` and `stage.py` at the end of each pilot's gather run
(2026-11-17 from 07:52 UTC): the builder 45 boards and 20 plate; three donors 64, 65 and 51 plate and
1 board from Node Beta; one donor 4 boards from Central Nexus; each donor gives into the builder's
storage at The Experiment, one unit first. Done 08:41 UTC: the builder's storage there read 200 steel
plate and 50 circuit boards (the game's storage view); each donor took 6.5 to 10.1 minutes from the
end of its run, 0 cr but fuel, no run cut. A deposit into the storage of a pilot that is not at the
station landed (08:22 UTC). The build is the Fleet Admiral's at 09:30 UTC; its outcome is entered
here at the next turn.

### 15.3 The first outpost as routes (task 3; deploy nothing yet)

The site is the Fleet Admiral's to choose. Mining and Intel name Garnet (admirals.log ENT-018,
ENT-021), two jumps beyond The Experiment through Achernar: by the table systems that is 2 systems
beyond our space (Garnet 5 jumps from home, our border 3), where rule F33 asks 3 or 4. At 3 or 4
beyond: GSC-0044 (Mining's earlier choice, reports.log ENT-057) and Atlas, 3 jumps from The
Experiment each; Felis, Intercrus, Botein and Acrux, 4 to 6. Distances (table lanes): Node Beta to
LHS 1140 6 jumps; LHS 1140 to The Experiment 4 (Antares, GSC-0041, Ironhollow, three of them
lawless); The Experiment to Garnet 2, to GSC-0044 3 (Achernar, Cedarhold), to Atlas 3 (Achernar,
Garnet); LHS 1140 to GSC-0044 5. The kit is staged at The Experiment whatever the site.

| Step | How | Cost | State |
|---|---|---|---|
| 1. The kit | `outpost-kit-ironlight-to-experiment`: one ship with an empty hold to Ironlight Crossroads, 1 kit at 75,000 cr or less (booked once), stored at The Experiment | 74,010 cr and about 10 jumps of fuel | written, off; a guard of Military for the 4 loaded jumps is asked before it is switched on |
| 2. The founding | The builder withdraws the kit at The Experiment, flies to the chosen place, stays undocked, `deploy_outpost`; the faction gives it manage_bases | 100,000 cr from the treasury | a first call: one flight by hand, then a script |
| 3. Fuel for its bunker | How fuel goes into a bunker is not read: the first test after the founding, one hauler. The good to carry is the fuel cell (a ship burns cells from its cargo where no station sells fuel: help of `refuel`), asked at 100 cr in depth at Central Nexus (1,911), Node Alpha (3,219) and The Experiment (3,842), the border station nearest the sites (Trade's readings, admirals.log ENT-022, books of 07:36 to 07:42 UTC); a fuel cell restores 20 fuel in one unit of hold (catalog), so a Threshold's 65 cells carry 1,300 fuel for 6,500 cr; the reserve keeps every fuel cell (game/reserve.tsv) | 6,500 cr a hold | open |
| 4. Stock in and out | Miners at the site's fields deposit ore into the outpost's faction storage; haulers carry loads to The Experiment's workshop (2 jumps from Garnet, 3 from GSC-0044 or Atlas) (an outpost has storage and fuel, no workshop and no market) | fuel | routes written once the outpost stands |

Credits for the whole: 174,010 cr and the fuel. What it draws each cycle: nothing (read).
