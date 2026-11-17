---
name: thornfield
id: 20261117T153756Z
tier: intel
author: Unity
kind: system
system_id: thornfield
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Thornfield

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where thornfield`).

| Field | Value |
|---|---|
| Position | x 1303.6, y -6554.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | alioth, almach, gsc_0025, helvetios |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `thornfield_star` | Thornfield Star | sun (M2V) | -- | -- | none | 2026-11-17 14:36 UTC | `get_system`, own ship |
| `thornfield_i` | Thornfield I | planet (scorched) | -- | -- | none | 2026-11-17 14:36 UTC | `get_system`, own ship |
| `thornfield_belt` | Thornfield Belt | asteroid_belt (metallic) | -- | iron_ore: richness 40, 99999 of 100000 left; copper_ore: richness 26, 100000 of 100000 left; lithium_ore: richness 43, 692 of 25000 left | none | 2026-11-17 14:36 UTC | `get_poi`, own ship |
| `thornfield_vapor_fields` | Thornfield Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 42, 1498 of 50000 left; argon_gas: richness 38, 1678 of 50000 left; plasma_gas: richness 31, 484 of 10000 left; xenon_gas: richness 27, 522 of 10000 left; nebula_gas: richness 25, 479 of 10000 left; neon_gas: richness 49, 1418 of 50000 left; chlorine_gas: richness 23, 532 of 10000 left; ion_gas: richness 21, 628 of 10000 left | none | 2026-11-17 14:36 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:36 UTC | own ship | Read Thornfield Belt: 200,691 units left in all | `get_poi`, own ship |
| 2026-11-17 14:36 UTC | own ship | Read Thornfield Vapor Fields: 7,239 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
