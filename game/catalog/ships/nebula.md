# Nebula -- Hulls

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.732.3; never edited by hand.
Up: [master-index.md](../master-index.md). Hulls: 66. The Piloting a tier needs, from the hulls of the catalog: tier 2: Piloting 10; tier 3: Piloting 20; tier 4: Piloting 30; tier 5: Piloting 50.
What a hull is built from: `python3 -I -B game/fleet/craftbook.py build <hull id>`, or `tables/ships.tsv`.

## Tier 0

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `prospect` | Miner | Industrial | -- | 0 | 95 / 50 / 4 | 1 | 130 | 100 | 1 / 1 / 2 | 13 / 26 | mining_laser_i, pulse_laser_i |

## Tier 1

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `nebula_tender` | Shuttle | Civilian | -- | 0 | 70 / 40 / 3 | 3 | 170 | 70 | 0 / 1 / 2 | 12 / 24 | cargo_expander_i |
| `underwriter` | Raider | Combat | -- | 0 | 130 / 70 / 6 | 3 | 160 | 50 | 2 / 1 / 1 | 16 / 34 | pulse_laser_i, pulse_laser_i, shield_booster_i |
| `overhead` | Patrol | Combat Support | -- | 0 | 110 / 60 / 5 | 3 | 130 | 45 | 2 / 1 / 2 | 18 / 34 | pulse_laser_i, pulse_laser_i, shield_booster_i |
| `dividend` | Freighter | Commercial | -- | 0 | 110 / 55 / 5 | 2 | 160 | 220 | 0 / 1 / 2 | 14 / 26 | cargo_expander_i, cargo_expander_i |
| `floor_price` | Freighter | Commercial | -- | 0 | 55 / 15 / 1 | 1 | 120 | 400 | 0 / 0 / 1 | 6 / 14 | cargo_expander_i |
| `futures` | Courier | Commercial | -- | 0 | 65 / 40 / 2 | 6 | 120 | 30 | 0 / 0 / 2 | 22 / 34 | ship_scanner_i |
| `leverage` | Courier | Commercial | -- | 0 | 120 / 55 / 6 | 2 | 140 | 120 | 1 / 1 / 2 | 14 / 30 | pulse_laser_i, cargo_expander_i |
| `margin` | Courier | Commercial | -- | 0 | 80 / 45 / 3 | 4 | 170 | 70 | 0 / 1 / 2 | 13 / 26 | cargo_expander_i |
| `venture` | Explorer | Exploration | -- | 0 | 80 / 45 / 4 | 3 | 180 | 80 | 1 / 1 / 2 | 14 / 28 | cargo_expander_i |
| `appraisal` | Salvager | Industrial | -- | 0 | 70 / 35 / 2 | 1 | 120 | 150 | 0 / 1 / 2 | 12 / 22 | basic_tow_rig, cargo_expander_i |
| `bonanza` | Miner | Industrial | -- | 0 | 75 / 30 / 2 | 1 | 140 | 180 | 0 / 1 / 3 | 12 / 24 | mining_laser_i, mining_laser_i, mining_laser_i |
| `frost_dividend` | Ice Harvester | Industrial | -- | 0 | 75 / 40 / 3 | 2 | 130 | 95 | 0 / 1 / 2 | 14 / 28 | ice_harvester_i, ice_harvester_i |
| `yield` | Gas Harvester | Industrial | -- | 0 | 85 / 45 / 3 | 2 | 190 | 85 | 0 / 1 / 2 | 14 / 28 | gas_harvester_i |

