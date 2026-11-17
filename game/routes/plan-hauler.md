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

Kept by Apollo. Routes: 57. Ships: 40.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 40 |
| 2 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 40 |
| 3 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 40 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 |
| 5 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 40 |
| 6 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 40 |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 40 |
| 8 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, while the_experiment_research_station bids 1 cr for copper_wiring | all 40 |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 40 |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 40 |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 40 |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 17 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 40 |
| 18 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 19 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 40 |
| 20 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 21 | [mine-grumium-belt](mine-grumium-belt.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 9 jumps | up to 1 ships | 1 of 40 |
| 22 | [craft-boards-node-beta](craft-boards-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, with 30 silicon_ore stored at node_beta_industrial_station, standing work | 1 of 40 |
| 23 | [gather-glasslight-shoal-silicon](gather-glasslight-shoal-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 10 jumps | up to 1 ships, empty hold, standing work | 1 of 40 |
| 24 | [craft-boards-gold-experiment](craft-boards-gold-experiment.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 1 ships, with 90 gold_ore stored at the_experiment_research_station, 90 copper_ore stored at the_experiment_research_station, 30 energy_crystal stored at the_experiment_research_station, standing work | 1 of 40 |
| 25 | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 30 cr for hydrogen_gas | all 40 |
| 26 | [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_gamma_relay_station, while node_gamma_relay_station bids 30 cr for hydrogen_gas | all 40 |
| 27 | [sell-hydrogen-at-synchrony](sell-hydrogen-at-synchrony.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while synchrony_hub bids 30 cr for hydrogen_gas | all 40 |
| 28 | [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while the_experiment_research_station bids 30 cr for hydrogen_gas | all 40 |
| 29 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | all 40 |
| 30 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | all 40 |
| 31 | [sell-soma-at-experiment](sell-soma-at-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at the_experiment_research_station, while the_experiment_research_station bids 320 cr for voidborn_neural_soma | all 40 |
| 32 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | all 40 |
| 33 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | all 40 |
| 34 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | all 40 |
| 35 | [sell-palladium-at-node-gamma](sell-palladium-at-node-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 palladium_ore stored at node_gamma_relay_station, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 36 | [carry-palladium-nexus-to-gamma](carry-palladium-nexus-to-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 palladium_ore stored at central_nexus, while node_gamma_relay_station bids 270 cr for palladium_ore | all 40 |
| 37 | [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at central_nexus, while central_nexus bids 100 cr for liquid_hydrogen | all 40 |
| 38 | [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at node_beta_industrial_station, while node_beta_industrial_station bids 95 cr for liquid_hydrogen | all 40 |
| 39 | [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 10 liquid_hydrogen stored at node_beta_industrial_station, while central_nexus bids 110 cr for liquid_hydrogen | all 40 |
| 40 | [mine-achernar-gas-pocket](mine-achernar-gas-pocket.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 4 of 40 |
| 41 | [mine-lesath-gas-cloud](mine-lesath-gas-cloud.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 4 of 40 |
| 42 | [mine-amberfall-emission-nebula](mine-amberfall-emission-nebula.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_gamma_relay_station bids 27 cr for hydrogen_gas | 4 of 40 |
| 43 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 40 |
| 44 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 40 |
| 45 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 40 |
| 46 | [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 8 ships, with 130 steel_plate stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 47 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | all 40 |
| 48 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 120 ships, needs mining_laser_i, standing work | all 40 |
| 49 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 40 |
| 50 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 40 |
| 51 | [gather-schedar-belt](gather-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 45 ships, needs mining_laser_i, empty hold, standing work | all 40 |
| 52 | [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 35 ships, needs mining_laser_i, empty hold, standing work | all 40 |
| 53 | [gather-okab-belt](gather-okab-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 42 ships, needs mining_laser_i, empty hold, standing work | all 40 |
| 54 | [gather-gj-3470-dewfall-fray](gather-gj-3470-dewfall-fray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 13 ships, needs mining_laser_i, empty hold, standing work | all 40 |
| 55 | [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, needs mining_laser_i, empty hold, standing work | all 40 |
| 56 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 40 |
| 57 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [stored-goods](templates-logistics.md) | 40 |
| [craft-reserve](templates-logistics.md) | 40 |
| [gather-reserve](templates-logistics.md) | 40 |
| [gas-harvest](templates-logistics.md) | 4 |

Planned:

| What | When |
|---|---|
| Goal: the outpost's bunker at 2,000 fuel or more, filled by a route (a runner step that burns cells into the tank and deposits it into the faction reserve, built through fleet-build with its test), its cost per unit read from its runs (1,276 fuel at 2026-11-17 21:17 UTC); read at the next turn | next turn |
| A flight of more than ten minutes goes into a route file, never a turn's shell (requests.log ENT-251, answered yes in ENT-252) | from the next turn |
| The outpost's fuel written into the supply chains (game/supply/chains.tsv) once the Fleet Admiral's supply.py stands | when it is committed |
| A shared flight-and-hold helper for found.py, build.py and outpost.py (goal option names written once, the hand kept fresh) | next turn |
| Haulers from the gather fields to the copper piping craft once the iron reserve reads met | when the reserve says so |
| The Recruitment Center (500 boards, 1,000 plate, 300 flex polymer, 2,000,000 cr) staged only on the Fleet Admiral's word | on her word |
| One Ledger or Prayer freighter quoted and flown on a carry, inside rule F12 | when a carry with a standing bid needs the hold |
