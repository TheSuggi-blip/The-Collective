---
name: saclateni
id: 20261117T163948Z
tier: intel
author: Unity
kind: system
system_id: saclateni
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Saclateni

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where saclateni`).

| Field | Value |
|---|---|
| Position | x 3627.3, y 3553.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | albireo, fumalsamakah, gsc_0013, ross_614, the_rampart |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `saclateni_star` | Saclateni Star | sun (M6V) | -- | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |
| `saclateni_ice_shelf` | Saclateni Ice Shelf | ice_field (kuiper) | -- | nitrogen_ice: richness 52, 50000 of 50000 left; helium_ice: richness 18, 5000 of 5000 left | none | 2026-11-17 15:43 UTC | `get_poi`, own ship |
| `shadowfleck_veins` | Shadowfleck Veins | asteroid_belt | -- | iron_ore: richness 29, 5136 of 100000 left; copper_ore: richness 28, 5133 of 100000 left; darksteel_ore: richness 5, 320 of 320 left | none | 2026-11-17 15:43 UTC | `get_poi`, own ship |
| `saclateni_fading_ember` | Saclateni Fading Ember | asteroid_belt | -- | iron_ore: richness 44, 217 of 100000 left; copper_ore: richness 28, 219 of 100000 left; plasma_residue: richness 10, 201 of 970 left | none | 2026-11-17 15:43 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:43 UTC | own ship | Read Saclateni Ice Shelf: 55,000 units left in all | `get_poi`, own ship |
| 2026-11-17 15:43 UTC | own ship | Read Shadowfleck Veins: 10,589 units left in all | `get_poi`, own ship |
| 2026-11-17 15:43 UTC | own ship | Read Saclateni Fading Ember: 637 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
