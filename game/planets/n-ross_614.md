---
name: ross_614
id: 20261117T163947Z
tier: intel
author: Unity
kind: system
system_id: ross_614
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ross 614

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ross_614`).

| Field | Value |
|---|---|
| Position | x 3341.4, y 3095.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | fumalsamakah, gsc_0013, rasalgethi, saclateni |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ross_614_star` | Ross 614 Star | sun (M4V) | -- | -- | none | 2026-11-17 15:46 UTC | `get_system`, own ship |
| `ross_614_i` | Ross 614 I | planet (scorched) | -- | -- | none | 2026-11-17 15:46 UTC | `get_system`, own ship |
| `ross_614_ii` | Ross 614 II | planet (arid) | -- | -- | none | 2026-11-17 15:46 UTC | `get_system`, own ship |
| `tortoise_roads` | Tortoise Roads | asteroid_belt | -- | iron_ore: richness 28, 98012 of 100000 left; copper_ore: richness 26, 98845 of 100000 left; darksteel_ore: richness 6, 309 of 309 left | none | 2026-11-17 15:46 UTC | `get_poi`, own ship |
| `ross_614_fading_ember` | Ross 614 Fading Ember | asteroid_belt | -- | iron_ore: richness 34, 7625 of 100000 left; copper_ore: richness 34, 7539 of 100000 left; plasma_residue: richness 7, 477 of 836 left | none | 2026-11-17 15:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:46 UTC | own ship | Read Tortoise Roads: 197,166 units left in all | `get_poi`, own ship |
| 2026-11-17 15:46 UTC | own ship | Read Ross 614 Fading Ember: 15,641 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
