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

Routes: 5.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) | circuit | home space | Stored null matter carried from Node Beta to the Central Nexus bid at 200 cr or more | up to 1 ships, with 1 null_matter stored at node_beta_industrial_station, while central_nexus bids 200 cr for null_matter | 3 | 25 | 10,020 | 24,120 | 2026-11-26 |
| [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) | circuit | home space | Stored null matter carried from Synchrony Hub to the Central Nexus bid (2 jumps) | up to 1 ships, with 30 null_matter stored at synchrony_hub, while central_nexus bids 150 cr for null_matter | 3 | 20 | 60 | 210 | 2026-11-26 |
| [drain-ice-node-alpha](drain-ice-node-alpha.json) | circuit | home space | Stored water ice sold where it lies, at node_alpha_processing_station, into the bid there | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | 2 | 2 | 2,220 | 54,440 | 2026-11-26 |
| [sell-lead-docked-central-nexus](sell-lead-docked-central-nexus.json) | circuit | home space | Stored lead_ore sold where it lies, at central_nexus, at 110 cr or more | up to 3 ships, with 3 lead_ore stored at central_nexus, while central_nexus bids 110 cr for lead_ore | 3 | 0 | 200 | 25,710 | 2026-11-26 |
| [carry-phase-deep-range-to-sol](carry-phase-deep-range-to-sol.json) | circuit | beyond the border, 19 jumps | Stored phase_crystal carried from deep_range_outpost to the confederacy_central_command bid at 100 cr or more | up to 1 ships, with 50 phase_crystal stored at deep_range_outpost, while confederacy_central_command bids 100 cr for phase_crystal | 4 | 39 | 5,730 | 8,520 | 2026-11-26 |
