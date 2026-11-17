---
name: barnard_77
id: 20261117T163925Z
tier: intel
author: Unity
kind: system
system_id: barnard_77
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Barnard 77

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where barnard_77`).

| Field | Value |
|---|---|
| Position | x 3669.5, y -3003.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | graffias, tianyi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `barnard_77_belt` | Barnard 77 Belt | asteroid_belt (metallic) | -- | iron_ore: richness 45, 99999 of 100000 left; copper_ore: richness 34, 100000 of 100000 left | none | 2026-11-17 16:14 UTC | `get_poi`, own ship |
| `barnard_77_haze` | Barnard 77 Haze | gas_cloud (molecular_cloud) | -- | argon_gas: richness 44, 49999 of 50000 left; neon_gas: richness 49, 50000 of 50000 left | none | 2026-11-17 16:14 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:14 UTC | own ship | Read Barnard 77 Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 16:14 UTC | own ship | Read Barnard 77 Haze: 99,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
