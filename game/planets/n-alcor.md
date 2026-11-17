---
name: alcor
id: 20261117T123122Z
tier: intel
author: Unity
kind: system
system_id: alcor
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alcor

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alcor`).

| Field | Value |
|---|---|
| Position | x 275.8, y -7504.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | embervale, menkalinan, mirzam, sadalbari, yarrowfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alcor_star` | Alcor Star | sun (A5V) | -- | -- | none | 2026-11-17 12:21 UTC | `get_system`, own ship |
| `alcor_disk` | Alcor Disk | asteroid_belt (mixed) | -- | iron_ore: richness 40, 10197 of 25000 left; copper_ore: richness 30, 10202 of 18000 left; aluminum_ore: richness 20, 6861 of 12000 left | none | 2026-11-17 12:21 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:21 UTC | own ship | Read Alcor Disk: 27,260 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
