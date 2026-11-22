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

Kept by Apophis. Routes: 190. Ships: 20.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 20 |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 20 |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 |
| 6 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 20 |
| 7 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 20 |
| 8 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 |
| 9 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 20 |
| 10 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 |
| 11 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 |
| 12 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 20 |
| 13 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 20 |
| 14 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 20 |
| 15 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 20 |
| 16 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 20 |
| 17 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 20 |
| 18 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 20 |
| 19 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 |
| 20 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 |
| 21 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 20 |
| 22 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 20 |
| 23 | [fit-pulse-laser-iii-lhs-1140](fit-pulse-laser-iii-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, up to 3 ships, 20 pilots in all, needs pulse_laser_i, without pulse_laser_iii, empty hold, from 30,000 cr, while 784309214f105860a16a0c100a70eb14 asks 14000 cr or less for pulse_laser_iii | all 20 |
| 24 | [buy-plasma-ammo-central-nexus](buy-plasma-ammo-central-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, 2 pilots in all, needs plasma_cannon_ii, from 15,000 cr, while central_nexus asks 200 cr or less for dispersal_plasma_cell_pack | all 20 |
| 25 | [give-drone-stores-node-beta](give-drone-stores-node-beta.json) | [Off](index-off.md) | home space | up to 3 ships, with 20 copper_ore stored at node_beta_industrial_station, off | all 20 |
| 26 | [give-drone-stores-experiment](give-drone-stores-experiment.json) | [Off](index-off.md) | home space | up to 3 ships, with 20 copper_ore stored at the_experiment_research_station, off | all 20 |
| 27 | [give-drone-stores-synchrony](give-drone-stores-synchrony.json) | [Off](index-off.md) | home space | up to 3 ships, with 20 copper_ore stored at synchrony_hub, off | all 20 |
| 28 | [give-drone-stores-central-nexus](give-drone-stores-central-nexus.json) | [Off](index-off.md) | home space | up to 3 ships, with 20 copper_ore stored at central_nexus, off | all 20 |
| 29 | [give-drone-stores-node-alpha](give-drone-stores-node-alpha.json) | [Off](index-off.md) | home space | up to 2 ships, with 20 nitrogen_ice stored at node_alpha_processing_station, off | all 20 |
| 30 | [give-drone-stores-first-step](give-drone-stores-first-step.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, with 20 creature_carapace stored at first_step_memorial_station, off | all 20 |
| 31 | [give-drone-stores-crucible](give-drone-stores-crucible.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, with 2 ember_gland stored at the_crucible_garrison, off | all 20 |
| 32 | [give-drone-stores-hexstar](give-drone-stores-hexstar.json) | [Off](index-off.md) | beyond the border, 11 jumps | up to 1 ships, with 2 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, off | all 20 |
| 33 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 20 |
| 34 | [hunt-sunbeam-dust-veil-ray](hunt-sunbeam-dust-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 35 | [hunt-thin-breath-haze-veil-ray](hunt-thin-breath-haze-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 36 | [hunt-test-tanglewood-hollow-pilgrim](hunt-test-tanglewood-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 20 |
| 37 | [hunt-rayfall-shimmer-veil-ray](hunt-rayfall-shimmer-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 38 | [hunt-regor-wr-bubble-cinder-sylph](hunt-regor-wr-bubble-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 39 | [hunt-gsc-0035-vapor-fields-cinder-sylph](hunt-gsc-0035-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 20 |
| 40 | [hunt-ran-haze-chlorophage](hunt-ran-haze-chlorophage.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 25 jumps | up to 1 ships, empty hold | 1 of 20 |
| 41 | [hunt-merope-dim-phase-pocket-veil-ray](hunt-merope-dim-phase-pocket-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 42 | [hunt-ankaa-cryobelt-hollow-pilgrim](hunt-ankaa-cryobelt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 20 |
| 43 | [hunt-driftwood-ghost-resonance-veil-ray](hunt-driftwood-ghost-resonance-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 2 of 20 |
| 44 | [hunt-miaplacidus-frost-ring-hollow-pilgrim](hunt-miaplacidus-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 45 | [hunt-relay-station-ice-shelf-hollow-pilgrim](hunt-relay-station-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 46 | [hunt-ashenmoor-ice-shelf-hollow-pilgrim](hunt-ashenmoor-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 17 jumps | up to 1 ships, empty hold | 1 of 20 |
| 47 | [drain-ice-nexus](drain-ice-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | 1 of 20 |
| 48 | [hunt-nightveil-haze-cinder-sylph](hunt-nightveil-haze-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 2 of 20 |
| 49 | [hunt-tania-vapor-fields-cinder-sylph](hunt-tania-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 50 | [hunt-unukalhai-ice-fields-hollow-pilgrim](hunt-unukalhai-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 24 jumps | up to 1 ships, empty hold | 1 of 20 |
| 51 | [hunt-oxbow-ice-belt-frost-moth](hunt-oxbow-ice-belt-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 1 ships, empty hold, standing work | 1 of 20 |
| 52 | [hunt-gsc-0004-gas-pocket-cinder-sylph](hunt-gsc-0004-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 20 |
| 53 | [hunt-cervantes-vapor-fields-halo-drifter](hunt-cervantes-vapor-fields-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 54 | [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | 1 of 20 |
| 55 | [hunt-minkar-cryobelt-hollow-pilgrim](hunt-minkar-cryobelt-hollow-pilgrim.json) | [Off](index-off.md) | beyond the border, 21 jumps | up to 1 ships, empty hold, off | 1 of 20 |
| 56 | [hunt-torcular-frost-ring-hollow-pilgrim](hunt-torcular-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 57 | [hunt-alchiba-ice-belt-hollow-pilgrim](hunt-alchiba-ice-belt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 2 of 20 |
| 58 | [hunt-summervale-gas-pocket-cinder-sylph](hunt-summervale-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 21 jumps | up to 1 ships, empty hold | 1 of 20 |
| 59 | [hunt-tania-frozen-drift-hollow-pilgrim](hunt-tania-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 60 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | 1 of 20 |
| 61 | [hunt-antares-gas-cloud-cinder-sylph](hunt-antares-gas-cloud-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 20 |
| 62 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | 2 of 20 |
| 63 | [hunt-proxima-centauri-frost-ring-hollow-pilgrim](hunt-proxima-centauri-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 64 | [hunt-saltwind-ice-shelf-hollow-pilgrim](hunt-saltwind-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 65 | [hunt-hd-10647-ice-field-frost-moth](hunt-hd-10647-ice-field-frost-moth.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 23 jumps | up to 1 ships, empty hold | 1 of 20 |
| 66 | [hunt-larawag-ice-belt-hollow-pilgrim](hunt-larawag-ice-belt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 20 |
| 67 | [hunt-avior-gas-pocket-halo-drifter](hunt-avior-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 20 |
| 68 | [hunt-biham-ice-shelf-hollow-pilgrim](hunt-biham-ice-shelf-hollow-pilgrim.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, off | 2 of 20 |
| 69 | [hunt-lanternwick-frozen-drift-hollow-pilgrim](hunt-lanternwick-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 70 | [hunt-gsc-0012-gas-plume-halo-drifter](hunt-gsc-0012-gas-plume-halo-drifter.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 2 of 20 |
| 71 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 20 |
| 72 | [hunt-wasat-cryobelt-hollow-pilgrim](hunt-wasat-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 2 of 20 |
| 73 | [hunt-groombridge-1618-frozen-drift-hollow-pilgrim](hunt-groombridge-1618-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 74 | [hunt-avior-cryobelt-hollow-pilgrim](hunt-avior-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 2 of 20 |
| 75 | [hunt-harborlight-ice-shelf-hollow-pilgrim](hunt-harborlight-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 76 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 3 of 20 |
| 77 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 20 |
| 78 | [hunt-alathfar-haze-chlorophage](hunt-alathfar-haze-chlorophage.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 79 | [hunt-fulu-vapor-fields-chlorophage](hunt-fulu-vapor-fields-chlorophage.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 80 | [hunt-chara-gas-plume-chlorophage](hunt-chara-gas-plume-chlorophage.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 81 | [hunt-test-keid-ice-shelf-deuteron-slug-pl3](hunt-test-keid-ice-shelf-deuteron-slug-pl3.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, needs pulse_laser_iii, empty hold, standing work | all 20 |
| 82 | [hunt-test-gsc-0035-belt-b-slag-tortoise-pl3](hunt-test-gsc-0035-belt-b-slag-tortoise-pl3.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, needs pulse_laser_iii, empty hold, standing work | all 20 |
| 83 | [hunt-test-acubens-bulwark-pl3](hunt-test-acubens-bulwark-pl3.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, needs pulse_laser_iii, empty hold, standing work | all 20 |
| 84 | [hunt-test-acubens-bulwark-pc2](hunt-test-acubens-bulwark-pc2.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, needs plasma_cannon_ii, empty hold, standing work | all 20 |
| 85 | [hunt-rasalhague-ice-fields-hollow-pilgrim](hunt-rasalhague-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 86 | [hunt-elnath-ice-belt-hollow-pilgrim](hunt-elnath-ice-belt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 87 | [hunt-gsc-0024-frost-ring-hollow-pilgrim](hunt-gsc-0024-frost-ring-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 88 | [hunt-atria-ice-fields-hollow-pilgrim](hunt-atria-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 89 | [hunt-groombridge-34-ice-fields-hollow-pilgrim](hunt-groombridge-34-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 90 | [hunt-epsilon-eridani-ice-fields-hollow-pilgrim](hunt-epsilon-eridani-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 91 | [hunt-hassaleh-ice-halo-hollow-pilgrim](hunt-hassaleh-ice-halo-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 92 | [hunt-hassaleh-ice-halo-frost-moth](hunt-hassaleh-ice-halo-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 93 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 20 |
| 94 | [hunt-test-bluerift-frost-ring-rime-grazer](hunt-test-bluerift-frost-ring-rime-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 95 | [hunt-schedar-belt-carapace](hunt-schedar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 96 | [hunt-ironhollow-fading-signal-carapace](hunt-ironhollow-fading-signal-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 97 | [hunt-ironhollow-echo-ejecta-carapace](hunt-ironhollow-echo-ejecta-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 98 | [hunt-achernar-belt-carapace](hunt-achernar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 99 | [hunt-okab-belt-carapace](hunt-okab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 100 | [hunt-gj-3470-dewfall-fray-carapace](hunt-gj-3470-dewfall-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 101 | [hunt-keid-belt-carapace](hunt-keid-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 102 | [hunt-achird-belt-carapace](hunt-achird-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 103 | [hunt-gsc-0012-flicker-fray-carapace](hunt-gsc-0012-flicker-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 104 | [hunt-amberfall-belt-carapace](hunt-amberfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 105 | [hunt-gsc-0031-belt-carapace](hunt-gsc-0031-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 106 | [hunt-acrab-thinspace-rubble-carapace](hunt-acrab-thinspace-rubble-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 107 | [hunt-acrab-belt-carapace](hunt-acrab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 108 | [hunt-atlas-gossamer-null-carapace](hunt-atlas-gossamer-null-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 109 | [hunt-gsc-0044-belt-carapace](hunt-gsc-0044-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 110 | [hunt-gsc-0044-forgotten-tailings-carapace](hunt-gsc-0044-forgotten-tailings-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 111 | [hunt-botein-lampglint-rock-carapace](hunt-botein-lampglint-rock-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 112 | [hunt-botein-belt-carapace](hunt-botein-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 113 | [hunt-acrux-belt-carapace](hunt-acrux-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 114 | [hunt-intercrus-sootfall-belt-carapace](hunt-intercrus-sootfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 115 | [hunt-intercrus-belt-carapace](hunt-intercrus-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 116 | [hunt-intercrus-alloy-remnants-carapace](hunt-intercrus-alloy-remnants-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 117 | [hunt-goldcrest-glitterback-scatter-carapace](hunt-goldcrest-glitterback-scatter-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 118 | [hunt-goldcrest-belt-carapace](hunt-goldcrest-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 119 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 20 |
| 120 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 20 |
| 121 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 122 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 123 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 124 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 125 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 126 | [hunt-home-drift-ray](hunt-home-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | all 20 |
| 127 | [hunt-shaula-gas-plume-drift-ray](hunt-shaula-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 128 | [hunt-gsc-0038-vapor-fields-drift-ray](hunt-gsc-0038-vapor-fields-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 129 | [hunt-marfik-emission-nebula-drift-ray](hunt-marfik-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 130 | [hunt-atria-emission-nebula-drift-ray](hunt-atria-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 131 | [hunt-markab-alloy-seam-patina-grazer](hunt-markab-alloy-seam-patina-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 132 | [hunt-harborlight-prospectors-leavings-patina-grazer](hunt-harborlight-prospectors-leavings-patina-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 133 | [hunt-kapteyn-5-belt-patina-grazer](hunt-kapteyn-5-belt-patina-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 134 | [hunt-kapteyn-5-weak-annihilation-zone-patina-grazer](hunt-kapteyn-5-weak-annihilation-zone-patina-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 135 | [hunt-greenplate-drift-patina-grazer](hunt-greenplate-drift-patina-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 136 | [hunt-patience-field-patina-grazer](hunt-patience-field-patina-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 137 | [hunt-aspidiske-belt-patina-grazer](hunt-aspidiske-belt-patina-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 138 | [hunt-giausar-frost-ring-frost-moth](hunt-giausar-frost-ring-frost-moth.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | all 20 |
| 139 | [hunt-etamin-haze-cinder-sylph](hunt-etamin-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | all 20 |
| 140 | [hunt-ridgecrest-ice-shelf-hollow-pilgrim](hunt-ridgecrest-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 141 | [hunt-willowgate-vapor-fields-halo-drifter](hunt-willowgate-vapor-fields-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 17 jumps | up to 1 ships, empty hold | all 20 |
| 142 | [hunt-ancha-haze-halo-drifter](hunt-ancha-haze-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 19 jumps | up to 1 ships, empty hold | all 20 |
| 143 | [hunt-rigel-gas-plume-drift-ray](hunt-rigel-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 144 | [hunt-scheat-haze-drift-ray](hunt-scheat-haze-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 145 | [hunt-chara-gas-plume-drift-ray](hunt-chara-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 146 | [hunt-gsc-0010-gas-pocket-drift-ray](hunt-gsc-0010-gas-pocket-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 147 | [hunt-stillwater-emission-nebula-drift-ray](hunt-stillwater-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, standing work | all 20 |
| 148 | [hunt-gsc-0034-gas-plume-drift-ray](hunt-gsc-0034-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 149 | [hunt-saiph-emission-nebula-drift-ray](hunt-saiph-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 150 | [hunt-lilii-borea-gas-cloud-drift-ray](hunt-lilii-borea-gas-cloud-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 151 | [hunt-wasat-gas-cloud-drift-ray](hunt-wasat-gas-cloud-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 152 | [hunt-gemma-haze-halo-drifter](hunt-gemma-haze-halo-drifter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 153 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland, standing work | all 20 |
| 154 | [hunt-silverbend-emission-nebula-cinder-sylph](hunt-silverbend-emission-nebula-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 155 | [hunt-orphan-nebula-veil-ray](hunt-orphan-nebula-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 156 | [hunt-ironpeak-weak-superposition-veil-ray](hunt-ironpeak-weak-superposition-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 157 | [hunt-elbowroom-veil-veil-ray](hunt-elbowroom-veil-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 158 | [hunt-the-telescope-flicker-field-veil-ray](hunt-the-telescope-flicker-field-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, standing work | all 20 |
| 159 | [hunt-the-telescope-entangled-drift-veil-ray](hunt-the-telescope-entangled-drift-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, standing work | all 20 |
| 160 | [hunt-duskfield-cryobelt-hollow-pilgrim](hunt-duskfield-cryobelt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 161 | [hunt-yed-prior-cryobelt-hollow-pilgrim](hunt-yed-prior-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 162 | [hunt-horizon-phase-drift-veil-ray](hunt-horizon-phase-drift-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, standing work | all 20 |
| 163 | [hunt-ancha-frozen-drift-hollow-pilgrim](hunt-ancha-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 19 jumps | up to 1 ships, empty hold | 1 of 20 |
| 164 | [hunt-tall-tale-nebula-veil-ray](hunt-tall-tale-nebula-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 165 | [hunt-sandrift-ice-fields-hollow-pilgrim](hunt-sandrift-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 166 | [hunt-ashenmoor-ghost-resonance-veil-ray](hunt-ashenmoor-ghost-resonance-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 167 | [hunt-aftermath-haze-veil-ray](hunt-aftermath-haze-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 168 | [hunt-wezen-faint-entanglement-veil-ray](hunt-wezen-faint-entanglement-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 169 | [hunt-errai-faint-entanglement-veil-ray](hunt-errai-faint-entanglement-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 170 | [hunt-edasich-ice-halo-frost-moth](hunt-edasich-ice-halo-frost-moth.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 25 jumps | up to 1 ships, empty hold | 1 of 20 |
| 171 | [hunt-alnair-ice-fields-hollow-pilgrim](hunt-alnair-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 20 |
| 172 | [hunt-ancha-frozen-drift-frost-moth](hunt-ancha-frozen-drift-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 173 | [hunt-alsciaukat-ghost-resonance-veil-ray](hunt-alsciaukat-ghost-resonance-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 174 | [hunt-broadwing-veil-veil-ray](hunt-broadwing-veil-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 175 | [hunt-hollow-light-veil-ray](hunt-hollow-light-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 176 | [hunt-alsciaukat-vapor-fields-cinder-sylph](hunt-alsciaukat-vapor-fields-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 177 | [hunt-alnilam-gas-pocket-halo-drifter](hunt-alnilam-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 2 of 20 |
| 178 | [hunt-gsc-0040-frost-ring-hollow-pilgrim](hunt-gsc-0040-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 20 |
| 179 | [hunt-toi-2257-gas-pocket-cinder-sylph](hunt-toi-2257-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 26 jumps | up to 1 ships, empty hold | 1 of 20 |
| 180 | [hunt-angetenar-gas-pocket-cinder-sylph](hunt-angetenar-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 1 of 20 |
| 181 | [craft-armor-military-experiment](craft-armor-military-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at the_experiment_research_station, standing work | all 20 |
| 182 | [craft-armor-military-node-beta](craft-armor-military-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at node_beta_industrial_station, standing work | all 20 |
| 183 | [craft-armor-military-synchrony-hub](craft-armor-military-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at synchrony_hub, standing work | all 20 |
| 184 | [craft-armor-military-central-nexus](craft-armor-military-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at central_nexus, standing work | all 20 |
| 185 | [craft-steel-military-experiment](craft-steel-military-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 20 |
| 186 | [craft-steel-military-node-beta](craft-steel-military-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 20 |
| 187 | [craft-steel-military-synchrony-hub](craft-steel-military-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at synchrony_hub, standing work | all 20 |
| 188 | [craft-steel-military-central-nexus](craft-steel-military-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at central_nexus, standing work | all 20 |
| 189 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 20 |
| 190 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 20 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [hunter](templates-military.md) | 20 |

Planned:

| What | When |
|---|---|
| Read the first runs of the Plasma Cannon II swap and the three Pulse Laser III tests (bulwark, deuteron slug, slag tortoise); name the division's weapon fit to the Fleet Admiral when both weapons have kills an hour | next turn |
