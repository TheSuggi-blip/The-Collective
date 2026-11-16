---
name: routes-index-standing-work
id: 20261116T174327Z
tier: intel
author: Unity
---

# index-standing-work.md -- Standing Work, Reading and Waiting

Written by `python3 -B game/fleet/routes.py index`, never by hand. Standing work (it trains a skill or gathers into storage and is not judged on its pay), the census and the park route: they keep every ship busy and the picture fresh.
A route is a task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured. Home space first, then by
kind and name. Up: [master-index.md](master-index.md).

Routes: 11.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [census-voidborn](census-voidborn.json) | census | home space | Read one Voidborn system whole: deposits, creatures, order book, mission board | up to 3 ships | 343 | 8 | -70 | -530 | 2026-11-16 |
| [park](park.json) | circuit | home space | Dock at Central Nexus and wait there: a docked ship costs nothing | the park route | 216 | 5 | -50 | -670 | 2026-11-16 |
| [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | mine | home space | Standing work: iron and copper at GSC-0027 Prism Scatter into storage at Node Beta (S6) | up to 50 ships, needs mining_laser_i, standing work | 80 | 45 | -90 | -120 | 2026-11-16 |
| [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | mine | home space | Standing work: iron at GSC-0027 Spacetime Seep into storage at Node Beta (S6) | up to 6 ships, standing work | 12 | 45 | -120 | -150 | 2026-11-16 |
| [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | mine | home space | Standing work: iron and copper at Hamal Crystal Bloom into storage at Node Beta (S6) | up to 50 ships, needs mining_laser_i, standing work | 81 | 45 | -130 | -170 | 2026-11-16 |
| [mine-acubens](mine-acubens.json) | mine | home space | Iron and copper at Acubens Shadow Pocket; ore into storage at Node Beta | up to 18 ships, needs mining_laser_i, standing work | 116 | 45 | -120 | -170 | 2026-11-16 |
| [mine-bellatrix](mine-bellatrix.json) | mine | home space | Wait at Bellatrix Major Belt beside Node Gamma station for whatever regrows (thorium, palladium, iridium, carbon) | up to 1 ships, standing work | 8 | 45 | 0 | 0 | 2026-11-15 |
| [mine-gsc-seep](mine-gsc-seep.json) | mine | home space | Iron and copper at GSC-0027 Spacetime Seep; ore into storage at Node Beta | up to 16 ships, standing work | 48 | 45 | -120 | -160 | 2026-11-15 |
| [mine-pherkad-rift](mine-pherkad-rift.json) | mine | home space | Copper and iron at Pherkad Null Rift; ore into storage at Synchrony Hub | up to 18 ships, needs mining_laser_i, standing work | 285 | 45 | -100 | -170 | 2026-11-16 |
| [census-frontier](census-frontier.json) | census | beyond the border, 7 jumps | Read one lawless system around our space whole: deposits, creatures, stations, order books, mission boards | up to 12 ships, empty hold | 195 | 15 | -160 | -630 | 2026-11-16 |
| [census-guard-ice](census-guard-ice.json) | census | beyond the border, 7 jumps | Guard by census: read whole, every hour, the lawless systems where our miners work | up to 2 ships, empty hold | 68 | 13 | -140 | -610 | 2026-11-16 |
