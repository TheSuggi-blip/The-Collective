# Solarian -- Hulls

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.723.1; never edited by hand.
Up: [master-index.md](../master-index.md). Hulls: 65. The Piloting a tier needs, from the hulls of the catalog: tier 2: Piloting 10; tier 3: Piloting 20; tier 4: Piloting 30; tier 5: Piloting 50.
What a hull is built from: `python3 -I -B game/fleet/craftbook.py build <hull id>`, or `tables/ships.tsv`.

## Tier 0

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `theoria` | Miner | Industrial | -- | 0 | 100 / 55 / 5 | 1 | 100 | 70 | 1 / 1 / 3 | 16 / 28 | mining_laser_i, pulse_laser_i |

## Tier 1

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `principia` | Shuttle | Civilian | -- | 0 | 80 / 50 / 3 | 3 | 140 | 50 | 0 / 1 / 3 | 18 / 28 | ship_scanner_i, cargo_expander_i |
| `axiom` | Fighter | Combat | -- | 0 | 120 / 75 / 7 | 3 | 130 | 30 | 2 / 1 / 2 | 20 / 38 | focused_beam_i, pulse_laser_i, shield_booster_i |
| `corollary` | Fighter | Combat | -- | 0 | 80 / 55 / 3 | 5 | 100 | 15 | 2 / 1 / 2 | 22 / 38 | focused_beam_i, pulse_laser_i, shield_booster_i |
| `precept` | Patrol | Combat Support | -- | 0 | 110 / 65 / 6 | 4 | 130 | 30 | 1 / 1 / 3 | 20 / 34 | pulse_laser_i |
| `cogito` | Courier | Commercial | -- | 0 | 85 / 50 / 4 | 3 | 200 | 45 | 0 / 1 / 3 | 16 / 28 | cargo_expander_i, ship_scanner_i |
| `datum` | Scout | Exploration | -- | 0 | 50 / 25 / 1 | 3 | 250 | 20 | 0 / 0 / 2 | 10 / 18 | -- |
| `lemma` | Scout | Exploration | -- | 0 | 70 / 45 / 3 | 5 | 170 | 25 | 0 / 1 / 3 | 22 / 30 | ship_scanner_i, cargo_expander_i |
| `aether` | Gas Harvester | Industrial | -- | 0 | 85 / 50 / 4 | 2 | 120 | 70 | 0 / 1 / 3 | 18 / 30 | gas_harvester_i, gas_harvester_i, ship_scanner_i |
| `archimedes` | Miner | Industrial | -- | 0 | 105 / 55 / 5 | 2 | 130 | 80 | 1 / 1 / 4 | 18 / 34 | mining_laser_i, mining_laser_i, cargo_expander_i, ship_scanner_i, pulse_laser_i |
| `catalogue` | Salvager | Industrial | -- | 0 | 90 / 55 / 5 | 2 | 110 | 100 | 1 / 1 / 4 | 22 / 36 | basic_tow_rig, ship_scanner_i, cargo_expander_i |
| `glacius` | Ice Harvester | Industrial | -- | 0 | 120 / 65 / 6 | 2 | 160 | 55 | 0 / 1 / 3 | 18 / 32 | ice_harvester_i, ice_harvester_i, ship_scanner_i |

