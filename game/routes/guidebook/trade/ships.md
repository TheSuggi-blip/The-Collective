# Trade guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-23. Evidence: table ship_modules; table items (size); table ships (hull by pilot, 2026-11-23 03:33 UTC); browse_ships 2026-11-21 19:55 UTC.

- The Voidborn traders fly the Threshold (cargo 65, fuel 95, hull 75)
  with a mining laser and a pulse laser; some carry a Gas Harvester I or
  a Cargo Expander I (+20 hold), each bought for a mission that paid
  more than it (voidborn-hardware-cargo, voidborn-atmospheric-extraction).
  The Nebula-born fly the Prospect, the Solarian-born the Theoria
  (cargo 72 read on a docked Theoria): table ships, column hull.
- An Ice Harvester I opens the ice routes, which are Mining's.
- An item's size decides a load: `craftbook.py item <id>` or the table
  items, column size (hydrogen gas 1, a cargo expander 10).
- The freighter test (rule F17): one trader bought a listed Prayer
  (cargo 540, no slot) by hand at Ironlight Crossroads (`buy_listed_ship`,
  tool group spacemolt_ship; `browse_ships` with `all_stations` and
  `can_fly`); its Threshold stays stored there. A slotless freighter's
  routes carry `requires.without_module mining_laser_i`, which keeps every
  Threshold off them.
- What a freighter burns a jump and how long it takes are read on its
  first run (`hive.py route <id>`).

### Multi-Empire Ship Catalog (Voidborn, Nebula, Solarian)
Status: proven. Updated: 2026-11-23. Evidence: table hulls; game/catalog/ships/voidborn.md; game/catalog/ships/nebula.md; game/catalog/ships/solarian.md; hive.py guide trade.

Trade operates across three origin empires plus secondhand neutral/Outer Rim bulk hulls. Match fits and upgrades to each empire's yards (`game/catalog/ships/<empire>.md`; `hive.py stats upgrades --member Mercury`):

| Empire | T0 Starter (hold / fuel / slots / CPU / pwr) | T1 Commercial Hulls (Piloting 0) | T2 Commercial Hulls (Piloting 10) |
|---|---|---|---|
| Voidborn | Threshold (65c / 95f / 1W 2D 2U / 16 / 30) | Fugue courier (55c, 2U) | Apophenia freighter (240c, 1W 2D 2U) |
| Nebula | Prospect (100c / 130f / 1W 1D 2U / 13 / 26) | Floor Price freighter (400c, 1U), Dividend (220c, 2U), Leverage (120c, 2U) | Caravan bulk hauler (540c, 3U), Bulk Terms (350c, 2U), Portfolio (300c, 3U) |
| Solarian | Theoria (70c / 100f / 1W 1D 3U / 16 / 28) | Cogito courier (45c, 3U) | Meridian Freighter (265c, 1W 1D 3U), Capacity tanker (80c, 2U) |
| Exchange | Neutral / Outer Rim secondhand (`browse_ships`) | Ledger (480c, 0 slots), Prayer (540c), Worship (1,100c), Congregation (1,900c) | Junk Convoy (850c, 6U), Workhorse (300c, 4U) |

- Fitting rules: strip off-role starter lasers on T0 traders (`Prospect` starts at 100c/2U; `Theoria` holds 3U slots for 3x cargo expanders). Nebula `Floor Price` (400c, Piloting 0) and neutral `Ledger` (480c) scale regional trade long before Piloting 10.
