---
name: gliese_229
id: 20261117T194621Z
tier: intel
author: Unity
kind: system
system_id: gliese_229
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Gliese 229

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gliese_229`).

| Field | Value |
|---|---|
| Position | x 3120.3, y -420.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | alnitak, breckenridge, ravenspire, whitecliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `gliese_229_star` | Gliese 229 Star | sun (G2V) | -- | -- | none | 2026-11-17 18:55 UTC | `get_system`, own ship |
| `gliese_229_haze` | Gliese 229 Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 55, 14218 of 50000 left; argon_gas: richness 48, 32248 of 50000 left; plasma_gas: richness 27, 3417 of 10000 left; xenon_gas: richness 19, 4447 of 10000 left; neon_gas: richness 42, 31340 of 50000 left; krypton_gas: richness 22, 3901 of 5000 left | none | 2026-11-17 18:55 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:55 UTC | own ship | Read Gliese 229 Haze: 89,571 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
