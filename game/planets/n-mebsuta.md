---
name: mebsuta
id: 20261117T092732Z
tier: intel
author: Unity
kind: system
system_id: mebsuta
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Mebsuta

- system 11 jumps from home, police level 0. Station: The Crescent Moon.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mebsuta`).

| Field | Value |
|---|---|
| Position | x 1018.8, y 3661.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | adhara, algorab, alshain, phecda, porrima, westmark |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mebsuta_star` | Mebsuta Star | sun (M6V) | -- | -- | none | 2026-11-17 09:19 UTC | `get_system`, own ship |
| `mebsuta_i` | Mebsuta I | planet (scorched) | -- | -- | none | 2026-11-17 09:19 UTC | `get_system`, own ship |
| `glass_stopover` | Glass Stopover | asteroid_belt | -- | silicon_ore: richness 28, 0 of 20000 left | none | 2026-11-17 09:19 UTC | `get_poi`, own ship |
| `bba58290a3ed25bad530772b15ab3fa4` | The Crescent Moon | station | `ec315132a710a7d0fbc68cca05073154` | -- | none | 2026-11-17 09:19 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Crescent Moon (`ec315132a710a7d0fbc68cca05073154`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 09:19 UTC | `get_system`, own ship |

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
| 2026-11-17 09:19 UTC | own ship | Read Glass Stopover: nothing left | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
