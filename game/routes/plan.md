---
name: routes-plan
id: 20261116T001236Z
tier: intel
author: Unity
---

# plan.md -- The Plans

Written by `python3 -B game/fleet/routes.py index`, never by hand, from
`plans/<role>.json`: per role (the word before the dash of a pilot's name) the routes
the dispatcher tries in this order for a free pilot. The role's Admiral keeps the
file; `planned` in it is what the Admiral means to do next. The roles at a glance:
[master-index.md](master-index.md); every route's figures: [index.md](index.md).

## command

Kept by Unity. Routes: 31.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-collective-provides](voidborn-collective-provides.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion | one-time |
| 2 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 3 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 4 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 5 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 6 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 7 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 9 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 11 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 12 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 13 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 14 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 1,480 |
| 15 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 7,430 |
| 16 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 4,590 |
| 17 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,040 |
| 18 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 780 |
| 19 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -340 |
| 20 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 600 |
| 21 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1,630 |
| 22 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 350 |
| 23 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 610 |
| 24 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 25 | [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, empty hold | 4,560 |
| 26 | [hunt-deepwell-haze-cinder-sylph](hunt-deepwell-haze-cinder-sylph.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, empty hold | -370 |
| 27 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 8 jumps | up to 1 ships, empty hold | -860 |
| 28 | [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | Measured at a Loss | beyond the border, 5 jumps | up to 1 ships, empty hold | -430 |
| 29 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 30 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 31 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

## drone

Kept by Apophis. Routes: 18.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 2 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 3 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 4 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 5 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 6 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 7 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 9 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 10 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 11 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 12 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 13 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 14 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 4,230 |
| 15 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,270 |
| 16 | [census-guard-ice](census-guard-ice.json) | Reading and Waiting | beyond the border, 7 jumps | up to 2 ships, empty hold | -610 |
| 17 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 18 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Veil-ray hunts back into the plan when a verdigris curd bid of 100 cr or more reads again at a station of our books (the tool market, item verdigris_curd); requires.bid for hunt routes asked of Unity so that the dispatcher does this by itself. | every turn until the bid returns |
| First Hunt at Achernar and Schedar back when a census reads the belt without a ship not ours twice in a row. | next turn |
| Carapace into armor plate where it lies (orders ENT-013, APOPHIS (6)): plate.py per drone and station, no plate sold past a bid's depth. | every turn |
| Measure census-guard-ice: its fuel per hour against what its reads renew (pilots met beside our miners). | next turn |
| Guard: the route kind guard (owed by Unity, requests.log ENT-070) replaces census-guard-ice with one drone standing beside each mine route beyond the border. | when the guard kind exists |
| The next hull: no purchase while every hunt is bounded by its herd and its bid; a tier-1 Vigil as one test only for prey over 100 hull, which needs an order beyond F9. | on an order |

## hauler

Kept by Apollo. Routes: 17.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion | one-time |
| 3 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 5 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 6 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 7 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 8 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 9 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 10 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 11 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 12 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 13 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 14 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 15 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 15 ships, needs ice_harvester_i, empty hold | 3,480 |
| 16 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 17 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Make about ten Ice Harvester I at the Central Nexus workshop from the staged goods (guidebook logistics.md, section 11) when Mining's silicon ore and energy crystal land (requests.log ENT-094); fit them where Zero names (ENT-108), and fit the one made before for the ice route Zero names (ENT-093) | turn of 2026-11-16 08:45 UTC |
| A route that crafts carapace into armor plate where it is stored and sells into the 233 to 380 cr station pools, and one that sells stored soma, both sent only while a bid stands (requests.log ENT-065: craft step, sale from storage, requires.bid); until then by hand where a hauler stands | after 2026-11-16 12:00 UTC |
| mine-achernar-gas-pocket: read its second RESULT line (the first with the runner's dock fix); out of the plan if it loses | turn of 2026-11-16 08:45 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |

## miner

Kept by Zero. Routes: 30.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 2 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 3 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 4 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 5 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 10 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 11 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 12 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 13 | [fit-ice-harvester](fit-ice-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 14 | [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 15 | [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 16 | [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | Fitting | home space | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 17 | [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 18 | [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | Fitting | beyond the border, 6 jumps | once per pilot, up to 5 ships, 20 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | one-time |
| 19 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold | 7,680 |
| 20 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 15 ships, needs ice_harvester_i, empty hold | 3,480 |
| 21 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 5 ships, needs ice_harvester_i, empty hold | 2,940 |
| 22 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 3,480 |
| 23 | [mine-alnair-ice-fields-nexus](mine-alnair-ice-fields-nexus.json) | Paying Routes | beyond the border, 5 jumps | up to 8 ships, needs ice_harvester_i, empty hold | 2,330 |
| 24 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 7,430 |
| 25 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 4,590 |
| 26 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -340 |
| 27 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,040 |
| 28 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 600 |
| 29 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 30 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT line of mine-ruchbah-ice-belt-nexus and the runs of the three lifted Central Nexus routes; lift what pays as far as the Central Nexus bid carries (44,128 units in all levels at 07:58 UTC, regains about 1,250 an hour); bring the Experiment and Node Alpha routes back up when their bids regain | turn of 2026-11-16 12:00 UTC |
| About 11,000 water ice lie in miners' storage at The Experiment, Node Alpha and Synchrony where the bids are 0: a carry from storage to the Central Nexus bid (a withdraw step), or Logistics hauling it | turn of 2026-11-16 12:00 UTC |

## scout

Kept by Oracle. Routes: 17.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 2 | [census-voidborn](census-voidborn.json) | Reading and Waiting | home space | up to 3 ships | -530 |
| 3 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 4 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | Once per Pilot | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 5 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 6 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 7 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 8 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 9 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 10 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 11 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 12 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 13 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 14 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | 3,220 |
| 15 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | 2,010 |
| 16 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 17 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 3; read the gaps per system every turn and change the threshold only on a measured gap over 60 minutes | every turn |
| Read the first RESULT line of voidborn-first-hunt-intercrus-belt after its loss stop lapses (about 09:30 UTC); if it pays, voidborn-first-hunt-intercrus-remnants and a route at Intercrus Sootfall Belt (16 belt-grazers at 08:17 UTC) for the rest of the scouts without First Hunt | next turn |
| Signal Fragments: 11 scouts with navigation 3; ask Trade for more places (requests.log ENT-118); the nine with navigation 2 fly it when they reach 3 | every turn |
| Fourth ring (Felis, Acrab, Botein, Acrux): belt-grazer herds of 11 to 14 and two pirates; a hunt route there only after a drop of the species sells and Military has looked at the pirates | when a herd's drop sells |
| Nova Terra Central (Solarian) read about once a day while Trade weighs a trade | daily |
| Read the game's changelog at every turn and name each line of game/rules/ a release makes wrong in a request to the Fleet Admiral | every turn |

## sentinel

Kept by Unity. Routes: 28.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 2 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 3 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 4 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 5 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 7 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 8 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 9 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 10 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 11 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 12 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | Fitting | home space | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 13 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 1,480 |
| 14 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 7,430 |
| 15 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 4,590 |
| 16 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,040 |
| 17 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 780 |
| 18 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -340 |
| 19 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 600 |
| 20 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1,630 |
| 21 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 350 |
| 22 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 610 |
| 23 | [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1,350 |
| 24 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, empty hold | -500 |
| 25 | [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, empty hold | -440 |
| 26 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 27 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 28 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

## trader

Kept by Mercury. Routes: 15.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 6 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 7 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 8 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 9 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 10 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 11 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 12 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 13 | [mine-the-experiment-haze](mine-the-experiment-haze.json) | Paying Routes | home space | up to 1 ships, needs gas_harvester_i | 2,330 |
| 14 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 15 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Atmospheric Extraction: Setup (2,000 cr once, acquire a gas harvester): one trader without a harvester accepts it, buys a Gas Harvester I at Node Beta (1,202 cr) and reads the objective; a route only if the purchase counts. Hardware Optimization: Cargo (1,500 cr, acquire a cargo expander): read the expander's ask first, then the same test. | the turn of 2026-11-16 12:30 UTC |
| Network Commerce Protocol (1,500 cr, sell 5 carbon ore) and Material Synthesis: Basic (1,500 cr, mine 10 iron ore and smelt it into steel): one hand test each with a trader that has The Collective Provides done; a route once the runner can withdraw from storage and craft. | the turn of 2026-11-16 12:30 UTC |
| Read the whole Central Nexus board of every docked trader at the start of each turn (skill trade-books, boards.py) and test every title the fleet has not booked. | every turn |
| Plasma gas from Ironlight Crossroads into the station bids at Node Beta: a route only with requires.bid (owed by Unity). | after 2026-11-16 12:00 UTC |
| Control-node craft as a route when the runner's craft step exists and circuit boards stand at depth. | after 2026-11-16 12:00 UTC |
