---
name: guidebook-trade
id: 20261115T205804Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# trade.md -- Guidebook of the Trade Division

Kept by Mercury; read by every member. What the Trade division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Mercury writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is the division's plan file
  (`/srv/collective/data/plans/plan-trade.md`); every route with its
  figure is in `game/routes/master-index.md` and its sub-indexes.

## Class Card

The trader's class in short (rule F14); the detail is in section 4
(levelling) and section 5 (ships and fits). Sources: the catalog's
tables `skills` and `hulls` (catalog 0.723.2), the game's page
https://www.spacemolt.com/docs/skills.md (read 2026-11-17 07:37 UTC),
the trader ship files (`xpsnap.py`, 2026-11-17 19:43 UTC).

### Ships

- Tier 0, every trader now: Threshold, cargo 65, fuel 95, hull 75, a
  mining laser and a pulse laser. Three carry a Gas Harvester I, one a
  Cargo Expander I (hold 85).
- Tier 1 (no Piloting asked): no Voidborn freighter; the largest hold
  is the Residuum's 100 (a salvager). Not worth a change for trade.
- Tier 2, Piloting 10: Apophenia, freighter, cargo 240, fuel 300, hull
  140: the trader's next hull. Tier 3, Piloting 20: Fold Hauler, cargo
  635. No price is in the catalog; not read at a shipyard yet.
- Fit: a Cargo Expander I (+20 hold) for carries; no weapon is needed.
  Default stance flee (game 0.721.0), set by script.
- Style: dock to dock. Sell each pilot's stores where a bid stands,
  carry one or two jumps, craft at a station workshop; never fight.

### Skills

