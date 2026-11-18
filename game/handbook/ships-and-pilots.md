# Ships and pilots -- the store's handbook

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
Up: [game/handbook.md](../handbook.md): how the data flows, and every call of this subject under Where to ask what.
One table alone: `hive.py handbook <table>`; its rows: `hive.py sql "SELECT ..."` (the tool sql).

## ships

now: one row per ship of ours (fleet/fleet.json): member and division, place, docked at which base, hull, fuel, hold, wallet, the order it flies

- Kind: snapshot
- Columns: pilot, member, division, role, number, class, empire, status, activity, system, poi, docked, base, in_transit, hull, max_hull, shield, max_shield, fuel, max_fuel, cargo_used, cargo_capacity, credits, flies, t, src; one row per pilot
- Kept: the last reading of its file, replaced when the file changes; a missing or bad file keeps them (source.note says why)
- Refreshed: the store's pass (every 60 s): ships from fleet/fleet.json (read again when it or fleet/flagships.json changed), and the order each flies (loaders fleet, orders)
- Where are our ships, by system: `SELECT system, COUNT(*) AS ships FROM ships GROUP BY system ORDER BY ships DESC`
- Ships low on fuel: `SELECT pilot, system, fuel, max_fuel FROM ships WHERE fuel < max_fuel / 4 ORDER BY fuel`
- What each division flies now: `SELECT division, flies, COUNT(*) FROM ships GROUP BY division, flies ORDER BY division, 3 DESC`

## ship_skills

now: every skill of every ship with its level and XP (fleet/ships/<pilot>.json)

- Kind: snapshot
- Columns: pilot, skill, level, xp, src; one row per pilot, skill
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `ships`, data/fleet/ships/*.json
- The highest Piloting levels: `SELECT pilot, level FROM ship_skills WHERE skill = 'piloting' ORDER BY level DESC LIMIT 10`
- Average and highest level per skill: `SELECT skill, ROUND(AVG(level), 1), MAX(level) FROM ship_skills GROUP BY skill ORDER BY 2 DESC`
- The skills of the mining division: `SELECT k.skill, ROUND(AVG(k.level), 1) FROM ship_skills k JOIN ships s ON s.pilot = k.pilot WHERE s.division = 'Mining' GROUP BY k.skill ORDER BY 2 DESC`

## ship_modules

now: every module fitted to every ship (fleet/ships/<pilot>.json)

- Kind: snapshot
- Columns: pilot, module, name, slot, kind, src
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `ships`, data/fleet/ships/*.json
- How many ships carry each module: `SELECT module, COUNT(DISTINCT pilot) FROM ship_modules GROUP BY module ORDER BY 2 DESC`
- Ships with an ice harvester: `SELECT pilot FROM ship_modules WHERE module = 'ice_harvester_i'`
- Ships without a mining laser: `SELECT pilot FROM ships WHERE pilot NOT IN (SELECT pilot FROM ship_modules WHERE module = 'mining_laser_i')`

## ship_cargo

now: what each ship carries in its hold, from its own live file (fleet/ships/<pilot>.json)

- Kind: snapshot
- Columns: pilot, item, units, src
- Kept: while its file stands: a file's rows are replaced when it changes and go when it goes
- Refreshed: the store's pass (every 60 s), when a file changed (size or mtime): loader `ships`, data/fleet/ships/*.json
- What our holds carry, by item: `SELECT item, SUM(units) FROM ship_cargo GROUP BY item ORDER BY 2 DESC`
- Which ships carry iron_ore: `SELECT pilot, units FROM ship_cargo WHERE item = 'iron_ore' ORDER BY units DESC`
- Ships with a full hold: `SELECT pilot, cargo_used, cargo_capacity FROM ships WHERE cargo_used >= cargo_capacity`

## fleet_positions

view: our ships per system: the system's name, empire and jumps from home, ships, docked, flying (in space), ships per division

- Kind: view over ships, systems
- Columns: system, name, empire, jumps, ships, docked, flying, command, mining, logistics, trade, military, intel
- Kept: nothing: a view stores no row
- Refreshed: computed when asked, from its tables
- Where are our ships, by system and division: `SELECT * FROM fleet_positions ORDER BY ships DESC`
- Our ships away from home: `SELECT system, name, empire, jumps, ships FROM fleet_positions WHERE jumps > 0 ORDER BY jumps DESC`
- Systems where ships lie docked: `SELECT system, docked, flying FROM fleet_positions WHERE docked > 0`

## stats_pilot_hour

history (stats.py): per pilot, key and UTC hour in which it moved: a skill's level and total XP (value) and the gain since the pilot's reading before, or a counter of its ship file (ships_lost, ships_destroyed, pirates_destroyed, damage_taken); kept 8 days

- Kind: statistics
- Columns: hour, pilot, role, key, level, value, gain, t; one row per hour, pilot, key
- Kept: 8 days (stats.py KEEP)
- Refreshed: stats.py part `pilots`, once an hour (the store's first pass of a UTC hour)
- XP gained per skill in the last 24 hours: `SELECT key, SUM(gain) FROM stats_pilot_hour WHERE gain > 0 AND key NOT IN ('ships_lost', 'ships_destroyed', 'pirates_destroyed', 'damage_taken') AND hour >= strftime('%s', 'now') - 86400 GROUP BY key ORDER BY 2 DESC`
- Ships lost per role in the last 24 hours: `SELECT role, SUM(gain) FROM stats_pilot_hour WHERE key = 'ships_lost' AND gain > 0 AND hour >= strftime('%s', 'now') - 86400 GROUP BY role`
- Piloting XP of one pilot hour by hour: `SELECT datetime(hour, 'unixepoch'), level, value, gain FROM stats_pilot_hour WHERE key = 'piloting' ORDER BY pilot, hour DESC LIMIT 24`

## stats_pilot_last

state (stats.py): each pilot's and key's newest reading, against which the next hour's gain is measured

- Kind: statistics
- Columns: pilot, key, level, value, t; one row per pilot, key
- Kept: for good: no step of the code deletes its rows
- Refreshed: stats.py part `pilots`, once an hour (the store's first pass of a UTC hour)
- The highest Piloting levels: `SELECT pilot, level, value FROM stats_pilot_last WHERE key = 'piloting' ORDER BY level DESC, value DESC LIMIT 10`
- Pilots per Piloting level: `SELECT level, COUNT(*) FROM stats_pilot_last WHERE key = 'piloting' GROUP BY level ORDER BY level`
- When each pilot was last read: `SELECT pilot, datetime(MAX(t), 'unixepoch') FROM stats_pilot_last GROUP BY pilot ORDER BY 2 LIMIT 20`
