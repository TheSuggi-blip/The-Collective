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

Routes: 34.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | circuit | home space | Liquid hydrogen made at the Node Beta workshop carried one jump to the Central Nexus bid | up to 1 ships, with 10 liquid_hydrogen stored at node_beta_industrial_station, while central_nexus bids 110 cr for liquid_hydrogen | 2 | 8 | -60 | -430 | 2026-11-17 |
| [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) | circuit | home space | Stored liquid hydrogen sold where it lies, at Central Nexus, into the station's bid | up to 1 ships, with 5 liquid_hydrogen stored at central_nexus, while central_nexus bids 100 cr for liquid_hydrogen | 2 | 7 | -70 | -610 | 2026-11-17 |
| [mine-stellar-siphon](mine-stellar-siphon.json) | mine | home space | Stellar Siphon: hydrogen_gas, argon_gas, neon_gas; sold at Synchrony Hub | up to 1 ships, needs gas_harvester_i | 2 | 48 | -210 | -260 | 2026-11-17 |
| [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | mine | home space | The Experiment Haze: hydrogen_gas; sold at Synchrony Hub | up to 1 ships, needs gas_harvester_i, while synchrony_hub bids 28 cr for hydrogen_gas | 2 | 45 | -310 | -410 | 2026-11-17 |
| [buy-gold-ironlight-boards](buy-gold-ironlight-boards.json) | circuit | beyond the border, 6 jumps | Gold ore bought at Ironlight Crossroads (LHS 1140, lawless) and made into circuit boards by hand at Node Beta with the pilot's own stored copper ore and energy crystal | up to 1 ships, empty hold, with 3 copper_ore stored at node_beta_industrial_station, 1 energy_crystal stored at node_beta_industrial_station | 1 | 21 | -560 | -1,630 | 2026-11-17 |
| [hunt-antares-gas-cloud-cinder-sylph](hunt-antares-gas-cloud-cinder-sylph.json) | hunt | beyond the border, 6 jumps | cinder_sylph at antares_gas_cloud; loot sold at Ironlight Crossroads | up to 1 ships, empty hold | 1 | 10 | -70 | -420 | 2026-11-17 |
| [hunt-avior-cryobelt-hollow-pilgrim](hunt-avior-cryobelt-hollow-pilgrim.json) | hunt | beyond the border, 12 jumps | hollow_pilgrim at avior_cryobelt; loot sold at Sirius Observatory Station | up to 1 ships, empty hold | 2 | 37 | -520 | -860 | 2026-11-17 |
| [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | hunt | beyond the border, 7 jumps | frost_moth at deepwell_volatile_ice; loot sold at Ironlight Crossroads | up to 1 ships, empty hold | 4 | 13 | -70 | -310 | 2026-11-16 |
| [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | hunt | beyond the border, 7 jumps | veil_ray at felis_dim_lattice; loot sold at Synchrony Hub | up to 1 ships, empty hold | 3 | 31 | -160 | -380 | 2026-11-17 |
| [hunt-fulu-vapor-fields-cinder-sylph](hunt-fulu-vapor-fields-cinder-sylph.json) | hunt | beyond the border, 10 jumps | cinder_sylph at fulu_vapor_fields; loot sold at The Core | up to 1 ships, empty hold | 3 | 28 | -180 | -330 | 2026-11-17 |
| [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at garnet_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold | 4 | 10 | -110 | -680 | 2026-11-17 |
| [hunt-orphan-nebula-veil-ray](hunt-orphan-nebula-veil-ray.json) | hunt | beyond the border, 9 jumps | veil_ray at orphan_nebula; loot sold at Nova Terra Central | up to 1 ships, empty hold | 2 | 40 | -460 | -700 | 2026-11-17 |
| [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | hunt | beyond the border, 8 jumps | veil_ray at raysheet_nebula; loot sold at Nova Terra Central | up to 1 ships, empty hold | 6 | 15 | -50 | -210 | 2026-11-17 |
| [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | hunt | beyond the border, 6 jumps | veil_ray at starveling_nebula; loot sold at Node Beta Industrial Station | up to 1 ships, empty hold | 3 | 23 | -150 | -360 | 2026-11-17 |
| [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | hunt | beyond the border, 5 jumps | Cinder-sylphs at lesath_gas_cloud (lawless); ember glands sold at Node Beta | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for ember_gland | 5 | 13 | -120 | -550 | 2026-11-16 |
| [mine-antares-gas-cloud](mine-antares-gas-cloud.json) | mine | beyond the border, 8 jumps | Antares Gas Cloud: hydrogen_gas, argon_gas, plasma_gas, nebula_gas, neon_gas, chlorine_gas; sold at Nova Terra Central | up to 1 ships, needs gas_harvester_i, empty hold | 3 | 55 | -290 | -350 | 2026-11-17 |
| [mine-atria-ice-fields](mine-atria-ice-fields.json) | mine | beyond the border, 7 jumps | Atria Ice Fields: water_ice, nitrogen_ice, deuterium_ice; sold at Node Beta Industrial Station | up to 1 ships, needs ice_harvester_i, empty hold | 2 | 87 | -680 | -470 | 2026-11-17 |
| [mine-celaeno-frozen-drift](mine-celaeno-frozen-drift.json) | mine | beyond the border, 9 jumps | Celaeno Frozen Drift: water_ice, deuterium_ice, tritium_ice, helium_ice; sold at Sirius Observatory Station | up to 1 ships, needs ice_harvester_i, empty hold | 2 | 83 | -790 | -570 | 2026-11-17 |
| [mine-deepwell-haze](mine-deepwell-haze.json) | mine | beyond the border, 8 jumps | Deepwell Haze: hydrogen_gas, argon_gas, plasma_gas, xenon_gas, neon_gas; sold at Nova Terra Central | up to 1 ships, needs gas_harvester_i, empty hold | 4 | 64 | -490 | -490 | 2026-11-17 |
| [mine-dewfall-fray](mine-dewfall-fray.json) | mine | beyond the border, 4 jumps | Dewfall Fray: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 8 | 10 | -150 | -300 | 2026-11-17 |
| [mine-felis-frost-ring](mine-felis-frost-ring.json) | mine | beyond the border, 7 jumps | Felis Frost Ring: water_ice, nitrogen_ice, deuterium_ice; sold at Node Beta Industrial Station | up to 1 ships, needs ice_harvester_i, empty hold, while node_beta_industrial_station bids 156 cr for deuterium_ice | 1 | 96 | -780 | -490 | 2026-11-17 |
| [mine-flicker-fray](mine-flicker-fray.json) | mine | beyond the border, 5 jumps | Flicker Fray: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 63 | -420 | -400 | 2026-11-17 |
| [mine-gaugewatch-belt](mine-gaugewatch-belt.json) | mine | beyond the border, 7 jumps | Gaugewatch Belt: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 82 | -570 | -410 | 2026-11-17 |
| [mine-gliese-876-belt](mine-gliese-876-belt.json) | mine | beyond the border, 8 jumps | Gliese 876 Belt: iron_ore, carbon_ore, nickel_ore; sold at Nova Terra Central | up to 1 ships, empty hold | 5 | 92 | -360 | -270 | 2026-11-17 |
| [mine-gossamer-null](mine-gossamer-null.json) | mine | beyond the border, 6 jumps | Gossamer Null: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 3 | 101 | -160 | -110 | 2026-11-17 |
| [mine-gsc-0033-void-whisper](mine-gsc-0033-void-whisper.json) | mine | beyond the border, 6 jumps | GSC-0033 Void Whisper: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 84 | -570 | -410 | 2026-11-17 |
| [mine-gsc-0042-ice-shelf](mine-gsc-0042-ice-shelf.json) | mine | beyond the border, 11 jumps | GSC-0042 Ice Shelf: water_ice, deuterium_ice; sold at Node Beta Industrial Station | up to 1 ships, needs ice_harvester_i, empty hold | 2 | 84 | -700 | -500 | 2026-11-17 |
| [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | mine | beyond the border, 5 jumps | GSC-0049 Platinum-Group Reef: nickel_ore, platinum_ore, rhodium_ore; sold at Node Gamma Relay Station | up to 1 ships, empty hold | 3 | 101 | -2,780 | -1,690 | 2026-11-17 |
| [mine-hd-147513-belt](mine-hd-147513-belt.json) | mine | beyond the border, 7 jumps | HD 147513 Belt: iron_ore, copper_ore, titanium_ore, gold_ore; sold at The Experiment Research Station | up to 1 ships, empty hold | 4 | 85 | -420 | -290 | 2026-11-17 |
| [mine-lesath-gas-cloud](mine-lesath-gas-cloud.json) | mine | beyond the border, 5 jumps | Lesath Gas Cloud: hydrogen_gas, plasma_gas, xenon_gas, neon_gas, ion_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold | 3 | 66 | -190 | -220 | 2026-11-17 |
| [mine-nightveil-dark-residue](mine-nightveil-dark-residue.json) | mine | beyond the border, 5 jumps | Nightveil Dark Residue: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 63 | -340 | -320 | 2026-11-17 |
| [mine-oxbow-ice-belt](mine-oxbow-ice-belt.json) | mine | beyond the border, 13 jumps | Oxbow Ice Belt: water_ice, deuterium_ice, helium_ice; sold at Node Beta Industrial Station | up to 1 ships, needs ice_harvester_i, empty hold | 2 | 91 | -480 | -320 | 2026-11-17 |
| [mine-stillwork-belt](mine-stillwork-belt.json) | mine | beyond the border, 7 jumps | Stillwork Belt: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 87 | -620 | -430 | 2026-11-17 |
| [mine-thinspace-rubble](mine-thinspace-rubble.json) | mine | beyond the border, 6 jumps | Thinspace Rubble: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 83 | -580 | -420 | 2026-11-17 |
