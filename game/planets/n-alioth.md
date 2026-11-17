---
name: alioth
id: 20261117T143527Z
tier: intel
author: Unity
kind: system
system_id: alioth
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alioth

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alioth`).

| Field | Value |
|---|---|
| Position | x 1195.8, y -5956.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | almach, azmidi, caph, helvetios, thornfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alioth_star` | Alioth Star | sun (F5V) | -- | -- | none | 2026-11-17 14:34 UTC | `get_system`, own ship |
| `alioth_i` | Alioth I | planet (scorched) | -- | -- | none | 2026-11-17 14:34 UTC | `get_system`, own ship |
| `alioth_ii` | Alioth II | planet (arid) | -- | -- | none | 2026-11-17 14:34 UTC | `get_system`, own ship |
| `alioth_iii` | Alioth III | planet (terran) | -- | -- | none | 2026-11-17 14:34 UTC | `get_system`, own ship |
| `alioth_gas_plume` | Alioth Gas Plume | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 14:34 UTC | `get_system`, own ship |
| `alioth_wild_facets` | Alioth Wild Facets | asteroid_belt | -- | not read | none | 2026-11-17 14:34 UTC | `get_system`, own ship |

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
| 2026-11-17 14:34 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `alioth_gas_plume`, `alioth_wild_facets`.
