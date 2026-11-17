---
name: propus
id: 20261117T153752Z
tier: intel
author: Unity
kind: system
system_id: propus
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Propus

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where propus`).

| Field | Value |
|---|---|
| Position | x 2241.4, y 1279.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | ankaa, coalridge, spica, syrma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `propus_star` | Propus Star | sun (G8V) | -- | -- | none | 2026-11-17 14:50 UTC | `get_system`, own ship |
| `propus_i` | Propus I | planet (scorched) | -- | -- | none | 2026-11-17 14:50 UTC | `get_system`, own ship |
| `propus_ii` | Propus II | planet (arid) | -- | -- | none | 2026-11-17 14:50 UTC | `get_system`, own ship |
| `propus_belt` | Propus Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 14:50 UTC | `get_system`, own ship |
| `propus_ice_belt` | Propus Ice Belt | ice_field (kuiper) | -- | not read | none | 2026-11-17 14:50 UTC | `get_system`, own ship |

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
| 2026-11-17 14:50 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `propus_belt`, `propus_ice_belt`.
