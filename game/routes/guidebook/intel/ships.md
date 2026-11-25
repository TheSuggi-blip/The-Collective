# Intel guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-25. Evidence: data/fleet/ships/; data/fleet/onetime.json; hive.py spend; catalog tables hulls and items; the books of Central Nexus and Ironlight Crossroads (tool market); fuelplan.ship_jump_cost; stats_money_hour (Intel, 2026-11-24 14:00 to 11-25 04:00 UTC); errors.log ENT-205.

- The Threshold: hold 65, tank 95, hull 75, shield 80, two utility slots.
  Fuel (fuelplan, 2026-11-25): about 3 a jump, 7 with an Afterburner II,
  8.5 with a III, 11 with two; census.py keeps a spare of 20 for the way
  there and on to fuel, and a leg longer than a tank calls at the
  stations between (refuel_hops).
- No afterburner on a scout: while 25 scouts flew 32 of them, Intel's
  fuel went from 16,390-27,074 to 31,572-58,032 cr an hour with no gain
  in freshness, and scouts were towed dry; fit-policy strips them as
  off-role (2026-11-25). A fit is judged by fuel a read, not speed.
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
- A loadout in fit-policy is a standing buy: fit-network buys each
  listed module for every scout with a free slot and the wallet for it.
  In the 7.8 h to 11:08 UTC on 2026-11-25 it spent 195,278 cr on scouts
  (shield boosters, cloaks, a ship scanner), none with a measured gain;
  the loadouts were emptied (34ebb36e). A module returns to a loadout
  only with its gain measured, e.g. fuel a jump of the four scouts that
  carry a fuel optimizer against the rest.
- A new module or hull is tried on two or three scouts first (F37).

### Multi-Empire Ship Catalog (Voidborn, Outer Rim, Nebula)
Status: proven. Updated: 2026-11-23. Evidence: table hulls; game/catalog/ships/voidborn.md; game/catalog/ships/outerrim.md; game/catalog/ships/nebula.md; hive.py guide intel.

Intel scouts operate across Voidborn, Outer Rim, and Nebula space. Outer Rim (`Cobble` 120f) and Nebula (`Prospect` 130f) starters carry larger fuel tanks than `Threshold` (95f), cutting refuel stops on long census loops (`game/catalog/ships/<empire>.md`; `hive.py stats upgrades --member Oracle`):

| Empire | T0 Starter (hold / fuel / slots / CPU / pwr) | T1 Recon / Scout Hulls (Piloting 0) | T2 Recon / Explorer Hulls (Piloting 10) |
|---|---|---|---|
| Voidborn | Threshold (65c / 95f / 1W 2D 2U / 16 / 30) | Eigenstate scout (30c, 2D 3U), Qualia explorer (30c, 2D 3U), Fugue courier (55c, 2U) | Confluence explorer (120c, 1W 2D 4U), Interstice covert recon (40c, 3D 4U), Parallax (40c, 1W 3D 3U) |
| Outer Rim | Cobble (75c / 120f / 1W 1D 2U / 12 / 24) | Warranty Void explorer (40c, 1W 2U), Technically Legal courier (50c, 2U) | Dust Devil blockade runner (95c, 1W 1D 3U), Terms and Conditions smuggler (120c, 1W 1D 3U) |
| Nebula | Prospect (100c / 130f / 1W 1D 2U / 13 / 26) | Venture explorer (80c, 1W 1D 2U), Futures courier (30c, 2U), Margin (70c, 2U) | Prospectus scout (80c, 1W 1D 3U), Arbitrage covert (145c, 1W 1D 3U) |

- Fitting rules: strip `mining_laser_i` and `pulse_laser_i` on T0 scouts (`Threshold`, `Cobble`, `Prospect` all carry 2U slots) to mount `survey_scanner_ii` + mobility/cloak mods. Use high-fuel `Prospect`/`Cobble` hulls on deep frontier census legs and diplomatic envoy relays.
