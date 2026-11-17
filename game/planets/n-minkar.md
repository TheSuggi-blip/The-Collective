---
name: minkar
id: 20261117T153748Z
tier: intel
author: Unity
kind: system
system_id: minkar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Minkar

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where minkar`).

| Field | Value |
|---|---|
| Position | x 4739.8, y 600.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | 61_cygni, atik, duskmere, mothallah, muphrid, sunhaven |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `minkar_star` | Minkar Star | sun (K2V) | -- | -- | none | 2026-11-17 14:49 UTC | `get_system`, own ship |
| `minkar_i` | Minkar I | planet (scorched) | -- | -- | none | 2026-11-17 14:49 UTC | `get_system`, own ship |
| `minkar_ii` | Minkar II | planet (arid) | -- | -- | none | 2026-11-17 14:49 UTC | `get_system`, own ship |
| `minkar_belt` | Minkar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 52, 99999 of 100000 left; copper_ore: richness 44, 100000 of 100000 left | none | 2026-11-17 14:49 UTC | `get_poi`, own ship |
| `minkar_haze` | Minkar Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 52, 17265 of 50000 left; neon_gas: richness 48, 49997 of 50000 left | none | 2026-11-17 14:49 UTC | `get_poi`, own ship |
| `minkar_cryobelt` | Minkar Cryobelt | ice_field (kuiper) | -- | water_ice: richness 48, 43835 of 50000 left; nitrogen_ice: richness 50, 50000 of 50000 left; deuterium_ice: richness 24, 2879 of 5000 left | none | 2026-11-17 14:49 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:49 UTC | own ship | Read Minkar Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 14:49 UTC | own ship | Read Minkar Haze: 67,262 units left in all | `get_poi`, own ship |
| 2026-11-17 14:49 UTC | own ship | Read Minkar Cryobelt: 96,714 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
