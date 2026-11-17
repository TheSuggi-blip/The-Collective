---
name: nihal
id: 20261117T082538Z
tier: intel
author: Unity
kind: system
system_id: nihal
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-17
---

# Nihal

Solarian system 8 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where nihal`).

| Field | Value |
|---|---|
| Position | x -533.5, y 1262.9 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 8 |
| Lanes | bluerift, epsilon_eridani, furud, markab, procyon |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `nihal_star` | Nihal Star | sun (G5II) | -- | -- | none | 2026-11-17 07:44 UTC | `get_system`, own ship |
| `nihal_gas_plume` | Nihal Gas Plume | gas_cloud (molecular_cloud) | -- | argon_gas: richness 33, 49999 of 50000 left; nebula_gas: richness 20, 10000 of 10000 left | none | 2026-11-17 07:44 UTC | `get_poi`, own ship |
| `nihal_containment_fracture` | Nihal Containment Fracture | asteroid_belt | -- | iron_ore: richness 27, 99998 of 100000 left; copper_ore: richness 26, 99999 of 100000 left; antimatter_containment_cell: richness 3, 203 of 203 left | none | 2026-11-17 07:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 07:44 UTC | own ship | Read Nihal Gas Plume: 59,999 units left in all | `get_poi`, own ship |
| 2026-11-17 07:44 UTC | own ship | Read Nihal Containment Fracture: 200,200 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
