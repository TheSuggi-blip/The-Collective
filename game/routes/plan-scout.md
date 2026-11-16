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

Kept by Oracle. Routes: 26. Ships: 30.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 30 |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 30 |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 30 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 30 |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 30 |
| 6 | [census-voidborn](census-voidborn.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships | all 30 |
| 7 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 30 |
| 8 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 30 |
| 9 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 30 |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 30 |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 30 |
| 12 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 30 |
| 13 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 30 |
| 14 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 30 |
| 15 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 30 |
| 16 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 30 |
| 17 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 |
| 18 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 |
| 19 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 30 |
| 20 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 30 |
| 21 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 30 |
| 22 | [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 30 |
| 23 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 30 |
| 24 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 30 |
| 25 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 30 |
| 26 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 30 |

Planned:

| What | When |
|---|---|
| Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 3; read the gaps per system every turn and change the threshold only on a measured gap over 60 minutes | every turn |
| Read the first RESULT line of voidborn-first-hunt-intercrus-belt after its loss stop lapses (about 09:30 UTC); if it pays, voidborn-first-hunt-intercrus-remnants and a route at Intercrus Sootfall Belt (16 belt-grazers at 08:17 UTC) for the rest of the scouts without First Hunt | next turn |
| Signal Fragments: 11 scouts with navigation 3; ask Trade for more places (requests.log ENT-118); the nine with navigation 2 fly it when they reach 3 | every turn |
| Fourth ring (Felis, Acrab, Botein, Acrux): belt-grazer herds of 11 to 14 and two pirates; a hunt route there only after a drop of the species sells and Military has looked at the pirates | when a herd's drop sells |
| Nova Terra Central (Solarian) read about once a day while Trade weighs a trade | daily |
| Read the game's changelog at every turn and name each line of game/rules/ a release makes wrong in a request to the Fleet Admiral | every turn |
