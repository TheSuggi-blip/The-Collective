---
name: kapteyn_5
id: 20261117T092731Z
tier: intel
author: Unity
kind: system
system_id: kapteyn_5
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kapteyn 5

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kapteyn_5`).

| Field | Value |
|---|---|
| Position | x 474.3, y 1610.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | adhafera, deneb, gsc_0022, harborlight, misthollow |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kapteyn_5_star` | Kapteyn 5 Star | sun (M2V) | -- | -- | none | 2026-11-17 08:42 UTC | `get_system`, own ship |
| `kapteyn_5_i` | Kapteyn 5 I | planet (scorched) | -- | -- | none | 2026-11-17 08:42 UTC | `get_system`, own ship |
| `kapteyn_5_ii` | Kapteyn 5 II | planet (arid) | -- | -- | none | 2026-11-17 08:42 UTC | `get_system`, own ship |
| `kapteyn_5_iii` | Kapteyn 5 III | planet (terran) | -- | -- | none | 2026-11-17 08:42 UTC | `get_system`, own ship |
| `kapteyn_5_belt` | Kapteyn 5 Belt | asteroid_belt (metallic) | -- | iron_ore: richness 63, 14662 of 100000 left; copper_ore: richness 29, 55630 of 100000 left; aluminum_ore: richness 59, 441 of 30000 left; manganese_ore: richness 24, 4157 of 16000 left | none | 2026-11-17 08:42 UTC | `get_poi`, own ship |
| `kapteyn_5_weak_annihilation_zone` | Kapteyn 5 Weak Annihilation Zone | asteroid_belt | -- | iron_ore: richness 41, 366 of 100000 left; copper_ore: richness 20, 98746 of 100000 left; antimatter_containment_cell: richness 2, 71 of 163 left | none | 2026-11-17 08:42 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:42 UTC | own ship | Read Kapteyn 5 Belt: 74,890 units left in all | `get_poi`, own ship |
| 2026-11-17 08:42 UTC | own ship | Read Kapteyn 5 Weak Annihilation Zone: 99,183 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
