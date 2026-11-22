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

Routes: 10.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [buy-plasma-ammo-central-nexus](buy-plasma-ammo-central-nexus.json) | circuit | home space | Plasma ammunition for the Plasma Cannon II test: four dispersal plasma cell packs at Central Nexus | up to 1 ships, 2 pilots in all, needs plasma_cannon_ii, from 15,000 cr, while central_nexus asks 200 cr or less for dispersal_plasma_cell_pack | 1 | 24 | -970 | -2,450 | 2026-11-22 |
| [sell-ember-hexstar-krynn](sell-ember-hexstar-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Hex Star (Dheneb) to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while crimson_war_citadel bids 5000 cr for ember_gland | 2 | 24 | -330 | -810 | 2026-11-22 |
| [trade-chemical-liner-beta-to-first-step](trade-chemical-liner-beta-to-first-step.json) | circuit | beyond the border, 18 jumps | Chemical liners bought at Node Beta for 620 cr or less, sold into First Step's bid at 720 or more: a trade test beyond the border | up to 1 ships, empty hold, from 25,000 cr, while first_step_memorial_station bids 720 cr for chemical_liner, while node_beta_industrial_station asks 620 cr or less for chemical_liner | 1 | 26 | -80 | -200 | 2026-11-22 |
| [hunt-propus-ice-belt-hollow-pilgrim](hunt-propus-ice-belt-hollow-pilgrim.json) | hunt | beyond the border, 15 jumps | hollow_pilgrim at propus_ice_belt; loot sold at Hex Star | up to 3 ships, empty hold | 2 | 18 | -100 | -310 | 2026-11-22 |
| [mine-ain-ice-belt](mine-ain-ice-belt.json) | mine | beyond the border, 16 jumps | Ain Ice Belt: water_ice; sold at Unknown Edge Waystation | up to 3 ships, needs ice_harvester_i, empty hold | 2 | 93 | -410 | -260 | 2026-11-22 |
| [mine-almach-stray-facets](mine-almach-stray-facets.json) | mine | beyond the border, 24 jumps | Almach Stray Facets: iron_ore, copper_ore, trade_crystal; sold at The Core | up to 1 ships, empty hold | 2 | 117 | -1,360 | -700 | 2026-11-22 |
| [mine-altais-outer-ice](mine-altais-outer-ice.json) | mine | beyond the border, 17 jumps | Altais Outer Ice: water_ice, nitrogen_ice; sold at Unknown Edge Waystation | up to 3 ships, needs ice_harvester_i | 2 | 62 | -240 | -230 | 2026-11-22 |
| [mine-flicker-fray](mine-flicker-fray.json) | mine | beyond the border, 5 jumps | Flicker Fray: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 95 | -750 | -480 | 2026-11-22 |
| [mine-gsc-0015-cryobelt](mine-gsc-0015-cryobelt.json) | mine | beyond the border, 16 jumps | GSC-0015 Cryobelt: water_ice; sold at Unknown Edge Waystation | up to 3 ships, needs ice_harvester_i, empty hold | 2 | 92 | -550 | -360 | 2026-11-22 |
| [mine-nightveil-dark-residue](mine-nightveil-dark-residue.json) | mine | beyond the border, 5 jumps | Nightveil Dark Residue: iron_ore, copper_ore, null_matter; sold at The Core | up to 1 ships, empty hold | 2 | 61 | -430 | -420 | 2026-11-21 |
