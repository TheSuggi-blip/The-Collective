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

Kept by Apollo. Routes: 49. Ships: 40.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [stock-rc-boards-node-beta](stock-rc-boards-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 1 ships, 1 pilots in all, empty hold, from 3,000 cr, with 500 circuit_board stored at node_beta_industrial_station, standing work | all 40 |
| 2 | [stock-rc-plate-node-beta](stock-rc-plate-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 3 ships, 9 pilots in all, empty hold, from 3,000 cr, with 120 steel_plate stored at node_beta_industrial_station, standing work | all 40 |
| 3 | [stock-rc-flex-carry-central-nexus](stock-rc-flex-carry-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 1 ships, 1 pilots in all, empty hold, from 3,000 cr, with 10 flex_polymer stored at central_nexus, standing work | all 40 |
| 4 | [stock-rc-flex-buy-home](stock-rc-flex-buy-home.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships, 3 pilots in all, empty hold, from 15,000 cr | all 40 |
| 5 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 40 |
| 6 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 40 |
| 7 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 40 |
| 8 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 |
| 9 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 40 |
| 10 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 40 |
| 11 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 40 |
| 12 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 |
| 13 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 |
| 14 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 15 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 40 |
| 16 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 17 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 40 |
| 18 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 40 |
| 19 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 40 |
| 20 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 21 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 40 |
| 22 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 40 |
| 23 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 40 |
| 24 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 25 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 40 |
| 26 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 27 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 28 | [drain-ice-nexus](drain-ice-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | 1 of 40 |
| 29 | [outpost-kit-ironlight-to-node-beta](outpost-kit-ironlight-to-node-beta.json) | [Tests](index-tests.md) | beyond the border, 6 jumps | up to 1 ships, 1 pilots in all, empty hold, from 152,000 cr, while 784309214f105860a16a0c100a70eb14 asks 148663 cr or less for outpost_kit | 1 of 40 |
| 30 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | 1 of 40 |
| 31 | [supply-repair-gsc-0044-boards](supply-repair-gsc-0044-boards.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, from 5,000 cr, with 30 circuit_board stored at node_beta_industrial_station, standing work | 34 of 40 |
| 32 | [supply-repair-gsc-0044-plate](supply-repair-gsc-0044-plate.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 6 pilots in all, from 5,000 cr, with 100 steel_plate stored at node_beta_industrial_station, standing work | 34 of 40 |
| 33 | [supply-bunker-gsc-0044-own-cells](supply-bunker-gsc-0044-own-cells.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 5,000 cr, with 29 fuel_cell stored at node_beta_industrial_station, standing work | 34 of 40 |
| 34 | [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 12,000 cr, standing work | 34 of 40 |
| 35 | [buy-flex-central-nexus-to-node-beta](buy-flex-central-nexus-to-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships, 3 pilots in all, empty hold, from 15,000 cr, while central_nexus asks 129 cr or less for flex_polymer | 5 of 40 |
| 36 | [buy-flex-ironlight-to-node-beta](buy-flex-ironlight-to-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 2 ships, 5 pilots in all, empty hold, from 15,000 cr, while 784309214f105860a16a0c100a70eb14 asks 123 cr or less for flex_polymer | 5 of 40 |
| 37 | [craft-boards-node-beta](craft-boards-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, with 30 silicon_ore stored at node_beta_industrial_station, standing work | 1 of 40 |
| 38 | [give-hauler-stores-node-beta](give-hauler-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_beta_industrial_station, standing work | all 40 |
| 39 | [give-hauler-stores-node-gamma](give-hauler-stores-node-gamma.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_gamma_relay_station, standing work | all 40 |
| 40 | [give-hauler-stores-nova-terra](give-hauler-stores-nova-terra.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 2 ships, with 50 argon_gas stored at nova_terra_central, standing work | all 40 |
| 41 | [give-hauler-stores-central-nexus](give-hauler-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 water_ice stored at central_nexus, standing work | all 40 |
| 42 | [craft-cells-hydrogen-node-beta](craft-cells-hydrogen-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, with 160 hydrogen_gas stored at node_beta_industrial_station, standing work | all 40 |
| 43 | [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 40 |
| 44 | [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 45 | [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at synchrony_hub, standing work | all 40 |
| 46 | [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at central_nexus, standing work | all 40 |
| 47 | [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 130 steel_plate stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 48 | [train-jumps-hauler](train-jumps-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 40 |
| 49 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [stored-goods](templates-logistics.md) | 40 |
| [craft-reserve](templates-logistics.md) | 40 |
| [outpost-supply](templates-logistics.md) | 34 |
| [train-hauler](templates-logistics.md) | 40 |

Planned:

| What | When |
|---|---|
| Read the first three runs of supply-bunker-gsc-0044-own-cells and of buy-flex-central-nexus-to-node-beta; lift or drop by them (F37) | next turn |
| Found Atria with found.py the hour the builder's kit lands at Node Beta (the kit route flies only on an ask at Ironlight) | on the kit |
| Take status off out of the four give-hauler-stores routes when strict classes go on (or Unity does it) | at the switch |
| Build the Recruitment Center with build.py --upgrade when the treasury holds 2,000,000 cr and the flex stands at 300 | on the fee |
