---
name: tau_bootis
id: 20261117T184402Z
tier: intel
author: Unity
kind: system
system_id: tau_bootis
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tau Bootis

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tau_bootis`).

| Field | Value |
|---|---|
| Position | x 2528.5, y -2771.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | alkaid, alrakis, gsc_0051, segin |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tau_bootis_star` | Tau Bootis Star | sun (K2V) | -- | -- | none | 2026-11-17 18:20 UTC | `get_system`, own ship |
| `tau_bootis_belt_a` | Tau Bootis Belt A | asteroid_belt (metallic) | -- | iron_ore: richness 43, 51779 of 100000 left; copper_ore: richness 21, 99921 of 100000 left | none | 2026-11-17 18:20 UTC | `get_poi`, own ship |
| `tau_bootis_belt_b` | Tau Bootis Belt B | asteroid_belt (metallic) | -- | iron_ore: richness 53, 180 of 100000 left; copper_ore: richness 29, 99861 of 100000 left; gold_ore: richness 36, 22 of 25000 left | none | 2026-11-17 18:20 UTC | `get_poi`, own ship |
| `tau_bootis_ice_shelf` | Tau Bootis Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 62, 194 of 50000 left; nitrogen_ice: richness 32, 21655 of 50000 left; deuterium_ice: richness 21, 1971 of 5000 left; helium_ice: richness 10, 4991 of 5000 left | none | 2026-11-17 18:20 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:20 UTC | own ship | Read Tau Bootis Belt A: 151,700 units left in all | `get_poi`, own ship |
| 2026-11-17 18:20 UTC | own ship | Read Tau Bootis Belt B: 100,063 units left in all | `get_poi`, own ship |
| 2026-11-17 18:20 UTC | own ship | Read Tau Bootis Ice Shelf: 28,811 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
