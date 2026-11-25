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

Routes: 13.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-melt-experiment-to-nexus](carry-melt-experiment-to-nexus.json) | circuit | home space | Crystal melt stored by Trade at The Experiment carried to the Central Nexus bid and sold there | up to 1 ships, with 10 crystal_melt stored at the_experiment_research_station, while central_nexus bids 2000 cr for crystal_melt | 1 | 20 | 3,080 | 9,270 | 2026-11-25 |
| [drain-ice-node-alpha](drain-ice-node-alpha.json) | circuit | home space | Stored water ice sold where it lies, at node_alpha_processing_station, into the bid there | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | 2 | 24 | 1,470 | 3,720 | 2026-11-25 |
| [sell-loot-at-experiment](sell-loot-at-experiment.json) | circuit | home space | Hunt loot stored by Trade's receiver at The Experiment sold where it lies | up to 1 ships, with 5 crystal_melt stored at the_experiment_research_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 10 | 920 | 5,310 | 2026-11-25 |
| [sell-loot-at-nexus](sell-loot-at-nexus.json) | circuit | home space | Hunt loot stored by Trade's receivers at Central Nexus sold where it lies | up to 1 ships, with 2 crystal_melt stored at central_nexus, while central_nexus bids 2000 cr for crystal_melt | 10 | 13 | 3,650 | 15,690 | 2026-11-25 |
| [carry-bladder-alpha-to-sol](carry-bladder-alpha-to-sol.json) | circuit | beyond the border, 11 jumps | Stored nitrogen_bladder carried from alpha_centauri_colonial_station to the confederacy_central_command bid at 100 cr or more | up to 1 ships, with 20 nitrogen_bladder stored at alpha_centauri_colonial_station, while confederacy_central_command bids 100 cr for nitrogen_bladder | 2 | 19 | 12,580 | 40,160 | 2026-11-25 |
| [carry-lead-beta-to-sirius](carry-lead-beta-to-sirius.json) | circuit | beyond the border, 9 jumps | Stored lead ore carried from Node Beta to Sirius Observatory Station and sold into its bid at 35 cr or more | up to 1 ships, with 30 lead_ore stored at node_beta_industrial_station, while sirius_observatory_station bids 35 cr for lead_ore | 2 | 19 | 3,560 | 11,520 | 2026-11-25 |
| [carry-sac-beta-to-hex-star](carry-sac-beta-to-hex-star.json) | circuit | beyond the border, 11 jumps | Caustic sacs stored by Trade at Node Beta carried to the deep player bid at Hex Star (Dheneb) and sold there | up to 1 ships, with 30 caustic_sac stored at node_beta_industrial_station, while b495c6003fc83e18f6d8cecbe6929133 bids 1250 cr for caustic_sac | 2 | 14 | 81,970 | 342,740 | 2026-11-24 |
| [sell-ember-hexstar-krynn](sell-ember-hexstar-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Hex Star (Dheneb) to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 4 ember_gland stored at b495c6003fc83e18f6d8cecbe6929133, while crimson_war_citadel bids 5000 cr for ember_gland | 1 | 39 | 38,800 | 59,850 | 2026-11-25 |
| [sell-ember-nexus-krynn](sell-ember-nexus-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Central Nexus to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 3 ember_gland stored at central_nexus, while crimson_war_citadel bids 5000 cr for ember_gland | 2 | 26 | 12,820 | 29,400 | 2026-11-25 |
| [sell-ember-node-beta-krynn](sell-ember-node-beta-krynn.json) | circuit | beyond the border, 20 jumps | Stored ember glands carried from Node Beta to the Crimson War Citadel (Krynn) bid | up to 1 ships, with 4 ember_gland stored at node_beta_industrial_station, while crimson_war_citadel bids 5000 cr for ember_gland | 1 | 30 | 30,380 | 61,780 | 2026-11-25 |
| [sell-loot-at-krynn](sell-loot-at-krynn.json) | circuit | beyond the border, 20 jumps | Hunt loot stored by Trade's receiver at the Crimson War Citadel (Krynn) sold where it lies | up to 1 ships, with 2 ember_gland stored at crimson_war_citadel, while crimson_war_citadel bids 5000 cr for ember_gland | 6 | 16 | 14,330 | 54,400 | 2026-11-25 |
| [sell-melt-at-dheneb](sell-melt-at-dheneb.json) | circuit | beyond the border, 11 jumps | Crystal melt stored at Hex Star (Dheneb, lawless) sold into its bid where it lies | up to 1 ships, with 5 crystal_melt stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 3000 cr for crystal_melt | 9 | 14 | 31,980 | 147,700 | 2026-11-25 |
| [sell-methane-at-dheneb](sell-methane-at-dheneb.json) | circuit | beyond the border, 11 jumps | Stored methane_ice sold where it lies, at b495c6003fc83e18f6d8cecbe6929133, at 34 cr or more | up to 1 ships, with 1 methane_ice stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 34 cr for methane_ice | 1 | 18 | 910 | 3,060 | 2026-11-25 |
