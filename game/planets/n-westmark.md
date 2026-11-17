---
name: westmark
id: 20261117T112936Z
tier: intel
author: Unity
kind: system
system_id: westmark
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Westmark

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where westmark`).

| Field | Value |
|---|---|
| Position | x 1659.1, y 3688.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | alshain, angetenar, mebsuta, subra, wasat |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `westmark_star` | Westmark Star | sun (M2V) | -- | -- | none | 2026-11-17 10:50 UTC | `get_system`, own ship |
| `westmark_i` | Westmark I | planet (scorched) | -- | -- | none | 2026-11-17 10:50 UTC | `get_system`, own ship |
| `westmark_belt` | Westmark Belt | asteroid_belt (metallic) | -- | iron_ore: richness 42, 38057 of 100000 left; copper_ore: richness 42, 29830 of 100000 left; silver_ore: richness 30, 0 of 25000 left; zinc_ore: richness 17, 540 of 12000 left | none | 2026-11-17 10:50 UTC | `get_poi`, own ship |
| `westmark_frozen_drift` | Westmark Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 54, 37912 of 50000 left; nitrogen_ice: richness 48, 50000 of 50000 left; helium_ice: richness 14, 4530 of 5000 left | none | 2026-11-17 10:50 UTC | `get_poi`, own ship |

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
| 2026-11-17 10:50 UTC | own ship | Read Westmark Belt: 68,427 units left in all | `get_poi`, own ship |
| 2026-11-17 10:50 UTC | own ship | Read Westmark Frozen Drift: 92,442 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
