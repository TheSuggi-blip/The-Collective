# Modules

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.723.1; never edited by hand.
Up: [master-index.md](master-index.md). Modules: 270. A hull's slots and its cpu and power: the hull's row in `ships/`.

## Defense

| Module | Kind | CPU | Power | Base value | What it does |
|---|---|---|---|---|---|
| `adaptive_shield_i` | defense | 5 | 10 | 21000 | adaptive_resistance_10 |
| `adaptive_shield_ii` | defense | 8 | 15 | 44000 | adaptive_resistance_20 |
| `adaptive_shield_iii` | defense | 12 | 22 | 53000 | adaptive_resistance_35 |
| `armor_plate_i` | defense | 1 | 0 | 490 | -- |
| `armor_plate_ii` | defense | 2 | 0 | 1200 | -- |
| `armor_plate_iii` | defense | 3 | 0 | 1700 | -- |
| `armor_repairer_i` | defense | 3 | 8 | 4300 | -- |
| `armor_repairer_ii` | defense | 5 | 14 | 8700 | -- |
| `armor_repairer_iii` | defense | 8 | 22 | 29000 | -- |
| `crimson_berserker_plating` | defense | 6 | 8 | 16000 | damage_boost_on_hit |
| `damage_control_system` | defense | 4 | 5 | 5600 | -- |
| `darksteel_armor` | defense | 5 | 0 | 8000 | -- |
| `em_hull_hardener` | defense | 2 | 4 | 1600 | -- |
| `em_shield_hardener` | defense | 3 | 6 | 4300 | -- |
| `emergency_cloaking_system` | defense | 8 | 12 | 4700 | auto_cloak_on_shield_failure,duration_10 |
| `emergency_warp_stabilizer` | defense | 6 | 8 | 19000 | emergency_warp_at_20_hull |
| `event_horizon_plating` | defense | 8 | 6 | 40000 | -- |
| `explosive_hull_hardener` | defense | 2 | 4 | 640 | -- |
| `explosive_shield_hardener` | defense | 3 | 6 | 3700 | -- |
| `hull_integrity_field` | defense | 7 | 14 | 5500 | -- |
| `hull_reinforcement_i` | defense | 1 | 0 | 880 | -- |
| `hull_reinforcement_ii` | defense | 2 | 0 | 1100 | -- |
| `hull_reinforcement_iii` | defense | 3 | 0 | 2100 | -- |
| `kinetic_hull_hardener` | defense | 2 | 4 | 740 | -- |
| `kinetic_shield_hardener` | defense | 3 | 6 | 3800 | -- |
| `nanite_hull_coating` | defense | 10 | 15 | 21000 | repairs_all_damage_types |
| `nanocarbon_hull_lattice` | defense | 5 | 0 | 2800 | -- |
| `nebula_bio_regenerator` | defense | 6 | 10 | 1600 | bio_repair |
| `nebula_storm_barrier` | defense | 8 | 14 | 18000 | shock_attackers_15 |
| `outer_rim_scrap_armor` | defense | 2 | 0 | 3300 | repair_from_salvage |
| `quantum_entanglement_shield` | defense | 12 | 22 | 83000 | -- |
| `quantum_shield_iv` | defense | 12 | 25 | 21000 | adaptive_resistance_35 |
| `reactive_armor_hardener` | defense | 6 | 10 | 8400 | reactive_resistance |
| `regenerative_armor_i` | defense | 4 | 6 | 3900 | -- |
| `regenerative_armor_ii` | defense | 7 | 10 | 12000 | -- |
| `shield_booster_i` | defense | 2 | 4 | 1700 | -- |
| `shield_booster_ii` | defense | 3 | 6 | 7200 | -- |
| `shield_booster_iii` | defense | 5 | 10 | 13000 | -- |
| `shield_booster_iv` | defense | 8 | 15 | 18000 | -- |
| `shield_recharger_i` | defense | 2 | 5 | 1300 | -- |
| `shield_recharger_ii` | defense | 3 | 8 | 7500 | -- |
| `solarian_aegis` | defense | 8 | 15 | 23000 | reflect_energy_20 |
| `thermal_hull_hardener` | defense | 2 | 4 | 580 | -- |
| `thermal_shield_hardener` | defense | 3 | 6 | 3600 | -- |
| `void_hull_hardener` | defense | 4 | 6 | 4900 | -- |
| `void_shield_hardener` | defense | 5 | 8 | 8200 | -- |
| `voidborn_phase_armor` | defense | 9 | 12 | 26000 | phase_dodge_25 |

