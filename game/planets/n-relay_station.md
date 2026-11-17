---
name: relay_station
id: 20261117T092736Z
tier: intel
author: Unity
kind: system
system_id: relay_station
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Relay Station

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where relay_station`).

| Field | Value |
|---|---|
| Position | x -4038.0, y 1062.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | clearwater, innes_40, rotanev, the_archive |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ross_major_star` | Ross Major Star | sun (DA) | -- | -- | none | 2026-11-17 08:46 UTC | `get_system`, own ship |
| `ross_major_i` | Ross Major I | planet (scorched) | -- | -- | none | 2026-11-17 08:46 UTC | `get_system`, own ship |
| `ross_major_ii` | Ross Major II | planet (arid) | -- | -- | none | 2026-11-17 08:46 UTC | `get_system`, own ship |
| `ross_major_iii` | Ross Major III | planet (terran) | -- | -- | none | 2026-11-17 08:46 UTC | `get_system`, own ship |
| `ross_major_iv` | Ross Major IV | planet (tundra) | -- | -- | none | 2026-11-17 08:46 UTC | `get_system`, own ship |
| `ross_major_belt` | Ross Major Belt | asteroid_belt (metallic) | -- | iron_ore: richness 62, 100000 of 100000 left; copper_ore: richness 44, 100000 of 100000 left | none | 2026-11-17 08:46 UTC | `get_poi`, own ship |
| `relay_station_ice_shelf` | Relay Station Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 64, 45560 of 50000 left; nitrogen_ice: richness 50, 50000 of 50000 left; helium_ice: richness 20, 5000 of 5000 left | none | 2026-11-17 08:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:46 UTC | own ship | Read Ross Major Belt: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 08:46 UTC | own ship | Read Relay Station Ice Shelf: 100,560 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
