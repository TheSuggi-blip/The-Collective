---
name: the_levy
id: 20261117T143554Z
tier: intel
author: Unity
kind: system
system_id: the_levy
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# The Levy

Nebula system 20 jumps from home, police level 30. Station: The Levy Customs Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where the_levy`).

| Field | Value |
|---|---|
| Position | x 1071.8, y -4569.6 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 20 |
| Lanes | gliese_436, ogma, stonecrest, wealth_lane |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tollkeeper` | Tollkeeper | sun (A8V) | -- | -- | none | 2026-11-17 14:08 UTC | `get_system`, own ship |
| `levy_i` | Levy I | planet (arid) | -- | -- | none | 2026-11-17 14:08 UTC | `get_system`, own ship |
| `levy_ii` | Levy II | planet (tundra) | -- | -- | none | 2026-11-17 14:08 UTC | `get_system`, own ship |
| `levy_ice_fields` | Levy Ice Fields | ice_field (kuiper) | -- | not read | none | 2026-11-17 14:08 UTC | `get_system`, own ship |
| `the_levy_customs_station` | The Levy Customs Station | station | `the_levy_customs_station` | -- | none | 2026-11-17 14:08 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Levy Customs Station (`the_levy_customs_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:08 UTC | `get_system`, own ship |

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
| 2026-11-17 14:08 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `levy_ice_fields`.
