---
name: 36_ophiuchi
id: 20261117T143523Z
tier: intel
author: Unity
kind: system
system_id: 36_ophiuchi
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# 36 Ophiuchi

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where 36_ophiuchi`).

| Field | Value |
|---|---|
| Position | x -452.0, y -4643.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | azelfafage, gsc_0001, highcrest, maia |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `36_ophiuchi_star` | 36 Ophiuchi Star | sun (K1V) | -- | -- | none | 2026-11-17 14:22 UTC | `get_system`, own ship |
| `36_ophiuchi_belt` | 36 Ophiuchi Belt | asteroid_belt (mixed) | -- | iron_ore: richness 45, 3832 of 28000 left; copper_ore: richness 35, 3865 of 20000 left; nickel_ore: richness 20, 911 of 10000 left; chromium_ore: richness 20, 1031 of 9000 left | none | 2026-11-17 14:22 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:22 UTC | own ship | Read 36 Ophiuchi Belt: 9,639 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
