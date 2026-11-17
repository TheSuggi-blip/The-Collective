---
name: ran
id: 20261117T133357Z
tier: intel
author: Unity
kind: system
system_id: ran
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ran

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ran`).

| Field | Value |
|---|---|
| Position | x -2827.8, y -6352.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | silverpine, toi_2257, zavijava |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ran_star` | Ran Star | sun (M2V) | -- | -- | none | 2026-11-17 12:35 UTC | `get_system`, own ship |
| `ran_i` | Ran I | planet (scorched) | -- | -- | none | 2026-11-17 12:35 UTC | `get_system`, own ship |
| `ran_ii` | Ran II | planet (arid) | -- | -- | none | 2026-11-17 12:35 UTC | `get_system`, own ship |
| `ran_belt` | Ran Belt | asteroid_belt (metallic) | -- | iron_ore: richness 47, 99999 of 100000 left; copper_ore: richness 23, 100000 of 100000 left; zinc_ore: richness 26, 22000 of 22000 left | none | 2026-11-17 12:35 UTC | `get_poi`, own ship |
| `ran_haze` | Ran Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 69, 50000 of 50000 left; argon_gas: richness 37, 50000 of 50000 left; chlorine_gas: richness 36, 10000 of 10000 left; krypton_gas: richness 16, 5000 of 5000 left | none | 2026-11-17 12:35 UTC | `get_poi`, own ship |
| `ran_frost_ring` | Ran Frost Ring | ice_field (kuiper) | -- | water_ice: richness 41, 32198 of 50000 left; helium_ice: richness 20, 1162 of 5000 left | none | 2026-11-17 12:35 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:35 UTC | own ship | Read Ran Belt: 221,999 units left in all | `get_poi`, own ship |
| 2026-11-17 12:35 UTC | own ship | Read Ran Haze: 115,000 units left in all | `get_poi`, own ship |
| 2026-11-17 12:35 UTC | own ship | Read Ran Frost Ring: 33,360 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
