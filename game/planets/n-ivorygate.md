---
name: ivorygate
id: 20261117T112929Z
tier: intel
author: Unity
kind: system
system_id: ivorygate
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ivorygate

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ivorygate`).

| Field | Value |
|---|---|
| Position | x 2075.6, y 2942.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | nashira, scheat, subra, toi_1452 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ivorygate_star` | Ivorygate Star | sun (K4V) | -- | -- | none | 2026-11-17 11:19 UTC | `get_system`, own ship |
| `ivorygate_i` | Ivorygate I | planet (scorched) | -- | -- | none | 2026-11-17 11:19 UTC | `get_system`, own ship |
| `ivorygate_belt` | Ivorygate Belt | asteroid_belt (metallic) | -- | iron_ore: richness 64, 16637 of 100000 left; copper_ore: richness 46, 59430 of 100000 left | none | 2026-11-17 11:19 UTC | `get_poi`, own ship |
| `forgotten_prism` | Forgotten Prism | nebula | -- | -- | none | 2026-11-17 11:19 UTC | `get_system`, own ship |

## Stations

None on the chart.

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
| 2026-11-17 11:19 UTC | own ship | Read Ivorygate Belt: 76,067 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