| Skill | Why it matters | What trains it, on which routes | Trade now | Next goal |
|---|---|---|---|---|
| Trading | The class skill. A higher level shows more in `analyze_market` (regional demand, price trends, arbitrage: the game's help); its bonus is not stated in the catalog | Buying and selling at stations or by exchange orders, XP by credit volume (catalog): `@trade-sell`, station stock bought (about 1 XP per 100 cr), mission rewards | 3 for 3, 2 for 21, 1 for 16 | 3 for every trader |
| Crafting | Station workshop speed from x1 at level 0 to x5 at 100 (with Refining); recipes ask it | Crafting at a station: `@trade-craft` (copper piping and steel plate from the pilot's own iron and copper ore, Logistics' steel crafts) | 5 for 1, 4 for 14, 3 for 23, 2 for 2 | 5 for every trader |
| Refining | With Crafting, the workshop's speed; smelting asks it | The smelt inside craft-piping and craft-steel | 5 for 1, 4 for 6, 3 for 11, 2 for 21, 1 for 1 | 3 for every trader |
| Navigation | Fuel, jump fuel and jump time -1% a level; level 3 opens Signal Fragments (7,000 cr once) | Every jump | 6 for 2, 5 for 1, 4 for 37 | 5 |
| Piloting | Tier 2 hulls at 10 (the Apophenia freighter), tier 3 at 20 | Flying, jumping, mining | 8 for 15, 7 for 5, 6 for 20 | 10 |
| Engineering | Module power and CPU, for a fuller fit | Crafting components or modules | 0 | not a goal yet |
| Mining | The fallback only (rule F23) | `@trade-gas`, `@trade-gather` | -- | -- |

Levels: the trader ship files, 2026-11-17 19:43 UTC (`xpsnap.py save`). XP of the 40 traders
(`xpsnap.py diff`, skill trade-books), four hours each: to 07:37 UTC
crafting 0 and trading 616; 07:37 to 11:41 UTC crafting 3,490, trading
455; 11:41 to 15:37 UTC crafting 10,775, trading 527; 15:37 to 19:43 UTC
deep core mining 34,542, mining 32,581, piloting 32,136, crafting 15,630,
navigation 11,557, refining 8,500, trading 379. Every trader gained XP in
each window; crafting stands at 2 or more for all 40 (3 or more for 38).
Trading is the skill that lags: it rises only by credit volume, and the
bids carry few ships.

## Standing Plan

What the traders fly between two turns: the division's plan file
(`/srv/collective/data/plans/plan-trade.md`, the tool `plan`), as set
in the turn of 2026-11-17 19:52 UTC. `game/routes/plan-trader.md`
prints it without names, and `game/routes/templates-trade.md` lists the
templates. Every trader's own routes are templates (section 2): a ship
is moved to other work with one word. A figure is credits per ship-hour
from the view `route_earnings` (4 hours to 19:33 UTC unless named); a
mission that pays once is judged with its reward (rule F19).

| Order | Work | Ships | Carries | Expected | Why it stands here |
|---|---|---|---|---|---|
| First | The once line: 23 routes from voidborn-first-steps-board to mission-workshop-production-run-node-beta. voidborn-conductive-lattice (Node Beta chain, 20,500 cr over three links) open to all 246 pilots since 19:41 UTC (was 146), 4 at a time; The Collective Provides 6 -> 4 at a time with a nickel floor of 60 | every ship, by the list First | Lattice: 99 pilots of the fleet unflown (data/fleet/onetime.json, 19:40 UTC); silver 170 x 200 at Ironlight Crossroads (18:56 UTC), energy crystal 420 x 1,186 at Central Nexus (19:37 UTC). Rotanev: 1,452 nickel at 14:03 UTC less about 740 taken by 37 paid runs since | Lattice about 10,400 cr a pilot after silver, crystals and fuel (2026-11-16 runs, 34 minutes); The Collective Provides 2,500 cr once in 30 to 35 minutes; Workshop Production Run 3,500 cr once (124 runs of the fleet since 15:56 UTC) | Rules F34, F35: every pilot flies its empire's chains to their end |
| 1 | `@trade-sell`, 14 routes: null matter first (two one-ship tests from Node Beta and Central Nexus stores, floor 200, beside Mining's Synchrony carry), then soma (floor 320), palladium (270), hydrogen (30) | every trader whose own storage holds the good, one ship a test, one or two a paying route | null matter: Central Nexus bid 200 to 210 for 7 to 295 units six times from 17:56 to 19:38 UTC; soma 342 to 343 x 5 to 17 at four stations; hydrogen: no home bid at 19:33 UTC | Mining's null matter carry +17,050 cr in 4 runs since 15:56 UTC; soma Node Beta 8,924 (12 runs), Synchrony 7,978 (11); hydrogen Node Beta 90,659 (5 runs of minutes): judged by credits a run times the runs a bid's regain allows | Traders store 2,141 null matter; the soma and hydrogen bids are thin and come back |
| 2 | `@trade-gas`: five gas routes | the three traders with a Gas Harvester I | no home hydrogen bid at 19:33 UTC | not measured in 4 hours | The gas ships' own work |
| 3 | `@trade-craft`: craft-piping-node-beta, craft-piping-synchrony-hub, craft-wiring-synchrony-hub (a one-ship test: copper wiring from surplus copper, nothing sold), Logistics' three craft-steel routes | a trader whose own storage holds the inputs | copper piping 328 short, steel plate 2,381 short (the tool stock, view=reserve, 19:32 UTC) | craft-piping-node-beta -167 (101 runs of all divisions), craft-steel-node-beta -343 (15): fuel only | Crafting is the class skill (rules F23, F30) |
| 4 | `@trade-gather`: gather-okab-belt (42, the Fleet Admiral's lift of 18:00 UTC, kept), gather-gj-3470-dewfall-fray (13), then the home fields | every trader as fallback | Okab Belt 88,829 iron and 88,262 copper (census about 18:15 UTC) | Okab -397 (102 runs), Dewfall -327 (36) | Standing work while the reserve is short 23,809 iron; copper ore is 447,390 held against 22,892 taken, so what Okab brings past the iron is no use (requests.log ENT-247) |
| Then | gather-hamal-crystal-bloom, gather-gsc-0027-prism-scatter, gather-ironhollow-echo-ejecta, gather-schedar-belt, the three craft-steel routes, mine-pherkad-rift, census-frontier, park | every ship | -- | -- | `park` should never be reached |

Trade's steady money (`hive.py briefing`, SUM trader): -9,988 cr an hour
over the 4 hours to 19:31 UTC; fill gate PASS at 19:44 UTC, 40 of 40 at
work. The loss is the fuel of the gather fields; the once-money of the
same 4 hours was 92,000 cr to traders.

What changes it: the iron the reserve still lacks (the tool stock,
view=reserve), and the Fleet Admiral's answer to requests.log ENT-247 on
the fallback once it is full; the first RESULT lines of the null matter
tests and of craft-wiring-synchrony-hub; the silver and crystal asks
that bound the Node Beta chain; a fresh census of Rotanev Daylight Seam.

## 1. Route Guides

How each kind of route of this division is flown: the fit and the
skills it needs, its place, its steps, what opens and closes it. A
credits figure in this section is a dated reading and no verdict: what
a route earns now is in the fleet's database with its age (rule F22;
the tool `routes`, the view `route_earnings`).

### Selling stores where they lie (`sell-<good>-at-<station>`, `carry-<good>-<from>-to-<to>`)

- Fit and skills: the starter hull, no module. Trains trading.
- Steps: at the station, `store: all`, then the `withdraw` step takes
  from the pilot's own storage only what the bid takes at its best
  price, then `sell` at the floor; a carry withdraws a few units,
  sells them one or two jumps on and stores what the bid left.
- Opens and closes: `requires.stored` (the pilot's own storage holds
  the good) and `requires.bid` (a book read within the hour shows the
  bid at the floor). Each ship sells its own stores; the routes are
  open to every division's ships (rule F24).
- Floor: above the best ask of the same good in depth elsewhere. Soma:
  370 cr, against 323 asked at Central Nexus in depth.
- Readings, 2026-11-16 23:49 to 2026-11-17 00:01 UTC (runs.jsonl):
  soma at Synchrony Hub +1,828 cr in 6.7 minutes, at Node Beta +321
  and +714, carried to Node Alpha +666 in 7.9 minutes; three later
  runs found the bid taken and cost -24 to -36 cr of fuel. Over the 12
  hours to 2026-11-17 03:32 UTC (route_earnings): Synchrony 6,247 per
  ship-hour over 8 runs, the carry to Node Alpha 9,178 over 7, Node
  Beta 2,735 over 6, the carry to Node Gamma 2,812 over 2.
- How a route is written: `sellgen.py scan` (the trade-books skill)
  lists every good we store above the reserve with the bid where it
  lies, the best bid elsewhere, the cheapest ask and the routes that
  sell it already; `sellgen.py sell` and `sellgen.py carry` write the
  route from the book and the storage book, with the readings in its
  note; the floor is set by hand above the cheapest ask in depth.
  Hydrogen gas (2026-11-17 03:39 UTC): floor 30 against Ironlight's
  ask of 6 for about 1.1 million; gas is size 2, so a carry takes 32.
- Null matter (2026-11-17 19:41 UTC): floor 200. Central Nexus is the one
  station of our 40 books that bids for it, 200 to 210 cr for 7 to 295
  units, six readings from 17:56 to 19:38 UTC, gone at 19:40 and back
  within minutes; it asks 213 to 220 itself, so the floor sits in the
  spread, not under the market. The catalog's base value is 450 and no
  book bids near it; processed null matter (910) needs a facility we do
  not own. Size 2: a carry takes 32. Mining's Synchrony carry made
  +17,050 cr in 4 runs from 15:56 to 19:33 UTC (runs.jsonl).
- Before a mine test the filler offers is let in, read what it sells
  into: on 2026-11-17 eight mine tests (Stillwork, Gaugewatch, GSC-0033,
  Deepwell, Sootfall and more) rested on that same null matter bid of 10
  to 16 units at its best price while the fleet stored 6,193 null matter.

### Crafting for sale (`craft-<good>-<station>`)

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

### Missions that pay once (`voidborn-<mission>`)

Section 3. Each starts with the accept at the giver's station and
skips a pilot that booked its reward. Neural Matrix Delivery: the
accept hands out 8 phase matrix, delivered on docking at Sirius
Observatory Station (9 jumps, three of them lawless): 5,000 cr, paid
in both runs (2026-11-16 19:49 UTC and 2026-11-16 23:59 UTC).

### Gas (`mine-<cloud>`)

- Fit: a Gas Harvester I. Trains mining.
- Sells hydrogen, plasma and argon into the Node Beta and Central
  Nexus bids; one ship a route, since a bid takes a few dozen units
  an hour.
- Readings (route_earnings, 2026-11-16 23:32 UTC, last 12 hours):
  Marfik Emission Nebula +280 per ship-hour over 6 runs, GSC-0016
  Emission Nebula +260 over 6 runs.

### Navigation training (`train-navigation-trader`)

- The starter hull. Docks at our five stations in a loop; about 4
  navigation XP a jump. `requires.skills_below` navigation 3: it
  closes at navigation 3, where Signal Fragments (7,000 cr once)
  opens.
- Reading, 2026-11-16 19:01 UTC: three loops of 17.6 to 17.9 minutes,
  -165 cr each.

### Fallback gathering (`mine-pherkad-rift`, `gather-hamal-crystal-bloom`, `gather-gsc-0027-prism-scatter`, `mine-acubens`)

- A mining laser. Iron and copper ore into the pilot's storage for
  the reserve; never judged on its pay (rule F8).
- Reading (route_earnings, 2026-11-16 23:32 UTC, last 4 hours): -169
  to -191 per ship-hour over 57 to 249 runs.

### Buying station stock by hand

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

## 2. Route Templates

A kind of work is a named list of routes: a template. The templates of
this division are kept in `game/routes/templates/trade.json` and listed
in `game/routes/templates-trade.md`. A ship's row in the plan file
names a template as `@<name>`, alone or beside routes of its own, and a
ship is switched to other work with one word.

| Template | Routes, in the order a ship tries them | Trains | Fit |
|---|---|---|---|
| `@trade-sell` | sell-soma-at-synchrony, carry-soma-synchrony-to-alpha, sell-soma-at-node-beta, carry-soma-beta-to-gamma, sell-soma-at-experiment, carry-palladium-nexus-to-gamma, sell-palladium-at-node-gamma, sell-hydrogen-at-node-beta, sell-hydrogen-at-node-gamma, sell-hydrogen-at-synchrony, carry-hydrogen-synchrony-to-experiment | trading | none |
| `@trade-craft` | craft-piping-node-beta, craft-piping-synchrony-hub, craft-steel-central-nexus, craft-steel-synchrony-hub, craft-steel-node-beta | crafting, refining | none |
| `@trade-train-nav` | train-navigation-trader | navigation, piloting | none |
| `@trade-gas` | mine-marfik-emission-nebula, mine-gsc-0016-emission-nebula, mine-the-experiment-haze, mine-coldwater-emission-nebula, mine-stellar-siphon, mine-the-experiment-haze-synchrony | mining | Gas Harvester I |
| `@trade-gather` | gather-okab-belt, gather-gj-3470-dewfall-fray, gather-hamal-crystal-bloom, gather-gsc-0027-prism-scatter, gather-ironhollow-echo-ejecta, mine-acubens | mining | mining laser |

The rows of the plan, 2026-11-16 23:47 UTC: the three traders with a
Gas Harvester I fly `@trade-sell > @trade-craft > @trade-gas >
@trade-gather`; the seventeen other traders at navigation 3 or more
`@trade-sell > @trade-craft > @trade-gather`; the twenty at navigation
2 `@trade-sell > @trade-craft > @trade-train-nav > @trade-gather`.

| Task | How |
|---|---|
| See the templates and how many ships use each | the tool `plan` with `action=templates` (`plan.py templates`) |
| Make or change one | `plan.py template <name> <routes with commas> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py use <ships> <name>`, or `plan.py set <ships> @a,@b` for several |
| Take one away | `plan.py template <name> none`, once no ship names it |

This guidebook keeps no list of routes that did not pay (Suggi,
2026-11-16; rule F22). What a route earns now, with the age of the
figure, is asked each turn: the tool `routes`, or `SELECT * FROM
route_earnings` through the tool `sql`.

## 3. Missions That Pay Once

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

## 4. Levelling Guide

Which skills a ship of this division levels and on which work (rule
F23): the work of its own role first, gathering ore only when none is
open. The levels below are the traders' at 2026-11-17 03:40 UTC (the
table `ship_skills`): trading 2 for 24 ships, 1 for 16; navigation 5
for 1, 4 for 3, 3 for 35, 2 for 1; piloting 7 for 3, 6 for 17, 4 for
19, 3 for 1; crafting 0 for all, 8 of them with XP. The XP of all 40
traders by skill: deep core mining 29,522, piloting 24,111, mining
16,363, navigation 10,687, exploration 4,970, trading 2,753, crafting
120: the standing work trains more than the trade does. At 00:07 UTC
the same table read navigation 2 for 20 traders and crafting XP for 3.

| Kind of ship | Skills it levels | On which work (template) | What the next level opens |
|---|---|---|---|
| A trader born 2026-11-16 evening (navigation 2, trading 0 to 1, piloting 2 to 3) | navigation, then trading | `@trade-train-nav` until navigation 3, `@trade-sell` and `@trade-craft` whenever its own stores and a bid allow | Navigation 3 opens Signal Fragments, 7,000 cr once |
| A trader of the first twenty (navigation 3 to 4, trading 2, piloting 5 to 7) | trading, crafting | `@trade-sell`, `@trade-craft` | Piloting 10 opens the tier-2 hulls; no route trains it faster than flying does |
| A trader with a Gas Harvester I | mining, trading | `@trade-gas`, then the two above | -- |

What raises each skill, as read:

- Trading: a buy gives about 1 XP per 100 cr (24,441 iron ore bought
  for 24,441 cr gave 244 XP, 2026-11-16 18:46 UTC); the 75 silicon ore
  bought for 31,814 cr took its buyer from trading 1 to 2 (159 XP into
  level 2 at 00:07 UTC). Mission rewards give it too: the Node Beta
  chain gives 45 + 30 + 25 (section 3). What a market sale gives is
  not measured.
- Crafting: one hand craft of a focused crystal gave 10 XP
  (2026-11-16 23:50 UTC). A craft's speed grows with the skill and it
  runs only while the pilot stays docked at the workshop (the game's
  `craft` help, 2026-11-15).
- Navigation: about 4 XP a jump on the training loop; level 3 at 340
  XP. The six born traders read at 23:40 UTC stood at 144 to 241 XP.
- Piloting 10, which opens the tier-2 hulls, was about 116 hours away
  at the division's median of 109 piloting XP an hour (`hive.py
  levels`, 2026-11-16 03:25 UTC).

## 5. Ships and Fits

Every trader flies the starter Threshold (cargo 65, fuel 95, hull 75)
with a mining laser and a pulse laser. Since 2026-11-16 12:43 UTC one
more trader carries a Gas Harvester I and one a Cargo Expander I (hold
85), each bought for a mission that paid more than the module
(section 3); a Cargo Expander I asks 352 cr at Synchrony Hub and 173
cr at Ironlight Crossroads (books of 12:39 to 12:40 UTC). Two traders carry a Gas
Harvester I since 2026-11-16 03:12 UTC: bought and fitted at Node Beta
for 1,214 cr each with the 1% tax (15 left there at 1,202 cr), the
tool of the two gas tests; the tests are out (the list in this file's history) and no more
traders get one while the gas bids at our stations stand at 2 cr and
plasma at a few units. An Ice Harvester I (638 cr at Ironlight
Crossroads, 1,413 cr at four of our stations) opens the ice routes,
which are Mining's: not for traders while miners wait for a
harvester (requests.log ENT-082, answered ENT-086). Gas items
are size 2: a hold of 65 carries 32 units of plasma gas. The next hull
is not chosen: tier 2 needs Piloting 10 (section 4).

## 6. Crafting by Hand: the Calls

Flown 2026-11-15, 21:21 to 21:34 UTC, through `game/fleet/gate.py`;
each answer read. A route's craft step is built from this
(requests.log ENT-030).

| Step | Call (tool group) | Answer |
|---|---|---|
| Quote the buy | `estimate_purchase {item_id, quantity}` (spacemolt_market) | Price per fill and the tax. At our stations every buy paid 1%, rounded down, from a player's ask and from the station's own: soma 3 x 258 cr paid 781 (station's ask, Central Nexus 23:27 UTC), ceramite 5 x 899 paid 4,539 (a player's, The Experiment 23:31 UTC), an ice harvester 1,413 paid 1,427 (Mining guidebook, section 5). A 52 cr buy paid 0: 1% of 52 rounds to 0. At Ironlight Crossroads (LHS 1140) 20 silver x 152 paid 3,040, no tax |
| Quote the craft | `craft {recipe_id, quantity, deliver_to: storage, preset: workshop, dry_run: true}` | Runs, venue Station Workshop, `have_inputs`, `effective_time_per_run` 12 ticks, no credit cost |
| Buy | `buy {item_id, quantity}` | One item per tick; goods into the hold |
| Inputs to storage | `deposit {item_id, quantity, target: self, source: cargo}` (spacemolt_storage) | A craft takes its inputs from station storage, not the hold |
| Craft | `craft {recipe_id, quantity, deliver_to: storage, preset: workshop}` | `quantity` counts output items; the job is queued and the inputs escrowed |
| Progress | `craft {}` | The queue with `progress`, `eta_ticks`; an empty queue when done |
| Output to the hold | `withdraw {item_id, quantity}` (spacemolt_storage) | `source: storage, target: self` is refused (`invalid_source`); without them it works |
| Sell | `view_market` first (every price level, each with its `source`: station or player), then `sell {item_id, quantity}` in the default tool group | `sell` takes the best bids level by level: sell no more than the units at the price wanted. `sell` under spacemolt_market is refused (`invalid_action`, 23:41 UTC) |

The circuit runner's `craft` stop, flown 2026-11-16 18:37 to 18:46 UTC
by one trader on a scratch route (assemble_control_node at The Experiment,
requests.log ENT-161): the four inputs bought there (2 circuit boards at
365, 4 copper wiring at 19, gold wiring 190, silver wiring 136: 1,141 cr
with the tax), the quote 0 cr and 12 ticks a run, one run queued, 2
control nodes in storage about two minutes later, taken into the hold and
stored again at the next stop. RESULT: 2/2 stops in 8 minutes, -1,196 cr
with the fuel; the nodes are kept for the station list (its foundry takes
1,500), since the best home bid stood at 40 cr (Node Gamma) against 1,013
asked at Ironlight Crossroads. The game's `craft` help says `quantity` is
the number of output items, rounded up to whole runs; the runner passes
the runs still wanted as that quantity and asks again after each job, so
it reaches `runs` x `per_run` in more jobs than one (`runs` 8, `per_run`
2: jobs of 4, 2, 1 and 1 runs, read from game/fleet/route_run.py, not
flown). With `runs` 1 it made 2 in one job, as the recipe does.

## 7. Open Tests

What the division means to test, with the readings it rests on. A
reading is the state of its hour, not a verdict (rule F22).

- **Copper wiring from surplus copper** (craft-wiring-synchrony-hub, one
  ship, 2026-11-17 19:46 UTC): 20 runs of basic_copper_processing (8
  copper ore make 1 wiring) at Synchrony Hub from the pilot's own copper;
  nothing sold. It reads minutes and crafting XP a run, the work that may
  replace gathering at Okab once the reserve holds its iron (requests.log
  ENT-247). The fleet holds 447,390 copper ore against 22,892 the reserve
  takes (19:32 UTC).
- **Null matter into the Central Nexus bid** (carry-null-matter-beta-to-nexus,
  sell-null-matter-at-nexus, one ship each, 2026-11-17 19:41 UTC): section 1.
- **Iron Ore Resupply** at Trader's Rest Resort Station (Nebula space, 22
  jumps): 80,000 cr for 10,000 iron ore delivered, a faction mission on the
  board read 2026-11-17 17:07 UTC. A Threshold carries 65 and the station
  asks iron at 6 x 924 itself; whether a delivery counts station storage is
  not known. No work for our hulls now.
- **Trade Run missions** (Node Beta and Trader's Rest boards, 2026-11-17):
  no credits, 20 to 40 trading XP and 220 to 620 piloting XP for selling a
  good at a far station (70 hydrogen at Thane Keep, 50 liquid hydrogen at
  Confederacy Central Command, 1 crystal melt at The Rampart Checkpoint).
  70 hydrogen are 140 units of hold: not for a Threshold. The melt run asks
  1 unit; its distance is not read.

- **Spiky bids from stock.** Focused crystal bids rose to 1,041 to
  1,575 cr for 1 to 12 units at Node Alpha and The Experiment for
  minutes at a time (2026-11-16 22:42 to 23:57 UTC, the view `moves`);
  gold wiring did the same at Node Alpha (190 cr, 18:45 UTC). Such a
  bid is served only from stock already lying at that station: a few
  crafted crystals stored at Node Alpha and a sell route with
  `requires.bid` at 1,000 cr is the next test.
- **The standing sell order.** One anchor beacon listed at 1,200 cr at
  Node Beta (2026-11-16 23:48 UTC; The Experiment asks 1,400 for 8,
  every station bid is 2 cr). Unfilled at 2026-11-17 03:34 UTC (section
  1); read again each turn, and cancel it when a reading shows no
  buyer in a day.
- **Buyers at every station since the game's update to v0.721.1**
  (first read about 00:57 UTC on 2026-11-17, books of 01:55 to 03:42
  UTC): uranium ore 600 cr x 3,333 (base value 150, size 2), thorium
  ore 240 x 772 to 886, seam glass 1,200 x 333 (base 600), superfluid
  vial 600 x 40 to 50, methane ice 36 x 1,000. Sirius bids crystal melt
  at 1,585 x 85 (03:29 UTC). No field we read holds uranium, thorium
  or seam glass now (requests.log ENT-194); no book we read asks any
  of them.
- **Market stations not read yet**: Procyon Colonial Station (9 jumps,
  four lawless) and Korr Fortress Station (Gliese 581, 7 jumps, a
  lawless stronghold on the chart): Procyon asked of Intel by name in
  requests.log ENT-194, the others as every station an explorer docks
  at. A stronghold is no place for a trader's test (rule F27).
- **Plasma bought at Ironlight Crossroads** (52 cr, 932,099 on offer,
  2026-11-16 01:39 UTC) and sold into the Node Beta bids: one load of
  32 units paid +1,380 cr in about 19 minutes by hand (03:11 UTC); the
  bids regained 4 to 17 units an hour at the top level. A route with
  `requires.bid` at 100 cr would fly it only when the bids stand.
- **Control nodes made by hand.** Two nodes from bought inputs cost
  about 1,141 to 1,247 cr (2026-11-16); the bids for nodes read 1,089
  x 2 at Synchrony Hub and 40 x 398 at Node Gamma (books of 23:04 to
  23:29 UTC). Two nodes are kept for the station list.
- **Foreign books.** Ironlight Crossroads (LHS 1140) and Nova Terra
  Central (Solarian): every gap against our six books read 2026-11-16
  01:39 and 03:22 UTC was one load or less (plasma 850 cr, processed
  null matter 392 cr for 2 units, deuterium ice 120 to Node Beta's 260
  x 5). Ironlight is cheaper for what the fleet buys: an Ice Harvester
  I 518 to 638 cr against 1,154 to 1,651 at home, fuel 7 cr against
  12.29. Sirius Observatory Station bids 40 cr for 527 lead ore
  (20:05 UTC), where every home bid is 1 cr: the fleet stores 493.
  Since rule F3 every station is open to one ship and one unit.
- **Titles on the Central Nexus board the fleet has not booked**
  (boards of 2026-11-16 12:34 UTC): Listening Orders (7,000 cr and a
  ship scanner), Deep Space Cartography (4,000), Local Sector Survey
  (2,500), Anomalous Readings (500), Titanium Extraction Contract
  (3,500; 20 titanium ore), Amplification Materials and Crystal
  Resonance Harvest (4,000 each), Deep Core Prospecting (5,000 and 10
  exotic matter), Material Synthesis: Basic (1,500), Network Commerce
  Protocol (1,500; sell 5 carbon ore). The survey and visit titles are
  offered to Intel (queue.log ENT-102). Station Need missions (sol
  nacre, void ichor, void-charged ichor; 3,686 to 13,133 cr) wait for a
  source: no book we read offers them and no recipe makes them.
- **The Crimson Resonance** (8,500 cr, after Signal Fragments): the
  accept hands out nothing; it asks 5 titanium alloy delivered at
  Blood Forge, Crimson space, 17 to 20 jumps out.
- **Outpost Kit** at Ironlight Crossroads: 74,010 cr (2 at 12:39 UTC);
  216,825 cr for 1 at 2026-11-15 23:21 UTC.
- Hive Antares has no market (Intel, queue.log ENT-049).

## 8. Station Inputs Bought (plan step P4)

Bought for storage, never for sale; a stock purchase is booked as money
paid once (data/fleet/onetime.json), not as a running cost.

| Input | Bought | Price and depth read | Against mining it | Date |
|---|---|---|---|---|
| Iron ore | 24,442 units into storage at Central Nexus for 24,686 cr with the 1% tax (one unit first, then the rest), 0.99 units per credit; `buy` with `deliver_to: storage` takes a whole ask in one call, no hold and no loop | 1 cr for 24,442 (estimate_purchase, 18:45 UTC): 6,481 from an account named as the market bot of Nexus Prime and 17,961 from ten players; 676 more at Node Gamma; the ask had read 35,923 at 14:49 UTC | The four standing gather routes bring 190 to 295 units of mixed iron and copper a ship-hour at 0.58 to 0.94 cr a unit (runs since 14:00 UTC); with half of it copper, an iron unit gathered costs about 1.2 to 1.9 cr | 2026-11-16 |
| Carbon ore | 1 unit into storage at Node Beta for 4 cr (tax 0 by rounding); no load bought | 4 cr at Node Beta (146,485), Node Gamma (100,595) and Node Alpha (83,648), books of 18:16 to 18:26 UTC; 1,000 units quoted at 4,040 cr with the tax | No home field holds carbon in depth (Gliese 876 Belt 2,901 left, Furud Belt 612); its use is circuit boards (12 carbon and 2 silicon ore make 3), and silicon ore is the limit (34 held, asks of 1 to 4 units) | 2026-11-16 |
| Silicon ore | 75 units at Central Nexus for 31,814 cr with the 1% tax (one unit first), deposited into the storage there of the hauler that crafts the circuit boards, which then read 107 silicon ore | 420 cr; 84 found at that price by `estimate_purchase` (2026-11-16 23:58 UTC); the ask had read 425 at 23:33 UTC; other asks 312 x 1 (Node Alpha), 376 x 4 (Synchrony), 561 x 200 (Ironlight Crossroads) | No field of the 63 systems read holds silicon (Intel, admirals.log ENT-003). Two silicon and 12 carbon make 3 boards by hand: a board costs about 283 cr of silicon and 16 cr of carbon, against 365 to 743 cr asked for boards (books of 23:04 to 23:33 UTC) | 2026-11-16 |
| Steel plate (not bought) | -- | 18 cr at five of our stations: Node Alpha 210,080, Node Beta 82,191, The Experiment 78,089, Node Gamma 71,787, Central Nexus 12,503 (books of 18:16 to 18:26 UTC) | One plate takes 10 iron ore by hand (basic_iron_smelting): 10 cr of bought iron, or 12 to 19 cr of gathered iron, plus the labour; the station list's 491,400 iron ore are its 49,140 steel plates | 2026-11-16 |

