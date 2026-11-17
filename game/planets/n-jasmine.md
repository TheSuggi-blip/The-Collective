---
name: jasmine
id: 20261117T041730Z
tier: intel
author: Unity
kind: system
system_id: jasmine
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Jasmine

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where jasmine`).

| Field | Value |
|---|---|
| Position | x -1712.6, y 4620.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | azha, biham, gliese_876, gsc_0024, gsc_0035, mirach |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `jasmine_star` | Jasmine Star | sun (G8V) | -- | -- | none | 2026-11-17 03:55 UTC | `get_system`, own ship |
| `jasmine_i` | Jasmine I | planet (scorched) | -- | -- | none | 2026-11-17 03:55 UTC | `get_system`, own ship |
| `jasmine_ii` | Jasmine II | planet (arid) | -- | -- | none | 2026-11-17 03:55 UTC | `get_system`, own ship |
| `jasmine_silent_reef` | Jasmine Silent Reef | asteroid_belt (metallic) | -- | iron_ore: richness 40, 10171 of 30000 left; copper_ore: richness 20, 9526 of 15000 left; titanium_ore: richness 25, 50 of 15000 left | none | 2026-11-17 03:55 UTC | `get_poi`, own ship |

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
| 2026-11-17 03:55 UTC | own ship | Read Jasmine Silent Reef: 19,747 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
