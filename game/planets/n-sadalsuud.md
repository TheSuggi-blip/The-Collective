---
name: sadalsuud
id: 20261117T010831Z
tier: intel
author: Unity
kind: system
system_id: sadalsuud
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sadalsuud

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sadalsuud`).

| Field | Value |
|---|---|
| Position | x -6204.0, y 1379.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | aldebaran, duskfield, giausar, gsc_0040 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sadalsuud_star` | Sadalsuud Star | sun (M2V) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `sadalsuud_i` | Sadalsuud I | planet (scorched) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `sadalsuud_ii` | Sadalsuud II | planet (arid) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `sadalsuud_iii` | Sadalsuud III | planet (terran) | -- | -- | none | 2026-11-17 00:44 UTC | `get_system`, own ship |
| `sadalsuud_emission_nebula` | Sadalsuud Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 63, 50000 of 50000 left | none | 2026-11-17 00:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 00:44 UTC | own ship | Read Sadalsuud Emission Nebula: 50,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
