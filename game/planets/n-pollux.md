---
name: pollux
id: 20261117T153751Z
tier: intel
author: Unity
kind: system
system_id: pollux
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Pollux

Nebula system 23 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where pollux`).

| Field | Value |
|---|---|
| Position | x 2186.8, y -5511.1 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 23 |
| Lanes | factory_belt, khambalia, nusakan, sadalmelik, treasure_cache |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `pollux_star` | Pollux Star | sun (K2III) | -- | -- | none | 2026-11-17 14:53 UTC | `get_system`, own ship |
| `pollux_b` | Pollux B | planet (jovian) | -- | -- | none | 2026-11-17 14:53 UTC | `get_system`, own ship |
| `pollux_outer_belt` | Pollux Outer Belt | asteroid_belt (metallic) | -- | iron_ore: richness 40, 288 of 30000 left; nickel_ore: richness 25, 10 of 15000 left; gold_ore: richness 10, 46 of 5000 left | none | 2026-11-17 14:53 UTC | `get_poi`, own ship |
| `pollux_poi_0` | Pollux | sun | -- | -- | none | 2026-11-17 14:53 UTC | `get_system`, own ship |
| `sys_0002_poi_0` | Pollux | sun | -- | -- | none | 2026-11-17 14:53 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:53 UTC | own ship | Read Pollux Outer Belt: 344 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
