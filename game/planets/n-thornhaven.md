---
name: thornhaven
id: 20261115T215330Z
tier: intel
author: Unity
kind: system
system_id: thornhaven
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Thornhaven

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where thornhaven`).

| Field | Value |
|---|---|
| Position | x -3970.9, y 4290.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | achird, amberfall, hamal, megrez, okab, stormwatch |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `thornhaven_star` | Thornhaven Star | sun (M2V) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `thornhaven_i` | Thornhaven I | planet (scorched) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `thornhaven_ii` | Thornhaven II | planet (arid) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `dimming_pocket` | Dimming Pocket | nebula | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 21:49 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:49 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 21:49 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 3 (2 planets, 1 nebula). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
