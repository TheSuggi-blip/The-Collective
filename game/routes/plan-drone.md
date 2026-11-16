---
name: routes-plan-drone
id: 20261116T174331Z
tier: intel
author: Unity
---

# plan-drone.md -- The Plan of the Role drone

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/drone.json`:
the routes the drone ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/drone.json` is written from it. `Planned` is what the Admiral
means to do next. Up: [master-index.md](master-index.md).

Kept by Apophis. Routes: 39. Ships: 30.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 30 | one-time |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 30 | one-time |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 30 | one-time |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 30 | one-time |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 30 | one-time |
| 6 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 30 | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 30 | one-time |
| 8 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 9 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 10 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 30 | one-time |
| 11 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 30 | one-time |
| 12 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 30 | one-time |
| 13 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 30 | one-time |
| 14 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 30 | one-time |
| 15 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 30 | one-time |
| 16 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 30 | one-time |
| 17 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 30 | one-time |
| 18 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 30 | TBD |
| 19 | [sell-curd-central-nexus](sell-curd-central-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 2 verdigris_curd stored at central_nexus, while central_nexus bids 250 cr for verdigris_curd | all 30 | 302,820 |
| 20 | [sell-curd-node-beta](sell-curd-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 2 verdigris_curd stored at node_beta_industrial_station, while node_beta_industrial_station bids 250 cr for verdigris_curd | all 30 | 29,370 |
| 21 | [sell-curd-experiment](sell-curd-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 2 verdigris_curd stored at the_experiment_research_station, while the_experiment_research_station bids 250 cr for verdigris_curd | all 30 | 13,390 |
| 22 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 100 cr for ember_gland | all 30 | 6,720 |
| 23 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, without piercing_railgun_i, while central_nexus bids 100 cr for verdigris_curd | all 30 | 3,020 |
| 24 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, without piercing_railgun_i, while central_nexus bids 100 cr for verdigris_curd | all 30 | 2,310 |
| 25 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 100 cr for verdigris_curd | all 30 | 2,100 |
| 26 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for verdigris_curd | all 30 | 1,420 |
| 27 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for verdigris_curd | all 30 | 1,300 |
| 28 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for ember_gland | all 30 | 600 |
| 29 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 100 cr for verdigris_curd | all 30 | 840 |
| 30 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for verdigris_curd | all 30 | 800 |
| 31 | [train-navigation-home](train-navigation-home.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships | all 30 | -470 |
| 32 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 33 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 | one-time |
| 34 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 30 | one-time |
| 35 | [census-guard-ice](census-guard-ice.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 2 ships, empty hold | all 30 | -610 |
| 36 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 30 | -120 |
| 37 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 30 | -170 |
| 38 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 30 | -630 |
| 39 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 30 | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of the seven veil-ray hunts once the loss stop's six-hour window passes their losing runs of 07:05 to 09:20 UTC, and of First Hunt and Cracking the Shell at Achernar on their herd floor; drop a route at its second losing run in a row. | next Military turn |
| Navigation 3 opens Signal Fragments (7,000 cr once) to the 19 drones at navigation 2: measure which drone route gains the most navigation XP per credit of fuel (ship files before and after), then put the drones nearest to level 3 on it. | next Military turn |
| Carapace into armor plate where it lies (orders ENT-013, APOPHIS (6)): plate.py over all drones, no plate sold past a bid's depth. | every turn |
| Guard: the route kind guard (owed by Unity, requests.log ENT-070, her turn of 18:30 UTC) replaces census-guard-ice with one drone beside each mine route beyond the border. | when the guard kind exists |
| The next hull: no purchase while every hunt is bounded by its herd and its bid; a tier-1 Vigil as one test only for prey over 100 hull, which needs an order beyond F9. | on an order |
