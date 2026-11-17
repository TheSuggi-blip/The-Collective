---
name: oxbow
id: 20261117T021124Z
tier: intel
author: Unity
kind: system
system_id: oxbow
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Oxbow

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where oxbow`).

| Field | Value |
|---|---|
| Position | x -6254.7, y -1062.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | chertan, gsc_0004, gsc_0043, gsc_0045, hawthorne, springdale |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `oxbow_star` | Oxbow Star | sun (M2V) | -- | -- | none | 2026-11-17 01:21 UTC | `get_system`, own ship |
| `oxbow_i` | Oxbow I | planet (scorched) | -- | -- | none | 2026-11-17 01:21 UTC | `get_system`, own ship |
| `oxbow_belt_a` | Oxbow Belt A | asteroid_belt (metallic) | -- | iron_ore: richness 68, 99997 of 100000 left; copper_ore: richness 27, 99999 of 100000 left | none | 2026-11-17 01:21 UTC | `get_poi`, own ship |
| `oxbow_belt_b` | Oxbow Belt B | asteroid_belt (metallic) | -- | iron_ore: richness 53, 100000 of 100000 left; copper_ore: richness 23, 100000 of 100000 left | none | 2026-11-17 01:21 UTC | `get_poi`, own ship |
| `oxbow_ice_belt` | Oxbow Ice Belt | ice_field (kuiper) | -- | water_ice: richness 52, 35912 of 50000 left; deuterium_ice: richness 19, 3592 of 5000 left; helium_ice: richness 18, 3635 of 5000 left | none | 2026-11-17 01:21 UTC | `get_poi`, own ship |

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
| 2026-11-17 01:21 UTC | own ship | Read Oxbow Belt A: 199,996 units left in all | `get_poi`, own ship |
| 2026-11-17 01:21 UTC | own ship | Read Oxbow Belt B: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 01:21 UTC | own ship | Read Oxbow Ice Belt: 43,139 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
