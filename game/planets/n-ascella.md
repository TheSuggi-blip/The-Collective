---
name: ascella
id: 20261117T112923Z
tier: intel
author: Unity
kind: system
system_id: ascella
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ascella

- system 13 jumps from home, police level 0. Station: Ironbelt Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ascella`).

| Field | Value |
|---|---|
| Position | x 1649.9, y 666.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | canopus, hr_8832, spica, syrma, thabit |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ascella_star` | Ascella Star | sun (A2V) | -- | -- | none | 2026-11-17 10:57 UTC | `get_system`, own ship |
| `ascella_belt` | Ascella Belt | asteroid_belt (metallic) | -- | iron_ore: richness 42, 99999 of 100000 left; copper_ore: richness 46, 99999 of 100000 left | none | 2026-11-17 10:57 UTC | `get_poi`, own ship |
| `ascella_containment_echo` | Ascella Containment Echo | asteroid_belt | -- | iron_ore: richness 38, 100000 of 100000 left; copper_ore: richness 32, 100000 of 100000 left; antimatter_containment_cell: richness 2, 162 of 162 left | none | 2026-11-17 10:57 UTC | `get_poi`, own ship |
| `e4148510aa80cb75ed982b7a7f671795` | Ironbelt Range | station | `6ada12f4b6baca5ffe69a89c82ad85c6` | -- | none | 2026-11-17 10:57 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Ironbelt Range (`6ada12f4b6baca5ffe69a89c82ad85c6`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 10:57 UTC | `get_system`, own ship |

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
| 2026-11-17 10:57 UTC | own ship | Read Ascella Belt: 199,998 units left in all | `get_poi`, own ship |
| 2026-11-17 10:57 UTC | own ship | Read Ascella Containment Echo: 200,162 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
