# Crimson -- Hulls

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.719.3; never edited by hand.
Up: [master-index.md](../master-index.md). Hulls: 68. The Piloting a tier needs, from the hulls of the catalog: tier 2: Piloting 10; tier 3: Piloting 20; tier 4: Piloting 30; tier 5: Piloting 50.
What a hull is built from: `python3 -I -B game/fleet/craftbook.py build <hull id>`, or `tables/ships.tsv`.

## Tier 0

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `shard` | Miner | Industrial | -- | 0 | 110 / 40 / 8 | 1 | 90 | 60 | 2 / 1 / 1 | 12 / 28 | mining_laser_i, pulse_laser_i, pulse_laser_i |

## Tier 1

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `buckler` | Raider | Combat | -- | 0 | 222 / 23 / 14 | 2 | 80 | 20 | 1 / 2 / 0 | 10 / 24 | pulse_laser_i, armor_plate_i, shield_booster_i |
| `cleaver` | Fighter | Combat | -- | 0 | 156 / 14 / 10 | 3 | 80 | 15 | 3 / 1 / 0 | 14 / 40 | autocannon_i, autocannon_i, autocannon_i, armor_plate_i |
| `flail` | Raider | Combat | -- | 0 | 143 / 12 / 8 | 4 | 100 | 80 | 2 / 1 / 1 | 12 / 28 | autocannon_i, autocannon_i, armor_plate_i |
| `levy` | Fighter | Combat | -- | 0 | 103 / 7 / 6 | 3 | 80 | 15 | 2 / 1 / 0 | 8 / 24 | autocannon_i, autocannon_i, armor_plate_i |
| `pike` | Fighter | Combat | -- | 0 | 133 / 12 / 8 | 5 | 90 | 15 | 2 / 1 / 0 | 12 / 30 | autocannon_i, autocannon_i, armor_plate_i |
| `shiv` | Assault | Combat | -- | 0 | 60 / 10 / 18 | 6 | 40 | 30 | 0 / 1 / 1 | 6 / 14 | armor_plate_i |
| `mandate` | Patrol | Combat Support | -- | 0 | 171 / 19 / 9 | 3 | 100 | 20 | 2 / 1 / 2 | 16 / 36 | autocannon_i, autocannon_i, armor_plate_i |
| `dirk` | Smuggler | Covert | -- | 0 | 100 / 35 / 7 | 5 | 120 | 110 | 1 / 1 / 2 | 12 / 26 | autocannon_i, cloaking_device_i |
| `crimson_stiletto` | Scout | Exploration | -- | 0 | 80 / 30 / 8 | 6 | 130 | 20 | 1 / 1 / 2 | 14 / 28 | autocannon_i |
| `crowbar` | Salvager | Industrial | -- | 0 | 160 / 25 / 14 | 2 | 70 | 80 | 2 / 1 / 1 | 12 / 26 | basic_tow_rig, autocannon_i, autocannon_i, armor_plate_i |
| `frostbite` | Ice Harvester | Industrial | -- | 0 | 90 / 25 / 8 | 3 | 70 | 45 | 1 / 1 / 2 | 12 / 28 | ice_harvester_i, autocannon_i, armor_plate_i |
| `maul` | Miner | Industrial | -- | 0 | 170 / 35 / 10 | 2 | 80 | 70 | 2 / 1 / 2 | 14 / 28 | mining_laser_i, autocannon_i, autocannon_i, armor_plate_i |
| `reaver` | Gas Harvester | Industrial | -- | 0 | 150 / 30 / 10 | 2 | 80 | 110 | 1 / 1 / 2 | 10 / 22 | gas_harvester_i, autocannon_i, armor_plate_i |

