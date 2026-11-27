---
name: routes-plan-sentinel
id: 20261116T174335Z
tier: intel
author: Unity
---

# plan-sentinel.md -- The Plan of the Role sentinel

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/sentinel.json`:
the routes the sentinel ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/sentinel.json` is written from it. `Planned` is what the Admiral
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Apophis. Routes: 87. Ships: 70.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [buy-autocannon-rounds-node-beta](buy-autocannon-rounds-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 3 ships, 20 pilots in all, needs autocannon_i or autocannon_ii, from 3,000 cr, while node_beta_industrial_station asks 2 cr or less for standard_rounds_box, standing work | all 70 |
| 2 | [buy-autocannon-rounds-central-nexus](buy-autocannon-rounds-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | once per pilot, up to 3 ships, 20 pilots in all, needs autocannon_i or autocannon_ii, from 3,000 cr, while central_nexus asks 2 cr or less for standard_rounds_box, standing work | all 70 |
| 3 | [buy-autocannon-rounds-the-anvil](buy-autocannon-rounds-the-anvil.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 3 ships, 20 pilots in all, needs autocannon_i or autocannon_ii, from 5,000 cr, while the_anvil_arsenal asks 15 cr or less for standard_rounds_box, standing work | all 70 |
| 4 | [rearm-pulse-laser-central-nexus](rearm-pulse-laser-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 5 ships, 20 pilots in all, without ['pulse_laser_i', 'pulse_laser_ii', 'pulse_laser_iii', 'focused_beam_i', 'plasma_cannon_ii', 'piercing_railgun_i'], from 3,000 cr, with 1 pulse_laser_i stored at central_nexus | all 70 |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 70 |
| 6 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 70 |
| 7 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 70 |
| 8 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 70 |
| 9 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 70 |
| 10 | [voidborn-crystal-resonance](voidborn-crystal-resonance.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, empty hold, after the reward The Collective Provides | all 70 |
| 11 | [voidborn-material-synthesis](voidborn-material-synthesis.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, 1 pilots in all, after the reward The Collective Provides | all 70 |
| 12 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 70 |
| 13 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 70 |
| 14 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 70 |
| 15 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 70 |
| 16 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 70 |
| 17 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 70 |
| 18 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 70 |
| 19 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 70 |
| 20 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 70 |
| 21 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 70 |
| 22 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 70 |
| 23 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 70 |
| 24 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 70 |
| 25 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 70 |
| 26 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 70 |
| 27 | [recursion-parts-sensor-void-node-beta](recursion-parts-sensor-void-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 1 pilots in all, empty hold, from 16,000 cr, while node_beta_industrial_station bids 850 cr for sensor_array, node_beta_industrial_station bids 400 cr for void_condensate, while 784309214f105860a16a0c100a70eb14 asks 900 cr or less for sensor_array | all 70 |
| 28 | [recursion-parts-silicate-node-beta](recursion-parts-silicate-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 1 pilots in all, empty hold, from 26,000 cr, while node_beta_industrial_station bids 420 cr for silicate_composite, while 784309214f105860a16a0c100a70eb14 asks 540 cr or less for silicate_composite | all 70 |
| 29 | [recursion2-parts-ironlight-mix-node-beta](recursion2-parts-ironlight-mix-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 2 pilots in all, empty hold, from 22,000 cr, while node_beta_industrial_station bids 420 cr for silicate_composite, while 784309214f105860a16a0c100a70eb14 asks 546 cr or less for silicate_composite | all 70 |
| 30 | [recursion2-parts-ironlight-silicate-node-beta](recursion2-parts-ironlight-silicate-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 1 ships, 2 pilots in all, empty hold, from 16,000 cr, while node_beta_industrial_station bids 420 cr for silicate_composite, while 784309214f105860a16a0c100a70eb14 asks 546 cr or less for silicate_composite | all 70 |
| 31 | [recursion2-parts-procyon-titanium-a-node-beta](recursion2-parts-procyon-titanium-a-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 1 ships, 3 pilots in all, empty hold, from 15,000 cr, while node_beta_industrial_station bids 800 cr for titanium_alloy, while procyon_colonial_station asks 900 cr or less for titanium_alloy | all 70 |
| 32 | [recursion2-parts-procyon-titanium-b-node-beta](recursion2-parts-procyon-titanium-b-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 1 ships, 3 pilots in all, empty hold, from 15,000 cr, while node_beta_industrial_station bids 800 cr for titanium_alloy, while procyon_colonial_station asks 900 cr or less for titanium_alloy | all 70 |
| 33 | [fit-pulse-laser-iii-lhs-1140](fit-pulse-laser-iii-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, 19 pilots in all, needs pulse_laser_i, without pulse_laser_iii, empty hold, from 17,000 cr, while 784309214f105860a16a0c100a70eb14 asks 14000 cr or less for pulse_laser_iii | all 70 |
| 34 | [fit-shield-booster-ii-lhs-1140](fit-shield-booster-ii-lhs-1140.json) | [Fitting](index-fitting.md) | beyond the border, 6 jumps | once per pilot, 34 pilots in all, needs pulse_laser_iii, without shield_booster_ii, empty hold, from 15,000 cr, while 784309214f105860a16a0c100a70eb14 asks 8000 cr or less for shield_booster_ii | all 70 |
| 35 | [fit-armor-plate-ii-krynn-test](fit-armor-plate-ii-krynn-test.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, 5 pilots in all, without armor_plate_ii, empty hold, from 5,000 cr, born crimson, while crimson_war_citadel asks 1500 cr or less for armor_plate_ii | all 70 |
| 36 | [fit-armor-plate-ii-sol-test](fit-armor-plate-ii-sol-test.json) | [Fitting](index-fitting.md) | beyond the border, 10 jumps | once per pilot, 17 pilots in all, without armor_plate_ii, empty hold, from 5,000 cr, born solarian, while confederacy_central_command asks 1400 cr or less for armor_plate_ii | all 70 |
| 37 | [strip-mining-laser-central-nexus](strip-mining-laser-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 70 |
| 38 | [strip-mining-laser-node-beta](strip-mining-laser-node-beta.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 70 |
| 39 | [strip-mining-laser-krynn](strip-mining-laser-krynn.json) | [Fitting](index-fitting.md) | beyond the border, 20 jumps | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 70 |
| 40 | [strip-mining-laser-sol](strip-mining-laser-sol.json) | [Fitting](index-fitting.md) | beyond the border, 10 jumps | once per pilot, up to 10 ships, 130 pilots in all, from 3,000 cr | all 70 |
| 41 | [give-mining-laser-sol-central](give-mining-laser-sol-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 5 ships, 40 pilots in all, from 3,000 cr, with 1 mining_laser_i stored at confederacy_central_command | all 70 |
| 42 | [load-plasma-ammo-nova-terra](load-plasma-ammo-nova-terra.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 8 jumps | up to 1 ships, 2 pilots in all, needs plasma_cannon_ii, with 1 dispersal_plasma_cell_pack stored at nova_terra_central, standing work | all 70 |
| 43 | [buy-plasma-ammo-central-nexus](buy-plasma-ammo-central-nexus.json) | [Tests](index-tests.md) | home space | up to 1 ships, 2 pilots in all, needs plasma_cannon_ii, from 15,000 cr, while central_nexus asks 200 cr or less for dispersal_plasma_cell_pack | all 70 |
| 44 | [give-drone-stores-node-beta](give-drone-stores-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 creature_carapace stored at node_beta_industrial_station, standing work | all 70 |
| 45 | [give-drone-stores-experiment](give-drone-stores-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 creature_carapace stored at the_experiment_research_station, standing work | all 70 |
| 46 | [give-drone-stores-synchrony](give-drone-stores-synchrony.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 creature_carapace stored at synchrony_hub, standing work | all 70 |
| 47 | [give-drone-stores-central-nexus](give-drone-stores-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 20 creature_carapace stored at central_nexus, standing work | all 70 |
| 48 | [give-drone-stores-node-alpha](give-drone-stores-node-alpha.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 20 nitrogen_ice stored at node_alpha_processing_station, standing work | all 70 |
| 49 | [give-drone-stores-first-step](give-drone-stores-first-step.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, with 20 creature_carapace stored at first_step_memorial_station, standing work | all 70 |
| 50 | [give-drone-stores-crucible](give-drone-stores-crucible.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 18 jumps | up to 1 ships, with 2 ember_gland stored at the_crucible_garrison, standing work | all 70 |
| 51 | [give-drone-stores-hexstar](give-drone-stores-hexstar.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 11 jumps | up to 1 ships, with 2 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, standing work | all 70 |
| 52 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 70 |
| 53 | [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 10 ships | all 70 |
| 54 | [mission-federation-market-analysis-market](mission-federation-market-analysis-market.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 23 jumps | once per pilot, up to 80 ships | all 70 |
| 55 | [mission-form-ta-1-confederacy](mission-form-ta-1-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 70 |
| 56 | [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 20 ships | all 70 |
| 57 | [mission-confederacy-infrastructure-audit-confederacy](mission-confederacy-infrastructure-audit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 90 ships | all 70 |
| 58 | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 24 jumps | once per pilot, up to 80 ships | all 70 |
| 59 | [mission-the-memorial-frontier](mission-the-memorial-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 18 jumps | once per pilot, up to 15 ships | all 70 |
| 60 | [mission-the-proposal-frontier](mission-the-proposal-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 70 |
| 61 | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 3 ships | all 70 |
| 62 | [mission-welcome-sol-central](mission-welcome-sol-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 3 ships, born solarian | all 70 |
| 63 | [mission-strategic-readiness-assessment-crimson](mission-strategic-readiness-assessment-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 30 ships | all 70 |
| 64 | [mission-last-known-position-crimson](mission-last-known-position-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 15 ships | all 70 |
| 65 | [mission-endorsements-alpha](mission-endorsements-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 50 ships | all 70 |
| 66 | [mission-voidborn-trajectory-unknown](mission-voidborn-trajectory-unknown.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 16 jumps | once per pilot, up to 3 ships | all 70 |
| 67 | [mission-structural-reinforcement-alpha](mission-structural-reinforcement-alpha.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 11 jumps | once per pilot, up to 20 ships, empty hold | all 70 |
| 68 | [join-krynn-trader](join-krynn-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 20 jumps | once per pilot, up to 15 ships, empty hold, born voidborn, standing work | all 70 |
| 69 | [mission-first-hunt-iron-reach-rigel](mission-first-hunt-iron-reach-rigel.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 1 ships, empty hold | all 70 |
| 70 | [mission-blood-forge-requisition-krynn](mission-blood-forge-requisition-krynn.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 36 ships, empty hold | all 70 |
| 71 | [mission-five-capitals-diplomatic-circuit-confederacy](mission-five-capitals-diplomatic-circuit-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 4 ships | all 70 |
| 72 | [mission-request-for-records-confederacy](mission-request-for-records-confederacy.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 20 jumps | once per pilot, up to 61 ships | all 70 |
| 73 | [mission-filed-in-triplicate-nova](mission-filed-in-triplicate-nova.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 40 ships | all 70 |
| 74 | [mission-first-hunt-ironhearth-rigel](mission-first-hunt-ironhearth-rigel.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships, empty hold | all 70 |
| 75 | [fit-network](fit-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 40 ships, standing work | all 70 |
| 76 | [mission-the-colonies-crimson](mission-the-colonies-crimson.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | all 70 |
| 77 | [mission-the-line-ironhearth](mission-the-line-ironhearth.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 3 ships | all 70 |
| 78 | [hunt-network-packs](hunt-network-packs.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 26 ships, standing work | all 70 |
| 79 | [hunt-network](hunt-network.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | -- | up to 140 ships, standing work | all 70 |
| 80 | [store-hold-sol-central-far](store-hold-sol-central-far.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 10 ships, goods aboard, born solarian, standing work | all 70 |
| 81 | [guard-ironhollow-fading-signal](guard-ironhollow-fading-signal.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, empty hold, standing work | all 70 |
| 82 | [guard-schedar-belt](guard-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 1 ships, empty hold, standing work | all 70 |
| 83 | [guard-ironhollow-echo-ejecta](guard-ironhollow-echo-ejecta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, empty hold, standing work | all 70 |
| 84 | [guard-garnet-belt](guard-garnet-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, empty hold, standing work | all 70 |
| 85 | [guard-achernar-belt](guard-achernar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, empty hold, standing work | all 70 |
| 86 | [guard-marfik-emission-nebula](guard-marfik-emission-nebula.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | all 70 |
| 87 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 70 |

Planned:

| What | When |
|---|---|
| Commission the first Recursion by hand at Node Beta once the Fleet Admiral's fund step pays the first drone at Piloting 10 (one ship, F17); fly its first hunts by route | next turn |
| Group whale hunt proven (three kills): ask for a group route kind so the dispatcher flies it, and test one Shield Booster II on a Laser III ship against a whale alone | next turn |
