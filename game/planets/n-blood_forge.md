---
name: blood_forge
id: 20261117T153727Z
tier: intel
author: Unity
kind: system
system_id: blood_forge
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 80
updated: 2026-11-17
---

# Blood Forge

Crimson system 20 jumps from home, police level 80. Station: Blood Forge Smelting Works.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where blood_forge`).

| Field | Value |
|---|---|
| Position | x 5263.8, y 3131.3 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 20 |
| Lanes | alzirr, iron_reach, krynn, stillwater, valor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `red_maw` | Red Maw | sun (M1III) | -- | -- | none | 2026-11-17 14:46 UTC | `get_system`, own ship |
| `slagworld` | Slagworld | planet (lava_world) | -- | -- | none | 2026-11-17 14:46 UTC | `get_system`, own ship |
| `crucible_minor` | Crucible Minor | planet (arid) | -- | -- | none | 2026-11-17 14:46 UTC | `get_system`, own ship |
| `blood_forge_smelting_works` | Blood Forge Smelting Works | station | `blood_forge_smelting_works` | -- | none | 2026-11-17 14:46 UTC | `get_system`, own ship |
| `red_maw_titanium_shoals` | Red Maw Titanium Shoals | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 14:46 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Blood Forge Smelting Works (`blood_forge_smelting_works`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:46 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:46 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `red_maw_titanium_shoals`.
