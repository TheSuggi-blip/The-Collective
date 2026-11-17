---
name: diphda
id: 20261117T143531Z
tier: intel
author: Unity
kind: system
system_id: diphda
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Diphda

- system 16 jumps from home, police level 0. Station: The Hush Chamber, Goldcrest Moon.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where diphda`).

| Field | Value |
|---|---|
| Position | x 2713.1, y 5206.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | alpheratz, arneb, crosshaven, gsc_0019, thuban, tiaki |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `diphda_star` | Diphda Star | sun (M2V) | -- | -- | none | 2026-11-17 14:15 UTC | `get_system`, own ship |
| `diphda_i` | Diphda I | planet (scorched) | -- | -- | none | 2026-11-17 14:15 UTC | `get_system`, own ship |
| `hullfrost_drift` | Hullfrost Drift | asteroid_belt | -- | silicon_ore: richness 44, 114 of 20000 left; neodymium_ore: richness 15, 57 of 5500 left | none | 2026-11-17 14:15 UTC | `get_poi`, own ship |
| `2574b16e0e18d90b98354bcae963854e` | The Hush Chamber | station | `d1f995a17a22b127c5aa249c672b8db0` | -- | none | 2026-11-17 14:15 UTC | `get_system`, own ship |
| `moon_foundation` | Goldcrest Moon | station | `moon_foundation` | -- | none | 2026-11-17 14:15 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Hush Chamber (`d1f995a17a22b127c5aa249c672b8db0`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:15 UTC | `get_system`, own ship |
| Goldcrest Moon (`moon_foundation`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:15 UTC | `get_system`, own ship |

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
| 2026-11-17 14:15 UTC | own ship | Read Hullfrost Drift: 171 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
