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

Routes: 2.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-levity-arneb-to-krynn](carry-levity-arneb-to-krynn.json) | circuit | beyond the border, 20 jumps | Levity bladders stored at Arneb carried to Crimson War Citadel (Krynn) and stored there, for the HEXC supply contract of 750 | up to 1 ships, with 30 levity_bladder stored at cca9e51e6eaf8dada77f698ccc4a09c7 | 1 | 28 | -140 | -280 | 2026-11-25 |
| [carry-melt-sirius-to-experiment](carry-melt-sirius-to-experiment.json) | circuit | beyond the border, 9 jumps | Stored crystal_melt carried from sirius_observatory_station to the the_experiment_research_station bid at 1000 cr or more | up to 1 ships, with 10 crystal_melt stored at sirius_observatory_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 26 | -320 | -750 | 2026-11-24 |
