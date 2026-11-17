---
name: silvermark
id: 20261117T174149Z
tier: intel
author: Unity
kind: system
system_id: silvermark
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Silvermark

- system 19 jumps from home, police level 0. Station: Glintfin Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where silvermark`).

| Field | Value |
|---|---|
| Position | x 3664.2, y -1654.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | breckenridge, gsc_0011, gsc_0018, nekkar, upsilon_andromedae |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `silvermark_star` | Silvermark Star | sun (K6V) | -- | -- | none | 2026-11-17 16:46 UTC | `get_system`, own ship |
| `silvermark_i` | Silvermark I | planet (scorched) | -- | -- | none | 2026-11-17 16:46 UTC | `get_system`, own ship |
| `silvermark_ii` | Silvermark II | planet (arid) | -- | -- | none | 2026-11-17 16:46 UTC | `get_system`, own ship |
| `silvermark_iii` | Silvermark III | planet (terran) | -- | -- | none | 2026-11-17 16:46 UTC | `get_system`, own ship |
| `silvermark_iv` | Silvermark IV | planet (tundra) | -- | -- | none | 2026-11-17 16:46 UTC | `get_system`, own ship |
| `silvermark_v` | Silvermark V | planet (glacial) | -- | -- | none | 2026-11-17 16:46 UTC | `get_system`, own ship |
| `silvermark_depleted_workings` | Silvermark Depleted Workings | asteroid_belt (metallic) | -- | silver_ore: richness 8, 10 of 25000 left; iron_ore: richness 35, 9660 of 100000 left | none | 2026-11-17 16:46 UTC | `get_poi`, own ship |
| `f5c443ef4344cba46a049c3252d89260` | Glintfin Range | station | `dd3585847939dda0ee1db268af8521ba` | -- | none | 2026-11-17 16:46 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Glintfin Range (`dd3585847939dda0ee1db268af8521ba`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:46 UTC | `get_system`, own ship |

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
| 2026-11-17 16:46 UTC | own ship | Read Silvermark Depleted Workings: 9,670 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
