---
name: rotanev
id: 20261117T010830Z
tier: intel
author: Unity
kind: system
system_id: rotanev
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Rotanev

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rotanev`).

| Field | Value |
|---|---|
| Position | x -4586.1, y 996.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | chalawan, clearwater, innes_40, relay_station, the_archive |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rotanev_star` | Rotanev Star | sun (F8V) | -- | -- | none | 2026-11-17 00:46 UTC | `get_system`, own ship |
| `rotanev_i` | Rotanev I | planet (scorched) | -- | -- | none | 2026-11-17 00:46 UTC | `get_system`, own ship |
| `rotanev_ii` | Rotanev II | planet (arid) | -- | -- | none | 2026-11-17 00:46 UTC | `get_system`, own ship |
| `daylight_seam` | Daylight Seam | asteroid_belt | -- | nickel_ore: richness 22, 424 of 20000 left | none | 2026-11-17 00:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 00:46 UTC | own ship | Read Daylight Seam: 424 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
