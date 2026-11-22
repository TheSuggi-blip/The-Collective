# Pirate and other -- Hulls

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.733.0; never edited by hand.
Up: [master-index.md](../master-index.md). Hulls: 53. The Piloting a tier needs, from the hulls of the catalog: tier 2: Piloting 10; tier 3: Piloting 20; tier 4: Piloting 30; tier 5: Piloting 50.
What a hull is built from: `python3 -I -B game/fleet/craftbook.py build <hull id>`, or `tables/ships.tsv`.

## Tier 1

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `lawn_dart` | Interceptor | Combat | -- | 0 | 75 / 40 / 2 | 6 | 100 | 20 | 2 / 0 / 1 | 12 / 30 | autocannon_i, autocannon_i, ship_scanner_i |
| `ledger` | Freighter | Commercial | -- | 0 | 150 / 70 / 8 | 4 | 100 | 480 | 0 / 0 / 0 | 4 / 10 | -- |
| `runner` | Courier | Commercial | -- | 0 | 90 / 60 / 3 | 6 | 160 | 120 | 0 / 0 / 2 | 12 / 24 | ship_scanner_i |
| `start_praying` | Freighter | Commercial | -- | 0 | 40 / 0 / 0 | 3 | 100 | 500 | 1 / 0 / 0 | 7 / 14 | autocannon_i |
| `insider_trading` | Courier | Covert | -- | 0 | 60 / 35 / 2 | 6 | 140 | 25 | 0 / 0 / 2 | 22 / 34 | ship_scanner_i |
| `lemming` | Scout | Exploration | -- | 0 | 80 / 40 / 3 | 5 | 170 | 30 | 1 / 1 / 2 | 15 / 28 | autocannon_i, armor_plate_i, ship_scanner_i |
| `overdue` | Courier | Exploration | -- | 0 | 80 / 45 / 3 | 4 | 160 | 65 | 1 / 1 / 1 | 10 / 26 | autocannon_i, armor_plate_i, ship_scanner_i |
| `red_herring` | Scout | Exploration | -- | 0 | 85 / 30 / 6 | 5 | 130 | 25 | 1 / 1 / 2 | 12 / 28 | autocannon_i, armor_plate_i, ship_scanner_i |
| `losers_weepers` | Salvager | Industrial | -- | 0 | 70 / 25 / 3 | 4 | 90 | 205 | 1 / 1 / 2 | 9 / 22 | basic_tow_rig, autocannon_i, armor_plate_i |

