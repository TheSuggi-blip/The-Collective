---
name: oakridge
id: 20261117T102833Z
tier: intel
author: Unity
kind: system
system_id: oakridge
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Oakridge

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where oakridge`).

| Field | Value |
|---|---|
| Position | x -2237.2, y -1722.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | aldhibah, gienah, hatysa |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `oakridge_star` | Oakridge Star | sun (M2V) | -- | -- | none | 2026-11-17 09:38 UTC | `get_system`, own ship |
| `oakridge_i` | Oakridge I | planet (scorched) | -- | -- | none | 2026-11-17 09:38 UTC | `get_system`, own ship |
| `oakridge_ii` | Oakridge II | planet (arid) | -- | -- | none | 2026-11-17 09:38 UTC | `get_system`, own ship |
| `oakridge_iii` | Oakridge III | planet (terran) | -- | -- | none | 2026-11-17 09:38 UTC | `get_system`, own ship |
| `oakridge_iv` | Oakridge IV | planet (tundra) | -- | -- | none | 2026-11-17 09:38 UTC | `get_system`, own ship |
| `oakridge_belt` | Oakridge Belt | asteroid_belt (metallic) | -- | iron_ore: richness 48, 51067 of 100000 left; copper_ore: richness 34, 99999 of 100000 left; zinc_ore: richness 20, 14827 of 17000 left | none | 2026-11-17 09:38 UTC | `get_poi`, own ship |
| `broadwing_veil` | Broadwing Veil | nebula | -- | -- | none | 2026-11-17 09:38 UTC | `get_system`, own ship |
| `coinflip_nebula` | Coinflip Nebula | nebula | -- | -- | none | 2026-11-17 09:38 UTC | `get_system`, own ship |

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
| 2026-11-17 09:38 UTC | own ship | Read Oakridge Belt: 165,893 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