## Tier 2

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `omnibus` | Liner | Civilian | 10 | 1 | 220 / 100 / 10 | 2 | 390 | 60 | 0 / 2 / 1 | 18 / 40 | -- |
| `theorem` | Heavy Fighter | Combat | 10 | 1 | 200 / 120 / 12 | 3 | 450 | 45 | 3 / 2 / 3 | 28 / 55 | pulse_laser_ii, pulse_laser_ii, focused_beam_i, shield_booster_ii, armor_plate_ii |
| `postulate` | Drone Carrier | Combat Support | 10 | 1 | 170 / 110 / 9 | 2 | 180 | 85 | 1 / 2 / 4 | 32 / 55 | pulse_laser_ii, shield_booster_ii, armor_plate_ii, light_drone_bay, light_drone_bay, ship_maintenance_bay, ship_scanner_ii |
| `scrutiny` | Customs Patrol | Combat Support | 10 | 1 | 170 / 90 / 8 | 4 | 160 | 50 | 1 / 2 / 3 | 28 / 48 | pulse_laser_i, shield_booster_i, shield_booster_i, warp_scrambler |
| `syllogism` | Electronic Warfare | Combat Support | 10 | 1 | 150 / 100 / 6 | 3 | 160 | 30 | 1 / 2 / 4 | 35 / 60 | pulse_laser_ii, shield_booster_ii, armor_plate_ii, stasis_webifier_i, warp_disruptor, target_painter_i, ship_scanner_ii |
| `capacity` | Tanker | Commercial | 10 | 1 | 190 / 70 / 9 | 2 | 1500 | 80 | 1 / 1 / 2 | 18 / 38 | refueling_pump, shield_booster_ii |
| `meridian_freighter` | Freighter | Commercial | 10 | 1 | 180 / 80 / 8 | 2 | 300 | 265 | 1 / 1 / 3 | 20 / 40 | pulse_laser_ii, shield_booster_ii, ship_scanner_ii |
| `empirica` | Research | Exploration | 10 | 1 | 155 / 95 / 6 | 2 | 270 | 125 | 0 / 2 / 5 | 34 / 55 | survey_scanner_i, cargo_expander_ii |
| `hypothesis` | Explorer | Exploration | 10 | 1 | 160 / 90 / 7 | 3 | 360 | 135 | 1 / 2 / 4 | 30 / 50 | survey_scanner_i, cargo_expander_i |
| `solarian_foundation` | Explorer | Exploration | 10 | 1 | 140 / 65 / 5 | 3 | 260 | 90 | 0 / 1 / 3 | 20 / 38 | survey_scanner_i |
| `absolute_zero` | Ice Harvester | Industrial | 10 | 1 | 180 / 85 / 8 | 2 | 390 | 175 | 0 / 1 / 4 | 22 / 42 | ice_harvester_ii, shield_booster_ii |
| `analysis` | Salvager | Industrial | 10 | 1 | 210 / 75 / 12 | 2 | 360 | 260 | 1 / 1 / 2 | 24 / 45 | advanced_tow_rig, armor_plate_ii, pulse_laser_ii |
| `excavation` | Miner | Industrial | 10 | 1 | 200 / 90 / 10 | 2 | 420 | 200 | 1 / 1 / 3 | 24 / 45 | mining_laser_ii, mining_laser_ii, pulse_laser_ii |
| `nebulae` | Gas Harvester | Industrial | 10 | 1 | 200 / 80 / 12 | 2 | 390 | 170 | 1 / 1 / 2 | 20 / 42 | gas_harvester_ii, gas_harvester_ii, armor_plate_ii |
| `triage` | Medical | Support | 10 | 1 | 155 / 100 / 7 | 3 | 180 | 70 | 0 / 2 / 4 | 28 / 48 | shipboard_sickbay, shield_booster_ii, armor_plate_ii |