## Tier 2

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `close_enough` | Heavy Fighter | Combat | 10 | 1 | 200 / 90 / 12 | 3 | 150 | 45 | 3 / 2 / 3 | 18 / 55 | pulse_laser_ii, pulse_laser_ii, focused_beam_i, shield_booster_ii, armor_plate_ii |
| `filibuster` | Monitor | Combat | 10 | 1 | 760 / 80 / 42 | 1 | 400 | 80 | 2 / 6 / 2 | 30 / 75 | autocannon_ii, autocannon_ii, armor_plate_ii, armor_plate_ii, armor_plate_ii, armor_plate_ii, kinetic_hull_hardener, explosive_hull_hardener, assault_barracks, crew_armory |
| `flight_risk` | Blockade Runner | Combat | 10 | 1 | 125 / 55 / 5 | 6 | 700 | 80 | 2 / 1 / 3 | 18 / 45 | autocannon_ii, afterburner_ii, shield_booster_ii, security_bulkheads, autocannon_i |
| `hostile_takeover` | Assault | Combat | 10 | 1 | 250 / 90 / 17 | 3 | 110 | 50 | 4 / 2 / 1 | 24 / 45 | autocannon_ii, autocannon_ii, autocannon_i, autocannon_i, armor_plate_ii, kinetic_hull_hardener, assault_barracks |
| `small_claims` | Corsair | Combat | -- | 1 | 240 / 130 / 14 | 5 | 300 | 60 | 3 / 2 / 2 | 36 / 70 | pulse_laser_ii, pulse_laser_ii, autocannon_ii, shield_booster_ii, armor_plate_i, ship_scanner_ii, afterburner_ii |
| `lone_star` | Multirole | Combat Support | -- | 1 | 300 / 180 / 18 | 4 | 360 | 240 | 2 / 2 / 4 | 40 / 80 | pulse_laser_ii, pulse_laser_i, shield_booster_ii, armor_plate_i, mining_laser_ii, ship_scanner_ii, cargo_expander_ii |
| `bulk_discount` | Bulk Hauler | Commercial | 10 | 1 | 300 / 50 / 5 | 2 | 760 | 900 | 1 / 1 / 6 | 22 / 50 | autocannon_i, armor_plate_ii, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, cargo_expander_ii |
| `last_call` | Tanker | Commercial | 10 | 1 | 185 / 40 / 9 | 3 | 1500 | 75 | 1 / 1 / 2 | 14 / 35 | autocannon_ii, refueling_pump, security_bulkheads, hull_reinforcement_i |
| `canteen` | Water Tender | Industrial | -- | 1 | 240 / 110 / 12 | 3 | 340 | 260 | 0 / 1 / 4 | 30 / 58 | ice_harvester_ii, cargo_expander_ii, ship_scanner_i, shield_booster_i |
| `larder` | Hunter | Industrial | -- | 1 | 460 / 80 / 32 | 4 | 420 | 260 | 3 / 2 / 3 | 30 / 60 | pulse_laser_ii, pulse_laser_ii, armor_plate_ii, shield_booster_ii, ship_scanner_ii, cargo_expander_ii, afterburner_ii |
| `mineral_rights` | Miner | Industrial | 10 | 1 | 200 / 55 / 12 | 2 | 120 | 230 | 2 / 1 / 2 | 14 / 38 | autocannon_ii, mining_laser_ii, armor_plate_ii, autocannon_ii |
| `repo` | Salvager | Industrial | 10 | 1 | 180 / 65 / 8 | 2 | 200 | 370 | 1 / 1 / 3 | 18 / 40 | advanced_tow_rig, autocannon_ii, armor_plate_ii |
| `workhorse` | Multirole | Industrial | -- | 1 | 220 / 100 / 12 | 3 | 300 | 300 | 1 / 1 / 4 | 30 / 55 | mining_laser_ii, cargo_expander_ii, ship_scanner_i, shield_booster_i, pulse_laser_i |
| `write_off` | Salvage Tug | Industrial | -- | 1 | 300 / 90 / 22 | 3 | 380 | 280 | 0 / 2 / 4 | 30 / 60 | tractor_beam, salvage_module, cargo_expander_ii, ship_scanner_i, shield_booster_ii, armor_plate_i |

