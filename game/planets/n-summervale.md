---
name: summervale
id: 20261117T123206Z
tier: intel
author: Unity
kind: system
system_id: summervale
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Summervale

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where summervale`).

| Field | Value |
|---|---|
| Position | x -4979.9, y -5382.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | libertas, meridian, navi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `summervale_star` | Summervale Star | sun (K6V) | -- | -- | none | 2026-11-17 11:55 UTC | `get_system`, own ship |
| `summervale_i` | Summervale I | planet (scorched) | -- | -- | none | 2026-11-17 11:55 UTC | `get_system`, own ship |
| `summervale_belt` | Summervale Belt | asteroid_belt (metallic) | -- | iron_ore: richness 37, 99999 of 100000 left; copper_ore: richness 44, 100000 of 100000 left | none | 2026-11-17 11:55 UTC | `get_poi`, own ship |
| `summervale_gas_pocket` | Summervale Gas Pocket | gas_cloud (molecular_cloud) | -- | plasma_gas: richness 16, 10000 of 10000 left; neon_gas: richness 37, 41741 of 50000 left | none | 2026-11-17 11:55 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:55 UTC | own ship | Read Summervale Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 11:55 UTC | own ship | Read Summervale Gas Pocket: 51,741 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
