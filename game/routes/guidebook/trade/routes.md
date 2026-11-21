# Trade guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-21. Evidence: plan.py show; fill.py status trader (20:01 UTC); table books (19:36 to 19:52 UTC).

What the traders fly between two turns: the division's plan file
(`/srv/collective/data/plans/plan-trade.md`, the tool `plan`), as set on
2026-11-21 at 20:00 UTC, the first turn after the pause.

- First, every ship: the once line of 24 routes; for the traders nearly
  all are booked or full (`fill.py status trader`).
- Own routes: `@trade-sell > @trade-craft` for all 40; ahead of them one
  ship each on a test beyond the border (entry `Trade beyond the border`):
  trade-silver-bar-alpha-to-arneb, carry-hydrogen-beta-to-crucible (two
  hydrogen holders, one ship at a time), go-ironlight-trader then
  carry-hydrogen-beta-to-crucible-bulk (the freighter test).
- Then: craft-steel-node-beta, craft-steel-central-nexus,
  craft-steel-synchrony-hub, park.

What it carries: little. After the pause the home bids that paid on
2026-11-17 are gone (null matter and hydrogen 0 at every home station,
soma 2 to 3 units; books of 19:36 to 19:52 UTC), the traders' own iron is
used up (under 100 a pilot) and copper wiring stands far over its max, so
most traders wait docked at no cost and the gate reads HALT.

What opens work: a home bid back (`requires.bid` opens a sell route by
itself), a far bid with depth on a fresh book, a freighter whose load is
worth the road, the Fleet Admiral's word on the trader fallback
(requests.log, 2026-11-21).

### Route Guides
Status: retired. Updated: 2026-11-21. Evidence: merged into `Selling stores where they lie` (refined under the caps, queue.log ENT-189).

How each kind of route of this division is flown: the fit and the
skills it needs, its place, its steps, what opens and closes it. A
credits figure in this section is a dated reading and no verdict: what
a route earns now is in the fleet's database with its age (rule F22;
the tool `routes`, the view `route_earnings`).

### Selling stores where they lie (`sell-<good>-at-<station>`, `carry-<good>-<from>-to-<to>`)
Status: proven. Updated: 2026-11-21. Evidence: the sell and carry route files with their measured figures; sellgen.py of the skill trade-books.

- The starter hull, nothing bought; trains trading. Each ship sells its
  own stores; the routes are open to every division (rule F24).
- Steps: `store: all`, `withdraw` from the pilot's own storage (the
  runner takes only what the bid takes when the same stop sells), `sell`
  at the floor; a carry sells one or two jumps on and stores the rest.
- Gates: `requires.stored` and `requires.bid` (a book read within the
  hour); a route opens again by itself when a docked ship reads the bid
  back.
- Floor: above the cheapest ask of the good in depth elsewhere, set again
  each turn beside `sellgen.py scan` (skill trade-books): soma's deep ask
  fell from 323 to 292 cr overnight and five routes stood closed by their
  own floor (2026-11-17).
- A route whose runs last minutes is judged by credits a run times the
  runs its bid's regain allows (table `stats_refill`), never by its
  per-hour figure.
- A standing sell order (`create_sell_order`, spacemolt_market) costs 1%
  of the listed value at once; one anchor beacon at 1,200 cr stood a day
  unfilled at Node Beta (2026-11-16 to 17).
- Readings: `hive.py route <id>` (sell-null-matter-at-nexus,
  sell-soma-at-node-beta, carry-soma-beta-to-gamma).

### Crafting for sale (`craft-<good>-<station>`)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Making goods from own stores` (refined under the caps, queue.log ENT-189).

- Fit and skills: the starter hull. Trains crafting and trading.
- Steps: at the workshop's station `store: all`, `buy` the bought
  input (one unit a run, with a price limit), the `craft` step
  (recipe, runs, per_run, makes, inputs), then `sell` where the bid
  stands. The craft takes its inputs from the pilot's own storage at
  that station; `requires.stored` sends only a pilot that holds them.
  How the calls work: section 6.
