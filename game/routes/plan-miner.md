---
name: routes-plan-miner
id: 20261116T174333Z
tier: intel
author: Unity
---

# plan-miner.md -- The Plan of the Role miner

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/miner.json`:
the routes the miner ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/miner.json` is written from it. `Planned` is what the Admiral
means to do next. Up: [master-index.md](master-index.md).

Kept by Zero. Routes: 38. Ships: 40.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 | one-time |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 40 | one-time |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 | one-time |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 40 | one-time |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 | one-time |
| 6 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 40 | one-time |
| 7 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 40 | one-time |
| 8 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 40 | one-time |
| 9 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 | one-time |
| 11 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 40 | one-time |
| 12 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 40 | one-time |
| 13 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 | one-time |
| 14 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 | one-time |
| 15 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 40 | one-time |
| 16 | [fit-ice-harvester](fit-ice-harvester.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 17 | [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 18 | [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 19 | [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 20 | [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | all 40 | one-time |
| 21 | [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, up to 5 ships, 20 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | all 40 | one-time |
| 22 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 40 | TBD |
| 23 | [drain-methane-experiment](drain-methane-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 30 methane_ice stored at the_experiment_research_station, while the_experiment_research_station bids 30 cr for methane_ice | 38 of 40 | TBD |
| 24 | [drain-ice-nexus](drain-ice-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 2 ships, with 30 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | 38 of 40 | -460 |
| 25 | [drain-ice-node-alpha](drain-ice-node-alpha.json) | [Tests](index-tests.md) | home space | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | 38 of 40 | TBD |
| 26 | [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | 38 of 40 | -360 |
| 27 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | 38 of 40 | -460 |
| 28 | [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | 38 of 40 | -480 |
| 29 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | 38 of 40 | 1,060 |
| 30 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 38 of 40 | 2,230 |
| 31 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 38 of 40 | 3,670 |
| 32 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 38 of 40 | 1,900 |
| 33 | [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | 38 of 40 | TBD |
| 34 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | 38 of 40 | -170 |
| 35 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | 38 of 40 | -120 |
| 36 | [mine-acubens](mine-acubens.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | 38 of 40 | -170 |
| 37 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 40 | -630 |
| 38 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of drain-ice-nexus, drain-ice-node-alpha and the three carries; lift the carries as far as the Central Nexus bid takes them, and cut the mine routes further if the carries fill it | turn of 2026-11-16 16:00 UTC |
| When the stored ice outside Central Nexus is under about 2,000 units, lift the Central Nexus mine routes back toward ten ships; bring the Experiment and Node Alpha mine routes back only when their bids regain with depth (requires.bid opens them by itself) | each turn |
