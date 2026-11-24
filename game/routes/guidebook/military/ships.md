# Military guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-22. Evidence: get_ship 2026-11-17 00:19 UTC; game/catalog/tables/modules.tsv (the live catalog); the tool market (pulse_laser_ii, pulse_laser_iii, shield_booster_i).

The Threshold: 1 weapon, 2 defence, 2 utility slots, CPU 16, power 30,
hull 75, shield 80, armor 3, speed 1. A Mining Laser I (CPU 2, power 5) and
a Pulse Laser I (CPU 2, power 5) leave both defence slots free.

| Module | Stats (catalog) | CPU / power |
|---|---|---|
| Pulse Laser I | 10 energy, reach 3, cooldown 1 | 2 / 5 |
| Pulse Laser II | 18 energy, reach 3, cooldown 1 | 3 / 8 |
| Pulse Laser III | 28 energy, reach 3, cooldown 1 | 5 / 12 |
| Plasma Cannon II | 38 thermal, cooldown 2, +50% to hull | 6 / 14 |
| Shield Booster I | +25 shield | 2 / 4 |

- Prices change by the hour: ask the tool market for the item. Energy
  and plasma weapons need no ammunition; energy gains from Voidborn
  Mastery, thermal cuts the armor of creatures (tests.md, Weapon fits).
- A Pulse Laser III or a Plasma Cannon II and two boosters fit beside
  the mining laser: CPU 11 or 12 of 16, power 25 or 27 of 30.
- The weapon slot holds one weapon: a route's `fit` with `replace` swaps
  it in one docked stop (BLUEPRINT.md).
- A railgun was no faster than the pulse laser on 60-hull grazers
  (2026-11-15).

### Hulls
Status: proven. Updated: 2026-11-24. Evidence: commission_quote Central Nexus 2026-11-16 03:16 UTC and Node Beta 2026-11-22 08:11 UTC, 2026-11-24 01:19 UTC; commission_status 2026-11-24 07:10 UTC; game_docs.py help spacemolt_ship; game/catalog/ships/.

- Tier 1, no Piloting gate: Vigil (patrol, hull 75, shield 90, 2 weapons),
  111,316 cr in credits or 15,706 cr plus materials (87 ticks); Paradox
  (hull 60, shield 130, 2 weapons).
- Tier 2 at Piloting 10: Recursion (hull 150, shield 150, 3 weapons, speed
  4), the drone's next hull; Dualism (160 / 175, 2 weapons, 3 defence).
  Node Beta commissions it for 315,699 cr, or 45,247 cr plus materials
  (commission_quote 2026-11-22 08:11 UTC, default fit two Pulse Laser II);
  asked of the purse (requests ENT-345). The upgrades view names who is 10.
- A credits-only quote is materials, the same again as markup, labor and
  a yard fee (310,897 = 133,138 + 133,138 + 3,600 + 41,021). The yard bids
  under the asks and stalls in SOURCING; `supply_commission` (docked at the
  yard, the owner) donates bought parts and the yard keeps its earmarked
  credits for a refund when sourcing ends: switch_hull.py `--supply`.
- One hull a pilot: a fund spent stays held for its hours and the top-up
  refilled the buyer, so a second commission went out on it;
  commission_hull.py now refuses a pilot with an open commission or a
  stored hull of the class. `cancel_commission` refunds in sourcing; a
  spare hull moves to another pilot by `list_ship_for_sale` at the yard.
- Tier 3 at Piloting 20: Annihilation (4 weapons, hull 360, shield 430),
  Voidborn Singularity (3 weapons); the sentinels go back to the command
  group at 20.
- The pirate hulls `small_claims` (240 hull, 3 weapons) and `larder` (460
  hull, 3 weapons) name no Piloting gate.

### Listed Hulls and Tier-2 Fuel
Status: test. Updated: 2026-11-24. Evidence: browse_ships all_stations=true 2026-11-24 10:27 UTC; table runs 2026-11-24 (Recursion against starters); game/rules/05-galaxy.md (Travel).

- Read the ship exchange before a commission: `browse_ships` with
  `all_stations: true` and `class_id` (free, any docked or flying pilot;
  `can_fly: true` checks Piloting, reputation and fit). Station Managers
  and empire treasuries list fitted hulls at fixed prices: a Recursion at
  Central Nexus for 224,430 cr (the credits-only quote: 313,273), Broadaxes
  of the Crimson treasury at Iron Reach and The Anvil for 36,927 cr with
  five modules, flyable by a Voidborn Piloting-11 pilot.
  `buy_listed_ship` works docked at the listing's station; the old ship
  stays stored there. Script: skill military-turn, buy_listed_hull.py.
- A tier-2 hull burns five to fifteen times a starter's fuel on the same
  hunt (jump fuel goes by ship scale and speed): the Recursion -5,002 cr an
  hour against -382 to -602 for starters; same route, same kills (the herd
  floor caps them). Put tier-2 hulls on work a starter cannot do: kit herds
  above the gauges, pilot whales, pirate formations.

### Multi-Empire Ship Catalog (Voidborn, Crimson, Solarian)
Status: proven. Updated: 2026-11-23. Evidence: table hulls; game/catalog/ships/voidborn.md; game/catalog/ships/crimson.md; game/catalog/ships/solarian.md; hive.py guide military.

Military operates across Voidborn, Crimson, and Solarian fleets. Starter slot geometry differs sharply by empire (`Shard` starts with 2 weapon slots and 1 utility slot), so fit routes must respect hull slots (`game/catalog/ships/<empire>.md`; `hive.py stats upgrades --member Apophis`):

| Empire | T0 Starter (hull / shd / slots / CPU / pwr) | T1 Combat Hulls (Piloting 0) | T2 Combat Hulls (Piloting 10) |
|---|---|---|---|
| Voidborn | Threshold (75h / 80s / 1W 2D 2U / 16 / 30) | Paradox fighter (2W 2D 1U), Vigil patrol (2W 2D 2U) | Recursion fighter (3W 2D 2U), Dualism heavy (2W 3D 2U), Census patrol (2W 2D 3U) |
| Crimson | Shard (110h / 40s / 2W 1D 1U / 12 / 28) | Cleaver fighter (3W 1D 0U), Flail raider (2W 1D 1U, 80c), Mandate patrol (2W 1D 2U) | Halberd assault (4W 2D 1U), Broadaxe heavy (4W 1D 2U), Gauntlet (3W 2D 1U), Trebuchet monitor (2W 6D 2U) |
| Solarian | Theoria (100h / 55s / 1W 1D 3U / 16 / 28) | Axiom fighter (2W 1D 2U, 30c), Corollary fighter (2W 1D 2U), Precept patrol (1W 1D 3U) | Theorem heavy fighter (3W 2D 3U), Postulate drone carrier (1W 2D 4U), Scrutiny patrol (1W 2D 3U) |

- Fitting rules: `Shard` has 2W / 1D / 1U (hull-heavy, low shield: prioritize armor and second weapon, never require 2U mods). `Theoria` has 1W / 1D / 3U (high utility/CPU). Match weapon damage types to each pilot's origin Mastery bonus (`F35`).
