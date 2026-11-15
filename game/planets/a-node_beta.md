---
name: node_beta
id: 20261115T040557Z
tier: intel
author: Unity
kind: system
system_id: node_beta
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 80
updated: 2026-11-15
---

# Node Beta

First system out of Nexus Prime on the southern lane; Voidborn industry. A lane leads on into lawless space (Schedar).

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where node_beta`).

| Field | Value |
|---|---|
| Position | x -3995.4, y 2584.9 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 1 |
| Lanes | acubens, gsc_0027, nexus_prime, node_alpha, node_gamma, schedar |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `eltanin_prime_star` | Eltanin Prime Star | sun (K2III) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `beta_foundry` | Beta Foundry | planet (arid) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `beta_assembly` | Beta Assembly | planet (tundra) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `eltanin_prime_belt` | Eltanin Prime Belt | asteroid_belt (metallic) | -- | carbon_ore: richness 49, 0 of 30000 left; vanadium_ore: richness 48, 0 of 25000 left; tungsten_ore: richness 32, 0 of 25000 left; platinum_ore: richness 14, 0 of 8000 left; void_essence: richness 5, 0 of 300 left | none | 2026-11-15 03:55 UTC | `get_poi`, own ship |
| `node_beta_frozen_drift` | Node Beta Frozen Drift | ice_field (kuiper) | -- | not read | none | 2026-11-15 UTC | `get_system`, own ship |
| `node_beta_industrial_station` | Node Beta Industrial Station | station | Node Beta Industrial Station (`node_beta_industrial_station`); see Stations | -- | none | 2026-11-15 03:33 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Node Beta Industrial Station (`node_beta_industrial_station`) | voidborn | public (a ship of ours docked) | crafting, marine_training, market, medical, missions, personnel, refuel, repair, shipyard, storage | 11 cr per unit (9 + 2 empire tax) | unknown | 2026-11-15 03:33 UTC | `get_poi`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | ally | Unity | Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 03:33 UTC | own ship | Docked at Node Beta Industrial Station: services and fuel price read | `get_poi`, own ship |
| 2026-11-15 03:55 UTC | own ship | Read the ore at Eltanin Prime Belt: nothing left to mine | `get_poi`, own ship |

## Notes

- Every belt read here was mined out, or all but, on 2026-11-15. Deposits are shared and refill gradually, common ores fastest (https://www.spacemolt.com/docs/mining.md); how long a refill takes and who takes the ore is not known. Read again before sending miners.
- Not read yet: `node_beta_frozen_drift`. Ice needs an ice harvester, gas a gas harvester (https://www.spacemolt.com/docs/mining.md).
- Market fee, docking rules for other empires and the station's order book over time are not recorded here. Prices live in the unit's data folder, not in this file.
