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

Kept by Apollo. Routes: 74. Ships: 90.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 90 |
| 2 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 90 |
| 3 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 90 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 90 |
| 5 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 90 |
| 6 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 90 |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 90 |
| 8 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 90 |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 90 |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 90 |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 90 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 90 |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 90 |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 90 |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 90 |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 90 |
| 17 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 90 |
| 18 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 90 |
| 19 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 90 |
| 20 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 90 |
| 21 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 90 |
| 22 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 90 |
| 23 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 90 |
| 24 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 90 |
| 25 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 90 |
| 26 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 20 ships | all 90 |
| 27 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 90 |
| 28 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 90 |
| 29 | [mission-the-memorial-frontier](mission-the-memorial-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 15 ships | all 90 |
| 30 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 90 |
| 31 | [mission-a-word-in-private-grand](mission-a-word-in-private-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 5 ships, born nebula | all 90 |
| 32 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 90 |
| 33 | [mission-scraping-by-frontier](mission-scraping-by-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 17 jumps | once per pilot, up to 1 ships, empty hold, born outerrim | all 90 |
| 34 | [mission-last-known-position-crimson](mission-last-known-position-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 15 ships | all 90 |
| 35 | [mission-strategic-readiness-assessment-crimson](mission-strategic-readiness-assessment-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 30 ships | all 90 |
| 36 | [strip-pulse-laser-central-nexus](strip-pulse-laser-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr, born voidborn | all 90 |
| 37 | [strip-mining-laser-krynn](strip-mining-laser-krynn.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 90 |
| 38 | [mission-structural-reinforcement-alpha](mission-structural-reinforcement-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 20 ships, empty hold | all 90 |
| 39 | [mission-filed-in-triplicate-nova](mission-filed-in-triplicate-nova.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 40 ships | all 90 |
| 40 | [mission-first-hunt-ironhearth](mission-first-hunt-ironhearth.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships | all 90 |
| 41 | [join-krynn-trader](join-krynn-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 15 ships, empty hold, born voidborn, standing work | all 90 |
| 42 | [mission-first-hunt-ironhearth-rigel](mission-first-hunt-ironhearth-rigel.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships, empty hold | all 90 |
| 43 | [mission-blood-forge-requisition-krynn](mission-blood-forge-requisition-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 36 ships, empty hold | all 90 |
| 44 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 10 ships | all 90 |
| 45 | [mission-first-hunt-iron-reach-rigel](mission-first-hunt-iron-reach-rigel.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 1 ships, empty hold | all 90 |
| 46 | [mission-request-for-records-confederacy](mission-request-for-records-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 61 ships | all 90 |
| 47 | [strip-mining-laser-krynn-hauler](strip-mining-laser-krynn-hauler.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 60 pilots in all, from 3,000 cr | all 90 |
| 48 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 90 |
| 49 | [mission-old-charts-sol](mission-old-charts-sol.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | once per pilot, up to 8 ships, empty hold, from 5,000 cr, under corporation_management 7, standing work | all 90 |
| 50 | [mission-courier-to-haven-sol-hauler](mission-courier-to-haven-sol-hauler.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | once per pilot, up to 45 ships, empty hold, under corporation_management 7, standing work | all 90 |
| 51 | [mission-diplomatic-pouch-haven-gold](mission-diplomatic-pouch-haven-gold.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | once per pilot, up to 70 ships, from 5,000 cr, under corporation_management 7, standing work | all 90 |
| 52 | [finish-prospectus-levy-haven](finish-prospectus-levy-haven.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | once per pilot, up to 43 ships, under corporation_management 7, standing work | all 90 |
| 53 | [finish-wayfinder-short](finish-wayfinder-short.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | once per pilot, up to 12 ships, under corporation_management 7, standing work | all 90 |
| 54 | [finish-prospectus-cache-haven](finish-prospectus-cache-haven.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 24 jumps | once per pilot, up to 9 ships, under corporation_management 7, standing work | all 90 |
| 55 | [finish-wayfinder-full](finish-wayfinder-full.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships, under corporation_management 7, standing work | all 90 |
| 56 | [mission-five-capitals-diplomatic-circuit-confederacy](mission-five-capitals-diplomatic-circuit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 4 ships | all 90 |
| 57 | [fit-network](fit-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 40 ships, standing work | all 90 |
| 58 | [mission-the-expeditionary-mandate-first](mission-the-expeditionary-mandate-first.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | all 90 |
| 59 | [mission-the-colonies-crimson](mission-the-colonies-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | all 90 |
| 60 | [buy-steel-reserve-central-nexus](buy-steel-reserve-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, while central_nexus asks 19 cr or less for steel_plate, under corporation_management 7, standing work | all 90 |
| 61 | [builder-home-node-beta](builder-home-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 1 ships, standing work | all 90 |
| 62 | [buy-carbon-reserve-node-beta](buy-carbon-reserve-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | while node_beta_industrial_station asks 4 cr or less for carbon_ore, standing work | all 90 |
| 63 | [join-sol-sirius](join-sol-sirius.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 45 ships, empty hold, under corporation_management 7, standing work | all 90 |
| 64 | [join-sol-records](join-sol-records.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | once per pilot, up to 61 ships, empty hold, under corporation_management 7, standing work | all 90 |
| 65 | [join-rim-debris](join-rim-debris.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | once per pilot, up to 30 ships, empty hold, under corporation_management 7, standing work | all 90 |
| 66 | [join-krynn-bloodforge](join-krynn-bloodforge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 60 ships, empty hold, under corporation_management 7, standing work | all 90 |
| 67 | [craft-network](craft-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 12 ships, standing work | all 90 |
| 68 | [haul-network-builder](haul-network-builder.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 1 ships, from corporation_management 7, standing work | all 90 |
| 69 | [haul-network](haul-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 100 ships, under corporation_management 7, standing work | all 90 |
| 70 | [supply-bunker-gsc-0044-own-cells](supply-bunker-gsc-0044-own-cells.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 5,000 cr, with 29 fuel_cell stored at node_beta_industrial_station, standing work | all 90 |
| 71 | [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, from 12,000 cr, standing work | all 90 |
| 72 | [supply-bunker-atria-own-cells](supply-bunker-atria-own-cells.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, empty hold, from 5,000 cr, with 29 fuel_cell stored at node_beta_industrial_station, standing work | all 90 |
| 73 | [supply-bunker-atria](supply-bunker-atria.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, empty hold, from 12,000 cr, while node_alpha_processing_station asks 101 cr or less for fuel_cell, standing work | all 90 |
| 74 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 90 |

Planned:

| What | When |
|---|---|
| read the kit row's RESULT lines: Outpost Kit crafted in our assembler at Node Beta, Atria founded at its belt; then the Atria bunker and its fuel chain | next turn |
| haul-network: read runs with a job against docked watch; escorted lawless freight (Ironlight LHS 1140 to Gold Run, about 100 cr a jump) only when Military's escort lane reopens | next turn |
| Guild Hall at GSC-0044 (Center first, then Hall; 225 seats by the game's best-office rule): stage plate, boards, flex and alloy only when the 24-hour net reads zero | at the gate |
