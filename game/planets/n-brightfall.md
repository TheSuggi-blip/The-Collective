---
name: brightfall
id: 20261117T000622Z
tier: intel
author: Unity
kind: system
system_id: brightfall
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Brightfall

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where brightfall`).

| Field | Value |
|---|---|
| Position | x -4896.6, y -2140.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | birchwood, errai, gsc_0014, pinecross, wezen |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `brightfall_star` | Brightfall Star | sun (K2V) | -- | -- | none | 2026-11-16 23:52 UTC | `get_system`, own ship |
| `brightfall_belt` | Brightfall Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-16 23:52 UTC | `get_system`, own ship |
| `brightfall_frost_ring` | Brightfall Frost Ring | ice_field (cometary) | -- | not read | none | 2026-11-16 23:52 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:52 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `brightfall_belt`, `brightfall_frost_ring`.
