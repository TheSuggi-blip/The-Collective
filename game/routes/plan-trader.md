---
name: routes-plan-trader
id: 20261116T174336Z
tier: intel
author: Unity
---

# plan-trader.md -- The Plan of the Role trader

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/trader.json`:
the routes the trader ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/trader.json` is written from it. `Planned` is what the Admiral
means to do next. Up: [master-index.md](master-index.md).

Kept by Mercury. Routes: 30. Ships: 40.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 40 | one-time |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 40 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 | one-time |
| 6 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 40 | one-time |
| 7 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 40 | one-time |
| 8 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 40 | one-time |
| 9 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 40 | one-time |
| 10 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 40 | one-time |
| 11 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 | one-time |
| 12 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 | one-time |
| 13 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 40 | one-time |
| 14 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 40 | one-time |
| 15 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 | one-time |
| 16 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 | one-time |
| 17 | [train-navigation-trader](train-navigation-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 4 ships, under navigation 3, standing work | 4 of 40 | -560 |
| 18 | [voidborn-neural-matrix-delivery](voidborn-neural-matrix-delivery.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 1 ships, empty hold, with 8 phase_matrix stored at synchrony_hub | 1 of 40 | one-time |
| 19 | [mine-coldwater-emission-nebula](mine-coldwater-emission-nebula.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 1 of 40 | -390 |
| 20 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 40 | 1,730 |
| 21 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 40 | 2,420 |
| 22 | [mine-marfik-emission-nebula](mine-marfik-emission-nebula.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold | all 40 | 420 |
| 23 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 40 | -130 |
| 24 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | all 40 | -170 |
| 25 | [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | [Tests](index-tests.md) | home space | up to 1 ships, needs gas_harvester_i, while synchrony_hub bids 28 cr for hydrogen_gas | all 40 | TBD |
| 26 | [mine-gsc-0016-emission-nebula](mine-gsc-0016-emission-nebula.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold | all 40 | 320 |
| 27 | [mine-acubens](mine-acubens.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | all 40 | -170 |
| 28 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 40 | -280 |
| 29 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 40 | -940 |
| 30 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 | -670 |

Planned:

| What | When |
|---|---|
| Neural Matrix Delivery (5,000 cr once, 8 phase matrix handed out at the accept, Sirius Observatory 9 jumps): one trader flies it as a test the turn Unity allows the goods out (requests.log ENT-146); then a route for every pilot the board offers it to. | after Unity's turn of 2026-11-16 14:30 UTC |
| voidborn-collective-provides on again when a census reads nickel at GSC-0049 Platinum-Group Reef; The Signal Protocol and the line behind it follow it. | each turn |
| The Collective Provides line (Atmospheric Extraction: Setup, Network Commerce Protocol, Hardware Optimization: Cargo, Material Synthesis: Basic): one hand test each with a trader that has The Collective Provides done; a route for each that pays. | the turns of 2026-11-16 |
| Read the whole Central Nexus board of every docked trader at the start of each turn (skill trade-books, boards.py) and test every title the fleet has not booked. | every turn |
| The two haze tests: lift the one whose bid regains, after two RESULT lines each. | the turn of 2026-11-16 16:30 UTC |
