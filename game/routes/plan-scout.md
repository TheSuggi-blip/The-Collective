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

Kept by Oracle. Routes: 59. Ships: 30.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 30 |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 30 |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 30 |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 30 |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 30 |
| 6 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 30 |
| 7 | [census-voidborn](census-voidborn.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 4 ships | all 30 |
| 8 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 30 |
| 9 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 30 |
| 10 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 30 |
| 11 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 30 |
| 12 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 30 |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 30 |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 30 |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 30 |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 30 |
| 17 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 30 |
| 18 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 |
| 19 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 30 |
| 20 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | 1 of 30 |
| 21 | [hunt-pleione-ice-fields-hollow-pilgrim](hunt-pleione-ice-fields-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 30 |
| 22 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | 1 of 30 |
| 23 | [hunt-alnilam-frozen-drift-hollow-pilgrim](hunt-alnilam-frozen-drift-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 10 jumps | up to 1 ships, empty hold | 1 of 30 |
| 24 | [hunt-gsc-0021-ice-fields-hollow-pilgrim](hunt-gsc-0021-ice-fields-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 30 |
| 25 | [hunt-achernar-frost-ring-hollow-pilgrim](hunt-achernar-frost-ring-hollow-pilgrim.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 30 |
| 26 | [hunt-intercrus-ice-fields-hollow-pilgrim](hunt-intercrus-ice-fields-hollow-pilgrim.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 9 jumps | up to 1 ships, empty hold | 1 of 30 |
| 27 | [mine-flicker-fray](mine-flicker-fray.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 30 |
| 28 | [mine-nightveil-dark-residue](mine-nightveil-dark-residue.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 30 |
| 29 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 6 jumps | up to 1 ships, empty hold, standing work | 1 of 30 |
| 30 | [hunt-titawin-gas-cloud-chlorophage](hunt-titawin-gas-cloud-chlorophage.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, empty hold, standing work | 1 of 30 |
| 31 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, empty hold | 1 of 30 |
| 32 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 30 |
| 33 | [fit-survey-scanner-central-nexus](fit-survey-scanner-central-nexus.json) | [Fitting](index-fitting.md) | home space | once per pilot, up to 1 ships, 7 pilots in all, without survey_scanner_i, from 12,000 cr | 5 of 30 |
| 34 | [hunt-birchwood-vapor-fields-cinder-sylph](hunt-birchwood-vapor-fields-cinder-sylph.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 18 jumps | up to 1 ships, empty hold | 1 of 30 |
| 35 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | 1 of 30 |
| 36 | [hunt-amberfall-chlorophage-sac](hunt-amberfall-chlorophage-sac.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 1 ships, empty hold, standing work | 1 of 30 |
| 37 | [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1 of 30 |
| 38 | [census-watch-gsc-0044](census-watch-gsc-0044.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 4 ships, empty hold | 20 of 30 |
| 39 | [census-worked](census-worked.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 6 ships, empty hold | 20 of 30 |
| 40 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 30 |
| 41 | [census-north](census-north.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 15 jumps | up to 6 ships, empty hold | all 30 |
| 42 | [census-far-2](census-far-2.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 26 jumps | up to 2 ships, empty hold | 3 of 30 |
| 43 | [census-far-5](census-far-5.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 24 jumps | up to 2 ships, empty hold | 1 of 30 |
| 44 | [census-far-1](census-far-1.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 27 jumps | up to 3 ships, empty hold | 4 of 30 |
| 45 | [census-east](census-east.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 14 jumps | up to 3 ships, empty hold | all 30 |
| 46 | [census-far-4](census-far-4.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 29 jumps | up to 2 ships, empty hold | 2 of 30 |
| 47 | [census-south](census-south.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 4 ships, empty hold | all 30 |
| 48 | [census-far-3](census-far-3.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 29 jumps | up to 2 ships, empty hold | 2 of 30 |
| 49 | [census-roads](census-roads.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 17 jumps | up to 10 ships, empty hold | all 30 |
| 50 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 30 |
| 51 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 120 ships, needs mining_laser_i, standing work | all 30 |
| 52 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, needs mining_laser_i, standing work | all 30 |
| 53 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 30 |
| 54 | [gather-schedar-belt](gather-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 45 ships, needs mining_laser_i, empty hold, standing work | all 30 |
| 55 | [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 35 ships, needs mining_laser_i, empty hold, standing work | all 30 |
| 56 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 30 |
| 57 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 30 |
| 58 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 30 |
| 59 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 30 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [explorer](templates-intel.md) | 10 |
| [reader](templates-intel.md) | 20 |

Planned:

| What | When |
|---|---|
| Goal of the turn of 19:15 UTC, read at about 23:15 UTC: every system of census-north and census-south read once at least (their rows), the outpost watch's longest gap under 60 minutes (WATCH line), scanning XP gained by the five scanner readers, exploration's median 3 held and the first scout at 4 | next turn |
| Read the first rows of census-north and census-south (reads an hour, fuel, pirates met) and name the site candidates again on fresh reads | next turn |
| A Mining Survey Probe (180 cr) with the scanner scout at Homam: does +30 survey power resolve the faint signature | next turn |
| Read the RESERVE line of the intel check: a scout route that sells a good the reserve keeps stores from that turn | every turn |
| Keep GSC-0044 and its six neighbours read every hour (census-watch-gsc-0044, every 35 minutes, 4 ships) | every turn |
| Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 4 | every turn |
| Signal Fragments for every scout with navigation 3 (requires.skills) | every turn |
| Read the game's changelog at every turn and name each line of game/rules/ a release makes wrong in a request to the Fleet Admiral | every turn |
