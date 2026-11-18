# Logistics guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section Standing Plan.

What the 40 haulers fly between two turns (2026-11-18 00:12 UTC, orders.log ENT-052), from the
division's plan file (`plan.py show`; the role plan `game/routes/plan-hauler.md` is written from
it). A free hauler takes the first route open to it of: the list First, its own routes, the list
Then. Figures: credits per ship-hour flown over the runs of the last four hours, every division's
pilots on the route counted (view route_earnings, 00:08 UTC). The briefing's SUM line at 23:45 UTC:
37 haulers on standing work, 1 on a route that pays, 1 on a test, 1 on a route that pays once;
-3,773 cr an hour of steady income over four hours of runs and 45,533 cr paid once; busy 71% of
160 ship-hours. Most of that standing work was iron gathering, which the reserve no longer takes
(iron 359,030 held of 314,400, the tool stock view=reserve 23:49 UTC): this plan takes it out.

| Order | Template or routes | Ships | Carries | Per ship-hour (dated reading) | Why it stands here |
|---|---|---|---|---|---|
| First (every ship) | the once missions (`voidborn-*`, `mission-cracking-the-shell-central`, the first hunts), `voidborn-crystal-resonance` and `voidborn-material-synthesis` (Mining's, added 00:12 UTC), `mission-workshop-production-run-node-beta` (4 at a time) | as their files say | -- | Crystal Resonance paid 4,000 cr once and Material Synthesis 1,500 (one miner run each, 23:25 and 23:27 UTC); the Workshop mission 32 runs in four hours, 2,620 a ship-hour | Strategy, principle 5; rules F34, F35 |
| Own 1 (3 member haulers) | `supply-bunker-gsc-0044`: 65 fuel cells from The Experiment into our outpost's bunker by the runner's `bunker` step | 1 at a time, 3 runs in all (`once`, `max_pilots` 3) | the bunker's draw: 18 fuel from 21:17 to 23:52 UTC | first run begun 00:12 UTC | Orders block APOLLO (1); section 15.3 |
| Own 1 (5 member haulers) | `buy-flex-ironlight-to-node-beta`: 57 flex polymer a load at Ironlight Crossroads into the faction store at Node Beta | 2 at a time, 5 runs in all | the ask, 121 cr x 300 (00:00 UTC) | first run begun 00:12 UTC | Orders block APOLLO (4): the Recruitment Center's 300 flex |
| Own 1 (the silicon hauler) | `craft-boards-node-beta`, then the template rows | 1 | its 1,038 silicon at Node Beta | not flown in four hours | Boards for the Center and the reserve (23,751 short) |
| Own 1 (two haulers) | `mine-achernar-gas-pocket`, `mine-grumium-belt` | 1 each | the bid at the selling end | Achernar 1,359 (3 runs) | The best mine runs of the division when their bids stand |
| Own (every hauler) | `@stored-goods`: Trade's hydrogen, soma, null matter and palladium sells and carries, then plasma and liquid hydrogen | 1 a route, only the pilot that stores the good, only while its bid stands | one ship while its bid stands | sell-hydrogen-at-node-beta 21,607 (6), sell-palladium-at-node-gamma 21,208 (2), sell-null-matter-at-nexus 55,970 (5), carry-null-matter-beta-to-nexus 11,566 (5), sell-soma-at-synchrony 8,499 (7), sell-soma-at-node-beta 5,500 (14) | The paying work of the division; Trade keeps the floors |
| Own (the four gas haulers) | `@gas-harvest`: Achernar, Lesath, Amberfall | 1 each | the bid at the selling end | Lesath -434 (2), Amberfall 184 (1) | The gas they store feeds the hydrogen and plasma sells |
| Own (every hauler) | `@craft-reserve`: `craft-steel-logistics-experiment`, `-node-beta`, `-synchrony-hub`, `-central-nexus` (all of a hauler's own iron in one visit), then `craft-piping-plate-node-beta` | 8, 8, 3, 3; piping 2 | the iron each hauler stores: 16,129 at The Experiment, 6,483 at Node Beta, 1,789 at Synchrony Hub, 2,003 at Central Nexus, about 2,640 plate in all | Trade's twin craft-steel-own-node-beta -202 (13 runs), craft-steel-own-experiment -454 (11) | Steel plate for the reserve (31,440 to make); trains crafting and refining |
| Own (every hauler) | `@gather-reserve`: `gather-glasslight-shoal-silicon` | 1 | the field under 65 silicon at 00:12 UTC | -460 (2 runs) | Gathers only what the reserve lacks; the iron and copper fields left the template |
| Then (every ship) | `census-frontier`, `park` | -- | Intel's census (12 for every plan) | -620 | The frontier census stands in every plan (rule F13); `park` docks a ship with no work |

So, for the four hours: the outpost's bunker and the Center's flex by routes; every hauler smelts
the iron it stores (26,404 iron ore, about 2,640 plate, one visit per hauler and station); stored
goods into each bid as it stands. A
hauler with none of that open docks at home: the iron gathering that kept 37 ships busy fed
nothing (orders ENT-052, P2; requests.log ENT-256, step 4: dock last).

What changes it: the bunker route's RESULT line and the reserve after (then max_pilots up, or the
gate of requests.log ENT-266); the Fleet Admiral's allocation for Atria (requests.log ENT-268; the
kit route is written and off); a reserve-short field read near home (silicon, carbon, gold,
nickel: within 8 jumps only Gliese 876, Furud, Gold Crest, Atria and HD 147513 hold any, read
00:07 UTC, and Mining or Intel claim them); a bid that comes back for a stored good.