## Tier 2

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `consortium` | Liner | Civilian | 10 | 1 | 170 / 100 / 7 | 3 | 250 | 95 | 0 / 2 / 2 | 24 / 50 | -- |
| `franchise` | Drone Carrier | Combat Support | 10 | 1 | 175 / 85 / 7 | 2 | 210 | 180 | 1 / 1 / 4 | 30 / 55 | ion_blaster_i, shield_booster_ii, light_drone_bay, light_drone_bay, ship_maintenance_bay, afterburner_ii |
| `bulk_terms` | Bulk Hauler | Commercial | 10 | 1 | 155 / 45 / 4 | 2 | 200 | 350 | 0 / 1 / 2 | 12 / 26 | cargo_expander_ii |
| `caravan` | Bulk Hauler | Commercial | 10 | 1 | 200 / 90 / 9 | 2 | 220 | 540 | 1 / 1 / 3 | 18 / 38 | cargo_expander_ii, cargo_expander_ii, shield_booster_ii |
| `portfolio` | Freighter | Commercial | 10 | 1 | 180 / 80 / 8 | 3 | 420 | 300 | 2 / 1 / 3 | 22 / 45 | pulse_laser_ii, shield_booster_ii, cargo_expander_ii |
| `recovery_notice` | Recovery Frigate | Commercial | 10 | 1 | 190 / 125 / 9 | 3 | 260 | 165 | 1 / 2 / 4 | 34 / 65 | pulse_laser_ii, shield_booster_ii, assault_barracks, cargo_expander_ii |
| `arbitrage` | Smuggler | Covert | 10 | 1 | 150 / 70 / 6 | 4 | 550 | 145 | 1 / 1 / 3 | 20 / 42 | afterburner_ii, shield_booster_ii |
| `prospectus` | Scout | Exploration | 10 | 1 | 140 / 70 / 6 | 5 | 450 | 80 | 1 / 1 / 3 | 24 / 45 | survey_scanner_i, cargo_expander_i |
| `cold_storage` | Ice Harvester | Industrial | 10 | 1 | 200 / 65 / 12 | 2 | 360 | 180 | 0 / 1 / 3 | 18 / 40 | ice_harvester_ii, ice_harvester_ii, armor_plate_ii |
| `motherlode` | Miner | Industrial | 10 | 1 | 170 / 70 / 8 | 2 | 420 | 200 | 0 / 1 / 3 | 18 / 40 | mining_laser_ii, ship_scanner_ii |
| `reclaim` | Salvager | Industrial | 10 | 1 | 180 / 65 / 8 | 3 | 315 | 280 | 0 / 1 / 3 | 18 / 40 | advanced_tow_rig, afterburner_ii |
| `revenue` | Gas Harvester | Industrial | 10 | 1 | 190 / 75 / 8 | 2 | 270 | 180 | 0 / 1 / 3 | 20 / 42 | gas_harvester_ii, gas_harvester_ii, cargo_expander_ii |
| `benefit` | Medical | Support | 10 | 1 | 160 / 100 / 7 | 3 | 220 | 120 | 0 / 2 / 4 | 26 / 50 | shipboard_sickbay, shield_booster_ii, cargo_expander_ii |

