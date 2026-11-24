---
name: routes-plan-scout
id: 20261116T174334Z
tier: intel
author: Unity
---

# plan-scout.md -- The Plan of the Role scout

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/scout.json`:
the routes the scout ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/scout.json` is written from it. `Planned` is what the Admiral
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Oracle. Routes: 102. Ships: 50.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 55 ships, goods aboard, standing work | all 50 |
| 2 | [store-hold-frontier-station-near](store-hold-frontier-station-near.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 12 ships, goods aboard, standing work | all 50 |
| 3 | [give-mining-laser-scout-central-nexus](give-mining-laser-scout-central-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 5 ships, 30 pilots in all, from 3,000 cr, with 1 mining_laser_i stored at central_nexus | all 50 |
| 4 | [give-scout-stores-node-beta](give-scout-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at node_beta_industrial_station, standing work | all 50 |
| 5 | [give-scout-stores-central-nexus](give-scout-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at central_nexus, standing work | all 50 |
| 6 | [give-scout-stores-synchrony](give-scout-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at synchrony_hub, standing work | all 50 |
| 7 | [give-scout-stores-experiment](give-scout-stores-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at the_experiment_research_station, standing work | all 50 |
| 8 | [fit-survey-scanner-ii-central-nexus](fit-survey-scanner-ii-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 1 pilots in all, needs survey_scanner_i, without ['survey_scanner_ii'], from 18,000 cr, while central_nexus asks 14000 cr or less for survey_scanner_ii | all 50 |
| 9 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 50 |
| 10 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 50 |
| 11 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 50 |
| 12 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 50 |
| 13 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 50 |
| 14 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 50 |
| 15 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 50 |
| 16 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 50 |
| 17 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 |
| 18 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 50 |
| 19 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 50 |
| 20 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 50 |
| 21 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 50 |
| 22 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 |
| 23 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 50 |
| 24 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 25 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 26 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 50 |
| 27 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 28 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 |
| 29 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 50 |
| 30 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 50 |
| 31 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 50 |
| 32 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 50 |
| 33 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 50 |
| 34 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 50 |
| 35 | [mission-the-objection-deep](mission-the-objection-deep.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 50 |
| 36 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 50 |
| 37 | [mission-a-word-in-private-grand](mission-a-word-in-private-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 5 ships, born nebula | all 50 |
| 38 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 50 |
| 39 | [mission-voidborn-trajectory-unknown](mission-voidborn-trajectory-unknown.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 16 jumps | once per pilot, up to 3 ships | all 50 |
| 40 | [mission-last-known-position-crimson](mission-last-known-position-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 15 ships | all 50 |
| 41 | [mission-filed-in-triplicate-nova](mission-filed-in-triplicate-nova.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 40 ships | all 50 |
| 42 | [mission-structural-reinforcement-alpha](mission-structural-reinforcement-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 20 ships, empty hold | all 50 |
| 43 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 10 ships | all 50 |
| 44 | [mission-the-memorial-frontier](mission-the-memorial-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 15 ships | all 50 |
| 45 | [mission-request-for-records-confederacy](mission-request-for-records-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 61 ships | all 50 |
| 46 | [join-krynn-bloodforge](join-krynn-bloodforge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 60 ships, empty hold, under corporation_management 7, standing work | all 50 |
| 47 | [mission-strategic-readiness-assessment-crimson](mission-strategic-readiness-assessment-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 30 ships | all 50 |
| 48 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 20 ships | all 50 |
| 49 | [mission-blood-forge-requisition-krynn](mission-blood-forge-requisition-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 36 ships, empty hold | all 50 |
| 50 | [mission-five-capitals-diplomatic-circuit-confederacy](mission-five-capitals-diplomatic-circuit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | all 50 |
| 51 | [store-hold-grand-exchange](store-hold-grand-exchange.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 35 ships, goods aboard, born nebula, standing work | 8 of 50 |
| 52 | [census-region-haven](census-region-haven.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 29 jumps | up to 6 ships, empty hold | 8 of 50 |
| 53 | [census-region-haven-ring](census-region-haven-ring.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 26 jumps | up to 2 ships, empty hold | 8 of 50 |
| 54 | [store-hold-frontier-station](store-hold-frontier-station.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 12 ships, goods aboard, born outerrim, standing work | 12 of 50 |
| 55 | [mission-scraping-by-frontier](mission-scraping-by-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 17 jumps | once per pilot, up to 1 ships, empty hold, born outerrim | 12 of 50 |
| 56 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | 12 of 50 |
| 57 | [census-region-altais](census-region-altais.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 23 jumps | up to 6 ships, empty hold | 12 of 50 |
| 58 | [census-region-altais-ring](census-region-altais-ring.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 2 ships, empty hold | 12 of 50 |
| 59 | [census-region-sol](census-region-sol.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 13 jumps | up to 2 ships, empty hold | 3 of 50 |
| 60 | [strip-gift-mining-laser-scout-central-nexus](strip-gift-mining-laser-scout-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 10 ships, 30 pilots in all, from 3,000 cr, born voidborn | 18 of 50 |
| 61 | [give-miner-stores-synchrony](give-miner-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 50 iron_ore or copper_ore or steel_plate or copper_piping or carbon_ore or silicon_ore or nickel_ore or gold_ore or platinum_ore or water_ice or nitrogen_ice or deuterium_ice or helium_ice or null_matter or lead_ore or voidborn_neural_soma or exotic_matter stored at synchrony_hub, standing work | 1 of 50 |
| 62 | [census-region-krynn](census-region-krynn.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 22 jumps | up to 3 ships, empty hold | 3 of 50 |
| 63 | [census-far-5](census-far-5.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 24 jumps | up to 2 ships, empty hold | 2 of 50 |
| 64 | [census-far-1](census-far-1.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 27 jumps | up to 3 ships, empty hold | 16 of 50 |
| 65 | [mission-the-expeditionary-mandate-first](mission-the-expeditionary-mandate-first.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | 1 of 50 |
| 66 | [census-kit-herds](census-kit-herds.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 29 jumps | up to 3 ships, empty hold | 3 of 50 |
| 67 | [census-far-4](census-far-4.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 29 jumps | up to 2 ships, empty hold | 11 of 50 |
| 68 | [census-far-3](census-far-3.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 29 jumps | up to 2 ships, empty hold | 11 of 50 |
| 69 | [census-far-2](census-far-2.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 25 jumps | up to 2 ships, empty hold | 11 of 50 |
| 70 | [census-roads](census-roads.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 14 jumps | up to 4 ships, empty hold | all 50 |
| 71 | [home-frontier-station](home-frontier-station.json) | [Tests](index-tests.md) | beyond the border, 17 jumps | up to 12 ships, empty hold, born outerrim | 12 of 50 |
| 72 | [census-voidborn](census-voidborn.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 5 ships | 20 of 50 |
| 73 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 74 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | 2 of 50 |
| 75 | [hunt-achernar-frost-ring-hollow-pilgrim](hunt-achernar-frost-ring-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 76 | [census-watch-gsc-0044](census-watch-gsc-0044.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 3 ships, empty hold | 20 of 50 |
| 77 | [hunt-intercrus-ice-fields-hollow-pilgrim](hunt-intercrus-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 78 | [census-worked](census-worked.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 6 ships, empty hold | 20 of 50 |
| 79 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | 30 of 50 |
| 80 | [hunt-pleione-ice-fields-hollow-pilgrim](hunt-pleione-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 81 | [hunt-alnilam-frozen-drift-hollow-pilgrim](hunt-alnilam-frozen-drift-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 82 | [hunt-gsc-0021-ice-fields-hollow-pilgrim](hunt-gsc-0021-ice-fields-hollow-pilgrim.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 9 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 83 | [hunt-birchwood-vapor-fields-cinder-sylph](hunt-birchwood-vapor-fields-cinder-sylph.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 84 | [hunt-amberfall-chlorophage-sac](hunt-amberfall-chlorophage-sac.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, empty hold, standing work | 1 of 50 |
| 85 | [census-worked-far](census-worked-far.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 29 jumps | up to 10 ships, empty hold | 30 of 50 |
| 86 | [census-north](census-north.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 6 ships, empty hold | 30 of 50 |
| 87 | [census-east](census-east.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 14 jumps | up to 3 ships, empty hold | 42 of 50 |
| 88 | [census-south](census-south.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 4 ships, empty hold | 30 of 50 |
| 89 | [watch-book-central-nexus](watch-book-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | all 50 |
| 90 | [watch-book-ramens-rest](watch-book-ramens-rest.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, standing work | all 50 |
| 91 | [watch-book-unknown-edge](watch-book-unknown-edge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, standing work | all 50 |
| 92 | [watch-book-alpha-centauri](watch-book-alpha-centauri.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, standing work | all 50 |
| 93 | [watch-book-gold-run](watch-book-gold-run.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, standing work | all 50 |
| 94 | [watch-book-the-levy](watch-book-the-levy.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, standing work | all 50 |
| 95 | [watch-book-factory-belt](watch-book-factory-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 23 jumps | up to 1 ships, standing work | all 50 |
| 96 | [watch-book-grand-exchange](watch-book-grand-exchange.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 1 ships, standing work | all 50 |
| 97 | [watch-book-cargo-lanes](watch-book-cargo-lanes.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, standing work | all 50 |
| 98 | [watch-book-deep-range](watch-book-deep-range.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, standing work | all 50 |
| 99 | [watch-book-starfall](watch-book-starfall.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, standing work | all 50 |
| 100 | [watch-book-ironlight-refuge](watch-book-ironlight-refuge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 22 jumps | up to 1 ships, standing work | all 50 |
| 101 | [watch-book-hex-star](watch-book-hex-star.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, standing work | all 50 |
| 102 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 50 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [explorer](templates-intel.md) | 10 |
| [reader](templates-intel.md) | 20 |
| [outerrim](templates-intel.md) | 12 |
| [nebula](templates-intel.md) | 8 |

Planned:

| What | When |
|---|---|
| Read the strip and give runs of the scouts' Mining Laser I (open within 2 jumps of Central Nexus since this turn) and the lasers Mining's receivers got (data/stock/handover.jsonl) | next turn |
| Read the Survey Scanner II scout's survey of Bnki (census-kit-herds, a faint signature at power 32): power 81 resolves it or not; resolved -> to Mining in queue.log; not -> a probe step by fleet-build | next turn |
| Weigh a tier-2 scout hull only by fuel a read against the Threshold (the tier-1 Qualia read 2.4 times the fuel a read on census-region-sol, 4 h runs) | once a T2 hull's fuel a jump is on record |
| Read the envoy's replies through diplomacy.py threads; Hail 2/3 to the eleven goes out by itself from 2026-11-25 09:27 UTC; replies to Unity as data | every turn |
| Judge census-south, census-north and census-frontier from four hours of reads: five, one and three systems stood 181 to 193 min against 180 (dispatch lag with every Voidborn scout busy); still over -> cadence 150 on that list | next turn |