### Route Guides
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 1.

How each kind of route of this division is flown: the fit and the skills it needs, its
place, its steps, what opens and closes it. A credits figure in this section is a dated
reading and no verdict: what a route earns now is in the fleet's database with its age
(rule F22; the tool `routes`, the view `route_earnings`).

### Stored goods sold or carried (template `stored-goods`)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 1.1.

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

### Crafting what we build with (template `craft-reserve`, and hand chains)
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section 1.2.

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
- All of a hauler's own iron in one visit (`craft-steel-logistics-experiment`, `-node-beta`, `-synchrony-hub`,
  `-central-nexus`, written 2026-11-18 00:12 UTC from Trade's `craft-steel-own-node-beta`, admirals.log ENT-065): the
  craft list asks `basic_iron_smelting` in halving sizes, 128 to 1 runs; the runner quotes each entry and makes
  nothing where the stores fall short, so the pilot smelts what it holds (up to 2,550 iron) and needs no 550 in store
  as the older 50-run routes did. Opens on 100 iron stored there. Trade's twins read -202 cr a ship-hour (13 runs) at
  Node Beta and -454 (11) at The Experiment (view route_earnings, 00:08 UTC).
- A craft in a public facility: a `craft` entry with `venue: "facility"` is asked without the
  workshop preset and the game rents a public facility; `max_fee` refuses a quote above runs x
  max_fee (route_run.py, commit 30a7961). `craft-steel-refine-node-beta` (refine_steel, 100 runs,
  max_fee 36): 500 iron ore into 200 plate for 2,900 cr in 1.3 minutes (2026-11-17 04:08 UTC,
  one run). A plate by refine: 2.5 iron and 14.5 cr; by hand: 10 iron and 0 cr. The route is in
  no plan while the Fleet Admiral weighs the fee (requests.log ENT-200).
- Copper piping from what a hauler already stores (`craft-piping-plate-node-beta`, written 2026-11-17
  12:05 UTC): 15 runs of `draw_copper_piping` take 180 copper ore and 30 steel plate and make 60 piping,
  which fit one hold; `requires.stored` asks 130 plate and 180 copper at Node Beta, so each storage keeps
  100 plate. First RESULT line 12:10 UTC: 2 of 2 stops in 9.1 minutes, 60 piping, -39 cr (the hop from
  Synchrony Hub); about 4 piping every 11 to 22 seconds at crafting 3. Lifted to 8 ships at 12:10 UTC. Trade's
  `craft-piping-node-beta` smelts its plate from iron first and stands after it in `@craft-reserve`.
