---
name: gemma
id: 20261117T082530Z
tier: intel
author: Unity
kind: system
system_id: gemma
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Gemma

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gemma`).

| Field | Value |
|---|---|
| Position | x -325.2, y 1916.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | adhafera, deepwell, goldcrest, gsc_0022 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `gemma_star` | Gemma Star | sun (M2V) | -- | -- | none | 2026-11-17 07:44 UTC | `get_system`, own ship |
| `gemma_belt` | Gemma Belt | asteroid_belt (metallic) | -- | iron_ore: richness 41, 4185 of 100000 left; copper_ore: richness 39, 4185 of 100000 left; manganese_ore: richness 21, 526 of 15000 left | none | 2026-11-17 07:44 UTC | `get_poi`, own ship |
| `gemma_haze` | Gemma Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 45, 3278 of 50000 left; argon_gas: richness 38, 46359 of 50000 left; xenon_gas: richness 15, 10000 of 10000 left | none | 2026-11-17 07:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 07:44 UTC | own ship | Read Gemma Belt: 8,896 units left in all | `get_poi`, own ship |
| 2026-11-17 07:44 UTC | own ship | Read Gemma Haze: 59,637 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
