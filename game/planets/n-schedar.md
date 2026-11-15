---
name: schedar
id: 20261115T215328Z
tier: intel
author: Unity
kind: system
system_id: schedar
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Schedar

- system 2 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where schedar`).

| Field | Value |
|---|---|
| Position | x -4685.1, y 2802.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 2 |
| Lanes | gsc_0027, gsc_0050, node_beta |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `schedar_star` | Schedar Star | sun (K2V) | -- | -- | none | 2026-11-15 21:14 UTC | `get_system`, own ship |
| `schedar_i` | Schedar I | planet (scorched) | -- | -- | none | 2026-11-15 21:14 UTC | `get_system`, own ship |
| `schedar_ii` | Schedar II | planet (arid) | -- | -- | none | 2026-11-15 21:14 UTC | `get_system`, own ship |
| `schedar_iii` | Schedar III | planet (terran) | -- | -- | none | 2026-11-15 21:14 UTC | `get_system`, own ship |
| `schedar_iv` | Schedar IV | planet (jovian) | -- | -- | none | 2026-11-15 21:14 UTC | `get_system`, own ship |
| `schedar_belt` | Schedar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 57, 77048 of 100000 left; copper_ore: richness 44, 99984 of 100000 left | none | 2026-11-15 21:14 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 21:14 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:14 UTC | own ship | Read Schedar Belt: 177,032 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 21:14 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 5 (4 planets, 1 belt). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
