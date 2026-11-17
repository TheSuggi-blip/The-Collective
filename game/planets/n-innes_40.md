---
name: innes_40
id: 20261117T010828Z
tier: intel
author: Unity
kind: system
system_id: innes_40
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Innes 40

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where innes_40`).

| Field | Value |
|---|---|
| Position | x -4608.2, y 1205.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | chalawan, clearwater, groombridge_34, relay_station, rotanev, the_archive |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `innes_40_star` | Innes 40 Star | sun (G5V) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `innes_40_i` | Innes 40 I | planet (scorched) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `innes_40_ii` | Innes 40 II | planet (arid) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `innes_40_iii` | Innes 40 III | planet (terran) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `innes_40_iv` | Innes 40 IV | planet (jovian) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `innes_40_gas_pocket` | Innes 40 Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 60, 6892 of 50000 left; argon_gas: richness 32, 50000 of 50000 left; neon_gas: richness 51, 50000 of 50000 left; chlorine_gas: richness 23, 2123 of 10000 left | none | 2026-11-17 00:44 UTC | `get_poi`, own ship |
| `orphan_nebula` | Orphan Nebula | nebula | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |

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
| 2026-11-17 00:44 UTC | own ship | Read Innes 40 Gas Pocket: 109,015 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
