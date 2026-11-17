---
name: peacock
id: 20261117T194618Z
tier: intel
author: Unity
kind: system
system_id: peacock
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Peacock

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where peacock`).

| Field | Value |
|---|---|
| Position | x 237.4, y -2427.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | alfirk, gsc_0009, pinewatch, revati |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `peacock_star` | Peacock Star | sun (B2IV) | -- | -- | none | 2026-11-17 19:11 UTC | `get_system`, own ship |
| `peacock_emission_cloud` | Peacock Emission Cloud | gas_cloud (emission) | -- | plasma_gas: richness 50, 582 of 22000 left; nebula_gas: richness 35, 587 of 18000 left; ion_gas: richness 20, 443 of 10000 left | none | 2026-11-17 19:11 UTC | `get_poi`, own ship |
| `peacock_poi_0` | Peacock | sun | -- | -- | none | 2026-11-17 19:11 UTC | `get_system`, own ship |
| `sys_0311_poi_0` | Peacock | sun | -- | -- | none | 2026-11-17 19:11 UTC | `get_system`, own ship |

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
| 2026-11-17 19:11 UTC | own ship | Read Peacock Emission Cloud: 1,612 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
