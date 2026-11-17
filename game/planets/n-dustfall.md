---
name: dustfall
id: 20261117T123136Z
tier: intel
author: Unity
kind: system
system_id: dustfall
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Dustfall

- system 27 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where dustfall`).

| Field | Value |
|---|---|
| Position | x -2064.3, y -6230.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 27 |
| Lanes | toi_2257, xamidimura |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dustfall_star` | Dustfall Star | sun (G5V) | -- | -- | none | 2026-11-17 12:29 UTC | `get_system`, own ship |
| `dustfall_i` | Dustfall I | planet (scorched) | -- | -- | none | 2026-11-17 12:29 UTC | `get_system`, own ship |
| `dustfall_emission_nebula` | Dustfall Emission Nebula | gas_cloud (emission) | -- | not read | none | 2026-11-17 12:29 UTC | `get_system`, own ship |
| `dustfall_frozen_drift` | Dustfall Frozen Drift | ice_field (kuiper) | -- | nitrogen_ice: richness 50, 50000 of 50000 left; helium_ice: richness 16, 5000 of 5000 left | none | 2026-11-17 12:29 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:29 UTC | own ship | Read Dustfall Frozen Drift: 55,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `dustfall_emission_nebula`.
