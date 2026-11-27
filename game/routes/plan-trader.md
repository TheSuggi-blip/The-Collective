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

Kept by Mercury. Routes: 87. Ships: 96.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [fit-network](fit-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 40 ships, standing work | all 96 |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 96 |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 96 |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 96 |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 96 |
| 6 | [voidborn-network-commerce](voidborn-network-commerce.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, empty hold, after the reward The Collective Provides, while central_nexus bids 4 cr for carbon_ore | all 96 |
| 7 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 96 |
| 8 | [voidborn-neural-matrix-board](voidborn-neural-matrix-board.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 4 ships | all 96 |
| 9 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 96 |
| 10 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 96 |
| 11 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 96 |
| 12 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 96 |
| 13 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 96 |
| 14 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 96 |
| 15 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 96 |
| 16 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 96 |
| 17 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 96 |
| 18 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 96 |
| 19 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 96 |
| 20 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 96 |
| 21 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 96 |
| 22 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 96 |
| 23 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 96 |
| 24 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 96 |
| 25 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 96 |
| 26 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 96 |
| 27 | [mission-voidborn-trajectory-unknown](mission-voidborn-trajectory-unknown.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 16 jumps | once per pilot, up to 3 ships | all 96 |
| 28 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 96 |
| 29 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 96 |
| 30 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 10 ships | all 96 |
| 31 | [mission-the-memorial-frontier](mission-the-memorial-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 15 ships | all 96 |
| 32 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 96 |
| 33 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 96 |
| 34 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 96 |
| 35 | [mission-welcome-sol-central](mission-welcome-sol-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 3 ships, born solarian | all 96 |
| 36 | [mission-a-word-in-private-grand](mission-a-word-in-private-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 5 ships, born nebula | all 96 |
| 37 | [mission-first-links-store-grand](mission-first-links-store-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 8 ships, from 4,300 cr, born nebula, while market_prime_exchange asks 180 cr or less for nickel_ore | all 96 |
| 38 | [mission-market-participation-grand](mission-market-participation-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships, from 3,200 cr, while grand_exchange_station bids 1 cr for liquid_nitrogen | all 96 |
| 39 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 96 |
| 40 | [mission-structural-reinforcement-alpha](mission-structural-reinforcement-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 20 ships, empty hold | all 96 |
| 41 | [mission-the-objection-deep](mission-the-objection-deep.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 96 |
| 42 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 96 |
| 43 | [mission-strategic-readiness-assessment-crimson](mission-strategic-readiness-assessment-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 30 ships | all 96 |
| 44 | [strip-mining-laser-krynn](strip-mining-laser-krynn.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 96 |
| 45 | [strip-pulse-laser-central-nexus](strip-pulse-laser-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr, born voidborn | all 96 |
| 46 | [mission-last-known-position-crimson](mission-last-known-position-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 15 ships | all 96 |
| 47 | [mission-filed-in-triplicate-nova](mission-filed-in-triplicate-nova.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 40 ships | all 96 |
| 48 | [mission-blood-forge-requisition-krynn](mission-blood-forge-requisition-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 36 ships, empty hold | all 96 |
| 49 | [need-melt-frontier](need-melt-frontier.json) | [Tests](index-tests.md) | beyond the border, 17 jumps | up to 1 ships, with 4 crystal_melt stored at frontier_station | all 96 |
| 50 | [need-melt-crucible](need-melt-crucible.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 12 crystal_melt stored at the_crucible_garrison | all 96 |
| 51 | [need-ember-gland-krynn](need-ember-gland-krynn.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 3 ember_gland stored at crimson_war_citadel | all 96 |
| 52 | [need-ember-gland-crucible](need-ember-gland-crucible.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, with 10 ember_gland stored at crimson_war_citadel | all 96 |
| 53 | [sell-ember-first-step-dheneb](sell-ember-first-step-dheneb.json) | [Tests](index-tests.md) | beyond the border, 18 jumps | up to 1 ships, with 6 ember_gland stored at first_step_memorial_station, while b495c6003fc83e18f6d8cecbe6929133 bids 4000 cr for ember_gland | all 96 |
| 54 | [sell-ember-synchrony-dheneb](sell-ember-synchrony-dheneb.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, with 6 ember_gland stored at synchrony_hub, while b495c6003fc83e18f6d8cecbe6929133 bids 4000 cr for ember_gland | all 96 |
| 55 | [sell-melt-at-dheneb](sell-melt-at-dheneb.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, with 5 crystal_melt stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 3000 cr for crystal_melt | all 96 |
| 56 | [sell-melt-nexus-dheneb](sell-melt-nexus-dheneb.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 2 ships, with 20 crystal_melt stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 3000 cr for crystal_melt | all 96 |
| 57 | [carry-sac-beta-to-hex-star](carry-sac-beta-to-hex-star.json) | [Tests](index-tests.md) | beyond the border, 11 jumps | up to 1 ships, with 30 caustic_sac stored at node_beta_industrial_station, while b495c6003fc83e18f6d8cecbe6929133 bids 1250 cr for caustic_sac | all 96 |
| 58 | [carry-ember-crucible-to-krynn](carry-ember-crucible-to-krynn.json) | [Tests](index-tests.md) | beyond the border, 20 jumps | up to 1 ships, empty hold, with 3 ember_gland stored at the_crucible_garrison | all 96 |
| 59 | [mission-request-for-records-confederacy](mission-request-for-records-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 61 ships | all 96 |
| 60 | [join-krynn-bloodforge](join-krynn-bloodforge.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 60 ships, empty hold, under corporation_management 7, standing work | all 96 |
| 61 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 20 ships | all 96 |
| 62 | [mission-workshop-production-run-krynn](mission-workshop-production-run-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, from 3,200 cr, born nebula, while crimson_war_citadel asks 60 cr or less for purified_water | all 96 |
| 63 | [fit-cargo-expander-ii-krynn](fit-cargo-expander-ii-krynn.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, 26 pilots in all, without ['cargo_expander_ii'], from 10,500 cr, while crimson_war_citadel asks 1430 cr or less for cargo_expander_ii | all 96 |
| 64 | [mission-the-colonies-crimson](mission-the-colonies-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | all 96 |
| 65 | [mission-the-expeditionary-mandate-first](mission-the-expeditionary-mandate-first.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | all 96 |
| 66 | [mission-first-hunt-iron-reach](mission-first-hunt-iron-reach.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships | all 96 |
| 67 | [mission-the-document-the](mission-the-document-the.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 3 ships | all 96 |
| 68 | [mission-the-swing-vote-first](mission-the-swing-vote-first.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 3 ships | all 96 |
| 69 | [strip-starters-trader-krynn](strip-starters-trader-krynn.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 85 pilots in all, from 3,000 cr | all 96 |
| 70 | [strip-starters-trader-alpha](strip-starters-trader-alpha.json) | [Fitting](index-fitting.md) | beyond the border, 11 jumps | once per pilot, up to 10 ships, 85 pilots in all, from 3,000 cr | all 96 |
| 71 | [strip-starters-trader-experiment](strip-starters-trader-experiment.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 10 ships, 85 pilots in all, from 3,000 cr | all 96 |
| 72 | [mission-workshop-production-run-grand](mission-workshop-production-run-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships, from 3,200 cr, born nebula, while grand_exchange_station asks 3 cr or less for argon_gas | all 96 |
| 73 | [haul-network-trade](haul-network-trade.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 30 ships, standing work | all 96 |
| 74 | [craft-network](craft-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 12 ships, standing work | all 96 |
| 75 | [bursar-network](bursar-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 55 ships, standing work | all 96 |
| 76 | [bursar-network-freighter](bursar-network-freighter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | standing work | all 96 |
| 77 | [bursar-desk-krynn](bursar-desk-krynn.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | standing work | all 96 |
| 78 | [bursar-desk-alpha](bursar-desk-alpha.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | standing work | all 96 |
| 79 | [bursar-desk-experiment](bursar-desk-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | standing work | all 96 |
| 80 | [bursar-desk-grand](bursar-desk-grand.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 21 jumps | standing work | all 96 |
| 81 | [bursar-desk-nova-terra](bursar-desk-nova-terra.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | standing work | all 96 |
| 82 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 96 |
| 83 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 96 |
| 84 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 96 |
| 85 | [train-trading-weapon-housing-node-alpha](train-trading-weapon-housing-node-alpha.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, while node_alpha_processing_station bids 221 cr for weapon_housing, while node_alpha_processing_station asks 230 cr or less for weapon_housing, standing work | all 96 |
| 86 | [train-jumps-trader](train-jumps-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 15 ships, from 5,000 cr, under navigation 6, piloting 10, standing work | all 96 |
| 87 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 96 |

Planned:

| What | When |
|---|---|
| read craft-network's first three runs on each of the three test rows (job, margin, what sold) before any lift | next turn |
| read the three Apophenia commissions at The Experiment after the owners supplied one neural gel each; the upgrade service switches them | next turn |
| read the first Meridian Freighter buys of the upgrade service (Sol, 10 jumps) and the fit-network fits of the mobile hulls | next turn |
| HEXC levity bladder (750, 55,125 cr) and fusion pearl (274, 69,048 cr) contracts at Krynn: consolidate once a 240+ cargo hull carries the Arneb lot | after the hull batch |
