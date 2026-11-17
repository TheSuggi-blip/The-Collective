---
name: sceptrum
id: 20261117T133403Z
tier: intel
author: Unity
kind: system
system_id: sceptrum
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sceptrum

- system 27 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sceptrum`).

| Field | Value |
|---|---|
| Position | x 6724.4, y -342.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 27 |
| Lanes | bellatrix, gsc_0007, redmarsh |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sceptrum_star` | Sceptrum Star | sun (G5III) | -- | -- | none | 2026-11-17 12:48 UTC | `get_system`, own ship |
| `sceptrum_i` | Sceptrum I | planet (scorched) | -- | -- | none | 2026-11-17 12:48 UTC | `get_system`, own ship |
| `sceptrum_ii` | Sceptrum II | planet (arid) | -- | -- | none | 2026-11-17 12:48 UTC | `get_system`, own ship |
| `slack_claims_belt` | Slack Claims Belt | asteroid_belt | -- | carbon_ore: richness 31, 1664 of 30000 left | none | 2026-11-17 12:48 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:48 UTC | own ship | Read Slack Claims Belt: 1,664 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
