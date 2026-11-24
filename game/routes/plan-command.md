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

Kept by Unity. Routes: 88. Ships: 9.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 9 |
| 2 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 9 |
| 3 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 9 |
| 4 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 9 |
| 5 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 9 |
| 6 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 9 |
| 7 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 9 |
| 8 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 9 |
| 9 | [voidborn-first-steps](voidborn-first-steps.json) | [Off](index-off.md) | home space | once per pilot, up to 2 ships, off | all 9 |
| 10 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 9 |
| 11 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 9 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 9 |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 9 |
| 14 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 9 |
| 15 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 9 |
| 16 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 9 |
| 17 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 9 |
| 18 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 9 |
| 19 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 9 |
| 20 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 9 |
| 21 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 9 |
| 22 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 9 |
| 23 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 9 |
| 24 | [mission-the-memorial-frontier](mission-the-memorial-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 15 ships | all 9 |
| 25 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 9 |
| 26 | [mission-the-objection-deep](mission-the-objection-deep.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 9 |
| 27 | [mission-a-word-in-private-grand](mission-a-word-in-private-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 5 ships, born nebula | all 9 |
| 28 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 9 |
| 29 | [mission-last-known-position-crimson](mission-last-known-position-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 15 ships | all 9 |
| 30 | [mission-welcome-sol-central](mission-welcome-sol-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 3 ships, born solarian | all 9 |
| 31 | [mission-scraping-by-frontier](mission-scraping-by-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 17 jumps | once per pilot, up to 1 ships, empty hold, born outerrim | all 9 |
| 32 | [mission-filed-in-triplicate-nova](mission-filed-in-triplicate-nova.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 40 ships | all 9 |
| 33 | [join-krynn-trader](join-krynn-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 15 ships, empty hold, born voidborn, standing work | all 9 |
| 34 | [mission-strategic-readiness-assessment-crimson](mission-strategic-readiness-assessment-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 30 ships | all 9 |
| 35 | [mission-structural-reinforcement-alpha](mission-structural-reinforcement-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 20 ships, empty hold | all 9 |
| 36 | [strip-mining-laser-krynn](strip-mining-laser-krynn.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 9 |
| 37 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | all 9 |
| 38 | [mission-blood-forge-requisition-krynn](mission-blood-forge-requisition-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 36 ships, empty hold | all 9 |
| 39 | [mission-request-for-records-confederacy](mission-request-for-records-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 8 ships | all 9 |
| 40 | [mission-70d9950c762ac17eeedfc9a292ed07ac-central](mission-70d9950c762ac17eeedfc9a292ed07ac-central.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 3 ships | 1 of 9 |
| 41 | [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 1 of 9 |
| 42 | [mission-first-links-store-grand](mission-first-links-store-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 8 ships, from 4,300 cr, born nebula | 1 of 9 |
| 43 | [hunt-harborlight-gas-cloud-drift-ray](hunt-harborlight-gas-cloud-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | 1 of 9 |
| 44 | [join-sol-command](join-sol-command.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 2 ships, standing work | 3 of 9 |
| 45 | [hunt-gsc-0038-vapor-fields-drift-ray](hunt-gsc-0038-vapor-fields-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 2 of 9 |
| 46 | [mission-crimson-wreckage-synchrony](mission-crimson-wreckage-synchrony.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | 2 of 9 |
| 47 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 2 of 9 |
| 48 | [hunt-achernar-belt-carapace](hunt-achernar-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 2 of 9 |
| 49 | [hunt-aldhibah-ice-shelf-hollow-pilgrim](hunt-aldhibah-ice-shelf-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | 2 of 9 |
| 50 | [mission-83d4aab496f36cd12fbed259b3f534bf-central](mission-83d4aab496f36cd12fbed259b3f534bf-central.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 3 ships | 6 of 9 |
| 51 | [home-sol-central](home-sol-central.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 6 ships, empty hold, born solarian, standing work | 1 of 9 |
| 52 | [store-hold-grand-exchange](store-hold-grand-exchange.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 35 ships, goods aboard, born nebula, standing work | 1 of 9 |
| 53 | [mission-market-participation-grand](mission-market-participation-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships, from 3,200 cr, while grand_exchange_station bids 1 cr for liquid_nitrogen | 1 of 9 |
| 54 | [hunt-flintrock-vapor-fields-cinder-sylph](hunt-flintrock-vapor-fields-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 3 ships, empty hold, standing work | 5 of 9 |
| 55 | [hunt-gsc-0012-gas-plume-halo-drifter](hunt-gsc-0012-gas-plume-halo-drifter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, empty hold, standing work | 1 of 9 |
| 56 | [hunt-shaula-gas-plume-drift-ray](hunt-shaula-gas-plume-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 1 of 9 |
| 57 | [mission-five-capitals-diplomatic-circuit-confederacy](mission-five-capitals-diplomatic-circuit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | 6 of 9 |
| 58 | [home-frontier-station](home-frontier-station.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 17 jumps | up to 12 ships, empty hold, born outerrim | 1 of 9 |
| 59 | [home-grand-exchange](home-grand-exchange.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 6 ships, empty hold, born nebula, standing work | 1 of 9 |
| 60 | [hunt-alnilam-gas-pocket-halo-drifter](hunt-alnilam-gas-pocket-halo-drifter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | 1 of 9 |
| 61 | [hunt-gemma-haze-halo-drifter](hunt-gemma-haze-halo-drifter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, empty hold, standing work | 1 of 9 |
| 62 | [hunt-deep-range-cryobelt-hollow-pilgrim](hunt-deep-range-cryobelt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 3 ships, standing work | 4 of 9 |
| 63 | [hunt-fulu-vapor-fields-chlorophage](hunt-fulu-vapor-fields-chlorophage.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | 1 of 9 |
| 64 | [hunt-gsc-0044-belt-carapace](hunt-gsc-0044-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 2 of 9 |
| 65 | [hunt-atlas-gossamer-null-carapace](hunt-atlas-gossamer-null-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 1 of 9 |
| 66 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 2 of 9 |
| 67 | [hunt-gsc-0031-belt-carapace](hunt-gsc-0031-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 1 of 9 |
| 68 | [hunt-propus-ice-belt-hollow-pilgrim](hunt-propus-ice-belt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 3 ships, empty hold, standing work | 5 of 9 |
| 69 | [hunt-diadem-ice-belt-hollow-pilgrim](hunt-diadem-ice-belt-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 3 ships, empty hold, standing work | 5 of 9 |
| 70 | [hunt-taygeta-frozen-drift-hollow-pilgrim](hunt-taygeta-frozen-drift-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 3 ships, empty hold, standing work | 5 of 9 |
| 71 | [hunt-titawin-gas-cloud-chlorophage](hunt-titawin-gas-cloud-chlorophage.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | 2 of 9 |
| 72 | [hunt-fulu-vapor-fields-cinder-sylph](hunt-fulu-vapor-fields-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | 3 of 9 |
| 73 | [hunt-hd-20794-ice-fields-hollow-pilgrim](hunt-hd-20794-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 1 ships, empty hold, standing work | 2 of 9 |
| 74 | [mission-voidborn-trajectory-unknown](mission-voidborn-trajectory-unknown.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 16 jumps | once per pilot, up to 3 ships | 2 of 9 |
| 75 | [hunt-gsc-0012-gas-plume-cinder-sylph](hunt-gsc-0012-gas-plume-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | 3 of 9 |
| 76 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | 6 of 9 |
| 77 | [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, empty hold, standing work | 7 of 9 |
| 78 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | 6 of 9 |
| 79 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | 6 of 9 |
| 80 | [give-miner-stores-central-nexus](give-miner-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at central_nexus, standing work | all 9 |
| 81 | [give-miner-stores-node-beta](give-miner-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at node_beta_industrial_station, standing work | all 9 |
| 82 | [give-drone-stores-central-nexus](give-drone-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 creature_carapace stored at central_nexus, standing work | all 9 |
| 83 | [give-miner-stores-experiment](give-miner-stores-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at the_experiment_research_station, standing work | all 9 |
| 84 | [give-miner-stores-synchrony](give-miner-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at synchrony_hub, standing work | all 9 |
| 85 | [give-scout-stores-experiment](give-scout-stores-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at the_experiment_research_station, standing work | all 9 |
| 86 | [give-scout-stores-synchrony](give-scout-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at synchrony_hub, standing work | all 9 |
| 87 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 9 |
| 88 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 9 |
