# Logistics guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-21. Evidence: ship files 2026-11-15 21:19 UTC (requests.log ENT-038); fit-gas-harvester-hauler 2026-11-16 03:16 UTC; install_mod and get_ship 2026-11-16 09:25 and 13:08 UTC; orders.log ENT-007; queue.log ENT-046; rule F23.

- The Threshold: cargo 65 (the rulebook's 66 predates release 0.715.3), fuel 95, 2 utility slots; with a harvester beside the mining laser it read cpu 8 of 16, power 17 of 30. No other hull tried: `not measured`.
- A module goes in docked: `withdraw` it from storage to the hold, then `install_mod {"module_id": ...}`.
- Cargo Expander I: one utility slot (cpu 1, power 1, size 10), hold 65 -> 85; bought at Synchrony Hub for 352 cr. The hauler's first fit: a hauler with a harvester and the mining laser has no room for it.
- Harvesters: an Ice Harvester I (1,413 cr at home, 638 at LHS 1140, or made by hand) and a Gas Harvester I (1,202 cr at Node Beta) each took the second utility slot (2026-11-16). Haulers no longer gather (rule F23).
- Next step up: Piloting 10 opens tier 2 (hours to it: the tool fleet, view=levels); tier 1 asks no Piloting.

### Hulls on the exchange
Status: proven. Updated: 2026-11-21. Evidence: browse_ships, all charted stations, can_fly true for a hauler, 2026-11-17 00:23 UTC; the catalog's figures; the help of buy_listed_ship.

| Hull | Class, tier | Cargo | Speed | Hull, shield | Slots | Cheapest listing (2026-11-17) |
|---|---|---|---|---|---|---|
| Threshold (ours) | Miner, 0 | 65 | 1 | 75, 80 | 1 weapon, 2 defence, 2 utility | -- |
| Prayer | Freighter, 1 | 540 | 3 | 40, 0 | none | 3,848 cr at Frontier Station (18 jumps); 6,000 at Ironlight Crossroads (6) |
| Floor Price | Freighter, 1 | 400 | 1 | 55, 15 | 1 utility | 7,479 cr at Trader's Rest (22) |
| Worship | Freighter, 1 | 1,100 | 2 | 60, 0 | none | 9,741 cr at Deep Range Outpost (19) |
| Congregation | Bulk Hauler, 1 | 1,900 | 1 | 100, 0 | none | 12,080 cr at First Step Memorial Station (18) |

- A freighter without slots carries no mining laser. Buying a listed ship stores the pilot's present ship at that station.
- Ledger (480): a prestige hull; `commission_quote` answers `achievement_required` (the faction must have earned the "Syndicate" achievement; Central Nexus, 2026-11-22 20:08 UTC). Apophenia (240, Piloting 10): 433,072 cr credits only, or 60,444 cr with eleven parts we lack (shield emitters, void nanite suspension, phase matrix ...), same quote. Listings: `browse_ships` (group spacemolt_ship, free) with `all_stations`, `class_id`, `can_fly` true.
