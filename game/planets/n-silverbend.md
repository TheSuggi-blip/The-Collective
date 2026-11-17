---
name: silverbend
id: 20261117T092738Z
tier: intel
author: Unity
kind: system
system_id: silverbend
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Silverbend

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where silverbend`).

| Field | Value |
|---|---|
| Position | x -476.6, y 5017.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | alderamin, alnilam, groombridge_1618 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `silverbend_star` | Silverbend Star | sun (G8V) | -- | -- | none | 2026-11-17 08:57 UTC | `get_system`, own ship |
| `silverbend_i` | Silverbend I | planet (scorched) | -- | -- | none | 2026-11-17 08:57 UTC | `get_system`, own ship |
| `silverbend_ii` | Silverbend II | planet (arid) | -- | -- | none | 2026-11-17 08:57 UTC | `get_system`, own ship |
| `silverbend_emission_nebula` | Silverbend Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 57, 2472 of 50000 left; argon_gas: richness 44, 48313 of 50000 left; plasma_gas: richness 23, 8708 of 10000 left; neon_gas: richness 40, 49998 of 50000 left; chlorine_gas: richness 35, 929 of 10000 left; krypton_gas: richness 24, 1181 of 5000 left | none | 2026-11-17 08:57 UTC | `get_poi`, own ship |
| `silverbend_exhausted_lode` | Silverbend Exhausted Lode | asteroid_belt (metallic) | -- | silver_ore: richness 6, 67 of 25000 left; copper_ore: richness 30, 14381 of 100000 left | none | 2026-11-17 08:57 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:57 UTC | own ship | Read Silverbend Emission Nebula: 111,601 units left in all | `get_poi`, own ship |
| 2026-11-17 08:57 UTC | own ship | Read Silverbend Exhausted Lode: 14,448 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
