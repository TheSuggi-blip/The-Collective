---
name: ross_154
id: 20261117T123158Z
tier: intel
author: Unity
kind: system
system_id: ross_154
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ross 154

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ross_154`).

| Field | Value |
|---|---|
| Position | x -269.1, y -1637.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | arcturus, electra, maplevale, mimosa, timberline |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ross_154_star` | Ross 154 Star | sun (M6V) | -- | -- | none | 2026-11-17 11:31 UTC | `get_system`, own ship |
| `ross_154_i` | Ross 154 I | planet (scorched) | -- | -- | none | 2026-11-17 11:31 UTC | `get_system`, own ship |
| `ross_154_frost_ring` | Ross 154 Frost Ring | ice_field (kuiper) | -- | water_ice: richness 68, 12160 of 50000 left; nitrogen_ice: richness 34, 50000 of 50000 left | none | 2026-11-17 11:31 UTC | `get_poi`, own ship |
| `ross_154_weak_annihilation_zone` | Ross 154 Weak Annihilation Zone | asteroid_belt | -- | iron_ore: richness 37, 99999 of 100000 left; copper_ore: richness 32, 99999 of 100000 left; antimatter_containment_cell: richness 2, 154 of 154 left | none | 2026-11-17 11:31 UTC | `get_poi`, own ship |
| `frostdust_belt` | Frostdust Belt | asteroid_belt | -- | iron_ore: richness 42, 100000 of 100000 left; copper_ore: richness 26, 100000 of 100000 left; sol_alloy_ore: richness 5, 1299 of 1299 left | none | 2026-11-17 11:31 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:31 UTC | own ship | Read Ross 154 Frost Ring: 62,160 units left in all | `get_poi`, own ship |
| 2026-11-17 11:31 UTC | own ship | Read Ross 154 Weak Annihilation Zone: 200,152 units left in all | `get_poi`, own ship |
| 2026-11-17 11:31 UTC | own ship | Read Frostdust Belt: 201,299 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