## Tier 3

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ambrosia` | Restaurant Cruiser | Civilian | -- | 2 | 400 / 280 / 18 | 3 | 500 | 260 | 0 / 3 / 5 | 55 / 100 | shield_booster_iii, damage_control_system, ship_scanner_ii, cargo_expander_iii, promenade_lounge |
| `midas` | Yacht | Civilian | -- | 2 | 600 / 420 / 70 | 5 | 800 | 150 | 0 / 4 / 6 | 45 / 100 | shield_booster_iii, shield_booster_iii, regenerative_armor_ii, ship_scanner_ii |
| `treasury` | Yacht | Civilian | 20 | 2 | 350 / 250 / 15 | 3 | 500 | 120 | 1 / 3 / 5 | 35 / 80 | shield_booster_iii, shield_booster_ii, cargo_expander_ii |
| `collateral` | Interceptor | Combat | 20 | 2 | 130 / 240 / 10 | 5 | 500 | 20 | 3 / 2 / 2 | 35 / 80 | pulse_laser_iii, pulse_laser_ii, pulse_laser_ii, shield_booster_iii, em_shield_hardener, afterburner_ii, fuel_optimizer |
| `tariff` | Cruiser | Combat Support | 20 | 2 | 380 / 260 / 18 | 3 | 350 | 150 | 3 / 3 / 3 | 38 / 95 | ion_blaster_ii, pulse_laser_iii, emp_pulse_ii, shield_booster_iii, damage_control_system, em_shield_hardener, warp_scrambler |
| `enterprise` | Bulk Hauler | Commercial | 20 | 2 | 400 / 200 / 10 | 2 | 400 | 800 | 0 / 1 / 4 | 28 / 65 | cargo_expander_iii, cargo_expander_ii, cargo_expander_ii, ship_scanner_ii |
| `liability` | Hazmat Freighter | Commercial | 20 | 2 | 480 / 220 / 18 | 2 | 400 | 500 | 1 / 2 / 4 | 36 / 50 | lead_lined_cargo_i, shield_booster_ii |
| `monopoly` | Cruiser | Commercial | 20 | 2 | 420 / 300 / 18 | 2 | 380 | 155 | 3 / 3 / 4 | 42 / 100 | pulse_laser_ii, pulse_laser_ii, shield_booster_iii, ship_scanner_ii |
| `reserve` | Tanker | Commercial | 20 | 2 | 380 / 180 / 16 | 2 | 4000 | 150 | 1 / 2 / 3 | 28 / 72 | refueling_pump |
| `syndicate` | Freighter | Commercial | 20 | 2 | 200 / 220 / 12 | 5 | 580 | 220 | 2 / 2 / 5 | 40 / 85 | pulse_laser_ii, pulse_laser_ii, shield_booster_ii, shield_booster_ii, cargo_expander_iii, cargo_expander_iii, cargo_expander_ii, fuel_optimizer, afterburner_ii |
| `waystation` | Carrier | Commercial | 20 | 2 | 520 / 200 / 20 | 1 | 500 | 200 | 0 / 2 / 3 | 20 / 60 | shield_booster_ii, shield_booster_ii |
| `survey_vessel` | Explorer | Exploration | 20 | 2 | 340 / 200 / 14 | 3 | 1020 | 305 | 2 / 2 / 5 | 42 / 90 | anomaly_detector, cargo_expander_iii, cargo_expander_iii |
| `bonanza_king` | Miner | Industrial | 20 | 2 | 380 / 170 / 12 | 1 | 280 | 600 | 0 / 1 / 6 | 38 / 85 | mining_laser_iii, cargo_expander_ii, ship_scanner_ii |
| `gas_tanker` | Gas Harvester | Industrial | 20 | 2 | 320 / 150 / 10 | 1 | 280 | 650 | 0 / 1 / 4 | 28 / 65 | gas_harvester_iii, cargo_expander_iii, cargo_expander_ii |
| `ice_dividend` | Ice Harvester | Industrial | 20 | 2 | 330 / 150 / 10 | 1 | 280 | 550 | 0 / 1 / 4 | 30 / 68 | ice_harvester_iii, ice_harvester_iii, cargo_expander_ii |
| `receivership` | Salvager | Industrial | 20 | 2 | 400 / 150 / 14 | 2 | 350 | 685 | 1 / 2 / 4 | 30 / 80 | advanced_tow_rig, cargo_expander_iii, cargo_expander_ii, ship_scanner_ii |
| `subcontract` | Workshop | Industrial | 20 | 2 | 380 / 200 / 12 | 1 | 340 | 720 | 0 / 1 / 5 | 34 / 85 | -- |
| `continuity` | Medical Freighter | Support | 20 | 2 | 470 / 270 / 18 | 3 | 520 | 330 | 1 / 3 / 5 | 60 / 118 | pulse_laser_ii, shield_booster_ii, field_hospital, cargo_expander_iii, cargo_expander_ii |
| `warranty` | Repair | Support | 20 | 2 | 380 / 210 / 16 | 2 | 380 | 335 | 1 / 2 / 5 | 38 / 85 | cargo_expander_iii, cargo_expander_iii |

## Tier 4

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `comet` | Liner | Civilian | -- | 3 | 700 / 700 / 20 | 6 | 900 | 200 | 0 / 4 / 5 | 55 / 150 | shield_booster_iii, shield_booster_iii, ship_scanner_ii |
| `liquidity_event` | Yacht | Civilian | 30 | 3 | 750 / 550 / 22 | 2 | 650 | 180 | 0 / 4 / 3 | 45 / 125 | -- |
| `premiere` | Liner | Civilian | 30 | 3 | 800 / 600 / 28 | 2 | 650 | 300 | 2 / 4 / 3 | 50 / 130 | -- |
| `paramount` | Command | Combat Support | 30 | 3 | 900 / 550 / 30 | 2 | 600 | 265 | 3 / 4 / 5 | 65 / 150 | pulse_laser_ii, ship_scanner_iii, cargo_expander_iii, cargo_expander_iii, expanded_fuel_tank, shield_booster_iii, shield_booster_ii |
| `conglomerate` | Bulk Hauler | Commercial | 30 | 3 | 1000 / 500 / 35 | 1 | 600 | 2400 | 2 / 3 / 5 | 40 / 110 | cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, expanded_fuel_tank, shield_booster_iii |
| `endowment` | Tanker | Commercial | 30 | 3 | 900 / 350 / 28 | 1 | 11500 | 380 | 1 / 3 / 6 | 40 / 115 | refueling_pump, expanded_fuel_tank, expanded_fuel_tank, cargo_expander_iii, shield_booster_iii |
| `insider` | Intelligence | Covert | 30 | 3 | 750 / 500 / 25 | 3 | 550 | 145 | 2 / 3 / 6 | 75 / 170 | ship_scanner_iii, cloaking_device_ii, cargo_expander_iii, shield_booster_iii, shield_booster_ii |
| `accumulator` | Refinery | Industrial | 30 | 3 | 750 / 400 / 22 | 1 | 350 | 1020 | 0 / 2 / 5 | 40 / 105 | gas_harvester_iv |
| `frost_venture` | Refinery | Industrial | 30 | 3 | 800 / 400 / 24 | 1 | 350 | 960 | 0 / 2 / 5 | 40 / 105 | ice_harvester_iv |
| `liquidator` | Salvager | Industrial | 30 | 3 | 900 / 380 / 32 | 1 | 480 | 695 | 2 / 2 / 5 | 45 / 120 | advanced_tow_rig, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, ship_scanner_ii, shield_booster_iii |
| `paydirt` | Miner | Industrial | 30 | 3 | 800 / 400 / 25 | 1 | 400 | 2160 | 0 / 2 / 6 | 52 / 110 | mining_laser_iv, mining_laser_iv, mining_laser_iv, mining_laser_iv |
| `smelter` | Refinery | Industrial | 30 | 3 | 950 / 400 / 35 | 1 | 500 | 780 | 2 / 2 / 5 | 55 / 160 | -- |
| `macguffin` | Diplomatic Blockade-Runner | Multirole | -- | 3 | 650 / 650 / 25 | 6 | 850 | 240 | 2 / 4 / 6 | 65 / 140 | pulse_laser_iii, shield_booster_iii, regenerative_armor_ii, ship_scanner_ii, fuel_optimizer |

## Tier 5

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ascendancy` | Command | Civilian | 50 | 4 | 2200 / 1800 / 75 | 1 | 1100 | 420 | 5 / 6 / 8 | 85 / 280 | pulse_laser_iii, pulse_laser_iii, ion_blaster_iii, nebula_storm_barrier, nebula_bio_regenerator, adaptive_shield_iii, shield_booster_iv, adaptive_shield_ii |
| `hegemon` | Dreadnought | Combat | 50 | 4 | 2800 / 1600 / 90 | 1 | 900 | 840 | 6 / 5 / 7 | 90 / 320 | energy_siphon, storm_lance, ion_blaster_iii, ion_blaster_iii, pulse_laser_iii, pulse_laser_iii, nebula_storm_barrier, nebula_bio_regenerator, adaptive_shield_iii, shield_booster_iv |
| `exchange` | Drone Carrier | Combat Support | 50 | 4 | 2500 / 1400 / 80 | 1 | 1000 | 720 | 5 / 5 / 8 | 100 / 340 | storm_lance, ion_blaster_iii, ion_blaster_iii, pulse_laser_iii, pulse_laser_iii, nebula_storm_barrier, nebula_bio_regenerator, adaptive_shield_iii, shield_booster_iv, adaptive_shield_ii |
| `grand_transit` | Fleet Carrier | Commercial | 50 | 4 | 3200 / 800 / 40 | 1 | 800 | 600 | 2 / 4 / 6 | 60 / 150 | -- |
| `cryo_industrial` | Ice Harvester | Industrial | 50 | 4 | 1800 / 1000 / 55 | 1 | 600 | 3000 | 0 / 3 / 8 | 75 / 250 | ice_harvester_iv |
| `eldorado` | Miner | Industrial | 50 | 4 | 1500 / 800 / 50 | 1 | 600 | 3600 | 0 / 3 / 8 | 70 / 240 | mining_laser_v, mining_laser_v, mining_laser_v, mining_laser_v, hyper_mining_laser_iii, crystal_mining_probe |
| `foundation` | Mobile Base | Industrial | -- | 4 | 2800 / 1200 / 85 |  |  |  | None / None / None | None / None | -- |