## Tier 3

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `asset_forfeiture` | Cruiser | Combat | 20 | 2 | 500 / 180 / 22 | 1 | 400 | 350 | 5 / 3 / 1 | 52 / 115 | mass_driver, railgun_ii, railgun_ii, railgun_ii, heavy_torpedo, damage_control_system, reactive_armor_hardener, hull_reinforcement_i |
| `casting_vote` | Cruiser | Combat | 20 | 2 | 430 / 200 / 18 | 2 | 380 | 95 | 4 / 3 / 4 | 40 / 90 | autocannon_ii, pulse_laser_ii, railgun_ii, missile_launcher_ii, armor_plate_ii, damage_control_system, cargo_expander_ii, assault_barracks, crew_armory, hull_reinforcement_ii |
| `dark_pool` | Cruiser | Combat | 20 | 2 | 320 / 400 / 12 | 2 | 360 | 70 | 3 / 4 / 4 | 48 / 100 | pulse_laser_ii, pulse_laser_ii, focused_beam_i, shield_booster_ii, shield_booster_ii, shield_recharger_ii, damage_control_system, security_bulkheads, crew_armory, assault_barracks |
| `eviction_notice` | Cruiser | Combat | 20 | 2 | 480 / 200 / 25 | 2 | 360 | 70 | 5 / 2 / 3 | 35 / 85 | autocannon_ii, autocannon_ii, autocannon_ii, railgun_ii, missile_launcher_ii, damage_control_system, assault_barracks |
| `foreclosure` | Cruiser | Combat | 20 | 2 | 450 / 150 / 22 | 2 | 340 | 75 | 4 / 3 / 2 | 28 / 70 | autocannon_ii, autocannon_ii, autocannon_ii, missile_launcher_ii, armor_plate_ii, kinetic_hull_hardener, assault_barracks |
| `four_on_the_floor` | Heavy Fighter | Combat | 20 | 2 | 140 / 100 / 6 | 5 | 60 | 10 | 6 / 1 / 1 | 46 / 130 | heavy_torpedo, heavy_torpedo, jury_rigged_cannon, railgun_i, armor_plate_i, expanded_fuel_tank, jury_rigged_cannon, jury_rigged_cannon |
| `margin_call` | Cruiser | Combat | 20 | 2 | 440 / 190 / 20 | 2 | 340 | 65 | 3 / 3 / 4 | 36 / 82 | autocannon_ii, autocannon_ii, railgun_ii, armor_plate_ii, damage_control_system, ship_scanner_ii, assault_barracks, crew_armory |
| `rhetorical_question` | Assault | Combat | 20 | 2 | 480 / 220 / 24 | 2 | 380 | 90 | 5 / 3 / 3 | 38 / 110 | pulse_laser_ii, pulse_laser_ii, pulse_laser_ii, focused_beam_i, focused_beam_i, shield_booster_ii, armor_plate_ii, damage_control_system, assault_barracks, crew_armory |
| `running_tab` | Cruiser | Combat | 20 | 2 | 340 / 130 / 12 | 5 | 650 | 75 | 4 / 2 / 3 | 32 / 82 | autocannon_ii, autocannon_ii, autocannon_ii, railgun_ii, armor_plate_iii, damage_control_system, assault_barracks |
| `no_take_backs` | Control Cruiser | Combat Support | 20 | 2 | 380 / 340 / 14 | 2 | 380 | 90 | 2 / 4 / 5 | 64 / 120 | pulse_laser_ii, pulse_laser_ii, shield_booster_ii, shield_recharger_ii, armor_plate_ii, damage_control_system, security_bulkheads, crew_armory, assault_barracks |
| `palisade` | Escort | Combat Support | -- | 2 | 540 / 280 / 26 | 3 | 480 | 120 | 3 / 4 / 2 | 46 / 90 | pulse_laser_ii, autocannon_ii, autocannon_ii, shield_booster_ii, shield_booster_ii, armor_plate_ii, damage_control_system, ship_scanner_ii, shipboard_sickbay |
| `privateer` | Patrol Cutter | Combat Support | -- | 2 | 430 / 120 / 18 | 4 | 420 | 75 | 2 / 3 / 3 | 42 / 65 | pulse_laser_ii, autocannon_ii, shield_booster_ii, damage_control_system, ship_scanner_ii, shipboard_sickbay |
| `liquidation` | Bulk Hauler | Commercial | 20 | 2 | 450 / 200 / 18 | 2 | 400 | 745 | 1 / 2 / 4 | 30 / 70 | autocannon_ii, armor_plate_ii, damage_control_system, assault_barracks, crew_armory, security_bulkheads, cargo_expander_iii |
| `nightcap` | Hospitality Coaster | Commercial | -- | 2 | 380 / 230 / 12 | 3 | 500 | 220 | 0 / 3 / 4 | 35 / 65 | shield_booster_ii, damage_control_system, cargo_expander_ii, ship_scanner_ii |
| `shell_company` | Freighter | Commercial | 20 | 2 | 190 / 200 / 11 | 5 | 620 | 240 | 2 / 2 / 5 | 40 / 85 | pulse_laser_ii, pulse_laser_ii, shield_booster_ii, cargo_expander_iii, cargo_expander_iii, cargo_expander_ii, fuel_optimizer, afterburner_ii, shield_booster_ii |
| `homeward` | Hospital Tender | Support | -- | 2 | 430 / 260 / 15 | 3 | 480 | 180 | 0 / 4 / 4 | 55 / 95 | fleet_hospital, shield_booster_ii, shield_recharger_ii, damage_control_system |

