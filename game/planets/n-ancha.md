---
name: ancha
id: 20261117T133329Z
tier: intel
author: Unity
kind: system
system_id: ancha
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ancha

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ancha`).

| Field | Value |
|---|---|
| Position | x -5223.9, y -4423.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | emberglow, greymist, heathwick, meridian, shadowmere, willowthorn |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ancha_haze` | Ancha Haze | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 12:59 UTC | `get_system`, own ship |
| `ancha_frozen_drift` | Ancha Frozen Drift | ice_field (kuiper) | -- | nothing listed | none | 2026-11-17 12:59 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:59 UTC | own ship | Read Ancha Frozen Drift: nothing left | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `ancha_haze`.