## Tier 3

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `concordia` | Liner | Civilian | 20 | 2 | 220 / 200 / 8 | 6 | 600 | 30 | 0 / 2 / 2 | 35 / 75 | -- |
| `promenade` | Liner | Civilian | 20 | 2 | 380 / 220 / 16 | 2 | 400 | 95 | 1 / 2 / 2 | 38 / 85 | -- |
| `dialectic` | Assault | Combat | 20 | 2 | 520 / 280 / 28 | 2 | 420 | 115 | 5 / 3 / 3 | 42 / 120 | pulse_laser_iii, pulse_laser_iii, pulse_laser_iii, focused_beam_ii, focused_beam_ii, shield_booster_iii, armor_plate_ii, damage_control_system |
| `quorum` | Cruiser | Combat | 20 | 2 | 500 / 300 / 25 | 2 | 440 | 105 | 4 / 3 / 4 | 45 / 100 | pulse_laser_iii, pulse_laser_iii, focused_beam_ii, focused_beam_ii, shield_booster_iii, armor_plate_ii, damage_control_system, ship_scanner_ii |
| `concordance` | Command | Combat Support | 20 | 2 | 450 / 280 / 20 | 2 | 350 | 70 | 3 / 3 / 5 | 60 / 120 | pulse_laser_iii, pulse_laser_ii, shield_booster_iii, ship_scanner_ii |
| `warrant` | Patrol Cruiser | Combat Support | 20 | 2 | 500 / 340 / 22 | 3 | 390 | 145 | 2 / 3 / 5 | 68 / 125 | pulse_laser_ii, pulse_laser_ii, shield_booster_ii, armor_plate_ii, security_bulkheads, crew_armory, shipboard_sickbay |
| `compendium` | Bulk Hauler | Commercial | 20 | 2 | 480 / 200 / 22 | 1 | 350 | 625 | 1 / 2 / 3 | 32 / 80 | cargo_expander_iii, ship_scanner_ii, pulse_laser_ii |
| `dosimetry` | Hazmat Freighter | Commercial | 20 | 2 | 450 / 280 / 20 | 2 | 350 | 420 | 1 / 2 / 4 | 40 / 52 | lead_lined_cargo_i, shield_booster_ii |
| `perigee` | Explorer | Exploration | 20 | 2 | 400 / 260 / 18 | 2 | 620 | 270 | 2 / 2 / 6 | 52 / 100 | anomaly_detector, cargo_expander_iii |
| `perihelion` | Research | Exploration | 20 | 2 | 380 / 250 / 15 | 2 | 600 | 205 | 1 / 2 / 6 | 55 / 90 | anomaly_detector, cargo_expander_iii, shield_booster_ii |
| `atmospheric_sampler` | Gas Harvester | Industrial | 20 | 2 | 350 / 200 / 14 | 1 | 240 | 500 | 1 / 1 / 5 | 38 / 80 | gas_harvester_iii, gas_harvester_iii, survey_scanner_ii |
| `cryogenic_survey` | Ice Harvester | Industrial | 20 | 2 | 350 / 200 / 14 | 1 | 240 | 500 | 1 / 1 / 5 | 38 / 80 | ice_harvester_iii, ice_harvester_iii, survey_scanner_ii |
| `deep_survey` | Miner | Industrial | 20 | 2 | 420 / 200 / 18 | 1 | 240 | 750 | 1 / 1 / 5 | 34 / 75 | mining_laser_iii, cargo_expander_iii, cargo_expander_ii, pulse_laser_ii |
| `praxis` | Workshop | Industrial | 20 | 2 | 420 / 260 / 18 | 1 | 300 | 360 | 1 / 2 / 7 | 64 / 125 | -- |
| `taxonomy` | Salvager | Industrial | 20 | 2 | 380 / 160 / 18 | 2 | 330 | 600 | 1 / 2 / 4 | 38 / 85 | advanced_tow_rig, ship_scanner_ii, cargo_expander_ii, pulse_laser_ii |
| `polymath` | Multirole | Multirole | -- | 2 | 480 / 280 / 22 | 2 | 520 | 360 | 3 / 3 / 6 | 60 / 120 | pulse_laser_iii, focused_beam_ii, mining_laser_iii, mining_laser_ii, cargo_expander_iii, ship_scanner_ii, shield_booster_ii, armor_plate_ii |
| `convoy` | Carrier | Support | 20 | 2 | 490 / 260 / 22 | 1 | 440 | 160 | 1 / 3 / 3 | 28 / 72 | shield_booster_ii, damage_control_system |
| `remedy` | Repair | Support | 20 | 2 | 420 / 250 / 20 | 2 | 380 | 240 | 1 / 2 / 5 | 48 / 95 | shield_booster_iii, ship_scanner_ii |

