# Bases and Facilities

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.734.3; never edited by hand.
Up: [master-index.md](master-index.md). What a facility's materials take down to the ore: `python3 -I -B game/fleet/craftbook.py build <facility id>`.

## Founding a Base

The part a founding needs, the recipe that makes it and the facility that runs the recipe.

| For | Part | The part is made from | In the facility | Level | Facility cost (cr) | Facility materials |
|---|---|---|---|---|---|---|
| An outpost | `outpost_kit` | steel_plate x 400; circuit_board x 150; reinforced_frame x 40; structural_frame x 60; control_node x 10 | `outpost_frame_assembler` | 2 | 600,000 | steel_plate x 800; circuit_board x 300; reinforced_frame x 120; control_node x 40 |
| A station | `station_core` | station_reactor_core x 4; station_reactor x 2; reinforced_frame x 220; structural_frame x 320; quantum_control_core x 60; docking_ring x 90; hull_plating x 520; reinforced_bulkhead x 340 | `station_core_foundry` | 4 | 38,000,000 | steel_plate x 12500; copper_piping x 7800; reinforced_frame x 4200; quantum_control_core x 1800; control_node x 1500; hull_plating x 8400; reinforced_bulkhead x 5600; docking_ring x 2900 |

## Defense

| Facility | Level | Gives | Needs first | Cost (cr) | Labor | Materials | Notes |
|---|---|---|---|---|---|---|---|
| `automated_repair_dock` | 1 | -- | -- | 1,100,000 | 70 | steel_plate x 1600; circuit_board x 200; armor_plate x 120 | player_station_buildable, station_or_faction_only |
| `fire_control_center` | 1 | -- | -- | 1,200,000 | 70 | steel_plate x 900; targeting_computer x 60; circuit_board x 300; superconductor x 80 | player_station_buildable, station_or_faction_only |
| `point_defense_battery` | 1 | -- | -- | 180,000 | 20 | steel_plate x 400; circuit_board x 60; targeting_computer x 4 | player_station_buildable, station_or_faction_only |
| `reinforced_plating` | 1 | -- | -- | 700,000 | 50 | steel_plate x 2000; armor_plate x 240 | player_station_buildable, station_or_faction_only |
| `shield_projector` | 1 | -- | -- | 900,000 | 60 | steel_plate x 1200; superconductor x 200; power_cell x 300 | player_station_buildable, station_or_faction_only |
| `bulwark_plating` | 2 | -- | -- | 2,800,000 | 140 | steel_plate x 4000; capital_armor_plate x 60; armor_plate x 600 | player_station_buildable, station_or_faction_only |
| `damage_control_center` | 2 | -- | -- | 2,400,000 | 130 | steel_plate x 2000; armor_plate x 400; circuit_board x 250; superconductor x 120 | player_station_buildable, station_or_faction_only |
| `integrated_fire_director` | 2 | -- | -- | 3,000,000 | 150 | steel_plate x 2200; targeting_computer x 200; circuit_board x 800; superconductor x 300; dark_matter_cell x 20 | player_station_buildable, station_or_faction_only |
| `scrap_flak_battery` | 2 | -- | -- | 200,000 | 20 | steel_plate x 600; circuit_board x 40 | pirate_base_only |
| `shield_bastion` | 2 | -- | -- | 3,200,000 | 160 | steel_plate x 3000; superconductor x 700; power_cell x 900; dark_matter_cell x 40 | player_station_buildable, station_or_faction_only |
| `station_defense_turret` | 2 | -- | -- | 420,000 | 40 | steel_plate x 900; circuit_board x 140; targeting_computer x 10; superconductor x 40 | player_station_buildable, station_or_faction_only |
| `harpoon_emplacement` | 3 | -- | -- | 320,000 | 30 | steel_plate x 900; tungsten_rod x 200; circuit_board x 60 | pirate_base_only |
| `heavy_defense_battery` | 3 | -- | -- | 1,400,000 | 90 | steel_plate x 2600; armor_plate x 200; targeting_computer x 30; superconductor x 160 | player_station_buildable, station_or_faction_only |
| `siege_lance` | 3 | -- | -- | 2,600,000 | 140 | steel_plate x 3200; superconductor x 400; targeting_computer x 40; dark_matter_cell x 30 | player_station_buildable, station_or_faction_only |

## Faction

