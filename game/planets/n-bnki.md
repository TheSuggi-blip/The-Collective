---
name: bnki
id: 20261117T082525Z
tier: intel
author: Unity
kind: system
system_id: bnki
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# BNKI

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where bnki`).

| Field | Value |
|---|---|
| Position | x 601.2, y 3947.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | pipirima |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `bnki_star` | BNKI Star | sun (M4V) | -- | -- | none | 2026-11-17 08:10 UTC | `get_system`, own ship |
| `the_interloper` | The Interloper | planet (glacial) | -- | -- | none | 2026-11-17 08:10 UTC | `get_system`, own ship |
| `swarm_fragment_theta` | Swarm Fragment Theta | asteroid_belt (carbonaceous) | -- | silicon_ore: richness 44, 6 of 8000 left; nickel_ore: richness 20, 0 of 5000 left | none | 2026-11-17 08:10 UTC | `get_poi`, own ship |
| `swarm_fragment_kappa` | Swarm Fragment Kappa | asteroid_belt (carbonaceous) | -- | silicon_ore: richness 38, 32 of 8000 left; iron_ore: richness 25, 89 of 10000 left | none | 2026-11-17 08:10 UTC | `get_poi`, own ship |
| `swarm_fragment_sigma` | Swarm Fragment Sigma | asteroid_belt (carbonaceous) | -- | silicon_ore: richness 41, 13 of 8000 left | none | 2026-11-17 08:10 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:10 UTC | own ship | Read Swarm Fragment Theta: 6 units left in all | `get_poi`, own ship |
| 2026-11-17 08:10 UTC | own ship | Read Swarm Fragment Kappa: 121 units left in all | `get_poi`, own ship |
| 2026-11-17 08:10 UTC | own ship | Read Swarm Fragment Sigma: 13 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
