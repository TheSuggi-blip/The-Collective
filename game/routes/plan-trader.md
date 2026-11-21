---
name: routes-plan-trader
id: 20261116T174336Z
tier: intel
author: Unity
---

# plan-trader.md -- The Plan of the Role trader

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/trader.json`:
the routes the trader ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/trader.json` is written from it. `Planned` is what the Admiral
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Mercury. Routes: 53. Ships: 40.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 40 |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 40 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 |
| 6 | [voidborn-neural-matrix-board](voidborn-neural-matrix-board.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 4 ships | all 40 |
| 7 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 40 |
| 8 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 40 |
| 9 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 40 |
| 10 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 40 |
| 11 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 40 |
| 12 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 13 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 14 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 40 |
| 15 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 40 |
| 16 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 17 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 18 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 19 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 20 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 21 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 22 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 23 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 40 |
| 24 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 25 | [carry-hydrogen-beta-to-crucible](carry-hydrogen-beta-to-crucible.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, with 41 hydrogen_gas stored at node_beta_industrial_station, while the_crucible_garrison bids 33 cr for hydrogen_gas, off | 2 of 40 |
| 26 | [go-ironlight-trader](go-ironlight-trader.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 1 pilots in all, empty hold, from 20,000 cr | 1 of 40 |
| 27 | [carry-hydrogen-beta-to-crucible-bulk](carry-hydrogen-beta-to-crucible-bulk.json) | [Off](index-off.md) | beyond the border, 18 jumps | up to 1 ships, without mining_laser_i, with 100 hydrogen_gas stored at node_beta_industrial_station, while the_crucible_garrison bids 33 cr for hydrogen_gas, off | 1 of 40 |
| 28 | [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 null_matter stored at node_beta_industrial_station, while central_nexus bids 200 cr for null_matter | all 40 |
| 29 | [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 null_matter stored at central_nexus, while central_nexus bids 200 cr for null_matter | all 40 |
| 30 | [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 30 null_matter stored at synchrony_hub, while central_nexus bids 150 cr for null_matter | all 40 |
| 31 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | all 40 |
| 32 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | all 40 |
| 33 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | all 40 |
| 34 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | all 40 |
| 35 | [sell-soma-at-experiment](sell-soma-at-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at the_experiment_research_station, while the_experiment_research_station bids 320 cr for voidborn_neural_soma | all 40 |
| 36 | [carry-palladium-nexus-to-gamma](carry-palladium-nexus-to-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 palladium_ore stored at central_nexus, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 37 | [sell-palladium-at-node-gamma](sell-palladium-at-node-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 palladium_ore stored at node_gamma_relay_station, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 38 | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 30 cr for hydrogen_gas | all 40 |
| 39 | [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_gamma_relay_station, while node_gamma_relay_station bids 30 cr for hydrogen_gas | all 40 |
| 40 | [sell-hydrogen-at-synchrony](sell-hydrogen-at-synchrony.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while synchrony_hub bids 30 cr for hydrogen_gas | all 40 |
| 41 | [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while the_experiment_research_station bids 30 cr for hydrogen_gas | all 40 |
| 42 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 43 | [craft-piping-synchrony-hub](craft-piping-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at synchrony_hub, 60 copper_ore stored at synchrony_hub, standing work | all 40 |
| 44 | [craft-steel-own-node-beta](craft-steel-own-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 45 | [craft-steel-own-experiment](craft-steel-own-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 40 |
| 46 | [craft-steel-own-central-nexus](craft-steel-own-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 100 iron_ore stored at central_nexus, standing work | all 40 |
| 47 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | all 40 |
| 48 | [craft-wiring-node-beta](craft-wiring-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 80 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 49 | [craft-wiring-experiment](craft-wiring-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at the_experiment_research_station, standing work | all 40 |
| 50 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 51 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 40 |
| 52 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 40 |
| 53 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [trade-sell](templates-trade.md) | 40 |
| [trade-craft](templates-trade.md) | 40 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of the four tests beyond the border (silver bars to Arneb, hydrogen and heat sinks to The Crucible, the freighter's bulk carry): what each far bid took, its regain, the fuel of the road; lift a test only on its own runs | next turn |
| The freighter step: if the Prayer's first carry pays its fuel, one Prayer (5,000 cr, Ironlight Crossroads) for each trader that has a load worth its road, inside rule F12, with the Fleet Admiral's answer to requests.log ENT-286 | after the first freighter RESULT |
| Read every sell floor beside its cheapest deep ask (sellgen.py scan) and the home bids that read 0 after the pause (null matter, hydrogen, palladium); run reservecheck.py and oncecheck.py; read Neural Matrix Delivery's runs at 4 ships | every turn |
