---
name: gacrux
id: 20261117T143533Z
tier: intel
author: Unity
kind: system
system_id: gacrux
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Gacrux

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gacrux`).

| Field | Value |
|---|---|
| Position | x 6513.7, y -2245.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | alsuhail, edasich, netherwick, paikauhale, tegmine |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `gacrux_star` | Gacrux Star | sun (M2V) | -- | -- | none | 2026-11-17 14:00 UTC | `get_system`, own ship |
| `gacrux_i` | Gacrux I | planet (scorched) | -- | -- | none | 2026-11-17 14:00 UTC | `get_system`, own ship |
| `gacrux_belt` | Gacrux Belt | asteroid_belt (metallic) | -- | iron_ore: richness 40, 100000 of 100000 left; copper_ore: richness 42, 100000 of 100000 left | none | 2026-11-17 14:00 UTC | `get_poi`, own ship |
| `gacrux_ice_belt` | Gacrux Ice Belt | ice_field (kuiper) | -- | water_ice: richness 45, 45394 of 50000 left; nitrogen_ice: richness 45, 50000 of 50000 left; helium_ice: richness 16, 5000 of 5000 left | none | 2026-11-17 14:00 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:00 UTC | own ship | Read Gacrux Belt: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 14:00 UTC | own ship | Read Gacrux Ice Belt: 100,394 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
