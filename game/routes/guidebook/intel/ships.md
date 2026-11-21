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