## Utility

| Module | Kind | CPU | Power | Base value | What it does |
|---|---|---|---|---|---|
| `crystal_mining_probe` | mining | 5 | 10 | 7200 | crystal_bonus_100 |
| `damped_mining_head_i` | mining | 6 | 10 | 19000 | -- |
| `damped_mining_head_ii` | mining | 8 | 14 | 48000 | -- |
| `damped_mining_head_iii` | mining | 10 | 18 | 150000 | -- |
| `deep_core_extractor_ii` | mining | 10 | 20 | 55000 | deep_core_access |
| `deep_core_extractor_iii` | mining | 14 | 28 | 15000 | deep_core_access |
| `deep_core_extractor_mk_i` | mining | 8 | 15 | 3000 | deep_core_access |
| `hyper_mining_laser_iii` | mining | 5 | 10 | 20000 | -- |
| `kinetic_core_drill` | mining | 7 | 14 | 10000 | -- |
| `mining_laser_i` | mining | 2 | 5 | 1600 | -- |
| `mining_laser_ii` | mining | 4 | 8 | 2500 | -- |
| `mining_laser_iii` | mining | 6 | 12 | 7900 | -- |
| `mining_laser_iv` | mining | 10 | 18 | 25000 | -- |
| `mining_laser_v` | mining | 13 | 24 | 55000 | -- |
| `modulated_mining_laser` | mining | 7 | 12 | 3900 | -- |
| `percussive_mining_array` | mining | 6 | 10 | 8000 | -- |
| `plasma_fracturing_torch` | mining | 8 | 16 | 12000 | -- |
| `strip_miner_i` | mining | 7 | 22 | 8000 | common_only |
| `strip_miner_ii` | mining | 9 | 32 | 18000 | common_only |
| `advanced_drone_bay` | utility | 12 | 15 | 4200 | -- |
| `advanced_tow_rig` | utility | 8 | 15 | 1500 | -- |
| `afterburner_i` | utility | 2 | 3 | 1100 | -- |
| `afterburner_ii` | utility | 3 | 5 | 2300 | -- |
| `afterburner_iii` | utility | 5 | 8 | 2500 | -- |
| `anomaly_detector` | utility | 15 | 25 | 20000 | anomaly_detection |
| `argon_condenser` | utility | 3 | 10 | 1400 | filter_argon_gas |
| `assault_barracks` | utility | 6 | 12 | 22000 | -- |
| `assault_boarding_lock` | utility | 10 | 18 | 28000 | -- |
| `atmospheric_processor` | utility | 8 | 28 | 7000 | filter_argon_gas,filter_hydrogen_gas,filter_neon_gas |
| `basic_tow_rig` | utility | 5 | 10 | 380 | -- |
| `boarding_clamp` | utility | 4 | 8 | 5200 | -- |
| `business_passenger_cabin` | utility | 6 | 8 | 22000 | -- |
| `capital_crew_habitat` | utility | 30 | 55 | 180000 | -- |
| `carbon_scrubber` | utility | 7 | 5 | 1500 | filter_carbon_ore |
| `cargo_expander_i` | utility | 1 | 1 | 160 | -- |
| `cargo_expander_ii` | utility | 2 | 2 | 800 | -- |
| `cargo_expander_iii` | utility | 3 | 3 | 2000 | -- |
| `citadel_security_grid` | utility | 14 | 24 | 48000 | -- |
| `cloaking_device_i` | utility | 5 | 10 | 4800 | -- |
| `cloaking_device_ii` | utility | 8 | 15 | 37000 | -- |
| `combat_drone_bay` | utility | 8 | 10 | 2000 | -- |
| `compact_aluminum_smelter` | utility | 24 | 60 | 45000 | -- |
| `compact_argon_purifier` | utility | 21 | 54 | 40000 | -- |
| `compact_copper_wiring_plant` | utility | 24 | 60 | 45000 | -- |
| `compact_deuterium_ice_processor` | utility | 19 | 48 | 35000 | -- |
| `compact_helium_ice_processor` | utility | 19 | 48 | 35000 | -- |
| `compact_hydrogen_compressor` | utility | 21 | 54 | 40000 | -- |
| `compact_lead_smelter` | utility | 24 | 60 | 45000 | -- |
| `compact_neon_ionizer` | utility | 21 | 54 | 40000 | -- |
| `compact_nitrogen_ice_processor` | utility | 19 | 48 | 35000 | -- |
| `compact_oxygen_liquefier` | utility | 21 | 54 | 40000 | -- |
| `compact_steel_refinery` | utility | 24 | 60 | 45000 | -- |
| `compact_titanium_refinery` | utility | 24 | 60 | 45000 | -- |
| `compact_water_ice_processor` | utility | 19 | 48 | 35000 | -- |
| `compact_xenon_extractor` | utility | 21 | 54 | 40000 | -- |
| `cpu_co_processor` | utility | 0 | 3 | 1000 | -- |
| `crew_armory` | utility | 4 | 5 | 9000 | -- |
| `crew_deck_expansion` | utility | 6 | 10 | 12000 | -- |
| `crew_habitat_complex` | utility | 14 | 24 | 48000 | -- |
| `crimson_berserker_core` | utility | 6 | 8 | 5400 | rage_damage_scaling |
| `deep_core_survey_scanner` | utility | 6 | 8 | 15000 | deep_core_detection,ore_quality_detection,rare_ore_detection |
| `dust_skirt_i` | utility | 2 | 2 | 12000 | -- |
| `dust_skirt_ii` | utility | 3 | 4 | 38000 | -- |
| `dust_skirt_iii` | utility | 4 | 7 | 130000 | -- |
| `ecm_jammer` | utility | 8 | 12 | 3800 | reach 3 |
| `economy_passenger_cabin` | utility | 3 | 4 | 6000 | -- |
| `electromagnetic_refinery` | utility | 12 | 18 | 6000 | filter_iron_ore,filter_copper_ore |
| `expanded_crew_quarters` | utility | 2 | 3 | 2600 | -- |
| `expanded_fuel_tank` | utility | 1 | 2 | 950 | -- |
| `field_generator` | utility | 6 | 14 | 3000 | -- |
| `field_hospital` | utility | 14 | 24 | 45000 | -- |
| `first_class_passenger_suite` | utility | 12 | 16 | 75000 | -- |
| `fleet_hospital` | utility | 22 | 38 | 95000 | -- |
| `flotation_cell` | utility | 8 | 4 | 1600 | filter_copper_ore |
| `fuel_optimizer` | utility | 3 | 2 | 800 | -- |
| `gas_harvester_i` | utility | 4 | 6 | 1200 | gas_harvesting |
| `gas_harvester_ii` | utility | 6 | 10 | 2500 | gas_harvesting |
| `gas_harvester_iii` | utility | 9 | 15 | 5000 | gas_harvesting |
| `gas_harvester_iv` | utility | 12 | 22 | 24000 | gas_harvesting |
| `grand_dining_hall` | utility | 12 | 16 | 68000 | -- |
| `hydrogen_combustor` | utility | 2 | 14 | 1500 | filter_hydrogen_gas |
| `ice_harvester_i` | utility | 4 | 7 | 1000 | ice_harvesting |
| `ice_harvester_ii` | utility | 6 | 12 | 1800 | ice_harvesting |
| `ice_harvester_iii` | utility | 9 | 18 | 9000 | ice_harvesting |
| `ice_harvester_iv` | utility | 12 | 25 | 28000 | ice_harvesting |
| `isotope_separator` | utility | 10 | 22 | 6500 | filter_water_ice,filter_nitrogen_ice |
| `lead_lined_cargo_i` | utility | 3 | 4 | 850 | hazmat_cargo |
| `lead_lined_cargo_ii` | utility | 5 | 8 | 2600 | hazmat_cargo |
| `legion_barracks` | utility | 30 | 60 | 240000 | -- |
| `lensing_veil` | utility | 14 | 22 | 200000 | -- |
| `light_drone_bay` | utility | 5 | 7 | 800 | -- |
| `magnetic_ore_separator` | utility | 2 | 12 | 1800 | filter_iron_ore |
| `marine_barracks` | utility | 2 | 4 | 5000 | -- |
| `marine_garrison_deck` | utility | 14 | 28 | 65000 | -- |
| `neon_vent` | utility | 3 | 8 | 1400 | filter_neon_gas |
| `nitrogen_vent` | utility | 4 | 9 | 1500 | filter_nitrogen_ice |
| `nuclear_reactor_i` | utility | 8 | 5 | 13000 | -- |
| `nuclear_reactor_ii` | utility | 14 | 8 | 49000 | -- |
| `onboard_galley` | utility | 4 | 5 | 9000 | -- |
| `onboard_h2o2_refinery` | utility | 20 | 50 | 48000 | -- |
| `onboard_hydrogen_refinery` | utility | 22 | 56 | 52000 | -- |
| `outer_rim_salvage_array` | utility | 5 | 6 | 5200 | -- |
| `pathfinder_drive` | utility | 18 | 30 | 120000 | pathfinder_drive |
| `phase_cloaking_device` | utility | 12 | 20 | 27000 | -- |
| `pirate_radio_scanner` | utility | 1 | 1 | 470 | pirate_radio |
| `plasma_afterburner` | utility | 8 | 12 | 4200 | -- |
| `power_reactor_upgrade` | utility | 2 | 0 | 1500 | -- |
| `promenade_lounge` | utility | 7 | 10 | 26000 | -- |
| `quantum_computer_core` | utility | 0 | 8 | 25000 | -- |
| `rad_harvester_i` | utility | 4 | 7 | 990 | rad_harvesting |
| `rad_harvester_ii` | utility | 6 | 11 | 2300 | rad_harvesting |
| `rad_harvester_iii` | utility | 9 | 18 | 4100 | rad_harvesting |
| `rad_harvester_iv` | utility | 13 | 26 | 6800 | rad_harvesting |
| `radiation_baffles_i` | utility | 2 | 3 | 14000 | -- |
| `radiation_baffles_ii` | utility | 3 | 5 | 42000 | -- |
| `radiation_baffles_iii` | utility | 4 | 8 | 140000 | -- |
| `refueling_pump` | utility | 4 | 6 | 1100 | -- |
| `remote_armor_repairer_i` | utility | 4 | 10 | 2000 | -- |
| `remote_armor_repairer_ii` | utility | 6 | 16 | 4500 | -- |
| `remote_armor_repairer_iii` | utility | 10 | 25 | 10000 | -- |
| `repair_arm` | utility | 4 | 6 | 1400 | -- |
| `salvage_module` | utility | 4 | 6 | 2000 | -- |
| `seam_glass_telescope` | utility | 16 | 24 | 240000 | -- |
| `security_bulkheads` | utility | 5 | 8 | 12000 | -- |
| `sensor_dampener` | utility | 4 | 5 | 1200 | -- |
| `shear_bracing_i` | utility | 2 | 3 | 14000 | -- |
| `shear_bracing_ii` | utility | 3 | 6 | 42000 | -- |
| `shear_bracing_iii` | utility | 5 | 10 | 140000 | -- |
| `ship_maintenance_bay` | utility | 8 | 10 | 7300 | -- |
| `ship_scanner_i` | utility | 3 | 4 | 3200 | -- |
| `ship_scanner_ii` | utility | 5 | 6 | 7000 | -- |
| `ship_scanner_iii` | utility | 7 | 10 | 22000 | -- |
| `shipboard_sickbay` | utility | 8 | 12 | 15000 | -- |
| `signal_scrubber_i` | utility | 6 | 4 | 16000 | -- |
| `signal_scrubber_ii` | utility | 10 | 6 | 48000 | -- |
| `signal_scrubber_iii` | utility | 14 | 8 | 150000 | -- |
| `stasis_webifier_i` | utility | 4 | 6 | 2500 | reach 3 |
| `stasis_webifier_ii` | utility | 6 | 10 | 4500 | reach 4 |
| `stellar_observation_deck` | utility | 18 | 24 | 140000 | -- |
| `stellar_telescope` | utility | 12 | 18 | 75000 | -- |
| `survey_scanner_i` | utility | 3 | 4 | 4400 | ore_quality_detection |
| `survey_scanner_ii` | utility | 5 | 7 | 14000 | ore_quality_detection,rare_ore_detection |
| `target_painter_i` | utility | 3 | 5 | 3000 | reach 3 |
| `target_painter_ii` | utility | 5 | 8 | 7000 | reach 5 |
| `thermal_sublimator` | utility | 5 | 10 | 1600 | filter_water_ice |
| `tracking_computer_i` | utility | 3 | 4 | 6400 | -- |
| `tracking_computer_ii` | utility | 5 | 7 | 12000 | -- |
| `tracking_computer_iii` | utility | 8 | 10 | 37500 | -- |
| `tractor_beam` | utility | 3 | 5 | 5200 | reach 2 |
| `vanadium_ejector` | utility | 3 | 13 | 1700 | filter_vanadium_ore |
| `void_reactor` | utility | 5 | 0 | 36000 | -- |
| `warp_core_stabilizer` | utility | 3 | 3 | 1500 | -- |
| `warp_disruptor` | utility | 5 | 7 | 2900 | reach 5 |
| `warp_scrambler` | utility | 6 | 8 | 4500 | reach 3 |

