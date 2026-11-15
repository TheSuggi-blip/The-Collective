---
name: intercrus
id: 20261115T215323Z
tier: intel
author: Unity
kind: system
system_id: intercrus
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Intercrus

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where intercrus`).

| Field | Value |
|---|---|
| Position | x -2183.3, y 413.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | atlas, botein, diadem, gsc_0044, kitalpha |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `intercrus_belt` | Intercrus Belt | asteroid_belt (metallic) | -- | iron_ore: richness 43, 99997 of 100000 left; copper_ore: richness 46, 99999 of 100000 left | none | 2026-11-15 21:41 UTC | `get_poi`, own ship |
| `intercrus_ice_fields` | Intercrus Ice Fields | ice_field (cometary) | -- | water_ice: richness 47, 50000 of 50000 left; nitrogen_ice: richness 42, 50000 of 50000 left | none | 2026-11-15 21:41 UTC | `get_poi`, own ship |
| `intercrus_alloy_remnants` | Intercrus Alloy Remnants | asteroid_belt | -- | iron_ore: richness 45, 100000 of 100000 left; copper_ore: richness 20, 100000 of 100000 left; sol_alloy_ore: richness 5, 1401 of 1401 left | none | 2026-11-15 21:41 UTC | `get_poi`, own ship |
| `sootfall_belt` | Sootfall Belt | asteroid_belt | -- | iron_ore: richness 32, 100000 of 100000 left; copper_ore: richness 26, 100000 of 100000 left; null_matter: richness 11, 650 of 650 left | none | 2026-11-15 21:41 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 21:41 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:41 UTC | own ship | Read Intercrus Belt: 199,996 units left in all | `get_poi`, own ship |
| 2026-11-15 21:41 UTC | own ship | Read Intercrus Ice Fields: 100,000 units left in all | `get_poi`, own ship |
| 2026-11-15 21:41 UTC | own ship | Read Intercrus Alloy Remnants: 201,401 units left in all | `get_poi`, own ship |
| 2026-11-15 21:41 UTC | own ship | Read Sootfall Belt: 200,650 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 21:41 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 4 (3 belts, 1 ice field). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
