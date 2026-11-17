---
name: caph
id: 20261117T153728Z
tier: intel
author: Unity
kind: system
system_id: caph
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Caph

Nebula system 22 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where caph`).

| Field | Value |
|---|---|
| Position | x 716.0, y -5551.8 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 22 |
| Lanes | alioth, gliese_436, helvetios, ogma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `caph_star` | Caph Star | sun (F2IV) | -- | -- | none | 2026-11-17 14:39 UTC | `get_system`, own ship |
| `caph_disk` | Caph Disk | asteroid_belt (mixed) | -- | iron_ore: richness 40, 6945 of 25000 left; copper_ore: richness 30, 17605 of 18000 left; aluminum_ore: richness 20, 5486 of 10000 left; prismatic_nebulite: richness 4, 9 of 200 left | none | 2026-11-17 14:39 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:39 UTC | own ship | Read Caph Disk: 30,045 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
