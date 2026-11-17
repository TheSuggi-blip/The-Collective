---
name: elnath
id: 20261117T041727Z
tier: intel
author: Unity
kind: system
system_id: elnath
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Elnath

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where elnath`).

| Field | Value |
|---|---|
| Position | x -2152.9, y 5514.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | biham, coppervale, gsc_0035, sualocin |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `elnath_star` | Elnath Star | sun (K2V) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `elnath_i` | Elnath I | planet (scorched) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `elnath_ii` | Elnath II | planet (arid) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `elnath_belt` | Elnath Belt | asteroid_belt (metallic) | -- | iron_ore: richness 63, 100000 of 100000 left; copper_ore: richness 37, 100000 of 100000 left; silver_ore: richness 38, 34 of 25000 left; zinc_ore: richness 16, 10000 of 10000 left | none | 2026-11-17 04:00 UTC | `get_poi`, own ship |
| `elnath_ice_belt` | Elnath Ice Belt | ice_field (kuiper) | -- | water_ice: richness 49, 49410 of 50000 left; nitrogen_ice: richness 52, 50000 of 50000 left | none | 2026-11-17 04:00 UTC | `get_poi`, own ship |

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
| 2026-11-17 04:00 UTC | own ship | Read Elnath Belt: 210,034 units left in all | `get_poi`, own ship |
| 2026-11-17 04:00 UTC | own ship | Read Elnath Ice Belt: 99,410 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
