---
name: torcular
id: 20261117T184358Z
tier: intel
author: Unity
kind: system
system_id: torcular
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Torcular

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where torcular`).

| Field | Value |
|---|---|
| Position | x -6014.3, y -1878.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | aludra, gsc_0002, gsc_0043, gsc_0045, tejat |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `torcular_star` | Torcular Star | sun (K4V) | -- | -- | none | 2026-11-17 17:53 UTC | `get_system`, own ship |
| `torcular_i` | Torcular I | planet (scorched) | -- | -- | none | 2026-11-17 17:53 UTC | `get_system`, own ship |
| `torcular_belt` | Torcular Belt | asteroid_belt (metallic) | -- | iron_ore: richness 56, 93030 of 100000 left; copper_ore: richness 49, 97347 of 100000 left; aluminum_ore: richness 56, 15774 of 30000 left | none | 2026-11-17 17:53 UTC | `get_poi`, own ship |
| `torcular_frost_ring` | Torcular Frost Ring | ice_field (kuiper) | -- | water_ice: richness 44, 45301 of 50000 left; nitrogen_ice: richness 48, 46487 of 50000 left; deuterium_ice: richness 19, 4654 of 5000 left | none | 2026-11-17 17:53 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:53 UTC | own ship | Read Torcular Belt: 206,151 units left in all | `get_poi`, own ship |
| 2026-11-17 17:53 UTC | own ship | Read Torcular Frost Ring: 96,442 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
