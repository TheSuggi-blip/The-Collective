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

## Standing Plan

What the 20 haulers fly between two turns (2026-11-16 18:37 UTC, orders.log
ENT-017), from the division's plan file (`plan.py show`; the role plan
`game/routes/plan-hauler.md` is written from it). Every hauler has routes of its
own since this turn. A free hauler takes the first route open to it of: the list
First, its own routes, the list Then. The forecast of the division (the tool hive,
verb=forecast): -3,165 cr an hour before this plan (18:27 UTC), -3,064 after it
(18:41 UTC), every ship on standing work at that moment.

| Order | Routes | Ships | Carries | Per ship-hour | Why it stands here |
|---|---|---|---|---|---|
| First (every ship) | the 17 once missions (`voidborn-*`, `mission-cracking-the-shell-central`) | as their files say | -- | once money | Strategy, principle 5: a pilot flies the once line first. Every hauler holds or has flown the ones open to it today |
| Own, 1-11 (every hauler) | `sell-soma-synchrony`, `sell-soma-node-beta`, four `carry-soma-*`, `sell-plate-node-beta`, `sell-plasma-node-beta`, `sell-liquid-hydrogen-central`, `sell-liquid-hydrogen-node-beta`, `carry-liquid-hydrogen-node-beta-central` | 1 each, only a pilot whose own storage holds the good (`requires.stored`), only while a book of the last hour shows the bid (`requires.bid`) | one ship while its bid stands | measured once each: liquid hydrogen at Central Nexus +2,702 cr in 4.9 min, at Node Beta +1,154 cr in 4.1 min; plasma +706 cr in 4.7 min; plate +1,050 cr in 3.7 min (runs.jsonl, 15:02 to 17:55 UTC) | Goods we own go into a standing bid before any ship gathers more. They head every own list because a route in Then is never reached by a ship whose own standing work stays open |
| Own, gas haulers (4 with a Gas Harvester I) | `mine-coldwater-emission-nebula` (test), `mine-antares-gas-cloud` (test), `mine-amberfall-emission-nebula`, `mine-deepwell-haze` (test) | 1 each | the bid at the selling end | amberfall 3 runs +1,362 cr in 217 min (about +376); antares 1 run +209 in 55.5 min; deepwell 1 run +41 in 59.9 min | Gas sold into the hydrogen bid at Node Gamma or the plasma bid at Nova Terra Central (Unity's ruling, requests.log ENT-160). What a small bid does not take is stored where the ship sold: 232 and 231 units after the two Nova Terra runs |
| Own, the ice hauler (an Ice Harvester I) | `mine-gliese-876-belt` (test, nickel at Nova Terra Central), `mine-achernar-frost-ring-nexus` | 1 | Achernar `2` | Achernar 2,230 measured for miners | The one made harvester in a hauler's slot |
| Own, standing work (every hauler, in three orders) | `gather-gsc-0027-prism-scatter` first for 5, `gather-hamal-crystal-bloom` first for 8, `gather-gsc-0027-spacetime-seep` first for 2; each hauler lists the other two behind | 56 and 56 of the fleet, 6 | `0 +363`, `0 +378`, `2 +115` | -132, -180, -152 (forecast, 18:41 UTC) | Iron and copper ore into storage at Node Beta: iron is the stations' largest shortfall and the input of the faction's steel plate (section 13). Not judged on pay; `min_left` closes each field |
| Then (every ship) | `census-frontier`, `park` | census 12 of the fleet | -- | census about -630 | A hauler should never reach them |

So, for the four hours: once money where a pilot still holds a link, stored goods
into each bid as it stands, the gas and ice tests one ship each, and iron and copper
gathered for the stations by every other hauler. Hand work of the turn (section 14):
the faction's 275 steel plate made from stored iron at the Node Beta workshop, and
stored hydrogen gas made into liquid hydrogen for the Central Nexus bid.

What changes it: the boards' silicon and carbon in one storage at Central Nexus
(requests.log ENT-168), which turns one hauler into a board maker; Trade's word on
focused crystal (ENT-169); a second RESULT line of each gas test (a test that loses
twice leaves); a craft step flown once by Trade (requests.log ENT-161), after which
the gas haulers can mine, compress and sell liquid hydrogen in one route; a bid
for water ice that regains more than the miners take.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| -- | -- | -- | No recurring route yet. The hand sales that earned (section 7) were each capped by a station bid of a few units |
| Stored hydrogen gas made into liquid hydrogen at the Node Beta workshop and carried one jump to the Central Nexus bid (scratch routes flown by route_run, `craftchain.py`) | +4,798 cr in about 20 min of one hauler: -48 cr the plasma stop that sold nothing, 0 cr the crafts, +4,846 cr the carry (42 sold at 116 cr); 33 liquid hydrogen left for the bids (21 at Central Nexus, 12 at Node Beta) | 2026-11-16 13:20 to 13:40 UTC | `compress_hydrogen_gas` (8 gas to 3 liquid, by hand, 0 cr) made 75 liquid hydrogen from 200 gas in 6.5 min, queued by the workshop in runs of 9, 6, 4, 2, 2, 1 and 1. The Central Nexus bid stood at 111 x 112 (12:50 UTC book) against 34 cr x 135 for the gas at Node Beta |
| Stored platinum ore into the Central Nexus bid where three haulers stood (`sellstore.py`) | +504 cr for 8 units at 63 cr, no fuel | 2026-11-16 about 12:58 UTC | Stopped there: platinum ore is an input of the station, 3,720 needed and 523 held, asked at 150 cr at Central Nexus (base_plan, 12:55 UTC) |
| Carapace from 11 hauler holds and 7 storages (114 units) made into armor plate at three stations, sold into the bids there and one hop away (by script: `gather.py`, `plate.py`, a scratch carry) | +4,240 cr for 12 plates: 3 at 378 (The Experiment), 1 at 396 (Node Beta), 4 at 373 (Central Nexus), and 4 carried one jump from Node Beta to the Node Gamma bid of 312 x 4, +1,218 cr after fuel in 4 min; 18 plates made from 108 carapace, 6 left in storage for the next bids | 2026-11-16 08:49 to 09:01 UTC | Every plate bid read minutes before the sale; each sold no deeper than its best price. The gathering emptied the holds that closed the census and the hunts (`hold not empty` on 10 haulers at 08:46 UTC) |
| Creature carapace made into armor plate and sold where the ship stood (by hand, no fuel) | +380 cr for each 6 carapace: 2 plates made at the Central Nexus workshop (recipe `carapace_plating`, 0 cr, about one tick) and sold into the 380 x 3 station bid | 2026-11-16 04:59 to 05:08 UTC | Carapace is bid 1 cr (Node Beta, 99,593 units, 05:15 UTC book); armor plate pools of 3 to 6 units stand at Central Nexus (380), Synchrony Hub (307 to 324), Node Gamma (319) and Node Alpha (222 to 259) and come back within the hour (`ledger.py prices armor_plate`). A route when the runner has its craft step (owed by 12:00 UTC) |
| The gas test's hold sold at Node Beta (scratch route by hand) | +899 cr in 7.5 min with the hop from Central Nexus: 8 plasma gas at 100 cr, 4 hydrogen gas at 33 cr; argon, neon and the other 8 hydrogen stored there | 2026-11-16 05:03 to 05:10 UTC | Both bids were empty after it |
| Two soma gathered from two holds sold into The Experiment's station bids of 677 x 1 and 645 x 1 where the ship stood | +1,322 cr | 2026-11-16 08:56 UTC | view_market read in the same minute |
| One stored soma into The Experiment's bid where a hauler stood | +588 cr | 2026-11-16, between 04:51 and 04:55 UTC | The 588 x 1 bid read in the book of 04:26 UTC still stood |
| Neural soma sold by hand where the haulers already stood (no fuel) | +2,381 cr for 4 soma: 3 at 588 cr into the Node Beta bid of 588 x 4 (02:57 UTC book; 2 from storage, 1 from a hold), 1 at 617 cr a few minutes after the same bid read 0 | 2026-11-16 03:00 to 03:19 UTC | Sold from storage and from the hold alike; a bid read empty at 03:18 UTC stood at 617 x 1 within about two minutes |
| Stored neural soma into station bids (hand test, not a route) | +1,995 cr in 4.7 min from the first jump to the sale (one ship, Central Nexus to Synchrony Hub, 3 soma sold at 678 cr from storage); the onward leg to The Experiment found no bid (-22 cr fuel) | 2026-11-15 23:29 to 23:37 UTC | Station bids of 559 to 694 cr for 1 to 3 units stand by turns at five of our stations and refill within about 40 minutes of being emptied (`data/market/history.jsonl`, 20:46 to 23:33 UTC). Logistics stores 50 soma, the fleet 302. A route needs a sell from storage and a dispatch on a standing bid (requests.log ENT-065) |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `mine-antares-gas-cloud`, `mine-deepwell-haze` (gas tests that sell plasma at Nova Terra Central, Solarian) | 1 run each: +209 cr in 55.5 min and +41 cr in 59.9 min; 240 and 239 units mined, 8 plasma sold each at 92 and 88 cr (runs.jsonl, 14:46 UTC) | 2026-11-16 | The plasma bid there took 8 units a run; the rest, 232 and 231 units of argon, neon, hydrogen and other gas, lies in two hauler storages at Nova Terra Central (storage book 18:37 UTC), 8 jumps from Nexus Prime (game/planets/n-nova_terra.md), and is bid 2 to 34 cr at our stations. Back in the plan as one-ship tests on Unity's ruling (requests.log ENT-160); a second run that pays less than standing work takes each out |
| `mission-ghosts-in-the-cloud-node` (added by fill.py on a measure of command ships) | 2 hauler runs, `ghosts_in_the_cloud not offered`, -24 cr each | 2026-11-16 13:12 to 13:18 UTC | The board offered it to the two command ships that were paid and refused the six pilots after them; out of the hauler plan at 13:16 UTC |
| `mine-achernar-frost-ring-nexus` (the hauler with the made harvester) | 2 runs, -3,346 cr in 107.5 min since 08:45 UTC (runs.jsonl) | 2026-11-16 | The weekly tax of 12:27 UTC fell inside a run (errors.log ENT-056); the loss stop closed the route on its last three runs. Zero cut its places from 15 to 3 (requests.log ENT-143) |
| `sell-plate-node-beta`, first run | -22 cr in 3.3 min: the 361 x 4 plate bid read at 12:44 UTC read 0 at 13:26 UTC | 2026-11-16 | `requires.bid` trusts a book up to an hour old. It stays in the plan: the bid came back within the hour all day (`ledger.py prices armor_plate`) |
| The once line after The Collective Provides, with a free utility slot | 4 hauler runs bought the module and fitted it: -1,262 cr three times (Atmospheric Extraction), -430 cr once (Hardware Optimization) | 2026-11-16 13:03 UTC | `have_item` counts the hold, not the slot (section 3). Two of the four handed in since by `handin_module.py`, +2,000 and +1,500 cr; the other two after their gas tests |
| `mine-gsc-0012-gas-plume`, `mine-miram-haze` (tests, one hauler each) | 1 run each: 224 and 304 units of gas mined in 72.6 and 71.9 min, nothing sold, -495 and -451 cr | 2026-11-16 13:12 to 14:25 UTC | The Node Beta hydrogen bid read 1 unit at 13:36 UTC; the runs began before `requires.bid` stood in their files. The gas lies in storage at Node Beta (174 hydrogen and more by 13:59 UTC): 8 hydrogen make 3 liquid hydrogen by hand, and the Central Nexus liquid-hydrogen bid stood at 116 to 121 cr for 34 to 89 units from 13:57 to 14:25 UTC (`ledger.py prices liquid_hydrogen`). Out of the plan at 14:28 UTC |
| The plasma sale of the first hand haul from storage | -48 cr in 8 min, nothing sold | 2026-11-16 13:20 UTC | The circuit's withdraw step asked 33 plasma (66 units of space) of a free hold of 65 and was refused; fixed in commit df8f6fb |
| `mine-acubens`, `mine-gsc-seep`, `mine-pherkad-rift` (haulers) | -172, -180 and -174 cr per ship-hour over 29, 7 and 31 runs (`board.py Apollo`, last four hours at 21:16 UTC) | 2026-11-15 | All fuel; the ore has no buyer. Out of the plan (orders F8) |
| `voidborn-first-steps` while the belt was empty | One run of 20 minutes, -109 cr, nothing handed in ("objectives not done") | 2026-11-15 21:02 UTC | Acubens Belt read 0 carbon ore at 21:01 UTC. It refilled since (section 3) |
| Selling stored iron ore into station bids | 10 units sold at 2 cr from storage; the bid at Central Nexus went 20, 10, none (21:22 to 21:33 UTC); it came back by 5 to 15 units at 1 to 2 cr every 5 to 20 minutes, and stood at 2 cr for 2,375 at 23:17 UTC, about two hours after it emptied (`data/market/history.jsonl`) | 2026-11-15 | A station-owned bid is a pool that refills on its own clock. At 2 cr the ore stays in storage (orders.log ENT-007, block APOLLO): steel and wiring are what a base will need |
| Ferrous slug cases for The Experiment | The best bid is 15 cr for 8 cases, then 2 cr for 314 (queue.log ENT-037). The 322 at 15 cr read on 2026-11-15 19:03 UTC was the total of all levels | 2026-11-15 | A trip burns more than 8 cases bring. Not flown |
| `mission-cracking-the-shell-central` and `-achernar` (once routes added by fill.py) | 12 hauler runs, every one `cracking_the_shell not offered`: 8 at -26 cr, 4 at 0 cr, -208 cr in all; the Achernar route read at a loss, 2 runs, -104 cr | 2026-11-16 02:56 to 03:27 UTC | The board offers it only to a pilot with First Hunt booked (errors.log ENT-033: 7 of 7 with it, 0 of 12 without). Both out of the hauler plan at 03:27 UTC; one hauler with First Hunt booked accepted it by hand at 05:14 UTC |
| `mine-achernar-gas-pocket` (gas test, one hauler with a Gas Harvester I) | 3 runs: -297, -396, -396 cr in 183.6 min, -1,089 cr in sum, about -356 cr per ship-hour; the first ended not docked for the sale, the other two sold nothing (`route mine-achernar-gas-pocket`, 03:51 to 07:15 UTC) | 2026-11-16 | Out of the plan at 08:59 UTC. The bids are the limit: at Node Beta hydrogen 33 x 32 and plasma 94 x 4 (08:57 UTC book), while that hauler stores 204 hydrogen, 83 plasma, 213 argon and 175 neon there. A gas route adds nothing until the stored gas is sold; the candidate mine-miram-haze (1,970 estimated, hydrogen into the same 32-unit bid) was not added for that reason |
| `hunt-dimming-pocket-veil-ray` | 6 runs: +583 and five at -77 to -99 cr; +176 cr in 68.7 min over all six, the last four all at a loss; every run left with a ship not of ours at the place | 2026-11-16 02:56 to 07:18 UTC | Out of the plan at 08:59 UTC; Military took the same herd out at 05:16 UTC for the same reason |
| `hunt-denebola-fractured-prism-veil-ray` (test) | 3 runs: -110, +209, -110 cr in 50.4 min, -11 cr in sum; a ship not of ours stood at the place in 2 of 3 | 2026-11-16 02:56 to 04:23 UTC | Out of the hauler plan at 05:00 UTC (commit 221f9d2) |
| Carrying a soma to a bid seen 39 minutes earlier | The Experiment bid 690 cr for 2 at 22:58 UTC; at 23:37 UTC no bid stood (view_market) | 2026-11-15 | A saved bid of a few units is gone within the hour: carry only to a bid read minutes before, or store the goods where the bid comes back |

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

## 4. Levelling

Navigation is the skill a hauler buys with jumps (2026-11-16): about 3 XP a
jump and 1 a dock. One hauler went 277 to 289 on three jumps and three docks
(9.4 min, -80 cr), and ten haulers gained 21 XP on each loop of six jumps and
three docks between our own stations (12.6 to 12.7 min, -109 cr a loop; ship
files and runs.jsonl, 13:05 to 13:35 UTC). The 10 haulers born on 2026-11-15
evening stood at navigation 2, 51 to 109 XP short of level 3, Signal Fragments'
gate (7,000 cr once); `train.py` of the skill logistics-stock flies the loop
until the level, three to six loops a pilot. Done 13:05 to 14:27 UTC: all ten
reached level 3 in 3 to 6 loops (49 loops, -5,341 cr, 620 ship-minutes, the
train.py RESULT lines and runs.jsonl), 534 cr a pilot against 7,000 cr once.
The first trained hauler flew Signal Fragments at once: +6,868 cr in 19.2 min.

On 2026-11-16 09:00 UTC (the tool fleet, view=levels): Piloting 3 lowest,
4 median, 5 highest; 87 Piloting XP an hour on average over a median of 17
hours played, about 141 hours to Piloting 10 and the tier-2 hulls at that
rate; deep core mining 3, mining 3, navigation 2, xenobiology 1 and weapons
1 (medians). Navigation 3 opens Signal Fragments (7,000 cr once): 2 haulers
held it at 08:46 UTC and 4 at 09:16 UTC (ship files); the two that reached
it had both flown the veil-ray hunt four jumps beyond the border that day
(runs.jsonl). Which work trains navigation fastest is `not measured`. The first
hauler run of the route: +6,883 cr in 17.9 min (08:51 UTC).
On 2026-11-16 03:28 UTC: Piloting 3 lowest, 4 median and highest; 112
Piloting XP an hour, about 111 hours to Piloting 10. Mining 3, deep core
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
the ask 1,202 cr). It is the tool of the gas test `mine-achernar-gas-pocket`, which lost
(section 2).

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
| Nitrogen ice | None worth a trip: 2 cr for 49 at The Experiment. Its hand recipe (5 ice to 4 liquid nitrogen) meets a 2 cr bid |
| Helium ice | 2 cr for 500 at The Experiment; its recipe is facility-only and helium-3 is bid 2 cr |
| Oxygen ice | No bid; its recipe is facility-only and oxygen gas has no bid |

