# Voidborn -- Hulls

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.717.0; never edited by hand.
Up: [master-index.md](../master-index.md). Hulls: 65. The Piloting a tier needs, from the hulls of the catalog: tier 2: Piloting 10; tier 3: Piloting 20; tier 4: Piloting 30; tier 5: Piloting 50.
What a hull is built from: `python3 -I -B game/fleet/craftbook.py build <hull id>`, or `tables/ships.tsv`.

## Tier 0

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `threshold` | Miner | Industrial | -- | 0 | 75 / 80 / 3 | 1 | 95 | 65 | 1 / 2 / 2 | 16 / 30 | mining_laser_i, pulse_laser_i |

## Tier 1

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `absence` | Shuttle | Civilian | -- | 0 | 45 / 80 / 1 | 3 | 110 | 25 | 0 / 2 / 3 | 18 / 32 | shield_booster_i |
| `paradox` | Fighter | Combat | -- | 0 | 60 / 130 / 2 | 3 | 100 | 15 | 2 / 2 / 1 | 20 / 40 | pulse_laser_i, pulse_laser_i, shield_booster_i, shield_recharger_i |
| `apeiron` | Electronic Warfare | Combat Support | -- | 0 | 70 / 90 / 3 | 3 | 100 | 15 | 1 / 2 / 2 | 22 / 40 | ion_blaster_i, shield_booster_i, em_shield_hardener, stasis_webifier_i, sensor_dampener |
| `vigil` | Patrol | Combat Support | -- | 0 | 75 / 90 / 3 | 3 | 110 | 20 | 2 / 2 / 2 | 22 / 38 | pulse_laser_i, pulse_laser_i, shield_booster_i, shield_booster_i |
| `fugue` | Courier | Commercial | -- | 0 | 55 / 100 / 2 | 4 | 110 | 55 | 0 / 2 / 2 | 20 / 36 | shield_booster_i |
| `eigenstate` | Scout | Exploration | -- | 0 | 55 / 90 / 2 | 3 | 100 | 30 | 0 / 2 / 3 | 24 / 36 | ship_scanner_i, shield_booster_i |
| `qualia` | Explorer | Exploration | -- | 0 | 60 / 85 / 3 | 3 | 130 | 30 | 0 / 2 / 3 | 20 / 34 | cloaking_device_i, shield_booster_i, shield_recharger_i |
| `accretion` | Gas Harvester | Industrial | -- | 0 | 55 / 85 / 3 | 2 | 90 | 65 | 0 / 2 / 4 | 22 / 36 | gas_harvester_i, gas_harvester_i, shield_booster_i, cargo_expander_i |
| `liminal` | Miner | Industrial | -- | 0 | 65 / 120 / 2 | 2 | 100 | 75 | 0 / 2 / 3 | 18 / 34 | mining_laser_i, shield_booster_i, shield_booster_i |
| `residuum` | Salvager | Industrial | -- | 0 | 50 / 85 / 2 | 2 | 90 | 100 | 0 / 2 / 3 | 22 / 36 | basic_tow_rig, cloaking_device_i, ship_scanner_i, shield_booster_i |
| `rime` | Ice Harvester | Industrial | -- | 0 | 50 / 80 / 2 | 2 | 110 | 65 | 0 / 2 / 3 | 20 / 35 | ice_harvester_i, shield_booster_i, shield_recharger_i |

