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

Kept by Zero. Routes: 76. Ships: 60.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [fit-mining-laser-iii-lhs-1140](fit-mining-laser-iii-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, up to 3 ships, 20 pilots in all, needs mining_laser_i, without mining_laser_iii, empty hold, from 20,000 cr, while 784309214f105860a16a0c100a70eb14 asks 7700 cr or less for mining_laser_iii | all 60 |
| 2 | [give-miner-stores-node-beta](give-miner-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at node_beta_industrial_station, standing work | all 60 |
| 3 | [give-miner-stores-experiment](give-miner-stores-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at the_experiment_research_station, standing work | all 60 |
| 4 | [give-miner-stores-central-nexus](give-miner-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at central_nexus, standing work | all 60 |
| 5 | [give-miner-stores-synchrony](give-miner-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at synchrony_hub, standing work | all 60 |
| 6 | [give-miner-stores-node-alpha](give-miner-stores-node-alpha.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at node_alpha_processing_station, standing work | all 60 |
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
| 32 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | all 60 |
| 33 | [gather-gsc-0044-forgotten-tailings-faction](gather-gsc-0044-forgotten-tailings-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | 3 of 60 |
| 34 | [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1 of 60 |
| 35 | [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 21 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2 of 60 |
| 36 | [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 5 of 60 |
| 37 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Tests](index-tests.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 60 |
| 38 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 39 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 40 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 41 | [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 60 |
| 42 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold, while synchrony_hub bids 25 cr for water_ice | all 60 |
| 43 | [gather-acrux-belt-faction](gather-acrux-belt-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 3 ships, empty hold, standing work | 13 of 60 |
| 44 | [gather-gsc-0044-belt-faction](gather-gsc-0044-belt-faction.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 10 ships, empty hold, standing work | 13 of 60 |
| 45 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 60 |
| 46 | [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, empty hold, standing work | all 60 |
| 47 | [gather-jishui-plainrock-carbon](gather-jishui-plainrock-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 8 ships, empty hold, standing work | all 60 |
| 48 | [gather-last-light-mineral-carbon](gather-last-light-mineral-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 49 | [gather-yildun-neverworld-carbon](gather-yildun-neverworld-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 4 ships, empty hold, standing work | all 60 |
| 50 | [gather-jadecove-nickel](gather-jadecove-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 51 | [gather-tiaki-worldsend-nickel](gather-tiaki-worldsend-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 2 ships, empty hold, standing work | all 60 |
| 52 | [gather-gsc-0049-reef-nickel](gather-gsc-0049-reef-nickel.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 53 | [gather-glasslight-shoal-silicon](gather-glasslight-shoal-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 54 | [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 55 | [gather-goldcrest-gold](gather-goldcrest-gold.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 3 ships, empty hold, standing work | all 60 |
| 56 | [gather-bunda-belt-platinum](gather-bunda-belt-platinum.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 57 | [gather-izar-quantum-fragments](gather-izar-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 58 | [gather-errai-quantum-fragments](gather-errai-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 2 ships, empty hold, standing work | all 60 |
| 59 | [gather-tidewater-quantum-fragments](gather-tidewater-quantum-fragments.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, empty hold, standing work | all 60 |
| 60 | [give-miner-stores-crescent-moon](give-miner-stores-crescent-moon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 2 ships, with 50 carbon_ore or silicon_ore or nickel_ore or quantum_fragments or iron_ore or copper_ore or gold_ore or platinum_ore stored at ec315132a710a7d0fbc68cca05073154, standing work | all 60 |
| 61 | [give-miner-stores-ramens-rest](give-miner-stores-ramens-rest.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 2 ships, with 50 carbon_ore or silicon_ore or nickel_ore or quantum_fragments or iron_ore or copper_ore or gold_ore or platinum_ore stored at ramens_rest, standing work | all 60 |
| 62 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 60 |
| 63 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, standing work | all 60 |
| 64 | [gather-achernar-belt](gather-achernar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 16 ships, empty hold, standing work | all 60 |
| 65 | [gather-garnet-belt](gather-garnet-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 29 ships, empty hold, standing work | all 60 |
| 66 | [gather-schedar-belt](gather-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 45 ships, empty hold, standing work | all 60 |
| 67 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 120 ships, standing work | all 60 |
| 68 | [gather-okab-belt](gather-okab-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 42 ships, empty hold, standing work | all 60 |
| 69 | [gather-gj-3470-dewfall-fray](gather-gj-3470-dewfall-fray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 13 ships, empty hold, standing work | all 60 |
| 70 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, standing work | all 60 |
| 71 | [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 35 ships, empty hold, standing work | all 60 |
| 72 | [gather-ironhollow-fading-signal](gather-ironhollow-fading-signal.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 20 ships, empty hold, standing work | all 60 |
| 73 | [gather-ruchbah-broken-glass-veil](gather-ruchbah-broken-glass-veil.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 6 ships, empty hold, standing work | all 60 |
| 74 | [mine-acubens](mine-acubens.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, standing work | all 60 |
| 75 | [train-jumps-miner](train-jumps-miner.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 25 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 60 |
| 76 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 60 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [ice-sell](templates-mining.md) | 60 |
| [reserve-prism](templates-mining.md) | 29 |
| [reserve-hamal](templates-mining.md) | 31 |

Planned:

| What | When |
|---|---|
| Read the Jishui field against its pull of about 176 carbon a ship-hour; lower it under 8 hours of stock above its floor | next turn |
| Read the give-miner-stores copies' first hand-overs; drop them once requires.stored takes any one item (requests ENT-349) | next turn |
| Far gathers give each load at The Crescent Moon and Ramen's Rest once Logistics names a receiver there (requests ENT-350) | on Apollo's answer |
| Yildun carbon: lift on its third result (F37) | next turn |