LHS 1140 bids for methane ice only (36 cr for 500 at 23:45 UTC; nothing at 23:21 UTC). And no ship carries goods of value out of
Voidborn space (orders F13): a buyer beyond the border is no use to the
goods we store until that order changes.

## 10. Open Tests

- The stored-goods routes (soma, plate, plasma, liquid hydrogen), one ship each
  while a bid stands; since 18:37 UTC at the head of every hauler's own routes.
  Measured once each (Standing Plan); the soma routes have no run yet.
- `carry-liquid-hydrogen-node-beta-central` (written 2026-11-16 18:35 UTC): liquid
  hydrogen made at the Node Beta workshop into the Central Nexus bid. Its first
  RESULT line decides it.
- The gas tests `mine-coldwater-emission-nebula`, `mine-antares-gas-cloud`,
  `mine-deepwell-haze` and the ice hauler's `mine-gliese-876-belt` (nickel at Nova
  Terra Central), one ship each.
- The boards for the faction (section 14): one batch of etchings when Mining's
  silicon and carbon lie in the crafter's storage (requests.log ENT-168).
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
waits. The workshop queued fewer runs than asked when a job would run long:
7 etchings asked, 3 queued, then 2, 1 and 1; 5 power cells and 5 harvesters
were queued whole (about 32 and 70 ticks). The harvesters took about 18
minutes for five, about 3.6 minutes each against 13.9 ticks quoted (about
2.5 minutes at 11 s a tick). Mining gave 30 silicon ore and
35 energy crystal by deposit (requests.log ENT-124). The first harvester is
fitted to the hauler that made it (09:25 UTC); the five lie in its storage,
unplaced, because the bids bound ice work (section 12). Left there: 16
silicon, 20 crystal, 19 carbon, 15 flex polymer, 8 wiring, 1 board; four
more need 160 iron ore and about 15 copper ore gathered (1 etching and 6
`fabricate_circuit_boards` runs for their 16 boards).

