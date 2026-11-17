---
name: foxglove
id: 20261117T133337Z
tier: intel
author: Unity
kind: system
system_id: foxglove
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Foxglove

- system 28 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where foxglove`).

| Field | Value |
|---|---|
| Position | x 4988.2, y -3036.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 28 |
| Lanes | inquill, ironveil, sadr |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `foxglove_star` | Foxglove Star | sun (F8V) | -- | -- | none | 2026-11-17 12:47 UTC | `get_system`, own ship |
| `foxglove_i` | Foxglove I | planet (scorched) | -- | -- | none | 2026-11-17 12:47 UTC | `get_system`, own ship |
| `foxglove_belt` | Foxglove Belt | asteroid_belt (metallic) | -- | iron_ore: richness 53, 100000 of 100000 left; copper_ore: richness 45, 100000 of 100000 left; lithium_ore: richness 28, 25000 of 25000 left | none | 2026-11-17 12:47 UTC | `get_poi`, own ship |
| `foxglove_gas_plume` | Foxglove Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 41, 35455 of 50000 left; argon_gas: richness 48, 50000 of 50000 left; xenon_gas: richness 20, 6961 of 10000 left; neon_gas: richness 48, 50000 of 50000 left; chlorine_gas: richness 25, 4629 of 10000 left; fluorine_gas: richness 12, 3913 of 5000 left | none | 2026-11-17 12:47 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:47 UTC | own ship | Read Foxglove Belt: 225,000 units left in all | `get_poi`, own ship |
| 2026-11-17 12:47 UTC | own ship | Read Foxglove Gas Plume: 150,958 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
