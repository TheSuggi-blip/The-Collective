---
name: amberfall
id: 20261115T225414Z
tier: intel
author: Unity
kind: system
system_id: amberfall
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Amberfall

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where amberfall`).

| Field | Value |
|---|---|
| Position | x -4663.1, y 4535.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | achird, lesath, megrez, thornhaven |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `amberfall_star` | Amberfall Star | sun (K4V) | -- | -- | none | 2026-11-15 21:59 UTC | `get_system`, own ship |
| `amberfall_i` | Amberfall I | planet (scorched) | -- | -- | none | 2026-11-15 21:59 UTC | `get_system`, own ship |
| `amberfall_belt` | Amberfall Belt | asteroid_belt (metallic) | -- | iron_ore: richness 61, 99997 of 100000 left; copper_ore: richness 49, 99999 of 100000 left | none | 2026-11-15 21:59 UTC | `get_poi`, own ship |
| `amberfall_emission_nebula` | Amberfall Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 58, 49999 of 50000 left; neon_gas: richness 37, 50000 of 50000 left; chlorine_gas: richness 35, 10000 of 10000 left | none | 2026-11-15 21:59 UTC | `get_poi`, own ship |

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
| 2026-11-15 21:59 UTC | own ship | Read Amberfall Belt: 199,996 units left in all | `get_poi`, own ship |
| 2026-11-15 21:59 UTC | own ship | Read Amberfall Emission Nebula: 109,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
