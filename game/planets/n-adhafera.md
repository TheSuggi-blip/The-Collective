---
name: adhafera
id: 20261117T082522Z
tier: intel
author: Unity
kind: system
system_id: adhafera
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Adhafera

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where adhafera`).

| Field | Value |
|---|---|
| Position | x 189.8, y 1635.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | gemma, gsc_0022, harborlight, kapteyn_5, markab, misthollow |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `adhafera_star` | Adhafera Star | sun (G8V) | -- | -- | none | 2026-11-17 07:46 UTC | `get_system`, own ship |
| `adhafera_i` | Adhafera I | planet (scorched) | -- | -- | none | 2026-11-17 07:46 UTC | `get_system`, own ship |
| `adhafera_ii` | Adhafera II | planet (arid) | -- | -- | none | 2026-11-17 07:46 UTC | `get_system`, own ship |
| `adhafera_iii` | Adhafera III | planet (terran) | -- | -- | none | 2026-11-17 07:46 UTC | `get_system`, own ship |
| `adhafera_vapor_fields` | Adhafera Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 45, 2491 of 50000 left; argon_gas: richness 54, 49999 of 50000 left; xenon_gas: richness 25, 10000 of 10000 left; nebula_gas: richness 23, 10000 of 10000 left; neon_gas: richness 42, 50000 of 50000 left; ion_gas: richness 24, 9789 of 10000 left | none | 2026-11-17 07:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 07:46 UTC | own ship | Read Adhafera Vapor Fields: 132,279 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
