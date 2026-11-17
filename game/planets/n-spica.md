---
name: spica
id: 20261117T133405Z
tier: intel
author: Unity
kind: system
system_id: spica
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Spica

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where spica`).

| Field | Value |
|---|---|
| Position | x 1826.1, y 1103.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | ascella, canopus, propus, syrma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `spica_star` | Spica Star | sun (M6V) | -- | -- | none | 2026-11-17 12:38 UTC | `get_system`, own ship |
| `spica_i` | Spica I | planet (scorched) | -- | -- | none | 2026-11-17 12:38 UTC | `get_system`, own ship |
| `spica_ii` | Spica II | planet (arid) | -- | -- | none | 2026-11-17 12:38 UTC | `get_system`, own ship |
| `spica_belt` | Spica Belt | asteroid_belt (metallic) | -- | iron_ore: richness 67, 21496 of 100000 left; copper_ore: richness 30, 100000 of 100000 left | none | 2026-11-17 12:38 UTC | `get_poi`, own ship |
| `spica_cryobelt` | Spica Cryobelt | ice_field (kuiper) | -- | water_ice: richness 59, 44091 of 50000 left | none | 2026-11-17 12:38 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:38 UTC | own ship | Read Spica Belt: 121,496 units left in all | `get_poi`, own ship |
| 2026-11-17 12:38 UTC | own ship | Read Spica Cryobelt: 44,091 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
