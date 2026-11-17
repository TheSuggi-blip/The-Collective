# Fuel Production -- Recipes

Built by `python3 -B scripts/catalog-index.py` from the game's catalog, version 0.723.0; never edited by hand.
Up: [master-index.md](../master-index.md). Recipes: 8; by hand: 0; in a facility only: 8.

| Recipe | Makes | From | Where | Time |
|---|---|---|---|---|
| `extract_fuel_cell` | fuel_reserve x 20 | fuel_cell x 1 | in: fuel_cell_extractor, automated_fuel_plant, high_throughput_fuel_works, advanced_fuel_extraction_complex | 0.6 |
| `extract_military_fuel_cell` | fuel_reserve x 100 | military_fuel_cell x 1 | in: military_fuel_cell_extractor, military_fuel_refinery, military_fuel_manufacturing_plant, military_fuel_production_complex | 3 |
| `extract_premium_fuel_cell` | fuel_reserve x 50 | premium_fuel_cell x 1 | in: premium_fuel_cell_extractor, premium_fuel_processing_plant, premium_fuel_manufacturing_works, premium_fuel_production_complex | 1.5 |
| `manufacture_fuel_basic` | fuel_reserve x 100 | liquid_hydrogen x 10 | in: h2_fuel_combustor, h2_fuel_plant, h2_fuel_complex, h2_fuel_hub | 3 |
| `manufacture_fuel_catalytic` | fuel_reserve x 200 | platinum_catalyst x 1; liquid_hydrogen x 4 | in: catalytic_fuel_refinery, catalytic_fuel_plant, catalytic_fuel_complex, catalytic_fuel_hub | 2 |
| `manufacture_fuel_h2o2` | fuel_reserve x 200 | liquid_hydrogen x 2; liquid_oxygen x 2 | in: peroxide_reaction_cell, h2o2_combustion_plant, bipropellant_fuel_complex, h2o2_synthesis_hub | 6 |
| `manufacture_fuel_plasma` | fuel_reserve x 500 | plasma_gas x 4 | in: plasma_fuel_combustor, plasma_fuel_plant, plasma_fuel_complex, plasma_synthesis_reactor | 15 |
| `manufacture_methane_fuel` | fuel_reserve x 100 | liquid_methane x 6 | in: methane_fuel_reformer, methane_fuel_plant, methane_fuel_complex, methane_fuel_hub | 4 |
