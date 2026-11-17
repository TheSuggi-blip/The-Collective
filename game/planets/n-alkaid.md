---
name: alkaid
id: 20261117T174221Z
tier: intel
author: Unity
kind: system
system_id: alkaid
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alkaid

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alkaid`).

| Field | Value |
|---|---|
| Position | x 1784.7, y -2740.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | capella, gsc_0030, gsc_0051, tau_bootis, xihe |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alkaid_star` | Alkaid Star | sun (M6V) | -- | -- | none | 2026-11-17 17:35 UTC | `get_system`, own ship |
| `alkaid_i` | Alkaid I | planet (scorched) | -- | -- | none | 2026-11-17 17:35 UTC | `get_system`, own ship |
| `alkaid_gas_pocket` | Alkaid Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 68, 178 of 50000 left; argon_gas: richness 35, 37554 of 50000 left; plasma_gas: richness 23, 364 of 10000 left; neon_gas: richness 37, 41014 of 50000 left; chlorine_gas: richness 58, 113 of 10000 left | none | 2026-11-17 17:35 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:35 UTC | own ship | Read Alkaid Gas Pocket: 79,223 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
