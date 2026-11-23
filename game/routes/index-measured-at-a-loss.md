---
name: routes-index-measured-at-a-loss
id: 20261116T174328Z
tier: intel
author: Unity
---

# index-measured-at-a-loss.md -- Measured at a Loss

Written by `python3 -B game/fleet/routes.py index`, never by hand. Work that repeats and whose runs of the last 12 hours measured zero or below.
A route is a task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured. Home space first, then by
kind and name. Up: [master-index.md](master-index.md).

Routes: 9.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [buy-plasma-ammo-central-nexus](buy-plasma-ammo-central-nexus.json) | circuit | home space | Plasma ammunition for the Plasma Cannon II test: four dispersal plasma cell packs at Central Nexus | up to 1 ships, 2 pilots in all, needs plasma_cannon_ii, from 15,000 cr, while central_nexus asks 200 cr or less for dispersal_plasma_cell_pack | 1 | 6 | -580 | -5,560 | 2026-11-22 |
| [carry-melt-beta-to-nexus](carry-melt-beta-to-nexus.json) | circuit | home space | Crystal melt stored by Trade at Node Beta carried to the Central Nexus bid and sold there | up to 1 ships, with 10 crystal_melt stored at node_beta_industrial_station, while central_nexus bids 2000 cr for crystal_melt | 1 | 4 | -30 | -390 | 2026-11-23 |
| [carry-melt-experiment-to-nexus](carry-melt-experiment-to-nexus.json) | circuit | home space | Crystal melt stored by Trade at The Experiment carried to the Central Nexus bid and sold there | up to 1 ships, with 10 crystal_melt stored at the_experiment_research_station, while central_nexus bids 2000 cr for crystal_melt | 6 | 11 | -150 | -580 | 2026-11-22 |
| [carry-hydrogen-beta-to-nova-terra](carry-hydrogen-beta-to-nova-terra.json) | circuit | beyond the border, 8 jumps | Stored hydrogen carried from Node Beta to Nova Terra Central and sold into its bid at 35 cr or more | up to 1 ships, with 65 hydrogen_gas stored at node_beta_industrial_station, while nova_terra_central bids 35 cr for hydrogen_gas | 1 | 11 | -160 | -880 | 2026-11-23 |
| [mission-shipyard-engine-core-deep-range](mission-shipyard-engine-core-deep-range.json) | circuit | beyond the border, 19 jumps | Shipyard Supply: Engine Core at Deep Range Outpost: 12 bought at Unknown Edge Waystation, delivered for 18,988 cr (Outer Rim haulers) | up to 1 ships, from 19,862 cr, born outerrim, while unknown_edge_waystation asks 1400 cr or less for engine_core | 2 | 7 | -8,940 | -75,510 | 2026-11-23 |
| [mission-shipyard-fuel-tank-deep-range](mission-shipyard-fuel-tank-deep-range.json) | circuit | beyond the border, 19 jumps | Shipyard Supply: Fuel Tank at Deep Range Outpost: 14 fuel tanks bought at Unknown Edge Waystation, carried 3 jumps and delivered for 9,515 cr (Outer Rim haulers) | up to 3 ships, from 11,500 cr, born outerrim, while unknown_edge_waystation asks 620 cr or less for fuel_tank | 13 | 9 | -390 | -2,690 | 2026-11-23 |
| [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | mine | beyond the border, 11 jumps | Dheneb Cryobelt: water_ice, nitrogen_ice, helium_ice, methane_ice; sold at Hex Star | up to 2 ships, needs ice_harvester_i, empty hold | 25 | 42 | -110 | -160 | 2026-11-22 |
| [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | mine | beyond the border, 9 jumps | Epsilon Eridani Ice Fields: water_ice, nitrogen_ice; sold at Sirius Observatory Station | up to 1 ships, needs ice_harvester_i, empty hold | 2 | 50 | -570 | -680 | 2026-11-23 |
| [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | mine | beyond the border, 21 jumps | HD 20794 Ice Fields: water_ice, nitrogen_ice, carbon_dioxide_ice; sold at The Anvil Arsenal | up to 1 ships, needs ice_harvester_i, empty hold | 5 | 50 | -520 | -630 | 2026-11-22 |
