---
name: stillwater
id: 20261117T123204Z
tier: intel
author: Unity
kind: system
system_id: stillwater
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 55
updated: 2026-11-17
---

# Stillwater

Crimson system 19 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where stillwater`).

| Field | Value |
|---|---|
| Position | x 5144.4, y 3764.8 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 19 |
| Lanes | bharani, blood_forge, the_crucible, trappist_1, valor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `stillwater_star` | Stillwater Star | sun (K4V) | -- | -- | none | 2026-11-17 12:19 UTC | `get_system`, own ship |
| `stillwater_i` | Stillwater I | planet (tundra) | -- | -- | none | 2026-11-17 12:19 UTC | `get_system`, own ship |
| `stillwater_ii` | Stillwater II | planet (glacial) | -- | -- | none | 2026-11-17 12:19 UTC | `get_system`, own ship |
| `stillwater_iii` | Stillwater III | planet (ice_world) | -- | -- | none | 2026-11-17 12:19 UTC | `get_system`, own ship |
| `stillwater_belt` | Stillwater Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 43, 221 of 30000 left; platinum_ore: richness 18, 199 of 8000 left; iridium_ore: richness 25, 196 of 5000 left; uranium_ore: richness 12, 0 of 5000 left; lead_ore: richness 14, 350 of 20000 left | none | 2026-11-17 12:19 UTC | `get_poi`, own ship |
| `stillwater_emission_nebula` | Stillwater Emission Nebula | gas_cloud (emission) | -- | argon_gas: richness 45, 49999 of 50000 left; neon_gas: richness 34, 50000 of 50000 left; chlorine_gas: richness 16, 1729 of 10000 left | none | 2026-11-17 12:19 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:19 UTC | own ship | Read Stillwater Belt: 966 units left in all | `get_poi`, own ship |
| 2026-11-17 12:19 UTC | own ship | Read Stillwater Emission Nebula: 101,728 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
