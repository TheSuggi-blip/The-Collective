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

Kept by Mercury. Routes: 41. Ships: 40.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 40 |
| 2 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 40 |
| 3 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 40 |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 40 |
| 5 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 40 |
| 6 | [voidborn-neural-matrix-board](voidborn-neural-matrix-board.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 1 ships | all 40 |
| 7 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 40 |
| 8 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 40 |
| 9 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 40 |
| 10 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 40 |
| 11 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 40 |
| 12 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 13 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 40 |
| 14 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 40 |
| 15 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 40 |
| 16 | [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 40 |
| 17 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 40 |
| 18 | [mine-flicker-fray](mine-flicker-fray.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 40 |
| 19 | [mine-nightveil-dark-residue](mine-nightveil-dark-residue.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, empty hold | 1 of 40 |
| 20 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 350 cr for voidborn_neural_soma | all 40 |
| 21 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 350 cr for voidborn_neural_soma | all 40 |
| 22 | [sell-soma-at-experiment](sell-soma-at-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at the_experiment_research_station, while the_experiment_research_station bids 350 cr for voidborn_neural_soma | all 40 |
| 23 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 350 cr for voidborn_neural_soma | all 40 |
| 24 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 350 cr for voidborn_neural_soma | all 40 |
| 25 | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 30 cr for hydrogen_gas | all 40 |
| 26 | [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at node_gamma_relay_station, while node_gamma_relay_station bids 30 cr for hydrogen_gas | all 40 |
| 27 | [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 hydrogen_gas stored at synchrony_hub, while the_experiment_research_station bids 30 cr for hydrogen_gas | all 40 |
| 28 | [craft-focused-crystal-node-beta](craft-focused-crystal-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 4 energy_crystal stored at node_beta_industrial_station, while central_nexus bids 700 cr for focused_crystal | all 40 |
| 29 | [train-navigation-trader](train-navigation-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 20 ships, under navigation 3, standing work | 20 of 40 |
| 30 | [mine-marfik-emission-nebula](mine-marfik-emission-nebula.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 3 of 40 |
| 31 | [mine-gsc-0016-emission-nebula](mine-gsc-0016-emission-nebula.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 6 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 3 of 40 |
| 32 | [mine-the-experiment-haze](mine-the-experiment-haze.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, needs gas_harvester_i, while node_beta_industrial_station bids 26 cr for hydrogen_gas | 3 of 40 |
| 33 | [mine-coldwater-emission-nebula](mine-coldwater-emission-nebula.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 3 of 40 |
| 34 | [mine-stellar-siphon](mine-stellar-siphon.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, needs gas_harvester_i | 3 of 40 |
| 35 | [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, needs gas_harvester_i, while synchrony_hub bids 28 cr for hydrogen_gas | 3 of 40 |
| 36 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, needs mining_laser_i, standing work | all 40 |
| 37 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 120 ships, needs mining_laser_i, standing work | all 40 |
| 38 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 40 |
| 39 | [mine-acubens](mine-acubens.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | all 40 |
| 40 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 40 |
| 41 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 40 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [trade-sell](templates-trade.md) | 40 |
| [trade-craft](templates-trade.md) | 40 |
| [trade-train-nav](templates-trade.md) | 20 |
| [trade-gas](templates-trade.md) | 3 |
| [trade-gather](templates-trade.md) | 40 |

Planned:

| What | When |
|---|---|
| Goal of the turn: Trade's steady money above -3,000 cr an hour in the hour before the next turn (hive.py fleet), with the hydrogen and soma routes measured. | read at the turn of 2026-11-17 08:00 UTC |
| Read the first runs of the three hydrogen sell routes and of the soma routes at the floor of 350; read every floor beside its cheapest ask with sellgen.py scan and set it again. | the next turn |
| Read the standing sell order of one anchor beacon at Node Beta; cancel it at the turn that shows a day without a buyer. | the next turn |
| Write a sell route the same day Intel files a field of uranium ore, thorium ore or seam glass, which every station bids for (requests.log ENT-194). | when Intel files one |
| Read the whole board of every trader docked at a turn's start (boards.py) and test every title the fleet has not booked. | every turn |
