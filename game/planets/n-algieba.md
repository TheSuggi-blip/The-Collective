---
name: algieba
id: 20261117T194624Z
tier: intel
author: Unity
kind: system
system_id: algieba
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Algieba

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where algieba`).

| Field | Value |
|---|---|
| Position | x 1833.4, y -638.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | fuyue, ross_248, situla, struve_2398 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `algieba_star` | Algieba Star | sun (K1III) | -- | -- | none | 2026-11-17 19:37 UTC | `get_system`, own ship |
| `algieba_i_b` | Algieba I b | planet (jovian) | -- | -- | none | 2026-11-17 19:37 UTC | `get_system`, own ship |
| `algieba_belt` | Algieba Belt | asteroid_belt (metallic) | -- | iron_ore: richness 35, 4146 of 22000 left; nickel_ore: richness 25, 358 of 15000 left; gold_ore: richness 12, 360 of 6000 left | none | 2026-11-17 19:37 UTC | `get_poi`, own ship |

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
| 2026-11-17 19:37 UTC | own ship | Read Algieba Belt: 4,864 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
