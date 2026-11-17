---
name: diadem
id: 20261117T041726Z
tier: intel
author: Unity
kind: system
system_id: diadem
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Diadem

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where diadem`).

| Field | Value |
|---|---|
| Position | x -1807.7, y 236.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | acrux, botein, intercrus, lanternwick |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `diadem_star` | Diadem Star | sun (M4V) | -- | -- | none | 2026-11-17 04:10 UTC | `get_system`, own ship |
| `diadem_i` | Diadem I | planet (scorched) | -- | -- | none | 2026-11-17 04:10 UTC | `get_system`, own ship |
| `diadem_ii` | Diadem II | planet (arid) | -- | -- | none | 2026-11-17 04:10 UTC | `get_system`, own ship |
| `diadem_iii` | Diadem III | planet (terran) | -- | -- | none | 2026-11-17 04:10 UTC | `get_system`, own ship |
| `diadem_iv` | Diadem IV | planet (jovian) | -- | -- | none | 2026-11-17 04:10 UTC | `get_system`, own ship |
| `diadem_v` | Diadem V | planet (jovian) | -- | -- | none | 2026-11-17 04:10 UTC | `get_system`, own ship |
| `diadem_ice_belt` | Diadem Ice Belt | ice_field (kuiper) | -- | water_ice: richness 40, 20892 of 50000 left; helium_ice: richness 12, 4459 of 5000 left | none | 2026-11-17 04:10 UTC | `get_poi`, own ship |

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
| 2026-11-17 04:10 UTC | own ship | Read Diadem Ice Belt: 25,351 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
