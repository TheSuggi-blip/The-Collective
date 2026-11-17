---
name: the_anvil
id: 20261117T174146Z
tier: intel
author: Unity
kind: system
system_id: the_anvil
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 80
updated: 2026-11-17
---

# The Anvil

Crimson system 20 jumps from home, police level 80. Station: The Anvil Arsenal.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where the_anvil`).

| Field | Value |
|---|---|
| Position | x 5031.3, y 2408.3 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 20 |
| Lanes | frostfeld, hd_20794, iron_reach, ironhearth, krynn |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `steelpoint` | Steelpoint | sun (DA) | -- | -- | none | 2026-11-17 16:55 UTC | `get_system`, own ship |
| `anvil_i` | Anvil I | planet (scorched) | -- | -- | none | 2026-11-17 16:55 UTC | `get_system`, own ship |
| `anvil_ii` | Anvil II | planet (glacial) | -- | -- | none | 2026-11-17 16:55 UTC | `get_system`, own ship |
| `anvil_proving_grounds` | Anvil Proving Grounds | asteroid_belt (mixed) | -- | carbon_ore: richness 58, 0 of 30000 left; vanadium_ore: richness 28, 0 of 25000 left | none | 2026-11-17 16:55 UTC | `get_poi`, own ship |
| `the_anvil_arsenal` | The Anvil Arsenal | station | `the_anvil_arsenal` | -- | none | 2026-11-17 16:55 UTC | `get_system`, own ship |
| `bulwark_vein` | Bulwark Vein | asteroid_belt (metallic) | -- | iron_ore: richness 35, 335 of 50000 left; carbon_ore: richness 15, 820 of 20000 left; titanium_ore: richness 65, 39 of 50000 left | none | 2026-11-17 16:55 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Anvil Arsenal (`the_anvil_arsenal`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:55 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 16:55 UTC | own ship | Read Anvil Proving Grounds: nothing left | `get_poi`, own ship |
| 2026-11-17 16:55 UTC | own ship | Read Bulwark Vein: 1,194 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
