---
name: zosma
id: 20261117T174138Z
tier: intel
author: Unity
kind: system
system_id: zosma
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Zosma

- system 20 jumps from home, police level 0. Station: Hex Wellspring.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where zosma`).

| Field | Value |
|---|---|
| Position | x -1070.0, y -4084.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | cloverfield, cocibolca, driftwood, highcrest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `zosma_star` | Zosma Star | sun (M2V) | -- | -- | none | 2026-11-17 17:13 UTC | `get_system`, own ship |
| `zosma_i` | Zosma I | planet (scorched) | -- | -- | none | 2026-11-17 17:13 UTC | `get_system`, own ship |
| `zosma_belt` | Zosma Belt | asteroid_belt (metallic) | -- | iron_ore: richness 61, 17089 of 100000 left; copper_ore: richness 30, 71576 of 100000 left; lithium_ore: richness 47, 0 of 25000 left | none | 2026-11-17 17:13 UTC | `get_poi`, own ship |
| `zosma_gas_pocket` | Zosma Gas Pocket | gas_cloud (molecular_cloud) | -- | argon_gas: richness 41, 14210 of 50000 left; plasma_gas: richness 18, 2842 of 10000 left; nebula_gas: richness 12, 2843 of 10000 left; neon_gas: richness 41, 13724 of 50000 left | none | 2026-11-17 17:13 UTC | `get_poi`, own ship |
| `zosma_ice_belt` | Zosma Ice Belt | ice_field (kuiper) | -- | water_ice: richness 52, 0 of 50000 left; nitrogen_ice: richness 34, 0 of 50000 left | none | 2026-11-17 17:13 UTC | `get_poi`, own ship |
| `abd3b90fdfb39304f5996c8bfaf7645d` | Hex Wellspring | station | `8f8c70ee692d37d78dc7741e053e0f87` | -- | none | 2026-11-17 17:13 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Hex Wellspring (`8f8c70ee692d37d78dc7741e053e0f87`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:13 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 17:13 UTC | own ship | Read Zosma Belt: 88,665 units left in all | `get_poi`, own ship |
| 2026-11-17 17:13 UTC | own ship | Read Zosma Gas Pocket: 33,619 units left in all | `get_poi`, own ship |
| 2026-11-17 17:13 UTC | own ship | Read Zosma Ice Belt: nothing left | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