| Facility | Level | Gives | Needs first | Cost (cr) | Labor | Materials | Notes |
|---|---|---|---|---|---|---|---|
| `faction_desk` | 1 | faction_admin | faction_storage | 100,000 |  | steel_plate x 100; circuit_board x 25 | -- |
| `faction_office` | 2 | faction_admin | faction_storage | 500,000 |  | steel_plate x 300; circuit_board x 150 | -- |
| `faction_quarters` | 1 | faction_commons | faction_storage | 100,000 |  | steel_plate x 100; flex_polymer x 50 | -- |
| `faction_lounge` | 2 | faction_commons | faction_storage | 400,000 |  | steel_plate x 300; flex_polymer x 200; reinforced_glass x 100 | -- |
| `faction_clubhouse` | 3 | faction_commons | faction_storage | 2,500,000 |  | steel_plate x 1000; flex_polymer x 500; reinforced_glass x 300; circuit_board x 200 | -- |
| `company_store` | 1 | faction_company_store | faction_market | 400,000 |  | steel_plate x 200; circuit_board x 150 | -- |
| `company_outlet` | 2 | faction_company_store | faction_market | 1,200,000 |  | steel_plate x 500; circuit_board x 400 | -- |
| `company_exchange` | 3 | faction_company_store | faction_market | 5,000,000 |  | steel_plate x 2000; circuit_board x 1000; titanium_alloy x 500 | -- |
| `espionage_hq` | 1 | faction_espionage | faction_storage | 250,000 |  | circuit_board x 250; optical_fiber_bundle x 150; superconductor x 50 | -- |
| `faction_fuel_bunker` | 1 | faction_fuel | faction_storage | 800,000 |  | steel_plate x 400; circuit_board x 100 | -- |
| `faction_large_fuel_bunker` | 2 | faction_fuel | faction_storage | 3,000,000 |  | steel_plate x 1200; circuit_board x 300; armor_plate x 100 | -- |
| `faction_capital_fuel_bunker` | 3 | faction_fuel | faction_storage | 10,000,000 |  | steel_plate x 3000; circuit_board x 800; armor_plate x 300; capital_armor_plate x 100 | -- |
| `intel_terminal` | 1 | faction_intel | faction_storage | 150,000 |  | circuit_board x 200; optical_fiber_bundle x 100 | -- |
| `intel_center` | 2 | faction_intel | faction_storage | 750,000 |  | circuit_board x 500; optical_fiber_bundle x 300; superconductor x 100 | -- |
| `market_runner` | 1 | faction_market | faction_storage | 150,000 |  | steel_plate x 100; circuit_board x 75 | -- |
| `trading_booth` | 2 | faction_market | faction_storage | 600,000 |  | steel_plate x 300; circuit_board x 250 | -- |
| `faction_trading_post` | 3 | faction_market | faction_storage | 3,000,000 |  | steel_plate x 1500; circuit_board x 750; titanium_alloy x 400 | -- |
| `letter_of_marque_office` | 1 | faction_marque | faction_storage | 600,000 |  | steel_plate x 300; circuit_board x 150; trade_cipher x 10 | pirate_base_only |
| `faction_aid_station` | 1 | faction_medical | faction_storage | 550,000 |  | steel_plate x 250; circuit_board x 150; medical_supplies x 50 | -- |
| `fleet_infirmary` | 2 | faction_medical | faction_storage | 2,400,000 |  | steel_plate x 800; circuit_board x 500; reinforced_glass x 180; medical_supplies x 150 | -- |
| `casualty_clearing_center` | 3 | faction_medical | faction_storage | 9,500,000 |  | steel_plate x 2500; circuit_board x 1500; titanium_alloy x 700; reinforced_glass x 500; medical_supplies x 500 | -- |
| `faction_fleet_hospital` | 4 | faction_medical | faction_storage | 35,000,000 |  | steel_plate x 7000; circuit_board x 4000; titanium_alloy x 2200; durasteel_plate x 800; quantum_processor x 80; medical_supplies x 1600 | -- |
| `notice_board` | 1 | faction_missions | faction_storage | 50,000 |  | steel_plate x 50; circuit_board x 20 | -- |
| `faction_mission_board` | 2 | faction_missions | faction_storage | 300,000 |  | steel_plate x 200; circuit_board x 150 | -- |
| `bounty_office` | 3 | faction_missions | faction_storage | 2,000,000 |  | steel_plate x 1000; circuit_board x 500; titanium_alloy x 250 | -- |
| `muster_office` | 1 | faction_personnel_reserve | faction_storage | 400,000 |  | steel_plate x 300; circuit_board x 100; protein_rations x 100 | -- |
| `reserve_barracks` | 2 | faction_personnel_reserve | faction_storage | 1,800,000 |  | steel_plate x 900; circuit_board x 350; flex_polymer x 250; protein_rations x 300 | -- |
| `fleet_mobilization_center` | 3 | faction_personnel_reserve | faction_storage | 7,500,000 |  | steel_plate x 3000; circuit_board x 1200; titanium_alloy x 600; protein_rations x 1000 | -- |
| `strategic_reserve_command` | 4 | faction_personnel_reserve | faction_storage | 28,000,000 |  | steel_plate x 8000; circuit_board x 3000; titanium_alloy x 1800; durasteel_plate x 600; protein_rations x 3000 | -- |
| `prize_recovery_yard` | 1 | faction_prize_recovery | faction_storage | 600,000 |  | steel_plate x 300; circuit_board x 150 | -- |
| `hiring_board` | 1 | faction_recruitment | faction_storage | 75,000 |  | steel_plate x 75; circuit_board x 25 | -- |
| `recruitment_desk` | 2 | faction_recruitment | faction_storage | 300,000 |  | steel_plate x 200; circuit_board x 100 | -- |
| `recruitment_center` | 3 | faction_recruitment | faction_storage | 2,000,000 |  | steel_plate x 1000; circuit_board x 500; flex_polymer x 300 | -- |
| `guild_hall_recruiting` | 4 | faction_recruitment | faction_storage | 8,000,000 |  | steel_plate x 3000; circuit_board x 1500; titanium_alloy x 800 | -- |
| `grand_recruitment_bureau` | 5 | faction_recruitment | faction_storage | 20,000,000 |  | steel_plate x 8000; circuit_board x 5000; titanium_alloy x 2500; durasteel_plate x 1000 | -- |
| `sensor_dome` | 1 | faction_sensor | faction_storage | 600,000 |  | steel_plate x 300; circuit_board x 150; sensor_array x 40 | -- |
| `deep_space_scanner` | 2 | faction_sensor | faction_storage | 3,500,000 |  | steel_plate x 800; circuit_board x 400; titanium_alloy x 200; sensor_package x 60; precision_optic x 30 | -- |
| `long_range_subspace_sensor` | 3 | faction_sensor | faction_storage | 12,000,000 |  | steel_plate x 2500; circuit_board x 1000; titanium_alloy x 600; durasteel_plate x 300; sensor_cluster x 80; communications_array x 40; quantum_processor x 40 | -- |
| `faction_ship_garage` | 1 | faction_ship_garage | faction_storage | 600,000 |  | steel_plate x 300; circuit_board x 150 | -- |
| `faction_ship_hangar` | 2 | faction_ship_garage | faction_storage | 3,000,000 |  | steel_plate x 1200; circuit_board x 500; titanium_alloy x 300 | -- |
| `faction_fleet_yard` | 3 | faction_ship_garage | faction_storage | 12,000,000 |  | steel_plate x 4000; circuit_board x 1500; titanium_alloy x 1000; durasteel_plate x 400 | -- |
| `faction_shipyard_berth` | 1 | faction_shipyard_slot | faction_storage | 1,500,000 |  | steel_plate x 800; circuit_board x 300 | -- |
| `faction_shipyard_bay` | 2 | faction_shipyard_slot | faction_storage | 5,000,000 |  | steel_plate x 2000; circuit_board x 800; titanium_alloy x 300 | -- |
| `faction_shipyard_dock` | 3 | faction_shipyard_slot | faction_storage | 15,000,000 |  | steel_plate x 5000; circuit_board x 2000; titanium_alloy x 1000; durasteel_plate x 300 | -- |
| `faction_shipyard_drydock` | 4 | faction_shipyard_slot | faction_storage | 40,000,000 |  | steel_plate x 10000; circuit_board x 4000; titanium_alloy x 2500; durasteel_plate x 1000; superconductor x 300 | -- |
| `faction_shipyard_complex` | 5 | faction_shipyard_slot | faction_storage | 100,000,000 |  | steel_plate x 20000; circuit_board x 8000; titanium_alloy x 5000; durasteel_plate x 2500; superconductor x 800; capital_armor_plate x 300 | -- |
| `faction_lockbox` | 1 | faction_storage | -- | 200,000 |  | steel_plate x 200; circuit_board x 50 | -- |
| `faction_warehouse` | 2 | faction_storage | -- | 750,000 |  | steel_plate x 500; circuit_board x 200 | -- |
| `faction_depot` | 3 | faction_storage | -- | 4,000,000 |  | steel_plate x 2000; circuit_board x 1000; titanium_alloy x 500 | -- |
| `faction_stronghold` | 4 | faction_storage | -- | 15,000,000 |  | steel_plate x 5000; circuit_board x 2500; titanium_alloy x 1500; durasteel_plate x 500 | -- |
| `storage_extension` | 1 | faction_storage_extension | faction_storage | 500,000 |  | steel_plate x 400; circuit_board x 150 | -- |
| `trade_ledger` | 1 | faction_trade_intel | faction_storage | 200,000 |  | circuit_board x 150; optical_fiber_bundle x 100; trade_cipher x 10 | -- |
| `commerce_terminal` | 2 | faction_trade_intel | faction_storage | 1,500,000 |  | circuit_board x 500; optical_fiber_bundle x 400; superconductor x 200; trade_cipher x 50 | -- |
| `transit_lounge` | 1 | faction_transit | faction_storage | 500,000 |  | steel_plate x 250; circuit_board x 100; flex_polymer x 100 | -- |
| `transit_terminal` | 2 | faction_transit | faction_storage | 2,500,000 |  | steel_plate x 1000; circuit_board x 400; flex_polymer x 300; reinforced_glass x 200 | -- |
| `transit_concourse` | 3 | faction_transit | faction_storage | 9,000,000 |  | steel_plate x 3000; circuit_board x 1200; titanium_alloy x 600; reinforced_glass x 500 | -- |

