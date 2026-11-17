# Outerrim -- Hulls

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.723.0; never edited by hand.
Up: [master-index.md](../master-index.md). Hulls: 68. The Piloting a tier needs, from the hulls of the catalog: tier 2: Piloting 10; tier 3: Piloting 20; tier 4: Piloting 30; tier 5: Piloting 50.
What a hull is built from: `python3 -I -B game/fleet/craftbook.py build <hull id>`, or `tables/ships.tsv`.

## Tier 0

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `cobble` | Miner | Industrial | -- | 0 | 80 / 35 / 3 | 2 | 120 | 75 | 1 / 1 / 2 | 12 / 24 | mining_laser_i, pulse_laser_i |

## Tier 1

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `loose_change` | Shuttle | Civilian | -- | 0 | 60 / 20 / 1 | 5 | 150 | 35 | 0 / 0 / 2 | 8 / 18 | -- |
| `five_finger_discount` | Raider | Combat | -- | 0 | 75 / 40 / 3 | 5 | 120 | 80 | 2 / 1 / 1 | 14 / 32 | autocannon_i, autocannon_i, armor_plate_i |
| `get_off_my_lawn` | Fighter | Combat | -- | 0 | 55 / 30 / 1 | 6 | 80 | 10 | 2 / 0 / 1 | 10 / 28 | autocannon_i, autocannon_i |
| `no_refunds` | Fighter | Combat | -- | 0 | 80 / 30 / 3 | 5 | 110 | 20 | 2 / 1 / 1 | 12 / 32 | autocannon_i, autocannon_i, armor_plate_i |
| `last_warning` | Patrol | Combat Support | -- | 0 | 90 / 40 / 4 | 5 | 130 | 20 | 2 / 1 / 2 | 14 / 32 | autocannon_i, autocannon_i, armor_plate_i |
| `congregation` | Bulk Hauler | Commercial | -- | 0 | 100 / 0 / 0 | 1 | 110 | 1900 | 0 / 0 / 0 | 8 / 16 | -- |
| `prayer` | Freighter | Commercial | -- | 0 | 40 / 0 / 0 | 3 | 100 | 540 | 0 / 0 / 0 | 4 / 10 | -- |
| `technically_legal` | Courier | Commercial | -- | 0 | 60 / 25 / 1 | 5 | 200 | 50 | 0 / 0 / 2 | 10 / 22 | afterburner_i |
| `worship` | Freighter | Commercial | -- | 0 | 60 / 0 / 0 | 2 | 120 | 1100 | 0 / 0 / 0 | 6 / 14 | -- |
| `warranty_void` | Explorer | Exploration | -- | 0 | 60 / 30 / 2 | 5 | 220 | 40 | 1 / 0 / 2 | 12 / 26 | afterburner_i |
| `claim_jumper` | Miner | Industrial | -- | 0 | 60 / 20 / 1 | 5 | 250 | 55 | 0 / 0 / 2 | 10 / 20 | mining_laser_i, afterburner_i |
| `finders_keepers` | Salvager | Industrial | -- | 0 | 55 / 15 / 1 | 5 | 130 | 70 | 1 / 0 / 1 | 8 / 20 | basic_tow_rig, autocannon_i |
| `frostbitten` | Ice Harvester | Industrial | -- | 0 | 45 / 0 / 0 | 3 | 80 | 70 | 0 / 0 / 1 | 6 / 14 | ice_harvester_i |
| `huffnpuff` | Gas Harvester | Industrial | -- | 0 | 55 / 25 / 1 | 4 | 120 | 45 | 0 / 0 / 2 | 9 / 18 | gas_harvester_i |

