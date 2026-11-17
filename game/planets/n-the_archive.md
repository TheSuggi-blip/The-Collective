---
name: the_archive
id: 20261117T092739Z
tier: intel
author: Unity
kind: system
system_id: the_archive
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# The Archive

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where the_archive`).

| Field | Value |
|---|---|
| Position | x -4405.8, y 1153.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | clearwater, innes_40, relay_station, rotanev |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `shielded_data_cache` | Shielded Data Cache | relic | -- | -- | none | 2026-11-17 09:04 UTC | `get_system`, own ship |
| `capella_major_star` | Capella Major Star | sun (M4V) | -- | -- | none | 2026-11-17 09:04 UTC | `get_system`, own ship |
| `capella_major_i` | Capella Major I | planet (scorched) | -- | -- | none | 2026-11-17 09:04 UTC | `get_system`, own ship |
| `capella_major_ii` | Capella Major II | planet (arid) | -- | -- | none | 2026-11-17 09:04 UTC | `get_system`, own ship |
| `capella_major_belt` | Capella Major Belt | asteroid_belt (metallic) | -- | iron_ore: richness 65, 99999 of 100000 left; copper_ore: richness 35, 100000 of 100000 left; aluminum_ore: richness 51, 4460 of 30000 left | none | 2026-11-17 09:04 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:04 UTC | own ship | Read Capella Major Belt: 204,459 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
