---
name: routes-plan
id: 20261116T001236Z
tier: intel
author: Unity
---

# plan.md -- The Plans

Written by `python3 -B game/fleet/routes.py index`, never by hand, from
`plans/<role>.json`: per role (the word before the dash of a pilot's name) the routes
its ships fly, in one order, and how many of its ships have each route in their plan.
Each division's Admiral keeps one plan file with every ship and its own routes
(`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder and
not here, and `plans/<role>.json` is written from it. `Planned` is what the Admiral
means to do next. The roles at a glance: [master-index.md](master-index.md); every
route's figures: [index.md](index.md).

## command

Kept by Unity. Routes: 37.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | all 6 | one-time |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 6 | one-time |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 6 | one-time |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | all 6 | one-time |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | all 6 | one-time |
| 6 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | all 6 | one-time |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | all 6 | one-time |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 6 | one-time |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | all 6 | one-time |
| 10 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | all 6 | one-time |
| 11 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 6 | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 6 | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 6 | one-time |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 6 | one-time |
| 15 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | Fitting | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 6 | one-time |
| 16 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | all 6 | 1,790 |
| 17 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 6 | 7,430 |
| 18 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 6 | 4,590 |
| 19 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 | 2,040 |
| 20 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 | 780 |
| 21 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 6 | 1,060 |
| 22 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 | 680 |
| 23 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 | 2,120 |
| 24 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 | 80 |
| 25 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 6 | 610 |
| 26 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 6 | one-time |
| 27 | [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 | 3,480 |
| 28 | [hunt-deepwell-haze-cinder-sylph](hunt-deepwell-haze-cinder-sylph.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 | 320 |
| 29 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 8 jumps | up to 1 ships, empty hold | all 6 | -740 |
| 30 | [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | Measured at a Loss | beyond the border, 5 jumps | up to 1 ships, empty hold | all 6 | -440 |
| 31 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 6 | one-time |
| 32 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 6 | one-time |
| 33 | [mine-hd-147513-belt](mine-hd-147513-belt.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 | 20 |
| 34 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | Standing Work, Reading and Waiting | home space | up to 50 ships, needs mining_laser_i, standing work | all 6 | -100 |
| 35 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | Standing Work, Reading and Waiting | home space | up to 46 ships, needs mining_laser_i, standing work | all 6 | -160 |
| 36 | [census-frontier](census-frontier.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | all 6 | -630 |
| 37 | [park](park.json) | Standing Work, Reading and Waiting | home space | the park route | all 6 | -670 |

## drone

Kept by Apophis. Routes: 38.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | all 30 | one-time |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | all 30 | one-time |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 30 | one-time |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 30 | one-time |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 30 | one-time |
| 6 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 30 | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 30 | one-time |
| 8 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 9 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 10 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 30 | one-time |
| 11 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 30 | one-time |
| 12 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 30 | one-time |
| 13 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | all 30 | one-time |
| 14 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | all 30 | one-time |
| 15 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | all 30 | one-time |
| 16 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | all 30 | one-time |
| 17 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 30 | one-time |
| 18 | [sell-curd-central-nexus](sell-curd-central-nexus.json) | Paying Routes | home space | up to 1 ships, with 2 verdigris_curd stored at central_nexus, while central_nexus bids 250 cr for verdigris_curd | all 30 | 302,820 |
| 19 | [sell-curd-node-beta](sell-curd-node-beta.json) | Paying Routes | home space | up to 1 ships, with 2 verdigris_curd stored at node_beta_industrial_station, while node_beta_industrial_station bids 250 cr for verdigris_curd | all 30 | 29,370 |
| 20 | [sell-curd-experiment](sell-curd-experiment.json) | Paying Routes | home space | up to 1 ships, with 2 verdigris_curd stored at the_experiment_research_station, while the_experiment_research_station bids 250 cr for verdigris_curd | all 30 | 13,390 |
| 21 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 100 cr for ember_gland | all 30 | 6,720 |
| 22 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i, while central_nexus bids 100 cr for verdigris_curd | all 30 | 3,020 |
| 23 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i, while central_nexus bids 100 cr for verdigris_curd | all 30 | 2,310 |
| 24 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 100 cr for verdigris_curd | all 30 | 2,100 |
| 25 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for verdigris_curd | all 30 | 1,420 |
| 26 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for verdigris_curd | all 30 | 1,300 |
| 27 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for ember_gland | all 30 | 600 |
| 28 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 100 cr for verdigris_curd | all 30 | 840 |
| 29 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for verdigris_curd | all 30 | 800 |
| 30 | [train-navigation-home](train-navigation-home.json) | Measured at a Loss | home space | up to 1 ships | all 30 | -470 |
| 31 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 32 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 33 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | Once per Pilot | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 30 | one-time |
| 34 | [census-guard-ice](census-guard-ice.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 2 ships, empty hold | all 30 | -610 |
| 35 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | Standing Work, Reading and Waiting | home space | up to 50 ships, needs mining_laser_i, standing work | all 30 | -100 |
| 36 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | Standing Work, Reading and Waiting | home space | up to 46 ships, needs mining_laser_i, standing work | all 30 | -160 |
| 37 | [census-frontier](census-frontier.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | all 30 | -630 |
| 38 | [park](park.json) | Standing Work, Reading and Waiting | home space | the park route | all 30 | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of the seven veil-ray hunts once the loss stop's six-hour window passes their losing runs of 07:05 to 09:20 UTC, and of First Hunt and Cracking the Shell at Achernar on their herd floor; drop a route at its second losing run in a row. | next Military turn |
| Navigation 3 opens Signal Fragments (7,000 cr once) to the 19 drones at navigation 2: measure which drone route gains the most navigation XP per credit of fuel (ship files before and after), then put the drones nearest to level 3 on it. | next Military turn |
| Carapace into armor plate where it lies (orders ENT-013, APOPHIS (6)): plate.py over all drones, no plate sold past a bid's depth. | every turn |
| Guard: the route kind guard (owed by Unity, requests.log ENT-070, her turn of 18:30 UTC) replaces census-guard-ice with one drone beside each mine route beyond the border. | when the guard kind exists |
| The next hull: no purchase while every hunt is bounded by its herd and its bid; a tier-1 Vigil as one test only for prey over 100 hull, which needs an order beyond F9. | on an order |

## hauler

Kept by Apollo. Routes: 36.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | Once per Pilot | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 20 | one-time |
| 2 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | Fitting | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 3 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | Fitting | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 | one-time |
| 5 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | all 20 | one-time |
| 6 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 20 | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 20 | one-time |
| 8 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 | one-time |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 11 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | all 20 | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 20 | one-time |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | all 20 | one-time |
| 14 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | all 20 | one-time |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | all 20 | one-time |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 17 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 20 | one-time |
| 18 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 20 | 2,230 |
| 19 | [sell-plate-node-beta](sell-plate-node-beta.json) | Measured at a Loss | home space | up to 1 ships, with 1 armor_plate stored at node_beta_industrial_station, while node_beta_industrial_station bids 300 cr for armor_plate | all 20 | -400 |
| 20 | [sell-soma-synchrony](sell-soma-synchrony.json) | Tests | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 21 | [sell-soma-node-beta](sell-soma-node-beta.json) | Tests | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 22 | [carry-soma-synchrony-node-alpha](carry-soma-synchrony-node-alpha.json) | Tests | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 23 | [carry-soma-synchrony-node-gamma](carry-soma-synchrony-node-gamma.json) | Tests | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 24 | [carry-soma-node-beta-node-alpha](carry-soma-node-beta-node-alpha.json) | Tests | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 25 | [carry-soma-node-beta-node-gamma](carry-soma-node-beta-node-gamma.json) | Tests | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 26 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | Tests | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | all 20 | TBD |
| 27 | [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) | Measured at a Loss | home space | up to 1 ships, with 5 liquid_hydrogen stored at central_nexus, while central_nexus bids 100 cr for liquid_hydrogen | all 20 | -480 |
| 28 | [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) | Paying Routes | home space | up to 1 ships, with 5 liquid_hydrogen stored at node_beta_industrial_station, while node_beta_industrial_station bids 95 cr for liquid_hydrogen | all 20 | 16,890 |
| 29 | [mine-atlas-gas-pocket](mine-atlas-gas-pocket.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 72 cr for plasma_gas | all 20 | 90 |
| 30 | [mine-amberfall-emission-nebula](mine-amberfall-emission-nebula.json) | Measured at a Loss | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_gamma_relay_station bids 27 cr for hydrogen_gas | all 20 | -120 |
| 31 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | Standing Work, Reading and Waiting | home space | up to 50 ships, needs mining_laser_i, standing work | all 20 | -100 |
| 32 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | Standing Work, Reading and Waiting | home space | up to 46 ships, needs mining_laser_i, standing work | all 20 | -160 |
| 33 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | Standing Work, Reading and Waiting | home space | up to 6 ships, standing work | all 20 | -130 |
| 34 | [mine-okab-haze](mine-okab-haze.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | all 20 | TBD |
| 35 | [census-frontier](census-frontier.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | all 20 | -630 |
| 36 | [park](park.json) | Standing Work, Reading and Waiting | home space | the park route | all 20 | -670 |

Planned:

| What | When |
|---|---|
| Navigation 3 for the ten haulers at level 2 by train.py (skill logistics-stock), a loop of our own stations at about 21 XP and 109 cr; then Signal Fragments (7,000 cr once) from this plan. Restart the training for any pilot whose loop the dispatcher interrupted | turn of 2026-11-16 16:45 UTC |
| Atmospheric Extraction: Setup handed in for the two haulers that fitted the harvester and fly the gas tests (handin_module.py, after their runs); the module fitted again | turn of 2026-11-16 16:45 UTC |
| Read the first RESULT lines of the stored-goods routes (soma, plate, plasma, liquid hydrogen) and of the three gas tests; drop each that loses, lift none above its bid | turn of 2026-11-16 16:45 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |

## miner

Kept by Zero. Routes: 41.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 | one-time |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | all 40 | one-time |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 | one-time |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 40 | one-time |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 | one-time |
| 6 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | all 40 | one-time |
| 7 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | all 40 | one-time |
| 8 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | all 40 | one-time |
| 9 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 40 | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 40 | one-time |
| 11 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 40 | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 40 | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 40 | one-time |
| 14 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 40 | one-time |
| 15 | [fit-ice-harvester](fit-ice-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 16 | [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 17 | [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 18 | [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | Fitting | home space | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 19 | [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 20 | [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | Fitting | beyond the border, 6 jumps | once per pilot, up to 5 ships, 20 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | all 40 | one-time |
| 21 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 40 | one-time |
| 22 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 40 | one-time |
| 23 | [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | Measured at a Loss | home space | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | all 40 | -360 |
| 24 | [drain-ice-node-alpha](drain-ice-node-alpha.json) | Tests | home space | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | all 40 | TBD |
| 25 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | Measured at a Loss | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | all 40 | -460 |
| 26 | [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | Measured at a Loss | home space | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | all 40 | -480 |
| 27 | [drain-ice-nexus](drain-ice-nexus.json) | Measured at a Loss | home space | up to 2 ships, with 30 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | all 40 | -460 |
| 28 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold, while synchrony_hub bids 25 cr for water_ice | all 40 | 5,860 |
| 29 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 40 | 2,230 |
| 30 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 40 | 3,670 |
| 31 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 40 | 1,900 |
| 32 | [mine-alnair-ice-fields-nexus](mine-alnair-ice-fields-nexus.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 40 | 2,200 |
| 33 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 40 | 1,060 |
| 34 | [mine-felis-frost-ring](mine-felis-frost-ring.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_beta_industrial_station bids 156 cr for deuterium_ice | all 40 | -70 |
| 35 | [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | Tests | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 40 | TBD |
| 36 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | Standing Work, Reading and Waiting | home space | up to 50 ships, needs mining_laser_i, standing work | all 40 | -100 |
| 37 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | Standing Work, Reading and Waiting | home space | up to 46 ships, needs mining_laser_i, standing work | all 40 | -160 |
| 38 | [mine-acubens](mine-acubens.json) | Standing Work, Reading and Waiting | home space | up to 18 ships, needs mining_laser_i, standing work | all 40 | -160 |
| 39 | [mine-pherkad-rift](mine-pherkad-rift.json) | Standing Work, Reading and Waiting | home space | up to 18 ships, needs mining_laser_i, standing work | all 40 | -170 |
| 40 | [census-frontier](census-frontier.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | all 40 | -630 |
| 41 | [park](park.json) | Standing Work, Reading and Waiting | home space | the park route | all 40 | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of drain-ice-nexus, drain-ice-node-alpha and the three carries; lift the carries as far as the Central Nexus bid takes them, and cut the mine routes further if the carries fill it | turn of 2026-11-16 16:00 UTC |
| When the stored ice outside Central Nexus is under about 2,000 units, lift the Central Nexus mine routes back toward ten ships; bring the Experiment and Node Alpha mine routes back only when their bids regain with depth (requires.bid opens them by itself) | each turn |

## scout

Kept by Oracle. Routes: 22.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | all 20 | one-time |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 20 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 | one-time |
| 6 | [census-voidborn](census-voidborn.json) | Standing Work, Reading and Waiting | home space | up to 3 ships | all 20 | -530 |
| 7 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | Once per Pilot | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 20 | one-time |
| 8 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | Once per Pilot | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 20 | one-time |
| 9 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 20 | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 11 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | all 20 | one-time |
| 12 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | all 20 | one-time |
| 13 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | all 20 | one-time |
| 14 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | all 20 | one-time |
| 15 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 16 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 20 | one-time |
| 17 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | all 20 | 2,420 |
| 18 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | all 20 | 1,730 |
| 19 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | Standing Work, Reading and Waiting | home space | up to 50 ships, needs mining_laser_i, standing work | all 20 | -100 |
| 20 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | Standing Work, Reading and Waiting | home space | up to 46 ships, needs mining_laser_i, standing work | all 20 | -160 |
| 21 | [census-frontier](census-frontier.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | all 20 | -630 |
| 22 | [park](park.json) | Standing Work, Reading and Waiting | home space | the park route | all 20 | -670 |

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

Kept by Unity. Routes: 35.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | all 10 | one-time |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 10 | one-time |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 10 | one-time |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | all 10 | one-time |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | all 10 | one-time |
| 6 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | all 10 | one-time |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | all 10 | one-time |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 10 | one-time |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | all 10 | one-time |
| 10 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | all 10 | one-time |
| 11 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 10 | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 15 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | Fitting | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 10 | one-time |
| 16 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | Fitting | home space | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | all 10 | one-time |
| 17 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 1,790 |
| 18 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 7,430 |
| 19 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 4,590 |
| 20 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 2,040 |
| 21 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 780 |
| 22 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 10 | 1,060 |
| 23 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 680 |
| 24 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 2,120 |
| 25 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 80 |
| 26 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 610 |
| 27 | [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 640 |
| 28 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, empty hold | all 10 | -520 |
| 29 | [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, empty hold | all 10 | -490 |
| 30 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 10 | one-time |
| 31 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | Once per Pilot | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 32 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | Standing Work, Reading and Waiting | home space | up to 50 ships, needs mining_laser_i, standing work | all 10 | -100 |
| 33 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | Standing Work, Reading and Waiting | home space | up to 46 ships, needs mining_laser_i, standing work | all 10 | -160 |
| 34 | [census-frontier](census-frontier.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | all 10 | -630 |
| 35 | [park](park.json) | Standing Work, Reading and Waiting | home space | the park route | all 10 | -670 |

## trader

Kept by Mercury. Routes: 24.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | Once per Pilot | home space | once per pilot, up to 3 ships | all 20 | one-time |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | Off | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 20 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | Once per Pilot | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 | one-time |
| 6 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | Fitting | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 7 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | Fitting | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 8 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | all 20 | one-time |
| 9 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | all 20 | one-time |
| 10 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | all 20 | one-time |
| 11 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 12 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 13 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 20 | one-time |
| 14 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | Once per Pilot | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 20 | one-time |
| 15 | [mine-the-experiment-haze](mine-the-experiment-haze.json) | Paying Routes | home space | up to 1 ships, needs gas_harvester_i, while node_beta_industrial_station bids 26 cr for hydrogen_gas | all 20 | 1,160 |
| 16 | [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | Tests | home space | up to 1 ships, needs gas_harvester_i, while synchrony_hub bids 28 cr for hydrogen_gas | all 20 | TBD |
| 17 | [mine-gsc-0016-emission-nebula](mine-gsc-0016-emission-nebula.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold | all 20 | 510 |
| 18 | [mine-marfik-emission-nebula](mine-marfik-emission-nebula.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold | all 20 | 240 |
| 19 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | Standing Work, Reading and Waiting | home space | up to 50 ships, needs mining_laser_i, standing work | all 20 | -100 |
| 20 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | Standing Work, Reading and Waiting | home space | up to 46 ships, needs mining_laser_i, standing work | all 20 | -160 |
| 21 | [mine-acubens](mine-acubens.json) | Standing Work, Reading and Waiting | home space | up to 18 ships, needs mining_laser_i, standing work | all 20 | -160 |
| 22 | [mine-pherkad-rift](mine-pherkad-rift.json) | Standing Work, Reading and Waiting | home space | up to 18 ships, needs mining_laser_i, standing work | all 20 | -170 |
| 23 | [census-frontier](census-frontier.json) | Standing Work, Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | all 20 | -630 |
| 24 | [park](park.json) | Standing Work, Reading and Waiting | home space | the park route | all 20 | -670 |

Planned:

| What | When |
|---|---|
| Neural Matrix Delivery (5,000 cr once, 8 phase matrix handed out at the accept, Sirius Observatory 9 jumps): one trader flies it as a test the turn Unity allows the goods out (requests.log ENT-146); then a route for every pilot the board offers it to. | after Unity's turn of 2026-11-16 14:30 UTC |
| voidborn-collective-provides on again when a census reads nickel at GSC-0049 Platinum-Group Reef; The Signal Protocol and the line behind it follow it. | each turn |
| The Collective Provides line (Atmospheric Extraction: Setup, Network Commerce Protocol, Hardware Optimization: Cargo, Material Synthesis: Basic): one hand test each with a trader that has The Collective Provides done; a route for each that pays. | the turns of 2026-11-16 |
| Read the whole Central Nexus board of every docked trader at the start of each turn (skill trade-books, boards.py) and test every title the fleet has not booked. | every turn |
| The two haze tests: lift the one whose bid regains, after two RESULT lines each. | the turn of 2026-11-16 16:30 UTC |
