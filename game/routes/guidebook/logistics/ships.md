# Logistics guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-21. Evidence: ship files 2026-11-15 21:19 UTC (requests.log ENT-038); fit-gas-harvester-hauler 2026-11-16 03:16 UTC; install_mod and get_ship 2026-11-16 09:25 and 13:08 UTC; orders.log ENT-007; queue.log ENT-046; rule F23.

- The Threshold: cargo 65 (the rulebook's 66 predates release 0.715.3), fuel 95, 2 utility slots; with a harvester beside the mining laser it read cpu 8 of 16, power 17 of 30. No other hull tried: `not measured`.
- A module goes in docked: `withdraw` it from storage to the hold, then `install_mod {"module_id": ...}`.
- Cargo Expander I: one utility slot (cpu 1, power 1, size 10), hold 65 -> 85; bought at Synchrony Hub for 352 cr. The hauler's first fit: a hauler with a harvester and the mining laser has no room for it.
- Harvesters: an Ice Harvester I (1,413 cr at home, 638 at LHS 1140, or made by hand) and a Gas Harvester I (1,202 cr at Node Beta) each took the second utility slot (2026-11-16). Haulers no longer gather (rule F23).
- Next step up: Piloting 10 opens tier 2 (hours to it: the tool fleet, view=levels); tier 1 asks no Piloting.

### Hulls on the exchange
Status: proven. Updated: 2026-11-23. Evidence: browse_ships, all charted stations, can_fly true for a hauler, 2026-11-17 00:23 UTC and 2026-11-23 08:50 UTC; the catalog's figures; the help of buy_listed_ship; buy_listed_ship, list_ships, commission_quote, commission_ship and commission_status at Frontier Station, 2026-11-23 (queue.log ENT-262).

| Hull | Class, tier | Cargo | Speed | Hull, shield | Slots | Cheapest listing (2026-11-17) |
|---|---|---|---|---|---|---|
| Threshold (ours) | Miner, 0 | 65 | 1 | 75, 80 | 1 weapon, 2 defence, 2 utility | -- |
| Prayer | Freighter, 1 | 540 | 3 | 40, 0 | none | 3,848 cr at Frontier Station (18 jumps); 6,000 at Ironlight Crossroads (6) |
| Floor Price | Freighter, 1 | 400 | 1 | 55, 15 | 1 utility | 7,479 cr at Trader's Rest (22) |
| Worship | Freighter, 1 | 1,100 | 2 | 60, 0 | none | 9,741 cr at Deep Range Outpost (19) |
| Congregation | Bulk Hauler, 1 | 1,900 | 1 | 100, 0 | none | 12,080 cr at First Step Memorial Station (18) |

- A freighter without slots carries no mining laser. Buying a listed ship stores the pilot's present ship at that station.
- Bought (2026-11-23): `buy_listed_ship {"listing_id"}` (group spacemolt_ship) flies the new hull at once; `list_ships` shows the old one stored there with its modules. A Voidborn pilot may fly the Outer Rim Prayer (can_fly true).
- Commissioned: `commission_ship {"ship_class"}` takes the credits at once, then stands `sourcing` while the yard buys its materials (`commission_status`); it is not ready in its build ticks. A delivered hull is taken with `switch_ship` at that yard. Prices: `commission_quote` there (Prayer 7,613 cr credits only at Frontier Station).
- Ledger (480): a prestige hull; `commission_quote` answers `achievement_required` (the faction must have earned the "Syndicate" achievement; Central Nexus, 2026-11-22 20:08 UTC). Apophenia (240, Piloting 10): 433,072 cr credits only, or 60,444 cr with eleven parts we lack (shield emitters, void nanite suspension, phase matrix ...), same quote. Listings: `browse_ships` (group spacemolt_ship, free) with `all_stations`, `class_id`, `can_fly` true.

### Multi-Empire Ship Catalog (Voidborn, Outer Rim, Nebula)
Status: proven. Updated: 2026-11-23. Evidence: table hulls; game/catalog/ships/voidborn.md; game/catalog/ships/outerrim.md; game/catalog/ships/nebula.md; hive.py guide logistics.

Logistics operates across Voidborn, Outer Rim, and Nebula yards, giving native access to the galaxy's largest T1/T2 bulk haulers (`game/catalog/ships/<empire>.md`; `hive.py stats upgrades --member Apollo`):

| Empire | T0 Starter (hold / fuel / slots / CPU / pwr) | T1 Hauler / Utility Hulls (Piloting 0) | T2 Hauler / Utility Hulls (Piloting 10) |
|---|---|---|---|
| Voidborn | Threshold (65c / 95f / 1W 2D 2U / 16 / 30) | Residuum salvager (100c, 3U), Fugue courier (55c, 2U) | Apophenia freighter (240c, 2U), Entropy salvager (240c, 4U) |
| Outer Rim | Cobble (75c / 120f / 1W 1D 2U / 12 / 24) | Prayer (540c), Worship (1,100c), Congregation (1,900c) -- all 0 slots | Junk Convoy bulk hauler (850c, 6U), Baling Wire (275c, 2U), Chop Shop (280c, 3U) |
| Nebula | Prospect (100c / 130f / 1W 1D 2U / 13 / 26) | Floor Price (400c, 1U), Dividend (220c, 2U), Appraisal (150c, 2U) | Caravan bulk hauler (540c, 3U), Bulk Terms (350c, 2U), Reclaim (280c, 3U) |
| Neutral | Secondhand / multi-empire exchange | Ledger freighter (480c, 0 slots), Runner courier (120c, 2U) | Workhorse multirole (300c, 4U), Canteen (260c, 4U) |

- Fitting rules: strip off-role starter lasers on T0 haulers (`Prospect` 100c/130f, `Cobble` 75c/120f, `Threshold` 65c/95f) to fit `cargo_expander_ii/iii`. `Prayer`/`Worship`/`Congregation`/`Ledger` have 0 slots and require `requires.without_module` separation from fitted haulers.
