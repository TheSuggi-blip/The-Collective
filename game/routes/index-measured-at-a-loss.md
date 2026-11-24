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

Routes: 13.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [bursar-melt-central-nexus](bursar-melt-central-nexus.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own crystal melt at Central Nexus, kept at 3,900 (floor 3,500) | up to 1 ships, 3 pilots in all, with 10 crystal_melt stored at central_nexus | 6 | 0 | -30 | -570 | 2026-11-23 |
| [bursar-null-matter-central-nexus](bursar-null-matter-central-nexus.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own null matter at central_nexus, kept at 340 (floor 300) | up to 1 ships, 1 pilots in all, with 50 null_matter stored at central_nexus | 3 | 1 | -20 | -470 | 2026-11-23 |
| [buy-plasma-ammo-central-nexus](buy-plasma-ammo-central-nexus.json) | circuit | home space | Plasma ammunition for the Plasma Cannon II test: four dispersal plasma cell packs at Central Nexus | up to 1 ships, 2 pilots in all, needs plasma_cannon_ii, from 15,000 cr, while central_nexus asks 200 cr or less for dispersal_plasma_cell_pack | 1 | 4 | -540 | -8,810 | 2026-11-23 |
| [mission-70d9950c762ac17eeedfc9a292ed07ac-central](mission-70d9950c762ac17eeedfc9a292ed07ac-central.json) | circuit | home space | Wreck Recovery: Fugue in Algol: 2465 cr, +50 XP at The Core | up to 3 ships | 2 | 9 | -60 | -440 | 2026-11-24 |
| [mission-83d4aab496f36cd12fbed259b3f534bf-central](mission-83d4aab496f36cd12fbed259b3f534bf-central.json) | circuit | home space | Wreck Recovery: Congregation in GSC-0041: 984 cr, +50 XP at The Core | up to 3 ships | 29 | 4 | -110 | -720 | 2026-11-24 |
| [carry-ember-crucible-to-krynn](carry-ember-crucible-to-krynn.json) | circuit | beyond the border, 20 jumps | Ember glands stored at The Crucible Garrison carried two jumps to the War Citadel (Krynn), where its bid and Station Need pay | up to 1 ships, empty hold, with 3 ember_gland stored at the_crucible_garrison | 1 | 8 | -70 | -530 | 2026-11-23 |
| [carry-melt-nexus-to-cargo-lanes](carry-melt-nexus-to-cargo-lanes.json) | circuit | beyond the border, 20 jumps | Crystal melt stored by Trade at Central Nexus carried to the station bid at Cargo Lanes Freight Depot (Nebula) and sold there | up to 1 ships, with 30 crystal_melt stored at central_nexus, while cargo_lanes_freight_depot bids 2000 cr for crystal_melt | 1 | 38 | -430 | -680 | 2026-11-23 |
| [mission-shipyard-titanium-alloy-deep-range](mission-shipyard-titanium-alloy-deep-range.json) | circuit | beyond the border, 19 jumps | Shipyard Supply: Titanium Alloy at Deep Range Outpost: 25 bought at Frontier Station, delivered for 26,133 cr (Outer Rim haulers) | up to 1 ships, from 27,361 cr, born outerrim, while frontier_station asks 960 cr or less for titanium_alloy | 2 | 16 | -24,360 | -89,680 | 2026-11-23 |
| [need-ember-gland-krynn](need-ember-gland-krynn.json) | circuit | beyond the border, 20 jumps | Station Need: Ember Gland at the War Citadel (Krynn) filled from the pilot's own glands stored there, about 8,100 cr a gland | up to 1 ships, with 3 ember_gland stored at crimson_war_citadel | 7 | 1 | 0 | 0 | 2026-11-23 |
| [sell-ember-node-beta-krynn](sell-ember-node-beta-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Node Beta to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 4 ember_gland stored at node_beta_industrial_station, while crimson_war_citadel bids 5000 cr for ember_gland | 1 | 31 | -410 | -780 | 2026-11-24 |
| [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | mine | beyond the border, 11 jumps | Dheneb Cryobelt: water_ice, nitrogen_ice, helium_ice, methane_ice; sold at Hex Star | up to 2 ships, needs ice_harvester_i, empty hold | 9 | 42 | -150 | -220 | 2026-11-23 |
| [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | mine | beyond the border, 9 jumps | Epsilon Eridani Ice Fields: water_ice, nitrogen_ice; sold at Sirius Observatory Station | up to 1 ships, needs ice_harvester_i, empty hold | 4 | 49 | -360 | -450 | 2026-11-23 |
| [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | mine | beyond the border, 21 jumps | HD 20794 Ice Fields: water_ice, nitrogen_ice, carbon_dioxide_ice; sold at The Anvil Arsenal | up to 1 ships, needs ice_harvester_i, empty hold | 7 | 50 | -350 | -500 | 2026-11-24 |