## Tier 4

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `axiomata` | Battlecruiser | Combat | 30 | 3 | 1200 / 700 / 50 | 2 | 500 | 180 | 6 / 4 / 5 | 80 / 180 | solar_lance, focused_beam_iii, focused_beam_iii, heavy_pulse_laser, pulse_laser_iii, pulse_laser_iii, solarian_aegis, shield_booster_iv, shield_booster_iii, damage_control_system |
| `pantheon` | Drone Carrier | Combat Support | 30 | 3 | 1000 / 600 / 40 | 1 | 500 | 455 | 3 / 4 / 6 | 85 / 180 | pulse_laser_iii, focused_beam_iii, pulse_laser_iii, solarian_aegis, shield_booster_iv, adaptive_shield_ii, damage_control_system, advanced_drone_bay, combat_drone_bay, ship_maintenance_bay, ship_scanner_iii |
| `paradox_engine` | Interdictor | Combat Support | 30 | 3 | 950 / 650 / 38 | 2 | 540 | 145 | 4 / 4 / 5 | 65 / 200 | pulse_laser_iii, pulse_laser_iii, focused_beam_iii, focused_beam_ii, solarian_aegis, shield_booster_iii, damage_control_system, ship_scanner_iii |
| `logistics_prime` | Bulk Hauler | Commercial | 30 | 3 | 900 / 500 / 30 | 1 | 480 | 2160 | 1 / 3 / 5 | 48 / 120 | cargo_expander_iii, cargo_expander_iii, expanded_fuel_tank, pulse_laser_iii, shield_booster_iii |
| `sustenance` | Tanker | Commercial | 30 | 3 | 950 / 350 / 22 | 1 | 11000 | 280 | 1 / 3 / 5 | 40 / 110 | refueling_pump, expanded_fuel_tank, expanded_fuel_tank, shield_booster_iii, damage_control_system |
| `observatorium` | Research | Exploration | 30 | 3 | 850 / 550 / 30 | 2 | 900 | 335 | 2 / 3 / 7 | 80 / 180 | anomaly_detector, survey_scanner_ii, ship_scanner_ii, cargo_expander_iii, cargo_expander_iii, pulse_laser_iii, shield_booster_iii |
| `praecursor` | Pathfinder | Exploration | 30 | 3 | 850 / 500 / 32 | 2 | 1100 | 290 | 2 / 3 / 7 | 80 / 180 | pathfinder_drive, survey_scanner_ii, gas_harvester_iv, onboard_hydrogen_refinery, expanded_fuel_tank, shield_booster_iii, pulse_laser_iii, pulse_laser_iii |
| `archive` | Salvager | Industrial | 30 | 3 | 850 / 350 / 28 | 1 | 450 | 670 | 2 / 2 / 5 | 50 / 130 | advanced_tow_rig, cargo_expander_iii, cargo_expander_iii, ship_scanner_ii, pulse_laser_iii, shield_booster_iii |
| `crucible` | Refinery | Industrial | 30 | 3 | 850 / 450 / 35 | 1 | 400 | 840 | 2 / 3 / 5 | 55 / 150 | -- |
| `exosphere` | Refinery | Industrial | 30 | 3 | 800 / 500 / 30 | 1 | 320 | 780 | 1 / 2 / 7 | 50 / 130 | gas_harvester_iv |
| `glacialis` | Refinery | Industrial | 30 | 3 | 800 / 500 / 30 | 1 | 320 | 720 | 1 / 2 / 7 | 50 / 130 | ice_harvester_iv |
| `lithosphere` | Miner | Industrial | 30 | 3 | 900 / 500 / 35 | 1 | 350 | 1680 | 1 / 2 / 8 | 70 / 140 | mining_laser_iv, mining_laser_iv, mining_laser_iv, mining_laser_iv, mining_laser_iv, survey_scanner_ii |
| `encyclopedia` | Logistics | Support | 30 | 3 | 900 / 500 / 35 | 2 | 600 | 720 | 2 / 3 / 6 | 50 / 120 | cargo_expander_iii, cargo_expander_iii, ship_scanner_ii, expanded_fuel_tank, pulse_laser_iii, shield_booster_iii |
| `panacea` | Medical | Support | 30 | 3 | 900 / 550 / 32 | 2 | 500 | 215 | 2 / 3 / 6 | 60 / 140 | fleet_hospital, shipboard_sickbay |
| `reliquary` | Fleet Carrier | Support | -- | 3 | 1200 / 700 / 40 | 2 | 700 | 400 | 2 / 5 / 5 | 50 / 130 | shield_booster_iii, shield_booster_iii, damage_control_system, ship_scanner_ii |

## Tier 5

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `opus_magna` | Dreadnought | Combat | 50 | 4 | 3000 / 1800 / 120 | 1 | 800 | 600 | 8 / 6 / 6 | 125 / 350 | judgment_beam, solar_lance, focused_beam_iii, focused_beam_iii, heavy_pulse_laser, heavy_pulse_laser, pulse_laser_iii, pulse_laser_iii, solarian_aegis, adaptive_shield_iii, shield_booster_iv, shield_booster_iii, darksteel_armor, nanite_hull_coating |
| `symposium` | Command | Combat Support | 50 | 4 | 2800 / 1600 / 100 | 1 | 900 | 420 | 6 / 6 / 8 | 120 / 380 | judgment_beam, solar_lance, heavy_pulse_laser, focused_beam_iii, pulse_laser_iii, pulse_laser_iii, solarian_aegis, adaptive_shield_iii, shield_booster_iv, shield_booster_iii, darksteel_armor, nanite_hull_coating |
| `civitas` | Mobile Base | Industrial | -- | 4 | 2200 / 1100 / 80 |  |  |  | None / None / None | None / None | -- |
| `tellurian` | Miner | Industrial | 50 | 4 | 1800 / 1000 / 65 | 1 | 600 | 2400 | 1 / 3 / 10 | 85 / 280 | mining_laser_v, mining_laser_v, mining_laser_v, mining_laser_v, hyper_mining_laser_iii, modulated_mining_laser, survey_scanner_ii, pulse_laser_iii |
| `fundament` | Logistics | Support | 50 | 4 | 2500 / 1200 / 90 | 1 | 1000 | 960 | 3 / 5 / 7 | 80 / 280 | pulse_laser_iii, pulse_laser_iii, focused_beam_iii, solarian_aegis, adaptive_shield_iii, shield_booster_iv, darksteel_armor, nanite_hull_coating |
