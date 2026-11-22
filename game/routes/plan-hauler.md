---
name: routes-plan-hauler
id: 20261116T174332Z
tier: intel
author: Unity
---

# plan-hauler.md -- The Plan of the Role hauler

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/hauler.json`:
the routes the hauler ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/hauler.json` is written from it. `Planned` is what the Admiral
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Apollo. Routes: 47. Ships: 55.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 55 |
| 2 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 55 |
| 3 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 55 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 55 |
| 5 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 55 |
| 6 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 55 |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 55 |
| 8 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 55 |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 55 |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 55 |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 55 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 55 |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 55 |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 55 |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 55 |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 55 |
| 17 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 55 |
| 18 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 55 |
| 19 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 55 |
| 20 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 55 |
| 21 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 55 |
| 22 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 55 |
| 23 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 55 |
| 24 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 3 ships | all 55 |
| 25 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 3 ships | all 55 |
| 26 | [craft-boards-crescent-moon](craft-boards-crescent-moon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, with 10 silicon_ore stored at ec315132a710a7d0fbc68cca05073154, 120 carbon_ore stored at ec315132a710a7d0fbc68cca05073154, standing work | 1 of 55 |
| 27 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 3 ships | 1 of 55 |
| 28 | [outpost-kit-ironlight-to-node-beta](outpost-kit-ironlight-to-node-beta.json) | [Tests](index-tests.md) | beyond the border, 6 jumps | up to 1 ships, 1 pilots in all, empty hold, from 152,000 cr, while 784309214f105860a16a0c100a70eb14 asks 148663 cr or less for outpost_kit | 1 of 55 |
| 29 | [supply-repair-gsc-0044-boards](supply-repair-gsc-0044-boards.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, from 5,000 cr, with 30 circuit_board stored at node_beta_industrial_station, standing work | 49 of 55 |
| 30 | [supply-repair-gsc-0044-plate](supply-repair-gsc-0044-plate.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 6 pilots in all, from 5,000 cr, with 100 steel_plate stored at node_beta_industrial_station, standing work | 49 of 55 |
| 31 | [supply-bunker-gsc-0044-own-cells](supply-bunker-gsc-0044-own-cells.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 5,000 cr, with 29 fuel_cell stored at node_beta_industrial_station, standing work | 49 of 55 |
| 32 | [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 12,000 cr, standing work | 49 of 55 |
| 33 | [give-hauler-stores-node-beta](give-hauler-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_beta_industrial_station, standing work | all 55 |
| 34 | [give-hauler-stores-node-gamma](give-hauler-stores-node-gamma.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_gamma_relay_station, standing work | all 55 |
| 35 | [give-hauler-stores-nova-terra](give-hauler-stores-nova-terra.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 2 ships, with 50 argon_gas stored at nova_terra_central, standing work | all 55 |
| 36 | [give-hauler-stores-central-nexus](give-hauler-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 water_ice stored at central_nexus, standing work | all 55 |
| 37 | [craft-boards-stored-node-beta](craft-boards-stored-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 silicon_ore stored at node_beta_industrial_station, 120 carbon_ore stored at node_beta_industrial_station, standing work | all 55 |
| 38 | [craft-gold-wiring-synchrony-hub](craft-gold-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 40 gold_ore stored at synchrony_hub, standing work | all 55 |
| 39 | [craft-gold-wiring-experiment](craft-gold-wiring-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 40 gold_ore stored at the_experiment_research_station, standing work | all 55 |
| 40 | [craft-cells-hydrogen-node-beta](craft-cells-hydrogen-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, with 160 hydrogen_gas stored at node_beta_industrial_station, standing work | all 55 |
| 41 | [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 55 |
| 42 | [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 55 |
| 43 | [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at synchrony_hub, standing work | all 55 |
| 44 | [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at central_nexus, standing work | all 55 |
| 45 | [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 130 steel_plate stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 55 |
| 46 | [train-jumps-hauler](train-jumps-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 55 |
| 47 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 55 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [stored-goods](templates-logistics.md) | 55 |
| [craft-reserve](templates-logistics.md) | 55 |
| [outpost-supply](templates-logistics.md) | 49 |
| [train-hauler](templates-logistics.md) | 55 |

Planned:

| What | When |
|---|---|
| Read the first runs of craft-wiring-logistics-* and how many haulers left train-jumps-hauler; size max_ships by the queue | next turn |
| Read the third run of craft-boards-crescent-moon (F37) and lift it to the receiver's silicon there; found Atria with found.py the hour a kit lands | next turn |
| Hydrogen at Node Gamma (about 1,675 gas in four haulers' stores) into fuel cells for the bunker: a route that brings plate to it first | when the wiring runs are read |
