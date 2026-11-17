---
name: sadr
id: 20261117T133402Z
tier: intel
author: Unity
kind: system
system_id: sadr
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sadr

- system 28 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sadr`).

| Field | Value |
|---|---|
| Position | x 5382.8, y -3323.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 28 |
| Lanes | altair, foxglove, inquill, ironveil, quartzfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sadr_star` | Sadr Star | sun (M4V) | -- | -- | none | 2026-11-17 12:43 UTC | `get_system`, own ship |
| `sadr_i` | Sadr I | planet (scorched) | -- | -- | none | 2026-11-17 12:43 UTC | `get_system`, own ship |
| `sadr_ii` | Sadr II | planet (arid) | -- | -- | none | 2026-11-17 12:43 UTC | `get_system`, own ship |
| `sadr_belt` | Sadr Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 12:43 UTC | `get_system`, own ship |
| `sadr_ice_belt` | Sadr Ice Belt | ice_field (cometary) | -- | water_ice: richness 50, 44645 of 50000 left; carbon_dioxide_ice: richness 12, 5000 of 5000 left | none | 2026-11-17 12:43 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:43 UTC | own ship | Read Sadr Ice Belt: 49,645 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `sadr_belt`.
