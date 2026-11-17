---
name: first_step
id: 20261117T174210Z
tier: intel
author: Unity
kind: system
system_id: first_step
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 55
updated: 2026-11-17
---

# First Step

Outerrim system 18 jumps from home, police level 55. Station: First Step Memorial Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where first_step`).

| Field | Value |
|---|---|
| Position | x -2334.9, y -3308.0 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 18 |
| Lanes | horizon, markeb, the_telescope, void_gate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `betelgeuse_prime_star` | Betelgeuse Prime Star | sun (M2Ib) | -- | -- | none | 2026-11-17 17:02 UTC | `get_system`, own ship |
| `first_step_prime` | First Step Prime | planet (arid) | -- | -- | none | 2026-11-17 17:02 UTC | `get_system`, own ship |
| `colony_debris_field` | Colony Debris Field | asteroid_belt (mixed) | -- | carbon_ore: richness 30, 0 of 30000 left; iron_ore: richness 25, 0 of 100000 left | none | 2026-11-17 17:02 UTC | `get_poi`, own ship |
| `colony_station_hulk` | Colony Station Hulk | relic (derelict) | -- | -- | none | 2026-11-17 17:02 UTC | `get_system`, own ship |
| `first_step_memorial_station` | First Step Memorial Station | station | `first_step_memorial_station` | -- | none | 2026-11-17 17:02 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| First Step Memorial Station (`first_step_memorial_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:02 UTC | `get_system`, own ship |

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
| 2026-11-17 17:02 UTC | own ship | Read Colony Debris Field: nothing left | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
