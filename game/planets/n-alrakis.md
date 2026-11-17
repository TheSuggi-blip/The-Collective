---
name: alrakis
id: 20261117T184422Z
tier: intel
author: Unity
kind: system
system_id: alrakis
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Alrakis

Nebula system 20 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alrakis`).

| Field | Value |
|---|---|
| Position | x 2527.3, y -3409.3 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 20 |
| Lanes | alula, bunda, cargo_lanes, gsc_0051, tau_bootis |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alrakis_star` | Alrakis Star | sun (K4V) | -- | -- | none | 2026-11-17 18:33 UTC | `get_system`, own ship |
| `alrakis_ice_fields` | Alrakis Ice Fields | ice_field (kuiper) | -- | water_ice: richness 56, 521 of 50000 left; nitrogen_ice: richness 31, 1111 of 50000 left; helium_ice: richness 13, 510 of 5000 left; ammonia_ice: richness 15, 509 of 6000 left | none | 2026-11-17 18:33 UTC | `get_poi`, own ship |
| `alrakis_commerce_vein` | Alrakis Commerce Vein | asteroid_belt | -- | iron_ore: richness 32, 54214 of 100000 left; copper_ore: richness 25, 99536 of 100000 left; trade_crystal: richness 30, 46 of 4800 left | none | 2026-11-17 18:33 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:33 UTC | own ship | Read Alrakis Ice Fields: 2,651 units left in all | `get_poi`, own ship |
| 2026-11-17 18:33 UTC | own ship | Read Alrakis Commerce Vein: 153,796 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
