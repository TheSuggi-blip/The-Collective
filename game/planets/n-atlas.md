---
name: atlas
id: 20261115T215317Z
tier: intel
author: Unity
kind: system
system_id: atlas
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Atlas

- system 6 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where atlas`).

| Field | Value |
|---|---|
| Position | x -2453.6, y 854.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 6 |
| Lanes | cedarhold, garnet, gsc_0044, hd_40307, intercrus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `atlas_star` | Atlas Star | sun (A0V) | -- | -- | none | 2026-11-15 21:40 UTC | `get_system`, own ship |
| `atlas_belt` | Atlas Belt | asteroid_belt (metallic) | -- | iron_ore: richness 66, 96354 of 100000 left; copper_ore: richness 20, 100000 of 100000 left | none | 2026-11-15 21:40 UTC | `get_poi`, own ship |
| `atlas_gas_pocket` | Atlas Gas Pocket | gas_cloud (molecular_cloud) | -- | plasma_gas: richness 34, 6671 of 10000 left; xenon_gas: richness 28, 9139 of 10000 left; nebula_gas: richness 17, 10000 of 10000 left; neon_gas: richness 51, 48528 of 50000 left | none | 2026-11-15 21:40 UTC | `get_poi`, own ship |
| `gossamer_null` | Gossamer Null | asteroid_belt | -- | iron_ore: richness 37, 100000 of 100000 left; copper_ore: richness 25, 100000 of 100000 left; null_matter: richness 11, 577 of 577 left | none | 2026-11-15 21:40 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:40 UTC | own ship | Read Atlas Belt: 196,354 units left in all | `get_poi`, own ship |
| 2026-11-15 21:40 UTC | own ship | Read Atlas Gas Pocket: 74,338 units left in all | `get_poi`, own ship |
| 2026-11-15 21:40 UTC | own ship | Read Gossamer Null: 200,577 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
