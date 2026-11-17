---
name: saltwind
id: 20261117T021126Z
tier: intel
author: Unity
kind: system
system_id: saltwind
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Saltwind

- system 11 jumps from home, police level 0. Station: ENDL:saltwind.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where saltwind`).

| Field | Value |
|---|---|
| Position | x -4711.3, y -201.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | mizar, rasalhague, tania |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `saltwind_star` | Saltwind Star | sun (A0V) | -- | -- | none | 2026-11-17 01:05 UTC | `get_system`, own ship |
| `saltwind_i` | Saltwind I | planet (scorched) | -- | -- | none | 2026-11-17 01:05 UTC | `get_system`, own ship |
| `saltwind_ii` | Saltwind II | planet (arid) | -- | -- | none | 2026-11-17 01:05 UTC | `get_system`, own ship |
| `saltwind_iii` | Saltwind III | planet (terran) | -- | -- | none | 2026-11-17 01:05 UTC | `get_system`, own ship |
| `saltwind_iv` | Saltwind IV | planet (tundra) | -- | -- | none | 2026-11-17 01:05 UTC | `get_system`, own ship |
| `saltwind_gas_pocket` | Saltwind Gas Pocket | gas_cloud (molecular_cloud) | -- | argon_gas: richness 50, 50000 of 50000 left; xenon_gas: richness 17, 10000 of 10000 left; nebula_gas: richness 24, 10000 of 10000 left; neon_gas: richness 41, 49995 of 50000 left; fluorine_gas: richness 11, 5000 of 5000 left | none | 2026-11-17 01:05 UTC | `get_poi`, own ship |
| `saltwind_ice_shelf` | Saltwind Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 65, 49044 of 50000 left; nitrogen_ice: richness 47, 50000 of 50000 left | none | 2026-11-17 01:05 UTC | `get_poi`, own ship |
| `c9455e7696471e38ad4bfc7ae5b45bc5` | ENDL:saltwind | station | `7d371fd119a1ea5b1048344ff1882a32` | -- | none | 2026-11-17 01:05 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| ENDL:saltwind (`7d371fd119a1ea5b1048344ff1882a32`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 01:05 UTC | `get_system`, own ship |

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
| 2026-11-17 01:05 UTC | own ship | Read Saltwind Gas Pocket: 124,995 units left in all | `get_poi`, own ship |
| 2026-11-17 01:05 UTC | own ship | Read Saltwind Ice Shelf: 99,044 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