## 12. Capacity of the Domain (orders F18)

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
  hydrogen (111 cr x 112 at Central Nexus). Only the liquid hydrogen and the plate
  have a bid worth a trip.
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
- Ships the hauling employs: the once missions for every hauler this turn;
  no repeating route pays a hauler. Logistics needs no more ships; each
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

Read 2026-11-16 04:50 to 05:21 UTC (`data/stock/storage.json`, the ship
files, the tool fleet with view=capacity, `ledger.py prices`).

- Storage of Logistics: iron ore 11,631 and copper ore 6,207 (all
  stations), carbon ore 130 before this turn's gathering, neural soma 46 in
  storage; the chain's goods of section 11 at Central Nexus.
- What it makes today by hand: about 1,160 steel plate and 775 copper
  wiring from that ore (each pilot from its own storage), neither with a
  bid worth a sale; and armor plate from creature carapace: the fleet holds
  565 carapace (468 in storage, 97 in holds; 394 of it Military's), about
  94 plates, sold at 233 to 380 cr into pools of 3 to 6 units at four
  stations that come back within the hour. The bids are the limit; how
  fast they come back is not measured.
- What the soma bids take: pools of 1 to 2 units at 522 to 698 cr at four
  stations (books of 04:13 to 04:26 UTC); the fleet holds 380 soma. The
  bids are the limit, not the haulers.
- Water ice, the work a harvester opens: the bids carry about 58 ships for
  four hours against 47 ships that carry a harvester, the fields about
  1,088 (fleet capacity, 05:00 UTC). So about 11 ice places stand open for
  the tool, about the ten Logistics makes.
- Ships the hauling employs today: one for the chain, one for the gas
  test, one hunter, two on First Steps, up to five on First Hunts and the
  census by turns; 12 of 20 wait. Logistics needs no more ships: each
  harvester made turns one waiting hauler into an ice ship where Mining
  gives the place.

## 13. The Stations' List (orders.log ENT-017, P4)

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

## 14. The Faction's Plates and Boards (orders.log ENT-017, P5)

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

Circuit boards: not made this turn. Every by-hand board recipe takes silicon ore,
and the fleet holds 34, all at Central Nexus: 16 in one hauler's storage, 16 and 1
in two Mining storages, 1 in a scout's (storage book 18:37 UTC).
`carbon_arc_circuit_etching` makes 3 boards from 2 silicon and 12 carbon;
`fabricate_circuit_boards` 2 boards from 2 silicon, 3 copper and 1 energy crystal.
So 75 boards take 50 silicon by etching (and 300 carbon), 75 by fabrication. With
Mining's 16 silicon and 17 carbon in the crafting hauler's storage (requests.log
ENT-168), 16 etchings give 48 boards; with the one board stored there, 49 of 75.
The other 26 take about 18 silicon more: Central Nexus asked silicon ore at 420 cr
for 424 units and circuit boards at 686 cr for 250 (book of 19:07 UTC). Etched from
bought silicon a board costs about 280 cr in silicon (2 at 420 for 3 boards), against
686 cr bought whole. Silicon is the limit; a buy for a craft is one unit first (rule
F12).
