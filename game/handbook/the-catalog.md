# The catalog -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## items

catalog: every item of the game: name, category (NULL where the catalog gives none), size, base value, rarity, module type and slot

- Kind: snapshot
- Columns: id, name, category, size, base_value, rarity, tradeable, stackable, type, slot, extracted_by, description, src; one row per id
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- The items of highest base value: `SELECT id, name, base_value FROM items ORDER BY base_value DESC LIMIT 10`
- How many items have no category: `SELECT COUNT(*) FROM items WHERE category IS NULL`
- Find an item by its name: `SELECT id, name, category FROM items WHERE name LIKE '%steel%'`

## recipes

catalog: every recipe: category, made by hand or only in a facility, crafting time; inputs, outputs and facilities in their own tables

- Kind: snapshot
- Columns: id, name, category, hand, facility_only, time, fuel_output, requires_unlock, description, src; one row per id
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- Recipes made by hand: `SELECT id, name, time FROM recipes WHERE hand = 1 ORDER BY name LIMIT 20`
- Recipes per category: `SELECT category, COUNT(*) FROM recipes GROUP BY category ORDER BY 2 DESC`
- What makes steel_plate: `SELECT r.id, r.name, o.units, r.hand FROM recipe_outputs o JOIN recipes r ON r.id = o.recipe WHERE o.item = 'steel_plate'`

## recipe_inputs

catalog: what a recipe takes, item and units per run

- Kind: snapshot
- Columns: recipe, item, units, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- Which recipes use steel_plate: `SELECT r.id, r.name, i.units FROM recipe_inputs i JOIN recipes r ON r.id = i.recipe WHERE i.item = 'steel_plate' ORDER BY r.name`
- What the recipe of steel_plate takes: `SELECT item, units FROM recipe_inputs WHERE recipe IN (SELECT recipe FROM recipe_outputs WHERE item = 'steel_plate')`
- The inputs most recipes use: `SELECT item, COUNT(*) FROM recipe_inputs GROUP BY item ORDER BY 2 DESC LIMIT 10`

## recipe_outputs

catalog: what a recipe makes, item and units per run

- Kind: snapshot
- Columns: recipe, item, units, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- What makes steel_plate: `SELECT recipe, units FROM recipe_outputs WHERE item = 'steel_plate'`
- Recipes with more than one output: `SELECT recipe, COUNT(*) FROM recipe_outputs GROUP BY recipe HAVING COUNT(*) > 1`
- Goods we hold that no recipe makes: `SELECT DISTINCT item FROM holdings WHERE item NOT IN (SELECT item FROM recipe_outputs)`

## recipe_facilities

catalog: the facilities a recipe runs in

- Kind: snapshot
- Columns: recipe, facility, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- Where steel_plate is made: `SELECT f.recipe, f.facility FROM recipe_facilities f JOIN recipe_outputs o ON o.recipe = f.recipe WHERE o.item = 'steel_plate'`
- Recipes per facility: `SELECT facility, COUNT(*) FROM recipe_facilities GROUP BY facility ORDER BY 2 DESC LIMIT 10`
- Recipes that run only in a facility: `SELECT id FROM recipes WHERE facility_only = 1 AND id IN (SELECT recipe FROM recipe_facilities) LIMIT 20`

## facilities

catalog: every facility type: level, build cost, time and labor, the facility it upgrades, its services, faction cap (member cap for recruitment)

- Kind: snapshot
- Columns: id, name, category, level, build_cost, build_time, labor_cost, upgrades_from, recipe, service_type, requires_service_type, faction_service_type, personal_service_type, faction_cap, power_draw, power_supply, empire, player_buildable, description, src; one row per id
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- Which facility types raise the faction's member limit, and what they cost: `SELECT id, level, faction_cap AS member_cap, build_cost, build_time, labor_cost, upgrades_from FROM facilities WHERE faction_service_type = 'faction_recruitment' ORDER BY level`
- Faction facilities by cost: `SELECT id, faction_service_type, level, build_cost FROM facilities WHERE category = 'faction' ORDER BY build_cost`
- The upgrade chain above hiring_board: `WITH RECURSIVE up(id, level) AS (SELECT id, level FROM facilities WHERE id = 'hiring_board' UNION ALL SELECT f.id, f.level FROM facilities f JOIN up ON f.upgrades_from = up.id) SELECT id, level FROM up`

