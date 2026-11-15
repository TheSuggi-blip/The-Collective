---
name: keid
id: 20261115T225421Z
tier: intel
author: Unity
kind: system
system_id: keid
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Keid

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where keid`).

| Field | Value |
|---|---|
| Position | x -3380.9, y 3665.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | coldwater, gsc_0012, gsc_0031, okab |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `keid_star` | Keid Star | sun (G2V) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `keid_i` | Keid I | planet (scorched) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `keid_ii` | Keid II | planet (arid) | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |
| `keid_belt` | Keid Belt | asteroid_belt (metallic) | -- | iron_ore: richness 58, 99999 of 100000 left; copper_ore: richness 49, 100000 of 100000 left | none | 2026-11-15 22:03 UTC | `get_poi`, own ship |
| `keid_ice_shelf` | Keid Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 56, 1959 of 50000 left; deuterium_ice: richness 12, 4303 of 5000 left | none | 2026-11-15 22:03 UTC | `get_poi`, own ship |
| `keid_fractured_prism` | Keid Fractured Prism | nebula | -- | -- | none | 2026-11-15 22:03 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 22:03 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 22:03 UTC | own ship | Read Keid Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-15 22:03 UTC | own ship | Read Keid Ice Shelf: 6,262 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 22:03 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 5 (2 planets, 1 belt, 1 ice field, 1 nebula). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
