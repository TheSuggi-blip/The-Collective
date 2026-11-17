---
name: scheat
id: 20261117T123202Z
tier: intel
author: Unity
kind: system
system_id: scheat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Scheat

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where scheat`).

| Field | Value |
|---|---|
| Position | x 2260.4, y 2651.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | alphecca, ivorygate, nashira |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `scheat_star` | Scheat Star | sun (M2V) | -- | -- | none | 2026-11-17 12:28 UTC | `get_system`, own ship |
| `scheat_haze` | Scheat Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 48, 2744 of 50000 left; argon_gas: richness 31, 48231 of 50000 left; plasma_gas: richness 23, 8002 of 10000 left; xenon_gas: richness 16, 9219 of 10000 left; nebula_gas: richness 14, 9529 of 10000 left; neon_gas: richness 36, 46548 of 50000 left | none | 2026-11-17 12:28 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:28 UTC | own ship | Read Scheat Haze: 124,273 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
