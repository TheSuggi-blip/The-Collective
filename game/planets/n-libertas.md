---
name: libertas
id: 20261117T153744Z
tier: intel
author: Unity
kind: system
system_id: libertas
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Libertas

- system 21 jumps from home, police level 0. Station: ENDL:libertas.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where libertas`).

| Field | Value |
|---|---|
| Position | x -4379.2, y -5466.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | gsc_0026, navi, summervale |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `libertas_star` | Libertas Star | sun (K2V) | -- | -- | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `libertas_i` | Libertas I | planet (scorched) | -- | -- | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `libertas_ii` | Libertas II | planet (arid) | -- | -- | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `libertas_belt` | Libertas Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `8f66582f4ff25f2accfe9c3f456a5600` | ENDL:libertas | station | `bd2a158b2c0950b831be358686eff953` | -- | none | 2026-11-17 14:35 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| ENDL:libertas (`bd2a158b2c0950b831be358686eff953`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:35 UTC | `get_system`, own ship |

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
| 2026-11-17 14:35 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `libertas_belt`.
