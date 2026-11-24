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

Routes: 4.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-melt-first-step-to-experiment](carry-melt-first-step-to-experiment.json) | circuit | beyond the border, 18 jumps | Stored crystal_melt carried from first_step_memorial_station to the the_experiment_research_station bid at 1000 cr or more | up to 1 ships, with 20 crystal_melt stored at first_step_memorial_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 34 | -310 | -540 | 2026-11-24 |
| [carry-melt-sirius-to-experiment](carry-melt-sirius-to-experiment.json) | circuit | beyond the border, 9 jumps | Stored crystal_melt carried from sirius_observatory_station to the the_experiment_research_station bid at 1000 cr or more | up to 1 ships, with 10 crystal_melt stored at sirius_observatory_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 26 | -320 | -750 | 2026-11-24 |
| [home-frontier-station](home-frontier-station.json) | circuit | beyond the border, 17 jumps | Home to Frontier Station: an Outer Rim scout far from Altais docks at its capital, where its region's work is | up to 12 ships, empty hold, born outerrim | 1 | 16 | -330 | -1,250 | 2026-11-24 |
| [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | circuit | beyond the border, 11 jumps | Stored ember glands carried from Central Nexus to the Hex Star bid (Dheneb, lawless) | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | 1 | 14 | -100 | -420 | 2026-11-24 |
