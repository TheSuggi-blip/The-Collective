---
name: pherkad
id: 20261115T142803Z
tier: intel
author: Unity
kind: system
system_id: pherkad
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 30
updated: 2026-11-15
---

# Pherkad

Voidborn system 3 jumps from home, police level 30. No station on the chart.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where pherkad`).

| Field | Value |
|---|---|
| Position | x -2710.6, y 2477.9 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 3 |
| Lanes | gsc_0041, ironhollow, shaula, synchrony, wolf_1061 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `pherkad_star` | Pherkad Star | sun (K5III) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `pherkad_i` | Pherkad I | planet (arid) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `pherkad_ii` | Pherkad II | planet (tundra) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `pherkad_iii` | Pherkad III | planet (glacial) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `sidelong_nebula` | Sidelong Nebula | nebula | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `pherkad_null_rift` | Pherkad Null Rift | asteroid_belt | -- | iron_ore: richness 31, 43423 of 100000 left; copper_ore: richness 24, 100000 of 100000 left; null_matter: richness 19, 458 of 889 left | none | 2026-11-15 13:12 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | ally | Unity | Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 13:12 UTC | own ship | Read Pherkad Null Rift: 143,881 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
