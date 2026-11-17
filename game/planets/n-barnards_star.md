---
name: barnards_star
id: 20261117T092722Z
tier: intel
author: Unity
kind: system
system_id: barnards_star
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Barnard's Star

- system 11 jumps from home, police level 0. Station: Argon Bank Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where barnards_star`).

| Field | Value |
|---|---|
| Position | x 577.1, y 364.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | aspidiske, dheneb, mira, proxima_centauri |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `barnards_star_star` | Barnards Star Star | sun (M4V) | -- | -- | none | 2026-11-17 09:10 UTC | `get_system`, own ship |
| `barnards_b` | Barnards B | planet (tundra) | -- | -- | none | 2026-11-17 09:10 UTC | `get_system`, own ship |
| `barnards_star_gas_pocket` | Barnard's Star Gas Pocket | gas_cloud (molecular_cloud) | -- | argon_gas: richness 30, 15000 of 15000 left; neon_gas: richness 20, 16529 of 10000 left | none | 2026-11-17 09:10 UTC | `get_poi`, own ship |
| `patience_field` | Patience Field | asteroid_belt | -- | iron_ore: richness 43, 99999 of 100000 left; copper_ore: richness 30, 99999 of 100000 left; antimatter_containment_cell: richness 2, 128 of 128 left | none | 2026-11-17 09:10 UTC | `get_poi`, own ship |
| `greenplate_drift` | Greenplate Drift | asteroid_belt | -- | iron_ore: richness 31, 100000 of 100000 left; copper_ore: richness 30, 100000 of 100000 left; sol_alloy_ore: richness 5, 1717 of 1717 left | none | 2026-11-17 09:10 UTC | `get_poi`, own ship |
| `752347d904ac1f6c086d00ba996427dd` | Argon Bank Range | station | `f6fe3fcbef60cf6b7a97abd6fcc81030` | -- | none | 2026-11-17 09:10 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Argon Bank Range (`f6fe3fcbef60cf6b7a97abd6fcc81030`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 09:10 UTC | `get_system`, own ship |

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
| 2026-11-17 09:10 UTC | own ship | Read Barnard's Star Gas Pocket: 31,529 units left in all | `get_poi`, own ship |
| 2026-11-17 09:10 UTC | own ship | Read Patience Field: 200,126 units left in all | `get_poi`, own ship |
| 2026-11-17 09:10 UTC | own ship | Read Greenplate Drift: 201,717 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
