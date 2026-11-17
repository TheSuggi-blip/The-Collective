---
name: yarrowfield
id: 20261117T143558Z
tier: intel
author: Unity
kind: system
system_id: yarrowfield
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Yarrowfield

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where yarrowfield`).

| Field | Value |
|---|---|
| Position | x -156.9, y -7257.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | alcor, algiedi, asterope, hd_85512, menkalinan, sadalbari, unukalhai |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `yarrowfield_star` | Yarrowfield Star | sun (M2V) | -- | -- | none | 2026-11-17 13:35 UTC | `get_system`, own ship |
| `yarrowfield_i` | Yarrowfield I | planet (scorched) | -- | -- | none | 2026-11-17 13:35 UTC | `get_system`, own ship |
| `yarrowfield_ii` | Yarrowfield II | planet (arid) | -- | -- | none | 2026-11-17 13:35 UTC | `get_system`, own ship |
| `yarrowfield_iii` | Yarrowfield III | planet (terran) | -- | -- | none | 2026-11-17 13:35 UTC | `get_system`, own ship |
| `yarrowfield_belt` | Yarrowfield Belt | asteroid_belt (metallic) | -- | iron_ore: richness 45, 100000 of 100000 left; copper_ore: richness 41, 100000 of 100000 left | none | 2026-11-17 13:35 UTC | `get_poi`, own ship |
| `yarrowfield_vapor_fields` | Yarrowfield Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 58, 1014 of 50000 left; argon_gas: richness 48, 1019 of 50000 left; neon_gas: richness 39, 1015 of 50000 left; chlorine_gas: richness 37, 438 of 10000 left; ion_gas: richness 24, 442 of 10000 left | none | 2026-11-17 13:35 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:35 UTC | own ship | Read Yarrowfield Belt: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 13:35 UTC | own ship | Read Yarrowfield Vapor Fields: 3,928 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
