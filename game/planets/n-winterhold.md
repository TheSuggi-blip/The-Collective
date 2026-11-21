---
name: winterhold
id: 20261121T210446Z
tier: intel
author: Unity
kind: system
system_id: winterhold
standing: neutral
standing_since: 2026-11-21
threat: unknown
empire: -
police_level: 0
updated: 2026-11-21
---

# Winterhold

- system 17 jumps from home, police level 0. Station: Carnegie Hall.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where winterhold`).

| Field | Value |
|---|---|
| Position | x -4805.3, y -3590.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | ashenmoor, gsc_0015, menkib, mirfak, tabit, willowgate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `winterhold_star` | Winterhold Star | sun (M2V) | -- | -- | none | 2026-11-21 19:20 UTC | `get_system`, own ship |
| `winterhold_i` | Winterhold I | planet (scorched) | -- | -- | none | 2026-11-21 19:20 UTC | `get_system`, own ship |
| `winterhold_ii` | Winterhold II | planet (arid) | -- | -- | none | 2026-11-21 19:20 UTC | `get_system`, own ship |
| `winterhold_iii` | Winterhold III | planet (terran) | -- | -- | none | 2026-11-21 19:20 UTC | `get_system`, own ship |
| `winterhold_gas_pocket` | Winterhold Gas Pocket | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-21 19:20 UTC | `get_system`, own ship |
| `grey_shimmer` | Grey Shimmer | nebula | -- | -- | none | 2026-11-21 19:20 UTC | `get_system`, own ship |
| `mothsilk_cloud` | Mothsilk Cloud | nebula | -- | -- | none | 2026-11-21 19:20 UTC | `get_system`, own ship |
| `6a286d5d8c48468a8d50e57da6cb3690` | Carnegie Hall | station | `554230f8a484b98ffeb5760d80d44c60` | -- | none | 2026-11-21 19:20 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Carnegie Hall (`554230f8a484b98ffeb5760d80d44c60`) | unknown | not tried | not read | unknown | unknown | 2026-11-21 19:20 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-21 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-21 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-21 19:20 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `winterhold_gas_pocket`.
