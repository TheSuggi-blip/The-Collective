# Trade guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-21. Evidence: table ship_modules; the fit and module mission routes; browse_ships 2026-11-21 19:55 UTC.

- Every trader flies the Threshold (cargo 65, fuel 95, hull 75) with a
  mining laser and a pulse laser; three carry a Gas Harvester I and some
  a Cargo Expander I (+20 hold; 352 cr at Synchrony Hub, 173 at Ironlight
  Crossroads), each bought for a mission that paid more than it
  (voidborn-hardware-cargo, voidborn-atmospheric-extraction).
- An Ice Harvester I opens the ice routes, which are Mining's.
- An item's size decides a load: `craftbook.py item <id>` (hydrogen gas
  reads size 1 in catalog 0.723.2).
- The freighter test (2026-11-21, rule F17): one trader docks at
  Ironlight Crossroads with an empty hold (go-ironlight-trader) and buys
  a listed Prayer by hand (`buy_listed_ship`, tool group spacemolt_ship,
  docked there; `browse_ships` lists the listings with `all_stations`
  and `can_fly`). The Threshold stays stored at that station with its
  modules. A slotless freighter's routes carry `requires.without_module
  mining_laser_i`, which keeps every Threshold off them
  (carry-hydrogen-beta-to-crucible-bulk).
- What a freighter burns a jump and how long it takes are read on its
  first run (`hive.py route <id>`).
