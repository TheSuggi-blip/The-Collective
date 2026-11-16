---
name: acrux
id: 20261116T050016Z
tier: intel
author: Unity
kind: system
system_id: acrux
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Acrux

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where acrux`).

| Field | Value |
|---|---|
| Position | x -1525.3, y 609.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | botein, diadem, furud, gsc_0044, hd_40307 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `acrux_star` | Acrux Star | sun (M2V) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `acrux_i` | Acrux I | planet (scorched) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `acrux_ii` | Acrux II | planet (arid) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `acrux_iii` | Acrux III | planet (terran) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `acrux_iv` | Acrux IV | planet (tundra) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `acrux_belt` | Acrux Belt | asteroid_belt (metallic) | -- | iron_ore: richness 64, 99999 of 100000 left; copper_ore: richness 36, 100000 of 100000 left; lithium_ore: richness 36, 10859 of 25000 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |

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
| 2026-11-16 04:39 UTC | own ship | Read Acrux Belt: 210,858 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
