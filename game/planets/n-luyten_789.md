---
name: luyten_789
id: 20261117T143547Z
tier: intel
author: Unity
kind: system
system_id: luyten_789
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Luyten 789

- system 28 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where luyten_789`).

| Field | Value |
|---|---|
| Position | x 5263.0, y -5176.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 28 |
| Lanes | ashmark, castula, gsc_0029, mekbuda |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `luyten_789_star` | Luyten 789 Star | sun (F5V) | -- | -- | none | 2026-11-17 13:46 UTC | `get_system`, own ship |
| `luyten_789_i` | Luyten 789 I | planet (scorched) | -- | -- | none | 2026-11-17 13:46 UTC | `get_system`, own ship |
| `luyten_789_frost_ring` | Luyten 789 Frost Ring | ice_field (kuiper) | -- | nitrogen_ice: richness 30, 2012 of 50000 left; deuterium_ice: richness 15, 646 of 5000 left; helium_ice: richness 24, 642 of 5000 left | none | 2026-11-17 13:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:46 UTC | own ship | Read Luyten 789 Frost Ring: 3,300 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
