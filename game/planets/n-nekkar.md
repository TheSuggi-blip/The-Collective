---
name: nekkar
id: 20261117T174153Z
tier: intel
author: Unity
kind: system
system_id: nekkar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Nekkar

- system 20 jumps from home, police level 0. Station: Woodstock.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where nekkar`).

| Field | Value |
|---|---|
| Position | x 3096.9, y -2077.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | gsc_0039, segin, silvermark |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `nekkar_star` | Nekkar Star | sun (M2V) | -- | -- | none | 2026-11-17 16:48 UTC | `get_system`, own ship |
| `nekkar_i` | Nekkar I | planet (scorched) | -- | -- | none | 2026-11-17 16:48 UTC | `get_system`, own ship |
| `nekkar_ii` | Nekkar II | planet (arid) | -- | -- | none | 2026-11-17 16:48 UTC | `get_system`, own ship |
| `nekkar_iii` | Nekkar III | planet (terran) | -- | -- | none | 2026-11-17 16:48 UTC | `get_system`, own ship |
| `nekkar_iv` | Nekkar IV | planet (tundra) | -- | -- | none | 2026-11-17 16:48 UTC | `get_system`, own ship |
| `nekkar_v` | Nekkar V | planet (glacial) | -- | -- | none | 2026-11-17 16:48 UTC | `get_system`, own ship |
| `nekkar_belt` | Nekkar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 34, 98414 of 100000 left; copper_ore: richness 29, 99999 of 100000 left; gold_ore: richness 35, 540 of 25000 left | none | 2026-11-17 16:48 UTC | `get_poi`, own ship |
| `nekkar_frozen_drift` | Nekkar Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 50, 380 of 50000 left; nitrogen_ice: richness 32, 996 of 50000 left; deuterium_ice: richness 23, 455 of 5000 left | none | 2026-11-17 16:48 UTC | `get_poi`, own ship |
| `dull_spark_scatter` | Dull Spark Scatter | asteroid_belt | -- | iron_ore: richness 35, 100000 of 100000 left; copper_ore: richness 35, 99999 of 100000 left; trade_crystal: richness 24, 0 of 2600 left | none | 2026-11-17 16:48 UTC | `get_poi`, own ship |
| `c53d084dac95fe237185050bc5369795` | Woodstock | station | `01bad6afe17a96264def4e8066bad050` | -- | none | 2026-11-17 16:48 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Woodstock (`01bad6afe17a96264def4e8066bad050`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:48 UTC | `get_system`, own ship |

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
| 2026-11-17 16:48 UTC | own ship | Read Nekkar Belt: 198,953 units left in all | `get_poi`, own ship |
| 2026-11-17 16:48 UTC | own ship | Read Nekkar Frozen Drift: 1,831 units left in all | `get_poi`, own ship |
| 2026-11-17 16:48 UTC | own ship | Read Dull Spark Scatter: 199,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
