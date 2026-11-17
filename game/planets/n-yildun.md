---
name: yildun
id: 20261117T010832Z
tier: intel
author: Unity
kind: system
system_id: yildun
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Yildun

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where yildun`).

| Field | Value |
|---|---|
| Position | x -5474.1, y 89.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | avior, gsc_0042, mizar, rasalhague |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `yildun_star` | Yildun Star | sun (A1V) | -- | -- | none | 2026-11-17 00:04 UTC | `get_system`, own ship |
| `yildun_disk` | Yildun Disk | asteroid_belt (mixed) | -- | iron_ore: richness 50, 27712 of 35000 left; copper_ore: richness 40, 29501 of 30000 left; aluminum_ore: richness 30, 102 of 20000 left; titanium_ore: richness 15, 3 of 8000 left | none | 2026-11-17 00:04 UTC | `get_poi`, own ship |
| `yildun_outer_ice` | Yildun Outer Ice | ice_field (kuiper) | -- | water_ice: richness 55, 45000 of 45000 left; nitrogen_ice: richness 30, 20000 of 20000 left | none | 2026-11-17 00:04 UTC | `get_poi`, own ship |
| `neverworld_carbon` | Neverworld Carbon | asteroid_belt | -- | carbon_ore: richness 23, 66 of 30000 left | none | 2026-11-17 00:04 UTC | `get_poi`, own ship |
| `sys_0160_poi_0` | Yildun | sun | -- | -- | none | 2026-11-17 00:04 UTC | `get_system`, own ship |

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
| 2026-11-17 00:04 UTC | own ship | Read Yildun Disk: 57,318 units left in all | `get_poi`, own ship |
| 2026-11-17 00:04 UTC | own ship | Read Yildun Outer Ice: 65,000 units left in all | `get_poi`, own ship |
| 2026-11-17 00:04 UTC | own ship | Read Neverworld Carbon: 66 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