## Tier 2

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `bad_idea` | Monitor | Combat | 10 | 1 | 780 / 70 / 35 | 2 | 680 | 110 | 3 / 4 / 2 | 22 / 75 | autocannon_ii, autocannon_ii, autocannon_ii, outer_rim_scrap_armor, outer_rim_scrap_armor, armor_plate_ii, damage_control_system |
| `junkyard_dog` | Heavy Fighter | Combat | 10 | 1 | 170 / 60 / 10 | 5 | 420 | 40 | 3 / 1 / 2 | 18 / 48 | autocannon_ii, autocannon_ii, autocannon_ii, armor_plate_ii, afterburner_ii |
| `bad_influence` | Electronic Warfare | Combat Support | 10 | 1 | 140 / 80 / 5 | 4 | 180 | 30 | 1 / 2 / 4 | 32 / 55 | scrapgun, outer_rim_scrap_armor, shield_booster_ii, stasis_webifier_i, warp_scrambler, sensor_dampener, ecm_jammer |
| `swarm_boss` | Drone Carrier | Combat Support | 10 | 1 | 180 / 70 / 8 | 3 | 160 | 85 | 1 / 1 / 4 | 30 / 50 | scrapgun, outer_rim_scrap_armor, light_drone_bay, light_drone_bay, ship_maintenance_bay, afterburner_ii |
| `baling_wire` | Freighter | Commercial | 10 | 1 | 160 / 50 / 7 | 3 | 420 | 275 | 1 / 1 / 2 | 14 / 35 | afterburner_ii, cargo_expander_ii |
| `junk_convoy` | Bulk Hauler | Commercial | 10 | 1 | 320 / 60 / 6 | 2 | 720 | 850 | 1 / 1 / 6 | 22 / 50 | autocannon_i, armor_plate_ii, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, cargo_expander_ii |
| `long_haul` | Tanker | Commercial | 10 | 1 | 170 / 50 / 8 | 3 | 1500 | 80 | 0 / 1 / 2 | 14 / 36 | refueling_pump |
| `dust_devil` | Blockade Runner | Covert | 10 | 1 | 130 / 60 / 5 | 6 | 700 | 95 | 1 / 1 / 3 | 18 / 45 | afterburner_ii, shield_booster_ii |
| `terms_and_conditions` | Smuggler | Covert | 10 | 1 | 135 / 70 / 5 | 5 | 650 | 120 | 1 / 1 / 3 | 20 / 44 | autocannon_ii, shield_booster_ii |
| `bedrock` | Miner | Industrial | 10 | 1 | 200 / 35 / 12 | 2 | 270 | 200 | 1 / 1 / 2 | 12 / 30 | mining_laser_ii, armor_plate_ii |
| `brain_freeze` | Ice Harvester | Industrial | 10 | 1 | 150 / 45 / 6 | 2 | 240 | 170 | 1 / 1 / 3 | 14 / 36 | ice_harvester_ii, cargo_expander_ii |
| `chop_shop` | Salvager | Industrial | 10 | 1 | 160 / 55 / 8 | 2 | 240 | 280 | 1 / 1 / 3 | 18 / 38 | advanced_tow_rig, shield_booster_ii |
| `come_along` | Recovery Frigate | Industrial | 10 | 1 | 220 / 55 / 13 | 4 | 240 | 130 | 1 / 2 / 4 | 30 / 62 | scrap_harpoon, outer_rim_scrap_armor, assault_barracks, afterburner_ii |
| `oil_money` | Whaler | Industrial | 10 | 1 | 450 / 80 / 14 | 3 | 480 | 220 | 3 / 1 / 3 | 22 / 52 | scrap_harpoon, scrap_harpoon, outer_rim_scrap_armor, afterburner_ii, cargo_expander_ii |
| `repo_man` | Miner | Industrial | 10 | 1 | 160 / 50 / 7 | 3 | 315 | 170 | 1 / 1 / 3 | 16 / 38 | mining_laser_ii, autocannon_i |
| `spit_and_prayer` | Gas Harvester | Industrial | 10 | 1 | 150 / 55 / 6 | 3 | 360 | 140 | 1 / 1 / 3 | 14 / 36 | gas_harvester_ii, afterburner_ii |
| `yard_sale` | Salvager | Industrial | 10 | 1 | 400 / 80 / 10 | 3 | 450 | 100 | 0 / 1 / 4 | 22 / 50 | advanced_tow_rig, tractor_beam, outer_rim_salvage_array, cargo_expander_ii, shield_booster_i |
| `duct_tape_special` | Medical | Support | 10 | 1 | 160 / 65 / 7 | 4 | 200 | 70 | 0 / 1 / 4 | 18 / 40 | shipboard_sickbay, armor_plate_ii, afterburner_ii |
| `jump_start` | Logistics | Support | 10 | 1 | 160 / 50 / 8 | 3 | 1200 | 60 | 0 / 1 / 2 | 16 / 40 | field_generator |

