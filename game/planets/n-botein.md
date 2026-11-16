---
name: botein
id: 20261116T050017Z
tier: intel
author: Unity
kind: system
system_id: botein
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Botein

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where botein`).

| Field | Value |
|---|---|
| Position | x -1690.5, y 476.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | acrux, diadem, gsc_0044, intercrus, lanternwick |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `botein_star` | Botein Star | sun (M2V) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `botein_i` | Botein I | planet (scorched) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `botein_ii` | Botein II | planet (arid) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `botein_iii` | Botein III | planet (terran) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `botein_belt` | Botein Belt | asteroid_belt (metallic) | -- | iron_ore: richness 68, 99999 of 100000 left; copper_ore: richness 47, 99999 of 100000 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |
| `lampglint_rock` | Lampglint Rock | asteroid_belt | -- | iron_ore: richness 30, 100000 of 100000 left; copper_ore: richness 21, 100000 of 100000 left; sol_alloy_ore: richness 5, 1676 of 1676 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |
| `raysheet_nebula` | Raysheet Nebula | nebula | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 04:39 UTC | own ship | Read Botein Belt: 199,998 units left in all | `get_poi`, own ship |
| 2026-11-16 04:39 UTC | own ship | Read Lampglint Rock: 201,676 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
