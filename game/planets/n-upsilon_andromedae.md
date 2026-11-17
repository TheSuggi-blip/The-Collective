---
name: upsilon_andromedae
id: 20261117T174142Z
tier: intel
author: Unity
kind: system
system_id: upsilon_andromedae
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Upsilon Andromedae

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where upsilon_andromedae`).

| Field | Value |
|---|---|
| Position | x 4314.7, y -1686.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | gsc_0011, gsc_0018, kepler_62, lalande_21185, silvermark |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `upsilon_andromedae_star` | Upsilon Andromedae Star | sun (K4V) | -- | -- | none | 2026-11-17 16:45 UTC | `get_system`, own ship |
| `upsilon_andromedae_ice_belt` | Upsilon Andromedae Ice Belt | ice_field (kuiper) | -- | nitrogen_ice: richness 36, 1438 of 50000 left; deuterium_ice: richness 15, 527 of 5000 left; tritium_ice: richness 9, 451 of 900 left; helium_ice: richness 19, 525 of 5000 left | none | 2026-11-17 16:45 UTC | `get_poi`, own ship |
| `wh_exit_c1577477` | Collapsed Wormhole | wormhole_collapsed | -- | -- | none | 2026-11-17 16:45 UTC | `get_system`, own ship |

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
| 2026-11-17 16:45 UTC | own ship | Read Upsilon Andromedae Ice Belt: 2,941 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
