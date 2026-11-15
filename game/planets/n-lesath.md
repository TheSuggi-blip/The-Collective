---
name: lesath
id: 20261115T225422Z
tier: intel
author: Unity
kind: system
system_id: lesath
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Lesath

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where lesath`).

| Field | Value |
|---|---|
| Position | x -4939.0, y 4055.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | amberfall, gj_3470, gsc_0038, megrez |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `lesath_star` | Lesath Star | sun (M2V) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `lesath_i` | Lesath I | planet (scorched) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `lesath_ii` | Lesath II | planet (arid) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `lesath_gas_cloud` | Lesath Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 67, 10803 of 50000 left; plasma_gas: richness 25, 8411 of 10000 left; xenon_gas: richness 19, 9419 of 10000 left; neon_gas: richness 35, 49601 of 50000 left; ion_gas: richness 23, 9516 of 10000 left | none | 2026-11-15 22:03 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 22:03 UTC | own ship | Read Lesath Gas Cloud: 87,750 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
