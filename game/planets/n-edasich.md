---
name: edasich
id: 20261117T143532Z
tier: intel
author: Unity
kind: system
system_id: edasich
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Edasich

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where edasich`).

| Field | Value |
|---|---|
| Position | x 6540.6, y -1910.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | alsuhail, gacrux, netherwick, tegmine |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `edasich_star` | Edasich Star | sun (K2III) | -- | -- | none | 2026-11-17 13:56 UTC | `get_system`, own ship |
| `edasich_b` | Edasich B | planet (jovian) | -- | -- | none | 2026-11-17 13:56 UTC | `get_system`, own ship |
| `edasich_ice_halo` | Edasich Ice Halo | ice_field (cometary) | -- | water_ice: richness 50, 40000 of 40000 left; nitrogen_ice: richness 35, 25000 of 25000 left; helium_ice: richness 15, 8000 of 8000 left | none | 2026-11-17 13:56 UTC | `get_poi`, own ship |
| `stormward_silicon` | Stormward Silicon | asteroid_belt | -- | silicon_ore: richness 37, 4545 of 20000 left | none | 2026-11-17 13:56 UTC | `get_poi`, own ship |
| `sys_0063_poi_0` | Edasich | sun | -- | -- | none | 2026-11-17 13:56 UTC | `get_system`, own ship |

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
| 2026-11-17 13:56 UTC | own ship | Read Edasich Ice Halo: 73,000 units left in all | `get_poi`, own ship |
| 2026-11-17 13:56 UTC | own ship | Read Stormward Silicon: 4,545 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
