---
name: coldwater
id: 20261115T225417Z
tier: intel
author: Unity
kind: system
system_id: coldwater
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Coldwater

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where coldwater`).

| Field | Value |
|---|---|
| Position | x -3432.8, y 3904.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | gsc_0012, keid, okab, stormwatch, tanglewood |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `coldwater_star` | Coldwater Star | sun (K6V) | -- | -- | none | 2026-11-15 22:02 UTC | `get_system`, own ship |
| `coldwater_emission_nebula` | Coldwater Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 59, 10064 of 50000 left; argon_gas: richness 47, 50000 of 50000 left; xenon_gas: richness 28, 2956 of 10000 left; neon_gas: richness 51, 50000 of 50000 left | none | 2026-11-15 22:02 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 22:02 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 22:02 UTC | own ship | Read Coldwater Emission Nebula: 113,020 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 22:02 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 1 (1 gas cloud). Foreign pilots our ships saw here: 0 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
