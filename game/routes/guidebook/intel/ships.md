# Intel guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-21. Evidence: data/fleet/ships/; catalog tables hulls and items; the books of Central Nexus and Ironlight Crossroads (tool market).

- The Threshold: hold 65, tank 95, hull 75, shield 80, two utility slots;
  the mining laser takes one. Fuel: one unit a jump and one a leg inside
  a system; a round trip six jumps out used 15 units (2026-11-15). A far
  list is cut so that start, target and home stay under about 60 jumps.
- A census refuels at every station it docks and, on `--stay`, starts its
  next read from there: a station that sells no fuel is no place to end
  (data/station/stations.json, services).
- Survey Scanner I (utility, survey power 30): the only fit that trains
  scanning. Each extra scanner adds 50% of the one before; a survey probe
  or an anomaly detector adds its power (the game's help for
  survey_system). Survey Scanner II is sold in Solarian books.
- Ship Scanner I (utility) counts the ships at every place of a system:
  the next fit for pirate readings, not tried yet.
- Fuel beyond the border is cheaper than at home (Hive Antares,
  Ironlight Crossroads; tool market, item fuel).
- A new module or hull is tried on one scout first (rule F17).

### Multi-Empire Ship Catalog (Voidborn, Outer Rim, Nebula)
Status: proven. Updated: 2026-11-23. Evidence: table hulls; game/catalog/ships/voidborn.md; game/catalog/ships/outerrim.md; game/catalog/ships/nebula.md; hive.py guide intel.

Intel scouts operate across Voidborn, Outer Rim, and Nebula space. Outer Rim (`Cobble` 120f) and Nebula (`Prospect` 130f) starters carry larger fuel tanks than `Threshold` (95f), cutting refuel stops on long census loops (`game/catalog/ships/<empire>.md`; `hive.py stats upgrades --member Oracle`):

| Empire | T0 Starter (hold / fuel / slots / CPU / pwr) | T1 Recon / Scout Hulls (Piloting 0) | T2 Recon / Explorer Hulls (Piloting 10) |
|---|---|---|---|
| Voidborn | Threshold (65c / 95f / 1W 2D 2U / 16 / 30) | Eigenstate scout (30c, 2D 3U), Qualia explorer (30c, 2D 3U), Fugue courier (55c, 2U) | Confluence explorer (120c, 1W 2D 4U), Interstice covert recon (40c, 3D 4U), Parallax (40c, 1W 3D 3U) |
| Outer Rim | Cobble (75c / 120f / 1W 1D 2U / 12 / 24) | Warranty Void explorer (40c, 1W 2U), Technically Legal courier (50c, 2U) | Dust Devil blockade runner (95c, 1W 1D 3U), Terms and Conditions smuggler (120c, 1W 1D 3U) |
| Nebula | Prospect (100c / 130f / 1W 1D 2U / 13 / 26) | Venture explorer (80c, 1W 1D 2U), Futures courier (30c, 2U), Margin (70c, 2U) | Prospectus scout (80c, 1W 1D 3U), Arbitrage covert (145c, 1W 1D 3U) |

- Fitting rules: strip `mining_laser_i` and `pulse_laser_i` on T0 scouts (`Threshold`, `Cobble`, `Prospect` all carry 2U slots) to mount `survey_scanner_ii` + mobility/cloak mods. Use high-fuel `Prospect`/`Cobble` hulls on deep frontier census legs and diplomatic envoy relays.