## Tier 2

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `reticence` | Yacht | Civilian | 10 | 1 | 135 / 165 / 5 | 3 | 250 | 30 | 0 / 3 / 2 | 30 / 58 | -- |
| `dualism` | Heavy Fighter | Combat | 10 | 1 | 160 / 175 / 7 | 2 | 270 | 35 | 2 / 3 / 2 | 30 / 60 | pulse_laser_ii, focused_beam_i, shield_booster_ii, shield_booster_ii, em_shield_hardener |
| `recursion` | Fighter | Combat | 10 | 1 | 150 / 150 / 6 | 4 | 360 | 35 | 3 / 2 / 2 | 28 / 58 | pulse_laser_ii, pulse_laser_ii, focused_beam_i, shield_booster_ii, shield_recharger_ii |
| `census` | Customs Patrol | Combat Support | 10 | 1 | 140 / 165 / 5 | 3 | 150 | 35 | 2 / 2 / 3 | 30 / 55 | pulse_laser_i, pulse_laser_i, shield_booster_i, shield_booster_i, warp_scrambler |
| `penumbra` | Electronic Warfare | Combat Support | 10 | 1 | 130 / 160 / 5 | 2 | 160 | 30 | 1 / 3 / 3 | 40 / 68 | ion_blaster_i, em_shield_hardener, shield_booster_ii, adaptive_shield_i, stasis_webifier_i, warp_disruptor, cloaking_device_i |
| `apophenia` | Freighter | Commercial | 10 | 1 | 140 / 145 / 6 | 2 | 300 | 240 | 1 / 2 / 2 | 24 / 44 | shield_booster_ii, shield_booster_ii |
| `interstice` | Recon | Covert | 10 | 1 | 135 / 150 / 4 | 3 | 200 | 40 | 0 / 3 / 4 | 36 / 62 | -- |
| `parallax` | Recon | Covert | 10 | 1 | 130 / 155 / 4 | 3 | 180 | 40 | 1 / 3 / 3 | 36 / 64 | -- |
| `confluence` | Explorer | Exploration | 10 | 1 | 130 / 145 / 5 | 3 | 360 | 120 | 1 / 2 / 4 | 34 / 58 | survey_scanner_i, shield_booster_ii |
| `hysteresis` | Research | Exploration | 10 | 1 | 140 / 150 / 5 | 2 | 240 | 120 | 0 / 3 / 4 | 40 / 65 | survey_scanner_i, shield_booster_ii |
| `entropy` | Salvager | Industrial | 10 | 1 | 140 / 145 / 6 | 2 | 330 | 240 | 0 / 2 / 4 | 28 / 48 | advanced_tow_rig, afterburner_ii, shield_booster_ii |
| `hoarfrost` | Ice Harvester | Industrial | 10 | 1 | 140 / 150 / 5 | 2 | 360 | 170 | 0 / 2 / 3 | 22 / 44 | ice_harvester_ii, ice_harvester_ii, shield_booster_ii |
| `nebulous` | Gas Harvester | Industrial | 10 | 1 | 140 / 150 / 5 | 2 | 300 | 175 | 0 / 2 / 4 | 28 / 46 | gas_harvester_ii, shield_booster_ii |
| `resonance_miner` | Miner | Industrial | 10 | 1 | 150 / 160 / 6 | 2 | 330 | 180 | 0 / 2 / 4 | 28 / 48 | mining_laser_ii, shield_booster_ii |
| `anamnesis` | Medical | Support | 10 | 1 | 135 / 155 / 5 | 2 | 170 | 35 | 0 / 3 / 4 | 38 / 60 | shipboard_sickbay, shield_booster_ii, shield_recharger_ii, em_shield_hardener |

