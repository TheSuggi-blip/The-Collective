---
name: dusthaven
id: 20261117T174211Z
tier: intel
author: Unity
kind: system
system_id: dusthaven
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Dusthaven

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where dusthaven`).

| Field | Value |
|---|---|
| Position | x 4793.0, y -77.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | atik, duskmere, edgewater, larawag, undercliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dusthaven_star` | Dusthaven Star | sun (M6V) | -- | -- | none | 2026-11-17 17:06 UTC | `get_system`, own ship |
| `dusthaven_i` | Dusthaven I | planet (scorched) | -- | -- | none | 2026-11-17 17:06 UTC | `get_system`, own ship |
| `dusthaven_ii` | Dusthaven II | planet (arid) | -- | -- | none | 2026-11-17 17:06 UTC | `get_system`, own ship |
| `dusthaven_iii` | Dusthaven III | planet (terran) | -- | -- | none | 2026-11-17 17:06 UTC | `get_system`, own ship |
| `dusthaven_iv` | Dusthaven IV | planet (tundra) | -- | -- | none | 2026-11-17 17:06 UTC | `get_system`, own ship |
| `dusthaven_v` | Dusthaven V | planet (glacial) | -- | -- | none | 2026-11-17 17:06 UTC | `get_system`, own ship |
| `dusk_scatter` | Dusk Scatter | asteroid_belt | -- | aluminum_ore: richness 40, 2334 of 30000 left | none | 2026-11-17 17:06 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:06 UTC | own ship | Read Dusk Scatter: 2,334 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
