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

Kept by Unity. Routes: 60. Ships: 6.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 6 |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 6 |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 6 |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 6 |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 6 |
| 6 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 6 |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 6 |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 6 |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | [Off](index-off.md) | home space | once per pilot, up to 2 ships, off | all 6 |
| 10 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 6 |
| 11 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 6 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 15 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 6 |
| 16 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 6 |
| 17 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 6 |
| 18 | [hunt-ashenmoor-ghost-resonance-veil-ray](hunt-ashenmoor-ghost-resonance-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | 1 of 6 |
| 19 | [hunt-hd-10647-ice-field-frost-moth](hunt-hd-10647-ice-field-frost-moth.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 23 jumps | up to 1 ships, empty hold | 1 of 6 |
| 20 | [hunt-the-telescope-flicker-field-veil-ray](hunt-the-telescope-flicker-field-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, standing work | 1 of 6 |
| 21 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 3 ships | 1 of 6 |
| 22 | [hunt-flintrock-vapor-fields-cinder-sylph](hunt-flintrock-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 3 ships, empty hold | 1 of 6 |
| 23 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 3 ships | 1 of 6 |
| 24 | [mission-voidborn-trajectory-unknown](mission-voidborn-trajectory-unknown.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 16 jumps | once per pilot, up to 3 ships | 2 of 6 |
| 25 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | 1 of 6 |
| 26 | [hunt-alchiba-ice-belt-hollow-pilgrim](hunt-alchiba-ice-belt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 14 jumps | up to 1 ships, empty hold | 1 of 6 |
| 27 | [hunt-regor-wr-bubble-cinder-sylph](hunt-regor-wr-bubble-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 2 of 6 |
| 28 | [hunt-the-quiet-shimmer-veil-ray](hunt-the-quiet-shimmer-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 6 |
| 29 | [hunt-wasat-cryobelt-hollow-pilgrim](hunt-wasat-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 6 |
| 30 | [hunt-etamin-haze-cinder-sylph](hunt-etamin-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 6 |
| 31 | [hunt-harborlight-ice-shelf-hollow-pilgrim](hunt-harborlight-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 6 |
| 32 | [hunt-gsc-0040-frost-ring-hollow-pilgrim](hunt-gsc-0040-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 2 of 6 |
| 33 | [hunt-gsc-0012-gas-plume-cinder-sylph](hunt-gsc-0012-gas-plume-cinder-sylph.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 6 |
| 34 | [hunt-alnilam-gas-pocket-halo-drifter](hunt-alnilam-gas-pocket-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 6 |
| 35 | [hunt-avior-cryobelt-hollow-pilgrim](hunt-avior-cryobelt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 2 of 6 |
| 36 | [hunt-aldhibah-ice-shelf-hollow-pilgrim](hunt-aldhibah-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 12 jumps | up to 1 ships, empty hold | 1 of 6 |
| 37 | [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 6 |
| 38 | [hunt-the-dim-lantern-veil-ray](hunt-the-dim-lantern-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 29 jumps | up to 1 ships, empty hold | 1 of 6 |
| 39 | [hunt-tania-vapor-fields-cinder-sylph](hunt-tania-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, empty hold | 1 of 6 |
| 40 | [hunt-angetenar-gas-pocket-cinder-sylph](hunt-angetenar-gas-pocket-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 13 jumps | up to 1 ships, empty hold | 1 of 6 |
| 41 | [hunt-ridgecrest-ice-shelf-hollow-pilgrim](hunt-ridgecrest-ice-shelf-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 6 |
| 42 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | 1 of 6 |
| 43 | [hunt-propus-ice-belt-hollow-pilgrim](hunt-propus-ice-belt-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 15 jumps | up to 3 ships, empty hold | 1 of 6 |
| 44 | [hunt-taygeta-frozen-drift-hollow-pilgrim](hunt-taygeta-frozen-drift-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 15 jumps | up to 3 ships, empty hold | 1 of 6 |
| 45 | [hunt-titawin-gas-cloud-chlorophage](hunt-titawin-gas-cloud-chlorophage.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | 1 of 6 |
| 46 | [hunt-silverbend-emission-nebula-cinder-sylph](hunt-silverbend-emission-nebula-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | 2 of 6 |
| 47 | [hunt-cervantes-vapor-fields-halo-drifter](hunt-cervantes-vapor-fields-halo-drifter.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 6 |
| 48 | [hunt-fulu-vapor-fields-cinder-sylph](hunt-fulu-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 6 |
| 49 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 6 |
| 50 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 6 |
| 51 | [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 |
| 52 | [hunt-deepwell-haze-cinder-sylph](hunt-deepwell-haze-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 7 jumps | up to 1 ships, empty hold | all 6 |
| 53 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | all 6 |
| 54 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 6 |
| 55 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 6 |
| 56 | [give-miner-stores-central-nexus](give-miner-stores-central-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 3 ships, with 50 iron_ore stored at central_nexus | all 6 |
| 57 | [give-miner-stores-node-beta](give-miner-stores-node-beta.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 3 ships, with 50 iron_ore stored at node_beta_industrial_station | all 6 |
| 58 | [give-drone-stores-central-nexus](give-drone-stores-central-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 20 copper_ore stored at central_nexus | all 6 |
| 59 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 6 |
| 60 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 6 |