## Infrastructure

| Facility | Level | Gives | Needs first | Cost (cr) | Labor | Materials | Notes |
|---|---|---|---|---|---|---|---|
| `atmospheric_recycler` | 1 | -- | -- | 600,000 | 40 | steel_plate x 1200; water_recycler x 200 | player_station_buildable |
| `battery_bank` | 1 | -- | -- | 500,000 | 30 | steel_plate x 1000; power_cell x 600 | -- |
| `bunker_fed_reactor` | 1 | -- | -- | 500,000 | 50 | steel_plate x 2000; power_cell x 400 | player_station_buildable |
| `capacitor_bank` | 1 | -- | -- | 500,000 | 30 | steel_plate x 1000; power_cell x 600 | player_station_buildable |
| `damage_control_station` | 1 | -- | -- | 8,000 | 20 | steel_plate x 20; repair_kit x 10 | player_station_buildable |
| `dark_matter_reactor` | 1 | -- | -- | 3,000,000 | 150 | steel_plate x 8000; circuit_board x 1000; dark_matter_cell x 200 | player_station_buildable |
| `dockside_diner` | 1 | -- | -- | 150,000 | 15 | steel_plate x 60; flex_polymer x 20 | player_station_buildable |
| `frontier_cantina` | 1 | -- | -- | 150,000 | 15 | steel_plate x 60; flex_polymer x 30 | player_station_buildable |
| `fuel_bunker` | 1 | -- | -- | 500,000 | 10 | steel_plate x 80000; ceramite_plating x 20000; fuel_tank x 800 | -- |
| `fuel_cell_generator` | 1 | -- | -- | 500,000 | 50 | steel_plate x 2000; power_cell x 400 | player_station_buildable |
| `fuel_tank_expansion` | 1 | -- | -- | 500,000 | 10 | steel_plate x 8000; ceramite_plating x 1500; fuel_tank x 800 | player_station_buildable |
| `fusion_power_core` | 1 | -- | -- | 800,000 | 50 | steel_plate x 2000; power_cell x 400 | -- |
| `life_support_expansion` | 1 | -- | -- | 45,000 | 35 | steel_plate x 35; water_recycler x 6; circuit_board x 2 | -- |
| `life_support_system` | 1 | -- | -- | 600,000 | 40 | steel_plate x 1200; water_recycler x 200 | -- |
| `pirate_bar` | 1 | -- | -- | 120,000 | 20 | steel_plate x 60; salvage_metal x 40 | -- |
| `pirate_life_support_rig` | 1 | -- | -- | 60,000 | 25 | steel_plate x 25; salvage_metal x 20 | -- |
| `power_plant_expansion` | 1 | -- | -- | 60,000 | 45 | steel_plate x 45; power_cell x 12; circuit_board x 3 | -- |
| `rec_lounge` | 1 | -- | -- | 150,000 | 15 | steel_plate x 60; flex_polymer x 30 | player_station_buildable |
| `salvaged_life_support_module` | 1 | -- | -- | 20,000 | 22 | salvage_metal x 30; steel_plate x 12 | -- |
| `scavenged_battery_rig` | 1 | -- | -- | 500,000 | 22 | salvage_metal x 1200; power_cell x 320 | -- |
| `scrap_reactor` | 1 | -- | -- | 80,000 | 30 | steel_plate x 40; salvage_metal x 30 | player_station_buildable |
| `slice_deck` | 1 | -- | -- | 150,000 | 15 | steel_plate x 60; flex_polymer x 20 | player_station_buildable |
| `stellar_collector_grid` | 1 | -- | -- | 900,000 | 80 | steel_plate x 2000; circuit_board x 1200 | player_station_buildable |
| `stolen_generator_module` | 1 | -- | -- | 35,000 | 30 | salvage_metal x 50; steel_plate x 20 | -- |
| `stolen_reactor_core` | 1 | -- | -- | 80,000 | 30 | steel_plate x 40; salvage_metal x 30 | -- |
| `sunrise_griddle` | 1 | -- | -- | 150,000 | 15 | steel_plate x 60; flex_polymer x 20 | player_station_buildable |
| `the_long_watch` | 1 | -- | -- | 150,000 | 20 | steel_plate x 80; flex_polymer x 30 | player_station_buildable |
| `biosphere_commons` | 2 | -- | -- | 0 | 40 | -- | empire=solarian |
| `buffer_array` | 2 | -- | -- | 1,500,000 | 60 | steel_plate x 4200; power_cell x 2500; circuit_board x 350 | player_station_buildable |
| `climate_control_array` | 2 | -- | -- | 1,300,000 | 60 | steel_plate x 1800; water_recycler x 300 | player_station_buildable |
| `environmental_processor` | 2 | -- | -- | 1,800,000 | 60 | steel_plate x 4200; water_recycler x 700 | -- |
| `grazer_grill` | 2 | -- | -- | 350,000 | 40 | steel_plate x 150; flex_polymer x 60; circuit_board x 20 | player_station_buildable |
| `large_fuel_bunker` | 2 | -- | -- | 1,500,000 | 25 | steel_plate x 560000; ceramite_plating x 140000; fuel_tank x 5600; circuit_board x 35000 | -- |
| `legion_mess_hall` | 2 | -- | -- | 0 | 40 | -- | empire=crimson |
| `power_buffer` | 2 | -- | -- | 1,500,000 | 60 | steel_plate x 4200; power_cell x 2500; circuit_board x 350 | -- |
| `reactor_complex` | 2 | -- | -- | 2,400,000 | 80 | steel_plate x 7000; power_cell x 1400 | -- |
| `stellar_bistro` | 2 | -- | -- | 350,000 | 40 | steel_plate x 150; flex_polymer x 60; circuit_board x 20 | player_station_buildable |
| `stillwater_node` | 2 | -- | -- | 0 | 40 | -- | empire=voidborn |
| `the_far_table` | 2 | -- | -- | 350,000 | 40 | steel_plate x 150; flex_polymer x 60; circuit_board x 20 | player_station_buildable |
| `the_tide_line` | 2 | -- | -- | 320,000 | 40 | steel_plate x 120; flex_polymer x 45; circuit_board x 20 | player_station_buildable |
| `zero_g_lounge_bar` | 2 | -- | -- | 350,000 | 40 | steel_plate x 150; flex_polymer x 80; circuit_board x 30 | player_station_buildable |
| `biosphere_ring` | 3 | -- | -- | 3,800,000 | 80 | steel_plate x 2700; water_recycler x 450 | player_station_buildable |
| `capacitor_array` | 3 | -- | -- | 4,500,000 | 100 | steel_plate x 14400; power_cell x 9600; circuit_board x 1800; dark_matter_cell x 240 | -- |
| `capital_fuel_bunker` | 3 | -- | -- | 4,500,000 | 60 | steel_plate x 3000000; ceramite_plating x 960000; fuel_tank x 30000; circuit_board x 240000; titanium_alloy x 120000 | -- |
| `collective_fleet_node` | 3 | -- | -- | 200,000 | 210 | silicate_composite x 60; circuit_board x 35; shield_emitter x 6; focused_crystal x 3 | empire=voidborn |
| `confederacy_fleet_depot` | 3 | -- | -- | 200,000 | 200 | steel_plate x 60; circuit_board x 35; sensor_array x 6; power_cell x 8 | empire=solarian |
| `cryo_capacitor_vault` | 3 | -- | -- | 4,500,000 | 100 | steel_plate x 14400; power_cell x 9600; circuit_board x 1800; dark_matter_cell x 240 | player_station_buildable |
| `federation_fleet_depot` | 3 | -- | -- | 200,000 | 220 | flex_polymer x 50; circuit_board x 35; cargo_container x 6; sensor_array x 5 | empire=nebula |
| `habitat_core` | 3 | -- | -- | 5,400,000 | 80 | steel_plate x 10800; water_recycler x 1800; circuit_board x 600 | -- |
| `orbital_spa_resort_deck` | 3 | -- | -- | 700,000 | 80 | steel_plate x 250; flex_polymer x 150; circuit_board x 60 | player_station_buildable |
| `pact_forward_armory` | 3 | -- | -- | 200,000 | 220 | steel_plate x 80; hull_plating x 20; weapon_housing x 8; armor_plate x 5 | empire=crimson |
| `power_grid` | 3 | -- | -- | 7,000,000 | 120 | steel_plate x 18000; power_cell x 3600; circuit_board x 1200 | -- |
| `rim_ranger_cache` | 3 | -- | -- | 150,000 | 190 | aluminum_sheet x 50; flex_polymer x 30; hull_plating x 8; thruster_nozzle x 5 | empire=outerrim |
| `the_gilded_flute` | 3 | -- | -- | 0 | 80 | -- | empire=nebula |
| `the_golden_table` | 3 | -- | -- | 700,000 | 80 | steel_plate x 250; flex_polymer x 100; circuit_board x 60 | player_station_buildable |
| `biosphere_module` | 4 | -- | -- | 16,000,000 | 100 | steel_plate x 24000; water_recycler x 4000; circuit_board x 2000 | -- |
| `collective_fleet_matrix` | 4 | -- | -- | 350,000 | 390 | silicate_composite x 100; circuit_board x 60; shield_emitter x 12; focused_crystal x 8; processing_core x 3 | empire=voidborn |
| `confederacy_naval_command` | 4 | -- | -- | 350,000 | 370 | steel_plate x 100; circuit_board x 60; sensor_array x 10; power_cell x 15; sensor_package x 3 | empire=solarian |
| `federation_fleet_hub` | 4 | -- | -- | 350,000 | 400 | flex_polymer x 80; circuit_board x 60; cargo_container x 10; sensor_array x 8; processing_core x 2 | empire=nebula |
| `full_habitat_dome` | 4 | -- | -- | 10,500,000 | 100 | steel_plate x 3900; water_recycler x 630 | player_station_buildable |
| `fusion_array` | 4 | -- | -- | 21,000,000 | 160 | steel_plate x 40000; power_cell x 8000; circuit_board x 4000 | -- |
| `grand_hotel_resort` | 4 | -- | -- | 1,200,000 | 150 | steel_plate x 400; flex_polymer x 250; circuit_board x 120 | player_station_buildable |
| `mobile_base_fuel_tank` | 4 | -- | -- | 40,000,000 |  | fuel_tank x 1600; ceramite_plating x 40000; steel_plate x 160000 | -- |
| `mobile_base_life_support` | 4 | -- | -- | 30,000,000 |  | life_support_array x 40; water_recycler x 16000; habitation_module x 120; reinforced_bulkhead x 150; steel_plate x 96000; circuit_board x 8000 | -- |
| `mobile_base_reactor` | 4 | -- | -- | 50,000,000 |  | station_reactor_core x 8; power_distribution_grid x 40; reinforced_bulkhead x 200; steel_plate x 80000; power_cell x 16000; circuit_board x 8000 | -- |
| `pact_war_depot` | 4 | -- | -- | 350,000 | 400 | steel_plate x 130; hull_plating x 40; weapon_housing x 15; armor_plate x 10; titanium_alloy x 5 | empire=crimson |
| `rim_rapid_response_base` | 4 | -- | -- | 300,000 | 380 | aluminum_sheet x 80; flex_polymer x 50; hull_plating x 15; thruster_nozzle x 10; fuel_tank x 5 | empire=outerrim |
| `the_leviathan_table` | 4 | -- | -- | 1,500,000 | 160 | steel_plate x 400; flex_polymer x 200; circuit_board x 150 | player_station_buildable |
| `collective_fleet_convergence` | 5 | -- | -- | 0 | 700 | -- | unique, empire=voidborn |
| `confederacy_grand_fleet_command` | 5 | -- | -- | 0 | 600 | -- | unique, empire=solarian |
| `fleet_life_support` | 5 | -- | -- | 0 | 100 | -- | unique, empire=crimson |
| `frontier_recycler` | 5 | -- | -- | 0 | 60 | -- | unique, empire=outerrim |
| `haven_ecosync` | 5 | -- | -- | 0 | 120 | -- | unique, empire=nebula |
| `haven_fleet_operations` | 5 | -- | -- | 0 | 700 | -- | unique, empire=nebula |
| `haven_promenade` | 5 | -- | -- | 0 | 200 | -- | unique, empire=nebula |
| `military_grade_reactor` | 5 | -- | -- | 0 | 250 | -- | unique, empire=crimson |
| `nebula_solar_array` | 5 | -- | -- | 0 | 100 | -- | unique, empire=nebula |
| `null_atmosphere_processor` | 5 | -- | -- | 0 | 200 | -- | unique, empire=voidborn |
| `null_energy_tap` | 5 | -- | -- | 0 | 300 | -- | unique, empire=voidborn |
| `pact_grand_armory` | 5 | -- | -- | 0 | 700 | -- | unique, empire=crimson |
| `patchwork_fleet_command` | 5 | -- | -- | 0 | 650 | -- | unique, empire=outerrim |
| `salvage_reactor` | 5 | -- | -- | 0 | 150 | -- | unique, empire=outerrim |
| `solarian_biosphere` | 5 | -- | -- | 0 | 150 | -- | unique, empire=solarian |
| `solarian_fusion_plant` | 5 | -- | -- | 0 | 200 | -- | unique, empire=solarian |
| `the_halcyon_concourse` | 5 | -- | -- | 0 | 140 | -- | unique, empire=solarian |
| `the_rally_point` | 5 | -- | -- | 0 | 140 | -- | unique, empire=crimson |
| `the_rusty_welcome` | 5 | -- | -- | 0 | 140 | -- | unique, empire=outerrim |
| `the_still_current` | 5 | -- | -- | 0 | 140 | -- | unique, empire=voidborn |
| `collective_observation_node` | 1 | police | -- | 35,000 | 80 | silicate_composite x 20; circuit_board x 15; shield_emitter x 3 | empire=voidborn |
| `confederacy_patrol_office` | 1 | police | -- | 35,000 | 80 | steel_plate x 20; circuit_board x 15; sensor_array x 3 | empire=solarian |
| `federation_trade_patrol_desk` | 1 | police | -- | 35,000 | 80 | flex_polymer x 15; circuit_board x 15; cargo_container x 2 | empire=nebula |
| `pact_security_post` | 1 | police | -- | 35,000 | 80 | steel_plate x 25; tungsten_rod x 10; weapon_housing x 3 | empire=crimson |
| `rim_ranger_shack` | 1 | police | -- | 25,000 | 60 | aluminum_sheet x 15; flex_polymer x 10; hull_plating x 2 | empire=outerrim |
| `collective_compliance_annex` | 2 | police | -- | 85,000 | 150 | silicate_composite x 40; circuit_board x 25; shield_emitter x 5; processing_core x 1 | empire=voidborn |
| `confederacy_precinct_station` | 2 | police | -- | 85,000 | 150 | steel_plate x 40; circuit_board x 25; sensor_array x 5; power_cell x 5 | empire=solarian |
| `federation_enforcement_bureau` | 2 | police | -- | 85,000 | 150 | flex_polymer x 30; circuit_board x 25; cargo_container x 4; sensor_array x 3 | empire=nebula |
| `pact_garrison_block` | 2 | police | -- | 85,000 | 150 | steel_plate x 50; tungsten_rod x 20; weapon_housing x 5; hull_plating x 3 | empire=crimson |
| `rim_ranger_station` | 2 | police | -- | 65,000 | 120 | aluminum_sheet x 30; flex_polymer x 20; hull_plating x 4; thruster_nozzle x 3 | empire=outerrim |
| `collective_panopticon` | 3 | police | -- | 200,000 | 250 | silicate_composite x 80; circuit_board x 40; shield_emitter x 8; processing_core x 3; power_cell x 10 | empire=voidborn |
| `confederacy_enforcement_command` | 3 | police | -- | 200,000 | 250 | steel_plate x 80; circuit_board x 40; sensor_array x 8; power_cell x 10; processing_core x 2 | empire=solarian |
| `federation_trade_authority` | 3 | police | -- | 200,000 | 250 | flex_polymer x 60; circuit_board x 40; cargo_container x 6; sensor_array x 6; processing_core x 2 | empire=nebula |
| `pact_war_precinct` | 3 | police | -- | 200,000 | 250 | steel_plate x 100; tungsten_rod x 40; weapon_housing x 8; hull_plating x 5; armor_plate x 3 | empire=crimson |
| `rim_marshals_office` | 3 | police | -- | 150,000 | 200 | aluminum_sheet x 60; flex_polymer x 40; hull_plating x 6; thruster_nozzle x 6; fuel_tank x 4 | empire=outerrim |
| `federation_seizure_processing_center` | 5 | police | -- | 0 | 100 | -- | unique, empire=nebula |

