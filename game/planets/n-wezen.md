---
name: wezen
id: 20261117T174139Z
tier: intel
author: Unity
kind: system
system_id: wezen
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Wezen

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where wezen`).

| Field | Value |
|---|---|
| Position | x -4822.7, y -2360.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | birchwood, brightfall, errai, gsc_0014, tarazed |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `wezen_star` | Wezen Star | sun (M2V) | -- | -- | none | 2026-11-17 17:10 UTC | `get_system`, own ship |
| `wezen_i` | Wezen I | planet (scorched) | -- | -- | none | 2026-11-17 17:10 UTC | `get_system`, own ship |
| `wezen_ii` | Wezen II | planet (arid) | -- | -- | none | 2026-11-17 17:10 UTC | `get_system`, own ship |
| `wezen_faint_entanglement` | Wezen Faint Entanglement | nebula | -- | -- | none | 2026-11-17 17:10 UTC | `get_system`, own ship |

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
| 2026-11-17 17:10 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
