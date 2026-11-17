---
name: enif
id: 20261117T133334Z
tier: intel
author: Unity
kind: system
system_id: enif
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Enif

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where enif`).

| Field | Value |
|---|---|
| Position | x 2682.8, y -6221.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | glenhaven, gsc_0032, sadachbia, sadalmelik |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `enif_star` | Enif Star | sun (G5V) | -- | -- | none | 2026-11-17 12:34 UTC | `get_system`, own ship |
| `enif_i` | Enif I | planet (scorched) | -- | -- | none | 2026-11-17 12:34 UTC | `get_system`, own ship |
| `enif_ice_belt` | Enif Ice Belt | ice_field (kuiper) | -- | water_ice: richness 56, 45279 of 50000 left; nitrogen_ice: richness 41, 50000 of 50000 left; deuterium_ice: richness 13, 5000 of 5000 left; helium_ice: richness 23, 4527 of 5000 left | none | 2026-11-17 12:34 UTC | `get_poi`, own ship |
| `enif_wild_facets` | Enif Wild Facets | asteroid_belt | -- | iron_ore: richness 43, 100000 of 100000 left; copper_ore: richness 29, 100000 of 100000 left; trade_crystal: richness 21, 702 of 2600 left | none | 2026-11-17 12:34 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:34 UTC | own ship | Read Enif Ice Belt: 104,806 units left in all | `get_poi`, own ship |
| 2026-11-17 12:34 UTC | own ship | Read Enif Wild Facets: 200,702 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
