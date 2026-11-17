---
name: fumalsamakah
id: 20261117T153734Z
tier: intel
author: Unity
kind: system
system_id: fumalsamakah
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Fumalsamakah

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where fumalsamakah`).

| Field | Value |
|---|---|
| Position | x 3274.4, y 3838.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | albireo, bd20_2457, dawnbreak, rasalgethi, rigel, ross_614, saclateni |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `fumalsamakah_star` | Fumalsamakah Star | sun (G5V) | -- | -- | none | 2026-11-17 15:18 UTC | `get_system`, own ship |
| `fumalsamakah_i` | Fumalsamakah I | planet (scorched) | -- | -- | none | 2026-11-17 15:18 UTC | `get_system`, own ship |
| `fumalsamakah_ii` | Fumalsamakah II | planet (arid) | -- | -- | none | 2026-11-17 15:18 UTC | `get_system`, own ship |
| `fumalsamakah_iii` | Fumalsamakah III | planet (terran) | -- | -- | none | 2026-11-17 15:18 UTC | `get_system`, own ship |
| `fumalsamakah_belt` | Fumalsamakah Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 15:18 UTC | `get_system`, own ship |
| `fumalsamakah_frost_ring` | Fumalsamakah Frost Ring | ice_field (kuiper) | -- | water_ice: richness 62, 43361 of 50000 left; nitrogen_ice: richness 49, 50000 of 50000 left; helium_ice: richness 22, 4108 of 5000 left | none | 2026-11-17 15:18 UTC | `get_poi`, own ship |
| `sleeping_caldera` | Sleeping Caldera | asteroid_belt | -- | not read | none | 2026-11-17 15:18 UTC | `get_system`, own ship |

## Stations

None on the chart.

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
| 2026-11-17 15:18 UTC | own ship | Read Fumalsamakah Frost Ring: 97,469 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `fumalsamakah_belt`, `sleeping_caldera`.
