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

Kept by Apophis. Routes: 153. Ships: 20.

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
| 23 | [hunt-sunbeam-dust-veil-ray](hunt-sunbeam-dust-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 24 | [hunt-thin-breath-haze-veil-ray](hunt-thin-breath-haze-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 25 | [hunt-rayfall-shimmer-veil-ray](hunt-rayfall-shimmer-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 26 | [hunt-gsc-0035-vapor-fields-cinder-sylph](hunt-gsc-0035-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 20 |
| 27 | [hunt-merope-dim-phase-pocket-veil-ray](hunt-merope-dim-phase-pocket-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 28 | [hunt-ankaa-cryobelt-hollow-pilgrim](hunt-ankaa-cryobelt-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 20 |
| 29 | [hunt-errai-faint-entanglement-veil-ray](hunt-errai-faint-entanglement-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 30 | [hunt-edasich-ice-halo-frost-moth](hunt-edasich-ice-halo-frost-moth.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 25 jumps | up to 1 ships, empty hold | 1 of 20 |
| 31 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | 2 of 20 |
| 32 | [hunt-test-tanglewood-hollow-pilgrim](hunt-test-tanglewood-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 20 |
| 33 | [hunt-alnair-ice-fields-hollow-pilgrim](hunt-alnair-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 20 |
| 34 | [hunt-driftwood-ghost-resonance-veil-ray](hunt-driftwood-ghost-resonance-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 2 of 20 |
| 35 | [hunt-horizon-phase-drift-veil-ray](hunt-horizon-phase-drift-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships | 1 of 20 |
| 36 | [hunt-ancha-frozen-drift-hollow-pilgrim](hunt-ancha-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 19 jumps | up to 1 ships, empty hold | 1 of 20 |
| 37 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | 5 of 20 |
| 38 | [hunt-regor-wr-bubble-cinder-sylph](hunt-regor-wr-bubble-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 39 | [hunt-ran-haze-chlorophage](hunt-ran-haze-chlorophage.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 25 jumps | up to 1 ships, empty hold | 1 of 20 |
| 40 | [hunt-miaplacidus-frost-ring-hollow-pilgrim](hunt-miaplacidus-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 41 | [hunt-duskfield-cryobelt-hollow-pilgrim](hunt-duskfield-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 42 | [hunt-yed-prior-cryobelt-hollow-pilgrim](hunt-yed-prior-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 43 | [hunt-relay-station-ice-shelf-hollow-pilgrim](hunt-relay-station-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 44 | [hunt-ashenmoor-ice-shelf-hollow-pilgrim](hunt-ashenmoor-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 17 jumps | up to 1 ships, empty hold | 1 of 20 |
| 45 | [hunt-proxima-centauri-frost-ring-hollow-pilgrim](hunt-proxima-centauri-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 46 | [hunt-alathfar-haze-chlorophage](hunt-alathfar-haze-chlorophage.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 20 |
| 47 | [hunt-nightveil-haze-cinder-sylph](hunt-nightveil-haze-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 2 of 20 |
| 48 | [hunt-tania-vapor-fields-cinder-sylph](hunt-tania-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 49 | [hunt-unukalhai-ice-fields-hollow-pilgrim](hunt-unukalhai-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 24 jumps | up to 1 ships, empty hold | 1 of 20 |
| 50 | [hunt-oxbow-ice-belt-frost-moth](hunt-oxbow-ice-belt-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 1 ships, empty hold, standing work | 1 of 20 |
| 51 | [hunt-gsc-0004-gas-pocket-cinder-sylph](hunt-gsc-0004-gas-pocket-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 20 |
| 52 | [hunt-cervantes-vapor-fields-halo-drifter](hunt-cervantes-vapor-fields-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 53 | [hunt-minkar-cryobelt-hollow-pilgrim](hunt-minkar-cryobelt-hollow-pilgrim.json) | [Off](index-off.md) | beyond the border, 21 jumps | up to 1 ships, empty hold, off | 1 of 20 |
| 54 | [hunt-torcular-frost-ring-hollow-pilgrim](hunt-torcular-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 55 | [hunt-alchiba-ice-belt-hollow-pilgrim](hunt-alchiba-ice-belt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 2 of 20 |
| 56 | [hunt-summervale-gas-pocket-cinder-sylph](hunt-summervale-gas-pocket-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 21 jumps | up to 1 ships, empty hold | 1 of 20 |
| 57 | [hunt-tania-frozen-drift-hollow-pilgrim](hunt-tania-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 58 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | 1 of 20 |
| 59 | [drain-methane-experiment](drain-methane-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 10 methane_ice stored at the_experiment_research_station, while the_experiment_research_station bids 30 cr for methane_ice | 1 of 20 |
| 60 | [hunt-antares-gas-cloud-cinder-sylph](hunt-antares-gas-cloud-cinder-sylph.json) | [Tests](index-tests.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 20 |
| 61 | [hunt-saltwind-ice-shelf-hollow-pilgrim](hunt-saltwind-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 62 | [hunt-hd-10647-ice-field-frost-moth](hunt-hd-10647-ice-field-frost-moth.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 23 jumps | up to 1 ships, empty hold | 1 of 20 |
| 63 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | 1 of 20 |
| 64 | [hunt-larawag-ice-belt-hollow-pilgrim](hunt-larawag-ice-belt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 20 jumps | up to 1 ships, empty hold | 1 of 20 |
| 65 | [hunt-avior-gas-pocket-halo-drifter](hunt-avior-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 20 |
| 66 | [hunt-biham-ice-shelf-hollow-pilgrim](hunt-biham-ice-shelf-hollow-pilgrim.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, off | 2 of 20 |
| 67 | [hunt-alsciaukat-vapor-fields-cinder-sylph](hunt-alsciaukat-vapor-fields-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 2 of 20 |
| 68 | [hunt-alnilam-gas-pocket-halo-drifter](hunt-alnilam-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 2 of 20 |
| 69 | [hunt-gsc-0040-frost-ring-hollow-pilgrim](hunt-gsc-0040-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 20 |
| 70 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | 1 of 20 |
| 71 | [hunt-toi-2257-gas-pocket-cinder-sylph](hunt-toi-2257-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 26 jumps | up to 1 ships, empty hold | 1 of 20 |
| 72 | [hunt-etamin-haze-cinder-sylph](hunt-etamin-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 20 |
| 73 | [hunt-ridgecrest-ice-shelf-hollow-pilgrim](hunt-ridgecrest-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 74 | [hunt-angetenar-gas-pocket-cinder-sylph](hunt-angetenar-gas-pocket-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 1 of 20 |
| 75 | [hunt-lanternwick-frozen-drift-hollow-pilgrim](hunt-lanternwick-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 20 |
| 76 | [hunt-gsc-0012-gas-plume-halo-drifter](hunt-gsc-0012-gas-plume-halo-drifter.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 2 of 20 |
| 77 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 20 |
| 78 | [hunt-wasat-cryobelt-hollow-pilgrim](hunt-wasat-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 2 of 20 |
| 79 | [hunt-groombridge-1618-frozen-drift-hollow-pilgrim](hunt-groombridge-1618-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 80 | [hunt-avior-cryobelt-hollow-pilgrim](hunt-avior-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 2 of 20 |
| 81 | [hunt-harborlight-ice-shelf-hollow-pilgrim](hunt-harborlight-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 20 |
| 82 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 3 of 20 |
| 83 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 20 |
| 84 | [sell-ember-nexus-krynn](sell-ember-nexus-krynn.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 3 ember_gland stored at central_nexus, while crimson_war_citadel bids 5000 cr for ember_gland | all 20 |
| 85 | [sell-ember-node-beta-krynn](sell-ember-node-beta-krynn.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 4 ember_gland stored at node_beta_industrial_station, while crimson_war_citadel bids 5000 cr for ember_gland | all 20 |
| 86 | [sell-ember-hexstar-krynn](sell-ember-hexstar-krynn.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while crimson_war_citadel bids 5000 cr for ember_gland | all 20 |
| 87 | [sell-ember-hexstar-first-step](sell-ember-hexstar-first-step.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while first_step_memorial_station bids 5000 cr for ember_gland | all 20 |
| 88 | [sell-ember-experiment-dheneb](sell-ember-experiment-dheneb.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at the_experiment_research_station, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 20 |
| 89 | [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 20 |
| 90 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | all 20 |
| 91 | [sell-melt-nexus-sirius](sell-melt-nexus-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at central_nexus, while sirius_observatory_station bids 1000 cr for crystal_melt | all 20 |
| 92 | [sell-melt-experiment-sirius](sell-melt-experiment-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at the_experiment_research_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 20 |
| 93 | [sell-melt-node-beta-sirius](sell-melt-node-beta-sirius.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at node_beta_industrial_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 20 |
| 94 | [sell-melt-synchrony-sirius](sell-melt-synchrony-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at synchrony_hub, while sirius_observatory_station bids 1000 cr for crystal_melt | all 20 |
| 95 | [sell-melt-at-sirius](sell-melt-at-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 1 crystal_melt stored at sirius_observatory_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 20 |
| 96 | [hunt-rasalhague-ice-fields-hollow-pilgrim](hunt-rasalhague-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 20 |
| 97 | [hunt-elnath-ice-belt-hollow-pilgrim](hunt-elnath-ice-belt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 20 |
| 98 | [hunt-gsc-0024-frost-ring-hollow-pilgrim](hunt-gsc-0024-frost-ring-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 20 |
| 99 | [hunt-atria-ice-fields-hollow-pilgrim](hunt-atria-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 20 |
| 100 | [hunt-groombridge-34-ice-fields-hollow-pilgrim](hunt-groombridge-34-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt, standing work | all 20 |
| 101 | [hunt-epsilon-eridani-ice-fields-hollow-pilgrim](hunt-epsilon-eridani-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt | all 20 |
| 102 | [hunt-hassaleh-ice-halo-hollow-pilgrim](hunt-hassaleh-ice-halo-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, while sirius_observatory_station bids 1000 cr for crystal_melt | all 20 |
| 103 | [hunt-hassaleh-ice-halo-frost-moth](hunt-hassaleh-ice-halo-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | all 20 |
| 104 | [hunt-gemma-haze-halo-drifter](hunt-gemma-haze-halo-drifter.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | all 20 |
| 105 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 20 |
| 106 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 20 |
| 107 | [hunt-test-bluerift-frost-ring-rime-grazer](hunt-test-bluerift-frost-ring-rime-grazer.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 108 | [hunt-schedar-belt-carapace](hunt-schedar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 109 | [hunt-ironhollow-fading-signal-carapace](hunt-ironhollow-fading-signal-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 110 | [hunt-ironhollow-echo-ejecta-carapace](hunt-ironhollow-echo-ejecta-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 111 | [hunt-achernar-belt-carapace](hunt-achernar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 112 | [hunt-okab-belt-carapace](hunt-okab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 113 | [hunt-gj-3470-dewfall-fray-carapace](hunt-gj-3470-dewfall-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 114 | [hunt-keid-belt-carapace](hunt-keid-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 115 | [hunt-achird-belt-carapace](hunt-achird-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 116 | [hunt-gsc-0012-flicker-fray-carapace](hunt-gsc-0012-flicker-fray-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 117 | [hunt-amberfall-belt-carapace](hunt-amberfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 118 | [hunt-gsc-0031-belt-carapace](hunt-gsc-0031-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 119 | [hunt-acrab-thinspace-rubble-carapace](hunt-acrab-thinspace-rubble-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 120 | [hunt-acrab-belt-carapace](hunt-acrab-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 121 | [hunt-atlas-gossamer-null-carapace](hunt-atlas-gossamer-null-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 122 | [hunt-gsc-0044-belt-carapace](hunt-gsc-0044-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 123 | [hunt-gsc-0044-forgotten-tailings-carapace](hunt-gsc-0044-forgotten-tailings-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 124 | [hunt-botein-lampglint-rock-carapace](hunt-botein-lampglint-rock-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 125 | [hunt-botein-belt-carapace](hunt-botein-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 126 | [hunt-acrux-belt-carapace](hunt-acrux-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 127 | [hunt-intercrus-sootfall-belt-carapace](hunt-intercrus-sootfall-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 128 | [hunt-intercrus-belt-carapace](hunt-intercrus-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 129 | [hunt-intercrus-alloy-remnants-carapace](hunt-intercrus-alloy-remnants-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 130 | [hunt-goldcrest-glitterback-scatter-carapace](hunt-goldcrest-glitterback-scatter-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 131 | [hunt-goldcrest-belt-carapace](hunt-goldcrest-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 132 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 20 |
| 133 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | all 20 |
| 134 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 135 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 136 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 137 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 138 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 139 | [hunt-home-drift-ray](hunt-home-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | all 20 |
| 140 | [hunt-shaula-gas-plume-drift-ray](hunt-shaula-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 141 | [hunt-gsc-0038-vapor-fields-drift-ray](hunt-gsc-0038-vapor-fields-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 142 | [hunt-marfik-emission-nebula-drift-ray](hunt-marfik-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 143 | [hunt-atria-emission-nebula-drift-ray](hunt-atria-emission-nebula-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | all 20 |
| 144 | [craft-armor-military-experiment](craft-armor-military-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at the_experiment_research_station, standing work | all 20 |
| 145 | [craft-armor-military-node-beta](craft-armor-military-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at node_beta_industrial_station, standing work | all 20 |
| 146 | [craft-armor-military-synchrony-hub](craft-armor-military-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at synchrony_hub, standing work | all 20 |
| 147 | [craft-armor-military-central-nexus](craft-armor-military-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 30 creature_carapace stored at central_nexus, standing work | all 20 |
| 148 | [craft-steel-military-experiment](craft-steel-military-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 20 |
| 149 | [craft-steel-military-node-beta](craft-steel-military-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 20 |
| 150 | [craft-steel-military-synchrony-hub](craft-steel-military-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at synchrony_hub, standing work | all 20 |
| 151 | [craft-steel-military-central-nexus](craft-steel-military-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at central_nexus, standing work | all 20 |
| 152 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 20 |
| 153 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 20 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [hunter](templates-military.md) | 20 |

Planned:

| What | When |
|---|---|
| Goal: Military's steady money above 0 cr an hour over the four hours to the next Military turn (hive.py fleet, the division's net per hour), read at that turn; the last turn's goal of +15,000 was missed (iron fallback, errors.log ENT-108). | next Military turn |
| Read the first RESULT lines of the four ember-gland sales (Krynn 7,400 x 24, First Step 5,686 x 57); when Krynn's bid is filled, the stores go to First Step. | next Military turn |
| Read the crafts from own stores (armor plate, steel plate): plates made, visits the stores carry, ships that dock for want of stores; add hunts, never gather routes. | next Military turn |
| The group: read the third flight's record (own dist, close to 2) and give the Fleet Admiral the dispatcher's steps for `group: N`. | next Military turn |
| Each turn: reserve_hunts.py, pirate_places.py, loot_bids.py against every sale route's bid base, and the holders of each once-chain link. | every turn |
