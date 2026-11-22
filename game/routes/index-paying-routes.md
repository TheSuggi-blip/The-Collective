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

Routes: 22.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | circuit | home space | Stored water ice carried from the_experiment_research_station to the Central Nexus bid (3 jumps) | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | 24 | 11 | 780 | 3,720 | 2026-11-22 |
| [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | circuit | home space | Stored water ice carried from node_alpha_processing_station to the Central Nexus bid (1 jumps) | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | 18 | 7 | 1,070 | 8,730 | 2026-11-22 |
| [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | circuit | home space | Stored water ice carried from synchrony_hub to the Central Nexus bid (2 jumps) | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | 7 | 10 | 1,140 | 5,370 | 2026-11-22 |
| [drain-ice-nexus](drain-ice-nexus.json) | circuit | home space | Stored water ice sold where it lies, at central_nexus, into the bid there | up to 1 ships, with 5 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | 31 | 4 | 1,040 | 8,350 | 2026-11-22 |
| [drain-ice-node-alpha](drain-ice-node-alpha.json) | circuit | home space | Stored water ice sold where it lies, at node_alpha_processing_station, into the bid there | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | 1 | 3 | 2,900 | 54,360 | 2026-11-22 |
| [sell-plasma-node-beta](sell-plasma-node-beta.json) | circuit | home space | Stored plasma gas sold where it lies, at Node Beta, into the station's plasma bid | up to 1 ships, with 5 plasma_gas stored at node_beta_industrial_station, while node_beta_industrial_station bids 90 cr for plasma_gas | 10 | 4 | 920 | 14,650 | 2026-11-22 |
| [sell-soma-at-synchrony](sell-soma-at-synchrony.json) | circuit | home space | Stored neural soma sold where it lies, at Synchrony Hub, into the station's bid at 350 cr or more | up to 1 ships, with 1 voidborn_neural_soma stored at synchrony_hub, while synchrony_hub bids 320 cr for voidborn_neural_soma | 1 | 13 | 510 | 2,310 | 2026-11-22 |
| [carry-hydrogen-beta-to-nova-terra](carry-hydrogen-beta-to-nova-terra.json) | circuit | beyond the border, 8 jumps | Stored hydrogen carried from Node Beta to Nova Terra Central and sold into its bid at 35 cr or more | up to 1 ships, with 65 hydrogen_gas stored at node_beta_industrial_station, while nova_terra_central bids 35 cr for hydrogen_gas | 10 | 15 | 590 | 2,130 | 2026-11-22 |
| [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | circuit | beyond the border, 11 jumps | Stored ember glands carried from Central Nexus to the Hex Star bid (Dheneb, lawless) | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | 4 | 24 | 27,700 | 65,380 | 2026-11-22 |
| [sell-ember-nexus-krynn](sell-ember-nexus-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Central Nexus to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 3 ember_gland stored at central_nexus, while crimson_war_citadel bids 5000 cr for ember_gland | 3 | 30 | 10,460 | 20,070 | 2026-11-22 |
| [sell-ember-node-beta-krynn](sell-ember-node-beta-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Node Beta to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 4 ember_gland stored at node_beta_industrial_station, while crimson_war_citadel bids 5000 cr for ember_gland | 2 | 27 | 7,760 | 17,210 | 2026-11-22 |
| [sell-loot-at-dheneb](sell-loot-at-dheneb.json) | circuit | beyond the border, 11 jumps | Hunt loot stored by Trade's receiver at the outpost at Dheneb sold where it lies | up to 1 ships, with 3 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 4500 cr for ember_gland | 1 | 14 | 33,440 | 140,300 | 2026-11-22 |
| [sell-loot-at-nova-terra](sell-loot-at-nova-terra.json) | circuit | beyond the border, 8 jumps | Hunt loot stored by Trade's receiver at Nova Terra Central sold where it lies | up to 1 ships, with 20 verdigris_curd stored at nova_terra_central, while nova_terra_central bids 300 cr for verdigris_curd | 2 | 6 | 340 | 3,520 | 2026-11-22 |
| [hunt-altais-outer-ice-hollow-pilgrim](hunt-altais-outer-ice-hollow-pilgrim.json) | hunt | beyond the border, 18 jumps | hollow_pilgrim at altais_outer_ice; loot sold at Mobile Capital | up to 3 ships | 1 | 19 | 12,600 | 40,000 | 2026-11-22 |
| [hunt-deep-range-cryobelt-hollow-pilgrim](hunt-deep-range-cryobelt-hollow-pilgrim.json) | hunt | beyond the border, 19 jumps | hollow_pilgrim at deep_range_cryobelt; loot sold at Mobile Capital | up to 3 ships | 1 | 58 | 2,720 | 2,790 | 2026-11-22 |
| [hunt-hatysa-vapor-fields-cinder-sylph](hunt-hatysa-vapor-fields-cinder-sylph.json) | hunt | beyond the border, 11 jumps | cinder_sylph at hatysa_vapor_fields; loot sold at Hex Star | up to 3 ships, empty hold | 1 | 32 | 19,860 | 37,230 | 2026-11-22 |
| [mine-alula-frost-ring](mine-alula-frost-ring.json) | mine | beyond the border, 23 jumps | Alula Frost Ring: water_ice, helium_ice; sold at Factory Belt Manufacturing Hub | up to 3 ships, needs ice_harvester_i, empty hold | 2 | 95 | 50 | 30 | 2026-11-22 |
| [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | mine | beyond the border, 11 jumps | Dheneb Cryobelt: water_ice, nitrogen_ice, helium_ice, methane_ice; sold at Hex Star | up to 2 ships, needs ice_harvester_i, empty hold | 34 | 42 | 700 | 1,100 | 2026-11-22 |
| [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | mine | beyond the border, 9 jumps | Epsilon Eridani Ice Fields: water_ice, nitrogen_ice; sold at Sirius Observatory Station | up to 1 ships, needs ice_harvester_i, empty hold | 7 | 49 | 7,640 | 9,480 | 2026-11-22 |
| [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | mine | beyond the border, 21 jumps | HD 20794 Ice Fields: water_ice, nitrogen_ice, carbon_dioxide_ice; sold at The Anvil Arsenal | up to 1 ships, needs ice_harvester_i, empty hold | 7 | 50 | 960 | 1,240 | 2026-11-22 |
| [mine-icecap-drift](mine-icecap-drift.json) | mine | beyond the border, 18 jumps | Icecap Drift: water_ice, nitrogen_ice, carbon_dioxide_ice; sold at Unknown Edge Waystation | up to 3 ships, needs ice_harvester_i | 2 | 52 | 2,920 | 3,360 | 2026-11-22 |
| [mine-khambalia-ice-fields](mine-khambalia-ice-fields.json) | mine | beyond the border, 23 jumps | Khambalia Ice Fields: water_ice, nitrogen_ice, helium_ice, methane_ice; sold at Factory Belt Manufacturing Hub | up to 3 ships, needs ice_harvester_i | 2 | 50 | 660 | 790 | 2026-11-22 |
