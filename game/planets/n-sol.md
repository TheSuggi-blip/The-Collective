---
name: sol
id: 20261116T025814Z
tier: intel
author: Unity
kind: system
system_id: sol
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: solarian
police_level: 100
updated: 2026-11-16
---

# Sol

Solarian system 10 jumps from home, police level 100. Station: Sol Central.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sol`).

| Field | Value |
|---|---|
| Position | x 0.0, y 0.0 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 10 |
| Lanes | alpha_centauri, sirius |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sol_star` | Sol Star | sun (G2V) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `mercury` | Mercury | planet (scorched) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `venus` | Venus | planet (hothouse) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `earth` | Earth | planet (terran) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `sol_central` | Sol Central | station | `confederacy_central_command` | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `mars` | Mars | planet (terran) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `main_belt` | Main Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `jupiter` | Jupiter | planet (jovian) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `jovian_extraction_zone` | Jovian Extraction Zone | gas_cloud (atmospheric) | -- | not read | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `saturn` | Saturn | planet (jovian) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `uranus` | Uranus | planet (ice_giant) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `neptune` | Neptune | planet (ice_giant) | -- | -- | none | 2026-11-16 02:00 UTC | `get_system`, own ship |
| `kuiper_ice_fields` | Kuiper Ice Fields | ice_field (kuiper) | -- | not read | none | 2026-11-16 02:00 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Sol Central (`confederacy_central_command`) | unknown | not tried | not read | unknown | unknown | 2026-11-16 02:00 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 100: Maximum Security (empire capital) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 02:00 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `main_belt`, `jovian_extraction_zone`, `kuiper_ice_fields`.
