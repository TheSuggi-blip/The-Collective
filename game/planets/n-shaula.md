---
name: shaula
id: 20261115T215329Z
tier: intel
author: Unity
kind: system
system_id: shaula
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Shaula

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where shaula`).

| Field | Value |
|---|---|
| Position | x -2213.7, y 2858.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | alnair, gsc_0041, pherkad, wolf_1061 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `shaula_star` | Shaula Star | sun (M2V) | -- | -- | none | 2026-11-15 21:48 UTC | `get_system`, own ship |
| `shaula_i` | Shaula I | planet (scorched) | -- | -- | none | 2026-11-15 21:48 UTC | `get_system`, own ship |
| `shaula_ii` | Shaula II | planet (arid) | -- | -- | none | 2026-11-15 21:48 UTC | `get_system`, own ship |
| `shaula_gas_plume` | Shaula Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 48, 534 of 50000 left; argon_gas: richness 30, 48839 of 50000 left; neon_gas: richness 46, 44304 of 50000 left; krypton_gas: richness 50, 561 of 5000 left | none | 2026-11-15 21:48 UTC | `get_poi`, own ship |

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
| 2026-11-15 21:48 UTC | own ship | Read Shaula Gas Plume: 94,238 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