- Reading, 2026-11-16 23:50 UTC: focused crystal from 4 stored energy
  crystal and 1 palladium ore bought at Node Beta, sold at Central
  Nexus: +278 cr in 14.3 minutes; the crafter's crafting XP read 10
  after it.
- Before a craft-for-sale route enters a plan, and every turn: its
  inputs and what it sells must have surplus (`reservecheck.py` of the
  skill trade-books; rule F24). craft-focused-crystal-node-beta made 7
  runs of about +500 cr from 14:23 to 15:04 UTC on 2026-11-17 while the
  reserve held energy crystal back for circuit boards (surplus.py
  reserve, 15:39 UTC); it is off since 15:41 UTC and opens again only
  if the reserve releases the crystals.

### Crafting for the reserve from stores (`craft-piping-<station>`)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Making goods from own stores` (refined under the caps, queue.log ENT-189).

- Fit and skills: the starter hull. Trains crafting and refining.
- Steps: one stop at the station's workshop with two crafts in its
  list: basic_iron_smelting (10 iron ore make 1 steel plate), then
  draw_copper_piping (12 copper ore and 2 steel plate make 4 copper
  piping). The runner makes the first craft's plates into storage
  before the second asks for its inputs, and withdraws what both made
  only after the last craft; a second stop stores it again. A craft
  without its inputs makes nothing and the run goes on.
- Opens and closes: `requires.stored` iron and copper ore at that
  station (a list of two); a pilot is sent again only after the
  ledger read its storage (about 40 minutes).
- Readings, 2026-11-17 11:41 to 11:49 UTC (runs.jsonl): at Node Beta
  60 copper piping from 180 copper and 30 stored plates in 4.8
  minutes, 0 cr (the smelt found no inputs: the pilot's iron had gone
  into Logistics' steel craft after the ledger's read); at Synchrony
  Hub 10 plates and 20 piping in 7.9 minutes, -39 cr of fuel. Piping
  takes about 1.6 ticks a run. Nine runs in the first 15 minutes.

### Making from one's own stores in one visit (`craft-steel-own-<station>`, `craft-wiring-<station>`)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Making goods from own stores` (refined under the caps, queue.log ENT-189).

- Fit and skills: the starter hull. Trains crafting and refining; costs
  one hop of fuel, nothing bought or sold.
