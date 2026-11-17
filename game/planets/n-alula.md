---
name: alula
id: 20261117T123127Z
tier: intel
author: Unity
kind: system
system_id: alula
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alula

- system 21 jumps from home, police level 0. Station: Ashborne Reach.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alula`).

| Field | Value |
|---|---|
| Position | x 2889.9, y -3698.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | alrakis, cargo_lanes, farpoint |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alula_star` | Alula Star | sun (K2V) | -- | -- | none | 2026-11-17 11:54 UTC | `get_system`, own ship |
| `alula_i` | Alula I | planet (scorched) | -- | -- | none | 2026-11-17 11:54 UTC | `get_system`, own ship |
| `alula_ii` | Alula II | planet (arid) | -- | -- | none | 2026-11-17 11:54 UTC | `get_system`, own ship |
| `alula_belt` | Alula Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 11:54 UTC | `get_system`, own ship |
| `alula_gas_pocket` | Alula Gas Pocket | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 11:54 UTC | `get_system`, own ship |
| `alula_frost_ring` | Alula Frost Ring | ice_field (kuiper) | -- | water_ice: richness 56, 293 of 50000 left; helium_ice: richness 13, 555 of 5000 left | none | 2026-11-17 11:54 UTC | `get_poi`, own ship |
| `fbdce01eaa4492be64ca3957c27cf56d` | Ashborne Reach | station | `644abb10f5991781c61da439b629a327` | -- | none | 2026-11-17 11:54 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Ashborne Reach (`644abb10f5991781c61da439b629a327`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 11:54 UTC | `get_system`, own ship |

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
| 2026-11-17 11:54 UTC | own ship | Read Alula Frost Ring: 848 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `alula_belt`, `alula_gas_pocket`.
