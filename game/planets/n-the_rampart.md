---
name: the_rampart
id: 20261117T123209Z
tier: intel
author: Unity
kind: system
system_id: the_rampart
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 30
updated: 2026-11-17
---

# The Rampart

Crimson system 17 jumps from home, police level 30. Station: The Rampart Checkpoint.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where the_rampart`).

| Field | Value |
|---|---|
| Position | x 4030.4, y 3777.1 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 17 |
| Lanes | albireo, dawnbreak, gsc_0013, saclateni, the_crucible |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `the_sentinel` | The Sentinel | sun (A2V) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rampart_i` | Rampart I | planet (scorched) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rampart_ii` | Rampart II | planet (arid) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rampart_iii` | Rampart III | planet (tundra) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rampart_iv` | Rampart IV | planet (glacial) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `the_rampart_checkpoint` | The Rampart Checkpoint | station | `the_rampart_checkpoint` | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Rampart Checkpoint (`the_rampart_checkpoint`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 12:12 UTC | `get_system`, own ship |

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
| 2026-11-17 12:12 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
