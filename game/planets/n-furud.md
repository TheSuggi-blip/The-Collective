---
name: furud
id: 20261116T033546Z
tier: intel
author: Unity
kind: system
system_id: furud
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-16
---

# Furud

Solarian system 7 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where furud`).

| Field | Value |
|---|---|
| Position | x -1130.4, y 1015.1 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 7 |
| Lanes | acrux, homam, nihal, nova_terra |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `furud_star` | Furud Star | sun (B2V) | -- | -- | none | 2026-11-16 03:19 UTC | `get_system`, own ship |
| `furud_belt` | Furud Belt | asteroid_belt (carbonaceous) | -- | carbon_ore: richness 63, 612 of 30000 left; tungsten_ore: richness 41, 398 of 25000 left | none | 2026-11-16 03:19 UTC | `get_poi`, own ship |
| `furud_vapor_fields` | Furud Vapor Fields | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-16 03:19 UTC | `get_system`, own ship |
| `furud_ice_shelf` | Furud Ice Shelf | ice_field (kuiper) | -- | not read | none | 2026-11-16 03:19 UTC | `get_system`, own ship |
| `furud_legacy_drift` | Furud Legacy Drift | asteroid_belt | -- | not read | none | 2026-11-16 03:19 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 03:19 UTC | own ship | Read Furud Belt: 1,010 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `furud_vapor_fields`, `furud_ice_shelf`, `furud_legacy_drift`.
