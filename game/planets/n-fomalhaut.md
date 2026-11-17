---
name: fomalhaut
id: 20261117T102826Z
tier: intel
author: Unity
kind: system
system_id: fomalhaut
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Fomalhaut

- system 12 jumps from home, police level 0. Station: ENDL:fomalhaut.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where fomalhaut`).

| Field | Value |
|---|---|
| Position | x -597.9, y 6224.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | jishui, pleione, yed_posterior |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `fomalhaut_star` | Fomalhaut Star | sun (G2V) | -- | -- | none | 2026-11-17 10:08 UTC | `get_system`, own ship |
| `fomalhaut_i` | Fomalhaut I | planet (scorched) | -- | -- | none | 2026-11-17 10:08 UTC | `get_system`, own ship |
| `fomalhaut_belt` | Fomalhaut Belt | asteroid_belt (metallic) | -- | iron_ore: richness 45, 21032 of 100000 left; copper_ore: richness 36, 100000 of 100000 left | none | 2026-11-17 10:08 UTC | `get_poi`, own ship |
| `928a5bc980039657de67bc9737f21f92` | ENDL:fomalhaut | station | `c0fc642303936d486889b183c122c3f0` | -- | none | 2026-11-17 10:08 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| ENDL:fomalhaut (`c0fc642303936d486889b183c122c3f0`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 10:08 UTC | `get_system`, own ship |

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
| 2026-11-17 10:08 UTC | own ship | Read Fomalhaut Belt: 121,032 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