## Tier 3

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `midlife_crisis` | Liner | Civilian | 20 | 2 | 350 / 180 / 14 | 3 | 400 | 145 | 1 / 2 / 2 | 28 / 75 | -- |
| `odyssey` | Expedition Tourer | Civilian | -- | 2 | 300 / 240 / 16 | 5 | 1000 | 160 | 1 / 3 / 5 | 45 / 80 | pulse_laser_ii, shield_booster_ii, survey_scanner_i, ship_scanner_ii, fuel_optimizer |
| `hells_bells` | Cruiser | Combat | 20 | 2 | 400 / 180 / 20 | 4 | 500 | 80 | 4 / 2 / 3 | 35 / 90 | scrapgun, scrapgun, autocannon_ii, autocannon_ii, outer_rim_scrap_armor, damage_control_system |
| `insurance_fraud` | Assault | Combat | 20 | 2 | 380 / 200 / 18 | 4 | 500 | 105 | 5 / 2 / 2 | 32 / 100 | scrapgun, scrapgun, autocannon_ii, autocannon_ii, autocannon_ii, outer_rim_scrap_armor, damage_control_system |
| `glows_in_the_dark` | Hazmat Freighter | Commercial | 20 | 2 | 350 / 200 / 12 | 3 | 400 | 300 | 1 / 2 / 4 | 38 / 46 | lead_lined_cargo_i, afterburner_i |
| `nomad` | Carrier | Commercial | 20 | 2 | 460 / 190 / 16 | 1 | 550 | 180 | 1 / 2 / 4 | 25 / 65 | autocannon_ii, cargo_expander_ii |
| `probable_cause` | Blockade Runner | Covert | 20 | 2 | 350 / 200 / 15 | 5 | 600 | 170 | 2 / 2 / 3 | 30 / 80 | cargo_expander_iii, shield_booster_ii |
| `peer_review` | Explorer | Exploration | 20 | 2 | 100 / 150 / 6 | 4 | 240 | 25 | 0 / 1 / 4 | 35 / 80 | anomaly_detector, survey_scanner_ii, fuel_optimizer, expanded_fuel_tank, shield_booster_ii |
| `gas_trawler` | Gas Harvester | Industrial | 20 | 2 | 340 / 130 / 12 | 2 | 380 | 450 | 1 / 1 / 4 | 24 / 55 | gas_harvester_iii, gas_harvester_iii, autocannon_ii |
| `hold_my_beer` | Salvager | Industrial | 20 | 2 | 420 / 170 / 22 | 3 | 400 | 480 | 2 / 2 / 4 | 28 / 75 | advanced_tow_rig, autocannon_ii, autocannon_ii, cargo_expander_ii |
| `ice_trawler` | Ice Harvester | Industrial | 20 | 2 | 350 / 130 / 14 | 2 | 330 | 620 | 1 / 1 / 4 | 24 / 55 | ice_harvester_iii, cargo_expander_iii, cargo_expander_ii |
| `money_pit` | Refinery | Industrial | 20 | 2 | 450 / 160 / 22 | 2 | 300 | 300 | 1 / 2 / 4 | 30 / 95 | -- |
| `rock_eater` | Miner | Industrial | 20 | 2 | 380 / 140 / 14 | 2 | 400 | 500 | 1 / 1 / 4 | 26 / 60 | mining_laser_iii, mining_laser_iii, autocannon_ii |
| `some_assembly_required` | Workshop | Industrial | 20 | 2 | 280 / 130 / 10 | 4 | 420 | 330 | 1 / 1 / 4 | 30 / 85 | -- |
| `last_chance` | Rescue Cruiser | Support | 20 | 2 | 540 / 145 / 27 | 2 | 900 | 230 | 1 / 3 / 5 | 58 / 120 | autocannon_ii, armor_plate_ii, field_hospital, ship_maintenance_bay, refueling_pump, afterburner_ii |

