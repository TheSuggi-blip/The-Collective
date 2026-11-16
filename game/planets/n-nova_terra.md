---
name: nova_terra
id: 20261116T033547Z
tier: intel
author: Unity
kind: system
system_id: nova_terra
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: solarian
police_level: 55
updated: 2026-11-16
---

# Nova Terra

Solarian system 8 jumps from home, police level 55. Station: Nova Terra Central.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where nova_terra`).

| Field | Value |
|---|---|
| Position | x -799.5, y 597.3 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 8 |
| Lanes | epsilon_eridani, furud, lacaille_9352, procyon, sirius |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sol_secundus` | Sol Secundus | sun (G3V) | -- | -- | none | 2026-11-16 03:20 UTC | `get_system`, own ship |
| `nova_terra_prime` | Nova Terra Prime | planet (terran) | -- | -- | none | 2026-11-16 03:20 UTC | `get_system`, own ship |
| `nova_terra_ii` | Nova Terra II | planet (terran) | -- | -- | none | 2026-11-16 03:20 UTC | `get_system`, own ship |
| `nova_terra_iii` | Nova Terra III | planet (arid) | -- | -- | none | 2026-11-16 03:20 UTC | `get_system`, own ship |
| `nova_terra_industrial_belt` | Nova Terra Industrial Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 47, 0 of 30000 left; tungsten_ore: richness 45, 0 of 25000 left; iridium_ore: richness 21, 0 of 5000 left; thorium_ore: richness 18, 0 of 5000 left; lead_ore: richness 12, 0 of 10000 left; aluminum_ore: richness 42, 0 of 30000 left; legacy_ore: richness 4, 0 of 200 left | none | 2026-11-16 03:20 UTC | `get_poi`, own ship |
| `nova_terra_gas_plume` | Nova Terra Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 42, 3666 of 50000 left; argon_gas: richness 43, 5736 of 50000 left; ion_gas: richness 13, 1721 of 10000 left | none | 2026-11-16 03:20 UTC | `get_poi`, own ship |
| `nova_terra_ice_shelf` | Nova Terra Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 61, 2519 of 50000 left; deuterium_ice: richness 18, 742 of 5000 left; helium_ice: richness 14, 798 of 5000 left | none | 2026-11-16 03:20 UTC | `get_poi`, own ship |
| `nova_terra_central` | Nova Terra Central | station | `nova_terra_central` | -- | none | 2026-11-16 03:20 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Nova Terra Central (`nova_terra_central`) | Solarian empire | docked 2026-11-16 03:22 UTC by a Voidborn ship with an empty hold | market and mission board (both read) | market price plus a Solarian surcharge of 6 cr a unit | listing 2%; foreign buyers pay 3% sales tax | 2026-11-16 03:22 UTC | census RESULT line; `get_empire_info` (solarian) |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 03:20 UTC | own ship | Read Nova Terra Industrial Belt: nothing left | `get_poi`, own ship |
| 2026-11-16 03:20 UTC | own ship | Read Nova Terra Gas Plume: 11,123 units left in all | `get_poi`, own ship |
| 2026-11-16 03:20 UTC | own ship | Read Nova Terra Ice Shelf: 4,059 units left in all | `get_poi`, own ship |
| 2026-11-16 03:22 UTC | own ship | Docked at Nova Terra Central with an empty hold: order book of 517 items (197 asks, 391 bids) and a board of 7 missions saved; the round trip from Central Nexus cost 304 cr in about 25 minutes | census RESULT line; `/srv/collective/data/market/nova_terra_central.json` |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Oracle, 2026-11-16: the nearest Solarian market, 8 jumps from Nexus Prime by Pherkad, GSC-0041, Antares, Homam and Furud. Its book against our six of 03:20 to 03:36 UTC: 16 price gaps; the deepest is argon gas, 1 cr against our 2 cr for 73 units, and every other closes after 1 to 6 units at our end. Deuterium ice is offered at 120 cr for 6,138 units, where our best bid holds 5 units; control nodes at 674 cr for 66, where a bid of 1,155 cr for 123 at Node Gamma Relay Station (01:43 UTC) had fallen to 41 cr for 20 by 03:19 UTC; with the 3% foreign tax nothing else is cheaper than our own books by more than a few units. Ice Harvester I stands at 2,600 cr and Gas Harvester I at 1,202 cr, no cheaper than at home.
- Solarian law (`get_empire_info`, policy read 2026-11-16): contraband ghost_rounds, gutter_flux, hot_cell, nerve_burn, pirate_moonshine, red_mist, starshine, void_dust, seized with a fine of twice their value on inspection; an attack in policed space carries a 500 cr bounty, a kill 2,000 cr; repair 5 cr a hull point.
- No base site: the system is Solarian and policed; a station or an outpost of our own needs a lawless system (`game/rules/09-factions.md`).
- The board offered Deep Space Cartography (4,000 cr: visit The Crucible and Horizon, 16 and 12 jumps from here in Crimson and Outer Rim space) and two trade runs to Crimson stations; none is in reach of a starter's 95 units of fuel without refuelling on the way.
