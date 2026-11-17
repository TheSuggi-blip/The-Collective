---
name: daybreak
id: 20261117T143530Z
tier: intel
author: Unity
kind: system
system_id: daybreak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Daybreak

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where daybreak`).

| Field | Value |
|---|---|
| Position | x 5476.3, y -2008.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | gsc_0047, jabbah, lalande_21185, zubeneschamali |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `daybreak_star` | Daybreak Star | sun (K6V) | -- | -- | none | 2026-11-17 14:05 UTC | `get_system`, own ship |
| `daybreak_i` | Daybreak I | planet (scorched) | -- | -- | none | 2026-11-17 14:05 UTC | `get_system`, own ship |
| `daybreak_gas_cloud` | Daybreak Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 51, 1602 of 50000 left; argon_gas: richness 42, 1602 of 50000 left; nebula_gas: richness 19, 560 of 10000 left; neon_gas: richness 42, 1604 of 50000 left | none | 2026-11-17 14:05 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:05 UTC | own ship | Read Daybreak Gas Cloud: 5,368 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
