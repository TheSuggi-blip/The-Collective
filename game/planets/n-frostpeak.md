---
name: frostpeak
id: 20261117T133338Z
tier: intel
author: Unity
kind: system
system_id: frostpeak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Frostpeak

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where frostpeak`).

| Field | Value |
|---|---|
| Position | x 47.4, y -3920.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | kurhah, maia, stonecrest, wazn |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `frostpeak_star` | Frostpeak Star | sun (M4V) | -- | -- | none | 2026-11-17 12:35 UTC | `get_system`, own ship |
| `frostpeak_i` | Frostpeak I | planet (scorched) | -- | -- | none | 2026-11-17 12:35 UTC | `get_system`, own ship |
| `frostpeak_ii` | Frostpeak II | planet (arid) | -- | -- | none | 2026-11-17 12:35 UTC | `get_system`, own ship |
| `unskimmed_belt` | Unskimmed Belt | asteroid_belt | -- | iron_ore: richness 26, 100000 of 100000 left; copper_ore: richness 29, 99994 of 100000 left; trade_crystal: richness 18, 59 of 2500 left | none | 2026-11-17 12:35 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:35 UTC | own ship | Read Unskimmed Belt: 200,053 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
