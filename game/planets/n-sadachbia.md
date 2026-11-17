---
name: sadachbia
id: 20261117T133359Z
tier: intel
author: Unity
kind: system
system_id: sadachbia
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sadachbia

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sadachbia`).

| Field | Value |
|---|---|
| Position | x 2389.3, y -6226.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | enif, glenhaven, naos, sadalmelik |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sadachbia_star` | Sadachbia Star | sun (M2V) | -- | -- | none | 2026-11-17 12:37 UTC | `get_system`, own ship |
| `sadachbia_i` | Sadachbia I | planet (scorched) | -- | -- | none | 2026-11-17 12:37 UTC | `get_system`, own ship |
| `sadachbia_ii` | Sadachbia II | planet (arid) | -- | -- | none | 2026-11-17 12:37 UTC | `get_system`, own ship |
| `sadachbia_belt` | Sadachbia Belt | asteroid_belt (metallic) | -- | iron_ore: richness 49, 99998 of 100000 left; copper_ore: richness 40, 99999 of 100000 left; aluminum_ore: richness 54, 30000 of 30000 left | none | 2026-11-17 12:37 UTC | `get_poi`, own ship |
| `dead_markers_field` | Dead Markers Field | asteroid_belt | -- | iron_ore: richness 34, 100000 of 100000 left; copper_ore: richness 27, 100000 of 100000 left; trade_crystal: richness 18, 687 of 2800 left | none | 2026-11-17 12:37 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:37 UTC | own ship | Read Sadachbia Belt: 229,997 units left in all | `get_poi`, own ship |
| 2026-11-17 12:37 UTC | own ship | Read Dead Markers Field: 200,687 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
