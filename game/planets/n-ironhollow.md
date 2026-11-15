---
name: ironhollow
id: 20261115T215324Z
tier: intel
author: Unity
kind: system
system_id: ironhollow
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Ironhollow

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ironhollow`).

| Field | Value |
|---|---|
| Position | x -2454.3, y 2029.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | gsc_0041, pherkad, ruchbah, the_experiment |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ironhollow_star` | Ironhollow Star | sun (M2V) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `ironhollow_i` | Ironhollow I | planet (scorched) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `ironhollow_ii` | Ironhollow II | planet (arid) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `ironhollow_fading_signal` | Ironhollow Fading Signal | asteroid_belt | -- | iron_ore: richness 40, 47201 of 100000 left; copper_ore: richness 22, 99999 of 100000 left; antimatter_containment_cell: richness 2, 129 of 129 left | none | 2026-11-15 21:13 UTC | `get_poi`, own ship |
| `echo_ejecta` | Echo Ejecta | asteroid_belt | -- | iron_ore: richness 26, 100000 of 100000 left; copper_ore: richness 25, 100000 of 100000 left; sol_alloy_ore: richness 4, 1450 of 1450 left | none | 2026-11-15 21:13 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 21:13 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:13 UTC | own ship | Read Ironhollow Fading Signal: 147,329 units left in all | `get_poi`, own ship |
| 2026-11-15 21:13 UTC | own ship | Read Echo Ejecta: 201,450 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 21:13 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 4 (2 planets, 2 belts). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