## Tier 2

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `pennon` | Shuttle | Civilian | 10 | 1 | 210 / 90 / 16 | 4 | 340 | 40 | 1 / 2 / 1 | 22 / 50 | -- |
| `broadaxe` | Heavy Fighter | Combat | 10 | 1 | 282 / 28 / 18 | 3 | 315 | 35 | 4 / 1 / 2 | 22 / 50 | autocannon_ii, autocannon_ii, autocannon_ii, flak_cannon_ii, armor_plate_ii |
| `gauntlet` | Fighter | Combat | 10 | 1 | 285 / 35 / 20 | 3 | 315 | 30 | 3 / 2 / 1 | 22 / 50 | autocannon_ii, autocannon_ii, flak_cannon_ii, armor_plate_ii, shield_booster_ii |
| `halberd` | Assault | Combat | 10 | 1 | 339 / 31 / 22 | 3 | 110 | 50 | 4 / 2 / 1 | 27 / 45 | autocannon_ii, autocannon_ii, autocannon_ii, flak_cannon_ii, armor_plate_ii, kinetic_hull_hardener, assault_barracks |
| `ordinance` | Heavy Fighter | Combat | 10 | 1 | 197 / 18 / 10 | 3 | 270 | 30 | 3 / 1 / 0 | 14 / 42 | autocannon_ii, autocannon_ii, autocannon_ii, armor_plate_ii |
| `stockade` | Monitor | Combat | 10 | 1 | 950 / 100 / 60 | 1 | 450 | 60 | 0 / 8 / 2 | 20 / 60 | armor_plate_ii, armor_plate_ii, armor_plate_ii, armor_plate_ii, kinetic_hull_hardener, explosive_hull_hardener, thermal_hull_hardener, damage_control_system, power_reactor_upgrade, cpu_co_processor |
| `trebuchet` | Monitor | Combat | 10 | 1 | 850 / 90 / 50 | 1 | 450 | 80 | 2 / 6 / 2 | 20 / 75 | autocannon_ii, autocannon_ii, armor_plate_ii, armor_plate_ii, armor_plate_ii, armor_plate_ii, kinetic_hull_hardener, explosive_hull_hardener |
| `cudgel` | Drone Carrier | Combat Support | 10 | 1 | 256 / 24 / 14 | 2 | 120 | 70 | 2 / 2 / 3 | 35 / 48 | autocannon_ii, autocannon_ii, armor_plate_ii, kinetic_hull_hardener, light_drone_bay, light_drone_bay, ship_maintenance_bay |
| `falchion` | Electronic Warfare | Combat Support | 10 | 1 | 232 / 28 / 12 | 3 | 120 | 30 | 1 / 2 / 3 | 28 / 55 | autocannon_ii, armor_plate_ii, kinetic_hull_hardener, stasis_webifier_i, warp_disruptor, target_painter_i |
| `toll` | Customs Patrol | Combat Support | 10 | 1 | 259 / 26 / 15 | 3 | 130 | 35 | 2 / 1 / 2 | 22 / 48 | autocannon_i, autocannon_i, armor_plate_i, warp_scrambler |
| `tourniquet` | Medical Corvette | Combat Support | 10 | 1 | 255 / 60 / 19 | 4 | 170 | 90 | 1 / 2 / 4 | 34 / 68 | autocannon_ii, armor_plate_ii, kinetic_hull_hardener, shipboard_sickbay, afterburner_ii |
| `morningstar` | Tanker | Commercial | 10 | 1 | 250 / 55 / 16 | 2 | 1500 | 80 | 1 / 2 / 2 | 14 / 36 | refueling_pump, armor_plate_ii |
| `ransack` | Freighter | Commercial | 10 | 1 | 240 / 55 / 16 | 2 | 300 | 300 | 2 / 2 / 1 | 16 / 35 | autocannon_ii, autocannon_ii, armor_plate_ii |
| `war_wagon` | Bulk Hauler | Commercial | 10 | 1 | 300 / 50 / 8 | 1 | 240 | 1200 | 0 / 2 / 8 | 22 / 50 | cargo_expander_ii, cargo_expander_ii, cargo_expander_ii, cargo_expander_ii, cargo_expander_ii, cargo_expander_ii, cargo_expander_ii, cargo_expander_ii, armor_plate_ii, armor_plate_ii |
| `billhook` | Gas Harvester | Industrial | 10 | 1 | 220 / 50 / 14 | 2 | 300 | 200 | 0 / 1 / 3 | 16 / 36 | gas_harvester_ii, gas_harvester_ii, cargo_expander_ii |
| `permafrost` | Ice Harvester | Industrial | 10 | 1 | 230 / 55 / 16 | 3 | 315 | 160 | 1 / 1 / 2 | 16 / 38 | ice_harvester_ii, afterburner_ii |
| `siege_drill` | Miner | Industrial | 10 | 1 | 250 / 60 / 18 | 2 | 270 | 200 | 2 / 1 / 2 | 16 / 40 | mining_laser_ii, railgun_i, railgun_i |
| `warhammer` | Salvager | Industrial | 10 | 1 | 200 / 60 / 14 | 2 | 240 | 250 | 1 / 1 / 3 | 18 / 38 | advanced_tow_rig, cargo_expander_ii, cargo_expander_ii |

