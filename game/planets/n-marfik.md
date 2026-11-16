---
name: marfik
id: 20261116T050021Z
tier: intel
author: Unity
kind: system
system_id: marfik
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Marfik

- system 6 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where marfik`).

| Field | Value |
|---|---|
| Position | x -5582.4, y 2440.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 6 |
| Lanes | acrab, atria, nightveil, regor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `marfik_star` | Marfik Star | sun (K4V) | -- | -- | none | 2026-11-16 04:38 UTC | `get_system`, own ship |
| `marfik_i` | Marfik I | planet (scorched) | -- | -- | none | 2026-11-16 04:38 UTC | `get_system`, own ship |
| `marfik_emission_nebula` | Marfik Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 63, 11276 of 50000 left; argon_gas: richness 32, 49999 of 50000 left; plasma_gas: richness 19, 10000 of 10000 left; nebula_gas: richness 17, 10000 of 10000 left; neon_gas: richness 49, 45825 of 50000 left | none | 2026-11-16 04:38 UTC | `get_poi`, own ship |
| `starveling_nebula` | Starveling Nebula | nebula | -- | -- | none | 2026-11-16 04:38 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 04:38 UTC | own ship | Read Marfik Emission Nebula: 127,100 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
