---
name: helvetios
id: 20261117T143541Z
tier: intel
author: Unity
kind: system
system_id: helvetios
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Helvetios

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where helvetios`).

| Field | Value |
|---|---|
| Position | x 810.4, y -6190.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | alioth, almach, caph, gsc_0025, thornfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `helvetios_star` | Helvetios Star | sun (M6V) | -- | -- | none | 2026-11-17 14:05 UTC | `get_system`, own ship |
| `helvetios_i` | Helvetios I | planet (scorched) | -- | -- | none | 2026-11-17 14:05 UTC | `get_system`, own ship |
| `helvetios_frost_ring` | Helvetios Frost Ring | ice_field (cometary) | -- | water_ice: richness 47, 11943 of 50000 left; nitrogen_ice: richness 34, 49852 of 50000 left | none | 2026-11-17 14:05 UTC | `get_poi`, own ship |
| `helvetios_stray_facets` | Helvetios Stray Facets | asteroid_belt | -- | not read | none | 2026-11-17 14:05 UTC | `get_system`, own ship |

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
| 2026-11-17 14:05 UTC | own ship | Read Helvetios Frost Ring: 61,795 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `helvetios_stray_facets`.
