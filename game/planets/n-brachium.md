---
name: brachium
id: 20261115T225416Z
tier: intel
author: Unity
kind: system
system_id: brachium
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Brachium

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where brachium`).

| Field | Value |
|---|---|
| Position | x -5561.4, y 3106.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | denebola, gsc_0049, gsc_0050, miram, nightveil |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `brachium_star` | Brachium Star | sun (F8V) | -- | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |
| `brachium_i` | Brachium I | planet (scorched) | -- | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |
| `brachium_ii` | Brachium II | planet (arid) | -- | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |
| `brachium_iii` | Brachium III | planet (terran) | -- | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |
| `brachium_iv` | Brachium IV | planet (tundra) | -- | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |
| `brachium_v` | Brachium V | planet (glacial) | -- | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 22:01 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 22:01 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 22:01 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 5 (5 planets). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
