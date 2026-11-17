---
name: the_crucible
id: 20261117T123208Z
tier: intel
author: Unity
kind: system
system_id: the_crucible
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 55
updated: 2026-11-17
---

# The Crucible

Crimson system 18 jumps from home, police level 55. Station: The Crucible Garrison.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where the_crucible`).

| Field | Value |
|---|---|
| Position | x 4612.1, y 3516.5 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 18 |
| Lanes | bharani, iron_reach, stillwater, the_rampart, valor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `fury_minor` | Fury Minor | sun (M3V) | -- | -- | none | 2026-11-17 12:22 UTC | `get_system`, own ship |
| `crucible_prime` | Crucible Prime | planet (terran) | -- | -- | none | 2026-11-17 12:22 UTC | `get_system`, own ship |
| `crucible_vents` | Crucible Vents | gas_cloud (atmospheric) | -- | argon_gas: richness 50, 1 of 50000 left; plasma_gas: richness 21, 0 of 10000 left; neon_gas: richness 34, 1 of 50000 left; chlorine_gas: richness 16, 0 of 10000 left | none | 2026-11-17 12:22 UTC | `get_poi`, own ship |
| `the_crucible_garrison` | The Crucible Garrison | station | `the_crucible_garrison` | -- | none | 2026-11-17 12:22 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Crucible Garrison (`the_crucible_garrison`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 12:22 UTC | `get_system`, own ship |

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
| 2026-11-17 12:22 UTC | own ship | Read Crucible Vents: 2 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
