---
name: birchwood
id: 20261117T021122Z
tier: intel
author: Unity
kind: system
system_id: birchwood
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Birchwood

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where birchwood`).

| Field | Value |
|---|---|
| Position | x -5069.4, y -1926.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | alchiba, brightfall, gsc_0014, pinecross, wezen |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `birchwood_star` | Birchwood Star | sun (M2V) | -- | -- | none | 2026-11-17 01:26 UTC | `get_system`, own ship |
| `birchwood_i` | Birchwood I | planet (scorched) | -- | -- | none | 2026-11-17 01:26 UTC | `get_system`, own ship |
| `birchwood_ii` | Birchwood II | planet (arid) | -- | -- | none | 2026-11-17 01:26 UTC | `get_system`, own ship |
| `birchwood_iii` | Birchwood III | planet (terran) | -- | -- | none | 2026-11-17 01:26 UTC | `get_system`, own ship |
| `birchwood_vapor_fields` | Birchwood Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 40, 9370 of 50000 left; argon_gas: richness 33, 50000 of 50000 left; plasma_gas: richness 33, 8910 of 10000 left; neon_gas: richness 52, 50000 of 50000 left; ion_gas: richness 35, 8408 of 10000 left; krypton_gas: richness 14, 3262 of 5000 left | none | 2026-11-17 01:26 UTC | `get_poi`, own ship |

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
| 2026-11-17 01:26 UTC | own ship | Read Birchwood Vapor Fields: 129,950 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
