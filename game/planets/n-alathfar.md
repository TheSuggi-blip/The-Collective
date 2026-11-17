---
name: alathfar
id: 20261117T102821Z
tier: intel
author: Unity
kind: system
system_id: alathfar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alathfar

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alathfar`).

| Field | Value |
|---|---|
| Position | x -3755.3, y -1507.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | hollowcrest, izar, merak, sabik, sheliak, titawin |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alathfar_star` | Alathfar Star | sun (K6V) | -- | -- | none | 2026-11-17 09:51 UTC | `get_system`, own ship |
| `alathfar_belt` | Alathfar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 36, 99999 of 100000 left; copper_ore: richness 29, 100000 of 100000 left; aluminum_ore: richness 52, 103 of 30000 left | none | 2026-11-17 09:51 UTC | `get_poi`, own ship |
| `alathfar_haze` | Alathfar Haze | gas_cloud (molecular_cloud) | -- | argon_gas: richness 45, 49999 of 50000 left; xenon_gas: richness 27, 10000 of 10000 left; nebula_gas: richness 22, 10000 of 10000 left; neon_gas: richness 51, 50000 of 50000 left; chlorine_gas: richness 26, 10000 of 10000 left | none | 2026-11-17 09:51 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:51 UTC | own ship | Read Alathfar Belt: 200,102 units left in all | `get_poi`, own ship |
| 2026-11-17 09:51 UTC | own ship | Read Alathfar Haze: 129,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
