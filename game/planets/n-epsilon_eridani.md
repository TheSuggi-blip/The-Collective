---
name: epsilon_eridani
id: 20261117T082528Z
tier: intel
author: Unity
kind: system
system_id: epsilon_eridani
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 55
updated: 2026-11-17
---

# Epsilon Eridani

Solarian system 9 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where epsilon_eridani`).

| Field | Value |
|---|---|
| Position | x -323.7, y 780.5 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 9 |
| Lanes | markab, nihal, nova_terra, procyon, proxima_centauri, sirius |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `delta_major_star` | Delta Major Star | sun (K2V) | -- | -- | none | 2026-11-17 07:48 UTC | `get_system`, own ship |
| `delta_major_i` | Delta Major I | planet (tundra) | -- | -- | none | 2026-11-17 07:48 UTC | `get_system`, own ship |
| `delta_major_ii` | Delta Major II | planet (glacial) | -- | -- | none | 2026-11-17 07:48 UTC | `get_system`, own ship |
| `delta_major_belt` | Delta Major Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 61, 8 of 30000 left; vanadium_ore: richness 50, 0 of 25000 left; platinum_ore: richness 16, 0 of 8000 left; aluminum_ore: richness 57, 7 of 30000 left; legacy_ore: richness 5, 0 of 250 left | none | 2026-11-17 07:48 UTC | `get_poi`, own ship |
| `epsilon_eridani_ice_fields` | Epsilon Eridani Ice Fields | ice_field (kuiper) | -- | water_ice: richness 67, 38989 of 50000 left; nitrogen_ice: richness 53, 49914 of 50000 left | none | 2026-11-17 07:48 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 07:48 UTC | own ship | Read Delta Major Belt: 15 units left in all | `get_poi`, own ship |
| 2026-11-17 07:48 UTC | own ship | Read Epsilon Eridani Ice Fields: 88,903 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
