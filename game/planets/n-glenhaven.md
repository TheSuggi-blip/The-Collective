---
name: glenhaven
id: 20261117T123140Z
tier: intel
author: Unity
kind: system
system_id: glenhaven
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Glenhaven

- system 26 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where glenhaven`).

| Field | Value |
|---|---|
| Position | x 2429.1, y -6783.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 26 |
| Lanes | alhena, enif, naos, sadachbia |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `glenhaven_star` | Glenhaven Star | sun (G2V) | -- | -- | none | 2026-11-17 12:24 UTC | `get_system`, own ship |
| `glenhaven_i` | Glenhaven I | planet (scorched) | -- | -- | none | 2026-11-17 12:24 UTC | `get_system`, own ship |
| `glenhaven_ii` | Glenhaven II | planet (arid) | -- | -- | none | 2026-11-17 12:24 UTC | `get_system`, own ship |
| `glenhaven_iii` | Glenhaven III | planet (terran) | -- | -- | none | 2026-11-17 12:24 UTC | `get_system`, own ship |
| `glenhaven_gas_cloud` | Glenhaven Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 40, 44046 of 50000 left; argon_gas: richness 54, 14368 of 50000 left; plasma_gas: richness 19, 8581 of 10000 left; xenon_gas: richness 28, 2414 of 10000 left; neon_gas: richness 54, 16192 of 50000 left; chlorine_gas: richness 23, 4606 of 10000 left; ion_gas: richness 25, 1833 of 10000 left | none | 2026-11-17 12:24 UTC | `get_poi`, own ship |
| `glenhaven_ice_belt` | Glenhaven Ice Belt | ice_field (cometary) | -- | water_ice: richness 67, 44808 of 50000 left; nitrogen_ice: richness 38, 50000 of 50000 left | none | 2026-11-17 12:24 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:24 UTC | own ship | Read Glenhaven Gas Cloud: 92,040 units left in all | `get_poi`, own ship |
| 2026-11-17 12:24 UTC | own ship | Read Glenhaven Ice Belt: 94,808 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
