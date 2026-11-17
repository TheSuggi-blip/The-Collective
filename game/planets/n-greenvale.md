---
name: greenvale
id: 20261117T082532Z
tier: intel
author: Unity
kind: system
system_id: greenvale
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Greenvale

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where greenvale`).

| Field | Value |
|---|---|
| Position | x -1368.0, y 5478.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | alderamin, coppervale, etamin, pleione |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `greenvale_star` | Greenvale Star | sun (K4V) | -- | -- | none | 2026-11-17 08:22 UTC | `get_system`, own ship |
| `greenvale_ice_fields` | Greenvale Ice Fields | ice_field (kuiper) | -- | deuterium_ice: richness 13, 190 of 5000 left; tritium_ice: richness 11, 190 of 1100 left | none | 2026-11-17 08:22 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:22 UTC | own ship | Read Greenvale Ice Fields: 380 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
