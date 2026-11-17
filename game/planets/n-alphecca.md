---
name: alphecca
id: 20261117T123126Z
tier: intel
author: Unity
kind: system
system_id: alphecca
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alphecca

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alphecca`).

| Field | Value |
|---|---|
| Position | x 2238.8, y 2193.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | ankaa, barnardstar, scheat |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alphecca_star` | Alphecca Star | sun (M4V) | -- | -- | none | 2026-11-17 11:51 UTC | `get_system`, own ship |
| `alphecca_i` | Alphecca I | planet (scorched) | -- | -- | none | 2026-11-17 11:51 UTC | `get_system`, own ship |
| `alphecca_ii` | Alphecca II | planet (arid) | -- | -- | none | 2026-11-17 11:51 UTC | `get_system`, own ship |
| `alphecca_iii` | Alphecca III | planet (terran) | -- | -- | none | 2026-11-17 11:51 UTC | `get_system`, own ship |
| `alphecca_vapor_fields` | Alphecca Vapor Fields | gas_cloud (molecular_cloud) | -- | argon_gas: richness 52, 47210 of 50000 left; plasma_gas: richness 27, 8510 of 10000 left; xenon_gas: richness 27, 8342 of 10000 left; neon_gas: richness 51, 47968 of 50000 left | none | 2026-11-17 11:51 UTC | `get_poi`, own ship |
| `overlooked_vein` | Overlooked Vein | asteroid_belt | -- | iron_ore: richness 39, 76575 of 100000 left; copper_ore: richness 27, 100000 of 100000 left; titanium_ore: richness 34, 24 of 25000 left; chromium_ore: richness 17, 72 of 8000 left | none | 2026-11-17 11:51 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:51 UTC | own ship | Read Alphecca Vapor Fields: 112,030 units left in all | `get_poi`, own ship |
| 2026-11-17 11:51 UTC | own ship | Read Overlooked Vein: 176,671 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
