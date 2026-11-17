---
name: gold_run
id: 20261117T123141Z
tier: intel
author: Unity
kind: system
system_id: gold_run
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 55
updated: 2026-11-17
---

# Gold Run

Nebula system 19 jumps from home, police level 55. Station: Gold Run Extraction Hub.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gold_run`).

| Field | Value |
|---|---|
| Position | x 2039.2, y -3896.3 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 19 |
| Lanes | bunda, cargo_lanes, copernicus, market_prime, wealth_lane |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `aurelia` | Aurelia | sun (K3V) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_i` | Gold Run I | planet (arid) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_ii` | Gold Run II | planet (terran) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_iii` | Gold Run III | planet (terran) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_iv` | Gold Run IV | planet (jovian) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_v` | Gold Run V | planet (glacial) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_mineral_fields` | Gold Run Mineral Fields | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_cryobelt` | Gold Run Cryobelt | ice_field (kuiper) | -- | not read | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `gold_run_extraction_hub` | Gold Run Extraction Hub | station | `gold_run_extraction_hub` | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Gold Run Extraction Hub (`gold_run_extraction_hub`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 12:16 UTC | `get_system`, own ship |

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
| 2026-11-17 12:16 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `gold_run_mineral_fields`, `gold_run_cryobelt`.
