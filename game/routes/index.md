---
name: routes-index
id: 20261115T153923Z
tier: intel
author: Unity
---

# index.md -- Routes We Fly

Written by `python3 -B game/fleet/routes.py index`, never by hand. A route is a
task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured.

| Route | Kind | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|
| [census-voidborn](census-voidborn.json) | census | Read one Voidborn system whole: deposits, creatures, order book, mission board | up to 3 ships | TBD | TBD | TBD | TBD | -- |
| [first-survey](first-survey.json) | circuit | Signal Propagation Survey: dock at the five other Voidborn stations (20,000 cr) | once per pilot, off | TBD | TBD | TBD | TBD | -- |
| [voidborn-missions-1](voidborn-missions-1.json) | circuit | Synchrony Relay Run and Crystal Delivery: two board missions in one circuit of 8 jumps | once per pilot | 55 | 21 | 8,690 | one-time | 2026-11-15 |
| [voidborn-substrate](voidborn-substrate.json) | circuit | Substrate Delivery: two neural soma bought at Central Nexus, the mission taken at Node Alpha and handed in at Central Nexus; 2 jumps | once per pilot | TBD | TBD | TBD | TBD | -- |
| [hunt-acubens-urchin](hunt-acubens-urchin.json) | hunt | Cinder-urchins at Acubens Shadow Pocket; radiant bile sold at Node Gamma | up to 1 ships, off | 2 | 25 | -120 | -290 | 2026-11-15 |
| [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | hunt | Veil-rays at GSC-0027 Prism Scatter; verdigris curd sold at Node Beta | up to 1 ships | 1 | 46 | 3,220 | 4,220 | 2026-11-15 |
| [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | hunt | Veil-rays at Hamal Crystal Bloom; verdigris curd sold at Node Beta | up to 1 ships | 2 | 29 | 1,950 | 3,970 | 2026-11-15 |
| [hunt-home-drift-ray](hunt-home-drift-ray.json) | hunt | Drift-rays at Stellar Siphon in Nexus Prime; goods sold or stored at Central Nexus | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-home-whale](hunt-home-whale.json) | hunt | Pilot-whales at Stellar Siphon in Nexus Prime; whale oil sold at Node Beta | up to 1 ships, needs piercing_railgun_i, off | 1 | 20 | 570 | 1,670 | 2026-11-15 |
| [mine-acubens](mine-acubens.json) | mine | Iron and copper at Acubens Shadow Pocket; ore into storage at Node Beta | up to 16 ships | TBD | TBD | TBD | TBD | -- |
| [mine-bellatrix](mine-bellatrix.json) | mine | Wait at Bellatrix Major Belt beside Node Gamma station for whatever regrows (thorium, palladium, iridium, carbon) | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [mine-gsc-seep](mine-gsc-seep.json) | mine | Iron and copper at GSC-0027 Spacetime Seep; ore into storage at Node Beta | up to 16 ships | TBD | TBD | TBD | TBD | -- |
| [mine-pherkad-rift](mine-pherkad-rift.json) | mine | Copper and iron at Pherkad Null Rift; ore into storage at Synchrony Hub | every pilot | TBD | TBD | TBD | TBD | -- |

## The Plan

`plan.json`: per role, the routes the dispatcher tries in this order for a free pilot.

| Role | Routes, first that is open |
|---|---|
| command | voidborn-substrate > voidborn-missions-1 > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| drone | voidborn-substrate > voidborn-missions-1 > hunt-gsc-veil-ray > hunt-hamal-veil-ray > hunt-home-drift-ray > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| hauler | voidborn-substrate > voidborn-missions-1 > mine-bellatrix > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| miner | voidborn-substrate > voidborn-missions-1 > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| scout | voidborn-substrate > voidborn-missions-1 > census-voidborn > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| sentinel | voidborn-substrate > voidborn-missions-1 > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| trader | voidborn-substrate > voidborn-missions-1 > mine-bellatrix > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
