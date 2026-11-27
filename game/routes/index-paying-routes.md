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

Routes: 2.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) | circuit | home space | Stored null matter carried from Node Beta to the Central Nexus bid at 200 cr or more | up to 1 ships, with 1 null_matter stored at node_beta_industrial_station, while central_nexus bids 200 cr for null_matter | 1 | 31 | 1,890 | 3,680 | 2026-11-27 |
| [carry-null-matter-nexus-to-crucible](carry-null-matter-nexus-to-crucible.json) | circuit | beyond the border, 18 jumps | Null matter stored by Trade at Central Nexus carried to the station bid at The Crucible Garrison and sold there | up to 1 ships, with 65 null_matter stored at central_nexus, while the_crucible_garrison bids 300 cr for null_matter | 1 | 30 | 130 | 260 | 2026-11-26 |
