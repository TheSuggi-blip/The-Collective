---
name: starfall
id: 20261117T194614Z
tier: intel
author: Unity
kind: system
system_id: starfall
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 30
updated: 2026-11-17
---

# Starfall

Outerrim system 18 jumps from home, police level 30. Station: Starfall Salvage Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where starfall`).

| Field | Value |
|---|---|
| Position | x -2058.8, y -2591.8 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 18 |
| Lanes | kochab, sulafat, the_telescope, void_gate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `starfall_star` | Starfall Star | sun (K5V) | -- | -- | none | 2026-11-17 19:07 UTC | `get_system`, own ship |
| `starfall_landing` | Starfall Landing | planet (scorched) | -- | -- | none | 2026-11-17 19:07 UTC | `get_system`, own ship |
| `starfall_belt` | Starfall Belt | asteroid_belt (mixed) | -- | not read | none | 2026-11-17 19:07 UTC | `get_system`, own ship |
| `starfall_salvage_station` | Starfall Salvage Station | station | `starfall_salvage_station` | -- | none | 2026-11-17 19:07 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Starfall Salvage Station (`starfall_salvage_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 19:07 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 19:07 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `starfall_belt`.
