---
name: barnardstar
id: 20261117T112924Z
tier: intel
author: Unity
kind: system
system_id: barnardstar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Barnardstar

- system 13 jumps from home, police level 0. Station: ENDL Barnardstar.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where barnardstar`).

| Field | Value |
|---|---|
| Position | x 1633.0, y 1999.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | alphecca, ankaa, toi_1452 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `barnardstar_star` | Barnardstar Star | sun (G8V) | -- | -- | none | 2026-11-17 11:01 UTC | `get_system`, own ship |
| `barnardstar_i` | Barnardstar I | planet (scorched) | -- | -- | none | 2026-11-17 11:01 UTC | `get_system`, own ship |
| `barnardstar_belt` | Barnardstar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 60, 673 of 100000 left; copper_ore: richness 37, 11523 of 100000 left; gold_ore: richness 37, 100 of 25000 left | none | 2026-11-17 11:01 UTC | `get_poi`, own ship |
| `bda0a4a03041d80373d220f479c3407e` | ENDL Barnardstar | station | `17278cea0329a7e3d3bd7f79d796a85e` | -- | none | 2026-11-17 11:01 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| ENDL Barnardstar (`17278cea0329a7e3d3bd7f79d796a85e`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 11:01 UTC | `get_system`, own ship |

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
| 2026-11-17 11:01 UTC | own ship | Read Barnardstar Belt: 12,296 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
