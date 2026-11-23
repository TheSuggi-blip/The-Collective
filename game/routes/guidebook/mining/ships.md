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
Status: proven. Updated: 2026-11-22. Evidence: catalog 0.732.0 items; docs/guides/miner.md (read 2026-11-21); hive.py route gather-gsc-0027-spacetime-seep (the runs with ore, 2026-11-21 22:00 to 2026-11-22 03:00 UTC); route fit-mining-laser-iii-lhs-1140.

- Laser power: I 5, II 12, III 22, IV 40 (cpu 2, 4, 6, 10). A III fits
  a Threshold ice miner beside its Ice Harvester. Proven (F37): ore an
  hour, III against I, runs of 2026-11-22 03:00 to 11:00 UTC (runs.jsonl
  by module): GSC-0044 belt 1,328 (12 runs) to 467 (52), seep 446 to
  213; far Jishui 176 to 164. It pays near storage; a far shuttle is
  bound by its hold. `fit-mining-laser-iii-lhs-1140`: its ask was bought
  out on 2026-11-22 (tool market, item mining_laser_iii).
- P x F over 20 can lock: under a quarter of capacity a deposit refuses
  the fit below P x 20 / 4 (110 units for a III); 20 or less never locks.
- Cargo Expander I: +20 hold (cpu 1, power 1); not tried yet.
- Ice Harvester I (power 8) ice; Gas Harvester I gas; a laser takes no
  ice. Nitrogen Vent in place of the laser lifted water from 59% to 83%
  of an ice load (2026-11-16).
- Filters take one ore out of the draw: Magnetic Ore Separator (iron),
  Flotation Cell (copper), Electromagnetic Refinery (both); a slot only
  where the rarer ore is wanted.

### Buying, refitting and moving goods
Status: proven. Updated: 2026-11-22. Evidence: errors.log ENT-026; the fit runs of 2026-11-16 (data/routes/runs.jsonl); refit.py and give.py of the skill mining-chains; dispatch.py why_not; commit 73c06c16.

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
- `requires.module` matches one exact id: a refit to a Laser III shut
  its ships out of every gather asking `mining_laser_i`. Gathers ask no
  laser; only a fit route names the module it replaces.
- Goods from one of our pilots to another at one station: `deposit`
  (spacemolt_storage) with `source` storage and `target` the other
  pilot; `give.py` flies it there and reads both storages.

### Multi-Empire Ship Catalog (Voidborn, Solarian, Nebula)
Status: proven. Updated: 2026-11-23. Evidence: table hulls; game/catalog/ships/voidborn.md; game/catalog/ships/solarian.md; game/catalog/ships/nebula.md; hive.py guide mining.

Mining operates across three origin empires. Starter hulls differ in hold, fuel, and utility slots, and each empire unlocks distinct T1/T2 mining, ice, and gas hulls (full live tables: `game/catalog/ships/<empire>.md` and `hive.py stats upgrades --member Zero`):

| Empire | T0 Starter (hold / fuel / slots / CPU / pwr) | T1 Role Hulls (Piloting 0) | T2 Role Hulls (Piloting 10) |
|---|---|---|---|
| Voidborn | Threshold (65c / 95f / 1W 2D 2U / 16 / 30) | Liminal (75c half-vol ore, 3U), Rime (65c ice, 3U), Accretion (65c gas, 4U) | Resonance Miner (180c, 4U), Hoarfrost (170c, 3U), Nebulous (175c, 4U) |
| Solarian | Theoria (70c / 100f / 1W 1D 3U / 16 / 28) | Archimedes (80c, 1W 4U), Glacius (55c ice, 3U), Aether (70c gas, 3U) | Excavation (200c, 1W 3U), Absolute Zero (175c ice, 4U), Nebulae (170c gas, 2U) |
| Nebula | Prospect (100c / 130f / 1W 1D 2U / 13 / 26) | Bonanza (180c, 3U), Frost Dividend (95c ice, 2U), Yield (85c gas, 2U) | Motherlode (200c, 3U), Cold Storage (180c ice, 3U), Revenue (180c gas, 3U) |

- Fitting rules: strip `pulse_laser_i` on T0 miners to unlock full utility slots (`Theoria` carries 3U at T0; `Prospect` carries 100c base hold). `Bonanza` (Nebula T1, 180c/3U) and `Archimedes` (Solarian T1, 4U) are major Piloting-0 upgrades before Piloting 10.
- Neutral exchange: `Workhorse` (T2 multirole, 300c, 4U, Piloting 0) in `game/catalog/ships/pirate-and-other.md`.
