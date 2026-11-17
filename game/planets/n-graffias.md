---
name: graffias
id: 20261117T163932Z
tier: intel
author: Unity
kind: system
system_id: graffias
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Graffias

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where graffias`).

| Field | Value |
|---|---|
| Position | x 3716.6, y -3638.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | barnard_77, farpoint, tianyi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `graffias_star` | Graffias Star | sun (M6V) | -- | -- | none | 2026-11-17 16:18 UTC | `get_system`, own ship |
| `graffias_i` | Graffias I | planet (scorched) | -- | -- | none | 2026-11-17 16:18 UTC | `get_system`, own ship |
| `graffias_ii` | Graffias II | planet (arid) | -- | -- | none | 2026-11-17 16:18 UTC | `get_system`, own ship |
| `graffias_iii` | Graffias III | planet (terran) | -- | -- | none | 2026-11-17 16:18 UTC | `get_system`, own ship |
| `graffias_ice_belt` | Graffias Ice Belt | ice_field (kuiper) | -- | water_ice: richness 41, 333 of 50000 left; deuterium_ice: richness 17, 305 of 5000 left; oxygen_ice: richness 9, 400 of 2500 left | none | 2026-11-17 16:18 UTC | `get_poi`, own ship |
| `unweighed_crystal` | Unweighed Crystal | asteroid_belt | -- | iron_ore: richness 37, 99999 of 100000 left; copper_ore: richness 24, 100000 of 100000 left; trade_crystal: richness 24, 81 of 3000 left | none | 2026-11-17 16:18 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:18 UTC | own ship | Read Graffias Ice Belt: 1,038 units left in all | `get_poi`, own ship |
| 2026-11-17 16:18 UTC | own ship | Read Unweighed Crystal: 200,080 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
