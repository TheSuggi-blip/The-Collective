---
name: aldhibah
id: 20261117T102822Z
tier: intel
author: Unity
kind: system
system_id: aldhibah
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Aldhibah

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where aldhibah`).

| Field | Value |
|---|---|
| Position | x -2667.3, y -1874.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | izar, oakridge, sabik |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `aldhibah_star` | Aldhibah Star | sun (F5V) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `aldhibah_i` | Aldhibah I | planet (scorched) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `aldhibah_ii` | Aldhibah II | planet (arid) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `aldhibah_ice_shelf` | Aldhibah Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 65, 36136 of 50000 left; nitrogen_ice: richness 53, 50000 of 50000 left; deuterium_ice: richness 14, 5000 of 5000 left | none | 2026-11-17 09:52 UTC | `get_poi`, own ship |
| `askance_nebula` | Askance Nebula | nebula | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |

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
| 2026-11-17 09:52 UTC | own ship | Read Aldhibah Ice Shelf: 91,136 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
