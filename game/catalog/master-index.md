---
name: catalog-master-index
id: 20261116T001239Z
tier: intel
author: Unity
---

# master-index.md -- The Game's Catalog

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.732.3; never edited by hand.
Start here: every name below is a link into one of the sub-indexes of this folder.
Recipes: 892. Facilities: 2953. Hulls: 385. Modules: 270. Items: 879. Skills: 30.

- Ask a question instead of reading a table: `python3 -I -B game/fleet/craftbook.py` from the
  repository root. `item <text>` finds an item, how it is made and what uses it; `needs <item>
  [quantity]` prints everything it takes down to what is mined or bought, beside what the fleet
  has in storage; `build <facility or hull>` does the same for a building or a ship; `can` lists
  what your division's stored goods can be made into by hand today, and what that sells for.
- A figure here is the game's own. What something sells for is not here: the order books are
  in the unit's data folder (`game/fleet/ledger.py prices <item>`).

## Recipes by Category

| Category | Recipes | By hand | In a facility only |
|---|---|---|---|
| [Chemical Synthesis](recipes/chemical-synthesis.md) | 50 | 18 | 32 |
| [Cooking](recipes/cooking.md) | 48 | 45 | 3 |
| [Armor & Shield Manufacturing](recipes/armor-shield-manufacturing.md) | 46 | 33 | 13 |
| [Rendering](recipes/rendering.md) | 44 | 39 | 5 |
| [Smelting](recipes/smelting.md) | 37 | 16 | 21 |
| [Brewing & Distilling](recipes/brewing-distilling.md) | 36 | 29 | 7 |
| [Crystal Growing & Glasswork](recipes/crystal-growing-glasswork.md) | 35 | 23 | 12 |
| [Electronics Assembly](recipes/electronics-assembly.md) | 35 | 19 | 16 |
| [Exotic Containment](recipes/exotic-containment.md) | 35 | 2 | 33 |
| [Habitat Outfitting](recipes/habitat-outfitting.md) | 35 | 23 | 12 |
| [Machining](recipes/machining.md) | 35 | 29 | 6 |
| [Ammunition Loading](recipes/ammunition-loading.md) | 29 | 26 | 3 |
| [Mining Gear Fabrication](recipes/mining-gear-fabrication.md) | 27 | 19 | 8 |
| [Refinery Module Fitting](recipes/refinery-module-fitting.md) | 27 | 5 | 22 |
| [Beam Weapon Tuning](recipes/beam-weapon-tuning.md) | 26 | 7 | 19 |
| [Gunsmithing](recipes/gunsmithing.md) | 26 | 8 | 18 |
| [Shipbuilding](recipes/shipbuilding.md) | 26 | 15 | 11 |
| [Nuclear Enrichment](recipes/nuclear-enrichment.md) | 25 | 1 | 24 |
| [Reactor & Hull Fitting](recipes/reactor-hull-fitting.md) | 25 | 21 | 4 |
| [Field Kit Assembly](recipes/field-kit-assembly.md) | 23 | 10 | 13 |
| [Fold Engineering](recipes/fold-engineering.md) | 22 | 1 | 21 |
| [Packing & Crating](recipes/packing-crating.md) | 22 | 1 | 21 |
| [Pharmaceutical Compounding](recipes/pharmaceutical-compounding.md) | 22 | 5 | 17 |
| [Scrap Reclamation](recipes/scrap-reclamation.md) | 21 | 15 | 6 |
| [Plasma & Void Forging](recipes/plasma-void-forging.md) | 16 | 0 | 16 |
| [Cloak & Jammer Rigging](recipes/cloak-jammer-rigging.md) | 15 | 11 | 4 |
| [Engine & Hold Fitting](recipes/engine-hold-fitting.md) | 15 | 13 | 2 |
| [Sensor Calibration](recipes/sensor-calibration.md) | 15 | 10 | 5 |
| [Drone Building](recipes/drone-building.md) | 14 | 14 | 0 |
| [Fuel Blending](recipes/fuel-blending.md) | 14 | 4 | 10 |
| [Gas Separation](recipes/gas-separation.md) | 13 | 7 | 6 |
| [Hydroponic Farming](recipes/hydroponic-farming.md) | 12 | 6 | 6 |
| [Ice Melting](recipes/ice-melting.md) | 11 | 4 | 7 |
| [Ship Passive](recipes/ship-passive.md) | 10 | 0 | 10 |