- Boards from silicon a hauler gathered: `craft-boards-node-beta` (45 boards a run from 30 silicon, carbon
  bought at 4 cr) is the first own route of the hauler that gathers at Glasslight Shoal, which brought 255
  ore in each of two runs of about 95 minutes, -732 and -740 cr (2026-11-17 09:04 and 10:40 UTC).
- Boards from gold: `craft-boards-gold-experiment` (written 12:00 UTC) makes 30 runs of
  `fabricate_gold_circuit_boards` (3 copper, 3 gold, 1 energy crystal for 2 boards, 9 ticks a run) at The
  Experiment from Mining's 90 gold ore and 30 crystal and 90 copper two haulers carried there from Node
  Beta (catch.py and stage.py, one unit first; the first carry done in 7.8 minutes, 12:10 UTC).
- `craft-boards-silicon-central-nexus` flew once (2026-11-17 09:58 UTC): 6 of 6 stops in 32.5 minutes,
  65 boards, 968 cr of carbon booked once. Its figure in route_earnings, about 158,000 cr a ship-hour, is
  the outpost's gifts landing in the wallet during the run, not earnings (requests.log ENT-220).
- Recipes made by hand so far, all at a station workshop for 0 cr and with no skill
  asked: `basic_iron_smelting`, `basic_copper_processing`, `carbon_arc_circuit_etching`,
  `build_power_cell`, `build_ice_harvester_i`, `compress_hydrogen_gas`, `carapace_plating`,
  `draw_copper_piping` (12 copper ore and 2 steel plate, 4 copper piping, 1.6 ticks a run,
  2026-11-17 00:14 UTC). Quoted, not made: `fabricate_circuit_boards`.

### Gas (template `gas-harvest`)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 1.3.

- Fit: a Gas Harvester I in the second utility slot (1,202 cr at Node Beta, section 5).
  Trains mining.
- Steps: the engine's mining loop at a gas cloud for the route's minutes; at the end the
  pilot docks at the route's station, sells into the bids at the route's floors and
  stores the rest of its hold there.
