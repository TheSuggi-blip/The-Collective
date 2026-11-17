---
name: edgewater
id: 20261117T153731Z
tier: intel
author: Unity
kind: system
system_id: edgewater
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Edgewater

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where edgewater`).

| Field | Value |
|---|---|
| Position | x 5013.5, y -188.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | alshat, duskmere, dusthaven, quarrytown, undercliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `edgewater_star` | Edgewater Star | sun (M2V) | -- | -- | none | 2026-11-17 15:07 UTC | `get_system`, own ship |
| `edgewater_i` | Edgewater I | planet (scorched) | -- | -- | none | 2026-11-17 15:07 UTC | `get_system`, own ship |
| `edgewater_ii` | Edgewater II | planet (arid) | -- | -- | none | 2026-11-17 15:07 UTC | `get_system`, own ship |
| `edgewater_iii` | Edgewater III | planet (terran) | -- | -- | none | 2026-11-17 15:07 UTC | `get_system`, own ship |
| `edgewater_belt` | Edgewater Belt | asteroid_belt (metallic) | -- | iron_ore: richness 55, 99999 of 100000 left; copper_ore: richness 44, 99999 of 100000 left; aluminum_ore: richness 67, 484 of 30000 left; manganese_ore: richness 26, 4041 of 18000 left | none | 2026-11-17 15:07 UTC | `get_poi`, own ship |
| `bluecast_seam` | Bluecast Seam | asteroid_belt | -- | iron_ore: richness 35, 100000 of 100000 left; copper_ore: richness 24, 100000 of 100000 left; cobalt_ore: richness 37, 10 of 25000 left | none | 2026-11-17 15:07 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:07 UTC | own ship | Read Edgewater Belt: 204,523 units left in all | `get_poi`, own ship |
| 2026-11-17 15:07 UTC | own ship | Read Bluecast Seam: 200,010 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
