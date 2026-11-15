---
name: achird
id: 20261115T215315Z
tier: intel
author: Unity
kind: system
system_id: achird
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Achird

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where achird`).

| Field | Value |
|---|---|
| Position | x -4517.3, y 4688.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | amberfall, megrez, thornhaven |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `achird_star` | Achird Star | sun (A5V) | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |
| `achird_i` | Achird I | planet (scorched) | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |
| `achird_ii` | Achird II | planet (arid) | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |
| `achird_iii` | Achird III | planet (terran) | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |
| `achird_belt` | Achird Belt | asteroid_belt (metallic) | -- | iron_ore: richness 45, 99999 of 100000 left; copper_ore: richness 34, 100000 of 100000 left; manganese_ore: richness 22, 10184 of 16000 left | none | 2026-11-15 21:51 UTC | `get_poi`, own ship |
| `faintlight_drift` | Faintlight Drift | nebula | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:51 UTC | own ship | Read Achird Belt: 210,183 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
