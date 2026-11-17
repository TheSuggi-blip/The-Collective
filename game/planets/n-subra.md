---
name: subra
id: 20261117T102836Z
tier: intel
author: Unity
kind: system
system_id: subra
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Subra

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where subra`).

| Field | Value |
|---|---|
| Position | x 1443.4, y 3014.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | ivorygate, porrima, toi_1452, westmark |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `subra_star` | Subra Star | sun (M6V) | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |
| `subra_i` | Subra I | planet (scorched) | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |
| `subra_ii` | Subra II | planet (arid) | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |
| `subra_iii` | Subra III | planet (terran) | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |
| `subra_iv` | Subra IV | planet (jovian) | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |
| `floodlight_flats` | Floodlight Flats | asteroid_belt | -- | iron_ore: richness 45, 95232 of 100000 left; copper_ore: richness 30, 100000 of 100000 left; silicon_ore: richness 43, 3187 of 20000 left; neodymium_ore: richness 11, 1666 of 3500 left | none | 2026-11-17 10:27 UTC | `get_poi`, own ship |

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
| 2026-11-17 10:27 UTC | own ship | Read Floodlight Flats: 200,085 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
