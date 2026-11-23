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
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Zero. Routes: 95. Ships: 130.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [fit-mining-laser-iii-lhs-1140](fit-mining-laser-iii-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, up to 3 ships, 50 pilots in all, needs mining_laser_i, without mining_laser_iii, empty hold, from 20,000 cr, while 784309214f105860a16a0c100a70eb14 asks 7700 cr or less for mining_laser_iii | all 130 |
| 2 | [fit-mining-laser-ii-lhs-1140](fit-mining-laser-ii-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, up to 3 ships, 20 pilots in all, needs mining_laser_i, without ['mining_laser_ii', 'mining_laser_iii'], empty hold, from 12,000 cr, born voidborn, while 784309214f105860a16a0c100a70eb14 asks 2600 cr or less for mining_laser_ii | all 130 |
| 3 | [fit-mining-laser-ii-second-central-nexus](fit-mining-laser-ii-second-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without ['mining_laser_ii', 'mining_laser_iii', 'ice_harvester_i'], empty hold, from 20,000 cr, while central_nexus asks 4300 cr or less for mining_laser_ii | all 130 |
| 4 | [give-miner-stores-node-beta](give-miner-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at node_beta_industrial_station, standing work | all 130 |
| 5 | [give-miner-stores-experiment](give-miner-stores-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at the_experiment_research_station, standing work | all 130 |
| 6 | [give-miner-stores-central-nexus](give-miner-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at central_nexus, standing work | all 130 |
| 7 | [give-miner-stores-synchrony](give-miner-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at synchrony_hub, standing work | all 130 |
| 8 | [give-miner-stores-node-alpha](give-miner-stores-node-alpha.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at node_alpha_processing_station, standing work | all 130 |
| 9 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 130 |
| 10 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 130 |
| 11 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 130 |
| 12 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 130 |
| 13 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 130 |
| 14 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 130 |
| 15 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 130 |
| 16 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 130 |
| 17 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 130 |
| 18 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 130 |
| 19 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 130 |
| 20 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 130 |
| 21 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 130 |
| 22 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 130 |
| 23 | [mission-deep-core-prospecting-first-step](mission-deep-core-prospecting-first-step.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 2 ships, 12 pilots in all, empty hold | all 130 |
| 24 | [mission-the-forge-tax-crucible](mission-the-forge-tax-crucible.json) | [Off](index-off.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships, 20 pilots in all, empty hold, off | all 130 |
| 25 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 130 |
| 26 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 130 |
| 27 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 130 |
| 28 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 130 |
| 29 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 130 |
| 30 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 130 |
| 31 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 130 |
| 32 | [mission-deep-core-prospecting-nova-terra](mission-deep-core-prospecting-nova-terra.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 1 ships, 16 pilots in all, empty hold | all 130 |
| 33 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 130 |
| 34 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | all 130 |
| 35 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 130 |
| 36 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 130 |
| 37 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 130 |
| 38 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 130 |
| 39 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 130 |
| 40 | [mission-welcome-sol-central](mission-welcome-sol-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 3 ships, born solarian | all 130 |
| 41 | [mission-a-word-in-private-grand](mission-a-word-in-private-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 5 ships, born nebula | all 130 |
| 42 | [mission-first-cargo-haven](mission-first-cargo-haven.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 22 jumps | once per pilot, up to 8 ships, born nebula | all 130 |
| 43 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 130 |
| 44 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 130 |
| 45 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 3 ships | all 130 |
| 46 | [mission-the-objection-deep](mission-the-objection-deep.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 130 |
| 47 | [store-hold-grand-exchange](store-hold-grand-exchange.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 20 ships, goods aboard, born nebula, standing work | 35 of 130 |
| 48 | [mission-deep-core-prospecting-haven](mission-deep-core-prospecting-haven.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships, 30 pilots in all, from mining 5, born nebula | 35 of 130 |
| 49 | [store-hold-sol-central](store-hold-sol-central.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 20 ships, goods aboard, born solarian, standing work | 35 of 130 |
| 50 | [fit-mining-laser-ii-sol-central](fit-mining-laser-ii-sol-central.json) | [Fitting](index-fitting.md) | beyond the border, 10 jumps | once per pilot, up to 1 ships, 7 pilots in all, needs mining_laser_i, without ['mining_laser_ii', 'mining_laser_iii'], empty hold, from 6,000 cr, born solarian, while confederacy_central_command asks 2600 cr or less for mining_laser_ii | 35 of 130 |
| 51 | [mission-copper-iron-procyon](mission-copper-iron-procyon.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 6 ships, born solarian | 35 of 130 |
| 52 | [mission-deep-core-prospecting-sol](mission-deep-core-prospecting-sol.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 2 ships, 7 pilots in all, from mining 5, born solarian | 35 of 130 |
| 53 | [gather-lacaille-deep-vein-train](gather-lacaille-deep-vein-train.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 6 ships, empty hold, born solarian, standing work | 35 of 130 |
| 54 | [gather-markab-alloy-seam-train](gather-markab-alloy-seam-train.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 6 ships, empty hold, born solarian, standing work | 35 of 130 |
| 55 | [gather-nihal-containment-fracture-train](gather-nihal-containment-fracture-train.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 12 ships, empty hold, born solarian, standing work | 35 of 130 |
| 56 | [gather-harborlight-leavings-train](gather-harborlight-leavings-train.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, born solarian, standing work | 35 of 130 |
| 57 | [gather-electra-echo-train](gather-electra-echo-train.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 1 ships, empty hold, born solarian, standing work | 35 of 130 |
| 58 | [gather-gsc-0044-belt-faction](gather-gsc-0044-belt-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 10 ships, empty hold, standing work | 20 of 130 |
| 59 | [gather-gsc-0044-forgotten-tailings-faction](gather-gsc-0044-forgotten-tailings-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 5 ships, empty hold, standing work | 20 of 130 |
| 60 | [gather-acrux-belt-faction](gather-acrux-belt-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 3 ships, empty hold, standing work | 20 of 130 |
| 61 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 130 |
| 62 | [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, empty hold, standing work | all 130 |
| 63 | [gather-jishui-plainrock-carbon](gather-jishui-plainrock-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 64 | [gather-last-light-mineral-carbon](gather-last-light-mineral-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 65 | [gather-yildun-neverworld-carbon](gather-yildun-neverworld-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 10 ships, empty hold, standing work | all 130 |
| 66 | [gather-jadecove-nickel](gather-jadecove-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 67 | [gather-tiaki-worldsend-nickel](gather-tiaki-worldsend-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 2 ships, empty hold, standing work | all 130 |
| 68 | [gather-gsc-0049-reef-nickel](gather-gsc-0049-reef-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 69 | [gather-glasslight-shoal-silicon](gather-glasslight-shoal-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 70 | [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 71 | [gather-goldcrest-gold](gather-goldcrest-gold.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 6 ships, empty hold, standing work | all 130 |
| 72 | [gather-bunda-belt-platinum](gather-bunda-belt-platinum.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 3 ships, empty hold, standing work | all 130 |
| 73 | [gather-khambalia-crystal-market-train](gather-khambalia-crystal-market-train.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 23 jumps | up to 18 ships, empty hold, born nebula, standing work | 35 of 130 |
| 74 | [gather-alrakis-commerce-vein-train](gather-alrakis-commerce-vein-train.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 14 ships, empty hold, born nebula, standing work | 35 of 130 |
| 75 | [gather-izar-quantum-fragments](gather-izar-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 76 | [gather-errai-quantum-fragments](gather-errai-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 2 ships, empty hold, standing work | all 130 |
| 77 | [gather-tidewater-quantum-fragments](gather-tidewater-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, empty hold, standing work | all 130 |
| 78 | [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 130 |
| 79 | [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 21 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2 of 130 |
| 80 | [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 11 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 5 of 130 |
| 81 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Tests](index-tests.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 130 |
| 82 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 130 |
| 83 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 130 |
| 84 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 130 |
| 85 | [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 130 |
| 86 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold, while synchrony_hub bids 25 cr for water_ice | all 130 |
| 87 | [give-miner-stores-crescent-moon](give-miner-stores-crescent-moon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 2 ships, with 50 carbon_ore or silicon_ore or nickel_ore or quantum_fragments or iron_ore or copper_ore or gold_ore or platinum_ore stored at ec315132a710a7d0fbc68cca05073154, standing work | all 130 |
| 88 | [give-miner-stores-ramens-rest](give-miner-stores-ramens-rest.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 2 ships, with 50 carbon_ore or silicon_ore or nickel_ore or quantum_fragments or iron_ore or copper_ore or gold_ore or platinum_ore stored at ramens_rest, standing work | all 130 |
| 89 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 130 |
| 90 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, standing work | all 130 |
| 91 | [gather-schedar-belt](gather-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 5 ships, empty hold, standing work | all 130 |
| 92 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 4 ships, empty hold, standing work | all 130 |
| 93 | [home-sol-central](home-sol-central.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 6 ships, empty hold, born solarian, standing work | all 130 |
| 94 | [train-jumps-miner](train-jumps-miner.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 25 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 130 |
| 95 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 130 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [ice-sell](templates-mining.md) | 130 |
| [reserve-prism](templates-mining.md) | 99 |
| [reserve-hamal](templates-mining.md) | 31 |

Planned:

| What | When |
|---|---|
| Read the Sol Laser II, Alrakis and store-hold results; size Khambalia again; put the GSC-0044 belts in the rows of seated Solarian miners | next turn |
