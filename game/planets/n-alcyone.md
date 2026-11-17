---
name: alcyone
id: 20261117T133325Z
tier: intel
author: Unity
kind: system
system_id: alcyone
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alcyone

- system 29 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alcyone`).

| Field | Value |
|---|---|
| Position | x 5248.2, y -4126.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 29 |
| Lanes | altair, castula, ironveil, mekbuda |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alcyone_star` | Alcyone Star | sun (M4V) | -- | -- | none | 2026-11-17 13:15 UTC | `get_system`, own ship |
| `alcyone_i` | Alcyone I | planet (scorched) | -- | -- | none | 2026-11-17 13:15 UTC | `get_system`, own ship |
| `alcyone_ii` | Alcyone II | planet (arid) | -- | -- | none | 2026-11-17 13:15 UTC | `get_system`, own ship |
| `alcyone_iii` | Alcyone III | planet (terran) | -- | -- | none | 2026-11-17 13:15 UTC | `get_system`, own ship |
| `parted_cables_field` | Parted Cables Field | asteroid_belt | -- | aluminum_ore: richness 41, 658 of 30000 left | none | 2026-11-17 13:15 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:15 UTC | own ship | Read Parted Cables Field: 658 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
