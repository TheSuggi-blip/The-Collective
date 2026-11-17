---
name: 61_cygni
id: 20261117T133323Z
tier: intel
author: Unity
kind: system
system_id: 61_cygni
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# 61 Cygni

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where 61_cygni`).

| Field | Value |
|---|---|
| Position | x 4331.8, y 848.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | alsephina, larchfield, minkar, muphrid, sargas, sunhaven, zubenelgenubi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `61_cygni_star` | 61 Cygni Star | sun (M2V) | -- | -- | none | 2026-11-17 13:14 UTC | `get_system`, own ship |
| `61_cygni_i` | 61 Cygni I | planet (scorched) | -- | -- | none | 2026-11-17 13:14 UTC | `get_system`, own ship |
| `61_cygni_ii` | 61 Cygni II | planet (arid) | -- | -- | none | 2026-11-17 13:14 UTC | `get_system`, own ship |
| `61_cygni_cryobelt` | 61 Cygni Cryobelt | ice_field (kuiper) | -- | nitrogen_ice: richness 52, 50000 of 50000 left; helium_ice: richness 17, 5000 of 5000 left | none | 2026-11-17 13:14 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:14 UTC | own ship | Read 61 Cygni Cryobelt: 55,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