- Steps: one stop at the station's workshop whose `craft` list asks the
  same recipe in halving sizes (32, 16, 8, 4, 2, 1 runs; 128 down to 1
  for wiring, 512 down to 1 for the Central Nexus iron). The runner
  quotes each entry; where the pilot's storage cannot fill it, the quote
  says `have_inputs False` and the entry makes nothing ("no inputs" in
  the run's notes), and the next entry is tried. One visit so makes
  exactly what the pilot holds, up to the sum of the list. A second stop
  stores what was taken into the hold.
- Opens and closes: `requires.stored` 100 iron ore or 80 copper ore at
  that station; the pilot is sent again only after the ledger read its
  storage, and by then its stores there are used up.
- Readings, 2026-11-17 23:42 UTC (runs.jsonl, the trader's log): at Node
  Beta 16 and then 4 runs made after 32 and 8 found too little iron, 20
  steel plate in 1.7 minutes, 0 cr; the quotes read 0.23 ticks a smelt
  and 0.26 to 0.28 ticks a wiring run (23:37 to 23:43 UTC). A fixed
  `runs` either fails whole on a store a little short or leaves the rest
  for a visit 40 minutes later.

### Missions that pay once (`voidborn-<mission>`)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Once missions: what they taught` (refined under the caps, queue.log ENT-189).

Section 3. Each starts with the accept at the giver's station and
skips a pilot that booked its reward. Neural Matrix Delivery: the
accept hands out 8 phase matrix, delivered on docking at Sirius
Observatory Station (9 jumps, three of them lawless): 5,000 cr, paid
in both runs (2026-11-16 19:49 UTC and 2026-11-16 23:59 UTC).

### Gas (`mine-<cloud>`)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Route Templates` (refined under the caps, queue.log ENT-189).

- Fit: a Gas Harvester I. Trains mining.
- Sells hydrogen, plasma and argon into the Node Beta and Central
  Nexus bids; one ship a route, since a bid takes a few dozen units
  an hour.
- Readings (route_earnings, 2026-11-16 23:32 UTC, last 12 hours):
  Marfik Emission Nebula +280 per ship-hour over 6 runs, GSC-0016
  Emission Nebula +260 over 6 runs.

### Navigation training (`train-navigation-trader`)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Route Templates` (refined under the caps, queue.log ENT-189).

- The starter hull. Docks at our five stations in a loop; about 4
  navigation XP a jump. `requires.skills_below` navigation 3: it
  closes at navigation 3, where Signal Fragments (7,000 cr once)
  opens.
- Reading, 2026-11-16 19:01 UTC: three loops of 17.6 to 17.9 minutes,
  -165 cr each.

### Fallback gathering (`mine-pherkad-rift`, `gather-hamal-crystal-bloom`, `gather-gsc-0027-prism-scatter`, `mine-acubens`)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Route Templates` (refined under the caps, queue.log ENT-189).

- A mining laser. Iron and copper ore into the pilot's storage for
  the reserve; never judged on its pay (rule F8).
- Reading (route_earnings, 2026-11-16 23:32 UTC, last 4 hours): -169
  to -191 per ship-hour over 57 to 249 runs.

### Buying station stock by hand
Status: retired. Updated: 2026-11-21. Evidence: merged into `Station Inputs Bought (plan step P4)` (refined under the caps, queue.log ENT-189).

- One unit first with `estimate_purchase`, then `buy` sized to the
  smallest of: the units asked, the units at the price, and what the
  wallet pays with 3,000 cr left (rule F7). `buy` fills as far as the
  wallet reaches without refusing (errors.log ENT-067).
- With `deliver_to: storage` the goods go to the buyer's storage; a
  `deposit` with another pilot of ours as `target` moves them into
  that pilot's storage at the same station (75 silicon ore into the
  board crafter's storage, 2026-11-16 23:58 to 2026-11-17 00:01 UTC).
- Book the cost as station stock (`gate.book_onetime`; requests.log
  ENT-172).

### Standing sell orders (`create_sell_order`, spacemolt_market)
Status: retired. Updated: 2026-11-21. Evidence: merged into `Selling stores where they lie` (refined under the caps, queue.log ENT-189).

- `item_id`, `quantity`, `price_each`; the goods are escrowed from the
  hold, then from storage; 1% of the listed value is paid at once.
  One anchor beacon listed at 1,200 cr at Node Beta: fee 12 cr
  (2026-11-16 23:48 UTC). `view_orders` lists a pilot's orders at the
  station where it is docked; undocked it answers `not_docked` but
  still names the count ("0 buy orders and 1 sell orders ... 1 items
  in escrow", 2026-11-17 03:34 UTC). Unfilled after 3 hours 46
  minutes; the Node Beta book showed it as the ask 1,200 x 1 at 03:31
  UTC. No station bids above 2 cr for anchor beacons; The Experiment
  asks 1,400 x 8. At 2026-11-17 07:39 UTC the Node Beta book still
  showed the ask 1,200 x 1, about 7 hours 50 minutes after the listing;
  `view_orders` docked at Synchrony Hub answered "No personal orders at
  Synchrony Hub" with the hint "No active orders on any market" (07:41
  UTC). The two readings disagree; the next reading is docked at Node
  Beta.

### Route Templates
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/trade.json; plan.py templates.

The division's kinds of work are templates in
`game/routes/templates/trade.json`, listed in
`game/routes/templates-trade.md`: `@trade-sell` (stored goods into the
bids where they lie; trading), `@trade-craft` (making from own stores;
crafting, refining), `@trade-train-nav` (navigation to 3 for Signal
Fragments). A ship's row names one as `@<name>`; `plan.py template` and
`plan.py use` change them. `@trade-gas` and `@trade-gather` are gone since
2026-11-18: gathering is the miners' work (rule F23). This guidebook keeps
no list of routes that did not pay (rule F22): what a route earns now is
the view `route_earnings`.

### Missions That Pay Once
Status: retired. Updated: 2026-11-21. Evidence: merged into `Once missions: what they taught` (refined under the caps, queue.log ENT-189).

The `once` routes at the head of the plan: every pilot flies them
first. What a new one pays and what it needs is written here when it
was flown the first time.

| Route | Pays | Measured | Date | Note |
|---|---|---|---|---|
| `voidborn-concurrent` (Concurrent Approval) | 3,000 cr | RESULT: 3/3 stops in 8 min, +2,952 cr (48 cr fuel) | 2026-11-15 | The accept puts the 2 neural soma into the hold: nothing is bought. Once per pilot: the mission left the board after the hand-in |
| Market Participation: Selling (`voidborn-selling`; the trader pilots have it done) | 1,000 cr | Command group RESULT lines: +865 cr each after the ten units bought and sold | 2026-11-15 | Ten units sold into any bid. Since 2026-11-17 11:40 UTC the route buys ten copper wiring at The Experiment (ask 21 x 1,413, bid 2 x 40 at 11:38 UTC) behind `requires.bid` on that bid: liquid nitrogen's ask had risen to 22 cr over the limit of 14 and no station bid for it (requests.log ENT-208, answered ENT-214) |
| `voidborn-precedence` (Precedence) | 4,000 cr and 1 neural soma | 14 traders, 23:35 to 23:58 UTC: +54,483 cr after 1,517 cr of fuel, about 15 minutes each (runs.jsonl) | 2026-11-15 | Three docks at our own stations, nothing bought. In the plan since its first RESULT line (command group, 23:20 UTC) |
| `voidborn-conductive-lattice` (Technician Pale-6's chain at Node Beta: Conductive Lattice, Resonance Substrate, Final Calibration) | 5,500 + 7,000 + 8,000 cr; trading XP 45 + 30 + 25 | Flown by hand by one trader, 2026-11-15 23:33 to 2026-11-16 00:12 UTC, one mission after the other: Lattice +2,312 cr (20 silver ore bought at Ironlight Crossroads, LHS 1140, for 3,040 cr; 148 cr fuel; 21.5 min); Resonance +589 cr (15 energy crystal bought at Central Nexus for 6,363 cr with the tax; 8 min); Final Calibration +7,946 cr (the accept hands out the 5 circuit boards; 7 min). +10,847 cr once per pilot in about 37 minutes | 2026-11-16 | Each mission appeared on the Node Beta board right after the one before was handed in, and left it after its own hand-in. Lattice and Resonance hand out nothing; Final Calibration hands out its goods. Silver ore is on offer in none of our six books: the first link needs a ship beyond the border, hold empty on the way out (orders F13); hull 75 of 75 throughout. By 00:53 UTC ten traders had flown all three: six by the route in one run each, +10,893 cr in 31.5 to 32.4 minutes; three in two runs (Lattice +2,290 to +2,334 cr, then the rest +8,559); one by hand (runs.jsonl). The silver ask stood whole at 152 x 200 in every read (23:21, 00:05, 01:24 and 01:39 UTC) after 20 units were bought about 23:40 and 120 about 00:30 UTC: it regains at least 120 units within about an hour, so it carries at least 34 pilots in four hours. The energy crystal ask at Central Nexus, 420 x 697 (03:12 UTC), carries 46. `max_pilots` 30 and `max_ships` 6 (a wave buys 120 of the 200) since 2026-11-16 03:09 UTC; open to every division's plan. The fleet's own energy crystals would make Resonance +7,000 instead of +589. Since 01:09 UTC the circuit runner crashes at the silver buy of every run (errors.log ENT-039): the accept step overwrites the name of the function the buy calls; no run row is written, and the pilot waits docked at Ironlight holding Conductive Lattice. The ten traders that had not flown it flew it by hand, 04:40 to 05:16 UTC, in split runs that buy before they accept (Ironlight buy and Node Beta hand-in; Central Nexus buy, Node Beta, Node Gamma): +109,213 cr in 24 runs and 4.6 ship-hours, 110,970 paid once; +10,942 cr for a pilot that already held the mission, +10,893 for one that took it at Node Beta. All 20 traders have it now. The runner was fixed at 04:49 UTC (requests.log ENT-098); from 05:00 UTC the route flies for every division, `max_ships` 10 and `max_pilots` 146: 64 runs from 04:40 to 07:25 UTC and ten more from 08:10 UTC; every run of other divisions from 05:05 to 07:25 UTC flew the whole chain, +10,816 to +10,893 cr in 31 to 37 minutes, none short of silver (data/routes/runs.jsonl). The ten of 08:10 UTC bought 200 silver at Ironlight between 08:19 and 08:28 UTC, the ask reading 80 left at 08:27 UTC: a wave of ten takes the whole ask of 200; how fast it stands whole again is not measured (the ledger saved no move of it after 01:24 UTC). About 86 pilots of the fleet had not done Resonance Substrate at 08:31 UTC (the tool fleet, view=capacity) 2026-11-17 19:41 UTC: the route stood still from 2026-11-16 23:25 UTC on `max_pilots` 146 (147 pilots had booked Conductive Lattice) while the fleet grew to 246; 99 pilots, 17 of them traders, had not flown it, and the Node Beta board offered it to both newer traders read (boards.py, 19:42 UTC). max_pilots 246 and the silver limit 160 -> 175 (Ironlight asked 170 x 200 at 18:56 UTC; the runner checks the ask with 1% against the limit); four pilots of four divisions took it at 19:43 UTC. A cap sized to the fleet of its day is read again when the fleet grows |
| `voidborn-signal-fragments` (Signal Fragments, Researcher Null-Seven at Central Nexus) | 7,000 cr; exploration XP 60 | RESULT by hand: accepted at Central Nexus, Node Beta and Node Gamma recorded on docking, handed in at Central Nexus, +6,909 cr after 91 cr of fuel in 14.3 minutes | 2026-11-16 | Nothing handed out, nothing bought. Not offered to every pilot: the next six traders that flew it found it missing from the board ("not offered", -26 to -39 cr each, -221 cr in all, 05:07 to 05:18 UTC), and another pilot's board at 05:04 UTC lacked it. The condition is navigation 3: the Central Nexus board, read for each of 30 docked pilots at about 05:28 UTC, offered it to 4 of 4 with navigation 3 and to 0 of 25 with navigation 2, whatever their piloting or exploration. 46 pilots of the fleet have navigation 3 or more (05:31 UTC), two of them traders. The second trader with navigation 3, flown by hand from 05:52 UTC, was offered it: +6,883 cr in 18 minutes (06:09 UTC). Out of the plan at 05:13 UTC; since 07:00 UTC the route asks `requires.skills` navigation 3 (requests.log ENT-110), and it heads the trader plan again since 08:32 UTC with `max_ships` 10 (requests.log ENT-118, answered ENT-121): 12 runs of the fleet from 06:43 to 08:10 UTC paid +6,792 to +6,909 cr each in 14.3 to 26.1 minutes, none refused; 56 pilots with navigation 3 had not flown it at 08:27 UTC (Intel's count). Its next link, The Crimson Resonance (8,500 cr), docks at The Rampart Checkpoint and delivers 5 titanium alloy at Blood Forge, Crimson space 17 to 20 jumps out: not flown |
| `voidborn-first-steps-board` (First Steps in the Void taken from the Central Nexus board) | 1,000 cr; voidborn mastery XP 15 | RESULT by hand: accepted at Central Nexus, 15 carbon ore mined at Acubens Belt in about 5 minutes, handed in at Central Nexus, +922 cr after fuel in 12 minutes | 2026-11-16 | The board offers it to every pilot that has not done it; `voidborn-first-steps` serves only a pilot that already holds it and counts any other pilot's run as done, so 87 pilots of the fleet never took it (data/fleet/onetime.json, 08:46 UTC). It opens Network Expansion. Acubens Belt read 76 carbon ore at 08:12 and 182 at 08:46 UTC with the test mining 15 there: `max_ships` 3. Since 08:59 UTC in the trader plan |
| `voidborn-network-expansion` (Network Expansion, the link after First Steps) | 1,500 cr; voidborn mastery XP 25 | RESULT by hand: accepted at Central Nexus, the visit counted on docking at Node Alpha, handed in at Central Nexus, +1,450 cr after fuel in 8 minutes; four more traders by the route, +1,450 cr each in 8 minutes | 2026-11-16 | Offered (boards read at 08:34 UTC) to the 6 of 8 traders docked at Central Nexus with First Steps done, to neither of the two without it: the route asks `requires.booked` First Steps in the Void. 59 pilots of the fleet could fly it at 08:46 UTC, about 88,000 cr once; `max_ships` 20 (docks at our own stations); offered to every Admiral (queue.log ENT-091). Its next link: The Collective Provides |
| `voidborn-collective-provides` (The Collective Provides, the link after Network Expansion) | 2,500 cr; voidborn mastery XP | RESULT by hand: hold stored at Central Nexus, accepted, 20 nickel ore mined at GSC-0049 Platinum-Group Reef (lawless, 5 jumps), handed in at Central Nexus, +2,188 cr after fuel in 48 minutes | 2026-11-16 | No home field holds nickel; the reef read 192 at 07:47 UTC. Its mix (nickel, platinum, rhodium, osmium, iridium) filled the hold with 14 nickel among 58 units, so the run went home to storage and back: two trips. The other ores have no bid above 2 cr at our stations (books of 09:05 UTC): stored. `requires.booked` Network Expansion, `max_ships` 2. Its hand-in opens eight missions of the same line (section 7). Off from 2026-11-16 12:34 UTC (the reef read 0 nickel); on again 2026-11-17 11:40 UTC as a one-ship test at Rotanev Daylight Seam (424 nickel and nothing else, 10 jumps by a road with no pirate on our record); not Gliese 876 Belt, where a pirate stood at 05:13 UTC, nor Jadecove, whose road crosses Gliese 876 (orders D9). A scout's plan took the test at 11:44 UTC. Seven runs of the fleet from 11:40 to 14:30 UTC paid 2,500 cr each in 30.5 to 35.2 minutes (the tool route); Rotanev read 1,452 nickel at 14:03 UTC: max_ships 6 since 2026-11-17 15:36 UTC 2026-11-17 19:50 UTC: 37 of 38 runs since 14:03 UTC paid (2,500 cr each, 35 hand-ins of the fleet from 15:56 to 19:40 UTC); Rotanev not read since 14:03 UTC, so max_ships 6 -> 4 and `min_left` 60 nickel on the mine step: a run on an emptied seam goes all the way round and counts as done for its pilot (dispatch.py done_once; Mining's Markab runs, errors.log ENT-096) |
| `voidborn-signal-protocol` (The Signal Protocol, after The Collective Provides) | 3,500 cr; voidborn mastery XP 25 | RESULT by hand: accepted at Central Nexus, the arrays recalibrated on docking at Node Beta and Node Gamma, handed in at Central Nexus, +3,409 cr after fuel in 14 minutes | 2026-11-16 | Nothing carried, nothing bought. `requires.booked` The Collective Provides, `max_ships` 20; offered to every Admiral (queue.log ENT-096) |
| `voidborn-first-steps` (First Steps in the Void, for a pilot that holds it) | 1,000 cr | Logistics' route: 26 runs of the fleet, 810 cr a run in about 10 minutes (route file, measured) | 2026-11-16 | Six traders hold the mission (get_active_missions, 05:02 UTC): in the trader plan since 05:07 UTC, 2 ships at a time across all plans; Acubens Belt carbon ore bounds it (97 units at 04:46 UTC, 15 a pilot) |
| `voidborn-hardware-cargo` (Hardware Optimization: Cargo, after The Collective Provides) | 1,500 cr; voidborn mastery XP 15 | By hand 2026-11-16 12:41 to 12:43 UTC: accepted at Central Nexus, one Cargo Expander I bought there after the accept (1,056 cr, 1,066 with the tax), the objective read 1 of 1 at once, handed in: +434 cr; fitted, the hold went from 65 to 85 | 2026-11-16 | The route buys at Synchrony Hub (7 at 352 cr, book of 12:40 UTC; limit 420): about +1,050 cr after fuel. One ship until its first RESULT line; the dispatcher gave it to the other tester at once Since 2026-11-16 18:34 UTC (commit 1c2800c, requests.log ENT-149) both module routes buy the module into the hold and never fit it before the hand-in: the objective counts a module in the hold (four hauler runs that fitted it read 0 of 1, -4,216 cr, errors.log ENT-058) |
| `voidborn-atmospheric-extraction` (Atmospheric Extraction: Setup, after The Collective Provides) | 2,000 cr; voidborn mastery XP 15 | By hand 2026-11-16 12:41 to 12:43 UTC: accepted, one Gas Harvester I bought at Central Nexus after the accept (1,554 cr, 1,569 with the tax; 1 at that price), 1 of 1 at once, handed in: +431 cr and a fitted harvester | 2026-11-16 | A harvester owned before the accept did not count (09:32 UTC); bought after it, it counts. The route buys at Node Beta (14 at 1,202 cr; limit 1,300) and skips a pilot that carries one |
| `voidborn-resonance-finish` (Resonance Substrate and Final Calibration for a pilot the chain left after Conductive Lattice) | 7,000 + 8,000 cr | Not flown yet. From 11:11 UTC six chain runs read 'energy_crystal: not bought; final_calibration not offered' when the Central Nexus crystal ask left 420 cr (3,500 at 11:35, 420 x 65 at 11:52, 420 x 43 at 12:48 UTC); the chain skips a pilot with its first link booked. 11 pilots, all miners, stood so at 12:49 UTC (data/fleet/onetime.json) | 2026-11-16 | Written 12:49 UTC, max_ships 2; the chain's max_ships 10 -> 4 on the crystal ask. A run without crystals ends 'not offered': no try, it rests an hour (requires.booked) |
| The Crimson Resonance (the link after Signal Fragments, 8,500 cr) | -- | One accept with an empty hold, 2026-11-16 12:36 UTC: the hold stayed empty, no titanium alloy handed out | 2026-11-16 | Not flown (orders ENT-014): 5 titanium alloy would be bought (about 6,500 cr) for 8,500 cr at 34 jumps. The trader holds the mission |
| `voidborn-neural-matrix-board` (Neural Matrix Delivery, Central Nexus board; deliver 8 phase matrix to Sirius Observatory Station, Solarian, 9 jumps) | 5,000 cr; navigation 25, trading 40 XP | Two runs, 5,000 cr each: the test route 2026-11-16 19:49 UTC (4 of 4 stops in 27.5 minutes) and the board route 2026-11-16, accepted 23:47 and handed in 23:59 UTC | 2026-11-16 | The accept with an empty hold put the 8 phase matrix (size 2) into the hold (12:36 UTC); nothing is bought. The road crosses three lawless systems (GSC-0041, Antares, Homam; `scripts/map.py route`). The first run's wallet fell 19,390 cr beyond the reward, which no step of the route explains: read as a gift of the wallet guard in the hour it gave without a record (errors.log ENT-064), not proven. A once route with the accept at its first stop since 2026-11-16 23:44 UTC, one ship at a time |

### Making goods from own stores
Status: proven. Updated: 2026-11-21. Evidence: craft-steel-own-node-beta, craft-wiring-synchrony-hub, craft-piping-node-beta (route files, runs.jsonl 2026-11-17).

Routes `craft-steel-own-<station>`, `craft-wiring-<station>`,
`craft-piping-<station>`: the starter hull, one hop of fuel, nothing
bought; they train crafting and refining.

- One stop at the workshop; its `craft` list asks one recipe in halving
  sizes (32, 16, 8, 4, 2, 1 runs). An entry the pilot's storage cannot
  fill makes nothing (`have_inputs` False) and the next is tried, so one
  visit makes exactly what the pilot holds. Two crafts in one list chain
  (a smelt, then piping): the runner withdraws only after the last.
- Gate: `requires.stored` the input at that station; a pilot goes again
  only after the ledger read its storage (about 40 minutes).
- Read: 20 steel plates in 1.7 minutes for 0 cr (craft-steel-own-node-beta,
  2026-11-17 23:42 UTC); a smelt about 0.23 ticks, a wiring run 0.26 to
  0.28.
- For sale only when every input and the output have surplus
  (`reservecheck.py`, rule F24): focused crystal made from held-back
  energy crystal was sold once (errors.log ENT-090).
- The pull rule closes a craft whose output stands at its max: copper
  wiring 10,732 of 96 on 2026-11-21 (`fill.py status trader`).
- The calls behind a craft step: lessons.md, `Crafting by Hand: the Calls`.

### Trade beyond the border
Status: test. Updated: 2026-11-21. Evidence: table books 2026-11-21; scripts/map.py route; data/intel/sightings.jsonl; route files of the four tests.

Home bids are thin and come back slowly; the far books hold the depth
(table `books`, 2026-11-21 19:36 to 19:52 UTC): The Obsidian Well, a
player station at Arneb (16 jumps, lawless), bids silver bar 501 x 44,527
and silver ore 101 x 502,177; The Crucible Garrison (Crimson, 18 jumps)
bids hydrogen 37 x 184 and heat sink 193 x 24.

- Tests, one ship each, from 2026-11-21 20:00 UTC:
  trade-silver-bar-alpha-to-arneb (Node Alpha asks 50 at 414),
  carry-hydrogen-beta-to-crucible (41 of our own hydrogen and 24 heat
  sinks bought at Node Beta at 147 in a hold of 65), go-ironlight-trader
  then carry-hydrogen-beta-to-crucible-bulk (a Prayer freighter of 540).
- The road: past Pherkad every system to Arneb or The Crucible is
  lawless; no pirate on our record in any of them
  (`scripts/map.py route`, data/intel/sightings.jsonl). Each test leaves
  home with an empty hold or our own goods, carries price limits at both
  ends, and stores at the far station what its bid left.
- A far book read days ago is a guess, not a price: most foreign books in
  the routemaker's trade candidates date from 2026-11-17; a ship that
  docks reads the book again.
- Each test answers: what the far bid takes and regains, what the road
  costs, whether Node Alpha's silver bar ask comes back.

### Once missions: what they taught
Status: proven. Updated: 2026-11-21. Evidence: data/fleet/onetime.json; the voidborn-* and mission-* route files; errors.log ENT-039, ENT-058, ENT-096.

The `once` routes head every plan's list First; a pilot flies each one
time and a route skips a pilot that booked its reward
(data/fleet/onetime.json; `oncecheck.py`, `boards.py` of the skill
trade-books). What they taught:

- A board mission is accepted at the route's first stop: a route without
  the accept serves only pilots that hold the mission and counts every
  other pilot as done (voidborn-first-steps, 2026-11-16).
- One accept with an empty hold decides whether a delivery hands out its
  goods: Concurrent Approval, Final Calibration and Neural Matrix Delivery
  do; Conductive Lattice, Resonance Substrate and The Crimson Resonance do
  not.
- An acquire-module mission counts a module bought after the accept and
  carried in the hold; one owned before does not.
- A board is one pilot's: Signal Fragments is offered from navigation 3
  (`requires.skills`).
- A chain is sized on its scarcest input and gets a finisher
  (voidborn-resonance-finish, `requires.booked` its first link).
- A mining mission is bounded by one shared field: read its census and
  set `min_left` (voidborn-collective-provides).

What each title paid: its route's note and `hive.py route <id>`.
