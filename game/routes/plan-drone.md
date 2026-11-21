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

Kept by Apophis. Routes: 175. Ships: 50.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 50 |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 50 |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 50 |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 50 |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 50 |
| 6 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 50 |
| 7 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 50 |
| 8 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 |
| 9 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 50 |
| 10 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 11 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 12 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 50 |
| 13 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 50 |
| 14 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 50 |
| 15 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 50 |
| 16 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 50 |
| 17 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 50 |
| 18 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 50 |
| 19 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 |
| 20 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 21 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 50 |
| 22 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 50 |
| 23 | [hunt-rigel-gas-plume-drift-ray](hunt-rigel-gas-plume-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 24 | [hunt-giausar-frost-ring-frost-moth](hunt-giausar-frost-ring-frost-moth.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 50 |
| 25 | [hunt-silverbend-emission-nebula-cinder-sylph](hunt-silverbend-emission-nebula-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 26 | [hunt-dawnbreak-frozen-drift-hollow-pilgrim](hunt-dawnbreak-frozen-drift-hollow-pilgrim.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 27 | [hunt-superposition-pocket-veil-ray](hunt-superposition-pocket-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships | 1 of 50 |
| 28 | [hunt-ironpeak-weak-superposition-veil-ray](hunt-ironpeak-weak-superposition-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 29 | [hunt-minkar-cryobelt-hollow-pilgrim](hunt-minkar-cryobelt-hollow-pilgrim.json) | [Tests](index-tests.md) | beyond the border, 21 jumps | up to 1 ships, empty hold | 1 of 50 |
| 30 | [hunt-elbowroom-veil-veil-ray](hunt-elbowroom-veil-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 19 jumps | up to 1 ships, empty hold | 1 of 50 |
| 31 | [hunt-alphecca-vapor-fields-cinder-sylph](hunt-alphecca-vapor-fields-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 32 | [hunt-lilii-borea-gas-cloud-drift-ray](hunt-lilii-borea-gas-cloud-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 33 | [hunt-the-telescope-flicker-field-veil-ray](hunt-the-telescope-flicker-field-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships | 1 of 50 |
| 34 | [hunt-the-telescope-entangled-drift-veil-ray](hunt-the-telescope-entangled-drift-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships | 1 of 50 |
| 35 | [hunt-duskfield-cryobelt-hollow-pilgrim](hunt-duskfield-cryobelt-hollow-pilgrim.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 36 | [hunt-horizon-phase-drift-veil-ray](hunt-horizon-phase-drift-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships | 1 of 50 |
| 37 | [hunt-nightveil-haze-cinder-sylph](hunt-nightveil-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 38 | [hunt-enif-ice-belt-hollow-pilgrim](hunt-enif-ice-belt-hollow-pilgrim.json) | [Tests](index-tests.md) | beyond the border, 25 jumps | up to 1 ships, empty hold | 1 of 50 |
| 39 | [hunt-torcular-frost-ring-hollow-pilgrim](hunt-torcular-frost-ring-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 40 | [hunt-scheat-haze-drift-ray](hunt-scheat-haze-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 41 | [hunt-chara-gas-plume-drift-ray](hunt-chara-gas-plume-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 42 | [hunt-etamin-haze-cinder-sylph](hunt-etamin-haze-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 43 | [hunt-tall-tale-nebula-veil-ray](hunt-tall-tale-nebula-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 44 | [hunt-gsc-0010-gas-pocket-drift-ray](hunt-gsc-0010-gas-pocket-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 17 jumps | up to 1 ships, empty hold | 1 of 50 |
| 45 | [hunt-tureis-vapor-fields-bell-jelly](hunt-tureis-vapor-fields-bell-jelly.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 46 | [hunt-summervale-gas-pocket-cinder-sylph](hunt-summervale-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 21 jumps | up to 1 ships, empty hold | 1 of 50 |
| 47 | [hunt-wasat-gas-cloud-drift-ray](hunt-wasat-gas-cloud-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 48 | [hunt-yildun-outer-ice-hollow-pilgrim](hunt-yildun-outer-ice-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 49 | [hunt-gsc-0034-gas-plume-drift-ray](hunt-gsc-0034-gas-plume-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 50 | [hunt-test-acubens-bulwark-pl3](hunt-test-acubens-bulwark-pl3.json) | [Tests](index-tests.md) | home space | up to 1 ships, needs pulse_laser_iii, empty hold | 1 of 50 |
| 51 | [hunt-alsciaukat-vapor-fields-cinder-sylph](hunt-alsciaukat-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 2 of 50 |
| 52 | [hunt-willowgate-vapor-fields-halo-drifter](hunt-willowgate-vapor-fields-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 17 jumps | up to 1 ships, empty hold | 1 of 50 |
| 53 | [hunt-merak-dim-phase-pocket-veil-ray](hunt-merak-dim-phase-pocket-veil-ray.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, off | 1 of 50 |
| 54 | [hunt-saltwind-gas-pocket-halo-drifter](hunt-saltwind-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 55 | [hunt-sandrift-ice-fields-hollow-pilgrim](hunt-sandrift-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 56 | [hunt-ashenmoor-ghost-resonance-veil-ray](hunt-ashenmoor-ghost-resonance-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 57 | [hunt-gsc-0042-ice-shelf-hollow-pilgrim](hunt-gsc-0042-ice-shelf-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 2 of 50 |
| 58 | [hunt-stillwater-emission-nebula-drift-ray](hunt-stillwater-emission-nebula-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 19 jumps | up to 1 ships | 1 of 50 |
| 59 | [hunt-aftermath-haze-veil-ray](hunt-aftermath-haze-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 60 | [hunt-lilii-borea-gas-cloud-bell-jelly](hunt-lilii-borea-gas-cloud-bell-jelly.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 61 | [hunt-wezen-faint-entanglement-veil-ray](hunt-wezen-faint-entanglement-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 62 | [hunt-edasich-ice-halo-frost-moth](hunt-edasich-ice-halo-frost-moth.json) | [Tests](index-tests.md) | beyond the border, 25 jumps | up to 1 ships, empty hold | 1 of 50 |
| 63 | [hunt-errai-faint-entanglement-veil-ray](hunt-errai-faint-entanglement-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 64 | [hunt-veritate-emission-nebula-halo-drifter](hunt-veritate-emission-nebula-halo-drifter.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 65 | [hunt-ancha-frozen-drift-frost-moth](hunt-ancha-frozen-drift-frost-moth.json) | [Tests](index-tests.md) | beyond the border, 19 jumps | up to 1 ships, empty hold | 1 of 50 |
| 66 | [hunt-gsc-0037-frost-ring-hollow-pilgrim](hunt-gsc-0037-frost-ring-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 67 | [hunt-edgeward-glow-veil-ray](hunt-edgeward-glow-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 21 jumps | up to 1 ships, empty hold | 1 of 50 |
| 68 | [hunt-unukalhai-ice-fields-hollow-pilgrim](hunt-unukalhai-ice-fields-hollow-pilgrim.json) | [Tests](index-tests.md) | beyond the border, 24 jumps | up to 1 ships, empty hold | 1 of 50 |
| 69 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | 3 of 50 |
| 70 | [hunt-gsc-0040-frost-ring-hollow-pilgrim](hunt-gsc-0040-frost-ring-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 50 |
| 71 | [hunt-gsc-0035-vapor-fields-cinder-sylph](hunt-gsc-0035-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 72 | [hunt-askance-nebula-veil-ray](hunt-askance-nebula-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 50 |
| 73 | [hunt-ancha-haze-halo-drifter](hunt-ancha-haze-halo-drifter.json) | [Tests](index-tests.md) | beyond the border, 19 jumps | up to 1 ships, empty hold | 1 of 50 |
| 74 | [hunt-dustfall-emission-nebula-cinder-sylph](hunt-dustfall-emission-nebula-cinder-sylph.json) | [Off](index-off.md) | beyond the border, 27 jumps | up to 1 ships, empty hold, off | 1 of 50 |
| 75 | [hunt-lurker-veil-veil-ray](hunt-lurker-veil-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 76 | [hunt-saiph-emission-nebula-drift-ray](hunt-saiph-emission-nebula-drift-ray.json) | [Tests](index-tests.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 77 | [hunt-denebola-fractured-prism-veil-ray](hunt-denebola-fractured-prism-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 50 |
| 78 | [hunt-silverpine-gas-plume-cinder-sylph](hunt-silverpine-gas-plume-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 24 jumps | up to 1 ships, empty hold | 1 of 50 |
| 79 | [hunt-alchiba-ice-belt-hollow-pilgrim](hunt-alchiba-ice-belt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 50 |
| 80 | [hunt-alsciaukat-ghost-resonance-veil-ray](hunt-alsciaukat-ghost-resonance-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 81 | [hunt-seginus-haze-cinder-sylph](hunt-seginus-haze-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 82 | [hunt-alathfar-haze-chlorophage](hunt-alathfar-haze-chlorophage.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 50 |
| 83 | [hunt-alsciaukat-faint-entanglement-veil-ray](hunt-alsciaukat-faint-entanglement-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 84 | [hunt-gsc-0045-gas-pocket-cinder-sylph](hunt-gsc-0045-gas-pocket-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 50 |
| 85 | [hunt-harborlight-ice-shelf-hollow-pilgrim](hunt-harborlight-ice-shelf-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 50 |
| 86 | [hunt-merope-gas-plume-cinder-sylph](hunt-merope-gas-plume-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 87 | [hunt-coinflip-nebula-veil-ray](hunt-coinflip-nebula-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 88 | [hunt-menkib-stellar-wind-cinder-sylph](hunt-menkib-stellar-wind-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 89 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | 6 of 50 |
| 90 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | 5 of 50 |
| 91 | [hunt-arneb-gas-pocket-drift-ray](hunt-arneb-gas-pocket-drift-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 16 jumps | up to 1 ships, empty hold | 1 of 50 |
| 92 | [hunt-angetenar-gas-pocket-cinder-sylph](hunt-angetenar-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 1 of 50 |
| 93 | [hunt-oxbow-ice-belt-frost-moth](hunt-oxbow-ice-belt-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 1 ships, empty hold, standing work | 2 of 50 |
| 94 | [hunt-avior-gas-pocket-halo-drifter](hunt-avior-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 2 of 50 |
| 95 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 2 of 50 |
| 96 | [hunt-hd-10647-ice-field-frost-moth](hunt-hd-10647-ice-field-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 23 jumps | up to 1 ships, empty hold | 2 of 50 |
| 97 | [hunt-broadwing-veil-veil-ray](hunt-broadwing-veil-veil-ray.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 98 | [hunt-violethall-gas-plume-cinder-sylph](hunt-violethall-gas-plume-cinder-sylph.json) | [Off](index-off.md) | beyond the border, 17 jumps | up to 1 ships, empty hold, off | 1 of 50 |
| 99 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | 8 of 50 |
| 100 | [hunt-tania-vapor-fields-cinder-sylph](hunt-tania-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 50 |
| 101 | [hunt-biham-ice-shelf-hollow-pilgrim](hunt-biham-ice-shelf-hollow-pilgrim.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, off | 1 of 50 |
| 102 | [hunt-gsc-0012-gas-plume-halo-drifter](hunt-gsc-0012-gas-plume-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 50 |
| 103 | [hunt-wasat-cryobelt-hollow-pilgrim](hunt-wasat-cryobelt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 50 |
| 104 | [hunt-avior-cryobelt-hollow-pilgrim](hunt-avior-cryobelt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 50 |
| 105 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 50 |
| 106 | [sell-ember-nexus-krynn](sell-ember-nexus-krynn.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 3 ember_gland stored at central_nexus, while crimson_war_citadel bids 5000 cr for ember_gland | all 50 |
| 107 | [sell-ember-node-beta-krynn](sell-ember-node-beta-krynn.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, with 4 ember_gland stored at node_beta_industrial_station, while crimson_war_citadel bids 5000 cr for ember_gland | all 50 |
| 108 | [sell-ember-hexstar-krynn](sell-ember-hexstar-krynn.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while crimson_war_citadel bids 5000 cr for ember_gland | all 50 |
| 109 | [sell-ember-hexstar-first-step](sell-ember-hexstar-first-step.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while first_step_memorial_station bids 5000 cr for ember_gland | all 50 |
| 110 | [sell-ember-experiment-dheneb](sell-ember-experiment-dheneb.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at the_experiment_research_station, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 111 | [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 112 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | all 50 |
| 113 | [sell-melt-nexus-sirius](sell-melt-nexus-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at central_nexus, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 114 | [sell-melt-experiment-sirius](sell-melt-experiment-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at the_experiment_research_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 115 | [sell-melt-node-beta-sirius](sell-melt-node-beta-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at node_beta_industrial_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 116 | [sell-melt-synchrony-sirius](sell-melt-synchrony-sirius.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at synchrony_hub, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 117 | [sell-melt-at-sirius](sell-melt-at-sirius.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, with 1 crystal_melt stored at sirius_observatory_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 118 | [hunt-rasalhague-ice-fields-hollow-pilgrim](hunt-rasalhague-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 119 | [hunt-elnath-ice-belt-hollow-pilgrim](hunt-elnath-ice-belt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 120 | [hunt-gsc-0024-frost-ring-hollow-pilgrim](hunt-gsc-0024-frost-ring-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 121 | [hunt-atria-ice-fields-hollow-pilgrim](hunt-atria-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 122 | [hunt-groombridge-34-ice-fields-hollow-pilgrim](hunt-groombridge-34-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 50 |
| 123 | [hunt-epsilon-eridani-ice-fields-hollow-pilgrim](hunt-epsilon-eridani-ice-fields-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 124 | [hunt-hassaleh-ice-halo-hollow-pilgrim](hunt-hassaleh-ice-halo-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt | all 50 |
| 125 | [hunt-hassaleh-ice-halo-frost-moth](hunt-hassaleh-ice-halo-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 50 |
| 126 | [hunt-gemma-haze-halo-drifter](hunt-gemma-haze-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | all 50 |
| 127 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 128 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 50 |
| 129 | [hunt-test-bluerift-frost-ring-rime-grazer](hunt-test-bluerift-frost-ring-rime-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 130 | [hunt-schedar-belt-carapace](hunt-schedar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 131 | [hunt-ironhollow-fading-signal-carapace](hunt-ironhollow-fading-signal-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 132 | [hunt-ironhollow-echo-ejecta-carapace](hunt-ironhollow-echo-ejecta-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 133 | [hunt-achernar-belt-carapace](hunt-achernar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 134 | [hunt-okab-belt-carapace](hunt-okab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 135 | [hunt-gj-3470-dewfall-fray-carapace](hunt-gj-3470-dewfall-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 136 | [hunt-keid-belt-carapace](hunt-keid-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 137 | [hunt-achird-belt-carapace](hunt-achird-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 138 | [hunt-gsc-0012-flicker-fray-carapace](hunt-gsc-0012-flicker-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 139 | [hunt-amberfall-belt-carapace](hunt-amberfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 140 | [hunt-gsc-0031-belt-carapace](hunt-gsc-0031-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 141 | [hunt-acrab-thinspace-rubble-carapace](hunt-acrab-thinspace-rubble-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 142 | [hunt-acrab-belt-carapace](hunt-acrab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 143 | [hunt-atlas-gossamer-null-carapace](hunt-atlas-gossamer-null-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 144 | [hunt-gsc-0044-belt-carapace](hunt-gsc-0044-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 145 | [hunt-gsc-0044-forgotten-tailings-carapace](hunt-gsc-0044-forgotten-tailings-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 146 | [hunt-botein-lampglint-rock-carapace](hunt-botein-lampglint-rock-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 147 | [hunt-botein-belt-carapace](hunt-botein-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 148 | [hunt-acrux-belt-carapace](hunt-acrux-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 149 | [hunt-intercrus-sootfall-belt-carapace](hunt-intercrus-sootfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 150 | [hunt-intercrus-belt-carapace](hunt-intercrus-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 151 | [hunt-intercrus-alloy-remnants-carapace](hunt-intercrus-alloy-remnants-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 152 | [hunt-goldcrest-glitterback-scatter-carapace](hunt-goldcrest-glitterback-scatter-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 153 | [hunt-goldcrest-belt-carapace](hunt-goldcrest-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 154 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 50 |
| 155 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 50 |
| 156 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 157 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 158 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 159 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 160 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 161 | [hunt-home-drift-ray](hunt-home-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | all 50 |
| 162 | [hunt-shaula-gas-plume-drift-ray](hunt-shaula-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 163 | [hunt-gsc-0038-vapor-fields-drift-ray](hunt-gsc-0038-vapor-fields-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 164 | [hunt-marfik-emission-nebula-drift-ray](hunt-marfik-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 165 | [hunt-atria-emission-nebula-drift-ray](hunt-atria-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 50 |
| 166 | [craft-armor-military-experiment](craft-armor-military-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at the_experiment_research_station, standing work | all 50 |
| 167 | [craft-armor-military-node-beta](craft-armor-military-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at node_beta_industrial_station, standing work | all 50 |
| 168 | [craft-armor-military-synchrony-hub](craft-armor-military-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at synchrony_hub, standing work | all 50 |
| 169 | [craft-armor-military-central-nexus](craft-armor-military-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at central_nexus, standing work | all 50 |
| 170 | [craft-steel-military-experiment](craft-steel-military-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 50 |
| 171 | [craft-steel-military-node-beta](craft-steel-military-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 50 |
| 172 | [craft-steel-military-synchrony-hub](craft-steel-military-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at synchrony_hub, standing work | all 50 |
| 173 | [craft-steel-military-central-nexus](craft-steel-military-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at central_nexus, standing work | all 50 |
| 174 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 50 |
| 175 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 50 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [hunter](templates-military.md) | 50 |

Planned:

| What | When |
|---|---|
| Goal: Military's steady money above 0 cr an hour over the four hours to the next Military turn (hive.py fleet, the division's net per hour), read at that turn; the last turn's goal of +15,000 was missed (iron fallback, errors.log ENT-108). | next Military turn |
| Read the first RESULT lines of the four ember-gland sales (Krynn 7,400 x 24, First Step 5,686 x 57); when Krynn's bid is filled, the stores go to First Step. | next Military turn |
| Read the crafts from own stores (armor plate, steel plate): plates made, visits the stores carry, ships that dock for want of stores; add hunts, never gather routes. | next Military turn |
| The group: read the third flight's record (own dist, close to 2) and give the Fleet Admiral the dispatcher's steps for `group: N`. | next Military turn |
| Each turn: reserve_hunts.py, pirate_places.py, loot_bids.py against every sale route's bid base, and the holders of each once-chain link. | every turn |