## Bases and Facilities

| Group | Entries | Holds |
|---|---|---|
| [Founding a Base](facilities.md#founding-a-base) | 2 | the kit of an outpost, the core of a station |
| [Defense](facilities.md#defense) | 14 | -- |
| [Faction](facilities.md#faction) | 56 | faction_admin, faction_commons, faction_company_store, faction_espionage, faction_fuel, faction_intel, faction_market, faction_marque, faction_medical, faction_ |
| [Infrastructure](facilities.md#infrastructure) | 104 | police |
| [Personal](facilities.md#personal) | 13 | drone_control, quarters, trader_office, workshop |
| [Ranch](facilities.md#ranch) | 3 | -- |
| [Service](facilities.md#service) | 97 | crafting, marine_training, market, medical, missions, personnel, refuel, repair, salvage_yard, shipyard, storage |
| [Production](facilities.md#production) | 2666 | one recipe each; the full list is `tables/facilities.tsv` |

## Hulls by Empire

The Piloting a tier needs: tier 2: Piloting 10; tier 3: Piloting 20; tier 4: Piloting 30; tier 5: Piloting 50.

| Empire | Hulls | Hulls per tier |
|---|---|---|
| [voidborn](ships/voidborn.md) | 65 | 0: 1, 1: 11, 2: 15, 3: 18, 4: 13, 5: 7 |
| [crimson](ships/crimson.md) | 68 | 0: 1, 1: 13, 2: 18, 3: 15, 4: 16, 5: 5 |
| [nebula](ships/nebula.md) | 66 | 0: 1, 1: 13, 2: 13, 3: 19, 4: 13, 5: 7 |
| [outerrim](ships/outerrim.md) | 68 | 0: 1, 1: 14, 2: 19, 3: 15, 4: 14, 5: 5 |
| [pirate and other](ships/pirate-and-other.md) | 53 | 1: 9, 2: 14, 3: 16, 4: 14 |
| [solarian](ships/solarian.md) | 65 | 0: 1, 1: 11, 2: 15, 3: 18, 4: 15, 5: 5 |

## Modules by Slot

| Slot | Modules | Kinds |
|---|---|---|
| [defense](modules.md#defense) | 47 | defense |
| [utility](modules.md#utility) | 154 | mining, utility |
| [weapon](modules.md#weapon) | 69 | weapon |

## Skills

[skills.md](skills.md): 30 skills, what a level of each gives.

## Full Tables

Tab-separated, one row per thing, a header row under three comment lines: for a search by text and for scripts.

| Table | Rows | Columns |
|---|---|---|
| `tables/facilities.tsv` | 2953 | id, name, category, level, upgrades_from, recipe, build_cost, build_time, labor_cost, materials, power_draw, life_support_draw, gives, needs_service, empire, notes |
| `tables/items.tsv` | 879 | id, name, category, rarity, size, base_value, made_by, used_in_recipes, used_in_builds, extracted_by |
| `tables/modules.tsv` | 270 | id, name, type, slot, cpu, power, size, base_value, damage, reach, cooldown, effect, special |
| `tables/recipes.tsv` | 892 | id, name, category, makes, from, time, by_hand, facilities, notes |
| `tables/ships.tsv` | 385 | id, name, empire, class, category, tier, piloting_required, shipyard_tier, hull, shield, armor, speed, fuel, cargo, cpu, power, weapon_slots, defense_slots, utility_slots, crew, build_time, build_materials, default_modules, notes |
