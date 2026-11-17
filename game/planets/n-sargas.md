---
name: sargas
id: 20261117T174150Z
tier: intel
author: Unity
kind: system
system_id: sargas
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sargas

- system 21 jumps from home, police level 0. Station: Cobalt Reach Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sargas`).

| Field | Value |
|---|---|
| Position | x 3980.8, y 593.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | 61_cygni, atik, larchfield, sunhaven |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sargas_star` | Sargas Star | sun (K6V) | -- | -- | none | 2026-11-17 17:00 UTC | `get_system`, own ship |
| `sargas_i` | Sargas I | planet (scorched) | -- | -- | none | 2026-11-17 17:00 UTC | `get_system`, own ship |
| `sargas_ii` | Sargas II | planet (arid) | -- | -- | none | 2026-11-17 17:00 UTC | `get_system`, own ship |
| `sargas_iii` | Sargas III | planet (terran) | -- | -- | none | 2026-11-17 17:00 UTC | `get_system`, own ship |
| `sargas_frost_ring` | Sargas Frost Ring | ice_field (kuiper) | -- | water_ice: richness 63, 41589 of 50000 left; nitrogen_ice: richness 46, 50000 of 50000 left; helium_ice: richness 11, 5000 of 5000 left | none | 2026-11-17 17:00 UTC | `get_poi`, own ship |
| `hearsay_cobalt` | Hearsay Cobalt | asteroid_belt | -- | iron_ore: richness 43, 99999 of 100000 left; copper_ore: richness 24, 100000 of 100000 left; cobalt_ore: richness 46, 3222 of 25000 left | none | 2026-11-17 17:00 UTC | `get_poi`, own ship |
| `572741d0cc03ee82057cb8af0031efca` | Cobalt Reach Range | station | `2efbd54d5db74153ec7fbc3da4fe7481` | -- | none | 2026-11-17 17:00 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Cobalt Reach Range (`2efbd54d5db74153ec7fbc3da4fe7481`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:00 UTC | `get_system`, own ship |

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
| 2026-11-17 17:00 UTC | own ship | Read Sargas Frost Ring: 96,589 units left in all | `get_poi`, own ship |
| 2026-11-17 17:00 UTC | own ship | Read Hearsay Cobalt: 203,221 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
