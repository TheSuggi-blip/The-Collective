---
name: routes-plan-miner
id: 20261116T174333Z
tier: intel
author: Unity
---

# plan-miner.md -- The Plan of the Role miner

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `plans/miner.json`:
the routes the miner ships fly, in one order, and how many of them have each route in
their plan. The division's Admiral keeps one plan file with every ship and its own
routes (`game/fleet/plan.py`); it names our ships, so it lies in the unit's data folder
and not here, and `plans/miner.json` is written from it. `Planned` is what the Admiral
means to do next. What a route earns now is not written here, because it changes by the
hour: ask the tool `route` or `routes`, or the database (`hive.py sql`), which carry each
figure with its age. Up: [master-index.md](master-index.md).

Kept by Zero. Routes: 66. Ships: 60.

| # | Route | Group | Zone | Open to | Ships planned |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 10 ships, from navigation 3 | all 60 |
| 2 | [voidborn-first-steps-board](voidborn-first-steps-board.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 3 ships | all 60 |
| 3 | [voidborn-network-expansion](voidborn-network-expansion.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward First Steps in the Void | all 60 |
| 4 | [voidborn-collective-provides](voidborn-collective-provides.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 10 jumps | once per pilot, up to 4 ships, empty hold, after the reward Network Expansion | all 60 |
| 5 | [voidborn-signal-protocol](voidborn-signal-protocol.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 20 ships, after the reward The Collective Provides | all 60 |
| 6 | [voidborn-concurrent](voidborn-concurrent.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot | all 60 |
| 7 | [voidborn-substrate](voidborn-substrate.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 3,000 cr | all 60 |
| 8 | [voidborn-missions-1](voidborn-missions-1.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, from 8,000 cr | all 60 |
| 9 | [voidborn-mining-missions](voidborn-mining-missions.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 60 |
| 10 | [voidborn-precedence](voidborn-precedence.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 40 ships | all 60 |
| 11 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 6 jumps | once per pilot, up to 4 ships, 246 pilots in all, empty hold, from 13,000 cr | all 60 |
| 12 | [voidborn-resonance-finish](voidborn-resonance-finish.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 2 ships, from 8,000 cr, after the reward Conductive Lattice | all 60 |
| 13 | [mission-deep-core-prospecting-first-step](mission-deep-core-prospecting-first-step.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 19 jumps | once per pilot, up to 1 ships, 1 pilots in all, empty hold | all 60 |
| 14 | [mission-the-forge-tax-crucible](mission-the-forge-tax-crucible.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 21 jumps | once per pilot, up to 1 ships, 1 pilots in all, empty hold | all 60 |
| 15 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 60 |
| 16 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 60 |
| 17 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | all 60 |
| 18 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 1 ships | all 60 |
| 19 | [voidborn-first-hunt-intercrus-sootfall](voidborn-first-hunt-intercrus-sootfall.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 60 |
| 20 | [voidborn-first-hunt-intercrus-belt](voidborn-first-hunt-intercrus-belt.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 7 jumps | once per pilot, up to 1 ships, empty hold | all 60 |
| 21 | [mission-workshop-production-run-node-beta](mission-workshop-production-run-node-beta.json) | [Once per Pilot](index-once-per-pilot.md) | home space | once per pilot, up to 4 ships, with 60 iron_ore stored at node_beta_industrial_station | all 60 |
| 22 | [mission-deep-core-prospecting-nova-terra](mission-deep-core-prospecting-nova-terra.json) | [Once per Pilot](index-once-per-pilot.md) | beyond the border, 9 jumps | once per pilot, up to 1 ships, 16 pilots in all, empty hold | all 60 |
| 23 | [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 12 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | 1 of 60 |
| 24 | [mine-almach-stray-facets](mine-almach-stray-facets.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 24 jumps | up to 1 ships, empty hold | 1 of 60 |
| 25 | [gather-goldcrest-gold](gather-goldcrest-gold.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 1 ships, needs mining_laser_i, empty hold, standing work | 1 of 60 |
| 26 | [train-navigation-trader](train-navigation-trader.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 20 ships, under navigation 3, standing work | 12 of 60 |
| 27 | [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | 7 of 60 |
| 28 | [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while node_alpha_processing_station bids 320 cr for voidborn_neural_soma | 3 of 60 |
| 29 | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_beta_industrial_station bids 320 cr for voidborn_neural_soma | 2 of 60 |
| 30 | [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at node_beta_industrial_station, while node_gamma_relay_station bids 320 cr for voidborn_neural_soma | 2 of 60 |
| 31 | [sell-soma-at-experiment](sell-soma-at-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 1 voidborn_neural_soma stored at the_experiment_research_station, while the_experiment_research_station bids 320 cr for voidborn_neural_soma | 9 of 60 |
| 32 | [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 11 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4 of 60 |
| 33 | [craft-piping-node-beta](craft-piping-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 14 ships, with 300 iron_ore stored at node_beta_industrial_station, 180 copper_ore stored at node_beta_industrial_station, standing work | 14 of 60 |
| 34 | [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 30 null_matter stored at synchrony_hub, while central_nexus bids 150 cr for null_matter | all 60 |
| 35 | [drain-methane-experiment](drain-methane-experiment.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 10 methane_ice stored at the_experiment_research_station, while the_experiment_research_station bids 30 cr for methane_ice | all 60 |
| 36 | [drain-ice-nexus](drain-ice-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 1 ships, with 5 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | all 60 |
| 37 | [drain-ice-node-alpha](drain-ice-node-alpha.json) | [Tests](index-tests.md) | home space | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | all 60 |
| 38 | [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | all 60 |
| 39 | [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | all 60 |
| 40 | [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | [Paying Routes](index-paying-routes.md) | home space | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | all 60 |
| 41 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | [Measured at a Loss](index-measured-at-a-loss.md) | home space | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 60 |
| 42 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 43 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 44 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | [Paying Routes](index-paying-routes.md) | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold, while central_nexus bids 25 cr for water_ice | all 60 |
| 45 | [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) | [Measured at a Loss](index-measured-at-a-loss.md) | beyond the border, 8 jumps | up to 1 ships, needs ice_harvester_i, while central_nexus bids 25 cr for water_ice | all 60 |
| 46 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | [Tests](index-tests.md) | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold, while synchrony_hub bids 25 cr for water_ice | all 60 |
| 47 | [store-hold-central-nexus](store-hold-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 40 ships, goods aboard, standing work | all 60 |
| 48 | [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 49 | [gather-ironhollow-fading-signal](gather-ironhollow-fading-signal.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 20 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 50 | [gather-schedar-belt](gather-schedar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 2 jumps | up to 45 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 51 | [gather-garnet-belt](gather-garnet-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 5 jumps | up to 29 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 52 | [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 35 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 53 | [gather-ruchbah-broken-glass-veil](gather-ruchbah-broken-glass-veil.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 6 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 54 | [gather-achernar-belt](gather-achernar-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 16 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 55 | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 120 ships, needs mining_laser_i, standing work | all 60 |
| 56 | [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 66 ships, needs mining_laser_i, standing work | all 60 |
| 57 | [mine-acubens](mine-acubens.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 18 ships, needs mining_laser_i, standing work | all 60 |
| 58 | [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 50 ships, standing work | all 60 |
| 59 | [mine-pherkad-rift](mine-pherkad-rift.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 125 ships, needs mining_laser_i, standing work | all 60 |
| 60 | [craft-steel-node-beta](craft-steel-node-beta.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 11 ships, with 550 iron_ore stored at node_beta_industrial_station, standing work | all 60 |
| 61 | [craft-steel-central-nexus](craft-steel-central-nexus.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 2 ships, with 300 iron_ore stored at central_nexus, standing work | all 60 |
| 62 | [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | up to 3 ships, with 300 iron_ore stored at synchrony_hub, standing work | all 60 |
| 63 | [gather-gj-3470-dewfall-fray](gather-gj-3470-dewfall-fray.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 13 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 64 | [gather-okab-belt](gather-okab-belt.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 4 jumps | up to 42 ships, needs mining_laser_i, empty hold, standing work | all 60 |
| 65 | [census-frontier](census-frontier.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | beyond the border, 7 jumps | up to 12 ships, empty hold | all 60 |
| 66 | [park](park.json) | [Standing Work, Reading and Waiting](index-standing-work.md) | home space | the park route | all 60 |

Templates its ships fly (a ship's own routes name one as `@<name>`):

| Template | Ships of this role on it |
|---|---|
| [ice-sell](templates-mining.md) | 60 |
| [reserve-prism](templates-mining.md) | 29 |
| [reserve-hamal](templates-mining.md) | 31 |

Planned:

| What | When |
|---|---|
| Goal of the turn of 23:00 UTC: Mining's reserve goods stored +10,000 units an hour over 4 hours (hive.py flow Zero; +11,937 at 19:12 UTC), of them gold above +250 an hour (+189); the three one-ship tests read (Deep Range Deep Core, The Forge Tax, The Gold Crest) | turn of 23:00 UTC |
| The Liminal: its yard waits for 12 silicate composite, 2 shield emitters and 1 Mining Laser I (commission_status 19:07 UTC); a script sells them into the yard's own bids at Node Beta this turn; the pilot switched in when the status no longer reads sourcing | next turn |
| Iron is short only 29,329 (stock reserve, 19:13 UTC) against +6,261 stored an hour: when it is met, the iron gather fields go down toward the ships the reserve's other ores need (gold, nickel, carbon, silicon), every miner still mining (rule F23) | turn of 23:00 UTC |
| The outpost at GSC-0044 (base 443f0c5b2a1fbbcea95d13b76a797fe9, members only): gather routes storing into its faction storage, richest first: Botein Belt (iron 68), Acrux Belt (64, lithium 13,361), GSC-0044 Belt (46), Intercrus Belt (43), Forgotten Tailings (40); they wait for faction seats of miners (the Desk) and a store step into faction storage proved by one run | when the Desk stands |
| When the stored water ice is under about 2,000 units, lift the Central Nexus mine routes back toward what the bid regains | each turn |
