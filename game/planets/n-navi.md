---
name: navi
id: 20261117T123154Z
tier: intel
author: Unity
kind: system
system_id: navi
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Navi

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where navi`).

| Field | Value |
|---|---|
| Position | x -4527.2, y -5133.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | gsc_0003, heathwick, libertas, meridian, summervale |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `navi_star` | Navi Star | sun (M2V) | -- | -- | none | 2026-11-17 11:58 UTC | `get_system`, own ship |
| `navi_i` | Navi I | planet (scorched) | -- | -- | none | 2026-11-17 11:58 UTC | `get_system`, own ship |
| `navi_ii` | Navi II | planet (arid) | -- | -- | none | 2026-11-17 11:58 UTC | `get_system`, own ship |
| `navi_belt` | Navi Belt | asteroid_belt (metallic) | -- | iron_ore: richness 53, 99999 of 100000 left; copper_ore: richness 22, 99999 of 100000 left | none | 2026-11-17 11:58 UTC | `get_poi`, own ship |
| `navi_haze` | Navi Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 43, 12504 of 50000 left; argon_gas: richness 52, 49999 of 50000 left; xenon_gas: richness 21, 2434 of 10000 left; neon_gas: richness 65, 50000 of 50000 left | none | 2026-11-17 11:58 UTC | `get_poi`, own ship |
| `navi_ice_shelf` | Navi Ice Shelf | ice_field (kuiper) | -- | helium_ice: richness 11, 5000 of 5000 left | none | 2026-11-17 11:58 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:58 UTC | own ship | Read Navi Belt: 199,998 units left in all | `get_poi`, own ship |
| 2026-11-17 11:58 UTC | own ship | Read Navi Haze: 114,937 units left in all | `get_poi`, own ship |
| 2026-11-17 11:58 UTC | own ship | Read Navi Ice Shelf: 5,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