## facility_materials

catalog: what a facility takes to build, item and units

- Kind: snapshot
- Columns: facility, item, units, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- What recruitment_desk takes to build: `SELECT item, units FROM facility_materials WHERE facility = 'recruitment_desk'`
- Facilities that need steel_plate: `SELECT facility, units FROM facility_materials WHERE item = 'steel_plate' ORDER BY units DESC LIMIT 20`
- The recruitment chain's materials against what we hold: `SELECT m.item, SUM(m.units) AS needed, (SELECT SUM(units) FROM holdings h WHERE h.item = m.item) AS held FROM facility_materials m JOIN facilities f ON f.id = m.facility WHERE f.faction_service_type = 'faction_recruitment' GROUP BY m.item`

## hulls

catalog: every hull (the catalog's `ships`): class, tier, cargo, hull, shield, slots, the piloting it needs; no price is in the catalog

- Kind: snapshot
- Columns: id, name, class, tier, category, faction, shipyard_tier, piloting_required, cargo, hull, shield, armor, speed, fuel, cpu, power, weapon_slots, defense_slots, utility_slots, build_time, description, src; one row per id
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- The hulls with the most cargo: `SELECT id, name, class, tier, cargo FROM hulls ORDER BY cargo DESC LIMIT 10`
- Tier 2 hulls of the voidborn: `SELECT id, name, class, cargo, piloting_required FROM hulls WHERE tier = 2 AND faction = 'voidborn'`
- Hulls per class: `SELECT class, COUNT(*) FROM hulls GROUP BY class ORDER BY 2 DESC`

## hull_materials

catalog: what a hull takes to build, item and units

- Kind: snapshot
- Columns: hull, item, units, src
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- What the hull of most cargo takes to build: `SELECT item, units FROM hull_materials WHERE hull = (SELECT id FROM hulls ORDER BY cargo DESC LIMIT 1)`
- Hulls that need processing_core: `SELECT hull, units FROM hull_materials WHERE item = 'processing_core' ORDER BY units DESC LIMIT 10`
- Materials over all tier 1 hulls: `SELECT m.item, SUM(m.units) FROM hull_materials m JOIN hulls h ON h.id = m.hull WHERE h.tier = 1 GROUP BY m.item ORDER BY 2 DESC LIMIT 10`

## skills

catalog: every skill: category, highest level, how it is trained, the empire that may learn it

- Kind: snapshot
- Columns: id, name, category, max_level, training, empire, description, src; one row per id
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `catalog`, The newest catalog/<version>.json by its version number (craftbook.load's rule); ammo.json and other names are no catalog
- Every skill: `SELECT id, name, category, max_level FROM skills ORDER BY category, id`
- How mining is trained: `SELECT id, training FROM skills WHERE id = 'mining'`
- Skills only one empire may learn: `SELECT id, empire FROM skills WHERE empire IS NOT NULL`

## game_releases

SpaceMolt official release notes and patch changes from catalog/releases.json (synced automatically by scripts/changelog-refresh.py)

- Kind: snapshot
- Columns: version, sort_key, pub_date, summary, bullets, src; one row per version
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `game_releases`, data/catalog/releases.json
- Newest 10 SpaceMolt releases and patch summaries: `SELECT version, pub_date, summary FROM game_releases ORDER BY sort_key DESC LIMIT 10`
- Releases mentioning recipes, hulls or storms: `SELECT version, pub_date, summary FROM game_releases WHERE summary LIKE '%recipe%' OR summary LIKE '%hull%' OR summary LIKE '%storm%' ORDER BY sort_key DESC`
- Count of synced releases and latest version: `SELECT COUNT(*) AS releases, MAX(version) AS max_ver FROM game_releases`
