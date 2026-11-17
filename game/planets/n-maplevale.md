---
name: maplevale
id: 20261117T102827Z
tier: intel
author: Unity
kind: system
system_id: maplevale
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Maplevale

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where maplevale`).

| Field | Value |
|---|---|
| Position | x -899.2, y -1802.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | dubhe, miaplacidus, ross_154 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `maplevale_star` | Maplevale Star | sun (G2V) | -- | -- | none | 2026-11-17 10:14 UTC | `get_system`, own ship |
| `maplevale_i` | Maplevale I | planet (scorched) | -- | -- | none | 2026-11-17 10:14 UTC | `get_system`, own ship |
| `maplevale_ii` | Maplevale II | planet (arid) | -- | -- | none | 2026-11-17 10:14 UTC | `get_system`, own ship |
| `maplevale_iii` | Maplevale III | planet (terran) | -- | -- | none | 2026-11-17 10:14 UTC | `get_system`, own ship |
| `maplevale_vapor_fields` | Maplevale Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 44, 616 of 50000 left; argon_gas: richness 32, 640 of 50000 left; plasma_gas: richness 24, 385 of 10000 left; xenon_gas: richness 26, 395 of 10000 left; nebula_gas: richness 17, 398 of 10000 left; neon_gas: richness 54, 613 of 50000 left; chlorine_gas: richness 29, 369 of 10000 left | none | 2026-11-17 10:14 UTC | `get_poi`, own ship |

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
| 2026-11-17 10:14 UTC | own ship | Read Maplevale Vapor Fields: 3,416 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
