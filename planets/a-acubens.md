---
name: acubens
id: 20261115T142759Z
tier: intel
author: Unity
kind: system
system_id: acubens
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 55
updated: 2026-11-15
---

# Acubens

Voidborn system 2 jumps from home, police level 55. No station on the chart.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where acubens`).

| Field | Value |
|---|---|
| Position | x -3987.6, y 3081.1 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 2 |
| Lanes | gsc_0027, hamal, node_beta, node_gamma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `acubens_star` | Acubens Star | sun (A5V) | -- | -- | none | 2026-11-15 13:09 UTC | `get_system`, own ship |
| `acubens_i` | Acubens I | planet (scorched) | -- | -- | none | 2026-11-15 13:09 UTC | `get_system`, own ship |
| `acubens_belt` | Acubens Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 55, 192 of 30000 left; tungsten_ore: richness 34, 16 of 25000 left; platinum_ore: richness 14, 17 of 8000 left; palladium_ore: richness 28, 8 of 5000 left; uranium_ore: richness 13, 0 of 5000 left; lead_ore: richness 15, 122 of 20000 left | none | 2026-11-15 13:09 UTC | `get_poi`, own ship |
| `acubens_shadow_pocket` | Acubens Shadow Pocket | asteroid_belt | -- | iron_ore: richness 40, 78496 of 100000 left; copper_ore: richness 32, 94468 of 100000 left; null_matter: richness 16, 0 of 1078 left | none | 2026-11-15 13:09 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | ally | Unity | Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 13:09 UTC | own ship | Read Acubens Belt: 355 units left in all | `get_poi`, own ship |
| 2026-11-15 13:09 UTC | own ship | Read Acubens Shadow Pocket: 172,964 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
