---
name: bunda
id: 20261117T184419Z
tier: intel
author: Unity
kind: system
system_id: bunda
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Bunda

Nebula system 19 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where bunda`).

| Field | Value |
|---|---|
| Position | x 2007.8, y -3445.4 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 19 |
| Lanes | alrakis, cargo_lanes, copernicus, gold_run |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `bunda_star` | Bunda Star | sun (K5V) | -- | -- | none | 2026-11-17 18:25 UTC | `get_system`, own ship |
| `bunda_i` | Bunda I | planet (tundra) | -- | -- | none | 2026-11-17 18:25 UTC | `get_system`, own ship |
| `bunda_belt` | Bunda Belt | asteroid_belt (carbonaceous) | -- | carbon_ore: richness 52, 268 of 30000 left; vanadium_ore: richness 48, 119 of 25000 left; tungsten_ore: richness 29, 136 of 25000 left; platinum_ore: richness 12, 158 of 8000 left; thorium_ore: richness 15, 0 of 5000 left; prismatic_nebulite: richness 4, 87 of 250 left | none | 2026-11-17 18:25 UTC | `get_poi`, own ship |
| `bunda_gas_cloud` | Bunda Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 49, 6344 of 50000 left; argon_gas: richness 33, 6341 of 50000 left; plasma_gas: richness 22, 1506 of 10000 left; neon_gas: richness 38, 6338 of 50000 left | none | 2026-11-17 18:25 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 18:25 UTC | own ship | Read Bunda Belt: 768 units left in all | `get_poi`, own ship |
| 2026-11-17 18:25 UTC | own ship | Read Bunda Gas Cloud: 20,529 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