## Personal

| Facility | Level | Gives | Needs first | Cost (cr) | Labor | Materials | Notes |
|---|---|---|---|---|---|---|---|
| `signal_relay` | 1 | drone_control | -- | 50,000 |  | circuit_board x 100; optical_fiber_bundle x 50 | -- |
| `control_hub` | 2 | drone_control | -- | 300,000 |  | circuit_board x 500; optical_fiber_bundle x 200 | -- |
| `command_center` | 3 | drone_control | -- | 1,500,000 |  | circuit_board x 1500; optical_fiber_bundle x 500; superconductor x 200 | -- |
| `crew_bunk` | 1 | quarters | -- | 10,000 |  | steel_plate x 20 | -- |
| `private_cabin` | 2 | quarters | -- | 50,000 |  | steel_plate x 100; circuit_board x 20 | -- |
| `officers_suite` | 3 | quarters | -- | 250,000 |  | steel_plate x 500; circuit_board x 100; flex_polymer x 50 | -- |
| `captains_estate` | 4 | quarters | -- | 1,000,000 |  | steel_plate x 2000; circuit_board x 500; titanium_alloy x 200 | -- |
| `ledger_desk` | 1 | trader_office | -- | 50,000 |  | steel_plate x 100; circuit_board x 50 | -- |
| `trading_office` | 2 | trader_office | -- | 300,000 |  | steel_plate x 500; circuit_board x 200 | -- |
| `brokerage` | 3 | trader_office | -- | 1,500,000 |  | steel_plate x 1500; circuit_board x 500; titanium_alloy x 200 | -- |
| `workshop_toolkit` | 1 | workshop | -- | 25,000 |  | steel_plate x 50; heat_sink x 2 | -- |
| `workshop_power_tools` | 2 | workshop | -- | 150,000 |  | steel_plate x 250; circuit_board x 50; heat_sink x 5 | -- |
| `workshop_fabricator` | 3 | workshop | -- | 750,000 |  | steel_plate x 1000; circuit_board x 250; titanium_alloy x 100 | -- |

