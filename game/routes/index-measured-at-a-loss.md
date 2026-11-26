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
| [sell-loot-at-nexus](sell-loot-at-nexus.json) | circuit | home space | Hunt loot stored by Trade's receivers at Central Nexus sold where it lies | up to 1 ships, with 2 crystal_melt stored at central_nexus, while central_nexus bids 2000 cr for crystal_melt | 1 | 13 | -670 | -3,010 | 2026-11-26 |
| [sell-melt-at-dheneb](sell-melt-at-dheneb.json) | circuit | beyond the border, 11 jumps | Crystal melt stored at Hex Star (Dheneb, lawless) sold into its bid where it lies | up to 1 ships, with 5 crystal_melt stored at b495c6003fc83e18f6d8cecbe6929133, while b495c6003fc83e18f6d8cecbe6929133 bids 3000 cr for crystal_melt | 1 | 14 | -440 | -1,860 | 2026-11-26 |