## Weapon

| Module | Kind | CPU | Power | Base value | What it does |
|---|---|---|---|---|---|
| `autocannon_i` | weapon | 3 | 4 | 710 | damage 10 kinetic, reach 2, cooldown 1 |
| `autocannon_ii` | weapon | 4 | 6 | 1800 | damage 18 kinetic, reach 2, cooldown 1 |
| `blood_reaver` | weapon | 9 | 20 | 8700 | damage 45 kinetic, reach 3, cooldown 2, lifesteal_20 |
| `dark_matter_projector` | weapon | 18 | 40 | 52000 | damage 150 void, reach 3, cooldown 6, ignores_resistance_100,shield_phase |
| `em_disruptor_i` | weapon | 5 | 8 | 3900 | damage 5 em, reach 2, cooldown 2, cpu_damage_10 |
| `emp_cannon_i` | weapon | 5 | 10 | 3000 | damage 8 energy, reach 3, cooldown 3, system_disable_2 |
| `emp_missile_launcher` | weapon | 8 | 12 | 5600 | damage 15 explosive, reach 6, cooldown 4, system_disable_3 |
| `emp_pulse_i` | weapon | 5 | 12 | 3800 | damage 5 em, reach 2, cooldown 4, system_disable_1 |
| `emp_pulse_ii` | weapon | 7 | 18 | 6800 | damage 10 em, reach 2, cooldown 4, system_disable_2 |
| `emp_pulse_iii` | weapon | 10 | 25 | 41000 | damage 18 em, reach 2, cooldown 5, system_disable_3 |
| `energy_siphon` | weapon | 12 | 15 | 33000 | damage 25 em, reach 3, cooldown 2, shield_drain_30,shield_transfer_50 |
| `entropy_beam` | weapon | 9 | 18 | 12000 | damage 15 void, reach 4, cooldown 2, dot_damage_10,dot_duration_5 |
| `flak_cannon_i` | weapon | 3 | 5 | 4800 | damage 15 kinetic, reach 3, cooldown 1, anti_drone_bonus_100,anti_missile_bonus_25 |
| `flak_cannon_ii` | weapon | 5 | 8 | 6200 | damage 28 kinetic, reach 3, cooldown 1, anti_drone_bonus_150,anti_missile_bonus_45 |
| `flak_cannon_iii` | weapon | 8 | 12 | 30000 | damage 40 kinetic, reach 3, cooldown 1, anti_drone_bonus_200,anti_missile_bonus_65 |
| `focused_beam_i` | weapon | 4 | 10 | 8700 | damage 15 energy, reach 4, cooldown 2, shield_bypass_25 |
| `focused_beam_ii` | weapon | 6 | 15 | 17000 | damage 25 energy, reach 4, cooldown 2, shield_bypass_40 |
| `focused_beam_iii` | weapon | 10 | 22 | 27000 | damage 40 energy, reach 4, cooldown 2, shield_bypass_60 |
| `fury_cannon` | weapon | 14 | 32 | 37000 | damage 70 kinetic, reach 5, cooldown 3, rage_damage_scaling |
| `galvanic_hull_grid` | weapon | 8 | 15 | 22000 | damage 70 energy, cooldown 2 |
| `graviton_beam_i` | weapon | 8 | 15 | 4200 | damage 32 kinetic, reach 4, cooldown 3, hull_damage_bonus_25 |
| `graviton_beam_ii` | weapon | 12 | 22 | 37000 | damage 50 kinetic, reach 4, cooldown 3, hull_damage_bonus_50 |
| `heavy_mass_driver` | weapon | 15 | 35 | 25000 | damage 150 kinetic, reach 6, cooldown 5, armor_bypass_80,hull_damage_bonus_50 |
| `heavy_pulse_laser` | weapon | 8 | 20 | 27000 | damage 45 energy, reach 3, cooldown 2 |
| `heavy_torpedo` | weapon | 8 | 8 | 4000 | damage 80 explosive, reach 6, cooldown 5 |
| `ion_beam_array` | weapon | 8 | 18 | 11000 | damage 30 energy, reach 3, cooldown 2 |
| `ion_blaster_i` | weapon | 4 | 8 | 3900 | damage 8 em, reach 2, cooldown 1, shield_damage_bonus_50 |
| `ion_blaster_ii` | weapon | 6 | 12 | 7200 | damage 14 em, reach 2, cooldown 1, shield_damage_bonus_75 |
| `ion_blaster_iii` | weapon | 9 | 18 | 11000 | damage 22 em, reach 2, cooldown 1, shield_damage_bonus_100 |
| `ion_cannon_i` | weapon | 3 | 8 | 2600 | damage 12 energy, reach 5, cooldown 2 |
| `ion_cannon_ii` | weapon | 5 | 12 | 5400 | damage 20 energy, reach 5, cooldown 2 |
| `judgment_beam` | weapon | 16 | 35 | 40000 | damage 100 energy, reach 4, cooldown 4, energy_damage_bonus_50,shield_bypass_50 |
| `jury_rigged_cannon` | weapon | 7 | 14 | 2500 | damage 60 kinetic, reach 3, cooldown 2, random_damage_variance_30,low_cpu_requirement |
| `mass_driver` | weapon | 12 | 28 | 12000 | damage 130 kinetic, reach 6, cooldown 4, armor_bypass_75 |
| `mine_launcher_i` | weapon | 5 | 4 | 1800 | damage 50 explosive, reach 3, cooldown 5, mine_capacity_5,mine_duration_60 |
| `mine_launcher_ii` | weapon | 7 | 6 | 4000 | damage 80 explosive, reach 3, cooldown 4, mine_capacity_10,mine_duration_120 |
| `missile_launcher_i` | weapon | 4 | 3 | 1800 | damage 20 explosive, reach 6, cooldown 3 |
| `missile_launcher_ii` | weapon | 6 | 5 | 6500 | damage 35 explosive, reach 6, cooldown 3 |
| `neural_disruptor` | weapon | 8 | 14 | 10000 | damage 12 em, reach 3, cooldown 2, cpu_damage_25 |
| `null_cannon` | weapon | 15 | 38 | 46000 | damage 110 void, reach 3, cooldown 4, ignores_all_defense,aoe_radius_2 |
| `phase_disruptor` | weapon | 10 | 22 | 21000 | damage 48 void, reach 3, cooldown 2, phase_strike_30 |
| `piercing_railgun_i` | weapon | 5 | 12 | 5000 | damage 60 kinetic, reach 5, cooldown 3, armor_bypass_70 |
| `piercing_railgun_ii` | weapon | 8 | 20 | 15000 | damage 90 kinetic, reach 5, cooldown 3, armor_bypass_85 |
| `plasma_cannon_i` | weapon | 4 | 10 | 2200 | damage 22 thermal, reach 3, cooldown 2, hull_damage_bonus_50 |
| `plasma_cannon_ii` | weapon | 6 | 14 | 3800 | damage 38 thermal, reach 3, cooldown 2, hull_damage_bonus_50 |
| `plasma_cannon_iii` | weapon | 9 | 20 | 8100 | damage 58 thermal, reach 3, cooldown 2, armor_melt_15 |
| `plasma_cannon_iv` | weapon | 14 | 30 | 9500 | damage 85 thermal, reach 3, cooldown 2, armor_melt_30 |
| `plasma_repeater_i` | weapon | 5 | 8 | 2400 | damage 12 thermal, reach 3, cooldown 1, hull_damage_bonus_50 |
| `plasma_repeater_ii` | weapon | 7 | 12 | 4900 | damage 20 thermal, reach 3, cooldown 1, hull_damage_bonus_50 |
| `plasma_torpedo_launcher` | weapon | 8 | 14 | 7500 | damage 60 thermal, reach 6, cooldown 5, armor_melt_20 |
| `proximity_mine_launcher` | weapon | 6 | 5 | 3500 | damage 65 explosive, reach 3, cooldown 4, mine_capacity_8,mine_detection_10,mine_duration_90 |
| `pulse_laser_i` | weapon | 2 | 5 | 2500 | damage 10 energy, reach 3, cooldown 1 |
| `pulse_laser_ii` | weapon | 3 | 8 | 6900 | damage 18 energy, reach 3, cooldown 1 |
| `pulse_laser_iii` | weapon | 5 | 12 | 13000 | damage 28 energy, reach 3, cooldown 1 |
| `railgun_i` | weapon | 5 | 12 | 5000 | damage 45 kinetic, reach 5, cooldown 2 |
| `railgun_ii` | weapon | 7 | 18 | 9500 | damage 90 kinetic, reach 5, cooldown 3, armor_bypass_50 |
| `scrap_harpoon` | weapon | 4 | 7 | 1500 | damage 44 kinetic, reach 2, cooldown 3, armor_bypass_30 |
| `scrapgun` | weapon | 4 | 6 | 1100 | damage 30 kinetic, reach 2, cooldown 1, ammo_from_cargo |
| `siege_railgun` | weapon | 16 | 35 | 30000 | damage 200 kinetic, reach 6, cooldown 5, armor_bypass_90 |
| `solar_lance` | weapon | 11 | 24 | 27000 | damage 65 energy, reach 4, cooldown 3, energy_damage_bonus_25 |
| `storm_lance` | weapon | 10 | 18 | 15000 | damage 40 em, reach 3, cooldown 2, chain_lightning_2 |
| `system_disabler` | weapon | 8 | 15 | 8800 | damage 2 em, reach 3, cooldown 3, module_disable_1,target_specific |
| `tracking_mine_launcher` | weapon | 10 | 8 | 8000 | damage 100 explosive, reach 3, cooldown 6, mine_capacity_5,mine_tracking_speed_3,mine_duration_60 |
| `void_cannon` | weapon | 14 | 28 | 25000 | damage 75 void, reach 3, cooldown 3, ignores_resistance_50 |
| `void_lance_i` | weapon | 10 | 20 | 17000 | damage 55 void, reach 4, cooldown 3, ignores_resistance_50 |
| `void_lance_ii` | weapon | 14 | 30 | 40000 | damage 85 void, reach 4, cooldown 3, ignores_resistance_75 |
| `void_laser` | weapon | 14 | 26 | 143000 | damage 65 energy, reach 5, cooldown 2, shield_bypass_50 |
| `void_mine_launcher` | weapon | 14 | 12 | 56000 | damage 120 void, reach 3, cooldown 8, mine_capacity_4,mine_duration_90,ignores_resistance_50 |
| `void_torpedo_launcher` | weapon | 16 | 32 | 108000 | damage 100 void, reach 6, cooldown 5, ignores_resistance_75 |
