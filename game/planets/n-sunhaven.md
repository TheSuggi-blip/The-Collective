---
name: sunhaven
id: 20261117T133406Z
tier: intel
author: Unity
kind: system
system_id: sunhaven
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sunhaven

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sunhaven`).

| Field | Value |
|---|---|
| Position | x 4488.5, y 565.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | 61_cygni, alsephina, atik, minkar, mothallah, sargas |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sunhaven_star` | Sunhaven Star | sun (K2V) | -- | -- | none | 2026-11-17 13:16 UTC | `get_system`, own ship |
| `sunhaven_i` | Sunhaven I | planet (scorched) | -- | -- | none | 2026-11-17 13:16 UTC | `get_system`, own ship |
| `sunhaven_ii` | Sunhaven II | planet (arid) | -- | -- | none | 2026-11-17 13:16 UTC | `get_system`, own ship |
| `sunhaven_haze` | Sunhaven Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 62, 11130 of 50000 left; neon_gas: richness 39, 50000 of 50000 left; chlorine_gas: richness 27, 4786 of 10000 left; krypton_gas: richness 25, 1895 of 5000 left | none | 2026-11-17 13:16 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:16 UTC | own ship | Read Sunhaven Haze: 67,811 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
