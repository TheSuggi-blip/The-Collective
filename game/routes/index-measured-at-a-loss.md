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

Routes: 19.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [bursar-melt-central-nexus](bursar-melt-central-nexus.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own crystal melt at Central Nexus, kept at 3,900 (floor 3,500) | up to 1 ships, 3 pilots in all, with 10 crystal_melt stored at central_nexus | 3 | 0 | 0 | 0 | 2026-11-23 |
| [bursar-null-matter-central-nexus](bursar-null-matter-central-nexus.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own null matter at central_nexus, kept at 340 (floor 300) | up to 1 ships, 1 pilots in all, with 50 null_matter stored at central_nexus | 1 | 23 | -250 | -670 | 2026-11-23 |
| [bursar-null-matter-node-beta](bursar-null-matter-node-beta.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own null matter at node_beta_industrial_station, kept at 340 (floor 300) | up to 1 ships, 1 pilots in all, with 50 null_matter stored at node_beta_industrial_station | 2 | 3 | -30 | -480 | 2026-11-23 |
| [bursar-null-matter-synchrony](bursar-null-matter-synchrony.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own null matter at synchrony_hub, kept at 340 (floor 300) | up to 1 ships, 1 pilots in all, with 50 null_matter stored at synchrony_hub | 1 | 3 | -100 | -2,010 | 2026-11-23 |
| [carry-melt-beta-to-nexus](carry-melt-beta-to-nexus.json) | circuit | home space | Crystal melt stored by Trade at Node Beta carried to the Central Nexus bid and sold there | up to 1 ships, with 10 crystal_melt stored at node_beta_industrial_station, while central_nexus bids 2000 cr for crystal_melt | 1 | 4 | -30 | -390 | 2026-11-23 |
| [carry-melt-experiment-to-nexus](carry-melt-experiment-to-nexus.json) | circuit | home space | Crystal melt stored by Trade at The Experiment carried to the Central Nexus bid and sold there | up to 1 ships, with 10 crystal_melt stored at the_experiment_research_station, while central_nexus bids 2000 cr for crystal_melt | 6 | 11 | -150 | -580 | 2026-11-22 |
| [mission-83d4aab496f36cd12fbed259b3f534bf-central](mission-83d4aab496f36cd12fbed259b3f534bf-central.json) | circuit | home space | Wreck Recovery: Congregation in GSC-0041: 984 cr, +50 XP at The Core | up to 3 ships | 2 | 3 | -10 | -320 | 2026-11-23 |
| [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) | circuit | home space | Stored liquid hydrogen sold where it lies, at Node Beta, into the station's bid | up to 1 ships, with 5 liquid_hydrogen stored at node_beta_industrial_station, while node_beta_industrial_station bids 95 cr for liquid_hydrogen | 1 | 4 | -30 | -380 | 2026-11-23 |
| [carry-curd-beta-to-procyon](carry-curd-beta-to-procyon.json) | circuit | beyond the border, 9 jumps | Stored verdigris curd carried from node_beta_industrial_station to procyon_colonial_station and sold into its bid at 315 cr or more | up to 1 ships, with 25 verdigris_curd stored at node_beta_industrial_station, while procyon_colonial_station bids 315 cr for verdigris_curd | 1 | 16 | -200 | -740 | 2026-11-23 |
| [carry-curd-nexus-to-procyon](carry-curd-nexus-to-procyon.json) | circuit | beyond the border, 9 jumps | Stored verdigris curd carried from central_nexus to procyon_colonial_station and sold into its bid at 315 cr or more | up to 1 ships, with 25 verdigris_curd stored at central_nexus, while procyon_colonial_station bids 315 cr for verdigris_curd | 1 | 13 | -170 | -790 | 2026-11-23 |
| [carry-hydrogen-beta-to-nova-terra](carry-hydrogen-beta-to-nova-terra.json) | circuit | beyond the border, 8 jumps | Stored hydrogen carried from Node Beta to Nova Terra Central and sold into its bid at 35 cr or more | up to 1 ships, with 65 hydrogen_gas stored at node_beta_industrial_station, while nova_terra_central bids 35 cr for hydrogen_gas | 1 | 11 | -160 | -880 | 2026-11-23 |
| [carry-null-matter-nexus-to-crucible](carry-null-matter-nexus-to-crucible.json) | circuit | beyond the border, 18 jumps | Null matter stored by Trade at Central Nexus carried to the station bid at The Crucible Garrison and sold there | up to 1 ships, with 65 null_matter stored at central_nexus, while the_crucible_garrison bids 300 cr for null_matter | 1 | 37 | -350 | -580 | 2026-11-23 |
| [home-frontier-station](home-frontier-station.json) | circuit | beyond the border, 17 jumps | Home to Frontier Station: an Outer Rim scout far from Altais docks at its capital, where its region's work is | up to 12 ships, empty hold, born outerrim | 4 | 17 | -410 | -1,400 | 2026-11-23 |
| [mission-shipyard-engine-core-deep-range](mission-shipyard-engine-core-deep-range.json) | circuit | beyond the border, 19 jumps | Shipyard Supply: Engine Core at Deep Range Outpost: 12 bought at Unknown Edge Waystation, delivered for 18,988 cr (Outer Rim haulers) | up to 1 ships, from 19,862 cr, born outerrim, while unknown_edge_waystation asks 1400 cr or less for engine_core | 4 | 8 | -12,000 | -95,350 | 2026-11-23 |
| [mission-shipyard-fuel-tank-deep-range](mission-shipyard-fuel-tank-deep-range.json) | circuit | beyond the border, 19 jumps | Shipyard Supply: Fuel Tank at Deep Range Outpost: 14 fuel tanks bought at Unknown Edge Waystation, carried 3 jumps and delivered for 9,515 cr (Outer Rim haulers) | up to 3 ships, from 11,500 cr, born outerrim, while unknown_edge_waystation asks 620 cr or less for fuel_tank | 27 | 9 | -1,080 | -7,890 | 2026-11-23 |
| [sell-ember-experiment-dheneb](sell-ember-experiment-dheneb.json) | circuit | beyond the border, 11 jumps | Stored ember glands carried from The Experiment Research Station to the Hex Star bid (Dheneb, lawless) | up to 1 ships, with 6 ember_gland stored at the_experiment_research_station, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | 1 | 16 | -150 | -580 | 2026-11-23 |
| [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | mine | beyond the border, 11 jumps | Dheneb Cryobelt: water_ice, nitrogen_ice, helium_ice, methane_ice; sold at Hex Star | up to 2 ships, needs ice_harvester_i, empty hold | 9 | 42 | -150 | -220 | 2026-11-23 |
| [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | mine | beyond the border, 9 jumps | Epsilon Eridani Ice Fields: water_ice, nitrogen_ice; sold at Sirius Observatory Station | up to 1 ships, needs ice_harvester_i, empty hold | 2 | 50 | -380 | -460 | 2026-11-23 |
| [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | mine | beyond the border, 21 jumps | HD 20794 Ice Fields: water_ice, nitrogen_ice, carbon_dioxide_ice; sold at The Anvil Arsenal | up to 1 ships, needs ice_harvester_i, empty hold | 5 | 50 | -520 | -630 | 2026-11-22 |
