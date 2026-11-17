---
name: vega
id: 20261117T143556Z
tier: intel
author: Unity
kind: system
system_id: vega
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Vega

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where vega`).

| Field | Value |
|---|---|
| Position | x 5664.8, y -1251.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | jabbah, northwick, vindemiatrix, zubeneschamali |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `vega_star` | Vega Star | sun (M4V) | -- | -- | none | 2026-11-17 14:05 UTC | `get_system`, own ship |
| `vega_cryobelt` | Vega Cryobelt | ice_field (kuiper) | -- | water_ice: richness 61, 47409 of 50000 left; deuterium_ice: richness 24, 4633 of 5000 left; helium_ice: richness 21, 4917 of 5000 left | none | 2026-11-17 14:05 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:05 UTC | own ship | Read Vega Cryobelt: 56,959 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
