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

Kept by Zero. Routes: 73. Ships: 60.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [fit-mining-laser-iii-lhs-1140](fit-mining-laser-iii-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, up to 3 ships, 20 pilots in all, needs mining_laser_i, without mining_laser_iii, empty hold, from 20,000 cr, while 784309214f105860a16a0c100a70eb14 asks 7700 cr or less for mining_laser_iii | all 60 |
| 2 | [give-miner-stores-node-beta](give-miner-stores-node-beta.json) | [Tests](index-tests.md) | home space | up to 3 ships, with 50 iron_ore stored at node_beta_industrial_station | all 60 |
| 3 | [give-miner-stores-experiment](give-miner-stores-experiment.json) | [Tests](index-tests.md) | home space | up to 3 ships, with 50 iron_ore stored at the_experiment_research_station | all 60 |
| 4 | [give-miner-stores-central-nexus](give-miner-stores-central-nexus.json) | [Tests](index-tests.md) | home space | up to 3 ships, with 50 iron_ore stored at central_nexus | all 60 |
| 5 | [give-miner-stores-synchrony](give-miner-stores-synchrony.json) | [Tests](index-tests.md) | home space | up to 3 ships, with 50 iron_ore stored at synchrony_hub | all 60 |
| 6 | [give-miner-stores-node-alpha](give-miner-stores-node-alpha.json) | [Tests](index-tests.md) | home space | up to 3 ships, with 50 iron_ore stored at node_alpha_processing_station | all 60 |
| 7 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 60 |
| 8 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 60 |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 60 |
| 10 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 60 |
| 11 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 60 |
| 12 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 60 |
| 13 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 60 |
| 14 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 60 |
| 15 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 60 |
| 16 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 60 |
| 17 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 60 |
| 18 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 60 |
| 19 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 60 |
| 20 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 60 |
| 21 | [mission-deep-core-prospecting-first-step](mission-deep-core-prospecting-first-step.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 2 ships, 12 pilots in all, empty hold | all 60 |
| 22 | [mission-the-forge-tax-crucible](mission-the-forge-tax-crucible.json) | [Off](index-off.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships, 20 pilots in all, empty hold, off | all 60 |
| 23 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 60 |
| 24 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 60 |
| 25 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 60 |
| 26 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 60 |
| 27 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 60 |
| 28 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 60 |
| 29 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 60 |
| 30 | [mission-deep-core-prospecting-nova-terra](mission-deep-core-prospecting-nova-terra.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 1 ships, 16 pilots in all, empty hold | all 60 |
| 31 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 60 |
| 32 | [gather-gsc-0049-reef-nickel](gather-gsc-0049-reef-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | 1 of 60 |
| 33 | [train-navigation-trader](train-navigation-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 20 ships, under navigation 3, standing work | 12 of 60 |
| 34 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | 2 of 60 |
| 35 | [gather-jishui-plainrock-carbon](gather-jishui-plainrock-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | 1 of 60 |
| 36 | [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | 2 of 60 |
| 37 | [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 21 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 60 |
| 38 | [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 60 |
| 39 | [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | 3 of 60 |
| 40 | [craft-steel-military-experiment](craft-steel-military-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | 1 of 60 |
| 41 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | 1 of 60 |
| 42 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | 1 of 60 |
| 43 | [drain-ice-nexus](drain-ice-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | 1 of 60 |
| 44 | [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4 of 60 |
| 45 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 60 |
| 46 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 47 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 48 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 49 | [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 60 |
| 50 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold, while synchrony_hub bids 25 cr for water_ice | all 60 |
| 51 | [gather-acrux-belt-faction](gather-acrux-belt-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | 10 of 60 |
| 52 | [gather-gsc-0044-belt-faction](gather-gsc-0044-belt-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 10 ships, needs mining_laser_i, empty hold, standing work | 10 of 60 |
| 53 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 60 |
| 54 | [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 55 | [gather-jadecove-nickel](gather-jadecove-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 3 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 56 | [gather-tiaki-worldsend-nickel](gather-tiaki-worldsend-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 2 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 57 | [gather-glasslight-shoal-silicon](gather-glasslight-shoal-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 58 | [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 59 | [gather-goldcrest-gold](gather-goldcrest-gold.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 6 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 60 | [gather-bunda-belt-platinum](gather-bunda-belt-platinum.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 61 | [gather-errai-belt-silver](gather-errai-belt-silver.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 62 | [gather-izar-quantum-fragments](gather-izar-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 63 | [gather-errai-quantum-fragments](gather-errai-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 64 | [gather-tidewater-quantum-fragments](gather-tidewater-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 65 | [craft-steel-experiment](craft-steel-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 550 iron_ore stored at the_experiment_research_station, standing work | all 60 |
| 66 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 60 |
| 67 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 60 |
| 68 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 60 |
| 69 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, needs mining_laser_i, standing work | all 60 |
| 70 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 60 |
| 71 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 60 |
| 72 | [train-jumps-miner](train-jumps-miner.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 25 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 60 |
| 73 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 60 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [ice-sell](templates-mining.md) | 60 |
| [reserve-prism](templates-mining.md) | 29 |
| [reserve-hamal](templates-mining.md) | 31 |

Planned:

| What | When |
|---|---|
| Read the Laser III fits (20 asks at Ironlight Crossroads, three at a time): on each fitted ship's first gather runs against Laser I's median 184 ore a seep run; a second fit station only on their result | next turn |
| Read the five one-ship tests beyond the border (quantum fragments at Tidewater, Errai and Izar; silver at Errai; platinum at Bunda): three fields at once give the quantum-fragment verdict (F37); lift or drop each | next turn |
| Strict classes: switch the five give-miner-stores routes on with the switch (requests ENT-332), then take the seven craft rows out of the miners' lists | when strict classes go on |