## Tier 3

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `muster` | Liner | Civilian | 20 | 2 | 520 / 180 / 30 | 2 | 420 | 150 | 1 / 3 / 2 | 26 / 65 | -- |
| `iron_tide` | Carrier | Combat | 20 | 2 | 723 / 77 / 35 | 1 | 420 | 120 | 2 / 3 / 2 | 30 / 80 | autocannon_ii, autocannon_ii, damage_control_system, shield_booster_ii |
| `mace` | Battlecruiser | Combat | 20 | 2 | 650 / 70 / 38 | 2 | 380 | 80 | 4 / 3 / 2 | 42 / 75 | blood_reaver, flak_cannon_ii, autocannon_ii, autocannon_ii, armor_plate_ii, damage_control_system, kinetic_hull_hardener, shipboard_sickbay, crew_armory |
| `partisan` | Interceptor | Combat | 20 | 2 | 120 / 200 / 12 | 6 | 300 | 20 | 3 / 1 / 2 | 35 / 80 | plasma_cannon_ii, plasma_cannon_ii, plasma_cannon_ii, shield_booster_ii, afterburner_ii, tracking_computer_i |
| `warmaul` | Cruiser | Combat | 20 | 2 | 680 / 70 / 35 | 2 | 380 | 70 | 5 / 2 / 3 | 35 / 85 | blood_reaver, flak_cannon_ii, autocannon_ii, autocannon_ii, autocannon_ii, armor_plate_ii, damage_control_system |
| `bastille` | Interdictor | Combat Support | 20 | 2 | 623 / 77 / 30 | 2 | 360 | 60 | 3 / 3 / 4 | 35 / 80 | autocannon_ii, autocannon_ii, armor_plate_ii, damage_control_system, ship_scanner_ii |
| `vanguard` | Command | Combat Support | 20 | 2 | 682 / 88 / 32 | 2 | 380 | 70 | 3 / 3 / 4 | 40 / 90 | autocannon_ii, autocannon_ii, armor_plate_ii, damage_control_system, ship_scanner_ii |
| `warhead` | Hazmat Freighter | Commercial | 20 | 2 | 520 / 180 / 35 | 2 | 340 | 460 | 2 / 2 / 3 | 38 / 55 | lead_lined_cargo_i, armor_plate_ii |
| `polearm` | Explorer | Exploration | 20 | 2 | 420 / 180 / 25 | 3 | 550 | 245 | 3 / 2 / 4 | 28 / 65 | anomaly_detector, autocannon_ii, autocannon_ii |
| `bonesaw` | Salvager | Industrial | 20 | 2 | 450 / 120 / 35 | 2 | 330 | 565 | 3 / 2 / 3 | 28 / 80 | advanced_tow_rig, autocannon_ii, autocannon_ii, autocannon_ii |
| `gas_raider` | Gas Harvester | Industrial | 20 | 2 | 400 / 120 / 25 | 2 | 330 | 450 | 2 / 1 / 3 | 28 / 60 | gas_harvester_iii, gas_harvester_iii, autocannon_ii, autocannon_ii |
| `siege_breaker` | Miner | Industrial | 20 | 2 | 500 / 140 / 30 | 1 | 180 | 450 | 1 / 2 / 3 | 24 / 60 | mining_laser_iii, mining_laser_iii, autocannon_ii |
| `thermal_lance` | Ice Harvester | Industrial | 20 | 2 | 420 / 120 / 28 | 2 | 360 | 430 | 1 / 1 / 3 | 26 / 60 | ice_harvester_iii, ice_harvester_iii, autocannon_ii |
| `whetstone` | Workshop | Industrial | 20 | 2 | 600 / 110 / 34 | 1 | 260 | 380 | 2 / 2 / 4 | 30 / 80 | -- |
| `anvil` | Repair | Support | 20 | 2 | 460 / 200 / 28 | 2 | 360 | 265 | 1 / 3 / 4 | 30 / 65 | autocannon_ii, armor_plate_ii, damage_control_system |

