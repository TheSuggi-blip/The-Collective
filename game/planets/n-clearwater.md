---
name: clearwater
id: 20261117T082527Z
tier: intel
author: Unity
kind: system
system_id: clearwater
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Clearwater

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where clearwater`).

| Field | Value |
|---|---|
| Position | x -4465.7, y 694.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | innes_40, mizar, relay_station, rotanev, the_archive |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `clearwater_star` | Clearwater Star | sun (M4V) | -- | -- | none | 2026-11-17 08:15 UTC | `get_system`, own ship |
| `clearwater_vapor` | Clearwater Vapor | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 35, 8545 of 20000 left; argon_gas: richness 25, 15000 of 15000 left | none | 2026-11-17 08:15 UTC | `get_poi`, own ship |
| `glasslight_shoal` | Glasslight Shoal | asteroid_belt | -- | silicon_ore: richness 40, 322 of 20000 left | none | 2026-11-17 08:15 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:15 UTC | own ship | Read Clearwater Vapor: 23,545 units left in all | `get_poi`, own ship |
| 2026-11-17 08:15 UTC | own ship | Read Glasslight Shoal: 322 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
