---
name: arneb
id: 20261117T143528Z
tier: intel
author: Unity
kind: system
system_id: arneb
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Arneb

- system 16 jumps from home, police level 0. Station: The Obsidian Well.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where arneb`).

| Field | Value |
|---|---|
| Position | x 3274.7, y 4797.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | diphda, gsc_0019, kornephoros, thuban |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `arneb_star` | Arneb Star | sun (M4V) | -- | -- | none | 2026-11-17 14:12 UTC | `get_system`, own ship |
| `arneb_i` | Arneb I | planet (scorched) | -- | -- | none | 2026-11-17 14:12 UTC | `get_system`, own ship |
| `arneb_gas_pocket` | Arneb Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 64, 1696 of 50000 left; argon_gas: richness 35, 50000 of 50000 left; xenon_gas: richness 22, 9932 of 10000 left; neon_gas: richness 48, 37932 of 50000 left; krypton_gas: richness 22, 971 of 5000 left | none | 2026-11-17 14:12 UTC | `get_poi`, own ship |
| `arneb_frost_ring` | Arneb Frost Ring | ice_field (kuiper) | -- | water_ice: richness 40, 740 of 50000 left; nitrogen_ice: richness 45, 740 of 50000 left; deuterium_ice: richness 13, 148 of 5000 left; tritium_ice: richness 8, 149 of 800 left | none | 2026-11-17 14:12 UTC | `get_poi`, own ship |
| `arneb_ash_pocket` | Arneb Ash Pocket | asteroid_belt | -- | iron_ore: richness 29, 0 of 100000 left; copper_ore: richness 22, 2 of 100000 left; plasma_residue: richness 9, 0 of 1022 left | none | 2026-11-17 14:12 UTC | `get_poi`, own ship |
| `a356fc2c1744c0425cf6cf47f48def92` | The Obsidian Well | station | `cca9e51e6eaf8dada77f698ccc4a09c7` | -- | none | 2026-11-17 14:12 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Obsidian Well (`cca9e51e6eaf8dada77f698ccc4a09c7`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:12 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:12 UTC | own ship | Read Arneb Gas Pocket: 100,531 units left in all | `get_poi`, own ship |
| 2026-11-17 14:12 UTC | own ship | Read Arneb Frost Ring: 1,777 units left in all | `get_poi`, own ship |
| 2026-11-17 14:12 UTC | own ship | Read Arneb Ash Pocket: 2 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
