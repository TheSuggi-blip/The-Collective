---
name: praecipua
id: 20261117T123155Z
tier: intel
author: Unity
kind: system
system_id: praecipua
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Praecipua

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where praecipua`).

| Field | Value |
|---|---|
| Position | x 6614.9, y 1293.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | copperfield, taiyi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `praecipua_star` | Praecipua Star | sun (G2V) | -- | -- | none | 2026-11-17 12:05 UTC | `get_system`, own ship |
| `praecipua_i` | Praecipua I | planet (scorched) | -- | -- | none | 2026-11-17 12:05 UTC | `get_system`, own ship |
| `freshface_drift` | Freshface Drift | asteroid_belt | -- | aluminum_ore: richness 32, 2121 of 30000 left | none | 2026-11-17 12:05 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:05 UTC | own ship | Read Freshface Drift: 2,121 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
