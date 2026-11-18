# Logistics guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 5.

The starter Threshold carries 65 cargo units and 95 fuel (ship files,
`cargo_capacity` 65, 2026-11-15 21:19 UTC; the rulebook's 66 predates
release 0.715.3, requests.log ENT-038). No other hull or module was
tried: `not measured`. A hauler that mines ice needs an Ice Harvester I
in the mining laser's place: 1,413 cr at home (orders.log ENT-007,
block ZERO), 638 cr at LHS 1140, six lawless jumps away (queue.log
ENT-046), or made by hand (section 11).

A Gas Harvester I goes into the second utility slot beside the mining
laser: one hauler bought and fitted one at Node Beta by the route
`fit-gas-harvester-hauler`, -1,236 cr in 3.7 min (2026-11-16 03:16 UTC,
the ask 1,202 cr). Four haulers carry one (table ship_modules, 2026-11-17 00:09 UTC); their
work is the template `gas-harvest` (section 1.3).

An Ice Harvester I made by hand went into a hauler's second utility slot
beside the mining laser the same way (`withdraw` from storage, then
`install_mod`, docked at Central Nexus, 2026-11-16 09:25 UTC): the Threshold
answer listed 2 utility slots, cpu 8 of 16 and power 17 of 30 in use.

A Cargo Expander I takes a utility slot (cpu 1, power 1, size 10) and lifts
the Threshold's hold from 65 to 85: one hauler bought one at Synchrony Hub for
352 cr in Hardware Optimization: Cargo and flies with it (2026-11-16 13:08 UTC,
get_ship `cargo_capacity` 85). The Threshold has two utility slots: a hauler
that carries a harvester and the mining laser has no room for it.

Next step up: Piloting 10 opens the tier-2 hulls, about 141 hours away at
the haulers' rate (section 4). Until then the step that pays is a tool, not
a hull: an ice harvester puts a hauler on routes measured at 4,000 to 8,400
cr per ship-hour (`hive.py tasks`, 03:28 UTC).

Hulls on the exchange (`browse_ships`, all charted stations, `can_fly` true for a hauler
of ours, 2026-11-17 00:23 UTC; the catalog's figures):

| Hull | Class, tier | Cargo | Speed | Hull, shield | Slots | Cheapest listing |
|---|---|---|---|---|---|---|
| Threshold (ours) | Miner, 0 | 65 | 1 | 75, 80 | 1 weapon, 2 defence, 2 utility | -- |
| Prayer | Freighter, 1 | 540 | 3 | 40, 0 | none | 3,848 cr at Frontier Station (18 jumps); 6,000 at Ironlight Crossroads (6 jumps, 2 listed) |
| Floor Price | Freighter, 1 | 400 | 1 | 55, 15 | 1 utility | 7,479 cr at Trader's Rest (22 jumps) |
| Worship | Freighter, 1 | 1,100 | 2 | 60, 0 | none | 9,741 cr at Deep Range Outpost (19 jumps) |
| Congregation | Bulk Hauler, 1 | 1,900 | 1 | 100, 0 | none | 12,080 cr at First Step Memorial Station (18 jumps) |

A freighter without slots carries no mining laser: it hauls and cannot gather. Buying a
listed ship stores the pilot's present ship at that station (the game's help of
`buy_listed_ship`). No Ledger (480 cargo) was listed; its commission quote asks a docked
ship and was not read. The first hull test is planned (plan file, Planned).
