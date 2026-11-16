---
name: routes-plan-hauler
id: 20261116T174332Z
tier: intel
author: Unity
---

# plan-hauler.md -- The Plan of the Role hauler

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/hauler.json`:
the routes the hauler ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/hauler.json` is written from it. `Planned` is what the Admiral
means to do next. Up: [master-index.md](master-index.md).

Kept by Apollo. Routes: 36. Ships: 20.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 20 | one-time |
| 2 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 3 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 | one-time |
| 5 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 20 | one-time |
| 6 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 20 | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 20 | one-time |
| 8 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 | one-time |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 20 | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 | one-time |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 20 | one-time |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 20 | one-time |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 20 | one-time |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 17 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 20 | one-time |
| 18 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 20 | 2,230 |
| 19 | [sell-plate-node-beta](sell-plate-node-beta.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 1 armor_plate stored at node_beta_industrial_station, while node_beta_industrial_station bids 300 cr for armor_plate | all 20 | -400 |
| 20 | [sell-soma-synchrony](sell-soma-synchrony.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 21 | [sell-soma-node-beta](sell-soma-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 22 | [carry-soma-synchrony-node-alpha](carry-soma-synchrony-node-alpha.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 23 | [carry-soma-synchrony-node-gamma](carry-soma-synchrony-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 24 | [carry-soma-node-beta-node-alpha](carry-soma-node-beta-node-alpha.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 25 | [carry-soma-node-beta-node-gamma](carry-soma-node-beta-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 26 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | all 20 | 9,010 |
| 27 | [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at central_nexus, while central_nexus bids 100 cr for liquid_hydrogen | all 20 | -480 |
| 28 | [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at node_beta_industrial_station, while node_beta_industrial_station bids 95 cr for liquid_hydrogen | all 20 | 16,890 |
| 29 | [mine-atlas-gas-pocket](mine-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 72 cr for plasma_gas | all 20 | 90 |
| 30 | [mine-amberfall-emission-nebula](mine-amberfall-emission-nebula.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_gamma_relay_station bids 27 cr for hydrogen_gas | all 20 | -120 |
| 31 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 20 | -120 |
| 32 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, needs mining_laser_i, standing work | all 20 | -170 |
| 33 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, standing work | all 20 | -150 |
| 34 | [mine-okab-haze](mine-okab-haze.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 4 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | all 20 | -380 |
| 35 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 20 | -630 |
| 36 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 20 | -670 |

Planned:

| What | When |
|---|---|
| Navigation 3 for the ten haulers at level 2 by train.py (skill logistics-stock), a loop of our own stations at about 21 XP and 109 cr; then Signal Fragments (7,000 cr once) from this plan. Restart the training for any pilot whose loop the dispatcher interrupted | turn of 2026-11-16 16:45 UTC |
| Atmospheric Extraction: Setup handed in for the two haulers that fitted the harvester and fly the gas tests (handin_module.py, after their runs); the module fitted again | turn of 2026-11-16 16:45 UTC |
| Read the first RESULT lines of the stored-goods routes (soma, plate, plasma, liquid hydrogen) and of the three gas tests; drop each that loses, lift none above its bid | turn of 2026-11-16 16:45 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |
