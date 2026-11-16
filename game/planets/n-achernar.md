---
name: achernar
id: 20261115T215314Z
tier: intel
author: Unity
kind: system
system_id: achernar
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Achernar

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where achernar`).

| Field | Value |
|---|---|
| Position | x -2716.0, y 1438.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | cedarhold, garnet, ruchbah, the_experiment |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `achernar_star` | Achernar Star | sun (M2V) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `achernar_i` | Achernar I | planet (scorched) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `achernar_ii` | Achernar II | planet (arid) | -- | -- | none | 2026-11-15 21:13 UTC | `get_system`, own ship |
| `achernar_belt` | Achernar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 32, 99999 of 100000 left; copper_ore: richness 39, 100000 of 100000 left | none | 2026-11-15 21:13 UTC | `get_poi`, own ship |
| `achernar_gas_pocket` | Achernar Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 44, 9333 of 50000 left; argon_gas: richness 41, 50000 of 50000 left; plasma_gas: richness 31, 10000 of 10000 left; neon_gas: richness 42, 50000 of 50000 left | none | 2026-11-15 21:13 UTC | `get_poi`, own ship |
| `achernar_frost_ring` | Achernar Frost Ring | ice_field (cometary) | -- | water_ice: richness 46, 27331 of 50000 left; nitrogen_ice: richness 35, 50000 of 50000 left; deuterium_ice: richness 12, 301 of 5000 left; methane_ice: richness 16, 301 of 7000 left | none | 2026-11-15 21:13 UTC | `get_poi`, own ship |

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
| 2026-11-15 21:13 UTC | own ship | Read Achernar Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-15 21:13 UTC | own ship | Read Achernar Gas Pocket: 119,333 units left in all | `get_poi`, own ship |
| 2026-11-15 21:13 UTC | own ship | Read Achernar Frost Ring: 77,933 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 21:13 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; a station too: none stands in the system (one per system, game/rules/09-factions.md). Places without a base: 5 (2 planets, 1 belt, 1 gas cloud, 1 ice field). Foreign pilots our ships saw here: 1 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
- Station site (S6), Oracle, 2026-11-16, ranked first of three (with Alnair and Wolf 1061): the only one of the three with all three kinds of field. Read 07:30 UTC (data/scouting/achernar.json, the tool system): Achernar Belt iron ore 99,997 of 100,000 and copper ore 99,997 of 100,000 (the station core foundry asks 491,400 iron ore, the tool base_plan); Achernar Gas Pocket plasma gas 9,960 of 10,000, argon and neon 50,000 each, hydrogen 1,800 of 50,000; Achernar Frost Ring water ice 24,253 of 50,000 (our ice routes draw on it), nitrogen ice 48,881. Herds: 10 belt-grazers, 5 patina-grazers, 4 slag tortoises at the belt; 12 drift-rays, 4 pilot whales, 2 cinder-sylphs at the gas pocket. Who passes: 95 reads of ours from 2026-11-15 21:14 to 2026-11-16 08:24 UTC, 18 of them with a pilot not ours, none with a pirate (data/intel/sightings.jsonl); factions met PAYN, HEXC, BUSY. Against it: the system's own description names it a long-haul lane between our space and the far empires, and the frost ring's water ice is half gone. How fast its fields grow back is not measured: our mining hides it.
