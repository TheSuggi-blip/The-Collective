---
name: trappist_1
id: 20261117T123212Z
tier: intel
author: Unity
kind: system
system_id: trappist_1
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 30
updated: 2026-11-17
---

# TRAPPIST-1

Crimson system 20 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where trappist_1`).

| Field | Value |
|---|---|
| Position | x 4809.1, y 4400.8 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 20 |
| Lanes | bharani, stillwater |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `trappist_1_star` | TRAPPIST-1 Star | sun (M8V) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `trappist_1_i` | TRAPPIST-1 I | planet (ice_world) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `trappist_1_ii` | TRAPPIST-1 II | planet (ice_world) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `trappist_1_gas_pocket` | TRAPPIST-1 Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 47, 780 of 50000 left; argon_gas: richness 53, 16364 of 50000 left; xenon_gas: richness 17, 10000 of 10000 left; nebula_gas: richness 15, 10000 of 10000 left; neon_gas: richness 35, 49998 of 50000 left | none | 2026-11-17 12:16 UTC | `get_poi`, own ship |
| `trappist_1_frost_ring` | TRAPPIST-1 Frost Ring | ice_field (kuiper) | -- | water_ice: richness 53, 28495 of 50000 left; nitrogen_ice: richness 34, 49965 of 50000 left | none | 2026-11-17 12:16 UTC | `get_poi`, own ship |
| `impact_anomaly` | Impact Anomaly | relic (derelict) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `banked_coal_reef` | Banked Coal Reef | asteroid_belt | -- | iron_ore: richness 43, 402 of 100000 left; copper_ore: richness 29, 9769 of 100000 left; plasma_residue: richness 15, 0 of 1291 left | none | 2026-11-17 12:16 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 12:16 UTC | own ship | Read TRAPPIST-1 Gas Pocket: 87,142 units left in all | `get_poi`, own ship |
| 2026-11-17 12:16 UTC | own ship | Read TRAPPIST-1 Frost Ring: 78,460 units left in all | `get_poi`, own ship |
| 2026-11-17 12:16 UTC | own ship | Read Banked Coal Reef: 10,171 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
