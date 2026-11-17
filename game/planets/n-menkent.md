---
name: menkent
id: 20261117T092733Z
tier: intel
author: Unity
kind: system
system_id: menkent
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Menkent

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where menkent`).

| Field | Value |
|---|---|
| Position | x -250.1, y 3915.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | jadecove, pipirima |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `menkent_star` | Menkent Star | sun (M6V) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `menkent_frost_ring` | Menkent Frost Ring | ice_field (kuiper) | -- | water_ice: richness 40, 3066 of 50000 left; nitrogen_ice: richness 52, 50000 of 50000 left; deuterium_ice: richness 11, 3881 of 5000 left | none | 2026-11-17 08:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:44 UTC | own ship | Read Menkent Frost Ring: 56,947 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
