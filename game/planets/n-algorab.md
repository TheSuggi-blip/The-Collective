---
name: algorab
id: 20261117T102823Z
tier: intel
author: Unity
kind: system
system_id: algorab
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Algorab

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where algorab`).

| Field | Value |
|---|---|
| Position | x 903.1, y 4283.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | chara, mebsuta, phecda, tureis |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `algorab_star` | Algorab Star | sun (G2V) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `algorab_i` | Algorab I | planet (scorched) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `algorab_ii` | Algorab II | planet (arid) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `algorab_iii` | Algorab III | planet (terran) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `algorab_iv` | Algorab IV | planet (tundra) | -- | -- | none | 2026-11-17 09:52 UTC | `get_system`, own ship |
| `long_sweep_arc` | Long Sweep Arc | asteroid_belt | -- | nickel_ore: richness 31, 1342 of 20000 left | none | 2026-11-17 09:52 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:52 UTC | own ship | Read Long Sweep Arc: 1,342 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