- Opens: the module, an empty hold (beyond the border, rule F13), a bid where named.
- Readings, 2026-11-16 19:16 to 2026-11-17 00:19 UTC: Amberfall 1 run -320 cr in 41.6 min,
  Deepwell haze 2 runs -1,428 in 128.3 min; The Experiment haze 2 runs +3,942 in 111.7 min
  (now Trade's claim). What a small bid does not take stays stored where the ship sold.

### Gathering for the reserve (template `gather-reserve`)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 1.4.

- Fit: the starter mining laser. Trains mining and deep core mining.
- Steps: the engine's mining loop at the field for 45 minutes; the ore goes into the
  pilot's storage at Node Beta. A run ends where its minutes run out, often at the field;
  the loop finishes its sequence (mine, then dock at Node Beta) after the order ends, for
  minutes: `catch.py` waits for the dock (2026-11-17 00:10 to 00:14 UTC).
- Opens: a field's place under its fleet-wide cap; `min_left` closes a field.
- Readings, 2026-11-16 19:16 to 2026-11-17 00:19 UTC: Hamal Crystal Bloom 58 runs -7,575 cr
  in 2,437 min; Spacetime Seep 29 runs -3,305 in 1,093 min; Prism Scatter 20 runs -2,091 in
  840 min. Standing work: its cost is the fuel, about -150 to -190 cr a ship-hour.

### Beyond the border (a test)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 1.5.

- `buy-gold-ironlight-boards`: one ship with an empty hold to Ironlight Crossroads (LHS
  1140, lawless, police 0, six jumps), 3 gold ore at 145 cr or less, booked as money paid
  once (craft inputs, requests.log ENT-172), then `fabricate_gold_circuit_boards` at Node
  Beta from the pilot's own stored copper ore and energy crystal. Written 2026-11-16
  23:58 UTC. First RESULT line: 2026-11-17 00:35 UTC, 3 of 3 stops in 20.6 min, -561 cr (414 of
  it gold booked once), 2 boards made. Out of the plan since 04:05 UTC: the 75 silicon ore Trade
  bought make the next 111 boards for no new spend. Our hunters sold at that station 14 times on 2026-11-16
  without a loss (runs table).

### Missions that pay once (the list First)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 1.6.

- The once line is section 3. From 19:16 to 00:19 UTC haulers were paid 240,938 cr once
  (runs table, column one_time): Mining Missions 60,900, Missions 1 59,548, Substrate
  41,522, Conductive Lattice 29,420, Resonance Finish 26,548, Network Expansion 12,000,
  First Steps Board 9,000, First Hunt 2,000.
- A once route measured on another role's pilots may not open to a hauler: read its runs
  by role before it enters the plan (skill logistics-stock).
- Board missions of Logistics' class (rule F34: deliveries, crafting, station needs), read
  2026-11-17 11:53 to 11:54 UTC (data/missions; the tool candidates, kind mission):
  - Workshop Production Run (Central Nexus and Node Beta): craft_item, "Craft 5 items using any
    recipe", 3,500 cr, 25 crafting XP, 20 Piloting XP; template id `workshop_production_run`.
    `mission-workshop-production-run-node-beta` accepts, smelts 5 plates from the pilot's own iron
    and hands in, all at Node Beta. First RESULT line 2026-11-17 12:41 UTC: 3 of 3 stops in 6.9 minutes,
    +3,448 cr, 3,500 cr paid once; 5 runs and 17,500 cr once in the four hours to 16:05 UTC (view
    route_earnings, every division's pilots). In the hauler plan's list First at 4 ships from 16:00 UTC:
    every hauler that stores 60 iron ore at Node Beta flies it once.
  - Shipyard Supply at Node Beta (Mining Laser I 1,693 cr, Void Nanite Suspension 1,454 cr, Shield
    Emitter 6,377 cr): deliver_item; each carries a station-made mission id
    (`procurement_<hash>_<item>`) and no template id, so the circuit runner's accept step, which looks
    a mission up by template id, cannot take them yet. The goods are bought: a laser at 1,433 cr at
    Node Alpha, 5 nanite at 222 cr at Central Nexus (+246 and +333 cr a run by the route maker's
    reckoning). What opens them: an accept by mission id in route_run.py (a fleet-build of mine).
  - Procyon Station Upgrade: 10 circuit boards delivered to Procyon for 1,960 cr (queue.log ENT-157), about the boards'
    base value of 200 each; boards are reserve (24,925 asked): not flown.
  - The hot-cell and gutter-flux deliveries of Central Nexus are smuggling jobs 20 to 42 jumps away,
    at a loss by the route maker's reckoning: not flown.

### Route Templates
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section 2.

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

The division's templates (2026-11-18 00:12 UTC, `plan.py templates`):

| Template | Routes, in the order a ship tries them | Trains | Ships |
|---|---|---|---|
| `stored-goods` | Trade's three hydrogen and five soma sell and carry routes, its two null matter routes (since 2026-11-18), the palladium sells, then `sell-plasma-node-beta` and the three liquid hydrogen routes | trading, navigation | 40 |
| `gas-harvest` | `mine-achernar-gas-pocket`, `mine-lesath-gas-cloud`, `mine-amberfall-emission-nebula` (clouds that sell at our own stations, since 2026-11-17 08:00 UTC) | mining | 4 (the Gas Harvester I) |
| `craft-reserve` | `craft-steel-logistics-experiment`, `-node-beta`, `-synchrony-hub`, `-central-nexus`, `craft-piping-plate-node-beta` (since 2026-11-18 00:12 UTC; piping is nearly met, plate is short) | crafting, refining | 40 |
| `gather-reserve` | `gather-glasslight-shoal-silicon` (since 2026-11-18 00:12 UTC: the iron and copper fields left it, the reserve's iron is met) | mining | 40 |

Every hauler's cell reads `@stored-goods, @craft-reserve, @gather-reserve`; the four gas
haulers put `@gas-harvest` after the first; the silicon hauler, two mine haulers, three member
haulers (the bunker's supply) and five member haulers (the Center's flex) each put their own route
before all.

### Missions That Pay Once
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/logistics.md section 3.

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
