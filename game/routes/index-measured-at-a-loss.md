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

Routes: 14.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [buy-plasma-ammo-central-nexus](buy-plasma-ammo-central-nexus.json) | circuit | home space | Plasma ammunition for the Plasma Cannon II test: four dispersal plasma cell packs at Central Nexus | up to 1 ships, 2 pilots in all, needs plasma_cannon_ii, from 15,000 cr, while central_nexus asks 200 cr or less for dispersal_plasma_cell_pack | 1 | 6 | -580 | -5,560 | 2026-11-22 |
| [carry-melt-experiment-to-nexus](carry-melt-experiment-to-nexus.json) | circuit | home space | Crystal melt stored by Trade at The Experiment carried to the Central Nexus bid and sold there | up to 1 ships, with 10 crystal_melt stored at the_experiment_research_station, while central_nexus bids 2000 cr for crystal_melt | 3 | 11 | -160 | -590 | 2026-11-22 |
| [sell-curd-at-experiment](sell-curd-at-experiment.json) | circuit | home space | Verdigris curd and noble condensate stored by Trade's receivers at The Experiment sold where they lie into the standing NPC bids | up to 1 ships, with 20 verdigris_curd stored at the_experiment_research_station, while the_experiment_research_station bids 300 cr for verdigris_curd | 1 | 4 | -50 | -740 | 2026-11-22 |
| [sell-curd-at-node-beta](sell-curd-at-node-beta.json) | circuit | home space | Verdigris curd and noble condensate stored by Trade's receivers at Node Beta sold where they lie into the standing NPC bids | up to 1 ships, with 20 verdigris_curd stored at node_beta_industrial_station, while node_beta_industrial_station bids 300 cr for verdigris_curd | 1 | 30 | -310 | -620 | 2026-11-22 |
| [carry-curd-beta-to-procyon](carry-curd-beta-to-procyon.json) | circuit | beyond the border, 9 jumps | Stored verdigris curd carried from node_beta_industrial_station to procyon_colonial_station and sold into its bid at 315 cr or more | up to 1 ships, with 25 verdigris_curd stored at node_beta_industrial_station, while procyon_colonial_station bids 315 cr for verdigris_curd | 1 | 16 | -210 | -770 | 2026-11-22 |
| [carry-lead-nexus-to-sirius](carry-lead-nexus-to-sirius.json) | circuit | beyond the border, 9 jumps | Stored lead ore carried from Central Nexus to Sirius Observatory Station and sold into its bid at 35 cr or more | up to 1 ships, with 30 lead_ore stored at central_nexus, while sirius_observatory_station bids 35 cr for lead_ore | 1 | 11 | 0 | 0 | 2026-11-22 |
| [carry-melt-first-step-to-experiment](carry-melt-first-step-to-experiment.json) | circuit | beyond the border, 18 jumps | Stored crystal_melt carried from first_step_memorial_station to the the_experiment_research_station bid at 1000 cr or more | up to 1 ships, with 20 crystal_melt stored at first_step_memorial_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 1 | 19 | -180 | -570 | 2026-11-22 |
| [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | circuit | beyond the border, 11 jumps | Stored ember glands carried from Central Nexus to the Hex Star bid (Dheneb, lawless) | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | 1 | 45 | -450 | -600 | 2026-11-22 |
| [mine-ain-ice-belt](mine-ain-ice-belt.json) | mine | beyond the border, 16 jumps | Ain Ice Belt: water_ice; sold at Unknown Edge Waystation | up to 3 ships, needs ice_harvester_i, empty hold | 2 | 93 | -410 | -260 | 2026-11-22 |
| [mine-altais-outer-ice](mine-altais-outer-ice.json) | mine | beyond the border, 17 jumps | Altais Outer Ice: water_ice, nitrogen_ice; sold at Unknown Edge Waystation | up to 3 ships, needs ice_harvester_i | 1 | 62 | -160 | -160 | 2026-11-22 |
| [mine-dheneb-cryobelt](mine-dheneb-cryobelt.json) | mine | beyond the border, 11 jumps | Dheneb Cryobelt: water_ice, nitrogen_ice, helium_ice, methane_ice; sold at Hex Star | up to 2 ships, needs ice_harvester_i, empty hold | 25 | 42 | -110 | -160 | 2026-11-22 |
| [mine-epsilon-eridani-ice-fields](mine-epsilon-eridani-ice-fields.json) | mine | beyond the border, 9 jumps | Epsilon Eridani Ice Fields: water_ice, nitrogen_ice; sold at Sirius Observatory Station | up to 1 ships, needs ice_harvester_i, empty hold | 9 | 50 | -430 | -510 | 2026-11-22 |
| [mine-gsc-0015-cryobelt](mine-gsc-0015-cryobelt.json) | mine | beyond the border, 16 jumps | GSC-0015 Cryobelt: water_ice; sold at Unknown Edge Waystation | up to 3 ships, needs ice_harvester_i, empty hold | 2 | 92 | -550 | -360 | 2026-11-22 |
| [mine-hd-20794-ice-fields](mine-hd-20794-ice-fields.json) | mine | beyond the border, 21 jumps | HD 20794 Ice Fields: water_ice, nitrogen_ice, carbon_dioxide_ice; sold at The Anvil Arsenal | up to 1 ships, needs ice_harvester_i, empty hold | 7 | 50 | -60 | -70 | 2026-11-22 |
