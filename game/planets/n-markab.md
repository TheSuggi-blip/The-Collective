---
name: markab
id: 20261117T082537Z
tier: intel
author: Unity
kind: system
system_id: markab
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-17
---

# Markab

Solarian system 9 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where markab`).

| Field | Value |
|---|---|
| Position | x -98.6, y 1273.1 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 9 |
| Lanes | adhafera, epsilon_eridani, gsc_0022, harborlight, nihal, procyon |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `markab_star` | Markab Star | sun (A0III) | -- | -- | none | 2026-11-17 07:51 UTC | `get_system`, own ship |
| `markab_i` | Markab I | planet (scorched) | -- | -- | none | 2026-11-17 07:51 UTC | `get_system`, own ship |
| `markab_ii` | Markab II | planet (scorched) | -- | -- | none | 2026-11-17 07:51 UTC | `get_system`, own ship |
| `markab_iii` | Markab III | planet (arid) | -- | -- | none | 2026-11-17 07:51 UTC | `get_system`, own ship |
| `markab_iv` | Markab IV | planet (arid) | -- | -- | none | 2026-11-17 07:51 UTC | `get_system`, own ship |
| `markab_belt` | Markab Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 60, 161 of 30000 left; vanadium_ore: richness 29, 260 of 25000 left; tungsten_ore: richness 42, 151 of 25000 left; platinum_ore: richness 18, 503 of 8000 left; palladium_ore: richness 29, 4 of 5000 left; gold_ore: richness 36, 158 of 25000 left; rhodium_ore: richness 11, 309 of 3000 left | none | 2026-11-17 07:51 UTC | `get_poi`, own ship |
| `markab_ice_fields` | Markab Ice Fields | ice_field (kuiper) | -- | water_ice: richness 59, 34396 of 50000 left; nitrogen_ice: richness 36, 50000 of 50000 left | none | 2026-11-17 07:51 UTC | `get_poi`, own ship |
| `decommissioned_array_platform` | Decommissioned Array Platform | relic (derelict) | -- | -- | none | 2026-11-17 07:51 UTC | `get_system`, own ship |
| `markab_alloy_seam` | Markab Alloy Seam | asteroid_belt | -- | iron_ore: richness 45, 89736 of 100000 left; copper_ore: richness 21, 100000 of 100000 left; sol_alloy_ore: richness 8, 768 of 2070 left | none | 2026-11-17 07:51 UTC | `get_poi`, own ship |

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
| 2026-11-17 07:51 UTC | own ship | Read Markab Belt: 1,546 units left in all | `get_poi`, own ship |
| 2026-11-17 07:51 UTC | own ship | Read Markab Ice Fields: 84,396 units left in all | `get_poi`, own ship |
| 2026-11-17 07:51 UTC | own ship | Read Markab Alloy Seam: 190,504 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
