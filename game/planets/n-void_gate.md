---
name: void_gate
id: 20261117T184357Z
tier: intel
author: Unity
kind: system
system_id: void_gate
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 30
updated: 2026-11-17
---

# Void Gate

Outerrim system 19 jumps from home, police level 30. Station: Void Gate Outpost, Mobile Capital.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where void_gate`).

| Field | Value |
|---|---|
| Position | x -2021.9, y -3142.8 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 19 |
| Lanes | first_step, haedus, kochab, markeb, starfall, sulafat |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `the_red_lantern` | The Red Lantern | sun (M0III) | -- | -- | none | 2026-11-17 18:39 UTC | `get_system`, own ship |
| `void_gate_i` | Void Gate I | planet (scorched) | -- | -- | none | 2026-11-17 18:39 UTC | `get_system`, own ship |
| `void_gate_ii` | Void Gate II | planet (glacial) | -- | -- | none | 2026-11-17 18:39 UTC | `get_system`, own ship |
| `void_gate_mineral_fields` | Void Gate Mineral Fields | asteroid_belt (mixed) | -- | carbon_ore: richness 42, 0 of 30000 left; vanadium_ore: richness 43, 0 of 25000 left; tungsten_ore: richness 33, 0 of 25000 left; iridium_ore: richness 24, 0 of 5000 left | none | 2026-11-17 18:39 UTC | `get_poi`, own ship |
| `void_gate_outpost` | Void Gate Outpost | station | `void_gate_outpost` | -- | none | 2026-11-17 18:39 UTC | `get_system`, own ship |
| `mobile_capital` | Mobile Capital | station | `frontier_station` | -- | none | 2026-11-17 18:39 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Void Gate Outpost (`void_gate_outpost`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 18:39 UTC | `get_system`, own ship |
| Mobile Capital (`frontier_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 18:39 UTC | `get_system`, own ship |

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
| 2026-11-17 18:39 UTC | own ship | Read Void Gate Mineral Fields: nothing left | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
