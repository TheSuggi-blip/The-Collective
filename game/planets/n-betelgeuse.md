---
name: betelgeuse
id: 20261117T163926Z
tier: intel
author: Unity
kind: system
system_id: betelgeuse
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Betelgeuse

- system 17 jumps from home, police level 0. Station: ENDL:betelgeuse.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where betelgeuse`).

| Field | Value |
|---|---|
| Position | x -6361.4, y -3246.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | gsc_0037, rimegate, veritate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `betelgeuse_star` | Betelgeuse Star | sun (M6V) | -- | -- | none | 2026-11-17 16:11 UTC | `get_system`, own ship |
| `betelgeuse_i` | Betelgeuse I | planet (scorched) | -- | -- | none | 2026-11-17 16:11 UTC | `get_system`, own ship |
| `betelgeuse_belt` | Betelgeuse Belt | asteroid_belt (metallic) | -- | iron_ore: richness 36, 99998 of 100000 left; copper_ore: richness 34, 99999 of 100000 left | none | 2026-11-17 16:11 UTC | `get_poi`, own ship |
| `b8e5ee2917f17ec7c89ca3a6821f34d4` | ENDL:betelgeuse | station | `cc9494fe55fb51dc74da14728199e609` | -- | none | 2026-11-17 16:11 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| ENDL:betelgeuse (`cc9494fe55fb51dc74da14728199e609`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:11 UTC | `get_system`, own ship |

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
| 2026-11-17 16:11 UTC | own ship | Read Betelgeuse Belt: 199,997 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
