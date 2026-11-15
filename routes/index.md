---
name: routes-index
id: 20261115T153923Z
tier: intel
author: Unity
---

# index.md -- Routes We Fly

Written by `python3 -B fleet/routes.py index`, never by hand. A route is a
task one pilot carries out by itself; its file is `routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured.

| Route | Kind | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|
| [census-voidborn](census-voidborn.json) | census | Read one Voidborn system whole: deposits, creatures, order book, mission board | up to 3 ships | 17 | 7 | 0 | 0 | 2026-11-15 |
| [first-survey](first-survey.json) | circuit | Signal Propagation Survey: dock at the five other Voidborn stations (20,000 cr) | once per pilot, off | TBD | TBD | TBD | TBD | -- |
| [voidborn-missions-1](voidborn-missions-1.json) | circuit | Synchrony Relay Run and Crystal Delivery: two board missions in one circuit of 8 jumps | once per pilot | 55 | 21 | 8,690 | one-time | 2026-11-15 |
| [hunt-acubens-urchin](hunt-acubens-urchin.json) | hunt | Cinder-urchins at Acubens Shadow Pocket; radiant bile sold at Node Gamma | up to 1 ships | 2 | 25 | 540 | 1,310 | 2026-11-15 |
| [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | hunt | Veil-rays at GSC-0027 Prism Scatter; verdigris curd sold at Node Gamma | up to 1 ships | 1 | 46 | 3,220 | 4,220 | 2026-11-15 |
| [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | hunt | Veil-rays at Hamal Crystal Bloom; verdigris curd sold at Node Gamma | up to 1 ships | 1 | 23 | 3,000 | 7,710 | 2026-11-15 |
| [hunt-home-whale](hunt-home-whale.json) | hunt | Pilot-whales at Stellar Siphon in Nexus Prime; whale oil sold at Node Beta | up to 1 ships, needs piercing_railgun_i, off | 1 | 20 | 570 | 1,670 | 2026-11-15 |
| [mine-acubens](mine-acubens.json) | mine | Iron and copper at Acubens Shadow Pocket; ore into storage at Node Beta | up to 16 ships | 17 | 45 | 0 | 0 | 2026-11-15 |
| [mine-gsc-seep](mine-gsc-seep.json) | mine | Iron and copper at GSC-0027 Spacetime Seep; ore into storage at Node Beta | up to 16 ships | 16 | 45 | 0 | 0 | 2026-11-15 |
| [mine-pherkad-rift](mine-pherkad-rift.json) | mine | Copper and iron at Pherkad Null Rift; ore into storage at Synchrony Hub | up to 16 ships | 16 | 45 | 0 | 0 | 2026-11-15 |

## The Plan

`plan.json`: per role, the routes the dispatcher tries in this order for a free pilot.

| Role | Routes, first that is open |
|---|---|
| drone | voidborn-missions-1 > hunt-home-whale > hunt-acubens-urchin > hunt-hamal-veil-ray > hunt-gsc-veil-ray > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| hauler | voidborn-missions-1 > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| miner | voidborn-missions-1 > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| scout | voidborn-missions-1 > census-voidborn > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
| trader | voidborn-missions-1 > mine-acubens > mine-gsc-seep > mine-pherkad-rift |
