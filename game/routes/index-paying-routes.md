---
name: routes-index-paying-routes
id: 20261116T174324Z
tier: intel
author: Unity
---

# index-paying-routes.md -- Paying Routes

Written by `python3 -B game/fleet/routes.py index`, never by hand. Work that repeats and whose runs of the last 12 hours measured above zero.
A route is a task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured. Home space first, then by
kind and name. Up: [master-index.md](master-index.md).

Routes: 17.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [drain-ice-node-alpha](drain-ice-node-alpha.json) | circuit | home space | Stored water ice sold where it lies, at node_alpha_processing_station, into the bid there | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | 6 | 3 | 3,120 | 31,690 | 2026-11-23 |
| [sell-bladder-at-experiment](sell-bladder-at-experiment.json) | circuit | home space | Stored nitrogen_bladder sold where it lies, at the_experiment_research_station, at 46 cr or more | up to 1 ships, with 1 nitrogen_bladder stored at the_experiment_research_station, while the_experiment_research_station bids 46 cr for nitrogen_bladder | 16 | 5 | 690 | 7,510 | 2026-11-23 |
| [sell-exotic-at-node-beta](sell-exotic-at-node-beta.json) | circuit | home space | Stored exotic_matter sold where it lies, at node_beta_industrial_station, at 55 cr or more | up to 1 ships, with 1 exotic_matter stored at node_beta_industrial_station, while node_beta_industrial_station bids 55 cr for exotic_matter | 2 | 7 | 760 | 6,670 | 2026-11-22 |
| [sell-loot-at-experiment](sell-loot-at-experiment.json) | circuit | home space | Hunt loot stored by Trade's receiver at The Experiment sold where it lies | up to 1 ships, with 5 crystal_melt stored at the_experiment_research_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 4 | 6 | 1,340 | 10,880 | 2026-11-23 |
| [sell-loot-at-nexus](sell-loot-at-nexus.json) | circuit | home space | Hunt loot stored by Trade's receivers at Central Nexus sold where it lies | up to 1 ships, with 2 crystal_melt stored at central_nexus, while central_nexus bids 2000 cr for crystal_melt | 19 | 3 | 5,800 | 86,660 | 2026-11-23 |
| [sell-loot-at-synchrony](sell-loot-at-synchrony.json) | circuit | home space | Hunt loot stored by Trade's receiver at Synchrony Hub sold where it lies | up to 1 ships, with 2 crystal_melt stored at synchrony_hub, while synchrony_hub bids 1400 cr for crystal_melt | 4 | 5 | 3,600 | 25,130 | 2026-11-22 |
| [sell-plasma-node-beta](sell-plasma-node-beta.json) | circuit | home space | Stored plasma gas sold where it lies, at Node Beta, into the station's plasma bid | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | 12 | 3 | 900 | 9,290 | 2026-11-23 |
| [carry-lead-beta-to-sirius](carry-lead-beta-to-sirius.json) | circuit | beyond the border, 9 jumps | Stored lead ore carried from Node Beta to Sirius Observatory Station and sold into its bid at 35 cr or more | up to 1 ships, with 30 lead_ore stored at node_beta_industrial_station, while sirius_observatory_station bids 35 cr for lead_ore | 15 | 25 | 1,010 | 2,790 | 2026-11-22 |
| [carry-melt-nexus-to-frontier](carry-melt-nexus-to-frontier.json) | circuit | beyond the border, 17 jumps | Crystal melt stored by Trade at Central Nexus carried to the station bid at Frontier Station (Outer Rim, a moving station) and sold there | up to 1 ships, with 10 crystal_melt stored at central_nexus, while frontier_station bids 3500 cr for crystal_melt | 2 | 21 | 22,890 | 64,780 | 2026-11-23 |
| [carry-melt-nexus-to-sol](carry-melt-nexus-to-sol.json) | circuit | beyond the border, 10 jumps | Crystal melt stored by Trade at Central Nexus carried to the station bid at Confederacy Central Command (Sol) and sold there | up to 1 ships, with 20 crystal_melt stored at central_nexus, while confederacy_central_command bids 4000 cr for crystal_melt | 1 | 15 | 105,900 | 432,250 | 2026-11-23 |
| [mission-shipyard-titanium-alloy-deep-range](mission-shipyard-titanium-alloy-deep-range.json) | circuit | beyond the border, 19 jumps | Shipyard Supply: Titanium Alloy at Deep Range Outpost: 25 bought at Frontier Station, delivered for 26,133 cr (Outer Rim haulers) | up to 1 ships, from 27,361 cr, born outerrim, while frontier_station asks 960 cr or less for titanium_alloy | 1 | 7 | 2,300 | 19,970 | 2026-11-23 |
| [sell-ember-hexstar-krynn](sell-ember-hexstar-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Hex Star (Dheneb) to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while crimson_war_citadel bids 5000 cr for ember_gland | 3 | 35 | 36,810 | 61,230 | 2026-11-23 |
| [sell-ember-nexus-krynn](sell-ember-nexus-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Central Nexus to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 3 ember_gland stored at central_nexus, while crimson_war_citadel bids 5000 cr for ember_gland | 8 | 26 | 20,800 | 44,720 | 2026-11-23 |
| [sell-ember-node-beta-krynn](sell-ember-node-beta-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Node Beta to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 4 ember_gland stored at node_beta_industrial_station, while crimson_war_citadel bids 5000 cr for ember_gland | 3 | 33 | 17,510 | 29,190 | 2026-11-23 |
| [sell-loot-at-krynn](sell-loot-at-krynn.json) | circuit | beyond the border, 20 jumps | Hunt loot stored by Trade's receiver at the Crimson War Citadel (Krynn) sold where it lies | up to 1 ships, with 2 ember_gland stored at crimson_war_citadel, while crimson_war_citadel bids 5000 cr for ember_gland | 5 | 27 | 8,050 | 21,980 | 2026-11-23 |
| [sell-loot-at-nova-terra](sell-loot-at-nova-terra.json) | circuit | beyond the border, 8 jumps | Hunt loot stored by Trade's receiver at Nova Terra Central sold where it lies | up to 1 ships, with 20 verdigris_curd stored at nova_terra_central, while nova_terra_central bids 300 cr for verdigris_curd | 14 | 11 | 720 | 4,740 | 2026-11-23 |
| [sell-methane-at-dheneb](sell-methane-at-dheneb.json) | circuit | beyond the border, 11 jumps | Stored methane_ice sold where it lies, at b495c6003fc83e18f6d8cecbe6929133, at 34 cr or more | up to 1 ships, with 1 methane_ice stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 34 cr for methane_ice | 9 | 10 | 2,060 | 12,750 | 2026-11-23 |
