---
name: routes-plan-drone
id: 20261116T174331Z
tier: intel
author: Unity
---

# plan-drone.md -- The Plan of the Role drone

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/drone.json`:
the routes the drone ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/drone.json` is written from it. `Planned` is what the Admiral
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Apophis. Routes: 119. Ships: 50.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 50 |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 50 |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 50 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 50 |
| 5 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 |
| 6 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 50 |
| 7 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 8 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 9 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 50 |
| 10 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 50 |
| 11 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 50 |
| 12 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 50 |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 50 |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 50 |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 50 |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 |
| 17 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 18 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 50 |
| 19 | [hunt-silverbend-emission-nebula-cinder-sylph](hunt-silverbend-emission-nebula-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 20 | [hunt-tania-vapor-fields-cinder-sylph](hunt-tania-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 21 | [hunt-etamin-haze-cinder-sylph](hunt-etamin-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 22 | [hunt-yildun-outer-ice-hollow-pilgrim](hunt-yildun-outer-ice-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 23 | [hunt-willowgate-vapor-fields-halo-drifter](hunt-willowgate-vapor-fields-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 17 jumps | up to 1 ships, empty hold | 1 of 50 |
| 24 | [hunt-saltwind-gas-pocket-halo-drifter](hunt-saltwind-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 25 | [hunt-sandrift-ice-fields-hollow-pilgrim](hunt-sandrift-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 26 | [hunt-gsc-0042-ice-shelf-hollow-pilgrim](hunt-gsc-0042-ice-shelf-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 27 | [hunt-gsc-0037-frost-ring-hollow-pilgrim](hunt-gsc-0037-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 28 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 29 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | 3 of 50 |
| 30 | [hunt-gsc-0040-frost-ring-hollow-pilgrim](hunt-gsc-0040-frost-ring-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 50 |
| 31 | [hunt-gsc-0035-vapor-fields-cinder-sylph](hunt-gsc-0035-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 32 | [hunt-alchiba-ice-belt-hollow-pilgrim](hunt-alchiba-ice-belt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 50 |
| 33 | [hunt-alathfar-haze-chlorophage](hunt-alathfar-haze-chlorophage.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 50 |
| 34 | [hunt-harborlight-ice-shelf-hollow-pilgrim](hunt-harborlight-ice-shelf-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 50 |
| 35 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | 1 of 50 |
| 36 | [hunt-biham-ice-shelf-hollow-pilgrim](hunt-biham-ice-shelf-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 37 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | 4 of 50 |
| 38 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | 3 of 50 |
| 39 | [hunt-arneb-gas-pocket-drift-ray](hunt-arneb-gas-pocket-drift-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 40 | [hunt-angetenar-gas-pocket-cinder-sylph](hunt-angetenar-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 1 of 50 |
| 41 | [hunt-oxbow-ice-belt-frost-moth](hunt-oxbow-ice-belt-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 1 ships, empty hold, standing work | 2 of 50 |
| 42 | [hunt-avior-gas-pocket-halo-drifter](hunt-avior-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 2 of 50 |
| 43 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 50 |
| 44 | [hunt-hd-10647-ice-field-frost-moth](hunt-hd-10647-ice-field-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 23 jumps | up to 1 ships, empty hold | 1 of 50 |
| 45 | [hunt-gsc-0012-gas-plume-halo-drifter](hunt-gsc-0012-gas-plume-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 50 |
| 46 | [hunt-wasat-cryobelt-hollow-pilgrim](hunt-wasat-cryobelt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 47 | [hunt-avior-cryobelt-hollow-pilgrim](hunt-avior-cryobelt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 50 |
| 48 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 50 |
| 49 | [sell-ember-experiment-dheneb](sell-ember-experiment-dheneb.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at the_experiment_research_station, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 50 | [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 51 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | all 50 |
| 52 | [sell-melt-nexus-sirius](sell-melt-nexus-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at central_nexus, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 53 | [sell-melt-experiment-sirius](sell-melt-experiment-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at the_experiment_research_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 54 | [sell-melt-node-beta-sirius](sell-melt-node-beta-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at node_beta_industrial_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 55 | [sell-melt-synchrony-sirius](sell-melt-synchrony-sirius.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at synchrony_hub, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 56 | [sell-melt-at-sirius](sell-melt-at-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 1 crystal_melt stored at sirius_observatory_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 57 | [hunt-rasalhague-ice-fields-hollow-pilgrim](hunt-rasalhague-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 58 | [hunt-elnath-ice-belt-hollow-pilgrim](hunt-elnath-ice-belt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 59 | [hunt-gsc-0024-frost-ring-hollow-pilgrim](hunt-gsc-0024-frost-ring-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 60 | [hunt-atria-ice-fields-hollow-pilgrim](hunt-atria-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 61 | [hunt-groombridge-34-ice-fields-hollow-pilgrim](hunt-groombridge-34-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 62 | [hunt-epsilon-eridani-ice-fields-hollow-pilgrim](hunt-epsilon-eridani-ice-fields-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 63 | [hunt-hassaleh-ice-halo-hollow-pilgrim](hunt-hassaleh-ice-halo-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 64 | [hunt-hassaleh-ice-halo-frost-moth](hunt-hassaleh-ice-halo-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 50 |
| 65 | [hunt-gemma-haze-halo-drifter](hunt-gemma-haze-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | all 50 |
| 66 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 67 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 68 | [hunt-test-bluerift-frost-ring-rime-grazer](hunt-test-bluerift-frost-ring-rime-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 69 | [hunt-schedar-belt-carapace](hunt-schedar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 70 | [hunt-ironhollow-fading-signal-carapace](hunt-ironhollow-fading-signal-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 71 | [hunt-ironhollow-echo-ejecta-carapace](hunt-ironhollow-echo-ejecta-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 72 | [hunt-achernar-belt-carapace](hunt-achernar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 73 | [hunt-okab-belt-carapace](hunt-okab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 74 | [hunt-gj-3470-dewfall-fray-carapace](hunt-gj-3470-dewfall-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 75 | [hunt-keid-belt-carapace](hunt-keid-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 76 | [hunt-achird-belt-carapace](hunt-achird-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 77 | [hunt-gsc-0012-flicker-fray-carapace](hunt-gsc-0012-flicker-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 78 | [hunt-amberfall-belt-carapace](hunt-amberfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 79 | [hunt-gsc-0031-belt-carapace](hunt-gsc-0031-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 80 | [hunt-acrab-thinspace-rubble-carapace](hunt-acrab-thinspace-rubble-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 81 | [hunt-acrab-belt-carapace](hunt-acrab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 82 | [hunt-atlas-gossamer-null-carapace](hunt-atlas-gossamer-null-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 83 | [hunt-gsc-0044-belt-carapace](hunt-gsc-0044-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 84 | [hunt-gsc-0044-forgotten-tailings-carapace](hunt-gsc-0044-forgotten-tailings-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 85 | [hunt-botein-lampglint-rock-carapace](hunt-botein-lampglint-rock-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 86 | [hunt-botein-belt-carapace](hunt-botein-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 87 | [hunt-acrux-belt-carapace](hunt-acrux-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 88 | [hunt-intercrus-sootfall-belt-carapace](hunt-intercrus-sootfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 89 | [hunt-intercrus-belt-carapace](hunt-intercrus-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 90 | [hunt-intercrus-alloy-remnants-carapace](hunt-intercrus-alloy-remnants-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 91 | [hunt-goldcrest-glitterback-scatter-carapace](hunt-goldcrest-glitterback-scatter-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 92 | [hunt-goldcrest-belt-carapace](hunt-goldcrest-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 93 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 50 |
| 94 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 50 |
| 95 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 96 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 97 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 98 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 99 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 100 | [hunt-home-drift-ray](hunt-home-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | all 50 |
| 101 | [hunt-shaula-gas-plume-drift-ray](hunt-shaula-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 102 | [hunt-gsc-0038-vapor-fields-drift-ray](hunt-gsc-0038-vapor-fields-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 103 | [hunt-marfik-emission-nebula-drift-ray](hunt-marfik-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 104 | [hunt-atria-emission-nebula-drift-ray](hunt-atria-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 105 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 50 |
| 106 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 50 |
| 107 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 50 |
| 108 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 50 |
| 109 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 50 |
| 110 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 50 |
| 111 | [mine-acubens](mine-acubens.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | all 50 |
| 112 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 120 ships, needs mining_laser_i, standing work | all 50 |
| 113 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, needs mining_laser_i, standing work | all 50 |
| 114 | [gather-schedar-belt](gather-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 45 ships, needs mining_laser_i, empty hold, standing work | all 50 |
| 115 | [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 35 ships, needs mining_laser_i, empty hold, standing work | all 50 |
| 116 | [gather-ironhollow-fading-signal](gather-ironhollow-fading-signal.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 20 ships, needs mining_laser_i, empty hold, standing work | all 50 |
| 117 | [gather-garnet-belt](gather-garnet-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 29 ships, needs mining_laser_i, empty hold, standing work | all 50 |
| 118 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 50 |
| 119 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 50 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [hunter](templates-military.md) | 50 |

Planned:

| What | When |
|---|---|
| Goal: Military's steady money above +15,000 cr an hour over the four hours to the next Military turn (hive.py fleet, the division's net per hour), read at that turn. | next Military turn |
| The second group flight: each member sets its target and closes in; read the kill, the loot and the damage per ship, and give the Fleet Admiral the dispatcher's steps for `group: N`. | next Military turn |
| Read the first RESULT line of the escort route (its one run started 20:33 UTC); no guard or escort in the first ring of outposts and its roads (orders ENT-045): the next escort serves beyond it, at the stations and the outposts past them. | next Military turn |
| Read the first runs of the six far tests of 20:19 UTC (GSC-0035, GSC-0045 cinder-sylphs; GSC-0037, GSC-0042, Sandrift, Yildun hollow-pilgrims); a test that pays gets its herd's one hunter for good. | next Military turn |
| Each turn: reserve_hunts.py and pirate_places.py over both roles; a pirate pack at or one lane from a hunt takes it out of the plans. | every turn |
| Read one drone's Shields and Armor XP before and after a hunt that dents its hull. | next Military turn |
