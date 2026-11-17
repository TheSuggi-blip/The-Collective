---
name: xihe
id: 20261117T205220Z
tier: intel
author: Unity
kind: system
system_id: xihe
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Xihe

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where xihe`).

| Field | Value |
|---|---|
| Position | x 1310.3, y -2767.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | alkaid, capella, gsc_0030, keelbreak |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `xihe_star` | Xihe Star | sun (M6V) | -- | -- | none | 2026-11-17 20:23 UTC | `get_system`, own ship |
| `xihe_i` | Xihe I | planet (scorched) | -- | -- | none | 2026-11-17 20:23 UTC | `get_system`, own ship |
| `xihe_ii` | Xihe II | planet (arid) | -- | -- | none | 2026-11-17 20:23 UTC | `get_system`, own ship |
| `xihe_iii` | Xihe III | planet (terran) | -- | -- | none | 2026-11-17 20:23 UTC | `get_system`, own ship |
| `xihe_iv` | Xihe IV | planet (tundra) | -- | -- | none | 2026-11-17 20:23 UTC | `get_system`, own ship |
| `xihe_frozen_drift` | Xihe Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 43, 1384 of 50000 left | none | 2026-11-17 20:23 UTC | `get_poi`, own ship |

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
| 2026-11-17 20:23 UTC | own ship | Read Xihe Frozen Drift: 1,384 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
