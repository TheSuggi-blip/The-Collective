---
name: frostfeld
id: 20261117T174208Z
tier: intel
author: Unity
kind: system
system_id: frostfeld
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 55
updated: 2026-11-17
---

# Frostfeld

Crimson system 21 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where frostfeld`).

| Field | Value |
|---|---|
| Position | x 5642.4, y 2496.8 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 21 |
| Lanes | 82_eridani, alzirr, gsc_0036, hd_20794, ironhearth, muscida, the_anvil, windmere |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `the_pale` | The Pale | sun (DA) | -- | -- | none | 2026-11-17 16:38 UTC | `get_system`, own ship |
| `frostfeld_i` | Frostfeld I | planet (ice_world) | -- | -- | none | 2026-11-17 16:38 UTC | `get_system`, own ship |
| `frostfeld_ii` | Frostfeld II | planet (ice_world) | -- | -- | none | 2026-11-17 16:38 UTC | `get_system`, own ship |
| `frostfeld_ice_flats` | Frostfeld Ice Flats | ice_field (kuiper) | -- | water_ice: richness 55, 86 of 50000 left; nitrogen_ice: richness 45, 104 of 50000 left; oxygen_ice: richness 12, 546 of 4000 left | none | 2026-11-17 16:38 UTC | `get_poi`, own ship |
| `smiths_detour` | Smith's Detour | asteroid_belt | -- | iron_ore: richness 28, 2960 of 100000 left; copper_ore: richness 21, 5156 of 100000 left; darksteel_ore: richness 10, 1 of 520 left | none | 2026-11-17 16:38 UTC | `get_poi`, own ship |
| `frostfeld_thermal_vent` | Frostfeld Thermal Vent | asteroid_belt | -- | iron_ore: richness 27, 1683 of 100000 left; copper_ore: richness 32, 360 of 100000 left; plasma_residue: richness 17, 6 of 1486 left | none | 2026-11-17 16:38 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 16:38 UTC | own ship | Read Frostfeld Ice Flats: 736 units left in all | `get_poi`, own ship |
| 2026-11-17 16:38 UTC | own ship | Read Smith's Detour: 8,117 units left in all | `get_poi`, own ship |
| 2026-11-17 16:38 UTC | own ship | Read Frostfeld Thermal Vent: 2,049 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
