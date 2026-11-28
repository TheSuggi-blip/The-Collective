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

Kept by Oracle. Routes: 73. Ships: 45.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 55 ships, goods aboard, standing work | all 45 |
| 2 | [store-hold-frontier-station-near](store-hold-frontier-station-near.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 12 ships, goods aboard, standing work | all 45 |
| 3 | [give-mining-laser-scout-central-nexus](give-mining-laser-scout-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 5 ships, 30 pilots in all, from 3,000 cr, with 1 mining_laser_i stored at central_nexus, standing work | all 45 |
| 4 | [give-scout-stores-node-beta](give-scout-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at node_beta_industrial_station, standing work | all 45 |
| 5 | [give-scout-stores-central-nexus](give-scout-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at central_nexus, standing work | all 45 |
| 6 | [give-scout-stores-synchrony](give-scout-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at synchrony_hub, standing work | all 45 |
| 7 | [give-scout-stores-experiment](give-scout-stores-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 50 iron_ore stored at the_experiment_research_station, standing work | all 45 |
| 8 | [fit-survey-scanner-ii-central-nexus](fit-survey-scanner-ii-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, 1 pilots in all, needs survey_scanner_i, without ['survey_scanner_ii'], from 18,000 cr, while central_nexus asks 14000 cr or less for survey_scanner_ii | all 45 |
| 9 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 45 |
| 10 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 45 |
| 11 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 45 |
| 12 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 45 |
| 13 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 45 |
| 14 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 45 |
| 15 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 45 |
| 16 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 45 |
| 17 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 45 |
| 18 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 45 |
| 19 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 45 |
| 20 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 45 |
| 21 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 45 |
| 22 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 45 |
| 23 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 45 |
| 24 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 45 |
| 25 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 45 |
| 26 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 45 |
| 27 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 45 |
| 28 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 45 |
| 29 | [mission-a-word-in-private-grand](mission-a-word-in-private-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 5 ships, born nebula | all 45 |
| 30 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 45 |
| 31 | [mission-voidborn-trajectory-unknown](mission-voidborn-trajectory-unknown.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 16 jumps | once per pilot, up to 3 ships | all 45 |
| 32 | [mission-last-known-position-crimson](mission-last-known-position-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 15 ships | all 45 |
| 33 | [mission-filed-in-triplicate-nova](mission-filed-in-triplicate-nova.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 40 ships | all 45 |
| 34 | [mission-structural-reinforcement-alpha](mission-structural-reinforcement-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 20 ships, empty hold | all 45 |
| 35 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 10 ships | all 45 |
| 36 | [mission-the-memorial-frontier](mission-the-memorial-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 15 ships | all 45 |
| 37 | [mission-request-for-records-confederacy](mission-request-for-records-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 61 ships | all 45 |
| 38 | [join-krynn-bloodforge](join-krynn-bloodforge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 60 ships, empty hold, under corporation_management 7, standing work | all 45 |
| 39 | [mission-strategic-readiness-assessment-crimson](mission-strategic-readiness-assessment-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 30 ships | all 45 |
| 40 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 20 ships | all 45 |
| 41 | [mission-blood-forge-requisition-krynn](mission-blood-forge-requisition-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 36 ships, empty hold | all 45 |
| 42 | [mission-five-capitals-diplomatic-circuit-confederacy](mission-five-capitals-diplomatic-circuit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 4 ships | all 45 |
| 43 | [finish-prospectus-levy-haven](finish-prospectus-levy-haven.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | once per pilot, up to 43 ships, under corporation_management 7, standing work | all 45 |
| 44 | [fit-network](fit-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 40 ships, standing work | all 45 |
| 45 | [mission-the-colonies-crimson](mission-the-colonies-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | all 45 |
| 46 | [mission-the-line-ironhearth](mission-the-line-ironhearth.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | all 45 |
| 47 | [census-network](census-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 45 ships, standing work | all 45 |
| 48 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 45 |
| 49 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 45 |
| 50 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 45 |
| 51 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 45 |
| 52 | [mission-first-hunt-iron-reach-rigel](mission-first-hunt-iron-reach-rigel.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 1 ships, empty hold | all 45 |
| 53 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 45 |
| 54 | [watch-book-central-nexus](watch-book-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | all 45 |
| 55 | [watch-book-node-beta](watch-book-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | all 45 |
| 56 | [watch-book-ramens-rest](watch-book-ramens-rest.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 1 ships, standing work | all 45 |
| 57 | [watch-book-unknown-edge](watch-book-unknown-edge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 16 jumps | up to 1 ships, standing work | all 45 |
| 58 | [watch-book-frontier-station](watch-book-frontier-station.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 1 ships, standing work | all 45 |
| 59 | [watch-book-alpha-centauri](watch-book-alpha-centauri.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, standing work | all 45 |
| 60 | [watch-book-gold-run](watch-book-gold-run.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, standing work | all 45 |
| 61 | [watch-book-the-levy](watch-book-the-levy.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, standing work | all 45 |
| 62 | [watch-book-factory-belt](watch-book-factory-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 23 jumps | up to 1 ships, standing work | all 45 |
| 63 | [watch-book-grand-exchange](watch-book-grand-exchange.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | up to 1 ships, standing work | all 45 |
| 64 | [watch-book-cargo-lanes](watch-book-cargo-lanes.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, standing work | all 45 |
| 65 | [watch-book-deep-range](watch-book-deep-range.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 19 jumps | up to 1 ships, standing work | all 45 |
| 66 | [watch-book-starfall](watch-book-starfall.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, standing work | all 45 |
| 67 | [watch-book-ironlight-refuge](watch-book-ironlight-refuge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 22 jumps | up to 1 ships, standing work | all 45 |
| 68 | [watch-book-hex-star](watch-book-hex-star.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, standing work | all 45 |
| 69 | [watch-book-crescent-moon](watch-book-crescent-moon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, standing work | all 45 |
| 70 | [watch-book-carnegie-hall](watch-book-carnegie-hall.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 1 ships, standing work | all 45 |
| 71 | [watch-book-treasure-cache](watch-book-treasure-cache.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 24 jumps | up to 1 ships, standing work | all 45 |
| 72 | [watch-book-zosma](watch-book-zosma.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | up to 1 ships, standing work | all 45 |
| 73 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 45 |

Planned:

| What | When |
|---|---|
| Read four hours of census-frontier at 145 min and SITES of census-north and census-region-altais after the move: still over the 3-hour target -> 10 min lower, never more ships | next turn |
| Read hive.py spend for Intel: modules bought once should read 0 after the loadouts were emptied; fit-network on scouts only strips | next turn |
| Measure fuel a jump of the scouts that carry a fuel optimizer against the rest before any module returns to an Intel loadout (P1) | next turn |
| Read the envoy's replies through diplomacy.py threads twice a turn; beacons go out by themselves (next round 2026-11-26 09:26 UTC); replies to Unity | every turn |
| Read the Survey Scanner II surveys (census-kit-herds): a faint signature resolved goes to Mining in queue.log | next turn |
| Weigh a tier-2 scout hull only by fuel a read against the Threshold (tests.md) and a payback within a week (P1); none bought until then | once a T2 hull's fuel a jump is on record |
