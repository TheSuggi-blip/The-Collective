---
name: azmidi
id: 20261117T123130Z
tier: intel
author: Unity
kind: system
system_id: azmidi
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Azmidi

Nebula system 23 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where azmidi`).

| Field | Value |
|---|---|
| Position | x 1595.0, y -5826.0 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 23 |
| Lanes | alioth, almach, khambalia, nusakan |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `azmidi_star` | Azmidi Star | sun (G8V) | -- | -- | none | 2026-11-17 12:20 UTC | `get_system`, own ship |
| `azmidi_i` | Azmidi I | planet (arid) | -- | -- | none | 2026-11-17 12:20 UTC | `get_system`, own ship |
| `azmidi_ii` | Azmidi II | planet (tundra) | -- | -- | none | 2026-11-17 12:20 UTC | `get_system`, own ship |
| `azmidi_belt` | Azmidi Belt | asteroid_belt (carbonaceous) | -- | not read | none | 2026-11-17 12:20 UTC | `get_system`, own ship |
| `azmidi_gas_cloud` | Azmidi Gas Cloud | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 12:20 UTC | `get_system`, own ship |
| `azmidi_ice_fields` | Azmidi Ice Fields | ice_field (kuiper) | -- | water_ice: richness 68, 55 of 50000 left; nitrogen_ice: richness 47, 117 of 50000 left; ammonia_ice: richness 17, 236 of 9000 left | none | 2026-11-17 12:20 UTC | `get_poi`, own ship |
| `guildless_facets` | Guildless Facets | asteroid_belt | -- | not read | none | 2026-11-17 12:20 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 12:20 UTC | own ship | Read Azmidi Ice Fields: 408 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `azmidi_belt`, `azmidi_gas_cloud`, `guildless_facets`.
