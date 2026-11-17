---
name: bharani
id: 20261117T123132Z
tier: intel
author: Unity
kind: system
system_id: bharani
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 55
updated: 2026-11-17
---

# Bharani

Crimson system 19 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where bharani`).

| Field | Value |
|---|---|
| Position | x 4884.9, y 3812.4 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 19 |
| Lanes | stillwater, the_crucible, trappist_1, valor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `bharani_star` | Bharani Star | sun (B8V) | -- | -- | none | 2026-11-17 12:18 UTC | `get_system`, own ship |
| `bharani_i` | Bharani I | planet (scorched) | -- | -- | none | 2026-11-17 12:18 UTC | `get_system`, own ship |
| `bharani_ii` | Bharani II | planet (scorched) | -- | -- | none | 2026-11-17 12:18 UTC | `get_system`, own ship |
| `crimson_signal_outpost_remnants` | Crimson Signal Outpost Remnants | relic (derelict) | -- | -- | none | 2026-11-17 12:18 UTC | `get_system`, own ship |
| `bharani_ember_field` | Bharani Ember Field | asteroid_belt | -- | iron_ore: richness 44, 10 of 100000 left; copper_ore: richness 27, 28047 of 100000 left; plasma_residue: richness 15, 1 of 1449 left | none | 2026-11-17 12:18 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 12:18 UTC | own ship | Read Bharani Ember Field: 28,058 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
