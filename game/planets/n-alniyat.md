---
name: alniyat
id: 20261117T123125Z
tier: intel
author: Unity
kind: system
system_id: alniyat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alniyat

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alniyat`).

| Field | Value |
|---|---|
| Position | x 1106.2, y -7296.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | embervale, gsc_0025, mirzam |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alniyat_star` | Alniyat Star | sun (B2III) | -- | -- | none | 2026-11-17 12:25 UTC | `get_system`, own ship |
| `alniyat_plasma_shroud` | Alniyat Plasma Shroud | gas_cloud (emission) | -- | plasma_gas: richness 60, 384 of 25000 left; ion_gas: richness 40, 386 of 18000 left; nebula_gas: richness 25, 344 of 12000 left | none | 2026-11-17 12:25 UTC | `get_poi`, own ship |
| `alniyat_debris_ring` | Alniyat Debris Ring | asteroid_belt (mixed) | -- | iron_ore: richness 30, 17959 of 20000 left; titanium_ore: richness 20, 2 of 10000 left | none | 2026-11-17 12:25 UTC | `get_poi`, own ship |
| `sys_0129_poi_0` | TOI Major | sun | -- | -- | none | 2026-11-17 12:25 UTC | `get_system`, own ship |
| `alniyat_poi_0` | Alniyat | sun | -- | -- | none | 2026-11-17 12:25 UTC | `get_system`, own ship |

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
| 2026-11-17 12:25 UTC | own ship | Read Alniyat Plasma Shroud: 1,114 units left in all | `get_poi`, own ship |
| 2026-11-17 12:25 UTC | own ship | Read Alniyat Debris Ring: 17,961 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
