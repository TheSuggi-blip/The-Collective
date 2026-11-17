---
name: alchiba
id: 20261117T010821Z
tier: intel
author: Unity
kind: system
system_id: alchiba
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alchiba

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alchiba`).

| Field | Value |
|---|---|
| Position | x -5125.7, y -1497.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | birchwood, dschubba, hawthorne, pinecross |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alchiba_star` | Alchiba Star | sun (M6V) | -- | -- | none | 2026-11-17 00:48 UTC | `get_system`, own ship |
| `alchiba_ice_belt` | Alchiba Ice Belt | ice_field (kuiper) | -- | water_ice: richness 67, 27529 of 50000 left; nitrogen_ice: richness 32, 50000 of 50000 left | none | 2026-11-17 00:48 UTC | `get_poi`, own ship |

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
| 2026-11-17 00:48 UTC | own ship | Read Alchiba Ice Belt: 77,529 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
