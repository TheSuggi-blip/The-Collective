---
name: routes-plan-sentinel
id: 20261116T174335Z
tier: intel
author: Unity
---

# plan-sentinel.md -- The Plan of the Role sentinel

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/sentinel.json`:
the routes the sentinel ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/sentinel.json` is written from it. `Planned` is what the Admiral
means to do next. Up: [master-index.md](master-index.md).

Kept by Unity. Routes: 36. Ships: 10.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 10 | one-time |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 10 | one-time |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 10 | one-time |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 10 | one-time |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 10 | one-time |
| 6 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 10 | one-time |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 10 | one-time |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 10 | one-time |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | [Off](index-off.md) | home space | once per pilot, up to 2 ships, off | all 10 | one-time |
| 10 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 10 | one-time |
| 11 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 10 | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 15 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 10 | one-time |
| 16 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 10 | 1,500 |
| 17 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | all 10 | one-time |
| 18 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 1,790 |
| 19 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 7,430 |
| 20 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 4,590 |
| 21 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 2,040 |
| 22 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 780 |
| 23 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 10 | 1,060 |
| 24 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 680 |
| 25 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 2,120 |
| 26 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 10 | 80 |
| 27 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 610 |
| 28 | [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 10 | 640 |
| 29 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | all 10 | -520 |
| 30 | [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | all 10 | -490 |
| 31 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 10 | one-time |
| 32 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 10 | one-time |
| 33 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 10 | -130 |
| 34 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 10 | -280 |
| 35 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 10 | -940 |
| 36 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 10 | -670 |
