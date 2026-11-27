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
| [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) | circuit | home space | Stored null matter carried from Synchrony Hub to the Central Nexus bid (2 jumps) | up to 1 ships, with 30 null_matter stored at synchrony_hub, while central_nexus bids 150 cr for null_matter | 1 | 8 | -300 | -2,310 | 2026-11-27 |
| [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) | circuit | home space | Stored null matter sold where it lies, at Central Nexus, at 200 cr or more | up to 1 ships, with 1 null_matter stored at central_nexus, while central_nexus bids 200 cr for null_matter | 1 | 1 | 0 | 0 | 2026-11-27 |
