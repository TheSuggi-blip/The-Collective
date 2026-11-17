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
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Unity. Routes: 88. Ships: 20.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 20 |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 1 ships, empty hold, after the reward Network Expansion | all 20 |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 20 |
| 6 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 20 |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 20 |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | [Off](index-off.md) | home space | once per pilot, up to 2 ships, off | all 20 |
| 10 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 20 |
| 11 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 |
| 15 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 20 |
| 16 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 20 |
| 17 | [mine-stillwater-belt](mine-stillwater-belt.json) | [Tests](index-tests.md) | beyond the border, 19 jumps | up to 1 ships | 1 of 20 |
| 18 | [hunt-test-tanglewood-hollow-pilgrim](hunt-test-tanglewood-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 20 |
| 19 | [hunt-wasat-cryobelt-hollow-pilgrim](hunt-wasat-cryobelt-hollow-pilgrim.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 20 | [hunt-groombridge-1618-frozen-drift-hollow-pilgrim](hunt-groombridge-1618-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 21 | [hunt-regor-wr-bubble-cinder-sylph](hunt-regor-wr-bubble-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 22 | [hunt-gsc-0012-gas-plume-halo-drifter](hunt-gsc-0012-gas-plume-halo-drifter.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 20 |
| 23 | [hunt-ran-haze-chlorophage](hunt-ran-haze-chlorophage.json) | [Tests](index-tests.md) | beyond the border, 25 jumps | up to 1 ships, empty hold | 1 of 20 |
| 24 | [hunt-hollowcrest-frozen-drift-hollow-pilgrim](hunt-hollowcrest-frozen-drift-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 25 | [hunt-ankaa-cryobelt-hollow-pilgrim](hunt-ankaa-cryobelt-hollow-pilgrim.json) | [Tests](index-tests.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 20 |
| 26 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | 1 of 20 |
| 27 | [hunt-aldhibah-ice-shelf-hollow-pilgrim](hunt-aldhibah-ice-shelf-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 20 |
| 28 | [hunt-violethall-gas-plume-cinder-sylph](hunt-violethall-gas-plume-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 17 jumps | up to 1 ships, empty hold | 1 of 20 |
| 29 | [hunt-miaplacidus-frost-ring-hollow-pilgrim](hunt-miaplacidus-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 30 | [hunt-tania-vapor-fields-cinder-sylph](hunt-tania-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 31 | [sell-melt-experiment-sirius](sell-melt-experiment-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at the_experiment_research_station, while sirius_observatory_station bids 1000 cr for crystal_melt | 1 of 20 |
| 32 | [hunt-alnair-ice-fields-hollow-pilgrim](hunt-alnair-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 20 |
| 33 | [mine-regor-inner-debris](mine-regor-inner-debris.json) | [Tests](index-tests.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | 1 of 20 |
| 34 | [hunt-toi-2257-gas-pocket-cinder-sylph](hunt-toi-2257-gas-pocket-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 26 jumps | up to 1 ships, empty hold | 1 of 20 |
| 35 | [hunt-alathfar-haze-chlorophage](hunt-alathfar-haze-chlorophage.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 2 of 20 |
| 36 | [hunt-etamin-haze-cinder-sylph](hunt-etamin-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 37 | [hunt-ridgecrest-ice-shelf-hollow-pilgrim](hunt-ridgecrest-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 38 | [hunt-avior-cryobelt-hollow-pilgrim](hunt-avior-cryobelt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 20 |
| 39 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | 1 of 20 |
| 40 | [hunt-harborlight-ice-shelf-hollow-pilgrim](hunt-harborlight-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 41 | [hunt-summervale-gas-pocket-cinder-sylph](hunt-summervale-gas-pocket-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 21 jumps | up to 1 ships, empty hold | 1 of 20 |
| 42 | [hunt-alsciaukat-vapor-fields-cinder-sylph](hunt-alsciaukat-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 1 of 20 |
| 43 | [hunt-alnilam-gas-pocket-halo-drifter](hunt-alnilam-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 44 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | 1 of 20 |
| 45 | [hunt-gsc-0004-gas-pocket-cinder-sylph](hunt-gsc-0004-gas-pocket-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 20 |
| 46 | [hunt-cervantes-vapor-fields-halo-drifter](hunt-cervantes-vapor-fields-halo-drifter.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 47 | [hunt-gsc-0040-frost-ring-hollow-pilgrim](hunt-gsc-0040-frost-ring-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 20 |
| 48 | [mine-flicker-fray](mine-flicker-fray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 20 |
| 49 | [hunt-antares-gas-cloud-cinder-sylph](hunt-antares-gas-cloud-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 20 |
| 50 | [mine-celaeno-frozen-drift](mine-celaeno-frozen-drift.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 20 |
| 51 | [mine-nightveil-dark-residue](mine-nightveil-dark-residue.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 20 |
| 52 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 20 |
| 53 | [drain-methane-experiment](drain-methane-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 10 methane_ice stored at the_experiment_research_station, while the_experiment_research_station bids 30 cr for methane_ice | 1 of 20 |
| 54 | [mine-oxbow-ice-belt](mine-oxbow-ice-belt.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 13 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 20 |
| 55 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 2 of 20 |
| 56 | [train-navigation-trader](train-navigation-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 20 ships, under navigation 3, standing work | 5 of 20 |
| 57 | [hunt-angetenar-gas-pocket-cinder-sylph](hunt-angetenar-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 1 of 20 |
| 58 | [mine-gsc-0042-ice-shelf](mine-gsc-0042-ice-shelf.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 20 |
| 59 | [mine-atria-ice-fields](mine-atria-ice-fields.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 20 |
| 60 | [mine-groombridge-34-ice-fields](mine-groombridge-34-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 20 |
| 61 | [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 20 |
| 62 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | all 20 |
| 63 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | all 20 |
| 64 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 20 |
| 65 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 20 |
| 66 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 20 |
| 67 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 20 |
| 68 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 20 |
| 69 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 20 |
| 70 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 20 |
| 71 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | all 20 |
| 72 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | [Tests](index-tests.md) | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 20 |
| 73 | [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) | [Tests](index-tests.md) | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | all 20 |
| 74 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | all 20 |
| 75 | [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | 17 of 20 |
| 76 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 |
| 77 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 |
| 78 | [gather-schedar-belt](gather-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 45 ships, needs mining_laser_i, empty hold, standing work | all 20 |
| 79 | [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 35 ships, needs mining_laser_i, empty hold, standing work | all 20 |
| 80 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 20 |
| 81 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 20 |
| 82 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 20 |
| 83 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 20 |
| 84 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 120 ships, needs mining_laser_i, standing work | all 20 |
| 85 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, needs mining_laser_i, standing work | all 20 |
| 86 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 20 |
| 87 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 20 |
| 88 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 20 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [ice-and-hunt](templates-command.md) | 17 |
