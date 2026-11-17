---
name: khambalia
id: 20261117T133347Z
tier: intel
author: Unity
kind: system
system_id: khambalia
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 55
updated: 2026-11-17
---

# Khambalia

Nebula system 22 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where khambalia`).

| Field | Value |
|---|---|
| Position | x 1651.4, y -5368.7 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 22 |
| Lanes | azmidi, factory_belt, gliese_436, pollux, traders_rest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `khambalia_star` | Khambalia Star | sun (A1V) | -- | -- | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `khambalia_i` | Khambalia I | planet (scorched) | -- | -- | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `khambalia_ii` | Khambalia II | planet (arid) | -- | -- | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `khambalia_iii` | Khambalia III | planet (tundra) | -- | -- | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `khambalia_belt` | Khambalia Belt | asteroid_belt (mixed) | -- | not read | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `khambalia_ice_fields` | Khambalia Ice Fields | ice_field (kuiper) | -- | not read | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `khambalia_crystal_market` | Khambalia Crystal Market | asteroid_belt | -- | iron_ore: richness 36, 21812 of 100000 left; copper_ore: richness 35, 23213 of 100000 left; trade_crystal: richness 30, 0 of 4000 left | none | 2026-11-17 12:41 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 12:41 UTC | own ship | Read Khambalia Crystal Market: 45,025 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `khambalia_belt`, `khambalia_ice_fields`.