## Tier 4

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `free_radical` | Battlecruiser | Combat | 30 | 3 | 1000 / 400 / 40 | 3 | 450 | 120 | 5 / 3 / 4 | 50 / 180 | mass_driver, piercing_railgun_ii, railgun_ii, railgun_ii, railgun_i, reactive_armor_hardener, outer_rim_scrap_armor, expanded_fuel_tank |
| `excessive_force` | Drone Carrier | Combat Support | 30 | 3 | 900 / 400 / 35 | 2 | 500 | 455 | 2 / 3 / 6 | 60 / 160 | scrapgun, scrapgun, outer_rim_scrap_armor, reactive_armor_hardener, damage_control_system, advanced_drone_bay, combat_drone_bay, ship_maintenance_bay, afterburner_ii |
| `plausible_deniability` | Command | Combat Support | 30 | 3 | 1100 / 500 / 40 | 2 | 550 | 205 | 3 / 3 / 6 | 72 / 200 | scrapgun, scrapgun, ship_scanner_iii, afterburner_i, expanded_fuel_tank, shield_booster_ii |
| `frankenhauler` | Bulk Hauler | Commercial | 30 | 3 | 600 / 250 / 22 | 2 | 500 | 2640 | 2 / 2 / 4 | 30 / 80 | autocannon_i, autocannon_i, afterburner_i, expanded_fuel_tank, cargo_expander_iii |
| `last_drop` | Tanker | Commercial | 30 | 3 | 550 / 180 / 12 | 2 | 11500 | 320 | 1 / 2 / 6 | 35 / 110 | refueling_pump, expanded_fuel_tank, expanded_fuel_tank, cargo_expander_iii, scrapgun |
| `need_to_know` | Intelligence | Covert | 30 | 3 | 750 / 450 / 28 | 3 | 600 | 145 | 2 / 3 / 5 | 65 / 170 | ship_scanner_iii, cloaking_device_ii, scrapgun, expanded_fuel_tank, shield_booster_ii |
| `going_dark` | Pathfinder | Exploration | 30 | 3 | 750 / 350 / 28 | 3 | 800 | 250 | 2 / 2 / 6 | 70 / 150 | pathfinder_drive, survey_scanner_ii, ice_harvester_iv, onboard_h2o2_refinery, expanded_fuel_tank, shield_booster_i, scrapgun, scrapgun |
| `manifest_destiny` | Explorer | Exploration | 30 | 3 | 800 / 350 / 30 | 3 | 900 | 335 | 3 / 2 / 5 | 45 / 120 | anomaly_detector, scrapgun, scrapgun, expanded_fuel_tank, cargo_expander_iii |
| `cold_comfort` | Refinery | Industrial | 30 | 3 | 700 / 250 / 28 | 2 | 320 | 780 | 1 / 2 / 5 | 32 / 90 | ice_harvester_iv |
| `lungful` | Refinery | Industrial | 30 | 3 | 700 / 250 / 28 | 2 | 320 | 840 | 1 / 2 / 5 | 32 / 90 | gas_harvester_iv |
| `no_fixed_address` | Outpost Tender | Industrial | -- | 3 | 900 / 300 / 45 | 2 | 900 | 600 | 1 / 4 / 5 | 50 / 110 | pulse_laser_iii, shield_booster_iii, armor_plate_ii, damage_control_system, ship_scanner_ii, cargo_expander_iii |
| `pithead` | Miner | Industrial | 30 | 3 | 900 / 350 / 35 | 2 | 550 | 1800 | 1 / 2 / 6 | 38 / 100 | mining_laser_iv, mining_laser_iv, mining_laser_iv, autocannon_ii |
| `rapid_smelter` | Refinery | Industrial | 30 | 3 | 800 / 300 / 30 | 2 | 320 | 720 | 1 / 2 / 5 | 35 / 95 | -- |
| `good_enough` | Logistics | Support | 30 | 3 | 850 / 350 / 35 | 2 | 650 | 840 | 2 / 2 / 5 | 40 / 110 | scrapgun, cargo_expander_iii, cargo_expander_iii, expanded_fuel_tank, shield_booster_i |

## Tier 5

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `finish_line` | Dreadnought | Civilian | 50 | 4 | 2000 / 1000 / 60 | 3 | 1200 | 240 | 5 / 3 / 5 | 80 / 380 | jury_rigged_cannon, jury_rigged_cannon, mass_driver, scrapgun, scrapgun, outer_rim_scrap_armor, reactive_armor_hardener, nanite_hull_coating |
| `first_step_dreadnought` | Dreadnought | Combat | 50 | 4 | 2500 / 1200 / 90 | 2 | 1000 | 660 | 7 / 4 / 6 | 130 / 350 | siege_railgun, siege_railgun, mass_driver, mass_driver, heavy_mass_driver, void_torpedo_launcher, void_torpedo_launcher, outer_rim_scrap_armor, darksteel_armor, reactive_armor_hardener, nanite_hull_coating |
| `controlled_chaos` | Drone Carrier | Combat Support | 50 | 4 | 2800 / 1100 / 80 | 2 | 900 | 780 | 5 / 4 / 8 | 95 / 320 | jury_rigged_cannon, jury_rigged_cannon, scrapgun, scrapgun, autocannon_ii, outer_rim_scrap_armor, darksteel_armor, reactive_armor_hardener, nanite_hull_coating |
| `all_mine` | Miner | Industrial | 50 | 4 | 2000 / 700 / 80 | 1 | 600 | 2640 | 2 / 3 / 8 | 60 / 230 | mining_laser_v, mining_laser_v, mining_laser_v, hyper_mining_laser_iii, hyper_mining_laser_iii, autocannon_ii, autocannon_ii |
| `here_to_stay` | Mobile Base | Support | -- | 4 | 3200 / 1400 / 100 |  |  |  | None / None / None | None / None | -- |
