---
name: alsciaukat
id: 20261117T112921Z
tier: intel
author: Unity
kind: system
system_id: alsciaukat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alsciaukat

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alsciaukat`).

| Field | Value |
|---|---|
| Position | x -4406.2, y -1636.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | errai, merak, merope, sheliak |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alsciaukat_star` | Alsciaukat Star | sun (M6V) | -- | -- | none | 2026-11-17 10:55 UTC | `get_system`, own ship |
| `alsciaukat_i` | Alsciaukat I | planet (scorched) | -- | -- | none | 2026-11-17 10:55 UTC | `get_system`, own ship |
| `alsciaukat_ii` | Alsciaukat II | planet (arid) | -- | -- | none | 2026-11-17 10:55 UTC | `get_system`, own ship |
| `alsciaukat_vapor_fields` | Alsciaukat Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 57, 8513 of 50000 left; argon_gas: richness 39, 49089 of 50000 left; plasma_gas: richness 18, 9546 of 10000 left; xenon_gas: richness 25, 2286 of 10000 left; nebula_gas: richness 22, 4916 of 10000 left; neon_gas: richness 48, 26380 of 50000 left; chlorine_gas: richness 26, 2637 of 10000 left | none | 2026-11-17 10:55 UTC | `get_poi`, own ship |
| `alsciaukat_ghost_resonance` | Alsciaukat Ghost Resonance | nebula | -- | -- | none | 2026-11-17 10:55 UTC | `get_system`, own ship |
| `alsciaukat_faint_entanglement` | Alsciaukat Faint Entanglement | nebula | -- | -- | none | 2026-11-17 10:55 UTC | `get_system`, own ship |

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
| 2026-11-17 10:55 UTC | own ship | Read Alsciaukat Vapor Fields: 103,367 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
