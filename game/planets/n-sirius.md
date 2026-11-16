---
name: sirius
id: 20261116T210214Z
tier: intel
author: Unity
kind: system
system_id: sirius
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: solarian
police_level: 80
updated: 2026-11-16
---

# Sirius

Solarian system 9 jumps from home, police level 80. Station: Sirius Observatory Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sirius`).

| Field | Value |
|---|---|
| Position | x -681.7, y 215.9 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 9 |
| Lanes | epsilon_eridani, lacaille_9352, nova_terra, sol |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sirius_a` | Sirius A | sun (A1V) | -- | -- | none | 2026-11-16 20:05 UTC | `get_system`, own ship |
| `research_campus` | Research Campus | planet (terran) | -- | -- | none | 2026-11-16 20:05 UTC | `get_system`, own ship |
| `observatory_plateau` | Observatory Plateau | planet (arid) | -- | -- | none | 2026-11-16 20:05 UTC | `get_system`, own ship |
| `sirius_gas_pocket` | Sirius Gas Pocket | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-16 20:05 UTC | `get_system`, own ship |
| `sirius_observatory_station` | Sirius Observatory Station | station | `sirius_observatory_station` | -- | none | 2026-11-16 20:05 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Sirius Observatory Station (`sirius_observatory_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-16 20:05 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 20:05 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `sirius_gas_pocket`.
