---
name: alnair
id: 20261115T215316Z
tier: intel
author: Unity
kind: system
system_id: alnair
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Alnair

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alnair`).

| Field | Value |
|---|---|
| Position | x -1894.7, y 3154.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | shaula, wolf_1061 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alnair_star` | Alnair Star | sun (M2V) | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |
| `alnair_i` | Alnair I | planet (scorched) | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |
| `alnair_ii` | Alnair II | planet (arid) | -- | -- | none | 2026-11-15 21:51 UTC | `get_system`, own ship |
| `alnair_ice_fields` | Alnair Ice Fields | ice_field (kuiper) | -- | water_ice: richness 67, 46714 of 50000 left; nitrogen_ice: richness 54, 50000 of 50000 left; deuterium_ice: richness 10, 5000 of 5000 left | none | 2026-11-15 21:51 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 21:51 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:51 UTC | own ship | Read Alnair Ice Fields: 101,714 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 21:51 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 3 (2 planets, 1 ice field). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
