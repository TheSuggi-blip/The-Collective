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

Kept by Apollo. Routes: 115. Ships: 95.

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
| 24 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 95 |
| 25 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 95 |
| 26 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 20 ships | all 95 |
| 27 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 95 |
| 28 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 95 |
| 29 | [mission-the-memorial-frontier](mission-the-memorial-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 15 ships | all 95 |
| 30 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 95 |
| 31 | [mission-a-word-in-private-grand](mission-a-word-in-private-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 5 ships, born nebula | all 95 |
| 32 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 95 |
| 33 | [mission-scraping-by-frontier](mission-scraping-by-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 17 jumps | once per pilot, up to 1 ships, empty hold, born outerrim | all 95 |
| 34 | [mission-last-known-position-crimson](mission-last-known-position-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 15 ships | all 95 |
| 35 | [mission-strategic-readiness-assessment-crimson](mission-strategic-readiness-assessment-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 30 ships | all 95 |
| 36 | [strip-pulse-laser-central-nexus](strip-pulse-laser-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr, born voidborn | all 95 |
| 37 | [strip-mining-laser-krynn](strip-mining-laser-krynn.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 95 |
| 38 | [mission-structural-reinforcement-alpha](mission-structural-reinforcement-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 20 ships, empty hold | all 95 |
| 39 | [mission-filed-in-triplicate-nova](mission-filed-in-triplicate-nova.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 40 ships | all 95 |
| 40 | [mission-first-hunt-ironhearth](mission-first-hunt-ironhearth.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships | all 95 |
| 41 | [join-krynn-trader](join-krynn-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 15 ships, empty hold, born voidborn, standing work | all 95 |
| 42 | [mission-first-hunt-ironhearth-rigel](mission-first-hunt-ironhearth-rigel.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships, empty hold | all 95 |
| 43 | [mission-blood-forge-requisition-krynn](mission-blood-forge-requisition-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 36 ships, empty hold | all 95 |
| 44 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 10 ships | all 95 |
| 45 | [mission-first-hunt-iron-reach-rigel](mission-first-hunt-iron-reach-rigel.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 1 ships, empty hold | all 95 |
| 46 | [mission-request-for-records-confederacy](mission-request-for-records-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 61 ships | all 95 |
| 47 | [strip-mining-laser-krynn-hauler](strip-mining-laser-krynn-hauler.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 60 pilots in all, from 3,000 cr | all 95 |
| 48 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 95 |
| 49 | [mission-old-charts-sol](mission-old-charts-sol.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | once per pilot, up to 8 ships, empty hold, from 5,000 cr, under corporation_management 7, standing work | all 95 |
| 50 | [mission-courier-to-haven-sol-hauler](mission-courier-to-haven-sol-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | once per pilot, up to 45 ships, empty hold, under corporation_management 7, standing work | all 95 |
| 51 | [mission-diplomatic-pouch-haven-gold](mission-diplomatic-pouch-haven-gold.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | once per pilot, up to 70 ships, from 5,000 cr, under corporation_management 7, standing work | all 95 |
| 52 | [finish-prospectus-levy-haven](finish-prospectus-levy-haven.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | once per pilot, up to 43 ships, under corporation_management 7, standing work | all 95 |
| 53 | [finish-wayfinder-short](finish-wayfinder-short.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | once per pilot, up to 12 ships, under corporation_management 7, standing work | all 95 |
| 54 | [finish-prospectus-cache-haven](finish-prospectus-cache-haven.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 24 jumps | once per pilot, up to 9 ships, under corporation_management 7, standing work | all 95 |
| 55 | [finish-wayfinder-full](finish-wayfinder-full.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships, under corporation_management 7, standing work | all 95 |
| 56 | [mission-five-capitals-diplomatic-circuit-confederacy](mission-five-capitals-diplomatic-circuit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 4 ships | all 95 |
| 57 | [mission-the-colonies-crimson](mission-the-colonies-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | 1 of 95 |
| 58 | [finish-first-links-grand](finish-first-links-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 8 ships, born nebula, while grand_exchange_station asks 128 cr or less for nickel_ore | 6 of 95 |
| 59 | [craft-steel-logistics-cargo-lanes](craft-steel-logistics-cargo-lanes.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, with 100 iron_ore stored at cargo_lanes_freight_depot, standing work | 1 of 95 |
| 60 | [craft-steel-logistics-grand-exchange](craft-steel-logistics-grand-exchange.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 1 ships, with 100 iron_ore stored at grand_exchange_station, standing work | 1 of 95 |
| 61 | [craft-steel-logistics-factory-belt](craft-steel-logistics-factory-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 23 jumps | up to 1 ships, with 100 iron_ore stored at factory_belt_manufacturing_hub, standing work | 1 of 95 |
| 62 | [craft-steel-logistics-alpha-centauri](craft-steel-logistics-alpha-centauri.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 2 ships, with 100 iron_ore stored at alpha_centauri_colonial_station, standing work | 2 of 95 |
| 63 | [craft-steel-logistics-confederacy](craft-steel-logistics-confederacy.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, with 100 iron_ore stored at confederacy_central_command, standing work | 1 of 95 |
| 64 | [store-hold-frontier-station](store-hold-frontier-station.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 12 ships, goods aboard, born outerrim, standing work | 30 of 95 |
| 65 | [mission-the-objection-deep](mission-the-objection-deep.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | 1 of 95 |
| 66 | [mission-the-expeditionary-mandate-first](mission-the-expeditionary-mandate-first.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | 2 of 95 |
| 67 | [mission-voidborn-trajectory-unknown](mission-voidborn-trajectory-unknown.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 16 jumps | once per pilot, up to 3 ships | 1 of 95 |
| 68 | [mission-the-swing-vote-first](mission-the-swing-vote-first.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | 1 of 95 |
| 69 | [join-krynn-hauler-foreign](join-krynn-hauler-foreign.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 25 ships, empty hold, born nebula, outerrim, standing work | 50 of 95 |
| 70 | [mission-first-links-nickel-grand](mission-first-links-nickel-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 8 ships, from 4,300 cr, born nebula, while grand_exchange_station asks 128 cr or less for nickel_ore | 25 of 95 |
| 71 | [mission-market-participation-grand](mission-market-participation-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships, from 3,200 cr, while grand_exchange_station bids 1 cr for liquid_nitrogen | 25 of 95 |
| 72 | [mission-market-participation-frontier](mission-market-participation-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 17 jumps | once per pilot, up to 3 ships, from 3,200 cr, while frontier_station bids 1 cr for copper_ore | 30 of 95 |
| 73 | [join-sol-hauler-nexus](join-sol-hauler-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 15 ships, born outerrim, standing work | 26 of 95 |
| 74 | [join-sol-hauler-rim](join-sol-hauler-rim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 1 ships, empty hold, born outerrim, standing work | 26 of 95 |
| 75 | [craft-steel-logistics-ramens-rest](craft-steel-logistics-ramens-rest.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, with 100 iron_ore stored at ramens_rest, standing work | 1 of 95 |
| 76 | [craft-boards-crescent-moon](craft-boards-crescent-moon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, empty hold, with 10 silicon_ore stored at ec315132a710a7d0fbc68cca05073154, 120 carbon_ore stored at ec315132a710a7d0fbc68cca05073154, standing work | 1 of 95 |
| 77 | [craft-steel-logistics-crescent-moon](craft-steel-logistics-crescent-moon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, with 100 iron_ore stored at ec315132a710a7d0fbc68cca05073154, standing work | 1 of 95 |
| 78 | [finish-prospectus-full-haven](finish-prospectus-full-haven.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 24 jumps | once per pilot, up to 2 ships, under corporation_management 7, standing work | 2 of 95 |
| 79 | [mission-cracking-the-shell-krynn](mission-cracking-the-shell-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships, after the reward First Hunt: Belt-Grazers | 1 of 95 |
| 80 | [mission-83d4aab496f36cd12fbed259b3f534bf-central](mission-83d4aab496f36cd12fbed259b3f534bf-central.json) | [Tests](index-tests.md) | home space | up to 3 ships | 1 of 95 |
| 81 | [outpost-kit-ironlight-to-node-beta](outpost-kit-ironlight-to-node-beta.json) | [Tests](index-tests.md) | beyond the border, 6 jumps | up to 1 ships, 1 pilots in all, empty hold, from 152,000 cr, while 784309214f105860a16a0c100a70eb14 asks 148663 cr or less for outpost_kit | 1 of 95 |
| 82 | [supply-repair-gsc-0044-boards](supply-repair-gsc-0044-boards.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, from 5,000 cr, with 30 circuit_board stored at node_beta_industrial_station, standing work | 34 of 95 |
| 83 | [supply-repair-gsc-0044-plate](supply-repair-gsc-0044-plate.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 6 pilots in all, from 5,000 cr, with 100 steel_plate stored at node_beta_industrial_station, standing work | 34 of 95 |
| 84 | [supply-bunker-gsc-0044-own-cells](supply-bunker-gsc-0044-own-cells.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 5,000 cr, with 29 fuel_cell stored at node_beta_industrial_station, standing work | 34 of 95 |
| 85 | [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 12,000 cr, standing work | 34 of 95 |
| 86 | [give-hauler-stores-node-beta](give-hauler-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_beta_industrial_station, standing work | 40 of 95 |
| 87 | [give-hauler-stores-node-gamma](give-hauler-stores-node-gamma.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 neon_gas stored at node_gamma_relay_station, standing work | 40 of 95 |
| 88 | [give-hauler-stores-nova-terra](give-hauler-stores-nova-terra.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 2 ships, with 50 argon_gas stored at nova_terra_central, standing work | 40 of 95 |
| 89 | [give-hauler-stores-central-nexus](give-hauler-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 water_ice stored at central_nexus, standing work | 40 of 95 |
| 90 | [craft-boards-stored-node-beta](craft-boards-stored-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 silicon_ore stored at node_beta_industrial_station, 120 carbon_ore stored at node_beta_industrial_station, standing work | 40 of 95 |
| 91 | [craft-gold-wiring-synchrony-hub](craft-gold-wiring-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 40 gold_ore stored at synchrony_hub, standing work | 40 of 95 |
| 92 | [craft-gold-wiring-experiment](craft-gold-wiring-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 40 gold_ore stored at the_experiment_research_station, standing work | 40 of 95 |
| 93 | [craft-cells-hydrogen-node-beta](craft-cells-hydrogen-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, with 160 hydrogen_gas stored at node_beta_industrial_station, standing work | 40 of 95 |
| 94 | [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at the_experiment_research_station, standing work | 40 of 95 |
| 95 | [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 12 ships, with 100 iron_ore stored at node_beta_industrial_station, standing work | 40 of 95 |
| 96 | [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at synchrony_hub, standing work | 40 of 95 |
| 97 | [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 100 iron_ore stored at central_nexus, standing work | 40 of 95 |
| 98 | [craft-steel-logistics-procyon](craft-steel-logistics-procyon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 2 ships, with 100 iron_ore stored at procyon_colonial_station, standing work | 41 of 95 |
| 99 | [craft-steel-logistics-nova-terra](craft-steel-logistics-nova-terra.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 2 ships, with 100 iron_ore stored at nova_terra_central, standing work | 41 of 95 |
| 100 | [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, with 130 steel_plate stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | 40 of 95 |
| 101 | [join-sol-loop-home](join-sol-loop-home.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 10 ships, empty hold, under corporation_management 7, standing work | 5 of 95 |
| 102 | [join-sol-hauler](join-sol-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 50 ships, standing work | 27 of 95 |
| 103 | [join-krynn-hauler](join-krynn-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 13 ships, empty hold, born voidborn, standing work | 15 of 95 |
| 104 | [join-nova-hauler](join-nova-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | once per pilot, up to 15 ships, empty hold, born voidborn, standing work | 39 of 95 |
| 105 | [join-rim-hauler](join-rim-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | once per pilot, up to 15 ships, empty hold, born voidborn, nebula, standing work | 63 of 95 |
| 106 | [train-jumps-hauler](train-jumps-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | 11 of 95 |
| 107 | [buy-steel-reserve-central-nexus](buy-steel-reserve-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, while central_nexus asks 19 cr or less for steel_plate, under corporation_management 7, standing work | all 95 |
| 108 | [builder-home-node-beta](builder-home-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 1 ships, standing work | all 95 |
| 109 | [buy-carbon-reserve-node-beta](buy-carbon-reserve-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, while node_beta_industrial_station asks 4 cr or less for carbon_ore, standing work | all 95 |
| 110 | [join-sol-sirius](join-sol-sirius.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 45 ships, empty hold, under corporation_management 7, standing work | all 95 |
| 111 | [join-sol-records](join-sol-records.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 61 ships, empty hold, under corporation_management 7, standing work | all 95 |
| 112 | [join-rim-debris](join-rim-debris.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | once per pilot, up to 30 ships, empty hold, under corporation_management 7, standing work | all 95 |
| 113 | [join-krynn-bloodforge](join-krynn-bloodforge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 60 ships, empty hold, under corporation_management 7, standing work | all 95 |
| 114 | [haul-network](haul-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 87 ships, under corporation_management 7, standing work | all 95 |
| 115 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 95 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [stored-goods](templates-logistics.md) | 40 |
| [craft-reserve](templates-logistics.md) | 40 |
| [outpost-supply](templates-logistics.md) | 34 |
| [train-hauler](templates-logistics.md) | 11 |
| [newborn-rim](templates-logistics.md) | 30 |
| [newborn-nebula](templates-logistics.md) | 25 |

Planned:

| What | When |
|---|---|
| read Unity's answer to requests ENT-523 (Atria kit: Arneb, our own kit line, or wait) and write its buy routes and build row the same turn | next turn |
| read haul-network without its arbitrage lane: runs with a freight or supply job against runs that found none; size it to what freight and supply carry | next turn |
| read the carbon buy's three-cycle runs (no stall rest) against its gate of 50,000 and the overshoot after one storage-book interval | next turn |
