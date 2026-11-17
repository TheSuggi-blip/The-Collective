---
name: 40_eridani
id: 20261117T123121Z
tier: intel
author: Unity
kind: system
system_id: 40_eridani
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# 40 Eridani

- system 14 jumps from home, police level 0. Station: The Second Ledger.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where 40_eridani`).

| Field | Value |
|---|---|
| Position | x 2243.9, y 4432.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | alpheratz, angetenar, bd20_2457, wasat |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `40_eridani_star` | 40 Eridani Star | sun (M4V) | -- | -- | none | 2026-11-17 11:42 UTC | `get_system`, own ship |
| `40_eridani_i` | 40 Eridani I | planet (scorched) | -- | -- | none | 2026-11-17 11:42 UTC | `get_system`, own ship |
| `40_eridani_ii` | 40 Eridani II | planet (arid) | -- | -- | none | 2026-11-17 11:42 UTC | `get_system`, own ship |
| `40_eridani_iii` | 40 Eridani III | planet (terran) | -- | -- | none | 2026-11-17 11:42 UTC | `get_system`, own ship |
| `flarelit_seam` | Flarelit Seam | asteroid_belt | -- | nickel_ore: richness 45, 2 of 20000 left | none | 2026-11-17 11:42 UTC | `get_poi`, own ship |
| `d6789ab34d7ec5bb3a9cdce9cdb1e31b` | The Second Ledger | station | `95734cdcee4d6ff00f2b393bb4dfab53` | -- | none | 2026-11-17 11:42 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Second Ledger (`95734cdcee4d6ff00f2b393bb4dfab53`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 11:42 UTC | `get_system`, own ship |

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
| 2026-11-17 11:42 UTC | own ship | Read Flarelit Seam: 2 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
