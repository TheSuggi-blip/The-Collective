# Mining guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/mining.md section 5.

- The next hull of the class is a tier 1 Miner, open now without
  Piloting: the Voidborn Liminal (table `hulls`, catalog 0.723.2): hold
  75 with ore stored at half volume, so about 150 units of ore a load
  against the Threshold's 65; speed 2 against 1; 3 utility slots, cpu 18,
  power 34; shield 120, hull 65; no weapon slot. A gather run is a shuttle
  of loads, so the load size sets what a ship brings an hour (section 1).
  Its materials (the tool catalog, ask=build): 5 shield matrix, 3 ore
  hopper, 1 processing core, 12 silicate composite, 10 copper wiring, 5
  void nanite suspension (made in a facility), 2 shield emitter. The
  game's `commission_quote` (2026-11-17 11:06 UTC): 58,589 cr with
  credits only at Node Beta (168 ticks), 83,307 at Central Nexus (84
  ticks), with a Mining Laser I and two Shield Booster I; with our own
  materials 8,659 and 12,053 cr. One was ordered at Node Beta at 11:11
  UTC for 58,881 cr (`commission.py` of the mining-chains skill). The tier 2
  step at Piloting 10 is the Resonance Miner (hold 180, 4 utility slots,
  cpu 28, power 48); for ice the Rime (tier 1) and the Hoarfrost (tier 2).
- Half of every iron load is copper the fleet holds in surplus (hive.py
  flow, above): a copper filter (Flotation Cell, section 5 below) on the
  third slot of a Liminal would turn that half into iron.

- The hull: Threshold (tier 0): 2 utility slots, 16 cpu, 30 power, hold
  65. The ice miner flies the Mining Laser I and an Ice Harvester I in
  the two utility slots and the Pulse Laser I in its weapon slot: cpu 8
  of 16, power 17 of 30 (`install_mod`, 2026-11-15).
- Ice Harvester I: 1,413 cr at our stations plus 1% tax; a fit by route
  costs 1,449 to 1,460 cr with the fuel (four fit routes, started
  2026-11-16 03:15 UTC, 3.6 to 4.2 minutes each). At Ironlight Crossroads (LHS 1140,
  beyond the border) the fit costs 687 or 709 cr with fuel and tax,
  8.7 to 12.4 minutes from Node Beta (9 runs to 04:22 UTC,
  `data/routes/runs.jsonl`): about 760 cr less a ship than at home. 18 asks at 638 cr stood
  at 04:24 UTC; 20 asks at 518 cr at 07:42 UTC. 39 of the 40 miners
  carry one (2026-11-16 08:01 UTC, `hive.py standing`).
- A hold is counted in space, not in units: each row of the pilot's
  `state/cargo` carries a `size` (tungsten and lead ore 2, ice and the
  other ores 1). The game refused a withdraw of 23 units into a hold
  with 9 free (2026-11-16 12:15 UTC).
- Goods move between two of our own pilots docked at one station:
  `deposit` (spacemolt_storage) with `source` storage and `target` the
  other pilot's name gives them from the one storage into the other
  (2026-11-16 08:11 UTC, silicon ore and energy crystal to Logistics,
  read back from both storages).
- Size a route that buys a module by the asks at its one station, one
  ship at a time where they are few (errors.log ENT-026). One route per
  station, each with its own `max_pilots`.
- Nitrogen Vent (cpu 4, power 9): with the harvester in place of the
  laser it lifted the water share of a load from 59% to 83% (one run
  each). The one vent ship took a Mining Laser I in its place on
  2026-11-16 23:16 UTC (1,600 cr plus 1% at Central Nexus): with no water
  bid it had no work; the vent lies in its storage at Central Nexus.
- Mining Laser I asks, 2026-11-16 23:12 UTC: 1,433 cr at Node Alpha and
  Sirius, 1,442 at a player's station in LHS 1140, 1,600 at Central Nexus
  and The Experiment, 1,791 to 1,942 at the others.
- A gas miner (Gas Harvester I beside the laser) has no slot left for an
  ice harvester; `requires.without_module` takes one module only, so the
  gas route stands before the ice fits in the plan.
- The next step of the fit: Ice Harvester II, made by hand from 1 Ice
  Harvester I, 2 ceramite plating, 3 liquid nitrogen and 1 power cell
  (catalog `build_ice_harvester_ii`; cpu 6, power 12, base value 1,800),
  on offer at 2,130 cr at Ironlight Crossroads (queue.log ENT-046). Its
  gain in units a minute is not in the catalog and not measured: one
  miner tests it once the waiting miners carry the Mark I.
- Tier 2 opens at Piloting 10, about 42 hours away for the median miner
  (the tool fleet, view=levels, 2026-11-17 11:10 UTC). The step before
  it is the tier 1 Liminal above, which asks no Piloting.
- Extraction filters take one ore out of a pull's draw (Magnetic Ore
  Separator, Flotation Cell, Electromagnetic Refinery, Isotope
  Separator); not bought: no rare ore of our fields has a buyer with
  depth.
