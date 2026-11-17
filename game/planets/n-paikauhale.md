---
name: paikauhale
id: 20261117T133355Z
tier: intel
author: Unity
kind: system
system_id: paikauhale
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Paikauhale

- system 26 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where paikauhale`).

| Field | Value |
|---|---|
| Position | x 6049.1, y -2795.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 26 |
| Lanes | gacrux, inquill, tegmine |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `paikauhale_star` | Paikauhale Star | sun (A0V) | -- | -- | none | 2026-11-17 12:51 UTC | `get_system`, own ship |
| `paikauhale_i` | Paikauhale I | planet (scorched) | -- | -- | none | 2026-11-17 12:51 UTC | `get_system`, own ship |
| `paikauhale_ii` | Paikauhale II | planet (arid) | -- | -- | none | 2026-11-17 12:51 UTC | `get_system`, own ship |
| `paikauhale_ice_shelf` | Paikauhale Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 62, 41983 of 50000 left; nitrogen_ice: richness 47, 50000 of 50000 left; deuterium_ice: richness 19, 5000 of 5000 left; helium_ice: richness 20, 5000 of 5000 left | none | 2026-11-17 12:51 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:51 UTC | own ship | Read Paikauhale Ice Shelf: 101,983 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
