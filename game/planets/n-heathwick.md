---
name: heathwick
id: 20261117T123146Z
tier: intel
author: Unity
kind: system
system_id: heathwick
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Heathwick

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where heathwick`).

| Field | Value |
|---|---|
| Position | x -4764.6, y -4556.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | ancha, meridian, navi, shadowmere, wolf_359 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `heathwick_star` | Heathwick Star | sun (K2V) | -- | -- | none | 2026-11-17 12:00 UTC | `get_system`, own ship |
| `heathwick_i` | Heathwick I | planet (scorched) | -- | -- | none | 2026-11-17 12:00 UTC | `get_system`, own ship |
| `heathwick_ii` | Heathwick II | planet (arid) | -- | -- | none | 2026-11-17 12:00 UTC | `get_system`, own ship |
| `heathwick_iii` | Heathwick III | planet (terran) | -- | -- | none | 2026-11-17 12:00 UTC | `get_system`, own ship |
| `heathwick_belt` | Heathwick Belt | asteroid_belt (metallic) | -- | iron_ore: richness 66, 69992 of 100000 left; copper_ore: richness 42, 100000 of 100000 left; zinc_ore: richness 23, 17709 of 19000 left | none | 2026-11-17 12:00 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:00 UTC | own ship | Read Heathwick Belt: 187,701 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
