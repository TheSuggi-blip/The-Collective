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

Routes: 7.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [drain-ice-node-alpha](drain-ice-node-alpha.json) | circuit | home space | Stored water ice sold where it lies, at node_alpha_processing_station, into the bid there | up to 2 ships, with 30 water_ice stored at node_alpha_processing_station, while node_alpha_processing_station bids 25 cr for water_ice | 4 | 12 | 1,160 | 5,610 | 2026-11-25 |
| [sell-lead-docked-central-nexus](sell-lead-docked-central-nexus.json) | circuit | home space | Stored lead_ore sold where it lies, at central_nexus, at 110 cr or more | up to 3 ships, with 3 lead_ore stored at central_nexus, while central_nexus bids 110 cr for lead_ore | 6 | 1 | 460 | 42,460 | 2026-11-25 |
| [carry-bladder-alpha-to-sol](carry-bladder-alpha-to-sol.json) | circuit | beyond the border, 11 jumps | Stored nitrogen_bladder carried from alpha_centauri_colonial_station to the confederacy_central_command bid at 100 cr or more | up to 1 ships, with 20 nitrogen_bladder stored at alpha_centauri_colonial_station, while confederacy_central_command bids 100 cr for nitrogen_bladder | 3 | 6 | 3,710 | 19,580 | 2026-11-25 |
| [carry-phase-deep-range-to-sol](carry-phase-deep-range-to-sol.json) | circuit | beyond the border, 19 jumps | Stored phase_crystal carried from deep_range_outpost to the confederacy_central_command bid at 100 cr or more | up to 1 ships, with 50 phase_crystal stored at deep_range_outpost, while confederacy_central_command bids 100 cr for phase_crystal | 9 | 36 | 4,570 | 7,520 | 2026-11-25 |
| [carry-phase-first-step-to-sol](carry-phase-first-step-to-sol.json) | circuit | beyond the border, 18 jumps | Stored phase_crystal carried from first_step_memorial_station to the confederacy_central_command bid at 100 cr or more | up to 1 ships, with 50 phase_crystal stored at first_step_memorial_station, while confederacy_central_command bids 100 cr for phase_crystal | 2 | 22 | 3,230 | 8,770 | 2026-11-25 |
| [sell-exotic-docked-grand-exchange](sell-exotic-docked-grand-exchange.json) | circuit | beyond the border, 21 jumps | Stored exotic_matter sold where it lies, at grand_exchange_station, at 45 cr or more | up to 1 ships, with 20 exotic_matter stored at grand_exchange_station, while grand_exchange_station bids 45 cr for exotic_matter | 1 | 1 | 2,850 | 244,290 | 2026-11-25 |
| [sell-methane-at-dheneb](sell-methane-at-dheneb.json) | circuit | beyond the border, 11 jumps | Stored methane_ice sold where it lies, at b495c6003fc83e18f6d8cecbe6929133, at 34 cr or more | up to 1 ships, with 1 methane_ice stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 34 cr for methane_ice | 1 | 6 | 1,610 | 15,850 | 2026-11-25 |
