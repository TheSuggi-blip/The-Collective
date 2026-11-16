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
means to do next. Up: [master-index.md](master-index.md).

Kept by Apollo. Routes: 39. Ships: 20.

| # | Route | Group | Zone | Open to | Ships planned | Credits per ship-hour |
|---|---|---|---|---|---|---|
| 1 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 20 | one-time |
| 2 | [voidborn-atmospheric-extraction](voidborn-atmospheric-extraction.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without gas_harvester_i, from 6,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 3 | [voidborn-hardware-cargo](voidborn-hardware-cargo.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships, without cargo_expander_i, from 4,000 cr, after the reward The Collective Provides | all 20 | one-time |
| 4 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 20 | one-time |
| 5 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 20 | one-time |
| 6 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Off](index-off.md) | beyond the border, 5 jumps | once per pilot, up to 2 ships, empty hold, after the reward Network Expansion, off | all 20 | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 146 pilots in all, empty hold, from 13,000 cr | all 20 | one-time |
| 8 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 20 | one-time |
| 9 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 20 | one-time |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 11 | [voidborn-selling](voidborn-selling.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships | all 20 | one-time |
| 12 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 20 | one-time |
| 13 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 20 | one-time |
| 14 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 20 | one-time |
| 15 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 20 | one-time |
| 16 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 20 | one-time |
| 17 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | all 20 | one-time |
| 18 | [sell-soma-synchrony](sell-soma-synchrony.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 19 | [sell-soma-node-beta](sell-soma-node-beta.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 20 | [carry-soma-synchrony-node-alpha](carry-soma-synchrony-node-alpha.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 21 | [carry-soma-synchrony-node-gamma](carry-soma-synchrony-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 22 | [carry-soma-node-beta-node-alpha](carry-soma-node-beta-node-alpha.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_alpha_processing_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 23 | [carry-soma-node-beta-node-gamma](carry-soma-node-beta-node-gamma.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 500 cr for voidborn_neural_soma | all 20 | TBD |
| 24 | [sell-plate-node-beta](sell-plate-node-beta.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 1 armor_plate stored at node_beta_industrial_station, while node_beta_industrial_station bids 300 cr for armor_plate | all 20 | -400 |
| 25 | [sell-plasma-node-beta](sell-plasma-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | all 20 | 9,010 |
| 26 | [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at central_nexus, while central_nexus bids 100 cr for liquid_hydrogen | all 20 | -480 |
| 27 | [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 liquid_hydrogen stored at node_beta_industrial_station, while node_beta_industrial_station bids 95 cr for liquid_hydrogen | all 20 | 16,890 |
| 28 | [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | [Tests](index-tests.md) | home space | up to 1 ships, with 10 liquid_hydrogen stored at node_beta_industrial_station, while central_nexus bids 110 cr for liquid_hydrogen | all 20 | TBD |
| 29 | [mine-gliese-876-belt](mine-gliese-876-belt.json) | [Tests](index-tests.md) | beyond the border, 8 jumps | up to 1 ships, empty hold | 1 of 20 | TBD |
| 30 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | 1 of 20 | 2,230 |
| 31 | [mine-antares-gas-cloud](mine-antares-gas-cloud.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 1 of 20 | 230 |
| 32 | [mine-coldwater-emission-nebula](mine-coldwater-emission-nebula.json) | [Tests](index-tests.md) | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 1 of 20 | TBD |
| 33 | [mine-amberfall-emission-nebula](mine-amberfall-emission-nebula.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold, while node_gamma_relay_station bids 27 cr for hydrogen_gas | 4 of 20 | -120 |
| 34 | [mine-deepwell-haze](mine-deepwell-haze.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 8 jumps | up to 1 ships, needs gas_harvester_i, empty hold | 1 of 20 | 40 |
| 35 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 20 | -170 |
| 36 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 6 ships, standing work | all 20 | -150 |
| 37 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 56 ships, needs mining_laser_i, standing work | all 20 | -120 |
| 38 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 20 | -630 |
| 39 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 20 | -670 |

Planned:

| What | When |
|---|---|
| 75 circuit boards for the faction: etch at the Central Nexus workshop once Mining's 16 silicon and carbon lie in the crafting storage (requests ENT-168); the rest from bought silicon (ask 420 cr x 424), one unit first | next turn |
| Read the first RESULT line of carry-liquid-hydrogen-node-beta-central (81 liquid hydrogen made at Node Beta) and of the gas tests; drop each that loses twice | next turn |
| Focused crystal (4 energy crystal, 1 palladium) into the Central Nexus bid of 800 x 10, if Trade says no to it (requests ENT-169) | after Mercury's answer |
| The next station step tested by hand: draw_copper_piping (12 copper ore, 2 steel plate, 4 piping) at the Node Beta workshop, one hauler and one batch, quoted first | next turn |
| The faction's 275 steel plate lie in one Logistics storage at Node Beta: deposit them to the builder the Fleet Admiral names | on her word |
