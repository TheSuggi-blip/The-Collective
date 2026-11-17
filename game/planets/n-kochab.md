---
name: kochab
id: 20261117T194619Z
tier: intel
author: Unity
kind: system
system_id: kochab
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kochab

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kochab`).

| Field | Value |
|---|---|
| Position | x -1730.5, y -2545.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | haedus, starfall, sulafat, void_gate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kochab_star` | Kochab Star | sun (G5V) | -- | -- | none | 2026-11-17 19:08 UTC | `get_system`, own ship |
| `kochab_i` | Kochab I | planet (scorched) | -- | -- | none | 2026-11-17 19:08 UTC | `get_system`, own ship |
| `kochab_belt` | Kochab Belt | asteroid_belt (metallic) | -- | iron_ore: richness 32, 99999 of 100000 left; copper_ore: richness 25, 100000 of 100000 left | none | 2026-11-17 19:08 UTC | `get_poi`, own ship |
| `elbowroom_veil` | Elbowroom Veil | nebula | -- | -- | none | 2026-11-17 19:08 UTC | `get_system`, own ship |

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
| 2026-11-17 19:08 UTC | own ship | Read Kochab Belt: 199,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