## Tier 4

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `dead_reckoning` | Battlecruiser | Combat | 30 | 3 | 880 / 350 / 32 | 2 | 450 | 120 | 5 / 3 / 4 | 50 / 180 | jury_rigged_cannon, jury_rigged_cannon, mass_driver, scrapgun, scrapgun, outer_rim_scrap_armor, darksteel_armor, reactive_armor_hardener, tracking_computer_i |
| `eminent_domain` | Battlecruiser | Combat | 30 | 3 | 1300 / 460 / 44 | 1 | 500 | 600 | 7 / 4 / 1 | 88 / 180 | siege_railgun, siege_railgun, mass_driver, railgun_ii, railgun_ii, heavy_torpedo, missile_launcher_ii, darksteel_armor, reactive_armor_hardener, damage_control_system, hull_reinforcement_i |
| `fait_accompli` | Battlecruiser | Combat | 30 | 3 | 1200 / 500 / 50 | 2 | 350 | 120 | 7 / 3 / 3 | 65 / 160 | blood_reaver, mass_driver, autocannon_ii, autocannon_ii, autocannon_ii, missile_launcher_ii, crimson_berserker_plating, darksteel_armor, reactive_armor_hardener, autocannon_ii, tracking_computer_ii |
| `known_quantity` | Battlecruiser | Combat | 30 | 3 | 1050 / 580 / 50 | 2 | 500 | 180 | 6 / 4 / 5 | 70 / 180 | solar_lance, heavy_pulse_laser, focused_beam_iii, pulse_laser_iii, solarian_aegis, shield_booster_iv, darksteel_armor, damage_control_system, missile_launcher_ii, tracking_computer_ii |
| `no_appeal` | Assault Carrier | Combat | 30 | 3 | 1050 / 450 / 44 | 1 | 300 | 240 | 5 / 3 / 4 | 50 / 140 | blood_reaver, autocannon_ii, autocannon_ii, missile_launcher_ii, missile_launcher_ii, crimson_berserker_plating, darksteel_armor, damage_control_system, tracking_computer_ii |
| `beachhead` | Assault Transport | Combat Support | -- | 3 | 1150 / 140 / 40 | 1 | 400 | 100 | 2 / 4 / 4 | 65 / 105 | pulse_laser_ii, autocannon_ii, shield_booster_ii, damage_control_system, shipboard_sickbay, crew_armory |
| `blind_spot` | Command | Combat Support | 30 | 3 | 780 / 440 / 24 | 2 | 500 | 265 | 3 / 4 / 5 | 65 / 150 | blood_reaver, heavy_pulse_laser, missile_launcher_ii, solarian_aegis, shield_booster_iv, darksteel_armor, damage_control_system, tracking_computer_iii, security_bulkheads, crew_armory |
| `magnate` | Command | Combat Support | -- | 3 | 1500 / 600 / 90 | 3 | 760 | 200 | 3 / 6 / 5 | 55 / 130 | shield_booster_iii, shield_booster_iii, regenerative_armor_ii, hull_reinforcement_ii, damage_control_system, ship_scanner_ii |
| `no_exit` | Interdictor | Combat Support | 30 | 3 | 800 / 520 / 30 | 2 | 450 | 145 | 4 / 4 / 5 | 65 / 200 | solar_lance, focused_beam_iii, pulse_laser_iii, missile_launcher_ii, solarian_aegis, shield_booster_iv, darksteel_armor, damage_control_system, tracking_computer_iii |
| `off_the_books` | Command | Combat Support | 30 | 3 | 950 / 410 / 32 | 2 | 550 | 205 | 3 / 3 / 6 | 72 / 200 | solar_lance, focused_beam_iii, missile_launcher_ii, solarian_aegis, darksteel_armor, damage_control_system, tracking_computer_iii, security_bulkheads, crew_armory, assault_barracks |
| `standing_order` | Command Dreadnought | Combat Support | 30 | 3 | 1100 / 460 / 48 | 1 | 320 | 205 | 4 / 4 / 5 | 65 / 170 | blood_reaver, heavy_pulse_laser, missile_launcher_ii, missile_launcher_ii, solarian_aegis, shield_booster_iv, darksteel_armor, damage_control_system, tracking_computer_ii, security_bulkheads |
| `severance_package` | Salvager | Industrial | 30 | 3 | 800 / 250 / 36 | 1 | 400 | 600 | 4 / 2 / 4 | 39 / 130 | tractor_beam, blood_reaver, scrapgun, scrapgun, darksteel_armor, reactive_armor_hardener, autocannon_i, tracking_computer_ii |
| `repatriator` | Recovery Carrier | Support | -- | 3 | 950 / 320 / 30 | 2 | 1000 | 360 | 1 / 4 / 5 | 55 / 100 | shield_booster_ii, damage_control_system, ship_scanner_ii, shipboard_sickbay, cargo_expander_ii |
| `watchkeeper` | Crew Transport | Support | -- | 3 | 800 / 300 / 22 | 2 | 650 | 180 | 0 / 4 / 3 | 40 / 75 | shield_booster_ii, damage_control_system, shipboard_sickbay, cargo_expander_ii |
