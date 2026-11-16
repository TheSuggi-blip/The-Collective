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

Kept by Unity. Routes: 34.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | one-time |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 6 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 10 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 11 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 15 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | 1,790 |
| 16 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 7,430 |
| 17 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 4,590 |
| 18 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 2,040 |
| 19 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 780 |
| 20 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | -340 |
| 21 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 880 |
| 22 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 3,240 |
| 23 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 350 |
| 24 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 610 |
| 25 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 26 | [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, empty hold | 4,560 |
| 27 | [hunt-deepwell-haze-cinder-sylph](hunt-deepwell-haze-cinder-sylph.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, empty hold | -370 |
| 28 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 8 jumps | up to 1 ships, empty hold | -860 |
| 29 | [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | Measured at a Loss | beyond the border, 5 jumps | up to 1 ships, empty hold | -440 |
| 30 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 31 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 32 | [mine-hd-147513-belt](mine-hd-147513-belt.json) | Tests | beyond the border, 7 jumps | up to 1 ships, empty hold | TBD |
| 33 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 34 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

## drone

Kept by Apophis. Routes: 18.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 2 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 3 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 4 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
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
| 15 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 970 |
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

Kept by Apollo. Routes: 18.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | one-time |
| 4 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 6 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 7 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 9 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 10 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 11 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 12 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 13 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 14 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 15 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 3,480 |
| 16 | [sell-plate-node-beta](sell-plate-node-beta.json) | Tests | home space | up to 1 ships, with 1 armor_plate stored at node_beta_industrial_station, while node_beta_industrial_station bids 300 cr for armor_plate | TBD |
| 17 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 18 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Make about ten Ice Harvester I at the Central Nexus workshop from the staged goods (guidebook logistics.md, section 11) when Mining's silicon ore and energy crystal land (requests.log ENT-094); fit them where Zero names (ENT-108), and fit the one made before for the ice route Zero names (ENT-093) | turn of 2026-11-16 08:45 UTC |
| A route that crafts carapace into armor plate where it is stored and sells into the 233 to 380 cr station pools, and one that sells stored soma, both sent only while a bid stands (requests.log ENT-065: craft step, sale from storage, requires.bid); until then by hand where a hauler stands | after 2026-11-16 12:00 UTC |
| mine-achernar-gas-pocket: read its second RESULT line (the first with the runner's dock fix); out of the plan if it loses | turn of 2026-11-16 08:45 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |

## miner

Kept by Zero. Routes: 35.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | one-time |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 6 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 7 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 8 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 9 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 11 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 14 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 15 | [fit-ice-harvester](fit-ice-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 16 | [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 17 | [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 18 | [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | Fitting | home space | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 19 | [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 20 | [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | Fitting | beyond the border, 6 jumps | once per pilot, up to 5 ships, 20 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | one-time |
| 21 | [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | Tests | home space | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | TBD |
| 22 | [drain-ice-node-alpha](drain-ice-node-alpha.json) | Tests | home space | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | TBD |
| 23 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | Tests | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | TBD |
| 24 | [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | Tests | home space | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | TBD |
| 25 | [drain-ice-nexus](drain-ice-nexus.json) | Tests | home space | up to 2 ships, with 30 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | TBD |
| 26 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold, while synchrony_hub bids 25 cr for water_ice | 7,680 |
| 27 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 3,480 |
| 28 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 3,430 |
| 29 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 2,940 |
| 30 | [mine-alnair-ice-fields-nexus](mine-alnair-ice-fields-nexus.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 2,620 |
| 31 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | -340 |
| 32 | [mine-felis-frost-ring](mine-felis-frost-ring.json) | Tests | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_beta_industrial_station bids 156 cr for deuterium_ice | TBD |
| 33 | [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | Tests | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | TBD |
| 34 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 35 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of drain-ice-nexus, drain-ice-node-alpha and the three carries; lift the carries as far as the Central Nexus bid takes them, and cut the mine routes further if the carries fill it | turn of 2026-11-16 16:00 UTC |
| When the stored ice outside Central Nexus is under about 2,000 units, lift the Central Nexus mine routes back toward ten ships; bring the Experiment and Node Alpha mine routes back only when their bids regain with depth (requires.bid opens them by itself) | each turn |

## scout

Kept by Oracle. Routes: 20.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 6 | [census-voidborn](census-voidborn.json) | Reading and Waiting | home space | up to 3 ships | -530 |
| 7 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | Once per Pilot | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 8 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | Once per Pilot | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | TBD |
| 9 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 11 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 12 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 13 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 14 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 15 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 16 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 17 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | 3,220 |
| 18 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | 2,010 |
| 19 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 20 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

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

Kept by Unity. Routes: 31.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | one-time |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 6 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | one-time |
| 10 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 11 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 15 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | Fitting | home space | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 16 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | 1,790 |
| 17 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 7,430 |
| 18 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 4,590 |
| 19 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 2,040 |
| 20 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 780 |
| 21 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | -340 |
| 22 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 880 |
| 23 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 3,240 |
| 24 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 350 |
| 25 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 610 |
| 26 | [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 1,350 |
| 27 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, empty hold | -500 |
| 28 | [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, empty hold | -440 |
| 29 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 30 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 31 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

## trader

Kept by Mercury. Routes: 19.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | one-time |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | one-time |
| 6 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | Fitting | home space | once per pilot, up to 1 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | TBD |
| 7 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | Fitting | home space | once per pilot, up to 1 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | TBD |
| 8 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 9 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 10 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 11 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 12 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 13 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 14 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | Once per Pilot | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | TBD |
| 15 | [mine-the-experiment-haze](mine-the-experiment-haze.json) | Paying Routes | home space | up to 1 ships, needs gas_harvester_i, while node_beta_industrial_station bids 26 cr for hydrogen_gas | 2,330 |
| 16 | [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | Tests | home space | up to 1 ships, needs gas_harvester_i, while synchrony_hub bids 28 cr for hydrogen_gas | TBD |
| 17 | [mine-gsc-0016-emission-nebula](mine-gsc-0016-emission-nebula.json) | Tests | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold | TBD |
| 18 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 19 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Neural Matrix Delivery (5,000 cr once, 8 phase matrix handed out at the accept, Sirius Observatory 9 jumps): one trader flies it as a test the turn Unity allows the goods out (requests.log ENT-146); then a route for every pilot the board offers it to. | after Unity's turn of 2026-11-16 14:30 UTC |
| voidborn-collective-provides on again when a census reads nickel at GSC-0049 Platinum-Group Reef; The Signal Protocol and the line behind it follow it. | each turn |
| The Collective Provides line (Atmospheric Extraction: Setup, Network Commerce Protocol, Hardware Optimization: Cargo, Material Synthesis: Basic): one hand test each with a trader that has The Collective Provides done; a route for each that pays. | the turns of 2026-11-16 |
| Read the whole Central Nexus board of every docked trader at the start of each turn (skill trade-books, boards.py) and test every title the fleet has not booked. | every turn |
| The two haze tests: lift the one whose bid regains, after two RESULT lines each. | the turn of 2026-11-16 16:30 UTC |
