---
name: saiph
id: 20261117T163949Z
tier: intel
author: Unity
kind: system
system_id: saiph
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Saiph

- system 16 jumps from home, police level 0. Station: Cryo Zenith.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where saiph`).

| Field | Value |
|---|---|
| Position | x 1875.7, y 5439.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | alpheratz, gsc_0010, gsc_0034, lilii_borea |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `saiph_star` | Saiph Star | sun (M2V) | -- | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |
| `saiph_i` | Saiph I | planet (scorched) | -- | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |
| `saiph_ii` | Saiph II | planet (arid) | -- | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |
| `saiph_iii` | Saiph III | planet (terran) | -- | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |
| `saiph_iv` | Saiph IV | planet (tundra) | -- | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |
| `saiph_v` | Saiph V | planet (glacial) | -- | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |
| `saiph_emission_nebula` | Saiph Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 63, 5929 of 50000 left; argon_gas: richness 35, 45550 of 50000 left; plasma_gas: richness 22, 7890 of 10000 left; nebula_gas: richness 21, 8653 of 10000 left; chlorine_gas: richness 30, 460 of 10000 left | none | 2026-11-17 15:43 UTC | `get_poi`, own ship |
| `saiph_frost_ring` | Saiph Frost Ring | ice_field (kuiper) | -- | water_ice: richness 51, 19311 of 50000 left; nitrogen_ice: richness 54, 19312 of 50000 left | none | 2026-11-17 15:43 UTC | `get_poi`, own ship |
| `f9a69fe2de7833d14270f634f46622ae` | Cryo Zenith | station | `0bf47c4aa0cb5fcea2d2ff20dac1729e` | -- | none | 2026-11-17 15:43 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Cryo Zenith (`0bf47c4aa0cb5fcea2d2ff20dac1729e`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 15:43 UTC | `get_system`, own ship |

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
| 2026-11-17 15:43 UTC | own ship | Read Saiph Emission Nebula: 68,482 units left in all | `get_poi`, own ship |
| 2026-11-17 15:43 UTC | own ship | Read Saiph Frost Ring: 38,623 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
