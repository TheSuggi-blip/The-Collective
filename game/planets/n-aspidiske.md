---
name: aspidiske
id: 20261117T102825Z
tier: intel
author: Unity
kind: system
system_id: aspidiske
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Aspidiske

- system 12 jumps from home, police level 0. Station: Copperbelt Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where aspidiske`).

| Field | Value |
|---|---|
| Position | x 877.6, y 18.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | barnards_star, dheneb |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `aspidiske_star` | Aspidiske Star | sun (M4V) | -- | -- | none | 2026-11-17 10:03 UTC | `get_system`, own ship |
| `aspidiske_belt` | Aspidiske Belt | asteroid_belt (metallic) | -- | iron_ore: richness 59, 100000 of 100000 left; copper_ore: richness 25, 100000 of 100000 left; manganese_ore: richness 20, 12098 of 14000 left | none | 2026-11-17 10:03 UTC | `get_poi`, own ship |
| `9065d81f81e8852261ed8c6e5e9e7ec8` | Copperbelt Range | station | `c18bc91c2d6c27e59f56c32bd24fdd3b` | -- | none | 2026-11-17 10:03 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Copperbelt Range (`c18bc91c2d6c27e59f56c32bd24fdd3b`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 10:03 UTC | `get_system`, own ship |

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
| 2026-11-17 10:03 UTC | own ship | Read Aspidiske Belt: 212,098 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
