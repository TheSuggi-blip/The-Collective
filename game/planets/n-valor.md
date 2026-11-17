---
name: valor
id: 20261117T174141Z
tier: intel
author: Unity
kind: system
system_id: valor
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 80
updated: 2026-11-17
---

# Valor

Crimson system 19 jumps from home, police level 80. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where valor`).

| Field | Value |
|---|---|
| Position | x 5158.2, y 3394.0 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 19 |
| Lanes | bharani, blood_forge, krynn, stillwater, the_crucible |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `valor_star` | Valor Star | sun (G5V) | -- | -- | none | 2026-11-17 17:10 UTC | `get_system`, own ship |
| `saiph_major_belt` | Saiph Major Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 52, 166 of 30000 left; vanadium_ore: richness 50, 49 of 25000 left; platinum_ore: richness 20, 52 of 8000 left; aluminum_ore: richness 67, 129 of 30000 left; fury_crystal: richness 4, 250 of 250 left | none | 2026-11-17 17:10 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 17:10 UTC | own ship | Read Saiph Major Belt: 646 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