## Tier 3

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `cloister` | Liner | Civilian | 20 | 2 | 360 / 420 / 12 | 2 | 420 | 80 | 0 / 4 / 2 | 40 / 100 | -- |
| `annihilation` | Battlecruiser | Combat | 20 | 2 | 360 / 430 / 13 | 2 | 380 | 95 | 4 / 4 / 3 | 50 / 125 | focused_beam_ii, focused_beam_ii, pulse_laser_iii, ion_blaster_ii, adaptive_shield_i, shield_booster_iii, damage_control_system, shield_booster_ii |
| `voidborn_singularity` | Cruiser | Combat | 20 | 2 | 380 / 450 / 14 | 2 | 380 | 75 | 3 / 4 / 4 | 55 / 115 | focused_beam_ii, pulse_laser_iii, ion_blaster_ii, shield_booster_iii, adaptive_shield_i, damage_control_system, shield_booster_ii, cloaking_device_ii |
| `aporia` | Interdictor | Combat Support | 20 | 2 | 340 / 400 / 12 | 2 | 360 | 50 | 2 / 4 / 5 | 58 / 120 | ion_blaster_ii, shield_booster_iii, adaptive_shield_i, damage_control_system |
| `gestalt` | Drone Carrier | Combat Support | 20 | 2 | 350 / 380 / 12 | 2 | 380 | 95 | 1 / 3 / 5 | 58 / 105 | shield_booster_iii, shield_recharger_ii, damage_control_system |
| `palinode` | Control Cruiser | Combat Support | 20 | 2 | 430 / 430 / 16 | 2 | 420 | 105 | 2 / 4 / 5 | 76 / 140 | ion_blaster_i, pulse_laser_ii, shield_booster_ii, shield_recharger_ii, em_shield_hardener, security_bulkheads, crew_armory, shipboard_sickbay |
| `attenuation` | Hazmat Freighter | Commercial | 20 | 2 | 380 / 240 / 15 | 2 | 350 | 340 | 1 / 2 / 4 | 42 / 48 | lead_lined_cargo_i, shield_booster_ii |
| `fold_hauler` | Freighter | Commercial | 20 | 2 | 380 / 350 / 10 | 2 | 350 | 635 | 1 / 2 / 4 | 32 / 75 | shield_booster_iii, cargo_expander_ii, cargo_expander_ii |
| `catharsis` | Intelligence | Covert | 20 | 2 | 340 / 370 / 11 | 2 | 380 | 35 | 1 / 3 / 6 | 60 / 118 | anomaly_detector, ship_scanner_ii, shield_booster_iii |
| `noumenon` | Explorer | Exploration | 20 | 2 | 320 / 360 / 10 | 2 | 560 | 215 | 1 / 3 / 5 | 55 / 100 | anomaly_detector, shield_booster_iii, shield_recharger_ii |
| `absolute_entropy` | Ice Harvester | Industrial | 20 | 2 | 260 / 380 / 6 | 1 | 220 | 420 | 0 / 2 / 5 | 35 / 75 | ice_harvester_iii, shield_booster_iii, shield_booster_ii |
| `deep_resonance` | Miner | Industrial | 20 | 2 | 180 / 200 / 8 | 5 | 500 | 130 | 0 / 2 / 5 | 40 / 90 | mining_laser_iii, mining_laser_iii, afterburner_iii, survey_scanner_ii |
| `dissolution` | Salvager | Industrial | 20 | 2 | 260 / 350 / 8 | 2 | 330 | 555 | 0 / 3 / 5 | 40 / 95 | advanced_tow_rig, shield_booster_iii, shield_booster_ii, cargo_expander_ii |
| `phase_collector` | Gas Harvester | Industrial | 20 | 2 | 260 / 380 / 6 | 1 | 220 | 400 | 0 / 2 / 5 | 35 / 75 | gas_harvester_iii, shield_booster_iii, shield_booster_ii |
| `poiesis` | Workshop | Industrial | 20 | 2 | 320 / 460 / 10 | 1 | 320 | 300 | 0 / 4 / 5 | 52 / 110 | -- |
| `sublimation` | Refinery | Industrial | 20 | 2 | 370 / 380 / 14 | 1 | 230 | 265 | 0 / 3 / 5 | 50 / 105 | -- |
| `substrate` | Refinery | Industrial | 20 | 2 | 380 / 400 / 16 | 1 | 250 | 240 | 0 / 3 / 6 | 52 / 110 | -- |
| `silent_tide` | Carrier | Support | 20 | 2 | 440 / 300 / 18 | 1 | 460 | 100 | 1 / 3 / 3 | 35 / 85 | shield_booster_iii, shield_recharger_ii, damage_control_system |

