---
name: alshain
id: 20261117T102824Z
tier: intel
author: Unity
kind: system
system_id: alshain
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alshain

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alshain`).

| Field | Value |
|---|---|
| Position | x 1244.8, y 3712.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | chara, mebsuta, phecda, porrima, westmark |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alshain_star` | Alshain Star | sun (K6V) | -- | -- | none | 2026-11-17 09:56 UTC | `get_system`, own ship |
| `alshain_i` | Alshain I | planet (scorched) | -- | -- | none | 2026-11-17 09:56 UTC | `get_system`, own ship |
| `alshain_ii` | Alshain II | planet (arid) | -- | -- | none | 2026-11-17 09:56 UTC | `get_system`, own ship |
| `alshain_ice_fields` | Alshain Ice Fields | ice_field (kuiper) | -- | water_ice: richness 45, 44837 of 50000 left; deuterium_ice: richness 23, 2877 of 5000 left; oxygen_ice: richness 10, 3000 of 3000 left | none | 2026-11-17 09:56 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:56 UTC | own ship | Read Alshain Ice Fields: 50,714 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
