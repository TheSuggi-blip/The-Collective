---
name: albireo
id: 20261117T143525Z
tier: intel
author: Unity
kind: system
system_id: albireo
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Albireo

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where albireo`).

| Field | Value |
|---|---|
| Position | x 3829.1, y 3915.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | dawnbreak, fumalsamakah, gsc_0013, kornephoros, saclateni, the_rampart |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `albireo_star` | Albireo Star | sun (G5V) | -- | -- | none | 2026-11-17 14:07 UTC | `get_system`, own ship |
| `albireo_i` | Albireo I | planet (scorched) | -- | -- | none | 2026-11-17 14:07 UTC | `get_system`, own ship |
| `albireo_ii` | Albireo II | planet (arid) | -- | -- | none | 2026-11-17 14:07 UTC | `get_system`, own ship |
| `albireo_belt` | Albireo Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 14:07 UTC | `get_system`, own ship |
| `albireo_ice_fields` | Albireo Ice Fields | ice_field (kuiper) | -- | water_ice: richness 46, 39683 of 50000 left; nitrogen_ice: richness 30, 50000 of 50000 left; deuterium_ice: richness 17, 4997 of 5000 left | none | 2026-11-17 14:07 UTC | `get_poi`, own ship |
| `missed_veins` | Missed Veins | asteroid_belt | -- | not read | none | 2026-11-17 14:07 UTC | `get_system`, own ship |
| `albireo_fading_ember` | Albireo Fading Ember | asteroid_belt | -- | not read | none | 2026-11-17 14:07 UTC | `get_system`, own ship |

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
| 2026-11-17 14:07 UTC | own ship | Read Albireo Ice Fields: 94,680 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `albireo_belt`, `missed_veins`, `albireo_fading_ember`.