## Tier 4

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `membrane` | Cruiser | Combat | 30 | 3 | 800 / 920 / 30 | 2 | 480 | 95 | 3 / 5 / 5 | 82 / 200 | phase_disruptor, focused_beam_iii, entropy_beam, voidborn_phase_armor, adaptive_shield_ii, shield_booster_iv, phase_cloaking_device, damage_control_system |
| `voidborn_event_horizon` | Battlecruiser | Combat | 30 | 3 | 900 / 1000 / 35 | 2 | 450 | 120 | 4 / 5 / 5 | 85 / 210 | phase_disruptor, focused_beam_iii, void_lance_i, entropy_beam, voidborn_phase_armor, adaptive_shield_ii, shield_booster_iv, shield_booster_iii, damage_control_system |
| `consensus` | Command | Combat Support | 30 | 3 | 850 / 950 / 30 | 2 | 600 | 120 | 2 / 5 / 7 | 90 / 220 | shield_booster_iv, adaptive_shield_ii, shield_booster_iii, ship_scanner_iii, cargo_expander_iii |
| `superposition` | Drone Carrier | Combat Support | 30 | 3 | 880 / 950 / 32 | 1 | 420 | 360 | 2 / 5 / 6 | 105 / 210 | phase_disruptor, void_lance_i, adaptive_shield_iii, shield_booster_iv, adaptive_shield_ii, voidborn_phase_armor, damage_control_system, advanced_drone_bay, combat_drone_bay, phase_cloaking_device, ship_maintenance_bay |
| `dimensional_fold` | Freighter | Commercial | 30 | 3 | 700 / 900 / 20 | 1 | 400 | 1380 | 1 / 3 / 5 | 45 / 120 | cargo_expander_iii, expanded_fuel_tank, shield_booster_iv, shield_booster_iii |
| `plenum` | Tanker | Commercial | 30 | 3 | 800 / 600 / 18 | 1 | 12000 | 260 | 0 / 4 / 6 | 45 / 130 | refueling_pump, expanded_fuel_tank, expanded_fuel_tank, shield_booster_iv, shield_booster_iii, adaptive_shield_ii |
| `palimpsest` | Intelligence | Covert | 30 | 3 | 780 / 900 / 28 | 2 | 500 | 70 | 2 / 5 / 6 | 90 / 200 | shield_booster_iv, adaptive_shield_ii, shield_booster_iii, ship_scanner_iii, phase_cloaking_device |
| `solipsism` | Recon | Covert | 30 | 3 | 90 / 180 / 4 | 5 | 320 | 15 | 0 / 2 / 4 | 50 / 120 | ship_scanner_ii, phase_cloaking_device, adaptive_shield_i, shield_booster_ii |
| `alloy_synthesizer` | Refinery | Industrial | 30 | 3 | 600 / 800 / 18 | 1 | 300 | 600 | 0 / 3 / 6 | 55 / 150 | -- |
| `harmonic` | Miner | Industrial | 30 | 3 | 700 / 900 / 22 | 1 | 320 | 1440 | 0 / 3 / 8 | 65 / 140 | mining_laser_iv, mining_laser_iv, mining_laser_iv, mining_laser_iv, mining_laser_iv, shield_booster_iv |
| `influx` | Refinery | Industrial | 30 | 3 | 650 / 850 / 18 | 1 | 300 | 660 | 0 / 3 / 7 | 50 / 135 | gas_harvester_iv |
| `thermodynamic_end` | Salvager | Industrial | 30 | 3 | 700 / 550 / 18 | 1 | 420 | 635 | 0 / 3 / 6 | 55 / 140 | advanced_tow_rig, cargo_expander_iii, cargo_expander_iii, cargo_expander_iii, shield_booster_iv, shield_booster_iii |
| `verglas` | Refinery | Industrial | 30 | 3 | 600 / 900 / 16 | 1 | 300 | 600 | 0 / 3 / 7 | 50 / 135 | ice_harvester_iv |

## Tier 5

| Hull | Class | Work | Piloting | Yard tier | Hull / shield / armor | Speed | Fuel | Cargo | Slots W / D / U | CPU / power | Fitted as built |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `apotheosis` | Dreadnought | Combat | 50 | 4 | 2200 / 2500 / 80 | 1 | 700 | 505 | 6 / 7 / 7 | 135 / 420 | null_cannon, void_lance_ii, dark_matter_projector, phase_disruptor, focused_beam_iii, focused_beam_iii, voidborn_phase_armor, adaptive_shield_iii, shield_booster_iv, shield_booster_iv, adaptive_shield_ii, nanite_hull_coating |
| `overmind` | Drone Carrier | Combat Support | 50 | 4 | 2400 / 2500 / 75 | 1 | 650 | 600 | 4 / 7 / 8 | 125 / 400 | phase_disruptor, focused_beam_iii, pulse_laser_iii, pulse_laser_iii, voidborn_phase_armor, adaptive_shield_iii, shield_booster_iv, adaptive_shield_ii, shield_booster_iii, damage_control_system |
| `omniscience` | Research | Exploration | 50 | 4 | 2000 / 2200 / 65 | 1 | 750 | 575 | 2 / 6 / 9 | 140 / 380 | focused_beam_iii, pulse_laser_iii, voidborn_phase_armor, adaptive_shield_iii, shield_booster_iv, shield_booster_iii, adaptive_shield_ii |
| `manifold` | Miner | Industrial | 50 | 4 | 1400 / 2000 / 45 | 1 | 600 | 2400 | 0 / 5 / 9 | 90 / 300 | mining_laser_iv |
| `rift_siphon` | Gas Harvester | Industrial | 50 | 4 | 1400 / 2200 / 40 | 1 | 600 | 2400 | 0 / 5 / 9 | 88 / 290 | gas_harvester_iv |
| `emanation` | Mobile Base | Support | -- | 4 | 2200 / 3600 / 70 |  |  |  | None / None / None | None / None | -- |
| `pleroma` | Medical | Support | 50 | 4 | 2100 / 2400 / 70 | 1 | 800 | 480 | 2 / 7 / 8 | 150 / 430 | fleet_hospital, shipboard_sickbay |
