---
name: tania
id: 20261117T021128Z
tier: intel
author: Unity
kind: system
system_id: tania
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tania

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tania`).

| Field | Value |
|---|---|
| Position | x -4536.4, y -100.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | mizar, rasalhague, saltwind |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tania_star` | Tania Star | sun (M2V) | -- | -- | none | 2026-11-17 01:10 UTC | `get_system`, own ship |
| `tania_i` | Tania I | planet (scorched) | -- | -- | none | 2026-11-17 01:10 UTC | `get_system`, own ship |
| `tania_ii` | Tania II | planet (arid) | -- | -- | none | 2026-11-17 01:10 UTC | `get_system`, own ship |
| `tania_belt` | Tania Belt | asteroid_belt (metallic) | -- | iron_ore: richness 63, 99999 of 100000 left; copper_ore: richness 29, 100000 of 100000 left | none | 2026-11-17 01:10 UTC | `get_poi`, own ship |
| `tania_vapor_fields` | Tania Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 58, 7070 of 50000 left; argon_gas: richness 32, 50000 of 50000 left; plasma_gas: richness 15, 9689 of 10000 left; nebula_gas: richness 24, 4368 of 10000 left; chlorine_gas: richness 36, 1645 of 10000 left | none | 2026-11-17 01:10 UTC | `get_poi`, own ship |
| `tania_frozen_drift` | Tania Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 41, 32202 of 50000 left; nitrogen_ice: richness 42, 50000 of 50000 left | none | 2026-11-17 01:10 UTC | `get_poi`, own ship |

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
| 2026-11-17 01:10 UTC | own ship | Read Tania Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 01:10 UTC | own ship | Read Tania Vapor Fields: 72,772 units left in all | `get_poi`, own ship |
| 2026-11-17 01:10 UTC | own ship | Read Tania Frozen Drift: 82,202 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
