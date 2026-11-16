---
name: regor
id: 20261116T234002Z
tier: intel
author: Unity
kind: system
system_id: regor
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Regor

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where regor`).

| Field | Value |
|---|---|
| Position | x -5175.4, y 1956.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | atria, groombridge_34, marfik |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `regor_star` | Regor Star | sun (WR) | -- | -- | none | 2026-11-16 23:30 UTC | `get_system`, own ship |
| `regor_wr_bubble` | Regor WR Bubble | gas_cloud (emission) | -- | plasma_gas: richness 75, 7563 of 50000 left; ion_gas: richness 60, 7920 of 40000 left; nebula_gas: richness 45, 5907 of 30000 left; fluorine_gas: richness 25, 2893 of 15000 left | none | 2026-11-16 23:30 UTC | `get_poi`, own ship |
| `regor_inner_debris` | Regor Inner Debris | asteroid_belt (mixed) | -- | iron_ore: richness 40, 85 of 28000 left; titanium_ore: richness 30, 12 of 18000 left; vanadium_ore: richness 20, 54 of 10000 left | none | 2026-11-16 23:30 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:30 UTC | own ship | Read Regor WR Bubble: 24,283 units left in all | `get_poi`, own ship |
| 2026-11-16 23:30 UTC | own ship | Read Regor Inner Debris: 151 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
