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

Kept by Apollo. Routes: 57. Ships: 95.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 95 |
| 2 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 95 |
| 3 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 95 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 95 |
| 5 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 95 |
| 6 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 95 |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 95 |
| 8 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 95 |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 95 |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 95 |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 95 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 95 |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 95 |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 95 |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 95 |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 95 |
| 17 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 95 |
| 18 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 95 |
| 19 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 95 |
| 20 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 95 |
| 21 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 95 |
| 22 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 95 |
| 23 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 95 |
| 24 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 10 ships | all 95 |
| 25 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 3 ships | all 95 |
| 26 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 95 |
| 27 | [mission-market-participation-grand](mission-market-participation-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships, from 3,200 cr, while grand_exchange_station bids 1 cr for copper_ore | 25 of 95 |
| 28 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 10 ships | 25 of 95 |
| 29 | [mission-the-objection-deep](mission-the-objection-deep.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | 1 of 95 |
| 30 | [mission-the-expeditionary-mandate-first](mission-the-expeditionary-mandate-first.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | 2 of 95 |
| 31 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | 30 of 95 |
| 32 | [mission-market-participation-frontier](mission-market-participation-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 17 jumps | once per pilot, up to 1 ships, from 3,200 cr, while frontier_station bids 1 cr for copper_ore | 30 of 95 |
| 33 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | 30 of 95 |
| 34 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | 30 of 95 |
| 35 | [craft-boards-crescent-moon](craft-boards-crescent-moon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, with 10 silicon_ore stored at ec315132a710a7d0fbc68cca05073154, 120 carbon_ore stored at ec315132a710a7d0fbc68cca05073154, standing work | 1 of 95 |
| 36 | [mission-cracking-the-shell-krynn](mission-cracking-the-shell-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | 1 of 95 |
| 37 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 6 ships | 1 of 95 |
| 38 | [outpost-kit-ironlight-to-node-beta](outpost-kit-ironlight-to-node-beta.json) | [Tests](index-tests.md) | beyond the border, 6 jumps | up to 1 ships, 1 pilots in all, empty hold, from 152,000 cr, while 784309214f105860a16a0c100a70eb14 asks 148663 cr or less for outpost_kit | 1 of 95 |
| 39 | [supply-repair-gsc-0044-boards](supply-repair-gsc-0044-boards.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, from 5,000 cr, with 30 circuit_board stored at node_beta_industrial_station, standing work | 34 of 95 |
| 40 | [supply-repair-gsc-0044-plate](supply-repair-gsc-0044-plate.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 6 pilots in all, from 5,000 cr, with 100 steel_plate stored at node_beta_industrial_station, standing work | 34 of 95 |
| 41 | [supply-bunker-gsc-0044-own-cells](supply-bunker-gsc-0044-own-cells.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 5,000 cr, with 29 fuel_cell stored at node_beta_industrial_station, standing work | 34 of 95 |
| 42 | [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 12,000 cr, standing work | 34 of 95 |
| 43 | [give-hauler-stores-node-beta](give-hauler-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_beta_industrial_station, standing work | 40 of 95 |
| 44 | [give-hauler-stores-node-gamma](give-hauler-stores-node-gamma.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_gamma_relay_station, standing work | 40 of 95 |
| 45 | [give-hauler-stores-nova-terra](give-hauler-stores-nova-terra.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 2 ships, with 50 argon_gas stored at nova_terra_central, standing work | 40 of 95 |
| 46 | [give-hauler-stores-central-nexus](give-hauler-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 water_ice stored at central_nexus, standing work | 40 of 95 |
| 47 | [craft-boards-stored-node-beta](craft-boards-stored-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 silicon_ore stored at node_beta_industrial_station, 120 carbon_ore stored at node_beta_industrial_station, standing work | 40 of 95 |
| 48 | [craft-gold-wiring-synchrony-hub](craft-gold-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 40 gold_ore stored at synchrony_hub, standing work | 40 of 95 |
| 49 | [craft-gold-wiring-experiment](craft-gold-wiring-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 40 gold_ore stored at the_experiment_research_station, standing work | 40 of 95 |
| 50 | [craft-cells-hydrogen-node-beta](craft-cells-hydrogen-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, with 160 hydrogen_gas stored at node_beta_industrial_station, standing work | 40 of 95 |
| 51 | [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | 40 of 95 |
| 52 | [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | 40 of 95 |
| 53 | [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at synchrony_hub, standing work | 40 of 95 |
| 54 | [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at central_nexus, standing work | 40 of 95 |
| 55 | [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 130 steel_plate stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | 40 of 95 |
| 56 | [train-jumps-hauler](train-jumps-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | 40 of 95 |
| 57 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 95 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [stored-goods](templates-logistics.md) | 40 |
| [craft-reserve](templates-logistics.md) | 40 |
| [outpost-supply](templates-logistics.md) | 34 |
| [train-hauler](templates-logistics.md) | 40 |
| [newborn-rim](templates-logistics.md) | 30 |
| [newborn-nebula](templates-logistics.md) | 25 |

Planned:

| What | When |
|---|---|
| Market Participation at Grand Exchange for the 25 Nebula-born haulers once their top-up lands (requests ENT-385) | next turn |
| Cap the empty jump loop at the 8 haulers nearest Piloting 10 when cargo-carrying loops stand for the rest (requests ENT-374) | when the carrying goods exist |
| A visit step in the runner for Local Sector Survey and Grand Tour (2,500 and 12,000 cr, 340 to 520 Piloting XP) on the newborns' boards | next turn |
| Found Atria the hour an Outpost Kit is read at Ironlight | on the kit |
