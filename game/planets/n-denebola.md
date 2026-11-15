---
name: denebola
id: 20261115T235515Z
tier: intel
author: Unity
kind: system
system_id: denebola
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Denebola

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where denebola`).

| Field | Value |
|---|---|
| Position | x -5729.4, y 3324.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | brachium, gsc_0049, miram, nightveil |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `denebola_star` | Denebola Star | sun (F8V) | -- | -- | none | 2026-11-15 23:32 UTC | `get_system`, own ship |
| `denebola_i` | Denebola I | planet (scorched) | -- | -- | none | 2026-11-15 23:32 UTC | `get_system`, own ship |
| `denebola_fractured_prism` | Denebola Fractured Prism | nebula | -- | -- | none | 2026-11-15 23:32 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 23:32 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
