---
name: cloverfield
id: 20261117T184418Z
tier: intel
author: Unity
kind: system
system_id: cloverfield
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Cloverfield

- system 19 jumps from home, police level 0. Station: Conjunction Junction.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where cloverfield`).

| Field | Value |
|---|---|
| Position | x -809.4, y -3764.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | cocibolca, driftwood, wazn, zosma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `cloverfield_star` | Cloverfield Star | sun (K4V) | -- | -- | none | 2026-11-17 18:14 UTC | `get_system`, own ship |
| `cloverfield_i` | Cloverfield I | planet (scorched) | -- | -- | none | 2026-11-17 18:14 UTC | `get_system`, own ship |
| `cloverfield_ii` | Cloverfield II | planet (arid) | -- | -- | none | 2026-11-17 18:14 UTC | `get_system`, own ship |
| `cloverfield_iii` | Cloverfield III | planet (terran) | -- | -- | none | 2026-11-17 18:14 UTC | `get_system`, own ship |
| `cloverfield_iv` | Cloverfield IV | planet (jovian) | -- | -- | none | 2026-11-17 18:14 UTC | `get_system`, own ship |
| `cloverfield_belt` | Cloverfield Belt | asteroid_belt (metallic) | -- | iron_ore: richness 30, 134 of 100000 left; copper_ore: richness 32, 133 of 100000 left; zinc_ore: richness 21, 109 of 18000 left | none | 2026-11-17 18:14 UTC | `get_poi`, own ship |
| `cloverfield_gas_plume` | Cloverfield Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 59, 0 of 50000 left; plasma_gas: richness 30, 0 of 10000 left; nebula_gas: richness 15, 0 of 10000 left; neon_gas: richness 47, 0 of 50000 left; chlorine_gas: richness 29, 0 of 10000 left; fluorine_gas: richness 11, 0 of 5000 left | none | 2026-11-17 18:14 UTC | `get_poi`, own ship |
| `cloverfield_frozen_drift` | Cloverfield Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 63, 759 of 50000 left; nitrogen_ice: richness 40, 50000 of 50000 left; ammonia_ice: richness 15, 6107 of 7000 left | none | 2026-11-17 18:14 UTC | `get_poi`, own ship |
| `shy_spark_nebula` | Shy Spark Nebula | nebula | -- | -- | none | 2026-11-17 18:14 UTC | `get_system`, own ship |
| `862e07fa76571d0a76cab3cbaf4046e7` | Conjunction Junction | station | `c976fa7df53c87f9616165d7d411b41a` | -- | none | 2026-11-17 18:14 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Conjunction Junction (`c976fa7df53c87f9616165d7d411b41a`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 18:14 UTC | `get_system`, own ship |

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
| 2026-11-17 18:14 UTC | own ship | Read Cloverfield Belt: 376 units left in all | `get_poi`, own ship |
| 2026-11-17 18:14 UTC | own ship | Read Cloverfield Gas Plume: nothing left | `get_poi`, own ship |
| 2026-11-17 18:14 UTC | own ship | Read Cloverfield Frozen Drift: 56,866 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
