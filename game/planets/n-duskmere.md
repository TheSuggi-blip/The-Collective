---
name: duskmere
id: 20261117T153730Z
tier: intel
author: Unity
kind: system
system_id: duskmere
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Duskmere

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where duskmere`).

| Field | Value |
|---|---|
| Position | x 5134.2, y 329.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | dusthaven, edgewater, minkar, mothallah, toi_700 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `duskmere_star` | Duskmere Star | sun (G2V) | -- | -- | none | 2026-11-17 15:09 UTC | `get_system`, own ship |
| `duskmere_i` | Duskmere I | planet (scorched) | -- | -- | none | 2026-11-17 15:09 UTC | `get_system`, own ship |
| `duskmere_ii` | Duskmere II | planet (arid) | -- | -- | none | 2026-11-17 15:09 UTC | `get_system`, own ship |
| `duskmere_ice_belt` | Duskmere Ice Belt | ice_field (kuiper) | -- | water_ice: richness 41, 37698 of 50000 left; nitrogen_ice: richness 52, 50000 of 50000 left; deuterium_ice: richness 13, 4907 of 5000 left | none | 2026-11-17 15:09 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:09 UTC | own ship | Read Duskmere Ice Belt: 92,605 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
