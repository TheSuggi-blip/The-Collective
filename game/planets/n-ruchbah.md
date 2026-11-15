---
name: ruchbah
id: 20261115T215327Z
tier: intel
author: Unity
kind: system
system_id: ruchbah
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Ruchbah

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ruchbah`).

| Field | Value |
|---|---|
| Position | x -2519.9, y 1693.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | achernar, garnet, ironhollow, the_experiment |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ruchbah_star` | Ruchbah Star | sun (M4V) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `ruchbah_i` | Ruchbah I | planet (scorched) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `ruchbah_ii` | Ruchbah II | planet (arid) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `ruchbah_ice_belt` | Ruchbah Ice Belt | ice_field (kuiper) | -- | water_ice: richness 58, 13456 of 50000 left; nitrogen_ice: richness 42, 19039 of 50000 left; deuterium_ice: richness 16, 3140 of 5000 left; methane_ice: richness 14, 3142 of 5000 left | none | 2026-11-15 21:13 UTC | `get_poi`, own ship |
| `broken_glass_veil` | Broken Glass Veil | nebula | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |

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
| 2026-11-15 21:13 UTC | own ship | Read Ruchbah Ice Belt: 38,777 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 21:13 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 4 (2 planets, 1 ice field, 1 nebula). Foreign pilots our ships saw here: 2 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
