---
name: mirach
id: 20261117T041732Z
tier: intel
author: Unity
kind: system
system_id: mirach
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Mirach

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mirach`).

| Field | Value |
|---|---|
| Position | x -1414.1, y 4298.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | azha, groombridge_1618, gsc_0020, gsc_0024, hassaleh, jasmine |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mirach_star` | Mirach Star | sun (M2V) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `mirach_i` | Mirach I | planet (scorched) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `mirach_ii` | Mirach II | planet (arid) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `mirach_iii` | Mirach III | planet (terran) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `mirach_iv` | Mirach IV | planet (tundra) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `mirach_v` | Mirach V | planet (glacial) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `mirach_belt` | Mirach Belt | asteroid_belt (metallic) | -- | iron_ore: richness 33, 6784 of 100000 left; copper_ore: richness 27, 83125 of 100000 left; lithium_ore: richness 32, 440 of 25000 left | none | 2026-11-17 04:00 UTC | `get_poi`, own ship |

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
| 2026-11-17 04:00 UTC | own ship | Read Mirach Belt: 90,349 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
