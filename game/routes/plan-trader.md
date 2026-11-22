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

Kept by Mercury. Routes: 96. Ships: 40.

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
| 30 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | all 40 |
| 31 | [trade-control-node-gamma-to-factory-belt](trade-control-node-gamma-to-factory-belt.json) | [Tests](index-tests.md) | beyond the border, 23 jumps | up to 1 ships, empty hold, from 30,000 cr, while factory_belt_manufacturing_hub bids 700 cr for control_node, while node_gamma_relay_station asks 410 cr or less for control_node | 1 of 40 |
| 32 | [sell-loot-at-krynn](sell-loot-at-krynn.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 2 ember_gland stored at crimson_war_citadel, while crimson_war_citadel bids 5000 cr for ember_gland | all 40 |
| 33 | [sell-loot-at-dheneb](sell-loot-at-dheneb.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, with 3 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 4500 cr for ember_gland | all 40 |
| 34 | [sell-ember-node-beta-krynn](sell-ember-node-beta-krynn.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, with 4 ember_gland stored at node_beta_industrial_station, while crimson_war_citadel bids 5000 cr for ember_gland | all 40 |
| 35 | [sell-ember-nexus-krynn](sell-ember-nexus-krynn.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 20 jumps | up to 1 ships, with 3 ember_gland stored at central_nexus, while crimson_war_citadel bids 5000 cr for ember_gland | all 40 |
| 36 | [sell-ember-hexstar-krynn](sell-ember-hexstar-krynn.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 20 jumps | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while crimson_war_citadel bids 5000 cr for ember_gland | all 40 |
| 37 | [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 40 |
| 38 | [sell-ember-experiment-dheneb](sell-ember-experiment-dheneb.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at the_experiment_research_station, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | all 40 |
| 39 | [sell-ember-hexstar-first-step](sell-ember-hexstar-first-step.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while first_step_memorial_station bids 5000 cr for ember_gland | all 40 |
| 40 | [sell-loot-at-synchrony](sell-loot-at-synchrony.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 2 crystal_melt stored at synchrony_hub, while synchrony_hub bids 1400 cr for crystal_melt | all 40 |
| 41 | [sell-loot-at-experiment](sell-loot-at-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 crystal_melt stored at the_experiment_research_station, while the_experiment_research_station bids 1000 cr for crystal_melt | all 40 |
| 42 | [carry-melt-sirius-to-experiment](carry-melt-sirius-to-experiment.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 10 crystal_melt stored at sirius_observatory_station, while the_experiment_research_station bids 1000 cr for crystal_melt | all 40 |
| 43 | [carry-melt-first-step-to-experiment](carry-melt-first-step-to-experiment.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 20 crystal_melt stored at first_step_memorial_station, while the_experiment_research_station bids 1000 cr for crystal_melt | all 40 |
| 44 | [sell-melt-at-sirius](sell-melt-at-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 1 crystal_melt stored at sirius_observatory_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 40 |
| 45 | [sell-melt-experiment-sirius](sell-melt-experiment-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at the_experiment_research_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 40 |
| 46 | [sell-melt-nexus-sirius](sell-melt-nexus-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 3 crystal_melt stored at central_nexus, while sirius_observatory_station bids 1000 cr for crystal_melt | all 40 |
| 47 | [sell-melt-node-beta-sirius](sell-melt-node-beta-sirius.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at node_beta_industrial_station, while sirius_observatory_station bids 1000 cr for crystal_melt | all 40 |
| 48 | [sell-melt-synchrony-sirius](sell-melt-synchrony-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 2 crystal_melt stored at synchrony_hub, while sirius_observatory_station bids 1000 cr for crystal_melt | all 40 |
| 49 | [sell-loot-at-node-beta](sell-loot-at-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 noble_condensate stored at node_beta_industrial_station, while node_beta_industrial_station bids 680 cr for noble_condensate | all 40 |
| 50 | [sell-loot-at-first-step](sell-loot-at-first-step.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 30 verdigris_curd stored at first_step_memorial_station, while first_step_memorial_station bids 300 cr for verdigris_curd | all 40 |
| 51 | [sell-noble-at-first-step](sell-noble-at-first-step.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 10 noble_condensate stored at first_step_memorial_station, while first_step_memorial_station bids 680 cr for noble_condensate | all 40 |
| 52 | [sell-loot-at-nova-terra](sell-loot-at-nova-terra.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, with 20 verdigris_curd stored at nova_terra_central, while nova_terra_central bids 300 cr for verdigris_curd | all 40 |
| 53 | [sell-noble-at-nova-terra](sell-noble-at-nova-terra.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, with 10 noble_condensate stored at nova_terra_central, while nova_terra_central bids 680 cr for noble_condensate | all 40 |
| 54 | [carry-hydrogen-beta-to-nova-terra](carry-hydrogen-beta-to-nova-terra.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, with 65 hydrogen_gas stored at node_beta_industrial_station, while nova_terra_central bids 35 cr for hydrogen_gas | all 40 |
| 55 | [carry-lead-beta-to-sirius](carry-lead-beta-to-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 30 lead_ore stored at node_beta_industrial_station, while sirius_observatory_station bids 35 cr for lead_ore | all 40 |
| 56 | [carry-lead-nexus-to-sirius](carry-lead-nexus-to-sirius.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 30 lead_ore stored at central_nexus, while sirius_observatory_station bids 35 cr for lead_ore | all 40 |
| 57 | [carry-lead-beta-to-grand-exchange](carry-lead-beta-to-grand-exchange.json) | [Tests](index-tests.md) | beyond the border, 21 jumps | up to 1 ships, with 30 lead_ore stored at node_beta_industrial_station, while grand_exchange_station bids 200 cr for lead_ore | all 40 |
| 58 | [carry-lead-nexus-to-grand-exchange](carry-lead-nexus-to-grand-exchange.json) | [Tests](index-tests.md) | beyond the border, 21 jumps | up to 1 ships, with 30 lead_ore stored at central_nexus, while grand_exchange_station bids 200 cr for lead_ore | all 40 |
| 59 | [carry-curd-beta-to-procyon](carry-curd-beta-to-procyon.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 25 verdigris_curd stored at node_beta_industrial_station, while procyon_colonial_station bids 315 cr for verdigris_curd | all 40 |
| 60 | [carry-curd-nexus-to-procyon](carry-curd-nexus-to-procyon.json) | [Tests](index-tests.md) | beyond the border, 9 jumps | up to 1 ships, with 25 verdigris_curd stored at central_nexus, while procyon_colonial_station bids 315 cr for verdigris_curd | all 40 |
| 61 | [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 null_matter stored at node_beta_industrial_station, while central_nexus bids 200 cr for null_matter | all 40 |
| 62 | [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 null_matter stored at central_nexus, while central_nexus bids 200 cr for null_matter | all 40 |
| 63 | [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 30 null_matter stored at synchrony_hub, while central_nexus bids 150 cr for null_matter | all 40 |
| 64 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | all 40 |
| 65 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | all 40 |
| 66 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | all 40 |
| 67 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | all 40 |
| 68 | [sell-soma-at-experiment](sell-soma-at-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at the_experiment_research_station, while the_experiment_research_station bids 320 cr for voidborn_neural_soma | all 40 |
| 69 | [carry-palladium-nexus-to-gamma](carry-palladium-nexus-to-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 palladium_ore stored at central_nexus, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 70 | [sell-palladium-at-node-gamma](sell-palladium-at-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 palladium_ore stored at node_gamma_relay_station, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 71 | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 30 cr for hydrogen_gas | all 40 |
| 72 | [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_gamma_relay_station, while node_gamma_relay_station bids 30 cr for hydrogen_gas | all 40 |
| 73 | [sell-hydrogen-at-synchrony](sell-hydrogen-at-synchrony.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while synchrony_hub bids 30 cr for hydrogen_gas | all 40 |
| 74 | [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while the_experiment_research_station bids 30 cr for hydrogen_gas | all 40 |
| 75 | [drain-ice-node-alpha](drain-ice-node-alpha.json) | [Tests](index-tests.md) | home space | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | all 40 |
| 76 | [drain-ice-nexus](drain-ice-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | all 40 |
| 77 | [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | all 40 |
| 78 | [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | all 40 |
| 79 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | all 40 |
| 80 | [sell-deuterium-at-node-beta](sell-deuterium-at-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 deuterium_ice stored at node_beta_industrial_station, while node_beta_industrial_station bids 150 cr for deuterium_ice | all 40 |
| 81 | [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at central_nexus, while central_nexus bids 100 cr for liquid_hydrogen | all 40 |
| 82 | [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at node_beta_industrial_station, while node_beta_industrial_station bids 95 cr for liquid_hydrogen | all 40 |
| 83 | [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 10 liquid_hydrogen stored at node_beta_industrial_station, while central_nexus bids 110 cr for liquid_hydrogen | all 40 |
| 84 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 85 | [craft-piping-synchrony-hub](craft-piping-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at synchrony_hub, 60 copper_ore stored at synchrony_hub, standing work | all 40 |
| 86 | [craft-steel-own-node-beta](craft-steel-own-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 87 | [craft-steel-own-experiment](craft-steel-own-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | all 40 |
| 88 | [craft-steel-own-central-nexus](craft-steel-own-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 100 iron_ore stored at central_nexus, standing work | all 40 |
| 89 | [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at synchrony_hub, standing work | all 40 |
| 90 | [craft-wiring-node-beta](craft-wiring-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 10 ships, with 80 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 91 | [craft-wiring-experiment](craft-wiring-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 80 copper_ore stored at the_experiment_research_station, standing work | all 40 |
| 92 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 93 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 40 |
| 94 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 40 |
| 95 | [train-jumps-trader](train-jumps-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 40 |
| 96 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 |

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
