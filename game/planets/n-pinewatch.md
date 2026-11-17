---
name: pinewatch
id: 20261117T194617Z
tier: intel
author: Unity
kind: system
system_id: pinewatch
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Pinewatch

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where pinewatch`).

| Field | Value |
|---|---|
| Position | x 453.3, y -2360.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | gsc_0009, peacock, revati |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `pinewatch_star` | Pinewatch Star | sun (K4V) | -- | -- | none | 2026-11-17 19:10 UTC | `get_system`, own ship |
| `pinewatch_i` | Pinewatch I | planet (scorched) | -- | -- | none | 2026-11-17 19:10 UTC | `get_system`, own ship |
| `pinewatch_vapor_fields` | Pinewatch Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 52, 987 of 50000 left; argon_gas: richness 37, 999 of 50000 left; xenon_gas: richness 27, 478 of 10000 left; neon_gas: richness 38, 994 of 50000 left | none | 2026-11-17 19:10 UTC | `get_poi`, own ship |

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
| 2026-11-17 19:10 UTC | own ship | Read Pinewatch Vapor Fields: 3,458 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
