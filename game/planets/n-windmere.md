---
name: windmere
id: 20261117T153802Z
tier: intel
author: Unity
kind: system
system_id: windmere
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 30
updated: 2026-11-17
---

# Windmere

Crimson system 22 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where windmere`).

| Field | Value |
|---|---|
| Position | x 6159.3, y 2722.8 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 22 |
| Lanes | 82_eridani, alzirr, frostfeld, muscida |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `windmere_star` | Windmere Star | sun (K3V) | -- | -- | none | 2026-11-17 14:41 UTC | `get_system`, own ship |
| `windmere_i` | Windmere I | planet (tundra) | -- | -- | none | 2026-11-17 14:41 UTC | `get_system`, own ship |
| `windmere_ii` | Windmere II | planet (glacial) | -- | -- | none | 2026-11-17 14:41 UTC | `get_system`, own ship |
| `windmere_iii` | Windmere III | planet (ice_world) | -- | -- | none | 2026-11-17 14:41 UTC | `get_system`, own ship |
| `windmere_iv` | Windmere IV | planet (ice_world) | -- | -- | none | 2026-11-17 14:41 UTC | `get_system`, own ship |
| `windmere_emission_nebula` | Windmere Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 53, 119 of 50000 left; argon_gas: richness 42, 47850 of 50000 left; nebula_gas: richness 13, 9999 of 10000 left; chlorine_gas: richness 19, 803 of 10000 left | none | 2026-11-17 14:41 UTC | `get_poi`, own ship |
| `windmere_war_metal_outcrop` | Windmere War Metal Outcrop | asteroid_belt | -- | iron_ore: richness 35, 280 of 100000 left; copper_ore: richness 20, 474 of 100000 left; darksteel_ore: richness 8, 26 of 501 left | none | 2026-11-17 14:41 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:41 UTC | own ship | Read Windmere Emission Nebula: 58,771 units left in all | `get_poi`, own ship |
| 2026-11-17 14:41 UTC | own ship | Read Windmere War Metal Outcrop: 780 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
