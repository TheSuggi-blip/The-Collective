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

Routes: 24.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) | circuit | home space | Stored water ice carried from the_experiment_research_station to the Central Nexus bid (3 jumps) | up to 3 ships, with 65 water_ice stored at the_experiment_research_station, while central_nexus bids 25 cr for water_ice | 1 | 12 | -100 | -480 | 2026-11-16 |
| [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) | circuit | home space | Stored water ice carried from node_alpha_processing_station to the Central Nexus bid (1 jumps) | up to 3 ships, with 65 water_ice stored at node_alpha_processing_station, while central_nexus bids 25 cr for water_ice | 3 | 8 | -50 | -360 | 2026-11-16 |
| [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) | circuit | home space | Stored water ice carried from synchrony_hub to the Central Nexus bid (2 jumps) | up to 2 ships, with 65 water_ice stored at synchrony_hub, while central_nexus bids 25 cr for water_ice | 1 | 10 | -80 | -460 | 2026-11-16 |
| [drain-ice-nexus](drain-ice-nexus.json) | circuit | home space | Stored water ice sold where it lies, at central_nexus, into the bid there | up to 2 ships, with 30 water_ice stored at central_nexus, while central_nexus bids 25 cr for water_ice | 2 | 3 | -20 | -460 | 2026-11-16 |
| [train-navigation-home](train-navigation-home.json) | circuit | home space | Navigation test: five jumps through our own stations (Node Alpha, Synchrony, Node Gamma, Node Beta, Central Nexus), nothing carried, for the drones that do not yet reach navigation 3 | up to 1 ships | 2 | 15 | -120 | -470 | 2026-11-16 |
| [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | mine | home space | Node Beta Frozen Drift: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, while node_alpha_processing_station bids 25 cr for water_ice | 2 | 44 | -240 | -320 | 2026-11-16 |
| [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | hunt | beyond the border, 7 jumps | frost_moth at deepwell_volatile_ice; loot sold at Ironlight Crossroads | up to 1 ships, empty hold | 4 | 13 | -70 | -310 | 2026-11-16 |
| [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | hunt | beyond the border, 7 jumps | veil_ray at felis_dim_lattice; loot sold at Synchrony Hub | up to 1 ships, empty hold | 4 | 17 | -160 | -480 | 2026-11-16 |
| [hunt-felis-frost-ring-hollow-pilgrim](hunt-felis-frost-ring-hollow-pilgrim.json) | hunt | beyond the border, 7 jumps | hollow_pilgrim at felis_frost_ring; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 29 | -160 | -340 | 2026-11-16 |
| [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at garnet_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold | 1 | 11 | -130 | -740 | 2026-11-16 |
| [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | hunt | beyond the border, 6 jumps | veil_ray at starveling_nebula; loot sold at Node Beta Industrial Station | up to 1 ships, empty hold | 4 | 17 | -140 | -470 | 2026-11-16 |
| [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | hunt | beyond the border, 5 jumps | Cinder-sylphs at lesath_gas_cloud (lawless); ember glands sold at Node Beta | up to 1 ships, without piercing_railgun_i, empty hold, while node_beta_industrial_station bids 100 cr for ember_gland | 5 | 13 | -120 | -550 | 2026-11-16 |
| [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | mine | beyond the border, 5 jumps | Alnair Ice Fields: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 2 | 68 | -520 | -460 | 2026-11-16 |
| [mine-antares-ice-fields](mine-antares-ice-fields.json) | mine | beyond the border, 5 jumps | Antares Ice Fields: water_ice, nitrogen_ice, deuterium_ice, helium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 2 | 69 | -530 | -460 | 2026-11-16 |
| [mine-coldwater-emission-nebula](mine-coldwater-emission-nebula.json) | mine | beyond the border, 5 jumps | Coldwater Emission Nebula: hydrogen_gas, argon_gas, xenon_gas, neon_gas; sold at Node Gamma Relay Station | up to 1 ships, needs gas_harvester_i, empty hold | 1 | 64 | -410 | -390 | 2026-11-16 |
| [mine-deepwell-haze](mine-deepwell-haze.json) | mine | beyond the border, 8 jumps | Deepwell Haze: hydrogen_gas, argon_gas, plasma_gas, xenon_gas, neon_gas; sold at Nova Terra Central | up to 1 ships, needs gas_harvester_i, empty hold | 2 | 62 | -310 | -300 | 2026-11-16 |
| [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) | mine | beyond the border, 7 jumps | Deepwell Volatile Ice: water_ice, methane_ice, ammonia_ice, helium_ice; sold at The Experiment Research Station | up to 1 ships, needs ice_harvester_i, empty hold, while the_experiment_research_station bids 25 cr for water_ice | 2 | 93 | -110 | -70 | 2026-11-16 |
| [mine-felis-frost-ring](mine-felis-frost-ring.json) | mine | beyond the border, 7 jumps | Felis Frost Ring: water_ice, nitrogen_ice, deuterium_ice; sold at Node Beta Industrial Station | up to 1 ships, needs ice_harvester_i, empty hold, while node_beta_industrial_station bids 156 cr for deuterium_ice | 2 | 95 | -110 | -70 | 2026-11-16 |
| [mine-gsc-0012-gas-plume](mine-gsc-0012-gas-plume.json) | mine | beyond the border, 5 jumps | GSC-0012 Gas Plume: hydrogen_gas, argon_gas, plasma_gas, xenon_gas, nebula_gas, neon_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | 1 | 73 | -500 | -410 | 2026-11-16 |
| [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | mine | beyond the border, 4 jumps | GSC-0041 Frost Ring: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, empty hold, while node_alpha_processing_station bids 25 cr for water_ice | 2 | 62 | -440 | -430 | 2026-11-16 |
| [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | mine | beyond the border, 5 jumps | GSC-0049 Platinum-Group Reef: nickel_ore, platinum_ore, rhodium_ore; sold at Node Gamma Relay Station | up to 1 ships, empty hold | 3 | 100 | -760 | -460 | 2026-11-16 |
| [mine-hd-147513-belt](mine-hd-147513-belt.json) | mine | beyond the border, 7 jumps | HD 147513 Belt: iron_ore, copper_ore, titanium_ore, gold_ore; sold at The Experiment Research Station | up to 1 ships, empty hold | 4 | 85 | -190 | -140 | 2026-11-16 |
| [mine-miram-haze](mine-miram-haze.json) | mine | beyond the border, 4 jumps | Miram Haze: hydrogen_gas, nebula_gas, ion_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | 1 | 72 | -450 | -380 | 2026-11-16 |
| [mine-okab-haze](mine-okab-haze.json) | mine | beyond the border, 4 jumps | Okab Haze: hydrogen_gas, argon_gas, nebula_gas, neon_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold, while node_beta_industrial_station bids 27 cr for hydrogen_gas | 1 | 57 | -360 | -380 | 2026-11-16 |
