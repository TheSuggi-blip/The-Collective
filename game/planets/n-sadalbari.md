---
name: sadalbari
id: 20261117T143550Z
tier: intel
author: Unity
kind: system
system_id: sadalbari
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sadalbari

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sadalbari`).

| Field | Value |
|---|---|
| Position | x -9.1, y -7018.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | alcor, asterope, gliese_667, hd_85512, menkalinan, poerava, unukalhai, yarrowfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sadalbari_star` | Sadalbari Star | sun (G5V) | -- | -- | none | 2026-11-17 14:00 UTC | `get_system`, own ship |
| `sadalbari_i` | Sadalbari I | planet (scorched) | -- | -- | none | 2026-11-17 14:00 UTC | `get_system`, own ship |
| `sadalbari_belt` | Sadalbari Belt | asteroid_belt (metallic) | -- | iron_ore: richness 59, 99998 of 100000 left; copper_ore: richness 23, 99995 of 100000 left; silver_ore: richness 25, 0 of 25000 left | none | 2026-11-17 14:00 UTC | `get_poi`, own ship |
| `unpolished_scatter` | Unpolished Scatter | asteroid_belt | -- | iron_ore: richness 40, 100000 of 100000 left; copper_ore: richness 24, 100000 of 100000 left; trade_crystal: richness 21, 41 of 2900 left | none | 2026-11-17 14:00 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:00 UTC | own ship | Read Sadalbari Belt: 199,993 units left in all | `get_poi`, own ship |
| 2026-11-17 14:00 UTC | own ship | Read Unpolished Scatter: 200,041 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