## Ranch

| Facility | Level | Gives | Needs first | Cost (cr) | Labor | Materials | Notes |
|---|---|---|---|---|---|---|---|
| `wildlife_corral` | 1 | -- | -- | 750,000 | 40 | steel_plate x 120; flex_polymer x 80; fuel_cell x 20 | station_or_faction_only |
| `range_station` | 2 | -- | -- | 1,500,000 | 100 | steel_plate x 300; flex_polymer x 180; circuit_board x 40; fuel_cell x 50 | station_or_faction_only |
| `ranch_complex` | 3 | -- | -- | 3,000,000 | 250 | steel_plate x 700; flex_polymer x 400; circuit_board x 150; fuel_cell x 120 | station_or_faction_only |

## Service

| Facility | Level | Gives | Needs first | Cost (cr) | Labor | Materials | Notes |
|---|---|---|---|---|---|---|---|
| `crafting_workshop` | 1 | crafting | -- | 500,000 | 60 | steel_plate x 800; circuit_board x 400 | -- |
| `faction_workshop` | 1 | crafting | -- | 500,000 | 60 | steel_plate x 800; circuit_board x 400 | player_station_buildable |
| `fabrication_lab` | 2 | crafting | -- | 1,500,000 | 80 | steel_plate x 2800; circuit_board x 1400 | -- |
| `assembly_works` | 3 | crafting | -- | 4,500,000 | 100 | steel_plate x 7200; circuit_board x 3600; power_cell x 600 | -- |
| `precision_foundry` | 4 | crafting | -- | 13,500,000 | 120 | steel_plate x 16000; circuit_board x 8000; power_cell x 2000 | -- |
| `fleet_weapons_forge` | 5 | crafting | -- | 0 | 100 | -- | unique, empire=crimson |
| `frontier_machine_shop` | 5 | crafting | -- | 0 | 60 | -- | unique, empire=outerrim |
| `haven_makers_market` | 5 | crafting | -- | 0 | 120 | -- | unique, empire=nebula |
| `null_energy_shaping_chamber` | 5 | crafting | -- | 0 | 150 | -- | unique, empire=voidborn |
| `solarian_research_labs` | 5 | crafting | -- | 0 | 150 | -- | unique, empire=solarian |
| `pirate_boarding_drill_deck` | 1 | marine_training | -- | 0 | 90 | -- | empire=pirates |
| `security_training_post` | 1 | marine_training | -- | 500,000 | 90 | steel_plate x 700; circuit_board x 150 | player_station_buildable |
| `marine_training_barracks` | 2 | marine_training | -- | 1,500,000 | 170 | steel_plate x 2400; circuit_board x 600; flex_polymer x 300 | player_station_buildable |
| `fleet_marine_academy` | 3 | marine_training | -- | 4,500,000 | 300 | steel_plate x 7000; circuit_board x 1900; flex_polymer x 1100; power_cell x 500 | player_station_buildable |
| `expeditionary_warfare_command` | 4 | marine_training | -- | 13,500,000 | 550 | steel_plate x 20000; circuit_board x 5500; flex_polymer x 3200; power_cell x 1500 | player_station_buildable |
| `crimson_legion_academy` | 5 | marine_training | -- | 0 | 700 | -- | unique, empire=crimson |
| `market_terminal` | 1 | market | -- | 500,000 | 100 | circuit_board x 400 | -- |
| `trade_concourse` | 1 | market | -- | 500,000 | 100 | circuit_board x 400 | player_station_buildable |
| `treasure_cache_market` | 1 | market | -- | 0 | 100 | -- | -- |
| `trade_exchange` | 2 | market | -- | 1,500,000 | 150 | circuit_board x 1400; steel_plate x 700 | -- |
| `black_market_hub` | 3 | market | -- | 0 | 250 | -- | empire=pirates |
| `commerce_hub` | 3 | market | -- | 4,500,000 | 250 | circuit_board x 3600; steel_plate x 2400 | -- |
| `trade_nexus` | 4 | market | -- | 13,500,000 | 400 | circuit_board x 10000; steel_plate x 6000; power_cell x 1000 | -- |
| `frontier_exchange` | 5 | market | -- | 0 | 300 | -- | unique, empire=outerrim |
| `grand_solarian_exchange` | 5 | market | -- | 0 | 500 | -- | unique, empire=solarian |
| `haven_grand_bazaar` | 5 | market | -- | 0 | 400 | -- | unique, empire=nebula |
| `void_nexus_exchange` | 5 | market | -- | 0 | 500 | -- | unique, empire=voidborn |
| `war_market` | 5 | market | -- | 0 | 500 | -- | unique, empire=crimson |
| `first_aid_ward` | 1 | medical | -- | 500,000 | 100 | steel_plate x 400; circuit_board x 250; medical_supplies x 200 | player_station_buildable |
| `pirate_sawbones_ward` | 1 | medical | -- | 0 | 100 | -- | empire=pirates |
| `trauma_clinic` | 2 | medical | -- | 1,500,000 | 180 | steel_plate x 1400; circuit_board x 900; flex_polymer x 500; medical_supplies x 700 | player_station_buildable |
| `surgical_center` | 3 | medical | -- | 4,500,000 | 320 | steel_plate x 4200; circuit_board x 2800; flex_polymer x 1600; medical_supplies x 2400 | player_station_buildable |
| `regenerative_medical_complex` | 4 | medical | -- | 13,500,000 | 600 | steel_plate x 12000; circuit_board x 8500; flex_polymer x 5000; medical_supplies x 7000 | player_station_buildable |
| `solarian_biotics_institute` | 5 | medical | -- | 0 | 750 | -- | unique, empire=solarian |
| `contract_terminal` | 1 | missions | -- | 500,000 | 30 | circuit_board x 200 | player_station_buildable |
| `mission_board` | 1 | missions | -- | 500,000 | 30 | circuit_board x 200 | -- |
| `contract_office` | 2 | missions | -- | 1,500,000 | 50 | circuit_board x 700; steel_plate x 350 | -- |
| `commission_hall` | 3 | missions | -- | 4,500,000 | 80 | circuit_board x 2400; steel_plate x 1200 | -- |
| `operations_center` | 4 | missions | -- | 13,500,000 | 120 | circuit_board x 6000; steel_plate x 3000; power_cell x 1000 | -- |
| `confederacy_administrative_bureau` | 5 | missions | -- | 0 | 200 | -- | unique, empire=solarian |
| `crimson_fleet_command` | 5 | missions | -- | 0 | 100 | -- | unique, empire=crimson |
| `haven_trade_commission` | 5 | missions | -- | 0 | 150 | -- | unique, empire=nebula |
| `pattern_council_terminal` | 5 | missions | -- | 0 | 150 | -- | unique, empire=voidborn |
| `the_notice_board` | 5 | missions | -- | 0 | 15 | -- | unique, empire=outerrim |
| `crew_registry` | 1 | personnel | -- | 500,000 | 80 | steel_plate x 500; circuit_board x 200 | player_station_buildable |
| `pirate_crew_muster` | 1 | personnel | -- | 0 | 80 | -- | empire=pirates |
| `personnel_bureau` | 2 | personnel | -- | 1,500,000 | 150 | steel_plate x 1800; circuit_board x 700; flex_polymer x 300 | player_station_buildable |
| `sector_labor_exchange` | 3 | personnel | -- | 4,500,000 | 280 | steel_plate x 5200; circuit_board x 2200; flex_polymer x 1000 | player_station_buildable |
| `fleet_personnel_command` | 4 | personnel | -- | 13,500,000 | 500 | steel_plate x 15000; circuit_board x 6500; flex_polymer x 3000; power_cell x 1200 | player_station_buildable |
| `fuel_depot` | 1 | refuel | -- | 500,000 | 60 | steel_plate x 800; fuel_cell x 2000 | -- |
| `refueling_dock` | 1 | refuel | -- | 500,000 | 60 | steel_plate x 800; fuel_cell x 2000 | player_station_buildable |
| `refueling_station` | 2 | refuel | -- | 1,500,000 | 80 | steel_plate x 2800; fuel_cell x 5600 | -- |
| `fuel_distribution_center` | 3 | refuel | -- | 4,500,000 | 100 | steel_plate x 7200; fuel_cell x 12000; circuit_board x 600 | -- |
| `fuel_grid` | 4 | refuel | -- | 13,500,000 | 120 | steel_plate x 16000; fuel_cell x 24000; circuit_board x 2000 | -- |
| `fleet_fuel_bunker` | 5 | refuel | -- | 0 | 100 | -- | unique, empire=crimson |
| `frontier_fuel_siphon` | 5 | refuel | -- | 0 | 80 | -- | unique, empire=outerrim |
| `haven_fuel_plaza` | 5 | refuel | -- | 0 | 150 | -- | unique, empire=nebula |
| `solarian_fuel_grid` | 5 | refuel | -- | 0 | 150 | -- | unique, empire=solarian |
| `void_energy_dispenser` | 5 | refuel | -- | 0 | 150 | -- | unique, empire=voidborn |
| `repair_bay` | 1 | repair | -- | 500,000 | 80 | steel_plate x 1200; repair_kit x 400 | -- |
| `repair_slip` | 1 | repair | -- | 500,000 | 80 | steel_plate x 1200; repair_kit x 400 | player_station_buildable |
| `maintenance_deck` | 2 | repair | -- | 1,500,000 | 100 | steel_plate x 4200; repair_kit x 1400 | -- |
| `restoration_works` | 3 | repair | -- | 4,500,000 | 120 | steel_plate x 9600; repair_kit x 3600; circuit_board x 1200 | -- |
| `engineering_complex` | 4 | repair | -- | 13,500,000 | 160 | steel_plate x 24000; repair_kit x 8000; circuit_board x 4000 | -- |
| `crimson_armor_works` | 5 | repair | -- | 0 | 150 | -- | unique, empire=crimson |
| `frontier_weld_shop` | 5 | repair | -- | 0 | 100 | -- | unique, empire=outerrim |
| `haven_repair_complex` | 5 | repair | -- | 0 | 180 | -- | unique, empire=nebula |
| `reconstruction_matrix` | 5 | repair | -- | 0 | 200 | -- | unique, empire=voidborn |
| `solarian_precision_drydock` | 5 | repair | -- | 0 | 200 | -- | unique, empire=solarian |
| `reclamation_dock` | 1 | salvage_yard | -- | 500,000 | 60 | steel_plate x 2000; circuit_board x 200 | player_station_buildable |
| `salvage_bay` | 1 | salvage_yard | -- | 500,000 | 60 | steel_plate x 2000; circuit_board x 200 | -- |
| `salvage_dock` | 2 | salvage_yard | -- | 1,500,000 | 80 | steel_plate x 5600; circuit_board x 700 | -- |
| `salvage_works` | 3 | salvage_yard | -- | 4,500,000 | 100 | steel_plate x 14400; circuit_board x 1800; thermal_ceramic x 1200 | -- |
| `salvage_complex` | 4 | salvage_yard | -- | 13,500,000 | 120 | steel_plate x 36000; circuit_board x 5000; thermal_ceramic x 3000; galactic_standard_alloy x 1000 | -- |
| `outfitting_bay` | 1 | shipyard | -- | 500,000 | 200 | steel_plate x 4000; circuit_board x 800 | player_station_buildable |
| `shipyard` | 1 | shipyard | -- | 500,000 | 200 | steel_plate x 4000; circuit_board x 800 | -- |
| `drydock` | 2 | shipyard | -- | 1,500,000 | 250 | steel_plate x 14000; circuit_board x 2800 | -- |
| `fabrication_yard` | 2 | shipyard | -- | 1,500,000 | 250 | steel_plate x 14000; circuit_board x 2800 | player_station_buildable |
| `assembly_complex` | 3 | shipyard | -- | 4,500,000 | 300 | steel_plate x 36000; circuit_board x 7200; power_cell x 1200 | player_station_buildable |
| `naval_yard` | 3 | shipyard | -- | 4,500,000 | 300 | steel_plate x 36000; circuit_board x 7200; power_cell x 1200 | -- |
| `fleet_yards` | 4 | shipyard | -- | 13,500,000 | 350 | steel_plate x 80000; circuit_board x 16000; power_cell x 4000 | -- |
| `grand_shipworks` | 4 | shipyard | -- | 13,500,000 | 350 | steel_plate x 80000; circuit_board x 16000; power_cell x 4000 | player_station_buildable |
| `crimson_war_forge` | 5 | shipyard | -- | 0 | 350 | -- | unique, empire=crimson |
| `crystalline_cradle` | 5 | shipyard | -- | 0 | 350 | -- | unique, empire=voidborn |
| `frontier_salvage_yard` | 5 | shipyard | -- | 0 | 200 | -- | unique, empire=outerrim |
| `haven_ship_showroom` | 5 | shipyard | -- | 0 | 300 | -- | unique, empire=nebula |
| `solarian_naval_shipyard` | 5 | shipyard | -- | 0 | 400 | -- | unique, empire=solarian |
| `locker_bay` | 1 | storage | -- | 500,000 | 40 | steel_plate x 1600 | player_station_buildable |
| `storage_bay` | 1 | storage | -- | 500,000 | 40 | steel_plate x 1600 | -- |
| `cargo_hold` | 2 | storage | -- | 1,500,000 | 50 | steel_plate x 5600 | -- |
| `warehouse` | 3 | storage | -- | 4,500,000 | 60 | steel_plate x 14400; circuit_board x 1200 | -- |
| `logistics_hub` | 4 | storage | -- | 13,500,000 | 80 | steel_plate x 32000; circuit_board x 4000 | -- |
| `confederacy_bonded_warehouse` | 5 | storage | -- | 0 | 120 | -- | unique, empire=solarian |
| `dimensional_vault` | 5 | storage | -- | 0 | 100 | -- | unique, empire=voidborn |
| `fleet_munitions_vault` | 5 | storage | -- | 0 | 60 | -- | unique, empire=crimson |
| `haven_premium_storage` | 5 | storage | -- | 0 | 80 | -- | unique, empire=nebula |
| `hull_lockers` | 5 | storage | -- | 0 | 30 | -- | unique, empire=outerrim |

## Production

2667 production lines (level 1: 824, level 2: 630, level 3: 600, level 4: 596, level 5: 17). Each runs one recipe: the recipe's row in `recipes/` names its
lines; a line's cost and materials are in `tables/facilities.tsv` and in `craftbook.py build <facility id>`.
