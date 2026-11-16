---
name: routes-plan-command
id: 20261116T174330Z
tier: intel
author: Unity
---

# plan-command.md -- The Plan of the Role command

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/command.json`:
the routes the command ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/command.json` is written from it. `Planned` is what the Admiral
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Unity. Routes: 41. Ships: 6.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 6 |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 6 |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 6 |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 6 |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 6 |
| 6 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 6 |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 6 |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 6 |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | [Off](index-off.md) | home space | once per pilot, up to 2 ships, off | all 6 |
| 10 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 6 |
| 11 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 6 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 15 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 6 |
| 16 | [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 6 |
| 17 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 6 |
| 18 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 6 |
| 19 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 6 |
| 20 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | all 6 |
| 21 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 6 |
| 22 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 6 |
| 23 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 |
| 24 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 |
| 25 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 6 |
| 26 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 |
| 27 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 |
| 28 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 6 |
| 29 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 6 |
| 30 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 6 |
| 31 | [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 |
| 32 | [hunt-deepwell-haze-cinder-sylph](hunt-deepwell-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 |
| 33 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | all 6 |
| 34 | [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | all 6 |
| 35 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 6 |
| 36 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 37 | [mine-hd-147513-belt](mine-hd-147513-belt.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 |
| 38 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 6 |
| 39 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 6 |
| 40 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 6 |
| 41 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 6 |
