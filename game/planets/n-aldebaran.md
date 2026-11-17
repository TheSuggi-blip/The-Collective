---
name: aldebaran
id: 20261117T000621Z
tier: intel
author: Unity
kind: system
system_id: aldebaran
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Aldebaran

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where aldebaran`).

| Field | Value |
|---|---|
| Position | x -6325.0, y 1009.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | giausar, gsc_0028, gsc_0040, sadalsuud |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `aldebaran_star` | Aldebaran Star | sun (M6V) | -- | -- | none | 2026-11-16 23:50 UTC | `get_system`, own ship |
| `aldebaran_i` | Aldebaran I | planet (scorched) | -- | -- | none | 2026-11-16 23:50 UTC | `get_system`, own ship |
| `aldebaran_ice_shelf` | Aldebaran Ice Shelf | ice_field (kuiper) | -- | nitrogen_ice: richness 51, 50000 of 50000 left | none | 2026-11-16 23:50 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:50 UTC | own ship | Read Aldebaran Ice Shelf: 50,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
