---
name: dawnbreak
id: 20261117T163930Z
tier: intel
author: Unity
kind: system
system_id: dawnbreak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Dawnbreak

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where dawnbreak`).

| Field | Value |
|---|---|
| Position | x 3719.6, y 4140.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | albireo, fumalsamakah, kornephoros, the_rampart |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dawnbreak_star` | Dawnbreak Star | sun (K2V) | -- | -- | none | 2026-11-17 15:38 UTC | `get_system`, own ship |
| `dawnbreak_i` | Dawnbreak I | planet (scorched) | -- | -- | none | 2026-11-17 15:38 UTC | `get_system`, own ship |
| `dawnbreak_frozen_drift` | Dawnbreak Frozen Drift | ice_field (cometary) | -- | water_ice: richness 46, 47287 of 50000 left; nitrogen_ice: richness 51, 50000 of 50000 left; helium_ice: richness 10, 5000 of 5000 left | none | 2026-11-17 15:38 UTC | `get_poi`, own ship |
| `dawnbreak_ash_pocket` | Dawnbreak Ash Pocket | asteroid_belt | -- | iron_ore: richness 30, 10543 of 100000 left; copper_ore: richness 35, 91875 of 100000 left; plasma_residue: richness 8, 580 of 762 left | none | 2026-11-17 15:38 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:38 UTC | own ship | Read Dawnbreak Frozen Drift: 102,287 units left in all | `get_poi`, own ship |
| 2026-11-17 15:38 UTC | own ship | Read Dawnbreak Ash Pocket: 102,998 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
