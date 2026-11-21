# Mining guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-21. Evidence: table hulls (catalog 0.723.2); commission_quote 2026-11-17 11:06 UTC; the tool catalog, ask=build.

- Threshold (tier 0): 2 utility slots, cpu 16, power 30, hold 65. The
  ice miner fits Mining Laser I and Ice Harvester I, a Pulse Laser I in
  the weapon slot: cpu 8 of 16, power 17 of 30.
- Liminal (tier 1, no Piloting): hold 75, ore at half volume, speed 2,
  3 utility slots, cpu 18, power 34, shield 120, hull 65, no weapon
  slot. Priced by `commission_quote` (spacemolt_ship, docked at a yard),
  which differs by yard: 58,589 cr at Node Beta, 83,307 at Central Nexus
  with credits only (2026-11-17). Ordered with `commission.py`; the yard
  buys its missing parts at its own bids (`sourcing`), which a miner can
  feed at the asks (`feed_yard.py`); the pilot switches in only after
  `sourcing` ends.
- Next: tier 2 at Piloting 10, the Resonance Miner (hold 180, 4 utility
  slots, cpu 28, power 48); for ice the Rime (tier 1) and the Hoarfrost
  (tier 2). Hours to Piloting 10: hive.py levels Zero.
- A gather run is a shuttle of loads: the load size sets what a ship
  brings an hour, so the hold is the class's first upgrade.

### Mining tools and filters
Status: proven. Updated: 2026-11-21. Evidence: catalog items; one-run tests of 2026-11-16 (data/routes/runs.jsonl); queue.log ENT-046.

- Mining Laser I (power 5) takes ore and energy crystal; Ice Harvester I
  (power 8) ice; Gas Harvester I gas. A laser alone takes no ice. A fit
  of power 20 or less never locks onto a deposit, so no field refuses it.
- Nitrogen Vent (cpu 4, power 9) in place of the laser lifted the water
  share of an ice load from 59% to 83% (one run each, 2026-11-16).
- Ice Harvester II: by hand from 1 Ice Harvester I, 2 ceramite plating, 3
  liquid nitrogen and 1 power cell (cpu 6, power 12); its gain is not
  measured.
- Extraction filters take one ore out of a pull's draw: Magnetic Ore
  Separator (iron; power 12, cpu 2), Flotation Cell (copper; power 4, cpu
  8), Electromagnetic Refinery (both; power 18, cpu 12). Worth a slot only
  where the rare ore is wanted: half of an iron load is copper, and a
  Liminal's third slot can take a Flotation Cell.
- A gas miner (laser and gas harvester) has no slot left for ice;
  `requires.module` and `requires.without_module` take one value each.

### Buying, refitting and moving goods
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-026; the fit runs of 2026-11-16 (data/routes/runs.jsonl); refit.py and give.py of the skill mining-chains.

- A route that buys a module: one route per station with asks,
  `max_pilots` = the asks at max_price there (`best_sell_qty`), `max_ships`
  1 where they are few. The buy goal answers success when it buys
  nothing, and a `once` run that found nothing counts as done.
- Beyond the border a tool can cost half: Ice Harvester I 687 to 709 cr
  with fuel at Ironlight Crossroads against 1,449 to 1,471 at home
  (2026-11-16).
- When the engine's goal answers 409 for minutes, the raw market `buy`
  takes the best ask at once: read the ask first.
- Refit by hand: `uninstall_mod` docked puts the module in the hold (in
  storage when the hold is full); then `deposit` it so the hold is empty.
  `refit.py --base --off --on --max-price` does both on the first named
  pilot that docks free.
- A hold is space, not units: a cargo row has `size` (tungsten and lead
  ore 2).
- Goods from one of our pilots to another at one station: `deposit`
  (spacemolt_storage) with `source` storage and `target` the other
  pilot; `give.py` flies it there and reads both storages.