## Tier 4

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `crimson_devastator` | Battlecruiser | Combat | 30 | 3 | 1725 / 175 / 65 | 2 | 350 | 120 | 7 / 3 / 3 | 90 / 185 | fury_cannon, mass_driver, mass_driver, piercing_railgun_ii, piercing_railgun_ii, railgun_ii, railgun_ii, crimson_berserker_plating, reactive_armor_hardener, darksteel_armor |
| `iron_fleet` | Fleet Carrier | Combat | 30 | 3 | 1925 / 175 / 60 | 1 | 600 | 250 | 3 / 4 / 3 | 50 / 130 | autocannon_ii, autocannon_ii, autocannon_ii, crimson_berserker_plating, damage_control_system, shield_booster_ii, cargo_expander_iii |
| `juggernaut` | Assault | Combat | 30 | 3 | 220 / 250 / 15 | 4 | 400 | 40 | 6 / 1 / 1 | 50 / 150 | railgun_ii, railgun_ii, railgun_ii, railgun_ii, railgun_ii, railgun_ii, crimson_berserker_plating, afterburner_i |
| `executioner` | Drone Carrier | Combat Support | 30 | 3 | 1492 / 158 / 55 | 1 | 300 | 240 | 5 / 3 / 4 | 105 / 160 | fury_cannon, mass_driver, piercing_railgun_ii, heavy_torpedo, heavy_torpedo, crimson_berserker_plating, darksteel_armor, damage_control_system, advanced_drone_bay, combat_drone_bay, shipboard_sickbay, ship_maintenance_bay |
| `overlord` | Command | Combat Support | 30 | 3 | 1658 / 192 / 60 | 1 | 320 | 205 | 4 / 4 / 5 | 65 / 170 | blood_reaver, autocannon_ii, autocannon_ii, autocannon_ii, crimson_berserker_plating, damage_control_system, ship_scanner_iii |
| `portcullis` | Interdictor | Combat Support | 30 | 3 | 1425 / 175 / 50 | 1 | 280 | 120 | 3 / 4 / 4 | 55 / 150 | autocannon_ii, autocannon_ii, autocannon_ii, crimson_berserker_plating, damage_control_system, shield_booster_ii, ship_scanner_ii |
| `usurper` | Boarding Cruiser | Combat Support | -- | 3 | 620 / 300 / 30 | 3 | 600 | 170 | 3 / 4 / 5 | 80 / 150 | ion_blaster_ii, pulse_laser_iii, shield_booster_iii, regenerative_armor_ii, damage_control_system, stasis_webifier_ii, ship_scanner_ii, shipboard_sickbay |
| `the_vault` | Freighter | Commercial | -- | 3 | 1800 / 200 / 150 | 1 | 600 | 500 | 0 / 5 / 0 | 40 / 100 | regenerative_armor_ii, armor_plate_ii, hull_reinforcement_ii, reactive_armor_hardener, damage_control_system |
| `warbarge` | Tanker | Commercial | 30 | 3 | 1100 / 250 / 50 | 1 | 10000 | 270 | 2 / 4 / 4 | 35 / 120 | refueling_pump, expanded_fuel_tank, autocannon_ii, autocannon_ii, armor_plate_iii, reactive_armor_hardener |
| `cryoclast` | Refinery | Industrial | 30 | 3 | 1050 / 300 / 48 | 1 | 280 | 660 | 2 / 2 / 4 | 38 / 100 | ice_harvester_iv |
| `guillotine` | Salvager | Industrial | 30 | 3 | 950 / 300 / 45 | 1 | 400 | 600 | 4 / 2 / 4 | 35 / 130 | advanced_tow_rig, autocannon_ii, autocannon_ii, autocannon_ii, autocannon_ii, cargo_expander_iii, cargo_expander_iii |
| `marauder` | Refinery | Industrial | 30 | 3 | 1000 / 300 / 45 | 1 | 280 | 660 | 2 / 2 / 4 | 38 / 100 | gas_harvester_iv |
| `munitions_foundry` | Construction | Industrial | 30 | 3 | 1100 / 350 / 50 | 1 | 280 | 660 | 2 / 2 / 4 | 45 / 120 | -- |
| `ravager` | Miner | Industrial | 30 | 3 | 1200 / 300 / 55 | 1 | 300 | 1440 | 2 / 2 / 5 | 50 / 110 | mining_laser_iv, mining_laser_iv, mining_laser_iv, railgun_i, railgun_i |
| `arsenal` | Logistics | Support | 30 | 3 | 1100 / 400 / 45 | 1 | 350 | 840 | 2 / 3 / 4 | 35 / 90 | autocannon_ii, autocannon_ii, crimson_berserker_plating, damage_control_system, cargo_expander_iii |
| `cauterizer` | Medical | Support | 30 | 3 | 900 / 450 / 40 | 2 | 280 | 240 | 2 / 3 / 5 | 60 / 125 | autocannon_ii, autocannon_ii, armor_plate_ii, damage_control_system, kinetic_hull_hardener, fleet_hospital, shipboard_sickbay |

