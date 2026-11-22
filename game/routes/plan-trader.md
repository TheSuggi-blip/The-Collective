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

Kept by Mercury. Routes: 65. Ships: 40.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 40 |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 40 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 |
| 5 | [voidborn-network-commerce](voidborn-network-commerce.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, empty hold, after the reward The Collective Provides, while central_nexus bids 4 cr for carbon_ore | all 40 |
| 6 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 |
| 7 | [voidborn-neural-matrix-board](voidborn-neural-matrix-board.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 4 ships | all 40 |
| 8 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 40 |
| 9 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 40 |
| 10 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 40 |
| 11 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 40 |
| 12 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 40 |
| 13 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 14 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 15 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 40 |
| 16 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 40 |
| 17 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 18 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 19 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 20 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 21 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 22 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 23 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 24 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 40 |
| 25 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 26 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 3 ships | all 40 |
| 27 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 3 ships | all 40 |
| 28 | [carry-liner-first-step-to-ramens](carry-liner-first-step-to-ramens.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 6 chemical_liner stored at first_step_memorial_station, while ramens_rest bids 900 cr for chemical_liner | 1 of 40 |
| 29 | [trade-run-cinderspice-nova-terra](trade-run-cinderspice-nova-terra.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 8 jumps | once per pilot, up to 1 ships, from 35,000 cr, while nova_terra_central bids 3000 cr for cinderspice, while central_nexus asks 3020 cr or less for cinderspice | 1 of 40 |
| 30 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | 1 of 40 |
| 31 | [trade-control-node-gamma-to-factory-belt](trade-control-node-gamma-to-factory-belt.json) | [Tests](index-tests.md) | beyond the border, 23 jumps | up to 1 ships, empty hold, from 30,000 cr, while factory_belt_manufacturing_hub bids 700 cr for control_node, while node_gamma_relay_station asks 410 cr or less for control_node | 1 of 40 |
| 32 | [carry-hydrogen-beta-to-nova-terra](carry-hydrogen-beta-to-nova-terra.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, with 65 hydrogen_gas stored at node_beta_industrial_station, while nova_terra_central bids 35 cr for hydrogen_gas | all 40 |
| 33 | [carry-lead-beta-to-sirius](carry-lead-beta-to-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 30 lead_ore stored at node_beta_industrial_station, while sirius_observatory_station bids 35 cr for lead_ore | all 40 |
| 34 | [carry-lead-nexus-to-sirius](carry-lead-nexus-to-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 30 lead_ore stored at central_nexus, while sirius_observatory_station bids 35 cr for lead_ore | all 40 |
| 35 | [carry-lead-beta-to-grand-exchange](carry-lead-beta-to-grand-exchange.json) | [Tests](index-tests.md) | beyond the border, 21 jumps | up to 1 ships, with 30 lead_ore stored at node_beta_industrial_station, while grand_exchange_station bids 200 cr for lead_ore | all 40 |
| 36 | [carry-lead-nexus-to-grand-exchange](carry-lead-nexus-to-grand-exchange.json) | [Tests](index-tests.md) | beyond the border, 21 jumps | up to 1 ships, with 30 lead_ore stored at central_nexus, while grand_exchange_station bids 200 cr for lead_ore | all 40 |
| 37 | [carry-curd-beta-to-procyon](carry-curd-beta-to-procyon.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 25 verdigris_curd stored at node_beta_industrial_station, while procyon_colonial_station bids 315 cr for verdigris_curd | all 40 |
| 38 | [carry-curd-nexus-to-procyon](carry-curd-nexus-to-procyon.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 25 verdigris_curd stored at central_nexus, while procyon_colonial_station bids 315 cr for verdigris_curd | all 40 |
| 39 | [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 null_matter stored at node_beta_industrial_station, while central_nexus bids 200 cr for null_matter | all 40 |
| 40 | [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 null_matter stored at central_nexus, while central_nexus bids 200 cr for null_matter | all 40 |
| 41 | [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 30 null_matter stored at synchrony_hub, while central_nexus bids 150 cr for null_matter | all 40 |
| 42 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | all 40 |
| 43 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | all 40 |
| 44 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | all 40 |
| 45 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | all 40 |
| 46 | [sell-soma-at-experiment](sell-soma-at-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at the_experiment_research_station, while the_experiment_research_station bids 320 cr for voidborn_neural_soma | all 40 |
| 47 | [carry-palladium-nexus-to-gamma](carry-palladium-nexus-to-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 palladium_ore stored at central_nexus, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 48 | [sell-palladium-at-node-gamma](sell-palladium-at-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 palladium_ore stored at node_gamma_relay_station, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 49 | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 30 cr for hydrogen_gas | all 40 |
| 50 | [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_gamma_relay_station, while node_gamma_relay_station bids 30 cr for hydrogen_gas | all 40 |
| 51 | [sell-hydrogen-at-synchrony](sell-hydrogen-at-synchrony.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while synchrony_hub bids 30 cr for hydrogen_gas | all 40 |
| 52 | [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while the_experiment_research_station bids 30 cr for hydrogen_gas | all 40 |
| 53 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 54 | [craft-piping-synchrony-hub](craft-piping-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at synchrony_hub, 60 copper_ore stored at synchrony_hub, standing work | all 40 |
| 55 | [craft-steel-own-node-beta](craft-steel-own-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 56 | [craft-steel-own-experiment](craft-steel-own-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 40 |
| 57 | [craft-steel-own-central-nexus](craft-steel-own-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 100 iron_ore stored at central_nexus, standing work | all 40 |
| 58 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | all 40 |
| 59 | [craft-wiring-node-beta](craft-wiring-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 80 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 60 | [craft-wiring-experiment](craft-wiring-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at the_experiment_research_station, standing work | all 40 |
| 61 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 62 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 40 |
| 63 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 40 |
| 64 | [train-jumps-trader](train-jumps-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 40 |
| 65 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [trade-sell](templates-trade.md) | 40 |
| [trade-craft](templates-trade.md) | 40 |

Planned:

| What | When |
|---|---|
| Read the two far buy-and-sell tests and the far carries; lift a test that paid twice, one ship more | next turn |
| Take one Trade Run mission by hand on a far gap's road (deadline, hand-in, which skill), then an accept stop on the route | next turn |
