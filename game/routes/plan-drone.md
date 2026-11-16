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

Kept by Apophis. Routes: 44. Ships: 50.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 50 | one-time |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 50 | one-time |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 50 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 50 | one-time |
| 5 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 | one-time |
| 6 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 50 | one-time |
| 7 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 | one-time |
| 8 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 | one-time |
| 9 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 50 | one-time |
| 10 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 50 | one-time |
| 11 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 50 | one-time |
| 12 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 50 | one-time |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 50 | one-time |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 50 | one-time |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 50 | one-time |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 50 | one-time |
| 17 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 50 | one-time |
| 18 | [sell-plate-node-beta](sell-plate-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 armor_plate stored at node_beta_industrial_station, while node_beta_industrial_station bids 300 cr for armor_plate | 1 of 50 | 8,810 |
| 19 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 50 | 1,730 |
| 20 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 50 | 2,420 |
| 21 | [guard-marfik-emission-nebula](guard-marfik-emission-nebula.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | 3 of 50 | -110 |
| 22 | [sell-curd-central-nexus](sell-curd-central-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 2 verdigris_curd stored at central_nexus, while central_nexus bids 250 cr for verdigris_curd | all 50 | 302,820 |
| 23 | [sell-curd-node-beta](sell-curd-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 2 verdigris_curd stored at node_beta_industrial_station, while node_beta_industrial_station bids 250 cr for verdigris_curd | all 50 | 29,370 |
| 24 | [sell-curd-experiment](sell-curd-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 2 verdigris_curd stored at the_experiment_research_station, while the_experiment_research_station bids 250 cr for verdigris_curd | all 50 | 13,390 |
| 25 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | 2 of 50 | -170 |
| 26 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 50 | 1,500 |
| 27 | [census-guard-ice](census-guard-ice.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 2 ships, empty hold | 2 of 50 | -610 |
| 28 | [hunt-felis-frost-ring-hollow-pilgrim](hunt-felis-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 1000 cr for crystal_melt | 32 of 50 | -600 |
| 29 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 100 cr for ember_gland | 32 of 50 | 6,720 |
| 30 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | 32 of 50 | 2,360 |
| 31 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, without piercing_railgun_i, standing work | 32 of 50 | 2,310 |
| 32 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 32 of 50 | 2,100 |
| 33 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 32 of 50 | 1,420 |
| 34 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 32 of 50 | 1,020 |
| 35 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 32 of 50 | 840 |
| 36 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 32 of 50 | 620 |
| 37 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for ember_gland | 32 of 50 | 470 |
| 38 | [hunt-home-drift-ray](hunt-home-drift-ray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, standing work | 32 of 50 | -240 |
| 39 | [hunt-keid-belt-carapace](hunt-keid-belt-carapace.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 32 of 50 | -540 |
| 40 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 50 | -130 |
| 41 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 50 | -280 |
| 42 | [mine-acubens](mine-acubens.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | 12 of 50 | -170 |
| 43 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 50 | -940 |
| 44 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 50 | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of the seven veil-ray hunts once the loss stop's six-hour window passes their losing runs of 07:05 to 09:20 UTC, and of First Hunt and Cracking the Shell at Achernar on their herd floor; drop a route at its second losing run in a row. | next Military turn |
| Navigation 3 opens Signal Fragments (7,000 cr once) to the 19 drones at navigation 2: measure which drone route gains the most navigation XP per credit of fuel (ship files before and after), then put the drones nearest to level 3 on it. | next Military turn |
| Carapace into armor plate where it lies (orders ENT-013, APOPHIS (6)): plate.py over all drones, no plate sold past a bid's depth. | every turn |
| Guard: the route kind guard (owed by Unity, requests.log ENT-070, her turn of 18:30 UTC) replaces census-guard-ice with one drone beside each mine route beyond the border. | when the guard kind exists |
| The next hull: no purchase while every hunt is bounded by its herd and its bid; a tier-1 Vigil as one test only for prey over 100 hull, which needs an order beyond F9. | on an order |