## Tier 5

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `annihilator` | Dreadnought | Combat | 50 | 4 | 4280 / 420 / 150 | 1 | 600 | 480 | 9 / 4 / 4 | 145 / 300 | fury_cannon, fury_cannon, siege_railgun, siege_railgun, mass_driver, mass_driver, heavy_mass_driver, heavy_torpedo, heavy_torpedo, crimson_berserker_plating, darksteel_armor, reactive_armor_hardener, nanite_hull_coating |
| `armageddon` | Dreadnought | Combat | 50 | 4 | 3482 / 368 / 130 | 1 | 500 | 480 | 9 / 3 / 3 | 150 / 350 | fury_cannon, fury_cannon, siege_railgun, siege_railgun, mass_driver, mass_driver, heavy_mass_driver, void_torpedo_launcher, void_torpedo_launcher, crimson_berserker_plating, darksteel_armor, reactive_armor_hardener |
| `reckoning` | Dreadnought | Combat | 50 | 4 | 4150 / 350 / 140 | 1 | 500 | 540 | 8 / 4 / 3 | 140 / 260 | fury_cannon, fury_cannon, siege_railgun, mass_driver, mass_driver, heavy_mass_driver, heavy_torpedo, heavy_torpedo, crimson_berserker_plating, darksteel_armor, reactive_armor_hardener, damage_control_system |
| `subjugator` | Drone Carrier | Combat Support | 50 | 4 | 3715 / 385 / 120 | 1 | 550 | 660 | 5 / 5 / 6 | 90 / 280 | fury_cannon, siege_railgun, mass_driver, heavy_torpedo, heavy_torpedo, crimson_berserker_plating, darksteel_armor, reactive_armor_hardener, damage_control_system, nanite_hull_coating |
| `siege_foundry` | Mobile Base | Industrial | -- | 4 | 2500 / 600 / 120 |  |  |  | None / None / None | None / None | -- |
