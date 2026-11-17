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

Routes: 29.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [census-voidborn](census-voidborn.json) | census | home space | Read one Voidborn system whole: deposits, creatures, order book, mission board | up to 4 ships | 191 | 7 | -50 | -360 | 2026-11-16 |
| [craft-steel-node-beta](craft-steel-node-beta.json) | circuit | home space | Steel plate made by hand at the Node Beta workshop from the pilot's own stored iron ore, kept in its storage there for the faction's ladder and the station (the reserve) | up to 1 ships, with 600 iron_ore stored at node_beta_industrial_station, standing work | TBD | TBD | TBD | TBD | -- |
| [park](park.json) | circuit | home space | Dock at Central Nexus and wait there: a docked ship costs nothing | the park route | 78 | 5 | 120 | 1,530 | 2026-11-17 |
| [train-navigation-trader](train-navigation-trader.json) | circuit | home space | Navigation for traders one level short of Signal Fragments: five jumps through our own stations, nothing carried | up to 20 ships, under navigation 3, standing work | 3 | 18 | -160 | -560 | 2026-11-16 |
| [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | hunt | home space | Veil-rays at GSC-0027 Prism Scatter; verdigris curd sold at Central Nexus | up to 1 ships, without piercing_railgun_i, standing work | 6 | 25 | -70 | -180 | 2026-11-16 |
| [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | hunt | home space | Veil-rays at Hamal Crystal Bloom; verdigris curd sold at Central Nexus | up to 1 ships, without piercing_railgun_i, standing work | TBD | TBD | TBD | TBD | -- |
| [hunt-home-drift-ray](hunt-home-drift-ray.json) | hunt | home space | Drift-rays at Stellar Siphon in Nexus Prime; goods sold or stored at Central Nexus | up to 1 ships, standing work | 21 | 10 | -40 | -200 | 2026-11-17 |
| [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) | mine | home space | Standing work: carbon ore at Acubens Belt into storage at Node Beta (the faction's circuit boards) | up to 1 ships, needs mining_laser_i, empty hold, standing work | 1 | 45 | -170 | -220 | 2026-11-17 |
| [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) | mine | home space | Standing work: iron and copper at GSC-0027 Prism Scatter into storage at Node Beta (S6) | up to 66 ships, needs mining_laser_i, standing work | 503 | 45 | -100 | -140 | 2026-11-16 |
| [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | mine | home space | Standing work: iron at GSC-0027 Spacetime Seep into storage at Node Beta (S6) | up to 6 ships, standing work | 36 | 45 | -120 | -160 | 2026-11-16 |
| [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) | mine | home space | Standing work: iron and copper at Hamal Crystal Bloom into storage at Node Beta (S6) | up to 97 ships, needs mining_laser_i, standing work | 300 | 45 | -140 | -180 | 2026-11-16 |
| [mine-acubens](mine-acubens.json) | mine | home space | Iron and copper at Acubens Shadow Pocket; ore into storage at Node Beta | up to 18 ships, needs mining_laser_i, standing work | 102 | 45 | -130 | -180 | 2026-11-16 |
| [mine-bellatrix](mine-bellatrix.json) | mine | home space | Wait at Bellatrix Major Belt beside Node Gamma station for whatever regrows (thorium, palladium, iridium, carbon) | up to 1 ships, standing work | TBD | TBD | TBD | TBD | -- |
| [mine-gsc-seep](mine-gsc-seep.json) | mine | home space | Iron and copper at GSC-0027 Spacetime Seep; ore into storage at Node Beta | up to 16 ships, standing work | TBD | TBD | TBD | TBD | -- |
| [mine-pherkad-rift](mine-pherkad-rift.json) | mine | home space | Copper and iron at Pherkad Null Rift; ore into storage at Synchrony Hub | up to 18 ships, needs mining_laser_i, standing work | 62 | 45 | -130 | -180 | 2026-11-16 |
| [census-frontier](census-frontier.json) | census | beyond the border, 7 jumps | Read one lawless system around our space whole: deposits, creatures, stations, order books, mission boards | up to 12 ships, empty hold | 119 | 14 | -140 | -620 | 2026-11-16 |
| [census-guard-ice](census-guard-ice.json) | census | beyond the border, 7 jumps | Guard by census: read whole, every hour, the lawless systems where our miners work | up to 2 ships, empty hold | 68 | 13 | -140 | -610 | 2026-11-16 |
| [census-roads](census-roads.json) | census | beyond the border, 15 jumps | Explore the roads to the station sites: read every system on the way to Aldebaran, Yildun, Hawthorne and Alchiba, and those beside them | up to 10 ships, empty hold | 5 | 22 | -240 | -620 | 2026-11-17 |
| [census-worked](census-worked.json) | census | beyond the border, 9 jumps | Read the places our routes use beyond home twice in a turn: deposits, creatures, order books, mission boards | up to 6 ships, empty hold | 5 | 13 | -140 | -710 | 2026-11-17 |
| [guard-ironhollow-fading-signal](guard-ironhollow-fading-signal.json) | guard | beyond the border, 4 jumps | Guard at Ironhollow Fading Signal while miners of ours gather iron there; docks at The Experiment | up to 1 ships, empty hold, standing work | TBD | TBD | TBD | TBD | -- |
| [guard-marfik-emission-nebula](guard-marfik-emission-nebula.json) | guard | beyond the border, 6 jumps | Guard at Marfik Emission Nebula while a ship of ours mines gas there; docks at Node Beta | up to 1 ships, empty hold, standing work | 1 | 73 | -130 | -110 | 2026-11-16 |
| [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at cedarhold_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 4 | 10 | -100 | -620 | 2026-11-17 |
| [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at faintlight_drift; loot sold at Node Beta Industrial Station | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 5 | 30 | -120 | -270 | 2026-11-16 |
| [hunt-keid-belt-carapace](hunt-keid-belt-carapace.json) | hunt | beyond the border, 5 jumps | Belt-grazers and patina-grazers at Keid Belt; creature carapace into storage at Node Beta | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 5 | 14 | -110 | -350 | 2026-11-17 |
| [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at keid_fractured_prism; loot sold at Node Beta Industrial Station | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 5 | 27 | -90 | -220 | 2026-11-16 |
| [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | hunt | beyond the border, 4 jumps | veil_ray at low_charge_glint; loot sold at Node Beta Industrial Station | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 8 | 23 | -100 | -300 | 2026-11-17 |
| [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | hunt | beyond the border, 4 jumps | Veil-rays at Ruchbah Broken Glass Veil (lawless); verdigris curd sold at The Experiment | up to 1 ships, without piercing_railgun_i, empty hold, standing work | 3 | 8 | -70 | -360 | 2026-11-16 |
| [gather-ironhollow-fading-signal](gather-ironhollow-fading-signal.json) | mine | beyond the border, 4 jumps | Standing work, a test: iron at Ironhollow Fading Signal (beyond the border) into storage at The Experiment | up to 11 ships, needs mining_laser_i, empty hold, standing work | 1 | 45 | -160 | -220 | 2026-11-16 |
| [gather-schedar-belt](gather-schedar-belt.json) | mine | beyond the border, 2 jumps | Standing work, a test: iron at Schedar Belt (beyond the border, one jump from Node Beta) into storage at Node Beta | up to 2 ships, needs mining_laser_i, empty hold, standing work | TBD | TBD | TBD | TBD | -- |
