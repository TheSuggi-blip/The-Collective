---
name: silverpine
id: 20261117T133404Z
tier: intel
author: Unity
kind: system
system_id: silverpine
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Silverpine

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where silverpine`).

| Field | Value |
|---|---|
| Position | x -3219.1, y -5907.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | ran, sarin, zavijava |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `silverpine_star` | Silverpine Star | sun (M2V) | -- | -- | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `silverpine_i` | Silverpine I | planet (scorched) | -- | -- | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `silverpine_gas_plume` | Silverpine Gas Plume | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `silverpine_cryobelt` | Silverpine Cryobelt | ice_field (cometary) | -- | not read | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `silverpine_played_out_reef` | Silverpine Played-Out Reef | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 13:03 UTC | `get_system`, own ship |

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
| 2026-11-17 13:03 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `silverpine_gas_plume`, `silverpine_cryobelt`, `silverpine_played_out_reef`.
