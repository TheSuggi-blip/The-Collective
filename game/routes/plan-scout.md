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
means to do next. Up: [master-index.md](master-index.md).

Kept by Oracle. Routes: 23. Ships: 20.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 20 | one-time |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 | one-time |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 20 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 | one-time |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 | one-time |
| 6 | [census-voidborn](census-voidborn.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships | all 20 | -530 |
| 7 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 20 | one-time |
| 8 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 20 | one-time |
| 9 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 20 | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 20 | one-time |
| 12 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 20 | one-time |
| 13 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 20 | one-time |
| 14 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 20 | one-time |
| 15 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 16 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 20 | one-time |
| 17 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 20 | TBD |
| 18 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | all 20 | 2,420 |
| 19 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | all 20 | 1,730 |
| 20 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 20 | -120 |
| 21 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 20 | -170 |
| 22 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 20 | -630 |
| 23 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 20 | -670 |

Planned:

| What | When |
|---|---|
| Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 3; read the gaps per system every turn and change the threshold only on a measured gap over 60 minutes | every turn |
| Read the first RESULT line of voidborn-first-hunt-intercrus-belt after its loss stop lapses (about 09:30 UTC); if it pays, voidborn-first-hunt-intercrus-remnants and a route at Intercrus Sootfall Belt (16 belt-grazers at 08:17 UTC) for the rest of the scouts without First Hunt | next turn |
| Signal Fragments: 11 scouts with navigation 3; ask Trade for more places (requests.log ENT-118); the nine with navigation 2 fly it when they reach 3 | every turn |
| Fourth ring (Felis, Acrab, Botein, Acrux): belt-grazer herds of 11 to 14 and two pirates; a hunt route there only after a drop of the species sells and Military has looked at the pirates | when a herd's drop sells |
| Nova Terra Central (Solarian) read about once a day while Trade weighs a trade | daily |
| Read the game's changelog at every turn and name each line of game/rules/ a release makes wrong in a request to the Fleet Admiral | every turn |
