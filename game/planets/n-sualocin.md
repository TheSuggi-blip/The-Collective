---
name: sualocin
id: 20261117T041733Z
tier: intel
author: Unity
kind: system
system_id: sualocin
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sualocin

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sualocin`).

| Field | Value |
|---|---|
| Position | x -2398.0, y 5217.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | biham, coppervale, elnath, felis, gsc_0035 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sualocin_star` | Sualocin Star | sun (B6IV) | -- | -- | none | 2026-11-17 03:53 UTC | `get_system`, own ship |
| `sualocin_belt` | Sualocin Belt | asteroid_belt (metallic) | -- | iron_ore: richness 43, 100000 of 100000 left; copper_ore: richness 26, 100000 of 100000 left | none | 2026-11-17 03:53 UTC | `get_poi`, own ship |

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
| 2026-11-17 03:53 UTC | own ship | Read Sualocin Belt: 200,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
