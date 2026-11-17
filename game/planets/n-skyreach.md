---
name: skyreach
id: 20261117T174148Z
tier: intel
author: Unity
kind: system
system_id: skyreach
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Skyreach

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where skyreach`).

| Field | Value |
|---|---|
| Position | x 1091.7, y 5315.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | flintrock, millhaven, talitha, yed_prior |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `skyreach_star` | Skyreach Star | sun (F5V) | -- | -- | none | 2026-11-17 17:16 UTC | `get_system`, own ship |
| `skyreach_belt` | Skyreach Belt | asteroid_belt (metallic) | -- | iron_ore: richness 32, 23014 of 100000 left; copper_ore: richness 28, 23024 of 100000 left | none | 2026-11-17 17:16 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:16 UTC | own ship | Read Skyreach Belt: 46,038 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
