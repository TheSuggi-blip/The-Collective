---
name: tonatiuh
id: 20261117T163952Z
tier: intel
author: Unity
kind: system
system_id: tonatiuh
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tonatiuh

- system 26 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tonatiuh`).

| Field | Value |
|---|---|
| Position | x 4148.5, y -5562.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 26 |
| Lanes | 55_cancri, gsc_0029 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tonatiuh_star` | Tonatiuh Star | sun (M4V) | -- | -- | none | 2026-11-17 16:05 UTC | `get_system`, own ship |
| `tonatiuh_i` | Tonatiuh I | planet (scorched) | -- | -- | none | 2026-11-17 16:05 UTC | `get_system`, own ship |
| `tonatiuh_ii` | Tonatiuh II | planet (arid) | -- | -- | none | 2026-11-17 16:05 UTC | `get_system`, own ship |
| `tonatiuh_iii` | Tonatiuh III | planet (terran) | -- | -- | none | 2026-11-17 16:05 UTC | `get_system`, own ship |
| `tonatiuh_iv` | Tonatiuh IV | planet (tundra) | -- | -- | none | 2026-11-17 16:05 UTC | `get_system`, own ship |
| `tonatiuh_ice_belt` | Tonatiuh Ice Belt | ice_field (kuiper) | -- | nitrogen_ice: richness 44, 404 of 50000 left; deuterium_ice: richness 23, 484 of 5000 left; helium_ice: richness 18, 563 of 5000 left | none | 2026-11-17 16:05 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:05 UTC | own ship | Read Tonatiuh Ice Belt: 1,451 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
