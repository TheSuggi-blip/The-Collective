---
name: flintrock
id: 20261117T133336Z
tier: intel
author: Unity
kind: system
system_id: flintrock
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Flintrock

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where flintrock`).

| Field | Value |
|---|---|
| Position | x 1057.0, y 5930.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | gsc_0008, millhaven, skyreach, violethall |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `flintrock_star` | Flintrock Star | sun (M4V) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `flintrock_i` | Flintrock I | planet (scorched) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `flintrock_ii` | Flintrock II | planet (arid) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `flintrock_iii` | Flintrock III | planet (terran) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `flintrock_iv` | Flintrock IV | planet (tundra) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `flintrock_v` | Flintrock V | planet (glacial) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `flintrock_vapor_fields` | Flintrock Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 58, 12728 of 50000 left; plasma_gas: richness 20, 8822 of 10000 left; neon_gas: richness 40, 49201 of 50000 left; chlorine_gas: richness 25, 2369 of 10000 left | none | 2026-11-17 13:18 UTC | `get_poi`, own ship |

## Stations

None on the chart.

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
| 2026-11-17 13:18 UTC | own ship | Read Flintrock Vapor Fields: 73,120 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
