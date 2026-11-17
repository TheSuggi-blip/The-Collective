---
name: rasalgethi
id: 20261117T163943Z
tier: intel
author: Unity
kind: system
system_id: rasalgethi
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Rasalgethi

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rasalgethi`).

| Field | Value |
|---|---|
| Position | x 2712.6, y 3357.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | fumalsamakah, nashira, rigel, ross_614 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rasalgethi_star` | Rasalgethi Star | sun (M4V) | -- | -- | none | 2026-11-17 15:48 UTC | `get_system`, own ship |
| `rasalgethi_i` | Rasalgethi I | planet (scorched) | -- | -- | none | 2026-11-17 15:48 UTC | `get_system`, own ship |
| `rasalgethi_ii` | Rasalgethi II | planet (arid) | -- | -- | none | 2026-11-17 15:48 UTC | `get_system`, own ship |
| `rasalgethi_iii` | Rasalgethi III | planet (terran) | -- | -- | none | 2026-11-17 15:48 UTC | `get_system`, own ship |
| `rasalgethi_iv` | Rasalgethi IV | planet (jovian) | -- | -- | none | 2026-11-17 15:48 UTC | `get_system`, own ship |
| `kneeling_veins` | Kneeling Veins | asteroid_belt | -- | iron_ore: richness 32, 100000 of 100000 left; copper_ore: richness 29, 100000 of 100000 left; darksteel_ore: richness 5, 290 of 290 left | none | 2026-11-17 15:48 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:48 UTC | own ship | Read Kneeling Veins: 200,290 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
