---
name: thuban
id: 20261117T184359Z
tier: intel
author: Unity
kind: system
system_id: thuban
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Thuban

- system 16 jumps from home, police level 0. Station: Ghost Runner Terminal.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where thuban`).

| Field | Value |
|---|---|
| Position | x 3202.8, y 5060.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | arneb, crosshaven, diphda, gsc_0019, kornephoros |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `thuban_star` | Thuban Star | sun (M2V) | -- | -- | none | 2026-11-17 17:55 UTC | `get_system`, own ship |
| `thuban_i` | Thuban I | planet (scorched) | -- | -- | none | 2026-11-17 17:55 UTC | `get_system`, own ship |
| `thuban_ii` | Thuban II | planet (arid) | -- | -- | none | 2026-11-17 17:55 UTC | `get_system`, own ship |
| `thuban_iii` | Thuban III | planet (terran) | -- | -- | none | 2026-11-17 17:55 UTC | `get_system`, own ship |
| `thuban_belt` | Thuban Belt | asteroid_belt (metallic) | -- | iron_ore: richness 46, 7128 of 100000 left; copper_ore: richness 38, 44454 of 100000 left | none | 2026-11-17 17:55 UTC | `get_poi`, own ship |
| `thuban_ice_shelf` | Thuban Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 48, 49670 of 50000 left; nitrogen_ice: richness 35, 50000 of 50000 left | none | 2026-11-17 17:55 UTC | `get_poi`, own ship |
| `thimble_field` | Thimble Field | asteroid_belt | -- | iron_ore: richness 34, 5353 of 100000 left; copper_ore: richness 34, 11734 of 100000 left; plasma_residue: richness 9, 725 of 997 left | none | 2026-11-17 17:55 UTC | `get_poi`, own ship |
| `6b710aa99f58aec15b0280ee71690ba4` | Ghost Runner Terminal | station | `002844965843233bd15f5e8b23802650` | -- | none | 2026-11-17 17:55 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Ghost Runner Terminal (`002844965843233bd15f5e8b23802650`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:55 UTC | `get_system`, own ship |

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
| 2026-11-17 17:55 UTC | own ship | Read Thuban Belt: 51,582 units left in all | `get_poi`, own ship |
| 2026-11-17 17:55 UTC | own ship | Read Thuban Ice Shelf: 99,670 units left in all | `get_poi`, own ship |
| 2026-11-17 17:55 UTC | own ship | Read Thimble Field: 17,812 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
