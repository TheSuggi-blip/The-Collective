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

Routes: 26.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [mine-stellar-siphon](mine-stellar-siphon.json) | mine | home space | Stellar Siphon: hydrogen_gas, argon_gas, neon_gas; sold at Synchrony Hub | up to 1 ships, needs gas_harvester_i | 2 | 48 | -210 | -260 | 2026-11-17 |
| [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | mine | home space | The Experiment Haze: hydrogen_gas; sold at Synchrony Hub | up to 1 ships, needs gas_harvester_i, while synchrony_hub bids 28 cr for hydrogen_gas | 2 | 45 | -310 | -410 | 2026-11-17 |
| [buy-gold-ironlight-boards](buy-gold-ironlight-boards.json) | circuit | beyond the border, 6 jumps | Gold ore bought at Ironlight Crossroads (LHS 1140, lawless) and made into circuit boards by hand at Node Beta with the pilot's own stored copper ore and energy crystal | up to 1 ships, empty hold, with 3 copper_ore stored at node_beta_industrial_station, 1 energy_crystal stored at node_beta_industrial_station | 1 | 21 | -560 | -1,630 | 2026-11-17 |
| [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | hunt | beyond the border, 7 jumps | frost_moth at deepwell_volatile_ice; loot sold at Ironlight Crossroads | up to 1 ships, empty hold | 4 | 13 | -70 | -310 | 2026-11-16 |
| [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | hunt | beyond the border, 7 jumps | veil_ray at felis_dim_lattice; loot sold at Synchrony Hub | up to 1 ships, empty hold | 3 | 31 | -160 | -380 | 2026-11-17 |
| [hunt-felis-frost-ring-hollow-pilgrim](hunt-felis-frost-ring-hollow-pilgrim.json) | hunt | beyond the border, 7 jumps | hollow_pilgrim at felis_frost_ring; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 29 | -160 | -340 | 2026-11-16 |
| [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at garnet_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold | 2 | 11 | -130 | -700 | 2026-11-17 |
| [hunt-orphan-nebula-veil-ray](hunt-orphan-nebula-veil-ray.json) | hunt | beyond the border, 9 jumps | veil_ray at orphan_nebula; loot sold at Nova Terra Central | up to 1 ships, empty hold | 1 | 31 | -440 | -860 | 2026-11-17 |
| [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | hunt | beyond the border, 6 jumps | veil_ray at starveling_nebula; loot sold at Node Beta Industrial Station | up to 1 ships, empty hold | 3 | 23 | -150 | -360 | 2026-11-17 |
| [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | hunt | beyond the border, 6 jumps | Yield test: frost_moth at homam_cryobelt (lawless); what a kill drops and whether a bid takes it | up to 1 ships, empty hold | 4 | 12 | -130 | -590 | 2026-11-17 |
| [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | hunt | beyond the border, 5 jumps | Cinder-sylphs at lesath_gas_cloud (lawless); ember glands sold at Node Beta | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for ember_gland | 5 | 13 | -120 | -550 | 2026-11-16 |
| [mine-antares-gas-cloud](mine-antares-gas-cloud.json) | mine | beyond the border, 8 jumps | Antares Gas Cloud: hydrogen_gas, argon_gas, plasma_gas, nebula_gas, neon_gas, chlorine_gas; sold at Nova Terra Central | up to 1 ships, needs gas_harvester_i, empty hold | 3 | 56 | -30 | -30 | 2026-11-17 |
| [mine-coldwater-emission-nebula](mine-coldwater-emission-nebula.json) | mine | beyond the border, 5 jumps | Coldwater Emission Nebula: hydrogen_gas, argon_gas, xenon_gas, neon_gas; sold at Node Gamma Relay Station | up to 1 ships, needs gas_harvester_i, empty hold | 2 | 50 | -280 | -330 | 2026-11-17 |
| [mine-deepwell-haze](mine-deepwell-haze.json) | mine | beyond the border, 8 jumps | Deepwell Haze: hydrogen_gas, argon_gas, plasma_gas, xenon_gas, neon_gas; sold at Nova Terra Central | up to 1 ships, needs gas_harvester_i, empty hold | 3 | 63 | -460 | -440 | 2026-11-17 |
| [mine-dewfall-fray](mine-dewfall-fray.json) | mine | beyond the border, 4 jumps | Dewfall Fray: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 7 | 10 | -80 | -230 | 2026-11-17 |
| [mine-felis-frost-ring](mine-felis-frost-ring.json) | mine | beyond the border, 7 jumps | Felis Frost Ring: water_ice, nitrogen_ice, deuterium_ice; sold at Node Beta Industrial Station | up to 1 ships, needs ice_harvester_i, empty hold, while node_beta_industrial_station bids 156 cr for deuterium_ice | 1 | 96 | -720 | -450 | 2026-11-17 |
| [mine-gaugewatch-belt](mine-gaugewatch-belt.json) | mine | beyond the border, 7 jumps | Gaugewatch Belt: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 1 | 67 | -390 | -350 | 2026-11-17 |
| [mine-gossamer-null](mine-gossamer-null.json) | mine | beyond the border, 6 jumps | Gossamer Null: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 1 | 67 | -340 | -300 | 2026-11-17 |
| [mine-gsc-0012-gas-plume](mine-gsc-0012-gas-plume.json) | mine | beyond the border, 5 jumps | GSC-0012 Gas Plume: hydrogen_gas, argon_gas, plasma_gas, xenon_gas, nebula_gas, neon_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | 1 | 73 | -500 | -410 | 2026-11-16 |
| [mine-gsc-0033-void-whisper](mine-gsc-0033-void-whisper.json) | mine | beyond the border, 6 jumps | GSC-0033 Void Whisper: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 1 | 65 | -380 | -350 | 2026-11-17 |
| [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | mine | beyond the border, 5 jumps | GSC-0049 Platinum-Group Reef: nickel_ore, platinum_ore, rhodium_ore; sold at Node Gamma Relay Station | up to 1 ships, empty hold | 3 | 100 | -760 | -460 | 2026-11-16 |
| [mine-hd-147513-belt](mine-hd-147513-belt.json) | mine | beyond the border, 7 jumps | HD 147513 Belt: iron_ore, copper_ore, titanium_ore, gold_ore; sold at The Experiment Research Station | up to 1 ships, empty hold | 4 | 85 | -420 | -290 | 2026-11-17 |
| [mine-miram-haze](mine-miram-haze.json) | mine | beyond the border, 4 jumps | Miram Haze: hydrogen_gas, nebula_gas, ion_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | 1 | 72 | -450 | -380 | 2026-11-16 |
| [mine-okab-haze](mine-okab-haze.json) | mine | beyond the border, 4 jumps | Okab Haze: hydrogen_gas, argon_gas, nebula_gas, neon_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | 1 | 57 | -360 | -380 | 2026-11-16 |
| [mine-stillwork-belt](mine-stillwork-belt.json) | mine | beyond the border, 7 jumps | Stillwork Belt: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 1 | 73 | -400 | -330 | 2026-11-17 |
| [mine-thinspace-rubble](mine-thinspace-rubble.json) | mine | beyond the border, 6 jumps | Thinspace Rubble: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 1 | 65 | -380 | -350 | 2026-11-17 |
