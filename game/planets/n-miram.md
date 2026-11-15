---
name: miram
id: 20261115T225423Z
tier: intel
author: Unity
kind: system
system_id: miram
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Miram

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where miram`).

| Field | Value |
|---|---|
| Position | x -5167.4, y 3463.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | brachium, denebola, gsc_0038, gsc_0050 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `miram_star` | Miram Star | sun (K6V) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `miram_i` | Miram I | planet (scorched) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `miram_ii` | Miram II | planet (arid) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `miram_iii` | Miram III | planet (terran) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `miram_haze` | Miram Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 59, 10155 of 50000 left; nebula_gas: richness 15, 10000 of 10000 left; ion_gas: richness 30, 3024 of 10000 left | none | 2026-11-15 22:03 UTC | `get_poi`, own ship |

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
| 2026-11-15 22:03 UTC | own ship | Read Miram Haze: 23,179 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
