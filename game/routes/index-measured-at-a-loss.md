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

Routes: 3.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) | circuit | home space | Stored null matter carried from Synchrony Hub to the Central Nexus bid (2 jumps) | up to 1 ships, with 30 null_matter stored at synchrony_hub, while central_nexus bids 150 cr for null_matter | 2 | 17 | -160 | -540 | 2026-11-26 |
| [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) | circuit | home space | Stored null matter sold where it lies, at Central Nexus, at 200 cr or more | up to 1 ships, with 1 null_matter stored at central_nexus, while central_nexus bids 200 cr for null_matter | 2 | 16 | -1,790 | -6,590 | 2026-11-26 |
| [carry-levity-arneb-to-krynn](carry-levity-arneb-to-krynn.json) | circuit | beyond the border, 20 jumps | Levity bladders stored at Arneb carried to Crimson War Citadel (Krynn) and stored there, for the HEXC supply contract of 750 | up to 1 ships, with 30 levity_bladder stored at cca9e51e6eaf8dada77f698ccc4a09c7 | 4 | 18 | -130 | -390 | 2026-11-25 |
